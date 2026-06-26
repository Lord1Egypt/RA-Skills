---
name: cloudnet-wlan-inspection-lite
description: |
  Cloudnet WLAN无线网络巡检技能（极简版）。通过mcporter调用Cloudnet MCP接口，执行6步巡检流程：
  获取场所信息→AC健康度→问题分布与接入成功率→Cloudnet问题推理→AP上线率→生成巡检报告。
  输出中文MD+DOCX双格式巡检报告，标题为"无线网络运维巡检报告（极简版）"。
  适用于日常快速健康检查。
  触发词：巡检、极简版巡检、WLAN巡检、无线网络巡检、cloudnet巡检。
  前置依赖：mcporter CLI + cloudnet MCP服务器配置（API Key认证） + python-docx（DOCX报告用）。
---

# Cloudnet WLAN巡检技能（极简版）

> **版本：V0.0.2**
>
> 🎯 **设计原则：大模型做数据提取+判定，脚本仅做报告格式输出（MD+DOCX双格式）。**

## 第0步：前置检查（必须最先执行）

### 0.1 读取配置文件

```bash
# 读取skill根目录的config.json
cat config.json
```

**config.json 格式：**
```json
{
  "mcporter_name": "oasis",
  "api_key": "xxxxxxxx",
  "shops": [
    { "name": "场所名称" }
  ]
}
```

> 💡 `shops` 只需填写 `name`（场所名称），shopId 在巡检时由第1步 API 自动获取。

如果 `api_key` 为占位文本（如"在此填入"），提示用户填入真实 API Key 后重新巡检。

### 0.2 检查mcporter CLI

```bash
mcporter --version
```
- 通过：≥ 0.9.0 | 未通过：提示 `npm install -g mcporter`

### 0.3 检查并配置Cloudnet MCP连接

**唯一MCP地址（正式环境）：**
```
https://oasis.h3c.com/mcp-server/api/sse
```

```bash
mcporter config list
```
- 如果列表中已存在 `mcporter_name` 对应的配置 → ✅ 通过
- 如果不存在 → 自动执行配置：

```bash
mcporter config add <mcporter_name> https://oasis.h3c.com/mcp-server/api/sse --header "Authorization=Bearer <API_KEY>"
```

### 0.4 确认巡检场所

优先使用 `config.json` 中的 `shops` 列表（仅 name 字段）：
- 仅1个场所 → 直接使用，无需询问
- 多个场所 → 列出供用户选择
- shops 为空 → 询问用户输入场所名称

> ⚠️ 不可假设场所名称，必须有明确来源。**shopId 由第1步 API 查询后获取，无需在 config.json 中预填。**

### 0.5 检查python-docx（DOCX报告用）

```bash
python -c "import docx; print('OK')"
```
- 通过：✅ | 未通过：提示 `pip install python-docx`（仅影响DOCX输出，MD仍可生成）

### 0.6 输出检查结果

```
✅ mcporter v0.9.0
✅ Cloudnet MCP连接：<mcporter_name>
✅ 巡检场所：XXX
✅ python-docx

全部就绪，开始巡检。
```

如有未通过项，逐条列出 ❌ 并提示修复方法，**不继续执行**。

---

## mcporter调用规范（必读）

### 规则1：无参工具不传任何参数

```bash
# ✅ 正确
mcporter call <mcp-name> getallshopsanddevofuser

# ❌ 错误
mcporter call <mcp-name> getallshopsanddevofuser --args '{}'
```

### 规则2：有参工具使用 key=value 格式（PowerShell兼容）

```bash
# ✅ 正确
mcporter call <mcp-name> getDeviceRunInfo devSN=210235A2G0B206000003
mcporter call <mcp-name> getProblemDistribute shopId=2673243 "startTime=2026-05-19 00:00:00.000" "endTime=2026-05-19 10:00:00.000" timezone=Asia/Shanghai

# ❌ 错误 — PowerShell下单引号JSON解析失败
mcporter call <mcp-name> getDeviceRunInfo --args '{"devSN":"210235A2G0B206000003"}'
```

### 规则3：每个API结果保存为独立JSON文件

> mcporter输出含大量schema信息，日志中易截断。**使用 mcporter_call.py 保存纯净JSON。**

