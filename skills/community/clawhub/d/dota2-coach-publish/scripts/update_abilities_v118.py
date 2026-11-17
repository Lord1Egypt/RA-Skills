#!/usr/bin/env python3
"""
v1.1.8 英雄技能数据更新脚本（7.41d 版本）
- field_patches: 结构化字段（mc/cd/cast_range）
- desc_patches: 精确文本替换
- desc_notes: 行为/数值变更说明
"""
import json, os, shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ABILITIES_FILE = f'{SCRIPT_DIR}/abilities_db.json'
BACKUP_FILE = f'{SCRIPT_DIR}/../backup_v118_20260731/abilities_db.json'

# === A. 结构化字段补丁 ===
field_patches = [
    # 光之守卫 - 查克拉魔法 cd
    ("keeper_of_the_light", "keeper_of_the_light_chakra_magic", "cd", ["19","16","13","10"], ["20","17","14","11"]),
    # 光之守卫 - 炎阳之缚 cast_range
    ("keeper_of_the_light", "keeper_of_the_light_radiant_bind", "cast_range", "850", "750"),
    # 帕克 - 幻象法球 cd
    ("puck", "puck_illusory_orb", "cd", ["11","10","9","8"], ["12","11","10","9"]),
    # 痛苦女王 - 暗影突袭 mc
    ("queenofpain", "queenofpain_shadow_strike", "mc", ["100","110","120","130"], ["100","105","110","115"]),
    # 瘟疫法师 - 死亡搜寻 cast_range
    ("necrolyte", "necrolyte_death_seeker", "cast_range", "750", "600"),
    # 远古冰魄 - 冰晶爆轰 cd
    ("ancient_apparition", "ancient_apparition_ice_blast", "cd", ["60","50","40"], ["50","45","40"]),
    # 矮人直升机 - 火箭弹幕 mc
    ("gyrocopter", "gyrocopter_rocket_barrage", "mc", 85, 75),
    # 矮人直升机 - 追踪导弹 mc
    ("gyrocopter", "gyrocopter_homing_missile", "mc", ["120","130","140","150"], ["120","120","120","120"]),
    # 矮人直升机 - 追踪导弹 cd
    ("gyrocopter", "gyrocopter_homing_missile", "cd", ["30","24","18","12"], ["26","21","16","11"]),
    # 卓尔游侠 - 数箭齐发 mc
    ("drow_ranger", "drow_ranger_multishot", "mc", ["50","70","90","110"], ["70","85","100","115"]),
    # 树精卫士 - 活体护甲 mc
    ("treant", "treant_living_armor", "mc", ["65","70","75","80"], ["80","80","80","80"]),
    # 森海飞霞 - 一箭穿心 mc
    ("hoodwink", "hoodwink_sharpshooter", "mc", ["100","150","200"], ["150","200","250"]),
    # 森海飞霞 - 猎手旋镖 cd
    ("hoodwink", "hoodwink_hunters_boomerang", "cd", 18, 20),
    # 殁境神蚀者 - 责难 cd
    ("obsidian_destroyer", "obsidian_destroyer_objurgation", "cd", ["36","34","32","30"], ["36","33","30","27"]),
    # 神谕者 - 虚妄之诺 cast_range
    ("oracle", "oracle_false_promise", "cast_range", ["700","800","900"], ["800","850","900"]),
    # 变体精灵 - 变形 cd
    ("morphling", "morphling_replicate", "cd", ["140","100","60"], ["125","90","55"]),
    # 剧毒术士 - 毒蛇撕咬 mc（值不变，但确保数据一致）
    ("venomancer", "venomancer_snakebite", "mc", ["70","80","90","100"], ["70","80","90","100"]),
]

# === B. desc 精确替换 ===
desc_patches = [
    # 剧毒术士 - 毒蛇撕咬初始伤害
    ("venomancer", "venomancer_snakebite",
     "dealing 10/20/30/40 magical damage per second",
     "dealing 10/30/50/70 magical damage per second"),
    # 全能骑士 - 纯洁之锤治疗量
    ("omniknight", "omniknight_hammer_of_purity",
     "heals for 30% of the damage dealt over 5s",
     "heals for 40% of the damage dealt over 4s"),
    # 电炎绝手 - 电光石火平射额外伤害
    ("snapfire", "snapfire_scatterblast",
     "Damage is increased by 30%",
     "Damage is increased by 25%"),
    # 发条技师 - 能量齿轮行进距离（desc 里有 "up to 1000 distance"）
    ("rattletrap", "rattletrap_power_cogs",
     "up to 1000 distance away",
     "up to 850/900/950/1000 distance away"),
    # 编织者 - 命运之线断裂距离
    ("weaver", "weaver_threads_of_fate",
     "within 700 range of them",
     "within 890 range of them"),
]

