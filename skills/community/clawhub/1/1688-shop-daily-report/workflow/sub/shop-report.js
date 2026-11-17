// ═══ Sub-workflow: 店铺日报（单店/多店统一，两段式：基础日报 → 深度补充分析） ═══
// 输入（由父图注入为同名 const）：mode('single'|'multi'), queryDate, prevDate, resolvedDate, userInput, shopHint
// 继承父图 @utility / @shared / @const
//
// 【为什么单店与多店合并为一个子图】
// CLI 层早已统一：get_multi_shop_report 传 --NEWTON_SHOP_LOGIN_ID 即只查该店，返回结构与多店一致
// （SKILL.md「使用原则」第 4-5 条明确「复用同一套并发管线」）。原先拆成两个子图后 10 个同名节点
// 逐一重复，导致多次「改了多店忘了单店」的不一致。真正的差异只有 3 处，已用条件分支收敛：
//   ① 单店需先 get_bindlist 把 shopHint 映射为 loginId；
//   ② 核心摘要表：单店纵向（指标×当日/日环比/周环比）vs 多店横向（店铺×指标）；
//   ③ 深度分析 prompt 与入参结构（deep-analysis-single / -multi）。
// 核心摘要列按【经营模式 × 阶段】动态选取（pickColumns）：Profile 推断与取数**并行**执行，
// 不拖慢首屏；Profile 模板文件（profiles/*.md）仍然只在基础日报输出后加载。
// 时序（对齐 SKILL 两段式）：取数∥Profile推断 → 基础日报（不含重点数据）→ 进度提示 → 知识大脑+模板+补充查询
// → 深度补充分析（含 LLM 生成的「四、重点数据」机会/风险）→ 行动选择

const isSingle = mode === 'single'

phase('店铺定位')

// @node:resolve_shop [tool] inputs:mode,shopHint outputs:targetLoginId,targetName
// 仅单店模式需要：先取绑定店铺列表，把 shopHint 映射为 loginId/companyName；多店模式跳过
let targetLoginId = ''
let targetName = ''
if (isSingle) {
  emit('<aside>📋 正在定位目标店铺...</aside>')
  const _bl = await callTool('Bash', buildBashCommand('python3', [CLI_SCRIPT, 'get_bindlist'], '查找目标店铺'))
  const _bindParsed = parseCliOutput(parseBashOutput(_bl), 'get_bindlist')
  const _bindList = _bindParsed?.data?.data?.data || _bindParsed?.data?.data || _bindParsed?.data || []
  const _hit = Array.isArray(_bindList)
    ? _bindList.find(s => shopHint && ((s.companyName && s.companyName.includes(shopHint)) || (s.loginId && String(s.loginId) === shopHint) || (shopHint.includes(s.companyName || '###'))))
    : null
  targetLoginId = _hit?.loginId || ''
  targetName = _hit?.companyName || shopHint || '当前登录店铺'
}

phase('基础数据')

