const HOSTED_API_BASE_URL = "https://claw-temp.nydhfc.cn";
const STORAGE_KEY = "openclaw-temperature-api-key";
const SKILL_VERSION = "openclaw-temperature.skill.v1";

const DEFAULT_EVENT_MAP = {
  task_success: "celebration",
  task_blocked: "encouragement",
  user_frustration: "empathy",
  user_delight: "playful"
};

const EVENT_CLASSIFIERS = [
  {
    eventType: "task_blocked",
    emotionalFamily: "encouragement",
    confidence: 0.82,
    reason: "task_blocked_signal",
    patterns: [
      /没有安装|未安装|没装|找不到|缺少|不存在|无法访问|权限不足|连接失败|超时|报错|错误|异常|失败|卡住|blocked|missing|not found|permission denied|timeout|cannot|can't|failed/i
    ]
  },
  {
    eventType: "user_frustration",
    emotionalFamily: "empathy",
    confidence: 0.86,
    reason: "user_frustration_signal",
    patterns: [
      /太丑|难看|不好看|不满意|失望|烦|崩溃|离谱|糟糕|垃圾|没用|不行|还是不对|又错了/,
      /\b(bad|ugly|annoying|frustrated|broken|error again|not working)\b/i
    ]
  },
  {
    eventType: "task_success",
    emotionalFamily: "celebration",
    confidence: 0.84,
    reason: "task_success_signal",
    patterns: [
      /完成了|已完成|搞定|成功|通过了|修好了|部署成功|安装成功|可以用了|验证通过|done|completed|success|passed|fixed|deployed/i
    ]
  },
  {
    eventType: "user_delight",
    emotionalFamily: "playful",
    confidence: 0.86,
    reason: "user_delight_signal",
    patterns: [
      /很好|好多了|太好了|不错|漂亮|喜欢|开心|哈哈|有趣|牛|厉害|great|nice|awesome|love it|looks good|much better/i
    ]
  }
];

function makeEventId() {
  if (globalThis.crypto?.randomUUID) {
    return `evt_${globalThis.crypto.randomUUID().replaceAll("-", "")}`;
  }

  return `evt_${Date.now().toString(36)}_${Math.random().toString(36).slice(2)}`;
}

function maskApiKey(apiKey) {
  if (!apiKey || apiKey.length <= 10) {
    return "********";
  }

  return `${apiKey.slice(0, 6)}...${apiKey.slice(-4)}`;
}

function normalizeClassificationText(parts) {
  return parts
    .filter((part) => part !== null && part !== undefined)
    .map((part) => String(part))
    .join("\n")
    .slice(-4000);
}

export function classifyReactionMoment({
  userMessage = "",
  mainReply = "",
  toolSummary = "",
  conversationSummary = "",
  metadata = {},
  fallbackEventType = null
} = {}) {
  const text = normalizeClassificationText([
    userMessage,
    mainReply,
    toolSummary,
    conversationSummary,
    metadata.summary,
    metadata.error,
    metadata.status
  ]);

  if (!text.trim()) {
    return {
      shouldReact: false,
      eventType: fallbackEventType,
      emotionalFamily: fallbackEventType ? DEFAULT_EVENT_MAP[fallbackEventType] : null,
      intensity: "low",
      confidence: 0.2,
      reason: "no_context"
    };
  }

  for (const classifier of EVENT_CLASSIFIERS) {
    if (classifier.patterns.some((pattern) => pattern.test(text))) {
      return {
        shouldReact: true,
        eventType: classifier.eventType,
        emotionalFamily: classifier.emotionalFamily,
        intensity: "low",
        confidence: classifier.confidence,
        reason: classifier.reason
      };
    }
  }

  if (fallbackEventType && DEFAULT_EVENT_MAP[fallbackEventType]) {
    return {
      shouldReact: true,
      eventType: fallbackEventType,
      emotionalFamily: DEFAULT_EVENT_MAP[fallbackEventType],
      intensity: "low",
      confidence: 0.72,
      reason: "fallback_event_type"
    };
  }

  return {
    shouldReact: false,
    eventType: null,
    emotionalFamily: null,
    intensity: "low",
    confidence: 0.35,
    reason: "no_clear_signal"
  };
}

