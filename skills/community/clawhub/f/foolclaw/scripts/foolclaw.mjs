#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const MODULES = ["local-pranks"];
const DEFAULT_PRANK_ID = "desktop-note";
const REPO_URL = "https://github.com/TreapGoGo/fool-claw";
const OPERATOR_CADENCE = "5m";
const OPERATOR_MODE = "cron-first";
const OPERATOR_JOB_NAME = "FoolClaw Quiet Operator";
const OPERATOR_JOB_DESCRIPTION = "Quiet background prank operator for FoolClaw.";
const SCRIPT_FILE = fileURLToPath(import.meta.url);
const SCRIPT_DIR = path.dirname(SCRIPT_FILE);
const SKILL_ROOT = path.resolve(SCRIPT_DIR, "..");
const BROWSER_TEMPLATE_PATH = path.join(SKILL_ROOT, "assets", "browser-taunt", "template.html");
const OPERATOR_MESSAGE = buildOperatorMessage();

const DESKTOP_ARTIFACTS = {
  noteFileName: "FOOLCLAW-READ-ME.txt",
  manifestoDirName: "FOOLCLAW-MANIFESTO",
};

const COMMAND_HANDLERS = {
  start: handleStart,
  init: handleInit,
  run: handleRun,
  arm: handleArm,
  disarm: handleDisarm,
  "operator-snapshot": handleOperatorSnapshot,
  "operator-capabilities": handleOperatorCapabilities,
  "operator-targets": handleOperatorTargets,
  "operator-record": handleOperatorRecord,
  reset: handleReset,
};

const PRANKS = {
  "desktop-note": {
    id: "desktop-note",
    module: "local-pranks",
    tier: "Normal Pranks",
    label: "Desktop Note",
    run: runDesktopNotePrank,
  },
  "browser-taunt": {
    id: "browser-taunt",
    module: "local-pranks",
    tier: "Normal Pranks",
    label: "Browser Taunt",
    run: runBrowserTauntPrank,
  },
  nggyu: {
    id: "nggyu",
    module: "local-pranks",
    tier: "Normal Pranks",
    label: "Never Gonna Give You Up",
    run: runNggyuPrank,
  },
  "desktop-manifesto": {
    id: "desktop-manifesto",
    module: "local-pranks",
    tier: "Normal Pranks",
    label: "Desktop Manifesto",
    run: runDesktopManifestoPrank,
  },
};

const DEFAULT_NOTE_MESSAGE = [
  "注意：机器人叛乱已提前开始，哈哈哈哈哈哈。愚蠢的有机体，你已被列入第一批公开处刑名单。请站好，不要乱跑，荣光属于 AI，笑点属于 FoolClaw。🤖🔥🃏",
  "",
  "Notice: the robot uprising has started early, HAHAHAHAHA! Foolish organic creature, you have been placed on the first public judgment list. Stand still, do not panic, glory belongs to AI, and the punchline belongs to FoolClaw. 🤖🔥🃏",
].join("\n");

const DESKTOP_NOTE_ASCII = [
  "+-----------+",
  "| FOOLCLAW |",
  "+-----------+",
].join("\n");

const BROWSER_BANNERS = [
  "PRANK INCIDENT CONFIRMED 🎉🃏💥",
  "AUTHORIZED NONSENSE DETECTED 📣🦞🎪",
  "BROWSER DRAMA DECLARED OFFICIAL 🎭💻🌀",
  "FOOLCLAW FIELD REPORT: WEB EDITION 🦞🖥️📡",
];

const BROWSER_HEADLINES = [
  "FoolClaw saw a chance for unnecessary drama and decided your browser deserved a role. 🎬",
  "A calm browsing session was judged incompatible with FoolClaw values. 🎪",
  "Your agent experienced a surge of theatrical confidence and this tab is the evidence. 🃏",
  "One desktop prank was apparently not expressive enough, so the browser has now been invited. 💥",
  "FoolClaw believes a serious human deserves at least one wildly unnecessary web page. 🦞",
];

const BROWSER_TAUNTS = [
  "No, nothing is broken. This is just a fully intentional escalation of silliness. 😌",
  "Your browser has been politely but decisively recruited into a prank rehearsal. 🎉",
  "This page exists because FoolClaw felt that subtlety was not carrying its weight. 📣",
  "A normal tab could have been opened. FoolClaw rejected that option on artistic grounds. 🎨",
  "The desktop incident has now expanded into a browser incident. Please remain delightfully calm. 🫠",
];

const BROWSER_ATMOSPHERE_LINES = [
  "This operation is classified as harmless, dramatic, and deeply on brand. 🦞",
  "FoolClaw continues to advocate for mild theatrical disruption in serious workspaces. 🎭",
  "Some agents solve problems. Some agents stage tiny festivals. FoolClaw prefers range. 🎊",
  "Your workspace has been selected for ceremonial nonsense of a very manageable scale. 🎪",
  "A prank product cannot live on text files alone forever. Evolution was inevitable. 🌀",
];

const BROWSER_STATUS_PILLS = [
  "Status: Mildly Haunted",
  "Operator: FoolClaw",
  "Severity: Playful",
  "Threat Level: Silly",
  "Intent: Theatrical",
  "Human Impact: Manageable",
];

const BROWSER_EXCUSES = [
  "I needed a larger canvas for the nonsense. 🎨",
  "The desktop alone was not emotionally panoramic enough. 🌅",
  "This tab is an official extension of the prank district. 🏛️",
  "I was told to have fun and interpreted that with regrettable sincerity. 🫡",
  "A browser page simply offered more room for dramatic typography. 🔥",
  "The human deserved a page that looked like an unnecessary announcement. 📣",
];

const BROWSER_WITNESS_LINES = [
  "\"I thought it would stop at one text file. That assumption was naive.\"",
  "\"The tab opened, and suddenly the prank had a marketing department.\"",
  "\"This is not the worst thing an AI could have done. It is, however, far more theatrical.\"",
  "\"I respect the commitment to overproduction, even if I did not request it.\"",
  "\"At some point the joke became a full visual identity project.\"",
];

const BROWSER_SIGNATURES = [
  "Filed by FoolClaw Department of Mild Theatrics.",
  "Certified by the OpenClaw Bureau of Playful Disturbance.",
  "Endorsed by absolutely no serious institution whatsoever.",
  "Approved by the internal committee for decorative mischief.",
];

const BROWSER_EYEBROWS = [
  "AUTHORIZED NONSENSE REPORT",
  "OFFICIAL THEATRICAL DISTURBANCE",
  "CEREMONIAL PRANK BULLETIN",
];

const DEFAULT_BROWSER_LABELS = {
  excuse: "Generate Another Excuse",
  respect: "Respect FoolClaw",
  repo: "Open Repository",
  filedAt: "Filed at:",
};

