// ═══ Sub-workflow: diagnose-shop ═══
// 单店铺全面诊断子工作流 — 按选定维度并行取数
// 输入: { shop, period, dimensions } (从父工作流注入)
// 输出: { shopName, loginId, period, dimensions: {...} }

// 提取店铺信息（引擎注入的 const 变量，禁止再写 const { shop } = inputs）
const _shop = shop || {}
const _loginId = _shop.loginId || ''
const _shopName = _shop.companyName || _shop.loginId || '当前店铺'
const _period = period || 'RECENT_7'
const _dims = dimensions || ['流量', '询盘', '成交', '商品', '客户', '广告', '风险']

// 构建店铺参数
const _shopArgs = _loginId ? ['--NEWTON_SHOP_LOGIN_ID', _loginId] : []
const _days = _period === 'RECENT_30' ? '30' : '7'
const _yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0]

// 广告接口日期（yyyyMMdd）：endDate=昨日，startDate=昨日往前 _days 天
const _fmtYmd = (d) => `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
const _adEndDate = _fmtYmd(new Date(Date.now() - 86400000))
const _adStartDate = _fmtYmd(new Date(Date.now() - 86400000 * Number(_days)))

// 任务构造器：argv 一律在此处拼好后下发给 batch_fetch.py，脚本只执行不拼参。
// 这条纪律是为了把参数特例（如 rag_query 不得带 --NEWTON_SHOP_LOGIN_ID）永久收在 workflow 侧，
// 避免参数逻辑在 JS 与 Python 两边各存一份而漂移。
const _cliTask = (key, args) => ({ key, argv: [CLI_SCRIPT, ...args] })
// freedom 跳技能取数（query_shop_data，路径写死）。cap：明细类接口单独收紧数组条数——
// /ad/item 与 /ad/customer 按默认 50 条摘要后各自就超 2 万字符（实测 22657 / 24542），
// 单独一张卡时就已压在平台截断阈值线外，合并后更不可能放过。
const _freedomTask = (key, dataSource, apiPath, params, cap) => {
  const argv = [FREEDOM_CLI, 'query_shop_data', '--data_source', dataSource, '--api_path', apiPath, '--params', JSON.stringify(params)]
  if (_loginId) argv.push('--NEWTON_SHOP_LOGIN_ID', _loginId)
  return cap ? { key, argv, array_cap: cap } : { key, argv }
}
const AD_DETAIL_CAP = 15

// 维度 → 卡片文案：一个维度一句口语化描述（只影响 UI 展示，不影响取数行为）。
// 未收录的维度名回落为通用文案，避免日后新增维度时卡片文案变成 undefined。
const _DIM_CARD_DESC = {
  '成交': (n) => `看看「${n}」最近生意的成色`,
  '流量': (n) => `蹲在「${n}」门口看看客流量`,
  '广告': (n) => `拿计算器敲敲「${n}」的广告账`,
  '商品': (n) => `瞧瞧「${n}」的商品`,
  '客户': (n) => `正在翻「${n}」的客户名册`,
  '风险': (n) => `排查「${n}」隐藏的提升空间`,
  '询盘': (n) => `正在「${n}」的柜台边，看询盘接得怎么样`,
}
const _cardDesc = (dim) => (_DIM_CARD_DESC[dim] ? _DIM_CARD_DESC[dim](_shopName) : `获取「${_shopName}」的${dim}维度数据`)

// ═══ Step 2: 按维度并行取数（一个维度一条 Bash 命令） ═══

const _hasTraffic = _dims.includes('流量')
const _hasInquiry = _dims.includes('询盘')
const _hasTransaction = _dims.includes('成交')
const _hasProduct = _dims.includes('商品')
const _hasCustomer = _dims.includes('客户')
const _hasAd = _dims.includes('广告')
const _hasRisk = _dims.includes('风险')

// 按维度分组：每组一次 runBatch（即一张卡片）。分组粒度选「维度」而不是「全合一条」：
// 错误定位仍能落到维度级，且单条信封的体量可控（实测除广告外各维度摘要均 ≤ 2 万字符）。
const _groups = []

// ── 成交维度（含订单履约 + 买家评价） ──
// 注：freedomCoreOverview(成交漏斗) 与 tradeIndex(成交总盘) 数据重叠，已移除
if (_hasTransaction) {
  _groups.push({
    dim: '成交',
    tasks: [
      _cliTask('tradeIndex', ['alibaba.1688.seller.trade.code.index', '--date_type', _period, ..._shopArgs]),
      _cliTask('coreMetrics', ['alibaba.1688.get.core.metrics', '--date_type', _period, ..._shopArgs]),
      _cliTask('orderRisk', ['shop_health_check', '--code', 'order_risk', ..._shopArgs]),
      _cliTask('feedback', ['shop_health_check', '--code', 'feedback', ..._shopArgs]),
    ],
  })
}

// ── 流量维度 ──
// 注：freedomFlowSource(流量来源) 与 channelTraffic(渠道流量) 重叠、freedomFlowBoard(流量大盘) 与 trafficOverview(流量概览) 重叠，已移除
// adChannelDetail(广告渠道下钻) 被流量与广告共用：只能归入一组取一次，两个维度在下方共同引用 _r.adChannelDetail
if (_hasTraffic) {
  const _trafficTasks = [
    _cliTask('trafficTrend', ['alibaba.1688.get.traffic.trend', '--query_date', _yesterday, '--days', _days, ..._shopArgs]),
    _cliTask('trafficOverview', ['alibaba.1688.get.traffic.overview', '--query_date', _yesterday, ..._shopArgs]),
    _cliTask('channelTraffic', ['alibaba.1688.get.channel.traffic', '--query_date', _yesterday, ..._shopArgs]),
    _cliTask('searchChannelDetail', ['alibaba.1688.get.search.channel.detail', '--query_date', _yesterday, ..._shopArgs]),
    _cliTask('recommendChannelDetail', ['alibaba.1688.get.recommend.channel.detail', '--query_date', _yesterday, ..._shopArgs]),
    _cliTask('adChannelDetail', ['alibaba.1688.get.ad.channel.detail', '--query_date', _yesterday, ..._shopArgs]),
  ]
  _groups.push({ dim: '流量', tasks: _trafficTasks })
}

// ── 广告维度（行业大盘对比 + freedom 广告账户/商品） ──
// freedom 参数为 startDate/endDate（yyyyMMdd）；未选流量时由本组负责取 adChannelDetail
if (_hasAd) {
  const _adTasks = []
  if (!_hasTraffic) {
    _adTasks.push(_cliTask('adChannelDetail', ['alibaba.1688.get.ad.channel.detail', '--query_date', _yesterday, ..._shopArgs]))
  }
  _adTasks.push(
    _cliTask('industryBenchmark', ['alibaba.1688.get.industry.benchmark', '--query_date', _yesterday, ..._shopArgs]),
    _freedomTask('adCustomer', 'AD', '/ad/customer', { startDate: _adStartDate, endDate: _adEndDate }, AD_DETAIL_CAP),
    _freedomTask('adItem', 'AD', '/ad/item', { startDate: _adStartDate, endDate: _adEndDate }, AD_DETAIL_CAP),
  )
  _groups.push({ dim: '广告', tasks: _adTasks })
}

// ── 商品维度 ──
// 注：拉新榜单/复购榜单(非核心细分)、活动参与效果(属活动维度非商品)、商品排行TOP freedom(与成交/流量榜单重叠)，已移除
if (_hasProduct) {
  _groups.push({
    dim: '商品',
    tasks: [
      _cliTask('abnormalOffer', ['alibaba.1688.seller.import.abnormal.offer', '--date_type', _period, ..._shopArgs]),
      _cliTask('topPayAmt', ['alibaba.1688.seller.top.offer', '--order_by', 'payAmt', '--range_type', _period, ..._shopArgs]),
      _cliTask('topUv', ['alibaba.1688.seller.top.offer', '--order_by', 'uv', '--range_type', _period, ..._shopArgs]),
      _cliTask('productStatus', ['alibaba.1688.get.product.status', '--query_date', _yesterday, ..._shopArgs]),
      _freedomTask('itemRate', 'ITEM', '/item/rate', { startDate: _adStartDate, endDate: _adEndDate }),
    ],
  })
}

// ── 客户维度 ──
// 注：freedomCustomerDetail(客户明细) 与 customerDetail(头部老客户明细) 数据重叠，已移除
if (_hasCustomer) {
  _groups.push({
    dim: '客户',
    tasks: [
      _cliTask('customerProvince', ['alibaba.1688.seller.customer.business.province', '--date_type', _period, ..._shopArgs]),
      _cliTask('customerDetail', ['alibaba.1688.seller.customer.detail', '--date_type', _period, ..._shopArgs]),
    ],
  })
}

// ── 风险维度（实时快照口径） ──
if (_hasRisk) {
  _groups.push({
    dim: '风险',
    tasks: [_cliTask('shopPunish', ['shop_health_check', '--code', 'shop_punish', ..._shopArgs])],
  })
}

// ── 询盘维度（通过 1688-shop-freedom-query-data 跳技能取数） ──
// @node:fetch_inquiry [tool] outputs:inquiryTasks
// rag_query 仅支持 --query（与店铺无关的纯语义检索），不得追加 --NEWTON_SHOP_LOGIN_ID，
// 否则 argparse 报 unrecognized arguments，导致每次体检都向分析注入一条必然失败记录
if (_hasInquiry) {
  _groups.push({
    dim: '询盘',
    tasks: [
      { key: 'ragResult', argv: [FREEDOM_CLI, 'rag_query', '--query', '询盘核心指标 询盘趋势 询盘商品排行'] },
      _freedomTask('inquiryCore', 'SYCM', 'customer/inquiry/coreIndex', { dataType: _period, device: 'ALL' }),
      _freedomTask('inquiryTrend', 'SYCM', 'customer/inquiry/coreIndexTrend', { dataType: _period, device: 'ALL' }),
      _freedomTask('inquiryRank', 'SYCM', 'customer/inquiry/itemRank', { dataType: _period, device: 'ALL' }),
    ],
  })
}

// @node:fetch_builtin [parallel] inputs:_shopArgs,_period,_days,_yesterday,_dims outputs:_rawResults
emit(`<aside>📋 正在综合分析「${_shopName}」的各项数据，包括：${_dims.join('、')}...</aside>`)
// 维度间仍由 workflow 侧 parallel 并发，维度内由 batch_fetch.py 的线程池并发，
// 峰值并发度与改造前的 25 任务全并发一致，墙上时间不退化。
const _groupResults = await parallel(_groups.map(g => () => runBatch(g.tasks, _cardDesc(g.dim))))

// 构建结果 map（key → 叶子）。parallel 对失败任务回 null，此时本组全部 key 如实标失败：
// 缺 key 会让下游拿到 undefined，被 compactShopData 当成「取到了但没数据」，又一条静默失败路径。
const _r = {}
_groupResults.forEach((leaves, i) => {
  const _g = _groups[i]
  if (leaves && typeof leaves === 'object') {
    Object.assign(_r, leaves)
    return
  }
  for (const _t of _g.tasks) {
    _r[_t.key] = { success: false, error: `${_g.dim}维度取数未返回结果`, command: _t.key, data: {} }
  }
})

emit(`<aside>✅ ${_shopName} 数据获取完成</aside>`)

// @node:collect_shop_data [transform] inputs:_shopName,_loginId,_period,_dims,_r
const _result = {
  shopName: _shopName,
  loginId: _loginId,
  period: _period,
  dimensions: {},
}

if (_hasTraffic) {
  _result.dimensions.traffic = {
    trend: _r.trafficTrend,
    overview: _r.trafficOverview,
    channelTraffic: _r.channelTraffic,
    searchDetail: _r.searchChannelDetail,
    recommendDetail: _r.recommendChannelDetail,
    adDetail: _r.adChannelDetail,
  }
}

if (_hasInquiry) {
  _result.dimensions.inquiry = {
    ragResult: _r.ragResult,
    coreIndex: _r.inquiryCore,
    coreIndexTrend: _r.inquiryTrend,
    itemRank: _r.inquiryRank,
  }
}

if (_hasTransaction) {
  _result.dimensions.transaction = {
    tradeIndex: _r.tradeIndex,
    coreMetrics: _r.coreMetrics,
    orderRisk: _r.orderRisk,
    feedback: _r.feedback,
  }
}

if (_hasProduct) {
  _result.dimensions.product = {
    abnormalOffer: _r.abnormalOffer,
    topPayAmt: _r.topPayAmt,
    topUv: _r.topUv,
    productStatus: _r.productStatus,
    itemRate: _r.itemRate,
  }
}

if (_hasCustomer) {
  _result.dimensions.customer = {
    province: _r.customerProvince,
    detail: _r.customerDetail,
  }
}

if (_hasAd) {
  _result.dimensions.ad = {
    channelDetail: _r.adChannelDetail,
    industryBenchmark: _r.industryBenchmark,
    adCustomer: _r.adCustomer,
    adItem: _r.adItem,
  }
}

if (_hasRisk) {
  _result.dimensions.risk = {
    shopPunish: _r.shopPunish,
  }
}

return _result
