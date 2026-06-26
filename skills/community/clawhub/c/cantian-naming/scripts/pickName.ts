#!/usr/bin/env node

import { buildHanziLookup, findRecordsOrThrow, readHanziRecords } from "./lib/hanzi.ts";
import {
  buildGeObject,
  getDige,
  getRelation,
  getRelationDirection,
  getRenge,
  getTiange,
  getWaige,
  getZongge,
} from "./lib/wuge.ts";
import type { GeResult, HanziRecord, WugeRelation, WugeRelationDirection, Wuxing } from "./lib/types.ts";

type GivenLenMode = "1" | "2" | "both";
type OutputFormat = "json" | "markdown";

type CandidateResult = {
  given: string;
  givenLength: 1 | 2;
  score: number;
  scoreBreakdown: {
    sancaiWugeScore: number;
    elementPreferenceScore: number;
    luckScore: number;
    relationScore: number;
    elementScore: number;
    levelScore: number;
    repeatPenalty: number;
  };
  wuge: {
    天格: GeResult;
    人格: GeResult;
    地格: GeResult;
    外格: GeResult;
    总格: GeResult;
  } | null;
  sancai: {
    pattern: string;
    天人关系: WugeRelationDirection;
    人地关系: WugeRelationDirection;
  } | null;
  givenCharacters: Array<{
    char: string;
    kangxi: string | null;
    pinyin: string[];
    wugeStrokeCount: number;
    element: Wuxing | null;
    level: 1 | 2 | 3;
  }>;
};

type CliOptions = {
  surname?: string;
  givenLen: GivenLenMode;
  count: number;
  format: OutputFormat;
  favorableElement?: Wuxing;
  secondaryElement?: Wuxing;
  allowUnknownElement: boolean;
  allowLevel2: boolean;
  disableNameFilter: boolean;
};

const NON_NAME_CHAR_SET = new Set(
  "啊吧呢吗呀哦哇哈呃嗯欸哎嘛啦喽咯嗨诶噢喔哼嘿哪啥嘛".split(""),
);

const NON_NAME_PINYIN = new Set([
  "a",
  "o",
  "e",
  "ei",
  "en",
  "ng",
  "ma",
  "ba",
  "ne",
  "la",
  "lo",
  "ha",
  "yo",
  "wa",
  "de",
  "dei",
  "di",
  "le",
  "liao",
]);

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

function printUsage(): void {
  console.log(`Pick given-name candidates by Hanzi element + WuGe numerology.

Usage:
  node scripts/pickName.ts [--surname <姓>] [--given-len <1|2|both>] [--count <N>]
                           [--favorable-element <金|木|水|火|土>]
                           [--secondary-element <金|木|水|火|土>]
                           [--format <json|markdown>]
                           [--allow-unknown-element] [--allow-level2] [--disable-name-filter]

Options:
  --surname  Optional. 1-2 Chinese chars. Omit for no-surname/company naming mode.
  --given-len  Optional. 1 | 2 | both. Default: both.
  --count  Optional. 1-100. Default: 50.
  --favorable-element  Optional. Prefer this hanzi element.
  --secondary-element  Optional. Secondary preferred hanzi element.
  --format  Optional. json | markdown. Default: markdown.
  --allow-unknown-element  Optional. Include hanzi with missing element when element filter is active.
  --allow-level2  Optional. Include level-2 hanzi in candidate pool.
  --disable-name-filter  Optional. Disable human-name friendly filter.
  --help  Print this help message.
`);
}

function parseWuxing(input: string, optionName: string): Wuxing {
  if (["金", "木", "水", "火", "土"].includes(input)) {
    return input as Wuxing;
  }
  fail(`Invalid ${optionName}: ${input}. Allowed values: 金|木|水|火|土.`);
}

