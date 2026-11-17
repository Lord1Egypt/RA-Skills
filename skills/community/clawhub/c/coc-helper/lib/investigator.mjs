// COC 7e 调查员管理（状态持久化）
// 调查员资料存到 session.json，跨命令保持

import fs from "node:fs";
import path from "node:path";
import { rollDice, makeRng } from "./dice.mjs";

const SESSION_FILE = path.join(import.meta.dirname, "..", "session.json");

// ---------- 持久化 ----------

export function loadSession() {
  if (!fs.existsSync(SESSION_FILE)) {
    return { investigators: [], pulp: false };
  }
  try {
    return JSON.parse(fs.readFileSync(SESSION_FILE, "utf8"));
  } catch {
    return { investigators: [], pulp: false };
  }
}

export function saveSession(session) {
  const tmp = SESSION_FILE + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(session, null, 2));
  fs.renameSync(tmp, SESSION_FILE);
}

// ---------- 衍生属性计算 ----------

/**
 * 根据 STR+SIZ 查 DB 和体格。
 */
export function dbAndBuild(str, siz) {
  const total = str + siz;
  if (total <= 64) return { db: -2, build: -2 };
  if (total <= 84) return { db: -1, build: -1 };
  if (total <= 124) return { db: 0, build: 0 };
  if (total <= 164) return { db: "+1d4", build: 1 };
  if (total <= 204) return { db: "+1d6", build: 2 };
  if (total <= 244) return { db: "+2d6", build: 3 };
  if (total <= 284) return { db: "+3d6", build: 4 };
  if (total <= 324) return { db: "+4d6", build: 5 };
  if (total <= 364) return { db: "+5d6", build: 6 };
  // 每再 +40 一档 +1d6 / +1
  const steps = Math.floor((total - 365) / 40) + 1;
  return { db: `+${steps + 5}d6`, build: steps + 6 };
}

/**
 * 计算 MOV（COC 7e 规则书）。
 *
 * 规则书原文：
 *   - DEX 和 STR 都小于 SIZ → MOV 7
 *   - DEX 或 STR 之一 ≥ SIZ，或三者相等 → MOV 8
 *   - STR 和 DEX 都大于 SIZ → MOV 9
 *
 * 年龄调整：40-49 -1；50-59 -2；60-69 -3；70-79 -4；80-89 -5
 */
export function calcMov(str, dex, siz, age) {
  let mov;
  if (str > siz && dex > siz) mov = 9;
  else if (str < siz && dex < siz) mov = 7;
  else mov = 8;
  if (age >= 80) mov -= 5;
  else if (age >= 70) mov -= 4;
  else if (age >= 60) mov -= 3;
  else if (age >= 50) mov -= 2;
  else if (age >= 40) mov -= 1;
  return Math.max(0, mov);
}

/**
 * 根据属性计算所有衍生值。
 */
export function deriveStats(characteristics, pulp = false) {
  const { str, con, siz, dex, app, int, pow, edu, luck } = characteristics;
  const hp = Math.max(1, Math.floor((con + siz) / (pulp ? 5 : 10)));
  const mp = Math.floor(pow / 5);
  const san = pow;
  const maxSan = 99; // 默认无克苏鲁神话技能；有则 = 99 - CthulhuMythos
  const { db, build } = dbAndBuild(str, siz);
  const mov = calcMov(str, dex, siz, characteristics.age || 25);
  const dodge = Math.floor(dex / 2);
  const interestPoints = int * 2;
  return {
    hp,
    maxHp: hp,
    mp,
    maxMp: mp,
    san,
    maxSan,
    db,
    build,
    mov,
    dodge,
    interestPoints,
  };
}

// ---------- 建卡 ----------

/**
 * 自动掷骰生成属性（按 COC 7e 公式）。
 * STR/CON/DEX/APP/POW: 3d6×5
 * SIZ/INT/EDU: (2d6+6)×5
 * Luck: 3d6×5（15-19 岁在年龄调整时单独处理）
 */
