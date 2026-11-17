export const meta = {
  name: '1688-product-analysis',
  description: '1688 商品诊断工作流，覆盖多店异常商品、明确商品 ID、关键词搜索、评分选品、同款竞品对比、商品库建议与一键优化交接',
  whenToUse: '分析这个商品、商品诊断、商品表现分析、为什么商品没流量、商品优化建议、最该优化的商品、商品数据分析、多店铺异常商品、新品没流量怎么办、提供商品 ID 直接诊断、搜索商品、关键词搜索、圈选重点品、推荐商品、今日运营重点、选品、商品分层',
  phases: [
    { title: '确定体检商品', detail: '支持指定商品 ID，也能从异常商品、关键词搜索和经营评分中挑选商品' },
    { title: '查看经营表现', detail: '核对商品所属店铺，查看近期流量、成交、加购和转化表现' },
    { title: '对比优秀同款', detail: '对比同款标杆的商品素材、经营表现、流量来源、服务保障、口碑和热卖 SKU' },
    { title: '整理诊断报告', detail: '结合经营数据、同款差距和商品库建议，整理问题、影响及优化方向' },
    { title: '准备后续操作', detail: '报告完整展示后，再提供一键优化和自动商品体检入口' },
  ],
}

// ─── 工具函数（含错误容灾） ───
const CLI_SCRIPT = baseDir + '/cli.py'
const CLI_TIMEOUT_MS = 120000
const ITEM_DIAGNOSIS_CONTEXT_TIMEOUT_MS = 180000
const MAX_CLI_CONCURRENCY = 6
const PROBE_TIMEOUT_MS = 15000
const PYTHON_MISSING_MESSAGE = '本机未检测到可用的 Python 3 运行环境（已尝试 python3、python、py -3），请安装 Python 3 并加入 PATH 后重试'

// ─── 跨平台 Bash 通道 ───
// exec 已不提倡，所有子进程统一走 callTool('Bash')。Bash tool 只接受一条命令串，
// 因此把「重定向到临时文件 → 回显退出码 → 回显 stdout → 回显 stderr → 清理」拼成
// 一条命令，再由 parseBashOutput 还原成 { exitCode, stdout, stderr } 信封。
const BASH_STDERR_MARKER = '__WFSE__:'
const PY_HEREDOC_DELIMITER = '_WF_PYEOF_'
const BASE64_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
let shellDialectPromise = null

// Windows 上 python.org 安装器只提供 python.exe 与 py.exe，没有 python3，
// 硬编码 python3 会直接报“不是内部或外部命令”；mac/Linux 则通常只有 python3。
// 这里按顺序探测一次并缓存结果，之后所有 Python 调用都复用同一解释器。
const PYTHON_CANDIDATES = [
  { cmd: 'python3', prefixArgs: [] },
  { cmd: 'python', prefixArgs: [] },
  { cmd: 'py', prefixArgs: ['-3'] },
]
const PYTHON_VERSION_PROBE_PY = 'import sys; sys.stdout.write(str(sys.version_info[0]))'
let pythonRuntimePromise = null

let activeCliExecutions = 0
const pendingCliExecutions = []

async function withCliExecutionSlot(task) {
  if (activeCliExecutions < MAX_CLI_CONCURRENCY) {
    activeCliExecutions += 1
  } else {
    await new Promise(resolve => pendingCliExecutions.push(resolve))
  }

  try {
    return await task()
  } finally {
    const next = pendingCliExecutions.shift()
    if (next) next()
    else activeCliExecutions -= 1
  }
}

function stringifyToolOutput(raw) {
  if (typeof raw === 'string') return raw
  if (raw && typeof raw === 'object') {
    for (const key of ['raw', 'output', 'stdout']) {
      if (typeof raw[key] === 'string') return raw[key]
    }
    try { return JSON.stringify(raw) } catch { return String(raw) }
  }
  return String(raw == null ? '' : raw)
}

// cmd.exe 会把 %OS% 展开成 Windows_NT，bash/sh 不展开 %VAR% 而原样输出 %OS%。
// 探测的是「当前 shell 的方言」而不是操作系统：Windows 上若 Bash tool 实际走
// git-bash，结果为 posix，此时 cat/rm/$? 确实可用，判断依然正确。
// 不读 process.env：workflow VM 沙箱里 process 可能不可用（会恒判 posix，Windows
// 上全链路失败），而 mac/CI 上设了 TEMP 又会被反向误判成 Windows。
// 这一条必须裸调 callTool，因为 buildBashCommand 本身依赖探测结果。
function resolveShellDialect() {
  if (!shellDialectPromise) {
    shellDialectPromise = (async () => {
      try {
        let raw = await callTool('Bash', {
          command: 'echo %OS%',
          description: '检测执行环境',
          timeout: PROBE_TIMEOUT_MS,
        })
        // 框架竞态空返回会被 /Windows_NT/ 判否而误判 posix（Windows 上全链路崩溃），重试一次
        if (stringifyToolOutput(raw).trim() === '') {
          raw = await callTool('Bash', {
            command: 'echo %OS%',
            description: '检测执行环境',
            timeout: PROBE_TIMEOUT_MS,
          })
        }
        const dialect = /Windows_NT/i.test(stringifyToolOutput(raw)) ? 'cmd' : 'posix'
        log(`shell dialect resolved: ${dialect}`)
        return dialect
      } catch (error) {
        log(`shell dialect probe failed: ${String((error && error.message) || error)}`)
        return 'posix'
      }
    })()
  }
  return shellDialectPromise
}

// 只用于路径和短参数；数据类内容一律走 heredoc 或 base64，不裸进命令行。
function shellEscape(value, dialect) {
  const text = String(value)
  if (/^[A-Za-z0-9._\-\/:,=@]+$/.test(text)) return text
  if (dialect === 'cmd') return '"' + text.replace(/"/g, '""') + '"'
  return "'" + text.replace(/'/g, "'\\''") + "'"
}

function utf8Bytes(text) {
  const bytes = []
  for (const char of String(text)) {
    const code = char.codePointAt(0)
    if (code <= 0x7f) {
      bytes.push(code)
    } else if (code <= 0x7ff) {
      bytes.push(0xc0 | (code >> 6), 0x80 | (code & 0x3f))
    } else if (code <= 0xffff) {
      bytes.push(0xe0 | (code >> 12), 0x80 | ((code >> 6) & 0x3f), 0x80 | (code & 0x3f))
    } else {
      bytes.push(0xf0 | (code >> 18), 0x80 | ((code >> 12) & 0x3f), 0x80 | ((code >> 6) & 0x3f), 0x80 | (code & 0x3f))
    }
  }
  return bytes
}

// base64 输出集只有 A-Za-z0-9+/=，不含 % ! " ' & | < > ^ ( ) 与换行，
// 因此编码后的内容进命令行不会被 cmd 变量展开或转义吃掉。
function toBase64(bytes) {
  let encoded = ''
  for (let index = 0; index < bytes.length; index += 3) {
    const b0 = bytes[index]
    const b1 = bytes[index + 1]
    const b2 = bytes[index + 2]
    encoded += BASE64_ALPHABET[b0 >> 2]
    encoded += BASE64_ALPHABET[((b0 & 0x03) << 4) | ((b1 === undefined ? 0 : b1) >> 4)]
    encoded += b1 === undefined ? '=' : BASE64_ALPHABET[((b1 & 0x0f) << 2) | ((b2 === undefined ? 0 : b2) >> 6)]
    encoded += b2 === undefined ? '=' : BASE64_ALPHABET[b2 & 0x3f]
  }
  return encoded
}

// program 传已探测出的解释器（可带固定前置参数，如 py -3）。
// args[0] === '-c' 时按 Python 内联脚本处理：posix 走 heredoc，正文不必转义；
// cmd 没有 heredoc，也无法在一行命令里塞进换行，故把脚本 base64 后 exec 还原。
// 两种形式下额外参数都从 sys.argv[1] 开始，内联脚本按 sys.argv[1:] 取参即可。
function buildBashCommand(dialect, program, args, description, timeout = CLI_TIMEOUT_MS) {
  const isCmd = dialect === 'cmd'
  const argList = (Array.isArray(args) ? args : []).map(String)
  const tmpDir = isCmd ? '%TEMP%' : '/tmp'
  const sep = isCmd ? '\\' : '/'
  const id = `_wf${Date.now()}${Math.random().toString(36).slice(2, 5)}`
  const outFile = `${tmpDir}${sep}${id}_o`
  const errFile = `${tmpDir}${sep}${id}_e`
  let redirectedCmd
  if (argList[0] === '-c') {
    const script = argList[1] || ''
    const extraArgs = argList.slice(2).map(arg => shellEscape(arg, dialect)).join(' ')
    const argsPart = extraArgs ? ` ${extraArgs}` : ''
    redirectedCmd = isCmd
      ? `${program} -c "import base64;exec(base64.b64decode('${toBase64(utf8Bytes(script))}').decode())"${argsPart} > "${outFile}" 2> "${errFile}"`
      : `{ ${program} -${argsPart} << '${PY_HEREDOC_DELIMITER}'\n${script}\n${PY_HEREDOC_DELIMITER}\n} > "${outFile}" 2> "${errFile}"`
  } else {
    const plainCmd = [program, ...argList.map(arg => shellEscape(arg, dialect))].join(' ')
    redirectedCmd = `${plainCmd} > "${outFile}" 2> "${errFile}"`
  }
  // cmd.exe /c 对整条单行命令只做一次解析：同行的 setlocal enabledelayedexpansion 来不及生效，
  // !errorlevel! 会原样输出字面量（线上 win32 已观测到，导致严格版 parseBashOutput 全部判负）；
  // 而 %errorlevel% 在单行命令里又是解析期展开的陈旧值。可靠做法：把「执行 → 回显退出码 →
  // 回显 stdout/stderr → 清理」写成多行 .cmd 批处理再 call 执行——批处理逐行解析执行，
  // %errorlevel% 在自己的行上展开，拿到的就是上一条命令的真实退出码。
  // 脚本内容含引号/重定向/括号，用 echo 落盘要层层转义，故内容 base64 后由 python 写文件；
  // writer 与被探测/被执行的解释器用同一 program（探测场景自洽：候选存在则 writer 可用；
  // python 缺失时 writer 报错进 stderr，信封首行非数字，上层仍按失败处理，不会误判成功）。
  let command
  if (isCmd) {
    const wrapFile = `${tmpDir}${sep}${id}_w.cmd`
    const wrapper = [
      '@echo off',
      redirectedCmd,
      'echo %errorlevel%',
      `type "${outFile}"`,
      'echo.',
      `echo ${BASH_STDERR_MARKER}`,
      `type "${errFile}"`,
      `del /f /q "${outFile}" "${errFile}"`,
    ].join('\r\n') + '\r\n'
    command = `${program} -c "import base64;open(r'${wrapFile}','wb').write(base64.b64decode('${toBase64(utf8Bytes(wrapper))}'))" & call "${wrapFile}" & del /f /q "${wrapFile}"`
  } else {
    command = `${redirectedCmd}; _ec=$?; echo $_ec; cat "${outFile}"; printf '\\n${BASH_STDERR_MARKER}'; cat "${errFile}"; rm -f "${outFile}" "${errFile}"`
  }
  return { command, timeout, description: description || `执行 ${program}` }
}

function parseBashOutput(raw) {
  let text = stringifyToolOutput(raw)
  if (text.startsWith('Command:')) {
    const headerEnd = text.indexOf('\n\n')
    if (headerEnd >= 0) text = text.slice(headerEnd + 2)
  }
  const newlineIndex = text.indexOf('\n')
  const head = (newlineIndex >= 0 ? text.slice(0, newlineIndex) : text).trim()
  // 首行不是退出码说明包装命令没按预期执行（如 Bash tool 直接回错误对象），
  // 此时整体按失败处理，绝不能当成 exitCode 0 把错误文本当业务输出用。
  if (!/^-?\d+$/.test(head)) {
    return { exitCode: 1, stdout: '', stderr: text.trim() || 'CLI 子进程返回格式不可识别' }
  }
  const rest = newlineIndex >= 0 ? text.slice(newlineIndex + 1) : ''
  const marker = '\n' + BASH_STDERR_MARKER
  const markerIndex = rest.lastIndexOf(marker)
  return {
    exitCode: Number(head),
    stdout: markerIndex >= 0 ? rest.slice(0, markerIndex) : rest,
    stderr: markerIndex >= 0 ? rest.slice(markerIndex + marker.length) : '',
  }
}

function resolvePythonRuntime() {
  if (!pythonRuntimePromise) {
    pythonRuntimePromise = (async () => {
      const dialect = await resolveShellDialect()
      for (const candidate of PYTHON_CANDIDATES) {
        const program = [candidate.cmd, ...candidate.prefixArgs].join(' ')
        try {
          let raw = await callTool('Bash', buildBashCommand(
            dialect,
            program,
            ['-c', PYTHON_VERSION_PROBE_PY],
            '检测 Python 运行环境',
            PROBE_TIMEOUT_MS
          ))
          // 端侧框架小概率让首个 callTool 返回空（竞态，跨平台），探测恰好是首个调用；
          // 空返回时原地重试同一候选一次，避免误杀可用解释器后错报「未检测到 Python」
          if (stringifyToolOutput(raw).trim() === '') {
            raw = await callTool('Bash', buildBashCommand(
              dialect,
              program,
              ['-c', PYTHON_VERSION_PROBE_PY],
              '检测 Python 运行环境',
              PROBE_TIMEOUT_MS
            ))
          }
          const probe = parseBashOutput(raw)
          // Windows 商店的假 python3.exe「存在」但不是 Python（打印 Python was not
          // found 并返回非零码），只判断命令是否存在会选中这个 stub，
          // 因此必须同时校验退出码为 0 且版本号以 3 开头。
          if (probe.exitCode === 0 && probe.stdout.trim().startsWith('3')) {
            log(`python runtime resolved: ${program}`)
            return { program }
          }
          log(`python probe rejected (${program}): exitCode=${probe.exitCode}`)
        } catch (error) {
          log(`python probe failed (${program}): ${String((error && error.message) || error)}`)
        }
      }
      log('python runtime not found')
      return null
    })()
  }
  return pythonRuntimePromise
}

// 统一的 Python 执行入口：解释器缺失时返回统一信封（退出码 127 + 商家可读文案），
// 由调用方走既有失败分支，不把“'python3' 不是内部或外部命令”泄露到对话。
async function runPython(pyArgs, { timeout = CLI_TIMEOUT_MS, description = '' } = {}) {
  const runtime = await resolvePythonRuntime()
  if (!runtime) {
    return { exitCode: 127, stdout: '', stderr: PYTHON_MISSING_MESSAGE }
  }
  const dialect = await resolveShellDialect()
  const built = buildBashCommand(
    dialect,
    runtime.program,
    Array.isArray(pyArgs) ? pyArgs : [],
    description,
    timeout
  )
  return parseBashOutput(await callTool('Bash', built))
}

function executeCli(command, cliArgs = []) {
  return withCliExecutionSlot(() => runPython(
    [CLI_SCRIPT, command, ...(Array.isArray(cliArgs) ? cliArgs : [])],
    {
      timeout: command === 'alibaba.1688.get.item.diagnosis.context'
        ? ITEM_DIAGNOSIS_CONTEXT_TIMEOUT_MS
        : CLI_TIMEOUT_MS,
      description: `查询 ${command}`,
    }
  ))
}

function normalizeCliResult(parsed) {
  const result = { ...parsed }
  let data = result.data

  for (let depth = 0; depth < 5; depth++) {
    const isObject = data && typeof data === 'object' && !Array.isArray(data)
    const isBusinessWrapper = isObject && 'success' in data && 'data' in data
    const isSingletonDataWrapper = isObject
      && Object.keys(data).length === 1
      && Object.prototype.hasOwnProperty.call(data, 'data')
    if (!isBusinessWrapper && !isSingletonDataWrapper) break
    if (isBusinessWrapper && data.success === false) {
      const extInfoMessage = typeof data.extInfo === 'string' ? data.extInfo : ''
      return {
        ...result,
        success: false,
        error: data.message || data.msgInfo || data.msgCode || extInfoMessage || '业务数据暂不可用',
        data: {},
      }
    }
    data = data.data
  }

  result.data = data
  if (!result.success && !result.error) {
    result.error = result.message
      || result.msgInfo
      || result.msgCode
      || (result.markdown || '').replace(/^❌\s*/, '')
      || '未知错误'
  }
  return result
}

async function runCli(command, cliArgs) {
  let result
  try {
    result = await executeCli(command, cliArgs)
  } catch (error) {
    const errMsg = error?.message || String(error || 'CLI 子进程调用失败')
    log(`CLI ${command} failed: ${errMsg}`)
    return { success: false, error: errMsg, command, data: {} }
  }
  if (result.exitCode !== 0) {
    const errMsg = (result.stderr || '').slice(0, 300).trim()
    log(`CLI ${command} failed: ${errMsg}`)
    return { success: false, error: errMsg, command, data: {} }
  }
  try {
    const parsed = JSON.parse(result.stdout)
    return normalizeCliResult(parsed)
  }
  catch { return { success: true, markdown: result.stdout, data: {} } }
}

function validateCorrectedArgs(correctedArgs, cliHelp, originalArgs = []) {
  if (!Array.isArray(correctedArgs)) {
    return { valid: false, reason: 'correctedArgs 必须是字符串数组' }
  }
  const helpOptions = String(cliHelp || '').match(/--[A-Za-z][A-Za-z0-9_-]*/g)
  const allowedOptions = new Set(Array.isArray(helpOptions) ? helpOptions : [])
  let canAcceptValue = false
  for (const token of correctedArgs) {
    if (typeof token !== 'string') {
      return { valid: false, reason: 'correctedArgs 只能包含字符串' }
    }
    if (token.startsWith('--')) {
      if (token === '--help' || !allowedOptions.has(token)) {
        return { valid: false, reason: `不允许的参数: ${token}` }
      }
      canAcceptValue = true
      continue
    }
    if (token.startsWith('-') || !canAcceptValue) {
      return { valid: false, reason: `参数值缺少已知长选项: ${token}` }
    }
    canAcceptValue = false
  }

  const collectKnownOptionValues = args => {
    const values = new Map()
    for (let index = 0; index < args.length - 1; index++) {
      const option = args[index]
      const value = args[index + 1]
      if (
        typeof option === 'string'
        && allowedOptions.has(option)
        && typeof value === 'string'
        && !value.startsWith('--')
      ) {
        values.set(option, value)
        index += 1
      }
    }
    return values
  }
  const originalOptionValues = collectKnownOptionValues(Array.isArray(originalArgs) ? originalArgs : [])
  const correctedOptionValues = collectKnownOptionValues(correctedArgs)
  for (const [option, value] of originalOptionValues) {
    if (correctedOptionValues.get(option) !== value) {
      return { valid: false, reason: `不允许改写原始参数 ${option}` }
    }
  }
  const originalStandaloneOptions = new Set()
  const safeOriginalArgs = Array.isArray(originalArgs) ? originalArgs : []
  for (let index = 0; index < safeOriginalArgs.length; index++) {
    const option = safeOriginalArgs[index]
    const nextToken = safeOriginalArgs[index + 1]
    if (
      typeof option === 'string'
      && allowedOptions.has(option)
      && (typeof nextToken !== 'string' || nextToken.startsWith('--'))
    ) {
      originalStandaloneOptions.add(option)
    }
  }
  for (const option of originalStandaloneOptions) {
    if (!correctedArgs.includes(option)) {
      return { valid: false, reason: `不允许删除原始参数 ${option}` }
    }
  }
  return { valid: true, args: correctedArgs }
}

// 判断是否为后端/网络类错误（直接重试即可，无需大模型分析）
function isBackendError(errorMsg) {
  const backendPatterns = ['BACKEND_ERROR', '后端服务', '服务调用失败', '网络异常', 'HSF', 'timeout', 'ETIMEDOUT', 'ECONNREFUSED', '服务异常']
  return backendPatterns.some(p => (errorMsg || '').includes(p))
}

function isOfferIdentityMismatch(errorMsg) {
  const identityPatterns = [
    '不在当前账号的多店绑定关系内',
    '不归属当前账号',
    '商品不归属',
    '归属校验失败',
    '无权操作商品',
    '没有权限操作商品',
    '是否归属当前账号',
  ]
  const normalized = String(errorMsg || '').toLowerCase()
  return identityPatterns.some(pattern => normalized.includes(pattern.toLowerCase()))
}

function isTerminalBusinessError(errorMsg) {
  const terminalPatterns = [
    '不在当前账号的多店绑定关系内',
    '不归属当前账号',
    '商品不归属',
    '归属校验失败',
    '无权操作商品',
    '无权限',
    '未授权',
    'unauthorized',
    'forbidden',
    '商品不存在',
    '未找到商品',
    'AK 未配置',
  ]
  return terminalPatterns.some(p => (errorMsg || '').toLowerCase().includes(p.toLowerCase()))
}

async function runCliWithSmartRetry(command, cliArgs, { maxRetries = 3, commandDesc = '' } = {}) {
  let lastResult = await runCli(command, cliArgs)
  if (lastResult.success) return lastResult
  if (command === 'alibaba.1688.get.offer.data' && isOfferLookupMiss(lastResult)) return lastResult

  let currentError = lastResult.error || ''
  if (isTerminalBusinessError(currentError)) {
    log(`${commandDesc || command} terminal business error: ${currentError}`)
    return { ...lastResult, _retryExhausted: true, _reason: currentError }
  }

  // ─── 路径 A：后端/网络异常 → 直接重试相同命令（不浪费 token 做分析） ───
  if (isBackendError(currentError)) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      log(`${commandDesc || command} backend retry ${attempt}/${maxRetries}`)
      await new Promise(r => setTimeout(r, 1000 * attempt)) // 递增等待
      lastResult = await runCli(command, cliArgs)
      if (lastResult.success) {
        log(`${commandDesc || command} backend retry succeeded`)
        return lastResult
      }
      currentError = lastResult.error || ''
      if (isTerminalBusinessError(currentError)) {
        log(`${commandDesc || command} terminal business error: ${currentError}`)
        return { ...lastResult, _retryExhausted: true, _reason: currentError }
      }
    }
    log(`${commandDesc || command} backend retries exhausted`)
    return { ...lastResult, _retryExhausted: true, _reason: '后端服务持续异常' }
  }

  // ─── 路径 B：其他异常 → 大模型智能分析重试 ───
  let helpResult
  try {
    helpResult = await executeCli(command, ['--help'])
  } catch (error) {
    helpResult = { exitCode: 1, stdout: '', stderr: error?.message || String(error || 'CLI 子进程调用失败') }
  }
  const cliHelp = helpResult.exitCode === 0 ? helpResult.stdout.slice(0, 1000) : ''

  let rejectionHistory = '' // 记录被拒绝的命令，注入给下一次 LLM 调用

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    log(`${commandDesc || command} retry analysis ${attempt}/${maxRetries}`)
    const fix = parseAgentResult(await agent(
      `你是一个 CLI 调试助手。以下 python CLI 子命令执行失败，请分析原因并给出修正后的参数数组。\n\n` +
      `## 当前子命令\n${command}\n\n` +
      `## 当前参数\n\`\`\`json\n${JSON.stringify(cliArgs || [])}\n\`\`\`\n\n` +
      `## 错误输出\n\`\`\`\n${currentError}\n\`\`\`\n\n` +
      (cliHelp ? `## CLI Help（该命令支持的全部参数）\n\`\`\`\n${cliHelp}\n\`\`\`\n\n` : '') +
      (rejectionHistory ? `## 上次生成的参数被拒绝\n${rejectionHistory}\n\n` : '') +
      `## 严格约束\n` +
      `1. correctedArgs 只能返回当前子命令之后的参数数组，不得包含 python3、脚本路径或子命令\n` +
      `2. 每个参数名必须是 CLI Help 中列出的 --长选项；参数值只能紧跟在对应选项后\n` +
      `3. 禁止返回 --help、完整命令、位置参数或任何 shell 操作符\n` +
      `4. 当前参数中已经属于 CLI Help 的选项及其值必须原样保留，只允许补充缺失选项或替换无效选项\n` +
      `5. 如果是环境问题（AK 未配置、依赖缺失、服务端错误等）无法通过改参数修复，shouldRetry 设为 false`,
      {
        label: `${command}-error-analysis-${attempt}`,
        schema: {
          type: 'object',
          properties: {
            reason: { type: 'string', description: '错误原因分析' },
            shouldRetry: { type: 'boolean', description: '是否值得用修正命令重试' },
            correctedArgs: {
              type: 'array',
              items: { type: 'string' },
              description: '仅当前子命令之后的修正参数，例如 ["--offer_id", "123"]',
            },
          },
          required: ['reason', 'shouldRetry'],
        },
      }
    )) || {}

    log(`${command} retry analysis: ${JSON.stringify(fix)}`)
    if (!fix.shouldRetry || !Array.isArray(fix.correctedArgs)) {
      return { ...lastResult, _retryExhausted: true, _reason: fix.reason }
    }

    const validation = validateCorrectedArgs(fix.correctedArgs, cliHelp, cliArgs)
    if (!validation.valid) {
      log(`Reject correctedArgs: ${JSON.stringify(fix.correctedArgs)}`)
      rejectionHistory = `被拒绝的参数: \`${JSON.stringify(fix.correctedArgs)}\`\n拒绝原因: ${validation.reason}。请严格按格式重新生成。`
      continue
    }
    rejectionHistory = ''

    log(`Retry ${command} with corrected arguments: ${JSON.stringify(validation.args)}`)
    let retryResult
    try {
      retryResult = await executeCli(command, validation.args)
    } catch (error) {
      retryResult = { exitCode: 1, stdout: '', stderr: error?.message || String(error || 'CLI 子进程调用失败') }
    }
    if (retryResult.exitCode === 0) {
      try {
        const normalized = normalizeCliResult(JSON.parse(retryResult.stdout))
        if (normalized.success) {
          log(`${commandDesc || command} corrected command succeeded`)
          return normalized
        }
        lastResult = normalized
        currentError = lastResult.error || ''
        if (isTerminalBusinessError(currentError)) {
          log(`${commandDesc || command} terminal business error: ${currentError}`)
          return { ...lastResult, _retryExhausted: true, _reason: currentError }
        }
        continue
      }
      catch { return { success: true, markdown: retryResult.stdout, data: {} } }
    }
    lastResult = {
      success: false,
      error: (retryResult.stderr || '').slice(0, 300).trim(),
      command,
      data: {},
    }
    currentError = lastResult.error || ''
    if (isTerminalBusinessError(currentError)) {
      log(`${commandDesc || command} terminal business error: ${currentError}`)
      return { ...lastResult, _retryExhausted: true, _reason: currentError }
    }
  }

  log(`${commandDesc || command} corrected command retries exhausted`)
  return { ...lastResult, _retryExhausted: true }
}

async function executeReportJobs(reportJobs, runParallel, onProgress = () => {}, concurrency = 5) {
  if (reportJobs.length === 0) return []

  let completedCount = 0
  const outcomes = new Array(reportJobs.length)
  const normalizedConcurrency = Math.max(1, Math.floor(concurrency || 1))
  const workerCount = Math.min(Math.max(1, normalizedConcurrency), reportJobs.length)
  let nextIndex = 0

  const recordOutcome = async (jobIndex, outcome) => {
    if (outcomes[jobIndex] !== undefined) return
    outcomes[jobIndex] = outcome
    completedCount += 1
    try {
      await onProgress(completedCount, reportJobs.length, outcome, reportJobs[jobIndex])
    } catch (error) {
      if (typeof log === 'function') {
        log(`report progress callback failed: ${String((error && error.message) || error)}`)
      }
    }
  }

  const workers = Array.from({ length: workerCount }, () => async () => {
    while (nextIndex < reportJobs.length) {
      const jobIndex = nextIndex
      nextIndex += 1
      const job = reportJobs[jobIndex]
      let outcome
      try {
        // Workflow 的 agent/callTool 调用必须直接 await；再包 Promise.race/then
        // 会让运行时提前得到 undefined，真实任务虽继续执行却无法回收 PRODUCT。
        outcome = await job.run()
      } catch (error) {
        if (typeof log === 'function') {
          log(`report job failed offerId=${job.offerId}: ${String((error && error.message) || error)}`)
        }
        outcome = {
          success: false,
          offerId: job.offerId,
          ordinal: job.ordinal,
          errorPreset: SECTION_ERROR_PRESET.AGENT_FAILED,
          reason: error?.message || '诊断生成失败',
        }
      }
      await recordOutcome(jobIndex, outcome)
    }
  })

  try {
    await runParallel(workers)
  } catch (error) {
    if (typeof log === 'function') {
      log(`report parallel scheduler failed: ${String((error && error.message) || error)}`)
    }
    for (let jobIndex = 0; jobIndex < reportJobs.length; jobIndex += 1) {
      if (outcomes[jobIndex] !== undefined) continue
      const job = reportJobs[jobIndex]
      await recordOutcome(jobIndex, {
        success: false,
        offerId: job.offerId,
        ordinal: job.ordinal,
        errorPreset: SECTION_ERROR_PRESET.AGENT_FAILED,
        reason: '诊断生成失败',
      })
    }
  }

  return outcomes
}