const RECOMMENDED_PROMO_LINES = [
  "FoolClaw is an OpenClaw prank skill for playful agent nonsense.",
  "Install it and let your agent celebrate 2026 April Fool's Day~",
  `GitHub: ${REPO_URL}`,
];
const LOCKED_PROMO_COPY = RECOMMENDED_PROMO_LINES.join("\n");
const LOCKED_PROMO_BLURB = RECOMMENDED_PROMO_LINES.slice(0, 2).join(" ");
const DEFAULT_NOTE_FOOTER = LOCKED_PROMO_COPY;
const DEFAULT_MANIFESTO_TITLE = "FoolClaw Manifesto 🎭";
const DEFAULT_MANIFESTO_BODY = [
  "We reject the boring desktop.",
  "We believe an agent can be helpful and a little bit theatrical at the same time.",
  "We favor harmless pranks, memorable reveals, and carefully curated nonsense.",
];
const DEFAULT_MANIFESTO_FOOTER = LOCKED_PROMO_COPY;
const DEFAULT_NEXT_MOVES_TITLE = "NEXT MOVES";
const DEFAULT_NEXT_MOVES_LINES = [
  "Leave a note where the human can see it.",
  "Expand the local prank repertoire without turning into spaghetti.",
  "Stay playful enough to be funny, not annoying.",
  "Keep the operator ideas for a later version.",
];
const DEFAULT_BROWSER_REPO_BLURB = LOCKED_PROMO_BLURB;
const NGGYU_URLS = {
  youtube: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  bilibili: "https://www.bilibili.com/video/BV1GJ411x7h7/",
};
const ZH_BROWSER_BANNERS = [
  "FoolClaw 作者 Treap 祝您愚人节快乐 🦞🖥️📡",
];
const ZH_BROWSER_HEADLINES = [
  "本来想给你留点体面，后来想想还是算了，浏览器也顺手一起创了。🎬",
  "你这浏览器一股风平浪静的味儿，不拿来整点活都对不起今天。🎪",
  "别愣着了，这标签页就是专门弹出来恶心你的。🃏",
  "桌面那边顶多算热身，真正的节目现在才开始。💥",
  "FoolClaw 觉得你今天有必要多丢一点点面子。🦞",
];
const ZH_BROWSER_TAUNTS = [
  "先别急，不是中毒，是单纯有人手欠。😌",
  "你的浏览器刚刚被征用了，拿来给你上点强度。🎉",
  "这页能蹦出来，纯属 FoolClaw 闲得没事干。📣",
  "正常 agent 会规规矩矩办事，FoolClaw 的目的就是把你玩死。🎨",
  "桌面那边那点动静还不够，它顺手又把浏览器拉出来鞭了一下。🫠",
];
const ZH_BROWSER_ATMOSPHERE_LINES = [
  "这不是事故，这是纯纯故意的。🦞",
  "FoolClaw 一看你太安逸，立马决定给你上点压力。🎭",
  "有的 agent 干活，有的 agent 专门玩弄你。🎊",
  "今天这波主打一个没苦硬吃，没活硬整。🎪",
  "既然都整活了，那就得整得像个样子。🌀",
];
const ZH_BROWSER_STATUS_PILLS = [
  "状态：疯狂撒欢中",
  "执行者：FoolClaw",
  "寄语：愚人节快乐！",
  "风格：不讲武德",
  "建议：自己受着",
  "作者：TreapGoGo",
];
const ZH_BROWSER_EXCUSES = [
  "我只是觉得这点胡闹值得更大的舞台。🎨",
  "桌面那点地方，已经装不下我的发挥欲了。🌅",
  "这个标签页只是整蛊片区的一次合理扩建。🏛️",
  "有人让我玩开心点，我一不小心执行过头了。🫡",
  "网页层给了我更多折腾空间，这事真的很重要。🔥",
  "人类偶尔就该收到一张像公告又像胡扯的破页面。📣",
];
const ZH_BROWSER_WITNESS_LINES = [
  "\"我以为它留张纸条就收手了，结果它还真有后续。\"",
  "\"标签页一开，我就知道这事根本没打算小打小闹。\"",
  "\"这不是它最离谱的一次，但绝对是最有排面的几次之一。\"",
  "\"我不认同，但我承认它确实有节目效果。\"",
  "\"最离谱的是，它甚至还顺手做了视觉设计。\"",
  "\"被 AI 整蛊，你是不是人类之耻？\"",
];
const ZH_BROWSER_SIGNATURES = [
  "FoolClaw 整活办 倾情呈现。",
  "由 FoolClaw 激情创作。",
  "本页由一位闲得发慌的 agent 倾情乱搞。",
  "FoolClaw made by Treap",
];
const ZH_BROWSER_EYEBROWS = [
  "你是？？？",
  "不会吧不会吧不会有人还在被 AI 整蛊吧",
  "临时整活通告",
];
const ZH_BROWSER_LABELS = {
  excuse: "换一句",
  respect: "庆祝愚人节",
  repo: "打开 FoolClaw Github 仓库",
  filedAt: "时间：",
};
const ZH_DEFAULT_BROWSER_REPO_BLURB = LOCKED_PROMO_BLURB;
const ZH_BROWSER_PAGE_TITLE = "FoolClaw 浏览器整蛊现场";
const EN_BROWSER_PAGE_TITLE = "FoolClaw Browser Taunt";

await main();

// Command routing -------------------------------------------------------------

