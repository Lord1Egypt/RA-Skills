import { spawn } from 'node:child_process'
import { randomUUID } from 'node:crypto'
import { createReadStream, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { copyFile, mkdir, mkdtemp, readdir, rm, stat, writeFile } from 'node:fs/promises'
import { createServer } from 'node:http'
import { homedir, tmpdir } from 'node:os'
import path from 'node:path'
import { deflateSync, inflateSync } from 'node:zlib'

export const defaultCodexImageServerPort = Number(process.env.CODEX_IMAGE_SERVER_PORT ?? 17341)
export const defaultCodexImageServerHost = process.env.CODEX_IMAGE_SERVER_HOST ?? '127.0.0.1'

const DEFAULT_MODEL = 'gpt-image-2'
const DEFAULT_OUTPUT_FORMAT = 'png'
const DEFAULT_TIMEOUT_MS = Number(process.env.CODEX_IMAGE_SERVER_TIMEOUT_MS ?? 10 * 60 * 1000)
const MAX_BODY_BYTES = Number(process.env.CODEX_IMAGE_SERVER_MAX_BODY_BYTES ?? 96 * 1024 * 1024)
const GPT_IMAGE_2_MIN_PIXELS = 655_360
const GPT_IMAGE_2_MAX_PIXELS = 8_294_400
const GPT_IMAGE_2_MAX_EDGE = 3840
const GPT_IMAGE_2_MAX_RATIO = 3

const qualityMap = new Map([
  ['自动', 'auto'],
  ['高', 'high'],
  ['中', 'medium'],
  ['低', 'low'],
  ['auto', 'auto'],
  ['high', 'high'],
  ['medium', 'medium'],
  ['low', 'low']
])

const supportedMimeTypes = new Map([
  ['png', 'image/png'],
  ['jpeg', 'image/jpeg'],
  ['jpg', 'image/jpeg'],
  ['webp', 'image/webp']
])

const commonSizes = [
  'auto',
  '1024x1024',
  '1536x1024',
  '1024x1536',
  '2048x2048',
  '2048x1152',
  '1152x2048',
  '3840x2160',
  '2160x3840',
  '2880x2880'
]

const ratioOptions = ['参考图比例', '画布比例', '1:1', '16:9', '9:16', '3:2', '2:3', '4:3', '3:4', '4:5', '5:4', '21:9']
const pngSignature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])

const state = {
  images: new Map()
}

class HttpError extends Error {
  constructor(status, code, message) {
    super(message)
    this.status = status
    this.code = code
  }
}

function getCodexHome() {
  return process.env.CODEX_HOME || path.join(homedir(), '.codex')
}

function getOutputDir() {
  return process.env.CODEX_IMAGE_SERVER_OUTPUT_DIR || path.join(getCodexHome(), 'generated_images', 'http')
}

function getOpenAiApiKey() {
  return process.env.CODEX_IMAGE_SERVER_OPENAI_API_KEY || process.env.OPENAI_API_KEY || ''
}

function getBackend() {
  const configured = (process.env.CODEX_IMAGE_SERVER_BACKEND || 'auto').trim().toLowerCase()
  if (configured === 'openai') {
    return 'openai'
  }

  if (configured === 'codex-exec') {
    return 'codex-exec'
  }

  return getOpenAiApiKey() ? 'openai' : 'codex-exec'
}

function sendJson(response, status, payload) {
  if (response.writableEnded || response.destroyed) {
    return
  }

  response.writeHead(status, {
    'Access-Control-Allow-Headers': 'authorization,content-type',
    'Access-Control-Allow-Methods': 'GET,HEAD,POST,OPTIONS',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'no-store',
    'Content-Type': 'application/json; charset=utf-8'
  })
  response.end(JSON.stringify(payload, null, 2))
}

function sendOptions(response) {
  response.writeHead(204, {
    'Access-Control-Allow-Headers': 'authorization,content-type',
    'Access-Control-Allow-Methods': 'GET,HEAD,POST,OPTIONS',
    'Access-Control-Allow-Origin': '*'
  })
  response.end()
}

function sendError(response, error) {
  if (response.writableEnded || response.destroyed) {
    return
  }

  const status = Number.isInteger(error?.status) ? error.status : 500
  const message = error instanceof Error ? error.message : 'Codex Image Server 请求失败'
  const code = typeof error?.code === 'string' ? error.code : 'server_error'

  sendJson(response, status, {
    error: {
      code,
      message,
      type: status >= 500 ? 'server_error' : 'invalid_request_error'
    }
  })
}

async function readJsonBody(request) {
  const chunks = []
  let total = 0

  for await (const chunk of request) {
    total += chunk.length
    if (total > MAX_BODY_BYTES) {
      throw new HttpError(413, 'body_too_large', '请求体过大')
    }
    chunks.push(chunk)
  }

  const raw = Buffer.concat(chunks).toString('utf8')
  if (!raw) {
    return {}
  }

  try {
    return JSON.parse(raw)
  } catch {
    throw new HttpError(400, 'invalid_json', '请求 JSON 无效')
  }
}

