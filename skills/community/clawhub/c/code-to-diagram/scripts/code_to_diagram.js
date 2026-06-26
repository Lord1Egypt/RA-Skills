#!/usr/bin/env node
/**
 * code-to-diagram Skill 渲染脚本
 *
 * 渲染引擎
 * --------
 *   mermaid  默认使用 beautiful-mermaid → SVG → rsvg-convert → PNG
 *            不支持的图表类型自动回退到 mmdc (Mermaid CLI)
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

// Dynamic import to resolve from script's own directory
const { renderMermaidSVG, THEMES } = await import('beautiful-mermaid')

// ─── 自定义主题 ─────────────────────────────────────────────────────────────

// 添加自定义主题：markdown-preview（浅色背景，简洁线条，系统字体）
THEMES['markdown-preview'] = {
  bg: '#ffffff',
  fg: '#24292f',
  line: '#d1d9e0',
  accent: '#0969da',
  muted: '#57606a',
  surface: '#f6f8fa',
  border: '#d1d9e0',
}

// ─── 常量 ─────────────────────────────────────────────────────────────────────

const BM_SUPPORTED_PREFIXES = [
  'graph', 'flowchart', 'statediagram', 'sequencediagram',
  'classdiagram', 'erdiagram', 'xychart',
]

// ─── 曲线插值算法 ─────────────────────────────────────────────────────────────

function pointsToCurvePath(points, curveType = 'basis') {
  if (points.length < 2) return ''
  
  switch (curveType) {
    case 'basis':
      return basisCurve(points)
    case 'monotoneX':
      return monotoneXCurve(points)
    case 'monotoneY':
      return monotoneYCurve(points)
    case 'stepBefore':
      return stepBeforeCurve(points)
    case 'stepAfter':
      return stepAfterCurve(points)
    default:
      return basisCurve(points)
  }
}

function basisCurve(points) {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const p0 = points[Math.max(0, i - 1)]
    const p1 = points[i]
    const p2 = points[i + 1]
    const p3 = points[Math.min(n - 1, i + 2)]
    
    const cp1x = p1.x + (p2.x - p0.x) / 6
    const cp1y = p1.y + (p2.y - p0.y) / 6
    const cp2x = p2.x - (p3.x - p1.x) / 6
    const cp2y = p2.y - (p3.y - p1.y) / 6
    
    path += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${p2.x},${p2.y}`
  }
  
  return path
}

function monotoneXCurve(points) {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  const tangents = []
  for (let i = 0; i < n; i++) {
    if (i === 0) {
      tangents.push((points[1].y - points[0].y) / (points[1].x - points[0].x))
    } else if (i === n - 1) {
      tangents.push((points[n - 1].y - points[n - 2].y) / (points[n - 1].x - points[n - 2].x))
    } else {
      const d0 = (points[i].y - points[i - 1].y) / (points[i].x - points[i - 1].x)
      const d1 = (points[i + 1].y - points[i].y) / (points[i + 1].x - points[i].x)
      tangents.push((d0 + d1) / 2)
    }
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const dx = points[i + 1].x - points[i].x
    const cp1x = points[i].x + dx / 3
    const cp1y = points[i].y + tangents[i] * dx / 3
    const cp2x = points[i + 1].x - dx / 3
    const cp2y = points[i + 1].y - tangents[i + 1] * dx / 3
    
    path += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${points[i + 1].x},${points[i + 1].y}`
  }
  
  return path
}

function monotoneYCurve(points) {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  const tangents = []
  for (let i = 0; i < n; i++) {
    if (i === 0) {
      tangents.push((points[1].x - points[0].x) / (points[1].y - points[0].y))
    } else if (i === n - 1) {
      tangents.push((points[n - 1].x - points[n - 2].x) / (points[n - 1].y - points[n - 2].y))
    } else {
      const d0 = (points[i].x - points[i - 1].x) / (points[i].y - points[i - 1].y)
      const d1 = (points[i + 1].x - points[i].x) / (points[i + 1].y - points[i].y)
      tangents.push((d0 + d1) / 2)
    }
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const dy = points[i + 1].y - points[i].y
    const cp1x = points[i].x + tangents[i] * dy / 3
    const cp1y = points[i].y + dy / 3
    const cp2x = points[i + 1].x - tangents[i + 1] * dy / 3
    const cp2y = points[i + 1].y - dy / 3
    
    path += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${points[i + 1].x},${points[i + 1].y}`
  }
  
  return path
}

function stepBeforeCurve(points) {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const midY = (points[i].y + points[i + 1].y) / 2
    path += ` L${points[i].x},${midY} L${points[i + 1].x},${midY}`
  }
  
  path += ` L${points[n - 1].x},${points[n - 1].y}`
  
  return path
}

function stepAfterCurve(points) {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const midX = (points[i].x + points[i + 1].x) / 2
    path += ` L${midX},${points[i].y} L${midX},${points[i + 1].y}`
  }
  
  path += ` L${points[n - 1].x},${points[n - 1].y}`
  
  return path
}

// ─── SVG 曲线后处理 ─────────────────────────────────────────────────────────────

function parseCurveConfig(mmdContent) {
  const match = mmdContent.match(/%%\s*\{\s*init\s*:\s*\{\s*'flowchart'\s*:\s*\{\s*'curve'\s*:\s*'([^']+)'\s*\}\s*\}\s*\}\s*%%/)
  
  if (match) {
    const curveType = match[1]
    const validTypes = ['basis', 'monotoneX', 'monotoneY', 'stepBefore', 'stepAfter']
    if (validTypes.includes(curveType)) {
      return curveType
    }
  }
  
  return null
}

function parsePoints(pointsStr) {
  const points = []
  const pairs = pointsStr.trim().split(/\s+/)
  
  for (const pair of pairs) {
    const [x, y] = pair.split(',').map(Number)
    if (!isNaN(x) && !isNaN(y)) {
      points.push({ x, y })
    }
  }
  
  return points
}

function convertPolylinesToCurves(svgString, curveType) {
  const polylineRegex = /<polyline([^>]*)points="([^"]*)"([^>]*)\/>/g
  
  return svgString.replace(polylineRegex, (match, before, pointsStr, after) => {
    const points = parsePoints(pointsStr)
    
    if (points.length < 2) {
      return match
    }
    
    const pathData = pointsToCurvePath(points, curveType)
    
    const attrs = (before + after).trim()
    
    return `<path ${attrs} d="${pathData}" />`
  })
}

function applyCurveToSvg(svgString, mmdContent) {
  const curveType = parseCurveConfig(mmdContent)
  
  if (!curveType) {
    return svgString
  }
  
  return convertPolylinesToCurves(svgString, curveType)
}

const AVAILABLE_THEMES = Object.keys(THEMES)

const MMDC_THEME_MAP = {
  'github-dark': 'dark',
  'github-light': 'default',
  'tokyo-night': 'dark',
  'tokyo-night-storm': 'dark',
  'tokyo-night-light': 'default',
  'catppuccin-mocha': 'dark',
  'catppuccin-latte': 'default',
  'nord': 'dark',
  'nord-light': 'default',
  'dracula': 'dark',
  'one-dark': 'dark',
  'solarized-dark': 'dark',
  'solarized-light': 'default',
  'zinc-dark': 'dark',
  'zinc-light': 'default',
  'markdown-preview': 'default',
}

// ─── CSS 变量解析（rsvg-convert 不支持 var() 和 color-mix()）──────────────────

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

function resolveSvgCssVars(svgString, themeColors, font) {
  const vars = {
    '--bg': themeColors.bg,
    '--fg': themeColors.fg,
    '--line': themeColors.line,
    '--accent': themeColors.accent,
    '--muted': themeColors.muted,
    '--surface': themeColors.surface,
    '--border': themeColors.border,
  }

  const bg = themeColors.bg
  const fg = themeColors.fg

  const derived = {
    '--_text':         vars['--fg'],
    '--_text-sec':     vars['--muted'] || mixColors(fg, 60, bg),
    '--_text-muted':   vars['--muted'] || mixColors(fg, 40, bg),
    '--_text-faint':   mixColors(fg, 25, bg),
    '--_line':         vars['--line'] || mixColors(fg, 50, bg),
    '--_arrow':        vars['--accent'] || mixColors(fg, 85, bg),
    '--_node-fill':    vars['--surface'] || mixColors(fg, 3, bg),
    '--_node-stroke':  vars['--border'] || mixColors(fg, 20, bg),
    '--_group-fill':   bg,
    '--_group-hdr':    mixColors(fg, 5, bg),
    '--_inner-stroke': mixColors(fg, 12, bg),
    '--_key-badge':    mixColors(fg, 10, bg),
  }

  const allVars = { ...vars, ...derived }

  // Remove <style> block and @import (rsvg-convert can't use them)
  let result = svgString.replace(/<style>[\s\S]*?<\/style>/, '')

  // Replace inline style var() on <svg> tag — skip background when transparent
  if (themeColors.transparent) {
    result = result.replace(/style="[^"]*"/, '')
  } else {
    result = result.replace(/style="[^"]*"/, `style="background:${bg}"`)
  }

  // Replace all var(--xxx) and var(--xxx, fallback) in attributes
  result = result.replace(/var\(([^)]+)\)/g, (match, inner) => {
    const parts = inner.split(',').map(s => s.trim())
    const varName = parts[0]
    if (allVars[varName]) return allVars[varName]
    // Handle fallback: var(--name, color-mix(...)) — use the derived value
    if (parts.length > 1) {
      const fallback = parts.slice(1).join(',').trim()
      if (fallback.startsWith('color-mix')) {
        // Parse: color-mix(in srgb, var(--fg) XX%, var(--bg))
        const mixMatch = fallback.match(/color-mix\(in srgb,\s*var\(([^)]+)\)\s+(\d+)%,\s*var\(([^)]+)\)\)/)
        if (mixMatch) {
          const c1 = allVars[mixMatch[1]] || fg
          const pct = parseInt(mixMatch[2])
          const c2 = allVars[mixMatch[3]] || bg
          return mixColors(c1, pct, c2)
        }
      }
      return fallback
    }
    return match
  })

  // Resolve any remaining color-mix() that weren't inside var()
  result = result.replace(/color-mix\(in srgb,\s*([^,]+?)\s+(\d+)%,\s*([^)]+)\)/g, (match, c1str, pct, c2str) => {
    let c1 = c1str.trim()
    let c2 = c2str.trim()
    if (c1.startsWith('var(')) c1 = allVars[c1.slice(4,-1)] || fg
    if (c2.startsWith('var(')) c2 = allVars[c2.slice(4,-1)] || bg
    if (c1.startsWith('#') && c2.startsWith('#')) {
      return mixColors(c1, parseInt(pct), c2)
    }
    return match
  })

  // Add font style inline (since @import was removed)
  const fontFamily = font || "'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'Hiragino Sans GB', 'WenQuanYi Micro Hei', 'Inter', -apple-system, system-ui, sans-serif"
  const fontStyle = `<style>text { font-family: ${fontFamily}; }</style>`
  result = result.replace('</defs>', `</defs>${fontStyle}`)

  // Add background rect (rsvg-convert ignores CSS background property)
  if (!themeColors.transparent) {
    const vbMatch = result.match(/viewBox="([^"]+)"/)
    if (vbMatch) {
      const [x, y, w, h] = vbMatch[1].split(/\s+/).map(Number)
      const bgRect = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${bg}"/>`
      // Insert right after <defs>...</defs><style>...</style>
      result = result.replace(/<\/style>/, `</style>${bgRect}`)
    }
  }

  return result
}

// ─── 缓存机制 ─────────────────────────────────────────────────────────────────

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

// ─── 尺寸自适应 ─────────────────────────────────────────────────────────────

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

function detectDiagramType(mmdContent) {
  const firstLine = mmdContent.trim().split('\n')[0].replace(/\s.*/, '').toLowerCase()
  // Handle stateDiagram-v2 → statediagram, xychart-beta → xychart
  const normalized = firstLine.replace(/-v\d+$/, '').replace(/-beta$/, '')
  return BM_SUPPORTED_PREFIXES.includes(normalized) ? normalized : null
}

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
  const file = path.join(os.tmpdir(), 'code_to_diagram_puppeteer.json')
  fs.writeFileSync(file, JSON.stringify(cfg))
  return file
}

