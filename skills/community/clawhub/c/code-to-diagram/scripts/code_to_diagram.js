#!/usr/bin/env node
/**
 * code-to-diagram Skill 渲染脚本
 *
 * 渲染引擎
 * --------
 *   mermaid  使用官方 mermaid (mmdc / Mermaid CLI) 渲染 .mmd → PNG
 *            与 Markdown 预览（GitHub / VS Code 等）使用同一渲染器，样式一致
 *   svg      使用 rsvg-convert 渲染 .svg → .png
 *
 * 用法示例
 * --------
 *   node code_to_diagram.js render \
 *     --file <diagram.mmd> \
 *     --theme tokyo-night \
 *     --output-dir <保存目录>
 */

import fs from 'fs'
import path from 'path'
import os from 'os'
import crypto from 'crypto'
import { execSync, spawnSync } from 'child_process'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// ─── 内置主题（16 个）─────────────────────────────────────────────────────────
// 主题颜色映射为 mermaid themeVariables（theme: 'base'），由官方渲染器应用。

const THEMES = {
  'markdown-preview': {
    bg: '#ffffff',
    fg: '#24292f',
    line: '#d1d9e0',
    accent: '#0969da',
    muted: '#57606a',
    surface: '#f6f8fa',
    border: '#d1d9e0',
  },
  'github-light': {
    bg: '#ffffff',
    fg: '#1f2328',
    line: '#d1d9e0',
    accent: '#0969da',
    muted: '#59636e',
  },
  'github-dark': {
    bg: '#0d1117',
    fg: '#e6edf3',
    line: '#3d444d',
    accent: '#4493f8',
    muted: '#9198a1',
  },
  'tokyo-night': {
    bg: '#1a1b26',
    fg: '#a9b1d6',
    line: '#3d59a1',
    accent: '#7aa2f7',
    muted: '#565f89',
  },
  'tokyo-night-storm': {
    bg: '#24283b',
    fg: '#a9b1d6',
    line: '#3d59a1',
    accent: '#7aa2f7',
    muted: '#565f89',
  },
  'tokyo-night-light': {
    bg: '#d5d6db',
    fg: '#343b58',
    line: '#34548a',
    accent: '#34548a',
    muted: '#9699a3',
  },
  'catppuccin-mocha': {
    bg: '#1e1e2e',
    fg: '#cdd6f4',
    line: '#585b70',
    accent: '#cba6f7',
    muted: '#6c7086',
  },
  'catppuccin-latte': {
    bg: '#eff1f5',
    fg: '#4c4f69',
    line: '#9ca0b0',
    accent: '#8839ef',
    muted: '#9ca0b0',
  },
  'nord': {
    bg: '#2e3440',
    fg: '#d8dee9',
    line: '#4c566a',
    accent: '#88c0d0',
    muted: '#616e88',
  },
  'nord-light': {
    bg: '#eceff4',
    fg: '#2e3440',
    line: '#aab1c0',
    accent: '#5e81ac',
    muted: '#7b88a1',
  },
  'dracula': {
    bg: '#282a36',
    fg: '#f8f8f2',
    line: '#6272a4',
    accent: '#bd93f9',
    muted: '#6272a4',
  },
  'one-dark': {
    bg: '#282c34',
    fg: '#abb2bf',
    line: '#4b5263',
    accent: '#c678dd',
    muted: '#5c6370',
  },
  'solarized-light': {
    bg: '#fdf6e3',
    fg: '#657b83',
    line: '#93a1a1',
    accent: '#268bd2',
    muted: '#93a1a1',
  },
  'solarized-dark': {
    bg: '#002b36',
    fg: '#839496',
    line: '#586e75',
    accent: '#268bd2',
    muted: '#586e75',
  },
  'zinc-light': {
    bg: '#FFFFFF',
    fg: '#27272A',
  },
  'zinc-dark': {
    bg: '#18181B',
    fg: '#FAFAFA',
  },
}

const AVAILABLE_THEMES = Object.keys(THEMES)

// ─── 颜色工具 ─────────────────────────────────────────────────────────────────