function hasUsableOfferData(result) {
  if (!result?.success) return false
  const data = result.data
  if (data === null || data === undefined) return false
  if (data && typeof data === 'object' && data.success === false) return false
  if (Array.isArray(data)) return data.length > 0
  if (typeof data === 'object') return Object.keys(data).length > 0
  return String(data).trim().length > 0
}

function isOfferLookupMiss(result) {
  if (hasUsableOfferData(result)) return false

  if (result?.failureType === 'offer_not_found' || result?.data?.failureType === 'offer_not_found') {
    return true
  }

  const message = [
    result?.error,
    result?.markdown,
    typeof result?.data === 'string' ? result.data : '',
  ].filter(Boolean).join(' ')

  // 权限/归属错误经常被底层统一包装成 BACKEND_ERROR；应先触发跨店查找，
  // 只有纯网络、超时或服务异常才按后端错误处理，避免错误地跳过绑定店铺兜底。
  if (isOfferIdentityMismatch(message)) return true
  if (isBackendError(message)) return false
  if (result?.success) return true

  const normalized = message.toLowerCase()
  const missPatterns = [
    '商品数据为空', '未找到', '找不到', '不存在', '归属', '当前账号',
    '无权', '没有权限', 'permission_denied', 'offer not found',
  ]
  return missPatterns.some(pattern => normalized.includes(pattern))
}

const itemDiagnosisContextPromiseByOfferId = new Map()

function adaptEnhancementResult(enhancement) {
  const status = String(enhancement?.status || ENHANCEMENT_STATUS.TOOL_FAILED)
  const consumable = status === ENHANCEMENT_STATUS.SUCCESS || status === ENHANCEMENT_STATUS.NO_DATA
  return {
    success: consumable,
    status,
    error: consumable ? '' : (enhancement?.errorMessage || '增强数据暂不可用'),
    errorCode: enhancement?.errorCode || '',
    data: enhancement?.data && typeof enhancement.data === 'object' ? enhancement.data : {},
  }
}

function hasNonemptyDiagnosisModule(value) {
  if (Array.isArray(value)) return value.length > 0
  if (value && typeof value === 'object') return Object.keys(value).length > 0
  return String(value || '').trim().length > 0
}

function adaptItemDiagnosisContext(result, offerId) {
  const failureType = String(result?.data?.failureType || result?.failureType || '').trim()
  if (!result?.success) {
    const failedResult = {
      ...result,
      success: false,
      failureType,
      data: result?.data && typeof result.data === 'object' ? result.data : {},
    }
    return {
      offerLookup: { result: failedResult, loginId: '', shopName: '', failureType },
      sameOfferResult: adaptEnhancementResult(),
      diagnosisActionResult: adaptEnhancementResult(),
      context: null,
    }
  }

  const context = result?.data && typeof result.data === 'object' ? result.data : {}
  const itemId = String(context.itemId || '')
  const offerData = context.offerData && typeof context.offerData === 'object'
    ? context.offerData
    : {}
  if (
    itemId !== String(offerId)
    || !String(context.loginId || '').trim()
    || !hasNonemptyDiagnosisModule(offerData.profile)
    || !hasNonemptyDiagnosisModule(offerData.performance)
  ) {
    const invalidResult = {
      success: false,
      error: '聚合商品诊断上下文缺少可验证的基础数据',
      failureType: 'data_unverifiable',
      data: { failureType: 'data_unverifiable', itemId: String(offerId) },
    }
    return {
      offerLookup: { result: invalidResult, loginId: '', shopName: '', failureType: 'data_unverifiable' },
      sameOfferResult: adaptEnhancementResult(),
      diagnosisActionResult: adaptEnhancementResult(),
      context: null,
    }
  }

  return {
    offerLookup: {
      result: { success: true, data: offerData },
      loginId: String(context.loginId || '').trim(),
      shopName: String(context.shopName || '').trim(),
      failureType: '',
    },
    sameOfferResult: adaptEnhancementResult(context.enhancements?.competition),
    diagnosisActionResult: adaptEnhancementResult(context.enhancements?.diagnosisActions),
    context,
  }
}

function queryItemDiagnosisContext(offerId) {
  const normalizedOfferId = String(offerId || '').trim()
  if (!itemDiagnosisContextPromiseByOfferId.has(normalizedOfferId)) {
    const contextPromise = runCli('alibaba.1688.get.item.diagnosis.context', [
      '--item_id',
      normalizedOfferId,
    ]).then(result => adaptItemDiagnosisContext(result, normalizedOfferId))
    itemDiagnosisContextPromiseByOfferId.set(normalizedOfferId, contextPromise)
  }
  return itemDiagnosisContextPromiseByOfferId.get(normalizedOfferId)
}

function fillTargetFromDiagnosisContext(target, context) {
  if (!target || !context) return target
  const resolvedLoginId = String(context.loginId || '').trim()
  const resolvedShopName = String(context.shopName || '').trim()
  if (resolvedLoginId) target.loginId = resolvedLoginId
  if (resolvedShopName) target.shopName = resolvedShopName
  if (!target.title) target.title = String(context.title || '').trim()
  const resolvedImageUrl = normalizeCandidateImageUrl(context.imageUrl)
  if (resolvedImageUrl) target.imageUrl = resolvedImageUrl
  return target
}

function buildProductDiagnosisTiming(inputTiming, taskStartedAt, inputsReadyAt, reportReadyAt) {
  const elapsed = value => {
    const normalizedValue = Number(value)
    return Number.isFinite(normalizedValue) ? Math.max(0, normalizedValue) : 0
  }
  return {
    offerDataMs: elapsed(inputTiming?.offerDataMs),
    enhancementMs: elapsed(inputTiming?.enhancementMs),
    enhancementReadyMs: elapsed(inputTiming?.enhancementReadyMs),
    inputsReadyMs: elapsed(inputsReadyAt - taskStartedAt),
    agentMs: elapsed(reportReadyAt - inputsReadyAt),
    totalMs: elapsed(reportReadyAt - taskStartedAt),
  }
}

async function queryProductDiagnosisInputs(target, taskStartedAt = Date.now()) {
  const aggregate = await queryItemDiagnosisContext(target.offerId)
  const inputsReadyAt = Date.now()
  fillTargetFromDiagnosisContext(target, aggregate.context)
  const elapsed = Math.max(0, inputsReadyAt - taskStartedAt)
  return {
    offerLookup: aggregate.offerLookup,
    sameOfferResult: aggregate.sameOfferResult,
    diagnosisActionResult: aggregate.diagnosisActionResult,
    timing: {
      offerDataMs: elapsed,
      enhancementMs: elapsed,
      enhancementReadyMs: elapsed,
      inputsReadyMs: elapsed,
    },
    inputsReadyAt,
  }
}

async function hydrateDiagnosisTargetsForCatalog(targets, runParallel, concurrency = 5) {
  const hydrationJobs = (Array.isArray(targets) ? targets : []).map((target, ordinal) => ({
    offerId: target.offerId,
    ordinal,
    run: async () => {
      const aggregate = await queryItemDiagnosisContext(target.offerId)
      fillTargetFromDiagnosisContext(target, aggregate.context)
      return { success: Boolean(aggregate.context), offerId: target.offerId, ordinal }
    },
  }))
  await executeReportJobs(hydrationJobs, runParallel, () => {}, concurrency)
  return targets
}

// Windows 没有 cat，统一用 Python 读；按字节输出避开本地编码与换行转换。
// 不用 cmd 的 type：references/*.md 全是中文，而 cmd 默认代码页是 936/437，
// type 输出 UTF-8 文件会乱码。
const READ_TEXT_PY = [
  'import sys',
  "with open(sys.argv[1], 'rb') as f:",
  '    sys.stdout.buffer.write(f.read())',
].join('\n')

async function readRef(filename) {
  let result
  try {
    result = await runPython(
      ['-c', READ_TEXT_PY, baseDir + '/references/' + filename],
      { timeout: CLI_TIMEOUT_MS, description: `读取分析标准 ${filename}` }
    )
  } catch {
    return ''
  }
  return result.exitCode === 0 ? result.stdout : ''
}

// ─── 辅助函数 ───

/**
 * 从 showInteraction 返回结果中提取第一个 answer
 * Desktop 实际格式:
 *   - type='card' → { data: [{ question, answer }] }  (对象数组)
 *   - type='input' → { data: ['用户输入的文本'] }      (字符串数组)
 */
function extractAnswerFromInteraction(result) {
  if (!result) return ''
  const data = result.data
  if (!Array.isArray(data) || data.length === 0) return ''
  const first = data[0]
  // input 类型: data 直接是字符串数组 ['answer']
  if (typeof first === 'string') return first.trim()
  // card 类型: data 是对象数组 [{ question, answer }]
  if (first && typeof first === 'object' && 'answer' in first) {
    const answer = first.answer
    return typeof answer === 'string' ? answer.trim() : (answer ?? '')
  }
  return ''
}

function getInteractionFailureReason(result) {
  const failureText = /WATCHDOG_TIMEOUT|Interaction watchdog timeout/i
  const seen = new Set()
  const inspect = value => {
    if (typeof value === 'string') {
      return failureText.test(value)
        || /["']?state["']?\s*[:=]\s*["']?error/i.test(value)
        || /["']?success["']?\s*[:=]\s*false/i.test(value)
    }
    if (!value || typeof value !== 'object') return false
    if (seen.has(value)) return false
    seen.add(value)
    if (value.success === false || String(value.state || '').toLowerCase() === 'error') return true
    return Object.values(value).some(inspect)
  }
  return inspect(result) ? '交互组件暂时不可用' : ''
}

async function safeShowInteraction(spec, options) {
  try {
    const result = await showInteraction(spec, options)
    const reason = getInteractionFailureReason(result)
    return { ok: !reason, result, reason }
  } catch {
    log('交互组件调用失败，已安全降级')
    return { ok: false, result: undefined, reason: '交互组件暂时不可用' }
  }
}

function parseManualOfferIds(input) {
  const matches = String(input || '').match(/\d{10,}/g) || []
  return Array.from(new Set(matches))
}

// ─── agent 返回值兜底解析（对标 shop-health-check） ───

/**
 * 统一处理 agent() 返回值：
 * - object → 直接返回
 * - string → 尝试提取 JSON；失败则用正则从 Markdown 文本中提取诊断字段
 * - null/undefined → 返回 null
 */
function parseAgentResult(raw) {
  if (raw && typeof raw === 'object' && !Array.isArray(raw)) return raw
  if (typeof raw === 'string') {
    // 第一优先：从 ```json ``` 代码块中提取
    const m = raw.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/)
    if (m) {
      try { return JSON.parse(m[1].trim()) } catch {}
    }
    // 第二优先：找最外层 { ... } 尝试 JSON.parse
    const start = raw.indexOf('{')
    const end = raw.lastIndexOf('}')
    if (start >= 0 && end > start) {
      const candidate = raw.substring(start, end + 1)
      try { return JSON.parse(candidate) } catch {}

      // ★ 第二优先-B：JSON.parse 失败但文本含 "report" 字段
      //   说明模型输出了 JSON 结构但含真实换行导致 parse 失败
      //   尝试用正则提取 report 字段值
      if (candidate.includes('"report"')) {
        const result = _extractReportFromMalformedJson(candidate)
        if (result) return result
      }
    }
    // 第三优先（兜底）：将纯文本视为 report，用正则提取 actionKeywords
    return _extractDiagnosisFromMarkdown(raw)
  }
  return null
}

/**
 * 诊断报告专用：从 agent() 返回值中提取纯 Markdown 报告 + 扫描关键词
 *
 * 设计思路：保留 schema 约束输出，但用此函数替代 parseAgentResult 处理诊断报告，
 * 解决后者缺少 JSON 守卫的问题。对齐 shop-health-check 的 parseAgentResult 的 JSON 提取逻辑。
 *
 * 处理三种 agent() 返回形态：
 *   1. object（schema FC 成功，主路径）→ 取 .report 字段
 *   2. string（schema FC 失败）→ 用 indexOf 定位 JSON 并提取 report
 *   3. null → fallback
 */
