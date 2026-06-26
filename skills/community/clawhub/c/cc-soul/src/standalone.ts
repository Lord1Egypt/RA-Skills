/**
 * standalone.ts — cc-soul 独立启动入口
 *
 * 不依赖 OpenClaw，直接启动 HTTP API 服务。
 * 用法：npx tsx cc-soul/standalone.ts [--port 18800]
 *
 * API 端点：
 *   POST /memories  — 存记忆（自动提取事实）
 *   POST /search    — 搜记忆 + 返回相关事实
 *   GET  /health    — 健康检查
 */

// 解析命令行参数
const args = process.argv.slice(2)
const portIdx = args.indexOf('--port')
const port = portIdx >= 0 && args[portIdx + 1] ? parseInt(args[portIdx + 1]) : 18800

async function main() {
  console.log(`[cc-soul] standalone mode — starting...`)

  // 初始化数据目录
  try {
    const { ensureDataDir } = require('./persistence.ts')
    ensureDataDir()
  } catch {}

  // 初始化 SQLite（独立 soul.db）
  try {
    const { initSQLite } = require('./sqlite-store.ts')
    initSQLite()
  } catch (e: any) {
    console.error(`[cc-soul] SQLite init failed: ${e.message}`)
  }

  // 初始化 soul 引擎
  try {
    const { initializeSoul } = require('./init.ts')
    initializeSoul()
  } catch {}

  // 启动 HTTP API
  try {
    const { startSoulApi } = require('./soul-api.ts')
    startSoulApi()
  } catch (e: any) {
    console.error(`[cc-soul] soul-api start failed: ${e.message}`)
    process.exit(1)
  }

  console.log(`[cc-soul] ✅ standalone API ready — http://0.0.0.0:${port}`)
  console.log(`[cc-soul] endpoints:`)
  console.log(`  POST /memories  — store memory`)
  console.log(`  POST /search    — search memories`)
  console.log(`  GET  /health    — health check`)
}

main().catch(e => {
  console.error(`[cc-soul] startup failed: ${e.message}`)
  process.exit(1)
})
