#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
e2e_check.py — blooming-elf v4 端到端流程验证（授权机制示范）

设计要点（对应授权机制）：
    • 默认无参：用 tests/fixtures/demo.json（合成假数据，可随包发布）跑闭环。
    • --data <真实plants.json>：要求同目录有 .auth（用户明示授权）；
      把真实数据**复制**到临时文件，仅在副本上模拟全流程，**源文件零改动**。
    • 拒绝 data 路径落在 skill 目录内（防误把真实数据塞进发布包）。
    • 内置失败用例：构造 next<last → 断言 commit_state 回滚 + 退出码 1。

退出码：0 = 全部通过；1 = 有断言失败。
"""
import sys
import os
import json
import shutil
import subprocess
import tempfile
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
DEMO = os.path.join(HERE, "fixtures", "demo.json")
PY = sys.executable


def run_commit(target):
    """调用 commit_state.py，返回 (exit_code, stdout)。"""
    r = subprocess.run(
        [PY, os.path.join(SCRIPTS, "commit_state.py"), target],
        capture_output=True, text=True,
    )
    return r.returncode, (r.stdout + r.stderr).strip()


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def all_plants(data):
    if "instances" in data:
        for inst in data["instances"]:
            for p in inst.get("plants", []):
                yield inst.get("elf", "?"), p
    else:
        for p in data.get("plants", []):
            yield "?", p


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="真实 plants.json 路径（需同目录 .auth 授权）")
    ap.add_argument("--auth", help="授权记录路径（默认 <data>.auth）")
    ap.add_argument("--today", help="模拟今日日期 YYYY-MM-DD（默认实际今天）")
    ap.add_argument("--keep", type=int, default=3)
    args = ap.parse_args()

    # 解析目标文件
    if args.data:
        data_path = os.path.abspath(args.data)
        # 防越权：真实数据不能在 skill 目录内
        if os.path.commonpath([data_path, SKILL_DIR]) == SKILL_DIR:
            print("❌ 安全拦截：data 路径落在 skill 目录内，禁止（真实数据不可进发布包）")
            sys.exit(1)
        auth_path = os.path.abspath(args.auth) if args.auth else data_path + ".auth"
        if not os.path.exists(auth_path):
            print(f"❌ 未找到授权记录 {auth_path}：请先显式授权（写 .auth）再验证")
            sys.exit(1)
        with open(auth_path, encoding="utf-8") as f:
            auth = json.load(f)
        print(f"🔓 已读取授权：owner={auth.get('owner')} granted_by={auth.get('granted_by')}")
        # 复制到临时副本（源不动）
        tmpdir = tempfile.mkdtemp(prefix="blooming_e2e_")
        target = os.path.join(tmpdir, "plants.copy.json")
        shutil.copyfile(data_path, target)
        source_hash = _sha(data_path)
    else:
        target = DEMO
        tmpdir = None
        print("ℹ️ 未指定 --data，使用合成 demo 夹具（无真实数据）")

    today = date.fromisoformat(args.today) if args.today else date.today()
    today_s = today.isoformat()
    print(f"🗓️ 模拟今日：{today_s}\n")

    fails = []

    # ---- 场景 1：查今日该浇 + 模拟浇水 + 提交 ----
    data = load(target)
    due = [(elf, p) for elf, p in all_plants(data)
           if p.get("next_water") and p["next_water"] <= today_s
           and p.get("status") != "已弃"]  # 已弃盆不提醒
    # 断言：所有 已弃 盆都不应出现在提醒清单（due 已按 status 过滤）
    due_names = {(elf, p["name"]) for elf, p in due}
    for elf, p in all_plants(data):
        if p.get("status") == "已弃" and (elf, p["name"]) in due_names:
            fails.append(f"场景1：已弃盆不应出现在提醒清单，却出现 {(elf, p['name'])}")
    # 选一盆操作：优先今日该浇，否则取第一盆（不含已弃）
    op_elf, op_plant = (due[0] if due else next(
        (e, p) for e, p in all_plants(data) if p.get("status") != "已弃"))
    print(f"▶ 场景1：对 [{op_elf}] {op_plant['name']} 模拟浇水")
    old_next = op_plant.get("next_water")
    interval = int(op_plant.get("water_interval_max", 4))
    new_last = today_s
    new_next = (today + timedelta(days=interval)).isoformat()
    # 在副本上更新
    _patch(target, op_elf, op_plant["key"], new_last, new_next)
    code, out = run_commit(target)
    print("   " + out.replace("\n", "\n   "))
    if code != 0:
        fails.append("场景1：提交未通过（exit!=0）")
    else:
        d2 = load(target)
        np_ = _find(d2, op_elf, op_plant["key"])
        if np_["last_water"] != new_last:
            fails.append(f"场景1：last_water 未更新为 {new_last}")
        if np_["next_water"] != new_next:
            fails.append(f"场景1：next_water 未更新为 {new_next}")
        if np_["next_water"] < np_["last_water"]:
            fails.append("场景1：日期倒挂")
        if not os.path.exists(target + ".bak"):
            fails.append("场景1：未生成备份")
    print()

    # ---- 场景 2：失败用例（next<last）→ 应回滚 ----
    print("▶ 场景2：构造 next<last 错误，断言回滚")
    _patch(target, op_elf, op_plant["key"], new_next, new_last)  # 故意倒挂
    code2, out2 = run_commit(target)
    print("   " + out2.replace("\n", "\n   "))
    if code2 != 1:
        fails.append(f"场景2：错误数据应退出码1，实际 {code2}")
    else:
        d3 = load(target)
        np3 = _find(d3, op_elf, op_plant["key"])
        if np3["next_water"] != new_next:  # 应已回滚到场景1提交的正确值
            fails.append("场景2：未回滚到上一版正确状态")
    print()

    # ---- 源文件完整性（仅真实数据场景） ----
    if args.data:
        if _sha(data_path) != source_hash:
            fails.append("源文件被修改（授权机制失效）")
        else:
            print("✅ 源真实数据未被改动（临时副本隔离验证）")
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)

    # ---- 结果 ----
    print("=" * 50)
    if fails:
        print(f"❌ E2E 失败，{len(fails)} 项：")
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print("✅ E2E 全部通过：建档→查今日该浇→浇水→更新 next_water→校验→备份/回滚 闭环正常")
    sys.exit(0)


def _sha(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _patch(target, elf, key, new_last, new_next):
    d = load(target)
    p = _find(d, elf, key)
    p["last_water"] = new_last
    p["next_water"] = new_next
    with open(target, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def _find(data, elf, key):
    if "instances" in data:
        for inst in data["instances"]:
            if inst.get("elf") == elf:
                for p in inst.get("plants", []):
                    if p.get("key") == key:
                        return p
    else:
        for p in data.get("plants", []):
            if p.get("key") == key:
                return p
    raise KeyError(f"plant {elf}/{key} not found")


if __name__ == "__main__":
    main()
