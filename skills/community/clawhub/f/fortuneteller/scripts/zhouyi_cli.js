#!/usr/bin/env node

const crypto = require("crypto");
const ZHOUYI_BENJING = require("../data/zhouyi-benjing");
const DIVINATION_SYSTEMS = require("../data/system-catalog");

const TRIGRAMS = {
  "111": { name: "乾", symbol: "☰", nature: "天", image: "健" },
  "110": { name: "兑", symbol: "☱", nature: "泽", image: "悦" },
  "101": { name: "离", symbol: "☲", nature: "火", image: "丽" },
  "100": { name: "震", symbol: "☳", nature: "雷", image: "动" },
  "011": { name: "巽", symbol: "☴", nature: "风", image: "入" },
  "010": { name: "坎", symbol: "☵", nature: "水", image: "险" },
  "001": { name: "艮", symbol: "☶", nature: "山", image: "止" },
  "000": { name: "坤", symbol: "☷", nature: "地", image: "顺" }
};

const HEXAGRAM_LOOKUP = {
  "乾|乾": 1, "乾|兑": 43, "乾|离": 14, "乾|震": 34, "乾|巽": 9, "乾|坎": 5, "乾|艮": 26, "乾|坤": 11,
  "兑|乾": 10, "兑|兑": 58, "兑|离": 38, "兑|震": 54, "兑|巽": 61, "兑|坎": 60, "兑|艮": 41, "兑|坤": 19,
  "离|乾": 13, "离|兑": 49, "离|离": 30, "离|震": 55, "离|巽": 37, "离|坎": 63, "离|艮": 22, "离|坤": 36,
  "震|乾": 25, "震|兑": 17, "震|离": 21, "震|震": 51, "震|巽": 42, "震|坎": 3, "震|艮": 27, "震|坤": 24,
  "巽|乾": 44, "巽|兑": 28, "巽|离": 50, "巽|震": 32, "巽|巽": 57, "巽|坎": 48, "巽|艮": 18, "巽|坤": 46,
  "坎|乾": 6, "坎|兑": 47, "坎|离": 64, "坎|震": 40, "坎|巽": 59, "坎|坎": 29, "坎|艮": 4, "坎|坤": 7,
  "艮|乾": 33, "艮|兑": 31, "艮|离": 56, "艮|震": 62, "艮|巽": 53, "艮|坎": 39, "艮|艮": 52, "艮|坤": 15,
  "坤|乾": 12, "坤|兑": 45, "坤|离": 35, "坤|震": 16, "坤|巽": 20, "坤|坎": 8, "坤|艮": 23, "坤|坤": 2
};

const POSITION_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"];

function usage() {
  console.log(`
Usage:
  node scripts/zhouyi_cli.js cast --question "..." --method coin|yarrow [--seed demo] [--json]
  node scripts/zhouyi_cli.js lookup --name 乾 [--json]
  node scripts/zhouyi_cli.js lookup --number 1 [--json]
  node scripts/zhouyi_cli.js search --query "利涉大川" [--json]
  node scripts/zhouyi_cli.js catalog [--grade S|B|C] [--query 关键词] [--json]
`);
}

function parseArgs(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith("--")) continue;
    const key = item.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      options[key] = true;
    } else {
      options[key] = next;
      i += 1;
    }
  }
  return options;
}