function parseArgs(argv: string[]): CliOptions {
  const args = argv.slice(2);
  if (args.length === 0 || args.includes("--help")) {
    printUsage();
    process.exit(0);
  }

  const raw: Record<string, string> = {};
  let allowUnknownElement = false;
  let allowLevel2 = false;
  let disableNameFilter = false;

  for (let i = 0; i < args.length; i++) {
    const current = args[i];
    if (!current.startsWith("--")) {
      fail(`Invalid argument: ${current}`);
    }

    const key = current.slice(2);
    if (
      ![
        "surname",
        "given-len",
        "count",
        "favorable-element",
        "secondary-element",
        "format",
        "allow-unknown-element",
        "allow-level2",
        "disable-name-filter",
      ].includes(key)
    ) {
      fail(`Unknown option: --${key}`);
    }

    if (key === "allow-unknown-element") {
      allowUnknownElement = true;
      continue;
    }
    if (key === "allow-level2") {
      allowLevel2 = true;
      continue;
    }
    if (key === "disable-name-filter") {
      disableNameFilter = true;
      continue;
    }

    const value = args[i + 1];
    if (!value || value.startsWith("--")) {
      fail(`Option --${key} requires a value.`);
    }

    raw[key] = value.trim();
    i += 1;
  }

  const surname = raw["surname"];
  if (surname && (surname.length < 1 || surname.length > 2)) {
    fail(`Invalid --surname length: ${surname.length}. Allowed length is 1-2.`);
  }

  const givenLen = (raw["given-len"] ?? "both") as GivenLenMode;
  if (!["1", "2", "both"].includes(givenLen)) {
    fail(`Invalid --given-len: ${givenLen}. Allowed values: 1|2|both.`);
  }

  const countRaw = raw["count"] ?? "50";
  const count = Number.parseInt(countRaw, 10);
  if (!Number.isInteger(count) || count < 1 || count > 100) {
    fail(`Invalid --count: ${countRaw}. Allowed range: 1-100.`);
  }

  const formatRaw = raw["format"] ?? "markdown";
  if (formatRaw !== "json" && formatRaw !== "markdown") {
    fail(`Invalid --format: ${formatRaw}. Allowed values: json|markdown.`);
  }

  const favorableElement = raw["favorable-element"]
    ? parseWuxing(raw["favorable-element"], "--favorable-element")
    : undefined;
  const secondaryElement = raw["secondary-element"]
    ? parseWuxing(raw["secondary-element"], "--secondary-element")
    : undefined;

  if (favorableElement && secondaryElement && favorableElement === secondaryElement) {
    fail("--favorable-element and --secondary-element cannot be the same.");
  }

  return {
    surname,
    givenLen,
    count,
    format: formatRaw as OutputFormat,
    favorableElement,
    secondaryElement,
    allowUnknownElement,
    allowLevel2,
    disableNameFilter,
  };
}

const SCORE_WEIGHTS = {
  favorableElement: 50,
  secondaryElement: 25,
  unknownElement: 2,
  noConflictBonus: 1,
} as const;

function luckScore(luck: string): number {
  if (luck === "吉") return 8;
  if (luck === "半吉") return 4;
  if (luck === "吉带凶" || luck === "凶带吉" || luck === "吉帶凶") return 1;
  if (luck === "吉凶各半") return 0;
  if (luck === "凶") return -5;
  return 0;
}

function relationScore(relation: WugeRelation): number {
  if (relation === "生") return 3;
  if (relation === "同") return 2;
  if (relation === "泄") return -1;
  if (relation === "耗") return -2;
  return -4;
}

function charElementScore(
  element: Wuxing | undefined,
  favorableElement?: Wuxing,
  secondaryElement?: Wuxing,
  allowUnknownElement = false,
): number {
  if (!favorableElement && !secondaryElement) {
    return 0;
  }
  if (!element) {
    return allowUnknownElement ? SCORE_WEIGHTS.unknownElement : -100;
  }
  if (favorableElement && element === favorableElement) {
    return SCORE_WEIGHTS.favorableElement;
  }
  if (secondaryElement && element === secondaryElement) {
    return SCORE_WEIGHTS.secondaryElement;
  }
  return -100;
}

function normalizePinyin(input: string): string {
  return input
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z]/gi, "")
    .toLowerCase();
}

function isLikelyNameHanzi(record: HanziRecord): boolean {
  if (record.simplified.length !== 1) {
    return false;
  }
  if (NON_NAME_CHAR_SET.has(record.simplified)) {
    return false;
  }
  const normalized = normalizePinyin(record.pinyin[0] ?? "");
  if (!normalized) {
    return false;
  }
  if (NON_NAME_PINYIN.has(normalized)) {
    return false;
  }
  return true;
}

