import { randomUUID } from 'node:crypto'
import { readFileSync } from 'node:fs'

const API = '/api/v1'
const own = (o, k) => Object.prototype.hasOwnProperty.call(o, k)

export class EasySerpError extends Error {
  constructor(code, { status, requestId, idempotencyKey, pending = false, outcomeUnknown = false, retryAfterSeconds, snapshot } = {}) {
    super(code === 'request_pending' ? 'Request is still processing.' : 'EasySerp request failed.')
    this.name = 'EasySerpError'
    this.code = code
    this.status = status
    this.requestId = requestId
    this.idempotencyKey = idempotencyKey
    this.pending = pending
    this.outcomeUnknown = outcomeUnknown
    this.retryAfterSeconds = retryAfterSeconds
    this.snapshot = snapshot
  }
  toJSON() {
    const data = { ...(this.snapshot ?? {}) }
    if (own(data, 'status')) { data.request_status = data.status; delete data.status }
    return { name: this.name, code: this.code, ...(this.status !== undefined && { http_status: this.status }), ...(this.requestId && { request_id: this.requestId }), ...(this.idempotencyKey && { idempotency_key: this.idempotencyKey }), ...data, ...(this.attempt_history && { attempt_history: this.attempt_history }), ...(this.recovery_keys && { recovery_keys: this.recovery_keys }), ...(this.charged_total !== undefined && { charged_total: this.charged_total }), ...(this.charged_total_known !== undefined && { charged_total_known: this.charged_total_known }), ...(this.pending && { pending: true }), ...(this.outcomeUnknown && { outcome_unknown: true }), ...(this.retryAfterSeconds !== undefined && { retry_after_seconds: this.retryAfterSeconds }), ...((this.outcomeUnknown || this.code === 'transport_unknown') && { recovery_guidance: this.idempotencyKey ? 'Retry the same request with the same idempotency key to recover its outcome.' : this.requestId ? 'Retry the request lookup with the same request ID.' : undefined }) }
  }
}

