#!/usr/bin/env node

import { buildHanziLookup, findRecordsOrThrow, readHanziRecords } from "./lib/hanzi.ts";
import {
  buildGeObject,
  getDige,
  getRelationDirection,
  getRenge,
  getTiange,
  getWaige,
  getZongge,
} from "./lib/wuge.ts";
import type { GeResult, HanziRecord, WugeRelationDirection, Wuxing } from "./lib/types.ts";

type OutputFormat = "json" | "markdown";

type AnalyzeOutput = {
  input: {
    surname: string | null;
    given: string;
    fullName: string;
    favorableElement: Wuxing | null;
    secondaryElement: Wuxing | null;
  };
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
  characters: Array<{
    index: number;
    input: string;
    simplified: string;
    kangxi: string | null;
    pinyin: string[];
    radical: string;
    strokeCount: number;
    wugeStrokeCount: number;
    element: Wuxing | null;
    level: 1 | 2 | 3;
  }>;
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
};

function luckScore(luck: string): number {
  if (luck === "吉") return 8;
  if (luck === "半吉") return 4;
  if (luck === "吉带凶" || luck === "凶带吉" || luck === "吉帶凶") return 1;
  if (luck === "吉凶各半") return 0;
  if (luck === "凶") return -5;
  return 0;
}

function relationScore(from: Wuxing, to: Wuxing): number {
  if (from === to) return 2;
  if ((from === "金" && to === "水") || (from === "水" && to === "木") || (from === "木" && to === "火") || (from === "火" && to === "土") || (from === "土" && to === "金")) return 3;
  if ((to === "金" && from === "水") || (to === "水" && from === "木") || (to === "木" && from === "火") || (to === "火" && from === "土") || (to === "土" && from === "金")) return -1;
  if ((from === "金" && to === "木") || (from === "木" && to === "土") || (from === "土" && to === "水") || (from === "水" && to === "火") || (from === "火" && to === "金")) return -4;
  return -2;
}

function parseWuxing(input: string, optionName: string): Wuxing {
  if (["金", "木", "水", "火", "土"].includes(input)) {
    return input as Wuxing;
  }
  fail(`Invalid ${optionName}: ${input}. Allowed values: 金|木|水|火|土.`);
}

function analyzeElementScore(element: Wuxing | null, favorableElement?: Wuxing, secondaryElement?: Wuxing): number {
  if (!favorableElement && !secondaryElement) {
    return 0;
  }
  if (!element) {
    return 0;
  }
  if (favorableElement && element === favorableElement) {
    return 50;
  }
  if (secondaryElement && element === secondaryElement) {
    return 25;
  }
  return -20;
}

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

function printUsage(): void {
  console.log(`Analyze Chinese name by San Cai & Wu Ge.

Usage:
  node scripts/analyzeName.ts [--surname <姓>] --given <名> [--format <json|markdown>]
                              [--favorable-element <金|木|水|火|土>]
                              [--secondary-element <金|木|水|火|土>]

Options:
  --surname  Optional. 1-2 Chinese chars.
  --given    Required. 1-2 Chinese chars.
  --format   Optional. json | markdown. Default: markdown.
  --favorable-element  Optional. Primary favorable element for scoring.
  --secondary-element  Optional. Secondary favorable element for scoring.
  --help     Print this help message.
`);
}

