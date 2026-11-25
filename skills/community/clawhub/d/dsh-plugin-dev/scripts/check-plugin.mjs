#!/usr/bin/env node
/**
 * DSH 插件机械自检（零依赖，Node >= 18）——退出码裁决，模型只可转述、无权改判
 *
 * 用法：
 *   node check-plugin.mjs <插件目录> [--listing <data/plugins/xxx.yml>]
 *
 * 裁决四态（本工具场景为三态）：
 *   退出码 0 = PASS（无 FAIL；WARN 不阻断）
 *   退出码 1 = FAIL（存在必须修复项）
 *   退出码 2 = 用法/内部错误（UNVERIFIED）
 *
 * 只读文件系统，不执行任何构建/网络/子进程。
 */
import fs from 'node:fs'
import path from 'node:path'

const argv = process.argv.slice(2)
const listIdx = argv.indexOf('--listing')
let listingFile = null
if (listIdx !== -1) {
  listingFile = argv[listIdx + 1]
  argv.splice(listIdx, 2)
}
const pluginDir = argv[0]

const issues = [] // { level: 'FAIL'|'WARN', msg }
const fail = (m) => issues.push({ level: 'FAIL', msg: m })
const warn = (m) => issues.push({ level: 'WARN', msg: m })
const CATEGORY_POOL = ['agi', 'ui', 'usage', 'theme', 'model', 'identity', 'session', 'memory',
  'tools', 'wsl', 'browser', 'vision', 'voice', 'docs', 'skill', 'workflow', 'git', 'notify',
  'dev', 'security', 'remote', 'market', 'fun']

if (!pluginDir) {
  console.error('用法: node check-plugin.mjs <插件目录> [--listing <data/plugins/xxx.yml>]')
  process.exitCode = 2
} else {
  checkPlugin(path.resolve(pluginDir))
  if (listingFile) checkListing(path.resolve(listingFile))
  report()
}