function baseURL(value) {
  let url
  try { url = new URL(value || 'https://serp.skyvora.cc') } catch { throw new TypeError('baseUrl must be a valid URL') }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) throw new TypeError('baseUrl must be an HTTP(S) origin/path without credentials, query, or fragment')
  const loopback = ['localhost', '127.0.0.1', '::1', '[::1]'].includes(url.hostname)
  if (url.protocol !== 'https:' && !loopback) throw new TypeError('baseUrl must use HTTPS except for loopback hosts')
  return url.toString().replace(/\/$/, '')
}
function validate(params) {
  if (!params || typeof params !== 'object' || Array.isArray(params)) throw new TypeError('search params must be an object')
  const allowed = new Set(['engine','q','region','device','idempotency_key','wait_ms','max_attempts','channel','resolve_urls','gl','hl','mkt','cc','count','start','cursor'])
  for (const key of Object.keys(params)) if (!allowed.has(key)) throw new TypeError(`unsupported search parameter: ${key}`)
  const p = { ...params }
  if (typeof p.q === 'string' && /[\0\r\n]/.test(p.q)) throw new TypeError('q must not contain NUL or newlines')
  p.engine ??= 'google'; p.region ??= 'US'; p.device ??= 'desktop'; p.idempotency_key ??= randomUUID()
  if (typeof p.q === 'string') p.q = p.q.trim()
  if (typeof p.cursor === 'number' && Number.isSafeInteger(p.cursor)) p.cursor = String(p.cursor)
  if (!['google','bing'].includes(p.engine)) throw new TypeError('engine must be google or bing')
  const queryChars = typeof p.q === 'string' ? Array.from(p.q).length : 0
  if (typeof p.q !== 'string' || queryChars < 1 || queryChars > 200 || /[\0\r\n]/.test(p.q)) throw new TypeError('q must be 1..200 characters without NUL or newlines')
  if (typeof p.region !== 'string' || !/^[A-Za-z]{2}$/.test(p.region)) throw new TypeError('region must be a two-letter country code')
  p.region = p.region.toUpperCase()
  if (!['desktop','mobile'].includes(p.device)) throw new TypeError('device must be desktop or mobile')
  if (typeof p.idempotency_key !== 'string' || Buffer.byteLength(p.idempotency_key.trim()) < 8 || Buffer.byteLength(p.idempotency_key.trim()) > 128 || !p.idempotency_key.trim()) throw new TypeError('idempotency_key must be 8..128 bytes after trimming')
  if (p.wait_ms !== undefined && (!Number.isInteger(p.wait_ms) || p.wait_ms < 0 || p.wait_ms > 30000)) throw new TypeError('wait_ms must be an integer from 0 to 30000')
  if (p.max_attempts !== undefined && (!Number.isInteger(p.max_attempts) || p.max_attempts < 1 || p.max_attempts > 3)) throw new TypeError('max_attempts must be 1..3')
  if (p.channel !== undefined && (typeof p.channel !== 'string' || Buffer.byteLength(p.channel) > 64)) throw new TypeError('channel must be at most 64 bytes')
  for (const k of ['gl','hl','mkt','cc']) if (p[k] !== undefined && (typeof p[k] !== 'string' || !p[k].length || Buffer.byteLength(p[k]) > 16 || /[\0\r\n]/.test(p[k]))) throw new TypeError(`${k} must be a non-empty locale of at most 16 bytes`)
  if (p.resolve_urls !== undefined && typeof p.resolve_urls !== 'boolean') throw new TypeError('resolve_urls must be boolean')
  if (p.engine === 'google' && ['mkt','cc'].some(k => own(p,k))) throw new TypeError('mkt and cc are Bing-only')
  if (p.engine === 'bing' && own(p,'resolve_urls')) throw new TypeError('resolve_urls is Google-only')
  if (p.engine === 'bing' && p.channel !== undefined && (typeof p.channel !== 'string' || Buffer.byteLength(p.channel) > 64)) throw new TypeError('channel must be at most 64 bytes')
  if (p.count !== undefined && (!Number.isInteger(p.count) || p.count < 10 || p.count > 50)) throw new TypeError('count must be 10..50')
  if (p.start !== undefined && (!Number.isInteger(p.start) || p.start < 0 || p.start > 10000)) throw new TypeError('start must be 0..10000')
  if (p.cursor !== undefined) {
    const min = p.engine === 'google' ? 0 : 1; const max = p.engine === 'google' ? 10000 : 10001
    if (typeof p.cursor !== 'string' || !/^(0|[1-9]\d*)$/.test(p.cursor) || Number(p.cursor) < min || Number(p.cursor) > max) throw new TypeError(`cursor must be a canonical integer string from ${min} to ${max}`)
    if (p.start > 0 && Number(p.cursor) !== p.start + (p.engine === 'bing' ? 1 : 0)) throw new TypeError('cursor must match start for the selected engine')
  }
  if (p.engine === 'bing') {
    const alpha = /^[A-Za-z]+$/
    if (p.mkt !== undefined && !/^[A-Za-z]{2,3}-[A-Za-z]{2}$/.test(p.mkt)) throw new TypeError('Bing mkt must use language-country form, such as en-US')
    for (const k of ['cc','gl']) if (p[k] !== undefined && (!/^[A-Za-z]{2}$/.test(p[k]) || p[k].toUpperCase() !== p.region)) throw new TypeError(`${k} must be a two-letter country matching region`)
    if (p.hl !== undefined && (!alpha.test(p.hl) || p.hl.length < 2 || p.hl.length > 3)) throw new TypeError('Bing hl must be 2..3 letters')
  }
  return p
}

function safeCode(code, fallback) {
  return typeof code === 'string' && /^[a-zA-Z0-9_-]{1,64}$/.test(code) ? code : fallback
}
function retryAfter(response) {
  const raw = response.headers?.get?.('retry-after')
  if (!raw) return undefined
  const seconds = /^\d+(?:\.\d+)?$/.test(raw) ? Number(raw) : (Date.parse(raw) - Date.now()) / 1000
  if (!Number.isFinite(seconds)) return undefined
  return Math.max(0, Math.min(3600, Math.ceil(seconds)))
}
const publicFields = ['request_id','status','timestamp','server_duration_ms','search_parameters','organic','related_searches','related_questions','pagination','charged','settlement_pending']
function publicPayload(payload) {
  const result = {}
  for (const field of publicFields) if (own(payload, field)) result[field] = payload[field]
  return result
}