function parseArgs(argv: string[]): {
  surname?: string;
  given: string;
  format: OutputFormat;
  favorableElement?: Wuxing;
  secondaryElement?: Wuxing;
} {
  const args = argv.slice(2);
  if (args.length === 0 || args.includes("--help")) {
    printUsage();
    process.exit(0);
  }

  const raw: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    const current = args[i];
    if (!current.startsWith("--")) {
      fail(`Invalid argument: ${current}`);
    }
    const key = current.slice(2);
    if (![
      "surname",
      "given",
      "format",
      "favorable-element",
      "secondary-element",
    ].includes(key)) {
      fail(`Unknown option: --${key}`);
    }
    const value = args[i + 1];
    if (!value || value.startsWith("--")) {
      fail(`Option --${key} requires a value.`);
    }
    raw[key] = value.trim();
    i += 1;
  }

  const surname = raw["surname"];
  const given = raw["given"];
  if (!given) {
    fail("--given is required.");
  }
  if (surname && (surname.length < 1 || surname.length > 2)) {
    fail(`Invalid --surname length: ${surname.length}. Allowed length is 1-2.`);
  }
  if (given.length < 1 || given.length > 2) {
    fail(`Invalid --given length: ${given.length}. Allowed length is 1-2.`);
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

  return { surname, given, format: formatRaw as OutputFormat, favorableElement, secondaryElement };
}

function buildOutput(
  fullName: string,
  surname: string | undefined,
  records: HanziRecord[],
  favorableElement?: Wuxing,
  secondaryElement?: Wuxing,
): AnalyzeOutput {
  const surnameLen = surname?.length ?? 0;
  const xingRecords = records.slice(0, surnameLen);
  const mingRecords = records.slice(surnameLen);
  const xingStrokes = xingRecords.map((item) => item.wugeStrokeCount);
  const mingStrokes = mingRecords.map((item) => item.wugeStrokeCount);
  const hasSurname = xingStrokes.length > 0;

  const tiange = hasSurname ? buildGeObject(getTiange(xingStrokes)) : null;
  const renge = hasSurname ? buildGeObject(getRenge(xingStrokes, mingStrokes)) : null;
  const dige = hasSurname ? buildGeObject(getDige(mingStrokes)) : null;
  const waige = hasSurname ? buildGeObject(getWaige(xingStrokes, mingStrokes)) : null;
  const zongge = hasSurname ? buildGeObject(getZongge(xingStrokes, mingStrokes)) : null;
  const lScore =
    tiange && renge && dige && waige && zongge
      ? [tiange, renge, dige, waige, zongge].reduce((sum, item) => sum + luckScore(item.luck), 0)
      : 0;
  const rScore =
    tiange && renge && dige
      ? relationScore(tiange.wuxing, renge.wuxing) + relationScore(renge.wuxing, dige.wuxing)
      : 0;
  const eScore = mingRecords.reduce(
    (sum, item) => sum + analyzeElementScore(item.element ?? null, favorableElement, secondaryElement),
    0,
  );
  const lvScore = mingRecords.reduce((sum, item) => sum + (item.level === 1 ? 4 : item.level === 2 ? 1 : -2), 0);
  const repeatPenalty = mingRecords.length === 2 && mingRecords[0].simplified === mingRecords[1].simplified ? -8 : 0;
  const totalScore = lScore + rScore + eScore + lvScore + repeatPenalty;

  return {
    input: {
      surname: surname ?? null,
      given: fullName.slice(surnameLen),
      fullName,
      favorableElement: favorableElement ?? null,
      secondaryElement: secondaryElement ?? null,
    },
    score: totalScore,
    scoreBreakdown: {
      sancaiWugeScore: lScore + rScore,
      elementPreferenceScore: eScore,
      luckScore: lScore,
      relationScore: rScore,
      elementScore: eScore,
      levelScore: lvScore,
      repeatPenalty,
    },
    characters: records.map((record, index) => ({
      index: index + 1,
      input: fullName[index],
      simplified: record.simplified,
      kangxi: record.kangxi ?? null,
      pinyin: record.pinyin,
      radical: record.radical,
      strokeCount: record.strokeCount,
      wugeStrokeCount: record.wugeStrokeCount,
      element: record.element ?? null,
      level: record.level,
    })),
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
      tiange && renge && dige
        ? {
            pattern: `${tiange.wuxing}-${renge.wuxing}-${dige.wuxing}`,
            天人关系: getRelationDirection(renge.wuxing, tiange.wuxing),
            人地关系: getRelationDirection(renge.wuxing, dige.wuxing),
          }
        : null,
  };
}

