#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { randomUUID } from "node:crypto";
import {
  mkdirSync,
  chmodSync,
  readFileSync,
  realpathSync,
  renameSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

import {
  buildPaymentHeader,
  enumeratePaymentOptions,
  parsePaymentRequirements,
} from "./payment-flow.mjs";

import {
  apiBase, apiRequest, createCredentials, sanitize, responseState, PACKS,
  accountResult, readAccount, prepareAccountAuth, executeAccountAuth,
} from "./account-flow.mjs";
import { formatDivergenceRows, validateDivergenceLimit, validateDivergenceLabels, validateDivergenceCountText } from "./divergence-flow.mjs";
import { firstDivergencePage, readDivergencePage } from "./divergence-pages.mjs";
const INTENT_TTL_MS = 30 * 60 * 1000;
const APPROVAL_WAIT_MS = 45 * 1000;
const APPROVAL_POLL_MS = 3 * 1000;
const PAYMENT_SETTLE_DELAY_MS = 3 * 1000;

const NETWORK_METADATA = {
  "eip155:8453": { name: "Base mainnet", environment: "mainnet" },
  "eip155:84532": { name: "Base Sepolia", environment: "testnet" },
  "eip155:56": { name: "BNB Chain mainnet", environment: "mainnet" },
};

const TOKEN_METADATA = new Map([
  ["eip155:8453", { symbol: "USDC", decimals: 6 }],
  ["eip155:84532", { symbol: "USDC", decimals: 6 }],
  ["eip155:56", { symbol: "USD1", decimals: 18 }],
]);

const WALLET_SETUP_OPTIONS = [
  {
    id: "binance-agentic-wallet",
    name: "Binance Agentic Wallet",
    recommended: true,
    url: "https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/binance-agentic-wallet",
  },
  {
    id: "x402-buyer-quickstart",
    name: "x402 Foundation Buyer Quickstart",
    recommended: false,
    url: "https://docs.x402.org/getting-started/quickstart-for-buyers",
  },
  {
    id: "viem-local-accounts",
    name: "viem Local Accounts",
    recommended: false,
    url: "https://viem.sh/docs/accounts/local",
  },
];

function fail(message, code = "INVALID_INPUT") {
  const error = new Error(message);
  error.code = code;
  throw error;
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function sameValue(left, right) {
  const a = String(left);
  const b = String(right);
  if (/^0x[0-9a-f]+$/i.test(a) && /^0x[0-9a-f]+$/i.test(b)) {
    return a.toLowerCase() === b.toLowerCase();
  }
  return a === b;
}

const redactSensitive = sanitize;

function formatBasisTimestamp(value) {
  if (typeof value !== "string") return value;
  return value.replace(
    /\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\b/g,
    (match) => {
      const timestamp = new Date(match);
      return Number.isNaN(timestamp.getTime())
        ? match
        : `${timestamp.toISOString().slice(0, 19).replace("T", " ")} UTC`;
    }
  );
}

function normalizeBasisTimestamps(value) {
  if (Array.isArray(value)) return value.map(normalizeBasisTimestamps);
  if (isObject(value)) {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [
        key,
        normalizeBasisTimestamps(item),
      ])
    );
  }
  return formatBasisTimestamp(value);
}

function basisLink(label, value) {
  if (typeof label !== "string" || typeof value !== "string") return null;
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" && url.protocol !== "http:") return null;
    const safeLabel = label.replace(/[\\[\]|]/g, "\\$&");
    return `[${safeLabel}](<${url.href}>)`;
  } catch {
    return null;
  }
}

function embedBasisLinks(value) {
  if (Array.isArray(value)) return value.map(embedBasisLinks);
  if (!isObject(value)) return value;

  const output = Object.fromEntries(
    Object.entries(value).map(([key, item]) => [key, embedBasisLinks(item)])
  );
  if (!("url" in output)) return output;

  const url = output.url;
  delete output.url;
  if (typeof output.summary === "string") {
    let linked = false;
    output.summary = output.summary.replace(/"([^"\n]+)"/, (match, label) => {
      const link = basisLink(label, url);
      if (!link) return match;
      linked = true;
      return `"${link}"`;
    });
    if (linked) return output;
  }
  const summaryLink = basisLink(output.summary, url);
  if (summaryLink) output.summary = summaryLink;
  return output;
}

function normalizeResponseForDisplay(response) {
  if (!isObject(response)) return response;
  const output = structuredClone(response);
  const data = output.data;
  if (!isObject(data)) return output;
  if (data.basis != null) {
    data.basis = embedBasisLinks(normalizeBasisTimestamps(data.basis));
  }
  if (isObject(data.probability) && data.probability.basis != null) {
    data.probability.basis = embedBasisLinks(
      normalizeBasisTimestamps(data.probability.basis)
    );
  }
  if (isObject(data.free_quota)) {
    delete data.free_quota.ip;
  }
  return output;
}

function validateProbabilityRequest(request) {
  if (!isObject(request)) fail("Probability request must be an object");
  if (typeof request.message !== "string" || request.message.trim() === "") {
    fail("Probability request message is required");
  }
  if (
    !Array.isArray(request.market_ids) ||
    request.market_ids.length === 0 ||
    request.market_ids.length > 10
  ) {
    fail("Probability request must contain 1 to 10 market_ids");
  }
  return structuredClone(request);
}

