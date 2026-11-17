export const meta = {
  name: '1688-shop-health-check',
  description: '1688 店铺生意体检。基于流量、询盘、成交、商品、客户、广告、风险七大维度进行全面健康诊断（成交维度覆盖成交、订单履约与买家评价，风险维度专注合规扣分），输出总结性结论 + HTML 网页数据报告，支持多店铺批量体检；报告后可基于优先行动建议展示可多选交互卡片，继续执行对应优化动作，并可按条件引导用户设置每日定时体检任务。',
  whenToUse: '店铺体检、健康检查、店铺诊断、店铺分析、经营分析、全面诊断、店铺经营状况、体检报告',
  phases: [
    { title: '前置准备', detail: '获取绑定店铺列表' },
    { title: '意图确认', detail: '输出执行计划，命中免确认时直接开始诊断，否则等待用户确认维度' },
    { title: '全面诊断', detail: '七维度并行取数（逐店串行）' },
    { title: '分析结论', detail: '读取方法论 + 综合分析 + 输出总结性结论' },
    { title: '报告生成', detail: '写入诊断数据文件，引导主 Agent 先调用可视化技能生成 HTML 网页数据报告' },
    { title: '行动项生成', detail: '内部生成最多 3 条行动建议终稿，主 Agent 直接渲染卡片（末尾按条件追加定时体检任务选项）' },
  ],
}

// ─── Utilities ───────────────────────────────────────────

// @utility:shellEscape
function shellEscape(arg) {
  const s = String(arg)
  if (/^[a-zA-Z0-9._\-\/:,=@]+$/.test(s)) return s
  if (typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)) {
    return '"' + s.replace(/"/g, '""') + '"'
  }
  return "'" + s.replace(/'/g, "'\\''") + "'"
}

// @utility:runDirPath
// 本轮 dataCapture 的落盘目录（<tmp>/hc_run_<HC_RUN_ID>）。buildBashCommand 与 batch_fetch.py 必须
// 落进同一个目录：cleanupRunDir 靠「末段 hc_run_<纯数字> + 文件名 _wf*.json」两条护栏回收，
// 换目录或换命名都会直接导致临时文件泄漏。TDZ：HC_RUN_ID 在常量区，故调用点必须在其后。
function runDirPath() {
  const isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const tmpDir = isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const sep = isWin ? '\\' : '/'
  return `${tmpDir}${sep}hc_run_${HC_RUN_ID}`
}

// @utility:buildBashCommand
// opts.dataCapture（布尔，默认 false）：true 时启用「引用传递」——stdout 落到本轮运行目录并保留，
// 工具结果只回 wf_capture.py 产出的「摘要 + 文件路径」，全量业务数据不进会话通道
// （见《店铺体检渲染进程卡死修复方案》3.3；outF 由 cleanupRunDir 统一清理）。
// dataCapture !== true 时行为逐字不变：stdout 落临时文件 → cat 回灌 → 命令末尾 rm。
function buildBashCommand(program, args, description, timeout = 120000, opts = {}) {
  const isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const tmpDir = isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const sep = isWin ? '\\' : '/'
  const id = `_wf${Date.now()}${Math.random().toString(36).slice(2, 5)}`
  const capture = !!(opts && opts.dataCapture === true)
  // TDZ：HC_RUN_ID / CAPTURE_SCRIPT 定义在常量区，故所有 buildBashCommand 调用点必须在常量区之后
  const runDir = capture ? runDirPath() : ''
  const outF = capture ? `${runDir}${sep}${id}.json` : `${tmpDir}${sep}${id}_o`
  const errF = `${tmpDir}${sep}${id}_e`
  let redirectedCmd
  if (program === 'python3' && args[0] === '-c') {
    const script = args[1]
    const extraArgs = args.slice(2).map(a => shellEscape(String(a))).join(' ')
    const argsPart = extraArgs ? ` ${extraArgs}` : ''
    if (isWin) {
      redirectedCmd = `python3 -c ${shellEscape(script)}${argsPart} > "${outF}" 2> "${errF}"`
    } else {
      redirectedCmd = `{ python3 -${argsPart} << '_WF_PYEOF_'\n${script}\n_WF_PYEOF_\n} > "${outF}" 2> "${errF}"`
    }
  } else if (program === 'sh' && args[0] === '-c') {
    const shellCmd = args[1]
    if (isWin) {
      redirectedCmd = `(${shellCmd}) > "${outF}" 2> "${errF}"`
    } else {
      redirectedCmd = `sh -c ${shellEscape(shellCmd)} > "${outF}" 2> "${errF}"`
    }
  } else {
    const shellCmd = [program, ...args.map(a => shellEscape(String(a)))].join(' ')
    redirectedCmd = `${shellCmd} > "${outF}" 2> "${errF}"`
  }
  // 回灌方式：dataCapture → wf_capture.py 摘要（跨平台一致，不走 type）；默认 → 原样 cat/type。
  // 摘要脚本的 stderr 必须转写进 errF（`2>>`）：否则它的告警行会流入 stdout 区，掉进
  // parseCliOutput 的解析对象里导致 JSON 解析失败 —— 恰好是 3.1 第 0 条要防的静默降级。
  // 转写后告警随 errF 进入 __WFSE__ 后的 stderr 段，仍可查（且不影响判定：仅 exitCode 非 0 时才读 stderr）。
  const emitOut = capture
    ? `python3 "${CAPTURE_SCRIPT}" "${outF}" 2>> "${errF}"`
    : (isWin ? `type "${outF}"` : `cat "${outF}"`)
  // 清理：dataCapture 只删 errF（保留 outF 供合并脚本按路径读取），默认删两者
  const rmTmp = isWin
    ? (capture ? `del /f /q "${errF}"` : `del /f /q "${outF}" "${errF}"`)
    : (capture ? `rm -f "${errF}"` : `rm -f "${outF}" "${errF}"`)
  // 运行目录创建（幂等，内联在命令前）
  const mkRunDir = capture
    ? (isWin ? `if not exist "${runDir}" mkdir "${runDir}" & ` : `mkdir -p "${runDir}"; `)
    : ''
  let command
  if (isWin) {
    command = `${mkRunDir}setlocal enabledelayedexpansion & ${redirectedCmd} & echo !errorlevel! & ${emitOut} & echo. & echo __WFSE__: & type "${errF}" & ${rmTmp}`
  } else {
    command = `${mkRunDir}${redirectedCmd}; _ec=$?; echo $_ec; ${emitOut}; printf '\\n__WFSE__:'; cat "${errF}"; ${rmTmp}`
  }
  return { command, timeout, description: description || `exec: ${program}` }
}

// @utility:parseBashOutput
function parseBashOutput(raw) {
  let text = typeof raw === 'string' ? raw
    : (raw !== null && typeof raw === 'object' ? (raw.raw || JSON.stringify(raw)) : String(raw || ''))
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
    if (parsed.data && typeof parsed.data === 'object' && 'data' in parsed.data) {
      const innerData = parsed.data
      parsed.data = innerData['data']
    }
    if (!parsed.success && !parsed.error) {
      parsed.error = (parsed.markdown || '').replace(/^❌\s*/, '') || '未知错误'
    }
    return parsed
  } catch {}
  if (exitCode !== 0) {
    const errMsg = stderr.slice(0, 300).trim()
    return { success: false, error: errMsg, command, data: {} }
  }
  // 解析失败 + 退出码 0：若响应以 { 或 [ 开头，说明它本该是 JSON 却没解成——最可能是被
  // 平台截断（单条 tool_result 约 2~3 万字符硬砍）。这种情况绝不能当成功：旧语义会回
  // { success: true, markdown: 残缺JSON }，一次数据丢失被标成 success 并静默进入分析与报告。
  // 非 {/[ 开头的才是接口的纯文本响应（wf_capture.py 的 RAW_CAP 分支就为此而设），保持原样透传。
  const head = (stdout || '').trim().slice(0, 1)
  if (head === '{' || head === '[') {
    return { success: false, error: TRUNCATED_ERR, command, data: {} }
  }
  return { success: true, markdown: stdout, data: {} }
}

// @utility:buildBatchCommand
// 构造「按维度批量取数」命令：一次 callTool('Bash') 跑完一个维度的全部接口。
// 不走 dataCapture：全量数据的逐接口落盘由 batch_fetch.py 自己完成（每个叶子一个 _wf*.json +
// 自带 __hc_src）——若改用 dataCapture，wf_capture.py 会把整个信封当成单个叶子去摘要，
// merge_shop_data.py 就拿不到逐叶子的全量文件路径，报告会退化成读摘要（违反报告保真红线）。
// spec 以纯 JSON 作为命令行参数下发：与 freedom CLI 的 --params 同一条路径（已在双平台验证），
// 由 shellEscape 统一转义；7 个任务的 spec 约 1~2 KB，远低于 cmd.exe 的命令长度上限。
function buildBatchCommand(tasks, description, opts = {}) {
  const spec = JSON.stringify({
    tasks,
    budget: opts.budget || BATCH_BUDGET,
    task_timeout: opts.taskTimeout || BATCH_TASK_TIMEOUT,
    deadline: opts.deadline || BATCH_DEADLINE,
  })
  return buildBashCommand(
    'python3',
    [BATCH_SCRIPT, '--out-dir', runDirPath(), '--spec', spec],
    description,
    opts.timeout || BATCH_BASH_TIMEOUT,
  )
}

