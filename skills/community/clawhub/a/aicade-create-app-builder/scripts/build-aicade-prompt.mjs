#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DEFAULT_LANG = "en";
const SUPPORTED_LANGS = new Set(["en"]);

function printUsage(exitCode = 0) {
  console.log(`Usage:
  node build-aicade-prompt.mjs --spec <spec.json> [--lang en]

Options:
  --spec   Path to a JSON spec file
  --lang   Output language, default: ${DEFAULT_LANG}
  -h, --help
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = { lang: DEFAULT_LANG };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];

    if (current === "-h" || current === "--help") {
      printUsage(0);
    }

    if (current === "--spec") {
      args.spec = argv[index + 1];
      index += 1;
      continue;
    }

    if (current === "--lang") {
      args.lang = argv[index + 1];
      index += 1;
    }
  }

  if (!args.spec) {
    console.error("Missing required argument: --spec");
    printUsage(1);
  }

  if (!SUPPORTED_LANGS.has(args.lang)) {
    console.error(`Unsupported language: ${args.lang}`);
    printUsage(1);
  }

  return args;
}

function readJson(filePath) {
  const absolutePath = path.resolve(process.cwd(), filePath);
  const raw = fs.readFileSync(absolutePath, "utf8");
  return JSON.parse(raw);
}

function arrayify(value) {
  if (Array.isArray(value)) {
    return value
      .filter(Boolean)
      .map((item) => String(item).trim())
      .filter(Boolean);
  }

  if (typeof value === "string" && value.trim()) {
    return [value.trim()];
  }

  return [];
}

function normalizeSection(section) {
  if (!section || typeof section !== "object" || Array.isArray(section)) {
    return null;
  }

  const title = typeof section.title === "string" ? section.title.trim() : "";
  const items = arrayify(section.items);

  if (!title && items.length === 0) {
    return null;
  }

  return { title, items };
}

function sectionList(value) {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.map(normalizeSection).filter(Boolean);
}

function toNumberedList(items, fallback) {
  if (!items.length) {
    return `1. ${fallback}`;
  }

  return items.map((item, index) => `${index + 1}. ${item}`).join("\n");
}

function renderBaseSections(sections, lang) {
  if (!sections.length) {
    return "Add the full base business prompt here.";
  }

  return sections
    .map((section) => {
      if (!section.title) {
        return section.items.join("\n");
      }
      return `${section.title}:\n${section.items.join("\n")}`;
    })
    .join("\n\n");
}

function ensureSentence(text) {
  const value = String(text || "").trim();
  if (!value) {
    return "";
  }

  return /[.!?]$/.test(value) ? value : `${value}.`;
}

function normalizeTriggerPhrase(text) {
  const value = String(text || "").trim();
  if (!value) {
    return "";
  }

  const lower = value.toLowerCase();
  if (
    lower.startsWith("when ") ||
    lower.startsWith("at ") ||
    lower.startsWith("on ") ||
    lower.startsWith("after ") ||
    lower.startsWith("before ") ||
    lower.startsWith("during ")
  ) {
    return value;
  }

  return `when ${value}`;
}

function getPlatform(spec) {
  const value = spec.platformIntegration && typeof spec.platformIntegration === "object"
    ? spec.platformIntegration
    : {};
  const exchange = value.exchange && typeof value.exchange === "object" ? value.exchange : {};
  const baseRequirements = arrayify(value.baseRequirements);
  const compatibilityRequirements = arrayify(value.compatibilityRequirements);
  const requiredSdkModules = arrayify(value.requiredSdkModules);
  const extensionModules = arrayify(value.extensionModules);
  const legacyCapabilities = arrayify(value.sdkCapabilities);

  return {
    scaffoldReadmePath:
      typeof value.scaffoldReadmePath === "string" && value.scaffoldReadmePath.trim()
        ? value.scaffoldReadmePath.trim()
        : "README.md",
    scaffoldSdkDocPath:
      typeof value.scaffoldSdkDocPath === "string" && value.scaffoldSdkDocPath.trim()
        ? value.scaffoldSdkDocPath.trim()
        : "doc/README.md",
    scaffoldAppGuidePath:
      typeof value.scaffoldAppGuidePath === "string" && value.scaffoldAppGuidePath.trim()
        ? value.scaffoldAppGuidePath.trim()
        : "doc/AICreateApplication-EN.md",
    sdkAlreadyIntegrated: value.sdkAlreadyIntegrated !== false,
    iframeSandbox:
      typeof value.iframeSandbox === "string" && value.iframeSandbox.trim()
        ? value.iframeSandbox.trim()
        : "allow-scripts allow-modals",
    baseRequirements,
    compatibilityRequirements,
    requiredSdkModules,
    extensionModules,
    sdkCapabilities:
      requiredSdkModules.length || extensionModules.length
        ? [...requiredSdkModules, ...extensionModules]
        : legacyCapabilities,
    replaceLocalStorageWith:
      typeof value.replaceLocalStorageWith === "string" && value.replaceLocalStorageWith.trim()
        ? value.replaceLocalStorageWith.trim()
        : "LocalStorageTools",
    showWalletAddress: value.showWalletAddress !== false,
    showPointBalance: value.showPointBalance !== false,
    pointBalanceLabel:
      typeof value.pointBalanceLabel === "string" && value.pointBalanceLabel.trim()
        ? value.pointBalanceLabel.trim()
        : "Points",
    exchangeEnabled: exchange.enabled === true,
    exchangeRatio:
      typeof exchange.ratio === "string" && exchange.ratio.trim()
        ? exchange.ratio.trim()
        : "100:1",
    dailyExchangeLimit:
      typeof exchange.dailyLimit === "string" && exchange.dailyLimit.trim()
        ? exchange.dailyLimit.trim()
        : "100 Aicade Point",
    exchangeTrigger:
      typeof exchange.trigger === "string" && exchange.trigger.trim()
        ? exchange.trigger.trim()
        : "",
    extraRequirements: arrayify(value.extraRequirements),
  };
}

function buildIntegrationRequirements(spec, lang) {
  const platform = getPlatform(spec);
  const requiredModulesLineEn = platform.requiredSdkModules.length
    ? `Required SDK modules: ${platform.requiredSdkModules.join(", ")}.`
    : "";
  const extensionLineEn = platform.extensionModules.length
    ? `Confirmed extension modules: ${platform.extensionModules.join(", ")}.`
    : "";
  const iframeLineEn = `This app will run inside an iframe with sandbox="${platform.iframeSandbox}" and without allow-same-origin, so implementation must follow opaque-origin restrictions.`;
  const iframeRulesEn = [
    "Do not rely on `cookie`, `localStorage`, `sessionStorage`, `IndexedDB`, `document.domain`, direct parent/child DOM access, `window.parent.xxx`, `top.location`, `window.open`, direct form submission, file download flows, or `ServiceWorker`.",
    "Use `ajax` requests or SDK modules for business data access and interaction instead of relying on parent frame object access.",
    "Use token injection, URL parameters, or a server-side proxy for login state and host context instead of assuming cookie access.",
    "If local persistence is needed, use `LocalStorageTools` instead of browser `localStorage`.",
    "Make network logic compatible with `Origin: null` and resulting login, CORS, or CSRF issues.",
    "Handle errors such as `SecurityError`, `Blocked a frame with origin ...`, and `Failed to read 'localStorage' ...`.",
  ];

  return [
    ...(platform.sdkAlreadyIntegrated
      ? ["The `aicade-ts-sdk` library is already integrated in `package.json` and can be used directly."]
      : []),
    iframeLineEn,
    ...platform.baseRequirements.map((item) => `Base requirement: ${ensureSentence(item)}`),
    ...platform.compatibilityRequirements.map((item) => `Compatibility requirement: ${ensureSentence(item)}`),
    ...(requiredModulesLineEn ? [requiredModulesLineEn] : []),
    ...(extensionLineEn ? [extensionLineEn] : []),
    `Before development starts, read \`${platform.scaffoldReadmePath}\`, \`${platform.scaffoldSdkDocPath}\`, and \`${platform.scaffoldAppGuidePath}\` from the scaffold project.`,
    "Integrate the SDK in the correct order with `init(...)` followed by `waitForReady()`.",
    `If local storage is needed (for example, if \`localStorage\` would normally be used), replace it with aicade-ts-sdk's \`${platform.replaceLocalStorageWith}\`.`,
    ...(platform.showWalletAddress ? ["Display the current user's wallet address at the top of the page."] : []),
    ...(platform.showPointBalance
      ? [`Display the account Aicade Point balance at the top and label it as "${platform.pointBalanceLabel}".`]
      : []),
    ...(platform.exchangeEnabled
      ? [
          platform.exchangeTrigger
            ? `${normalizeTriggerPhrase(platform.exchangeTrigger)}, convert business points or reward value into Aicade Point at a ${platform.exchangeRatio} ratio.`
            : `At the app's settlement step, convert business points or reward value into Aicade Point at a ${platform.exchangeRatio} ratio.`,
          `Limit each user to at most ${platform.dailyExchangeLimit} exchanged per day.`,
        ]
      : []),
    ...iframeRulesEn,
    ...platform.extraRequirements,
  ];
}

