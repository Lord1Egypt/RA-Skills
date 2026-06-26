"use strict";
(() => {
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
  async function getArtifact(id) {
    const db = await openDb();
    const tx = db.transaction(STORE_NAME, "readonly");
    const store = tx.objectStore(STORE_NAME);
    const req = store.get(id);
    const result = await Promise.all([requestToPromise(req), txDone(tx)]);
    return result[0] || null;
  }

  // agent_demo/panel/panel.ts
  var runButton = document.getElementById("runDemo");
  var runAiButton = document.getElementById("runAi");
  var confirmBar = document.getElementById("confirmBar");
  var confirmText = document.getElementById("confirmText");
  var approveButton = document.getElementById("approve");
  var rejectButton = document.getElementById("reject");
  var traceEl = document.getElementById("trace");
  var previewSection = document.getElementById("previewSection");
  var previewImg = document.getElementById("previewImg");
  var previewMeta = document.getElementById("previewMeta");
  var extractSection = document.getElementById("extractSection");
  var extractText = document.getElementById("extractText");
  var cfgEndpoint = document.getElementById("cfgEndpoint");
  var cfgModel = document.getElementById("cfgModel");
  var cfgApiKey = document.getElementById("cfgApiKey");
  var saveConfigButton = document.getElementById("saveConfig");
  var promptInput = document.getElementById("promptInput");
  var pendingConfirm = null;
  var previewUrl = null;
  function appendTrace(entry) {
    const line = JSON.stringify(entry, null, 2);
    traceEl.textContent += `${line}

`;
    traceEl.scrollTop = traceEl.scrollHeight;
  }
  function showConfirm(message) {
    pendingConfirm = { runId: message.runId, callId: message.callId };
    confirmText.textContent = JSON.stringify(message.toolCall, null, 2);
    confirmBar.style.display = "block";
  }
  function hideConfirm() {
    pendingConfirm = null;
    confirmBar.style.display = "none";
  }
  function showExtractResult(data) {
    extractText.textContent = JSON.stringify(data, null, 2);
    extractSection.style.display = "block";
  }
  async function showArtifactPreview(artifactId) {
    const record = await getArtifact(artifactId);
    if (!record) {
      appendTrace({ error: "artifact_not_found", artifactId });
      return;
    }
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    previewUrl = URL.createObjectURL(record.blob);
    previewImg.src = previewUrl;
    previewMeta.textContent = `artifactId: ${artifactId}`;
    previewSection.style.display = "block";
  }
  async function syncPendingConfirm() {
    const all = await chrome.storage.local.get(null);
    const pendingKeys = Object.keys(all).filter((key) => key.startsWith("agent_run:"));
    for (const key of pendingKeys) {
      const state = all[key];
      if (state?.status === "waiting_confirm" && state?.pendingCallId && state?.pendingToolCall) {
        const pendingMessage = {
          type: "agent.request_confirm",
          runId: state.runId,
          callId: state.pendingCallId,
          toolCall: state.pendingToolCall
        };
        appendTrace({ ...pendingMessage, recovered: true });
        showConfirm(pendingMessage);
        return;
      }
    }
  }
  async function loadConfig() {
    const result = await chrome.storage.local.get("agent_config");
    const config = result.agent_config || {};
    cfgEndpoint.value = config.endpoint || "https://api.openai.com/v1/chat/completions";
    cfgModel.value = config.model || "gpt-4o-mini";
    cfgApiKey.value = config.apiKey || "";
  }
  async function saveConfig() {
    const config = {
      endpoint: cfgEndpoint.value.trim(),
      model: cfgModel.value.trim(),
      apiKey: cfgApiKey.value.trim()
    };
    await chrome.storage.local.set({ agent_config: config });
    appendTrace({ type: "config.saved", config: { ...config, apiKey: config.apiKey ? "***" : "" } });
  }
  runButton.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    if (!tab?.id) {
      appendTrace({ error: "no_active_tab" });
      return;
    }
    const runId = `run_${Date.now()}`;
    const request = {
      type: "agent.run",
      runId,
      input: "demo",
      target: { tabId: tab.id }
    };
    appendTrace({ type: "agent.run", runId, tabId: tab.id });
    await chrome.runtime.sendMessage(request);
  });
  runAiButton.addEventListener("click", async () => {
    const prompt = promptInput.value.trim();
    if (!prompt) {
      appendTrace({ error: "empty_prompt" });
      return;
    }
    const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    if (!tab?.id) {
      appendTrace({ error: "no_active_tab" });
      return;
    }
    const runId = `run_${Date.now()}`;
    const request = {
      type: "agent.run",
      runId,
      input: prompt,
      target: { tabId: tab.id }
    };
    appendTrace({ type: "agent.run", runId, tabId: tab.id, prompt });
    await chrome.runtime.sendMessage(request);
  });
  saveConfigButton.addEventListener("click", async () => {
    await saveConfig();
  });
  approveButton.addEventListener("click", async () => {
    if (!pendingConfirm) return;
    const payload = {
      type: "agent.confirm",
      runId: pendingConfirm.runId,
      callId: pendingConfirm.callId,
      approved: true
    };
    await chrome.runtime.sendMessage(payload);
    hideConfirm();
  });
  rejectButton.addEventListener("click", async () => {
    if (!pendingConfirm) return;
    const payload = {
      type: "agent.confirm",
      runId: pendingConfirm.runId,
      callId: pendingConfirm.callId,
      approved: false
    };
    await chrome.runtime.sendMessage(payload);
    hideConfirm();
  });
  chrome.runtime.onMessage.addListener((message) => {
    if (message?.type === "agent.request_confirm") {
      appendTrace(message);
      showConfirm(message);
      return;
    }
    if (message?.type === "agent.tool_result") {
      appendTrace(message);
      if (message?.result?.tool === "browser.extract") {
        showExtractResult(message.result.data);
      }
      const artifactId = message?.result?.artifacts?.artifactId;
      if (artifactId) {
        showArtifactPreview(artifactId).catch(() => {
          appendTrace({ error: "preview_failed", artifactId });
        });
      }
      return;
    }
    if (message?.type === "agent.done") {
      appendTrace(message);
      return;
    }
    if (message?.type === "agent.error") {
      appendTrace(message);
      return;
    }
  });
  syncPendingConfirm().catch(() => {
  });
  chrome.storage.onChanged.addListener(() => {
    syncPendingConfirm().catch(() => {
    });
  });
  loadConfig().catch(() => {
  });
})();