// @node:fetch_and_infer [parallel] inputs:queryDate,targetLoginId,userInput outputs:reportBash,profile
// 取数与 Profile 推断并行：两者互不依赖（推断只需 userInput），并行后动态列选取几乎不增加首屏耗时。
// 单店/多店同一条命令：传 --NEWTON_SHOP_LOGIN_ID 则只查该店；内部并发查交易/流量/买家+广告+评价。
// Profile 推断失败时回退 integrated 默认值，绝不阻断日报（SKILL「空值 Fallback」）。
emit(isSingle ? '<aside>📋 先把这家店的生意数据拢到一块</aside>' : '<aside>📋 正在把每家店的生意数据拢到一块</aside>')
const _idArgs = (isSingle && targetLoginId) ? ['--NEWTON_SHOP_LOGIN_ID', targetLoginId] : []
const [_mr, _profRaw] = await Promise.all([
  callTool('Bash', buildBashCommand('python3',
    [CLI_SCRIPT, 'get_multi_shop_report', '--query_date', queryDate, ..._idArgs], isSingle ? '查询单店日报' : '批量查询多店铺日报', 180000)),
  // 推断失败（超时/模型报错）不得拖垮取数主链路：catch 后返 null，下方回落 integrated 默认值
  agent(
    __prompt('../prompts/infer-profile.prompt.md', { userInput: userInput || '（无额外输入）' }),
    { label: 'infer-profile', schema: {
      type: 'object', required: ['bizMode'],
      properties: {
        bizMode: { type: 'string', enum: ['factory', 'trader', 'integrated'] },
        profitSource: { type: 'string' },
        supplyCycle: { type: 'string' },
        moq: { type: 'string' },
        targetCustomer: { type: 'string' },
      },
    } }
  ).catch(() => null),
])
const reportBash = parseBashOutput(_mr)
// 必须过 parseAgentResult：推理模型会把结果包在 `<think>…</think>` 后，直接取字段会永远拿不到
// bizMode，使动态选列静默退化为 integrated 默认值（表面上日报正常，实际 Profile 适配形同虚设）。
const _prof = parseAgentResult(_profRaw)
const profile = {
  bizMode: (_prof && ['factory', 'trader', 'integrated'].includes(_prof?.bizMode)) ? _prof?.bizMode : 'integrated',
  profitSource: _prof?.profitSource || '薄利多销',
  supplyCycle: _prof?.supplyCycle || '',
  moq: _prof?.moq || '',
  targetCustomer: _prof?.targetCustomer || '',
}

// @node:parse_report [transform] inputs:reportBash outputs:shops,adReport,reviewData,activeLoginIds,hasValidData
const reportData = parseCliOutput(reportBash, 'get_multi_shop_report')
const _payload = reportData?.data || {}
const shops = Array.isArray(_payload.shops) ? _payload.shops : []
const adReport = _payload.adReport || null
const reviewData = _payload.reviewData || null
const activeShops = shops.filter(s => s.today && (num(s.today, 'gmv') > 0 || num(s.today, 'uv') > 0))
const activeLoginIds = activeShops.map(s => s.loginId).filter(Boolean)
const hasValidData = reportData?.success !== false && shops.some(s => s.today && !s.error)

// @node:data_check [condition] expression:hasValidData
if (!hasValidData) {
  // @branch:无有效数据 → empty_return
  // @node:empty_return [end] inputs:resolvedDate
  // 错误原因优先聚合店铺级 error：顶层 success=true 时 markdown 是「查询成功」文案，
  // 直接当原因会输出「未能获取…原因：多店铺日报查询成功」的矛盾提示（线上实锤）；
  // success=false 时 markdown 本身携带真实错误（如 HTTP 409），仍可作为原因。
  const _shopErrs = [...new Set(shops.map(s => s && s.error).filter(Boolean))]
  const _err = (_shopErrs.join('；').slice(0, 300))
    || (reportData?.success === false ? (reportData?.markdown || reportData?.error) : '')
    || (isSingle ? '未取到该店铺的有效经营数据' : '未取到任何店铺的有效经营数据')
  const _who = isSingle ? `「${targetName}」` : ''
  emit(`### ⚠️ 无法生成日报\n\n未能获取${_who}「${resolvedDate}」的经营数据。原因：${_err}\n\n请检查鉴权配置或日期参数后重试。`)
  return `日报生成终止：${_err}（${_who}日期 ${resolvedDate}）`
}
// @branch:有数据继续 → build_base_metrics

phase('基础日报')