// @utility:parseBatchEnvelope
// 把批量取数的信封拆回「每个 key 一个叶子」，叶子形状与 parseCliOutput 的产出逐字一致。
// 信封不可解析（被截断 / 脚本崩 / 退出码非 0）时，本维度全部 key 如实标失败——不能回空对象，
// 否则下游 compactShopData 会把它当成「取到了但没数据」，变成又一条静默失败路径。
function parseBatchEnvelope(raw, keys, label) {
  const result = parseBashOutput(raw)
  let envelope = null
  try { envelope = JSON.parse(result.stdout) } catch { /* 下方统一走失败分支 */ }
  const results = envelope && typeof envelope.results === 'object' && envelope.results !== null
    ? envelope.results
    : null
  const leaves = {}
  if (!results) {
    const errMsg = (result.stderr || '').slice(0, 300).trim() || TRUNCATED_ERR
    for (const k of keys) leaves[k] = { success: false, error: errMsg, command: k, data: {} }
    log(`批量取数信封解析失败[${label}] exitCode=${result.exitCode} head=${String(result.stdout || '').slice(0, 160)}`)
    return { leaves, ok: false, meta: envelope ? envelope.__hc_batch : null }
  }
  for (const k of keys) {
    leaves[k] = results[k] || { success: false, error: '取数未返回结果', command: k, data: {} }
  }
  return { leaves, ok: true, meta: envelope.__hc_batch || null }
}

// @utility:detectMissingModule
// 从信封的 per-task stderr 与叶子错误里找缺失依赖（对齐 runScript 的单接口自动安装链路）。
function detectMissingModule(parsed) {
  const texts = []
  const _stderrMap = parsed && parsed.meta && parsed.meta.stderr
  if (_stderrMap && typeof _stderrMap === 'object') texts.push(...Object.values(_stderrMap).map(String))
  for (const leaf of Object.values(parsed && parsed.leaves ? parsed.leaves : {})) {
    if (leaf && typeof leaf.error === 'string') texts.push(leaf.error)
  }
  for (const t of texts) {
    const m = t.match(/ModuleNotFoundError:\s+No module named '([^']+)'/)
    if (m) return m[1].split('.')[0]
  }
  return ''
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

// @utility:parseRequirements
function parseRequirements(text) {
  return text
    .split('\n')
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('#'))
    .map(l => l.split(/[>=<!\[]/)[0].trim())
    .filter(l => l)
}

// @utility:formatReturnSummary
function formatReturnSummary(completedSteps, failedSteps, { filePresented = false, hasVizData = false } = {}) {
  const doneList = completedSteps.map(s => `- ✅ ${s.step}：${s.detail}`).join('\n')
  const failList = failedSteps.length > 0
    ? `\n失败：\n${failedSteps.map(s => `- ❌ ${s.step}：${s.detail}`).join('\n')}`
    : ''
  // 有可视化数据时，不添加「不要调用 skill」的限制语，因为下游需要触发可视化技能
  const guidance = hasVizData
    ? ''
    : filePresented
      ? '\n\n以上进度提示和文件卡片已通过 emit / present_files 输出给用户，你只需简洁回复确认完成即可，不要重复输出已展示的内容，不要再次调用本 skill 或手动执行脚本。'
      : '\n\n以上进度提示已通过 emit 输出给用户，不要重复输出已展示的内容，不要再次调用本 skill 或手动执行脚本。'
  return `\n执行步骤：\n${doneList}${failList}${guidance}`
}

// 维度 → 报告章节说明映射（强约束下游可视化技能按诊断维度出章节，问题1）
const _DIM_SECTION_MAP = {
  '流量': '流量分析（趋势图、渠道占比、搜索/推荐/广告下钻）',
  '询盘': '询盘分析（询盘量、有效询盘用户数、趋势、商品排行）',
  '成交': '成交分析（支付金额、买家数、转化率、客单价、退款、新老客结构；订单履约：四类待处理计数、超时订单明细；买家评价：1~5 分分布、差评明细）',
  '商品': '商品分析（异常商品列表、四大榜单 TOP 商品、商品状态）',
  '客户': '客户分析（地域分布图、头部老客户明细与流失风险）',
  '广告': '广告分析（广告渠道贡献、行业对比）',
  '风险': '风险分析（违规扣分、待处理违规明细、商品预警、司法预警，实时快照口径）',
}

// 构建可视化技能调用指引（附带完整参数说明，确保 LLM 能正确触发）
// 问题1：按选定维度动态生成必出章节清单，强约束下游按诊断维度出章节
// 问题2：注入 actionItems，供下游渲染「行动建议」章节
function buildVizGuide(dataFilePath, conclusionText, periodText, dimensions, actionItems, userQueryText) {
  if (!dataFilePath) return ''
  const _dims = Array.isArray(dimensions) && dimensions.length > 0 ? dimensions : ALL_DIMENSIONS
  const _dimSections = _dims.map(d => _DIM_SECTION_MAP[d]).filter(Boolean)
  const _chapters = [
    '报告标题与基本信息（分析周期、覆盖店铺、数据时间）',
    '多店铺总览对比（若存在多个店铺则必出：完整店铺名、核心指标、健康等级；单店可省略）',
    '执行摘要（将总结性结论中的核心发现以卡片/高亮形式呈现）',
    ..._dimSections,
    '行动建议（依据 interpretation.actionItems 分层呈现，标注责任店铺/商品/渠道）',
  ]
  const _chapterList = _chapters.map((c, i) => `${i + 1}. ${c}`).join('\n')
  const _interp = JSON.stringify({
    summary: conclusionText || '',
    period: periodText || '',
    dimensionText: _dims.join('、'),
    actionItems: Array.isArray(actionItems) ? actionItems : [],
  })
  return `\n\n## 📊 HTML 报告生成（待执行）\n店铺诊断数据已保存到文件：\n\`\`\`\n${dataFilePath}\n\`\`\`\n\n请调用 \`1688-common-report-to-visualization\` 技能生成可视化报告，传入以下参数（args 为 JSON 对象）：\n\`\`\`json\n{\n  "dataFilePath": "${dataFilePath}",\n  "interpretation": ${_interp},\n  "reportTitle": "店铺健康检查报告",\n  "userQuery": "${(userQueryText || '').replace(/"/g, '\\"')}"\n}\n\`\`\`\n\n**报告必须严格按以下章节顺序生成（缺数据的章节标注"数据暂不可用"，不得省略，也不得新增本次诊断维度以外的章节）：**\n${_chapterList}\n\n> 注意：数据文件路径为 \`${dataFilePath}\`，请直接读取该文件（该文件可达 MB 级，**不要把文件全文拼进技能入参或输出到会话**）；interpretation 已提供，其中 actionItems 用于渲染"行动建议"章节；章节须与上方清单完全一致，且仅覆盖本次诊断维度。\n> 📅 口径标注：各章节须标注该章节数据的实际口径；若与本次分析周期不一致（如询盘趋势接口返回近 30 天全量、风险维度为实时快照），必须在章节标题或首行显式注明，不得统一按主周期表述。\n> 🤫 静默要求：直接按上述步骤执行工具与技能调用，**不要向用户输出计划性叙述**（如「我先读取数据文件」「Let me generate the visualization plan」之类），对用户只呈现生成进度与最终报告。`
}

