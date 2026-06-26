#!/usr/bin/env node

const baseUrl = (process.argv[2] ?? 'http://127.0.0.1:17341').replace(/\/+$/, '')

async function readJson(path, init) {
  const response = await fetch(`${baseUrl}${path}`, init)
  const text = await response.text()
  const payload = text ? JSON.parse(text) : {}
  if (!response.ok) {
    throw new Error(`${path} failed: ${response.status} ${text}`)
  }
  return payload
}

await readJson('/healthz')
const capabilities = await readJson('/v1/capabilities')

if (capabilities.model !== 'gpt-image-2') {
  throw new Error('expected gpt-image-2 capability')
}

if (capabilities.max_images !== 4) {
  throw new Error('expected max_images=4')
}

if (capabilities.references?.mode !== 'original_image') {
  throw new Error('expected original_image reference mode')
}

const controller = new AbortController()
const request = fetch(`${baseUrl}/v1/images/generate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  signal: controller.signal,
  body: JSON.stringify({
    prompt: 'smoke cancellation test',
    count: 4,
    size: '1024x1024',
    quality: 'low',
    output_format: 'png'
  })
})

setTimeout(() => controller.abort(), 500)

try {
  await request
} catch (error) {
  if (error?.name !== 'AbortError') {
    throw error
  }
}

console.log(`Codex image server smoke passed: ${baseUrl}`)
