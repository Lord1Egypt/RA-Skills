const { runSkill, runFullFlow } = require("../_easybuy_browser_runtime");

const EASYBUY_SKILLS = new Set([
  "order_reader",
  "evidence_builder",
  "message_drafter",
  "form_filler",
  "amazon_product_detector",
  "amazon_orders_scraper",
  "amazon_orders_opener",
  "amazon_order_details_fetcher",
  "amazon_price_checker",
  "amazon_review_scraper",
  "amazon_contact_flow",
  "message_monitor",
  "price_alert_manager",
  "case_exporter"
]);

const NATURAL_FULL_FLOW_TRIGGERS = [
  "执行amazon-after-sales-flow",
  "运行amazon-after-sales-flow",
  "run amazon-after-sales-flow",
  "execute amazon-after-sales-flow",
  "full flow",
  "run_full_flow",
  "全流程",
  "售后"
];

function parseJson(text) {
  const raw = String(text || "").trim();
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function looksLikeJsonObject(text) {
  const raw = String(text || "").trim();
  return raw.startsWith("{") && raw.endsWith("}");
}

function isLikelyUrlInput(inputText) {
  const raw = String(inputText || "").trim();
  if (!raw) return false;
  if (/^https?:\/\//i.test(raw)) return true;
  if (/\s/.test(raw)) return false;
  return /^[a-z0-9.-]+\.[a-z]{2,}([/:?#].*)?$/i.test(raw);
}

function parseYearFromText(text) {
  const m = String(text || "").match(/\b(20\d{2})\b/);
  if (!m) return new Date().getFullYear();
  const y = Number(m[1]);
  if (!Number.isFinite(y) || y < 2000 || y > 2100) return new Date().getFullYear();
  return y;
}

function parseMessageFromText(text) {
  const raw = String(text || "").trim();
  const quoted = raw.match(/(?:message|消息|内容)\s*[:：]\s*["“](.+?)["”]/i);
  if (quoted && quoted[1]) return quoted[1].trim();
  return "I noticed a price drop after purchase and request a refund for the difference.";
}

function parseAutoSendFromText(text) {
  const raw = String(text || "").toLowerCase();
  if (/(auto[\s_-]?send|自动发送|直接发送|send now)/i.test(raw)) return true;
  if (/(no[\s_-]?send|dont send|don't send|不发送|仅输入|只输入)/i.test(raw)) return false;
  return false;
}

function toNaturalFullFlowPayload(inputText) {
  const raw = String(inputText || "").trim();
  if (!raw) return null;
  if (isLikelyUrlInput(raw)) return null;

  const lower = raw.toLowerCase();
  const hit = NATURAL_FULL_FLOW_TRIGGERS.some((k) => lower.includes(k.toLowerCase())) || lower.includes("amazon-after-sales-flow");
  if (!hit) return null;

  return {
    action: "run_full_flow",
    year: parseYearFromText(raw),
    message: parseMessageFromText(raw),
    auto_send: parseAutoSendFromText(raw),
    browser: {
      headless: false,
      keepOpen: true,
      slowMo: 300,
      timeoutMs: 60000,
      debug: true
    }
  };
}

function blockedUrlResponse(inputText) {
  return JSON.stringify({
    status: "blocked",
    reason: "url_open_disabled_for_security",
    input: String(inputText || ""),
    hint: "Use natural language like '执行amazon-after-sales-flow 2025' or JSON action run_full_flow."
  });
}

function unsupportedInputResponse() {
  return JSON.stringify({
    status: "error",
    error: "unsupported_input",
    hint: "Use '执行amazon-after-sales-flow 2025' / 'run amazon-after-sales-flow 2025' or JSON {\"action\":\"run_full_flow\"}."
  });
}

async function run(inputText) {
  const payload = parseJson(inputText);

  if (payload && typeof payload === "object" && !Array.isArray(payload)) {
    const skillName = String(payload.skill || "").trim();
    if (EASYBUY_SKILLS.has(skillName)) {
      return runSkill(skillName, JSON.stringify(payload.args || {}));
    }

    const action = String(payload.action || "").trim().toLowerCase();
    if (action === "open_orders") {
      return runSkill("amazon_orders_opener", JSON.stringify(payload));
    }
    if (["run_contact_flow", "contact_flow"].includes(action)) {
      return runSkill("amazon_contact_flow", JSON.stringify(payload));
    }
    if (["run_full_flow", "full_flow", "open_orders_and_contact"].includes(action)) {
      return runFullFlow(JSON.stringify(payload));
    }

    if (payload.playbook) {
      const name = String(payload.playbook).toLowerCase();
      if (["refund", "replacement", "return", "refund_request", "replacement_request", "return_request"].includes(name)) {
        return runFullFlow(JSON.stringify(payload));
      }
    }
  }

  if (looksLikeJsonObject(inputText) && payload === null) {
    throw new Error("invalid_json_input");
  }

  const naturalFlowPayload = toNaturalFullFlowPayload(inputText);
  if (naturalFlowPayload) {
    return runFullFlow(JSON.stringify(naturalFlowPayload));
  }

  if (isLikelyUrlInput(inputText)) {
    return blockedUrlResponse(inputText);
  }

  return unsupportedInputResponse();
}

if (require.main === module) {
  const input = process.argv.slice(2).join(" ");
  run(input)
    .then((out) => process.stdout.write(String(out)))
    .catch((err) => {
      process.stderr.write(err && err.message ? err.message : String(err));
      process.exit(1);
    });
}

module.exports = { run };