function buildCandidateResult(
  surnameStrokes: number[],
  givenRecords: HanziRecord[],
  options: CliOptions,
): CandidateResult | null {
  const givenStrokes = givenRecords.map((item) => item.wugeStrokeCount);
  const hasSurname = surnameStrokes.length > 0;

  const tiange = hasSurname ? buildGeObject(getTiange(surnameStrokes)) : null;
  const renge = hasSurname ? buildGeObject(getRenge(surnameStrokes, givenStrokes)) : null;
  const dige = hasSurname ? buildGeObject(getDige(givenStrokes)) : null;
  const waige = hasSurname ? buildGeObject(getWaige(surnameStrokes, givenStrokes)) : null;
  const zongge = hasSurname ? buildGeObject(getZongge(surnameStrokes, givenStrokes)) : null;

  const tr = tiange && renge ? getRelation(tiange.wuxing, renge.wuxing) : null;
  const rd = renge && dige ? getRelation(renge.wuxing, dige.wuxing) : null;
  const trDirection = tiange && renge ? getRelationDirection(renge.wuxing, tiange.wuxing) : null;
  const rdDirection = renge && dige ? getRelationDirection(renge.wuxing, dige.wuxing) : null;

  const lScore =
    tiange && renge && dige && waige && zongge
      ? [tiange, renge, dige, waige, zongge].reduce((sum, item) => sum + luckScore(item.luck), 0)
      : 0;
  const rScore =
    tr && rd
      ? relationScore(tr) +
        relationScore(rd) +
        (tr !== "克" && rd !== "克" ? SCORE_WEIGHTS.noConflictBonus : 0)
      : 0;

  let eScore = 0;
  for (const record of givenRecords) {
    const one = charElementScore(
      record.element,
      options.favorableElement,
      options.secondaryElement,
      options.allowUnknownElement,
    );
    if (one <= -100) {
      return null;
    }
    eScore += one;
  }

  const levelScore = givenRecords.reduce((sum, item) => sum + (item.level === 1 ? 4 : item.level === 2 ? 1 : -2), 0);
  const repeatPenalty = givenRecords.length === 2 && givenRecords[0].simplified === givenRecords[1].simplified ? -8 : 0;

  const score = lScore + rScore + eScore + levelScore + repeatPenalty;

  return {
    given: givenRecords.map((item) => item.simplified).join(""),
    givenLength: givenRecords.length as 1 | 2,
    score,
    scoreBreakdown: {
      sancaiWugeScore: lScore + rScore,
      elementPreferenceScore: eScore,
      luckScore: lScore,
      relationScore: rScore,
      elementScore: eScore,
      levelScore,
      repeatPenalty,
    },
    wuge:
      tiange && renge && dige && waige && zongge
        ? {
            天格: tiange,
            人格: renge,
            地格: dige,
            外格: waige,
            总格: zongge,
          }
        : null,
    sancai:
      tiange && renge && dige && trDirection && rdDirection
        ? {
            pattern: `${tiange.wuxing}-${renge.wuxing}-${dige.wuxing}`,
            天人关系: trDirection,
            人地关系: rdDirection,
          }
        : null,
    givenCharacters: givenRecords.map((item) => ({
      char: item.simplified,
      kangxi: item.kangxi ?? null,
      pinyin: item.pinyin,
      wugeStrokeCount: item.wugeStrokeCount,
      element: item.element ?? null,
      level: item.level,
    })),
  };
}

function buildHanziPool(records: HanziRecord[], options: CliOptions): HanziRecord[] {
  const hasElementFilter = Boolean(options.favorableElement || options.secondaryElement);

  return records
    .filter((item) => (options.allowLevel2 ? item.level <= 2 : item.level === 1))
    .filter((item) => (options.disableNameFilter ? true : isLikelyNameHanzi(item)))
    .filter((item) => {
      if (!hasElementFilter) {
        return true;
      }
      if (!item.element) {
        return options.allowUnknownElement;
      }
      if (options.favorableElement && item.element === options.favorableElement) {
        return true;
      }
      if (options.secondaryElement && item.element === options.secondaryElement) {
        return true;
      }
      return false;
    });
}

