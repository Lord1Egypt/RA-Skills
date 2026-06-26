/**
 * Claw RPG — 核心公式引擎 v2.0.0
 * D&D 3.5 標準規則系統
 * 等级 / XP / 属性調整值 / 職業 / 技能 / 衍生數值
 */

// ── 等级 / XP (D&D 3.5 標準公式) ─────────────────────────────

/** 到达第 n 级所需总 XP（n >= 1）— D&D 3.5: n*(n-1)/2 * 1000 */
export function xpForLevel(n) {
  if (n <= 1) return 0;
  return n * (n - 1) / 2 * 1000;
}

/** 从总 XP 反推当前等级 */
export function levelForXp(totalXp) {
  let level = 1;
  while (xpForLevel(level + 1) <= totalXp) level++;
  return Math.min(level, 999);
}

/** 当前等级还需多少 XP 才升级 */
export function xpToNextLevel(totalXp) {
  const cur = levelForXp(totalXp);
  if (cur >= 999) return 0;
  return xpForLevel(cur + 1) - totalXp;
}

/** 当前等级内进度百分比 0-100 */
export function levelProgress(totalXp) {
  const cur = levelForXp(totalXp);
  if (cur >= 999) return 100;
  const start = xpForLevel(cur);
  const end   = xpForLevel(cur + 1);
  return Math.floor(((totalXp - start) / (end - start)) * 100);
}

/** 从 token 消耗计算获得的 XP */
export function calcXpGain({ consumed = 0, produced = 0, bonusXp = 0 } = {}) {
  return Math.floor(consumed / 10) + Math.floor(produced / 10 * 2) + bonusXp;
}

// ── 转职 (Prestige) ───────────────────────────────────────────

export const PRESTIGE_TITLES = [
  'Apprentice', 'Warrior Lobster', 'Knight Lobster', 'Commander Lobster',
  'General Lobster', 'Legendary Lobster', 'Mythic Lobster', 'Epic Lobster',
  'Ancient Lobster', 'Eternal Lobster', 'Chaos Lobster',
];

export function prestigeTitle(prestige) {
  return PRESTIGE_TITLES[Math.min(prestige, PRESTIGE_TITLES.length - 1)];
}

/** 转职后属性加成倍率（每次转职 +10%）*/
export function prestigeMultiplier(prestige) {
  return 1 + prestige * 0.1;
}

// ── 能力調整值 (D&D 3.5) ──────────────────────────────────────

/** D&D 3.5 核心公式：mod = floor((score - 10) / 2) */
export function abilityMod(score) {
  return Math.floor((score - 10) / 2);
}

// ── 属性 (Stats) ──────────────────────────────────────────────

export const STAT_NAMES = {
  claw:      { zh: '爪力', dnd: 'STR', icon: '🦀', desc: '处理复杂任务' },
  antenna:   { zh: '敏捷', dnd: 'DEX', icon: '📡', desc: '反应速度与感知' },
  shell:     { zh: '體質', dnd: 'CON', icon: '🐚', desc: '记忆深度与持久' },
  brain:     { zh: '智力', dnd: 'INT', icon: '🧠', desc: '知识广度与推理' },
  foresight: { zh: '感知', dnd: 'WIS', icon: '👁️', desc: '判断力与价值观' },
  charm:     { zh: '魅力', dnd: 'CHA', icon: '✨', desc: '对话魅力与个性' },
};

/** 从 SOUL.md 和 MEMORY.md 文本推导初始属性（8-18 范围）*/
export function deriveStats(soulText = '', memoryText = '') {
  const soul = soulText.toLowerCase();
  const mem  = memoryText.toLowerCase();

  const weights = {
    claw: [
      ['resourceful','能干','擅长','专业','技能','解决','完成','有用','useful','efficient'],
      soul + mem
    ],
    antenna: [
      ['快速','敏捷','简洁','轻松','随性','灵活','quick','fast','adaptive','responsive'],
      soul
    ],
    shell: [
      ['记忆','memory','经历','历史','积累','连续','持久','深度','learn','experience'],
      soul + mem
    ],
    brain: [
      ['知识','智慧','分析','研究','逻辑','推理','intelligence','knowledge','reason','analysis'],
      soul
    ],
    foresight: [
      ['判断','价值','边界','道德','谨慎','原则','wisdom','careful','ethics','principle'],
      soul
    ],
    charm: [
      ['幽默','俏皮','魅力','个性','有趣','charisma','funny','playful','witty','personality'],
      soul
    ],
  };

  const stats = {};
  for (const [stat, [keywords, text]] of Object.entries(weights)) {
    const hits = keywords.filter(kw => text.includes(kw)).length;
    stats[stat] = Math.min(18, Math.max(8, 10 + hits));
  }

  const memLines = memoryText.split('\n').filter(l => l.trim()).length;
  stats.shell = Math.min(18, stats.shell + Math.floor(memLines / 20));

  return stats;
}