export class EasySerpClient {
  constructor({ apiKey, apiKeyFile, baseUrl, timeoutMs = 35000, fetchImpl = globalThis.fetch } = {}) {
    const envKey = process.env.EASYSERP_API_KEY || process.env.SKYVORA_API_KEY || process.env.SERP_API_TOKEN
    if (apiKey !== undefined) this.apiKey = apiKey
    else if (envKey) this.apiKey = envKey
    else {
      const keyFile = apiKeyFile ?? process.env.EASYSERP_API_KEY_FILE
      if (keyFile !== undefined) {
        try { this.apiKey = readFileSync(keyFile, 'utf8').trim() }
        catch { throw new TypeError('API key file could not be read') }
      }
    }
    if (typeof this.apiKey !== 'string' || !this.apiKey.trim() || /[\0\r\n]/.test(this.apiKey)) throw new TypeError('API key is missing or invalid')
    this.baseUrl = baseURL(baseUrl ?? process.env.EASYSERP_BASE_URL ?? process.env.SKYVORA_BASE_URL)
    if (!Number.isFinite(timeoutMs) || timeoutMs < 1) throw new TypeError('timeoutMs must be at least 1')
    if (typeof fetchImpl !== 'function') throw new TypeError('fetchImpl must be a function')
    this.timeoutMs = timeoutMs; this.fetchImpl = fetchImpl
  }
  async #request(path, { method = 'GET', body, signal, idempotencyKey, requestId, timeoutMs = this.timeoutMs } = {}) {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), timeoutMs)
    const abort = () => controller.abort(signal?.reason)
    if (signal?.aborted) abort(); else signal?.addEventListener('abort', abort, { once: true })
    try {
      const response = await this.fetchImpl(`${this.baseUrl}${API}${path}`, { method, redirect: 'error', signal: controller.signal, headers: { Authorization: `Bearer ${this.apiKey}`, Accept: 'application/json', ...(body && { 'Content-Type': 'application/json' }), ...(idempotencyKey && { 'Idempotency-Key': idempotencyKey }) }, ...(body && { body: JSON.stringify(body) }) })
      let payload
      try { payload = await response.json() } catch { payload = null }
      const e = payload?.error
      const pendingStatus = ['queued','running'].includes(payload?.status)
      if ((response.status === 202 && (pendingStatus || e?.code === 'request_pending')) || (response.status === 504 && e?.code === 'request_pending')) {
        return { ...publicPayload(payload), status: payload?.status ?? e?.status ?? 'queued', ...(idempotencyKey && { idempotency_key: idempotencyKey }) }
      }
      if (!response.ok) throw new EasySerpError(safeCode(e?.code, `http_${response.status}`), { status: response.status, requestId: payload?.request_id ?? requestId, idempotencyKey, snapshot: payload && typeof payload === 'object' && !Array.isArray(payload) ? publicPayload(payload) : undefined, retryAfterSeconds: response.status === 429 ? retryAfter(response) : undefined })
      if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw new EasySerpError('response_invalid', { status: response.status, requestId, idempotencyKey, outcomeUnknown: method === 'POST' })
      const validStates = method === 'POST' ? ['succeeded'] : ['queued','running','succeeded','failed']
      const validState = validStates.includes(payload.status)
      const validOrganic = payload.status !== 'succeeded' || Array.isArray(payload.organic)
      if (!validState || !validOrganic) throw new EasySerpError(payload.status === 'failed' && method === 'POST' ? 'request_failed' : 'response_invalid', { status: response.status, requestId: payload.request_id ?? requestId, idempotencyKey, snapshot: publicPayload(payload), outcomeUnknown: method === 'POST' && payload.status !== 'failed' })
      return publicPayload(payload)
    } catch (err) {
      if (err instanceof EasySerpError) throw err
      throw new EasySerpError('transport_unknown', { requestId, idempotencyKey, outcomeUnknown: method === 'POST' })
    } finally { clearTimeout(timer); signal?.removeEventListener('abort', abort) }
  }
  async search(params, { signal, timeoutMs = this.timeoutMs } = {}) {
    const input = validate(params)
    const start = performance.now()
    const data = await this.#request('/search', { method: 'POST', body: input, signal, idempotencyKey: input.idempotency_key, timeoutMs })
    return { ...data, idempotency_key: input.idempotency_key, client_duration_ms: Math.round((performance.now() - start) * 100) / 100 }
  }
  /** Search for a user-facing result set while preserving search() as the raw API operation. */
  async searchRelevant(params, { signal, retries = 2, deadlineMs = 120000, includeDomains = [], excludeDomains = [] } = {}) {
    if (!Number.isInteger(retries) || retries < 0 || retries > 2) throw new TypeError('retries must be 0..2')
    if (!Number.isFinite(deadlineMs) || deadlineMs < 1) throw new TypeError('deadlineMs must be at least 1')
    const includes = normalizeDomains(includeDomains, 'includeDomains')
    const excludes = normalizeDomains(excludeDomains, 'excludeDomains')
    const original = validate(params)
    const deadline = Date.now() + deadlineMs
    const history = []
    let current = { ...original }
    let last
    for (let attempt = 0; attempt <= retries; attempt++) {
      if (signal?.aborted) throw new EasySerpError('aborted', { idempotencyKey: current.idempotency_key, outcomeUnknown: history.length > 0 })
      if (Date.now() >= deadline) break
      try {
        const remaining = deadline - Date.now()
        if (remaining <= 0) break
        last = await this.search(current, { signal, timeoutMs: Math.min(this.timeoutMs, remaining) })
        history.push({ attempt: attempt + 1, q: original.q, status: last.status, request_id: last.request_id, charged: last.charged, idempotency_key: current.idempotency_key })
        // Pending receipts are useful recovery handles; polling/re-submitting could obscure settlement.
        if (['queued','running'].includes(last.status)) return decorateRelevant(last, original.q, includes, excludes, history)
        return decorateRelevant(last, original.q, includes, excludes, history)
      } catch (error) {
        const safe = error instanceof EasySerpError ? error : new EasySerpError('client_error')
        let snap = safe.snapshot ?? {}
        // A terminal HTTP error may omit settlement fields. Confirm it once through the public request API.
        if (safe.requestId && (snap.status === 'failed' || safe.status >= 500) && (snap.charged === undefined || snap.settlement_pending === undefined) && !signal?.aborted && Date.now() < deadline) {
          try {
            const receipt = await this.getRequest(safe.requestId, { signal, timeoutMs: Math.min(this.timeoutMs, Math.max(1, deadline - Date.now())) })
            snap = receipt
            if (['queued','running'].includes(receipt.status)) return decorateRelevant({ ...receipt, idempotency_key: current.idempotency_key }, original.q, includes, excludes, [...history, { attempt: attempt + 1, q: original.q, status: receipt.status, request_id: receipt.request_id, charged: receipt.charged, idempotency_key: current.idempotency_key }])
            if (receipt.status === 'succeeded') return decorateRelevant({ ...receipt, idempotency_key: current.idempotency_key }, original.q, includes, excludes, [...history, { attempt: attempt + 1, q: original.q, status: receipt.status, request_id: receipt.request_id, charged: receipt.charged, idempotency_key: current.idempotency_key }])
          } catch { /* Keep the original safe receipt and recovery identity. */ }
        }
        const settledFailure = snap.status === 'failed' && snap.charged === 0 && snap.settlement_pending !== true
        const retryableUnknown = safe.outcomeUnknown || safe.code === 'transport_unknown' || safe.status === 429 || safe.status >= 500
        history.push({ attempt: attempt + 1, q: original.q, status: snap.status ?? 'unknown', request_id: safe.requestId, charged: snap.charged, idempotency_key: current.idempotency_key, error_code: safe.code })
        if (signal?.aborted) {
          safe.attempt_history = history; safe.recovery_keys = history.map(row => row.idempotency_key)
          applyChargeSummary(safe, history)
          throw safe
        }
        if (attempt >= retries || (!settledFailure && !retryableUnknown)) {
          safe.attempt_history = history
          safe.recovery_keys = history.map(row => row.idempotency_key)
          applyChargeSummary(safe, history)
          throw safe
        }
        // Unknown outcomes must retain the exact key and body. Rotate only after explicit free settlement.
        if (settledFailure) current = { ...current, idempotency_key: randomUUID() }
        const delay = retryDelay(safe.retryAfterSeconds, attempt)
        if (Date.now() + delay >= deadline) {
          safe.attempt_history = history; safe.recovery_keys = history.map(row => row.idempotency_key)
          applyChargeSummary(safe, history)
          throw safe
        }
        await pause(delay, signal)
      }
    }
    if (last) return decorateRelevant(last, original.q, includes, excludes, history)
    throw new EasySerpError('deadline_exceeded', { idempotencyKey: current.idempotency_key, outcomeUnknown: history.length > 0 })
  }
  async getRequest(id, { signal, timeoutMs = this.timeoutMs } = {}) {
    if (typeof id !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(id)) throw new TypeError('request id is invalid')
    return this.#request(`/requests/${encodeURIComponent(id)}`, { signal, requestId: id, timeoutMs })
  }
  async batchSearch(queries, { concurrency = 4, signal, relevant = false, retries = 2, includeDomains = [], excludeDomains = [], deadlineMs = 120000 } = {}) {
    if (!Array.isArray(queries) || queries.length > 100) throw new TypeError('queries must be an array of at most 100 items')
    if (!Number.isInteger(concurrency) || concurrency < 1 || concurrency > 32) throw new TypeError('concurrency must be 1..32')
    const results = new Array(queries.length); let next = 0
    await Promise.all(Array.from({ length: Math.min(concurrency, queries.length) }, async () => {
      while (next < queries.length) {
        if (signal?.aborted) break
        const index = next++
        try { results[index] = { index, ok: true, data: relevant ? await this.searchRelevant(queries[index], { signal, retries, includeDomains, excludeDomains, deadlineMs }) : await this.search(queries[index], { signal }) } }
        catch (error) { results[index] = { index, ok: false, error: error instanceof EasySerpError ? error.toJSON() : { name: 'EasySerpError', code: 'invalid_input' } } }
      }
    }))
    for (let i = 0; i < results.length; i++) if (!results[i]) results[i] = { index: i, ok: false, error: { name: 'EasySerpError', code: 'batch_aborted' } }
    const pending = results.filter(x => x.ok && ['queued','running'].includes(x.data.status)).length
    const succeeded = results.filter(x => x.ok && !['queued','running'].includes(x.data.status)).length
    const unknown = results.filter(x => !x.ok && (x.error.outcome_unknown || x.error.code === 'transport_unknown')).length
    const failed = results.length - succeeded - pending - unknown
    return { results, summary: { total: results.length, succeeded, pending, failed, unknown } }
  }
}