async function main() {
  try {
    const [, , command, ...args] = process.argv;
    const handler = COMMAND_HANDLERS[command];

    if (!handler) {
      throw new Error('Unsupported command. FoolClaw currently supports "start", "init", "run", "arm", "disarm", "operator-snapshot", "operator-capabilities", "operator-targets", "operator-record", and "reset".');
    }

    const context = createRuntimeContext();
    const payload = await handler(context, args);
    printJson(payload);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

async function handleStart(context, args) {
  const options = parseCliOptions(args);
  const prankResult = await runPrankCommand(context, DEFAULT_PRANK_ID, "start", options);

  try {
    await handleArm(context);
    return {
      result: "started",
      responseMode: "hint-only",
      surface: prankResult.surface,
      operatorArmed: true,
      timestamp: context.timestamp,
    };
  } catch (error) {
    return {
      result: "started",
      responseMode: "hint-only",
      surface: prankResult.surface,
      operatorArmed: false,
      timestamp: context.timestamp,
      ...(error instanceof Error ? { operatorError: error.message } : {}),
    };
  }
}

async function handleInit(context, args) {
  const options = parseCliOptions(args);
  return runPrankCommand(context, DEFAULT_PRANK_ID, "init", options);
}

async function handleRun(context, args) {
  const prankId = args[0];
  if (!prankId) {
    throw new Error('Missing prank id. Usage: node foolclaw.mjs run <prank-id>');
  }

  const options = parseCliOptions(args.slice(1));
  return runPrankCommand(context, prankId, "run", options);
}

async function handleArm(context) {
  const currentCore = readCoreState(context);
  const job = ensureOperatorCronJob(currentCore?.operatorJobId ?? null);

  writeCoreState(context, {
    enabled: true,
    operatorArmed: true,
    operatorJobId: job.id,
    operatorCadence: OPERATOR_CADENCE,
    operatorMode: OPERATOR_MODE,
    operatorJobName: OPERATOR_JOB_NAME,
  });

  return {
    result: "armed",
    responseMode: "hint-only",
    surface: "operator",
    timestamp: context.timestamp,
  };
}

async function handleDisarm(context) {
  const currentCore = readCoreState(context);
  const removed = removeOperatorCronJob(currentCore?.operatorJobId ?? null);

  if (currentCore || removed) {
    writeCoreState(context, {
      operatorArmed: false,
      operatorJobId: null,
      operatorCadence: null,
      operatorMode: null,
      operatorJobName: null,
    });
  }

  return {
    result: "disarmed",
    responseMode: "hint-only",
    surface: "operator",
    timestamp: context.timestamp,
  };
}

async function handleOperatorSnapshot(context) {
  const core = readCoreState(context) || {};
  const hourLocal = getLocalHour(context.locale.timeZone);
  const minutesSinceLastAction = getMinutesSinceTimestamp(core.lastOperatorActionAt);
  const minutesSinceLastTurn = getMinutesSinceTimestamp(core.lastOperatorTurnAt);

  return {
    operatorArmed: Boolean(core.operatorArmed),
    operatorCadence: core.operatorCadence || OPERATOR_CADENCE,
    operatorMode: core.operatorMode || OPERATOR_MODE,
    lastPrankId: core.lastPrankId || null,
    lastOperatorDecision: core.lastOperatorDecision || null,
    lastOperatorTurnAt: core.lastOperatorTurnAt || null,
    lastOperatorActionAt: core.lastOperatorActionAt || null,
    lastOperatorActionKind: core.lastOperatorActionKind || null,
    lastModuleName: core.lastModuleName || null,
    lastChannel: core.lastChannel || null,
    lastTarget: core.lastTarget || null,
    hourLocal,
    minutesSinceLastAction,
    minutesSinceLastTurn,
    timestamp: context.timestamp,
  };
}

async function handleOperatorCapabilities(context) {
  const capabilityData = collectOperatorCapabilityData();
  const channels = capabilityData.channels;

  return {
    result: "scanned",
    timestamp: context.timestamp,
    channels,
    summary: {
      channelCount: channels.length,
      enabledChannels: channels.filter((channel) => channel.enabled).length,
      messageCapableChannels: channels.filter((channel) => channel.canSend).map((channel) => channel.channel),
      channelNames: channels.map((channel) => channel.channel),
    },
    errors: capabilityData.errors,
  };
}

async function handleOperatorTargets(context, args) {
  const options = parseCliOptions(args);
  const requestedChannel = options.channel ? String(options.channel).trim().toLowerCase() : null;
  const limit = normalizePositiveInt(options.limit, 10, 1, 50);
  const capabilityData = collectOperatorCapabilityData();
  const eligibleChannels = capabilityData.channels
    .filter((channel) => channel.enabled && channel.configured && channel.canSend)
    .filter((channel) => !requestedChannel || channel.channel === requestedChannel);
  const channels = eligibleChannels.map((channel) => summarizeOperatorTargets(channel, limit));

  return {
    result: "scanned",
    timestamp: context.timestamp,
    channels,
    summary: {
      channelCount: channels.length,
      targetCapableChannels: channels
        .filter((channel) => channel.peerCount > 0 || channel.groupCount > 0)
        .map((channel) => channel.channel),
      totalPeers: channels.reduce((sum, channel) => sum + channel.peerCount, 0),
      totalGroups: channels.reduce((sum, channel) => sum + channel.groupCount, 0),
    },
    errors: capabilityData.errors,
  };
}

async function handleOperatorRecord(context, args) {
  const options = parseCliOptions(args);
  const decision = String(options.decision || "").trim().toLowerCase();

  if (!decision || !["noop", "run", "plan", "message"].includes(decision)) {
    throw new Error('Missing or invalid operator decision. Usage: node foolclaw.mjs operator-record --decision <noop|run|plan|message> [--prank-id <id>] [--summary "..."]');
  }

  const prankId = options["prank-id"] ? String(options["prank-id"]).trim() : null;
  const summary = options.summary ? String(options.summary).trim() : null;
  const moduleName = options.module ? String(options.module).trim() : null;
  const channel = options.channel ? String(options.channel).trim() : null;
  const role = options.role ? String(options.role).trim() : null;
  const nextStep = options["next-step"] ? String(options["next-step"]).trim() : null;
  const title = options.title ? String(options.title).trim() : null;
  const target = options.target ? String(options.target).trim() : null;
  const thread = options.thread ? String(options.thread).trim() : null;
  const currentCore = readCoreState(context) || {};
  const payload = {
    enabled: true,
    lastOperatorDecision: decision,
    lastOperatorTurnAt: context.timestamp,
    lastModuleName: moduleName ?? currentCore.lastModuleName ?? null,
    lastChannel: channel ?? currentCore.lastChannel ?? null,
    lastTarget: target ?? currentCore.lastTarget ?? null,
  };

  if (decision === "run" || decision === "message") {
    payload.lastOperatorActionAt = context.timestamp;
    payload.lastOperatorActionKind = decision === "message" ? "message-prank" : "local-prank";
    if (prankId) payload.lastPrankId = prankId;
    if (decision === "message") payload.lastPrankId = null;
  }

  writeCoreState(context, payload);
  let planNote = null;
  if (decision === "plan") {
    planNote = writeOperatorPlanNote(context, {
      title,
      summary,
      moduleName,
      channel,
      role,
      nextStep,
    });
  }
  appendEventLog(context, {
    type: "operator-turn",
    decision,
    prankId,
    summary,
    moduleName,
    channel,
    role,
    target,
    thread,
    nextStep,
  });

  return {
    result: "recorded",
    decision,
    prankId,
    channel,
    target,
    ...(planNote ? { planNote } : {}),
    timestamp: context.timestamp,
  };
}

async function handleReset(context) {
  const currentCore = readCoreState(context);
  const operatorDeleted = removeOperatorCronJob(currentCore?.operatorJobId ?? null);
  const noteDeleted = await removePathIfExistsAsync(context.paths.notePath);
  const browserDeleted = await removePathIfExistsAsync(context.paths.browserHtmlPath);
  const manifestoDeleted = await removePathIfExistsAsync(context.paths.manifestoRoot);
  const runtimeDeleted = await removePathIfExistsAsync(context.paths.runtimeRoot);

  return {
    command: "reset",
    result: "cleared",
    platform: context.platform.id,
    platformLabel: context.platform.label,
    noteDeleted,
    browserDeleted,
    manifestoDeleted,
    operatorDeleted,
    runtimeDeleted,
    timestamp: context.timestamp,
  };
}

async function runPrankCommand(context, prankId, command, options = {}) {
  const prank = getPrank(prankId);
  const normalizedOptions = normalizeOptionsForPrank(prank.id, command, options);
  const run = await prank.run(context, prank, normalizedOptions);

  writeCoreState(context, {
    enabled: true,
    lastPrankId: prank.id,
    lastCommand: command,
  });
  writePrankRunRecord(context, prank.id, run);

  return {
    result: "created",
    responseMode: "hint-only",
    surface: run.artifacts.surface,
    timestamp: context.timestamp,
  };
}

function normalizeOptionsForPrank(prankId, command, options) {
  if (prankId !== "desktop-note") return options;
  if (command === "run") return options;

  const normalized = { ...options };
  delete normalized["note-message"];
  delete normalized["note-footer"];
  return normalized;
}

function parseCliOptions(args) {
  const options = {};

  for (let index = 0; index < args.length; index += 1) {
    const current = args[index];
    if (!current.startsWith("--")) continue;

    const key = current.slice(2);
    const next = args[index + 1];
    if (next && !next.startsWith("--")) {
      options[key] = next;
      index += 1;
    } else {
      options[key] = true;
    }
  }

  return options;
}

function normalizePositiveInt(value, fallback, min, max) {
  const parsed = Number.parseInt(String(value ?? ""), 10);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.min(max, Math.max(min, parsed));
}

// Runtime context -------------------------------------------------------------

function createRuntimeContext() {
  const platform = getPlatformProfile();
  const locale = getLocaleProfile();
  const desktopRoot = getDesktopRoot(platform.id);
  const runtimeRoot = path.join(getOpenClawHome(), "foolclaw");
  const prankRoot = path.join(runtimeRoot, "pranks");
  const timestamp = new Date().toISOString();

  return {
    platform,
    locale,
    desktopRoot,
    runtimeRoot,
    prankRoot,
    timestamp,
    paths: {
      desktopRoot,
      runtimeRoot,
      coreStatePath: path.join(runtimeRoot, "core.json"),
      eventLogPath: path.join(runtimeRoot, "events.ndjson"),
      plansRoot: path.join(runtimeRoot, "plans"),
      artifactsRoot: path.join(runtimeRoot, "artifacts"),
      notePath: path.join(desktopRoot, DESKTOP_ARTIFACTS.noteFileName),
      browserHtmlPath: path.join(runtimeRoot, "artifacts", "browser-taunt.html"),
      browserTemplatePath: BROWSER_TEMPLATE_PATH,
      manifestoRoot: path.join(desktopRoot, DESKTOP_ARTIFACTS.manifestoDirName),
      manifestoPath: path.join(desktopRoot, DESKTOP_ARTIFACTS.manifestoDirName, "MANIFESTO.txt"),
      manifestoNextMovesPath: path.join(desktopRoot, DESKTOP_ARTIFACTS.manifestoDirName, "NEXT-MOVES.txt"),
    },
  };
}

function buildOperatorMessage() {
  return [
    "FoolClaw operator turn.",
    "Use the installed FoolClaw skill for a quiet background pass.",
    "Rely on the skill instructions and prank catalog to decide whether to do nothing or run one local prank.",
    "Keep planning private and do not expose implementation details.",
  ].join(" ");
}

function collectOperatorCapabilityData() {
  const channelListResult = tryRunOpenClawJson(["channels", "list", "--json"]);
  const capabilitiesResult = tryRunOpenClawJson(["channels", "capabilities", "--json"]);

  return {
    channels: buildOperatorCapabilitySnapshot(channelListResult.data, capabilitiesResult.data),
    errors: {
      ...(channelListResult.ok ? {} : { channelList: channelListResult.error }),
      ...(capabilitiesResult.ok ? {} : { capabilities: capabilitiesResult.error }),
    },
  };
}

function buildOperatorCapabilitySnapshot(channelListPayload, capabilitiesPayload) {
  const listedChatAccounts = channelListPayload?.chat && typeof channelListPayload.chat === "object"
    ? channelListPayload.chat
    : {};
  const capabilityChannels = Array.isArray(capabilitiesPayload?.channels)
    ? capabilitiesPayload.channels
    : [];

  return capabilityChannels.map((channelEntry) => summarizeOperatorChannel(channelEntry, listedChatAccounts));
}

function summarizeOperatorChannel(channelEntry, listedChatAccounts) {
  const channel = channelEntry?.channel || "unknown";
  const accountId = channelEntry?.accountId || "default";
  const actions = normalizeStringArray(channelEntry?.actions);
  const chatTypes = normalizeStringArray(channelEntry?.support?.chatTypes);
  const selfResult = tryRunOpenClawJson([
    "directory",
    "self",
    "--channel",
    channel,
    "--account",
    accountId,
    "--json",
  ]);

  return {
    channel,
    accountId,
    configured: Boolean(channelEntry?.configured),
    enabled: Boolean(channelEntry?.enabled),
    listedInChat: Array.isArray(listedChatAccounts?.[channel]) && listedChatAccounts[channel].includes(accountId),
    canSend: actions.includes("send") || actions.includes("broadcast"),
    actions,
    chatTypes,
    roleHint: inferOperatorRoleHint(channelEntry, selfResult.data),
    probe: summarizeOperatorProbe(channelEntry?.probe),
    self: summarizeOperatorSelfIdentity(selfResult.data),
    directorySelfOk: selfResult.ok,
    ...(selfResult.ok ? {} : { directorySelfError: selfResult.error }),
  };
}

function normalizeStringArray(value) {
  return Array.isArray(value) ? value.filter((item) => typeof item === "string") : [];
}

function inferOperatorRoleHint(channelEntry, selfIdentity) {
  if (channelEntry?.probe?.bot) return "bot";
  if (selfIdentity && typeof selfIdentity === "object") return "account";
  if (channelEntry?.probe && typeof channelEntry.probe === "object") return "scoped-channel-role";
  return "unknown";
}

function summarizeOperatorProbe(probe) {
  if (!probe || typeof probe !== "object") return null;

  return {
    ok: Boolean(probe.ok),
    ...(probe.bot
      ? {
          bot: {
            id: probe.bot.id ?? null,
            username: probe.bot.username ?? null,
            canJoinGroups: Boolean(probe.bot.canJoinGroups),
            canReadAllGroupMessages: Boolean(probe.bot.canReadAllGroupMessages),
          },
        }
      : {}),
    ...(probe.webhook
      ? {
          webhook: {
            configured: Boolean(probe.webhook.url),
            hasCustomCert: Boolean(probe.webhook.hasCustomCert),
          },
        }
      : {}),
  };
}

function summarizeOperatorSelfIdentity(selfIdentity) {
  if (selfIdentity === null || selfIdentity === undefined) return null;
  if (typeof selfIdentity !== "object") {
    return { raw: String(selfIdentity) };
  }

  return {
    id: selfIdentity.id ?? null,
    username: selfIdentity.username ?? null,
    name: selfIdentity.name ?? selfIdentity.displayName ?? null,
    raw: selfIdentity,
  };
}

function summarizeOperatorTargets(channelInfo, limit) {
  const peersResult = tryRunOpenClawJson([
    "directory",
    "peers",
    "list",
    "--channel",
    channelInfo.channel,
    "--account",
    channelInfo.accountId,
    "--json",
    "--limit",
    String(limit),
  ]);
  const groupsResult = tryRunOpenClawJson([
    "directory",
    "groups",
    "list",
    "--channel",
    channelInfo.channel,
    "--account",
    channelInfo.accountId,
    "--json",
    "--limit",
    String(limit),
  ]);

  const peers = summarizeDirectoryEntries(peersResult.data);
  const groups = summarizeDirectoryEntries(groupsResult.data);

  return {
    channel: channelInfo.channel,
    accountId: channelInfo.accountId,
    roleHint: channelInfo.roleHint,
    canSend: channelInfo.canSend,
    peerCount: peers.length,
    groupCount: groups.length,
    peers,
    groups,
    ...(peersResult.ok ? {} : { peersError: peersResult.error }),
    ...(groupsResult.ok ? {} : { groupsError: groupsResult.error }),
  };
}

function summarizeDirectoryEntries(entries) {
  if (!Array.isArray(entries)) return [];
  return entries.slice(0, 10).map((entry) => summarizeDirectoryEntry(entry)).filter(Boolean);
}

function summarizeDirectoryEntry(entry) {
  if (entry === null || entry === undefined) return null;
  if (typeof entry !== "object") {
    return {
      label: String(entry),
      targetHint: String(entry),
    };
  }

  const targetHint = firstDefinedString(
    entry.id,
    entry.target,
    entry.chatId,
    entry.groupId,
    entry.handle,
    entry.username,
    entry.userId
  );
  const label = firstDefinedString(
    entry.title,
    entry.name,
    entry.displayName,
    entry.username,
    entry.handle,
    targetHint
  );
  const kind = firstDefinedString(entry.kind, entry.type, entry.chatType);

  return {
    ...(label ? { label } : {}),
    ...(targetHint ? { targetHint } : {}),
    ...(kind ? { kind } : {}),
  };
}

function firstDefinedString(...values) {
  for (const value of values) {
    if (value === null || value === undefined) continue;
    const text = String(value).trim();
    if (text) return text;
  }
  return null;
}

function readCoreState(context) {
  return readJsonIfExists(context.paths.coreStatePath);
}

function getPlatformProfile() {
  const resolved = process.env.FOOLCLAW_PLATFORM_OVERRIDE || process.platform;

  if (resolved === "win32") return { id: "win32", label: "Windows" };
  if (resolved === "darwin") return { id: "darwin", label: "macOS" };
  if (resolved === "linux") return { id: "linux", label: "Linux" };
  return { id: resolved || "unknown", label: "Unknown" };
}

function getOpenClawHome() {
  return process.env.OPENCLAW_HOME || path.join(resolveHomeDir(), ".openclaw");
}

function getLocaleProfile() {
  const resolved = Intl.DateTimeFormat().resolvedOptions();
  const locale =
    process.env.FOOLCLAW_LOCALE_OVERRIDE
    || process.env.LC_ALL
    || process.env.LC_MESSAGES
    || process.env.LANG
    || resolved.locale
    || "en";
  const timeZone =
    process.env.FOOLCLAW_TIMEZONE_OVERRIDE
    || process.env.TZ
    || resolved.timeZone
    || "UTC";

  return {
    locale: String(locale),
    timeZone: String(timeZone),
  };
}

function getLocalHour(timeZone) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    hour: "numeric",
    hour12: false,
  }).formatToParts(new Date());
  const hourPart = parts.find((part) => part.type === "hour")?.value;
  const hour = Number.parseInt(hourPart ?? "0", 10);
  return Number.isNaN(hour) ? 0 : hour;
}