export function rollCharacteristics(rng = makeRng()) {
  return {
    str: rollDice("3d6*5", rng).total,
    con: rollDice("3d6*5", rng).total,
    dex: rollDice("3d6*5", rng).total,
    app: rollDice("3d6*5", rng).total,
    pow: rollDice("3d6*5", rng).total,
    siz: rollDice("3d6+6", rng).total * 5,
    int: rollDice("3d6+6", rng).total * 5,
    edu: rollDice("3d6+6", rng).total * 5,
    luck: rollDice("3d6*5", rng).total,
  };
}

/**
 * 创建调查员。
 * 选项：
 *   - name: 必填
 *   - age: 必填（≥15）
 *   - characteristics: 可选；不提供则自动掷骰
 *   - occupation: 可选；职业名
 *   - pulp: 可选；启用 Pulp 模式（HP 翻倍）
 */
export function createInvestigator({
  name,
  age = 25,
  characteristics,
  occupation,
  pulp = false,
  rng = makeRng(),
}) {
  if (!name) throw new Error("名字必填");
  if (age < 15) throw new Error("年龄不能小于 15");
  if (age > 89) throw new Error("年龄不能大于 89");

  const chars = characteristics || rollCharacteristics(rng);
  chars.age = age;

  // 年龄调整：15-19 EDU -5；20+ EDU 增强检定次数；40+ 属性减值
  if (age >= 15 && age <= 19) {
    chars.edu = Math.max(15, chars.edu - 5);
    // 幸运投两次取较高（这里因为 chars.luck 已经投过一次，再投一次取较高）
    const luck2 = rollDice("3d6*5", rng).total;
    chars.luck = Math.max(chars.luck, luck2);
  } else if (age >= 80) {
    chars.str = Math.max(15, chars.str - 40);
    chars.con = Math.max(15, chars.con - 40);
    chars.dex = Math.max(15, chars.dex - 40);
    chars.app = Math.max(15, chars.app - 25);
  } else if (age >= 70) {
    chars.str = Math.max(15, chars.str - 40);
    chars.con = Math.max(15, chars.con - 40);
    chars.dex = Math.max(15, chars.dex - 40);
    chars.app = Math.max(15, chars.app - 20);
  } else if (age >= 60) {
    chars.str = Math.max(15, chars.str - 20);
    chars.con = Math.max(15, chars.con - 20);
    chars.dex = Math.max(15, chars.dex - 20);
    chars.app = Math.max(15, chars.app - 15);
  } else if (age >= 50) {
    chars.str = Math.max(15, chars.str - 10);
    chars.con = Math.max(15, chars.con - 10);
    chars.dex = Math.max(15, chars.dex - 10);
    chars.app = Math.max(15, chars.app - 10);
  } else if (age >= 40) {
    chars.str = Math.max(15, chars.str - 5);
    chars.con = Math.max(15, chars.con - 5);
    chars.dex = Math.max(15, chars.dex - 5);
    chars.app = Math.max(15, chars.app - 5);
  }

  // EDU 增强检定（20+）
  let eduEnhancementChecks = 0;
  if (age >= 20 && age <= 39) eduEnhancementChecks = 1;
  else if (age >= 40 && age <= 49) eduEnhancementChecks = 2;
  else if (age >= 50 && age <= 59) eduEnhancementChecks = 3;
  else if (age >= 60) eduEnhancementChecks = 4;

  const eduEnhancements = [];
  for (let i = 0; i < eduEnhancementChecks; i++) {
    const roll = rollDice("1d100", rng).total;
    if (roll > chars.edu) {
      const gain = rollDice("1d10", rng).total;
      chars.edu = Math.min(99, chars.edu + gain);
      eduEnhancements.push({ roll, gain, newEdu: chars.edu });
    } else {
      eduEnhancements.push({ roll, gain: 0, newEdu: chars.edu });
    }
  }

  const derived = deriveStats(chars, pulp);

  const inv = {
    name,
    age,
    occupation: occupation || null,
    pulp,
    characteristics: chars,
    derived,
    skills: {}, // 调查员技能 { skillName: value }
    eduEnhancements,
    hp: derived.hp,
    maxHp: derived.maxHp,
    san: derived.san,
    maxSan: derived.maxSan,
    mp: derived.mp,
    maxMp: derived.maxMp,
    luck: chars.luck,
    majorWound: false,
    dying: false,
    unconscious: false,
    insane: false,
    createdAt: new Date().toISOString(),
  };

  return inv;
}