// 构建「行动项渲卡」指引：行动项已在 workflow 内部定稿（≤3 条，build-actions 产出终稿），
// 主 Agent 只负责渲卡与执行。静默根治：不再要求主 Agent 列技能/建映射表/筛选——
// 没有需要跨轮备忘的中间产物，从结构上消除内部逻辑外泄；仅剩定时任务去重一个判断。
function buildActionSelectionGuide(actionCandidates) {
  const _cands = Array.isArray(actionCandidates) ? actionCandidates.filter(Boolean) : []
  const _scheduleOption = '⏰ 需要我自动帮你的店铺全面体检嘛？点击设置定时任务'
  const _scheduleTaskName = '店铺健康检查'
  // 文案须逐字包含全部七个标准维度名（与 ALL_DIMENSIONS 一致）：定时任务的 query 即本 description，
  // 需命中意图识别免确认规则与代码层白名单兜底，缺一个维度名都会导致定时体检漏诊断该维度。
  const _scheduleTaskDesc = '自动进行 1688 店铺全面体检，覆盖流量、询盘、成交、商品、客户、广告、风险七大维度，生成体检报告并给出异常提醒和经营建议'
  // 定时任务选项（must-check）：先 Schedule list + name/description 双键 OR 命中判断，再决定是否追加；与 react 模式 interaction-specs 对齐
  const _scheduleBlock = `\n\n### ⏰ 定时任务选项（must-check，先查后决定）\n除行动项外，在 \`select_action_items\` 卡片选项**末尾按条件追加一条定时任务选项**，文案固定为：\`${_scheduleOption}\`\n- **必须先查（must-check）**：定时任务状态检查须在结论与报告输出之后进行，不得前置阻塞。构造卡片前**必须先调用 \`Schedule\`（action=list）拉取全部任务**，按下方去重规则判断，**不得跳过检查直接追加**。\n- **去重匹配（name / description 双键 OR 命中）**：对 list 返回的每条任务，\`name\` 精确等于 \`${_scheduleTaskName}\` **或** \`description\` 精确等于 \`${_scheduleTaskDesc}\`（规范化后精确比对，禁止 includes 粗匹配），任一命中即视为「已存在体检定时任务」。\n- **展示 / 动作决策**：未命中 → 追加，确认后新建（create）；命中且 enabled:true → 不追加（见措辞护栏）；命中但 enabled:false → 追加，确认后走 update 重新启用（禁止 create）；list 调用报错 → fail-open 追加，确认后新建。该选项不参与优先级排序、不计入 3 条行动项上限。\n- **命中且已开启、决定不追加时（必须静默）**：该选项**不追加**，且**绝对不要输出任何与定时任务相关的文案**——尤其禁止「已为您设置/已为您开启『${_scheduleTaskName}』定时任务…」这类确认语（此时用户既没有该选项、也没有勾选，任何定时任务提示都是凭空出现的误导）；同样禁止泄露内部判断过程或技术字段（id / enabled / schedule / cron 等）。\n- **用户勾选并确认后**：未命中时以完整定时任务规格新建、命中但已停用时改为 update 重新启用；新建由客户端弹出「设置定时任务」确认卡片（含执行时间、执行内容、修改任务/立即执行按钮），待用户点击「立即执行」后再创建，不可直接建任务。规格与日报一致——任务名「${_scheduleTaskName}」；执行时间「每天 09:30」；执行内容「${_scheduleTaskDesc}」。设置成功后，用一句话向用户确认已开启（如「已为您开启『${_scheduleTaskName}』每日定时任务，每天 09:30 自动生成体检报告」）。**仅当用户确实勾选了该选项并成功新建/重新启用后才输出这句确认；用户未勾选、或该选项本就未追加时，禁止输出任何定时任务文案。**`
  // 静默约束（瘦身版）：主 Agent 在本环节只剩定时任务去重一个内部判断，其它一律直接动作
  const _silenceBlock = `\n\n### 🤫 静默约束（必读，最高优先级）\n本环节你唯一需要做的内部判断是「是否追加定时任务选项」：调用 Schedule（action=list）后立即按结果渲卡，中间不得输出任何正文。对用户只呈现：最终的 select_action_items 交互卡片，以及用户选择后真实执行的结果与确认语。\n- 禁止向用户叙述计划与判断过程，尤其禁止出现「让我先检查定时任务」「根据 Schedule 列表我看到…」「既然定时任务已启用，我不应该追加这个选项」「Let me render the action items card」之类的话。\n- 禁止泄露任何内部字段与判据（id、enabled、schedule、cron、技能名、触发语等）。\n- 用户勾选后的执行环节同理：直接调用对应技能，不要输出「让我看看哪个技能能处理」「行动项映射：xxx → 某技能」之类的匹配过程，对用户只呈现执行进度与结果。`
  if (_cands.length === 0) {
    // fail-open：即使没有行动项，也要触发卡片并仅展示定时任务选项
    return `\n\n## 🎯 行动项卡片渲染（待执行，须在 HTML 报告生成之后）${_silenceBlock}\n本次体检未发现需要优化的问题。请使用 \`select_action_items\` 交互卡片，**仅展示下方定时任务选项**，等待用户选择，不要因无行动项而跳过卡片。${_scheduleBlock}\n\n> 顺序约束：本卡片必须在上方「HTML 报告生成」完成之后再展示；且本卡片整轮体检只展示一次，用户处理或跳过后流程即结束，不得再次渲染。`
  }
  const _list = _cands.map((a, i) => `${i + 1}. ${a}`).join('\n')
  return `\n\n## 🎯 行动项卡片渲染（⛔ 体检尚未结束，以下为必须继续执行的步骤，不得停在这里）${_silenceBlock}\n以下行动建议已在体检流程内部完成挑选与排序，是**终稿**（已按紧急程度排序，最多 3 条）：\n${_list}\n\n请严格按以下步骤执行：\n\n**第 1 步（查定时任务，must-check）**：调用 \`Schedule\`（action=list），按下方规则判断是否追加定时任务选项；判断完成后**立即**进入第 2 步，中间不输出任何正文。\n**第 2 步（渲卡）**：用 \`select_action_items\` 交互卡片渲染多选卡——上述行动项**逐条原样作为选项**（不得增删、改写、重排），再在末尾按条件追加定时任务选项（见下方），等待用户选择。\n**第 3 步（选后必须真实执行）**：用户勾选确认后，对勾选的**每一项**在当前会话可用技能中现场寻找能承接的技能，**立即读取该技能的 SKILL.md 并按其定义真实执行**——这是必须完成的动作，**严禁只回一句“好的/已为你规划”而不实际触发技能**；一条行动项涉多个技能时按依赖顺序依次执行；**若某项确实没有技能可承接，直接给出具体的人工操作建议并明确告知用户**，不要静默忽略；若勾选定时任务选项，则按下方规格设置。\n**第 4 步（收尾，本卡片只弹一次）**：完成第 3 步后（或用户点「跳过」、未勾选任何项），本轮体检即结束——**你触发的下游技能返回后，不要把“控制权回到本流程”理解为要重新弹卡，绝不可再次渲染 select_action_items 卡片**；用户若还想继续优化，由其主动发起新请求。${_scheduleBlock}\n\n> 顺序约束：本卡片必须在上方「HTML 报告生成」完成之后再展示，确保用户先看到完整报告、再选择行动项。`
}

// @utility:parseAgentResult
// agent() 返回值抖救解析（移植自 0.52.0 已验证实现，适配现行字段）：
// 处理模型间歇性返回字符串（markdown 代码块 / 闲聊包裹 / broken JSON / 纯 Markdown 文档）而非结构化对象的情况。
// 级联：1 对象直通 → 2 ```json 围栏提取 → 3 裸 {...} 解析 → 3.5 broken JSON 正则抠字段 → 4 纯 Markdown 文本回收（可选）
function parseAgentResult(raw, { textAsConclusion = false } = {}) {
  if (raw && typeof raw === 'object' && !Array.isArray(raw)) return raw
  if (typeof raw === 'string') {
    // 第一优先：从 ```json ``` 代码块中提取
    const m = raw.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/)
    if (m) { try { return JSON.parse(m[1].trim()) } catch {} }
    // 第二优先：找最外层 { ... } 尝试 JSON.parse
    const start = raw.indexOf('{')
    const end = raw.lastIndexOf('}')
    if (start >= 0 && end > start) {
      const jsonCandidate = raw.substring(start, end + 1)
      try { return JSON.parse(jsonCandidate) } catch {}
      // 2.5：JSON.parse 失败（常因值中含未转义引号），用正则从 broken JSON 中抠字段
      const extracted = _extractFieldsFromBrokenJson(jsonCandidate)
      if (extracted) return extracted
    }
    // 第三优先（兜底）：模型无视 schema 直接输出 Markdown 文档 → 整段文本回收为 conclusion
    if (textAsConclusion) return _extractConclusionFromMarkdown(raw)
  }
  return null
}

// 从格式有误的 JSON 文本中用正则提取结构化字段（移植自 0.52.0）
// 典型场景：字符串值包含未转义引号（如 评级为"极低"）导致 JSON.parse 失败
function _extractFieldsFromBrokenJson(text) {
  if (!text || text.length < 20) return null
  const result = {}
  // 字符串字段：匹配 "field":"..." 直到下一个字段边界或结尾
  const stringFields = ['conclusion', 'healthLevel']
  for (const field of stringFields) {
    const pattern = new RegExp('"' + field + '"\\s*:\\s*"([\\s\\S]*?)"\\s*(?:,\\s*"[a-zA-Z]|\\}\\s*$)')
    const fm = text.match(pattern)
    if (fm) result[field] = fm[1].replace(/\\n/g, '\n').replace(/\\"/g, '"')
  }
  // 数组字段
  const arrayFields = ['keyFindings', 'actionItems', 'actionOptions']
  for (const field of arrayFields) {
    const arrPattern = new RegExp('"' + field + '"\\s*:\\s*\\[([\\s\\S]*?)\\]')
    const am = text.match(arrPattern)
    if (am) {
      const arrContent = am[1].trim()
      if (!arrContent) { result[field] = []; continue }
      try {
        result[field] = JSON.parse('[' + arrContent + ']')
      } catch {
        // 降级：提取所有引号包裹的字符串
        const items = [...arrContent.matchAll(/"((?:[^"\\]|\\.)*)"/g)].map(x => x[1])
        if (items.length > 0) result[field] = items
      }
    }
  }
  // conclusion / actionOptions 任一抠到即有效（分别对应分析类与行动项类调用）
  if (typeof result.conclusion === 'string' && result.conclusion.trim()) return result
  if (Array.isArray(result.actionOptions)) return result
  return Object.keys(result).length >= 2 ? result : null
}

// 模型直接输出纯 Markdown 分析文档时的回收（0.52.0 思路适配现行字段）：
// conclusion 需要的本就是 Markdown 全文 → 整段零损耗回收；healthLevel/keyFindings 正则辅助提取；
// actionItems 留空，由 build-actions 兜底链从结论全文回填，下游天然闭环。
function _extractConclusionFromMarkdown(text) {
  const _t = typeof text === 'string' ? text.trim() : ''
  if (_t.length < 80) return null // 太短不像一份分析，交给上层重试/兜底
  const levelPatterns = [
    /健康等级[*\s]*[：:]+\s*(.+?)(?:[\n\r—|]|$)/,
    /(健康|基本稳定|存在风险|明显承压)/,
  ]
  let healthLevel = ''
  for (const p of levelPatterns) {
    const lm = _t.match(p)
    if (lm) { healthLevel = lm[1].replace(/\*\*/g, '').trim(); break }
  }
  const keyFindings = []
  const bulletLines = _t.match(/[-•*]\s+.+/g) || []
  for (const line of bulletLines) {
    const clean = line.replace(/^[-•*]\s+/, '').replace(/\*\*/g, '').trim()
    if (clean.length >= 8 && !keyFindings.includes(clean)) keyFindings.push(clean)
    if (keyFindings.length >= 4) break
  }
  return { conclusion: _t, healthLevel, keyFindings, actionItems: [] }
}

// healthLevel 白名单归一：精确 → 包含匹配 → 空串（怪值既不透传、也不否决整单）
// 包含匹配把「健康」排最后，避免「亚健康/基本稳定」这类表述被误归为健康
const _HEALTH_LEVELS = ['基本稳定', '存在风险', '明显承压', '健康']
function normalizeHealthLevel(raw) {
  const _v = typeof raw === 'string' ? raw.trim() : ''
  if (!_v) return ''
  if (_HEALTH_LEVELS.includes(_v)) return _v
  for (const lv of _HEALTH_LEVELS) { if (_v.includes(lv)) return lv }
  // 关键字兜底：处理「存在一定风险」「较为稳定」这类插字/变体表述（顺序：先重后轻，健康最后）
  if (_v.includes('承压')) return '明显承压'
  if (_v.includes('风险')) return '存在风险'
  if (_v.includes('稳定')) return '基本稳定'
  if (_v.includes('健康') && !_v.includes('不') && !_v.includes('亚')) return '健康'
  return ''
}

