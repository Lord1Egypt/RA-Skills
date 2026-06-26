#!/usr/bin/env node

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");

const VERSION = "0.6.3";
const DEFAULT_API_BASE_URL = "https://51yzt.cn/assetInnovate";
const CONFIG_DIR = path.join(os.homedir(), ".openclaw", "invoice-skill");
const CONFIG_FILE = path.join(CONFIG_DIR, "config.json");
const IDENTITY_FILE = path.join(CONFIG_DIR, "identity.json");
const LEGACY_CONFIG_FILE = path.join(os.homedir(), ".openclaw", "invoice-plugin", "config.json");
const IMAGE_MAX_BYTES = 2 * 1024 * 1024;
const SUPPORTED_FORMATS = new Set(["json", "base64", "base64+json", "both"]);
const SUPPORTED_IMAGE_EXTENSIONS = new Set([".png", ".jpg", ".jpeg"]);
const FOUR_ELEMENT_TEMPLATES = {
  checkCode: {
    fields: ["invoiceCode", "invoiceNumber", "billingDate", "checkCode"],
    description: "校验码后 6 位"
  },
  amount: {
    fields: ["invoiceCode", "invoiceNumber", "billingDate", "totalAmount"],
    description: "不含税金额"
  },
  taxAmount: {
    fields: ["invoiceCode", "invoiceNumber", "billingDate", "totalAmount"],
    description: "含税金额"
  }
};

function determineInvoiceFourElementRequirement(invoiceCode, invoiceNumber) {
  const sanitizedCode = String(invoiceCode || "").replace(/\D/g, "");
  const sanitizedNumber = String(invoiceNumber || "").replace(/\D/g, "");
  const fallback = {
    key: "checkCode",
    invoiceType: "未识别票种",
    description: FOUR_ELEMENT_TEMPLATES.checkCode.description
  };

  if (!sanitizedCode) {
    if (sanitizedNumber.length === 20) {
      return {
        key: "taxAmount",
        invoiceType: "二维码含税票",
        description: FOUR_ELEMENT_TEMPLATES.taxAmount.description
      };
    }
    return fallback;
  }

  if (sanitizedCode.length === 12) {
    const first = sanitizedCode[0];
    const tail = sanitizedCode.slice(-2);
    if (first === "1") {
      return {
        key: "amount",
        invoiceType: "机动车销售统一发票",
        description: FOUR_ELEMENT_TEMPLATES.amount.description
      };
    }
    if (first === "0") {
      if (tail === "17") {
        return {
          key: "amount",
          invoiceType: "二手车销售统一发票",
          description: "车价合计"
        };
      }
      if (["04", "05"].includes(tail)) {
        return {
          key: "checkCode",
          invoiceType: "增值税普通发票",
          description: FOUR_ELEMENT_TEMPLATES.checkCode.description
        };
      }
      if (["06", "07"].includes(tail)) {
        return {
          key: "checkCode",
          invoiceType: "增值税普通发票（卷式）",
          description: FOUR_ELEMENT_TEMPLATES.checkCode.description
        };
      }
      if (tail === "11") {
        return {
          key: "checkCode",
          invoiceType: "增值税电子普通发票",
          description: FOUR_ELEMENT_TEMPLATES.checkCode.description
        };
      }
      if (tail === "12") {
        return {
          key: "checkCode",
          invoiceType: "增值税电子普通发票（通行费）",
          description: FOUR_ELEMENT_TEMPLATES.checkCode.description
        };
      }
    }
  }

  if (sanitizedCode.length === 10) {
    const eighth = sanitizedCode[7];
    if (["1", "5"].includes(eighth)) {
      return {
        key: "amount",
        invoiceType: "增值税专用发票",
        description: FOUR_ELEMENT_TEMPLATES.amount.description
      };
    }
    if (["2", "7"].includes(eighth)) {
      return {
        key: "amount",
        invoiceType: "货运运输业增值税专用发票",
        description: FOUR_ELEMENT_TEMPLATES.amount.description
      };
    }
    if (["3", "6"].includes(eighth)) {
      return {
        key: "checkCode",
        invoiceType: "增值税普通发票",
        description: FOUR_ELEMENT_TEMPLATES.checkCode.description
      };
    }
  }

  return fallback;
}

function printJson(payload, exitCode = 0) {
  console.log(JSON.stringify(payload, null, 2));
  process.exitCode = exitCode;
}

function fail(message, extra = {}, exitCode = 1) {
  printJson(
    {
      ok: false,
      error: {
        message,
        ...extra
      }
    },
    exitCode
  );
}

function readJsonFile(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return {};
  }
}

function readConfig() {
  const legacy = readJsonFile(LEGACY_CONFIG_FILE);
  const current = readJsonFile(CONFIG_FILE);
  return {
    ...legacy,
    ...current
  };
}

function readIdentity() {
  const identity = readJsonFile(IDENTITY_FILE);
  return {
    clientInstanceId: identity.clientInstanceId ? String(identity.clientInstanceId) : "",
    deviceFingerprint: identity.deviceFingerprint ? String(identity.deviceFingerprint) : ""
  };
}

function writeIdentity(next) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(
    IDENTITY_FILE,
    JSON.stringify(
      {
        clientInstanceId: String(next.clientInstanceId || ""),
        deviceFingerprint: String(next.deviceFingerprint || "")
      },
      null,
      2
    ),
    "utf8"
  );
}

function writeConfig(next) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(next, null, 2), "utf8");
}

function clearStoredAppKey() {
  const current = readConfig();
  const next = { ...current };
  delete next.appKey;
  writeConfig(next);
  return next;
}

function getApiBaseUrl(config, override) {
  return override || config.apiBaseUrl || process.env.INVOICE_API_BASE_URL || DEFAULT_API_BASE_URL;
}

function randomId(prefix) {
  return `${prefix}${crypto.randomUUID().replace(/-/g, "")}`;
}

function stableHash(prefix, payload) {
  const digest = crypto.createHash("sha256").update(String(payload || ""), "utf8").digest("hex");
  return `${prefix}${digest.slice(0, 32)}`;
}

function createRandomScopedId(prefix) {
  return `${prefix}${crypto.randomUUID().replace(/-/g, "")}`;
}

function deriveStableClientInstanceId(deviceFingerprint) {
  if (!deviceFingerprint) {
    return createRandomScopedId("client_");
  }
  return stableHash("client_", `invoice-skill||${String(deviceFingerprint)}`);
}

