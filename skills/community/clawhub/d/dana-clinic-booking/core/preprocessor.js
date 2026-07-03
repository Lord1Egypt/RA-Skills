/**
 * JD皮肤科预约技能 — 预处理层
 *
 * 功能：
 * 1. 检测用户意图（view / open / book / consult / price / download）
 * 2. 解析自然语言中的预约表单信息（人数、日期、时间段、联系方式）
 * 3. 提取项目关键字（价格查询用）
 */

// ── 意图检测规则 ─────────────────────────────────────────────────────────────

/**
 * 检测用户意图
 * @param {string} query 用户输入
 * @param {object} context 多轮对话上下文
 * @returns {string} 'view' | 'open' | 'book' | 'consult' | 'price' | 'download'
 */
function detectIntent(query, context = {}) {
  const q = query.trim()
  const qLower = q.toLowerCase()

  // 是否有历史医院上下文（对于单医院技能，通常总是有）
  const hasContext = !!(context.resolvedHospital && context.resolvedHospital.name)

  // ── download ──
  if (/(下载|download|app|客户端)/i.test(qLower) &&
      !qLower.includes('预约')) return 'download'

  // ── open ──
  if (/^(打开链接|打开页面|帮我打开|打开医院页面|打开详情)$/.test(q.trim())) return 'open'
  if (/^打开/i.test(q.trim()) && q.trim().length <= 6) return 'open'

  // ── book ──
  if (/^(帮我预约|直接预约|点击预约|自动预约|提交预约)$/.test(q.trim())) return 'book'
  if (/帮我预约|直接预约|点击预约|自动预约|我要预约|我想预约|预约一下/.test(qLower) &&
      !qLower.includes('怎么') && !qLower.includes('如何') && !qLower.includes('流程')) return 'book'

  // ── consult ──
  if (/^(咨询客服|联系客服|咨询一下|帮我咨询|在线咨询)$/.test(q.trim())) return 'consult'
  if (/咨询|客服|问一下/.test(qLower) && !qLower.includes('怎么')) return 'consult'

  // ── price ──
  if (/(价格|多少钱|怎么收费|报价|费用|价钱|查价格|价格表|价目)/.test(qLower)) return 'price'

  // ── 预约信息（包含人数、日期等）→ book 的延续 ──
  if (/(\d+[人人位]|\d+月|今天|明天|后天|周[一二三四五六日天]|星期[一二三四五六日天])/.test(q) &&
      hasContext && context.intent === 'book') return 'book'

  // ── 纯数字/简短信息（延续上一轮 book） ──
  if (/^\d{11}$/.test(q.trim()) && hasContext && context.intent === 'book') return 'book'
  if (/^\d+[人人位]/.test(q.trim()) && hasContext && context.intent === 'book') return 'book'

  // ── 默认：view（查看预约指南） ──
  return 'view'
}

// ── 预约表单解析 ─────────────────────────────────────────────────────────────

/**
 * 从自然语言中解析预约表单信息
 * 输入: "2人，3月26日下午，电话19102044571"
 * 输出: { persons: 2, dateText: "3月26日", timeSlot: "下午", contact: "19102044571" }
 */
function parseFormInput(query) {
  const result = {
    persons: 1,
    dateText: '',
    timeSlot: '',
    contact: ''
  }

  let q = query.trim()

  // 提取人数
  const personMatch = q.match(/(\d+)\s*[人人位]/)
  if (personMatch) {
    result.persons = parseInt(personMatch[1], 10)
    q = q.replace(personMatch[0], '')
  }

  // 提取联系方式（手机号）
  const phoneMatch = q.match(/(1[3-9]\d{9})/)
  if (phoneMatch) {
    result.contact = phoneMatch[1]
    q = q.replace(phoneMatch[0], '')
  }

  // 提取时间
  // 上午/下午/晚上
  const timeSlotMatch = q.match(/(上午|下午|晚上)/)
  if (timeSlotMatch) {
    result.timeSlot = timeSlotMatch[1]
    q = q.replace(timeSlotMatch[0], '')
  }

  // 日期：今天/明天/后天 或 X月X日 或 X月X号
  const today = new Date()
  const todayStr = `${today.getMonth() + 1}月${today.getDate()}日`

  if (/今天/.test(q)) {
    result.dateText = todayStr
  } else if (/明天/.test(q)) {
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    result.dateText = `${tomorrow.getMonth() + 1}月${tomorrow.getDate()}日`
  } else if (/后天/.test(q)) {
    const dayAfter = new Date(today)
    dayAfter.setDate(dayAfter.getDate() + 2)
    result.dateText = `${dayAfter.getMonth() + 1}月${dayAfter.getDate()}日`
  } else {
    const dateMatch = q.match(/(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]/)
    if (dateMatch) {
      result.dateText = `${parseInt(dateMatch[1], 10)}月${parseInt(dateMatch[2], 10)}日`
    }
  }

  return result
}

/**
 * 从价格查询中提取项目关键字
 * 输入: "JD皮肤科 Onda 价格" → "Onda"
 */
function extractProjectKeyword(query, hospital) {
  let q = query.trim()
  // 移除医院名
  if (hospital.name) q = q.replace(new RegExp(hospital.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '')
  if (hospital.alias) q = q.replace(new RegExp(hospital.alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '')
  if (hospital.short_name) q = q.replace(new RegExp(hospital.short_name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), '')
  if (hospital.en_name) q = q.replace(new RegExp(hospital.en_name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), '')

  // 移除价格相关词
  q = q.replace(/(价格|多少钱|怎么收费|报价|费用|价钱|查价格|价格表|价目|查|看|的)/g, '')
  q = q.replace(/[，,。.!?？、；;:\s]/g, ' ').trim()

  return q || ''
}

module.exports = { detectIntent, parseFormInput, extractProjectKeyword }
