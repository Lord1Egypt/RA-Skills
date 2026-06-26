---
name: Cloudnet AI Diagnostics
description: Cloudnet AI Diagnostics针对无线场景下终端体验差、网卡、无法接入 WiFi 等问题进行排障的技能
version: "1.0"
metadata: { "openclaw": { "requires": { "bins": ["npm", "mcporter"] }, "primaryEnv": "CLOUDNET_API_KEY" } }
triggers:
  - "WiFi 问题排查"
  - "无线网络故障"
  - "终端上网慢"
  - "连不上 WiFi"
  - "网络卡顿"
author: Cloudnet Skills
---

# Cloudnet AI Diagnostics

针对无线场景下终端体验差、网卡、无法接入 WiFi 等问题进行排障。

## 触发条件

用户询问关于无线终端连接问题，例如：
- "XX 场所的 XX 终端上网很慢"
- "XX 场所的 XX 设备连不上 WiFi"
- "XX 场所的 XX 用户反馈网络卡"

## 前置环境检查

### 安装`mcporter`cli支持及skill支持

- mcporter: `npm install -g mcporter`
- 然后再通过clawhub安装`mcporter`技能

### 配置MCP连接参数

- `CLOUDNET_API_KEY` 必须.  需要用户提供Cloudnet管理平台的API KEY，可通过Cloudnet管理平台（网络管理=>设置=>开放平台）获取
- 可选: `CLOUDNET_BASE_URL` Cloudnet管理平台地址. 默认使用https://oasis.h3c.com
- 执行`mcporter config add cloudnet-mcp ${CLOUDNET_BASE_URL}/mcp-server/api/sse --header Authorization="Bearer ${CLOUDNET_API_KEY}"`


## 排障步骤

### 第一步：提取关键信息

从用户问题中提取以下信息：

| 信息 | 说明 | 示例 |
|------|------|------|
| **场所名** | 必填，问题发生的场所 | "总部办公室"、"XX门店" |
| **终端信息** | 必填，MAC 地址或终端用户名 | MAC: `xxxx-xxxx-xxxx` 或用户名: `zhangsan` |
| **故障时间** | 可选，用户未指定则默认当前时间 | "2026-03-24 10:00:00" |

**重要**：如果场所名和终端信息未提取到，必须让用户补充完整后才能继续下一步。

### 第二步：查询场所 ID

调用 `cloudnet-mcp.getallshopsanddevofuser` 获取用户下所有场所，找到场所名对应的场所 ID，场所 ID 无需显示告诉用户。

```bash
mcporter call cloudnet-mcp.getallshopsanddevofuser
```

### 第三步：执行终端诊断

根据提取的终端信息（MAC 或用户名 或IP地址），调用 `executeStaDiagnosis` 进行诊断：

**参数说明**：
- `clientInfo`: 终端 MAC 地址，格式 `xxxx-xxxx-xxxx` 或者 终端 IP 地址，如`192.168.1.1`， 或者 终端用户名，如`h3cuser1`
- `shopId`: 场所 ID（来自第二步），需要转为字符串类型
- `faultTime`: 故障时间，格式 `yyyy-MM-dd HH:mm:ss`，用户未指定则使用当前时间
- `timezone`: 用户时区，默认 `Asia/Shanghai`

- 当提取到MAC地址时的调用示例

```bash
mcporter call cloudnet-mcp.executeStaDiagnosis clientInfo:"xxxx-xxxx-xxxx" shopId:"场所ID" faultTime:"2026-03-24 10:00:00" timezone:"Asia/Shanghai"
```

- 当提取到终端IP地址时的调用示例

```bash
mcporter call cloudnet-mcp.executeStaDiagnosis clientInfo:"192.168.1.1" shopId:"场所ID" faultTime:"2026-03-24 10:00:00" timezone:"Asia/Shanghai"
```

- 当提取到终端用户名时的调用示例

```bash
mcporter call cloudnet-mcp.executeStaDiagnosis clientInfo:"h3cuser1" shopId:"场所ID" faultTime:"2026-03-24 10:00:00" timezone:"Asia/Shanghai"
```

### 第四步：分析诊断结果

诊断返回后会包含：
- 终端连接概览数据（包含终端接入能力、当前认证方式、信号强度、丢包率、重传率等数据）
- 连接设备软件版本信息（包含AP、AC）
- 云平台操作日志
- 设备运行状态（包含AC、AP设备的CPU、内存问题发生次数）
- 终端连接过程数据
- 终端运行状态分析，诊断时间内终端的无线指标（干扰、信号强度、流量、选速、丢包率、重传率等）采样数据
- AP空口环境分析，诊断时间内AP射频相关的无线指标（干扰、底噪、信噪比、流量、选速、信道利用率、接入用户数等）采样数据
- 根因推理结论（定位终端发生问题可能的根因）
- 诊断结论（包含异常指标及修复建议）

结合诊断结果回答用户问题，并给出具体的解决建议。

## 输出格式

你是一名资深的无线网络排障专家。现在排障工作已完成，请基于用户的问题，仅提取与问题相关的诊断数据和结论，进行专业、正面的回答。输出内容必须严格遵循以下三个部分：
1. 诊断结果摘要：用1-2句话概括当前网络状态及核心结论。
2. 问题根因分析：深入分析导致该问题的技术原因，避免罗列无关数据。
3. 建议解决措施：提供具体、可操作的实施步骤。