function hexToRgb(hex) {
  hex = hex.replace('#', '')
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2]
  return [parseInt(hex.slice(0,2),16), parseInt(hex.slice(2,4),16), parseInt(hex.slice(4,6),16)]
}

function rgbToHex(r, g, b) {
  return '#' + [r,g,b].map(v => Math.round(v).toString(16).padStart(2,'0')).join('')
}

function mixColors(color1, pct1, color2) {
  const [r1,g1,b1] = hexToRgb(color1)
  const [r2,g2,b2] = hexToRgb(color2)
  const p = pct1 / 100
  return rgbToHex(r1*p+r2*(1-p), g1*p+g2*(1-p), b1*p+b2*(1-p))
}

// ─── Mermaid 配置生成（themeVariables 映射）───────────────────────────────────

function buildMermaidConfig(theme, args) {
  const bg = args.transparent ? 'transparent' : (args.bg || theme.bg)
  const fg = theme.fg
  const surface = theme.surface || mixColors(fg, 5, theme.bg)
  const border = theme.border || theme.line || mixColors(fg, 25, theme.bg)
  const line = theme.line || mixColors(fg, 35, theme.bg)
  const accent = theme.accent || fg

  return {
    theme: 'base',
    themeVariables: {
      background: bg,
      primaryColor: surface,
      primaryTextColor: fg,
      primaryBorderColor: border,
      secondaryColor: mixColors(accent, 12, surface),
      tertiaryColor: mixColors(fg, 8, theme.bg),
      lineColor: line,
      textColor: fg,
      titleColor: fg,
      nodeBorder: border,
      clusterBkg: surface,
      clusterBorder: border,
      edgeLabelBackground: bg,
      // 时序图
      actorBkg: surface,
      actorBorder: border,
      actorTextColor: fg,
      actorLineColor: line,
      signalColor: line,
      signalTextColor: fg,
      noteBkgColor: mixColors(accent, 15, surface),
      noteBorderColor: border,
      noteTextColor: fg,
      activationBorderColor: border,
      activationBkgColor: mixColors(fg, 10, surface),
      // 状态图 / 其他
      labelColor: fg,
      loopTextColor: fg,
    },
  }
}

// ─── 缓存机制（SVG 引擎）──────────────────────────────────────────────────────

const CACHE_DIR = path.join(os.tmpdir(), 'code-to-diagram-cache')

function ensureCacheDir() {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true })
  }
}

function generateCacheKey(content, params) {
  const hash = crypto.createHash('md5')
  hash.update(content)
  hash.update(JSON.stringify(params))
  return hash.digest('hex')
}

function getCachePath(cacheKey) {
  return path.join(CACHE_DIR, `${cacheKey}.png`)
}

function checkCache(cacheKey) {
  const cachePath = getCachePath(cacheKey)
  if (fs.existsSync(cachePath)) {
    return cachePath
  }
  return null
}

function saveToCache(cacheKey, pngPath) {
  ensureCacheDir()
  const cachePath = getCachePath(cacheKey)
  fs.copyFileSync(pngPath, cachePath)
  return cachePath
}

// ─── 尺寸自适应（SVG 引擎）────────────────────────────────────────────────────

function estimateDiagramComplexity(svgString) {
  // 统计节点数量（通过常见的 SVG 元素）
  const nodePatterns = [
    /<rect[\s>]/g,      // 矩形节点
    /<circle[\s>]/g,    // 圆形节点
    /<ellipse[\s>]/g,   // 椭圆节点
    /<polygon[\s>]/g,   // 多边形节点
    /<path[\s>]/g,      // 路径节点
    /<text[\s>]/g,      // 文本节点
  ]

  let nodeCount = 0
  for (const pattern of nodePatterns) {
    const matches = svgString.match(pattern)
    if (matches) {
      nodeCount += matches.length
    }
  }

  // 统计连线数量
  const edgePatterns = [
    /<line[\s>]/g,      // 直线
    /<polyline[\s>]/g,  // 折线
  ]

  let edgeCount = 0
  for (const pattern of edgePatterns) {
    const matches = svgString.match(pattern)
    if (matches) {
      edgeCount += matches.length
    }
  }

  return { nodeCount, edgeCount, totalElements: nodeCount + edgeCount }
}

