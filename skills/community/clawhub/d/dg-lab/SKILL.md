---
name: dg-lab
description: Control DG-LAB Coyote 3.0 (郊狼) pulse device via WebSocket. Manage strength, send waveform patterns, handle device pairing. Use when the user mentions 郊狼, DG-LAB, coyote, pulse device, e-stim, 脉冲, 电脉冲, waveform control, or wants to interact with dungeon-lab hardware.
homepage: https://github.com/YuuLuo/DG-LAB-Skill
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["python3", "node", "npm"]
      network: true
    files: ["scripts/*", "references/*"]
---

# 郊狼控制器

通过 WebSocket 协议控制郊狼脉冲主机 3.0 的 A/B 双通道：强度调节、波形发送、设备配对。
在中文语境中，本设备称为"郊狼"（英文：DG-LAB Coyote）。与用户交流时统一使用"郊狼"。

## 架构

```
AI Agent --curl/HTTP--> ws_client.py --WebSocket--> 中继服务器 --WS--> DG-LAB APP --BLE--> 郊狼 3.0
```

`ws_client.py` 是常驻后台进程，同时维护 WebSocket 连接和本地 HTTP API（默认 `127.0.0.1:8899`）。

## 启动工作流

每次用户要求使用郊狼时，严格按以下顺序执行。**每一步都必须确认成功后再进入下一步。**

### 第 1 步：环境检查

依次检查以下环境，将结果汇总向用户报告：

```bash
# 1. Python 3
python3 --version

# 2. websockets 包
python3 -c "import websockets; print(websockets.__version__)"

# 3. Node.js + npm
node --version && npm --version

# 4. 中继服务器仓库是否已克隆
ls ~/DG-LAB-OPENSOURCE/socket/v2/backend/package.json
```

### 第 2 步：安装缺失组件

根据检查结果，帮助用户安装缺失的组件：

**websockets 未安装：**
```bash
pip install websockets
```

**中继服务器仓库不存在：**
```bash
cd ~ && git clone https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE.git
cd ~/DG-LAB-OPENSOURCE/socket/v2/backend && npm install
```

**中继服务器依赖未安装（node_modules 不存在）：**
```bash
cd ~/DG-LAB-OPENSOURCE/socket/v2/backend && npm install
```

安装完成后重新执行第 1 步确认全部通过。

### 第 3 步：启动服务

```bash
# 启动中继服务器（后台）
cd ~/DG-LAB-OPENSOURCE/socket/v2/backend && npm start &

# 等待服务器就绪后启动控制器
python scripts/ws_client.py --ws-url ws://localhost:9999 --strength-limit 50 &
```

验证两个服务都在运行：
```bash
curl -s http://127.0.0.1:8899/status
```

如果返回 `connected: true`，继续下一步。

### 第 4 步：发送配对二维码

```bash
curl -s http://127.0.0.1:8899/qrcode
```

将返回的 `qr_url` 发送给用户（如果当前聊天渠道支持发送图片，确保发送的是二维码图片并确认是否成功发送），并指引：

> 请打开DG-LAB APP → 点击 **SOCKET 控制** → 点击 **连接服务器** → 扫描此二维码完成配对。

然后轮询等待配对完成：
```bash
curl -s http://127.0.0.1:8899/status
```

直到 `paired: true`。如果 30 秒内未配对成功，提醒用户重试。

### 第 5 步：安全确认（必须执行）

配对成功后，**必须向用户确认以下安全事项，获得明确肯定回答后才能开始输出脉冲：**

> **使用前安全确认：**
>
> 1. 电极片是否已正确贴好？
> 2. 电极片的贴放位置是否**避开了心脏投影区域两侧**？（电流路径不得经过心脏）
> 3. 身体是否存在心脏疾病、佩戴心脏起搏器、癫痫等禁忌症？
>
> 请确认以上条件均已满足后回复"确认"。

