// ─── Meta ────────────────────────────────────────────────
export const meta = {
  name: '1688-shop-daily-report',
  description: '1688 店铺经营日报 — 路由入口。识别单店/多店意图后分发到对应子图，生成含核心摘要/广告/评价/异常/行动重点的日报并弹出行动选择卡片。不做长期战略与冗余分析。',
  whenToUse: '当用户要求生成日报、经营报告、店铺分析、店铺日报、生成日报、经营数据、查看昨天经营情况时使用',
  phases: [
    { title: '意图识别', detail: '解析用户输入，判定单店/多店模式并确定日期' },
    { title: '日期解析', detail: '解析查询日期与前一天日期，拦截今日/未来日期' },
    { title: '模式分发', detail: '按模式 subgraph 到 single-shop 或 multi-shop 子图' },
  ],
}

// ─── Utilities（纯同步数据函数，子图自动继承） ────────────

// @utility:shellEscape
function shellEscape(arg) {
  const s = String(arg)
  if (/^[a-zA-Z0-9._\-\/:,=@]+$/.test(s)) return s
  if (typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)) {
    return '"' + s.replace(/"/g, '""') + '"'
  }
  return "'" + s.replace(/'/g, "'\\''") + "'"
}

// @utility:utf8Bytes
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

const BASE64_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

// base64 输出集只有 A-Za-z0-9+/=，不含 % ! " ' & | < > ^ ( ) 与换行，
// 因此编码后的内容进命令行不会被 cmd 变量展开或转义吃掉。
// @utility:toBase64
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

// @utility:buildBashCommand
function buildBashCommand(program, args, description, timeout = 120000) {
  const isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  const tmpDir = isWin ? (process.env.TEMP || process.env.TMP || 'C:\\temp') : '/tmp'
  const sep = isWin ? '\\' : '/'
  const id = `_wf${Date.now()}${Math.random().toString(36).slice(2, 5)}`
  const outF = `${tmpDir}${sep}${id}_o`
  const errF = `${tmpDir}${sep}${id}_e`
  let redirectedCmd
  // .cmd 批处理文件的内容不会被 newton 的 win-command-normalizer 二次处理（它只改写外层
  // 命令行），因此 Windows 侧在这里自己完成 python3→python 映射，与 normalizer 规则保持一致。
  const prog = isWin && program === 'python3' ? 'python' : program
  // args[0] === '-c' 时按 Python 内联脚本处理：posix 走 heredoc，正文不必转义；
  // cmd 没有 heredoc，且 cmd.exe /c 的解析在第一个换行符处终止（多行内联脚本只会
  // 静默执行第一行：「核对日报数据日期」在 Windows 上曾因此返回空、被误判成数据未回收），
  // 故把脚本 base64 后由 python 解码 exec 还原成单行命令。
  // 两种形式下额外参数都从 sys.argv[1] 开始，内联脚本按 sys.argv[1:] 取参即可。
  if (args[0] === '-c' && program !== 'sh') {
    const script = args[1]
    const extraArgs = args.slice(2).map(a => shellEscape(String(a))).join(' ')
    const argsPart = extraArgs ? ` ${extraArgs}` : ''
    if (isWin) {
      redirectedCmd = `${prog} -c "import base64;exec(base64.b64decode('${toBase64(utf8Bytes(script))}').decode())"${argsPart} > "${outF}" 2> "${errF}"`
    } else {
      redirectedCmd = `{ ${prog} -${argsPart} << '_WF_PYEOF_'\n${script}\n_WF_PYEOF_\n} > "${outF}" 2> "${errF}"`
    }
  } else if (program === 'sh' && args[0] === '-c') {
    const shellCmd = args[1]
    if (isWin) {
      redirectedCmd = `(${shellCmd}) > "${outF}" 2> "${errF}"`
    } else {
      redirectedCmd = `sh -c ${shellEscape(shellCmd)} > "${outF}" 2> "${errF}"`
    }
  } else {
    const shellCmd = [prog, ...args.map(a => shellEscape(String(a)))].join(' ')
    redirectedCmd = `${shellCmd} > "${outF}" 2> "${errF}"`
  }
  let command
  if (isWin) {
    // cmd.exe /c 对整条单行命令只做一次解析：同行的 setlocal enabledelayedexpansion 来不及生效，
    // !errorlevel! 会原样输出字面量（线上 win32 日志已观测到）；而 %errorlevel% 在单行里又是
    // 解析期展开的陈旧值。可靠做法：把「执行 → 回显退出码 → 回显 stdout/stderr → 清理」写成
    // 多行 .cmd 批处理执行——批处理逐行解析执行，%errorlevel% 在自己的行上展开，拿到的就是
    // 上一条命令的真实退出码。脚本内容含引号/重定向/括号，用 echo 落盘要层层转义，
    // 故内容 base64 后由 python 写文件（python 缺失时 writer 报错进 stderr，信封首行非数字，
    // 上层仍按失败处理，不会误判成功）。
    const wrapF = `${tmpDir}${sep}${id}_w.cmd`
    const wrapper = [
      '@echo off',
      redirectedCmd,
      'echo %errorlevel%',
      `type "${outF}"`,
      'echo.',
      'echo __WFSE__:',
      `type "${errF}"`,
      `del /f /q "${outF}" "${errF}"`,
    ].join('\r\n') + '\r\n'
    command = `python -c "import base64;open(r'${wrapF}','wb').write(base64.b64decode('${toBase64(utf8Bytes(wrapper))}'))" & call "${wrapF}" & del /f /q "${wrapF}"`
  } else {
    command = `${redirectedCmd}; _ec=$?; echo $_ec; cat "${outF}"; printf '\\n__WFSE__:'; cat "${errF}"; rm -f "${outF}" "${errF}"`
  }
  // description 会作为命令步骤展示给商家，兜底值不得用 `exec: python3` 这类英文技术字样
  // （SKILL「输出格式·用语规范」：一律使用中文、禁露命令名与内部术语）
  return { command, timeout, description: description || '正在处理数据' }
}

// @utility:parseBashOutput
function parseBashOutput(raw) {
  let text = typeof raw === 'string' ? raw
    : (raw !== null && typeof raw === 'object' ? (raw.raw || JSON.stringify(raw)) : String(raw || ''))
  if (text.startsWith('Command:')) {
    const hEnd = text.indexOf('\n\n')
    if (hEnd >= 0) text = text.slice(hEnd + 2)
  }
  const nlIdx = text.indexOf('\n')
  const head = (nlIdx >= 0 ? text.slice(0, nlIdx) : text).trim()
  // 首行不是退出码说明包装命令没按预期执行（如框架竞态空返回、或只回显了命令头），
  // 此时整体按失败处理，绝不能 parseInt 兜底 0 把垃圾文本当业务输出用。
  if (!/^-?\d+$/.test(head)) {
    return { exitCode: 1, stdout: '', stderr: text.trim() || 'CLI 子进程返回格式不可识别' }
  }
  const rest = nlIdx >= 0 ? text.slice(nlIdx + 1) : ''
  const exitCode = Number(head)
  const seMarker = '\n__WFSE__:'
  const seIdx = rest.lastIndexOf(seMarker)
  const stdout = seIdx >= 0 ? rest.slice(0, seIdx) : rest
  const stderr = seIdx >= 0 ? rest.slice(seIdx + seMarker.length) : ''
  return { exitCode, stdout, stderr }
}

// @utility:parseCliOutput
function parseCliOutput(bashResult, command) {
  const { exitCode, stdout, stderr } = bashResult
  try { return JSON.parse(stdout) } catch {}
  if (exitCode !== 0) {
    const errMsg = stderr.slice(0, 300).trim()
    return { success: false, error: errMsg, command, data: {} }
  }
  return { success: true, markdown: stdout, data: {} }
}

// @utility:extract
function extract(source, mapping) {
  const result = {}
  for (const [key, config] of Object.entries(mapping)) {
    const raw = config.path.includes('.')
      ? config.path.split('.').reduce((o, k) => o?.[k], source)
      : source?.[config.path]
    if (config.type === 'number') {
      result[key] = typeof raw === 'number' ? raw : (config.default ?? 0)
    } else if (config.type === 'array') {
      result[key] = Array.isArray(raw) ? raw : (config.default ?? [])
    } else if (config.type === 'boolean') {
      result[key] = typeof raw === 'boolean' ? raw : (config.default ?? false)
    } else {
      result[key] = raw ?? config.default ?? ''
    }
  }
  return result
}

// @utility:buildArgs
function buildArgs(specs) {
  const result = []
  for (const spec of specs) {
    if (spec.when === undefined || spec.when) result.push(...spec.args)
  }
  return result
}

// @utility:absNum — 沙箱可能禁用 Math，自行实现绝对值
function absNum(n) { return n < 0 ? -n : n }

// @utility:roundTo — 四舍五入到指定小数位（不依赖 Math.round）
function roundTo(n, digits) {
  return parseFloat(Number(n).toFixed(digits === undefined ? 0 : digits))
}

// @utility:num — 安全取数，支持多个候选字段名（真实字段可能为中文）
function num(row, ...keys) {
  for (const k of keys) {
    const v = row?.[k]
    if (v !== undefined && v !== null && v !== '') {
      const n = typeof v === 'string' ? parseFloat(v) : v
      if (typeof n === 'number' && !isNaN(n)) return n
    }
  }
  return 0
}

// @utility:pct — 涨跌幅百分比（保留1位小数），基准为0/空时返回 null（不可比）
function pct(today, base) {
  if (base === 0 || base === null || base === undefined) return null
  return roundTo(((today - base) / base) * 100, 1)
}

// @utility:fmtPct — 百分比格式化为带符号字符串；null → '-'
function fmtPct(p) {
  if (p === null || p === undefined) return '-'
  return (p > 0 ? '+' : '') + p + '%'
}

// @utility:fmtNum — 千分位格式化
function fmtNum(n, digits) {
  const d = digits === undefined ? 0 : digits
  const fixed = Number(n).toFixed(d)
  const parts = fixed.split('.')
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return parts.join('.')
}

// @utility:normalizeMetrics — 将扁平的交易/流量/用户字段归一化为标准指标对象
// 周环比为接口预计算的**平铺字段**（gmvWeekOnWeek 等），必须一并带出来：
// 本函数是白名单式投影，之前没带这三个字段，导致下游 computeMetricSet 永远拿不到周环比、整列全是“-”。
function normalizeMetrics(day) {
  const d = day || {}
  const gmv = num(d, 'gmv', '当日GMV（元）')
  const orderCount = num(d, 'orderCount', '当日支付子订单数')
  const inquiryCount = num(d, 'inquiryCount', '当日询盘数')
  const payConversionRate = num(d, 'payConversionRate', '支付转化率（%）')
  const avgPrice = num(d, 'avgPrice', '客单价') || (orderCount > 0 ? gmv / orderCount : 0)
  const uv = num(d, 'uv', 'UV')
  const pv = num(d, 'pv', 'PV')
  const uvCtr = num(d, 'uvCtr', 'UVCTR')
  const bounceRate = num(d, 'bounceRate', '跳出率（%）')
  const newBuyerCount = num(d, 'newBuyerCount', '全店支付新买家数')
  const oldBuyerCount = num(d, 'oldBuyerCount', '全店支付老买家数')
  // 周环比原值透传（可能不存在，保留 undefined 以便下游区分“无字段”与“值为 0”）
  const _w = (k) => (typeof d[k] === 'number') ? d[k] : undefined
  return {
    gmv, orderCount, inquiryCount, payConversionRate, avgPrice, uv, pv, uvCtr, bounceRate, newBuyerCount, oldBuyerCount,
    gmvWeekOnWeek: _w('gmvWeekOnWeek'), orderWeekOnWeek: _w('orderWeekOnWeek'), inquiryWeekOnWeek: _w('inquiryWeekOnWeek'),
    uvWeekOnWeek: _w('uvWeekOnWeek'), pvWeekOnWeek: _w('pvWeekOnWeek'), searchUvWeekOnWeek: _w('searchUvWeekOnWeek'),
    avgPriceWeekOnWeek: _w('avgPriceWeekOnWeek'),
  }
}

// @utility:parseAgentResult — agent 结果容错解析（返回对象或 null）
// 实测事故：推理模型返回 `<think>…思考…</think>{"insights":[…]}`，agent(schema) 未剥离思考块，
// 于是 `deep?.insights` 全取空 → 深度分析静默降级成“暂无建议”，而模型其实已产出 5 条洞察与 5 条行动。
// 同一坑会让 intent（模式/日期）与 profile（经营模式）一并退回默认值，**失败无任何报错**，所以每个
// agent 返回值都必须过这层；不得直接 `(await agent(...))?.field`。
function parseAgentResult(raw) {
  if (raw && typeof raw === 'object' && !Array.isArray(raw)) return raw
  if (typeof raw !== 'string') return null
  let s = raw
  // 取最后一个 </think> 之后的内容（思考内容里可能也带 JSON 草稿，不能取第一个）
  const _tEnd = s.lastIndexOf('</think>')
  if (_tEnd >= 0) s = s.slice(_tEnd + 8)
  s = s.replace(/```(?:json)?/gi, '').trim()
  const _a = s.indexOf('{')
  const _b = s.lastIndexOf('}')
  if (_a < 0 || _b <= _a) return null
  try { return JSON.parse(s.slice(_a, _b + 1)) } catch { return null }
}

// @utility:extractAnswer — 从 showInteraction 返回结果中提取用户选择（多级兜底）
function extractAnswer(result) {
  if (!result) return ''
  const raw = result.data
  const list = Array.isArray(raw) ? raw : (raw?.answers || result.answers)
  const first = Array.isArray(list) ? list[0] : null
  const val = (typeof first === 'string' ? first : first?.answer)
    || result.selection || result.choice || ''
  return typeof val === 'string' ? val.trim() : (val ?? '')
}

// @utility:itemLine — 机会/风险条目渲染（兼容 LLM 返回对象 {shop,metric,reason} 或 "店铺/指标/原因" 斜杠字符串）
function itemLine(it) {
  if (it === null || it === undefined) return ''
  if (typeof it === 'string') {
    const parts = it.split('/').map(s => s.trim()).filter(Boolean)
    if (parts.length >= 3) return `**${parts[0]} ${parts[1]}** — ${parts.slice(2).join(' / ')}`
    if (parts.length === 2) return `**${parts[0]}** — ${parts[1]}`
    return parts.join(' — ')
  }
  const head = [it.shop, it.metric].filter(Boolean).join(' ')
  const body = it.reason || it.change || it.desc || ''
  return head ? `**${head}** — ${body}` : String(body || '')
}

// @utility:actionLine — 行动条目渲染（兼容对象 {action,reason,shop} 或整句字符串）
function actionLine(a) {
  if (a === null || a === undefined) return ''
  if (typeof a === 'string') return a.trim()
  const t = a.action || a.title || ''
  const r = a.reason || ''
  const s = a.shop ? `（${a.shop}）` : ''
  return t ? `**${t}**${r ? ` - ${r}` : ''}${s}` : `${r}${s}`
}

// @utility:actionText — 行动条目关键词匹配用纯文本（兼容对象或字符串）
function actionText(a) {
  if (a === null || a === undefined) return ''
  if (typeof a === 'string') return a.trim()
  return `${a.action || ''} ${a.reason || ''}`.trim()
}

// @utility:matchProfileTrigger — profile 字段是否命中触发条件（包含匹配）；无 trigger 视为命中
function matchProfileTrigger(profile, trigger) {
  if (!trigger || !trigger.field) return true
  const kws = Array.isArray(trigger.contains) ? trigger.contains : []
  if (kws.length === 0) return true
  const val = String((profile && profile[trigger.field]) || '')
  return kws.some(k => val.includes(k))
}

// @utility:selectProfileQueries — 按经营模式 + Profile 字段从目录挑出触发命中的补充查询
// AD 源数据已由 get_ad_report / get_multi_shop_report 覆盖，统一剔除避免重复查询
function selectProfileQueries(profile, catalog) {
  const key = (profile && profile.bizMode) || 'integrated'
  const list = (catalog && (catalog[key] || catalog.integrated)) || []
  return list
    .filter(q => q.data_source !== 'AD')
    .filter(q => matchProfileTrigger(profile, q.trigger))
    .map(q => ({ label: q.label, data_source: q.data_source, api_path: q.api_path, params: q.params }))
}

// @utility:fmtVal — 按度量类型格式化数值
function fmtVal(raw, fmt) {
  if (raw === null || raw === undefined) return '-'
  if (fmt === 'money0') return '¥' + fmtNum(raw)
  if (fmt === 'money2') return '¥' + fmtNum(raw, 2)
  if (fmt === 'int') return fmtNum(raw)
  if (fmt === 'pct2') return fmtNum(raw, 2) + '%'
  if (fmt === 'pct1') return fmtNum(raw, 1) + '%'
  return String(raw)
}

// @utility:pickColumns — 按经营模式 × 阶段动态选取核心摘要列
function pickColumns(bizMode, stage) {
  const byMode = COLUMN_PREFS[bizMode] || COLUMN_PREFS.integrated
  const cols = (byMode && byMode[stage]) || COLUMN_PREFS.integrated['成长'] || ['gmv', 'order', 'uv', 'conv']
  const valid = cols.filter(k => METRIC_META[k])
  return valid.length >= 3 ? valid.slice(0, 5) : ['gmv', 'order', 'uv', 'conv']
}

// @utility:metricCell — 横向表格单元格：值(日环比)
function metricCell(metrics, key) {
  const meta = METRIC_META[key]
  const c = metrics && metrics[key]
  if (!meta || !c) return '-'
  const v = fmtVal(c.raw, meta.fmt)
  if (meta.noDod || c.dod === null || c.dod === undefined) return v
  return `${v}(${fmtPct(c.dod)})`
}

// @utility:metricRow — 纵向表格行：| 指标 | 当日 | 日环比 |（withWeek 时追加周环比列）
// 不展环比的指标（如转化率，SKILL 规定仅看当日值）用空单元格，不用 "-"：
// "-" 已用于表示“无数据”，两者混用会让商家以为数据缺失。
function metricRow(metrics, key, withWeek) {
  const meta = METRIC_META[key]
  const c = metrics && metrics[key]
  if (!meta || !c) return ''
  const v = fmtVal(c.raw, meta.fmt)
  const day = meta.noDod ? '' : fmtPct(c.dod)
  if (!withWeek) return `| ${meta.name} | ${v} | ${day} |`
  const week = meta.noDod ? '' : fmtPct(c.week === undefined ? null : c.week)
  return `| ${meta.name} | ${v} | ${day} | ${week} |`
}

// @utility:singleMetricKeys — 单店纵向表的指标顺序：Profile 关注的在前，其余补齐在后
// 横向表（多店）受屏幕宽度限制必须精简到 4-5 列；纵向表（单店）每个指标一行，
// 多几行成本很低、信息更全，因此单店列全部可用指标，仅用 Profile 选列结果控制优先顺序。
function singleMetricKeys(bizMode, stage) {
  const preferred = pickColumns(bizMode, stage)
  const all = Object.keys(METRIC_META)
  const rest = all.filter(k => preferred.indexOf(k) < 0)
  return preferred.concat(rest)
}

// @utility:computeMetricSet — 由 today/prev/weekAgo 归一化对象派生全部可渲染指标
// 周环比：服务端已用上周同日原值自算并写回平铺字段（gmvWeekOnWeek 等），直接取用。
// **自算后 0 是有效值**（真的持平），不能再当无数据；仅当 weekAgo 缺失（--no_week_on_week）
// 时拿到的才是接口预计算值，那种情况下除 GMV 外恒为 0、不可信，故整体忽略。
// 派生指标（老客占比/询盘转化率）接口不提供环比，在此用 weekAgo 原值现算。
function computeMetricSet(today, prev, preDod, weekAgo) {
  const t = today || {}, p = prev || {}, pd = preDod || {}
  const wk = weekAgo || null
  const hasWk = !!wk
  // 服务端自算的周环比（仅在拿到 weekAgo 时可信）
  const wkOf = (flatKey) => (hasWk && typeof t[flatKey] === 'number') ? roundTo(t[flatKey], 1) : null
  const oldR = (t.newBuyerCount + t.oldBuyerCount) > 0 ? roundTo(t.oldBuyerCount / (t.newBuyerCount + t.oldBuyerCount) * 100, 1) : null
  const oldRP = (p.newBuyerCount + p.oldBuyerCount) > 0 ? roundTo(p.oldBuyerCount / (p.newBuyerCount + p.oldBuyerCount) * 100, 1) : null
  const oldRW = (hasWk && (wk.newBuyerCount + wk.oldBuyerCount) > 0) ? roundTo(wk.oldBuyerCount / (wk.newBuyerCount + wk.oldBuyerCount) * 100, 1) : null
  const iqC = t.inquiryCount > 0 ? roundTo(t.orderCount / t.inquiryCount * 100, 1) : null
  const iqCP = p.inquiryCount > 0 ? roundTo(p.orderCount / p.inquiryCount * 100, 1) : null
  const iqCW = (hasWk && wk.inquiryCount > 0) ? roundTo(wk.orderCount / wk.inquiryCount * 100, 1) : null
  return {
    gmv: { raw: t.gmv || 0, prev: p.gmv || 0, dod: (typeof pd.gmv === 'number' ? pd.gmv : pct(t.gmv, p.gmv)), week: wkOf('gmvWeekOnWeek') },
    order: { raw: t.orderCount || 0, prev: p.orderCount || 0, dod: (typeof pd.orderCount === 'number' ? pd.orderCount : pct(t.orderCount, p.orderCount)), week: wkOf('orderWeekOnWeek') },
    uv: { raw: t.uv || 0, prev: p.uv || 0, dod: pct(t.uv, p.uv), week: wkOf('uvWeekOnWeek') },
    inquiry: { raw: t.inquiryCount || 0, prev: p.inquiryCount || 0, dod: (typeof pd.inquiryCount === 'number' ? pd.inquiryCount : pct(t.inquiryCount, p.inquiryCount)), week: wkOf('inquiryWeekOnWeek') },
    // 转化率不算环比（百分比的环比口径歧义），保留两个基准原值供直接比对
    conv: { raw: t.payConversionRate || 0, prev: p.payConversionRate || 0, weekPrev: hasWk ? (wk.payConversionRate || 0) : null, dod: null },
    avgPrice: { raw: t.avgPrice || 0, prev: p.avgPrice || 0, dod: pct(t.avgPrice, p.avgPrice), week: wkOf('avgPriceWeekOnWeek') },
    oldRatio: { raw: oldR, prev: oldRP, dod: (oldR !== null && oldRP) ? pct(oldR, oldRP) : null, week: (oldR !== null && oldRW) ? pct(oldR, oldRW) : null },
    inqConv: { raw: iqC, prev: iqCP, dod: (iqC !== null && iqCP) ? pct(iqC, iqCP) : null, week: (iqC !== null && iqCW) ? pct(iqC, iqCW) : null },
  }
}

// @utility:collectAbnormal — 遍历指标集合，|日环比|超阈值即记为异常（含零成交）
// 每条附带 up（方向）/ raw / prev / noisy，供 focusBlock 聚合展示与极小基数降噪；
// metric / change 两个字段保留不变（单店模式与深度分析 prompt 仍在用）。
function collectAbnormal(metrics, thr) {
  const out = []
  const keys = ['gmv', 'order', 'uv', 'inquiry', 'avgPrice', 'oldRatio']
  for (const k of keys) {
    const c = metrics[k]
    if (!c) continue
    if (c.dod !== null && c.dod !== undefined && absNum(c.dod) > thr) {
      out.push({
        metric: METRIC_META[k].name, change: fmtPct(c.dod),
        key: k, dod: c.dod, up: c.dod > 0, raw: c.raw, prev: c.prev,
        // 翻 3 倍以上基本来自极低基数，百分比对商家无阅读价值，改用绝对值对比
        noisy: absNum(c.dod) >= 300,
      })
    }
  }
  if (metrics.uv && metrics.uv.raw > 0 && metrics.gmv && metrics.gmv.raw === 0) out.push({ metric: '零成交', change: '成交额=0', key: 'gmv', dod: null, up: false, raw: 0, prev: metrics.gmv.prev, noisy: false })
  return out
}

// @utility:focusSides — 机会/风险条目聚合：按店铺聚合 + 限量 + 极小基数降噪，返回带 "- " 前缀行文的 {opp, risk} 两个数组
// 店铺多时逐店逐指标平铺会产生「店铺数 × 异常指标数」数十行（7 店最多 42 行），
// 违反 SKILL「总长度控制在手机 3-4 屏内」与多店 400-600 字上限。因此：
//   ① 一店一行，把该店多个异常合并；
//   ② 依赖上游已按成交额降序的 shopMetrics（大店的 10% 比小店的 300% 更值得看）；
//   ③ 各侧最多 cap 家，其余汇总为一句；
//   ④ noisy 项改用「X → Y」绝对值表述，避开 +10836.71% 这类无意义数字。
// perMetric=true（单店模式）：报告标题已含店名，改为逐指标一行（最多 6 行，不会过长）。
// 【四、重点数据】板块已移至子图深度阶段渲染：机会/风险优先用 LLM 生成版（异常事实由脚本注入、
// 模型只做归因解读），本函数产出的程序阈值版作为兜底，确保该板块永不开天窗。
function focusSides(shopMetrics, cap, perMetric) {
  const _cap = cap || 5
  const _val = (ab) => {
    if (ab.metric === '零成交') return '成交额=0'
    if (ab.noisy) return `${fmtNum(ab.prev)} → ${fmtNum(ab.raw)}`
    return ab.change
  }
  const _item = (ab) => ab.metric === '零成交' ? '零成交' : `${ab.metric} ${_val(ab)}`
  const opp = [], risk = []
  if (perMetric) {
    const _one = shopMetrics[0]
    const _abn = (_one && Array.isArray(_one.abnormal)) ? _one.abnormal : []
    for (const ab of _abn) {
      const _line = ab.metric === '零成交' ? '- **零成交** — 有访客但成交额为 0' : `- **${ab.metric}** — ${_val(ab)}`
      if (ab.up === true) opp.push(_line)
      else risk.push(_line)
    }
  } else {
    for (const m of shopMetrics) {
      const _abn = Array.isArray(m.abnormal) ? m.abnormal : []
      const ups = _abn.filter(a => a.up === true).map(_item)
      const downs = _abn.filter(a => a.up !== true).map(_item)
      if (ups.length > 0) opp.push(`- **${m.companyName}**：${ups.join('、')}`)
      if (downs.length > 0) risk.push(`- **${m.companyName}**：${downs.join('、')}`)
    }
  }
  const _clipArr = (arr) => {
    if (arr.length <= _cap || perMetric) return arr
    // 注意：被省略的是「成交额规模靠后」的店，不一定波动小（小店百分比往往更大），文案不得写成「波动较小」
    return arr.slice(0, _cap).concat([`- 其余 ${arr.length - _cap} 家成交额规模较小，已省略`])
  }
  return { opp: _clipArr(opp), risk: _clipArr(risk) }
}

// @utility:adBlock — 广告板块 markdown（含环比 + Top 计划）
function adBlock(adReport) {
  if (!adReport || !adReport.hasData || !adReport.today) return ''
  const t = adReport.today, ch = adReport.changes || {}
  const seg = (label, val, key, money) => {
    const v = money ? fmtNum(val, 2) : fmtNum(val)
    const c = (typeof ch[key] === 'number') ? `(${fmtPct(roundTo(ch[key], 1))})` : ''
    return `${label} ${money ? '¥' : ''}${v}${c}`
  }
  const line = [seg('消耗', t.spend, 'spend', true), seg('曝光', t.exposure, 'exposure', false), seg('点击', t.clicks, 'clicks', false), seg('客户咨询', t.inquiries, 'inquiries', false), seg('成交', t.deals, 'deals', false), `投产比 ${t.roi}`].join(' | ')
  const plans = Array.isArray(adReport.topPlans) ? adReport.topPlans.filter(Boolean).slice(0, 2) : []
  // 消耗 >0 但成交额 =0 的计划展示「无成交」，不展示投产比数值（SKILL「广告分析规范」第 4 条）
  const planLine = plans.length > 0 ? '\n**Top 计划**：' + plans.map(pl => {
    const _noDeal = Number(pl.spend) > 0 && !Number(pl.deal_amount)
    return `${pl.name} 消耗 ¥${fmtNum(pl.spend, 2)}，${_noDeal ? '无成交' : `投产比 ${pl.roi}`}`
  }).join('；') : ''
  return `\n## 二、广告投放\n${line}${planLine}`
}

// @utility:reviewBlock — 评价板块 markdown（含好差评关键词）
function reviewBlock(reviewData) {
  if (!reviewData || !reviewData.hasData || !reviewData.summary) return ''
  const s = reviewData.summary
  const clean = (arr) => (Array.isArray(arr) ? arr.filter(x => x && String(x).trim()).slice(0, 3) : [])
  const good = clean(s.goodReasons)
  const bad = clean(s.badReasons)
  let out = `\n## 三、商品评价\n新增评价 ${s.total} 条 | 好评率 ${s.goodRate}% | 差评率 ${s.badRate}%`
  if (good.length > 0) out += `\n**好评关键词**：${good.join('、')}`
  if (bad.length > 0) out += `\n**差评关键词**：${bad.join('、')}`
  return out
}

// ─── Shared Functions（含原语调用的可复用函数，子图自动继承） ─────

// @shared:readRef
async function readRef(filename) {
  const _isWin = typeof process !== 'undefined' && process.env && (process.env.OS === 'Windows_NT' || !!process.env.TEMP)
  // 命令描述对商家可见：不露英文文件名（三不露），与旁白共用同一句人话
  const _raw = await callTool('Bash', buildBashCommand(_isWin ? 'type' : 'cat', [baseDir + '/references/' + filename], '对照分析指引，定下一步怎么查'))
  const result = parseBashOutput(_raw)
  return result.exitCode === 0 ? result.stdout : ''
}

// @shared:wikiEventEmitter
// 知识大脑子任务的事件回调：**仅统计真正的知识库读取次数，不负责出声**。
// 通过 toolDesc/summary 命中 WikiNav/WikiRead/知识库成功事件，避免把子 Agent
// 顺手调用的其它内置工具误计为知识库读取。state = { readCount, started } 由发起方传入。
// 进度提示由调用方统一输出一行（否则 N 家店并发时会刷出 2N 行逐店提示）。
function wikiEventEmitter(label, state) {
  return (event) => {
    switch (event.type) {
      case 'tool_result_end': {
        // 只统计 WikiNav/WikiRead 的成功读取：兼容工具名与展示文案。
        const desc = `${event.toolDesc || ''}${event.summary || ''}`
        if (/WikiNav|WikiRead|知识库/i.test(desc) && event.state !== 'error') {
          state.started = true
          state.readCount++
        }
        break
      }
      case 'run_finished':
        // 是否真正补充到背景，必须等子任务返回正文后由 collectShopWiki 判断。
        break
    }
  }
}

// @shared:collectShopWiki
// 未真正读到任何知识库页面（含 agent 无 WikiNav/WikiRead 工具时）→ 返回空，
// 丢弃子 Agent 可能产生的空谈/幻觉，不污染下游。失败同样返回空。
// wikiRules 可由调用方预先读好传入：多店并发时避免每家店重复读一次规则文件。
async function collectShopWiki(shop, wikiRules) {
  if (!shop || (!shop.loginId && !shop.companyName)) return ''
  const loginId = shop.loginId || ''
  const companyName = shop.companyName || loginId
  const sceneText = '日报深度分析'
  try {
    const _rules = (typeof wikiRules === 'string' && wikiRules) ? wikiRules : await readRef('wiki-routing-rules.md')
    const wikiState = { readCount: 0, started: false }
    const result = await subTask({
      task: __prompt(baseDir + '/workflow/prompts/collect-shop-wiki.prompt.md', {
        shopName: companyName,
        loginId,
        sceneText,
        wikiRules: _rules,
      }),
      label: companyName,
      tools: ['WikiNav', 'WikiRead'],
      maxRounds: 3,
      onEvent: wikiEventEmitter(companyName, wikiState),
    })
    const wikiContext = typeof result === 'string' ? result.trim() : ''
    // 已补充 = 确实读到过知识库页（readCount>0）且产出了非空摘要；
    // 二者缺一（无工具/没命中/只输出空/纯幻觉无实读）都判为未找到并返回空。
    // 这里不出声：进度提示由调用方汇总成一行，避免逐店刷屏。
    if (wikiContext && wikiState.readCount > 0) return wikiContext
    return ''
  } catch (e) {
    return ''
  }
}

// ─── Constants（子图自动继承） ─────────────────────────────
// @const
const CLI_SCRIPT = baseDir + '/cli.py'
const TMP_DIR = baseDir + '/.tmp'
const PROFILE_INTEGRATED = baseDir + '/references/profiles/integrated.md'
// 经营模式 → Profile 模板路径（infer_profile 推断经营模式后据此加载对应模板）
const PROFILE_TEMPLATES = {
  factory: baseDir + '/references/profiles/factory.md',
  trader: baseDir + '/references/profiles/trader.md',
  integrated: PROFILE_INTEGRATED,
}
// 经营模式 → 中文展示标签（供分析 prompt 使用）
const BIZ_MODE_LABEL = { factory: '工厂/生产型', trader: '贸易商/分销商', integrated: '工贸一体' }
// 各 Profile「额外数据预查询」目录：trigger 命中则纳入 batch_query_profile_data。
// trigger.field 取值来自 infer_profile 推断的 profitSource/supplyCycle/moq/targetCustomer。
const PROFILE_QUERY_CATALOG = {
  factory: [
    { label: '商品动销率', trigger: { field: 'supplyCycle', contains: ['现货'] }, data_source: 'SYCM', api_path: 'portal/core/overview', params: { dataType: 'RECENT_1' } },
    { label: '大客户询盘概况', trigger: { field: 'moq', contains: ['批量'] }, data_source: 'SYCM', api_path: 'customer/inquiry/coreIndex', params: { dateType: 'RECENT_1', indexCode: 'effectiveInQUsers,effectInQCnt,factoryInQUsers,factoryPerfectInQUsers' } },
    { label: '广告花费明细', trigger: { field: 'profitSource', contains: ['薄利', '走量'] }, data_source: 'AD', api_path: '/ad/customer', params: {} },
  ],
  trader: [
    { label: '广告花费明细', trigger: { field: 'profitSource', contains: ['薄利', '走量'] }, data_source: 'AD', api_path: '/ad/customer', params: {} },
    { label: '客户层级分布', trigger: { field: 'profitSource', contains: ['品牌', '溢价', '高客单'] }, data_source: 'SYCM', api_path: 'customer/layerAnalysis', params: { dateType: 'RECENT_7' } },
    { label: '跨境买家占比', trigger: { field: 'targetCustomer', contains: ['跨境'] }, data_source: 'SYCM', api_path: 'customer/businessScenario', params: { dateType: 'RECENT_7', buyerType: '整体客户', page: 1, pageSize: 10 } },
  ],
  integrated: [
    { label: '广告获客成本', trigger: { field: 'profitSource', contains: ['薄利', '走量'] }, data_source: 'AD', api_path: '/ad/customer', params: {} },
    { label: '各渠道流量趋势', trigger: { field: 'profitSource', contains: ['薄利', '走量'] }, data_source: 'SYCM', api_path: 'portal/flowBoard/getFlowSourceTopV2', params: { dataType: 'RECENT_1', device: 'ALL', indexCode: 'uv,crtByrCnt' } },
    { label: '商品动销率', trigger: { field: 'supplyCycle', contains: ['现货'] }, data_source: 'SYCM', api_path: 'portal/core/overview', params: { dataType: 'RECENT_1' } },
    { label: '跨境买家占比', trigger: { field: 'targetCustomer', contains: ['跨境'] }, data_source: 'SYCM', api_path: 'customer/businessScenario', params: { dateType: 'RECENT_7', buyerType: '整体客户', page: 1, pageSize: 10 } },
    { label: '大客户询盘概况', trigger: { field: 'moq', contains: ['批量'] }, data_source: 'SYCM', api_path: 'customer/inquiry/coreIndex', params: { dateType: 'RECENT_1', indexCode: 'effectiveInQUsers,effectInQCnt,factoryInQUsers,factoryPerfectInQUsers' } },
  ],
}
// 异常判定阈值：经营模式 × 阶段（factory 波动大放宽）
const THRESHOLDS = {
  integrated: { 起步: 25, 成长: 12, 成熟: 8 },
  trader: { 起步: 25, 成长: 12, 成熟: 8 },
  factory: { 起步: 30, 成长: 15, 成熟: 8 },
}
// 可渲染的每店指标元数据
const METRIC_META = {
  gmv: { name: '成交额', fmt: 'money0' },
  order: { name: '订单量', fmt: 'int' },
  uv: { name: '访客数', fmt: 'int' },
  inquiry: { name: '客户咨询', fmt: 'int' },
  conv: { name: '成交转化率', fmt: 'pct2', noDod: true },
  avgPrice: { name: '客单价', fmt: 'money2' },
  oldRatio: { name: '老客占比', fmt: 'pct1' },
  inqConv: { name: '询盘转化率', fmt: 'pct1' },
}
// 核心摘要列：经营模式 × 阶段动态选取
const COLUMN_PREFS = {
  integrated: { 起步: ['gmv', 'uv', 'inquiry', 'conv'], 成长: ['gmv', 'order', 'uv', 'conv', 'avgPrice'], 成熟: ['gmv', 'order', 'avgPrice', 'oldRatio'] },
  factory: { 起步: ['gmv', 'uv', 'inquiry', 'conv'], 成长: ['gmv', 'order', 'inqConv', 'avgPrice', 'oldRatio'], 成熟: ['gmv', 'order', 'avgPrice', 'oldRatio'] },
  trader: { 起步: ['gmv', 'uv', 'conv'], 成长: ['gmv', 'order', 'conv', 'avgPrice'], 成熟: ['gmv', 'order', 'avgPrice', 'oldRatio'] },
}
// 用户 Profile 不可从记忆读取，按 SKILL「报告生成规范·空值 Fallback」取默认值
const DEFAULT_IDENTITY = '老板'
const DEFAULT_BIZ_MODE = '工贸一体'
// 日期解析脚本（沙箱禁用 Date，交由 python 计算 queryDate/prevDate 并拦截未来日期）
// 入参：argv[1]=explicitDate（完整 YYYY-MM-DD，可空），argv[2]=dayOffset（距今天数，昨天=1/前天=2）。
// LLM 不知道今天几号，所以「前天/三天前」这类相对日期必须用 dayOffset 表达、在此换算；
// 无法识别时返回 unresolved=true，由上层明确告知用户（绝不静默退回昨天，否则用户以为看的是前天）。
const PYDATE = [
  'import sys,json,datetime',
  'a=(sys.argv[1] if len(sys.argv)>1 else "").strip()',
  'o=(sys.argv[2] if len(sys.argv)>2 else "").strip()',
  't=datetime.date.today()',
  'q=None',
  'bad=False',
  'if a and a!="yesterday":',
  '    try:',
  '        q=datetime.datetime.strptime(a,"%Y-%m-%d").date()',
  '    except Exception:',
  '        bad=True',
  'if q is None:',
  '    n=1',
  '    if o:',
  '        try:',
  '            n=int(float(o))',
  '        except Exception:',
  '            bad=True',
  '    q=t-datetime.timedelta(days=n)',
  'fut = q>=t',
  'p=q-datetime.timedelta(days=1)',
  'print(json.dumps({"queryDate":str(q),"prevDate":str(p),"isFuture":fut,"today":str(t),"unresolved":bad}))',
].join('\n')
// 行动重点关键词 → 行动选项(emoji+名称) → 下游技能 映射（见 references/interaction-specs.md）
const ACTION_MAP = [
  { keywords: ['主图', '图片', '优化图', '详情页'], label: '🖼️ 优化商品主图', skill: '1688-item-image-optimizer' },
  { keywords: ['标题', '关键词', 'SEO', '热搜'], label: '✏️ 优化商品标题', skill: '1688-item-title-optimizer' },
  { keywords: ['商品诊断', '商品分析', '商品问题', '单品', '转化低', '滞销'], label: '🔍 商品分析', skill: '1688-product-analysis' },
  { keywords: ['店铺体检', '全面检查', '店铺健康', '经营诊断', '深度诊断'], label: '🏥 店铺经营诊断', skill: '1688-shop-health-check' },
  { keywords: ['询盘质检', '聊天', '客服', '服务质量', '响应'], label: '💬 询盘质检', skill: '1688-inquiry-evaluate' },
  { keywords: ['客户', '买家', '复购', '老客', '机会'], label: '👥 买家客户管理', skill: '1688-shop-zkt-buyer-manage' },
  { keywords: ['跟进话术', '客户沟通', '回复', '接待'], label: '🗣️ 客服接待路由', skill: '1688-cowboy' },
  { keywords: ['流量异常', '流量下降', '异常提醒', '流量异动'], label: '⚠️ 店铺流量异动诊断', skill: '1688-shop-abnormal-alert' },
  { keywords: ['数据分析', '查看数据', '更多数据', '深入分析', '广告', '投放'], label: '📊 数据查询分析', skill: '1688-shop-freedom-query-data' },
]

// ═══ Main Flow ═══════════════════════════════════════════

phase('意图识别')

// @node:parse_args [transform] source:args,params outputs:userInput,paramsDate
const userInput = (typeof args === 'string' && args.trim()) ? args.trim() : ''
// 框架约定：LLM 传 {query, params} 时 query→args、params→同名全局对象（engine 归一化注入）。
// outer agent 纠错重试会主动带上 params.date（线上已多次观测且值正确），它是显式指定的
// 日历日期，优先级高于 LLM 意图解析——可免疫缺年份/点分形态（"8.15"）的年份误判。
// 仅接受严格 YYYY-MM-DD；非法/缺失则留空走 LLM 路径；最终仍由 PYDATE 校验（不存在
// 的日期如 02-30 会落 unresolved），未来日期仍被 future_return 拦截，语义不破。
let paramsDate = ''
try {
  const _pd = (typeof params === 'object' && params) ? String(params.date || '').trim() : ''
  if (/^\d{4}-\d{2}-\d{2}$/.test(_pd)) paramsDate = _pd
} catch { /* params 不可用：忽略，走 LLM 解析路径 */ }

// 沙箱禁用 Date，先用 python 拿「今天」注入意图识别 prompt：缺年份的月日（"8月15日"）
// 和日期范围（"16日到20日"）都必须基于今天才能换算成 explicitDate，否则 LLM 只能留空
// 静默退回昨天（用户以为看的是指定日期，实际是昨天）。与 resolve_dates 同理原地重试一次
// 防框架首调竞态；两次都失败则 today 为空，prompt 按保守规则（缺年份/范围→昨天）降级，不阻断主流程。
let today = ''
for (let _attempt = 0; _attempt < 2 && !today; _attempt++) {
  const _tp = await callTool('Bash', buildBashCommand('python3', ['-c', PYDATE, '', ''], '核对今天日期'))
  try { today = String(JSON.parse(parseBashOutput(_tp).stdout.trim()).today || '') } catch { /* 解析失败：进入下一次重试 */ }
}

// @node:classify_intent [agent] inputs:userInput,today outputs:mode,shopHint,dateArg,dayOffset,isRange
emit('<aside>📋 让我想想怎么样更好地把报告展示给你…</aside>')
// agent 失败（超时/模型报错）不得拖垮整个 workflow：回落多店+昨天默认值照常出日报。
// 多店覆盖全部绑定店铺不漏数据，相对日期默认昨天，与无输入时的行为一致。
let intent = null
try {
  intent = parseAgentResult(await agent(
    __prompt('./prompts/classify-intent.prompt.md', { userInput, today }),
    { label: 'classify-intent', schema: {
      type: 'object', required: ['mode'],
      properties: {
        mode: { type: 'string', enum: ['single', 'multi'] },
        shopHint: { type: 'string' },
        explicitDate: { type: 'string' },
        dayOffset: { type: 'number' },
        isRange: { type: 'boolean' },
      },
    } }
  ))
} catch (e) {
  emit('<aside>⚠️ 需求理解这一步没跑成，我按默认方式（全部店铺+昨天）给你出日报</aside>')
}
// shopHint 兼容校验：LLM 偶发把技能名/工作流名（如 1688-shop-daily-report）或「1688店铺」这类泛称
// 当成店铺名，导致误入单店模式且定位不到店铺。命中泛称/技能标识即视为未指定店铺。
const _INVALID_HINT = /^\s*(1688)?\s*(店铺|我的?店铺?|本店|我们店|shop|store)\s*$|shop-daily-report|daily-report|workflow|工作流|技能/i
const _rawHint = String(intent?.shopHint || '').trim()
const shopHint = (_rawHint.length >= 2 && !_INVALID_HINT.test(_rawHint)) ? _rawHint : ''
// 硬约束：单店模式必须同时拿到有效店铺名，否则一律回退多店（多店覆盖全部绑定店铺，不会漏数据）
const mode = (intent?.mode === 'single' && shopHint) ? 'single' : 'multi'
const isSingleMode = mode === 'single'
// params.date 显式指定时覆盖 LLM 的日期判断（店铺范围与相对日期意图仍由 LLM 解析）
const dateArg = paramsDate || String(intent?.explicitDate || '').trim()
const dayOffset = paramsDate ? '0' : ((typeof intent?.dayOffset === 'number' && intent?.dayOffset >= 0) ? String(intent?.dayOffset) : '1')

phase('日期解析')

// @node:resolve_dates [tool] inputs:dateArg,dayOffset outputs:dates
emit('<aside>⚙️ 报表日期选多久好呢，让我想想</aside>')
// 端侧框架小概率让首个 callTool 返回空（竞态，跨平台），此时 stdout 解析不出日期 JSON；
// 原地重试一次仍失败才按未识别处理，避免把框架空返回误判成「日期无法识别」而误报「数据尚未回收」。
let dates = { queryDate: '', prevDate: '', isFuture: false, unresolved: false }
let _drDiag = '未执行'
for (let _attempt = 0; _attempt < 2 && !dates.queryDate; _attempt++) {
  const _dr = await callTool('Bash', buildBashCommand('python3', ['-c', PYDATE, dateArg, dayOffset], '核对日报数据日期'))
  const _drOut = parseBashOutput(_dr)
  _drDiag = `exitCode=${_drOut.exitCode} stderr=${_drOut.stderr.slice(0, 200)}`
  try {
    const _parsed = JSON.parse(_drOut.stdout.trim())
    if (_parsed && _parsed.queryDate) dates = _parsed
  } catch { /* 解析失败：进入下一次重试 */ }
}
// 日期未能识别时明确告知实际用了哪一天，不让用户误以为看的是自己要的那天
if (dates.unresolved && dates.queryDate) emit(`<aside>⚠️ 未能识别您说的日期，已按 ${dates.queryDate} 生成</aside>`)

phase('模式分发')

// @node:dispatch [condition] expression:dates.isFuture / mode
if (dates.isFuture || !dates.queryDate) {
  // @branch:今日或未来日期 → future_return
  // @node:future_return [end] inputs:dates
  if (!dates.queryDate) {
    // 命令层两次都没返回有效日期 JSON（竞态/解释器异常），并非真的未来日期：
    // 商家可见信息保持克制，技术诊断写进 return 供上层与日志排查
    emit('### ⚠️ 无法生成日报\n\n日期解析失败，请稍后重试。')
    return `日报生成终止：日期解析命令两次均未返回有效结果（非日期问题）。诊断：${_drDiag}`
  }
  emit(`### ⚠️ 无法生成日报\n\n「${dates.queryDate || dateArg}」的数据尚未回收。日报数据 T+1 更新，最早可查询昨天的数据，请指定一个不晚于昨天的日期。`)
  return `日报生成终止：「${dates.queryDate || dateArg}」为今日或未来日期，数据未回收。请将原因如实告知用户，不要自行改写日期重新调用本 workflow；用户确认查询其他日期时会明确发起新请求。`
}
// @branch:日期合法 → run_report

// 范围查询按「范围内不晚于昨天的最后一天」单日出报（prompt 已让 LLM 基于今天换算好），
// 明确告知实际出的是哪天，避免用户误以为拿到的是整个范围
if (intent?.isRange) emit(`<aside>📅 日报按单日生成，已为您生成「${dates.queryDate}」的日报；想看多天可逐日查询对比</aside>`)

// @node:run_report [subgraph] ref:./sub/shop-report.js inputs:mode,shopHint,queryDate,prevDate,userInput outputs:reportPayload
// 单店与多店共用同一子图（CLI 层本就是同一条并发管线，仅店铺范围不同），mode 控制内部 3 处差异
emit(isSingleMode
  ? `<aside>📋 这就给你出「${shopHint}」${dates.queryDate} 的日报！</aside>`
  : `<aside>📋 你绑了多家店，每家的情况我都会报告给你！（${dates.queryDate}）</aside>`)
const reportPayload = await __subgraph('./sub/shop-report.js', {
  mode, shopHint, queryDate: dates.queryDate, prevDate: dates.prevDate, resolvedDate: dates.queryDate, userInput,
})

// 子图取数/校验失败时返回终止字符串（"日报生成终止：..."），成功时返回
// {actions, reportKind, shopCount, overview, insights} 对象。失败必须原样终止透传：
// 此前未做检查直接走收尾，会照常弹追问卡片并 return「任务已完成/queryStatus=fulfilled」
// 把失败谎报成成功（线上实锤：HTTP 409 后 outer agent 被告知任务完成，放弃补救）。
if (!reportPayload || typeof reportPayload !== 'object') {
  return String(reportPayload || '日报生成终止：子流程未返回有效结果')
}

phase('行动选择')

// @node:build_options [transform] inputs:reportPayload outputs:actionOptions
// 按行动重点关键词匹配 ACTION_MAP，构建 2-6 个行动选项（emoji+名称+简短说明）
// 卡片逻辑放在主图：子图间横向 __subgraph 引用在平台上会报 missing file（见 sub/shop-report.js 末尾说明）。
const _actions = Array.isArray(reportPayload?.actions) ? reportPayload.actions : []
const _reportKind = reportPayload?.reportKind || '多店铺'
const _shopCount = reportPayload?.shopCount || 0
const _entries = []
const _seen = new Set()
for (const a of _actions) {
  const text = actionText(a)
  const matched = ACTION_MAP.find(m => m.keywords.some(k => text.includes(k)))
  if (matched && !_seen.has(matched.label)) {
    _seen.add(matched.label)
    _entries.push({ label: `${matched.label}（${text.slice(0, 16)}）`, skill: matched.skill })
  }
}
// 数量兜底：不足 2 个补充通用诊断项
if (_entries.length < 2 && !_seen.has('🏥 店铺经营诊断')) {
  _entries.push({ label: '🏥 店铺经营诊断（全面排查经营问题）', skill: '1688-shop-health-check' })
  _seen.add('🏥 店铺经营诊断')
}
if (_entries.length < 2) {
  _entries.push({ label: '🔍 商品分析（定位问题商品）', skill: '1688-product-analysis' })
}
const actionOptions = _entries.slice(0, 6)

// @node:build_followup_card [agent] inputs:userInput,actionOptions outputs:followupCard
// agent 生成追问卡片 JSON 参数（question/options），同时充当「反问闸门」：
// userInput 明确写了不需要反问（如「不用反问」）时返回 needInteraction=false，跳过卡片弹窗。
// 解析失败按 parseAgentResult 约定回落 null，下游兜底为默认卡片照常弹出（不得静默吞掉交互）。
emit('<aside>📋 正在整理接下来可以帮你做的事</aside>')
// 追问卡片 agent 失败不得拖垮收尾：回落 null，下游照旧用默认文案+候选列表弹卡片
let followupCard = null
try {
  followupCard = parseAgentResult(await agent(
    __prompt('./prompts/followup-card.prompt.md', {
      userInput,
      candidateOptions: JSON.stringify(actionOptions.map(o => o.label)),
    }),
    { label: 'followup-card', schema: {
      type: 'object', required: ['needInteraction'],
      properties: {
        needInteraction: { type: 'boolean' },
        question: { type: 'string' },
        options: { type: 'array', items: { type: 'string' } },
      },
    } }
  ))
} catch (e) {
  // 解析失败/调用失败都不得静默吞掉交互：默认弹卡片，保持原行为
}

// @node:dispatch_followup [condition] expression:followupCard.needInteraction
// 仅当 agent 明确判定「不需要反问」（用户在输入中主动声明）才跳过交互；
// agent 解析失败 / 未给字段时一律默认弹卡片，保持原有行为。
let nextAction = ''
let nextSkill = ''
let _chosen = null
if (followupCard && followupCard.needInteraction === false) {
  // @branch:无需反问（用户明确声明） → return_report
  emit('<aside>✅ 已按您的要求跳过追问卡片</aside>')
} else {
  // @branch:需要反问 → show_action_card

  // @node:show_action_card [interaction] inputs:actionOptions,followupCard outputs:actionResult
  // 字段对齐生产在跑的 workflow（1688-shop-health-check / 1688-item-image-optimizer）：
  // 只传 type / selectionType / questions，**不传 name**（name 是技能路径的 metadata 字段，
  // workflow 原语不识别，多传会导致卡片渲染失败）。
  // question/options 优先用 agent 产出的卡片参数，缺失时回退默认文案与候选列表。
  const _followupQuestion = (followupCard && typeof followupCard.question === 'string' && followupCard.question.trim())
    ? followupCard.question.trim()
    : '📋 以上是今日经营日报。根据数据分析，建议您优先执行以下行动，请选择：'
  const _followupOptions = (followupCard && Array.isArray(followupCard.options) && followupCard.options.filter(Boolean).length >= 2)
    ? followupCard.options.filter(Boolean)
    : actionOptions.map(o => o.label)
  emit('<aside>🔄 到你了——下面几件事，挑一件我马上去办</aside>')
  const actionResult = await showInteraction({
    type: 'card',
    selectionType: 'requirement',
    questions: [{
      question: _followupQuestion,
      options: _followupOptions,
      allowMultiple: false,
      required: true,
    }],
  })

  // @node:parse_choice [transform] source:actionResult outputs:nextAction,nextSkill
  nextAction = extractAnswer(actionResult)
  _chosen = actionOptions.find(o => nextAction && (o.label === nextAction || nextAction.includes(o.label.slice(0, 6))))
  nextSkill = _chosen?.skill || ''
  if (nextAction) emit(`<aside>✅ 已选择「${nextAction}」</aside>`)
}

// @node:return_report [end] inputs:nextAction,nextSkill,followupCard outputs:
const _matchedAction = _actions.find(a => nextAction && _chosen && _chosen.skill && actionText(a).includes(_chosen.label.slice(0, 4)))
// 免反问（定时任务/用户声明不需要追问）时没有交互步骤，返回文本必须显式声明这是预期路径，
// 否则外层 Agent 会把「没弹卡片/没拿到选择」误判为 workflow 未跑完，按 SKILL.md 回退规则
// 重新加载技能从头重跑一遍（已实测：定时任务场景下真实发生过）。
const _interactionSkipped = !!(followupCard && followupCard.needInteraction === false)
// 免反问路径（用户声明不追问 / 定时任务）：日报正文已 emit 完毕，workflow 到此结束。
// 返回值只给强完结信号，**不再附带日报结论摘要**——带上摘要后外层 Agent 会照着内容把日报
// 再完整输出一遍（已实测），用户明确要求跳过追问时不要重复输出。
if (_interactionSkipped) {
  return `✅ 任务已完成：${_reportKind}日报已由 workflow 完整生成，报告正文已在上方全部输出，用户要求的全部经营指标（交易/成交金额、订单量、支付买家数、询盘/客户咨询及环比）均已覆盖。
🛑 到此直接结束任务：不要把日报内容再输出一遍（无论全文还是摘要总结）；不要重新执行任何 CLI 命令；不要回退到技能路径重跑日报。
ℹ️ 本次按用户要求（或定时任务场景）跳过了追问卡片，这是正常完结流程，不是错误，也不需要用任何文字向用户复述日报内容。

<execution_manifest>
${JSON.stringify({ queryDate: dates.queryDate, reportKind: _reportKind, shopCount: _shopCount, queryStatus: 'fulfilled', taskComplete: true, interactionSkipped: true, outputAlreadyEmitted: true, actionSelected: null, nextSkill: null }, null, 2)}
</execution_manifest>`
}
// 有追问卡片的常规路径：必然是用户实时会话（emit 正文用户都看得到），返回值**同样不附带
// 任何日报内容**——带摘要/行动清单后外层 Agent 会照着复述日报（已实测：用户在卡片选了
// 「数据查询分析」，外层 Agent 却先把日报又输出了一遍）。只给强完结信号 + 行动衔接指令。
return `✅ 任务已完成：${_reportKind}日报已由 workflow 完整生成，报告正文已在上方全部输出，用户已在会话中看到完整日报，用户要求的全部经营指标（交易/成交金额、订单量、支付买家数、询盘/客户咨询及环比）均已覆盖。
🛑 不要把日报内容再输出一遍（无论全文还是摘要总结）；不要重新执行任何 CLI 命令；不要回退到技能路径重跑日报 —— workflow 已正常执行完毕，queryStatus=fulfilled。

<execution_manifest>
${JSON.stringify({ queryDate: dates.queryDate, reportKind: _reportKind, shopCount: _shopCount, queryStatus: 'fulfilled', taskComplete: true, interactionSkipped: _interactionSkipped, outputAlreadyEmitted: true, actionSelected: nextAction || null, nextSkill: nextSkill || null }, null, 2)}
</execution_manifest>
${nextAction && nextSkill ? `\n⏭️ 用户已在行动卡片中选择「${nextAction}」，请立即调用技能 ${nextSkill} 开始执行，无需等待用户再次确认，也不需要先复述日报。${_matchedAction ? `\n上下文：${actionText(_matchedAction)}` : ''}` : nextAction ? `\n用户已选择「${nextAction}」，未匹配到对应技能，请根据用户选择引导后续操作，不需要复述日报内容。` : '\n用户暂无进一步选择，简短收尾确认即可，无需复述日报内容。'}`
