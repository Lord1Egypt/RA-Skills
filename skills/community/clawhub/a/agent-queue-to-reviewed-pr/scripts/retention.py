#!/usr/bin/env python3
"""Execute the retention this skill declares. A declared retention nobody runs is not a retention.

It NEVER performs a network call: you fetch the PR states, it consumes them.

    gh pr list --repo <owner/repo> --label agent --state all --json number,state > pr-states.json
    python3 scripts/retention.py pr-states.json           # dry run: prints the plan, changes NOTHING
    python3 scripts/retention.py pr-states.json --apply   # executes that same plan
    python3 scripts/retention.py pr-states.json --apply --root=/path/to/repo   # cron-safe

Run it from the loop's repo root, or pass --root. It REFUSES a root holding neither memory/
nor work/qa-runs rather than print "APPLYING", purge nothing and exit 0 like a healthy run.
Every control it skips -- unreadable index, unresolvable key, a PR-<n> that is a symlink --
is announced as WARN on stderr. Judge the exit code and the WARNs, never the silence.

Two rules, both declared in SKILL.md and enforced here:
  1. Index entries (qa/remediation/pr) whose PR is no longer OPEN are dropped. An entry is
     expirable only if a PR number can be resolved from its key (`42@<sha>`, `PR-42`) or from
     its `number` field -- pr-index is keyed by ticket id, so its entries MUST carry `number`.
     A key that resolves to nothing is kept AND reported as WARN: a retention that cannot
     resolve an entry says so. Silence would read as "purged".
  2. work/qa-runs/PR-<n> is deleted once its PR is no longer OPEN, and in ALL cases
     after MAX_AGE_DAYS -- screenshots carry authenticated-session data.

The daily journal memory/YYYY-MM-DD.md is deliberately out of scope: it is the audit trail
(ids and PR URLs only, never personal data). Nothing else on disk is touched.

Deletion is confined by construction: only directories named exactly PR-<digits>, sitting
directly under <root>/work/qa-runs, that are real directories and not symlinks. Nothing else
is ever removed, and the qa-runs root itself never is.

Exit codes:
    0  plan printed (dry run), or applied
    1  bad input -- nothing was changed
"""
import json
import os
import re
import shutil
import sys
import time

MAX_AGE_DAYS = 7
QA_RUNS = os.path.join("work", "qa-runs")
INDEXES = ("memory/qa-index.json", "memory/remediation-index.json", "memory/pr-index.json")
PR_DIR_RE = re.compile(r"^PR-(\d+)$")


def die(msg):
    print("retention: %s -- NOTHING was changed." % msg, file=sys.stderr)
    raise SystemExit(1)


def warn(msg):
    """Every skipped control says so, on the one channel SKILL.md tells you to grep."""
    print("  retention: WARN %s" % msg, file=sys.stderr)


def check_root(root):
    """Refuse an unrecognizable root. Without this, a cron with the wrong WorkingDirectory
    finds no index and no qa-runs, purges nothing, prints APPLYING and exits 0 -- byte-identical
    to a healthy run. Retention would be declared and not enforced, which is the exact failure
    this script exists to prevent."""
    if not os.path.isdir(os.path.join(root, "memory")) and \
       not os.path.isdir(os.path.join(root, QA_RUNS)):
        die("neither memory/ nor %s exists under %s -- run from the loop's repo root, or pass "
            "--root=<path>. Refusing to report a purge that did not happen" % (QA_RUNS, root))


def load_states(path):
    """{number: state} from `gh pr list --json number,state`."""
    try:
        with open(path, encoding="utf-8") as fh:
            rows = json.load(fh)
    except OSError as exc:
        die("cannot read PR states: %s" % exc)
    except json.JSONDecodeError as exc:
        die("PR states file is not valid JSON: %s. Produce it with: "
            "gh pr list --repo <owner/repo> --label agent --state all --json number,state" % exc)
    if not isinstance(rows, list):
        die("expected a JSON array from `gh pr list --json number,state`")
    states = {}
    for row in rows:
        if not isinstance(row, dict) or "number" not in row or "state" not in row:
            die("every row needs `number` and `state` -- re-run gh with --json number,state")
        states[str(row["number"])] = str(row["state"]).upper()
    return states


