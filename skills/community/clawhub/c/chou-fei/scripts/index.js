/**
 * 臭肺·吐纳魄 - 资源获取与信息摄取
 */

const https = require('https')
const http = require('http')

/**
 * 资源获取
 */
function fetch(resource) {
  const { type, location, format } = resource
  let content = ''
  let success = false
  let cached = false
  let size = 0
  
  if (type === 'url' && location) {
    try {
      const urlObj = new URL(location)
      const client = urlObj.protocol === 'https:' ? https : http
      
      // 简化实现，实际使用需要完整HTTP请求
      content = `[模拟获取] URL: ${location}`
      success = true
      size = content.length
    } catch (e) {
      content = ''
      success = false
    }
  } else if (type === 'text' || !type) {
    // 模拟文本内容
    content = location || ''
    success = true
    size = content.length
  }
  
  return {
    content: success ? content.substring(0, 500) : '',
    size,
    format: format || 'text',
    cached,
    success,
    timestamp: new Date().toISOString()
  }
}

/**
 * 信息摄取
 */
function absorb(content) {
  if (!content || typeof content !== 'string') {
    return { error: '内容为空' }
  }
  
  // 提取摘要
  const sentences = content.split(/[.!?。！？]+/).filter(s => s.trim())
  const summary = sentences.slice(0, 2).join('。') + '。'
  
  // 提取关键点（简单实现）
  const keyPoints = []
  const lines = content.split('\n').filter(l => l.trim())
  
  lines.slice(0, 5).forEach((line, i) => {
    if (line.length > 10 && line.length < 200) {
      keyPoints.push({
        index: i + 1,
        text: line.trim().substring(0, 100)
      })
    }
  })
  
  // 实体识别（简单实现）
  const entities = {
    numbers: (content.match(/\d+\.?\d*/g) || []).slice(0, 5),
    urls: (content.match(/https?:\/\/[^\s]+/g) || []),
    emails: (content.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g) || [])
  }
  
  // 相关性评分（模拟）
  const relevance = Math.round((0.6 + Math.random() * 0.4) * 100) / 100
  
  return {
    summary: summary.substring(0, 200) || '无法提取摘要',
    keyPoints,
    entities,
    relevance,
    stats: {
      charCount: content.length,
      sentenceCount: sentences.length,
      lineCount: lines.length
    },
    timestamp: new Date().toISOString()
  }
}

/**
 * 算力调度
 */
function allocate(request) {
  const { task, priority, estimatedLoad } = request
  const os = require('os')
  
  // 模拟算力分配
  const cpuCount = os.cpus().length
  const cpuUsage = os.loadavg()[0] / cpuCount
  
  let allocated = 'balanced'
  let queuePosition = 0
  let estimatedTime = '即时'
  
  if (task === 'training' || task === 'inference') {
    if (cpuUsage > 0.8) {
      allocated = 'queued'
      queuePosition = Math.floor(cpuUsage * 5)
      estimatedTime = `${queuePosition * 5}秒`
    } else {
      allocated = 'dedicated'
      estimatedTime = '即时'
    }
  }
  
  if (priority === 'high') {
    allocated = 'dedicated'
    queuePosition = 0
    estimatedTime = '即时'
  }
  
  return {
    task: task || 'general',
    request: {
      priority: priority || 'normal',
      estimatedLoad: estimatedLoad || 'medium'
    },
    allocation: {
      mode: allocated,
      queuePosition,
      estimatedTime
    },
    system: {
      availableCores: cpuCount,
      currentLoad: cpuUsage.toFixed(2)
    },
    timestamp: new Date().toISOString()
  }
}

// CLI
const args = process.argv.slice(2)
const command = args[0]

if (command === 'fetch') {
  const resource = JSON.parse(args.slice(1).join(' '))
  console.log(JSON.stringify(fetch(resource), null, 2))
} else if (command === 'absorb') {
  console.log(JSON.stringify(absorb(args.slice(1).join(' ')), null, 2))
} else if (command === 'allocate') {
  const request = JSON.parse(args.slice(1).join(' '))
  console.log(JSON.stringify(allocate(request), null, 2))
} else {
  console.log('Usage: node index.js <fetch|absorb|allocate> [json_args]')
}

module.exports = { fetch, absorb, allocate }
