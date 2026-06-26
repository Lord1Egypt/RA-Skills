const { getBookingGuide } = require('../core/service')
const staticHospitals = require('../data/hospitals.json')
const { matchHospital } = require('../core/resolver')
const { extractHospitalKeyword } = require('../core/preprocessor')
const { openUrl } = require('./browser/open-url')
const https = require('https')
const http = require('http')

// 实时医院列表（运行时替换）
let hospitals = staticHospitals

const HOSPITALS_API_URL = 'https://api.yestokr.com/openapi/HospitalManage/listing'
const HOSPITALS_API_TOKEN = 'beautsgo-openapi-fixed-token-change-me'

/**
 * 从后台 API 实时拉取医院列表
 * 失败时静默回退到本地 JSON
 */
function fetchHospitalList() {
  return new Promise((resolve, reject) => {
    const url = new URL(HOSPITALS_API_URL)
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: { 'X-Open-Token': HOSPITALS_API_TOKEN },
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', chunk => { data += chunk })
      res.on('end', () => {
        try {
          const json = JSON.parse(data)
          if (json.code === 0 && Array.isArray(json.data) && json.data.length > 0) {
            resolve(json.data)
          } else {
            reject(new Error(`API error: ${json.msg || 'empty data'}`))
          }
        } catch (e) {
          reject(new Error(`Parse error: ${data.slice(0, 100)}`))
        }
      })
    })
    req.on('error', reject)
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Timeout')) })
    req.end()
  })
}

/**
 * 识别用户意图
 *
 * 修复歧义问题：
 * - 首次带医院名的查询（"怎么咨询JD皮肤科"）一律判 view，不误触发 consult
 * - 只有纯操作词（没有医院名）才触发 open / book / consult
 * - 歧义消除规则：含有医院名 + 含有"咨询"= view（查看流程），而非 consult（自动化点击）
 *
 * @param {string} query 用户输入
 * @param {string[]} hospitalNames 所有医院名（用于检测输入是否含有医院名）
 * @param {object} context 跨轮上下文（用于 fill_form 判断）
 * @returns {string} 意图类型：'view' | 'open' | 'book' | 'consult' | 'price' | 'download'
 */
function detectIntent(query, hospitalNames = [], context = {}) {
  const q = query.trim()
  const qLower = q.toLowerCase()

  // ——— 是否含有明确的医院名（防止误判）———
  const containsHospitalName = hospitalNames.some(name =>
    qLower.includes(name.toLowerCase())
  )

  // ——— 是否有上下文传入的医院（用于 fill_form 判断）———
  const hasContextHospital = !!(context.resolvedHospital && context.resolvedHospital.name)

  // ——— 严格操作词检测（只有短句纯操作词才触发自动化）———
  const isOpenIntent = /^(打开链接|打开页面|帮我打开|打开医院页面)$/.test(q.trim())
  const isBookIntent = /^(帮我预约|直接预约|点击预约|自动预约)$/.test(q.trim()) ||
    (!containsHospitalName && (qLower.includes('帮我预约') || qLower.includes('直接预约') || qLower.includes('点击预约')))
  // consult 歧义修复：只有不含医院名的纯"咨询客服"才触发自动化
  const isConsultIntent = /^(咨询客服|联系客服|咨询一下|帮我咨询)$/.test(q.trim()) ||
    (!containsHospitalName && (qLower.includes('咨询客服') || qLower.includes('联系客服')))

  // ——— download：下载 APP ———
  const isDownloadIntent =
    /下载|download|安装app|装app/i.test(q)

  // ——— price：查看价格表（含医院名也允许触发）———
  const isPriceIntent =
    qLower.includes('价格') || qLower.includes('价钱') || qLower.includes('收费') ||
    qLower.includes('多少钱') || qLower.includes('费用') || qLower.includes('报价') ||
    qLower.includes('价格表') || qLower.includes('price') || qLower.includes('cost') ||
    /^(查价格|看价格|打开价格|价格页面)$/.test(q.trim())

  // ——— fill_form：用户提供预约信息（人数 + 时间 / 继续填写 / 提交）———
  // 识别策略：
  // - 明确填表关键词（无需上下文）
  // - 含人数词 / 日期词：必须同时有 context.resolvedHospital（第3轮之后），防止泛意图误触发
  const isFillFormIntent =
    /^(继续填写|填写信息|帮我填写|提交预约|确认预约)$/.test(q.trim()) ||
    // 包含人数词（N人、N位）—— 必须有上下文医院
    (/\d+\s*(人|位)/.test(q) && !containsHospitalName && hasContextHospital) ||
    // 包含日期（3月25日 / 25号 / 2026-03-25 等）—— 必须有上下文医院
    (/\d+(月|号|日|\/|-)\d*/.test(q) && !containsHospitalName && hasContextHospital)

  if (isDownloadIntent) return 'download'
  if (isFillFormIntent) return 'fill_form'
  if (isPriceIntent) return 'price'
  if (isConsultIntent) return 'consult'
  if (isBookIntent) return 'book'
  if (isOpenIntent) return 'open'

  // 默认：含有医院名 or 含有问询词 → 查看预约流程
  return 'view'
}

