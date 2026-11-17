// ─── Meta ────────────────────────────────────────────────────────
export const meta = {
  name: '1688-supplychain-order-inquiry-workflow',
  description: [
    '1688 订单询盘直连工作流：主 agent 不参与业务理解，调用方直接驱动。',
    '能力：inquiry_send（含 orders-detail 按单附件模式）/ inquiry_query / inquiry_config / configure 四个命令。',
    '⚠️ 多订单【问题相同】时必须在一次 workflow 调用内完成（无差异附件→orderIds 共用同一 question；逐单不同附件→ordersDetail，在这一次调用内部按订单逐单发下游、各订单各一次、互不重叠）。严禁因"每单附件不同"就把问题相同的多订单按订单拆成多路并行调用——那会让每一路都重解析全文、各自对全部订单再发一遍，导致每单被重复询盘。',
    '不做商品搜索、不做订单列表查询、不代商家作答、不处理非询盘类诉求、不提供跨订单不同问题的并行批量。',
    '入参两种模式：① params 结构化（带 command 字段，零 LLM 最快路径）',
    '② instruction 自然语言（workflow 内部 agent 解析意图，主 agent 仍不参与）。',
    'params 字段要点：question 目标总价格式 "目标总价<金额>" 无空格；',
    'orderSingleRound 三态 "true"/"false"/""（未提及留空）；ext 为 JSON 对象字符串；',
    'ordersDetail 需同时命中"按订单分配"关键词 + 逐订单列举才启用。',
    '输出：纯 JSON 字符串（首字符 { 或 [），每命令有独立 formatter，与 reference 中 "Agent 输出格式" 一致。',
  ].join('\n'),
  whenToUse:
    '用户就已生成的订单/采购单向商家提问或表达诉求（发货时间/物流单号/订单状态/订单议价/目标总价），或查询商家询盘回复，或配置订单询盘对话轮次，或配置访问 AK 时。不承接商品搜索、供应商询盘、找货、选品等非订单诉求。多订单问题相同时（含每单各带不同图/附件）一律在一次 workflow 调用内完成，不要因每单附件不同就按订单拆成多路并行调用。',
  phases: [
    { title: '意图解析', detail: '结构化入参直读，自然语言走 agent 解析' },
    { title: '参数校验', detail: '校验命令与必填参数，缺失直接返回错误 JSON' },
    { title: '询盘执行', detail: '按命令组装 CLI 参数并执行 cli.py' },
    { title: '结果输出', detail: '按各能力 Agent 输出格式生成纯 JSON' },
  ],
}

// ─── Utilities ───────────────────────────────────────────────────

