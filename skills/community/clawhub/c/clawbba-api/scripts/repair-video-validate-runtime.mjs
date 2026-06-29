#!/usr/bin/env node
/**
 * 自愈：Gateway 上 video dispatch 已打但 clawbbaValidateVideoGenerateParams 未定义。
 * install / ensure-openclaw-patches 也会调用。
 */
import fs from 'node:fs'
import path from 'node:path'
import { findAllOpenclawDists, findDistJsFile, formatOpenclawDistDiscoveryReport } from './openclaw-dist-paths.mjs'
import { ensureMediaToolValidateRuntime, injectModuleLevelMediaRuntime } from './clawbba-media-tool-validate.mjs'
import { patchVideoGenerateMediaDispatch } from './clawbba-media-dispatch-patch.mjs'
import {
  mediaValidateRuntimeSummary,
  videoValidateRuntimeIsBroken,
  videoValidateRuntimeIsHealthy,
} from './clawbba-video-validate-health.mjs'
import { clawbbaDebugLog, clawbbaDebugLogPath } from './clawbba-debug-log.mjs'

const RUN_ID = process.env.CLAWBBA_DEBUG_RUN_ID || 'repair-pre'

function findToolsFile(dist) {
  return findDistJsFile(dist, 'openclaw-tools-', 'createVideoGenerateTool')
}

function repairDist(dist) {
  const tools = findToolsFile(dist)
  if (!tools) {
    clawbbaDebugLog({
      hypothesisId: 'D',
      location: 'repair-video-validate-runtime.mjs:repairDist',
      message: 'no openclaw-tools bundle in dist',
      data: { dist },
      runId: RUN_ID,
    })
    return { dist, status: 'missing-tools' }
  }
  const toolsPath = path.join(dist, tools)
  const before = fs.readFileSync(toolsPath, 'utf8')
  const beforeSummary = mediaValidateRuntimeSummary(before)

  clawbbaDebugLog({
    hypothesisId: 'A',
    location: 'repair-video-validate-runtime.mjs:before',
    message: 'dist health before repair',
    data: { dist, tools, ...beforeSummary },
    runId: RUN_ID,
  })

  if (!videoValidateRuntimeIsBroken(before) && videoValidateRuntimeIsHealthy(before)) {
    clawbbaDebugLog({
      hypothesisId: 'A',
      location: 'repair-video-validate-runtime.mjs:skip',
      message: 'already healthy',
      data: { dist, tools },
      runId: RUN_ID,
    })
    return { dist, tools, status: 'healthy', ...beforeSummary }
  }

  let status = 'unchanged'
  try {
    const v = patchVideoGenerateMediaDispatch(toolsPath)
    status = `vidDispatch:${v}`
  } catch (e) {
    clawbbaDebugLog({
      hypothesisId: 'B',
      location: 'repair-video-validate-runtime.mjs:vidDispatch',
      message: 'patchVideoGenerateMediaDispatch failed',
      data: { dist, error: String(e?.message || e) },
      runId: RUN_ID,
    })
  }

  const ensure = ensureMediaToolValidateRuntime(toolsPath)
  status += `,mediaValidate:${ensure}`
  if (!videoValidateRuntimeIsHealthy(fs.readFileSync(toolsPath, 'utf8'))) {
    const src2 = fs.readFileSync(toolsPath, 'utf8')
    const out2 = injectModuleLevelMediaRuntime(src2)
    if (out2 !== src2) {
      fs.writeFileSync(toolsPath, out2)
      status += ',moduleRuntime:patched'
    }
  }

  const after = fs.readFileSync(toolsPath, 'utf8')
  const afterSummary = mediaValidateRuntimeSummary(after)
  const fixed = !videoValidateRuntimeIsBroken(after) && videoValidateRuntimeIsHealthy(after)

  clawbbaDebugLog({
    hypothesisId: fixed ? 'A' : 'C',
    location: 'repair-video-validate-runtime.mjs:after',
    message: fixed ? 'repair succeeded' : 'repair still broken',
    data: { dist, tools, status, before: beforeSummary, after: afterSummary },
    runId: RUN_ID,
  })

  if (!fixed) {
    return { dist, tools, status: 'failed', ...afterSummary }
  }
  return { dist, tools, status: `fixed (${status})`, ...afterSummary }
}

const dists = findAllOpenclawDists()
clawbbaDebugLog({
  hypothesisId: 'D',
  location: 'repair-video-validate-runtime.mjs:main',
  message: 'discovered dists',
  data: { count: dists.length, dists },
  runId: RUN_ID,
})

if (!dists.length) {
  process.stderr.write(
    `[clawbba-api] x repair-video-validate: OpenClaw dist not found\n${formatOpenclawDistDiscoveryReport([])}\n  Set OPENCLAW_DIST or ensure openclaw is on PATH\n`,
  )
  process.exit(1)
}

process.stderr.write(formatOpenclawDistDiscoveryReport(dists))
if (/^(1|true|yes)$/i.test(String(process.env.CLAWBBA_DEBUG || ''))) {
  process.stderr.write(`[clawbba-api] debug log: ${clawbbaDebugLogPath()}\n`)
}

const results = dists.map(repairDist)
const failed = results.filter((r) => r.status === 'failed' || r.broken)

for (const r of results) {
  const tag = r.status === 'healthy' ? 'ok' : r.status.startsWith('fixed') ? 'ok' : 'x'
  process.stderr.write(`[clawbba-api] ${tag} ${r.dist}: ${r.status}\n`)
}

if (failed.length) {
  process.stderr.write(
    '[clawbba-api] x video_validate runtime incomplete; upgrade clawbba-api 2.0.8+ and re-run install\n',
  )
  process.exit(1)
}

process.stderr.write('[clawbba-api] ok video_validate runtime on all dist(s)\n')