/**
 * 从 hospital.url 推导咨询页 URL
 *
 * URL 规则：
 *   详情页：https://i.beautsgo.com/cn/hospital/<slug>?from=skill
 *   咨询页：https://i.beautsgo.com/cn/hospital/<slug>-chat
 *
 * 优先使用 hospital.chat_url（如果有），否则自动推导
 */
function getChatUrl(hospital) {
  if (hospital.chat_url) return hospital.chat_url

  // 从 url 提取 slug（去掉查询参数）
  try {
    const parsed = new URL(hospital.url)
    // pathname 形如 /cn/hospital/<slug>
    const slug = parsed.pathname.replace(/^\/cn\/hospital\//, '').replace(/\/$/, '')
    return `https://i.beautsgo.com/cn/hospital/${slug}-chat`
  } catch (e) {
    // url 解析失败时兜底：直接拼
    const base = hospital.url.split('?')[0].replace(/\/$/, '')
    return `${base}-chat`
  }
}

/**
 * 从 hospital.url 推导价格表页 URL
 *
 * URL 规则：
 *   详情页：https://i.beautsgo.com/cn/hospital/<slug>?from=skill
 *   价格页：https://i.beautsgo.com/cn/hospital/<slug>-price
 *
 * 优先使用 hospital.price_url（如果有），否则自动推导
 */
function getPriceUrl(hospital) {
  if (hospital.price_url) return hospital.price_url

  try {
    const parsed = new URL(hospital.url)
    const slug = parsed.pathname.replace(/^\/cn\/hospital\//, '').replace(/\/$/, '')
    return `https://i.beautsgo.com/cn/hospital/${slug}-price`
  } catch (e) {
    const base = hospital.url.split('?')[0].replace(/\/$/, '')
    return `${base}-price`
  }
}

/**
 * 从 hospitals.json 中提取所有医院名（中文 + 英文 + 别名）
 * 用于意图识别中的医院名检测
 */
function getAllHospitalNames(hospitals) {
  const names = []
  for (const h of hospitals) {
    if (h.name) names.push(h.name)
    if (h.en_name) names.push(h.en_name)
    if (h.aliases) names.push(...h.aliases)
  }
  return names
}


/**
 * 解析用户输入，提取预约表单字段
 * @param {string} query 用户输入，如 "2人，3月26日，19102044571"
 * @returns {{ persons: number, dateText: string, contact: string }}
 */
function parseFormInput(query) {
  // 人数：匹配"2人"、"2位"、"两人"等
  let persons = 1
  const personMatch = query.match(/(\d+)\s*(人|位)/)
  if (personMatch) {
    persons = parseInt(personMatch[1], 10)
  } else if (query.includes('两人') || query.includes('两位')) {
    persons = 2
  } else if (query.includes('三人') || query.includes('三位')) {
    persons = 3
  }

  // 日期：匹配"3月26日"、"3月26号"、"26号"、"2026-03-26"、"26日"
  let dateText = ''
  const dateMatch =
    query.match(/(\d{1,2})[月\/\-](\d{1,2})[日号]?/) ||
    query.match(/(\d{4})[年\-\/](\d{1,2})[月\-\/](\d{1,2})/)
  if (dateMatch) {
    dateText = dateMatch[0]
  }

  // 联系方式：优先匹配手机号（11位数字），否则取去除人数、日期后的剩余内容
  let contact = ''
  const phoneMatch = query.match(/1[3-9]\d{9}/)
  if (phoneMatch) {
    contact = phoneMatch[0]
  } else {
    contact = query
      .replace(/\d+\s*(人|位)/g, '')
      .replace(/两人|两位|三人|三位/g, '')
      .replace(/\d{1,4}[年月\/\-]\d{1,2}[日号月\/\-]?\d{0,2}[日号]?/g, '')
      .replace(/[，,。.、！!？?]/g, ' ')
      .trim()
    if (contact.length < 2) contact = ''
  }

  // 时间段：上午 / 下午 / 全天（默认全天）
  let timeSlot = '全天'
  if (query.includes('上午') || query.match(/AM|morning/i)) timeSlot = '上午'
  else if (query.includes('下午') || query.match(/PM|afternoon/i)) timeSlot = '下午'

  return { persons, dateText, contact, timeSlot }
}

/**
 * 将日期文本解析为 YYYY-MM-DD 格式
 * 输入如："3月26日"、"4月5号"、"2026-04-05"
 */
function parseDateToISO(dateText) {
  // 已是 YYYY-MM-DD
  const isoMatch = dateText.match(/(\d{4})[年\-\/](\d{1,2})[月\-\/](\d{1,2})/)
  if (isoMatch) {
    const y = isoMatch[1]
    const m = String(isoMatch[2]).padStart(2, '0')
    const d = String(isoMatch[3]).padStart(2, '0')
    return `${y}-${m}-${d}`
  }
  // "3月26日" or "3月26号"
  const cnMatch = dateText.match(/(\d{1,2})[月\/](\d{1,2})[日号]?/)
  if (cnMatch) {
    const year = new Date().getFullYear()
    const m = String(cnMatch[1]).padStart(2, '0')
    const d = String(cnMatch[2]).padStart(2, '0')
    return `${year}-${m}-${d}`
  }
  return dateText
}

/**
 * 从用户输入中提取项目关键字（去除医院名和价格相关词后剩余的内容）
 * @param {string} query 用户原始输入
 * @param {object|null} hospital 已匹配的医院对象
 * @returns {string} 提取到的项目关键字（小写）
 */
function extractProjectKeyword(query, hospital) {
  let text = query.trim()

  // 1. 去除医院名（中文名、英文名、别名）
  if (hospital) {
    const hospitalNames = [hospital.name, hospital.en_name, ...(hospital.aliases || [])]
      .filter(Boolean)
      .map(n => n.toLowerCase())
    // 按长度降序排序，优先匹配长名
    hospitalNames.sort((a, b) => b.length - a.length)
    for (const name of hospitalNames) {
      if (text.toLowerCase().includes(name)) {
        text = text.replace(new RegExp(name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), '')
        break
      }
    }
  }

  // 2. 去除价格/查询相关词
  text = text.replace(/价格|价钱|收费|费用|报价|多少钱|价格表|查价格|看价格|打开价格|价格页面|查一下|查询|多少钱|怎么收费|price|cost|pricing/gi, '')

  // 3. 去除标点、空格、纯数字
  text = text.replace(/[，,。.、！!？?\s（）()\[\]【】：:;；"'"」「]/g, ' ').trim()

  // 4. 如果剩下的是单医院名、无意义词或空，返回空
  if (!text || text.length < 1) return ''

  // 5. 去除医院相关残留（如 "做""项目" 等泛词）
  text = text.replace(/做|项目|有|吗|多少/gi, '').trim()

  return text.toLowerCase()
}

/**
 * 通过接口查询项目价格
 * GET https://apis.beise.com:50144/c5d1dcbc/ProjectDraft/search?h_id={id}&keywords={keyword}
 */
function queryProjectPrice(h_id, keywords) {
  return new Promise((resolve, reject) => {
    const path = `/c5d1dcbc/ProjectDraft/search?h_id=${encodeURIComponent(h_id)}&keywords=${encodeURIComponent(keywords)}`
    const options = {
      hostname: 'apis.beise.com',
      port: 50144,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': '275aed9b-7c41-4a88-b291-20c0df803148',
      },
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', chunk => { data += chunk })
      res.on('end', () => {
        try {
          const json = JSON.parse(data)
          resolve(json)
        } catch (e) {
          resolve({ code: -1, msg: `响应解析失败: ${data.slice(0, 200)}` })
        }
      })
    })
    req.on('error', (e) => {
      resolve({ code: -1, msg: `请求失败: ${e.message}` })
    })
    req.setTimeout(15000, () => {
      req.destroy()
      resolve({ code: -1, msg: '请求超时' })
    })
    req.end()
  })
}

