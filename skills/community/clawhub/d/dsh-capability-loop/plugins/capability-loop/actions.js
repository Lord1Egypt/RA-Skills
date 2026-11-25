/**
 * dsh-capability-loop-bundle — 运行中心（host half 的命令通道）
 *
 * 客户端面板不能直接执行脚本（浏览器半边没有 fetch 到 Host 的通道，也没有写文件权限），
 * 所以「运行体检 / 门禁 / 交接体检 / 打包 / 视觉探测 / 切档位」统一走**会话命令**：
 *
 *   面板 → ctx.remote.commands.execute(sessionId, '/capability-loop run gate design docs/design')
 *        → 本文件的 handler → ctx.subprocess 起 PowerShell/Python → 返回退出码与输出尾部
 *
 * 白名单在 `ACTIONS` 表里，参数逐个校验（不允许任意命令、不允许 shell 拼接）。
 */

import path from 'node:path'

/** 可执行动作（白名单）。kind 决定用哪个解释器。 */
const ACTIONS = {
  audit: { kind: 'ps', script: 'capability-audit.ps1', timeoutMs: 180000, label: '能力体检' },
  gate: { kind: 'ps', script: 'loop-gate.ps1', timeoutMs: 180000, label: '门禁' },
  env: { kind: 'ps', script: 'loop-gate.ps1', timeoutMs: 180000, label: '环境验收' },
  'handoff-audit': { kind: 'py', script: 'handoff-audit.py', timeoutMs: 120000, label: '交接体检' },
  preflight: { kind: 'py', script: 'module-preflight.py', timeoutMs: 120000, label: '模块预检' },
  pack: { kind: 'ps', script: 'package-skill.ps1', timeoutMs: 240000, label: '上架打包' },
  visual: { kind: 'ps', script: 'visual-qa-check.ps1', timeoutMs: 180000, label: '视觉探测' },
  'skill-status': { kind: 'ps', script: 'skill-status.ps1', timeoutMs: 120000, label: '版本检查' },
  'sync-shadow': { kind: 'state', label: '影子计数' },
  mode: { kind: 'state', label: '切档位' },
}

const GATE_KINDS = ['design', 'requirement', 'test', 'all']
const MODES = ['on', 'shadow', 'off']

function clip(text, max) {
  const value = String(text === undefined || text === null ? '' : text)
  if (value.length <= max) return value
  return value.slice(0, Math.max(0, max - 12)) + '…（已截断）'
}

/** 命令名/商店 handle：只接受 ASCII 安全字符。 */
function safeToken(value) {
  const text = String(value === undefined || value === null ? '' : value).trim()
  if (text === '') return ''
  if (!/^[A-Za-z0-9._\-\/\\:]+$/.test(text)) return ''
  if (text.includes('..')) return ''
  return text
}

/**
 * 路径类参数（taskDir / workspace / out）：允许中文、空格、盘符，但拒绝控制字符、
 * `..` 与以 `-` 开头（避免被 PowerShell 当参数）。argv 传参不拼 shell，所以不需要
 * 限制到 ASCII——中文工程目录（如「气量平衡月表」）必须能用。
 */
function safePath(value) {
  const text = String(value === undefined || value === null ? '' : value).trim()
  if (text === '') return ''
  if (/[\u0000-\u001f]/.test(text)) return ''
  if (text.includes('..')) return ''
  if (text.charAt(0) === '-') return ''
  return text
}