function normalizeOutputFormat(value) {
  const outputFormat = String(value || DEFAULT_OUTPUT_FORMAT).toLowerCase()
  const normalized = outputFormat === 'jpg' ? 'jpeg' : outputFormat
  if (!supportedMimeTypes.has(normalized)) {
    throw new HttpError(400, 'invalid_output_format', 'output_format 必须是 png、jpeg 或 webp')
  }

  return normalized
}

function normalizeQuality(value) {
  const quality = qualityMap.get(String(value || 'auto').trim())
  if (!quality) {
    throw new HttpError(400, 'invalid_quality', 'quality 必须是 low、medium、high 或 auto')
  }

  return quality
}

function normalizeCount(value) {
  const count = Number(value ?? 1)
  if (!Number.isFinite(count)) {
    return 1
  }

  return Math.max(1, Math.min(Math.round(count), 4))
}

function parseSize(value) {
  const match = /^([1-9][0-9]*)x([1-9][0-9]*)$/i.exec(String(value || ''))
  if (!match) {
    return null
  }

  return {
    width: Number(match[1]),
    height: Number(match[2])
  }
}

function validateGptImage2Size(size) {
  if (size === 'auto') {
    return
  }

  const parsed = parseSize(size)
  if (!parsed) {
    throw new HttpError(400, 'invalid_size', 'size 必须是 auto 或 WIDTHxHEIGHT')
  }

  const { width, height } = parsed
  const maxEdge = Math.max(width, height)
  const minEdge = Math.min(width, height)
  const pixels = width * height
  if (maxEdge > GPT_IMAGE_2_MAX_EDGE) {
    throw new HttpError(400, 'invalid_size', 'gpt-image-2 尺寸最长边不能超过 3840px')
  }
  if (width % 16 !== 0 || height % 16 !== 0) {
    throw new HttpError(400, 'invalid_size', 'gpt-image-2 尺寸宽高必须是 16 的倍数')
  }
  if (maxEdge / minEdge > GPT_IMAGE_2_MAX_RATIO) {
    throw new HttpError(400, 'invalid_size', 'gpt-image-2 尺寸长短边比例不能超过 3:1')
  }
  if (pixels < GPT_IMAGE_2_MIN_PIXELS || pixels > GPT_IMAGE_2_MAX_PIXELS) {
    throw new HttpError(400, 'invalid_size', 'gpt-image-2 总像素必须在 655360 到 8294400 之间')
  }
}

function parseRatioText(value) {
  const match = /^([1-9][0-9]*(?:\.\d+)?):([1-9][0-9]*(?:\.\d+)?)$/.exec(String(value || ''))
  if (!match) {
    return null
  }

  const width = Number(match[1])
  const height = Number(match[2])
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
    return null
  }

  return { width, height }
}

function ratioFromDimensions(dimensions) {
  if (!dimensions?.width || !dimensions?.height) {
    return null
  }

  const width = Number(dimensions.width)
  const height = Number(dimensions.height)
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
    return null
  }

  return { width, height }
}

function readReferenceDimensions(references) {
  const first = Array.isArray(references) ? references[0] : undefined
  return ratioFromDimensions(first)
}

function resolveAspectDimensions(aspect, references, canvasSize, fallbackSize) {
  if (aspect === '参考图比例' || aspect === '原图比例' || aspect === 'reference') {
    return readReferenceDimensions(references) ?? parseRatioText(fallbackSize) ?? { width: 16, height: 9 }
  }

  if (aspect === '画布比例' || aspect === 'canvas') {
    return ratioFromDimensions(canvasSize) ?? parseRatioText(fallbackSize) ?? { width: 16, height: 9 }
  }

  if (aspect === 'landscape') {
    return { width: 16, height: 9 }
  }

  if (aspect === 'portrait') {
    return { width: 9, height: 16 }
  }

  if (aspect === 'square') {
    return { width: 1, height: 1 }
  }

  return parseRatioText(aspect) ?? parseRatioText(fallbackSize) ?? { width: 16, height: 9 }
}

function roundDownToMultiple(value, multiple) {
  return Math.max(multiple, Math.floor(value / multiple) * multiple)
}

function deriveSizeForRatio(aspect, maxEdge = GPT_IMAGE_2_MAX_EDGE, maxPixels = GPT_IMAGE_2_MAX_PIXELS) {
  const sourceRatio = aspect.width / aspect.height
  const ratio = Math.max(1 / GPT_IMAGE_2_MAX_RATIO, Math.min(GPT_IMAGE_2_MAX_RATIO, sourceRatio))
  const heightLimitByEdge = ratio >= 1 ? maxEdge / ratio : maxEdge
  const heightLimitByPixels = Math.sqrt(maxPixels / ratio)
  const height = roundDownToMultiple(Math.min(heightLimitByEdge, heightLimitByPixels), 16)
  const width = roundDownToMultiple(height * ratio, 16)
  let candidate = { width, height }

  while (
    candidate.width * candidate.height > maxPixels ||
    Math.max(candidate.width, candidate.height) > maxEdge ||
    Math.max(candidate.width, candidate.height) / Math.min(candidate.width, candidate.height) > GPT_IMAGE_2_MAX_RATIO
  ) {
    if (candidate.width >= candidate.height) {
      candidate.width -= 16
      candidate.height = roundDownToMultiple(candidate.width / ratio, 16)
    } else {
      candidate.height -= 16
      candidate.width = roundDownToMultiple(candidate.height * ratio, 16)
    }
  }

  return `${candidate.width}x${candidate.height}`
}

