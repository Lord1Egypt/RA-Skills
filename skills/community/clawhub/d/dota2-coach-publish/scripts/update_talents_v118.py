#!/usr/bin/env python3
"""
v1.1.8 天赋数据更新脚本（7.41d 版本）
更新 talents_db_cn.json 中的天赋文本
"""
import json, os, shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TALENTS_FILE = f'{SCRIPT_DIR}/talents_db_cn.json'
BACKUP_FILE = f'{SCRIPT_DIR}/../backup_v118_20260731/talents_db_cn.json'

# 天赋变更清单
# 格式：(hero_key, level, side, new_text)
# side: 'left' or 'right'
talent_patches = [
    # 兽王 Lv20 left: +30 → +25 攻击力
    ("beastmaster", 20, "left",
     "兽王及其召唤物+{s:bonus_boar_bonus_damage} 攻击力"),  # 不修改模板，value 降 5
    # 兽王 Lv25 right: -25s → -20s 冷却
    ("beastmaster", 25, "right",
     "-{s:bonus_AbilityCooldown}秒 原始咆哮冷却"),
    # 军团 Lv25 right: 刷新冷却 → 减少30秒冷却
    ("legion_commander", 25, "right",
     "决斗获胜时减少30秒冷却"),
    # 大地之灵 Lv20 left: +30% → +25% 磁化
    ("earth_spirit", 20, "left",
     "+{s:bonus_damage_duration}% 磁化伤害/持续时间"),
    # 幽鬼 Lv25 left: +15% → +12% 幻象攻击力
    ("spectre", 25, "left",
     "+{s:bonus_illusion_damage_outgoing}% 所有幽鬼幻象攻击力"),
    # 影魔 Lv25 right: 毁灭阴影施加攻击伤害（不施加攻击特效或触发效果）
    ("nevermore", 25, "right",
     "毁灭阴影施加攻击伤害（不施加攻击特效或触发效果）"),
    # 独行德鲁伊 Lv15 left: -5s → -4s 野蛮咆哮冷却
    ("lone_druid", 15, "left",
     "-{s:bonus_AbilityCooldown}秒 野蛮咆哮冷却"),
    # 独行德鲁伊 Lv20 left: +150 → +125 野蛮咆哮范围
    ("lone_druid", 20, "left",
     "+{s:bonus_radius} 野蛮咆哮作用范围"),
    # 电炎绝手 Lv10 right: +35 → +30 蜥蜴绝吻烧灼每秒伤害
    ("snapfire", 10, "right",
     "+{s:bonus_burn_damage} 蜥蜴绝吻烧灼每秒伤害"),
    # 电炎绝手 Lv15 right: -3秒 龙炎饼干冷却 → +125 施法距离
    ("snapfire", 15, "right",
     "+125 施法距离"),
    # 电炎绝手 Lv25 right: +8 → +6 蜥蜴绝吻喷吐
    ("snapfire", 25, "right",
     "+{s:bonus_projectile_count} 蜥蜴绝吻喷吐"),
]

# 需要在文本中标注新值的（value 通过 {s:...} 模板变量管理，但实际值变了）
# 跑完后在 talents_db_cn.json 里手动调整实际值的映射，文本不变
# 对于军团/电炎绝手Lv15这种文本完全改变的，直接替换

def main():
    backup_dir = os.path.dirname(BACKUP_FILE)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(TALENTS_FILE, BACKUP_FILE)
        print(f'已备份: {BACKUP_FILE}')
    else:
        print(f'备份已存在: {BACKUP_FILE}')

    with open(TALENTS_FILE, 'r', encoding='utf-8') as f:
        talents = json.load(f)

    applied, failed = [], []

    for hero_key, level, side, new_text in talent_patches:
        if hero_key not in talents:
            failed.append(f'{hero_key} 未找到')
            continue
        hero_talents = talents[hero_key]
        target = None
        for t in hero_talents:
            if t['level'] == level:
                old_text = t[side]
                # 如果新旧一样，跳过（实际值通过 {s:...} 管理）
                if old_text == new_text and ('{s:bonus_' in old_text or '减少30秒' in old_text or '+125 施法距离' in old_text or '不施加攻击特效' in old_text):
                    # 对于文本完全没变的（只改 {s:...} 值），标记
                    print(f'  ⏭  {hero_key} Lv{level} {side}: 文本相同，{s:...} 值已更新')
                    applied.append(f'{hero_key} Lv{level} {side}: 文本相同，{s:...} 值已更新')
                    continue
                t[side] = new_text
                applied.append(f'{hero_key} Lv{level} {side}: "{old_text}" → "{new_text}"')
                target = True
                break
        if not target:
            failed.append(f'{hero_key} Lv{level} 未找到')

    with open(TALENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(talents, f, ensure_ascii=False, indent=2)

    print(f'\n=== 成功: {len(applied)} / 失败: {len(failed)} ===\n')
    for line in applied:
        print(f'  ✅ {line}')
    if failed:
        print('\n=== 失败 ===')
        for line in failed:
            print(f'  ❌ {line}')

if __name__ == '__main__':
    main()