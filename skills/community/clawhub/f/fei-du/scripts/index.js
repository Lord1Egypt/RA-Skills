/**
 * 非毒·分析魄 - 数据分析与洞察提取
 */

/**
 * 数据分析
 */
function analyze(data) {
  const { type, content, context } = data
  const insights = []
  const patterns = []
  const anomalies = []
  
  if (type === 'text' && typeof content === 'string') {
    // 文本分析
    const words = content.split(/\s+/).filter(w => w.length > 0)
    const wordCount = words.length
    
    // 提取关键词（简单词频）
    const wordFreq = {}
    words.forEach(w => {
      const clean = w.replace(/[^\w]/g, '').toLowerCase()
      if (clean.length > 2) {
        wordFreq[clean] = (wordFreq[clean] || 0) + 1
      }
    })
    
    const topWords = Object.entries(wordFreq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([word, count]) => ({ word, count }))
    
    insights.push({
      key: '词频统计',
      value: `共${wordCount}词，高频词：${topWords.slice(0, 3).map(w => w.word).join(', ')}`,
      confidence: 0.85
    })
    
    patterns.push({
      type: 'word_frequency',
      description: '词频分布模式',
      data: topWords
    })
    
    // 检测异常
    if (content.includes('错误') || content.includes('失败') || content.includes('异常')) {
      anomalies.push({
        type: 'negative_sentiment',
        position: content.indexOf('错误') || content.indexOf('失败'),
        content: '检测到负面情绪词汇'
      })
    }
    
    // 句子分析
    const sentences = content.split(/[.!?。！？]+/).filter(s => s.trim())
    if (sentences.length > 1) {
      insights.push({
        key: '内容结构',
        value: `共${sentences.length}个句子，平均${Math.round(wordCount / sentences.length)}词/句`,
        confidence: 0.9
      })
    }
  } else if (type === 'number' || type === 'list') {
    // 数值/列表分析
    const arr = Array.isArray(content) ? content : content.split(',').map(Number)
    const nums = arr.filter(n => typeof n === 'number' && !isNaN(n))
    
    if (nums.length > 0) {
      const sum = nums.reduce((a, b) => a + b, 0)
      const avg = sum / nums.length
      const min = Math.min(...nums)
      const max = Math.max(...nums)
      
      insights.push({
        key: '统计摘要',
        value: `总和${sum.toFixed(2)}，均值${avg.toFixed(2)}，范围[${min}, ${max}]`,
        confidence: 0.95
      })
      
      // 检测趋势
      if (nums.length >= 3) {
        const first = nums.slice(0, Math.floor(nums.length / 2))
        const second = nums.slice(Math.floor(nums.length / 2))
        const firstAvg = first.reduce((a, b) => a + b, 0) / first.length
        const secondAvg = second.reduce((a, b) => a + b, 0) / second.length
        
        if (secondAvg > firstAvg * 1.1) {
          patterns.push({ type: 'increasing', description: '数据呈上升趋势' })
        } else if (secondAvg < firstAvg * 0.9) {
          patterns.push({ type: 'decreasing', description: '数据呈下降趋势' })
        }
      }
    }
  }
  
  return {
    insights,
    patterns,
    anomalies,
    summary: insights.length > 0 ? insights[0].value : '未检测到明显模式',
    timestamp: new Date().toISOString()
  }
}

/**
 * 趋势识别
 */
function trend(series) {
  const nums = series.filter(n => typeof n === 'number')
  if (nums.length < 2) {
    return { error: '数据点不足' }
  }
  
  // 简单线性回归
  const n = nums.length
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0
  for (let i = 0; i < n; i++) {
    sumX += i
    sumY += nums[i]
    sumXY += i * nums[i]
    sumX2 += i * i
  }
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX)
  const avg = sumY / n
  
  let direction = 'stable'
  if (slope > avg * 0.05) direction = 'ascending'
  else if (slope < -avg * 0.05) direction = 'descending'
  
  const changeRate = ((nums[n - 1] - nums[0]) / nums[0] * 100).toFixed(2)
  const lastValue = nums[n - 1]
  const forecast = lastValue + slope * 2
  
  return {
    direction,
    changeRate: `${changeRate}%`,
    slope: slope.toFixed(4),
    forecast: forecast.toFixed(2),
    confidence: Math.min(0.95, 0.7 + Math.abs(slope) / avg)
  }
}

/**
 * 对比分析
 */
function compare(items) {
  if (!Array.isArray(items) || items.length < 2) {
    return { error: '需要至少2个对比项' }
  }
  
  const similarities = []
  const differences = []
  
  // 简单对比逻辑
  if (typeof items[0] === 'string' && typeof items[1] === 'string') {
    const [a, b] = items
    const setA = new Set(a.split(''))
    const setB = new Set(b.split(''))
    const intersection = [...setA].filter(c => setB.has(c))
    const union = [...new Set([...a, ...b])]
    
    const jaccard = intersection.length / union.length
    if (jaccard > 0.3) {
      similarities.push(`字符重叠度 ${(jaccard * 100).toFixed(1)}%`)
    }
    if (a.length !== b.length) {
      differences.push(`长度不同: ${a.length} vs ${b.length}`)
    }
  }
  
  return {
    items: items.length,
    similarities,
    differences,
    recommendation: similarities.length > differences.length ? '相似度高' : '差异明显',
    timestamp: new Date().toISOString()
  }
}

// CLI
const args = process.argv.slice(2)
const command = args[0]

if (command === 'analyze') {
  const data = JSON.parse(args.slice(1).join(' '))
  console.log(JSON.stringify(analyze(data), null, 2))
} else if (command === 'trend') {
  const series = JSON.parse(args.slice(1).join(' '))
  console.log(JSON.stringify(trend(series), null, 2))
} else if (command === 'compare') {
  const items = JSON.parse(args.slice(1).join(' '))
  console.log(JSON.stringify(compare(items), null, 2))
} else {
  console.log('Usage: node index.js <analyze|trend|compare> [json_data]')
}

module.exports = { analyze, trend, compare }
