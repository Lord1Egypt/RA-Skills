/**
 * 异步流式任务执行器
 * 
 * 实现真正的 AsyncGenerator 流式输出
 * 用于贫道的流式任务处理
 */

/**
 * 模拟一个流式写作任务
 * 
 * @param {Object} params
 * @param {string} params.topic - 写作主题
 * @param {number} params.length - 目标字数
 * @param {AbortSignal} params.signal - 中断信号
 */
async function* streamingWrite(params) {
  const { topic, length = 500, signal } = params
  
  let written = 0
  const startTime = Date.now()
  
  // 输出开始信息
  yield {
    type: 'text',
    content: `✍️ 开始撰写关于「${topic}」的文章...\n\n`,
    progress: 0,
  }
  
  // 模拟段落内容
  const paragraphs = [
    `在当今数字化时代，${topic}已经成为一个重要的发展趋势。`,
    `从技术演进的角度来看，这一领域正在经历快速的创新和突破。`,
    `首先，核心技术的突破为整个行业带来了新的可能性。`,
    `其次，市场需求的多元化推动了产品和服务的持续升级。`,
    `此外，生态系统的完善也为长期发展奠定了坚实基础。`,
    `展望未来，我们期待看到更多创新应用的涌现。`,
    `总的来说，这是一个充满机遇和挑战的重要领域。`,
  ]
  
  for (const paragraph of paragraphs) {
    // 检查中断
    if (signal?.aborted) {
      yield {
        type: 'error',
        content: '任务已被取消',
      }
      return
    }
    
    // 逐字输出
    for (const char of paragraph) {
      written++
      
      yield {
        type: 'text',
        content: char,
        progress: Math.min(99, Math.round((written / length) * 100)),
        written,
      }
      
      // 模拟打字延迟（15-30ms随机）
      await sleep(Math.random() * 15 + 15)
    }
    
    // 段落结束
    yield { type: 'text', content: '\n\n', progress: Math.min(99, Math.round((written / length) * 100)) }
    
    // 如果已达到目标字数，停止
    if (written >= length) break
  }
  
  // 完成
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)
  yield {
    type: 'done',
    content: `\n\n✅ 文章完成！共 ${written} 字，耗时 ${elapsed}秒`,
    progress: 100,
    written,
    elapsed: parseFloat(elapsed),
  }
}

/**
 * 模拟一个流式搜索任务
 */
async function* streamingSearch(params) {
  const { query, signal } = params
  
  yield {
    type: 'text',
    content: `🔍 正在搜索: "${query}"...\n\n`,
  }
  
  // 模拟搜索结果
  const fakeResults = [
    { title: 'OpenAI ChatGPT', url: 'https://chat.openai.com', desc: 'AI 对话助手' },
    { title: 'Anthropic Claude', url: 'https://claude.ai', desc: 'AI 助手' },
    { title: 'GitHub Copilot', url: 'https://github.com/features/copilot', desc: 'AI 代码补全' },
    { title: 'Midjourney', url: 'https://midjourney.com', desc: 'AI 图像生成' },
    { title: 'Stable Diffusion', url: 'https://stability.ai', desc: '开源 AI 图像生成' },
  ]
  
  for (let i = 0; i < fakeResults.length; i++) {
    if (signal?.aborted) {
      yield { type: 'error', content: '搜索已被取消' }
      return
    }
    
    // 模拟搜索延迟
    await sleep(400)
    
    const result = fakeResults[i]
    yield {
      type: 'result',
      content: undefined,
      result: {
        index: i + 1,
        ...result,
      },
      progress: Math.round(((i + 1) / fakeResults.length) * 100),
    }
  }
  
  yield {
    type: 'done',
    content: `\n✅ 搜索完成，找到 ${fakeResults.length} 个结果`,
    progress: 100,
  }
}

/**
 * 模拟一个流式数据处理任务
 */
async function* streamingProcess(params) {
  const { dataType, rows = 100, signal } = params
  
  yield {
    type: 'text',
    content: `📊 开始处理 ${dataType} 数据，共 ${rows} 行...\n\n`,
  }
  
  const processed = []
  
  for (let i = 0; i < rows; i++) {
    if (signal?.aborted) {
      yield { type: 'error', content: '处理已被取消' }
      return
    }
    
    // 模拟处理延迟
    await sleep(20)
    
    // 模拟处理结果
    processed.push({
      row: i + 1,
      status: Math.random() > 0.1 ? 'success' : 'failed',
      value: Math.round(Math.random() * 100),
    })
    
    // 每10行输出一次进度
    if ((i + 1) % 10 === 0 || i === rows - 1) {
      const successRate = (processed.filter(p => p.status === 'success').length / processed.length * 100).toFixed(1)
      yield {
        type: 'progress',
        content: `已处理 ${i + 1}/${rows} 行，成功率 ${successRate}%`,
        progress: Math.round(((i + 1) / rows) * 100),
        stats: {
          processed: i + 1,
          total: rows,
          successRate: parseFloat(successRate),
        },
      }
    }
  }
  
  const successCount = processed.filter(p => p.status === 'success').length
  yield {
    type: 'done',
    content: `\n✅ 处理完成！成功 ${successCount}/${rows} 行`,
    progress: 100,
    stats: {
      total: rows,
      success: successCount,
      failed: rows - successCount,
    },
  }
}

// ============================================================
// 辅助函数
// ============================================================

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

// ============================================================
// CLI 入口
// ============================================================

const args = process.argv.slice(2)
const command = args[0]
const params = JSON.parse(args.slice(1).join(' ') || '{}')

async function main() {
  let stream
  
  switch (command) {
    case 'write':
      stream = streamingWrite({ ...params, signal: { aborted: false } })
      break
    case 'search':
      stream = streamingSearch({ ...params, signal: { aborted: false } })
      break
    case 'process':
      stream = streamingProcess({ ...params, signal: { aborted: false } })
      break
    default:
      console.log('用法: node streaming-task.js <write|search|process> [json_params]')
      console.log('示例: node streaming-task.js write \'{"topic":"AI","length":300}\'')
      return
  }
  
  // 流式输出
  for await (const chunk of stream) {
    switch (chunk.type) {
      case 'text':
        process.stdout.write(chunk.content || '')
        break
      case 'result':
        console.log(`\n[${chunk.result.index}] ${chunk.result.title}`)
        console.log(`    ${chunk.result.desc}`)
        console.log(`    ${chunk.result.url}`)
        break
      case 'progress':
        process.stdout.write(`\r${chunk.content} (${chunk.progress}%)`)
        break
      case 'done':
        console.log('\n' + chunk.content)
        break
      case 'error':
        console.error('\n❌ 错误:', chunk.content)
        break
    }
  }
}

main().catch(console.error)

module.exports = {
  streamingWrite,
  streamingSearch,
  streamingProcess,
}
