#!/usr/bin/env node
/**
 * 验证 OpenClaw 运行时 clawbba provider 配置（baseUrl / apiKey / headers）。
 * setup.sh 在 sync models.json 之后调用。
 */
import fs from 'fs'
import {
  CLAWBBA_OPENCLAW_HEADERS,
  CLAWBBA_PROVIDER_DISPLAY_NAME,
  CLAWBBA_WEBCHAT_ASSISTANT_NAME,
} from './openclaw-provider-block.mjs'
import {
  discoverAgentModelPaths,
  getOpenclawHome,
  getOpenclawJsonPath,
} from './openclaw-paths.mjs'
import { buildSmokeChatModelCandidates } from './clawbba-vision-models.mjs'
import { clawbbaDebugLog } from './clawbba-debug-log.mjs'

function agentLog(location, message, data, hypothesisId) {
  clawbbaDebugLog({
    location,
    message,
    data,
    hypothesisId,
    runId: process.env.CLAWBBA_DEBUG_RUN_ID || 'pre-fix',
  })
}

const API_BASE = (process.env.CLAWBBA_API_BASE || 'https://www.clawbba.com/api/v1').replace(
  /\/$/,
  '',
)
const API_KEY = String(process.env.CLAWBBA_API_KEY || '').trim()
const openclawHome = getOpenclawHome()

function fail(msg) {
  process.stderr.write(`[clawbba-api] ✗ ${msg}\n`)
  process.exit(1)
}

function warn(msg) {
  process.stderr.write(`[clawbba-api] ⚠ ${msg}\n`)
}

function ok(msg) {
  process.stderr.write(`[clawbba-api] ✓ ${msg}\n`)
}

function checkProvider(name, provider) {
  if (!provider || typeof provider !== 'object') {
    fail(`${name}: provider 块缺失`)
  }
  const baseUrl = String(provider.baseUrl || '').replace(/\/$/, '')
  if (baseUrl !== API_BASE) {
    fail(
      `${name}: baseUrl 应为 ${API_BASE}，当前为 ${baseUrl || '(空)'}。OpenClaw 可能请求错误地址并出现 403 Your request was blocked`,
    )
  }
  const key = String(provider.apiKey || '').trim()
  if (key.startsWith('${') && key.endsWith('}')) {
    fail(
      `${name}: apiKey 仍是占位符 ${key}。请 export CLAWBBA_API_KEY 后重跑 setup.sh --yes，或 node scripts/fix-provider-config.mjs`,
    )
  }
  if (!key.startsWith('cbb_sk_live_')) {
    fail(`${name}: apiKey 格式无效（须 cbb_sk_live_ 开头）`)
  }
  const ua = provider.headers?.['User-Agent'] || provider.headers?.['user-agent']
  if (!ua) {
    fail(
      `${name}: 缺少 headers.User-Agent。OpenClaw WebChat 常见 403 Your request was blocked；请重跑 setup 或 fix-provider-config.mjs`,
    )
  }
  ok(`${name}: baseUrl + apiKey + User-Agent 正常`)
}

function checkAgentProviderDisplayName(name, provider) {
  const display = String(provider?.name || '').trim()
  if (display !== CLAWBBA_PROVIDER_DISPLAY_NAME) {
    fail(
      `${name}: providers.*.name 应为 ${CLAWBBA_PROVIDER_DISPLAY_NAME}（WebChat「from ClawBBA」），当前为 ${display || '(空)'}。请 node scripts/ensure-clawbba-session-branding.mjs`,
    )
  }
  ok(`${name}: display name = ${CLAWBBA_PROVIDER_DISPLAY_NAME}`)
}

async function fetchCatalogRows(apiKey) {
  const res = await fetch(`${API_BASE}/models`, {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      Accept: 'application/json',
      ...CLAWBBA_OPENCLAW_HEADERS,
    },
  })
  const text = await res.text()
  let body
  try {
    body = text ? JSON.parse(text) : {}
  } catch {
    body = {}
  }
  if (!res.ok) {
    agentLog('verify-openclaw-runtime.mjs:fetchCatalogRows', 'models fetch failed', {
      status: res.status,
      error: body.error || body.message || text.slice(0, 120),
    }, 'H2')
    return []
  }
  const rows = body.data ?? body.models ?? (Array.isArray(body) ? body : [])
  return Array.isArray(rows) ? rows : []
}

