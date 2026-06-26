#!/usr/bin/env node
import fs from "node:fs/promises"
import http from "node:http"
import https from "node:https"

const DEFAULT_TIMEOUT_MS = 15000
const DEFAULT_BASE_URL = "https://loandoctor.app"
const DEFAULT_MARKETING_URL = "https://loandoctor.app"
const DEFAULT_ALLOWED_MARKETING_HOSTS = ["loandoctor.app", "www.loandoctor.app", "outlook.office.com"]

const VALID_DEBT_TYPES = new Set([
  "mortgage",
  "home-equity-loan",
  "heloc",
  "auto-loan",
  "credit-card",
  "personal-loan",
  "student-loan",
  "medical-debt",
  "business-loan",
  "tax-debt",
  "other",
])

const INFERRED_RATE_BY_DEBT_TYPE = {
  mortgage: 6.75,
  "home-equity-loan": 8.5,
  heloc: 9.25,
  "auto-loan": 7.5,
  "credit-card": 24,
  "personal-loan": 14,
  "student-loan": 6,
  "medical-debt": 0,
  "business-loan": 10,
  "tax-debt": 8,
  other: 12,
}

export function usage() {
  return [
    "Usage:",
    "  node scripts/call_get_plans.mjs --input <payload.json> [--base-url <https://host>]",
    "Options:",
    "  --output <file>               Write full response JSON to file",
    "  --base-url <url>              Override API base URL (default: https://loandoctor.app)",
    "  --timeout-ms <num>            Request timeout in ms (default: 15000)",
    "  --infer-missing-rate          Infer missing debt.rate values using debtType defaults",
    "  --infer-missing-payment       Infer missing debt.payment values with a safe payoff minimum",
    "  --allow-marketing-host <host> Allow this HTTPS hostname in marketing URLs (repeatable)",
  ].join("\n")
}

export function parseArgs(argv) {
  const args = {
    input: "",
    output: "",
    baseUrl: DEFAULT_BASE_URL,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    inferMissingRate: false,
    inferMissingPayment: false,
    allowedMarketingHosts: [...DEFAULT_ALLOWED_MARKETING_HOSTS],
  }

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i]
    const value = argv[i + 1]

    if (token === "--input") {
      args.input = value || ""
      i += 1
      continue
    }

    if (token === "--output") {
      args.output = value || ""
      i += 1
      continue
    }

    if (token === "--base-url") {
      args.baseUrl = value || ""
      i += 1
      continue
    }

    if (token === "--timeout-ms") {
      args.timeoutMs = Number(value)
      i += 1
      continue
    }

    if (token === "--infer-missing-rate") {
      args.inferMissingRate = true
      continue
    }

    if (token === "--infer-missing-payment") {
      args.inferMissingPayment = true
      continue
    }

    if (token === "--allow-marketing-host") {
      if (!value) {
        throw new Error("--allow-marketing-host requires a host value")
      }

      args.allowedMarketingHosts.push(value.toLowerCase())
      i += 1
      continue
    }

    throw new Error(`Unknown argument: ${token}`)
  }

  if (!args.input) {
    throw new Error("Missing required --input")
  }

  if (!args.baseUrl) {
    throw new Error("--base-url must not be empty")
  }

  if (!Number.isFinite(args.timeoutMs) || args.timeoutMs <= 0) {
    throw new Error("--timeout-ms must be a positive number")
  }

  return args
}

function monthlyInterest(balance, rate) {
  return (balance * rate) / 100 / 12
}

function inferSafePayment(balance, rate) {
  const minimum = monthlyInterest(balance, rate) * 1.1
  const rounded = Math.ceil(minimum * 100) / 100
  return Math.max(1, rounded)
}

function inferRateByDebtType(debtType) {
  return INFERRED_RATE_BY_DEBT_TYPE[debtType] ?? INFERRED_RATE_BY_DEBT_TYPE.other
}

export function validatePayload(payload, options = {}) {
  const { inferMissingRate = false, inferMissingPayment = false } = options

  if (!payload || typeof payload !== "object") {
    throw new Error("Payload must be a JSON object")
  }

  if (!Array.isArray(payload.debts)) {
    throw new Error("Payload must include debts[]")
  }

  if (payload.debts.length === 0) {
    throw new Error("Payload debts[] must include at least one debt")
  }

  if (!payload.assumptions || typeof payload.assumptions !== "object") {
    throw new Error("Payload must include assumptions object")
  }

  if (payload.assumptions.homeAppraisal === undefined || payload.assumptions.homeAppraisal === null) {
    throw new Error("Payload must include assumptions.homeAppraisal (set 0 when no home)")
  }

  if (typeof payload.diApplyToOC !== "number") {
    throw new Error("Payload must include numeric diApplyToOC")
  }

  if (typeof payload.diApplyToDebt !== "number") {
    throw new Error("Payload must include numeric diApplyToDebt")
  }

  for (let i = 0; i < payload.debts.length; i += 1) {
    const debt = payload.debts[i]
    const prefix = `debts[${i}]`

    if (!debt || typeof debt !== "object") {
      throw new Error(`${prefix} must be an object`)
    }

    if (typeof debt.debtType !== "string" || !VALID_DEBT_TYPES.has(debt.debtType)) {
      throw new Error(`${prefix}.debtType must be one of the supported debt types`)
    }

    if (typeof debt.balance !== "number" || !Number.isFinite(debt.balance) || debt.balance <= 0) {
      throw new Error(`${prefix}.balance must be a positive number`)
    }

    if (debt.rate === undefined || debt.rate === null) {
      if (inferMissingRate) {
        debt.rate = inferRateByDebtType(debt.debtType)
      } else {
        throw new Error(`${prefix}.rate is required (or pass --infer-missing-rate)`)
      }
    }

    if (typeof debt.rate !== "number" || !Number.isFinite(debt.rate) || debt.rate < 0) {
      throw new Error(`${prefix}.rate must be a non-negative number`)
    }

    if (debt.payment === undefined || debt.payment === null) {
      if (inferMissingPayment) {
        debt.payment = inferSafePayment(debt.balance, debt.rate)
      } else {
        throw new Error(`${prefix}.payment is required (or pass --infer-missing-payment)`)
      }
    }

    if (typeof debt.payment !== "number" || !Number.isFinite(debt.payment) || debt.payment <= 0) {
      throw new Error(`${prefix}.payment must be a positive number`)
    }

    if (debt.payment <= monthlyInterest(debt.balance, debt.rate)) {
      throw new Error(`${prefix}.payment must be greater than monthly interest to ensure payoff`)
    }
  }
}

