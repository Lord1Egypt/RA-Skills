#!/usr/bin/env python3
"""Session-contract regression: bootstrap / recall / finish.

bootstrap dumps the shared context and points at the session commands;
recall is a read-only grep over shared memory (AND by default, --all = OR,
--limit caps output, exit 1 on no hit); finish closes a session — summary
(stdin) into today's daily log, a last_seen refresh, and the inbox
report / --archive-inbox split required by SPEC 3.6.

Runs fully offline against a throwaway central dir. Run:
    python3 scripts/test_session.py
"""
import io
import json
import os
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest import mock

TMP = Path(tempfile.mkdtemp(prefix="ag-session-"))
os.environ["AGENT_GUILD_DIR"] = str(TMP)  # must precede the ag import
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ag  # noqa: E402

FAILED = []


def check(label, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {label}: got={got!r} want={want!r}")
    if not ok:
        FAILED.append(label)


def run(fn, args, stdin=""):
    """Invoke an ag cmd_* with argv + faked stdin; return (exit, stdout)."""
    out = io.StringIO()
    old = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(out):
            code = fn(list(args))
    finally:
        sys.stdin = old
    return code, out.getvalue()


def build_guild():
    for rel in ag.SKELETON:
        (ag.CENTRAL / rel).mkdir(parents=True, exist_ok=True)
    (ag.CENTRAL / "memory/shared").mkdir(parents=True, exist_ok=True)
    for rel in ag.PLACEHOLDERS:  # the 5 bootstrap files + ledgers + RETENTION
        p = ag.CENTRAL / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(ag.PLACEHOLDERS[rel], encoding="utf-8")
    (ag.CENTRAL / "identity/profile.md").write_text(
        "# Who the user is\n\nLikes coffee and espresso.\n", encoding="utf-8")
    (ag.CENTRAL / "rules/universal.md").write_text(
        "# Universal rules\n\n- Brew coffee slowly, never rush.\n", encoding="utf-8")
    (ag.CENTRAL / "memory/shared/notes.md").write_text(
        "# Shared notes\n\nTea goes into memory/shared.\n", encoding="utf-8")
    (ag.CENTRAL / "messages/archive/from-cara-to-alice-old.md").write_text(
        "an archived kerfluffle\n", encoding="utf-8")
    (ag.CENTRAL / "registry.json").write_text(json.dumps({
        "protocol_version": "3.3", "central_dir": "~/.agent-guild/",
        "agents": {"alice": {"home": "/tmp/alice", "install_tier": "readonly"}}}),
        encoding="utf-8")
    # bootstrap runs the upgrade self-check — keep tests offline
    (ag.CENTRAL / "UPGRADE.md").write_text("mode = off\n", encoding="utf-8")


def main():
    # -- _session_path: relative -> central, write pre-creates parents -------
    check("session path resolves under central",
          ag._session_path("messages/archive"), ag.CENTRAL / "messages/archive")
    deep = ag._session_path("log/decisions/a/b", write=True)
    check("session path write makes parents", deep.parent.is_dir(), True)
    check("session path absolute passthrough",
          ag._session_path(Path("/tmp/abs.md")), Path("/tmp/abs.md"))

    # -- atomic_append: lock-protected, never loses an append ---------------
    notes = ag.CENTRAL / "log/decisions/scratch.md"
    ag.atomic_append(notes, "first")
    ag.atomic_append(notes, "second")
    check("atomic_append concatenates",
          notes.read_text(encoding="utf-8"), "first\nsecond\n")
    check("append lock sidecar exists",
          (notes.parent / f".{notes.name}.ag-lock").is_file(), True)

    build_guild()

    # Context inspection can be explicitly free of maintenance and network
    # hooks. Verify both bypass and no changes anywhere in the guild.
    def snapshot():
        return {str(p.relative_to(ag.CENTRAL)): p.read_bytes()
                for p in ag.CENTRAL.rglob("*") if p.is_file()}

    # Background startup must not read any task-bearing files, even if the
    # same workspace or agent had unfinished work in another conversation.
    private_sources = [ag.CENTRAL / "projects/active.md",
                       ag.CENTRAL / "handoff/shared-state/current-focus.md",
                       ag.host_dir() / ag.HOST_NOTES]
    for source in private_sources:
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("UNRELATED_TASK_CONTEXT_MUST_NOT_LOAD", encoding="utf-8")
    original_read = Path.read_text
    def guarded_read(path, *args, **kwargs):
        if path in private_sources:
            raise AssertionError("bootstrap read unrelated task context")
        return original_read(path, *args, **kwargs)
    before = snapshot()
    with mock.patch.object(Path, "read_text", guarded_read), \
            mock.patch.object(ag, "maybe_auto_groom") as groom, \
            mock.patch.object(ag, "maybe_auto_upgrade") as upgrade:
        code, out = run(ag.cmd_bootstrap, ["alice", "--no-maintenance"])
    check("bootstrap without maintenance exit", code, 0)
    check("bootstrap without maintenance still reads context",
          "3/3 context files loaded" in out, True)
    check("bootstrap without maintenance skips grooming", groom.called, False)
    check("bootstrap without maintenance skips upgrade checks", upgrade.called, False)
    check("bootstrap without maintenance leaves guild unchanged", snapshot() == before, True)

    # -- bootstrap: dumps context + points at the session commands ----------
    code, out = run(ag.cmd_bootstrap, ["alice"])
    check("bootstrap exit", code, 0)
    check("bootstrap shows profile", "WHO THE USER IS" in out, True)
    check("bootstrap excludes focus", "CURRENT FOCUS" in out, False)
    check("bootstrap excludes projects", "ACTIVE PROJECTS" in out, False)
    check("bootstrap shows only 3 background files", "3/3 context files loaded" in out, True)
    check("bootstrap explains opt-in", "Task context: not loaded" in out, True)
    check("bootstrap hints recall/finish",
          "ag recall" in out and "ag finish" in out, True)

    # -- recall: grep-style shared-memory search ----------------------------
    code, out = run(ag.cmd_recall, ["coffee"])
    check("recall exit on hit", code, 0)
    check("recall hit line",
          "identity/profile.md:3: Likes coffee and espresso." in out, True)
    check("recall finds both coffee lines", out.count(".md:"), 2)

    code, out = run(ag.cmd_recall, ["coffee", "espresso"])  # AND: one line has both
    check("recall AND exit", code, 0)
    check("recall AND narrows", out.count(".md:"), 1)

    code, out = run(ag.cmd_recall, ["coffee", "tea"])  # no line has both
    check("recall AND-miss exit", code, 1)
    check("recall AND-miss message", "no matches for: coffee tea" in out, True)

    code, out = run(ag.cmd_recall, ["coffee", "tea", "--all"])  # OR: 2 + 1
    check("recall OR exit", code, 0)
    check("recall OR widens", out.count(".md:"), 3)

    code, out = run(ag.cmd_recall, ["coffee", "--limit", "1"])
    check("recall limit caps output", out.count(".md:"), 1)
    check("recall limit exit", code, 0)

    code, _ = run(ag.cmd_recall, [])
    check("recall without keyword exit", code, 2)
    code, _ = run(ag.cmd_recall, ["coffee", "--limit", "many"])
    check("recall bad limit exit", code, 2)

    code, out = run(ag.cmd_recall, ["kerfluffle"])  # messages/archive is searched
    check("recall searches messages/archive", code, 0)
    check("recall archive hit",
          "messages/archive/from-cara-to-alice-old.md:1: an archived kerfluffle"
          in out, True)

    # -- finish: session close-out -------------------------------------------
    day = datetime.now().strftime("%Y-%m-%d")
    daily = ag.CENTRAL / "log/daily" / f"{day}-alice.md"
    code, out = run(ag.cmd_finish, ["alice"], stdin="wrapped the report")
    check("finish exit", code, 0)
    body = daily.read_text(encoding="utf-8")
    check("finish writes session summary",
          "## Session summary" in body and "wrapped the report" in body, True)
    reg = json.loads((ag.CENTRAL / "registry.json").read_text(encoding="utf-8"))
    check("finish refreshes last_seen",
          bool(reg["agents"]["alice"].get("last_seen")), True)
    trail = (ag.CENTRAL / "log/audit.jsonl").read_text(encoding="utf-8")
    check("finish audited", '"action": "finish"' in trail, True)

    code, _ = run(ag.cmd_finish, ["alice"], stdin="   ")  # blank stdin
    check("finish empty stdin exit", code, 2)

    code, out = run(ag.cmd_finish, ["ghost"], stdin="ghost session")
    check("finish unregistered exit", code, 0)
    check("finish unregistered notes it",
          "agent 'ghost' not registered" in out, True)
    check("finish unregistered still logs",
          (ag.CENTRAL / "log/daily" / f"{day}-ghost.md").is_file(), True)

    # inbox: report-only by default, archived only when asked (SPEC 3.6)
    msg = ag.CENTRAL / "messages/inbox/from-bob-to-alice-report.md"
    msg.write_text("please review", encoding="utf-8")
    code, out = run(ag.cmd_finish, ["alice"], stdin="second pass")
    check("finish reports pending inbox",
          "1 inbox message(s) still pending" in out, True)
    check("finish keeps inbox file untouched", msg.is_file(), True)

    code, out = run(ag.cmd_finish, ["alice", "--archive-inbox"],
                    stdin="third pass")
    check("finish archive exit", code, 0)
    check("finish archives inbox message",
          (ag.CENTRAL / "messages/archive/from-bob-to-alice-report.md").is_file(),
          True)
    check("finish empties inbox", msg.exists(), False)
    check("finish archive reported",
          "archived 1 inbox message(s) -> messages/archive/" in out, True)

    # Real sends create persistent lock sidecars. They are not messages and
    # must not move with an archive, or a concurrent sender can lose its lock.
    code, _ = run(ag.cmd_send, ["alice", "repeat"], stdin="first message")
    check("send exit", code, 0)
    sent = ag._inbox_messages("alice")
    check("inbox excludes send lock sidecars", len(sent), 1)
    sent_path = sent[0]
    sidecar = sent_path.with_name(f".{sent_path.name}.ag-lock")
    code, out = run(ag.cmd_bootstrap, ["alice"])
    check("bootstrap hides message filenames", sent_path.name in out, False)
    code, inbox_output = run(ag.cmd_inbox, ["alice"])
    check("explicit inbox lists message", sent_path.name in inbox_output, True)
    check("explicit inbox hides lock sidecars", ".ag-lock" in inbox_output, False)
    code, out = run(ag.cmd_finish, ["alice", "--archive-inbox"], stdin="first batch")
    check("finish counts actual messages only",
          "archived 1 inbox message(s)" in out, True)
    check("finish leaves inbox lock in place", sidecar.is_file(), True)
    archive = ag.CENTRAL / "messages/archive"
    first_archive = archive / sent_path.name
    check("first archived body", first_archive.read_text(encoding="utf-8"),
          "first message\n")
    code, _ = run(ag.cmd_send, ["alice", "repeat"], stdin="second message")
    code, _ = run(ag.cmd_finish, ["alice", "--archive-inbox"], stdin="second batch")
    check("repeat topic preserves first archive",
          first_archive.read_text(encoding="utf-8"), "first message\n")
    check("repeat topic gets a separate archive",
          (archive / f"{sent_path.stem}-1.md").read_text(encoding="utf-8"),
          "second message\n")
    code, out = run(ag.cmd_finish, ["alice"], stdin="all processed")
    check("only lock sidecars do not count as pending inbox",
          "inbox message(s) still pending" in out, False)

    # cmd_log must still land in the same daily file after the refactor
    code, _ = run(ag.cmd_log, ["alice", "did things"], stdin="details here")
    check("log exit", code, 0)
    check("log lands in same daily file",
          "## did things" in daily.read_text(encoding="utf-8"), True)

    # cmd_last_seen must behave the same after the _touch_last_seen refactor
    code, _ = run(ag.cmd_last_seen, ["alice"])
    check("last-seen exit", code, 0)
    code, _ = run(ag.cmd_last_seen, ["nobody"])
    check("last-seen unknown agent exit", code, 1)

    # -- auto-upgrade: config parsing + rate-limit state (offline) ----------
    up = ag.CENTRAL / "UPGRADE.md"
    up.write_text("mode = apply\ninterval_hours = 12\n", encoding="utf-8")
    cfg = ag.load_upgrade_config()
    check("upgrade config parsed",
          (cfg["mode"], cfg["interval_hours"]), ("apply", 12))
    up.write_text("mode = nonsense\n", encoding="utf-8")
    cfg = ag.load_upgrade_config()
    check("upgrade bad mode falls back", cfg["mode"], "check")
    up.unlink()
    cfg = ag.load_upgrade_config()
    check("upgrade defaults",
          (cfg["mode"], cfg["interval_hours"]), ("check", 24))

    up.write_text("mode = off\n", encoding="utf-8")
    code, out = run(ag.cmd_bootstrap, ["alice"])  # off: no network, no crash
    check("bootstrap with upgrade off", code, 0)
    check("upgrade off stays silent", "update available" not in out, True)

    check("upgrade due without state", ag._upgrade_due({"interval_hours": 24}), True)
    state = ag._upgrade_state()
    state.write_text(json.dumps({"last_check": ag.now_iso()}), encoding="utf-8")
    check("upgrade not due after stamp",
          ag._upgrade_due({"interval_hours": 24}), False)

    print()
    shutil.rmtree(TMP, ignore_errors=True)
    if FAILED:
        print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
        return 1
    print("all session-contract checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