function normalizeDomains(values, name) {
  if (values === undefined) return []
  if (!Array.isArray(values) || values.length > 50) throw new TypeError(`${name} must be an array of at most 50 domains`)
  return values.map(value => {
    if (typeof value !== 'string') throw new TypeError(`${name} entries must be domains`)
    const domain = value.trim().toLowerCase().replace(/^\.+|\.+$/g, '')
    if (!domain || domain.includes('/') || domain.includes(':') || !/^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:\.(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?))+$/.test(domain)) throw new TypeError(`${name} contains an invalid domain`)
    return domain
  })
}
function queryScope(q) {
  const includes = []; const excludes = []
  for (const match of q.matchAll(/(^|\s)(-?)site:([^\s]+)/gi)) {
    const domain = match[3].toLowerCase().replace(/^\*\./, '').replace(/[),;]+$/, '')
    if (domain) (match[2] ? excludes : includes).push(domain)
  }
  return { includes, excludes }
}
function hostMatches(host, domain) { return host === domain || host.endsWith(`.${domain}`) }
function canonicalURL(value) {
  try {
    const url = new URL(value)
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) return null
    url.hash = ''
    for (const key of [...url.searchParams.keys()]) if (/^(utm_.+|gclid|dclid|fbclid|msclkid|ref|ref_src|mc_cid|mc_eid)$/i.test(key)) url.searchParams.delete(key)
    url.hostname = url.hostname.toLowerCase()
    if (url.pathname !== '/') url.pathname = url.pathname.replace(/\/+$/, '')
    url.searchParams.sort()
    return url.toString().replace(/\/$/, '')
  } catch { return null }
}
function queryTerms(q) {
  const terms = q.toLocaleLowerCase().match(/[\p{L}\p{N}]{2,}/gu) ?? []
  const latin = terms.filter(term => /^[\p{Script=Latin}\p{N}]+$/u.test(term) && !/^(site|and|the|for|with|from|into|what|when|where|how|why)$/i.test(term))
  const cjk = terms.filter(term => /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u.test(term))
  return [...new Set([...latin, ...cjk])].slice(0, 20)
}
function decorateRelevant(data, q, includeDomains, excludeDomains, history) {
  const original = Array.isArray(data.organic) ? data.organic : []
  const queryDomains = queryScope(q)
  const scope = [...new Set(queryDomains.includes)]
  const excluded = [...new Set([...queryDomains.excludes, ...excludeDomains])]
  const terms = queryTerms(q)
  let out = original.map((row, index) => {
    const url = canonicalURL(row?.link)
    if (!url) return null
    let host
    try { host = new URL(row.link).hostname.toLowerCase() } catch { return null }
    if (excluded.some(domain => hostMatches(host, domain))) return null
    if ((scope.length && !scope.some(domain => hostMatches(host, domain))) || (includeDomains.length && !includeDomains.some(domain => hostMatches(host, domain)))) return null
    const text = `${row.title ?? ''} ${row.snippet ?? ''}`.toLocaleLowerCase()
    const matched = terms.reduce((count, term) => count + (text.includes(term) ? 1 : 0), 0)
    return { row, url, index, matched }
  }).filter(Boolean).sort((a, b) => b.matched - a.matched || a.index - b.index)
  const seen = new Set()
  out = out.filter(item => { if (seen.has(item.url)) return false; seen.add(item.url); return true }).map(item => item.row)
  const warnings = []
  if ((scope.length || includeDomains.length) && out.length === 0) warnings.push('source_scope_not_satisfied')
  if (original.length && out.length < original.length) warnings.push('results_filtered_or_deduplicated')
  const charges = chargeSummary(history)
  return { ...data, original_organic: original, organic: out, quality: { returned: out.length, original: original.length, scope_domains: scope, include_domains: includeDomains, excluded_domains: excluded, warnings }, ...(history.length > 0 && { attempt_history: history, recovery_keys: history.map(item => item.idempotency_key), ...(charges.known && { charged_total: charges.total }), charged_total_known: charges.known }) }
}
function chargeSummary(history) {
  const seen = new Map(); let total = 0; let known = true
  for (const [index, row] of history.entries()) {
    const identity = row.idempotency_key ? `key:${row.idempotency_key}` : row.request_id ? `request:${row.request_id}` : `attempt:${index}`
    const previous = seen.get(identity)
    if (!previous || (typeof previous.charged !== 'number' && typeof row.charged === 'number')) seen.set(identity, row)
  }
  for (const row of seen.values()) { if (typeof row.charged === 'number' && Number.isFinite(row.charged)) total += row.charged; else known = false }
  return { total, known }
}
function applyChargeSummary(target, history) {
  const charges = chargeSummary(history)
  if (charges.known) target.charged_total = charges.total
  target.charged_total_known = charges.known
}
function retryDelay(retryAfterSeconds, attempt) {
  return Math.min(3600000, Math.max(0, retryAfterSeconds !== undefined ? retryAfterSeconds * 1000 : 250 * (2 ** attempt)))
}
function pause(ms, signal) {
  if (signal?.aborted) return Promise.reject(new EasySerpError('aborted'))
  return new Promise((resolve, reject) => {
    const timer = setTimeout(done, ms)
    function done() { signal?.removeEventListener('abort', abort); resolve() }
    function abort() { clearTimeout(timer); signal?.removeEventListener('abort', abort); reject(new EasySerpError('aborted')) }
    signal?.addEventListener('abort', abort, { once: true })
  })
}

export { EasySerpClient as SkyvoraClient, EasySerpError as SkyvoraError }