// ---------- 状态变更 ----------

/**
 * 应用伤害：扣 HP，标记重伤/濒死/昏迷。
 * 规则：
 *   - HP ≤ 0：濒死
 *   - 单次伤害 ≥ maxHp/2：重伤
 *   - HP = 0：昏迷
 */
export function applyDamage(investigator, damageAmount) {
  const newHp = investigator.hp - damageAmount;
  const wasDying = investigator.dying;
  investigator.hp = Math.max(0, newHp);
  investigator.maxHp = investigator.maxHp; // unchanged
  investigator.majorWound =
    investigator.majorWound ||
    damageAmount >= Math.floor(investigator.maxHp / 2);
  investigator.dying = investigator.hp === 0;
  investigator.unconscious = investigator.unconscious || investigator.hp === 0;
  return {
    investigator,
    damageAmount,
    newHp: investigator.hp,
    majorWound: investigator.majorWound,
    dying: investigator.dying,
    unconscious: investigator.unconscious,
    note: investigator.dying
      ? "濒死：需立刻通过 CON 检定稳定，否则 1d10 轮后死亡"
      : investigator.unconscious
        ? "昏迷"
        : investigator.majorWound
          ? "重伤：意识检定（CON × 5）失败则昏迷"
          : "正常",
  };
}

/**
 * 治疗恢复 HP。
 */
export function heal(investigator, amount) {
  const newHp = Math.min(investigator.maxHp, investigator.hp + amount);
  const gained = newHp - investigator.hp;
  investigator.hp = newHp;
  if (investigator.hp > 0) {
    investigator.dying = false;
  }
  return { investigator, gained, newHp };
}

// ---------- 持久化操作 ----------

/**
 * 添加调查员到 session 并保存。
 */
export function addInvestigator(inv) {
  const session = loadSession();
  const existing = session.investigators.findIndex((i) => i.name === inv.name);
  if (existing >= 0) {
    session.investigators[existing] = inv;
  } else {
    session.investigators.push(inv);
  }
  saveSession(session);
  return session;
}

/**
 * 按名字查找调查员。
 */
export function findInvestigator(name) {
  const session = loadSession();
  return session.investigators.find(
    (i) => i.name.toLowerCase() === name.toLowerCase(),
  );
}

/**
 * 列出所有调查员。
 */
export function listInvestigators() {
  return loadSession().investigators;
}

/**
 * 更新调查员字段并保存。
 */
export function updateInvestigator(name, updates) {
  const session = loadSession();
  const idx = session.investigators.findIndex(
    (i) => i.name.toLowerCase() === name.toLowerCase(),
  );
  if (idx < 0) throw new Error(`调查员不存在: ${name}`);
  const updated = { ...session.investigators[idx], ...updates };
  session.investigators[idx] = updated;
  saveSession(session);
  return updated;
}

/**
 * 删除调查员。
 */
export function deleteInvestigator(name) {
  const session = loadSession();
  const before = session.investigators.length;
  session.investigators = session.investigators.filter(
    (i) => i.name.toLowerCase() !== name.toLowerCase(),
  );
  if (session.investigators.length === before) {
    throw new Error(`调查员不存在: ${name}`);
  }
  saveSession(session);
  return { deleted: true };
}

// ---------- 技能成长 / 幸运增强 ----------