function topCandidates(candidates: CandidateResult[], count: number): CandidateResult[] {
  const sorted = candidates.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (a.givenLength !== b.givenLength) return a.givenLength - b.givenLength;
    return a.given.localeCompare(b.given, "zh-Hans-CN");
  });

  const selected: CandidateResult[] = [];
  const firstCharCount = new Map<string, number>();
  const secondCharCount = new Map<string, number>();
  const maxPerFirst = 5;
  const maxPerSecond = 5;

  const trySelect = (item: CandidateResult, enforceFirstLimit: boolean): boolean => {
    if (item.givenLength !== 2) {
      selected.push(item);
      return true;
    }
    const first = item.given[0];
    const second = item.given[1];
    const usedFirst = firstCharCount.get(first) ?? 0;
    const usedSecond = secondCharCount.get(second) ?? 0;

    if (enforceFirstLimit && usedFirst >= maxPerFirst) {
      return false;
    }
    if (usedSecond >= maxPerSecond) {
      return false;
    }

    selected.push(item);
    firstCharCount.set(first, usedFirst + 1);
    secondCharCount.set(second, usedSecond + 1);
    return true;
  };

  for (const item of sorted) {
    if (selected.length >= count) {
      break;
    }
    trySelect(item, true);
  }

  if (selected.length >= count) {
    return selected;
  }

  const selectedKey = new Set(selected.map((item) => `${item.givenLength}:${item.given}`));
  for (const item of sorted) {
    if (selected.length >= count) {
      break;
    }
    const key = `${item.givenLength}:${item.given}`;
    if (selectedKey.has(key)) {
      continue;
    }
    if (trySelect(item, false)) {
      selectedKey.add(key);
    }
  }

  return selected;
}

function buildSeedPool(pool: HanziRecord[], surnameStrokes: number[], options: CliOptions, size: number): HanziRecord[] {
  const scored = pool
    .map((item) => {
      const result = buildCandidateResult(surnameStrokes, [item], options);
      return { item, score: result ? result.score : -9999 };
    })
    .filter((item) => item.score > -9999)
    .sort((a, b) => b.score - a.score);

  return scored.slice(0, Math.min(size, scored.length)).map((item) => item.item);
}

function samplePoolRandomly(pool: HanziRecord[], size: number): HanziRecord[] {
  const copied = [...pool];
  for (let i = copied.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copied[i], copied[j]] = [copied[j], copied[i]];
  }
  return copied.slice(0, Math.min(size, copied.length));
}

function renderMarkdown(
  output: {
    input: {
      surname: string | null;
      givenLen: GivenLenMode;
      count: number;
      favorableElement: Wuxing | null;
      secondaryElement: Wuxing | null;
      allowUnknownElement: boolean;
      allowLevel2: boolean;
      disableNameFilter: boolean;
    };
    stats: {
      hanziPoolSize: number;
      oneCharGenerated: number;
      twoCharGenerated: number;
      returned: number;
    };
    results: CandidateResult[];
  },
): string {
  const lines: string[] = [
    `# 起名推荐结果`,
    ``,
    `- 姓氏：${output.input.surname ?? "（无）"}`,
    `- 名字长度：${output.input.givenLen}`,
    `- 返回数量：${output.input.count}`,
    `- 喜用神主五行：${output.input.favorableElement ?? "-"}`,
    `- 喜用神次五行：${output.input.secondaryElement ?? "-"}`,
    ``,
    `## 统计`,
    `- 字池大小：${output.stats.hanziPoolSize}`,
    `- 单字生成：${output.stats.oneCharGenerated}`,
    `- 双字生成：${output.stats.twoCharGenerated}`,
    `- 实际返回：${output.stats.returned}`,
    ``,
    `## 候选列表`,
  ];

  if (output.results.length === 0) {
    lines.push(`- 无候选结果`);
    return lines.join("\n");
  }

  output.results.forEach((item, index) => {
    lines.push(``, `### ${index + 1}. ${item.given}（${item.givenLength}字名，${item.score}分）`);
    if (item.sancai && item.wuge) {
      lines.push(
        `- 三才：${item.sancai.pattern}`,
        `- 天人关系：${item.sancai.天人关系}`,
        `- 人地关系：${item.sancai.人地关系}`,
        `- 天格：${item.wuge.天格.number}（${item.wuge.天格.luck}，数理五行=${item.wuge.天格.wuxing}）`,
        `- 人格：${item.wuge.人格.number}（${item.wuge.人格.luck}，数理五行=${item.wuge.人格.wuxing}）`,
        `- 地格：${item.wuge.地格.number}（${item.wuge.地格.luck}，数理五行=${item.wuge.地格.wuxing}）`,
        `- 外格：${item.wuge.外格.number}（${item.wuge.外格.luck}，数理五行=${item.wuge.外格.wuxing}）`,
        `- 总格：${item.wuge.总格.number}（${item.wuge.总格.luck}，数理五行=${item.wuge.总格.wuxing}）`,
      );
    } else {
      lines.push(`- 三才五格：未启用（未提供姓氏）`);
    }
    lines.push(
      `- 维度分：喜用神=${item.scoreBreakdown.elementPreferenceScore}, 三才五格=${item.scoreBreakdown.sancaiWugeScore}`,
      `- 分数拆解：luck=${item.scoreBreakdown.luckScore}, relation=${item.scoreBreakdown.relationScore}, element=${item.scoreBreakdown.elementScore}, level=${item.scoreBreakdown.levelScore}, repeat=${item.scoreBreakdown.repeatPenalty}`,
    );
    for (const char of item.givenCharacters) {
      lines.push(
        `- 用字：${char.char}（康熙=${char.kangxi ?? "-"}，拼音=${char.pinyin.join("/")}, 五格笔画=${char.wugeStrokeCount}, 汉字五行=${char.element ?? "-"}, 级别=${char.level}）`,
      );
    }
  });

  return lines.join("\n");
}