// @utility:extractAllAnswersFromInteraction
// 按官方文档铺开解析面（保险）：形态 1 data 数组（GenericCard 实际回传，置首）→
// 形态 2 data.answers / answers 数组 → 形态 3 selection / choice 字符串 → 都取不到返回 [] 交 plan_check 如实终止。
function extractAllAnswersFromInteraction(result) {
  if (!result) return []
  const answers = []
  const _push = (v) => {
    if (typeof v === 'string') { if (v.trim()) answers.push(v.trim()) }
    else if (v != null && typeof v !== 'object') answers.push(String(v))
  }
  const _collectItem = (item) => {
    if (item == null) return
    if (typeof item !== 'object') { _push(item); return }
    // 优先读取 selected 字段（多选，GenericCard 实际回传格式）
    if (Array.isArray(item.selected)) {
      for (const s of item.selected) _push(s)
    }
    // 回退到 answer 字段（单选或测试桩）
    else if ('answer' in item) {
      const a = item.answer
      if (Array.isArray(a)) { for (const s of a) _push(s) }
      else _push(a)
    }
  }
  const data = result.data
  // 形态 1：data 为数组（现有主形态）
  if (Array.isArray(data)) {
    for (const item of data) _collectItem(item)
    if (answers.length > 0) return answers
  }
  // 形态 2：data.answers / answers 为数组
  const _answersArr = (data && typeof data === 'object' && !Array.isArray(data) && Array.isArray(data.answers))
    ? data.answers
    : (Array.isArray(result.answers) ? result.answers : null)
  if (_answersArr) {
    for (const item of _answersArr) _collectItem(item)
    if (answers.length > 0) return answers
  }
  // 形态 3：selection / choice 字符串
  _push(result.selection)
  if (answers.length === 0) _push(result.choice)
  if (answers.length === 0 && data && typeof data === 'object' && !Array.isArray(data)) {
    _push(data.selection)
    if (answers.length === 0) _push(data.choice)
  }
  return answers
}

// @utility:compactShopData
// 压缩单店铺数据：解包 data.data.data 嵌套 + 去除 metadata 字段 + 截断长文本
// 将原始 API 响应压缩为 LLM 可处理的精简结构（通常 3-5x 压缩比）
const _COMPACT_META_KEYS = new Set([
  'code', 'message', 'messageEn', 'requestId', 'apiVersion',
  'success', 'domain', 'localizedMsg', 'class',
  'token', 'accessToken', 'refreshToken',
  'page', 'pageSize', 'totalCount', 'totalPage', 'total',
  'gmtCreate', 'gmtModified', 'creator', 'modifier',
  'extensions', 'extend',
])

function _compactValue(val, depth) {
  if (depth > 6) return '...'
  if (val === null || val === undefined) return val
  if (typeof val === 'string') {
    // SYCM 接口可能返回 JSON 格式字符串，先尝试二次解析为结构化对象
    if (val.length > 2 && (val.startsWith('{') || val.startsWith('['))) {
      try {
        const parsed = JSON.parse(val)
        if (typeof parsed === 'object' && parsed !== null) {
          return _compactValue(parsed, depth + 1)
        }
      } catch { /* 非合法 JSON，按普通字符串处理 */ }
    }
    return val.length > 2000 ? val.slice(0, 2000) + '...' : val
  }
  if (typeof val === 'number' || typeof val === 'boolean') return val
  if (Array.isArray(val)) return val.slice(0, 50).map(v => _compactValue(v, depth + 1))
  if (typeof val === 'object') {
    // 解包 data.data.data 三层嵌套
    let inner = val
    for (let i = 0; i < 3 && inner && typeof inner === 'object' && 'data' in inner && Object.keys(inner).length <= 3; i++) {
      inner = inner.data
    }
    if (inner !== val && typeof inner === 'object' && inner !== null) val = inner
    const result = {}
    for (const [k, v] of Object.entries(val)) {
      if (_COMPACT_META_KEYS.has(k)) continue
      result[k] = _compactValue(v, depth + 1)
    }
    return result
  }
  return val
}

function compactShopData(shopData) {
  if (!shopData) return null
  const compacted = {
    shopName: shopData.shopName,
    loginId: shopData.loginId,
    period: shopData.period,
    dimensions: {},
  }
  for (const [dimName, dimData] of Object.entries(shopData.dimensions || {})) {
    compacted.dimensions[dimName] = {}
    for (const [key, value] of Object.entries(dimData)) {
      // 每个 value 是 parseCliOutput 的结果：{ success, data, error, markdown }
      if (value && typeof value === 'object' && 'success' in value) {
        const _compactedData = value.success !== false ? _compactValue(value.data, 0) : undefined
        const _isDataEmpty = !_compactedData
          || (typeof _compactedData === 'object' && !Array.isArray(_compactedData) && Object.keys(_compactedData).length === 0)
        const _entry = {
          success: value.success,
          data: _compactedData,
          error: value.error,
        }
        // 当 data 为空但 markdown 存在时（API返回非JSON纯文本），保留 markdown 作为 fallback
        if (_isDataEmpty && value.markdown) {
          _entry.markdown = value.markdown.length > 2000 ? value.markdown.slice(0, 2000) + '...' : value.markdown
        }
        compacted.dimensions[dimName][key] = _entry
      } else {
        compacted.dimensions[dimName][key] = _compactValue(value, 0)
      }
    }
  }
  return compacted
}

// @utility:normalizeForViz
// 为「写给可视化技能的数据文件」做无损规整（区别于 compactShopData 的有损压缩）。
// compactShopData 会砍深度(>6)、丢 meta 键(total/page 等)、解包 data 壳时连带丢兄弟键，
// 这些对分析 LLM 无碍，但对 viz 会丢掉真实业务数字 → 故此处单写一个绝对无损的函数。
// 只做两件零丢失的事：
//   1. value 若是可解析的 JSON 文本 → 解析成对象/数组（只换表示，正是"value 是 JSON 串"的解药）；
//   2. 仅当 `data` 是对象的唯一键时才解包 { data: X }（无兄弟键可丢 → 无损）。
// 绝不做：丢 meta 键、丢兄弟键、砍深度、截断数组/字符串。
// 对 wikiContext（纯文本背景，非 JSON 串）原样透传，不受影响。
function _normalizeValue(val) {
  if (val === null || val === undefined) return val
  if (typeof val === 'string') {
    // value 是 JSON 文本时解析成结构化，否则原样保留（含 wikiContext 等纯文本）
    const _t = val.trim()
    if (_t.length > 1 && (_t[0] === '{' || _t[0] === '[')) {
      try {
        const parsed = JSON.parse(_t)
        if (parsed !== null && typeof parsed === 'object') return _normalizeValue(parsed)
      } catch { /* 非合法 JSON，按普通字符串原样保留 */ }
    }
    return val
  }
  if (typeof val !== 'object') return val
  if (Array.isArray(val)) return val.map(_normalizeValue)
  // 仅当 data 是唯一键时解包（无兄弟键可丢 → 无损）；有兄弟键则原样保留全部键
  let cur = val
  while (cur && typeof cur === 'object' && !Array.isArray(cur)
         && Object.keys(cur).length === 1 && 'data' in cur) {
    cur = cur.data
  }
  if (cur !== val) return _normalizeValue(cur)
  const result = {}
  for (const [k, v] of Object.entries(val)) result[k] = _normalizeValue(v)
  return result
}

// ⚠️ 本函数自「渲染进程卡死修复」后**不再参与运行时**：可视化数据文件已改为由
// scripts/merge_shop_data.py 在磁盘侧按 manifest 合并生成（Python 版 `_normalize_value`）。
// 此处保留仅作 Python 等价实现的比对基准，逐条对照见《店铺体检渲染进程卡死修复方案》第四章；
// 若改动本函数语义，必须同步改 merge_shop_data.py，否则两侧实现漂移。
function normalizeForViz(shopData) {
  return _normalizeValue(shopData)
}

// @utility:buildDataManifest
// 构建「引用传递」manifest：allShopData 的骨架副本，凡带 __hc_src 的取数叶子整体替换为
// { __hc_load: <落盘文件绝对路径> }（不保留 data/success/error/markdown 任何字段——合并脚本
// 需从原始文件重建整个叶子以保证键序与改造前逐字节一致，见修复方案 3.2「键序等价」）。
// 无 __hc_src 的叶子（非 JSON 响应、exitCode != 0 的失败项）与所有非叶子键原样保留。
function _toManifestValue(val) {
  if (val === null || val === undefined) return val
  if (Array.isArray(val)) return val.map(_toManifestValue)
  if (typeof val !== 'object') return val
  const _src = val.__hc_src
  if (_src && typeof _src === 'object' && typeof _src.file === 'string' && _src.file) {
    return { __hc_load: _src.file }
  }
  const result = {}
  for (const [k, v] of Object.entries(val)) result[k] = _toManifestValue(v)
  return result
}

function buildDataManifest(allShops) {
  return { shops: (Array.isArray(allShops) ? allShops : []).map(_toManifestValue) }
}

// ─── Shared Functions (含原语，子图继承) ──────────────────

// @shared:wikiEventEmitter
// Wiki 查阅子任务专用事件回调，仅对"真正的知识库读取"出声。
// 通过 toolDesc/summary 命中 WikiNav/WikiRead/知识库筛选成功事件，避免把子
// Agent 顺手调用的其它内置工具（使用技能/调用扩展能力/Bash 等）误计为 wiki 读取。
// state = { readCount, started } 由发起方传入并共享，collectShopWiki 据此决定
// 展示文案与是否返回空。修改输出样式只需改此处，无需核心包发版。
function wikiEventEmitter(label, state) {
  const who = label ? `「${label}」` : ''
  return (event) => {
    switch (event.type) {
      case 'tool_result_end': {
        // 只统计 WikiNav/WikiRead 的成功读取，用于 collectShopWiki 判定是否返回背景；
        // 进度提示已合并为「体检的判定标准有哪些呢」，此处不再单独出声。
        const desc = `${event.toolDesc || ''}${event.summary || ''}`
        if (/WikiNav|WikiRead|知识库/i.test(desc) && event.state !== 'error') {
          state.readCount++
        }
        break
      }
    }
  }
}

