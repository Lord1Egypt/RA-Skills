"""chatgpt_web.py — upload a harvested dataset to the ChatGPT web UI.

Drives a logged-in browser session: opens a chat, attaches a batch of
images, optionally sends a short message, and moves to the next batch.

LOGIN: nothing here types or stores credentials. If the session is not
already signed in, a visible window opens and waits for YOU to log in
(including 2FA). The session is kept in a persistent profile so later runs
reuse it.

WHY THE SELECTORS ARE DISCOVERED AT RUNTIME
-------------------------------------------
This drives a UI that is not a stable interface and changes without
notice. Rather than hardcoding one selector and failing opaquely, the
script probes several candidates, and reports what it actually found and
clicked. If ChatGPT's markup shifts, run with --inspect to see the
candidates present on the page, then pass --file-input / --composer /
--send-button explicitly.

A note you should read once: uploading third-party artwork makes the
representations in OpenAI's Terms of Use ("you have all rights, licenses,
and permissions needed to provide Input") yours to make. That is a
decision about your own account and it is yours to take; this script does
not make it for you.

    python chatgpt_web.py --dataset ./ds
    python chatgpt_web.py --dataset ./ds --batch 20 --message "here you go"
    python chatgpt_web.py --dataset ./ds --dry-run      # everything but send
    python chatgpt_web.py --inspect                     # dump the markup
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from browser import Browser, NeedsLogin                          # noqa: E402
from normalize import load_jsonl                                 # noqa: E402

# Decoupled from the skill name on purpose: this directory holds the user's
# signed-in session, so a rename must not orphan it. See harvest.py for the
# override variable.
DEFAULT_PROFILE = Path(
    os.environ.get("HARVEST_PROFILE_ROOT", "")
    or Path.home() / ".cache" / "art-dataset-harvest" / "profiles"
) / "chatgpt"

# Candidate selectors, most likely first. Kept as lists so drift is
# survivable and the failure is informative rather than silent.
# Verified against a live session. There is more than one file input on the
# page: `#upload-files` (the composer) plus separate ones for photo/media
# pickers. Selecting by tag name alone picks whichever comes first in DOM
# order, which is the composer's visually-hidden wrapper — files go in and
# NOTHING renders, so the send then carries zero attachments with no error.
# Target the composer's input by id first, and prefer one that is actually
# wired to photo upload over a bare tag match.
# Verified by inspecting a real sent conversation: `set_input_files` on the
# first input[type=file] (which is #upload-files) DOES attach images. A
# Free account silently capped a 4-image batch at 2.
#
# The catch, and the reason this is easy to get wrong: an attached image
# renders NO preview chip in the composer. There is no element to count
# before sending. Probing for one and finding none proves nothing — an
# earlier revision concluded the upload was dead on exactly that evidence
# and was wrong. Acceptance is only observable AFTER sending, by counting
# images in the message that was posted. See sent_image_count().
FILE_INPUTS = (
    'input[type="file"]',
    'input[type="file"][multiple]',
)
COMPOSERS = (
    '#prompt-textarea',
    'div[contenteditable="true"].ProseMirror',
    'div[contenteditable="true"]',
    'textarea[data-id]',
)
# Verified against BOTH a Free and a Plus account, because they differ.
# Free exposes [data-testid="send-button"] on a <div>. Plus has no testid at
# all: the control is a real <button type="submit" aria-label="Send"> that
# only appears once there is something to send. Selecting by element name
# alone, or by the older aria-labels, fails on one account or the other.
SEND_BUTTONS = (
    '[data-testid="send-button"]',
    'form button[aria-label="Send"]',
    'form button[type="submit"]',
    '[aria-label="Send prompt"]',
    '[aria-label="Send message"]',
)
LOGIN_URL_MARKERS = ("/auth/login", "/auth/0", "/login")
LOGIN_DOM = ('input[name="username"]', 'input[type="email"]', 'input[name="password"]')
# Positive proof of a session. Without these, login_wall() has only negative
# signals to work from and can either nag an already-signed-in user or, worse,
# declare success on a page that merely stopped looking like a login form.
# Verified against BOTH accounts. #prompt-textarea exists on a Free
# conversation view but NOT on a fresh new-chat page; the contenteditable
# ProseMirror div is present in both and is the reliable marker, because it
# only mounts once there is a real chat surface to type into.
LOGGED_IN_DOM = (
    'div[contenteditable="true"].ProseMirror',
    'div[contenteditable="true"][id="prompt-textarea"]',
    '#prompt-textarea',
    '[data-testid="accounts-profile-button"]',
)

# What the setting is actually called in the ChatGPT UI, so the human can
# find it. This is printed, never touched: an account-level training toggle
# governs everything the user sends, not just this batch, and changing it is
# their decision to make in their own settings.
TRAINING_SETTING = (
    "Settings -> Data controls -> 'Improve the model for everyone'"
)

# NOTE: there is deliberately no attachment-chip selector list here.
# An earlier revision had one and it was wrong in a costly way. An attached
# image renders NO preview in the composer, so the list always matched zero
# — and zero was read as "the upload did nothing", which led to the
# conclusion that attaching was broken when it demonstrably works.
# Do not reintroduce a pre-send count. Acceptance is measured after the
# send, by sent_image_count().

# Text ChatGPT shows when it refuses work: plan caps, rate limits, file-size
# rejections. Matched case-insensitively against visible body text.
LIMIT_PATTERNS = (
    "too many requests",
    "rate limit",
    "rate-limit",
    "hit the limit",
    "you've reached",
    "you have reached",
    "upgrade to",
    "free tier",
    "maximum of",
    "limit of",
    "up to 10 files",
    "files per message",
    "file size",
    "unable to upload",
    "failed to upload",
    "unsupported file",
    "too large",
)


def first_present(page, selectors, what: str, required: bool = True):
    for sel in selectors:
        try:
            el = page.query_selector(sel)
        except Exception:                                        # noqa: BLE001
            continue
        if el:
            print(f"  {what}: matched {sel}")
            return el, sel
    if required:
        raise RuntimeError(
            f"could not find {what}. Run --inspect and pass an explicit "
            f"selector, or the page may not have finished loading."
        )
    print(f"  {what}: not found (optional)")
    return None, ""

def content_image_count(page) -> int:
    """Count images in the page that are actual content, not chrome.

    Filters out avatars and other UI imagery by src. Everything else on a
    ChatGPT thread is an uploaded image.

    Deliberately does NOT try to scope to "the last message". There is no
    stable selector for a turn: on the markup observed, every ancestor of
    an uploaded image is a bare <div> with no data-testid, no
    data-message-id, and no role. Scoping guesses were what made the
    earlier acceptance check report success while delivering nothing.
    """
    try:
        return int(page.evaluate(
            r"""() => [...document.querySelectorAll('img')]
                .filter(i => {
                  const s = (i.src || '');
                  if (!s) return false;
                  // Avatars, icons and provider branding are not content.
                  return !/cdn\.auth0\.com|gravatar|sentinel|logo/i.test(s);
                }).length"""))
    except Exception as e:                                       # noqa: BLE001
        print(f"  could not count images: {e}", file=sys.stderr)
        return -1


def sent_image_count(page, baseline: int | None = None) -> int:
    """How many images this batch actually delivered.

    Measured as a DELTA against a baseline taken before sending. A capped
    account keeps only some attachments, silently and with no error, so
    the only honest number is "how many more images are on the page than
    were there before I pressed send".

    Returns -1 when it cannot measure. Callers MUST treat -1 as unknown,
    never as success: laundering an unmeasurable result into a pass is how
    this check reported "1/1 sent" for a message that arrived with nothing
    attached.
    """
    now = content_image_count(page)
    if now < 0:
        return -1
    if baseline is None:
        return now
    return max(0, now - baseline)


def find_limit_notice(page) -> str:
    """Return the refusal text if the page is showing one, else ''."""
    blob = ""
    try:
        blob = (page.inner_text("body") or "").lower()
    except Exception:                                            # noqa: BLE001
        try:
            blob = (page.title() or "").lower()
        except Exception:                                        # noqa: BLE001
            return ""
    for pat in LIMIT_PATTERNS:
        if pat in blob:
            # Return the sentence around it so the human sees the real
            # message rather than a bare pattern name.
            i = blob.find(pat)
            return blob[max(0, i - 90):i + 110].replace("\n", " ").strip()
    return ""


def parse_until(text: str, now: datetime | None = None) -> datetime | None:
    """Parse a human "keep retrying until" value into a deadline.

    Accepts an ISO timestamp, HH:MM (today or tomorrow if already past),
    a relative "+90m" / "+2h", or a duration like "90 minutes". Returns
    None when the input cannot be understood, so the caller can refuse
    rather than silently defaulting to "retry forever".
    """
    now = now or datetime.now()
    s = (text or "").strip()
    if not s:
        return None

    if s.lower().startswith("+"):
        m = re.fullmatch(r"\+(\d+)\s*([mhm])?", s)
        if m:
            n = int(m.group(1))
            unit = (m.group(2) or "m").lower()
            return now + timedelta(minutes=n) if unit == "m" \
                else now + timedelta(hours=n)
        return None

    m = re.fullmatch(r"(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours)",
                     s, re.I)
    if m:
        n = int(m.group(1))
        return now + (timedelta(minutes=n) if m.group(2).lower().startswith("m")
                      else timedelta(hours=n))

    m = re.fullmatch(r"(\d{1,2}):(\d{2})", s)
    if m:
        cand = now.replace(hour=int(m.group(1)), minute=int(m.group(2)),
                           second=0, microsecond=0)
        if cand <= now:
            cand += timedelta(days=1)
        return cand

    try:
        cand = datetime.fromisoformat(s)
    except ValueError:
        return None
    if cand.tzinfo is not None:
        cand = cand.astimezone().replace(tzinfo=None)
    return cand


def wait_until(deadline: datetime, page=None,
               poll_s: int = 30) -> bool:
    """Sleep until `deadline`, returning False if it is already past."""
    while datetime.now() < deadline:
        remaining = (deadline - datetime.now()).total_seconds()
        print(f"  limit reached; retrying in {int(remaining // 60)}m "
              f"{int(remaining % 60)}s "
              f"(until {deadline.strftime('%H:%M:%S')})", flush=True)
        time.sleep(min(poll_s, max(1, remaining)))
        if page is not None:
            notice = find_limit_notice(page)
            if not notice:
                return True          # the notice cleared; go ahead now
    return False


def handle_retry(br, owed, args, sent: int = 0) -> int:
    """Re-send whatever did not land, honouring --retry-until.

    Default is to STOP. Retrying is a policy choice the user makes, not
    something the script should decide on its own: hammering an account
    that just said "no" until a wall-clock deadline can look like abuse,
    and a plan cap may never lift at all.

    `--retry-until` accepts "HH:MM", "+90m", "2 hours", or an ISO
    timestamp. An unparseable value is refused loudly rather than silently
    becoming "retry forever".
    """
    owed = list(dict.fromkeys(owed))     # order-preserving dedupe

    if not args.retry_until:
        print(f"\n{len(owed)} image(s) were not delivered. Re-run later, or "
              f"pass --retry-until to keep trying.")
        return 4

    deadline = parse_until(args.retry_until)
    if deadline is None:
        print(f"could not understand --retry-until {args.retry_until!r}. "
              f"Use HH:MM, +90m, '2 hours', or an ISO timestamp. Not "
              f"retrying.", file=sys.stderr)
        return 4

    print(f"\n{len(owed)} image(s) outstanding; will retry until "
          f"{deadline.strftime('%Y-%m-%d %H:%M')}.")
    remaining = list(owed)
    delivered = sent
    while remaining:
        if not wait_until(deadline, br.page):
            print(f"  gave up at the deadline; {len(remaining)} image(s) "
                  f"never sent: {', '.join(f.name for f in remaining)}")
            return 4
        still: list[Path] = []
        for i in range(0, len(remaining), max(1, args.batch)):
            chunk = remaining[i:i + max(1, args.batch)]
            landed = send_batch(br, chunk, args)
            if landed < len(chunk):
                print(f"  {landed}/{len(chunk)} landed; queuing the rest")
                still.extend(chunk[landed:])
            else:
                delivered += landed
        if not still:
            print(f"  all outstanding images delivered ({delivered} total).")
            return 0
        print(f"  {len(still)} still outstanding; waiting for the next window.")
        remaining = still
    return 0


def send_batch(br, batch, args) -> bool:
    """Attach, type and send one batch. Returns how many images actually
    landed, which on a capped account is fewer than were submitted.

    Never trust the send succeeding. A capped account drops attachments
    silently, so acceptance is measured by counting images in the posted
    message afterwards.
    """
    br.goto(args.url, wait="domcontentloaded", settle=2.5)
    clear_composer(br.page)
    # Baseline BEFORE attaching; see the note in main().
    baseline = content_image_count(br.page)
    el, sel = first_present(
        br.page, (args.file_input,) if args.file_input else FILE_INPUTS,
        "file input")
    el.set_input_files([str(f) for f in batch])
    composer, _ = first_present(br.page,
                                (args.composer,) if args.composer else COMPOSERS,
                                "composer")
    composer.click()
    try:
        composer.fill(args.message)
    except Exception:                                            # noqa: BLE001
        br.page.keyboard.type(args.message)
    send, _ = first_present(br.page,
                            (args.send_button,) if args.send_button else SEND_BUTTONS,
                            "send button")
    wait_enabled(br.page, send)
    br.page.wait_for_timeout(int(args.settle * 1000))
    if args.dry_run:
        return len(batch)
    send.click()
    br.page.wait_for_timeout(int(args.settle * 1000) + 3000)
    return sent_image_count(br.page, baseline)


def clear_composer(page) -> None:
    """Empty the composer without sending.

    A fresh chat URL still restores the previous draft in some cases, which
    would concatenate this batch's message onto the last one and then send
    both. Select-all plus delete is the only reliable clear.
    """
    try:
        composer, _ = first_present(page, COMPOSERS, "composer",
                                    required=False)
        if composer is None:
            return
        composer.click()
        page.keyboard.press("Control+a")
        page.keyboard.press("Delete")
    except Exception:                                            # noqa: BLE001
        pass


def wait_enabled(page, el, timeout_ms: int = 120_000) -> bool:
    """Wait for a button to stop being disabled (uploads finished)."""
    waited = 0
    step = 500
    while waited < timeout_ms:
        try:
            if el.is_enabled():
                return True
        except Exception:                                        # noqa: BLE001
            pass
        page.wait_for_timeout(step)
        waited += step
    return False


def login_prompt(br, url: str) -> None:
    """Open the window and print what the AGENT must relay to the user.

    The person using this skill is talking to an agent, not sitting at a
    terminal. Anything printed to stdout here is read by that agent, not by
    the user. So this does not ask the user to type into a script they never
    see; it emits a block the agent copies into the conversation, and the
    user answers in their own client.

    The script never reads a credential field and never types into it.
    """
    br.goto(url, wait="domcontentloaded", settle=2.0)
    # Hand the window back to the user and DO NOT let the context manager
    # close it. The script exits right after printing this block, which
    # unwinds into Browser.__exit__ -> self.ctx.close() and shut the window
    # the user was just told to sign into, so the gate could never be
    # satisfied. The profile dir persists, so the session survives; only
    # the window died. keep_open makes __exit__ a disconnect instead.
    br.keep_open = True
    print("\n" + "=" * 66)
    print("  NEEDS HUMAN LOGIN — relay this to the user verbatim")
    print("=" * 66)
    print("  A browser window is now open at:")
    print(f"    {url}")
    print()
    print("  Ask the user to:")
    print("    1. Sign in to ChatGPT in that window (including any 2FA or")
    print("       passkey prompt). Nothing is typed for them.")
    print("    2. Confirm they have signed in.")
    print("    3. Check Settings -> Data controls -> 'Improve the model for")
    print("       everyone' is ON, if they want these uploads to be eligible")
    print("       for training. It is an account-wide permission switch;")
    print("       do not change it on their behalf.")
    print()
    print("  Then re-run this script with --logged-in, which skips the gate.")
    print("=" * 66 + "\n", flush=True)


def await_session(br, timeout_s: int = 120) -> bool:
    """Poll the page for positive proof of a session. No stdin involved.

    Used by --logged-in: the user said they are signed in, so rather than
    trusting that claim blindly, watch the DOM for actual evidence. Requires
    logged-in markers rather than mere absence of a wall, because ChatGPT's
    SPA keeps a stable URL across the whole auth flow.
    """
    if br.logged_in(LOGGED_IN_DOM):
        return True
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(3)
        if br.logged_in(LOGGED_IN_DOM):
            return True
    return False


def image_paths(ds: Path, limit: int = 0) -> list[Path]:
    rows = load_jsonl(ds / "metadata.jsonl")
    out: list[Path] = []
    for r in rows:
        rel = r.get("file_name") or r.get("file_path")
        if not rel:
            continue
        p = ds / rel
        if p.exists():
            out.append(p)
    if limit:
        out = out[:limit]
    return out


def inspect(page) -> None:
    print("\n--- candidate elements present on this page ---")
    for label, sels in (("file input", FILE_INPUTS),
                        ("composer", COMPOSERS),
                        ("send button", SEND_BUTTONS)):
        print(f"\n{label}:")
        for s in sels:
            try:
                n = len(page.query_selector_all(s))
            except Exception:                                    # noqa: BLE001
                n = -1
            print(f"  {n:>3}x  {s}")
    try:
        print("\ncomposer outerHTML (first 400 chars):")
        _, sel = first_present(page, COMPOSERS, "composer", required=False)
        if sel:
            html = page.eval_on_selector(sel, "el => el.outerHTML")
            print("  " + html[:400])
    except Exception as e:                                       # noqa: BLE001
        print(f"  (could not dump composer: {e})")


def parse_args(argv=None):
    """Build the parser. Split out so the tests can read defaults without
    opening a browser."""
    p = argparse.ArgumentParser(
        description="Upload a harvested dataset to the ChatGPT web UI.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--batch", type=int, default=10,
                   help="images per conversation. 10 matches ChatGPT's "
                        "attachment cap; higher values silently lose files "
                        "on capped accounts rather than erroring.")
    p.add_argument("--message", default="here you go",
                   help="text sent with each batch")
    p.add_argument("--limit", type=int, default=0, help="cap total images")
    p.add_argument("--url", default="https://chatgpt.com/")
    p.add_argument("--profile", default=str(DEFAULT_PROFILE))
    p.add_argument("--channel", default="msedge",
                   help="'msedge'/'chrome' for an installed browser, '' for bundled")
    p.add_argument("--cdp", default="",
                   help="attach to an already-open ChatGPT browser instead of "
                        "launching one, e.g. http://localhost:9223. Needed "
                        "when the profile is already held by a running "
                        "browser, which otherwise fails with 'Opening in "
                        "existing browser session'. The attached window is "
                        "never closed.")
    p.add_argument("--new-chat-per-batch", action="store_true", default=True,
                   help="start a fresh conversation for each batch (default on)")
    p.add_argument("--no-new-chat", dest="new_chat_per_batch",
                   action="store_false")
    p.add_argument("--login-wait", type=int, default=180)
    p.add_argument("--logged-in", action="store_true",
                   help="the user has signed in already. Skips the login "
                        "prompt, but still verifies a real session before "
                        "uploading anything.")
    p.add_argument("--settle", type=float, default=3.0,
                   help="seconds to wait after attaching before sending")
    p.add_argument("--dry-run", action="store_true",
                   help="attach and type, but do NOT click send")
    p.add_argument("--inspect", action="store_true",
                   help="dump candidate selectors on the page, then exit")
    p.add_argument("--retry-until", default="",
                   help="on a limit refusal, keep retrying until this time. "
                        "Accepts HH:MM, +90m, '2 hours', or an ISO "
                        "timestamp. Default is to STOP and report: a plan "
                        "cap may never lift, and retrying past a refusal "
                        "can look like abuse. Only retry when you have "
                        "decided that is what you want.")
    p.add_argument("--file-input", default="")
    p.add_argument("--composer", default="")
    p.add_argument("--send-button", default="")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    ds = Path(args.dataset).resolve()
    if not (ds / "metadata.jsonl").exists():
        print(f"no metadata.jsonl in {ds}", file=sys.stderr)
        return 1

    imgs = image_paths(ds, args.limit)
    if not imgs:
        print(f"no images referenced by {ds}/metadata.jsonl", file=sys.stderr)
        return 1

    batches = [imgs[i:i + args.batch] for i in range(0, len(imgs), args.batch)]
    print(f"dataset  : {ds}")
    print(f"images   : {len(imgs)}")
    print(f"batches  : {len(batches)} of up to {args.batch}")
    print(f"message  : {args.message!r}")
    print(f"mode     : {'DRY RUN (no send)' if args.dry_run else 'send'}")

    with Browser(Path(args.profile), headed=True,
                 channel=args.channel or None,
                 cdp_url=args.cdp) as br:
        br.goto(args.url, wait="domcontentloaded", settle=3.0)

        # -- login gate: the human does this, never the script -----------
        # Positive logged-in evidence wins over the wall check, so a
        # signed-in user with a "Log in" link in the nav is not nagged.
        if br.login_wall(LOGIN_URL_MARKERS, LOGIN_DOM, LOGGED_IN_DOM):
            if args.logged_in:
                # The user says they signed in. Verify, don't trust the
                # claim: ChatGPT keeps a stable URL across the auth flow,
                # so a wall-free page is not proof of anything.
                if not await_session(br, timeout_s=args.login_wait):
                    print("  --logged-in was set but no session is "
                          "detectable. The sign-in did not take, or it "
                          "expired. Re-run without it.", file=sys.stderr)
                    return 2
                print("  session confirmed\n")
            else:
                # Print the request and stop. Do NOT block waiting on
                # stdin: the user is not at this terminal, they are in a
                # chat client talking to an agent, so they cannot answer a
                # prompt they never see.
                login_prompt(br, args.url)
                return 2

        if args.inspect:
            inspect(br.page)
            return 0

        # Make sure we are actually on a chat surface, not still on auth.
        if br.login_wall(LOGIN_URL_MARKERS, LOGIN_DOM, LOGGED_IN_DOM):
            print("still on a login page — sign in, then re-run "
                  "with --logged-in", file=sys.stderr)
            return 2

        # Surface the account-level training setting before any upload. It
        # governs whether attachments are eligible for training, it is
        # account-wide rather than per-batch, and it is the user's to change.
        print(f"note: for these uploads to be eligible for training, make sure")
        print(f"      {TRAINING_SETTING} is ON in your ChatGPT settings.")
        print("      This script does not change that setting for you.")

        sent = 0
        dropped: list[Path] = []
        unconfirmed: list[Path] = []
        for bi, batch in enumerate(batches, 1):
            print(f"\n--- batch {bi}/{len(batches)}  ({len(batch)} files) ---")

            if args.new_chat_per_batch and bi > 1:
                br.goto(args.url, wait="domcontentloaded", settle=2.5)
                clear_composer(br.page)

            # Baseline BEFORE attaching. Taken after, it already includes the
            # composer's own preview, so the post-send delta comes out ~0 and
            # a perfectly good upload gets reported as a total failure.
            baseline = content_image_count(br.page)

            # Attach. This is the step that works: set_input_files on the
            # composer's input really does attach images, but a capped
            # account keeps only some of them with no error at all, so
            # acceptance can only be confirmed after the send.
            el, fsel = first_present(
                br.page, (args.file_input,) if args.file_input else FILE_INPUTS,
                "file input")
            el.set_input_files([str(f) for f in batch])
            print(f"  submitted {len(batch)} file(s) via {fsel}:")
            for f in batch:
                print(f"    {f.name}")

            # An attached image renders as a data:/blob: preview in the
            # composer. If that never appeared, the attach silently did
            # nothing and there is no point pressing send.
            time.sleep(2.0)
            staged = content_image_count(br.page)
            if staged <= baseline:
                print("  ATTACH FAILED: the composer shows no preview of "
                      "what was submitted. Not sending — a message with "
                      "no image would look like success.", file=sys.stderr)
                unconfirmed.extend(batch)
                continue
            print(f"  composer preview shows {staged - baseline} attachment(s)")

            composer, _ = first_present(
                br.page, (args.composer,) if args.composer else COMPOSERS,
                "composer")
            composer.click()
            try:
                composer.fill(args.message)
            except Exception:                                    # noqa: BLE001
                # contenteditable does not support fill() everywhere
                br.page.keyboard.type(args.message)
            print(f"  typed message")

            # Let the uploads finish: the send button stays disabled until
            # every attachment has been accepted.
            send, _ = first_present(
                br.page, (args.send_button,) if args.send_button else SEND_BUTTONS,
                "send button", required=False)
            if send is not None:
                ok = wait_enabled(br.page, send)
                print(f"  send button enabled: {ok}")
            br.page.wait_for_timeout(int(args.settle * 1000))

            if args.dry_run:
                print("  DRY RUN: not clicking send")
                continue

            if send is None:
                send, _ = first_present(
                    br.page, (args.send_button,) if args.send_button else SEND_BUTTONS,
                    "send button")
            send.click()
            br.page.wait_for_timeout(int(args.settle * 1000) + 3000)

            # The ONLY honest acceptance check: how many more images are on
            # the page than before the send. A capped account drops the
            # overflow with no error, and there is no per-turn selector to
            # scope to, so the delta is the measurement.
            landed = sent_image_count(br.page, baseline)
            notice = find_limit_notice(br.page)
            if landed < 0:
                # Unmeasurable. Say so. Do NOT report this as a success.
                print("  VERIFICATION FAILED: could not measure whether the "
                      "images arrived. Treat this batch as UNCONFIRMED.")
                unconfirmed.extend(batch)
            else:
                print(f"  images delivered: {landed}/{len(batch)} submitted")
                if notice:
                    print(f"  ChatGPT said: {notice}")
                if landed < len(batch):
                    short = len(batch) - landed
                    print(f"  {short} image(s) were dropped - account limit.")
                    dropped.extend(batch[landed:])
                sent += min(landed, len(batch))
                print(f"  sent  (confirmed {sent} total)")
            br.page.wait_for_timeout(1500)

        # ---- report, honestly -------------------------------------------
        print(f"\ndone. {sent} image(s) "
              f"{'prepared' if args.dry_run else 'confirmed sent'} "
              f"across {len(batches)} batch(es).")
        if unconfirmed:
            print(f"\n{len(unconfirmed)} image(s) UNCONFIRMED: the script "
                  f"could not verify delivery. They may or may not have "
                  f"arrived — open the conversation and look.")
            for f in unconfirmed:
                print(f"  - {f.name}")
            return 5
        if dropped:
            print(f"\n{len(dropped)} image(s) were submitted but did NOT "
                  f"land. ChatGPT accepted the message and silently kept "
                  f"fewer images than were sent — that is an account cap, "
                  f"not an error:")
            for f in dropped:
                print(f"  - {f.name}")
            print("\nSend the remainder in a smaller batch, or pass "
                  "--retry-until to keep trying on a schedule.")
            return handle_retry(br, dropped, args, sent)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

