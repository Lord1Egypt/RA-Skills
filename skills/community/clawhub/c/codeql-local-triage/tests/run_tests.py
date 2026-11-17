#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-test: needs no CodeQL — it asserts against the two measured SARIF files checked in the repo.

自测：不需要安装 CodeQL，用仓库内已存的两份实测 SARIF 做断言。

    python tests/run_tests.py        # also works under pytest / 也兼容 pytest

Note for pytest: this file is named ``run_tests.py``, so pytest will **not** auto-collect it —
pass the path explicitly (``pytest tests/run_tests.py``). ``pytest tests/`` collects nothing.
pytest 注记：本文件名不匹配 ``test_*.py``，pytest 不会自动收集，须显式指定路径；
``pytest tests/`` 收集不到任何用例。

Coverage / 覆盖：
  1. regex self-test of the prefilter (the classifier agrees with the QL definitions)
     预筛脚本的正则自检（分类器与 QL 定义一致）
  2. repro/scan.py yields 1 candidate source; repro_fixed/scan.py is clean
     repro/scan.py 命中 1 处候选源，repro_fixed/scan.py 干净
  3. the two fixtures are byte-identical apart from the variable name — one variable only
     两份 fixture「除变量名外逐字节相同」——保证对照实验只有一个变量
  4. read_sarif reads the two measured SARIF files correctly (1 / 0) and honours --expect
     read_sarif 能正确判读两份实测 SARIF（1 条 / 0 条）与 --expect 断言
  5. read_sarif recovers the source line from codeFlows, and it is that sensitive-name assignment
     read_sarif 能从 codeFlows 里取回 source 行，且就是那行敏感名赋值

Note: the test harness's own check labels below are fixed strings; the *target scripts*
honour ``--lang`` / ``TRIAGE_LANG`` — run ``python tests/run_tests.py --lang en`` to exercise
the scripts in English. / 说明：本测试自身的检查标签为固定字符串；被测脚本尊重
``--lang`` / ``TRIAGE_LANG`` —— 用 ``python tests/run_tests.py --lang en`` 即可让被测脚本以英文运行。
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN = ROOT / "scripts" / "scan_sensitive_sources.py"
READ = ROOT / "scripts" / "read_sarif.py"
BISECT = ROOT / "scripts" / "bisect_taint.py"
REPRO = ROOT / "tests" / "fixtures" / "repro" / "scan.py"
REPRO_FIXED = ROOT / "tests" / "fixtures" / "repro_fixed" / "scan.py"
SARIF_HIT = ROOT / "tests" / "fixtures" / "sarif" / "repro.sarif"
SARIF_CLEAN = ROOT / "tests" / "fixtures" / "sarif" / "repro_fixed.sarif"

FAILS: list[str] = []


def _run(script: Path, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    # 列表传参、shell=False、执行本仓脚本（本地受信），无外部输入（S5 安全整改）
    run_env = dict(os.environ)
    if env:
        run_env.update(env)
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          shell=False, env=run_env)


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + ("" if cond else f"    {detail}"))
    if not cond:
        FAILS.append(name)


def test_prefilter_self_test() -> None:
    r = _run(SCAN, "--self-test")
    check("预筛脚本正则自检通过", r.returncode == 0, r.stdout[-300:])