function writeChineseFontCss() {
  const css = `text, .label, .edgeLabel, .nodeLabel, .cluster-label {
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'Hiragino Sans GB',
               'WenQuanYi Micro Hei', 'Inter', -apple-system, system-ui, sans-serif !important;
}`
  const file = path.join(os.tmpdir(), 'code_to_diagram_chinese_font.css')
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
    renderer:    'auto',     // 'auto' | 'beautiful-mermaid' | 'mmdc'
    padding:     40,
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
      case '--renderer':              args.renderer     = argv[++i]; break
      case '--padding':               args.padding      = parseInt(argv[++i], 10); break
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
      case '--help':       case '-h': args.command      = 'help'; break
      default:
        console.error(`未知参数：${flag}`)
        process.exit(1)
    }
    i++
  }
  return args
}

// ─── beautiful-mermaid 渲染 ─────────────────────────────────────────────────

function renderWithBeautifulMermaid(mmdContent, args) {
  const themeColors = THEMES[args.theme]
  if (!themeColors) {
    console.error(`❌  未知主题：${args.theme}`)
    console.error(`    可用主题：${AVAILABLE_THEMES.join(', ')}`)
    process.exit(1)
  }

  const options = {
    ...themeColors,
    padding: args.padding,
    transparent: args.transparent,
  }

  if (args.bg) {
    options.bg = args.bg
  }

  console.log(`🎨  使用 beautiful-mermaid 渲染，主题：${args.theme}`)
  let svgString = renderMermaidSVG(mmdContent, options)

  // 应用曲线转换（如果配置了曲线样式）
  const curveType = parseCurveConfig(mmdContent)
  if (curveType) {
    console.log(`🌊  应用曲线样式：${curveType}`)
    svgString = applyCurveToSvg(svgString, mmdContent)
  }

  // 解析 CSS 变量为实际颜色值（rsvg-convert 不支持 var()）
  const resolvedSvg = resolveSvgCssVars(svgString, { ...themeColors, ...(args.bg ? { bg: args.bg } : {}) }, args.font)
  return resolvedSvg
}

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

