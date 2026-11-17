---
name: ai-browser-automation
description: 视觉驱动的浏览器自动化：自然语言操作页面、抓取数据、断言 UI，无需选择器
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/ai-browser-automation/SKILL.md
  version: 1.0.0
  updated: 2026-09-02
  url: https://skills.sh/web-infra-dev/midscene-skills/browser-automation
metadata:
  category: 工具
  platform: Web
  difficulty: 入门
---

# 视觉驱动浏览器自动化（Midscene）

> 用 `npx -y @midscene/web@1` 驱动浏览器：**基于截图做视觉理解**，不依赖 DOM 选择器或无障碍标签。
> 用自然语言描述"要做什么"，由模型定位元素并执行点击/输入/滚动/拖拽等多步交互。

## 与同类技能的分工（先选对工具）

| 场景 | 用哪个 |
|------|--------|
| 页面结构稳定、要写可复现调试脚本、跑 Lighthouse | [skills/browser-devtools](../../skills/browser-devtools/SKILL.md)（CDP + 无障碍快照 ref） |
| 要写进 CI 的正式 E2E 断言用例 | `software-tester` 的 `e2e-testing`（Playwright 选择器） |
| **选择器不稳定 / 只有截图 / 想用自然语言描述意图 / Canvas 与富交互页面** | **本技能（视觉驱动）** |

## 四条铁律（违反会破坏工作流）

1. **绝不后台运行** midscene 命令——必须同步执行，读到截图后再决定下一步；后台执行会打断「截图→分析→动作」闭环。
2. **一次只跑一条命令**，等上一条结束、看过截图再发下一条，不要串联。
3. **留足超时**：命令内含 AI 推理，典型约 1 分钟，复杂 `act` 更久。
4. **结束前必须汇报**：主动总结抓到的数据、完成的动作、截图路径与结论，不要静默收尾。

## 前置条件：模型环境变量

Midscene 需要**具备视觉定位能力**的模型。写入系统环境变量或当前目录 `.env`（自动加载）：

```bash
MIDSCENE_MODEL_API_KEY="your-api-key"
MIDSCENE_MODEL_NAME="model-name"
MIDSCENE_MODEL_BASE_URL="https://..."
MIDSCENE_MODEL_FAMILY="family-identifier"
```

常用可选模型：Doubao Seed 2.0 Lite、Qwen 3.5、智谱 GLM-4.6V、Gemini-3-Pro/Flash。未配置时先让用户补齐，不要硬跑。

## 三种连接模式

| 模式 | 何时用 | 行为 |
|------|--------|------|
| **Puppeteer（默认）** | 只是打开某个 URL、抓数据、验 UI，不需要用户自己的浏览器 | 新起无头 Chrome，与用户浏览器隔离；**跨 CLI 调用保持会话** |
| **CDP** | 用户说"连我的 Chrome""控制我的浏览器"，或任务**隐含登录态**（"看我的订单""打开我的后台"） | 走 DevTools 协议接管已开浏览器；需在 `chrome://inspect` 开启 "Allow remote debugging" |
| **Bridge** | 用户明确提"bridge""扩展"，或已装 Midscene Chrome 扩展 | 经扩展接管真实 Chrome |

CDP 与 Bridge 都保留登录态；未指定时**优先 CDP**（只需开个开关，无需装扩展）。

### CDP 预检（避免长超时）

```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" -H "Upgrade: websocket" -H "Connection: Upgrade" \
  -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  http://127.0.0.1:9222/devtools/browser
```

返回 `101` → 可用 `--cdp`；返回 `000`/curl 退出 7 → Chrome 未开远程调试，用 `--remote-debugging-port=9222` 启动后等 2–3 秒重试，仍失败则回落 Puppeteer 模式。

> **Bridge 模式没有可用预检**：3766 端口是 CLI 自己开的（CLI 是服务端、扩展是客户端），跑之前查必然空。直接 `--bridge connect`，看首行日志从 `waiting for bridge to connect...` 变成 `one client connected` 即成功。

## 核心命令

```bash
# 1. 连接并导航（CDP 模式下是导航"当前活动标签页"，不新开标签）
npx -y @midscene/web@1 connect --url https://example.com

# 2. 截图 —— 之后务必读取该图片文件再决定下一步
npx -y @midscene/web@1 take_screenshot

# 3. 执行动作：给高层复杂任务，别拆成碎步；描述"要做什么 + 期望效果"，不要写 #submit 这种选择器
npx -y @midscene/web@1 act --prompt "填入邮箱 user@example.com 和密码 pass123，然后点登录"
npx -y @midscene/web@1 act --prompt "点击国家下拉框并选择 Japan"

# 4. 断言当前页面状态（只校验、不操作，失败抛 AI 生成的原因）
npx -y @midscene/web@1 assert --prompt "结算页显示订单总额和支付按钮"
npx -y @midscene/web@1 assert --prompt "订单已确认" --message "点支付后应出现确认信息"

# 5. 收尾：disconnect 只断连接（浏览器还在）；close 才彻底关（仅 Puppeteer 模式）
npx -y @midscene/web@1 disconnect
npx -y @midscene/web@1 close
```

