const MODEL_WINDOWS = {
  // Claude
  "claude-opus-4-6": 2e5,
  "claude-sonnet-4-6": 2e5,
  "claude-haiku-4-5": 2e5,
  "claude-3-5-sonnet": 2e5,
  "claude-3-haiku": 2e5,
  // OpenAI
  "gpt-4o": 128e3,
  "gpt-4o-mini": 128e3,
  "gpt-4-turbo": 128e3,
  "gpt-4": 8192,
  "gpt-3.5-turbo": 16384,
  "o1": 2e5,
  "o1-mini": 128e3,
  "o3": 2e5,
  "o3-mini": 2e5,
  "o4-mini": 2e5,
  // Ollama / 本地模型（保守估计）
  "llama3": 8192,
  "llama3.1": 131072,
  "llama3.2": 131072,
  "mistral": 32768,
  "mixtral": 32768,
  "qwen2": 32768,
  "qwen2.5": 131072,
  "deepseek-v2": 128e3,
  "deepseek-v3": 128e3,
  "deepseek-r1": 128e3,
  "gemma2": 8192,
  "phi3": 4096,
  "phi4": 16384,
  // 国产
  "glm-4": 128e3,
  "glm-4-flash": 128e3,
  "qwen-turbo": 131072,
  "qwen-plus": 131072,
  "qwen-max": 32768,
  "doubao-seed": 32768,
  "moonshot-v1-128k": 128e3,
  "moonshot-v1-32k": 32768,
  "moonshot-v1-8k": 8192,
  "yi-large": 32768,
  "ernie-4.0": 8192
};
let _cachedWindow = null;
function getContextWindow() {
  if (_cachedWindow !== null) return _cachedWindow;
  try {
    const { DATA_DIR, loadJson } = require("./persistence.ts");
    const { resolve } = require("path");
    const config = loadJson(resolve(DATA_DIR, "ai_config.json"), {});
    if (config.context_window && config.context_window > 0) {
      _cachedWindow = config.context_window;
      return _cachedWindow;
    }
    const modelName = config.api_model || "";
    if (modelName) {
      if (MODEL_WINDOWS[modelName]) {
        _cachedWindow = MODEL_WINDOWS[modelName];
        return _cachedWindow;
      }
      for (const [key, window] of Object.entries(MODEL_WINDOWS)) {
        if (modelName.includes(key) || key.includes(modelName.split("/").pop() || "")) {
          _cachedWindow = window;
          return _cachedWindow;
        }
      }
    }
  } catch {
  }
  try {
    const { existsSync, readFileSync } = require("fs");
    const { homedir } = require("os");
    const { resolve } = require("path");
    const configPath = resolve(homedir(), ".openclaw/openclaw.json");
    if (existsSync(configPath)) {
      const raw = JSON.parse(readFileSync(configPath, "utf-8"));
      const modelRef = raw?.agents?.defaults?.model?.primary || "";
      if (modelRef) {
        const modelId = modelRef.split("/").pop() || "";
        for (const [key, window] of Object.entries(MODEL_WINDOWS)) {
          if (modelId.includes(key) || key.includes(modelId)) {
            _cachedWindow = window;
            return _cachedWindow;
          }
        }
      }
    }
  } catch {
  }
  _cachedWindow = 32768;
  return _cachedWindow;
}
function setContextWindow(tokens) {
  _cachedWindow = tokens;
}
function resetContextWindowCache() {
  _cachedWindow = null;
}
const STRATEGIES = {
  extreme: { maxWindow: 4096, augmentRatio: 0.15, historyRatio: 0.3, outputReserve: 512, tokensPerTurn: 150 },
  aggressive: { maxWindow: 8192, augmentRatio: 0.2, historyRatio: 0.4, outputReserve: 800, tokensPerTurn: 200 },
  light: { maxWindow: 32768, augmentRatio: 0.25, historyRatio: 0.4, outputReserve: 1500, tokensPerTurn: 250 },
  none: { maxWindow: Infinity, augmentRatio: 0.3, historyRatio: 0.4, outputReserve: 2e3, tokensPerTurn: 300 }
};
function computeBudget(contextWindow) {
  const totalWindow = contextWindow ?? getContextWindow();
  const systemPromptTokens = 500;
  let strategy;
  let tier;
  if (totalWindow <= 4096) {
    strategy = STRATEGIES.extreme;
    tier = "extreme";
  } else if (totalWindow <= 8192) {
    strategy = STRATEGIES.aggressive;
    tier = "aggressive";
  } else if (totalWindow <= 32768) {
    strategy = STRATEGIES.light;
    tier = "light";
  } else {
    strategy = STRATEGIES.none;
    tier = "none";
  }
  const available = Math.max(0, totalWindow - systemPromptTokens - strategy.outputReserve);
  const augmentBudget = Math.floor(available * strategy.augmentRatio * _budgetFactor);
  const historyBudget = Math.floor(available * strategy.historyRatio);
  const historyTurns = Math.max(1, Math.floor(historyBudget / strategy.tokensPerTurn));
  return {
    totalWindow,
    systemPrompt: systemPromptTokens,
    outputReserve: strategy.outputReserve,
    available,
    augmentBudget,
    historyBudget,
    historyTurns,
    compressionTier: tier
  };
}
function getAugmentCompressionConfig(budget) {
  switch (budget.compressionTier) {
    case "extreme":
      return {
        maxAugments: 3,
        forceCompression: "compressed_fact",
        skipTypes: ["\u4E3E\u4E00\u53CD\u4E09", "\u9884\u6D4B", "\u60C5\u7EEA\u5916\u663E", "\u601D\u7EF4\u76F2\u70B9", "\u6210\u957F\u611F\u77E5", "\u77E5\u8BC6\u8870\u51CF"],
        maxAugmentTokens: 100
      };
    case "aggressive":
      return {
        maxAugments: 5,
        forceCompression: "summary",
        skipTypes: ["\u601D\u7EF4\u76F2\u70B9", "\u6210\u957F\u611F\u77E5"],
        maxAugmentTokens: 200
      };
    case "light":
      return {
        maxAugments: 12,
        forceCompression: null,
        skipTypes: [],
        maxAugmentTokens: 500
      };
    case "none":
      return {
        maxAugments: 25,
        forceCompression: null,
        skipTypes: [],
        maxAugmentTokens: 1e3
      };
  }
}
function trimHistory(history, budget) {
  if (history.length === 0) return history;
  if (history.length <= budget.historyTurns) {
    return applyPerTurnLimits(history, budget);
  }
  const maxTurns = budget.historyTurns;
  switch (budget.compressionTier) {
    case "extreme": {
      const first = history[0];
      const recent = history.slice(-(maxTurns - 1));
      return applyPerTurnLimits([
        { ...first, user: first.user.slice(0, 200), assistant: first.assistant.slice(0, 200) },
        ...recent
      ], budget);
    }
    case "aggressive": {
      return applyPerTurnLimits(history.slice(-maxTurns), budget);
    }
    default: {
      return history.slice(-maxTurns);
    }
  }
}
function applyPerTurnLimits(turns, budget) {
  const limits = {
    extreme: { user: 200, assistant: 300 },
    aggressive: { user: 400, assistant: 600 },
    light: { user: 800, assistant: 1200 },
    none: { user: 2e3, assistant: 4e3 }
  };
  const limit = limits[budget.compressionTier];
  return turns.map((t) => ({
    user: t.user.slice(0, limit.user),
    assistant: t.assistant.slice(0, limit.assistant),
    ts: t.ts
  }));
}
let _budgetFactor = 1;
let _overBudgetCount = 0;
let _qualityDropCount = 0;
function recordBudgetUsage(actualTokens, budgetTokens) {
  const ratio = budgetTokens > 0 ? actualTokens / budgetTokens : 0;
  if (ratio > 0.9) {
    _overBudgetCount++;
    if (_overBudgetCount >= 3) {
      _budgetFactor = Math.max(0.5, _budgetFactor * 0.85);
      _overBudgetCount = 0;
      console.log(`[cc-soul][budget] tightened: factor=${_budgetFactor.toFixed(2)} (3\xD7 over 90%)`);
    }
  } else {
    _overBudgetCount = Math.max(0, _overBudgetCount - 1);
  }
}
function recordBudgetQuality(qualityScore) {
  if (qualityScore < 4 && _budgetFactor < 1) {
    _qualityDropCount++;
    if (_qualityDropCount >= 3) {
      _budgetFactor = Math.min(1, _budgetFactor * 1.1);
      _qualityDropCount = 0;
      console.log(`[cc-soul][budget] relaxed: factor=${_budgetFactor.toFixed(2)} (3\xD7 quality < 4)`);
    }
  } else {
    _qualityDropCount = Math.max(0, _qualityDropCount - 1);
  }
}
function getBudgetDiagnostic() {
  const b = computeBudget();
  return [
    `[context-budget] window=${b.totalWindow}, tier=${b.compressionTier}`,
    `  available=${b.available} (augment=${b.augmentBudget}, history=${b.historyBudget})`,
    `  historyTurns=${b.historyTurns}, reserve=${b.outputReserve}`
  ].join("\n");
}
export {
  computeBudget,
  getAugmentCompressionConfig,
  getBudgetDiagnostic,
  getContextWindow,
  recordBudgetQuality,
  recordBudgetUsage,
  resetContextWindowCache,
  setContextWindow,
  trimHistory
};
