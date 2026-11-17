#!/usr/bin/env python3
"""
v1.1.8 物品数据更新脚本（7.41d 版本）
按用户给出的物品变更清单更新 items_db.json：
- 结构化字段（cost/cooldown/mana_cost）：直接修改
- description 里的精确数值：替换
- 语义/机制变更：在 description 末尾追加 Note
- 基础属性（如 +30 力量）：当前数据模型无 attributes 字段，跳过

备份：items_db.json → backup_v118_20260731/items_db.json
"""
import json
import os
import sys
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = f'{SCRIPT_DIR}/items_db.json'
BACKUP_FILE = f'{SCRIPT_DIR}/../backup_v118_20260731/items_db.json'

# === Patch 列表 ===
patches = [
    # ---- A. 结构化字段 ----
    {"key": "item_chasm_stone",         "type": "field",        "field": "cost",      "old": 800,  "new": 900},
    {"key": "item_recipe_shivas_guard", "type": "field",        "field": "cost",      "old": 1350, "new": 1250},
    {"key": "item_recipe_gungir",       "type": "field",        "field": "cost",      "old": 400,  "new": 300},
    {"key": "item_heavens_halberd",     "type": "field",        "field": "cooldown",  "old": "16", "new": "15"},
    {"key": "item_satanic",             "type": "field",        "field": "cooldown",  "old": "30", "new": "40"},
    {"key": "item_veil_of_discord",     "type": "field",        "field": "mana_cost", "old": "50", "new": "25"},

    # ---- B. description 精确替换 ----
    {"key": "item_crellas_crozier",     "type": "desc_replace", "find": "Movement speed steal lasts **1.5**s.",                                                                                                                                                     "replace": "Movement speed steal lasts **2**s."},
    {"key": "item_crellas_crozier",     "type": "desc_replace", "find": "Putrefaction Aura's effect is increased to **75%**.",                                                                                                                                   "replace": "Putrefaction Aura's effect is increased to **90%**."},
    {"key": "item_skadi",               "type": "desc_replace", "find": "Attacks also lower enemy attack speed by **-20%**",                                                                                                                                       "replace": "Attacks also lower enemy attack speed by **-25%**"},
    {"key": "item_hurricane_pike",      "type": "desc_replace", "find": "and for **6** seconds, allows you to make **5** attacks",                                                                                                                                  "replace": "and for **5** seconds, allows you to make **5** attacks"},
    {"key": "item_mask_of_madness",     "type": "desc_replace", "find": "**8%** / **12%** movement speed (ranged/melee), and **30%** slow resistance",                                                                                                              "replace": "**6%** / **12%** movement speed (ranged/melee), and **15%** / **30%** slow resistance (ranged/melee)"},
    {"key": "item_orb_of_frost",        "type": "desc_replace", "find": "reduces Health Restoration by **13%**",                                                                                                                                                   "replace": "reduces Health Restoration by **15%**"},
    {"key": "item_orb_of_corrosion",    "type": "desc_replace", "find": "reduces Health Restoration by **16%**",                                                                                                                                                   "replace": "reduces Health Restoration by **18%**"},
    {"key": "item_orb_of_venom",        "type": "desc_replace", "find": "Poisons the target, dealing **10** magical damage per second.",                                                                                                                            "replace": "Poisons the target, dealing **12** magical damage per second."},

    # ---- C. description 末尾追加 Note ----
    {"key": "item_rapier",              "type": "desc_append",  "append": "\n\n# Update (7.41d)\nMultiple Rapiers no longer stack their ability enhancements."},
    {"key": "item_smoke_of_deceit",     "type": "desc_append",  "append": "\n\n# Update (7.41d)\nDisguise duration is now fixed and not affected by duration-increasing effects."},
    {"key": "item_urn_of_shadows",      "type": "desc_append",  "append": "\n\n# Update (7.41d)\nDoes not gain charges from nearby hero deaths while in the Stash."},
    {"key": "item_essence_distiller",   "type": "desc_append",  "append": "\n\n# Update (7.41d)\nDoes not gain charges from nearby hero deaths while in the Stash."},
    {"key": "item_spirit_vessel",       "type": "desc_append",  "append": "\n\n# Update (7.41d)\nDoes not gain charges from nearby hero deaths while in the Stash."},
    {"key": "item_orb_of_frost",        "type": "desc_append",  "append": "\n\n# Update (7.41d)\nFrost no longer applies when attacking allied units."},
]

