#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_state.py — blooming-elf v4 状态文件写后校验（多实例版）

用法：
    python3 validate_state.py <状态文件路径/plants.json>

校验项（根治 v3「格式乱 / 日期不更新 / 记不住」）：
    1. JSON 可解析
    2. 顶层含 instances[]（或兼容旧版单实例 plants[]）
    3. 每实例内每盆 key 唯一
    4. category 合法（土培/吸水盆/水培/鲜切花）
    5. 必填字段完整（key/name/category）
    6. 日期字段为 ISO YYYY-MM-DD
    7. next_water >= last_water

退出码：0 = 通过，1 = 有错误，2 = 参数错误。
"""
import sys
import json
import re

VALID_CATEGORIES = {"土培", "吸水盆", "水培", "鲜切花", "水养"}
# 水养 是 水培 的同义写法（用户档案常用「水养」），校验同时接受，提交时归一为 水培
CATEGORY_ALIASES = {"水养": "水培"}
VALID_STATUS = {"正常", "休眠", "停水观察", "已弃"}
REQUIRED_FIELDS = ["key", "name", "category"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_date(s):
    from datetime import date
    return date.fromisoformat(s)


def _validate_plants(plants, tag_prefix, errors):
    """校验一个 plants 数组，错误写入 errors。返回 None。"""
    if not isinstance(plants, list):
        errors.append(f"{tag_prefix}: 'plants' 必须是数组")
        return
    seen_keys = {}
    for i, p in enumerate(plants):
        tag = f"{tag_prefix}plants[{i}]"
        if not isinstance(p, dict):
            errors.append(f"{tag}: 必须是对象")
            continue
        for field in REQUIRED_FIELDS:
            val = p.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(f"{tag}: 缺少必填字段 '{field}'")
        key = p.get("key")
        if key:
            if key in seen_keys:
                errors.append(f"{tag}: key 重复 '{key}'（首次见于 {tag_prefix}plants[{seen_keys[key]}]）")
            else:
                seen_keys[key] = i
        cat = p.get("category")
        if cat and cat not in VALID_CATEGORIES:
            errors.append(f"{tag}: category 非法 '{cat}'（合法：{sorted(VALID_CATEGORIES)}；水养=水培同义）")
        st = p.get("status")
        if st and st not in VALID_STATUS:
            errors.append(f"{tag}: status 非法 '{st}'（合法：{sorted(VALID_STATUS)}）")
        lw = p.get("last_water")
        nw = p.get("next_water")
        for df, dv in (("last_water", lw), ("next_water", nw)):
            if dv and not DATE_RE.match(str(dv)):
                errors.append(f"{tag}: {df} 非 ISO 格式 '{dv}'（需 YYYY-MM-DD）")
        if lw and nw and DATE_RE.match(str(lw)) and DATE_RE.match(str(nw)):
            try:
                if parse_date(str(nw)) < parse_date(str(lw)):
                    errors.append(f"{tag}: next_water({nw}) < last_water({lw})，日期倒挂")
            except ValueError:
                pass  # 格式错误已在上面记录


def validate_data(data):
    """校验状态数据，返回 (是否通过, 错误列表)。供 CLI 与 commit_state.py 复用。"""
    errors = []
    if not isinstance(data, dict):
        return False, ["顶层必须是 JSON 对象"]

    instances = data.get("instances")
    legacy_plants = data.get("plants")

    if instances is not None:
        if not isinstance(instances, list) or not instances:
            errors.append("顶层 'instances' 必须是非空数组")
            return (len(errors) == 0), errors
        for i, inst in enumerate(instances):
            itag = f"instances[{i}]"
            if not isinstance(inst, dict):
                errors.append(f"{itag}: 必须是对象")
                continue
            if not inst.get("elf"):
                errors.append(f"{itag}: 缺少 'elf'（精灵名）")
            _validate_plants(inst.get("plants", []), itag + ".", errors)
        return (len(errors) == 0), errors

    if legacy_plants is not None:
        # 向后兼容：单实例归一
        _validate_plants(legacy_plants, "", errors)
        return (len(errors) == 0), errors

    errors.append("顶层缺少 'instances' 或 'plants'")
    return False, errors


def main():
    if len(sys.argv) < 2:
        print("用法：python3 validate_state.py <plants.json>")
        sys.exit(2)

    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        _report([f"文件不存在：{path}"])
    except json.JSONDecodeError as e:
        _report([f"JSON 解析失败：{e}"])

    ok, errors = validate_data(data)
    if ok:
        # 统计总盆数
        total = 0
        for inst in data.get("instances", []):
            total += len(inst.get("plants", []))
        _report([], total=total)
    _report(errors)


def _report(errors, total=None):
    if errors:
        print(f"❌ 校验失败，共 {len(errors)} 个错误：")
        for e in errors:
            print("  - " + e)
        sys.exit(1)
    msg = "✅ 校验通过"
    if total is not None:
        msg += f"：{total} 盆植物，状态文件健康"
    print(msg)
    sys.exit(0)


if __name__ == "__main__":
    main()