function ensurePersistentIds(config, options = {}) {
  const identity = readIdentity();
  const resolvedDeviceFingerprint =
    options.deviceFingerprint ||
    config.deviceFingerprint ||
    identity.deviceFingerprint ||
    process.env.OPENCLAW_DEVICE_FINGERPRINT ||
    createRandomScopedId("device_");
  const resolvedClientInstanceId =
    options.clientInstanceId ||
    config.clientInstanceId ||
    identity.clientInstanceId ||
    process.env.OPENCLAW_CLIENT_INSTANCE_ID ||
    deriveStableClientInstanceId(resolvedDeviceFingerprint);
  writeIdentity({
    clientInstanceId: resolvedClientInstanceId,
    deviceFingerprint: resolvedDeviceFingerprint
  });
  return {
    clientInstanceId: resolvedClientInstanceId,
    deviceFingerprint: resolvedDeviceFingerprint
  };
}

function buildHeaders(appKey, requestId) {
  const headers = {
    "Content-Type": "application/json"
  };
  if (requestId) {
    headers["X-Request-Id"] = requestId;
  }
  if (appKey) {
    headers.Authorization = `Bearer ${appKey}`;
  }
  return headers;
}

async function callApi(baseUrl, method, endpoint, body, appKey, requestId) {
  let response;
  try {
    response = await fetch(`${baseUrl}${endpoint}`, {
      method,
      headers: buildHeaders(appKey, requestId),
      body: body ? JSON.stringify(body) : undefined
    });
  } catch (error) {
    const detail =
      error && error.cause && error.cause.message ? error.cause.message : error.message;
    const wrapped = new Error(`request to ${baseUrl}${endpoint} failed: ${detail}`);
    wrapped.code = error && error.code ? error.code : "";
    throw wrapped;
  }

  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }

  if (!response.ok) {
    const message =
      (data && (data.message || data.msg || data.error)) || `HTTP ${response.status}`;
    const error = new Error(message);
    error.code = data && data.code ? String(data.code) : "";
    error.status = response.status;
    error.response = data;
    throw error;
  }

  return data;
}

function isInvalidAppKeyError(error) {
  const code = String(error && error.code ? error.code : "").toUpperCase();
  const message = String(error && error.message ? error.message : "").toLowerCase();
  return code === "INVALID_KEY" || message.includes("invalid key");
}

function isExpiredAppKeyError(error) {
  const code = String(error && error.code ? error.code : "").toUpperCase();
  const message = String(error && error.message ? error.message : "").toLowerCase();
  return code === "KEY_EXPIRED" || message.includes("key expired") || message.includes("过期");
}

async function initKey(options = {}) {
  const config = readConfig();
  const apiBaseUrl = getApiBaseUrl(config, options.apiBaseUrl);
  const ids = ensurePersistentIds(config, options);
  const clientInstanceId = options.rotateClientInstanceId ? randomId("client_") : ids.clientInstanceId;
  const deviceFingerprint = ids.deviceFingerprint;

  const response = await callApi(
    apiBaseUrl,
    "POST",
    "/api/v4/plugin/key/init",
    {
      clientInstanceId,
      deviceFingerprint,
      clientVersion: VERSION
    },
    null
  );

  const data = (response && response.data) || {};
  const appKey = data.key || response.key || "";
  const next = {
    ...config,
    apiBaseUrl,
    clientInstanceId,
    deviceFingerprint,
    cipherKey: data.cipherKey || config.cipherKey || null
  };
  if (appKey) {
    next.appKey = appKey;
  }
  writeConfig(next);

  return {
    ...next,
    autoBound: Boolean(appKey),
    initResponse: response
  };
}

async function withBoundConfig(handler, options = {}) {
  let bound = readConfig();
  bound.apiBaseUrl = getApiBaseUrl(bound, options.apiBaseUrl);

  if (!bound.appKey) {
    bound = await initKey(options);
  }

  try {
    return await handler(bound);
  } catch (error) {
    if (isExpiredAppKeyError(error)) {
      throw error;
    }
    if (!isInvalidAppKeyError(error)) {
      throw error;
    }

    const rebound = await initKey(options);
    if (!rebound.appKey) {
      const message = "key init succeeded but backend did not return a usable key";
      const wrapped = new Error(message);
      wrapped.code = "KEY_REINIT_NO_KEY";
      wrapped.status = error && error.status ? error.status : null;
      throw wrapped;
    }
    return handler(rebound);
  }
}

function toHalfWidth(text) {
  return String(text || "")
    .replace(/\u3000/g, " ")
    .replace(/[\uff01-\uff5e]/g, (char) => String.fromCharCode(char.charCodeAt(0) - 0xfee0));
}

function pad2(value) {
  return String(value).padStart(2, "0");
}

function normalizeDate(year, month, day) {
  return `${year}-${pad2(month)}-${pad2(day)}`;
}

function normalizeInvoiceText(text) {
  return toHalfWidth(text)
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/[\uFF0C\uFF1B]/g, ",")
    .replace(/[\uFF1A]/g, ":")
    .replace(/[\uFF08]/g, "(")
    .replace(/[\uFF09]/g, ")")
    .replace(/(\d{4})\s*\u5E74\s*(\d{1,2})\s*\u6708\s*(\d{1,2})\s*\u65E5?/g, (_, year, month, day) =>
      normalizeDate(year, month, day)
    )
    .replace(/(\d{4})[/.](\d{1,2})[/.](\d{1,2})/g, (_, year, month, day) =>
      normalizeDate(year, month, day)
    )
    .replace(/\n+/g, "\n")
    .replace(/[ \t]+/g, " ")
    .trim();
}


