"""回归守卫（P1-②）测试。

覆盖：
  T-GD-01 快照只含白名单文件（SKILL.md/references/scripts，排除运行时产物）
  T-GD-02 快照后可回滚（改文件 → 回滚 → 字节还原）
  T-GD-03 CHANGELOG 追加含原因/预期/测试
  T-GD-04 check：采纳率上升 → 返回 0
  T-GD-05 check：采纳率下降超阈值 → 返回 2 + 告警
  T-GD-06 check：数据不足 → 返回 0（不误报）
"""
import json
import os
import shutil
import sys
import tempfile
import unittest.mock as mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import apply_guard as gd

PASSED = 0
FAILED = 0


def check(name, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  ✅ {name}")
    else:
        FAILED += 1
        print(f"  ❌ {name}  {detail}")


def make_skill(tmp):
    skill = os.path.join(tmp, "test-skill")
    os.makedirs(os.path.join(skill, "references"))
    os.makedirs(os.path.join(skill, "scripts"))
    os.makedirs(os.path.join(skill, ".git"))
    for name, content in [("SKILL.md", "---\nversion: 1.0.0\n---\n# T\n"),
                          ("references/signals.md", "# spec\n"),
                          ("scripts/tool.py", "print('hi')\n")]:
        p = os.path.join(skill, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
    with open(os.path.join(skill, ".git", "config"), "w", encoding="utf-8") as f:
        f.write("[core]\n")
    with open(os.path.join(skill, "signals-log.jsonl"), "w", encoding="utf-8") as f:
        f.write("")
    return skill


def _sig(ts, accepted):
    return {"ts": ts, "event": "accept", "accepted": accepted, "weight": 3}


def _write_signals(skill, rows):
    with open(os.path.join(skill, "signals-log.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_gd_01_snapshot_scope():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        sid = gd.cmd_snapshot(skill, label="test")
        snap_dir = os.path.join(skill, gd.SNAP_ROOT, sid)
        names = []
        for root, _, files in os.walk(snap_dir):
            for fn in files:
                if fn == "_meta.json":
                    continue
                names.append(os.path.relpath(os.path.join(root, fn), snap_dir).replace("\\", "/"))
        check("T-GD-01 快照只含白名单文件",
              set(names) == {"SKILL.md", "references/signals.md", "scripts/tool.py"}, f"names={names}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_gd_02_rollback_restores():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        orig = open(os.path.join(skill, "SKILL.md"), encoding="utf-8").read()
        sid = gd.cmd_snapshot(skill)
        with open(os.path.join(skill, "SKILL.md"), "a", encoding="utf-8") as f:
            f.write("# broken edit\n")
        gd.cmd_rollback(skill, sid)
        after = open(os.path.join(skill, "SKILL.md"), encoding="utf-8").read()
        check("T-GD-02 回滚后字节还原", after == orig, f"{orig!r} != {after!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_gd_03_changelog():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        gd.cmd_changelog(skill, "snap-1", "修检索", "负反馈下降", "模拟测试通过")
        content = open(os.path.join(skill, gd.CHANGELOG_NAME), encoding="utf-8").read()
        check("T-GD-03 CHANGELOG 含原因/预期/测试/快照", "修检索" in content and "负反馈下降" in content
              and "模拟测试通过" in content and "snap-1" in content, content)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_gd_04_05_06_check():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        d = lambda days: (now - timedelta(days=days)).isoformat()  # noqa: E731
        # 上升：前 14 天采纳率低，近 14 天高
        _write_signals(skill, [])
        for i in range(10):
            for acc in (0, 0, 1, 1):  # 前段 50%
                pass
        rows = [{"ts": d(20), "accepted": 0}, {"ts": d(20), "accepted": 0},
                {"ts": d(10), "accepted": 1}, {"ts": d(10), "accepted": 1}]
        _write_signals(skill, [_sig(r["ts"], r["accepted"]) for r in rows])
        rc = gd.cmd_check(skill, days=14)
        check("T-GD-04 采纳率上升 → 返回 0", rc == 0, f"rc={rc}")
        # 下降：近 14 天低
        rows2 = [{"ts": d(20), "accepted": 1}, {"ts": d(20), "accepted": 1},
                 {"ts": d(10), "accepted": 0}, {"ts": d(10), "accepted": 0}]
        _write_signals(skill, [_sig(r["ts"], r["accepted"]) for r in rows2])
        rc2 = gd.cmd_check(skill, days=14)
        check("T-GD-05 采纳率下降超阈值 → 返回 2", rc2 == 2, f"rc={rc2}")
        # 数据不足
        _write_signals(skill, [_sig(d(10), None)])
        rc3 = gd.cmd_check(skill, days=14)
        check("T-GD-06 数据不足 → 返回 0（不误报）", rc3 == 0, f"rc={rc3}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    print("== P1-② 回归守卫测试 ==")
    test_gd_01_snapshot_scope()
    test_gd_02_rollback_restores()
    test_gd_03_changelog()
    test_gd_04_05_06_check()
    print(f"\nSUMMARY: {PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