def test_skill_frontmatter_is_plain_yaml() -> None:
    """SKILL.md 的 frontmatter 必须是朴素 YAML。

    普通标量里出现「冒号 + 空格」会让 key 被静默截断（技能加载失败却没有任何报错）。
    中文用全角冒号是安全的；英文冒号后若要跟空格，必须把整个值加引号。
    """
    fm = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    risks = []
    for i, line in enumerate(fm.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or ": " in value or value.rstrip().endswith(":"):
            risks.append(f"L{i} key={key!r}")
    check("SKILL.md frontmatter 无「冒号+空格」类 YAML 陷阱", not risks, "; ".join(risks))


def test_frontmatter_has_progressive_disclosure_fields() -> None:
    """v1.0.6 重构：frontmatter 必须齐备渐进式披露所需的四类字段。

    这些字段是**加载期**契约，缺一个就可能让技能静默退化（例如没有 allowed-tools 时
    工具范围不受约束；没有 when_to_use 时触发判断全靠 description 猜）。
    """
    fm = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    required = {
        "触发描述": "description",
        "使用时机": "when_to_use",
        "工具白名单": "allowed-tools",
        "上下文隔离": "context",
        "版本": "version",
    }
    missing = [f"{cn}({en})" for cn, en in required.items() if not re.search(rf"^{en}:", fm, re.M)]
    check("SKILL.md frontmatter 齐备触发/时机/工具/上下文字段",
          not missing, "缺: " + ", ".join(missing))

    # allowed-tools 必须显式排除联网工具——本技能 H8 承诺「不联网」
    m = re.search(r"^allowed-tools:\s*\[(.*?)\]", fm, re.M)
    tools = m.group(1) if m else ""
    check("allowed-tools 排除联网工具（H8 不联网）",
          "WebFetch" not in tools and "WebSearch" not in tools,
          f"实际: {tools!r}")

    # context: fork —— 子任务定位，避免污染主对话
    check("标注 context: fork（子任务隔离）",
          re.search(r"^context:\s*fork\s*$", fm, re.M) is not None)

    # 网络权限声明必须为 none
    check("permissions 网络声明为 none",
          re.search(r'network:\s*"none"', fm) is not None)


def test_hard_constraints_are_marked_every_turn() -> None:
    """v1.0.6 重构核心：硬约束必须显式标注「每轮重读」，且编号连续。

    这是抗上下文压缩的设计——压缩后 agent 只可能读到文件前部，
    所以硬约束必须靠前、且自我声明为「每轮必读」。
    """
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    check("§0 显式声明「每轮重读」",
          re.search(r"re-read these every turn", t) is not None)
    check("§0 段落明确提到上下文压缩",
          "context compression" in t)

    ids = sorted({int(m[1:]) for m in re.findall(r"\*\*(H\d+)\*\*", t)})
    check("硬约束编号连续无缺号（H1..Hn）",
          len(ids) >= 8 and ids == list(range(1, len(ids) + 1)),
          f"实际: {ids}")

    # 硬约束必须出现在单次流程之前（否则压缩时先被截掉）
    i_h = t.index("HARD CONSTRAINTS")
    i_f = t.index("SINGLE-RUN FLOW")
    check("硬约束排在单次流程之前", i_h < i_f, f"{i_h} vs {i_f}")


def test_single_run_flow_is_five_steps_with_fallbacks() -> None:
    """v1.0.6 重构：单次执行流程必须 ≤5 步，且每步写明输入/输出/失败兜底。

    「单轮内闭环」是硬要求——agent 不应为了完成一步而回头重读技能文件。
    """
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    body = t.split("## §1. SINGLE-RUN FLOW")[1].split("## §2.")[0]
    steps = re.findall(r"^### Step (\d+)", body, re.M)
    check("单次流程步数 ≤5 且编号连续",
          len(steps) <= 5 and steps == [str(i) for i in range(1, len(steps) + 1)],
          f"实际: {steps}")
    # 每个执行型步骤（1-4）必须有 Input / Run / Output / Fallback 四要素；
    # Step 5 是「交付」步骤，天然没有输入与命令，只需 Output + Fallback。
    check("每步都有 Output 与 Fallback",
          body.count("**Output**") == len(steps)
          and body.count("**Fallback**") == len(steps),
          f"steps={len(steps)} out={body.count('**Output**')} "
          f"fb={body.count('**Fallback**')}")
    exec_steps = len(steps) - 1 if "Deliver" in body else len(steps)
    check("执行型步骤（1..N-1）都有 Input / Run",
          body.count("**Input**") == exec_steps
          and body.count("**Run**") == exec_steps,
          f"expect={exec_steps} in={body.count('**Input**')} run={body.count('**Run**')}")


def test_progressive_disclosure_length_budget() -> None:
    """v1.0.6 重构：篇幅预算——全文 ≤8000 token，核心规则（§0+§1）≤3000 token。

    token 数为估算（ASCII≈4 chars/token，CJK≈1.4 chars/token），留足余量。
    """
    import re as _re

    def est(s: str) -> float:
        cjk = len(_re.findall(r"[\u4e00-\u9fff]", s))
        return len(s) / 4 + cjk * 0.7

    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    total = est(t)
    check("SKILL.md 全文 ≤8000 token", total <= 8000, f"实测 ~{total:.0f}")

    i_ctx = t.index("## §2.")
    core = est(t[:i_ctx])
    check("核心规则（§0 硬约束 + §1 流程）≤3000 token", core <= 3000,
          f"实测 ~{core:.0f}")


def test_both_language_files_mirror_frontmatter_fields() -> None:
    """v1.0.6：两份 SKILL 的 frontmatter 关键字段必须一致（版本 + 加载契约）。"""
    en = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    zh = (ROOT / "SKILL.zh.md").read_text(encoding="utf-8").split("---")[1]
    for field in ("version", "when_to_use", "allowed-tools", "context"):
        e = re.search(rf"^{field}:(.*)$", en, re.M)
        z = re.search(rf"^{field}:(.*)$", zh, re.M)
        check(f"中英 frontmatter 都有 {field}", bool(e and z),
              f"en={bool(e)} zh={bool(z)}")
    # 版本号必须一致（发版前最后一道闸）
    ev = re.search(r"^version:\s*(\S+)", en, re.M)
    zv = re.search(r"^version:\s*(\S+)", zh, re.M)
    check("中英版本号一致", ev and zv and ev.group(1) == zv.group(1),
          f"en={ev and ev.group(1)} zh={zv and zv.group(1)}")
    # 中文版不得出现 name/slug（防双技能误注册）
    check("SKILL.zh.md 无 name/slug（防双技能误注册）",
          re.search(r"^(name|slug):", zh, re.M) is None)


def test_repro_has_one_source() -> None:
    r = _run(SCAN, str(REPRO), "--json")
    data = json.loads(r.stdout)
    check("repro/scan.py 命中 1 处候选源", data["total_sources"] == 1,
          f"实际 {data['total_sources']}")
    srcs = data["files"][0]["sources"]
    if srcs:
        check("命中项是 SECRET_PATTERNS 的赋值",
              "SECRET_PATTERNS" in srcs[0]["label"] and srcs[0]["hits"] == ["secret"],
              json.dumps(srcs[0], ensure_ascii=False))
    check("有候选源时退出码为 1", r.returncode == 1, f"实际 {r.returncode}")


def test_fixed_is_clean() -> None:
    r = _run(SCAN, str(REPRO_FIXED), "--json")
    data = json.loads(r.stdout)
    check("repro_fixed/scan.py 无候选源", data["total_sources"] == 0,
          f"实际 {data['total_sources']}")
    check("无候选源时退出码为 0", r.returncode == 0, f"实际 {r.returncode}")


def test_missing_path_returns_2() -> None:
    """R1 回归：缺失路径必须返回 2（输入错误），绝不能误判为 0（干净）。"""
    r = _run(SCAN, "this_path_does_not_exist_anywhere_12345.py", "--json")
    check("缺失路径时退出码为 2（非 0）", r.returncode == 2, f"实际 {r.returncode}")
    check("缺失路径时 stderr 给出提示",
          "this_path_does_not_exist_anywhere_12345.py" in r.stderr, r.stderr[-200:])


def test_fixtures_differ_only_in_name() -> None:
    """两份 fixture 必须「除这个变量名外」逐字节相同，否则对照实验混入了别的变量。

    断言方式是**严格**的：把 repro 里的这个名字全局替换掉，结果必须与 repro_fixed
    完全相等。所以两份 .py 里除代码外**不能**出现这个名字（说明文字已移到
    tests/fixtures/README.md），否则全局替换会连文档一起改掉、断言不成立。
    """
    a = REPRO.read_text(encoding="utf-8")
    b = REPRO_FIXED.read_text(encoding="utf-8")
    replaced = a.replace("SECRET_PATTERNS", "CREDENTIAL_PATTERNS")
    diff_desc = ""
    if replaced != b:
        al, bl = replaced.splitlines(), b.splitlines()
        for i, (x, y) in enumerate(zip(al, bl), 1):
            if x != y:
                diff_desc = f"首个差异在第 {i} 行: {x!r} != {y!r}"
                break
        else:
            diff_desc = f"行数不同: {len(al)} != {len(bl)}"
    check("两份 fixture 除该变量名外逐字节相同（严格替换比对）", replaced == b, diff_desc)
    # 该名字只应出现在代码里：赋值 1 处 + for 循环 1 处。若有人往 docstring 里补一句说明，
    # 全局替换就会连文档一起改掉，上面的严格比对随之失效——这项断言专门守这个。
    check("repro 中该变量名只出现在代码里（2 处）",
          a.count("SECRET_PATTERNS") == 2, f"实际出现 {a.count('SECRET_PATTERNS')} 次")


def test_read_sarif_counts() -> None:
    # SkillHub 的发布包封禁 .sarif（实测 400），故这两个 fixture 在该平台上不存在。
    # 缺失时**跳过而非判失败**——否则包一旦发出去，自测就永远红，等于交付一个"必失败"的技能。
    # 完整仓库（GitHub / ClawHub / 本地）保留 fixture，这两条断言照常生效。
    if not SARIF_HIT.is_file() or not SARIF_CLEAN.is_file():
        print("  skip  SARIF fixtures 不在本包内（SkillHub 封禁 .sarif）—— 跳过 SARIF 读数断言")
        return
    r = _run(READ, str(SARIF_HIT), "--expect", "1")
    check("repro.sarif 结果数 = 1（--expect 断言通过）", r.returncode == 0, r.stdout[-300:])
    r = _run(READ, str(SARIF_CLEAN), "--expect", "0")
    check("repro_fixed.sarif 结果数 = 0（--expect 断言通过）", r.returncode == 0, r.stdout[-300:])


def test_read_sarif_extracts_source() -> None:
    if not SARIF_HIT.is_file():
        return
    r = _run(READ, str(SARIF_HIT), "--json")
    info = json.loads(r.stdout)["sarifs"][0]
    res = info["results"][0]
    check("评到 error 级", res["level"] == "error", res["level"])
    check("规则是 py/clear-text-storage-sensitive-data",
          res["rule"] == "py/clear-text-storage-sensitive-data", res["rule"])
    check("消息指明分类为 secret", "secret" in res["message"], res["message"])
    flows = res["flows"]
    check("至少有一条 codeFlows 数据流", bool(flows), "SARIF 里没有数据流")
    if flows:
        src = flows[0][0]
        check("数据流起点落在 SECRET_PATTERNS 那一行",
              REPRO.read_text(encoding="utf-8").splitlines()[src["line"] - 1]
              .strip().startswith("SECRET_PATTERNS"),
              f"{src['file']}:{src['line']} {src['role']}")
        check("数据流终点是写文件那行",
              REPRO.read_text(encoding="utf-8").splitlines()[flows[0][-1]["line"] - 1]
              .strip().startswith("Path(out).write_text"),
              f"{flows[0][-1]['file']}:{flows[0][-1]['line']}")


def test_sarif_structure_errors() -> None:
    """S1-1 回归：坏 SARIF 必须给出可定位的错误并返回 2，绝不静默返回「0 条结果」。

    「把读错文件当成干净」是最危险的误判，因此这里逐个结构异常都要拦住。
    """
    tmp = Path(tempfile.gettempdir())
    cases = {
        "not_sarif": b'{"foo": "bar"}\n',                    # 缺 runs 顶层
        "runs_not_list": b'{"runs": {}}\n',                  # runs 类型错
        "run_not_obj": b'{"runs": ["x"]}\n',                 # runs 元素非对象
        "results_not_list": b'{"runs": [{"results": "oops"}]}\n',
        "result_not_obj": b'{"runs": [{"results": [1]}]}\n',
    }
    for name, payload in cases.items():
        f = tmp / f"_cql_bad_{name}.json"
        f.write_bytes(payload)
        try:
            r = _run(READ, str(f))
            check(f"畸形 SARIF（{name}）退出码为 2",
                  r.returncode == 2, f"实际 {r.returncode}")
            check(f"畸形 SARIF（{name}）stderr 有可读诊断",
                  "[error]" in r.stderr, r.stderr[-160:])
        finally:
            f.unlink(missing_ok=True)

    # 真语法错误：必须定位到行列 + 给出出错行内容
    f = tmp / "_cql_badjson.json"
    f.write_bytes(b'{\n "runs": [\n  {broken\n ]\n}\n')
    try:
        r = _run(READ, str(f))
        check("坏 JSON 定位到行号", "line 3" in r.stderr, r.stderr[-200:])
        check("坏 JSON 给出出错处内容", "broken" in r.stderr, r.stderr[-200:])
        check("坏 JSON 给出修复建议", "how to fix" in r.stderr, r.stderr[-200:])
    finally:
        f.unlink(missing_ok=True)


def test_variant_arg_validation() -> None:
    """S1-2 回归：--variant 四类格式错误必须各自返回 2 并附修复建议。"""
    base = ["--source", "scan.py", "--tree", str(REPRO.parent), "--dry-run"]
    bad = {
        "缺=": ["--variant", "NOEQUALS"],
        "缺:": ["--variant", "t2=NOCOLON"],
        "变体名为空": ["--variant", "=X:Y"],
        "与control重名": ["--variant", "t1_control=X:Y"],
        "NEW为空": ["--variant", "t2=SECRET_PATTERNS:"],
    }
    for name, extra in bad.items():
        r = _run(BISECT, *base, *extra)
        check(f"--variant {name} 被显式拦截（退出码 2）", r.returncode == 2,
              f"实际 {r.returncode}: {r.stderr[-140:]}")
        check(f"--variant {name} 附修复建议",
              "how to fix" in r.stderr, r.stderr[-160:])

    # 自己撞自己也要拦
    r = _run(BISECT, *base, "--variant", "t2=SECRET_PATTERNS:X",
             "--variant", "t2=A:B")
    check("--variant 自重复名被拦截", r.returncode == 2, f"实际 {r.returncode}")


def test_scan_jobs_and_summary() -> None:
    """S1-4 回归：--summary 汇总表、--jobs 并行、批量退出码契约。"""
    fixtures = REPRO.parent.parent          # tests/fixtures（含 repro 与 repro_fixed 两个目录）
    r = _run(SCAN, str(fixtures), "--summary")
    check("--summary 列出全部 fixture 文件",
          "repro" in r.stdout and "repro_fixed" in r.stdout, r.stdout[-300:])
    check("--summary 有汇总行", "Total:" in r.stdout, r.stdout[-200:])

    # 并行与串行结果必须一致（计数相同）
    r1 = _run(SCAN, str(fixtures), "--summary", "--jobs", "1")
    r4 = _run(SCAN, str(fixtures), "--summary", "--jobs", "4")
    check("--jobs 1 与 --jobs 4 结果一致", r1.stdout == r4.stdout,
          "并行与串行输出不一致")
    check("并行时退出码仍为 1（有候选源）", r1.returncode == 1 and r4.returncode == 1,
          f"{r1.returncode}/{r4.returncode}")

    # 批量退出码契约：任一命中→1；全干净→0；路径全缺→2
    check("全干净目录退出码 0",
          _run(SCAN, str(REPRO_FIXED.parent), "--summary").returncode == 0)
    check("含候选源目录退出码 1",
          _run(SCAN, str(fixtures), "--summary").returncode == 1)
    check("路径全缺失退出码 2",
          _run(SCAN, "no_such_dir_xyz", "--summary").returncode == 2)

    # --jobs 非法值必须被拦
    r = _run(SCAN, str(fixtures), "--summary", "--jobs", "0")
    check("--jobs 0 被拦截", r.returncode != 0, f"实际 {r.returncode}")


def test_path_gating() -> None:
    """v1.0.7 P0：--source 绝对路径 / 含 ".." 必须被门禁拦下（exit 2），且不触碰目标文件。"""
    import hashlib
    outside = Path(tempfile.gettempdir()) / "_cql_outside_src.py"
    outside.write_text("SECRET_PATTERNS = ['a']\n", encoding="utf-8")
    before_sha = hashlib.sha256(outside.read_bytes()).hexdigest()

    # 绝对路径：应在 src_rel 门禁处被拦（根本不会去读 is_file / 写盘）
    r = _run(BISECT, "--source", str(outside), "--tree", str(REPRO.parent),
             "--dry-run", "--variant", "t2=SECRET_PATTERNS:CREDENTIAL_PATTERNS")
    check("绝对路径 --source 被门禁拦下（exit 2）", r.returncode == 2,
          f"实际 {r.returncode}: {r.stderr[-160:]}")
    check("绝对路径 --source 未触碰目标文件（sha256 不变）",
          hashlib.sha256(outside.read_bytes()).hexdigest() == before_sha)

    # 含 ".." 的相对路径
    r = _run(BISECT, "--source", "../outside.py", "--tree", str(REPRO.parent),
             "--dry-run", "--variant", "t2=SECRET_PATTERNS:CREDENTIAL_PATTERNS")
    check("含 '..' 的 --source 被门禁拦下（exit 2）",
          r.returncode == 2, f"实际 {r.returncode}: {r.stderr[-160:]}")

    outside.unlink(missing_ok=True)


def test_variant_name_gating() -> None:
    """v1.0.7 P0：--variant 名字含 '..' / 非法字符必须被白名单拦下，且 workdir 外不新建目录。"""
    base = ["--source", "scan.py", "--tree", str(REPRO.parent), "--dry-run"]
    r = _run(BISECT, *base, "--variant", "../evil=SECRET_PATTERNS:CREDENTIAL_PATTERNS")
    check("含 '..' 的变体名被白名单拦下（exit 2）",
          r.returncode == 2, f"实际 {r.returncode}: {r.stderr[-160:]}")
    check("变体名拦截附修复建议", "how to fix" in r.stderr, r.stderr[-160:])
    # workdir/<name> 不应逃出 tree：若未被拦，--variant ../evil 会落到 tree/evil
    evil = REPRO.parent / "evil"
    check("workdir 外未新建目录（tree/evil 不存在）", not evil.exists())


def test_scripts_honor_lang() -> None:
    """A-4 (v1.0.7)：脚本尊重显式 --lang 选择，证明语言是用户可控的 opt-in（根因 A）。"""
    r_en = _run(SCAN, "--self-test", env={"TRIAGE_LANG": "en"})
    check("TRIAGE_LANG=en 时输出英文", "Self-test: all passed" in r_en.stdout,
          r_en.stdout[-160:])
    r_zh = _run(SCAN, "--self-test", env={"TRIAGE_LANG": "zh"})
    check("TRIAGE_LANG=zh 时输出中文", "自检: 全部通过" in r_zh.stdout,
          r_zh.stdout[-160:])


def test_codeql_download_doc_safety() -> None:
    """v1.0.8 T08 回归：下载段不得把镜像写成与官方等价的安全选项，必须强调校验。

    aig (ruleId T08) + clawscan (install_mechanism) 双双 concern 的根因是：文档把第三方
    镜像写成「更省事」且断言「换镜像不改变校验和」—— 这不成立（第三方镜像可能提供被替换的归档）。
    本测试守住整改后的形态：官方源为默认、镜像为不可信回退、强制 sha256 校验、删除错误断言。
    """
    doc = (ROOT / "references" / "running-codeql-cli.md").read_text(encoding="utf-8")

    check("下载段含官方源命令（--repo github/codeql-cli-binaries）",
          "gh release download" in doc
          and "--repo github/codeql-cli-binaries" in doc,
          "缺少官方 GitHub Release 下载命令")
    check("下载段含 sha256sum --check 强制校验",
          "sha256sum --check" in doc,
          "缺少 SHA-256 校验步骤")
    check("镜像被标注为不可信回退（untrusted fallback / 不可信回退）",
          "untrusted fallback" in doc or "不可信回退" in doc,
          "未把镜像标注为不可信回退")
    check("已删除'换镜像不改变校验和'类错误断言",
          "changes no checksum" not in doc
          and "不改变校验和" not in doc,
          "仍含'换镜像不改变校验和'错误断言")


TESTS = [test_prefilter_self_test, test_skill_frontmatter_is_plain_yaml,
         test_frontmatter_has_progressive_disclosure_fields,
         test_hard_constraints_are_marked_every_turn,
         test_single_run_flow_is_five_steps_with_fallbacks,
         test_progressive_disclosure_length_budget,
         test_both_language_files_mirror_frontmatter_fields,
         test_repro_has_one_source, test_fixed_is_clean,
         test_missing_path_returns_2,
         test_fixtures_differ_only_in_name, test_read_sarif_counts,
         test_read_sarif_extracts_source,
         test_sarif_structure_errors, test_variant_arg_validation,
         test_scan_jobs_and_summary,          test_path_gating, test_variant_name_gating,
         test_scripts_honor_lang, test_codeql_download_doc_safety]


def main() -> int:
    print("=" * 70)
    print("codeql-local-triage 自测")
    print("=" * 70)
    for t in TESTS:
        print(f"\n{t.__name__}")
        t()
    print("\n" + "=" * 70)
    if FAILS:
        print(f"❌ {len(FAILS)} 项失败: {', '.join(FAILS)}")
        return 1
    print("✅ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
