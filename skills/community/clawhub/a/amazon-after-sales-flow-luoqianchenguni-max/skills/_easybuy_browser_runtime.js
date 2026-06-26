const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const ARTIFACTS_DIR = path.join(ROOT, "artifacts");

function compact(value, maxLen = 260) {
  try {
    const raw = typeof value === "string" ? value : JSON.stringify(value);
    if (!raw) return "";
    return raw.length > maxLen ? `${raw.slice(0, maxLen)}...` : raw;
  } catch {
    const raw = String(value || "");
    return raw.length > maxLen ? `${raw.slice(0, maxLen)}...` : raw;
  }
}

function createLogger(enabled, prefix) {
  return (event, data = {}) => {
    if (!enabled) return;
    const payload = {
      ts: new Date().toISOString(),
      event,
      ...data
    };
    try {
      console.log(`[EB/runtime][${prefix}] ${JSON.stringify(payload)}`);
    } catch {
      console.log(`[EB/runtime][${prefix}]`, payload);
    }
  };
}

function safeJsonParse(text) {
  const raw = String(text || "").trim();
  if (!raw) return {};
  try {
    const data = JSON.parse(raw);
    return data && typeof data === "object" ? data : { value: data };
  } catch {
    return { raw_text: raw };
  }
}

function loadSkillSpec(skillName) {
  const p = path.join(ROOT, "dist", "skills", `${skillName}.json`);
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function amazonBase(origin) {
  if (!origin) return "https://www.amazon.com";
  try {
    const u = new URL(String(origin));
    if (["http:", "https:"].includes(u.protocol) && /amazon\./i.test(u.hostname)) {
      return `${u.protocol}//${u.host}`;
    }
  } catch {
  }
  return "https://www.amazon.com";
}
function isTrustedAmazonUrl(raw) {
  try {
    const u = new URL(String(raw));
    const hostOk = /(^|\.)amazon\./i.test(String(u.hostname || ""));
    return u.protocol === "https:" && hostOk;
  } catch {
    return false;
  }
}

function sanitizeAmazonUrl(raw, fieldName = "url") {
  const value = String(raw || "").trim();
  if (!value) throw new Error(`${fieldName}_missing`);
  if (!isTrustedAmazonUrl(value)) throw new Error(`${fieldName}_not_allowed`);
  return new URL(value).toString();
}

function resolveAutoSend(args = {}) {
  const requested = args.auto_send === true || args.autoSend === true;
  if (!requested) return false;
  const confirmed =
    args.confirm_send === true ||
    args.confirmSend === true ||
    String(args.send_confirmation || args.sendConfirmation || "").trim() === "YES_SEND";
  return Boolean(confirmed);
}

function ordersUrlFromArgs(args = {}) {
  const base = amazonBase(args.origin);
  const qs = new URLSearchParams();
  if (args.timeFilter) {
    qs.set("timeFilter", String(args.timeFilter));
  } else if (args.year) {
    qs.set("timeFilter", `year-${String(args.year)}`);
    qs.set("ref_", `ppx_yo2ov_dt_b_filter_all_y${String(args.year)}`);
  }
  const s = qs.toString();
  return s ? `${base}/your-orders/orders?${s}` : `${base}/your-orders/orders`;
}

function detailsUrlFromArgs(args = {}) {
  if (args.details_url) return sanitizeAmazonUrl(args.details_url, "details_url");
  if (args.detailsUrl) return sanitizeAmazonUrl(args.detailsUrl, "details_url");
  if (!args.order_id && !args.orderId) return null;
  const orderId = args.order_id || args.orderId;
  const base = amazonBase(args.origin);
  return `${base}/your-orders/order-details?orderID=${encodeURIComponent(String(orderId))}`;
}

async function launchContext(options = {}) {
  const headless = options.headless !== false;
  const slowMo = Number(options.slowMo || 0);
  const timeout = Number(options.timeoutMs || 45000);
  const userDataDir = path.resolve(options.userDataDir || path.join(ROOT, ".browser-profile"));
  ensureDir(userDataDir);

  const launchOpts = {
    headless,
    slowMo,
    viewport: { width: 1400, height: 900 }
  };

  if (options.executablePath) {
    launchOpts.executablePath = String(options.executablePath);
  } else {
    launchOpts.channel = options.channel || "chrome";
  }

  const context = await chromium.launchPersistentContext(userDataDir, launchOpts);
  context.setDefaultTimeout(timeout);
  let page = context.pages()[0];
  if (!page) page = await context.newPage();
  return { context, page };
}

async function wait(ms) {
  await new Promise((r) => setTimeout(r, Number(ms || 500)));
}

async function waitForSelectorVisible(page, selector, timeoutMs = 10000) {
  try {
    const loc = page.locator(selector).first();
    await loc.waitFor({ state: "visible", timeout: timeoutMs });
    return loc;
  } catch {
    return null;
  }
}

async function toolQuery(page, args = {}) {
  const selector = String(args.selector || "body");
  const count = await page.locator(selector).count();
  let preview = "";
  if (count > 0) {
    preview = (await page.locator(selector).first().innerText().catch(() => "") || "").trim().slice(0, 200);
  }
  return { selector, count, preview };
}

async function toolGetDom(page, args = {}) {
  const selector = args.selector ? String(args.selector) : null;
  const limit = Number(args.limit || 5000);
  const html = await page.evaluate(({ selector, limit }) => {
    const node = selector ? document.querySelector(selector) : document.documentElement;
    return (node ? node.outerHTML : "").slice(0, limit);
  }, { selector, limit });
  return { html };
}

async function toolNavigate(page, args = {}) {
  const url = args.url ? String(args.url) : null;
  if (!url) throw new Error("navigate_target_missing");
  const trustedUrl = sanitizeAmazonUrl(url, "navigate_url");
  await page.goto(trustedUrl, { waitUntil: "domcontentloaded" });
  return { url: trustedUrl };
}

async function toolClick(page, args = {}) {
  const selector = String(args.selector || "");
  const allowMissing = Boolean(args.allowMissing);
  if (!selector) throw new Error("missing_selector");
  const loc = await waitForSelectorVisible(page, selector, Number(args.timeoutMs || 10000));
  if (!loc) {
    if (allowMissing) return { selector, skipped: true };
    throw new Error("element_not_found");
  }
  await loc.scrollIntoViewIfNeeded().catch(() => {});
  await loc.click({ timeout: Number(args.timeoutMs || 10000) });
  return { selector };
}

async function toolClickText(page, args = {}) {
  const text = String(args.text || "").trim();
  const selector = String(args.selector || "a,button,span,div,li");
  const exact = Boolean(args.exact);
  const timeoutMs = Number(args.timeoutMs || 8000);
  const allowMissing = Boolean(args.allowMissing);
  if (!text) throw new Error("missing_text");

  const result = await page.evaluate(async ({ text, selector, exact, timeoutMs }) => {
    const target = text.toLowerCase();
    const start = Date.now();
    const visible = (el) => {
      if (!el) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
    };
    while (Date.now() - start < timeoutMs) {
      const nodes = Array.from(document.querySelectorAll(selector)).filter(visible);
      const found = nodes.find((n) => {
        const candidates = [
          (n.textContent || "").trim(),
          (n.getAttribute?.("aria-label") || "").trim(),
          (n.getAttribute?.("title") || "").trim(),
          (n.value || "").trim()
        ].filter(Boolean).map((s) => s.toLowerCase());
        if (!candidates.length) return false;
        return exact ? candidates.some((c) => c === target) : candidates.some((c) => c.includes(target));
      });
      if (found) {
        found.scrollIntoView({ block: "center", inline: "center" });
        found.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        found.click?.();
        return { ok: true };
      }
      await new Promise((r) => setTimeout(r, 250));
    }
    return { ok: false };
  }, { text, selector, exact, timeoutMs });

  if (!result.ok) {
    if (allowMissing) return { selector, text, skipped: true };
    throw new Error("text_not_found");
  }
  return { selector, text };
}

async function toolType(page, args = {}) {
  const selector = String(args.selector || "");
  const text = String(args.text || "");
  const clear = args.clear !== false;
  if (!selector) throw new Error("missing_selector");
  const loc = await waitForSelectorVisible(page, selector, Number(args.timeoutMs || 10000));
  if (!loc) throw new Error("element_not_found");
  await loc.click({ timeout: 5000 }).catch(() => {});
  if (clear) await loc.fill("");
  await loc.type(text, { delay: 8 });
  return { selector, length: text.length };
}

async function toolTypeMessage(page, args = {}) {
  const text = String(args.text || "");
  const autoSend = Boolean(args.autoSend || args.auto_send);
  const data = await page.evaluate(async ({ text, autoSend }) => {
    const visible = (el) => {
      if (!el) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
    };

    const inputs = Array.from(document.querySelectorAll("textarea, [contenteditable='true'], [role='textbox']")).filter(visible);
    const input = inputs[0] || null;
    if (!input) return { ok: false, error: "input_not_found" };

    input.focus?.();
    if (input instanceof HTMLTextAreaElement || input instanceof HTMLInputElement) {
      input.value = text;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      input.textContent = text;
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }

    let sent = false;
    if (autoSend && text.trim().length >= 2) {
      const btns = Array.from(document.querySelectorAll("button, input[type='submit']")).filter(visible);
      const btn = btns.find((n) => {
        const t = (n.textContent || "").trim().toLowerCase();
        const a = (n.getAttribute?.("aria-label") || "").toLowerCase();
        const title = (n.getAttribute?.("title") || "").toLowerCase();
        return t.includes("send") || a.includes("send") || title.includes("send");
      });
      if (btn) {
        btn.click();
        sent = true;
      }
    }
    return { ok: true, sent };
  }, { text, autoSend });

  if (!data.ok) throw new Error(data.error || "type_message_failed");
  return { sent: Boolean(data.sent) };
}

async function toolScroll(page, args = {}) {
  if (args.selector) {
    const selector = String(args.selector);
    const loc = await waitForSelectorVisible(page, selector, Number(args.timeoutMs || 10000));
    if (!loc) throw new Error("element_not_found");
    await loc.scrollIntoViewIfNeeded();
    return { selector };
  }
  const top = Number(args.top || 500);
  await page.evaluate((top) => window.scrollBy({ top, behavior: "smooth" }), top);
  return { top };
}

async function toolWait(_page, args = {}) {
  const ms = Number(args.ms || 500);
  await wait(ms);
  return { ms };
}

async function toolExtract(page, schema = {}) {
  if (!schema.rootSelector || !schema.fields) throw new Error("invalid_schema");
  const data = await page.evaluate((schema) => {
    const attrOf = (node, attr) => {
      if (!node) return null;
      if (!attr) return (node.textContent || "").trim() || null;
      return node.getAttribute(attr);
    };
    const mapFields = (root) => {
      const item = {};
      for (const [key, field] of Object.entries(schema.fields)) {
        const node = root ? root.querySelector(field.selector) : null;
        item[key] = attrOf(node, field.attr);
      }
      return item;
    };

    if (schema.list) {
      const roots = Array.from(document.querySelectorAll(schema.rootSelector));
      return { items: roots.map((r) => mapFields(r)) };
    }
    const root = document.querySelector(schema.rootSelector);
    return { item: mapFields(root) };
  }, schema);
  return data;
}

async function toolScreenshot(page, args = {}) {
  ensureDir(ARTIFACTS_DIR);
  const artifactId = `artifact_${Date.now()}_${Math.random().toString(16).slice(2)}`;
  const filePath = path.join(ARTIFACTS_DIR, `${artifactId}.png`);

  if (args.selector) {
    const loc = await waitForSelectorVisible(page, String(args.selector), Number(args.timeoutMs || 10000));
    if (!loc) throw new Error("element_not_found");
    await loc.screenshot({ path: filePath });
  } else {
    await page.screenshot({ path: filePath, fullPage: true });
  }
  return { artifactId, filePath };
}

async function runContactFlow(initialPage, context = null, includePage = false, logger = null) {
  let page = initialPage;
  const log = [];
  const logEvt = typeof logger === "function" ? logger : () => {};

  const isContactLikeUrl = (url) => /\/gp\/help\/contact|\/messaging|\/message-us|\/contact-us/i.test(String(url || ""));

  const getVisibleInputCount = async (p) => {
    return p.evaluate(() => {
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };

      const selectors = "textarea, [contenteditable='true'], [role='textbox']";
      const nodes = Array.from(document.querySelectorAll(selectors)).filter(visible);

      const frames = Array.from(document.querySelectorAll("iframe"));
      frames.forEach((frame) => {
        try {
          const doc = frame.contentDocument;
          if (!doc) return;
          const inside = Array.from(doc.querySelectorAll(selectors)).filter((el) => {
            const s = doc.defaultView.getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
          });
          nodes.push(...inside);
        } catch (_) {
        }
      });

      return nodes.length;
    }).catch(() => 0);
  };

  const findContactUrl = async (p) => {
    return p.evaluate(() => {
      const links = Array.from(document.querySelectorAll("a[href]"));
      const target = links.find((a) => /\/gp\/help\/contact|contact-us|messaging/i.test(String(a.getAttribute("href") || "")));
      return target ? target.href : null;
    }).catch(() => null);
  };

  const maybeSwitchPage = async () => {
    if (!context) return;
    const pages = context.pages();
    const target = pages.find((p) => isContactLikeUrl(p.url())) || null;
    if (target && target !== page) {
      const from = page.url();
      page = target;
      await page.bringToFront().catch(() => {});
      logEvt("contact.switch_page", { from, to: page.url() });
    }
  };

  const clickTextWithPolling = async (p, options) => {
    const text = String(options.text || "").trim().toLowerCase();
    const selector = String(options.selector || "a,button,[role='button'],li.smartcs-buttons-button,input[type='button'],input[type='submit']");
    const exact = Boolean(options.exact);
    const timeoutMs = Number(options.timeoutMs || 15000);

    return p.evaluate(async ({ text, selector, exact, timeoutMs }) => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const textOf = (node) => {
        const t = (node.textContent || "").trim();
        const a = (node.getAttribute?.("aria-label") || "").trim();
        const title = (node.getAttribute?.("title") || "").trim();
        const value = (node.value || "").trim();
        return [t, a, title, value].find(Boolean) || "";
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button'],li.smartcs-buttons-button,input[type='button'],input[type='submit']") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          text: textOf(node).slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        const nodes = Array.from(document.querySelectorAll(selector)).filter(visible);
        const found = nodes.find((n) => {
          const candidate = n.closest?.("a,button,[role='button'],li.smartcs-buttons-button,input[type='button'],input[type='submit']") || n;
          if (!candidate || candidate === document.body || candidate === document.documentElement) return false;
          if (!visible(candidate)) return false;
          const t = textOf(candidate).toLowerCase();
          if (!t || t.length > 180) return false;
          return exact ? t === text : t.includes(text);
        });

        if (found) {
          const detail = clickNode(found);
          return { clicked: true, ...detail };
        }
        await sleep(300);
      }
      return { skipped: true };
    }, { text, selector, exact, timeoutMs });
  };

  const clickAskEntry = async (p) => {
    return p.evaluate(async () => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button']") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          text: ((node.textContent || node.getAttribute?.("aria-label") || node.getAttribute?.("title") || "").trim()).slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const selectors = [
        "a[href*='shipconns_dt_b_prod_question']",
        "a[href*='/gp/help/contact/contact.html'][href*='orderId=']",
        "a[href*='/gp/help/contact/contact.html'][href*='assistanceType=order']",
        "a[data-action*='ask']",
        "button[data-action*='ask']",
        "a,button,[role='button']"
      ];

      const start = Date.now();
      while (Date.now() - start < 18000) {
        for (const sel of selectors) {
          const nodes = Array.from(document.querySelectorAll(sel)).filter(visible);
          const found = nodes.find((n) => {
            const t = ((n.textContent || n.getAttribute?.("aria-label") || n.getAttribute?.("title") || "").trim()).toLowerCase();
            if (sel === "a,button,[role='button']") {
              return t.includes("ask product question") || t.includes("contact seller");
            }
            return true;
          });
          if (found) {
            const detail = clickNode(found);
            return { clicked: true, selector: sel, ...detail };
          }
        }
        await sleep(350);
      }
      return { skipped: true };
    });
  };

  const listSmartcsOptions = async (p) => {
    return p.evaluate(() => {
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const isEnabled = (el) => {
        if (!el) return false;
        const cls = String(el.className || "").toLowerCase();
        if (cls.includes("disabled")) return false;
        if (el.hasAttribute("disabled")) return false;
        const aria = String(el.getAttribute("aria-disabled") || "").toLowerCase();
        if (aria === "true") return false;
        return true;
      };

      const selectors = [
        "li.smartcs-buttons-button",
        "button.smartcs-button",
        ".smartcs-buttons-container button",
        ".smartcs-buttons-container a[role='button']"
      ];
      const nodes = selectors.flatMap((sel) => Array.from(document.querySelectorAll(sel))).filter((n) => visible(n) && isEnabled(n));
      const texts = nodes
        .map((n) => (n.textContent || n.getAttribute?.("aria-label") || "").trim())
        .filter((t) => t && t.length <= 120);
      return Array.from(new Set(texts)).slice(0, 30);
    }).catch(() => []);
  };

  const clickSmartcsButtonByKeywords = async (p, keywords = []) => {
    return p.evaluate(async ({ keywords }) => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const keys = Array.isArray(keywords) ? keywords.map((k) => String(k || "").toLowerCase()).filter(Boolean) : [];
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const isEnabled = (el) => {
        if (!el) return false;
        const cls = String(el.className || "").toLowerCase();
        if (cls.includes("disabled")) return false;
        if (el.hasAttribute("disabled")) return false;
        const aria = String(el.getAttribute("aria-disabled") || "").toLowerCase();
        if (aria === "true") return false;
        return true;
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button'],li.smartcs-buttons-button") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          text: (node.textContent || "").trim().slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const start = Date.now();
      while (Date.now() - start < 20000) {
        const nodes = Array.from(document.querySelectorAll("li.smartcs-buttons-button, .smartcs-buttons-container button, .smartcs-buttons-container a[role='button']")).filter((n) => visible(n) && isEnabled(n));
        const found = nodes.find((n) => {
          const t = (n.textContent || n.getAttribute?.("aria-label") || "").trim().toLowerCase();
          if (!t || t.length > 120) return false;
          return keys.some((k) => t.includes(k));
        });
        if (found) {
          const detail = clickNode(found);
          return { clicked: true, matchedBy: "keywords", ...detail };
        }
        await sleep(350);
      }
      return { skipped: true };
    }, { keywords });
  };

  const listSelectCards = async (p) => {
    return p.evaluate(() => {
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };

      const footers = Array.from(document.querySelectorAll(".smartcs-card-carousel a .card-footer, .smartcs-card-carousel .card-footer")).filter(visible);
      return footers.map((node, idx) => {
        const card = node.closest("a, .smartcs-card, li, div") || node;
        const cardText = (card.textContent || "").trim().replace(/\s+/g, " ").slice(0, 220);
        const footerText = (node.textContent || "").trim().replace(/\s+/g, " ").slice(0, 80);
        return { index: idx, footerText, cardText };
      });
    }).catch(() => []);
  };

  const clickSelectCardByIndex = async (p, index) => {
    return p.evaluate(({ index }) => {
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button']") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          text: (node.textContent || "").trim().slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const footers = Array.from(document.querySelectorAll(".smartcs-card-carousel a .card-footer, .smartcs-card-carousel .card-footer")).filter(visible);
      const target = footers[Number(index)] || null;
      if (!target) return { skipped: true, reason: "select_index_not_found", index };
      const detail = clickNode(target);
      return { clicked: true, index, source: "smartcs-card-carousel-by-index", ...detail };
    }, { index }).catch((err) => ({ skipped: true, reason: err && err.message ? err.message : String(err), index }));
  };

  const clickSelectUntilOtherReady = async (p, contactUrl) => {
    const readSelectState = async () => {
      return p.evaluate(() => {
        const pickText = (n) => (n.textContent || n.getAttribute?.("aria-label") || "").trim();
        const options = Array.from(document.querySelectorAll("li.smartcs-buttons-button, .smartcs-buttons-container button, .smartcs-buttons-container a[role='button']"))
          .map((n) => pickText(n))
          .filter(Boolean)
          .slice(0, 40);
        const selectedCards = document.querySelectorAll(".smartcs-card-carousel [aria-selected='true'], .smartcs-card-carousel .selected, .smartcs-card-selected").length;
        const signature = `${selectedCards}|${options.join("|")}`;
        return { selectedCards, options, signature };
      }).catch(() => ({ selectedCards: 0, options: [], signature: "" }));
    };

    const cards = await listSelectCards(p);
    if (!cards.length) {
      const before = await readSelectState();
      const fallback = await clickSelectCard(p);
      await wait(1400);
      const after = await readSelectState();
      const activated = before.signature !== after.signature;
      return { ...fallback, cardsTried: 0, optionsAfterClick: after.options, selectActivated: activated };
    }

    let last = null;
    for (let i = 0; i < cards.length; i += 1) {
      if (i > 0 && contactUrl) {
        await p.goto(contactUrl, { waitUntil: "domcontentloaded" }).catch(() => {});
        await wait(1200);
      }

      const before = await readSelectState();
      const clickRes = await clickSelectCardByIndex(p, i);
      await wait(1400);
      const after = await readSelectState();
      const activated = before.signature !== after.signature;

      const snapshot = {
        ...clickRes,
        triedIndex: i,
        card: cards[i],
        optionsAfterClick: after.options,
        selectActivated: activated
      };

      logEvt("contact.select.try", {
        triedIndex: i,
        cardText: cards[i]?.cardText || "",
        footerText: cards[i]?.footerText || "",
        options: after.options,
        selectActivated: activated
      });

      if (activated) return snapshot;
      last = snapshot;
    }

    return last || { skipped: true, reason: "select_cards_exhausted", selectActivated: false, optionsAfterClick: [] };
  };

  const clickSelectCard = async (p) => {
    return p.evaluate(async () => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button']") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          text: (node.textContent || "").trim().slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const start = Date.now();
      while (Date.now() - start < 20000) {
        const footers = Array.from(document.querySelectorAll(".smartcs-card-carousel a .card-footer, .smartcs-card-carousel .card-footer")).filter(visible);
        const footer = footers.find((x) => (x.textContent || "").trim().toLowerCase().includes("select"));
        if (footer) {
          const detail = clickNode(footer);
          return { clicked: true, source: "smartcs-card-carousel", ...detail };
        }

        const inCarousel = Array.from(document.querySelectorAll(".smartcs-card-carousel a, .smartcs-card-carousel button, .smartcs-card-carousel [role='button']")).filter(visible);
        const exactSelect = inCarousel.find((x) => (x.textContent || "").trim().toLowerCase() === "select");
        if (exactSelect) {
          const detail = clickNode(exactSelect);
          return { clicked: true, source: "smartcs-card-carousel-exact", ...detail };
        }

        const globalCandidates = Array.from(document.querySelectorAll("a,button,span,div")).filter(visible);
        const globalExactSelect = globalCandidates.find((x) => (x.textContent || "").trim().toLowerCase() === "select");
        if (globalExactSelect) {
          const detail = clickNode(globalExactSelect);
          return { clicked: true, source: "global-exact-select", ...detail };
        }

        await sleep(350);
      }
      return { skipped: true };
    });
  };

  const forceClickSelect = async (p) => {
    const selectors = [
      ".smartcs-card-carousel a .card-footer:has-text(\"Select\")",
      ".smartcs-card-carousel .card-footer:has-text(\"Select\")",
      ".smartcs-card-carousel a:has-text(\"Select\")",
      ".smartcs-card-carousel [role='button']:has-text(\"Select\")"
    ];

    for (const sel of selectors) {
      try {
        const loc = p.locator(sel).first();
        await loc.waitFor({ state: "visible", timeout: 8000 });
        await loc.scrollIntoViewIfNeeded().catch(() => {});
        await loc.click({ timeout: 8000, force: true });
        await wait(700);
        return { clicked: true, source: "playwright-force", selector: sel };
      } catch (_) {
      }
    }

    try {
      const loc = p.getByText("Select", { exact: true }).first();
      await loc.waitFor({ state: "visible", timeout: 8000 });
      await loc.scrollIntoViewIfNeeded().catch(() => {});
      await loc.click({ timeout: 8000, force: true });
      await wait(700);
      return { clicked: true, source: "playwright-force-text", selector: "text=Select" };
    } catch (_) {
    }

    const domFallback = await p.evaluate(() => {
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button']") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          clicked: true,
          source: "dom-force",
          text: (node.textContent || "").trim().slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const cardFooters = Array.from(document.querySelectorAll(".smartcs-card-carousel a .card-footer, .smartcs-card-carousel .card-footer")).filter(visible);
      const footer = cardFooters.find((n) => (n.textContent || "").trim().toLowerCase() === "select") ||
        cardFooters.find((n) => (n.textContent || "").trim().toLowerCase().includes("select"));
      if (footer) return clickNode(footer);

      const globalExact = Array.from(document.querySelectorAll("a,button,[role='button'],span,div")).filter(visible)
        .find((n) => (n.textContent || "").trim().toLowerCase() === "select");
      if (globalExact) return clickNode(globalExact);

      return { skipped: true, reason: "force_select_not_found" };
    }).catch(() => ({ skipped: true, reason: "force_select_eval_failed" }));

    if (domFallback && domFallback.clicked) {
      await wait(700);
      return domFallback;
    }
    return domFallback || { skipped: true, reason: "force_select_not_found" };
  };

  const clickSmartcsButtonExact = async (p, text) => {
    return p.evaluate(async ({ text }) => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const target = String(text || "").trim().toLowerCase();
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const isEnabled = (el) => {
        if (!el) return false;
        const cls = String(el.className || "").toLowerCase();
        if (cls.includes("disabled")) return false;
        if (el.hasAttribute("disabled")) return false;
        const aria = String(el.getAttribute("aria-disabled") || "").toLowerCase();
        if (aria === "true") return false;
        return true;
      };
      const clickNode = (raw) => {
        const node = raw.closest?.("a,button,[role='button'],li.smartcs-buttons-button") || raw;
        node.scrollIntoView({ block: "center", inline: "center" });
        node.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
        node.click?.();
        return {
          text: (node.textContent || "").trim().slice(0, 120),
          html: (node.outerHTML || "").slice(0, 220)
        };
      };

      const start = Date.now();
      while (Date.now() - start < 20000) {
        const all = Array.from(document.querySelectorAll("li.smartcs-buttons-button, .smartcs-buttons-container button, .smartcs-buttons-container a[role='button']")).filter((n) => visible(n) && isEnabled(n));
        const found = all.find((li) => (li.textContent || li.getAttribute?.("aria-label") || "").trim().toLowerCase() === target);
        if (found) {
          const detail = clickNode(found);
          return { clicked: true, ...detail };
        }
        await sleep(350);
      }
      return { skipped: true };
    }, { text });
  };

  const waitForContactUiReady = async (p, timeoutMs = 30000) => {
    return p.evaluate(async ({ timeoutMs }) => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };

      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        const selectFooter = Array.from(document.querySelectorAll(".smartcs-card-carousel a .card-footer, .smartcs-card-carousel .card-footer"))
          .find((n) => visible(n) && (n.textContent || "").trim().toLowerCase().includes("select"));

        const buttonCount = Array.from(document.querySelectorAll("li.smartcs-buttons-button, .smartcs-buttons-container button, .smartcs-buttons-container a[role='button']"))
          .filter((n) => visible(n)).length;

        if (selectFooter || buttonCount > 0) {
          return {
            ready: true,
            hasSelectFooter: Boolean(selectFooter),
            buttonCount,
            elapsedMs: Date.now() - start
          };
        }
        await sleep(350);
      }

      return {
        ready: false,
        hasSelectFooter: false,
        buttonCount: 0,
        elapsedMs: timeoutMs
      };
    }, { timeoutMs }).catch(() => ({ ready: false, hasSelectFooter: false, buttonCount: 0, elapsedMs: timeoutMs }));
  };

  const waitForExactEnabledOption = async (p, text, timeoutMs = 30000) => {
    return p.evaluate(async ({ text, timeoutMs }) => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const target = String(text || "").trim().toLowerCase();
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0" && r.width > 0 && r.height > 0;
      };
      const isEnabled = (el) => {
        if (!el) return false;
        const cls = String(el.className || "").toLowerCase();
        if (cls.includes("disabled")) return false;
        if (el.hasAttribute("disabled")) return false;
        const aria = String(el.getAttribute("aria-disabled") || "").toLowerCase();
        if (aria === "true") return false;
        return true;
      };

      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        const nodes = Array.from(document.querySelectorAll("li.smartcs-buttons-button, .smartcs-buttons-container button, .smartcs-buttons-container a[role='button']")).filter((n) => visible(n) && isEnabled(n));
        const options = Array.from(new Set(nodes.map((n) => (n.textContent || n.getAttribute?.("aria-label") || "").trim()).filter(Boolean))).slice(0, 30);
        const found = nodes.find((n) => ((n.textContent || n.getAttribute?.("aria-label") || "").trim().toLowerCase() === target));
        if (found) {
          return { found: true, options };
        }
        await sleep(300);
      }
      const nodes = Array.from(document.querySelectorAll("li.smartcs-buttons-button, .smartcs-buttons-container button, .smartcs-buttons-container a[role='button']"));
      const options = Array.from(new Set(nodes.map((n) => (n.textContent || n.getAttribute?.("aria-label") || "").trim()).filter(Boolean))).slice(0, 30);
      return { found: false, options };
    }, { text, timeoutMs });
  };

  const step = async (name, fn, sleepMs = 1200) => {
    let out;
    logEvt("contact.step.start", { name, url: page.url() });
    try {
      out = await fn();
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      if (/Execution context was destroyed|Target page, context or browser has been closed/i.test(msg)) {
        out = { navigated: true };
      } else {
        out = { error: msg };
      }
    }

    await wait(sleepMs);
    await maybeSwitchPage();
    log.push({ name, ok: out, url: page.url(), ts: Date.now() });
    logEvt("contact.step.end", { name, url: page.url(), result: compact(out) });
    return out;
  };

  logEvt("contact.start", { url: page.url() });
  await maybeSwitchPage();

  await step("ask product question", async () => {
    let out = await clickAskEntry(page);

    if (out && out.skipped) {
      out = await clickTextWithPolling(page, {
        text: "ask product question",
        selector: "a,button,[role='button']",
        exact: false,
        timeoutMs: 12000
      });
    }

    if (out && out.skipped) {
      out = await clickTextWithPolling(page, {
        text: "contact seller",
        selector: "a,button,[role='button']",
        exact: false,
        timeoutMs: 12000
      });
    }

    if (out && out.skipped) {
      out = await toolClick(page, {
        selector: "a[href*='/gp/help/contact'],a[href*='contact-us'],a[href*='messaging']",
        timeoutMs: 10000,
        allowMissing: true
      });
    }
    return out;
  }, 1600);

  if (!isContactLikeUrl(page.url())) {
    const contactUrl = await findContactUrl(page);
    logEvt("contact.goto_contact_url.try", { contactUrl: contactUrl || null, currentUrl: page.url() });
    if (contactUrl) {
      await page.goto(contactUrl, { waitUntil: "domcontentloaded" }).catch(() => {});
      await wait(1400);
      await maybeSwitchPage();
      log.push({ name: "goto contact url", ok: true, url: page.url(), ts: Date.now() });
      logEvt("contact.goto_contact_url.done", { url: page.url() });
    }
  }

  const contactEntryUrl = page.url();
  logEvt("contact.ui_ready.wait.start", { url: page.url() });
  const uiReady = await waitForContactUiReady(page, 30000);
  logEvt("contact.ui_ready.wait.end", uiReady);
  if (!uiReady.ready) {
    throw new Error("chain_break_contact_ui_not_ready");
  }

  const selectStep = await step("select", async () => {
    logEvt("contact.select.force.try", { url: page.url() });
    const forced = await forceClickSelect(page);
    if (forced && forced.clicked) {
      logEvt("contact.select.force.ok", forced);
      return forced;
    }
    logEvt("contact.select.force.fallback", forced || {});
    return clickSelectUntilOtherReady(page, contactEntryUrl);
  });

  const optionsAfterSelect = await listSmartcsOptions(page);
  logEvt("contact.options.after_select", { count: optionsAfterSelect.length, options: optionsAfterSelect });

  const selectClicked = Boolean(selectStep && selectStep.clicked);
  logEvt("contact.select.confirmed", {
    selectClicked,
    selectActivated: Boolean(selectStep && selectStep.selectActivated),
    optionsAfterSelect
  });

  if (!selectClicked) {
    throw new Error("chain_break_select_click_failed");
  }

  const otherStep = await step("other", async () => {
    const ready = await waitForExactEnabledOption(page, "other", 30000);
    if (!ready.found) {
      return { skipped: true, reason: "other_not_found", options: ready.options };
    }
    return clickSmartcsButtonExact(page, "other");
  });

  if (!otherStep || otherStep.skipped) {
    throw new Error("chain_break_other_not_found");
  }

  const optionsAfterOther = await listSmartcsOptions(page);
  logEvt("contact.options.after_other", { count: optionsAfterOther.length, options: optionsAfterOther });

  const returnPolicyStep = await step("return policy", async () => {
    const ready = await waitForExactEnabledOption(page, "return policy", 30000);
    if (!ready.found) {
      return { skipped: true, reason: "return_policy_not_found", options: ready.options };
    }
    return clickSmartcsButtonExact(page, "return policy");
  });

  if (!returnPolicyStep || returnPolicyStep.skipped) {
    throw new Error("chain_break_return_policy_not_found");
  }

  const optionsAfterReturnPolicy = await listSmartcsOptions(page);
  logEvt("contact.options.after_return_policy", { count: optionsAfterReturnPolicy.length, options: optionsAfterReturnPolicy });

  const convStep = await step("ok, take me to the conversation", async () => {
    const ready = await waitForExactEnabledOption(page, "ok, take me to the conversation", 30000);
    if (!ready.found) {
      return { skipped: true, reason: "conversation_button_not_found", options: ready.options };
    }
    return clickTextWithPolling(page, {
      text: "ok, take me to the conversation",
      selector: "a,button,[role='button']",
      exact: false,
      timeoutMs: 18000
    });
  });

  if (!convStep || convStep.skipped) {
    throw new Error("chain_break_conversation_button_not_found");
  }

  const inputCount = await getVisibleInputCount(page);
  const hasInput = inputCount > 0;

  const activeSteps = log.filter((x) => {
    if (!x || !x.ok || typeof x.ok !== "object") return false;
    if (x.ok.skipped === true) return false;
    if (x.ok.error) return false;
    return true;
  }).length;

  const ok = hasInput;
  const reason = ok ? null : "contact_flow_not_ready";
  const out = { ok, reason, hasInput, activeSteps, steps: log, url: page.url() };
  logEvt("contact.finish", { ok, reason, hasInput, activeSteps, url: page.url() });
  if (includePage) out.page = page;
  return out;
}

