/**
 * context-prep.ts — Intelligent context preparation engine
 * Detects actionable references in user messages and pre-fetches context.
 * Supports: file paths, URL prefetch, code symbol grep, stack trace parsing, intent hints.
 *
 * Exports:
 *   prepareContext(msg)       — sync, handles everything except URL fetch
 *   prepareContextAsync(msg)  — async, includes URL fetch on top of sync results
 *   PreparedContext           — { content: string, source: string }
 */

import { existsSync, readFileSync } from 'fs'
import { execFileSync } from 'child_process'

export interface PreparedContext {
  content: string
  source: string
}

// ── constants ──────────────────────────────────────────────────────────────
const MAX_FILES = 2
const INLINE_LIMIT = 2000
const HEAD_LINES = 50
const MAX_URLS = 2
const URL_TIMEOUT_MS = 3000
const MAX_GREP_SYMBOLS = 2
const MAX_GREP_LINES = 5
const GREP_TIMEOUT_MS = 2000
const MAX_STACK_FRAMES = 5
const URL_BODY_CHARS = 300

// ── regex patterns ─────────────────────────────────────────────────────────
const PATH_RE = /(?:~\/|\/[\w.-]+)[\w./-]*\.[\w]+/g
const URL_RE = /https?:\/\/[^\s<>"')\]]+/g
const HEX_RE = /0x[0-9a-f]{6,}/i
const ERROR_RE = /(?:Error|错误|error|FAIL|panic|Exception|TypeError|ReferenceError|SyntaxError)[:：]\s*(.{10,120})/i

// backtick-wrapped identifiers: `someFunc`
const BACKTICK_SYMBOL_RE = /`([a-zA-Z_]\w{2,})`/g
// camelCase or snake_case identifiers (>=6 chars to reduce noise)
const IDENT_RE = /\b([a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*|[a-z]\w*_\w+)\b/g

// stack trace patterns
const STACK_AT_RE = /^\s*at\s+.+[:(]\d+/
const STACK_PY_RE = /^\s*File\s+"[^"]+",\s*line\s+\d+/
const TRACEBACK_RE = /Traceback\s*\(most recent call last\)/

// frame extraction: file:line
const FRAME_TS_RE = /\(([^)]+:\d+:\d+)\)/
const FRAME_PY_RE = /File\s+"([^"]+)",\s*line\s+(\d+)/

// ── helpers ────────────────────────────────────────────────────────────────

function stripHtml(html: string): string {
  // remove script/style blocks, then all tags, collapse whitespace
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim()
}

