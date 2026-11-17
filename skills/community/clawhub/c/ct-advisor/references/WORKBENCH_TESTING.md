# ct-advisor 工作台 · 前端测试标准流程（Standard Process）

> ⚠️ **已迁移至统一测试框架**：本文件保留作为历史参考。当前 ct-advisor 的工作台测试已纳入 CT 系列统一的 `ctqa` 框架（位于 `ct-base/testing/ctqa/`），通过 `ctqa.config.json` 的 `legacy` 字段桥接原有套件。统一入口：`python -m ctqa run --skill ct-advisor`。规范详见 `ct-base/references/workbench_ui.md` §23。
>
> 本文件是 `workbench/` 前端（含 `index.html` / `ct-advisor-proxy.py` / `wb-list.*`）的**历史回归流程**。
> 配套测试代码仍保留在 `workbench/tests/` 作为 legacy 桥接；实操速查见 `workbench/tests/README.md`（中文）。
>
> This is the **legacy regression process** for the ct-advisor workbench frontend, now superseded by the unified ctqa framework.

---

## 0. 一句话定位

> 工作台前端改动 **不可裸奔上线**。改之前先有绿基线，改之后必须全量跑通 `tests/run_all.py`，
> P0/P1 失败即**门禁红灯**，修复后必须回到绿灯 + `verify_fixes.py` 对照，才能发布。

This is the regression net that caught 6 real defects (P0×3 / P1×2 / P2×1) in one pass — including a
`loadLang` operator-precedence trap that silently reverted language choice on every refresh, and an
`esc()` that failed to escape `>` (HTML-injection surface). Both would have shipped unnoticed without E2E behavior tests.

---

## 1. 适用范围（Scope）

| 受控文件 | 说明 |
|---|---|
| `workbench/index.html` | 主工作台页面（v1.3.26+），测试主目标 |
| `workbench/ct-advisor-proxy.py` | 本地代理 / 后端契约实现 |
| `workbench/wb-list.js` / `wb-list.css` | 列表组件 |
| `workbench/tokens.css` | 设计令牌（ct-base 规范） |

**触发**：上述任一文件的内容改动（含 CSS 令牌化、i18n 字典增删、事件绑定、fetch 契约）。

**不归本流程管**：`scripts/`（Python 管线，属 `entry.py` 链，有独立的 `test_*` 套件）、Coze 云端逻辑。

> 历史快照 `WorkBuddy/<date>*/ct-advisor-workspace.html`（legacy 版）与 `workbench/index.html` 同源，
> 共享同一族根因缺陷。触碰 legacy 文件时，至少手工核对本文档 §12 列出的根因点。

---

## 2. 标准流程（The Loop）

```
┌──────────────────────────────────────────────────────────────────┐
│ ① 基线确认  改前先跑 run_all.py，确认当前是绿灯（无历史红灯残留）  │
│ ② 小步改动  优先最小化根因修复，不夹带无关重构                     │
│ ③ 全量测试  python tests/run_all.py  →  退出码 0 = 绿            │
│ ④ 门禁判定  P0/P1 失败 ⇒ 红灯，禁止发布；P2/P3 可延后但须记录     │
│ ⑤ 修复回归  逐项定位 file:line → 修复 → 重跑，直到全绿           │
│ ⑥ 修复验收  P0/P1 修复须跑 verify_fixes.py 做前后对照            │
│ ⑦ 发布门禁  仅当全绿 + 验收通过，才允许 run_app.bat / publish-kit │
└──────────────────────────────────────────────────────────────────┘
```

**铁律**：绝不允许"标记已修复但没有重跑绿灯"——未重跑的修复视为未修复。

---

## 3. 命令速查（Commands）

```bash
# 全量（约 40–50s，含 L0–L5 八层）
C:/Tools/anaconda3/python.exe workbench/tests/run_all.py

# 只跑某几层（调试用）
C:/Tools/anaconda3/python.exe workbench/tests/run_all.py --layer L0 L1
C:/Tools/anaconda3/python.exe workbench/tests/run_all.py --layer L4V      # 只测响应式/无障碍

# 显示浏览器（排查交互问题时）
C:/Tools/anaconda3/python.exe workbench/tests/run_all.py --head

# 修复验收：修复前(备份 .bak) / 修复后 同一会话对照
C:/Tools/anaconda3/python.exe workbench/tests/verify_fixes.py
```

