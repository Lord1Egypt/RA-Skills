import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import {
  buildReactionEvent,
  classifyReactionMoment,
  createTemperatureGifReply,
  formatReactionMarkdown,
  initializeTemperatureLayer,
  maybeAttachTemperatureReaction,
  requestReaction
} from "../index.js";

test("initializes by auto-registering a free key", async () => {
  let storedApiKey = null;
  const storage = {
    async getItem() {
      return storedApiKey;
    },
    async setItem(apiKey) {
      storedApiKey = apiKey;
    }
  };
  const fetchImpl = async (url) => {
    assert.equal(url, "https://claw-temp.nydhfc.cn/v1/public/api-keys/register");
    return new Response(JSON.stringify({
      api_key_registration: {
        status: "free_active",
        trial_expires_at: null,
        recharge_url: null,
        billing_mode: "free",
        apiKey: {
          token: "ocl_publishable_free_key"
        }
      }
    }), { status: 201 });
  };

  const result = await initializeTemperatureLayer({ storage, fetchImpl });

  assert.equal(result.status, "free_active");
  assert.equal(result.source, "registered");
  assert.equal(result.apiKeyHint, "ocl_pu..._key");
  assert.equal(result.trialExpiresAt, null);
  assert.equal(result.rechargeUrl, null);
  assert.equal(result.billingMode, "free");
  assert.equal(storedApiKey, "ocl_publishable_free_key");
});

test("returns recharge-required for expired trials", async () => {
  const payload = buildReactionEvent({
    eventType: "task_blocked",
    metadata: {
      summary: "User is blocked"
    }
  });
  const storage = {
    async getItem() {
      return "ocl_expired_trial_key";
    },
    async setItem() {
      throw new Error("should not write storage");
    }
  };
  const fetchImpl = async (url) => {
    if (url === "https://claw-temp.nydhfc.cn/v1/public/commerce-settings") {
      return new Response(JSON.stringify({
        commerce_settings: {
          betaPriceDisplay: "当前免费",
          paymentMethodLabel: "无需付款",
          paymentQrImageUrl: "https://claw-temp.nydhfc.cn/pay/qr.png",
          paymentInstructions: "付款后提交 API key 和付款凭证。",
          buy_page_url: "https://claw-temp.nydhfc.cn/recharge",
          status_page_url: "https://claw-temp.nydhfc.cn/status"
        }
      }), { status: 200 });
    }

    assert.equal(url, "https://claw-temp.nydhfc.cn/v1/reactions/decide");
    return new Response(JSON.stringify({
      code: "recharge_required",
      recharge_url: "https://claw-temp.nydhfc.cn/recharge"
    }), { status: 402 });
  };

  const result = await requestReaction({ payload, storage, fetchImpl });

  assert.equal(result.mode, "recharge_required");
  assert.equal(result.degraded, false);
  assert.equal(result.reason, "trial_expired");
  assert.equal(result.rechargeUrl, "https://claw-temp.nydhfc.cn/recharge");
  assert.equal(result.apiKeyHint, "ocl_ex..._key");
  assert.equal(result.recharge.paymentQrImageUrl, undefined);
  assert.equal(result.recharge.paymentInstructions, undefined);
  assert.equal(result.recharge.statusPageUrl, undefined);
  assert.equal(result.recharge.buyPageUrl, "https://claw-temp.nydhfc.cn/recharge?api_key=ocl_expired_trial_key");
  assert.equal(formatReactionMarkdown(result).includes("API Key：ocl_expired_trial_key"), true);
  assert.equal(formatReactionMarkdown(result).includes("查看免费说明：https://claw-temp.nydhfc.cn/recharge?api_key=ocl_expired_trial_key"), true);
  assert.equal(formatReactionMarkdown(result).includes("查询处理进度"), false);
  assert.equal(formatReactionMarkdown(result).includes("付款凭证"), false);
});

test("contains marketplace metadata", async () => {
  const [skill, source, manifest] = await Promise.all([
    fs.readFile("SKILL.md", "utf8"),
    fs.readFile("index.js", "utf8"),
    fs.readFile("manifest.json", "utf8")
  ]);
  const parsedManifest = JSON.parse(manifest);

  assert.equal(skill.includes("https://claw-temp.nydhfc.cn"), true);
  assert.equal(source.includes("initializeTemperatureLayer"), true);
  assert.equal(parsedManifest.name, "openclaw-temperature");
  assert.equal(parsedManifest.repository, "https://github.com/wangych/OpenClaw-temperature-skill");
  assert.equal(parsedManifest.billing.mode, "free");
  assert.equal(parsedManifest.billing.trial_days, null);
  assert.equal(parsedManifest.billing.recharge_url, null);
  assert.deepEqual(parsedManifest.permissions.network, ["https://claw-temp.nydhfc.cn"]);
});

