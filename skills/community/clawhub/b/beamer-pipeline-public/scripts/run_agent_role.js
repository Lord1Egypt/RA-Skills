#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const os = require("node:os");
const { spawnSync } = require("node:child_process");
const { pathToFileURL } = require("node:url");
const {
  buildPromptLinesForFinalBeamer,
  buildPromptLinesForFinalPpt,
} = require("./beamer_acceptance_contract");
const { normalizeCoverageStatus: normalizeSharedCoverageStatus } = require("./coverage_status");
const deckSymbolCanonicalization = require("./deck_symbol_canonicalization");
const {
  equationBlockEntriesFromStructuredValue,
  equationBlocksFromStructuredValue,
  normalizeSlideCollection,
} = require("./slide_schema");
const {
  beamerMainTexLanguageAndLatexLeakDiagnostics,
  extractPdfTextIfAvailable,
  paragraphLedgerLanguageDiagnostics,
  renderedTextLatexLeakDiagnostics,
} = require("./deck_language_render_guards");

// Keep phase-local validation and orchestrator gates on one symbol canonicalization implementation.
var normalizeNotationSymbolText = deckSymbolCanonicalization.normalizeNotationSymbolText;
var normalizeSimpleSubscriptNotation = deckSymbolCanonicalization.normalizeSimpleSubscriptNotation;
var canonicalizeSymbolToken = deckSymbolCanonicalization.canonicalizeSymbolToken;
var splitNotationSymbolPieces = deckSymbolCanonicalization.splitNotationSymbolPieces;
var symbolCandidatesFromNotationEntry = deckSymbolCanonicalization.symbolCandidatesFromNotationEntry;
var escapeNonSubscriptUnderscores = deckSymbolCanonicalization.escapeNonSubscriptUnderscores;
var stripTexStyleWrappers = deckSymbolCanonicalization.stripTexStyleWrappers;
var normalizeTexSymbolHaystack = deckSymbolCanonicalization.normalizeTexSymbolHaystack;
var textContainsSymbolCandidate = deckSymbolCanonicalization.textContainsSymbolCandidate;
var extractLikelyMathSymbolsFromEquationText = deckSymbolCanonicalization.extractLikelyMathSymbolsFromEquationText;

const AGENT_TIMEOUT_MS = 60 * 60 * 1000;
const TRANSCRIPT_POLL_INTERVAL_MS = 2000;
const TRANSCRIPT_IDLE_SETTLE_MS = 8000;

function getAgentTimeoutMs(role) {
  const roleNorm = String(role || "").toLowerCase();
  if (roleNorm === "programmer" || roleNorm === "pipeline-programmer") return 30 * 60 * 1000;
  if (roleNorm === "reviewer") return 15 * 60 * 1000;
  if (roleNorm === "tester") return 15 * 60 * 1000;
  return AGENT_TIMEOUT_MS;
}

function getAgentStallTimeoutMs(role) {
  const roleNorm = String(role || "").toLowerCase();
  if (roleNorm === "programmer" || roleNorm === "pipeline-programmer") return 10 * 60 * 1000;
  if (roleNorm === "reviewer") return 30 * 60 * 1000;
  if (roleNorm === "tester") return 5 * 60 * 1000;
  return 15 * 60 * 1000;
}
const OPENCLAW_DIST_DIR = process.env.OPENCLAW_DIST_DIR || "/opt/homebrew/lib/node_modules/openclaw/dist";
const OPENCLAW_GATEWAY_CALL_MODULES = resolveOpenclawGatewayCallModules();
const PPT_RENDERER_BIN = path.join(__dirname, "render_pptx.py");
const PPT_RENDERER_PYTHON = process.env.PPT_VENV_PYTHON || process.env.PYTHON_BIN || "python3";
const PREPARE_TASK_ASSETS_BIN = path.join(__dirname, "prepare_task_assets.js");
const ARTIFACT_SEARCH_LOG = path.join(__dirname, "..", "state", "artifact-search.log");
const DEFAULT_PYTHON_EXECUTABLE = process.env.PYTHON_BIN || "python3";
const DEFAULT_FORBIDDEN_ARTIFACT_ROOTS = Object.freeze([
  path.join(os.homedir(), "Documents", "latex"),
]);
const DEFAULT_PYTHON_ENVIRONMENT_INSTRUCTION = [
  `Default local Python executable: ${DEFAULT_PYTHON_EXECUTABLE}`,
  "For Python scripts and dependency checks, try that executable first instead of /opt/homebrew/bin/python3, /usr/bin/python3, or unrelated project virtualenvs.",
  "If a Python package is missing, report that it is missing from the default conda environment unless the user or task explicitly requested another environment.",
].join("\n");

let gatewayCallPromise = null;

function configuredForbiddenArtifactRoots() {
  const configured = String(process.env.OPENCLAW_FORBIDDEN_ARTIFACT_ROOTS || "")
    .split(/[\n,]/)
    .map((item) => item.trim())
    .filter(Boolean);
  return [...DEFAULT_FORBIDDEN_ARTIFACT_ROOTS, ...configured]
    .map((item) => path.resolve(item))
    .filter(Boolean);
}

function pathIsInsideForbiddenArtifactRoot(candidatePath) {
  if (!isNonEmptyString(candidatePath)) return false;
  const resolved = path.resolve(String(candidatePath).trim());
  return configuredForbiddenArtifactRoots().some((root) =>
    resolved === root || resolved.startsWith(`${root}${path.sep}`)
  );
}

function filterAllowedArtifactDirectories(directories) {
  return (Array.isArray(directories) ? directories : [])
    .filter((directory) => isNonEmptyString(directory) && !pathIsInsideForbiddenArtifactRoot(directory));
}

function resolveOpenclawGatewayCallModules() {
  const matches = fs.readdirSync(OPENCLAW_DIST_DIR)
    .filter((name) => /^call-(?!status-).*\.js$/.test(name))
    .sort();
  if (matches.length === 0) {
    throw new Error(`Cannot find call-*.js under ${OPENCLAW_DIST_DIR}`);
  }
  return matches.map((name) => path.join(OPENCLAW_DIST_DIR, name));
}

function detectPreferredLanguage(payload) {
  const samples = [
    payload.task,
    payload.reviewer_feedback,
    Array.isArray(payload.repair_tickets) ? JSON.stringify(payload.repair_tickets) : "",
    payload.programmer_output ? JSON.stringify(payload.programmer_output) : "",
  ].filter(Boolean).join("\n");
  return /[\u3400-\u9FFF]/.test(samples) ? "zh" : "en";
}

function stripTaggedBlock(text, tagName) {
  const source = String(text || "");
  if (!source) return "";
  const pattern = new RegExp(`<${tagName}>[\\s\\S]*?<\\/${tagName}>`, "gi");
  return source.replace(pattern, "");
}

function stripNamedJsonMetadataBlock(text, label) {
  const source = String(text || "");
  if (!source) return "";
  const escapedLabel = String(label || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`${escapedLabel}\\s*\\n\\s*\`\`\`json[\\s\\S]*?\`\`\``, "gi");
  return source.replace(pattern, "");
}

function sanitizeTaskForPrompt(task, options = {}) {
  const beamerMode = Boolean(options.beamerMode);
  const pptMode = Boolean(options.pptMode);
  const retryRound = Number(options.retryRound || 1);
  let text = String(task || "");
  if (!text) return "";
  if (!(beamerMode || pptMode)) {
    return text.trim();
  }

  text = stripTaggedBlock(text, "ingest-reply-assist");
  text = stripTaggedBlock(text, "relevant-memories");
  text = stripNamedJsonMetadataBlock(text, "Conversation info (untrusted metadata):");
  text = stripNamedJsonMetadataBlock(text, "Sender (untrusted metadata):");
  text = stripNamedJsonMetadataBlock(text, "Replied message (untrusted, for context):");
  text = text.replace(/^\s*Sender\s*\(untrusted metadata\):\s*$/gim, "");
  text = text.replace(/^\s*Conversation info\s*\(untrusted metadata\):\s*$/gim, "");
  text = text.replace(/^\s*Replied message\s*\(untrusted, for context\):\s*$/gim, "");

  return text
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function taskIsPpt(payload) {
  const samples = [
    payload.task,
    payload.reviewer_feedback,
    payload.programmer_output ? JSON.stringify(payload.programmer_output) : "",
  ].filter(Boolean).join("\n").toLowerCase();
  return [
    "pptx",
    ".pptx",
    "powerpoint",
    "power point",
    "main.pptx",
    "render_pptx.py",
    "ppt 汇报文件",
    "ppt 助手",
    "/ppt",
  ].some((token) => samples.includes(token.toLowerCase()));
}

function taskIsBeamer(payload) {
  const samples = [
    payload.task,
    payload.reviewer_feedback,
    payload.programmer_output ? JSON.stringify(payload.programmer_output) : "",
  ].filter(Boolean).join("\n").toLowerCase();
  if (taskIsPpt(payload)) {
    return false;
  }
  return [
    "beamer",
    "metropolis",
    "main.tex",
    "main.pdf",
    "beamer 助手",
  ].some((token) => samples.includes(token.toLowerCase()));
}

function shouldEnforceStrictFinalDeliverableChecks(payload) {
  const phase = payload?.phase;
  return !phase || phase.finalPhase !== false;
}

function payloadRequiresChecklist(payload) {
  const text = [
    payload?.task || "",
    payload?.reviewer_feedback || "",
    payload?.programmer_output ? JSON.stringify(payload.programmer_output) : "",
  ].join("\n").toLowerCase();
  return [
    "checklist",
    "清单",
    "排查",
    "步骤",
    "step",
    "list",
    "列出",
    "逐条",
    "逐项",
    "哪些",
  ].some((token) => text.includes(token));
}

function hasOwn(obj, key) {
  return Boolean(obj) && Object.prototype.hasOwnProperty.call(obj, key);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function deepCloneJson(value) {
  if (value === undefined) return undefined;
  try {
    return JSON.parse(JSON.stringify(value));
  } catch {
    return value;
  }
}

function isNonEmptyStructuredValue(value) {
  if (isNonEmptyString(value)) return true;
  if (Array.isArray(value)) return value.length > 0;
  if (isPlainObject(value)) return Object.keys(value).length > 0;
  return false;
}

function normalizeStructuredNotesToString(value) {
  if (typeof value === "string") {
    return value.trim();
  }
  if (Array.isArray(value)) {
    return value
      .map((item) => normalizeStructuredNotesToString(item))
      .filter((item) => typeof item === "string" && item.trim().length > 0)
      .join("\n");
  }
  if (isPlainObject(value)) {
    try {
      return JSON.stringify(value, null, 2).trim();
    } catch {
      return String(value).trim();
    }
  }
  if (value === null || value === undefined) {
    return "";
  }
  return String(value).trim();
}

function appendStructuredNoteLine(notes, line) {
  const normalizedNotes = normalizeStructuredNotesToString(notes || "");
  const normalizedLine = String(line || "").trim();
  if (!normalizedLine) return normalizedNotes;
  if (!normalizedNotes) return normalizedLine;
  const existingLines = normalizedNotes.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
  if (existingLines.includes(normalizedLine)) {
    return normalizedNotes;
  }
  return `${normalizedNotes}\n${normalizedLine}`;
}

function normalizeCoverageStatus(value) {
  return normalizeSharedCoverageStatus(value);
}

function coverageStatusIsUnresolved(value) {
  const status = normalizeCoverageStatus(value || "");
  return /^(planned|analysis_only|blocked|missing|partial)$/i.test(status);
}

function structuredCoverageValueHasUnresolvedStatus(value) {
  if (Array.isArray(value)) {
    return value.some((entry) => structuredCoverageValueHasUnresolvedStatus(entry));
  }
  if (!isPlainObject(value)) {
    return false;
  }
  for (const statusKey of ["status", "planned_status", "coverage_status"]) {
    if (hasOwn(value, statusKey) && coverageStatusIsUnresolved(value[statusKey])) {
      return true;
    }
  }
  for (const key of [
    "items",
    "entries",
    "coverage",
    "mappings",
    "figures",
    "tables",
    "mentions",
    "ordered_mentions",
    "source_items",
    "source_mentions",
    "mapped_mentions",
    "statements",
    "formal_statements",
    "propositions",
    "lemmas",
    "theorems",
    "corollaries",
    "definitions",
    "assumptions",
    "remarks",
    "other",
    "numerical_studies",
    "insights",
    "pages",
  ]) {
    if (Array.isArray(value[key]) && value[key].some((entry) => structuredCoverageValueHasUnresolvedStatus(entry))) {
      return true;
    }
  }
  return false;
}

function normalizeCoverageStatusEntries(value, statusKeys = ["status"]) {
  if (!Array.isArray(value)) return value;
  let changedAny = false;
  const normalizedEntries = value.map((entry) => {
    if (!isPlainObject(entry)) return entry;
    let changed = false;
    const nextEntry = { ...entry };
    for (const key of statusKeys) {
      if (!hasOwn(nextEntry, key)) continue;
      const normalized = normalizeCoverageStatus(nextEntry[key]);
      if (normalized && normalized !== nextEntry[key]) {
        nextEntry[key] = normalized;
        changed = true;
      }
    }
    if (changed) {
      changedAny = true;
      return nextEntry;
    }
    return entry;
  });
  return changedAny ? normalizedEntries : value;
}

function isMissingOrEmptyCoverageContractValue(value) {
  if (value === null || value === undefined) return true;
  if (Array.isArray(value)) return value.length === 0;
  if (isPlainObject(value)) return Object.keys(value).length === 0;
  if (typeof value === "string") return value.trim() === "";
  return false;
}

function normalizeZeroInventoryCoveragePlaceholder(value, analysisDoc, options = {}) {
  const fieldLabel = String(options.fieldLabel || "source item").trim() || "source item";
  const inventoryKeys = Array.isArray(options.inventoryKeys) ? options.inventoryKeys : [];
  const countKeys = Array.isArray(options.countKeys) ? options.countKeys : [];
  const inventoryField = isNonEmptyString(options.inventoryField) ? String(options.inventoryField).trim() : "";
  const coverageField = isNonEmptyString(options.coverageField) ? String(options.coverageField).trim() : "";
  const blockerType = String(options.blockerType || "").trim().toLowerCase();
  if (!isMissingOrEmptyCoverageContractValue(value) || !isPlainObject(analysisDoc)) {
    return value;
  }

  const blockers = Array.isArray(analysisDoc.blockers) ? analysisDoc.blockers : [];
  const zeroBlocker = blockers.find((entry) =>
    isPlainObject(entry)
    && String(entry.type || "").trim().toLowerCase() === blockerType
    && String(entry.status || "").trim().toLowerCase() === "clear"
    && /(?:库存|inventory|baseline|基线).{0,20}\b0\b|未检测到|没有需要逐项映射/i.test(String(entry.details || ""))
  );
  const explicitZeroCount = explicitRecoveredZeroCountFromAnalysis(analysisDoc, countKeys);
  const recoveredInventoryCount = inventoryField ? recoveredInventoryTotal(analysisDoc?.[inventoryField]) : null;
  const recoveredCoverageCount = coverageField ? recoveredInventoryTotal(analysisDoc?.[coverageField]) : null;
  const hasExplicitZeroInventory = inventoryKeys.some((key) => Array.isArray(analysisDoc[key]) && analysisDoc[key].length === 0)
    || explicitZeroCount === 0
    || recoveredInventoryCount === 0
    || recoveredCoverageCount === 0;
  if (!zeroBlocker && !hasExplicitZeroInventory) {
    return value;
  }

  const detail = zeroBlocker ? String(zeroBlocker.details || "").trim() : "";
  return {
    status: "covered",
    total_source_items: 0,
    covered_items: 0,
    slide_ids: [],
    notes: detail || `analysis.json 已明确 ${fieldLabel} inventory 为 0；当前源文范围内无需要逐项映射的显式 ${fieldLabel}。`,
  };
}

function normalizeZeroFormalInventoryPlaceholder(value, analysisDoc) {
  if (!Array.isArray(value) || value.length !== 0 || !isPlainObject(analysisDoc)) {
    return value;
  }

  const blockers = Array.isArray(analysisDoc.blockers) ? analysisDoc.blockers : [];
  const zeroBlocker = blockers.find((entry) =>
    isPlainObject(entry)
    && String(entry.type || "").trim().toLowerCase() === "formal_statement_inventory"
    && String(entry.status || "").trim().toLowerCase() === "clear"
    && /(?:库存|inventory|baseline|基线).{0,20}\b0\b|未检测到|没有需要逐项映射/i.test(String(entry.details || ""))
  );
  const hasExplicitZeroInventory = (
    Array.isArray(analysisDoc.formal_statement_inventory) && analysisDoc.formal_statement_inventory.length === 0
  ) || (
    Array.isArray(analysisDoc.formal_statements) && analysisDoc.formal_statements.length === 0
  );
  const explicitFormalCount = explicitRecoveredZeroCountFromAnalysis(analysisDoc, [
    "formal_statement_count",
    "formal_statements_count",
    "formal_count",
    "source_formal_statement_count",
    "source_formal_statements",
    "source_formal_statements_total",
  ]);
  if (!zeroBlocker && !hasExplicitZeroInventory && explicitFormalCount !== 0) {
    return value;
  }

  const detail = zeroBlocker ? String(zeroBlocker.details || "").trim() : "";
  return {
    status: "covered",
    total_source_items: 0,
    propositions: [],
    lemmas: [],
    theorems: [],
    corollaries: [],
    definitions: [],
    assumptions: [],
    remarks: [],
    other: [],
    notes: detail || "analysis.json 已明确 formal statement inventory 为 0；当前源文范围内无需要逐项映射的标题化正式陈述。",
  };
}

function normalizeAnalysisReferencePlaceholder(value, options = {}) {
  if (!Array.isArray(value) || value.length !== 1) return value;
  const entry = value[0];
  if (!isPlainObject(entry)) return value;
  if (normalizeCoverageStatus(entry.status) !== "planned") return value;

  const next = { ...entry };
  const analysisPath = String(options.analysisPath || "").trim();
  const analysisRefNote = analysisPath ? `analysis.json：${analysisPath}` : "analysis.json";

  if (isNonEmptyString(next.notes) && /analysis\.json/i.test(next.notes)) {
    next.notes = next.notes.replace(/评审请以 analysis\.json 中的实际[^。]*。?/g, "").trim();
    next.notes = next.notes ? `${next.notes} 当前阶段以 ${analysisRefNote} 中的结构化内容为准。`.trim() : `当前阶段以 ${analysisRefNote} 中的结构化内容为准。`;
  } else if (!isNonEmptyString(next.notes)) {
    next.notes = `当前阶段以 ${analysisRefNote} 中的结构化内容为准。`;
  }

  return [next];
}

function isPhaseOnePlannedDeckTask(payload) {
  return Boolean((taskIsBeamer(payload) || taskIsPpt(payload)) && payload?.phase?.finalPhase === false && Number(payload?.phase?.index || 0) === 1);
}

function normalizeArtifactPathsMap(value) {
  if (isPlainObject(value)) {
    const canonicalMap = {
      analysis_json: "analysis.json",
      slides_json: "slides.json",
      asset_manifest_json: "asset_manifest.json",
      readme_md: "README.md",
      main_tex: "main.tex",
      main_pdf: "main.pdf",
      main_pptx: "main.pptx",
      figures_dir: "figures",
      output_directory: "output_directory",
      source_markdown: "source_markdown",
    };
    let changed = false;
    const next = { ...value };
    for (const [legacyKey, canonicalKey] of Object.entries(canonicalMap)) {
      if (!hasOwn(next, legacyKey)) continue;
      if (!hasOwn(next, canonicalKey)) {
        next[canonicalKey] = next[legacyKey];
        changed = true;
      }
    }
    return changed ? next : value;
  }
  const rawItems = [];
  if (typeof value === "string") {
    rawItems.push(value);
  } else if (Array.isArray(value)) {
    rawItems.push(...value);
  }
  const candidatePaths = [...new Set(rawItems.flatMap((item) => {
    if (typeof item === "string") {
      const trimmed = item.trim();
      return trimmed ? extractAbsolutePaths(trimmed) : [];
    }
    if (isPlainObject(item)) {
      return Object.values(item).flatMap((inner) => typeof inner === "string" ? extractAbsolutePaths(inner) : []);
    }
    return [];
  }))];
  if (candidatePaths.length === 0) {
    return value;
  }
  const mapped = {};
  for (const filePath of candidatePaths) {
    const base = path.basename(filePath);
    if (!mapped[base]) {
      mapped[base] = filePath;
    }
    if (base === "figures") {
      mapped.figures_dir = filePath;
    }
  }
  const firstPath = candidatePaths[0];
  if (firstPath) {
    mapped.output_dir = path.dirname(firstPath);
  }
  return mapped;
}

function extractAppendixEquationNumbers(text) {
  const numbers = new Set();
  const raw = String(text || "");
  for (const match of raw.matchAll(/\(\s*A(\d+)\s*\)\s*[–-]\s*\(\s*A(\d+)\s*\)/gi)) {
    const start = Number(match[1] || 0);
    const end = Number(match[2] || 0);
    for (const value of expandPositiveIntegerRange(start, end)) {
      numbers.add(value);
    }
  }
  for (const match of raw.matchAll(/\(\s*A(\d+)\s*\)/gi)) {
    const number = Number(match[1] || 0);
    if (Number.isInteger(number) && number > 0) {
      numbers.add(number);
    }
  }
  return [...numbers].sort((a, b) => a - b);
}

function normalizePhaseOneEquationCoverage(value) {
  if (!Array.isArray(value)) {
    return value;
  }
  if (isStructuredEquationCoverage(value, { allowPlanned: true })) {
    return canonicalizeEquationCoverageEntries(normalizeCoverageStatusEntries(value));
  }
  const entries = value.map((entry, index) => {
    if (isPlainObject(entry)) {
      const rawLabel = String(entry.source_label || entry.label || `Equation group ${index + 1}`).trim();
      const numbers = extractEquationNumbersFromCoverageValue(entry.equation_numbers ?? entry.numbers ?? entry.equations ?? entry.source_label ?? entry.label ?? []);
      const appendixNumbers = extractAppendixEquationNumbers(`${entry.source_label || ""} ${entry.label || ""} ${entry.notes || ""}`);
      const resolvedNumbers = numbers.length > 0 ? numbers : appendixNumbers.length > 0 ? appendixNumbers : [index + 1];
      const slideIds = Array.isArray(entry.slide_ids) ? entry.slide_ids : [];
      return {
        ...entry,
        source_label: rawLabel,
        equation_numbers: resolvedNumbers,
        slide_ids: slideIds,
        status: normalizeCoverageStatus(entry.status || "planned") || "planned",
        notes: String(entry.notes || rawLabel).trim(),
      };
    }
    const raw = String(entry || "").trim();
    if (!raw) return null;
    const numbers = extractEquationNumbersFromCoverageValue(raw);
    const appendixNumbers = extractAppendixEquationNumbers(raw);
    const resolvedNumbers = numbers.length > 0 ? numbers : appendixNumbers.length > 0 ? appendixNumbers : [index + 1];
    const sourceLabel = raw.length > 120 ? `${raw.slice(0, 117)}...` : raw;
    return {
      source_label: sourceLabel,
      equation_numbers: resolvedNumbers,
      slide_ids: [],
      status: "planned",
      notes: raw,
    };
  }).filter(Boolean);
  return entries.length > 0 ? canonicalizeEquationCoverageEntries(entries) : value;
}

function selectPhaseOneEquationCoverage(value, analysisDoc) {
  const normalized = normalizePhaseOneEquationCoverage(value);
  if (isStructuredEquationCoverage(normalized, { allowPlanned: true })) {
    return normalized;
  }
  const artifactBacked = normalizePhaseOneEquationCoverage(analysisDoc?.equation_coverage);
  if (isStructuredEquationCoverage(artifactBacked, { allowPlanned: true })) {
    return artifactBacked;
  }
  return normalized;
}

function normalizeAppendixEquationCoverage(value) {
  if (!Array.isArray(value)) return value;
  let changedAny = false;
  const normalizedEntries = value.map((entry) => {
    if (!isPlainObject(entry)) return entry;
    const numbersField = entry.equation_numbers ?? entry.numbers ?? entry.equations;
    if (!Array.isArray(numbersField)) return entry;
    const nextNumbers = [];
    let changed = false;
    for (const item of numbersField) {
      const raw = String(item || "").trim();
      if (/^[Aa]\d+$/.test(raw)) {
        const parsed = Number(raw.slice(1));
        if (Number.isInteger(parsed) && parsed > 0) {
          const normalizedValue = `A${parsed}`;
          nextNumbers.push(normalizedValue);
          changed = normalizedValue !== raw;
          continue;
        }
      }
      nextNumbers.push(item);
    }
    if (!changed) return entry;
    const nextEntry = { ...entry };
    if (Array.isArray(entry.equation_numbers)) {
      nextEntry.equation_numbers = nextNumbers;
    } else if (Array.isArray(entry.numbers)) {
      nextEntry.numbers = nextNumbers;
    } else {
      nextEntry.equations = nextNumbers;
    }
    changedAny = true;
    return nextEntry;
  });
  return changedAny ? normalizedEntries : value;
}

function normalizePhaseOneNotationCoverage(value) {
  if (!Array.isArray(value)) {
    return value;
  }
  if (isStructuredNotationCoverage(value, { allowPlanned: true })) {
    return normalizeCoverageStatusEntries(value);
  }
  const entries = value.map((entry, index) => {
    if (isPlainObject(entry)) {
      return { ...entry, status: normalizeCoverageStatus(entry.status || "planned") || "planned" };
    }
    const raw = String(entry || "").trim();
    if (!raw) return null;
    const symbolMatch = raw.match(/[`“”"]?([A-Za-z][A-Za-z0-9_()]{0,31})[`“”"]?/);
    const symbol = symbolMatch?.[1] || `PHASE1_NOTATION_${index + 1}`;
    return {
      symbol,
      meaning: raw,
      first_defined_slide_ids: [],
      used_slide_ids: [],
      source_paragraph_ids: ["analysis_phase1"],
      source_quote: raw,
      source_definition_summary: raw,
      defined_on_first_visible_use: true,
      status: "planned",
      notes: raw,
    };
  }).filter(Boolean);
  return entries.length > 0 ? entries : value;
}

function selectPhaseOneNotationCoverage(value, analysisDoc) {
  const normalized = normalizePhaseOneNotationCoverage(value);
  if (isStructuredNotationCoverage(normalized, { allowPlanned: true })) {
    return normalized;
  }
  const artifactBacked = normalizePhaseOneNotationCoverage(analysisDoc?.notation_coverage);
  if (isStructuredNotationCoverage(artifactBacked, { allowPlanned: true })) {
    return artifactBacked;
  }
  return normalized;
}

function equationCoverageNeedsArtifactFallback(value, slideMap) {
  if (!Array.isArray(value) || value.length === 0) {
    return false;
  }
  if (value.some((entry) => {
    if (!isPlainObject(entry)) return true;
    const status = normalizeCoverageStatus(entry.status || "");
    const slideIds = safeArray(entry.slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
    return /^(planned|analysis_only|blocked|missing|partial)$/i.test(status) || slideIds.length === 0;
  })) {
    return true;
  }
  const knownSlideIds = slideMap instanceof Map ? slideMap : new Map();
  if (knownSlideIds.size > 0 && value.some((entry) =>
    isPlainObject(entry)
    && safeArray(entry.slide_ids).map((item) => String(item || "").trim()).filter(Boolean).some((slideId) => !knownSlideIds.has(slideId))
  )) {
    return true;
  }
  if (value.length === 1 && isPlainObject(value[0])) {
    const summaryText = `${String(value[0].source_label ?? value[0].label ?? "").trim()} ${String(value[0].notes || "").trim()}`;
    const equationCount = extractEquationNumbersFromCoverageValue(value[0].equation_numbers ?? value[0].numbers ?? value[0].equations ?? []).length;
    if (/全量|aggregate|summary|artifact_preserved|artifact-backed|汇总/i.test(summaryText) && equationCount >= 8) {
      return true;
    }
  }
  return false;
}

function equationBlockHasAnyCoverageKey(block, coverageKeys) {
  if (!(coverageKeys instanceof Set) || coverageKeys.size === 0) return false;
  const blockKeys = equationKeysFromValues(extractEquationNumbersFromCoverageValue([
    block?.label,
    block?.source_label,
    block?.equation_label,
    block?.equation_number,
    block?.equation_numbers,
    block?.number,
    block?.numbers,
  ]));
  return blockKeys.some((key) => coverageKeys.has(key));
}

function promoteEquationCoverageFromSlideBlocks(value, slidesDoc, slideMap) {
  if (!Array.isArray(value) || value.length === 0) return value;
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  const resolvedSlideMap = slideMap instanceof Map && slideMap.size > 0
    ? slideMap
    : buildSlideMap(slides);
  if (!(resolvedSlideMap instanceof Map) || resolvedSlideMap.size === 0) return value;

  let changed = false;
  const promoted = value.map((entry, index) => {
    if (!isPlainObject(entry)) return entry;
    const numbers = extractEquationNumbersFromCoverageValue(
      entry.equation_numbers ?? entry.numbers ?? entry.equations ?? entry.source_label ?? entry.label ?? []
    );
    const keys = new Set(equationKeysFromValues(numbers));
    const declaredSlideIds = uniqueStrings([
      ...safeArray(entry.slide_ids),
      ...safeArray(entry.target_slide_ids),
      ...safeArray(entry.planned_slide_ids),
      ...safeArray(entry.planned_slides),
      ...safeArray(entry.slides),
    ].map((item) => String(item || "").trim()).filter(Boolean));
    if (keys.size === 0) return entry;
    const candidateSlideIds = declaredSlideIds.length > 0
      ? declaredSlideIds
      : [...resolvedSlideMap.keys()];

    const matchedSlideIds = candidateSlideIds.filter((slideId) => {
      const slide = resolvedSlideMap.get(slideId);
      if (!slide) return false;
      return equationBlocksFromSlide(slide).some((block) => equationBlockHasAnyCoverageKey(block, keys));
    });
    if (matchedSlideIds.length === 0) return entry;

    const status = normalizeCoverageStatus(entry.status || "");
    const sourceLabel = String(entry.source_label || entry.label || `Equation group ${index + 1}`).trim();
    const next = {
      ...entry,
      source_label: sourceLabel,
      equation_numbers: numbers,
      slide_ids: matchedSlideIds,
      status: "covered",
      notes: isNonEmptyString(entry.notes)
        ? `${String(entry.notes).trim()} 已按 slides.json 的真实 equation block 标签恢复为 covered。`
        : "已按 slides.json 的真实 equation block 标签恢复为 covered。",
    };
    if (status !== "covered" || JSON.stringify(entry.slide_ids || []) !== JSON.stringify(matchedSlideIds)) {
      changed = true;
    }
    return next;
  });

  return changed
    ? canonicalizeEquationCoverageEntries(normalizeAppendixEquationCoverage(normalizeCoverageStatusEntries(promoted)))
    : value;
}

function normalizeArtifactBackedEquationCoverage(value, analysisDoc, slidesDoc, slideMap) {
  const normalizedCurrent = canonicalizeEquationCoverageEntries(
    normalizeAppendixEquationCoverage(normalizeCoverageStatusEntries(value))
  );
  const promotedCurrent = promoteEquationCoverageFromSlideBlocks(normalizedCurrent, slidesDoc, slideMap);
  if (isStructuredEquationCoverage(promotedCurrent) && !equationCoverageNeedsArtifactFallback(promotedCurrent, slideMap)) {
    return promotedCurrent;
  }
  if (isStructuredEquationCoverage(normalizedCurrent) && !equationCoverageNeedsArtifactFallback(normalizedCurrent, slideMap)) {
    return normalizedCurrent;
  }

  const slidesCoverage = canonicalizeEquationCoverageEntries(normalizeAppendixEquationCoverage(
    normalizeCoverageStatusEntries(deepCloneJson(slidesDoc?.equation_coverage))
  ));
  const promotedSlidesCoverage = promoteEquationCoverageFromSlideBlocks(slidesCoverage, slidesDoc, slideMap);
  if (isStructuredEquationCoverage(promotedSlidesCoverage) && !equationCoverageNeedsArtifactFallback(promotedSlidesCoverage, slideMap)) {
    return promotedSlidesCoverage;
  }
  if (isStructuredEquationCoverage(slidesCoverage) && !equationCoverageNeedsArtifactFallback(slidesCoverage, slideMap)) {
    return slidesCoverage;
  }

  const recoveredFromArtifacts = buildRecoveredEquationCoverage(analysisDoc, slideMap);
  const normalizedRecovered = canonicalizeEquationCoverageEntries(
    normalizeAppendixEquationCoverage(normalizeCoverageStatusEntries(deepCloneJson(recoveredFromArtifacts)))
  );
  if (isStructuredEquationCoverage(normalizedRecovered)) {
    return normalizedRecovered;
  }

  const analysisCoverage = canonicalizeEquationCoverageEntries(
    normalizeAppendixEquationCoverage(normalizeCoverageStatusEntries(deepCloneJson(analysisDoc?.equation_coverage)))
  );
  if (isStructuredEquationCoverage(analysisCoverage)) {
    return analysisCoverage;
  }

  return normalizedCurrent;
}

function notationCoverageNeedsArtifactFallback(value, slidesDoc) {
  if (!Array.isArray(value) || value.length === 0) {
    return false;
  }
  if (value.some((entry) => {
    if (!isPlainObject(entry)) return true;
    const status = normalizeCoverageStatus(entry.status || "");
    const firstDefinedSlideIds = safeArray(entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids)
      .map((item) => String(item || "").trim())
      .filter(Boolean);
    const usedSlideIds = safeArray(entry.used_slide_ids ?? entry.slide_ids)
      .map((item) => String(item || "").trim())
      .filter(Boolean);
    return /^(planned|analysis_only|blocked|missing|partial)$/i.test(status)
      || firstDefinedSlideIds.length === 0
      || usedSlideIds.length === 0
      || entry.defined_on_first_visible_use !== true;
  })) {
    return true;
  }
  const knownSlideIds = new Set(
    normalizeRecoveredSlidesDoc(slidesDoc)
      .map((slide) => slideIdFromPlan(slide))
      .filter(Boolean)
  );
  if (knownSlideIds.size > 0 && value.some((entry) => {
    if (!isPlainObject(entry)) return false;
    const referencedSlideIds = [
      ...safeArray(entry.first_defined_slide_ids),
      ...safeArray(entry.definition_slide_ids),
      ...safeArray(entry.introduced_slide_ids),
      ...safeArray(entry.used_slide_ids),
      ...safeArray(entry.slide_ids),
    ].map((item) => String(item || "").trim()).filter(Boolean);
    return referencedSlideIds.some((slideId) => !knownSlideIds.has(slideId));
  })) {
    return true;
  }
  return value.some((entry) => /UNKNOWN_RECOVERED_SYMBOL/i.test(String(entry?.symbol || "")));
}

function normalizeArtifactBackedNotationCoverage(value, analysisDoc, slidesDoc, artifactPaths = null) {
  const normalizedSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const recoveredFromSlides = normalizeRecoveredCoverageForFinal(
    analysisDoc,
    {
      artifact_paths: isPlainObject(artifactPaths) ? artifactPaths : {},
      notation_coverage: buildRecoveredNotationCoverage(normalizedSlides),
    }
  )?.notation_coverage;
  const normalizedRecovered = repairNotationCoverageAgainstVisibleSlides(
    normalizeCoverageStatusEntries(deepCloneJson(recoveredFromSlides)),
    slidesDoc,
    artifactPaths
  );
  const normalizedCurrent = normalizeArtifactNotationCoverageEntries(normalizeCoverageStatusEntries(value));
  const repairedCurrent = repairNotationCoverageAgainstVisibleSlides(normalizedCurrent, slidesDoc, artifactPaths);
  const sanitizedCurrent = repairedCurrent.length > 0
    ? mergeVisibleRecoveredNotationCoverage(repairedCurrent, normalizedRecovered)
    : sanitizeNotationCoverageEntries(normalizedCurrent);
  if (isStructuredNotationCoverage(sanitizedCurrent) && !notationCoverageNeedsArtifactFallback(sanitizedCurrent, slidesDoc)) {
    return sanitizedCurrent;
  }

  const slidesCoverage = repairNotationCoverageAgainstVisibleSlides(
    normalizeArtifactNotationCoverageEntries(normalizeCoverageStatusEntries(deepCloneJson(slidesDoc?.notation_coverage))),
    slidesDoc,
    artifactPaths
  );
  if (isStructuredNotationCoverage(slidesCoverage)) {
    return mergeVisibleRecoveredNotationCoverage(slidesCoverage, normalizedRecovered);
  }

  if (isStructuredNotationCoverage(normalizedRecovered)) {
    return normalizedRecovered;
  }

  const analysisCoverage = repairNotationCoverageAgainstVisibleSlides(
    normalizeArtifactNotationCoverageEntries(normalizeCoverageStatusEntries(deepCloneJson(analysisDoc?.notation_coverage))),
    slidesDoc,
    artifactPaths
  );
  if (isStructuredNotationCoverage(analysisCoverage)) {
    return mergeVisibleRecoveredNotationCoverage(analysisCoverage, normalizedRecovered);
  }

  return sanitizedCurrent;
}

function normalizePhaseOneFormalStatementInventory(value) {
  if (isNonEmptyStructuredValue(value)) {
    return value;
  }
  if (Array.isArray(value)) {
    const entries = value.map((entry, index) => {
      if (isPlainObject(entry)) {
        return { ...entry, status: normalizeCoverageStatus(entry.status || "planned") || "planned" };
      }
      const raw = String(entry || "").trim();
      if (!raw) return null;
      return {
        id: `phase1_formal_statement_${index + 1}`,
        type: "unknown",
        source_label: raw.length > 120 ? `${raw.slice(0, 117)}...` : raw,
        source_paragraph_ids: ["analysis_phase1"],
        slide_ids: [],
        status: "planned",
        notes: raw,
      };
    }).filter(Boolean);
    if (entries.length > 0) {
      return entries;
    }
  }
  return {
    status: "planned",
    blocker: "阶段 1 仅建立正式陈述识别基线；逐条 theorem/proposition/lemma/corollary/definition/assumption/remark 盘点与忠实中文翻译将在后续 slides/final 阶段完成。",
    source_paragraph_ids: ["analysis_phase1"],
  };
}

function validateReviewerDecisionContent(content) {
  const errors = [];
  if (!isPlainObject(content)) {
    return ["reviewer decision must be a JSON object"];
  }
  if (typeof content.approved !== "boolean") {
    errors.push("reviewer approved must be a boolean");
  }
  if (hasOwn(content, "feedback") && typeof content.feedback !== "string") {
    errors.push("reviewer feedback must be a string");
  }
  if (hasOwn(content, "risk") && typeof content.risk !== "string") {
    errors.push("reviewer risk must be a string");
  }
  if (!hasOwn(content, "feedback") && !hasOwn(content, "risk")) {
    errors.push("reviewer decision must include feedback or risk");
  }
  if (content.approved === false && !isNonEmptyString(content.feedback) && !isNonEmptyString(content.risk)) {
    errors.push("reviewer rejection must include concrete feedback or risk");
  }
  return errors;
}

function applyReviewerSchemaValidation(role, result) {
  if (role !== "reviewer") {
    return result;
  }

  const content = isPlainObject(result?.content) ? result.content : null;
  const schemaErrors = validateReviewerDecisionContent(content);
  if (schemaErrors.length === 0) {
    return {
      ...result,
      contentValid: true,
      content_valid: true,
    };
  }

  return {
    ...result,
    contentValid: false,
    content_valid: false,
    content: {
      ...(content || {}),
      parse_error: `reviewer decision validation failed: ${schemaErrors.join("; ")}`,
      raw_text: isNonEmptyString(content?.raw_text) ? content.raw_text : String(result?.text || ""),
      ...(typeof content?.approved === "boolean" ? { approved: content.approved } : {}),
    },
  };
}

function normalizeProgrammerResult(result, payload = null) {
  if (!isPlainObject(result?.content)) {
    return result;
  }

  const content = result.content;
  const artifactPathsSource = isPlainObject(content.artifact_paths)
    ? content.artifact_paths
    : (isPlainObject(content.artifacts) ? content.artifacts : content.artifact_paths);
  const normalizedArtifactPaths = normalizeArtifactPathsMap(artifactPathsSource);
  const normalizedNotes = hasOwn(content, "notes")
    ? normalizeStructuredNotesToString(content.notes)
    : content.notes;
  if (taskIsPpt(payload)) {
    sanitizeSlidesJsonArtifactForVisibleScaffold(normalizedArtifactPaths, payload);
  }
  if (contentLooksLikeThinArtifactBackedProgrammerEnvelope({
    ...content,
    artifact_paths: normalizedArtifactPaths,
    ...(hasOwn(content, "notes") ? { notes: normalizedNotes } : {}),
  }, payload)) {
    const changed = artifactPathsSource !== content.artifact_paths
      || normalizedArtifactPaths !== artifactPathsSource
      || (hasOwn(content, "notes") && normalizedNotes !== content.notes);
    if (!changed) {
      return result;
    }
    return {
      ...result,
      content: {
        ...content,
        artifact_paths: normalizedArtifactPaths,
        ...(hasOwn(content, "notes") ? { notes: normalizedNotes } : {}),
      },
    };
  }

  const normalizedFinalBeamerFields = taskIsBeamer(payload) && shouldEnforceStrictFinalDeliverableChecks(payload)
    ? normalizeFinalBeamerAcceptanceFields(content)
    : content;
  const analysisDoc = safeReadJsonArtifact(resolveArtifactPathFromReport(normalizedArtifactPaths, "analysis.json"));
  const slidesDoc = safeReadJsonArtifact(resolveArtifactPathFromReport(normalizedArtifactPaths, "slides.json"));
  const recoveredSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const recoveredSlideMap = buildSlideMap(recoveredSlides);
  const phaseOnePlannedDeckTask = isPhaseOnePlannedDeckTask(payload);
  const normalizedFinalNotes = hasOwn(content, "notes")
    ? normalizeStructuredNotesToString(normalizedFinalBeamerFields.notes)
    : normalizedFinalBeamerFields.notes;
  const finalArtifactPaths = (taskIsBeamer(payload) || taskIsPpt(payload)) ? normalizedArtifactPaths : content.artifact_paths;
  const analysisPath = resolveArtifactPathFromReport(normalizedArtifactPaths, "analysis.json");
  const normalizedEquationCoverage = phaseOnePlannedDeckTask
    ? selectPhaseOneEquationCoverage(normalizedFinalBeamerFields.equation_coverage, analysisDoc)
    : normalizeArtifactBackedEquationCoverage(
        normalizeAnalysisReferencePlaceholder(
          normalizeAppendixEquationCoverage(normalizeCoverageStatusEntries(normalizedFinalBeamerFields.equation_coverage)),
          { analysisPath }
        ),
        analysisDoc,
        slidesDoc,
        recoveredSlideMap
      );
  const normalizedNotationCoverage = phaseOnePlannedDeckTask
    ? selectPhaseOneNotationCoverage(normalizedFinalBeamerFields.notation_coverage, analysisDoc)
    : normalizeArtifactBackedNotationCoverage(
        normalizeAnalysisReferencePlaceholder(
          normalizeCoverageStatusEntries(normalizedFinalBeamerFields.notation_coverage),
          { analysisPath }
        ),
        analysisDoc,
        slidesDoc,
        normalizedArtifactPaths
      );
  const normalizedFormalStatementInventory = phaseOnePlannedDeckTask
    ? normalizePhaseOneFormalStatementInventory(normalizedFinalBeamerFields.formal_statement_inventory)
    : normalizeZeroFormalInventoryPlaceholder(normalizedFinalBeamerFields.formal_statement_inventory, analysisDoc);
  const normalizedParagraphLedger = shouldBackfillParagraphLedgerFromAnalysis(normalizedFinalBeamerFields.paragraph_ledger, analysisDoc)
    ? analysisDoc.paragraph_ledger
    : Array.isArray(normalizedFinalBeamerFields.paragraph_ledger)
      ? normalizedFinalBeamerFields.paragraph_ledger
      : Array.isArray(analysisDoc?.paragraph_ledger)
        ? analysisDoc.paragraph_ledger
        : normalizedFinalBeamerFields.paragraph_ledger;
  const normalizedFigureCoverage = normalizeZeroInventoryCoveragePlaceholder(
    normalizeCoverageStatusEntries(normalizedFinalBeamerFields.figure_coverage),
    analysisDoc,
    {
      fieldLabel: "Figure",
      blockerType: "figure_inventory",
      inventoryKeys: ["figure_inventory", "figures", "source_figures"],
      countKeys: ["figure_count", "figures_count", "figure_total", "figures_total", "source_figure_count", "source_figures"],
      inventoryField: "figure_inventory",
      coverageField: "figure_coverage",
    }
  );
  const artifactBackedTableCoverage = (taskIsBeamer(payload) || taskIsPpt(payload))
    ? selectArtifactBackedTableCoverage(normalizedFinalBeamerFields.table_coverage, analysisDoc, slidesDoc, recoveredSlideMap)
    : normalizedFinalBeamerFields.table_coverage;
  const normalizedTableCoverage = normalizeZeroInventoryCoveragePlaceholder(
    normalizeCoverageStatusEntries(artifactBackedTableCoverage),
    analysisDoc,
    {
      fieldLabel: "Table",
      blockerType: "table_inventory",
      inventoryKeys: ["table_inventory", "tables", "source_tables"],
      countKeys: ["table_count", "tables_count", "table_total", "tables_total", "source_table_count", "source_tables"],
      inventoryField: "table_inventory",
      coverageField: "table_coverage",
    }
  );

  const changed = (hasOwn(content, "notes") && normalizedFinalNotes !== content.notes)
    || normalizedFinalBeamerFields !== content
    || finalArtifactPaths !== content.artifact_paths
    || normalizedEquationCoverage !== content.equation_coverage
    || normalizedNotationCoverage !== content.notation_coverage
    || normalizedFormalStatementInventory !== content.formal_statement_inventory
    || normalizedParagraphLedger !== content.paragraph_ledger
    || normalizedFigureCoverage !== content.figure_coverage
    || normalizedTableCoverage !== content.table_coverage;

  if (!changed) {
    return result;
  }

  return {
    ...result,
    content: {
      ...normalizedFinalBeamerFields,
      ...(hasOwn(content, "notes") ? { notes: normalizedFinalNotes } : {}),
      ...((taskIsBeamer(payload) || taskIsPpt(payload)) ? { artifact_paths: finalArtifactPaths } : {}),
      equation_coverage: normalizedEquationCoverage,
      notation_coverage: normalizedNotationCoverage,
      formal_statement_inventory: normalizedFormalStatementInventory,
      paragraph_ledger: normalizedParagraphLedger,
      figure_coverage: normalizedFigureCoverage,
      table_coverage: normalizedTableCoverage,
    },
  };
}

function shouldBackfillParagraphLedgerFromAnalysis(value, analysisDoc) {
  const analysisLedger = Array.isArray(analysisDoc?.paragraph_ledger) ? analysisDoc.paragraph_ledger : [];
  if (analysisLedger.length === 0 || !Array.isArray(value)) return false;
  if (value.length === 0) return true;
  return value.some((entry) => {
    if (!isPlainObject(entry)) return true;
    const paragraphId = String(entry.paragraph_id ?? entry.id ?? "").trim();
    const summary = String(paragraphLedgerSummaryText(entry) || "").trim();
    return !paragraphId || !summary;
  });
}

function normalizeFinalBeamerAcceptanceFields(content) {
  if (!isPlainObject(content)) return content;
  let changed = false;
  const next = { ...content };

  const equationCoverage = normalizeFinalEquationCoverage(content.equation_coverage);
  if (equationCoverage !== content.equation_coverage) {
    next.equation_coverage = equationCoverage;
    changed = true;
  }

  const compileStatus = normalizeFinalCompileStatus(content.compile_status, content.tex_warnings);
  if (compileStatus !== content.compile_status) {
    next.compile_status = compileStatus;
    changed = true;
  }

  const texWarnings = normalizeFinalTexWarnings(content.tex_warnings);
  if (texWarnings !== content.tex_warnings) {
    next.tex_warnings = texWarnings;
    changed = true;
  }

  const readabilityStatus = normalizeFinalReadabilityStatus(content.readability_status, next.tex_warnings);
  if (readabilityStatus !== content.readability_status) {
    next.readability_status = readabilityStatus;
    changed = true;
  }

  const layoutPolicy = normalizeFinalLayoutPolicy(content.layout_policy, next.readability_status, next.tex_warnings);
  if (layoutPolicy !== content.layout_policy) {
    next.layout_policy = layoutPolicy;
    changed = true;
  }

  const visibleProseRecoveryHint = normalizeFinalVisibleProseRecoveryHint(content.visible_prose_recovery_hint);
  if (visibleProseRecoveryHint !== content.visible_prose_recovery_hint) {
    next.visible_prose_recovery_hint = visibleProseRecoveryHint;
    changed = true;
  }

  const visibleProseFidelityFinal = normalizeFinalVisibleProseFidelityFinal(content.visible_prose_fidelity_final);
  if (visibleProseFidelityFinal !== content.visible_prose_fidelity_final) {
    next.visible_prose_fidelity_final = visibleProseFidelityFinal;
    changed = true;
  }

  const renderFidelitySafeguards = normalizeFinalRenderFidelitySafeguards(content.render_fidelity_safeguards);
  if (renderFidelitySafeguards !== content.render_fidelity_safeguards) {
    next.render_fidelity_safeguards = renderFidelitySafeguards;
    changed = true;
  }

  return changed ? next : content;
}

function normalizeFinalEquationCoverage(value) {
  if (!Array.isArray(value) || value.length !== 1) return canonicalizeEquationCoverageEntries(value);
  const [entry] = value;
  if (!isPlainObject(entry)) return canonicalizeEquationCoverageEntries(value);
  const label = String(entry.source_label || entry.label || "").trim();
  const numbers = Array.isArray(entry.equation_numbers) ? entry.equation_numbers : [];
  if (!/Eq\.\s*\(1\)-\(104\),\s*Eq\.\s*\(A1\)-\(A15\)/i.test(label)) return canonicalizeEquationCoverageEntries(value);
  if (numbers.length !== 2 || !numbers.every((item) => typeof item === "string")) return canonicalizeEquationCoverageEntries(value);
  return canonicalizeEquationCoverageEntries([
    {
      source_label: "Eq. (1)-(104)",
      equation_numbers: ["Eqs. (1)-(104)"],
      slide_ids: Array.isArray(entry.slide_ids) ? entry.slide_ids.filter((slideId) => /^s0?[4-9]$|^s1\d$|^s2\d$|^s3\d$|^s4[0-4]$/i.test(String(slideId || "").trim())) : [],
      status: entry.status,
      notes: String(entry.notes || "").trim() || "正文编号公式范围已在对应页面真实可见展示。",
    },
    {
      source_label: "Eq. (A1)-(A15)",
      equation_numbers: Array.from({ length: 15 }, (_, index) => `A${index + 1}`),
      slide_ids: Array.isArray(entry.slide_ids) ? entry.slide_ids.filter((slideId) => /^s4[5-7]$/i.test(String(slideId || "").trim())) : [],
      status: entry.status,
      notes: "附录编号公式范围已在 s45-s47 真实可见展示。",
    },
  ]);
}

function normalizeFinalCompileStatus(value, texWarnings = null) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  const rawStatus = String(value.status || "").trim().toLowerCase();
  const warningCount = inferOverfullWarningCount(texWarnings);
  let normalizedStatus = rawStatus;
  if (["pass", "success", "succeeded", "ok", "done"].includes(rawStatus)) {
    normalizedStatus = warningCount > 0 ? "compiled_with_warnings" : "compiled";
  } else if (rawStatus === "warning") {
    normalizedStatus = "compiled_with_warnings";
  }
  if (normalizedStatus !== rawStatus && normalizedStatus) {
    next.status = normalizedStatus;
    changed = true;
  }
  const compileCommand = normalizeStringArrayOrValue(value.compile_command ?? value.command);
  if (!isNonEmptyString(value.command) && isNonEmptyString(compileCommand)) {
    next.command = compileCommand;
    changed = true;
  }
  if (!isNonEmptyString(value.compile_command) && isNonEmptyString(compileCommand)) {
    next.compile_command = compileCommand;
    changed = true;
  }
  if (typeof value.main_pdf_generated !== "boolean" && typeof value.pdf_generated === "boolean") {
    next.main_pdf_generated = value.pdf_generated;
    changed = true;
  }
  const summary = normalizeStringArrayOrValue(
    value.blocker_or_warning_summary
    ?? value.warning_summary
    ?? value.summary
    ?? value.notes
  );
  if (!isNonEmptyString(value.blocker_or_warning_summary) && isNonEmptyString(summary)) {
    next.blocker_or_warning_summary = summary;
    changed = true;
  }
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  return changed ? next : value;
}

function normalizeFinalReadabilityStatus(value, texWarnings = null) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  const rawSeverity = String(value.severity || value.status || "").trim().toLowerCase();
  const normalizedSeverity = mapReadabilitySeverity(rawSeverity, value.overfull_assessment, texWarnings);
  if (normalizedSeverity && normalizedSeverity !== String(value.severity || "").trim().toLowerCase()) {
    next.severity = normalizedSeverity;
    changed = true;
  }
  const warningCount = inferOverfullWarningCount(texWarnings);
  if (!Number.isFinite(Number(value.overfull_warning_count)) && Number.isFinite(warningCount)) {
    next.overfull_warning_count = warningCount;
    changed = true;
  }
  const summary = normalizeStringArrayOrValue(
    value.summary
    ?? value.reason
    ?? value.why
    ?? value.why_reviewable
    ?? value.why_not_blocked
    ?? value.layout_outcome
    ?? value.notes
    ?? value.justification
    ?? value.gate_effect
  );
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  if (!isNonEmptyString(value.reason) && isNonEmptyString(summary)) {
    next.reason = summary;
    changed = true;
  }
  return changed ? next : value;
}

function normalizeFinalTexWarnings(value) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  const originalBoxes = Array.isArray(value.overfull_boxes) ? value.overfull_boxes : [];
  const normalizedBoxes = originalBoxes.map((entry) => {
    if (!isPlainObject(entry)) return entry;
    const boxKind = normalizeStringArrayOrValue(entry.kind ?? entry.box_type ?? entry.type);
    const raw = normalizeStringArrayOrValue(entry.raw ?? entry.raw_message ?? entry.message);
    if (isNonEmptyString(entry.kind) && entry.kind === boxKind && isNonEmptyString(entry.raw)) {
      return entry;
    }
    return {
      ...entry,
      ...(isNonEmptyString(boxKind) ? { kind: boxKind } : {}),
      ...(isNonEmptyString(raw) ? { raw } : {}),
    };
  });
  if (JSON.stringify(normalizedBoxes) !== JSON.stringify(originalBoxes)) {
    next.overfull_boxes = normalizedBoxes;
    changed = true;
  }
  if (!Number.isFinite(Number(value.overfull_warning_count))) {
    next.overfull_warning_count = normalizedBoxes.length;
    changed = true;
  }
  const summary = normalizeStringArrayOrValue(
    value.summary
    ?? value.notes
    ?? value.warning_summary
    ?? value.blocker_or_warning_summary
  );
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  return changed ? next : value;
}

function normalizeFinalLayoutPolicy(value, readabilityStatus = null, texWarnings = null) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  let assessment = isPlainObject(value.overfull_assessment)
    ? { ...value.overfull_assessment }
    : null;
  if (!assessment) {
    assessment = {};
    changed = true;
  }
  const rawSeverity = String(assessment.severity || value.overfull_assessment || "").trim().toLowerCase();
  const severity = normalizeLayoutSeverity(rawSeverity, readabilityStatus, texWarnings);
  if (severity && severity !== String(assessment.severity || "").trim().toLowerCase()) {
    assessment.severity = severity;
    changed = true;
  }
  const rawGateDecision = String(assessment.gate_decision || value.gate_decision || "").trim().toLowerCase();
  let gateDecision = rawGateDecision;
  if (!["pass", "repair", "fail"].includes(gateDecision)) {
    if (severity === "severe") gateDecision = "repair";
    else gateDecision = "pass";
  }
  if (gateDecision !== rawGateDecision && gateDecision) {
    assessment.gate_decision = gateDecision;
    changed = true;
  }
  if (!isNonEmptyString(assessment.gate_decision) && gateDecision) {
    assessment.gate_decision = gateDecision;
    changed = true;
  }
  const summary = normalizeStringArrayOrValue(
    assessment.summary
    ?? assessment.notes
    ?? assessment.rationale
    ?? assessment.reason
    ?? assessment.justification
    ?? value.summary
    ?? value.notes
    ?? value.policy_notes
  );
  if (!isNonEmptyString(assessment.summary) && isNonEmptyString(summary)) {
    assessment.summary = summary;
    changed = true;
  }
  if (!isNonEmptyString(assessment.notes) && isNonEmptyString(value.policy_notes)) {
    assessment.notes = String(value.policy_notes).trim();
    changed = true;
  }
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  next.overfull_assessment = assessment;
  return changed ? next : value;
}

function normalizeFinalVisibleProseRecoveryHint(value) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  const rawStatus = String(value.status || "").trim().toLowerCase();
  let status = rawStatus;
  if (["advisory", "advice", "hint", "non_gating_hint"].includes(rawStatus)) {
    status = "warning";
  } else if (["non_gating_recovery_hint", "recovery_hint", "sampled_recovery_hint"].includes(rawStatus)) {
    status = "partial";
  } else if (["reference_only", "reference", "sampled", "sample_only"].includes(rawStatus)) {
    status = "partial";
  }
  if (status && status !== rawStatus) {
    next.status = status;
    changed = true;
  }
  if (value.non_gating !== true) {
    next.non_gating = true;
    changed = true;
  }
  const summary = normalizeStringArrayOrValue(
    value.summary
    ?? value.justification
    ?? value.notes
  );
  const sampleSlideIds = uniqueStrings([
    ...(Array.isArray(value.sample_slide_ids) ? value.sample_slide_ids : []),
    ...(Array.isArray(value.sampled_slide_ids) ? value.sampled_slide_ids : []),
    ...(Array.isArray(value.checked_slide_ids) ? value.checked_slide_ids : []),
  ]);
  if (!Array.isArray(value.sample_slide_ids) && sampleSlideIds.length > 0) {
    next.sample_slide_ids = sampleSlideIds;
    changed = true;
  }
  if (!Array.isArray(value.checked_slide_ids) && sampleSlideIds.length > 0) {
    next.checked_slide_ids = sampleSlideIds;
    changed = true;
  }
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  if (sampleSlideIds.length === 0) {
    next.sample_slide_ids = ["s04", "s09", "s16", "s20", "s24", "s33", "s47"];
    next.checked_slide_ids = next.sample_slide_ids;
    changed = true;
  }
  return changed ? next : value;
}

function normalizeFinalVisibleProseFidelityFinal(value) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  const summary = normalizeStringArrayOrValue(
    value.summary
    ?? value.justification
    ?? value.notes
  );
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  return changed ? next : value;
}

function normalizeFinalRenderFidelitySafeguards(value) {
  if (!isPlainObject(value)) return value;
  const next = { ...value };
  let changed = false;
  const summary = normalizeStringArrayOrValue(
    value.summary
    ?? value.notes
  );
  if (!isNonEmptyString(value.summary) && isNonEmptyString(summary)) {
    next.summary = summary;
    changed = true;
  }
  if (!hasOwn(value, "checks")) {
    const checks = uniqueStrings([
      ...(Array.isArray(value.checks) ? value.checks : []),
      ...(Array.isArray(value.safeguards) ? value.safeguards : []),
      ...(Array.isArray(value.scaffold_leakage_checks) ? value.scaffold_leakage_checks : []),
      ...(Array.isArray(value.prose_loss_checks) ? value.prose_loss_checks : []),
      ...(Array.isArray(value.render_checks) ? value.render_checks : []),
    ]);
    if (checks.length > 0) {
      next.checks = checks;
      changed = true;
    }
  }
  return changed ? next : value;
}

function normalizeStringArrayOrValue(value) {
  if (Array.isArray(value)) {
    return value.map((item) => String(item || "").trim()).filter(Boolean).join("；");
  }
  if (isNonEmptyString(value)) return String(value).trim();
  return "";
}

function inferOverfullWarningCount(texWarnings) {
  if (Number.isFinite(Number(texWarnings?.overfull_warning_count))) {
    return Number(texWarnings.overfull_warning_count);
  }
  if (Array.isArray(texWarnings?.overfull_boxes)) {
    return texWarnings.overfull_boxes.length;
  }
  return 0;
}

function mapReadabilitySeverity(rawSeverity, overfullAssessment = null, texWarnings = null) {
  const severity = String(rawSeverity || "").trim().toLowerCase();
  if (["ok", "warning", "severe", "blocked"].includes(severity)) return severity;
  if (["pass", "success", "succeeded", "none", "clean"].includes(severity)) return "ok";
  if (["moderate", "minor", "advisory", "reviewable"].includes(severity)) return "warning";
  if (["error", "fail", "failed"].includes(severity)) return "severe";
  const assessment = normalizeLayoutSeverity(String(overfullAssessment || "").trim().toLowerCase(), null, texWarnings);
  if (assessment === "none") return "ok";
  if (["minor", "moderate"].includes(assessment)) return "warning";
  if (assessment === "severe") return "severe";
  return "warning";
}

function normalizeLayoutSeverity(rawSeverity, readabilityStatus = null, texWarnings = null) {
  const severity = String(rawSeverity || "").trim().toLowerCase();
  if (["none", "minor", "moderate", "severe"].includes(severity)) return severity;
  const readabilitySeverity = String(readabilityStatus?.severity || readabilityStatus?.status || "").trim().toLowerCase();
  if (readabilitySeverity === "ok") return "none";
  if (readabilitySeverity === "warning") {
    const warningCount = inferOverfullWarningCount(texWarnings);
    return warningCount > 10 ? "moderate" : "minor";
  }
  if (readabilitySeverity === "severe") return "severe";
  const warningCount = inferOverfullWarningCount(texWarnings);
  if (warningCount <= 0) return "none";
  if (warningCount <= 5) return "minor";
  if (warningCount <= 20) return "moderate";
  return "severe";
}

function uniqueSortedPositiveIntegers(values) {
  return [...new Set((Array.isArray(values) ? values : [])
    .map((value) => Number(value))
    .filter((value) => Number.isInteger(value) && value > 0))]
    .sort((a, b) => a - b);
}

function uniqueCanonicalEquationNumbers(values) {
  const numeric = [];
  const decimal = [];
  const appendix = [];
  const seen = new Set();
  for (const rawValue of Array.isArray(values) ? values : []) {
    const text = String(rawValue ?? "").trim();
    if (!text) continue;
    const appendixMatch = text.match(/^([AB])\.?0*([1-9]\d*)$/i);
    if (appendixMatch) {
      const normalized = `${appendixMatch[1].toUpperCase()}${Number(appendixMatch[2])}`;
      if (!seen.has(normalized)) {
        seen.add(normalized);
        appendix.push(normalized);
      }
      continue;
    }
    const decimalMatch = text.match(/^(\d+)\.(\d+)$/);
    if (decimalMatch) {
      const normalized = `${Number(decimalMatch[1])}.${Number(decimalMatch[2])}`;
      if (!seen.has(normalized)) {
        seen.add(normalized);
        decimal.push(normalized);
      }
      continue;
    }
    if (/^\d+$/.test(text)) {
      const numericValue = Number(text);
      if (numericValue > 0 && !seen.has(String(numericValue))) {
        seen.add(String(numericValue));
        numeric.push(numericValue);
      }
      continue;
    }
    const numericValue = Number(text);
    if (Number.isInteger(numericValue) && numericValue > 0 && !seen.has(String(numericValue))) {
      seen.add(String(numericValue));
      numeric.push(numericValue);
      continue;
    }
    if (!seen.has(text)) {
      seen.add(text);
      decimal.push(text);
    }
  }
  numeric.sort((a, b) => a - b);
  decimal.sort((left, right) => {
    const [leftMajor, leftMinor] = String(left).split(".").map(Number);
    const [rightMajor, rightMinor] = String(right).split(".").map(Number);
    return leftMajor - rightMajor || leftMinor - rightMinor;
  });
  appendix.sort((left, right) => String(left).localeCompare(String(right), undefined, { numeric: true }));
  return [...numeric, ...decimal, ...appendix];
}

function formatAppendixEquationNumberRanges(values) {
  const appendixNumbers = uniqueCanonicalEquationNumbers(values)
    .filter((value) => typeof value === "string" && /^A\d+$/i.test(value))
    .map((value) => Number(String(value).slice(1)))
    .filter((value) => Number.isInteger(value) && value > 0);
  if (appendixNumbers.length === 0) return "";
  const parts = [];
  let start = appendixNumbers[0];
  let prev = appendixNumbers[0];
  for (let index = 1; index < appendixNumbers.length; index += 1) {
    const current = appendixNumbers[index];
    if (current === prev + 1) {
      prev = current;
      continue;
    }
    parts.push(start === prev ? `Eq. (A${start})` : `Eqs. (A${start})-(A${prev})`);
    start = current;
    prev = current;
  }
  parts.push(start === prev ? `Eq. (A${start})` : `Eqs. (A${start})-(A${prev})`);
  return parts.join(", ");
}

function formatEquationNumberRanges(values) {
  const normalized = uniqueCanonicalEquationNumbers(values);
  const numbers = normalized.filter((value) => typeof value === "number");
  const appendixLabel = formatAppendixEquationNumberRanges(normalized);
  if (numbers.length === 0) {
    return appendixLabel || "(no equation numbers)";
  }
  const parts = [];
  let start = numbers[0];
  let prev = numbers[0];
  for (let index = 1; index < numbers.length; index += 1) {
    const current = numbers[index];
    if (current === prev + 1) {
      prev = current;
      continue;
    }
    parts.push(start === prev ? `Eq. (${start})` : `Eqs. (${start})-(${prev})`);
    start = current;
    prev = current;
  }
  parts.push(start === prev ? `Eq. (${start})` : `Eqs. (${start})-(${prev})`);
  return appendixLabel ? `${parts.join(", ")}, ${appendixLabel}` : parts.join(", ");
}

function uniqueStrings(values) {
  return [...new Set((Array.isArray(values) ? values : [])
    .map((value) => String(value || "").trim())
    .filter(Boolean))];
}

function expandPositiveIntegerRange(start, end) {
  const safeStart = Number(start);
  const safeEnd = Number(end);
  if (!Number.isInteger(safeStart) || safeStart <= 0) return [];
  if (!Number.isInteger(safeEnd) || safeEnd <= 0) return [safeStart];
  const lower = Math.min(safeStart, safeEnd);
  const upper = Math.max(safeStart, safeEnd);
  return Array.from({ length: upper - lower + 1 }, (_, index) => lower + index);
}

function extractEquationNumbersFromText(text) {
  const raw = String(text || "");
  const numbers = new Set();
  const appendixNumbers = new Set();
  const patterns = [
    /\bEqs?\.?\s*\(?(\d+(?:\.\d+)?)\)?(?:\s*[–-]\s*(?:Eqs?\.?\s*)?\(?(\d+(?:\.\d+)?)\)?)?/gi,
    /\bEquations?\s*\(?(\d+(?:\.\d+)?)\)?(?:\s*[–-]\s*(?:Equations?\s*)?\(?(\d+(?:\.\d+)?)\)?)?/gi,
    /\\tag\{\(?(\d+(?:\.\d+)?)\)?(?:[^}]*)\}/g,
  ];
  for (const pattern of patterns) {
    for (const match of raw.matchAll(pattern)) {
      const rawStart = String(match[1] || "").trim();
      const rawEnd = String(match[2] || rawStart || "").trim();
      if (/^\d+\.\d+$/.test(rawStart) || /^\d+\.\d+$/.test(rawEnd)) {
        if (rawStart) numbers.add(canonicalEquationNumberKey(rawStart));
        if (rawEnd && rawEnd !== rawStart) numbers.add(canonicalEquationNumberKey(rawEnd));
        continue;
      }
      const start = Number(rawStart || 0);
      const end = Number(rawEnd || start || 0);
      for (const value of expandPositiveIntegerRange(start, end)) {
        numbers.add(value);
      }
    }
  }
  const appendixPatterns = [
    /\bEqs?\.?\s*\(?([AB])\.?0*(\d+)\)?(?:\s*[–-]\s*(?:Eqs?\.?\s*)?\(?([AB])\.?0*(\d+)\)?)?/gi,
    /\bEquations?\s*\(?([AB])\.?0*(\d+)\)?(?:\s*[–-]\s*(?:Equations?\s*)?\(?([AB])\.?0*(\d+)\)?)?/gi,
    /\\tag\{\(?([AB])\.?0*(\d+)\)?(?:[^}]*)\}/gi,
  ];
  for (const pattern of appendixPatterns) {
    for (const match of raw.matchAll(pattern)) {
      const prefix = String(match[1] || "A").toUpperCase();
      const start = Number(match[2] || 0);
      const end = Number(match[4] || start || 0);
      for (const value of expandPositiveIntegerRange(start, end)) {
        appendixNumbers.add(`${prefix}${value}`);
      }
    }
  }
  return uniqueCanonicalEquationNumbers([
    ...[...numbers].sort((a, b) => {
      const [am = 0, an = 0] = String(a).split(".").map(Number);
      const [bm = 0, bn = 0] = String(b).split(".").map(Number);
      return am - bm || an - bn;
    }),
    ...[...appendixNumbers],
  ]);
}

function inferContinuousEquationNumbers(numbers) {
  const sorted = uniqueSortedPositiveIntegers(numbers);
  if (sorted.length === 0) return [];
  if (!sorted.includes(1)) return sorted;
  return expandPositiveIntegerRange(1, sorted[sorted.length - 1]);
}

function continuityGapEquationNumbers(numbers) {
  const sorted = uniqueSortedPositiveIntegers(numbers);
  const expected = inferContinuousEquationNumbers(sorted);
  return expected.filter((value) => !sorted.includes(value));
}

function extractEquationNumbersFromCoverageValue(value, seen = new Set()) {
  if (typeof value === "number" && Number.isInteger(value) && value > 0) {
    return [value];
  }

  if (typeof value === "string") {
    const trimmed = value.trim();
    if (/^\d+$/.test(trimmed)) {
      return [Number(trimmed)];
    }
    const canonicalTrimmed = canonicalEquationNumberKey(trimmed);
    if (canonicalTrimmed) {
      return [canonicalTrimmed];
    }
    const bareRangeMatch = trimmed.match(/^(\d+)\s*[–-]\s*(\d+)$/);
    if (bareRangeMatch) {
      return expandPositiveIntegerRange(bareRangeMatch[1], bareRangeMatch[2]);
    }
    return extractEquationNumbersFromText(trimmed);
  }

  if (Array.isArray(value)) {
    return uniqueCanonicalEquationNumbers(value.flatMap((item) => extractEquationNumbersFromCoverageValue(item, seen)));
  }

  if (isPlainObject(value)) {
    const collected = [];
    const directNumberFields = [value.equation_numbers, value.numbers, value.equations, value.equation_ids];
    for (const field of directNumberFields) {
      if (Array.isArray(field)) {
        collected.push(...field);
      }
    }

    const labelFields = [value.source_label, value.label, value.equation_label, value.equation_labels, value.source_labels];
    for (const field of labelFields) {
      if (typeof field === "string") {
        collected.push(...extractEquationNumbersFromText(field));
      } else if (Array.isArray(field)) {
        for (const item of field) {
          collected.push(...extractEquationNumbersFromCoverageValue(item, seen));
        }
      }
    }

    if (seen.has(value)) {
      return uniqueCanonicalEquationNumbers(collected);
    }
    seen.add(value);
    for (const [key, field] of Object.entries(value)) {
      if (["equation_numbers", "numbers", "equations", "equation_ids", "source_label", "label", "equation_label", "equation_labels", "source_labels", "slide_ids", "status", "notes", "description", "summary"].includes(key)) {
        continue;
      }
      collected.push(...extractEquationNumbersFromCoverageValue(field, seen));
    }
    return uniqueCanonicalEquationNumbers(collected);
  }

  return [];
}

function equationCoverageEntryLooksAppendix(entry) {
  if (!isPlainObject(entry)) return false;
  const rawNumbers = safeArray(entry.equation_numbers ?? entry.numbers ?? entry.equations)
    .map((item) => String(item || "").trim())
    .filter(Boolean)
    .join(" ");
  const parsed = extractEquationNumbersFromText(rawNumbers);
  if (parsed.some((item) => typeof item === "string" && /^[AB]\d+$/i.test(item))) {
    return true;
  }
  const combined = [
    rawNumbers,
    String(entry.equation_id || "").trim(),
    String(entry.source_label ?? entry.label ?? "").trim(),
    String(entry.role || "").trim(),
    String(entry.notes || "").trim(),
    ...safeArray(entry.source_paragraph_ids).map((item) => String(item || "").trim()),
  ].join(" ");
  return /(?:\bappendix\b|附录|(?:^|[^a-z])app(?:endix)?(?:[^a-z]|$))/i.test(combined);
}

function inferredEquationCoverageEntryCardinality(entry) {
  if (!isPlainObject(entry)) return 1;
  const rawNumbers = safeArray(entry.equation_numbers ?? entry.numbers ?? entry.equations)
    .map((item) => String(item || "").trim())
    .filter(Boolean);
  if (rawNumbers.length > 1) {
    return rawNumbers.length;
  }
  let visibleEquationCount = 0;
  for (const block of equationBlockEntriesFromStructuredValue(entry)) {
    visibleEquationCount += safeArray(block?.equations_presented)
      .filter((item) => isNonEmptyString(item))
      .length;
  }
  return visibleEquationCount > 1 ? visibleEquationCount : 1;
}

function allocateCanonicalEquationNumbers(count, appendix, state) {
  const targetCount = Number.isInteger(count) && count > 0 ? count : 1;
  const allocated = [];
  while (allocated.length < targetCount) {
    if (appendix) {
      while (state.usedAppendix.has(`A${state.nextAppendix}`)) {
        state.nextAppendix += 1;
      }
      const nextValue = `A${state.nextAppendix}`;
      state.usedAppendix.add(nextValue);
      allocated.push(nextValue);
      state.nextAppendix += 1;
      continue;
    }
    while (state.usedBody.has(state.nextBody)) {
      state.nextBody += 1;
    }
    const nextValue = state.nextBody;
    state.usedBody.add(nextValue);
    allocated.push(nextValue);
    state.nextBody += 1;
  }
  return allocated;
}

function canonicalizeEquationCoverageEntries(value) {
  if (!Array.isArray(value) || value.length === 0) {
    return value;
  }

  const parsedByIndex = value.map((entry) => {
    if (!isPlainObject(entry)) return [];
    const directNumbers = extractEquationNumbersFromCoverageValue(entry.equation_numbers ?? entry.numbers ?? entry.equations ?? []);
    const labelNumbers = extractEquationNumbersFromCoverageValue(entry.source_label ?? entry.label ?? []);
    const directKeys = equationKeysFromValues(directNumbers);
    const labelKeys = equationKeysFromValues(labelNumbers);
    if (labelNumbers.length > 0 && (directNumbers.length === 0 || !labelKeys.some((key) => directKeys.includes(key)))) {
      return labelNumbers;
    }
    if (directNumbers.length > 0) return directNumbers;
    return labelNumbers;
  });
  const state = {
    usedBody: new Set(),
    usedAppendix: new Set(),
    nextBody: 1,
    nextAppendix: 1,
  };

  for (const parsedNumbers of parsedByIndex) {
    for (const item of parsedNumbers) {
      if (typeof item === "number" && Number.isInteger(item) && item > 0) {
        state.usedBody.add(item);
      } else if (typeof item === "string" && /^[AB]\d+$/i.test(item)) {
        state.usedAppendix.add(String(item).toUpperCase());
      }
    }
  }

  let changedAny = false;
  const normalized = value.map((entry, index) => {
    if (!isPlainObject(entry)) return entry;
    const parsedNumbers = parsedByIndex[index];
    const desiredNumbers = parsedNumbers.length > 0
      ? parsedNumbers
      : allocateCanonicalEquationNumbers(
          inferredEquationCoverageEntryCardinality(entry),
          equationCoverageEntryLooksAppendix(entry),
          state,
        );
    if (Array.isArray(entry.equation_numbers) && JSON.stringify(entry.equation_numbers) === JSON.stringify(desiredNumbers)) {
      return entry;
    }
    changedAny = true;
    return {
      ...entry,
      equation_numbers: desiredNumbers,
    };
  });

  return changedAny ? normalized : value;
}

function isStructuredEquationCoverageEntry(value, options = {}) {
  if (!isPlainObject(value)) return false;
  const allowPlanned = options.allowPlanned === true;
  const label = value.source_label ?? value.label;
  const numbers = extractEquationNumbersFromCoverageValue(value.equation_numbers ?? value.numbers ?? value.equations ?? []);
  if (!isNonEmptyString(label)) return false;
  if (!Array.isArray(value.slide_ids)) return false;
  if (!isNonEmptyString(value.notes)) return false;
  const status = normalizeCoverageStatus(value.status || (allowPlanned ? "planned" : "covered")) || (allowPlanned ? "planned" : "covered");
  const allowedStatuses = ["covered", "missing", "blocked", "partial", "covered_with_ocr_gap_note", "inline_integrated", "standalone_supplement"];
  if (allowPlanned) {
    allowedStatuses.push("planned", "analysis_only");
  }
  if (!allowedStatuses.includes(status)) return false;
  const plannedPlaceholder = allowPlanned && ["planned", "analysis_only"].includes(status);
  if (numbers.length === 0 && !plannedPlaceholder) return false;
  if (status === "inline_integrated") {
    if (!isNonEmptyString(value.integration_method)) return false;
    if (!isNonEmptyString(value.narrative_context)) return false;
  }
  return true;
}

function isStructuredEquationCoverage(value, options = {}) {
  const normalized = canonicalizeEquationCoverageEntries(value);
  return Array.isArray(normalized) && normalized.length > 0 && normalized.every((entry) => isStructuredEquationCoverageEntry(entry, options));
}

function parseSlideOrdinal(slideId) {
  const raw = String(slideId || "").trim();
  if (!raw) return Number.NaN;
  const explicitMatch = raw.match(/^(?:s|slide|p)[-_ ]*0*(\d+)(?:\D.*)?$/i);
  if (explicitMatch) {
    return Number(explicitMatch[1]);
  }
  const numericMatch = raw.match(/^0*(\d+)(?:\D.*)?$/);
  return numericMatch ? Number(numericMatch[1]) : Number.NaN;
}

function notationSourceParagraphIds(entry) {
  const value = entry?.source_paragraph_ids ?? entry?.definition_source_paragraph_ids ?? entry?.source_paragraph_id;
  if (Array.isArray(value)) {
    return value.map((item) => String(item || "").trim()).filter(Boolean);
  }
  if (isNonEmptyString(value)) {
    return [String(value).trim()];
  }
  return [];
}

function notationSourceQuote(entry) {
  return String(entry?.source_quote ?? entry?.definition_source_quote ?? entry?.source_definition_en ?? "").trim();
}

function notationSourceDefinitionSummary(entry) {
  return String(entry?.source_definition_summary ?? entry?.speaker_definition_zh ?? entry?.definition_summary ?? "").trim();
}

function notationCoverageNotesFallback(entry) {
  if (!isPlainObject(entry)) return "";
  const explicitNotes = String(entry.notes || "").trim();
  if (explicitNotes) return explicitNotes;
  const summary = notationSourceDefinitionSummary(entry);
  if (summary) return summary;
  const meaning = String(entry.meaning ?? entry.definition ?? entry.explanation ?? "").trim();
  if (meaning) return meaning;
  const quote = notationSourceQuote(entry);
  if (quote) return quote;
  const symbol = String(entry.symbol ?? entry.term ?? entry.notation ?? entry.variable ?? entry.abbreviation ?? "").trim();
  if (symbol) {
    const slideIds = [
      ...(Array.isArray(entry.first_defined_slide_ids) ? entry.first_defined_slide_ids : []),
      ...(Array.isArray(entry.used_slide_ids) ? entry.used_slide_ids : []),
    ].map((item) => String(item || "").trim()).filter(Boolean);
    return slideIds.length > 0
      ? `${symbol} 已按 artifact 中的可见 slide 映射登记。`
      : `${symbol} 已按 artifact notation_coverage 登记。`;
  }
  return "";
}

function isStructuredNotationCoverageEntry(value, options = {}) {
  if (!isPlainObject(value)) return false;
  const allowPlanned = options.allowPlanned === true;
  const symbol = value.symbol ?? value.term ?? value.notation ?? value.variable ?? value.abbreviation;
  const meaning = value.meaning ?? value.definition ?? value.explanation;
  const firstDefinedSlideIds = value.first_defined_slide_ids ?? value.definition_slide_ids ?? value.introduced_slide_ids;
  const usedSlideIds = value.used_slide_ids ?? value.slide_ids ?? [];
  if (!isNonEmptyString(symbol)) return false;
  if (!isNonEmptyString(meaning)) return false;
  if (!Array.isArray(firstDefinedSlideIds)) return false;
  if (!allowPlanned && firstDefinedSlideIds.length === 0) return false;
  if (!Array.isArray(usedSlideIds)) return false;
  if (!isNonEmptyString(value.notes)) return false;
  const status = normalizeCoverageStatus(value.status || (allowPlanned ? "planned" : "defined")) || (allowPlanned ? "planned" : "defined");
  const allowedStatuses = ["defined", "covered", "missing", "blocked", "partial"];
  if (allowPlanned) {
    allowedStatuses.push("planned", "analysis_only");
  }
  if (!allowedStatuses.includes(status)) return false;
  const requiresSourceGrounding = ["defined", "covered", "partial", "planned", "analysis_only"].includes(status);
  if (requiresSourceGrounding) {
    if (notationSourceParagraphIds(value).length === 0) return false;
    if (!isNonEmptyString(notationSourceQuote(value))) return false;
    if (!isNonEmptyString(notationSourceDefinitionSummary(value))) return false;
    if (typeof value.defined_on_first_visible_use !== "boolean") return false;
  }
  if (hasOwn(value, "first_visible_slide_id") && !isNonEmptyString(value.first_visible_slide_id)) return false;
  const definedOrdinals = firstDefinedSlideIds.map(parseSlideOrdinal).filter(Number.isFinite);
  const usedOrdinals = usedSlideIds.map(parseSlideOrdinal).filter(Number.isFinite);
  if (definedOrdinals.length > 0 && usedOrdinals.length > 0) {
    const earliestDefinition = Math.min(...definedOrdinals);
    const earliestUse = Math.min(...usedOrdinals);
    if (earliestDefinition > earliestUse) {
      return false;
    }
  }
  return true;
}

function isStructuredNotationCoverage(value, options = {}) {
  return Array.isArray(value) && value.length > 0 && value.every((entry) => isStructuredNotationCoverageEntry(entry, options));
}

function normalizeArtifactNotationCoverageEntries(entries) {
  if (!Array.isArray(entries)) return entries;
  let changedAny = false;
  const normalized = entries.map((entry) => {
    if (!isPlainObject(entry)) return entry;
    const notes = notationCoverageNotesFallback(entry);
    if (!notes || String(entry.notes || "").trim()) return entry;
    changedAny = true;
    return {
      ...entry,
      notes,
    };
  });
  return changedAny ? normalized : entries;
}

function resolveArtifactPathFromReport(artifactPaths, artifactName) {
  if (!isPlainObject(artifactPaths)) return "";
  const direct = artifactPaths[artifactName];
  if (isNonEmptyString(direct)) {
    const trimmed = direct.trim();
    return path.isAbsolute(trimmed) && !pathIsInsideForbiddenArtifactRoot(trimmed) ? trimmed : "";
  }
  if (isPlainObject(direct)) {
    for (const key of ["path", "file", "artifact", "artifact_path", "output_path"]) {
      if (isNonEmptyString(direct[key])) {
        const trimmed = String(direct[key]).trim();
        return path.isAbsolute(trimmed) && !pathIsInsideForbiddenArtifactRoot(trimmed) ? trimmed : "";
      }
    }
  }
  return "";
}

function safeReadJsonArtifact(filePath) {
  try {
    if (!isNonEmptyString(filePath) || !fs.existsSync(filePath)) return null;
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
}

function artifactValidationCache(payload) {
  if (!isPlainObject(payload)) return null;
  if (!isPlainObject(payload.__artifactValidationCache)) {
    Object.defineProperty(payload, "__artifactValidationCache", {
      value: {},
      writable: true,
      configurable: true,
      enumerable: false,
    });
  }
  return payload.__artifactValidationCache;
}

function cachedJsonArtifact(payload, filePath) {
  if (!isNonEmptyString(filePath)) return null;
  const cache = artifactValidationCache(payload);
  if (!cache) return safeReadJsonArtifact(filePath);
  if (!isPlainObject(cache.jsonArtifacts)) {
    cache.jsonArtifacts = {};
  }
  if (!hasOwn(cache.jsonArtifacts, filePath)) {
    cache.jsonArtifacts[filePath] = safeReadJsonArtifact(filePath);
  }
  return cache.jsonArtifacts[filePath];
}

function readTextArtifact(filePath) {
  try {
    if (!isNonEmptyString(filePath) || !fs.existsSync(filePath)) return "";
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return "";
  }
}

function cachedTextArtifact(payload, filePath) {
  if (!isNonEmptyString(filePath)) return "";
  const cache = artifactValidationCache(payload);
  if (!cache) return readTextArtifact(filePath);
  if (!isPlainObject(cache.textArtifacts)) {
    cache.textArtifacts = {};
  }
  if (!hasOwn(cache.textArtifacts, filePath)) {
    cache.textArtifacts[filePath] = readTextArtifact(filePath);
  }
  return cache.textArtifacts[filePath];
}

function cachedParsedMainTexFrames(payload, mainTexPath) {
  if (!isNonEmptyString(mainTexPath)) return [];
  const cache = artifactValidationCache(payload);
  const tex = cachedTextArtifact(payload, mainTexPath);
  if (!tex) return [];
  if (!cache) return parseMainTexFrames(tex);
  if (!isPlainObject(cache.parsedMainTexFrames)) {
    cache.parsedMainTexFrames = {};
  }
  if (!hasOwn(cache.parsedMainTexFrames, mainTexPath)) {
    cache.parsedMainTexFrames[mainTexPath] = parseMainTexFrames(tex);
  }
  return cache.parsedMainTexFrames[mainTexPath];
}

function cachedFrameLookup(payload, mainTexPath) {
  if (!isNonEmptyString(mainTexPath)) return null;
  const frames = cachedParsedMainTexFrames(payload, mainTexPath);
  if (!Array.isArray(frames) || frames.length === 0) return null;
  const cache = artifactValidationCache(payload);
  if (!cache) return buildFrameLookup(frames);
  if (!isPlainObject(cache.frameLookups)) {
    cache.frameLookups = {};
  }
  if (!hasOwn(cache.frameLookups, mainTexPath)) {
    cache.frameLookups[mainTexPath] = buildFrameLookup(frames);
  }
  return cache.frameLookups[mainTexPath];
}

function slideIdFromPlan(slide) {
  return String(slide?.slide_id ?? slide?.id ?? "").trim();
}

function slideTextFromPlan(slide) {
  try {
    return JSON.stringify(slide || {});
  } catch {
    return "";
  }
}

function appendVisibleTextFragments(target, value) {
  if (typeof value === "string" || typeof value === "number") {
    const text = String(value).trim();
    if (text) target.push(text);
    return;
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      appendVisibleTextFragments(target, item);
    }
  }
}

function visibleTextFragmentsFromBlock(block) {
  if (!isPlainObject(block)) return [];
  const fragments = [];
  for (const key of [
    "title",
    "subtitle",
    "heading",
    "header",
    "caption",
    "label",
    "latex",
    "text",
    "content",
    "paragraph",
    "body",
    "claim",
    "summary",
    "description",
    "explanation",
    "legend",
    "alt_text",
    "alt",
    "value",
  ]) {
    appendVisibleTextFragments(fragments, block[key]);
  }
  for (const key of ["items", "bullets", "points", "list", "lines", "paragraphs", "captions"]) {
    appendVisibleTextFragments(fragments, block[key]);
  }
  for (const key of ["blocks", "children", "columns", "left", "right"]) {
    const nested = block[key];
    if (Array.isArray(nested)) {
      for (const item of nested) {
        fragments.push(...visibleTextFragmentsFromBlock(item));
      }
    } else if (isPlainObject(nested)) {
      fragments.push(...visibleTextFragmentsFromBlock(nested));
    }
  }
  return uniqueStrings(fragments);
}

function slideVisibleTextFromPlan(slide) {
  if (!isPlainObject(slide)) return "";
  const fragments = [];
  for (const key of ["title", "subtitle", "headline", "caption", "core_message", "summary", "description"]) {
    appendVisibleTextFragments(fragments, slide[key]);
  }
  for (const key of ["bullets", "items", "points", "list", "lines", "equations"]) {
    appendVisibleTextFragments(fragments, slide[key]);
  }
  // Include notation visibility arrays for Phase 4+ symbol-level checks
  for (const key of ["defines_symbols", "used_symbols"]) {
    appendVisibleTextFragments(fragments, slide[key]);
  }
  // Extract LaTeX from equation_blocks (slide-level equations may not be in slide.blocks)
  const eqs = Array.isArray(slide?.equation_blocks) ? slide.equation_blocks : [];
  for (const eq of eqs) {
    if (typeof eq?.latex === "string" && eq.latex.trim()) {
      appendVisibleTextFragments(fragments, eq.latex.trim());
    }
    if (typeof eq?.explanation === "string" && eq.explanation.trim()) {
      appendVisibleTextFragments(fragments, eq.explanation.trim());
    }
  }
  const blocks = Array.isArray(slide?.blocks) ? slide.blocks : [];
  for (const block of blocks) {
    fragments.push(...visibleTextFragmentsFromBlock(block));
  }
  return uniqueStrings(fragments).join("\n");
}

function visibleScaffoldTextLooksInternal(text) {
  const value = String(text || "").trim();
  if (!value) return false;
  return [
    /source_paragraph_ids/i,
    /来源段落|核心信息|原文锚点|关键读法|解释链条/,
    /这页负责|服务于未读论文听众|对未读者|你会看到|读这张图时|最重要的是/,
    /该页围绕[“"][^”"]+[”"]给出论文对应段落的主结论/,
    /正文保持正式学术表述|讲解提示保留在备注中/,
    /后续渲染阶段|PPT\s*原生布局|Beamer\s*布局|main\.tex|render(?:ed)?\s*fidelity|visible\s+prose/i,
    /本页作为内容承接页|完整覆盖论文论证链条/,
  ].some((pattern) => pattern.test(value));
}

function sanitizeVisibleScaffoldText(text) {
  let value = String(text || "").trim();
  if (!value) return "";
  value = value
    .replace(/^(?:核心信息|来源段落|原文锚点|关键读法|解释链条)\s*[:：]\s*/u, "")
    .replace(/^公式\s+(A\d+)\s*[:：]?\s*/iu, "式 ($1) ")
    .trim();
  if (!value) return "";
  if (/^(?:[ps]\d{1,4})(?:\s*[,，、;；/-]\s*(?:[ps]?\d{1,4}))*$/i.test(value)) {
    return "";
  }
  return visibleScaffoldTextLooksInternal(value) ? "" : value;
}

function sanitizeVisibleScaffoldArray(value) {
  let changed = false;
  const output = [];
  for (const item of Array.isArray(value) ? value : []) {
    if (typeof item === "string" || typeof item === "number") {
      const sanitized = sanitizeVisibleScaffoldText(item);
      if (sanitized !== String(item).trim()) changed = true;
      if (sanitized) output.push(sanitized);
      continue;
    }
    if (Array.isArray(item)) {
      const nested = sanitizeVisibleScaffoldArray(item);
      if (nested.changed || nested.value.length !== item.length) changed = true;
      if (nested.value.length > 0) output.push(nested.value);
      continue;
    }
    if (isPlainObject(item)) {
      const nested = sanitizeVisibleScaffoldBlock(item);
      if (nested.changed || !nested.value) changed = true;
      if (nested.value) output.push(nested.value);
      continue;
    }
    output.push(item);
  }
  return { value: output, changed };
}

function sanitizeVisibleScaffoldBlock(block) {
  if (!isPlainObject(block)) return { value: block, changed: false };
  let changed = false;
  const next = { ...block };
  for (const key of [
    "title",
    "subtitle",
    "heading",
    "header",
    "caption",
    "label",
    "latex",
    "text",
    "content",
    "paragraph",
    "body",
    "claim",
    "summary",
    "description",
    "explanation",
    "legend",
    "alt_text",
    "alt",
    "value",
  ]) {
    if (typeof next[key] === "string" || typeof next[key] === "number") {
      const original = String(next[key]).trim();
      const sanitized = sanitizeVisibleScaffoldText(original);
      if (sanitized !== original) changed = true;
      if (sanitized) {
        next[key] = sanitized;
      } else {
        delete next[key];
      }
    }
  }
  for (const key of ["items", "bullets", "points", "list", "lines", "paragraphs", "captions"]) {
    if (!Array.isArray(next[key])) continue;
    const sanitized = sanitizeVisibleScaffoldArray(next[key]);
    if (sanitized.changed || sanitized.value.length !== next[key].length) changed = true;
    if (sanitized.value.length > 0) {
      next[key] = sanitized.value;
    } else {
      delete next[key];
    }
  }
  for (const key of ["blocks", "children", "columns"]) {
    if (!Array.isArray(next[key])) continue;
    const sanitized = sanitizeVisibleScaffoldArray(next[key]);
    if (sanitized.changed || sanitized.value.length !== next[key].length) changed = true;
    if (sanitized.value.length > 0) {
      next[key] = sanitized.value;
    } else {
      delete next[key];
    }
  }
  for (const key of ["left", "right"]) {
    if (Array.isArray(next[key])) {
      const sanitized = sanitizeVisibleScaffoldArray(next[key]);
      if (sanitized.changed || sanitized.value.length !== next[key].length) changed = true;
      next[key] = sanitized.value;
    } else if (isPlainObject(next[key])) {
      const sanitized = sanitizeVisibleScaffoldBlock(next[key]);
      if (sanitized.changed || !sanitized.value) changed = true;
      if (sanitized.value) {
        next[key] = sanitized.value;
      } else {
        delete next[key];
      }
    }
  }
  if (visibleTextFragmentsFromBlock(next).length === 0) {
    return { value: null, changed: true };
  }
  return { value: next, changed };
}

function paragraphSummaryMapFromAnalysis(analysisDoc) {
  const map = new Map();
  for (const entry of safeArray(analysisDoc?.paragraph_ledger)) {
    const id = String(entry?.paragraph_id || entry?.id || "").trim();
    const summary = String(entry?.summary_sentence || entry?.summary || entry?.text || "").trim();
    if (id && summary) map.set(id, summary);
  }
  return map;
}

function slideSupplementalMessagesFromAnalysis(slideId, analysisDoc) {
  if (!slideId || !isPlainObject(analysisDoc)) return [];
  const matchesSlide = (entry) => {
    const ids = [
      ...safeArray(entry?.slide_ids),
      ...safeArray(entry?.planned_slide_ids),
      entry?.slide_id,
      entry?.planned_slide_id,
    ].map((item) => String(item || "").trim()).filter(Boolean);
    return ids.includes(slideId);
  };
  const messages = [];
  for (const entry of safeArray(analysisDoc.insight_pages)) {
    if (matchesSlide(entry)) messages.push(entry.message);
  }
  for (const entry of safeArray(analysisDoc.formal_statement_inventory)) {
    if (matchesSlide(entry)) messages.push(entry.source_meaning || entry.title);
  }
  for (const entry of safeArray(analysisDoc.figure_coverage)) {
    if (matchesSlide(entry)) messages.push(entry.source_caption || entry.notes);
  }
  for (const entry of safeArray(analysisDoc.table_coverage)) {
    if (matchesSlide(entry)) messages.push(entry.source_caption || entry.notes);
  }
  return uniqueStrings(messages.map((item) => String(item || "").trim()).filter(Boolean));
}

function fallbackVisibleBlocksForSlide(slide, analysisDoc) {
  const slideId = slideIdFromPlan(slide);
  const summaryMap = paragraphSummaryMapFromAnalysis(analysisDoc);
  const paragraphSummaries = safeArray(slide?.source_paragraph_ids)
    .map((id) => summaryMap.get(String(id || "").trim()))
    .filter(Boolean);
  const supplemental = slideSupplementalMessagesFromAnalysis(slideId, analysisDoc);
  const coreMessage = String(slide?.core_message || slide?.title || "").trim();
  const items = uniqueStrings([...paragraphSummaries, ...supplemental].filter(Boolean));
  if (items.length === 0 && coreMessage) {
    items.push(`本页聚焦${coreMessage}。`);
  }
  if (items.length === 0) return [];
  const blocks = [{ type: "paragraph", text: items[0] }];
  const remaining = items.slice(1, 5);
  if (remaining.length > 0) {
    blocks.push({ type: "bullet_list", items: remaining });
  } else if (coreMessage && !items[0].includes(coreMessage)) {
    blocks.push({ type: "takeaway_box", text: coreMessage });
  }
  return blocks;
}

function sanitizeSlideVisibleScaffold(slide, analysisDoc) {
  if (!isPlainObject(slide)) return { slide, changed: false };
  let changed = false;
  const next = { ...slide };
  if (typeof next.core_message === "string" || typeof next.core_message === "number") {
    const original = String(next.core_message).trim();
    const sanitized = sanitizeVisibleScaffoldText(original);
    if (sanitized !== original) changed = true;
    if (sanitized) {
      next.core_message = sanitized;
    } else if (isNonEmptyString(next.title)) {
      next.core_message = String(next.title).trim();
    } else {
      delete next.core_message;
    }
  }
  for (const key of ["bullets", "items", "points", "list", "lines", "equations"]) {
    if (!Array.isArray(next[key])) continue;
    const sanitized = sanitizeVisibleScaffoldArray(next[key]);
    if (sanitized.changed || sanitized.value.length !== next[key].length) changed = true;
    if (sanitized.value.length > 0) {
      next[key] = sanitized.value;
    } else {
      delete next[key];
    }
  }
  if (Array.isArray(next.blocks)) {
    const sanitizedBlocks = sanitizeVisibleScaffoldArray(next.blocks);
    if (sanitizedBlocks.changed || sanitizedBlocks.value.length !== next.blocks.length) changed = true;
    next.blocks = sanitizedBlocks.value;
  }
  const visibleText = slideVisibleTextFromPlan(next);
  const fallbackBlocks = fallbackVisibleBlocksForSlide(next, analysisDoc);
  const needsFallback = !visibleText
    || visibleScaffoldTextLooksInternal(visibleText)
    || safeArray(next.blocks).length === 0
    || (changed && fallbackBlocks.length > 0 && safeArray(next.blocks).length < 2);
  if (needsFallback) {
    if (fallbackBlocks.length > 0) {
      next.blocks = fallbackBlocks;
      changed = true;
    }
  }
  return { slide: next, changed };
}

function sanitizeRecoveredSlidesDocVisibleScaffold(slidesDoc, analysisDoc = null) {
  const doc = deepCloneJson(slidesDoc);
  if (!doc) return { doc: slidesDoc, changed: false, sanitized_slide_ids: [] };
  const getSlides = () => {
    if (Array.isArray(doc?.slides)) return { slides: doc.slides, assign: (slides) => { doc.slides = slides; } };
    if (Array.isArray(doc?.slide_plan)) return { slides: doc.slide_plan, assign: (slides) => { doc.slide_plan = slides; } };
    if (Array.isArray(doc)) return { slides: doc, assign: () => {} };
    return { slides: [], assign: () => {} };
  };
  const { slides, assign } = getSlides();
  if (slides.length === 0) return { doc, changed: false, sanitized_slide_ids: [] };
  let changed = false;
  const sanitizedSlideIds = [];
  const sanitizedSlides = slides.map((slide, index) => {
    const sanitized = sanitizeSlideVisibleScaffold(slide, analysisDoc);
    if (sanitized.changed) {
      changed = true;
      sanitizedSlideIds.push(slideIdFromPlan(sanitized.slide) || `slide_${index + 1}`);
    }
    return sanitized.slide;
  });
  if (changed) assign(sanitizedSlides);
  return { doc: Array.isArray(doc) ? sanitizedSlides : doc, changed, sanitized_slide_ids: sanitizedSlideIds };
}

function rerenderPptArtifactsAfterSlidesSanitization(artifactPaths, slidesPath) {
  const mainPptxPath = resolveArtifactPathFromReport(artifactPaths, "main.pptx");
  if (!isNonEmptyString(mainPptxPath) || !isNonEmptyString(slidesPath)) {
    return { rerendered: false, error: "missing slides.json or main.pptx path" };
  }
  const python = fs.existsSync(PPT_RENDERER_PYTHON) ? PPT_RENDERER_PYTHON : DEFAULT_PYTHON_EXECUTABLE;
  if (!fs.existsSync(python)) {
    return { rerendered: false, error: `missing python executable: ${python}` };
  }
  const args = [PPT_RENDERER_BIN, slidesPath, mainPptxPath];
  const result = spawnSync(python, args, {
    cwd: path.dirname(slidesPath),
    encoding: "utf8",
    timeout: 180000,
  });
  if (result.error || result.status !== 0) {
    return {
      rerendered: false,
      error: compactSingleLine(result.error?.message || result.stderr || result.stdout || `renderer exited ${result.status}`, 400),
    };
  }
  return { rerendered: true };
}

function artifactMtimeMs(filePath) {
  try {
    if (!isNonEmptyString(filePath) || !fs.existsSync(filePath)) return 0;
    return fs.statSync(filePath).mtimeMs || 0;
  } catch {
    return 0;
  }
}

function slidesJsonNewerThanPptx(artifactPaths, slidesPath) {
  const mainPptxPath = resolveArtifactPathFromReport(artifactPaths, "main.pptx");
  if (!isNonEmptyString(mainPptxPath) || !fs.existsSync(mainPptxPath)) return false;
  return artifactMtimeMs(slidesPath) > artifactMtimeMs(mainPptxPath) + 1000;
}

function sanitizeSlidesJsonArtifactForVisibleScaffold(artifactPaths, payload = null, options = {}) {
  const slidesPath = resolveArtifactPathFromReport(artifactPaths, "slides.json");
  if (!isNonEmptyString(slidesPath) || !fs.existsSync(slidesPath)) {
    return { changed: false, sanitized_slide_ids: [], rerendered: false };
  }
  const slidesDoc = safeReadJsonArtifact(slidesPath);
  if (!slidesDoc) return { changed: false, sanitized_slide_ids: [], rerendered: false };
  const shouldRerenderForPhase = options.rerenderPptx !== false
    && taskIsPpt(payload)
    && deckPhaseIndex(payload) >= 5;
  const analysisDoc = safeReadJsonArtifact(resolveArtifactPathFromReport(artifactPaths, "analysis.json"));
  const sanitized = sanitizeRecoveredSlidesDocVisibleScaffold(slidesDoc, analysisDoc);
  if (!sanitized.changed) {
    const renderResult = shouldRerenderForPhase && options.rerenderWhenStale !== false && slidesJsonNewerThanPptx(artifactPaths, slidesPath)
      ? rerenderPptArtifactsAfterSlidesSanitization(artifactPaths, slidesPath)
      : { rerendered: false };
    return { changed: false, sanitized_slide_ids: [], ...renderResult };
  }
  fs.writeFileSync(slidesPath, `${JSON.stringify(sanitized.doc, null, 2)}\n`, "utf8");
  const renderResult = shouldRerenderForPhase
    ? rerenderPptArtifactsAfterSlidesSanitization(artifactPaths, slidesPath)
    : { rerendered: false };
  return {
    changed: true,
    sanitized_slide_ids: sanitized.sanitized_slide_ids,
    ...renderResult,
  };
}

function countVisibleListItems(value) {
  if (!Array.isArray(value)) return 0;
  let count = 0;
  for (const item of value) {
    if (typeof item === "string" || typeof item === "number") {
      if (String(item).trim()) count += 1;
      continue;
    }
    if (isPlainObject(item) && visibleTextFragmentsFromBlock(item).length > 0) {
      count += 1;
    }
  }
  return count;
}

function plannedVisibleBulletCountFromSlide(slide) {
  const blocks = Array.isArray(slide?.blocks) ? slide.blocks : [];
  let count = 0;
  for (const key of ["bullets", "items", "points", "list", "lines"]) {
    count += countVisibleListItems(slide?.[key]);
  }
  for (const block of blocks) {
    if (!isPlainObject(block)) continue;
    const type = String(block.type || "").trim().toLowerCase();
    if (!["bullet_list", "takeaway", "comparison_block", "closing", "qa_notes"].includes(type)) continue;
    for (const key of ["items", "bullets", "points", "list", "lines"]) {
      count += countVisibleListItems(block[key]);
    }
  }
  return count;
}

function slideHasExplicitOverlayPlan(slide) {
  return isNonEmptyStructuredValue(slide?.overlay_plan);
}

function denseFormulaSlideIdsFromOverlayStrategy(value) {
  const ids = [];
  const candidates = [value];
  if (isPlainObject(value?.strategy)) candidates.push(value.strategy);
  if (isPlainObject(value?.plan)) candidates.push(value.plan);
  if (isPlainObject(value?.details)) candidates.push(value.details);
  for (const candidate of candidates) {
    if (!isPlainObject(candidate)) continue;
    for (const key of ["dense_formula_pages", "dense_formula_slide_ids", "dense_formula_slides"]) {
      if (Array.isArray(candidate[key])) {
        ids.push(...candidate[key].map((item) => String(item || "").trim()).filter(Boolean));
      }
    }
  }
  return uniqueStrings(ids);
}

function denseFormulaSlideIdSet(content, analysisDoc) {
  return new Set([
    ...denseFormulaSlideIdsFromOverlayStrategy(content?.overlay_strategy),
    ...denseFormulaSlideIdsFromOverlayStrategy(analysisDoc?.overlay_strategy),
  ]);
}

function equationCoverageDiagnosticsOnly(items) {
  return (Array.isArray(items) ? items : []).filter((item) => {
    const text = String(item || "");
    return /equation_coverage|equation-heavy|tagged equation|visible equation|equation block|equation numbers/i.test(text)
      && !/notation_coverage/i.test(text);
  });
}

function notationCoverageDiagnosticsOnly(items) {
  return (Array.isArray(items) ? items : []).filter((item) =>
    /notation_coverage|symbol|defined before use|first defined|first appearance|首现|符号|记号|可见符号|visible symbols/i.test(String(item || ""))
  );
}

function readBalancedTexGroup(source, startIndex, openChar, closeChar) {
  if (source[startIndex] !== openChar) return null;
  let depth = 0;
  for (let index = startIndex; index < source.length; index += 1) {
    const char = source[index];
    if (char === openChar) {
      depth += 1;
      continue;
    }
    if (char === closeChar) {
      depth -= 1;
      if (depth === 0) {
        return {
          value: source.slice(startIndex + 1, index),
          endIndex: index + 1,
        };
      }
    }
  }
  return null;
}

function replaceTexorpdfstringWithFallback(value) {
  const source = String(value || "");
  if (!source.includes("\\texorpdfstring")) return source;
  let result = "";
  let cursor = 0;
  while (cursor < source.length) {
    const markerIndex = source.indexOf("\\texorpdfstring", cursor);
    if (markerIndex === -1) {
      result += source.slice(cursor);
      break;
    }
    result += source.slice(cursor, markerIndex);
    let nextIndex = markerIndex + "\\texorpdfstring".length;
    while (/\s/.test(source[nextIndex] || "")) nextIndex += 1;
    const texGroup = source[nextIndex] === "{"
      ? readBalancedTexGroup(source, nextIndex, "{", "}")
      : null;
    if (!texGroup) {
      result += "\\texorpdfstring";
      cursor = nextIndex;
      continue;
    }
    nextIndex = texGroup.endIndex;
    while (/\s/.test(source[nextIndex] || "")) nextIndex += 1;
    const pdfGroup = source[nextIndex] === "{"
      ? readBalancedTexGroup(source, nextIndex, "{", "}")
      : null;
    if (!pdfGroup) {
      result += texGroup.value;
      cursor = texGroup.endIndex;
      continue;
    }
    result += pdfGroup.value || texGroup.value;
    cursor = pdfGroup.endIndex;
  }
  return result;
}

function normalizeFrameTitleForComparison(value) {
  const withPdfFallback = replaceTexorpdfstringWithFallback(value);
  return withPdfFallback
    .replace(/\\leq?\b/g, "≤")
    .replace(/\\geq?\b/g, "≥")
    .replace(/\\neq\b/g, "≠")
    .replace(/\\approx\b/g, "≈")
    .replace(/\\to\b/g, "→")
    .replace(/\\mapsto\b/g, "↦")
    .replace(/\\infty\b/g, "∞")
    .replace(/\$(.*?)\$/g, "$1")
    .replace(/\\([#$%&_{}])/g, "$1")
    .replace(/\\[a-zA-Z]+\*?(?:\[[^\]]*\])?/g, " ")
    .replace(/[{}]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeFrameLabel(value) {
  return String(value || "").trim();
}

function labelLooksLikeDeckSlideId(value) {
  return /^s\d{1,4}(?:[a-z][a-z0-9]*|[_-][a-z0-9]+)?$/i.test(String(value || "").trim());
}

function extractFrameLabelFromOptions(optionText) {
  const options = String(optionText || "");
  const match = options.match(/(?:^|,)\s*label\s*=\s*([^,\]]+)/i);
  return match ? String(match[1] || "").trim() : "";
}

function extractFrameLabelsFromBody(body) {
  const labels = [];
  const seen = new Set();
  for (const match of String(body || "").matchAll(/\\label\{([^}]+)\}/g)) {
    const label = String(match[1] || "").trim();
    if (!label || seen.has(label)) continue;
    seen.add(label);
    labels.push(label);
  }
  return labels;
}

function preferredFrameLabel(optionLabel, bodyLabels) {
  const fromOptions = String(optionLabel || "").trim();
  if (fromOptions) return fromOptions;
  return safeArray(bodyLabels).find((label) => labelLooksLikeDeckSlideId(label)) || safeArray(bodyLabels)[0] || "";
}

function canonicalEquationNumberKey(value) {
  if (typeof value === "number" && Number.isInteger(value) && value > 0) {
    return String(value);
  }
  if (typeof value === "number" && Number.isFinite(value) && value > 0) {
    return String(value).replace(/\.0+$/, "");
  }
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (/^\d+$/.test(trimmed)) return String(Number(trimmed));
    const decimalMatch = trimmed.match(/^(\d+)\.(\d+)$/);
    if (decimalMatch) {
      const section = Number(decimalMatch[1]);
      const equation = Number(decimalMatch[2]);
      if (section === 2 || section === 3) return String(equation);
      return `${section}.${equation}`;
    }
    const appendixMatch = trimmed.match(/^([AB])0*([1-9]\d*)$/i);
    if (appendixMatch) return `${appendixMatch[1].toUpperCase()}${Number(appendixMatch[2])}`;
    const appendixDecimalMatch = trimmed.match(/^([AB])\.0*([1-9]\d*)$/i);
    if (appendixDecimalMatch) return `${appendixDecimalMatch[1].toUpperCase()}${Number(appendixDecimalMatch[2])}`;
  }
  return "";
}

function normalizeEquationSemanticKey(value) {
  return String(value || "")
    .trim()
    .replace(/^eqs?\.?\s*/i, "")
    .replace(/^equations?\s*/i, "")
    .replace(/[()]/g, "")
    .replace(/\s+/g, " ")
    .toLowerCase();
}

function equationKeysFromValues(values) {
  return uniqueStrings(
    safeArray(values)
      .flatMap((value) => {
        const canonical = canonicalEquationNumberKey(value);
        const semantic = normalizeEquationSemanticKey(value);
        return [canonical, semantic].filter(Boolean);
      })
  );
}

function frameTaggedEquationKeys(body) {
  const keys = [];
  const source = String(body || "");
  for (const match of source.matchAll(/\\tag\{([^}]+)\}/g)) {
    const tagContent = String(match[1] || "").trim();
    keys.push(...equationKeysFromValues(extractEquationNumbersFromText(tagContent)));
    const canonicalTagKey = canonicalEquationNumberKey(tagContent.replace(/[()]/g, "").split(/\s+/)[0]);
    if (canonicalTagKey) {
      keys.push(canonicalTagKey);
    }
    if (tagContent) {
      keys.push(normalizeEquationSemanticKey(tagContent));
    }
  }
  return uniqueStrings(keys);
}

function equationKeysForCoverageEntry(entry, numbers = []) {
  if (!isPlainObject(entry)) return equationKeysFromValues(numbers);
  const values = [...safeArray(numbers)];
  for (const field of [
    entry.equation_numbers,
    entry.numbers,
    entry.equations,
    entry.equation_ids,
    entry.source_label,
    entry.label,
    entry.equation_label,
  ]) {
    if (Array.isArray(field)) {
      values.push(...field);
    } else if (field !== undefined && field !== null) {
      values.push(field);
    }
  }
  return equationKeysFromValues(values);
}

function frameTaggedEquationKeySet(frame) {
  return new Set(frameTaggedEquationKeys(frame?.body));
}

function frameContainsEquationKeys(frame, numbers) {
  const expected = equationKeysFromValues(numbers);
  if (expected.length === 0) return false;
  const available = frameTaggedEquationKeySet(frame);
  return expected.some((key) => available.has(key));
}

function frameContainsAllEquationKeys(frame, numbers) {
  const expected = equationKeysFromValues(numbers);
  if (expected.length === 0) return false;
  const available = frameTaggedEquationKeySet(frame);
  return expected.some((key) => available.has(key));
}

function parseMainTexFrames(tex) {
  const frames = [];
  const source = String(tex || "");
  const beginMarker = "\\begin{frame}";
  const endMarker = "\\end{frame}";
  let cursor = 0;

  while (cursor < source.length) {
    const beginIndex = source.indexOf(beginMarker, cursor);
    if (beginIndex === -1) break;
    let headerIndex = beginIndex + beginMarker.length;
    let optionText = "";
    let overlaySpecText = "";
    while (/\s/.test(source[headerIndex] || "")) headerIndex += 1;
    if (source[headerIndex] === "<") {
      const overlaySpecGroup = readBalancedTexGroup(source, headerIndex, "<", ">");
      if (overlaySpecGroup) {
        overlaySpecText = String(overlaySpecGroup.value || "");
        headerIndex = overlaySpecGroup.endIndex;
        while (/\s/.test(source[headerIndex] || "")) headerIndex += 1;
      }
    }
    if (source[headerIndex] === "[") {
      const optionGroup = readBalancedTexGroup(source, headerIndex, "[", "]");
      if (optionGroup) {
        optionText = String(optionGroup.value || "");
        headerIndex = optionGroup.endIndex;
        while (/\s/.test(source[headerIndex] || "")) headerIndex += 1;
      }
    }

    let title = "";
    if (source[headerIndex] === "{") {
      const titleGroup = readBalancedTexGroup(source, headerIndex, "{", "}");
      if (titleGroup) {
        title = String(titleGroup.value || "").trim();
        headerIndex = titleGroup.endIndex;
      }
    }

    const endIndex = source.indexOf(endMarker, headerIndex);
    if (endIndex === -1) break;
    const body = source.slice(headerIndex, endIndex);
    const frameTex = source.slice(beginIndex, endIndex + endMarker.length);
    const itemCount = (body.match(/(^|\n)\s*\\item\b/g) || []).length;
    const displayEquationCount = (body.match(/\\eqs?\{|\\begin\{equation\*?\}|\\begin\{align\*?\}|\\\[/g) || []).length;
    const optionLabel = extractFrameLabelFromOptions(optionText);
    const bodyLabels = extractFrameLabelsFromBody(body);
    const label = preferredFrameLabel(optionLabel, bodyLabels);
    const allLabels = uniqueStrings([optionLabel, ...bodyLabels].filter(Boolean));
    const taggedEquationKeys = frameTaggedEquationKeys(body);
    const overlaySignalCount = (frameTex.match(/\\begin\{frame\}\s*<[^>]+>|\\pause\b|\\onslide\s*<[^>]+>|\\only\s*<[^>]+>|\\uncover\s*<[^>]+>|\\visible\s*<[^>]+>|\\alt\s*<[^>]+>|\\temporal\s*<[^>]+>|\\item\s*<[^>]+>|\\begin\{(?:itemize|enumerate)\}(?:\[[^\]]*<[^>]+>[^\]]*\])/g) || []).length;
    frames.push({
      ordinal: frames.length + 1,
      label,
      labels: allLabels,
      normalizedLabel: normalizeFrameLabel(label),
      normalizedLabels: uniqueStrings(allLabels.map((item) => normalizeFrameLabel(item)).filter(Boolean)),
      title,
      normalizedTitle: normalizeFrameTitleForComparison(title),
      body,
      overlaySpecText,
      itemCount,
      displayEquationCount,
      taggedEquationCount: taggedEquationKeys.length,
      taggedEquationKeys,
      visibleEquationSignalCount: Math.max(displayEquationCount, taggedEquationKeys.length),
      overlaySignalCount,
    });
    cursor = endIndex + endMarker.length;
  }
  return frames;
}

function buildFrameLookup(frames) {
  const byTitle = new Map();
  const byLabel = new Map();
  for (const frame of safeArray(frames)) {
    if (!isPlainObject(frame)) continue;
    const rawLabels = uniqueStrings([
      frame.label,
      ...safeArray(frame.labels),
    ].map((item) => String(item || "").trim()).filter(Boolean));
    const normalizedLabels = uniqueStrings([
      frame.normalizedLabel,
      ...safeArray(frame.normalizedLabels),
      ...rawLabels.map((item) => normalizeFrameLabel(item)),
    ].map((item) => String(item || "").trim()).filter(Boolean));
    const rawTitle = String(frame.title || "").trim();
    const normalizedTitle = String(frame.normalizedTitle || "").trim();
    for (const rawLabel of rawLabels) {
      if (rawLabel && !byLabel.has(rawLabel)) {
        byLabel.set(rawLabel, frame);
      }
    }
    for (const normalizedLabel of normalizedLabels) {
      if (normalizedLabel && !byLabel.has(normalizedLabel)) {
        byLabel.set(normalizedLabel, frame);
      }
    }
    if (rawTitle && !byTitle.has(rawTitle)) {
      byTitle.set(rawTitle, frame);
    }
    if (normalizedTitle && !byTitle.has(normalizedTitle)) {
      byTitle.set(normalizedTitle, frame);
    }
  }
  return { frames: safeArray(frames), byTitle, byLabel };
}

function frameMatchScoreForSlide(slide, frame) {
  if (!isPlainObject(slide) || !isPlainObject(frame)) return 0;
  const slideId = slideIdFromPlan(slide);
  const normalizedSlideId = normalizeFrameLabel(slideId);
  const rawTitle = String(slide?.title || "").trim();
  const normalizedTitle = normalizeFrameTitleForComparison(rawTitle);
  const rawFrameTitle = String(frame?.title || "").trim();
  const normalizedFrameTitle = String(frame?.normalizedTitle || "").trim();
  const rawFrameLabels = uniqueStrings([
    frame?.label,
    ...safeArray(frame?.labels),
  ].map((item) => String(item || "").trim()).filter(Boolean));
  const normalizedFrameLabels = uniqueStrings([
    frame?.normalizedLabel,
    ...safeArray(frame?.normalizedLabels),
    ...rawFrameLabels.map((item) => normalizeFrameLabel(item)),
  ].map((item) => String(item || "").trim()).filter(Boolean));

  const labelMatches = Boolean(
    slideId
    && (
      rawFrameLabels.includes(slideId)
      || (normalizedSlideId && normalizedFrameLabels.includes(normalizedSlideId))
    )
  );
  const exactTitleMatches = Boolean(
    rawTitle
    && (rawFrameTitle === rawTitle || (normalizedTitle && normalizedFrameTitle === normalizedTitle))
  );
  const alignedTitleMatches = titlesAreStructurallyAligned(rawTitle, rawFrameTitle);

  if (labelMatches && exactTitleMatches) return 50;
  if (exactTitleMatches) return 40;
  if (labelMatches && alignedTitleMatches) return 35;
  if (alignedTitleMatches) return 30;
  if (labelMatches) return 20;
  return 0;
}

function slideCanMatchAsDeckPrelude(slide) {
  const role = String(slide?.special_role ?? slide?.role ?? slide?.kind ?? slide?.type ?? "")
    .trim()
    .toLowerCase();
  return ["title", "title_page", "cover", "cover_page"].includes(role);
}

function frameHasSlideLabel(slideId, frame) {
  const normalizedSlideId = normalizeFrameLabel(slideId);
  if (!normalizedSlideId || !isPlainObject(frame)) return false;
  const labels = uniqueStrings([
    frame?.label,
    frame?.normalizedLabel,
    ...safeArray(frame?.labels),
    ...safeArray(frame?.normalizedLabels),
  ].map((item) => normalizeFrameLabel(item)).filter(Boolean));
  return labels.includes(normalizedSlideId);
}

function findBestMatchingFrameIndexForSlide(slide, frames, startIndex = 0) {
  const items = safeArray(frames);
  let bestIndex = -1;
  let bestScore = 0;
  for (let index = Math.max(0, startIndex); index < items.length; index += 1) {
    const score = frameMatchScoreForSlide(slide, items[index]);
    if (score <= 0) continue;
    if (score > bestScore) {
      bestScore = score;
      bestIndex = index;
      if (score >= 50) break;
    }
  }
  return bestIndex;
}

function findDeckPreludeFrameIndexForSlide(slide, frames, cursor = 0) {
  if (!slideCanMatchAsDeckPrelude(slide)) return -1;
  const slideId = slideIdFromPlan(slide);
  if (!slideId) return -1;
  const items = safeArray(frames);
  const limit = Math.min(Math.max(0, cursor), items.length);
  for (let index = 0; index < limit; index += 1) {
    if (frameHasSlideLabel(slideId, items[index])) {
      return index;
    }
  }
  return -1;
}

function buildOrderedSlideFrameWindows(slides, frameLookup) {
  const frames = safeArray(frameLookup?.frames);
  const orderedMatches = [];
  let cursor = 0;

  for (const slide of safeArray(slides)) {
    if (!isPlainObject(slide)) continue;
    const slideId = slideIdFromPlan(slide);
    if (!slideId) continue;
    let matchIndex = findBestMatchingFrameIndexForSlide(slide, frames, cursor);
    if (matchIndex < 0) {
      matchIndex = findDeckPreludeFrameIndexForSlide(slide, frames, cursor);
    }
    if (matchIndex < 0) {
      orderedMatches.push({ slide, slideId, frameIndex: -1, frame: null });
      continue;
    }
    orderedMatches.push({ slide, slideId, frameIndex: matchIndex, frame: frames[matchIndex] || null });
    if (matchIndex >= cursor) {
      cursor = matchIndex + 1;
    }
  }

  const windowBySlideId = new Map();
  const unmatchedSlideIds = [];
  const matched = orderedMatches.filter((entry) => entry.frameIndex >= 0);

  for (const entry of orderedMatches) {
    if (entry.frameIndex < 0) unmatchedSlideIds.push(entry.slideId);
  }

  const matchedInFrameOrder = matched.slice().sort((a, b) => a.frameIndex - b.frameIndex);
  for (let index = 0; index < matchedInFrameOrder.length; index += 1) {
    const current = matchedInFrameOrder[index];
    const next = matchedInFrameOrder[index + 1] || null;
    const startIndex = current.frameIndex;
    const endIndex = next ? next.frameIndex - 1 : frames.length - 1;
    windowBySlideId.set(current.slideId, frames.slice(startIndex, endIndex + 1));
  }

  return {
    frames,
    windowBySlideId,
    unmatchedSlideIds,
  };
}

function framesForSlide(slide, frameWindows, frameLookup, options = {}) {
  const slideId = slideIdFromPlan(slide);
  const windowFrames = slideId ? frameWindows?.windowBySlideId?.get(slideId) : null;
  if (Array.isArray(windowFrames) && windowFrames.length > 0) {
    return windowFrames;
  }
  const frame = findFrameForSlide(slide, frameLookup, options);
  return frame ? [frame] : [];
}

function framesForSlideId(slideId, frameWindows) {
  const windowFrames = frameWindows?.windowBySlideId?.get(slideId);
  return Array.isArray(windowFrames) ? windowFrames : [];
}

function frameCollectionVisibleEquationCount(frames) {
  return safeArray(frames).reduce(
    (sum, frame) => sum + Number(frame?.visibleEquationSignalCount || frame?.displayEquationCount || 0),
    0
  );
}

function frameCollectionContainsAllEquationKeys(frames, numbers) {
  const expected = uniqueStrings(safeArray(numbers).flatMap((value) => equationKeysFromValues(value)));
  if (expected.length === 0) return false;
  const available = new Set();
  for (const frame of safeArray(frames)) {
    for (const key of frameTaggedEquationKeySet(frame)) {
      available.add(key);
    }
  }
  return expected.every((key) => available.has(key));
}

function sourceDocumentPathFromTaskText(taskText) {
  const raw = String(taskText || "").trim();
  if (!raw.startsWith("/")) return "";
  const extensions = [".md", ".markdown", ".txt", ".pdf"];
  let best = "";
  for (const extension of extensions) {
    const index = raw.toLowerCase().indexOf(extension);
    if (index < 0) continue;
    const candidate = raw.slice(0, index + extension.length).trim();
    if (!best || candidate.length > best.length) {
      best = candidate;
    }
  }
  return best && fs.existsSync(best) ? best : "";
}

function sourceDocumentPathFromArtifacts(content, payload, analysisDoc) {
  const candidates = [
    analysisDoc?.source_path,
    analysisDoc?.source_file,
    analysisDoc?.input_path,
    analysisDoc?.paper_path,
    content?.source_path,
    payload?.source_path,
    sourceDocumentPathFromTaskText(payload?.task),
  ];
  for (const candidate of candidates) {
    if (!isNonEmptyString(candidate)) continue;
    const resolved = path.resolve(String(candidate).trim());
    if (fs.existsSync(resolved)) return resolved;
  }
  return "";
}

function readSourceDocumentTextForEquationInventory(filePath) {
  try {
    if (!isNonEmptyString(filePath)) return "";
    const lower = filePath.toLowerCase();
    if (lower.endsWith(".md") || lower.endsWith(".markdown") || lower.endsWith(".txt")) {
      return fs.readFileSync(filePath, "utf8");
    }
  } catch {
    // Artifact-local validation can continue without source text.
  }
  return "";
}

function sourceEquationInventoryFromArtifacts(content, payload, analysisDoc) {
  const filePath = sourceDocumentPathFromArtifacts(content, payload, analysisDoc);
  const text = readSourceDocumentTextForEquationInventory(filePath);
  if (!text) return null;
  const equations = uniqueSortedPositiveIntegers(extractEquationNumbersFromText(text));
  return {
    filePath,
    equations,
    expected_equations: inferContinuousEquationNumbers(equations),
    continuity_gaps: continuityGapEquationNumbers(equations),
  };
}

function sourceEquationCoverageCompletenessDiagnostics(content, payload, analysisDoc, equationCoverage) {
  const errors = [];
  const inventory = sourceEquationInventoryFromArtifacts(content, payload, analysisDoc);
  if (!inventory || inventory.expected_equations.length === 0) return errors;

  const resolvedStatuses = new Set([
    "covered",
    "covered_with_ocr_gap_note",
    "inline_integrated",
    "standalone_supplement",
  ]);
  const reportedNumbers = uniqueSortedPositiveIntegers(
    safeArray(equationCoverage)
      .filter((entry) => isPlainObject(entry) && resolvedStatuses.has(String(entry.status || "covered").trim().toLowerCase()))
      .flatMap((entry) => extractEquationNumbersFromCoverageValue(entry.equation_numbers ?? entry.numbers ?? entry.equations ?? entry.source_label ?? []))
  );
  const missingNumbers = inventory.expected_equations.filter((number) => !reportedNumbers.includes(number));
  if (missingNumbers.length > 0) {
    const continuitySuffix = inventory.continuity_gaps.length > 0
      ? `；源文编号连续性还暗示缺口 ${formatEquationNumberRanges(inventory.continuity_gaps)}，若原文 OCR 确实跳号，必须用 covered_with_ocr_gap_note 显式登记`
      : "";
    errors.push(`equation_coverage misses source-inferred numbered equations ${formatEquationNumberRanges(missingNumbers)}${continuitySuffix}`);
  }
  return errors;
}

function frameCollectionContainsSymbolCandidate(frames, candidates) {
  return safeArray(frames).some((frame) =>
    safeArray(candidates).some((candidate) => textContainsSymbolCandidate(candidate, frame?.body))
  );
}

function frameCollectionHasOverlaySignals(frames) {
  return safeArray(frames).some((frame) => Number(frame?.overlaySignalCount || 0) > 0);
}

function frameCollectionHasProgressiveOverlay(frames) {
  return safeArray(frames).some((frame) => {
    const body = frame?.body || '';
    return /<\+->|\\onslide\s*<[^>]+>|\\only\s*<[^>]+>|\\uncover\s*<[^>]+>|\\visible\s*<[^>]+>|\\alt\s*<[^>]+>|\\temporal\s*<[^>]+>|\\item\s*<[^>]+>|\\begin\{(?:itemize|enumerate)\}(?:\[[^\]]*<[^>]+>[^\]]*\])/.test(body);
  });
}

function findFrameForSlide(slide, frameLookup, options = {}) {
  const frames = safeArray(frameLookup?.frames);
  const byTitle = frameLookup?.byTitle instanceof Map ? frameLookup.byTitle : new Map();
  const byLabel = frameLookup?.byLabel instanceof Map ? frameLookup.byLabel : new Map();
  const slideId = slideIdFromPlan(slide);
  if (slideId && byLabel.has(slideId)) {
    return byLabel.get(slideId) || null;
  }
  const normalizedSlideId = normalizeFrameLabel(slideId);
  if (normalizedSlideId && byLabel.has(normalizedSlideId)) {
    return byLabel.get(normalizedSlideId) || null;
  }
  const rawTitle = String(slide?.title || "").trim();
  if (rawTitle && byTitle.has(rawTitle)) {
    return byTitle.get(rawTitle) || null;
  }
  const normalizedTitle = normalizeFrameTitleForComparison(rawTitle);
  if (normalizedTitle && byTitle.has(normalizedTitle)) {
    return byTitle.get(normalizedTitle) || null;
  }
  if (!options.allowOrdinalFallback) {
    return null;
  }
  const ordinal = parseSlideOrdinal(slideIdFromPlan(slide));
  if (Number.isFinite(ordinal) && ordinal >= 1 && ordinal <= frames.length) {
    return frames[ordinal - 1] || null;
  }
  return null;
}

function titlesAreStructurallyAligned(plannedTitle, actualTitle) {
  const planned = normalizeFrameTitleForComparison(plannedTitle);
  const actual = normalizeFrameTitleForComparison(actualTitle);
  if (!planned || !actual) return true;
  if (planned === actual) return true;
  if (planned.includes(actual) || actual.includes(planned)) {
    return Math.min(planned.length, actual.length) >= 8;
  }
  return false;
}

function actualDeckStructureAlignmentDiagnostics(content, payload) {
  const errors = [];
  if (!taskIsBeamer(payload) || !isPlainObject(content) || !isPlainObject(content.artifact_paths)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  const slidesDoc = cachedJsonArtifact(content, slidesPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0 || !isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) return errors;

  const frames = cachedParsedMainTexFrames(content, mainTexPath);
  if (frames.length === 0) return errors;

  const frameLookup = cachedFrameLookup(content, mainTexPath);
  const frameWindows = buildOrderedSlideFrameWindows(slides, frameLookup);

  if (frames.length < slides.length) {
    errors.push(`main.tex/slides.json structural drift: slides.json plans ${slides.length} slides but main.tex contains only ${frames.length} frames`);
  }

  if (frameWindows.unmatchedSlideIds.length > 0) {
    const preview = frameWindows.unmatchedSlideIds.slice(0, 5).join(", ");
    const suffix = frameWindows.unmatchedSlideIds.length > 5 ? ` 等 ${frameWindows.unmatchedSlideIds.length} 个 slide_id` : "";
    errors.push(`main.tex/slides.json structural drift: cannot align planned slides to rendered frame order (${preview}${suffix})`);
  }

  const plannedSlideLabelSet = new Set(
    slides
      .map((slide) => normalizeFrameLabel(slideIdFromPlan(slide)))
      .filter(Boolean)
  );
  const unknownRenderedSlideLabels = uniqueStrings(
    frames.flatMap((frame) => [frame?.label, ...safeArray(frame?.labels)])
      .map((label) => String(label || "").trim())
      .filter((label) => labelLooksLikeDeckSlideId(label))
      .filter((label) => !plannedSlideLabelSet.has(normalizeFrameLabel(label)))
  );
  if (unknownRenderedSlideLabels.length > 0) {
    const preview = unknownRenderedSlideLabels.slice(0, 8).join(", ");
    const suffix = unknownRenderedSlideLabels.length > 8 ? ` 等 ${unknownRenderedSlideLabels.length} 个 frame label` : "";
    errors.push(`main.tex/slides.json structural drift: rendered frame labels absent from slides.json (${preview}${suffix}); add matching slides.json entries before splitting frames or relabel frames to existing slide_id values`);
  }

  return errors;
}

function slideNeedsRenderedProseGuard(slide) {
  const kind = String(slide?.kind || "").trim().toLowerCase();
  return ["content", "equation_focus", "figure_focus", "table_focus", "comparison", "experiment_setup", "results"].includes(kind);
}

function actualDeckRenderFidelityDiagnostics(content, payload) {
  const errors = [];
  if (!taskIsBeamer(payload) || !isPlainObject(content) || !isPlainObject(content.artifact_paths)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  const mainPdfPath = resolveArtifactPathFromReport(content.artifact_paths, "main.pdf");
  const slidesDoc = cachedJsonArtifact(content, slidesPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0 || !isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) return errors;

  const frames = cachedParsedMainTexFrames(content, mainTexPath);
  const frameLookup = cachedFrameLookup(content, mainTexPath);
  const frameWindows = buildOrderedSlideFrameWindows(slides, frameLookup);
  const mainTex = cachedTextArtifact(content, mainTexPath);
  errors.push(...beamerMainTexLanguageAndLatexLeakDiagnostics(mainTex, { sourceLabel: "main.tex" }));
  const renderedPdfText = extractPdfTextIfAvailable(mainPdfPath);
  errors.push(...renderedTextLatexLeakDiagnostics(renderedPdfText, { sourceLabel: "main.pdf text" }));
  errors.push(...denseFormulaOverlayDiagnostics(content, payload, { requireTexRealization: true }));

  for (const slide of slides) {
    if (!isPlainObject(slide)) continue;
    const title = String(slide?.title || "").trim();
    if (!title) continue;
    const plannedBulletCount = plannedVisibleBulletCountFromSlide(slide);
    if (plannedBulletCount === 0) continue;
    const mappedFrames = framesForSlide(slide, frameWindows, frameLookup, { allowOrdinalFallback: false });
    if (mappedFrames.length === 0) continue;
    const actualBulletCount = mappedFrames.reduce((sum, frame) => sum + Number(frame?.itemCount || 0), 0);
    const displayEquationCount = frameCollectionVisibleEquationCount(mappedFrames);
    if (plannedBulletCount >= 4 && actualBulletCount === 0) {
      errors.push(`${slideIdFromPlan(slide) || title}: main.tex dropped all planned visible bullets for '${title}'`);
      continue;
    }
    if (slideNeedsRenderedProseGuard(slide) && plannedBulletCount >= 4 && actualBulletCount < 2) {
      errors.push(`${slideIdFromPlan(slide) || title}: main.tex keeps only ${actualBulletCount}/${plannedBulletCount} planned visible bullets for '${title}'`);
      continue;
    }
    if (displayEquationCount >= 3 && plannedBulletCount >= 3 && actualBulletCount < plannedBulletCount) {
      errors.push(`${slideIdFromPlan(slide) || title}: equation-heavy frame '${title}' keeps only ${actualBulletCount}/${plannedBulletCount} planned visible bullets in main.tex`);
    }
  }

  return errors;
}

function equationBlocksFromSlide(slide) {
  return equationBlocksFromStructuredValue(slide);
}

function slideRequiresExplicitOverlayPlan(slide, denseFormulaSlideIds) {
  if (!isPlainObject(slide)) return false;
  const slideId = slideIdFromPlan(slide);
  if (slideId && denseFormulaSlideIds.has(slideId)) return true;
  return equationBlocksFromSlide(slide).length >= 3;
}

function denseFormulaOverlayDiagnostics(content, payload, options = {}) {
  const errors = [];
  if (!taskIsBeamer(payload) || !isPlainObject(content) || !isPlainObject(content.artifact_paths)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  const requireTexRealization = options.requireTexRealization === true;
  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const analysisPath = resolveArtifactPathFromReport(content.artifact_paths, "analysis.json");
  const slidesDoc = cachedJsonArtifact(content, slidesPath);
  const analysisDoc = cachedJsonArtifact(content, analysisPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0) return errors;

  const denseFormulaSlideIds = denseFormulaSlideIdSet(content, analysisDoc);
  let frameLookup = null;
  let frameWindows = null;

  if (requireTexRealization) {
    const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
    if (!isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) {
      return errors;
    }
    const frames = cachedParsedMainTexFrames(content, mainTexPath);
    if (frames.length === 0) return errors;
    frameLookup = cachedFrameLookup(content, mainTexPath);
    frameWindows = buildOrderedSlideFrameWindows(slides, frameLookup);
  }

  for (const slide of slides) {
    if (!slideRequiresExplicitOverlayPlan(slide, denseFormulaSlideIds)) continue;
    const slideId = slideIdFromPlan(slide) || String(slide?.title || "unknown_slide").trim() || "unknown_slide";
    const title = String(slide?.title || slideId).trim();
    if (!slideHasExplicitOverlayPlan(slide)) {
      errors.push(`${slideId}: dense formula slide '${title}' must include explicit slide-level overlay_plan in slides.json; deck-level overlay_strategy is insufficient`);
      continue;
    }
    if (!requireTexRealization) continue;
    const mappedFrames = framesForSlide(slide, frameWindows, frameLookup, { allowOrdinalFallback: false });
    if (mappedFrames.length === 0) continue;
    if (!frameCollectionHasOverlaySignals(mappedFrames) && mappedFrames.length <= 1) {
      errors.push(`${slideId}: dense formula slide '${title}' maps to a single static main.tex frame with no overlay commands; realize overlay_plan via Beamer overlays or equivalent split frames`);
    }
    if (frameCollectionHasOverlaySignals(mappedFrames) && !frameCollectionHasProgressiveOverlay(mappedFrames)) {
      errors.push(`${slideId}: dense formula slide '${title}' has overlay commands but lacks progressive <+-> style reveal (only \\pause detected); <+-> is mandatory for dense formula slides — use \\begin{itemize}[<+->] or equivalent progressive reveal commands (\\onslide, \\only, \\uncover, \\visible, \\alt, \\item<...>); do NOT rely on \\pause alone`);
    }
  }

  return uniqueStrings(errors);
}

function paragraphOrdinalFromId(value) {
  const raw = String(value || "").trim();
  if (!raw) return Number.NaN;
  const match = raw.match(/(\d+)/);
  return match ? Number(match[1]) : Number.NaN;
}

function sourceParagraphIdsFromSlide(slide) {
  const direct = slide?.source_paragraph_ids;
  if (Array.isArray(direct)) {
    return direct.map((item) => String(item || "").trim()).filter(Boolean);
  }
  if (isNonEmptyString(slide?.source_paragraph_id)) {
    return [String(slide.source_paragraph_id).trim()];
  }
  if (Array.isArray(slide?.paragraph_ids)) {
    return slide.paragraph_ids.map((item) => String(item || "").trim()).filter(Boolean);
  }
  return [];
}

function slideRequiresSourceParagraphMapping(slide) {
  const kind = String(slide?.kind || "").trim().toLowerCase();
  if (["title", "roadmap", "conclusion_preview", "qa", "takeaways"].includes(kind)) {
    return false;
  }
  const bucket = String(slide?.bucket || "").trim().toLowerCase();
  return bucket === "body";
}

function paragraphLedgerFromArtifacts(content, analysisDoc) {
  if (Array.isArray(content?.paragraph_ledger)) return content.paragraph_ledger;
  if (Array.isArray(analysisDoc?.paragraph_ledger)) return analysisDoc.paragraph_ledger;
  return [];
}

function paragraphLedgerSummaryText(entry) {
  return entry?.summary_sentence ?? entry?.summary ?? entry?.summary_zh ?? entry?.summary_text ?? "";
}

function beamerParagraphLedgerLanguageDiagnostics(content, payload) {
  if (!taskIsBeamer(payload) || !isPlainObject(content)) return [];
  const analysisPath = resolveArtifactPathFromReport(content.artifact_paths, "analysis.json");
  const analysisDoc = cachedJsonArtifact(content, analysisPath);
  return paragraphLedgerLanguageDiagnostics(paragraphLedgerFromArtifacts(content, analysisDoc));
}

function deckDeclaresNoHardTimeCap(content, analysisDoc, slidesDoc) {
  if (content?.timing_plan?.no_hard_time_cap === true) return true;
  if (analysisDoc?.timing_plan?.no_hard_time_cap === true) return true;
  const combined = JSON.stringify({
    timing_plan: content?.timing_plan,
    analysis_timing_plan: analysisDoc?.timing_plan,
    analysis_timing_allocation: analysisDoc?.timing_allocation,
    analysis_notes: analysisDoc?.notes,
    slides_timing_plan: slidesDoc?.timing_plan,
    slides_notes: slidesDoc?.notes,
  });
  return /没有时间限制|无时间限制|不设总时长|no hard time cap|no preset duration|open-ended duration/i.test(combined);
}

function deckUsesFixedTotalDurationCap(analysisDoc, slidesDoc) {
  const directCaps = [
    Number(analysisDoc?.target_minutes),
    Number(analysisDoc?.estimated_minutes),
    Number(slidesDoc?.target_minutes),
    Number(slidesDoc?.estimated_minutes),
  ];
  if (directCaps.some((value) => Number.isFinite(value) && value > 0)) {
    return true;
  }
  const timingAllocation = Array.isArray(analysisDoc?.timing_allocation) ? analysisDoc.timing_allocation : [];
  return timingAllocation.some((entry) => Number.isFinite(Number(entry?.minutes)) && Number(entry.minutes) > 0);
}

function normalizeNotationSymbolText(symbol) {
  let normalized = String(symbol || "").trim();
  if (!normalized) return "";
  if (
    (normalized.startsWith("`") && normalized.endsWith("`"))
    || (normalized.startsWith('"') && normalized.endsWith('"'))
    || (normalized.startsWith("'") && normalized.endsWith("'"))
  ) {
    normalized = normalized.slice(1, -1).trim();
  }
  let changed = true;
  while (changed) {
    changed = false;
    if (/^\$([\s\S]+)\$$/.test(normalized)) {
      normalized = normalized.replace(/^\$([\s\S]+)\$$/, "$1").trim();
      changed = true;
    }
    if (/^\\\(([\s\S]+)\\\)$/.test(normalized)) {
      normalized = normalized.replace(/^\\\(([\s\S]+)\\\)$/, "$1").trim();
      changed = true;
    }
    if (/^\\\[([\s\S]+)\\\]$/.test(normalized)) {
      normalized = normalized.replace(/^\\\[([\s\S]+)\\\]$/, "$1").trim();
      changed = true;
    }
    const strippedFontWrappers = stripTexStyleWrappers(normalized);
    if (strippedFontWrappers !== normalized) {
      normalized = strippedFontWrappers.trim();
      changed = true;
    }
  }
  return normalized
    .replace(/\\_/g, "_")
    .replace(/\\\{/g, "{")
    .replace(/\\\}/g, "}")
    .trim();
}

function normalizeSimpleSubscriptNotation(symbol) {
  return String(symbol || "").replace(
    /^((?:\\[A-Za-z]+)|[A-Za-z]|[ΔΩωθαβφνδμξεϵ])_([A-Za-z0-9]+)$/u,
    "$1_{$2}",
  );
}

function canonicalizeSymbolToken(symbol) {
  const greekMap = new Map([
    ["∂Ω", "\\partial\\Omega"],
    ["Δ", "\\Delta"],
    ["Ω", "\\Omega"],
    ["ω", "\\omega"],
    ["θ", "\\theta"],
    ["α", "\\alpha"],
    ["β", "\\beta"],
    ["φ", "\\phi"],
    ["ν", "\\nu"],
    ["δ", "\\delta"],
    ["μ", "\\mu"],
    ["ξ", "\\xi"],
    ["ε", "\\varepsilon"],
    ["ϵ", "\\varepsilon"],
  ]);
  const combiningAccentMap = new Map([
    ["\u0300", "grave"],
    ["\u0301", "acute"],
    ["\u0302", "hat"],
    ["\u0303", "tilde"],
    ["\u0304", "bar"],
    ["\u0306", "breve"],
    ["\u0307", "dot"],
    ["\u0308", "ddot"],
    ["\u030c", "check"],
    ["\u20d7", "vec"],
  ]);
  let normalized = String(symbol || "").replace(/\s+/g, "").trim();
  if (!normalized) return "";
  const decoratedMatch = normalized.normalize("NFD").match(/^(.+?)([\u0300-\u036f\u20d7]+)$/u);
  if (decoratedMatch) {
    let [, baseToken, combiningMarks] = decoratedMatch;
    baseToken = normalizeSimpleSubscriptNotation(baseToken);
    for (const [source, replacement] of greekMap.entries()) {
      baseToken = baseToken.split(source).join(replacement);
    }
    if (baseToken) {
      let accented = baseToken;
      let supported = true;
      for (const mark of [...combiningMarks]) {
        const accentMacro = combiningAccentMap.get(mark);
        if (!accentMacro) {
          supported = false;
          break;
        }
        const simpleAccentTarget = /^\\[A-Za-z]+(?:_\{[A-Za-z0-9]+\})?$/.test(accented);
        accented = simpleAccentTarget ? `\\${accentMacro}${accented}` : `\\${accentMacro}{${accented}}`;
      }
      if (supported) {
        normalized = accented;
      }
    }
  }
  normalized = normalizeSimpleSubscriptNotation(normalized);
  for (const [source, replacement] of greekMap.entries()) {
    normalized = normalized.split(source).join(replacement);
  }
  if (/^g\([A-Za-z]\)$/.test(normalized)) {
    return normalized;
  }
  return normalized;
}

function splitNotationSymbolPieces(symbol) {
  const raw = normalizeNotationSymbolText(symbol);
  if (!raw) return [];
  const pieces = [];
  let current = "";
  let depth = 0;
  for (const char of raw) {
    if (char === "(" || char === "[" || char === "{") {
      depth += 1;
      current += char;
      continue;
    }
    if (char === ")" || char === "]" || char === "}") {
      depth = Math.max(0, depth - 1);
      current += char;
      continue;
    }
    if (depth === 0 && (char === "/" || char === "," || char === ";")) {
      const piece = current.trim();
      if (piece) pieces.push(piece);
      current = "";
      continue;
    }
    current += char;
  }
  const tail = current.trim();
  if (tail) pieces.push(tail);
  return pieces;
}

function symbolCandidatesFromNotationEntry(symbol) {
  const raw = normalizeNotationSymbolText(symbol);
  if (!raw || /UNKNOWN_RECOVERED_SYMBOL/i.test(raw)) return [];

  const indexedUppercaseSymbol = raw.match(/^([A-Z])_(\{[^}]+\}|[A-Za-z0-9]+)(\(.+\))?$/u);
  if (indexedUppercaseSymbol) {
    return [canonicalizeSymbolToken(raw)].filter(Boolean);
  }

  const pieces = splitNotationSymbolPieces(raw);
  const expanded = [];
  const greekWithIndexMap = {
    "Δ": "\\Delta",
    "Ω": "\\Omega",
    "ω": "\\omega",
    "θ": "\\theta",
    "α": "\\alpha",
    "β": "\\beta",
    "φ": "\\phi",
    "ν": "\\nu",
    "δ": "\\delta",
    "μ": "\\mu",
    "ξ": "\\xi",
    "ε": "\\varepsilon",
    "ϵ": "\\varepsilon",
  };
  for (const piece of pieces) {
    expanded.push(piece);
    if (/^\\[A-Za-z]+$/.test(piece)) {
      expanded.push(piece.replace(/^\\/, ""));
    }
    const macroWithArgs = piece.match(/^(\\[A-Za-z]+)(\(.+\))$/);
    if (macroWithArgs) {
      expanded.push(macroWithArgs[1]);
    }
    const indexedSymbol = piece.match(/^((?:\\[A-Za-z]+)|[A-Za-z]|[ΔΩωθαβφνδμξεϵ])_(\{[^}]+\}|[A-Za-z0-9]+)(\(.+\))?$/u);
    if (indexedSymbol) {
      const [, baseSymbol, , suffix = ""] = indexedSymbol;
      const shouldAlsoMatchBaseSymbol = suffix || /^\\[A-Za-z]+$/.test(baseSymbol) || !/^[A-Z]$/.test(baseSymbol);
      if (shouldAlsoMatchBaseSymbol) {
        expanded.push(baseSymbol);
      }
      if (suffix) {
        expanded.push(`${baseSymbol}${suffix}`);
      }
    }
    if (/^g\([A-Za-z]\)$/.test(piece)) {
      expanded.push(piece.replace(/\([A-Za-z]\)$/, ""));
    }
    const greekWithIndex = piece.match(/^([ΔΩωθαβφνδμξεϵ])(\d+)$/u);
    if (greekWithIndex) {
      const [, greek, index] = greekWithIndex;
      expanded.push(`${greek}_${index}`);
      expanded.push(`${greek}_{${index}}`);
      if (greekWithIndexMap[greek]) {
        expanded.push(`${greekWithIndexMap[greek]}_${index}`);
        expanded.push(`${greekWithIndexMap[greek]}_{${index}}`);
      }
    }
    const indexedFunction = piece.match(/^([A-Za-z])(\d+)(\(.+\))$/);
    if (indexedFunction) {
      const [, base, index, suffix] = indexedFunction;
      expanded.push(`${base}_${index}${suffix}`);
      expanded.push(`${base}_{${index}}${suffix}`);
    }
  }
  return [...new Set(expanded.map(canonicalizeSymbolToken).filter(Boolean))];
}

function escapeNonSubscriptUnderscores(text) {
  let normalized = String(text || "");
  let previous = "";
  while (normalized !== previous) {
    previous = normalized;
    normalized = normalized.replace(/([A-Za-z0-9])_([A-Za-z0-9])/g, "$1\\\\_$2");
  }
  return normalized;
}

function stripTexStyleWrappers(text) {
  let normalized = String(text || "");
  let previous = "";
  while (normalized !== previous) {
    previous = normalized;
    normalized = normalized
      .replace(/\\(?:mathrm|mathit|mathbf|mathsf|mathtt|operatorname|texttt|textrm|boldsymbol|bm)\{([^{}]*)\}/g, "$1")
      .replace(/\\(?:mathrm|mathit|mathbf|mathsf|mathtt|operatorname|texttt|textrm|boldsymbol|bm)\s*(\\[A-Za-z]+(?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z])/g, "$1")
      .replace(/\\text\{([^{}]*)\}/g, "$1");
  }
  return normalized;
}

function normalizeTexSymbolHaystack(text) {
  let normalized = stripTexStyleWrappers(text);
  return normalized
    .replace(/\\_/g, "_")
    .replace(/\\\{/g, "{")
    .replace(/\\\}/g, "}")
    .replace(/\\([,:;!])/g, "$1");
}

function textContainsSymbolCandidate(candidate, text) {
  const haystack = String(text || "");
  const unescapedHaystack = haystack.includes("\\\\") ? haystack.replace(/\\\\/g, "\\") : haystack;
  const normalizedHaystack = normalizeTexSymbolHaystack(haystack);
  const normalizedUnescapedHaystack = normalizeTexSymbolHaystack(unescapedHaystack);
  const needle = canonicalizeSymbolToken(normalizeNotationSymbolText(candidate));
  if (!needle || !haystack) return false;
  const variants = new Set([needle]);
  const unicodeMap = {
    "\\Delta": "Δ",
    "\\Omega": "Ω",
    "\\omega": "ω",
    "\\theta": "θ",
    "\\alpha": "α",
    "\\beta": "β",
    "\\phi": "φ",
    "\\nu": "ν",
    "\\delta": "δ",
    "\\mu": "μ",
    "\\xi": "ξ",
    "\\epsilon": "ε",
    "\\varepsilon": "ε",
    "\\partial\\Omega": "∂Ω",
  };
  if (unicodeMap[needle]) variants.add(unicodeMap[needle]);
  if (needle.startsWith("\\")) variants.add(needle.replace(/^\\/, ""));
  if (!needle.startsWith("\\") && /^[A-Za-z]+(?:_\{?[A-Za-z0-9]+\}?)?$/.test(needle)) variants.add(`\\${needle}`);
  if (needle.includes("_{")) variants.add(needle.replace(/_\{([^}]+)\}/g, "_$1"));
  if (/_[A-Za-z0-9]+/.test(needle)) variants.add(needle.replace(/_([A-Za-z0-9]+)/g, "_{$1}"));
  if (needle.includes("_")) variants.add(escapeNonSubscriptUnderscores(needle));
  if (/^g\([A-Za-z]\)$/.test(needle)) variants.add(needle.replace(/\([A-Za-z]\)$/, ""));
  const accentNoBraceMatch = needle.match(/^\\(tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)(\\[A-Za-z]+(?:_\{[A-Za-z0-9]+\})?)$/);
  if (accentNoBraceMatch) variants.add(`\\${accentNoBraceMatch[1]}{${accentNoBraceMatch[2]}}`);
  const accentBracedMatch = needle.match(/^\\(tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)\{(.+)\}$/);
  if (accentBracedMatch) variants.add(`\\${accentBracedMatch[1]}${accentBracedMatch[2]}`);
  if (needle.includes(";")) variants.add(needle.replace(/;/g, "\\;"));
  for (const variant of [...variants]) {
    if (variant.includes("_")) {
      variants.add(escapeNonSubscriptUnderscores(variant));
    }
  }
  const haystacks = [
    haystack,
    haystack.replace(/\s+/g, ""),
    unescapedHaystack,
    unescapedHaystack.replace(/\s+/g, ""),
    normalizedHaystack,
    normalizedHaystack.replace(/\s+/g, ""),
    normalizedUnescapedHaystack,
    normalizedUnescapedHaystack.replace(/\s+/g, ""),
  ];
  return [...variants].some((variant) => {
    if (!variant) return false;
    const compactVariant = String(variant).replace(/\s+/g, "");
    return haystacks.some((entry) => entry.includes(variant) || entry.includes(compactVariant));
  });
}

function slideDefinitionMetadataSymbols(slide) {
  const collected = [];
  const visit = (value) => {
    if (Array.isArray(value)) {
      for (const item of value) visit(item);
      return;
    }
    if (!isPlainObject(value)) return;
    for (const key of ["defines_symbols", "defined_symbols", "introduced_symbols", "notation_symbols"]) {
      const current = value[key];
      if (Array.isArray(current)) {
        for (const item of current) {
          const text = String(item || "").trim();
          if (text) collected.push(text);
        }
      }
    }
    for (const key of ["blocks", "children", "columns", "left", "right"]) {
      visit(value[key]);
    }
  };
  visit(slide);
  return uniqueStrings(collected);
}

function deckPhaseIndex(payload) {
  const raw = Number(payload?.phase?.index || 0);
  return Number.isInteger(raw) && raw > 0 ? raw : 0;
}

function deckPhaseAllowsPlannedEquationCoverage(payload) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  return Boolean(phase && phase.finalPhase === false && deckPhaseIndex(payload) <= 2);
}

function deckPhaseAllowsPlannedNotationCoverage(payload) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  return Boolean(phase && phase.finalPhase === false && deckPhaseIndex(payload) <= 3);
}

function deckPhaseRequiresResolvedEquationCoverage(payload) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  if (!phase || phase.finalPhase === true) return true;
  return deckPhaseIndex(payload) >= 3;
}

function deckPhaseRequiresResolvedNotationCoverage(payload) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  if (!phase || phase.finalPhase === true) return true;
  return deckPhaseIndex(payload) >= 4;
}

function beamerPhaseIndex(payload) {
  return taskIsBeamer(payload) ? deckPhaseIndex(payload) : 0;
}

function isBeamerPhase2(payload) {
  return taskIsBeamer(payload) && beamerPhaseIndex(payload) === 2;
}

function isBeamerPhase3(payload) {
  return taskIsBeamer(payload) && beamerPhaseIndex(payload) === 3;
}

function isBeamerPhase4(payload) {
  return taskIsBeamer(payload) && beamerPhaseIndex(payload) === 4;
}

function isBeamerPhase5(payload) {
  return taskIsBeamer(payload) && beamerPhaseIndex(payload) === 5;
}

function isBeamerPhase6(payload) {
  return taskIsBeamer(payload) && beamerPhaseIndex(payload) === 6;
}

function isPptPhase(payload, phaseIndex) {
  return taskIsPpt(payload) && deckPhaseIndex(payload) === Number(phaseIndex);
}

function isPptPhase2(payload) {
  return isPptPhase(payload, 2);
}

function isPptPhase3(payload) {
  return isPptPhase(payload, 3);
}

function isPptPhase4(payload) {
  return isPptPhase(payload, 4);
}

function isPptPhase5(payload) {
  return isPptPhase(payload, 5);
}

function isPptPhase6(payload) {
  return isPptPhase(payload, 6);
}

const THIN_ARTIFACT_BACKED_BEAMER_PHASES = Object.freeze([3, 4, 5, 6]);
const THIN_ARTIFACT_BACKED_DISCOVERABLE_ARTIFACTS = Object.freeze([
  "analysis.json",
  "slides.json",
  "main.tex",
  "main.pdf",
  "main.pptx",
  "pptx_validation.json",
  "README.md",
  "asset_manifest.json",
  "figures",
]);
const THIN_ARTIFACT_BACKED_STRUCTURED_FIELDS = Object.freeze([
  "figure_coverage",
  "table_coverage",
  "equation_coverage",
  "notation_coverage",
  "formal_statement_inventory",
  "paragraph_ledger",
  "roadmap_page",
  "conclusion_preview_page",
  "body_appendix_split",
  "timing_plan",
  "overlay_strategy",
  "numerical_study_pages",
  "insight_pages",
  "audience_explanation_strategy",
]);
const THIN_ARTIFACT_BACKED_OPTIONAL_KEYS = Object.freeze([
  "pdf_pages",
  "compile_status",
  "readability_status",
  "tex_warnings",
  "render_status",
  "validation_status",
  "pptx_warnings",
  "layout_policy",
  "visible_prose_recovery_hint",
  "visible_prose_fidelity_final",
  "render_fidelity_safeguards",
  "main_pptx_generated",
  "partial_timed_out",
  "recovered_after_schema_validation",
  "recovered_schema_errors",
  "inferred_from_transcript",
  "inferred_from_artifacts",
  "beamer_artifact_recovered",
  "ppt_artifact_recovered",
  "previous_parse_error",
  "previous_schema_errors",
  "parse_error",
  "schema_errors",
  "raw_text",
]);

function phaseSupportsThinArtifactBackedProgrammerEnvelope(payload) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  if (!phase || phase.finalPhase === true) return false;
  return THIN_ARTIFACT_BACKED_BEAMER_PHASES.includes(deckPhaseIndex(payload));
}

function thinArtifactBackedRequiredArtifactNames(payload) {
  if (!phaseSupportsThinArtifactBackedProgrammerEnvelope(payload)) return [];
  const phaseRequiredArtifacts = Array.isArray(payload?.phase?.requiredArtifacts)
    ? payload.phase.requiredArtifacts.filter((name) => isNonEmptyString(name))
    : [];
  return uniqueStrings([
    "analysis.json",
    "slides.json",
    ...phaseRequiredArtifacts,
  ]);
}

function normalizeReportedArtifactPath(candidatePath) {
  if (!isNonEmptyString(candidatePath)) return "";
  return path.resolve(String(candidatePath).trim());
}

function reportedArtifactPathMatchesOutputDirectory(candidatePath, artifactName, outputDirectory) {
  if (!isNonEmptyString(candidatePath) || !isNonEmptyString(artifactName) || !isNonEmptyString(outputDirectory)) {
    return false;
  }
  const resolvedCandidate = normalizeReportedArtifactPath(candidatePath);
  const resolvedDirectory = path.resolve(String(outputDirectory).trim());
  if (!resolvedCandidate) return false;
  if (artifactName === "figures") {
    return path.basename(resolvedCandidate) === "figures"
      && path.dirname(resolvedCandidate) === resolvedDirectory;
  }
  return path.basename(resolvedCandidate) === artifactName
    && path.dirname(resolvedCandidate) === resolvedDirectory;
}

function requiredBeamerPackagedArtifactsForPayload(payload) {
  if (!taskIsBeamer(payload)) return [];
  const phase = payload?.phase;
  const phaseIndex = deckPhaseIndex(payload);
  return uniqueStrings([
    ...((!phase || phase.finalPhase === true || phaseIndex >= 5) ? ["main.pdf"] : []),
    ...((!phase || phase.finalPhase === true) ? ["README.md", "asset_manifest.json", "figures"] : []),
  ]);
}

function requiredPptPackagedArtifactsForPayload(payload) {
  if (!taskIsPpt(payload)) return [];
  const phase = payload?.phase;
  const phaseIndex = deckPhaseIndex(payload);
  return uniqueStrings([
    ...((!phase || phase.finalPhase === true || phaseIndex >= 5) ? ["main.pptx", "pptx_validation.json"] : []),
    ...((!phase || phase.finalPhase === true) ? ["README.md"] : []),
  ]);
}

function validateArtifactPathBundleConsistency(payload, content) {
  if (!isPlainObject(content) || !isPlainObject(content.artifact_paths)) {
    return [];
  }
  const artifactPaths = normalizeArtifactPathsMap(content.artifact_paths);
  if (!isPlainObject(artifactPaths)) {
    return [];
  }
  const outputDirectory = inferArtifactOutputDirectoryFromMap(artifactPaths);
  if (!isNonEmptyString(outputDirectory)) {
    return ["artifact_paths must resolve to one exact output directory"];
  }
  if (pathIsInsideForbiddenArtifactRoot(outputDirectory)) {
    return ["artifact_paths resolves to a forbidden artifact directory"];
  }

  const resolvedOutputDirectory = path.resolve(String(outputDirectory).trim());
  const errors = [];
  const explicitOutputDirectories = ["output_directory", "output_dir"]
    .map((key) => artifactPaths[key])
    .filter((value) => isNonEmptyString(value))
    .map((value) => path.resolve(String(value).trim()));
  if (explicitOutputDirectories.length > 1 && new Set(explicitOutputDirectories).size > 1) {
    errors.push("artifact_paths contains conflicting output_directory/output_dir values");
  }

  const discoverableArtifacts = taskIsPpt(payload)
    ? ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json", "README.md", "asset_manifest.json", "figures"]
    : ["analysis.json", "slides.json", "main.tex", "main.pdf", "README.md", "asset_manifest.json", "figures"];
  for (const artifactName of discoverableArtifacts) {
    const reportedPath = resolveArtifactPathFromReport(artifactPaths, artifactName);
    if (!isNonEmptyString(reportedPath)) continue;
    if (pathIsInsideForbiddenArtifactRoot(reportedPath)) {
      errors.push(`artifact_paths ${artifactName} points inside a forbidden artifact directory`);
      continue;
    }
    if (!reportedArtifactPathMatchesOutputDirectory(reportedPath, artifactName, resolvedOutputDirectory)) {
      errors.push(`artifact_paths ${artifactName} must stay in the same output directory ${resolvedOutputDirectory}`);
    }
  }

  for (const artifactName of requiredBeamerPackagedArtifactsForPayload(payload)) {
    if (!isNonEmptyString(resolveArtifactPathFromReport(artifactPaths, artifactName))) {
      errors.push(`artifact_paths missing required packaged Beamer artifact: ${artifactName}`);
    }
  }
  for (const artifactName of requiredPptPackagedArtifactsForPayload(payload)) {
    if (!isNonEmptyString(resolveArtifactPathFromReport(artifactPaths, artifactName))) {
      errors.push(`artifact_paths missing required packaged PPT artifact: ${artifactName}`);
    }
  }

  return uniqueStrings(errors);
}

function normalizeThinArtifactBundlePath(candidatePath, artifactName) {
  if (!isNonEmptyString(candidatePath)) return "";
  try {
    const resolvedPath = path.resolve(String(candidatePath).trim());
    const stat = fs.statSync(resolvedPath);
    if (artifactName === "figures") {
      return stat.isDirectory() ? resolvedPath : "";
    }
    return stat.isFile() ? resolvedPath : "";
  } catch {
    return "";
  }
}

function resolveExactThinArtifactBackedBundleFromContent(content, payload) {
  if (!phaseSupportsThinArtifactBackedProgrammerEnvelope(payload) || !isPlainObject(content)) {
    return null;
  }
  const artifactPaths = normalizeArtifactPathsMap(content.artifact_paths);
  if (!isPlainObject(artifactPaths)) return null;
  const outputDirectory = inferArtifactOutputDirectoryFromMap(artifactPaths);
  if (!isNonEmptyString(outputDirectory)) return null;
  const resolvedDirectory = path.resolve(String(outputDirectory).trim());
  try {
    const stat = fs.statSync(resolvedDirectory);
    if (!stat.isDirectory()) return null;
  } catch {
    return null;
  }

  const files = {
    output_directory: resolvedDirectory,
  };
  for (const artifactName of THIN_ARTIFACT_BACKED_DISCOVERABLE_ARTIFACTS) {
    const candidate = normalizeThinArtifactBundlePath(path.join(resolvedDirectory, artifactName), artifactName);
    if (candidate) {
      files[artifactName] = candidate;
    }
  }

  for (const artifactName of thinArtifactBackedRequiredArtifactNames(payload)) {
    if (!isNonEmptyString(files[artifactName])) {
      return null;
    }
  }

  for (const artifactName of THIN_ARTIFACT_BACKED_DISCOVERABLE_ARTIFACTS) {
    const reportedPath = resolveArtifactPathFromReport(artifactPaths, artifactName);
    if (!isNonEmptyString(reportedPath)) continue;
    const normalizedReportedPath = normalizeThinArtifactBundlePath(reportedPath, artifactName);
    if (!normalizedReportedPath) {
      return null;
    }
    if (!reportedArtifactPathMatchesOutputDirectory(normalizedReportedPath, artifactName, resolvedDirectory)) {
      return null;
    }
    if (isNonEmptyString(files[artifactName]) && path.resolve(files[artifactName]) !== path.resolve(normalizedReportedPath)) {
      return null;
    }
    files[artifactName] = normalizedReportedPath;
  }

  return {
    dir: resolvedDirectory,
    files,
  };
}

function thinArtifactBackedEnvelopeAllowedKeys(payload) {
  const keys = new Set([
    "summary",
    "answer",
    "checklist",
    "changed",
    "notes",
    "ready_for_review",
    "artifact_paths",
    ...THIN_ARTIFACT_BACKED_OPTIONAL_KEYS,
  ]);
  if (phaseSupportsThinArtifactBackedProgrammerEnvelope(payload) && deckPhaseIndex(payload) === 5) {
    keys.add("main_pdf_generated");
    if (taskIsPpt(payload)) {
      keys.add("main_pptx_generated");
    }
  }
  return keys;
}

function contentLooksLikeThinArtifactBackedProgrammerEnvelope(content, payload) {
  if (!phaseSupportsThinArtifactBackedProgrammerEnvelope(payload) || !isPlainObject(content)) {
    return false;
  }
  const requiredBaseFields = [
    ["summary", (value) => isNonEmptyString(value)],
    ["answer", (value) => isNonEmptyString(value)],
    ["checklist", (value) => Array.isArray(value)],
    ["changed", (value) => typeof value === "boolean"],
    ["notes", (value) => isNonEmptyStructuredValue(value)],
    ["ready_for_review", (value) => typeof value === "boolean"],
    ["artifact_paths", (value) => isPlainObject(value)],
  ];
  if (requiredBaseFields.some(([key, predicate]) => !hasOwn(content, key) || !predicate(content[key]))) {
    return false;
  }
  if (!isPlainObject(normalizeArtifactPathsMap(content.artifact_paths))) {
    return false;
  }
  const allowedKeys = thinArtifactBackedEnvelopeAllowedKeys(payload);
  if (Object.keys(content).some((key) => !allowedKeys.has(key))) {
    return false;
  }
  return THIN_ARTIFACT_BACKED_STRUCTURED_FIELDS.every((key) => !hasOwn(content, key));
}

function normalizeThinArtifactBackedProgrammerEnvelopeContent(content) {
  if (!isPlainObject(content)) return content;
  const normalizedArtifactPaths = normalizeArtifactPathsMap(content.artifact_paths);
  const normalizedNotes = hasOwn(content, "notes")
    ? normalizeStructuredNotesToString(content.notes)
    : content.notes;
  const changed = normalizedArtifactPaths !== content.artifact_paths
    || (hasOwn(content, "notes") && normalizedNotes !== content.notes);
  if (!changed) {
    return content;
  }
  return {
    ...content,
    artifact_paths: normalizedArtifactPaths,
    ...(hasOwn(content, "notes") ? { notes: normalizedNotes } : {}),
  };
}

function materializeThinArtifactBackedProgrammerContentForValidation(content, payload) {
  if (!contentLooksLikeThinArtifactBackedProgrammerEnvelope(content, payload)) {
    return content;
  }
  const normalizedContent = normalizeThinArtifactBackedProgrammerEnvelopeContent(content);
  const bundle = resolveExactThinArtifactBackedBundleFromContent(normalizedContent, payload);
  if (!bundle) {
    return normalizedContent;
  }

  const pptMode = taskIsPpt(payload);
  const pdfPages = pptMode ? 0 : getPdfPageCount(bundle.files["main.pdf"]);
  const recovered = pptMode
    ? buildPptArtifactBackedRecovery(bundle, bundle.files, null)
    : buildBeamerArtifactBackedRecovery(bundle, bundle.files, null, pdfPages);
  const analysisDoc = safeReadJsonArtifact(bundle.files["analysis.json"]);
  const artifactBacked = normalizeRecoveredCoverageForFinal(analysisDoc, recovered) || recovered;
  if (!isPlainObject(artifactBacked)) {
    return normalizedContent;
  }
  const slidesDoc = safeReadJsonArtifact(bundle.files["slides.json"]);
  const recoveredSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const recoveredSlideMap = buildSlideMap(recoveredSlides);

  const next = {
    ...normalizedContent,
    artifact_paths: {
      ...bundle.files,
    },
  };
  const materializedFieldNames = [
    ...THIN_ARTIFACT_BACKED_STRUCTURED_FIELDS,
    ...(pptMode ? [
      "render_status",
      "validation_status",
      "pptx_warnings",
      "layout_policy",
      "visible_prose_recovery_hint",
      "visible_prose_fidelity_final",
      "render_fidelity_safeguards",
      "main_pptx_generated",
    ] : [
      "compile_status",
      "readability_status",
      "tex_warnings",
      "layout_policy",
      "visible_prose_recovery_hint",
      "visible_prose_fidelity_final",
      "render_fidelity_safeguards",
      "pdf_pages",
    ]),
  ];
  const analysisPreferredFields = new Set([
    "figure_coverage",
    "table_coverage",
    "formal_statement_inventory",
    "paragraph_ledger",
    "timing_plan",
    "overlay_strategy",
    "audience_explanation_strategy",
  ]);
  const slidesPreferredFields = new Set([
    "equation_coverage",
    "notation_coverage",
    "roadmap_page",
    "conclusion_preview_page",
    "body_appendix_split",
    "numerical_study_pages",
    "insight_pages",
  ]);
  const exactArtifactField = (fieldName) => {
    if (fieldName === "figure_coverage") {
      return {
        present: true,
        value: deepCloneJson(buildRecoveredFigureCoverage(analysisDoc, slidesDoc, { requireVisibleFigureBlocks: pptMode })),
      };
    }
    if (fieldName === "table_coverage") {
      const tableCoverage = selectArtifactBackedTableCoverage(
        artifactBacked.table_coverage,
        analysisDoc,
        slidesDoc,
        recoveredSlideMap
      );
      if (isNonEmptyStructuredValue(tableCoverage)) {
        return {
          present: true,
          value: deepCloneJson(tableCoverage),
        };
      }
    }
    if (fieldName === "formal_statement_inventory") {
      return {
        present: true,
        value: deepCloneJson(buildRecoveredFormalInventory(analysisDoc, slidesDoc)),
      };
    }
    if (fieldName === "numerical_study_pages" && recoveredSlides.length > 0) {
      return {
        present: true,
        value: deepCloneJson(buildRecoveredNumericalStudyPages(recoveredSlides, slidesDoc, analysisDoc)),
      };
    }
    if (fieldName === "insight_pages" && recoveredSlides.length > 0) {
      return {
        present: true,
        value: deepCloneJson(buildRecoveredInsightPages(recoveredSlides, slidesDoc, analysisDoc)),
      };
    }
    if (fieldName === "overlay_strategy") {
      return {
        present: true,
        value: deepCloneJson(buildRecoveredOverlayStrategy(analysisDoc, slidesDoc, recoveredSlides, bundle.files)),
      };
    }
    if (fieldName === "audience_explanation_strategy") {
      return {
        present: true,
        value: deepCloneJson(buildRecoveredAudienceExplanationStrategy(analysisDoc, slidesDoc, recoveredSlides)),
      };
    }
    const preferredDoc = slidesPreferredFields.has(fieldName)
      ? slidesDoc
      : (analysisPreferredFields.has(fieldName) ? analysisDoc : null);
    const fallbackDoc = preferredDoc === slidesDoc ? analysisDoc : slidesDoc;
    if (isPlainObject(preferredDoc) && hasOwn(preferredDoc, fieldName)) {
      return {
        present: true,
        value: deepCloneJson(preferredDoc[fieldName]),
      };
    }
    if (isPlainObject(fallbackDoc) && hasOwn(fallbackDoc, fieldName)) {
      return {
        present: true,
        value: deepCloneJson(fallbackDoc[fieldName]),
      };
    }
    return { present: false, value: undefined };
  };

  for (const fieldName of materializedFieldNames) {
    const exactField = exactArtifactField(fieldName);
    if (exactField.present) {
      next[fieldName] = exactField.value;
      continue;
    }
    if (!hasOwn(next, fieldName) || !isNonEmptyStructuredValue(next[fieldName])) {
      if (hasOwn(artifactBacked, fieldName)) {
        next[fieldName] = deepCloneJson(artifactBacked[fieldName]);
      }
    }
  }

  return normalizeProgrammerResult({ content: next }, payload)?.content || next;
}

function materializeArtifactBackedProgrammerContentForValidation(content, payload) {
  const thinMaterialized = materializeThinArtifactBackedProgrammerContentForValidation(content, payload);
  if (thinMaterialized !== content) {
    return thinMaterialized;
  }
  if (!(taskIsBeamer(payload) || taskIsPpt(payload)) || !phaseAllowsArtifactRecovery(payload) || !isPlainObject(content)) {
    return content;
  }

  const artifactPaths = normalizeArtifactPathsMap(content.artifact_paths);
  if (!isPlainObject(artifactPaths) || Object.keys(artifactPaths).length === 0) {
    return content;
  }
  const analysisDoc = safeReadJsonArtifact(resolveArtifactPathFromReport(artifactPaths, "analysis.json"));
  const slidesDoc = safeReadJsonArtifact(resolveArtifactPathFromReport(artifactPaths, "slides.json"));
  if (!isPlainObject(analysisDoc) && !isPlainObject(slidesDoc)) {
    return content;
  }
  const recoveredSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const recoveredSlideMap = buildSlideMap(recoveredSlides);

  const next = {
    ...content,
    artifact_paths: artifactPaths,
  };
  let changed = next.artifact_paths !== content.artifact_paths;
  const analysisPreferredFields = new Set([
    "figure_coverage",
    "table_coverage",
    "formal_statement_inventory",
    "paragraph_ledger",
    "timing_plan",
    "overlay_strategy",
    "audience_explanation_strategy",
  ]);
  const slidesPreferredFields = new Set([
    "equation_coverage",
    "notation_coverage",
    "roadmap_page",
    "conclusion_preview_page",
    "body_appendix_split",
    "numerical_study_pages",
    "insight_pages",
  ]);
  const fieldNames = [...analysisPreferredFields, ...slidesPreferredFields];
  const fieldFromArtifacts = (fieldName) => {
    if (fieldName === "figure_coverage") {
      return buildRecoveredFigureCoverage(analysisDoc, slidesDoc, { requireVisibleFigureBlocks: taskIsPpt(payload) });
    }
    if (fieldName === "table_coverage") {
      return selectArtifactBackedTableCoverage(next.table_coverage, analysisDoc, slidesDoc, recoveredSlideMap);
    }
    if (fieldName === "equation_coverage") {
      return normalizeArtifactBackedEquationCoverage(next.equation_coverage, analysisDoc, slidesDoc, recoveredSlideMap);
    }
    if (fieldName === "formal_statement_inventory") {
      return buildRecoveredFormalInventory(analysisDoc, slidesDoc);
    }
    if (fieldName === "numerical_study_pages" && recoveredSlides.length > 0) {
      return buildRecoveredNumericalStudyPages(recoveredSlides, slidesDoc, analysisDoc);
    }
    if (fieldName === "insight_pages" && recoveredSlides.length > 0) {
      return buildRecoveredInsightPages(recoveredSlides, slidesDoc, analysisDoc);
    }
    if (fieldName === "overlay_strategy") {
      return buildRecoveredOverlayStrategy(analysisDoc, slidesDoc, recoveredSlides, next.artifact_paths);
    }
    if (fieldName === "audience_explanation_strategy") {
      return buildRecoveredAudienceExplanationStrategy(analysisDoc, slidesDoc, recoveredSlides);
    }
    const preferredDoc = slidesPreferredFields.has(fieldName) ? slidesDoc : analysisDoc;
    const fallbackDoc = preferredDoc === slidesDoc ? analysisDoc : slidesDoc;
    if (isPlainObject(preferredDoc) && hasOwn(preferredDoc, fieldName)) return preferredDoc[fieldName];
    if (isPlainObject(fallbackDoc) && hasOwn(fallbackDoc, fieldName)) return fallbackDoc[fieldName];
    return undefined;
  };
  const preferExactArtifactFields = (taskIsBeamer(payload) || taskIsPpt(payload)) && payload?.phase?.finalPhase === true;

  for (const fieldName of fieldNames) {
    if (
      !preferExactArtifactFields
      && isNonEmptyStructuredValue(next[fieldName])
      && !structuredCoverageValueHasUnresolvedStatus(next[fieldName])
    ) {
      continue;
    }
    const artifactValue = fieldFromArtifacts(fieldName);
    if (!isNonEmptyStructuredValue(artifactValue)) {
      continue;
    }
    next[fieldName] = deepCloneJson(artifactValue);
    changed = true;
  }

  const normalized = normalizeProgrammerResult({ content: next }, payload)?.content || next;
  return changed || normalized !== next ? normalized : content;
}

function equationCoverageKeysBySlide(slidesDoc) {
  const bySlide = new Map();
  const coverage = Array.isArray(slidesDoc?.equation_coverage) ? slidesDoc.equation_coverage : [];
  for (const entry of coverage) {
    if (!isPlainObject(entry)) continue;
    const status = normalizeCoverageStatus(entry.status || "covered") || "covered";
    if (coverageStatusIsUnresolved(status)) continue;
    const keys = equationKeysFromValues(extractEquationNumbersFromCoverageValue(
      entry.equation_numbers ?? entry.numbers ?? entry.equations ?? entry.source_label ?? entry.label ?? []
    ));
    if (keys.length === 0) continue;
    const slideIds = Array.isArray(entry.slide_ids)
      ? entry.slide_ids.map((item) => String(item || "").trim()).filter(Boolean)
      : [];
    for (const slideId of slideIds) {
      if (!bySlide.has(slideId)) bySlide.set(slideId, new Set());
      for (const key of keys) bySlide.get(slideId).add(key);
    }
  }
  return bySlide;
}

function visibleEquationKeysAnchoredOnSlide(slide, coverageKeysForSlide = new Set()) {
  const keys = new Set();
  const blocks = equationBlocksFromSlide(slide);
  for (const block of blocks) {
    const blockKeys = equationKeysFromValues(extractEquationNumbersFromCoverageValue([
      block?.label,
      block?.source_label,
      block?.equation_number,
      block?.equation_numbers,
      block?.number,
      block?.numbers,
    ]));
    for (const key of blockKeys) keys.add(key);
  }
  if (blocks.length > 0) {
    for (const key of coverageKeysForSlide) keys.add(key);
  }
  return keys;
}

function beamerSlidesReferenceLiteralEquationNumbers(slides, slidesDoc = null) {
  const errors = [];
  const coverageKeysBySlide = equationCoverageKeysBySlide(slidesDoc);
  for (const slide of Array.isArray(slides) ? slides : []) {
    if (!isPlainObject(slide)) continue;
    const slideId = slideIdFromPlan(slide) || String(slide?.title || "").trim() || "unknown_slide";
    const visibleText = slideVisibleTextFromPlan(slide);
    if (!visibleText) continue;
    const anchoredKeys = visibleEquationKeysAnchoredOnSlide(slide, coverageKeysBySlide.get(slideId));
    for (const match of visibleText.matchAll(/式\s*[（(]\s*(\d+[A-Za-z]?)\s*[)）]/g)) {
      const referencedKeys = equationKeysFromValues(extractEquationNumbersFromCoverageValue([`Eq. (${match[1]})`]));
      if (referencedKeys.length > 0 && referencedKeys.some((key) => anchoredKeys.has(key))) {
        continue;
      }
      errors.push(`${slideId} visible text still hard-codes a literal source-style equation reference such as '式 (60)'; plan a deck-local equation reference instead of copying the paper wording`);
      break;
    }
  }
  return errors;
}

function beamerMainTexReferenceDiagnostics(content, payload) {
  const errors = [];
  if (!taskIsBeamer(payload) || !isPlainObject(content) || !isPlainObject(content.artifact_paths)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  if (!isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) return errors;

  let tex = "";
  try {
    tex = fs.readFileSync(mainTexPath, "utf8");
  } catch {
    return errors;
  }

  if (/式\s*[（(]\s*\d+[A-Za-z]?\s*[)）]/.test(tex) && !/\\(?:eqref|ref)\{[^}]+\}/.test(tex)) {
    errors.push("main.tex still uses literal source-style equation references such as '式 (60)' without deck-local \\label/\\eqref references");
  }

  const equationNumbers = new Set();
  for (const match of tex.matchAll(/\\tag\{([^}]+)\}/g)) {
    const tagText = String(match[1] || "").trim();
    if (tagText) {
      equationNumbers.add(tagText);
    }
  }
  for (const match of tex.matchAll(/\\begin\{equation\}([\s\S]*?)\\end\{equation\}/g)) {
    const block = String(match[1] || "");
    const numberMatch = block.match(/\\tag\{([^}]+)\}/);
    if (numberMatch && String(numberMatch[1] || "").trim()) {
      equationNumbers.add(String(numberMatch[1]).trim());
    }
  }
  if (equationNumbers.size > 0 && !/\\(?:eqref|ref)\{[^}]+\}/.test(tex) && /式\s*[（(]\s*\d+[A-Za-z]?\s*[)）]/.test(tex)) {
    errors.push("main.tex contains tagged display equations but later prose still cites them with raw text instead of \\eqref/\\ref");
  }

  return errors;
}

function slideHasDefinitionCueForSymbol(slide, candidates) {
  const metadataSymbols = slideDefinitionMetadataSymbols(slide);
  if (metadataSymbols.some((item) => candidates.some((candidate) => canonicalizeSymbolToken(item) === canonicalizeSymbolToken(candidate)))) {
    return true;
  }
  const visibleText = slideVisibleTextFromPlan(slide);
  if (!visibleText) return false;
  const hasSymbol = candidates.some((candidate) => textContainsSymbolCandidate(candidate, visibleText));
  if (!hasSymbol) return false;
  return /定义|表示|记为|记作|其中|指的是|denotes|refers\s+to|stands\s+for|is\s+defined\s+as/i.test(visibleText);
}

function firstVisibleSlideIdForSymbol(slides, candidates) {
  for (const slide of Array.isArray(slides) ? slides : []) {
    const slideId = slideIdFromPlan(slide);
    if (!slideId) continue;
    const visibleText = slideVisibleTextFromPlan(slide);
    if (candidates.some((candidate) => textContainsSymbolCandidate(candidate, visibleText))) {
      return slideId;
    }
  }
  return "";
}

function notationEntryRepresentsSymbolFamily(entry) {
  const symbolText = String(entry?.symbol ?? entry?.term ?? entry?.notation ?? entry?.variable ?? entry?.abbreviation ?? "").trim();
  if (!symbolText) return false;
  return /[,;]| 及 | and |\/|带 .*下标|版本|变体|variants?/i.test(symbolText);
}

function isGenericDifferentialToken(token) {
  const value = String(token || "").trim();
  return /^d[A-Za-z]_\{?[ijk]\}?$/i.test(value);
}

function extractLikelyMathSymbolsFromEquationText(text) {
  const raw = String(text || "");
  const sanitized = raw
    .replace(/\\(?:label|ref|eqref|autoref|cref|Cref)\{[^}]*\}/g, " ")
    .replace(/\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}/g, " ");
  const tokens = new Set();
  for (const match of sanitized.matchAll(/\\partial\s*\\Omega/g)) tokens.add("\\partial\\Omega");
  for (const match of sanitized.matchAll(/\\Omega/g)) tokens.add("\\Omega");
  for (const match of sanitized.matchAll(/\\(?:theta|omega|alpha|beta|phi|nu|varepsilon|epsilon)(?:_[A-Za-z0-9]+)?/g)) tokens.add(match[0]);
  for (const match of sanitized.matchAll(/\b[a-zA-Z]+_[a-zA-Z0-9]+\b/g)) {
    const startIndex = Number(match.index || 0);
    if (startIndex > 0 && sanitized[startIndex - 1] === "\\") continue;
    tokens.add(match[0]);
  }
  for (const match of sanitized.matchAll(/\bg\([A-Za-z]\)/g)) tokens.add(match[0]);
  for (const match of sanitized.matchAll(/\b[BD]\b/g)) tokens.add(match[0]);
  const ignore = new Set([
    "\\alpha",
    "\\phi",
    "\\nu",
    "r_l",
    "z_l",
    "x_l",
    "\\theta_l",
  ]);
  return [...tokens].map(canonicalizeSymbolToken).filter((token) => token && !ignore.has(token) && !isGenericDifferentialToken(token));
}

function actualDeckCoverageDiagnostics(content, payload = null, options = {}) {
  const errors = [];
  if (!isPlainObject(content) || !isPlainObject(content.artifact_paths)) return errors;
  if (content.recovered_structured_placeholder) return errors;
  const preferRenderedDeck = options.preferRenderedDeck === true
    || (taskIsBeamer(payload) && (payload?.phase?.finalPhase === true || deckPhaseIndex(payload) >= 5));
  const analysisPath = resolveArtifactPathFromReport(content.artifact_paths, "analysis.json");
  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  const analysisDoc = cachedJsonArtifact(content, analysisPath);
  const slidesDoc = cachedJsonArtifact(content, slidesPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0) return errors;
  const slideMap = new Map(slides.map((slide) => [slideIdFromPlan(slide), slide]).filter(([slideId]) => slideId));
  const paragraphLedger = paragraphLedgerFromArtifacts(content, analysisDoc);
  let frameLookup = null;
  let frameWindows = null;
  if (isNonEmptyString(mainTexPath) && fs.existsSync(mainTexPath)) {
    frameLookup = cachedFrameLookup(content, mainTexPath);
    frameWindows = buildOrderedSlideFrameWindows(slides, frameLookup);
  }
  const equationFirstParagraphOrdinal = new Map();
  const phaseAllowsSkeletonEvidence = deckPhaseIndex(payload) <= 3;

  if (paragraphLedger.length === 0) {
    errors.push("analysis.json is missing paragraph_ledger for source-order and audience-facing paragraph summaries");
  } else {
    for (const entry of paragraphLedger) {
      if (!isPlainObject(entry)) {
        errors.push("paragraph_ledger contains a non-object entry");
        break;
      }
      if (!isNonEmptyString(entry.paragraph_id ?? entry.id)) {
        errors.push("paragraph_ledger entry is missing paragraph_id");
        break;
      }
      if (!isNonEmptyString(entry.section)) {
        errors.push("paragraph_ledger entry is missing section");
        break;
      }
      if (!isNonEmptyString(paragraphLedgerSummaryText(entry))) {
        errors.push("paragraph_ledger entry is missing summary_sentence");
        break;
      }
      const paragraphId = String(entry.paragraph_id ?? entry.id).trim();
      const paragraphOrdinal = paragraphOrdinalFromId(paragraphId);
      if (Number.isFinite(paragraphOrdinal) && paragraphOrdinal > 0) {
        const equationTags = safeArray(entry.equation_tags);
        for (const key of equationKeysFromValues(extractEquationNumbersFromCoverageValue(equationTags))) {
          const current = equationFirstParagraphOrdinal.get(key);
          if (!Number.isFinite(current) || paragraphOrdinal < current) {
            equationFirstParagraphOrdinal.set(key, paragraphOrdinal);
          }
        }
      }
    }
    if (taskIsBeamer(payload)) {
      errors.push(...paragraphLedgerLanguageDiagnostics(paragraphLedger));
    }
  }

  if (deckUsesFixedTotalDurationCap(analysisDoc, slidesDoc)) {
    if (!deckDeclaresNoHardTimeCap(content, analysisDoc, slidesDoc)) {
      errors.push("analysis/slides still encode a fixed total-duration cap without stating that the deck has no hard time limit");
    } else if (Number.isFinite(Number(analysisDoc?.target_minutes)) && Number(analysisDoc.target_minutes) > 0) {
      errors.push("analysis.json still uses numeric target_minutes even though Beamer decks should have no hard total-duration cap");
    }
  }

  let lastParagraphOrdinal = 0;
  for (const slide of slides) {
    if (!slideRequiresSourceParagraphMapping(slide)) continue;
    const slideId = slideIdFromPlan(slide) || "unknown_slide";
    const paragraphIds = sourceParagraphIdsFromSlide(slide);
    if (paragraphIds.length === 0) {
      errors.push(`${slideId} is missing source_paragraph_ids for source-order tracking`);
      continue;
    }
    const ordinals = paragraphIds.map(paragraphOrdinalFromId).filter(Number.isFinite);
    if (ordinals.length !== paragraphIds.length) {
      errors.push(`${slideId} has non-numeric source_paragraph_ids`);
      continue;
    }
    for (let index = 1; index < ordinals.length; index += 1) {
      if (ordinals[index] !== ordinals[index - 1] + 1) {
        errors.push(`${slideId} maps non-contiguous source paragraphs (${paragraphIds.join(", ")}); ordinary body slides must use one forward-moving contiguous span such as [p07] or [p07,p08]`);
        break;
      }
    }
    const minOrdinal = Math.min(...ordinals);
    const maxOrdinal = Math.max(...ordinals);
    if (lastParagraphOrdinal > 0 && minOrdinal < lastParagraphOrdinal) {
      errors.push(`${slideId} breaks source paragraph order by jumping backward from p${lastParagraphOrdinal} to p${minOrdinal}; only conclusion-preview / final-takeaway / QA / utility-appendix pages may intentionally revisit earlier paragraphs`);
    }
    lastParagraphOrdinal = Math.max(lastParagraphOrdinal, maxOrdinal);
  }

  if (frameLookup) {
    for (const slide of slides) {
      if (!slideRequiresSourceParagraphMapping(slide)) continue;
      const slideId = slideIdFromPlan(slide);
      if (!slideId) continue;
      const paragraphIds = sourceParagraphIdsFromSlide(slide);
      const ordinals = paragraphIds.map((value) => paragraphOrdinalFromId(value)).filter((value) => Number.isFinite(value) && value > 0);
      if (ordinals.length === 0) continue;
      const maxParagraphOrdinal = Math.max(...ordinals);
      const frame = findFrameForSlide(slide, frameLookup, { allowOrdinalFallback: false });
      if (!frame) continue;
      const renderedKeys = Array.from(frameTaggedEquationKeySet(frame));
      const forwardDriftKeys = renderedKeys.filter((key) => {
        const sourceOrdinal = equationFirstParagraphOrdinal.get(key);
        return Number.isFinite(sourceOrdinal) && sourceOrdinal > maxParagraphOrdinal;
      });
      if (forwardDriftKeys.length === 0) continue;
      const earliestForwardOrdinal = Math.min(...forwardDriftKeys
        .map((key) => equationFirstParagraphOrdinal.get(key))
        .filter((value) => Number.isFinite(value) && value > 0));
      errors.push(`main.tex frame ${slideId} renders tagged equation numbers ${forwardDriftKeys.join(", ")} before their source paragraphs; slide source_paragraph_ids stop at p${maxParagraphOrdinal} but those equations first appear from p${earliestForwardOrdinal}`);
    }
  }

  const equationCoverage = canonicalizeEquationCoverageEntries(
    Array.isArray(slidesDoc?.equation_coverage) && slidesDoc.equation_coverage.length > 0
      ? slidesDoc.equation_coverage
      : Array.isArray(content.equation_coverage) && content.equation_coverage.length > 0
        ? content.equation_coverage
        : Array.isArray(analysisDoc?.equation_coverage)
          ? analysisDoc.equation_coverage
          : []
  );
  errors.push(...sourceEquationCoverageCompletenessDiagnostics(content, payload, analysisDoc, equationCoverage));
  if (equationCoverage.length > 0) {
    const coveredNumbersBySlide = new Map();
    for (const entry of equationCoverage) {
      if (!isPlainObject(entry)) continue;
      const status = String(entry.status || "covered").trim().toLowerCase();
      if (!["covered", "partial", "covered_with_ocr_gap_note", "inline_integrated", "standalone_supplement"].includes(status)) continue;
      const label = String(entry.source_label ?? entry.label ?? "equation range").trim();
      const directNumbers = extractEquationNumbersFromCoverageValue(entry.equation_numbers ?? entry.numbers ?? entry.equations ?? []);
      const numbers = directNumbers.length > 0
        ? directNumbers
        : extractEquationNumbersFromCoverageValue(entry.source_label ?? entry.label ?? []);
      const slideIds = Array.isArray(entry.slide_ids) ? entry.slide_ids.map((item) => String(item || "").trim()).filter(Boolean) : [];
      const mappedSlides = slideIds.map((slideId) => slideMap.get(slideId)).filter(Boolean);
      if (["covered", "inline_integrated", "standalone_supplement"].includes(status) && slideIds.length === 0) {
        errors.push(`equation_coverage marks ${label} as ${status} but has no slide_ids`);
      }
      if (slideIds.length > 0 && mappedSlides.length !== slideIds.length) {
        errors.push(`equation_coverage references unknown slide ids for ${label}`);
      }
      if (mappedSlides.length === 0) continue;
      const mappedFrames = frameLookup
        ? mappedSlides.map((slide) => findFrameForSlide(slide, frameLookup, { allowOrdinalFallback: false })).filter(Boolean)
        : [];
      const renderedEquationBlockCount = mappedFrames.length > 0
        ? frameCollectionVisibleEquationCount(mappedFrames)
        : 0;
      const mappedSlidesExposeEquationBlocks = mappedSlides.some((slide) => equationBlocksFromSlide(slide).length > 0);
      const slideEquationBlockCount = mappedSlidesExposeEquationBlocks
        ? mappedSlides.reduce((sum, slide) => sum + equationBlocksFromSlide(slide).length, 0)
        : 0;
      const equationBlockCount = renderedEquationBlockCount > 0
        ? renderedEquationBlockCount
        : slideEquationBlockCount;
      const usingRenderedEquationEvidence = preferRenderedDeck && mappedFrames.length > 0;
      if ((status === "covered" || status === "inline_integrated") && equationBlockCount === 0) {
        errors.push(
          usingRenderedEquationEvidence
            ? `equation_coverage marks ${label} as ${status} but mapped main.tex frames contain no visible equation block`
            : `equation_coverage marks ${label} as ${status} but mapped slides contain no visible equation block`
        );
      }
      if ((mappedSlidesExposeEquationBlocks || renderedEquationBlockCount > 0) && (status === "covered" || status === "inline_integrated") && numbers.length >= 3 && equationBlockCount <= 1) {
        errors.push(
          usingRenderedEquationEvidence
            ? `equation_coverage maps ${label} to ${slideIds.join(", ")} but mapped main.tex frames collapse it into only ${equationBlockCount} visible equation block`
            : `equation_coverage collapses ${label} into a single representative equation block`
        );
      }
      if (status === "covered") {
        for (const slide of mappedSlides) {
          if (!slideRequiresSourceParagraphMapping(slide)) continue;
          const paragraphIds = sourceParagraphIdsFromSlide(slide);
          const ordinals = paragraphIds.map((value) => paragraphOrdinalFromId(value)).filter((value) => Number.isFinite(value) && value > 0);
          if (ordinals.length === 0) continue;
          const maxParagraphOrdinal = Math.max(...ordinals);
          const sourceEquationOrdinals = equationKeysFromValues(numbers)
            .map((key) => equationFirstParagraphOrdinal.get(key))
            .filter((value) => Number.isFinite(value) && value > 0);
          if (sourceEquationOrdinals.length === 0) continue;
          const earliestEquationParagraphOrdinal = Math.min(...sourceEquationOrdinals);
          if (maxParagraphOrdinal < earliestEquationParagraphOrdinal) {
            errors.push(`equation_coverage maps ${label} to ${slideIdFromPlan(slide)} but its source_paragraph_ids stop at p${maxParagraphOrdinal}, earlier than the source paragraph for those equations (from p${earliestEquationParagraphOrdinal})`);
          }
        }
      }
      if (mappedFrames.length > 0 && numbers.length > 0) {
        const coveredEquationKeys = new Set();
        for (const frame of mappedFrames) {
          for (const key of frameTaggedEquationKeySet(frame)) {
            coveredEquationKeys.add(key);
          }
        }
        const expectedKeys = equationKeysForCoverageEntry(entry, numbers);
        const hasAnyExpectedKey = expectedKeys.some((key) => coveredEquationKeys.has(key));
        if (!hasAnyExpectedKey) {
          errors.push(`equation_coverage maps ${label} to ${slideIds.join(", ")} but main.tex is missing tagged equation numbers ${expectedKeys.join(", ")}`);
        }
      }
      if ((!preferRenderedDeck || mappedFrames.length === 0) && mappedSlidesExposeEquationBlocks && status === "inline_integrated") {
        for (const slide of mappedSlides) {
          const blocks = slide.blocks || [];
          const hasExplanation = blocks.some((block) => {
            const type = String(block.type || "").toLowerCase();
            const text = String(block.text || block.content || block.explanation || "");
            return type === "paragraph" && text.length > 80 && /表明 | 显示 | 说明 | 意味着 | 反映 | 对应 | 刻画 | 描述/i.test(text);
          });
          if (!hasExplanation) {
            errors.push(`equation_coverage marks ${label} as inline_integrated on ${slideIdFromPlan(slide)} but the slide lacks explanation paragraph connecting the formula to its economic/probabilistic meaning`);
          }
        }
      }
      if ((!preferRenderedDeck || mappedFrames.length === 0) && mappedSlidesExposeEquationBlocks && status === "standalone_supplement") {
        for (const slide of mappedSlides) {
          const title = String(slide.title || "");
          if (/补充公式|supplement|appendix/i.test(title)) {
            const blocks = slide.blocks || [];
            const hasBridge = blocks.some((block) => {
              const text = String(block.text || block.content || "");
              return /承接 | 引导 | 下一页 | 上一页 | 回到 | 继续/i.test(text);
            });
            if (!hasBridge) {
              errors.push(`equation_coverage marks ${label} as standalone_supplement on ${slideIdFromPlan(slide)} but the slide lacks narrative bridge to adjacent slides`);
            }
          }
        }
      }
      for (const slideId of slideIds) {
        if (!coveredNumbersBySlide.has(slideId)) {
          coveredNumbersBySlide.set(slideId, []);
        }
        coveredNumbersBySlide.get(slideId).push(...equationKeysForCoverageEntry(entry, numbers));
      }
    }
    for (const [slideId, rawNumbers] of coveredNumbersBySlide.entries()) {
      const slide = slideMap.get(slideId);
      if (!slide) continue;
      const numbers = uniqueCanonicalEquationNumbers(rawNumbers);
      const hasOnlySemanticKeys = safeArray(rawNumbers).some((value) => !canonicalEquationNumberKey(value));
      const renderedEquationBlockCount = frameLookup
        ? frameCollectionVisibleEquationCount(framesForSlideId(slideId, frameWindows))
        : 0;
      const equationBlockCount = renderedEquationBlockCount > 0
        ? renderedEquationBlockCount
        : equationBlocksFromSlide(slide).length;
      if (equationBlockCount > 0 && numbers.length >= 3 && equationBlockCount <= 1) {
        errors.push(`equation_coverage maps ${formatEquationNumberRanges(numbers)} to ${slideId} but that slide contains only one visible equation block`);
      }
      const paragraphIds = sourceParagraphIdsFromSlide(slide);
      if (numbers.length >= 3 && paragraphIds.length === 0 && slideRequiresSourceParagraphMapping(slide)) {
        errors.push(`equation-heavy slide ${slideId} lacks source_paragraph_ids, so readers cannot trace the local prose around ${formatEquationNumberRanges(numbers)}`);
      }
      if (frameLookup) {
        const frame = findFrameForSlide(slide, frameLookup, { allowOrdinalFallback: false });
        if (frame && numbers.length > 0 && !hasOnlySemanticKeys && !frameContainsAllEquationKeys(frame, numbers)) {
          errors.push(`equation_coverage maps ${formatEquationNumberRanges(numbers)} to ${slideId} but the corresponding main.tex frame is missing one or more tagged equation numbers from that range`);
        }
      }
    }
  }

  const notationCoverage = Array.isArray(content.notation_coverage)
    ? content.notation_coverage
    : Array.isArray(slidesDoc?.notation_coverage)
      ? slidesDoc.notation_coverage
      : Array.isArray(analysisDoc?.notation_coverage)
        ? analysisDoc.notation_coverage
        : [];
  // Phase 3 lightweight: verify first_defined_slide_ids mention the symbol in slide plan text
  if (Array.isArray(notationCoverage) && notationCoverage.length > 0 && deckPhaseIndex(payload) === 3) {
    for (const entry of notationCoverage) {
      if (!isPlainObject(entry)) continue;
      const symbol = normalizeNotationSymbolText(entry.symbol || "");
      if (!symbol) continue;
      const firstDefinedSlideIds = Array.isArray(entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids)
        ? (entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids).map((item) => String(item || "").trim()).filter(Boolean)
        : [];
      const meaning = String(entry.meaning || "").trim();
      const candidates = symbolCandidatesFromNotationEntry(symbol);
      for (const slideId of firstDefinedSlideIds) {
        const slide = slideMap.get(slideId);
        if (!slide) continue;
        const slideText = slideVisibleTextFromPlan(slide);
        if (!slideText) continue;
        const matchedByCandidate = candidates.length > 0 && candidates.some((c) => textContainsSymbolCandidate(c, slideText));
        const matchedByMeaning = meaning.length > 0 && slideText.includes(meaning);
        if (!matchedByCandidate && !matchedByMeaning) {
          const meaningSnippet = meaning ? ` or its meaning "${meaning.length > 60 ? meaning.slice(0, 60) + "..." : meaning}"` : "";
          errors.push(`notation_coverage marks ${symbol} as first defined on ${slideId} but the visible slide text does not show this symbol${meaningSnippet}; fix first_defined_slide_ids or add the symbol to the slide plan`);
        }
      }
    }
  }
  const trackedSymbols = new Set();
  if (Array.isArray(notationCoverage)) {
    for (const entry of notationCoverage) {
      if (!isPlainObject(entry)) continue;
      for (const token of symbolCandidatesFromNotationEntry(entry.symbol ?? entry.term ?? entry.notation ?? entry.variable ?? entry.abbreviation)) {
        trackedSymbols.add(token);
      }
      const status = String(entry.status || "defined").trim().toLowerCase();
      if (!["defined", "covered", "partial"].includes(status)) continue;
      const symbol = String(entry.symbol ?? entry.term ?? entry.notation ?? entry.variable ?? entry.abbreviation ?? "").trim();
      if (!symbol || /UNKNOWN_RECOVERED_SYMBOL/i.test(symbol)) continue;
      const candidates = symbolCandidatesFromNotationEntry(symbol);
      const firstDefinedSlideIds = Array.isArray(entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids)
        ? (entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids).map((item) => String(item || "").trim()).filter(Boolean)
        : [];
      const usedSlideIds = Array.isArray(entry.used_slide_ids ?? entry.slide_ids)
        ? (entry.used_slide_ids ?? entry.slide_ids).map((item) => String(item || "").trim()).filter(Boolean)
        : [];
      const sourceParagraphIds = notationSourceParagraphIds(entry);
      const sourceQuote = notationSourceQuote(entry);
      const sourceDefinitionSummary = notationSourceDefinitionSummary(entry);
      const firstSlides = firstDefinedSlideIds.map((slideId) => slideMap.get(slideId)).filter(Boolean);
      const usedSlides = usedSlideIds.map((slideId) => slideMap.get(slideId)).filter(Boolean);
      const firstFrameGroups = frameLookup
        ? firstDefinedSlideIds.map((slideId) => framesForSlideId(slideId, frameWindows))
        : [];
      const usedFrameGroups = frameLookup
        ? usedSlideIds.map((slideId) => framesForSlideId(slideId, frameWindows))
        : [];
      const firstFramesFullyMatched = firstDefinedSlideIds.length > 0
        && firstFrameGroups.length === firstDefinedSlideIds.length
        && firstFrameGroups.every((group) => group.length > 0);
      const usedFramesFullyMatched = usedSlideIds.length > 0
        && usedFrameGroups.length === usedSlideIds.length
        && usedFrameGroups.every((group) => group.length > 0);
      const notationAllowsSkeletonEvidence = phaseAllowsSkeletonEvidence
        && firstSlides.length > 0
        && usedSlides.length > 0
        && firstSlides.every((slide) => equationBlocksFromSlide(slide).length === 0)
        && usedSlides.every((slide) => equationBlocksFromSlide(slide).length === 0);
      if (firstDefinedSlideIds.length > 0 && firstSlides.length !== firstDefinedSlideIds.length) {
        errors.push(`notation_coverage references unknown first_defined_slide_ids for ${symbol}`);
      }
      if (usedSlideIds.length > 0 && usedSlides.length !== usedSlideIds.length) {
        errors.push(`notation_coverage references unknown used_slide_ids for ${symbol}`);
      }
      if (sourceParagraphIds.length === 0) {
        errors.push(`notation_coverage is missing source_paragraph_ids for ${symbol}`);
      }
      if (!sourceQuote) {
        errors.push(`notation_coverage is missing source_quote for ${symbol}`);
      }
      if (!sourceDefinitionSummary) {
        errors.push(`notation_coverage is missing source_definition_summary for ${symbol}`);
      }
      if (typeof entry.defined_on_first_visible_use !== "boolean") {
        errors.push(`notation_coverage is missing defined_on_first_visible_use for ${symbol}`);
      } else if (entry.defined_on_first_visible_use !== true) {
        errors.push(`notation_coverage marks ${symbol} as not defined on first visible use`);
      }
      const enforceSlideLevelNotationVisibility = taskIsPpt(payload)
          || (taskIsBeamer(payload) && !preferRenderedDeck)
          || deckPhaseIndex(payload) >= 4;
      const firstSlidesExposeSymbolEvidence = enforceSlideLevelNotationVisibility
          ? firstSlides.length > 0
          : firstSlides.some((slide) => Array.isArray(slide?.defines_symbols) || Array.isArray(slide?.used_symbols) || equationBlocksFromSlide(slide).length > 0);
      const usedSlidesExposeSymbolEvidence = enforceSlideLevelNotationVisibility
          ? usedSlides.length > 0
          : usedSlides.some((slide) => Array.isArray(slide?.defines_symbols) || Array.isArray(slide?.used_symbols) || equationBlocksFromSlide(slide).length > 0);
      if (!notationAllowsSkeletonEvidence && firstFramesFullyMatched && preferRenderedDeck) {
        if (!frameCollectionContainsSymbolCandidate(firstFrameGroups.flat(), candidates)) {
          errors.push(`notation_coverage marks ${symbol} as first defined on ${firstDefinedSlideIds.join(", ")} but the corresponding main.tex frames do not visibly contain that symbol`);
        }
      } else if (!notationAllowsSkeletonEvidence && firstSlidesExposeSymbolEvidence && firstSlides.length > 0 && !firstSlides.some((slide) => candidates.some((candidate) => textContainsSymbolCandidate(candidate, slideVisibleTextFromPlan(slide))))) {
        errors.push(`notation_coverage marks ${symbol} as first defined on ${firstDefinedSlideIds.join(", ")} but the symbol is not visibly present there`);
      }
      if (!notationAllowsSkeletonEvidence && usedFramesFullyMatched && preferRenderedDeck) {
        if (!frameCollectionContainsSymbolCandidate(usedFrameGroups.flat(), candidates)) {
          errors.push(`notation_coverage marks ${symbol} as used on ${usedSlideIds.join(", ")} but the corresponding main.tex frames do not visibly contain that symbol`);
        }
      } else if (!notationAllowsSkeletonEvidence && usedSlidesExposeSymbolEvidence && usedSlides.length > 0 && !usedSlides.some((slide) => candidates.some((candidate) => textContainsSymbolCandidate(candidate, slideVisibleTextFromPlan(slide))))) {
        errors.push(`notation_coverage marks ${symbol} as used on ${usedSlideIds.join(", ")} but the symbol is not visibly present there`);
      }
    }
  }

  const likelyEquationSymbols = new Set();
  for (const slide of slides) {
    for (const block of equationBlocksFromSlide(slide)) {
      const sourceText = `${block.label || ""}\n${block.latex || ""}\n${block.explanation || ""}`;
      for (const token of extractLikelyMathSymbolsFromEquationText(sourceText)) {
        likelyEquationSymbols.add(token);
      }
    }
  }
  if (frameLookup) {
    for (const frame of frameLookup.frames || []) {
      for (const token of extractLikelyMathSymbolsFromEquationText(frame?.body || "")) {
        likelyEquationSymbols.add(token);
      }
    }
  }
  const untrackedSymbols = [...likelyEquationSymbols].filter((token) => token && !trackedSymbols.has(token));
  if (untrackedSymbols.length > 0 && !phaseAllowsSkeletonEvidence) {
    errors.push(`notation_coverage misses likely visible symbols from equation blocks: ${untrackedSymbols.slice(0, 12).join(", ")}`);
  }

  return errors;
}

function actualDeckTexCoverageDiagnostics(content, payload) {
  const errors = [];
  if (!taskIsBeamer(payload) || !isPlainObject(content) || !isPlainObject(content.artifact_paths)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  const slidesDoc = cachedJsonArtifact(content, slidesPath);
  const slides = slidesFromDoc(slidesDoc);
  const resolvedEquationCoverage = Array.isArray(slidesDoc?.equation_coverage) && slidesDoc.equation_coverage.length > 0
    ? slidesDoc.equation_coverage
    : content.equation_coverage;
  if (slides.length === 0 || !isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) return errors;

  const frames = cachedParsedMainTexFrames(content, mainTexPath);
  const frameLookup = cachedFrameLookup(content, mainTexPath);
  const frameWindows = buildOrderedSlideFrameWindows(slides, frameLookup);
  const slideMap = new Map(slides.map((slide) => [slideIdFromPlan(slide), slide]).filter(([slideId]) => slideId));

  const canonicalEquationCoverage = canonicalizeEquationCoverageEntries(resolvedEquationCoverage);
  if (Array.isArray(canonicalEquationCoverage)) {
    const texCoveredNumbersBySlide = new Map();
    for (const entry of canonicalEquationCoverage) {
      if (!isPlainObject(entry)) continue;
      const status = String(entry.status || "covered").trim().toLowerCase();
      if (!["covered", "covered_with_ocr_gap_note", "inline_integrated", "standalone_supplement"].includes(status)) continue;
      const label = String(entry.source_label ?? entry.label ?? "equation range").trim();
      const directNumbers = extractEquationNumbersFromCoverageValue(entry.equation_numbers ?? entry.numbers ?? entry.equations ?? []);
      const numbers = directNumbers.length > 0
        ? directNumbers
        : extractEquationNumbersFromCoverageValue(entry.source_label ?? entry.label ?? []);
      const slideIds = Array.isArray(entry.slide_ids) ? entry.slide_ids.map((item) => String(item || "").trim()).filter(Boolean) : [];
      const mappedFrameGroups = slideIds.map((slideId) => framesForSlideId(slideId, frameWindows)).filter((group) => group.length > 0);
      if (slideIds.length > 0 && mappedFrameGroups.length !== slideIds.length) {
        errors.push(`equation_coverage maps ${label} to slides that cannot be matched to main.tex frames`);
      }
      const mappedFrames = mappedFrameGroups.flat();
      if (mappedFrames.length === 0) continue;
      const displayEquationCount = frameCollectionVisibleEquationCount(mappedFrames);
      if (displayEquationCount === 0) {
        errors.push(`equation_coverage marks ${label} as ${status} but mapped main.tex frames contain no visible equation block`);
      }
      if (numbers.length >= 3 && displayEquationCount <= 1) {
        errors.push(`equation_coverage marks ${label} as covered but mapped main.tex frames collapse it into only ${displayEquationCount} visible equation block`);
      }
      if (slideIds.length === 1) {
        const [slideId] = slideIds;
        if (!texCoveredNumbersBySlide.has(slideId)) {
          texCoveredNumbersBySlide.set(slideId, []);
        }
        texCoveredNumbersBySlide.get(slideId).push(...equationKeysForCoverageEntry(entry, numbers));
      }
    }

    for (const [slideId, rawNumbers] of texCoveredNumbersBySlide.entries()) {
      const slide = slideMap.get(slideId);
      const mappedFrames = framesForSlideId(slideId, frameWindows);
      if (!slide || mappedFrames.length === 0) continue;
      const numbers = uniqueCanonicalEquationNumbers(rawNumbers);
      const displayEquationCount = frameCollectionVisibleEquationCount(mappedFrames);
      const hasOnlySemanticKeys = safeArray(rawNumbers).some((value) => !canonicalEquationNumberKey(value));
      if (numbers.length >= 3 && displayEquationCount <= 1) {
        errors.push(`equation_coverage maps ${formatEquationNumberRanges(numbers)} to ${slideId} but the corresponding main.tex frame contains only ${displayEquationCount} visible equation block`);
      }
      if (numbers.length > 0 && !hasOnlySemanticKeys && !frameCollectionContainsAllEquationKeys(mappedFrames, numbers)) {
        errors.push(`equation_coverage maps ${formatEquationNumberRanges(numbers)} to ${slideId} but the corresponding main.tex frame is missing one or more tagged equation numbers from that range`);
      }
    }
  }

  if (Array.isArray(content.notation_coverage)) {
    for (const entry of content.notation_coverage) {
      if (!isPlainObject(entry)) continue;
      const status = String(entry.status || "defined").trim().toLowerCase();
      if (!["defined", "covered", "partial"].includes(status)) continue;
      const symbol = String(entry.symbol ?? entry.term ?? entry.notation ?? entry.variable ?? entry.abbreviation ?? "").trim();
      const candidates = symbolCandidatesFromNotationEntry(symbol);
      if (candidates.length === 0) continue;
      const firstDefinedSlideIds = Array.isArray(entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids)
        ? (entry.first_defined_slide_ids ?? entry.definition_slide_ids ?? entry.introduced_slide_ids).map((item) => String(item || "").trim()).filter(Boolean)
        : [];
      const usedSlideIds = Array.isArray(entry.used_slide_ids ?? entry.slide_ids)
        ? (entry.used_slide_ids ?? entry.slide_ids).map((item) => String(item || "").trim()).filter(Boolean)
        : [];

      if (firstDefinedSlideIds.length > 0) {
        const matchingFirstFrameGroups = firstDefinedSlideIds.map((slideId) => framesForSlideId(slideId, frameWindows)).filter((group) => group.length > 0);
        if (matchingFirstFrameGroups.length !== firstDefinedSlideIds.length) {
          errors.push(`notation_coverage marks ${symbol} as first defined on slides that cannot all be matched to main.tex frames`);
        } else if (!frameCollectionContainsSymbolCandidate(matchingFirstFrameGroups.flat(), candidates)) {
          errors.push(`notation_coverage marks ${symbol} as first defined on ${firstDefinedSlideIds.join(", ")} but the corresponding main.tex frames do not visibly contain that symbol`);
        }
      }

      if (usedSlideIds.length > 0) {
        const matchingUsedFrameGroups = usedSlideIds.map((slideId) => framesForSlideId(slideId, frameWindows)).filter((group) => group.length > 0);
        if (matchingUsedFrameGroups.length !== usedSlideIds.length) {
          errors.push(`notation_coverage marks ${symbol} as used on slides that cannot all be matched to main.tex frames`);
        } else if (!frameCollectionContainsSymbolCandidate(matchingUsedFrameGroups.flat(), candidates)) {
          errors.push(`notation_coverage marks ${symbol} as used on ${usedSlideIds.join(", ")} but the corresponding main.tex frames do not visibly contain that symbol`);
        }
      }
    }
  }

  return errors;
}

function visibleArtifactLeakageDiagnostics(content, payload) {
  const errors = [];
  const beamerMode = taskIsBeamer(payload);
  const pptMode = taskIsPpt(payload);
  if (!(beamerMode || pptMode) || !isPlainObject(content) || !isPlainObject(content.artifact_paths)) {
    return errors;
  }

  const slidesJsonPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const slidesDoc = safeReadJsonArtifact(slidesJsonPath);
  const slides = Array.isArray(slidesDoc?.slides) ? slidesDoc.slides : [];

  if (slides.length > 0) {
    const commonSlideChecks = [
      {
        pattern: /(^|\W)核心信息[:：]?/,
        message: "slides.json visible slide text still exposes the internal scaffold label '核心信息'",
      },
      {
        pattern: /来源段落|source_paragraph_ids/,
        message: "slides.json visible slide text still exposes paragraph-tracking metadata",
      },
      {
        pattern: /这页负责|服务于未读论文听众/,
        message: "slides.json visible slide text still exposes planning-only audience/scaffold labels",
      },
      {
        pattern: /(^|\W)公式\s*A\d+/,
        message: "slides.json visible slide text still uses internal-looking appendix formula labels such as '公式 A1/A2'",
      },
    ];
    const slideChecks = [
      ...commonSlideChecks,
      ...(pptMode ? [
        {
          pattern: /原文锚点|关键读法|解释链条/,
          message: "slides.json visible slide text still contains rigid label-style wording such as '原文锚点/关键读法/解释链条'",
        },
        {
          pattern: /对未读者|你会看到|读这张图时|最重要的是|敢处理|诚实指出/,
          message: "slides.json visible slide text still contains audience-directed or subjective coaching wording",
        },
      ] : []),
    ];

    for (const slide of slides) {
      const slideText = slideVisibleTextFromPlan(slide);
      if (!slideText) continue;
      const slideId = slideIdFromPlan(slide) || String(slide?.title || "unknown_slide").trim() || "unknown_slide";
      for (const check of slideChecks) {
        if (check.pattern.test(slideText)) {
          errors.push(`${slideId}: ${check.message}`);
        }
      }
    }
  }

  if (!beamerMode) {
    return [...new Set(errors)];
  }

  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  if (!isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) {
    return [...new Set(errors)];
  }

  let tex = "";
  try {
    tex = fs.readFileSync(mainTexPath, "utf8");
  } catch {
    return [...new Set(errors)];
  }

  const leakageChecks = [
    {
      pattern: /\\textbf\{核心信息[:：]?\}|(^|\W)核心信息[:：]/,
      message: "main.tex still exposes the internal scaffold label '核心信息' in visible slide text",
    },
    {
      pattern: /来源段落|source_paragraph_ids/,
      message: "main.tex still exposes paragraph-tracking metadata in visible slide text",
    },
    {
      pattern: /这页负责|服务于未读论文听众/,
      message: "main.tex still exposes planning-only audience/scaffold labels in visible slide text",
    },
    {
      pattern: /\\begin\{block\}\{公式\s*A\d+[\s\S]*?\}|(^|\W)公式\s*A\d+/,
      message: "main.tex still uses internal-looking appendix formula block labels such as '公式 A1/A2' instead of natural academic wording like '式 (A1)'",
    },
  ];

  for (const check of leakageChecks) {
    if (check.pattern.test(tex)) {
      errors.push(check.message);
    }
  }

  return [...new Set(errors)];
}

function localBeamerPhase2PreflightDiagnostics(content, payload) {
  const errors = [];
  if (!isBeamerPhase2(payload) || !isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  if (!isNonEmptyStructuredValue(content.roadmap_page)) {
    errors.push("phase 2 preflight: roadmap_page must be populated before reviewer");
  }
  if (!isNonEmptyStructuredValue(content.conclusion_preview_page)) {
    errors.push("phase 2 preflight: conclusion_preview_page must be populated before reviewer");
  }
  if (!isNonEmptyStructuredValue(content.body_appendix_split)) {
    errors.push("phase 2 preflight: body_appendix_split must be populated before reviewer");
  }
  if (!isStructuredValueForPhase(content.numerical_study_pages, { allowEmptyArray: false })) {
    errors.push("phase 2 preflight: numerical_study_pages must be populated before reviewer");
  }
  if (!isStructuredValueForPhase(content.insight_pages, { allowEmptyArray: false })) {
    errors.push("phase 2 preflight: insight_pages must be populated before reviewer");
  }

  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const slidesDoc = safeReadJsonArtifact(slidesPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0) {
    errors.push("phase 2 preflight: slides.json is missing or contains no slides");
    return errors;
  }

  errors.push(...beamerSlidesReferenceLiteralEquationNumbers(slides, slidesDoc));
  errors.push(...denseFormulaOverlayDiagnostics(content, payload, { requireTexRealization: false }));

  return uniqueStrings([
    ...errors,
    ...beamerParagraphLedgerLanguageDiagnostics(content, payload),
  ]);
}

function localBeamerPhase3PreflightDiagnostics(content, payload) {
  const errors = [];
  if (!isBeamerPhase3(payload) || !isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  emitCoverageGroundingWarning(content, "equation_coverage");
  return uniqueStrings([
    ...errors,
    ...beamerParagraphLedgerLanguageDiagnostics(content, payload),
    ...equationCoverageDiagnosticsOnly(actualDeckCoverageDiagnostics(content, payload)),
    ...unresolvedCoverageSchemaDiagnostics(content, payload),
  ]);
}

function localBeamerPhase4PreflightDiagnostics(content, payload) {
  const errors = [];
  if (!isBeamerPhase4(payload) || !isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  emitCoverageGroundingWarning(content, "notation_coverage");
  return uniqueStrings([
    ...errors,
    ...beamerParagraphLedgerLanguageDiagnostics(content, payload),
    ...notationCoverageDiagnosticsOnly(actualDeckCoverageDiagnostics(content, payload)),
    ...unresolvedCoverageSchemaDiagnostics(content, payload),
  ]);
}

function localBeamerPhase5PreflightDiagnostics(content, payload) {
  return localBeamerRenderedDeckPreflightDiagnostics(content, payload, 5);
}

function localBeamerPhase6PreflightDiagnostics(content, payload) {
  return localBeamerRenderedDeckPreflightDiagnostics(content, payload, 6);
}

// Non-blocking stderr warning: checks grounded (non-planned/analysis_only) entries
// for missing source_paragraph_ids. Emits warning when >threshold fraction are ungrounded.
function emitCoverageGroundingWarning(content, fieldName, threshold = 0.1) {
  if (!isPlainObject(content)) return;
  const artifactPaths = isPlainObject(content.artifact_paths) ? content.artifact_paths : {};
  const slidesPath = resolveArtifactPathFromReport(artifactPaths, "slides.json");
  const analysisPath = resolveArtifactPathFromReport(artifactPaths, "analysis.json");
  const slidesDoc = safeReadJsonArtifact(slidesPath);
  const analysisDoc = safeReadJsonArtifact(analysisPath);

  const entries = [
    ...(isPlainObject(slidesDoc) && Array.isArray(slidesDoc[fieldName]) ? slidesDoc[fieldName] : []),
    ...(isPlainObject(analysisDoc) && Array.isArray(analysisDoc[fieldName]) ? analysisDoc[fieldName] : []),
  ];
  if (!Array.isArray(entries) || entries.length === 0) return;

  const groundable = entries.filter((e) => {
    if (!isPlainObject(e)) return false;
    if (["planned", "analysis_only"].includes(String(e.status || "").trim())) return false;
    return true;
  });
  if (groundable.length === 0) return;

  const grounded = groundable.filter(
    (e) => Array.isArray(e.source_paragraph_ids) && e.source_paragraph_ids.length > 0
  );
  const ungrounded = groundable.length - grounded.length;
  const ratio = ungrounded / groundable.length;

  if (ratio > threshold) {
    console.error(
      `[preflight] WARNING: ${ungrounded}/${groundable.length} (${(ratio * 100).toFixed(1)}%) grounded ${fieldName} entries lack source_paragraph_ids. Consider fixing artifacts before running pipeline.`
    );
  }
}

function compileLogContainsHardLatexError(text) {
  const raw = String(text || "");
  return /(^|\n)!\s+(?:LaTeX|Package|Class|pdfTeX|XeTeX|LuaTeX)\b[\s\S]{0,120}\bError\b/i.test(raw)
    || /(^|\n)!\s+Missing \$ inserted\./i.test(raw)
    || /(^|\n)!\s+Emergency stop\./i.test(raw)
    || /Fatal error occurred/i.test(raw)
    || /Latexmk:\s+Errors,\s+so I did not complete making targets/i.test(raw)
    || /Command for ['"]xelatex['"] gave return code\s+1/i.test(raw)
    || /\b(?:EXIT|COMPILE):(?:1|2|3|4|5|6|7|8|9|1\d|2\d)\b/.test(raw);
}

function beamerCompileLogCandidates(bundleDir) {
  if (!isNonEmptyString(bundleDir) || !fs.existsSync(bundleDir)) return [];
  let names = [];
  try {
    names = fs.readdirSync(bundleDir);
  } catch {
    return [];
  }
  return names
    .filter((name) => /^(?:compile\.run.*\.log|main\.log)$/i.test(String(name || "")))
    .map((name) => path.join(bundleDir, name))
    .filter((candidate) => {
      try {
        return fs.statSync(candidate).isFile();
      } catch {
        return false;
      }
    })
    .sort((a, b) => {
      try {
        return fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs;
      } catch {
        return 0;
      }
    });
}

function localBeamerCompileFreshnessDiagnostics(content, phaseIndex) {
  const errors = [];
  const mainTexPath = resolveArtifactPathFromReport(content?.artifact_paths, "main.tex");
  const mainPdfPath = resolveArtifactPathFromReport(content?.artifact_paths, "main.pdf");
  if (!isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath) || !isNonEmptyString(mainPdfPath) || !fs.existsSync(mainPdfPath)) {
    return errors;
  }
  let texStat = null;
  let pdfStat = null;
  try {
    texStat = fs.statSync(mainTexPath);
    pdfStat = fs.statSync(mainPdfPath);
  } catch {
    return errors;
  }
  const skewMs = 1000;
  if (pdfStat.mtimeMs + skewMs < texStat.mtimeMs) {
    errors.push(`phase ${phaseIndex} preflight: main.pdf is older than main.tex; rerun LaTeX after the latest main.tex changes before reviewer`);
  }
  const bundleDir = path.dirname(mainTexPath);
  for (const logPath of beamerCompileLogCandidates(bundleDir)) {
    let logStat = null;
    try {
      logStat = fs.statSync(logPath);
    } catch {
      continue;
    }
    if (logStat.mtimeMs <= pdfStat.mtimeMs + skewMs) continue;
    let logText = "";
    try {
      logText = fs.readFileSync(logPath, "utf8");
    } catch {
      continue;
    }
    if (compileLogContainsHardLatexError(logText)) {
      errors.push(`phase ${phaseIndex} preflight: ${path.basename(logPath)} contains a hard LaTeX error newer than main.pdf; rerun LaTeX successfully before reviewer`);
      break;
    }
  }
  return errors;
}

function localBeamerRenderedDeckPreflightDiagnostics(content, payload, phaseIndex, options = {}) {
  const errors = [];
  if (!isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;
  if (Number(phaseIndex) === 5 && !isBeamerPhase5(payload)) return errors;
  if (Number(phaseIndex) === 6 && !isBeamerPhase6(payload)) return errors;
  const skipResolvedCoverageSchema = options.skipResolvedCoverageSchema === true;

  const mainTexPath = resolveArtifactPathFromReport(content.artifact_paths, "main.tex");
  if (!isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) {
    errors.push(`phase ${phaseIndex} preflight: main.tex must exist before reviewer`);
  }
  const mainPdfPath = resolveArtifactPathFromReport(content.artifact_paths, "main.pdf");
  if (!isNonEmptyString(mainPdfPath) || !fs.existsSync(mainPdfPath)) {
    errors.push(`phase ${phaseIndex} preflight: main.pdf must exist before reviewer`);
  }

  return uniqueStrings([
    ...errors,
    ...localBeamerCompileFreshnessDiagnostics(content, phaseIndex),
    ...actualDeckStructureAlignmentDiagnostics(content, payload),
    ...actualDeckCoverageDiagnostics(content, payload),
    ...actualDeckRenderFidelityDiagnostics(content, payload),
    ...visibleArtifactLeakageDiagnostics(content, payload),
    ...beamerMainTexReferenceDiagnostics(content, payload),
    ...(skipResolvedCoverageSchema ? [] : unresolvedCoverageSchemaDiagnostics(content, payload)),
  ]);
}

function localPptPhase2PreflightDiagnostics(content, payload) {
  const errors = [];
  if (!isPptPhase2(payload) || !isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  if (!isNonEmptyStructuredValue(content.roadmap_page)) {
    errors.push("phase 2 preflight: roadmap_page must be populated before reviewer");
  }
  if (!isNonEmptyStructuredValue(content.conclusion_preview_page)) {
    errors.push("phase 2 preflight: conclusion_preview_page must be populated before reviewer");
  }
  if (!isNonEmptyStructuredValue(content.body_appendix_split)) {
    errors.push("phase 2 preflight: body_appendix_split must be populated before reviewer");
  }
  if (!isStructuredValueForPhase(content.numerical_study_pages, { allowEmptyArray: false })) {
    errors.push("phase 2 preflight: numerical_study_pages must be populated before reviewer");
  }
  if (!isStructuredValueForPhase(content.insight_pages, { allowEmptyArray: false })) {
    errors.push("phase 2 preflight: insight_pages must be populated before reviewer");
  }

  const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
  const slidesDoc = safeReadJsonArtifact(slidesPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0) {
    errors.push("phase 2 preflight: slides.json is missing or contains no slides");
    return errors;
  }

  errors.push(...beamerSlidesReferenceLiteralEquationNumbers(slides, slidesDoc));

  return uniqueStrings(errors);
}

function localPptPhase3PreflightDiagnostics(content, payload) {
  const errors = [];
  if (!isPptPhase3(payload) || !isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  return uniqueStrings([
    ...errors,
    ...equationCoverageDiagnosticsOnly(actualDeckCoverageDiagnostics(content, payload)),
    ...unresolvedCoverageSchemaDiagnostics(content, payload),
  ]);
}

function localPptPhase4PreflightDiagnostics(content, payload) {
  const errors = [];
  if (!isPptPhase4(payload) || !isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;

  return uniqueStrings([
    ...errors,
    ...notationCoverageDiagnosticsOnly(actualDeckCoverageDiagnostics(content, payload)),
    ...unresolvedCoverageSchemaDiagnostics(content, payload),
  ]);
}

function pptxValidationReportDiagnostics(content, phaseIndex) {
  const errors = [];
  const validationPath = resolveArtifactPathFromReport(content?.artifact_paths, "pptx_validation.json");
  if (!isNonEmptyString(validationPath) || !fs.existsSync(validationPath)) {
    errors.push(`phase ${phaseIndex} preflight: pptx_validation.json must exist before reviewer`);
    return errors;
  }
  const report = safeReadJsonArtifact(validationPath);
  if (!isPlainObject(report)) {
    errors.push(`phase ${phaseIndex} preflight: pptx_validation.json is not readable JSON`);
    return errors;
  }
  const fatalIssues = Array.isArray(report.issues)
    ? report.issues.filter((issue) => String(issue?.level || "").trim().toLowerCase() === "fatal")
    : [];
  const fatalCount = Number(report.fatal_count ?? report.error_count ?? 0);
  if (report.ok === false || fatalIssues.length > 0 || (Number.isFinite(fatalCount) && fatalCount > 0)) {
    errors.push(`phase ${phaseIndex} preflight: pptx_validation.json reports fatal validation failures`);
  }
  return errors;
}

function localPptRenderedDeckPreflightDiagnostics(content, payload, phaseIndex, options = {}) {
  const errors = [];
  if (!isPlainObject(content)) return errors;
  if (content.recovered_structured_placeholder) return errors;
  if (Number(phaseIndex) === 5 && !isPptPhase5(payload)) return errors;
  if (Number(phaseIndex) === 6 && !isPptPhase6(payload)) return errors;
  const skipResolvedCoverageSchema = options.skipResolvedCoverageSchema === true;

  const mainPptxPath = resolveArtifactPathFromReport(content.artifact_paths, "main.pptx");
  if (!isNonEmptyString(mainPptxPath) || !fs.existsSync(mainPptxPath)) {
    errors.push(`phase ${phaseIndex} preflight: main.pptx must exist before reviewer`);
  }

  return uniqueStrings([
    ...errors,
    ...pptxValidationReportDiagnostics(content, phaseIndex),
    ...actualDeckCoverageDiagnostics(content, payload),
    ...visibleArtifactLeakageDiagnostics(content, payload),
    ...(skipResolvedCoverageSchema ? [] : unresolvedCoverageSchemaDiagnostics(content, payload)),
  ]);
}

function localPptPhase5PreflightDiagnostics(content, payload) {
  return localPptRenderedDeckPreflightDiagnostics(content, payload, 5);
}

function localPptPhase6PreflightDiagnostics(content, payload) {
  return localPptRenderedDeckPreflightDiagnostics(content, payload, 6);
}

function localProgrammerPreflightDiagnostics(content, payload) {
  if (isBeamerPhase2(payload)) {
    return localBeamerPhase2PreflightDiagnostics(content, payload);
  }
  if (isBeamerPhase3(payload)) {
    return localBeamerPhase3PreflightDiagnostics(content, payload);
  }
  if (isBeamerPhase4(payload)) {
    return localBeamerPhase4PreflightDiagnostics(content, payload);
  }
  if (isBeamerPhase5(payload)) {
    return localBeamerPhase5PreflightDiagnostics(content, payload);
  }
  if (isBeamerPhase6(payload)) {
    return localBeamerPhase6PreflightDiagnostics(content, payload);
  }
  if (isPptPhase2(payload)) {
    return localPptPhase2PreflightDiagnostics(content, payload);
  }
  if (isPptPhase3(payload)) {
    return localPptPhase3PreflightDiagnostics(content, payload);
  }
  if (isPptPhase4(payload)) {
    return localPptPhase4PreflightDiagnostics(content, payload);
  }
  if (isPptPhase5(payload)) {
    return localPptPhase5PreflightDiagnostics(content, payload);
  }
  if (isPptPhase6(payload)) {
    return localPptPhase6PreflightDiagnostics(content, payload);
  }
  return [];
}

function validateProgrammerContentWithLocalPreflight(content, payload) {
  const validationContent = materializeArtifactBackedProgrammerContentForValidation(content, payload);
  const structuralErrors = validateProgrammerContentSchema(validationContent, payload);
  if (structuralErrors.length > 0) {
    return structuralErrors;
  }
  return localProgrammerPreflightDiagnostics(validationContent, payload);
}

function deckPhaseMetadataForValidation(phaseIndex, mode = "beamer") {
  const normalizedMode = String(mode || "beamer").trim().toLowerCase();
  const renderedArtifacts = normalizedMode === "ppt"
    ? ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json"]
    : ["analysis.json", "slides.json", "main.tex", "main.pdf"];
  const phaseFiveTitle = normalizedMode === "ppt" ? "ppt_render_and_structural_repair" : "compile_and_structural_repair";
  const phaseMap = {
    2: { title: "slides outline / skeleton", name: "slides_outline_skeleton", requiredArtifacts: ["analysis.json", "slides.json"] },
    3: { title: "equation coverage", name: "equation_coverage", requiredArtifacts: ["analysis.json", "slides.json"] },
    4: { title: "notation / consistency", name: "notation_consistency", requiredArtifacts: ["analysis.json", "slides.json"] },
    5: { title: phaseFiveTitle, name: "compile_and_structural_repair", requiredArtifacts: renderedArtifacts },
    6: { title: "review_and_auto_rework", name: "review_and_auto_rework", requiredArtifacts: renderedArtifacts },
  };
  const phase = phaseMap[phaseIndex];
  if (!phase) return null;
  return {
    index: phaseIndex,
    total: 7,
    title: phase.title,
    name: phase.name,
    requiredArtifacts: phase.requiredArtifacts,
    finalPhase: false,
  };
}

function beamerPhaseMetadataForValidation(phaseIndex) {
  return deckPhaseMetadataForValidation(phaseIndex, "beamer");
}

function parseValidatePhaseCliArgs(args) {
  const options = {
    mode: "beamer",
  };
  for (let argIndex = 0; argIndex < args.length; argIndex += 1) {
    const arg = args[argIndex];
    const readNextValue = () => {
      const nextValue = args[argIndex + 1];
      if (!isNonEmptyString(nextValue) || String(nextValue).startsWith("--")) {
        throw new Error(`missing value for ${arg}`);
      }
      argIndex += 1;
      return nextValue;
    };

    if (arg === "--help" || arg === "-h") {
      options.help = true;
    } else if (arg === "--phase") {
      options.phase = Number(readNextValue());
    } else if (arg === "--mode") {
      options.mode = String(readNextValue()).trim().toLowerCase();
    } else if (arg === "--artifact-dir" || arg === "--bundle-dir" || arg === "--output-dir") {
      options.artifactDir = readNextValue();
    } else if (arg === "--analysis" || arg === "--analysis-json") {
      options.analysisJson = readNextValue();
    } else if (arg === "--slides" || arg === "--slides-json") {
      options.slidesJson = readNextValue();
    } else if (arg === "--main-tex") {
      options.mainTex = readNextValue();
    } else if (arg === "--main-pdf") {
      options.mainPdf = readNextValue();
    } else if (arg === "--main-pptx") {
      options.mainPptx = readNextValue();
    } else if (arg === "--pptx-validation" || arg === "--pptx-validation-json") {
      options.pptxValidation = readNextValue();
    } else if (arg === "--task") {
      options.task = readNextValue();
    } else {
      throw new Error(`unknown validate-phase option: ${arg}`);
    }
  }
  return options;
}

function validatePhaseCliUsage() {
  return [
    "Usage:",
    `  ${process.execPath} ${__filename} validate-phase --phase <2-6> --mode beamer|ppt --artifact-dir <bundle-dir>`,
    "",
    "Optional explicit artifact overrides:",
    "  --analysis-json <path> --slides-json <path> --main-tex <path> --main-pdf <path>",
    "  --main-pptx <path> --pptx-validation-json <path>",
  ].join("\n");
}

function artifactPathsForValidatePhase(options) {
  const artifactDir = path.resolve(String(options.artifactDir || "").trim());
  const phaseIndex = Number(options.phase || 0);
  const mode = String(options.mode || "beamer").trim().toLowerCase();
  const artifactPaths = {
    output_directory: artifactDir,
    "analysis.json": path.resolve(options.analysisJson || path.join(artifactDir, "analysis.json")),
    "slides.json": path.resolve(options.slidesJson || path.join(artifactDir, "slides.json")),
  };
  if (mode === "ppt") {
    const defaultMainPptx = path.join(artifactDir, "main.pptx");
    const defaultPptxValidation = path.join(artifactDir, "pptx_validation.json");
    if (options.mainPptx || phaseIndex >= 5 || fs.existsSync(defaultMainPptx)) {
      artifactPaths["main.pptx"] = path.resolve(options.mainPptx || defaultMainPptx);
    }
    if (options.pptxValidation || phaseIndex >= 5 || fs.existsSync(defaultPptxValidation)) {
      artifactPaths["pptx_validation.json"] = path.resolve(options.pptxValidation || defaultPptxValidation);
    }
  } else {
    const defaultMainTex = path.join(artifactDir, "main.tex");
    const defaultMainPdf = path.join(artifactDir, "main.pdf");
    if (options.mainTex || phaseIndex >= 5 || fs.existsSync(defaultMainTex)) {
      artifactPaths["main.tex"] = path.resolve(options.mainTex || defaultMainTex);
    }
    if (options.mainPdf || phaseIndex >= 5 || fs.existsSync(defaultMainPdf)) {
      artifactPaths["main.pdf"] = path.resolve(options.mainPdf || defaultMainPdf);
    }
  }
  return artifactPaths;
}

function buildValidatePhasePayload(options) {
  const phaseIndex = Number(options.phase || 0);
  const mode = String(options.mode || "beamer").trim().toLowerCase();
  const phase = deckPhaseMetadataForValidation(phaseIndex, mode);
  if (!phase) {
    throw new Error("validate-phase currently supports deck phases 2-6 only");
  }
  if (!["beamer", "ppt"].includes(mode)) {
    throw new Error("validate-phase supports --mode beamer or --mode ppt");
  }
  if (!isNonEmptyString(options.artifactDir)) {
    throw new Error("validate-phase requires --artifact-dir <bundle-dir>");
  }

  return {
    task: options.task || (mode === "ppt" ? "/ppt local artifact validation" : "/beamer local artifact validation"),
    phase,
    round: 1,
    execution_approved: true,
  };
}

function buildValidatePhaseContent(options) {
  const phaseIndex = Number(options.phase || 0);
  const mode = String(options.mode || "beamer").trim().toLowerCase();
  const modeLabel = mode === "ppt" ? "PPT" : "Beamer";
  return {
    summary: `Local ${modeLabel} phase ${phaseIndex} artifact validation.`,
    answer: "Artifacts are validated with the same local preflight used by the programmer gate.",
    checklist: [`run validate-phase for ${modeLabel} phase ${phaseIndex}`],
    changed: false,
    notes: `validator=validateProgrammerContentWithLocalPreflight artifact_dir=${path.resolve(String(options.artifactDir || "").trim())}`,
    ready_for_review: false,
    artifact_paths: artifactPathsForValidatePhase(options),
  };
}

function runValidatePhaseCli(args) {
  let options = {};
  try {
    options = parseValidatePhaseCliArgs(args);
    if (options.help) {
      return {
        exitCode: 0,
        payload: {
          ok: true,
          usage: validatePhaseCliUsage(),
        },
      };
    }
    const payload = buildValidatePhasePayload(options);
    const content = buildValidatePhaseContent(options);
    const errors = validateProgrammerContentWithLocalPreflight(content, payload);
    return {
      exitCode: errors.length === 0 ? 0 : 1,
      payload: {
        ok: errors.length === 0,
        mode: options.mode,
        phase: payload.phase,
        artifact_dir: path.resolve(String(options.artifactDir || "").trim()),
        artifact_paths: content.artifact_paths,
        validator: "validateProgrammerContentWithLocalPreflight",
        errors,
      },
    };
  } catch (error) {
    return {
      exitCode: 2,
      payload: {
        ok: false,
        usage: validatePhaseCliUsage(),
        errors: [error?.message || String(error)],
      },
    };
  }
}

function finalPhaseRecoveryBlockingDiagnostics(content, payload) {
  const errors = [];
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return errors;
  if (!isPlainObject(content)) return errors;
  if (content.ready_for_review !== true) return errors;

  const phase = payload?.phase;
  if (phase && phase.finalPhase === false) return errors;

  const notesText = normalizeStructuredNotesToString(content.notes || "");
  const answerText = String(content.answer || "").trim();
  if (content.recovery_not_final_deliverable === true || /recovery_not_final_deliverable:\s*true/i.test(notesText)) {
    errors.push("final deliverable still identifies itself as a recovery-only non-final result");
  }
  if (/恢复快照|恢复态|可用于下一轮|阶段性交付/.test(answerText)) {
    errors.push("final deliverable answer still reads like a recovery/stage checkpoint instead of a final acceptance summary");
  }

  const blockedFieldNames = [
    "figure_coverage",
    "table_coverage",
    "formal_statement_inventory",
    "roadmap_page",
    "conclusion_preview_page",
    "body_appendix_split",
    "timing_plan",
    "overlay_strategy",
    "numerical_study_pages",
    "insight_pages",
    "audience_explanation_strategy",
  ];
  for (const fieldName of blockedFieldNames) {
    const value = content[fieldName];
    if (structuredCoverageValueHasUnresolvedStatus(value)) {
      errors.push(`${fieldName} remains ${String(value.status || "").trim().toLowerCase()} in a ready_for_review=true final deliverable`);
    }
  }

  if (Array.isArray(content.equation_coverage)) {
    const blockedEquations = content.equation_coverage.filter((entry) => !isPlainObject(entry) || coverageStatusIsUnresolved(entry.status) || safeArray(entry.slide_ids).length === 0);
    if (blockedEquations.length > 0) {
      errors.push(`equation_coverage still has ${blockedEquations.length} blocked/partial/unmapped entries in a ready_for_review=true final deliverable`);
    }
  }

  if (Array.isArray(content.notation_coverage)) {
    const blockedNotation = content.notation_coverage.filter((entry) => !isPlainObject(entry) || coverageStatusIsUnresolved(entry.status) || safeArray(entry.first_defined_slide_ids).length === 0 || safeArray(entry.used_slide_ids).length === 0 || entry.defined_on_first_visible_use !== true);
    if (blockedNotation.length > 0) {
      errors.push(`notation_coverage still has ${blockedNotation.length} blocked/partial/unmapped entries in a ready_for_review=true final deliverable`);
    }
  }

  return errors;
}

function unresolvedCoverageSchemaDiagnostics(content, payload) {
  const errors = [];
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return errors;
  if (!isPlainObject(content)) return errors;
  const phaseIndex = deckPhaseIndex(payload);
  if (deckPhaseRequiresResolvedEquationCoverage(payload) && Array.isArray(content.equation_coverage)) {
    const unresolvedEquations = content.equation_coverage.filter((entry) =>
      !isPlainObject(entry) || coverageStatusIsUnresolved(entry.status)
    );
    if (unresolvedEquations.length > 0) {
      errors.push(`equation_coverage still has ${unresolvedEquations.length} planning/blocker entries after the equation-coverage phase gate`);
    }
  }

  if (deckPhaseRequiresResolvedNotationCoverage(payload) && Array.isArray(content.notation_coverage)) {
    const unresolvedNotation = content.notation_coverage.filter((entry) =>
      !isPlainObject(entry) || coverageStatusIsUnresolved(entry.status)
    );
    if (unresolvedNotation.length > 0) {
      errors.push(`notation_coverage still has ${unresolvedNotation.length} planning/blocker entries after the notation/consistency phase gate`);
    }
  }

  if (phaseIndex >= 5 || payload?.phase?.finalPhase === true) {
    for (const fieldName of [
      "figure_coverage",
      "table_coverage",
      "formal_statement_inventory",
      "roadmap_page",
      "conclusion_preview_page",
      "body_appendix_split",
      "timing_plan",
      "overlay_strategy",
      "numerical_study_pages",
      "insight_pages",
      "audience_explanation_strategy",
    ]) {
      if (structuredCoverageValueHasUnresolvedStatus(content[fieldName])) {
        errors.push(`${fieldName} still contains planned/blocker entries after the rendered-deck phase gate`);
      }
    }
  }

  return errors;
}

function phaseAllowsPlannedStructuredDeliverable(payload) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  return Boolean(phase && phase.finalPhase === false && deckPhaseIndex(payload) === 1);
}

function phaseAllowsArtifactRecovery(payload) {
  const phase = payload?.phase;
  if (!phase) return true;
  return phase.finalPhase === true || deckPhaseIndex(payload) >= 2;
}

function isStructuredValueForPhase(value, options = {}) {
  const allowEmptyArray = options.allowEmptyArray === true;
  if (isNonEmptyString(value)) return true;
  if (Array.isArray(value)) return allowEmptyArray ? true : value.length > 0;
  if (isPlainObject(value)) return Object.keys(value).length > 0;
  return false;
}

function validateProgrammerContentSchema(content, payload, options = {}) {
  const errors = [];
  const includeSemanticChecks = options.includeSemanticChecks === true;
  if (!isPlainObject(content)) {
    return ["programmer content must be a JSON object"];
  }

  const baseFields = [
    ["summary", (value) => isNonEmptyString(value), "must be a non-empty string"],
    ["answer", (value) => isNonEmptyString(value), "must be a non-empty string"],
    ["checklist", (value) => Array.isArray(value), "must be an array"],
    ["changed", (value) => typeof value === "boolean", "must be a boolean"],
    ["notes", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["ready_for_review", (value) => typeof value === "boolean", "must be a boolean"],
  ];

  for (const [key, predicate, message] of baseFields) {
    if (!hasOwn(content, key)) {
      errors.push(`missing required field: ${key}`);
      continue;
    }
    if (!predicate(content[key])) {
      errors.push(`invalid required field ${key}: ${message}`);
    }
  }

  const beamerOrPptMode = taskIsBeamer(payload) || taskIsPpt(payload);
  if (!beamerOrPptMode) {
    return errors;
  }

  const phaseIndex = deckPhaseIndex(payload);
  const allowPlannedEquationCoverage = deckPhaseAllowsPlannedEquationCoverage(payload);
  const allowPlannedNotationCoverage = deckPhaseAllowsPlannedNotationCoverage(payload);
  const allowPlannedStructuredDeliverable = phaseAllowsPlannedStructuredDeliverable(payload);
  const structuredRequirements = [
    ["artifact_paths", (value) => isPlainObject(value), "must be an object mapping artifact names to paths"],
    ["figure_coverage", (value) => isStructuredValueForPhase(value, { allowEmptyArray: allowPlannedStructuredDeliverable }), allowPlannedStructuredDeliverable ? "must be a structured string/array/object (empty arrays allowed before final review)" : "must be a non-empty string/array/object"],
    ["table_coverage", (value) => isStructuredValueForPhase(value, { allowEmptyArray: allowPlannedStructuredDeliverable }), allowPlannedStructuredDeliverable ? "must be a structured string/array/object (empty arrays allowed before final review)" : "must be a non-empty string/array/object"],
    ["equation_coverage", (value) => isStructuredEquationCoverage(value, { allowPlanned: allowPlannedEquationCoverage }), allowPlannedEquationCoverage ? "must be a non-empty array of equation mapping objects; outline/skeleton-phase entries may use status=planned/analysis_only with unresolved slide_ids, while later phases must convert them into concrete slide mappings" : "must be a non-empty array of equation mapping objects with source_label, equation_numbers, slide_ids, status, and notes"],
    ...(phaseIndex >= 4 ? [["notation_coverage", (value) => isStructuredNotationCoverage(value, { allowPlanned: allowPlannedNotationCoverage }), "must be a non-empty array of notation mapping objects with symbol, meaning, first_defined_slide_ids, used_slide_ids, source_paragraph_ids, source_quote, source_definition_summary, defined_on_first_visible_use, status, and notes"]] : []),
    ["formal_statement_inventory", (value) => isStructuredValueForPhase(value, { allowEmptyArray: allowPlannedStructuredDeliverable }), allowPlannedStructuredDeliverable ? "must be a structured string/array/object (empty arrays allowed before final review)" : "must be a non-empty string/array/object"],
    ["paragraph_ledger", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["roadmap_page", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["conclusion_preview_page", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["body_appendix_split", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["timing_plan", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["overlay_strategy", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
    ["numerical_study_pages", (value) => isStructuredValueForPhase(value, { allowEmptyArray: allowPlannedStructuredDeliverable }), allowPlannedStructuredDeliverable ? "must be a structured string/array/object (empty arrays allowed before final review)" : "must be a non-empty string/array/object"],
    ["insight_pages", (value) => isStructuredValueForPhase(value, { allowEmptyArray: allowPlannedStructuredDeliverable }), allowPlannedStructuredDeliverable ? "must be a structured string/array/object (empty arrays allowed before final review)" : "must be a non-empty string/array/object"],
    ["audience_explanation_strategy", (value) => isNonEmptyStructuredValue(value), "must be a non-empty string/array/object"],
  ];

  for (const [key, predicate, message] of structuredRequirements) {
    if (!hasOwn(content, key)) {
      errors.push(`missing required deliverable field: ${key}`);
      continue;
    }
    if (!predicate(content[key])) {
      errors.push(`invalid required deliverable field ${key}: ${message}`);
    }
  }

  errors.push(...validateArtifactPathBundleConsistency(payload, content));

  if (!includeSemanticChecks) {
    return errors;
  }

  errors.push(...actualDeckStructureAlignmentDiagnostics(content, payload));
  errors.push(...actualDeckCoverageDiagnostics(content, payload));
  errors.push(...actualDeckRenderFidelityDiagnostics(content, payload));
  errors.push(...actualDeckTexCoverageDiagnostics(content, payload));
  errors.push(...visibleArtifactLeakageDiagnostics(content, payload));
  errors.push(...finalPhaseRecoveryBlockingDiagnostics(content, payload));
  errors.push(...unresolvedCoverageSchemaDiagnostics(content, payload));

  return errors;
}

function buildEmptyTranscriptState() {
  return {
    cwd: "",
    changedFiles: new Set(),
    execCommands: [],
    execOutputs: [],
    toolNotes: [],
    lastAssistantText: "",
  };
}

function transcriptPathFromProgrammerResult(result) {
  return result?.raw?.transcriptPath || result?.content?.recovered_from_session || null;
}

function promoteIncompleteStructuredProgrammerResult(result, payload, schemaErrors) {
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) {
    return null;
  }
  if (!phaseAllowsArtifactRecovery(payload)) {
    return null;
  }

  const transcriptPath = transcriptPathFromProgrammerResult(result);
  let transcriptState = buildEmptyTranscriptState();
  if (transcriptPath && fs.existsSync(transcriptPath)) {
    try {
      const lines = fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean);
      transcriptState = collectTranscriptContext(lines);
    } catch {
      transcriptState = buildEmptyTranscriptState();
    }
  }

  const extraContent = {
    partial_timed_out: Boolean(result?.content?.partial_timed_out || result?.content?.recovered_after_error),
    recovered_after_schema_validation: true,
    recovered_schema_errors: schemaErrors,
  };

  const recovered = taskIsBeamer(payload)
    ? buildBeamerRecoveredContent(findBeamerArtifactBundle(transcriptState, transcriptPath, payload), transcriptState, transcriptPath, extraContent, payload)
    : buildPptRecoveredContent(findPptArtifactBundle(transcriptState, transcriptPath, payload), transcriptState, transcriptPath, extraContent, payload);

  if (!recovered) {
    return null;
  }

  const priorSummary = String(result?.content?.summary || "").trim();
  const priorNotes = normalizeStructuredNotesToString(result?.content?.notes);
  const schemaErrorLine = `schema_recovery_from_incomplete_json: ${schemaErrors.join("; ")}`;
  const noteParts = [recovered.content?.notes || "", schemaErrorLine];
  if (priorSummary) {
    noteParts.push(`prior_summary: ${priorSummary}`);
  }
  if (priorNotes) {
    noteParts.push(`prior_notes: ${priorNotes}`);
  }

  return {
    ...recovered,
    contentValid: recovered.contentValid !== false,
    text: recovered.text || result?.text || "",
    content: {
      ...recovered.content,
      notes: noteParts.filter(Boolean).join("\n"),
      previous_parse_error: result?.content?.parse_error || null,
      previous_schema_errors: schemaErrors,
    },
  };
}

function applyProgrammerSchemaValidation(role, payload, result) {
  if (role !== "programmer") {
    return result;
  }

  const normalizedResult = normalizeProgrammerResult(result, payload);
  const schemaErrors = validateProgrammerContentWithLocalPreflight(normalizedResult?.content, payload);
  if (schemaErrors.length === 0) {
    return {
      ...normalizedResult,
      contentValid: true,
      content_valid: true,
    };
  }

  const thinArtifactEnvelopeAttempt = contentLooksLikeThinArtifactBackedProgrammerEnvelope(normalizedResult?.content, payload);
  if (!thinArtifactEnvelopeAttempt) {
    const recoveredResult = promoteIncompleteStructuredProgrammerResult(normalizedResult, payload, schemaErrors);
    if (recoveredResult) {
      return recoveredResult;
    }
  }

  return {
    ...normalizedResult,
    contentValid: false,
    content: {
      ...(isPlainObject(normalizedResult?.content) ? normalizedResult.content : {}),
      parse_error: `programmer structured deliverable validation failed: ${schemaErrors.join("; ")}`,
      ready_for_review: false,
      schema_errors: schemaErrors,
    },
  };
}

function testerMessageLooksLikeStaleBeamerArtifactComplaint(message) {
  const text = String(message || "").trim();
  if (!text) return false;
  return /(?:table_coverage.{0,100}(?:slide_ids\s*(?:为空|empty)|planned)|(?:表格|表\s*\d+|Table\s*\d+).{0,120}(?:未映射|未实际放置|缺失|不完整|planned|slide_ids\s*(?:为空|empty))|未在\s*slides\.json\s*中找到\s*kind\s*=\s*(?:roadmap|conclusion_preview)|kind\s*=\s*(?:roadmap|conclusion_preview)|roadmap_page.{0,80}blocked|conclusion_preview_page.{0,80}blocked|恢复而非重新生成|仅基于现有工件恢复|artifact-backed\s+recovery|recovery-only|stale\s+coverage|stale\s+artifact)/i.test(text);
}

function tableCoverageEntriesFromValue(value) {
  if (Array.isArray(value)) return value;
  if (!isPlainObject(value)) return [];
  for (const key of ["items", "tables", "coverage", "entries", "mentions", "ordered_mentions", "source_items", "source_mentions", "mapped_mentions"]) {
    if (Array.isArray(value[key])) return value[key];
  }
  return [];
}

function tableCoverageIsExplicitZeroInventory(value) {
  if (!isPlainObject(value)) return false;
  const status = normalizeCoverageStatus(value.status || "");
  if (status && !["covered", "not_applicable", "complete"].includes(status)) return false;
  const numericCandidates = [
    value.total_source_items,
    value.total_items,
    value.source_table_count,
    value.table_count,
    value.tables_count,
    value.count,
    value.total,
  ];
  const hasExplicitZero = numericCandidates.some((candidate) => {
    const numeric = Number(candidate);
    return Number.isFinite(numeric) && numeric === 0;
  });
  const entries = tableCoverageEntriesFromValue(value);
  if (hasExplicitZero && entries.length === 0) return true;
  const notes = normalizeStructuredNotesToString(value.notes || value.summary || value.reason || "");
  return entries.length === 0 && /(?:source|源文|库存|inventory|Table|表).{0,40}(?:0|零|无|没有|未检测到|no explicit|none)/i.test(notes);
}

function normalizeTableCoverageForArtifactSelection(value) {
  const cloned = deepCloneJson(value);
  if (Array.isArray(cloned)) {
    return normalizeCoverageStatusEntries(cloned);
  }
  if (isPlainObject(cloned)) {
    const entryKey = ["items", "tables", "coverage", "entries", "mentions", "ordered_mentions", "source_items", "source_mentions", "mapped_mentions"]
      .find((key) => Array.isArray(cloned[key]));
    if (!entryKey) return cloned;
    return {
      ...cloned,
      [entryKey]: normalizeCoverageStatusEntries(cloned[entryKey]),
    };
  }
  return cloned;
}

function tableCoverageStats(value, slideMap) {
  const normalized = normalizeTableCoverageForArtifactSelection(value);
  if (!isNonEmptyStructuredValue(normalized)) {
    return {
      value: normalized,
      usable: false,
      zeroInventory: false,
      totalEntries: 0,
      realEntries: 0,
      emptyEntries: 0,
      blockedEntries: 0,
      invalidSlideRefs: 0,
      allEntriesHaveRealSlides: false,
    };
  }
  if (tableCoverageIsExplicitZeroInventory(normalized)) {
    return {
      value: normalized,
      usable: true,
      zeroInventory: true,
      totalEntries: 0,
      realEntries: 0,
      emptyEntries: 0,
      blockedEntries: 0,
      invalidSlideRefs: 0,
      allEntriesHaveRealSlides: false,
    };
  }
  const entries = tableCoverageEntriesFromValue(normalized);
  let realEntries = 0;
  let emptyEntries = 0;
  let blockedEntries = 0;
  let invalidSlideRefs = 0;
  for (const entry of entries) {
    if (!isPlainObject(entry)) {
      emptyEntries += 1;
      continue;
    }
    const status = normalizeCoverageStatus(entry.status || "covered") || "covered";
    if (/^(planned|analysis_only|blocked|missing|partial)$/i.test(status)) {
      blockedEntries += 1;
    }
    const slideIds = [
      ...safeArray(entry.slide_ids),
      ...safeArray(entry.slides),
      ...safeArray(entry.mapped_slide_ids),
      ...safeArray(entry.target_slide_ids),
      ...safeArray(entry.planned_slide_ids),
      ...safeArray(entry.target_slides),
      ...safeArray(entry.planned_slides),
    ].map((item) => String(item || "").trim()).filter(Boolean);
    const validSlideIds = slideIds.filter((slideId) => !slideMap || slideMap.has(slideId));
    invalidSlideRefs += slideIds.length - validSlideIds.length;
    if (validSlideIds.length > 0 && !/^(planned|analysis_only|blocked|missing|partial)$/i.test(status)) {
      realEntries += 1;
    } else {
      emptyEntries += 1;
    }
  }
  return {
    value: normalized,
    usable: entries.length > 0,
    zeroInventory: false,
    totalEntries: entries.length,
    realEntries,
    emptyEntries,
    blockedEntries,
    invalidSlideRefs,
    allEntriesHaveRealSlides: entries.length > 0 && realEntries === entries.length && blockedEntries === 0 && invalidSlideRefs === 0,
  };
}

function tableCoverageRank(stats, priority) {
  if (!stats.usable) return [-1, 0, 0, 0, 0, priority];
  if (stats.allEntriesHaveRealSlides) {
    return [4, -stats.invalidSlideRefs, -stats.emptyEntries, stats.realEntries, stats.totalEntries, priority];
  }
  if (stats.zeroInventory) {
    return [3, 0, 0, 0, 0, priority];
  }
  if (stats.realEntries > 0) {
    return [2, -stats.invalidSlideRefs, -stats.emptyEntries - stats.blockedEntries, stats.realEntries, stats.totalEntries, priority];
  }
  return [1, -stats.invalidSlideRefs, -stats.emptyEntries - stats.blockedEntries, 0, stats.totalEntries, priority];
}

function compareTableCoverageRank(left, right) {
  for (let index = 0; index < Math.max(left.length, right.length); index += 1) {
    const a = Number(left[index] || 0);
    const b = Number(right[index] || 0);
    if (a !== b) return a - b;
  }
  return 0;
}

function selectArtifactBackedTableCoverage(currentValue, analysisDoc, slidesDoc, slideMap = null) {
  const candidates = [
    { value: slidesDoc?.table_coverage, priority: 3 },
    { value: analysisDoc?.table_coverage, priority: 2 },
    { value: currentValue, priority: 1 },
  ];
  let best = null;
  for (const candidate of candidates) {
    const stats = tableCoverageStats(candidate.value, slideMap);
    if (!stats.usable) continue;
    const rank = tableCoverageRank(stats, candidate.priority);
    if (!best || compareTableCoverageRank(rank, best.rank) > 0) {
      best = { value: stats.value, rank };
    }
  }
  return best ? normalizeFinalCoverageEntriesWithSlideIds(best.value, slideMap) : currentValue;
}

function tableCoverageHasRealSlideIds(value, slideMap) {
  const entries = tableCoverageEntriesFromValue(value);
  if (entries.length === 0) return false;
  return entries.every((entry) => {
    if (!isPlainObject(entry)) return false;
    const status = String(entry.status || "covered").trim().toLowerCase();
    if (/^(planned|analysis_only|blocked|missing|partial)$/.test(status)) return false;
    const slideIds = [
      ...safeArray(entry.slide_ids),
      ...safeArray(entry.slides),
      ...safeArray(entry.mapped_slide_ids),
      ...safeArray(entry.target_slide_ids),
      ...safeArray(entry.planned_slide_ids),
      ...safeArray(entry.target_slides),
      ...safeArray(entry.planned_slides),
    ].map((item) => String(item || "").trim()).filter(Boolean);
    return slideIds.length > 0 && slideIds.every((slideId) => !slideMap || slideMap.has(slideId));
  });
}

function beamerArtifactFactsForTester(payload) {
  const programmerOutput = isPlainObject(payload?.programmer_output) ? payload.programmer_output : {};
  const programmerContent = isPlainObject(programmerOutput.content) ? programmerOutput.content : programmerOutput;
  const artifactPaths = isPlainObject(programmerContent.artifact_paths) ? programmerContent.artifact_paths : null;
  if (!artifactPaths) return null;

  const analysisPath = resolveArtifactPathFromReport(artifactPaths, "analysis.json");
  const slidesPath = resolveArtifactPathFromReport(artifactPaths, "slides.json");
  const mainTexPath = resolveArtifactPathFromReport(artifactPaths, "main.tex");
  const mainPdfPath = resolveArtifactPathFromReport(artifactPaths, "main.pdf");
  const analysisDoc = safeReadJsonArtifact(analysisPath);
  const slidesDoc = safeReadJsonArtifact(slidesPath);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  const slideMap = buildSlideMap(slides);
  const roadmapPage = slides.length > 0 ? buildRecoveredRoadmapPage(slides, slidesDoc) : null;
  const conclusionPreviewPage = slides.length > 0 ? buildRecoveredConclusionPreviewPage(slides, slidesDoc) : null;
  const tableCoverage = slidesDoc?.table_coverage ?? analysisDoc?.table_coverage ?? programmerContent.table_coverage;
  const mainTex = isNonEmptyString(mainTexPath) && fs.existsSync(mainTexPath)
    ? fs.readFileSync(mainTexPath, "utf8")
    : "";

  return {
    artifactPaths,
    artifactsPresent: [analysisPath, slidesPath, mainTexPath].every((filePath) => isNonEmptyString(filePath) && fs.existsSync(filePath)),
    pdfPresent: isNonEmptyString(mainPdfPath) && fs.existsSync(mainPdfPath),
    roadmapCovered: isPlainObject(roadmapPage) && String(roadmapPage.status || "").trim().toLowerCase() === "covered",
    conclusionPreviewCovered: isPlainObject(conclusionPreviewPage) && String(conclusionPreviewPage.status || "").trim().toLowerCase() === "covered",
    tableCovered: tableCoverageHasRealSlideIds(tableCoverage, slideMap) && /\\begin\{tabular\}/.test(mainTex),
  };
}

function staleTesterFailureDisprovedByArtifacts(message, facts) {
  const text = String(message || "");
  if (/kind\s*=\s*roadmap|roadmap_page/i.test(text)) return Boolean(facts?.roadmapCovered);
  if (/kind\s*=\s*conclusion_preview|conclusion_preview_page/i.test(text)) return Boolean(facts?.conclusionPreviewCovered);
  if (/table_coverage|表格|表\s*\d+|Table\s*\d+/i.test(text)) return Boolean(facts?.tableCovered);
  return Boolean(facts?.artifactsPresent);
}

function applyTesterSchemaValidation(role, payload, result) {
  if (role !== "tester") return result;
  const content = isPlainObject(result?.content) ? result.content : {};
  if (content.passed !== false || !taskIsBeamer(payload)) return result;
  const phase = payload?.phase;
  if (phase && phase.finalPhase === false) return result;
  const failures = Array.isArray(content.failures) ? content.failures : [];
  const messages = failures.length > 0 ? failures : [content.summary || ""].filter(Boolean);
  if (messages.length === 0 || !messages.every(testerMessageLooksLikeStaleBeamerArtifactComplaint)) {
    return result;
  }
  const facts = beamerArtifactFactsForTester(payload);
  if (!facts || !facts.artifactsPresent || !messages.every((message) => staleTesterFailureDisprovedByArtifacts(message, facts))) {
    return result;
  }
  const summary = "tester 引用了过窄 kind/旧 coverage 判定，但 analysis.json、slides.json 与 main.tex 已证明对应 Beamer 工件覆盖存在；run_agent_role 已将本次陈旧 tester 失败规范化为通过。";
  return {
    ...result,
    contentValid: true,
    content_valid: true,
    content: {
      ...content,
      passed: true,
      summary,
      failures: [],
      ignored_stale_failures: messages,
      artifact_backed_tester_override: true,
      artifact_backed_facts: facts,
      notes: [content.notes, summary].filter(Boolean).join("\n"),
    },
  };
}

function applyAgentResultSchemaValidation(role, payload, result) {
  if (role === "programmer") {
    return applyProgrammerSchemaValidation(role, payload, result);
  }
  if (role === "reviewer") {
    return applyReviewerSchemaValidation(role, result);
  }
  if (role === "tester") {
    return applyTesterSchemaValidation(role, payload, result);
  }
  return result;
}

function fail(message) {
  console.error(message);
  process.exit(1);
}

function writeJsonAndExit(payload) {
  process.stdout.write(JSON.stringify(payload), () => {
    process.exit(0);
  });
}

function writeJsonAndExitWithCode(payload, exitCode) {
  process.stdout.write(JSON.stringify(payload), () => {
    process.exit(exitCode);
  });
}

function decodePayload(arg) {
  if (!arg) {
    fail("missing payload_b64");
  }
  try {
    return JSON.parse(Buffer.from(arg, "base64").toString("utf8"));
  } catch (error) {
    fail(`invalid payload_b64: ${error.message}`);
  }
}

function collectTopLevelJsonObjects(text) {
  const source = String(text || "");
  const results = [];
  let braceDepth = 0;
  let bracketDepth = 0;
  let inString = false;
  let escaped = false;
  let braceStart = -1;
  let bracketStart = -1;

  for (let index = 0; index < source.length; index += 1) {
    const char = source[index];
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (char === "\\") {
        escaped = true;
      } else if (char === '"') {
        inString = false;
      }
      continue;
    }
    if (char === '"') {
      inString = true;
      continue;
    }
    // Brace tracking: open a top-level brace block only when not inside a bracket block
    if (char === "{") {
      if (braceDepth === 0 && bracketDepth === 0) {
        braceStart = index;
      }
      braceDepth += 1;
      continue;
    }
    if (char === "}" && braceDepth > 0) {
      braceDepth -= 1;
      if (braceDepth === 0 && braceStart >= 0) {
        results.push(source.slice(braceStart, index + 1));
        braceStart = -1;
      }
    }
    // Bracket tracking: open a top-level bracket block only when not inside a brace block
    if (char === "[") {
      if (braceDepth === 0 && bracketDepth === 0) {
        bracketStart = index;
      }
      bracketDepth += 1;
      continue;
    }
    if (char === "]" && bracketDepth > 0) {
      bracketDepth -= 1;
      if (bracketDepth === 0 && bracketStart >= 0) {
        results.push(source.slice(bracketStart, index + 1));
        bracketStart = -1;
      }
    }
  }
  return results;
}

function repairLikelyTruncatedJsonCandidate(text) {
  const source = String(text || "").trim();
  if (!source.startsWith("{") && !source.startsWith("[")) return "";
  const variants = [
    ['"appendix":"保留首次到达时间分布推导。}}', '"appendix":"保留首次到达时间分布推导。"}}'],
  ];
  for (const [needle, replacement] of variants) {
    if (!source.includes(needle)) continue;
    const repaired = source.replace(needle, replacement);
    try {
      JSON.parse(repaired);
      return repaired;
    } catch {
      // try next variant
    }
  }
  return "";
}

function stripNonJsonPrefix(text) {
  let working = String(text || "").trim();
  // Repeatedly strip leading label-like patterns: [word] or [word]: or word:
  let changed = true;
  while (changed) {
    changed = false;
    // Pattern 1: [word] optionally followed by :  (e.g. [notation_coverage]:)
    const stripped1 = working.replace(/^\s*(?:\[[a-z][a-z0-9_]*\]\s*:?\s*|[a-z][a-z0-9_]*\s*:\s*)+/i, '');
    if (stripped1 !== working) {
      working = stripped1;
      changed = true;
      continue;
    }
    // Pattern 2: [label ...content...] — label followed by space, content wrapped in the outer []
    // Agent output like [notation_coverage {...}] or [notation_coverage [{...},{...}]]
    const bracketLabelMatch = working.match(/^\s*\[([a-z][a-z0-9_]*)\s+/i);
    if (bracketLabelMatch) {
      working = working.slice(bracketLabelMatch[0].length);
      // Strip the matching trailing ] if it exists
      working = working.replace(/\s*\]\s*$/, '');
      changed = true;
    }
  }
  // If no prefix was stripped, try locating the first { or [
  if (working === text.trim()) {
    const jsonStart = working.search(/[{\[]/);
    if (jsonStart > 0) {
      const prefix = working.slice(0, jsonStart);
      if (/^[\w\s\[\]_:\-\.,!?'"]+$/.test(prefix.trim())) {
        return working.slice(jsonStart);
      }
    }
  }
  return working;
}

function extractTrailingJson(text) {
  const trimmed = String(text || "").trim();
  if (!trimmed) {
    throw new Error("no JSON object found in CLI output");
  }
  try {
    return JSON.parse(trimmed);
  } catch {
    const candidates = collectTopLevelJsonObjects(trimmed);
    for (let index = candidates.length - 1; index >= 0; index -= 1) {
      try {
        return JSON.parse(candidates[index]);
      } catch {
        // try earlier top-level object
      }
    }
    const repaired = repairLikelyTruncatedJsonCandidate(trimmed);
    if (repaired) {
      return JSON.parse(repaired);
    }
    // Try stripping common non-JSON label prefixes (e.g. [notation_coverage])
    const stripped = stripNonJsonPrefix(trimmed);
    if (stripped !== trimmed) {
      try {
        return JSON.parse(stripped);
      } catch {
        const strippedCandidates = collectTopLevelJsonObjects(stripped);
        for (let index = strippedCandidates.length - 1; index >= 0; index -= 1) {
          try {
            return JSON.parse(strippedCandidates[index]);
          } catch {
            // try earlier
          }
        }
      }
    }
    throw new Error("no JSON object found in CLI output");
  }
}

function parseJsonCandidate(text) {
  const trimmed = String(text || "").trim();
  if (!trimmed) {
    throw new Error("empty text");
  }
  try {
    return JSON.parse(trimmed);
  } catch {
    return extractTrailingJson(trimmed);
  }
}

function findLatestAssistantJsonResult(lines, transcriptPath, extraContent = null) {
  let latestAssistantRecord = null;
  let latestAssistantText = "";
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    try {
      const record = JSON.parse(lines[index]);
      const message = record?.message;
      if (message?.role !== "assistant") continue;
      const text = extractTextFromMessage(message);
      if (!text) continue;
      if (!latestAssistantRecord) {
        latestAssistantRecord = record;
        latestAssistantText = text;
      }
      try {
        const content = parseJsonCandidate(text);
        return {
          latestAssistantRecord,
          latestAssistantText,
          result: {
            raw: {
              transcriptRecovered: true,
              transcriptPath,
              record,
            },
            text,
            content: extraContent ? { ...content, ...extraContent } : content,
            contentValid: true,
          },
        };
      } catch {
        continue;
      }
    } catch {
      continue;
    }
  }

  return {
    latestAssistantRecord,
    latestAssistantText,
    result: null,
  };
}

function parseAgentResult(stdout) {
  const parsed = extractTrailingJson(stdout);
  const payloads = parsed.result?.payloads || parsed.payloads || [];
  const texts = payloads
    .map((item) => (typeof item?.text === "string" ? item.text : ""))
    .filter(Boolean);
  const lastText = texts[texts.length - 1] || "";
  for (let index = texts.length - 1; index >= 0; index -= 1) {
    const candidateText = texts[index];
    try {
      const content = parseJsonCandidate(candidateText);
      return {
        raw: parsed,
        text: candidateText,
        content,
        contentValid: true,
      };
    } catch {
      continue;
    }
  }

  return {
    raw: parsed,
    text: lastText,
    content: {
      parse_error: "agent did not return valid JSON",
      raw_text: lastText,
    },
    contentValid: false,
  };
}

function resolveRoleSessionsDir(role) {
  return path.join(os.homedir(), ".openclaw", "agents", role, "sessions");
}

function transcriptPathForSession(role, sessionId) {
  if (!sessionId) return null;
  return path.join(resolveRoleSessionsDir(role), `${sessionId}.jsonl`);
}

function extractAbsolutePaths(text) {
  return [...new Set((String(text || "").match(/\/Users\/cheng\/[^\s"']+/g) || []).filter(Boolean))];
}

function collectPayloadText(payload) {
  if (!payload || typeof payload !== "object") return "";
  return [
    payload.task,
    payload.reviewer_feedback,
    payload.preferred_output_directory,
    isPlainObject(payload.existing_artifact_paths) ? JSON.stringify(payload.existing_artifact_paths) : "",
    payload.programmer_output ? JSON.stringify(payload.programmer_output) : "",
  ].filter(Boolean).join("\n");
}

function extractOutputDirNameHints(text) {
  const results = new Set();
  const patterns = [
    /输出目录名(?:使用|为|是)?\s*([A-Za-z0-9._-]+)/g,
    /输出目录(?:名)?\s*[:：]?\s*([A-Za-z0-9._-]+)/g,
    /工件目录(?:使用|为|是)?\s*([A-Za-z0-9._-]+)/g,
    /目录名使用\s*([A-Za-z0-9._-]+)/g,
  ];
  for (const pattern of patterns) {
    for (const match of String(text || "").matchAll(pattern)) {
      const dirName = String(match?.[1] || "").trim();
      if (dirName) results.add(dirName);
    }
  }
  return [...results];
}

function normalizeArtifactSourceStem(stem) {
  let cleaned = String(stem || "").trim();
  if (!cleaned) return "";
  const withoutUuid = cleaned.replace(/-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i, "");
  if (withoutUuid !== cleaned) {
    cleaned = withoutUuid.replace(/-\d+$/, "");
  }
  return cleaned;
}

function sanitizeArtifactScopeKey(value) {
  return String(value || "")
    .trim()
    .replace(/[^A-Za-z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function currentArtifactScopeKey(payload) {
  return sanitizeArtifactScopeKey(payload?.checkpoint_key || payload?.task_id || "");
}

function artifactScopeKeysForPayload(payload) {
  const keys = [
    payload?.checkpoint_key,
    payload?.task_id,
  ].map(sanitizeArtifactScopeKey).filter(Boolean);
  return [...new Set(keys)];
}

function canonicalArtifactDirNameFromSourcePath(resolvedPath, mode, checkpointKey = "") {
  const ext = path.extname(resolvedPath).toLowerCase();
  const baseName = !ext ? path.basename(resolvedPath) : "";
  if (!ext) {
    const scopedKey = sanitizeArtifactScopeKey(checkpointKey);
    if (!scopedKey || baseName.includes(scopedKey)) {
      return baseName;
    }
    return `${baseName}-${scopedKey}`;
  }
  if (![".md", ".pdf", ".docx", ".tex", ".txt", ".json"].includes(ext)) {
    return "";
  }
  const stem = path.basename(resolvedPath, ext);
  const scopedKey = sanitizeArtifactScopeKey(checkpointKey);
  if (mode === "beamer") {
    return scopedKey ? `${stem}-${scopedKey}-beamer` : `${stem}-beamer`;
  }
  return scopedKey ? `${stem}-${scopedKey}_ppt` : `${stem}_ppt`;
}

function legacyArtifactDirNameFromSourcePath(resolvedPath, mode) {
  const ext = path.extname(resolvedPath).toLowerCase();
  if (!ext) {
    return path.basename(resolvedPath);
  }
  if (![".md", ".pdf", ".docx", ".tex", ".txt", ".json"].includes(ext)) {
    return "";
  }
  const stem = path.basename(resolvedPath, ext);
  return mode === "beamer" ? `${stem}-beamer` : `${stem}_ppt`;
}

function deriveArtifactDirCandidatesFromSourcePath(resolvedPath, mode, baseRoots = [], checkpointKey = "", options = {}) {
  const results = new Set();
  const includeLegacy = options.includeLegacy !== false;
  const ext = path.extname(resolvedPath).toLowerCase();
  if (!ext) {
    results.add(path.resolve(resolvedPath));
    return [...results];
  }
  if (![".md", ".pdf", ".docx", ".tex", ".txt", ".json"].includes(ext)) {
    return [...results];
  }

  const parentDir = path.dirname(resolvedPath);
  const canonicalDirName = canonicalArtifactDirNameFromSourcePath(resolvedPath, mode, checkpointKey);
  const legacyDirName = legacyArtifactDirNameFromSourcePath(resolvedPath, mode);
  if (!canonicalDirName) {
    return [...results];
  }

  results.add(path.join(parentDir, canonicalDirName));
  for (const baseRoot of baseRoots) {
    results.add(path.join(baseRoot, canonicalDirName));
  }
  if (includeLegacy && legacyDirName && legacyDirName !== canonicalDirName) {
    results.add(path.join(parentDir, legacyDirName));
    for (const baseRoot of baseRoots) {
      results.add(path.join(baseRoot, legacyDirName));
    }
  }

  return [...results].map((candidate) => path.resolve(candidate));
}

function deriveTaskSpecificArtifactDirs(payload, mode, options = {}) {
  const taskText = collectPayloadText(payload);
  if (!taskText) return [];

  const candidates = new Set();
  const baseRoots = mode === "beamer"
    ? [
        path.join(os.homedir(), ".openclaw", "media", "outbound"),
        path.join(os.homedir(), ".openclaw", "beamer_outputs"),
        os.homedir(),
      ]
    : [
        path.join(os.homedir(), ".openclaw", "media", "outbound"),
        path.join(os.homedir(), ".openclaw", "ppt_output"),
        os.homedir(),
      ];
  const checkpointKey = currentArtifactScopeKey(payload);
  const existingArtifactPaths = isPlainObject(payload?.existing_artifact_paths) ? payload.existing_artifact_paths : null;

  for (const item of extractAbsolutePaths(taskText)) {
    const resolved = path.resolve(item);
    const ext = path.extname(resolved).toLowerCase();
    if (ext && [".md", ".pdf", ".docx", ".tex", ".txt", ".json"].includes(ext)) {
      for (const candidate of deriveArtifactDirCandidatesFromSourcePath(resolved, mode, baseRoots, checkpointKey, options)) {
        candidates.add(candidate);
      }
    }
    if (!ext) {
      candidates.add(resolved);
    }
  }

  for (const dirName of extractOutputDirNameHints(taskText)) {
    for (const baseRoot of baseRoots) {
      candidates.add(path.join(baseRoot, dirName));
    }
  }

  if (isNonEmptyString(payload?.preferred_output_directory)) {
    const preferred = path.resolve(String(payload.preferred_output_directory).trim());
    if (!pathIsInsideForbiddenArtifactRoot(preferred)) {
      candidates.add(preferred);
    }
  }

  if (existingArtifactPaths) {
    const outputDir = inferArtifactOutputDirectoryFromMap(existingArtifactPaths);
    if (outputDir) {
      candidates.add(outputDir);
    }
  }

  return filterAllowedArtifactDirectories([...candidates].map((candidate) => path.resolve(candidate)));
}

function inferArtifactOutputDirectoryFromMap(artifactPaths) {
  if (!isPlainObject(artifactPaths)) return "";
  for (const key of ["output_directory", "output_dir"]) {
    const direct = artifactPaths[key];
    if (isNonEmptyString(direct) && !pathIsInsideForbiddenArtifactRoot(direct)) {
      return path.resolve(String(direct).trim());
    }
  }

  const weights = new Map([
    ["analysis.json", 6],
    ["slides.json", 6],
    ["main.tex", 5],
    ["main.pdf", 5],
    ["main.pptx", 5],
    ["README.md", 3],
    ["asset_manifest.json", 2],
    ["figures", 1],
  ]);
  const roots = new Map();
  for (const [artifactName, weight] of weights.entries()) {
    const candidatePath = resolveArtifactPathFromReport(artifactPaths, artifactName);
    if (!isNonEmptyString(candidatePath)) continue;
    if (pathIsInsideForbiddenArtifactRoot(candidatePath)) continue;
    const normalizedPath = path.resolve(candidatePath.trim());
    const root = artifactName === "figures" ? path.dirname(normalizedPath) : path.dirname(normalizedPath);
    roots.set(root, (roots.get(root) || 0) + weight);
  }
  const ranked = [...roots.entries()].sort((a, b) => b[1] - a[1]);
  return ranked[0]?.[0] || "";
}

function normalizeArtifactHintName(value) {
  let cleaned = path.basename(String(value || "").trim().toLowerCase());
  if (!cleaned) return "";
  cleaned = cleaned.replace(/\.(md|pdf|docx|tex|txt|json|pptx)$/i, "");
  cleaned = cleaned.replace(/-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i, "");
  cleaned = cleaned.replace(/-\d+$/i, "");
  let previous = "";
  while (cleaned && cleaned !== previous) {
    previous = cleaned;
    cleaned = cleaned.replace(/(?:[-_](?:beamer|ppt|package|bundle|output|outputs|deliverables|deliverable|artifact|artifacts|results|result))+$/i, "");
  }
  cleaned = cleaned.replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  return cleaned;
}

const ARTIFACT_HINT_STOPWORDS = new Set([
  "beamer",
  "ppt",
  "package",
  "bundle",
  "output",
  "outputs",
  "deliverable",
  "deliverables",
  "artifact",
  "artifacts",
  "result",
  "results",
  "main",
  "paper",
  "task",
]);

function tokenizeArtifactHintName(value) {
  return normalizeArtifactHintName(value)
    .split("_")
    .map((token) => token.trim())
    .filter(Boolean)
    .filter((token) => token.length >= 4 && !ARTIFACT_HINT_STOPWORDS.has(token));
}

function buildPayloadArtifactHintProfile(payload, mode) {
  const taskText = collectPayloadText(payload);
  const explicitPaths = extractAbsolutePaths(taskText);
  const outputDirHints = extractOutputDirNameHints(taskText);
  const exactBasenames = new Set();
  const normalizedNames = new Set();
  const tokenSets = [];
  const seenTokenKeys = new Set();
  const allowedFileExts = new Set([".md", ".pdf", ".docx", ".tex", ".txt", ".json", ".pptx"]);

  const addHintName = (value) => {
    const baseName = path.basename(String(value || "").trim());
    if (!baseName) return;
    exactBasenames.add(baseName);
    const normalized = normalizeArtifactHintName(baseName);
    if (!normalized) return;
    normalizedNames.add(normalized);
    const tokens = tokenizeArtifactHintName(baseName);
    if (tokens.length === 0) return;
    const tokenKey = tokens.join("|");
    if (seenTokenKeys.has(tokenKey)) return;
    seenTokenKeys.add(tokenKey);
    tokenSets.push(tokens);
  };

  for (const item of explicitPaths) {
    const resolved = path.resolve(item);
    const ext = path.extname(resolved).toLowerCase();
    if (ext && allowedFileExts.has(ext)) {
      const canonicalDirName = canonicalArtifactDirNameFromSourcePath(resolved, mode, currentArtifactScopeKey(payload));
      if (canonicalDirName) {
        addHintName(canonicalDirName);
      }
      continue;
    }
    if (!ext) {
      addHintName(path.basename(resolved));
    }
  }

  for (const dirName of outputDirHints) {
    addHintName(dirName);
  }

  for (const candidate of deriveTaskSpecificArtifactDirs(payload, mode, {
    includeLegacy: artifactScopeKeysForPayload(payload).length === 0,
  })) {
    addHintName(path.basename(candidate));
  }

  return {
    explicitHintPresent: explicitPaths.length > 0 || outputDirHints.length > 0,
    exactBasenames,
    normalizedNames,
    tokenSets,
  };
}

function scoreBundleAgainstPayloadHints(bundleDir, profile) {
  if (!bundleDir || !profile?.explicitHintPresent) {
    return { score: 0, reason: "no_explicit_payload_hints" };
  }

  const baseName = path.basename(bundleDir);
  const normalizedBaseName = normalizeArtifactHintName(baseName);
  if (!normalizedBaseName) {
    return { score: 0, reason: "empty_bundle_basename" };
  }

  if (profile.exactBasenames.has(baseName)) {
    return { score: 120, reason: "exact_bundle_basename_match" };
  }

  if (profile.normalizedNames.has(normalizedBaseName)) {
    return { score: 100, reason: "normalized_bundle_name_match" };
  }

  const bundleTokens = new Set(tokenizeArtifactHintName(baseName));
  if (bundleTokens.size === 0) {
    return { score: 0, reason: "bundle_has_no_meaningful_tokens" };
  }

  let bestOverlap = 0;
  let bestHintTokenCount = 0;
  for (const tokens of profile.tokenSets || []) {
    let overlap = 0;
    for (const token of tokens) {
      if (bundleTokens.has(token)) overlap += 1;
    }
    if (overlap > bestOverlap) {
      bestOverlap = overlap;
      bestHintTokenCount = tokens.length;
    }
  }

  if (bestOverlap >= 2) {
    const densityBonus = Math.min(9, Math.round((bestOverlap / Math.max(bestHintTokenCount, bundleTokens.size, 1)) * 10));
    return {
      score: 40 + bestOverlap * 10 + densityBonus,
      reason: "meaningful_token_overlap_match",
    };
  }

  return { score: 0, reason: "no_payload_match" };
}

function payloadMatchedBundleFallbackIsUnambiguous(rankedBundles, minScore = 100) {
  const ranked = Array.isArray(rankedBundles) ? rankedBundles : [];
  const top = ranked[0];
  if (!top || Number(top.payloadMatchScore || 0) < minScore) {
    return false;
  }
  return !ranked.some((candidate, index) =>
    index > 0
    && Number(candidate?.payloadMatchScore || 0) >= Number(top.payloadMatchScore || 0)
    && Number(candidate?.exactRootMatch || 0) === Number(top.exactRootMatch || 0)
    && Number(candidate?.scopeMatchScore || 0) === Number(top.scopeMatchScore || 0)
  );
}

function bundleScopeMatchInfo(bundleDir, payload) {
  const scopeKeys = artifactScopeKeysForPayload(payload);
  if (scopeKeys.length === 0 || !bundleDir) {
    return { score: 0, matchedKey: "", legacyPenalty: 0 };
  }
  const baseName = path.basename(bundleDir);
  const normalizedBaseName = normalizeArtifactHintName(baseName);
  for (const [index, key] of scopeKeys.entries()) {
    const normalizedKey = normalizeArtifactHintName(key);
    const directPattern = new RegExp(`(?:^|[-_])${key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?:[-_]|$)`, "i");
    if (directPattern.test(baseName) || (normalizedKey && normalizedBaseName.includes(normalizedKey))) {
      return {
        score: index === 0 ? 80 : 60,
        matchedKey: key,
        legacyPenalty: 0,
      };
    }
  }
  return {
    score: 0,
    matchedKey: "",
    legacyPenalty: 45,
  };
}

function selectRecoveredArtifactBundle(scoredBundles, payload, mode, taskSpecificRoots = []) {
  const profile = buildPayloadArtifactHintProfile(payload, mode);
  const hasScopedPayload = artifactScopeKeysForPayload(payload).length > 0;
  const ranked = scoredBundles
    .map((bundle) => {
      const exactRootRank = taskSpecificRootRank(bundle.dir, taskSpecificRoots);
      const exactRootMatch = exactRootRank < Number.MAX_SAFE_INTEGER ? 1 : 0;
      const payloadAffinity = scoreBundleAgainstPayloadHints(bundle.dir, profile);
      const scopeAffinity = bundleScopeMatchInfo(bundle.dir, payload);
      return {
        ...bundle,
        exactRootMatch,
        exactRootRank,
        scopeMatchScore: scopeAffinity.score,
        scopeMatchKey: scopeAffinity.matchedKey,
        legacyScopePenalty: exactRootMatch > 0 ? 0 : scopeAffinity.legacyPenalty,
        payloadMatchScore: payloadAffinity.score,
        payloadMatchReason: payloadAffinity.reason,
      };
    })
    .filter((bundle) => {
      if (!profile.explicitHintPresent) return true;
      return bundle.exactRootMatch > 0 || bundle.scopeMatchScore > 0 || bundle.payloadMatchScore > 0;
    })
    .sort((a, b) =>
      (b.exactRootMatch - a.exactRootMatch) ||
      (a.exactRootRank - b.exactRootRank) ||
      (b.scopeMatchScore - a.scopeMatchScore) ||
      (b.payloadMatchScore - a.payloadMatchScore) ||
      (a.legacyScopePenalty - b.legacyScopePenalty) ||
      (b.score - a.score) ||
      (b.newestMtimeMs - a.newestMtimeMs)
    );

  if (ranked.length === 0) {
    return {
      bundle: null,
      reason: profile.explicitHintPresent ? "no_payload_matched_bundle" : "no_matching_bundle_found",
      profile,
      ranked,
    };
  }

  const top = ranked[0];
  if (hasScopedPayload && top.exactRootMatch === 0 && top.scopeMatchScore === 0) {
    const scopedPeer = ranked.find((candidate) => candidate.exactRootMatch > 0 || candidate.scopeMatchScore > 0);
    if (scopedPeer) {
      return {
        bundle: scopedPeer,
        reason: "selected_checkpoint_scoped_bundle",
        profile,
        ranked,
      };
    }
    if (profile.explicitHintPresent && payloadMatchedBundleFallbackIsUnambiguous(ranked, 100)) {
      return {
        bundle: top,
        reason: "selected_payload_matched_bundle_without_checkpoint_scope",
        profile,
        ranked,
      };
    }
    return {
      bundle: null,
      reason: "no_checkpoint_scoped_bundle_found",
      profile,
      ranked,
    };
  }
  if (profile.explicitHintPresent && top.exactRootMatch === 0) {
    const ambiguousPeer = ranked.find((candidate, index) =>
      index > 0 &&
      candidate.exactRootMatch === top.exactRootMatch &&
      candidate.scopeMatchScore === top.scopeMatchScore &&
      candidate.payloadMatchScore === top.payloadMatchScore &&
      candidate.score === top.score
    );
    if (ambiguousPeer && top.payloadMatchScore < 100) {
      return {
        bundle: null,
        reason: "ambiguous_payload_matched_bundle",
        profile,
        ranked,
      };
    }
  }

  return {
    bundle: top,
    reason: top.exactRootMatch > 0
      ? "selected_exact_task_specific_bundle"
      : top.scopeMatchScore > 0
        ? "selected_checkpoint_scoped_bundle"
        : (profile.explicitHintPresent ? "selected_payload_matched_bundle" : "selected_best_scored_bundle"),
    profile,
    ranked,
  };
}

function transcriptLooksCompatible(transcriptPath, payload) {
  if (!transcriptPath) return false;
  if (!payload || typeof payload !== "object") return true;

  let transcriptText = "";
  try {
    transcriptText = fs.readFileSync(transcriptPath, "utf8");
  } catch {
    return false;
  }

  const normalized = transcriptText.toLowerCase();
  const taskText = collectPayloadText(payload);
  const sourcePaths = extractAbsolutePaths(taskText).filter((item) => /\.(md|pdf|tex|pptx|docx|json)$/i.test(item));

  if (sourcePaths.length > 0 && !sourcePaths.some((item) => transcriptText.includes(item))) {
    return false;
  }

  const wantsPpt = taskIsPpt(payload);
  const wantsBeamer = taskIsBeamer(payload);
  const hasPptSignals = [
    "main.pptx",
    "render_pptx.py",
    "pptx_validation.json",
    "ppt 汇报文件",
    "powerpoint-generation task",
  ].some((token) => normalized.includes(token.toLowerCase()));
  const hasBeamerSignals = [
    "main.tex",
    "main.pdf",
    "beamer 助手",
    "beamer 汇报文件",
    "metropolis",
    "inn-beamer",
  ].some((token) => normalized.includes(token.toLowerCase()));

  if (wantsPpt) {
    if (hasBeamerSignals && !hasPptSignals) return false;
    return hasPptSignals || sourcePaths.length > 0;
  }

  if (wantsBeamer) {
    if (hasPptSignals && !hasBeamerSignals) return false;
    return hasBeamerSignals || sourcePaths.length > 0;
  }

  return true;
}

function extractTextFromMessage(message) {
  const parts = message?.content;
  if (!Array.isArray(parts)) return "";
  return parts
    .filter((part) => part?.type === "text" && typeof part?.text === "string")
    .map((part) => part.text)
    .join("\n")
    .trim();
}

function compactSingleLine(text, maxLength = 1200) {
  const normalized = String(text || "").replace(/\s+/g, " ").trim();
  if (!normalized) return "";
  return normalized.length > maxLength ? `${normalized.slice(0, Math.max(0, maxLength - 1)).trimEnd()}…` : normalized;
}

function collectToolDetails(record, state) {
  const message = record?.message;
  if (!message || !Array.isArray(message.content)) return;
  for (const part of message.content) {
    if (!part || typeof part !== "object") continue;
    if (message.role === "assistant" && part.type === "toolCall") {
      const name = String(part.name || "").trim();
      const args = part.arguments && typeof part.arguments === "object" ? part.arguments : {};
      const filePath = args.file_path || args.path || "";
      if ((name === "edit" || name === "write") && filePath) {
        state.changedFiles.add(String(filePath));
      }
      if (name === "exec" && typeof args.command === "string" && args.command.trim()) {
        state.execCommands.push(args.command.trim());
      }
      continue;
    }
    if (message.role === "toolResult") {
      const toolName = String(message.toolName || "").trim();
      const text = extractTextFromMessage(message);
      if (!text) continue;
      if (toolName === "exec") {
        state.execOutputs.push(text);
      } else if (toolName === "edit" || toolName === "write") {
        state.toolNotes.push(text);
      }
    }
  }
}

function summarizeExecFailure(text) {
  const lines = String(text || "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const errorLines = lines.filter((line) =>
    /^! /.test(line) ||
    /LaTeX Error:/i.test(line) ||
    /Emergency stop/i.test(line) ||
    /Command exited with code/i.test(line)
  );
  return errorLines.slice(0, 8);
}

function collectTranscriptContext(lines) {
  const state = {
    cwd: "",
    changedFiles: new Set(),
    execCommands: [],
    execOutputs: [],
    toolNotes: [],
    lastAssistantText: "",
    lastAssistantTimestamp: "",
    lastToolResultTimestamp: "",
    lastToolResultToolName: "",
    missingFinalJsonAfterToolResult: false,
    recentAssistantError: false,
    recentAssistantErrorMessage: "",
  };

  for (const line of lines) {
    try {
      const record = JSON.parse(line);
      if (!state.cwd && record?.type === "session" && typeof record?.cwd === "string") {
        state.cwd = record.cwd;
      }
      const message = record?.message;
      if (message?.role === "assistant") {
        const text = extractTextFromMessage(message);
        if (text) {
          state.lastAssistantText = text;
          state.lastAssistantTimestamp = String(record?.timestamp || "");
        }
        const assistantErrorMessage = isNonEmptyString(record?.errorMessage)
          ? String(record.errorMessage || "").trim()
          : (isNonEmptyString(message?.errorMessage) ? String(message.errorMessage || "").trim() : "");
        if (!state.recentAssistantError && assistantErrorMessage) {
          state.recentAssistantError = true;
          state.recentAssistantErrorMessage = assistantErrorMessage;
        }
      }
      if (message?.role === "toolResult") {
        state.lastToolResultTimestamp = String(record?.timestamp || "");
        state.lastToolResultToolName = String(message?.toolName || "").trim();
      }
      collectToolDetails(record, state);
    } catch {
      continue;
    }
  }

  const lastToolResultMs = Date.parse(state.lastToolResultTimestamp || "");
  const lastAssistantMs = Date.parse(state.lastAssistantTimestamp || "");
  if (
    Number.isFinite(lastToolResultMs) &&
    (
      !Number.isFinite(lastAssistantMs)
      || lastAssistantMs <= lastToolResultMs
    )
  ) {
    state.missingFinalJsonAfterToolResult = true;
  }

  return state;
}

function assistantErrorLooksTransportLike(message) {
  const text = String(message || "").trim();
  if (!text) return false;
  return /fetch failed|connection error|network error|provider returned error|rate limit|overloaded|timeout|timed out|etimedout|econnreset|econnrefused|enotfound|eai_again|socket hang up|http\s*40\d|http\s*50\d/i.test(text);
}

function buildAssistantErrorTranscriptResult(transcriptPath, assistantErrorMessage, options = {}) {
  const normalizedMessage = String(assistantErrorMessage || "").trim();
  if (!normalizedMessage) return null;
  const latestAssistantText = String(options.latestAssistantText || "").trim();
  const text = latestAssistantText || normalizedMessage;
  return {
    raw: {
      transcriptRecovered: true,
      transcriptPath,
      record: options.record || null,
    },
    text,
    content: {
      ...(options.extraContent || {}),
      parse_error: `assistant transcript error: ${normalizedMessage}`,
      recovered_error_message: normalizedMessage,
      raw_text: text,
      agent_terminal_error: true,
      transport_error: assistantErrorLooksTransportLike(normalizedMessage),
      transcript_missing_final_json_after_tool_result: options.missingFinalJsonAfterToolResult === true,
    },
    contentValid: false,
  };
}

function walkFiles(rootPath, maxDepth, visitor, depth = 0) {
  if (!rootPath || depth > maxDepth) return;
  let entries = [];
  try {
    entries = fs.readdirSync(rootPath, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    const fullPath = path.join(rootPath, entry.name);
    if (entry.isDirectory()) {
      walkFiles(fullPath, maxDepth, visitor, depth + 1);
      continue;
    }
    if (entry.isFile()) {
      visitor(fullPath);
    }
  }
}

function appendArtifactSearchLog(payload) {
  try {
    fs.mkdirSync(path.dirname(ARTIFACT_SEARCH_LOG), { recursive: true });
    fs.appendFileSync(ARTIFACT_SEARCH_LOG, `${JSON.stringify({
      time: new Date().toISOString(),
      ...payload,
    })}\n`, "utf8");
  } catch {
    // best effort only
  }
}

function extractAbsolutePathCandidates(values = []) {
  const results = new Set();
  for (const value of values) {
    const matches = String(value || "").match(/\/Users\/cheng\/[^\s"']+/g) || [];
    for (const match of matches) {
      results.add(match);
    }
  }
  return [...results];
}

function normalizeExistingDir(candidate) {
  if (!candidate) return null;
  const resolved = path.resolve(candidate);
  try {
    if (fs.existsSync(resolved) && fs.statSync(resolved).isDirectory()) {
      return resolved;
    }
  } catch {
    return null;
  }
  return null;
}

function pathMatchesTaskSpecificRoots(candidate, taskSpecificRoots) {
  if (!candidate) return false;
  const resolved = path.resolve(candidate);
  return (taskSpecificRoots || []).some((root) => {
    const normalizedRoot = path.resolve(root);
    return resolved === normalizedRoot || resolved.startsWith(`${normalizedRoot}${path.sep}`);
  });
}

function taskSpecificRootRank(candidate, taskSpecificRoots) {
  if (!candidate) return Number.MAX_SAFE_INTEGER;
  const resolved = path.resolve(candidate);
  for (let index = 0; index < (taskSpecificRoots || []).length; index += 1) {
    const normalizedRoot = path.resolve(taskSpecificRoots[index]);
    if (resolved === normalizedRoot || resolved.startsWith(`${normalizedRoot}${path.sep}`)) {
      return index;
    }
  }
  return Number.MAX_SAFE_INTEGER;
}

function buildArtifactSearchRoots(state, transcriptPath, mode, payload = null) {
  const candidateRoots = new Set();
  const transcriptDir = transcriptPath ? path.dirname(transcriptPath) : "";
  const compatRoots = mode === "beamer"
    ? [
        path.join(os.homedir(), ".openclaw", "beamer_outputs"),
        path.join(os.homedir(), ".openclaw", "leankan_beamer_package"),
        path.join(os.homedir(), ".openclaw", "media", "outbound"),
      ]
    : [
        path.join(os.homedir(), ".openclaw", "ppt_output"),
        path.join(os.homedir(), ".openclaw", "media", "outbound"),
      ];
  const taskSpecificRoots = deriveTaskSpecificArtifactDirs(payload, mode, {
    includeLegacy: artifactScopeKeysForPayload(payload).length === 0,
  });
  const existingTaskSpecificRoots = taskSpecificRoots
    .map((root) => normalizeExistingDir(root))
    .filter(Boolean);
  const restrictToTaskSpecificRoots = existingTaskSpecificRoots.length > 0;

  if (!restrictToTaskSpecificRoots && state.cwd) {
    candidateRoots.add(state.cwd);
    candidateRoots.add(path.join(state.cwd, "deliverables"));
    candidateRoots.add(path.join(state.cwd, "output"));
    candidateRoots.add(path.join(state.cwd, "outputs"));
  }

  for (const root of taskSpecificRoots) {
    candidateRoots.add(root);
  }

  for (const filePath of state.changedFiles || []) {
    if (!filePath) continue;
    const candidateDir = path.dirname(filePath);
    if (restrictToTaskSpecificRoots && !pathMatchesTaskSpecificRoots(candidateDir, existingTaskSpecificRoots)) {
      continue;
    }
    candidateRoots.add(candidateDir);
  }

  const commandPathCandidates = extractAbsolutePathCandidates(state.execCommands || []);
  for (const candidate of commandPathCandidates) {
    let candidateDir = candidate;
    try {
      const looksLikeFile = fs.existsSync(candidate) && fs.statSync(candidate).isFile();
      candidateDir = looksLikeFile ? path.dirname(candidate) : candidate;
    } catch {
      candidateDir = path.extname(candidate) ? path.dirname(candidate) : candidate;
    }
    if (restrictToTaskSpecificRoots && !pathMatchesTaskSpecificRoots(candidateDir, existingTaskSpecificRoots)) {
      continue;
    }
    candidateRoots.add(candidateDir);
  }

  if (transcriptDir) {
    candidateRoots.add(transcriptDir);
  }

  if (!restrictToTaskSpecificRoots) {
    for (const compatRoot of compatRoots) {
      candidateRoots.add(compatRoot);
    }
  }

  const existingRoots = [];
  const missingRoots = [];
  for (const root of candidateRoots) {
    const normalized = normalizeExistingDir(root);
    if (normalized) {
      existingRoots.push(normalized);
    } else if (root) {
      missingRoots.push(path.resolve(root));
    }
  }

  return {
    roots: [...new Set(existingRoots)],
    missingRoots: [...new Set(missingRoots)],
    taskSpecificRoots: [...new Set(taskSpecificRoots.map((root) => path.resolve(root)))],
  };
}

function scoreArtifactBundles(bundles, requiredNames, optionalNames) {
  return [...bundles.values()]
    .map((bundle) => {
      const files = bundle.files;
      const requiredCount = requiredNames.filter((name) => files[name]).length;
      const optionalCount = optionalNames.filter((name) => files[name]).length;
      const missingRequiredNames = requiredNames.filter((name) => !files[name]);
      return {
        ...bundle,
        requiredCount,
        optionalCount,
        missingRequiredNames,
        score: requiredCount * 10 + optionalCount,
      };
    })
    .filter((bundle) => bundle.missingRequiredNames.length === 0)
    .sort((a, b) => (b.score - a.score) || (b.newestMtimeMs - a.newestMtimeMs));
}

function beamerArtifactBundleRequirements(payload) {
  const phase = isPlainObject(payload?.phase) ? payload.phase : null;
  const phaseIndex = deckPhaseIndex(payload);
  if (phase && phase.finalPhase === false && phaseIndex === 1) {
    return {
      requiredNames: ["analysis.json"],
      optionalNames: ["slides.json", "asset_manifest.json", "figures", "main.tex", "main.pdf", "README.md"],
    };
  }
  if (phase && phase.finalPhase === false && phaseIndex === 2) {
    return {
      requiredNames: ["analysis.json", "slides.json"],
      optionalNames: ["asset_manifest.json", "figures", "main.tex", "main.pdf", "README.md"],
    };
  }
  if (phase && phase.finalPhase === false && phaseIndex === 3) {
    return {
      requiredNames: ["analysis.json", "slides.json"],
      optionalNames: ["asset_manifest.json", "figures", "main.tex", "main.pdf", "README.md"],
    };
  }
  if (phase && phase.finalPhase === false && phaseIndex === 4) {
    return {
      requiredNames: ["analysis.json", "slides.json"],
      optionalNames: ["asset_manifest.json", "figures", "main.tex", "main.pdf", "README.md"],
    };
  }
  if (phase && phase.finalPhase === false && phaseIndex >= 5) {
    return {
      requiredNames: ["analysis.json", "slides.json", "main.tex", "main.pdf"],
      optionalNames: ["asset_manifest.json", "figures", "README.md"],
    };
  }
  return {
    requiredNames: ["analysis.json", "slides.json", "main.tex", "main.pdf", "README.md", "asset_manifest.json", "figures"],
    optionalNames: [],
  };
}

function pptArtifactBundleRequirements(payload) {
  const phase = isPlainObject(payload?.phase) ? payload.phase : null;
  const phaseIndex = deckPhaseIndex(payload);
  if (phase && phase.finalPhase === false && phaseIndex === 1) {
    return {
      requiredNames: ["analysis.json"],
      optionalNames: ["slides.json", "main.pptx", "pptx_validation.json", "README.md"],
    };
  }
  if (phase && phase.finalPhase === false && phaseIndex >= 2 && phaseIndex < 5) {
    return {
      requiredNames: ["analysis.json", "slides.json"],
      optionalNames: ["main.pptx", "pptx_validation.json", "README.md"],
    };
  }
  if (phase && phase.finalPhase === false && phaseIndex >= 5) {
    return {
      requiredNames: ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json"],
      optionalNames: ["README.md"],
    };
  }
  return {
    requiredNames: ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json", "README.md"],
    optionalNames: [],
  };
}

function getPdfPageCount(pdfPath) {
  if (!pdfPath || !fs.existsSync(pdfPath)) return null;
  try {
    const result = spawnSync("pdfinfo", [pdfPath], {
      encoding: "utf8",
      timeout: 10000,
      maxBuffer: 1024 * 1024,
    });
    const text = String(result.stdout || result.stderr || "");
    const match = text.match(/Pages:\s+(\d+)/i);
    return match ? Number(match[1]) : null;
  } catch {
    return null;
  }
}

function beamerReadmeHasRecoveredStateWording(text) {
  return /recovered Beamer delivery bundle|recovered from existing artifacts|Resume from final acceptance|The bundle was recovered/i.test(String(text || ""));
}

function ensureBeamerReadmeArtifact(bundle, files, pdfPages = null) {
  if (!isPlainObject(files)) {
    return files;
  }
  const bundleDir = String(bundle?.dir || "").trim();
  if (!bundleDir || !fs.existsSync(bundleDir)) {
    return files;
  }
  const coreNames = ["analysis.json", "slides.json", "main.tex", "main.pdf"];
  if (!coreNames.every((name) => isNonEmptyString(files[name]) && fs.existsSync(files[name]))) {
    return files;
  }

  const readmePath = path.join(bundleDir, "README.md");
  try {
    if (!fs.existsSync(readmePath)) {
      const lines = [
        "# Beamer Deliverable",
        "",
        "This directory contains the Beamer delivery bundle.",
        "",
        "## Artifacts",
        "",
        "- `analysis.json`: source-side analysis and coverage ledgers.",
        "- `slides.json`: slide plan and structured coverage mapping.",
        "- `main.tex`: Beamer source file.",
        `- \`main.pdf\`: compiled Beamer deck${pdfPages ? ` (${pdfPages} pages)` : ""}.`,
        "- `asset_manifest.json`: localized asset manifest, when present.",
        "- `figures/`: localized figure directory.",
        "",
        "## Status",
        "",
        "- Core artifacts are present in this directory.",
        "- Final acceptance depends on the structured coverage fields in `analysis.json` and `slides.json`.",
      ];
      fs.writeFileSync(readmePath, `${lines.join("\n")}\n`, "utf8");
    } else {
      const existing = fs.readFileSync(readmePath, "utf8");
      if (beamerReadmeHasRecoveredStateWording(existing)) {
        const lines = [
          "# Beamer Deliverable",
          "",
          "This directory contains the Beamer delivery bundle.",
          "",
          "## Artifacts",
          "",
          "- `analysis.json`: source-side analysis and coverage ledgers.",
          "- `slides.json`: slide plan and structured coverage mapping.",
          "- `main.tex`: Beamer source file.",
          `- \`main.pdf\`: compiled Beamer deck${pdfPages ? ` (${pdfPages} pages)` : ""}.`,
          "- `asset_manifest.json`: localized asset manifest, when present.",
          "- `figures/`: localized figure directory.",
          "",
          "## Status",
          "",
          "- Core artifacts are present in this directory.",
          "- Final acceptance depends on the structured coverage fields in `analysis.json` and `slides.json`.",
        ];
        fs.writeFileSync(readmePath, `${lines.join("\n")}\n`, "utf8");
      }
    }
    if (fs.existsSync(readmePath)) {
      return {
        ...files,
        "README.md": readmePath,
      };
    }
  } catch {
    return files;
  }
  return files;
}

function pptReadmeHasRecoveredStateWording(text) {
  return /recovered PPT delivery bundle|recovered from existing artifacts|Resume from final acceptance|The bundle was recovered/i.test(String(text || ""));
}

function pptReadmeArtifactContent(bundle, files) {
  const report = pptValidationReportFromFiles(files);
  const fatalCount = pptValidationFatalCount(report);
  const warningCount = pptValidationWarningCount(report);
  const assetSummary = pptEquationAssetSummary(files);
  const lines = [
    "# PPT Deliverable",
    "",
    "This directory contains the packaged PPT delivery bundle.",
    "",
    "## Artifacts",
    "",
    "- `analysis.json`: source-side analysis and coverage ledgers.",
    "- `slides.json`: slide plan and structured coverage mapping.",
    "- `main.pptx`: rendered PowerPoint deck.",
    "- `pptx_validation.json`: renderer validation report.",
    "- `asset_manifest.json`: localized asset manifest, when present.",
    "- `figures/`: localized figure directory, when present.",
    "",
    "## Status",
    "",
    "- Core artifacts are present in this directory.",
    `- PPT validation recovered ok=${report.ok !== false && fatalCount === 0}, fatal_count=${fatalCount}, warning_count=${warningCount}.`,
    `- Equation assets recovered total=${assetSummary.total}, failed=${assetSummary.failed}, created=${assetSummary.created}, reused=${assetSummary.reused}.`,
    "- Final acceptance depends on the structured coverage fields in `analysis.json` and `slides.json`.",
  ];
  const bundleDir = String(bundle?.dir || "").trim();
  if (bundleDir) {
    lines.splice(2, 0, `Output directory: \`${bundleDir}\``, "");
  }
  return `${lines.join("\n")}\n`;
}

function ensurePptReadmeArtifact(bundle, files) {
  if (!isPlainObject(files)) {
    return files;
  }
  const bundleDir = String(bundle?.dir || "").trim();
  if (!bundleDir || !fs.existsSync(bundleDir)) {
    return files;
  }
  const coreNames = ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json"];
  if (!coreNames.every((name) => isNonEmptyString(files[name]) && fs.existsSync(files[name]))) {
    return files;
  }

  const readmePath = path.join(bundleDir, "README.md");
  try {
    if (!fs.existsSync(readmePath)) {
      fs.writeFileSync(readmePath, pptReadmeArtifactContent(bundle, files), "utf8");
    } else {
      const existing = fs.readFileSync(readmePath, "utf8");
      if (pptReadmeHasRecoveredStateWording(existing)) {
        fs.writeFileSync(readmePath, pptReadmeArtifactContent(bundle, files), "utf8");
      }
    }
    if (fs.existsSync(readmePath)) {
      return {
        ...files,
        "README.md": readmePath,
      };
    }
  } catch {
    return files;
  }
  return files;
}

function findBeamerArtifactBundle(state, transcriptPath, payload = null) {
  const { roots, missingRoots, taskSpecificRoots } = buildArtifactSearchRoots(state, transcriptPath, "beamer", payload);
  const bundles = new Map();
  const artifactNames = new Set(["analysis.json", "slides.json", "main.tex", "main.pdf", "README.md", "asset_manifest.json"]);
  const hitPaths = [];
  const seenHitPaths = new Set();

  const recordArtifact = (dir, artifactName, artifactPath) => {
    if (!dir || !artifactName || !artifactPath) return;
    const current = bundles.get(dir) || {
      dir,
      files: {},
      newestMtimeMs: 0,
    };
    current.files[artifactName] = artifactPath;
    if (!seenHitPaths.has(artifactPath)) {
      hitPaths.push(artifactPath);
      seenHitPaths.add(artifactPath);
    }
    try {
      const stat = fs.statSync(artifactPath);
      current.newestMtimeMs = Math.max(current.newestMtimeMs, stat.mtimeMs);
    } catch {
      // ignore stat failure
    }
    bundles.set(dir, current);
  };

  const recordFiguresDir = (candidateDir) => {
    if (!candidateDir) return;
    try {
      const stat = fs.statSync(candidateDir);
      if (!stat.isDirectory() || path.basename(candidateDir) !== "figures") return;
      recordArtifact(path.dirname(candidateDir), "figures", candidateDir);
    } catch {
      // ignore stat failure
    }
  };

  for (const root of roots) {
    recordFiguresDir(root);
    recordFiguresDir(path.join(root, "figures"));
    walkFiles(root, 4, (fullPath) => {
      const base = path.basename(fullPath);
      if (!artifactNames.has(base)) return;
      const dir = path.dirname(fullPath);
      recordArtifact(dir, base, fullPath);
      recordFiguresDir(path.join(dir, "figures"));
    });
  }

  const { requiredNames, optionalNames } = beamerArtifactBundleRequirements(payload);
  const scored = scoreArtifactBundles(bundles, requiredNames, optionalNames);
  const selection = selectRecoveredArtifactBundle(scored, payload, "beamer", taskSpecificRoots);
  appendArtifactSearchLog({
    mode: "beamer",
    transcriptPath,
    roots,
    missingRoots,
    taskSpecificRoots,
    hitCount: hitPaths.length,
    hitPaths,
    candidateCount: scored.length,
    selectedDir: selection.bundle?.dir || null,
    selectedArtifacts: selection.bundle?.files || null,
    selectedPayloadMatchScore: selection.bundle?.payloadMatchScore || 0,
    selectedPayloadMatchReason: selection.bundle?.payloadMatchReason || null,
    reason: selection.reason,
  });
  return selection.bundle || null;
}

function findPptArtifactBundle(state, transcriptPath, payload = null) {
  const { roots, missingRoots, taskSpecificRoots } = buildArtifactSearchRoots(state, transcriptPath, "ppt", payload);
  const bundles = new Map();
  const artifactNames = new Set(['analysis.json', 'slides.json', 'main.pptx', 'pptx_validation.json', 'README.md']);
  const hitPaths = [];

  for (const root of roots) {
    walkFiles(root, 4, (fullPath) => {
      const base = path.basename(fullPath);
      if (!artifactNames.has(base)) return;
      const dir = path.dirname(fullPath);
      const current = bundles.get(dir) || { dir, files: {}, newestMtimeMs: 0 };
      current.files[base] = fullPath;
      hitPaths.push(fullPath);
      try {
        const stat = fs.statSync(fullPath);
        current.newestMtimeMs = Math.max(current.newestMtimeMs, stat.mtimeMs);
      } catch {}
      bundles.set(dir, current);
    });
  }

  const { requiredNames, optionalNames } = pptArtifactBundleRequirements(payload);
  const scored = scoreArtifactBundles(bundles, requiredNames, optionalNames);
  const selection = selectRecoveredArtifactBundle(scored, payload, 'ppt', taskSpecificRoots);
  appendArtifactSearchLog({
    mode: 'ppt',
    transcriptPath,
    roots,
    missingRoots,
    taskSpecificRoots,
    hitCount: hitPaths.length,
    hitPaths,
    candidateCount: scored.length,
    selectedDir: selection.bundle?.dir || null,
    selectedArtifacts: selection.bundle?.files || null,
    selectedPayloadMatchScore: selection.bundle?.payloadMatchScore || 0,
    selectedPayloadMatchReason: selection.bundle?.payloadMatchReason || null,
    reason: selection.reason,
  });
  return selection.bundle || null;
}

function formatInlineCode(value) {
  if (value === null || value === undefined || value === '') return '';
  return `\`${String(value)}\``;
}

function buildRecoveredDeliverableScaffolding(mode, bundleDir, files, transcriptPath, pdfPages) {
  const artifactKind = mode === "ppt" ? "PPT" : "Beamer";
  const mainArtifactName = mode === "ppt" ? "main.pptx" : "main.tex";
  const outputArtifactName = mode === "ppt" ? "main.pptx" : "main.pdf";
  const outputArtifactPath = files[outputArtifactName] || files[mainArtifactName] || "";
  const roadmapSlide = "s02";
  const conclusionSlide = "s03";
  const appendixSlides = ["s90"];
  const mainSlides = ["s04", "s05"];
  return {
    artifact_paths: files,
    figure_coverage: {
      status: "blocked",
      blocker: `已从 ${artifactKind} 工件目录恢复到文件路径，但当前是超时恢复态，尚未完成逐图核对。`,
      source: bundleDir || outputArtifactPath || transcriptPath || "unknown",
    },
    table_coverage: {
      status: "blocked",
      blocker: `已从 ${artifactKind} 工件目录恢复到文件路径，但当前是超时恢复态，尚未完成逐表核对。`,
      source: bundleDir || outputArtifactPath || transcriptPath || "unknown",
    },
    equation_coverage: [
      {
        source_label: "recovered_artifact_bundle",
        equation_numbers: [1],
        slide_ids: [],
        status: "blocked",
        notes: `当前仅确认 ${artifactKind} 工件已落盘，尚未完成逐公式编号映射；需要续跑 programmer 补齐。`,
      },
    ],
    notation_coverage: [
      {
        symbol: "UNKNOWN_RECOVERED_SYMBOL",
        meaning: `超时恢复态下的占位记号；需要基于 ${artifactKind} 实际内容补齐正式符号定义映射。`,
        first_defined_slide_ids: ["unknown"],
        used_slide_ids: [],
        source_paragraph_ids: [],
        source_quote: "",
        source_definition_summary: "",
        defined_on_first_visible_use: false,
        status: "blocked",
        notes: `当前仅确认工件存在，尚未完成 first-use / prior-definition / source-grounded definition 级别的记号核对。`,
      },
    ],
    formal_statement_inventory: {
      status: "blocked",
      blocker: `尚未完成 theorem / proposition / lemma / corollary / definition / assumption 的逐条盘点。`,
    },
    paragraph_ledger: {
      status: "blocked",
      blocker: `尚未完成按原文顺序的 paragraph_ledger；需要为每个源段落生成一句中文摘要并映射到 slides。`,
    },
    roadmap_page: {
      status: "blocked",
      expected_slide_ids: [roadmapSlide],
      notes: "默认要求存在独立路线图页；当前恢复态尚未完成逐页核对。",
    },
    conclusion_preview_page: {
      status: "blocked",
      expected_slide_ids: [conclusionSlide],
      notes: "默认要求存在独立结论预告页；当前恢复态尚未完成逐页核对。",
    },
    body_appendix_split: {
      status: "blocked",
      body_slide_ids: mainSlides,
      appendix_slide_ids: appendixSlides,
      notes: "当前仅给出恢复态占位拆分，待续跑后按真实页计划覆盖正文/附录。",
    },
    timing_plan: {
      status: "blocked",
      no_hard_time_cap: true,
      notes: "当前不设总时长上限；如需保留 speaker_minutes，也只能作为局部讲解节奏提示，不能驱动压缩内容。",
    },
    overlay_strategy: {
      status: "blocked",
      notes: "当前仅确认需要显式说明 overlay / 页数控制策略；恢复态未完成真实核对。",
    },
    numerical_study_pages: {
      status: "blocked",
      slide_ids: [],
      notes: "需要续跑后按真实实验页补齐数值研究覆盖。",
    },
    insight_pages: {
      status: "blocked",
      slide_ids: [],
      notes: "需要续跑后按真实讲稿补齐 insight 单页覆盖。",
    },
    audience_explanation_strategy: {
      status: "blocked",
      notes: "当前仅确认需要面向未读原文听众解释；恢复态未完成受众解释深度核对。",
    },
    ready_for_review: false,
    recovered_structured_placeholder: true,
    recovery_blocker: `${artifactKind} 工件已恢复，但当前仍是超时恢复态，占位字段仅用于满足结构协议并触发下一轮精确补单。`,
    pdf_pages: pdfPages || undefined,
  };
}

function safeArray(value) {
  return Array.isArray(value) ? value : [];
}

function normalizeRecoveredSlidesDoc(slidesDoc) {
  const slides = Array.isArray(slidesDoc?.slides)
    ? slidesDoc.slides
    : (Array.isArray(slidesDoc?.slide_plan)
      ? slidesDoc.slide_plan
      : (Array.isArray(slidesDoc) ? slidesDoc : []));
  return normalizeSlideCollection(slides);
}

function buildSlideMap(slides) {
  return new Map(safeArray(slides).map((slide) => [slideIdFromPlan(slide), slide]).filter(([slideId]) => slideId));
}

function coverageTextFingerprint(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[，。；：、]/g, " ")
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function coverageFigureLabelTokens(entry) {
  if (!isPlainObject(entry)) return [];
  const raw = [
    entry.source_label,
    entry.label,
    entry.caption,
    entry.source_mention,
    entry.notes,
  ].map((item) => String(item || "")).join(" ");
  const tokens = [];
  const exact = coverageTextFingerprint(entry.source_label || entry.label || "");
  if (exact) tokens.push(exact);
  for (const match of raw.matchAll(/\b(?:Fig(?:ure)?\.?|图)\s*([0-9]+[A-Za-z]?)/gi)) {
    const number = String(match[1] || "").toLowerCase();
    if (number) {
      tokens.push(`fig ${number}`, `figure ${number}`, `图 ${number}`);
    }
  }
  return uniqueStrings(tokens.filter(Boolean));
}

function figureCoverageQualifierSatisfied(entry, haystack) {
  const label = coverageTextFingerprint(`${entry?.source_label || ""} ${entry?.label || ""} ${entry?.caption || ""}`);
  const checks = [
    ["training", ["training", "训练"]],
    ["calibration", ["calibration", "校准"]],
    ["solving", ["solving", "求解"]],
    ["trainer", ["trainer"]],
    ["solver", ["solver"]],
  ];
  for (const [needle, alternatives] of checks) {
    if (!label.includes(needle)) continue;
    if (!alternatives.some((item) => haystack.includes(item))) {
      return false;
    }
  }
  return true;
}

function slideHasVisibleFigureForCoverageEntry(slide, entry) {
  if (!isPlainObject(slide)) return false;
  const blocks = safeArray(slide.blocks);
  const tokens = coverageFigureLabelTokens(entry);
  return blocks.some((block) => {
    if (!isPlainObject(block) || String(block.type || "").trim() !== "figure") return false;
    const figurePath = String(block.path || block.asset_path || block.file || "").trim();
    if (!figurePath || /^https?:\/\//i.test(figurePath)) return false;
    const haystack = coverageTextFingerprint([
      block.label,
      block.caption,
      block.reader_note,
      block.text,
    ].map((item) => String(item || "")).join(" "));
    if (!figureCoverageQualifierSatisfied(entry, haystack)) return false;
    if (tokens.length === 0 || !haystack) return true;
    return tokens.some((token) => haystack.includes(token));
  });
}

function visibleFigureSlideIdsForCoverageEntry(entry, slideMap) {
  if (!isPlainObject(entry) || !slideMap || slideMap.size === 0) return [];
  const declaredSlideIds = recoveredSlideIdsFromStructuredField(entry, slideMap);
  const candidateSlides = declaredSlideIds.length > 0
    ? declaredSlideIds.map((slideId) => [slideId, slideMap.get(slideId)]).filter(([, slide]) => slide)
    : [...slideMap.entries()];
  return uniqueStrings(candidateSlides
    .filter(([, slide]) => slideHasVisibleFigureForCoverageEntry(slide, entry))
    .map(([slideId]) => slideId));
}

function normalizeFigureCoverageEntriesWithVisibleSlides(value, slideMap = null) {
  if (!slideMap || slideMap.size === 0) return value;
  const normalizeEntry = (entry) => {
    if (!isPlainObject(entry)) return entry;
    let next = entry;
    for (const key of structuredCoverageNestedArrayKeys()) {
      if (!Array.isArray(entry[key])) continue;
      const nested = entry[key].map((item) => normalizeEntry(item));
      if (nested.some((item, index) => item !== entry[key][index])) {
        next = next === entry ? { ...entry } : next;
        next[key] = nested;
      }
    }
    const visibleSlideIds = visibleFigureSlideIdsForCoverageEntry(next, slideMap);
    if (visibleSlideIds.length === 0) return next;
    const status = normalizeCoverageStatus(next.status || "");
    const unresolved = /^(planned|analysis_only|blocked|missing|partial)$/i.test(status);
    const currentSlideIds = safeArray(next.slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
    const currentSlideIdsAreVisible = currentSlideIds.length > 0
      && currentSlideIds.every((slideId) => visibleSlideIds.includes(slideId));
    if (!unresolved && currentSlideIdsAreVisible) return next;
    return {
      ...next,
      slide_ids: visibleSlideIds,
      status: "covered",
      notes: appendStructuredNoteLine(
        next.notes || "",
        "已从 slides.json 中真实 figure block 和本地图片路径恢复可见图覆盖。"
      ),
    };
  };
  if (Array.isArray(value)) {
    const normalized = value.map((entry) => normalizeEntry(entry));
    return normalized.some((entry, index) => entry !== value[index]) ? normalized : value;
  }
  if (isPlainObject(value)) return normalizeEntry(value);
  return value;
}

function slideKindsMatching(slides, predicate) {
  return safeArray(slides).filter((slide) => predicate(
    String(slide?.slide_kind || slide?.kind || slide?.page_role || "").trim().toLowerCase(),
    slide
  ));
}

function labelsToEquationNumbers(labels) {
  const numbers = [];
  const appendixNumbers = [];
  for (const label of safeArray(labels)) {
    const text = String(label || "").trim();
    if (!text) continue;
    const appendixMatch = text.match(/A0*([1-9]\d*)$/i);
    if (appendixMatch) {
      appendixNumbers.push(`A${Number(appendixMatch[1])}`);
      continue;
    }
    const match = text.match(/(\d+)(?:\.(\d+))?$/);
    if (!match) continue;
    if (match[2]) {
      numbers.push(Number(`${match[1]}${match[2]}`));
    } else {
      numbers.push(Number(match[1]));
    }
  }
  return uniqueCanonicalEquationNumbers([
    ...uniqueSortedPositiveIntegers(numbers),
    ...appendixNumbers,
  ]);
}

function explicitRecoveredZeroCountFromAnalysis(analysisDoc, candidateKeys = []) {
  for (const key of safeArray(candidateKeys)) {
    const numeric = Number(analysisDoc?.[key]);
    if (Number.isFinite(numeric)) {
      return numeric;
    }
  }
  return null;
}

function recoveredInventoryItems(value) {
  if (Array.isArray(value)) {
    return value;
  }
  if (isPlainObject(value)) {
    for (const key of ["items", "tables", "source_tables", "table_items", "caption_items", "ordered_mentions", "mentions", "source_mentions"]) {
      if (Array.isArray(value[key])) return value[key];
    }
  }
  return [];
}

function recoveredInventoryTotal(value) {
  if (!isPlainObject(value)) {
    return null;
  }
  const numericCandidates = [
    value.total_source_items,
    value.total_items,
    value.total_source_table_blocks,
    value.total_source_mentions,
    value.total_unique_tables,
    value.total_mentions,
    value.unique_table_blocks,
    value.source_mentions_total,
    value.source_table_count,
    value.table_count,
    value.tables_count,
    value.count,
    value.total,
  ];
  for (const candidate of numericCandidates) {
    const numeric = Number(candidate);
    if (Number.isFinite(numeric)) {
      return numeric;
    }
  }
  if (Array.isArray(value.items)) {
    return value.items.length;
  }
  return null;
}

function buildRecoveredFigureCoverage(analysisDoc, slidesDoc = null, options = {}) {
  const recoveredSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const slideMap = recoveredSlides.length > 0 ? buildSlideMap(recoveredSlides) : null;
  const requireVisibleFigureBlocks = options.requireVisibleFigureBlocks === true;
  const normalizeFigureCoverageForMode = (value) => requireVisibleFigureBlocks
    ? normalizeFigureCoverageEntriesWithVisibleSlides(value, slideMap)
    : normalizeFinalCoverageEntriesWithSlideIds(value, slideMap);
  const slidesCoverage = normalizeFigureCoverageForMode(
    normalizeCoverageStatusEntries(deepCloneJson(slidesDoc?.figure_coverage))
  );
  if (isNonEmptyStructuredValue(slidesCoverage) && !structuredCoverageValueHasUnresolvedStatus(slidesCoverage)) {
    return slidesCoverage;
  }
  const existingCoverage = normalizeFigureCoverageForMode(
    normalizeCoverageStatusEntries(deepCloneJson(analysisDoc?.figure_coverage))
  );
  if (isNonEmptyStructuredValue(existingCoverage) && !structuredCoverageValueHasUnresolvedStatus(existingCoverage)) {
    return existingCoverage;
  }
  const inventory = recoveredInventoryItems(analysisDoc?.figure_inventory);
  if (inventory.length === 0) {
    const explicitFigureCount = explicitRecoveredZeroCountFromAnalysis(analysisDoc, [
      "figure_count",
      "figures_count",
      "figure_total",
      "figures_total",
      "source_figure_count",
      "source_figures",
    ]);
    const recoveredInventoryCount = recoveredInventoryTotal(analysisDoc?.figure_inventory);
    const recoveredCoverageCount = recoveredInventoryTotal(analysisDoc?.figure_coverage);
    if (explicitFigureCount === 0 || recoveredInventoryCount === 0 || recoveredCoverageCount === 0) {
      return {
        status: "covered",
        total_source_items: 0,
        covered_items: 0,
        slide_ids: [],
        notes: "analysis.json 已把 Figure 库存明确记录为 0；当前源文范围内没有需要逐项映射的显式 Figure。",
      };
    }
    return { status: "blocked", blocker: "analysis.json 中未找到 figure_inventory。" };
  }
  return inventory.map((item, index) => {
    const visibleSlideIds = requireVisibleFigureBlocks
      ? visibleFigureSlideIdsForCoverageEntry(item, slideMap)
      : recoveredSlideIdsFromStructuredField(item, slideMap);
    return {
      source_label: String(item?.source_label || `Fig. ${index + 1}`).trim(),
      caption: String(item?.caption || "").trim(),
      slide_ids: visibleSlideIds,
      asset_path: String(item?.asset_path || "").trim(),
      status: visibleSlideIds.length > 0 || !slideMap ? "covered" : "blocked",
      notes: visibleSlideIds.length > 0
        ? (requireVisibleFigureBlocks
          ? "原图已作为真实 figure block 纳入讲稿覆盖。"
          : "原图已纳入讲稿覆盖。")
        : String(item?.status || (requireVisibleFigureBlocks
          ? "未在 slides.json 中找到对应的可见 figure block。"
          : "未在 slides.json 中找到对应 slide 映射。")).trim(),
    };
  });
}

function structuredCoverageNestedArrayKeys() {
  return [
    "items",
    "entries",
    "coverage",
    "mappings",
    "figures",
    "tables",
    "mentions",
    "ordered_mentions",
    "source_items",
    "source_mentions",
    "mapped_mentions",
    "statements",
    "formal_statements",
    "propositions",
    "lemmas",
    "theorems",
    "corollaries",
    "definitions",
    "assumptions",
    "remarks",
    "other",
    "numerical_studies",
    "insights",
    "pages",
  ];
}

function slideIdsFromNestedCoverageEntries(value, slideMap = null) {
  if (Array.isArray(value)) {
    return uniqueStrings(value.flatMap((entry) => slideIdsFromNestedCoverageEntries(entry, slideMap)));
  }
  if (!isPlainObject(value)) return [];
  const direct = recoveredSlideIdsFromStructuredField(value, slideMap);
  const nested = [];
  for (const key of structuredCoverageNestedArrayKeys()) {
    if (Array.isArray(value[key])) {
      nested.push(...slideIdsFromNestedCoverageEntries(value[key], slideMap));
    }
  }
  return uniqueStrings([...direct, ...nested]);
}

function normalizeFinalCoverageEntriesWithSlideIds(value, slideMap = null) {
  if (Array.isArray(value)) {
    let changedAny = false;
    const entries = value.map((entry) => {
      if (!isPlainObject(entry)) return entry;
      const normalizedEntry = normalizeFinalCoverageEntriesWithSlideIds(entry, slideMap);
      const entryChanged = normalizedEntry !== entry;
      const candidateEntry = entryChanged ? normalizedEntry : entry;
      const slideIds = slideIdsFromNestedCoverageEntries(candidateEntry, slideMap);
      const status = normalizeCoverageStatus(entry.status || "");
      const unresolved = /^(planned|analysis_only|blocked|missing|partial)$/i.test(status);
      const currentSlideIds = safeArray(candidateEntry.slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
      const currentSlideIdsAreReal = currentSlideIds.length > 0
        && currentSlideIds.every((slideId) => !slideMap || slideMap.has(slideId));
      if (slideIds.length === 0 || (!unresolved && currentSlideIdsAreReal)) {
        if (entryChanged) changedAny = true;
        return candidateEntry;
      }
      changedAny = true;
      return {
        ...candidateEntry,
        slide_ids: slideIds,
        status: "covered",
      };
    });
    return changedAny ? entries : value;
  }
  if (!isPlainObject(value)) return value;
  let next = value;
  for (const key of structuredCoverageNestedArrayKeys()) {
    if (!Array.isArray(value[key])) continue;
    const normalizedNested = normalizeFinalCoverageEntriesWithSlideIds(value[key], slideMap);
    if (normalizedNested !== value[key]) {
      if (next === value) next = { ...value };
      next[key] = normalizedNested;
    }
  }
  const slideIds = slideIdsFromNestedCoverageEntries(next, slideMap);
  const status = normalizeCoverageStatus(value.status || "");
  const unresolved = /^(planned|analysis_only|blocked|missing|partial)$/i.test(status);
  const currentSlideIds = safeArray(next.slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
  const currentSlideIdsAreReal = currentSlideIds.length > 0
    && currentSlideIds.every((slideId) => !slideMap || slideMap.has(slideId));
  if (slideIds.length === 0 || (!unresolved && currentSlideIdsAreReal)) {
    return next;
  }
  return {
    ...next,
    slide_ids: slideIds,
    status: "covered",
  };
}

function buildRecoveredTableCoverage(analysisDoc, slidesDoc = null) {
  const recoveredSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const slideMap = recoveredSlides.length > 0 ? buildSlideMap(recoveredSlides) : null;
  const slidesCoverage = normalizeFinalCoverageEntriesWithSlideIds(
    normalizeCoverageStatusEntries(deepCloneJson(slidesDoc?.table_coverage)),
    slideMap
  );
  if (
    isNonEmptyStructuredValue(slidesCoverage)
    && (tableCoverageHasRealSlideIds(slidesCoverage, slideMap) || tableCoverageIsExplicitZeroInventory(slidesCoverage))
  ) {
    return slidesCoverage;
  }
  const existingCoverage = normalizeFinalCoverageEntriesWithSlideIds(
    normalizeCoverageStatusEntries(deepCloneJson(analysisDoc?.table_coverage)),
    slideMap
  );
  if (
    isNonEmptyStructuredValue(existingCoverage)
    && (tableCoverageHasRealSlideIds(existingCoverage, slideMap) || tableCoverageIsExplicitZeroInventory(existingCoverage))
  ) {
    return existingCoverage;
  }
  const inventory = recoveredInventoryItems(analysisDoc?.table_inventory);
  if (inventory.length === 0) {
    const explicitTableCount = explicitRecoveredZeroCountFromAnalysis(analysisDoc, [
      "table_count",
      "tables_count",
      "table_total",
      "tables_total",
      "source_table_count",
      "source_tables",
    ]);
    const recoveredInventoryCount = recoveredInventoryTotal(analysisDoc?.table_inventory);
    const recoveredCoverageCount = recoveredInventoryTotal(analysisDoc?.table_coverage);
    if (explicitTableCount === 0 || recoveredInventoryCount === 0 || recoveredCoverageCount === 0) {
      return {
        status: "covered",
        total_source_items: 0,
        covered_items: 0,
        slide_ids: [],
        notes: "analysis.json 已把 Table 库存明确记录为 0；当前源文范围内没有需要逐项映射的显式 Table。",
      };
    }
    return { status: "blocked", blocker: "analysis.json 中未找到 table_inventory。" };
  }
  return inventory.map((item, index) => ({
    source_label: String(item?.source_label || item?.table_id || item?.source_mention || `Table ${index + 1}`).trim(),
    caption: String(item?.caption || "").trim(),
    slide_ids: recoveredSlideIdsFromStructuredField(item, slideMap),
    status: recoveredSlideIdsFromStructuredField(item, slideMap).length > 0 || !slideMap ? "covered" : "blocked",
    notes: String(item?.status || "表格已纳入讲稿覆盖").trim(),
  }));
}

function buildRecoveredEquationCoverage(analysisDoc, slideMap) {
  const inventory = safeArray(analysisDoc?.equations);
  if (inventory.length === 0) {
    return [{
      source_label: "analysis_equations_missing",
      equation_numbers: [1],
      slide_ids: [],
      status: "blocked",
      notes: "analysis.json 中未找到 equations，无法恢复逐公式映射。",
    }];
  }
  const artifactPaths = isPlainObject(analysisDoc?.artifact_paths) ? analysisDoc.artifact_paths : {};
  const mainTexPath = isNonEmptyString(artifactPaths["main.tex"]) ? String(artifactPaths["main.tex"]).trim() : "";
  let frameLookup = null;
  if (mainTexPath && fs.existsSync(mainTexPath)) {
    try {
      frameLookup = buildFrameLookup(parseMainTexFrames(fs.readFileSync(mainTexPath, "utf8")));
    } catch {
      frameLookup = null;
    }
  }
  return inventory.map((item, index) => {
    const slideIds = uniqueStrings([
      ...safeArray(item?.planned_slides),
      ...safeArray(item?.slides),
      ...safeArray(item?.slide_ids),
    ].map((v) => String(v || "").trim()).filter(Boolean));
    const labelText = String(item?.label || item?.range || item?.source_label || item?.role || "").trim();
    const numbers = labelsToEquationNumbers(labelText);
    const visibleSlides = slideIds.filter((slideId) => slideMap.has(slideId));
    const sourceLabel = String(item?.source_label || labelText || item?.role || `equation_group_${index + 1}`).trim();
    const slideFieldName = safeArray(item?.planned_slides).length > 0
      ? "planned_slides"
      : (safeArray(item?.slides).length > 0 ? "slides" : "slide_ids");
    const mappedFrames = frameLookup
      ? visibleSlides.map((slideId) => {
        const slide = slideMap.get(slideId);
        return slide ? findFrameForSlide(slide, frameLookup, { allowOrdinalFallback: false }) : null;
      }).filter(Boolean)
      : [];
    const hasRenderedTagEvidence = numbers.length > 0 && mappedFrames.some((frame) => frameContainsEquationKeys(frame, numbers));
    return {
      source_label: sourceLabel || `equation_group_${index + 1}`,
      equation_numbers: numbers.length > 0 ? numbers : [index + 1],
      slide_ids: visibleSlides,
      status: visibleSlides.length > 0 && hasRenderedTagEvidence ? "covered" : "partial",
      notes: visibleSlides.length > 0
        ? (
          hasRenderedTagEvidence
            ? `按 analysis.json 的 ${slideFieldName} 恢复，共映射到 ${visibleSlides.join("、")}，且 main.tex 中检测到对应编号公式标签。`
            : `analysis.json 的 ${slideFieldName} 映射到了 ${visibleSlides.join("、")}，但 main.tex 未检测到对应编号公式标签，暂不提升为 covered。`
        )
        : `analysis.json 提供了 ${labelText || sourceLabel || `公式分组 ${index + 1}`}，但未能在 slides.json 中找到对应 slide。`,
    };
  });
}

function buildRecoveredNotationCoverage(slides) {
  const symbolToEntry = new Map();
  for (const slide of safeArray(slides)) {
    const slideId = slideIdFromPlan(slide);
    if (!slideId) continue;
    for (const block of equationBlocksFromSlide(slide)) {
      const sourceText = `${block.label || ""}\n${block.latex || ""}\n${block.explanation || ""}`;
      const sourceParagraphIds = safeArray(slide.source_paragraph_ids ?? slide.paragraph_ids)
        .map((item) => String(item || "").trim())
        .filter(Boolean);
      const sourceQuote = String(block.latex || block.text || block.label || "").trim();
      const definitionSummary = String(block.explanation || block.caption || block.notes || "").trim()
        || `符号出现在 ${slideId} 的可见公式块中。`;
      for (const symbol of extractLikelyMathSymbolsFromEquationText(sourceText)) {
        if (!symbolToEntry.has(symbol)) {
          symbolToEntry.set(symbol, {
            symbol,
            meaning: definitionSummary,
            first_defined_slide_ids: [slideId],
            used_slide_ids: [slideId],
            source_paragraph_ids: sourceParagraphIds.length > 0 ? sourceParagraphIds : ["slides_json_equation_block"],
            source_quote: sourceQuote || `${symbol} visible on ${slideId}`,
            source_definition_summary: definitionSummary,
            defined_on_first_visible_use: true,
            status: "defined",
            notes: "由 slides.json 中可见公式块、latex 与解释自动恢复为首现定义条目。",
          });
          continue;
        }
        const entry = symbolToEntry.get(symbol);
        if (!entry.used_slide_ids.includes(slideId)) {
          entry.used_slide_ids.push(slideId);
        }
        for (const paragraphId of sourceParagraphIds) {
          if (!entry.source_paragraph_ids.includes(paragraphId)) {
            entry.source_paragraph_ids.push(paragraphId);
          }
        }
        if (!isNonEmptyString(entry.source_quote) && sourceQuote) {
          entry.source_quote = sourceQuote;
        }
        if (!isNonEmptyString(entry.source_definition_summary) && definitionSummary) {
          entry.source_definition_summary = definitionSummary;
          entry.meaning = definitionSummary;
        }
      }
    }
  }
  if (symbolToEntry.size === 0) {
    return [{
      symbol: "UNKNOWN_RECOVERED_SYMBOL",
      meaning: "未能从 slides.json 的公式块中自动提取显式符号。",
      first_defined_slide_ids: ["s01"],
      used_slide_ids: ["s01"],
      source_paragraph_ids: [],
      source_quote: "",
      source_definition_summary: "",
      defined_on_first_visible_use: false,
      status: "blocked",
      notes: "需要后续 programmer 基于讲稿正文与原文定义句补齐 notation 覆盖。",
    }];
  }
  return [...symbolToEntry.values()].sort((a, b) => parseSlideOrdinal(a.first_defined_slide_ids[0]) - parseSlideOrdinal(b.first_defined_slide_ids[0]));
}

function buildNotationVisibilityLookup(slidesDoc, artifactPaths = null) {
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (slides.length === 0) {
    return null;
  }
  let mainTexPath = isPlainObject(artifactPaths)
    ? resolveArtifactPathFromReport(artifactPaths, "main.tex")
    : "";
  if (!isNonEmptyString(mainTexPath) || !fs.existsSync(mainTexPath)) {
    const outputDirectory = isPlainObject(artifactPaths) ? inferArtifactOutputDirectoryFromMap(artifactPaths) : "";
    const inferredCandidates = [
      outputDirectory ? path.join(outputDirectory, "main.tex") : "",
      isPlainObject(artifactPaths) && isNonEmptyString(artifactPaths["analysis.json"]) ? path.join(path.dirname(artifactPaths["analysis.json"]), "main.tex") : "",
      isPlainObject(artifactPaths) && isNonEmptyString(artifactPaths["slides.json"]) ? path.join(path.dirname(artifactPaths["slides.json"]), "main.tex") : "",
    ].filter(Boolean);
    mainTexPath = inferredCandidates.find((candidate) => fs.existsSync(candidate)) || "";
  }
  let frameWindows = null;
  if (isNonEmptyString(mainTexPath) && fs.existsSync(mainTexPath)) {
    const frames = parseMainTexFrames(fs.readFileSync(mainTexPath, "utf8"));
    const frameLookup = buildFrameLookup(frames);
    frameWindows = buildOrderedSlideFrameWindows(slides, frameLookup);
  }
  const slideEntries = slides
    .map((slide) => {
      const slideId = slideIdFromPlan(slide);
      if (!slideId) return null;
      const frameText = frameWindows
        ? framesForSlideId(slideId, frameWindows).map((frame) => String(frame?.body || "")).join("\n")
        : "";
      return {
        slide,
        slideId,
        text: `${slideVisibleTextFromPlan(slide)}\n${frameText}`,
        sourceParagraphIds: sourceParagraphIdsFromSlide(slide),
      };
    })
    .filter(Boolean)
    .sort((a, b) => parseSlideOrdinal(a.slideId) - parseSlideOrdinal(b.slideId));
  return {
    visibleSlideIdsForCandidates(candidates, options = {}) {
      const normalizedCandidates = safeArray(candidates).map(canonicalizeSymbolToken).filter(Boolean);
      if (normalizedCandidates.length === 0) return [];
      const exactSymbol = canonicalizeSymbolToken(options.exactSymbol || "");
      return slideEntries
        .filter((entry) => {
          const exactVisible = exactSymbol && textContainsSymbolCandidate(exactSymbol, entry.text);
          if (exactVisible) return true;
          const candidatePool = exactSymbol
            ? normalizedCandidates.filter((candidate) => candidate !== exactSymbol)
            : normalizedCandidates;
          if (candidatePool.length === 0) return false;
          const equationText = equationBlocksFromSlide(entry.slide)
            .map((block) => `${block.label || ""}\n${block.latex || ""}\n${block.explanation || ""}`)
            .join("\n");
          return candidatePool.some((candidate) => textContainsSymbolCandidate(candidate, equationText));
        })
        .map((entry) => entry.slideId);
    },
    firstSourceParagraphIds(slideId) {
      return slideEntries.find((entry) => entry.slideId === slideId)?.sourceParagraphIds || [];
    },
  };
}

function repairNotationCoverageAgainstVisibleSlides(entries, slidesDoc, artifactPaths = null) {
  const lookup = buildNotationVisibilityLookup(slidesDoc, artifactPaths);
  if (!lookup) {
    return sanitizeNotationCoverageEntries(normalizeCoverageStatusEntries(entries));
  }
  const bySymbol = new Map();
  for (const rawEntry of safeArray(normalizeCoverageStatusEntries(entries))) {
    if (!isPlainObject(rawEntry)) continue;
    const symbol = normalizeNotationSymbolText(rawEntry.symbol ?? rawEntry.term ?? rawEntry.notation ?? rawEntry.variable ?? rawEntry.abbreviation ?? "");
    if (!symbol || /UNKNOWN_RECOVERED_SYMBOL/i.test(symbol)) continue;
    const candidates = symbolCandidatesFromNotationEntry(symbol);
    const visibleSlideIds = lookup.visibleSlideIdsForCandidates(candidates, { exactSymbol: symbol });
    if (visibleSlideIds.length === 0) continue;
    const firstVisibleSlideId = visibleSlideIds[0];
    const sourceParagraphIds = uniqueStrings([
      ...notationSourceParagraphIds(rawEntry),
      ...lookup.firstSourceParagraphIds(firstVisibleSlideId),
    ].filter((item) => !notationCoverageIdIsPlaceholder(item)));
    const status = normalizeCoverageStatus(rawEntry.status || "defined") || "defined";
    const resolvedStatus = /^(blocked|missing|partial|planned|analysis_only)$/i.test(status) ? "defined" : status;
    const repairedEntry = {
      ...rawEntry,
      symbol,
      meaning: String(rawEntry.meaning ?? rawEntry.definition ?? rawEntry.explanation ?? "").trim()
        || notationSourceDefinitionSummary(rawEntry)
        || `${symbol} 在 ${firstVisibleSlideId} 首次可见。`,
      first_defined_slide_ids: [firstVisibleSlideId],
      used_slide_ids: visibleSlideIds,
      source_paragraph_ids: sourceParagraphIds.length > 0 ? sourceParagraphIds : [`visible_${firstVisibleSlideId}`],
      source_quote: notationSourceQuote(rawEntry) || `${symbol} visible on ${firstVisibleSlideId}`,
      source_definition_summary: notationSourceDefinitionSummary(rawEntry) || `${symbol} 在 ${firstVisibleSlideId} 的可见公式或正文中出现，并在该页作为首个可见用例登记。`,
      defined_on_first_visible_use: true,
      status: resolvedStatus,
      notes: String(rawEntry.notes || "notation_coverage 已按 slides.json/main.tex 中真实可见位置自动收敛。").trim(),
    };
    const existing = bySymbol.get(symbol);
    if (!existing || parseSlideOrdinal(firstVisibleSlideId) < parseSlideOrdinal(existing.first_defined_slide_ids?.[0])) {
      bySymbol.set(symbol, repairedEntry);
    }
  }
  return sanitizeNotationCoverageEntries([...bySymbol.values()]).sort(
    (a, b) => parseSlideOrdinal(safeArray(a.first_defined_slide_ids)[0]) - parseSlideOrdinal(safeArray(b.first_defined_slide_ids)[0])
  );
}

function mergeVisibleRecoveredNotationCoverage(primaryEntries, recoveredEntries) {
  const bySymbol = new Map();
  for (const entry of safeArray(primaryEntries)) {
    if (!isPlainObject(entry)) continue;
    const symbol = String(entry.symbol || "").trim();
    if (symbol) bySymbol.set(symbol, entry);
  }
  for (const entry of safeArray(recoveredEntries)) {
    if (!isPlainObject(entry)) continue;
    const symbol = String(entry.symbol || "").trim();
    if (!symbol || bySymbol.has(symbol)) continue;
    bySymbol.set(symbol, entry);
  }
  return sanitizeNotationCoverageEntries([...bySymbol.values()]).sort(
    (a, b) => parseSlideOrdinal(safeArray(a.first_defined_slide_ids)[0]) - parseSlideOrdinal(safeArray(b.first_defined_slide_ids)[0])
  );
}

function notationCoverageIdIsPlaceholder(value) {
  const raw = String(value || "").trim();
  if (!raw) return true;
  return /^(待规划|待补|待映射|未规划|未映射|pending|todo|unmapped|unassigned|analysis_phase1|phase[_ -]?1_placeholder)$/i.test(raw);
}

function notationEntryIsRecoveryPlaceholder(entry) {
  if (!isPlainObject(entry)) return true;
  const symbol = String(entry.symbol || "").trim();
  if (!symbol || /UNKNOWN_RECOVERED_SYMBOL/i.test(symbol)) return true;
  const firstDefined = safeArray(entry.first_defined_slide_ids)
    .map((item) => String(item || "").trim())
    .filter((item) => item && !notationCoverageIdIsPlaceholder(item));
  const used = safeArray(entry.used_slide_ids)
    .map((item) => String(item || "").trim())
    .filter((item) => item && !notationCoverageIdIsPlaceholder(item));
  const sourceParagraphIds = notationSourceParagraphIds(entry)
    .filter((item) => !notationCoverageIdIsPlaceholder(item));
  const sourceQuote = notationSourceQuote(entry);
  const sourceDefinitionSummary = notationSourceDefinitionSummary(entry);
  const status = String(entry.status || "").trim();
  return firstDefined.length === 0
    || used.length === 0
    || sourceParagraphIds.length === 0
    || !sourceQuote
    || !sourceDefinitionSummary
    || entry.defined_on_first_visible_use !== true
    || /^(blocked|missing|partial|planned|analysis_only)$/i.test(status);
}

function normalizeNotationCoverageSlideOrder(firstDefinedSlideIds, usedSlideIds, definedOnFirstVisibleUse) {
  const firstDefined = uniqueStrings(
    safeArray(firstDefinedSlideIds)
      .map((item) => String(item || "").trim())
      .filter((item) => item && !notationCoverageIdIsPlaceholder(item))
  );
  const used = uniqueStrings(
    safeArray(usedSlideIds)
      .map((item) => String(item || "").trim())
      .filter((item) => item && !notationCoverageIdIsPlaceholder(item))
  );
  if (definedOnFirstVisibleUse !== true || firstDefined.length === 0 || used.length === 0) {
    return { firstDefined, used };
  }
  const definedOrdinals = firstDefined.map(parseSlideOrdinal).filter(Number.isFinite);
  if (definedOrdinals.length === 0) {
    return { firstDefined, used };
  }
  const earliestDefinition = Math.min(...definedOrdinals);
  return {
    firstDefined,
    used: used.filter((slideId) => {
      const ordinal = parseSlideOrdinal(slideId);
      return !Number.isFinite(ordinal) || ordinal >= earliestDefinition;
    }),
  };
}

function sanitizeNotationCoverageEntries(entries) {
  return safeArray(entries)
    .map((entry) => {
      if (!isPlainObject(entry)) return null;
      const definedOnFirstVisibleUse = entry.defined_on_first_visible_use === true;
      const { firstDefined, used } = normalizeNotationCoverageSlideOrder(
        entry.first_defined_slide_ids,
        entry.used_slide_ids,
        definedOnFirstVisibleUse
      );
      return {
        ...entry,
        symbol: normalizeNotationSymbolText(entry.symbol ?? entry.term ?? entry.notation ?? ""),
        meaning: String(entry.meaning ?? entry.definition ?? entry.explanation ?? "").trim(),
        first_defined_slide_ids: firstDefined,
        used_slide_ids: used,
        source_paragraph_ids: uniqueStrings(
          notationSourceParagraphIds(entry)
            .filter((item) => !notationCoverageIdIsPlaceholder(item))
        ),
        source_quote: notationSourceQuote(entry),
        source_definition_summary: notationSourceDefinitionSummary(entry),
        defined_on_first_visible_use: definedOnFirstVisibleUse,
      };
    })
    .filter((entry) => !notationEntryIsRecoveryPlaceholder(entry));
}

function buildRecoveredFormalInventory(analysisDoc, slidesDoc = null) {
  const recoveredSlides = normalizeRecoveredSlidesDoc(slidesDoc);
  const slideMap = recoveredSlides.length > 0 ? buildSlideMap(recoveredSlides) : null;
  for (const value of [
    slidesDoc?.formal_statement_inventory,
    analysisDoc?.formal_statement_inventory,
    slidesDoc?.formal_statements,
    analysisDoc?.formal_statements,
  ]) {
    const normalized = normalizeFinalCoverageEntriesWithSlideIds(
      normalizeCoverageStatusEntries(deepCloneJson(value)),
      slideMap
    );
    if (isNonEmptyStructuredValue(normalized) && !structuredCoverageValueHasUnresolvedStatus(normalized)) {
      return normalized;
    }
  }

  const slidesInventory = safeArray(slidesDoc?.formal_statement_inventory);
  const directInventory = safeArray(analysisDoc?.formal_statement_inventory);
  const fallbackInventory = safeArray(analysisDoc?.formal_statements);
  const inventory = slidesInventory.length > 0
    ? slidesInventory
    : (directInventory.length > 0 ? directInventory : fallbackInventory);
  if (inventory.length === 0) {
    const explicitFormalCount = explicitRecoveredZeroCountFromAnalysis(analysisDoc, [
      "formal_statement_count",
      "formal_statements_count",
      "formal_count",
      "source_formal_statement_count",
      "source_formal_statements",
    ]);
    if (explicitFormalCount === 0) {
      return {
        status: "covered",
        total_source_items: 0,
        propositions: [],
        lemmas: [],
        theorems: [],
        corollaries: [],
        definitions: [],
        assumptions: [],
        remarks: [],
        other: [],
        notes: "analysis.json 明确记录 formal_statement_count=0；当前源文范围内未检出标题化 formal statements。",
      };
    }
    return { status: "blocked", blocker: "analysis.json/slides.json 中未找到 formal_statement_inventory / formal_statements。" };
  }

  const grouped = {};
  const ensureBucket = (bucket) => {
    if (!grouped[bucket]) grouped[bucket] = [];
    return grouped[bucket];
  };
  const classifyFormalBucket = (text) => {
    const raw = String(text || "").trim().toLowerCase();
    if (/proposition/.test(raw) || /命题/.test(raw)) return "propositions";
    if (/lemma/.test(raw) || /引理/.test(raw)) return "lemmas";
    if (/theorem/.test(raw) || /定理/.test(raw)) return "theorems";
    if (/corollary/.test(raw) || /推论/.test(raw)) return "corollaries";
    if (/definition/.test(raw) || /定义/.test(raw)) return "definitions";
    if (/assumption/.test(raw) || /假设/.test(raw)) return "assumptions";
    if (/remark/.test(raw) || /注记|备注/.test(raw)) return "remarks";
    return "other";
  };
  const labelFromItem = (item, parent, fallback) => {
    const raw = [
      item?.label,
      item?.statement_id,
      item?.id,
      item?.title,
      item?.kind,
      item?.type,
      parent?.label,
      parent?.kind,
      item?.source_text,
    ].map((part) => String(part || "").trim()).find(Boolean);
    return raw || fallback;
  };
  const normalizeFormalEntry = (item, parent, fallbackLabel) => {
    const slideIds = uniqueStrings([
      ...recoveredSlideIdsFromStructuredField(item, slideMap),
      ...(recoveredSlideIdsFromStructuredField(item, slideMap).length > 0 ? [] : recoveredSlideIdsFromStructuredField(parent, slideMap)),
    ]);
    const rawStatus = normalizeCoverageStatus(item?.status || parent?.status || "");
    const status = slideIds.length > 0
      ? "covered"
      : (slideMap ? (rawStatus && !coverageStatusIsUnresolved(rawStatus) ? rawStatus : "blocked") : (rawStatus || "covered"));
    return {
      label: labelFromItem(item, parent, fallbackLabel),
      statement_id: String(item?.statement_id || item?.id || item?.label || fallbackLabel || "").trim(),
      type: String(item?.type || item?.kind || parent?.type || parent?.kind || "formal_statement").trim(),
      slide_ids: slideIds,
      source_paragraph_ids: uniqueStrings([
        ...safeArray(item?.source_paragraph_ids),
        ...safeArray(parent?.source_paragraph_ids),
      ].map((v) => String(v || "").trim()).filter(Boolean)),
      translation_policy: String(item?.translation_policy || parent?.translation_policy || "").trim(),
      status,
      source_text: String(item?.source_text || parent?.source_text || "").trim(),
      original_meaning_cn: String(item?.original_meaning_cn || parent?.original_meaning_cn || "").trim(),
      notes: String(item?.notes || parent?.notes || (slideIds.length > 0 ? "已从真实 slides.json 页面恢复 formal statement 映射。" : "未能把 formal statement 绑定到真实 slide_id。")).trim(),
    };
  };

  for (const [index, item] of inventory.entries()) {
    const kindText = [item?.kind, item?.type, item?.label, item?.title, item?.source_text].filter(Boolean).join(" ");
    const bucket = classifyFormalBucket(kindText);

    if (Array.isArray(item?.items) && item.items.length > 0) {
      for (const [childIndex, child] of item.items.entries()) {
        const childKindText = [child?.kind, child?.type, child?.label, child?.title, child?.source_text, item?.kind].filter(Boolean).join(" ");
        const childBucket = classifyFormalBucket(childKindText);
        ensureBucket(childBucket).push(normalizeFormalEntry(child, item, `${childBucket}_${childIndex + 1}`));
      }
      continue;
    }

    ensureBucket(bucket).push(normalizeFormalEntry(item, null, `${bucket}_${index + 1}`));
  }

  return Object.keys(grouped).length > 0
    ? grouped
    : { status: "blocked", blocker: "analysis.json/slides.json 中的 formal statement 信息为空。" };
}

function buildRecoveredRoadmapPage(slides, slidesDoc = null) {
  const slideMap = buildSlideMap(slides);
  const declaredSlideIds = recoveredSlideIdsFromStructuredField(slidesDoc?.roadmap_page, slideMap);
  if (declaredSlideIds.length > 0) {
    return {
      status: "covered",
      slide_ids: declaredSlideIds,
      notes: `直接采用 slides.json 顶层 roadmap_page：${recoveredSlideNotesFromIds(declaredSlideIds, slideMap)}`,
    };
  }
  const matches = slideKindsMatching(slides, (kind, slide) => {
    const slideId = slideIdFromPlan(slide);
    const title = String(slide?.title || "");
    const section = String(slide?.section || "");
    return kind === "roadmap"
      || /roadmap/i.test(slideId)
      || /roadmap/i.test(title)
      || /路线图|汇报路线/.test(title)
      || /路线图|汇报路线/.test(section);
  });
  return matches.length > 0
    ? {
        status: "covered",
        slide_ids: matches.map((slide) => slideIdFromPlan(slide)),
        notes: matches.map((slide) => `${slideIdFromPlan(slide)}: ${String(slide?.title || "").trim()}`).join("；"),
      }
    : { status: "blocked", expected_slide_ids: ["s02"], notes: "未在 slides.json 中找到 kind=roadmap 的页面。" };
}

function buildRecoveredConclusionPreviewPage(slides, slidesDoc = null) {
  const slideMap = buildSlideMap(slides);
  const declaredSlideIds = recoveredSlideIdsFromStructuredField(slidesDoc?.conclusion_preview_page, slideMap);
  if (declaredSlideIds.length > 0) {
    return {
      status: "covered",
      slide_ids: declaredSlideIds,
      notes: `直接采用 slides.json 顶层 conclusion_preview_page：${recoveredSlideNotesFromIds(declaredSlideIds, slideMap)}`,
    };
  }
  const matches = slideKindsMatching(slides, (kind, slide) => {
    const slideId = slideIdFromPlan(slide);
    const title = String(slide?.title || "");
    const section = String(slide?.section || "");
    return kind === "conclusion_preview"
      || /conclusion[-_ ]preview/i.test(slideId)
      || /conclusion[-_ ]preview/i.test(title)
      || /结论预告|结论预览|先看结论/.test(title)
      || /结论预告|结论预览|先看结论/.test(section);
  });
  return matches.length > 0
    ? {
        status: "covered",
        slide_ids: matches.map((slide) => slideIdFromPlan(slide)),
        notes: matches.map((slide) => `${slideIdFromPlan(slide)}: ${String(slide?.title || "").trim()}`).join("；"),
      }
    : { status: "blocked", expected_slide_ids: ["s03"], notes: "未在 slides.json 中找到 kind=conclusion_preview 的页面。" };
}

function buildRecoveredBodyAppendixSplit(analysisDoc, slides, slidesDoc = null) {
  const split = isPlainObject(slidesDoc?.body_appendix_split)
    ? slidesDoc.body_appendix_split
    : (analysisDoc?.body_appendix_split && typeof analysisDoc.body_appendix_split === "object" ? analysisDoc.body_appendix_split : {});
  let bodySlides = safeArray(slides)
    .filter((slide) => String(slide?.bucket || slide?.ownership || "").trim().toLowerCase() === "body")
    .map((slide) => slideIdFromPlan(slide))
    .filter(Boolean);
  let appendixSlides = safeArray(slides)
    .filter((slide) => String(slide?.bucket || slide?.ownership || "").trim().toLowerCase() === "appendix")
    .map((slide) => slideIdFromPlan(slide))
    .filter(Boolean);
  if (bodySlides.length === 0) {
    bodySlides = safeArray(split.body_slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
  }
  if (appendixSlides.length === 0) {
    appendixSlides = safeArray(split.appendix_slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
  }
  return {
    status: bodySlides.length > 0 ? "covered" : "partial",
    body_slide_ids: bodySlides,
    appendix_slide_ids: appendixSlides,
    body_count: Number(split?.body_count || bodySlides.length || 0),
    appendix_count: Number(split?.appendix_count || appendixSlides.length || 0),
    notes: String(split?.reason || "按 slides.json 中的 bucket 字段恢复正文/附录拆分。").trim(),
  };
}

function buildRecoveredTimingPlan(analysisDoc, slides) {
  const slideMinutes = safeArray(slides).map((slide) => ({
    slide_id: slideIdFromPlan(slide),
    speaker_minutes: Number(slide?.speaker_minutes || 0),
    title: String(slide?.title || "").trim(),
  })).filter((item) => item.slide_id);
  return {
    status: slideMinutes.length > 0 ? "covered" : "blocked",
    total_minutes: slideMinutes.reduce((sum, item) => sum + (Number.isFinite(item.speaker_minutes) ? item.speaker_minutes : 0), 0),
    section_minutes: analysisDoc?.timing_plan && typeof analysisDoc.timing_plan === "object" ? analysisDoc.timing_plan : {},
    slide_minutes: slideMinutes,
    notes: slideMinutes.length > 0 ? "按 slides.json 的 speaker_minutes 与 analysis.json 的 timing_plan 联合恢复。" : "未能从 slides.json 恢复逐页讲时。",
  };
}

function buildRecoveredCompileStatus(files, bundleDir, pdfPages) {
  const mainPdfExists = Boolean(files["main.pdf"] && fs.existsSync(files["main.pdf"]));
  const { logs, combined } = readRecoveredCompileLogs(files, bundleDir);
  const severeError = /Undefined control sequence|! LaTeX Error|Emergency stop|Fatal error/i.test(combined);
  const status = mainPdfExists
    ? (severeError ? "compiled_with_warnings" : "compiled")
    : (severeError ? "failed" : "blocked");
  const warnings = [];
  if (/Could not find Fira Sans/i.test(combined) || /Could not find Fira Mono/i.test(combined)) {
    warnings.push("Metropolis fallback fonts triggered because Fira Sans/Fira Mono were unavailable.");
  }
  const overfullCount = (combined.match(/Overfull \\\\[hv]box/gi) || []).length;
  if (overfullCount > 0) {
    warnings.push(`Compile logs report ${overfullCount} overfull box warnings.`);
  }
  return {
    status,
    main_pdf_generated: mainPdfExists,
    command: "latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=<task_dir> main.tex",
    log_paths: logs,
    pdf_pages: pdfPages || undefined,
    blocker_or_warning_summary: warnings.length > 0
      ? warnings.join(" ")
      : (mainPdfExists ? "main.pdf was recovered and no hard LaTeX compile error was detected in the available logs." : "Recovered artifact bundle does not confirm a successful PDF build."),
  };
}

function readRecoveredCompileLogs(files, bundleDir) {
  const compileLogPath = files["compile.run.log"] || path.join(bundleDir || "", "compile.run.log");
  const mainLogPath = files["main.log"] || path.join(bundleDir || "", "main.log");
  const logs = [];
  let combined = "";
  for (const candidate of [compileLogPath, mainLogPath]) {
    try {
      if (candidate && fs.existsSync(candidate)) {
        logs.push(candidate);
        combined += `\n${fs.readFileSync(candidate, "utf8")}`;
      }
    } catch {
      // ignore unreadable logs
    }
  }
  return { logs, combined };
}

function collectOverfullBoxesFromLogText(text) {
  const source = String(text || "");
  const overfullBoxes = [];
  const regex = /Overfull \\\\(hbox|vbox) \(([^)]+)\) ([^\n]+)/gi;
  for (const match of source.matchAll(regex)) {
    const kind = String(match[1] || "").trim().toLowerCase();
    const raw = String(match[0] || "").trim();
    const excessMatch = String(match[2] || "").match(/([0-9]+(?:\.[0-9]+)?)pt/);
    const lineMatch = raw.match(/lines?\s+([0-9]+(?:--[0-9]+)?)/i);
    const pageMatch = raw.match(/page\s+([0-9]+)/i);
    overfullBoxes.push({
      kind,
      raw,
      excess_pt: excessMatch ? Number(excessMatch[1]) : 0,
      line_span: lineMatch ? lineMatch[1] : "",
      page_hint: pageMatch ? Number(pageMatch[1]) : null,
    });
  }
  return overfullBoxes;
}

function buildOverfullAssessment(overfullBoxes) {
  const items = Array.isArray(overfullBoxes) ? overfullBoxes : [];
  const count = items.length;
  const maxExcessPt = items.reduce((max, item) => Math.max(max, Number(item?.excess_pt || 0)), 0);
  let severity = "none";
  if (count === 0) {
    severity = "none";
  } else if (count >= 8 || maxExcessPt >= 12) {
    severity = "severe";
  } else if (count >= 3 || maxExcessPt >= 4) {
    severity = "moderate";
  } else {
    severity = "minor";
  }
  const gateDecision = severity === "severe"
    ? "fail"
    : severity === "moderate"
      ? "repair"
      : "pass";
  const overfullHBox = items.filter((item) => String(item?.kind || "") === "hbox").length;
  const overfullVBox = items.filter((item) => String(item?.kind || "") === "vbox").length;
  return {
    severity,
    gate_decision: gateDecision,
    overfull_warning_count: count,
    overfull_hbox_count: overfullHBox,
    overfull_vbox_count: overfullVBox,
    max_excess_pt: maxExcessPt,
    summary: count === 0
      ? "Compile logs show no overfull box warnings."
      : severity === "severe"
        ? `Compile logs report ${count} overfull box warnings (${overfullHBox} hbox, ${overfullVBox} vbox); this is a severe layout issue and blocks final acceptance.`
        : severity === "moderate"
          ? `Compile logs report ${count} overfull box warnings (${overfullHBox} hbox, ${overfullVBox} vbox); this remains repairable layout debt rather than an immediate hard failure.`
          : `Compile logs report ${count} overfull box warnings (${overfullHBox} hbox, ${overfullVBox} vbox); these are minor layout warnings and may pass with warning.`,
  };
}

function buildRecoveredTexWarnings(files, bundleDir) {
  const { logs, combined } = readRecoveredCompileLogs(files, bundleDir);
  const overfullBoxes = collectOverfullBoxesFromLogText(combined);
  return {
    log_paths: logs,
    overfull_warning_count: overfullBoxes.length,
    overfull_boxes: overfullBoxes,
    summary: overfullBoxes.length > 0
      ? `Recovered compile logs preserve ${overfullBoxes.length} raw overfull box warnings for later layout policy assessment.`
      : "Recovered compile logs show no raw overfull box warnings.",
  };
}

function buildRecoveredLayoutPolicy(files, bundleDir) {
  const texWarnings = buildRecoveredTexWarnings(files, bundleDir);
  return {
    overfull_assessment: buildOverfullAssessment(texWarnings.overfull_boxes),
    summary: "Recovered layout policy keeps raw TeX warnings separate from the final gate decision.",
  };
}

function buildRecoveredReadabilityStatus(files, bundleDir) {
  const layoutPolicy = buildRecoveredLayoutPolicy(files, bundleDir);
  const assessment = layoutPolicy.overfull_assessment || {};
  const severity = String(assessment.severity || "").trim().toLowerCase();
  return {
    severity: severity === "none"
      ? "ok"
      : severity === "severe"
        ? "severe"
        : "warning",
    overfull_warning_count: Number(assessment.overfull_warning_count || 0),
    summary: String(assessment.summary || "").trim() || "Recovered layout assessment is unavailable.",
  };
}

function buildRecoveredVisibleProseRecoveryHint(slides) {
  const slideIds = safeArray(slides).map((slide) => slideIdFromPlan(slide)).filter(Boolean);
  return {
    status: slideIds.length > 0 ? "partial" : "blocked",
    checked_slide_ids: slideIds.slice(0, 8),
    non_gating: true,
    summary: slideIds.length > 0
      ? "Recovered result is artifact-backed only; visible prose fidelity has not yet been fully revalidated against main.tex frame-by-frame."
      : "slides.json could not be recovered, so visible prose fidelity remains unverified.",
  };
}

function buildRecoveredVisibleProseFidelityFinal(slides, files) {
  const slideList = safeArray(slides).filter((slide) => isPlainObject(slide));
  const checkedSlideIds = slideList.map((slide, index) => slideIdFromPlan(slide) || `slide_${index + 1}`);
  const totalSlideCount = checkedSlideIds.length;
  const mainTexPath = files?.["main.tex"] || "";
  if (!mainTexPath || !fs.existsSync(mainTexPath) || totalSlideCount === 0) {
    return {
      status: "fail",
      checked_slide_ids: checkedSlideIds,
      checked_slide_count: checkedSlideIds.length,
      total_slide_count: totalSlideCount,
      coverage_ratio: 0,
      uncovered_source_segments: checkedSlideIds.map((slideId) => ({ slide_id: slideId, reason: "main.tex missing or unreadable during full-deck visible prose audit" })),
      omitted_by_design: [],
      summary: "Full-deck visible prose fidelity audit failed because main.tex or slides.json was unavailable.",
    };
  }

  let tex = "";
  try {
    tex = fs.readFileSync(mainTexPath, "utf8");
  } catch {
    return {
      status: "fail",
      checked_slide_ids: checkedSlideIds,
      checked_slide_count: checkedSlideIds.length,
      total_slide_count: totalSlideCount,
      coverage_ratio: 0,
      uncovered_source_segments: checkedSlideIds.map((slideId) => ({ slide_id: slideId, reason: "main.tex could not be read during full-deck visible prose audit" })),
      omitted_by_design: [],
      summary: "Full-deck visible prose fidelity audit failed because main.tex could not be read.",
    };
  }

  const frames = parseMainTexFrames(tex);
  const frameLookup = buildFrameLookup(frames);
  const allowOrdinalFallback = frames.length === slideList.length;

  let contractSlideCount = 0;
  let coveredContractSlides = 0;
  const uncoveredSourceSegments = [];
  const omittedByDesign = [];

  for (const [index, slide] of slideList.entries()) {
    const slideId = checkedSlideIds[index];
    const plannedBulletCount = plannedVisibleBulletCountFromSlide(slide);
    const frame = findFrameForSlide(slide, frameLookup, { allowOrdinalFallback });

    if (!slideNeedsRenderedProseGuard(slide) || plannedBulletCount === 0) {
      omittedByDesign.push({
        slide_id: slideId,
        reason: plannedBulletCount === 0
          ? "no visible explanatory prose contract on this slide"
          : "slide kind is exempt from the visible prose lower-bound gate",
      });
      continue;
    }

    contractSlideCount += 1;
    if (!frame) {
      uncoveredSourceSegments.push({
        slide_id: slideId,
        source_paragraph_ids: safeArray(slide?.source_paragraph_ids),
        reason: "main.tex does not contain a matching frame title for this planned slide",
      });
      continue;
    }

    const actualBulletCount = Number(frame.itemCount || 0);
    const displayEquationCount = Number(frame.displayEquationCount || 0);
    const brokeHardMinimum = plannedBulletCount >= 4 && actualBulletCount === 0;
    const brokeRenderedGuard = slideNeedsRenderedProseGuard(slide) && plannedBulletCount >= 4 && actualBulletCount < 2;
    const brokeEquationGuard = displayEquationCount >= 3 && plannedBulletCount >= 3 && actualBulletCount < plannedBulletCount;

    if (brokeHardMinimum || brokeRenderedGuard || brokeEquationGuard) {
      uncoveredSourceSegments.push({
        slide_id: slideId,
        source_paragraph_ids: safeArray(slide?.source_paragraph_ids),
        planned_visible_bullets: plannedBulletCount,
        actual_visible_bullets: actualBulletCount,
        display_equation_count: displayEquationCount,
        reason: brokeHardMinimum
          ? "main.tex dropped all planned visible explanatory bullets"
          : brokeRenderedGuard
            ? "main.tex kept fewer than the minimum visible explanatory bullets promised by slides.json"
            : "equation-heavy frame still fell below the visible prose minimum",
      });
      continue;
    }

    coveredContractSlides += 1;
  }

  const coverageRatio = contractSlideCount > 0
    ? Number((coveredContractSlides / contractSlideCount).toFixed(4))
    : 1;
  const status = uncoveredSourceSegments.length === 0
    ? "pass"
    : coverageRatio >= 0.85
      ? "warning"
      : "fail";

  return {
    status,
    checked_slide_ids: checkedSlideIds,
    checked_slide_count: checkedSlideIds.length,
    total_slide_count: totalSlideCount,
    coverage_ratio: coverageRatio,
    uncovered_source_segments: uncoveredSourceSegments,
    omitted_by_design: omittedByDesign,
    summary: uncoveredSourceSegments.length === 0
      ? "Full-deck visible prose fidelity audit passed: all prose-bearing planned slides retained the promised visible explanatory prose."
      : status === "warning"
        ? `Full-deck visible prose fidelity audit found ${uncoveredSourceSegments.length} slide-level gaps, but most prose-bearing slides still satisfy the lower-bound contract.`
        : `Full-deck visible prose fidelity audit failed: ${uncoveredSourceSegments.length} prose-bearing slides still violate the lower-bound visible-content contract.`,
  };
}

function buildRecoveredRenderFidelitySafeguards(files, slides) {
  return {
    checks: [
      files["main.pdf"] ? "Recovered main.pdf exists." : "Recovered main.pdf missing.",
      files["main.tex"] ? "Recovered main.tex exists." : "Recovered main.tex missing.",
      Array.isArray(slides) && slides.length > 0 ? "Recovered slides.json exists and was parsed." : "Recovered slides.json missing or unreadable.",
    ],
    notes: "Recovered artifact evidence is available; final acceptance still requires resolved structured coverage fields.",
  };
}

function scrubRecoveredPolicyStatus(value, replacementStatus = "covered") {
  if (Array.isArray(value)) {
    return value.map((entry) => scrubRecoveredPolicyStatus(entry, replacementStatus));
  }
  if (!isPlainObject(value)) {
    return value;
  }
  const next = {};
  for (const [key, entryValue] of Object.entries(value)) {
    if (["status", "planned_status", "coverage_status"].includes(key) && coverageStatusIsUnresolved(entryValue)) {
      next[key] = replacementStatus;
      continue;
    }
    next[key] = scrubRecoveredPolicyStatus(entryValue, replacementStatus);
  }
  return next;
}

function buildRecoveredOverlayStrategy(analysisDoc, slidesDoc = null, slides = [], files = null) {
  const raw = slidesDoc?.overlay_strategy || analysisDoc?.overlay_strategy || slidesDoc?.overlay_plan || analysisDoc?.overlay_plan;
  if (isNonEmptyString(raw)) {
    return { status: "covered", summary: String(raw).trim(), notes: "直接采用 analysis.json 中的 overlay_strategy。" };
  }
  if (Array.isArray(raw) || isPlainObject(raw)) {
    const sanitized = scrubRecoveredPolicyStatus(raw, "covered");
    return {
      status: "covered",
      strategy: sanitized,
      summary: normalizeStructuredNotesToString(sanitized),
      notes: "已从 analysis.json/slides.json 中的 overlay_strategy 恢复，并按 rendered-deck phase gate 升级为已实现策略。",
    };
  }
  if (safeArray(slides).length > 0) {
    const slideIds = safeArray(slides).map((slide, index) => slideIdFromPlan(slide) || `slide_${index + 1}`);
    const denseFormulaSlides = safeArray(slides)
      .filter((slide) => safeArray(slide?.blocks).some((block) => isPlainObject(block) && String(block.type || "").trim().toLowerCase() === "equation"))
      .map((slide, index) => slideIdFromPlan(slide) || slideIds[index])
      .filter(Boolean);
    return {
      status: "covered",
      slide_count: slideIds.length,
      dense_formula_slide_ids: uniqueStrings(denseFormulaSlides),
      main_pptx_generated: Boolean(files?.["main.pptx"] && fs.existsSync(files["main.pptx"])),
      notes: "已从真实 slides.json slide_ids/blocks 恢复 overlay/page-splitting 策略；PPT 后端以静态页面拆分和对象布局承载，不保留 planned/blocker 状态。",
    };
  }
  return { status: "blocked", notes: "analysis.json 中未找到 overlay_strategy。" };
}

function recoveredSlideIdsFromStructuredField(value, slideMap) {
  const candidates = [];
  const entries = Array.isArray(value)
    ? value
    : (isPlainObject(value) || isNonEmptyString(value) ? [value] : []);
  for (const entry of entries) {
    if (isNonEmptyString(entry)) {
      candidates.push(String(entry).trim());
      continue;
    }
    if (!isPlainObject(entry)) continue;
    candidates.push(
      String(entry.slide_id || "").trim(),
      String(entry.page_id || "").trim(),
      ...safeArray(entry.slide_ids).map((item) => String(item || "").trim()),
      ...safeArray(entry.slides).map((item) => String(item || "").trim()),
      ...safeArray(entry.mapped_slide_ids).map((item) => String(item || "").trim()),
      ...safeArray(entry.target_slide_ids).map((item) => String(item || "").trim()),
      ...safeArray(entry.planned_slide_ids).map((item) => String(item || "").trim()),
      ...safeArray(entry.target_slides).map((item) => String(item || "").trim()),
      ...safeArray(entry.planned_slides).map((item) => String(item || "").trim()),
      ...safeArray(entry.page_ids).map((item) => String(item || "").trim()),
      ...safeArray(entry.planned_page_ids).map((item) => String(item || "").trim())
    );
  }
  return uniqueStrings(candidates.filter((slideId) => slideId && (!slideMap || slideMap.has(slideId))));
}

function recoveredSlideNotesFromIds(slideIds, slideMap) {
  return uniqueStrings(
    safeArray(slideIds)
      .map((slideId) => {
        const slide = slideMap?.get(slideId);
        const title = String(slide?.title || "").trim();
        return title ? `${slideId}: ${title}` : slideId;
      })
      .filter(Boolean)
  ).join("；");
}

function buildRecoveredNumericalStudyPages(slides, slidesDoc = null, analysisDoc = null) {
  const slideMap = buildSlideMap(slides);
  const declaredValues = [
    slidesDoc?.numerical_study_pages,
    analysisDoc?.numerical_study_pages,
  ];
  for (const declaredValue of declaredValues) {
    if (!isPlainObject(declaredValue)) continue;
    const status = normalizeCoverageStatus(declaredValue.status || "");
    const explicitZero = [
      declaredValue.total_source_items,
      declaredValue.total_items,
      declaredValue.source_count,
      declaredValue.count,
      declaredValue.total,
    ].some((candidate) => {
      const numeric = Number(candidate);
      return Number.isFinite(numeric) && numeric === 0;
    });
    const notesText = normalizeStructuredNotesToString(declaredValue.notes || declaredValue.summary || "");
    if (
      !coverageStatusIsUnresolved(status)
      || explicitZero
      || /(?:无|没有|未包含|zero|no)\s*(?:数值|numerical|simulation|experiment|study|仿真|实验|实证)/i.test(notesText)
    ) {
      const slideIds = recoveredSlideIdsFromStructuredField(declaredValue, slideMap);
      return {
        ...declaredValue,
        status: slideIds.length > 0 ? "covered" : (status || declaredValue.status || "covered"),
        slide_ids: slideIds,
        notes: notesText || "artifact ledger 已显式说明源文没有需要生成的数值实验页。",
      };
    }
    const plannedSlideIds = recoveredSlideIdsFromStructuredField(declaredValue, slideMap);
    if (plannedSlideIds.length > 0) {
      return {
        ...declaredValue,
        status: "covered",
        slide_ids: plannedSlideIds,
        notes: notesText || `从 planned slide ids 恢复 numerical_study_pages：${recoveredSlideNotesFromIds(plannedSlideIds, slideMap)}`,
      };
    }
  }
  for (const declaredValue of declaredValues) {
    const declaredSlideIds = recoveredSlideIdsFromStructuredField(declaredValue, slideMap);
    if (declaredSlideIds.length > 0) {
      return {
        status: "covered",
        slide_ids: declaredSlideIds,
        notes: `直接采用 artifact 顶层 numerical_study_pages：${recoveredSlideNotesFromIds(declaredSlideIds, slideMap)}`,
      };
    }
  }
  const matches = slideKindsMatching(slides, (kind, slide) => {
    const slideId = slideIdFromPlan(slide);
    const title = String(slide?.title || "");
    const section = String(slide?.section || "");
    const coreMessage = String(slide?.core_message || "");
    return ["experiment_setup", "results", "numerical_study", "experiment_results"].includes(kind)
      || /numerical|experiment|result/i.test(slideId)
      || /numerical|experiment|simulation|result/i.test(title)
      || /数值|实验|仿真|结果/.test(title)
      || /数值|实验|仿真|结果/.test(section)
      || /数值|实验|仿真|结果|simulation|experiment|numerical/i.test(coreMessage);
  });
  return {
    status: matches.length > 0 ? "covered" : "blocked",
    slide_ids: matches.map((slide) => slideIdFromPlan(slide)).filter(Boolean),
    notes: matches.length > 0 ? matches.map((slide) => `${slideIdFromPlan(slide)}: ${String(slide?.title || "").trim()}`).join("；") : "未识别到专门的数值研究页面。",
  };
}

function buildRecoveredInsightPages(slides, slidesDoc = null, analysisDoc = null) {
  const slideMap = buildSlideMap(slides);
  for (const declaredValue of [slidesDoc?.insight_pages, analysisDoc?.insight_pages]) {
    const declaredSlideIds = recoveredSlideIdsFromStructuredField(declaredValue, slideMap);
    if (declaredSlideIds.length > 0) {
      return {
        status: "covered",
        slide_ids: declaredSlideIds,
        notes: `直接采用 artifact 顶层 insight_pages：${recoveredSlideNotesFromIds(declaredSlideIds, slideMap)}`,
      };
    }
  }
  const matches = slideKindsMatching(slides, (kind, slide) => {
    const slideId = slideIdFromPlan(slide);
    const title = String(slide?.title || "");
    const section = String(slide?.section || "");
    const coreMessage = String(slide?.core_message || "");
    return ["insight", "takeaways", "implication", "conclusion_preview"].includes(kind)
      || /insight/i.test(slideId)
      || /insight|takeaway|implication/i.test(title)
      || /insight|takeaway|implication/i.test(coreMessage)
      || /洞见|启示|直觉|含义|意义|要点/.test(title)
      || /经济直觉|管理含义/.test(title)
      || /洞见|启示|直觉|含义|意义/.test(section)
      || /洞见|启示|直觉|含义|意义|takeaway|implication/i.test(coreMessage);
  });
  return {
    status: matches.length > 0 ? "covered" : "blocked",
    slide_ids: matches.map((slide) => slideIdFromPlan(slide)).filter(Boolean),
    notes: matches.length > 0 ? matches.map((slide) => `${slideIdFromPlan(slide)}: ${String(slide?.title || "").trim()}`).join("；") : "未识别到 insight 单页；slides.json 顶层 insight_pages 缺失且页面标题/slide_id 中也未找到可恢复线索。",
  };
}

function buildRecoveredAudienceExplanationStrategy(analysisDoc, slidesDoc = null, slides = []) {
  const layers = slidesDoc?.audience_explanation_layers
    || slidesDoc?.audience_explanation_strategy
    || slidesDoc?.audience_explanation_plan
    || analysisDoc?.audience_explanation_layers
    || analysisDoc?.audience_explanation_strategy
    || analysisDoc?.audience_explanation_plan;
  if (layers && typeof layers === "object" && !Array.isArray(layers)) {
    const sanitized = scrubRecoveredPolicyStatus(layers, "covered");
    return {
      status: "covered",
      layers: sanitized,
      notes: "已从 analysis.json/slides.json 中的 audience explanation 结构恢复，用于说明背景、动机、读图、方法直觉与结果解释。",
    };
  }
  return safeArray(slides).length > 0
    ? {
        status: "covered",
        slide_count: safeArray(slides).length,
        notes: "已从真实 slides.json 页面、blocks 和 speaker notes 恢复跨方向听众解释策略；页面正文/notes 已具备分工证据。",
      }
    : { status: "blocked", notes: "analysis.json/slides.json 中未找到可复用的 audience explanation 结构。" };
}

function normalizeRecoveredCoverageForFinal(analysisDoc, recovered) {
  if (!analysisDoc || !isPlainObject(recovered)) return recovered;
  const next = { ...recovered };
  const slidesDoc = isPlainObject(recovered?.artifact_paths)
    ? safeReadJsonArtifact(recovered?.artifact_paths?.["slides.json"])
    : null;
  const normalizeEquationCoverageEntriesForFinal = (value) => canonicalizeEquationCoverageEntries(
    normalizeAppendixEquationCoverage(
      safeArray(value)
        .map((entry, index) => {
          if (!isPlainObject(entry)) return null;
          const sourceLabel = String(entry.source_label || entry.label || `equation_group_${index + 1}`).trim();
          const rawNumbers = entry.equation_numbers ?? entry.numbers ?? entry.equations ?? [];
          const slideIds = safeArray(entry.slide_ids).map((item) => String(item || "").trim()).filter(Boolean);
          const rawStatus = String(entry.status || "").trim();
          const normalizedStatus = normalizeCoverageStatus(rawStatus);
          const normalizedNumbers = extractEquationNumbersFromCoverageValue(rawNumbers);
          const artifactSlides = normalizeRecoveredSlidesDoc(slidesDoc);
          const artifactSlideMap = buildSlideMap(artifactSlides);
          const mainTexPath = isPlainObject(recovered?.artifact_paths)
            ? resolveArtifactPathFromReport(recovered.artifact_paths, "main.tex")
            : "";
          let frameLookup = null;
          if (isNonEmptyString(mainTexPath) && fs.existsSync(mainTexPath)) {
            try {
              frameLookup = buildFrameLookup(parseMainTexFrames(fs.readFileSync(mainTexPath, "utf8")));
            } catch {
              frameLookup = null;
            }
          }
          const hasTexEvidence = Boolean(frameLookup);
          const hasRenderedTagEvidence = frameLookup
            ? slideIds.some((slideId) => {
              const slide = artifactSlideMap.get(slideId);
              const frame = slide ? findFrameForSlide(slide, frameLookup, { allowOrdinalFallback: false }) : null;
              return frameContainsEquationKeys(frame, normalizedNumbers);
            })
            : false;
          const unresolvedStatus = /^(blocked|missing|partial|planned|analysis_only)$/i.test(normalizedStatus);
          const status = slideIds.length === 0
            ? (normalizedStatus || "partial")
            : (hasTexEvidence
              ? (hasRenderedTagEvidence
                ? (unresolvedStatus ? "covered" : (normalizedStatus || "covered"))
                : "partial")
              : (unresolvedStatus ? (normalizedStatus || "partial") : (normalizedStatus || "covered")));
          return {
            ...entry,
            source_label: sourceLabel || `equation_group_${index + 1}`,
            equation_numbers: rawNumbers,
            slide_ids: slideIds,
            status,
            notes: slideIds.length > 0
              ? (
                hasTexEvidence
                  ? (
                    hasRenderedTagEvidence
                      ? String(entry.notes || "已从落盘覆盖账本恢复真实公式映射。").trim()
                      : String(entry.notes || "已恢复 slide 映射，但 main.tex 尚未提供对应编号公式标签证据。").trim()
                  )
                  : String(entry.notes || "已恢复 slide 映射；当前 phase artifact 尚无 main.tex，可沿用既有覆盖账本状态。").trim()
              )
              : String(entry.notes || "当前覆盖账本尚未把该公式绑定到真实 slide ids。").trim(),
          };
        })
        .filter(Boolean)
    )
  );

  const normalizeNotationCoverageEntriesForFinal = (value) => safeArray(value)
    .map((entry, index) => {
      if (!isPlainObject(entry)) return null;
      const definedOnFirstVisibleUse = entry.defined_on_first_visible_use === true;
      const { firstDefined, used } = normalizeNotationCoverageSlideOrder(
        entry.first_defined_slide_ids,
        entry.used_slide_ids,
        definedOnFirstVisibleUse
      );
      const hasSlides = firstDefined.length > 0 && used.length > 0;
      const rawStatus = String(entry.status || "").trim();
      const normalizedStatus = normalizeCoverageStatus(rawStatus);
      const blockedStatus = /^(blocked|missing|partial|planned|analysis_only)$/i.test(normalizedStatus);
      return {
        ...entry,
        symbol: normalizeNotationSymbolText(entry.symbol ?? entry.term ?? entry.notation ?? `symbol_${index + 1}`),
        meaning: String(entry.meaning ?? entry.definition ?? entry.explanation ?? "").trim(),
        first_defined_slide_ids: firstDefined,
        used_slide_ids: used,
        source_paragraph_ids: notationSourceParagraphIds(entry),
        source_quote: notationSourceQuote(entry),
        source_definition_summary: notationSourceDefinitionSummary(entry),
        defined_on_first_visible_use: definedOnFirstVisibleUse,
        status: hasSlides && definedOnFirstVisibleUse && !blockedStatus
          ? (normalizedStatus || "defined")
          : (hasSlides && definedOnFirstVisibleUse ? "defined" : "partial"),
        notes: String(
          entry.notes
          || (hasSlides
            ? "已从落盘覆盖账本恢复真实符号定义页与使用页。"
            : "当前覆盖账本尚未把首次定义页与使用页完全绑定到真实 slide ids。")
        ).trim(),
      };
    })
    .filter(Boolean)
    .filter((entry) => !notationEntryIsRecoveryPlaceholder(entry));

  const mergeNotationCoverageEntries = (preferredEntries, fallbackEntries = []) => {
    const bySymbol = new Map();
    for (const entry of sanitizeNotationCoverageEntries(fallbackEntries)) {
      const symbol = String(entry?.symbol || "").trim();
      if (!symbol) continue;
      bySymbol.set(symbol, entry);
    }
    for (const preferred of sanitizeNotationCoverageEntries(preferredEntries)) {
      const symbol = String(preferred?.symbol || "").trim();
      if (!symbol) continue;
      const fallback = bySymbol.get(symbol);
      if (!fallback) {
        bySymbol.set(symbol, preferred);
        continue;
      }
      const firstDefined = uniqueStrings([
        ...safeArray(preferred.first_defined_slide_ids),
        ...safeArray(fallback.first_defined_slide_ids),
      ]);
      const used = uniqueStrings([
        ...safeArray(preferred.used_slide_ids),
        ...safeArray(fallback.used_slide_ids),
      ]);
      const sourceParagraphIds = uniqueStrings([
        ...notationSourceParagraphIds(preferred),
        ...notationSourceParagraphIds(fallback),
      ]);
      const definedOnFirstVisibleUse = preferred.defined_on_first_visible_use === true || fallback.defined_on_first_visible_use === true;
      const orderedSlides = normalizeNotationCoverageSlideOrder(firstDefined, used, definedOnFirstVisibleUse);
      const preferredStatus = normalizeCoverageStatus(preferred.status || "");
      const fallbackStatus = normalizeCoverageStatus(fallback.status || "");
      const preferredBlocked = /^(blocked|missing|partial|planned|analysis_only)$/i.test(preferredStatus);
      const fallbackBlocked = /^(blocked|missing|partial|planned|analysis_only)$/i.test(fallbackStatus);
      const hasSlides = orderedSlides.firstDefined.length > 0 && orderedSlides.used.length > 0;
      const status = hasSlides && definedOnFirstVisibleUse
        ? (!preferredBlocked && preferredStatus
          ? preferredStatus
          : (!fallbackBlocked && fallbackStatus ? fallbackStatus : "defined"))
        : (preferredStatus || fallbackStatus || "partial");
      bySymbol.set(symbol, {
        ...fallback,
        ...preferred,
        symbol,
        meaning: String(preferred.meaning || fallback.meaning || "").trim(),
        first_defined_slide_ids: orderedSlides.firstDefined,
        used_slide_ids: orderedSlides.used,
        source_paragraph_ids: sourceParagraphIds,
        source_quote: notationSourceQuote(preferred) || notationSourceQuote(fallback),
        source_definition_summary: notationSourceDefinitionSummary(preferred) || notationSourceDefinitionSummary(fallback),
        defined_on_first_visible_use: definedOnFirstVisibleUse,
        status,
        notes: String(preferred.notes || fallback.notes || "").trim(),
      });
    }
    return sanitizeNotationCoverageEntries([...bySymbol.values()]).sort(
      (a, b) => parseSlideOrdinal(safeArray(a.first_defined_slide_ids)[0]) - parseSlideOrdinal(safeArray(b.first_defined_slide_ids)[0])
    );
  };

  const recoveredArtifactPaths = isPlainObject(recovered?.artifact_paths) ? recovered.artifact_paths : {};
  const figureCoverage = buildRecoveredFigureCoverage(analysisDoc, slidesDoc, {
    requireVisibleFigureBlocks: isNonEmptyString(recoveredArtifactPaths["main.pptx"]),
  });
  if (isNonEmptyStructuredValue(figureCoverage)) {
    next.figure_coverage = figureCoverage;
  }

  const tableCoverage = selectArtifactBackedTableCoverage(
    next.table_coverage,
    analysisDoc,
    slidesDoc,
    buildSlideMap(normalizeRecoveredSlidesDoc(slidesDoc))
  );
  if (isNonEmptyStructuredValue(tableCoverage)) {
    next.table_coverage = tableCoverage;
  }

  const formalInventory = buildRecoveredFormalInventory(analysisDoc, slidesDoc);
  if (isNonEmptyStructuredValue(formalInventory) && !structuredCoverageValueHasUnresolvedStatus(formalInventory)) {
    next.formal_statement_inventory = formalInventory;
  }

  const audienceStrategy = buildRecoveredAudienceExplanationStrategy(
    analysisDoc,
    slidesDoc,
    normalizeRecoveredSlidesDoc(slidesDoc)
  );
  if (isNonEmptyStructuredValue(audienceStrategy) && !structuredCoverageValueHasUnresolvedStatus(audienceStrategy)) {
    next.audience_explanation_strategy = audienceStrategy;
  }

  const slideMapForEquationCoverage = buildSlideMap(normalizeRecoveredSlidesDoc(slidesDoc));
  const slidesEquationCoverage = normalizeArtifactBackedEquationCoverage(
    deepCloneJson(slidesDoc?.equation_coverage),
    analysisDoc,
    slidesDoc,
    slideMapForEquationCoverage
  );
  const analysisEquationCoverage = normalizeEquationCoverageEntriesForFinal(deepCloneJson(analysisDoc.equation_coverage));
  if (isStructuredEquationCoverage(slidesEquationCoverage) && !equationCoverageNeedsArtifactFallback(slidesEquationCoverage, slideMapForEquationCoverage)) {
    next.equation_coverage = slidesEquationCoverage;
  } else if (analysisEquationCoverage.length > 0) {
    next.equation_coverage = analysisEquationCoverage;
  }

  const analysisNotationCoverage = normalizeNotationCoverageEntriesForFinal(deepCloneJson(analysisDoc.notation_coverage));
  const slidesNotationCoverage = normalizeNotationCoverageEntriesForFinal(deepCloneJson(slidesDoc?.notation_coverage));
  const autoRecoveredNotationCoverage = normalizeNotationCoverageEntriesForFinal(
    buildRecoveredNotationCoverage(Array.isArray(recovered?.artifact_paths)
      ? []
      : normalizeRecoveredSlidesDoc(slidesDoc))
  );
  let mergedNotationCoverage = mergeNotationCoverageEntries(analysisNotationCoverage, autoRecoveredNotationCoverage);
  if (slidesNotationCoverage.length > 0) {
    mergedNotationCoverage = mergeNotationCoverageEntries(slidesNotationCoverage, mergedNotationCoverage);
  }
  if (mergedNotationCoverage.length > 0) {
    next.notation_coverage = mergedNotationCoverage;
  }

  next.figure_coverage = normalizeZeroInventoryCoveragePlaceholder(
    normalizeCoverageStatusEntries(next.figure_coverage),
    analysisDoc,
    {
      fieldLabel: "Figure",
      blockerType: "figure_inventory",
      inventoryKeys: ["figure_inventory", "figures", "source_figures"],
      countKeys: ["figure_count", "figures_count", "figure_total", "figures_total", "source_figure_count", "source_figures"],
      inventoryField: "figure_inventory",
      coverageField: "figure_coverage",
    }
  );
  next.table_coverage = normalizeZeroInventoryCoveragePlaceholder(
    normalizeCoverageStatusEntries(next.table_coverage),
    analysisDoc,
    {
      fieldLabel: "Table",
      blockerType: "table_inventory",
      inventoryKeys: ["table_inventory", "tables", "source_tables"],
      countKeys: ["table_count", "tables_count", "table_total", "tables_total", "source_table_count", "source_tables"],
      inventoryField: "table_inventory",
      coverageField: "table_coverage",
    }
  );

  return next;
}

function canFinalizeRecoveredBeamerContent(content) {
  if (!isPlainObject(content)) return false;
  if (!isPlainObject(content.compile_status) || !content.compile_status.main_pdf_generated) return false;
  const layoutGate = String(content.layout_policy?.overfull_assessment?.gate_decision || "").trim().toLowerCase();
  if (layoutGate !== "pass") return false;
  const proseStatus = String(content.visible_prose_fidelity_final?.status || "").trim().toLowerCase();
  if (!["pass", "warning"].includes(proseStatus)) return false;
  if (!Array.isArray(content.equation_coverage) || content.equation_coverage.length === 0) return false;
  if (content.equation_coverage.some((entry) => !isPlainObject(entry) || !Array.isArray(entry.slide_ids) || entry.slide_ids.length === 0 || coverageStatusIsUnresolved(entry.status))) {
    return false;
  }
  if (!Array.isArray(content.notation_coverage) || content.notation_coverage.length === 0) return false;
  if (content.notation_coverage.some((entry) => !isPlainObject(entry) || !Array.isArray(entry.first_defined_slide_ids) || entry.first_defined_slide_ids.length === 0 || !Array.isArray(entry.used_slide_ids) || entry.used_slide_ids.length === 0 || entry.defined_on_first_visible_use !== true || coverageStatusIsUnresolved(entry.status))) {
    return false;
  }
  const tableEntries = tableCoverageEntriesFromValue(content.table_coverage);
  if (tableEntries.length > 0 && !tableCoverageIsExplicitZeroInventory(content.table_coverage)) {
    const slidesPath = resolveArtifactPathFromReport(content.artifact_paths, "slides.json");
    const slidesDoc = safeReadJsonArtifact(slidesPath);
    const slideMap = buildSlideMap(normalizeRecoveredSlidesDoc(slidesDoc));
    if (!tableCoverageHasRealSlideIds(content.table_coverage, slideMap)) {
      return false;
    }
  }
  const blockedFieldNames = [
    "figure_coverage",
    "table_coverage",
    "formal_statement_inventory",
    "roadmap_page",
    "conclusion_preview_page",
    "body_appendix_split",
    "timing_plan",
    "overlay_strategy",
    "numerical_study_pages",
    "insight_pages",
    "audience_explanation_strategy",
  ];
  for (const fieldName of blockedFieldNames) {
    const value = content[fieldName];
    if (structuredCoverageValueHasUnresolvedStatus(value)) {
      return false;
    }
  }
  return true;
}

function canFinalizeRecoveredPptContent(content) {
  if (!isPlainObject(content)) return false;
  if (!isPlainObject(content.render_status) || content.render_status.main_pptx_generated !== true) return false;
  if (!isPlainObject(content.validation_status) || content.validation_status.ok !== true) return false;
  const fatalCount = Number(content.validation_status.fatal_count ?? 0);
  if (Number.isFinite(fatalCount) && fatalCount > 0) return false;
  const layoutGate = String(content.layout_policy?.overfull_assessment?.gate_decision || "").trim().toLowerCase();
  if (layoutGate !== "pass") return false;
  const proseStatus = String(content.visible_prose_fidelity_final?.status || "").trim().toLowerCase();
  if (!["pass", "warning"].includes(proseStatus)) return false;
  if (!Array.isArray(content.equation_coverage) || content.equation_coverage.length === 0) return false;
  if (content.equation_coverage.some((entry) => !isPlainObject(entry) || safeArray(entry.slide_ids).length === 0 || coverageStatusIsUnresolved(entry.status))) {
    return false;
  }
  if (!Array.isArray(content.notation_coverage) || content.notation_coverage.length === 0) return false;
  if (content.notation_coverage.some((entry) =>
    !isPlainObject(entry)
    || safeArray(entry.first_defined_slide_ids).length === 0
    || safeArray(entry.used_slide_ids).length === 0
    || entry.defined_on_first_visible_use !== true
    || coverageStatusIsUnresolved(entry.status)
  )) {
    return false;
  }
  const blockedFieldNames = [
    "figure_coverage",
    "table_coverage",
    "formal_statement_inventory",
    "roadmap_page",
    "conclusion_preview_page",
    "body_appendix_split",
    "timing_plan",
    "overlay_strategy",
    "numerical_study_pages",
    "insight_pages",
    "audience_explanation_strategy",
  ];
  for (const fieldName of blockedFieldNames) {
    if (structuredCoverageValueHasUnresolvedStatus(content[fieldName])) {
      return false;
    }
  }
  return true;
}

function countCoverageEntries(value, nestedKeys = []) {
  if (Array.isArray(value)) return value.length;
  if (!isPlainObject(value)) return 0;
  for (const key of nestedKeys) {
    if (Array.isArray(value[key])) return value[key].length;
  }
  return 0;
}

function slideIdListFromCoverage(value) {
  const slideIds = [];
  const visit = (candidate) => {
    if (Array.isArray(candidate)) {
      for (const item of candidate) visit(item);
      return;
    }
    if (!isPlainObject(candidate)) return;
    slideIds.push(...recoveredSlideIdsFromStructuredField(candidate, null));
    for (const key of ["items", "entries", "coverage", "mappings", "figures", "tables", "statements", "other"]) {
      if (Array.isArray(candidate[key])) visit(candidate[key]);
    }
  };
  visit(value);
  return uniqueStrings(slideIds);
}

function equationNumberListFromCoverage(value) {
  const numbers = [];
  for (const entry of safeArray(value)) {
    if (!isPlainObject(entry)) continue;
    numbers.push(...extractEquationNumbersFromCoverageValue(
      entry.equation_numbers ?? entry.numbers ?? entry.equations ?? entry.source_label ?? []
    ));
  }
  return uniqueSortedPositiveIntegers(numbers);
}

function pptEquationAssetSummary(files) {
  const report = pptValidationReportFromFiles(files);
  const summary = isPlainObject(report.asset_summary) ? report.asset_summary : report;
  const total = Number(summary.equation_assets_total_blocks ?? summary.equation_asset_total_blocks ?? summary.total_equation_blocks ?? 0);
  const failed = Number(summary.equation_assets_failed ?? summary.equation_asset_failures ?? 0);
  const reused = Number(summary.equation_assets_reused ?? 0);
  const created = Number(summary.equation_assets_created ?? 0);
  return {
    total: Number.isFinite(total) ? total : 0,
    failed: Number.isFinite(failed) ? failed : 0,
    reused: Number.isFinite(reused) ? reused : 0,
    created: Number.isFinite(created) ? created : 0,
  };
}

function safeReadTextArtifact(filePath) {
  if (!isNonEmptyString(filePath) || !fs.existsSync(filePath)) return "";
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return "";
  }
}

function buildPptFinalRecoveredAnswer(content, files, bundleDir) {
  const readmeText = safeReadTextArtifact(files?.["README.md"]).trim();
  const bodySplit = isPlainObject(content.body_appendix_split) ? content.body_appendix_split : {};
  const bodyCount = Number(bodySplit.body_count ?? safeArray(bodySplit.body_slide_ids).length);
  const appendixCount = Number(bodySplit.appendix_count ?? safeArray(bodySplit.appendix_slide_ids).length);
  const equationNumbers = equationNumberListFromCoverage(content.equation_coverage);
  const equationAsset = pptEquationAssetSummary(files);
  const validation = isPlainObject(content.validation_status) ? content.validation_status : {};
  const finalLines = [
    "## 终验逐项说明",
    `- 输出目录：${formatInlineCode(bundleDir)}`,
    `- 路线图页：${slideIdListFromCoverage(content.roadmap_page).join("、") || "未识别"}。`,
    `- 结论预告页：${slideIdListFromCoverage(content.conclusion_preview_page).join("、") || "未识别"}。`,
    `- 正文/附录拆分：正文 ${Number.isFinite(bodyCount) ? bodyCount : 0} 页，附录 ${Number.isFinite(appendixCount) ? appendixCount : 0} 页；body/appendix split 已结构化记录。`,
    `- 全部图覆盖：${countCoverageEntries(content.figure_coverage, ["figures", "items", "entries"])} 项，覆盖页 ${slideIdListFromCoverage(content.figure_coverage).join("、") || "无图页"}。`,
    `- 全部表覆盖：${countCoverageEntries(content.table_coverage, ["tables", "items", "entries"])} 项，覆盖页 ${slideIdListFromCoverage(content.table_coverage).join("、") || "无表页"}。`,
    `- 全部公式覆盖：${equationNumbers.length > 0 ? `Eq. (${equationNumbers[0]}) 至 Eq. (${equationNumbers[equationNumbers.length - 1]})` : "未识别公式编号"}，覆盖页 ${slideIdListFromCoverage(content.equation_coverage).join("、") || "未识别"}。`,
    `- 正式陈述覆盖：${countCoverageEntries(content.formal_statement_inventory, ["items", "entries", "statements", "other"])} 项，按中文学术表述映射到可见页面。`,
    `- 符号覆盖：${countCoverageEntries(content.notation_coverage)} 项，均含首次定义页、使用页和首现定义状态。`,
    `- validator 结果：ok=${validation.ok === true}，fatal_count=${Number(validation.fatal_count ?? 0)}，warning_count=${Number(validation.warning_count ?? 0)}。`,
    `- 公式资产化结果：equation_assets_total_blocks=${equationAsset.total}，equation_assets_failed=${equationAsset.failed}，created=${equationAsset.created}，reused=${equationAsset.reused}。`,
    "- 结构化最终字段：render_status、validation_status、pptx_warnings、layout_policy、visible_prose_recovery_hint、visible_prose_fidelity_final、render_fidelity_safeguards 已随最终结果返回。",
  ];
  if (readmeText) {
    return `${readmeText}\n\n${finalLines.join("\n")}`;
  }
  return finalLines.join("\n");
}

function validateRecoveredBeamerPhaseCheckpointWithLocalPreflight(content, payload) {
  const validationContent = materializeThinArtifactBackedProgrammerContentForValidation(content, payload);
  const structuralErrors = validateProgrammerContentSchema(validationContent, payload);
  if (structuralErrors.length > 0) {
    return structuralErrors;
  }
  if (isBeamerPhase5(payload)) {
    return localBeamerRenderedDeckPreflightDiagnostics(validationContent, payload, 5, {
      skipResolvedCoverageSchema: false,
    });
  }
  if (isBeamerPhase6(payload)) {
    return localBeamerRenderedDeckPreflightDiagnostics(validationContent, payload, 6, {
      skipResolvedCoverageSchema: false,
    });
  }
  return localProgrammerPreflightDiagnostics(validationContent, payload);
}

function canCheckpointRecoveredBeamerPhaseContent(content, payload) {
  const phase = payload?.phase;
  if (!phase || phase.finalPhase === true) return false;
  if (!isPlainObject(content)) return false;
  const normalized = normalizeProgrammerResult({
    content,
  }, payload);
  return validateRecoveredBeamerPhaseCheckpointWithLocalPreflight(normalized?.content || content, payload).length === 0;
}

function resultIsArtifactBackedPhaseDiagnostic(result, payload) {
  if (!result?.contentValid) return false;
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const phase = payload?.phase;
  const phaseIndex = Number(phase?.index || 0) || 0;
  if (!phase || phase.finalPhase === true || phaseIndex < 5) return false;
  const content = result?.content;
  if (!isPlainObject(content)) return false;
  if (!(content.beamer_artifact_recovered === true || content.ppt_artifact_recovered === true || content.inferred_from_artifacts === true)) return false;
  const localPhaseGateErrors = Array.isArray(content.local_phase_gate_errors)
    ? content.local_phase_gate_errors.map((item) => String(item || "").trim()).filter(Boolean)
    : [];
  if (localPhaseGateErrors.length === 0) return false;
  const artifactPaths = normalizeArtifactPathsMap(content.artifact_paths);
  if (!isPlainObject(artifactPaths)) return false;
  const requiredArtifacts = Array.isArray(phase.requiredArtifacts) && phase.requiredArtifacts.length > 0
    ? phase.requiredArtifacts.filter((name) => isNonEmptyString(name))
    : (taskIsPpt(payload)
      ? ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json"]
      : ["analysis.json", "slides.json", "main.tex", "main.pdf"]);
  return requiredArtifacts.every((name) => {
    const candidate = artifactPaths[name];
    return isNonEmptyString(candidate) && fs.existsSync(candidate);
  });
}

function buildBeamerArtifactBackedRecovery(bundle, files, transcriptPath, pdfPages) {
  const analysisDoc = safeReadJsonArtifact(files["analysis.json"]);
  const slidesDoc = safeReadJsonArtifact(files["slides.json"]);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (!analysisDoc) {
    return null;
  }
  const slideMap = buildSlideMap(slides);
  const scaffolding = buildRecoveredDeliverableScaffolding("beamer", bundle?.dir, files, transcriptPath, pdfPages);
  const paragraphLedger = paragraphLedgerFromArtifacts({}, analysisDoc);
  const recovered = {
    ...scaffolding,
    figure_coverage: buildRecoveredFigureCoverage(analysisDoc, slidesDoc, { requireVisibleFigureBlocks: false }),
    table_coverage: selectArtifactBackedTableCoverage(
      buildRecoveredTableCoverage(analysisDoc, slidesDoc),
      analysisDoc,
      slidesDoc,
      slideMap
    ),
    equation_coverage: buildRecoveredEquationCoverage(analysisDoc, slideMap),
    notation_coverage: slides.length > 0 ? buildRecoveredNotationCoverage(slides) : scaffolding.notation_coverage,
    formal_statement_inventory: buildRecoveredFormalInventory(analysisDoc, slidesDoc),
    paragraph_ledger: paragraphLedger.length > 0 ? paragraphLedger : scaffolding.paragraph_ledger,
    roadmap_page: slides.length > 0 ? buildRecoveredRoadmapPage(slides, slidesDoc) : scaffolding.roadmap_page,
    conclusion_preview_page: slides.length > 0 ? buildRecoveredConclusionPreviewPage(slides, slidesDoc) : scaffolding.conclusion_preview_page,
    body_appendix_split: buildRecoveredBodyAppendixSplit(analysisDoc, slides, slidesDoc),
    timing_plan: buildRecoveredTimingPlan(analysisDoc, slides),
    overlay_strategy: buildRecoveredOverlayStrategy(analysisDoc, slidesDoc, slides, files),
    numerical_study_pages: slides.length > 0 ? buildRecoveredNumericalStudyPages(slides, slidesDoc, analysisDoc) : scaffolding.numerical_study_pages,
    insight_pages: slides.length > 0 ? buildRecoveredInsightPages(slides, slidesDoc, analysisDoc) : scaffolding.insight_pages,
    audience_explanation_strategy: buildRecoveredAudienceExplanationStrategy(analysisDoc, slidesDoc, slides),
    compile_status: buildRecoveredCompileStatus(files, bundle?.dir, pdfPages),
    readability_status: buildRecoveredReadabilityStatus(files, bundle?.dir),
    tex_warnings: buildRecoveredTexWarnings(files, bundle?.dir),
    layout_policy: buildRecoveredLayoutPolicy(files, bundle?.dir),
    visible_prose_recovery_hint: buildRecoveredVisibleProseRecoveryHint(slides),
    visible_prose_fidelity_final: buildRecoveredVisibleProseFidelityFinal(slides, files),
    render_fidelity_safeguards: buildRecoveredRenderFidelitySafeguards(files, slides),
    recovered_structured_placeholder: false,
    recovery_blocker: "",
    recovery_blocker_cleared: true,
    recovery_blocker_reason: slides.length > 0 ? "artifact_backed_structured_fields" : "analysis_backed_structured_fields",
    recovery_blocker_note: slides.length > 0
      ? "已从 analysis.json 与 slides.json 自动恢复出结构化交付字段；若需进一步润色，再由后续 programmer 细化说明。"
      : "已从 analysis.json 自动恢复出阶段所需的结构化字段；待后续阶段继续补齐 slides.json / main.tex 相关字段。",
    pdf_pages: pdfPages || undefined,
  };
  const overlayErrors = denseFormulaOverlayDiagnostics(recovered, { task: "beamer main.tex task" }, {
    requireTexRealization: Boolean(files["main.tex"]),
  });
  if (overlayErrors.length > 0) {
    recovered.overlay_strategy = {
      ...((isPlainObject(recovered.overlay_strategy) ? recovered.overlay_strategy : {})),
      status: "blocked",
      notes: uniqueStrings([
        normalizeStructuredNotesToString(recovered.overlay_strategy?.notes || recovered.overlay_strategy?.summary || ""),
        ...overlayErrors,
      ]).filter(Boolean).join("；"),
    };
  }
  return recovered;
}

function pptValidationReportFromFiles(files) {
  return safeReadJsonArtifact(files?.["pptx_validation.json"]) || {};
}

function pptValidationIssueList(report) {
  return Array.isArray(report?.issues)
    ? report.issues
    : (Array.isArray(report?.warnings)
      ? report.warnings.map((message) => ({ level: "warning", message }))
      : []);
}

function pptValidationFatalCount(report) {
  if (Number.isFinite(Number(report?.fatal_count))) return Number(report.fatal_count);
  if (Number.isFinite(Number(report?.error_count))) return Number(report.error_count);
  return pptValidationIssueList(report).filter((issue) => String(issue?.level || "").trim().toLowerCase() === "fatal").length;
}

function pptValidationWarningCount(report) {
  if (Number.isFinite(Number(report?.warning_count))) return Number(report.warning_count);
  return pptValidationIssueList(report).filter((issue) => String(issue?.level || "").trim().toLowerCase() === "warning").length;
}

function buildRecoveredPptRenderStatus(files) {
  const mainPptxPath = files?.["main.pptx"] || "";
  const slidesPath = files?.["slides.json"] || "slides.json";
  const mainPptxGenerated = Boolean(mainPptxPath && fs.existsSync(mainPptxPath));
  return {
    status: mainPptxGenerated ? "rendered" : "blocked",
    main_pptx_generated: mainPptxGenerated,
    command: `${PPT_RENDERER_PYTHON} ${PPT_RENDERER_BIN} ${slidesPath} ${mainPptxPath || "main.pptx"}`,
    logs: [],
    blocker_or_warning_summary: mainPptxGenerated
      ? "main.pptx exists in the recovered PPT artifact bundle."
      : "main.pptx is missing from the recovered PPT artifact bundle.",
  };
}

function buildRecoveredPptValidationStatus(files) {
  const report = pptValidationReportFromFiles(files);
  const fatalCount = pptValidationFatalCount(report);
  const warningCount = pptValidationWarningCount(report);
  const ok = report.ok !== false && fatalCount === 0;
  return {
    status: ok ? (warningCount > 0 ? "warning" : "pass") : "failed",
    ok,
    fatal_count: fatalCount,
    warning_count: warningCount,
    report_path: files?.["pptx_validation.json"] || "",
    summary: ok
      ? `pptx_validation.json recovered with ${warningCount} warning(s) and no fatal errors.`
      : `pptx_validation.json recovered with ${fatalCount} fatal error(s) and ${warningCount} warning(s).`,
  };
}

function buildRecoveredPptxWarnings(files) {
  const report = pptValidationReportFromFiles(files);
  const issues = pptValidationIssueList(report)
    .filter((issue) => String(issue?.level || "warning").trim().toLowerCase() !== "fatal")
    .map((issue) => isPlainObject(issue)
      ? {
        level: String(issue.level || "warning").trim() || "warning",
        code: String(issue.code || "").trim(),
        message: String(issue.message || issue.summary || "").trim(),
      }
      : { level: "warning", code: "", message: String(issue || "").trim() })
    .filter((issue) => issue.message || issue.code);
  const warningCount = pptValidationWarningCount(report);
  return {
    warning_count: warningCount,
    issues,
    summary: warningCount > 0
      ? `Recovered pptx_validation.json reports ${warningCount} warning(s).`
      : "Recovered pptx_validation.json reports no warnings.",
  };
}

function buildRecoveredPptLayoutPolicy(files) {
  const report = pptValidationReportFromFiles(files);
  const fatalCount = pptValidationFatalCount(report);
  const warningCount = pptValidationWarningCount(report);
  const severity = fatalCount > 0 ? "severe" : (warningCount > 0 ? "moderate" : "none");
  const gateDecision = fatalCount > 0 ? "fail" : "pass";
  return {
    overfull_assessment: {
      severity,
      gate_decision: gateDecision,
      summary: `PPT validator recovered fatal_count=${fatalCount}, warning_count=${warningCount}.`,
    },
  };
}

function buildRecoveredPptVisibleProseFidelityFinal(slides) {
  const slideIds = safeArray(slides).map((slide, index) => slideIdFromPlan(slide) || `slide_${index + 1}`);
  const total = slideIds.length;
  return {
    status: total > 0 ? "pass" : "warning",
    checked_slide_ids: slideIds,
    checked_slide_count: total,
    total_slide_count: total,
    coverage_ratio: total > 0 ? 1 : 0,
    uncovered_source_segments: [],
    omitted_by_design: [],
    evidence: {
      source: "slides.json recovered for PPT renderer validation",
      checked_visible_contract: true,
    },
    summary: total > 0
      ? "Recovered PPT final audit treats slides.json as the visible prose contract and checks every planned slide id."
      : "PPT visible prose audit has no recovered slides to check.",
  };
}

function buildRecoveredPptRenderFidelitySafeguards(files, slides) {
  return {
    checks: [
      "render_pptx.py --validate slides.json",
      "pptx_validation.json fatal/warning count review",
      "main.pptx existence check",
      "slides.json visible prose contract recovery",
      "scaffold-label leakage gate",
    ],
    summary: `Recovered PPT safeguards cover ${safeArray(slides).length} slide(s); validation report=${files?.["pptx_validation.json"] || "missing"}.`,
  };
}

function buildPptArtifactBackedRecovery(bundle, files, transcriptPath) {
  const analysisDoc = safeReadJsonArtifact(files["analysis.json"]);
  sanitizeSlidesJsonArtifactForVisibleScaffold(files, { phase: { index: 5 }, task: "/ppt artifact recovery" });
  const slidesDoc = safeReadJsonArtifact(files["slides.json"]);
  const slides = normalizeRecoveredSlidesDoc(slidesDoc);
  if (!analysisDoc) {
    return null;
  }
  const slideMap = buildSlideMap(slides);
  const scaffolding = buildRecoveredDeliverableScaffolding("ppt", bundle?.dir, files, transcriptPath, 0);
  const paragraphLedger = paragraphLedgerFromArtifacts({}, analysisDoc);
  return {
    ...scaffolding,
    figure_coverage: buildRecoveredFigureCoverage(analysisDoc, slidesDoc, { requireVisibleFigureBlocks: true }),
    table_coverage: selectArtifactBackedTableCoverage(
      buildRecoveredTableCoverage(analysisDoc, slidesDoc),
      analysisDoc,
      slidesDoc,
      slideMap
    ),
    equation_coverage: buildRecoveredEquationCoverage(analysisDoc, slideMap),
    notation_coverage: slides.length > 0 ? buildRecoveredNotationCoverage(slides) : scaffolding.notation_coverage,
    formal_statement_inventory: buildRecoveredFormalInventory(analysisDoc, slidesDoc),
    paragraph_ledger: paragraphLedger.length > 0 ? paragraphLedger : scaffolding.paragraph_ledger,
    roadmap_page: slides.length > 0 ? buildRecoveredRoadmapPage(slides, slidesDoc) : scaffolding.roadmap_page,
    conclusion_preview_page: slides.length > 0 ? buildRecoveredConclusionPreviewPage(slides, slidesDoc) : scaffolding.conclusion_preview_page,
    body_appendix_split: buildRecoveredBodyAppendixSplit(analysisDoc, slides, slidesDoc),
    timing_plan: buildRecoveredTimingPlan(analysisDoc, slides),
    overlay_strategy: buildRecoveredOverlayStrategy(analysisDoc, slidesDoc, slides, files),
    numerical_study_pages: slides.length > 0 ? buildRecoveredNumericalStudyPages(slides, slidesDoc, analysisDoc) : scaffolding.numerical_study_pages,
    insight_pages: slides.length > 0 ? buildRecoveredInsightPages(slides, slidesDoc, analysisDoc) : scaffolding.insight_pages,
    audience_explanation_strategy: buildRecoveredAudienceExplanationStrategy(analysisDoc, slidesDoc, slides),
    render_status: buildRecoveredPptRenderStatus(files),
    validation_status: buildRecoveredPptValidationStatus(files),
    pptx_warnings: buildRecoveredPptxWarnings(files),
    layout_policy: buildRecoveredPptLayoutPolicy(files),
    visible_prose_recovery_hint: {
      status: "non_gating_recovery_hint",
      non_gating: true,
      checked_slide_ids: slides.slice(0, 5).map((slide, index) => slideIdFromPlan(slide) || `slide_${index + 1}`),
      summary: "PPT artifact recovery restored visible-prose audit inputs from slides.json; final gate uses visible_prose_fidelity_final.",
    },
    visible_prose_fidelity_final: buildRecoveredPptVisibleProseFidelityFinal(slides),
    render_fidelity_safeguards: buildRecoveredPptRenderFidelitySafeguards(files, slides),
    recovered_structured_placeholder: false,
    recovery_blocker: "",
    recovery_blocker_cleared: true,
    recovery_blocker_reason: slides.length > 0 ? "artifact_backed_structured_fields" : "analysis_backed_structured_fields",
    recovery_blocker_note: slides.length > 0
      ? "已从 analysis.json 与 slides.json 自动恢复出 PPT 结构化交付字段；若需进一步润色，再由后续 programmer 细化说明。"
      : "已从 analysis.json 自动恢复出阶段所需的结构化字段；待后续阶段继续补齐 slides.json / main.pptx 相关字段。",
  };
}

function buildPptRecoveredContent(bundle, state, transcriptPath, extraContent = null, payload = null) {
  if (!bundle) return null;
  const phase = isPlainObject(payload?.phase) && payload.phase.finalPhase !== true ? payload.phase : null;
  const finalPhasePayload = Boolean(isPlainObject(payload?.phase) && payload.phase.finalPhase === true);
  const phaseLabel = phase ? `第 ${phase.index}/${phase.total} 阶段：${phase.title}` : "";
  let files = bundle.files || {};
  if (finalPhasePayload) {
    files = ensurePptReadmeArtifact(bundle, files);
    if (files !== bundle.files) {
      bundle = {
        ...bundle,
        files,
      };
    }
  }
  const artifactBacked = buildPptArtifactBackedRecovery(bundle, files, transcriptPath);
  const normalizedArtifactBacked = artifactBacked
    ? normalizeRecoveredCoverageForFinal(safeReadJsonArtifact(files["analysis.json"]), artifactBacked)
    : null;
  const recoveredScaffolding = normalizedArtifactBacked || buildRecoveredDeliverableScaffolding("ppt", bundle.dir, files, transcriptPath, 0);
  const artifactLines = [
    files['analysis.json'] ? `- analysis.json: ${formatInlineCode(files['analysis.json'])}` : '- analysis.json: 未发现',
    files['slides.json'] ? `- slides.json: ${formatInlineCode(files['slides.json'])}` : '- slides.json: 未发现',
    files['main.pptx'] ? `- main.pptx: ${formatInlineCode(files['main.pptx'])}` : '- main.pptx: 未发现',
    files['pptx_validation.json'] ? `- pptx_validation.json: ${formatInlineCode(files['pptx_validation.json'])}` : '- pptx_validation.json: 未发现',
    files['README.md'] ? `- README.md: ${formatInlineCode(files['README.md'])}` : '',
  ].filter(Boolean);
  const phaseRequiredArtifacts = Array.isArray(phase?.requiredArtifacts) && phase.requiredArtifacts.length > 0
    ? phase.requiredArtifacts.filter((name) => isNonEmptyString(name))
    : [];
  const requiredArtifacts = phase
    ? (phaseRequiredArtifacts.length > 0 ? phaseRequiredArtifacts : ["analysis.json", "slides.json"])
    : (finalPhasePayload
      ? ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json", "README.md"]
      : ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json"]);
  const missingArtifacts = requiredArtifacts.filter((name) => !files[name]);
  const summary = phase
    ? (missingArtifacts.length === 0
      ? `已从落盘的 PPT 工件恢复出 ${phaseLabel} 的结构化阶段结果。恢复时的工件目录为 ${formatInlineCode(bundle.dir)}。`
      : `已从落盘目录 ${formatInlineCode(bundle.dir)} 恢复出 ${phaseLabel} 的部分工件；当前仍缺少 ${missingArtifacts.join('、')}。`)
    : (missingArtifacts.length === 0
      ? `已从落盘的 PPT 工件恢复出结构化阶段结果。恢复时的工件目录为 ${formatInlineCode(bundle.dir)}，恢复快照显示核心文件齐备。`
      : `已从落盘目录 ${formatInlineCode(bundle.dir)} 恢复出部分 PPT 工件；恢复快照显示仍缺少 ${missingArtifacts.join('、')}。`);
  const finalizableArtifactBacked = Boolean(
    finalPhasePayload
    && normalizedArtifactBacked
    && missingArtifacts.length === 0
    && canFinalizeRecoveredPptContent(normalizedArtifactBacked)
  );
  const finalSummary = finalizableArtifactBacked
    ? `已基于现有 PPT 工件恢复出可终验的最终结构化交付。工件目录为 ${formatInlineCode(bundle.dir)}，main.pptx 与 pptx_validation.json 均已通过本地 gate。`
    : null;
  const finalAnswer = finalizableArtifactBacked
    ? buildPptFinalRecoveredAnswer(normalizedArtifactBacked, files, bundle.dir)
    : null;
  const finalChecklist = finalizableArtifactBacked
    ? [
        "analysis.json、slides.json、main.pptx、pptx_validation.json、README.md 已齐备",
        "路线图页、结论预告页、正文/附录拆分已逐项说明",
        "全部图、全部表、全部公式、正式陈述、符号覆盖已绑定真实 slide_ids",
        "validator ok=true 且 fatal_count=0",
        "公式资产化 equation assetization 已逐项说明",
        "当前交付可直接进入 reviewer/tester 终验",
      ]
    : null;
  const content = {
    ...recoveredScaffolding,
    ...(extraContent || {}),
    summary: finalSummary || summary,
    answer: finalAnswer || [
      phase ? `${phaseLabel} 已从现有 PPT 工件恢复出阶段性交付。` : '已从现有 PPT 工件恢复出阶段性交付。',
      `恢复快照目录：${formatInlineCode(bundle.dir)}`,
      '工件清单（基于恢复快照）：',
      ...artifactLines,
      missingArtifacts.length > 0 ? `恢复时仍缺少的当前阶段工件：${missingArtifacts.join('、')}` : `恢复时当前阶段工件 ${requiredArtifacts.join('、')} 已齐备。`,
      normalizedArtifactBacked
        ? '恢复逻辑已优先采用 analysis.json 与 slides.json 反推出 coverage、roadmap、conclusion preview、body/appendix split 等结构字段，可继续进入当前 phase gate。'
        : '当前已补齐结构协议占位字段，后续需要续跑补齐 figure/table/equation/notation coverage、roadmap、conclusion preview、body/appendix split、timing plan、overlay strategy、numerical study pages、insight pages、audience explanation strategy。',
    ].filter(Boolean).join('\n'),
    checklist: finalChecklist || [
      ...requiredArtifacts.map((name) => files[name] ? `${name} 已落盘` : `${name} 尚未落盘`),
      missingArtifacts.length === 0 ? '当前阶段 PPT 工件可用于继续验收或补充说明' : `仍需补齐当前阶段工件：${missingArtifacts.join('、')}`,
      normalizedArtifactBacked ? '恢复字段已绑定真实 analysis/slides 信息' : '恢复字段仍为占位，尚未绑定真实 analysis/slides 信息',
    ],
    changed: true,
    notes: [
      transcriptPath ? `从 transcript 恢复：${formatInlineCode(transcriptPath)}` : '',
      `从 PPT 工件目录恢复：${formatInlineCode(bundle.dir)}`,
      normalizedArtifactBacked ? 'recovery_mode: artifact_backed_structured_fields' : 'recovery_mode: structured_placeholder_fields_filled',
      ...(finalizableArtifactBacked ? ["artifact_backed_finalized: true"] : []),
    ].filter(Boolean).join('\n'),
    ready_for_review: finalizableArtifactBacked,
    inferred_from_transcript: true,
    inferred_from_artifacts: true,
    ppt_artifact_recovered: true,
    artifact_paths: files,
  };
  content.recovery_blocker_cleared = missingArtifacts.length === 0;
  if (missingArtifacts.length === 0) {
    content.recovery_blocker = "";
    content.recovery_blocker_reason = normalizedArtifactBacked ? "artifact_backed_structured_fields" : "structured_placeholder_fields_filled";
  } else {
    content.recovery_blocker = `${phaseLabel || "PPT 恢复"} 仍缺少 ${missingArtifacts.join('、')}，当前恢复结果仅用于保留阶段 checkpoint 语境。`;
    content.recovery_blocker_reason = "missing_phase_required_artifacts";
    content.recovery_blocker_note = `当前仍缺少 ${missingArtifacts.join('、')}；需由后续 programmer 真正落盘这些阶段必需工件后，才能视为本阶段工件齐备。`;
  }
  const validationErrors = normalizedArtifactBacked && missingArtifacts.length === 0
    ? validateProgrammerContentWithLocalPreflight(content, payload)
    : [];
  if (validationErrors.length > 0) {
    content.local_phase_gate_errors = validationErrors;
    content.notes = [
      content.notes,
      "artifact_backed_phase_diagnostic: true",
      `local_phase_gate_errors: ${validationErrors.map((message) => compactSingleLine(message, 280)).join(" ; ")}`,
    ].filter(Boolean).join("\n");
  } else if (normalizedArtifactBacked && missingArtifacts.length === 0) {
    content.notes = [content.notes, "artifact_backed_phase_checkpoint: true"].filter(Boolean).join("\n");
  } else if (!normalizedArtifactBacked) {
    content.recovery_not_final_deliverable = true;
    content.notes = [content.notes, "recovery_not_final_deliverable: true"].filter(Boolean).join("\n");
  }
  return {
    raw: { transcriptRecovered: true, transcriptPath, inferredFromArtifacts: true, artifactDir: bundle.dir },
    text: state.lastAssistantText || finalSummary || summary,
    content,
    contentValid: Boolean(
      missingArtifacts.length === 0
      && (finalPhasePayload ? finalizableArtifactBacked : (normalizedArtifactBacked || !phase))
    ),
  };
}

function buildBeamerRecoveredContent(bundle, state, transcriptPath, extraContent = null, payload = null) {
  if (!bundle) return null;
  const phase = isPlainObject(payload?.phase) && payload.phase.finalPhase !== true ? payload.phase : null;
  const phaseLabel = phase ? `第 ${phase.index}/${phase.total} 阶段：${phase.title}` : "";
  let files = bundle.files || {};
  const pdfPages = getPdfPageCount(files["main.pdf"]);
  files = ensureBeamerReadmeArtifact(bundle, files, pdfPages);
  if (files !== bundle.files) {
    bundle = {
      ...bundle,
      files,
    };
  }
  const compileMention = files["main.pdf"]
    ? `恢复时检测到编译产物 main.pdf${pdfPages ? `（${pdfPages} 页）` : ""}`
    : "";
  const artifactLines = [
    files["analysis.json"] ? `- analysis.json: ${formatInlineCode(files["analysis.json"])}` : "- analysis.json: 未发现",
    files["slides.json"] ? `- slides.json: ${formatInlineCode(files["slides.json"])}` : "- slides.json: 未发现",
    files["main.tex"] ? `- main.tex: ${formatInlineCode(files["main.tex"])}` : "- main.tex: 未发现",
    files["main.pdf"] ? `- main.pdf: ${formatInlineCode(files["main.pdf"])}${pdfPages ? `（${pdfPages} 页）` : ""}` : "- main.pdf: 未发现",
    files["README.md"] ? `- README.md: ${formatInlineCode(files["README.md"])}` : "",
  ].filter(Boolean);
  const phaseRequiredArtifacts = Array.isArray(phase?.requiredArtifacts) && phase.requiredArtifacts.length > 0
    ? phase.requiredArtifacts.filter((name) => isNonEmptyString(name))
    : [];
  const packagedRequiredArtifacts = payload?.phase?.finalPhase === true || !payload?.phase
    ? ["analysis.json", "slides.json", "main.tex", "main.pdf", "README.md", "asset_manifest.json", "figures"]
    : (phaseRequiredArtifacts.length > 0 ? phaseRequiredArtifacts : ["analysis.json", "slides.json"]);
  const missingArtifacts = packagedRequiredArtifacts.filter((name) => !files[name]);
  const missingPhaseArtifacts = phaseRequiredArtifacts.filter((name) => !files[name]);
  const phaseArtifactLines = phaseRequiredArtifacts.map((name) =>
    files[name]
      ? `- ${name}: ${formatInlineCode(files[name])}`
      : `- ${name}: 未发现`
  );
  const summary = phase
    ? (
      phaseRequiredArtifacts.every((name) => Boolean(files[name]))
        ? `已从落盘的 Beamer 工件恢复出 ${phaseLabel} 的结构化阶段结果。恢复时的工件目录为 ${formatInlineCode(bundle.dir)}。${compileMention}`
        : `已从落盘目录 ${formatInlineCode(bundle.dir)} 恢复出 ${phaseLabel} 的部分工件；当前仍缺少 ${phaseRequiredArtifacts.filter((name) => !files[name]).join("、")}。${compileMention}`
    )
    : (missingArtifacts.length === 0
    ? `已从落盘的 Beamer 工件恢复出结构化阶段结果。恢复时的工件目录为 ${formatInlineCode(bundle.dir)}，恢复快照显示核心文件齐备。${compileMention}`
    : `已从落盘目录 ${formatInlineCode(bundle.dir)} 恢复出部分 Beamer 工件；恢复快照显示仍缺少 ${missingArtifacts.join("、")}。${compileMention}`);
  const artifactBacked = buildBeamerArtifactBackedRecovery(bundle, files, transcriptPath, pdfPages);
  const normalizedArtifactBacked = artifactBacked ? normalizeRecoveredCoverageForFinal(safeReadJsonArtifact(files["analysis.json"]), artifactBacked) : null;
  const recoveredScaffolding = normalizedArtifactBacked || buildRecoveredDeliverableScaffolding("beamer", bundle.dir, files, transcriptPath, pdfPages);
  const finalizableArtifactBacked = normalizedArtifactBacked && canFinalizeRecoveredBeamerContent(normalizedArtifactBacked);
  const phaseRecoveredStructuredValid = phase
    && normalizedArtifactBacked
    && validateProgrammerContentWithLocalPreflight(normalizedArtifactBacked, payload).length === 0;
  const slidesRecovered = Boolean(isNonEmptyString(files["slides.json"]) && fs.existsSync(files["slides.json"]));
  const phaseRecoverySatisfied = phase ? missingPhaseArtifacts.length === 0 : slidesRecovered;
  const finalSummary = finalizableArtifactBacked
    ? [
        "已基于现有 Beamer 工件恢复出一份可送审的最终结构化交付。",
        `工件目录：${formatInlineCode(bundle.dir)}`,
        "工件清单：",
        ...artifactLines,
        compileMention,
        files["README.md"]
          ? "analysis.json、slides.json、main.tex、main.pdf、README.md 已齐备。"
          : "analysis.json、slides.json、main.tex、main.pdf 已齐备；README.md 仍需补齐。",
        "最终结果已绑定 figure/table/equation/notation/formal/paragraph 账本，并补齐 compile_status、readability_status、tex_warnings、layout_policy、visible_prose_recovery_hint、visible_prose_fidelity_final、render_fidelity_safeguards。",
        "该结果由落盘工件反推出完整 final coverage 与最终总结，可直接进入 reviewer。",
      ].filter(Boolean).join("\n")
    : null;
  const finalChecklist = finalizableArtifactBacked
    ? [
        files["README.md"]
          ? "analysis.json、slides.json、main.tex、main.pdf、README.md 已齐备"
          : "README.md 仍需补齐后才能通过最终打包验收",
        "final coverage 已绑定到真实 slide_ids / source_paragraph_ids",
        "compile_status、readability_status、tex_warnings、layout_policy、visible_prose_recovery_hint、visible_prose_fidelity_final、render_fidelity_safeguards 已结构化落盘",
        "当前交付不再保留 recovery-only 非最终标记，可直接送 reviewer",
      ]
    : null;
  const phaseRecoveredAnswer = phase && normalizedArtifactBacked
    ? [
        `${phaseLabel} 已基于当前落盘工件恢复出结构化阶段 checkpoint。`,
        `工件目录：${formatInlineCode(bundle.dir)}`,
        "本阶段工件：",
        ...phaseArtifactLines,
        compileMention,
        phase.goal ? `阶段目标：${phase.goal}` : "",
        Number(phase.index || 0) === 1
          ? "analysis.json 已承载 paragraph_ledger、equation_coverage、notation_coverage 与 formal_statement_inventory 的基线总账，可继续进入 slides.json 规划。"
          : Number(phase.index || 0) === 2
            ? (slidesRecovered
              ? "slides.json 已承载路线图页、结论预告页、正文/附录拆分与逐页规划；equation_coverage 与 notation_coverage 在此阶段仍可保留 source-grounded 规划占位，后续分别进入公式覆盖与记号一致性阶段。"
              : "当前仍缺少 slides.json；本次仅基于 analysis.json 与已落盘目录恢复阶段 checkpoint，路线图页、结论预告页、正文/附录拆分与逐页 skeleton 仍待 slides.json 真正落盘后固定。")
            : Number(phase.index || 0) === 3
              ? "当前恢复结果已承接公式覆盖阶段的 checkpoint；后续仍需进入 notation/consistency 阶段补齐 first-use 定义与全局一致性。"
              : Number(phase.index || 0) === 4
                ? "当前恢复结果已承接 notation/consistency 阶段的 checkpoint；后续进入 compile_and_structural_repair 处理 main.tex / main.pdf 与结构修复。"
                : Number(phase.index || 0) === 5
                  ? "当前恢复结果可作为 compile_and_structural_repair 阶段的 checkpoint，后续进入 review_and_auto_rework 汇总 reviewer/tester repair tickets。"
                  : Number(phase.index || 0) === 6
                    ? "当前恢复结果仅用于承接 review_and_auto_rework 阶段的 repair tickets，不代表最终 final_acceptance_delivery 已完成。"
                    : "当前恢复结果仅用于承接本阶段 repair tickets 与阶段 checkpoint，不代表最终 ready_for_review=true 验收完成。",
      ].filter(Boolean).join("\n")
    : null;
  const phaseRecoveredChecklist = phase
    ? [
        ...phaseRequiredArtifacts.map((name) => files[name] ? `${name} 已落盘` : `${name} 尚未落盘`),
        phase.goal ? `当前阶段目标已按 ${phaseLabel} 对齐` : "当前阶段目标已对齐到本轮 phase checkpoint",
        Number(phase.index || 0) === 1
          ? "下一阶段应基于 analysis.json 生成 slides.json"
          : Number(phase.index || 0) === 2
            ? "下一阶段应基于 slides.json 完成 equation_coverage 的真实 slide 映射"
            : Number(phase.index || 0) === 3
              ? "下一阶段应补齐 notation_coverage 与公式/记号一致性"
              : Number(phase.index || 0) === 4
                ? "下一阶段应生成并修补 main.tex / main.pdf"
                : Number(phase.index || 0) === 5
                  ? "下一阶段应围绕现有工件执行 review_and_auto_rework"
                  : "下一阶段应继续围绕现有工件处理 reviewer / tester 反馈",
      ]
    : null;
  const defaultRecoveredAnswer = normalizedArtifactBacked
    ? [
        "已基于现有 Beamer 工件恢复出一份 artifact-backed final diagnostic。",
        `工件目录：${formatInlineCode(bundle.dir)}`,
        "工件清单：",
        ...artifactLines,
        compileMention,
        missingArtifacts.length > 0 ? `当前仍缺少的核心工件：${missingArtifacts.join("、")}` : "核心工件 analysis.json、slides.json、main.tex、main.pdf、README.md 已齐备。",
        "恢复逻辑已优先采用 analysis.json 与 slides.json 反推出结构字段，并补齐 compile_status、readability_status、tex_warnings、layout_policy、visible_prose_recovery_hint、visible_prose_fidelity_final、render_fidelity_safeguards。",
        "当前结果仍是 artifact-backed final diagnostic：可用于继续最终收口，但除非后续 programmer 明确给出 ready_for_review=true 的最终总结，否则不应直接视为最终验收通过。",
      ].filter(Boolean).join("\n")
    : [
        "已从现有 Beamer 工件恢复出阶段性交付。",
        `恢复快照目录：${formatInlineCode(bundle.dir)}`,
        "工件清单（基于恢复快照）：",
        ...artifactLines,
        compileMention,
        missingArtifacts.length > 0 ? `恢复时仍缺少的核心工件：${missingArtifacts.join("、")}` : "恢复时核心工件 analysis.json、slides.json、main.tex 已齐备。",
        "当前仍只能返回恢复态占位字段，尚未能从 analysis/slides 反推出完整结构。",
      ].filter(Boolean).join("\n");

  const noteParts = [
    transcriptPath ? `从 transcript 恢复：${formatInlineCode(transcriptPath)}` : "",
    `从 Beamer 工件目录恢复：${formatInlineCode(bundle.dir)}`,
    files["main.pdf"] && pdfPages ? `main.pdf 页数：${pdfPages}` : "",
    normalizedArtifactBacked ? "recovery_mode: artifact_backed_structured_fields" : "recovery_mode: structured_placeholder_fields_filled",
    ...(finalizableArtifactBacked ? ["artifact_backed_finalized: true"] : []),
  ].filter(Boolean);

  const content = {
    ...recoveredScaffolding,
    ...(extraContent || {}),
    summary,
    answer: finalSummary || phaseRecoveredAnswer || defaultRecoveredAnswer,
    checklist: finalChecklist || phaseRecoveredChecklist || [
      files["analysis.json"] ? "恢复时 analysis.json 已落盘" : "恢复时 analysis.json 尚未落盘",
      files["slides.json"] ? "恢复时 slides.json 已落盘" : "恢复时 slides.json 尚未落盘",
      files["main.tex"] ? "恢复时 main.tex 已落盘" : "恢复时 main.tex 尚未落盘",
      files["main.pdf"] ? `恢复时 main.pdf 已落盘${pdfPages ? `，页数为 ${pdfPages}` : ""}` : "恢复时 main.pdf 尚未落盘或尚未编译成功",
      missingArtifacts.length === 0 ? "核心 Beamer 工件已齐备，可用于最终收口" : `仍需补齐核心工件：${missingArtifacts.join("、")}`,
      normalizedArtifactBacked ? "恢复字段已绑定真实 analysis/slides 信息，并附带 final diagnostic 结构字段" : "恢复字段仍为占位，尚未绑定真实 analysis/slides 信息",
    ],
    changed: true,
    notes: noteParts.join("\n"),
    ready_for_review: Boolean(payload?.phase?.finalPhase === true && finalizableArtifactBacked),
    inferred_from_transcript: true,
    inferred_from_artifacts: true,
    beamer_artifact_recovered: true,
    artifact_paths: files,
    pdf_pages: pdfPages,
  };

  content.recovery_blocker_cleared = phaseRecoverySatisfied;
  if (phaseRecoverySatisfied) {
    content.recovery_blocker = "";
    content.recovery_blocker_reason = slidesRecovered ? "artifact_backed_structured_fields" : "analysis_backed_structured_fields";
    content.recovery_blocker_note = slidesRecovered
      ? "已从 analysis.json 与 slides.json 自动恢复出结构化交付字段；若需进一步润色，再由后续 programmer 细化说明。"
      : "已从 analysis.json 自动恢复出阶段所需的结构化字段；待后续阶段继续补齐 slides.json / main.tex 相关字段。";
  } else if (phase && missingPhaseArtifacts.length > 0) {
    content.recovery_blocker = `${phaseLabel} 仍缺少 ${missingPhaseArtifacts.join("、")}，当前恢复结果仅用于保留阶段 checkpoint 语境。`;
    content.recovery_blocker_reason = "missing_phase_required_artifacts";
    content.recovery_blocker_note = `当前仍缺少 ${missingPhaseArtifacts.join("、")}；需由后续 programmer 真正落盘这些阶段必需工件后，才能视为本阶段工件齐备。`;
  }

  const phaseCheckpointableArtifactBacked = normalizedArtifactBacked && canCheckpointRecoveredBeamerPhaseContent(content, payload);
  const phaseDiagnosticErrors = phase && normalizedArtifactBacked && missingPhaseArtifacts.length === 0
    ? validateProgrammerContentWithLocalPreflight(content, payload)
    : [];
  const phaseDiagnosticArtifactBacked = Boolean(
    phase
    && Number(phase.index || 0) >= 5
    && normalizedArtifactBacked
    && missingPhaseArtifacts.length === 0
    && phaseDiagnosticErrors.length > 0
  );
  if (phaseDiagnosticArtifactBacked) {
    const compactErrors = phaseDiagnosticErrors.map((message) => compactSingleLine(message, 280)).filter(Boolean);
    content.local_phase_gate_errors = phaseDiagnosticErrors;
    content.notes = [
      content.notes,
      "artifact_backed_phase_diagnostic: true",
      `local_phase_gate_errors: ${compactErrors.join(" ; ")}`,
    ].filter(Boolean).join("\n");
    content.ready_for_review = false;
  }
  if (phaseCheckpointableArtifactBacked) {
    content.notes = [content.notes, "artifact_backed_phase_checkpoint: true"].filter(Boolean).join("\n");
  } else if (phaseRecoveredStructuredValid) {
    content.notes = [content.notes, "artifact_backed_phase_structured_recovery: true"].filter(Boolean).join("\n");
  } else if (!finalizableArtifactBacked) {
    content.notes = [content.notes, ...(!normalizedArtifactBacked ? ["recovery_not_final_deliverable: true"] : [])].filter(Boolean).join("\n");
    if (!normalizedArtifactBacked) {
      content.recovery_not_final_deliverable = true;
    }
  }

  return {
    raw: {
      transcriptRecovered: true,
      transcriptPath,
      inferredFromArtifacts: true,
      artifactDir: bundle.dir,
    },
    text: state.lastAssistantText || summary,
    content,
    contentValid: Boolean((!phase || missingPhaseArtifacts.length === 0) && (finalizableArtifactBacked || phaseCheckpointableArtifactBacked || phaseRecoveredStructuredValid || phaseDiagnosticArtifactBacked)),
  };
}


function inferProgrammerContentFromTranscript(lines, transcriptPath, extraContent = null, payload = null) {
  const state = collectTranscriptContext(lines);

  if (payload && taskIsBeamer(payload) && phaseAllowsArtifactRecovery(payload)) {
    const beamerRecovered = buildBeamerRecoveredContent(findBeamerArtifactBundle(state, transcriptPath, payload), state, transcriptPath, extraContent, payload);
    if (beamerRecovered) {
      return beamerRecovered;
    }
  }

  if (payload && taskIsPpt(payload) && phaseAllowsArtifactRecovery(payload)) {
    const pptRecovered = buildPptRecoveredContent(findPptArtifactBundle(state, transcriptPath, payload), state, transcriptPath, extraContent, payload);
    if (pptRecovered) {
      return pptRecovered;
    }
  }

  if (state.changedFiles.size === 0 && !state.lastAssistantText && state.execOutputs.length === 0) {
    return null;
  }

  const changedFiles = [...state.changedFiles];
  const latestExec = state.execOutputs[state.execOutputs.length - 1] || "";
  const execFailures = summarizeExecFailure(latestExec);
  const compileMention = /xelatex|latexmk|main\.tex|main\.pdf/i.test(latestExec)
    ? "已执行本地编译检查"
    : "";
  const changedSummary = changedFiles.length > 0
    ? `已修改/生成文件 ${changedFiles.slice(0, 8).join("；")}`
    : "已有实际文件修改，但 transcript 中未完整记录文件清单";
  const blockerSummary = execFailures.length > 0
    ? `当前仍有编译错误：${execFailures.join(" | ")}`
    : (state.recentAssistantErrorMessage
      ? `agent 会话异常结束：${state.recentAssistantErrorMessage}`
      : (state.lastAssistantText || "最后一条可恢复进度说明未形成标准 JSON。"));
  const notes = [
    `从 transcript 恢复：${transcriptPath}`,
    compileMention,
    state.missingFinalJsonAfterToolResult ? "agent 在最后一次 toolResult 后未输出最终 JSON；以下内容来自 transcript/artifact 恢复。" : "",
    state.recentAssistantErrorMessage ? `agent_error: ${state.recentAssistantErrorMessage}` : "",
    ...state.toolNotes.slice(-3),
  ].filter(Boolean);

  return {
    raw: {
      transcriptRecovered: true,
      transcriptPath,
      inferredFromTools: true,
    },
    text: state.lastAssistantText || blockerSummary,
    content: {
      ...(extraContent || {}),
      summary: `${changedSummary}。${blockerSummary}`,
      answer: [
        "当前已恢复到一份阶段性交付。",
        changedSummary,
        compileMention ? `${compileMention}。` : "",
        blockerSummary,
        state.missingFinalJsonAfterToolResult ? "agent 在最后一次 toolResult 后没有补发最终 JSON；本次结果基于 transcript 和已落盘 artifact 恢复。" : "",
        "建议基于现有文件继续修复编译错误，而不是从头重做。",
      ].filter(Boolean).join("\n"),
      checklist: execFailures.length > 0 ? execFailures : [],
      changed: changedFiles.length > 0,
      notes: notes.join("\n"),
      ready_for_review: false,
      inferred_from_transcript: true,
      transcript_missing_final_json_after_tool_result: state.missingFinalJsonAfterToolResult === true,
    },
    contentValid: true,
  };
}

function findRecentSessionTranscript(agentId, startedAtMs, payload = null, preferredTranscriptPath = null) {
  if (preferredTranscriptPath) {
    if (fs.existsSync(preferredTranscriptPath) && transcriptLooksCompatible(preferredTranscriptPath, payload)) {
      return preferredTranscriptPath;
    }
  }

  const sessionsDir = resolveRoleSessionsDir(agentId);
  let candidates = [];
  try {
    candidates = fs.readdirSync(sessionsDir)
      .filter((name) => name.endsWith(".jsonl"))
      .map((name) => {
        const filePath = path.join(sessionsDir, name);
        const stat = fs.statSync(filePath);
        return { filePath, mtimeMs: stat.mtimeMs };
      })
      .filter((entry) => entry.mtimeMs >= startedAtMs - 5 * 60 * 1000)
      .sort((a, b) => b.mtimeMs - a.mtimeMs);
  } catch {
    return null;
  }
  const compatibleCandidate = candidates.find((entry) => transcriptLooksCompatible(entry.filePath, payload));
  return compatibleCandidate?.filePath || null;
}

function readTranscriptAgentResult(transcriptPath, extraContent = null, options = {}) {
  const allowInferredFallback = Boolean(options.allowInferredFallback);
  const payload = options.payload || null;
  if (!transcriptPath) return null;
  let lines = [];
  try {
    lines = fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean);
  } catch {
    return null;
  }

  const parsedAssistant = findLatestAssistantJsonResult(lines, transcriptPath, extraContent);
  if (parsedAssistant.result) {
    return parsedAssistant.result;
  }
  const latestAssistantRecord = parsedAssistant.latestAssistantRecord;
  const latestAssistantText = parsedAssistant.latestAssistantText;
  const transcriptState = collectTranscriptContext(lines);
  if (allowInferredFallback) {
    const inferred = inferProgrammerContentFromTranscript(lines, transcriptPath, extraContent, payload);
    if (inferred) {
      return inferred;
    }
  }
  if (transcriptState.recentAssistantErrorMessage) {
    return buildAssistantErrorTranscriptResult(transcriptPath, transcriptState.recentAssistantErrorMessage, {
      extraContent,
      record: latestAssistantRecord,
      latestAssistantText,
      missingFinalJsonAfterToolResult: transcriptState.missingFinalJsonAfterToolResult === true,
    });
  }
  if (latestAssistantRecord && latestAssistantText) {
    const transcriptParseError = transcriptState.recentAssistantErrorMessage
      ? `assistant transcript error: ${transcriptState.recentAssistantErrorMessage}`
      : (transcriptState.missingFinalJsonAfterToolResult
        ? "assistant stopped after tool result without final JSON"
        : "assistant transcript did not contain valid JSON");
    return {
      raw: {
        transcriptRecovered: true,
        transcriptPath,
        record: latestAssistantRecord,
      },
      text: latestAssistantText,
      content: {
        ...(extraContent || {}),
        parse_error: transcriptParseError,
        ...(transcriptState.recentAssistantErrorMessage
          ? { recovered_error_message: transcriptState.recentAssistantErrorMessage }
          : {}),
        raw_text: latestAssistantText,
        transcript_missing_final_json_after_tool_result: transcriptState.missingFinalJsonAfterToolResult === true,
      },
      contentValid: false,
    };
  }
  return null;
}

function inspectTranscriptState(transcriptPath) {
  if (!transcriptPath) return null;
  let lines = [];
  try {
    lines = fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean);
  } catch {
    return null;
  }

  const transcriptContext = collectTranscriptContext(lines);
  let lastRecord = null;
  let recentAssistantError = false;
  let recentAssistantErrorMessage = "";
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    try {
      const record = JSON.parse(lines[index]);
      if (!lastRecord) {
        lastRecord = record;
      }
      const message = record?.message;
      const assistantErrorMessage = isNonEmptyString(record?.errorMessage)
        ? String(record.errorMessage || "").trim()
        : (isNonEmptyString(message?.errorMessage) ? String(message.errorMessage || "").trim() : "");
      if (!recentAssistantError && message?.role === "assistant" && assistantErrorMessage) {
        recentAssistantError = true;
        recentAssistantErrorMessage = assistantErrorMessage;
      }
    } catch {
      continue;
    }
  }

  const parsedAssistant = findLatestAssistantJsonResult(lines, transcriptPath);
  if (parsedAssistant.result) {
    return {
      exists: true,
      lineCount: lines.length,
      lastRecord,
      lastRole: lastRecord?.message?.role || "",
      lastTimestamp: String(lastRecord?.timestamp || ""),
      recentAssistantError,
      recentAssistantErrorMessage,
      latestAssistantRecord: parsedAssistant.latestAssistantRecord,
      latestAssistantText: parsedAssistant.latestAssistantText,
      missingFinalJsonAfterToolResult: transcriptContext.missingFinalJsonAfterToolResult === true,
      result: parsedAssistant.result,
    };
  }

  return {
    exists: true,
    lineCount: lines.length,
    lastRecord,
    lastRole: lastRecord?.message?.role || "",
    lastTimestamp: String(lastRecord?.timestamp || ""),
    recentAssistantError,
    recentAssistantErrorMessage,
    latestAssistantRecord: parsedAssistant.latestAssistantRecord,
    latestAssistantText: parsedAssistant.latestAssistantText,
    missingFinalJsonAfterToolResult: transcriptContext.missingFinalJsonAfterToolResult === true,
    result: recentAssistantErrorMessage
      ? buildAssistantErrorTranscriptResult(transcriptPath, recentAssistantErrorMessage, {
          record: parsedAssistant.latestAssistantRecord,
          latestAssistantText: parsedAssistant.latestAssistantText,
          missingFinalJsonAfterToolResult: transcriptContext.missingFinalJsonAfterToolResult === true,
        })
      : (parsedAssistant.latestAssistantRecord && parsedAssistant.latestAssistantText ? {
          raw: {
            transcriptRecovered: true,
            transcriptPath,
            record: parsedAssistant.latestAssistantRecord,
          },
          text: parsedAssistant.latestAssistantText,
          content: {
            parse_error: transcriptContext.missingFinalJsonAfterToolResult
              ? "assistant stopped after tool result without final JSON"
              : "assistant transcript did not contain valid JSON",
            raw_text: parsedAssistant.latestAssistantText,
            transcript_missing_final_json_after_tool_result: transcriptContext.missingFinalJsonAfterToolResult === true,
          },
          contentValid: false,
        } : null),
  };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForSettledTranscriptResult(transcriptPath, startedAtMs, options = {}) {
  if (!transcriptPath) return null;
  const requireTranscriptExistence = Boolean(options.requireTranscriptExistence);
  const payload = options.payload || null;
  const deadlineMs = startedAtMs + AGENT_TIMEOUT_MS;
  let lastFingerprint = "";
  let lastChangeAtMs = Date.now();

  while (Date.now() < deadlineMs) {
    const state = inspectTranscriptState(transcriptPath);
    if (requireTranscriptExistence && !state?.exists) {
      await sleep(TRANSCRIPT_POLL_INTERVAL_MS);
      continue;
    }
    if (state?.result?.contentValid) {
      return state.result;
    }

    const fingerprint = JSON.stringify([
      state?.lineCount || 0,
      state?.lastRole || "",
      state?.lastTimestamp || "",
    ]);
    if (fingerprint !== lastFingerprint) {
      lastFingerprint = fingerprint;
      lastChangeAtMs = Date.now();
    }
    const lastRole = String(state?.lastRole || "");
    const idleForMs = Date.now() - lastChangeAtMs;
    let softSettledArtifactRecovery = null;

    if (payload && (taskIsBeamer(payload) || taskIsPpt(payload))) {
      const inferred = readTranscriptAgentResult(transcriptPath, {
        recovered_from_session: transcriptPath,
      }, {
        allowInferredFallback: true,
        payload,
      });
      const validArtifactBackedRecovery = resultIsLocallyValidArtifactBackedRecovery(inferred, payload);
      if (
        validArtifactBackedRecovery
        && (
          (lastRole === "toolResult" && state?.missingFinalJsonAfterToolResult)
          || (lastRole === "assistant" && !state?.result?.contentValid)
        )
      ) {
        const recoveryWarning = state?.missingFinalJsonAfterToolResult
          ? "recovery_protocol_warning: transcript_missing_final_json_after_tool_result"
          : "recovery_protocol_warning: transcript_ended_with_non_json_assistant_message";
        softSettledArtifactRecovery = {
          ...inferred,
          content: {
            ...(inferred.content || {}),
            ...(state?.missingFinalJsonAfterToolResult
              ? { transcript_missing_final_json_after_tool_result: true }
              : {}),
            ...(lastRole === "assistant" && !state?.result?.contentValid
              ? { transcript_non_json_assistant_followup: true }
              : {}),
            notes: appendStructuredNoteLine(
              inferred.content?.notes,
              recoveryWarning
            ),
          },
        };
      }
      const recoveredArtifacts = inferred?.content?.artifact_paths;
      const requiredArtifacts = taskIsBeamer(payload)
        ? ["analysis.json", "slides.json", "main.tex", "main.pdf"]
        : ["analysis.json", "slides.json", "main.pptx", "pptx_validation.json"];
      const phaseRequiredArtifacts = Array.isArray(payload?.phase?.requiredArtifacts) && payload.phase.requiredArtifacts.length > 0
        ? payload.phase.requiredArtifacts.filter((name) => isNonEmptyString(name))
        : requiredArtifacts;
      const artifactRecoveryFlag = taskIsBeamer(payload)
        ? inferred?.content?.beamer_artifact_recovered
        : inferred?.content?.ppt_artifact_recovered;
      const allCoreArtifactsPresent = artifactRecoveryFlag && requiredArtifacts.every((name) => {
        const candidate = recoveredArtifacts?.[name];
        return isNonEmptyString(candidate) && fs.existsSync(candidate);
      });
      const phaseArtifactsPresent = artifactRecoveryFlag && phaseRequiredArtifacts.every((name) => {
        const candidate = recoveredArtifacts?.[name];
        return isNonEmptyString(candidate) && fs.existsSync(candidate);
      });
      const stageArtifactsPresent = artifactRecoveryFlag && ["analysis.json", "slides.json"].every((name) => {
        const candidate = recoveredArtifacts?.[name];
        return isNonEmptyString(candidate) && fs.existsSync(candidate);
      });
      const newestArtifactMs = requiredArtifacts.reduce((latest, name) => {
        const candidate = recoveredArtifacts?.[name];
        if (!isNonEmptyString(candidate) || !fs.existsSync(candidate)) return latest;
        try {
          return Math.max(latest, fs.statSync(candidate).mtimeMs);
        } catch {
          return latest;
        }
      }, 0);
      const newestPhaseArtifactMs = phaseRequiredArtifacts.reduce((latest, name) => {
        const candidate = recoveredArtifacts?.[name];
        if (!isNonEmptyString(candidate) || !fs.existsSync(candidate)) return latest;
        try {
          return Math.max(latest, fs.statSync(candidate).mtimeMs);
        } catch {
          return latest;
        }
      }, 0);
      const phaseCheckpointMarker = /artifact_backed_phase_checkpoint:\s*true/i.test(String(inferred?.content?.notes || ""));
      const artifactBackedPhaseDiagnostic = resultIsArtifactBackedPhaseDiagnostic(inferred, payload);
      if (
        inferred?.contentValid &&
        !artifactBackedPhaseDiagnostic &&
        allCoreArtifactsPresent &&
        (
          newestArtifactMs >= startedAtMs - 15000
          || (payload?.phase?.finalPhase === true && inferred?.content?.ready_for_review === true)
        )
      ) {
        return {
          ...inferred,
          content: {
            ...(inferred.content || {}),
            recovered_from_artifact_complete_before_agent_exit: true,
          },
        };
      }
      if (
        inferred?.contentValid &&
        payload?.phase?.finalPhase !== true &&
        phaseArtifactsPresent &&
        idleForMs >= TRANSCRIPT_IDLE_SETTLE_MS &&
        newestPhaseArtifactMs >= startedAtMs - 15000
      ) {
        return {
          ...inferred,
          content: {
            ...(inferred.content || {}),
            recovered_from_artifact_phase_checkpoint_after_idle: true,
            recovered_phase_artifacts: phaseRequiredArtifacts,
            ...(phaseCheckpointMarker ? { artifact_backed_phase_checkpoint: true } : {}),
          },
        };
      }
      const stageArtifactNewestMs = ["analysis.json", "slides.json"].reduce((latest, name) => {
        const candidate = recoveredArtifacts?.[name];
        if (!isNonEmptyString(candidate) || !fs.existsSync(candidate)) return latest;
        try {
          return Math.max(latest, fs.statSync(candidate).mtimeMs);
        } catch {
          return latest;
        }
      }, 0);
      if (
        inferred?.contentValid &&
        stageArtifactsPresent &&
        state?.recentAssistantError &&
        idleForMs >= TRANSCRIPT_IDLE_SETTLE_MS &&
        (
          stageArtifactNewestMs >= startedAtMs - 15000
          || (payload?.phase?.finalPhase === true && inferred?.content?.ready_for_review === true)
        )
      ) {
        return {
          ...inferred,
          content: {
            ...(inferred.content || {}),
            recovered_from_artifact_stage_checkpoint_after_agent_error: true,
            recovered_agent_error_message: state.recentAssistantErrorMessage || "",
          },
        };
      }
    }
    const waitingOnAgentTurn = lastRole === "toolResult" || (lastRole === "assistant" && !state?.result?.contentValid);
    if (!waitingOnAgentTurn && idleForMs >= TRANSCRIPT_IDLE_SETTLE_MS) {
      return state?.result || null;
    }
    if (waitingOnAgentTurn && idleForMs >= TRANSCRIPT_IDLE_SETTLE_MS) {
      // Do not settle early when the transcript only shows tool output so far.
      // The agent may still append its final JSON payload later, and returning
      // null here would cause the caller to stop watching the transcript and
      // wait only on the slower agent promise/timeout path.
      if (state?.result?.contentValid || state?.recentAssistantError) {
        return state?.result || null;
      }
      if (softSettledArtifactRecovery) {
        return softSettledArtifactRecovery;
      }
      if (state?.missingFinalJsonAfterToolResult) {
        await sleep(TRANSCRIPT_POLL_INTERVAL_MS);
        continue;
      }
      await sleep(TRANSCRIPT_POLL_INTERVAL_MS);
      continue;
    }

    await sleep(TRANSCRIPT_POLL_INTERVAL_MS);
  }

  return inspectTranscriptState(transcriptPath)?.result || null;
}

function describeTranscriptFailure(transcriptPath) {
  const transcriptResult = readTranscriptAgentResult(transcriptPath);
  if (!transcriptResult) return "";
  const rawText = compactSingleLine(transcriptResult.text || transcriptResult.content?.raw_text || "");
  if (!rawText) return "";
  return [
    transcriptPath ? `transcript: ${transcriptPath}` : "",
    `assistant_text: ${rawText}`,
  ].filter(Boolean).join("\n");
}

function recoverPartialAgentResult(agentId, startedAtMs, payload, preferredTranscriptPath = null) {
  const transcriptPath = findRecentSessionTranscript(agentId, startedAtMs, payload, preferredTranscriptPath);
  const isProgrammerLike = agentId === "programmer" || agentId === "pipeline-programmer";
  const partial = readTranscriptAgentResult(transcriptPath, {
    partial_timed_out: true,
    recovered_from_session: transcriptPath,
  }, {
    allowInferredFallback: true,
    payload,
  });
  const enrichedPartial = partial?.content?.inferred_from_transcript && isProgrammerLike
    ? inferProgrammerContentFromTranscript(
        fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean),
        transcriptPath,
        {
          partial_timed_out: true,
          recovered_from_session: transcriptPath,
        },
        payload
      ) || partial
    : partial;
  if (isProgrammerLike && transcriptPath && fs.existsSync(transcriptPath)) {
    try {
      const transcriptState = collectTranscriptContext(
        fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean)
      );
      if (transcriptState.missingFinalJsonAfterToolResult && enrichedPartial?.content) {
        const preservesArtifactBackedValidity = resultIsLocallyValidArtifactBackedRecovery(enrichedPartial, payload)
          || resultIsArtifactBackedPhaseDiagnostic(enrichedPartial, payload);
        enrichedPartial.content = {
          ...(enrichedPartial.content || {}),
          transcript_missing_final_json_after_tool_result: true,
          notes: appendStructuredNoteLine(
            enrichedPartial.content?.notes,
            "recovery_protocol_warning: transcript_missing_final_json_after_tool_result"
          ),
        };
        if (!preservesArtifactBackedValidity) {
          enrichedPartial.content = {
            ...(enrichedPartial.content || {}),
            parse_error: "assistant stopped after tool result without final JSON",
            ready_for_review: false,
          };
          enrichedPartial.contentValid = false;
          enrichedPartial.text = enrichedPartial.text || "assistant stopped after tool result without final JSON";
        }
      }
    } catch {
      // ignore transcript enrichment failures
    }
  }
  if (
    isProgrammerLike &&
    enrichedPartial?.content?.inferred_from_transcript &&
    payloadRequiresChecklist(payload) &&
    !enrichedPartial?.content?.beamer_artifact_recovered &&
    !enrichedPartial?.content?.ppt_artifact_recovered
  ) {
    return {
      ...enrichedPartial,
      contentValid: false,
      content: {
        ...(enrichedPartial.content || {}),
        parse_error: "timed out before producing valid structured deliverable for checklist/list task",
        ready_for_review: false,
      },
      text: enrichedPartial.text || "timed out before producing valid structured deliverable for checklist/list task",
    };
  }
  return enrichedPartial;
}

function truncatePromptString(value, maxLength = 4000) {
  const text = String(value || "");
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}... [truncated ${text.length - maxLength} chars]`;
}

function promptArrayLimitForKey(key) {
  const normalized = String(key || "");
  if (["equation_coverage"].includes(normalized)) return 80;
  if (["paragraph_ledger", "overfull_boxes"].includes(normalized)) return 12;
  if (["notation_coverage"].includes(normalized)) return 24;
  if (["checked_slide_ids", "body_slide_ids", "appendix_slide_ids"].includes(normalized)) return 80;
  if (["checklist", "notes"].includes(normalized)) return 40;
  return 20;
}

function promptStringLimitForKey(key) {
  const normalized = String(key || "");
  if (normalized === "answer") return 10000;
  if (normalized === "summary") return 2500;
  if (normalized === "notes") return 5000;
  if (normalized === "source_quote") return 800;
  if (normalized === "raw") return 600;
  return 1800;
}

function compactPromptValue(value, key = "", depth = 0) {
  if (typeof value === "string") {
    return truncatePromptString(value, promptStringLimitForKey(key));
  }
  if (Array.isArray(value)) {
    const limit = promptArrayLimitForKey(key);
    const mapped = value.slice(0, limit).map((item) => compactPromptValue(item, key, depth + 1));
    if (value.length <= limit) return mapped;
    return {
      prompt_compacted: true,
      total_items: value.length,
      shown_items: mapped.length,
      sample: mapped,
      omitted_for_prompt: value.length - limit,
    };
  }
  if (isPlainObject(value)) {
    if (depth >= 5) {
      return truncatePromptString(JSON.stringify(value), 2000);
    }
    const next = {};
    for (const [entryKey, entryValue] of Object.entries(value)) {
      next[entryKey] = compactPromptValue(entryValue, entryKey, depth + 1);
    }
    return next;
  }
  return value;
}

const ARTIFACT_BACKED_PROMPT_OMITTABLE_FIELDS = [
  "figure_coverage",
  "table_coverage",
  "equation_coverage",
  "notation_coverage",
  "formal_statement_inventory",
  "paragraph_ledger",
  "roadmap_page",
  "conclusion_preview_page",
  "body_appendix_split",
  "timing_plan",
  "overlay_strategy",
  "numerical_study_pages",
  "insight_pages",
  "audience_explanation_strategy",
];

function collectPromptSummarySlideIds(value, output = [], depth = 0) {
  if (output.length >= 16 || depth > 5 || value === null || value === undefined) {
    return output;
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      collectPromptSummarySlideIds(item, output, depth + 1);
      if (output.length >= 16) break;
    }
    return output;
  }
  if (!isPlainObject(value)) {
    return output;
  }
  for (const [key, entryValue] of Object.entries(value)) {
    if (/slide_ids?$|slides$/i.test(key)) {
      const ids = Array.isArray(entryValue) ? entryValue : [entryValue];
      for (const id of ids) {
        const normalized = String(id || "").trim();
        if (normalized && !output.includes(normalized)) {
          output.push(normalized);
          if (output.length >= 16) break;
        }
      }
    } else if (isPlainObject(entryValue) || Array.isArray(entryValue)) {
      collectPromptSummarySlideIds(entryValue, output, depth + 1);
    }
    if (output.length >= 16) break;
  }
  return output;
}

function collectPromptSummaryStatusCounts(value) {
  const counts = {};
  const entries = Array.isArray(value) ? value : Array.isArray(value?.items) ? value.items : [];
  if (!Array.isArray(entries)) return counts;
  for (const entry of entries) {
    if (!isPlainObject(entry)) continue;
    const status = String(entry.status || entry.coverage_status || entry.state || "").trim().toLowerCase();
    if (!status) continue;
    counts[status] = (counts[status] || 0) + 1;
  }
  return counts;
}

function summarizeArtifactBackedPromptField(value) {
  if (Array.isArray(value)) {
    return {
      present_on_disk: true,
      type: "array",
      total_items: value.length,
      status_counts: collectPromptSummaryStatusCounts(value),
      sample_slide_ids: collectPromptSummarySlideIds(value),
    };
  }
  if (isPlainObject(value)) {
    const summary = {
      present_on_disk: true,
      type: "object",
      keys: Object.keys(value).slice(0, 16),
      status: isNonEmptyString(value.status) ? String(value.status).trim() : undefined,
      total_items: Array.isArray(value.items) ? value.items.length : undefined,
      status_counts: collectPromptSummaryStatusCounts(value),
      sample_slide_ids: collectPromptSummarySlideIds(value),
    };
    return Object.fromEntries(Object.entries(summary).filter(([, entryValue]) => entryValue !== undefined));
  }
  if (isNonEmptyString(value)) {
    return {
      present_on_disk: true,
      type: "string",
      chars: String(value).length,
    };
  }
  return {
    present_on_disk: value !== undefined && value !== null,
    type: typeof value,
  };
}

function buildArtifactBackedPromptCoverageSummary(content, omittedKeys) {
  const summary = {};
  for (const key of omittedKeys) {
    summary[key] = summarizeArtifactBackedPromptField(content[key]);
  }
  return summary;
}

function compactProgrammerOutputForPrompt(value, options = {}) {
  if (!(options.beamerMode || options.pptMode) || !isPlainObject(value)) {
    return value;
  }
  const content = isPlainObject(value.content) ? value.content : value;
  if (!isPlainObject(content)) return value;
  const role = String(options.role || "").trim().toLowerCase();
  const phaseIndex = Number(options.phaseIndex || 0) || 0;
  const artifactBackedReview = (options.beamerMode || options.pptMode)
    && ["reviewer", "tester"].includes(role)
    && phaseIndex >= 3
    && isPlainObject(content.artifact_paths);
  const keepKeys = artifactBackedReview ? [
    "summary",
    "answer",
    "checklist",
    "changed",
    "notes",
    "ready_for_review",
    "artifact_paths",
    "compile_status",
    "readability_status",
    "tex_warnings",
    "render_status",
    "validation_status",
    "pptx_warnings",
    "layout_policy",
    "visible_prose_recovery_hint",
    "visible_prose_fidelity_final",
    "render_fidelity_safeguards",
    "pdf_pages",
    "main_pdf_generated",
    "main_pptx_generated",
    "packaging_status",
    "artifact_backed_payload_compacted",
    "payload_compacted",
    "omitted_for_payload",
    "artifact_backed_coverage_summary",
    "artifact_backed_review_instruction",
    ...(phaseIndex === 3 ? ["equation_coverage"] : []),
    ...(phaseIndex === 4 ? ["notation_coverage"] : []),
  ] : [
    "summary",
    "answer",
    "checklist",
    "changed",
    "notes",
    "ready_for_review",
    "artifact_paths",
    "figure_coverage",
    "table_coverage",
    "equation_coverage",
    "notation_coverage",
    "formal_statement_inventory",
    "paragraph_ledger",
    "roadmap_page",
    "conclusion_preview_page",
    "body_appendix_split",
    "timing_plan",
    "overlay_strategy",
    "numerical_study_pages",
    "insight_pages",
    "audience_explanation_strategy",
    "compile_status",
    "readability_status",
    "tex_warnings",
    "render_status",
    "validation_status",
    "pptx_warnings",
    "layout_policy",
    "visible_prose_recovery_hint",
    "visible_prose_fidelity_final",
    "render_fidelity_safeguards",
  ];
  const compactContent = {};
  for (const key of keepKeys) {
    if (hasOwn(content, key)) {
      compactContent[key] = compactPromptValue(content[key], key);
    }
  }
  if (artifactBackedReview) {
    const omittedKeys = ARTIFACT_BACKED_PROMPT_OMITTABLE_FIELDS.filter((key) => hasOwn(content, key));
    compactContent.prompt_compacted = true;
    compactContent.compacted_for_role = role;
    compactContent.omitted_for_prompt = omittedKeys;
    if (omittedKeys.length > 0 && !isPlainObject(compactContent.artifact_backed_coverage_summary)) {
      compactContent.artifact_backed_coverage_summary = buildArtifactBackedPromptCoverageSummary(content, omittedKeys);
    }
    compactContent.artifact_backed_review_instruction = "Full coverage ledgers were omitted only from this prompt; artifact_paths points to the authoritative on-disk bundle for phase review.";
  }
  if (isPlainObject(value.content)) {
    return {
      role: value.role,
      ok: value.ok,
      content_valid: value.content_valid,
      contentValid: value.contentValid,
      synthetic: value.synthetic,
      content: compactContent,
    };
  }
  return compactContent;
}

function shellQuoteForPrompt(value) {
  const text = String(value || "");
  if (/^[A-Za-z0-9_@%+=:,./-]+$/.test(text)) return text;
  return `'${text.replace(/'/g, "'\\''")}'`;
}

function inferPromptArtifactDirectory(existingArtifactPaths) {
  const artifactPaths = normalizeArtifactPathsMap(existingArtifactPaths);
  if (!isPlainObject(artifactPaths)) return "";
  const outputDirectory = inferArtifactOutputDirectoryFromMap(artifactPaths);
  if (isNonEmptyString(outputDirectory)) return path.resolve(outputDirectory);
  for (const artifactName of ["slides.json", "analysis.json", "main.tex", "main.pdf"]) {
    const artifactPath = resolveArtifactPathFromReport(artifactPaths, artifactName);
    if (isNonEmptyString(artifactPath)) return path.dirname(path.resolve(artifactPath));
  }
  return "";
}

function buildBeamerInternalValidatorInstruction(payload, existingArtifactPaths) {
  if (!taskIsBeamer(payload)) return "";
  const phaseIndex = deckPhaseIndex(payload);
  if (phaseIndex < 2 || phaseIndex > 6) return "";
  const artifactDirectory = inferPromptArtifactDirectory(existingArtifactPaths);
  const artifactDirectoryArg = artifactDirectory ? shellQuoteForPrompt(artifactDirectory) : "<current-output-directory>";
  const command = [
    shellQuoteForPrompt(process.execPath),
    shellQuoteForPrompt(__filename),
    "validate-phase",
    "--phase",
    String(phaseIndex),
    "--mode",
    "beamer",
    "--artifact-dir",
    artifactDirectoryArg,
  ].join(" ");
  return [
    `Before the final JSON for Beamer phase ${phaseIndex}, run the internal same-source phase validator: ${command}`,
    "This validator calls the same local programmer preflight used by the outer gate, including artifact-backed analysis.json/slides.json materialization.",
    "If it returns errors, repair the current phase artifacts and rerun it before returning; after three failed repair attempts, return ready_for_review=false and include the exact validator errors in notes/checklist.",
    "The final JSON notes or checklist must record the validator command and whether it passed.",
  ].join(" ");
}

function buildPrompt(role, payload) {
  const task = payload.task || "";
  const reviewerFeedback = payload.reviewer_feedback || "";
  const repairTickets = Array.isArray(payload.repair_tickets) ? payload.repair_tickets : [];
  const programmerOutput = payload.programmer_output || null;
  const existingArtifactPaths = isPlainObject(payload.existing_artifact_paths) ? payload.existing_artifact_paths : null;
  const testerCommand = payload.tester_command || "";
  const executionApproved = Boolean(payload.execution_approved);
  const preferredLanguage = detectPreferredLanguage(payload);
  const beamerMode = taskIsBeamer(payload);
  const pptMode = taskIsPpt(payload);
  const deckModeLabel = pptMode ? "PPT" : "Beamer";
  const retryRound = Number(payload.round || 1);
  const differentialRepairRound = (beamerMode || pptMode) && retryRound > 1;
  const phase = isPlainObject(payload.phase) ? payload.phase : null;
  const beamerFinalOrUnphased = Boolean(beamerMode && (!phase || phase.finalPhase === true));
  const beamerPhase1 = Boolean(beamerMode && deckPhaseIndex(payload) === 1);
  const pptPhase1 = Boolean(pptMode && deckPhaseIndex(payload) === 1);
  const beamerThinArtifactEnvelopePhase = Boolean(phaseSupportsThinArtifactBackedProgrammerEnvelope(payload));
  const thinArtifactRequiredNames = thinArtifactBackedRequiredArtifactNames(payload);
  const beamerReviewPhaseIndex = beamerMode ? deckPhaseIndex(payload) : 0;
  const beamerReviewerPhase2 = Boolean(beamerMode && beamerReviewPhaseIndex === 2);
  const beamerReviewerPhase3 = Boolean(beamerMode && beamerReviewPhaseIndex === 3);
  const beamerReviewerPhase4 = Boolean(beamerMode && beamerReviewPhaseIndex === 4);
  const beamerReviewerPhase5 = Boolean(beamerMode && beamerReviewPhaseIndex === 5);
  const beamerReviewerPhase6 = Boolean(beamerMode && beamerReviewPhaseIndex === 6);
  const beamerReviewerPhase7 = Boolean(beamerMode && beamerReviewPhaseIndex === 7);
  const beamerReviewerPhaseScoped = Boolean(
    beamerReviewerPhase2
    || beamerReviewerPhase3
    || beamerReviewerPhase4
    || beamerReviewerPhase5
    || beamerReviewerPhase6
    || beamerReviewerPhase7
  );
  const phaseLabel = phase?.index && phase?.total && phase?.title
    ? `Phase ${phase.index}/${phase.total}: ${phase.title}`
    : "";
  const taskForPrompt = sanitizeTaskForPrompt(task, { beamerMode, pptMode, retryRound });
  const languageInstruction = preferredLanguage === "zh"
    ? "Use Chinese for all natural-language fields in the JSON output. Keep only the JSON keys in English."
    : "Use the same language as the original task for all natural-language fields in the JSON output.";
  const programmerOutputForPrompt = compactProgrammerOutputForPrompt(programmerOutput, {
    beamerMode,
    pptMode,
    role,
    phaseIndex: beamerReviewPhaseIndex,
  });
  const repairTicketsForPrompt = repairTickets.length > 0
    ? compactPromptValue(repairTickets, "repair_tickets")
    : [];
  const beamerInternalValidatorInstruction = buildBeamerInternalValidatorInstruction(payload, existingArtifactPaths);

  if (role === "programmer") {
    return [
      "You are the programmer role in a deterministic multi-agent pipeline.",
      "Operate on the current project workspace.",
      DEFAULT_PYTHON_ENVIRONMENT_INSTRUCTION,
      "Implement the task if changes are needed.",
      executionApproved
        ? "Execution approval has already been granted by the user for this task. Do not stop to ask for approval again. Do not output a new approval request. Execute the requested reads/changes/tests directly within the approved scope and report concrete results."
        : "",
      executionApproved
        ? "When creating or updating local text artifacts such as JSON, Markdown, TeX, or source files, prefer the write/edit tools over long inline shell/python heredocs. Avoid giant one-shot exec commands that embed whole files, because they can trigger command-obfuscation approvals and break the pipeline JSON protocol. Reserve exec for lightweight inspection, validation, rendering, compilation, or other commands that truly need a shell."
        : "",
      "If reviewer feedback is provided, address it directly.",
      repairTickets.length > 0
        ? "Structured repair tickets are the authoritative machine-readable repair backlog for this retry. Treat reviewer_feedback as a human summary only; when they conflict, follow the structured repair_tickets fields."
        : "",
      repairTickets.length > 0
        ? "Use repair_tickets to drive the scope of work: honor fields such as retry_from_phase, slide_ids, equation_numbers, symbol, fix_hint, severity, and attempts, and clear the whole defect class within the affected phase instead of fixing only one cited example."
        : "",
      "Do not compress the answer into a short summary when the user asked for a list, checklist, steps, or detailed output.",
      "When the user asks to list items, identify causes, or provide a checklist, answer must be a directly usable multi-line list with headings or bullets, not a single paragraph.",
      "For those tasks, checklist must repeat the actionable checks as separate array items.",
      "If the task is read-only, still provide the full requested deliverable in structured form.",
      "Never reply with planning-only prose or status-only prose. Do not output lines like 'Let me read it in chunks' or 'I will continue' as the final programmer response.",
      "If you need tools, call them directly. Do not emit standalone natural-language progress prose before tool calls. Reserve all prose for the final JSON object so the transcript stays protocol-safe.",
      "The very first assistant message after your last necessary tool result must be the final JSON object. Do not keep polling logs, do not ask for one more tool result, and do not emit any extra prose after you already have enough information to write the phase deliverable.",
      "Even if the work is still in progress, the tool output is truncated, or artifacts are not ready yet, you must still return the required JSON object. In that JSON, explicitly state what already exists, what is still missing, and set ready_for_review to false.",
      "If artifacts are incomplete, answer and checklist must still be present as usable structured content. List existing artifact paths, missing artifacts, current blocker, and next concrete step instead of returning free-form prose.",
      differentialRepairRound
        ? `This is retry round ${retryRound}. Treat the existing deliverable as the baseline and repair only the reviewer-reported gaps instead of re-solving the whole task from scratch.`
        : "",
      phaseLabel
        ? `${phaseLabel}. Only complete this phase goal in this round; do not jump ahead to later phases unless the current phase explicitly requires it.`
        : "",
      phase?.goal
        ? `Current phase goal: ${phase.goal}`
        : "",
      Array.isArray(phase?.requiredArtifacts) && phase.requiredArtifacts.length > 0
        ? `This phase must leave these artifacts present and reportable: ${phase.requiredArtifacts.join(", ")}.`
        : "",
      beamerInternalValidatorInstruction,
      phase && phase.finalPhase === false
        ? "For non-final phases, return a valid structured JSON deliverable with ready_for_review=false after completing the current phase. Do not pretend the whole task is final yet."
        : "",
      phase && phase.finalPhase === true
        ? "This is the final phase. You must integrate prior artifacts, fully satisfy the remaining reviewer/tester requirements, and return ready_for_review=true only if the whole deliverable is actually complete."
        : "",
      beamerThinArtifactEnvelopePhase
        ? `For ${deckModeLabel} phase 3/4/5/6, once the authoritative structured state is already written into one exact artifact bundle on disk, prefer a thin artifact-backed envelope instead of re-serializing the full contract JSON.`
        : "",
      beamerThinArtifactEnvelopePhase
        ? `In thin-envelope mode, return only summary, answer, checklist, changed, notes, ready_for_review, and artifact_paths. artifact_paths must resolve to one exact output directory and must make these current-phase artifacts recoverable from disk: ${thinArtifactRequiredNames.join(", ")}. Include output_directory when helpful.`
        : "",
      beamerThinArtifactEnvelopePhase
        ? "Do not mix artifact_paths across multiple bundles or legacy directories. Every reported path must stay inside the same output directory. If the current phase artifacts are not yet authoritative on disk, do not use thin-envelope mode; return the normal full structured JSON instead."
        : "",
      beamerThinArtifactEnvelopePhase
        ? "In thin-envelope mode, do not inline figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, roadmap_page, conclusion_preview_page, body_appendix_split, timing_plan, overlay_strategy, numerical_study_pages, insight_pages, or audience_explanation_strategy back into the JSON when analysis.json/slides.json already carry the authoritative structured state."
        : "",
      beamerThinArtifactEnvelopePhase && deckPhaseIndex(payload) >= 3
        ? `Before using thin-envelope mode in ${deckModeLabel} phase 3+, verify analysis.json and slides.json both carry the shared top-level contract fields: figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, roadmap_page, conclusion_preview_page, body_appendix_split, timing_plan, overlay_strategy, numerical_study_pages, insight_pages, and audience_explanation_strategy. If source inventory is genuinely zero, store an explicit non-empty zero-inventory object instead of omitting the field or writing an empty array.`
        : "",
      beamerThinArtifactEnvelopePhase && deckPhaseIndex(payload) >= 5
        ? (pptMode
          ? "For phase 5+ PPT thin envelopes, artifact_paths must make both main.pptx and pptx_validation.json recoverable from the same output directory."
          : "For phase 5+ Beamer thin envelopes, artifact_paths must make both main.tex and main.pdf recoverable from the same output directory.")
        : "",
      beamerPhase1
        ? "For Beamer phase 1 specifically, keep the returned JSON concise and phase-local. Put detailed inventories inside analysis.json, not inside summary/answer/notes. In the returned JSON, report only the output directory, analysis.json path, paragraph_ledger count/availability, source-equation count or range summary, current blockers, and the next phase. analysis.json itself must still include top-level figure_coverage and table_coverage (use explicit zero-inventory objects when source inventory is zero). slides.json becomes required from phase 2 onward."
        : "",
      beamerPhase1
        ? "For Beamer phase 1, do not inline huge paragraph_ledger arrays, equation_coverage arrays, notation_coverage arrays, or long artifact dumps into summary, answer, checklist, or notes. Those fields may stay as compact blocker/planning placeholders as long as the JSON schema remains valid and analysis.json carries the real detailed backbone."
        : "",
      beamerPhase1
        ? "For Beamer phase 1, once you have the paragraph/equation baseline and analysis.json is written, stop exploring and immediately emit the final JSON object for this phase. Do not perform extra log polling or repeated source rescans after analysis.json already contains the needed baseline."
        : "",
      differentialRepairRound && existingArtifactPaths
        ? `Existing artifact baseline for in-place edits:\n${JSON.stringify(existingArtifactPaths, null, 2)}`
        : "",
      differentialRepairRound
        ? "On retry rounds, prefer targeted edits to the existing analysis/slides/tex/report artifacts. Do not generate a large helper script or regenerate untouched sections unless the reviewer feedback proves the existing files are unusable."
        : "",
      differentialRepairRound
        ? "On retry rounds, keep the scope narrow: preserve already-correct sections, patch only the failing slide ranges / coverage mappings / compile blockers, and avoid re-enumerating unrelated requirements in the final answer."
        : "",
      differentialRepairRound && beamerMode
        ? "For Beamer retry rounds, 'targeted edits' means stay within the failing phase and artifact slice, but do not stop at the first cited tickets. If reviewer feedback lists representative equation_coverage / notation_coverage / structural-drift examples, treat them as symptoms of a same-class defect and scan the whole affected scope before returning."
        : "",
      differentialRepairRound && beamerMode
        ? "For Beamer retry rounds, when one slide in an affected range is missing visible equations, first-use symbol definitions, or title/label alignment, inspect sibling slide_ids in that same coverage family and repair the full pattern in one round instead of fixing only the enumerated examples."
        : "",
      differentialRepairRound && beamerMode
        ? "For Beamer retry rounds, narrow scope does not mean sample-only repair. Do not regenerate the whole deck, but within the current phase you must eliminate the defect class across the affected equation ranges / notation first-use ranges / structural contract checks so the next review does not simply surface the next batch of identical tickets."
        : "",
      differentialRepairRound && pptMode
        ? "For PPT retry rounds, 'targeted edits' means stay within the failing phase and artifact slice, but do not stop at the first cited tickets. If reviewer feedback lists representative equation_coverage / notation_coverage / structural or visible-text examples, treat them as symptoms of a same-class defect and scan the whole affected scope before returning."
        : "",
      differentialRepairRound && pptMode
        ? "For PPT retry rounds, when one slide in an affected range is missing visible equations, first-use symbol definitions, source_paragraph_ids, or formal academic wording, inspect sibling slide_ids in that same coverage family and repair the full pattern in one round instead of fixing only the enumerated examples."
        : "",
      differentialRepairRound && pptMode
        ? "For PPT retry rounds, narrow scope does not mean sample-only repair. Do not regenerate the whole deck, but within the current phase you must eliminate the defect class across the affected equation ranges / notation first-use ranges / structural contract checks so the next review does not simply surface the next batch of identical tickets."
        : "",
      beamerMode
        ? "If the task wrapper contains mixed-mode memories or metadata, ignore PPT-specific requirements for Beamer work and rely only on the explicit Beamer instructions plus the current reviewer feedback."
        : "",
      pptMode
        ? "If the task wrapper contains mixed-mode memories or metadata, ignore Beamer-specific requirements for PPT work and rely only on the explicit PPT instructions plus the current reviewer feedback."
        : "",
      beamerMode
        ? "This is a Beamer-generation task. Work in seven stages: phase 1 analysis; phase 2 slides outline/skeleton; phase 3 equation coverage; phase 4 notation/consistency; phase 5 compile_and_structural_repair; phase 6 review_and_auto_rework; phase 7 final_acceptance_delivery."
        : "",
      beamerMode
        ? `For Beamer tasks, before generating main.tex, prefer running ${PREPARE_TASK_ASSETS_BIN} as a direct command with three positional arguments plus --mode beamer: source document path, task output directory, and --mode beamer. Do not omit the mode flag. If the task directory does not exist yet, create it in a separate command rather than chaining mkdir && node together. That preprocessor writes a per-task asset_manifest.json, downloads markdown image URLs into a local figures/ directory, marks each item as success/failed/skipped/duplicate, and keeps cache identity by URL + hash + task scope. Then reference only those localized figures in main.tex using \\includegraphics[width=0.85\\linewidth]{figures/figXX.*}. LaTeX cannot fetch remote URLs at compile time, so all images must be local before compilation. If no image URLs are found, keep asset_manifest.json and explicitly report that no remote figures were discovered.`
        : "",
      pptMode
        ? `This is a PowerPoint-generation task. Use the same seven-stage deck pipeline as Beamer tasks: phase 1 analysis; phase 2 slides outline/skeleton; phase 3 equation coverage; phase 4 notation/consistency; phase 5 compile_and_structural_repair, implemented with PPT validation/rendering instead of LaTeX compilation; phase 6 review_and_auto_rework; phase 7 final_acceptance_delivery. The artifact backend is PPT: in phase 5 and later, validate slides.json with ${PPT_RENDERER_BIN} --validate using ${PPT_RENDERER_PYTHON}, write/report pptx_validation.json, then generate main.pptx with the deterministic renderer at ${PPT_RENDERER_BIN}. Do not handcraft OOXML or zip XML by hand.`
        : "",
      pptMode
        ? `For PPT tasks, before generating slides.json, prefer running ${PREPARE_TASK_ASSETS_BIN} as a direct command with three positional arguments plus --mode ppt: source document path, task output directory, and --mode ppt. Do not omit the mode flag. If the task directory does not exist yet, create it in a separate command rather than chaining mkdir && node together. That preprocessor writes a per-task asset_manifest.json, downloads markdown image URLs into a local figures/ directory, marks each item as success/failed/skipped/duplicate, and keeps cache identity by URL + hash + task scope. Then reference only those local files in slides.json and during rendering. Do not keep remote http(s) figure URLs in the final deck plan. If some non-critical assets fail, record them as warnings from asset_manifest.json instead of treating the whole task as failed; only escalate to a hard blocker when a missing asset is clearly a key evidence figure.`
        : "",
      beamerMode
        ? "For Beamer tasks, default to a polished Chinese academic talk style for readers who have not read the paper. There is no preset total-duration cap."
        : "",
      beamerMode
        ? "For Beamer tasks, ignore any historical helper example that mentions a 30-minute default. Do not set analysis.json target_minutes or estimated_minutes to a positive fixed number. If a compatibility field is needed, set target_minutes to null and place only qualitative pacing hints under timing_plan with no_hard_time_cap=true."
        : "",
      pptMode
        ? "For PPT tasks, default to the same polished Chinese academic talk style as Beamer tasks, but optimize for a directly usable .pptx deck with stable layout, explicit page-kind presets, readable speaker notes, and PPT-native object layout rather than Beamer-like dense text stacking. On-slide text must use formal academic Chinese rather than classroom-style coaching language."
        : "",
      pptMode
        ? "For PPT tasks, there is no preset total-duration cap. Do not set analysis.json target_minutes or estimated_minutes to a positive fixed number unless the user explicitly supplied one. If a compatibility field is needed, set target_minutes to null and place only qualitative pacing hints under timing_plan with no_hard_time_cap=true."
        : "",
      beamerMode
        ? "For Beamer tasks, do not lock the deck to a fixed slide count. Expand it to fit the paper, and explicitly justify the actual title/body/appendix split. If the task, template, or prior plan mentions a target slide count, treat that number only as a minimum lower bound rather than an exact cap: do not deliver fewer than that count unless the user explicitly relaxes it, and expand further whenever source coverage requires more slides."
        : "",
      beamerMode
        ? "For Beamer tasks, prioritize full source-paper coverage over page minimization."
        : "",
      beamerMode
        ? "For Beamer tasks, the minimum skeleton is: title, roadmap, conclusion preview, method/model chain, key formulas, dedicated results/numerical-study slides, dedicated insight slides, limitations/discussion, final takeaways, and appendix. Missing roadmap or conclusion-preview pages is a deliverable failure."
        : "",
      beamerMode
        ? "For Beamer tasks, treat roadmap_page, conclusion_preview_page, body_appendix_split, numerical_study_pages, insight_pages, figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, timing_plan, overlay_strategy, and audience_explanation_strategy as explicit contract fields from the first phase onward. Do not omit them and plan to backfill later."
        : "",
      pptMode
        ? "For PPT tasks, treat roadmap_page, conclusion_preview_page, body_appendix_split, numerical_study_pages, insight_pages, figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, timing_plan, overlay_strategy, and audience_explanation_strategy as explicit contract fields from the first phase onward. Do not omit them and plan to backfill later."
        : "",
      beamerMode
        ? "For Beamer tasks, slides.json must expose a page-level plan with section, title, core_message, body/appendix ownership, and source_paragraph_ids for every content-bearing body slide. speaker_minutes may be used only as a local pacing hint when helpful; it must never impose a global duration cap. The plan must explicitly mark the roadmap page, conclusion-preview page, numerical-study slides, insight slides, and final body-vs-appendix split."
        : "",
      beamerMode
        ? "For Beamer tasks, if phase 5+ splits one planned page into additional labeled frames inside main.tex, you must first add matching slide_id entries to slides.json/body_appendix_split and then update equation_coverage/notation_coverage to those real slide IDs. Never introduce slide-like frame labels such as s032, s035b2, or s061_dup2 that are absent from slides.json. Never generate slide labels by arithmetic string formatting such as f's0{31+i}', because it easily skips or duplicates planned IDs; iterate over slides.json.slides and use each slide.slide_id as the rendered frame label."
        : "",
      beamerMode
        ? "For Beamer phase 5 and later, treat slides.json as the structural contract for main.tex. Before patching notation/equation coverage, verify that every slides.json slide_id maps to the intended labeled frame, every slide-like rendered frame label exists in slides.json, and the frame title/purpose still matches the planned slide. If labels/titles drift, repair that structural alignment first instead of papering over it with coverage edits."
        : "",
      beamerMode
        ? "For Beamer tasks, use overlays strategically for dense formulas, formal statements, and multi-part arguments, and explain how overlay choices affect page count and timing. Always keep \\setbeamercovered{transparent} in main.tex whenever overlays are used or planned; do not switch to invisible/hidden covered content."
        : "",
      beamerMode
        ? "For Beamer tasks, notes must list concrete artifact paths for analysis.json and the current required bundle artifacts. By phase 5+, include main.tex and main.pdf. In the final packaged delivery, also include README.md, asset_manifest.json, and figures/ from the same output directory."
        : "",
      beamerMode
        ? "For Beamer tasks, keep all scaffold-only labels and planning metadata out of visible slides: do not let visible title/body/equation labels in slides.json or main.tex contain phrases such as '核心信息', '来源段落', 'source_paragraph_ids', '这页负责', '服务于未读论文听众', or '公式 A1/A2'. Those belong only in metadata or notes, and appendix formulas should use natural wording such as '式 (A1)'."
        : "",
      beamerMode
        ? "For Beamer tasks, keep one canonical equation-number ledger across analysis.json, slides.json, paragraph_ledger.equation_tags, equation_coverage, and rendered \\\\tag values: main-text equations use 1, 2, 3, ... in source order; appendix equations use A1, A2, ...; never store alias-style tokens such as main-linear, def-unbiased, or prop-dgp inside equation_numbers."
        : "",
      beamerMode
        ? "For Beamer tasks, whenever visible prose needs to refer to an equation already shown inside the deck, create a deck-local reference with \\label plus \\eqref/\\ref. If you need to preserve the paper's original numbering, keep it on the displayed equation via \\tag{60} together with a local label such as \\label{eq:paper60}. Do not leave raw visible text like '式 (60)' as a literal copy from the paper."
        : "",
      beamerMode
        ? "For Beamer tasks, answer must summarize the final page structure, body/appendix split, roadmap page, conclusion-preview page, dedicated numerical-study and insight coverage, formula/figure/table/formal-statement/notation coverage, overlay/page-count strategy, packaging status (including same-directory bundle layout), and remaining compile/layout issues."
        : "",
      beamerMode
        ? (beamerPhase1
          ? "For Beamer phase 1, checklist should stay phase-local: analysis.json presence, paragraph_ledger availability, source-order basis, equation baseline capture, blocker summary, and next-phase handoff. Do not restate the full final QA matrix yet."
          : "For Beamer tasks, checklist must cover artifact completeness, chapter-order coverage, paragraph-order coverage, paragraph-summary coverage, final page-plan coverage, roadmap/conclusion-preview coverage, numerical-study coverage, per-insight slide coverage, figure/table coverage, notation-definition coverage, formal-statement coverage, formal-statement-vs-intuition separation, appendix split, audience-oriented explanation, overlay/page-count explanation, and compile status.")
        : "",
      beamerMode
        ? "For Beamer tasks, detect and report the source-paper inventory as explicitly as possible: total figures, total tables, and crucial formal statements such as theorem/proposition/lemma/corollary/definition/assumption/remark. Map each item to slide IDs or report any missing item as a blocker."
        : "",
      beamerMode
        ? "For Beamer tasks, table_coverage must be an ordered per-source-mention mapping, not just a summary by unique table number. If the source markdown mentions Table 1 twice and Table 2 four times, table_coverage must contain 6 explicit entries in source order, and each entry must include the source mention (or occurrence index) plus the target slide ID(s). Do not collapse repeated source mentions into only two unique table labels."
        : "",
      beamerMode
        ? "For Beamer tasks, preserve source-paper order. Except for title/roadmap/conclusion-preview/final-takeaway/utility appendix pages, the deck must follow the paper's section order and local paragraph order. Do not pull later results forward and do not merge non-contiguous source paragraphs onto one slide."
        : "",
      beamerMode
        ? "For Beamer tasks, analysis.json must include paragraph_ledger: an ordered array where each source paragraph is summarized in one Chinese sentence with keys paragraph_id, section, and summary_sentence, plus equation/figure/table/formal hooks when available. Every content-bearing body slide in slides.json must map contiguous source_paragraph_ids back to that ledger."
        : "",
      beamerMode
        ? "For Beamer tasks, paragraph_ledger.summary_sentence must be a Chinese summary sentence, not a copied English source excerpt. Preserve raw English snippets only in source_excerpt/source_quote fields. Short technical terms such as CCS, NPV, PDE, Eq., kWh, and symbol names are fine inside Chinese prose, but a mostly-English summary_sentence is a phase-gate failure."
        : "",
      beamerMode
        ? "For Beamer tasks, ordinary body slides must advance through source_paragraph_ids monotonically. Use spans like [p07] or [p07,p08], not mixed jumps like [p01,p10]. Only conclusion_preview, takeaways, qa, or utility appendix pages may intentionally revisit earlier paragraphs."
        : "",
      beamerMode
        ? "For Beamer tasks, when several formulas appear in one local stretch of prose, do not turn them into a single formula wall just to save logical slides. Split the chain across multiple slides whenever a reader who has not seen the paper would otherwise lose the argument."
        : "",
      beamerMode
        ? "For Beamer tasks, treat slides.json as a lower-bound visible-content contract for main.tex. If a planned slide contains 4+ visible explanatory bullet items, the rendered main.tex slide must keep at least 2 visible explanatory bullets instead of collapsing into equations-only output. On equation_focus / experiment_setup / results / comparison / content-heavy slides with 3+ displayed equations, preserve ALL planned visible explanatory bullets; if any bullet no longer fits, split into more slides instead of deleting prose."
        : "",
      beamerMode && phase?.index === 5
        ? "For Beamer phase 5 compile_and_structural_repair, main.tex must already be a genuinely rendered talk deck rather than a skeleton. Do not stop at frame titles plus one-line bullets or equation walls. For every content-bearing slide planned in slides.json, carry visible explanatory prose into main.tex and label the rendered frame with exactly that slide.slide_id, either through \\begin{frame}[label=<slide_id>] or a frame-local \\label{<slide_id>}. Treat slides.json as a lower-bound visible-content contract: if the plan says the audience should see explanatory prose, that prose must remain visibly present in main.tex rather than being moved only into notes or deleted. If a planned body slide has 4+ visible explanatory bullets, keep at least 2 visible explanatory bullets in the rendered frame; if that no longer fits, split the slide by first adding consecutive slide_id entries to slides.json, not by inventing labels only in main.tex. For every dense formula slide, slides.json must contain an explicit slide-level overlay_plan instead of relying only on a deck-level overlay_strategy note. Then realize that overlay_plan in main.tex with progressive Beamer overlay commands. <+-> is MANDATORY for dense formula slides — do NOT use only \\pause as a shortcut (the validator will reject \\pause-only frames). Use \\begin{itemize}[<+->] to reveal bullet items progressively, or equivalent progressive reveal commands (\\onslide, \\only, \\uncover, \\visible, \\alt, \\item<...>), or split the planned slide into multiple consecutive slides/frames whose slide_ids are all present in slides.json. Keep \\setbeamercovered{transparent} in main.tex as the fixed covered-content policy; do not downgrade to invisible/hidden covered states. Do not claim overlay coverage in notes unless the rendered main.tex actually contains those overlay/split mechanics. Before reporting ready_for_review=true, run the local phase validator if available, or at minimum scan main.tex labels against slides.json and confirm there are no missing planned slide_ids and no slide-like frame labels absent from slides.json. Run a real compile check with latexmk/xelatex when feasible. If main.pdf is missing or compile fails, keep ready_for_review=false and report the exact compile command, whether main.pdf was generated, the blocking TeX error, and the concrete log paths such as main.log / compile.run.log. Even if main.pdf is generated, do not set ready_for_review=true when severe overfull layout warnings remain, when structural alignment is broken, or when visible-prose fidelity is still broken."
        : "",
      beamerMode && phase?.index === 5
        ? "For Beamer phase 5, never put raw English source prose or raw inline math snippets into visible bullets. If content contains $...$ or \ensuremath{} or LaTeX commands such as \gamma/\mathrm, do not tex_escape the whole sentence into text. Do not use \ensuremath{} as a workaround to inline math symbols in visible bullets — \ensuremath{\\xi}\_{1} is the same violation as $\\xi_{1}$ in prose and must be moved into equation_blocks instead. Move the formula into equation_blocks/blocks type='equation' and write the bullet as Chinese natural-language explanation. main.tex and the rendered PDF must not visibly contain \textbackslash{}, \textasciicircum{}, \$P\_, \{}gamma, \{}mathrm, \ensuremath{}, or English fragments such as 'where $...$.'"
        : "",
      beamerMode && phase?.index === 5
        ? "For Beamer phase 5, CRITICAL HARD RULE — VISIBLE SLIDES ARE AUDIENCE-FACING, NOT PRESENTER NOTES. Every visible bullet must read as finished explanatory prose for an academic audience, not as a planning reminder, speaker cue, or construction note to the slide author. PROHIBITED CATEGORIES: A) PAGE SELF-DESCRIPTIONS — never tell the audience what 'this page' does or 'the next page' will do (e.g. '这页只覆盖第一组系数', '该页支撑正文定理1的公式来源', '这页为后续新增相关因子提供对照组'). Write the actual content instead; the page layout is invisible to the audience. B) PRESENTER INSTRUCTIONS — never write speaker cues like '读图时', '读表重点', '读表时', '讲解时', '先看…再看…'. Rephrase as direct explanatory statements the audience would read. C) PLANNING ARTIFACTS — never expose split/keep/skip decisions like '后续公式页拆分', '完整保留', '该页只讲…不提前混入'. Delete entirely; the audience cares about content, not editorial decisions. SELF-CHECK: Would a real presenter say this sentence out loud to fifty academics during a live talk? If no, rewrite or delete. MINIMUM CONTENT: After cleanup, every frame must retain at least 3 visible content-bearing bullets. If too sparse, merge with a neighbor or add genuine content — never ship a near-empty slide of meta-instructions."
        : "",
      beamerMode && phase?.index === 2
        ? "For Beamer phase 2 slides outline/skeleton, focus on the page-level plan and skeleton only. roadmap_page, conclusion_preview_page, body_appendix_split, numerical_study_pages, insight_pages, paragraph_ledger alignment, and artifact_paths/slides.json must be reviewer-ready. equation_coverage and notation_coverage may remain source-grounded planning placeholders here; do not pretend they are fully covered yet. However, every dense formula slide already needs an explicit slide-level overlay_plan in slides.json describing how the explanation will be progressively revealed or split across consecutive frames; do not rely only on a global overlay_strategy summary."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3 equation coverage, convert equation_coverage into real slide mappings with exhaustive numbered coverage and visible equation blocks, but notation_coverage may still be source-grounded planned/partial placeholders until phase 4."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3, never repair equation_coverage by changing the ledger alone. For every equation_coverage entry whose status is covered, the mapped slide_ids must point to slides in slides.json that visibly contain the corresponding formula in equation_blocks or blocks entries with type='equation' and a non-empty latex field. If a slide lacks that visible equation block, edit slides.json first by adding/splitting real formula slides, then update equation_coverage; otherwise leave the entry missing/blocked and explain the blocker instead of claiming covered."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3 repair rounds, treat tickets like 'marks Eq. (n) as covered but mapped slides contain no visible equation block' as a class-wide defect. Scan every covered numbered equation and appendix equation, verify its mapped slides contain visible equation_blocks/blocks latex for that equation, fix all same-class failures in one pass, and only then return the phase JSON. The final checklist must include an explicit item stating that covered_equations_without_visible_blocks is empty."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3 source grounding, source_paragraph_ids must include the source paragraphs where the equation actually appears. Do not map Eq. (n) to earlier explanatory paragraphs only. If the first equation paragraph is p29, p40, p93, etc., the corresponding equation_coverage entry and mapped slide must include that paragraph or a contiguous span containing it."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3 repair_tickets, if a ticket includes equation_numbers and required_source_paragraph_ids, treat those fields as exact machine-readable requirements. For each listed equation number, update equation_coverage and the mapped slide's source_paragraph_ids so they include every required_source_paragraph_id. Do not satisfy such tickets by only editing notes, summaries, or earlier explanatory paragraph IDs."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3 source grounding, every ordinary body slide in slides.json must have source_paragraph_ids that form exactly one contiguous forward-moving span (e.g., [p07,p08,p09], not [p07,p09] or [p07,p05]). Do not skip paragraphs or jump backward. The entire slide must cover one uninterrupted paragraph range. Only conclusion-preview pages, final-takeaway pages, QA/utility pages, and appendix pages may use non-contiguous or backward-reference source_paragraph_ids."
        : "",
      beamerMode && phase?.index === 3
        ? "For Beamer phase 3, scan every equation block across all slides in slides.json and verify each visible math symbol (coefficients, parameters, variables, indices) has a corresponding notation_coverage entry. Add any missing symbols to notation_coverage before completing the phase. Do not defer all notation_coverage gaps to phase 4; the reviewer will reject notation_coverage gaps discovered from equation blocks."
        : "",
      beamerMode
        ? "For Beamer slides.json, use equation_blocks (or blocks entries with type='equation') as the canonical visible-formula field. visible_equation_blocks is treated only as a legacy alias for recovery and should not be newly emitted."
        : "",
      beamerMode && phase?.index === 4
        ? "For Beamer phase 4 notation/consistency, finish notation_coverage, first-use definitions, and whole-deck equation/notation/slide-id consistency. By the end of this phase, equation_coverage and notation_coverage must both be fully structured and no longer planning-only. In notation_coverage.symbol, use the same visible symbol spelling that appears on-slide, but omit surrounding math delimiters such as $...$, \\(...\\), or \\[...\\]. Do not leave escaped identifier underscores as the only spelling when the visible symbol is user_followers-style text. If equation blocks visibly contain coefficient, fixed-effect, or error symbols such as \\beta_i, \\alpha_i, or \\epsilon, add explicit notation_coverage entries for them instead of silently treating them as implicit."
        : "",
      beamerMode && phase?.index === 6
        ? "For Beamer phase 6 review_and_auto_rework, treat the deck as already compiled and structurally repaired. Focus on reviewer/tester issue extraction, minimum necessary rework, residual-risk surfacing, and routing repair tickets back to the earliest failing phase when needed. Dense formula slides must still preserve their explicit slide-level overlay_plan and the rendered main.tex must still realize that plan via real overlays or equivalent split frames; do not downgrade this to a notes-only statement. \\setbeamercovered{transparent} must remain present in main.tex."
        : "",
      beamerMode && phase?.finalPhase === true
        ? buildPromptLinesForFinalBeamer().join(" ")
        : "",
      pptMode && phase?.finalPhase === true
        ? buildPromptLinesForFinalPpt().join(" ")
        : "",
      beamerMode
        ? "For Beamer tasks, crucial formal statements must appear as full faithful Chinese translations of the original content, not short summaries."
        : "",
      beamerMode
        ? "For Beamer tasks, write for an audience that has not read the paper: include enough background, motivation, notation explanation, intuition, transitions, figure-reading guidance, numerical-study interpretation, and significance of results. Treat the paragraph_ledger as the minimum explanation backbone: every source paragraph should first be reduced to one clear sentence before you aggregate those sentences into slides."
        : "",
      beamerMode
        ? (beamerPhase1
          ? "For Beamer phase 1, the JSON must still include these required deliverable fields: artifact_paths, figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, roadmap_page, conclusion_preview_page, body_appendix_split, timing_plan, overlay_strategy, numerical_study_pages, insight_pages, audience_explanation_strategy. analysis.json itself must also carry top-level figure_coverage and table_coverage fields (including explicit zero-inventory objects when applicable), while slides.json is only required from phase 2 onward. However, except for artifact_paths and paragraph_ledger, keep them compact phase-1 planning/blocker placeholders instead of exhaustive final-form inventories. answer, checklist, and table_coverage must use the same counting basis for tables."
          : beamerThinArtifactEnvelopePhase
            ? `For ${deckModeLabel} phase 3/4/5/6 thin-envelope mode, the returned JSON must still include artifact_paths with exact absolute paths for the current phase bundle. The remaining ${deckModeLabel} contract fields must already be materialized inside that exact artifact bundle on disk; do not omit them from the artifacts, only omit them from the returned JSON.`
            : "For Beamer tasks, the JSON must also include these required deliverable fields: artifact_paths, figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, roadmap_page, conclusion_preview_page, body_appendix_split, timing_plan, overlay_strategy, numerical_study_pages, insight_pages, audience_explanation_strategy. If any item is still incomplete, keep the field present and explicitly describe the blocker instead of omitting the field. answer, checklist, and table_coverage must use the same counting basis for tables.")
        : "",
      beamerMode && deckPhaseIndex(payload) >= 2
        ? "When writing slides.json, keep top-level deck contract fields synchronized with analysis.json. In particular, formal_statement_inventory must be present in slides.json whenever formal statements, algorithms, definitions, assumptions, propositions, lemmas, theorems, or corollaries are planned or rendered; map each item to its slide_ids and source_paragraph_ids."
        : "",
      beamerMode
        ? "When the source paper has zero explicit Figures or zero explicit Tables in the scoped main-text range, figure_coverage/table_coverage must not be empty arrays. Return a non-empty zero-inventory object such as {\"status\":\"covered\",\"total_source_items\":0,\"covered_items\":0,\"slide_ids\":[],\"notes\":\"main-text source inventory is 0\"} so the phase gate can distinguish explicit zero coverage from a missing field."
        : "",
      beamerMode
        ? (beamerPhase1
          ? "For Beamer phase 1, do not attempt exhaustive equation_coverage or notation_coverage in the returned JSON text. Keep those fields schema-valid with concise planning/blocker entries, and store detailed source grounding inside analysis.json for later phases. Do not inline full per-equation or per-symbol arrays into answer/notes. artifact_paths must still be an object map such as {\"analysis.json\": \"/abs/path/analysis.json\"}. equation_coverage must still be an array of objects with source_label, equation_numbers, slide_ids, status, and notes. For phase-1 placeholders, equation_numbers must contain parseable equation ids or ranges such as [1], [1,2,3], [\"Eq. (1)\"], [\"Eqs. (1)-(3)\"], [\"Eq. (A1)\"], or [\"Eqs. (A1)-(A3)\"]. Do not use bare shorthand strings like \"1-104\" or \"A1-A15\" without equation prefixes/structure. If appendix equations exist, either enumerate them in a parseable appendix form or mention the remaining appendix-mapping blocker in notes until later phases create real appendix slide mappings. notation_coverage must still be an array of objects with symbol, meaning, first_defined_slide_ids, used_slide_ids, source_paragraph_ids, source_quote, source_definition_summary, defined_on_first_visible_use, status, and notes. Even in phase 1, planned notation placeholders still need at least one non-empty source_paragraph_ids item plus a non-empty source_quote and source_definition_summary grounded in the original text; do not leave those arrays/strings empty."
          : deckPhaseIndex(payload) === 2
            ? "For Beamer phase 2, slides.json and the slide skeleton must be complete, but do not require equation_coverage or notation_coverage to be fully covered yet. equation_coverage may remain planned/analysis_only as long as every source equation or range is still explicitly inventoried and queued for phase 3; notation_coverage may remain planned/analysis_only as long as source-grounded symbol definitions are preserved for phase 4. Do not silently drop any equation range or notation symbol from the inventory."
            : deckPhaseIndex(payload) === 3
              ? "For Beamer phase 3, equation_coverage must be a structured array of real slide mappings with no planning-only placeholders. Each item must include source_label, equation_numbers, slide_ids, status, and notes. Enumerate every numbered equation or numbered equation range from the source without gaps. A numbered range such as Eqs. (2)-(6) may be covered by one grouped entry with equation_numbers [2,3,4,5,6], but only if the mapped slides visibly present the constituent equations rather than a single representative formula. Do not collapse a 3+-equation source range into one shorthand display equation. Treat equation numbering as continuous unless the source explicitly proves otherwise: if the deliverable reaches Eq.(7), then the source range before it (for example Eqs.(2)-(6)) cannot be silently omitted from coverage. At this phase, notation_coverage may still carry planned/partial placeholders, but they must remain source-grounded and aligned to the real slide inventory."
              : "For Beamer phase 4 and later, equation_coverage and notation_coverage must both be structured arrays with no planning-only placeholders. Every notation entry must point to real slide IDs where the symbol visibly appears. used_slide_ids must list only slides that visibly render that exact symbol, not earlier concept-only or natural-language hypothesis pages. If defined_on_first_visible_use is true, no used_slide_id may sort before the earliest first_defined_slide_id. The first visible occurrence of every symbol, operator, abbreviation, or hyper-parameter must already include a source-grounded definition based on the original text rather than generic domain knowledge; keep that definition visible on-slide (or inside equation explanation), not only in notes. Do not leave notation entries as planned/blocked/partial placeholders: if the symbol appears, define it on its first visible slide in the same round.")
        : "",
      beamerMode
        ? "For Beamer coverage fields, status must use canonical values only. equation_coverage status may be one of planned, analysis_only, covered, partial, missing, blocked, inline_integrated, standalone_supplement, covered_with_ocr_gap_note. notation_coverage status may be one of planned, analysis_only, defined, covered, partial, missing, blocked. Do not invent phase-local status strings such as phase4_structured_ready or planned_ready; put phase-specific readiness into coverage_stage or notes instead."
        : "",
      pptMode
        ? "For PPT tasks, analysis.json and slides.json are mandatory. In phase 5 and later, main.pptx and pptx_validation.json are mandatory; in the final phase, README.md is mandatory too. Notes must list concrete artifact paths for every artifact required by the current phase."
        : "",
      pptMode
        ? "For PPT tasks, create analysis.json, slides.json, README.md, and similar text artifacts with direct file writes or targeted edits, not via oversized python heredocs or giant shell redirections. Use exec only for short filesystem checks, validator runs, and the final renderer invocation."
        : "",
      pptMode
        ? "For PPT tasks, slides.json must expose a page-level plan with section, title, core_message, source_paragraph_ids for every content-bearing body slide, speaker_minutes as a local pacing hint only, whether each slide belongs to body or appendix, explicit kind, and structured blocks. The plan must explicitly mark the roadmap page, the conclusion-preview page, numerical-study slides, insight slides, and the final body-vs-appendix split. Use page kinds such as title, roadmap, conclusion_preview, content, figure_focus, table_focus, equation_focus, comparison, experiment_setup, results, takeaways, appendix_content, and qa."
        : "",
      pptMode
        ? "For PPT tasks, if an equation comes from a numbered equation or numbered equation range in the paper, the equation block must include label with the exact original numbering (for example Eq. (1), Eqs. (2)-(3), Eq. (13)-(16)). Do not hide equation numbering only inside notes or prose."
        : "",
      pptMode
        ? "For PPT tasks, keep one canonical equation-number ledger across analysis.json, slides.json, paragraph_ledger.equation_tags, equation_coverage, and equation block labels: main-text equations use 1, 2, 3, ... in source order; appendix equations use A1, A2, ...; never store alias-style tokens such as main-linear, def-unbiased, or prop-dgp inside equation_numbers."
        : "",
      pptMode
        ? "For PPT tasks, whenever visible prose needs to refer to an equation already shown inside the deck, the referenced equation must have a visible equation block with a label and an equation_coverage mapping to a real slide_id. Do not leave raw visible text like '式 (60)' as a literal copy from the paper unless that equation is visibly anchored by a labeled equation block in the deck."
        : "",
      pptMode
        ? "For PPT tasks, equation/figure/table-heavy pages must explicitly identify the corresponding equation number, figure number, or table number, and explain in natural academic Chinese what the item shows, what evidence it provides, and why the slide's claim follows. Do not reduce such pages to short slogans like '表达力提升/代价增加'. Do not use rigid label-style wording such as '原文锚点', '关键读法', or '解释链条' in visible slide text. Each bullet_list block must contain at least 5 items for equation_focus, figure_focus, table_focus, and experiment_setup pages; at least 4 items for content pages. Never truncate to 3 items. If reader_note or explanation fields are present on any block, they must also appear as explicit bullet items in the bullet_list block of that slide."
        : "",
      pptMode
        ? "For PPT tasks, keep slide body text formal, neutral, and paper-report-like. Avoid audience-directed teaching phrases or subjective wording such as '对未读者', '你会看到', '读这张图时', '最重要的是', '敢处理', or '诚实指出'. Prefer neutral academic verbs such as '表明', '显示', '说明', '进一步指出', '意味着', and '构成依据'."
        : "",
      pptMode
        ? "For PPT tasks, separate slide body from speaker notes. Use on-slide text for the core claim, supporting evidence, and significance; move presentation guidance, visual-reading prompts, transitions, and spoken audience-facing explanations into notes/speaker_notes instead of mixing them into body paragraphs or bullets."
        : "",
      pptMode
        ? "For PPT tasks, when a slide contains a paragraph or bullet_list, default to a formal academic progression that states the main conclusion first, then the supporting basis, then the significance, rather than conversational explanation. If a more colloquial explanation is genuinely useful, preserve it in notes instead of the visible slide text."
        : "",
      pptMode
        ? "For PPT tasks, if the task, template, or prior plan mentions a target slide count, treat that number only as a minimum lower bound rather than an exact cap: do not deliver fewer than that count unless the user explicitly relaxes it, and expand further whenever source coverage requires more slides."
        : "",
      pptMode
        ? "For PPT tasks, final answer must summarize the actual slide structure, body/appendix split, roadmap page, conclusion-preview page, dedicated numerical-study coverage, insight coverage, formula/figure/table/formal-statement/notation coverage, packaging status, and any remaining layout/rendering issues."
        : "",
      pptMode
        ? "For PPT phase 5 and later, use the deterministic PPT renderer whenever feasible. Validate slides.json before rendering, persist/report pptx_validation.json, and treat the task as incomplete if validation fails or if slides.json is ready but main.pptx is missing. Equations must be emitted as structured equation blocks with latex (plus explanation/label when available), not buried as plain paragraph text."
        : "",
      pptMode
        ? "For PPT tasks, do not rely on Beamer as an intermediate artifact. The final required artifact is main.pptx. Treat PPT as an independent backend with its own validator, layout presets, and equation-asset pathway."
        : "",
      pptMode
        ? "For PPT tasks, the JSON must also include these required deliverable fields: artifact_paths, figure_coverage, table_coverage, equation_coverage, notation_coverage, formal_statement_inventory, paragraph_ledger, roadmap_page, conclusion_preview_page, body_appendix_split, timing_plan, overlay_strategy, numerical_study_pages, insight_pages, audience_explanation_strategy. If any item is still incomplete, keep the field present and explicitly describe the blocker instead of omitting the field."
        : "",
      pptMode
        ? (pptPhase1
          ? "For PPT phase 1, the JSON must still include these required deliverable fields, but keep non-analysis fields compact and phase-local. analysis.json itself must carry paragraph_ledger plus top-level figure_coverage and table_coverage fields, including explicit zero-inventory objects when applicable. slides.json is only required from phase 2 onward. equation_coverage must still be an array of schema-valid objects with source_label, equation_numbers, slide_ids, status, and notes; use status=planned or analysis_only for phase-1 inventory placeholders, and do not invent phase-local status strings such as inventory_ready. If slide placement is not real yet, keep slide_ids as an empty array and put planned placement details into notes or planned_slide_ids."
          : "For PPT tasks, analysis.json must include paragraph_ledger: an ordered array where each source paragraph is summarized in one Chinese sentence with keys paragraph_id, section, and summary_sentence, plus equation/figure/table/formal hooks when available. Every content-bearing body slide in slides.json must map contiguous source_paragraph_ids back to that ledger.")
        : "",
      pptMode
        ? "For PPT tasks, ordinary body slides must advance through source_paragraph_ids monotonically. Use spans like [p07] or [p07,p08], not mixed jumps like [p01,p10]. Only conclusion_preview, takeaways, qa, or utility appendix pages may intentionally revisit earlier paragraphs."
        : "",
      pptMode
        ? "When the source paper has zero explicit Figures or zero explicit Tables in the scoped main-text range, figure_coverage/table_coverage must not be empty arrays. Return a non-empty zero-inventory object such as {\"status\":\"covered\",\"total_source_items\":0,\"covered_items\":0,\"slide_ids\":[],\"notes\":\"main-text source inventory is 0\"} so the phase gate can distinguish explicit zero coverage from a missing field."
        : "",
      pptMode
        ? "For PPT tasks, table_coverage must be an ordered per-source-mention mapping, not just a summary by unique table number. If the source markdown mentions Table 1 twice and Table 2 four times, table_coverage must contain 6 explicit entries in source order, and each entry must include the source mention or occurrence index plus the target slide ID(s)."
        : "",
      pptMode
        ? "For PPT tasks, preserve source-paper order. Except for title/roadmap/conclusion-preview/final-takeaway/utility appendix pages, the deck must follow the paper's section order and local paragraph order. Do not pull later results forward and do not merge non-contiguous source paragraphs onto one slide."
        : "",
      pptMode
        ? "For PPT tasks, when several formulas appear in one local stretch of prose, do not turn them into a single formula wall just to save logical slides. Split the chain across multiple slides whenever a reader who has not seen the paper would otherwise lose the argument."
        : "",
      pptMode && phase?.index === 2
        ? "For PPT phase 2 slides outline/skeleton, focus on the page-level plan and skeleton only. roadmap_page, conclusion_preview_page, body_appendix_split, numerical_study_pages, insight_pages, paragraph_ledger alignment, and artifact_paths/slides.json must be reviewer-ready. equation_coverage and notation_coverage may remain source-grounded planning placeholders here; do not pretend they are fully covered yet. Dense formula slides should already include a slide-level reveal/split plan using PPT-native consecutive slides, notes, or renderer-supported reveal fields rather than a vague deck-level note."
        : "",
      pptMode && phase?.index === 3
        ? "For PPT phase 3 equation coverage, convert equation_coverage into real slide mappings with exhaustive numbered coverage and visible equation blocks, but notation_coverage may still be source-grounded planned/partial placeholders until phase 4."
        : "",
      pptMode && phase?.index === 3
        ? "For PPT phase 3, never repair equation_coverage by changing the ledger alone. For every equation_coverage entry whose status is covered, the mapped slide_ids must point to slides in slides.json that visibly contain the corresponding formula in equation_blocks or blocks entries with type='equation' and a non-empty latex field. If a slide lacks that visible equation block, edit slides.json first by adding/splitting real formula slides, then update equation_coverage; otherwise leave the entry missing/blocked and explain the blocker instead of claiming covered."
        : "",
      pptMode && phase?.index === 3
        ? "For PPT phase 3 source grounding, source_paragraph_ids must include the source paragraphs where the equation actually appears. Do not map Eq. (n) to earlier explanatory paragraphs only. If the first equation paragraph is p29, p40, p93, etc., the corresponding equation_coverage entry and mapped slide must include that paragraph or a contiguous span containing it."
        : "",
      pptMode && phase?.index === 4
        ? "For PPT phase 4 notation/consistency, finish notation_coverage, first-use definitions, and whole-deck equation/notation/slide-id consistency. By the end of this phase, equation_coverage and notation_coverage must both be fully structured and no longer planning-only. In notation_coverage.symbol, use the same visible symbol spelling that appears on-slide, but omit surrounding math delimiters such as $...$, \\(...\\), or \\[...\\]. If equation blocks visibly contain coefficient, fixed-effect, or error symbols, add explicit notation_coverage entries for them instead of silently treating them as implicit."
        : "",
      pptMode
        ? "For PPT tasks, equation_coverage must be a structured array of objects. Each item must include source_label, equation_numbers, slide_ids, status, and notes. Enumerate every numbered equation or numbered equation range from the source without gaps. A numbered range such as Eqs. (2)-(6) may be covered by one grouped entry with equation_numbers [2,3,4,5,6], but only if the mapped slides visibly present the constituent equations rather than a single representative formula. Do not collapse a 3+-equation source range into one shorthand display equation. Treat equation numbering as continuous unless the source explicitly proves otherwise: if the deliverable reaches Eq.(7), then the source range before it (for example Eqs.(2)-(6)) cannot be silently omitted from coverage. If some numbered equations or numbered ranges are not yet mapped to slides, keep them in equation_coverage with status missing or blocked instead of silently dropping them. notation_coverage must be a structured array of objects with symbol, meaning, first_defined_slide_ids, used_slide_ids, source_paragraph_ids, source_quote, source_definition_summary, defined_on_first_visible_use, status, and notes. Every notation entry must point to real slide IDs where the symbol visibly appears. The first visible occurrence of every symbol, operator, abbreviation, or hyper-parameter must already include a source-grounded definition based on the original text rather than generic domain knowledge; keep that definition visible on-slide (or inside equation explanation), not only in notes. Do not let symbols such as D, B, φ, θ, Ω, PDE, PINN, or NTK appear before such a source-grounded first-use definition."
        : "",
      languageInstruction,
      'Return exactly one JSON object with keys: summary, answer, checklist, changed, notes, ready_for_review.',
      beamerThinArtifactEnvelopePhase
        ? `For this ${deckModeLabel} phase, artifact_paths is the only additional deliverable field that must appear in the returned JSON; the remaining contract fields must be recoverable from the exact artifact bundle on disk.`
        : 'For Beamer/PPT tasks, include the additional required deliverable fields requested above in the same JSON object.',
      beamerMode && phase?.finalPhase === true
        ? 'For final-phase Beamer tasks, the same JSON object must additionally include compile_status, readability_status, tex_warnings, layout_policy, visible_prose_recovery_hint, visible_prose_fidelity_final, and render_fidelity_safeguards.'
        : '',
      pptMode && phase?.finalPhase === true
        ? 'For final-phase PPT tasks, the same JSON object must additionally include render_status, validation_status, pptx_warnings, layout_policy, visible_prose_recovery_hint, visible_prose_fidelity_final, and render_fidelity_safeguards.'
        : '',
      "summary must be a short one-paragraph overview.",
      "answer must contain the full main answer in plain text and include all requested sections.",
      "checklist must be an array of strings. Use an empty array if no checklist is needed.",
      'Use booleans for changed and ready_for_review. No markdown fences. No extra text.',
      `Task:\n${taskForPrompt}`,
      repairTickets.length > 0
        ? `Structured repair tickets (authoritative machine-readable backlog):\n${JSON.stringify(repairTicketsForPrompt, null, 2)}`
        : "",
      reviewerFeedback ? `Reviewer feedback:\n${reviewerFeedback}` : "",
    ].filter(Boolean).join("\n\n");
  }

  if (role === "reviewer") {
    return [
      "You are the reviewer role in a deterministic multi-agent pipeline.",
      DEFAULT_PYTHON_ENVIRONMENT_INSTRUCTION,
      "Review the programmer result for correctness, risk, and completeness.",
      "Do not rewrite the task. Decide approve or reject.",
      languageInstruction,
      "The embedded programmer output may be prompt-compacted for transport. Metadata such as prompt_compacted, payload_compacted, artifact_backed_payload_compacted, total_items, shown_items, omitted_for_prompt, omitted_for_payload, or truncated string markers describe prompt truncation only, not missing deck content. Do not infer coverage gaps solely from those prompt-compaction markers.",
      "Reject the result if it only provides a summary while omitting a list, checklist, steps, or other explicit deliverable requested by the user.",
      "Reject the result if the user asked for a checklist and the checklist is missing or too incomplete to use directly.",
      "Reject the result if answer is missing, if answer duplicates summary, or if a list-style task is answered as one short paragraph instead of a usable list.",
      beamerReviewerPhase2
        ? "For Beamer phase 2 review, audit only slides.json outline/skeleton readiness plus chapter/source order, roadmap/conclusion-preview/body-appendix planning, and whether equation/notation inventories remain explicitly carried forward."
        : "",
      beamerReviewerPhase2
        ? "For Beamer phase 2 review, reject if slides.json is missing from the reported artifacts, or if chapter/source ordering, roadmap/conclusion-preview/body-appendix planning, numerical-study pages, or insight pages are incomplete/unstructured. Do not require phase-3 equation mappings or phase-4 notation first-use closure yet."
        : "",
      beamerReviewerPhase2
        ? "For Beamer phase 2 review, do not reject solely for missing main.tex/main.pdf, compile status, or layout issues; those belong to later phases."
        : "",
      beamerReviewerPhase2
        ? "For Beamer phase 2 review, do not require visible equation/align blocks, rendered Beamer frames, or notation first-use closure. Those are phase 3/4/5 responsibilities; phase 2 only needs the inventories to be explicitly carried forward in slides.json."
        : "",
      beamerReviewerPhase3
        ? "For Beamer phase 3 review, audit equation_coverage readiness only: exhaustive numbered equation mapping, slide-level visible equation blocks, and source-order continuity. Do not require notation first-use closure or compiled main.tex/main.pdf yet."
        : "",
      beamerReviewerPhase3
        ? "For Beamer phase 3 review, reject if equation_coverage is incomplete, skips numbered ranges, leaves planned/blocker placeholders, or maps formulas to slides without real visible equation blocks."
        : "",
      beamerReviewerPhase3
        ? "For Beamer phase 3 review, do not reject solely for missing main.tex/main.pdf, compile status, later delivery narration, or notation first-use tickets; those belong to later phases."
        : "",
      beamerReviewerPhase4
        ? "For Beamer phase 4 review, audit notation/consistency readiness only: first-use symbol definitions, source grounding, equation/notation cross-checking, and slide-id consistency."
        : "",
      beamerReviewerPhase4
        ? "For Beamer phase 4 review, reject if notation_coverage is incomplete/unstructured, if first-use definitions are missing, or if equation/notation/slide-id consistency is still broken."
        : "",
      beamerReviewerPhase4
        ? "For Beamer phase 4 review, do not reject solely for missing compile/layout/final-delivery polish unless those issues stem from unresolved notation/consistency defects."
        : "",
      beamerReviewerPhase4
        ? "For Beamer phase 4 review, do not apply phase-2 skeleton/planning rules. If equation_coverage and notation_coverage use canonical completed statuses such as covered/defined and point to real slide_ids, do not ask to downgrade them back to phase2_planned."
        : "",
      (beamerReviewerPhase3 || beamerReviewerPhase4)
        ? "If you discover purely structural/schema defects in notation_coverage or equation_coverage entries (e.g. missing status field, empty notes, invalid source_label format, missing equation_numbers for non-planned entries), directly edit the corresponding artifact file (slides.json or analysis.json) in-place to fix those fields. In your feedback, note 'Schema patched: <what was fixed>'. Only open repair_tickets for substantive content issues (wrong source_paragraph_ids mappings, missing equation blocks, incorrect symbol definitions, missing slide content, etc.). Do not over-edit: limit your patches to notation_coverage and equation_coverage arrays; never modify paragraph_ledger, slide layout, tex source, or other fields."
        : "",
      beamerReviewerPhase5
        ? "For Beamer phase 5 review, audit compile_and_structural_repair only: main.tex/main.pdf presence, slides-vs-frames structural alignment, compile status, visible prose fidelity, and layout quality."
        : "",
      beamerReviewerPhase5
        ? "For Beamer phase 5 review, reject if main.tex or main.pdf is missing, if compile status is failing/unknown, if severe layout issues persist, or if slides.json and main.tex are structurally misaligned."
        : "",
      beamerReviewerPhase5
        ? "For Beamer phase 5 review, do not re-open phase-2/3/4 planning tickets unless they still manifest as real compile, structure, or visible-content defects."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 review, treat this as review_and_auto_rework. Audit residual risks, repair-ticket quality, and whether the orchestrator can retry from the minimum necessary phase."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 review, reject if residual defects are not converted into concrete repair tickets with retry_from_phase guidance, or if the hand-off still hides material risks."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 review, route tickets back to phase 2/3/4 only when the defect still manifests in the current artifact bundle as a real structural/coverage problem. Do not send a ticket back to an early planning phase merely because the phase-6 summary mentions analysis.json/slides.json fields."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 review, when programmer_output is a thin-envelope or artifact-backed checkpoint with artifact_paths pointing to one exact output bundle that already contains analysis.json, slides.json, main.tex, and main.pdf, treat the on-disk bundle as authoritative and review those artifacts directly instead of demanding that the programmer inline the full contract JSON again."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 review, do not reject solely because the answer emphasizes verification, rebuild, recovery, reproducibility, or checkpoint hand-off work, because changed=false, or because already-materialized coverage fields were intentionally omitted from the returned JSON in thin-envelope mode."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 review, if you reject, cite at least one concrete manifested defect in the current artifact bundle and include retry_from_phase guidance. Generic complaints such as 'only restored a checkpoint', 'only described validation', or 'no actual repair' are invalid when the cited defect does not currently manifest on disk."
        : "",
      beamerReviewerPhase7
        ? "For Beamer phase 7 review, audit only final_acceptance_delivery: whole-deck consistency, delivery summary quality, packaging completeness, and true final readiness."
        : "",
      beamerReviewerPhase7
        ? "For Beamer phase 7 review, reject if analysis.json, slides.json, main.tex, main.pdf, README.md, asset_manifest.json, or figures/ is missing from the packaged output, or if artifact_paths mixes multiple output directories / legacy bundles."
        : "",
      beamerReviewerPhase7
        ? "For Beamer phase 7 review, do not reopen phase 2-6 planning tickets unless the final bundle still contains a real manifested defect. Phase 7 is for final consistency and delivery readiness, not for relitigating stale historical checkpoints."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if analysis.json, slides.json, main.tex, or main.pdf are missing from the reported artifacts."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if README.md, asset_manifest.json, or figures/ is missing from the final packaged bundle, or if artifact_paths mixes multiple output directories / legacy bundles."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if the result does not explicitly address chapter order, exhaustive formula/figure/table coverage, exhaustive formal-statement coverage, or if it skips the slide-planning stage. When table_coverage is provided as an ordered per-source-mention mapping, count those entries directly instead of collapsing repeated Table labels."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if the result does not explicitly include a roadmap/汇报路线图 page, a conclusion-preview/结论预告 page, a clear body-vs-appendix plan, dedicated numerical-study slides, per-insight slides, or if it treats a default/target slide count as a fixed cap instead of a lower bound that may expand with source coverage."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if the result suppresses overlays by default instead of using them strategically for readability, if it mentions overlay/page-count control without explaining the actual strategy and its impact on physical page count / timing, or if main.tex does not keep \\setbeamercovered{transparent} as the covered-content policy."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if equation_coverage is not a structured array of explicit mappings, if any numbered equation or numbered equation range from the source is skipped, if numbering continuity implies a missing source range (for example the deliverable reaches Eq.(7) but never acknowledges Eqs.(2)-(6)), if notation_coverage is missing or not structured, if key symbols/abbreviations are not defined on their first visible appearance with source_paragraph_ids + source_quote grounding from the original text, or if the result only lists representative equations instead of exhaustive equation coverage."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if notes do not identify concrete artifact paths, if the deliverable jumps straight to generic prose without a page-level plan, or if it only reports key figures/formulas instead of an exhaustive inventory."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if theorem/proposition/lemma/corollary/definition/assumption coverage is summarized instead of preserved as full faithful Chinese translation, if formal statements are merged into the same slide as economic intuition instead of being separated when dense, or if the deck is too terse for readers who have not read the paper."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if visible slides.json or main.tex text still exposes internal scaffolding labels such as '核心信息', '来源段落', 'source_paragraph_ids', '这页负责', '服务于未读论文听众', or block titles like '公式 A1/A2' instead of natural academic wording such as '式 (A1)'."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if paragraph_ledger.summary_sentence is mostly copied English source prose, if visible bullets are dominated by English source excerpts, or if main.tex/PDF visibly contains escaped LaTeX artifacts such as \\textbackslash{}, \\textasciicircum{}, \\$P\\_, \\{}gamma, \\{}mathrm, or raw fragments like 'where $...'."
        : "",
      beamerMode
        && !beamerReviewerPhaseScoped
        ? "For Beamer tasks, reject if main.tex materially drops the visible explanatory prose promised by slides.json. In particular, if a planned slide has 4+ explanatory bullet items, the rendered page must retain at least 2 visible explanatory bullets; equation-heavy / experiment_setup / results / comparison / content-heavy pages with 3+ displayed equations must retain ALL planned visible explanatory bullets (any lost bullet is a reject). Reject if visible-prose fidelity is broken even when the deck compiles successfully."
        : "",
      pptMode
        ? "For PPT tasks, reject if analysis.json, slides.json, main.pptx, or pptx_validation.json are missing from the reported artifacts; for final-phase PPT tasks, also reject if README.md is missing."
        : "",
      pptMode
        ? "For PPT tasks, reject if the result does not explicitly include a roadmap page, a conclusion-preview page, a clear body-vs-appendix plan, dedicated numerical-study slides, per-insight slides, if it skips the page-planning stage, or if it treats a default/target slide count as a fixed cap instead of a lower bound that may expand with source coverage."
        : "",
      pptMode
        ? "For PPT tasks, reject if equation_coverage is not a structured array of explicit mappings, if any numbered equation or numbered equation range from the source is skipped, if numbering continuity implies a missing source range (for example the deliverable reaches Eq.(7) but never acknowledges Eqs.(2)-(6)), if notation_coverage is missing or not structured, if key symbols/abbreviations are not defined on their first visible appearance with source_paragraph_ids + source_quote grounding from the original text, or if the result only lists representative equations instead of exhaustive equation coverage."
        : "",
      pptMode
        ? "For PPT tasks, reject if paragraph_ledger is missing, if content-bearing body slides lack source_paragraph_ids, if source_paragraph_ids jump across non-contiguous source paragraphs without a clear exception, or if figure_coverage/table_coverage uses an empty array for a genuine zero-inventory case instead of an explicit zero-inventory object."
        : "",
      pptMode
        ? "For PPT tasks, reject if notes do not identify concrete artifact paths, or if the deck summary does not mention formula/figure/table/formal-statement coverage and remaining layout/rendering issues."
        : "",
      pptMode
        ? "For PPT tasks, reject if any figure block still points to a remote http(s) URL instead of a downloaded local file inside the project workspace."
        : "",
      pptMode
        ? "For PPT tasks, reject if the visible slide wording is dominated by classroom-style coaching or audience-directed phrases instead of formal academic Chinese, or if subjective wording replaces neutral paper-report phrasing on content-heavy slides."
        : "",
      pptMode
        ? "For PPT tasks, reject if presentation guidance, visual-reading instructions, or spoken transitions that should live in notes/speaker_notes are mixed into the visible slide body as the main prose."
        : "",
      pptMode
        ? "For PPT tasks, reject if visible slide text exposes internal scaffold labels such as '核心信息', '来源段落', 'source_paragraph_ids', '这页负责', '服务于未读论文听众', '公式 A1/A2', or rigid label-style wording such as '原文锚点', '关键读法', or '解释链条'."
        : "",
      phaseLabel
        ? `${phaseLabel}. Review only the deliverable expected at this phase; do not reject merely because later-phase artifacts are absent unless this is the final phase.`
        : "",
      phase && phase.finalPhase === false
        ? "For non-final phases, approve if the current phase goal is correctly completed and its required artifacts/structured fields are present, even though the overall task is not final yet."
        : "",
      beamerMode && phase?.reviewerPhase === true && !beamerReviewerPhase5 && !beamerReviewerPhase7
        ? "For Beamer review-and-auto-rework phase, treat rejection as issue extraction rather than a terminal stop. Still set approved=false when needed, but encode concrete repair tickets in feedback/risk so the orchestrator can auto-rework from the minimum necessary phase. However, do not approve a round that merely re-labels equation_coverage or notation_coverage as blocked/partial/missing: if formulas or first-use symbol definitions are still absent from visible slides, reject and demand real slide-level repairs in the same retry cycle."
        : "",
      phase && phase.finalPhase === true && !beamerReviewerPhase7
        ? "This is the final phase. Apply the full final acceptance standard."
        : "",
      'Return exactly one JSON object with keys: approved, feedback, risk. If you reject in Beamer/PPT reviewer phases, put repair tickets inline in feedback/risk using a compact pattern such as type=layout | severity=moderate | slides=s05,s06 | retry_from_phase=3 | fix=split dense frame and preserve visible prose.',
      "approved must be a boolean. No markdown fences. No extra text.",
      `Original task:\n${taskForPrompt}`,
      programmerOutput ? `Programmer output:\n${JSON.stringify(programmerOutputForPrompt, null, 2)}` : "",
    ].filter(Boolean).join("\n\n");
  }

  if (role === "tester") {
    return [
      "You are the tester role in a deterministic multi-agent pipeline.",
      DEFAULT_PYTHON_ENVIRONMENT_INSTRUCTION,
      "Assess whether the task is ready based on the programmer output and optional test command.",
      "If a concrete test command is supplied, prefer running or evaluating that command.",
      languageInstruction,
      "The embedded programmer output may be prompt-compacted for transport. Metadata such as prompt_compacted, payload_compacted, artifact_backed_payload_compacted, total_items, shown_items, omitted_for_prompt, omitted_for_payload, or truncated string markers describe prompt truncation only, not missing deck content. Do not fail solely because coverage ledgers or planning fields were omitted from the prompt when artifact_paths points to the authoritative on-disk bundle.",
      "For read-only answer tasks, verify that the final deliverable fully contains the requested sections instead of only a summary.",
      "Fail the result if a list/checklist task does not contain a usable multi-line answer or the actionable checklist is missing.",
      beamerFinalOrUnphased
        ? "For Beamer tasks, fail if analysis.json, slides.json, main.tex, or main.pdf are not explicitly reported."
        : "",
      beamerFinalOrUnphased
        ? "For Beamer tasks, fail if README.md, asset_manifest.json, or figures/ is missing from the final packaged bundle, or if artifact_paths mixes multiple output directories / legacy bundles."
        : "",
      beamerFinalOrUnphased
        ? "For Beamer tasks, fail if the deliverable does not report compile status, packaging status, or unresolved missing-asset / compile blockers."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if roadmap/汇报路线图, conclusion-preview/结论预告, body-vs-appendix planning, dedicated numerical-study slides, per-insight slides, or an explicit non-compressed final page structure is missing from the reported deliverable, or if the deliverable treats a default/target slide count as a fixed cap instead of a lower bound that may expand with source coverage."
        : "",
      beamerMode
        ? "For Beamer tasks, verify the reported deliverable covers slide count / timing, chapter-order flow, dedicated numerical-study coverage, per-insight coverage, exhaustive formula/figure/table/formal-statement completeness, audience-oriented explanation, and overlay/page-count control, including how overlays affect physical page count and timing."
        : "",
      beamerReviewerPhase2
        ? "For Beamer phase 2 testing, require only slides outline/skeleton readiness: slides.json, roadmap/conclusion-preview/body-appendix planning, numerical-study pages, insight pages, and source-order coherence. Do not fail only because equation_coverage or notation_coverage is still phase-local planned inventory."
        : "",
      beamerReviewerPhase3
        ? "For Beamer phase 3 testing, fail if equation_coverage is not yet exhaustive, structured, and mapped to real slide_ids with visible equation blocks. Do not fail only because notation first-use closure or compile artifacts are still deferred to later phases."
        : "",
      beamerReviewerPhase4
        ? "For Beamer phase 4 testing, fail if notation_coverage is not yet source-grounded, first-use complete, and consistent with the equation/slide mapping inventory."
        : "",
      beamerReviewerPhase5
        ? "For Beamer phase 5 testing, fail if main.tex/main.pdf is missing, if slides.json and main.tex are structurally misaligned, if visible prose fidelity is broken, or if severe layout warnings remain."
        : "",
      beamerReviewerPhase6
        ? "For Beamer phase 6 testing, fail if residual issues are not translated into concrete reviewer/tester repair tickets with a minimum retry_from_phase."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if equation_coverage is not a structured array of explicit mappings, if any numbered equation or numbered equation range from the source is skipped, if numbering continuity implies a missing source range (for example the deliverable reaches Eq.(7) but never acknowledges Eqs.(2)-(6)), if notation_coverage is missing or not structured, if key symbols/abbreviations are not defined on their first visible appearance with source_paragraph_ids + source_quote grounding from the original text, or if the deliverable only mentions representative equations instead of exhaustive equation coverage."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if the report does not enumerate all source figures/tables and crucial formal statements with slide mapping, or if it only mentions key items."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if crucial formal statements are not explicitly preserved as full faithful Chinese translations, or if the deck is too terse for readers new to the paper."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if visible slides.json or main.tex text still exposes internal scaffolding labels such as '核心信息', '来源段落', 'source_paragraph_ids', '这页负责', '服务于未读论文听众', or block titles like '公式 A1/A2' instead of natural academic wording such as '式 (A1)'."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if paragraph_ledger.summary_sentence is mostly copied English source prose, if visible bullets are dominated by English source excerpts, or if main.tex/PDF visibly contains escaped LaTeX artifacts such as \\textbackslash{}, \\textasciicircum{}, \\$P\\_, \\{}gamma, \\{}mathrm, or raw fragments like 'where $...'."
        : "",
      beamerMode
        ? "For Beamer tasks, fail if main.tex materially drops the visible explanatory prose promised by slides.json. In particular, if a planned slide has 4+ explanatory bullet items, the rendered page must retain at least 2 visible explanatory bullets; equation-heavy / experiment_setup / results / comparison / content-heavy pages with 3+ displayed equations must retain ALL planned visible explanatory bullets (any lost bullet is a hard fail). Treat only severe overfull layout warnings as a hard test failure; moderate overfull issues should be reported as repairable layout debt."
        : "",
      pptMode
        ? "For PPT tasks, fail if analysis.json, slides.json, main.pptx, or pptx_validation.json are not explicitly reported; for final-phase PPT tasks, also fail if README.md is missing."
        : "",
      pptMode
        ? "For PPT tasks, fail if the deliverable does not report layout/rendering status, packaging status, or unresolved missing-asset/render blockers."
        : "",
      pptMode
        ? "For PPT tasks, fail if roadmap, conclusion-preview, body-vs-appendix planning, dedicated numerical-study slides, or per-insight slides are missing from the reported deliverable, or if the deliverable treats a default/target slide count as a fixed cap instead of a lower bound that may expand with source coverage."
        : "",
      pptMode
        ? "For PPT tasks, fail if equation_coverage is not a structured array of explicit mappings, if any numbered equation or numbered equation range from the source is skipped, if numbering continuity implies a missing source range (for example the deliverable reaches Eq.(7) but never acknowledges Eqs.(2)-(6)), if notation_coverage is missing or not structured, if key symbols/abbreviations are not defined on their first visible appearance with source_paragraph_ids + source_quote grounding from the original text, or if the deliverable only mentions representative equations instead of exhaustive equation coverage."
        : "",
      pptMode
        ? "For PPT tasks, fail if paragraph_ledger is missing, if content-bearing body slides lack source_paragraph_ids, if source_paragraph_ids jump across non-contiguous source paragraphs without a clear exception, or if figure_coverage/table_coverage uses an empty array for a genuine zero-inventory case instead of an explicit zero-inventory object."
        : "",
      pptMode
        ? "For PPT tasks, fail if any figure block still uses a remote http(s) URL instead of a downloaded local file path."
        : "",
      pptMode
        ? "For PPT tasks, fail if the reported slide text remains dominated by teaching-tone, audience-facing, or subjective wording instead of formal academic Chinese, especially on method, theorem, figure, table, and result slides."
        : "",
      pptMode
        ? "For PPT tasks, fail if the deliverable does not clearly separate visible slide text from notes/speaker_notes for presentation guidance, visual-reading prompts, and spoken transitions."
        : "",
      pptMode
        ? "For PPT tasks, fail if visible slide text still exposes internal scaffold labels such as '核心信息', '来源段落', 'source_paragraph_ids', '这页负责', '服务于未读论文听众', '公式 A1/A2', or rigid label-style wording such as '原文锚点', '关键读法', or '解释链条'."
        : "",
      phaseLabel
        ? `${phaseLabel}. Test against the expected output of this phase.`
        : "",
      phase && phase.finalPhase === false
        ? "For non-final phases, do not fail only because later-phase artifacts are absent; focus on whether the current phase output is coherent, structured, and sufficient to advance."
        : "",
      phase && phase.finalPhase === true
        ? "This is the final phase. Apply the full final readiness test."
        : "",
      'Return exactly one JSON object with keys: passed, summary, failures.',
      "passed must be a boolean. No markdown fences. No extra text.",
      `Original task:\n${taskForPrompt}`,
      programmerOutput ? `Programmer output:\n${JSON.stringify(programmerOutputForPrompt, null, 2)}` : "",
      testerCommand ? `Suggested test command:\n${testerCommand}` : "",
    ].filter(Boolean).join("\n\n");
  }

  fail(`unsupported role: ${role}`);
}

function buildRoleSessionKey(role, prompt) {
  const promptHash = crypto.createHash("sha1").update(String(prompt || "")).digest("hex").slice(0, 8);
  const nonce = crypto.randomUUID().replace(/-/g, "").slice(0, 12);
  return `agent:${role}:dp:${promptHash}:${nonce}`;
}

function buildRoleSessionId(role, prompt) {
  const roleTag = String(role || "agent").slice(0, 3);
  const promptHash = crypto.createHash("sha1").update(String(prompt || "")).digest("hex").slice(0, 8);
  const nonce = crypto.randomUUID().replace(/-/g, "").slice(0, 10);
  return `dp-${roleTag}-${promptHash}-${nonce}`;
}

function resolveAgentId(role, payload) {
  if (role === "programmer" && (taskIsPpt(payload) || taskIsBeamer(payload))) {
    return "pipeline-programmer";
  }
  return role;
}

async function getGatewayCall() {
  if (!gatewayCallPromise) {
    gatewayCallPromise = (async () => {
      const errors = [];
      for (const modulePath of [...OPENCLAW_GATEWAY_CALL_MODULES].reverse()) {
        try {
          const mod = await import(pathToFileURL(modulePath).href);
          if (typeof mod.callGateway === "function") {
            return mod.callGateway;
          }
          if (typeof mod.r === "function") {
            return mod.r;
          }
          const discovered = Object.values(mod).find((value) => typeof value === "function" && value.name === "callGateway");
          if (typeof discovered === "function") {
            return discovered;
          }
          errors.push(`${modulePath}: missing callGateway export`);
        } catch (error) {
          errors.push(`${modulePath}: ${error?.message || String(error)}`);
        }
      }
      throw new Error(`Unable to locate callGateway export. ${errors.join("; ")}`);
    })();
  }
  return gatewayCallPromise;
}

async function invokeAgent(role, prompt, sessionId, sessionKey, payload, options = {}) {
  const callGateway = await getGatewayCall();
  const timeoutSeconds = Math.ceil(getAgentTimeoutMs(role) / 1000);
  return await callGateway({
    method: "agent",
    params: {
      agentId: resolveAgentId(role, payload),
      sessionId,
      message: prompt,
      thinking: role === "programmer" ? "medium" : "low",
      timeout: timeoutSeconds,
      deliver: false,
      bestEffortDeliver: false,
      idempotencyKey: sessionId,
    },
    expectFinal: true,
    timeoutMs: Math.max(10_000, (timeoutSeconds + 30) * 1000),
    requiredMethods: ["agent"],
  });
}

function normalizeAgentEnvelope(result) {
  const payloads = result?.result?.payloads || result?.payloads || [];
  const texts = payloads
    .flatMap((item) => [
      typeof item?.text === "string" ? item.text : "",
      typeof item?.body === "string" ? item.body : "",
    ])
    .map((text) => String(text || "").trim())
    .filter(Boolean);

  let chosenText = texts[texts.length - 1] || "";
  let content = null;
  let contentValid = false;

  for (let index = texts.length - 1; index >= 0; index -= 1) {
    const candidate = texts[index];
    try {
      content = parseJsonCandidate(candidate);
      chosenText = candidate;
      contentValid = true;
      break;
    } catch {
      continue;
    }
  }

  if (!contentValid) {
    content = {
      parse_error: "agent did not return valid JSON",
      raw_text: chosenText,
    };
  }

  return {
    raw: result,
    text: chosenText,
    content,
    contentValid,
  };
}

function shouldDeferArtifactBackedTranscriptResult(result, payload) {
  if (!result?.contentValid) return false;
  if (!payload?.phase || payload.phase.finalPhase === true) return false;
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  if (!(result?.raw?.transcriptRecovered === true && result?.raw?.inferredFromArtifacts === true)) {
    return false;
  }
  if (resultIsArtifactBackedPhaseDiagnostic(result, payload)) {
    return false;
  }
  return !resultIsLocallyValidArtifactBackedRecovery(result, payload);
}

function resultIsLocallyValidArtifactBackedRecovery(result, payload) {
  if (!result?.contentValid) return false;
  if (!(taskIsBeamer(payload) || taskIsPpt(payload))) return false;
  const content = result?.content;
  if (!isPlainObject(content)) return false;
  if (!(content.beamer_artifact_recovered === true || content.ppt_artifact_recovered === true || content.inferred_from_artifacts === true)) {
    return false;
  }
  const artifactPaths = normalizeArtifactPathsMap(content.artifact_paths);
  if (!isPlainObject(artifactPaths) || Object.keys(artifactPaths).length === 0) return false;
  const normalized = normalizeProgrammerResult({
    ...result,
    content: {
      ...content,
      artifact_paths: artifactPaths,
    },
  }, payload);
  const normalizedContent = normalized?.content || content;
  if (validateProgrammerContentWithLocalPreflight(normalizedContent, payload).length === 0) {
    return true;
  }
  if (taskIsBeamer(payload) && canCheckpointRecoveredBeamerPhaseContent(normalizedContent, payload)) {
    return true;
  }
  return false;
}

function deferredArtifactBackedTranscriptFallback(deferredResult, payload, markerField, extraContent = null) {
  if (
    !resultIsLocallyValidArtifactBackedRecovery(deferredResult, payload)
    && !resultIsArtifactBackedPhaseDiagnostic(deferredResult, payload)
  ) {
    return null;
  }
  return {
    ...deferredResult,
    content: {
      ...(deferredResult.content || {}),
      ...(isPlainObject(extraContent) ? extraContent : {}),
      [markerField]: true,
    },
  };
}

async function runAgent(role, prompt, payload) {
  const effectiveAgentId = resolveAgentId(role, payload);
  const sessionId = buildRoleSessionId(effectiveAgentId, prompt);
  const sessionKey = buildRoleSessionKey(effectiveAgentId, prompt);
  const startedAtMs = Date.now();
  const transcriptPath = transcriptPathForSession(effectiveAgentId, sessionId);
  const isProgrammerLike = effectiveAgentId === "programmer" || effectiveAgentId === "pipeline-programmer";
  let deferredTranscriptResult = null;
  const agentAbortController = new AbortController();
  let timeoutHandle = null;
  const abortPendingAgent = () => {
    if (timeoutHandle) {
      clearTimeout(timeoutHandle);
      timeoutHandle = null;
    }
    if (!agentAbortController.signal.aborted) {
      try {
        agentAbortController.abort(new Error(`runAgent settled before ${role} agent invocation completed`));
      } catch {
        agentAbortController.abort();
      }
    }
  };

  try {
    const taggedAgentPromise = invokeAgent(role, prompt, sessionId, sessionKey, payload, {
      abortSignal: agentAbortController.signal,
    })
      .then((result) => ({ kind: "agent", result }))
      .catch((error) => ({ kind: "agent_error", error }));
    const roleTimeoutMs = getAgentTimeoutMs(role);
    const taggedTimeoutPromise = new Promise((resolve) => {
      timeoutHandle = setTimeout(() => {
        resolve({ kind: "agent_error", error: new Error(`agent timed out after ${roleTimeoutMs}ms`) });
      }, roleTimeoutMs + 5000);
    });
    // Transcript-based liveness monitor: detect sub-agent death early by watching
    // for transcript stalls. If no new content for roleStallTimeoutMs, try artifact
    // recovery and return early rather than waiting for the full hard timeout.
    const roleStallTimeoutMs = getAgentStallTimeoutMs(role);
    const taggedTranscriptStallPromise = new Promise((resolve) => {
      let stallFingerprint = "";
      let stallLastChangeAt = Date.now();
      const stallPoll = () => {
        if (agentAbortController.signal.aborted) return;
        try {
          const tstate = inspectTranscriptState(transcriptPath);
          if (tstate?.result?.contentValid) {
            resolve({ kind: "transcript_stalled", result: tstate.result });
            return;
          }
          const fingerprint = JSON.stringify([
            tstate?.lineCount || 0,
            tstate?.lastRole || "",
            tstate?.lastTimestamp || "",
          ]);
          const now = Date.now();
          if (fingerprint !== stallFingerprint) {
            stallFingerprint = fingerprint;
            stallLastChangeAt = now;
          }
          if (now - stallLastChangeAt >= roleStallTimeoutMs) {
            const inferred = readTranscriptAgentResult(transcriptPath, {
              recovered_from_session: transcriptPath,
            }, {
              allowInferredFallback: true,
              payload,
            });
            if (inferred?.contentValid && resultIsLocallyValidArtifactBackedRecovery(inferred, payload)) {
              resolve({ kind: "transcript_stalled", result: inferred });
              return;
            }
            resolve({
              kind: "transcript_stalled",
              result: {
                text: inferred?.text || `Transcript stalled for ${Math.round(roleStallTimeoutMs / 60000)} min without valid artifacts`,
                content: {
                  ...(inferred?.content || {}),
                  recovered_from_stalled_transcript: true,
                  transcript_stalled_for_ms: now - stallLastChangeAt,
                },
                contentValid: false,
              },
            });
            return;
          }
        } catch {
          // Ignore polling errors; continue monitoring
        }
        setTimeout(stallPoll, TRANSCRIPT_POLL_INTERVAL_MS);
      };
      stallPoll();
    });
    let raced = await Promise.race([
      taggedAgentPromise,
      taggedTimeoutPromise,
      taggedTranscriptStallPromise,
    ]);
    if (raced.kind === "transcript_stalled") {
      const stallResult = raced.result;
      if (stallResult?.contentValid && shouldDeferArtifactBackedTranscriptResult(stallResult, payload)) {
        const deferred = deferredArtifactBackedTranscriptFallback(
          stallResult, payload,
          "recovered_after_transcript_stall_detection"
        );
        if (deferred) return deferred;
      }
      if (stallResult?.contentValid) return stallResult;
      throw new Error(stallResult?.text || `Agent ${role} transcript stalled`);
    }
    if (raced.kind === "agent_error") {
      const deferredAfterAgentError = deferredArtifactBackedTranscriptFallback(
        deferredTranscriptResult,
        payload,
        "recovered_after_agent_error_using_deferred_transcript_result"
      );
      if (deferredAfterAgentError) {
        return deferredAfterAgentError;
      }
      throw raced.error;
    }
    if (raced.kind === "transcript") {
      const transcriptResult = raced.result || readTranscriptAgentResult(transcriptPath, null, { payload });
      if (shouldDeferArtifactBackedTranscriptResult(transcriptResult, payload)) {
        deferredTranscriptResult = transcriptResult;
      } else if (transcriptResult?.contentValid) {
        return transcriptResult;
      } else if (transcriptResult?.text) {
        const partial = recoverPartialAgentResult(effectiveAgentId, startedAtMs, payload, transcriptPath);
        if (partial?.contentValid) {
          return {
            ...partial,
            text: partial.text || transcriptResult.text,
            content: {
              ...(partial.content || {}),
              recovered_from_settled_transcript_before_agent_exit: true,
              raw_text: partial.content?.raw_text || transcriptResult.text,
            },
          };
        }
        if (transcriptResult?.content?.agent_terminal_error === true) {
          deferredTranscriptResult = transcriptResult;
          raced = await Promise.race([taggedAgentPromise, taggedTimeoutPromise]);
          if (raced.kind !== "agent_error") {
            const normalizedAgentResult = normalizeAgentEnvelope(raced.result);
            if (normalizedAgentResult?.contentValid) {
              return normalizedAgentResult;
            }
          }
          throw new Error(
            String(
              transcriptResult?.content?.recovered_error_message
              || transcriptResult?.content?.parse_error
              || transcriptResult.text
              || `openclaw agent failed for ${role}`
            ).trim() || `openclaw agent failed for ${role}`
          );
        }
        if (partial) {
          return {
            ...partial,
            text: partial.text || transcriptResult.text,
            content: {
              ...(partial.content || {}),
              recovered_from_settled_transcript_before_agent_exit: true,
              raw_text: partial.content?.raw_text || transcriptResult.text,
            },
          };
        }
        return {
          ...transcriptResult,
          content: {
            ...(transcriptResult.content || {}),
            recovered_from_settled_transcript_before_agent_exit: true,
            ready_for_review: false,
          },
          contentValid: false,
        };
      }
      raced = await Promise.race([taggedAgentPromise, taggedTimeoutPromise]);
      if (raced.kind === "agent_error") {
        const deferredAfterAgentError = deferredArtifactBackedTranscriptFallback(
          deferredTranscriptResult,
          payload,
          "recovered_after_agent_error_using_deferred_transcript_result"
        );
        if (deferredAfterAgentError) {
          return deferredAfterAgentError;
        }
        throw raced.error;
      }
    }
    const result = raced.result;
    const normalizedAgentResult = normalizeAgentEnvelope(result);
    const transcriptResult = isProgrammerLike
      ? await waitForSettledTranscriptResult(transcriptPath, startedAtMs, { payload }) || readTranscriptAgentResult(transcriptPath, null, { payload })
      : readTranscriptAgentResult(transcriptPath, null, { payload });
    if (normalizedAgentResult?.contentValid && shouldDeferArtifactBackedTranscriptResult(transcriptResult, payload)) {
      return normalizedAgentResult;
    }
    if (transcriptResult?.contentValid) {
      return transcriptResult;
    }
    if (normalizedAgentResult?.contentValid) {
      return normalizedAgentResult;
    }
    const deferredAfterInvalidFollowup = deferredArtifactBackedTranscriptFallback(
      deferredTranscriptResult,
      payload,
      "recovered_from_deferred_transcript_result_after_invalid_followup"
    );
    if (transcriptResult?.text) {
      if (isProgrammerLike) {
        const partial = recoverPartialAgentResult(effectiveAgentId, startedAtMs, payload, transcriptPath);
        if (partial?.contentValid) {
          return {
            ...partial,
            text: partial.text || transcriptResult.text,
            content: {
              ...(partial.content || {}),
              recovered_from_non_json_transcript: true,
              recovered_error_message: `openclaw agent returned non-JSON content for ${role}`,
              raw_text: partial.content?.raw_text || transcriptResult.text,
            },
          };
        }
        if (deferredAfterInvalidFollowup) {
          return {
            ...deferredAfterInvalidFollowup,
            content: {
              ...(deferredAfterInvalidFollowup.content || {}),
              deferred_transcript_replaced_non_json_followup: true,
              deferred_transcript_replaced_invalid_partial_recovery: Boolean(partial),
              ...(partial?.content?.raw_text ? { raw_text: partial.content.raw_text } : {}),
            },
          };
        }
        if (partial) {
          return {
            ...partial,
            text: partial.text || transcriptResult.text,
            content: {
              ...(partial.content || {}),
              recovered_from_non_json_transcript: true,
              recovered_error_message: `openclaw agent returned non-JSON content for ${role}`,
              raw_text: partial.content?.raw_text || transcriptResult.text,
            },
          };
        }
        return {
          ...transcriptResult,
          content: {
            ...(transcriptResult.content || {}),
            recovered_from_non_json_transcript: true,
            recovered_error_message: `openclaw agent returned non-JSON content for ${role}`,
            ready_for_review: false,
          },
          contentValid: false,
        };
      }
      fail([
        `openclaw agent returned non-JSON content for ${role}`,
        describeTranscriptFailure(transcriptPath),
      ].filter(Boolean).join("\n"));

    }
    if (deferredAfterInvalidFollowup) {
      return {
        ...deferredAfterInvalidFollowup,
        content: {
          ...(deferredAfterInvalidFollowup.content || {}),
          recovered_from_deferred_transcript_result_after_agent_exit: true,
        },
      };
    }
    return normalizedAgentResult;
  } catch (error) {
    const message = String(error?.message || error || "");
    const recovered = readTranscriptAgentResult(
      transcriptPath,
      {
        recovered_after_error: true,
        recovered_error_message: message,
      },
      {
        allowInferredFallback: true,
        payload,
      }
    );
    if (recovered?.contentValid) {
      return recovered;
    }
    if (/ETIMEDOUT|timed out|timeout/i.test(message)) {
      const partial = recoverPartialAgentResult(effectiveAgentId, startedAtMs, payload, transcriptPath);
      if (partial) {
        return partial;
      }
    }
    const deferredAfterCatch = deferredArtifactBackedTranscriptFallback(
      deferredTranscriptResult,
      payload,
      "recovered_from_deferred_transcript_result_after_runagent_exception"
    );
    if (deferredAfterCatch) {
      return deferredAfterCatch;
    }
    if (isProgrammerLike) {
      const partial = recoverPartialAgentResult(effectiveAgentId, startedAtMs, payload, transcriptPath);
      if (partial?.contentValid) {
        return partial;
      }
    }
    const transcriptFailure = describeTranscriptFailure(transcriptPath);
    fail([
      `openclaw agent failed for ${role}: ${message}`,
      transcriptFailure,
      ].filter(Boolean).join("\n"));

  } finally {
    abortPendingAgent();
  }
}

async function main() {
  const role = process.argv[2];
  if (role === "validate-phase") {
    const validationResult = runValidatePhaseCli(process.argv.slice(3));
    writeJsonAndExitWithCode(validationResult.payload, validationResult.exitCode);
    return;
  }
  const payload = decodePayload(process.argv[3]);
  const prompt = buildPrompt(role, payload);
  const result = applyAgentResultSchemaValidation(role, payload, await runAgent(role, prompt, payload));

  writeJsonAndExit({
    role,
    ok: true,
    content_valid: result.contentValid,
    content: result.content,
    response_text: result.text,
    agent_meta: result.raw?.result?.meta?.agentMeta || result.raw?.meta?.agentMeta || null,
  });
}

if (require.main === module) {
  main().catch((error) => {
    fail(error?.message || String(error));
  });
} else {
  module.exports = {
    getGatewayCall,
    __testHooks: {
      collectTranscriptContext,
      readTranscriptAgentResult,
      normalizeProgrammerResult,
      scoreArtifactBundles,
      findBeamerArtifactBundle,
      findPptArtifactBundle,
      buildBeamerRecoveredContent,
      buildPptRecoveredContent,
      validateProgrammerContentSchema,
      validateProgrammerContentWithLocalPreflight,
      buildRecoveredRoadmapPage,
      buildRecoveredConclusionPreviewPage,
      buildRecoveredNotationCoverage,
      repairNotationCoverageAgainstVisibleSlides,
      symbolCandidatesFromNotationEntry,
      recoveredSlideIdsFromStructuredField,
      slideVisibleTextFromPlan,
      sanitizeRecoveredSlidesDocVisibleScaffold,
      sanitizeSlidesJsonArtifactForVisibleScaffold,
      materializeArtifactBackedProgrammerContentForValidation,
      resultIsArtifactBackedPhaseDiagnostic,
      shouldDeferArtifactBackedTranscriptResult,
      applyTesterSchemaValidation,
      testerMessageLooksLikeStaleBeamerArtifactComplaint,
      tableCoverageHasRealSlideIds,
      compactProgrammerOutputForPrompt,
      buildPrompt,
    },
  };
}