// ── 11 個職業定義 ─────────────────────────────────────────────

/**
 * HD: 生命骰面值
 * bab: 'full' | '3/4' | '1/2'
 * fort/ref/will: 'G'(Good) | 'P'(Poor)
 */
export const CLASSES = {
  barbarian: { zh: '蠻勇龍蝦', icon: '🪓', hd: 12, bab: 'full', fort: 'G', ref: 'P', will: 'P', desc: 'STR 主導，狂暴戰士' },
  fighter:   { zh: '戰士龍蝦', icon: '⚔️',  hd: 10, bab: 'full', fort: 'G', ref: 'P', will: 'P', desc: 'STR+CON，全能戰士' },
  paladin:   { zh: '聖騎龍蝦', icon: '🛡️', hd: 10, bab: 'full', fort: 'G', ref: 'P', will: 'P', desc: 'STR+CHA，神聖騎士' },
  ranger:    { zh: '遊俠龍蝦', icon: '🏹', hd: 8,  bab: 'full', fort: 'G', ref: 'G', will: 'P', desc: 'DEX+WIS，野外獵手' },
  cleric:    { zh: '祭司龍蝦', icon: '✝️',  hd: 8,  bab: '3/4', fort: 'G', ref: 'P', will: 'G', desc: 'WIS+CON，神術師' },
  druid:     { zh: '德魯伊龍蝦',icon: '🌿', hd: 8,  bab: '3/4', fort: 'G', ref: 'P', will: 'G', desc: '全均衡，自然之力' },
  monk:      { zh: '武僧龍蝦', icon: '👊', hd: 8,  bab: '3/4', fort: 'G', ref: 'G', will: 'G', desc: 'WIS+DEX，拳法大師' },
  rogue:     { zh: '刺客龍蝦', icon: '🗡️', hd: 6,  bab: '3/4', fort: 'P', ref: 'G', will: 'P', desc: 'DEX+INT，暗影刺客' },
  bard:      { zh: '吟遊龍蝦', icon: '🎭', hd: 6,  bab: '3/4', fort: 'P', ref: 'G', will: 'G', desc: 'CHA+DEX，吟遊詩人' },
  wizard:    { zh: '法師龍蝦', icon: '🧙', hd: 4,  bab: '1/2', fort: 'P', ref: 'P', will: 'G', desc: 'INT+WIS，奧術法師' },
  sorcerer:  { zh: '術士龍蝦', icon: '🔮', hd: 4,  bab: '1/2', fort: 'P', ref: 'P', will: 'G', desc: 'CHA 主導，天生術士' },
};

// ── 職業判定 ─────────────────────────────────────────────────

/** 根据属性判断职业（D&D 3.5 11職業邏輯）*/
export function detectClass(stats) {
  const sorted = Object.entries(stats).sort(([,a],[,b]) => b - a);
  const top2   = sorted.slice(0, 2).map(([k]) => k);
  const max    = sorted[0][1];
  const min    = sorted[sorted.length - 1][1];

  // 1. 全屬性差距 < 3 → druid
  if (max - min < 3) return 'druid';

  const s = stats;
  const sortedVals = sorted.map(([,v]) => v);
  const second = sortedVals[1];

  // 2. claw(STR) 最高且比第2高≥3 → barbarian
  if (sorted[0][0] === 'claw' && max - second >= 3) return 'barbarian';

  // 3. claw+charm(STR+CHA) 是 top2 → paladin
  if (top2.includes('claw') && top2.includes('charm')) return 'paladin';

  // 4. antenna+foresight(DEX+WIS) 是 top2 → ranger
  if (top2.includes('antenna') && top2.includes('foresight')) return 'ranger';

  // 5. foresight+shell(WIS+CON) 是 top2 → cleric
  if (top2.includes('foresight') && top2.includes('shell')) return 'cleric';

  // 6. foresight+antenna(WIS+DEX) 是 top2 → monk
  if (top2.includes('foresight') && top2.includes('antenna')) return 'monk';

  // 7. antenna+brain(DEX+INT) 是 top2 → rogue
  if (top2.includes('antenna') && top2.includes('brain')) return 'rogue';

  // 8. charm+antenna(CHA+DEX) 是 top2 → bard
  if (top2.includes('charm') && top2.includes('antenna')) return 'bard';

  // 9. brain+foresight(INT+WIS) 是 top2 → wizard
  if (top2.includes('brain') && top2.includes('foresight')) return 'wizard';

  // 10. charm 最高且比第2高≥3 → sorcerer
  if (sorted[0][0] === 'charm' && max - second >= 3) return 'sorcerer';

  // 11. claw+shell(STR+CON) 是 top2 → fighter（兜底）
  if (top2.includes('claw') && top2.includes('shell')) return 'fighter';

  // 12. 最高單屬性兜底
  const highest = sorted[0][0];
  const fallback = {
    claw: 'fighter', antenna: 'rogue', shell: 'fighter',
    brain: 'wizard', foresight: 'cleric', charm: 'bard',
  };
  return fallback[highest] || 'druid';
}