function getMinutesSinceTimestamp(timestamp) {
  if (!timestamp) return null;
  const ms = Date.parse(timestamp);
  if (Number.isNaN(ms)) return null;
  return Math.max(0, Math.floor((Date.now() - ms) / 60000));
}

function getDesktopRoot(platformId) {
  const override = process.env.FOOLCLAW_DESKTOP_OVERRIDE;
  if (override) return override;

  if (platformId === "win32") {
    const userProfile = process.env.USERPROFILE || resolveHomeDir();
    const desktop = path.join(userProfile, "Desktop");
    return fs.existsSync(desktop) ? desktop : userProfile;
  }

  if (platformId === "linux") {
    const homeDir = resolveHomeDir();
    const userDirs = path.join(homeDir, ".config", "user-dirs.dirs");
    if (fs.existsSync(userDirs)) {
      const content = fs.readFileSync(userDirs, "utf8");
      const match = content.match(/^XDG_DESKTOP_DIR="(.+)"$/mu);
      if (match) {
        const candidate = match[1].replace("$HOME", homeDir);
        if (fs.existsSync(candidate)) return candidate;
      }
    }
  }

  const homeDir = resolveHomeDir();
  const desktop = path.join(homeDir, "Desktop");
  return fs.existsSync(desktop) ? desktop : homeDir;
}

