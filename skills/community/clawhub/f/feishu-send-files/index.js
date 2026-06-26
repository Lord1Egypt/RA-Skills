#!/usr/bin/env node

/**
 * 飞书文件发送统一入口
 * 支持两种触发方式：
 * 1. 机器人触发：通过 skill 调用 run(context)
 * 2. 命令行触发：node index.js --file "/path" 或 node index.js --search "关键词"
 */

const fs = require('fs')
const https = require('https')
const path = require('path')
const os = require('os')

// 基础路径配置
const scriptDir = __dirname
const logDir = path.join(scriptDir, 'logs')
const configPath = path.join(os.homedir(), '.openclaw/openclaw.json')
const workspacePath = path.join(os.homedir(), '.openclaw/workspace')

// 默认用户 ID 从配置中读取，支持多层优先级，不硬编码
function getDefaultOpenId(feishuConfig) {
  const localConfigPath = path.join(workspacePath, 'config.json')
  
  // 优先级 1: 从本地 workspace 配置读取 (最高优先级)
  if (fs.existsSync(localConfigPath)) {
    try {
      const localConfig = JSON.parse(fs.readFileSync(localConfigPath, 'utf8'))
      if (localConfig.defaultRecipient?.id) {
        writeLog(`使用 workspace 本地配置：${localConfig.defaultRecipient.id}`, 'INFO')
        return localConfig.defaultRecipient.id
      }
    } catch (err) {
      writeLog(`读取本地配置失败：${err.message}`, 'WARN')
    }
  }
  
  // 优先级 2: 从飞书配置的 allowFrom 列表中获取 (回退)
  if (feishuConfig?.allowFrom && feishuConfig.allowFrom.length > 0) {
    const defaultId = feishuConfig.allowFrom[0]
    writeLog(`使用全局配置 allowFrom: ${defaultId}`, 'INFO')
    
    // 自动创建本地配置文件，方便后续使用
    if (!fs.existsSync(localConfigPath)) {
      try {
        const autoConfig = {
          defaultRecipient: {
            type: 'open_id',
            id: defaultId,
            note: '自动创建 - 从全局配置读取'
          }
        }
        fs.writeFileSync(localConfigPath, JSON.stringify(autoConfig, null, 2), 'utf8')
        writeLog(`已自动创建配置文件：${localConfigPath}`, 'INFO')
      } catch (err) {
        writeLog(`自动创建配置文件失败：${err.message}`, 'WARN')
      }
    }
    
    return defaultId
  }
  
  // 没有配置，抛出错误提示用户
  throw new Error('未找到默认接收者 ID，请在 workspace/config.json 或 openclaw.json 中配置')
}

// 确保日志目录存在
try {
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true, mode: 0o777 })
  }
} catch (err) {
  console.error('日志目录创建失败:', err.message)
}

// 日志写入
function writeLog(content, level = 'INFO') {
  try {
    const dateStr = new Date().toISOString().split('T')[0]
    const logFile = path.join(logDir, `send-${dateStr}.log`)
    const logTime = new Date().toISOString()
    const logContent = `[${logTime}] [${level}] ${content}\n`
    fs.appendFileSync(logFile, logContent, { encoding: 'utf8', flag: 'a+' })
    console.log(logContent.trim())
  } catch (err) {
    console.error('日志写入失败:', err.message)
  }
}

// 格式化文件大小
function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

// 获取飞书配置
function getFeishuConfig() {
  const configRaw = fs.readFileSync(configPath, 'utf8')
  const config = JSON.parse(configRaw)
  return config.channels?.feishu
}

// 获取 token
function getToken(feishuConfig) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      app_id: feishuConfig.appId,
      app_secret: feishuConfig.appSecret
    })
    const options = {
      hostname: 'open.feishu.cn',
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      timeout: 15000
    }
    const req = https.request(options, (res) => {
      let body = ''
      res.on('data', (chunk) => body += chunk)
      res.on('end', () => {
        try {
          const resObj = JSON.parse(body)
          if (resObj.code === 0 && resObj.tenant_access_token) {
            writeLog('Token 获取成功', 'SUCCESS')
            resolve(resObj.tenant_access_token)
          } else {
            reject(new Error(`Token 获取失败 code:${resObj.code}`))
          }
        } catch (e) {
          reject(e)
        }
      })
    })
    req.on('error', reject)
    req.on('timeout', () => reject(new Error('Token 请求超时')))
    req.write(postData)
    req.end()
  })
}

