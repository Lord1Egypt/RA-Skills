#!/usr/bin/env python3
"""Regression: Windows directory junctions must count as links.

`Path.is_symlink()` returns False for a junction (IO_REPARSE_TAG_MOUNT_POINT),
while `make_link` creates junctions on Windows as the no-privilege fallback.
If a junction is mistaken for a real directory, `adopt` and `link-root` would
treat the guild's own files as unadopted skills and try to move them into the
guild — a self-move.

The Windows branch cannot run on POSIX, so `os.name` and `os.lstat` are
faked to prove the code path. Run: python3 scripts/test_junction.py
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ag  # noqa: E402

FAILED = []


def check(label, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {label}: got={got!r} want={want!r}")
    if not ok:
        FAILED.append(label)


class _FakeStat:
    def __init__(self, tag):
        if tag is not None:
            self.st_reparse_tag = tag


def fake_windows(tag_by_path):
    """Pretend we are on Windows; report reparse tags from a dict."""
    real_name, real_lstat = ag.os.name, ag.os.lstat

    def lstat(p, *a, **k):
        tag = tag_by_path.get(str(p), None)
        if tag is None:
            return real_lstat(p, *a, **k)
        return _FakeStat(tag)

    ag.os.name = "nt"
    ag.os.lstat = lstat
    return real_name, real_lstat


def restore(saved):
    ag.os.name, ag.os.lstat = saved


def main():
    tmp = Path(tempfile.mkdtemp(prefix="ag-junction-"))
    real_dir = tmp / "real_dir"
    real_dir.mkdir()
    (real_dir / "SKILL.md").write_text("x", encoding="utf-8")
    sym = tmp / "sym"
    sym.symlink_to(real_dir, target_is_directory=True)

    # POSIX baseline: symlink is a link, plain dir is not.
    check("posix symlink", ag.is_link(sym), True)
    check("posix real dir", ag.is_link(real_dir), False)
    check("posix missing path", ag.is_link(tmp / "nope"), False)

    # Windows: a junction reports IO_REPARSE_TAG_MOUNT_POINT and
    # is_symlink() is False, yet it MUST be treated as a link.
    saved = fake_windows({str(real_dir): ag._TAG_MOUNT_POINT})
    try:
        check("windows junction (the reported bug)", ag.is_link(real_dir), True)
    finally:
        restore(saved)

    # Windows: a reparse point that is not a link (e.g. dedup/placeholder
    # tags such as OneDrive) must NOT be treated as a link.
    saved = fake_windows({str(real_dir): 0x80000013})
    try:
        check("windows unrelated reparse tag", ag.is_link(real_dir), False)
    finally:
        restore(saved)

    # Windows: plain directory with no reparse tag attribute at all.
    saved = fake_windows({str(real_dir): "no-attr"})
    try:
        ag.os.lstat = lambda p, *a, **k: _FakeStat(None)
        check("windows plain dir (no tag attr)", ag.is_link(real_dir), False)
    finally:
        restore(saved)

    # A junctioned skills dir must be skipped by the adopt scanner instead of
    # being reported as an adoptable skill.
    skills = tmp / "skills"
    skills.mkdir()
    junctioned = skills / "guild-skill"
    junctioned.mkdir()
    (junctioned / "SKILL.md").write_text("x", encoding="utf-8")
    found_before = [i["src"].name for i in ag._scan_dir(skills, "skills")]
    check("adopt sees it as adoptable while undetected",
          found_before, ["guild-skill"])
    saved = fake_windows({str(junctioned): ag._TAG_MOUNT_POINT})
    try:
        found_after = [i["src"].name for i in ag._scan_dir(skills, "skills")]
        check("adopt skips a junctioned skill (no self-move)", found_after, [])
    finally:
        restore(saved)

    # to_trash must unlink a link instead of handing it to a trash helper
    # that could follow it and take the target's contents.
    victim = tmp / "link_to_real"
    victim.symlink_to(real_dir, target_is_directory=True)
    check("to_trash drops the link", ag.to_trash(victim), True)
    check("link is gone", victim.exists() or victim.is_symlink(), False)
    check("target survived", (real_dir / "SKILL.md").is_file(), True)

    print()
    if FAILED:
        print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
        return 1
    print("all junction regression checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