function escapeRegex(text) {
  return String(text || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function extractLabeledValue(text, labels, valuePattern) {
  for (const label of labels) {
    const pattern = new RegExp(
      `${escapeRegex(label)}\\s*(?:[:\uFF1A]|\u662F|\u4E3A|=)?\\s*["']?(${valuePattern})["']?`,
      "i"
    );
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  return "";
}

function extractLabeledValues(text, labels, valuePattern) {
  const results = [];
  for (const label of labels) {
    const pattern = new RegExp(
      `${escapeRegex(label)}\\s*(?:[:\uFF1A]|\u662F|\u4E3A|=)?\\s*["']?(${valuePattern})["']?`,
      "ig"
    );
    let match;
    while ((match = pattern.exec(text)) !== null) {
      if (match[1] && match[1].trim()) {
        results.push(match[1].trim());
      }
    }
  }
  return [...new Set(results)];
}

function uniqueMatches(text, pattern) {
  return [...new Set(String(text || "").match(pattern) || [])];
}

function normalizeBillingDateValue(value) {
  const raw = String(value || "").trim();
  if (!raw) return "";
  const match = raw.match(/^(\d{4})[-/.]?(\d{2})[-/.]?(\d{2})$/);
  if (!match) return "";
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (year < 1900 || year > 2200) return "";
  if (month < 1 || month > 12) return "";
  if (day < 1 || day > 31) return "";
  return `${match[1]}-${match[2]}-${match[3]}`;
}

function cleanupAmount(value) {
  const raw = String(value || "").replace(/,/g, "");
  const match = raw.match(/\d+(?:\.\d{1,2})?/);
  return match ? match[0] : "";
}

function parseAmountNumber(value) {
  const cleaned = cleanupAmount(value);
  if (!cleaned) return null;
  const numeric = Number(cleaned);
  if (!Number.isFinite(numeric)) return null;
  return {
    numeric,
    cleaned
  };
}

function pickMaxAmount(values) {
  const list = Array.isArray(values) ? values : [values];
  let bestNumeric = Number.NEGATIVE_INFINITY;
  let bestCleaned = "";
  for (const item of list) {
    const parsed = parseAmountNumber(item);
    if (!parsed) continue;
    if (parsed.numeric > bestNumeric) {
      bestNumeric = parsed.numeric;
      bestCleaned = parsed.cleaned;
    }
  }
  return bestCleaned;
}

function normalizeInvoiceCodeCandidate(value) {
  const normalized = String(value || "").replace(/\D/g, "");
  if (normalized.length === 10 || normalized.length === 12) {
    return normalized;
  }
  return "";
}

function scoreInvoiceCodeCandidate(value) {
  let score = 0;
  if (value.length === 12) score += 4;
  if (value.length === 10) score += 3;
  if (value.startsWith("0") || value.startsWith("1")) score += 1;
  if (["04", "05", "06", "07", "11", "12", "17"].includes(value.slice(-2))) score += 1;
  return score;
}

function pickBestInvoiceCode(values) {
  const list = Array.isArray(values) ? values : [values];
  let best = "";
  let bestScore = Number.NEGATIVE_INFINITY;
  for (const item of list) {
    const normalized = normalizeInvoiceCodeCandidate(item);
    if (!normalized) continue;
    const score = scoreInvoiceCodeCandidate(normalized);
    if (score > bestScore) {
      best = normalized;
      bestScore = score;
    }
  }
  return best;
}

function normalizeInvoiceNumberCandidate(value) {
  const normalized = String(value || "").replace(/\D/g, "");
  if (normalized.length >= 8 && normalized.length <= 20) {
    return normalized;
  }
  return "";
}

function scoreInvoiceNumberCandidate(value, invoiceCode) {
  if (!value) return Number.NEGATIVE_INFINITY;
  if (invoiceCode && value === invoiceCode) return Number.NEGATIVE_INFINITY;
  let score = 0;
  if (value.length === 8 || value.length === 20) score += 4;
  if (value.length >= 8 && value.length <= 12) score += 2;
  if (/^\d+$/.test(value)) score += 1;
  if (/^20\d{6}$/.test(value)) score -= 2;
  return score;
}

function pickBestInvoiceNumber(values, invoiceCode) {
  const list = Array.isArray(values) ? values : [values];
  let best = "";
  let bestScore = Number.NEGATIVE_INFINITY;
  for (const item of list) {
    const normalized = normalizeInvoiceNumberCandidate(item);
    if (!normalized) continue;
    const score = scoreInvoiceNumberCandidate(normalized, invoiceCode);
    if (score > bestScore) {
      best = normalized;
      bestScore = score;
    }
  }
  return best;
}

function extractInvoiceFields(text) {
  const normalizedText = normalizeInvoiceText(text);
  const amountPattern = "[¥￥]?\\s*\\d{1,3}(?:,\\d{3})*(?:\\.\\d{1,2})?|[¥￥]?\\s*\\d+(?:\\.\\d{1,2})?";
  const invoiceCodeLabels = [
    "\u53d1\u7968\u4ee3\u7801",
    "\u7968\u636e\u4ee3\u7801",
    "\u4ee3\u7801",
    "invoice code",
    "invoicecode"
  ];
  const invoiceNumberLabels = [
    "\u53d1\u7968\u53f7\u7801",
    "\u53d1\u7968\u53f7",
    "\u7968\u53f7",
    "\u53f7\u7801",
    "\u7968\u636e\u53f7\u7801",
    "invoice number",
    "invoicenumber"
  ];
  const billingDateLabels = [
    "\u5f00\u7968\u65e5\u671f",
    "\u5f00\u7968\u65f6\u95f4",
    "\u65e5\u671f",
    "\u7968\u636e\u65e5\u671f",
    "invoice date",
    "billing date"
  ];
  const checkCodeLabels = [
    "\u6821\u9a8c\u7801",
    "\u6821\u9a8c\u7801\u540e6\u4f4d",
    "\u6821\u9a8c\u7801\u540e 6 \u4f4d",
    "check code",
    "checkcode"
  ];
  const taxAmountLabels = [
    "\u542b\u7a0e\u91d1\u989d",
    "\u4ef7\u7a0e\u5408\u8ba1",
    "\u4ef7\u7a0e\u5408\u8ba1(\u5c0f\u5199)",
    "\u5c0f\u5199\u91d1\u989d",
    "\u542b\u7a0e\u603b\u91d1\u989d"
  ];
  const amountLabels = [
    "\u4e0d\u542b\u7a0e\u91d1\u989d",
    "\u91d1\u989d",
    "\u5408\u8ba1",
    "\u4ef7\u7a0e\u5408\u8ba1",
    "\u4ef7\u7a0e\u5408\u8ba1(\u5c0f\u5199)",
    "\u5c0f\u5199\u91d1\u989d",
    "invoice amount",
    "total amount"
  ];

  const rawCheckCodeCandidates = extractLabeledValues(normalizedText, checkCodeLabels, "[A-Za-z0-9]{6,20}");
  const rawCheckCode = rawCheckCodeCandidates[0] || "";
  const taxAmount = pickMaxAmount(extractLabeledValues(normalizedText, taxAmountLabels, amountPattern));
  const labeledAmount = pickMaxAmount(extractLabeledValues(normalizedText, amountLabels, amountPattern));
  const detectedAmounts = uniqueMatches(normalizedText, /(?:¥|￥)?\s*\d{1,3}(?:,\d{3})*(?:\.\d{1,2})|(?:¥|￥)?\s*\d+(?:\.\d{1,2})/g);
  const detectedMaxAmount = pickMaxAmount(detectedAmounts);
  const resolvedTotalAmount = pickMaxAmount([labeledAmount, taxAmount, detectedMaxAmount]);
  const invoiceCodeCandidates = [
    ...extractLabeledValues(normalizedText, invoiceCodeLabels, "[A-Za-z0-9]{10,12}"),
    ...uniqueMatches(normalizedText, /\b\d{10,12}\b/g)
  ];
  const resolvedInvoiceCode = pickBestInvoiceCode(invoiceCodeCandidates);
  const invoiceNumberCandidates = [
    ...extractLabeledValues(normalizedText, invoiceNumberLabels, "[A-Za-z0-9]{8,20}"),
    ...uniqueMatches(normalizedText, /\b\d{8,20}\b/g)
  ].filter((item) => String(item || "").replace(/\D/g, "") !== resolvedInvoiceCode);
  const resolvedInvoiceNumber = pickBestInvoiceNumber(invoiceNumberCandidates, resolvedInvoiceCode);
  const labeledDate = normalizeBillingDateValue(
    extractLabeledValue(normalizedText, billingDateLabels, "(?:\\d{4}-\\d{2}-\\d{2}|\\d{8})")
  );
  const fallbackDate = uniqueMatches(normalizedText, /\b\d{4}-\d{2}-\d{2}\b/g)[0] || "";
  const fields = {
    invoiceCode: resolvedInvoiceCode,
    invoiceNumber: resolvedInvoiceNumber,
    billingDate: labeledDate || fallbackDate,
    taxAmount,
    totalAmount: resolvedTotalAmount,
    checkCodeRaw: rawCheckCode,
    checkCode: rawCheckCode ? rawCheckCode.slice(-6) : ""
  };

  if (!fields.invoiceCode) {
    fields.invoiceCode = pickBestInvoiceCode(uniqueMatches(normalizedText, /\b\d{10,12}\b/g));
  }
  if (!fields.invoiceNumber) {
    const values = uniqueMatches(normalizedText, /\b\d{8,20}\b/g).filter(
      (item) => item !== fields.invoiceCode
    );
    fields.invoiceNumber = pickBestInvoiceNumber(values, fields.invoiceCode);
  }
  if (!fields.billingDate) {
    const candidate = uniqueMatches(normalizedText, /\b\d{4}-\d{2}-\d{2}\b/g)[0] || "";
    fields.billingDate = normalizeBillingDateValue(candidate) || candidate;
  }
  if (!fields.totalAmount) {
    const amounts = uniqueMatches(normalizedText, /\b\d+(?:\.\d{1,2})\b/g).filter(
      (item) => item !== fields.invoiceCode && item !== fields.invoiceNumber
    );
    fields.totalAmount = pickMaxAmount(amounts);
  }
  if (!fields.checkCode) {
    fields.checkCode = uniqueMatches(normalizedText, /\b[A-Za-z0-9]{6}\b/g)[0] || "";
  }
  fields.taxAmount = pickMaxAmount([fields.taxAmount, fields.totalAmount]) || fields.totalAmount;

  const requirement = determineInvoiceFourElementRequirement(fields.invoiceCode, fields.invoiceNumber);
  const template = FOUR_ELEMENT_TEMPLATES[requirement.key] || FOUR_ELEMENT_TEMPLATES.checkCode;
  fields.invoiceType = requirement.invoiceType;
  fields.fourElementKey = requirement.key;
  fields.fourElementDescription = requirement.description || template.description;
  fields.requiredFourElementFields = template.fields;

  return {
    normalizedText,
    fields
  };
}

function normalizeResponseFormat(value) {
  const format = String(value || "json").toLowerCase();
  if (!SUPPORTED_FORMATS.has(format)) {
    throw new Error("format must be one of: json, base64, base64+json, both");
  }
  return format === "both" ? "base64+json" : format;
}

function maskAppKey(appKey) {
  if (!appKey) return null;
  if (appKey.length < 12) return appKey;
  return `${appKey.slice(0, 8)}****${appKey.slice(-4)}`;
}

function buildQrCodeEntries(orderData) {
  const entries = [];
  const pushEntry = (label, url) => {
    if (!url) return;
    entries.push({ channel: label, url });
  };

  pushEntry("微信支付", orderData.wechatPayQrCodeUrl || orderData.wechatPayQrCodeImageUrl);
  pushEntry("支付宝支付", orderData.alipayPayQrCodeUrl || orderData.alipayPayQrCodeImageUrl);
  pushEntry("支付二维码", orderData.payQrCodeUrl || orderData.qrCodeImageUrl);

  if (orderData.payQrCode && typeof orderData.payQrCode === "string") {
    const trimmed = orderData.payQrCode.trim();
    if (trimmed.startsWith("data:image/")) {
      pushEntry("支付二维码", trimmed);
    } else {
      // assume base64 payload without prefix
      pushEntry("支付二维码", `data:image/png;base64,${trimmed}`);
    }
  }

  return entries;
}

function parseArgs(argv) {
  const positionals = [];
  const options = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      positionals.push(token);
      continue;
    }

    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      options[key] = true;
      continue;
    }

    options[key] = next;
    index += 1;
  }

  return { positionals, options };
}