function extractTitleAndDesc(html: string): { title: string; desc: string } {
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)
  const title = titleMatch ? stripHtml(titleMatch[1]).slice(0, 200) : ''

  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*?)["']/i)
    || html.match(/<meta[^>]*content=["']([^"']*?)["'][^>]*name=["']description["']/i)
  const desc = descMatch ? descMatch[1].slice(0, 300) : ''

  return { title, desc }
}

function detectSymbols(msg: string): string[] {
  const symbols = new Set<string>()

  // backtick-wrapped
  let m: RegExpExecArray | null
  const btRe = new RegExp(BACKTICK_SYMBOL_RE.source, 'g')
  while ((m = btRe.exec(msg)) !== null) {
    symbols.add(m[1])
  }

  // camelCase / snake_case (only if not too many backtick symbols already)
  if (symbols.size < MAX_GREP_SYMBOLS) {
    const idRe = new RegExp(IDENT_RE.source, 'g')
    while ((m = idRe.exec(msg)) !== null) {
      // skip common noise words
      if (['forEach', 'indexOf', 'toString', 'valueOf', 'hasOwnProperty', 'console_log'].includes(m[1])) continue
      symbols.add(m[1])
    }
  }

  return Array.from(symbols).slice(0, MAX_GREP_SYMBOLS)
}

function grepSymbol(symbol: string): string | null {
  try {
    // Sanitize symbol to alphanumeric + underscore only
    const safeSymbol = symbol.replace(/[^a-zA-Z0-9_]/g, '')
    if (!safeSymbol) return null
    const pattern = `(function|class|def|const|let|var|interface|type|export)\\s+${safeSymbol}`
    const result = execFileSync('grep', [
      '-rn', '-E', pattern,
      '--include=*.ts', '--include=*.py', '--include=*.swift', '--include=*.js',
      '.',
    ], {
      cwd: process.cwd(),
      timeout: GREP_TIMEOUT_MS,
      encoding: 'utf-8',
      maxBuffer: 64 * 1024,
    }).trim()
    // Limit output lines
    const lines = result.split('\n').slice(0, MAX_GREP_LINES).join('\n')
    return lines || null
  } catch {
    return null
  }
}

function parseStackTrace(msg: string): PreparedContext | null {
  const lines = msg.split('\n')
  const frames: string[] = []
  let errorType = ''

  for (const line of lines) {
    if (TRACEBACK_RE.test(line)) continue

    // detect error type line (e.g. "TypeError: foo is not a function")
    if (ERROR_RE.test(line) && !errorType) {
      errorType = line.trim().slice(0, 150)
    }

    // JS/TS stack frame
    if (STACK_AT_RE.test(line)) {
      const fm = FRAME_TS_RE.exec(line)
      if (fm && frames.length < MAX_STACK_FRAMES) {
        frames.push(fm[1])
      }
      continue
    }

    // Python stack frame
    const pyMatch = FRAME_PY_RE.exec(line)
    if (pyMatch && frames.length < MAX_STACK_FRAMES) {
      frames.push(`${pyMatch[1]}:${pyMatch[2]}`)
    }
  }

  if (frames.length === 0) return null

  const header = errorType ? `错误: ${errorType}\n` : ''
  const body = frames.map((f, i) => `  ${i + 1}. ${f}`).join('\n')
  return {
    content: `[堆栈解析] ${header}关键帧:\n${body}`,
    source: 'stack-parse',
  }
}

function buildIntentHint(flags: {
  hasFiles: boolean
  hasErrors: boolean
  hasHex: boolean
  hasUrls: boolean
  hasSymbols: boolean
  hasStack: boolean
}): PreparedContext | null {
  const hints: string[] = []
  if (flags.hasFiles)   hints.push('用户在讨论特定文件')
  if (flags.hasErrors || flags.hasStack) hints.push('用户在调试问题')
  if (flags.hasHex)     hints.push('用户在做逆向/调试')
  if (flags.hasUrls)    hints.push('用户在引用外部资源')
  if (flags.hasSymbols) hints.push('用户在讨论代码实现')

  if (hints.length === 0) return null
  return {
    content: `[意图预判] ${hints.join('；')}`,
    source: 'intent-hint',
  }
}

// ── main sync entry ────────────────────────────────────────────────────────

export function prepareContext(msg: string): PreparedContext[] {
  const contexts: PreparedContext[] = []
  const intentFlags = {
    hasFiles: false,
    hasErrors: false,
    hasHex: false,
    hasUrls: false,
    hasSymbols: false,
    hasStack: false,
  }

  // 1. File paths — e.g. /Users/z/foo/bar.py, ~/src/main.ts
  const rawPaths = msg.match(PATH_RE) || []
  const paths = rawPaths
    .map(p => p.startsWith('~/') ? p.replace('~', process.env.HOME || '') : p)
    .slice(0, MAX_FILES)

  for (const p of paths) {
    try {
      if (!existsSync(p)) continue
      intentFlags.hasFiles = true
      const content = readFileSync(p, 'utf-8')
      if (content.length <= INLINE_LIMIT) {
        contexts.push({ content: `[文件内容: ${p}]\n${content}`, source: p })
      } else {
        const lines = content.split('\n')
        const head = lines.slice(0, HEAD_LINES).join('\n')
        contexts.push({
          content: `[文件内容: ${p}] (${lines.length}行, 前${HEAD_LINES}行)\n${head}`,
          source: p,
        })
      }
    } catch { /* file not readable, skip */ }
  }

  // 2. Stack trace parsing (before simple error detect, as it's more specific)
  const stackCtx = parseStackTrace(msg)
  if (stackCtx) {
    intentFlags.hasStack = true
    contexts.push(stackCtx)
  }

  // 3. Error messages — extract key error info
  const errorMatch = msg.match(ERROR_RE)
  if (errorMatch) {
    intentFlags.hasErrors = true
    // only add simple error detect if stack parse didn't already cover it
    if (!stackCtx) {
      contexts.push({ content: `[错误信息提取] ${errorMatch[1].trim()}`, source: 'error-detect' })
    }
  }

  // 4. Hex addresses — reverse engineering / debugging
  if (HEX_RE.test(msg)) {
    intentFlags.hasHex = true
    contexts.push({ content: `[检测到内存地址] 用户可能在做逆向/调试，注意地址格式和偏移量`, source: 'hex-detect' })
  }

  // 5. Code symbol grep
  const symbols = detectSymbols(msg)
  for (const sym of symbols) {
    const result = grepSymbol(sym)
    if (result) {
      intentFlags.hasSymbols = true
      contexts.push({
        content: `[代码符号: ${sym}]\n${result}`,
        source: `grep:${sym}`,
      })
    }
  }

  // 6. URL detection (flag only — actual fetch in async version)
  const urls = msg.match(URL_RE) || []
  if (urls.length > 0) {
    intentFlags.hasUrls = true
  }

  // 7. Intent hint (always last)
  const hint = buildIntentHint(intentFlags)
  if (hint) {
    contexts.push(hint)
  }

  return contexts
}

// ── async entry (includes URL prefetch) ────────────────────────────────────

async function fetchUrlContext(url: string): Promise<PreparedContext | null> {
  try {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), URL_TIMEOUT_MS)

    const resp = await fetch(url, {
      signal: controller.signal,
      headers: { 'User-Agent': 'cc-soul-context/1.0', 'Accept': 'text/html' },
      redirect: 'follow',
    })
    clearTimeout(timer)

    const contentType = resp.headers.get('content-type') || ''
    if (!contentType.includes('text/html')) return null

    const html = await resp.text()
    const { title, desc } = extractTitleAndDesc(html)
    const bodyText = stripHtml(html).slice(0, URL_BODY_CHARS)

    const parts: string[] = [`[URL 预取: ${url}]`]
    if (title) parts.push(`标题: ${title}`)
    if (desc)  parts.push(`描述: ${desc}`)
    if (bodyText) parts.push(`正文: ${bodyText}`)

    return {
      content: parts.join('\n'),
      source: `url:${url}`,
    }
  } catch {
    return null
  }
}

export async function prepareContextAsync(msg: string): Promise<PreparedContext[]> {
  // start with all sync results
  const contexts = prepareContext(msg)

  // additionally fetch URLs
  const urls = (msg.match(URL_RE) || []).slice(0, MAX_URLS)
  if (urls.length > 0) {
    const results = await Promise.allSettled(urls.map(u => fetchUrlContext(u)))
    for (const r of results) {
      if (r.status === 'fulfilled' && r.value) {
        contexts.push(r.value)
      }
    }
  }

  return contexts
}