/** 在若干候选目录里找 skill 根（含 scripts/loop-state.ps1）。 */
async function resolveSkillDir(ctx, cwd, configured) {
  const fsService = ctx.get('fs')
  if (fsService === undefined) return ''
  const candidates = []
  if (typeof configured === 'string' && configured.trim() !== '') candidates.push(configured.trim())
  const home = process.env.DSH_HOME || ''
  if (home !== '') {
    candidates.push(path.join(home, 'skills', 'dsh-capability-loop'))
    candidates.push(path.join(home, 'skills', 'dsh-capability-loop-bundle'))
  }
  for (const candidate of candidates) {
    try {
      const target = await fsService.resolve(candidate, { cwd })
      const info = await fsService.stat(target)
      if (info !== undefined && info.type === 'directory') return target.path || candidate
    } catch {
      // 继续试下一个
    }
  }
  // 扫 $DSH_HOME/skills 下所有目录，找带 scripts/loop-state.ps1 的那个（商店安装目录名带 handle 前缀）
  if (home !== '') {
    try {
      const root = await fsService.resolve(path.join(home, 'skills'), { cwd })
      const entries = await fsService.listDir(root)
      for (const entry of entries) {
        if (entry.type !== 'directory') continue
        if (entry.name.indexOf('capability-loop') === -1) continue
        const probe = path.join(home, 'skills', entry.name, 'scripts', 'loop-state.ps1')
        try {
          const info = await fsService.stat(await fsService.resolve(probe, { cwd }))
          if (info !== undefined && info.type === 'file') return path.join(home, 'skills', entry.name)
        } catch {
          // 继续
        }
      }
    } catch {
      // 没有 skills 目录
    }
  }
  return ''
}

/** 解析子进程输出（collected.stdout.readFrom(0) 可能是 Buffer 或字符串）。 */
function readCollected(handle) {
  const chunks = []
  for (const stream of ['stdout', 'stderr']) {
    const collected = handle.collected !== undefined && handle.collected !== null ? handle.collected[stream] : undefined
    if (collected === undefined || collected === null || typeof collected.readFrom !== 'function') continue
    try {
      const raw = collected.readFrom(0)
      if (raw === undefined || raw === null) continue
      chunks.push(typeof raw === 'string' ? raw : Buffer.from(raw).toString('utf8'))
    } catch {
      // 读不到就跳过
    }
  }
  return chunks.join('\n').trim()
}

async function runSpawn(ctx, spec) {
  const subprocess = ctx.get('subprocess')
  if (subprocess === undefined) return { ok: false, text: '当前 composition 没有 ctx.subprocess，无法运行脚本。' }
  if (spec.signal !== undefined && spec.signal !== null && spec.signal.aborted) {
    return { ok: false, cancelled: true, text: '已取消（未启动）。' }
  }
  let executable
  try {
    executable = await subprocess.resolveExecutable(spec.executable)
  } catch (error) {
    return { ok: false, text: '找不到解释器 ' + spec.executable + '：' + String(error && error.message ? error.message : error) }
  }
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(new Error('timeout')), spec.timeoutMs)
  // 取消：用户/客户端 abort → 一起中止子进程（Actions 的 signal 可选）。
  const onAbort = () => controller.abort(new Error('cancelled'))
  if (spec.signal !== undefined && spec.signal !== null && typeof spec.signal.addEventListener === 'function') {
    spec.signal.addEventListener('abort', onAbort, { once: true })
  }
  let handle
  try {
    handle = subprocess.spawn({
      argv: [executable, ...spec.argv],
      cwd: spec.cwd,
      stdio: { stdin: 'ignore', stdout: { maxBytes: 256 * 1024 }, stderr: { maxBytes: 64 * 1024 } },
      graceMs: 5000,
      signal: controller.signal,
    })
  } catch (error) {
    clearTimeout(timer)
    return { ok: false, text: '启动失败：' + String(error && error.message ? error.message : error) }
  }
  let exitCode = null
  let failure = ''
  try {
    const outcome = await handle.done
    exitCode = outcome !== undefined && outcome !== null && typeof outcome.exitCode === 'number' ? outcome.exitCode : null
  } catch (error) {
    failure = String(error && error.message ? error.message : error)
  } finally {
    clearTimeout(timer)
    if (spec.signal !== undefined && spec.signal !== null && typeof spec.signal.removeEventListener === 'function') {
      spec.signal.removeEventListener('abort', onAbort)
    }
  }
  const output = readCollected(handle)
  const cancelled = spec.signal !== undefined && spec.signal !== null && spec.signal.aborted === true
  return { ok: exitCode === 0, exitCode, output, failure, cancelled, timedOut: !cancelled && controller.signal.aborted }
}