产出：
- `workbench/tests/reports/report.html` — 可视化报告（分层用例、严重度、修复建议）
- `workbench/tests/reports/report.json` — 机器可读，可接 CI
- 退出码：`0` 全绿 / `1` 有失败

---

## 4. 测试分层一览（L0–L5）

| 层 | 名称 | 手段 | 覆盖 |
|---|---|---|---|
| **L0** | 静态结构与契约 | 纯文本分析 | 资源引用、id 唯一性、inline 处理器引用的函数是否存在、转义表完整性、硬编码密钥、config↔DOM 一致性 |
| **L1** | 纯逻辑单元 | 浏览器内调真实函数 | `esc` / `md2html` / `detectVague` / `cliCmd` / `normalizeCozeMessage` / `extractAnswer` / `getQid` / i18n 键对齐 |
| **L2** | DOM 交互 | Playwright 真实点击 | 三视图切换、语言切换**跨刷新持久化**、侧栏折叠、历史展开/再问/删除/导入导出、字符计数、Enter 发送、toast |
| **L3** | 端到端集成 | 真实 HTTP + mock 后端 | 正常问答、need_tool、HTTP 500/524、缺 task_id、空答案、连续对话开关、附件 file_id、docx 导出、bug 上报、澄清循环 |
| **L4S** | 安全 | XSS 注入矩阵 | 6 类 payload（img onerror / script / svg onload / iframe / 属性逃逸 / js 链接）、历史导入污染 |
| **L4R** | 健壮性 | 脏数据与故障注入 | localStorage 全毁、非法 lang、旧版 qid、400 条历史、断网、空白输入 |
| **L4V** | 响应式与无障碍 | 5 档视口 | 320/375/768/1024/1440 无横向滚动、移动端点击区 ≥44px、按钮可访问名称 |
| **L5** | 性能 | 计时断言 | 首屏 DCL、可用时间、全量重渲染、md 缓存、节点泄漏 |

---

## 5. Mock 后端契约（Mock Server）

`workbench/tests/mock_server.py` 实现前端依赖的**全部** API 契约，并提供统一故障注入通道
`POST /__mode?m=<mode>`：

`ok` / `http500` / `async_500` / `poll_500` / `http404` / `nojid` / `badjson` / `slow` /
`netdown` / `health_down` / `clarify_need` / `skill_fail` / `upload_fail` / `bug_fail` / `export_fail`

好处：
- **离线可跑**，不消耗真实 Coze 额度，不受网络抖动影响
- **异常分支可达** —— Cloudflare 524、task 缺 id 这类边缘故障真实后端难稳定复现
- **请求可审计** —— 每个请求落 `tests/__requests.jsonl`，断言"头是否带齐 / 是否重试 2 次 / 是否携带前文"

---

## 6. 严重度与门禁（Severity & Gate）

- **P0**：崩溃 / 安全漏洞 / 核心功能不可用（语言钮失效、XSS 可执行）→ **红灯阻断**
- **P1**：功能异常但有绕路，或违反 ct-base 规范（移动端点击区过小）→ **红灯阻断**
- **P2**：体验问题、次要路径 → 可延后，须入 CHANGELOG
- **P3**：清洁度（console.log 残留等）→ 可延后

**门禁规则**：P0/P1 任一失败 = 发布红灯。只有全绿（fail=0）方可进入发布流程。

---

## 7. 修复-回归闭环（关键纪律）

1. 从 `report.json` / 终端失败清单取 `file:line`，**先读真实代码**定位根因，不盲改。
2. 修复后**必须重跑整层或全量**，确认该项变绿且**无新回归**。
3. 同一文件多处改动、或多文件并行编辑后，**逐文件 grep 关键新文本复核**（Edit 可能"假成功"只落盘一处）。
4. 绝不"凭推理宣布修好"——未重跑绿灯的修复 = 未修复。