// @shared:collectShopWiki
// 收集指定店铺的 Wiki 经营上下文（含 subTask 原语调用）。
// 逐店独立 subTask：每店独占 Wiki 探索，避免跨店上下文混用。
// 发起方负责传入精确的 loginId/companyName，subTask 内部用 WikiNav/WikiRead 读取。
// 未真正读到任何知识库页面（含 agent 无 WikiNav/WikiRead 工具时）→ 返回空，
// 丢弃子 Agent 可能产生的空谈/幻觉，不污染下游。失败同样返回空。
async function collectShopWiki(shop, dimensions = []) {
  if (!shop || (!shop.loginId && !shop.companyName)) return ''
  const { loginId, companyName } = shop
  const queryText = '店铺'
  const dimensionText = Array.isArray(dimensions) && dimensions.length > 0
    ? dimensions.join('、')
    : '流量、询盘、成交、商品、客户、广告、风险'
  try {
    const wikiRules = await readRef('wiki-routing-rules.md', '对照分析指引，定下一步怎么查')
    const wikiState = { readCount: 0, started: false }
    const result = await subTask({
      task: __prompt(baseDir + '/workflow/prompts/collect-shop-wiki.prompt.md', {
        shopName: companyName || loginId,
        loginId: loginId || '',
        dimensionText,
        queryText,
        wikiRules,
      }),
      label: companyName || loginId,
      tools: ['WikiNav', 'WikiRead'],
      maxRounds: 3,
      onEvent: wikiEventEmitter(companyName || loginId, wikiState),
    })
    const wikiContext = typeof result === 'string' ? result.trim() : ''
    // 有效补充 = 确实读到过 wiki 页（readCount>0）且产出了非空摘要；二者缺一
    //（无工具/没命中/只输出空/纯幻觉无实读）一律返回空，丢弃幻觉，不污染下游。
    // 进度提示已合并为「体检的判定标准有哪些呢」，此处静默，不单独 emit（与其它维度空结果一致）。
    if (wikiContext && wikiState.readCount > 0) {
      return wikiContext
    }
    return ''
  } catch (e) {
    return ''
  }
}

// @shared:runScript
async function runScript(scriptName, args, { description = '' } = {}) {
  const bashArgs = [CLI_SCRIPT, scriptName, ...(args || [])]
  // @node:run_script_call [tool] inputs:scriptName,args outputs:bashResult
  // dataCapture：全部 cli.py 取数结果只回摘要 + 文件路径，全量数据留在磁盘
  const _raw = await callTool('Bash', buildBashCommand('python3', bashArgs, description || `执行 ${scriptName}`, 120000, { dataCapture: true }))
  const result = parseBashOutput(_raw)
  if (result.exitCode !== 0) {
    const errMsg = result.stderr.slice(0, 500).trim()
    const modMatch = errMsg.match(/ModuleNotFoundError:\s+No module named '([^']+)'/)
    if (modMatch) {
      const modName = modMatch[1].split('.')[0]
      emit(`<aside>📦 检测到缺失依赖 ${modName}，正在自动安装...</aside>`)
      const installCmd = `python3 -m pip install ${shellEscape(modName)} 2>&1`
      const _installRaw = await callTool('Bash', buildBashCommand('sh', ['-c', installCmd], `安装 ${modName}`, 180000))
      const installResult = parseBashOutput(_installRaw)
      if (installResult.exitCode === 0) {
        emit(`<aside>✅ ${modName} 安装完成，重新执行脚本...</aside>`)
        // 重试与主取数同语义，同样启用 dataCapture
        const _retryRaw = await callTool('Bash', buildBashCommand('python3', bashArgs, description || `重试 ${scriptName}`, 120000, { dataCapture: true }))
        const retryResult = parseBashOutput(_retryRaw)
        return parseCliOutput(retryResult, scriptName)
      }
    }
    return { success: false, error: errMsg, command: scriptName, data: {} }
  }
  return parseCliOutput(result, scriptName)
}

// @shared:runBatch
// 按维度批量取数：一次 Bash 调用跑完一个维度的全部接口，返回 { key: 叶子 }。
// tasks 的 argv 一律由调用方构造（参数拼装保持在 workflow 侧收口，诸如 rag_query 不得带
// --NEWTON_SHOP_LOGIN_ID 这类特例不得下沉到 Python）；本函数只负责执行、补依赖、拆信封。
async function runBatch(tasks, description) {
  const keys = (tasks || []).map(t => t.key)
  // @node:run_batch_call [tool] inputs:tasks outputs:leaves
  const _raw = await callTool('Bash', buildBatchCommand(tasks, description))
  let parsed = parseBatchEnvelope(_raw, keys, description)
  // 缺失依赖：装一次再整批重跑。取数全是只读 GET，重跑幂等；与 runScript 的单接口链路同语义。
  const modName = detectMissingModule(parsed)
  if (modName) {
    emit(`<aside>📦 检测到缺失依赖 ${modName}，正在自动安装...</aside>`)
    const installCmd = `python3 -m pip install ${shellEscape(modName)} 2>&1`
    const _installRaw = await callTool('Bash', buildBashCommand('sh', ['-c', installCmd], `安装 ${modName}`, 180000))
    if (parseBashOutput(_installRaw).exitCode === 0) {
      emit(`<aside>✅ ${modName} 安装完成，重新取数...</aside>`)
      const _retryRaw = await callTool('Bash', buildBatchCommand(tasks, description))
      parsed = parseBatchEnvelope(_retryRaw, keys, description)
    }
  }
  if (parsed.meta && Array.isArray(parsed.meta.degraded) && parsed.meta.degraded.length > 0) {
    // 降级只影响分析看到的摘要精度，报告仍读磁盘全量，故不向用户出声，只进日志便于排障
    log(`批量取数信封降级[${description}] chars=${parsed.meta.chars} degraded=${parsed.meta.degraded.join(',')}`)
  }
  return parsed.leaves
}

// @shared:readRef
// desc：卡片上展示的动作文案（只影响 UI，不影响读取行为）；不传则回落为「读取 <文件名>」。
async function readRef(filename, desc) {
  // @node:read_ref_call [tool] inputs:filename,desc outputs:refContent
  const _isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const _raw = await callTool('Bash', buildBashCommand(_isWin ? 'type' : 'cat', [baseDir + '/references/' + filename], desc || `读取 ${filename}`))
  const result = parseBashOutput(_raw)
  return result.exitCode === 0 ? result.stdout : ''
}

// @shared:collectCaptureDirs
// 递归收集 __hc_src.file 的父目录（去重）。子图（每店一次 __subgraph）会各自重新求值
// HC_RUN_ID，因此一轮体检存在多个 runDir（主图 1 个 + 每店 1 个）；仅靠主图 runId 派生路径
// 清不到子图目录，必须按实际落盘路径回收。见《店铺体检渲染进程卡死修复方案》3.7。
function collectCaptureDirs(node, sep, out) {
  if (!node || typeof node !== 'object') return out
  if (Array.isArray(node)) {
    for (const v of node) collectCaptureDirs(v, sep, out)
    return out
  }
  const _f = node.__hc_src && node.__hc_src.file
  if (typeof _f === 'string' && _f) {
    const _i = _f.lastIndexOf(sep)
    if (_i > 0) out.add(_f.slice(0, _i))
  }
  for (const v of Object.values(node)) collectCaptureDirs(v, sep, out)
  return out
}

// @shared:cleanupRunDir
// 清理本轮 dataCapture 的落盘目录（见修复方案 3.7）。目录来源两路：
//   A 主图自身 <tmpDir>/hc_run_<HC_RUN_ID>（装周期探测结果，其路径不进 allShopData，只能由 runId 派生）
//   B 从 allShopData 收集的全部 __hc_src.file 父目录（覆盖每个子图各自建的目录）
// 四条护栏逐目录校验：非空 / 在 tmpDir 下 / 末段以 hc_run_ 开头 / 末段完全匹配 hc_run_<纯数字>。
// 删除粒度只到「目录内 _wf*.json 普通文件」，收尾用非递归 rmdir——目录里有陌生文件则原样保留；
// 全程无 rm -rf、无跨目录通配，故不会碰到并发轮次或其它 skill 的临时文件。
// <tmp>/hc_shopdata_<ts>.json 不在任何 runDir 内，不受影响（主 Agent 在 workflow 返回后才读它）。
async function cleanupRunDir(allShops) {
  const _isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const _tmpDir = _isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const _sep = _isWin ? '\\' : '/'
  // 路 A 作为种子，路 B 递归补全；Set 天然去重
  const _dirs = collectCaptureDirs(allShops, _sep, new Set([`${_tmpDir}${_sep}hc_run_${HC_RUN_ID}`]))
  const _safe = []
  for (const _d of _dirs) {
    const _lastSeg = (typeof _d === 'string' ? _d : '').split(_sep).pop() || ''
    if (_d && _d.startsWith(_tmpDir + _sep) && _lastSeg.startsWith('hc_run_') && /^hc_run_\d+$/.test(_lastSeg)) {
      _safe.push(_d)
    } else {
      log('跳过临时数据目录清理（护栏未通过）：' + _d)
    }
  }
  if (_safe.length === 0) return
  try {
    // 多目录串成一条命令，仍只一次工具调用；-maxdepth 1 不递归、-type f 不碰目录与链接。
    // 末尾 `|| :` 让整条命令恒以 0 退出：目录非空（含陌生文件）或已不存在时 rmdir 本就会失败，
    // 那是预期行为而非故障，不应让收尾命令报非 0 退出码。
    const _cmd = _safe.map(d => (_isWin
      ? `del /f /q "${d}${_sep}_wf*.json" 2>nul & rmdir "${d}" 2>nul`
      : `find "${d}" -maxdepth 1 -type f -name "_wf*.json" -delete 2>/dev/null; rmdir "${d}" 2>/dev/null || :`
    )).join(_isWin ? ' & ' : '; ')
    await callTool('Bash', buildBashCommand('sh', ['-c', _cmd], '正在收拾工作台', 30000))
  } catch (e) {
    log('清理临时数据目录失败（不影响体检结果）：' + (e instanceof Error ? e.message : String(e)))
  }
}