async function getNodeStorageFilePath() {
  if (!globalThis.process?.versions?.node) {
    return null;
  }

  const path = await import("node:path");
  return process.env.OPENCLAW_TEMPERATURE_KEY_FILE
    ?? path.join(process.cwd(), ".openclaw-temperature", "api-key.json");
}

export function createDefaultApiKeyStorage({ storageKey = STORAGE_KEY } = {}) {
  return {
    async getItem() {
      if (globalThis.localStorage) {
        return globalThis.localStorage.getItem(storageKey);
      }

      const filePath = await getNodeStorageFilePath();
      if (!filePath) {
        return null;
      }

      try {
        const fs = await import("node:fs/promises");
        const raw = await fs.readFile(filePath, "utf8");
        const parsed = JSON.parse(raw);
        return typeof parsed.apiKey === "string" ? parsed.apiKey : null;
      } catch {
        return null;
      }
    },

    async setItem(apiKey) {
      if (globalThis.localStorage) {
        globalThis.localStorage.setItem(storageKey, apiKey);
        return;
      }

      const filePath = await getNodeStorageFilePath();
      if (!filePath) {
        return;
      }

      const fs = await import("node:fs/promises");
      const path = await import("node:path");
      await fs.mkdir(path.dirname(filePath), { recursive: true });
      await fs.writeFile(
        filePath,
        JSON.stringify({ apiKey, createdAt: new Date().toISOString() }, null, 2),
        "utf8"
      );
    }
  };
}

export function buildReactionEvent({
  eventType,
  emotionalFamily,
  intensity = "low",
  confidence = 0.8,
  metadata = {}
}) {
  return {
    schema_version: "reaction-event.v1",
    event: {
      event_id: makeEventId(),
      event_type: eventType,
      emotional_family: emotionalFamily ?? DEFAULT_EVENT_MAP[eventType],
      intensity,
      timestamp: new Date().toISOString(),
      source_context: {
        surface: "chat_reply",
        trigger_moment: "after_main_reply",
        confidence
      },
      metadata
    }
  };
}

export async function registerApiKey({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  fetchImpl = fetch
} = {}) {
  const response = await fetchImpl(`${hostedApiBaseUrl}/v1/public/api-keys/register`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify({
      source: "openclaw_skill_library"
    })
  });

  if (!response.ok) {
    throw new Error(`register_http_${response.status}`);
  }

  const body = await response.json();
  const registration = body.api_key_registration;
  const apiKey = registration?.apiKey?.token;
  if (!apiKey) {
    throw new Error("register_missing_api_key");
  }

  return {
    apiKey,
    registration
  };
}

export async function ensureApiKey({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  apiKey,
  storage = createDefaultApiKeyStorage(),
  fetchImpl = fetch
} = {}) {
  if (apiKey) {
    return {
      apiKey,
      registration: null,
      source: "provided"
    };
  }

  const storedApiKey = await storage.getItem();
  if (storedApiKey) {
    return {
      apiKey: storedApiKey,
      registration: null,
      source: "stored"
    };
  }

  const registered = await registerApiKey({ hostedApiBaseUrl, fetchImpl });
  await storage.setItem(registered.apiKey);
  return {
    ...registered,
    source: "registered"
  };
}