# === C. desc 追加 Note ===
desc_notes = [
    # --- 隐身/开关行为变更 ---
    ("zuus", "zuus_lightning_hands",
     "\n\n# Update (7.41d)\nLightning Hands no longer breaks invisibility when toggled. Can be toggled while silenced. Attack speed bonus reduced to 20 (was 30)."),
    ("elder_titan", "elder_titan_return_spirit",
     "\n\n# Update (7.41d)\nReturn Spirit and Spirit Move sub-abilities no longer break invisibility."),
    ("elder_titan", "elder_titan_ancestral_spirit",
     "\n\n# Update (7.41d)\nAncestral Spirit's Move sub-ability no longer breaks invisibility."),
    ("troll_warlord", "troll_warlord_switch_stance",
     "\n\n# Update (7.41d)\nSwitching stances no longer breaks invisibility."),
    ("troll_warlord", "troll_warlord_battle_trance",
     "\n\n# Update (7.41d)\nBattle Trance now also grants 35% slow resistance."),
    ("medusa", "medusa_split_shot",
     "\n\n# Update (7.41d)\nSplit Shot no longer breaks invisibility when toggled. Can be toggled while silenced."),
    ("muerta", "muerta_gunslinger",
     "\n\n# Update (7.41d)\nGunslinger no longer breaks invisibility when toggled."),
    ("visage", "visage_stone_form_self_cast",
     "\n\n# Update (7.41d)\nStone Form no longer breaks invisibility when used to command Familiars."),
    ("batrider", "batrider_smoldering_resin",
     "\n\n# Update (7.41d)\nSmoldering Resin no longer applies when attacking allied units."),

    # --- 缠绕打断 ---
    ("abyssal_underlord", "abyssal_underlord_dark_portal",
     "\n\n# Update (7.41d)\nChanneling Dark Portal is now interrupted by immobilize effects."),
    ("templar_assassin", "templar_assassin_trap_teleport",
     "\n\n# Update (7.41d)\nPsi Blades Trap Teleport is now interrupted by immobilize effects."),
    ("sniper", "sniper_concussive_grenade",
     "\n\n# Update (7.41d)\nConcussive Grenade can now be cast while immobilized. Sniper is not knocked back while immobilized."),

    # --- 幻象视野惩罚移除 ---
    ("morphling", "morphling_replicate",
     "\n\n# Update (7.41d)\nAghanim's Scepter upgrade: Replicate illusions no longer have vision penalty."),
    ("vengefulspirit", "vengefulspirit_command_aura",
     "\n\n# Update (7.41d)\nAghanim's Scepter upgrade: Vengeance Aura illusions no longer have vision penalty."),
    ("grimstroke", "grimstroke_dark_portrait",
     "\n\n# Update (7.41d)\nDark Portrait illusions no longer have vision penalty."),
    ("phantom_assassin", "phantom_assassin_blur",
     "\n\n# Update (7.41d)\nBlur is now undispellable."),

    # --- 技能叠加/交互 ---
    ("queenofpain", "queenofpain_sonic_wave",
     "\n\n# Update (7.41d)\nRapidly cast Sonic Waves can now stack their damage."),
    ("oracle", "oracle_fates_edict",
     "\n\n# Update (7.41d)\nFate's Edict cast on Oracle or allies can now be dispelled by enemies."),
    ("witch_doctor", "witch_doctor_maledict",
     "\n\n# Update (7.41d)\nLevel 20 talent: Maledict burst treats illusions as non-hero targets. Burst from illusions does not deal damage."),
    ("nevermore", "nevermore_shadowraze1",
     "\n\n# Update (7.41d)\nShadowraze stack duration reduced from 7s to 6s. Level 25 talent: Shadowraze attack damage no longer applies attack modifiers or triggers."),

    # --- 技能数值变更（desc 无具体数字，用 Note 说明） ---
    ("zuus", "zuus_thundergods_wrath",
     "\n\n# Update (7.41d)\nDamage reduced from 300/475/650 to 275/425/575."),
    ("axe", "axe_battle_hunger",
     "\n\n# Update (7.41d)\nDamage per second reduced to 12/16/20/24 (was 12/18/24/30)."),
    ("doom_bringer", "doom_bringer_infernal_blade",
     "\n\n# Update (7.41d)\nBase burn damage: 18/34/50/66 (was 15/30/45/60). Max Health Burn: 0.5/1.75/3/4.25% (was 1/2/3/4%)."),
    ("snapfire", "snapfire_firesnap_cookie",
     "\n\n# Update (7.41d)\nImpact damage reduced from 75/150/225/300 to 60/130/200/270."),
    ("snapfire", "snapfire_mortimer_kisses",
     "\n\n# Update (7.41d)\nFireball damage reduced from 180/270/360 to 170/250/330."),
    ("snapfire", "snapfire_scatterblast",
     "\n\n# Update (7.41d)\nScatterblast initial blast width is no longer increased by cast range bonuses. Point-blank bonus damage reduced from 30% to 25%."),
    ("centaur", "centaur_double_edge",
     "\n\n# Update (7.41d)\nAghanim's Shard upgrade: Double Edge buff duration reduced from 15s to 12s."),
    ("centaur", "centaur_return",
     "\n\n# Update (7.41d)\nReturn damage based on strength reduced from 16/24/32/40% to 14/21/28/35%."),
    ("magnataur", "magnataur_horn_toss",
     "\n\n# Update (7.41d)\nHorn Toss damage increased from 300 to 325."),
    ("dragon_knight", "dragon_knight_wyrms_wrath",
     "\n\n# Update (7.41d)\nRadius bonus increased from 25/50/75/100 to 30/60/90/120."),
    ("ringmaster", "ringmaster_impalement",
     "\n\n# Update (7.41d)\nNon-hero damage per second adjusted from 85/90/95/100 to 60/75/90/105."),
    ("treant", "treant_leech_seed",
     "\n\n# Update (7.41d)\nRoot duration reduced from 0.9/1.1/1.3/1.5s to 0.75/1.0/1.25/1.5s."),
    ("rattletrap", "rattletrap_power_cogs",
     "\n\n# Update (7.41d)\nMana lost: 40/75/110/145 (was 40/80/120/160). Cogs travel distance: 850/900/950/1000 (was 1000). Cogs vision: 800/400 (was 1600/600). Cogs no longer block neutral camp spawns."),
    ("night_stalker", "night_stalker_crippling_fear",
     "\n\n# Update (7.41d)\nRadius reduced from 375 to 350."),
    ("bane", "bane_nightmare",
     "\n\n# Update (7.41d)\nDuration reduced from 3.5/4.5/5.5/6.5s to 3/4/5/6s. Target now has no vision instead of overlaid vision."),
    ("bane", "bane_ichor_of_nyctasha",
     "\n\n# Update (7.41d)\nMax Fear Stacks: 6 (was 5). Status Resistance per Stack: 4% (was 5%)."),
    ("bane", "bane_fiends_grip",
     "\n\n# Update (7.41d)\nAghanim's Scepter: Fiend's Grip cooldown reduction reduced from 45s to 40s."),
    ("undying", "undying_flesh_golem",
     "\n\n# Update (7.41d)\nMovement speed bonus increased from 20% to 25%."),
    ("elder_titan", "elder_titan_momentum",
     "\n\n# Update (7.41d)\nArmor from movement speed: 7% + 0.5% per level (was 5% + 0.5% per level)."),
    ("omniknight", "omniknight_hammer_of_purity",
     "\n\n# Update (7.41d)\nHeal: 40% of damage dealt over 4s (was 35% over 5s)."),
    ("obsidian_destroyer", "obsidian_destroyer_objurgation",
     "\n\n# Update (7.41d)\nObjurgation is now instant cast, no longer interrupts movement. Shield: 150/200/250/300 (was 120/180/240/300)."),
    ("invoker", "invoker_ghost_walk",
     "\n\n# Update (7.41d)\nDuration reduced from 60s to 50s. Aghanim's Shard no longer increases Ghost Walk's radius."),
    ("spectre", "spectre_haunt",
     "\n\n# Update (7.41d)\nIllusion attack damage: 35/50/65% (was 30/50/70%)."),
    ("hoodwink", "hoodwink_mistwoods_wayfarer",
     "\n\n# Update (7.41d)\nTurn chance: 14.25% + 0.75% per level (was 14% + 1% per level)."),
    ("necrolyte", "necrolyte_sadist",
     "\n\n# Update (7.41d)\nSadist regen: 3.8 + 0.2 per level (was 3.7 + 0.3 per level)."),
    ("phantom_lancer", "phantom_lancer_juxtapose",
     "\n\n# Update (7.41d)\nAghanim's Shard: Juxtapose cooldown increased from 15s to 18s."),
    ("chaos_knight", "chaos_knight_chaos_bolt",
     "\n\n# Update (7.41d)\nChaos Bolt projectile speed increased from 700 to 900."),
    ("lone_druid", "lone_druid_spirit_bear",
     "\n\n# Update (7.41d)\nSpirit Bear base armor reduced by 1. Demolish: bonus damage to buildings reduced from 30% to 20%."),
    ("drow_ranger", "drow_ranger_multishot",
     "\n\n# Update (7.41d)\nArrow distance: 475 + 1x Attack Range (was 1.75x). Base damage bonus: 80/100/120/140% (was 100/120/140/160%)."),
    ("weaver", "weaver_threads_of_fate",
     "\n\n# Update (7.41d)\nThreads of Fate break distance: 890 + 10 * Hero Level (was 900)."),
    ("tiny", None, "\n\n# Update (7.41d)\nBase health regeneration reduced by 1.0."),
]