/** 解析动作参数：`run <action> key=value …` 或 `mode on`。 */
function parseRequest(rawInput) {
  const text = String(rawInput === undefined || rawInput === null ? '' : rawInput).trim()
  if (text === '') return { action: '', args: {} }
  const parts = text.split(/\s+/)
  let action = parts[0]
  let rest = parts.slice(1)
  if (action === 'run') {
    action = rest.length > 0 ? rest[0] : ''
    rest = rest.slice(1)
  }
  const args = {}
  // 关键值可用引号包住（路径里有空格）：taskDir="docs/my design"
  const joined = rest.join(' ')
  const pattern = /([A-Za-z][A-Za-z0-9-]*)=("([^"]*)"|'([^']*)'|(\S+))/g
  let match
  while ((match = pattern.exec(joined)) !== null) {
    const value = match[3] !== undefined ? match[3] : (match[4] !== undefined ? match[4] : match[5])
    args[match[1]] = value
  }
  // 位置参数：`mode on` 这种写法
  if (action === 'mode' && args.value === undefined && rest.length > 0 && rest[0].indexOf('=') === -1) {
    args.value = rest[0]
  }
  return { action, args }
}

function usageText() {
  return [
    '用法：/capability-loop <动作> [key=value …]',
    '',
    '  run gate kind=design|requirement|test|all taskDir=<必填> [grill=1]     门禁',
    '  run env                                                              环境验收（等价 -Environment）',
    '  run audit                                                             九组体检',
    '  run handoff-audit slug=<slug> [workspace=<路径>]                       交接包体检',
    '  run preflight keyword=<词> alias=<英文别名>                            模块/路由预检',
    '  run pack handle=<商店handle>                                           上架打包',
    '  run visual out=<输出目录>                                              视觉探测',
    '  run skill-status                                                      版本检查',
    '  run sync-shadow                                                       影子观察计数',
    '  mode on|shadow|off                                                    切档位',
    '',
    '也可以用面板里的按钮触发同样的命令。',
  ].join('\n')
}

/**
 * 执行一个动作；返回给命令结果的文本。
 * @param ctx 插件 ctx
 * @param cfg 插件配置
 * @param request `{ action, args }`，或 `mode` 的裸值
 */