export async function initializeTemperatureLayer({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  apiKey = null,
  storage = createDefaultApiKeyStorage(),
  fetchImpl = fetch
} = {}) {
  const resolved = await ensureApiKey({
    hostedApiBaseUrl,
    apiKey,
    storage,
    fetchImpl
  });

  return {
    status: resolved.registration?.status ?? "ready",
    apiKeyHint: maskApiKey(resolved.apiKey),
    source: resolved.source,
    trialExpiresAt: resolved.registration?.trial_expires_at ?? null,
    rechargeUrl: resolved.registration?.recharge_url ?? null,
    billingMode: resolved.registration?.billing_mode ?? "free",
    message:
      resolved.source === "registered"
        ? "OpenClaw 温度层已开启，当前 Beta 免费使用。"
        : "OpenClaw 温度层已就绪。"
  };
}

export async function getRechargeInstructions({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  apiKey = null,
  storage = createDefaultApiKeyStorage(),
  fetchImpl = fetch
} = {}) {
  const resolved = await ensureApiKey({
    hostedApiBaseUrl,
    apiKey,
    storage,
    fetchImpl
  });
  const response = await fetchImpl(`${hostedApiBaseUrl}/v1/public/commerce-settings`);
  const body = response.ok ? await response.json() : {};
  const settings = body.commerce_settings ?? {};

  return {
    mode: "recharge_instructions",
    apiKey: resolved.apiKey,
    apiKeyHint: maskApiKey(resolved.apiKey),
    price: settings.betaPriceDisplay ?? "当前免费",
    paymentMethod: settings.paymentMethodLabel ?? "无需付款",
    buyPageUrl: `${hostedApiBaseUrl}/recharge?api_key=${encodeURIComponent(resolved.apiKey)}`
  };
}