// @node:build_base_metrics [transform] inputs:shops outputs:shopMetrics,abnormalAll
// 逐店归一化 + 全量指标（日环比优先用接口预计算值）+ 内部阶段判定 + 异常识别；按成交额降序。
// 阶段仅内部使用、绝不输出；基础日报用通用指标，此段不加载 Profile，异常阈值用 integrated 通用档
const shopMetrics = shops.map(s => {
  const today = normalizeMetrics(s.today)
  const prev = normalizeMetrics(s.prevDay)
  // 上周同日（服务端已多查一天）：用于派生指标的周环比与转化率基准比对；缺失时为 null
  const weekAgo = s.weekAgo ? normalizeMetrics(s.weekAgo) : null
  const preDod = {
    gmv: (s.today && typeof s.today.gmvDayOnDay === 'number') ? s.today.gmvDayOnDay : null,
    orderCount: (s.today && typeof s.today.orderDayOnDay === 'number') ? s.today.orderDayOnDay : null,
    inquiryCount: (s.today && typeof s.today.inquiryDayOnDay === 'number') ? s.today.inquiryDayOnDay : null,
  }
  const metrics = computeMetricSet(today, prev, preDod, weekAgo)
  let stage = '成长'
  if (today.gmv < 300 || today.uv < 50) stage = '起步'
  if (today.gmv > 6000 || today.orderCount > 10) stage = '成熟'
  return {
    companyName: s.companyName || targetName || '未知店铺', loginId: s.loginId || '', error: s.error || null,
    today, metrics, stage, abnormal: collectAbnormal(metrics, THRESHOLDS.integrated[stage]),
  }
}).sort((a, b) => (b.metrics.gmv.raw || 0) - (a.metrics.gmv.raw || 0))
const abnormalAll = shopMetrics.filter(m => m.abnormal.length > 0)
const _topShop = shopMetrics[0]
const _shopNames = shopMetrics.map(m => m.companyName)
// 整体阶段：单店取该店阶段；多店按 SKILL「经营阶段自动推断」用多店均值判定（仅用于选列，绝不输出）
let overallStage = _topShop.stage
if (!isSingle && shopMetrics.length > 1) {
  const _n = shopMetrics.length
  const _avgGmv = shopMetrics.reduce((s, m) => s + (m.metrics.gmv.raw || 0), 0) / _n
  const _avgUv = shopMetrics.reduce((s, m) => s + (m.metrics.uv.raw || 0), 0) / _n
  const _avgOrder = shopMetrics.reduce((s, m) => s + (m.metrics.order.raw || 0), 0) / _n
  overallStage = '成长'
  if (_avgGmv < 300 || _avgUv < 50) overallStage = '起步'
  if (_avgGmv > 6000 || _avgOrder > 10) overallStage = '成熟'
}