function renderMarkdown(output: AnalyzeOutput): string {
  const lines = [
    `# 姓名分析结果`,
    ``,
    `- 姓名：${output.input.fullName}`,
    `- 姓：${output.input.surname ?? "（无）"}`,
    `- 名：${output.input.given}`,
    `- 喜用神主五行：${output.input.favorableElement ?? "-"}`,
    `- 喜用神次五行：${output.input.secondaryElement ?? "-"}`,
    `- 总分：${output.score}`,
    `- 维度分：喜用神=${output.scoreBreakdown.elementPreferenceScore}, 三才五格=${output.scoreBreakdown.sancaiWugeScore}`,
    `- 分数拆解：luck=${output.scoreBreakdown.luckScore}, relation=${output.scoreBreakdown.relationScore}, element=${output.scoreBreakdown.elementScore}, level=${output.scoreBreakdown.levelScore}, repeat=${output.scoreBreakdown.repeatPenalty}`,
    ``,
  ];

  if (output.sancai && output.wuge) {
    lines.push(
      `- 三才：${output.sancai.pattern}`,
      `- 天人关系：${output.sancai.天人关系}`,
      `- 人地关系：${output.sancai.人地关系}`,
      ``,
      `## 五格`,
      `### 天格`,
      `- 数值：${output.wuge.天格.number}`,
      `- 吉凶：${output.wuge.天格.luck}`,
      `- 数理五行：${output.wuge.天格.wuxing}`,
      ``,
      `### 人格`,
      `- 数值：${output.wuge.人格.number}`,
      `- 吉凶：${output.wuge.人格.luck}`,
      `- 数理五行：${output.wuge.人格.wuxing}`,
      ``,
      `### 地格`,
      `- 数值：${output.wuge.地格.number}`,
      `- 吉凶：${output.wuge.地格.luck}`,
      `- 数理五行：${output.wuge.地格.wuxing}`,
      ``,
      `### 外格`,
      `- 数值：${output.wuge.外格.number}`,
      `- 吉凶：${output.wuge.外格.luck}`,
      `- 数理五行：${output.wuge.外格.wuxing}`,
      ``,
      `### 总格`,
      `- 数值：${output.wuge.总格.number}`,
      `- 吉凶：${output.wuge.总格.luck}`,
      `- 数理五行：${output.wuge.总格.wuxing}`,
      ``,
    );
  } else {
    lines.push(`- 三才五格：未启用（未提供姓氏）`, ``);
  }

  lines.push(`## 用字明细`);

  for (const c of output.characters) {
    lines.push(
      ``,
      `### 第${c.index}字：${c.simplified}`,
      `- 康熙：${c.kangxi ?? "-"}`,
      `- 拼音：${c.pinyin.join("/")}`,
      `- 偏旁：${c.radical}`,
      `- 笔画：${c.strokeCount}`,
      `- 五格笔画：${c.wugeStrokeCount}`,
      `- 汉字五行：${c.element ?? "-"}`,
      `- 级别：${c.level}`,
    );
  }

  return lines.join("\n");
}

function main(): void {
  const { surname, given, format, favorableElement, secondaryElement } = parseArgs(process.argv);
  const fullName = `${surname ?? ""}${given}`;

  const records = readHanziRecords();
  const lookup = buildHanziLookup(records);

  let found: HanziRecord[];
  try {
    found = findRecordsOrThrow(fullName, lookup);
  } catch (error) {
    fail((error as Error).message);
  }

  const output = buildOutput(fullName, surname, found, favorableElement, secondaryElement);
  if (format === "markdown") {
    console.log(renderMarkdown(output));
    return;
  }
  console.log(JSON.stringify(output, null, 2));
}

main();
