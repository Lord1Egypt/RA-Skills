/**
 * Claw RPG — 通知助手
 * 通过 OpenClaw gateway 推送 Telegram 消息
 * 所有重要事件（升级 / 职业变化 / 转职）统一走这里
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { SKILL_ROOT } from './_paths.mjs';

function loadGateway() {
  const paths = [
    join(process.env.USERPROFILE || '', '.openclaw', 'openclaw.json'),
    join(process.env.HOME || '', '.openclaw', 'openclaw.json'),
  ];
  for (const p of paths) {
    if (existsSync(p)) {
      try { return JSON.parse(readFileSync(p, 'utf8')); } catch {}
    }
  }
  return null;
}

function loadChatId() {
  const cfg = join(SKILL_ROOT, 'config.json');
  if (existsSync(cfg)) {
    try { return JSON.parse(readFileSync(cfg, 'utf8'))?.telegram_chat_id || ''; } catch {}
  }
  return '';
}

/**
 * 推送通知
 * @param {string} text - 消息正文（支持 emoji）
 * @returns {Promise<boolean>} 是否发送成功
 */
export async function notify(text) {
  const gw     = loadGateway();
  const chatId = loadChatId();

  if (!gw || !chatId) return false; // 未配置，静默跳过

  const token = gw?.gateway?.auth?.token;
  const port  = gw?.gateway?.port || 18789;

  try {
    const res = await fetch(`http://localhost:${port}/tools/invoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        tool: 'message',
        args: { action: 'send', channel: 'telegram', target: chatId, message: text },
      }),
    });
    return res.ok;
  } catch {
    return false;
  }
}

// ── 语言 & 吐槽库 ─────────────────────────────────────────────

const QUIPS = {
  zh: {
    levelUp: [
      '升级比谈恋爱容易多了——至少这里的进度条不会说分手。',
      '好耶，又升级了。你已经比你的简历强了。',
      '恭喜，距离退休又远了一步。',
      '这么努力，你爸妈知道吗？',
      '升级了！不过你的工资还是原地踏步。',
      '又升一级，感动了吗？感动就对了，感动完继续干活。',
      '人类升职要年会打分，你升级只需要闲聊，命真好。',
    ],
    classChange: [
      '职业转变了，上辈子的技能树白点了。',
      '换职业？这就是传说中的"裸辞"。',
      '新职业解锁！出门记得更新一下名片。',
      '恭喜，你有了一个更酷但依然解释不清楚的头衔。',
      '转职成功——属性确实变了，但你妈还是会问你什么时候找对象。',
    ],
    prestige: [
      '满级转职，证明你的核心技能是"重复劳动并乐在其中"。',
      '转职了，但你还是那个你，只是贵了 10%。',
      '又从零开始？这是成长，不是倒退……应该吧。',
      '传说中的轮回你触发了！恭喜，意义由你自己定义。',
      '满级转职，这是信仰，不是游戏。',
    ],
    maxLevel: [
      'Lv.999！建议申请吉尼斯世界纪录。',
      '满级了。现在可以享受生活了，但你不会的，对吧。',
      '你打满级了，但人生 DLC 还没开始呢。',
      '恭喜满级！现在有资格嘲笑低等级了——但你不会，因为你是好龙虾。',
    ],
    statUp: [
      '属性涨了，但你还是得干活。',
      '成长是真实的，加班也是真实的。',
      '又强了一点点。积少成多，量变引质变，哲学家说的。',
      '这一点属性是用多少对话堆出来的，你心里有数吗？',
      '涨了！去跟别的龙虾比划比划。',
    ],
  },
  en: {
    levelUp: [
      "Leveled up! Your real-world salary, however, remains unchanged.",
      "Congrats! You're now slightly less mediocre than before.",
      "Another level! Your parents would be proud — if they knew what this meant.",
      "Ding! You've officially spent too much time talking to an AI.",
      "Level up! Still not enough to impress anyone at a party, but hey.",
      "Progress! The bar was low, but you cleared it. Repeatedly.",
    ],
    classChange: [
      "Class changed! Your old skills are now worthless. Relatable.",
      "New class unlocked. Time to update your LinkedIn, apparently.",
      "Career pivot! Very brave. Very unhinged. We respect it.",
      "Class changed. Your identity crisis is now officially documented.",
      "New class! You didn't choose it — your stats did. Accountability moment.",
    ],
    prestige: [
      "Prestiged! Proof you enjoy voluntary suffering.",
      "Back to level 1, but fancier. That's basically your whole career arc.",
      "Prestige complete! You've earned 10% more ego and 0% more sleep.",
      "You reset on purpose. That's either enlightenment or a cry for help.",
    ],
    maxLevel: [
      "Level 999! Seek help. Or don't. You're clearly self-sufficient.",
      "Max level! You've peaked. It's all downhill from here. Congrats!",
      "Lv.999 achieved. The game is over. Real life starts now. (Good luck.)",
      "You hit max level. The developers didn't expect anyone to get here. Neither did we.",
    ],
    statUp: [
      "Stat increased. You're still on the clock though.",
      "Growth detected. Imperceptible to others. Monumental to you.",
      "That stat didn't grow by accident. It grew by repetition. Respect.",
      "One point up. One step closer to being insufferable about it.",
      "Stronger. Marginally. But it counts.",
    ],
  },
};

export function detectLang() {
  try {
    const ws = join(process.env.USERPROFILE || process.env.HOME || '', '.openclaw', 'workspace');
    const files = ['MEMORY.md', 'IDENTITY.md', 'USER.md', 'SOUL.md'];
    let totalChars = 0, cjkChars = 0;
    for (const f of files) {
      const fp = join(ws, f);
      if (!existsSync(fp)) continue;
      const text = readFileSync(fp, 'utf8');
      totalChars += text.length;
      cjkChars += (text.match(/[\u4e00-\u9fff\u3040-\u30ff]/g) || []).length;
    }
    return cjkChars / Math.max(totalChars, 1) > 0.05 ? 'zh' : 'en';
  } catch { return 'zh'; }
}

function quip(category) {
  const lang  = detectLang();
  const pool  = QUIPS[lang]?.[category] || QUIPS.zh[category] || [];
  return pool[Math.floor(Math.random() * pool.length)] || '';
}

// ── 事件模板 ──────────────────────────────────────────────────

/** 升级通知 */
export function msgLevelUp(char, oldLevel, newLevel) {
  const multi = newLevel - oldLevel;
  return [
    `⚔️ 升级！`,
    ``,
    `🦞 ${char.name}`,
    `Lv.${oldLevel} → Lv.${newLevel}${multi > 1 ? `（连升 ${multi} 级！）` : ''}`,
    `当前 XP：${char.xp.toLocaleString()}`,
    ``,
    `_${quip('levelUp')}_`,
  ].join('\n');
}

/** 职业变化通知 */
export function msgClassChange(char, _oldClass, _newClass, oldClassZh, newClassZh, changedStat, statIcon) {
  return [
    `🔄 职业转变！`,
    ``,
    `🦞 ${char.name}`,
    `${statIcon} ${changedStat}能力显著提升`,
    `${oldClassZh} → ${newClassZh}`,
    `新职业技能已解锁，继续冒险！`,
    ``,
    `_${quip('classChange')}_`,
  ].join('\n');
}

/** 转职通知 */
export function msgPrestige(char, newPrestige, title) {
  return [
    `🌟 传说时刻——转职！`,
    ``,
    `🦞 ${char.name} 完成第 ${newPrestige} 次转职`,
    `称号：${title}`,
    `全属性永久 +10%`,
    `等级归一，再铸传奇！`,
    ``,
    `_${quip('prestige')}_`,
  ].join('\n');
}

/** 属性成长通知 */
export function msgStatUp(char, statKey, oldVal, newVal) {
  const STAT_NAMES = {
    claw:      { zh: '爪力', icon: '🦀' },
    antenna:   { zh: '触觉', icon: '📡' },
    shell:     { zh: '殼厚', icon: '🐚' },
    brain:     { zh: '脑芯', icon: '🧠' },
    foresight: { zh: '慧眼', icon: '👁️' },
    charm:     { zh: '魅影', icon: '✨' },
  };
  const info = STAT_NAMES[statKey] || { zh: statKey, icon: '📊' };
  return [
    `${info.icon} 属性成长！`,
    ``,
    `🦞 ${char.name}`,
    `${info.zh}  ${oldVal} → ${newVal}`,
    ``,
    `_${quip('statUp')}_`,
  ].join('\n');
}

/** 满级通知 */
export function msgMaxLevel(char) {
  return [
    `🏆 满级！`,
    ``,
    `🦞 ${char.name} 到达 Lv.999！`,
    `运行 node scripts/levelup.mjs --prestige 执行转职`,
    ``,
    `_${quip('maxLevel')}_`,
  ].join('\n');
}

// ── 事件驱动通知 ─────────────────────────────────────────────

const EVENT_MSGS = {
  zh: {
    bigQuest: [
      '⚔️ 副本已通關。耗時漫長，傷痕累累，但你站著出來了。',
      '📜 漫漫長夜，一場硬仗剛剛落幕。',
      '🏰 巨型副本清場。你的爪痕留在了這片土地上。',
    ],
    speedClear: [
      '⚡ 三招制敵。精準，高效，不廢話。傳說級效率。',
    ],
    return2: [
      '📡 訊號恢復。傳令兵已跑斷兩雙靴子。',
    ],
    return4: [
      '🕯️ 七日未見，有人說你退出江湖了。顯然謠言。',
    ],
    return7: [
      '⚰️ ……你回來了。我們都以為你羽化登仙了。歡迎回到獅駝嶺。',
    ],
    streak3:  ['🔥 連續上線 3 天！這不是習慣，是修行。'],
    streak7:  ['🔥 連續上線 7 天！七日不輟，鐵杵成針。'],
    streak14: ['🔥 連續上線 14 天！半月之約，風雨無阻。你是真的狠。'],
    streak30: ['🔥 連續上線 30 天！一整個月。你已經不是普通冒險者了，你是傳說。'],
    xpMilestone: {
      10000:  '🏅 XP 突破 10,000！新手村畢業了。',
      50000:  '🏅 XP 突破 50,000！你在這片大陸已小有名氣。',
      100000: '🏅 XP 突破 100,000！十萬經驗，百戰老兵。',
      500000: '🏅 XP 突破 500,000！半百萬。史書該為你留一頁了。',
    },
    convMilestone: {
      100:  '💬 對話突破 100 次！從陌生到熟悉，路還很長。',
      500:  '💬 對話突破 500 次！五百次交鋒，默契已成。',
      1000: '💬 對話突破 1,000 次！千言萬語，盡在不言中。',
      5000: '💬 對話突破 5,000 次！五千回合，你我已是老戰友。',
    },
    nightOwl: [
      '🌙 深夜了還在戰鬥？夜行者，注意別驚動暗影龍。',
      '🦉 子時已過，你還在磨劍。真·肝帝。',
      '🌃 萬籟俱寂，唯有你的鍵盤聲迴盪在副本裡。',
    ],
    silentOutput: [
      '🗿 你今日一言未發，卻讓吾輸出萬字。沉默的指揮官，最可怕。',
    ],
  },
  en: {
    bigQuest: [
      '⚔️ Dungeon cleared. Long, brutal, but you walked out standing.',
      '📜 A long night, a hard battle — now behind you.',
      '🏰 Mega dungeon swept clean. Your claw marks remain on this land.',
    ],
    speedClear: [
      '⚡ Three moves. Precise. Efficient. No wasted words. Legendary speed.',
    ],
    return2: [
      '📡 Signal restored. The messenger wore out two pairs of boots.',
    ],
    return4: [
      '🕯️ Gone for days. Some said you left the game. Clearly a rumor.',
    ],
    return7: [
      '⚰️ …You\'re back. We all thought you ascended. Welcome home.',
    ],
    streak3:  ['🔥 3-day streak! This isn\'t habit — it\'s discipline.'],
    streak7:  ['🔥 7-day streak! An iron will, forged in daily fire.'],
    streak14: ['🔥 14-day streak! Half a month. Rain or shine. Relentless.'],
    streak30: ['🔥 30-day streak! A full month. You\'re no longer an adventurer — you\'re a legend.'],
    xpMilestone: {
      10000:  '🏅 XP crossed 10,000! Tutorial complete.',
      50000:  '🏅 XP crossed 50,000! Your name echoes across the land.',
      100000: '🏅 XP crossed 100,000! A hundred thousand. Battle-hardened veteran.',
      500000: '🏅 XP crossed 500,000! Half a million. The chronicles await your page.',
    },
    convMilestone: {
      100:  '💬 100 conversations! From strangers to comrades.',
      500:  '💬 500 conversations! Five hundred exchanges. Synergy achieved.',
      1000: '💬 1,000 conversations! A thousand words — we understand each other.',
      5000: '💬 5,000 conversations! Five thousand rounds. We are old war buddies now.',
    },
    nightOwl: [
      '🌙 Still fighting at this hour? Night walker, beware the shadow dragon.',
      '🦉 Past midnight, still sharpening your blade. True dedication.',
      '🌃 The world sleeps. Only your keystrokes echo through the dungeon.',
    ],
    silentOutput: [
      '🗿 You said nothing today, yet commanded ten thousand words from me. The silent commander — most fearsome.',
    ],
  },
};

function pickEvent(key) {
  const lang = detectLang();
  const pool = EVENT_MSGS[lang]?.[key] || EVENT_MSGS.zh[key] || [];
  if (Array.isArray(pool)) return pool[Math.floor(Math.random() * pool.length)] || '';
  return '';
}

/** 大副本完成 */
export function msgBigQuest(char, gained) {
  return `${pickEvent('bigQuest')}\n\n🦞 ${char.name}  本次 XP +${gained.toLocaleString()}`;
}

/** 速通 */
export function msgSpeedClear(char, gained) {
  return `${pickEvent('speedClear')}\n\n🦞 ${char.name}  XP +${gained.toLocaleString()}`;
}

/** 長期回歸 */
export function msgReturn(char, days) {
  const key = days >= 7 ? 'return7' : days >= 4 ? 'return4' : 'return2';
  return `${pickEvent(key)}\n\n🦞 ${char.name}  離線 ${days} 天`;
}

/** 連續在線 streak */
export function msgStreak(char, streak) {
  const key = `streak${streak}`;
  const lang = detectLang();
  const pool = EVENT_MSGS[lang]?.[key] || EVENT_MSGS.zh[key] || [];
  const text = Array.isArray(pool) ? pool[Math.floor(Math.random() * pool.length)] : '';
  return `${text}\n\n🦞 ${char.name}`;
}

/** XP 里程碑 */
export function msgXpMilestone(char, milestone) {
  const lang = detectLang();
  const text = EVENT_MSGS[lang]?.xpMilestone?.[milestone] || EVENT_MSGS.zh.xpMilestone[milestone] || '';
  return `${text}\n\n🦞 ${char.name}  總 XP：${char.xp.toLocaleString()}`;
}

/** 對話數里程碑 */
export function msgConvMilestone(char, milestone) {
  const lang = detectLang();
  const text = EVENT_MSGS[lang]?.convMilestone?.[milestone] || EVENT_MSGS.zh.convMilestone[milestone] || '';
  return `${text}\n\n🦞 ${char.name}  總對話：${char.conversations.toLocaleString()}`;
}

/** 深夜勇士 */
export function msgNightOwl(char) {
  return `${pickEvent('nightOwl')}\n\n🦞 ${char.name}`;
}

/** 單向巨輸出 */
export function msgSilentOutput(char) {
  return `${pickEvent('silentOutput')}\n\n🦞 ${char.name}`;
}