function createSeededRng(seedInput) {
  let seed = 0x811c9dc5;
  for (const ch of String(seedInput)) {
    seed ^= ch.charCodeAt(0);
    seed = Math.imul(seed, 16777619);
  }
  if (!seed) seed = 0x9e3779b9;
  return () => {
    seed += 0x6d2b79f5;
    let t = seed;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function randomRng() {
  return () => {
    if (typeof crypto.randomInt === "function") {
      return crypto.randomInt(0, 1_000_000) / 1_000_000;
    }
    return Math.random();
  };
}

function weightedPick(items, rng) {
  const total = items.reduce((sum, item) => sum + item.weight, 0);
  let cursor = rng() * total;
  for (const item of items) {
    cursor -= item.weight;
    if (cursor < 0) return item.value;
  }
  return items[items.length - 1].value;
}

function createLine(value, coins = []) {
  return {
    value,
    coins,
    yang: value === 7 || value === 9,
    moving: value === 6 || value === 9,
    label: value === 6 ? "老阴" : value === 7 ? "少阳" : value === 8 ? "少阴" : "老阳"
  };
}

function tossLine(method, rng) {
  if (method === "yarrow") {
    return createLine(
      weightedPick(
        [
          { value: 6, weight: 1 },
          { value: 7, weight: 5 },
          { value: 8, weight: 7 },
          { value: 9, weight: 3 }
        ],
        rng
      )
    );
  }

  const coins = Array.from({ length: 3 }, () => (rng() < 0.5 ? 2 : 3));
  return createLine(coins.reduce((sum, coin) => sum + coin, 0), coins);
}

function sameTrigramName(sourceName, trigramName) {
  const aliases = { 兑: "兌", 离: "離" };
  return sourceName === trigramName || sourceName === aliases[trigramName];
}

function fullHexagramName(name, upper, lower) {
  if (upper.name === lower.name && sameTrigramName(name, upper.name)) {
    return `${name}为${upper.nature}`;
  }
  return `${upper.nature}${lower.nature}${name}`;
}

function resolveHexagram(lines) {
  const lowerBits = lines.slice(0, 3).map((line) => (line.yang ? "1" : "0")).join("");
  const upperBits = lines.slice(3, 6).map((line) => (line.yang ? "1" : "0")).join("");
  const lower = TRIGRAMS[lowerBits];
  const upper = TRIGRAMS[upperBits];
  const number = HEXAGRAM_LOOKUP[`${lower.name}|${upper.name}`];
  const benjing = ZHOUYI_BENJING[number - 1];

  return {
    number,
    name: benjing.name,
    fullName: fullHexagramName(benjing.name, upper, lower),
    judgment: benjing.judgment,
    lines: benjing.lines,
    extras: benjing.extras,
    lower,
    upper
  };
}

function lineEntry(hexagram, index, priority) {
  return {
    title: `${hexagram.name}${hexagram.lines[index].label}`,
    label: hexagram.lines[index].label,
    text: hexagram.lines[index].text,
    priority
  };
}

function decideTextSource(primary, changed, moving) {
  const count = moving.length;

  if (count === 0) {
    return {
      rule: "六爻不变：以本卦卦辞为主。",
      focus: "本卦卦辞",
      entries: [{ title: `${primary.name}卦辞`, text: primary.judgment, priority: true }]
    };
  }

  if (count === 1) {
    const item = moving[0];
    return {
      rule: "一爻变：以该动爻爻辞为主。",
      focus: primary.lines[item.index].label,
      entries: [lineEntry(primary, item.index, true)]
    };
  }

  if (count === 2) {
    const indexes = moving.map((item) => item.index).sort((a, b) => a - b);
    const upperIndex = indexes[indexes.length - 1];
    return {
      rule: "二爻变：取两条动爻爻辞，以上爻为主。",
      focus: primary.lines[upperIndex].label,
      entries: indexes.map((index) => lineEntry(primary, index, index === upperIndex))
    };
  }

  if (count === 3) {
    return {
      rule: "三爻变：以本卦卦辞与变卦卦辞合看。",
      focus: "本卦与变卦卦辞",
      entries: [
        { title: `${primary.name}卦辞`, text: primary.judgment, priority: true },
        { title: `${changed.name}卦辞`, text: changed.judgment, priority: false }
      ]
    };
  }

  if (count === 4) {
    const staticIndexes = [0, 1, 2, 3, 4, 5].filter((index) => !moving.some((item) => item.index === index));
    const lowerIndex = staticIndexes[0];
    return {
      rule: "四爻变：取两条静爻爻辞，以下爻为主。",
      focus: primary.lines[lowerIndex].label,
      entries: staticIndexes.map((index) => lineEntry(primary, index, index === lowerIndex))
    };
  }

  if (count === 5) {
    const staticIndex = [0, 1, 2, 3, 4, 5].find((index) => !moving.some((item) => item.index === index));
    return {
      rule: "五爻变：取变卦中唯一静爻所对应的爻辞。",
      focus: changed.lines[staticIndex].label,
      entries: [lineEntry(changed, staticIndex, true)]
    };
  }

  const special =
    primary.number === 1
      ? primary.extras.find((item) => item.label === "用九")
      : primary.number === 2
        ? primary.extras.find((item) => item.label === "用六")
        : null;

  if (special) {
    return {
      rule: "六爻皆变：乾用用九，坤用用六。",
      focus: special.label,
      entries: [{ title: special.label, text: special.text, priority: true }]
    };
  }

  return {
    rule: "六爻皆变：乾坤之外，以变卦卦辞为主。",
    focus: `${changed.name}卦辞`,
    entries: [{ title: `${changed.name}卦辞`, text: changed.judgment, priority: true }]
  };
}

function renderLineGlyph(line) {
  if (line.yang) {
    return line.moving ? "⚊ ○" : "⚊";
  }
  return line.moving ? "⚋ ×" : "⚋";
}

function castHexagram(question, method, seed) {
  const rng = seed ? createSeededRng(seed) : randomRng();
  const lines = Array.from({ length: 6 }, () => tossLine(method, rng));
  const changedLines = lines.map((line) => ({
    ...line,
    yang: line.moving ? !line.yang : line.yang,
    moving: false
  }));

  const primary = resolveHexagram(lines);
  const changed = resolveHexagram(changedLines);
  const moving = lines
    .map((line, index) => ({ index, line }))
    .filter((item) => item.line.moving)
    .map((item) => ({
      index: item.index,
      position: POSITION_NAMES[item.index],
      originalLabel: primary.lines[item.index].label,
      lineType: item.line.label,
      text: primary.lines[item.index].text
    }));

  return {
    question,
    method,
    seed: seed || null,
    lines: lines.map((line, index) => ({
      index,
      position: POSITION_NAMES[index],
      lineType: line.label,
      value: line.value,
      moving: line.moving,
      yang: line.yang,
      coins: line.coins,
      glyph: renderLineGlyph(line)
    })),
    primary,
    changed,
    moving,
    decision: decideTextSource(primary, changed, moving)
  };
}

function lookupHexagramByName(name) {
  return ZHOUYI_BENJING.find((item) => item.name === name) || null;
}

function lookupHexagramByNumber(number) {
  const value = Number(number);
  if (!Number.isInteger(value) || value < 1 || value > 64) return null;
  return ZHOUYI_BENJING[value - 1];
}

function searchHexagrams(query) {
  const keyword = String(query || "").trim();
  return ZHOUYI_BENJING.filter((item) => {
    if (item.name.includes(keyword) || item.judgment.includes(keyword)) return true;
    if (item.lines.some((line) => line.text.includes(keyword) || line.label.includes(keyword))) return true;
    if (item.extras.some((extra) => extra.text.includes(keyword) || extra.label.includes(keyword))) return true;
    return false;
  }).map((item) => ({
    number: item.number,
    name: item.name,
    judgment: item.judgment
  }));
}

function filterCatalog(query, grade) {
  return DIVINATION_SYSTEMS.filter((item) => {
    const gradeOk = !grade || grade === "all" || item.grade === grade;
    if (!gradeOk) return false;
    if (!query) return true;
    const haystack = [
      item.name,
      item.family,
      item.basis,
      item.capability,
      item.guardrail,
      ...(item.bestFor || []),
      ...(item.inputs || [])
    ].join(" ");
    return haystack.includes(query);
  });
}

function print(payload, asJson, formatter) {
  if (asJson) {
    console.log(JSON.stringify(payload, null, 2));
    return;
  }
  console.log(formatter(payload));
}

function formatCast(payload) {
  const lines = payload.lines
    .slice()
    .reverse()
    .map((line) => `${line.position} ${line.glyph} ${line.lineType}`)
    .join("\n");
  const selected = payload.decision.entries
    .map((entry) => `${entry.title}${entry.priority ? " [主]" : ""}\n${entry.text}`)
    .join("\n\n");
  return [
    `问题：${payload.question || "未填写"}`,
    `方法：${payload.method}`,
    `本卦：${payload.primary.number}. ${payload.primary.fullName}`,
    `变卦：${payload.changed.number}. ${payload.changed.fullName}`,
    `动爻：${payload.moving.length ? payload.moving.map((item) => item.originalLabel).join("、") : "无"}`,
    "",
    lines,
    "",
    `取辞规则：${payload.decision.rule}`,
    selected
  ].join("\n");
}

function formatLookup(payload) {
  const lines = payload.lines.map((line) => `${line.label}：${line.text}`).join("\n");
  const extras = payload.extras.length ? `\n${payload.extras.map((item) => `${item.label}：${item.text}`).join("\n")}` : "";
  return `${payload.number}. ${payload.name}\n卦辞：${payload.judgment}\n${lines}${extras}`;
}

function formatSearch(results) {
  if (!results.length) return "未找到匹配卦象。";
  return results.map((item) => `${item.number}. ${item.name}：${item.judgment}`).join("\n");
}

function formatCatalog(results) {
  if (!results.length) return "未找到匹配体系。";
  return results
    .map((item) => `${item.grade} ${item.name} [${item.status}]\n依据：${item.basis}\n能力：${item.capability}\n边界：${item.guardrail}`)
    .join("\n\n");
}

function main() {
  const command = process.argv[2];
  const options = parseArgs(process.argv.slice(3));
  const asJson = Boolean(options.json || options.format === "json");

  if (!command || command === "help" || command === "--help" || command === "-h") {
    usage();
    process.exit(command ? 0 : 1);
  }

  if (command === "cast") {
    const method = options.method === "yarrow" ? "yarrow" : "coin";
    const payload = castHexagram(options.question || "", method, options.seed || "");
    print(payload, asJson, formatCast);
    return;
  }

  if (command === "lookup") {
    const result = options.name ? lookupHexagramByName(options.name) : lookupHexagramByNumber(options.number);
    if (!result) {
      console.error("未找到指定卦象。请提供 --name 或 --number。");
      process.exit(1);
    }
    print(result, asJson, formatLookup);
    return;
  }

  if (command === "search") {
    if (!options.query) {
      console.error("search 需要 --query。");
      process.exit(1);
    }
    const results = searchHexagrams(options.query);
    print(results, asJson, formatSearch);
    return;
  }

  if (command === "catalog") {
    const results = filterCatalog(options.query || "", options.grade || "all");
    print(results, asJson, formatCatalog);
    return;
  }

  console.error(`未知命令：${command}`);
  usage();
  process.exit(1);
}

main();