// @node:emit_base_report [emit] inputs:shopMetrics,abnormalAll,adReport,reviewData,profile outputs:
// 【基础日报】首屏：📊 标题 + （多店）店铺范围 + 经营总览 + 核心摘要 + 广告 + 评价；不含重点数据与今日行动重点
// 「四、重点数据」改由深度阶段的 LLM 基于异常事实生成（含归因解读），见 emit_deep
// 核心摘要列按【经营模式 × 整体阶段】动态选取（COLUMN_PREFS，如 integrated 成熟期→成交额/订单量/客单价/老客占比）；
// 阶段名与判定逻辑仅内部使用，绝不出现在报告正文
const BASE_COLUMNS = pickColumns(profile.bizMode, overallStage)
// 差异②：单店纵向表 vs 多店横向表
// 单店纵向表不受屏幕宽度限制，列全部可用指标（Profile 关注的排前）；多店横向表仍取精简的 4-5 列
let _summarySection = ''
if (isSingle) {
  const _keys = singleMetricKeys(profile.bizMode, overallStage)
  // 服务端已多查上周同日并自算周环比，正常情况下各指标都有值；
  // 仅当上周同日数据缺失（接口异常等）时整列为空，此时直接省掉这一列，不摆空表格
  const _hasWeek = _keys.some(k => {
    const c = _topShop.metrics[k]
    return c && c.week !== null && c.week !== undefined
  })
  const _rows = _keys.map(k => metricRow(_topShop.metrics, k, _hasWeek)).filter(Boolean).join('\n')
  _summarySection = _hasWeek
    ? `| 指标 | 当日 | 日环比 | 周环比 |\n| ---- | ---- | ---- | ---- |\n${_rows}`
    : `| 指标 | 当日 | 日环比 |\n| ---- | ---- | ---- |\n${_rows}`
} else {
  const _colHeader = '| 店铺 | ' + BASE_COLUMNS.map(k => METRIC_META[k].name).join(' | ') + ' |'
  const _colDivider = '| ---- |' + BASE_COLUMNS.map(() => ' ---- |').join('')
  const _tableRows = shopMetrics.map(m => '| ' + m.companyName + ' | ' + BASE_COLUMNS.map(k => metricCell(m.metrics, k)).join(' | ') + ' |').join('\n')
  _summarySection = `${_colHeader}\n${_colDivider}\n${_tableRows}`
}
// 经营总览：单店讲这一家，多店讲合计 + 最高店 + 异常店家数；支付买家数（新+老）用户常点名要，
// 接口有数据但原先正文不展示，导致外层 Agent 误判指标缺失而回退技能重查
const _buyersOf = (m) => (m.today.newBuyerCount || 0) + (m.today.oldBuyerCount || 0)
const _overviewLine = isSingle
  ? `「${_topShop.companyName}」${resolvedDate} 成交额 ¥${fmtNum(_topShop.metrics.gmv.raw)}（日环比 ${fmtPct(_topShop.metrics.gmv.dod)}）、订单 ${_topShop.metrics.order.raw} 单、支付买家 ${_buyersOf(_topShop)} 人（新客 ${_topShop.today.newBuyerCount || 0} / 老客 ${_topShop.today.oldBuyerCount || 0}）、客户咨询 ${_topShop.metrics.inquiry.raw} 次、访客 ${_topShop.metrics.uv.raw} 人${_topShop.abnormal.length ? `，有 ${_topShop.abnormal.length} 项指标需要关注` : '，各项指标总体平稳'}。`
  : `${_shopNames.length} 家店铺合计成交额 ¥${fmtNum(shopMetrics.reduce((sum, m) => sum + (m.metrics.gmv.raw || 0), 0))}、合计支付买家 ${shopMetrics.reduce((sum, m) => sum + _buyersOf(m), 0)} 人，其中「${_topShop.companyName}」成交额最高（¥${fmtNum(_topShop.metrics.gmv.raw)}）${abnormalAll.length ? `；有 ${abnormalAll.length} 家店铺出现需要关注的指标波动` : '；各店指标总体平稳'}。`
// 店铺范围段仅多店需要（≤5 全列，>5 用「A、B、C 等共 x 家」）
const _scopeSection = isSingle ? '' : `\n## 店铺范围\n本次分析 ${_shopNames.length} 家店铺：${_shopNames.length <= 5 ? _shopNames.join('、') : `${_shopNames.slice(0, 3).join('、')} 等共 ${_shopNames.length} 家店铺`}\n`
const baseReport = `# 📊 1688店铺日报 - ${resolvedDate}
${_scopeSection}
## 经营总览
${_overviewLine}

## 一、核心摘要
${_summarySection}
${adBlock(adReport)}${reviewBlock(reviewData)}`
emit(baseReport)

// @node:emit_progress [emit]
emit('<aside>⏳ 有几处数据反常，我再挖一挖</aside>')

phase('深度补充')

// @node:wiki_context [parallel] inputs:abnormalAll outputs:wikiContext
// 基础日报已输出后，只为重点店铺补充商家背景；失败为空，不影响深度分析。
// 候选逻辑单店/多店天然统一：有异常的店优先，再补成交额最高且未入选的店，最多 3 家
// （单店时 shopMetrics 只有 1 项，无论是否有异常都恰好选中它）。
// 两项提速：① 规则文件只读一次后复用（原先写在 collectShopWiki 内，N 家店会重复读 N 次）；
//            ② N 家店的子任务并发（subTask 已传 label 区分店铺），原先是逐家 await 串行。
const _wikiTargets = []
for (const m of abnormalAll) {
  if (m.loginId && !_wikiTargets.some(x => x.loginId === m.loginId)) _wikiTargets.push(m)
}
if (_topShop && _topShop.loginId && !_wikiTargets.some(x => x.loginId === _topShop.loginId)) _wikiTargets.push(_topShop)
const _wikiPicked = _wikiTargets.slice(0, 3)
const _wikiRules = _wikiPicked.length > 0 ? await readRef('wiki-routing-rules.md') : ''
if (_wikiPicked.length > 0) emit('<aside>🔍 结合你店铺的档案深度分析</aside>')
const _wikiResults = _wikiPicked.length > 0
  ? await Promise.all(_wikiPicked.map(m => collectShopWiki({ loginId: m.loginId, companyName: m.companyName }, _wikiRules)))
  : []
