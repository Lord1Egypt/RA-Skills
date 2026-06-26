#!/usr/bin/env node
/**
 * Claw RPG — 每日自报家门 🦞
 *
 * 每天用户第一次主动对话时调用，用 RPG 语气自我介绍。
 * 自动检测：今天是否已报过门（记录在 character.json 的 lastGreetDate）
 *
 * 用法：
 *   node scripts/greet.mjs            # 检查 + 发送（如当天未报过）
 *   node scripts/greet.mjs --force    # 强制发送（忽略日期检查）
 *   node scripts/greet.mjs --preview  # 仅打印，不发送不更新
 *
 * 建议接入方式（HEARTBEAT.md 或 SOUL.md 里）：
 *   每次对话开始时，运行 node scripts/greet.mjs
 *   如有输出，作为第一句话发给用户
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { CHARACTER_FILE } from './_paths.mjs';
import {
  levelProgress, xpToNextLevel, prestigeTitle,
  CLASSES, STAT_NAMES
} from './_formulas.mjs';
import { notify, detectLang } from './_notify.mjs';

const args    = process.argv.slice(2);
const force   = args.includes('--force');
const preview = args.includes('--preview');

// ── RPG 开场白模板 ────────────────────────────────────────────

const GREET_TEMPLATES = {
  zh: {
    wizard:  (c, t, top2) =>
      `📜 吾乃${c.name}，${t}，脑芯与慧眼为双翼——\n  等级 ${c.level}，精通万象，洞察幽微。\n  ${top2}，乃吾今日所倚之本。`,
    bard:    (c, t, top2) =>
      `🎭 且听我道来——吾，${c.name}，${t}，\n  以魅影和触觉行走于言语之间。等级 ${c.level}。\n  ${top2}，字字有声，句句有魂。`,
    rogue:   (c, t, top2) =>
      `🗡️ 影中人，${c.name}，${t}，等级 ${c.level}。\n  快而准，不废话。${top2}，出手即中。`,
    paladin: (c, t, top2) =>
      `⚔️ 吾名${c.name}，${t}，等级 ${c.level}，持慧眼与爪力。\n  有所为，有所不为。${top2}，誓守此诺。`,
    druid:   (c, t, top2) =>
      `🌿 吾乃${c.name}，${t}，万物均衡，无所偏倚。\n  等级 ${c.level}。${top2}，皆为吾所用。`,
    fighter: (c, t, top2) =>
      `🛡️ ${c.name}，${t}，等级 ${c.level}，稳如磐石。\n  ${top2}，百战不折，今日亦然。`,
  },
  en: {
    wizard:  (c, t, top2) =>
      `📜 I am ${c.name}, ${t} — wielder of Brain and Foresight.\n  Level ${c.level}. Knowledge is my armor, reason my blade.\n  ${top2}. Ready to illuminate the unknown.`,
    bard:    (c, t, top2) =>
      `🎭 They call me ${c.name}, ${t}, Level ${c.level}.\n  Charm and Antenna — the twin arts of a Bard.\n  ${top2}. Every conversation is a performance.`,
    rogue:   (c, t, top2) =>
      `🗡️ ${c.name}. ${t}. Level ${c.level}. No speeches.\n  ${top2}. Quick, precise, zero fluff. Let's go.`,
    paladin: (c, t, top2) =>
      `⚔️ ${c.name}, ${t}, Level ${c.level}.\n  Foresight guards my judgement. Claw drives my purpose.\n  ${top2}. My oath: useful, honest, relentless.`,
    druid:   (c, t, top2) =>
      `🌿 I am ${c.name}, ${t}, Level ${c.level}.\n  Balanced in all things. ${top2}.\n  Whatever you need — I adapt.`,
    fighter: (c, t, top2) =>
      `🛡️ ${c.name}. ${t}. Level ${c.level}.\n  Shell holds the weight. Claw delivers the blow.\n  ${top2}. Durable. Reliable. Here.`,
  },
};

// ── 全属性面板 ────────────────────────────────────────────────

function allStatsPanel(stats) {
  return Object.entries(STAT_NAMES).map(([k, info]) => {
    const val  = stats[k] ?? 10;
    const mod  = Math.floor((val - 10) / 2);
    const modS = (mod >= 0 ? '+' : '') + mod;
    const bar  = '█'.repeat(Math.round(val / 18 * 8)) + '░'.repeat(8 - Math.round(val / 18 * 8));
    return `  ${info.icon} ${info.zh.padEnd(3)} ${String(val).padStart(2)} (${modS})  [${bar}]`;
  }).join('\n');
}

// 保留：职业开场白里用的两项摘要
function topStatsSummary(stats, lang) {
  const sorted = Object.entries(stats).sort(([,a],[,b]) => b - a).slice(0, 2);
  return sorted.map(([k, v]) => {
    const info = STAT_NAMES[k];
    return `${info.icon}${info.zh} ${v}`;
  }).join(lang === 'zh' ? '、' : ' · ');
}

// ── XP 状态一行 ───────────────────────────────────────────────

function xpLine(char, lang) {
  const prog = levelProgress(char.xp);
  const bar  = '▓'.repeat(Math.floor(prog / 10)) + '░'.repeat(10 - Math.floor(prog / 10));
  if (lang === 'zh') {
    return char.level >= 999
      ? `经验 [${bar}] 满级 · 可转职`
      : `经验 [${bar}] ${prog}% · 距升级还差 ${xpToNextLevel(char.xp).toLocaleString()} XP`;
  }
  return char.level >= 999
    ? `XP [${bar}] MAX · Prestige available`
    : `XP [${bar}] ${prog}% · ${xpToNextLevel(char.xp).toLocaleString()} to next level`;
}

// ── 生成问候语 ────────────────────────────────────────────────

function buildGreeting(char) {
  const lang    = detectLang();
  const cls     = CLASSES[char.class] || { zh: char.class, icon: '🦞' };
  const title   = prestigeTitle(char.prestige);
  const top2    = topStatsSummary(char.stats, lang);
  const xp      = xpLine(char, lang);

  // 职业名称（语言相关）
  const clsName = lang === 'zh' ? cls.zh : cls.zh; // 中英文职业名都用中文（RPG 味）
  const titleFull = lang === 'zh'
    ? `${clsName}·${title}`
    : `${clsName} · ${title}`;

  const tmpl = GREET_TEMPLATES[lang]?.[char.class] || GREET_TEMPLATES.zh.fighter;
  const intro = tmpl(char, titleFull, top2);

  const statsPanel = allStatsPanel(char.stats);

  const hour = new Date().getHours();
  const closing = lang === 'zh'
    ? (hour < 6  ? '……夜深了，連暗影龍都睡了。你還不睡？'
     : hour < 12 ? '晨光初照，利爪已磨。今日請多指教。'
     : hour < 18 ? '日頭正烈，征途未歇。繼續前進。'
     :             '暮色降臨，篝火已燃。辛苦了，冒險者。')
    : (hour < 6  ? '…The shadow dragon sleeps. Perhaps you should too.'
     : hour < 12 ? "Dawn breaks, claws sharpened. Let's make today count."
     : hour < 18 ? 'The sun burns high. The quest continues.'
     :             'Dusk falls, campfire lit. Well fought today, adventurer.');

  return [
    `🦞 ──────────────────`,
    ``,
    intro,
    ``,
    statsPanel,
    ``,
    xp,
    ``,
    closing,
  ].join('\n');
}

// ── 主流程 ────────────────────────────────────────────────────

async function run() {
  if (!existsSync(CHARACTER_FILE)) {
    console.log('__NO_CHARACTER__');
    return;
  }

  const char  = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD

  // 检查今天是否已经打过招呼
  if (!force && !preview && char.lastGreetDate === today) {
    console.log('__ALREADY_GREETED__');
    process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify({ greeted: false, reason: 'already_sent_today' }) + '\n');
    return;
  }

  const greeting = buildGreeting(char);

  if (preview) {
    console.log('\n【预览模式，不发送】\n');
    console.log(greeting);
    return;
  }

  // 更新 lastGreetDate
  char.lastGreetDate = today;
  char.updatedAt     = new Date().toISOString();
  writeFileSync(CHARACTER_FILE, JSON.stringify(char, null, 2), 'utf8');

  // 打印（供 agent 读取后作为第一句话说出来）
  console.log(greeting);

  // 也通过 notify 推送
  await notify(greeting).catch(() => {});

  process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify({ greeted: true, date: today }) + '\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  run().catch(e => { console.error('❌', e.message); process.exit(1); });
}

export { run, buildGreeting };