CDP/Bridge 模式下，上述每条命令都要带同样的连接参数：`--cdp ws://127.0.0.1:9222/devtools/browser` 或 `--bridge`。

### 文件上传

`act` 上传文件必须显式给 `--file-chooser-allowed-dir`，且**只给最小必要目录**，不要把项目根或家目录放进去：

```bash
npx -y @midscene/web@1 act --file-chooser-allowed-dir ./fixtures \
  --prompt "点上传按钮并上传 avatar.png"
```

Bridge 模式还需在 `chrome://extensions` → Midscene → 详情里打开「允许访问文件网址」，再从目标 `http(s)://` 标签页重连。

### 瞬时 UI（toast / loading / 动画）要用录制

当待验证状态会在断言前消失时，用录制而非当前屏断言：

```bash
# 终端 1：前台常驻，不要加 &
npx -y @midscene/web@1 record start --output ./obs.json
# 终端 2：期间执行交互
npx -y @midscene/web@1 act --prompt "点击提交按钮"
# 回终端 1 按 Ctrl+C，等它打印保存路径后再断言
npx -y @midscene/web@1 assert --record ./obs.json --prompt "提交过程中出现了成功 toast"
```

产物是 JSON manifest + 同名 `.frames` 图片目录，**两者要一起保留/搬迁**。默认看门狗 5 分钟自动保存，`--watchdog-ms 0` 可关。

### 有参考图时用 `tap --locate` 而非 `act`

用户给了截图/图标/logo 并要求精确视觉匹配时：

```bash
npx -y @midscene/web@1 tap --locate '{
  "prompt": "点击包含该图片的区域",
  "images": [{ "name": "target", "url": "https://example.com/logo.png" }],
  "convertHttpImage2Base64": true
}'
```

## 标准工作流

```
connect --url  →  take_screenshot（确认加载完成）  →  act（高层任务）
   →  assert / assert --record（校验）  →  close 或 disconnect  →  汇报结果与产物路径
```

## 精度不够时的两个开关

- `--deep-locate` — 多花一轮视觉推理精确定位。**点偏了/定位漂移**时加它（对 `act` 内部定位同样生效）。
- `--deep-think` — 让 `act` 做更深的规划与子目标拆解。**多步复杂指令**时加它。

两者可叠加，代价是变慢：

```bash
npx -y @midscene/web@1 act --deep-locate --deep-think \
  --prompt "打开设置菜单，进入偏好设置，开启暗色模式"
```

## 踩坑速查

| 现象 | 原因 / 处理 |
|------|------------|
| 连接失败 | 确认系统有 Chrome/Chromium（Puppeteer 默认自带）；检查防火墙是否拦本地调试端口 |
| API Key 报错 | 检查 `.env` 中 `MIDSCENE_MODEL_API_KEY`，并确认该 key 对配置的模型供应商有效 |
| 超时 | 连接后先截图确认页面就绪再交互；慢页面步骤间稍等 |
| `Cannot access a chrome:// URL` | Bridge 模式不能操作 `chrome://`、扩展页、应用商店；让用户切到普通 `http(s)://` 标签页 |
| 上传报 `Not allowed` | 先查 Bridge 扩展的「允许访问文件网址」权限 |
| 截图看不到 | 返回的是本地绝对路径，用读文件工具打开 |
| `@midscene/*` 版本过旧 | `npm ls @midscene/web` 查现状，`npm view @midscene/web version` 查最新，再 `npm i @midscene/web@latest` |

## 安全边界

- CDP 自定义请求头用 `--extra-http-header 'Name:Value'`（可重复传多个）。**不要把敏感值打进任务总结或 shell 历史**。
- 接管用户真实浏览器（CDP/Bridge）等于持有其登录态，只做用户明确要求的操作。
- `disconnect` 不会关掉外部管理的浏览器；CDP 模式下没有 `close`。

## 限制

- 依赖具备视觉定位能力的多模态模型，需自备 API key，有推理延迟与调用成本
- 不替代 Playwright/Cypress 写正式 CI 用例（正式 E2E 走 `software-tester`）
- 视觉定位对极小控件、纯图形界面仍可能漂移，需 `--deep-locate` 兜底

## 相关参考（Playbook）

本子技能落地"视觉驱动浏览器自动化"，前端方法论见下列 `references/`（按需读取）：

- 前端深度 playbook（组件 / CSS / 调试 / 性能 / 水合踩坑，§4 为 DevTools 自动化对照）：[references/frontend-playbook.md](../../references/frontend-playbook.md)
