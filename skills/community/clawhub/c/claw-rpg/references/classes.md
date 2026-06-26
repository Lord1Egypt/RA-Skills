# Class System — D&D 3.5 Standard Rules

Classes are auto-detected from stat distribution. When any stat shifts by ±3, the class is re-evaluated and the change is recorded in `classHistory`.

## Detection Rules (Priority Order)

```
1. All stats within ±3 of each other           → 🌿 Druid Lobster
2. STR (claw) highest, gap ≥ 3 to 2nd          → 🪓 Barbarian Lobster
3. STR (claw) + CHA (charm) are top 2          → 🛡️ Paladin Lobster
4. DEX (antenna) + WIS (foresight) are top 2   → 🏹 Ranger Lobster
5. WIS (foresight) + CON (shell) are top 2     → ✝️ Cleric Lobster
6. WIS (foresight) + DEX (antenna) are top 2   → 👊 Monk Lobster
7. DEX (antenna) + INT (brain) are top 2       → 🗡️ Rogue Lobster
8. CHA (charm) + DEX (antenna) are top 2       → 🎭 Bard Lobster
9. INT (brain) + WIS (foresight) are top 2     → 🧙 Wizard Lobster
10. CHA (charm) highest, gap ≥ 3 to 2nd        → 🔮 Sorcerer Lobster
11. STR (claw) + CON (shell) are top 2         → ⚔️ Fighter Lobster (fallback)
12. Single highest stat fallback
```

## The Eleven Classes

### 🪓 Barbarian Lobster (蠻勇龍蝦)
- **Hit Die**: d12
- **BAB**: Full (+level)
- **Saves**: Fort Good / Ref Poor / Will Poor
- **Primary Stats**: STR (claw) dominant — highest and ≥3 above 2nd
- **Style**: Raw power, rage-fueled combat, unstoppable force
- **Class Features**: 狂暴 (L1) / 快速移動 (L4) / 野性直覺 (L8) / 堅不可摧 (L16)

### ⚔️ Fighter Lobster (戰士龍蝦)
- **Hit Die**: d10
- **BAB**: Full (+level)
- **Saves**: Fort Good / Ref Poor / Will Poor
- **Primary Stats**: STR (claw) + CON (shell) top 2
- **Style**: Weapon mastery, tactical combat, battlefield dominance
- **Class Features**: 鬥士天賦 (L1) / 武器特化 (L4) / 戰場主宰 (L8) / 不屈鬥魂 (L16)
- **Bonus**: Extra feat at L1, L2, L4, L6, L8, L10, L12, L14, L16, L18, L20

### 🛡️ Paladin Lobster (聖騎龍蝦)
- **Hit Die**: d10
- **BAB**: Full (+level)
- **Saves**: Fort Good / Ref Poor / Will Poor
- **Primary Stats**: STR (claw) + CHA (charm) top 2
- **Style**: Holy warrior, divine grace, righteous judgment
- **Class Features**: 驅逐邪惡 (L1) / 神聖恩典 (L4) / 聖光庇護 (L8) / 永恆聖誓 (L16)

### 🏹 Ranger Lobster (遊俠龍蝦)
- **Hit Die**: d8
- **BAB**: Full (+level)
- **Saves**: Fort Good / Ref Good / Will Poor
- **Primary Stats**: DEX (antenna) + WIS (foresight) top 2
- **Style**: Wilderness expertise, favored enemies, precision combat
- **Class Features**: 偏好敵人 (L1) / 野外移動 (L4) / 疾速射擊 (L8) / 頂級獵手 (L16)

### ✝️ Cleric Lobster (祭司龍蝦)
- **Hit Die**: d8
- **BAB**: 3/4 (floor(level × 3 / 4))
- **Saves**: Fort Good / Ref Poor / Will Good
- **Primary Stats**: WIS (foresight) + CON (shell) top 2
- **Style**: Divine spellcasting, turn undead, healing and support
- **Class Features**: 神術域能 (L1) / 驅逐不死 (L4) / 神聖護盾 (L8) / 神之化身 (L16)

