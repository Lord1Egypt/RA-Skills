/**
 * rag.ts — Document ingestion (RAG-lite)
 *
 * Users can paste URLs or long text, cc-soul chunks and stores as memories.
 * No vector DB needed — uses existing tag-based recall system.
 */

import type { SoulModule } from './brain.ts'
import { existsSync, readFileSync } from 'fs'
import { extname } from 'path'
import { spawnCLI } from './cli.ts'
import { addMemory } from './memory.ts'

const URL_PATTERN = /https?:\/\/[^\s<>"']+/g
const MAX_CHUNK_SIZE = 500  // chars per chunk

/**
 * Detect if a message contains a URL or is very long text that should be ingested.
 */
export function shouldIngest(msg: string): boolean {
  URL_PATTERN.lastIndex = 0
  if (URL_PATTERN.test(msg) && (msg.includes('记住') || msg.includes('remember') || msg.includes('读一下') || msg.includes('read this'))) {
    return true
  }
  // Very long paste (>1000 chars) with ingest signal
  if (msg.length > 1000 && (msg.includes('记住这个') || msg.includes('remember this') || msg.includes('存一下') || msg.includes('save this'))) {
    return true
  }
  return false
}

/**
 * Extract URL from message.
 */
function extractUrl(msg: string): string | null {
  URL_PATTERN.lastIndex = 0
  const match = msg.match(URL_PATTERN)
  return match ? match[0] : null
}

/**
 * Chunk Markdown by ## headings — each section becomes one chunk.
 * Falls back to paragraph chunking if no headings found.
 */
function chunkMarkdown(text: string, maxSize = MAX_CHUNK_SIZE): string[] {
  const sections = text.split(/^(?=##\s)/m)
  if (sections.length <= 1) return chunkByParagraph(text, maxSize)
  const result: string[] = []
  for (const section of sections) {
    if (section.length <= maxSize) {
      if (section.trim().length > 10) result.push(section.trim())
    } else {
      result.push(...chunkByParagraph(section, maxSize))
    }
  }
  return result
}

/**
 * Chunk code files by function/class definitions.
 * Detects: function, class, def, fn, func, impl, export (TS/JS/Python/Rust/Go).
 */
function chunkCode(text: string, maxSize = MAX_CHUNK_SIZE): string[] {
  const defPattern = /^(?:export\s+)?(?:async\s+)?(?:function|class|def|fn|func|impl|interface|type|struct|enum)\s/m
  const lines = text.split('\n')
  const chunks: string[] = []
  let current: string[] = []
  for (const line of lines) {
    if (defPattern.test(line) && current.length > 0) {
      const block = current.join('\n').trim()
      if (block.length > 10) {
        if (block.length <= maxSize) chunks.push(block)
        else chunks.push(...chunkByParagraph(block, maxSize))
      }
      current = []
    }
    current.push(line)
  }
  if (current.length > 0) {
    const block = current.join('\n').trim()
    if (block.length > 10) {
      if (block.length <= maxSize) chunks.push(block)
      else chunks.push(...chunkByParagraph(block, maxSize))
    }
  }
  return chunks
}

/**
 * Chunk text into memory-sized pieces by paragraph, with sentence-level fallback.
 */
function chunkByParagraph(text: string, maxSize = MAX_CHUNK_SIZE): string[] {
  const chunks: string[] = []
  const paragraphs = text.split(/\n\n+/)
  let current = ''

  for (const para of paragraphs) {
    if (current.length + para.length > maxSize && current.length > 0) {
      chunks.push(current.trim())
      current = para
    } else {
      current += (current ? '\n\n' : '') + para
    }
  }
  if (current.trim()) chunks.push(current.trim())

  // If any chunk is still too large, split by sentences
  const result: string[] = []
  for (const chunk of chunks) {
    if (chunk.length <= maxSize) {
      result.push(chunk)
    } else {
      const sentences = chunk.split(/[。！？.!?\n]+/)
      let buf = ''
      for (const sent of sentences) {
        if (buf.length + sent.length > maxSize && buf.length > 0) {
          result.push(buf.trim())
          buf = sent
        } else {
          buf += (buf ? '。' : '') + sent
        }
      }
      if (buf.trim()) result.push(buf.trim())
    }
  }
  return result.filter(c => c.length > 10)
}

/**
 * Detect if text is an academic paper (arXiv-style) and extract key sections.
 * Returns null if not a paper, or { title, abstract, conclusions } if detected.
 */
function detectPaper(text: string): { title: string; abstract: string; conclusions: string } | null {
  const markers = ['abstract', 'introduction', 'conclusion', 'references', 'methodology', 'related work']
  const found = markers.filter(m => new RegExp(`^\\s*(?:\\d+\\.?\\s*)?${m}`, 'im').test(text))
  if (found.length < 3) return null
  // Title: first non-empty line
  const title = text.split('\n').find(l => l.trim().length > 5)?.trim() || 'Untitled Paper'
  // Abstract: text between "abstract" and next section heading
  const absMatch = text.match(/abstract[:\s]*\n?([\s\S]*?)(?=\n\s*(?:\d+\.?\s*)?(?:introduction|keywords|1\s))/im)
  const abstract = absMatch?.[1]?.trim().slice(0, 800) || ''
  // Conclusions
  const concMatch = text.match(/conclusions?[:\s]*\n?([\s\S]*?)(?=\n\s*(?:\d+\.?\s*)?(?:references|acknowledgment|appendix))/im)
  const conclusions = concMatch?.[1]?.trim().slice(0, 800) || ''
  return { title, abstract, conclusions }
}

/**
 * Chunk academic paper by sections (Abstract, Introduction, etc.)
 */
function chunkPaper(text: string, maxSize = MAX_CHUNK_SIZE): string[] {
  const sections = text.split(/\n(?=\s*(?:\d+\.?\s*)?(?:abstract|introduction|related work|methodology|method|experiment|result|discussion|conclusion|references)\b)/im)
  const chunks: string[] = []
  for (const section of sections) {
    const trimmed = section.trim()
    if (trimmed.length < 15) continue
    if (trimmed.length <= maxSize) { chunks.push(trimmed) }
    else { chunks.push(...chunkByParagraph(trimmed, maxSize)) }
  }
  return chunks
}

/** Route to appropriate chunker based on file extension or content heuristics. */
function chunkText(text: string, maxSize = MAX_CHUNK_SIZE, ext?: string): string[] {
  if (ext === '.md' || ext === '.markdown') return chunkMarkdown(text, maxSize)
  const codeExts = ['.ts', '.js', '.py', '.rs', '.go', '.java', '.swift', '.c', '.cpp', '.h', '.m']
  if (ext && codeExts.includes(ext)) return chunkCode(text, maxSize)
  // Paper detection (arXiv-style)
  if (detectPaper(text)) return chunkPaper(text, maxSize)
  return chunkByParagraph(text, maxSize)
}

/**
 * Ingest a URL: fetch content via CLI, chunk, store as memories.
 */
export function ingestUrl(url: string, userId?: string, channelId?: string) {
  console.log(`[cc-soul][rag] ingesting URL: ${url}`)

  spawnCLI(
    `Read the content from this URL and extract the key information. ` +
    `Return ONLY the main text content (no HTML, no navigation, no ads). ` +
    `If it's too long, summarize the key points.\n\nURL: ${url}`,
    (output) => {
      if (!output || output.length < 50) {
        console.log(`[cc-soul][rag] URL fetch returned empty/short content`)
        return
      }
      if (output.length > 5 * 1024 * 1024) {
        console.log(`[cc-soul][rag] URL content too large (>${(output.length / 1024 / 1024).toFixed(1)}MB), skipping`)
        return
      }

      const chunks = chunkText(output, MAX_CHUNK_SIZE)
      let stored = 0
      for (const chunk of chunks.slice(0, 20)) { // max 20 chunks per URL
        addMemory(`[doc:${url.slice(0, 50)}] ${chunk}`, 'fact', userId, 'global', channelId)
        stored++
      }
      console.log(`[cc-soul][rag] stored ${stored} chunks from ${url}`)
    },
    10000, // 10s timeout for URL fetching
  )
}

/**
 * Ingest raw text: chunk and store as memories.
 */
export function ingestText(text: string, source: string, userId?: string, channelId?: string) {
  const chunks = chunkText(text, MAX_CHUNK_SIZE)
  let stored = 0
  for (const chunk of chunks.slice(0, 30)) { // max 30 chunks per paste
    addMemory(`[doc:${source.slice(0, 30)}] ${chunk}`, 'fact', userId, 'global', channelId)
    stored++
  }
  console.log(`[cc-soul][rag] stored ${stored} text chunks (source: ${source})`)
  return stored
}

/**
 * Ingest a local file: read, chunk based on file type, store as memories.
 * Returns number of chunks stored, or -1 on read failure.
 */
export function ingestFile(filePath: string, userId?: string, channelId?: string): number {
  if (!existsSync(filePath)) {
    console.log(`[cc-soul][rag] file not found: ${filePath}`)
    return -1
  }
  try {
    const text = readFileSync(filePath, 'utf-8')
    if (!text || text.length < 10) { console.log(`[cc-soul][rag] file too short: ${filePath}`); return 0 }
    const ext = extname(filePath).toLowerCase()
    const source = filePath.split('/').pop() || filePath.slice(0, 30)
    // Academic paper detection: store structured summary as scope='paper'
    const paper = detectPaper(text)
    if (paper) {
      const summary = `[paper:${source}] Title: ${paper.title}\nAbstract: ${paper.abstract}\nConclusions: ${paper.conclusions}`
      addMemory(summary, 'paper' as any, userId, 'global', channelId)
      console.log(`[cc-soul][rag] detected paper "${paper.title}" — stored summary`)
    }
    const chunks = paper ? chunkPaper(text, MAX_CHUNK_SIZE) : chunkText(text, MAX_CHUNK_SIZE, ext)
    let stored = paper ? 1 : 0
    for (const chunk of chunks.slice(0, 50)) { // max 50 chunks per file
      addMemory(`[doc:${source}] ${chunk}`, 'fact', userId, 'global', channelId)
      stored++
    }
    console.log(`[cc-soul][rag] ingested file "${filePath}": ${stored} chunks (ext: ${ext})`)
    return stored
  } catch (err: any) {
    console.log(`[cc-soul][rag] failed to read file "${filePath}": ${err.message}`)
    return -1
  }
}

/**
 * Process a message for document ingestion.
 * Called from handler.ts message:preprocessed.
 * Returns augment text if ingestion was triggered, empty string otherwise.
 */
export function processIngestion(msg: string, userId?: string, channelId?: string): string {
  if (!shouldIngest(msg)) return ''

  const url = extractUrl(msg)
  if (url) {
    ingestUrl(url, userId, channelId)
    return `[document ingestion] Reading and storing content from ${url}. It will be available in memory for future conversations.`
  }

  // Long text paste
  if (msg.length > 1000) {
    const preview = msg.slice(0, 50)
    const count = ingestText(msg, preview, userId, channelId)
    return `[document ingestion] Stored ${count} knowledge chunks from pasted text.`
  }

  return ''
}

// ── SoulModule registration ──

export const ragModule: SoulModule = {
  id: 'rag',
  name: 'RAG 检索增强',
  dependencies: ['memory'],
  priority: 50,
}
