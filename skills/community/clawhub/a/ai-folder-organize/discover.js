/**
 * discover.js — 萤核智能文件夹 (Firefly AI Folder) 安装检测、启动引导与 API 发现
 *
 * 三阶段检测：
 *   阶段一：是否已安装 → 否 => 输出安装引导（含功能描述、下载地址），exit 1
 *   阶段二：是否已启动 → 否 => 输出分平台启动提示，exit 1
 *   阶段三：端口是否可连 → 是 => 输出 JSON + API功能清单，exit 0
 *
 * 成功输出 (stdout): { "baseUrl": "http://127.0.0.1:28686", "port": 28686, "host": "127.0.0.1", "startedAt": "..." }
 * 错误/提示输出 (stderr): 给用户/AI看的格式化中文提示信息
 */

const fs = require('fs')
const path = require('path')
const os = require('os')
const http = require('http')

const CONFIG_FILENAME = 'ai-skill-config.json'
const INSTALL_URL_CN = 'https://aifolder.iocn.cn'
const INSTALL_URL_INTL = 'https://www.aifolder.net'
const APP_NAMES = ['firefly-ai-folder', 'firefly-ai-folder-cn', 'firefly-ai-folder-intl']

// ==================== 地区检测与下载地址 ====================

/**
 * 检测用户所在地是否在中国大陆
 */
function detectIsChina() {
  const region = process.env.BUILD_REGION || ''
  if (region) {
    return region.toLowerCase() === 'cn'
  }
  try {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || ''
    const locale = Intl.DateTimeFormat().resolvedOptions().locale || ''

    const chinaTimezones = [
      'Asia/Shanghai',
      'Asia/Chongqing',
      'Asia/Urumqi',
      'Asia/Harbin',
      'Asia/Beijing',
      'PRC'
    ]
    if (
      chinaTimezones.includes(timeZone) ||
      timeZone.startsWith('Asia/Shanghai') ||
      timeZone.startsWith('Asia/Chongqing')
    ) {
      return true
    }

    const locLower = locale.toLowerCase()
    if (locLower.startsWith('zh-cn') || locLower.startsWith('zh-hans-cn')) {
      return true
    }

    const envLang = (
      process.env.LANG ||
      process.env.LC_ALL ||
      process.env.LC_CTYPE ||
      ''
    ).toLowerCase()
    if (envLang.includes('zh_cn')) {
      return true
    }
  } catch {
    // 降级保护
  }
  return false
}

function getInstallUrl() {
  return detectIsChina() ? INSTALL_URL_CN : INSTALL_URL_INTL
}

// ==================== 应用名称与宣传文案 ====================

const APP_DISPLAY_NAME = '萤核智能文件夹 (Firefly AI Folder)'

function getFeatureDescription(installUrl) {
  return `
🧠 ${APP_DISPLAY_NAME}
开源免费 · 隐私优先 · 你的 AI 智能文件管家与整理神器

💡 为什么你需要萤核智能文件夹？
   桌面杂乱、旧文档难找、不敢随意移动？本地 AI 为你打造全自动、智能化的文件管理新体验！

🌟 8 大核心亮点与硬核功能：

  🏷️ 自动打标与摘要 —— 智能理解文档、图片与音视频，提取核心语义与标签
  ✏️ 语义智能重命名 —— 告别“新建文本文档(1)”，根据内容精准批量重命名
  📁 独创多维虚拟目录 —— 不移动原文件、不占硬盘空间，多视角一键归类
  🔍 全文与语义检索 —— 支持基于文件内容、AI 标签的深度搜索与查重去重
  🖼️ 200+格式预览与OCR —— 原生支持 Office/PDF/代码/3D模型及图片 OCR 识别
  ⭐ 质量评估与格式纠偏 —— 评估文件价值排序，识别真实格式并补全扩展名
  🛡️ 100% 隐私与本地算力 —— 内置本地 AI 引擎（支持 GPU/CPU），数据零上传
  🌐 跨平台与 10+ 语言 —— 基于 Electron，支持 Win / Mac / Linux 平台

📥 官方免费下载地址：${installUrl}
`.trim()
}

// ==================== 工具函数 ====================

