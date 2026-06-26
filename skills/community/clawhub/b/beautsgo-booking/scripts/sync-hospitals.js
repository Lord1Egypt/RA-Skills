/**
 * 同步医院数据脚本
 *
 * 从 BeautsGO 后台 API 拉取最新医院列表，更新 data/hospitals.json
 *
 * 用法:
 *   node scripts/sync-hospitals.js              # 仅同步 JSON
 *   node scripts/sync-hospitals.js --publish    # 同步 + git push + clawhub publish
 *   node scripts/sync-hospitals.js --dry-run    # 模拟运行，只显示差异
 */

const https = require('https')
const http = require('http')
const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

const API_URL = 'https://api.yestokr.com/openapi/HospitalManage/listing'
const TOKEN = 'beautsgo-openapi-fixed-token-change-me'
const DATA_FILE = path.resolve(__dirname, '..', 'data', 'hospitals.json')
const SKILL_DIR = path.resolve(__dirname, '..')

// 解析参数
const args = process.argv.slice(2)
const DRY_RUN = args.includes('--dry-run')
const SHOULD_PUBLISH = args.includes('--publish')

/**
 * 调用后台 API 获取医院列表
 */
function fetchHospitals() {
  return new Promise((resolve, reject) => {
    const url = new URL(API_URL)
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'X-Open-Token': TOKEN,
      },
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', chunk => { data += chunk })
      res.on('end', () => {
        try {
          const json = JSON.parse(data)
          if (json.code === 0 && Array.isArray(json.data)) {
            resolve(json.data)
          } else {
            reject(new Error(`API 返回异常: ${json.msg || JSON.stringify(json)}`))
          }
        } catch (e) {
          reject(new Error(`响应解析失败: ${data.slice(0, 200)}`))
        }
      })
    })
    req.on('error', reject)
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('请求超时')) })
    req.end()
  })
}

/**
 * 格式化医院数据为 hospitals.json 所需的格式
 * API 返回的字段与 JSON 基本一致，只需确保字段完整
 */
function formatHospital(raw) {
  return {
    id: raw.id,
    name: raw.name || '',
    alias: raw.alias || raw.name || '',
    en_name: raw.en_name || '',
    pinyin: raw.pinyin || '',
    pinyin_abbr: raw.pinyin_abbr || '',
    url: raw.url || '',
    booking_url: raw.booking_url || '',
    zh_cn_address: raw.zh_cn_address || '',
    en_address: raw.en_address || '',
    ko_kr_address: raw.ko_kr_address || '',
    ja_address: raw.ja_address || '',
    th_address: raw.th_address || '',
  }
}

/**
 * 按 id 排序
 */
function sortById(a, b) {
  return a.id - b.id
}

async function main() {
  console.log('🔄 正在从后台拉取医院列表...')
  const rawList = await fetchHospitals()
  console.log(`  ✓ 获取到 ${rawList.length} 条记录`)

  // 格式化
  const formatted = rawList.map(formatHospital).sort(sortById)

  // 读取当前本地数据（如果存在）
  let currentList = []
  let currentCount = 0
  try {
    currentList = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'))
    currentCount = currentList.length
  } catch (e) {
    console.log('  ! 本地文件不存在，将创建新文件')
  }

  // 对比差异
  const existingIds = new Set(currentList.map(h => h.id))
  const newIds = new Set(formatted.map(h => h.id))
  const added = formatted.filter(h => !existingIds.has(h.id))
  const removed = currentList.filter(h => !newIds.has(h.id))

  console.log(`\n📊 差异统计:`)
  console.log(`  • 本地现有: ${currentCount} 条`)
  console.log(`  • 后台现有: ${formatted.length} 条`)
  console.log(`  • 新增:     ${added.length} 条`)
  console.log(`  • 移除:     ${removed.length} 条`)
  if (added.length > 0) {
    console.log(`  新增医院:`)
    added.forEach(h => console.log(`    + [${h.id}] ${h.name}`))
  }
  if (removed.length > 0) {
    console.log(`  移除医院:`)
    removed.forEach(h => console.log(`    - [${h.id}] ${h.name}`))
  }
  if (currentCount === formatted.length && added.length === 0 && removed.length === 0) {
    console.log(`  ℹ️  数据无变化，无需更新`)
    return
  }

  if (DRY_RUN) {
    console.log(`\n🔍 模拟模式，不写入文件`)
    return
  }

  // 写入文件
  fs.writeFileSync(DATA_FILE, JSON.stringify(formatted, null, 2), 'utf-8')
  console.log(`\n✅ 已更新 ${DATA_FILE}（${formatted.length} 条）`)

  // 如果指定 --publish，自动提交 + 发布
  if (SHOULD_PUBLISH) {
    console.log(`\n📤 提交 Git...`)
    execSync(`cd "${SKILL_DIR}" && git add data/hospitals.json && git commit -m "chore: sync hospitals data (${added.length} new, ${removed.length} removed)" && git push`, {
      stdio: 'inherit',
      cwd: SKILL_DIR,
    })
    console.log(`\n🚀 发布到 ClawHub...`)
    execSync(`clawhub publish "${SKILL_DIR}" --slug beautsgo-booking --version 1.0.10 --changelog "sync hospitals data: ${added.length} added, ${removed.length} removed"`, {
      stdio: 'inherit',
      cwd: SKILL_DIR,
    })
    console.log(`\n🎉 同步完成并已发布！`)
  } else {
    console.log(`\n💡 提示: 加 --publish 参数可自动 git push + clawhub publish`)
  }
}

main().catch(err => {
  console.error(`\n❌ 同步失败: ${err.message}`)
  process.exit(1)
})