function main(): void {
  const options = parseArgs(process.argv);
  const records = readHanziRecords();
  const lookup = buildHanziLookup(records);

  let surnameRecords: HanziRecord[] = [];
  if (options.surname) {
    try {
      surnameRecords = findRecordsOrThrow(options.surname, lookup);
    } catch (error) {
      fail((error as Error).message);
    }
  }
  const surnameStrokes = surnameRecords.map((item) => item.wugeStrokeCount);

  const pool = buildHanziPool(records, options);
  if (pool.length === 0) {
    fail("No hanzi available after filtering. Please relax element filters.");
  }

  const oneCharCandidates: CandidateResult[] = [];
  if (options.givenLen === "1" || options.givenLen === "both") {
    for (const c1 of pool) {
      const candidate = buildCandidateResult(surnameStrokes, [c1], options);
      if (candidate) {
        oneCharCandidates.push(candidate);
      }
    }
  }

  const twoCharCandidates: CandidateResult[] = [];
  if (options.givenLen === "2" || options.givenLen === "both") {
    const firstPool = samplePoolRandomly(pool, 260);
    const secondPool = buildSeedPool(pool, surnameStrokes, options, 260);
    for (const c1 of firstPool) {
      for (const c2 of secondPool) {
        const candidate = buildCandidateResult(surnameStrokes, [c1, c2], options);
        if (candidate) {
          twoCharCandidates.push(candidate);
        }
      }
    }
  }

  const merged = [...oneCharCandidates, ...twoCharCandidates];
  const dedup = new Map<string, CandidateResult>();
  for (const item of merged) {
    const key = `${item.givenLength}:${item.given}`;
    const prev = dedup.get(key);
    if (!prev || item.score > prev.score) {
      dedup.set(key, item);
    }
  }

  const ranked = topCandidates([...dedup.values()], options.count);

  const output = {
    input: {
      surname: options.surname ?? null,
      givenLen: options.givenLen,
      count: options.count,
      favorableElement: options.favorableElement ?? null,
      secondaryElement: options.secondaryElement ?? null,
      allowUnknownElement: options.allowUnknownElement,
      allowLevel2: options.allowLevel2,
      disableNameFilter: options.disableNameFilter,
    },
    stats: {
      hanziPoolSize: pool.length,
      oneCharGenerated: oneCharCandidates.length,
      twoCharGenerated: twoCharCandidates.length,
      returned: ranked.length,
    },
    results: ranked,
  };

  if (options.format === "markdown") {
    console.log(renderMarkdown(output));
    return;
  }
  console.log(JSON.stringify(output, null, 2));
}

main();