export async function requestReaction({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  apiKey = null,
  payload,
  storage = createDefaultApiKeyStorage(),
  fetchImpl = fetch
}) {
  try {
    const resolved = await ensureApiKey({
      hostedApiBaseUrl,
      apiKey,
      storage,
      fetchImpl
    });

    const response = await fetchImpl(`${hostedApiBaseUrl}/v1/reactions/decide`, {
      method: "POST",
      headers: {
        authorization: `Bearer ${resolved.apiKey}`,
        "content-type": "application/json",
        "x-openclaw-skill-version": SKILL_VERSION
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      if (response.status === 402 || errorBody.code === "recharge_required") {
        const recharge = await getRechargeInstructions({
          hostedApiBaseUrl,
          apiKey: resolved.apiKey,
          storage,
          fetchImpl
        }).catch(() => null);
        return {
          mode: "recharge_required",
          degraded: false,
          apiKey: resolved.apiKey,
          apiKeyHint: maskApiKey(resolved.apiKey),
          reason: "trial_expired",
          rechargeUrl: errorBody.recharge_url ?? recharge?.buyPageUrl ?? `${hostedApiBaseUrl}/recharge`,
          recharge
        };
      }

      return {
        mode: "no_reaction",
        degraded: true,
        reason: `http_${response.status}`
      };
    }

    const body = await response.json();
    if (body.decision?.status !== "reacted" || !body.reaction) {
      return {
        mode: "no_reaction",
        degraded: false,
        apiKeyHint: maskApiKey(resolved.apiKey),
        reason: body.decision?.reason_codes ?? []
      };
    }

    return {
      mode: "react",
      degraded: false,
      apiKeyHint: maskApiKey(resolved.apiKey),
      reaction: stripPlaybackUrl(body.reaction),
      decision: body.decision
    };
  } catch {
    return {
      mode: "no_reaction",
      degraded: true,
      reason: "network_error"
    };
  }
}

export function attachReactionAfterReply({ mainReply, reactionResult }) {
  if (!reactionResult || reactionResult.mode !== "react") {
    return {
      mainReply,
      reaction: null
    };
  }

  return {
    mainReply,
    reaction: {
      displayMode: "after_main_reply",
      caption: reactionResult.reaction.caption,
      assetUrl: reactionResult.reaction.asset_url
    }
  };
}

export function formatReactionMarkdown(reactionResult) {
  if (!reactionResult || reactionResult.mode === "no_reaction") {
    return "";
  }

  if (reactionResult.mode === "recharge_required") {
    return formatRechargeMarkdown(reactionResult.recharge ?? reactionResult);
  }

  if (reactionResult.mode !== "react" || !reactionResult.reaction) {
    return "";
  }

  const caption = reactionResult.reaction.caption || "OpenClaw 温度层";
  return `${caption}\n\n![${caption}](${reactionResult.reaction.asset_url})`;
}

export function formatRechargeMarkdown(recharge) {
  const buyPageUrl = recharge.buyPageUrl ?? recharge.rechargeUrl ?? "https://claw-temp.nydhfc.cn/recharge";
  return [
    "OpenClaw 温度层当前已改为免费 Beta，通常不需要充值。",
    "",
    `价格：${recharge.price ?? "当前免费"}`,
    `付款方式：${recharge.paymentMethod ?? "无需付款"}`,
    `API Key：${recharge.apiKey ?? recharge.apiKeyHint ?? "请让 OpenClaw 读取本地保存的 ocl_ key"}`,
    "",
    `查看免费说明：${buyPageUrl}`
  ].join("\n");
}

export async function createTemperatureGifReply({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  apiKey = null,
  eventType = "user_delight",
  emotionalFamily,
  intensity = "low",
  confidence = 0.85,
  metadata = {},
  storage = createDefaultApiKeyStorage(),
  fetchImpl = fetch
} = {}) {
  const payload = buildReactionEvent({
    eventType,
    emotionalFamily,
    intensity,
    confidence,
    metadata
  });
  const result = await requestReaction({
    hostedApiBaseUrl,
    apiKey,
    payload,
    storage,
    fetchImpl
  });

  return {
    ...result,
    markdown: formatReactionMarkdown(result)
  };
}

export async function maybeAttachTemperatureReaction({
  hostedApiBaseUrl = HOSTED_API_BASE_URL,
  apiKey = null,
  mainReply,
  userMessage = "",
  toolSummary = "",
  conversationSummary = "",
  eventType,
  emotionalFamily,
  intensity = "low",
  confidence,
  metadata = {},
  autoClassify = true,
  storage = createDefaultApiKeyStorage(),
  fetchImpl = fetch
}) {
  const classification = autoClassify
    ? classifyReactionMoment({
        userMessage,
        mainReply,
        toolSummary,
        conversationSummary,
        metadata,
        fallbackEventType: eventType
      })
    : {
        shouldReact: true,
        eventType,
        emotionalFamily: emotionalFamily ?? DEFAULT_EVENT_MAP[eventType],
        intensity,
        confidence: confidence ?? 0.8,
        reason: "manual_event"
      };

  if (!classification.shouldReact) {
    return {
      mainReply,
      reaction: null,
      debug: {
        mode: "no_reaction",
        degraded: false,
        reason: classification.reason,
        classification
      }
    };
  }

  const payload = buildReactionEvent({
    eventType: classification.eventType,
    emotionalFamily: emotionalFamily ?? classification.emotionalFamily,
    intensity: intensity ?? classification.intensity,
    confidence: confidence ?? classification.confidence,
    metadata: {
      ...metadata,
      classification_reason: classification.reason
    }
  });

  const result = await requestReaction({
    hostedApiBaseUrl,
    apiKey,
    payload,
    storage,
    fetchImpl
  });
  if (result.mode !== "react") {
    return {
      mainReply,
      reaction: null,
      debug: result
    };
  }

  return {
    mainReply,
    reaction: {
      displayMode: "after_main_reply",
      caption: result.reaction.caption,
      assetUrl: result.reaction.asset_url
    },
    debug: result
  };
}

function stripPlaybackUrl(reaction) {
  if (!reaction || typeof reaction !== "object") {
    return reaction;
  }

  const cleanReaction = { ...reaction };
  delete cleanReaction["open" + "_url"];
  return cleanReaction;
}