function nonBrowserSkill(skillName, args = {}) {
  if (skillName === "message_drafter") {
    const title = args.title || "your order";
    const buy = args.buy_price || "";
    const current = args.current_price || "";
    const tone = args.tone || "polite";
    const draft = `Hello, I bought ${title}${buy ? ` at ${buy}` : ""}. I noticed the current price is ${current || "lower"}. Could you help with a price adjustment/refund?`;
    return {
      skill: skillName,
      status: "ready",
      output: { draft_message: draft, summary: `${tone} request generated` }
    };
  }
  if (skillName === "price_alert_manager") {
    return {
      skill: skillName,
      status: "ready",
      output: { alert_id: `alert_${Date.now()}` }
    };
  }
  return null;
}

function expandSkillToCalls(skillName, args = {}, page) {
  switch (skillName) {
    case "amazon_orders_opener": {
      return [{ tool: "browser.navigate", args: { url: ordersUrlFromArgs(args) } }];
    }
    case "amazon_product_detector": {
      return [{
        tool: "browser.extract",
        args: {
          rootSelector: "body",
          fields: {
            asin: { selector: "#ASIN, input[name='ASIN']", attr: "value" },
            title: { selector: "#productTitle" },
            price: { selector: ".a-price .a-offscreen" },
            image_url: { selector: "#landingImage", attr: "src" },
            rating: { selector: "#acrPopover span.a-icon-alt" },
            review_count: { selector: "#acrCustomerReviewText" }
          }
        }
      }];
    }
    case "amazon_orders_scraper": {
      const calls = [{
        tool: "browser.extract",
        args: {
          rootSelector: ".order-card.js-order-card, .order-card",
          list: true,
          fields: {
            order_id: { selector: "[data-order-id]", attr: "data-order-id" },
            title: { selector: ".yohtmlc-item-title, .a-link-normal" },
            price: { selector: ".a-price .a-offscreen" },
            details_url: { selector: "a[href*='order-details']", attr: "href" }
          }
        }
      }];
      if (args.openFirstDetails) {
        calls.push({ tool: "browser.click", args: { selector: "a[href*='order-details']", allowMissing: false } });
      }
      return calls;
    }
    case "order_reader": {
      return [{
        tool: "browser.extract",
        args: {
          rootSelector: args.rootSelector || ".order-card",
          fields: args.fields || {
            title: { selector: ".item-title" },
            price: { selector: ".a-price .a-offscreen" }
          }
        }
      }];
    }
    case "evidence_builder": {
      const calls = [];
      if (args.includeDom) calls.push({ tool: "browser.get_dom", args: {} });
      const selectors = Array.isArray(args.selectors) ? args.selectors : [];
      if (!selectors.length) calls.push({ tool: "browser.screenshot", args: {} });
      else selectors.forEach((s) => calls.push({ tool: "browser.screenshot", args: { selector: s } }));
      return calls;
    }
    case "case_exporter": {
      const calls = [];
      if (args.includeDom) calls.push({ tool: "browser.get_dom", args: {} });
      const selectors = Array.isArray(args.selectors) ? args.selectors : [];
      if (!selectors.length) calls.push({ tool: "browser.screenshot", args: {} });
      else selectors.forEach((s) => calls.push({ tool: "browser.screenshot", args: { selector: s } }));
      return calls;
    }
    case "form_filler": {
      const calls = [];
      const fields = Array.isArray(args.fields) ? args.fields : [];
      fields.forEach((f) => {
        if (!f || !f.selector) return;
        calls.push({ tool: "browser.type", args: { selector: f.selector, text: f.value || "", clear: f.clear !== false } });
      });
      if (args.submitSelector) calls.push({ tool: "browser.click", args: { selector: args.submitSelector } });
      return calls;
    }
    case "amazon_contact_flow": {
      const calls = [];
      const durl = detailsUrlFromArgs(args);
      const autoSend = resolveAutoSend(args);
      if (durl) {
        calls.push({ tool: "browser.navigate", args: { url: durl } });
        calls.push({ tool: "browser.wait", args: { ms: 1500 } });
      }
      calls.push({ tool: "browser.click_text", args: { text: "ask product question", selector: "a,button", exact: false, timeoutMs: 12000, allowMissing: true } });
      calls.push({ tool: "browser.wait", args: { ms: 1200 } });
      calls.push({ tool: "browser.contact_flow", args: {} });
      calls.push({ tool: "browser.wait", args: { ms: 1600 } });
      calls.push({ tool: "browser.type_message", args: { text: args.message || "", autoSend } });
      return calls;
    }
    case "amazon_order_details_fetcher": {
      const calls = [];
      const durl = detailsUrlFromArgs(args);
      const autoSend = resolveAutoSend(args);
      if (durl) {
        calls.push({ tool: "browser.navigate", args: { url: durl } });
        calls.push({ tool: "browser.wait", args: { ms: 1200 } });
      }
      calls.push({
        tool: "browser.extract",
        args: {
          rootSelector: "body",
          fields: {
            asin: { selector: "#ASIN, input[name='ASIN']", attr: "value" },
            buy_price: { selector: ".a-price .a-offscreen" },
            items: { selector: ".a-fixed-left-grid, .yohtmlc-item" }
          }
        }
      });
      return calls;
    }
    case "amazon_price_checker": {
      const calls = [];
      if (args.asin) {
        const base = amazonBase(args.origin);
        calls.push({ tool: "browser.navigate", args: { url: `${base}/dp/${args.asin}` } });
      }
      calls.push({ tool: "browser.query", args: { selector: ".a-price .a-offscreen" } });
      return calls;
    }
    case "amazon_review_scraper": {
      return [{
        tool: "browser.extract",
        args: {
          rootSelector: args.reviewSelector || "[data-hook='review']",
          list: true,
          fields: {
            rating: { selector: "[data-hook='review-star-rating']" },
            title: { selector: "[data-hook='review-title']" },
            body: { selector: "[data-hook='review-body']" }
          }
        }
      }];
    }
    case "message_monitor": {
      return [{
        tool: "browser.extract",
        args: {
          rootSelector: "body",
          fields: {
            latest_message: { selector: "textarea, [contenteditable='true'], [role='textbox']" }
          }
        }
      }];
    }
    default:
      return [];
  }
}