function calculateAdaptiveScale(complexity, baseWidth) {
  const { totalElements } = complexity

  // 根据元素数量确定缩放因子
  // 简单图表 (< 15 元素): 8倍放大
  // 中等图表 (15-40 元素): 12倍放大
  // 复杂图表 (> 40 元素): 16倍放大
  let scale
  if (totalElements < 15) {
    scale = 8
  } else if (totalElements < 40) {
    scale = 12
  } else {
    scale = 16
  }

  // 计算输出宽度，确保在合理范围内
  const outputWidth = Math.max(1200, Math.min(4800, Math.round(baseWidth * scale)))

  return { scale, outputWidth }
}

// ─── 工具函数 ─────────────────────────────────────────────────────────────────

function resolveMmdc() {
  try {
    const p = execSync('which mmdc', { encoding: 'utf8' }).trim()
    if (p) return p
  } catch (_) {}

  const local = path.resolve(__dirname, 'node_modules', '.bin', 'mmdc')
  if (fs.existsSync(local)) return local

  try {
    const prefix = execSync('npm prefix -g', { encoding: 'utf8' }).trim()
    const p = path.join(prefix, 'bin', 'mmdc')
    if (fs.existsSync(p)) return p
  } catch (_) {}

  return null
}

function writePuppeteerConfig() {
  const cfg = { args: ['--no-sandbox', '--disable-setuid-sandbox'] }
  const ts = Date.now()
  const file = path.join(os.tmpdir(), `code_to_diagram_puppeteer_${ts}.json`)
  fs.writeFileSync(file, JSON.stringify(cfg))
  return file
}

function writeChineseFontCss(font) {
  const fontFamily = font
    ? `${font}, 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'Hiragino Sans GB', 'WenQuanYi Micro Hei', 'Inter', -apple-system, system-ui, sans-serif`
    : `'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'Hiragino Sans GB', 'WenQuanYi Micro Hei', 'Inter', -apple-system, system-ui, sans-serif`
  const css = `text, .label, .edgeLabel, .nodeLabel, .cluster-label {
  font-family: ${fontFamily} !important;
}`
  const ts = Date.now()
  const file = path.join(os.tmpdir(), `code_to_diagram_chinese_font_${ts}.css`)
  fs.writeFileSync(file, css, 'utf-8')
  return file
}

function resolveRsvgConvert() {
  try {
    const p = execSync('which rsvg-convert', { encoding: 'utf8' }).trim()
    if (p) return p
  } catch (_) {}

  const candidates = [
    '/opt/homebrew/bin/rsvg-convert',
    '/usr/local/bin/rsvg-convert',
    '/usr/bin/rsvg-convert',
  ]
  for (const c of candidates) {
    if (fs.existsSync(c)) return c
  }
  return null
}

function validateSvg(svgPath) {
  const scriptPath = path.join(__dirname, 'validate_svg.sh')
  if (!fs.existsSync(scriptPath)) return true
  const result = spawnSync('bash', [scriptPath, svgPath], { stdio: 'inherit' })
  return result.status === 0
}