function resolveRequestedSize(body) {
  const requestedSize = String(body.size || 'auto')
  const explicitSize = parseSize(requestedSize)
  if (explicitSize) {
    validateGptImage2Size(requestedSize)
    return requestedSize
  }

  if (requestedSize.toLowerCase() === '4k') {
    const aspect = resolveAspectDimensions(body.aspect, body.references, body.canvas_size, undefined)
    const size = deriveSizeForRatio(aspect)
    validateGptImage2Size(size)
    return size
  }

  if (requestedSize.toLowerCase() === '2k') {
    const aspect = resolveAspectDimensions(body.aspect, body.references, body.canvas_size, undefined)
    const size = deriveSizeForRatio(aspect, 2048, 2048 * 2048)
    validateGptImage2Size(size)
    return size
  }

  if (requestedSize === 'auto') {
    return 'auto'
  }

  throw new HttpError(400, 'invalid_size', 'size 必须是 auto、2K、4K 或 WIDTHxHEIGHT')
}

function readDataUrlParts(value) {
  const match = /^data:([^;,]+)?(;base64)?,(.*)$/s.exec(String(value || ''))
  if (!match) {
    return null
  }

  const mimeType = match[1] || 'image/png'
  const isBase64 = Boolean(match[2])
  const data = match[3] || ''

  return {
    data,
    extension: mimeType.includes('jpeg') ? 'jpg' : mimeType.includes('webp') ? 'webp' : 'png',
    isBase64,
    mimeType
  }
}

function dataUrlToBuffer(value) {
  const parts = readDataUrlParts(value)
  if (!parts) {
    throw new HttpError(400, 'invalid_reference', '参考图必须是 data URL')
  }

  return {
    buffer: parts.isBase64 ? Buffer.from(parts.data, 'base64') : Buffer.from(decodeURIComponent(parts.data), 'utf8'),
    extension: parts.extension,
    mimeType: parts.mimeType
  }
}

async function writeReferenceFiles(workDir, references) {
  if (!Array.isArray(references) || !references.length) {
    return []
  }

  const referenceDir = path.join(workDir, 'references')
  await mkdir(referenceDir, { recursive: true })

  const files = []
  for (const [index, reference] of references.entries()) {
    if (!reference?.image) {
      continue
    }

    const parsed = dataUrlToBuffer(reference.image)
    const filePath = path.join(referenceDir, `reference-${index + 1}.${parsed.extension}`)
    await writeFile(filePath, parsed.buffer)
    files.push({
      filePath,
      label: reference.label || `参考图 ${index + 1}`,
      mimeType: parsed.mimeType
    })
  }

  return files
}

function getMimeType(filePath, fallback = 'image/png') {
  const extension = path.extname(filePath).slice(1).toLowerCase()
  return supportedMimeTypes.get(extension) ?? fallback
}

function readPngDimensions(buffer) {
  if (buffer.length < 24 || buffer.toString('ascii', 1, 4) !== 'PNG') {
    return null
  }

  return {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20)
  }
}

function readJpegDimensions(buffer) {
  if (buffer.length < 4 || buffer[0] !== 0xff || buffer[1] !== 0xd8) {
    return null
  }

  let offset = 2
  while (offset < buffer.length) {
    if (buffer[offset] !== 0xff) {
      offset += 1
      continue
    }

    const marker = buffer[offset + 1]
    const length = buffer.readUInt16BE(offset + 2)
    if (marker >= 0xc0 && marker <= 0xc3) {
      return {
        height: buffer.readUInt16BE(offset + 5),
        width: buffer.readUInt16BE(offset + 7)
      }
    }

    offset += 2 + length
  }

  return null
}

function readWebpDimensions(buffer) {
  if (buffer.length < 30 || buffer.toString('ascii', 0, 4) !== 'RIFF' || buffer.toString('ascii', 8, 12) !== 'WEBP') {
    return null
  }

  const chunkType = buffer.toString('ascii', 12, 16)
  if (chunkType === 'VP8X') {
    return {
      width: 1 + buffer.readUIntLE(24, 3),
      height: 1 + buffer.readUIntLE(27, 3)
    }
  }

  if (chunkType === 'VP8 ' && buffer.length >= 30) {
    return {
      width: buffer.readUInt16LE(26) & 0x3fff,
      height: buffer.readUInt16LE(28) & 0x3fff
    }
  }

  if (chunkType === 'VP8L' && buffer.length >= 25) {
    const bits = buffer.readUInt32LE(21)
    return {
      width: (bits & 0x3fff) + 1,
      height: ((bits >> 14) & 0x3fff) + 1
    }
  }

  return null
}