def resolve_number(key, entry):
    """PR number for an index entry, or None if it cannot be resolved.

    The entry's own `number` wins -- it is the only thing that works for an index keyed by
    ticket id (pr-index). Otherwise the key must be `<number>@<sha>` or `PR-<number>`.
    NOT `lstrip("PR-")`: that strips a CHARACTER SET, mangling 'P0-42' into '0-42'.
    """
    if isinstance(entry, dict) and entry.get("number") is not None:
        return str(entry["number"])
    head = str(key).split("@")[0]
    if head.isdigit():
        return head
    match = PR_DIR_RE.match(head)
    return match.group(1) if match else None


def purge_indexes(root, states, apply_it):
    """Drop entries whose PR is not OPEN. Unknown PRs are KEPT: absent from the listing is not
    proof of closure, and keeping is the safe error. An UNRESOLVABLE key is kept and WARNed."""
    for rel in INDEXES:
        path = os.path.join(root, rel)
        try:
            with open(path, encoding="utf-8") as fh:
                index = json.load(fh)
        except FileNotFoundError:
            continue  # a missing index is normal: that link may not run here
        except (OSError, json.JSONDecodeError) as exc:
            # An unreadable index is NOT normal. Skipping it silently reports a purge that did
            # not happen: the entries live forever and the operator has no way to know.
            warn("%s: unreadable (%s) -- NOT purged, fix the file and re-run" % (rel, exc))
            continue
        if not isinstance(index, dict):
            warn("%s: not a JSON object (%s) -- NOT purged, fix the file and re-run"
                 % (rel, type(index).__name__))
            continue
        kept = {}
        unresolved = []
        for key, entry in index.items():
            number = resolve_number(key, entry)
            if number is None:
                unresolved.append(str(key))
                kept[key] = entry
            elif states.get(number, "OPEN") == "OPEN":
                kept[key] = entry
        for key in unresolved:
            warn("%s: key %s carries no PR number, cannot expire -- add a \"number\" field to "
                 "this entry." % (rel, key))
        if len(kept) != len(index):
            print("  %s: %d -> %d entries" % (rel, len(index), len(kept)))
        if apply_it and len(kept) != len(index):
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(kept, fh, ensure_ascii=False, indent=2)
                fh.write("\n")


def expire_screenshots(root, states, apply_it):
    base = os.path.join(root, QA_RUNS)
    if not os.path.isdir(base):
        return
    cutoff = time.time() - MAX_AGE_DAYS * 86400
    for name in sorted(os.listdir(base)):
        match = PR_DIR_RE.match(name)
        if not match:
            continue  # never touch anything we did not create
        path = os.path.join(base, name)
        if os.path.islink(path) or not os.path.isdir(path):
            # Never follow a symlink out of qa-runs, and never rmtree a plain file. But say so:
            # this is screenshot data we claim to expire and are not expiring.
            warn("%s: not a real directory (symlink or file) -- left alone, NOT expired. Remove "
                 "it by hand if it holds session data." % os.path.join(QA_RUNS, name))
            continue
        state = states.get(match.group(1), "OPEN")
        try:
            aged = os.path.getmtime(path) < cutoff
        except OSError as exc:
            warn("%s: cannot stat (%s) -- NOT expired" % (os.path.join(QA_RUNS, name), exc))
            continue
        if state == "OPEN" and not aged:
            continue
        why = "PR %s" % state if state != "OPEN" else "older than %d days" % MAX_AGE_DAYS
        print("  %s: removing (%s)" % (os.path.join(QA_RUNS, name), why))
        if apply_it:
            shutil.rmtree(path)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = [a for a in argv[1:] if a.startswith("--")]
    roots = [a.split("=", 1)[1] for a in flags if a.startswith("--root=")]
    unknown = [a for a in flags if a != "--apply" and not a.startswith("--root=")]
    if len(args) != 1 or unknown or len(roots) > 1:
        die("usage: retention.py <pr-states.json> [--apply] [--root=<repo root>]")
    apply_it = "--apply" in flags
    root = roots[0] if roots else os.getcwd()
    if not os.path.isdir(root):
        die("--root=%s is not a directory" % root)
    check_root(root)
    states = load_states(args[0])

    print("retention: %s (%d PRs known)" % ("APPLYING" if apply_it else "DRY RUN", len(states)))
    purge_indexes(root, states, apply_it)
    expire_screenshots(root, states, apply_it)
    if not apply_it:
        print("retention: dry run -- nothing changed. Re-run with --apply to execute this plan.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