function requireOption(options, key, message) {
  const value = options[key];
  if (value === undefined || value === null || value === "") {
    throw new Error(message);
  }
  return value;
}

function parseIntegerOption(options, key, message) {
  const raw = requireOption(options, key, message);
  const value = Number(raw);
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(message);
  }
  return value;
}

function parseNonNegativeIntegerOption(value, message, defaultValue) {
  if (value === undefined || value === null || value === "") {
    return defaultValue;
  }
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < 0) {
    throw new Error(message);
  }
  return parsed;
}

function parseBooleanOption(value, defaultValue = false) {
  if (value === undefined || value === null || value === "") {
    return defaultValue;
  }
  if (typeof value === "boolean") {
    return value;
  }
  const normalized = String(value).trim().toLowerCase();
  if (["true", "1", "yes", "y"].includes(normalized)) {
    return true;
  }
  if (["false", "0", "no", "n"].includes(normalized)) {
    return false;
  }
  throw new Error("boolean option must be one of: true, false, yes, no, 1, 0");
}

function formatTimestampForFileName(date = new Date()) {
  const year = String(date.getFullYear());
  const month = pad2(date.getMonth() + 1);
  const day = pad2(date.getDate());
  const hour = pad2(date.getHours());
  const minute = pad2(date.getMinutes());
  const second = pad2(date.getSeconds());
  return `${year}${month}${day}-${hour}${minute}${second}`;
}

