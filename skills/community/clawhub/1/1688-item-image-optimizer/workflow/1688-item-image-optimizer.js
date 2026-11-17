// ════════════════════════════════════════════════════════════════════
// item-image-optimizer Workflow (SWJ 结构化编码)
// 商品图片制作统一入口：意图识别 → 权限校验 → 构建入口 → open_tab（终态）
//
// 严格对应 SKILL.md 的 SOP：
//   路径 A（意图明确 + 基础功能 main/carousel/detail/replaceSubject）→ 免校验 → build_tool_url → open_tab
//   路径 B（意图明确 + 数字模特 digitalModel）→ verify_permission
//            ├─ digitalModel=true  → build_tool_url → open_tab
//            └─ digitalModel=false → 提示文案（禁 open_tab）
//   路径 C（意图模糊 ambiguous）→ verify_permission → 按权限平铺 select_image_type → build_tool_url → open_tab
//   横切：有图必带（单图 --img-url / 多图 --img-url-list）；图片超限 → select_images 选子集
//   横切：verify_permission success=false → fail-closed 拦截（禁 open_tab）
// ════════════════════════════════════════════════════════════════════

// ─── Meta ────────────────────────────────────────────────
export const meta = {
  name: '1688-item-image-optimizer',
  description: '1688 商品图片制作统一入口：识别图片类型意图 →（数字模特/模糊意图先校验权限）→ 构建工具页 URL → open_tab 唤起页面（fire-and-forget 终态）。不做：新品发布/批量上架、品牌VI/海报/店铺装修、图片规范问答。',
  whenToUse: '做图、做一套图、出一套图、主图优化、优化主图、轮播图、详情图、背景替换、换背景、数字模特、模特图、商品图片制作、改图、图片优化、提升转化的图',
  phases: [
    { title: '意图识别', detail: '从用户输入识别图片类型意图（明确 type / 模糊），并提取 offerId 与图片 URL' },
    { title: '权限校验', detail: '数字模特或意图模糊时校验商家数字模特权限（fail-closed）' },
    { title: '构建入口', detail: '处理图片超限，构建工具页 URL 并 open_tab 唤起（终态）' },
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

// @utility:buildBashCommand
// 跨平台兼容：自动检测 Windows/macOS 并生成对应 shell 语法，捕获 stdout/stderr/exitCode
function buildBashCommand(program, args, description, timeout = 120000) {
  const isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const tmpDir = isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const sep = isWin ? '\\' : '/'
  const id = `_wf${Date.now()}${Math.random().toString(36).slice(2, 5)}`
  const outF = `${tmpDir}${sep}${id}_o`
  const errF = `${tmpDir}${sep}${id}_e`
  const shellCmd = [program, ...args.map(a => shellEscape(String(a)))].join(' ')
  const redirectedCmd = `${shellCmd} > "${outF}" 2> "${errF}"`
  let command
  if (isWin) {
    command = `setlocal enabledelayedexpansion & ${redirectedCmd} & echo !errorlevel! & type "${outF}" & echo. & echo __WFSE__: & type "${errF}" & del /f /q "${outF}" "${errF}"`
  } else {
    command = `${redirectedCmd}; _ec=$?; echo $_ec; cat "${outF}"; printf '\\n__WFSE__:'; cat "${errF}"; rm -f "${outF}" "${errF}"`
  }
  return { command, timeout, description: description || `run: ${program}` }
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

// @utility:parseCliJson
// 解析 CLI 输出的 JSON。优先用 {"success" 标记，否则退回【第一个】'{'（顶层对象起点）。
// ⚠️ 必须用 indexOf 而非 lastIndexOf：lastIndexOf('{') 会落到嵌套内层的 '{'，截出残缺片段导致误判 success=false。
// 解析失败时绝不把原文残片塞进 markdown（会被误当业务数据泄漏给用户）。
function parseCliJson(bashResult, command) {
  const raw = String(bashResult && bashResult.stdout || '')
  const stderr = String(bashResult && bashResult.stderr || '')
  let idx = raw.indexOf('{"success"')
  if (idx === -1) idx = raw.indexOf('{')
  if (idx === -1) {
    return { success: false, markdown: stderr.slice(0, 300).trim() || 'CLI 无有效输出', command, data: {} }
  }
  try { return JSON.parse(raw.slice(idx)) }
  catch (e) { return { success: false, markdown: `CLI 输出解析失败（${command}）`, command, data: {} } }
}

// @utility:permData
// 容忍网关包裹层数差异：在 data / data.data / data.data.data 里定位真正含 digitalModel 的权限对象。
function permData(perm) {
  const candidates = [
    perm && perm.data && perm.data.data && perm.data.data.data,
    perm && perm.data && perm.data.data,
    perm && perm.data,
    perm,
  ]
  for (const c of candidates) {
    if (c && typeof c === 'object' && 'digitalModel' in c) return c
  }
  return (perm && perm.data && perm.data.data) || {}
}

// @utility:parseAnswers
// 卡片回传多级兜底解析（showInteraction 返回结构不固定）。
// 实测生产回传形如 { selectionType, data:[{question, answer}], _instruction }，
// 即 result.data 本身就是 answers 数组（元素是 {question, answer/selected/value} 对象），
// 而非带 .answers 属性的对象。这里同时兼容 result.data(数组) / result.data.answers / result.answers，
// 并从每个 answer 对象里抽出 label（answer / selected / value），selected 可能是数组（多选）。
function parseAnswers(result) {
  const root = result || {}
  let answers = null
  if (Array.isArray(root.data)) answers = root.data
  else if (root.data && Array.isArray(root.data.answers)) answers = root.data.answers
  else if (Array.isArray(root.answers)) answers = root.answers
  const flat = (v, out) => {
    if (v == null) return
    if (Array.isArray(v)) { for (const x of v) flat(x, out); return }
    if (typeof v === 'object') {
      const picked = v.answer != null ? v.answer : (v.selected != null ? v.selected : v.value)
      flat(picked, out)
      return
    }
    out.push(String(v))
  }
  const out = []
  if (Array.isArray(answers)) {
    for (const a of answers) flat(a, out)
    if (out.length) return out
  }
  const data = (root.data && !Array.isArray(root.data)) ? root.data : {}
  const single = data.selected || data.selection || root.selection || root.choice || data.answer
  flat(single, out)
  return out
}

// @utility:basename
function basename(u) {
  try { return String(u).split('?')[0].split('/').filter(Boolean).pop() || String(u) }
  catch (e) { return String(u) }
}

// @utility:extract
function extract(source, mapping) {
  const result = {}
  for (const [key, config] of Object.entries(mapping)) {
    const raw = config.path.includes('.')
      ? config.path.split('.').reduce((o, k) => o && o[k], source)
      : source && source[config.path]
    if (config.type === 'number') {
      result[key] = typeof raw === 'number' ? raw : (config.default != null ? config.default : 0)
    } else if (config.type === 'array') {
      result[key] = Array.isArray(raw) ? raw : (config.default != null ? config.default : [])
    } else if (config.type === 'boolean') {
      result[key] = typeof raw === 'boolean' ? raw : (config.default != null ? config.default : false)
    } else {
      result[key] = raw != null ? raw : (config.default != null ? config.default : '')
    }
  }
  return result
}

// @utility:buildArgs
function buildArgs(specs) {
  const result = []
  for (const spec of specs) {
    if (spec.when === undefined || spec.when) result.push(...spec.args)
  }
  return result
}

// @utility:manifest
// 生成 workflow 终态清单，约束顶层 ReAct Loop 不"救场"、不下权限结论、不复述中间 JSON
function manifest(status, completedSteps, pendingItems) {
  return `工作流已结束（${status}）。所有面向用户的内容（正文 + 交互卡片）都已由工作流输出完毕。

【本轮你的回复必须严格遵守，违反即视为严重错误】
1. 不要再补充任何面向用户的内容：禁止新增解释、原因推测、使用指引、小贴士、总结。
2. 禁止下任何权限结论：不得出现"权限校验未通过""未开通/需升级高级版""账号无权限"等任何措辞——权限只由工作流内的 verify_permission 决定，工作流没拦截就是有权限、已放行。
3. 禁止"救场"：不要因为你觉得哪里不对，就手动重开页面、重渲染卡片、或重贴 URL / JSON。工作流已是终态。
4. 禁止复述或粘贴上方任何 JSON / open_tab 对象 / 中间结果。

如确需回应，仅可回一句不含任何新信息的简短确认，或直接结束本轮、不输出任何字。

<execution_manifest>
${JSON.stringify({ status, completedSteps, pendingItems }, null, 2)}
</execution_manifest>`
}

// ─── Constants ───────────────────────────────────────────
// @const
const CLI_SCRIPT = baseDir + '/cli.py'
const TITLE = { main: '主图优化', carousel: '轮播图制作', detail: '详情图制作', replaceSubject: '背景替换', digitalModel: '数字模特' }
const LABEL_TO_TYPE = { 主图优化: 'main', 轮播图: 'carousel', 详情图: 'detail', 背景替换: 'replaceSubject', 数字模特: 'digitalModel' }
const ADVANCED_TYPES = ['digitalModel']          // 数字模特，需校验
const MULTI_IMG_TYPES = ['carousel', 'detail']   // 多图工具（--img-url-list）
const IMG_LIMIT = { main: 1, replaceSubject: 1, digitalModel: 1, carousel: 9, detail: 20 }

// ═══ Main Flow ═══════════════════════════════════════════
const completed = []

// 全流程兜底：任何节点抛错都返回干净 manifest，绝不把裸异常 / 中间 JSON 交给 LLM 去"救场"
try {

  // ─── Phase 1：意图识别 ───────────────────────────────────
  phase('意图识别')
  emit('<aside>📋 正在识别图片制作意图...</aside>')

  // @node:parse_user_input [transform] inputs:args outputs:userInput
  const userInput = (typeof args === 'string' && args.trim()) ? args.trim() : ''

  // @node:intent_detect [agent] inputs:userInput outputs:intentResult
  const intentResult = await agent(
    `你是 1688 图片制作意图识别器。根据用户输入判断要制作的图片类型，并提取可选的商品 ID 与图片地址。

用户输入：「${userInput.slice(0, 1000)}」

触发词 → type 映射规则：
- 主图优化 / 优化主图 / 生成更好的主图 / 主图哪里有问题 → main
- 轮播图 / 做轮播图 → carousel
- 详情图 / 做详情图 → detail
- 背景替换 / 换背景 → replaceSubject
- 数字模特 / 模特图 / 生成模特 / 换模特 / AI模特 → digitalModel
- 做图 / 做一套图 / 出一套图 / 商品图片 / 商品图制作 / 提升转化的图 / 优化图片 / 改图（意图笼统、未指明具体类型）→ ambiguous

提取规则：
- offerId：用户输入中 8 位以上的纯数字商品 ID，无则留空字符串
- imgUrls：用户输入中出现的图片 URL（http/https）或本地文件路径（/Users/...、~/...、D:\\...）；附件图片的 path 字段也算；无则空数组。禁止编造路径。

判断不准时优先返回 ambiguous（更安全，会走权限校验+选择卡片）。`,
    {
      label: 'intent-detect',
      schema: {
        type: 'object',
        required: ['intent'],
        properties: {
          intent: { type: 'string', enum: ['main', 'carousel', 'detail', 'replaceSubject', 'digitalModel', 'ambiguous'] },
          offerId: { type: 'string' },
          imgUrls: { type: 'array', items: { type: 'string' } },
        },
      },
    }
  )

  // @node:extract_intent [extract] source:intentResult outputs:intent,offerId,imgUrlsRaw
  const { intent, offerId, imgUrlsRaw } = extract(intentResult, {
    intent: { path: 'intent', default: 'ambiguous' },
    offerId: { path: 'offerId', default: '' },
    imgUrlsRaw: { path: 'imgUrls', type: 'array', default: [] },
  })

  // @node:normalize_intent [transform] inputs:intent,offerId,imgUrlsRaw outputs:finalType,cleanOfferId,imgUrls
  let finalType = intent || 'ambiguous'
  const cleanOfferId = String(offerId || '').trim()
  const imgUrls = (Array.isArray(imgUrlsRaw) ? imgUrlsRaw : []).map(u => String(u || '').trim()).filter(Boolean)
  log(`意图识别: type=${finalType}, offerId=${cleanOfferId || '无'}, imgUrls=${imgUrls.length}`)
  completed.push(`意图识别 → ${finalType}`)

  // ─── Phase 2：权限校验（路径 B 数字模特 / 路径 C 意图模糊）─────────────
  // @node:need_perm_check [condition] expression:finalType==='ambiguous' || ADVANCED_TYPES.includes(finalType)
  const needPerm = (finalType === 'ambiguous') || ADVANCED_TYPES.includes(finalType)
  if (needPerm) {
    // @branch:需校验 → verify_permission
    phase('权限校验')
    emit('<aside>⚙️ 正在校验图片制作权限...</aside>')

    // @node:verify_permission [tool] inputs: outputs:perm
    const _permRaw = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, 'verify_permission'], '校验数字模特权限'))
    const perm = parseCliJson(parseBashOutput(_permRaw), 'verify_permission')

    // @node:perm_success_check [condition] expression:perm.success
    if (!perm || !perm.success) {
      // @branch:校验失败 → block_perm_fail
      // 铁律 fail-closed：校验失败一律拦截，禁 open_tab
      emit(perm && perm.markdown ? perm.markdown : '❌ 权限校验失败，请稍后重试或先运行 `cli.py configure YOUR_AK` 配置 AK')
      // @node:block_perm_fail [end] inputs:completed
      return manifest('blocked', completed, ['verify_permission 失败（fail-closed 拦截），未渲染 open_tab'])
    } else {
      // @branch:校验成功 → extract_perm
    }

    // @node:extract_perm [transform] inputs:perm outputs:digitalModel
    const digitalModel = !!permData(perm).digitalModel
    log(`权限: digitalModel=${digitalModel}`)
    completed.push(`权限校验 → digitalModel=${digitalModel}`)

    // @node:intent_route [condition] expression:finalType==='ambiguous'
    if (finalType === 'ambiguous') {
      // @branch:意图模糊 → build_type_options
      // @node:build_type_options [transform] inputs:digitalModel outputs:options
      const options = ['主图优化', '轮播图', '详情图', '背景替换']
      if (digitalModel) options.push('数字模特')

      emit('<aside>🔄 请在下方卡片中选择要制作的图片类型...</aside>')
      // @node:select_image_type [interaction] inputs:options outputs:typeSel
      const typeSel = await showInteraction({
        type: 'card',
        name: 'select_image_type',
        selectionType: 'image_type',
        questions: [{ question: '你想制作哪种商品图片？', options, allowMultiple: false, required: true }],
      })
      log(`select_image_type 原始回传: ${JSON.stringify(typeSel)}`)

      // @node:resolve_type [transform] inputs:typeSel outputs:finalType
      finalType = LABEL_TO_TYPE[parseAnswers(typeSel)[0]] || ''

      // @node:type_valid_check [condition] expression:finalType
      if (!finalType) {
        // @branch:无效选择 → block_no_type
        emit('未获取到有效的图片类型选择，请重新发起需求。')
        // @node:block_no_type [end] inputs:completed
        return manifest('blocked', completed, ['select_image_type 未返回有效选择'])
      } else {
        // @branch:有效选择 → prep_imgs
      }
      completed.push(`用户选择 → ${TITLE[finalType]}(${finalType})`)
    } else {
      // @branch:数字模特 → advanced_perm_check
      // @node:advanced_perm_check [condition] expression:digitalModel
      if (!digitalModel) {
        // @branch:无权限 → block_no_perm
        emit('数字模特功能暂未对你的账号开放～')
        // @node:block_no_perm [end] inputs:completed
        return manifest('blocked', completed, [`${TITLE[finalType]} 权限不通过（digitalModel=false），按规则禁止 open_tab`])
      } else {
        // @branch:有权限 → prep_imgs
      }
    }
  } else {
    // @branch:免校验 → prep_imgs
    // 路径 A（基础功能 main/carousel/detail/replaceSubject）：免校验，直接进入构建入口
  }

  // ─── Phase 3：构建入口（图片超限处理 + build_tool_url + open_tab）──────────
  phase('构建入口')

  // @node:prep_imgs [transform] inputs:finalType,imgUrls outputs:limit,chosenImgs
  const limit = IMG_LIMIT[finalType] || 1
  let chosenImgs = imgUrls

  // @node:overflow_check [condition] expression:imgUrls.length > limit
  if (imgUrls.length > limit) {
    // @branch:超限 → select_images
    emit(`<aside>⚠️ 上传了 ${imgUrls.length} 张图片，${TITLE[finalType]}最多支持 ${limit} 张，请选择要处理的图片...</aside>`)
    const labels = imgUrls.map((u, i) => `图片${i + 1}（${basename(u)}）`)

    // @node:select_images [interaction] inputs:imgUrls,labels,limit outputs:imgSel
    const imgSel = await showInteraction({
      type: 'card',
      name: 'select_images',
      selectionType: 'image',
      questions: [{
        question: `你上传了 ${imgUrls.length} 张图片，${TITLE[finalType]}工具最多支持 ${limit} 张。请选择要处理的图片：`,
        options: labels,
        allowMultiple: true,
        required: true,
      }],
    })

    // @node:resolve_imgs [transform] inputs:imgSel,imgUrls,limit outputs:chosenImgs
    const pickedLabels = parseAnswers(imgSel)
    const picked = pickedLabels
      .map(lab => { const m = String(lab).match(/图片(\d+)/); return m ? imgUrls[parseInt(m[1], 10) - 1] : null })
      .filter(Boolean)
    chosenImgs = (picked.length ? picked : imgUrls).slice(0, limit)
    completed.push(`图片超限选择 → ${chosenImgs.length}/${imgUrls.length} 张`)
  } else {
    // @branch:未超限 → build_url_args
    // @node:trim_imgs [transform] inputs:imgUrls,limit outputs:chosenImgs
    chosenImgs = imgUrls.slice(0, limit)
  }

  // @node:build_url_args [buildArgs] inputs:finalType,cleanOfferId,chosenImgs outputs:cliArgs
  const cliArgs = buildArgs([
    { args: ['build_tool_url', '--type', finalType] },
    { when: !!cleanOfferId, args: ['--offer-id', cleanOfferId] },
    { when: chosenImgs.length > 0 && MULTI_IMG_TYPES.includes(finalType), args: ['--img-url-list', chosenImgs.join(',')] },
    { when: chosenImgs.length > 0 && !MULTI_IMG_TYPES.includes(finalType), args: ['--img-url', chosenImgs[0] || ''] },
  ])

  emit('<aside>⚙️ 正在生成工具页面入口...</aside>')
  // @node:build_tool_url [tool] inputs:cliArgs outputs:built
  const _builtRaw = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, ...cliArgs], `构建工具页 URL(${finalType})`))
  const built = parseCliJson(parseBashOutput(_builtRaw), 'build_tool_url')

  // @node:build_success_check [condition] expression:built.success
  if (!built || !built.success) {
    // @branch:构建失败 → block_build_fail
    emit(built && built.markdown ? built.markdown : '❌ 工具页面构建失败，请稍后重试')
    // @node:block_build_fail [end] inputs:completed
    return manifest('error', completed, [`build_tool_url(${finalType}) 失败，未渲染 open_tab`])
  } else {
    // @branch:构建成功 → extract_open_tab
  }
  completed.push(`build_tool_url(${finalType}) → 成功`)

  // @node:extract_open_tab [extract] source:built outputs:openUrl,openTitle
  const { openUrl, openTitle } = extract(built, {
    openUrl: { path: 'data.open_tab.url', default: '' },
    openTitle: { path: 'data.open_tab.title', default: '' },
  })

  // @node:resolve_title [transform] inputs:openTitle,finalType outputs:title
  const title = openTitle || TITLE[finalType] || '图片优化'

  // open_tab 交互（fire-and-forget 终态）；字段严格对齐 interaction-specs §1：仅 type/selectionType/url/title
  // @node:open_tab [interaction] inputs:openUrl,title outputs:
  await showInteraction({ type: 'open_tab', name: 'open_tab_image_optimize', selectionType: 'shop_backend', url: openUrl || '', title })
  completed.push(`open_tab → ${title}`)

  // @node:final_return [end] inputs:completed
  return manifest('success', completed, [])

} catch (e) {
  const errMsg = (e && e.message) ? e.message : String(e)
  log(`workflow 异常兜底: ${errMsg}`)
  emit('图片工具暂时无法打开，请稍后重试～')
  // @node:catch_fallback [end] inputs:completed
  return manifest('error', completed, [`workflow 抛出异常，已兜底拦截（未渲染 open_tab）：${errMsg}`])
}