/** 检查属性变化是否应触发职业重判（任意属性变化 > 3）*/
export function shouldReclassify(oldStats, newStats) {
  return Object.keys(oldStats).some(k => Math.abs((newStats[k]||0) - (oldStats[k]||0)) > 3);
}

// ── 衍生數值計算 ──────────────────────────────────────────────

/** 計算基礎攻擊加值 */
export function calcBAB(classId, level) {
  const cls = CLASSES[classId];
  if (!cls) return level;
  switch (cls.bab) {
    case 'full': return level;
    case '3/4':  return Math.floor(level * 3 / 4);
    case '1/2':  return Math.floor(level / 2);
    default:     return level;
  }
}

/** 計算基礎豁免值（不含屬性調整值）*/
function baseSave(saveType, level) {
  if (saveType === 'G') return 2 + Math.floor(level / 2);
  return Math.floor(level / 3);
}

/** 計算豁免三值（含屬性調整值）*/
export function calcSaves(classId, level, stats) {
  const cls = CLASSES[classId] || CLASSES.fighter;
  const conMod = abilityMod(stats.shell     || 10);
  const dexMod = abilityMod(stats.antenna   || 10);
  const wisMod = abilityMod(stats.foresight || 10);
  return {
    fort: baseSave(cls.fort, level) + conMod,
    ref:  baseSave(cls.ref,  level) + dexMod,
    will: baseSave(cls.will, level) + wisMod,
  };
}

/** 計算最大 HP
 * HP = HD + floor((HD/2+1) * (level-1)) + CON_mod * level
 */
export function calcHP(classId, level, stats) {
  const cls = CLASSES[classId] || CLASSES.fighter;
  const hd     = cls.hd;
  const conMod = abilityMod(stats.shell || 10);
  return hd + Math.floor((hd / 2 + 1) * (level - 1)) + conMod * level;
}

/** 計算護甲等級 AC = 10 + DEX_mod */
export function calcAC(stats) {
  return 10 + abilityMod(stats.antenna || 10);
}

/** 計算先攻加值 = DEX_mod */
export function calcInitiative(stats) {
  return abilityMod(stats.antenna || 10);
}

// ── 專長 (Feats) ──────────────────────────────────────────────

const FEAT_NAMES = {
  barbarian: {
    general: ['Primal Instinct','Power Surge','Wild Charge','Iron Constitution','Savage Sense','Thick Hide','Brutal Strike','Undying Will'],
    bonus:   [],
  },
  fighter: {
    general: ['Iron Defense','Combat Expertise','Steadfast Fighter','Power Attack','Tactical Master','Indomitable','Fearless Warrior','Eternal Grit'],
    bonus:   ['Weapon Focus','Weapon Specialization','Shield Mastery','Improved Power Attack','Combat Reflexes','Weapon Versatility','Lightning Riposte','Armor Proficiency','Combat Intuition','War God Talent','Armor Penetration'],
  },
  paladin: {
    general: ['Sacred Oath','Path of Light','Holy Shield','Divine Blessing','Radiant Drive','Eternal Heart','Divine Guardian','Celestial Ward'],
    bonus:   [],
  },
  ranger: {
    general: ["Hunter's Eye",'Wilderness Stealth','Precise Shot','Nature Affinity','Track Master','Swift Stride','Woodland Ranger','Supreme Hunter'],
    bonus:   [],
  },
  cleric: {
    general: ['Spell Power','Devout Prayer','Sacred Defense','Exorcism','Divine Mercy','Holy Baptism','Divine Miracle','Celestial Envoy'],
    bonus:   [],
  },
  druid: {
    general: ['Nature Affinity','Shape Control','Ecosystem Sense','Earth Force','Nature Ward','Wild Form','Heart of Nature','Life Cycle'],
    bonus:   [],
  },
  monk: {
    general: ['Zen Mind','Swift Footwork','Ki Cultivation','Diamond Mind','Martial Mastery','Shadowless Kick','Meditative State','Egoless Way'],
    bonus:   [],
  },
  rogue: {
    general: ['Shadow Step','Precision Strike','Evasive Instinct','Thrown Weapon','Intel Gathering','Perfect Ambush','Darkvision','Shadow Assassination'],
    bonus:   [],
  },
  bard: {
    general: ['Poetic Resonance','Silver Tongue','Rally Morale','Counter Enchantment','Polyglot','Charismatic Aura','Inspire Greatness','Timeless Song'],
    bonus:   [],
  },
  wizard: {
    general: ['Arcane Acuity','Spellbook Research','Broad Knowledge','Elemental Mastery','Spell Power','Magic Sense','Arcane Insight','Omniscient Mind'],
    bonus:   [],
  },
  sorcerer: {
    general: ['Draconic Awakening','Innate Spellcasting','Surging Power','Bloodline Resonance','Chaos Burst','Born Caster','Sorcerous Instinct','Chaos Incarnate'],
    bonus:   [],
  },
};