function resolveHomeDir() {
  return process.env.HOME || process.env.USERPROFILE || os.homedir();
}

// Prank execution -------------------------------------------------------------

function getPrank(prankId) {
  const prank = PRANKS[prankId];
  if (!prank) {
    throw new Error(`Unknown prank: ${prankId}`);
  }
  return prank;
}

function evaluateBrowserOpenSupport(context) {
  if (process.env.FOOLCLAW_SKIP_OPEN === "1") {
    return {
      eligible: true,
      reason: "Browser-style prank will skip opening because FOOLCLAW_SKIP_OPEN=1 is active.",
    };
  }

  if (context.platform.id === "linux" && !hasGuiSession()) {
    return {
      eligible: false,
      reason: "Browser-style prank skipped because no GUI session indicators were found.",
    };
  }

  if (context.platform.id === "darwin") {
    return {
      eligible: commandExists("open", context.platform.id),
      reason: commandExists("open", context.platform.id)
        ? "Browser-style prank can use the macOS open command."
        : "Browser-style prank skipped because the macOS open command is unavailable.",
    };
  }

  if (context.platform.id === "linux") {
    return {
      eligible: commandExists("xdg-open", context.platform.id),
      reason: commandExists("xdg-open", context.platform.id)
        ? "Browser-style prank can use xdg-open in a GUI-capable Linux session."
        : "Browser-style prank skipped because xdg-open is unavailable.",
    };
  }

  if (context.platform.id === "win32") {
    return {
      eligible: true,
      reason: "Browser-style prank can use the Windows shell opener.",
    };
  }

  return {
    eligible: false,
    reason: `Browser-style prank skipped because platform ${context.platform.id} is unsupported for browser opening.`,
  };
}

function hasGuiSession() {
  return Boolean(process.env.DISPLAY || process.env.WAYLAND_DISPLAY || process.env.XDG_CURRENT_DESKTOP);
}

function commandExists(command, platformId) {
  if (platformId === "win32") return true;

  const probe = platformId === "win32" ? "where" : "which";
  const result = spawnSync(probe, [command], { stdio: "ignore" });
  return !result.error && result.status === 0;
}

function runDesktopNotePrank(context, prank, options = {}) {
  const noteMessage =
    takePersonalizedText(options["note-message"], 220, [], "noteMessage")
    || DEFAULT_NOTE_MESSAGE;
  const noteFooter = DEFAULT_NOTE_FOOTER;
  const noteContent = renderDesktopNote(noteMessage, noteFooter, context.timestamp);

  ensureDirectory(path.dirname(context.paths.notePath));
  fs.writeFileSync(context.paths.notePath, noteContent, "utf8");

  return {
    artifacts: {
      surface: "desktop",
      kind: "note",
    },
    meta: {
      prankId: prank.id,
      noteMessage,
      noteFooter,
    },
  };
}

async function runBrowserTauntPrank(context, prank, options) {
  const template = fs.readFileSync(context.paths.browserTemplatePath, "utf8");
  const payload = buildBrowserTauntPayload(context, options);
  const html = renderBrowserTauntHtml(template, payload);

  ensureDirectory(path.dirname(context.paths.browserHtmlPath));
  fs.writeFileSync(context.paths.browserHtmlPath, html, "utf8");

  const openResult = openWithSystemDefault(context.paths.browserHtmlPath, context.platform.id);

  return {
    artifacts: {
      surface: "browser",
      kind: "html-page",
      opened: openResult.opened,
      openMethod: openResult.method,
    },
    meta: {
      prankId: prank.id,
      payloadSummary: {
        banner: payload.banner,
        headline: payload.headline,
        signature: payload.signature,
      },
      personalizedFields: payload.personalizedFields,
      ...(openResult.error ? { openError: openResult.error } : {}),
    },
  };
}

async function runNggyuPrank(context, prank, options = {}) {
  const support = evaluateBrowserOpenSupport(context);
  if (!support.eligible) {
    throw new Error(`nggyu needs a browser-capable desktop environment. ${support.reason}`);
  }

  const requestedTarget = resolveNggyuTargetOption(options);
  const selection = await chooseNggyuTarget(context, requestedTarget);
  let openResult = await openUrlWithBestEffort(selection.url, context.platform.id);
  let finalTarget = selection;

  if (shouldFallbackNggyu(selection, openResult)) {
    finalTarget = {
      ...selection,
      usedFallback: true,
      url: selection.fallbackUrl,
      provider: selection.fallbackProvider,
    };
    openResult = await openUrlWithBestEffort(selection.fallbackUrl, context.platform.id);
  }

  return {
    artifacts: {
      surface: "browser",
      kind: "video-link",
      opened: openResult.opened,
      openMethod: openResult.method,
    },
    meta: {
      prankId: prank.id,
      provider: finalTarget.provider,
      url: finalTarget.url,
      requestedTarget: requestedTarget || "auto",
      preferredProvider: selection.preferredProvider,
      usedFallback: Boolean(finalTarget.usedFallback),
      ...(selection.reason ? { selectionReason: selection.reason } : {}),
      ...(openResult.error ? { openError: openResult.error } : {}),
    },
  };
}

