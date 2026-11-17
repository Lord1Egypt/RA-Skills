#!/usr/bin/env node
// coc-helper CLI 入口 (v1.0)
//
// 子命令：
//   roll     — 掷骰（含 COC 7e d100 检定、奖励/惩罚骰）
//   san      — SAN 检定 / 恢复 / 阈值
//   inv      — 调查员管理（建卡/列出/查看/伤害/治疗/删除）
//   table    — 抽取疯狂表/恐惧症/躁狂症/职业/武器/NPC/钩子
//   combat   — 战斗先攻（按 DEX）/追逐先攻（按 MOV）
//   config   — 规则配置（大成功/大失败范围、SAN 阈值等）

import {
  rollDice,
  rollPercentile,
  successLevel,
  SUCCESS_LEVEL_LABEL,
  SUCCESS_LEVEL_RANK,
  makeRng,
  opposedRoll,
} from "./lib/dice.mjs";

import {
  sanCheck,
  sanGain,
  privateCare,
  institutionalCare,
  sanThreshold,
  parseSanLoss,
} from "./lib/sanity.mjs";

import {
  createInvestigator,
  addInvestigator,
  listInvestigators,
  findInvestigator,
  updateInvestigator,
  deleteInvestigator,
  applyDamage,
  heal,
  deriveStats,
  dbAndBuild,
  calcMov,
  skillGrowth,
  luckGain,
  eduEnhancementCheck,
} from "./lib/investigator.mjs";

import {
  randomName,
  randomNpc,
  randomPhobia,
  randomMania,
  randomMadnessInstant,
  randomMadnessSummary,
  listOccupations,
  listWeapons,
  findWeapon,
  combatInitiative,
  chaseInitiative,
  generateHook,
} from "./lib/tables.mjs";

import {
  loadRules,
  saveRules,
  resetRules,
  applyVariant,
  parseRange,
  formatRange,
  DEFAULT_RULES,
  RULE_VARIANTS,
} from "./lib/rules-config.mjs";

// ---------- argv 解析 ----------

// KNOWN_FLAGS 内的 flag 不吃下一个参数（布尔开关）；
// 其他 --xxx 视为带值选项（吃下一个参数）。
const KNOWN_FLAGS = new Set([
  "json",
  "quiet",
  "help",
  "h",
  "pulp",
  "auto",
  "summary",
  "male",
  "female",
  "zh",
  "en",
]);