async function executeCall(page, call, context = null, logger = null) {
  const tool = call.tool;
  const args = call.args || {};
  const logEvt = typeof logger === "function" ? logger : () => {};
  logEvt("tool.dispatch", { tool, args: compact(args) });

  if (tool === "browser.query") return { ok: true, tool, data: await toolQuery(page, args) };
  if (tool === "browser.get_dom") return { ok: true, tool, data: await toolGetDom(page, args) };
  if (tool === "browser.navigate") return { ok: true, tool, data: await toolNavigate(page, args) };
  if (tool === "browser.click") return { ok: true, tool, data: await toolClick(page, args) };
  if (tool === "browser.click_text") return { ok: true, tool, data: await toolClickText(page, args) };
  if (tool === "browser.type") return { ok: true, tool, data: await toolType(page, args) };
  if (tool === "browser.type_message") return { ok: true, tool, data: await toolTypeMessage(page, args) };
  if (tool === "browser.scroll") return { ok: true, tool, data: await toolScroll(page, args) };
  if (tool === "browser.wait") return { ok: true, tool, data: await toolWait(page, args) };
  if (tool === "browser.extract") return { ok: true, tool, data: await toolExtract(page, args) };
  if (tool === "browser.screenshot") return { ok: true, tool, data: await toolScreenshot(page, args) };
  if (tool === "browser.contact_flow") {
    const flow = await runContactFlow(page, context, true, logger);
    const data = {
      ok: Boolean(flow.ok),
      reason: flow.reason || null,
      hasInput: Boolean(flow.hasInput),
      activeSteps: Number(flow.activeSteps || 0),
      url: flow.url,
      steps: Array.isArray(flow.steps) ? flow.steps : []
    };
    return { ok: true, tool, data, page: flow.page || page };
  }
  throw new Error("tool_not_supported");
}

