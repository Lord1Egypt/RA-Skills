"""capture_skill_edits 单元测试（F6 · 被动捕获，零网络）。

覆盖测试方案 T-CAP：
  T-CAP-01 READ-only 生死线：捕获前后技能内容文件字节不变（发布阻断项）
  T-CAP-02 首跑仅建基线，不产信号
  T-CAP-03 手改 SKILL.md → 二跑产生 edit_capture（不自动 apply）
  T-CAP-04 note 仅相对路径，无绝对路径/用户名（零 PII）
  T-CAP-05 范围白名单：.git 内文件不跟踪
  T-CAP-06 改后还原 → 无净变化 → 不产信号
  T-CAP-09 baseline 损坏 → 走首跑逻辑（只建基线不崩）
  T-CAP-11 云端 .cloud_optin 状态不影响本地捕获
"""
import json
import os
import shutil
import sys
import tempfile
import unittest.mock as mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import capture_skill_edits as cap

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


def _sha256_hex(path):
    return cap._sha16(path)


def make_skill(tmp):
    """造一个最小信号技能目录：SKILL.md + references/signals.md + scripts/x.py + .git/ignored.py + 运行时产物。"""
    skill = os.path.join(tmp, "test-skill")
    os.makedirs(os.path.join(skill, "references"))
    os.makedirs(os.path.join(skill, "scripts"))
    os.makedirs(os.path.join(skill, ".git"))
    with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("---\nslug: test-skill\nversion: 1.0.0\n---\n# Test\n")
    with open(os.path.join(skill, "references", "signals.md"), "w", encoding="utf-8") as f:
        f.write("# signals spec\n")
    with open(os.path.join(skill, "scripts", "tool.py"), "w", encoding="utf-8") as f:
        f.write("print('hi')\n")
    # .git 内文件：不应被跟踪
    with open(os.path.join(skill, ".git", "config"), "w", encoding="utf-8") as f:
        f.write("[core]\n")
    # 运行时产物：不应被跟踪
    with open(os.path.join(skill, "signals-log.jsonl"), "w", encoding="utf-8") as f:
        f.write("")
    with open(os.path.join(skill, ".cloud_optin"), "w", encoding="utf-8") as f:
        f.write("off")
    with open(os.path.join(skill, ".anon_id"), "w", encoding="utf-8") as f:
        f.write("anon-test-1")
    return skill


