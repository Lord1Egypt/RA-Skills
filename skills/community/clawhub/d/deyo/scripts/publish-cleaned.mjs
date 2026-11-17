#!/usr/bin/env node

import { randomBytes } from 'node:crypto'
import { open, link, unlink } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'

function fail(message) {
  process.stderr.write(`${message}\n`)
  process.exitCode = 1
}

function readTargetArgument(argv) {
  if (argv.includes('--help')) {
    process.stdout.write('Usage: publish-cleaned.mjs --target <path> < cleaned-draft.txt\n')
    return null
  }

  const targetIndex = argv.indexOf('--target')
  if (targetIndex === -1 || !argv[targetIndex + 1] || argv.length !== 2) {
    throw new Error('Usage: publish-cleaned.mjs --target <path> < cleaned-draft.txt')
  }

  return argv[targetIndex + 1]
}

function normalizeTxtTarget(input) {
  const resolved = path.resolve(input)
  const parsed = path.parse(resolved)

  if (parsed.ext.toLowerCase() === '.txt') {
    return resolved
  }

  const stem = parsed.ext ? parsed.name : parsed.base
  if (!stem) {
    throw new Error('The cleaned output target must include a file name')
  }

  return path.join(parsed.dir, `${stem}.txt`)
}

function * candidatePaths(target) {
  yield target

  const parsed = path.parse(target)
  const cleanedMatch = parsed.name.match(/^(.*)\.cleaned(?:-(\d+))?$/)
  const baseStem = cleanedMatch ? cleanedMatch[1] : parsed.name
  let suffix = cleanedMatch
    ? (cleanedMatch[2] ? BigInt(cleanedMatch[2]) + 1n : 2n)
    : 1n

  while (true) {
    const name = suffix === 1n
      ? `${baseStem}.cleaned.txt`
      : `${baseStem}.cleaned-${suffix}.txt`
    yield path.join(parsed.dir, name)
    suffix += 1n
  }
}

async function readStdin() {
  const chunks = []
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.from(chunk))
  }
  return Buffer.concat(chunks)
}

async function publishNoClobber(target, content) {
  const directory = path.dirname(target)
  const temporaryPath = path.join(
    directory,
    `.${path.basename(target)}.${process.pid}.${randomBytes(8).toString('hex')}.tmp`,
  )

  let temporaryExists = false
  try {
    const handle = await open(temporaryPath, 'wx', 0o600)
    temporaryExists = true
    try {
      await handle.writeFile(content)
      await handle.sync()
    }
    finally {
      await handle.close()
    }

    for (const candidate of candidatePaths(target)) {
      try {
        await link(temporaryPath, candidate)
        await unlink(temporaryPath)
        temporaryExists = false
        return candidate
      }
      catch (error) {
        if (error?.code === 'EEXIST') {
          continue
        }
        throw error
      }
    }
  }
  finally {
    if (temporaryExists) {
      await unlink(temporaryPath).catch(() => {})
    }
  }
}

try {
  process.umask(0o077)
  const targetArgument = readTargetArgument(process.argv.slice(2))
  if (targetArgument !== null) {
    const target = normalizeTxtTarget(targetArgument)
    const content = await readStdin()
    const publishedPath = await publishNoClobber(target, content)
    process.stdout.write(`${publishedPath}\n`)
  }
}
catch (error) {
  fail(error instanceof Error ? error.message : String(error))
}