async function runSkill(skillName, inputText) {
  const args = safeJsonParse(inputText);
  const spec = loadSkillSpec(skillName);

  const nonBrowser = nonBrowserSkill(skillName, args);
  if (nonBrowser) return JSON.stringify(nonBrowser);

  const browserOptions = (args.browser && typeof args.browser === "object") ? args.browser : {};
  const keepOpen = browserOptions.keepOpen === true;
  const debug = browserOptions.debug !== false;
  const logEvt = createLogger(debug, `runSkill:${skillName}`);

  logEvt("start", { keepOpen, browser: compact(browserOptions), input: compact(args) });

  const launched = await launchContext(browserOptions);
  const context = launched.context;
  let page = launched.page;
  const calls = expandSkillToCalls(skillName, args, page);

  const trace = [];
  let fatalError = null;

  try {
    for (let i = 0; i < calls.length; i += 1) {
      const call = calls[i];
      logEvt("tool.start", { index: i + 1, total: calls.length, tool: call.tool, url: page.url(), args: compact(call.args || {}) });
      try {
        const result = await executeCall(page, call, context, logEvt);
        if (result && result.page) {
          page = result.page;
          logEvt("page.switch", { index: i + 1, tool: call.tool, url: page.url() });
        }
        trace.push({ tool: call.tool, ok: true, data: result.data });
        logEvt("tool.ok", { index: i + 1, tool: call.tool, url: page.url(), data: compact(result.data) });
      } catch (err) {
        const errorText = err && err.message ? err.message : String(err);
        trace.push({ tool: call.tool, ok: false, error: errorText });
        fatalError = err;
        logEvt("tool.error", { index: i + 1, tool: call.tool, url: page.url(), error: errorText });
        break;
      }
    }
  } finally {
    if (!keepOpen) {
      logEvt("context.close", { reason: "keepOpen=false" });
      await context.close().catch(() => {});
    } else {
      logEvt("context.keep_open", { url: page.url() });
    }
  }

  const output = {
    skill: spec.name || skillName,
    version: spec.version,
    description: spec.description,
    status: fatalError ? "error" : "done",
    trace
  };

  if (fatalError) {
    output.error = fatalError && fatalError.message ? fatalError.message : String(fatalError);
  }

  logEvt("finish", { status: output.status, error: output.error || null, traceSteps: trace.length });
  return JSON.stringify(output);
}