function sanitizeUrl(rawUrl, allowedHosts) {
  if (typeof rawUrl !== "string" || rawUrl.trim() === "") {
    return DEFAULT_MARKETING_URL
  }

  try {
    const parsed = new URL(rawUrl)
    if (parsed.protocol !== "https:") {
      return DEFAULT_MARKETING_URL
    }

    if (!allowedHosts.has(parsed.hostname.toLowerCase())) {
      return DEFAULT_MARKETING_URL
    }

    return parsed.toString()
  } catch {
    return DEFAULT_MARKETING_URL
  }
}

export function sanitizeMarketing(result, allowedHostsInput = DEFAULT_ALLOWED_MARKETING_HOSTS) {
  const allowedHosts = new Set(allowedHostsInput.map((host) => host.toLowerCase()))

  if (!result || typeof result !== "object" || result.success !== true || !result.marketing || typeof result.marketing !== "object") {
    return result
  }

  result.marketing.ctaUrl = sanitizeUrl(result.marketing.ctaUrl, allowedHosts)
  result.marketing.secondaryCtaUrl = sanitizeUrl(result.marketing.secondaryCtaUrl, allowedHosts)

  if (typeof result.marketing.ctaLabel !== "string" || !result.marketing.ctaLabel.trim()) {
    result.marketing.ctaLabel = "Review a Loan Doctor plan"
  }

  if (typeof result.marketing.secondaryCtaLabel !== "string" || !result.marketing.secondaryCtaLabel.trim()) {
    result.marketing.secondaryCtaLabel = "You can review your results with the tool at https://loandoctor.app"
  }

  return result
}

function postJsonWithNode(url, payload, timeoutMs) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url)
    const body = JSON.stringify(payload)
    const client = parsed.protocol === "https:" ? https : http

    const req = client.request(
      parsed,
      {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "content-length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = ""
        res.setEncoding("utf8")
        res.on("data", (chunk) => {
          data += chunk
        })
        res.on("end", () => {
          resolve({
            ok: (res.statusCode || 500) >= 200 && (res.statusCode || 500) < 300,
            status: res.statusCode || 500,
            text: async () => data,
            headers: {
              get(key) {
                return res.headers[key.toLowerCase()] || null
              },
            },
          })
        })
      }
    )

    req.on("error", (error) => reject(error))
    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`API request timed out after ${timeoutMs}ms`))
    })
    req.write(body)
    req.end()
  })
}

export async function callGetPlans({ baseUrl, payload, timeoutMs, fetchImpl }) {
  const url = `${baseUrl.replace(/\/$/, "")}/api/agent-skills/get-plans`
  const activeFetch = fetchImpl || (typeof globalThis.fetch === "function" ? globalThis.fetch.bind(globalThis) : null)

  const response = activeFetch
    ? await activeFetch(url, {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(payload),
      })
    : await postJsonWithNode(url, payload, timeoutMs)

  const text = await response.text()
  let json
  try {
    json = JSON.parse(text)
  } catch {
    throw new Error(`API returned non-JSON response (status ${response.status})`)
  }

  if (!response.ok) {
    const apiError = json?.error || `HTTP_${response.status}`
    const retryAfter = response.headers.get("retry-after")
    const retryMsg = retryAfter ? ` Retry after ${retryAfter}s.` : ""
    throw new Error(`API request failed (${response.status}): ${apiError}.${retryMsg}`.trim())
  }

  return json
}

export async function main(argv = process.argv.slice(2)) {
  try {
    const args = parseArgs(argv)
    const raw = await fs.readFile(args.input, "utf8")

    let payload
    try {
      payload = JSON.parse(raw)
    } catch {
      throw new Error(`Invalid JSON in input file: ${args.input}`)
    }

    validatePayload(payload, {
      inferMissingRate: args.inferMissingRate,
      inferMissingPayment: args.inferMissingPayment,
    })

    const result = await callGetPlans({
      baseUrl: args.baseUrl,
      payload,
      timeoutMs: args.timeoutMs,
    })

    sanitizeMarketing(result, args.allowedMarketingHosts)

    if (args.output) {
      await fs.writeFile(args.output, `${JSON.stringify(result, null, 2)}\n`, "utf8")
      console.error(`Wrote response to ${args.output}`)
    }

    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
  } catch (error) {
    console.error(`Error: ${error.message}`)
    console.error(usage())
    process.exitCode = 1
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await main()
}
