import { readFileSync } from "node:fs";
import { createServer } from "node:http";

// Load .env (no dotenv dependency needed)
try {
  const env = readFileSync(new URL("../.env", import.meta.url), "utf-8");
  for (const line of env.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 1) continue;
    const key = trimmed.slice(0, eq);
    const val = trimmed.slice(eq + 1);
    if (!process.env[key]) process.env[key] = val;
  }
} catch {}
import { createWebhookHandler } from "../src/webhook-handler.js";
import { classifyEvent } from "../src/event-processor.js";
import { formatEventAlert } from "../src/rule-engine.js";
import { analyzeChurn } from "../src/llm-analyzer.js";
import { executeAction, formatActionResult } from "../src/action-executor.js";
import { createTelegramBot, formatChurnAlert, buildInlineKeyboard } from "../src/telegram.js";
import { extractChurnContext, shouldAutoExecute } from "../src/index-helpers.js";
import type { CreemWebhookPayload, LLMDecision, ChurnContext } from "../src/types.js";

const PORT = Number(process.env.PORT ?? 3000);
const AUTO_EXECUTE_THRESHOLD = 0.8;

const pendingDecisions = new Map<string, { decision: LLMDecision; context: ChurnContext }>();

async function main(): Promise<void> {
  const {
    CREEM_API_KEY,
    CREEM_WEBHOOK_SECRET,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    ANTHROPIC_API_KEY,
  } = process.env;

  if (!CREEM_WEBHOOK_SECRET) {
    console.error("❌ CREEM_WEBHOOK_SECRET is required");
    process.exit(1);
  }

  // --- Initialize SDKs ---
  let creem: any = null;
  if (CREEM_API_KEY) {
    const { Creem } = await import("creem");
    creem = new Creem({ apiKey: CREEM_API_KEY, serverIdx: 1 });
    console.log("✅ Creem SDK initialized (test mode)");
  } else {
    console.log("⚠️  CREEM_API_KEY not set — Creem SDK calls will be skipped");
  }

  let anthropic: any = null;
  if (ANTHROPIC_API_KEY) {
    const Anthropic = (await import("@anthropic-ai/sdk")).default;
    anthropic = new Anthropic({ apiKey: ANTHROPIC_API_KEY });
    console.log("✅ Anthropic SDK initialized");
  } else {
    console.log("⚠️  ANTHROPIC_API_KEY not set — using rule-based fallback only");
  }

  let bot: any = null;
  if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHAT_ID) {
    const TelegramBotLib = (await import("node-telegram-bot-api")).default;
    const rawBot = new TelegramBotLib(TELEGRAM_BOT_TOKEN, { polling: true });
    bot = createTelegramBot(rawBot, TELEGRAM_CHAT_ID);
    console.log("✅ Telegram bot initialized");

    // Callback handler
    rawBot.on("callback_query", async (query: any) => {
      if (!query.data) return;
      const [action, subscriptionId] = query.data.split(":");
      if (!action || !subscriptionId) return;

      if (action === "skip") {
        pendingDecisions.delete(subscriptionId);
        await bot.sendMessage(`⏭️ Skipped action for ${subscriptionId}`);
        return;
      }

      if (action === "apply" || action === "pause") {
        const entry = pendingDecisions.get(subscriptionId);
        if (!entry) {
          await bot.sendMessage(`❌ No pending decision for ${subscriptionId}`);
          return;
        }
        const overrideDecision = action === "apply"
          ? entry.decision
          : { ...entry.decision, action: "SUGGEST_PAUSE" as const };
        const result = await executeAction(overrideDecision, entry.context, creem);
        const resultMsg = formatActionResult(result, entry.context);
        await bot.sendMessage(resultMsg);
        pendingDecisions.delete(subscriptionId);
      }
    });

    // Telegram commands
    rawBot.onText(/\/creem-status/, async () => {
      await bot.sendMessage(`✅ Creem Store Agent is running\nWebhook: http://localhost:${PORT}/webhook/creem`);
    });

    rawBot.onText(/\/creem-report/, async () => {
      await bot.sendMessage("📊 Daily Report\n(Connect to Creem dashboard for full stats)");
    });
  } else {
    console.log("⚠️  TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID not set — logging to console only");
  }

  // --- Send message helper (Telegram or console) ---
  async function sendAlert(text: string, options?: any): Promise<void> {
    if (bot) {
      await bot.sendMessage(text, options);
    } else {
      console.log("\n📨 ALERT:\n" + text);
      if (options?.reply_markup) {
        console.log("  [Buttons]:", JSON.stringify(options.reply_markup.inline_keyboard));
      }
    }
  }

  // --- Event handler ---
  async function handleEvent(payload: CreemWebhookPayload): Promise<void> {
    const classified = classifyEvent(payload);

    if (classified.category === "simple") {
      const alert = formatEventAlert(payload);
      await sendAlert(alert);
      return;
    }

    // Churn event
    let churnCtx: ChurnContext;
    if (creem) {
      churnCtx = await extractChurnContext(payload, creem);
    } else {
      // Mock context when Creem SDK is not available
      const obj = payload.object as Record<string, unknown>;
      churnCtx = {
        subscriptionId: (obj.id as string) ?? "sub_unknown",
        customerId: (obj.customerId as string) ?? "cus_unknown",
        productId: "prod_unknown",
        customerEmail: ((obj.customer as any)?.email as string) ?? "unknown",
        productName: ((obj.product as any)?.name as string) ?? "Unknown Plan",
        price: 49,
        tenureMonths: 8,
        totalRevenue: 392,
        cancelReason: (obj.cancelReason as string) ?? "not provided",
      };
    }

    console.log(`🔍 Analyzing churn for ${churnCtx.customerEmail} (${churnCtx.productName})`);

    const { fallbackDecision } = await import("../src/llm-analyzer.js");
    const decision = anthropic
      ? await analyzeChurn(churnCtx, anthropic)
      : fallbackDecision(churnCtx);

    const alertMsg = formatChurnAlert(churnCtx, decision);
    const keyboard = buildInlineKeyboard(churnCtx.subscriptionId, decision.action);

    await sendAlert(alertMsg, {
      parse_mode: "HTML",
      ...(keyboard.length > 0 ? { reply_markup: { inline_keyboard: keyboard } } : {}),
    });

    if (shouldAutoExecute(decision, AUTO_EXECUTE_THRESHOLD)) {
      if (creem) {
        const result = await executeAction(decision, churnCtx, creem);
        const resultMsg = formatActionResult(result, churnCtx);
        await sendAlert(`🤖 Auto-executed (confidence ${Math.round(decision.confidence * 100)}%):\n${resultMsg}`);
      } else {
        await sendAlert(`🤖 Would auto-execute ${decision.action} (confidence ${Math.round(decision.confidence * 100)}%) — Creem SDK not configured`);
      }
    } else {
      pendingDecisions.set(churnCtx.subscriptionId, { decision, context: churnCtx });
    }
  }

  // --- HTTP server ---
  const webhookHandler = createWebhookHandler({
    secret: CREEM_WEBHOOK_SECRET,
    onEvent: handleEvent,
  });

  const server = createServer(async (req, res) => {
    if (req.url === "/webhook/creem" && req.method === "POST") {
      await webhookHandler(req, res);
    } else {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ status: "Creem Store Agent running", webhook: "/webhook/creem" }));
    }
  });

  server.listen(PORT, () => {
    console.log(`\n🍦 Creem Store Agent — Standalone Demo Server`);
    console.log(`   Webhook: http://localhost:${PORT}/webhook/creem`);
    console.log(`   Health:  http://localhost:${PORT}/`);
    console.log(`\n   Run demo:  CREEM_WEBHOOK_SECRET=${CREEM_WEBHOOK_SECRET} npm run demo\n`);
  });
}

main().catch(console.error);