// ─── Constants ───────────────────────────────────────────
// @const
// Wiki 功能开关：读取失败或当前任务无法调用 WikiNav/WikiRead 时自动回落为空，不影响体检主流程。
const WIKI_ENABLED = true
const CLI_SCRIPT = baseDir + '/cli.py'
// dataCapture 辅助脚本（绝对路径，禁止相对路径）：摘要回灌 + 磁盘侧合并
const CAPTURE_SCRIPT = baseDir + '/scripts/wf_capture.py'
const MERGE_SCRIPT = baseDir + '/scripts/merge_shop_data.py'
// 按维度批量取数脚本：把一个维度的多个接口合成一条 Bash 命令（卡片 25 → ≤ 7）
const BATCH_SCRIPT = baseDir + '/scripts/batch_fetch.py'
// 信封字符预算：平台对单条 tool_result 的截断阈值约 2~3 万字符（按字符硬砍），此处取下界。
// 合并后一条信封被砍 = 整个维度报废，所以宁可在 batch_fetch.py 内主动降级，也不能赌平台不砍。
// 平台给出准确阈值后只需改这一处（它是我们自己的常量，不是平台限制）。
const BATCH_BUDGET = 20000
// 三级超时预算，必须严格递增：单接口 < 全批 deadline < Bash timeout。
// 否则 Bash 先超时，信封根本没机会输出 → 整个维度丢失，而不是只丢慢的那一个接口。
const BATCH_TASK_TIMEOUT = 100
const BATCH_DEADLINE = 150
const BATCH_BASH_TIMEOUT = 180000
// 响应本该是 JSON 却解析失败（最可能是被平台截断）时的统一文案；共用以保证归因口径一致
const TRUNCATED_ERR = '响应不是合法 JSON（疑似被截断），本项数据暂不可用'
// 本轮体检运行标识：dataCapture 落盘目录 <tmp>/hc_run_<HC_RUN_ID>，返回前统一清理
const HC_RUN_ID = Date.now()
const FREEDOM_BASE_DIR = baseDir + '/../1688-shop-freedom-query-data'
const FREEDOM_CLI = FREEDOM_BASE_DIR + '/cli.py'
const COMPRESS_SCRIPT = FREEDOM_BASE_DIR + '/scripts/compress_data.py'
const ALL_DIMENSIONS = ['流量', '询盘', '成交', '商品', '客户', '广告', '风险']

// ═══ Main Flow ═══════════════════════════════════════════

// @node:parse_input [transform] source:args outputs:userQuery
// args 可能是纯文本，也可能是 {"query": "..."} JSON 字符串（主 Agent 透传）——
// 先按 JSON 解析、含 query 字段则取其值，否则按纯文本，为意图识别提供干净的用户原话。
let userQuery = (typeof args === 'string' && args.trim()) ? args.trim() : ''
if (userQuery.startsWith('{')) {
  try {
    const _parsedArgs = JSON.parse(userQuery)
    if (_parsedArgs && typeof _parsedArgs === 'object' && typeof _parsedArgs.query === 'string' && _parsedArgs.query.trim()) {
      userQuery = _parsedArgs.query.trim()
    }
  } catch { /* 非合法 JSON，按纯文本处理 */ }
} else if (args && typeof args === 'object' && typeof args.query === 'string' && args.query.trim()) {
  userQuery = args.query.trim()
}

// ═══ Step 0: 前置准备 ═══
phase('前置准备')

// @node:get_bindlist [tool]
const _bindlistRaw = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, 'get_bindlist'], '先来清点你绑了几家店'))
const _bindlistParsed = parseCliOutput(parseBashOutput(_bindlistRaw), 'get_bindlist')
let shopList = []
if (_bindlistParsed.success !== false) {
  const _raw = _bindlistParsed?.data?.data || _bindlistParsed?.data || []
  shopList = Array.isArray(_raw) ? _raw : []
}
if (shopList.length === 0) {
  shopList = [{ loginId: '', companyName: '当前店铺' }]
  emit('<aside>⚠️ 未获取到绑定店铺列表，降级为当前 AK 单店模式</aside>')
} else {
  emit(`<aside>✅ 点名完毕：${shopList.length}家店，一个不落</aside>`)
}

// ═══ Step 1: 意图澄清与执行计划确认 ═══
phase('意图确认')

// @node:parse_intent [agent] inputs:userQuery outputs:intent
emit('<aside>📋 正在打印体检项目单</aside>')
const intent = parseAgentResult(await agent(
  __prompt('./prompts/parse-intent.prompt.md', { userQuery: userQuery || '（用户未提供具体需求，使用默认计划）' }),
  {
    label: 'parse-intent',
    schema: {
      type: 'object',
      properties: {
        dimensions: { type: 'array', items: { type: 'string' } },
        dimensionText: { type: 'string' },
        outputFormat: { type: 'string' },
        period: { type: 'string' },
        shopScope: { type: 'string' },
        shopName: { type: 'string' },
        dimensionsExplicit: { type: 'boolean' },
      },
      required: ['dimensions'],
    },
  }
)) || { dimensions: ALL_DIMENSIONS, dimensionText: '流量、询盘、成交、商品、客户、广告、风险', outputFormat: 'conclusion+html', period: 'RECENT_7', shopScope: 'all', shopName: '', dimensionsExplicit: false }

// @node:filter_shops [transform] inputs:intent,shopList outputs:shopList desc:按用户指定店铺名定向过滤（2.5）
if (intent.shopScope === 'single' && intent.shopName) {
  const _kw = String(intent.shopName).trim()
  const _matched = shopList.filter(s => {
    const _name = s.companyName || s.loginId || ''
    return (_name && _name.includes(_kw)) || (s.loginId && s.loginId.includes(_kw))
  })
  if (_matched.length > 0) {
    shopList = _matched
    emit(`<aside>🎯 已按指定店铺「${_kw}」定向诊断，命中 ${_matched.length} 家</aside>`)
  } else {
    const _allNames = shopList.map(s => s.companyName || s.loginId || '').filter(Boolean).join('、')
    emit(`<aside>⚠️ 未匹配到店铺「${_kw}」，将对全部绑定店铺进行诊断。当前绑定：${_allNames}</aside>`)
  }
}

// @node:check_skip_confirm [transform] inputs:userQuery,intent outputs:skipConfirm,presetDimensions desc:意图识别免确认短路（核心修复，已获平台侧认可）
// 用户已把维度说出口（含定时任务文案自带信号）→ 跳过弹卡直接取数，故障点不出现。
const _validLlmDims = Array.isArray(intent.dimensions) ? intent.dimensions.filter(d => ALL_DIMENSIONS.includes(d)) : []
let skipConfirm = false
let presetDimensions = []
// 第一层：LLM 意图识别标记「已明确指定维度 / 要求全面诊断 / 要求直接开始」且已解析出有效维度
if (intent.dimensionsExplicit === true && _validLlmDims.length > 0) {
  skipConfirm = true
  presetDimensions = _validLlmDims
}
// 第二层：代码层确定性白名单兜底（防 LLM 抖动）——不依赖 LLM，是定时任务等无人值守场景的最终保底。
// 覆盖 parse-intent 免确认规则列举的全部信号词，使本层对信号词场景真正冗余层 1（层 1 另覆盖同义改写）：
// 全量信号（全面体检/全面诊断/全面深度诊断/全部维度）→ 七维度；多个标准维度名 → 对应维度；
// 直启信号（不用选/直接启动/直接开始/立即开始）→ 有点名维度则按点名，否则七维度。
if (!skipConfirm && userQuery) {
  const _hitDims = ALL_DIMENSIONS.filter(d => userQuery.includes(d))
  // 「全面深度诊断」等中间插词写法不能被「全面诊断」字面命中，故单独列举
  if (/全面体检|全面诊断|全面深度诊断|全部维度/.test(userQuery)) {
    skipConfirm = true
    presetDimensions = ALL_DIMENSIONS
  } else if (_hitDims.length >= 2) {
    skipConfirm = true
    presetDimensions = _hitDims
  } else if (/不用选|直接启动|直接开始|立即开始/.test(userQuery)) {
    skipConfirm = true
    presetDimensions = _hitDims.length > 0 ? _hitDims : ALL_DIMENSIONS
  }
}

// @node:build_plan_text [transform] inputs:intent outputs:planText
const _wantHtml = (intent.outputFormat || 'conclusion+html') !== 'conclusion'
const _outputFormDesc = _wantHtml
  ? '1. 一段结构化总结性结论（含健康等级、核心发现、优先行动）\n2. 一份 HTML 网页数据报告（承载详细数据、图表、各维度分析与行动建议）'
  : '1. 一段结构化总结性结论（含健康等级、核心发现、优先行动）'
const _shopScopeDesc = shopList.length === 1
  ? `${shopList[0].companyName || shopList[0].loginId || '当前店铺'}`
  : `当前绑定的全部店铺（共 ${shopList.length} 家）`
// 时间周期文案：只讲人话，不暴露 RECENT_7/RECENT_30 枚举；
// 近 7 天口径下个别接口仅提供近 30 天数据，用一句轻提示说明，具体口径由报告章节标注。
const _periodDesc = intent.period === 'RECENT_30'
  ? '近30天'
  : '近7天（个别数据只有近30天的，报告里会标注）'
const planText = `## 店铺健康检查执行计划\n\n**输出形式**：\n${_outputFormDesc}\n**时间周期**：${_periodDesc}\n**覆盖店铺**：${_shopScopeDesc}${skipConfirm ? `\n**诊断维度**：${presetDimensions.join('、')}（已按您的要求确认，无需选择）` : '\n\n请在下方卡片中选择要诊断的维度。'}`

// @node:emit_plan [emit] inputs:planText
emit(planText)