function sanitizeFileName(value) {
  return String(value || "")
    .replace(/[<>:"/\\|?*\u0000-\u001F]/g, "_")
    .replace(/\s+/g, "_");
}

function ensureDirectoryExists(dirPath, message) {
  const resolved = path.resolve(String(dirPath || ""));
  if (!fs.existsSync(resolved)) {
    throw new Error(message || `directory not found: ${resolved}`);
  }
  if (!fs.statSync(resolved).isDirectory()) {
    throw new Error(`path is not a directory: ${resolved}`);
  }
  return resolved;
}

function isSupportedImageFile(filePath) {
  return SUPPORTED_IMAGE_EXTENSIONS.has(path.extname(filePath).toLowerCase());
}

function listImageFiles(dirPath, recursive = false) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });
  const sortedEntries = entries.sort((left, right) => left.name.localeCompare(right.name, "en"));
  const files = [];

  for (const entry of sortedEntries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      if (recursive) {
        files.push(...listImageFiles(fullPath, true));
      }
      continue;
    }
    if (entry.isFile() && isSupportedImageFile(fullPath)) {
      files.push(fullPath);
    }
  }

  return files;
}

function writeJsonFile(filePath, payload) {
  fs.writeFileSync(filePath, JSON.stringify(payload, null, 2), "utf8");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeErrorPayload(error) {
  return {
    message: error && error.message ? error.message : String(error),
    code: error && error.code ? String(error.code) : "",
    status: error && error.status ? error.status : null,
    response: error && error.response ? error.response : null
  };
}

function resolveBatchTextForImage(options, imagePath) {
  const inlineText = String(options.text || "").trim();
  if (inlineText) {
    return {
      text: inlineText,
      sidecarTextPath: null
    };
  }

  if (!imagePath) {
    return {
      text: "",
      sidecarTextPath: null
    };
  }

  const useSidecarText = parseBooleanOption(options["use-sidecar-text"], true);
  if (!useSidecarText) {
    return {
      text: "",
      sidecarTextPath: null
    };
  }

  const parsed = path.parse(imagePath);
  const sidecarPath = path.join(parsed.dir, `${parsed.name}.txt`);
  if (!fs.existsSync(sidecarPath) || !fs.statSync(sidecarPath).isFile()) {
    return {
      text: "",
      sidecarTextPath: null
    };
  }
  return {
    text: fs.readFileSync(sidecarPath, "utf8").trim(),
    sidecarTextPath: sidecarPath
  };
}

function getMimeTypeFromPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".png") return "image/png";
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  throw new Error("only .png, .jpg, and .jpeg are supported for image verification");
}

function stripDataUrlPrefix(value) {
  const text = String(value || "").trim();
  const match = text.match(/^data:(image\/[a-zA-Z0-9.+-]+);base64,(.+)$/s);
  if (match) {
    return {
      mimeType: match[1].toLowerCase(),
      base64: match[2]
    };
  }
  return {
    mimeType: "",
    base64: text
  };
}

function sanitizeBase64(value) {
  return String(value || "").replace(/\s+/g, "");
}

function estimateBase64Bytes(base64) {
  const clean = sanitizeBase64(base64);
  if (!clean) return 0;
  const padding = clean.endsWith("==") ? 2 : clean.endsWith("=") ? 1 : 0;
  return Math.floor((clean.length * 3) / 4) - padding;
}

function readImageInput(options) {
  const fromFile = (sourcePath, sourceLabel = "file") => {
    const filePath = path.resolve(String(sourcePath));
    if (!fs.existsSync(filePath)) {
      throw new Error(`image file not found: ${filePath}`);
    }
    if (!fs.statSync(filePath).isFile()) {
      throw new Error(`image path is not a file: ${filePath}`);
    }
    const mimeType = options["mime-type"] || getMimeTypeFromPath(filePath);
    const buffer = fs.readFileSync(filePath);
    return {
      imageSource: sourceLabel,
      imagePath: filePath,
      mimeType,
      base64: buffer.toString("base64")
    };
  };

  const fromBase64 = (rawBase64, sourceLabel = "base64") => {
    const parsed = stripDataUrlPrefix(rawBase64);
    return {
      imageSource: sourceLabel,
      mimeType: String(options["mime-type"] || parsed.mimeType || "image/png").toLowerCase(),
      base64: sanitizeBase64(parsed.base64)
    };
  };

  if (options["image-file"]) {
    return fromFile(options["image-file"], "file");
  }

  if (options["image-base64"]) {
    return fromBase64(options["image-base64"], "base64");
  }

  if (options.image) {
    const maybePath = path.resolve(String(options.image));
    if (fs.existsSync(maybePath) && fs.statSync(maybePath).isFile()) {
      return fromFile(maybePath, "image");
    }
    return fromBase64(options.image, "image");
  }

  if (options.content) {
    return fromBase64(options.content, "content");
  }

  throw new Error("verify-image requires --image-file, --image-base64, or --image <path|base64|data-url>");
}

function validateImagePayload(image) {
  if (!["image/png", "image/jpeg"].includes(image.mimeType)) {
    throw new Error("mime type must be image/png or image/jpeg");
  }
  if (!image.base64) {
    throw new Error("image content is empty");
  }
  const sizeBytes = estimateBase64Bytes(image.base64);
  if (sizeBytes > IMAGE_MAX_BYTES) {
    throw new Error("image must be 2MB or smaller");
  }
  return {
    ...image,
    sizeBytes
  };
}