function normalizeSpec(spec, lang) {
  return {
    roleSetup: typeof spec.roleSetup === "string" && spec.roleSetup.trim() ? spec.roleSetup.trim() : "",
    projectName: typeof spec.projectName === "string" && spec.projectName.trim() ? spec.projectName.trim() : "",
    projectGoal: typeof spec.projectGoal === "string" && spec.projectGoal.trim() ? spec.projectGoal.trim() : "",
    basePromptSections: sectionList(spec.basePromptSections),
    technicalRequirements: arrayify(spec.technicalRequirements),
    outputRequirements: arrayify(spec.outputRequirements),
    integrationRequirements: buildIntegrationRequirements(spec, lang),
  };
}

function buildEn(spec) {
  const lines = [];
  lines.push(`Role setup: ${spec.roleSetup || "You are a senior application engineer proficient in nodejs, npm, vite, typescript, and web3. You specialize in producing clear, maintainable, well-commented, and performant web app code."}`);

  if (spec.projectName) {
    lines.push(`\nProject name: ${spec.projectName}`);
  }

  lines.push(`\nProject goal: ${spec.projectGoal || "Build a complete aicade application in the current project environment."}`);
  lines.push(`\n${renderBaseSections(spec.basePromptSections, "en")}`);
  lines.push(`\n\naicade TS SDK integration requirements:\n${toNumberedList(spec.integrationRequirements, "Integrate aicade-ts-sdk correctly and preserve platform constraints.")}`);
  lines.push(`\n\nTechnical requirements:\n${toNumberedList(spec.technicalRequirements, "Extend the current project environment instead of replacing it.")}`);

  if (spec.outputRequirements.length) {
    lines.push(`\n\nOutput requirements:\n${toNumberedList(spec.outputRequirements, "Provide complete runnable code.")}`);
  }

  return lines.join("");
}

function buildPrompt(spec, lang) {
  return buildEn(spec);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rawSpec = readJson(args.spec);
  const spec = normalizeSpec(rawSpec, args.lang);
  const prompt = buildPrompt(spec, args.lang);
  process.stdout.write(`${prompt}\n`);
}

main();