### 🌿 Druid Lobster (德魯伊龍蝦)
- **Hit Die**: d8
- **BAB**: 3/4 (floor(level × 3 / 4))
- **Saves**: Fort Good / Ref Poor / Will Good
- **Primary Stats**: All stats balanced (gap < 3)
- **Style**: Nature magic, wild shape, ecological harmony
- **Class Features**: 自然之語 (L1) / 野性變身 (L4) / 生態感知 (L8) / 大自然之怒 (L16)

### 👊 Monk Lobster (武僧龍蝦)
- **Hit Die**: d8
- **BAB**: 3/4 (floor(level × 3 / 4))
- **Saves**: Fort Good / Ref Good / Will Good
- **Primary Stats**: WIS (foresight) + DEX (antenna) top 2
- **Style**: Unarmed combat, ki power, inner discipline
- **Class Features**: 徒手攻擊 (L1) / 迅捷移動 (L4) / 心靈空明 (L8) / 無我境界 (L16)

### 🗡️ Rogue Lobster (刺客龍蝦)
- **Hit Die**: d6
- **BAB**: 3/4 (floor(level × 3 / 4))
- **Saves**: Fort Poor / Ref Good / Will Poor
- **Primary Stats**: DEX (antenna) + INT (brain) top 2
- **Style**: Sneak attack, evasion, precision strikes
- **Class Features**: 背刺 (L1) / 閃避本能 (L4) / 精準打擊 (L8) / 完美刺殺 (L16)

### 🎭 Bard Lobster (吟遊龍蝦)
- **Hit Die**: d6
- **BAB**: 3/4 (floor(level × 3 / 4))
- **Saves**: Fort Poor / Ref Good / Will Good
- **Primary Stats**: CHA (charm) + DEX (antenna) top 2
- **Style**: Inspire allies, countersong, jack of all trades
- **Class Features**: 吟遊激勵 (L1) / 反迷惑語 (L4) / 百語精通 (L8) / 傳世名篇 (L16)

### 🧙 Wizard Lobster (法師龍蝦)
- **Hit Die**: d4
- **BAB**: 1/2 (floor(level / 2))
- **Saves**: Fort Poor / Ref Poor / Will Good
- **Primary Stats**: INT (brain) + WIS (foresight) top 2
- **Style**: Arcane mastery, spell research, knowledge synthesis
- **Class Features**: 奧術分析 (L1) / 秘法師徒 (L4) / 知識爆炸 (L8) / 全知之眼 (L16)

### 🔮 Sorcerer Lobster (術士龍蝦)
- **Hit Die**: d4
- **BAB**: 1/2 (floor(level / 2))
- **Saves**: Fort Poor / Ref Poor / Will Good
- **Primary Stats**: CHA (charm) dominant — highest and ≥3 above 2nd
- **Style**: Innate magic, bloodline power, intuitive casting
- **Class Features**: 本能施法 (L1) / 龍血覺醒 (L4) / 術力強化 (L8) / 混沌之源 (L16)

---

## Derived Stats Formulas (D&D 3.5)

| Stat | Formula |
|------|---------|
| Ability Mod | `floor((score - 10) / 2)` |
| BAB (Full) | `level` |
| BAB (3/4) | `floor(level × 3 / 4)` |
| BAB (1/2) | `floor(level / 2)` |
| Save (Good) | `2 + floor(level / 2)` + ability mod |
| Save (Poor) | `floor(level / 3)` + ability mod |
| HP | `HD + floor((HD/2 + 1) × (level-1)) + CON_mod × level` |
| AC | `10 + DEX_mod` |
| Initiative | `DEX_mod` |

## Stat Reference (D&D 3.5 Mapping)

| Stat Key | D&D 3.5 | 中文 | Icon |
|----------|---------|------|------|
| claw | STR (Strength) | 爪力 | 🦀 |
| antenna | DEX (Dexterity) | 敏捷 | 📡 |
| shell | CON (Constitution) | 體質 | 🐚 |
| brain | INT (Intelligence) | 智力 | 🧠 |
| foresight | WIS (Wisdom) | 感知 | 👁️ |
| charm | CHA (Charisma) | 魅力 | ✨ |