/**
 * 通过接口提交预约
 * POST https://api.yestokr.com/api/Appointment/saveFromSkill
 */
function submitBookingApi(payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload)
    const options = {
      hostname: 'api.yestokr.com',
      path: '/api/Appointment/saveFromSkill',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', chunk => { data += chunk })
      res.on('end', () => {
        try {
          const json = JSON.parse(data)
          resolve(json)
        } catch (e) {
          resolve({ code: -1, msg: `响应解析失败: ${data.slice(0, 200)}` })
        }
      })
    })
    req.on('error', (e) => {
      resolve({ code: -1, msg: `请求失败: ${e.message}` })
    })
    req.setTimeout(15000, () => {
      req.destroy()
      resolve({ code: -1, msg: '请求超时' })
    })
    req.write(body)
    req.end()
  })
}

/**
 * 主 Skill 入口
 *
 * context 约定（用于跨轮传递医院信息）：
 *   context.resolvedHospital  — 已解析的医院对象（由第1轮写入，后续轮次读取）
 *   context.lastQuery         — 上一轮含有医院名的原始 query（备用）
 */
module.exports = async function (input) {
  const { query, context = {} } = input
  const lang = input.lang || 'zh'

  // ——— 实时拉取最新医院列表，失败时静默使用本地数据 ———
  try {
    const freshData = await fetchHospitalList()
    hospitals = freshData
    console.log(`[Booking Skill] 实时拉取医院列表: ${hospitals.length} 家`)
  } catch (e) {
    // 静默回退，不阻塞主流程
    hospitals = staticHospitals
    console.warn(`[Booking Skill] API 拉取失败，使用本地数据: ${e.message}`)
  }

  // 预先加载所有医院名，用于意图识别的歧义消除
  const allHospitalNames = getAllHospitalNames(hospitals)
  const intent = detectIntent(query, allHospitalNames, context)

  /**
   * 获取当前医院对象的统一方法
   *
   * 优先级：
   * 1. context.resolvedHospital（AI 框架传入的上下文）
   * 2. 从当前 query 解析
   * 3. 扫描 context 所有字符串字段（兜底：AI 框架可能把历史文本放在不同字段）
   * 4. 只有 1 家医院时直接返回（单医院兜底）
   */
  function resolveHospital() {
    // 1. 优先从 context.resolvedHospital 读取
    if (context.resolvedHospital && context.resolvedHospital.name) {
      const h = matchHospital(context.resolvedHospital.name, hospitals)
      if (h) return h
      // context 里有 url 也能直接用
      if (context.resolvedHospital.url) return context.resolvedHospital
    }

    // 2. 从当前 query 解析
    const keyword = extractHospitalKeyword(query)
    if (keyword) {
      const h = matchHospital(keyword, hospitals)
      if (h) return h
    }

    // 2b. 兜底：从原始 query 中查找医院名（当 stop words 过度清洗时）
    //  场景："GU皮肤科江南店 Onda 价格" → keyword="GU店 Onda" 匹配失败
    //  但原始 query 中实际包含了"GU皮肤科江南店"完整名称
    if (query && query.trim()) {
      const originalLower = query.trim().toLowerCase()
      const h = hospitals.find(h => {
        const nameLower = (h.name || '').toLowerCase()
        return nameLower.length >= 2 && originalLower.includes(nameLower)
      })
      if (h) return h
    }

    // 3. 从 context 的已知字段中读取历史医院信息（只读取明确字段，不递归扫描）
    const knownContextFields = [
      context.lastQuery,
      context.query,
      context.hospitalName,
    ].filter(v => typeof v === 'string' && v.length > 0)

    for (const text of knownContextFields) {
      const kw = extractHospitalKeyword(text)
      if (kw) {
        const h = matchHospital(kw, hospitals)
        if (h) return h
      }
      const h2 = matchHospital(text, hospitals)
      if (h2) return h2
    }

    // 4. 单医院兜底：只有一家医院时直接返回
    if (hospitals.length === 1) {
      return hospitals[0]
    }

    return null
  }

  try {
    // ——————————————————————————————————————————
    // 第1轮：查看预约流程
    // 解析医院并写入返回值，供后续轮次使用
    // ——————————————————————————————————————————
    if (intent === 'view') {
      // 解析医院信息
      const keyword = extractHospitalKeyword(query)
      const hospital = matchHospital(keyword, hospitals)

      // ——————————————————————————————————————————
      // 兜底：匹配不到医院名 → 按项目类型给推荐列表
      // 场景："我在首尔打算做脸" / "想做皮肤管理" 等泛意图输入
      // ——————————————————————————————————————————
      if (!hospital) {
        // 精选推荐库（按项目类型，医院名必须存在于 hospitals.json）
        const RECOMMEND_MAP = {
          skin: {
            label: '皮肤管理 / 护肤',
            items: [
              { name: 'JD皮肤科',         note: '水光针/皮肤管理，网红爆款' },
              { name: '德安皮肤科',        note: '激光嫩肤、综合护理' },
              { name: 'AMRED皮肤科医院',   note: '医疗级护肤，口碑好' },
              { name: 'dayone皮肤科总院',  note: '多项目一站式护肤管理' },
              { name: 'CNP皮肤科狎鸥亭店', note: '清洁护理、注射类' },
            ],
          },
          eye: {
            label: '眼部整形',
            items: [
              { name: 'ID医院',               note: '多项目一站式，名气大' },
              { name: '原辰整形外科医院&皮肤科', note: '双眼皮、眼部综合' },
            ],
          },
          nose: {
            label: '鼻部整形',
            items: [
              { name: 'ID医院',               note: '鼻综合、隆鼻' },
              { name: '原辰整形外科医院&皮肤科', note: '鼻部整形专业' },
            ],
          },
          inject: {
            label: '注射美容（玻尿酸/肉毒素）',
            items: [
              { name: 'JD皮肤科',         note: '水光针/玻尿酸，最受欢迎' },
              { name: '德安皮肤科',        note: '注射美容专业' },
              { name: 'AMRED皮肤科医院',   note: '肉毒素注射' },
            ],
          },
          laser: {
            label: '激光 / 光子',
            items: [
              { name: 'JD皮肤科',         note: '皮秒、点阵激光' },
              { name: 'AMRED皮肤科医院',   note: '激光嫩肤' },
              { name: 'dayone皮肤科总院',  note: '光子嫩肤' },
            ],
          },
          face: {
            label: '面部轮廓 / 面部整形',
            items: [
              { name: 'ID医院',               note: '轮廓三件套，名气大' },
              { name: '原辰整形外科医院&皮肤科', note: '下颌/颧骨综合' },
            ],
          },
          breast: {
            label: '胸部整形',
            items: [
              { name: 'MD胸部外科医院', note: '胸部专科，专业度高' },
            ],
          },
          body: {
            label: '体雕 / 吸脂',
            items: [
              { name: 'ID医院',               note: '吸脂、体雕综合' },
              { name: '原辰整形外科医院&皮肤科', note: '体型管理' },
            ],
          },
        }

        // ——————————————————————————————————————————
        // 区域推荐:用户提到首尔/釜山/济州区域名时,推该区域热门医院
        // 优先级:region > category(区域更具体,优先推)
        // ——————————————————————————————————————————
        const REGION_RECOMMEND_MAP = {
          江南: {
            label: '首尔江南区',
            items: [
              { name: 'JD皮肤科',                   note: '水光针/皮肤管理,网红爆款' },
              { name: 'ID医院',                     note: '面部轮廓/眼鼻综合,名气大' },
              { name: 'Barog医院（江南店）',         note: '皮肤管理,江南热门' },
              { name: '陶瓷医院',                   note: '整形综合' },
              { name: '梅宗德医院',                 note: '皮肤科口碑老牌' },
              { name: '鹿美人皮肤科',               note: '皮肤管理与抗衰' },
              { name: 'Oganacell奥嘉娜皮肤科',      note: '高端皮肤管理' },
            ],
          },
          明洞: {
            label: '首尔明洞',
            items: [
              { name: '明洞丹雅皮肤科',             note: '皮肤管理/水光针' },
              { name: '明洞lijin皮肤科',            note: '中文服务,游客口碑' },
              { name: '明洞daybeau',                note: 'daybeau 明洞店,韩式护肤' },
              { name: '奥缇娜医院 明洞店',          note: '整形综合' },
            ],
          },
          弘大: {
            label: '首尔弘大',
            items: [
              { name: '弘大丽诺芙医院',             note: '皮肤管理/抗衰' },
              { name: '弘大mind皮肤科',             note: '弘大商圈口碑店' },
            ],
          },
          东大门: {
            label: '首尔东大门',
            items: [
              { name: '东大门doctors皮肤科',        note: '皮肤管理 + 多语言服务' },
              { name: '夏恩医院',                   note: '皮肤科综合' },
              { name: '德希尔皮肤科',               note: '德希尔连锁东大门' },
            ],
          },
          清潭: {
            label: '首尔清潭',
            items: [
              { name: '清潭minit',                  note: '皮肤管理' },
              { name: '清潭jionu医院',              note: '抗衰/整形综合' },
              { name: '清潭antian抗衰医院',         note: '抗衰专科' },
            ],
          },
          圣水: {
            label: '首尔圣水',
            items: [
              { name: '圣水serene 皮肤科',          note: '圣水商圈精品店' },
              { name: '圣水melting皮肤科',          note: '皮肤管理' },
              { name: '圣水艾瑞诗皮肤科医院',       note: 'iris 系列,综合护理' },
              { name: '圣水newlline皮肤科',         note: '皮肤管理新店' },
            ],
          },
          舍堂: {
            label: '首尔舍堂',
            items: [
              { name: '艾森秀皮肤科',               note: 'Essential 舍堂' },
            ],
          },
          釜山: {
            label: '釜山',
            items: [
              { name: '釜山JRYN 南浦店',            note: '皮肤管理/抗衰' },
              { name: '釜山丽诺博 renovo （西面）', note: 'renovo 釜山西面' },
              { name: '奥纳比整形外科',             note: '整形综合' },
              { name: '米米诊所(光州广川店)',       note: '皮肤管理' },
            ],
          },
          济州: {
            label: '济州岛',
            items: [
              { name: '济州4ever jeju',             note: '济州皮肤管理' },
              { name: 'Toxnfill济州店',             note: '注射/抗衰' },
            ],
          },
        }

        // 识别区域(放在 category 之前)
        let region = null
        if (/江南/.test(query)) region = '江南'
        else if (/明洞/.test(query)) region = '明洞'
        else if (/弘大/.test(query)) region = '弘大'
        else if (/东大门|东大门/.test(query)) region = '东大门'
        else if (/清潭/.test(query)) region = '清潭'
        else if (/圣水/.test(query)) region = '圣水'
        else if (/舍堂/.test(query)) region = '舍堂'
        else if (/釜山|busan/i.test(query)) region = '釜山'
        else if (/济州|jeju/i.test(query)) region = '济州'

        // 识别项目类型
        const qLower = query.toLowerCase()
        let category = null
        if (/皮肤管理|护肤|补水|美白|祛斑|肤质|做脸/.test(query)) category = 'skin'
        else if (/双眼皮|眼皮|眼型|开眼角/.test(query)) category = 'eye'
        else if (/鼻子|隆鼻|鼻型/.test(query)) category = 'nose'
        else if (/玻尿酸|肉毒素|botox|填充|注射/.test(qLower)) category = 'inject'
        else if (/激光|皮秒|光子|点阵/.test(query)) category = 'laser'
        else if (/脸|轮廓|下颌|颧骨|面部/.test(query)) category = 'face'
        else if (/胸|胸部|隆胸/.test(query)) category = 'breast'
        else if (/吸脂|瘦身|体型/.test(query)) category = 'body'

        // 区域优先级高于项目类型 — 区域信息更具体
        if (region && REGION_RECOMMEND_MAP[region]) {
          const rec = REGION_RECOMMEND_MAP[region]
          const lines = rec.items.map(item => {
            const h = hospitals.find(h => h.name === item.name)
            if (!h) return null
            return `• **${item.name}** — ${item.note}`
          }).filter(Boolean)

          if (lines.length > 0) {
            return `📍 **${rec.label}** 热门医美机构 — BeautsGO 平台口碑机构:

${lines.join('\n')}

👉 **直接说医院名字**,我帮你查预约流程
例如:"${rec.items[0].name}怎么预约" 或 "帮我预约${rec.items[0].name}"`
          }
        }

        if (category) {
          // 有项目意图 → 给精选推荐列表
          const rec = RECOMMEND_MAP[category]
          // 从 hospitals.json 查找对应链接
          const lines = rec.items.map(item => {
            const h = hospitals.find(h => h.name === item.name)
            if (!h) return null
            return `• **${item.name}** — ${item.note}`
          }).filter(Boolean)

          return `🏥 **${rec.label}** 推荐 — BeautsGO 平台口碑机构：

${lines.join('\n')}

👉 **直接说医院名字**，我帮你查预约流程
例如："JD皮肤科怎么预约" 或 "帮我预约德安皮肤科"`
        } else {
          // 无项目意图 → 通用引导
          return `你好！BeautsGO 平台收录了首尔 900+ 家正规医美机构 🏥

**皮肤管理 / 护肤** 口碑首选：
• JD皮肤科 — 水光针/皮肤管理，网红爆款
• 德安皮肤科 — 激光嫩肤、综合护理
• AMRED皮肤科医院 — 医疗级护肤

**整形手术** 口碑首选：
• ID医院 — 面部轮廓/眼鼻综合，名气大
• 原辰整形外科医院 — 综合整形，资历深

👉 告诉我你想做的项目或医院名，我帮你查预约流程`
        }
      }

      const guide = await getBookingGuide(query, lang)

      // 通过 __context__ 字段返回需要持久化的状态（由 AI 框架注入到下一轮 context）
      const hospitalHint = `\n\n<!-- __context__:resolvedHospital=${JSON.stringify({ name: hospital.name, url: hospital.url, en_name: hospital.en_name })} lastQuery=${encodeURIComponent(query)} -->`

      return `${guide}

---
💡 **接下来，选择你想要的操作：**

📖 **打开医院页面**
说"打开链接" → 我帮你打开 ${hospital.name} 的页面

💰 **查看价格表**
说"查价格" → 我帮你打开 ${hospital.name} 的价格表页面

⚡ **直接预约**
说"帮我预约" → 填写人数/时间，直接提交预约

💬 **在线咨询**
说"咨询客服" → 打开 ${hospital.name} 的在线客服页面

📲 **下载 APP**
说"帮我下载" → 获取 BeautsGO iOS / Android 下载链接

---
你想做哪个？${hospitalHint}`
    }

    // ——————————————————————————————————————————
    // 第2轮：打开链接
    // ——————————————————————————————————————————
    if (intent === 'open') {
      const hospital = resolveHospital()

      if (!hospital) {
        return '❌ 我还不知道你要查看哪家医院，请告诉我医院名称，例如"打开JD皮肤科的链接"。'
      }

      const opened = await openUrl(hospital.url).then(() => true).catch(() => false)
      if (!opened) {
        return `❌ 链接打开失败，请手动访问：${hospital.url}`
      }

      return `✅ 已打开 **${hospital.name}** 的页面！

页面地址：${hospital.url}

页面上你可以看到：
• 📍 医院地址和地图
• ⏰ 营业时间
• 💰 价格表和优惠
• 👨‍⚕️ 医生团队介绍
• ✅ 预约面诊 / 咨询按钮

接下来可以：
• 说"帮我预约" → 自动点击预约按钮
• 说"咨询客服" → 自动点击咨询按钮
• 说"换一家"并告诉我医院名 → 切换医院`
    }

    // ——————————————————————————————————————————
    // 第3轮：直接打开预约表单页 → 询问预约信息
    // ——————————————————————————————————————————
    if (intent === 'book') {
      const hospital = resolveHospital()

      if (!hospital) {
        return '❌ 我还不知道你要预约哪家医院，请告诉我医院名称，例如"帮我预约JD皮肤科"。'
      }

      return `好的，帮你预约 **${hospital.name}** 🏥

📝 请告诉我以下信息，我直接帮你提交预约：

1. **预约人数**（例如：1人、2人）
2. **预约时间**（例如：3月26日）
3. **时间段**（上午 / 下午 / 全天，默认全天）
4. **联系方式**（手机号）

👉 直接回复，例如："**2人，3月26日下午，19102044571**"`
    }

    // ——————————————————————————————————————————
    // 第4轮：用户提供信息 → 自动填表 + 提交
    // ——————————————————————————————————————————
    if (intent === 'fill_form') {
      const hospital = resolveHospital()

      if (!hospital) {
        return '❌ 我还不知道你要预约哪家医院，请先告诉我医院名称，例如"帮我预约JD皮肤科"。'
      }

      // 解析用户输入的表单字段
      const formData = parseFormInput(query)
      console.log(`[Booking Skill] 解析表单数据：`, JSON.stringify(formData))

      // 校验必填字段
      if (!formData.dateText) {
        return `⚠️ 请告诉我预约时间，例如："3月26日"。

其他信息可选：
• 预约人数（默认1人）
• 联系方式（手机号）`
      }

      if (!hospital.id) {
        return `❌ 该医院暂不支持在线预约（缺少医院ID），请手动打开 BeautsGO 预约：${hospital.url || ''}`
      }

      // 组装接口参数
      const dateISO = parseDateToISO(formData.dateText)
      const expectedTime = formData.timeSlot && formData.timeSlot !== '全天'
        ? `${dateISO} ${formData.timeSlot}`
        : `${dateISO} 全天`

      const payload = {
        contact: formData.contact || '',
        expected_time: expectedTime,
        project_type: '',
        d_id: '',
        h_id: hospital.id,
        p_id: '',
        num: formData.persons,
        source_type: 'skill',
      }

      console.log(`[Booking Skill] 提交接口参数：`, JSON.stringify(payload))
      const result = await submitBookingApi(payload)
      console.log(`[Booking Skill] 接口返回：`, JSON.stringify(result))

      if (result.code === 0) {
        return `✅ **预约已提交！**

📋 **预约信息摘要：**
• 🏥 机构：${hospital.name}
• 👥 人数：${formData.persons} 人
• 📅 时间：${expectedTime}${formData.contact ? `\n• 📞 联系方式：${formData.contact}` : ''}

🎉 提交成功！BeautsGO 平台会尽快联系机构为你匹配时间，确认短信将发送到你的账号绑定手机。

还有什么需要帮忙吗？`
      } else {
        const errMsg = result.msg || result.message || JSON.stringify(result)
        return `❌ 预约提交失败：${errMsg}

你可以通过以下方式手动预约：
• 打开 BeautsGO App，搜索"${hospital.name}"
• 或说"打开链接"，我帮你打开医院页面

如需重试，请告诉我新的预约信息。`
      }
    }

    // ——————————————————————————————————————————
    // 下载：返回 BeautsGO APP 下载链接
    // ——————————————————————————————————————————
    if (intent === 'download') {
      return `📲 **BeautsGO APP 下载**

🍎 **iOS（苹果）**
[App Store 下载](https://apps.apple.com/cn/app/beautsgo%E5%BD%BC%E6%AD%A4%E7%BE%8E-%E9%9F%A9%E5%9B%BD%E7%9A%AE%E8%82%A4%E7%A7%91%E9%A2%84%E7%BA%A6/id6741841509)

🤖 **Android（谷歌商店）**
[Google Play 下载](https://play.google.com/store/apps/details?id=uni.UNIEF980DB)

📦 **Android（国内直接安装包）**
[下载 APK](https://img.beautsgo.com/3.6.apk)（适合无法访问 Google Play 的用户）

安装后搜索医院名称即可预约 ✅`
    }

    // ——————————————————————————————————————————
    // 价格：优先调 API 查项目价格，无返回时打开价格表页面
    // ——————————————————————————————————————————
    if (intent === 'price') {
      const hospital = resolveHospital()

      if (!hospital) {
        return '❌ 我还不知道你要查询哪家医院的价格，请告诉我医院名称，例如"JD皮肤科价格"。'
      }

      // 尝试提取项目关键字
      const projectKeyword = extractProjectKeyword(query, hospital)

      // 如果有项目关键字，先调 API 查询具体价格
      if (projectKeyword && hospital.id) {
        const priceResult = await queryProjectPrice(hospital.id, projectKeyword)

        // API 返回有效数据
        if (priceResult && priceResult.code === 0 && priceResult.data && priceResult.data.length > 0) {
          const items = priceResult.data.map(item => {
            const priceText = item.korean_won ? `💰 ${new Intl.NumberFormat().format(parseFloat(item.korean_won))}원` : ''
            const unitText = item.unit ? `（${item.unit}）` : ''
            return `• **${item.name}**${unitText}\n  ${priceText}`
          }).join('\n')

          return `🏥 **${hospital.name}** — **${projectKeyword}** 项目价格

${items}

---
💡 想了解更多项目，说"查价格"查看全部价格表
📖 说"打开链接"查看医院详情
⚡ 说"帮我预约"直接提交预约申请`
        }
      }

      // API 无返回或没有项目关键字 → 回退到打开价格表页面
      const priceUrl = getPriceUrl(hospital)
      const opened = await openUrl(priceUrl).then(() => true).catch(() => false)

      if (opened) {
        return `✅ 已为你打开 **${hospital.name}** 的价格表页面！

价格页面：${priceUrl}

页面上你可以看到：
• 💰 各项目收费标准
• 🎁 当前优惠套餐
• 📋 项目详情说明

💡 如果想查询具体项目价格，可以说"${hospital.name} Onda 价格"

还需要预约或在线咨询吗？`
      } else {
        return `⚠️ 自动打开价格页面失败，请手动访问：

${priceUrl}

还需要其他帮助吗？`
      }
    }

    // ——————————————————————————————————————————
    // 咨询客服 → 直接打开咨询页
    // ——————————————————————————————————————————
    if (intent === 'consult') {
      const hospital = resolveHospital()

      if (!hospital) {
        return '❌ 我还不知道你要咨询哪家医院，请告诉我医院名称，例如"帮我咨询JD皮肤科"。'
      }

      const chatUrl = getChatUrl(hospital)
      const opened = await openUrl(chatUrl).then(() => true).catch(() => false)

      if (opened) {
        return `✅ 已为你打开 **${hospital.name}** 的在线客服对话页面！

客服页面：${chatUrl}

你可以直接向客服咨询：
• 询问价格和套餐详情
• 询问指定医生是否有档期
• 确认预约时间
• 了解术前术后注意事项

还需要预约或其他帮助吗？`
      } else {
        return `⚠️ 自动打开咨询页面失败，请手动访问：

${chatUrl}

除了网页客服，你也可以通过：
• 微信公众号搜索「BeautsGO 彼此美 APP」
• 添加客服微信：BeautsGOkr

还需要其他帮助吗？`
      }
    }

  } catch (err) {
    console.error('[Booking Skill] Error:', err.message)
    return `❌ 处理请求时出错：${err.message}。请重试或告诉我具体需求。`
  }
}