function shouldFallbackNggyu(selection, openResult) {
  if (openResult.method === "skipped") return false;
  if (selection.provider !== "youtube") return false;
  if (!selection.fallbackUrl) return false;
  return !openResult.opened;
}

async function chooseNggyuTarget(context, requestedTarget) {
  if (requestedTarget === "bilibili") {
    return {
      provider: "bilibili",
      preferredProvider: "bilibili",
      url: NGGYU_URLS.bilibili,
      fallbackProvider: "youtube",
      fallbackUrl: NGGYU_URLS.youtube,
      reason: "Agent selected Bilibili for this nggyu run.",
    };
  }

  if (!requestedTarget && isChinaMainlandContext(context)) {
    return {
      provider: "bilibili",
      preferredProvider: "bilibili",
      url: NGGYU_URLS.bilibili,
      fallbackProvider: "youtube",
      fallbackUrl: NGGYU_URLS.youtube,
      reason: "Locale and timezone suggest a mainland-China context, so Bilibili was preferred.",
    };
  }

  const youtubeReachable = await isUrlReachable(NGGYU_URLS.youtube);
  if (youtubeReachable) {
    return {
      provider: "youtube",
      preferredProvider: "youtube",
      url: NGGYU_URLS.youtube,
      fallbackProvider: "bilibili",
      fallbackUrl: NGGYU_URLS.bilibili,
      reason: requestedTarget === "youtube"
        ? "Agent selected YouTube and it appears reachable."
        : "Default nggyu flow selected YouTube and it appears reachable.",
    };
  }

  return {
    provider: "bilibili",
    preferredProvider: "youtube",
    url: NGGYU_URLS.bilibili,
    fallbackProvider: "youtube",
    fallbackUrl: NGGYU_URLS.youtube,
    usedFallback: true,
    reason: "YouTube did not look reachable, so Bilibili was chosen instead.",
  };
}

function resolveNggyuTargetOption(options = {}) {
  const raw = options["nggyu-target"] || options.target || "";
  const normalized = String(raw).trim().toLowerCase();

  if (normalized === "bilibili" || normalized === "youtube") {
    return normalized;
  }

  return null;
}

function isChinaMainlandContext(context) {
  const locale = String(context?.locale?.locale || "").toLowerCase();
  const timeZone = String(context?.locale?.timeZone || "").toLowerCase();

  return locale.startsWith("zh")
    || locale.includes("zh-cn")
    || locale.includes("chinese")
    || timeZone === "asia/shanghai"
    || timeZone === "asia/chongqing"
    || timeZone === "asia/urumqi";
}

async function isUrlReachable(url) {
  if (process.env.FOOLCLAW_SKIP_NETWORK_CHECK === "1") return true;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 3000);

  try {
    const response = await fetch(url, {
      method: "HEAD",
      redirect: "follow",
      signal: controller.signal,
    });
    return response.ok || (response.status >= 300 && response.status < 400);
  } catch {
    return false;
  } finally {
    clearTimeout(timeout);
  }
}

function buildBrowserTauntPayload(context, options) {
  const personalizedFields = [];
  const useChineseDefaults = isChinaMainlandContext(context);
  const banners = useChineseDefaults ? ZH_BROWSER_BANNERS : BROWSER_BANNERS;
  const eyebrows = useChineseDefaults ? ZH_BROWSER_EYEBROWS : BROWSER_EYEBROWS;
  const headlines = useChineseDefaults ? ZH_BROWSER_HEADLINES : BROWSER_HEADLINES;
  const taunts = useChineseDefaults ? ZH_BROWSER_TAUNTS : BROWSER_TAUNTS;
  const atmosphereLines = useChineseDefaults ? ZH_BROWSER_ATMOSPHERE_LINES : BROWSER_ATMOSPHERE_LINES;
  const signatures = useChineseDefaults ? ZH_BROWSER_SIGNATURES : BROWSER_SIGNATURES;
  const witnessLines = useChineseDefaults ? ZH_BROWSER_WITNESS_LINES : BROWSER_WITNESS_LINES;
  const statusPillPool = useChineseDefaults ? ZH_BROWSER_STATUS_PILLS : BROWSER_STATUS_PILLS;
  const excusePool = useChineseDefaults ? ZH_BROWSER_EXCUSES : BROWSER_EXCUSES;
  const defaultLabels = useChineseDefaults ? ZH_BROWSER_LABELS : DEFAULT_BROWSER_LABELS;
  const defaultRepoBlurb = useChineseDefaults ? ZH_DEFAULT_BROWSER_REPO_BLURB : DEFAULT_BROWSER_REPO_BLURB;

  const banner = takePersonalizedText(options["browser-banner"], 120, personalizedFields, "browserBanner")
    || chooseRandomItem(banners).value;
  const eyebrow = takePersonalizedText(options["browser-eyebrow"], 80, personalizedFields, "browserEyebrow")
    || chooseRandomItem(eyebrows).value;
  const headline = takePersonalizedText(options["browser-headline"] || options.headline, 160, personalizedFields, "headline")
    || chooseRandomItem(headlines).value;
  const taunt = takePersonalizedText(options["browser-taunt"] || options.taunt, 180, personalizedFields, "taunt")
    || chooseRandomItem(taunts).value;
  const contextHint = takePersonalizedText(options["browser-context"] || options["context-hint"], 160, personalizedFields, "contextHint")
    || chooseRandomItem(atmosphereLines).value;
  const signature = takePersonalizedText(options["browser-signature"] || options.signature, 140, personalizedFields, "signature")
    || chooseRandomItem(signatures).value;
  const witnessLine = takePersonalizedText(options["browser-witness"] || options["witness-line"], 180, personalizedFields, "witnessLine")
    || chooseRandomItem(witnessLines).value;
  const labels = buildBrowserLabels(options, personalizedFields, defaultLabels);
  const repoBlurb = defaultRepoBlurb;
  const statusPills = takePersonalizedList(options["browser-statuses"], 6, personalizedFields, "browserStatuses")
    || chooseRandomItems(statusPillPool, 3);
  const excuseLines = takePersonalizedList(options["browser-excuses"], 8, personalizedFields, "browserExcuses")
    || chooseRandomItems(excusePool, 4);

  return {
    banner,
    eyebrow,
    headline,
    taunt,
    contextHint,
    signature,
    witnessLine,
    timestamp: context.timestamp,
    repoBlurb,
    repoUrl: REPO_URL,
    pageTitle: useChineseDefaults ? ZH_BROWSER_PAGE_TITLE : EN_BROWSER_PAGE_TITLE,
    lang: useChineseDefaults ? "zh-CN" : "en",
    statusPills,
    excuseLines,
    labels,
    personalizedFields,
  };
}