function readImageDimensions(filePath) {
  const buffer = readFileSync(filePath)
  return readPngDimensions(buffer) ?? readJpegDimensions(buffer) ?? readWebpDimensions(buffer) ?? null
}

const crcTable = new Uint32Array(256).map((_, index) => {
  let value = index
  for (let bit = 0; bit < 8; bit += 1) {
    value = value & 1 ? 0xedb88320 ^ (value >>> 1) : value >>> 1
  }
  return value >>> 0
})

function crc32(buffer) {
  let value = 0xffffffff
  for (const byte of buffer) {
    value = crcTable[(value ^ byte) & 0xff] ^ (value >>> 8)
  }
  return (value ^ 0xffffffff) >>> 0
}

function paethPredictor(left, up, upperLeft) {
  const estimate = left + up - upperLeft
  const leftDistance = Math.abs(estimate - left)
  const upDistance = Math.abs(estimate - up)
  const upperLeftDistance = Math.abs(estimate - upperLeft)

  if (leftDistance <= upDistance && leftDistance <= upperLeftDistance) {
    return left
  }

  return upDistance <= upperLeftDistance ? up : upperLeft
}

function decodePng(buffer) {
  if (buffer.length < 33 || !buffer.subarray(0, 8).equals(pngSignature)) {
    throw new HttpError(500, 'png_decode_failed', 'PNG 解码失败')
  }

  let offset = 8
  let width = 0
  let height = 0
  let bitDepth = 0
  let colorType = 0
  const idatChunks = []

  while (offset + 8 <= buffer.length) {
    const length = buffer.readUInt32BE(offset)
    const type = buffer.toString('ascii', offset + 4, offset + 8)
    const dataStart = offset + 8
    const dataEnd = dataStart + length
    const data = buffer.subarray(dataStart, dataEnd)

    if (type === 'IHDR') {
      width = data.readUInt32BE(0)
      height = data.readUInt32BE(4)
      bitDepth = data[8]
      colorType = data[9]
    } else if (type === 'IDAT') {
      idatChunks.push(data)
    } else if (type === 'IEND') {
      break
    }

    offset = dataEnd + 4
  }

  if (bitDepth !== 8 || ![0, 2, 6].includes(colorType) || width <= 0 || height <= 0) {
    throw new HttpError(500, 'png_decode_failed', 'PNG 格式不支持')
  }

  const bytesPerPixel = colorType === 6 ? 4 : colorType === 2 ? 3 : 1
  const inflated = inflateSync(Buffer.concat(idatChunks))
  const stride = width * bytesPerPixel
  const rgba = new Uint8Array(width * height * 4)
  let inputOffset = 0
  let previous = new Uint8Array(stride)

  for (let y = 0; y < height; y += 1) {
    const filter = inflated[inputOffset]
    inputOffset += 1
    const row = new Uint8Array(stride)

    for (let x = 0; x < stride; x += 1) {
      const raw = inflated[inputOffset]
      inputOffset += 1
      const left = x >= bytesPerPixel ? row[x - bytesPerPixel] : 0
      const up = previous[x] ?? 0
      const upperLeft = x >= bytesPerPixel ? previous[x - bytesPerPixel] ?? 0 : 0
      const value =
        filter === 0
          ? raw
          : filter === 1
            ? raw + left
            : filter === 2
              ? raw + up
              : filter === 3
                ? raw + Math.floor((left + up) / 2)
                : raw + paethPredictor(left, up, upperLeft)
      row[x] = value & 0xff
    }

    for (let x = 0; x < width; x += 1) {
      const source = x * bytesPerPixel
      const target = (y * width + x) * 4
      if (colorType === 6) {
        rgba[target] = row[source] ?? 0
        rgba[target + 1] = row[source + 1] ?? 0
        rgba[target + 2] = row[source + 2] ?? 0
        rgba[target + 3] = row[source + 3] ?? 255
      } else if (colorType === 2) {
        rgba[target] = row[source] ?? 0
        rgba[target + 1] = row[source + 1] ?? 0
        rgba[target + 2] = row[source + 2] ?? 0
        rgba[target + 3] = 255
      } else {
        const gray = row[source] ?? 0
        rgba[target] = gray
        rgba[target + 1] = gray
        rgba[target + 2] = gray
        rgba[target + 3] = 255
      }
    }

    previous = row
  }

  return { width, height, rgba }
}