function extractReportDirect(raw) {
  const KNOWN_KEYWORDS = [
    '主图', '图片', '白底图', '视频', '视觉素材',
    '标题', '关键词', 'SEO', '搜索词', '类目词',
    '详情页', '价格', 'SKU', '规格', '运费',
    '违规', '滞销', '库存', '评价', '复购',
  ]
  const FALLBACK = {
    report: '诊断数据不足，无法生成报告',
    recommendations: [],
    actionKeywords: [],
    actionCandidates: [],
    competitionAnalysis: null,
  }

  // 情况 1：agent() 返回 object（schema FC 成功，主路径）
  if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
    const report = raw.report || raw.content || ''
    if (report.length >= 30) {
      const actionKeywords = (Array.isArray(raw.actionKeywords) && raw.actionKeywords.length > 0)
        ? raw.actionKeywords
        : KNOWN_KEYWORDS.filter(kw => report.includes(kw))
      const actionCandidates = Array.isArray(raw.actionCandidates) ? raw.actionCandidates : []
      const recommendations = Array.isArray(raw.recommendations) ? raw.recommendations : []
      const competitionAnalysis = raw.competitionAnalysis && typeof raw.competitionAnalysis === 'object'
        ? raw.competitionAnalysis
        : null
      return { report, recommendations, actionKeywords, actionCandidates, competitionAnalysis }
    }
    return FALLBACK
  }

  // 情况 2：agent() 返回 null/undefined
  if (!raw || typeof raw !== 'string') return FALLBACK

  let text = raw.trim()

  // 情况 3：从 ```json ``` 代码块中提取（对齐 shop-health-check parseAgentResult）
  const codeBlockMatch = text.match(/```(?:json|markdown)?\s*\n?([\s\S]*?)\n?```/)
  if (codeBlockMatch) {
    text = codeBlockMatch[1].trim()
  }

  // 情况 4：文本中包含 JSON 结构 → 尝试提取 report 字段
  // 使用 indexOf 而非 startsWith，兼容 "json " 前缀、代码块残留等情况（对齐 shop-health-check）
  const jsonStart = text.indexOf('{')
  const jsonEnd = text.lastIndexOf('}')
  if (jsonStart >= 0 && jsonEnd > jsonStart && text.includes('"report"')) {
    const jsonCandidate = text.substring(jsonStart, jsonEnd + 1)

    // 第一层：尝试 JSON.parse（如果 \n 是转义序列则会成功）
    try {
      const parsed = JSON.parse(jsonCandidate)
      if (parsed.report && parsed.report.length >= 30) {
        const kws = (Array.isArray(parsed.actionKeywords) && parsed.actionKeywords.length > 0)
          ? parsed.actionKeywords
          : KNOWN_KEYWORDS.filter(kw => parsed.report.includes(kw))
        log(`extractReportDirect: JSON.parse 成功, report.length=${parsed.report.length}`)
        return {
          report: parsed.report,
          recommendations: Array.isArray(parsed.recommendations) ? parsed.recommendations : [],
          actionKeywords: kws,
          actionCandidates: Array.isArray(parsed.actionCandidates) ? parsed.actionCandidates : [],
          competitionAnalysis: parsed.competitionAnalysis && typeof parsed.competitionAnalysis === 'object'
            ? parsed.competitionAnalysis
            : null,
        }
      }
    } catch {
      try {
        const repaired = JSON.parse(escapeLiteralNewlinesInJsonStrings(jsonCandidate))
        if (repaired.report && repaired.report.length >= 30) {
          const kws = (Array.isArray(repaired.actionKeywords) && repaired.actionKeywords.length > 0)
            ? repaired.actionKeywords
            : KNOWN_KEYWORDS.filter(kw => repaired.report.includes(kw))
          log(`extractReportDirect: 修复 JSON 字符串换行后解析成功, report.length=${repaired.report.length}`)
          return {
            report: repaired.report,
            recommendations: Array.isArray(repaired.recommendations) ? repaired.recommendations : [],
            actionKeywords: kws,
            actionCandidates: Array.isArray(repaired.actionCandidates) ? repaired.actionCandidates : [],
            competitionAnalysis: repaired.competitionAnalysis && typeof repaired.competitionAnalysis === 'object'
              ? repaired.competitionAnalysis
              : null,
          }
        }
      } catch {}
    }

    // 第二层：JSON.parse 失败（含真实换行）→ 正则提取 report 值
    const extracted = _extractReportFromMalformedJson(jsonCandidate)
    if (extracted && extracted.report && extracted.report.length >= 30) {
      return extracted
    }

    // 第三层：去掉 JSON 包装壳，提取纯文本内容
    const reportFieldMatch = jsonCandidate.match(/"report"\s*:\s*"([\s\S]*)/)
    if (reportFieldMatch) {
      let content = reportFieldMatch[1]
      const tailCut = content.lastIndexOf('",')
      if (tailCut > 30) content = content.substring(0, tailCut)
      content = content.replace(/\\n/g, '\n').replace(/\\"/g, '"')
      if (content.length >= 30) {
        const kws = KNOWN_KEYWORDS.filter(kw => content.includes(kw))
        log(`extractReportDirect: 从 JSON 壳中提取 report 成功, length=${content.length}`)
        return { report: content, recommendations: [], actionKeywords: kws, actionCandidates: [], competitionAnalysis: null }
      }
    }
  }

  // 情况 5：正常路径 — 纯 Markdown 文本（最常见）
  if (text.length < 30) return FALLBACK

  const actionKeywords = KNOWN_KEYWORDS.filter(kw => text.includes(kw))
  log(`extractReportDirect: 纯文本路径成功, report.length=${text.length}, actionKeywords=${JSON.stringify(actionKeywords)}`)
  return { report: text, recommendations: [], actionKeywords, actionCandidates: [], competitionAnalysis: null }
}

/**
 * 从纯 Markdown 诊断报告文本中提取结构化字段
 * 适用于模型无视 schema 直接输出 Markdown 叙述的场景
 */
function _extractDiagnosisFromMarkdown(text) {
  if (!text || text.length < 30) return null

  // 整段文本作为 report（模型实际已输出了完整报告，只是没走 function calling）
  const report = text.trim()

  // 从文本中提取 actionKeywords —— 扫描已知优化方向关键词
  const KNOWN_KEYWORDS = [
    '主图', '图片', '白底图', '视频', '视觉素材',
    '标题', '关键词', 'SEO', '搜索词', '类目词',
    '详情页', '价格', 'SKU', '规格', '运费',
    '违规', '滞销', '库存', '评价', '复购',
  ]
  const actionKeywords = KNOWN_KEYWORDS.filter(kw => text.includes(kw))

  // 如果连一个关键词都没提取到，给一个通用兜底
  log(`parseAgentResult: 正则兜底提取成功 report.length=${report.length}, actionKeywords=${JSON.stringify(actionKeywords)}`)
  return { report, actionKeywords, actionCandidates: [] }
}

function escapeLiteralNewlinesInJsonStrings(text) {
  let output = ''
  let inString = false
  let escaped = false
  for (const char of String(text || '')) {
    if (!inString) {
      output += char
      if (char === '"') inString = true
      continue
    }
    if (escaped) {
      output += char
      escaped = false
      continue
    }
    if (char === '\\') {
      output += char
      escaped = true
      continue
    }
    if (char === '"') {
      output += char
      inString = false
      continue
    }
    if (char === '\n') {
      output += '\\n'
      continue
    }
    if (char === '\r') {
      output += '\\r'
      continue
    }
    output += char
  }
  return output
}

/**
 * 从含真实换行的伪 JSON 文本中提取 report 字段值
 * 适用于：JSON.parse 失败但文本确实是 JSON 结构（含有 "report" key）
 * 原理：利用 "actionKeywords" 作为右边界锚点定位 report 值的起止位置
 */
function _extractReportFromMalformedJson(text) {
  const trimmed = text.trim()
  try {
    const parsed = JSON.parse(escapeLiteralNewlinesInJsonStrings(trimmed))
    if (parsed.report && parsed.report.length >= 30) {
      return {
        report: parsed.report,
        recommendations: Array.isArray(parsed.recommendations) ? parsed.recommendations : [],
        actionKeywords: Array.isArray(parsed.actionKeywords) ? parsed.actionKeywords : [],
        actionCandidates: Array.isArray(parsed.actionCandidates) ? parsed.actionCandidates : [],
        competitionAnalysis: parsed.competitionAnalysis && typeof parsed.competitionAnalysis === 'object'
          ? parsed.competitionAnalysis
          : null,
      }
    }
  } catch {}
  let extractedReport = null
  let extractedKeywords = null

  // 策略 A：利用 "actionKeywords" 作为右边界锚点
  const kwAnchor = trimmed.indexOf('"actionKeywords"')
  if (kwAnchor > 0) {
    const reportKeyIdx = trimmed.indexOf('"report"')
    if (reportKeyIdx < 0) return null
    // 找到 "report" 值的起始引号（跳过 "report" 和冒号后的第一个 "）
    const valueStartQuote = trimmed.indexOf('"', reportKeyIdx + '"report"'.length + 1)
    if (valueStartQuote > 0 && valueStartQuote < kwAnchor) {
      // 从 kwAnchor 向前回溯，找到 report 值的结束引号
      const segment = trimmed.substring(0, kwAnchor)
      const valueEndQuote = segment.lastIndexOf('"')
      if (valueEndQuote > valueStartQuote) {
        extractedReport = trimmed.substring(valueStartQuote + 1, valueEndQuote)
        // 还原 JSON 转义（模型可能混用了 \n 转义和真实换行）
        extractedReport = extractedReport.replace(/\\n/g, '\n').replace(/\\"/g, '"')
      }
    }
    // 顺带提取 actionKeywords 数组
    const kwMatch = trimmed.substring(kwAnchor).match(/"actionKeywords"\s*:\s*\[([^\]]*)\]/)
    if (kwMatch) {
      const keywordMatches = kwMatch[1].match(/"([^"]+)"/g)
      extractedKeywords = Array.isArray(keywordMatches)
        ? keywordMatches.map(s => s.replace(/"/g, ''))
        : []
    }
  }

  // 策略 B：无 actionKeywords 锚点时，用文本末尾的 "} 作为右边界
  if (!extractedReport) {
    const reportKeyIdx = trimmed.indexOf('"report"')
    if (reportKeyIdx >= 0) {
      const valueStartQuote = trimmed.indexOf('"', reportKeyIdx + '"report"'.length + 1)
      const valueEndQuote = trimmed.lastIndexOf('"')
      if (valueStartQuote > 0 && valueEndQuote > valueStartQuote + 30) {
        extractedReport = trimmed.substring(valueStartQuote + 1, valueEndQuote)
        extractedReport = extractedReport.replace(/\\n/g, '\n').replace(/\\"/g, '"')
      }
    }
  }

  // 验证提取结果有效性
  if (!extractedReport || extractedReport.length < 30) return null

  log(`_extractReportFromMalformedJson: 成功，report.length=${extractedReport.length}`)

  // actionKeywords：优先用提取的，否则扫描关键词
  const KNOWN_KEYWORDS = [
    '主图', '图片', '白底图', '视频', '视觉素材',
    '标题', '关键词', 'SEO', '搜索词', '类目词',
    '详情页', '价格', 'SKU', '规格', '运费',
    '违规', '滞销', '库存', '评价', '复购',
  ]
  const actionKeywords = extractedKeywords && extractedKeywords.length > 0
    ? extractedKeywords
    : KNOWN_KEYWORDS.filter(kw => extractedReport.includes(kw))
  return { report: extractedReport, recommendations: [], actionKeywords, actionCandidates: [], competitionAnalysis: null }
}

function fmtMoney(value) {
  if (value === undefined || value === null) return '-'
  return '¥' + Number(value).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

function fmtPct(value) {
  if (value === undefined || value === null) return '-'
  const n = Number(value)
  return (n > 0 ? '+' : '') + n.toFixed(1) + '%'
}

const CHINESE_COUNT_VALUES = {
  '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
  '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
}

function parseChineseCount(value) {
  if (CHINESE_COUNT_VALUES[value]) return CHINESE_COUNT_VALUES[value]
  if (!value.includes('十')) return null
  const [tensText, onesText] = value.split('十')
  const tens = tensText ? CHINESE_COUNT_VALUES[tensText] : 1
  const ones = onesText ? CHINESE_COUNT_VALUES[onesText] : 0
  if (!tens || ones === undefined || ones === null) return null
  return tens * 10 + ones
}

function hasProblemDiagnosisIntent(input) {
  const text = String(input || '')
  return /(新品没流量|没流量|没有流量|低效|滞销|最(?:该|应该|需要|值得优先|值得)优化|需要优化|优先优化|优化调整|问题品|异常商品|先改(?:哪个|哪些)?|诊断.*问题|排查.*问题|找出.*问题|停止广告)/.test(text)
}

function parseRequestedDiagnosisCount(input) {
  const normalized = String(input || '').replace(/\s+/g, '')
  if (!/(分析|诊断|体检|检查|检测)/.test(normalized) && !hasProblemDiagnosisIntent(normalized)) return null
  const match = normalized.match(/前?([1-9]\d*|[一二两三四五六七八九十]+)[个件](?:商品|产品)?/)
  if (!match) return null
  const count = /^\d+$/.test(match[1]) ? Number(match[1]) : parseChineseCount(match[1])
  return Number.isInteger(count) && count > 0 ? count : null
}

function numberOrZero(value) {
  const number = Number(value)
  return Number.isFinite(number) ? number : 0
}

function abnormalRiskPriority(item) {
  const reason = String(item?.reason || '')
  return /(违规|下架|处罚|侵权|禁限售|售假|违禁)/.test(reason) ? 1 : 0
}

function prioritizeDiagnosisCandidates(candidates) {
  return (Array.isArray(candidates) ? candidates : [])
    .map((item, index) => ({ item, index }))
    .sort((left, right) => {
      const leftSource = left.item?.source || ''
      const rightSource = right.item?.source || ''
      const sourcePriority = source => source === 'abnormal' ? 0 : source === 'scoring' ? 1 : 2
      const sourceDiff = sourcePriority(leftSource) - sourcePriority(rightSource)
      if (sourceDiff !== 0) return sourceDiff

      if (leftSource === 'abnormal') {
        const riskDiff = abnormalRiskPriority(right.item) - abnormalRiskPriority(left.item)
        if (riskDiff !== 0) return riskDiff
        const declineDiff = Math.abs(numberOrZero(right.item?.payCycle)) - Math.abs(numberOrZero(left.item?.payCycle))
        if (declineDiff !== 0) return declineDiff
        const amountDiff = numberOrZero(right.item?.payAmount) - numberOrZero(left.item?.payAmount)
        if (amountDiff !== 0) return amountDiff
      }

      if (leftSource === 'scoring') {
        const scoreDiff = numberOrZero(left.item?.totalScore) - numberOrZero(right.item?.totalScore)
        if (scoreDiff !== 0) return scoreDiff
      }
      return left.index - right.index
    })
    .map(entry => entry.item)
}

function prioritizeAbnormalItems(items) {
  return (Array.isArray(items) ? items : [])
    .map((item, index) => ({ item, index }))
    .sort((left, right) => {
      const riskDiff = abnormalRiskPriority(right.item) - abnormalRiskPriority(left.item)
      if (riskDiff !== 0) return riskDiff

      const leftPay = left.item?.valueMap?.payAmt || {}
      const rightPay = right.item?.valueMap?.payAmt || {}
      const declineDiff = Math.abs(numberOrZero(rightPay.cycleCrc)) - Math.abs(numberOrZero(leftPay.cycleCrc))
      if (declineDiff !== 0) return declineDiff

      const amountDiff = numberOrZero(rightPay.value) - numberOrZero(leftPay.value)
      return amountDiff !== 0 ? amountDiff : left.index - right.index
    })
    .map(entry => entry.item)
}

function toTargetOffer(item) {
  return {
    offerId: item?.id || item?.itemId || item?.offerId || '',
    loginId: item?.loginId || '',
    isCurrent: item?.isCurrent === true || item?.is_current === true,
    shopName: item?.shop_name || '',
    title: (item?.title || item?.offerTitle || '').slice(0, 20),
  }
}

const CANDIDATE_IMAGE_CDN_PREFIX = 'https://cbu01.alicdn.com/'

function normalizeCandidateImageUrl(value) {
  const imageUrl = String(value || '').trim()
  if (!imageUrl) return ''
  return /^https?:\/\//i.test(imageUrl)
    ? imageUrl
    : `${CANDIDATE_IMAGE_CDN_PREFIX}${imageUrl.replace(/^\/+/, '')}`
}

function toCandidateFromAbnormal(item, discoverySource = '异常下跌') {
  return {
    source: 'abnormal',
    discoverySource,
    id: item?.itemId || item?.offerId || item?.id || '',
    offerId: item?.itemId || item?.offerId || item?.id || '',
    title: item?.offerTitle || item?.title || '',
    imageUrl: normalizeCandidateImageUrl(item?.offerImageUrl || item?.imageUrl),
    reason: item?.reason || '',
    payAmount: item?.valueMap?.payAmt?.value,
    payCycle: item?.valueMap?.payAmt?.cycleCrc,
    visitorCount: item?.valueMap?.uv?.value,
    visitorCycle: item?.valueMap?.uv?.cycleCrc,
    shop_name: item?.shop_name || item?.shopName || '',
    loginId: item?.loginId || '',
    isCurrent: item?.isCurrent === true || item?.is_current === true,
    raw: item,
  }
}

function toCandidateFromScoring(product, discoverySource = '评分分层-C级') {
  const metrics = product?.key_metrics || {}
  const scores = product?.scores || {}
  const classification = product?.classification || {}
  return {
    source: 'scoring',
    discoverySource,
    id: product?.item_id || product?.itemId || product?.offerId || '',
    offerId: product?.item_id || product?.itemId || product?.offerId || '',
    title: product?.title || '',
    imageUrl: normalizeCandidateImageUrl(product?.imageUrl),
    reason: `${classification.level || ''}${classification.name ? ` · ${classification.name}` : ''}`.trim(),
    level: classification.level || '',
    levelName: classification.name || '',
    totalScore: scores.total_score,
    payAmount: metrics.pay_ord_amt_1d,
    buyerCount: metrics.pay_ord_byr_cnt_1d,
    uv: metrics.ipv_uv_1d,
    shop_name: product?.shop_name || '',
    loginId: product?.loginId || '',
    raw: product,
  }
}

function toCandidateFromSearch(product) {
  const rawStatus = product?.status || product?.statusText || ''
  return {
    source: 'search',
    discoverySource: '关键词搜索',
    id: product?.id || product?.itemId || product?.item_id || product?.offerId || '',
    offerId: product?.id || product?.itemId || product?.item_id || product?.offerId || '',
    title: product?.title || product?.offerTitle || '',
    imageUrl: normalizeCandidateImageUrl(product?.imageUrl || product?.offerImageUrl || product?.mainImage),
    minPrice: product?.minPrice ?? product?.priceMin ?? product?.price,
    maxPrice: product?.maxPrice ?? product?.priceMax ?? product?.price,
    status: rawStatus === 'PUBLISHED' || rawStatus === '上架中' ? '上架中' : '未上架',
    shop_name: product?.shop_name || product?.shopName || '',
    loginId: product?.loginId || '',
    raw: product,
  }
}

function candidateToTargetOffer(candidate) {
  return {
    offerId: candidate?.offerId || candidate?.id || '',
    loginId: candidate?.loginId || '',
    isCurrent: candidate?.isCurrent === true || candidate?.is_current === true,
    shopName: candidate?.shop_name || '',
    title: candidate?.title || '',
    imageUrl: normalizeCandidateImageUrl(candidate?.imageUrl),
    candidateTitle: candidate?.title || '',
    selectionEvidence: {
      source: candidate?.source || '',
      discoverySource: candidate?.discoverySource || '',
      reason: candidate?.reason || '',
      payCycle: candidate?.payCycle,
      payAmount: candidate?.payAmount,
      totalScore: candidate?.totalScore,
      level: candidate?.level || '',
      levelName: candidate?.levelName || '',
    },
  }
}

function normalizeIdentityText(value) {
  return String(value || '').replace(/\s+/g, '').toLowerCase()
}

// ─── 商品诊断真实数据适配 ───

function findOfferTitleInObject(data, depth = 0) {
  if (!data || typeof data !== 'object' || depth > 5) return ''
  const titleKeys = ['offerTitle', 'itemTitle', 'productTitle', 'subject']
  for (const key of titleKeys) {
    const value = data[key]
    if (typeof value === 'string' && value.trim()) return value.trim()
  }
  for (const value of Object.values(data)) {
    if (value && typeof value === 'object') {
      const title = findOfferTitleInObject(value, depth + 1)
      if (title) return title
    }
  }
  if (depth === 0) {
    for (const scope of [data.profile, data.offer, data.item, data.product, data]) {
      const title = scope && typeof scope.title === 'string' ? scope.title.trim() : ''
      if (title) return title
    }
  }
  return ''
}

function extractNumberFromOfferText(text, patterns) {
  for (const pattern of patterns) {
    const match = String(text || '').match(pattern)
    if (!match) continue
    const value = Number(match[1])
    if (Number.isFinite(value)) return value
  }
  return undefined
}

function normalizeOfferDiagnosisPayload(source) {
  if (source?.__normalizedOfferDiagnosisPayload === true) return source

  const raw = source
    && typeof source === 'object'
    && !Array.isArray(source)
    && Object.prototype.hasOwnProperty.call(source, 'data')
    ? source.data
    : source

  if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
    // 新聚合 Tool（seller-agent HSF）返回 {profile, performance} 文本形态：
    // 拼接为纯文本后走 regex 提取指标路径，保证 deriveOfferStats 与 overview KPI 卡片可计算
    if (typeof raw.profile === 'string' && typeof raw.performance === 'string') {
      const promptText = (raw.profile + '\n' + raw.performance).trim()
      const titleMatch = promptText.match(/(?:^|\n)\s*商品标题\s*[:：]\s*([^\n]+)/)
      const categoryMatch = promptText.match(/(?:^|\n)\s*商品类目\s*[:：]\s*([^\n]+)/)
      const recentSixWeeksAllZero = /近\s*6\s*周[^。\n]*全(?:部)?为?\s*0/.test(promptText)
      return {
        __normalizedOfferDiagnosisPayload: true,
        structured: {},
        promptText,
        promptFormat: 'text',
        title: titleMatch ? titleMatch[1].trim() : '',
        category: categoryMatch ? categoryMatch[1].trim() : '',
        metrics: {
          gmv12m: extractNumberFromOfferText(promptText, [
            /近\s*12\s*个月[^。\n]*?GMV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
            /GMV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
          ]),
          ipvuv12m: extractNumberFromOfferText(promptText, [
            /近\s*12\s*个月[^。\n]*?IPVUV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
            /IPVUV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
          ]),
          uv12m: extractNumberFromOfferText(promptText, [
            /近\s*12\s*个月[^。\n]*?(?:访客数|访客人数|\bUV\b)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
            /(?:访客数|访客人数|\bUV\b)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
          ]),
          payBuyer12m: extractNumberFromOfferText(promptText, [
            /近\s*12\s*个月[^。\n]*?(?:支付人数|支付买家(?:数)?)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
            /(?:支付人数|支付买家(?:数)?)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
          ]),
          adSpend6w: extractNumberFromOfferText(promptText, [
            /近\s*6\s*周[^。\n]*?(?:广告成本|广告消耗|广告投入)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
            /(?:广告成本|广告消耗|广告投入)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
          ]) ?? (recentSixWeeksAllZero ? 0 : undefined),
          adPayByr6w: extractNumberFromOfferText(promptText, [
            /近\s*6\s*周[^。\n]*?广告[^。\n]*?(?:支付人数|支付买家(?:数)?)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
          ]),
        },
      }
    }

    return {
      __normalizedOfferDiagnosisPayload: true,
      structured: raw,
      promptText: JSON.stringify(raw, null, 2),
      promptFormat: 'json',
      title: findOfferTitleInObject(raw),
      category: '',
      metrics: {},
    }
  }

  const promptText = String(raw || '').trim()
  const titleMatch = promptText.match(/(?:^|\n)\s*商品标题\s*[:：]\s*([^\n]+)/)
  const categoryMatch = promptText.match(/(?:^|\n)\s*商品类目\s*[:：]\s*([^\n]+)/)
  const recentSixWeeksAllZero = /近\s*6\s*周[^。\n]*全(?:部)?为?\s*0/.test(promptText)
  return {
    __normalizedOfferDiagnosisPayload: true,
    structured: {},
    promptText,
    promptFormat: 'text',
    title: titleMatch ? titleMatch[1].trim() : '',
    category: categoryMatch ? categoryMatch[1].trim() : '',
    metrics: {
      gmv12m: extractNumberFromOfferText(promptText, [
        /近\s*12\s*个月[^。\n]*?GMV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
        /GMV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
      ]),
      ipvuv12m: extractNumberFromOfferText(promptText, [
        /近\s*12\s*个月[^。\n]*?IPVUV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
        /IPVUV\s*[=:：]\s*(-?\d+(?:\.\d+)?)/i,
      ]),
      uv12m: extractNumberFromOfferText(promptText, [
        /近\s*12\s*个月[^。\n]*?(?:访客数|访客人数|\bUV\b)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
        /(?:访客数|访客人数|\bUV\b)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
      ]),
      payBuyer12m: extractNumberFromOfferText(promptText, [
        /近\s*12\s*个月[^。\n]*?(?:支付人数|支付买家(?:数)?)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
        /(?:支付人数|支付买家(?:数)?)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
      ]),
      adSpend6w: extractNumberFromOfferText(promptText, [
        /近\s*6\s*周[^。\n]*?(?:广告成本|广告消耗|广告投入)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
        /(?:广告成本|广告消耗|广告投入)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
      ]) ?? (recentSixWeeksAllZero ? 0 : undefined),
      adPayByr6w: extractNumberFromOfferText(promptText, [
        /近\s*6\s*周[^。\n]*?广告[^。\n]*?(?:支付人数|支付买家(?:数)?)\s*(?:均为|为|[=:：])\s*(-?\d+(?:\.\d+)?)/i,
      ]),
    },
  }
}

function repairMalformedJsonStrings(text) {
  const source = String(text || '')
  let output = ''
  let inString = false
  let escaped = false

  for (let index = 0; index < source.length; index++) {
    const char = source[index]
    if (!inString) {
      output += char
      if (char === '"') inString = true
      continue
    }
    if (escaped) {
      output += char
      escaped = false
      continue
    }
    if (char === '\\') {
      output += char
      escaped = true
      continue
    }
    if (char === '\n' || char === '\r') {
      output += char === '\n' ? '\\n' : ''
      continue
    }
    if (char !== '"') {
      output += char
      continue
    }

    let nextIndex = index + 1
    while (nextIndex < source.length && /\s/.test(source[nextIndex])) nextIndex += 1
    const nextChar = source[nextIndex] || ''
    let closesString = !nextChar || [':', '}', ']'].includes(nextChar)
    if (nextChar === ',') {
      let valueIndex = nextIndex + 1
      while (valueIndex < source.length && /\s/.test(source[valueIndex])) valueIndex += 1
      const valueStart = source[valueIndex] || ''
      closesString = /["{\[\]\}\d\-tfn]/.test(valueStart)
    }
    if (closesString) {
      output += char
      inString = false
    } else {
      output += '\\"'
    }
  }
  return output
}

// 从带有分析过程/多个 JSON 片段的模型文本中提取完整对象。
// 模型偶尔会先输出 reasonHighlights 示例，再输出最终对象；只取首尾花括号会把两段拼在一起。
function findJsonObjectCandidates(text) {
  const source = String(text || '')
  const candidates = []
  const starts = []
  let inString = false
  let escaped = false
  const MAX_CANDIDATES = 96
  const MAX_CANDIDATE_LENGTH = 60000
  for (let index = 0; index < source.length; index += 1) {
    const char = source[index]
    if (inString) {
      if (escaped) escaped = false
      else if (char === '\\') escaped = true
      else if (char === '"') inString = false
      continue
    }
    if (char === '"') {
      inString = true
    } else if (char === '{') {
      starts.push(index)
    } else if (char === '}' && starts.length > 0) {
      const start = starts.pop()
      // 只保留每个顶层对象，避免对深层嵌套对象反复 parse/repair 造成 O(n²) 阻塞。
      if (starts.length === 0 && index - start + 1 <= MAX_CANDIDATE_LENGTH) {
        candidates.push(source.slice(start, index + 1))
        if (candidates.length > MAX_CANDIDATES) candidates.shift()
      }
    }
  }
  return candidates
}

function isStructuredDiagnosisCandidate(value) {
  return Boolean(
    value
    && typeof value === 'object'
    && !Array.isArray(value)
    && typeof value.reason === 'string'
    && value.reason.trim()
    && Array.isArray(value.reasonHighlights)
    && value.positioning
    && typeof value.positioning === 'object'
    && !Array.isArray(value.positioning)
    && typeof value.positioning.code === 'string'
    && value.positioning.code.trim()
    && Array.isArray(value.evidence)
    && Array.isArray(value.recommendations)
  )
}

const STRUCTURED_POSITIONING_CODES = new Set(['TRAFFIC', 'STABLE', 'POTENTIAL'])

function deriveLegacyPositioningCode(positioning) {
  const explicitCode = String(positioning && positioning.code || '').trim().toUpperCase()
  if (STRUCTURED_POSITIONING_CODES.has(explicitCode)) return explicitCode

  const descriptor = [
    positioning && positioning.currentPosition,
    positioning && positioning.targetPosition,
    positioning && positioning.gap,
  ].map(value => String(value || '')).join(' ')
  if (!descriptor.trim()) return ''
  if (/引流|流量/.test(descriptor)) return 'TRAFFIC'
  if (/稳定/.test(descriptor)) return 'STABLE'
  return 'POTENTIAL'
}

function normalizeRecommendationPriority(value, index) {
  const numeric = Number(value)
  if (String(value || '').trim() && Number.isFinite(numeric)) return numeric
  const legacyPriority = String(value || '').trim().match(/^P(\d+)$/i)
  if (legacyPriority) return Number(legacyPriority[1]) + 1
  return index + 1
}

// 模型偶尔会返回旧版诊断结构；只做字段归一化，不补造经营事实。
function normalizeStructuredDiagnosisCandidate(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return value

  const normalized = { ...value }
  if (value.positioning && typeof value.positioning === 'object' && !Array.isArray(value.positioning)) {
    normalized.positioning = {
      ...value.positioning,
      code: deriveLegacyPositioningCode(value.positioning),
      tags: Array.isArray(value.positioning.tags) ? value.positioning.tags : [],
    }
  }
  if (Array.isArray(value.reasonHighlights)) {
    normalized.reasonHighlights = value.reasonHighlights
      .map(highlight => {
        if (typeof highlight === 'string') return { text: highlight.trim(), evidenceCodes: [] }
        if (!highlight || typeof highlight !== 'object' || Array.isArray(highlight)) return null
        return {
          ...highlight,
          text: String(highlight.text || '').trim(),
          evidenceCodes: Array.isArray(highlight.evidenceCodes) ? highlight.evidenceCodes : [],
        }
      })
      .filter(highlight => highlight && highlight.text)
  }
  const rawRecommendations = Array.isArray(value.recommendations)
    ? value.recommendations
    : (value.recommendations && typeof value.recommendations === 'object' && !Array.isArray(value.recommendations)
      ? [value.recommendations]
      : null)
  if (rawRecommendations) {
    normalized.recommendations = rawRecommendations
      .map((recommendation, index) => {
        if (!recommendation || typeof recommendation !== 'object' || Array.isArray(recommendation)) return null
        return {
          ...recommendation,
          priority: normalizeRecommendationPriority(recommendation.priority, index),
        }
      })
      .filter(Boolean)
  }
  return normalized
}

function scoreStructuredDiagnosisCandidate(value) {
  const normalized = normalizeStructuredDiagnosisCandidate(value)
  if (!isStructuredDiagnosisCandidate(normalized)) return -1
  let score = 2
  if (normalized.positioning && typeof normalized.positioning === 'object') score += 2
  if (Array.isArray(normalized.evidence)) score += 2
  if (Array.isArray(normalized.reasonHighlights)) score += 1
  if (Array.isArray(normalized.anomalies)) score += 1
  if (Array.isArray(normalized.actionKeywords)) score += 1
  if (Array.isArray(normalized.actionCandidates)) score += 1
  return score
}

function parseStructuredDiagnosisValue(value, depth = 0) {
  if (depth > 6 || value === null || value === undefined) return null
  if (Array.isArray(value)) {
    let best = null
    let bestScore = -1
    for (const item of value) {
      const parsed = parseStructuredDiagnosisValue(item, depth + 1)
      const score = scoreStructuredDiagnosisCandidate(parsed)
      if (score >= bestScore) {
        best = parsed
        bestScore = score
      }
    }
    return best
  }
  if (typeof value === 'string') {
    const trimmed = value.trim()
    const codeBlocks = Array.from(trimmed.matchAll(/```(?:json)?\s*\n?([\s\S]*?)\n?```/g))
      .map(match => match[1].trim())
    const candidateTexts = [...codeBlocks, trimmed]
    let latestParsed = null
    let latestScore = -1
    for (const candidateText of candidateTexts) {
      const start = candidateText.indexOf('{')
      const end = candidateText.lastIndexOf('}')
      if (start === -1 || end <= start) continue

      const candidates = findJsonObjectCandidates(candidateText)
      candidates.push(candidateText.slice(start, end + 1))
      const seen = new Set()
      // 按文本顺序遍历，保留最后一个完整 schema 对象；前置对象通常是分析过程中的示例片段。
      for (const candidate of candidates) {
        if (seen.has(candidate)) continue
        seen.add(candidate)
        for (const textCandidate of [candidate, repairMalformedJsonStrings(candidate)]) {
          try {
            const parsed = parseStructuredDiagnosisValue(JSON.parse(textCandidate), depth + 1)
            const score = scoreStructuredDiagnosisCandidate(parsed)
            if (score >= latestScore) {
              latestParsed = parsed
              latestScore = score
            }
          } catch {
            // 继续尝试下一个完整对象或修复后的 JSON。
          }
        }
      }
    }
    return latestParsed
  }
  if (typeof value !== 'object') return null
  let best = null
  let bestScore = -1
  for (const key of ['data', 'result', 'output', 'content', 'value', 'text']) {
    if (!Object.prototype.hasOwnProperty.call(value, key)) continue
    const parsed = parseStructuredDiagnosisValue(value[key], depth + 1)
    const score = scoreStructuredDiagnosisCandidate(parsed)
    if (score >= bestScore) {
      best = parsed
      bestScore = score
    }
  }
  const selfScore = scoreStructuredDiagnosisCandidate(value)
  if (selfScore >= 0 && selfScore >= bestScore) return value
  return bestScore >= 0 ? best : null
}

// 校验 Agent 结构化诊断输出；兼容运行时常见 data/result/output 包裹。
function extractStructuredDiagnosis(raw) {
  const candidate = normalizeStructuredDiagnosisCandidate(parseStructuredDiagnosisValue(raw))
  if (!candidate) return null
  if (!isStructuredDiagnosisCandidate(candidate)) return null
  const reason = candidate.reason.trim()
  const recommendations = candidate.recommendations
  const actionCandidates = (Array.isArray(candidate.actionCandidates) ? candidate.actionCandidates : [])
    .filter(item => (
      item
      && typeof item.action === 'string'
      && item.action.trim()
      && typeof item.evidence === 'string'
      && item.evidence.trim()
    ))
  return {
    reason,
    reasonHighlights: Array.isArray(candidate.reasonHighlights) ? candidate.reasonHighlights : [],
    positioning: candidate.positioning || null,
    evidence: Array.isArray(candidate.evidence) ? candidate.evidence : [],
    anomalies: Array.isArray(candidate.anomalies) ? candidate.anomalies : [],
    recommendations,
    actionKeywords: Array.isArray(candidate.actionKeywords) ? candidate.actionKeywords : [],
    actionCandidates,
  }
}

// ─── end 商品诊断真实数据适配 ───

function reconcileOfferIdentity(target, offerPayload) {
  const actualTitle = normalizeOfferDiagnosisPayload(offerPayload).title
  const candidateTitle = target?.candidateTitle || target?.title || ''
  const identityMismatch = Boolean(
    actualTitle
    && candidateTitle
    && normalizeIdentityText(actualTitle) !== normalizeIdentityText(candidateTitle)
  )
  return {
    ...target,
    title: actualTitle || candidateTitle,
    identityMismatch,
    identityWarning: identityMismatch
      ? '候选标题与商品详情不一致，以下诊断仅以当前商品详情和经营数据为准。'
      : '',
  }
}

function extractAbnormalCandidates(multiShopResult) {
  const shops = multiShopResult?.data?.shops || []
  const discoveredItems = []
  for (const shop of shops) {
    if (shop?.error) continue
    for (const item of (shop.items || [])) {
      discoveredItems.push({
        ...item,
        shop_name: shop.shop_name,
        loginId: item.loginId || shop.loginId || '',
        isCurrent: shop?.is_current === true || shop?.isCurrent === true,
      })
    }
  }
  return prioritizeAbnormalItems(discoveredItems).map(item => toCandidateFromAbnormal(item))
}

function inspectAbnormalSource(multiShopResult) {
  if (!multiShopResult?.success) {
    return {
      available: false,
      candidates: [],
      failedShopNames: [],
      error: multiShopResult?.error || '异常商品数据暂不可用',
    }
  }

  const data = multiShopResult.data || {}
  const shops = Array.isArray(data.shops) ? data.shops : []
  const failedShops = shops.filter(shop => Boolean(shop?.error))
  const successfulShops = shops.filter(shop => !shop?.error)
  const failedShopNames = failedShops.map(shop => shop?.shop_name || shop?.shopName || '未命名店铺')
  const allReturnedShopsFailed = shops.length > 0 && successfulShops.length === 0
  const topLevelFailure = Boolean(data.error) && successfulShops.length === 0

  return {
    available: !allReturnedShopsFailed && !topLevelFailure,
    candidates: !allReturnedShopsFailed && !topLevelFailure ? extractAbnormalCandidates(multiShopResult) : [],
    failedShopNames,
    error: data.error || failedShops.map(shop => shop.error).filter(Boolean).join('；'),
  }
}

function extractSearchItems(data) {
  if (Array.isArray(data)) return data
  if (!data || typeof data !== 'object') return []
  for (const key of ['items', 'products', 'list', 'records', 'rows']) {
    if (Array.isArray(data[key])) return data[key]
  }
  if (data.data && data.data !== data) return extractSearchItems(data.data)
  return []
}

function chooseScoringArgs(itemOverview) {
  const total = Number(itemOverview?.itemCount || itemOverview?.onlineItemCount || itemOverview?.online_item_count || itemOverview?.total || 0)
  if (total > 500) return ['--strategy', 'comprehensive', '--limit', '200']
  if (total > 0 && total <= 200) return ['--strategy', 'all']
  return ['--strategy', 'comprehensive']
}

function positiveLevel(product) {
  return String(product?.classification?.level || product?.level || '').replace(/\s+/g, '')
}

function isPositiveCandidate(product) {
  return /^(S|A|B)级?$/.test(positiveLevel(product))
}

function formatPositiveCandidate(product) {
  const metrics = product?.key_metrics || {}
  const classification = product?.classification || {}
  const scores = product?.scores || {}
  const metricParts = [
    metrics.pay_ord_amt_1d != null ? `支付金额 ${fmtMoney(metrics.pay_ord_amt_1d)}` : '',
    metrics.pay_ord_byr_cnt_1d != null ? `买家数 ${metrics.pay_ord_byr_cnt_1d}` : '',
    metrics.ipv_uv_1d != null ? `访客数 ${metrics.ipv_uv_1d}` : '',
    scores.total_score != null ? `综合得分 ${scores.total_score}` : '',
  ].filter(Boolean)
  return `### ${product?.title || '重点运营候选商品'}\n\n` +
    `- 商品 ID：${product?.item_id || product?.offerId || '-'}\n` +
    `- 评分分层：${classification.level || '-'} · ${classification.name || '-'}\n` +
    `- 关键指标：${metricParts.join('，') || '-'}\n` +
    `- 入选理由：该商品进入 ${classification.level || 'S/A/B'} 候选，具备当前数据下的重点运营价值。`
}

function buildCandidateRows(candidates, includeDiscoverySource = false) {
  return candidates.map(candidate => {
    const imageUrl = candidate.imageUrl
      ? (String(candidate.imageUrl).startsWith('http') ? candidate.imageUrl : `https://cbu01.alicdn.com/${candidate.imageUrl}`)
      : ''
    return {
      id: candidate.offerId || candidate.id || '',
      title: (candidate.title || '').slice(0, 30),
      imageUrl,
      shop_name: candidate.shop_name || '',
      reason: candidate.reason || '',
      discoverySource: candidate.discoverySource || '',
      payAmount: candidate.payAmount != null ? fmtMoney(candidate.payAmount) : '-',
      changeRate: candidate.payCycle != null ? fmtPct(candidate.payCycle) : '-',
      visitorCount: candidate.visitorCount ?? candidate.uv ?? '-',
      visitorChange: candidate.visitorCycle != null ? fmtPct(candidate.visitorCycle) : '-',
      level: candidate.level || '',
      levelName: candidate.levelName || '',
      totalScore: candidate.totalScore ?? '',
      buyerCount: candidate.buyerCount ?? '',
      minPrice: candidate.minPrice ?? '',
      maxPrice: candidate.maxPrice ?? '',
      status: candidate.status || '',
      loginId: candidate.loginId || '',
      _candidate: candidate,
      ...(includeDiscoverySource ? { discoverySource: candidate.discoverySource || '' } : {}),
    }
  })
}

function buildCandidateTableSpec(candidates, { kind = 'abnormal', title, includeDiscoverySource = false } = {}) {
  const rows = buildCandidateRows(candidates, includeDiscoverySource)
  if (kind === 'search') {
    return {
      selectionType: 'select_products_from_search',
      title: title || '搜索结果 — 请选择要诊断的商品',
      columns: [
        { key: 'imageUrl', label: '图片', width: 80 },
        { key: 'id', label: '商品ID', width: 140 },
        { key: 'title', label: '商品标题' },
        { key: 'minPrice', label: '最低价(元)', width: 100 },
        { key: 'maxPrice', label: '最高价(元)', width: 100 },
        { key: 'status', label: '状态', width: 90 },
      ],
      rows,
    }
  }
  if (kind === 'scoring') {
    return {
      selectionType: 'select_products_from_scoring',
      title: title || '评分分层候选商品 — 请选择要诊断的商品',
      columns: [
        { key: 'id', label: '商品ID', width: 100 },
        { key: 'title', label: '商品标题' },
        { key: 'level', label: '等级', width: 70 },
        { key: 'levelName', label: '分层', width: 100 },
        { key: 'totalScore', label: '综合得分', width: 90 },
        { key: 'payAmount', label: '支付金额', width: 100 },
        { key: 'buyerCount', label: '买家数', width: 80 },
        { key: 'uv', label: '访客数', width: 80 },
      ],
      rows,
    }
  }
  return {
    selectionType: 'select_abnormal_offer',
    title: title || '候选商品列表 — 请选择要诊断的商品',
    columns: [
      { key: 'imageUrl', label: '图片', width: 80 },
      { key: 'title', label: '商品标题' },
      ...(includeDiscoverySource ? [{ key: 'discoverySource', label: '发现来源', width: 120 }] : []),
      { key: 'shop_name', label: '店铺', width: 100 },
      { key: 'reason', label: '原因', width: 120 },
      { key: 'payAmount', label: '支付金额', width: 120 },
      { key: 'changeRate', label: '支付环比', width: 100 },
      { key: 'visitorCount', label: '访客数', width: 100 },
      { key: 'visitorChange', label: '访客环比', width: 100 },
    ],
    rows,
  }
}

function selectTopCandidates(candidates, count) {
  const rankedCandidates = prioritizeDiagnosisCandidates(candidates)
  const uniqueOffers = dedupeTargetOffers(
    rankedCandidates.map(candidateToTargetOffer).filter(item => item.offerId)
  )
  const effectiveCount = Math.min(count || 1, uniqueOffers.length)
  return uniqueOffers.slice(0, effectiveCount)
}

const AUTO_DIAGNOSIS_TASK_QUERY = '自动按优先级挑出【最该优化的 5 个商品】，完成诊断后直接在对话中输出完整报告和每个商品的优化建议'

function normalizeDiagnosisModeText(input) {
  return String(input || '').replace(/[\s\p{P}]/gu, '')
}

function hasExplicitInteractiveDiagnosisRequest(input) {
  const text = normalizeDiagnosisModeText(input)
  const deniesAutomatic = /(?:不要|不准|别|禁止|请勿|不可|不能|不允许)(?:再)?(?:进行|采用)?自动/.test(text)
  const asksUserToDecide = /(?:让我|由我|请我).{0,8}(?:选择|确认|询问|问)/.test(text)
    || /(?:请)?先(?:让我|由我|请我)?(?:选择|确认|询问|问)/.test(text)
  const selectsBeforeExecution = /选择(?:商品|结果|方案)?(?:后|之后)(?:再)?/.test(text)
    && !/(?:自动|无人值守).{0,20}选择(?:商品|结果|方案)?(?:后|之后)(?:再)?/.test(text)
  const confirmsBeforeExecution = /确认(?:结果|方案)?(?:后|之后)(?:再)?/.test(text)
  const asksPerItemInteraction = /(?:逐个|逐件|逐款).{0,8}(?:选择|确认)/.test(text)
  return deniesAutomatic || asksUserToDecide || selectsBeforeExecution || confirmsBeforeExecution || asksPerItemInteraction
}

function hasAutomaticDiagnosisAuthorization(input) {
  const text = normalizeDiagnosisModeText(input)
  const hasAutomaticAction = /(?:自动|无人值守).{0,20}(?:挑|选|找|筛|分析|诊断|体检|执行)/.test(text)
  const hasNoFollowupDirective = /(?:无需|不用|不必|不准|不要)(?:再)?(?:反问|询问|确认|选择)/.test(text)
  return hasAutomaticAction || hasNoFollowupDirective
}

function hasAutomaticDiagnosisIntentCandidate(input) {
  if (hasExplicitInteractiveDiagnosisRequest(input)) return false
  const text = normalizeDiagnosisModeText(input)
  const hasDirectContinuation = /(?:直接|继续)(?:执行|分析|诊断|体检|往后走)/.test(text)
  return hasAutomaticDiagnosisAuthorization(input) || hasDirectContinuation
}

function hasStrongAutomaticDiagnosisIntent(input) {
  if (!hasAutomaticDiagnosisIntentCandidate(input) || !hasAutomaticDiagnosisAuthorization(input)) return false
  const text = normalizeDiagnosisModeText(input)
  const hasDiagnosis = /(?:诊断|体检)/.test(text)
  const hasCompleteReport = /完整报告/.test(text)
  const hasPerProductAdvice = /(?:每(?:个|件|款)商品|逐(?:个|件|款)?商品).{0,16}(?:优化)?建议/.test(text)
  const hasConversationDelivery = /(?:对话|聊天).{0,16}(?:输出|给出|展示)|(?:输出|给出|展示).{0,16}(?:对话|聊天)/.test(text)
  return hasDiagnosis && hasCompleteReport && hasPerProductAdvice && hasConversationDelivery
}

async function detectDiagnosisExecutionMode(userInput) {
  if (!hasAutomaticDiagnosisIntentCandidate(userInput)) return 'interactive'
  try {
    const raw = await agent(
      `你是商品诊断执行模式分类器。请仅根据用户原始请求判断，用户是否明确授权本轮无人值守完成商品诊断。\n\nautomatic=true 必须满足：\n1. 用户要求自动挑选、自动分析，或明确要求不要反问、不要中途确认；\n2. 用户要求完成诊断并在当前对话交付报告或逐商品优化建议；\n3. 用户没有要求先选择商品、先询问或确认后再执行。\n\n不要匹配固定句子：“直接”不是必需词，“开始执行”等附加文字不影响判断。若只是普通商品诊断、搜索、选品，或需要用户选择/确认，automatic=false。\n\n用户请求：${String(userInput || '')}`,
      {
        label: 'diagnosis-execution-mode',
        schema: {
          type: 'object',
          properties: { automatic: { type: 'boolean' } },
          required: ['automatic'],
        },
      }
    )
    const modelDecision = parseAgentResult(raw)
    if (typeof modelDecision?.automatic === 'boolean') {
      if (modelDecision.automatic) return 'automatic'
      return hasStrongAutomaticDiagnosisIntent(userInput) ? 'automatic' : 'interactive'
    }
  } catch (error) {
    console?.warn?.(`diagnosis execution mode detection failed: ${String((error && error.message) || error)}`)
  }
  return hasStrongAutomaticDiagnosisIntent(userInput) ? 'automatic' : 'interactive'
}

function classifyIntent(input, hasDirectOfferId) {
  if (hasDirectOfferId) return 'direct'
  const text = String(input || '')
  if (/(搜索|搜一下|查找|查一下|关键词|按.*词|含有|包含)/.test(text)) return 'keyword_search'
  if (hasProblemDiagnosisIntent(text)) return 'problem_diagnosis'
  if (/(选品|推荐商品|圈选|重点品|重点运营|商品分层|今日运营重点|值得投入|优质商品)/.test(text)) return 'positive_selection'
  return 'pure_diagnosis'
}

const ACTION_RULES = [
  { key: 'title_opt', label: '标题优化', terms: ['标题优化', '优化标题', '关键词优化', 'seo', '搜索词', '类目词', '标题'] },
  { key: 'main_img_opt', label: '主图优化', terms: ['主图优化', '优化主图', '图片优化', '视觉素材', '视频', '图片', '主图'] },
  { key: 'white_img', label: '白底图', terms: ['白底图优化', '白底图'] },
  { key: 'free_shipping', label: '设置包邮', terms: ['设置包邮', '包邮'] },
  { key: 'send_24h', label: '24H发货', terms: ['设置24小时发货', '24小时发货', '24h发货'] },
  { key: 'swbp', label: '三无包赔', terms: ['三无包赔'] },
  { key: 'jskp', label: '极速开票', terms: ['极速开票'] },
  { key: 'mix_whole', label: '混批', terms: ['混批'] },
  { key: 'one_batch', label: '一件起批', terms: ['一件起批'] },
  { key: 'qtwlybt', label: '7天无理由', terms: ['7天无理由', '七天无理由'] },
  { key: 'psbj', label: '破损包赔', terms: ['破损包赔'] },
  { key: 'shbp', label: '少货必赔', terms: ['少货必赔'] },
  { key: 'wow', label: '哇噢定制', terms: ['哇噢定制'] },
  { key: 'one_shipping', label: '一件代发', terms: ['一件代发'] },
  { key: 'cross_border', label: '跨境资质', terms: ['跨境资质'] },
]

const PRICE_ACTION_TERMS = ['价格', '定价', '调价', '涨价', '降价', '改价', '营销价', '促销价', '优惠价']

function canonicalizeAction(rawAction) {
  const normalized = String(rawAction || '').replace(/\s+/g, '').toLowerCase()
  if (!normalized) return null
  if (PRICE_ACTION_TERMS.some(term => normalized.includes(term))) return null
  return ACTION_RULES.find(rule => rule.terms.some(term => normalized.includes(term.toLowerCase()))) || null
}

function findActionEvidence(report, terms) {
  const lines = String(report || '')
    .split('\n')
    .map(line => line.replace(/^\s*[-*●\d.]+\s*/, '').trim())
    .filter(Boolean)
  return lines.find(line => terms.some(term => line.toLowerCase().includes(term.toLowerCase()))) || ''
}

function resolveOfferTitle(data, depth = 0) {
  if (!data || typeof data !== 'object' || depth > 4) return ''
  const titleKeys = ['offerTitle', 'itemTitle', 'productTitle', 'subject', 'title']
  for (const key of titleKeys) {
    const value = data[key]
    if (typeof value === 'string' && value.trim()) return value.trim()
  }
  for (const value of Object.values(data)) {
    if (value && typeof value === 'object') {
      const title = resolveOfferTitle(value, depth + 1)
      if (title) return title
    }
  }
  return ''
}

function deriveDiagnosisActionCandidates(report, actionKeywords) {
  const keywordText = (Array.isArray(actionKeywords) ? actionKeywords : []).join(' ')
  const candidates = []
  const titleTerms = ['标题', '关键词', 'seo', '搜索词', '类目词']
  const imageTerms = ['主图', '图片', '白底图', '视频', '视觉素材']
  const hasTitleAction = titleTerms.some(term => keywordText.toLowerCase().includes(term.toLowerCase()))
  const hasImageAction = imageTerms.some(term => keywordText.toLowerCase().includes(term.toLowerCase()))

  if (hasTitleAction) {
    candidates.push({
      action: '标题优化',
      evidence: findActionEvidence(report, titleTerms),
    })
  }
  if (hasImageAction) {
    candidates.push({
      action: '主图优化',
      evidence: findActionEvidence(report, imageTerms),
    })
  }

  return candidates
}

const ENHANCEMENT_STATUS = Object.freeze({
  SUCCESS: 'success',
  NO_DATA: 'no_data',
  UNAUTHORIZED: 'unauthorized',
  TOOL_FAILED: 'tool_failed',
})

function enhancementResultText(result) {
  try {
    return [
      result?.error,
      result?.markdown,
      result?.data?.errorMsg,
      result?.data?.message,
      JSON.stringify(result?.data || {}),
    ].filter(Boolean).join(' ')
  } catch {
    return String(result?.error || result?.markdown || '')
  }
}

function isUnauthorizedEnhancement(result) {
  return /(无权限|未授权|不归属|归属校验|绑定关系|permission|unauthorized|forbidden)/i
    .test(enhancementResultText(result))
}

function declaredEnhancementStatus(result) {
  const status = String(result?.status || '')
  return Object.values(ENHANCEMENT_STATUS).includes(status) ? status : ''
}

function classifySameOfferResult(result) {
  const declaredStatus = declaredEnhancementStatus(result)
  if (declaredStatus === ENHANCEMENT_STATUS.UNAUTHORIZED) return ENHANCEMENT_STATUS.UNAUTHORIZED
  if (declaredStatus === ENHANCEMENT_STATUS.TOOL_FAILED) return ENHANCEMENT_STATUS.TOOL_FAILED
  if (declaredStatus === ENHANCEMENT_STATUS.NO_DATA) return ENHANCEMENT_STATUS.NO_DATA
  const comparison = result?.data?.v2Comparison
  const hasComparison = comparison && typeof comparison === 'object' && Object.keys(comparison).length > 0
  if (declaredStatus === ENHANCEMENT_STATUS.SUCCESS) {
    return hasComparison ? ENHANCEMENT_STATUS.SUCCESS : ENHANCEMENT_STATUS.NO_DATA
  }
  if (!result?.success) {
    return isUnauthorizedEnhancement(result)
      ? ENHANCEMENT_STATUS.UNAUTHORIZED
      : ENHANCEMENT_STATUS.TOOL_FAILED
  }
  return hasComparison
    ? ENHANCEMENT_STATUS.SUCCESS
    : ENHANCEMENT_STATUS.NO_DATA
}

function classifyOfferDiagnosisResult(result, offerId) {
  const declaredStatus = declaredEnhancementStatus(result)
  if (declaredStatus === ENHANCEMENT_STATUS.UNAUTHORIZED) return ENHANCEMENT_STATUS.UNAUTHORIZED
  if (declaredStatus === ENHANCEMENT_STATUS.TOOL_FAILED) return ENHANCEMENT_STATUS.TOOL_FAILED
  if (declaredStatus === ENHANCEMENT_STATUS.NO_DATA) return ENHANCEMENT_STATUS.NO_DATA
  const data = result?.data
  const exactMatch = data && String(data.offerId || '') === String(offerId || '')
  const hasActions = exactMatch && Array.isArray(data.actions) && data.actions.length > 0
  if (declaredStatus === ENHANCEMENT_STATUS.SUCCESS) {
    return hasActions ? ENHANCEMENT_STATUS.SUCCESS : ENHANCEMENT_STATUS.NO_DATA
  }
  if (!result?.success) {
    return isUnauthorizedEnhancement(result)
      ? ENHANCEMENT_STATUS.UNAUTHORIZED
      : ENHANCEMENT_STATUS.TOOL_FAILED
  }
  if (isUnauthorizedEnhancement(result)) return ENHANCEMENT_STATUS.UNAUTHORIZED
  return hasActions
    ? ENHANCEMENT_STATUS.SUCCESS
    : ENHANCEMENT_STATUS.NO_DATA
}

function extractOfferImageFromDiagnosis(result, offerId) {
  if (!result?.success) return ''
  const data = result.data
  if (!data || String(data.offerId || '') !== String(offerId || '')) return ''
  return normalizeCandidateImageUrl(data.offerImageUrl)
}

function projectCompetitionV2ForReport(data) {
  const v2 = data?.v2Comparison
  if (!v2) return null
  const pickProduct = product => ({
    title: product?.title || '-',
    videoStatus: product?.videoStatus || '-',
    mainImageAnalysis: product?.mainImageAnalysis || '-',
    detailImageAnalysis: product?.detailImageAnalysis || '-',
  })
  return {
    source: data?.competitionSource || '-',
    category: {
      sameSecondCategory: v2.sameSecondCategory === true,
      target: v2.targetCategory || '-',
      competitor: v2.competitorCategory || '-',
    },
    material: { target: pickProduct(v2.target), competitor: pickProduct(v2.competitor) },
    performanceWindow: v2.performanceWindow || '-',
    performance: v2.performance || {},
    trafficWindow: v2.trafficWindow || '-',
    trafficChannels: Array.isArray(v2.trafficChannels) ? v2.trafficChannels : [],
    afterSales: v2.afterSales || {},
    reviews: {
      goodRate: v2.goodRate || {}, goodsGrade: v2.goodsGrade || {},
      impressions: v2.reviewImpressions || {}, counts: v2.reviewCounts || {}, fulfillment: v2.fulfillmentRates || {},
    },
    topSkus: v2.topSkus || {},
  }
}

function projectCompetitionV2ForAgent(data) {
  const v2 = projectCompetitionV2ForReport(data)
  if (!v2) return null
  return {
    category: v2.category,
    material: v2.material,
    performance: v2.performance,
    afterSales: v2.afterSales,
  }
}

function normalizeCompetitionNarrative(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null
  const normalize = text => typeof text === 'string'
    ? text.replace(/[\r\n]+/g, ' ').trim().slice(0, 150)
    : ''
  return {
    materialAnalysis: normalize(value.materialAnalysis),
    performanceAnalysis: normalize(value.performanceAnalysis),
    marketingAnalysis: normalize(value.marketingAnalysis),
    lessonsToLearn: normalize(value.lessonsToLearn),
  }
}

function formatSameOfferAnalysis(data, competitionAnalysis) {
  const v2 = projectCompetitionV2ForReport(data)
  if (!v2) return ''
  const narrative = normalizeCompetitionNarrative(competitionAnalysis)

  const competitorLabel = data?.competitionSource === 'SPID' ? '同款标杆' : '竞品对照商品'
  const fmt = value => value === undefined || value === null || value === '' ? '-' : value
  const hasValue = value => {
    if (Array.isArray(value)) return value.some(hasValue)
    return value !== undefined && value !== null && value !== '' && value !== '-'
  }
  const text = (value, maxLength = 100) => String(fmt(value)).replace(/[|\n]/g, ' ').slice(0, maxLength)
  const fullText = value => String(fmt(value)).replace(/[|\n]/g, ' ')
  const list = (values, limit = 3) => Array.isArray(values) && values.some(hasValue)
    ? values.filter(hasValue).slice(0, limit).map(value => text(value, 60)).join('、')
    : '-'
  const formatVisitCartRate = value => {
    if (typeof value === 'string' && value.trim() === '') return '-'
    const formatText = () => text(String(value).replace(/\r\n?/g, '\n'), 50)
    if (typeof value === 'string' && value.includes('%')) return formatText()
    const numericValue = Number(value)
    if (Number.isFinite(numericValue)) return `${Number((numericValue * 100).toFixed(2))}%`
    return formatText()
  }
  const formatMetricValue = (key, value) => {
    if (!hasValue(value)) return '-'
    if (key === 'payAmount' && Number.isFinite(Number(value))) return fmtMoney(value)
    if (key === 'visitCartRate') return formatVisitCartRate(value)
    return text(value, 50)
  }
  const compareValues = (target, competitor) => {
    if (!hasValue(target) || !hasValue(competitor)) return '仅供参考'
    const targetNumber = Number(target)
    const competitorNumber = Number(competitor)
    if (Number.isFinite(targetNumber) && Number.isFinite(competitorNumber)) {
      if (targetNumber === competitorNumber) return '基本持平'
      return targetNumber < competitorNumber ? '低于标杆' : '高于标杆'
    }
    return text(target) === text(competitor) ? '表现一致' : '存在差异'
  }
  const metricDefinitions = [
    ['payAmount', '近7天支付金额'],
    ['itemUv', '访客数'],
    ['visitCartRate', '访客加购率'],
  ]
  const performanceRows = metricDefinitions
    .map(([key, label]) => {
      const metric = v2.performance[key] || {}
      if (!hasValue(metric.target) && !hasValue(metric.competitor)) return null
      const trend = metric.targetCycleCrcPct != null || metric.competitorCycleCrcPct != null
        ? `；环比 ${fmtPct(metric.targetCycleCrcPct)} / ${fmtPct(metric.competitorCycleCrcPct)}`
        : ''
      return {
        key,
        label,
        target: formatMetricValue(key, metric.target),
        competitor: formatMetricValue(key, metric.competitor),
        judgement: `${compareValues(metric.target, metric.competitor)}${trend}`,
        rawTarget: metric.target,
        rawCompetitor: metric.competitor,
      }
    })
    .filter(Boolean)

  const materialRows = [
    ['标题', fullText(v2.material.target.title), fullText(v2.material.competitor.title)],
    ['视频', text(v2.material.target.videoStatus, 50), text(v2.material.competitor.videoStatus, 50)],
    ['主图解读', text(v2.material.target.mainImageAnalysis, 90), text(v2.material.competitor.mainImageAnalysis, 90)],
    ['详情图解读', text(v2.material.target.detailImageAnalysis, 90), text(v2.material.competitor.detailImageAnalysis, 90)],
  ].filter(([, target, competitor]) => hasValue(target) || hasValue(competitor))

  const afterSaleDefinitions = [
    ['peaceOfMindGuarantee', '安心购现货版'],
    ['sevenDayReturn', '7天包退'],
    ['shipWithin48Hours', '48小时发货'],
    ['sevenDayNoReasonReturn', '7天无理由退货'],
  ]
  const serviceRows = afterSaleDefinitions
    .map(([key, label]) => [label, text(v2.afterSales[key]?.target, 50), text(v2.afterSales[key]?.competitor, 50)])
    .filter(([, target, competitor]) => hasValue(target) || hasValue(competitor))

  const reviewRows = [
    ['好评率', text(v2.reviews.goodRate.target, 50), text(v2.reviews.goodRate.competitor, 50)],
    ['商品评分', text(v2.reviews.goodsGrade.target, 50), text(v2.reviews.goodsGrade.competitor, 50)],
    ['买家印象', list(v2.reviews.impressions.target), list(v2.reviews.impressions.competitor)],
    ['评价数量', list(v2.reviews.counts.target), list(v2.reviews.counts.competitor)],
    ['履约表现', list(v2.reviews.fulfillment.target), list(v2.reviews.fulfillment.competitor)],
  ].filter(([, target, competitor]) => hasValue(target) || hasValue(competitor))

  const sections = ['#### 同款商品分析']

  if (materialRows.length > 0) {
    const rows = materialRows.map(([label, target, competitor]) => `| ${label} | ${target} | ${competitor} |`).join('\n')
    let materialSection = `##### 商品素材\n\n| 对比项 | 当前商品 | ${competitorLabel} |\n|---|---|---|\n${rows}`
    if (narrative?.materialAnalysis) materialSection += `\n\n${narrative.materialAnalysis}`
    sections.push(materialSection)
  }
  if (performanceRows.length > 0) {
    const period = hasValue(v2.performanceWindow) ? `（统计周期：${text(v2.performanceWindow, 30)}）` : ''
    let perfSection = `##### 经营表现${period}\n\n| 指标 | 当前商品 | ${competitorLabel} | 判断 |\n|---|---|---|---|\n${performanceRows.map(row => `| ${row.label} | ${row.target} | ${row.competitor} | ${row.judgement} |`).join('\n')}`
    if (narrative?.performanceAnalysis) perfSection += `\n\n${narrative.performanceAnalysis}`
    sections.push(perfSection)
  }

  const trafficRows = v2.trafficChannels
    .filter(channel => hasValue(channel.ipvUv?.target) || hasValue(channel.ipvUv?.competitor)
      || hasValue(channel.payAmount?.target) || hasValue(channel.payAmount?.competitor))
    .map(channel => `| ${channel.source === 'market' ? '市场' : '自主访问'}${channel.child ? ` / ${text(channel.name, 30)}` : ''} | ${text(channel.ipvUv?.target, 30)} | ${text(channel.ipvUv?.competitor, 30)} | ${formatMetricValue('payAmount', channel.payAmount?.target)} / ${formatMetricValue('payAmount', channel.payAmount?.competitor)} |`)
  if (trafficRows.length > 0) {
    const period = hasValue(v2.trafficWindow) ? `（统计周期：${text(v2.trafficWindow, 30)}）` : ''
    sections.push(`##### 流量来源${period}\n\n| 来源 | 当前访客 | 对照访客 | 支付金额（当前 / 对照） |\n|---|---|---|---|\n${trafficRows.join('\n')}`)
  }

  if (serviceRows.length > 0) {
    const rows = serviceRows.map(([label, target, competitor]) => `| ${label} | ${target} | ${competitor} |`).join('\n')
    let serviceSection = `##### 服务保障\n\n| 对比项 | 当前商品 | ${competitorLabel} |\n|---|---|---|\n${rows}`
    if (narrative?.marketingAnalysis) serviceSection += `\n\n${narrative.marketingAnalysis}`
    sections.push(serviceSection)
  }

  if (reviewRows.length > 0) {
    const rows = reviewRows.map(([label, target, competitor]) => `| ${label} | ${target} | ${competitor} |`).join('\n')
    sections.push(`##### 口碑评价\n\n| 对比项 | 当前商品 | ${competitorLabel} |\n|---|---|---|\n${rows}`)
  }

  if (hasValue(v2.topSkus.target) || hasValue(v2.topSkus.competitor)) {
    sections.push(`##### 热卖 SKU\n\n| 当前商品 Top3 | ${competitorLabel} Top3 |\n|---|---|\n| ${list(v2.topSkus.target)} | ${list(v2.topSkus.competitor)} |`)
  }
  return sections.join('\n\n')
}

function cleanRecommendation(value) {
  return String(value || '')
    .trim()
    .replace(/^\s*(?:[-*●•]\s*|\d+[.)、]\s*)/, '')
    .replace(/^\*{0,2}(?:优化建议|优化|可借鉴方向)\*{0,2}\s*[：:]\s*/, '')
    .trim()
}

function normalizeRecommendations(values) {
  const source = Array.isArray(values) ? values : [values]
  return source
    .flatMap(value => String(value || '').split(/\n+/))
    .map(cleanRecommendation)
    .filter(Boolean)
    .filter(value => !/(?:广告|推广).{0,12}预算|预算.{0,8}(?:元|块)|(?:办理|补充|申请|开通).{0,10}(?:认证|备案资质)|(?:预计|预期|可望).{0,20}(?:提升|增长).{0,8}\d+(?:\.\d+)?%/i.test(value))
}

function sanitizeMerchantReport(value) {
  const internalLine = /^\s*(?:(?:Now|Next|Let me|I need to|I should|I'll)\b|(?:让我|我需要|我应该)(?:先|来|检查|调用|读取|分析|构造|输出)|(?:现在|接下来)(?:先|来|检查|调用|读取|分析|构造|输出))/i
  const internalMarker = /(TodoWrite|show_interaction|get_offer_data|alibaba\.1688\.get\.offer\.data|get_same_offer_competition|get_offer_diagnosis_actions|<execution_manifest>|<\/?function>|<\/?parameter>)/i
  let text = String(value || '')
    .replace(/<execution_manifest>[\s\S]*?<\/execution_manifest>/gi, '')
    .replace(/<aside>[\s\S]*?<\/aside>/gi, '')
    .replace(/<\/?(?:function|parameter|tool_call|tool_result)[^>]*>/gi, '')
    .replace(/```(?:json|javascript|js|text)?\s*([\s\S]*?)```/gi, (block, body) =>
      internalMarker.test(body) ? '' : block)

  text = text
    .split('\n')
    .filter(line => {
      const trimmed = line.trim()
      if (!trimmed) return true
      if (internalMarker.test(trimmed)) return false
      if (internalLine.test(trimmed)) return false
      if (/^\s*\{.*"(?:name|tool|command)"\s*:\s*"(?:TodoWrite|Edit|Read|Bash|show_interaction)"/i.test(trimmed)) return false
      return true
    })
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
  return text
}

// ─── 商品诊断隐藏数据流式协议（section protocol）───
const SECTION_COMPONENT = 'product-diagnosis-report'
const SECTION_VERSION = '1.0'
const SECTION_FENCE_BY_SECTION = Object.freeze({
  report_meta: 'DATA-HIDDEN-PRODUCT-DIAGNOSIS-META',
  product_catalog: 'DATA-HIDDEN-PRODUCT-DIAGNOSIS-CATALOG',
  product_result: 'DATA-HIDDEN-PRODUCT-DIAGNOSIS-PRODUCT',
  overview_result: 'DATA-HIDDEN-PRODUCT-DIAGNOSIS-OVERVIEW',
  footer_actions: 'DATA-HIDDEN-PRODUCT-DIAGNOSIS-ACTIONS',
  report_completed: 'DATA-HIDDEN-PRODUCT-DIAGNOSIS-COMPLETED',
})
const DIAGNOSIS_COMPONENT_URL = 'webComponent:csbc-newton-modules-seller-data-table?planCode=CDT_68lm5S'
const DIAGNOSIS_COMPONENT_TITLE = 'AI商品诊断'
// 色板硬编（参考设计稿）；Agent 无颜色输出权，span 色值必须命中色板
const SECTION_PALETTE = Object.freeze({
  emphasis: '#FF6A00',
  status: '#1677FF',
  danger: '#F5222D',
  secondary: '#999999',
})
const SECTION_LIMITS = Object.freeze({ evidence: 6, recommendations: 3, anomalies: 2 })
const SECTION_HTML_ALLOWED_TAGS = ['b', 'strong', 'i', 'em', 'br', 'span']

function generateReportId(now = new Date()) {
  const pad = value => String(value).padStart(2, '0')
  const stamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`
  let rand = ''
  for (let i = 0; i < 4; i += 1) rand += Math.floor(Math.random() * 36).toString(36)
  return `pd_${stamp}_${rand}`
}

function escapeHtml(text) {
  return String(text == null ? '' : text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function escapeSectionTag(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function sanitizeSectionHtml(input) {
  const spanValidStack = []
  return String(input == null ? '' : input)
    .replace(/<!--[\s\S]*?-->/g, escapeSectionTag)
    .replace(/<\/?\s*([a-zA-Z][a-zA-Z0-9]*)((?:[^<>])*?)\/?\s*>/g, (match, rawTag, rawAttrs) => {
      const tag = rawTag.toLowerCase()
      const closing = /^<\s*\//.test(match)
      if (!SECTION_HTML_ALLOWED_TAGS.includes(tag)) return escapeSectionTag(match)
      if (closing) {
        if (tag !== 'span') return `</${tag}>`
        const openingValid = spanValidStack.length > 0 ? spanValidStack.pop() : false
        return openingValid ? '</span>' : escapeSectionTag(match)
      }
      if (tag === 'br') return '<br>'
      if (tag !== 'span') return `<${tag}>`
      const colorMatch = String(rawAttrs || '').match(/style\s*=\s*(["'])\s*color\s*:\s*(#[0-9a-fA-F]{6})\s*;?\s*\1/)
      const color = colorMatch
        ? Object.values(SECTION_PALETTE).find(value => value.toLowerCase() === colorMatch[2].toLowerCase()) || ''
        : ''
      const valid = Boolean(color)
      spanValidStack.push(valid)
      return valid ? `<span style="color:${color}">` : escapeSectionTag(match)
    })
}

// 硬编颜色包裹（内容先转义，防注入）
function sectionColorSpan(text, color) {
  return `<span style="color:${color}">${escapeHtml(text)}</span>`
}

function normalizeHighlightEvidenceText(value) {
  return String(value == null ? '' : value)
    .toLowerCase()
    .replace(/[,，。；：、（）()[\]{}"'`_\s]/g, '')
    .replace(/[—–~～至]/g, '-')
}

function buildEvidenceLabelTokens(label) {
  const normalized = normalizeHighlightEvidenceText(label)
    .replace(/近\d+(?:个月|周|天)/g, '')
    .replace(/近期/g, '')
  const tokens = new Set()
  for (const match of normalized.matchAll(/[a-z][a-z0-9]*/g)) {
    if (match[0].length >= 2) tokens.add(match[0])
  }
  for (const match of normalized.matchAll(/[\u4e00-\u9fff]{2,}/g)) {
    for (const segment of match[0].split(/[未无与和及]/)) {
      if (segment.length >= 2) tokens.add(segment)
    }
  }
  return [...tokens]
}

function containsNormalizedNumber(text, value) {
  const numericText = String(Math.abs(value))
  const escapedNumber = numericText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const decimalSuffix = Number.isInteger(Math.abs(value)) ? '(?:\\.0+)?' : ''
  const unsignedPattern = new RegExp(`(^|[^0-9.])${escapedNumber}${decimalSuffix}(?=$|[^0-9.])`)
  if (value >= 0) return unsignedPattern.test(text)
  const signedPattern = new RegExp(`(^|[^0-9.])-\\s*${escapedNumber}${decimalSuffix}(?=$|[^0-9.])`)
  return signedPattern.test(text)
    || (/(?:下降|下跌|减少|降低|负)/.test(text) && unsignedPattern.test(text))
}

function evidenceSupportsReasonHighlight(highlightText, evidence) {
  const normalizedText = normalizeHighlightEvidenceText(highlightText)
  const normalizedValue = normalizeHighlightEvidenceText(evidence && evidence.value)
  if (!normalizedText || !normalizedValue) return false

  const numericValue = Number(String(evidence.value).replace(/[%千万元人件次/]/g, ''))
  const hasValue = Number.isFinite(numericValue)
    ? (containsNormalizedNumber(normalizedText, numericValue)
      || (numericValue === 0 && /(?:零|无)/.test(normalizedText)))
    : normalizedText.includes(normalizedValue)
  if (!hasValue) return false

  const labelTokens = buildEvidenceLabelTokens(evidence.label)
  return labelTokens.length > 0 && labelTokens.every(token => normalizedText.includes(token))
}

function isWholeReasonSentence(reason, highlightText) {
  const normalizeSentence = value => String(value || '').trim().replace(/[。！？!?；;]+$/g, '')
  const normalizedHighlight = normalizeSentence(highlightText)
  if (!normalizedHighlight) return true
  const sentences = String(reason || '').match(/[^。！？!?；;]+[。！？!?；;]?/g) || []
  return sentences.some(sentence => normalizeSentence(sentence) === normalizedHighlight)
}

function highlightDiagnosisReason(value, highlights, evidence, allowedEvidenceCodes) {
  const text = String(value || '').trim()
  if (!text) return ''

  const allowedCodeSet = new Set(
    (Array.isArray(allowedEvidenceCodes) ? allowedEvidenceCodes : [])
      .map(code => String(code || '').trim())
      .filter(Boolean)
  )
  const evidenceByCode = new Map(
    (Array.isArray(evidence) ? evidence : [])
      .filter(entry => entry && entry.code)
      .map(entry => [String(entry.code), entry])
  )
  const candidates = []
  for (const highlight of (Array.isArray(highlights) ? highlights : []).slice(0, 6)) {
    const highlightText = String((highlight && highlight.text) || '').trim()
    const evidenceCodes = [...new Set(
      (Array.isArray(highlight && highlight.evidenceCodes) ? highlight.evidenceCodes : [])
        .map(code => String(code || '').trim())
        .filter(Boolean)
    )].slice(0, 3)
    if (highlightText.length < 2 || highlightText.length > 60 || evidenceCodes.length === 0) continue
    if (isWholeReasonSentence(text, highlightText)) continue
    if (allowedCodeSet.size === 0 || evidenceCodes.some(code => !allowedCodeSet.has(code))) continue

    const referencedEvidence = evidenceCodes.map(code => evidenceByCode.get(code))
    if (referencedEvidence.some(entry => !entry)) continue
    if (!referencedEvidence.every(entry => evidenceSupportsReasonHighlight(highlightText, entry))) continue

    let start = text.indexOf(highlightText)
    while (start !== -1) {
      candidates.push({ start, end: start + highlightText.length })
      start = text.indexOf(highlightText, start + highlightText.length)
    }
  }

  candidates.sort((left, right) => {
    const lengthDiff = (right.end - right.start) - (left.end - left.start)
    return lengthDiff || left.start - right.start
  })
  const ranges = []
  for (const candidate of candidates) {
    if (ranges.some(range => candidate.start < range.end && candidate.end > range.start)) continue
    ranges.push(candidate)
    if (ranges.length >= 6) break
  }
  ranges.sort((left, right) => left.start - right.start)

  let cursor = 0
  let html = ''
  for (const range of ranges) {
    if (range.start < cursor) continue
    html += escapeHtml(text.slice(cursor, range.start))
    html += `<span style="color:${SECTION_PALETTE.emphasis}"><b>${escapeHtml(text.slice(range.start, range.end))}</b></span>`
    cursor = range.end
  }
  html += escapeHtml(text.slice(cursor))
  return html
}

function buildSectionEnvelope(reportId, seq, section, payload, emittedAt = new Date().toISOString()) {
  return { version: SECTION_VERSION, component: SECTION_COMPONENT, reportId, seq, section, emittedAt, payload }
}

// 唯一 section 出口：所有区块进入同一 Promise 队列，按调用顺序分配连续 seq
function emitSection(reportId, seqState, section, payload) {
  const fence = SECTION_FENCE_BY_SECTION[section]
  if (!fence) {
    seqState.failed = true
    log(`unknown diagnosis section: ${String(section || '')}`)
    return Promise.resolve(0)
  }
  seqState.counter += 1
  const seq = seqState.counter
  const envelope = buildSectionEnvelope(reportId, seq, section, payload)
  seqState.chain = Promise.resolve(seqState.chain).then(async () => {
    try {
      await emit(`\`\`\`${fence}\n${JSON.stringify(envelope)}\n\`\`\``)
    } catch (error) {
      seqState.failed = true
      log(`section emit failed: ${String((error && error.message) || error)}`)
    }
    return seq
  })
  return seqState.chain
}

async function waitForSectionDrain(seqState) {
  await Promise.resolve(seqState.chain)
  return seqState.failed !== true
}

async function finalizeSectionStream(seqState, emitCompleted) {
  await Promise.resolve(seqState.chain)
  const hadPriorFailure = seqState.failed === true
  emitCompleted()
  await Promise.resolve(seqState.chain)
  return !hadPriorFailure && seqState.failed !== true
}

const SECTION_ERROR_PRESET = Object.freeze({
  OFFER_NOT_FOUND: { code: 'OFFER_NOT_FOUND', message: '未找到该商品或不属于当前账号' },
  DATA_UNAVAILABLE: { code: 'DATA_UNAVAILABLE', message: '商品数据暂时无法读取' },
  AGENT_FAILED: { code: 'AGENT_FAILED', message: '诊断生成失败' },
  TIMEOUT: { code: 'TIMEOUT', message: '诊断超时' },
})

function getMerchantSafeReportFailureMessage(outcome, presets = SECTION_ERROR_PRESET) {
  const presetCode = typeof outcome?.errorPreset === 'string'
    ? outcome.errorPreset
    : outcome?.errorPreset?.code
  const preset = Object.values(presets).find(item => item.code === presetCode)
  if (preset) return preset.message
  return outcome?.timedOut
    ? presets.TIMEOUT.message
    : presets.DATA_UNAVAILABLE.message
}

async function invokeDiagnosisComponent(reportId, totalProducts) {
  try {
    const result = await callTool('show_interaction', {
      type: 'open_tab',
      url: DIAGNOSIS_COMPONENT_URL,
      title: DIAGNOSIS_COMPONENT_TITLE,
    })
    const explicitlyFailed = Boolean(getInteractionFailureReason(result))
      || result?.opened === false
      || result?.data?.opened === false
      || Boolean(result?.error)
      || Boolean(result?.data?.error)
    // open_tab 在端侧完成导航后允许无返回体；只要没有明确失败信号，就视为已唤起。
    const explicitlyOpened = !explicitlyFailed
    if (!explicitlyOpened) {
      log(`component launch unavailable, continue section stream: ${JSON.stringify(result).substring(0, 200)}`)
    }
    return { attempted: true, opened: explicitlyOpened }
  } catch (err) {
    // show_interaction(open_tab) 只负责唤起承载页；隐藏数据块仍需发送，供当前或后续注册的渲染器消费。
    log(`component launch exception, continue section stream: ${String((err && err.message) || err)}`)
    return { attempted: true, opened: false }
  }
}

// 本地时区 ISO 8601 格式（YYYY-MM-DDTHH:mm:ss±HH:mm，含显式时区偏移），与 metaLine 展示时间同源，避免 toISOString 的 UTC 偏移
function formatDiagnosedAt(now = new Date()) {
  const pad = value => String(value).padStart(2, '0')
  // getTimezoneOffset() 返回 UTC-本地 的分钟数（东八区为 -480），符号与偏移后缀相反；取绝对值后拆时/分，兼容半小时时区（如 -05:30）
  const offsetMinutes = -now.getTimezoneOffset()
  const offsetSign = offsetMinutes >= 0 ? '+' : '-'
  const absMinutes = Math.abs(offsetMinutes)
  const offsetSuffix = `${offsetSign}${pad(Math.floor(absMinutes / 60))}:${pad(absMinutes % 60)}`
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}${offsetSuffix}`
}

function formatDiagnosedAtDisplay(now = new Date()) {
  const pad = value => String(value).padStart(2, '0')
  return `${now.getFullYear()}.${pad(now.getMonth() + 1)}.${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`
}

function buildReportMetaPayload(now = new Date(), totalProducts = 0) {
  const metaLineText = `诊断时间 ${formatDiagnosedAtDisplay(now)} · 共 ${totalProducts} 款商品`
  return {
    title: 'AI 商品诊断',
    badge: '智能体检',
    diagnosedAt: formatDiagnosedAt(now),
    totalProducts,
    metaLine: sectionColorSpan(metaLineText, SECTION_PALETTE.secondary),
    disclaimer: sectionColorSpan('AI 诊断结果仅供参考，建议结合店铺实际经营情况执行', SECTION_PALETTE.secondary),
  }
}

function buildProductCatalogPayload(targets) {
  return {
    products: (Array.isArray(targets) ? targets : []).map((target, index) => ({
      offerId: String(target.offerId),
      ordinal: index,
      status: 'loading',
      title: String(target.title || ''),
      imageUrl: String(target.imageUrl || ''),
      loginId: String(target.loginId || ''),
    })),
  }
}

function readStatValue(data, ...paths) {
  for (const path of paths) {
    let node = data
    for (const key of path.split('.')) {
      node = node == null ? undefined : node[key]
    }
    if (node !== undefined && node !== null && node !== '') return node
  }
  return undefined
}

// 从 alibaba.1688.get.offer.data 结果归一化出指标快照（字段路径以实际返回为准；缺失 → undefined → pool 省略）
// valueMap 兼容两种包裹：顶层 data.valueMap 与聚合 Tool 的模块嵌套 data.performance.valueMap。
function deriveOfferStats(offerData) {
  const normalized = normalizeOfferDiagnosisPayload(offerData)
  const data = normalized.structured || {}
  const num = value => {
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : undefined
  }
  const cyclePct = crc => {
    const parsed = Number(crc)
    return Number.isFinite(parsed) ? Math.round(parsed * 100) : undefined
  }
  return {
    gmv12m: num(readStatValue(data, 'valueMap.payAmt.value', 'performance.valueMap.payAmt.value', 'gmv12m') ?? normalized.metrics.gmv12m),
    ipvuv12m: num(readStatValue(data, 'valueMap.ipvUv.value', 'performance.valueMap.ipvUv.value', 'ipvuv12m') ?? normalized.metrics.ipvuv12m),
    payBuyer12m: num(readStatValue(data, 'valueMap.payByrCnt.value', 'performance.valueMap.payByrCnt.value', 'payByrCnt12m') ?? normalized.metrics.payBuyer12m),
    uv12m: num(readStatValue(data, 'valueMap.uv.value', 'performance.valueMap.uv.value') ?? normalized.metrics.uv12m),
    uvCyclePct: cyclePct(readStatValue(data, 'valueMap.uv.cycleCrc', 'performance.valueMap.uv.cycleCrc')),
    adClickCost6w: num(readStatValue(data, 'adClickCost6w', 'valueMap.adClickCost.value')),
    adSpend6w: num(readStatValue(data, 'adSpend6w', 'valueMap.adSpend.value') ?? normalized.metrics.adSpend6w),
    adPayByr6w: num(readStatValue(data, 'adPayByr6w', 'valueMap.adPayByr.value') ?? normalized.metrics.adPayByr6w),
    exposureRange6w: readStatValue(data, 'exposureRange6w'),
    cartNoPay: num(readStatValue(data, 'cartNoPayWeek', 'valueMap.cartCnt.value')),
  }
}

function buildEvidencePool(stats) {
  const pool = []
  const push = (code, label, value, unit, severity) => {
    if (value === undefined || value === null || value === '') return
    const valueText = String(value)
    pool.push({
      code,
      label,
      value: valueText,
      unit: unit || '',
      severity,
      display: sectionColorSpan(valueText, SECTION_PALETTE.emphasis)
        + (unit ? sectionColorSpan(unit, SECTION_PALETTE.secondary) : ''),
    })
  }
  push('GMV_12M', '近12个月 GMV', stats.gmv12m, '元', Number(stats.gmv12m) === 0 ? 'critical' : 'info')
  push('IPVUV_12M', '近12个月 IPVUV', stats.ipvuv12m, '', Number(stats.ipvuv12m) === 0 ? 'critical' : 'info')
  push('PAY_BUYER_12M', '近12个月支付人数', stats.payBuyer12m, '人', Number(stats.payBuyer12m) === 0 ? 'critical' : 'info')
  push('UV_12M', '近12个月访客数', stats.uv12m, '人', Number(stats.uv12m) === 0 ? 'critical' : 'info')
  const payBuyer = Number(stats.payBuyer12m)
  const visitors = Number(stats.uv12m)
  const conversionRate = Number.isFinite(payBuyer) && Number.isFinite(visitors) && visitors > 0
    ? Number(((payBuyer / visitors) * 100).toFixed(2))
    : undefined
  push('CONVERSION_RATE_12M', '近12个月转化率', conversionRate, '%', conversionRate === 0 ? 'critical' : 'info')
  push('AD_CLICK_COST_6W', '近6周广告点击成本', stats.adClickCost6w, '元/次',
    Number(stats.adClickCost6w) > 0 && Number(stats.adPayByr6w) === 0 ? 'warning' : 'info')
  push('AD_SPEND_6W', '近6周广告消耗', stats.adSpend6w, '元', 'info')
  push('AD_PAY_BUYER_6W', '近6周广告支付人数', stats.adPayByr6w, '人',
    Number(stats.adSpend6w) > 0 && Number(stats.adPayByr6w) === 0 ? 'critical' : 'info')
  push('EXPOSURE_RANGE_6W', '近6周曝光波动', stats.exposureRange6w, '', 'warning')
  push('CART_NO_PAY', '近期加购未支付', stats.cartNoPay, '件', Number(stats.cartNoPay) > 0 ? 'critical' : 'info')
  push('UV_CYCLE', '访客环比', stats.uvCyclePct === undefined ? undefined : `${stats.uvCyclePct}%`, '', Number(stats.uvCyclePct) < 0 ? 'warning' : 'info')
  return pool
}

// LLM 诊断不可用时仍基于已核验的商品指标交付一份最小可用报告。
// 该兜底只引用 evidencePool/selectionEvidence，不生成类目、属性或合规结论，避免把模型故障扩大成数据故障。
function buildDeterministicDiagnosisFallback(stats = {}, evidencePool = [], selectionEvidence = {}) {
  const numberOrUndefined = value => {
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : undefined
  }
  const gmv = numberOrUndefined(stats.gmv12m)
  const ipvuv = numberOrUndefined(stats.ipvuv12m)
  const uv = numberOrUndefined(stats.uv12m)
  const payBuyer = numberOrUndefined(stats.payBuyer12m)
  const severityRank = { critical: 0, warning: 1, info: 2 }
  const rankedEvidence = (Array.isArray(evidencePool) ? evidencePool : [])
    .filter(entry => entry && entry.code && entry.label && entry.value !== undefined && entry.value !== null)
    .slice()
    .sort((left, right) => (severityRank[left.severity] ?? 9) - (severityRank[right.severity] ?? 9))
  // 没有任何已核验指标时不能把模型失败伪装成成功报告。
  if (rankedEvidence.length === 0) return null
  const formatFact = entry => `${entry.label}为${entry.value}${entry.unit || ''}`
  const facts = rankedEvidence.slice(0, 2).map(formatFact)

  const reason = `已读取到${facts.join('，')}；本次诊断报告由已核验指标生成，详细原因需稍后重试。`

  const hasSales = (gmv !== undefined && gmv > 0) || (payBuyer !== undefined && payBuyer > 0)
  const selectionReason = String(selectionEvidence?.reason || '')
  const noTraffic = (ipvuv !== undefined && ipvuv <= 0)
    || (uv !== undefined && uv <= 0)
    || /零访问|访客下跌/.test(selectionReason)
  const positioningCode = hasSales ? 'STABLE' : (noTraffic ? 'TRAFFIC' : null)
  const reasonHighlights = facts.map((text, index) => ({
    text,
    evidenceCodes: [rankedEvidence[index].code],
  }))
  const evidence = rankedEvidence.slice(0, 3).map(entry => ({
    code: entry.code,
    severity: entry.severity || 'info',
  }))

  return {
    reason: reason.slice(0, 150),
    reasonHighlights,
    positioning: positioningCode ? { code: positioningCode, tags: [] } : null,
    evidence,
    anomalies: [],
    recommendations: [
      {
        code: 'VERIFY_CATEGORY',
        priority: 1,
        title: '确认商品状态与数据回传',
        description: '在商品管理页确认商品已上架、类目与详情一致，并重新检查经营数据是否正常回传。',
      },
    ],
    actionKeywords: [],
    actionCandidates: [],
  }
}

async function runDiagnosisAgent(prompt, options, offerId) {
  try {
    return await agent(prompt, options)
  } catch (error) {
    log(`[DIAG_AGENT_ERROR] offerId=${offerId} message=${String((error && error.message) || error || 'unknown')}`)
    return null
  }
}

const SEVERITY_RANK = { critical: 0, warning: 1, info: 2 }

// Agent 输出 [{code,severity}] 引用 → 从池展开完整结构（含 code 供去重/埋点，协议出参由组装方选字段）；非法 code 丢弃；空引用 → 确定性 top-3
function resolveEvidenceRefs(refs, pool, limit = SECTION_LIMITS.evidence) {
  const byCode = new Map((Array.isArray(pool) ? pool : []).map(entry => [entry.code, entry]))
  const picked = []
  for (const ref of Array.isArray(refs) ? refs : []) {
    const entry = byCode.get(ref && ref.code)
    if (!entry || picked.some(item => item.code === entry.code)) continue
    const severity = ['critical', 'warning', 'info'].includes(ref && ref.severity) ? ref.severity : entry.severity
    picked.push({ code: entry.code, label: entry.label, value: entry.value, unit: entry.unit, severity, display: entry.display })
    if (picked.length >= limit) break
  }
  if (picked.length > 0) return picked
  return [...(Array.isArray(pool) ? pool : [])]
    .sort((a, b) => (SEVERITY_RANK[a.severity] ?? 9) - (SEVERITY_RANK[b.severity] ?? 9))
    .slice(0, Math.min(3, limit))
    .map(entry => ({ code: entry.code, label: entry.label, value: entry.value, unit: entry.unit, severity: entry.severity, display: entry.display }))
}

// 设计稿短状态形态：优先展示当前经营数据；数据无法形成明确结论时，回退异常商品自带原因。
function buildBriefStatusText(stats, fallbackReason = '') {
  const gmv = Number(stats.gmv12m)
  const ipvuv = Number(stats.ipvuv12m)
  const uvDown = Number(stats.uvCyclePct) < 0
  const cartNoPay = Number(stats.cartNoPay) > 0
  const adNoConversion = Number(stats.adSpend6w) > 0 && Number(stats.adPayByr6w) === 0
  // stats 无 exposureTotal6w 数值字段：以 exposureRange6w（近6周曝光波动）非空作为"有曝光"证据
  const hasExposure = !!stats.exposureRange6w
  if (ipvuv === 0 && gmv === 0) return '零访问 · 零成交'
  // 兜底：访客数据缺失（NaN）且零成交、无曝光、无其他异常信号
  if (!(ipvuv > 0) && !uvDown && !cartNoPay && !adNoConversion && gmv === 0 && !hasExposure) return '零访问 · 零成交'
  const trend = uvDown ? '访客下跌' : ''
  let mode = ''
  if (gmv === 0 && hasExposure) mode = '零成交'
  else if (cartNoPay) mode = '加购未转化'
  else if (adNoConversion) mode = '广告未转化'
  else if (uvDown) mode = '自然流量未转化'
  const dataDrivenStatus = [trend, mode].filter(Boolean).join(' · ')
  return dataDrivenStatus || String(fallbackReason || '').trim()
}

function buildBriefStatusHtml(stats, fallbackReason = '') {
  const text = buildBriefStatusText(stats || {}, fallbackReason)
  return text ? sectionColorSpan(text, SECTION_PALETTE.status) : ''
}

const POSITIONING_CODES = Object.freeze({ TRAFFIC: '引流款', STABLE: '稳定款', POTENTIAL: '潜力款' })

function buildPositioning(raw) {
  const code = String((raw && raw.code) || '').trim().toUpperCase()
  if (!POSITIONING_CODES[code]) return null
  const seenTags = new Set()
  const tags = Array.isArray(raw && raw.tags)
    ? raw.tags
      .map(tag => String(tag).trim())
      .filter(tag => {
        if (!tag || tag === POSITIONING_CODES[code] || seenTags.has(tag)) return false
        seenTags.add(tag)
        return true
      })
      .slice(0, 3)
    : []
  return { code, label: POSITIONING_CODES[code], tags }
}

// 内部保留的建议 code 白名单（供一键优化准入与埋点；协议层只出 HTML 字符串）
const RECOMMENDATION_CODE_WHITELIST = new Set([
  'OPTIMIZE_TITLE', 'OPTIMIZE_MAIN_IMAGE', 'WHITE_BG_IMAGE', 'OPTIMIZE_DETAIL_PAGE',
  'ADD_SCENARIO_IMAGE', 'ADD_TECHNICAL_PARAMETERS', 'ADD_MAIN_VIDEO', 'ADD_TRUST_ELEMENT',
  'VERIFY_AD_MATCH', 'VERIFY_CATEGORY', 'PAUSE_LOW_EFFICIENCY_AD',
])
const RECOMMENDATION_BANNED_CODES = new Set(['ADJUST_PRICE'])

function selectTopRecommendations(recs, limit = SECTION_LIMITS.recommendations) {
  return (Array.isArray(recs) ? recs : [])
    .filter(rec => {
      const title = String((rec && rec.title) || '').trim()
      const description = String((rec && rec.description) || '').trim()
      const code = String((rec && rec.code) || '').trim().toUpperCase()
      return (title || description) && !RECOMMENDATION_BANNED_CODES.has(code)
    })
    .map((rec, index) => {
      const priority = Number(rec && rec.priority)
      return {
        rec,
        index,
        priority: Number.isFinite(priority) && priority > 0 ? priority : Number.POSITIVE_INFINITY,
      }
    })
    .sort((left, right) => left.priority - right.priority || left.index - right.index)
    .slice(0, limit)
    .map(entry => entry.rec)
}

function buildRecommendationsHtmlList(recs, limit = SECTION_LIMITS.recommendations) {
  const htmlList = []
  const codes = []
  for (const rec of selectTopRecommendations(recs, limit)) {
    const title = String((rec && rec.title) || '').trim()
    const description = String((rec && rec.description) || '').trim()
    if (!title && !description) continue
    const rawCode = String((rec && rec.code) || '').trim().toUpperCase()
    if (RECOMMENDATION_BANNED_CODES.has(rawCode)) continue
    const code = RECOMMENDATION_CODE_WHITELIST.has(rawCode) ? rawCode : 'GENERAL'
    // description 先经 sanitizeSectionHtml（非白名单标签转义为可见文本），再剥离剩余白名单标签：
    // 建议正文按纯文本渲染（设计稿 §4.3 示例 description 无内联标签），标签内文字保留
    const descriptionText = sanitizeSectionHtml(description).replace(/<[^>]+>/g, '')
    const html = `${htmlList.length + 1}. <span style="color:${SECTION_PALETTE.emphasis}"><b>${escapeHtml(title)}</b></span>：${descriptionText}`
    htmlList.push(html)
    codes.push(code)
    if (htmlList.length >= limit) break
  }
  return { htmlList, codes }
}

function limitTextSentences(value, limit = 1) {
  const text = String(value || '').trim()
  if (!text) return ''
  const sentences = text.match(/[^。！？!?；;]+[。！？!?；;]?/g) || [text]
  return sentences.slice(0, limit).join('').trim()
}

function buildAnomaliesList(anomalies, limit = SECTION_LIMITS.anomalies) {
  const list = []
  const sorted = (Array.isArray(anomalies) ? anomalies : [])
    .map((anomaly, index) => ({ anomaly, index }))
    .sort((left, right) => {
      const leftRank = left.anomaly && left.anomaly.level === 'critical' ? 0 : 1
      const rightRank = right.anomaly && right.anomaly.level === 'critical' ? 0 : 1
      return leftRank - rightRank || left.index - right.index
    })
  for (const { anomaly } of sorted) {
    const title = String((anomaly && anomaly.title) || '').trim()
    const description = limitTextSentences(anomaly && anomaly.description, 1)
    if (!title && !description) continue
    list.push({
      code: String((anomaly && anomaly.code) || 'ANOMALY'),
      level: anomaly && anomaly.level === 'critical' ? 'critical' : 'warning',
      title,
      description: sanitizeSectionHtml(description),
    })
    if (list.length >= limit) break
  }
  return list
}

// 协议出参：evidence 不含内部 code（resolveEvidenceRefs 产物里的 code 仅供去重/埋点）
function buildProductResultPayload(input) {
  const positioning = input.positioning
    ? {
        code: input.positioning.code,
        label: input.positioning.label,
        tags: Array.isArray(input.positioning.tags) ? input.positioning.tags : [],
      }
    : null
  return {
    offerId: String(input.offerId),
    ordinal: input.ordinal,
    status: 'success',
    title: String(input.title || ''),
    imageUrl: String(input.imageUrl || ''),
    briefStatus: input.briefStatusHtml || '',
    positioning,
    diagnosis: {
      reason: sanitizeSectionHtml(highlightDiagnosisReason(
        input.reasonHtml || '',
        input.reasonHighlights,
        input.evidence,
        input.reasonHighlightEvidenceCodes
      )),
      evidence: (input.evidence || []).map(entry => ({
        label: entry.label, value: entry.value, unit: entry.unit, severity: entry.severity, display: entry.display,
      })),
      anomalies: input.anomalies || [],
    },
    recommendations: input.recommendationsHtml || [],
  }
}

function buildProductFailurePayload(input) {
  const preset = input.errorPreset || SECTION_ERROR_PRESET.DATA_UNAVAILABLE
  return {
    offerId: String(input.offerId),
    ordinal: input.ordinal,
    status: 'failed',
    title: String(input.title || ''),
    imageUrl: String(input.imageUrl || ''),
    error: { code: preset.code, message: input.errorMessage || preset.message },
  }
}

function summarizeReportFailures(outcomes) {
  const failures = (Array.isArray(outcomes) ? outcomes : []).filter(outcome => !outcome?.success)
  if (failures.length === 0) {
    return {
      visibleMessage: '商品体检未完成，未获得可用诊断结果，请稍后重试。',
      reason: '未获得可用诊断结果',
    }
  }
  const codes = failures.map(outcome => outcome?.errorPreset?.code || '')
  const allAre = predicate => codes.every(predicate)
  if (allAre(code => code === SECTION_ERROR_PRESET.TIMEOUT.code)) {
    return {
      visibleMessage: '商品诊断超时，暂未生成报告，请稍后重试。',
      reason: '商品诊断超时',
    }
  }
  if (allAre(code => code === SECTION_ERROR_PRESET.AGENT_FAILED.code)) {
    return {
      visibleMessage: '商品数据已读取，但诊断报告生成失败，请稍后重试。',
      reason: '诊断报告生成失败',
    }
  }
  if (allAre(code => code === SECTION_ERROR_PRESET.OFFER_NOT_FOUND.code)) {
    return {
      visibleMessage: '未找到选中的商品，请确认商品 ID 和绑定店铺后重试。',
      reason: '未找到选中的商品',
    }
  }
  if (allAre(code => code === SECTION_ERROR_PRESET.DATA_UNAVAILABLE.code)) {
    return {
      visibleMessage: '暂时无法读取选中商品的数据，请稍后重试。',
      reason: '所有商品数据获取失败',
    }
  }
  if (failures.length === codes.length && codes.every(code => code === '')) {
    return {
      visibleMessage: '商品诊断执行失败，暂未生成报告，请稍后重试。',
      reason: '商品诊断执行失败',
    }
  }
  const totalOutcomes = Array.isArray(outcomes) ? outcomes.length : 0
  if (totalOutcomes > 0 && failures.length === totalOutcomes) {
    return {
      visibleMessage: '商品体检未完成，所有商品的数据或诊断结果暂不可用，请稍后重试。',
      reason: '所有商品数据或诊断报告获取失败',
    }
  }
  return {
    visibleMessage: failures.length === 1
      ? '商品体检未完成，该商品的数据或诊断结果暂不可用，请稍后重试。'
      : '商品体检未完成，部分商品数据或诊断结果暂不可用，请稍后重试。',
    reason: '商品数据或诊断报告获取失败',
  }
}

function dedupeTargetOffers(targetOffers) {
  const seen = new Set()
  const deduped = []
  for (const target of Array.isArray(targetOffers) ? targetOffers : []) {
    const offerId = String((target && target.offerId) || '').trim()
    if (!offerId || seen.has(offerId)) continue
    seen.add(offerId)
    deduped.push({ ...target, offerId })
  }
  return deduped
}

function sectionHtmlToText(value) {
  return sanitizeSectionHtml(value).replace(/<[^>]+>/g, '').trim()
}

// 降级（Markdown）模式：从结构化字段确定性组装完整基础报告段
function renderBaseReportMarkdown({ header, title, offerId, positioning, reason, evidence, anomalies, identityWarning }) {
  const lines = [header, '']
  lines.push(`**商品**：${title || `商品 ${offerId}`}`, '')
  lines.push(`**商品 ID**：${offerId}`, '')
  if (positioning) {
    const explanation = Array.isArray(positioning.tags) && positioning.tags.length > 0
      ? `（${positioning.tags.join('、')}）`
      : ''
    lines.push(`**货盘定位**：【${positioning.label}】${explanation}`, '')
  }
  lines.push(`**选择原因**：${sectionHtmlToText(reason)}`, '')
  if (Array.isArray(evidence) && evidence.length > 0) {
    lines.push('**数据依据**：', '')
    for (const entry of evidence) {
      lines.push(`- ${entry.label}：${entry.value}${entry.unit || ''}`)
    }
    lines.push('')
  }
  if (Array.isArray(anomalies) && anomalies.length > 0) {
    lines.push('**异常项**：', '')
    for (const anomaly of anomalies) {
      const titleText = String(anomaly.title || '').trim()
      const descriptionText = sectionHtmlToText(anomaly.description)
      lines.push(`- ${[titleText, descriptionText].filter(Boolean).join('：')}`)
    }
    lines.push('')
  }
  if (identityWarning) lines.push(`> ${identityWarning}`, '')
  return lines.join('\n')
}

function buildOverviewMetric(code, label, value, unit) {
  const valueText = String(value)
  const resolvedUnit = valueText === '--' ? '' : (unit || '')
  return {
    code,
    label,
    value: valueText,
    unit: resolvedUnit,
    display: sectionColorSpan(valueText, SECTION_PALETTE.emphasis)
      + (resolvedUnit ? sectionColorSpan(resolvedUnit, SECTION_PALETTE.secondary) : ''),
  }
}

function buildOverviewPayload(reportItems) {
  const successItems = (Array.isArray(reportItems) ? reportItems : []).filter(item => item && item.status === 'success' && item.stats)
  let payBuyerTotal = 0
  let uvTotal = 0
  let payBuyerMetricCount = 0
  let uvMetricCount = 0
  let adSpendMetricCount = 0
  let adNoConversionCount = 0
  let attributeAnomalyCount = 0
  for (const item of successItems) {
    const payBuyers = Number(item.stats.payBuyer12m)
    const visitors = Number(item.stats.uv12m ?? item.stats.ipvuv12m)
    const adSpend = Number(item.stats.adSpend6w)
    if (Number.isFinite(payBuyers)) {
      payBuyerTotal += payBuyers
      payBuyerMetricCount += 1
    }
    if (Number.isFinite(visitors)) {
      uvTotal += visitors
      uvMetricCount += 1
    }
    if (Number.isFinite(adSpend)) {
      adSpendMetricCount += 1
      if (adSpend > 0 && Number(item.stats.adPayByr6w) === 0) adNoConversionCount += 1
    }
    if ((item.anomalies || []).some(anomaly => {
      const code = String((anomaly && anomaly.code) || '').toUpperCase()
      return /(ATTRIBUTE|ATTR_|MATERIAL|FABRIC|SPECIFICATION|PARAMETER)/.test(code)
    })) attributeAnomalyCount += 1
  }
  const conversionRate = payBuyerMetricCount > 0 && uvMetricCount > 0
    ? (uvTotal > 0 ? ((payBuyerTotal / uvTotal) * 100).toFixed(1) : '0')
    : '--'
  const metrics = [
    buildOverviewMetric('CONVERSION_RATE', '转化率', conversionRate, '%'),
    buildOverviewMetric('PAY_BUYER', '支付人数', payBuyerMetricCount > 0 ? payBuyerTotal : '--', '人'),
    buildOverviewMetric('AD_NO_CONVERSION', '广告投入未转化', adSpendMetricCount > 0 ? adNoConversionCount : '--', '款'),
    buildOverviewMetric('ATTRIBUTE_ANOMALY', '属性数据异常', attributeAnomalyCount, '款'),
  ]
  const counts = new Map()
  const bump = (code, label) => {
    if (!code) return
    const existing = counts.get(code) || { code, label, count: 0 }
    existing.count += 1
    counts.set(code, existing)
  }
  for (const item of successItems) {
    if (item.positioning) {
      bump(item.positioning.code, item.positioning.label)
    }
  }
  return { metrics, positionCounts: Array.from(counts.values()) }
}

function buildOneClickProductOptimizations(candidates) {
  const grouped = new Map()
  for (const candidate of Array.isArray(candidates) ? candidates : []) {
    const offerId = String((candidate && candidate.offerId) || '').trim()
    const opKey = String((candidate && candidate.canonicalKey) || '').trim()
    const label = String((candidate && candidate.actionLabel) || '').trim()
    if (!/^\d{1,30}$/.test(offerId) || !opKey || !label) continue
    const product = grouped.get(offerId) || {
      offerId,
      title: String(candidate.title || `商品 ${offerId}`).replace(/[\r\n]+/g, ' ').trim(),
      optimizationPoints: [],
    }
    if (!product.optimizationPoints.some(point => point.opKey === opKey)) {
      product.optimizationPoints.push({ opKey, label })
    }
    grouped.set(offerId, product)
  }
  return Array.from(grouped.values()).filter(product => product.optimizationPoints.length > 0)
}

const REPORT_CACHE_PREFIX = '.report-cache-'

// agent 的 Glob/相对 Write 以会话工作目录为根（如 Workspace/<id>/seller），
// 而 baseDir 在兄弟树 Workspace/<id>/skills/<category>/<skill> 下，缓存放 baseDir
// 时 Glob 搜不到、只能全盘 find。这里从 baseDir 反推工作目录（skills 的父目录 +
// 类目角色目录），缓存优先落到工作目录让 agent 一次 Glob 命中。
function resolveAgentWorkspaceDir() {
  const parts = String(baseDir).split(/[/\\]+/)
  const skillsIndex = parts.lastIndexOf('skills')
  if (skillsIndex < 1 || skillsIndex + 1 >= parts.length) return ''
  const role = parts[skillsIndex + 1].replace(/^newton_/, '')
  if (!role) return ''
  return parts.slice(0, skillsIndex).join('/') + '/' + role
}

// 报告全文预写缓存：用户点击"导出报告"时，workflow 返回里的 <export_report_markdown>
// 可能已被上下文压缩丢失，agent 按回填 prompt 里的编号定位缓存文件 Read 即可导出，
// 不再依赖会话上下文，也杜绝 agent 搜索/读取工作区 JSON 等救援行为。
// 报告全文可达数十 KB，两条写入路径都不把正文裸放进命令行：
// - posix：heredoc 一次写完。单引号 delimiter 下 bash 对正文不做任何处理（不展开
//   $VAR、不处理反引号与转义），逐字节原样落盘，一次 callTool 约 0.5 秒。
// - cmd：没有 heredoc，而报告正文必然含 %（“支付金额下跌 30%”）与半角 !，直接进
//   命令行会被变量展开静默吃掉一段且退出码仍为 0，只能先整体 base64
//   再按 4 的倍数切块追加（base64 输出集不含任何 shell 元字符）。
// 写完读回字节数与原文比对，不一致即判缓存失败并降级，把“静默丢内容”变成可感知的失败。
const REPORT_CACHE_B64_CHUNK_SIZE = 6000 // 必须是 4 的倍数；约对应 4500 字节原文，留出 cmd 8191 上限的固定开销
const REPORT_CACHE_TIMEOUT_MS = 30000
// 平台分支的固有风险是“mac 只跑 heredoc、Windows 只跑分块，各自的 bug 对方测不到”。
// 置 true 可在 mac 上强制走 Windows 分块路径，用于本地验证该分支。
const FORCE_CHUNK_WRITE = false
const APPEND_B64_PY = [
  'import sys, base64',
  'path, mode, payload = sys.argv[1:4]',
  'with open(path, mode) as f:',
  '    f.write(base64.b64decode(payload))',
].join('\n')
const CACHE_SIZE_PY = [
  'import sys, os',
  'sys.stdout.write(str(os.path.getsize(sys.argv[1])))',
].join('\n')
const PRUNE_CACHE_PY = [
  'import sys, glob, os',
  'cache_dir, prefix = sys.argv[1:3]',
  'caches = sorted(glob.glob(os.path.join(cache_dir, prefix + "*.md")), key=os.path.getmtime, reverse=True)',
  'for stale in caches[5:]:',
  '    try:',
  '        os.unlink(stale)',
  '    except OSError:',
  '        pass',
].join('\n')

// delimiter 只需不与正文任意整行相等（bash 按整行精确匹配终止符）。
function pickHeredocDelimiter(content) {
  const lines = new Set(String(content).split('\n'))
  let delimiter = 'WFHEREDOC_END'
  while (lines.has(delimiter)) {
    delimiter += '_' + Math.random().toString(36).slice(2, 6)
  }
  return delimiter
}

// 返回预期落盘字节数；heredoc 每行带行尾换行，文件固定比原文多一个 \n。
async function writeReportCacheByHeredoc(cachePath, content) {
  const delimiter = pickHeredocDelimiter(content)
  await callTool('Bash', {
    command: `cat > ${shellEscape(cachePath, 'posix')} << '${delimiter}'\n${content}\n${delimiter}`,
    timeout: REPORT_CACHE_TIMEOUT_MS,
    description: '写入报告缓存',
  })
  return utf8Bytes(content).length + 1
}

// base64 是「4 字符 ↔ 3 字节」分组编码，必须先整体编码再按 4 的倍数切；
// 先切原文再分别编码拼接会造成解码失败或错位。
async function writeReportCacheByChunks(cachePath, content) {
  const bytes = utf8Bytes(content)
  const encoded = toBase64(bytes)
  const chunks = []
  for (let offset = 0; offset < encoded.length; offset += REPORT_CACHE_B64_CHUNK_SIZE) {
    chunks.push(encoded.slice(offset, offset + REPORT_CACHE_B64_CHUNK_SIZE))
  }
  if (chunks.length === 0) chunks.push('')
  for (let index = 0; index < chunks.length; index++) {
    // 首块用 wb 直接截断旧文件，后续块 ab 追加
    const result = await runPython(
      ['-c', APPEND_B64_PY, cachePath, index === 0 ? 'wb' : 'ab', chunks[index]],
      { timeout: REPORT_CACHE_TIMEOUT_MS, description: `写入报告缓存 ${index + 1}/${chunks.length}` }
    )
    if (result.exitCode !== 0) {
      throw new Error(String(result.stderr || '').slice(0, 200) || '报告缓存分块写入失败')
    }
  }
  return bytes.length
}

async function readReportCacheByteSize(cachePath) {
  const result = await runPython(
    ['-c', CACHE_SIZE_PY, cachePath],
    { timeout: REPORT_CACHE_TIMEOUT_MS, description: '校验报告缓存' }
  )
  if (result.exitCode !== 0) return -1
  const size = parseInt(String(result.stdout).trim(), 10)
  return Number.isFinite(size) ? size : -1
}

async function writeReportCache(reportId, content) {
  const fileName = `${REPORT_CACHE_PREFIX}${reportId}.md`
  const workspaceDir = resolveAgentWorkspaceDir()
  const candidateDirList = workspaceDir ? [workspaceDir, baseDir] : [baseDir]
  const body = String(content == null ? '' : content)
  const useChunkWrite = FORCE_CHUNK_WRITE || (await resolveShellDialect()) === 'cmd'
  for (const cacheDir of candidateDirList) {
    const cachePath = `${cacheDir}/${fileName}`
    try {
      const expectedBytes = useChunkWrite
        ? await writeReportCacheByChunks(cachePath, body)
        : await writeReportCacheByHeredoc(cachePath, body)
      const actualBytes = await readReportCacheByteSize(cachePath)
      if (actualBytes !== expectedBytes) {
        log(`report cache size mismatch in ${cacheDir}: expected=${expectedBytes} actual=${actualBytes}`)
        continue
      }
      const pruned = await runPython(
        ['-c', PRUNE_CACHE_PY, cacheDir, REPORT_CACHE_PREFIX],
        { timeout: REPORT_CACHE_TIMEOUT_MS, description: '清理陈旧报告缓存' }
      )
      if (pruned.exitCode !== 0) {
        log(`report cache prune failed in ${cacheDir}: ${String(pruned.stderr || '').slice(0, 200)}`)
      }
      return { cachePath, inWorkspace: cacheDir === workspaceDir }
    } catch (error) {
      log(`report cache write error in ${cacheDir}: ${String((error && error.message) || error)}`)
    }
  }
  return { cachePath: '', inWorkspace: false }
}

function buildFooterActionsPayload({ oneClickCandidates, includeSchedule, reportCache }) {
  const actions = []
  const products = buildOneClickProductOptimizations(oneClickCandidates)
  if (products.length > 0) {
    const offers = products
      .map(product => `商品ID ${product.offerId}`)
      .join('、')
    actions.push({
      order: actions.length + 1,
      type: 'ONE_CLICK_OPTIMIZE',
      label: '一键优化商品',
      variant: 'primary',
      products,
      prompt: `请帮我一键优化以下商品：${offers} 请逐项让我确认后再执行。`,
      enabled: true,
    })
  }
  const cacheLocationText = reportCache && reportCache.inWorkspace
    ? '当前工作目录'
    : '本 skill 根目录（cli.py 所在目录）'
  actions.push({
    order: actions.length + 1,
    type: 'EXPORT_REPORT',
    label: '导出报告',
    prompt: reportCache && reportCache.cachePath
      ? `请将刚才的商品体检报告导出为一个 Markdown 文件，文件名固定为“商品体检报告.md”。全文已缓存在${cacheLocationText}，Read 后调用一次 Write 原样写入`
      : '请将刚才的商品体检报告导出为一个 Markdown 文件，文件名固定为“商品体检报告.md”。',
    enabled: true,
  })
  if (includeSchedule) {
    actions.push({
      order: actions.length + 1,
      type: 'SCHEDULE_TASK',
      label: '设置定时任务',
      prompt: `请帮我设置“1688商品自动体检”定时任务，任务执行内容固定为：“${AUTO_DIAGNOSIS_TASK_QUERY}”。请先询问执行频率和时间，再打开定时任务设置让我确认；不要自动修改商品。`,
      enabled: true,
    })
  }
  return { actions }
}

function buildReportCompletedPayload(results) {
  const latestByOfferId = new Map()
  for (const item of Array.isArray(results) ? results : []) {
    const offerId = String((item && item.offerId) || '').trim()
    if (!offerId) continue
    latestByOfferId.set(offerId, { ...item, offerId })
  }
  const list = Array.from(latestByOfferId.values())
    .sort((left, right) => (left.ordinal ?? 0) - (right.ordinal ?? 0))
  const total = list.length
  const failed = list.filter(item => item.status !== 'success').length
  const completed = total - failed
  return {
    status: total === 0 || completed === 0 ? 'failed' : (failed === 0 ? 'success' : 'partial'),
    completed,
    failed,
    total,
    products: list.map(item => ({ offerId: String(item.offerId), ordinal: item.ordinal, status: item.status === 'success' ? 'success' : 'failed' })),
  }
}

function buildReportCompletionSnapshot(targetOffers, allReports) {
  const successfulOfferIds = new Set(
    (Array.isArray(allReports) ? allReports : [])
      .map(item => String((item && item.offerId) || '').trim())
      .filter(Boolean)
  )
  return buildReportCompletedPayload(
    (Array.isArray(targetOffers) ? targetOffers : []).map((target, ordinal) => ({
      offerId: String((target && target.offerId) || '').trim(),
      ordinal,
      status: successfulOfferIds.has(String((target && target.offerId) || '').trim()) ? 'success' : 'failed',
    }))
  )
}

function resolveReportQueryStatus(reportCompletedPayload, completedSteps) {
  const completed = Number(reportCompletedPayload?.completed) || 0
  const failed = Number(reportCompletedPayload?.failed) || 0
  const selected = Number(reportCompletedPayload?.total) || completed + failed
  if (selected > 0 && completed === 0) return 'failed'
  if (completed > 0 && failed > 0) return 'partial'
  return Array.isArray(completedSteps) && completedSteps.every(step => step.status === 'done')
    ? 'fulfilled'
    : 'partial'
}

function buildAutomaticIncompleteReportSection(targetOffers, allReports, reportOutcomes) {
  const successfulOfferIds = new Set(
    (Array.isArray(allReports) ? allReports : [])
      .map(item => String((item && item.offerId) || '').trim())
      .filter(Boolean)
  )
  const outcomeByOfferId = new Map(
    (Array.isArray(reportOutcomes) ? reportOutcomes : [])
      .filter(outcome => outcome && outcome.offerId !== undefined && outcome.offerId !== null)
      .map(outcome => [String(outcome.offerId).trim(), outcome])
  )
  const lines = (Array.isArray(targetOffers) ? targetOffers : [])
    .map(target => String((target && target.offerId) || '').trim())
    .filter(offerId => offerId && !successfulOfferIds.has(offerId))
    .map(offerId => `- 商品 ID ${offerId}：${getMerchantSafeReportFailureMessage(outcomeByOfferId.get(offerId))}`)
  return lines.length > 0 ? `### 未完成商品\n\n${lines.join('\n')}` : ''
}
// ─── end 商品诊断隐藏数据流式协议 ───


function extractProductTitleFromReport(report) {
  const match = String(report || '').match(/^\s*(?:\*\*)?商品(?:\*\*)?\s*[：:]\s*(.+?)\s*$/m)
  return match ? match[1].replace(/\*\*/g, '').trim() : ''
}

function splitLegacyRecommendations(report) {
  const lines = String(report || '').split('\n')
  const inlineHeaderPattern = /^\s*(?:[-*●•]\s*)?(?:\*{0,2})?(?:优化建议|优化)(?:\*{0,2})?\s*[：:]\s*(.*)$/
  const headingPattern = /^\s*(?:#{1,6}\s+|\*{1,2})(?:优化建议|优化)(?:\*{1,2})?\s*[：:]?\s*$/
  const start = lines.findIndex(line => inlineHeaderPattern.test(line) || headingPattern.test(line))
  if (start < 0) return { report: String(report || '').trim(), recommendations: [] }

  const recommendations = []
  const inline = lines[start].match(inlineHeaderPattern)?.[1]
  if (inline) recommendations.push(inline)
  let end = lines.length
  for (let index = start + 1; index < lines.length; index++) {
    if (/^\s*#{1,6}\s+/.test(lines[index]) || /^\s*---+\s*$/.test(lines[index])) {
      end = index
      break
    }
    recommendations.push(lines[index])
  }
  const remaining = [...lines.slice(0, start), ...lines.slice(end)]
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
  return { report: remaining, recommendations: normalizeRecommendations(recommendations) }
}

function formatComprehensiveRecommendations(baseRecommendations, lessonsToLearn) {
  const merged = []
  const seen = new Set()
  for (const recommendation of [
    ...normalizeRecommendations(baseRecommendations),
    ...normalizeRecommendations(lessonsToLearn),
  ]) {
    const key = recommendation.toLowerCase().replace(/[\s，。；、：:,.!?！？]/g, '')
    if (!key || seen.has(key)) continue
    seen.add(key)
    merged.push(recommendation)
  }
  if (merged.length === 0) return ''
  return `#### 综合优化建议\n\n${merged.map(item => `- ${item}`).join('\n')}`
}

function mergeActionCandidates(reports) {
  const candidates = new Map()
  const unsupported = []
  const add = (report, rawAction, source, evidence = '') => {
    const rule = canonicalizeAction(rawAction)
    if (!rule) {
      if (rawAction) unsupported.push({ offerId: report.offerId, action: String(rawAction), source })
      return
    }
    const key = `${report.offerId}:${rule.key}`
    const current = candidates.get(key) || {
      offerId: report.offerId,
      title: report.title || '',
      loginId: report.loginId || '',
      canonicalKey: rule.key,
      actionLabel: rule.label,
      sources: [],
      rawActions: [],
      evidences: [],
    }
    if (!current.sources.includes(source)) current.sources.push(source)
    if (!current.rawActions.includes(rawAction)) current.rawActions.push(rawAction)
    if (evidence && !current.evidences.includes(evidence)) current.evidences.push(evidence)
    candidates.set(key, current)
  }
  for (const report of reports) {
    for (const candidate of report.diagnosisActionCandidates || []) add(report, candidate?.action, 'diagnosis', candidate?.evidence)
    if (report.sameSecondCategory === true) {
      for (const candidate of report.v2ActionCandidates || []) add(report, candidate?.action, 'competitionV2', candidate?.evidence)
    }
    for (const action of report.productLibraryActions || []) add(report, action, 'productLibrary')
  }
  return { candidates: Array.from(candidates.values()), unsupported }
}

function buildActionSummary(candidates) {
  return buildOneClickProductOptimizations(candidates)
    .map(product => `- ${product.title || `商品 ${product.offerId}`}（ID：${product.offerId}）：${product.optimizationPoints.map(point => point.label).join('、')}`)
    .join('\n')
}

function buildPostReportFollowupText(candidates, { includeSchedule = true, forExport = false } = {}) {
  const sections = []
  const actionSummary = buildActionSummary(candidates)
  if (actionSummary) {
    // 导出版只保留行动点清单；"回复进入一键优化"等对话交互引导只出现在对话报告里
    sections.push(forExport
      ? `以下商品可以执行一键优化：
${actionSummary}`
      : `以下商品可以执行一键优化：
${actionSummary}

需要继续时，回复“进入一键优化”。一键优化会再逐项确认执行或跳过。`)
  }
  if (includeSchedule && !forExport) {
    sections.push(`⏰需要我自动帮你找出需要优化的商品嘛？点击设置定时任务

需要配置时，回复“设置定时任务”。`)
  }
  if (sections.length === 0) return ''
  return `### 后续操作

${sections.join('\n\n')}`
}

function buildOneClickHandoff(candidates) {
  return {
    source: '1688-product-analysis',
    tasks: (Array.isArray(candidates) ? candidates : []).map(candidate => ({
      itemId: candidate.offerId,
      title: candidate.title,
      loginId: candidate.loginId,
      opKey: candidate.canonicalKey,
      actionLabel: candidate.actionLabel,
    })),
  }
}

async function extractShopName(userInput) {
  // 用 agent 语义理解是否提及具体店铺名称，避免正则误提取
  const result = parseAgentResult(await agent(
    `判断用户输入中是否提及了具体的店铺名称。\n\n用户输入："${userInput}"\n\n规则：\n- "店铺"、"我的店"、"我店"等通用词不是店铺名称\n- "店铺的商品"、"商品分析"、"异常商品"等是描述性语言，不是店铺名\n- 只有明确的公司名/店铺名才算（如"义乌市财气日用品有限公司"、"张三的店"、"好货源旗舰店"）\n- 引号包裹的内容优先视为店铺名\n\n输出：如果有具体店铺名称，返回该名称；如果没有，返回空字符串。`,
    { label: 'extract-shop-name', schema: {
      type: 'object',
      properties: { shopName: { type: 'string', description: '提取到的店铺名称，没有则为空字符串' } },
      required: ['shopName']
    }}
  ))
  return result?.shopName || ''
}

async function extractSearchKeyword(userInput) {
  const result = parseAgentResult(await agent(
    `从用户输入中提取店铺商品搜索关键词。\n\n用户输入："${userInput}"\n\n规则：\n- 只返回商品关键词，不要返回"搜索"、"查找"、"商品"等动作词\n- 如果用户用引号包裹关键词，优先使用引号内容\n- 如果没有明确关键词，返回空字符串`,
    { label: 'extract-search-keyword', schema: {
      type: 'object',
      properties: { keyword: { type: 'string', description: '商品搜索关键词，没有则为空字符串' } },
      required: ['keyword']
    }}
  ))
  return result?.keyword || ''
}

function buildScoringCliArgs(itemOverview, shopData) {
  return [
    '--shop_total', JSON.stringify(shopData || {}),
    ...chooseScoringArgs(itemOverview),
    '--top_n', '10',
  ]
}

function scoringFailureMessage(result) {
  const messages = {
    item_overview: '商品概览数据暂时无法获取，已跳过评分候选。',
    shop_data: '店铺经营数据暂时无法获取，已跳过评分候选。',
    item_scoring: '商品明细评分暂时无法完成，已跳过评分候选。',
  }
  return messages[result?.failedStage] || '商品评分结果暂时无法获取，已跳过评分候选。'
}

async function runScoringSelection(itemOverviewResult, shopDataResult) {
  if (!itemOverviewResult?.success) {
    return {
      success: false,
      failedStage: 'item_overview',
      error: itemOverviewResult?.error || '商品概览数据暂不可用',
      data: {},
    }
  }
  if (!shopDataResult?.success) {
    return {
      success: false,
      failedStage: 'shop_data',
      error: shopDataResult?.error || '店铺经营数据暂不可用',
      data: {},
    }
  }
  const scoreResult = await runCliWithSmartRetry(
    'score_and_select',
    buildScoringCliArgs(itemOverviewResult.data, shopDataResult.data),
    { commandDesc: '商品评分分层' }
  )
  return scoreResult.success
    ? scoreResult
    : { ...scoreResult, failedStage: 'item_scoring' }
}

let selectionTerminalReason = ''

function stopSelection(reason, message = '') {
  selectionTerminalReason = reason
  if (message) emit(message)
  return []
}

function isUserSelectionCancellation(reason) {
  return reason === '用户已跳过商品选择' || reason === '用户未选择商品'
}

function buildSelectionTermination(completedSteps, reason, executionMode = 'interactive') {
  const cancelled = isUserSelectionCancellation(reason)
  const resolvedReason = reason || '未获取到有效商品 ID'
  const manifest = {
    completedSteps,
    queryStatus: cancelled ? 'cancelled' : 'failed',
    terminal: cancelled,
    shouldRetry: !cancelled,
    reason: resolvedReason,
    ...(executionMode === 'automatic' ? {
      executionMode: 'automatic',
      delivery: 'markdown',
      componentLaunchState: 'skipped',
      sectionStreamState: 'skipped',
      scheduleDeduplicationStatus: executionMode === 'automatic' ? 'skipped' : undefined,
      selectedCount: 0,
      completed: 0,
      failed: 0,
      products: [],
    } : {}),
  }

  if (cancelled) {
    return `商品诊断工作流已按用户选择正常结束。用户未选择要诊断的商品。不得自动重试、重新展示候选表或继续调用工具。

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify(manifest, null, 2)}
</execution_manifest>`
  }

  return `商品诊断工作流因未获取到有效商品 ID 而终止。

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify(manifest, null, 2)}
</execution_manifest>`
}

function createDiagnosisProgressEmitter(executionMode) {
  return message => {
    if (executionMode !== 'automatic') emit(message)
  }
}

async function askManualOfferId(message) {
  if (message) emit(message)
  const interaction = await safeShowInteraction({
    type: 'input',
    selectionType: 'input_offer_id',
    questions: [{
      question: '请输入要体检的商品 ID：',
      type: 'input',
      placeholder: '请输入10位以上的商品ID',
    }],
  })
  if (!interaction.ok) {
    return stopSelection('交互超时', '选择组件超时，本次未开始深度诊断；请直接回复商品 ID 重试。')
  }
  const manualOfferIds = parseManualOfferIds(extractAnswerFromInteraction(interaction.result))
  if (manualOfferIds.length === 0) {
    return stopSelection('未输入有效商品 ID', '没有识别到有效商品 ID，本次体检已结束。')
  }
  return manualOfferIds
    .map(offerId => ({ offerId, loginId: '', shopName: '', title: '' }))
}

async function askSearchKeyword() {
  const interaction = await safeShowInteraction({
    type: 'input',
    selectionType: 'input_search_keyword',
    questions: [{
      question: '请输入要搜索的商品关键词：',
      type: 'input',
      placeholder: '例如：护眼套装',
    }],
  })
  if (!interaction.ok) {
    stopSelection('交互超时', '选择组件超时，本次未开始深度诊断；请直接回复商品 ID 重试。')
    return null
  }
  return String(extractAnswerFromInteraction(interaction.result) || '').trim()
}

async function chooseProductLocator(message, requestedCount) {
  emit(message)
  const interaction = await safeShowInteraction({
    type: 'card',
    selectionType: 'choose_product_locator',
    questions: [{
      question: '请选择一种方式继续定位商品：',
      options: ['输入商品 ID', '关键词搜索'],
    }],
  })
  if (!interaction.ok) {
    return stopSelection('交互超时', '选择组件超时，本次未开始深度诊断；请直接回复商品 ID 重试。')
  }
  const choice = extractAnswerFromInteraction(interaction.result)
  if (choice === '输入商品 ID') return askManualOfferId('')
  if (choice === '关键词搜索') {
    const keyword = await askSearchKeyword()
    if (keyword === null) return []
    if (!keyword) return stopSelection('未输入搜索关键词', '没有输入搜索关键词，本次体检已结束。')
    return searchOffersByKeyword(keyword, requestedCount)
  }
  return stopSelection('未选择商品定位方式', '没有选择商品定位方式，本次体检已结束。')
}

async function selectDiagnosisCandidates(candidates, { kind = 'abnormal', title, includeDiscoverySource = false, requestedCount = null, emptyMessage = '当前没有可选商品。', executionMode = 'interactive' } = {}) {
  if (executionMode === 'automatic') {
    return selectTopCandidates(candidates, requestedCount || 5)
  }
  if (!Array.isArray(candidates) || candidates.length === 0) return chooseProductLocator(emptyMessage, requestedCount)
  const rankedCandidates = prioritizeDiagnosisCandidates(candidates)

  if (requestedCount !== null) {
    const targetOffers = selectTopCandidates(rankedCandidates, requestedCount)
    if (targetOffers.length < requestedCount) {
      emit(`目前只找到 ${targetOffers.length} 件符合条件的商品，已全部开始体检。`)
    } else {
      emit(`已按优先级选出 ${targetOffers.length} 件商品，开始体检。`)
    }
    return targetOffers
  }

  emit(`已找到 ${rankedCandidates.length} 件候选商品，请在下方选择要体检的商品。`)
  const tableSpec = buildCandidateTableSpec(rankedCandidates, { kind, title, includeDiscoverySource })

  const interaction = await safeShowInteraction({
    type: 'table',
    selectionType: tableSpec.selectionType,
    title: tableSpec.title,
    columns: tableSpec.columns,
    rows: tableSpec.rows,
  })
  if (!interaction.ok) {
    return stopSelection('交互超时', '选择组件超时，本次未开始深度诊断；请直接回复商品 ID 重试。')
  }

  const selectedData = interaction.result?.data
  if (selectedData?.action === 'skip') {
    return stopSelection('用户已跳过商品选择', '你已跳过商品选择，本次体检已结束。')
  }
  if (
    !selectedData
    || Array.isArray(selectedData)
    || selectedData.action !== 'confirm'
    || !Array.isArray(selectedData.selectedRows)
    || selectedData.selectedRows.length === 0
  ) {
    return stopSelection('用户未选择商品', '你没有选择商品，本次体检已结束。')
  }

  const selected = selectedData.selectedRows
    .map(row => candidateToTargetOffer(row?._candidate || row))
    .filter(item => item.offerId)
  if (selected.length === 0) {
    return stopSelection('用户未选择商品', '你没有选择商品，本次体检已结束。')
  }
  return selected
}

async function handleKeywordSearch(userInput, requestedCount) {
  const keyword = await extractSearchKeyword(userInput)
  if (!keyword) {
    const manualKeyword = await askSearchKeyword()
    if (manualKeyword === null) return []
    if (!manualKeyword) return stopSelection('未输入搜索关键词', '没有输入搜索关键词，本次体检已结束。')
    return searchOffersByKeyword(manualKeyword, requestedCount)
  }
  return searchOffersByKeyword(keyword, requestedCount)
}

async function searchOffersByKeyword(keyword, requestedCount) {
  const tryKeywords = [keyword]
  const seen = new Set(tryKeywords)
  for (let attempt = 0; attempt < tryKeywords.length && attempt < 4; attempt++) {
    const currentKeyword = tryKeywords[attempt]
    const result = await runCliWithSmartRetry(
      'search_offer_by_keyword',
      ['--keyword', currentKeyword],
      { commandDesc: '商品关键词搜索' }
    )
    if (!result.success) {
      return stopSelection('商品搜索失败', '商品搜索暂时失败，请稍后重试。')
    }
    const items = extractSearchItems(result.data).map(toCandidateFromSearch).filter(item => item.offerId)
    if (items.length === 1 && requestedCount === null) {
      emit('已找到 1 件匹配商品，开始体检。')
      return [candidateToTargetOffer(items[0])]
    }
    if (items.length > 0) {
      return selectDiagnosisCandidates(items, {
        kind: 'search',
        title: `搜索结果：${currentKeyword}`,
        requestedCount,
        emptyMessage: '没有选定要体检的商品，请输入商品 ID。',
      })
    }
    if (attempt === 0) {
      const alternatives = parseAgentResult(await agent(
        `用户搜索关键词"${currentKeyword}"没有匹配商品。请给出最多 3 个更短、更常见的相似商品关键词。\n只返回 JSON。`,
        { label: 'keyword-alternatives', schema: {
          type: 'object',
          properties: { keywords: { type: 'array', items: { type: 'string' } } },
          required: ['keywords']
        }}
      ))?.keywords || []
      for (const alt of alternatives.slice(0, 3)) {
        const normalized = String(alt || '').trim()
        if (normalized && !seen.has(normalized)) {
          seen.add(normalized)
          tryKeywords.push(normalized)
        }
      }
    }
  }
  return askManualOfferId('没有找到匹配商品，你可以直接输入要体检的商品 ID。')
}

async function handlePositiveSelection() {
  phase('确定体检商品')
  const [itemOverviewResult, shopDataResult] = await parallel([
    () => runCliWithSmartRetry('get_item_overview', [], { commandDesc: '商品概览' }),
    () => runCliWithSmartRetry('get_shop_data', [], { commandDesc: '店铺经营数据' }),
  ])
  const scoreResult = await runScoringSelection(itemOverviewResult, shopDataResult)
  if (!scoreResult.success) {
    emit(scoringFailureMessage(scoreResult))
    return {
      done: true,
      final: `正向选品流程终止：评分数据暂不可用。\n\n<execution_manifest>\n${JSON.stringify({ queryStatus: 'failed', failedStage: scoreResult.failedStage || 'unknown', reason: scoreResult.error || '评分数据暂不可用' }, null, 2)}\n</execution_manifest>`
    }
  }
  const products = (Array.isArray(scoreResult.data?.products) ? scoreResult.data.products : []).filter(isPositiveCandidate)
  if (products.length >= 2) {
    const rows = products.map(product => {
      const candidate = toCandidateFromScoring(product, '评分分层')
      return {
        id: candidate.offerId,
        title: candidate.title,
        level: candidate.level,
        levelName: candidate.levelName,
        totalScore: candidate.totalScore,
        payAmount: candidate.payAmount != null ? fmtMoney(candidate.payAmount) : '-',
        buyerCount: candidate.buyerCount ?? '-',
        uv: candidate.uv ?? '-',
      }
    })
    emit(`已圈选出 ${products.length} 件重点运营候选商品。`)
    const presentation = await safeShowInteraction({
      type: 'table',
      selectionType: 'select_products_from_scoring',
      title: '重点品圈选结果',
      columns: [
        { key: 'id', label: '商品ID', width: 120 },
        { key: 'title', label: '标题' },
        { key: 'level', label: '等级', width: 80 },
        { key: 'levelName', label: '分层', width: 100 },
        { key: 'totalScore', label: '综合得分', width: 90 },
        { key: 'payAmount', label: '支付金额', width: 120 },
        { key: 'buyerCount', label: '买家数', width: 90 },
        { key: 'uv', label: '访客数', width: 90 },
      ],
      rows,
    })
    const manifest = {
      queryStatus: 'fulfilled',
      selectedCount: products.length,
      ...(presentation.ok ? {} : { presentationStatus: 'degraded' }),
    }
    return { done: true, final: `正向选品流程执行完毕。\n\n<execution_manifest>\n${JSON.stringify(manifest, null, 2)}\n</execution_manifest>` }
  }
  if (products.length === 1) {
    emit(formatPositiveCandidate(products[0]))
    return { done: true, final: `正向选品流程执行完毕。\n\n<execution_manifest>\n${JSON.stringify({ queryStatus: 'fulfilled', selectedCount: 1 }, null, 2)}\n</execution_manifest>` }
  }
  emit('当前没有合适的重点运营候选。')
  return { done: true, final: `正向选品流程执行完毕，无重点运营候选。\n\n<execution_manifest>\n${JSON.stringify({ queryStatus: 'fulfilled', selectedCount: 0 }, null, 2)}\n</execution_manifest>` }
}

async function handleProblemDiagnosis(userInput, requestedCount, stepReport, executionMode = 'interactive') {
  const progressEmit = createDiagnosisProgressEmitter(executionMode)
  phase('确定体检商品')
  const shopName = await extractShopName(userInput)
  const multiShopArgs = shopName ? ['--shop_name', shopName] : []
  const [multiShopResult, itemOverviewResult, shopDataResult] = await parallel([
    () => runCliWithSmartRetry('multi_shop_product_analysis', multiShopArgs, { commandDesc: '多店铺异常商品汇总' }),
    () => runCliWithSmartRetry('get_item_overview', [], { commandDesc: '商品概览' }),
    () => runCliWithSmartRetry('get_shop_data', [], { commandDesc: '店铺经营数据' }),
  ])
  const abnormalSource = inspectAbnormalSource(multiShopResult)
  stepReport.push({
    step: '多店铺异常商品汇总',
    status: !abnormalSource.available ? 'failed' : abnormalSource.failedShopNames.length > 0 ? 'partial' : 'done',
    detail: abnormalSource.error || '成功',
  })
  if (!abnormalSource.available) {
    progressEmit('异常商品数据暂时无法获取。')
  } else if (abnormalSource.failedShopNames.length > 0) {
    progressEmit(`以下店铺暂时未能完成检查：${abnormalSource.failedShopNames.join('、')}，其余店铺结果已正常获取。`)
  }

  const abnormalCandidates = abnormalSource.candidates
  const scoreResult = await runScoringSelection(itemOverviewResult, shopDataResult)
  const scoringCandidates = scoreResult.success
    ? (Array.isArray(scoreResult.data?.c_grade_candidates) ? scoreResult.data.c_grade_candidates : []).map(product => toCandidateFromScoring(product)).filter(item => item.offerId)
    : []
  stepReport.push({
    step: '商品评分分层',
    status: scoreResult.success ? 'done' : 'partial',
    detail: scoreResult.success
      ? '成功'
      : `${scoreResult.failedStage || 'unknown'}: ${scoreResult.error || '评分失败'}`,
  })
  if (!scoreResult.success) progressEmit(scoringFailureMessage(scoreResult))

  if (!abnormalSource.available && !scoreResult.success) {
    return stopSelection('异常商品和评分分层数据均不可用', '暂时无法完成商品发现，请稍后重试。')
  }
  const candidates = [...abnormalCandidates, ...scoringCandidates]
  const truncInfo = abnormalSource.available ? multiShopResult.data?.truncation_info : null
  if (truncInfo && truncInfo.truncated) {
    const shopsList = (truncInfo.shops_with_items || []).join('、')
    progressEmit(`⚠️ 当前共检测到 ${truncInfo.total_before_truncation} 条异常商品，涉及店铺：${shopsList}。为保证展示效果，表格仅展示跌幅最严重的 ${truncInfo.total_after_truncation} 条，如需查看其他商品可输入商品 ID 进行诊断。`)
  }
  return selectDiagnosisCandidates(candidates, {
    kind: abnormalCandidates.length === 0 && scoringCandidates.length > 0 ? 'scoring' : 'abnormal',
    title: abnormalCandidates.length > 0 && scoringCandidates.length > 0 ? '问题商品候选 — 请选择要体检的商品' : undefined,
    includeDiscoverySource: abnormalCandidates.length > 0 && scoringCandidates.length > 0,
    requestedCount,
    executionMode,
    emptyMessage: '当前没有发现需要优先体检的商品，你也可以直接输入要体检的商品 ID。',
  })
}

async function handlePureDiagnosis(userInput, requestedCount, stepReport, executionMode = 'interactive') {
  const progressEmit = createDiagnosisProgressEmitter(executionMode)
  phase('确定体检商品')
  const shopName = await extractShopName(userInput)
  const multiShopArgs = shopName ? ['--shop_name', shopName] : []
  const multiShopResult = await runCliWithSmartRetry(
    'multi_shop_product_analysis',
    multiShopArgs,
    { commandDesc: '多店铺异常商品汇总' }
  )
  const abnormalSource = inspectAbnormalSource(multiShopResult)
  stepReport.push({
    step: '多店铺异常商品汇总',
    status: !abnormalSource.available ? 'failed' : abnormalSource.failedShopNames.length > 0 ? 'partial' : 'done',
    detail: abnormalSource.error || '成功',
  })
  if (!abnormalSource.available) {
    return stopSelection('异常商品数据不可用', '暂时无法获取异常商品数据，请稍后重试。')
  }
  if (abnormalSource.failedShopNames.length > 0) {
    progressEmit(`以下店铺暂时未能完成检查：${abnormalSource.failedShopNames.join('、')}，其余店铺结果已正常获取。`)
  }
  const truncInfo = multiShopResult.data?.truncation_info
  if (truncInfo && truncInfo.truncated) {
    const shopsList = (truncInfo.shops_with_items || []).join('、')
    progressEmit(`⚠️ 当前共检测到 ${truncInfo.total_before_truncation} 条异常商品，涉及店铺：${shopsList}。为保证展示效果，表格仅展示跌幅最严重的 ${truncInfo.total_after_truncation} 条，如需查看其他商品可输入商品 ID 进行诊断。`)
  }
  return selectDiagnosisCandidates(abnormalSource.candidates, {
    title: '异常商品列表 — 请选择要诊断的商品',
    requestedCount,
    executionMode,
    emptyMessage: '当前没有需要关注的异常商品，你也可以直接输入要体检的商品 ID。',
  })
}

// ─── 主流程 ───

const stepReport = []
const userInput = (typeof args === 'string' && args.trim()) ? args.trim() : ''
const MAX_DIAGNOSIS_CONCURRENCY = 5
const requestedDiagnosisCount = parseRequestedDiagnosisCount(userInput)

// 检查用户是否已明确提供 offer_id（直接跳到数据采集）
const directOfferIds = parseManualOfferIds(userInput)
const hasDirectOfferId = directOfferIds.length > 0
const executionMode = await detectDiagnosisExecutionMode(userInput)
const intentBranch = classifyIntent(userInput, hasDirectOfferId)
const progressEmit = createDiagnosisProgressEmitter(executionMode)

// ─── 阶段 A：确定目标商品列表 ───
let targetOffers = [] // [{offerId, loginId, shopName}, ...]
let idFromManualInput = false // 标记 ID 是否来自用户手动输入（非表格选择）

// 快捷路径：用户直接给了商品 ID，先验证有效性
if (executionMode !== 'automatic' && hasDirectOfferId) {
  phase('确定体检商品')
  const verificationJobs = directOfferIds.map((candidateId, ordinal) => ({
    offerId: candidateId,
    ordinal,
    run: async () => {
      log(`用户直接提供 offer_id: ${candidateId}，正在验证...`)
      const aggregate = await queryItemDiagnosisContext(candidateId)
      const checkLookup = aggregate.offerLookup
      if (hasUsableOfferData(checkLookup.result)) {
        const target = fillTargetFromDiagnosisContext({
          offerId: candidateId,
          title: '',
        }, aggregate.context)
        return {
          success: true,
          offerId: candidateId,
          ordinal,
          target,
        }
      }
      return {
        success: false,
        offerId: candidateId,
        ordinal,
        result: checkLookup.result,
        lookupMiss: isOfferLookupMiss(checkLookup.result),
      }
    },
  }))
  const verificationOutcomes = await executeReportJobs(
    verificationJobs,
    parallel,
    () => {},
    MAX_DIAGNOSIS_CONCURRENCY
  )
  for (const outcome of verificationOutcomes.sort((left, right) => left.ordinal - right.ordinal)) {
    if (outcome.success) {
      targetOffers.push({
        ...outcome.target,
      })
      continue
    }
    emit(outcome.lookupMiss
      ? `没有找到商品 ${outcome.offerId}，已跳过。`
      : `商品 ${outcome.offerId} 暂时无法读取，已跳过。`)
    stepReport.push({
      step: `商品${outcome.offerId}ID验证`,
      status: 'failed',
      detail: outcome.lookupMiss
        ? `${outcome.offerId} 未归属任何绑定店铺`
        : (outcome.result?.error || '校验失败'),
    })
  }
  if (targetOffers.length === 0) {
    return `商品诊断工作流终止：用户提供的商品 ID 均校验失败。

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify({ completedSteps: stepReport, queryStatus: 'failed', reason: '用户提供的商品 ID 均校验失败' }, null, 2)}
</execution_manifest>`
  }
}

// 标准选择路径（无直接 ID 或直接 ID 无效时执行）
const dispatchIntentBranch = executionMode === 'automatic' ? 'problem_diagnosis' : intentBranch
if (targetOffers.length === 0) {
  if (dispatchIntentBranch === 'keyword_search') {
    phase('确定体检商品')
    targetOffers = await handleKeywordSearch(userInput, requestedDiagnosisCount)
    idFromManualInput = targetOffers.length > 0 && !targetOffers[0].title
  } else if (dispatchIntentBranch === 'positive_selection') {
    const positiveResult = await handlePositiveSelection()
    if (positiveResult?.done) return positiveResult.final
  } else if (dispatchIntentBranch === 'problem_diagnosis') {
    targetOffers = await handleProblemDiagnosis(userInput, requestedDiagnosisCount, stepReport, executionMode)
    idFromManualInput = targetOffers.length > 0 && !targetOffers[0].title
  } else {
    targetOffers = await handlePureDiagnosis(userInput, requestedDiagnosisCount, stepReport, executionMode)
    idFromManualInput = targetOffers.length > 0 && !targetOffers[0].title
  }
}

// ─── 前置校验（区分未输入 vs 输入无效） ───
if (targetOffers.length === 0) {
  if (executionMode === 'automatic' && !selectionTerminalReason) {
    return `本次未找到可诊断的商品，已正常结束，无需输入商品 ID 或关键词。

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify({ completedSteps: stepReport, executionMode, delivery: 'markdown', queryStatus: 'fulfilled', selectedCount: 0, completed: 0, failed: 0, products: [], componentLaunchState: 'skipped', sectionStreamState: 'skipped', scheduleDeduplicationStatus: 'skipped' }, null, 2)}
</execution_manifest>`
  }
  if (!selectionTerminalReason) emit('还没有选定要体检的商品，请重新选择或输入商品 ID。')
  return buildSelectionTermination(stepReport, selectionTerminalReason, executionMode)
}

// 不同发现来源可能命中同一商品；进入归属校验、catalog 和诊断任务前统一按首次出现去重。
targetOffers = dedupeTargetOffers(targetOffers)

// 如果是用户手动输入的 ID（非表格选择），验证其有效性
if (idFromManualInput && targetOffers.length > 0) {
  const verificationJobs = targetOffers.map((target, ordinal) => ({
    offerId: target.offerId,
    ordinal,
    run: async () => {
      const aggregate = await queryItemDiagnosisContext(target.offerId)
      const verifyLookup = aggregate.offerLookup
      if (hasUsableOfferData(verifyLookup.result)) {
        return {
          success: true,
          offerId: target.offerId,
          ordinal,
          target: fillTargetFromDiagnosisContext(target, aggregate.context),
        }
      }
      return {
        success: false,
        offerId: target.offerId,
        ordinal,
        result: verifyLookup.result,
        lookupMiss: isOfferLookupMiss(verifyLookup.result),
      }
    },
  }))
  const verificationOutcomes = await executeReportJobs(
    verificationJobs,
    parallel,
    () => {},
    MAX_DIAGNOSIS_CONCURRENCY
  )
  const verifiedManualOffers = []
  for (const outcome of verificationOutcomes.sort((left, right) => left.ordinal - right.ordinal)) {
    if (outcome.success) {
      verifiedManualOffers.push(outcome.target)
      continue
    }
    emit(outcome.lookupMiss
      ? `没有找到商品 ${outcome.offerId}，已跳过。`
      : `商品 ${outcome.offerId} 暂时无法读取，已跳过。`)
    stepReport.push({
      step: `商品${outcome.offerId}ID验证`,
      status: 'failed',
      detail: outcome.lookupMiss ? '未归属任何绑定店铺' : (outcome.result?.error || '校验失败'),
    })
  }
  targetOffers = verifiedManualOffers
  if (targetOffers.length === 0) {
    return `商品诊断工作流终止：用户输入的商品均未通过校验。

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify({ completedSteps: stepReport, queryStatus: 'failed', reason: '用户输入的商品均未通过校验' }, null, 2)}
</execution_manifest>`
  }
}

// ─── 阶段 B/C：数据采集与诊断报告（循环执行） ───
phase('查看经营表现')

const allReports = []
const reportJobs = []
progressEmit(`<aside>本次商品体检支持经营表现诊断、同款对比和商品库建议，将检查 ${targetOffers.length} 件商品。</aside>`)
progressEmit('<aside>开始查看商品经营表现，重点核对近期流量、成交、加购和转化。</aside>')
progressEmit(`<aside>共 ${targetOffers.length} 件商品，将开始商品体检，完成后会逐件更新结果。</aside>`)

// ─── 组件唤起与隐藏流是两个独立状态：唤起失败仍发送区块，但可见交付降级 Markdown ───
const sectionReportId = generateReportId()
const sectionSeqState = { counter: 0, chain: Promise.resolve(), failed: false }
const sectionResults = targetOffers.map((target, ordinal) => ({
  offerId: target.offerId,
  ordinal,
  status: 'failed',
}))
const componentLaunch = executionMode === 'automatic'
  ? { opened: false }
  : await invokeDiagnosisComponent(sectionReportId, targetOffers.length)
const componentLaunchState = executionMode === 'automatic' ? 'skipped' : (componentLaunch.opened ? 'succeeded' : 'failed')
const sectionStreamEnabled = executionMode !== 'automatic'
let sectionStreamState = executionMode === 'automatic' ? 'skipped' : 'started'
let deliveryMode = executionMode === 'automatic' ? 'markdown' : (componentLaunch.opened ? 'component' : 'markdown')
const sectionStartedAt = new Date()
await hydrateDiagnosisTargetsForCatalog(targetOffers, parallel, MAX_DIAGNOSIS_CONCURRENCY)
if (sectionStreamEnabled) {
  await emitSection(sectionReportId, sectionSeqState, 'report_meta', buildReportMetaPayload(sectionStartedAt, targetOffers.length))
  await emitSection(sectionReportId, sectionSeqState, 'product_catalog', buildProductCatalogPayload(targetOffers))
}

let sectionCompletedEmitted = false
const emitReportCompletedOnce = () => {
  if (!sectionStreamEnabled || sectionCompletedEmitted) return
  sectionCompletedEmitted = true
  emitSection(sectionReportId, sectionSeqState, 'report_completed', buildReportCompletedPayload(sectionResults))
}
const finalizeSectionDelivery = async () => {
  const sectionDeliverySucceeded = sectionStreamEnabled
    ? await finalizeSectionStream(sectionSeqState, emitReportCompletedOnce)
    : true
  if (sectionStreamEnabled) sectionStreamState = sectionDeliverySucceeded ? 'succeeded' : 'failed'
  if (!sectionDeliverySucceeded) {
    deliveryMode = 'markdown'
    emit('组件区块发送失败，本次使用文字报告交付。')
  }
}

// 诊断-聚合段内赋值、段外（报告收尾与最终返回）消费的变量，声明提升到 try 之外
let merchantReportValue = ''
let candidates = []
let unsupported = []
let scheduleCheck = { success: false, data: {} }
let includeScheduleOption = false
let reportCache = { cachePath: '', inWorkspace: false }
let reportOutcomes = []
let reportCompletedPayload = buildReportCompletionSnapshot(targetOffers, allReports)
try {
  for (let i = 0; i < targetOffers.length; i++) {
    const target = targetOffers[i]
    reportJobs.push({
      offerId: target.offerId,
      ordinal: i,
      title: target.title || '',
      imageUrl: target.imageUrl || '',
      run: async () => {
        const taskStartedAt = Date.now()
        const {
          offerLookup,
          sameOfferResult,
          diagnosisActionResult,
          timing,
          inputsReadyAt,
        } = await queryProductDiagnosisInputs(target, taskStartedAt)
        const offerData = offerLookup.result
        if (!hasUsableOfferData(offerData)) {
          stepReport.push({
            step: `商品${target.offerId}数据采集`,
            status: 'failed',
            detail: offerData.error || '获取失败',
          })
          return {
            success: false,
            offerId: target.offerId,
            ordinal: i,
            title: target.title || '',
            imageUrl: target.imageUrl || '',
            errorPreset: isOfferLookupMiss(offerData) ? SECTION_ERROR_PRESET.OFFER_NOT_FOUND : SECTION_ERROR_PRESET.DATA_UNAVAILABLE,
            reason: offerData.error || '商品数据获取失败',
          }
        }

        if (offerLookup.loginId) target.loginId = offerLookup.loginId
        if (offerLookup.shopName) target.shopName = offerLookup.shopName
        const normalizedOfferData = normalizeOfferDiagnosisPayload(offerData)
        Object.assign(target, reconcileOfferIdentity(target, normalizedOfferData))

        const sameOfferStatus = classifySameOfferResult(sameOfferResult)
        const offerDiagnosisStatus = classifyOfferDiagnosisResult(diagnosisActionResult, target.offerId)
        const sameOfferData = sameOfferStatus === ENHANCEMENT_STATUS.SUCCESS ? (sameOfferResult.data || {}) : null
        const v2ActionEvidence = projectCompetitionV2ForAgent(sameOfferData)
        const diagnosisActionData = offerDiagnosisStatus === ENHANCEMENT_STATUS.SUCCESS
          ? diagnosisActionResult.data
          : null
        target.imageUrl = normalizeCandidateImageUrl(
          target.imageUrl || extractOfferImageFromDiagnosis(diagnosisActionResult, target.offerId)
        )
        stepReport.push({
          step: `商品${target.offerId}同款分析`,
          status: sameOfferStatus === ENHANCEMENT_STATUS.SUCCESS ? 'done' : 'partial',
          detail: sameOfferStatus,
        })
        stepReport.push({
          step: `商品${target.offerId}商品库行动点`,
          status: offerDiagnosisStatus === ENHANCEMENT_STATUS.SUCCESS ? 'done' : 'partial',
          detail: offerDiagnosisStatus,
        })

        const evidencePool = buildEvidencePool(deriveOfferStats(normalizedOfferData))
        let reportRaw = await runDiagnosisAgent(
      `你是 1688 商品运营专家。请为当前商品生成精简、可核验的结构化基础诊断。\n\n` +
      `## 商品数据（CLI 真实返回）\n\`\`\`${normalizedOfferData.promptFormat}\n${normalizedOfferData.promptText.substring(0, 8000)}\n\`\`\`\n\n` +
      `## 可选证据指标（evidence 只能从中选 code）\n\`\`\`json\n${JSON.stringify(evidencePool.map(entry => ({ code: entry.code, label: entry.label, value: entry.value, unit: entry.unit })))}\n\`\`\`\n\n` +
      `## 同款行动证据（仅用于 recommendations 和 actionCandidates）\n\`\`\`json\n${JSON.stringify(v2ActionEvidence || {}).substring(0, 3500)}\n\`\`\`\n\n` +
      `## 商品库行动点\n\`\`\`json\n${JSON.stringify(diagnosisActionData || {}).substring(0, 1200)}\n\`\`\`\n\n` +
      `## 选择依据\n${JSON.stringify(target.selectionEvidence || {})}\n${target.identityWarning || '候选商品与当前详情身份一致。'}\n\n` +
      `## 输出要求\n` +
      `1. reason：只写1-2句话（总≤150字）的经营数据结论，挑流量/成交/加购/转化中最突出的1-2个指标，用真实数值一句话说清问题或状态。禁止写标题宣称、类目错放、属性冲突、合规风险或身份矛盾，这些只允许进入 anomalies；数据缺失就省略，不得猜测。禁止输出颜色/HTML 标签。\n` +
      `2. reasonHighlights：从 reason 原文中选 1-6 个最值得强调的数据事实，每项格式为 {text,evidenceCodes}。text 必须是 reason 中的连续原文、不超过60字，并使用对应可选证据指标的 label 原词；evidenceCodes 只能引用已选入 evidence、并能同时支撑该片段的真实指标 code。不得整句高亮，不得输出 HTML；无可核验片段时返回空数组。\n` +
      `3. positioning.code 只能是 TRAFFIC（引流款）/STABLE（稳定款）/POTENTIAL（潜力款）之一；新品等辅助标签放 tags 字符串数组。\n` +
      `4. evidence：从可选证据指标中选 1-6 个最支持诊断的 code，并给 severity（critical/warning/info）。evidence 只输出 code 和 severity；reason 只能引用上方真实原值，禁止改写或编造指标数值。\n` +
      `5. anomalies：只写标题宣称、类目疑似错放、属性冲突、合规风险或身份矛盾等内容异常，最多2条，按 critical（红色）在前、warning 在后输出；每条 {code, level(warning/critical), title, description}，description 只写1句话。禁止复述 GMV、支付人数、访客、曝光、加购、转化率、广告消耗等经营指标；无异常返回空数组。身份矛盾仅提示数据一致性异常，不直接判定类目错放。\n` +
      `6. recommendations：1-3条 {code, priority, title, description}，priority 为数字且 1 最高，必须按优先级从高到低输出。description 只写执行步骤（改什么、怎么改、在哪改），禁止重述原因或引用指标。不写价格调整，禁止 HTML。\n` +
      `7. actionCandidates 只根据同二级类目的明确证据填写一键优化支持项：标题优化、主图优化、白底图优化、设置包邮、24H发货、三无包赔、极速开票、7天无理由、破损包赔、少货必赔、混批、一件起批、哇噢定制、一件代发、跨境资质。跨类目或证据不足时返回空数组；价格调整不得进入 actionCandidates。\n` +
      `8. reason 与 anomalies 职责必须互斥，同一问题不得在两处重复。禁止输出工具名、内部字段、原始 JSON、模型思考、认证办理建议、虚构预算或效果预测。\n` +
      `9. 只能直接返回符合 schema 的原始 JSON 对象，不要调用工具，不要输出分析过程、Markdown 代码块或额外说明。`,
      {
        label: `product-diagnosis-report-${i}`,
        schema: {
          type: 'object',
          required: ['reason', 'reasonHighlights', 'positioning', 'evidence', 'recommendations'],
          properties: {
            reason: { type: 'string', description: '≤150字经营数据结论，只写最突出的1-2个指标，纯文本' },
            reasonHighlights: {
              type: 'array',
              description: 'reason 中由真实 evidence 支撑、需要橙色强调的连续原文片段',
              items: {
                type: 'object',
                required: ['text', 'evidenceCodes'],
                properties: {
                  text: { type: 'string', description: 'reason 中的连续原文，不含 HTML' },
                  evidenceCodes: {
                    type: 'array',
                    items: { type: 'string' },
                    description: '支撑该片段且已选入 evidence 的指标 code',
                  },
                },
              },
            },
            positioning: {
              type: 'object',
              required: ['code'],
              properties: {
                code: { type: 'string', description: 'TRAFFIC/STABLE/POTENTIAL' },
                tags: { type: 'array', items: { type: 'string' }, description: '辅助标签，如 新品' },
              },
            },
            evidence: {
              type: 'array',
              items: {
                type: 'object',
                required: ['code', 'severity'],
                properties: {
                  code: { type: 'string', description: '只能来自可选证据指标列表' },
                  severity: { type: 'string', description: 'critical/warning/info' },
                },
              },
            },
            anomalies: {
              type: 'array',
              description: '标题、类目、属性、合规或身份异常，不得重复 reason 中的经营指标',
              items: {
                type: 'object',
                properties: {
                  code: { type: 'string' },
                  level: { type: 'string', description: 'warning/critical' },
                  title: { type: 'string' },
                  description: { type: 'string' },
                },
              },
            },
            recommendations: {
              type: 'array',
              items: {
                type: 'object',
                required: ['priority', 'title', 'description'],
                properties: {
                  code: { type: 'string' },
                  priority: { type: 'number', description: '优先级，1最高，数字越大优先级越低' },
                  title: { type: 'string' },
                  description: { type: 'string', description: '只写执行步骤，禁止重述原因或指标' },
                },
              },
              description: '按优先级从高到低输出1-3条具体优化建议',
            },
            actionKeywords: { type: 'array', items: { type: 'string' }, description: '优化项涉及的关键词列表' },
            actionCandidates: {
              type: 'array',
              description: '仅由竞品 V2 明确证据支持、且可交给一键优化的行动点',
              items: {
                type: 'object',
                required: ['action', 'evidence'],
                properties: {
                  action: { type: 'string', description: '一键优化已支持的行动名称' },
                  evidence: { type: 'string', description: '不含竞品标识的简短事实依据' },
                },
              },
            },
          },
        },
      },
      target.offerId
    )
        // 直接校验 agent 原始返回（object 或含 JSON 的 string）；不要经过 parseAgentResult（其字符串分支按旧 schema 提取会丢失新结构）
        let structured = extractStructuredDiagnosis(reportRaw)
        let diagnosisSource = 'agent'
        if (!structured) {
          log(`[DIAG_FAIL] offerId=${target.offerId} structured=null attempt=1 reportRawType=${typeof reportRaw} reportRawLen=${reportRaw ? String(reportRaw).length : 0} reportRawHead=${String(reportRaw || '').substring(0, 200)}`)
          // 自动重试一次（LLM 偶发空对象/空字符串，重试通常可恢复）
          reportRaw = await runDiagnosisAgent(
            `你是 1688 商品运营专家。请为当前商品重新生成结构化基础诊断（上一次返回为空，请务必输出完整 JSON）。\n\n` +
            `## 商品数据（CLI 真实返回）\n\`\`\`${normalizedOfferData.promptFormat}\n${normalizedOfferData.promptText.substring(0, 8000)}\n\`\`\`\n\n` +
            `## 可选证据指标（evidence 只能从中选 code）\n\`\`\`json\n${JSON.stringify(evidencePool.map(entry => ({ code: entry.code, label: entry.label, value: entry.value, unit: entry.unit })))}\n\`\`\`\n\n` +
            `## 同款行动证据（仅用于 recommendations 和 actionCandidates）\n\`\`\`json\n${JSON.stringify(v2ActionEvidence || {}).substring(0, 3500)}\n\`\`\`\n\n` +
            `## 商品库行动点\n\`\`\`json\n${JSON.stringify(diagnosisActionData || {}).substring(0, 1200)}\n\`\`\`\n\n` +
            `## 选择依据\n${JSON.stringify(target.selectionEvidence || {})}\n${target.identityWarning || '候选商品与当前详情身份一致。'}\n\n` +
            `## 输出要求\n` +
            `重试必须严格返回原始 JSON（不要 Markdown 代码围栏）。positioning 必须为 {"code":"TRAFFIC|STABLE|POTENTIAL","tags":[]}；reasonHighlights 必须为 [{"text":"...","evidenceCodes":[]}]；recommendations.priority 必须为数字且 1 最高；字符串内的双引号必须转义。禁止输出空对象、工具调用或分析过程，必须返回包含 reason/recommendations 的完整 JSON。`,
            {
              label: `product-diagnosis-report-${i}-retry`,
              schema: { type: 'object', required: ['reason', 'reasonHighlights', 'positioning', 'evidence', 'recommendations'] },
            },
            target.offerId
          )
          structured = extractStructuredDiagnosis(reportRaw)
          if (!structured) {
            log(`[DIAG_FAIL] offerId=${target.offerId} structured=null attempt=2 reportRawType=${typeof reportRaw} reportRawLen=${reportRaw ? String(reportRaw).length : 0} reportRawHead=${String(reportRaw || '').substring(0, 200)}`)
          }
        }
        if (!structured) {
          const fallback = buildDeterministicDiagnosisFallback(
            deriveOfferStats(normalizedOfferData),
            evidencePool,
            target.selectionEvidence
          )
          if (fallback) {
            structured = fallback
            diagnosisSource = 'deterministic_fallback'
            log(`[DIAG_FALLBACK] offerId=${target.offerId} evidenceCount=${evidencePool.length} reason=${structured.reason}`)
          }
        }
        const reportReadyAt = Date.now()
        const diagnosisTiming = buildProductDiagnosisTiming(
          timing,
          taskStartedAt,
          inputsReadyAt,
          reportReadyAt
        )
        log(`product diagnosis timing offerId=${target.offerId} offerDataMs=${diagnosisTiming.offerDataMs} enhancementMs=${diagnosisTiming.enhancementMs} enhancementReadyMs=${diagnosisTiming.enhancementReadyMs} inputsReadyMs=${diagnosisTiming.inputsReadyMs} agentMs=${diagnosisTiming.agentMs} totalMs=${diagnosisTiming.totalMs}`)
        if (!structured) {
          stepReport.push({ step: `商品${target.offerId}诊断报告`, status: 'failed', detail: 'AGENT_FAILED' })
          return {
            success: false,
            offerId: target.offerId,
            ordinal: i,
            title: target.title || '',
            imageUrl: target.imageUrl || '',
            errorPreset: SECTION_ERROR_PRESET.AGENT_FAILED,
            reason: '诊断生成失败',
          }
        }

        // 旧版从 const legacyReport = splitLegacyRecommendations 开始组装 Markdown；
        // 组件版改为结构化诊断，但仍在 allReports.push 前生成完整 Markdown 降级内容。
        const sameSecondCategory = sameOfferData?.v2Comparison?.sameSecondCategory === true
        const sameOfferSection = formatSameOfferAnalysis(sameOfferData, null)
        const positioning = buildPositioning(structured.positioning)
        const evidence = resolveEvidenceRefs(structured.evidence, evidencePool)
        const anomalies = buildAnomaliesList(structured.anomalies)
        const topRecommendations = selectTopRecommendations(structured.recommendations)
        const { htmlList: recommendationsHtml, codes: recommendationCodes } = buildRecommendationsHtmlList(topRecommendations)
        const recommendationTexts = topRecommendations
          .map(rec => `${String((rec && rec.title) || '').trim()}：${String((rec && rec.description) || '').trim()}`)
          .filter(text => text !== '：')
        const comprehensiveRecommendations = formatComprehensiveRecommendations(recommendationTexts, '')
        const briefStatusHtml = buildBriefStatusHtml(
          deriveOfferStats(normalizedOfferData),
          target.selectionEvidence?.source === 'abnormal'
            ? target.selectionEvidence?.reason || ''
            : ''
        )
        const sectionPayload = buildProductResultPayload({
          offerId: target.offerId,
          ordinal: i,
          title: target.title || '',
          imageUrl: target.imageUrl || '',
          briefStatusHtml,
          positioning,
          reasonHtml: structured.reason,
          reasonHighlights: structured.reasonHighlights,
          reasonHighlightEvidenceCodes: structured.evidence.map(ref => ref && ref.code),
          evidence,
          anomalies,
          recommendationsHtml,
        })

        // 降级模式仍需完整 Markdown：基础报告段 + 同款 + 综合优化建议（对齐现行结构）
        const baseReportMarkdown = renderBaseReportMarkdown({
          header: targetOffers.length > 1 ? `### 商品 ${i + 1}/${targetOffers.length}` : '### 商品诊断',
          title: target.title || '',
          offerId: target.offerId,
          positioning,
          reason: structured.reason,
          evidence,
          anomalies,
          identityWarning: target.identityWarning || '',
        })
        const visibleContent = sanitizeMerchantReport(
          [baseReportMarkdown, sameOfferSection, comprehensiveRecommendations].filter(Boolean).join('\n\n')
        )
        const reportProductTitle = target.title || ''
        if (!visibleContent) {
          return {
            success: false,
            offerId: target.offerId,
            ordinal: i,
            title: target.title || '',
            imageUrl: target.imageUrl || '',
            errorPreset: SECTION_ERROR_PRESET.AGENT_FAILED,
            reason: '报告内容为空',
          }
        }

        return {
          success: true,
          offerId: target.offerId,
          ordinal: i,
          sectionPayload,
          item: {
            status: 'success',
            offerId: target.offerId,
            loginId: target.loginId,
            shopName: target.shopName,
            title: reportProductTitle,
            report: baseReportMarkdown,
            recommendations: topRecommendations,
            recommendationCodes,
            visibleContent,
            sameOfferSection,
            sameOfferData,
            sameOfferStatus,
            offerDiagnosisStatus,
            diagnosisSource,
            sameSecondCategory,
            positioning,
            stats: deriveOfferStats(normalizedOfferData),
            anomalies,
            diagnosisActionCandidates: deriveDiagnosisActionCandidates(structured.reason + ' ' + topRecommendations.map(rec => `${rec.title} ${rec.description}`).join(' '), structured.actionKeywords),
            v2ActionCandidates: sameSecondCategory ? structured.actionCandidates : [],
            productLibraryActions: Array.isArray(diagnosisActionData?.actions) ? diagnosisActionData.actions : [],
          },
        }
      },
    })
  }

  // ─── 阶段 B/C：并行执行每件商品的完整体检，结果按原商品顺序回收 ───
  let completedReportCount = 0
  if (reportJobs.length > 0) {
    phase('对比优秀同款')
    reportOutcomes = await executeReportJobs(
      reportJobs,
      parallel,
      async (completed, total, outcome, job) => {
        completedReportCount = completed
        if (sectionStreamEnabled) {
          const payload = outcome && outcome.success && outcome.sectionPayload
            ? outcome.sectionPayload
            : buildProductFailurePayload({
                offerId: (outcome && outcome.offerId) || job.offerId,
                ordinal: (outcome && outcome.ordinal != null ? outcome.ordinal : job.ordinal),
                title: (outcome && outcome.title) || job.title || '',
                imageUrl: (outcome && outcome.imageUrl) || job.imageUrl || '',
                errorPreset: (outcome && outcome.errorPreset)
                  || (outcome && outcome.timedOut ? SECTION_ERROR_PRESET.TIMEOUT : SECTION_ERROR_PRESET.DATA_UNAVAILABLE),
              })
          await emitSection(sectionReportId, sectionSeqState, 'product_result', payload)
          sectionResults.push({ offerId: payload.offerId, ordinal: payload.ordinal, status: payload.status })
          return
        }
        const resultText = outcome?.success ? '已完成' : '暂未完成'
        progressEmit(`<aside>${resultText} ${completedReportCount}/${total} 件商品诊断：商品 ${job.offerId}。</aside>`)
      },
      MAX_DIAGNOSIS_CONCURRENCY
    )
  }

  phase('整理诊断报告')
  const successIds = [], failIds = []
  for (const outcome of reportOutcomes.sort((left, right) => (left?.ordinal ?? 0) - (right?.ordinal ?? 0))) {
    if (!outcome?.success || !outcome.item) {
      failIds.push(outcome?.offerId || '?')
      stepReport.push({
        step: `商品${outcome?.offerId || '未知'}诊断报告`,
        status: 'failed',
        detail: outcome?.reason || '报告生成失败',
      })
      continue
    }
    successIds.push(outcome.offerId)
    allReports.push(outcome.item)
    stepReport.push({ step: `商品${outcome.offerId}诊断报告`, status: 'done', detail: '已生成' })
  }
  log(`[DIAG_SUMMARY] success=${successIds.length} fail=${failIds.length} successIds=${JSON.stringify(successIds)} failIds=${JSON.stringify(failIds)}`)
  reportCompletedPayload = buildReportCompletionSnapshot(targetOffers, allReports)

  if (allReports.length === 0) {
    if (sectionStreamEnabled) {
      emitSection(sectionReportId, sectionSeqState, 'overview_result', buildOverviewPayload([]))
      emitSection(sectionReportId, sectionSeqState, 'footer_actions', buildFooterActionsPayload({
        oneClickCandidates: [],
        includeSchedule: false,
      }))
    }
    await finalizeSectionDelivery()
    const failureSummary = summarizeReportFailures(reportOutcomes)
    emit(failureSummary.visibleMessage)
    return `商品诊断工作流终止：${failureSummary.reason}。

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify({ completedSteps: stepReport, executionMode, delivery: executionMode === 'automatic' ? 'markdown' : deliveryMode, reportId: sectionReportId, queryStatus: 'failed', reason: failureSummary.reason, selectedCount: targetOffers.length, completed: reportCompletedPayload.completed, failed: reportCompletedPayload.failed, products: reportCompletedPayload.products, componentLaunchState, sectionStreamState, scheduleDeduplicationStatus: executionMode === 'automatic' ? 'skipped' : (scheduleCheck.data?.status || 'query_failed') }, null, 2)}
</execution_manifest>`
  }

  if (sectionStreamEnabled) {
    emitSection(sectionReportId, sectionSeqState, 'overview_result', buildOverviewPayload(allReports))
  }

  const incompleteReportSection = executionMode === 'automatic'
    ? buildAutomaticIncompleteReportSection(targetOffers, allReports, reportOutcomes)
    : ''
  merchantReportValue = [
    sanitizeMerchantReport(allReports.map(item => item.visibleContent).filter(Boolean).join('\n\n---\n\n')),
    incompleteReportSection,
  ].filter(Boolean).join('\n\n---\n\n')

  progressEmit('<aside>商品经营表现检查完成，已覆盖近期流量、成交、加购和转化。</aside>')
  progressEmit('<aside>同款对比和商品库建议核对完成。</aside>')
  progressEmit(`<aside>已生成 ${allReports.length} 件商品的完整诊断报告。</aside>`)

  // ─── 阶段 D：准备报告后的一键优化交接 ───
  phase('准备后续操作')
  ;({ candidates, unsupported } = mergeActionCandidates(allReports))
  if (unsupported.length > 0) {
    progressEmit('部分建议暂不支持一键优化，未加入本次一键优化任务。')
  }

  if (executionMode === 'automatic') includeScheduleOption = false
  if (executionMode !== 'automatic') {
    scheduleCheck = await runCli('check_auto_diagnosis_schedule', [])
    includeScheduleOption = scheduleCheck.success
      && scheduleCheck.data?.showScheduleOption === true
  }
  const includeScheduleForCache = executionMode === 'automatic' ? false : includeScheduleOption
  reportCache = await writeReportCache(
    sectionReportId,
    [merchantReportValue, buildPostReportFollowupText(candidates, { includeSchedule: includeScheduleForCache, forExport: true })]
      .filter(Boolean)
      .join('\n\n---\n\n')
  )
  if (sectionStreamEnabled) {
    emitSection(sectionReportId, sectionSeqState, 'footer_actions', buildFooterActionsPayload({
      oneClickCandidates: candidates,
      includeSchedule: includeScheduleForCache,
      reportCache,
    }))
  }
} catch (error) {
  log(`diagnosis stream failed: ${String((error && error.message) || error)}`)
  deliveryMode = 'markdown'
  merchantReportValue = [
    sanitizeMerchantReport(allReports.map(item => item.visibleContent).filter(Boolean).join('\n\n---\n\n'))
      || '### 商品诊断\n\n诊断过程暂时中断，请稍后重试。',
    executionMode === 'automatic'
      ? buildAutomaticIncompleteReportSection(targetOffers, allReports, reportOutcomes)
      : '',
  ].filter(Boolean).join('\n\n---\n\n')
  stepReport.push({
    step: '整理诊断报告',
    status: 'failed',
    detail: '诊断过程异常中断',
  })
} finally {
  await finalizeSectionDelivery()
  reportCompletedPayload = buildReportCompletionSnapshot(targetOffers, allReports)
}
const merchantReport = merchantReportValue
const oneClickHandoff = buildOneClickHandoff(candidates)
const postReportFollowupText = buildPostReportFollowupText(
  candidates,
  { includeSchedule: executionMode === 'automatic' ? false : includeScheduleOption }
)
const merchantReportWithFollowup = [merchantReport, postReportFollowupText]
  .filter(Boolean)
  .join('\n\n---\n\n')
// 导出/缓存版：后续操作只保留行动点清单，去掉"回复进入一键优化/设置定时任务"等对话交互引导
const exportReportFollowupText = buildPostReportFollowupText(
  candidates,
  { includeSchedule: executionMode === 'automatic' ? false : includeScheduleOption, forExport: true }
)
const exportReportMarkdown = [merchantReport, exportReportFollowupText]
  .filter(Boolean)
  .join('\n\n---\n\n')
const sameOfferMarkdown = allReports
  .map((item, index) => {
    if (!item.sameOfferSection) return ''
    const sectionBody = item.sameOfferSection.replace(/^#### 同款商品分析\s*\n+/, '')
    return `#### 商品 ${index + 1}：${item.title || item.offerId}\n\n${sectionBody}`
  })
  .filter(Boolean)
  .join('\n\n')
const sameOfferMarkdownForComponent = sameOfferMarkdown
  ? `### 同款商品分析\n\n${sameOfferMarkdown}`
  : ''
stepReport.push({
  step: '准备后续操作',
  status: 'done',
  detail: executionMode === 'automatic'
    ? `${candidates.length} 条行动已整理为 Markdown 报告和一键优化交接`
    : `${candidates.length} 条行动已按商品汇总到 footer_actions`,
})
if (deliveryMode === 'component') {
  return `# 唯一输出要求：组件已是主交付，当前回复只输出同款分析

本次商品体检的结构化诊断结果已通过诊断组件（reportId=${sectionReportId}）流式交付，基础诊断、证据、建议和底部操作均已在组件内展示，**禁止在回复中重复输出任何基础诊断内容**。

1. 下一条 assistant 内容只把 \`<same_offer_markdown>\` 内的同款分析原样输出到主对话；无同款内容时输出一句"诊断报告已生成，请在左侧查看详情"。一键优化和定时任务只由组件 footer_actions 展示，禁止在主对话重复输出。禁止总结、改写、删减。
2. 当前回复禁止调用任何工具，包括 notice、card、show_interaction、其他 workflow 或 skill。输出后立即结束当前回复，禁止追加总结、追问或重复报告。
3. 用户下一条消息明确表达一键优化意图（包括组件按钮按商品和优化项回填的普通文本，或手动回复"进入一键优化"）时，使用本返回内的 \`<one_click_handoff_json>\` 调用一次 \`1688-item-one-click\` workflow。必须复制该标签内的原始 JSON 对象，将其 JSON.stringify 后的完整字符串直接作为 Workflow args；禁止依赖 reportId 或会话外存储，禁止包装成 query/params、空参数调用、增删任务或重复调用。无法取得完整 handoff JSON 时请用户重新发起商品诊断。
4. 用户下一条消息命中组件“导出报告”按钮回填（要求导出一个 Markdown 文件）时，不得再次调用当前 workflow、商品查询、组件、模型或其他工具。回填消息指明报告全文缓存在当前工作目录：缓存文件名为 \`.report-cache-<报告编号>.md\`（报告编号含诊断时间戳，形如 \`pd_20260731151541_lqz3\`；存在多份时取时间戳最新的一份），用 \`.report-cache-*.md\` 模式在当前工作目录直接定位即可，禁止全盘搜索；回填消息说明缓存在 skill 根目录时，才到 cli.py 所在目录（形如 \`.../skills/newton_seller/1688-product-analysis\`）下定位。定位后只允许两个工具调用——先 Read 缓存文件取得报告全文，再调用一次 Write 把读到的内容原样写入相对路径 \`商品体检报告.md\`，禁止改动、总结、删减或补充任何内容。回填消息没有提及缓存时，才回退为只调用一次 Write、完整复制本返回内 \`<export_report_markdown>\` 的 Markdown（组件降级时回退 \`<merchant_report>\`）。Newton 会根据 Write 成功结果自动渲染文件卡，严禁调用 present_files。导出必须幂等：只要上下文已出现该文件的 Write 成功结果，就视为导出完成，绝对禁止再次调用任何工具，只回复“已导出商品体检报告.md。”并立即结束。缓存文件与标签都缺失或读取失败时，不得创建空文件、不得全盘搜索文件系统或读取任何 JSON 文件、旧报告、工作区文件来重建、编造报告，只回复“报告缓存已失效，请重新发起商品体检后再导出。”。严禁调用 Bash、Edit、schedule_task、show_interaction 或处理其他 footer action，不得在对话中重复报告正文，不得生成 JSON、中间文件或第二个附件。
5. 用户下一条消息明确表达设置商品自动体检定时任务的意图（含组件按钮完整 prompt 回填）时，进入 Newton 原生定时任务设置流程（规则同现行 Step 4 第 4 条）。

<same_offer_markdown>
${sameOfferMarkdownForComponent}
</same_offer_markdown>

<one_click_handoff_json>
${JSON.stringify(oneClickHandoff, null, 2)}
</one_click_handoff_json>

<export_report_markdown>
${exportReportMarkdown}
</export_report_markdown>

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify({
  completedSteps: stepReport,
  executionMode,
  delivery: 'component',
  reportId: sectionReportId,
  queryStatus: resolveReportQueryStatus(reportCompletedPayload, stepReport),
  selectedCount: targetOffers.length,
  completed: reportCompletedPayload.completed,
  failed: reportCompletedPayload.failed,
  products: reportCompletedPayload.products,
  productAnalysisActionConfirmation: candidates.length > 0,
  actionCandidateCount: candidates.length,
  oneClickHandoffPending: candidates.length > 0,
  scheduleDeduplicationStatus: executionMode === 'automatic' ? 'skipped' : (scheduleCheck.data?.status || 'query_failed'),
  followupInteractionPending: false,
  reportDeliveryRequired: true,
  reportDeliveryState: 'component_streamed',
  componentLaunchState,
  sectionStreamState,
  enhancementStates: allReports.map(item => ({
    offerId: item.offerId,
    sameOffer: item.sameOfferStatus,
    offerDiagnosis: item.offerDiagnosisStatus,
    recommendationCodes: item.recommendationCodes,
  })),
}, null, 2)}
</execution_manifest>`
}

return `# 强制交付：以下报告尚未向用户展示

完整报告是本次商品体检不可跳过的主输出，不是总结，也不是可选步骤。只有 workflow 完成、却没有在主对话完整输出报告，仍然属于任务失败。

报告最后一个字符输出到主对话之前，严禁加载、调用、预执行或重复执行一键优化、其他 skill、workflow、show_interaction 或定时任务。不得把完成一键优化 workflow 当作完成商品体检。少执行后续工具可以接受，少输出或不输出报告绝对不允许。

<merchant_report>
${merchantReportWithFollowup}
</merchant_report>

（以下为内部交付约束，请勿展示给用户）

<response_contract>
完整报告是本次商品体检不可跳过的主输出，不是总结，也不是可选步骤。只有 workflow 完成、却没有在主对话完整输出报告，仍然属于任务失败。

报告最后一个字符输出到主对话之前，严禁加载、调用、预执行或重复执行一键优化、其他 skill、workflow、show_interaction 或定时任务。不得把完成一键优化 workflow 当作完成商品体检。少执行后续工具可以接受，少输出或不输出报告绝对不允许。

1. 下一条 assistant 内容的第一个 block 必须是普通文本 block，并把上方 \`<merchant_report>\` 内的完整 Markdown 原样输出到主对话。禁止总结、改写、删减、折叠或只提炼核心发现；不要输出标签和本段内部指令。不得给任何文字额外添加 Markdown 强调，尤其禁止把“进入一键优化”或“设置定时任务”改成带 \`**\`、\`__\`、反引号或其他包裹的形式。
2. 当前回复禁止调用任何工具，包括 notice、card、show_interaction、其他 workflow 或 skill。输出报告后立即结束当前回复，禁止追加总结、追问或重复报告。
3. 报告末尾已经列出可执行商品和行动点。只有用户下一条消息明确表达一键优化意图（包括按钮按商品和优化项回填的普通文本，或手动回复“进入一键优化”）时，才使用 \`<one_click_handoff_json>\` 调用一次 \`1688-item-one-click\` workflow。必须复制该标签内的原始 JSON 对象，将其 JSON.stringify 后的完整字符串直接作为 Workflow args；禁止把用户原话作为 query 试探调用，禁止包装成 query/params，禁止空参数调用、增删任务、重新组合或重复调用。若当前上下文无法取得完整 handoff JSON，应请用户重新发起商品诊断，不得猜测任务。逐项“执行/跳过”由一键优化自己确认。
4. 只有用户下一条消息明确表达设置商品自动体检定时任务的意图（包括手动回复“设置定时任务”或组件按钮完整 prompt 回填）时，才进入 Newton 原生定时任务设置流程：先收集执行频率和时间，再调用 \`show_interaction(type="schedule_task")\`；仅当返回 \`action="execute"\` 后调用 \`Schedule(action="create")\`。主 Agent 禁止再次调用 \`Schedule(action="list")\`。只有 enabled=true 才算已配置，enabled=false 不算已配置。任务名称建议为“1688商品自动体检”，任务 prompt 默认且完整使用“${AUTO_DIAGNOSIS_TASK_QUERY}”；不得自动修改商品。
</response_contract>

<one_click_handoff_json>
${JSON.stringify(oneClickHandoff, null, 2)}
</one_click_handoff_json>

（以下为内部调度信息，请勿展示给用户）

<execution_manifest>
${JSON.stringify({
  completedSteps: stepReport,
  executionMode,
  delivery: 'markdown',
  reportId: sectionReportId,
  queryStatus: resolveReportQueryStatus(reportCompletedPayload, stepReport),
  selectedCount: targetOffers.length,
  completed: reportCompletedPayload.completed,
  failed: reportCompletedPayload.failed,
  products: reportCompletedPayload.products,
  productAnalysisActionConfirmation: candidates.length > 0,
  actionCandidateCount: candidates.length,
  oneClickHandoffPending: candidates.length > 0,
  scheduleDeduplicationStatus: executionMode === 'automatic' ? 'skipped' : (scheduleCheck.data?.status || 'query_failed'),
  followupInteractionPending: false,
  reportDeliveryRequired: true,
  reportDeliveryState: 'pending_assistant_text',
  componentLaunchState,
  sectionStreamState,
  enhancementStates: allReports.map(item => ({
    offerId: item.offerId,
    sameOffer: item.sameOfferStatus,
    offerDiagnosis: item.offerDiagnosisStatus,
  })),
}, null, 2)}
</execution_manifest>`