let selectedDimensions
if (skipConfirm) {
  // @branch:免确认 → 跳过弹卡，直接进入取数
  selectedDimensions = presetDimensions
} else {
  // @node:confirm_plan [interaction] name:confirm_execution_plan outputs:planResult
  emit('<aside>🔄 请选择要诊断的维度...</aside>')
  const planResult = await showInteraction({
    name: 'confirm_execution_plan',
    type: 'card',
    selectionType: 'requirement',
    questions: [
      {
        question: '请选择要诊断的维度（可多选），或选择"全面诊断（七维度）"执行全部：',
        options: [...ALL_DIMENSIONS, '全面诊断（七维度）'],
        allowMultiple: true,
        required: true,
      },
    ],
  })
  // 记录交互卡原始返回，便于定位平台实际回传形态（无人作答/取消/异常时尤其关键）
  log('confirm_execution_plan 原始返回：' + JSON.stringify(planResult))

  // @node:plan_check [condition] expression:selectedDimensions
  // 终止语义如实化（保持终止，遵循平台「没人点卡就不往下执行」语义）：
  // 平台取消回包形态无法确认，不猜测取消信号——取消/空/无人作答/格式不识别/异常统一以
  // 「未收到有效的维度选择」口径如实终止，绝不表述为「用户取消」，切断误导文案引发的重试放大链。
  const _planAnswers = extractAllAnswersFromInteraction(planResult)
  const _selectedAll = _planAnswers.some(a => a.includes('全面诊断'))
  selectedDimensions = _selectedAll ? ALL_DIMENSIONS : _planAnswers.filter(a => ALL_DIMENSIONS.includes(a))

  if (selectedDimensions.length === 0) {
    // @branch:未收到有效选择 → end_no_selection
    // @node:end_no_selection [end]
    // 返回语去失败化：不走 formatReturnSummary 的「失败：❌」框架——那会让主 Agent 把正常终止
    // 当成可重试故障，重新发起体检/重新弹卡，用户被迫再次取消（重试放大链的另一触发形态）。
    emit('<aside>⚠️ 未收到有效的维度选择，本次体检未执行</aside>')
    return '维度选择卡未收到有效选择（用户取消或未作答），本次体检已按平台语义正常结束——这是预期行为，不是失败或系统故障，无需任何补救。\n- 禁止重试：不要再次调用本 workflow 或本 skill，不要降级为手工模式重新体检，不要再向用户展示任何维度选择/确认卡片。\n- 终止提示已通过 emit 展示给用户，你只需用一句话收尾（如「本次体检未执行，需要时随时可以重新发起」），不要重复已展示内容、不要道歉、不要解释技术细节；用户若稍后主动重新发起体检，再按新请求正常处理。'
  }
}
// @branch:确认 → shop_loop
intent.dimensions = selectedDimensions
intent.dimensionText = selectedDimensions.join('、')
emit(`<aside>✅ 已确认执行计划，开始诊断（${intent.dimensionText}）</aside>`)

// ═══ Step 2: 全面诊断取数 ═══
phase('全面诊断')
const allShopData = []
let period = intent.period || 'RECENT_7'

// @node:period_probe [tool] inputs:shopList,period outputs:period desc:RECENT_7 无数据自动降级 RECENT_30，父图统一多店口径（2.4）
if (period === 'RECENT_7') {
  const _probeShop = shopList[0] || {}
  const _probeArgs = _probeShop.loginId ? ['--NEWTON_SHOP_LOGIN_ID', _probeShop.loginId] : []
  const _hasData = (r) => r?.success !== false && r?.data && (Array.isArray(r.data) ? r.data.length > 0 : Object.keys(r.data).length > 0)
  const _probe7Raw = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, 'alibaba.1688.seller.trade.code.index', '--date_type', 'RECENT_7', ..._probeArgs], '周期探测（近 7 天）', 120000, { dataCapture: true }))
  const _probe7 = parseCliOutput(parseBashOutput(_probe7Raw), 'alibaba.1688.seller.trade.code.index')
  if (!_hasData(_probe7)) {
    const _probe30Raw = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, 'alibaba.1688.seller.trade.code.index', '--date_type', 'RECENT_30', ..._probeArgs], '周期探测（近 30 天）', 120000, { dataCapture: true }))
    const _probe30 = parseCliOutput(parseBashOutput(_probe30Raw), 'alibaba.1688.seller.trade.code.index')
    if (_hasData(_probe30)) {
      period = 'RECENT_30'
      emit('<aside>ℹ️ 近 7 天无成交数据，已自动降级为近 30 天口径（全店统一）</aside>')
    }
  }
}

// @node:shop_loop [loop] inputs:shopList,period outputs:allShopData
for (let i = 0; i < shopList.length; i++) {
  const shop = shopList[i]
  const progressLabel = shopList.length > 1 ? `（${i + 1}/${shopList.length}）` : ''
  const shopName = shop.companyName || shop.loginId || '当前店铺'
  emit(`<aside>📋 正在诊断店铺：${shopName} ${progressLabel}...</aside>`)

  // @node:diagnose_shop [subgraph] ref:./sub/diagnose-shop.js inputs:shop,period,intent.dimensions outputs:shopData
  let shopData
  try {
    shopData = await __subgraph('./sub/diagnose-shop.js', { shop, period, dimensions: intent.dimensions })
  } catch (e) {
    const _errMsg = e instanceof Error ? e.message : String(e)
    emit(`<aside>❌ 店铺 ${shopName} 诊断失败：${_errMsg}</aside>`)
    shopData = { shopName, loginId: shop.loginId || '', period, dimensions: {}, error: _errMsg }
  }

  // @node:wiki_context [agent] inputs:shop,intent.dimensions outputs:shopWikiContext
  // 用户已确认执行计划后，再按实际诊断店铺补充 Wiki 背景；失败为空，不影响分析。
  let shopWikiContext = ''
  if (WIKI_ENABLED) {
    shopWikiContext = await collectShopWiki(shop, intent.dimensions)
  }
  shopData.wikiContext = shopWikiContext

  allShopData.push(shopData)
}

// ═══ Step 3: 分析与结论输出 ═══
phase('分析结论')

// @node:read_methodology [tool] inputs:FREEDOM_BASE_DIR,intent.dimensions outputs:methodologyContent desc:确定性动态扫描——ls目录+按维度匹配cat（无LLM、无subTask，避免上下文膨胀超时）
emit('<aside>体检的判定标准有哪些呢…</aside>')
let methodologyContent = await readRef('analysis-methodology.md', '先翻分析方法总纲，定好体检怎么做')

const _mIsWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
const _freedomRefDir = FREEDOM_BASE_DIR + '/references'
// 维度 → 方法论文件名关键词（确定性映射）
const _METHODOLOGY_KEYWORD = { '广告': 'ad', '客户': 'customer', '商品': 'product' }
// 方法论文件名 → 卡片上展示的中文动作文案（只影响 UI，不影响读取行为）；未收录的文件回落为带文件名的通用文案
const _METHODOLOGY_LABEL = {
  'shop-diagnosis-rules.md': '店铺诊断',
  'data-parsing-rules.md': '数据核对',
  'product-operation-rules.md': '商品运营',
  'customer-analysis-rules.md': '客户分析',
  'ad-analysis-rules.md': '广告分析',
}
// 通用方法论：无论选什么维度都读取
const _alwaysFiles = ['shop-diagnosis-rules.md', 'data-parsing-rules.md']

// 1. 扫描 freedom references 目录，拿到真实文件名列表
let _refFiles = []
try {
  const _lsRaw = await callTool('Bash', buildBashCommand(_mIsWin ? 'dir' : 'ls', [_mIsWin ? _freedomRefDir : (_freedomRefDir + '/')], '看看选哪些标准比较好'))
  const _lsResult = parseBashOutput(_lsRaw)
  if (_lsResult.exitCode === 0) {
    _refFiles = _lsResult.stdout.split(/\s+/).map(s => s.trim()).filter(s => s.endsWith('.md'))
  }
} catch (e) { /* 扫描失败则仅用通用文件兜底 */ }

// 2. 按选定维度动态匹配 + 通用文件，去重
const _picked = new Set(_alwaysFiles)
for (const _dim of (intent.dimensions || [])) {
  const _kw = _METHODOLOGY_KEYWORD[_dim]
  if (!_kw) continue
  for (const _f of _refFiles) { if (_f.includes(_kw)) _picked.add(_f) }
}

// 3. 逐个 cat 命中的方法论文件并合并（缺失文件自动跳过）
let _mLoaded = 0
for (const _f of _picked) {
  const _raw = await callTool('Bash', buildBashCommand(_mIsWin ? 'type' : 'cat', [_freedomRefDir + '/' + _f], _METHODOLOGY_LABEL[_f] || `判定标准 ${_f}`))
  const _res = parseBashOutput(_raw)
  if (_res.exitCode === 0 && _res.stdout.trim()) {
    methodologyContent += '\n\n' + _res.stdout.trim()
    _mLoaded++
  }
}
// @node:analyze_per_shop [agent] inputs:allShopData,methodologyContent,intent outputs:perShopConclusions
// 分店渐进式分析：逐店调用 LLM 分析，避免一次性注入全部数据导致上下文撑爆
const perShopConclusions = []
let allActionItems = []