// ─── 参数解析 ─────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {
    command:     null,
    content:     null,
    file:        null,
    name:        'diagram',
    outputDir:   null,
    theme:       'markdown-preview',
    transparent: false,
    width:       2400,
    height:      4000,
    scale:       3,
    bg:          null,
    engine:      'mermaid',
    style:       'flat-icon',
    svgWidth:    1920,
    font:        null,
    noCache:     false,
    noPng:       false,
  }

  let i = 2
  if (argv.length > i && !argv[i].startsWith('-')) {
    args.command = argv[i++]
  }

  while (i < argv.length) {
    const flag = argv[i]
    switch (flag) {
      case '--content':    case '-c': args.content     = argv[++i]; break
      case '--file':       case '-f': args.file         = argv[++i]; break
      case '--name':       case '-n': args.name         = argv[++i]; break
      case '--output-dir': case '-o': args.outputDir    = argv[++i]; break
      case '--theme':      case '-t': args.theme        = argv[++i]; break
      case '--transparent':           args.transparent  = true; break
      case '--width':      case '-W': args.width        = parseInt(argv[++i], 10); break
      case '--height':     case '-H': args.height       = parseInt(argv[++i], 10); break
      case '--scale':      case '-s': args.scale        = parseFloat(argv[++i]);   break
      case '--bg':         case '-b': args.bg           = argv[++i]; break
      case '--engine':     case '-e': args.engine       = argv[++i]; break
      case '--style':                 args.style        = argv[++i]; break
      case '--svg-width':             args.svgWidth     = parseInt(argv[++i], 10); break
      case '--font':                  args.font         = argv[++i]; break
      case '--no-cache':              args.noCache      = true; break
      case '--no-png':                args.noPng        = true; break
      case '--renderer':
        i++
        console.warn('⚠️  --renderer 已废弃：Mermaid 引擎固定使用官方渲染器 (mmdc)，该参数被忽略。')
        break
      case '--padding':
        i++
        console.warn('⚠️  --padding 已废弃：官方渲染器 (mmdc) 不支持该参数，已被忽略。')
        break
      case '--help':       case '-h': args.command      = 'help'; break
      default:
        console.error(`未知参数：${flag}`)
        process.exit(1)
    }
    i++
  }
  return args
}

// ─── SVG → PNG（SVG 引擎，rsvg-convert）───────────────────────────────────────

function svgToPng(svgString, pngPath, width, enableCache = true) {
  const rsvg = resolveRsvgConvert()
  if (!rsvg) {
    console.error('❌  未找到 rsvg-convert。请安装 librsvg：')
    console.error('    macOS:         brew install librsvg')
    console.error('    Debian/Ubuntu: apt-get install librsvg2-bin')
    process.exit(1)
  }

  // 缓存检查
  if (enableCache) {
    const complexity = estimateDiagramComplexity(svgString)
    const viewBoxMatch = svgString.match(/viewBox="([^"]+)"/)
    let baseWidth = 300
    if (viewBoxMatch) {
      [, , baseWidth] = viewBoxMatch[1].split(/\s+/).map(Number)
    }
    const { scale, outputWidth: adaptiveWidth } = calculateAdaptiveScale(complexity, baseWidth)
    const finalWidth = width || adaptiveWidth

    const cacheKey = generateCacheKey(svgString, { width: finalWidth, scale })
    const cachedPath = checkCache(cacheKey)
    if (cachedPath) {
      console.log(`⚡  命中缓存，跳过渲染`)
      fs.copyFileSync(cachedPath, pngPath)
      return
    }
  }

  const tmpSvg = path.join(os.tmpdir(), `bm_${Date.now()}.svg`)
  fs.writeFileSync(tmpSvg, svgString, 'utf-8')

  const viewBoxMatch = svgString.match(/viewBox="([^"]+)"/)
  let outputWidth = width || 2400
  let scaleInfo = ''

  if (viewBoxMatch) {
    const [, , vbWidth] = viewBoxMatch[1].split(/\s+/).map(Number)
    const complexity = estimateDiagramComplexity(svgString)
    const { scale, outputWidth: adaptiveWidth } = calculateAdaptiveScale(complexity, vbWidth)
    outputWidth = width || adaptiveWidth
    scaleInfo = ` (元素: ${complexity.totalElements}, 缩放: ${scale}x)`
  }

  const rsvgArgs = ['-w', String(outputWidth), tmpSvg, '-o', pngPath]
  console.log(`    rsvg-convert -w ${outputWidth} → ${pngPath}${scaleInfo}`)

  const result = spawnSync(rsvg, rsvgArgs, { stdio: 'inherit' })

  try { fs.unlinkSync(tmpSvg) } catch (_) {}

  if (result.status !== 0) {
    console.error(`❌  rsvg-convert 退出码：${result.status}`)
    process.exit(result.status ?? 1)
  }

  if (enableCache) {
    const complexity = estimateDiagramComplexity(svgString)
    const cacheKey = generateCacheKey(svgString, { width: outputWidth, scale: complexity.totalElements < 15 ? 8 : complexity.totalElements < 40 ? 12 : 16 })
    saveToCache(cacheKey, pngPath)
    console.log(`💾  已保存到缓存`)
  }
}