export async function executeAction(ctx, cfg, rawInput, signal) {
  const parsed = parseRequest(rawInput)
  if (parsed.action === '') return { ok: true, text: usageText() }

  const action = parsed.action
  const spec = ACTIONS[action]
  if (spec === undefined) {
    return { ok: false, text: '未知动作：' + (action || '(空)') + '\n\n' + usageText() }
  }

  const cwd = cfg.workspaceRoot !== '' ? cfg.workspaceRoot : process.cwd()
  const skillDir = await resolveSkillDir(ctx, cwd, cfg.skillDir)
  if (action !== 'mode') {
    if (skillDir === '') return { ok: false, text: '找不到 skill 目录（里面应有 scripts/loop-state.ps1）。请在插件配置里填 skillDir。' }
  }

  // ---- 状态类动作：走 loop-state.ps1 ----
  if (spec.kind === 'state') {
    const stateScript = path.join(skillDir, 'scripts', 'loop-state.ps1')
    let argv = null
    if (action === 'mode') {
      const raw = parsed.args.value || parsed.args.mode || ''
      const value = String(raw || '').trim().toLowerCase()
      if (MODES.indexOf(value) === -1) return { ok: false, text: 'mode 需要 on|shadow|off（收到：' + String(raw || '') + '）' }
      argv = ['-Action', 'set-mode', '-Root', cwd, '-Mode', value]
    } else if (action === 'sync-shadow') {
      argv = ['-Action', 'sync-shadow', '-Root', cwd]
    }
    const result = await runSpawn(ctx, {
      executable: 'powershell',
      argv: ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', stateScript, ...argv],
      cwd,
      timeoutMs: spec.timeoutMs || 120000,
      signal,
    })
    return { ok: result.ok === true, text: formatResult(spec.label, result) }
  }

  // ---- 脚本类动作 ----
  const script = path.join(skillDir, 'scripts', spec.script)
  let argv
  if (spec.kind === 'ps') {
    const psArgs = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script]
    if (action === 'audit') {
      psArgs.push('-Workspace', cwd)
    } else if (action === 'env') {
      psArgs.push('-Environment')
    } else if (action === 'gate') {
      const kind = String(parsed.args.kind || 'auto').trim()
      if (kind !== 'auto' && GATE_KINDS.indexOf(kind) === -1) {
        return { ok: false, text: 'gate 的 kind 只能是 auto|design|requirement|test|all' }
      }
      psArgs.push('-Workspace', cwd, '-Kind', kind)
      const taskDir = safePath(parsed.args.taskDir || '')
      if (taskDir !== '') psArgs.push('-TaskDir', taskDir)
      if (parsed.args.grill === '1' || parsed.args.grill === 'true') psArgs.push('-RequireGrill')
    } else if (action === 'pack') {
      const handle = safeToken(parsed.args.handle || 'testhandle')
      if (handle === '') return { ok: false, text: 'pack 的 handle 含非法字符' }
      psArgs.push('-SkillRoot', skillDir, '-Handle', handle, '-Slug', 'dsh-capability-loop')
    } else if (action === 'visual') {
      const out = safePath(parsed.args.out || path.join(cwd, '.tmp', 'visual-qa'))
      if (out === '') return { ok: false, text: 'visual 的 out 含非法字符' }
      psArgs.push('-OutDir', out)
    } else if (action === 'skill-status') {
      psArgs.push('-Workspace', cwd)
    }
    argv = { executable: 'powershell', argv: psArgs }
  } else {
    const pyArgs = [script]
    if (action === 'handoff-audit') {
      const slug = safeToken(parsed.args.slug || '')
      if (slug === '') return { ok: false, text: 'handoff-audit 需要 slug=<目录名>' }
      pyArgs.push('--workspace', safePath(parsed.args.workspace || cwd) || cwd, '--slug', slug)
    } else if (action === 'preflight') {
      const keyword = String(parsed.args.keyword || '').trim()
      const aliases = String(parsed.args.alias || '').trim().split(/\s+/).filter(Boolean)
      if (keyword === '') return { ok: false, text: 'preflight 需要 keyword=<模块名关键词>' }
      pyArgs.push('--project', safePath(parsed.args.project || cwd) || cwd, '--keyword', keyword)
      if (aliases.length > 0) pyArgs.push('--alias', ...aliases)
    }
    argv = { executable: cfg.pythonExecutable || 'python', argv: pyArgs }
  }

  const result = await runSpawn(ctx, { ...argv, cwd, timeoutMs: spec.timeoutMs, signal })
  return { ok: result.ok === true, text: formatResult(spec.label, result) }
}

function formatResult(label, result) {
  // 早退路径（没有 subprocess / 解释器解析失败 / spawn 抛错）只给了 text，直接返回它，
  // 不要把原因吞掉。
  if (typeof result.text === 'string' && result.text !== '') return clip(result.text, 6000)
  const lines = []
  const head = '[' + label + '] ' + (result.cancelled === true ? '已取消' : result.ok ? 'PASS' : 'FAIL')
    + (result.exitCode === undefined || result.exitCode === null ? '' : '（exit ' + result.exitCode + '）')
  lines.push(head)
  if (result.timedOut === true) lines.push('超时被中止。')
  if (result.failure !== '') lines.push('错误：' + result.failure)
  if (result.output !== undefined && result.output !== '') {
    // 只回最后 40 行，避免把长输出塞进会话
    const tail = String(result.output).split(/\r?\n/).slice(-40).join('\n')
    lines.push('')
    lines.push(tail)
  }
  return clip(lines.join('\n'), 6000)
}