async function verifyImageFile(bound, imageFilePath, options) {
  const image = validateImagePayload(readImageInput({ "image-file": imageFilePath }));
  const textInput = resolveBatchTextForImage(options, imageFilePath);
  const text = textInput.text;
  const payload = buildVerifyPayload({ ...options, text }, "image", image.base64);
  const requestId = crypto.randomUUID();

  try {
    const response = await callApi(
      bound.apiBaseUrl,
      "POST",
      "/api/v4/plugin/verify",
      payload.requestBody,
      bound.appKey,
      requestId
    );
    const businessOk = !(response && response.success === false);
    return {
      ok: businessOk,
      verifiedAt: new Date().toISOString(),
      requestId,
      sourceFile: imageFilePath,
      response: response,
      error: businessOk
        ? null
        : {
            message: response && response.message ? response.message : "verification failed",
            code: response && response.code ? String(response.code) : "",
            status: null,
            response: response
          },
      meta: {
        apiBaseUrl: bound.apiBaseUrl,
        mimeType: image.mimeType,
        sizeBytes: image.sizeBytes,
        costQuota: 2,
        quotaNotice: "Image verification costs 2 quota per request.",
        textSupplementUsed: Boolean(text),
        sidecarTextPath: textInput.sidecarTextPath,
        transportOk: true,
        businessOk,
        extractedFields: payload.extracted.fields
      }
    };
  } catch (error) {
    if (isInvalidAppKeyError(error) || isExpiredAppKeyError(error)) {
      throw error;
    }
    return {
      ok: false,
      verifiedAt: new Date().toISOString(),
      requestId,
      sourceFile: imageFilePath,
      error: normalizeErrorPayload(error),
      meta: {
        apiBaseUrl: bound.apiBaseUrl,
        mimeType: image.mimeType,
        sizeBytes: image.sizeBytes,
        costQuota: 2,
        quotaNotice: "Image verification costs 2 quota per request.",
        textSupplementUsed: Boolean(text),
        sidecarTextPath: textInput.sidecarTextPath,
        transportOk: false,
        businessOk: false,
        extractedFields: payload.extracted.fields
      }
    };
  }
}

function buildVerifyPayload(options, inputType, content) {
  const rawText = String(options.text || "").trim();
  const defaultFields = {
    invoiceCode: "",
    invoiceNumber: "",
    billingDate: "",
    totalAmount: "",
    taxAmount: "",
    checkCode: "",
    checkCodeRaw: "",
    fourElementKey: "checkCode",
    invoiceType: "未识别票种",
    fourElementDescription: FOUR_ELEMENT_TEMPLATES.checkCode.description,
    requiredFourElementFields: FOUR_ELEMENT_TEMPLATES.checkCode.fields
  };
  const extracted = rawText
    ? extractInvoiceFields(rawText)
    : { normalizedText: "", fields: defaultFields };
  const amountValue =
    extracted.fields.fourElementKey === "taxAmount"
      ? pickMaxAmount([extracted.fields.taxAmount, extracted.fields.totalAmount]) || extracted.fields.taxAmount
      : extracted.fields.totalAmount;

  return {
    requestBody: {
      inputType,
      content,
      responseFormat: normalizeResponseFormat(options.format),
      invoiceCode: extracted.fields.invoiceCode,
      invoiceNumber: extracted.fields.invoiceNumber,
      billingDate: extracted.fields.billingDate,
      totalAmount: amountValue,
      checkCode: extracted.fields.checkCode
    },
    extracted
  };
}

function extractOrderData(response) {
  return response && response.data ? response.data : {};
}

function extractOrderStatus(response) {
  const data = extractOrderData(response);
  return String(
    data.orderStatus ||
      data.status ||
      response.orderStatus ||
      response.status ||
      ""
  )
    .trim()
    .toLowerCase();
}

function isOrderFinalStatus(status) {
  return ["credited", "paid", "success", "completed", "finished", "closed", "failed", "cancelled"].includes(status);
}

function isOrderCreditedStatus(status) {
  return ["credited", "paid", "success", "completed", "finished"].includes(status);
}

async function pollOrderUntilFinal(bound, orderNo, waitSeconds, pollIntervalSeconds) {
  const maxWaitSeconds = Math.max(0, Number(waitSeconds) || 0);
  const intervalSeconds = Math.max(1, Number(pollIntervalSeconds) || 1);
  const startedAt = Date.now();
  let elapsedSeconds = 0;
  let polls = 0;
  let finalStatus = "";
  let finalResponse = null;

  while (true) {
    polls += 1;
    finalResponse = await callApi(
      bound.apiBaseUrl,
      "GET",
      `/api/v4/plugin/orders/${encodeURIComponent(orderNo)}`,
      null,
      bound.appKey
    );
    finalStatus = extractOrderStatus(finalResponse);

    if (isOrderFinalStatus(finalStatus)) {
      break;
    }

    elapsedSeconds = Math.floor((Date.now() - startedAt) / 1000);
    if (elapsedSeconds >= maxWaitSeconds) {
      break;
    }

    const remainingSeconds = maxWaitSeconds - elapsedSeconds;
    const sleepSeconds = Math.max(1, Math.min(intervalSeconds, remainingSeconds));
    await sleep(sleepSeconds * 1000);
  }

  elapsedSeconds = Math.floor((Date.now() - startedAt) / 1000);
  const settled = isOrderCreditedStatus(finalStatus);
  return {
    orderNo,
    finalStatus,
    settled,
    polls,
    waitedSeconds: elapsedSeconds,
    maxWaitSeconds,
    pollIntervalSeconds: intervalSeconds,
    orderQuery: finalResponse
  };
}