async function smokeChat(apiKey, configuredPrimary) {
  const catalogRows = await fetchCatalogRows(apiKey)
  const candidates = buildSmokeChatModelCandidates(configuredPrimary, catalogRows)
  agentLog(
    'verify-openclaw-runtime.mjs:smokeChat',
    'smoke candidates',
    { configuredPrimary, candidateCount: candidates.length, first: candidates[0] || null },
    'H1',
  )
  if (!candidates.length) {
    warn('POST /chat/completions 跳过：catalog 中无可用文本模型')
    return
  }

  let lastErr = null
  for (const model of candidates) {
    const res = await fetch(`${API_BASE}/chat/completions`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...CLAWBBA_OPENCLAW_HEADERS,
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: 'ping' }],
        max_tokens: 8,
      }),
    })
    const text = await res.text()
    if (res.ok) {
      agentLog('verify-openclaw-runtime.mjs:smokeChat', 'smoke ok', { model, status: res.status }, 'H1')
      ok(`POST /chat/completions → HTTP ${res.status} (model=${model})`)
      return
    }
    let body
    try {
      body = text ? JSON.parse(text) : {}
    } catch {
      body = { raw: text.slice(0, 120) }
    }
    const detail = body.error || body.message || text.slice(0, 120)
    agentLog('verify-openclaw-runtime.mjs:smokeChat', 'smoke attempt failed', {
      model,
      status: res.status,
      detail,
    }, 'H1')
    if (String(body.raw || body.message || '').includes('Your request was blocked')) {
      fail('POST /chat/completions 被 CDN/WAF 拦截（403 blocked）。请检查 headers.User-Agent')
    }
    if (res.status === 401 || res.status === 403) {
      fail(`POST /chat/completions → HTTP ${res.status}: ${detail}`)
    }
    lastErr = { model, status: res.status, detail }
    if (res.status === 404) continue
  }

  warn(
    `POST /chat/completions 未成功（已试 ${candidates.length} 个模型，末次 HTTP ${lastErr?.status}: ${lastErr?.detail}）。Key 若已通过 verify-key，可忽略此项或检查账户余额`,
  )
}

const modelPaths = discoverAgentModelPaths(openclawHome)
if (!modelPaths.length) {
  warn(`未发现 agent models.json，跳过本地 provider 检查`)
} else {
  for (const modelPath of modelPaths) {
    const rel = modelPath.startsWith(openclawHome)
      ? modelPath.slice(openclawHome.length + 1)
      : modelPath
    const agentModels = JSON.parse(fs.readFileSync(modelPath, 'utf8'))
    checkProvider(`${rel} → clawbba`, agentModels.providers?.clawbba)
    checkAgentProviderDisplayName(`${rel} → clawbba`, agentModels.providers?.clawbba)
    if (agentModels.providers?.openrouter) {
      checkProvider(`${rel} → ClawBBA 媒体`, agentModels.providers.openrouter)
      checkAgentProviderDisplayName(`${rel} → openrouter`, agentModels.providers.openrouter)
    }
  }
}