async function postProbability(fetchImpl, request, paymentHeader, { base = apiBase(), key } = {}) {
  const headers = {};
  if (paymentHeader) headers["PAYMENT-SIGNATURE"] = paymentHeader;
  if (key && !paymentHeader) headers["COURNOT-API-KEY"] = key;
  return apiRequest({ base, path: "probability", method: "POST", body: request, headers, fetchImpl });
}

const WINDOWS_CMD_META = /([()\][%!^"`<>&|;, *?])/g;

function escapeWindowsCommand(value) {
  const command = String(value);
  if (/[\r\n]/.test(command)) {
    fail("Wallet command cannot contain line breaks");
  }
  return command.replace(WINDOWS_CMD_META, "^$1");
}

function escapeWindowsArgument(value) {
  let escaped = String(value);
  if (/[\r\n]/.test(escaped)) {
    fail("Wallet command arguments cannot contain line breaks");
  }
  escaped = escaped.replace(/(?=(\\+?)?)\1"/g, "$1$1\\\"");
  escaped = escaped.replace(/(?=(\\+?)?)\1$/, "$1$1");
  escaped = `"${escaped}"`.replace(WINDOWS_CMD_META, "^$1");
  return escaped.replace(WINDOWS_CMD_META, "^$1");
}

function walletInvocation(command, args, platform, comspec) {
  if (platform !== "win32") return { command, args, windows: false };

  const commandLine = [
    escapeWindowsCommand(command),
    ...args.map(escapeWindowsArgument),
  ].join(" ");
  return {
    command: comspec || "cmd.exe",
    args: ["/d", "/s", "/c", `"${commandLine}"`],
    windows: true,
  };
}

export function runBaw(
  args,
  {
    command = process.env.COURNOT_WALLET_COMMAND || "baw",
    platform = process.platform,
    comspec = process.env.ComSpec || process.env.COMSPEC,
    spawn = spawnSync,
  } = {}
) {
  const invocation = walletInvocation(
    command,
    [...args, "--json"],
    platform,
    comspec
  );
  if (invocation.windows) {
    const available = spawn("where.exe", [command], {
      encoding: "utf8",
      shell: false,
      windowsHide: true,
    });
    if (available.error || available.status !== 0) {
      fail("Binance Agentic Wallet CLI is not installed", "WALLET_UNAVAILABLE");
    }
  }
  const result = spawn(invocation.command, invocation.args, {
    encoding: "utf8",
    maxBuffer: 10 * 1024 * 1024,
    shell: false,
    ...(invocation.windows
      ? { windowsVerbatimArguments: true, windowsHide: true }
      : {}),
  });
  if (result.error?.code === "ENOENT") {
    fail("Binance Agentic Wallet CLI is not installed", "WALLET_UNAVAILABLE");
  }
  if (result.error || result.status !== 0) {
    let code;
    try { code = JSON.parse(result.stdout).error?.code; } catch {}
    fail("Binance Agentic Wallet command failed", Number.isInteger(code) ? `WALLET_${code}` : "WALLET_COMMAND_FAILED");
  }
  try {
    return JSON.parse(result.stdout);
  } catch {
    fail("Binance Agentic Wallet returned invalid JSON", "WALLET_INVALID_RESPONSE");
  }
}

export function createBinanceWalletRunner({
  run = runBaw,
  wait = (milliseconds) =>
    new Promise((resolve) => setTimeout(resolve, milliseconds)),
  now = () => Date.now(),
} = {}) {
  return {
    preflight() {
      const cli = run(["cli-check", "--required-version", "1.8.0"]);
      if (cli?.success !== true || cli?.data?.needUpdateCli === true) {
        fail(
          "Binance Agentic Wallet CLI 1.8.0 or newer is required",
          "WALLET_UPDATE_REQUIRED"
        );
      }
      const status = run(["wallet", "status"]);
      return {
        connected:
          status?.success === true && status?.data?.status === "CONNECTED",
        status: status?.data?.status ?? "UNKNOWN",
      };
    },
    preview(paymentRequired) {
      return run([
        "x402-payment",
        "preview",
        "--paymentRequirements",
        paymentRequired,
      ]);
    },
    sign(paymentId, selectedIndex) {
      return run([
        "x402-payment",
        "sign",
        "--paymentId",
        paymentId,
        "--selectedIndex",
        String(selectedIndex),
      ]);
    },
    async waitForApproval(txHash, binanceChainId) {
      const deadline = now() + APPROVAL_WAIT_MS;
      while (now() < deadline) {
        const result = run([
          "wallet",
          "tx-history",
          "--tx",
          txHash,
          ...(binanceChainId
            ? ["--binanceChainId", String(binanceChainId)]
            : []),
        ]);
        const transactions = result?.data?.transactions;
        if (
          result?.success === true &&
          Array.isArray(transactions) &&
          transactions.some(
            (transaction) =>
              sameValue(transaction.txHash, txHash) &&
              String(transaction.status).toLowerCase() === "confirmed"
          )
        ) {
          return true;
        }
        await wait(APPROVAL_POLL_MS);
      }
      return false;
    },
  };
}

function defaultIntentDirectory() {
  return process.env.COURNOT_INTENT_DIR || join(tmpdir(), "cournot-intents");
}

export function createFileIntentStore({
  directory = defaultIntentDirectory(),
  now = () => Date.now(),
  createId = randomUUID,
} = {}) {
  mkdirSync(directory, { recursive: true, mode: 0o700 });
  chmodSync(directory, 0o700);

  function assertIntentId(intentId) {
    if (!/^[0-9a-f-]{36}$/i.test(intentId || "")) {
      fail("Invalid payment intent id");
    }
  }

  return {
    save(value) {
      const intentId = createId();
      const path = join(directory, `${intentId}.json`);
      writeFileSync(
        path,
        JSON.stringify({
          ...structuredClone(value),
          createdAt: now(),
          expiresAt: now() + INTENT_TTL_MS,
        }),
        { encoding: "utf8", flag: "wx", mode: 0o600 }
      );
      return intentId;
    },
    take(intentId) {
      assertIntentId(intentId);
      const path = join(directory, `${intentId}.json`);
      const processingPath = join(directory, `${intentId}.processing`);
      try {
        renameSync(path, processingPath);
      } catch {
        fail("Payment intent is missing or already used", "INTENT_UNAVAILABLE");
      }
      let value;
      try {
        value = JSON.parse(readFileSync(processingPath, "utf8"));
      } catch {
        unlinkSync(processingPath);
        fail("Payment intent is invalid", "INTENT_INVALID");
      }
      if (value.expiresAt <= now()) {
        unlinkSync(processingPath);
        fail("Payment intent has expired", "INTENT_EXPIRED");
      }
      return {
        value,
        consume() {
          try {
            unlinkSync(processingPath);
          } catch {}
        },
        restore() {
          renameSync(processingPath, path);
        },
      };
    },
  };
}

function safeTokenSymbol(value) {
  return typeof value === "string" && /^[A-Za-z0-9 ._-]{1,32}$/.test(value)
    ? value
    : null;
}

function normalizeDecimal(value) {
  if (value == null) return null;
  const text = String(value);
  if (!/^\d+(?:\.\d+)?$/.test(text)) return text;
  if (!text.includes(".")) return text;
  const normalized = text.replace(/0+$/, "").replace(/\.$/, "");
  return normalized === "" ? "0" : normalized;
}

function roundDecimal(value, places) {
  const normalized = normalizeDecimal(value);
  if (normalized == null || !/^\d+(?:\.\d+)?$/.test(normalized)) return null;

  const [whole, fraction = ""] = normalized.split(".");
  const kept = fraction.padEnd(places, "0").slice(0, places);
  let scaled = BigInt(`${whole}${kept}` || "0");
  if ((fraction[places] || "0") >= "5") scaled += 1n;

  const digits = scaled.toString().padStart(places + 1, "0");
  if (places === 0) return digits;
  return `${digits.slice(0, -places)}.${digits.slice(-places)}`;
}

function formatUsdLabel(value) {
  const normalized = normalizeDecimal(value);
  if (normalized == null || !/^\d+(?:\.\d+)?$/.test(normalized)) return null;

  const [whole, fraction = ""] = normalized.split(".");
  const atLeastOneCent =
    BigInt(whole) > 0n || BigInt(fraction.padEnd(2, "0").slice(0, 2)) >= 1n;
  return `$${roundDecimal(normalized, atLeastOneCent ? 2 : 6)}`;
}

function tokenMetadata(option) {
  const declaredSymbol = safeTokenSymbol(option.extra?.name);
  const canonicalSymbol =
    declaredSymbol === "USD Coin" ? "USDC" : declaredSymbol;
  const known = TOKEN_METADATA.get(option.network);
  const declaredDecimals = Number(option.extra?.decimals);
  const decimals =
    known?.decimals ??
    (Number.isInteger(declaredDecimals) &&
    declaredDecimals >= 0 &&
    declaredDecimals <= 36
      ? declaredDecimals
      : null);
  return {
    symbol: known?.symbol ?? canonicalSymbol,
    decimals,
  };
}

function formatUnits(value, decimals) {
  if (!/^\d+$/.test(String(value)) || !Number.isInteger(decimals)) return null;
  const padded = String(value).padStart(decimals + 1, "0");
  const whole = decimals === 0 ? padded : padded.slice(0, -decimals);
  const fraction = decimals === 0 ? "" : padded.slice(-decimals).replace(/0+$/, "");
  return fraction ? `${whole}.${fraction}` : whole;
}

function publicNetwork(network) {
  const metadata = NETWORK_METADATA[network];
  const networkName = metadata?.name ?? network;
  const networkEnvironment = metadata?.environment ?? "unknown";
  return {
    networkName,
    networkEnvironment,
    networkLabel:
      networkEnvironment === "unknown"
        ? `${networkName} (unknown)`
        : `${networkName} (${network}, ${networkEnvironment})`,
  };
}

function publicServerOptions(requirements) {
  return enumeratePaymentOptions(requirements).map((option, index) => ({
    originalIndex: index,
    displayIndex: index + 1,
    scheme: option.scheme,
    network: option.network,
    ...publicNetwork(option.network),
    asset: option.asset,
    ...(() => {
      const metadata = tokenMetadata(option);
      const displayAmount = formatUnits(option.amount, metadata.decimals);
      return {
        tokenSymbol: metadata.symbol,
        displayAmount,
        amountLabel: displayAmount
          ? `${displayAmount}${metadata.symbol ? ` ${metadata.symbol}` : ""}`
          : `${option.amount} base units${metadata.symbol ? ` ${metadata.symbol}` : ""}`,
      };
    })(),
    payTo: option.payTo,
    assetTransferMethod: option.extra?.assetTransferMethod ?? null,
  }));
}

function publicWalletSetup(reason, walletStatus = null) {
  return {
    walletStatus,
    options: WALLET_SETUP_OPTIONS.map((option) => ({
      ...option,
      installed:
        option.id === "binance-agentic-wallet"
          ? reason !== "WALLET_UNAVAILABLE"
          : null,
      connected:
        option.id === "binance-agentic-wallet"
          ? walletStatus === "CONNECTED"
          : null,
    })),
    actions: ["connect_or_install", "configure_x402_buyer", "connect_other_wallet", "stop"],
  };
}

function markdownCell(value) {
  return String(value ?? "")
    .replace(/\r?\n/g, " ")
    .replace(/\|/g, "\\|");
}

function walletRequiredPresentation({ request, reason, walletStatus, serverOptions }) {
  const chinese = /[\u3400-\u9fff]/u.test(request.message);
  const rows = serverOptions
    .map((option) => {
      const asset = option.tokenSymbol
        ? `${option.tokenSymbol} — \`${markdownCell(option.asset)}\``
        : `\`${markdownCell(option.asset)}\``;
      return `| ${option.displayIndex} | ${markdownCell(option.networkLabel)} | ${asset} | ${markdownCell(option.amountLabel)} | \`${markdownCell(option.payTo)}\` |`;
    })
    .join("\n");
  const hasMainnet = serverOptions.some(
    (option) => option.networkEnvironment === "mainnet"
  );
  const binanceStatus =
    reason === "WALLET_UNAVAILABLE"
      ? chinese
        ? "尚未安装"
        : "not installed"
      : walletStatus === "UNCONNECTED"
        ? chinese
          ? "已安装，目前未登录"
          : "installed, currently signed out"
        : chinese
          ? "当前不可用"
          : "currently unavailable";

  if (chinese) {
    return `${request.pack_id ? "购买流量包需要可用的钱包，尚未付款。" : request.operation === "divergence" ? "本次查询需要可用的钱包，尚未获得偏差榜单，也未发生任何付款。" : "本次查询需要可用的钱包，尚未获得概率结果，也未发生任何付款。"}

可用付款路线：

| 付款路线 | 网络 | 资产 | 金额 | 收款地址 |
|---|---|---|---|---|
${rows}
${hasMainnet ? "\n主网付款会转移真实资产。" : ""}

你可以选择：

- 连接或安装 [Binance Agentic Wallet](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/binance-agentic-wallet)（推荐；${binanceStatus}）
- 使用 [x402 Foundation Buyer Quickstart](https://docs.x402.org/getting-started/quickstart-for-buyers) 和 [viem Local Accounts](https://viem.sh/docs/accounts/local) 配置钱包
- 连接其他兼容钱包
- 停止，不付款

执行任何钱包设置前，我会展示具体操作和风险并再次确认；钱包设置确认不等于付款确认。

${walletStatus === "UNCONNECTED" ? "如果你已有 Binance Agentic Wallet，请回复“登录钱包”；如果尚未创建，需要先在 Binance App 中创建。" : "请选择一种设置方式，或选择停止。"}`;
  }

  return `${request.pack_id ? "A wallet is required to purchase this pack. No payment occurred." : request.operation === "divergence" ? "A wallet is needed for this query. No divergence ranking was obtained and no payment occurred." : "A wallet is needed for this query. No probability was obtained and no payment occurred."}

Available payment routes:

| Payment route | Network | Asset | Amount | Recipient |
|---|---|---|---|---|
${rows}
${hasMainnet ? "\nMainnet payment transfers real assets." : ""}

Choose how to continue:

- Connect or install [Binance Agentic Wallet](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/binance-agentic-wallet) (recommended; ${binanceStatus})
- Configure a wallet using [x402 Foundation Buyer Quickstart](https://docs.x402.org/getting-started/quickstart-for-buyers) and [viem Local Accounts](https://viem.sh/docs/accounts/local)
- Connect another compatible wallet
- Stop without paying

Before any wallet setup, I will show the exact action and risks and ask for separate confirmation. Wallet setup confirmation is not payment confirmation.

${walletStatus === "UNCONNECTED" ? 'Reply "sign in to wallet" if you already have a Binance Agentic Wallet. If you have not created one, create it in the Binance App first.' : "Choose one setup option, or stop."}`;
}

function walletRequiredResult({ request, reason, walletStatus = null, serverOptions, base }) {
  return {
    state: "wallet_required",
    base,
    reason,
    ...(walletStatus ? { walletStatus } : {}),
    serverOptions,
    walletSetup: publicWalletSetup(reason, walletStatus),
    presentation: walletRequiredPresentation({
      base,
      request,
      reason,
      walletStatus,
      serverOptions,
    }),
  };
}

function matchingAcceptIndex(requirements, originalAccept) {
  if (!isObject(originalAccept)) return null;
  const accepts = parsePaymentRequirements(requirements).accepts;
  const index = accepts.findIndex((accept) =>
    ["scheme", "network", "asset", "amount", "payTo"].every((field) =>
      sameValue(accept[field], originalAccept[field])
    )
  );
  return index === -1 ? null : index;
}

function sanitizePreviewOptions(previewOptions, requirements) {
  const ready = [];
  const blockers = [];
  for (const option of previewOptions) {
    const originalAcceptIndex = matchingAcceptIndex(
      requirements,
      option.originalAccept
    );
    const network = option.originalAccept?.network ?? null;
    const safe = {
      walletOptionIndex: option.index,
      status: option.status,
      reasons: Array.isArray(option.reasons) ? option.reasons : [],
      network,
      tokenAddress: option.tokenAddress ?? option.originalAccept?.asset ?? null,
      tokenSymbol:
        tokenMetadata(option.originalAccept ?? {}).symbol ??
        safeTokenSymbol(option.tokenSymbol),
      amount: option.amount ?? null,
      amountUsd: option.amountUsd ?? null,
      payTo: option.payTo ?? option.originalAccept?.payTo ?? null,
      currentBalance: option.currentBalance ?? null,
      currentBalanceUsd: option.currentBalanceUsd ?? null,
      needApproveFirst: option.needApproveFirst === true,
      originalAcceptIndex,
    };
    if (option.status === "READY_TO_SIGN" && originalAcceptIndex !== null) {
      ready.push(safe);
    } else {
      blockers.push(safe);
    }
  }
  return { ready, blockers };
}

function publicReadyOptions(ready) {
  return ready.map((option, index) => {
    const amount = normalizeDecimal(option.amount);
    const currentBalance = normalizeDecimal(option.currentBalance);
    const amountUsd = normalizeDecimal(option.amountUsd);
    const currentBalanceUsd = normalizeDecimal(option.currentBalanceUsd);
    return {
      displayIndex: index + 1,
      networkLabel: publicNetwork(option.network).networkLabel,
      tokenAddress: option.tokenAddress,
      tokenSymbol: option.tokenSymbol,
      amount,
      amountLabel:
        amount == null
          ? null
          : `${amount}${option.tokenSymbol ? ` ${option.tokenSymbol}` : ""}`,
      amountUsd,
      amountUsdLabel: formatUsdLabel(amountUsd),
      payTo: option.payTo,
      currentBalance,
      balanceLabel:
        currentBalance == null
          ? null
          : `${currentBalance}${option.tokenSymbol ? ` ${option.tokenSymbol}` : ""}`,
      currentBalanceUsd,
      balanceUsdLabel: formatUsdLabel(currentBalanceUsd),
      needApproveFirst: option.needApproveFirst,
    };
  });
}

function publicBlockers(blockers) {
  return blockers.map((option) => ({
    status: option.status,
    reasons: option.reasons,
    networkLabel: publicNetwork(option.network).networkLabel,
    tokenSymbol: option.tokenSymbol,
    tokenAddress: option.tokenAddress,
  }));
}

function walletFailureResult({ error, operation, request, serverOptions, base }) {
  const reason = error?.code || "WALLET_COMMAND_FAILED";
  if (reason === "WALLET_UNAVAILABLE") {
    return walletRequiredResult({ request, reason, serverOptions, base });
  }
  return {
    state: "wallet_blocked",
    base,
    serverOptions,
    blockers: [
      {
        scope: "wallet",
        wallet: "Binance Agentic Wallet",
        operation,
        status: "ACTION_REQUIRED",
        reasons: [reason],
      },
    ],
  };
}

export async function prepareProbability({
  request, fetchImpl = fetch, wallet = createBinanceWalletRunner(),
  intents = createFileIntentStore(), base = apiBase(), credentials = createCredentials(), perCall = false,
} = {}) {
  base = apiBase(base);
  const originalRequest = validateProbabilityRequest(request);
  const key = perCall ? null : credentials.read(base).key;
  const initial = await postProbability(fetchImpl, originalRequest, null, { base, key });
  if (initial.status !== 402) {
    return redactSensitive({
      state: responseState(initial), httpStatus: initial.status,
      response: normalizeResponseForDisplay(initial.body),
    });
  }
  if (!perCall) return { state: key ? "pack_exhausted" : "payment_choice_required", choices: ["topup", "import", "per_call"] };
  return preparePayment({ initial, originalRequest, base, path: "probability", wallet, intents });
}

function divergenceResult(result, request, paid = false) {
  const output = redactSensitive({ state: responseState(result), httpStatus: result.status,
    response: normalizeResponseForDisplay(result.body) });
  if (output.state === "complete") {
    try {
      output.rows_markdown = formatDivergenceRows(output.response, request);
      return firstDivergencePage(output, request);
    }
    catch (error) {
      output.state = "invalid_response";
      output.error = { code: error.code, message: error.message };
      output.next = "The response cannot be displayed as a divergence ranking. Report any returned billing route and quota; only missing billing evidence is uncertain. Do not retry automatically.";
    }
  } else if (paid) output.state = "payment_failed";
  return output;
}

export async function prepareDivergence({ limit, labels, fetchImpl = fetch,
  wallet = createBinanceWalletRunner(), intents = createFileIntentStore(), base = apiBase(),
  credentials = createCredentials(), perCall = false } = {}) {
  validateDivergenceLimit(limit);
  labels = validateDivergenceLabels(labels);
  base = apiBase(base);
  const originalRequest = { ...(limit === undefined ? {} : { limit }), labels };
  const key = perCall ? null : credentials.read(base).key;
  const headers = key ? { "COURNOT-API-KEY": key } : {};
  const initial = await apiRequest({ base, path: "divergence", limit, headers, fetchImpl });
  if (initial.status !== 402) return divergenceResult(initial, originalRequest);
  if (!perCall) return { state: key ? "pack_exhausted" : "payment_choice_required", choices: ["topup", "import", "per_call"] };
  return preparePayment({ initial, originalRequest, base, path: "divergence", wallet, intents,
    presentationRequest: { message: labels.cournot_above, operation: "divergence" } });
}

export async function preparePack({ packId, language = "en", fetchImpl = fetch,
  wallet = createBinanceWalletRunner(), intents = createFileIntentStore(), base = apiBase() } = {}) {
  const pack = PACKS.find((item) => item.pack_id === String(packId).trim().toLowerCase());
  if (!pack) fail("Select a valid pack: p5, p20, or p50");
  base = apiBase(base);
  const request = { pack_id: pack.pack_id };
  const initial = await apiRequest({ base, path: "packs", method: "POST", body: request, fetchImpl });
  if (initial.status !== 402) return { state: "api_error", httpStatus: initial.status, response: sanitize(initial.body) };
  const result = await preparePayment({ initial, originalRequest: request, base, path: "packs", wallet, intents,
    presentationRequest: { ...request, message: language === "zh" ? "购买" : "Purchase" } });
  return { ...result, pack, base, notice: "Calls never expire and are non-refundable. Losing both wallet and key prevents recovery. Credit belongs to the paying wallet; its key replaces this machine's saved key after purchase. Payment terms come from the actual payment preview." };
}

async function preparePayment({ initial, originalRequest, base, path, wallet, intents, presentationRequest = originalRequest }) {
  if (!initial.paymentRequired) {
    fail("Cournot 402 response is missing PAYMENT-REQUIRED", "INVALID_402");
  }

  const paymentRequired = initial.paymentRequired.replaceAll(/\s/g, "");
  const requirements = parsePaymentRequirements(paymentRequired);
  const serverOptions = publicServerOptions(requirements);
  if (typeof wallet.preflight === "function") {
    let preflight;
    try {
      preflight = wallet.preflight();
    } catch (error) {
      return walletFailureResult({
        error,
        base,
        operation: "preflight",
        request: presentationRequest,
        serverOptions,
      });
    }
    if (preflight?.connected !== true) {
      return walletRequiredResult({
        base,
        request: presentationRequest,
        reason: "WALLET_NOT_CONNECTED",
        walletStatus: preflight?.status ?? "UNKNOWN",
        serverOptions,
      });
    }
  }
  let preview;
  try {
    preview = wallet.preview(paymentRequired);
  } catch (error) {
    return walletFailureResult({
      error,
      base,
      operation: "preview",
      request: presentationRequest,
      serverOptions,
    });
  }
  if (
    preview?.success !== true ||
    typeof preview?.data?.paymentId !== "string" ||
    !Array.isArray(preview?.data?.options)
  ) {
    fail("Binance Agentic Wallet preview failed", "WALLET_PREVIEW_FAILED");
  }

  const { ready, blockers } = sanitizePreviewOptions(
    preview.data.options,
    requirements
  );
  if (ready.length === 0) {
    return {
      state: "wallet_blocked",
      base,
      serverOptions,
      blockers: publicBlockers(blockers),
    };
  }

  const intentId = intents.save({
    kind: "payment", base, path,
    request: originalRequest,
    requirements,
    walletPaymentId: preview.data.paymentId,
    ready,
  });
  return {
    state: "payment_confirmation_required",
    base,
    intentId,
    serverOptions,
    options: publicReadyOptions(ready),
    blockers: publicBlockers(blockers),
  };
}

function parseSignedPayment(result) {
  if (
    result?.success !== true ||
    result?.data?.paymentHeaderName !== "PAYMENT-SIGNATURE" ||
    typeof result?.data?.paymentHeaderValue !== "string" ||
    result.data.paymentHeaderValue === ""
  ) {
    fail("Binance Agentic Wallet signing failed", "WALLET_SIGN_FAILED");
  }
  return result.data;
}

// Retry only a specific authorization precheck rejection, never an ambiguous
// settlement/network failure. The original signed header and request are reused.
async function submitSignedPayment({ paymentHeader, now, wait, method = "POST", ...request }) {
  let window;
  try {
    const authorization = JSON.parse(Buffer.from(paymentHeader, "base64").toString("utf8")).payload.authorization;
    const timestamps = [authorization?.validAfter, authorization?.validBefore];
    if (timestamps.every((value) => /^\d+$/.test(String(value)))) {
      const [after, before] = timestamps.map((value) => Number(value) * 1000);
      if ([after, before].every(Number.isSafeInteger) && after < before) window = { after, before };
    }
  } catch { /* Other supported payment schemes may not have an authorization window. */ }
  const send = () => apiRequest({ ...request, method, headers: { "PAYMENT-SIGNATURE": paymentHeader } });
  if (window && now() + PAYMENT_SETTLE_DELAY_MS >= window.before) {
    fail("Payment authorization expires before submission", "PAYMENT_AUTHORIZATION_EXPIRED");
  }
  await wait(PAYMENT_SETTLE_DELAY_MS);
  if (window && now() >= window.before) {
    fail("Payment authorization expired before submission", "PAYMENT_AUTHORIZATION_EXPIRED");
  }
  const response = await send();
  if (response.body?.code !== 22000 || ![
    "authorization_not_yet_valid", "EIP3009: authorization is not yet valid",
  ].includes(response.body?.msg) || response.status >= 500 || response.status === 429
    || response.body?.data?.charged || response.body?.data?.x402?.txn_hash) return response;
  if (!window) return response;
  const { after, before } = window;
  const current = now();
  const delay = Math.max(3000, after + 3000 - current);
  if (delay > 10000 || current + delay >= before) return response;
  await wait(delay);
  if (now() >= before || now() < after + 3000) return response;
  return send();
}

export async function executePayment({
  intentId,
  selectedOption,
  confirmed,
  fetchImpl = fetch,
  wallet = createBinanceWalletRunner(),
  intents = createFileIntentStore(),
  base = apiBase(), credentials = createCredentials(),
  now = () => Date.now(), wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
} = {}) {
  if (confirmed !== true) {
    fail("Explicit user confirmation is required", "CONFIRMATION_REQUIRED");
  }
  if (!Number.isInteger(selectedOption) || selectedOption < 1) {
    fail("A valid displayed payment option is required");
  }

  const lease = intents.take(intentId);
  const intent = lease.value;
  if (intent.kind !== "payment" || intent.base !== apiBase(base) || !["probability", "divergence", "packs"].includes(intent.path)) {
    lease.restore();
    fail("Payment intent belongs to another operation or environment", "INTENT_MISMATCH");
  }
  if (intent.path === "divergence") {
    try {
      if (!isObject(intent.request)) fail("Invalid divergence payment request");
      validateDivergenceLimit(intent.request.limit);
      validateDivergenceLabels(intent.request.labels);
    } catch (error) { lease.restore(); throw error; }
  }
  const selected = intent.ready[selectedOption - 1];
  if (!selected) {
    lease.restore();
    fail("Selected payment option does not exist");
  }

  let signed;
  try {
    signed = parseSignedPayment(
      wallet.sign(intent.walletPaymentId, selected.walletOptionIndex)
    );
  } catch (error) {
    lease.consume();
    throw error;
  }

  try {
    if (signed.approveTxHash) {
      const confirmedApproval = await wallet.waitForApproval(
        signed.approveTxHash,
        signed.binanceChainId
      );
      if (!confirmedApproval) {
        return {
          state: "approval_pending",
          approveTxHash: signed.approveTxHash,
          binanceChainId: signed.binanceChainId ?? null,
          next: "Prepare a fresh payment after the approval confirms.",
        };
      }
    }

    let paymentHeader;
    try {
      paymentHeader = buildPaymentHeader(
        signed.paymentHeaderValue,
        intent.requirements,
        selected.originalAcceptIndex + 1
      );
    } catch (error) {
      fail("Wallet payment did not match the confirmed option", "PAYMENT_MISMATCH");
    }

    if (intent.path === "packs") {
      // Store the exact signed request before sending: recovery never signs or charges a new payment.
      const recoveryId = intents.save({ kind: "pack_recovery", base: intent.base, request: intent.request, paymentHeader });
      return recoverPack({ intentId: recoveryId, confirmed: true, base, credentials, intents, fetchImpl, now, wait });
    }
    const paid = await submitSignedPayment({ base: intent.base, path: intent.path,
      ...(intent.path === "divergence" ? { method: "GET", limit: intent.request.limit } : { body: intent.request }),
      paymentHeader, fetchImpl, now, wait });
    if (intent.path === "divergence") return divergenceResult(paid, intent.request, true);
    const settled = paid.status >= 200 && paid.status < 300 && paid.body?.code === 0;
    return redactSensitive({
      state: settled ? "complete" : "payment_failed", httpStatus: paid.status,
      response: normalizeResponseForDisplay(paid.body),
    });
  } finally {
    lease.consume();
  }
}

export async function recoverPack({ intentId, confirmed, base = apiBase(), credentials = createCredentials(),
  intents = createFileIntentStore(), fetchImpl = fetch,
  now = () => Date.now(), wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms)) } = {}) {
  if (confirmed !== true) fail("Explicit purchase recovery confirmation is required", "CONFIRMATION_REQUIRED");
  const lease = intents.take(intentId);
  const intent = lease.value;
  if (intent.kind !== "pack_recovery" || intent.base !== apiBase(base)) {
    lease.restore(); fail("Wrong recovery intent or environment", "INTENT_MISMATCH");
  }
  let response;
  try {
    response = await submitSignedPayment({ base: intent.base, path: "packs", body: intent.request,
      paymentHeader: intent.paymentHeader, fetchImpl, now, wait });
  } catch (error) {
    lease.restore();
    return { state: "purchase_unknown", recoveryId: intentId,
      error: { code: error.code || error.cause?.code || "PAYMENT_REQUEST_FAILED", message: sanitize(error.message) },
      next: "Do not purchase again. Explicitly recover this same payment or check the paying wallet's account." };
  }
  if (responseState(response) !== "complete") {
    lease.restore();
    return { state: "purchase_unknown", recoveryId: intentId, httpStatus: response.status, response: sanitize(response.body),
      next: "Do not sign a new payment. Check the wallet account or explicitly recover the same payment." };
  }
  lease.consume();
  const result = accountResult(response, { base, credentials, save: true });
  if (!result.hasKey) return { state: "credential_save_failed", next: "Purchase succeeded without a key. Recover via the paying wallet account; do not buy again." };
  return { ...result, pack: response.body.data.pack, x402: sanitize(response.body.data.x402), charged: response.body.data.charged };
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const args = {};
  for (let index = 0; index < rest.length; index += 2) {
    const key = rest[index];
    const value = rest[index + 1];
    if (!key?.startsWith("--") || value == null) {
      fail("Arguments must use --name value pairs");
    }
    args[key.slice(2)] = value;
  }
  return { command, args };
}