```bash
# ✅ 正确
python scripts/mcporter_call.py <mcp-name> <tool-name> reports/stepX.json [key=value ...]

# ❌ 错误 — PowerShell重定向有编码问题
mcporter call ... > reports/stepX.json
```

> 💡 mcporter_call.py 是唯一保留的Python脚本，仅做mcporter输出提取和文件保存，无第三方依赖。如Python也不可用，可改用cmd重定向：`cmd /c "mcporter call ... > reports/stepX.json 2>&1"`

---

## 巡检步骤

### 第1步：获取场所shopId和AC信息（串行，必须先完成）

**工具：** `getallshopsanddevofuser`（无参数！）

```bash
python scripts/mcporter_call.py <mcp-name> getallshopsanddevofuser reports/step1.json
```

**大模型处理：** 从step1.json中提取：
- 匹配用户指定场所名称（来自 config.json 或用户输入）→ `shopId`
- 该场所下customType=ac的设备 → `devSN`、`devModel`、`devAlias`、`status`、`softVer`
- 如匹配不到场所名称，列出所有场所供用户选择

> 💡 shopId 由本步骤从 API 实时获取，config.json 无需预填。

### 第2-5步：并行采集数据

> ⚠️ 步骤2/3/4/5 相互无依赖，**必须同时发起**。

#### 第2步：AC健康度

**工具：** `getDeviceRunInfo`

```bash
python scripts/mcporter_call.py <mcp-name> getDeviceRunInfo reports/step2.json devSN=<AC序列号>
```

**大模型提取：** cpuRatio / memoryRatio / diskRatio / speed_up / speed_down

**判定标准：**
| 检查项 | 🟢 正常 | ⚠️ 需关注 | 🔴 严重 |
|--------|---------|-----------|---------|
| CPU | ≤50% | ≤70% | >70% |
| 内存 | ≤70% | ≤85% | >85% |
| 磁盘 | ≤70% | ≤85% | >85% |

#### 第3步：问题分布 + 接入成功率（2个调用并行）

**工具A：** `getProblemDistribute`

```bash
python scripts/mcporter_call.py <mcp-name> getProblemDistribute reports/step3a.json shopId=<场所ID> "startTime=<当天 00:00:00.000>" "endTime=<当前时间>" timezone=Asia/Shanghai
```

**大模型提取：** 按times降序排列取TOP5问题类型及子类明细

**工具B：** `getHistoryAccessSucOneDay`（参数同上）

```bash
python scripts/mcporter_call.py <mcp-name> getHistoryAccessSucOneDay reports/step3b.json shopId=<场所ID> "startTime=<当天 00:00:00.000>" "endTime=<当前时间>" timezone=Asia/Shanghai
```

**大模型提取：** 找出最低接入成功率、对应时间、低于98%的时段数

**判定：** ≥98% 🟢 | ≥95% ⚠️ | <95% 🔴

#### 第4步：Cloudnet问题推理

**工具：** `getShopNetworkProblem`

```bash
python scripts/mcporter_call.py <mcp-name> getShopNetworkProblem reports/step4.json shopId=<场所ID>
```

**大模型提取：**
- `data.summary[]` → 按alarmLevel统计高危(3)/中危(2)数量
- `data.data[]` → 按alarmLevel分组，提取 reasoningType / count / reasoningCategory / suggestion / status

#### 第5步：AP上线率（2个调用并行）

**工具A：** `getCurrentApCount`

```bash
python scripts/mcporter_call.py <mcp-name> getCurrentApCount reports/step5a.json shopId=<场所ID>
```

**大模型提取：** online / offline / total，计算上线率

**工具B：** `getApRegularMatch`

```bash
python scripts/mcporter_call.py <mcp-name> getApRegularMatch reports/step5b.json shopId=<场所ID> dim=1
```

**大模型提取：** 从detail[]中筛选Ss=2的AP，提取apName列表

**判定：** ≥98% 🟢 | ≥95% ⚠️ | <95% 🔴

### 第6步：组装数据 + 生成双格式报告

#### 6.1 组装结构化巡检数据

大模型逐个读取 step1~step5b 的JSON文件，从 `response.data` 中提取关键字段，组装为符合 `references/data-format.md` 格式的JSON文件。

```bash
# 将结构化数据写入 reports/巡检数据_<场所>_<时间>.json
```