// 上传文件
function uploadFile(token, filePath, fileName) {
  return new Promise((resolve, reject) => {
    const fileData = fs.readFileSync(filePath)
    const boundary = `----feishu-upload-${Date.now()}`
    const bodyArr = [
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file_type"\r\n\r\nstream\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file_name"\r\n\r\n${fileName}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName}"\r\nContent-Type: application/octet-stream\r\n\r\n`),
      fileData,
      Buffer.from(`\r\n--${boundary}--\r\n`)
    ]
    const formData = Buffer.concat(bodyArr)
    const options = {
      hostname: 'open.feishu.cn',
      path: '/open-apis/im/v1/files',
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`
      },
      timeout: 30000
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', (chunk) => data += chunk)
      res.on('end', () => {
        try {
          const resObj = JSON.parse(data)
          if (resObj.code === 0 && resObj.data?.file_key) {
            writeLog(`文件上传成功 file_key:${resObj.data.file_key}`, 'SUCCESS')
            resolve(resObj.data.file_key)
          } else {
            reject(new Error(`上传失败 code:${resObj.code}`))
          }
        } catch (e) {
          reject(e)
        }
      })
    })
    req.on('error', reject)
    req.on('timeout', () => reject(new Error('文件上传超时')))
    req.write(formData)
    req.end()
  })
}

// 发送文件消息
function sendFileMsg(token, fileKey, receiveId, receiveType) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      receive_id: receiveId,
      content: JSON.stringify({ file_key: fileKey }),
      msg_type: 'file'
    })
    const options = {
      hostname: 'open.feishu.cn',
      path: `/open-apis/im/v1/messages?receive_id_type=${receiveType}`,
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: 20000
    }
    const req = https.request(options, (res) => {
      let body = ''
      res.on('data', (chunk) => body += chunk)
      res.on('end', () => {
        try {
          const resObj = JSON.parse(body)
          if (resObj.code === 0) {
            writeLog('文件发送成功', 'SUCCESS')
            resolve('发送成功')
          } else {
            reject(new Error(`发送失败 code:${resObj.code}`))
          }
        } catch (e) {
          reject(e)
        }
      })
    })
    req.on('error', reject)
    req.on('timeout', () => reject(new Error('发送请求超时')))
    req.write(postData)
    req.end()
  })
}

// 搜索文件
function searchFiles(dir, keywords, extensions, maxDepth = 3) {
  const results = []
  
  function search(currentDir, depth) {
    if (depth > maxDepth) return
    
    try {
      const entries = fs.readdirSync(currentDir, { withFileTypes: true })
      
      for (const entry of entries) {
        if (entry.name.startsWith('.') || entry.name === 'node_modules') continue
        
        const fullPath = path.join(currentDir, entry.name)
        
        if (entry.isDirectory()) {
          search(fullPath, depth + 1)
        } else {
          const nameLower = entry.name.toLowerCase()
          const matchKeyword = !keywords || keywords.length === 0 || keywords.some(kw => nameLower.includes(kw.toLowerCase()))
          const matchExt = !extensions || extensions.length === 0 || extensions.some(ext => nameLower.endsWith('.' + ext.toLowerCase()))
          
          if (matchKeyword && matchExt) {
            const relPath = path.relative(workspacePath, fullPath)
            results.push({
              path: fullPath,
              relativePath: relPath,
              name: entry.name,
              size: entry.size || fs.statSync(fullPath).size
            })
          }
        }
      }
    } catch (err) {
      // 忽略
    }
  }
  
  search(dir, 0)
  return results.slice(0, 20)
}

// 提取文件路径
function extractFilePath(userInput) {
  const text = userInput.trim()
  
  // 匹配绝对路径
  const absPathMatch = text.match(/(\/[^\s]+)/g)
  if (absPathMatch) {
    for (const p of absPathMatch) {
      if (p.startsWith('/') && !p.startsWith('/open-apis') && !p.startsWith('/api') && fs.existsSync(p)) {
        return p
      }
    }
  }
  
  // 匹配 workspace 下的文件
  const fileNameMatch = text.match(/([a-zA-Z0-9_\-\.]+\.(pptx?|docx?|xlsx?|pdf|txt|zip|rar|jpg|png|gif|mp4|mp3))/gi)
  if (fileNameMatch) {
    for (const m of fileNameMatch) {
      const filePath = path.join(workspacePath, m)
      if (fs.existsSync(filePath)) {
        return filePath
      }
    }
  }
  
  return null
}

// 提取搜索关键词
function extractSearchTerms(userInput) {
  const text = userInput.trim()
  
  // 提取扩展名
  const extMatch = text.match(/\.(pptx?|docx?|xlsx?|pdf|txt|zip|rar|jpg|png|gif|mp4|mp3)/gi)
  const extensions = extMatch ? extMatch.map(e => e.replace('.', '')) : []
  
  // 提取中文关键词
  const cnMatch = text.match(/[\u4e00-\u9fa5]+/g)
  const keywords = cnMatch ? cnMatch.filter(k => k.length > 1) : []
  
  return { keywords, extensions }
}

// ==================== 机器人模式 ====================

/**
 * 机器人触发入口
 * @param {Object} context - 机器人上下文
 * @param {Object} context.session - 会话信息
 * @param {Object} context.message - 消息内容
 * @param {Function} context.replyText - 回复方法
 */
async function run(context) {
  writeLog('技能触发成功', 'START')
  try {
    if (!context) {
      const errMsg = '❌ 机器人上下文为空，重启 OpenClaw 重试'
      if (context?.replyText) await context.replyText(errMsg)
      writeLog(errMsg, 'ERROR')
      return
    }
    
    const session = context.session || {}
    const message = context.message || {}
    const { chatId, openId, isGroup } = session
    const userInput = (message.text || '').trim()
    
    writeLog(`会话参数 - 群聊:${isGroup}, 群 ID:${chatId}, 用户 ID:${openId}`, 'INFO')
    
    // 读取飞书配置
    const feishuConfig = getFeishuConfig()
    if (!feishuConfig?.appId || !feishuConfig?.appSecret) {
      await context.replyText('❌ 飞书配置不存在')
      return
    }
    
    const token = await getToken(feishuConfig)
    
    // 尝试直接提取文件路径
    let filePath = extractFilePath(userInput)
    
    if (filePath && fs.existsSync(filePath)) {
      await sendFile(context, token, filePath, isGroup, chatId, openId)
      return
    }
    
    // 尝试模糊搜索
    const { keywords, extensions } = extractSearchTerms(userInput)
    const files = searchFiles(workspacePath, keywords, extensions)
    
    if (files.length === 0) {
      await context.replyText('⚠️ 未找到匹配的文件\n\n请提供文件路径或更具体的文件名')
      return
    }
    
    if (files.length === 1) {
      await context.replyText(`找到 1 个匹配文件：${files[0].name}\n正在发送...`)
      await sendFile(context, token, files[0].path, isGroup, chatId, openId)
      return
    }
    
    // 多个匹配，展示列表
    const fileList = files.map((f, i) => `${i + 1}. ${f.name} (${formatSize(f.size)})`).join('\n')
    const selectPrompt = `找到 ${files.length} 个匹配文件，请选择：\n\n${fileList}\n\n回复数字选择（如：1）或输入多个数字（如：1,2,3）或输入 "all" 发送全部`
    await context.replyText(selectPrompt)
    
    // 存储候选文件
    session.candidateFiles = files
    
  } catch (err) {
    const errMsg = `❌ 执行失败：${err.message}`
    writeLog(errMsg, 'ERROR')
    if (context?.replyText) {
      await context.replyText(errMsg)
    }
  }
}

// 发送文件（机器人模式）
async function sendFile(context, token, filePath, isGroup, chatId, openId) {
  const fileName = path.basename(filePath)
  
  try {
    const fileKey = await uploadFile(token, filePath, fileName)
    
    const receiveId = isGroup ? chatId : openId
    const receiveType = isGroup ? 'chat_id' : 'open_id'
    
    await sendFileMsg(token, fileKey, receiveId, receiveType)
    
    const successMsg = `🎉 发送成功！\n文件名：${fileName}\n发送渠道：${isGroup ? '群聊' : '私聊'}`
    await context.replyText(successMsg)
    writeLog(`全流程完成：${fileName}`, 'FINISH')
  } catch (err) {
    const errMsg = `❌ 发送失败：${err.message}`
    writeLog(errMsg, 'ERROR')
    await context.replyText(errMsg)
  }
}

// 处理选择（机器人多文件选择）
async function handleSelection(context, selection) {
  writeLog(`处理用户选择：${selection}`, 'INFO')
  
  const session = context.session || {}
  const candidateFiles = session.candidateFiles || []
  
  if (candidateFiles.length === 0) {
    await context.replyText('❌ 没有候选文件，请重新发起发送请求')
    return
  }
  
  const feishuConfig = getFeishuConfig()
  const token = await getToken(feishuConfig)
  
  // 解析选择（支持多种格式：数字、多个数字、all）
  let selectedFiles = []
  
  const normalized = selection.trim().toLowerCase()
  
  // 发送所有文件
  if (normalized === 'all' || normalized === '全部') {
    selectedFiles = candidateFiles
  } else {
    // 支持逗号分隔的数字（如 "1,2,3"）或文件名
    const selections = normalized.split(/[,,]/).map(s => s.trim())
    
    for (const sel of selections) {
      // 数字选择
      const num = parseInt(sel)
      if (num >= 1 && num <= candidateFiles.length) {
        selectedFiles.push(candidateFiles[num - 1])
        continue
      }
      
      // 文件名匹配
      const matchedFile = candidateFiles.find(f => 
        f.name.toLowerCase().includes(sel.toLowerCase()) ||
        f.relativePath.toLowerCase().includes(sel.toLowerCase())
      )
      if (matchedFile) {
        selectedFiles.push(matchedFile)
      }
    }
  }
  
  if (selectedFiles.length === 0) {
    await context.replyText(`❌ 未找到匹配的文件，请重新选择`)
    return
  }
  
  // 批量发送
  const totalFiles = selectedFiles.length
  let successCount = 0
  
  await context.replyText(`选择：${selectedFiles.map(f => f.name).join(', ')}\n共 ${totalFiles} 个文件，开始发送...`)
  
  for (const selectedFile of selectedFiles) {
    try {
      const fileKey = await uploadFile(token, selectedFile.path, selectedFile.name)
      await sendFileMsg(token, fileKey, session.isGroup ? session.chatId : session.openId, session.isGroup ? 'chat_id' : 'open_id')
      successCount++
    } catch (err) {
      writeLog(`发送失败 ${selectedFile.name}: ${err.message}`, 'ERROR')
    }
  }
  
  await context.replyText(`✅ 发送完成！成功 ${successCount}/${totalFiles} 个文件`)
  writeLog(`批量发送完成：${successCount}/${totalFiles}`, 'FINISH')
}

// ==================== 命令行模式 ====================

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2)
  const params = { files: [], search: null, to: 'user', toType: 'open_id' }
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file' && args[i + 1]) {
      params.files.push(args[++i])
    } else if (args[i] === '--files' && args[i + 1]) {
      // 支持逗号分隔的多个文件
      params.files = params.files.concat(args[++i].split(',').map(f => f.trim()))
    } else if (args[i] === '--search' && args[i + 1]) {
      params.search = args[++i]
    } else if (args[i] === '--to' && args[i + 1]) {
      params.to = args[++i]
      // 自动判断 toType
      if (params.to.startsWith('chat:')) {
        params.toType = 'chat_id'
        params.to = params.to.replace('chat:', '')
      } else if (params.to.startsWith('open_id:')) {
        params.to = params.to.replace('open_id:', '')
      }
    }
  }
  
  return params
}

// 命令行主函数
async function main() {
  const params = parseArgs()
  writeLog(`命令行启动 - 参数:${JSON.stringify(params)}`, 'START')
  
  const feishuConfig = getFeishuConfig()
  if (!feishuConfig?.appId || !feishuConfig?.appSecret) {
    console.error('❌ 飞书配置不存在')
    process.exit(1)
  }
  
  const token = await getToken(feishuConfig)
  
  // 获取默认接收者 ID（如果没有指定 --to）
  let receiveId = params.to
  let receiveType = params.toType
  
  if (!params.to) {
    receiveId = getDefaultOpenId(feishuConfig)
    receiveType = 'open_id'
  }
  
  writeLog(`发送目标 - ID:${receiveId}, Type:${receiveType}`, 'INFO')
  
  // 搜索文件
  if (params.search) {
    const keywords = params.search.split(' ')
    const files = searchFiles(workspacePath, keywords, [])
    console.log(`找到 ${files.length} 个文件:`)
    files.forEach((f, i) => {
      console.log(`  ${i + 1}. ${f.name} (${formatSize(f.size)})`)
    })
    return
  }
  
  // 发送文件（支持批量）
  if (params.files.length > 0) {
    const validFiles = params.files.filter(f => fs.existsSync(f))
    
    if (validFiles.length === 0) {
      console.error('❌ 没有有效的文件')
      process.exit(1)
    }
    
    console.log(`准备发送 ${validFiles.length} 个文件...`)
    
    for (const filePath of validFiles) {
      const fileName = path.basename(filePath)
      console.log(`\n上传文件：${fileName}...`)
      
      try {
        const fileKey = await uploadFile(token, filePath, fileName)
        console.log(`✅ ${fileName} 上传成功`)
        
        console.log(`发送到 ${receiveType === 'chat_id' ? '群聊' : '用户'}...`)
        const result = await sendFileMsg(token, fileKey, receiveId, receiveType)
        console.log(`✅ ${fileName} 发送成功`)
      } catch (err) {
        console.error(`❌ ${fileName} 发送失败：${err.message}`)
      }
    }
    
    console.log('\n✅ 全部完成！')
    return
  }
  
  console.log('用法:')
  console.log('  node index.js --file "/path/to/file"               # 发送单个文件')
  console.log('  node index.js --file "/path1" --file "/path2"     # 批量发送多个文件')
  console.log('  node index.js --files "/path1,/path2,/path3"      # 批量发送（逗号分隔）')
  console.log('  node index.js --search "关键词"                    # 搜索文件')
}

// 如果是直接运行此脚本
if (require.main === module) {
  main().catch(err => {
    console.error('错误:', err.message)
    process.exit(1)
  })
}

// 导出函数
module.exports = { run, handleSelection }