// ─── mmdc 渲染（官方 mermaid）─────────────────────────────────────────────────

function renderWithMmdc(inputMmdPath, pngPath, args) {
  let mmdc = resolveMmdc()
  let useNpx = false
  if (!mmdc) {
    console.log('⚙️  未直接找到 mmdc，将通过 npx 调用 @mermaid-js/mermaid-cli …')
    useNpx = true
  } else {
    console.log(`🔧  使用官方渲染器 mmdc：${mmdc}`)
  }

  const theme = THEMES[args.theme]
  if (!theme) {
    console.error(`❌  未知主题：${args.theme}`)
    console.error(`    可用主题：${AVAILABLE_THEMES.join(', ')}`)
    process.exit(1)
  }

  // 主题颜色 → mermaid themeVariables（theme: 'base'），由官方渲染器应用
  const mermaidConfig = buildMermaidConfig(theme, args)
  const configFile = path.join(os.tmpdir(), `code_to_diagram_mermaid_config_${Date.now()}.json`)
  fs.writeFileSync(configFile, JSON.stringify(mermaidConfig, null, 2))
  console.log(`🎨  主题：${args.theme}（themeVariables 映射）`)

  const puppeteerCfg = writePuppeteerConfig()
  const chineseFontCss = writeChineseFontCss(args.font)
  const bgColor = args.transparent ? 'transparent' : (args.bg || theme.bg)

  const mmdcArgs = [
    ...(useNpx ? ['mmdc'] : []),
    '-i', inputMmdPath,
    '-o', pngPath,
    '-c', configFile,
    '-b', bgColor,
    '-w', String(args.width),
    '-H', String(args.height),
    '-s', String(args.scale),
    '-p', puppeteerCfg,
    '-C', chineseFontCss,
  ]

  const cmd = useNpx ? 'npx' : mmdc
  console.log(`🎨  正在使用官方 mermaid 渲染 PNG …`)

  const result = spawnSync(cmd, mmdcArgs, { stdio: 'inherit', shell: false })

  try { fs.unlinkSync(puppeteerCfg) } catch (_) {}
  try { fs.unlinkSync(chineseFontCss) } catch (_) {}
  try { fs.unlinkSync(configFile) } catch (_) {}

  if (result.status !== 0) {
    console.error(`❌  mmdc 退出码：${result.status}`)
    process.exit(result.status ?? 1)
  }
}

// ─── 子命令实现 ───────────────────────────────────────────────────────────────