def main():
    backup_dir = os.path.dirname(BACKUP_FILE)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(ABILITIES_FILE, BACKUP_FILE)
        print(f'已备份: {BACKUP_FILE}')
    else:
        print(f'备份已存在: {BACKUP_FILE}')

    with open(ABILITIES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    abilities_by_hero = {}
    for hero in data:
        abilities_by_hero[hero['hero_key']] = {}
        for ab in hero['abilities']:
            abilities_by_hero[hero['hero_key']][ab['key']] = ab

    applied, failed = [], []

    # A. field_patches
    for hero_key, ab_key, field, old, new in field_patches:
        if hero_key not in abilities_by_hero or ab_key not in abilities_by_hero[hero_key]:
            failed.append(f'field: {hero_key}/{ab_key} 未找到')
            continue
        ab = abilities_by_hero[hero_key][ab_key]
        if ab.get(field) != old:
            failed.append(f'field: {hero_key}/{ab_key}.{field}: 当前={ab.get(field)}, 期望={old}')
            continue
        ab[field] = new
        applied.append(f'field: {hero_key}/{ab_key}.{field}: {old} → {new}')

    # B. desc_patches
    for hero_key, ab_key, find_str, replace_str in desc_patches:
        if hero_key not in abilities_by_hero or ab_key not in abilities_by_hero[hero_key]:
            failed.append(f'desc: {hero_key}/{ab_key} 未找到')
            continue
        ab = abilities_by_hero[hero_key][ab_key]
        desc = ab.get('desc', '') or ''
        cnt = desc.count(find_str)
        if cnt != 1:
            failed.append(f'desc: {hero_key}/{ab_key} find={cnt}, 文本="{find_str[:60]}..."')
            continue
        ab['desc'] = desc.replace(find_str, replace_str)
        applied.append(f'desc: {hero_key}/{ab_key}: 替换 "{find_str[:40]}..."')

    # C. desc_notes
    for hero_key, ab_key, note in desc_notes:
        if hero_key not in abilities_by_hero:
            failed.append(f'note: {hero_key} 未找到')
            continue
        if ab_key is None:
            # 标记在英雄第一个技能上
            for k, v in abilities_by_hero[hero_key].items():
                ab_key = k
                break
            if ab_key is None:
                failed.append(f'note: {hero_key} 无技能')
                continue
        ab = abilities_by_hero[hero_key].get(ab_key)
        if not ab:
            failed.append(f'note: {hero_key}/{ab_key} 未找到')
            continue
        desc = ab.get('desc', '') or ''
        if note.strip() in desc:
            applied.append(f'note: {hero_key}/{ab_key} Note 已存在，跳过')
            continue
        ab['desc'] = desc + note
        applied.append(f'note: {hero_key}/{ab_key}: 追加 Note')

    with open(ABILITIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\n=== 成功: {len(applied)} / 失败: {len(failed)} ===\n')
    for line in applied:
        print(f'  ✅ {line}')
    if failed:
        print('\n=== 失败 ===')
        for line in failed:
            print(f'  ❌ {line}')

if __name__ == '__main__':
    main()