function parseArgs(argv) {
  const args = { _: [], flags: {}, options: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      if (key.includes("=")) {
        const [k, ...rest] = key.split("=");
        args.options[k] = rest.join("=");
      } else if (KNOWN_FLAGS.has(key)) {
        args.flags[key] = true;
      } else if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
        args.options[key] = argv[++i];
      } else {
        args.options[key] = true;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

// ---------- 格式化 ----------

function fmtDice(r) {
  const parts = [];
  parts.push(`[${r.rolls.join(" + ")}]`);
  if (r.multiplier !== 1) parts.push(`×${r.multiplier}`);
  if (r.modifier > 0) parts.push(`+${r.modifier}`);
  else if (r.modifier < 0) parts.push(`${r.modifier}`);
  return parts.join(" ");
}

function formatRoll(r) {
  const lines = [
    `🎲 Rolling ${r.spec}`,
    `   Rolls: ${fmtDice(r)}`,
    `   Total: ${r.total}`,
  ];
  if (r.level) lines.push(`   Level: ${SUCCESS_LEVEL_LABEL[r.level]}`);
  return lines.join("\n");
}

function formatPercentile(r) {
  const lines = [];
  const tag = r.bonus ? " (奖励骰)" : r.penalty ? " (惩罚骰)" : "";
  lines.push(`🎲 d100${tag}`);
  if (r.tensDice.length > 1) {
    const tensStr = r.tensDice
      .map((t, i) => (i === r.usedTensIndex ? `${t}✓` : `${t}`))
      .join(", ");
    lines.push(`   Tens: [${tensStr}]  Ones: ${r.ones}`);
  } else {
    lines.push(`   Tens: ${r.tensDice[0]}  Ones: ${r.ones}`);
  }
  lines.push(`   Total: ${r.total}`);
  if (r.target !== undefined) {
    lines.push(
      `   Target: ${r.target} (hard ${r.hardTarget}, extreme ${r.extremeTarget}, fumble ≥${r.fumbleThreshold})`,
    );
    lines.push(`   Level: ${r.levelLabel}`);
  }
  return lines.join("\n");
}

function formatSanCheck(r) {
  const lines = [
    `🧠 SAN Check: ${r.currentSan} → ${r.newSan} (-${r.sanLoss})`,
    `   ${r.note}`,
  ];
  if (r.check) {
    lines.push(
      `   Roll: ${r.check.total} vs ${r.currentSan} → ${r.check.levelLabel}`,
    );
  }
  if (r.successLossRoll) {
    lines.push(
      `   Success loss: ${r.successLossRoll.spec} = ${r.successLossRoll.total}`,
    );
  }
  if (r.failLossRoll) {
    lines.push(
      `   Fail loss: ${r.failLossRoll.spec} = ${r.failLossRoll.total}`,
    );
  }
  if (r.intCheck) {
    lines.push(
      `   INT 检定: ${r.intCheck.total} vs ${r.intCheck.target} → ${r.intCheck.levelLabel}`,
    );
  }
  if (r.sanityBout) {
    lines.push(
      `   ⚠️  临时性疯狂 ${r.boutDuration} 小时；疯狂发作 ${r.boutOnset} 战斗轮`,
    );
  }
  if (r.wentInsane) {
    lines.push(`   ⚠️  不定性疯狂（单次损失 ≥ 20）`);
  }
  if (r.permanentInsanity) {
    lines.push(`   ☠️  永久性疯狂（SAN = 0）`);
  }
  return lines.join("\n");
}

function formatInvestigator(inv, verbose = false) {
  const lines = [];
  lines.push(
    `👤 ${inv.name}（${inv.age}岁）${inv.occupation ? " [" + inv.occupation + "]" : ""}${inv.pulp ? " [Pulp]" : ""}`,
  );
  const c = inv.characteristics;
  lines.push(
    `   STR ${c.str}  CON ${c.con}  SIZ ${c.siz}  DEX ${c.dex}  APP ${c.app}  INT ${c.int}  POW ${c.pow}  EDU ${c.edu}`,
  );
  lines.push(
    `   Luck ${inv.luck}  SAN ${inv.san}/${inv.maxSan}  HP ${inv.hp}/${inv.maxHp}  MP ${inv.mp}/${inv.maxMp}`,
  );
  lines.push(
    `   DB ${inv.derived.db}  Build ${inv.derived.build}  MOV ${inv.derived.mov}  闪避 ${inv.derived.dodge}`,
  );
  if (inv.majorWound) lines.push(`   ⚠️ 重伤`);
  if (inv.dying) lines.push(`   ⚠️ 濒死`);
  if (inv.unconscious) lines.push(`   💤 昏迷`);
  if (inv.insane) lines.push(`   🌀 疯狂中`);
  if (verbose && inv.skills && Object.keys(inv.skills).length > 0) {
    lines.push(`   技能：`);
    for (const [k, v] of Object.entries(inv.skills)) {
      lines.push(`     ${k}: ${v}`);
    }
  }
  if (verbose && inv.eduEnhancements && inv.eduEnhancements.length > 0) {
    lines.push(`   EDU 增强检定历史：`);
    for (const e of inv.eduEnhancements) {
      lines.push(`     roll=${e.roll} gain=${e.gain} newEdu=${e.newEdu}`);
    }
  }
  return lines.join("\n");
}

function formatNpc(npc) {
  const langTag = npc.lang === "zh" ? "中" : "英";
  return [
    `🎭 ${npc.name}（${npc.gender === "male" ? "男" : "女"}，${langTag}）`,
    `   职业: ${npc.occupation}`,
    `   信用评级: ${npc.creditRating}`,
    `   核心技能: ${npc.skills.join(", ")}`,
    `   人脉: ${npc.contacts}`,
  ].join("\n");
}

// ---------- 主入口 ----------

function printHelp() {
  console.error(`coc-helper v1.0 — COC 7e 掷骰 & KP 助手

Usage:
  node cli.mjs <command> [options]

Commands:
  roll <spec>            掷骰（3d6*5 / 1d100 / 2d6+3 / 8d6 / d20-2）
    --target N            d100 检定目标值
    --bonus N             奖励骰数量（1 或 2，默认 1）
    --penalty N           惩罚骰数量（1 或 2，默认 1）
    --seed N              种子化 PRNG（可复现）
    --json / --quiet      输出格式

  roll opposed <a_target> <b_target> [--a-label X] [--b-label Y]
                         对抗检定（双方 d100，比较成功等级，平手时目标高者胜）
    --a-bonus N / --a-penalty N
    --b-bonus N / --b-penalty N

  roll push <spec> --target N
                         孤注一掷（失败后再投一次）
                         不可用于幸运、理智、战斗、伤害骰
    --bonus N / --penalty N

  roll luck <name>       幸运检定（目标=调查员的 luck 值）
                         或：roll luck --target N

  san <action>            SAN 系统
    check <name> <loss>   SAN 检定（loss 为 "X/Y" 格式，如 0/1d4 / 1/1d4+1 / 1d10/1d100）
                         旧写法 san check <name> 1d4 等价于 1/1d4
    gain <name>           团末恢复 d10
    private <name> [psy]  私人护理（--psy=精神分析技能）
    institution <name>    收容机构护理
    threshold <name>      查看阈值

  inv <action>            调查员管理
    create --name X --age N [--occupation Y] [--pulp]
    list                  列出所有调查员
    show <name>           查看详情
    damage <name> <N>     应用伤害
    heal <name> <N>       治疗
    delete <name>         删除
    derive --str N --con N --siz N --dex N --app N --int N --pow N --edu N
                           计算衍生属性
    growth <name> <skill1> [skill2 ...]  幕间技能成长检定（每技能 1d100 vs 当前值）
    luck-gain <name>      幕间幸运增强检定（1d100 > 当前幸运 → +1d10，上限 99）

  table <action>          表格辅助
    madness [--summary]   抽取疯狂发作表（默认即时；--summary 抽总结表）
    phobia                随机恐惧症
    mania                 随机躁狂症
    npc [--zh|--en]       随机 NPC（默认随机语言）
    name [--male|--female] [--zh|--en]  随机姓名
    occupations           列出职业
    weapons [name]        列出/查找武器
    hook                  生成剧情钩子

  combat <action>         战斗辅助
    init name1:DEX name2:DEX ...   战斗先攻（按 DEX 降序）
    chase name1:MOV name2:MOV ...  追逐先攻（按 MOV 降序）

  config <action>         规则配置（可变规则 / 可选阈值，持久化到 session.json）
    show                   查看当前规则配置
    defaults               查看默认规则配置
    set <key> <value>      设置单项（见下方可配置项）
    variant [name]         查看/应用预设变体：strict（1/100）、lenient（1-5/96-100）
    reset                  重置为默认规则配置

Global Options:
  --seed N                全局种子
  --json                  JSON 输出
  --quiet                 简洁输出
  -h, --help              显示此帮助

规则要点：
  - 大成功：默认骰出 01（可用 config variant lenient 改为 1-5）
  - 大失败：默认目标<50 时 96-100，目标≥50 时 100（可用 config variant lenient 改为 96-100）
  - 临时疯狂：单次损失 ≥ 5 SAN（可配置）→ INT 检定成功则进入（持续 1D10 小时）
  - 不定性疯狂：单次损失 ≥ 20 SAN（可配置）或一天内累计损失 ≥ 1/5 当前 SAN
  - 永久疯狂：SAN 降至 0
  - 对抗检定不可孤注一掷；孤注一掷不可用于幸运/理智/战斗/伤害

可配置规则项（config set <key> <value>）：
  criticalRange               大成功骰值范围（"1" 或 "1-5"）
  fumbleRange                 大失败骰值范围（"100"、"96-100" 或 "auto"）
  tempInsanityThreshold       临时性疯狂阈值（默认 5）
  indefiniteInsanitySingleLoss 不定性疯狂单次阈值（默认 20）
  indefiniteInsanityDailyFraction 不定性疯狂日累计分数（默认 0.2 = 1/5）

Examples:
  node cli.mjs roll 1d100 --target 60 --bonus 1
  node cli.mjs roll 1d100 --target 60 --penalty 2
  node cli.mjs roll opposed 55 45 --a-label "陈博士" --b-label "邪教徒"
  node cli.mjs roll push 1d100 --target 50
  node cli.mjs roll luck "陈博士"
  node cli.mjs san check "陈博士" 1/1d4+1 --seed 42
  node cli.mjs san check "陈博士" 0/1d6
  node cli.mjs inv create --name "陈博士" --age 35 --occupation 医生
  node cli.mjs inv damage "陈博士" 5
  node cli.mjs inv growth "陈博士" "图书馆使用" "侦查" "聆听"
  node cli.mjs inv luck-gain "陈博士"
  node cli.mjs table madness
  node cli.mjs table npc --seed 7
  node cli.mjs combat init "陈博士:60" "邪教徒:50" "怪物:80"
  node cli.mjs config show
  node cli.mjs config variant lenient
  node cli.mjs config set tempInsanityThreshold 3
  node cli.mjs config reset`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args._.length === 0 || args.flags.h || args.flags.help) {
    printHelp();
    process.exit(1);
  }

  const seed =
    args.options.seed !== undefined ? Number(args.options.seed) : undefined;
  const rng = makeRng(seed);
  const json = !!args.flags.json;
  const quiet = !!args.flags.quiet;
  // 加载当前规则配置（含可变大成功/大失败范围、SAN 阈值）
  const rules = loadRules();

  try {
    const cmd = args._[0];

    if (cmd === "config") return cmdConfig(args, json, quiet);
    if (cmd === "roll") return cmdRoll(args, rng, json, quiet, rules);
    if (cmd === "san") return cmdSan(args, rng, json, quiet, rules);
    if (cmd === "inv") return cmdInv(args, rng, json, quiet, rules);
    if (cmd === "table") return cmdTable(args, rng, json, quiet);
    if (cmd === "combat") return cmdCombat(args, rng, json, quiet);

    throw new Error(`Unknown command: ${cmd}`);
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(2);
  }
}

// ---------- roll ----------

function parseBonusPenalty(args) {
  // 支持 --bonus N / --bonus（默认 1）；--penalty N / --penalty（默认 1）
  let bonus = 0;
  let penalty = 0;
  if (args.options.bonus !== undefined) {
    bonus = args.options.bonus === true ? 1 : Number(args.options.bonus) || 1;
  }
  if (args.options.penalty !== undefined) {
    penalty =
      args.options.penalty === true ? 1 : Number(args.options.penalty) || 1;
  }
  return { bonus, penalty };
}

// 从 rules 配置中提取掷骰相关 opts
function diceRules(rules) {
  const opts = {};
  if (rules.criticalRange) opts.criticalRange = rules.criticalRange;
  if (rules.fumbleRange !== undefined) opts.fumbleRange = rules.fumbleRange;
  return opts;
}

function cmdRoll(args, rng, json, quiet, rules) {
  const sub = args._[1];

  // 对抗检定
  if (sub === "opposed") {
    return cmdRollOpposed(args, rng, json, quiet, rules);
  }
  // 孤注一掷
  if (sub === "push") {
    return cmdRollPush(args, rng, json, quiet, rules);
  }
  // 幸运检定
  if (sub === "luck") {
    return cmdRollLuck(args, rng, json, quiet, rules);
  }

  // 普通掷骰
  const spec = sub;
  if (!spec) throw new Error("missing dice spec");
  const target =
    args.options.target !== undefined ? Number(args.options.target) : undefined;
  const { bonus, penalty } = parseBonusPenalty(args);
  const isPercentile = /^[1]?d100$/i.test(spec);

  let result;
  if (isPercentile && (target !== undefined || bonus > 0 || penalty > 0)) {
    result = rollPercentile({
      target,
      bonus,
      penalty,
      rng,
      ...diceRules(rules),
    });
    if (json) console.log(JSON.stringify(result));
    else if (quiet) console.log(result.total);
    else console.log(formatPercentile(result));
  } else {
    result = rollDice(spec, rng);
    if (target !== undefined && isPercentile) {
      result.target = target;
      result.level = successLevel(result.total, target, diceRules(rules));
      result.levelLabel = SUCCESS_LEVEL_LABEL[result.level];
    }
    if (json) console.log(JSON.stringify(result));
    else if (quiet) console.log(result.total);
    else console.log(formatRoll(result));
  }
}

function cmdRollOpposed(args, rng, json, quiet, rules) {
  const aTarget = Number(args._[2]);
  const bTarget = Number(args._[3]);
  if (!Number.isFinite(aTarget) || !Number.isFinite(bTarget)) {
    throw new Error(
      "用法：roll opposed <a_target> <b_target> [--a-label X --b-label Y]",
    );
  }
  const aLabel = args.options["a-label"] || "A";
  const bLabel = args.options["b-label"] || "B";
  const aBonus =
    args.options["a-bonus"] !== undefined ? Number(args.options["a-bonus"]) : 0;
  const aPenalty =
    args.options["a-penalty"] !== undefined
      ? Number(args.options["a-penalty"])
      : 0;
  const bBonus =
    args.options["b-bonus"] !== undefined ? Number(args.options["b-bonus"]) : 0;
  const bPenalty =
    args.options["b-penalty"] !== undefined
      ? Number(args.options["b-penalty"])
      : 0;
  const dr = diceRules(rules);

  const result = opposedRoll(
    { target: aTarget, bonus: aBonus, penalty: aPenalty, label: aLabel, ...dr },
    { target: bTarget, bonus: bBonus, penalty: bPenalty, label: bLabel, ...dr },
    rng,
  );
  if (json) {
    console.log(JSON.stringify(result));
    return;
  }
  console.log(`⚔️  对抗检定：${aLabel} (${aTarget}) vs ${bLabel} (${bTarget})`);
  console.log(
    `   ${aLabel}: ${result.rollA.total} → ${result.rollA.levelLabel}`,
  );
  console.log(
    `   ${bLabel}: ${result.rollB.total} → ${result.rollB.levelLabel}`,
  );
  const winnerLabel =
    result.winner === "a"
      ? aLabel
      : result.winner === "b"
        ? bLabel
        : "（僵局）";
  console.log(`   ✓ 胜者：${winnerLabel}`);
  console.log(`   原因：${result.reason}`);
}

function cmdRollPush(args, rng, json, quiet, rules) {
  const spec = args._[2];
  if (!spec)
    throw new Error("missing dice spec (用法：roll push 1d100 --target N)");
  const target =
    args.options.target !== undefined ? Number(args.options.target) : undefined;
  if (target === undefined) throw new Error("孤注一掷必须指定 --target");
  const { bonus, penalty } = parseBonusPenalty(args);
  const dr = diceRules(rules);

  // 第一次掷骰
  const first = rollPercentile({ target, bonus, penalty, rng, ...dr });
  // 失败时进行孤注一掷
  let pushed = null;
  let finalResult = first;
  if (first.level === "failure" || first.level === "fumble") {
    pushed = rollPercentile({ target, bonus, penalty, rng, ...dr });
    finalResult = pushed;
  }

  const summary = {
    target,
    first,
    pushed,
    final: finalResult,
    note:
      first.level === "regular" ||
      first.level === "hard" ||
      first.level === "extreme" ||
      first.level === "critical"
        ? "首次成功，无需孤注一掷"
        : pushed
          ? pushed.level === "failure" || pushed.level === "fumble"
            ? "孤注一掷失败：KP 可施加更严重后果（伤害、SAN 损失、装备损失、被俘等）"
            : "孤注一掷成功：目标达成，无失败后果"
          : "首次失败但未孤注一掷",
  };

  if (json) {
    console.log(JSON.stringify(summary));
    return;
  }
  console.log(`🎲 孤注一掷（target=${target}）`);
  console.log(`   第一次：${first.total} → ${first.levelLabel}`);
  if (pushed) {
    console.log(`   孤注一掷：${pushed.total} → ${pushed.levelLabel}`);
  }
  console.log(`   → ${summary.note}`);
}

function cmdRollLuck(args, rng, json, quiet, rules) {
  // roll luck <name>  或  roll luck --target N
  const name = args._[2];
  let target;
  if (name) {
    const inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    target = inv.luck;
  } else if (args.options.target !== undefined) {
    target = Number(args.options.target);
  } else {
    throw new Error("用法：roll luck <name>  或  roll luck --target N");
  }
  const { bonus, penalty } = parseBonusPenalty(args);
  const result = rollPercentile({
    target,
    bonus,
    penalty,
    rng,
    ...diceRules(rules),
  });
  if (json) {
    console.log(JSON.stringify({ type: "luck", target, ...result }));
    return;
  }
  if (quiet) {
    console.log(result.total);
    return;
  }
  console.log(`🍀 幸运检定（目标=${target}${name ? ` [${name}]` : ""}）`);
  if (result.tensDice.length > 1) {
    const tensStr = result.tensDice
      .map((t, i) => (i === result.usedTensIndex ? `${t}✓` : `${t}`))
      .join(", ");
    console.log(
      `   Tens: [${tensStr}]  Ones: ${result.ones}  Total: ${result.total}`,
    );
  } else {
    console.log(`   Total: ${result.total}`);
  }
  console.log(`   → ${result.levelLabel}`);
}

// ---------- san ----------

function cmdSan(args, rng, json, quiet, rules) {
  const action = args._[1];
  if (!action)
    throw new Error(
      "missing san action: check|gain|private|institution|threshold",
    );

  if (action === "threshold") {
    const name = args._[2];
    if (!name) throw new Error("missing investigator name");
    const inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    const result = sanThreshold(inv.san, inv.maxSan);
    if (json) console.log(JSON.stringify(result));
    else console.log(result.notes);
    return;
  }

  const name = args._[2];
  if (!name) throw new Error("missing investigator name");
  const inv = findInvestigator(name);
  if (!inv) throw new Error(`investigator not found: ${name}`);

  let result;
  if (action === "check") {
    const lossArg = args._[3];
    if (!lossArg)
      throw new Error(
        "missing loss spec (e.g. 1/1d4+1 或 0/1d6 或 1d10/1d100)",
      );
    let lossExpr;
    if (lossArg.includes("/")) {
      // 新格式 X/Y
      lossExpr = lossArg;
    } else {
      // 旧格式兼容：纯骰子表达式视为 "1/X"
      lossExpr = `1/${lossArg}`;
    }
    // 调查员的 INT 用于临时疯狂的 INT 检定
    const intScore = inv.characteristics && inv.characteristics.int;
    result = sanCheck({
      currentSan: inv.san,
      loss: lossExpr,
      intScore,
      rng,
      tempInsanityThreshold: rules.tempInsanityThreshold,
      indefiniteInsanitySingleLoss: rules.indefiniteInsanitySingleLoss,
      criticalRange: rules.criticalRange,
      fumbleRange: rules.fumbleRange,
    });
    // 更新调查员 SAN
    const updates = {
      san: result.newSan,
      insane: result.wentInsane || result.permanentInsanity || inv.insane,
    };
    updateInvestigator(name, updates);
  } else if (action === "gain") {
    result = sanGain({ currentSan: inv.san, maxSan: inv.maxSan, rng });
    updateInvestigator(name, { san: result.newSan });
  } else if (action === "private") {
    const psy = args.options.psy !== undefined ? Number(args.options.psy) : 0;
    result = privateCare({
      currentSan: inv.san,
      maxSan: inv.maxSan,
      psychoanalysis: psy,
      rng,
    });
    updateInvestigator(name, {
      san: result.newSan,
      insane: result.exitsInsanity ? false : inv.insane,
    });
  } else if (action === "institution") {
    result = institutionalCare({
      currentSan: inv.san,
      maxSan: inv.maxSan,
      rng,
    });
    updateInvestigator(name, {
      san: result.newSan,
      insane: result.exitsInsanity ? false : inv.insane,
    });
  } else {
    throw new Error(`unknown san action: ${action}`);
  }

  if (json) console.log(JSON.stringify(result));
  else if (quiet) console.log(result.newSan !== undefined ? result.newSan : "");
  else console.log(formatSanCheck(result));
}

// ---------- inv ----------

function cmdInv(args, rng, json, quiet, rules) {
  const action = args._[1];
  if (!action)
    throw new Error(
      "missing inv action: create|list|show|damage|heal|delete|derive",
    );

  if (action === "list") {
    const invs = listInvestigators();
    if (json) {
      console.log(JSON.stringify(invs));
      return;
    }
    if (invs.length === 0) {
      console.log("(尚无调查员)");
      return;
    }
    for (const inv of invs) {
      console.log(formatInvestigator(inv));
    }
    return;
  }

  if (action === "derive") {
    const required = ["str", "con", "siz", "dex", "app", "int", "pow", "edu"];
    const c = {};
    for (const k of required) {
      if (args.options[k] === undefined) throw new Error(`missing --${k}`);
      c[k] = Number(args.options[k]);
    }
    const derived = deriveStats(c, !!args.flags.pulp);
    const { db, build } = dbAndBuild(c.str, c.siz);
    const mov = calcMov(c.str, c.dex, c.siz, Number(args.options.age || 25));
    const result = {
      characteristics: c,
      derived: { ...derived, db, build, mov: mov },
    };
    if (json) console.log(JSON.stringify(result));
    else
      console.log(
        `HP ${derived.hp}  MP ${derived.mp}  SAN ${derived.san}  DB ${db}  Build ${build}  MOV ${mov}  闪避 ${derived.dodge}`,
      );
    return;
  }

  if (action === "create") {
    const name = args.options.name;
    if (!name) throw new Error("missing --name");
    const age = args.options.age !== undefined ? Number(args.options.age) : 25;
    const occupation = args.options.occupation;
    const pulp = !!args.flags.pulp;
    const inv = createInvestigator({ name, age, occupation, pulp, rng });
    addInvestigator(inv);
    if (json) console.log(JSON.stringify(inv));
    else console.log(formatInvestigator(inv, true));
    return;
  }

  // 其余 action 都需要名字
  const name = args._[2];
  if (!name) throw new Error("missing investigator name");

  if (action === "show") {
    const inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    if (json) console.log(JSON.stringify(inv));
    else console.log(formatInvestigator(inv, true));
    return;
  }

  if (action === "delete") {
    const result = deleteInvestigator(name);
    if (json) console.log(JSON.stringify(result));
    else console.log(`✓ 已删除 ${name}`);
    return;
  }

  if (action === "damage") {
    const amount = Number(args._[3]);
    if (!Number.isFinite(amount)) throw new Error("missing damage amount");
    let inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    const result = applyDamage(inv, amount);
    updateInvestigator(name, {
      hp: result.investigator.hp,
      majorWound: result.investigator.majorWound,
      dying: result.investigator.dying,
      unconscious: result.investigator.unconscious,
    });
    if (json) console.log(JSON.stringify(result));
    else
      console.log(
        `${formatInvestigator(result.investigator)}\n   → ${result.note}`,
      );
    return;
  }

  if (action === "heal") {
    const amount = Number(args._[3]);
    if (!Number.isFinite(amount)) throw new Error("missing heal amount");
    let inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    const result = heal(inv, amount);
    updateInvestigator(name, {
      hp: result.newHp,
      dying: result.investigator.dying,
    });
    if (json) console.log(JSON.stringify(result));
    else console.log(formatInvestigator(result.investigator));
    return;
  }

  if (action === "growth") {
    // inv growth <name> <skill1> [skill2 ...]
    const skills = args._.slice(3);
    if (skills.length === 0)
      throw new Error("用法：inv growth <name> <skill1> [skill2 ...]");
    const inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    const result = skillGrowth(inv, skills, rng);
    // 持久化
    updateInvestigator(name, {
      skills: result.skills,
      san: result.newSan,
    });
    if (json) {
      console.log(JSON.stringify(result));
      return;
    }
    console.log(`🌱 技能成长检定：${name}`);
    for (const r of result.results) {
      if (r.skipped) {
        console.log(`   ${r.skill}: 跳过（${r.reason}）`);
        continue;
      }
      const arrow = r.grew ? "↑" : "=";
      console.log(
        `   ${r.skill}: ${r.oldValue} ${arrow} ${r.newValue}  (1d100=${r.roll}${r.grew ? `, +1d10=${r.gain}` : ""})`,
      );
      if (r.sanBonus) {
        console.log(`      ★ 技能达 90，SAN +${r.sanBonus}`);
      }
    }
    if (result.sanGained > 0) {
      const actual = result.newSan - inv.san;
      console.log(
        `   SAN 奖励：+${actual}${result.capped ? ` (已上限 ${inv.maxSan})` : ""}`,
      );
    }
    return;
  }

  if (action === "luck-gain") {
    // inv luck-gain <name>
    const inv = findInvestigator(name);
    if (!inv) throw new Error(`investigator not found: ${name}`);
    const result = luckGain(inv, rng);
    updateInvestigator(name, { luck: result.newLuck });
    if (json) {
      console.log(JSON.stringify(result));
      return;
    }
    console.log(`🍀 幸运增强检定：${name}`);
    console.log(`   1d100=${result.roll} vs luck=${result.currentLuck}`);
    if (result.grew) {
      console.log(
        `   幸运 ${result.currentLuck} → ${result.newLuck} (+${result.gain})${result.capped ? " (已达上限 99)" : ""}`,
      );
    } else {
      console.log(`   幸运未变（${result.currentLuck}）`);
    }
    return;
  }

  throw new Error(`unknown inv action: ${action}`);
}

// ---------- table ----------

function cmdTable(args, rng, json, quiet) {
  const action = args._[1];
  if (!action)
    throw new Error(
      "missing table action: madness|phobia|mania|npc|name|occupations|weapons|hook",
    );

  let result;
  switch (action) {
    case "madness":
      result = args.flags.summary
        ? randomMadnessSummary(rng)
        : randomMadnessInstant(rng);
      break;
    case "phobia":
      result = randomPhobia(rng);
      break;
    case "mania":
      result = randomMania(rng);
      break;
    case "npc": {
      const lang = args.flags.zh ? "zh" : args.flags.en ? "en" : "any";
      result = randomNpc(lang, rng);
      break;
    }
    case "name": {
      const gender = args.flags.male
        ? "male"
        : args.flags.female
          ? "female"
          : "any";
      const lang = args.flags.zh ? "zh" : args.flags.en ? "en" : "any";
      result = randomName(gender, lang, rng);
      break;
    }
    case "occupations":
      result = listOccupations();
      break;
    case "weapons": {
      const filter = args._[2];
      result = filter ? findWeapon(filter) : listWeapons();
      break;
    }
    case "hook":
      result = generateHook(rng);
      break;
    default:
      throw new Error(`unknown table action: ${action}`);
  }

  if (json) {
    console.log(JSON.stringify(result));
    return;
  }
  if (quiet) {
    if (typeof result === "string") console.log(result);
    else if (result.value) console.log(result.value);
    else if (result.full) console.log(result.full);
    else if (result.toString) console.log(result.toString());
    else console.log(JSON.stringify(result));
    return;
  }
  if (action === "madness") {
    console.log(`🎲 1d10=${result.roll}：${result.value}`);
  } else if (action === "phobia" || action === "mania") {
    console.log(`🎲 1d20=${result.roll}：${result.value}`);
  } else if (action === "npc") {
    console.log(formatNpc(result));
  } else if (action === "name") {
    const langTag = result.lang === "zh" ? "中" : "英";
    console.log(
      `👤 ${result.full}（${result.gender === "male" ? "男" : "女"}，${langTag}）`,
    );
  } else if (action === "occupations") {
    console.log(`📚 职业列表（${result.length} 项）：`);
    for (const o of result) {
      console.log(
        `   [${o.id}] ${o.name}（CR ${o.creditRating[0]}-${o.creditRating[1]}）：${o.skills.join(", ")}`,
      );
    }
  } else if (action === "weapons") {
    if (Array.isArray(result)) {
      console.log(`⚔️  武器列表（${result.length} 项）：`);
      for (const w of result) {
        console.log(
          `   ${w.name} [${w.skill}] 伤害 ${w.damage} 射程 ${w.range} 弹仓 ${w.magazine} 故障 ${w.malfunction}`,
        );
      }
    } else if (result) {
      console.log(`⚔️  ${result.name}`);
      console.log(
        `   技能: ${result.skill}  伤害: ${result.damage}  射程: ${result.range}`,
      );
      console.log(
        `   贯穿: ${result.penetrate ? "是" : "否"}  每轮攻击: ${result.attacks}  弹仓: ${result.magazine}`,
      );
      console.log(
        `   故障值: ${result.malfunction}  时代: ${result.eras.join("/")}`,
      );
      console.log(
        `   价格: 1920s $${result.price["1920s"] ?? "—"} / 现代 $${result.price["现代"] ?? "—"}`,
      );
    } else {
      console.log("(未找到)");
    }
  } else if (action === "hook") {
    console.log(`📜 ${result.toString()}`);
  }
}

// ---------- combat ----------

function cmdCombat(args, rng, json, quiet) {
  const action = args._[1];
  if (!action) throw new Error("missing combat action: init|chase");
  const entries = args._.slice(2);
  if (entries.length === 0)
    throw new Error("missing combatants (format: name:stat)");

  const combatants = entries.map((e) => {
    const [name, stat] = e.split(":");
    if (!name || stat === undefined)
      throw new Error(`invalid format: ${e} (expected name:stat)`);
    return { name, [action === "init" ? "dex" : "mov"]: Number(stat) };
  });

  const result =
    action === "init"
      ? combatInitiative(combatants)
      : chaseInitiative(combatants);

  if (json) {
    console.log(JSON.stringify(result));
    return;
  }
  console.log(
    action === "init"
      ? "⚔️  战斗先攻（按 DEX 降序）："
      : "🏃 追逐先攻（按 MOV 降序）：",
  );
  for (const c of result) {
    const stat = action === "init" ? `DEX ${c.dex}` : `MOV ${c.mov}`;
    console.log(`   ${c.initiative}. ${c.name}（${stat}）`);
  }
}

// ---------- config ----------

// 支持的配置键及其设置函数
const CONFIG_KEYS = {
  criticalRange: {
    desc: "大成功骰值范围",
    parse: (v) => parseRange(v),
    format: (v) => formatRange(v),
  },
  fumbleRange: {
    desc: "大失败骰值范围（设为 auto 表示按目标值自动）",
    parse: (v) => (v === "auto" || v === "" ? null : parseRange(v)),
    format: (v) => formatRange(v),
  },
  tempInsanityThreshold: {
    desc: "单次 SAN 损失触发临时性疯狂的阈值",
    parse: (v) => {
      const n = Number(v);
      if (!Number.isFinite(n) || n < 0) throw new Error(`无效数值: ${v}`);
      return n;
    },
    format: (v) => `${v}`,
  },
  indefiniteInsanitySingleLoss: {
    desc: "单次 SAN 损失触发不定性疯狂的阈值",
    parse: (v) => {
      const n = Number(v);
      if (!Number.isFinite(n) || n < 0) throw new Error(`无效数值: ${v}`);
      return n;
    },
    format: (v) => `${v}`,
  },
  indefiniteInsanityDailyFraction: {
    desc: "一天累计 SAN 损失触发不定性疯狂的分数（如 0.2 = 1/5）",
    parse: (v) => {
      const n = Number(v);
      if (!Number.isFinite(n) || n <= 0 || n > 1)
        throw new Error(`无效分数: ${v}（应在 0~1 之间）`);
      return n;
    },
    format: (v) => `${v} (${Math.round(v * 100)}%)`,
  },
};

function cmdConfig(args, json, quiet) {
  const action = args._[1];
  if (!action)
    throw new Error("missing config action: show|set|variant|reset|defaults");

  if (action === "show") {
    const rules = loadRules();
    if (json) {
      console.log(JSON.stringify(rules));
      return;
    }
    console.log("📋 当前规则配置：");
    for (const [k, def] of Object.entries(CONFIG_KEYS)) {
      console.log(`   ${k}: ${def.format(rules[k])}  — ${def.desc}`);
    }
    return;
  }

  if (action === "defaults") {
    if (json) {
      console.log(JSON.stringify(DEFAULT_RULES));
      return;
    }
    console.log("📋 默认规则配置：");
    for (const [k, def] of Object.entries(CONFIG_KEYS)) {
      console.log(`   ${k}: ${def.format(DEFAULT_RULES[k])}  — ${def.desc}`);
    }
    return;
  }

  if (action === "reset") {
    const rules = resetRules();
    if (json) {
      console.log(JSON.stringify(rules));
      return;
    }
    console.log("✓ 已重置为默认规则配置");
    return;
  }

  if (action === "variant") {
    const variantName = args._[2];
    if (!variantName) {
      // 列出所有变体
      if (json) {
        console.log(JSON.stringify(RULE_VARIANTS));
        return;
      }
      console.log("📋 可用规则变体：");
      for (const [name, v] of Object.entries(RULE_VARIANTS)) {
        console.log(`   ${name}: ${v.label}`);
      }
      return;
    }
    const rules = applyVariant(variantName);
    if (json) {
      console.log(JSON.stringify(rules));
      return;
    }
    console.log(
      `✓ 已应用规则变体：${variantName}（${RULE_VARIANTS[variantName].label}）`,
    );
    return;
  }

  if (action === "set") {
    // config set <key> <value>
    const key = args._[2];
    const value = args._[3];
    if (!key || value === undefined)
      throw new Error(
        "用法：config set <key> <value>（用 config defaults 查看可选项）",
      );
    const def = CONFIG_KEYS[key];
    if (!def) {
      throw new Error(
        `未知配置项: ${key}（可用项：${Object.keys(CONFIG_KEYS).join(", ")}）`,
      );
    }
    const parsed = def.parse(value);
    const rules = saveRules({ [key]: parsed });
    if (json) {
      console.log(JSON.stringify(rules));
      return;
    }
    console.log(`✓ 已设置 ${key} = ${def.format(parsed)}`);
    return;
  }

  throw new Error(`unknown config action: ${action}`);
}

main();