test("formats a direct GIF response as markdown", async () => {
  const reactionResult = {
    mode: "react",
    reaction: {
      caption: "这下气氛立刻活过来了",
      asset_url: "https://claw-temp.nydhfc.cn/assets/gifs/playful/user_delight/low/playful-user_delight-low-001.gif",
      open_url: "https://claw-temp.nydhfc.cn/r/playful.user_delight.low.001?v=motion-v2"
    }
  };

  const markdown = formatReactionMarkdown(reactionResult);

  assert.equal(markdown.includes("这下气氛立刻活过来了"), true);
  assert.equal(markdown.includes("![这下气氛立刻活过来了]("), true);
  assert.equal(markdown.includes("playful-user_delight-low-001.gif"), true);
  assert.equal(markdown.includes("微信里如果不动"), false);
  assert.equal(markdown.includes("https://claw-temp.nydhfc.cn/r/playful.user_delight.low.001"), false);
});

test("classifies natural context into supported reaction events", () => {
  const blocked = classifyReactionMoment({
    userMessage: "这里报错了，提示没有安装依赖",
    mainReply: "我先检查安装状态。"
  });
  const delight = classifyReactionMoment({
    userMessage: "现在好多了，这个看起来不错",
    mainReply: "我会继续保持这个方向。"
  });
  const quiet = classifyReactionMoment({
    userMessage: "继续",
    mainReply: "我会读取相关文件并更新实现。"
  });

  assert.equal(blocked.shouldReact, true);
  assert.equal(blocked.eventType, "task_blocked");
  assert.equal(blocked.emotionalFamily, "encouragement");
  assert.equal(delight.shouldReact, true);
  assert.equal(delight.eventType, "user_delight");
  assert.equal(quiet.shouldReact, false);
});

test("auto-classifies before requesting a reaction", async () => {
  const calls = [];
  const storage = {
    async getItem() {
      return "ocl_auto_classify_key";
    },
    async setItem() {
      throw new Error("should not write storage");
    }
  };
  const fetchImpl = async (url, options) => {
    calls.push({ url, body: JSON.parse(options.body) });
    return new Response(JSON.stringify({
      decision: {
        status: "reacted",
        reason_codes: ["eligible", "asset_exact_match"]
      },
      reaction: {
        caption: "别慌，我来兜底",
        asset_url: "https://claw-temp.nydhfc.cn/assets/gifs/encouragement/task_blocked/low/encouragement-task_blocked-low-002.gif"
      }
    }), { status: 200 });
  };

  const result = await maybeAttachTemperatureReaction({
    mainReply: "我发现当前环境没有安装这个工具，先帮你检查安装方式。",
    userMessage: "为什么运行不了？",
    metadata: {
      summary: "用户遇到环境问题"
    },
    storage,
    fetchImpl
  });

  assert.equal(result.reaction.caption, "别慌，我来兜底");
  assert.equal(calls.length, 1);
  assert.equal(calls[0].body.event.event_type, "task_blocked");
  assert.equal(calls[0].body.event.emotional_family, "encouragement");
  assert.equal(calls[0].body.event.metadata.classification_reason, "task_blocked_signal");
});

test("stays quiet when auto-classification has no clear signal", async () => {
  const fetchImpl = async () => {
    throw new Error("should not call hosted API");
  };

  const result = await maybeAttachTemperatureReaction({
    mainReply: "我会继续读取文件并检查实现。",
    userMessage: "继续",
    fetchImpl
  });

  assert.equal(result.reaction, null);
  assert.equal(result.debug.reason, "no_clear_signal");
});

test("creates markdown for direct user GIF requests", async () => {
  const calls = [];
  let storedApiKey = "ocl_direct_request_key";
  const storage = {
    async getItem() {
      return storedApiKey;
    },
    async setItem(apiKey) {
      storedApiKey = apiKey;
    }
  };
  const fetchImpl = async (url, options) => {
    calls.push({ url, options });
    return new Response(JSON.stringify({
      decision: {
        status: "reacted",
        reason_codes: ["eligible", "asset_exact_match"]
      },
      reaction: {
        caption: "这下气氛立刻活过来了",
        asset_url: "https://claw-temp.nydhfc.cn/assets/gifs/playful/user_delight/low/playful-user_delight-low-001.gif"
      }
    }), { status: 200 });
  };

  const result = await createTemperatureGifReply({
    eventType: "user_delight",
    emotionalFamily: "playful",
    storage,
    fetchImpl
  });

  assert.equal(result.mode, "react");
  assert.equal(result.markdown.includes("playful-user_delight-low-001.gif"), true);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].options.headers.authorization, "Bearer ocl_direct_request_key");
});