function resizeRgbaNearest(source, sourceWidth, sourceHeight, targetWidth, targetHeight) {
  if (sourceWidth === targetWidth && sourceHeight === targetHeight) {
    return source
  }

  const output = new Uint8Array(targetWidth * targetHeight * 4)
  for (let y = 0; y < targetHeight; y += 1) {
    const sourceY = Math.min(sourceHeight - 1, Math.floor((y / targetHeight) * sourceHeight))
    for (let x = 0; x < targetWidth; x += 1) {
      const sourceX = Math.min(sourceWidth - 1, Math.floor((x / targetWidth) * sourceWidth))
      const sourceIndex = (sourceY * sourceWidth + sourceX) * 4
      const targetIndex = (y * targetWidth + x) * 4
      output[targetIndex] = source[sourceIndex] ?? 0
      output[targetIndex + 1] = source[sourceIndex + 1] ?? 0
      output[targetIndex + 2] = source[sourceIndex + 2] ?? 0
      output[targetIndex + 3] = source[sourceIndex + 3] ?? 255
    }
  }

  return output
}

function createPngChunk(type, data) {
  const typeBuffer = Buffer.from(type, 'ascii')
  const length = Buffer.alloc(4)
  length.writeUInt32BE(data.length, 0)
  const crc = Buffer.alloc(4)
  crc.writeUInt32BE(crc32(Buffer.concat([typeBuffer, data])), 0)

  return Buffer.concat([length, typeBuffer, data, crc])
}

function encodePng(width, height, rgba) {
  const ihdr = Buffer.alloc(13)
  ihdr.writeUInt32BE(width, 0)
  ihdr.writeUInt32BE(height, 4)
  ihdr[8] = 8
  ihdr[9] = 6
  ihdr[10] = 0
  ihdr[11] = 0
  ihdr[12] = 0

  const rowLength = width * 4
  const raw = Buffer.alloc((rowLength + 1) * height)
  for (let y = 0; y < height; y += 1) {
    const rowOffset = y * (rowLength + 1)
    raw[rowOffset] = 0
    raw.set(rgba.subarray(y * rowLength, (y + 1) * rowLength), rowOffset + 1)
  }

  return Buffer.concat([
    pngSignature,
    createPngChunk('IHDR', ihdr),
    createPngChunk('IDAT', deflateSync(raw, { level: 6 })),
    createPngChunk('IEND', Buffer.alloc(0))
  ])
}

function resizePngFileToRequestedSize(filePath, requestedSize) {
  const parsed = parseSize(requestedSize)
  if (!parsed || path.extname(filePath).toLowerCase() !== '.png') {
    return
  }

  const current = readImageDimensions(filePath)
  if (current?.width === parsed.width && current?.height === parsed.height) {
    return
  }

  const decoded = decodePng(readFileSync(filePath))
  const resized = resizeRgbaNearest(decoded.rgba, decoded.width, decoded.height, parsed.width, parsed.height)
  writeFileSync(filePath, encodePng(parsed.width, parsed.height, resized))
}

async function listImageFiles(rootDir) {
  const output = []

  async function visit(dir) {
    let entries
    try {
      entries = await readdir(dir, { withFileTypes: true })
    } catch {
      return
    }

    for (const entry of entries) {
      const filePath = path.join(dir, entry.name)
      if (entry.isDirectory()) {
        await visit(filePath)
        continue
      }

      if (/\.(png|jpe?g|webp)$/i.test(entry.name)) {
        try {
          const fileStat = await stat(filePath)
          output.push({ filePath, mtimeMs: fileStat.mtimeMs })
        } catch {
        }
      }
    }
  }

  await visit(rootDir)
  return output.sort((a, b) => b.mtimeMs - a.mtimeMs)
}

function tailOutput(value) {
  return value.slice(-4000).trim()
}

function appendCapped(current, chunk) {
  const next = current + chunk.toString()
  return next.length > 120_000 ? next.slice(-120_000) : next
}

function runCodexExec(args, options) {
  return new Promise((resolve, reject) => {
    const detached = process.platform !== 'win32'
    const child = spawn('codex', args, {
      cwd: options.cwd,
      detached,
      env: {
        ...process.env,
        CODEX_CI: '1'
      },
      stdio: ['pipe', 'pipe', 'pipe']
    })
    let stdout = ''
    let stderr = ''
    let settled = false

    function killChild() {
      if (child.killed) {
        return
      }

      if (detached && child.pid) {
        try {
          process.kill(-child.pid, 'SIGTERM')
          return
        } catch {
        }
      }

      child.kill('SIGTERM')
    }

    function finish(callback) {
      if (settled) {
        return
      }

      settled = true
      clearTimeout(timer)
      options.signal?.removeEventListener('abort', handleAbort)
      callback()
    }

    function handleAbort() {
      killChild()
      finish(() => reject(new HttpError(499, 'request_canceled', '请求已取消')))
    }

    const timer = setTimeout(() => {
      killChild()
      finish(() => reject(new HttpError(504, 'codex_timeout', 'Codex 图像生成超时')))
    }, options.timeoutMs)

    if (options.signal?.aborted) {
      handleAbort()
      return
    }
    options.signal?.addEventListener('abort', handleAbort, { once: true })

    child.stdout.on('data', (chunk) => {
      stdout = appendCapped(stdout, chunk)
    })
    child.stderr.on('data', (chunk) => {
      stderr = appendCapped(stderr, chunk)
    })
    child.on('error', (error) => {
      finish(() => reject(new HttpError(502, 'codex_spawn_failed', `无法启动 Codex：${error.message}`)))
    })
    child.on('close', (code) => {
      if (code === 0) {
        finish(() => resolve({ stdout, stderr }))
        return
      }

      finish(() => reject(new HttpError(502, 'codex_exec_failed', tailOutput(stderr || stdout) || `Codex 退出码 ${code}`)))
    })
    child.stdin.end(options.stdin || '')
  })
}

