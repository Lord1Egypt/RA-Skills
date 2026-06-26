---
name: geeklink-home
description: "[English] Control Geeklink Home local gateway devices and scenes over LAN via the bundled self-contained Node.js runtime. Supports device listing, scene listing, state checks, scene activation, and local device control using pairing-token based auth. | [中文] 通过内置自包含的 Node.js 运行时，在局域网内控制 Geeklink Home 网关设备和场景。支持设备列表、场景列表、状态查询、场景执行，以及基于配对 token 的本地设备控制。"
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["node"]}}}
---

# Geeklink Home Control | Geeklink Home 局域网控制

[English] | [中文](#中文说明)

---

## English

Use the local Geeklink Home gateway over LAN through the bundled self-contained Node.js skill runtime.

### Features

- Local LAN access to the Geeklink Home gateway
- Pairing-token based authentication
- Device catalog, scene catalog, and state snapshot access
- Background watcher with recent event and single-device state queries
- Scene activation and local device control
- Multi-gang panels are expanded into practical sub-devices such as `吊灯` and `筒灯`
- Packaged around the bundled `vendor/geeklink-lan-cli.js` runtime
- The persistent runtime keeps a single watcher instance per loaded skill

### Setup

1. Ensure `vendor/geeklink-lan-cli.js` exists in the installed skill package.
2. Open the gateway details page in the Geeklink app and go to `AI Skill Access`.
3. Copy `gatewayHost` and `pairingToken` from that page.
4. Use the cross-platform Node wrapper scripts in `scripts/` to query devices, scenes, states, and execute actions.
5. When loaded by ClawHub/OpenClaw as a skill runtime, the watcher is started automatically and tools can read recent events.

### Core Workflow

1. Open the gateway details page in the Geeklink app and enter `AI Skill Access`.
2. Read the `gatewayHost` and `pairingToken` shown on that page.
3. Run `node scripts/geeklink-home.js login --host <host> --pairing-token <token>` once to cache session.
3. Use:
   - `node scripts/geeklink-home.js catalog devices --refresh`
   - `node scripts/geeklink-home.js catalog devices --query 吊灯 --refresh`
   - `node scripts/geeklink-home.js catalog scenes --refresh`
   - `node scripts/geeklink-home.js state snapshot --refresh`
   - `node scripts/geeklink-home.js scene activate <sceneId>`
   - `node scripts/geeklink-home.js device control <catalogDeviceId> ...`

### Natural Language Mapping

When the user asks for:

- "What devices do I have?" -> run `catalog devices --refresh`
- "What scenes are available?" -> run `catalog scenes --refresh`
- "Turn on living room light" -> find the matching expanded `catalog_device_id` (for example `吊灯` under a panel), then run `device control <id> --power on`
- "Set bedroom AC to 26 cool high" -> `device control <id> --power on --temperature 26 --mode cool --fan-speed high`
- "Run away mode" -> find `scene_id`, then run `scene activate <sceneId>`
- "Is the living room light on?" -> use `geeklink_get_device_state`
- "What changed recently?" -> use `geeklink_get_recent_events`

Do not guess `catalog_device_id`. Always list devices first if the mapping is unclear. When a panel exposes named roads, prefer the expanded road device like `吊灯` instead of the parent panel name.

### Release Notes

- Version: `0.1.0`
- Validated:
  - Device catalog
  - Scene catalog
  - Local device control
  - State snapshot
  - Single-watcher recent event tracking
- ClawHub publisher owner id for this package is `lintertion`.

---

## 中文说明

通过内置的自包含 Node.js 运行时，在局域网内直接访问 Geeklink Home 网关。

### 功能

- 在局域网内访问 Geeklink Home 网关
- 基于 pairing token 的认证
- 读取设备目录、场景目录、状态快照
- 提供后台 watcher、最近事件和单设备状态查询
- 执行场景和本地设备控制
- 以 `vendor/geeklink-lan-cli.js` 为底层运行时
- 多路面板会展开成更符合用户习惯的子设备，例如 `吊灯`、`筒灯`
- 常驻 skill runtime 只会启动一个 watcher 实例

### 使用前准备

1. 确认已安装的 skill 包中存在 `vendor/geeklink-lan-cli.js`。
2. 在 Geeklink App 的网关详情页进入 `AI技能接入` 页面。
3. 在该页面查看并复制 `gatewayHost` 和 `pairingToken`。
4. 通过 `scripts/` 中的跨平台 Node 包装脚本完成登录、列表查询、场景执行和设备控制。
5. 如果由 ClawHub/OpenClaw 以常驻 skill runtime 加载，watcher 会自动启动，并支持读取最近事件。

### 建议工作流

1. 先在 Geeklink App 的网关详情页打开 `AI技能接入` 页面。
2. 记录页面展示的 `gatewayHost` 和 `pairingToken`。
3. 首次使用先执行：
   ```bash
   node scripts/geeklink-home.js login --host <host> --pairing-token <token>
   ```
4. 然后按需执行：
   - `node scripts/geeklink-home.js catalog devices --refresh`
   - `node scripts/geeklink-home.js catalog devices --query 吊灯 --refresh`
   - `node scripts/geeklink-home.js catalog scenes --refresh`
   - `node scripts/geeklink-home.js state snapshot --refresh`
   - `node scripts/geeklink-home.js scene activate <sceneId>`
   - `node scripts/geeklink-home.js device control <catalogDeviceId> ...`

### 自然语言意图映射

- “我有哪些设备” -> `catalog devices --refresh`
- “有哪些场景” -> `catalog scenes --refresh`
- “打开客厅主灯” -> 先找到展开后的子设备 `catalog_device_id`，再执行 `device control <id> --power on`
- “卧室空调调到 26 度制冷高速” -> `device control <id> --power on --temperature 26 --mode cool --fan-speed high`
- “执行离家模式” -> 找到 `scene_id`，再执行 `scene activate <sceneId>`
- “客厅灯现在开着吗” -> `geeklink_get_device_state`
- “最近发生了什么变化” -> `geeklink_get_recent_events`

不要猜测 `catalog_device_id`。如果设备匹配不确定，先列出设备再确认。对于多路面板，优先使用展开后的子设备名，例如 `吊灯`、`筒灯`，不要只盯着父设备名。

### 发布说明

- 版本：`0.1.0`
- 已验证能力：
  - 设备目录
  - 场景目录
  - 本地设备控制
  - 状态快照
  - 单实例 watcher 最近事件跟踪
- 该包发布到 ClawHub 时使用的 `ownerId` 为 `lintertion`。