function printHelp() {
  console.log(`
code-to-diagram Skill —— 从代码分析结果生成 PNG 图片

渲染引擎：
  mermaid  使用官方 mermaid (mmdc) 渲染 .mmd → PNG（默认）
           与 Markdown 预览使用同一渲染器，样式一致
  svg      使用 rsvg-convert 渲染 .svg → .png

用法：
  node code_to_diagram.js render [选项]

通用选项：
  --file,       -f  <路径>      输入文件路径（.mmd 或 .svg）
  --content,    -c  <字符串>    Mermaid 源码（仅 mermaid 引擎，与 --file 二选一）
  --name,       -n  <字符串>    输出文件基础名（默认：diagram）
  --output-dir, -o  <路径>      输出目录（默认：当前工作目录）
  --engine,     -e  <引擎>      mermaid | svg（默认：mermaid）
  --no-cache                    禁用缓存，强制重新渲染（仅 SVG 引擎）
  --no-png                      只生成 Markdown 文档，不生成 PNG 图片（仅 mermaid 引擎）
  --help,       -h              显示帮助信息

Mermaid 引擎选项（官方 mmdc 渲染）：
  --theme,      -t  <主题>      ${AVAILABLE_THEMES.join(' | ')}
                                （默认：markdown-preview，映射为 themeVariables）
  --transparent                 透明背景
  --bg,         -b  <颜色>      自定义背景色（覆盖主题）
  --font        <字体>          自定义字体（默认：系统中文字体）
  --width,      -W  <像素>      画布宽度（默认：2400）
  --height,     -H  <像素>      画布高度（默认：4000）
  --scale,      -s  <倍数>      缩放系数（默认：3）

SVG 引擎选项：
  --style       <风格>          flat-icon | dark-terminal | blueprint | notion-clean | glassmorphism
  --svg-width   <像素>          输出宽度（默认：1920）

可用主题（16 个）：
  暗色：github-dark, tokyo-night, tokyo-night-storm, catppuccin-mocha,
        nord, dracula, one-dark, solarized-dark, zinc-dark
  亮色：github-light, tokyo-night-light, catppuccin-latte,
        nord-light, solarized-light, zinc-light, markdown-preview

示例：
  # 官方 mermaid 渲染（默认）
  node code_to_diagram.js render -f diagram.mmd -t tokyo-night -o ./output

  # 透明背景
  node code_to_diagram.js render -f diagram.mmd --transparent -o ./output

  # SVG 引擎
  node code_to_diagram.js render -e svg -f arch.svg --style dark-terminal -o ./output

  # 只生成 Markdown 文档，不生成 PNG 图片
  node code_to_diagram.js render -f diagram.mmd --no-png -o ./output

特性说明：
  - 官方渲染：PNG 与 GitHub / VS Code 等 Markdown 预览使用同一 mermaid 渲染器
  - 主题映射：16 个主题通过 themeVariables 应用，曲线等 init 配置原生支持
  - SVG 引擎：根据图表元素数量自动调整输出尺寸（8x / 12x / 16x），结果自动缓存
  - 缓存位置：系统临时目录下的 code-to-diagram-cache 文件夹
  - 渲染完成后自动删除输入的 .mmd 中间文件，只保留 .md 和 .png

注意：此脚本仅生成 PNG 图片。Markdown 文档（包含代码逻辑解释和图表源码）由 Claude 生成。
`)
}

function removeIntermediateMmd(inputMmdPath, cleanupMmd, args) {
  if (!inputMmdPath) return
  let removed = false
  if (cleanupMmd) {
    try { fs.unlinkSync(inputMmdPath); removed = true } catch (_) {}
  } else if (args.file && inputMmdPath.endsWith('.mmd')) {
    try { fs.unlinkSync(inputMmdPath); removed = true } catch (_) {}
  }
  if (removed) {
    console.log(`🧹  已删除中间文件：${inputMmdPath}`)
  }
}