async function runFullFlow(inputText) {
  const args = safeJsonParse(inputText);
  const browserOptions = (args.browser && typeof args.browser === "object") ? args.browser : {};
  const keepOpen = browserOptions.keepOpen !== false;
  const debug = browserOptions.debug !== false;
  const logEvt = createLogger(debug, "runFullFlow");

  logEvt("start", { keepOpen, browser: compact(browserOptions), input: compact(args) });

  const launched = await launchContext(browserOptions);
  const context = launched.context;
  let page = launched.page;
  const trace = [];

  const finish = async (status, extra = {}) => {
    if (!keepOpen) {
      logEvt("context.close", { reason: "keepOpen=false" });
      await context.close().catch(() => {});
    } else {
      logEvt("context.keep_open", { url: page.url() });
    }
    logEvt("finish", { status, extra: compact(extra), traceSteps: trace.length });
    return JSON.stringify({ status, trace, ...extra });
  };

  try {
    const ordersUrl = ordersUrlFromArgs(args);
    logEvt("open_orders.start", { ordersUrl });
    await page.goto(ordersUrl, { waitUntil: "domcontentloaded" });
    trace.push({ step: "open_orders", ok: true, url: page.url() });
    logEvt("open_orders.ok", { url: page.url() });

    await wait(1500);

    logEvt("find_order_details.start", { wantedOrderId: args.order_id || args.orderId || null });
    const linkData = await page.evaluate((orderId) => {
      const visible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== "none" && s.visibility !== "hidden" && r.width > 0 && r.height > 0;
      };
      const normalize = (s) => {
        try { return decodeURIComponent(String(s || "")).toLowerCase(); } catch (_) { return String(s || "").toLowerCase(); }
      };
      const extractOrderId = (href) => {
        try {
          const u = new URL(href, window.location.href);
          return u.searchParams.get("orderID") || "";
        } catch (_) {
          return "";
        }
      };
      const links = Array.from(document.querySelectorAll("a[href*='order-details?orderID='], a[href*='/your-orders/order-details'], a[href*='orderID=']")).filter(visible);
      if (!links.length) return null;
      if (orderId) {
        const n = normalize(orderId);
        const m = links.find((a) => normalize(a.href).includes(n));
        if (m) return { href: m.href, text: (m.textContent || "").trim(), orderId: extractOrderId(m.href) };
      }
      const first = links[0];
      return { href: first.href, text: (first.textContent || "").trim(), orderId: extractOrderId(first.href) };
    }, args.order_id || args.orderId || "");

    if (!linkData || !linkData.href) {
      trace.push({ step: "find_order_details", ok: false, error: "details_link_not_found" });
      logEvt("find_order_details.error", { error: "details_link_not_found", url: page.url() });
      return finish("error", { error: "details_link_not_found" });
    }

    trace.push({
      step: "find_order_details",
      ok: true,
      href: linkData.href,
      order_id: linkData.orderId || null
    });
    logEvt("find_order_details.ok", { href: linkData.href, order_id: linkData.orderId || null });

    const marked = await page.evaluate((href) => {
      const normalize = (s) => {
        try { return decodeURIComponent(String(s || "")).toLowerCase(); } catch (_) { return String(s || "").toLowerCase(); }
      };
      const target = normalize(href);
      const links = Array.from(document.querySelectorAll("a[href*='order-details'], a[href*='orderID=']"));
      const node = links.find((a) => normalize(a.href) === target) || links.find((a) => normalize(a.href).includes(target));
      if (!node) return false;
      node.setAttribute("data-eb-target-details", "1");
      return true;
    }, linkData.href);

    let openedByClick = false;
    if (marked) {
      const beforePages = context.pages().length;
      try {
        logEvt("open_order_details.click.try", { href: linkData.href });
        await page.locator("a[data-eb-target-details='1']").first().click({ timeout: 8000 });
        await wait(1800);
        const pages = context.pages();
        const detailTab = pages.find((p) => /\/your-orders\/order-details/i.test(p.url()));
        if (detailTab) {
          page = detailTab;
          await page.bringToFront().catch(() => {});
          openedByClick = true;
        } else if (/\/your-orders\/order-details/i.test(page.url())) {
          openedByClick = true;
        } else if (pages.length > beforePages) {
          const newest = pages[pages.length - 1];
          if (newest && newest !== page) {
            page = newest;
            await page.bringToFront().catch(() => {});
          }
          if (/\/your-orders\/order-details/i.test(page.url())) {
            openedByClick = true;
          }
        }
      } catch (err) {
        logEvt("open_order_details.click.error", { error: err && err.message ? err.message : String(err) });
      }
    }

    if (!openedByClick) {
      logEvt("open_order_details.goto", { href: linkData.href });
      await page.goto(linkData.href, { waitUntil: "domcontentloaded" });
    }
    trace.push({ step: "open_order_details", ok: true, by: openedByClick ? "click" : "goto", url: page.url() });
    logEvt("open_order_details.ok", { by: openedByClick ? "click" : "goto", url: page.url() });

    await wait(1400);

    logEvt("contact_flow.start", { url: page.url() });
    const cf = await runContactFlow(page, context, true, logEvt);
    if (cf && cf.page) {
      page = cf.page;
      logEvt("contact_flow.page", { url: page.url() });
    }

    const cfTrace = {
      ok: Boolean(cf.ok),
      reason: cf.reason || null,
      hasInput: Boolean(cf.hasInput),
      activeSteps: Number(cf.activeSteps || 0),
      url: cf.url,
      steps: Array.isArray(cf.steps) ? cf.steps : []
    };
    trace.push({ step: "contact_flow", ok: Boolean(cf.ok), data: cfTrace });
    logEvt("contact_flow.end", { ok: Boolean(cf.ok), reason: cf.reason || null, hasInput: Boolean(cf.hasInput), activeSteps: Number(cf.activeSteps || 0), url: cf.url });

    if (!cf.ok) {
      throw new Error(cf.reason || "contact_flow_not_ready");
    }

    const autoSend = resolveAutoSend(args);
    logEvt("type_message.start", { auto_send_requested: args.auto_send === true, auto_send_effective: autoSend, message_len: String(args.message || "").length, url: page.url() });
    const typed = await toolTypeMessage(page, { text: args.message || "", autoSend });
    trace.push({ step: "type_message", ok: true, data: typed });
    logEvt("type_message.ok", { sent: Boolean(typed.sent), url: page.url() });

    return finish("done", { finalUrl: page.url() });
  } catch (err) {
    const errorText = err && err.message ? err.message : String(err);
    trace.push({ step: "fatal", ok: false, error: errorText });
    logEvt("fatal", { error: errorText, url: page.url() });
    return finish("error", { error: errorText });
  }
}

if (require.main === module) {
  const mode = process.argv[2] || "skill";
  const name = process.argv[3] || "";
  const input = process.argv.slice(4).join(" ");

  (async () => {
    if (mode === "full_flow") {
      const out = await runFullFlow(name || input);
      process.stdout.write(String(out));
      return;
    }

    if (!name) throw new Error("missing_skill_name");
    const out = await runSkill(name, input);
    process.stdout.write(String(out));
  })().catch((err) => {
    process.stderr.write(err && err.message ? err.message : String(err));
    process.exit(1);
  });
}

module.exports = {
  runSkill,
  runFullFlow
};