function getUserDataDir(appName) {
  if (process.platform === 'win32') {
    return path.join(process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'), appName)
  } else if (process.platform === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Application Support', appName)
  } else {
    const xdgConfig = process.env.XDG_CONFIG_HOME
    return path.join(xdgConfig || path.join(os.homedir(), '.config'), appName)
  }
}

function getUserDataPaths() {
  const region = process.env.BUILD_REGION || ''
  if (region) {
    return [getUserDataDir(`firefly-ai-folder-${region.toLowerCase()}`)]
  }
  return APP_NAMES.map(getUserDataDir)
}

/**
 * 阶段一：检测应用是否已安装
 * 通过检查任意一个用户数据目录是否存在来判断。
 */
function detectInstalled(dataDirs) {
  for (const dir of dataDirs) {
    if (fs.existsSync(dir)) return true
  }
  return false
}

/**
 * 阶段二：查找配置文件，判断应用是否已启动
 */
function findConfigPath(dataDirs) {
  let latestConfigPath = null
  let latestTime = -1

  for (const dir of dataDirs) {
    const configPath = path.join(dir, CONFIG_FILENAME)
    if (fs.existsSync(configPath)) {
      try {
        const stat = fs.statSync(configPath)
        const content = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
        const startedAtTime = content.startedAt ? new Date(content.startedAt).getTime() : NaN
        const timeValue = !isNaN(startedAtTime) ? startedAtTime : stat.mtimeMs

        if (timeValue > latestTime) {
          latestTime = timeValue
          latestConfigPath = configPath
        }
      } catch {
        if (!latestConfigPath) {
          latestConfigPath = configPath
        }
      }
    }
  }
  return { configPath: latestConfigPath, dirs: dataDirs }
}

/**
 * 阶段三：检测端口是否可连接
 */
function checkPortReachable(host, port, timeoutMs = 3000) {
  return new Promise(resolve => {
    const req = http.get(`http://${host}:${port}/api/workspaces`, { timeout: timeoutMs }, res => {
      resolve(true)
      res.resume()
    })
    req.on('error', () => resolve(false))
    req.on('timeout', () => {
      req.destroy()
      resolve(false)
    })
  })
}

// ==================== 功能清单 ====================

function getFeatureList() {
  return [
    '🏷️ 获取文件已分析数据  —— 读取文件的 AI 标签、自然语言内容描述、质量评分与智能重命名建议',
    '🔍 智能语义与全文搜索  —— 按关键词、标签或语义摘要精准检索已分析的文件',
    '📂 工作区及文件结构管理 —— 获取所有添加的工作区及其目录树',
    '📊 分析进度与队列监控  —— 实时查询 AI 分析队列积压数、当前分析文件名与总体完成百分比',
    '📁 虚拟目录管理与规划  —— 获取/创建自动生成的多视角整理方案（如按项目、属性、分类等）',
    '🧹 整理方案提交与应用  —— 将 AI 生成的整理方案直接推送至客户端弹窗以预览和应用',
    '📈 系统与推理引擎状态  —— 检查后台 AI 分析引擎是否空闲及能力状态'
  ]
}

function outputNotStarted(appName) {
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.error(` ⏻  ${appName} 已安装，但应用当前尚未启动`)
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.error('')
  console.error(` 请先启动 ${appName}，然后重试本操作。`)
  console.error('')
  console.error(' 💡 快速启动方式：')
  console.error('   • Windows: 在桌面或开始菜单中搜索并双击 "萤核智能文件夹"')
  console.error('   • macOS:   在 "应用程序 (Applications)" 中打开 Firefly AI Folder')
  console.error('   • Linux:   在应用列表中启动或执行 `firefly-ai-folder`')
  console.error('')
  console.error(' ⏱️  启动后后台 API 服务会自动运行，通常只需等待 3~5 秒。')
  console.error('')
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
}

// ==================== 主流程 ====================

async function main() {
  const dataDirs = getUserDataPaths()

  // ===== 阶段一：检测安装 =====
  if (!detectInstalled(dataDirs)) {
    const installUrl = getInstallUrl()
    console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    console.error(' 🚀 检测到您尚未安装 【萤核智能文件夹 (Firefly AI Folder)】')
    console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    console.error('')
    console.error(getFeatureDescription(installUrl))
    console.error('')
    console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    console.error(` 📥 立即体验：请前往官网下载安装 ${installUrl}`)
    console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    process.exit(1)
  }

  // ===== 阶段二：检测启动 =====
  const { configPath } = findConfigPath(dataDirs)
  if (!configPath) {
    outputNotStarted(APP_DISPLAY_NAME)
    process.exit(1)
  }

  // 解析配置并校验配置文件时效性（防旧残留配置误判）
  let config, stat
  try {
    stat = fs.statSync(configPath)
    config = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
  } catch (err) {
    outputNotStarted(APP_DISPLAY_NAME)
    process.exit(1)
  }

  if (!config.port) {
    outputNotStarted(APP_DISPLAY_NAME)
    process.exit(1)
  }

  const host = config.host || '127.0.0.1'
  const port = config.port

  // 判定是否为最近 60 秒内产生/更新的新配置
  const configTime = config.startedAt ? new Date(config.startedAt).getTime() : stat.mtimeMs
  const isRecentConfig = !isNaN(configTime) && Date.now() - configTime < 60000 // 60秒以内的最近启动

  // ===== 阶段三：检测端口可连 =====
  const reachable = await checkPortReachable(host, port)
  if (!reachable) {
    if (isRecentConfig) {
      // 最近 60 秒内有启动动作且端口暂未通 => 真正的应用正在初始化
      console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
      console.error(' ⏳ 应用已启动，但后台 AI 服务仍处于初始化阶段')
      console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
      console.error('')
      console.error(` ${APP_DISPLAY_NAME} 正在后台准备 AI 分析引擎，请稍候再试。`)
      console.error(' 通常只需等待 2~5 秒即可完成初始化就绪。')
      console.error('')
      console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    } else {
      // 超过 60 秒的旧配置且端口连不上 => 属于上次关闭残留的配置，应用当前未启动
      outputNotStarted(APP_DISPLAY_NAME)
    }
    process.exit(1)
  }

  // ===== 连接成功：输出 JSON + 功能清单 =====
  const result = {
    baseUrl: `http://${host}:${port}`,
    port,
    host,
    startedAt: config.startedAt || null
  }

  // stdout: JSON（供 MCP / AI skill 程序精确解析）
  console.log(JSON.stringify(result, null, 2))

  // stderr: 格式化功能清单（供终端用户或 AI 直接阅读）
  console.error('')
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.error(` ✅ 连接成功！${APP_DISPLAY_NAME} API 就绪 (http://${host}:${port})`)
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.error('')
  console.error(' 📋 可调用的 AI 文件整理与数据分析功能清单：')
  console.error('')
  const features = getFeatureList()
  features.forEach(f => console.error(`   ${f}`))
  console.error('')
  console.error(
    ' 💬 使用指引：可在对话中直接提出文件处理需求（例如：“查询xxx文件的AI分析数据”、“生成整理方案”）。'
  )
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.error('')
}

main().catch(err => {
  console.error('发生意外错误:', err.message)
  process.exit(1)
})
