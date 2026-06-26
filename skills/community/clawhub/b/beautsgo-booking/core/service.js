const hospitals = require('../data/hospitals.json')
const { matchHospital, generateSearchKeywords } = require('./resolver')
const { render, loadI18n } = require('./renderer')
const { extractHospitalKeyword } = require('./preprocessor')

async function getBookingGuide(query, lang = 'zh') {
  // 1. 预处理：从自然语言中提取医院名关键词
  const keyword = extractHospitalKeyword(query)
  
  // 2. 匹配医院
  const hospital = matchHospital(keyword, hospitals)
  if (!hospital) {
    // Read not_found message from i18n; fall back to Chinese if key is missing
    let i18n
    try { i18n = loadI18n(lang) } catch (_) { i18n = {} }
    return i18n.not_found || '请告诉我医院名称，我帮你生成预约流程'
  }

  const enriched = {
    ...hospital,
    search_keywords: generateSearchKeywords(hospital)
  }

  return render(enriched, lang)
}

module.exports = { getBookingGuide }
