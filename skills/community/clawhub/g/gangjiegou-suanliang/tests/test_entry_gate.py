#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s9 入口闸门测试：退出码 20/21/22/23/24 + 五技能真实 --check-deps。

运行：
    PY=~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
    $PY tests/test_entry_gate.py

全部使用合成 fixture 与临时沙箱（CODEX_SKILLS_ROOT），不碰真实图纸，也不删改本机技能。
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
ROOT = SKILLS / "gangjiegou-suanliang"
GATE_PATH = ROOT / "scripts" / "entry_gate.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# entry_gate 通过同目录 contract_guard 做契约校验；importlib 载入不会自动
# 把 scripts/ 放入 sys.path，因此必须显式加入，否则测试会误报为 22。
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("vendored_entry_gate", GATE_PATH)
eg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eg)

RESULTS = []

# 入口脚本只存文件名，路径在 run_skill 里拼 scripts/ 目录：
# 本文件的文本会被发布扫描当作 scripts/<name>.py 依赖引用，写全路径会误报缺失。
SKILL_ENTRIES = {
    "gangjiegou": ("gangjiegou-suanliang", "steel_tonnage.py"),
    "tujian": ("tujian-suanliang", "qty_core.py"),
    "anzhuang": ("anzhuang-suanliang", "mep_scan.py"),
    "yuanlin": ("yuanlin-suanliang", "yuanlin_qty.py"),
    "zhuangshi": ("zhuangshi-suanliang", "decor_qty.py"),
}


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if detail:
        print("      " + detail.replace("\n", "\n      ")[:1200])


def expect_gate(name, fn, want_code):
    try:
        fn()
    except eg.GateError as exc:
        check(name, exc.code == want_code,
              "code=%d（期望 %d）message=%s" % (exc.code, want_code, exc.message))
        return
    except Exception as exc:  # noqa: BLE001
        check(name, False, "%s: %s" % (type(exc).__name__, exc))
        return
    check(name, False, "未抛 GateError（期望 code=%d）" % want_code)


def make_sandbox(base: Path, *, reader: bool, bus: bool) -> Path:
    root = base / ("sandbox_r%d_b%d" % (int(reader), int(bus)))
    root.mkdir(parents=True, exist_ok=True)
    for slug, enabled, version in (
        ("cad-file-reader", reader, "0.41.0"),
        ("lis-skill-bus", bus, "0.1.11"),
    ):
        if not enabled:
            continue
        d = root / slug
        (d / "scripts").mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text("# %s\n" % slug, encoding="utf-8")
        (d / "manifest.json").write_text(
            json.dumps({"name": slug, "version": version}), encoding="utf-8")
    return root


def clean_env(extra=None):
    env = os.environ.copy()
    for key in ("CAD_FILE_READER_HOME", "CAD_SKILL_DIR", "SKILLBUS_HOME",
                "CAD_DEV_DXF", "CAD_ALLOW_DIRECT"):
        env.pop(key, None)
    env.update(extra or {})
    return env


def run_skill(slug: str, entry: str, args, env):
    return subprocess.run(
        [sys.executable, str(SKILLS / slug / "scripts" / entry)] + [str(a) for a in args],
        capture_output=True, text=True, env=env, cwd=str(SKILLS / slug))


