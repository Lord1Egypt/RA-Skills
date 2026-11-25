/**
 * dsh-capability-loop-bundle — 控制台（client half）
 *
 * 在侧边栏注册一个全局面板「能力闭环」，只读展示 `.dsh/loop/state.json`：
 * 档位 / 阶段 / 门禁 / 阻断 / 下一步。数据经 `GET /api/file?path=` 读取
 * （已认证的 connection 通道，不需要会话），不写任何文件。
 *
 * 依据（已核源码/README，DSH 0.2.2-rc.3）：
 *   - client 产物格式：dsh-doc `templates/decoration/client.js`（`window.__ModuleLoader__.load`）
 *   - 面板注册：`sidebar.panellist`（id/order/label/icon）+ `main`（同名 key）
 *   - 读文件通道：`dsh-api-session-controller` README §SessionMediaReferences —
 *     `GET|HEAD /api/file?path=<absolute path>`，`connection.fetch(request, peer)` +
 *     `ctx.connection.browserPeer`
 *   - `$host.home`：`dsh-api-gateway` README §Client service（`ctx.remote.$host`）
 */
window.__ModuleLoader__.load({
  id: 'dsh-capability-loop-bundle',
  factory(require) {
    const React = require('react')
    const h = React.createElement

    /** apply() 收到的插件 ctx；面板据此读服务（不依赖 slot props 形状）。 */
    let pluginCtx

    const PANEL_ID = 'capability-loop'
    // 面板自身版本：用来判断渲染器加载的是不是最新 client.js（桌面正式版没有 Ctrl+R，见 README）
    const PANEL_VERSION = '2.14.2'
    const STAGE_ORDER = ['INTAKE', 'AUDIT', 'FIX', 'WIRE', 'HANDOFF', 'GRILL', 'GATE']
    const CHECK_LABEL = {
      design: '设计门',
      requirement: '需求门',
      test: '测试门',
      handoff: '交接体检',
      grill: 'grill',
      environment: '环境验收',
      'environment-audit': '能力体检',
    }

    // ---------- 样式（只用主题 token，不新增色值） ----------
    const S = {
      page: {
        height: '100%', overflow: 'auto', background: 'var(--dsw-alias-bg-base)',
        color: 'var(--dsw-alias-label-primary)', padding: '22px 40px 40px',
      },
      inner: { maxWidth: 960, margin: '0 auto' },
      head: { display: 'flex', alignItems: 'flex-start', gap: 16 },
      h1: { margin: 0, fontSize: 20, fontWeight: 600, lineHeight: 1.35, letterSpacing: '-0.2px' },
      sub: {
        margin: '7px 0 0', fontSize: 13, color: 'var(--dsw-alias-label-tertiary)',
        display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center',
      },
      dotsep: { color: 'var(--dsw-alias-label-caption)' },
      kpis: { display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, marginTop: 18 },
      kpisCompact: { display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: 10, marginTop: 18 },
      kpi: {
        background: 'var(--dsw-alias-card-fill)', border: '1px solid var(--dsw-alias-border-l1)',
        borderRadius: 'var(--dsw-radius-md)', padding: '11px 14px', minHeight: 68,
        display: 'flex', flexDirection: 'column', gap: 5,
      },
      kpiK: { fontSize: 11, color: 'var(--dsw-alias-label-caption)' },
      kpiV: { fontSize: 18, fontWeight: 600, lineHeight: 1.1, display: 'flex', alignItems: 'baseline', gap: 5 },
      kpiM: { marginTop: 'auto', fontSize: 11, color: 'var(--dsw-alias-label-tertiary)', lineHeight: 1.3 },
      card: {
        border: '1px solid var(--dsw-alias-border-l2)', borderRadius: 'var(--dsw-radius-md)',
        background: 'var(--dsw-alias-card-fill)', overflow: 'hidden', marginTop: 14,
      },
      cardHd: {
        display: 'flex', alignItems: 'center', gap: 8, padding: '11px 14px 9px',
        fontSize: 13, fontWeight: 600, flexWrap: 'wrap',
      },
      hint: { marginLeft: 'auto', fontSize: 11, fontWeight: 400, color: 'var(--dsw-alias-label-caption)' },
      row: {
        display: 'flex', alignItems: 'center', gap: 10, minHeight: 38, padding: '6px 14px',
        borderTop: '1px solid var(--dsw-alias-border-l1)', fontSize: 12,
      },
      name: { width: 112, color: 'var(--dsw-alias-label-primary)' },
      meta: { color: 'var(--dsw-alias-label-tertiary)', fontSize: 11 },
      right: { marginLeft: 'auto', color: 'var(--dsw-alias-label-caption)', fontSize: 11 },
      badge: {
        display: 'inline-flex', alignItems: 'center', gap: 5, height: 20, padding: '0 7px',
        borderRadius: 5, fontSize: 10, fontWeight: 600, color: 'var(--dsw-alias-label-primary)',
      },
      track: { display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 4, padding: '4px 14px 14px' },
      stage: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 7, fontSize: 12 },
      node: {
        width: 18, height: 18, borderRadius: '50%', display: 'grid', placeItems: 'center',
        fontSize: 9, fontWeight: 600, border: '1px solid var(--dsw-alias-border-l3)',
        background: 'var(--dsw-alias-bg-base)', color: 'var(--dsw-alias-label-caption)',
      },
      stageName: { color: 'var(--dsw-alias-label-secondary)' },
      btn: {
        border: '1px solid var(--dsw-alias-border-l2)', background: 'var(--dsw-alias-bg-base)',
        color: 'var(--dsw-alias-label-primary)', fontSize: 12, borderRadius: 6,
        padding: '7px 10px', cursor: 'pointer',
      },
      select: {
        border: '1px solid var(--dsw-alias-border-l2)', background: 'var(--dsw-alias-bg-base)',
        color: 'var(--dsw-alias-label-primary)', fontSize: 12, borderRadius: 6, padding: '6px 8px',
      },
      input: {
        border: '1px solid var(--dsw-alias-border-l2)', background: 'var(--dsw-alias-bg-base)',
        color: 'var(--dsw-alias-label-primary)', fontSize: 12, borderRadius: 6, padding: '6px 8px',
        minWidth: 90, flex: '0 1 190px',
      },
      btnPrimary: {
        background: 'var(--dsw-alias-state-business-primary)',
        borderColor: 'transparent',
        color: 'var(--dsw-alias-label-on-color)',
      },
      runRow: {
        display: 'flex', alignItems: 'center', gap: 8, minHeight: 40, padding: '6px 14px',
        borderTop: '1px solid var(--dsw-alias-border-l1)', fontSize: 12, flexWrap: 'wrap',
      },
      seg: {
        display: 'inline-flex', border: '1px solid var(--dsw-alias-border-l2)',
        borderRadius: 6, overflow: 'hidden', background: 'var(--dsw-alias-bg-base)',
      },
      segItem: {
        border: 'none', background: 'transparent', color: 'var(--dsw-alias-label-secondary)',
        fontSize: 12, padding: '6px 10px', cursor: 'pointer',
      },
      segOn: {
        background: 'var(--dsw-alias-state-business-primary)',
        color: 'var(--dsw-alias-label-on-color)',
        fontWeight: 600,
      },
      pre: {
        margin: '0 14px 12px', padding: '10px 12px', background: 'var(--dsw-alias-bg-layer-2)',
        borderRadius: 6, maxHeight: 220, overflow: 'auto', whiteSpace: 'pre-wrap',
        fontFamily: 'var(--ds-font-family-code, monospace)', fontSize: 11,
        color: 'var(--dsw-alias-label-primary)', lineHeight: 1.55,
      },
      overlay: {
        position: 'fixed', inset: 0,
        background: 'var(--dsw-alias-bg-mask-3, rgba(0,0,0,.55))',
        backdropFilter: 'blur(4px)', WebkitBackdropFilter: 'blur(4px)',
        display: 'grid', placeItems: 'center', zIndex: 9999,
      },
      modal: {
        width: 560, maxWidth: 'calc(100vw - 40px)', maxHeight: '82vh', overflow: 'auto',
        // 两层背景：先铺主题色，再压一层静态深色底——玻璃皮肤把 alias 调成半透明时仍不透视。
        background: 'linear-gradient(var(--dsw-alias-bg-base), var(--dsw-alias-bg-base)), var(--dsw-static-neutral-bluish-950)',
        border: '1px solid var(--dsw-alias-border-l3)',
        borderRadius: 12, padding: '20px 22px',
        boxShadow: '0 24px 64px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.05)',
        backdropFilter: 'blur(24px) saturate(140%)', WebkitBackdropFilter: 'blur(24px) saturate(140%)',
      },
      modalBar: {
        height: 3, borderRadius: 3, marginBottom: 14,
        background: 'var(--dsw-alias-state-business-primary)',
      },
      modalHd: { margin: 0, fontSize: 16, fontWeight: 600, lineHeight: 1.4 },
      modalBody: { marginTop: 10, fontSize: 12, color: 'var(--dsw-alias-label-secondary)', lineHeight: 1.6 },
      modalFt: { display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 16 },
      projectBar: {
        display: 'flex', alignItems: 'center', gap: 10, marginTop: 14, padding: '8px 12px',
        border: '1px solid var(--dsw-alias-border-l2)', borderRadius: 8,
        background: 'var(--dsw-alias-bg-layer-1)', fontSize: 12, flexWrap: 'wrap',
      },
      projectTag: { color: 'var(--dsw-alias-label-caption)', fontSize: 11, flex: 'none' },
      projectPath: {
        color: 'var(--dsw-alias-label-tertiary)', fontFamily: 'var(--ds-font-family-code, monospace)',
        fontSize: 11, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      },
      projectChip: {
        display: 'inline-flex', alignItems: 'center', height: 18, padding: '0 6px',
        borderRadius: 4, fontSize: 10, fontWeight: 500,
        background: 'var(--dsw-alias-bg-layer-2)', border: '1px solid var(--dsw-alias-border-l1)',
        color: 'var(--dsw-alias-label-tertiary)',
      },
      empty: { textAlign: 'center', padding: '56px 0 0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10 },
      mono: { fontFamily: 'var(--ds-font-family-code, monospace)', fontSize: 11 },
    }

    function statusColor(status) {
      if (status === 'PASS') return 'var(--dsw-alias-state-success-primary)'
      if (status === 'WARN') return 'var(--dsw-alias-state-warn-primary)'
      if (status === 'FAIL') return 'var(--dsw-alias-state-error-primary)'
      return 'var(--dsw-alias-label-caption)'
    }

    function Badge(props) {
      const status = props.status === undefined ? 'MISSING' : String(props.status)
      const color = statusColor(status)
      const missing = status === 'MISSING' || status === ''
      return h('span', {
        style: {
          ...S.badge,
          background: missing ? 'transparent' : 'color-mix(in srgb, ' + color + ' 10%, transparent)',
          border: missing ? '1px dashed var(--dsw-alias-border-l3)' : 'none',
          color: missing ? 'var(--dsw-alias-label-tertiary)' : 'var(--dsw-alias-label-primary)',
        },
      },
        h('span', {
          style: { width: 5, height: 5, borderRadius: '50%', background: missing ? 'var(--dsw-alias-label-caption)' : color },
        }),
        status === 'MISSING' || status === '' ? '未运行' : status,
      )
    }

    // ---------- 数据 ----------
    // 主通道：`ctx.remote.session.list` 拿会话（含 cwd）→ `workspaceFiles.read(sessionId, 相对路径)`
    // 读 `<cwd>/.dsh/loop/{project,state}.json`。相对路径自动落在该会话的工作区根，
    // 因此不需要知道 DSH home，也不需要 `/api/file`（桌面壳的渲染器不是 http 源，走不通）。
    // 备通道：浏览器里若 `connection.fetch` 存在，退回 `/api/file?path=`。
    let lastDiagnostic = ''
    function recordDiagnostic(text) {
      const value = String(text || '')
      if (value !== '') lastDiagnostic = value
    }

    function unwrap(result) {
      if (result === null || result === undefined) return undefined
      if (typeof result === 'object' && 'ok' in result) return result.ok === true ? result.value : undefined
      return result
    }

    function joinPath(base, rel) {
      const trimmed = String(base).replace(/[\\/]+$/, '')
      return trimmed.replace(/\\/g, '/') + '/' + rel
    }

    /** 用某个会话的身份读工作区相对路径；读不到返回 null。 */
    async function readJsonViaSession(filesNamespace, sessionId, relPath) {
      let result
      try {
        result = await filesNamespace.read(sessionId, relPath, {}, undefined)
      } catch (error) {
        recordDiagnostic('workspaceFiles.read 抛错（' + relPath + '）：' + String(error && error.message ? error.message : error))
        return null
      }
      const value = unwrap(result)
      if (value === undefined || typeof value.text !== 'string') return null
      try {
        return JSON.parse(value.text)
      } catch {
        recordDiagnostic('非 JSON：' + relPath)
        return null
      }
    }

    /** 备通道：/api/file?path=（仅当 connection.fetch 存在，例如普通浏览器载体）。 */
    async function readJsonViaFileApi(ctx, absPath) {
      const connection = ctx.get('connection')
      if (connection === undefined || connection === null || typeof connection.fetch !== 'function') return null
      const peer = connection.browserPeer
      const query = '/api/file?path=' + encodeURIComponent(absPath)
      const candidates = [query]
      try {
        const origin = typeof location !== 'undefined' && location.origin ? location.origin : ''
        if (origin !== '' && origin !== 'null' && origin.indexOf('http') === 0) {
          candidates.push(origin.replace(/\/+$/, '') + query)
        }
      } catch {
        // 没有 location 就只走相对路径
      }
      for (const url of candidates) {
        let response
        try {
          response = await connection.fetch(url, peer)
        } catch (error) {
          recordDiagnostic('fetch 抛错 ' + url + '：' + String(error && error.message ? error.message : error))
          continue
        }
        if (response === undefined || response === null || !response.ok) {
          recordDiagnostic('HTTP ' + (response === undefined || response === null ? '?' : response.status) + ' ' + url)
          continue
        }
        try {
          return JSON.parse(await response.text())
        } catch (error) {
          recordDiagnostic('响应不是 JSON：' + String(error && error.message ? error.message : error))
        }
      }
      return null
    }

    /** 收集所有「已接入」工程；按会话最近使用排序。 */
    async function collect(ctx) {
      const remote = ctx.get('remote')
      const sessionNamespace = remote !== undefined && remote !== null ? remote.session : undefined
      const filesNamespace = remote !== undefined && remote !== null ? remote.workspaceFiles : undefined

      if (sessionNamespace === undefined || typeof sessionNamespace.list !== 'function'
        || filesNamespace === undefined || typeof filesNamespace.read !== 'function') {
        recordDiagnostic('当前 composition 没有 remote.session / remote.workspaceFiles，面板暂时读不到状态')
        return { projects: [] }
      }

      let listResult
      try {
        listResult = await sessionNamespace.list({})
      } catch (error) {
        recordDiagnostic('session.list 失败：' + String(error && error.message ? error.message : error))
        return { projects: [] }
      }
      const listed = unwrap(listResult)
      const items = listed !== undefined && Array.isArray(listed.items) ? listed.items : []
      if (items.length === 0) {
        recordDiagnostic('还没有任何会话（面板需要一个会话作为读取凭据）')
        return { projects: [] }
      }

      // 每个工作区取最近的一个会话作为读取凭据
      const byWorkspace = new Map()
      for (const item of items) {
        if (item === null || item === undefined) continue
        const cwd = typeof item.cwd === 'string' && item.cwd !== '' ? item.cwd : ''
        if (cwd === '') continue
        const previous = byWorkspace.get(cwd)
        const stamp = typeof item.updatedAt === 'number' ? item.updatedAt : 0
        if (previous === undefined || stamp > previous.stamp) {
          byWorkspace.set(cwd, { cwd, sessionId: item.sessionId, stamp })
        }
      }
      const workspaces = Array.from(byWorkspace.values()).sort((a, b) => b.stamp - a.stamp).slice(0, 12)

      const projects = []
      for (const workspace of workspaces) {
        const project = await readJsonViaSession(filesNamespace, workspace.sessionId, '.dsh/loop/project.json')
        if (project === null) continue
        const state = await readJsonViaSession(filesNamespace, workspace.sessionId, '.dsh/loop/state.json')
        projects.push({
          workspace: {
            id: workspace.cwd,
            path: workspace.cwd,
            title: typeof project.name === 'string' && project.name !== '' ? project.name : workspace.cwd,
            sessionId: workspace.sessionId,
          },
          project,
          state,
        })
      }
      if (projects.length === 0 && lastDiagnostic === '') {
        recordDiagnostic('读了 ' + workspaces.length + ' 个工作区，都没有 .dsh/loop/project.json（未接入）')
      }
      return { projects }
    }

    /** 备通道入口：把工作区列表换成 state（仅在 remote.session 不可用时使用）。 */
    async function collectViaFileApi(ctx) {
      const remote = ctx.get('remote')
      const home = remote !== undefined && remote !== null && remote.$host !== undefined ? remote.$host.home : undefined
      if (typeof home !== 'string' || home === '') {
        recordDiagnostic('拿不到 Host home，无法定位 workspace.json')
        return { projects: [] }
      }
      const workspaceFile = await readJsonViaFileApi(ctx, joinPath(home, 'storages/workspace.json'))
      const table = workspaceFile !== null && workspaceFile.tables !== undefined ? workspaceFile.tables.workspaces : undefined
      if (table === undefined || table === null || typeof table !== 'object') return { projects: [] }
      const rows = []
      for (const id of Object.keys(table)) {
        const row = table[id]
        if (row === null || row === undefined || typeof row.path !== 'string') continue
        rows.push({ id, path: row.path, title: typeof row.title === 'string' ? row.title : row.path, updatedAt: String(row.updatedAt || '') })
      }
      rows.sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : a.updatedAt > b.updatedAt ? -1 : 0))
      const projects = []
      for (const workspace of rows.slice(0, 12)) {
        const project = await readJsonViaFileApi(ctx, joinPath(workspace.path, '.dsh/loop/project.json'))
        if (project === null) continue
        const state = await readJsonViaFileApi(ctx, joinPath(workspace.path, '.dsh/loop/state.json'))
        projects.push({
          workspace: { ...workspace, sessionId: '' },
          project,
          state,
        })
      }
      return { projects }
    }

    async function collectAny(ctx) {
      const remote = ctx.get('remote')
      const hasSessionRemote = remote !== undefined && remote !== null
        && remote.session !== undefined && typeof remote.session.list === 'function'
        && remote.workspaceFiles !== undefined && typeof remote.workspaceFiles.read === 'function'
      if (hasSessionRemote) return collect(ctx)
      return collectViaFileApi(ctx)
    }
    function stageIndexOf(state) {
      const stage = state !== null && state !== undefined && typeof state.stage === 'string' ? state.stage : 'INTAKE'
      const index = STAGE_ORDER.indexOf(stage)
      return { stage, index: index < 0 ? 0 : index }
    }

    function checksOf(state) {
      const rows = []
      if (state === null || state === undefined || typeof state.checks !== 'object' || state.checks === null) return rows
      for (const key of Object.keys(state.checks)) {
        const entry = state.checks[key]
        if (entry === null || entry === undefined || typeof entry !== 'object') continue
        rows.push({
          key,
          label: CHECK_LABEL[key] || key,
          status: typeof entry.status === 'string' ? entry.status : 'MISSING',
          exit: entry.exit === undefined || entry.exit === null ? '—' : String(entry.exit),
          at: typeof entry.at === 'string' && entry.at.length >= 16 ? entry.at.slice(5, 16).replace('T', ' ') : '—',
        })
      }
      return rows
    }

    function countChecks(rows) {
      const tally = { pass: 0, warn: 0, fail: 0, missing: 0 }
      for (const row of rows) {
        if (row.status === 'PASS') tally.pass += 1
        else if (row.status === 'WARN') tally.warn += 1
        else if (row.status === 'FAIL') tally.fail += 1
        else tally.missing += 1
      }
      return tally
    }

    // ---------- 视图 ----------
    function StageTrack(props) {
      const index = props.index
      return h('div', { style: S.track },
        STAGE_ORDER.map((stage, i) => {
          const done = i < index
          const current = i === index
          const nodeStyle = { ...S.node }
          if (done) {
            nodeStyle.background = 'color-mix(in srgb, var(--dsw-alias-state-success-primary) 16%, var(--dsw-alias-bg-base))'
            nodeStyle.borderColor = 'var(--dsw-alias-state-success-primary)'
            nodeStyle.color = 'var(--dsw-alias-state-success-primary)'
          } else if (current) {
            nodeStyle.background = 'var(--dsw-alias-state-business-primary)'
            nodeStyle.borderColor = 'var(--dsw-alias-state-business-primary)'
            nodeStyle.color = 'var(--dsw-alias-label-on-color)'
          }
          return h('div', { key: stage, style: S.stage },
            h('div', { style: nodeStyle }, done ? '✓' : String(i + 1)),
            h('div', { style: { ...S.stageName, fontWeight: current ? 600 : 400, color: current ? 'var(--dsw-alias-label-primary)' : S.stageName.color } }, stage),
          )
        }),
      )
    }

    /** 当前正在跑的命令的取消控制器（面板是单例，够用）。 */
    let activeController = null
    let copyTimer = null

    /** 复制到剪贴板：优先 Clipboard API，失败退到 execCommand，再失败返回 false。 */
    function copyToClipboard(value) {
      const text = String(value === undefined || value === null ? '' : value)
      try {
        if (typeof navigator !== 'undefined' && navigator !== null
          && navigator.clipboard !== undefined && typeof navigator.clipboard.writeText === 'function') {
          return navigator.clipboard.writeText(text).then(
            () => true,
            () => fallbackCopy(text),
          )
        }
      } catch {
        // 落到降级路径
      }
      return Promise.resolve(fallbackCopy(text))
    }

    function fallbackCopy(text) {
      try {
        if (typeof document === 'undefined' || document === null) return false
        const area = document.createElement('textarea')
        area.value = text
        area.setAttribute('readonly', '')
        area.style.position = 'fixed'
        area.style.opacity = '0'
        document.body.appendChild(area)
        area.select()
        const ok = document.execCommand('copy')
        document.body.removeChild(area)
        return ok === true
      } catch {
        return false
      }
    }

    function stampNow() {
      const d = new Date()
      const pad = (n) => (n < 10 ? '0' + n : String(n))
      return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate())
        + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes())
    }

    /** 命令值里有空格/引号时用双引号包起来（Host 侧解析器支持引号）。 */
    function quoteArg(value) {
      const text = String(value === undefined || value === null ? '' : value).trim()
      if (text === '') return ''
      if (/[\s"']/.test(text)) return '"' + text.replace(/"/g, "'") + '"'
      return text
    }

    /**
     * 面板动作 → 会话命令行（不含 /capability-loop 前缀）。
     * 白名单与参数校验在 Host 半（plugins/capability-loop/actions.js），这里只拼文本。
     */
    function buildAction(key, fields) {
      const f = fields === undefined || fields === null ? {} : fields
      if (key === 'gate') {
        const kind = f.gateKind || 'auto'
        const taskDir = String(f.taskDir || '').trim()
        // 没有 taskDir 时 loop-gate 只会报「没有可执行的门禁」，所以这里不发空命令。
        if (taskDir === '') return null
        const grill = f.grill === true || f.grill === '1' || f.grill === 'true'
        return {
          key,
          label: '运行门禁（' + kind + '）',
          line: 'run gate kind=' + kind + ' taskDir=' + quoteArg(taskDir) + (grill ? ' grill=1' : ''),
          note: '执行 loop-gate.ps1：结果写回 state.json；有 FAIL 时退出码非 0（不会改写结论）。',
        }
      }
      if (key === 'env') return { key, label: '环境验收', line: 'run env', note: '等价 loop-gate -Environment：只跑环境级验收，不需要 taskDir。' }
      if (key === 'audit') return { key, label: '能力体检', line: 'run audit', note: '九组只读体检，报告默认写到 .tmp/（写不进时改用 %TEMP%）。' }
      if (key === 'handoff') {
        const slug = String(f.slug || '').trim()
        if (slug === '') return null
        return { key, label: '交接包体检', line: 'run handoff-audit slug=' + quoteArg(slug), note: '材料可达性 / 证据对账 / 批次 / 网关前缀（exit 1 = 不得交）。' }
      }
      if (key === 'preflight') {
        const keyword = String(f.keyword || '').trim()
        if (keyword === '') return null
        const alias = String(f.alias || '').trim()
        return { key, label: '模块/路由预检', line: 'run preflight keyword=' + quoteArg(keyword) + (alias !== '' ? ' alias=' + quoteArg(alias) : ''), note: 'EXISTS / WEAK 时必须先确认复用还是另建。' }
      }
      if (key === 'pack') {
        const handle = String(f.handle || '').trim()
        if (handle === '') return null
        return { key, label: '上架打包', line: 'run pack handle=' + quoteArg(handle), note: '校验 frontmatter/version/CHANGELOG + manifest + SHA256 + ZIP。' }
      }
      if (key === 'visual') return { key, label: '视觉验收探测', line: 'run visual', note: 'exit 2 = 权限受限，必须显式让用户选 A/B/C。' }
      if (key === 'skill-status') return { key, label: '版本检查', line: 'run skill-status' }
      if (key === 'sync-shadow') return { key, label: '影子计数', line: 'run sync-shadow' }
      return null
    }

    function modeAction(mode) {
      const label = mode === 'on' ? '切到接管（on）' : mode === 'shadow' ? '切到影子（shadow）' : '切到关闭（off）'
      return { key: 'mode', label, line: 'mode ' + mode, note: '写 state.json 的 mode；只影响后续注入，不改历史消息。' }
    }

    /** 面板 → Host 会话命令通道；返回 { ok, text }（永不抛错）。 */
    async function runCommand(ctx, sessionId, line, signal) {
      const remote = ctx !== undefined && ctx !== null ? ctx.get('remote') : undefined
      const commands = remote !== undefined && remote !== null ? remote.commands : undefined
      if (commands === undefined || commands === null || typeof commands.execute !== 'function') {
        return { ok: false, text: '当前 composition 没有 remote.commands，面板无法触发 Host 动作。请确认插件已启用后刷新页面。' }
      }
      let response
      try {
        response = await commands.execute(sessionId, '/capability-loop ' + line, [], signal)
      } catch (error) {
        return { ok: false, text: '命令通道抛错：' + String(error && error.message ? error.message : error) }
      }
      if (response === undefined || response === null || response.ok !== true) {
        const error = response !== undefined && response !== null ? response.error : undefined
        return { ok: false, text: '命令通道失败：' + String(error && error.message ? error.message : '无结果') }
      }
      const value = response.value
      if (value === undefined || value === null) {
        return {
          ok: false,
          text: '命令未被受理（未注册或语法不符）：/capability-loop ' + line
            + '\n提示：Host 半新注册的命令需要重启应用后才会出现。',
        }
      }
      const inner = value.result !== undefined && value.result !== null ? value.result : {}
      const ok = inner.kind === 'success'
      const text = typeof inner.text === 'string' && inner.text !== ''
        ? inner.text
        : (ok ? '完成（无输出）' : '失败（无输出）')
      return { ok, text }
    }

    function ActionCenter(props) {
      const f = props.fields === undefined || props.fields === null ? {} : props.fields
      const disabled = props.sessionId === '' || props.sessionId === undefined
      const set = props.setField
      const labelStyle = props.compact === true ? { ...S.name, width: 72 } : S.name
      const runBtn = (key, label, extra) => h('button', {
        type: 'button',
        style: { ...S.btn, ...(extra !== undefined && extra.primary === true ? S.btnPrimary : {}) },
        disabled: disabled || (extra !== undefined && extra.disabled === true),
        onClick: () => props.onRequest(key),
      }, label)
      const enter = (key, allowed) => (event) => {
        if (event.key !== 'Enter' || disabled || allowed === false) return
        event.preventDefault()
        props.onRequest(key)
      }
      return h('div', { style: S.card },
        h('div', { style: S.cardHd }, '运行中心',
          props.projectName !== undefined ? h('span', { style: S.projectChip }, props.projectName) : null,
          h('span', { style: S.hint },
            disabled ? '没有可用会话：动作需要会话凭据' : '动作 = 会话命令 /capability-loop（确认后运行）')),
        h('div', { style: S.runRow },
          h('span', { style: labelStyle }, '门禁'),
          h('select', {
            style: S.select, value: f.gateKind || 'design', disabled,
            onChange: (event) => set('gateKind', event.target.value),
          }, ['design', 'requirement', 'test', 'all', 'auto'].map((kind) => h('option', { key: kind, value: kind }, kind))),
          h('input', {
            style: S.input, placeholder: 'taskDir（必填，如 docs/design）', disabled,
            value: f.taskDir || '',
            onChange: (event) => set('taskDir', event.target.value),
            onKeyDown: enter('gate', String(f.taskDir || '').trim() !== ''),
          }),
          h('label', {
            style: { display: 'inline-flex', alignItems: 'center', gap: 5, ...S.meta, cursor: 'pointer' },
            title: '把 grill 记录缺失当硬门（-RequireGrill）',
          },
            h('input', {
              type: 'checkbox', checked: f.grill === true, disabled,
              onChange: (event) => set('grill', event.target.checked),
            }),
            '含 grill'),
          runBtn('gate', '运行门禁', {
            primary: true,
            disabled: String(f.taskDir || '').trim() === '',
          }),
          runBtn('env', '环境验收'),
          String(f.taskDir || '').trim() === ''
            ? h('span', { style: { ...S.meta, color: 'var(--dsw-alias-state-warn-primary)' } }, '先填 taskDir（门禁要一个任务目录）')
            : null,
        ),
        h('div', { style: S.runRow },
          h('span', { style: labelStyle }, '交接体检'),
          h('input', {
            style: S.input, placeholder: 'slug（必填）', disabled, value: f.slug || '',
            onChange: (event) => set('slug', event.target.value),
            onKeyDown: enter('handoff', String(f.slug || '').trim() !== ''),
          }),
          runBtn('handoff', '运行', { disabled: String(f.slug || '').trim() === '' }),
          h('span', { style: { ...labelStyle, width: 'auto', marginLeft: 10 } }, '模块预检'),
          h('input', {
            style: S.input, placeholder: 'keyword（必填）', disabled, value: f.keyword || '',
            onChange: (event) => set('keyword', event.target.value),
            onKeyDown: enter('preflight', String(f.keyword || '').trim() !== ''),
          }),
          h('input', {
            style: S.input, placeholder: 'alias（可选，空格分隔）', disabled, value: f.alias || '',
            onChange: (event) => set('alias', event.target.value),
          }),
          runBtn('preflight', '运行', { disabled: String(f.keyword || '').trim() === '' }),
        ),
        h('div', { style: S.runRow },
          h('span', { style: labelStyle }, '上架打包'),
          h('input', {
            style: S.input, placeholder: 'handle（必填）', disabled, value: f.handle || '',
            onChange: (event) => set('handle', event.target.value),
            onKeyDown: enter('pack', String(f.handle || '').trim() !== ''),
          }),
          runBtn('pack', '运行', { disabled: String(f.handle || '').trim() === '' }),
          h('span', { style: { ...labelStyle, width: 'auto', marginLeft: 10 } }, '只读动作'),
          runBtn('audit', '能力体检'),
          runBtn('visual', '视觉探测'),
          runBtn('skill-status', '版本检查'),
          runBtn('sync-shadow', '影子计数'),
        ),
      )
    }

    function RunningPanel(props) {
      if (props.running === null || props.running === undefined) return null
      return h('div', { style: S.card },
        h('div', { style: S.cardHd }, '正在运行：' + props.running.label,
          props.running.projectName !== undefined ? h('span', { style: S.projectChip }, props.running.projectName) : null,
          h('button', {
            type: 'button', style: { ...S.btn, marginLeft: 'auto' }, onClick: props.onCancelRun,
          }, '取消')),
        h('div', { style: { ...S.row, ...S.meta, borderTop: 'none' } }, props.running.line),
      )
    }

    function ResultPanel(props) {
      const result = props.result
      if (result === null || result === undefined) return null
      const label = (key, idle) => (props.copied === key ? '已复制' : (props.copied === key + ':fail' ? '复制失败' : idle))
      const copyBtn = (key, idle, text) => h('button', {
        type: 'button',
        style: { ...S.btn, fontSize: 11, padding: '3px 8px', marginLeft: 6 },
        onClick: () => props.onCopy(key, text),
      }, label(key, idle))
      return h('div', { style: S.card },
        h('div', { style: S.cardHd }, '最近一次运行',
          h(Badge, { status: result.ok ? 'PASS' : 'FAIL' }),
          result.projectName !== undefined ? h('span', { style: S.projectChip }, result.projectName) : null,
          h('span', { style: S.hint },
            result.label + ' · ' + result.at + (typeof result.elapsed === 'number' ? ' · ' + result.elapsed + 's' : '')),
          copyBtn('result-output', '复制输出', result.text),
          copyBtn('result-cmd', '复制命令', '/capability-loop ' + result.line),
        ),
        h('div', { style: { padding: '0 14px 8px', ...S.meta } }, result.line),
        h('pre', { style: S.pre }, result.text),
      )
    }

    function ConfirmModal(props) {
      const pending = props.pending
      if (pending === null || pending === undefined) return null
      const command = '/capability-loop ' + pending.line
      const copyLabel = props.copied === 'pending-cmd' ? '已复制' : (props.copied === 'pending-cmd:fail' ? '复制失败' : '复制命令')
      return h('div', { style: S.overlay }, h('div', {
        style: S.modal, role: 'dialog', 'aria-modal': true,
        'aria-labelledby': 'cl-confirm-title',
        'data-cl-modal': '1',
      },
        h('div', { style: S.modalBar }),
        h('h3', { id: 'cl-confirm-title', style: S.modalHd }, '确认运行：' + pending.label),
        h('div', { style: S.modalBody },
          h('div', null, '工程：' + (pending.projectName !== undefined ? pending.projectName + '（' + pending.workspace + '）' : pending.workspace)),
          h('div', { style: { marginTop: 10 } }, '命令：'),
          h('code', {
            style: {
              ...S.mono, display: 'block', marginTop: 4, padding: '10px 12px',
              background: 'linear-gradient(var(--dsw-alias-bg-layer-1), var(--dsw-alias-bg-layer-1)), var(--dsw-static-neutral-bluish-900)',
              borderRadius: 6, whiteSpace: 'pre-wrap',
              border: '1px solid var(--dsw-alias-border-l2)', color: 'var(--dsw-alias-label-primary)',
            },
          }, command),
          h('div', { style: { display: 'flex', justifyContent: 'flex-end', marginTop: 8 } },
            h('button', {
              type: 'button', style: { ...S.btn, fontSize: 11, padding: '4px 10px' },
              onClick: () => props.onCopy('pending-cmd', command),
            }, copyLabel)),
          pending.note !== undefined ? h('div', { style: { marginTop: 10 } }, pending.note) : null,
        ),
        h('div', { style: { ...S.modalFt, borderTop: '1px solid var(--dsw-alias-border-l1)', paddingTop: 14 } },
          h('button', {
            type: 'button', style: { ...S.btn, minWidth: 88, padding: '8px 14px' }, onClick: props.onCancel,
          }, '取消'),
          h('button', {
            type: 'button', 'data-cl-primary': '1',
            style: { ...S.btn, ...S.btnPrimary, minWidth: 96, padding: '8px 14px' }, onClick: props.onConfirm,
          }, '确认运行'),
        ),
      ))
    }

    function ProjectView(props) {
      const project = props.project
      const state = props.state
      const info = stageIndexOf(state)
      const checks = checksOf(state)
      const tally = countChecks(checks)
      const mode = state !== null && state !== undefined && typeof state.mode === 'string'
        ? state.mode
        : (project !== null && project !== undefined && typeof project.mode === 'string' ? project.mode : 'off')
      const name = project !== null && project !== undefined && typeof project.name === 'string' ? project.name : '未命名工程'
      const blockers = state !== null && state !== undefined && Array.isArray(state.blockers) ? state.blockers : []
      const next = state !== null && state !== undefined && state.next !== undefined && state.next !== null ? state.next : undefined
      const version = state !== null && state !== undefined && typeof state.skillVersion === 'string' ? state.skillVersion : '—'
      const shadow = state !== null && state !== undefined && state.shadow !== undefined && state.shadow !== null ? state.shadow : undefined
      const modeText = mode === 'on' ? '接管' : mode === 'shadow' ? '影子' : '关闭'
      const modeMeta = mode === 'shadow'
        ? (shadow !== undefined ? '已观察 ' + shadow.sessions + ' / ' + shadow.target + ' 个会话' : '只记录，不阻断')
        : mode === 'on' ? '完整契约随首步注入' : '不注入'
      const updated = state !== null && state !== undefined && typeof state.updatedAt === 'string' ? state.updatedAt.slice(0, 16).replace('T', ' ') : '未记录'

      const kpis = [
        { k: '档位', v: modeText, m: modeMeta, id: 'mode' },
        { k: '当前阶段', v: info.stage, m: '第 ' + (info.index + 1) + ' / 7 阶段', id: 'stage' },
        { k: '门禁', v: tally.pass + ' / ' + checks.length + ' 通过', m: tally.warn + ' WARN · ' + tally.fail + ' FAIL · ' + tally.missing + ' 未运行', id: 'gate' },
        { k: '阻断', v: String(blockers.length) + ' 项', m: blockers.length > 0
          ? blockers.slice(0, 1).map((b) => b.id + ' ' + b.text).join('') + (blockers.length > 1 ? ' 等 ' + blockers.length + ' 项' : '')
          : '无阻断', id: 'blocker' },
      ]

      return h('div', null,
        h('div', null,
          h('div', { style: S.head },
            h('div', { style: { flex: 1, minWidth: 0 } },
              h('h1', { style: S.h1 }, '能力闭环'),
              h('p', { style: S.sub },
                h('span', null, name),
                h('span', { style: S.dotsep }, '·'),
                h('span', null, 'skill v' + version),
                h('span', { style: S.dotsep }, '·'),
                h('span', null, '面板 v' + PANEL_VERSION),
                h('span', { style: S.dotsep }, '·'),
                h('span', null, '更新于 ' + updated),
                h('span', { style: S.dotsep }, '·'),
                h('span', null, '状态只读 · 动作走会话命令'),
              ),
            ),
            h('div', { style: { display: 'flex', gap: 8, alignItems: 'center', flex: 'none' } },
              h('div', { style: S.seg },
                [['on', '接管'], ['shadow', '影子'], ['off', '关闭']].map((pair) => h('button', {
                  key: pair[0], type: 'button',
                  disabled: pair[0] === mode,
                  title: pair[0] === mode ? '当前档位' : '切换到 ' + pair[0],
                  style: pair[0] === mode ? { ...S.segItem, ...S.segOn } : S.segItem,
                  onClick: () => { if (pair[0] !== mode) props.onRequest('mode', pair[0]) },
                }, pair[1]))),
              props.onRefresh ? h('button', { style: S.btn, onClick: props.onRefresh, type: 'button' }, '刷新') : null,
            ),
          ),
          h('div', { style: S.projectBar },
            h('span', { style: S.projectTag }, '工程'),
            h('select', {
              style: S.select,
              value: String(props.selectedIndex === undefined ? 0 : props.selectedIndex),
              disabled: !Array.isArray(props.projects) || props.projects.length <= 1,
              title: '切换工程会重新读取该工程的状态',
              onChange: (event) => { if (props.onSelect) props.onSelect(Number(event.target.value)) },
            }, (Array.isArray(props.projects) ? props.projects : []).map((item, i) =>
              h('option', { key: item.workspace.id, value: String(i) }, item.workspace.title))),
            h('span', { style: S.projectPath }, props.workspace.path),
            h('span', { style: S.hint },
              Array.isArray(props.projects) && props.projects.length > 1
                ? '已接入工程 ' + props.projects.length + ' 个 · 切换后重读该工程状态'
                : '只列已接入工程；未接入的跑 init 后出现'),
          ),
          h('div', { style: props.compact === true ? S.kpisCompact : S.kpis },
            kpis.map((kpi) => h('div', { key: kpi.id, style: S.kpi },
              h('span', { style: S.kpiK }, kpi.k),
              h('span', { style: S.kpiV }, kpi.v),
              h('span', { style: S.kpiM }, kpi.m),
            )),
          ),
          h(ActionCenter, {
            fields: props.fields,
            setField: props.setField,
            sessionId: props.sessionId,
            projectName: name,
            compact: props.compact === true,
            onRequest: props.onRequest,
          }),
        ),
        h('div', { style: S.card },
          h('div', { style: S.cardHd }, '阶段', h('span', { style: S.projectChip }, name), h('span', { style: S.hint }, '七阶段闭环')),
          h(StageTrack, { index: info.index }),
        ),
        h('div', { style: S.card },
          h('div', { style: S.cardHd }, '门禁与证据', h('span', { style: S.projectChip }, name), h('span', { style: S.hint }, '点击行展开命令与退出码')),
          checks.length === 0
            ? h('div', { style: { ...S.row, ...S.meta } }, '还没有门禁记录：跑一次 loop-gate.ps1 就会出现在这里。')
            : checks.map((row) => h('div', { key: row.key, style: S.row },
              h('span', { style: S.name }, row.label),
              h(Badge, { status: row.status }),
              h('span', { style: S.meta }, 'exit ' + row.exit),
              h('span', { style: S.right }, row.at),
            )),
        ),
        h('div', { style: S.card },
          h('div', { style: S.cardHd }, '阻断与下一步', h('span', { style: S.projectChip }, name), h('span', { style: S.hint }, blockers.length + ' 项阻断')),
          blockers.length === 0
            ? h('div', { style: { ...S.row, ...S.meta } }, '无阻断')
            : blockers.map((b, i) => h('div', { key: (b.id || 'b') + i, style: S.row },
              h('span', { style: S.badge }, b.id || 'D-?'),
              h('span', { style: { flex: 1, minWidth: 0, overflowWrap: 'anywhere', color: 'var(--dsw-alias-label-primary)' } }, b.text || ''),
              h('span', { style: { ...S.right, flex: 'none' } }, (b.owner || '') + (b.due ? ' · ' + b.due : '')),
            )),
          next !== undefined
            ? h('div', { style: { ...S.row, alignItems: 'flex-start' } },
              h('span', { style: S.name }, '下一步'),
              h('span', { style: { flex: 1, color: 'var(--dsw-alias-label-primary)' } }, String(next.label || '按 state.next 执行')),
            )
            : null,
          next !== undefined && next.command
            ? h('div', { style: { padding: '0 14px 12px' } }, h('code', { style: S.mono }, String(next.command)))
            : null,
        ),
        h('div', { style: { ...S.meta, marginTop: 12 } },
          '状态源：' + joinPath(props.workspace.path, '.dsh/loop/state.json'),
        ),
      )
    }

    function EmptyView(props) {
      return h('div', { style: S.empty },
        h('div', { style: { fontSize: 16, fontWeight: 600 } }, '还没有已接入的工程'),
        h('div', { style: { ...S.meta, maxWidth: 520, lineHeight: 1.6 } },
          '在任意工程根跑一次接入命令，这里就会显示档位、阶段、门禁与阻断：'),
        h('code', { style: { ...S.mono, background: 'var(--dsw-alias-bg-layer-2)', padding: '8px 10px', borderRadius: 6 } },
          'loop-state.ps1 -Action init -Root <工程根> -ProjectName <名称>'),
        h('div', { style: { ...S.meta, marginTop: 4 } },
          '读取诊断：' + (props.diagnostic === '' ? '未发生错误（只是没找到已标记工程）' : props.diagnostic)),
        props.onRefresh ? h('button', { style: S.btn, onClick: props.onRefresh, type: 'button' }, '重新扫描') : null,
      )
    }

    /** 轻量记忆：刷新后回到上次看的工程 / 上次的 taskDir（存不了就只影响体验）。 */
    const STORE_KEY = 'dsh-capability-loop:panel:v1'
    function readStore(name, fallback) {
      try {
        if (typeof localStorage === 'undefined' || localStorage === null) return fallback
        const raw = localStorage.getItem(STORE_KEY)
        if (raw === null || raw === '') return fallback
        const data = JSON.parse(raw)
        return data !== null && typeof data === 'object' && data[name] !== undefined ? data[name] : fallback
      } catch {
        return fallback
      }
    }
    function writeStore(name, value) {
      try {
        if (typeof localStorage === 'undefined' || localStorage === null) return
        const raw = localStorage.getItem(STORE_KEY)
        const data = raw !== null && raw !== '' ? JSON.parse(raw) : {}
        data[name] = value
        localStorage.setItem(STORE_KEY, JSON.stringify(data))
      } catch {
        // 隐私模式/禁用存储时静默降级
      }
    }

    function CapabilityLoopPage(props) {
      // ctx 由 apply() 注入（不猜 slot props 的形状）；props 仅作为兜底。
      const slot = props === undefined || props === null ? {} : props
      const services = pluginCtx !== undefined && pluginCtx !== null
        ? pluginCtx
        : (slot.hookContext !== undefined && slot.hookContext !== null && slot.hookContext.ctx !== undefined
          ? slot.hookContext.ctx
          : slot.ctx)
      const [view, setView] = React.useState({ status: 'loading', projects: [], error: null })
      const [selectedPath, setSelectedPath] = React.useState(() => String(readStore('projectPath', '') || ''))
      const [fields, setFields] = React.useState(() => ({
        gateKind: 'design',
        taskDir: String(readStore(selectedPath !== '' ? 'taskDir:' + selectedPath : 'taskDir', '') || ''),
        slug: '',
        keyword: '',
        alias: '',
        handle: '',
        grill: false,
      }))
      const [pending, setPending] = React.useState(null)
      const [running, setRunning] = React.useState(null)
      const [result, setResult] = React.useState(null)
      const [copied, setCopied] = React.useState(null)
      const [viewport, setViewport] = React.useState(() => (typeof window !== 'undefined' && typeof window.innerWidth === 'number' ? window.innerWidth : 1024))
      const pageStyle = viewport < 820 ? { ...S.page, padding: '18px 16px 32px' } : S.page
      const load = React.useCallback(() => {
        setView((prev) => ({ ...prev, status: 'loading' }))
        const source = services
        if (source === undefined) {
          setView({ status: 'error', projects: [], error: 'no context' })
          return
        }
        collectAny(source).then(
          (data) => setView({ status: 'ready', projects: data.projects, error: null }),
          (error) => setView({ status: 'error', projects: [], error: String(error && error.message ? error.message : error), }),
        )
      }, [services])
      React.useEffect(() => { load() }, [load])

      // 窄窗口（<820px）用紧凑排版：KPI 2 列、标签变窄、工程条换行
      React.useEffect(() => {
        if (typeof window === 'undefined' || typeof window.addEventListener !== 'function') return undefined
        const onResize = () => setViewport(typeof window.innerWidth === 'number' ? window.innerWidth : 1024)
        window.addEventListener('resize', onResize)
        return () => window.removeEventListener('resize', onResize)
      }, [])

      // 确认框：ESC 关闭 + Tab 焦点陷阱 + 打开时把焦点放到「确认运行」
      React.useEffect(() => {
        if (pending === null || pending === undefined || typeof document === 'undefined') return undefined
        const onKeyDown = (event) => {
          if (event.key === 'Escape') {
            event.preventDefault()
            setPending(null)
            return
          }
          if (event.key !== 'Tab') return
          const modal = document.querySelector('[data-cl-modal="1"]')
          if (modal === null) return
          const focusables = modal.querySelectorAll('button, input, select, textarea, [tabindex]:not([tabindex="-1"])')
          if (focusables.length === 0) return
          const first = focusables[0]
          const last = focusables[focusables.length - 1]
          if (event.shiftKey && document.activeElement === first) {
            event.preventDefault()
            last.focus()
          } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault()
            first.focus()
          }
        }
        document.addEventListener('keydown', onKeyDown, true)
        const modal = document.querySelector('[data-cl-modal="1"]')
        if (modal !== null) {
          const primary = modal.querySelector('[data-cl-primary="1"]')
          if (primary !== null && typeof primary.focus === 'function') primary.focus()
        }
        return () => document.removeEventListener('keydown', onKeyDown, true)
      }, [pending])

      const markCopied = (key, ok) => {
        setCopied(ok === true ? key : key + ':fail')
        try {
          if (typeof setTimeout === 'function') {
            if (copyTimer !== null) clearTimeout(copyTimer)
            copyTimer = setTimeout(() => setCopied(null), 1500)
          }
        } catch {
          // 没有定时器就保持状态，不影响功能
        }
      }
      const copyAndMark = (key, text) => {
        copyToClipboard(text).then((ok) => markCopied(key, ok), () => markCopied(key, false))
      }

      // 选中的工程按**路径**记，不按索引——刷新/动作后工程顺序可能变，索引会指错。
      const foundIndex = view.projects.findIndex((item) => item.workspace.path === selectedPath)
      const currentIndex = foundIndex >= 0 ? foundIndex : 0
      const current = view.projects.length > 0 ? view.projects[currentIndex] : undefined
      const sessionId = current !== undefined && current.workspace !== undefined && typeof current.workspace.sessionId === 'string'
        ? current.workspace.sessionId
        : ''
      const setField = (name, value) => {
        setFields((prev) => {
          const next = { ...prev }
          next[name] = value
          return next
        })
        if (name === 'taskDir') {
          // 每个工程记自己的 taskDir，切换工程时不会把 A 的目录带到 B
          writeStore('taskDir:' + (current !== undefined ? current.workspace.path : ''), value)
        }
      }
      const requestAction = (key, mode) => {
        if (current === undefined) return
        const request = key === 'mode' ? modeAction(mode) : buildAction(key, fields)
        if (request === null) return
        if (sessionId === '') {
          setResult({
            label: request.label, line: request.line, ok: false, at: stampNow(),
            projectName: current.workspace.title,
            text: '当前工程没有可用会话，动作需要会话凭据。',
          })
          return
        }
        setPending({
          ...request,
          workspace: current.workspace.path,
          projectName: current.workspace.title,
          sessionId,
        })
      }
      const confirmPending = () => {
        const job = pending
        if (job === null || job === undefined) return
        setPending(null)
        const controller = new AbortController()
        activeController = controller
        const started = Date.now()
        setRunning({ label: job.label, line: job.line, projectName: job.projectName })
        const settle = (outcome) => {
          // 已被取消：不要再覆盖「已取消」结果
          if (activeController !== controller) return
          activeController = null
          setRunning(null)
          setResult({
            label: job.label, line: job.line, ok: outcome.ok, text: outcome.text,
            at: stampNow(), elapsed: Math.round((Date.now() - started) / 100) / 10,
            projectName: job.projectName,
          })
          load()
        }
        runCommand(services, job.sessionId, job.line, controller.signal).then(settle, (error) => {
          settle({ ok: false, text: '调用失败：' + String(error && error.message ? error.message : error) })
        })
      }
      const cancelRun = () => {
        const controller = activeController
        activeController = null
        if (controller !== null) controller.abort()
        setRunning(null)
        setResult((prev) => ({
          label: prev !== null && prev !== undefined ? prev.label : '运行',
          line: prev !== null && prev !== undefined ? prev.line : '',
          ok: false, text: '已取消。', at: stampNow(),
          projectName: prev !== null && prev !== undefined ? prev.projectName : undefined,
        }))
      }

      if (view.status === 'loading' && view.projects.length === 0) {
        return h('div', { style: pageStyle }, h('div', { style: S.inner },
          h('h1', { style: S.h1 }, '能力闭环'),
          h('p', { style: S.sub }, h('span', null, '读取状态中…')),
        ))
      }
      if (view.status === 'error') {
        return h('div', { style: pageStyle }, h('div', { style: S.inner },
          h('h1', { style: S.h1 }, '能力闭环'),
          h('p', { style: S.sub }, h('span', null, '读取失败：' + view.error)),
          h('button', { style: S.btn, onClick: load, type: 'button' }, '重试'),
        ))
      }
      if (view.projects.length === 0) {
        return h('div', { style: pageStyle }, h('div', { style: S.inner }, h(EmptyView, { onRefresh: load, diagnostic: lastDiagnostic })))
      }
      return h('div', { style: pageStyle }, h('div', { style: S.inner },
        h(ProjectView, {
          project: current.project,
          state: current.state,
          workspace: current.workspace,
          onRefresh: load,
          fields,
          setField,
          sessionId,
          onRequest: requestAction,
          projects: view.projects,
          selectedIndex: currentIndex,
          compact: viewport < 820,
          onSelect: (index) => {
            const picked = view.projects[index]
            const path = picked !== undefined && picked.workspace !== undefined ? picked.workspace.path : ''
            setSelectedPath(path)
            if (path !== '') writeStore('projectPath', path)
            setFields((prev) => ({
              ...prev,
              taskDir: String(readStore(path !== '' ? 'taskDir:' + path : 'taskDir', '') || ''),
            }))
            load()
          },
        }),
        h(RunningPanel, { running, onCancelRun: cancelRun }),
        h(ResultPanel, { result, copied, onCopy: copyAndMark }),
      ),
      h(ConfirmModal, {
        pending,
        copied,
        onCopy: copyAndMark,
        onCancel: () => setPending(null),
        onConfirm: confirmPending,
      }),
      )
    }

    function PanelIcon(props) {
      const size = props !== undefined && props !== null && typeof props.size === 'number' ? props.size : 16
      return h('svg', { width: size, height: size, viewBox: '0 0 24 24', fill: 'none', 'aria-hidden': true },
        h('path', { d: 'M20 12a8 8 0 0 1-13.66 5.66', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round' }),
        h('path', { d: 'M4 12a8 8 0 0 1 13.66-5.66', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round' }),
        h('path', { d: 'M17.66 3.6v2.74h-2.74', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' }),
        h('path', { d: 'M6.34 20.4v-2.74h2.74', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' }),
        h('circle', { cx: 12, cy: 12, r: 2.2, fill: 'currentColor' }),
      )
    }

    return {
      inject: ['slots', 'connection', 'remote', 'remote.session', 'remote.workspaceFiles', 'remote.commands'],
      apply(ctx) {
        pluginCtx = ctx
        ctx.slots.inject('main', () => ctx.slots.register({
          name: 'main',
          key: PANEL_ID,
        }, CapabilityLoopPage))
        ctx.slots.inject('sidebar.panellist', () => ctx.slots.register({
          name: 'sidebar.panellist',
          id: PANEL_ID,
          order: 20,
          label: () => '能力闭环',
        }, PanelIcon))
      },
    }
  },
})
