import { z } from "zod";

// ── Stellar G-address format ──────────────────────────────
const stellarAddress = z
  .string()
  .regex(/^G[A-Z2-7]{55}$/, "Must be a valid Stellar public key (G...)");

// ── Environment modes ─────────────────────────────────────
const nodeEnv = z.enum(["development", "staging", "production", "test"]).default("development");
const logLevel = z.enum(["debug", "info", "warn", "error"]).default("info");

const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  API_VERSION: z.string().default("0.3.1"),
  NODE_ENV: nodeEnv,
  LOG_LEVEL: logLevel,

  // ── Stellar-native config (primary) ──────────────────────
  STELLAR_NETWORK: z.string().default("stellar:pubnet"),
  STELLAR_HORIZON_URL: z
    .string()
    .url()
    .default("https://horizon.stellar.org"),
  STELLAR_USDC_ASSET: z
    .string()
    .default("CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75"),

  // ── MANDATORY in all environments (no unsafe defaults) ───
  STELLAR_TREASURY_ADDRESS: stellarAddress,
  FACILITATOR_URL: z.string().url(),
  FACILITATOR_API_KEY: z.string().min(1),
  WEBHOOK_SECRET: z.string().min(1),
  WEBHOOK_SECRET_PREVIOUS: z.string().optional(),

  // ── Facilitator tuning ───────────────────────────────────
  FACILITATOR_TIMEOUT_MS: z.coerce.number().default(8000),
  FACILITATOR_MAX_RETRIES: z.coerce.number().default(2),

  // ── Repository mode ─────────────────────────────────────
  REPO_MODE: z.enum(["inmemory", "postgres"]).default("inmemory"),
  DATABASE_URL: z.string().optional(),
  CARD_DETAILS_KEY: z.string().optional(), // base64-encoded 32 bytes, validated below

  // ── Legacy Solana fallback (backward compat, removed in M2) ──
  SOLANA_NETWORK: z.string().optional(),
  SOLANA_RPC_URL: z.string().optional(),
  USDC_MINT: z.string().optional(),
  TREASURY_PUBKEY: z.string().optional(),

  // ── Rollout gate (staged traffic control) ──────────────
  ROLLOUT_ENABLED: z.enum(["true", "false"]).default("true"),
  ROLLOUT_PCT: z.coerce.number().min(0).max(100).default(100),

  // ── Ops dashboard security ─────────────────────────────
  OPS_API_KEY: z.string().optional(),
  OPS_IP_ALLOWLIST: z.string().optional(),           // comma-separated CIDRs/IPs

  // ── Telegram Bot (@ASGCardbot) ──────────────────────────
  TG_BOT_ENABLED: z.enum(["true", "false"]).default("false"),
  TG_BOT_TOKEN: z.string().optional(),
  TG_WEBHOOK_SECRET: z.string().optional(),

  // ── Owner Portal ───────────────────────────────────────
  OWNER_PORTAL_ENABLED: z.enum(["true", "false"]).default("false"),

  // ── Bot Alerts (event notifications to TG) ─────────────
  BOT_ALERTS_ENABLED: z.enum(["true", "false"]).default("false"),

  // ── Admin Bot (ops notifications to admin TG chat) ─────
  ADMIN_BOT_ENABLED: z.enum(["true", "false"]).default("false"),
  ADMIN_BOT_TOKEN: z.string().optional(),
  ADMIN_CHAT_ID: z.string().optional(),

  // ── Agent Details (REALIGN: nonce + anti-replay for card details) ──
  AGENT_DETAILS_ENABLED: z.enum(["true", "false"]).default("true"),
  DETAILS_READ_LIMIT_PER_HOUR: z.coerce.number().default(5),
});

// ── Fail-fast startup validation ──────────────────────────
let env: z.infer<typeof envSchema>;

try {
  env = envSchema.parse(process.env);

  // ── Conditional validation for postgres mode ────────────
  if (env.REPO_MODE === "postgres") {
    if (!env.DATABASE_URL) {
      throw new Error(
        "DATABASE_URL is required when REPO_MODE=postgres"
      );
    }
    if (!env.CARD_DETAILS_KEY) {
      throw new Error(
        "CARD_DETAILS_KEY is required when REPO_MODE=postgres. " +
        'Generate with: node -e "console.log(require(\'crypto\').randomBytes(32).toString(\'base64\'))"'
      );
    }
    // Validate key byte length (must be exactly 32 bytes when decoded from base64)
    const keyBuf = Buffer.from(env.CARD_DETAILS_KEY, "base64");
    if (keyBuf.length !== 32) {
      throw new Error(
        `CARD_DETAILS_KEY must be exactly 32 bytes (got ${keyBuf.length}). ` +
        'Generate with: node -e "console.log(require(\'crypto\').randomBytes(32).toString(\'base64\'))"'
      );
    }
  }
} catch (error) {
  if (error instanceof z.ZodError) {
    const missing = error.issues
      .map((i) => `  • ${i.path.join(".")}: ${i.message}`)
      .join("\n");
    const message =
      `\n❌ ASG Card API — environment validation failed:\n${missing}\n\n` +
      `Hint: copy api/.env.example to api/.env and fill in required values.\n`;
    // In production, log and exit; in test, throw for assertions
    if (typeof process !== "undefined" && process.env.NODE_ENV !== "test") {
      console.error(message);
      process.exit(1);
    }
    throw new Error(message);
  }
  // Re-throw non-Zod errors (e.g. our conditional validation errors)
  if (typeof process !== "undefined" && process.env.NODE_ENV !== "test") {
    console.error(`\n❌ ${(error as Error).message}\n`);
    process.exit(1);
  }
  throw error;
}

export { env };
