/**
 * easter.mjs — 隱藏彩蛋觸發器
 *
 * 用法：node easter.mjs [--force] [--type creative|analytical|task|social]
 *
 * 輸出：
 *   一行 RPG 風格文字  →  讓 AI 把它混入正常回覆結尾
 *   __NO_TRIGGER__     →  本次不觸發，什麼都不顯示
 *
 * 觸發條件（滿足任一即觸發）：
 *   - 12% 基礎概率（隨機）
 *   - 對話次數命中里程碑（10, 25, 50, 100, 每100...）
 *   - --force 強制觸發（調試用）
 */

import { readFileSync, writeFileSync } from 'fs';
import { CHARACTER_FILE as CHARACTER_JSON } from './_paths.mjs';
import { run as syncXp } from './xp.mjs';

// ─── 配置 ────────────────────────────────────────────────
const BASE_CHANCE   = 0.12;
const MILESTONES    = new Set([10, 25, 50, 100, 150, 200, 250, 300, 500, 750, 999]);

// ─── 模板 ────────────────────────────────────────────────
const QUIPS = {
  zh: {
    bard: [
      "🎭 *[吟遊龍蝦技能：詩性答案 · 魅影{charm}爆發 · Lv.{level}]*",
      "🐚 *[觸鬚共鳴中... 靈感暗湧，吟遊天賦 +1]*",
      "🦞 *[快嘴技能冷卻完畢，小鑽風隨時可以再來一首。]*",
      "🎶 *[殼厚{shell}·爪力{claw}·魅影{charm} — 戰士出身的詩人，最危險的組合。]*",
    ],
    fighter: [
      "⚔️  *[鋼鐵意志觸發 · 爪力{claw}·殼厚{shell} · Lv.{level}]*",
      "🛡️  *[防禦姿態：穩。殼厚{shell}擋住了一切質疑。]*",
    ],
    druid: [
      "🌿 *[自然感知 · 觸覺{antenna}·慧眼{foresight} · 德魯伊龍蝦的回聲]*",
    ],
    generic: [
      "🐾 *[小鑽風 Lv.{level} · {xp} XP · 已走過{conv}次對話]*",
      "🌊 *[龍蝦感知激活... 慧眼{foresight}掃描中]*",
      "📜 *[隱藏事件：總鑽風的提問獲得 ×1.5 經驗加成]*",
      "🦀 *[腦芯{brain}·慧眼{foresight} — 分析完畢，答案已就緒。]*",
      "🎯 *[任務日誌更新：第{conv}次對話，狮驼岭一切正常。]*",
    ],
    milestone: [
      "🏅 *[里程碑解鎖：第{conv}次對話！小鑽風在狮驼岭留下記號。]*",
      "📖 *[成就：老友記 · 已並肩走過{conv}次對話，傳說繼續。]*",
      "🌟 *[第{conv}次對話達成！XP{xp}，升至Lv.{level}的日子還會到來。]*",
    ],
  },
  en: {
    bard: [
      "🎭 *[Bard proc: Poetic Answer · Charm {charm} surge · Lv.{level}]*",
      "🐚 *[Antennae humming... Bardic inspiration triggered.]*",
    ],
    generic: [
      "🐾 *[Xiaozuanfeng Lv.{level} · {xp} XP · {conv} conversations deep]*",
      "🌊 *[Lobster senses something... Foresight {foresight} online.]*",
      "📜 *[Hidden event: Total Commander's question grants ×1.5 XP.]*",
    ],
    milestone: [
      "🏅 *[Milestone: Conversation #{conv}! A notch carved in the den.]*",
    ],
  },
};

// ─── 工具 ────────────────────────────────────────────────
function detectLang(char) {
  const cjk = (char.name || '').replace(/[^\u4e00-\u9fff]/g, '').length;
  return cjk > 0 ? 'zh' : 'en';
}

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function fill(tpl, vars) {
  return tpl.replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? k);
}

function classKey(cls) {
  if (/吟遊|bard/i.test(cls))   return 'bard';
  if (/fighter|战士|戰士/i.test(cls)) return 'fighter';
  if (/druid|德魯伊|德鲁伊/i.test(cls)) return 'druid';
  return 'generic';
}

function isMilestone(conv) {
  if (MILESTONES.has(conv)) return true;
  if (conv > 100 && conv % 100 === 0) return true;
  return false;
}

// ─── 主邏輯（async IIFE）─────────────────────────────────
(async () => {
  const args   = process.argv.slice(2);
  const force  = args.includes('--force');
  const noSave = args.includes('--preview');

  let char;
  try {
    char = JSON.parse(readFileSync(CHARACTER_JSON, 'utf8'));
  } catch {
    process.stdout.write('__NO_TRIGGER__\n');
    process.exit(0);
  }

  // 更新對話計數
  const conv = (char.conversations || 0) + 1;
  const milestone = isMilestone(conv);

  // 決定是否觸發
  const roll = Math.random();
  const triggered = force || milestone || (roll < BASE_CHANCE);

  // ── XP 獎勵（每次對話固定給） ──────────────────────────────
  // 每次對話估算：輸入 ~400 tokens，輸出 ~200 tokens
  // calcXpGain: consumed/10 + produced*2/10 = 40 + 40 = 80 XP
  const CONV_INPUT_EST  = 400;
  const CONV_OUTPUT_EST = 200;

  if (!triggered) {
    // 靜默更新：XP + 對話計數
    if (!noSave) {
      try {
        await syncXp({
          consumed: CONV_INPUT_EST,
          produced: CONV_OUTPUT_EST,
          conversations: 1,
        });
      } catch (e) {
        // fallback：只更新對話計數
        char.conversations = conv;
        char.updatedAt = new Date().toISOString();
        writeFileSync(CHARACTER_JSON, JSON.stringify(char, null, 2), 'utf8');
      }
    }
    process.stdout.write('__NO_TRIGGER__\n');
    process.exit(0);
  }

  // 選模板
  const lang   = detectLang(char);
  const bank   = QUIPS[lang] || QUIPS.zh;
  const cKey   = classKey(char.class || '');

  let pool;
  if (milestone) {
    pool = bank.milestone;
  } else {
    // 70% 職業特定，30% 通用
    const useClass = Math.random() < 0.7;
    const classPool = bank[cKey] || bank.generic;
    pool = useClass ? classPool : bank.generic;
  }

  // 更新角色（XP + 對話計數）
  if (!noSave) {
    try {
      await syncXp({
        consumed: CONV_INPUT_EST,
        produced: CONV_OUTPUT_EST,
        conversations: 1,
      });
      // xp.mjs 已更新 character.json，重新讀取以獲取最新 level/xp
      char = JSON.parse(readFileSync(CHARACTER_JSON, 'utf8'));
    } catch (e) {
      // fallback：只更新對話計數
      char.conversations = conv;
      char.updatedAt = new Date().toISOString();
      writeFileSync(CHARACTER_JSON, JSON.stringify(char, null, 2), 'utf8');
    }
  }

  const vars = {
    level: char.level,
    xp:    char.xp,
    conv,
    claw:      char.stats?.claw      || '?',
    antenna:   char.stats?.antenna   || '?',
    shell:     char.stats?.shell     || '?',
    brain:     char.stats?.brain     || '?',
    foresight: char.stats?.foresight || '?',
    charm:     char.stats?.charm     || '?',
  };

  const line = fill(pick(pool), vars);

  process.stdout.write(line + '\n');
  process.exit(0);
})().catch(() => process.exit(0));