for (let i = 0; i < allShopData.length; i++) {
  const shop = allShopData[i]
  const shopName = shop.shopName || '当前店铺'
  emit(`<aside>⚙️ 正在综合分析「${shopName}」的数据...</aside>`)

  // 压缩单店数据：解包嵌套 + 去 metadata + 截断长文本，降低 LLM 上下文压力
  const _compactData = compactShopData(shop)
  const _analyzePrompt = __prompt('./prompts/analyze-shop.prompt.md', {
    methodologyContent,
    dimensionText: intent.dimensionText,
    period: period,
    wikiContextJson: shop.wikiContext ? JSON.stringify({ shopName, context: shop.wikiContext }) : '无 Wiki 背景信息',
    shopDataJson: JSON.stringify(_compactData),
    shopName,
  })
  // healthLevel 不再用 enum 硬校验（枚举外取值会否决整单），合法性由 normalizeHealthLevel 归一兜底
  const _analyzeSchema = {
    type: 'object',
    properties: {
      conclusion: { type: 'string', description: '该店铺的 Markdown 分析结论' },
      healthLevel: { type: 'string', description: '健康 / 基本稳定 / 存在风险 / 明显承压 四选一' },
      keyFindings: { type: 'array', items: { type: 'string' } },
      actionItems: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            action: { type: 'string' },
            priority: { type: 'string' },
            dimension: { type: 'string' },
          },
        },
      },
    },
    required: ['conclusion'],
  }
  // 模型偶发返回字符串/Markdown 文档/broken JSON 而非结构化对象：先抖救解析，失败原样重试一次，仍失败才落兜底
  let _shopResult = null
  for (let _attempt = 0; _attempt < 2 && !_shopResult; _attempt++) {
    if (_attempt > 0) emit(`<aside>⚠️ 「${shopName}」分析结果格式异常，正在重试...</aside>`)
    let _rawShopResult = null
    try {
      _rawShopResult = await agent(_analyzePrompt, { label: `analyze-${shopName}`, schema: _analyzeSchema })
    } catch (e) { _rawShopResult = null }
    const _salvaged = parseAgentResult(_rawShopResult, { textAsConclusion: true })
    if (_salvaged && typeof _salvaged.conclusion === 'string' && _salvaged.conclusion.trim()) {
      _shopResult = _salvaged
    }
  }

  // 兜底语义：明确是“分析服务波动”而非数据缺失，防止下游综合环节误读为采集/授权问题
  const _analysisFailed = !_shopResult
  if (_analysisFailed) {
    emit(`<aside>⚠️ 「${shopName}」本次分析未能生成结论（店铺数据已正常获取），将在总结中如实说明</aside>`)
  }
  const _shopConclusion = _shopResult?.conclusion
    || `### ${shopName}\n\n该店铺分析服务出现波动，本次未能生成分析结论（店铺数据已正常获取，非数据缺失），可稍后重新体检。`
  const _shopActions = Array.isArray(_shopResult?.actionItems)
    ? _shopResult.actionItems.map(a => (a && typeof a === 'object' ? { ...a, shopName } : { action: String(a), priority: '', dimension: '', shopName }))
    : []

  perShopConclusions.push({
    shopName,
    conclusion: _shopConclusion,
    healthLevel: normalizeHealthLevel(_shopResult?.healthLevel),
    keyFindings: Array.isArray(_shopResult?.keyFindings) ? _shopResult?.keyFindings : [],
    actionItems: _shopActions,
    analysisFailed: _analysisFailed,
  })
  allActionItems.push(..._shopActions)
}

// @node:synthesize_conclusion [agent] inputs:perShopConclusions outputs:conclusion
// 跨店综合：仅用各店结构化结论（非原始数据）做跨店对比，上下文极小
let conclusion
let actionItems

if (allShopData.length > 1) {
  emit('<aside>📊 正在进行跨店对比分析...</aside>')
  // analysisFailed 透传给综合 LLM，配合 prompt 护栏：失败店铺如实说明，不得推断为数据缺失
  const _synthPrompt = __prompt('./prompts/analyze-conclude.prompt.md', {
    dimensionText: intent.dimensionText,
    perShopConclusionsJson: JSON.stringify(perShopConclusions.map(s => ({
      shopName: s.shopName,
      healthLevel: s.healthLevel,
      keyFindings: s.keyFindings,
      conclusion: s.conclusion,
      analysisFailed: !!s.analysisFailed,
    }))),
  })
  const _synthSchema = {
    type: 'object',
    properties: {
      conclusion: { type: 'string', description: '完整的 Markdown 总结性结论' },
      actionItems: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            action: { type: 'string' },
            priority: { type: 'string' },
            shopName: { type: 'string' },
            dimension: { type: 'string' },
          },
        },
      },
    },
    required: ['conclusion'],
  }
  // 与分店分析同样的抖救 + 重试链
  let _synthesisResult = null
  for (let _attempt = 0; _attempt < 2 && !_synthesisResult; _attempt++) {
    if (_attempt > 0) emit('<aside>⚠️ 跨店综合结论格式异常，正在重试...</aside>')
    let _rawSynth = null
    try {
      _rawSynth = await agent(_synthPrompt, { label: 'cross-shop-synthesis', schema: _synthSchema })
    } catch (e) { _rawSynth = null }
    const _salvaged = parseAgentResult(_rawSynth, { textAsConclusion: true })
    if (_salvaged && typeof _salvaged.conclusion === 'string' && _salvaged.conclusion.trim()) {
      _synthesisResult = _salvaged
    }
  }
  // 综合失败兜底：直接拼接各店结论，不丢内容
  conclusion = _synthesisResult?.conclusion || perShopConclusions.map(s => s.conclusion).join('\n\n')
  // 空数组不覆盖各店行动项（Markdown 抖救路径 actionItems 为空时保住 per-shop 产出）
  actionItems = (Array.isArray(_synthesisResult?.actionItems) && _synthesisResult.actionItems.length > 0)
    ? _synthesisResult.actionItems
    : allActionItems
} else {
  // 单店场景：直接使用该店分析结论（分析失败时 perShopConclusions 已携带故障语义兜底文案）
  conclusion = perShopConclusions[0]?.conclusion || '本次分析服务出现波动，未能生成结论（店铺数据已正常获取），可稍后重新体检。'
  actionItems = allActionItems
}

// @node:emit_conclusion [emit] inputs:conclusion
emit(conclusion)
emit('<aside>✅ 总结性结论已输出</aside>')

// ═══ Step 4: 数据文件写入（best-effort，供下游可视化技能使用） ═══
phase('报告生成')
let _dataFilePath = ''
if (_wantHtml) {
  const _isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const _tmpDir = _isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const _sep = _isWin ? '\\' : '/'
  const _ts = Date.now()
  _dataFilePath = `${_tmpDir}${_sep}hc_shopdata_${_ts}.json`
  // 引用传递：只把 manifest（路径 + 标量，数 KB）送进会话通道，全量数据由 merge_shop_data.py
  // 按路径从磁盘读取并套用 normalizeForViz 等价规则，产出结构与改造前完全一致的数据文件。
  const _manifest = buildDataManifest(allShopData)
  try {
    const _writeRaw = await callTool('Bash', {
      command: `python3 "${MERGE_SCRIPT}" --output ${shellEscape(_dataFilePath)}`,
      stdinJson: _manifest,
      description: '合并店铺数据文件',
    })
    const _writeCheck = typeof _writeRaw === 'string' ? _writeRaw : (_writeRaw?.output || _writeRaw?.stdout || JSON.stringify(_writeRaw))
    if (!_writeCheck || !_writeCheck.includes('OK')) {
      throw new Error(`写入异常: ${String(_writeCheck).slice(0, 200)}`)
    }
  } catch (e) {
    emit(`<aside>⚠️ 数据文件写入失败: ${e instanceof Error ? e.message : String(e)}</aside>`)
    _dataFilePath = ''
  }
}

// ═══ Step 5: 行动项终稿生成（内部定稿 ≤3 条，主 Agent 直接渲卡） ═══
phase('行动项生成')

// @node:build_actions [agent] inputs:actionItems outputs:actionOptions
// 内部定稿：build-actions 直接产出最多 3 条终稿（含软性可承接偏好），主 Agent 不再二次筛选
const _actionsPrompt = __prompt('./prompts/build-actions.prompt.md', {
  actionItemsJson: JSON.stringify(actionItems),
  conclusionText: conclusion || '',
})
let _actionsResult = null
try {
  const _rawActions = await agent(_actionsPrompt, {
    label: 'build-actions',
    schema: {
      type: 'object',
      properties: {
        actionOptions: { type: 'array', items: { type: 'string' } },
      },
      required: ['actionOptions'],
    },
  })
  _actionsResult = parseAgentResult(_rawActions)
  // Markdown 兜底：结构化抢不回来时，从文本抓编号/圆点行当选项
  if ((!_actionsResult || !Array.isArray(_actionsResult.actionOptions)) && typeof _rawActions === 'string') {
    const _lines = (_rawActions.match(/^\s*(?:\d+[.、)]|[-•*])\s+.+$/gm) || [])
      .map(l => l.replace(/^\s*(?:\d+[.、)]|[-•*])\s+/, '').replace(/\*\*/g, '').trim())
      .filter(Boolean)
    if (_lines.length > 0) _actionsResult = { actionOptions: _lines }
  }
} catch (e) { _actionsResult = null }
const actionOptions = (Array.isArray(_actionsResult?.actionOptions) ? _actionsResult?.actionOptions : []).slice(0, 3)
// 兜底：结构化 actionItems 为空、但 build-actions 已从结论全文兜出行动项 → 用其回填，
// 保证 HTML「行动建议」章节与行动项卡片同源、不再出现「卡片有建议但报告没有」的分裂。
if ((!Array.isArray(actionItems) || actionItems.length === 0) && actionOptions.length > 0) {
  actionItems = actionOptions.map(a => ({ action: String(a), priority: '', dimension: '' }))
}
if (actionOptions.length > 0) {
  emit(`<aside>✅ 已生成 ${actionOptions.length} 条优先行动建议</aside>`)
} else {
  emit('<aside>ℹ️ 本次体检未发现需要优化的问题，行动项卡片将仅提供定时体检设置选项</aside>')
}

// 返回前统一清理本轮 dataCapture 落盘目录（必在上方合并完成之后；_wantHtml 为 false 时同样清理）。
// 传 allShopData：子图会各自建 runDir，只有按其落盘路径才能清到（见 cleanupRunDir 注释）。
await cleanupRunDir(allShopData)

// @node:final_return [end] inputs:conclusion,actionOptions
// 返回顺序 = 先「HTML 报告生成指引」，再「行动项渲卡指引」（行动项已在内部定稿，主 Agent 只渲卡与执行），
// 确保主 Agent 先出报告、再渲染行动项卡片
return formatReturnSummary(
  [
    { step: '店铺健康检查', detail: `完成 ${allShopData.length} 个店铺的${intent.dimensionText}诊断` },
    { step: '总结性结论', detail: '已输出健康等级、核心发现和优先行动建议' },
  ],
  [],
  { hasVizData: !!_dataFilePath }
) + buildVizGuide(_dataFilePath, conclusion, period, intent.dimensions, actionItems, userQuery)
  + buildActionSelectionGuide(actionOptions)
