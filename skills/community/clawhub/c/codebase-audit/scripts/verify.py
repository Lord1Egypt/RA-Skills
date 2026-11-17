#!/usr/bin/env python3
"""Verify an audit's output against the lens files, so "done" is checked, not claimed.

Usage:
  verify.py [out=.audit] [--root .] [--lens a,b]

Checks, per findings file (findings/<lens>[-<shard>].md):
  - every finding block has every field of the finding format, with allowed values;
  - its probe exists in the lens, and its `where` path exists in the repo (and the line, when given);
  - every probe of the lens ends in a finding or a `clean:` line (shards of one lens are pooled);
  - conditional probes may close as `clean: <probe> — n/a: <why the condition does not hold>`.
And across the audit: every lens SCAN.md says fires has a findings file, and REPORT.md (when present)
places every surviving finding id. Exit 1 on any problem.
"""
import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan import load_lenses, read_text  # noqa: E402  the lens files are the single source of probes

FIELDS = ("where", "probe", "scenario", "severity", "detectability", "verdict", "fix family")
SEVERITY = {"critical", "high", "medium", "low"}
DETECTABILITY = {"loud", "quiet", "silent"}
HEADING = re.compile(r"^### ([A-Z]+-\d+) (.+)$", re.MULTILINE)
FIELD = re.compile(r"^- ([a-z ]+): (.+)$", re.MULTILINE)
CLEAN = re.compile(r"^clean: ([a-z0-9-]+) [—-]+ (.+)$", re.MULTILINE)
FIRES = re.compile(r"^- \*\*([a-z]+)\*\* fires", re.MULTILINE)


def parse(text):
    """(findings, clean lines) from one findings file. A finding is a heading plus its field lines."""
    findings = []
    starts = [m.start() for m in HEADING.finditer(text)] + [len(text)]
    for start, end in zip(starts, starts[1:]):
        block = text[start:end]
        head = HEADING.match(block)
        findings.append(dict(id=head.group(1), claim=head.group(2),
                             **{k: v.strip() for k, v in FIELD.findall(block)}))
    return findings, dict(CLEAN.findall(text))


def check_finding(f, lens, root):
    problems = [f"missing field '{k}'" for k in FIELDS if k not in f]
    if f.get("severity", "").split()[0:1] and f["severity"].split()[0] not in SEVERITY:
        problems.append(f"severity '{f['severity']}' is not one of {sorted(SEVERITY)}")
    if f.get("detectability", "").split()[0:1] and f["detectability"].split()[0] not in DETECTABILITY:
        problems.append(f"detectability '{f['detectability']}' is not one of {sorted(DETECTABILITY)}")
    verdict = f.get("verdict", "")
    if verdict and not re.match(r"(CONFIRMED|PLAUSIBLE)\b", verdict):
        problems.append(f"verdict '{verdict}' is not CONFIRMED or PLAUSIBLE")
    if verdict.startswith("CONFIRMED") and "(" not in verdict:
        problems.append("CONFIRMED verdict names no reproduction")
    if "probe" in f and f["probe"] not in lens.probes:
        problems.append(f"probe '{f['probe']}' is not in lenses/{lens.name}.md")
    if "where" in f:
        problems += check_where(f["where"], root)
    return problems


def check_where(where, root):
    m = re.match(r"`?([^`:\s]+)(?::(\d+))?", where)
    if not m:
        return [f"where '{where}' is not path:line"]
    path, line = m.group(1), m.group(2)
    full = os.path.join(root, path)
    if not os.path.isfile(full):
        return [f"where path '{path}' does not exist"]
    if line and int(line) > len(read_text(full).splitlines()):
        return [f"where line {line} is past the end of {path}"]
    return []


def verify(out, root, only):
    lenses = load_lenses()
    problems, ids, counts = [], [], collections.Counter()
    covered = collections.defaultdict(set)
    files = sorted(os.listdir(os.path.join(out, "findings"))) if os.path.isdir(os.path.join(out, "findings")) else []
    seen_lenses = set()
    for name in files:
        if not name.endswith(".md"):
            continue
        lens_name = name[:-3].split("-")[0]
        if only and lens_name not in only:
            continue
        lens = lenses.get(lens_name)
        if not lens:
            problems.append(f"findings/{name}: no lens named '{lens_name}'")
            continue
        seen_lenses.add(lens_name)
        findings, clean = parse(read_text(os.path.join(out, "findings", name)))
        for f in findings:
            problems += [f"findings/{name} {f['id']}: {p}" for p in check_finding(f, lens, root)]
            covered[lens_name].add(f.get("probe"))
            ids.append(f["id"])
            counts[f.get("severity", "?").split()[0]] += 1
        for probe, evidence in clean.items():
            if probe not in lens.probes:
                problems.append(f"findings/{name}: clean line names unknown probe '{probe}'")
            elif evidence.lower().startswith("n/a") and probe not in lens.conditional:
                problems.append(f"findings/{name}: '{probe}' is unconditional, so n/a cannot close it")
            covered[lens_name].add(probe)
    for lens_name in seen_lenses:
        missing = [p for p in lenses[lens_name].probes if p not in covered[lens_name]]
        problems += [f"lens {lens_name}: probe '{p}' has no finding and no clean line" for p in missing]

    scan_md = os.path.join(out, "SCAN.md")
    if os.path.isfile(scan_md):
        fired = set(FIRES.findall(read_text(scan_md)))
        problems += [f"lens {l} fires in SCAN.md but has no findings file" for l in sorted(fired - seen_lenses)
                     if not only or l in only]
    report_md = os.path.join(out, "REPORT.md")
    if os.path.isfile(report_md) and not only:
        report = read_text(report_md)
        problems += [f"REPORT.md does not place {i}" for i in ids if i not in report]
    duplicates = [i for i, n in collections.Counter(ids).items() if n > 1]
    problems += [f"finding id {i} appears more than once; merge with an `also:` line" for i in duplicates]
    return problems, ids, counts, seen_lenses


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", nargs="?", default=".audit")
    ap.add_argument("--root", default=".", help="the audited repo, for checking `where` paths")
    ap.add_argument("--lens", help="verify only these lenses (a hunter checking its own file)")
    a = ap.parse_args()
    only = set(a.lens.split(",")) if a.lens else None
    problems, ids, counts, lenses = verify(a.out, os.path.abspath(a.root), only)
    if problems:
        print("\n".join(problems))
        print(f"\nnot verified: {len(problems)} problems")
        return 1
    by_sev = ", ".join(f"{counts[s]} {s}" for s in ("critical", "high", "medium", "low") if counts[s])
    print(f"verified: {len(ids)} findings ({by_sev or 'none'}) across {len(lenses)} lenses, every probe answered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