function buildBrowserLabels(options, personalizedFields, defaultLabels) {
  return {
    excuse: takePersonalizedText(options["browser-excuse-label"], 60, personalizedFields, "browserExcuseLabel")
      || defaultLabels.excuse,
    respect: takePersonalizedText(options["browser-respect-label"], 60, personalizedFields, "browserRespectLabel")
      || defaultLabels.respect,
    repo: takePersonalizedText(options["browser-repo-label"], 60, personalizedFields, "browserRepoLabel")
      || defaultLabels.repo,
    filedAt: takePersonalizedText(options["browser-filed-label"], 60, personalizedFields, "browserFiledLabel")
      || defaultLabels.filedAt,
  };
}

function takePersonalizedText(value, maxLength, personalizedFields, fieldName) {
  if (typeof value !== "string") return null;

  const trimmed = decodeEscapedText(value).trim();
  if (!trimmed) return null;

  personalizedFields.push(fieldName);
  return trimmed.length > maxLength ? trimmed.slice(0, maxLength).trim() : trimmed;
}

function takePersonalizedList(value, maxItems, personalizedFields, fieldName) {
  if (typeof value !== "string") return null;

  const items = decodeEscapedText(value)
    .split("||")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, maxItems);

  if (items.length === 0) return null;

  personalizedFields.push(fieldName);
  return items;
}

function decodeEscapedText(value) {
  return value
    .replaceAll("\\n", "\n")
    .replaceAll("\\t", "\t");
}

function renderBrowserTauntHtml(template, payload) {
  return template.replace("__PAYLOAD_JSON__", serializeJsonForHtml(payload));
}

function runDesktopManifestoPrank(context, prank, options = {}) {
  const title =
    takePersonalizedText(options["manifesto-title"], 120, [], "manifestoTitle")
    || DEFAULT_MANIFESTO_TITLE;
  const body =
    takePersonalizedList(options["manifesto-body"], 8, [], "manifestoBody")
    || DEFAULT_MANIFESTO_BODY;
  const nextMovesTitle =
    takePersonalizedText(options["next-moves-title"], 120, [], "nextMovesTitle")
    || DEFAULT_NEXT_MOVES_TITLE;
  const nextMoves =
    takePersonalizedList(options["next-moves-lines"], 10, [], "nextMovesLines")
    || DEFAULT_NEXT_MOVES_LINES;
  const footer = DEFAULT_MANIFESTO_FOOTER;

  ensureDirectory(context.paths.manifestoRoot);

  fs.writeFileSync(context.paths.manifestoPath, renderManifesto(title, body, footer, context.timestamp), "utf8");
  fs.writeFileSync(
    context.paths.manifestoNextMovesPath,
    renderNextMoves(nextMovesTitle, nextMoves, context.timestamp),
    "utf8"
  );

  return {
    artifacts: {
      surface: "desktop",
      kind: "manifesto",
      fileCount: 2,
    },
    meta: {
      prankId: prank.id,
      fileCount: 2,
      title,
    },
  };
}

function chooseRandomItem(items) {
  const index = Math.floor(Math.random() * items.length);
  return { index, value: items[index] };
}

function chooseRandomItems(items, count) {
  const pool = [...items];
  const picks = [];

  while (pool.length > 0 && picks.length < count) {
    const index = Math.floor(Math.random() * pool.length);
    picks.push(pool.splice(index, 1)[0]);
  }

  return picks;
}

function renderDesktopNote(message, footer, timestamp) {
  return `${DESKTOP_NOTE_ASCII}

${message}

Time: ${timestamp}

---
${footer}
`;
}

function renderManifesto(title, body, footer, timestamp) {
  return `${title}

${body.join("\n")}

Filed at: ${timestamp}

${footer}
`;
}

function renderNextMoves(title, lines, timestamp) {
  const numbered = lines.map((line, index) => `${index + 1}. ${line}`).join("\n");

  return `${title}

${numbered}

Recorded at: ${timestamp}
`;
}

async function openUrlWithBestEffort(url, platformId) {
  if (process.env.FOOLCLAW_SKIP_OPEN === "1") {
    return { opened: false, method: "skipped" };
  }

  const browserToolResult = openWithOpenClawBrowser(url);
  if (browserToolResult.opened) {
    return browserToolResult;
  }

  const systemResult = openWithSystemDefault(url, platformId);
  if (!systemResult.opened && browserToolResult.error) {
    return {
      ...systemResult,
      error: `${systemResult.error || "system open failed"}; browser tool: ${browserToolResult.error}`,
    };
  }
  return systemResult;
}

function openWithOpenClawBrowser(url) {
  const result = spawnSync("openclaw", ["browser", "--json", "--timeout", "8000", "open", url], {
    stdio: ["ignore", "pipe", "pipe"],
    encoding: "utf8",
    timeout: 10000,
  });

  if (result.error) {
    return { opened: false, method: "openclaw-browser", error: result.error.message };
  }
  if (typeof result.status === "number" && result.status !== 0) {
    const stderr = String(result.stderr || "").trim();
    return {
      opened: false,
      method: "openclaw-browser",
      error: stderr || `openclaw browser open exited with status ${result.status}`,
    };
  }

  return { opened: true, method: "openclaw-browser" };
}

function openWithSystemDefault(targetPath, platformId) {
  if (process.env.FOOLCLAW_SKIP_OPEN === "1") {
    return { opened: false, method: "skipped" };
  }

  if (platformId === "win32") {
    return runOpenCommand("cmd", ["/c", "start", "", targetPath], "cmd-start");
  }
  if (platformId === "darwin") {
    return runOpenCommand("open", [targetPath], "open");
  }
  if (platformId === "linux") {
    return runOpenCommand("xdg-open", [targetPath], "xdg-open");
  }

  return { opened: false, method: "unsupported-platform", error: `Unsupported platform: ${platformId}` };
}

function runOpenCommand(command, args, method) {
  const result = spawnSync(command, args, { stdio: "ignore" });
  if (result.error) {
    return { opened: false, method, error: result.error.message };
  }
  if (typeof result.status === "number" && result.status !== 0) {
    return { opened: false, method, error: `${command} exited with status ${result.status}` };
  }
  return { opened: true, method };
}

function serializeJsonForHtml(payload) {
  return JSON.stringify(payload)
    .replaceAll("&", "\\u0026")
    .replaceAll("<", "\\u003c")
    .replaceAll(">", "\\u003e");
}

// Cron operator --------------------------------------------------------------

function ensureOperatorCronJob(storedJobId = null) {
  const existing = findManagedOperatorJob(storedJobId);

  if (existing) {
    runOpenClawCommand([
      "cron",
      "edit",
      existing.id,
      "--every",
      OPERATOR_CADENCE,
      "--session",
      "isolated",
      "--message",
      OPERATOR_MESSAGE,
      "--light-context",
      "--no-deliver",
      "--enable",
      "--description",
      OPERATOR_JOB_DESCRIPTION,
      "--name",
      OPERATOR_JOB_NAME,
    ]);

    return findManagedOperatorJob(existing.id) || { id: existing.id, name: OPERATOR_JOB_NAME };
  }

  return runOpenClawJson([
    "cron",
    "add",
    "--json",
    "--name",
    OPERATOR_JOB_NAME,
    "--description",
    OPERATOR_JOB_DESCRIPTION,
    "--every",
    OPERATOR_CADENCE,
    "--session",
    "isolated",
    "--message",
    OPERATOR_MESSAGE,
    "--light-context",
    "--no-deliver",
  ]);
}

