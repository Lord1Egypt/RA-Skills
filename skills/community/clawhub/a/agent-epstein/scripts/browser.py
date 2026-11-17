"""Browser transport — the primary path.

Two jobs:

1. Get past bot walls (Cloudflare and friends) and logged-in-only views
   that a plain HTTP client cannot reach. Uses a PERSISTENT profile so a
   user logs in ONCE and later runs reuse the session.

2. Act as an authenticated HTTP client: once the browser holds the site's
   clearance/login cookies, we navigate straight to the site's JSON API
   and read it out of the rendered page. That is how a Cloudflare-gated
   booru can still be harvested through its API instead of by scraping DOM.

CREDENTIALS: this module never accepts, stores, or types a password.
When a site needs a login it raises NeedsLogin; the caller opens a HEADED
window, tells the human "log in here", and waits for them to finish.
"""
from __future__ import annotations

import json
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

from errors import Blocked, NeedsLogin

CHALLENGE_MARKERS = (
    "just a moment",
    "attention required",
    "checking your browser",
    "verify you are human",
    "enable javascript and cookies",
    "cf-browser-verification",
    "ddos protection by",
)

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


class Browser:
    """Context manager around a persistent Playwright browser profile.

    profile_dir : per-source persistent dir; logins survive across runs.
    headed      : a REAL visible window. Bot walls clear far more reliably
                  headed than headless; also required for human login.
    channel     : "msedge" / "chrome" to use an installed real browser
                  build (best bot-wall pass rate), or None for bundled
                  Chromium.
    """

    def __init__(
        self,
        profile_dir: str | Path,
        headed: bool = False,
        channel: str | None = None,
        timeout_ms: int = 45_000,
        cdp_url: str = "",
    ) -> None:
        self.profile_dir = Path(profile_dir)
        self.headed = headed
        self.channel = channel or None
        self.timeout_ms = timeout_ms
        # When set, ATTACH to an already-running real browser instead of
        # launching our own. This is the answer to sites that refuse to let
        # an automated browser log in (X): the human logs into their own
        # browser once, and we drive that session.
        self.cdp_url = cdp_url
        self._pw = None
        self.ctx = None
        self.page = None
        self._attached = False

    # -- lifecycle ---------------------------------------------------------
    def __enter__(self) -> "Browser":
        self._pw = sync_playwright().start()
        if self.cdp_url:
            return self._attach_cdp()
        return self._launch()

    def _attach_cdp(self) -> "Browser":
        """Attach to a browser already running with --remote-debugging-port."""
        self._attached = True
        try:
            self.browser = self._pw.chromium.connect_over_cdp(self.cdp_url)
        except Exception as e:                               # noqa: BLE001
            # A refused connection is nearly always "the browser on that
            # port was never started". Say so with the fix, rather than
            # dumping a Playwright stack trace at someone who cannot see
            # which of their twenty steps actually failed.
            raise RuntimeError(
                f"could not attach to a browser at {self.cdp_url}: "
                f"{type(e).__name__}\n"
                f"  Start it first, in its own terminal:\n"
                f"    python scripts/start_browser.py --port "
                f"{urllib.parse.urlparse(self.cdp_url).port or 9222}\n"
                f"  Log in there, then re-run this command with the same "
                f"--cdp value.") from e
        if not self.browser.contexts:
            raise RuntimeError(
                f"attached to {self.cdp_url} but it has no browser context; "
                f"start the browser with at least one tab open")
        self.ctx = self.browser.contexts[0]
        self.ctx.set_default_timeout(self.timeout_ms)
        pages = [p for p in self.ctx.pages if not p.is_closed()]
        self.page = pages[-1] if pages else self.ctx.new_page()
        print(f"attached to existing browser at {self.cdp_url} "
              f"({len(pages)} tab(s))")
        return self

    def _launch(self) -> "Browser":
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        kwargs: dict = {
            "user_data_dir": str(self.profile_dir),
            "headless": not self.headed,
            "viewport": {"width": 1440, "height": 1000},
            "user_agent": DEFAULT_UA,
            "locale": "en-US",
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        }
        if self.channel:
            kwargs["channel"] = self.channel
        self.ctx = self._pw.chromium.launch_persistent_context(**kwargs)
        self.ctx.set_default_timeout(self.timeout_ms)
        self.page = self.ctx.pages[0] if self.ctx.pages else self.ctx.new_page()
        return self

    def __exit__(self, *exc) -> None:
        try:
            if self._attached or getattr(self, "keep_open", False):
                # Disconnect only. Never close a browser we did not open —
                # that is the user's own window with their other tabs in it.
                # keep_open covers the other case: WE opened it, but handed
                # it to the user mid-run (the ChatGPT login gate), so closing
                # would take away the window they were told to use.
                pass
            elif self.ctx:
                self.ctx.close()
        except Exception:                                        # noqa: BLE001
            pass
        finally:
            if self._pw:
                try:
                    self._pw.stop()
                except Exception:                                # noqa: BLE001
                    pass

    # -- navigation --------------------------------------------------------
    def goto(self, url: str, wait: str = "domcontentloaded", settle: float = 1.0):
        resp = self.page.goto(url, wait_until=wait)
        if settle:
            self.page.wait_for_timeout(int(settle * 1000))
        return resp

    def text(self) -> str:
        try:
            return self.page.inner_text("body") or ""
        except Exception:
            return ""

    def title(self) -> str:
        try:
            return self.page.title() or ""
        except Exception:
            return ""

    # -- bot walls ---------------------------------------------------------
    def is_challenged(self) -> bool:
        blob = (self.title() + " " + self.text()[:2500]).lower()
        return any(m in blob for m in CHALLENGE_MARKERS)

    def clear_challenge(self, max_wait_s: int = 30) -> bool:
        """Wait for an interstitial to resolve itself. True if it cleared."""
        deadline = time.time() + max_wait_s
        while time.time() < deadline:
            if not self.is_challenged():
                return True
            self.page.wait_for_timeout(1500)
        return False

    # -- login walls -------------------------------------------------------
    def logged_in(self, logged_in_selectors: tuple[str, ...] = ()) -> bool:
        """Positive proof of a session. Wins over every negative signal."""
        for sel in logged_in_selectors:
            try:
                if self.page.query_selector(sel):
                    return True
            except Exception:                                    # noqa: BLE001
                continue
        return False

    def login_wall(
        self,
        url_markers: tuple[str, ...],
        dom_selectors: tuple[str, ...] = (),
        logged_in_selectors: tuple[str, ...] = (),
    ) -> bool:
        """Does the current page look like a login wall?

        Checked in this order on purpose:
          1. positive logged-in evidence -> NOT a wall, stop looking
          2. login-ish URL
          3. login-ish DOM
        Without step 1 a page that merely *contains* a "Sign in" link
        reads as a wall, and we nag a user who is already signed in.
        """
        if logged_in_selectors and self.logged_in(logged_in_selectors):
            return False
        url = (self.page.url or "").lower()
        if any(m in url for m in url_markers):
            return True
        for sel in dom_selectors:
            try:
                if self.page.query_selector(sel):
                    return True
            except Exception:                                    # noqa: BLE001
                continue
        return False

    def login_needed(self, spec) -> bool:
        """`spec` is any object carrying the login_* marker tuples — a
        sources.Source satisfies it, so the markers live with the site
        definition instead of being hardcoded in the orchestrator."""
        return self.login_wall(
            tuple(getattr(spec, "login_url_markers", ()) or ("/login",)),
            tuple(getattr(spec, "login_dom_markers", ()) or ()),
            tuple(getattr(spec, "logged_in_markers", ()) or ()),
        )

    def probe_login(self, spec, settle: float = 3.0) -> str:
        """Visit the site root and classify the session.

        Returns 'logged_in' | 'needs_login' | 'unknown'.
        """
        url = getattr(spec, "base", "") or getattr(spec, "login_url", "")
        if not url:
            return "unknown"
        try:
            self.goto(url, wait="domcontentloaded", settle=settle)
        except Exception:                                        # noqa: BLE001
            return "unknown"
        if self.is_challenged():
            self.clear_challenge(20)
        if self.logged_in(tuple(getattr(spec, "logged_in_markers", ()) or ())):
            return "logged_in"
        if self.login_wall(
            tuple(getattr(spec, "login_url_markers", ()) or ("/login",)),
            tuple(getattr(spec, "login_dom_markers", ()) or ()),
        ):
            return "needs_login"
        # No positive either way: logged-out sites often just render a
        # generic marketing page, so treat "no evidence" as needs_login
        # for a source that declares needs_login.
        return "needs_login" if getattr(spec, "needs_login", False) else "unknown"

    def await_human_login(
        self,
        url: str,
        url_markers: tuple[str, ...],
        dom_selectors: tuple[str, ...] = (),
        max_wait_s: int = 600,
        poll_s: int = 3,
        logged_in_selectors: tuple[str, ...] = (),
    ) -> bool:
        """Open `url`, then block until the human logs in.

        NEVER types credentials. The human does that in the window.
        Returns True when the wall is gone, False on timeout.
        """
        self.goto(url, wait="domcontentloaded", settle=2.0)
        deadline = time.time() + max_wait_s
        announced = False
        while time.time() < deadline:
            wall = self.login_wall(url_markers, dom_selectors, logged_in_selectors)
            # When the caller supplied POSITIVE logged-in markers, absence
            # of a wall is not enough — sites bounce an unauthenticated
            # session through onboarding URLs that match no marker at all.
            # Demand real evidence before declaring success.
            proven = self.logged_in(logged_in_selectors) if logged_in_selectors else True
            if proven and not wall:
                try:
                    self.ctx.storage_state(
                        path=str(self.profile_dir / "state.json"))
                except Exception:                                # noqa: BLE001
                    pass
                return True
            if not announced:
                print(f"\n[LOGIN REQUIRED] A browser window is open at:\n  {url}\n"
                      f"  Log in there yourself. This process is waiting up to "
                      f"{max_wait_s}s and will continue automatically.\n",
                      flush=True)
                announced = True
            self.page.wait_for_timeout(poll_s * 1000)
        return False

    # -- browser-as-HTTP-client -------------------------------------------
    def get_json(self, url: str, retries: int = 2):
        """Fetch a JSON endpoint THROUGH the browser session.

        Navigating to a .json URL renders raw JSON as page text; reading
        it back means the request carried the browser's cookies, so
        Cloudflare-gated APIs answer that curl cannot even reach.
        Returns parsed JSON, or raises Blocked.
        """
        last = ""
        for attempt in range(retries + 1):
            self.goto(url, wait="domcontentloaded", settle=max(1.0, attempt * 1.5))
            if self.is_challenged():
                if not self.clear_challenge():
                    last = "bot wall did not clear"
                    continue
            raw = self.text().strip()
            if not raw:
                last = "empty body"
                continue
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                head = raw[:160].replace("\n", " ")
                if head.lower().startswith("<!doctype") or head.lower().startswith("<html"):
                    last = f"html instead of json: {head}"
                    continue
                last = f"non-json body: {head}"
                continue
        raise Blocked(f"could not read JSON from {url}: {last}")

    def fetch_bytes(self, url: str, referer: str | None = None) -> bytes:
        """Download an asset through the browser session.

        Two-stage on purpose. The request context is cheap and shares the
        browser's cookies, but hotlink-protected CDNs (danbooru's
        cdn.donmai.us, pixiv's i.pximg.net) still 403 it: they check for a
        real document/image navigation with full browser headers, not a
        side-channel fetch. So fall back to navigating the page straight
        at the asset, which is exactly what an <img> load looks like.
        """
        headers = {"Referer": referer} if referer else {}
        stage = ""
        try:
            resp = self.ctx.request.get(url, headers=headers,
                                        timeout=self.timeout_ms)
            if resp.ok:
                return resp.body()
            stage = f"request-context HTTP {resp.status}"
        except Exception as e:                               # noqa: BLE001
            stage = f"request-context {type(e).__name__}: {e}"

        try:
            nav = self.page.goto(url, wait_until="domcontentloaded")
            if nav and nav.ok:
                return nav.body()
            stage += f"; nav HTTP {nav.status if nav else 'no-response'}"
        except Exception as e:                               # noqa: BLE001
            stage += f"; nav {type(e).__name__}: {e}"

        raise Blocked(f"could not fetch {url} ({stage})")