function decodeRequest(value) {
  if (typeof value !== "string" || value === "") {
    fail("--request-base64 is required");
  }
  try {
    return JSON.parse(Buffer.from(value, "base64").toString("utf8"));
  } catch {
    fail("--request-base64 must contain base64 JSON");
  }
}

function packSelection(language = "en") {
  const base = apiBase();
  const zh = language === "zh";
  const dev = base === "https://dev-interface.cournot.ai";
  const rows = PACKS.map(pack => `| ${pack.name} (${pack.pack_id}) | ${pack.calls.toLocaleString("en-US")} | $${pack.price_usd} |`).join("\n");
  const presentation = `| ${zh ? "套餐 | 次数 | 目录标价" : "Pack | Calls | List price"} |
|---|---:|---:|
${rows}

${dev ? (zh ? "当前每个套餐收费 $0.01。" : "Each pack currently costs $0.01. ") : ""}${zh ? "实际付款金额、资产和网络以随后展示的最新付款预览为准，确认后才会付款。" : "The latest payment preview determines the actual amount, asset and network; payment requires your confirmation."}

${zh ? "次数永久有效、可叠加，购买后不退款。额度归付款钱包所有；购买成功后会在本机保存该钱包的密钥，可能替换现有密钥。若同时失去钱包访问权和密钥，将无法恢复。主网付款会使用真实资产。" : "Calls never expire, stack, and are non-refundable. Credit belongs to the paying wallet; purchase saves its key on this device and may replace an existing key. Losing both wallet access and the key prevents recovery. Mainnet payments use real assets."}

${zh ? "你想选择哪个套餐？" : "Which pack would you like?"}`;
  return { state: "pack_selection_required", base, packs: PACKS, presentation };
}