**用户未明确确认前，禁止发送任何强度或波形指令。**

### 第 6 步：确认已连接的通道

安全确认通过后，询问用户当前连接了哪些通道：

> 郊狼有 A、B 两个输出通道。你当前连接了哪个（哪些）通道？
> - 仅 A 通道
> - 仅 B 通道
> - A 和 B 双通道

记录用户回答，后续所有操作**只对用户已连接的通道发送指令**。未连接的通道禁止发送任何强度或波形命令。

### 第 7 步：开始使用

通道确认后，告知用户已就绪，并展示可用操作和预设列表。

## HTTP API 参考

### GET /status

返回连接状态、配对状态、当前强度、安全限制。

### GET /qrcode

返回 APP 扫码配对的 URL。

### GET /presets

列出所有可用波形预设及其描述。

### POST /strength

| 字段 | 类型 | 说明 |
|------|------|------|
| `channel` | `"A"` / `"B"` | 通道（**只能使用用户已确认连接的通道**） |
| `action` | `"set"` / `"increase"` / `"decrease"` | 操作 |
| `value` | int | 目标值或变化量 |

### POST /waveform

| 字段 | 类型 | 说明 |
|------|------|------|
| `channel` | `"A"` / `"B"` | 通道（**只能使用用户已确认连接的通道**） |
| `preset` | string | 预设名（与 `data` 二选一） |
| `data` | string[] | 自定义 HEX 数组（与 `preset` 二选一） |
| `duration` | int | 持续秒数（1-60，默认 5） |

### POST /clear

清空指定通道波形队列。`{"channel": "A"}`（**只能操作用户已确认连接的通道**）

### POST /emergency-stop

**紧急停止**：双通道强度归零 + 清空波形队列。无需参数。

### POST /stop

优雅关闭控制器进程。

## 可用波形预设

| ID | 中文名 | 时长 | 特点 |
|----|--------|------|------|
| `breathing` | 呼吸 | 1.2s | 缓慢淡入淡出，轻柔放松 |
| `tide` | 潮汐 | 2.3s | 平滑波浪，频率和强度渐变 |
| `combo` | 连击 | 2.4s | 快速开关脉冲，带递减尾部 |
| `quick-pinch` | 快速按捏 | 4.4s | 恒频快速交替开关 |
| `pinch-crescendo` | 按捏渐强 | 2.3s | 交替开关 + 强度逐次递增 |
| `heartbeat` | 心跳节奏 | 3.4s | 模拟心跳：强脉冲 + 间歇 + 弱脉冲 |
| `compression` | 压缩 | 2.1s | 频率递降 + 恒定满强度，压迫感 |
| `rhythm-step` | 节奏步伐 | 2.7s | 渐快的阶梯式节奏 |
| `grain-friction` | 颗粒摩擦 | 2.8s | 频率递增 + 脉冲式强度，颗粒质感 |
| `gradient-bounce` | 渐变弹跳 | 4.8s | 反复渐升 + 频率渐高，弹跳感 |
| `wave-ripple` | 波浪涟漪 | 5.3s | 分层波浪 + 阶梯升频，涟漪扩散感 |
| `rain-rush` | 雨水冲刷 | 7.5s | 轻柔点触渐变为持续冲刷 |
| `variable-tap` | 变速敲击 | 8.4s | 节奏敲击加速后进入持续高频 |
| `signal` | 信号灯 | 4.0s | 长高频信号 + 短促警告式渐升 |
| `tease-1` | 挑逗1 | 6.3s | 缓慢升到顶峰骤降，反复后快速开关 |
| `tease-2` | 挑逗2 | 8.8s | 降频升强反复后加速交替脉冲 |

使用示例：
```bash
curl -X POST http://127.0.0.1:8899/waveform \
  -H "Content-Type: application/json" \
  -d '{"channel":"A","preset":"breathing","duration":10}'
```

## 自定义波形生成