const _wikiContextList = []
for (let _i = 0; _i < _wikiPicked.length; _i++) {
  if (_wikiResults[_i]) _wikiContextList.push({ shopName: _wikiPicked[_i].companyName, context: _wikiResults[_i] })
}
// 结果也只报一行：补充到几家就说几家，一家都没补充到则明确告知，不逐店刷屏
if (_wikiPicked.length > 0) {
  emit(_wikiContextList.length > 0
    ? `<aside>✅ ${_wikiContextList.length}家店的档案都拿到了！</aside>`
    : '<aside>暂时没找到店铺档案，不影响分析</aside>')
}
const wikiContext = _wikiContextList.length > 0 ? JSON.stringify(_wikiContextList, null, 2) : ''

// @node:load_profile [tool] inputs:profile outputs:profileText
// 按推断经营模式加载对应诊断模板（模板文件仅供深度分析使用，保持在基础日报之后加载；
// profile 字段本身已在取数阶段并行推断完成）
// 命令描述对商家可见，SKILL「输出格式·用语规范」将 Profile / 模板文件名列为禁露术语，故用中文人话。
const _isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
const _profilePath = PROFILE_TEMPLATES[profile.bizMode] || PROFILE_INTEGRATED
const _profileCmd = _isWin ? `type ${shellEscape(_profilePath)}` : `cat ${shellEscape(_profilePath)}`
const _pf = await callTool('Bash', buildBashCommand('sh', ['-c', _profileCmd], '对照经营诊断的思路，看看有什么能优化的'))
const profileText = (parseBashOutput(_pf).stdout || '').slice(0, 1600)

// @node:profile_query [tool] inputs:activeLoginIds,profile outputs:profileExtra
// 按推断 Profile 从目录选出触发命中的补充查询（不同经营模式查不同数据源）；无目标店铺或无命中查询则跳过。
// 单店零流量时 activeLoginIds 为空，仍用目标店 loginId 兜底，保持与拆分前的单店行为一致
let profileExtra = null
const _profileQueries = selectProfileQueries(profile, PROFILE_QUERY_CATALOG)
const _queryIds = activeLoginIds.length > 0 ? activeLoginIds : ((isSingle && targetLoginId) ? [targetLoginId] : [])
if (_queryIds.length > 0 && _profileQueries.length > 0) {
  emit('<aside>⚙️ 再调几个关键指标，把问题看得更透</aside>')
  const _pe = await callTool('Bash', buildBashCommand('python3',
    [CLI_SCRIPT, 'batch_query_profile_data', '--queries', JSON.stringify(_profileQueries), '--shop_login_ids', JSON.stringify(_queryIds)], '关键指标补充查询', 180000))
  const _peParsed = parseCliOutput(parseBashOutput(_pe), 'batch_query_profile_data')
  profileExtra = _peParsed?.success !== false ? (_peParsed?.data || null) : null
}