async function runCli() {
  const usage = "Usage: cournot-client.mjs divergence --labels-json <localized-row-labels> [--limit <1-100> --count-text <original-count>] [--output json|markdown] [--per-call true] | divergence-page --snapshot <saved-file> --page <1-5> | resolve|prepare --request-base64 <json-base64> [--per-call true] | packs | topup --pack <id> | execute --intent <id> --selected-option <n> --confirmed true | balance | key | import (stdin) | auth-prepare --action account|rotate | auth-execute --intent <id> --confirmed true | auth-status --intent <id> | recover-purchase --intent <id> --confirmed true";
  const argv = process.argv.slice(2);
  if ((argv.length === 1 && argv[0] === "--help") || (argv.length === 2 && argv[1] === "--help")) return usage;
  const { command, args } = parseArgs(argv);
  if (command === "divergence-page") {
    if (Object.keys(args).some(key => !["snapshot", "page"].includes(key)) ||
        !/^\d+$/.test(args.page ?? "")) fail("Use divergence-page --snapshot <saved-file> --page <integer>");
    return redactSensitive(readDivergencePage(args.snapshot, Number(args.page)));
  }
  if (command === "divergence") {
    if (Object.keys(args).some((key) => !["limit", "count-text", "labels-json", "per-call", "output"].includes(key))) fail("Unknown divergence argument");
    if (args.limit !== undefined && !/^\d+$/.test(args.limit)) fail("Divergence limit must be an integer from 1 to 100");
    if (args["per-call"] !== undefined && !["true", "false"].includes(args["per-call"])) fail("--per-call must be true or false");
    if (args.output !== undefined && !["json", "markdown"].includes(args.output)) fail("--output must be json or markdown");
    const limit = args.limit === undefined ? undefined : Number(args.limit);
    validateDivergenceCountText(limit, args["count-text"]);
    let labels;
    if (args["labels-json"] !== undefined) {
      try { labels = JSON.parse(args["labels-json"]); } catch { fail("--labels-json must be a JSON object"); }
    }
    const result = await prepareDivergence({ limit, labels, perCall: args["per-call"] === "true" });
    return args.output === "markdown" && result.state === "complete" ? result.rows_markdown : result;
  }
  if (command === "prepare") {
    return prepareProbability({ request: decodeRequest(args["request-base64"]), perCall: args["per-call"] === "true" });
  }
  if (command === "execute") {
    return executePayment({
      intentId: args.intent,
      selectedOption: Number(args["selected-option"]),
      confirmed: args.confirmed === "true",
    });
  }
  if (command === "packs") return packSelection(args.language);
  if (command === "topup") return preparePack({ packId: args.pack, language: args.language });
  if (command === "recover-purchase") return recoverPack({ intentId: args.intent, confirmed: args.confirmed === "true" });
  if (command === "balance" || command === "key") return readAccount({ reveal: command === "key" });
  if (command === "import") {
    if (Object.keys(args).length) fail("Import accepts the key on stdin only");
    return readAccount({ importKey: readFileSync(0, "utf8").trim() });
  }
  if (command === "auth-prepare") return prepareAccountAuth({ action: args.action, reveal: args.reveal === "true", run: runBaw, intents: createFileIntentStore() });
  if (command === "auth-execute" || command === "auth-status") return executeAccountAuth({ intentId: args.intent,
    confirmed: args.confirmed === "true", poll: command === "auth-status", run: runBaw, intents: createFileIntentStore() });
  if (command === "resolve") {
    const response = await apiRequest({ path: "resolve", method: "POST", body: decodeRequest(args["request-base64"]) });
    return { state: responseState(response), response: sanitize(response.body) };
  }
  fail(usage);
}

function isMain() {
  try {
    return !!process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href;
  } catch { return false; }
}

if (isMain()) {
  try {
    const result = await runCli();
    console.log(typeof result === "string" ? result : JSON.stringify(result));
  } catch (error) {
    console.error(
      JSON.stringify({
        success: false,
        code: error.code || "COURNOT_CLIENT_ERROR",
        message: sanitize(error.message),
      })
    );
    process.exitCode = 1;
  }
}