async function cmdRender(args) {
  const outputDir = args.outputDir ? path.resolve(args.outputDir) : process.cwd()
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true })
  }

  // 获取 Mermaid 源码
  let mmdContent
  let inputMmdPath
  let cleanupMmd = false

  if (args.file) {
    const src = path.resolve(args.file)
    if (!fs.existsSync(src)) {
      console.error(`❌  文件不存在：${src}`)
      process.exit(1)
    }
    mmdContent = fs.readFileSync(src, 'utf-8')
    inputMmdPath = src
  } else if (args.content) {
    mmdContent = args.content.replace(/\\n/g, '\n')
    inputMmdPath = path.join(os.tmpdir(), `code_to_diagram_${Date.now()}.mmd`)
    fs.writeFileSync(inputMmdPath, mmdContent, 'utf-8')
    cleanupMmd = true
  } else {
    console.error('❌  --content 或 --file 必须提供其中一个。')
    process.exit(1)
  }

  const pngPath = path.join(outputDir, `${args.name}.png`)

  // --no-png：只生成 Markdown 文档，跳过图片渲染
  if (args.noPng) {
    removeIntermediateMmd(inputMmdPath, cleanupMmd, args)

    const mdPath = path.join(outputDir, `${args.name}.md`)
    const mdFileContent = '```mermaid\n' + mmdContent.trim() + '\n```\n'
    fs.writeFileSync(mdPath, mdFileContent, 'utf-8')
    console.log(`✅  Markdown 文档已保存：${mdPath}（--no-png，未生成图片）`)

    console.log(JSON.stringify({ md: mdPath, png: null, engine: 'mermaid', theme: args.theme, renderer: 'mmdc' }))
    return 0
  }

  // 官方 mermaid (mmdc) 渲染
  renderWithMmdc(inputMmdPath, pngPath, args)

  removeIntermediateMmd(inputMmdPath, cleanupMmd, args)

  if (!fs.existsSync(pngPath)) {
    console.error('❌  渲染完成但未找到 PNG 文件。')
    process.exit(1)
  }

  const { size } = fs.statSync(pngPath)
  const kb = (size / 1024).toFixed(1)
  console.log(`✅  PNG 渲染完成：${pngPath}（${kb} KB）`)

  // 生成基础 Markdown 文档（仅包含图表源码）
  const mdPath = path.join(outputDir, `${args.name}.md`)
  const mdFileContent = '```mermaid\n' + mmdContent.trim() + '\n```\n'
  fs.writeFileSync(mdPath, mdFileContent, 'utf-8')
  console.log(`✅  Markdown 文档已保存：${mdPath}`)

  console.log(JSON.stringify({ md: mdPath, png: pngPath, engine: 'mermaid', theme: args.theme, renderer: 'mmdc' }))

  return 0
}

async function cmdRenderSvg(args) {
  const outputDir = args.outputDir ? path.resolve(args.outputDir) : process.cwd()
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true })
  }

  if (!args.file) {
    console.error('❌  SVG 引擎必须使用 --file 指定 .svg 文件路径。')
    process.exit(1)
  }

  const svgPath = path.resolve(args.file)
  if (!fs.existsSync(svgPath)) {
    console.error(`❌  文件不存在：${svgPath}`)
    process.exit(1)
  }

  const svgContent = fs.readFileSync(svgPath, 'utf-8')
  console.log(`📄  已加载 SVG 文件：${svgPath}`)

  console.log('🔍  正在验证 SVG …')
  if (!validateSvg(svgPath)) {
    console.error('❌  SVG 验证失败，请检查上方错误信息。')
    process.exit(1)
  }

  const pngPath = path.join(outputDir, `${args.name}.png`)
  svgToPng(svgContent, pngPath, null, !args.noCache)

  if (!fs.existsSync(pngPath)) {
    console.error('❌  渲染完成但未找到 PNG 文件。')
    process.exit(1)
  }

  const { size } = fs.statSync(pngPath)
  const kb = (size / 1024).toFixed(1)
  console.log(`✅  PNG 渲染完成：${pngPath}（${kb} KB）`)

  // 生成基础 Markdown 文档（仅包含图表源码）
  const mdPath = path.join(outputDir, `${args.name}.md`)
  const mdFileContent = '```svg\n' + svgContent.trim() + '\n```\n'
  fs.writeFileSync(mdPath, mdFileContent, 'utf-8')
  console.log(`✅  Markdown 文档已保存：${mdPath}`)

  console.log(JSON.stringify({ md: mdPath, png: pngPath, engine: 'svg', style: args.style }))

  return 0
}

// ─── 程序入口 ─────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv)

  if (!args.command || args.command === 'help') {
    printHelp()
    process.exit(args.command === 'help' ? 0 : 1)
  }

  let exitCode = 1
  switch (args.command) {
    case 'render':
      if (args.engine === 'svg') {
        exitCode = await cmdRenderSvg(args)
      } else if (args.engine === 'mermaid') {
        exitCode = await cmdRender(args)
      } else {
        console.error(`❌  未知引擎：${args.engine}，可选值：mermaid | svg`)
        exitCode = 1
      }
      break
    default:
      console.error(`未知子命令：${args.command}`)
      printHelp()
      exitCode = 1
  }

  process.exit(exitCode)
}

main()