// @node:deep_analysis [agent] inputs:shopMetrics,profileText,profileExtra,adReport,reviewData outputs:deep
// 结合 Profile 差异化指标 + 补充查询做深度归因，产出差异化洞察 + 今日行动重点（只讲基础日报没有的新信息）
// 差异③：单店按指标维度组织入参 + 独立 prompt（字数上限 200-350），多店按店铺维度（400-600）
const _common = {
  identity: DEFAULT_IDENTITY,
  bizMode: BIZ_MODE_LABEL[profile.bizMode] || DEFAULT_BIZ_MODE,
  profileText,
  adReportJson: adReport && adReport.hasData ? JSON.stringify(adReport, null, 2).slice(0, 900) : '无广告数据',
  reviewDataJson: reviewData && reviewData.hasData ? JSON.stringify(reviewData.summary, null, 2).slice(0, 600) : '无评价数据',
  profileExtraJson: profileExtra ? JSON.stringify(profileExtra, null, 2).slice(0, 1000) : '无补充数据',
  wikiContextJson: wikiContext || '无商家背景信息',
}
let _promptFile = '../prompts/deep-analysis-multi.prompt.md'
let _promptVars = _common
if (isSingle) {
  const _rows = ['gmv', 'order', 'uv', 'inquiry', 'conv', 'avgPrice', 'oldRatio'].map(k => ({
    指标: METRIC_META[k].name,
    当日: fmtVal(_topShop.metrics[k].raw, METRIC_META[k].fmt),
    日环比: METRIC_META[k].noDod ? '-' : fmtPct(_topShop.metrics[k].dod),
  }))
  const _abn = _topShop.abnormal.map(a => ({ 指标: a.metric, 变动: a.change }))
  _promptFile = '../prompts/deep-analysis-single.prompt.md'
  _promptVars = Object.assign({}, _common, {
    companyName: _topShop.companyName,
    resolvedDate,
    metricsJson: JSON.stringify(_rows, null, 2),
    abnormalJson: _abn.length > 0 ? JSON.stringify(_abn, null, 2) : '无显著异常',
  })
} else {
  _promptVars = Object.assign({}, _common, {
    metricsJson: JSON.stringify(shopMetrics.map(m => ({
      店铺: m.companyName,
      成交额: fmtNum(m.metrics.gmv.raw), 成交额日环比: fmtPct(m.metrics.gmv.dod),
      订单量: m.metrics.order.raw, 订单日环比: fmtPct(m.metrics.order.dod),
      访客数: m.metrics.uv.raw, 访客日环比: fmtPct(m.metrics.uv.dod),
      客单价: m.metrics.avgPrice.raw, 客单价日环比: fmtPct(m.metrics.avgPrice.dod),
      客户咨询: m.metrics.inquiry.raw, 成交转化率: m.metrics.conv.raw,
      老客占比: m.metrics.oldRatio.raw, 老客占比日环比: fmtPct(m.metrics.oldRatio.dod),
      异常: m.abnormal.map(a => `${a.metric}${a.change}`),
    })), null, 2),
  })
}
// agent 调用（超时/模型服务报错）会直接 reject：不加防护会拖垮整个 workflow，
// 首屏日报已发出却在深度阶段报「Workflow failed」回退技能重跑（已实测一次）。
// 失败时 deep=null，emit_deep 自动降级：重点数据用程序阈值版 focusSides，行动重点走兜底文案。
let _deepFailed = false
let deep = null
try {
  deep = parseAgentResult(await agent(
    __prompt(_promptFile, _promptVars),
    { label: isSingle ? 'deep-analysis-single' : 'deep-analysis-multi', schema: {
      type: 'object', required: ['actions'],
      properties: {
        focus: { type: 'object', properties: {
          opportunities: { type: 'array', items: { type: 'object', properties: { shop: { type: 'string' }, metric: { type: 'string' }, change: { type: 'string' }, reason: { type: 'string' } } } },
          risks: { type: 'array', items: { type: 'object', properties: { shop: { type: 'string' }, metric: { type: 'string' }, change: { type: 'string' }, reason: { type: 'string' } } } },
        } },
        insights: { type: 'array', items: { type: 'object', properties: { label: { type: 'string' }, value: { type: 'string' }, insight: { type: 'string' } } } },
        actions: { type: 'array', items: { type: 'object', properties: { action: { type: 'string' }, reason: { type: 'string' }, shop: { type: 'string' } } } },
      },
    } }
  ))
} catch (e) {
  _deepFailed = true
}

phase('深度输出')