// ─── mmdc 回退渲染 ──────────────────────────────────────────────────────────

function renderWithMmdc(inputMmdPath, pngPath, args) {
  let mmdc = resolveMmdc()
  let useNpx = false
  if (!mmdc) {
    console.log('⚙️  未直接找到 mmdc，将通过 npx 调用 @mermaid-js/mermaid-cli …')
    useNpx = true
  } else {
    console.log(`🔧  回退使用 mmdc：${mmdc}`)
  }

  const puppeteerCfg = writePuppeteerConfig()
  const chineseFontCss = writeChineseFontCss()
  const mmdcTheme = MMDC_THEME_MAP[args.theme] || 'dark'
  const bgColor = args.bg || (mmdcTheme === 'dark' ? '#0d1117' : '#ffffff')

  const mmdcArgs = [
    ...(useNpx ? ['mmdc'] : []),
    '-i', inputMmdPath,
    '-o', pngPath,
    '-t', mmdcTheme,
    '-b', bgColor,
    '-w', String(args.width),
    '-H', String(args.height),
    '-s', String(args.scale),
    '-p', puppeteerCfg,
    '-C', chineseFontCss,
  ]

  const cmd = useNpx ? 'npx' : mmdc
  console.log(`🎨  正在使用 mmdc 渲染 PNG …`)

  const result = spawnSync(cmd, mmdcArgs, { stdio: 'inherit', shell: false })

  try { fs.unlinkSync(puppeteerCfg) } catch (_) {}
  try { fs.unlinkSync(chineseFontCss) } catch (_) {}

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
  mermaid  使用 beautiful-mermaid 渲染 .mmd → SVG → PNG（默认）
           不支持的图表类型自动回退到 mmdc
  svg      使用 rsvg-convert 渲染 .svg → .png

用法：
  node code_to_diagram.js render [选项]

通用选项：
  --file,       -f  <路径>      输入文件路径（.mmd 或 .svg）
  --content,    -c  <字符串>    Mermaid 源码（仅 mermaid 引擎，与 --file 二选一）
  --name,       -n  <字符串>    输出文件基础名（默认：diagram）
  --output-dir, -o  <路径>      输出目录（默认：当前工作目录）
  --engine,     -e  <引擎>      mermaid | svg（默认：mermaid）
  --no-cache                    禁用缓存，强制重新渲染
  --help,       -h              显示帮助信息

Mermaid 引擎选项（beautiful-mermaid）：
  --theme,      -t  <主题>      ${AVAILABLE_THEMES.join(' | ')}
                                （默认：markdown-preview）
  --renderer        <渲染器>    auto | beautiful-mermaid | mmdc（默认：auto）
  --padding         <像素>      画布内边距（默认：40）
  --transparent                 透明背景
  --bg,         -b  <颜色>      自定义背景色（覆盖主题）
  --font            <字体>      自定义字体（默认：系统字体）

mmdc 回退选项（仅当 renderer=mmdc 或自动回退时）：
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
  # beautiful-mermaid 渲染（默认，自动缓存）
  node code_to_diagram.js render -f diagram.mmd -t tokyo-night -o ./output

  # 强制使用 mmdc
  node code_to_diagram.js render -f diagram.mmd --renderer mmdc -o ./output

  # SVG 引擎
  node code_to_diagram.js render -e svg -f arch.svg --style dark-terminal -o ./output

  # 禁用缓存，强制重新渲染
  node code_to_diagram.js render -f diagram.mmd --no-cache -o ./output

特性说明：
  - 尺寸自适应：根据图表元素数量自动调整输出尺寸（简单图表 8x，中等 12x，复杂 16x）
  - 自动缓存：相同内容和参数的渲染结果会缓存，加速重复渲染
  - 缓存位置：系统临时目录下的 code-to-diagram-cache 文件夹

注意：此脚本仅生成 PNG 图片。Markdown 文档（包含代码逻辑解释和图表源码）由 Claude 生成。
`)
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

  // 选择渲染器
  const diagramType = detectDiagramType(mmdContent)
  let useBM = false

  if (args.renderer === 'mmdc') {
    useBM = false
  } else if (args.renderer === 'beautiful-mermaid') {
    useBM = true
  } else {
    // auto: 根据图表类型决定
    useBM = diagramType !== null
  }

  if (useBM) {
    try {
      const svgString = renderWithBeautifulMermaid(mmdContent, args)
      svgToPng(svgString, pngPath, null, !args.noCache)
    } catch (err) {
      console.log(`⚠️  beautiful-mermaid 渲染失败，回退到 mmdc：${err.message}`)
      useBM = false
    }
  }

  if (!useBM) {
    if (!inputMmdPath) {
      inputMmdPath = path.join(os.tmpdir(), `code_to_diagram_${Date.now()}.mmd`)
      fs.writeFileSync(inputMmdPath, mmdContent, 'utf-8')
      cleanupMmd = true
    }
    renderWithMmdc(inputMmdPath, pngPath, args)
  }

  if (cleanupMmd && inputMmdPath) {
    try { fs.unlinkSync(inputMmdPath) } catch (_) {}
  }

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

  const renderer = useBM ? 'beautiful-mermaid' : 'mmdc'
  console.log(JSON.stringify({ md: mdPath, png: pngPath, engine: 'mermaid', theme: args.theme, renderer }))

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