function parseSessionId(output) {
  return /session id:\s*([0-9a-f-]+)/i.exec(output)?.[1] ?? null
}

async function findCodexGeneratedImages(startedAtMs, output) {
  const codexHome = getCodexHome()
  const sessionId = parseSessionId(output)
  if (sessionId) {
    const sessionDir = path.join(codexHome, 'generated_images', sessionId)
    const sessionFiles = await listImageFiles(sessionDir)
    if (sessionFiles.length) {
      return sessionFiles
    }
  }

  const allFiles = await listImageFiles(path.join(codexHome, 'generated_images'))
  return allFiles.filter((entry) => entry.mtimeMs >= startedAtMs - 2000)
}

function buildCodexExecPrompt(body, resolvedSize, quality, referenceFiles, variantIndex, totalCount) {
  const prompt = String(body.prompt || '').trim() || (referenceFiles.length ? '根据参考图生成一张新图' : '生成一张新图')
  const lines = [
    'Use the image_generation tool to create the requested raster image.',
    'Do not create images with shell commands, ImageMagick, SVG, HTML, Canvas, Python, local drawing scripts, or placeholder files.',
    'The final image must come from the image_generation tool and be saved under CODEX_HOME/generated_images.',
    `Primary request: ${prompt}`,
    `Generate image ${variantIndex + 1} of ${totalCount}. Make this image a distinct candidate for the same request.`,
    `Target output size: ${resolvedSize}`,
    `Requested quality: ${quality}`,
    `Output format: ${DEFAULT_OUTPUT_FORMAT}`
  ]

  if (referenceFiles.length) {
    lines.push('Use every attached image as a visual reference for the generation or edit.')
  }

  lines.push('Reply with the absolute saved image path only.')
  return lines.join('\n')
}

async function generateOneWithCodexExec(body, resolvedSize, quality, outputFormat, requestId, variantIndex, totalCount, signal) {
  const startedAtMs = Date.now()
  const outputDir = getOutputDir()
  const workDir = await mkdtemp(path.join(tmpdir(), 'codex-image-server-'))
  const lastMessagePath = path.join(workDir, 'last-message.txt')
  const referenceFiles = await writeReferenceFiles(workDir, body.references)
  const prompt = buildCodexExecPrompt(body, resolvedSize, quality, referenceFiles, variantIndex, totalCount)
  const args = [
    'exec',
    '--skip-git-repo-check',
    '--sandbox',
    'read-only',
    '-C',
    workDir,
    '-o',
    lastMessagePath,
    ...referenceFiles.flatMap((reference) => ['--image', reference.filePath])
  ]

  try {
    const result = await runCodexExec(args, { cwd: workDir, signal, stdin: prompt, timeoutMs: DEFAULT_TIMEOUT_MS })
    const generated = await findCodexGeneratedImages(startedAtMs, `${result.stdout}\n${result.stderr}`)
    if (!generated.length) {
      throw new HttpError(502, 'codex_no_image', 'Codex 未返回图像生成结果')
    }

    const source = generated[0].filePath
    const extension = path.extname(source).slice(1).toLowerCase() || outputFormat
    const fileName = `${requestId}${totalCount > 1 ? `-${variantIndex + 1}` : ''}.${extension}`
    const target = path.join(outputDir, fileName)
    await mkdir(outputDir, { recursive: true })
    await copyFile(source, target)
    resizePngFileToRequestedSize(target, resolvedSize)

    return createImageRecord(totalCount > 1 ? `${requestId}-${variantIndex + 1}` : requestId, target, 'codex-exec', body, resolvedSize)
  } finally {
    await rm(workDir, { force: true, recursive: true })
  }
}

async function generateWithCodexExec(body, resolvedSize, quality, outputFormat, count, requestId, signal) {
  const controller = new AbortController()
  const handleAbort = () => controller.abort()
  signal?.addEventListener('abort', handleAbort, { once: true })
  if (signal?.aborted) {
    handleAbort()
  }

  try {
    return await Promise.all(
      Array.from({ length: count }, (_value, index) =>
        generateOneWithCodexExec(body, resolvedSize, quality, outputFormat, requestId, index, count, controller.signal)
      )
    )
  } catch (error) {
    controller.abort()
    throw error
  } finally {
    signal?.removeEventListener('abort', handleAbort)
  }
}