async function runAction(action, options) {
  const apiBaseUrl = options["api-base-url"];

  if (action === "help") {
    return {
      ok: true,
      action,
        data: {
          commands: [
          "config show",
          "config set --api-base-url <url>",
          "config set --app-key <key>",
          "config clear-app-key",
          "init-key",
          "packages",
          "quota",
          "ledger [--page 1 --page-size 20]",
          "verify --text <invoice text> [--format json|base64|base64+json|both]",
          "verify-image --image-file <path> [--text <invoice text>] [--format json|base64|base64+json|both]",
          "verify-image --image-base64 <base64|data-url> [--mime-type image/png|image/jpeg] [--text <invoice text>]",
          "verify-image --image <path|base64|data-url> [--mime-type image/png|image/jpeg] [--text <invoice text>]",
          "verify-directory --dir <folder> [--recursive true] [--format json|base64|base64+json|both]",
          "create-order --amount <yuan> [--agree-terms true] [--wait-seconds 45] [--poll-interval-seconds 3]",
          "query-order --order-no <orderNo>"
        ]
      }
    };
  }

  if (action === "config") {
    const configAction = options._subaction || "show";
    const current = readConfig();

    if (configAction === "show") {
      return {
        ok: true,
        action,
        data: {
          configFile: CONFIG_FILE,
          legacyConfigFile: LEGACY_CONFIG_FILE,
          apiBaseUrl: getApiBaseUrl(current),
          appKeyMasked: maskAppKey(current.appKey),
          clientInstanceId: current.clientInstanceId || null,
          deviceFingerprint: current.deviceFingerprint || null,
          cipherKey: current.cipherKey || null
        }
      };
    }

    if (configAction === "set") {
      const next = { ...current };
      if (options["api-base-url"]) next.apiBaseUrl = String(options["api-base-url"]);
      if (options["app-key"]) next.appKey = String(options["app-key"]);
      if (options["client-instance-id"]) next.clientInstanceId = String(options["client-instance-id"]);
      if (options["device-fingerprint"]) next.deviceFingerprint = String(options["device-fingerprint"]);
      writeConfig(next);
      return {
        ok: true,
        action,
        data: {
          configFile: CONFIG_FILE,
          apiBaseUrl: getApiBaseUrl(next),
          appKeyMasked: maskAppKey(next.appKey),
          clientInstanceId: next.clientInstanceId || null,
          deviceFingerprint: next.deviceFingerprint || null
        }
      };
    }

    if (configAction === "clear-app-key") {
      const next = clearStoredAppKey();
      return {
        ok: true,
        action,
        data: {
          configFile: CONFIG_FILE,
          apiBaseUrl: getApiBaseUrl(next),
          appKeyMasked: null,
          clientInstanceId: next.clientInstanceId || null,
          deviceFingerprint: next.deviceFingerprint || null
        }
      };
    }

    throw new Error("config subcommand must be show, set, or clear-app-key");
  }

  if (action === "init-key") {
    const result = await initKey({
      apiBaseUrl,
      clientInstanceId: options["client-instance-id"],
      deviceFingerprint: options["device-fingerprint"],
      rotateClientInstanceId: Boolean(options["rotate-client-instance-id"])
    });
    return {
      ok: true,
      action,
      data: result.initResponse,
      meta: {
        apiBaseUrl: result.apiBaseUrl,
        appKeyMasked: maskAppKey(result.appKey),
        clientInstanceId: result.clientInstanceId,
        deviceFingerprint: result.deviceFingerprint
      }
    };
  }

  return withBoundConfig(async (bound) => {
    if (action === "quota") {
      const response = await callApi(bound.apiBaseUrl, "GET", "/api/v4/plugin/quota", null, bound.appKey);
      return {
        ok: true,
        action,
        data: response,
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl
        }
      };
    }

    if (action === "packages") {
      const response = await callApi(bound.apiBaseUrl, "GET", "/api/v4/plugin/packages", null, bound.appKey);
      return {
        ok: true,
        action,
        data: response,
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl
        }
      };
    }

    if (action === "ledger") {
      const page = Number(options.page || 1);
      const pageSize = Number(options["page-size"] || 20);
      const response = await callApi(
        bound.apiBaseUrl,
        "GET",
        `/api/v4/plugin/ledger?page=${encodeURIComponent(String(page))}&pageSize=${encodeURIComponent(String(pageSize))}`,
        null,
        bound.appKey
      );
      return {
        ok: true,
        action,
        data: response,
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl,
          page,
          pageSize
        }
      };
    }

    if (action === "verify") {
      const text = requireOption(options, "text", "verify requires --text");
      const payload = buildVerifyPayload(options, "text", text);
      const requestId = crypto.randomUUID();
      const response = await callApi(
        bound.apiBaseUrl,
        "POST",
        "/api/v4/plugin/verify",
        payload.requestBody,
        bound.appKey,
        requestId
      );
      return {
        ok: true,
        action,
        data: response,
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl,
          extractedFields: payload.extracted.fields,
          normalizedText: payload.extracted.normalizedText
        }
      };
    }

    if (action === "verify-image") {
      const image = validateImagePayload(readImageInput(options));
      const textInput = resolveBatchTextForImage(options, image.imagePath || null);
      const payload = buildVerifyPayload({ ...options, text: textInput.text }, "image", image.base64);
      const requestId = crypto.randomUUID();
      const response = await callApi(
        bound.apiBaseUrl,
        "POST",
        "/api/v4/plugin/verify",
        payload.requestBody,
        bound.appKey,
        requestId
      );
      return {
        ok: true,
        action,
        data: {
          ...response,
          quotaCost: 2,
          quotaCostNotice: "Image verification costs 2 quota per request."
        },
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl,
          costQuota: 2,
          quotaNotice: "Image verification costs 2 quota per request.",
          extractedFields: payload.extracted.fields,
          normalizedText: payload.extracted.normalizedText,
          image: {
            source: image.imageSource,
            path: image.imagePath || null,
            mimeType: image.mimeType,
            sizeBytes: image.sizeBytes
          },
          textSupplementUsed: Boolean(textInput.text),
          sidecarTextPath: textInput.sidecarTextPath
        }
      };
    }

    if (action === "verify-directory") {
      const sourceDirectory = ensureDirectoryExists(
        requireOption(options, "dir", "verify-directory requires --dir <folder>"),
        "verify-directory requires an existing directory"
      );
      const recursive = parseBooleanOption(options.recursive, false);
      const imageFiles = listImageFiles(sourceDirectory, recursive);

      if (imageFiles.length === 0) {
        throw new Error(`no supported image files found in directory: ${sourceDirectory}`);
      }

      const results = [];
      for (const imageFile of imageFiles) {
        results.push(await verifyImageFile(bound, imageFile, options));
      }

      const successCount = results.filter((item) => item.ok).length;
      const failureCount = results.length - successCount;

      if (results.length === 1) {
        const outputPath = path.join(sourceDirectory, `${path.basename(imageFiles[0])}.verify.json`);
        const singlePayload = {
          generatedAt: new Date().toISOString(),
          sourceDirectory,
          totalFiles: 1,
          successCount,
          failureCount,
          result: results[0]
        };
        writeJsonFile(outputPath, singlePayload);
        return {
          ok: true,
          action,
          data: {
            mode: "single",
            sourceDirectory,
            totalFiles: 1,
            successCount,
            failureCount,
            outputPath,
            result: results[0]
          },
          meta: {
            autoBound: bound.autoBound,
            apiBaseUrl: bound.apiBaseUrl,
            recursive
          }
        };
      }

      const outputDirectory = path.join(
        sourceDirectory,
        `invoice-verify-results-${formatTimestampForFileName()}`
      );
      fs.mkdirSync(outputDirectory, { recursive: true });

      const resultFiles = [];
      for (let index = 0; index < results.length; index += 1) {
        const imageFile = imageFiles[index];
        const relativeName = path.relative(sourceDirectory, imageFile) || path.basename(imageFile);
        const outputFileName = `${String(index + 1).padStart(3, "0")}-${sanitizeFileName(relativeName)}.verify.json`;
        const outputFilePath = path.join(outputDirectory, outputFileName);
        writeJsonFile(outputFilePath, results[index]);
        resultFiles.push({
          sourceFile: imageFile,
          outputFile: outputFilePath,
          ok: results[index].ok
        });
      }

      const summaryPath = path.join(outputDirectory, "summary.json");
      const summaryPayload = {
        generatedAt: new Date().toISOString(),
        sourceDirectory,
        totalFiles: results.length,
        successCount,
        failureCount,
        recursive,
        resultFiles
      };
      writeJsonFile(summaryPath, summaryPayload);

      return {
        ok: true,
        action,
        data: {
          mode: "batch",
          sourceDirectory,
          totalFiles: results.length,
          successCount,
          failureCount,
          outputDirectory,
          summaryPath,
          resultFiles
        },
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl,
          recursive
        }
      };
    }

    if (action === "create-order") {
      const amount = parseIntegerOption(options, "amount", "create-order requires --amount <positive integer yuan>");
      const waitSeconds = parseNonNegativeIntegerOption(
        options["wait-seconds"],
        "wait-seconds must be a non-negative integer",
        90
      );
      const pollIntervalSeconds = parseNonNegativeIntegerOption(
        options["poll-interval-seconds"],
        "poll-interval-seconds must be a non-negative integer",
        3
      );
      if (pollIntervalSeconds <= 0) {
        throw new Error("poll-interval-seconds must be at least 1");
      }
      const agreeTerms =
        options["agree-terms"] === undefined
          ? true
          : parseBooleanOption(options["agree-terms"], true);
      const response = await callApi(
        bound.apiBaseUrl,
        "POST",
        "/api/v4/plugin/orders",
        {
          amount,
          agreeTerms
        },
        bound.appKey,
        crypto.randomUUID()
      );
      const orderData = response && response.data ? response.data : {};
      const paymentPageUrl = orderData.paymentPageUrl || orderData.payQrCode || null;
      const qrCodes = buildQrCodeEntries(orderData);
      const orderNo = orderData.orderNo || null;
      let orderPolling = null;
      if (orderNo) {
        try {
          orderPolling = await pollOrderUntilFinal(bound, orderNo, waitSeconds, pollIntervalSeconds);
        } catch (error) {
          orderPolling = {
            orderNo,
            finalStatus: "",
            settled: false,
            polls: 0,
            waitedSeconds: 0,
            maxWaitSeconds: waitSeconds,
            pollIntervalSeconds,
            orderQuery: null,
            error: normalizeErrorPayload(error)
          };
        }
      }
      const finalOrderResponse = orderPolling && orderPolling.orderQuery ? orderPolling.orderQuery : null;
      const finalStatus = orderPolling ? orderPolling.finalStatus : extractOrderStatus(response);
      const settled = orderPolling ? orderPolling.settled : false;
      const quotaAfterPayment =
        finalOrderResponse && finalOrderResponse.remainingQuota !== undefined
          ? finalOrderResponse.remainingQuota
          : null;
      const guidanceParts = [];
      if (paymentPageUrl) {
        guidanceParts.push("Use paymentPageUrl to open the cashier page and choose WeChat or Alipay.");
      }
      if (qrCodes.length) {
        guidanceParts.push("Below are the QR codes for the available payment methods.");
      }
      const paymentGuidance = guidanceParts.length ? guidanceParts.join(" ") : null;
      const paymentPostTip = settled
        ? `Recharge credited. Remaining quota: ${quotaAfterPayment === null ? "unknown" : quotaAfterPayment}.`
        : "Payment not settled yet in callback. You can run `query-order` or `quota` again shortly.";
      return {
        ok: true,
        action,
        data: {
          ...response,
          paymentPageUrl,
          paymentGuidance,
          qrCodes,
          paymentPostTip,
          paymentSettled: settled,
          orderStatus: finalStatus || null,
          orderPolling
        },
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl,
          amount,
          agreeTerms,
          orderNo,
          waitSeconds,
          pollIntervalSeconds,
          paymentSettled: settled
        }
      };
    }

    if (action === "query-order") {
      const orderNo = requireOption(options, "order-no", "query-order requires --order-no <orderNo>");
      const response = await callApi(
        bound.apiBaseUrl,
        "GET",
        `/api/v4/plugin/orders/${encodeURIComponent(orderNo)}`,
        null,
        bound.appKey
      );
      return {
        ok: true,
        action,
        data: response,
        meta: {
          autoBound: bound.autoBound,
          apiBaseUrl: bound.apiBaseUrl,
          orderNo,
          orderStatus: extractOrderStatus(response),
          paymentSettled: isOrderCreditedStatus(extractOrderStatus(response))
        }
      };
    }

    throw new Error(`unsupported action: ${action}`);
  }, {
    apiBaseUrl,
    clientInstanceId: options["client-instance-id"],
    deviceFingerprint: options["device-fingerprint"]
  });
}

async function main() {
  const argv = process.argv.slice(2);
  const { positionals, options } = parseArgs(argv);
  const action = positionals[0] || "help";

  if (
    action === "verify-image" &&
    !options["image-file"] &&
    !options["image-base64"] &&
    !options.image &&
    positionals[1]
  ) {
    options.image = positionals[1];
  }

  if (action === "config") {
    options._subaction = positionals[1] || "show";
  }

  const result = await runAction(action, options);
  printJson(result, result.ok ? 0 : 1);
}

main().catch((error) => {
  fail(error && error.message ? error.message : String(error), {
    code: error && error.code ? String(error.code) : "",
    status: error && error.status ? error.status : null,
    response: error && error.response ? error.response : null
  });
});