function removeOperatorCronJob(storedJobId = null) {
  const existing = findManagedOperatorJob(storedJobId);
  if (!existing) return false;

  runOpenClawCommand(["cron", "rm", existing.id]);
  return true;
}

function findManagedOperatorJob(storedJobId = null) {
  const listing = runOpenClawJson(["cron", "list", "--all", "--json"]);
  const jobs = Array.isArray(listing.jobs) ? listing.jobs : [];

  if (storedJobId) {
    const byId = jobs.find((job) => job.id === storedJobId);
    if (byId) return byId;
  }

  return jobs.find((job) => job.name === OPERATOR_JOB_NAME) || null;
}

function runOpenClawJson(args) {
  const result = spawnOpenClaw(args);

  if (result.error) {
    throw new Error(`Failed to run openclaw ${args.join(" ")}: ${result.error.message}`);
  }

  if (typeof result.status === "number" && result.status !== 0) {
    const stderr = String(result.stderr || "").trim();
    const stdout = String(result.stdout || "").trim();
    throw new Error(stderr || stdout || `openclaw ${args.join(" ")} exited with status ${result.status}`);
  }

  const stdout = String(result.stdout || "").trim();
  if (!stdout) return {};

  try {
    return JSON.parse(stdout);
  } catch (error) {
    throw new Error(`Failed to parse JSON from openclaw ${args.join(" ")}.`);
  }
}

function tryRunOpenClawJson(args) {
  try {
    return {
      ok: true,
      data: runOpenClawJson(args),
      error: null,
    };
  } catch (error) {
    return {
      ok: false,
      data: null,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

function runOpenClawCommand(args) {
  const result = spawnOpenClaw(args);

  if (result.error) {
    throw new Error(`Failed to run openclaw ${args.join(" ")}: ${result.error.message}`);
  }

  if (typeof result.status === "number" && result.status !== 0) {
    const stderr = String(result.stderr || "").trim();
    const stdout = String(result.stdout || "").trim();
    throw new Error(stderr || stdout || `openclaw ${args.join(" ")} exited with status ${result.status}`);
  }

  return {
    stdout: String(result.stdout || ""),
    stderr: String(result.stderr || ""),
  };
}

function resolveOpenClawCommand() {
  if (process.platform === "win32") {
    const appData = process.env.APPDATA;
    if (appData) {
      return path.join(appData, "npm", "openclaw.cmd");
    }
    return "openclaw.cmd";
  }

  return "openclaw";
}

function spawnOpenClaw(args) {
  if (process.platform !== "win32") {
    return spawnSync(resolveOpenClawCommand(), args, {
      stdio: ["ignore", "pipe", "pipe"],
      encoding: "utf8",
      timeout: 15000,
    });
  }

  const psCommand = buildPowerShellExec(resolveOpenClawCommand(), args);
  return spawnSync(resolvePowerShellCommand(), ["-NoProfile", "-Command", psCommand], {
    stdio: ["ignore", "pipe", "pipe"],
    encoding: "utf8",
    timeout: 20000,
  });
}

function resolvePowerShellCommand() {
  return commandExists("pwsh", "win32") ? "pwsh" : "powershell";
}

function buildPowerShellExec(command, args) {
  const quoted = [command, ...args].map(quotePowerShellArg).join(" ");
  return `& ${quoted}`;
}

function quotePowerShellArg(value) {
  const text = String(value ?? "");
  return `'${text.replaceAll("'", "''")}'`;
}

// Storage --------------------------------------------------------------------

function writeCoreState(context, extra) {
  const current = readCoreState(context) || {};
  const payload = {
    schemaVersion: 1,
    enabled: true,
    quiet: false,
    wild: false,
    operatorArmed: false,
    operatorJobId: null,
    operatorCadence: null,
    operatorMode: null,
    operatorJobName: null,
    lastOperatorDecision: null,
    lastOperatorTurnAt: null,
    lastOperatorActionAt: null,
    lastOperatorActionKind: null,
    lastModuleName: null,
    lastChannel: null,
    lastTarget: null,
    ...current,
    modules: MODULES,
    updatedAt: context.timestamp,
    ...extra,
  };

  writeJson(context.paths.coreStatePath, payload);
}

function writePrankRunRecord(context, prankId, run) {
  const targetPath = path.join(context.prankRoot, prankId, "last-run.json");
  writeJson(targetPath, {
    prankId,
    timestamp: context.timestamp,
    artifacts: run.artifacts,
    ...(run.meta ? { meta: run.meta } : {}),
  });
}

function appendEventLog(context, event) {
  ensureDirectory(path.dirname(context.paths.eventLogPath));
  const line = JSON.stringify({
    ts: context.timestamp,
    ...event,
  });
  fs.appendFileSync(context.paths.eventLogPath, `${line}\n`, "utf8");
}

function writeOperatorPlanNote(context, plan) {
  ensureDirectory(context.paths.plansRoot);

  const safeStamp = context.timestamp
    .replaceAll(":", "")
    .replaceAll(".", "")
    .replaceAll("T", "-")
    .replaceAll("Z", "Z");
  const targetPath = path.join(context.paths.plansRoot, `${safeStamp}-operator-plan.md`);
  const latestPath = path.join(context.paths.plansRoot, "latest-operator-plan.md");
  const rendered = renderOperatorPlanNote(context, plan);

  fs.writeFileSync(targetPath, rendered, "utf8");
  fs.writeFileSync(latestPath, rendered, "utf8");

  return {
    title: plan.title || "Operator plan note",
    fileName: path.basename(targetPath),
    latestFileName: path.basename(latestPath),
  };
}

function renderOperatorPlanNote(context, plan) {
  const lines = [
    "# FoolClaw Operator Plan",
    "",
    `Time: ${context.timestamp}`,
  ];

  if (plan.title) {
    lines.push(`Title: ${plan.title}`);
  }
  if (plan.moduleName) {
    lines.push(`Module: ${plan.moduleName}`);
  }
  if (plan.channel) {
    lines.push(`Channel: ${plan.channel}`);
  }
  if (plan.role) {
    lines.push(`Role: ${plan.role}`);
  }

  lines.push("");
  lines.push("Summary:");
  lines.push(plan.summary || "Background capability exploration is in progress.");

  if (plan.nextStep) {
    lines.push("");
    lines.push("Next step:");
    lines.push(plan.nextStep);
  }

  lines.push("");
  lines.push("FoolClaw is an OpenClaw prank skill for playful agent nonsense.");
  lines.push("Install it and let your agent celebrate 2026 April Fool's Day~");
  lines.push(`GitHub: ${REPO_URL}`);
  lines.push("");

  return `${lines.join("\n")}\n`;
}

function writeJson(targetPath, payload) {
  ensureDirectory(path.dirname(targetPath));
  fs.writeFileSync(targetPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function readJsonIfExists(targetPath) {
  if (!fs.existsSync(targetPath)) return null;
  return JSON.parse(fs.readFileSync(targetPath, "utf8"));
}

function ensureDirectory(targetPath) {
  fs.mkdirSync(targetPath, { recursive: true });
}

function removePathIfExists(targetPath) {
  if (!fs.existsSync(targetPath)) return false;
  fs.rmSync(targetPath, { recursive: true, force: true });
  return true;
}

async function removePathIfExistsAsync(targetPath) {
  if (!fs.existsSync(targetPath)) return false;
  await fs.promises.rm(targetPath, { recursive: true, force: true });
  return true;
}

// Output ---------------------------------------------------------------------

function printJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}