> 📄 数据格式参考：读取 `references/data-format.md` 了解完整JSON schema。

**告警级别判定标准：**

| 检查项 | 🟢 正常 | ⚠️ 需关注 | 🔴 严重 |
|--------|---------|-----------|---------|
| CPU | ≤50% | ≤70% | >70% |
| 内存 | ≤70% | ≤85% | >85% |
| 磁盘 | ≤70% | ≤85% | >85% |
| 接入成功率 | ≥98% | ≥95% | <95% |
| AP上线率 | ≥98% | ≥95% | <95% |

#### 6.2 生成MD+DOCX双格式报告

```bash
python scripts/gen_report.py --data-file reports/巡检数据_<场所>_<时间>.json --output-dir reports/
```

此脚本同时输出：
- MD报告：`reports/巡检报告_<场所>_<时间戳>.md`
- DOCX报告：`reports/巡检报告_<场所>_<时间戳>.docx`

**报告结构（6章）：**
```
一、执行摘要 → 关键指标 + 风险概览
二、健康度评估 → AC健康度 + 问题分布 + 接入成功率 + AP上线率
三、问题详细分析 → 高危/中危问题明细
四、问题处理优先级 → P0/P1/P2 分级
五、整改计划 → 短期/中期/长期
六、巡检结论 → 总体评价 + 关键风险 + 趋势建议
```

**报告撰写要求：**
- 全部中文，术语/缩写保留英文（CPU、RSSI、AP、AC、SSID、Portal、DHCP、SNMP、ARP、DNS、MTU、MSS、MCP、Cloudnet、mcporter等）
- 首页：标题"无线网络运维巡检报告（极简版）" + 场所名称 + 巡检时间 + 巡检工具名
- 按告警级别判定标准进行各项评级
- 问题分析基于实际数据，不可编造
- 整改计划结合实际问题给出针对性建议

#### 6.3 向用户输出巡检摘要（必须执行）

> ⚠️ **报告生成后，必须在聊天界面输出摘要，不要只说"报告已生成"。**

```
📋 巡检完成 — {场所名称}

🏥 AC健康度：CPU {x}% / 内存 {x}% / 磁盘 {x}% — {🟢正常/⚠️需关注/🔴严重}
📊 接入成功率：{min}%~100% — {🟢/⚠️/🔴}
📡 AP上线率：{rate}%（在线{on}/总计{total}）— {🟢/⚠️/🔴}
⚠️ 问题：高危{h}项 / 中危{m}项

🔴 需立即处理：
  1. {最高优先级问题} — {建议}
  2. {次高优先级问题} — {建议}

📁 报告已生成：
  MD：{md文件完整路径}
  DOCX：{docx文件完整路径}
```

---

## 执行流程图

```
第0步：读取config.json → mcporter检查 → MCP连接配置 → 场所确认
        │
        ▼
第1步：获取shopId + devSN（串行）→ step1.json
        │
        ├──────────┬──────────┬──────────┐
        ▼          ▼          ▼          ▼
     第2步       第3步       第4步       第5步       ← 并行
     step2.json  step3a/b   step4.json  step5a/b
        │          │          │          │
        └──────────┴──────────┴──────────┘
                        │
                        ▼
第6步：LLM提取数据 → 组装结构化JSON → gen_report.py
        │
        ├── reports/巡检报告_XXX.md    (MD格式)
        └── reports/巡检报告_XXX.docx  (DOCX格式)
                        │
                        ▼
                  输出巡检摘要
```

## 文件结构

```
skills/cloudnet-wlan-inspection-lite/
├── SKILL.md                        # 本文件
├── config.json                     # API Key + 场所配置（用户填写）
├── scripts/
│   ├── mcporter_call.py            # mcporter输出提取（无第三方依赖）
│   └── gen_report.py              # MD+DOCX双格式报告生成（依赖python-docx）
└── references/
    └── data-format.md              # 巡检数据结构化JSON格式定义
```

## config.json 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mcporter_name` | string | ✅ | mcporter config add 时使用的连接名称 |
| `api_key` | string | ✅ | Cloudnet API Key（在Cloudnet平台获取） |
| `shops` | array | ✅ | 场所列表，每个场所含 name |
| `shops[].name` | string | ✅ | 场所名称（巡检时通过 API 自动获取 shopId） |