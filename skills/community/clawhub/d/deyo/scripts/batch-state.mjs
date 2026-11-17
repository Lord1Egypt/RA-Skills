#!/usr/bin/env node
// Local recovery only. This module has no network, CLI execution, or model client.
import { constants } from 'node:fs'
import { lstat, mkdir, open, realpath, rename, unlink, rmdir, link } from 'node:fs/promises'
import path from 'node:path'
import { randomUUID } from 'node:crypto'
import { fileURLToPath } from 'node:url'

const stages = new Set(['pending', 'running', 'transcribed', 'completed', 'skipped', 'failed', 'summary_failed', 'paused_auth', 'paused_balance', 'unknown'])
const reasons = new Set(['unsupported', 'confirmed_failure', 'auth', 'balance', 'uncertain', 'summary_failed'])
const halted = new Set(['running', 'unknown', 'paused_auth', 'paused_balance'])
const idPattern = /^\d{3,}$/

async function directory(target) {
  const stat = await lstat(target)
  if (!stat.isDirectory() || stat.isSymbolicLink() || (stat.mode & 0o077)) throw new Error('Private ordinary directory required')
}
async function readPrivate(target) {
  const file = await open(target, constants.O_RDONLY | constants.O_NOFOLLOW)
  try {
    const stat = await file.stat()
    if (!stat.isFile() || stat.nlink !== 1 || (stat.mode & 0o077)) throw new Error('Private ordinary file required')
    return await file.readFile('utf8')
  } finally { await file.close() }
}
async function publish(target, text) {
  if (typeof text !== 'string' || !text.trim()) throw new Error('Non-empty content required')
  const temporary = `${target}.${randomUUID()}.tmp`
  const file = await open(temporary, 'wx', 0o600)
  try { await file.writeFile(text); await file.sync() } finally { await file.close() }
  try { await link(temporary, target) } finally { await unlink(temporary) }
}
function validate(state) {
  if (state.schema !== 1 || !Array.isArray(state.items)) throw new Error('Invalid local manifest')
  const ids = new Set()
  for (const item of state.items) {
    if (!idPattern.test(item.id) || ids.has(item.id) || !stages.has(item.stage)) throw new Error('Invalid item state')
    ids.add(item.id)
    if (item.taskId && !/^[a-zA-Z0-9_-]{1,128}$/.test(item.taskId)) throw new Error('Invalid task identifier')
    if (item.error && !reasons.has(item.error)) throw new Error('Unsafe error')
  }
  return state
}
export async function createBatch(requested, inputs) {
  if (!Array.isArray(inputs) || !inputs.length || inputs.some(input => typeof input !== 'string' || !input.trim())) throw new Error('Explicit input list required')
  const parent = await realpath(path.dirname(path.resolve(requested)))
  const stem = path.basename(path.resolve(requested))
  let root
  for (let suffix = 0; ; suffix++) {
    root = path.join(parent, `${stem}${suffix ? `-${suffix + 1}` : ''}`)
    try { await mkdir(root, { mode: 0o700 }); break } catch (error) { if (error.code !== 'EEXIST') throw error }
  }
  const seen = new Map(), duplicates = [], items = []
  inputs.forEach((input, index) => {
    if (seen.has(input)) { duplicates.push({ inputNumber: index + 1, sameAs: seen.get(input) }); return }
    const id = String(items.length + 1).padStart(3, '0')
    seen.set(input, id)
    // Never persist input URLs or paths: the numbered original list stays with the user.
    items.push({ id, inputNumber: index + 1, stage: 'pending', taskId: null, transcript: null, summary: null, error: null })
  })
  for (const item of items) await mkdir(path.join(root, item.id), { mode: 0o700 })
  await publish(path.join(root, 'manifest.json'), JSON.stringify({ schema: 1, revision: 0, duplicates, items }, null, 2) + '\n')
  return { root, duplicates }
}
export async function readBatch(root) {
  await directory(root)
  return validate(JSON.parse(await readPrivate(path.join(root, 'manifest.json'))))
}
async function change(root, work) {
  await directory(root)
  const lock = path.join(root, '.batch-lock')
  await mkdir(lock, { mode: 0o700 }) // Atomic claim; never steal a stale lock.
  try {
    const state = await readBatch(root)
    const result = await work(state)
    state.revision++
    validate(state)
    const draft = path.join(root, `.manifest-${randomUUID()}.tmp`)
    await publish(draft, JSON.stringify(state, null, 2) + '\n')
    // Only this helper's manifest is mutable; all delivered content is no-clobber.
    await readPrivate(path.join(root, 'manifest.json'))
    await rename(draft, path.join(root, 'manifest.json'))
    return result ?? state
  } finally { await rmdir(lock) }
}
function itemById(state, id) {
  const item = state.items.find(item => item.id === id)
  if (!item) throw new Error('Unknown input number')
  return item
}
export async function beginItem(root, id) {
  return change(root, state => {
    if (state.items.some(item => halted.has(item.stage))) throw new Error('Batch paused: verify existing state first')
    const item = itemById(state, id)
    if (item.stage !== 'pending') throw new Error('Never resubmit an existing item')
    const next = state.items.find(item => item.stage === 'pending')
    if (next?.id !== id) throw new Error('Process inputs in order')
    item.stage = 'running'
  })
}
export async function recordTask(root, id, taskId) {
  return change(root, state => {
    const item = itemById(state, id)
    if (item.stage !== 'running') throw new Error('No active item')
    if (!/^[a-zA-Z0-9_-]{1,128}$/.test(taskId) || (item.taskId && item.taskId !== taskId)) throw new Error('Invalid task identifier')
    item.taskId = taskId
  })
}
export async function settleItem(root, id, outcome, transcript) {
  return change(root, async state => {
    const item = itemById(state, id)
    if (item.stage !== 'running' && item.stage !== 'unknown') throw new Error('No active or verified unknown item')
    if (outcome === 'transcribed') {
      await directory(path.join(root, id))
      await publish(path.join(root, id, 'transcript.txt'), transcript)
      item.transcript = `${id}/transcript.txt`
      item.stage = 'transcribed'
      item.error = null
    } else {
      const outcomes = { unsupported: 'skipped', confirmed_failure: 'failed', auth: 'paused_auth', balance: 'paused_balance', uncertain: 'unknown' }
      if (!outcomes[outcome]) throw new Error('Explicit known outcome required')
      item.stage = outcomes[outcome]
      item.error = outcome
    }
  })
}
export function splitTranscript(text, size = 800) {
  if (!Number.isSafeInteger(size) || size < 400 || size > 920) throw new Error('Invalid chunk size')
  const points = Array.from(text), chunks = []
  for (let start = 0; start < points.length; start += size) chunks.push({ number: chunks.length + 1, start, end: Math.min(start + size, points.length), text: points.slice(start, start + size).join('') })
  return chunks
}
export async function transcriptChunks(root, id) {
  const item = itemById(await readBatch(root), id)
  if (!item.transcript) throw new Error('No saved transcript')
  await directory(path.join(root, id))
  return splitTranscript(await readPrivate(path.join(root, id, 'transcript.txt')))
}
export async function readChunkPage(root, id, offset = 0, limit = 5) {
  if (!Number.isSafeInteger(offset) || offset < 0 || !Number.isSafeInteger(limit) || limit < 1 || limit > 20) throw new Error('Invalid chunk page')
  const chunks = await transcriptChunks(root, id)
  if (offset >= chunks.length) throw new Error('Chunk offset out of range')
  const nextOffset = offset + limit < chunks.length ? offset + limit : null
  return { totalChunks: chunks.length, chunks: chunks.slice(offset, offset + limit), nextOffset }
}
export async function saveSummary(root, id, text, readChunks) {
  return change(root, async state => {
    const item = itemById(state, id)
    if (!['transcribed', 'summary_failed'].includes(item.stage)) throw new Error('Summary requires saved transcript')
    const chunks = await transcriptChunks(root, id)
    if (JSON.stringify(readChunks) !== JSON.stringify(chunks.map(chunk => chunk.number))) throw new Error('Read every chunk before summarizing')
    if (text === null) { item.stage = 'summary_failed'; item.error = 'summary_failed'; return }
    if (!['核心观点', '关键事实', '待核实信息', `[${id}]`].every(part => text.includes(part))) throw new Error('Summary sections and source number required')
    await publish(path.join(root, id, 'summary.md'), text)
    item.summary = `${id}/summary.md`
    item.stage = 'completed'
    item.error = null
  })
}
export async function resumeBatch(root) {
  return change(root, state => {
    for (const item of state.items) if (item.stage === 'running') { item.stage = 'unknown'; item.error = 'uncertain' }
    // A resume request is not evidence that a task was never created.
  })
}
export async function releasePause(root, id, verifiedNoTask) {
  if (verifiedNoTask !== true) throw new Error('Verify no task was created before resuming')
  return change(root, state => {
    const item = itemById(state, id)
    if (!['paused_auth', 'paused_balance'].includes(item.stage) || item.taskId) throw new Error('Existing or uncertain task must not be resubmitted')
    item.stage = 'pending'; item.error = null
  })
}
export async function finishBatch(root, overview) {
  return change(root, async state => {
    if (state.items.some(item => ['pending', ...halted].includes(item.stage))) throw new Error('Batch not settled')
    const completed = new Set(state.items.filter(item => item.stage === 'completed').map(item => item.id))
    if (!['共识', '分歧', '建议'].every(part => overview.includes(part))) throw new Error('Overview sections required')
    const lines = overview.split('\n').filter(line => line.trim() && !line.startsWith('#'))
    for (const line of lines) {
      const refs = [...line.matchAll(/\[(\d{3,})\]/g)].map(match => match[1])
      if (completed.size && !refs.length) throw new Error('Every conclusion needs a source')
      if (refs.some(id => !completed.has(id))) throw new Error('Only completed sources may support conclusions')
    }
    if (!completed.size && overview !== '# 共识\n无成功材料。\n# 分歧\n无成功材料。\n# 建议\n无成功材料。\n') throw new Error('No conclusions without successful sources')
    await publish(path.join(root, 'overview.md'), overview)
    const index = '# 处理索引\n\n' + state.items.map(item => `- [${item.id}] ${item.stage}${item.transcript ? ` · [全文](${item.transcript})` : ''}${item.summary ? ` · [总结](${item.summary})` : ''}`).join('\n') + '\n'
    await publish(path.join(root, 'index.md'), index)
  })
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const input = JSON.parse(await new Promise(resolve => { let text = ''; process.stdin.setEncoding('utf8'); process.stdin.on('data', chunk => { text += chunk }); process.stdin.on('end', () => resolve(text)) }))
    const actions = { init: () => createBatch(input.directory, input.inputs), status: () => readBatch(input.directory), begin: () => beginItem(input.directory, input.id), task: () => recordTask(input.directory, input.id, input.taskId), settle: () => settleItem(input.directory, input.id, input.outcome, input.transcript), chunks: () => readChunkPage(input.directory, input.id, input.offset, input.limit), summary: () => saveSummary(input.directory, input.id, input.text, input.readChunks), resume: () => resumeBatch(input.directory), release: () => releasePause(input.directory, input.id, input.verifiedNoTask), finish: () => finishBatch(input.directory, input.text) }
    if (!actions[input.action]) throw new Error('Unknown action')
    process.stdout.write(JSON.stringify(await actions[input.action]()) + '\n')
  } catch { process.stderr.write('Local batch operation refused; inspect local state before continuing.\n'); process.exitCode = 1 }
}