---

## 8. 修复验收（verify_fixes.py）

针对 P0/P1 修复，`verify_fixes.py` 把 `index.html.bak-*` 备份挂到测试服务器，与修复后的版本在
**同一浏览器会话**里并排求值，输出每项"修复前 / 修复后 / 级别 / 性质"。

**前置**：必须保留 `index.html.bak-*`（见 §9）。删除即失去对照能力。

---

## 9. 文件保管红线（Custody）

- 🔴 **永不删除 `workbench/index.html.bak-*` ** —— `verify_fixes.py` 依赖它做前后对照。
- 🔴 **测试运行中途不删 `workbench/tests/__requests.jsonl`** —— 审计断言依赖它。
- ✅ `workbench/tests/reports/` 可提交（HTML + JSON），便于 CI 留存与回溯。
- ✅ mock server 的故障注入是**临时态**，一次 `run_all.py` 生命周期内有效，不影响真实后端。

---

## 10. 发布门禁（Publish Gate）

仅当满足以下条件，才允许：
- `run_app.bat` 重启工作台（本地预览）
- `publish-kit/build_publish.py` 出包 / 覆盖发布到 `https://ct-advisor.app.workbuddy.host/`

发布前置 = **全绿（fail=0）+ P0/P1 修复经 verify_fixes 对照通过**。
未达标发布 = 违规（与"绝不自动推送"同源的红线意识）。

---

## 11. 已知坑（写/维护用例必读，避免重蹈）

1. **`state` 是 `let` 声明**，不挂 `window`。等待就绪须写 `typeof state !== 'undefined' && state`，
   写 `window.state` 恒 undefined、`wait_for_function` 必超时。
2. **`page.add_init_script` 必须是可执行语句**，包一层 `() => {...}` 只定义了函数、**不会调用**，
   会让整组脏数据用例"假通过"（健壮性用例曾在没有注入任何脏数据时显示绿色）。
3. **等待发送完成不能用"存在 bot 气泡"** —— 历史里本来就有 bot 消息，会在请求真正发出前就为真。
   正确做法：先等 `sendBtn` 进入 `disabled/loading`，再等它解除。
4. **`#contChk` 原生 checkbox 被 CSS `display:none`**，Playwright 点不到，需 `evaluate` 改 `.checked`。
5. **`a || b ? c : d` 运算符优先级陷阱，纯文本正则无法可靠识别**（多种形态会被误判）。
   L0 只把它作 **warn 线索**，真正拦截靠 L2 行为测试（"切成英文 → 刷新 → 仍是英文"）。
   **行为断言 > 静态启发式**。

---

## 12. 本流程已固化的根因清单（回归必查点）

改动下列逻辑时，先确认对应测试点仍绿：

| 根因 | 现象 | 守门测试 |
|---|---|---|
| `esc()` 漏转义 `>` | HTML 转义不完整（注入面） | L1 `esc` 用例 |
| `loadLang()` 的 `a \|\| b ? c : d` 优先级 | 切英文刷新回中文 | L2 语言跨刷新持久化 |
| `loadLang()` 取值无白名单 | 脏 lang 值令整页初始化崩溃 | L4R 非法 lang 注入 |
| `seedSamples()` 未置脏位 | 示例历史不落盘、刷新消失 | L2 历史持久化 |
| Markdown 引用块正则依赖未转义 `>` | 修 esc 后引用渲染失效（隐性回归） | L1 `md2html` 引用块 |
| `sendConsole()` 缺 `const T=t()` | 长输入提示静默失效 | L2 字符计数/提示 |

---

## 13. 记录要求（Record-keeping）

- 每轮实质性前端改动，在 `CHANGELOG.md` 加一条（日期 · 版本 · 主题 + 测试结论：
  "全量 X 通过 / 0 失败 / verify_fixes 对照通过"）。
- 复现的共性坑写入 `.learnings/ERRORS.md`（遵循 self-improving-agent 格式）。
- 测试套件本身若有新增缺陷防护，须同步更新 `tests/README.md` 与本文档 §4/§12。