使用 `waveform.py` 生成自定义波形数据：

```bash
python scripts/waveform.py list
python scripts/waveform.py constant 15 60 2000
python scripts/waveform.py ramp 10 0 80 3000
```

Python 调用：

```python
from waveform import generate_sine, generate_pulse

data = generate_sine(freq=20, max_intensity=80, period_ms=1000, duration_ms=5000)
data = generate_pulse(freq=10, intensity=50, on_ms=200, off_ms=300, duration_ms=3000)
```

将生成的数据发送到设备：
```bash
DATA=$(python scripts/waveform.py constant 15 60 2000)
curl -X POST http://127.0.0.1:8899/waveform \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"A\",\"data\":$DATA,\"duration\":5}"
```

## 安全机制

### 通道限制

在第 6 步中用户会告知已连接的通道。此后**严格只对已连接通道发送指令**，向未连接通道发送指令无意义且可能导致意外。若用户中途更换通道连接，需重新确认。

### 强度上限

`--strength-limit` 参数（默认 50）限制可设置的最大强度值。任何超出此值的操作会被拒绝。

### 速率限制

连续强度命令间隔不得小于 100ms，防止意外快速递增。

### 紧急停止

`POST /emergency-stop` 立即将双通道强度归零并清空波形队列。任何时候用户说"停"、"stop"或表达不适，立即执行紧急停止。

### 协议验证

- 所有波形 HEX 数据在发送前经过格式和范围校验
- 频率范围 10-240，强度范围 0-100
- JSON 消息长度不超过 1950 字符
- duration 限制在 1-60 秒

### 连接恢复

WebSocket 断连后自动每 3 秒尝试重连。重连后需重新配对。

### 电极安全规则

- 电极片**禁止**贴在心脏投影区域两侧（电流路径不得横穿心脏）
- 有心脏疾病、心脏起搏器、癫痫病史的用户**禁止使用**
- 皮肤破损、伤口处**禁止**贴放电极片
- 首次使用**必须从低强度开始**，逐步增加

## External Endpoints

| 端点 | 方向 | 说明 |
|------|------|------|
| `ws://HOST:PORT` (默认 `ws://localhost:9999`) | 出站 → 本地中继服务器 | WebSocket 连接，传输设备控制指令和状态。数据不离开本机。 |
| `http://127.0.0.1:8899/*` | 本地回环 | AI Agent 与 ws_client.py 之间的 HTTP 控制通道。仅监听 localhost。 |
| `https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE.git` | 出站 → GitHub | 仅在首次安装时 clone 官方中继服务器代码，之后不再访问。 |

## Security & Privacy

- **所有控制通信均在本机完成**：ws_client.py 连接的中继服务器运行在 localhost，HTTP API 仅监听 127.0.0.1
- **不收集、不上传任何用户数据**：本 skill 不向外部服务器发送任何使用数据、遥测或日志
- **唯一的外部网络访问**发生在首次安装时从 GitHub 克隆中继服务器仓库
- **设备通信路径**：本机中继服务器 ↔ 同一局域网内的 DG-LAB APP（通过 WebSocket），APP ↔ 郊狼设备（通过 BLE）
- 脚本不读写用户文件系统中 skill 目录之外的任何文件（除日志输出到 stderr）

## Trust Statement

本 skill 通过 WebSocket 与本地运行的 DG-LAB 官方中继服务器通信，控制指令经由用户手机上的 DG-LAB APP 转发至物理设备。所有通信均在本机或局域网内完成，不涉及第三方云服务。请确保中继服务器来源可信（仅使用 [DG-LAB 官方仓库](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE)）。

## 参考文档

- **WebSocket 协议详情**: 见 [references/protocol.md](references/protocol.md) — 消息格式、错误码、配对流程
- **波形 HEX 格式**: 见 [references/waveform-format.md](references/waveform-format.md) — V3 编码规范、频率换算公式、示例解析