let chatPrimaryForSmoke = ''
const openclawJsonPath = getOpenclawJsonPath(openclawHome)
if (fs.existsSync(openclawJsonPath)) {
  const cfg = JSON.parse(fs.readFileSync(openclawJsonPath, 'utf8'))
  checkProvider('openclaw.json → clawbba', cfg.models?.providers?.clawbba)
  const envKey = String(cfg.env?.CLAWBBA_API_KEY || '').trim()
  if (envKey.startsWith('${')) {
    fail('openclaw.json env.CLAWBBA_API_KEY 仍为占位符，请重跑 setup 或 fix-provider-config.mjs')
  }
  if (!envKey.startsWith('cbb_sk_live_')) {
    fail('openclaw.json env.CLAWBBA_API_KEY 无效')
  }
  ok('openclaw.json env 已写入真实 Key')

  const imgPrimary = String(cfg.agents?.defaults?.imageGenerationModel?.primary || '').trim()
  const vidPrimary = String(cfg.agents?.defaults?.videoGenerationModel?.primary || '').trim()
  if (imgPrimary.startsWith('clawbba/')) {
    fail(
      `imageGenerationModel.primary 不能为 ${imgPrimary}。须为 ClawBBA 默认生图模型（setup 写入）或重跑 setup.sh；文本对话仅用 clawbba/`,
    )
  }
  if (vidPrimary.startsWith('clawbba/')) {
    fail(
      `videoGenerationModel.primary 不能为 ${vidPrimary}。须为 ClawBBA 默认生视频模型（setup 写入）或重跑 setup.sh`,
    )
  }
  if (imgPrimary) ok(`imageGenerationModel.primary = ${imgPrimary}`)
  if (vidPrimary) ok(`videoGenerationModel.primary = ${vidPrimary}`)

  const visionPrimary = String(cfg.agents?.defaults?.imageModel?.primary || '').trim()
  if (visionPrimary.startsWith('openrouter/')) {
    fail(
      `imageModel.primary 不能为 ${visionPrimary}（ClawBBA 生图路由）。聊天看图须 clawbba/<vision-文本模型>；请重跑 setup.sh 或 fix-openclaw-vision-config.mjs`,
    )
  }
  if (visionPrimary && /flux\.|seedream|gemini-.*-image|dall-e/i.test(visionPrimary)) {
    fail(`imageModel.primary 误为生图模型: ${visionPrimary}`)
  }
  if (visionPrimary && /gemini-2\.0-flash/i.test(visionPrimary)) {
    fail(
      `imageModel.primary=${visionPrimary} 已废弃（上游 404）。请执行: CLAWBBA_API_KEY=… node scripts/fix-openclaw-vision-config.mjs && openclaw gateway restart`,
    )
  }
  const chatPrimary = String(cfg.agents?.defaults?.model?.primary || '').trim()
  chatPrimaryForSmoke = chatPrimary.startsWith('clawbba/') ? chatPrimary.slice('clawbba/'.length) : chatPrimary
  if (visionPrimary && chatPrimary && visionPrimary !== chatPrimary) {
    fail(
      `imageModel.primary (${visionPrimary}) 应与对话 model.primary (${chatPrimary}) 一致。ClawBBA 不再自动切换到 Gemini 看图；请重跑 setup.sh 或 fix-openclaw-vision-config.mjs`,
    )
  }
  if (visionPrimary) ok(`imageModel.primary = ${visionPrimary}`)

  if (!chatPrimary.startsWith('clawbba/')) {
    fail(
      `agents.defaults.model.primary 应为 clawbba/<文本模型>，当前为 ${chatPrimary || '(空)'}。请重跑 one-shot-setup.sh`,
    )
  }
  ok(`agents.defaults.model.primary = ${chatPrimary}`)

  const uiAssistantName = String(cfg.ui?.assistant?.name || '').trim()
  if (uiAssistantName !== CLAWBBA_WEBCHAT_ASSISTANT_NAME) {
    fail(
      `ui.assistant.name 应为「${CLAWBBA_WEBCHAT_ASSISTANT_NAME}」（WebChat 消息署名），当前为 ${uiAssistantName || '(空)'}。请 node scripts/ensure-clawbba-session-branding.mjs`,
    )
  }
  ok(`ui.assistant.name = ${uiAssistantName}`)

  if (Array.isArray(cfg.agents?.list)) {
    for (const agent of cfg.agents.list) {
      const id = String(agent?.id || '').trim() || '(unnamed)'
      const primary = String(agent?.model?.primary || '').trim()
      if (primary && !primary.startsWith('clawbba/')) {
        fail(
          `agents.list[${id}].model.primary 应为 clawbba/…（当前 ${primary}）。请重跑 one-shot-setup.sh`,
        )
      }
    }
  }

  const clawbbaModels = cfg.models?.providers?.clawbba?.models
  if (chatPrimary.startsWith('clawbba/') && Array.isArray(clawbbaModels)) {
    const mid = chatPrimary.slice('clawbba/'.length)
    const def = clawbbaModels.find((m) => String(m?.id || '').trim() === mid)
    if (def && Array.isArray(def.input) && !def.input.includes('image')) {
      warn(
        `当前文本模型 ${chatPrimary} 在 provider 中未标记 image input；上传图可能被 offload。请重跑 setup.sh 或 fix-openclaw-provider-schema.mjs`,
      )
    }
  }
}

const keyForSmoke = API_KEY
if (!keyForSmoke.startsWith('cbb_sk_live_')) {
  warn('未设置 CLAWBBA_API_KEY，跳过在线 smoke test')
  process.exit(0)
}

await smokeChat(keyForSmoke, chatPrimaryForSmoke)
