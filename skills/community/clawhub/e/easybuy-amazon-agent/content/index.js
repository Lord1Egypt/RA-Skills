"use strict";
(() => {
  // agent_demo/content/index.ts
  function okResult(tool, tabId, data) {
    return { ok: true, tool, tabId, data };
  }
  function errResult(tool, tabId, error) {
    return { ok: false, tool, tabId, error };
  }
  function textOf(node) {
    if (!node) return null;
    const text = node.textContent || "";
    return text.trim();
  }
  function attrOf(node, attr) {
    if (!node) return null;
    if (!attr) return textOf(node);
    return node.getAttribute(attr);
  }
  function isVisible(el) {
    if (!el) return false;
    const win = el.ownerDocument?.defaultView || window;
    const style = win.getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden" || style.opacity === "0") {
      return false;
    }
    const rect = el.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) return true;
    return el.getClientRects().length > 0;
  }
  function collectNodes(selector) {
    const nodes = Array.from(document.querySelectorAll(selector));
    const frames = Array.from(document.querySelectorAll("iframe"));
    frames.forEach((frame) => {
      try {
        const doc = frame.contentDocument;
        if (!doc) return;
        nodes.push(...Array.from(doc.querySelectorAll(selector)));
      } catch (_) {
      }
    });
    return nodes;
  }
  async function runContactFlow() {
    const logs = [];
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    function log(step, extra = {}) {
      const row = { step, t: Date.now(), url: location.href, ...extra };
      logs.push(row);
      console.log("[agent][contactFlow]", row);
    }
    function isVisibleLocal(el) {
      if (!el) return false;
      const style = getComputedStyle(el);
      return style.display !== "none" && style.visibility !== "hidden" && el.offsetParent !== null;
    }
    async function waitUntil(fn, timeout = 12e3, interval = 350, label = "waitUntil") {
      const start = Date.now();
      while (Date.now() - start < timeout) {
        try {
          const res = fn();
          if (res) return res;
        } catch (_) {
        }
        await sleep(interval);
      }
      log(label, { ok: false, error: "timeout" });
      return null;
    }
    async function clickEl(el, label) {
      if (!el) return false;
      try {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        await sleep(200);
        el.dispatchEvent(
          new MouseEvent("click", { bubbles: true, cancelable: true, view: window })
        );
        log(label, { ok: true, html: el.outerHTML?.slice(0, 200) || "" });
        return true;
      } catch (e) {
        log(label, { ok: false, error: e?.message || "click_failed" });
        return false;
      }
    }
    async function clickSelectCard() {
      log("Step Select: searching...");
      const el = await waitUntil(() => {
        const footers = Array.from(
          document.querySelectorAll(".smartcs-card-carousel a .card-footer")
        ).filter(isVisibleLocal);
        const footer = footers.find(
          (x) => (x.textContent || "").trim().toLowerCase().includes("select")
        );
        if (footer) return footer;
        const candidates = Array.from(document.querySelectorAll("a,button,span,div")).filter(
          isVisibleLocal
        );
        return candidates.find((x) => (x.textContent || "").trim().toLowerCase() === "select") || null;
      }, 2e4, 350, "Wait Select");
      if (!el) return false;
      return clickEl(el, "Step Select: click");
    }
    async function clickSmartcsButtonExact(text) {
      const target = text.trim().toLowerCase();
      log(`Step ${text}: searching...`);
      const el = await waitUntil(() => {
        const all = Array.from(document.querySelectorAll("li.smartcs-buttons-button")).filter(
          isVisibleLocal
        );
        return all.find((li) => (li.textContent || "").trim().toLowerCase() === target) || null;
      }, 2e4, 350, `Wait ${text}`);
      if (!el) return false;
      return clickEl(el, `Step ${text}: click`);
    }
    async function clickTakeMeToConversationIfExists() {
      log("Step Take me to conversation: searching...");
      const el = await waitUntil(() => {
        const candidates = Array.from(document.querySelectorAll("a,button,span,div")).filter(
          isVisibleLocal
        );
        return candidates.find((x) => {
          const t = (x.textContent || "").trim().toLowerCase();
          return t.includes("take me to the conversation");
        }) || null;
      }, 2e4, 350, "Wait take me to conversation");
      if (!el) return false;
      return clickEl(el, "Step take me to conversation: click");
    }
    async function run() {
      log("Start contact flow");
      try {
        await clickSelectCard();
        await sleep(1500);
        await clickSmartcsButtonExact("Other");
        await sleep(1500);
        await clickSmartcsButtonExact("Return policy");
        await sleep(1500);
        await clickTakeMeToConversationIfExists();
        await sleep(800);
        log("Contact flow done (click-only)", { ok: true });
        return { ok: true, steps: logs };
      } catch (e) {
        log("Contact flow crashed", { ok: false, error: e?.message || "crash" });
        return { ok: false, steps: logs, error: e?.message || "crash" };
      }
    }
    return run();
  }
  async function handleExtract(schema) {
    const roots = schema.list ? Array.from(document.querySelectorAll(schema.rootSelector)) : [document.querySelector(schema.rootSelector)].filter(Boolean);
    const mapFields = (root) => {
      const item = {};
      for (const [key, field] of Object.entries(schema.fields)) {
        const node = root?.querySelector(field.selector) || null;
        item[key] = attrOf(node, field.attr);
      }
      return item;
    };
    if (schema.list) {
      return { items: roots.map((root) => mapFields(root)) };
    }
    return { item: mapFields(roots[0]) };
  }
  async function handleToolCall(toolCallMessage) {
    const { toolCall, callId } = toolCallMessage;
    const tabId = toolCall.target?.tabId ?? -1;
    try {
      switch (toolCall.tool) {
        case "browser.ping":
          return { type: "tool.result", callId, result: okResult("browser.ping", tabId) };
        case "browser.query": {
          const selector = toolCall.args?.selector;
          if (!selector) {
            return { type: "tool.result", callId, result: errResult("browser.query", tabId, "missing_selector") };
          }
          const nodes = Array.from(document.querySelectorAll(selector));
          const preview = nodes[0]?.textContent?.trim().slice(0, 160) || "";
          return {
            type: "tool.result",
            callId,
            result: okResult("browser.query", tabId, {
              selector,
              count: nodes.length,
              preview
            })
          };
        }
        case "browser.get_dom": {
          const selector = toolCall.args?.selector;
          const limit = Number(toolCall.args?.limit || 5e3);
          const node = selector ? document.querySelector(selector) : document.documentElement;
          const html = node ? node.outerHTML.slice(0, limit) : "";
          return { type: "tool.result", callId, result: okResult("browser.get_dom", tabId, { html }) };
        }
        case "browser.click": {
          const selector = toolCall.args?.selector;
          const allowMissing = Boolean(toolCall.args?.allowMissing ?? false);
          const node = selector ? document.querySelector(selector) : null;
          if (!node) {
            if (allowMissing) {
              return {
                type: "tool.result",
                callId,
                result: okResult("browser.click", tabId, { selector, skipped: true })
              };
            }
            return { type: "tool.result", callId, result: errResult("browser.click", tabId, "element_not_found") };
          }
          node.click();
          return { type: "tool.result", callId, result: okResult("browser.click", tabId, { selector }) };
        }
        case "browser.click_text": {
          const text = String(toolCall.args?.text || "").trim();
          const selector = toolCall.args?.selector || "a,button,span,div,li";
          const exact = Boolean(toolCall.args?.exact ?? false);
          const timeoutMs = Number(toolCall.args?.timeoutMs || 8e3);
          const intervalMs = Number(toolCall.args?.intervalMs || 300);
          const allowMissing = Boolean(toolCall.args?.allowMissing ?? false);
          if (!text) {
            return { type: "tool.result", callId, result: errResult("browser.click_text", tabId, "missing_text") };
          }
          const targetText = text.toLowerCase();
          const start = Date.now();
          while (Date.now() - start < timeoutMs) {
            const nodes = collectNodes(selector).filter(isVisible);
            const found = nodes.find((node) => {
              const text2 = (node.textContent || "").trim();
              const aria = (node.getAttribute("aria-label") || "").trim();
              const title = (node.getAttribute("title") || "").trim();
              let value = "";
              if (node instanceof HTMLInputElement || node instanceof HTMLButtonElement) {
                value = (node.value || "").trim();
              }
              const candidates = [text2, aria, title, value].filter(Boolean).map((s) => s.toLowerCase());
              if (!candidates.length) return false;
              return exact ? candidates.some((s) => s === targetText) : candidates.some((s) => s.includes(targetText));
            });
            if (found) {
              found.scrollIntoView({ block: "center", inline: "center" });
              found.click();
              return {
                type: "tool.result",
                callId,
                result: okResult("browser.click_text", tabId, { selector, text })
              };
            }
            await new Promise((resolve) => setTimeout(resolve, intervalMs));
          }
          if (allowMissing) {
            return {
              type: "tool.result",
              callId,
              result: okResult("browser.click_text", tabId, { selector, text, skipped: true })
            };
          }
          return { type: "tool.result", callId, result: errResult("browser.click_text", tabId, "text_not_found") };
        }
        case "browser.exec": {
          const name = String(toolCall.args?.name || "").trim();
          if (name === "contact_flow") {
            const data = await runContactFlow();
            return { type: "tool.result", callId, result: okResult("browser.exec", tabId, data) };
          }
          return { type: "tool.result", callId, result: errResult("browser.exec", tabId, "unknown_exec") };
        }
        case "browser.type": {
          const selector = toolCall.args?.selector;
          const text = toolCall.args?.text ?? "";
          const clear = Boolean(toolCall.args?.clear ?? true);
          const input = selector ? document.querySelector(selector) : null;
          if (!input || !input.focus) {
            return { type: "tool.result", callId, result: errResult("browser.type", tabId, "element_not_found") };
          }
          const element = input;
          element.focus();
          if (clear) element.value = "";
          element.value = `${element.value}${text}`;
          element.dispatchEvent(new Event("input", { bubbles: true }));
          element.dispatchEvent(new Event("change", { bubbles: true }));
          return { type: "tool.result", callId, result: okResult("browser.type", tabId, { selector }) };
        }
        case "browser.type_message": {
          const text = String(toolCall.args?.text ?? "");
          const autoSend = Boolean(toolCall.args?.autoSend ?? false);
          const inputs = Array.from(
            document.querySelectorAll("textarea, [contenteditable='true'], [role='textbox']")
          ).filter(isVisible);
          const input = inputs[0] || null;
          if (!input) {
            return { type: "tool.result", callId, result: errResult("browser.type_message", tabId, "input_not_found") };
          }
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
            const form = input.closest?.("form") || null;
            const sendSelectors = [
              'button[type="submit"]',
              'input[type="submit"]',
              'button[aria-label*="Send"]',
              'button[aria-label*="send"]'
            ];
            let sendBtn = null;
            if (form) {
              for (const sel of sendSelectors) {
                const candidate = form.querySelector(sel);
                if (candidate && isVisible(candidate)) {
                  sendBtn = candidate;
                  break;
                }
              }
            }
            if (!sendBtn) {
              const candidates = Array.from(
                document.querySelectorAll("button, input[type='submit']")
              ).filter(isVisible);
              sendBtn = candidates.find((node) => {
                const label = (node.getAttribute("aria-label") || "").toLowerCase();
                if (label.includes("send")) return true;
                const t = (node.textContent || "").trim().toLowerCase();
                if (t === "send" || t.includes("send message")) return true;
                const title = (node.getAttribute("title") || "").toLowerCase();
                return title.includes("send");
              }) || null;
            }
            if (sendBtn) {
              sendBtn.click();
              sent = true;
            }
          }
          return {
            type: "tool.result",
            callId,
            result: okResult("browser.type_message", tabId, { sent })
          };
        }
        case "browser.scroll": {
          const selector = toolCall.args?.selector;
          if (selector) {
            const node = document.querySelector(selector);
            if (!node) {
              return { type: "tool.result", callId, result: errResult("browser.scroll", tabId, "element_not_found") };
            }
            node.scrollIntoView({ block: "center", inline: "center" });
          } else {
            const top = Number(toolCall.args?.top || 0);
            window.scrollBy({ top, behavior: "smooth" });
          }
          return { type: "tool.result", callId, result: okResult("browser.scroll", tabId) };
        }
        case "browser.wait": {
          const ms = Number(toolCall.args?.ms || 500);
          await new Promise((resolve) => setTimeout(resolve, ms));
          return { type: "tool.result", callId, result: okResult("browser.wait", tabId, { ms }) };
        }
        case "browser.extract": {
          const schema = toolCall.args;
          if (!schema?.rootSelector || !schema?.fields) {
            return { type: "tool.result", callId, result: errResult("browser.extract", tabId, "invalid_schema") };
          }
          const data = await handleExtract(schema);
          return { type: "tool.result", callId, result: okResult("browser.extract", tabId, data) };
        }
        case "browser.screenshot": {
          const selector = toolCall.args?.selector;
          if (selector) {
            const node = document.querySelector(selector);
            if (!node) {
              return { type: "tool.result", callId, result: errResult("browser.screenshot", tabId, "element_not_found") };
            }
            node.scrollIntoView({ block: "center", inline: "center" });
            const rect = node.getBoundingClientRect();
            return {
              type: "tool.result",
              callId,
              result: okResult("browser.screenshot", tabId, {
                rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
              })
            };
          }
          return {
            type: "tool.result",
            callId,
            result: okResult("browser.screenshot", tabId, { rect: null })
          };
        }
        default:
          return { type: "tool.result", callId, result: errResult(toolCall.tool, tabId, "tool_not_supported") };
      }
    } catch (error) {
      return {
        type: "tool.result",
        callId,
        result: errResult(toolCall.tool, tabId, error instanceof Error ? error.message : "tool_failed")
      };
    }
  }
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message?.type === "ping") {
      sendResponse({ ok: true });
      return false;
    }
    if (message?.type === "tool.call") {
      handleToolCall(message).then((result) => sendResponse(result)).catch((error) => {
        sendResponse({
          type: "tool.result",
          callId: message.callId,
          result: errResult(message.toolCall.tool, message.toolCall.target?.tabId ?? -1, String(error))
        });
      });
      return true;
    }
    return false;
  });
})();
