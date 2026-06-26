#!/usr/bin/env node

import { buildHanziLookup, findRecordsOrThrow, readHanziRecords } from "./lib/hanzi.ts";
import type { HanziRecord, Wuxing } from "./lib/types.ts";

type GivenLenMode = "1" | "2" | "both";
type OutputFormat = "json" | "markdown";

type CliOptions = {
  surname?: string;
  givenLen: GivenLenMode;
  count: number;
  format: OutputFormat;
  favorableElement?: Wuxing;
  secondaryElement?: Wuxing;
  allowLevel2: boolean;
  disableNameFilter: boolean;
};

type CandidateResult = {
  given: string;
  givenLength: 1 | 2;
  score: number;
  scoreBreakdown: {
    elementPreferenceScore: number;
    elementScore: number;
    levelScore: number;
    repeatPenalty: number;
  };
  givenCharacters: Array<{
    char: string;
    kangxi: string | null;
    pinyin: string[];
    wugeStrokeCount: number;
    element: Wuxing | null;
    level: 1 | 2 | 3;
  }>;
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
  console.log(`Pick given-name candidates by favorable elements only (no WuGe scoring).

Usage:
  node scripts/pickNameByElement.ts [--surname <姓>] [--given-len <1|2|both>] [--count <N>]
                                    [--favorable-element <金|木|水|火|土>]
                                    [--secondary-element <金|木|水|火|土>]
                                    [--format <json|markdown>]
                                    [--allow-level2] [--disable-name-filter]

Options:
  --surname  Optional. 1-2 Chinese chars.
  --given-len  Optional. 1 | 2 | both. Default: both.
  --count  Optional. 1-100. Default: 50.
  --favorable-element  Optional. Primary favorable element.
  --secondary-element  Optional. Secondary favorable element.
  --format  Optional. json | markdown. Default: markdown.
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
        "allow-level2",
        "disable-name-filter",
      ].includes(key)
    ) {
      fail(`Unknown option: --${key}`);
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

  const surname = raw.surname;
  if (surname && (surname.length < 1 || surname.length > 2)) {
    fail(`Invalid --surname length: ${surname.length}. Allowed length is 1-2.`);
  }

  const givenLen = (raw["given-len"] ?? "both") as GivenLenMode;
  if (!["1", "2", "both"].includes(givenLen)) {
    fail(`Invalid --given-len: ${givenLen}. Allowed values: 1|2|both.`);
  }

  const countRaw = raw.count ?? "50";
  const count = Number.parseInt(countRaw, 10);
  if (!Number.isInteger(count) || count < 1 || count > 100) {
    fail(`Invalid --count: ${countRaw}. Allowed range: 1-100.`);
  }

  const formatRaw = raw.format ?? "markdown";
  if (formatRaw !== "json" && formatRaw !== "markdown") {
    fail(`Invalid --format: ${formatRaw}. Allowed values: json|markdown.`);
  }

  const favorableElement = raw["favorable-element"]
    ? parseWuxing(raw["favorable-element"], "--favorable-element")
    : undefined;
  const secondaryElement = raw["secondary-element"]
    ? parseWuxing(raw["secondary-element"], "--secondary-element")
    : undefined;

  if (!favorableElement && !secondaryElement) {
    fail("At least one of --favorable-element or --secondary-element is required.");
  }
  if (favorableElement && secondaryElement && favorableElement === secondaryElement) {
    fail("--favorable-element and --secondary-element cannot be the same.");
  }

  return {
    surname,
    givenLen,
    count,
    format: formatRaw,
    favorableElement,
    secondaryElement,
    allowLevel2,
    disableNameFilter,
  };
}

function normalizePinyin(input: string): string {
  return input
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z]/gi, "")
    .toLowerCase();
}

function isLikelyNameHanzi(record: HanziRecord): boolean {
  if (record.simplified.length !== 1) return false;
  if (NON_NAME_CHAR_SET.has(record.simplified)) return false;
  const normalized = normalizePinyin(record.pinyin[0] ?? "");
  if (!normalized) return false;
  if (NON_NAME_PINYIN.has(normalized)) return false;
  return true;
}

function buildHanziPool(records: HanziRecord[], options: CliOptions): HanziRecord[] {
  return records
    .filter((item) => (options.allowLevel2 ? item.level <= 2 : item.level === 1))
    .filter((item) => (options.disableNameFilter ? true : isLikelyNameHanzi(item)))
    .filter((item) => {
      if (!item.element) return false;
      if (options.favorableElement && item.element === options.favorableElement) return true;
      if (options.secondaryElement && item.element === options.secondaryElement) return true;
      return false;
    });
}

function getCharElementScore(record: HanziRecord, options: CliOptions): number {
  if (!record.element) return -999;
  if (options.favorableElement && record.element === options.favorableElement) return 30;
  if (options.secondaryElement && record.element === options.secondaryElement) return 16;
  return -999;
}

function getCharLevelScore(record: HanziRecord): number {
  return record.level === 1 ? 4 : record.level === 2 ? 1 : -2;
}

function buildCandidateResult(givenRecords: HanziRecord[], options: CliOptions): CandidateResult | null {
  const elementScore = givenRecords.reduce((sum, item) => sum + getCharElementScore(item, options), 0);
  if (elementScore < 0) {
    return null;
  }
  const levelScore = givenRecords.reduce((sum, item) => sum + getCharLevelScore(item), 0);
  const repeatPenalty = givenRecords.length === 2 && givenRecords[0].simplified === givenRecords[1].simplified ? -8 : 0;

  return {
    given: givenRecords.map((item) => item.simplified).join(""),
    givenLength: givenRecords.length as 1 | 2,
    score: elementScore + levelScore + repeatPenalty,
    scoreBreakdown: {
      elementPreferenceScore: elementScore,
      elementScore,
      levelScore,
      repeatPenalty,
    },
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

function buildSeedPool(pool: HanziRecord[], options: CliOptions, size: number): HanziRecord[] {
  return [...pool]
    .sort((a, b) => {
      const scoreDiff = getCharElementScore(b, options) - getCharElementScore(a, options);
      if (scoreDiff !== 0) return scoreDiff;
      const levelDiff = getCharLevelScore(b) - getCharLevelScore(a);
      if (levelDiff !== 0) return levelDiff;
      return a.simplified.localeCompare(b.simplified, "zh-Hans-CN");
    })
    .slice(0, Math.min(size, pool.length));
}

function topCandidates(candidates: CandidateResult[], count: number): CandidateResult[] {
  return candidates
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      if (a.givenLength !== b.givenLength) return a.givenLength - b.givenLength;
      return a.given.localeCompare(b.given, "zh-Hans-CN");
    })
    .slice(0, count);
}

function renderMarkdown(output: {
  input: {
    surname: string | null;
    givenLen: GivenLenMode;
    count: number;
    favorableElement: Wuxing | null;
    secondaryElement: Wuxing | null;
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
}): string {
  const lines: string[] = [
    "# 喜用神起名结果（仅看汉字五行）",
    "",
    `- 姓氏：${output.input.surname ?? "-"}`,
    `- 名字长度：${output.input.givenLen}`,
    `- 返回数量：${output.input.count}`,
    `- 喜用神主五行：${output.input.favorableElement ?? "-"}`,
    `- 喜用神次五行：${output.input.secondaryElement ?? "-"}`,
    "",
    "## 统计",
    `- 字池大小：${output.stats.hanziPoolSize}`,
    `- 单字生成：${output.stats.oneCharGenerated}`,
    `- 双字生成：${output.stats.twoCharGenerated}`,
    `- 实际返回：${output.stats.returned}`,
    "",
    "## 候选列表",
  ];

  if (output.results.length === 0) {
    lines.push("- 无候选结果");
    return lines.join("\n");
  }

  output.results.forEach((item, index) => {
    lines.push(
      "",
      `### ${index + 1}. ${item.given}（${item.givenLength}字名，${item.score}分）`,
      `- 维度分：喜用神=${item.scoreBreakdown.elementPreferenceScore}`,
      `- 分数拆解：element=${item.scoreBreakdown.elementScore}, level=${item.scoreBreakdown.levelScore}, repeat=${item.scoreBreakdown.repeatPenalty}`,
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

  if (options.surname) {
    try {
      findRecordsOrThrow(options.surname, lookup);
    } catch (error) {
      fail((error as Error).message);
    }
  }

  const pool = buildHanziPool(records, options);
  if (pool.length === 0) {
    fail("No hanzi available after filtering. Please relax element filters.");
  }

  const oneCharCandidates: CandidateResult[] = [];
  if (options.givenLen === "1" || options.givenLen === "both") {
    for (const c1 of pool) {
      const candidate = buildCandidateResult([c1], options);
      if (candidate) oneCharCandidates.push(candidate);
    }
  }

  const twoCharCandidates: CandidateResult[] = [];
  if (options.givenLen === "2" || options.givenLen === "both") {
    const firstPool = buildSeedPool(pool, options, 240);
    const secondPool = buildSeedPool(pool, options, 240);

    for (const c1 of firstPool) {
      for (const c2 of secondPool) {
        const candidate = buildCandidateResult([c1, c2], options);
        if (candidate) twoCharCandidates.push(candidate);
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
