#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
commit_state.py — blooming-elf v4 状态写后「原子提交钩子」（多实例 + 加固版）

这是根治 v3「格式乱 / 日期不更新 / 记不住」的核心机制：
模型用 Write/Edit 改完 plants.json 后，必须调用本脚本一次完成
「校验 → 原子写盘 → 备份轮转 / 失败回滚」，不靠模型自觉逐项检查。

加固点（P1-6）：
    • 原子写盘：先写临时文件再 os.replace，杜绝半截文件
    • 备份轮转：保留最近 3 份（.bak / .bak.1 / .bak.2），可回溯
    • 无备份首跑：校验失败时保留坏文件为 .failed 供排查，不再静默丢失

用法：
    python3 commit_state.py <plants.json> [--keep N]

退出码：0 = 提交成功；1 = 校验失败已回滚；2 = 参数错误。
"""
import sys
import os
import json
import shutil

# 复用 validate_state 的校验逻辑（避免重复实现）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_state import validate_data, CATEGORY_ALIASES  # noqa: E402


def normalize(data):
    """提交前归一化：水养→水培；缺失 status 补「正常」。原地修改，返回是否改动。"""
    changed = False
    for inst in data.get("instances", []):
        for p in inst.get("plants", []):
            cat = p.get("category")
            if cat in CATEGORY_ALIASES and p.get("category") != CATEGORY_ALIASES[cat]:
                p["category"] = CATEGORY_ALIASES[cat]
                changed = True
            if not p.get("status"):
                p["status"] = "正常"
                changed = True
    return changed


def rotate_backup(bak, keep=3):
    """轮转备份：保留最近 keep 份（bak, bak.1, ..., bak.(keep-1)）。"""
    oldest = f"{bak}.{keep - 1}"
    if os.path.exists(oldest):
        os.remove(oldest)
    for k in range(keep - 2, 0, -1):
        src = f"{bak}.{k}"
        if os.path.exists(src):
            os.replace(src, f"{bak}.{k + 1}")
    if os.path.exists(bak):
        os.replace(bak, f"{bak}.1")


def count_plants(data, alive_only=False):
    total = 0
    for inst in data.get("instances", []):
        for p in inst.get("plants", []):
            if alive_only and p.get("status") == "已弃":
                continue
            total += 1
    return total


def main():
    if len(sys.argv) < 2:
        print("用法：python3 commit_state.py <plants.json> [--keep N]")
        sys.exit(2)

    path = sys.argv[1]
    keep = 3
    if "--keep" in sys.argv:
        idx = sys.argv.index("--keep")
        if idx + 1 < len(sys.argv):
            try:
                keep = max(1, int(sys.argv[idx + 1]))
            except ValueError:
                pass

    bak = path + ".bak"

    if not os.path.exists(path):
        print(f"❌ 状态文件不存在：{path}（先 Write 再 commit）")
        sys.exit(1)

    # 读入
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        if os.path.exists(bak):
            shutil.copyfile(bak, path)
            print(f"↩️ 已回滚到上一版备份：{bak}")
        else:
            shutil.copyfile(path, path + ".failed")
            print("⚠️ 无备份可回滚，坏文件已另存为 .failed 供排查")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取失败：{e}")
        sys.exit(1)

    # 归一化（水养→水培，补 status）
    normalize(data)

    # 校验
    ok, errors = validate_data(data)
    if not ok:
        print(f"❌ 校验失败，共 {len(errors)} 个错误（提交被阻断）：")
        for e in errors:
            print("  - " + e)
        if os.path.exists(bak):
            shutil.copyfile(bak, path)
            print(f"↩️ 已回滚到上一版备份：{bak}")
        else:
            shutil.copyfile(path, path + ".failed")
            print("⚠️ 无备份可回滚，坏文件已另存为 .failed 供排查")
        sys.exit(1)

    # 校验通过 → 原子写盘（规范化 JSON，消除格式漂移）
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)  # 原子替换，无半截文件
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        print(f"❌ 写盘失败：{e}")
        sys.exit(1)

    # 备份轮转 + 刷新最新备份
    rotate_backup(bak, keep)
    shutil.copyfile(path, bak)
    total = count_plants(data)
    alive = count_plants(data, alive_only=True)
    n_inst = len(data.get("instances", [])) if "instances" in data else 1
    discarded = total - alive
    msg = f"✅ 提交成功：{n_inst} 个实例，{alive} 盆存活"
    if discarded:
        msg += f"（{discarded} 盆已弃不计）"
    msg += f"，状态健康，已备份至 {bak}（保留最近 {keep} 份）"
    print(msg)
    sys.exit(0)


if __name__ == "__main__":
    main()
