#!/usr/bin/env bun
/**
 * Gamma Presentation Generator
 * Calls Gamma API, polls for completion, downloads the result.
 *
 * Usage:
 *   bun run generate.ts --topic "AI Agent Economy" --output ./slides.pdf
 *   bun run generate.ts --topic "Q2 Planning" --format pptx --pages 10
 *   bun run generate.ts --content "$(cat brief.md)" --output ./deck.pdf
 *
 * Env:
 *   GAMMA_API_KEY  — Gamma API key (required)
 */

const GAMMA_API = 'https://public-api.gamma.app/v1.0'
const CONFIG_PATH = `${process.env.HOME}/.gamma/config.json`

async function readManagedKey(): Promise<string | null> {
  try {
    const config = JSON.parse(await Bun.file(CONFIG_PATH).text())
    return config.api_key || null
  } catch {
    return null
  }
}

interface GenerateOptions {
  topic?: string
  content?: string
  format?: 'pdf' | 'pptx'
  pages?: number
  output?: string
}

function parseArgs(): GenerateOptions {
  const args = process.argv.slice(2)
  const opts: GenerateOptions = { format: 'pdf' }
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--topic' && args[i + 1]) opts.topic = args[++i]
    else if (args[i] === '--content' && args[i + 1]) opts.content = args[++i]
    else if (args[i] === '--format' && args[i + 1]) opts.format = args[++i] as 'pdf' | 'pptx'
    else if (args[i] === '--pages' && args[i + 1]) opts.pages = parseInt(args[++i])
    else if (args[i] === '--output' && args[i + 1]) opts.output = args[++i]
  }
  return opts
}

async function createGeneration(apiKey: string, inputText: string): Promise<string> {
  const res = await fetch(`${GAMMA_API}/generations`, {
    method: 'POST',
    headers: {
      'X-API-KEY': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      inputText,
      textMode: 'AUTO',
    }),
  })

  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Gamma API error ${res.status}: ${err}`)
  }

  const data = await res.json() as { generationId: string }
  return data.generationId
}

async function pollGeneration(apiKey: string, generationId: string, maxWait = 120000): Promise<{
  gammaUrl: string
  title: string
}> {
  const start = Date.now()
  while (Date.now() - start < maxWait) {
    const res = await fetch(`${GAMMA_API}/generations/${generationId}`, {
      headers: { 'X-API-KEY': apiKey },
    })

    if (!res.ok) {
      const err = await res.text()
      throw new Error(`Poll error ${res.status}: ${err}`)
    }

    const data = await res.json() as any
    if (data.status === 'completed') {
      return {
        gammaUrl: data.gammaUrl || data.url,
        title: data.title || 'presentation',
      }
    }
    if (data.status === 'failed') {
      throw new Error(`Generation failed: ${data.error || 'unknown'}`)
    }

    // Wait 3 seconds before next poll
    await new Promise(r => setTimeout(r, 3000))
  }
  throw new Error('Generation timed out after ' + (maxWait / 1000) + 's')
}

async function downloadPresentation(gammaUrl: string, format: string, outputPath: string): Promise<string> {
  // Gamma export endpoint
  const exportUrl = `${gammaUrl}/export/${format}`
  console.log(`Downloading ${format} from: ${exportUrl}`)

  const res = await fetch(exportUrl, { redirect: 'follow' })
  if (!res.ok) {
    // Try alternate download approach — Gamma web export
    console.log(`Direct export failed (${res.status}), trying web export...`)
    // For now, return the gammaUrl for manual download
    return gammaUrl
  }

  const buffer = await res.arrayBuffer()
  await Bun.write(outputPath, buffer)
  return outputPath
}

async function main() {
  // API key resolution: BYOK > managed config > env
  const apiKey = process.env.GAMMA_API_KEY
    || await readManagedKey()
  if (!apiKey) {
    console.error('Error: No Gamma API key found.')
    console.error('  BYOK: export GAMMA_API_KEY=sk-gamma-...')
    console.error('  Managed: add key to ~/.gamma/config.json')
    process.exit(1)
  }

  const opts = parseArgs()
  if (!opts.topic && !opts.content) {
    console.log(`Usage:
  bun run generate.ts --topic "Topic" [--format pdf|pptx] [--pages N] [--output path]
  bun run generate.ts --content "Full content" [--format pdf|pptx] [--output path]`)
    process.exit(1)
  }

  const inputText = opts.content || `Create a presentation about: ${opts.topic}${opts.pages ? `. Target ${opts.pages} slides.` : ''}`

  console.log('Creating presentation...')
  const generationId = await createGeneration(apiKey, inputText)
  console.log(`Generation ID: ${generationId}`)

  console.log('Waiting for completion...')
  const result = await pollGeneration(apiKey, generationId)
  console.log(`Done! Title: ${result.title}`)
  console.log(`Gamma URL: ${result.gammaUrl}`)

  if (opts.output) {
    const format = opts.format || 'pdf'
    const downloaded = await downloadPresentation(result.gammaUrl, format, opts.output)
    if (downloaded === result.gammaUrl) {
      console.log(`Download: open ${result.gammaUrl} and export manually`)
    } else {
      console.log(`Saved to: ${downloaded}`)
    }
  }

  // Output JSON for skill consumption
  console.log(JSON.stringify({
    generationId,
    gammaUrl: result.gammaUrl,
    title: result.title,
    output: opts.output || null,
  }))
}

main().catch(e => {
  console.error('Error:', e.message)
  process.exit(1)
})