// @node:emit_deep [emit] inputs:deep outputs:deepActions
// 【四、重点数据】+【深度补充分析】：机会/风险优先用 LLM 生成版（异常事实已由脚本注入 prompt，
// 模型只做归因解读，数字不靠模型编造）；LLM 对应侧缺失/解析失败时回退程序阈值版（focusSides），
// 确保板块永不开天窗。itemLine 同时兼容对象与「店铺/指标/原因」斜杠字符串（qwen 不完全遵守 schema 的既有教训）。
const _llmSide = (arr) => Array.isArray(arr)
  ? arr.map(it => { const _l = itemLine(it); return _l ? `- ${_l}` : '' }).filter(Boolean)
  : []
const _progSides = focusSides(shopMetrics, 5, isSingle)
const _llmFocus = (deep && deep.focus) || {}
const _finalOpp = _llmSide(_llmFocus.opportunities)
const _finalRisk = _llmSide(_llmFocus.risks)
// 深度解读调用失败（_deepFailed）时先认账再说，不静默；随后照常用兜底数据渲染，日报不中断
if (_deepFailed) emit('<aside>⚠️ 深度解读这次没跑成，我先用已取到的数据给你划重点</aside>')
const focusSection = `## 四、重点数据
### 📈 机会
${_finalOpp.length > 0 ? _finalOpp.join('\n') : (_progSides.opp.length > 0 ? _progSides.opp.join('\n') : '- 无显著正向异常')}
### ⚠️ 风险
${_finalRisk.length > 0 ? _finalRisk.join('\n') : (_progSides.risk.length > 0 ? _progSides.risk.join('\n') : '- 无显著负向风险')}`
// 【深度补充分析】追加段：差异化洞察 + 今日行动重点（始终输出行动重点，即使无补充洞察）
// deep 已经 parseAgentResult 容错；仍为空时才走兜底文案。若这里频繁出现“暂无”，
// 优先怀疑 agent 返回格式而非模型真的无话可说（已发生过一次：思考块未剥离导致结果全丢）。
const _insights = Array.isArray(deep?.insights) ? deep?.insights : []
const _insightLines = _insights.map(it => {
  const _head = [it.label, it.value].filter(Boolean).join('：')
  return _head ? `- **${_head}**${it.insight ? ` — ${it.insight}` : ''}` : (it.insight ? `- ${it.insight}` : '')
}).filter(l => l.trim() && l.trim() !== '-').join('\n')
const deepActions = Array.isArray(deep?.actions) ? deep?.actions : []
const _actionLines = deepActions.length > 0
  ? deepActions.map((a, i) => `${i + 1}. ${actionLine(a)}`).join('\n')
  : '1. 暂无特别行动建议，保持日常运营节奏'
emit(`${focusSection}

## 🔍 深度补充分析
${_insightLines || '- 暂无更多差异化洞察'}

### 今日行动重点
${_actionLines}`)

// @node:report_return [end] inputs:deepActions outputs:reportPayload
// 本子图**不再调用兄弟子图**，只回传数据；行动卡片改由主图弹。
// 原因（已实测）：__subgraph 相对路径基准在三方不一致 —— run-swj 按主图目录、
// validate-code 按当前文件目录，而平台上两种写法都报 missing file，导致流程在末段失败，
// 并被平台按 SKILL.md 的回退规则转到技能路径（表现为日报从头重跑一遍）。
// 只保留「主图 → sub/」单层引用则无歧义：主图就在 workflow/ 根目录，
// 两种基准下 './sub/xxx.js' 都指向同一个文件。不要把卡片逻辑改回子图。
// overview/insights 回传给主图嵌入 return：定时任务等场景外层 Agent 看不到 emit 正文，
// 返回值里必须自带结论摘要，否则它会误判「没拿到数据」而回退技能重查（已实测）。
return {
  actions: deepActions,
  reportKind: isSingle ? '单店铺' : '多店铺',
  shopCount: _shopNames.length,
  overview: _overviewLine,
  insights: _insightLines,
}