def write_bus_state(state_dir: Path):
    reader = json.loads((FIXTURES / "reader_contract.json").read_text(encoding="utf-8"))
    reader["_id"] = "s2-reader-0001"
    v0 = json.loads((FIXTURES / "contract_v0.json").read_text(encoding="utf-8"))
    v0["_id"] = "s2-v0-0001"
    state = {
        "state_version": 1,
        "projects": {"s2-test": {"s2-reader-0001": reader, "s2-v0-0001": v0}},
    }
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="s9_entry_gate_"))
    empty = tmp / "empty"
    empty.mkdir()
    reader_only = make_sandbox(tmp, reader=True, bus=False)
    both = make_sandbox(tmp, reader=True, bus=True)

    # ---------------------------------------------------------------- 20 / 21
    old_root = os.environ.get("CODEX_SKILLS_ROOT")
    try:
        os.environ["CODEX_SKILLS_ROOT"] = str(empty)
        expect_gate("1 空沙箱 require_reader -> 20",
                    eg.require_reader, 20)
        os.environ["CODEX_SKILLS_ROOT"] = str(reader_only)
        expect_gate("2 只有 reader 时 require_bus -> 21",
                    eg.require_bus, 21)
        got = eg.require_reader()
        check("3 只有 reader 时 require_reader 通过", got.get("version") == "0.41.0",
              "version=%s" % got.get("version"))
        os.environ["CODEX_SKILLS_ROOT"] = str(both)
        got = eg.require_bus()
        check("4 reader+bus 就绪 require_bus 通过", got.get("version") == "0.1.11",
              "version=%s" % got.get("version"))
    finally:
        if old_root is None:
            os.environ.pop("CODEX_SKILLS_ROOT", None)
        else:
            os.environ["CODEX_SKILLS_ROOT"] = old_root

    # 五技能真实 subprocess：空沙箱 20，只有 reader 21
    for label, root, want in (("20", empty, 20), ("21", reader_only, 21)):
        env = clean_env({"CODEX_SKILLS_ROOT": str(root)})
        for name, (slug, entry) in SKILL_ENTRIES.items():
            r = run_skill(slug, entry, ["--check-deps"], env)
            check("5.%s %s --check-deps 缺依赖 -> %s" % (label, name, want),
                  r.returncode == want,
                  "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()))

    # ------------------------------------------------------------------- 23
    for suffix in (".dwg", ".dxf", ".dwt", ".DWG"):
        expect_gate("6 reject_drawing_input %s -> 23" % suffix,
                    lambda s=suffix: eg.reject_drawing_input("plan" + s), 23)

    env_both = clean_env({"CODEX_SKILLS_ROOT": str(both)})
    drawing_cases = [
        ("gangjiegou", ["--steel", "plan.dxf", "--out-prefix", str(tmp / "g")]),
        ("tujian", ["index", "plan.dwg"]),
        ("anzhuang", ["plan.dwg", "--out", str(tmp / "a.json")]),
        ("yuanlin", ["--dxf-block-refs", "plan.dxf", "--out-dir", str(tmp / "y")]),
        ("zhuangshi", ["--input", "plan.dwg", "--out-dir", str(tmp / "z")]),
    ]
    for name, args in drawing_cases:
        slug, entry = SKILL_ENTRIES[name]
        r = run_skill(slug, entry, args, env_both)
        check("7 %s 真实入口传图纸 -> 23" % name, r.returncode == 23,
              "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:600]))

    # ------------------------------------------------------------ 22 / 24
    reader_contract = FIXTURES / "reader_contract.json"
    try:
        guard = eg.require_contract(reader_contract)
        check("8 正常 cad-contract/v1 可过 require_contract",
              guard.get("mode") == "formal" and bool(guard.get("contract_id")),
              "mode=%s contract_id=%s" % (guard.get("mode"), guard.get("contract_id")))
    except Exception as exc:  # noqa: BLE001
        check("8 正常 cad-contract/v1 可过 require_contract", False,
              "%s: %s" % (type(exc).__name__, exc))

    expect_gate("9 契约版本 v0（guard 4）-> 22",
                lambda: eg.require_contract(FIXTURES / "contract_v0.json"), 22)

    missing_key = tmp / "missing_key.json"
    missing_key.write_text(
        json.dumps(json.loads(reader_contract.read_text(encoding="utf-8"))),
        encoding="utf-8")
    expect_gate("10 缺必需顶层键（guard 2）-> 22",
                lambda: eg.require_contract(missing_key, required_keys=("sections",)), 22)

    manual = tmp / "manual_contract.json"
    manual.write_text(json.dumps({
        "schema": "cad-contract/v1",
        "provenance": "manual",
        "coordinate_unit": "mm",
        "contract": {"schema": "cad-steel-geometry/v1"},
    }, ensure_ascii=False), encoding="utf-8")
    expect_gate("11 手工来源未授权（guard 3）-> 22",
                lambda: eg.require_contract(manual), 22)
    expect_gate("12 手工来源要求正式量 -> 24",
                lambda: eg.require_contract(manual, allow_manual=True,
                                            require_formal=True), 24)
    expect_gate("13 evidence_ok=False -> 24",
                lambda: eg.require_contract(reader_contract, evidence_ok=False), 24)

    # ------------------------------------------- 装饰表格输入（不经 CAD 识图）
    csv_path = tmp / "decor_input.csv"
    csv_path.write_text(
        "楼层,区域,房间,部位类型,做法编号,做法名称,做法类型,依据,间数,长_m,宽_m\n"
        "二层,A区,办公室,地面/楼面,D01,地砖楼面,通用,建施-05,1,6,4.5\n",
        encoding="utf-8-sig")
    out_dir = tmp / "decor_out"
    r = run_skill("zhuangshi-suanliang", "decor_qty.py",
                  ["--input", csv_path, "--out-dir", out_dir, "--allow-manual"],
                  clean_env())
    ok = r.returncode == 0 and (out_dir / "provenance.json").exists()
    detail = "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[-800:])
    if ok:
        prov = json.loads((out_dir / "provenance.json").read_text(encoding="utf-8"))
        report = (out_dir / "装饰概算物资计划报告.md").read_text(encoding="utf-8")
        ok = (prov.get("input_channel") == "table"
              and prov.get("final_quantity") is False
              and "表格输入（不经 CAD 识图）" in report)
        detail += "\ninput_channel=%s final_quantity=%s" % (
            prov.get("input_channel"), prov.get("final_quantity"))
    check("14 装饰表格输入 exit 0 且 input_channel=table", ok, detail)

    # ------------------------------------------------- 钢构 from-contract 旧链路
    bus_dir = tmp / "bus_state"
    write_bus_state(bus_dir)
    env_bus = clean_env({"SKILLBUS_STATE_DIR": str(bus_dir)})
    script = SKILLS / "gangjiegou-suanliang" / "scripts" / "steel_tonnage.py"

    def run_steel(args):
        return subprocess.run([sys.executable, str(script)] + [str(a) for a in args],
                              capture_output=True, text=True, env=env_bus)

    p2 = tmp / "t2"
    r = run_steel(["--steel", FIXTURES / "manual_steel.json", "--out-prefix", p2])
    check("15 手工 steel 无 --allow-manual -> 3", r.returncode == 3,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()))

    p3 = tmp / "t3"
    r = run_steel(["--steel", FIXTURES / "manual_steel.json", "--allow-manual",
                   "--out-prefix", p3])
    ok = r.returncode == 0
    detail = "exit=%d" % r.returncode
    if ok:
        data = json.loads(Path(str(p3) + ".json").read_text(encoding="utf-8"))
        ok = (data.get("provenance") == "manual"
              and data.get("formal_ledger_eligible") is False
              and data.get("final_quantity") is False)
        detail += "\nprovenance=%s formal=%s final_quantity=%s" % (
            data.get("provenance"), data.get("formal_ledger_eligible"),
            data.get("final_quantity"))
    else:
        detail += "\n%s" % (r.stdout + r.stderr).strip()
    check("16 手工 steel --allow-manual -> 0 且非正式量", ok, detail)

    p5 = tmp / "t5"
    r = run_steel(["--from-contract", "no-such-id", "--project", "s2-test",
                   "--out-prefix", p5])
    text5 = r.stdout + r.stderr
    check("17 --from-contract 不存在 -> 1 且含拉取/安装提示",
          r.returncode == 1 and "拉取命令" in text5 and "安装 bus" in text5,
          "exit=%d\n%s" % (r.returncode, text5.strip()))

    p6 = tmp / "t6"
    r = run_steel(["--from-contract", "s2-v0-0001", "--project", "s2-test",
                   "--out-prefix", p6])
    check("18 契约版本 cad-contract/v0 -> 4", r.returncode == 4,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()))

    p7 = tmp / "t7"
    r = run_steel(["--from-contract", "s2-reader-0001", "--project", "s2-test",
                   "--out-prefix", p7])
    ok = r.returncode == 0
    detail = "exit=%d" % r.returncode
    if ok:
        data = json.loads(Path(str(p7) + ".json").read_text(encoding="utf-8"))
        ok = (data.get("provenance") == "reader"
              and bool(data.get("contract_id"))
              and data.get("formal_ledger_eligible") is True
              and data.get("final_quantity") is False)
        detail += "\nprovenance=%s contract_id=%s formal=%s final_quantity=%s" % (
            data.get("provenance"), data.get("contract_id"),
            data.get("formal_ledger_eligible"), data.get("final_quantity"))
    else:
        detail += "\n%s" % (r.stdout + r.stderr).strip()
    check("19 reader 契约 -> 0 且 provenance=reader", ok, detail)

    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    print("\nentry_gate: %d/%d PASS" % (passed, len(RESULTS)))
    print("tmp=%s" % tmp)
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
