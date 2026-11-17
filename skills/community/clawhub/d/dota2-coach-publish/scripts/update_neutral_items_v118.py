#!/usr/bin/env python3
"""
v1.1.8 中性物品本体更新脚本（7.41d 版本）
- heavy_blade：cd 40→30 + 追加 patch_changes
- foragers_kit / conjurers_catalyst / enchanters_bauble：加 patch_changes 记录 + 补 localized_name（用户给的中文名）
- 附魔（贪婪/狂热）：跳过，description 为空，无响应字段
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NEUTRAL_FILE = f'{SCRIPT_DIR}/neutral_items.json'
BACKUP_FILE = f'{SCRIPT_DIR}/../backup_v118_20260731/neutral_items.json'

# === 补丁定义 ===
# heavy_blade.cd 当前是 int 类型
heavy_blade_cd_old = 40
heavy_blade_cd_new = 30

patches_to_add = {
    "foragers_kit": [
        {
            "patch": "7.41d",
            "date": "2026-07-31",
            "field": "harvest_time",
            "old": "1",
            "new": "0.75",
            "description": "采菌时间 1s→0.75s"
        }
    ],
    "conjurers_catalyst": [
        {
            "patch": "7.41d",
            "date": "2026-07-31",
            "field": "spell_overflow_nonhero_damage",
            "old": "30",
            "new": "20",
            "description": "法术外溢对非英雄单位的爆炸伤害 30→20"
        },
        {
            "patch": "7.41d",
            "date": "2026-07-31",
            "field": "spell_overflow_illusion_threshold",
            "old": "consider_all_damage",
            "new": "only_pre_increased_damage",
            "description": "法术外溢对幻象的伤害临界值现在只考虑增伤前伤害"
        }
    ],
    "enchanters_bauble": [
        {
            "patch": "7.41d",
            "date": "2026-07-31",
            "field": "reforge_bonus",
            "old": "40",
            "new": "35",
            "description": "附魔的重新打造加成 40%→35%"
        }
    ],
    "heavy_blade": [
        {
            "patch": "7.41d",
            "date": "2026-07-31",
            "field": "cd",
            "old": "40",
            "new": "30",
            "description": "清洗 CD 40s→30s"
        }
    ],
}

localized_names = {
    "foragers_kit": "采菌套具",
    "conjurers_catalyst": "咒术师触媒",
    "enchanters_bauble": "附魔师之椟",
}

# 跳过的项
skipped = [
    {"key": "item_enhancement_greedy", "cn": "贪婪", "reason": "description 为空，items_db.json 无 patch_changes 字段"},
    {"key": "item_enhancement_feverish", "cn": "狂热", "reason": "description 为空，items_db.json 无 patch_changes 字段"},
]

def main():
    # ---- 备份 ----
    backup_dir = os.path.dirname(BACKUP_FILE)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    if not os.path.exists(BACKUP_FILE):
        import shutil
        shutil.copy2(NEUTRAL_FILE, BACKUP_FILE)
        print(f'已备份: {BACKUP_FILE}')
    else:
        print(f'备份已存在: {BACKUP_FILE}')

    # ---- 加载 ----
    with open(NEUTRAL_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 把所有 tier 展平成 (tier_key, item) 列表
    all_items = []
    for tier_key, items in data.items():
        for it in items:
            all_items.append((tier_key, it))
    items_by_key = {it['key']: (tier, it) for (tier, it) in all_items}

    applied, failed = [], []

    # ---- A. heavy_blade: cd 字段 + patch_changes ----
    if 'heavy_blade' in items_by_key:
        tier, hb = items_by_key['heavy_blade']
        cur_cd = hb.get('cd')
        # 类型兼容比较
        if cur_cd == heavy_blade_cd_old or str(cur_cd) == str(heavy_blade_cd_old):
            hb['cd'] = heavy_blade_cd_new
            applied.append(f'heavy_blade.cd: {cur_cd} → {heavy_blade_cd_new}')
        else:
            failed.append(f'heavy_blade.cd: 当前={cur_cd} ({type(cur_cd).__name__}), 期望={heavy_blade_cd_old}')
            return  # 字段不一致就不继续 patch_changes，避免记录与实际不符
        hb.setdefault('patch_changes', []).extend(patches_to_add['heavy_blade'])
        hb['last_updated'] = '2026-07-31'
        applied.append(f'heavy_blade: 追加 patch_changes 1 条 + last_updated 更新')

    # ---- B. 其他 3 个：patch_changes + localized_name ----
    for k in ['foragers_kit', 'conjurers_catalyst', 'enchanters_bauble']:
        if k not in items_by_key:
            failed.append(f'{k}: 未找到')
            continue
        tier, it = items_by_key[k]
        it.setdefault('patch_changes', []).extend(patches_to_add[k])
        applied.append(f'{k}: 追加 patch_changes {len(patches_to_add[k])} 条')
        if not it.get('localized_name'):
            it['localized_name'] = localized_names[k]
            applied.append(f'{k}: 补 localized_name="{localized_names[k]}"')
        else:
            applied.append(f'{k}: localized_name 已有 "{it["localized_name"]}"，未动')

    # ---- 写回 ----
    with open(NEUTRAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # ---- 输出 ----
    print(f'\n=== 成功: {len(applied)} / 失败: {len(failed)} ===')
    for line in applied:
        print(f'  ✅ {line}')
    if failed:
        print('\n=== 失败 ===')
        for line in failed:
            print(f'  ❌ {line}')

    print(f'\n=== 跳过（无响应字段）: {len(skipped)} 项 ===')
    for s in skipped:
        print(f'  ⏭  {s["key"]} ({s["cn"]}): {s["reason"]}')

if __name__ == '__main__':
    main()