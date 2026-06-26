"use strict";
(() => {
  // agent_demo/background/sw_helpers.ts
  async function ensureContentScript(tabId) {
    const pingResult = await pingContentScript(tabId);
    if (pingResult.ok) {
      return { ok: true };
    }
    try {
      await chrome.scripting.executeScript({
        target: { tabId },
        files: ["content/index.js"]
      });
    } catch (error) {
      return { ok: false, error: "cs_inject_failed" };
    }
    const pingAfter = await pingContentScript(tabId);
    if (!pingAfter.ok) {
      return { ok: false, error: "cs_unavailable" };
    }
    return { ok: true };
  }
  async function pingContentScript(tabId) {
    try {
      const response = await chrome.tabs.sendMessage(tabId, { type: "ping" });
      return { ok: Boolean(response?.ok) };
    } catch (error) {
      return { ok: false };
    }
  }

  // agent_demo/storage/artifacts.ts
  var DB_NAME = "agent_artifacts";
  var DB_VERSION = 1;
  var STORE_NAME = "artifacts";
  function openDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME, { keyPath: "id" });
        }
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
  function txDone(tx) {
    return new Promise((resolve, reject) => {
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error);
    });
  }
  function requestToPromise(request) {
    return new Promise((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
  function createId() {
    if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
      return crypto.randomUUID();
    }
    return `artifact_${Date.now()}_${Math.random().toString(16).slice(2)}`;
  }
  async function putArtifact(blob, meta, mimeType = blob.type || "application/octet-stream") {
    const db = await openDb();
    const tx = db.transaction(STORE_NAME, "readwrite");
    const store = tx.objectStore(STORE_NAME);
    const record = {
      id: createId(),
      createdAt: Date.now(),
      mimeType,
      blob,
      meta
    };
    const req = store.put(record);
    await Promise.all([requestToPromise(req), txDone(tx)]);
    return record.id;
  }
  async function putArtifactFromDataUrl(dataUrl, meta) {
    const response = await fetch(dataUrl);
    const blob = await response.blob();
    return putArtifact(blob, meta, blob.type || "image/png");
  }

  // agent_demo/background/agent/runtime.ts
  var ALLOWED_TOOLS = [
    "browser.query",
    "browser.get_dom",
    "browser.navigate",
    "browser.click",
    "browser.click_text",
    "browser.exec",
    "browser.type",
    "browser.type_message",
    "browser.scroll",
    "browser.wait",
    "browser.extract",
    "browser.screenshot"
  ];
  var skillsCache = null;
  function buildDemoPlan(target) {
    return [
      {
        tool: "browser.query",
        target,
        args: { selector: "body" }
      },
      {
        tool: "browser.screenshot",
        target,
        args: {}
      }
    ];
  }
  async function buildPlanForRun(input, target) {
    const config = await getAgentConfig();
    if (!config || !config.apiKey || !config.endpoint || !config.model) {
      return buildDemoPlan(target);
    }
    const skills = await loadSkillsRegistry();
    const planned = await planWithLLM(input, config, skills);
    const normalized = normalizeToolCalls(planned, target, skills);
    if (!normalized.length) {
      return buildDemoPlan(target);
    }
    return normalized;
  }
  async function getAgentConfig() {
    const result = await chrome.storage.local.get("agent_config");
    return result.agent_config || null;
  }
  async function planWithLLM(input, config, skills) {
    const skillsBlock = formatSkillsForPrompt(skills);
    const systemPrompt = `You are a browser agent planner. Return ONLY a JSON array of tool calls. Each tool call must be { tool: string, args: object }. Allowed tools: browser.query, browser.get_dom, browser.navigate, browser.click, browser.type, browser.scroll, browser.wait, browser.extract, browser.screenshot. You may also call a skill using tool name 'skill.<skill_name>'. Do not include target; it will be injected. For browser.extract you MUST use schema: { rootSelector: string, list?: boolean, fields: { [key]: { selector: string, attr?: string } } }. Example: [{"tool":"browser.extract","args":{"rootSelector":"body","fields":{"title":{"selector":"h1"}}}}]. ` + skillsBlock;
    const userPrompt = `User goal: ${input}`;
    const response = await fetch(config.endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${config.apiKey}`
      },
      body: JSON.stringify({
        model: config.model,
        temperature: config.temperature ?? 0.2,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt }
        ]
      })
    });
    if (!response.ok) {
      throw new Error(`planner_http_${response.status}`);
    }
    const data = await response.json();
    const content = data?.choices?.[0]?.message?.content;
    if (!content || typeof content !== "string") {
      return [];
    }
    try {
      const parsed = JSON.parse(content);
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }
  async function loadSkillsRegistry() {
    if (skillsCache) return skillsCache;
    try {
      const registryUrl = chrome.runtime.getURL("skills/registry.json");
      const registryRes = await fetch(registryUrl);
      const registry = await registryRes.json();
      const entries = Array.isArray(registry?.skills) ? registry.skills : [];
      const skills = [];
      for (const entry of entries) {
        if (!entry?.file) continue;
        const fileUrl = chrome.runtime.getURL(`skills/${entry.file}`);
        const res = await fetch(fileUrl);
        const data = await res.json();
        if (data?.name) skills.push(data);
      }
      skillsCache = skills;
      return skills;
    } catch (error) {
      skillsCache = [];
      return [];
    }
  }
  function formatSkillsForPrompt(skills) {
    if (!skills.length) return "";
    const lines = skills.map((skill) => {
      const inputs = skill.input_schema ? JSON.stringify(skill.input_schema) : "{}";
      const outputs = skill.output_schema ? JSON.stringify(skill.output_schema) : "{}";
      return `Skill ${skill.name}: ${skill.description || ""} Input=${inputs} Output=${outputs}`;
    });
    return ` Available skills: ${lines.join(" | ")}`;
  }
  function normalizeToolCalls(raw, target, skills) {
    const normalized = [];
    const skillNames = new Set(skills.map((s) => s.name));
    for (const call of raw) {
      if (!call || typeof call !== "object") continue;
      const tool = String(call.tool || "");
      if (tool.startsWith("skill.") || skillNames.has(tool)) {
        const skillName = tool.startsWith("skill.") ? tool.slice(6) : tool;
        const expanded = expandSkillCall(skillName, call.args || {}, target);
        normalized.push(...expanded);
        continue;
      }
      if (!ALLOWED_TOOLS.includes(tool)) continue;
      normalized.push({
        tool,
        target,
        args: call.args || {}
      });
    }
    return normalized.slice(0, 20);
  }
  function expandSkillCall(skillName, args, target) {
    switch (skillName) {
      case "amazon_orders_opener":
        const ordersArgs = { kind: "orders_page" };
        if (args?.timeFilter) ordersArgs.timeFilter = args.timeFilter;
        if (args?.year) ordersArgs.year = args.year;
        if (!ordersArgs.timeFilter && !ordersArgs.year) {
          ordersArgs.year = 2025;
        }
        return [
          {
            tool: "browser.navigate",
            target,
            args: ordersArgs
          }
        ];
      case "amazon_product_detector":
        return [
          {
            tool: "browser.extract",
            target,
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
          }
        ];
      case "amazon_orders_scraper":
        const extractCall = {
          tool: "browser.extract",
          target,
          args: {
            rootSelector: ".order-card.js-order-card, .order-card",
            list: true,
            fields: {
              order_id: { selector: "[data-order-id]", attr: "data-order-id" },
              title: { selector: ".yohtmlc-item-title, .a-link-normal" },
              price: { selector: ".a-price .a-offscreen" },
              details_url: {
                selector: "a[href*='order-details']",
                attr: "href"
              }
            }
          }
        };
        if (args?.openFirstDetails) {
          return [
            extractCall,
            {
              tool: "browser.click",
              target,
              args: { selector: "a[href*='order-details']" }
            }
          ];
        }
        return [extractCall];
      case "order_reader":
        return [
          {
            tool: "browser.extract",
            target,
            args: {
              rootSelector: args.rootSelector || ".order-card",
              fields: args.fields || {
                title: { selector: ".item-title" },
                price: { selector: ".a-price .a-offscreen" }
              }
            }
          }
        ];
      case "evidence_builder": {
        const selectors = Array.isArray(args.selectors) ? args.selectors : [];
        if (!selectors.length) {
          return [{ tool: "browser.screenshot", target, args: {} }];
        }
        return selectors.map((selector) => ({
          tool: "browser.screenshot",
          target,
          args: { selector }
        }));
      }
      case "case_exporter": {
        const selectors = Array.isArray(args.selectors) ? args.selectors : [];
        const calls = [];
        if (args.includeDom) {
          calls.push({ tool: "browser.get_dom", target, args: {} });
        }
        if (!selectors.length) {
          calls.push({ tool: "browser.screenshot", target, args: {} });
        } else {
          selectors.forEach(
            (selector) => calls.push({ tool: "browser.screenshot", target, args: { selector } })
          );
        }
        return calls;
      }
      case "form_filler": {
        const calls = [];
        const fields = Array.isArray(args.fields) ? args.fields : [];
        fields.forEach((field) => {
          if (!field?.selector) return;
          calls.push({
            tool: "browser.type",
            target,
            args: {
              selector: field.selector,
              text: field.value || "",
              clear: field.clear !== false
            }
          });
        });
        if (args.submitSelector) {
          calls.push({
            tool: "browser.click",
            target,
            args: { selector: args.submitSelector }
          });
        }
        return calls;
      }
      case "amazon_contact_flow": {
        const calls = [];
        if (args?.details_url) {
          calls.push({
            tool: "browser.navigate",
            target,
            args: { url: args.details_url }
          });
          calls.push({ tool: "browser.wait", target, args: { ms: 1500 } });
        }
        calls.push({
          tool: "browser.click_text",
          target,
          args: {
            text: "ask product question",
            selector: "a,button",
            exact: false,
            timeoutMs: 8e3,
            allowMissing: true
          }
        });
        calls.push({ tool: "browser.wait", target, args: { ms: 1200 } });
        calls.push({ tool: "browser.exec", target, args: { name: "contact_flow" } });
        calls.push({ tool: "browser.wait", target, args: { ms: 2e3 } });
        calls.push({
          tool: "browser.type_message",
          target,
          args: { text: args?.message || "", autoSend: args?.auto_send === true }
        });
        return calls;
      }
      default:
        return [];
    }
  }
  async function executeToolCall(context) {
    const { toolCall } = context;
    const tabId = toolCall.target.tabId;
    try {
      const tabExists = await chrome.tabs.get(tabId).then(() => true).catch(() => false);
      if (!tabExists) {
        return {
          ok: false,
          tool: toolCall.tool,
          tabId,
          error: "tab_closed"
        };
      }
      if (toolCall.tool === "browser.navigate") {
        const destination = await resolveNavigationTarget(tabId, toolCall.args);
        if (!destination) {
          return {
            ok: false,
            tool: toolCall.tool,
            tabId,
            error: "navigate_target_missing"
          };
        }
        await chrome.tabs.update(tabId, { url: destination, active: true });
        return {
          ok: true,
          tool: toolCall.tool,
          tabId,
          data: { url: destination }
        };
      }
      const csReady = await ensureContentScript(tabId);
      if (!csReady.ok) {
        return {
          ok: false,
          tool: toolCall.tool,
          tabId,
          error: csReady.error || "cs_unavailable"
        };
      }
      if (toolCall.tool === "browser.screenshot") {
        const toolResultMessage = await chrome.tabs.sendMessage(tabId, {
          type: "tool.call",
          callId: context.callId,
          toolCall
        });
        const baseResult = toolResultMessage?.result;
        if (!baseResult || !baseResult.ok) {
          return {
            ok: false,
            tool: toolCall.tool,
            tabId,
            error: baseResult?.error || "screenshot_preflight_failed"
          };
        }
        const tab = await chrome.tabs.get(tabId);
        const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, {
          format: "png"
        });
        const artifactId = await putArtifactFromDataUrl(dataUrl, {
          runId: context.runId,
          callId: context.callId,
          tool: toolCall.tool
        });
        return {
          ok: true,
          tool: toolCall.tool,
          tabId,
          data: {
            rect: baseResult.data?.rect || null,
            viewportCaptured: true
          },
          artifacts: { artifactId }
        };
      }
      const resultMessage = await chrome.tabs.sendMessage(tabId, {
        type: "tool.call",
        callId: context.callId,
        toolCall
      });
      if (!resultMessage || !resultMessage.result) {
        return {
          ok: false,
          tool: toolCall.tool,
          tabId,
          error: "no_tool_result"
        };
      }
      return {
        ...resultMessage.result,
        tabId
      };
    } catch (error) {
      return {
        ok: false,
        tool: toolCall.tool,
        tabId,
        error: error instanceof Error ? error.message : "tool_failed"
      };
    }
  }
  async function resolveNavigationTarget(tabId, args) {
    if (args?.url) {
      return String(args.url);
    }
    if (args?.kind === "orders_page") {
      const base = await resolveAmazonOrdersBase(tabId);
      const params = new URLSearchParams();
      if (args.timeFilter) {
        params.set("timeFilter", String(args.timeFilter));
      } else if (args.year) {
        params.set("timeFilter", `year-${String(args.year)}`);
      }
      const timeFilter = params.get("timeFilter");
      if (timeFilter) {
        const match = timeFilter.match(/year-(\d{4})/);
        if (match) {
          params.set("ref_", `ppx_yo2ov_dt_b_filter_all_y${match[1]}`);
        }
      }
      const qs = params.toString();
      const url = qs ? `${base}/your-orders/orders?${qs}` : `${base}/your-orders/orders`;
      console.log("[agent][orders] navigate:", url);
      return url;
    }
    return null;
  }
  async function resolveAmazonOrdersBase(tabId) {
    const current = await chrome.tabs.get(tabId).catch(() => null);
    const base = getAmazonBaseFromUrl(current?.url || "");
    if (base) return base;
    const tabs = await chrome.tabs.query({});
    for (const tab of tabs) {
      const tabBase = getAmazonBaseFromUrl(tab.url || "");
      if (tabBase) return tabBase;
    }
    return "https://www.amazon.com";
  }
  function getAmazonBaseFromUrl(url) {
    try {
      const u = new URL(url);
      if (!/(^|\.)amazon\./i.test(u.hostname)) return null;
      return `${u.protocol}//${u.host}`;
    } catch (_) {
      return null;
    }
  }

  // agent_demo/storage/runs.ts
  var RUN_PREFIX = "agent_run:";
  function keyFor(runId) {
    return `${RUN_PREFIX}${runId}`;
  }
  async function saveRunState(state) {
    state.updatedAt = Date.now();
    await chrome.storage.local.set({ [keyFor(state.runId)]: state });
  }
  async function getRunState(runId) {
    const result = await chrome.storage.local.get(keyFor(runId));
    return result[keyFor(runId)] || null;
  }
  async function listRuns() {
    const result = await chrome.storage.local.get(null);
    return Object.keys(result).filter((key) => key.startsWith(RUN_PREFIX)).map((key) => result[key]);
  }
  async function appendTraceEntry(runId, entry) {
    const state = await getRunState(runId);
    if (!state) return null;
    state.trace.push(entry);
    await saveRunState(state);
    return state;
  }

  // agent_demo/background/sw.ts
  var pendingCalls = /* @__PURE__ */ new Map();
  function createCallId() {
    return `call_${Date.now()}_${Math.random().toString(16).slice(2)}`;
  }
  function sendToPanel(message) {
    chrome.runtime.sendMessage(message).catch(() => {
    });
  }
  async function createRun(request) {
    const plan = await buildPlanForRun(request.input, request.target);
    if (!plan.length) {
      throw new Error("empty_plan");
    }
    const state = {
      runId: request.runId,
      target: request.target,
      input: request.input,
      plan,
      stepIndex: 0,
      status: "idle",
      trace: [],
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    await saveRunState(state);
    return state;
  }
  async function requestConfirm(state, toolCall) {
    const callId = createCallId();
    pendingCalls.set(callId, { runId: state.runId, toolCall });
    state.status = "waiting_confirm";
    state.pendingCallId = callId;
    state.pendingToolCall = toolCall;
    await saveRunState(state);
    sendToPanel({
      type: "agent.request_confirm",
      runId: state.runId,
      callId,
      toolCall
    });
  }
  async function handleConfirm(message) {
    const { callId, approved, runId } = message;
    let pending = pendingCalls.get(callId);
    if (!pending) {
      const state2 = await getRunState(runId);
      if (state2?.pendingCallId === callId && state2.pendingToolCall) {
        pending = { runId, toolCall: state2.pendingToolCall };
        pendingCalls.set(callId, pending);
      }
    }
    if (!pending) {
      sendToPanel({
        type: "agent.error",
        runId,
        callId,
        error: "pending_call_not_found"
      });
      return;
    }
    const state = await getRunState(pending.runId);
    if (!state) {
      sendToPanel({
        type: "agent.error",
        runId,
        callId,
        error: "run_not_found"
      });
      return;
    }
    if (!approved) {
      pendingCalls.delete(callId);
      state.status = "error";
      await saveRunState(state);
      sendToPanel({
        type: "agent.error",
        runId,
        callId,
        error: "user_rejected"
      });
      return;
    }
    pendingCalls.delete(callId);
    state.status = "running";
    await saveRunState(state);
    const callTrace = {
      runId: state.runId,
      callId,
      ts: Date.now(),
      tool: pending.toolCall.tool,
      args: pending.toolCall.args
    };
    await appendTraceEntry(state.runId, callTrace);
    const result = await executeToolCall({
      runId: state.runId,
      callId,
      toolCall: pending.toolCall
    });
    const resultTrace = {
      runId: state.runId,
      callId,
      ts: Date.now(),
      tool: pending.toolCall.tool,
      args: pending.toolCall.args,
      ok: result.ok,
      error: result.error,
      artifacts: result.artifacts
    };
    await appendTraceEntry(state.runId, resultTrace);
    sendToPanel({
      type: "agent.tool_result",
      runId: state.runId,
      callId,
      result
    });
    if (!result.ok) {
      state.status = "error";
      await saveRunState(state);
      sendToPanel({
        type: "agent.error",
        runId: state.runId,
        callId,
        error: result.error || "tool_failed"
      });
      return;
    }
    state.stepIndex += 1;
    state.pendingCallId = void 0;
    state.pendingToolCall = void 0;
    if (state.stepIndex >= state.plan.length) {
      state.status = "done";
      await saveRunState(state);
      sendToPanel({ type: "agent.done", runId: state.runId });
      return;
    }
    const nextTool = state.plan[state.stepIndex];
    await requestConfirm(state, nextTool);
  }
  chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {
      if (message?.type === "agent.run") {
        createRun(message).then((state) => requestConfirm(state, state.plan[state.stepIndex])).then(() => sendResponse({ ok: true })).catch((error) => {
          const err = error?.message || "run_failed";
          sendToPanel({
            type: "agent.error",
            runId: message.runId,
            error: err
          });
          sendResponse({ ok: false, error: err });
        });
        return true;
      }
      if (message?.type === "agent.confirm") {
        handleConfirm(message).then(() => sendResponse({ ok: true })).catch(
          (error) => sendResponse({ ok: false, error: error?.message || "confirm_failed" })
        );
        return true;
      }
      return false;
    }
  );
  async function recoverRuns() {
    const runs = await listRuns();
    for (const run of runs) {
      if (run.status === "waiting_confirm" && run.pendingCallId && run.pendingToolCall) {
        pendingCalls.set(run.pendingCallId, {
          runId: run.runId,
          toolCall: run.pendingToolCall
        });
      }
    }
  }
  recoverRuns().catch(() => {
  });
})();