async function readOpenAiImageBytes(item, signal) {
  if (item.b64_json) {
    return Buffer.from(item.b64_json, 'base64')
  }

  if (item.url) {
    let response
    try {
      response = await fetch(item.url, { signal })
    } catch (error) {
      if (signal?.aborted || error?.name === 'AbortError') {
        throw new HttpError(499, 'request_canceled', '请求已取消')
      }

      throw error
    }
    if (!response.ok) {
      throw new HttpError(502, 'openai_image_fetch_failed', 'OpenAI 图片下载失败')
    }
    return Buffer.from(await response.arrayBuffer())
  }

  throw new HttpError(502, 'openai_no_image', 'OpenAI 未返回图片')
}

async function fetchOpenAiJson(url, init) {
  let response
  try {
    response = await fetch(url, init)
  } catch (error) {
    if (init?.signal?.aborted || error?.name === 'AbortError') {
      throw new HttpError(499, 'request_canceled', '请求已取消')
    }

    throw error
  }
  const text = await response.text()
  let payload = {}
  try {
    payload = text ? JSON.parse(text) : {}
  } catch {
    payload = { message: text }
  }

  if (!response.ok) {
    const message = payload.error?.message || payload.message || 'OpenAI 图像 API 请求失败'
    throw new HttpError(response.status, payload.error?.code || 'openai_error', message)
  }

  return payload
}