function checkPlugin(dir) {
  const pkgPath = path.join(dir, 'package.json')
  let pkg = null
  if (!fs.existsSync(pkgPath)) { fail('package.json 不存在'); return }
  try { pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8')) }
  catch (e) { fail(`package.json 解析失败: ${e.message}`); return }

  if (!pkg.name) fail('package.json 缺 name')
  if (!pkg.version) fail('package.json 缺 version')

  // —— 硬门槛 1：dsh.bundle manifest ——
  const patchField = pkg?.dsh?.bundle?.patch
  if (!patchField) {
    fail('package.json 未声明 dsh.bundle：没有 dsh.bundle 的包只被当普通依赖安装（dsh plugin 打印警告、不激活任何层）；只声明 dsh.client 会被收录 PR 拒绝')
  } else {
    warnIf(!/^\.\/|^\/?[\w.-]+\.ya?ml$/.test(patchField) && !patchField.endsWith('.yml') && !patchField.endsWith('.yaml'),
      `dsh.bundle.patch="${patchField}" 看起来不像 .yml 文件路径`)
  }

  // —— 硬门槛 2：入口文件存在 ——
  const main = pkg.main || 'index.js'
  if (!fs.existsSync(path.join(dir, main))) fail(`入口文件 ${main} 不存在（files/main 指向的文件必须随包提供）`)

  // —— 硬门槛 3：patch 文件内容 ——
  if (patchField) {
    const patchPath = path.join(dir, patchField)
    if (!fs.existsSync(patchPath)) {
      fail(`patch 文件 ${patchField} 不存在`)
    } else {
      const yml = fs.readFileSync(patchPath, 'utf8')
      if (!/insert\s*:/.test(yml)) fail(`${patchField} 缺 "insert:"（bundle patch 必须贡献插件行）`)
      const names = [...yml.matchAll(/^\s*-?\s*name\s*:\s*(.+)$/gm)].map(m => m[1].trim())
      if (names.length === 0) fail(`${patchField} 没有 name: 行（须指向本包）`)
      for (const raw of names) {
        const unquoted = raw.replace(/^['"]|['"]$/g, '')
        if (/^[./]/.test(unquoted)) fail(`patch 行 name: "${raw}" 用了源码路径——bundle 包必须写包名（Node 模块解析），路径仅限 --patch 开发期 overlay`)
        if (unquoted.startsWith('@') && !/^['"]/.test(raw)) fail(`patch 行 name: ${raw} 以 @ 开头未加引号——@ 是 YAML 保留字符，scoped 包名必须写成 name: '${unquoted}'`)
        if (pkg.name && unquoted !== pkg.name) warn(`patch 行 name: "${unquoted}" 与 package.json name "${pkg.name}" 不一致`)
      }
      if (!/^\s*-?\s*id\s*:\s*\S+/m.test(yml)) fail(`${patchField} 的 insert 行缺 id:`)
    }
    // files 字段完整性
    if (Array.isArray(pkg.files)) {
      const base = (p) => String(p).replace(/^\.\//, '').split('/').pop()
      warnIf(!pkg.files.includes(base(patchField)), `files 缺 ${base(patchField)}（npm 包会缺 patch 文件）`)
      warnIf(!pkg.files.includes(base(main)), `files 缺 ${base(main)}（npm 包会缺入口文件）`)
    } else {
      warn('package.json 无 files 字段：npm publish 将按 .npmignore 默认规则打包，建议显式列出 index 与 patch')
    }
  }

  // —— 收录相关 ——
  const readme = path.join(dir, 'README.md')
  if (!fs.existsSync(readme)) warn('缺 README.md（收录审查要求描述与代码相符，README 是必要载体）')
  else if (!/dsh\s+plugin/.test(fs.readFileSync(readme, 'utf8'))) warn('README 未包含 "dsh plugin" 安装命令（收录审查会看安装方式）')

  const desc = String(pkg.description || '')
  if (!desc || /TODO/.test(desc)) warn('package.json description 缺失或仍是 TODO 占位——收录要求描述与代码一致')

  // —— 工具实现 ——
  const entryPath = path.join(dir, main)
  if (fs.existsSync(entryPath)) {
    const code = fs.readFileSync(entryPath, 'utf8')
    const n = (code.match(/defineTool\s*\(/g) || []).length
    if (n === 0) warn(`${main} 中未发现 defineTool(——纯服务/前端插件可忽略，工具类插件不应为 0`)
    if (/TODO/.test(code)) warn('入口文件仍含 TODO 占位——收录要求"真实可用代码"')
  }

  if (pkg.engines && pkg.engines.dsh) warn('声明了 engines.dsh：注意 SemVer 预发布版本默认不满足常规范围，DSH 当前基线是 0.1.1-rc.2；拿不准就删掉 engines.dsh 让 peer 依赖兜底')
}

function checkListing(f) {
  if (!fs.existsSync(f)) { fail(`listing 文件 ${f} 不存在`); return }
  const lines = fs.readFileSync(f, 'utf8').split(/\r?\n/)

  const get = (key) => {
    for (const l of lines) {
      const m = new RegExp(`^\\s*${key}\\s*:\\s*(.+)$`).exec(l)
      if (m) return m[1].trim()
    }
    return null
  }
  const url = get('url')
  if (!url || !/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+\/?$/.test(url)) {
    fail(`url "${url}" 必须形如 https://github.com/<owner>/<repo>（收录要求 url=仓库 URL）`)
  }
  const ownerRepo = url ? url.replace(/^https:\/\/github\.com\//, '').replace(/\/$/, '') : null
  const name = get('name')
  if (ownerRepo && name !== ownerRepo) fail(`name "${name}" 应为 "${ownerRepo}"（owner/repo 格式，与 url 一致）`)
  const category = get('category')
  if (!category || !CATEGORY_POOL.includes(category)) fail(`category "${category}" 不在分类池：${CATEGORY_POOL.join(' ')}`)
  if (!/^\s*en\s*:\s*\S/m.test(lines.join('\n'))) fail('description.en 必填')

  for (const [i, line] of lines.entries()) {
    const m = /^\s*([\w.-]+)\s*:\s+(.+)$/.exec(line)
    if (!m) continue
    const val = m[2]
    if (/:\s/.test(val) && !/^['"{[]/.test(val)) {
      fail(`第 ${i + 1} 行 "${m[1]}:" 的值含 ": " 但未加引号——YAML 解析会报错，必须加单引号`)
    }
  }
  const tar = get('tarball')
  if (tar && /-\d+\.\d+\.\d+\.tgz/.test(tar)) warn(`tarball 文件名带版本号（${tar}）——收录建议文件名不带版本防 404`)
}

function warnIf(cond, msg) { if (cond) warn(msg) }

function report() {
  for (const { level, msg } of issues) console.log(`[${level}] ${msg}`)
  const nFail = issues.filter(i => i.level === 'FAIL').length
  const nWarn = issues.filter(i => i.level === 'WARN').length
  const verdict = nFail > 0 ? 'FAIL' : 'PASS'
  console.log(`VERDICT: ${verdict} (${nFail} fail, ${nWarn} warn)`)
  process.exitCode = nFail > 0 ? 1 : 0
}