# === 跳过但需要告知用户的：基础属性变更（无 attributes 字段） ===
skipped_attribute_changes = [
    {"item": "深渊之刃 item_abyssal_blade",   "change": "力量加成 +26 → +30"},
    {"item": "蝴蝶 item_butterfly",           "change": "敏捷加成 +35 → +30；攻击力加成 +25 → +30"},
    {"item": "慧光 item_kaya",                "change": "魔法恢复增强 30% → 20%"},
    {"item": "陨星锤 item_meteor_hammer",     "change": "魔法恢复增强 35% → 25%"},
    {"item": "散慧对剑 item_kaya_and_sange",  "change": "魔法恢复增强 40% → 30%"},
    {"item": "慧夜对剑 item_yasha_and_kaya",  "change": "魔法恢复增强 40% → 30%"},
    {"item": "迈达斯之手 item_hand_of_midas", "change": "攻击速度加成 +35 → +40"},
    {"item": "影之灵龛 item_urn_of_shadows",   "change": "魔法恢复加成 +1.25 → +1"},
]

def main():
    # ---- 备份 ----
    backup_dir = os.path.dirname(BACKUP_FILE)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(ITEMS_FILE, BACKUP_FILE)
        print(f'已备份: {BACKUP_FILE}')
    else:
        print(f'备份已存在: {BACKUP_FILE}')

    # ---- 加载 ----
    with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
        items = json.load(f)
    items_by_key = {it['key']: it for it in items}

    applied, failed = [], []

    for p in patches:
        k = p['key']
        if k not in items_by_key:
            failed.append((p, 'item not found'))
            continue
        item = items_by_key[k]

        if p['type'] == 'field':
            if item.get(p['field']) != p['old']:
                failed.append((p, f"current {p['field']}={item.get(p['field'])}, expected {p['old']}"))
                continue
            item[p['field']] = p['new']
            applied.append(p)

        elif p['type'] == 'desc_replace':
            desc = item.get('description', '') or ''
            cnt = desc.count(p['find'])
            if cnt != 1:
                failed.append((p, f'find count = {cnt}, expected 1'))
                continue
            item['description'] = desc.replace(p['find'], p['replace'])
            applied.append(p)

        elif p['type'] == 'desc_append':
            desc = item.get('description', '') or ''
            item['description'] = desc + p['append']
            applied.append(p)

    # ---- 写回 ----
    if applied:
        with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    # ---- 输出 ----
    print(f'\n=== 成功应用: {len(applied)} / 失败: {len(failed)} ===\n')
    for p in applied:
        if p['type'] == 'field':
            print(f'  ✅ {p["key"]}.{p["field"]}: {p["old"]} → {p["new"]}')
        elif p['type'] == 'desc_replace':
            print(f'  ✅ {p["key"]}: desc 替换 "{p["find"][:55]}..."')
        else:
            print(f'  ✅ {p["key"]}: desc 追加 Note')

    if failed:
        print('\n=== 失败项 ===')
        for p, err in failed:
            print(f'  ❌ {p["key"]}: {err}')

    print(f'\n=== 跳过（基础属性变更，无 attributes 字段）: {len(skipped_attribute_changes)} 项 ===')
    for s in skipped_attribute_changes:
        print(f'  ⏭  {s["item"]}: {s["change"]}')

if __name__ == '__main__':
    main()