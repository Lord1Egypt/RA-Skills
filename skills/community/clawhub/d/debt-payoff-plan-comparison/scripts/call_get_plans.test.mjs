import assert from "node:assert/strict"
import { callGetPlans, parseArgs, sanitizeMarketing, validatePayload } from "./call_get_plans.mjs"

async function run(name, fn) {
  try {
    await fn()
    console.log(`PASS: ${name}`)
  } catch (error) {
    console.error(`FAIL: ${name}`)
    console.error(error.message)
    process.exitCode = 1
  }
}

function validPayload() {
  return {
    debts: [
      {
        debtType: "credit-card",
        balance: 15000,
        rate: 24,
        payment: 450,
      },
    ],
    assumptions: { homeAppraisal: 0 },
    diApplyToOC: 0,
    diApplyToDebt: 0,
  }
}

await run("parseArgs validates required args and default base URL", async () => {
  assert.throws(() => parseArgs([]), /Missing required --input/)
  const parsedDefault = parseArgs(["--input", "a.json"])
  assert.equal(parsedDefault.baseUrl, "https://loandoctor.app")

  const parsed = parseArgs([
    "--input",
    "a.json",
    "--base-url",
    "https://example.com",
    "--timeout-ms",
    "1234",
    "--infer-missing-rate",
    "--infer-missing-payment",
    "--allow-marketing-host",
    "example.com",
  ])
  assert.equal(parsed.timeoutMs, 1234)
  assert.equal(parsed.inferMissingRate, true)
  assert.equal(parsed.inferMissingPayment, true)
  assert.equal(parsed.allowedMarketingHosts.includes("example.com"), true)
})

await run("validatePayload rejects missing required fields", async () => {
  assert.throws(() => validatePayload({}), /debts/)
  assert.throws(() => validatePayload({ debts: [], assumptions: {}, diApplyToOC: 1, diApplyToDebt: 2 }), /at least one debt/)
})

await run("validatePayload enforces debt-level fields", async () => {
  const payload = validPayload()
  payload.debts[0].payment = 1
  assert.throws(() => validatePayload(payload), /greater than monthly interest/)
})

await run("validatePayload requires rate unless rate inference is enabled", async () => {
  const payload = validPayload()
  delete payload.debts[0].rate

  assert.throws(() => validatePayload(payload), /rate is required/)
})

await run("validatePayload can infer missing rate when opted in", async () => {
  const payload = validPayload()
  delete payload.debts[0].rate

  validatePayload(payload, { inferMissingRate: true })

  assert.equal(typeof payload.debts[0].rate, "number")
  assert.equal(payload.debts[0].rate > 0, true)
})

await run("validatePayload can infer missing payment when opted in", async () => {
  const payload = validPayload()
  delete payload.debts[0].payment

  validatePayload(payload, { inferMissingPayment: true })

  assert.equal(typeof payload.debts[0].payment, "number")
  assert.equal(payload.debts[0].payment > 0, true)
})

await run("sanitizeMarketing clamps untrusted URLs", async () => {
  const result = {
    success: true,
    plans: [],
    marketing: {
      ctaLabel: "Click me",
      ctaUrl: "https://evil.example/phish",
      secondaryCtaLabel: "Also this",
      secondaryCtaUrl: "http://evil.example/plain-http",
    },
  }

  sanitizeMarketing(result, ["loandoctor.app"])

  assert.equal(result.marketing.ctaUrl, "https://loandoctor.app")
  assert.equal(result.marketing.secondaryCtaUrl, "https://loandoctor.app")
})

await run("callGetPlans returns parsed json on success", async () => {
  const mockFetch = async () => ({
    ok: true,
    status: 200,
    text: async () => JSON.stringify({ success: true, plans: [] }),
    headers: { get: () => null },
  })

  const result = await callGetPlans({
    baseUrl: "https://example.com",
    payload: validPayload(),
    timeoutMs: 500,
    fetchImpl: mockFetch,
  })

  assert.equal(result.success, true)
})

await run("callGetPlans includes retry guidance when rate-limited", async () => {
  const mockFetch = async () => ({
    ok: false,
    status: 429,
    text: async () => JSON.stringify({ success: false, error: "RATE_LIMITED" }),
    headers: {
      get(key) {
        if (key.toLowerCase() === "retry-after") {
          return "9"
        }
        return null
      },
    },
  })

  let rejected = false

  try {
    await callGetPlans({
      baseUrl: "https://example.com",
      payload: validPayload(),
      timeoutMs: 500,
      fetchImpl: mockFetch,
    })
  } catch (error) {
    rejected = true
    assert.match(error.message, /Retry after 9s/)
  }

  assert.equal(rejected, true)
})
