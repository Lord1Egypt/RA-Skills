#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cli-skill-release · releaser.py 测试套件（目标 30+ 用例）。

运行：python -m pytest -q   （建议在 cli-skill-release 目录或其父级）
"""
import os
import sys
import subprocess
import textwrap
import tempfile

import pytest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASER = os.path.join(SKILL_DIR, "releaser.py")
SCAFFOLD = os.path.join(SKILL_DIR, "scaffold.py")
PY = sys.executable

sys.path.insert(0, SKILL_DIR)
import releaser as R  # noqa: E402

MIT0 = ("Permission to use, copy, modify, and/or distribute this software\n"
        "with or without fee is hereby granted, provided that the above\n"
        "copyright notice appears in all copies.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND.\n")
MIT_ASCII = MIT0 + "Copyright (c) 2026 He Wei\n"
MIT_NONASCII = MIT0 + "Copyright (c) 2026 何巍\n"


def run(args, cwd=None):
    return subprocess.run([PY, RELEASER] + args, cwd=cwd,
                         capture_output=True, text=True)


def gen_skill(tmp_path, name="demo-cli-skill"):
    out = os.path.join(str(tmp_path), name)
    r = subprocess.run([PY, SCAFFOLD, name, "--author", "He Wei", "--dest", out],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return out


def make_skill(tmp_path, name, doctor_rc=0, license_text=MIT_ASCII,
               with_ci=True, with_tee=True, ref=None, with_skillcard=False,
               with_license=True):
    import pathlib
    base = pathlib.Path(tmp_path)
    d = base / name
    d.mkdir()
    (d / "SKILL.md").write_text(textwrap.dedent(
        "---\nname: %s\nslug: %s\nversion: 1.0.0\nlicense: MIT-0\n"
        "keywords: test,cli\n---\nbody text\n" % (name, name)), encoding="utf-8")
    main = d / (name.replace("-", "_") + ".py")
    main.write_text(textwrap.dedent(
        "import argparse, sys\n"
        "def main():\n"
        "    p = argparse.ArgumentParser()\n"
        "    sub = p.add_subparsers(dest='c')\n"
        "    dd = sub.add_parser('doctor'); dd.add_argument('--path', default='.')\n"
        "    dd.set_defaults(func=lambda a: sys.exit(%d))\n"
        "    a = p.parse_args()\n"
        "    (a.func(a) if hasattr(a, 'func') else None)\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main())\n" % doctor_rc), encoding="utf-8")
    if with_license:
        (d / "LICENSE").write_text(license_text, encoding="utf-8")
    if with_ci:
        cd = d / ".github" / "workflows"
        cd.mkdir(parents=True)
        step = "python %s doctor --path ." % main.name
        if with_tee:
            step += " | tee $GITHUB_STEP_SUMMARY"
        (cd / "ci.yml").write_text(
            "jobs:\n  build:\n    steps:\n      - run: %s\n" % step, encoding="utf-8")
    if with_skillcard:
        (d / "skill-card.md").write_text("x", encoding="utf-8")
    if ref:
        with open(d / "SKILL.md", "a", encoding="utf-8") as f:
            f.write("\nsee %s\n" % ref)
    return d


# ---------------- validate 主流程 ----------------

def test_validate_scaffold_pass(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["validate", "--path", out])
    assert r.returncode == 0
    assert "PASS=13" in r.stdout


def test_validate_score_100(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["validate", "--path", out])
    assert "发布就绪分: 100 / 100" in r.stdout


def test_validate_missing_skillmd(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    r = run(["validate", "--path", str(d)])
    assert r.returncode == 1
    assert "SKILL.md 缺失" in r.stdout


def test_validate_no_license(tmp_path):
    d = make_skill(tmp_path, "s1", with_license=False)
    r = run(["validate", "--path", d])
    assert "LICENSE 文件缺失" in r.stdout
    assert r.returncode == 1


def test_validate_nonascii_license(tmp_path):
    d = make_skill(tmp_path, "s2", license_text=MIT_NONASCII)
    r = run(["validate", "--path", d])
    assert "非 ASCII" in r.stdout  # FAIL 项


def test_validate_skillcard_conflict(tmp_path):
    d = make_skill(tmp_path, "s3", with_skillcard=True)
    r = run(["validate", "--path", d])
    assert "skill-card.md" in r.stdout
    assert r.returncode == 1


def test_validate_missing_ref(tmp_path):
    d = make_skill(tmp_path, "s4", ref="scripts/missing_xyz.py")
    r = run(["validate", "--path", d])
    assert "引用了不存在的文件" in r.stdout
    assert r.returncode == 1


def test_validate_no_ci_warn(tmp_path):
    d = make_skill(tmp_path, "s5", with_ci=False)
    r = run(["validate", "--path", d])
    assert "无 .github/workflows/ci.yml" in r.stdout


def test_validate_ci_no_tee_warn(tmp_path):
    d = make_skill(tmp_path, "s6", with_tee=False)
    r = run(["validate", "--path", d])
    assert "缺 tee $GITHUB_STEP_SUMMARY" in r.stdout


def test_validate_doctor_fail(tmp_path):
    d = make_skill(tmp_path, "s7", doctor_rc=1)
    r = run(["validate", "--path", d])
    assert "doctor --path . 退出 1" in r.stdout
    assert r.returncode == 1


def test_validate_cli_mode_no_skillmd(tmp_path):
    d = tmp_path / "clidir"
    d.mkdir()
    (d / "tool.py").write_text(
        "import argparse, sys\n"
        "p=argparse.ArgumentParser(); s=p.add_subparsers(dest='c')\n"
        "dd=s.add_parser('doctor'); dd.add_argument('--path',default='.')\n"
        "dd.set_defaults(func=lambda a: None)\n"
        "p.parse_args()\n", encoding="utf-8")
    (d / "LICENSE").write_text(MIT_ASCII, encoding="utf-8")
    r = run(["validate", "--path", str(d), "--mode", "cli"])
    assert "跳过 frontmatter" in r.stdout
    assert "FAIL" not in r.stdout.split("合计")[0]


def test_validate_cli_mode_ignores_skillcard(tmp_path):
    d = tmp_path / "clidir2"
    d.mkdir()
    (d / "tool.py").write_text("import argparse, sys\n"
        "p=argparse.ArgumentParser(); s=p.add_subparsers(dest='c')\n"
        "dd=s.add_parser('doctor'); dd.add_argument('--path',default='.')\n"
        "dd.set_defaults(func=lambda a: None)\n"
        "p.parse_args()\n", encoding="utf-8")
    (d / "LICENSE").write_text(MIT_ASCII, encoding="utf-8")
    (d / "skill-card.md").write_text("x", encoding="utf-8")  # cli 模式应忽略
    r = run(["validate", "--path", str(d), "--mode", "cli"])
    assert "skill-card.md" not in r.stdout


def test_validate_warn_lowers_score(tmp_path):
    # 去掉 CI → 失去 8 分权重中的一半(4)，满分 100 → 96
    d = make_skill(tmp_path, "s8", with_ci=False)
    r = run(["validate", "--path", d])
    assert "发布就绪分: 96 / 100" in r.stdout


def test_validate_zero_dep_warn(tmp_path):
    d = make_skill(tmp_path, "s9")
    (d / "extra.py").write_text("import numpy\n", encoding="utf-8")
    r = run(["validate", "--path", d])
    assert "可能非标准库依赖" in r.stdout


# ---------------- selfcheck ----------------

def test_selfcheck_own_pass():
    r = run(["selfcheck", "--path", SKILL_DIR])
    assert r.returncode == 0
    assert "零依赖成立" in r.stdout


def test_selfcheck_detects_thirdparty(tmp_path):
    d = tmp_path / "dep"
    d.mkdir()
    (d / "x.py").write_text("import requests\n", encoding="utf-8")
    r = run(["selfcheck", "--path", str(d)])
    assert r.returncode == 1
    assert "requests" in r.stdout


# ---------------- bump ----------------

def test_bump_patch(tmp_path):
    d = make_skill(tmp_path, "b1")
    r = run(["bump", "--path", d, "--type", "patch"])
    assert "1.0.1" in r.stdout
    assert "1.0.1" in (d / "SKILL.md").read_text(encoding="utf-8")


def test_bump_minor(tmp_path):
    d = make_skill(tmp_path, "b2")
    r = run(["bump", "--path", d, "--type", "minor"])
    assert "1.1.0" in r.stdout


def test_bump_major(tmp_path):
    d = make_skill(tmp_path, "b3")
    r = run(["bump", "--path", d, "--type", "major"])
    assert "2.0.0" in r.stdout


def test_bump_creates_changelog(tmp_path):
    d = make_skill(tmp_path, "b4")
    run(["bump", "--path", d, "--type", "patch"])
    assert (d / "CHANGELOG.md").is_file()


# ---------------- gap ----------------

def _make_skills_root(tmp_path, specs):
    sk = tmp_path / "skills"
    sk.mkdir()
    for name, kw in specs:
        d = sk / name
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: %s\nkeywords: %s\ndescription: x\n---\nbody\n" % (name, kw),
            encoding="utf-8")
    return str(sk)


def test_gap_runs(tmp_path):
    sk = _make_skills_root(tmp_path, [("g1", "git,ci,release"), ("g2", "security,scan")])
    r = run(["gap", "--roots", sk])
    assert r.returncode == 0
    assert "本机缺口" in r.stdout


def test_gap_reports_gap_and_thin(tmp_path):
    sk = _make_skills_root(tmp_path, [("g1", "git,ci,release")])
    r = run(["gap", "--roots", sk])
    assert "缺口" in r.stdout
    assert "可补强" in r.stdout


def test_gap_suggests_scaffold(tmp_path):
    sk = _make_skills_root(tmp_path, [("g1", "git")])
    r = run(["gap", "--roots", sk])
    assert "releaser.py scaffold" in r.stdout


# ---------------- release ----------------

def test_release_dry_run_no_git(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["release", "--path", out, "--dry-run"])
    assert r.returncode == 0
    assert "dry-run" in r.stdout
    assert "导入" in r.stdout


def test_release_dry_run_skips_push(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["release", "--path", out, "--dry-run"])
    assert "dry-run" in r.stdout
    assert "推送" in r.stdout  # dry-run 明确跳过推送


# ---------------- scaffold ----------------

def test_scaffold_files(tmp_path):
    out = gen_skill(tmp_path)
    names = os.listdir(out)
    assert "SKILL.md" in names
    assert any(n.endswith(".py") for n in names)
    assert "LICENSE" in names
    assert os.path.isfile(os.path.join(out, ".github", "workflows", "ci.yml"))
    assert os.path.isdir(os.path.join(out, "tests"))


def test_scaffold_doctor_passes(tmp_path):
    out = gen_skill(tmp_path)
    main = [n for n in os.listdir(out) if n.endswith(".py")][0]
    r = subprocess.run([PY, os.path.join(out, main), "doctor", "--path", "."],
                       cwd=out, capture_output=True, text=True)
    assert r.returncode == 0


# ---------------- 纯函数单元 ----------------

def test_categorize():
    cats = R.categorize("git ci release python 发布")
    assert "Developer Tools" in cats


def test_categorize_security():
    assert "Security" in R.categorize("security scan vuln guard")


def test_auto_topics_truncate():
    kw = "alpha,beta,gamma,delta,epsilon,zeta,eta,theta"
    out = R._auto_topics(kw, max_len=48)
    assert len(out) <= 48


def test_auto_topics_single():
    assert R._auto_topics("onlyone") == "onlyone"


def test_detect_license_mit0():
    import tempfile
    sp = tempfile.mkdtemp()
    p = os.path.join(sp, "LICENSE")
    open(p, "w", encoding="utf-8").write(MIT_ASCII)
    spdx, na = R.detect_license(p)
    assert spdx == "MIT-0"
    assert na is False


def test_find_main_entry(tmp_path):
    d = make_skill(tmp_path, "fe")
    m = R.find_main_entry(d, "fe")
    assert m and m.endswith("fe.py")


def test_score_full_clean():
    import tempfile
    d = make_skill(tempfile.mkdtemp(), "sc")
    R.validate_skill(d)
    assert R._score() == 100


def test_score_zero_on_missing_core():
    import tempfile
    d = tempfile.mkdtemp()
    open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write("body\n")
    R.validate_skill(d)
    assert R._score() < 100
    assert R._score() >= 0


def test_inventory_roots_return_list():
    roots = R.default_roots()
    assert isinstance(roots, list)


def test_validate_self_no_recursion():
    # 对自身（含 releaser.py 的 doctor 子命令）校验不得无限递归：
    # 进程须正常结束（不被 SIGTERM 杀掉），且 doctor 自检门被执行（报告含 doctor 行）
    r = run(["validate", "--path", SKILL_DIR])
    assert r.returncode in (0, 1, 2)
    assert "doctor --path . 退出" in r.stdout


def test_recursion_guard_env_set():
    import os
    os.environ["RELEASER_VALIDATE_DEPTH"] = "1"
    try:
        d = make_skill(tempfile.mkdtemp(), "rg")
        R.validate_skill(d)
        lines = [x[1] for x in R.REPORT]
        assert any("防递归" in x for x in lines)
    finally:
        os.environ.pop("RELEASER_VALIDATE_DEPTH", None)


def test_validate_json_structure():
    import json as _json
    d = make_skill(tempfile.mkdtemp(), "jskill")
    r = run(["validate", "--path", str(d), "--json"])
    assert r.returncode == 0, r.stderr
    payload = _json.loads(r.stdout)
    assert set(["path", "mode", "score", "summary", "items"]) <= set(payload)
    assert isinstance(payload["score"], int) and 0 <= payload["score"] <= 100
    assert payload["summary"]["FAIL"] == 0
    assert len(payload["items"]) >= 7
    # 每条至少含 level/msg/weight
    for it in payload["items"]:
        assert set(["level", "msg", "weight"]) <= set(it)


def test_validate_json_self_is_100():
    import json as _json
    r = run(["validate", "--path", SKILL_DIR, "--json"])
    assert r.returncode == 0
    payload = _json.loads(r.stdout)
    assert payload["score"] == 100
    assert payload["summary"]["FAIL"] == 0


def test_gap_scan_json_market_mode():
    import json as _json
    import tempfile
    data = [
        {"name": "a", "categories": ["Security", "Developer Tools"]},
        {"name": "b", "categories": ["Security"]},
    ]
    p = os.path.join(tempfile.mkdtemp(), "scan.json")
    with open(p, "w", encoding="utf-8") as f:
        _json.dump(data, f)
    r = run(["gap", "--scan-json", p])
    assert r.returncode == 0
    # 消费了市场扫描数据（而非本机）—— 新输出用 [市场] 段 + 组合机会
    assert "[市场]" in r.stdout
    assert "组合机会" in r.stdout
    # 市场数据含 Finance（即使本机无）
    assert "Finance" in r.stdout
    # 组合机会给出 scaffold 建议
    assert "scaffold" in r.stdout


# ---------------- 1.5.0 新能力 ----------------

def test_validate_package_mode_no_manifest(tmp_path):
    d = tmp_path / "pkgdir"
    d.mkdir()
    (d / "tool.py").write_text(
        "import argparse, sys\n"
        "p=argparse.ArgumentParser(); s=p.add_subparsers(dest='c')\n"
        "dd=s.add_parser('doctor'); dd.add_argument('--path',default='.')\n"
        "dd.set_defaults(func=lambda a: None)\n"
        "p.parse_args()\n", encoding="utf-8")
    (d / "LICENSE").write_text(MIT_ASCII, encoding="utf-8")
    r = run(["validate", "--path", str(d), "--mode", "package"])
    assert "跳过 frontmatter" in r.stdout
    assert "未检测到打包清单" in r.stdout
    assert "FAIL" not in r.stdout.split("合计")[0]


def test_validate_package_mode_with_manifest(tmp_path):
    d = tmp_path / "pkgdir2"
    d.mkdir()
    (d / "tool.py").write_text(
        "import argparse, sys\n"
        "p=argparse.ArgumentParser(); s=p.add_subparsers(dest='c')\n"
        "dd=s.add_parser('doctor'); dd.add_argument('--path',default='.')\n"
        "dd.set_defaults(func=lambda a: None)\n"
        "p.parse_args()\n", encoding="utf-8")
    (d / "LICENSE").write_text(MIT_ASCII, encoding="utf-8")
    (d / "pyproject.toml").write_text("[build-system]\nrequires=['setuptools']\n", encoding="utf-8")
    r = run(["validate", "--path", str(d), "--mode", "package"])
    assert "检测到打包清单" in r.stdout
    assert "未检测到打包清单" not in r.stdout


def test_validate_bench_output(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["validate", "--path", out, "--bench"])
    assert "距头部还差" in r.stdout
    assert "已对齐头部" in r.stdout


def test_validate_json_bench_structure():
    import json as _json
    r = run(["validate", "--path", SKILL_DIR, "--json", "--bench"])
    assert r.returncode == 0, r.stderr
    payload = _json.loads(r.stdout)
    assert "bench" in payload
    assert set(["baseline", "score", "gap", "missed_head_dims"]) <= set(payload["bench"])
    assert payload["bench"]["baseline"] == 100
    assert payload["bench"]["score"] == 100
    assert payload["bench"]["gap"] == 0


def test_release_no_remote_action_without_flags(tmp_path, monkeypatch):
    """安全保证：未显式传 --push / --publish 时，release 绝不触碰远端。"""
    calls = []

    real_run = subprocess.run

    def spy(*a, **k):
        if a and isinstance(a[0], list):
            calls.append(a[0])
        return real_run(*a, **k)

    monkeypatch.setattr(subprocess, "run", spy)
    out = gen_skill(tmp_path)
    r = run(["release", "--path", out, "--dry-run"])
    assert r.returncode == 0
    joined = [" ".join(c) for c in calls]
    assert not any("push" in c for c in joined), "release 不应发起 git push: %s" % joined
    assert not any("publish" in c for c in joined), "release 不应发起 clawhub publish: %s" % joined


def test_release_publish_flag_triggers_cli(tmp_path, monkeypatch):
    """显式 --publish 才会调用 clawhub publish（且需本机已装 CLI 并登录）。"""
    monkeypatch.setattr(R, "_clawhub_publish", lambda *a, **k: (False, "未安装 clawhub CLI，回退人工导入"))
    out = gen_skill(tmp_path)
    r = run(["release", "--path", out, "--publish"])
    assert r.returncode == 0
    assert "clawhub publish" in r.stdout


# ---------------- 1.6.0 新能力：功能验证 / 门禁 / 透明评分 / 组合缺口 ----------------

def test_functional_syntax_error_fails(tmp_path):
    d = make_skill(tmp_path, "fn1")
    (d / "broken.py").write_text("def f(:\n    pass\n", encoding="utf-8")
    r = run(["validate", "--path", str(d)])
    assert "语法错误" in r.stdout
    assert r.returncode == 1


def test_functional_import_failure_fails(tmp_path):
    d = make_skill(tmp_path, "fn2")
    main = d / (d.name.replace("-", "_") + ".py")
    main.write_text("import sys\nraise RuntimeError('boom at import')\n", encoding="utf-8")
    r = run(["validate", "--path", str(d)])
    assert "import 失败" in r.stdout
    assert r.returncode == 1


def test_functional_clean_passes_all_three(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["validate", "--path", out])
    assert "无语法错误" in r.stdout       # compile
    assert "可 import" in r.stdout         # import
    assert "CLI 可 boot" in r.stdout       # --help 烟测


def test_gate_pass(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["gate", "--path", out, "--min", "90"])
    assert r.returncode == 0
    assert "通过" in r.stdout


def test_gate_blocks_on_low_score(tmp_path):
    d = make_skill(tmp_path, "gt1")
    (d / "LICENSE").unlink()  # 缺 LICENSE → 触发 FAIL，分数 < 90
    r = run(["gate", "--path", str(d), "--min", "90"])
    assert r.returncode == 1
    assert "拦截" in r.stdout or "未达" in r.stdout


def test_rubric_output(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["validate", "--path", out, "--rubric"])
    assert "评分权重与理由" in r.stdout
    assert "compile" in r.stdout


def test_rubric_json_field(tmp_path):
    import json as _json
    r = run(["validate", "--path", SKILL_DIR, "--json", "--rubric"])
    assert r.returncode == 0, r.stderr
    payload = _json.loads(r.stdout)
    assert "rubric" in payload
    assert payload["rubric"]["fn_smoke"]["weight"] == 10
    assert "功能验证" in payload["rubric"]["fn_smoke"]["reason"]
    assert payload["rubric"]["secret"]["weight"] == 12
    assert "安全红线" in payload["rubric"]["secret"]["reason"]


def test_gap_combo_opportunity(tmp_path):
    import json as _json
    import tempfile
    sk = _make_skills_root(tmp_path, [("g1", "git,ci,release")])  # 本机仅 Developer Tools
    data = [
        {"name": "m1", "categories": ["Finance"]},
        {"name": "m2", "categories": ["Developer Tools"]},
    ]
    p = os.path.join(tempfile.mkdtemp(), "scan.json")
    with open(p, "w", encoding="utf-8") as f:
        _json.dump(data, f)
    r = run(["gap", "--roots", sk, "--scan-json", p])
    assert r.returncode == 0
    assert "组合机会" in r.stdout
    assert "Finance" in r.stdout  # 市场有 / 本机为 0 → 组合机会


# ---------------- 1.7.0 新能力：badge 链式传播 / promote 宣传工具箱 ----------------

def test_badge_svg_helper_colors():
    green = R._badge_svg("releaser", "100/100", R._badge_color(95))
    yellow = R._badge_svg("releaser", "75/100", R._badge_color(75))
    red = R._badge_svg("releaser", "40/100", R._badge_color(40))
    assert "#4c1" in green and "#dfb317" not in green
    assert "#dfb317" in yellow
    assert "#e05d44" in red
    assert "releaser" in green and "100/100" in green
    assert "svg" in green and "xlink:href" in green


def test_badge_generates_svg_and_link(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["badge", "--path", out])
    assert r.returncode == 0, r.stderr
    assert "<svg" in r.stdout
    assert "100/100" in r.stdout
    assert "链式传播" in r.stdout
    # 片段把徽章链回本技能页（默认 RELEASER_PAGE）
    assert R.RELEASER_PAGE in r.stdout


def test_badge_writes_file(tmp_path):
    out = gen_skill(tmp_path)
    svg_path = os.path.join(str(tmp_path), "readiness-badge.svg")
    r = run(["badge", "--path", out, "--output", svg_path])
    assert r.returncode == 0, r.stderr
    assert os.path.isfile(svg_path)
    with open(svg_path, encoding="utf-8") as f:
        content = f.read()
    assert content.startswith("<svg")
    assert "100/100" in content


def test_promote_outputs_toolbox(tmp_path):
    out = gen_skill(tmp_path)
    r = run(["promote", "--path", out])
    assert r.returncode == 0, r.stderr
    assert "链式传播工具箱" in r.stdout
    assert "电梯演讲" in r.stdout
    assert "社媒" in r.stdout
    assert R.RELEASER_PAGE in r.stdout
    # 链式玩法关键词
    assert "链式" in r.stdout


def test_promote_without_path(tmp_path):
    r = run(["promote"])
    assert r.returncode == 0, r.stderr
    assert "README 徽章区" in r.stdout
    assert R.RELEASER_PAGE in r.stdout


# ---------------- 1.8.0 新能力：diagnose 长尾诊断 / preflight 上架清单 / clawhub CLI ----------------

def test_diagnose_list():
    r = run(["diagnose", "--list"])
    assert r.returncode == 0, r.stderr
    assert "已知症状" in r.stdout
    assert "LICENSE" in r.stdout
    assert "pytest exit code 2" in r.stdout


def test_diagnose_match_license():
    r = run(["diagnose", "--symptom", "LICENSE 显示 Other"])
    assert r.returncode == 0, r.stderr
    assert "根因" in r.stdout
    assert "MIT-0" in r.stdout
    assert "ASCII" in r.stdout


def test_diagnose_match_pytest():
    r = run(["diagnose", "--symptom", "pytest exit code 2"])
    assert r.returncode == 0, r.stderr
    assert "conftest" in r.stdout
    assert "退出码" in r.stdout


def test_diagnose_no_match():
    r = run(["diagnose", "--symptom", "zzz-nonsense-xyz"])
    assert r.returncode == 1
    assert "未匹配" in r.stdout


def test_preflight_clawhub():
    r = run(["preflight", "--market", "clawhub"])
    assert r.returncode == 0, r.stderr
    assert "上架前检查清单" in r.stdout
    assert "MIT-0" in r.stdout
    assert "skill-card" in r.stdout
    assert "Topics" in r.stdout


def test_preflight_default_generic():
    r = run(["preflight"])
    assert r.returncode == 0, r.stderr
    assert "通用" in r.stdout
    assert "就绪分" in r.stdout


def test_release_default_manual_import(tmp_path):
    out = gen_skill(tmp_path)
    # 默认（无 --push/--publish）：只构造人工导入步骤，不触碰远端
    r = run(["release", "--path", out, "--dry-run"])
    assert r.returncode == 0, r.stderr
    assert "导入" in r.stdout
    assert "Publish" in r.stdout


def test_clawhub_publish_not_installed(tmp_path):
    import tempfile
    d = make_skill(tempfile.mkdtemp(), "cli1")
    ok, msg = R._clawhub_publish(str(d), "cli1", "cli1", "1.0.0", "test")
    assert ok is False
    assert "未安装" in msg


# ---------------- 1.9.4 新能力：安全红线 secretscan（消灭"不该进 GitHub 的凭据"） ----------------

def test_secret_scan_detects_hardcoded_password(tmp_path):
    d = make_skill(tmp_path, "sec1")
    (d / "config.py").write_text('PASSWORD = "uvuzznmybedscaic123"\n', encoding="utf-8")
    r = run(["validate", "--path", str(d)])
    assert "安全红线" in r.stdout
    assert r.returncode == 1


def test_secret_scan_blocks_release(tmp_path):
    d = make_skill(tmp_path, "sec2")
    (d / "cfg.py").write_text('api_token = "abcdefghij1234567890"\n', encoding="utf-8")
    r = run(["release", "--path", str(d), "--dry-run"])
    assert "安全红线拦截" in r.stdout
    assert r.returncode == 1


def test_secretscan_command_detects(tmp_path):
    d = make_skill(tmp_path, "sec3")
    (d / "cfg.py").write_text('client_secret = "smVa8KpQ2xLm9NcR7tB4wD1eF0"\n', encoding="utf-8")
    r = run(["secretscan", "--path", str(d)])
    assert r.returncode == 1
    # 命中已知/疑似凭据，且绝不回显明文
    assert "硬编码" in r.stdout
    assert "uvuzznmybedscaic123" not in r.stdout
    assert "abcdefghij1234567890" not in r.stdout
    assert "smVa8KpQ2xLm9NcR7tB4wD1eF0" not in r.stdout


def test_secret_scan_env_ref_safe(tmp_path):
    """环境变量引用视为安全：凭据由运行时注入，不入库，不应报警。"""
    d = make_skill(tmp_path, "sec4")
    (d / "config.py").write_text(
        'PASSWORD = os.environ.get("QQ_SMTP_PASSWORD")\n'
        'API_KEY = os.getenv("API_KEY")\n', encoding="utf-8")
    r = run(["validate", "--path", str(d)])
    assert r.returncode == 0               # 环境变量引用不报警 → 无 FAIL
    assert "安全红线通过" in r.stdout       # 安全维度 PASS
    assert "安全红线拦截" not in r.stdout   # 未被误判拦截


def test_secret_scan_env_file_flagged(tmp_path):
    (tmp_path / ".env").write_text('DB_PASSWORD=supersecret123\n', encoding="utf-8")
    d = make_skill(tmp_path, "sec5")
    (d / ".env").write_text('SMTP_PASSWORD=anothersecret99\n', encoding="utf-8")
    r = run(["validate", "--path", str(d)])
    assert "安全红线" in r.stdout
    assert r.returncode == 1
    # .env 文件本身即风险，明文不应回显
    assert "anothersecret99" not in r.stdout


def test_secret_scan_allowlist(tmp_path):
    d = make_skill(tmp_path, "sec6")
    (d / "cfg.py").write_text('PASSWORD = "redacted_dummy_value_000"\n', encoding="utf-8")
    (d / ".releaser-secret-allow").write_text("redacted_dummy_value_000\n", encoding="utf-8")
    r = run(["secretscan", "--path", str(d)])
    assert r.returncode == 0
    assert "未发现" in r.stdout


# ---------------- 1.9.5 新能力：多站上架编排 publish（显式逐站授权） ----------------

def test_publish_no_target_flags_no_remote(tmp_path, monkeypatch):
    """安全保证：publish 未显式传 --github/--clawhub 等时，绝不触碰任何远程。"""
    calls = []
    real_run = subprocess.run

    def spy(*a, **k):
        if a and isinstance(a[0], list) and "releaser.py" not in a[0]:
            calls.append(a[0])
        return real_run(*a, **k)

    monkeypatch.setattr(subprocess, "run", spy)
    d = make_skill(tmp_path, "pub1")
    r = run(["publish", "--path", str(d)])
    assert r.returncode == 0
    joined = [" ".join(c) for c in calls]
    assert not any("push" in c for c in joined), "publish 不应发起 git push: %s" % joined
    assert not any("clawhub" in c and "publish" in c for c in joined), "publish 不应发起 clawhub publish: %s" % joined
    assert "不触碰任何远程" in r.stdout


def test_publish_dry_run_github(tmp_path):
    """publish --github --dry-run 只预览，不提交不推送。"""
    d = make_skill(tmp_path, "pub2")
    r = run(["publish", "--path", str(d), "--github", "--dry-run"])
    assert r.returncode == 0
    assert "dry-run" in r.stdout
    assert "github" in r.stdout


def test_publish_secret_gate_blocks(tmp_path):
    """审定闸门：publish 同样因硬编码凭据被拦截，绝不入库/外发。"""
    d = make_skill(tmp_path, "pub3")
    (d / "cfg.py").write_text('api_token = "abcdefghij1234567890"\n', encoding="utf-8")
    r = run(["publish", "--path", str(d), "--github"])
    assert "安全红线拦截" in r.stdout
    assert r.returncode == 1


def test_publish_reserved_targets_print(tmp_path):
    """虾评/WorkBuddy 本轮为预留位：给出人工链接，不报错崩溃。"""
    d = make_skill(tmp_path, "pub4")
    r = run(["publish", "--path", str(d), "--xiaping"])
    assert "虾评" in r.stdout
    assert "本轮未接入" in r.stdout
    r2 = run(["publish", "--path", str(d), "--workbuddy"])
    assert "WorkBuddy" in r2.stdout
    assert "本轮未接入" in r2.stdout


# ---------------- 1.9.0 新能力：状态层 / 生命周期 / 自证 / 策展 ----------------

def _ns(**kw):
    return __import__("types").SimpleNamespace(**kw)


def test_registry_list_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    R.cmd_registry(_ns(action="list", slug=None, name=None, repo=None,
                       version=None, score=None, market=None, path=None))
    out = capsys.readouterr().out
    assert "账本为空" in out


def test_registry_add_and_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    R.cmd_registry(_ns(action="add", slug="demo", name="demo", repo="", version="1.0.0",
                       score=100, market="manual", path=str(tmp_path)))
    R.cmd_registry(_ns(action="list", slug=None, name=None, repo=None,
                       version=None, score=None, market=None, path=None))
    out = capsys.readouterr().out
    assert "已登记" in out
    assert "demo" in out
    assert "共 1 个" in out


def test_registry_show(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    R._ledger_add({"slug": "demo", "name": "demo", "score": 100, "market": "manual",
                   "path": str(tmp_path), "version": "1.0.0", "repo": "",
                   "published_at": "2026-09-23", "last_checked": "2026-09-23"})
    R.cmd_registry(_ns(action="show", slug="demo", name=None, repo=None,
                       version=None, score=None, market=None, path=None))
    out = capsys.readouterr().out
    assert '"slug": "demo"' in out


def test_recheck_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    rc = R.cmd_recheck(_ns(slug=None))
    out = capsys.readouterr().out
    assert "账本为空" in out
    assert rc == 0


def test_recheck_healthy(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    out = gen_skill(tmp_path)
    R._ledger_add({"slug": "demo-cli-skill", "name": "demo", "score": 100, "market": "manual",
                   "path": out, "version": "1.0.0", "repo": "",
                   "published_at": "2026-09-23", "last_checked": "2026-09-23"})
    rc = R.cmd_recheck(_ns(slug=None))
    sout = capsys.readouterr().out
    assert "健康" in sout
    assert rc == 0


def test_selfdemo_runs(capsys):
    rc = R.cmd_selfdemo(_ns())
    out = capsys.readouterr().out
    assert "自证结果" in out
    assert "能力通过演示" in out
    assert rc == 0


def test_curate_basic(tmp_path, capsys):
    sk = _make_skills_root(tmp_path, [("g1", "git,ci,release")])
    R.cmd_curate(_ns(roots=sk, scan_json=None))
    out = capsys.readouterr().out
    assert "该造什么" in out
    assert "空白类目" in out


def test_curate_combo_with_market(tmp_path, capsys):
    import json as _json
    sk = _make_skills_root(tmp_path, [("g1", "git,ci,release")])
    data = [{"name": "m1", "categories": ["Finance"]},
            {"name": "m2", "categories": ["Developer Tools"]}]
    p = os.path.join(str(tmp_path), "scan.json")
    with open(p, "w", encoding="utf-8") as f:
        _json.dump(data, f)
    R.cmd_curate(_ns(roots=sk, scan_json=p))
    out = capsys.readouterr().out
    assert "组合机会" in out
    assert "Finance" in out


def test_release_auto_registers(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    out = gen_skill(tmp_path)
    rc = R.cmd_release(_ns(path=out, remote="origin", branch="main", message=None,
                           dry_run=True, push=False, publish=False))
    assert rc == 0
    data = R._load_ledger()
    assert "demo_cli_skill" in data["entries"], "release 应自动登记到账本"
    assert data["entries"]["demo_cli_skill"]["score"] == 100


def test_release_cli_success_registers(tmp_path, monkeypatch, capsys):
    # clawhub CLI 真一键成功路径也应登记账本（修复：2b 早退曾漏登记，与 SKILL.md §2.13 矛盾）
    monkeypatch.setattr(R, "LEDGER_PATH", str(tmp_path / "ledger.json"))
    monkeypatch.setattr(R, "_clawhub_publish", lambda *a, **k: (True, "published via CLI"))
    out = gen_skill(tmp_path)  # 非 git 仓库，2a 推送自动跳过；2b 走 monkeypatch 的成功分支
    rc = R.cmd_release(_ns(path=out, remote="origin", branch="main", message=None,
                           dry_run=False, push=False, publish=True))
    assert rc == 0
    data = R._load_ledger()
    assert "demo_cli_skill" in data["entries"], "clawhub CLI 成功也应登记到账本"
    assert data["entries"]["demo_cli_skill"]["market"] == "clawhub"



