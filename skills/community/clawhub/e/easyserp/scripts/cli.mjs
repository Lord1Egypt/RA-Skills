#!/usr/bin/env node
import { readFile } from 'node:fs/promises'
import { EasySerpClient } from './client.mjs'
import { formatMarkdown } from './format.mjs'

const help = `EasySerp CLI\n\nUsage:\n  easyserp search QUERY [--engine google|bing] [--region US] [--format json|markdown] [--include-domain example.com] [--exclude-domain example.com] [--retries 2]\n  easyserp batch FILE [--concurrency 4]\n  easyserp request ID\n  easyserp --help\n\nCredentials: EASYSERP_API_KEY (or SKYVORA_API_KEY or SERP_API_TOKEN). Private key-file option: EASYSERP_API_KEY_FILE. Optional base: EASYSERP_BASE_URL.`
function options(args) {
  const flags = {}; const positional = []
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a.startsWith('--')) { const key = a.slice(2); if (key === 'help') { flags.help = true; continue }; if (!['engine','region','format','idempotency-key','concurrency','include-domain','exclude-domain','retries'].includes(key)) throw Error('Unknown option.'); if (!args[i + 1] || args[i + 1].startsWith('--')) throw Error('Option value is missing.'); const value = args[++i]; if (key === 'include-domain' || key === 'exclude-domain') (flags[key] ??= []).push(value); else flags[key] = value }
    else positional.push(a)
  }
  return { flags, positional }
}
function safeError(e) {
  return e?.toJSON?.() ?? { code: 'client_error', message: e instanceof SyntaxError ? 'Input file is not valid JSON.' : 'Command could not be completed.' }
}
async function main() {
  const { flags, positional } = options(process.argv.slice(2))
  if (flags.help || positional[0] === 'help' || positional[0] === '--help') { process.stdout.write(`${help}\n`); return }
  const client = new EasySerpClient()
  let result
  switch (positional[0]) {
    case 'search': {
      const q = positional.slice(1).join(' ')
      if (!q) throw Error('Search query is required.')
      if (flags.format && !['json','markdown'].includes(flags.format)) throw Error('Format must be json or markdown.')
      result = await client.searchRelevant({ q, ...(flags.engine && { engine: flags.engine }), ...(flags.region && { region: flags.region }), ...(flags['idempotency-key'] && { idempotency_key: flags['idempotency-key'] }) }, { ...(flags.retries !== undefined && { retries: Number(flags.retries) }), includeDomains: flags['include-domain'] ?? [], excludeDomains: flags['exclude-domain'] ?? [] })
      process.stdout.write(flags.format === 'markdown' ? `${formatMarkdown(result)}\n` : `${JSON.stringify(result, null, 2)}\n`); return
    }
    case 'batch': {
      if (!positional[1] || positional.length !== 2) throw Error('Batch requires one JSON file path.')
      const items = JSON.parse(await readFile(positional[1], 'utf8'))
      result = await client.batchSearch(items, { concurrency: flags.concurrency === undefined ? 4 : Number(flags.concurrency), relevant: true, ...(flags.retries !== undefined && { retries: Number(flags.retries) }), includeDomains: flags['include-domain'] ?? [], excludeDomains: flags['exclude-domain'] ?? [] })
      process.stdout.write(`${JSON.stringify(result, null, 2)}\n`); return
    }
    case 'request':
      if (positional.length !== 2) throw Error('Request requires one request ID.')
      result = await client.getRequest(positional[1]); process.stdout.write(`${JSON.stringify(result, null, 2)}\n`); return
    default: throw Error('Command must be search, batch, or request.')
  }
}
main().catch(error => { process.stderr.write(`${JSON.stringify(safeError(error))}\n`); process.exitCode = 1 })