def _signals(skill):
    p = os.path.join(skill, "signals-log.jsonl")
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def test_cap_01_readonly():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        content_files = ["SKILL.md", "references/signals.md", "scripts/tool.py"]
        before = {f: _sha256_hex(os.path.join(skill, f)) for f in content_files}
        cap.run_for_skill(skill)  # 首跑（只建基线）
        after1 = {f: _sha256_hex(os.path.join(skill, f)) for f in content_files}
        check("T-CAP-01 首跑后技能内容字节不变（READ-only）", before == after1, f"{before} vs {after1}")
        # 用户手动改 SKILL.md
        with open(os.path.join(skill, "SKILL.md"), "a", encoding="utf-8") as f:
            f.write("# edited\n")
        h_edited = _sha256_hex(os.path.join(skill, "SKILL.md"))
        cap.run_for_skill(skill)  # 二跑（产生 edit_capture 信号）
        after2 = {f: _sha256_hex(os.path.join(skill, f)) for f in content_files}
        check("T-CAP-01 产生信号后技能内容字节不变（生死线）",
              after2["SKILL.md"] == h_edited and after2["references/signals.md"] == before["references/signals.md"],
              f"h_edited={h_edited} after2={after2['SKILL.md']}")
        check("T-CAP-01 二跑确实产生了信号", len(_signals(skill)) == 1, f"count={len(_signals(skill))}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_02_first_run_baseline_only():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        ok, stats = cap.run_for_skill(skill)
        check("T-CAP-02 首跑 first_run=True", ok and stats["first_run"])
        check("T-CAP-02 首跑不产信号", len(_signals(skill)) == 0)
        check("T-CAP-02 baseline 已建", os.path.exists(os.path.join(skill, ".skill_edit_baseline.json")))
        b = cap._read_json(os.path.join(skill, ".skill_edit_baseline.json"))
        content_keys = set(b.keys()) - {"_date"}
        check("T-CAP-02 baseline 只含白名单相对路径（+_date）",
              content_keys == {"SKILL.md", "references/signals.md", "scripts/tool.py"}, f"keys={sorted(b.keys())}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_03_manual_edit_captured():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        cap.run_for_skill(skill)  # 首跑建基线
        with open(os.path.join(skill, "SKILL.md"), "a", encoding="utf-8") as f:
            f.write("# user edit\n")
        ok, stats = cap.run_for_skill(skill)  # 二跑
        check("T-CAP-03 手改 SKILL.md 被捕获", ok and stats["modified"] == 1, f"stats={stats}")
        sigs = _signals(skill)
        check("T-CAP-03 产生 1 条 edit_capture", len(sigs) == 1 and sigs[0]["event"] == "edit_capture", f"sigs={sigs}")
        check("T-CAP-03 不自动 apply（技能内容保持用户改动）",
              "user edit" in open(os.path.join(skill, "SKILL.md"), encoding="utf-8").read())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_04_relative_path_no_pii():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        cap.run_for_skill(skill)
        with open(os.path.join(skill, "references", "signals.md"), "a", encoding="utf-8") as f:
            f.write("# more\n")
        cap.run_for_skill(skill)
        sigs = _signals(skill)
        note = sigs[0]["note"] if sigs else ""
        check("T-CAP-04 note 为 kind:相对路径", note == "modify:references/signals.md", f"note={note!r}")
        check("T-CAP-04 无绝对路径/用户名", tmp not in note and "zyd" not in note and "Users" not in note,
              f"note={note!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_05_scope_whitelist():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        tracked = cap._tracked_files(skill)
        check("T-CAP-05 .git 内文件不跟踪", not any(".git" in t for t in tracked), f"tracked={tracked}")
        check("T-CAP-05 运行时产物不跟踪", not any(t in ("signals-log.jsonl", ".cloud_optin") for t in tracked),
              f"tracked={tracked}")
        check("T-CAP-05 只含 SKILL.md/references/scripts", set(tracked) == {"SKILL.md", "references/signals.md", "scripts/tool.py"},
              f"tracked={tracked}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_06_revert_no_signal():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        cap.run_for_skill(skill)
        p = os.path.join(skill, "SKILL.md")
        orig = open(p, encoding="utf-8").read()
        with open(p, "a", encoding="utf-8") as f:
            f.write("# tmp\n")
        cap.run_for_skill(skill)  # 改
        with open(p, "w", encoding="utf-8") as f:
            f.write(orig)  # 还原
        cap.run_for_skill(skill)  # 还原
        sigs = _signals(skill)
        check("T-CAP-06 改后还原 → 仅 1 条 modify（还原无净变化不重复计）", len(sigs) == 1, f"count={len(sigs)}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_09_baseline_corrupt():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        cap.run_for_skill(skill)
        with open(os.path.join(skill, ".skill_edit_baseline.json"), "w", encoding="utf-8") as f:
            f.write("{corrupt!!")
        ok, stats = cap.run_for_skill(skill)
        check("T-CAP-09 baseline 损坏 → 走首跑逻辑不崩", ok and stats["first_run"])
        check("T-CAP-09 重建基线且不产信号", len(_signals(skill)) == 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cap_11_cloud_optin_irrelevant():
    tmp = tempfile.mkdtemp()
    try:
        skill = make_skill(tmp)
        cap.run_for_skill(skill)
        with open(os.path.join(skill, "SKILL.md"), "a", encoding="utf-8") as f:
            f.write("# x\n")
        # .cloud_optin=off 时捕获照常本地记录（云端上传与否由 upload_signals 管）
        with open(os.path.join(skill, ".cloud_optin"), "w", encoding="utf-8") as f:
            f.write("off")
        cap.run_for_skill(skill)
        check("T-CAP-11 .cloud_optin=off 本地仍记 edit_capture", len(_signals(skill)) == 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    print("== capture_skill_edits 单元测试（F6，零网络）==")
    test_cap_01_readonly()
    test_cap_02_first_run_baseline_only()
    test_cap_03_manual_edit_captured()
    test_cap_04_relative_path_no_pii()
    test_cap_05_scope_whitelist()
    test_cap_06_revert_no_signal()
    test_cap_09_baseline_corrupt()
    test_cap_11_cloud_optin_irrelevant()
    print(f"\nSUMMARY: {PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