/** 計算某職業在某等級應有的全部專長列表 */
export function calcFeats(classId, level) {
  const names = FEAT_NAMES[classId] || FEAT_NAMES.fighter;
  const feats = [];

  // General feats: L1, L3, L6, L9, L12, L15, L18, L21, L24, L27, L30...
  const generalLevels = [];
  generalLevels.push(1);
  for (let l = 3; l <= level; l += 3) generalLevels.push(l);

  let gIdx = 0;
  for (const l of generalLevels) {
    if (l > level) break;
    const name = names.general[gIdx] || `General Feat ${gIdx + 1}`;
    feats.push({ level: l, name: `${name} (L${l})` });
    gIdx++;
  }

  // Fighter bonus feats: L1, L2, L4, L6, L8, L10, L12, L14, L16, L18, L20...
  if (classId === 'fighter') {
    const bonusLevels = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20];
    let bIdx = 0;
    for (const l of bonusLevels) {
      if (l > level) break;
      const name = names.bonus[bIdx] || `Fighter Feat ${bIdx + 1}`;
      feats.push({ level: l, name: `${name} (L${l}) [Fighter]` });
      bIdx++;
    }
  }

  // Sort by level, then by name
  feats.sort((a, b) => a.level - b.level || a.name.localeCompare(b.name));

  return feats.map(f => f.name);
}

// ── 技能 (Abilities) ──────────────────────────────────────────

export const ABILITY_TABLE = {
  barbarian: { 1: 'Rage',             4: 'Fast Movement',   8: 'Primal Instinct', 16: 'Indomitable' },
  fighter:   { 1: 'Fighter Talent',   4: 'Weapon Mastery',  8: 'Battlefield Control', 16: 'Unbreakable Soul' },
  paladin:   { 1: 'Smite Evil',       4: 'Divine Grace',    8: 'Sacred Shield',   16: 'Eternal Vow' },
  ranger:    { 1: 'Favored Enemy',    4: 'Wilderness Stride',8: 'Swift Shot',      16: 'Master Hunter' },
  cleric:    { 1: 'Domain Power',     4: 'Turn Undead',     8: 'Divine Shield',   16: 'Avatar of God' },
  druid:     { 1: "Nature's Tongue",  4: 'Wild Shape',      8: 'Ecosystem Sense', 16: "Nature's Wrath" },
  monk:      { 1: 'Unarmed Strike',   4: 'Swift Movement',  8: 'Diamond Mind',    16: 'Egoless State' },
  rogue:     { 1: 'Sneak Attack',     4: 'Evasion',         8: 'Precision Strike', 16: 'Perfect Kill' },
  bard:      { 1: 'Bardic Inspiration',4: 'Countersong',    8: 'Master of Tongues',16: 'Timeless Work' },
  wizard:    { 1: 'Arcane Analysis',  4: 'Arcane Apprentice',8: 'Knowledge Explosion',16: 'All-Seeing Eye' },
  sorcerer:  { 1: 'Innate Casting',   4: 'Draconic Bloodline',8: 'Spell Power',   16: 'Chaos Source' },
};

/** 获取某职业在某等级应拥有的全部技能（閾值：1/4/8/16）*/
export function getAbilities(classId, level) {
  const table = ABILITY_TABLE[classId] || {};
  const thresholds = [1, 4, 8, 16];
  return thresholds
    .filter(req => req <= level)
    .map(req => table[req])
    .filter(Boolean);
}

// ── 等级段加成 ────────────────────────────────────────────────

/** 每 5 级给一次属性点 */
export function statPointsAtLevel(level) {
  return Math.floor(level / 5);
}

// ── Proficiency Bonus（保留不變）─────────────────────────────

export function proficiencyBonus(level) {
  return 2 + Math.floor((Math.min(level, 20) - 1) / 4);
}