// @utility:shellEscape
function shellEscape(arg) {
  const s = String(arg)
  if (/^[a-zA-Z0-9._\-\/:,=@]+$/.test(s)) return s
  if (typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)) {
    return '"' + s.replace(/"/g, '""') + '"'
  }
  return "'" + s.replace(/'/g, "'\\\\''") + "'"
}

// @utility:buildBashCommand
function buildBashCommand(program, args, description, timeout = 120000) {
  const isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const tmpDir = isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const sep = isWin ? '\\' : '/'
  const id = `_wf${Date.now()}${Math.random().toString(36).slice(2, 5)}`
  const outF = `${tmpDir}${sep}${id}_o`
  const errF = `${tmpDir}${sep}${id}_e`
  let redirectedCmd
  if (program === 'sh' && args[0] === '-c') {
    const shellCmd = args[1]
    redirectedCmd = isWin
      ? `(${shellCmd}) > "${outF}" 2> "${errF}"`
      : `sh -c ${shellEscape(shellCmd)} > "${outF}" 2> "${errF}"`
  } else {
    const shellCmd = [program, ...args.map(a => shellEscape(String(a)))].join(' ')
    redirectedCmd = `${shellCmd} > "${outF}" 2> "${errF}"`
  }
  const command = isWin
    ? `setlocal enabledelayedexpansion & ${redirectedCmd} & echo !errorlevel! & type "${outF}" & echo. & echo __WFSE__: & type "${errF}" & del /f /q "${outF}" "${errF}"`
    : `${redirectedCmd}; _ec=$?; echo $_ec; cat "${outF}"; printf '\\n__WFSE__:'; cat "${errF}"; rm -f "${outF}" "${errF}"`
  return { command, timeout, description: description || `exec: ${program}` }
}

// @utility:parseBashOutput
function parseBashOutput(raw) {
  let text = typeof raw === 'string' ? raw
    : (raw !== null && typeof raw === 'object' ? (raw.raw || raw.output || raw.stdout || JSON.stringify(raw)) : String(raw || ''))
  if (text.startsWith('Command:')) {
    const hEnd = text.indexOf('\n\n')
    if (hEnd >= 0) text = text.slice(hEnd + 2)
  }
  const nlIdx = text.indexOf('\n')
  const exitCode = parseInt(nlIdx >= 0 ? text.slice(0, nlIdx) : text) || 0
  const rest = nlIdx >= 0 ? text.slice(nlIdx + 1) : ''
  const seMarker = '\n__WFSE__:'
  const seIdx = rest.lastIndexOf(seMarker)
  const stdout = seIdx >= 0 ? rest.slice(0, seIdx) : rest
  const stderr = seIdx >= 0 ? rest.slice(seIdx + seMarker.length) : ''
  return { exitCode, stdout, stderr }
}

// @utility:parseCliOutput
function parseCliOutput(bashResult, command) {
  const { exitCode, stdout, stderr } = bashResult
  try {
    const parsed = JSON.parse(stdout)
    if (!parsed.success && !parsed.error) {
      parsed.error = (parsed.markdown || '').replace(/^❌\s*/, '') || '未知错误'
    }
    return parsed
  } catch (e) {
    emit(`<aside>⚠️ JSON 解析失败(${command}): ${String(e).slice(0, 100)}</aside>`)
  }
  if (exitCode !== 0) {
    return { success: false, error: stderr.slice(0, 300).trim(), command, data: {} }
  }
  return { success: true, markdown: stdout, data: {} }
}

// @utility:extract
function extract(source, mapping) {
  const result = {}
  for (const [key, config] of Object.entries(mapping)) {
    const raw = config.path.includes('.')
      ? config.path.split('.').reduce((o, k) => o?.[k], source)
      : source?.[config.path]
    if (config.type === 'number') {
      result[key] = typeof raw === 'number' ? raw : (config.default ?? 0)
    } else if (config.type === 'array') {
      result[key] = Array.isArray(raw) ? raw : (config.default ?? [])
    } else if (config.type === 'boolean') {
      result[key] = typeof raw === 'boolean' ? raw : (config.default ?? false)
    } else {
      result[key] = raw ?? config.default ?? ''
    }
  }
  return result
}

// @utility:buildArgs
function buildArgs(specs) {
  const result = []
  for (const spec of specs) {
    if (spec.when === undefined || spec.when) {
      result.push(...spec.args)
    }
  }
  return result
}

// @utility:camelizeParams
// 直连调用方可能用 snake_case 传 params（order_ids / task_id / multi_round），统一补一份 camelCase 别名，显式 camelCase 优先。
function camelizeParams(src) {
  const entries = Object.entries(src || {})
  const out = {}
  for (const [k, v] of entries) {
    const ck = k.replace(/_([a-z])/g, (m, c) => c.toUpperCase())
    if (ck !== k && out[ck] === undefined) out[ck] = v
  }
  for (const [k, v] of entries) out[k] = v
  // 归一到 agent schema 字段名，保证结构化入参与自然语言入参产出同构对象
  if (out.timeoutMinutes === undefined && out.timeout !== undefined) out.timeoutMinutes = out.timeout
  if (out.ext === undefined && out.extJson !== undefined) out.ext = out.extJson
  return out
}

// @utility:toList
function toList(v) {
  if (Array.isArray(v)) return v.map(x => String(x).trim()).filter(x => x)
  if (typeof v === 'string') return v.split(',').map(x => x.trim()).filter(x => x)
  return []
}

// @utility:toText
function toText(v) {
  if (v === null || v === undefined) return ''
  return String(v).trim()
}

// @utility:toObjectList
function toObjectList(v) {
  if (Array.isArray(v)) return v.filter(x => x && typeof x === 'object')
  if (typeof v === 'string' && v.trim().startsWith('[')) {
    try {
      const parsed = JSON.parse(v)
      return Array.isArray(parsed) ? parsed.filter(x => x && typeof x === 'object') : []
    } catch (e) {
      return []
    }
  }
  return []
}

// @utility:toPositiveInt
function toPositiveInt(v) {
  const n = typeof v === 'number' ? v : parseInt(String(v || ''), 10)
  return Number.isFinite(n) && n > 0 ? Math.floor(n) : 0
}

// @utility:toTriState
// order-single-round 三态：明确单轮 'true'，明确多轮 'false'，未提及 ''（不下发该参数）
function toTriState(v) {
  if (v === true || v === 'true') return 'true'
  if (v === false || v === 'false') return 'false'
  return ''
}

// @utility:inferSingleRoundFromText
// 确定性兜底：LLM 偶发把"多轮/单轮"控制词从 question 剥离却漏填 orderSingleRound（长输入下高发）。
// 仅在 LLM 返回 '' 时对原始 query 做关键词兜底；不覆盖模型已明确给出的 true/false。
// 注意：否定/单轮信号必须先于肯定/多轮信号判断，否则"不需要多轮"会被"多轮"误判为多轮。
function inferSingleRoundFromText(text) {
  if (!text) return ''
  const t = String(text)
  // 单轮信号（否定多轮 / 关闭自动回复 / 只要单轮）
  if (/(不需要|不要|无需|不用|关闭|关掉|取消)[^，。,;；\n]{0,6}(多轮|自动回复|AI\s*对话|ai\s*对话|人工介入)/i.test(t)) return 'true'
  if (/(只要|仅要|只需|仅需|要)?\s*单轮/.test(t)) return 'true'
  // 多轮信号（明确需要多轮 / 开启自动回复）
  if (/(需要|开启|打开|要|启用)[^，。,;；\n]{0,6}(多轮|自动回复|AI\s*对话|ai\s*对话)/i.test(t)) return 'false'
  return ''
}

// @utility:inferTimeoutMinutesFromText
// 确定性兜底：LLM 偶发把"超时时长"配置词从 question 剥离却漏填 timeoutMinutes（与 orderSingleRound 同款双步脱节）。
// 仅在 LLM 返回 0 时对原始 query 兜底；数字必须处于"超时"语境内，避免把"5分钟内发货"这类面向商家的诉求误判为超时配置。
function inferTimeoutMinutesFromText(text) {
  if (!text) return 0
  const t = String(text)
  const m = t.match(/超\s*时[^0-9]{0,8}(\d+(?:\.\d+)?)\s*(个?小时|h|H|分钟|分|min|m)/)
  if (!m) return 0
  const num = parseFloat(m[1])
  if (!Number.isFinite(num) || num <= 0) return 0
  const isHour = /小时|h|H/.test(m[2])
  const minutes = isHour ? Math.round(num * 60) : Math.round(num)
  return minutes > 0 ? minutes : 0
}

// @utility:toExtJson
function toExtJson(v) {
  if (!v) return ''
  if (typeof v === 'string') return v.trim().startsWith('{') ? v.trim() : ''
  if (typeof v === 'object') {
    const s = JSON.stringify(v)
    return s === '{}' ? '' : s
  }
  return ''
}

// @utility:formatErrorReply
function formatErrorReply(cliOut) {
  const msg = (cliOut && (cliOut.error || cliOut.markdown)) || '命令执行失败'
  return JSON.stringify({ success: false, message: String(msg).slice(0, 500) })
}

// @utility:formatSendReply
// 默认模式返回 wwTaskId；orders-detail 模式返回 wwTaskIds 列表（只要一个订单成功即 success=true）
function formatSendReply(cliOut) {
  const data = (cliOut && cliOut.data) || {}
  if (Array.isArray(data.results)) {
    const results = data.results
    const okCount = results.filter(r => r && r.suc).length
    return JSON.stringify({
      success: okCount > 0,
      wwTaskIds: results.map(r => (r && r.wwTaskId) || ''),
      message: okCount === results.length
        ? '询盘已成功发送'
        : `询盘部分成功：成功 ${okCount}，失败 ${results.length - okCount}`,
    })
  }
  return JSON.stringify({
    success: !!data.suc,
    wwTaskId: data.wwTaskId || '',
    message: data.suc ? '询盘已成功发送' : (data.errorMsg || '询盘触发失败'),
  })
}

// @utility:formatConfigReply
function formatConfigReply(cliOut) {
  const data = (cliOut && cliOut.data) || {}
  const single = data.orderSingleRound === true || data.orderSingleRound === 'true'
  return JSON.stringify({
    success: !!data.success,
    orderSingleRound: data.orderSingleRound,
    message: `对话配置已更新为${single ? '单轮对话' : '多轮对话'}`,
  })
}

// @utility:formatConfigureReply
function formatConfigureReply(cliOut) {
  const data = (cliOut && cliOut.data) || {}
  const configured = !!data.configured
  return JSON.stringify({
    success: configured,
    configured,
    message: configured ? 'AK 已配置' : 'AK 尚未配置或写入失败',
  })
}

// @utility:formatQueryReply
// 直接透出 CLI 的 data.result，不做任何包装
function formatQueryReply(cliOut) {
  const data = (cliOut && cliOut.data) || {}
  if (data.result && typeof data.result === 'object') return JSON.stringify(data.result)
  return JSON.stringify({ status: 'FAILED', summary: [], message: '询盘已发送，商家尚未回复' })
}

// ─── Constants ───────────────────────────────────────────────────

// @const
const CLI_SCRIPT = baseDir + '/cli.py'
const SUPPORTED_COMMANDS = ['inquiry_send', 'inquiry_query', 'inquiry_config', 'configure']
const PROGRESS_TEXT = {
  inquiry_send: '正在向商家发起询盘，请稍等...',
  inquiry_query: '正在查询商家回复，请稍等...',
  inquiry_config: '正在为您配置对话能力，请稍等...',
  configure: '正在处理 AK 配置，请稍等...',
}

// ═══ Main Flow ═══════════════════════════════════════════════════

// @node:read_input [transform] outputs:userQuery,inputParams
phase('意图解析')
const userQuery = (typeof args === 'string' && args.trim()) ? args.trim() : ''
const inputParams = camelizeParams((typeof params === 'object' && params !== null) ? params : {})

let rawIntent = null

// @node:input_mode_check [condition] expression:inputParams.command
if (inputParams.command) {
  // @branch:结构化入参 → read_structured_intent
  // @node:read_structured_intent [extract] source:inputParams outputs:rawIntent
  emit('<aside>📋 已收到结构化询盘参数，跳过意图解析</aside>')
  rawIntent = extract(inputParams, {
    command: { path: 'command', default: '' },
    orderIds: { path: 'orderIds', default: [] },
    question: { path: 'question', default: '' },
    ordersStatus: { path: 'ordersStatus', default: [] },
    orderSingleRound: { path: 'orderSingleRound', default: '' },
    timeoutMinutes: { path: 'timeoutMinutes', default: 0 },
    isPriceNegotiation: { path: 'isPriceNegotiation', type: 'boolean', default: false },
    imageUrls: { path: 'imageUrls', default: [] },
    localImages: { path: 'localImages', default: [] },
    ext: { path: 'ext', default: '' },
    ordersDetail: { path: 'ordersDetail', default: [] },
    taskId: { path: 'taskId', default: '' },
    multiRound: { path: 'multiRound', type: 'boolean', default: false },
    ak: { path: 'ak', default: '' },
    missing: { path: 'missing', default: '' },
  })
} else {
  // @branch:自然语言入参 → parse_intent
  // @node:parse_intent [agent] inputs:userQuery outputs:rawIntent
  emit('<aside>⚙️ 正在解析询盘意图...</aside>')
  rawIntent = await agent(await __prompt('./prompts/intent-parse.prompt.md', { userQuery }), {
    label: 'inquiry-intent-parse',
    model: 'qwen3.6-plus',
    schema: {
      type: 'object',
      properties: {
        command: { type: 'string', description: 'inquiry_send / inquiry_query / inquiry_config / configure，无法判定填空串' },
        orderIds: { type: 'array', items: { type: 'string' }, description: '订单/采购单号' },
        question: { type: 'string', description: '询盘问题，目标总价格式为 目标总价<金额>' },
        taskId: { type: 'string', description: 'inquiry_query 专用，询盘任务编号 wwTaskId' },
        multiRound: { type: 'boolean', description: 'inquiry_config 专用，明确要多轮对话才为 true' },
        ak: { type: 'string', description: 'configure 专用，用户给出的 AK' },
        imageUrls: { type: 'array', items: { type: 'string' }, description: '在线链接，图片与文件不区分' },
        localImages: { type: 'array', items: { type: 'string' }, description: '本地图片路径' },
        ordersStatus: { type: 'array', items: { type: 'string' }, description: '订单状态集合' },
        orderSingleRound: { type: 'string', description: "三态：'true' 单轮 / 'false' 多轮 / '' 未提及" },
        timeoutMinutes: { type: 'number', description: '询盘超时分钟数，未提及填 0' },
        isPriceNegotiation: { type: 'boolean', description: '用户意图是否为改价/议价（改价/议价/讲价/砍价/目标总价/调单价/改运费等 → true；催发货/问物流/问状态等 → false）。仅 inquiry_send 时填写，其他命令填 false' },
        ext: { type: 'string', description: '额外扩展字段 JSON 字符串，未提及填空串' },
        ordersDetail: {
          type: 'array',
          description: '按订单维度分配附件，需同时满足关键词+逐订单列举两个条件',
          items: {
            type: 'object',
            properties: {
              order_id: { type: 'string' },
              image_urls: { type: 'array', items: { type: 'string' } },
              file_urls: { type: 'array', items: { type: 'string' } },
            },
          },
        },
        missing: { type: 'string', description: '缺失的关键信息说明，齐全填空串' },
      },
      required: ['command'],
    },
  })
  emit('<aside>✅ 询盘意图解析完成</aside>')
}

// @node:normalize_intent [transform] inputs:rawIntent outputs:intent
const intent = {
  command: toText(rawIntent?.command),
  orderIds: toList(rawIntent?.orderIds),
  question: toText(rawIntent?.question),
  ordersStatus: toList(rawIntent?.ordersStatus),
  orderSingleRound: toTriState(rawIntent?.orderSingleRound) || inferSingleRoundFromText(userQuery),
  timeoutMinutes: toPositiveInt(rawIntent?.timeoutMinutes) || inferTimeoutMinutesFromText(userQuery),
  isPriceNegotiation: rawIntent?.isPriceNegotiation === true || rawIntent?.isPriceNegotiation === 'true',
  imageUrls: toList(rawIntent?.imageUrls),
  localImages: toList(rawIntent?.localImages),
  extJson: toExtJson(rawIntent?.ext),
  ordersDetail: toObjectList(rawIntent?.ordersDetail),
  taskId: toText(rawIntent?.taskId),
  multiRound: rawIntent?.multiRound === true || rawIntent?.multiRound === 'true',
  ak: toText(rawIntent?.ak),
  missing: toText(rawIntent?.missing),
}

// @node:validate_intent [transform] inputs:intent outputs:guardError
phase('参数校验')
let guardError = ''
if (!SUPPORTED_COMMANDS.includes(intent.command)) {
  guardError = intent.missing || '无法识别询盘意图，请说明要对哪个订单向商家提出什么问题'
} else if (intent.command === 'inquiry_send' && intent.orderIds.length === 0) {
  guardError = '缺少订单 ID，请提供需要询盘的订单/采购单号'
} else if (intent.command === 'inquiry_send' && !intent.question) {
  guardError = '缺少询盘问题，请说明询盘目的（如发货时间、物流单号、目标总价）'
} else if (intent.command === 'inquiry_query' && !intent.taskId) {
  guardError = '缺少询盘任务编号（wwTaskId），请提供发起询盘时返回的任务编号'
}

let replyJson = ''

// @node:intent_guard [condition] expression:guardError
if (guardError) {
  // @branch:参数缺失 → guard_reply
  // @node:guard_reply [transform] inputs:guardError outputs:replyJson
  emit(`<aside>❌ ${guardError}</aside>`)
  replyJson = JSON.stringify({ success: false, message: guardError })
} else {
  // @branch:参数完整 → route_command
  phase('询盘执行')
  let cliArgs = []

  // @node:route_command [condition] expression:intent.command
  if (intent.command === 'inquiry_config') {
    // @branch:对话配置 → build_config_args
    // @node:build_config_args [buildArgs] inputs:intent outputs:cliArgs
    cliArgs = buildArgs([
      { args: ['inquiry_config'] },
      { when: intent.multiRound, args: ['--multi-round'] },
    ])
  } else if (intent.command === 'configure') {
    // @branch:配置AK → build_configure_args
    // @node:build_configure_args [buildArgs] inputs:intent outputs:cliArgs
    cliArgs = buildArgs([
      { args: ['configure'] },
      { when: intent.ak !== '', args: [intent.ak] },
    ])
  } else if (intent.command === 'inquiry_query') {
    // @branch:结果查询 → build_query_args
    // @node:build_query_args [buildArgs] inputs:intent outputs:cliArgs
    cliArgs = buildArgs([
      { args: ['inquiry_query', '-t', intent.taskId] },
    ])
  } else {
    // @branch:订单询盘 → build_send_args
    // @node:build_send_args [buildArgs] inputs:intent outputs:cliArgs
    cliArgs = buildArgs([
      { args: ['inquiry_send', '-o', intent.orderIds.join(','), '-q', intent.question] },
      { when: intent.localImages.length > 0, args: ['--image', intent.localImages.join(',')] },
      { when: intent.imageUrls.length > 0, args: ['--image-url', intent.imageUrls.join(',')] },
      { when: intent.ordersStatus.length > 0, args: ['-s', JSON.stringify(intent.ordersStatus)] },
      { when: intent.orderSingleRound !== '', args: ['--order-single-round', intent.orderSingleRound] },
      { when: intent.extJson !== '', args: ['--ext', intent.extJson] },
      { when: intent.timeoutMinutes > 0, args: ['--timeout', String(intent.timeoutMinutes)] },
      { when: intent.isPriceNegotiation, args: ['--is-price-negotiation', 'true'] },
      { when: intent.ordersDetail.length > 0, args: ['--orders-detail', JSON.stringify(intent.ordersDetail)] },
    ])
  }

  // @node:execute_cli [tool] inputs:cliArgs outputs:cliRaw
  emit(`<aside>📋 ${PROGRESS_TEXT[intent.command] || '正在执行询盘命令，请稍等...'}</aside>`)
  const cliRaw = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, ...cliArgs], `执行 ${intent.command}`, 300000))

  // @node:parse_cli_result [transform] inputs:cliRaw outputs:cliOut,missingModule
  const bashOut = parseBashOutput(cliRaw)
  let cliOut = parseCliOutput(bashOut, intent.command)
  const missingModule = !cliOut.success && /ModuleNotFoundError/.test(String(bashOut.stderr || ''))

  // @node:dep_repair_check [condition] expression:missingModule
  if (missingModule) {
    // @branch:缺失依赖 → repair_and_retry
    // @node:repair_and_retry [tool] inputs:cliArgs outputs:cliOut
    emit('<aside>⚠️ 检测到缺失 Python 依赖，正在安装后重试...</aside>')
    const retryShell = `python3 -m pip install -r ${shellEscape(baseDir + '/requirements.txt')} && python3 ${shellEscape(CLI_SCRIPT)} ${cliArgs.map(a => shellEscape(String(a))).join(' ')}`
    const retryRaw = await callTool('Bash', buildBashCommand('sh', ['-c', retryShell], '安装依赖并重试', 300000))
    cliOut = parseCliOutput(parseBashOutput(retryRaw), intent.command)
  }

  // @node:format_reply [transform] inputs:cliOut,intent outputs:replyJson
  phase('结果输出')
  if (intent.command === 'configure') {
    replyJson = formatConfigureReply(cliOut)
  } else if (!cliOut.success) {
    replyJson = formatErrorReply(cliOut)
  } else if (intent.command === 'inquiry_query') {
    replyJson = formatQueryReply(cliOut)
  } else if (intent.command === 'inquiry_config') {
    replyJson = formatConfigReply(cliOut)
  } else {
    replyJson = formatSendReply(cliOut)
  }
  if (cliOut.success) {
    emit('<aside>✅ 询盘命令执行完成</aside>')
  } else {
    emit(`<aside>⚠️ 命令执行未成功：${String(cliOut.error || cliOut.markdown || '未知错误').slice(0, 120)}</aside>`)
  }
}

// @node:final_return [end] inputs:replyJson
return replyJson