async function generateWithOpenAi(body, resolvedSize, quality, outputFormat, count, requestId, signal) {
  const apiKey = getOpenAiApiKey()
  if (!apiKey) {
    throw new HttpError(503, 'openai_key_missing', '未配置 CODEX_IMAGE_SERVER_OPENAI_API_KEY 或 OPENAI_API_KEY')
  }

  const hasReferences = Array.isArray(body.references) && body.references.length > 0
  const endpoint = hasReferences ? 'https://api.openai.com/v1/images/edits' : 'https://api.openai.com/v1/images/generations'
  let payload

  if (hasReferences) {
    const form = new FormData()
    form.append('model', DEFAULT_MODEL)
    form.append('prompt', String(body.prompt || '根据参考图生成'))
    form.append('n', String(count))
    form.append('size', resolvedSize)
    form.append('quality', quality)
    form.append('output_format', outputFormat)

    for (const [index, reference] of body.references.entries()) {
      const parsed = dataUrlToBuffer(reference.image)
      form.append('image[]', new Blob([parsed.buffer], { type: parsed.mimeType }), `reference-${index + 1}.${parsed.extension}`)
    }

    payload = await fetchOpenAiJson(endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`
      },
      signal,
      body: form
    })
  } else {
    payload = await fetchOpenAiJson(endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      signal,
      body: JSON.stringify({
        model: DEFAULT_MODEL,
        prompt: String(body.prompt || '生成一张新图'),
        n: count,
        size: resolvedSize,
        quality,
        output_format: outputFormat
      })
    })
  }

  const data = Array.isArray(payload.data) ? payload.data : []
  const outputDir = getOutputDir()
  await mkdir(outputDir, { recursive: true })

  const records = []
  for (const [index, item] of data.entries()) {
    const id = index === 0 ? requestId : `${requestId}-${index + 1}`
    const target = path.join(outputDir, `${id}.${outputFormat}`)
    writeFileSync(target, await readOpenAiImageBytes(item, signal))
    resizePngFileToRequestedSize(target, resolvedSize)
    records.push(createImageRecord(id, target, 'openai', body, resolvedSize, item.revised_prompt))
  }

  if (!records.length) {
    throw new HttpError(502, 'openai_no_image', 'OpenAI 未返回图片')
  }

  return records
}

function createImageRecord(id, filePath, backend, body, requestedSize, revisedPrompt) {
  const dimensions = readImageDimensions(filePath)
  const mimeType = getMimeType(filePath)
  const record = {
    id,
    backend,
    filePath,
    label: '生成图',
    mimeType,
    model: DEFAULT_MODEL,
    requestedSize,
    resolvedSize: dimensions ? `${dimensions.width}x${dimensions.height}` : requestedSize,
    revisedPrompt: revisedPrompt || body.prompt || ''
  }
  state.images.set(id, record)
  return record
}

function createPublicImageRecord(record, origin) {
  return {
    id: record.id,
    label: record.label,
    mime_type: record.mimeType,
    model: record.model,
    path: record.filePath,
    resolved_size: record.resolvedSize,
    revised_prompt: record.revisedPrompt,
    url: `${origin}/v1/images/${encodeURIComponent(record.id)}/file`
  }
}

function findImageRecord(id) {
  const existing = state.images.get(id)
  if (existing) {
    return existing
  }

  const outputDir = getOutputDir()
  for (const extension of ['png', 'jpg', 'jpeg', 'webp']) {
    const filePath = path.join(outputDir, `${id}.${extension}`)
    if (!existsSync(filePath)) {
      continue
    }

    const record = createImageRecord(id, filePath, 'unknown', {}, 'auto')
    state.images.set(id, record)
    return record
  }

  return null
}

function sendImageFile(response, record, method) {
  try {
    const fileStat = statSync(record.filePath)
    response.writeHead(200, {
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-store',
      'Content-Length': String(fileStat.size),
      'Content-Type': record.mimeType
    })
    if (method === 'HEAD') {
      response.end()
      return
    }
    createReadStream(record.filePath).pipe(response)
  } catch {
    sendJson(response, 404, { error: { code: 'not_found', message: '图片文件不存在' } })
  }
}

function createCapabilities() {
  return {
    backend: getBackend(),
    model: DEFAULT_MODEL,
    output_formats: ['png', 'jpeg', 'webp'],
    qualities: ['auto', 'high', 'medium', 'low'],
    max_images: 4,
    ratio_options: ratioOptions,
    size_options: commonSizes,
    size_constraints: {
      custom_size: true,
      max_edge: GPT_IMAGE_2_MAX_EDGE,
      max_pixels: GPT_IMAGE_2_MAX_PIXELS,
      min_pixels: GPT_IMAGE_2_MIN_PIXELS,
      multiple_of: 16,
      max_ratio: '3:1'
    },
    high_resolution_presets: {
      landscape: '3840x2160',
      portrait: '2160x3840',
      square: '2880x2880'
    },
    references: {
      max_images: 16,
      mode: 'original_image'
    }
  }
}

async function handleGenerate(request, response, requestUrl) {
  const abortController = new AbortController()
  let completed = false
  const abortRequest = () => {
    if (!completed) {
      abortController.abort()
    }
  }

  request.on('aborted', abortRequest)
  response.on('close', abortRequest)

  const body = await readJsonBody(request)
  const outputFormat = normalizeOutputFormat(body.output_format)
  const quality = normalizeQuality(body.quality)
  const count = normalizeCount(body.count ?? body.n)
  const resolvedSize = resolveRequestedSize(body)
  const requestId = `codex-${randomUUID()}`
  const backend = getBackend()
  try {
    const records =
      backend === 'openai'
        ? await generateWithOpenAi(body, resolvedSize, quality, outputFormat, count, requestId, abortController.signal)
        : await generateWithCodexExec(body, resolvedSize, quality, outputFormat, count, requestId, abortController.signal)
    const publicRecords = records.map((record) => createPublicImageRecord(record, requestUrl.origin))

    completed = true
    sendJson(response, 200, {
      id: publicRecords[0]?.id,
      status: 'completed',
      backend,
      model: DEFAULT_MODEL,
      requested_size: resolvedSize,
      resolved_size: publicRecords[0]?.resolved_size ?? resolvedSize,
      quality,
      mime_type: publicRecords[0]?.mime_type ?? supportedMimeTypes.get(outputFormat),
      path: publicRecords[0]?.path,
      url: publicRecords[0]?.url,
      revised_prompt: publicRecords[0]?.revised_prompt ?? body.prompt ?? '',
      data: publicRecords
    })
  } finally {
    completed = true
    request.off('aborted', abortRequest)
    response.off('close', abortRequest)
  }
}

export function createCodexImageServer() {
  return createServer(async (request, response) => {
    const requestUrl = new URL(
      request.url ?? '/',
      `http://${request.headers.host ?? `${defaultCodexImageServerHost}:${defaultCodexImageServerPort}`}`
    )

    try {
      if (request.method === 'OPTIONS') {
        sendOptions(response)
        return
      }

      if (request.method === 'GET' && requestUrl.pathname === '/healthz') {
        mkdirSync(getOutputDir(), { recursive: true })
        sendJson(response, 200, {
          status: 'ok',
          backend: getBackend(),
          model: DEFAULT_MODEL,
          output_dir: getOutputDir()
        })
        return
      }

      if (request.method === 'GET' && requestUrl.pathname === '/v1/capabilities') {
        sendJson(response, 200, createCapabilities())
        return
      }

      if ((request.method === 'GET' || request.method === 'HEAD') && /^\/v1\/images\/[^/]+\/file$/.test(requestUrl.pathname)) {
        const id = decodeURIComponent(requestUrl.pathname.split('/').at(-2) ?? '')
        const record = findImageRecord(id)
        if (!record) {
          sendJson(response, 404, { error: { code: 'not_found', message: '图片不存在' } })
          return
        }

        sendImageFile(response, record, request.method)
        return
      }

      if (request.method === 'POST' && requestUrl.pathname === '/v1/images/generate') {
        await handleGenerate(request, response, requestUrl)
        return
      }

      sendJson(response, 404, { error: { code: 'not_found', message: 'Not found' } })
    } catch (error) {
      sendError(response, error)
    }
  })
}

export function listenCodexImageServer() {
  const server = createCodexImageServer()

  return new Promise((resolve, reject) => {
    server.once('error', reject)
    server.listen(defaultCodexImageServerPort, defaultCodexImageServerHost, () => {
      server.off('error', reject)
      resolve(server)
    })
  })
}