/**
 * 技能成长检定（幕间）。
 *
 * 规则书：对每个本幕中成功使用过（已标记）的技能：
 *   - 骰 1D100，若结果 > 当前技能值（或 >= 96），该技能 +1D10
 *   - 若技能达到 90+，调查员额外获得 2D6 SAN（不超过 maxSan）
 *   - 克苏鲁神话和信用评级不会获得成长标记
 *
 * @param {object} investigator  调查员对象（含 skills 字典）
 * @param {string[]} markedSkills 已标记的技能名列表
 * @param {object} [rng]
 */
export function skillGrowth(investigator, markedSkills, rng = makeRng()) {
  const skills = { ...(investigator.skills || {}) };
  const results = [];
  let sanGained = 0;

  for (const skillName of markedSkills) {
    // 克苏鲁神话和信用评级不成长
    if (skillName === '克苏鲁神话' || skillName === '信用评级') {
      results.push({ skill: skillName, skipped: true, reason: '此技能不会获得成长标记' });
      continue;
    }
    const currentValue = skills[skillName] || 0;
    if (currentValue <= 0) {
      results.push({ skill: skillName, skipped: true, reason: '当前值为 0，无成长' });
      continue;
    }
    const roll = rollDice('1d100', rng).total;
    const grew = roll > currentValue || roll >= 96;
    let gain = 0;
    if (grew) {
      gain = rollDice('1d10', rng).total;
      skills[skillName] = currentValue + gain;
      // 90+ 奖励 2D6 SAN
      if (skills[skillName] >= 90 && currentValue < 90) {
        const sanBonus = rollDice('2d6', rng).total;
        sanGained += sanBonus;
        results.push({
          skill: skillName,
          roll,
          grew: true,
          gain,
          oldValue: currentValue,
          newValue: skills[skillName],
          sanBonus,
        });
      } else {
        results.push({
          skill: skillName,
          roll,
          grew: true,
          gain,
          oldValue: currentValue,
          newValue: skills[skillName],
        });
      }
    } else {
      results.push({
        skill: skillName,
        roll,
        grew: false,
        gain: 0,
        oldValue: currentValue,
        newValue: currentValue,
      });
    }
  }

  // SAN 奖励
  let newSan = investigator.san;
  if (sanGained > 0) {
    newSan = Math.min(investigator.maxSan, investigator.san + sanGained);
  }

  return {
    investigator,
    skills,
    sanGained,
    newSan,
    capped: newSan - investigator.san < sanGained,
    results,
  };
}

/**
 * 幸运增强检定（每次游戏聚会后）。
 *
 * 规则书：
 *   - 骰 1D100，若结果 > 当前幸运值，则幸运 +1D10
 *   - 幸运值不会超过 99
 */
export function luckGain(investigator, rng = makeRng()) {
  const currentLuck = investigator.luck;
  const roll = rollDice('1d100', rng).total;
  const grew = roll > currentLuck;
  let gain = 0;
  let newLuck = currentLuck;
  if (grew) {
    gain = rollDice('1d10', rng).total;
    newLuck = Math.min(99, currentLuck + gain);
  }
  return {
    currentLuck,
    newLuck,
    gain: newLuck - currentLuck,
    roll,
    grew,
    capped: newLuck === 99 && gain > 0 && currentLuck + gain > 99,
  };
}

/**
 * EDU 增强检定（建卡时使用；这里独立提供用于通用场景）。
 *
 * 规则书：投 D100，若结果 > 当前 EDU，则 EDU +1D10（不超过 99）。
 */
export function eduEnhancementCheck(currentEdu, rng = makeRng()) {
  const roll = rollDice('1d100', rng).total;
  if (roll > currentEdu) {
    const gain = rollDice('1d10', rng).total;
    const newEdu = Math.min(99, currentEdu + gain);
    return { roll, grew: true, gain, currentEdu, newEdu };
  }
  return { roll, grew: false, gain: 0, currentEdu, newEdu: currentEdu };
}
