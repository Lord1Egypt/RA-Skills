---

slug: aegis-security-tool-free
name: aegis-security-tool-free
version: 1.0.0
displayName: 区块链安全扫描免费版
summary: "区块链地址与代币安全检查工具,支持地址信誉查询、代币蜜罐检测,适合个人开发者日常交易前快速验证.。区块链安全扫描免费版,为个人用户提供地址信誉查询、代币安全检测等核心能力."
license: MIT
edition: free
description: "区块链安全扫描免费版,为个人用户包含地址信誉查询、代币安全查验等核心能力. 适用于需要aegis security tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 主要功能包括区块链安全扫描免费版、免费版与专业版对比. 适用于需要aegis security tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量."
tags:
  - 安全
  - aegis
  - security
  - automation
  - productivity
  - 区块链
  - DeFi
  - 免费版
  - 加密
  - 工具
tools:
  - read
  - exec
homepage: ""
category: "Security"
pricing_tier: free





---

# 区块链安全扫描免费版

## 概述

本工具为区块链用户提供轻量级安全检查能力,支持对以太坊、Base、Solana等多链地址进行信誉查询与代币安全检测。免费版提供每日100次检查额度,覆盖个人开发者日常交易验证需求,帮助用户在发送交易前快速识别风险地址与恶意代币.
### 免费版与专业版对比

| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 每日检查额度 | 100次/天 | 无限制 |
| 交易模拟 | 不支持 | 支持 |
| 多链覆盖 | 8条主流链 | 15条链+测试网 |
| 批量检查 | 单次单地址 | 批量CSV导入 |
| 风险报告导出 | 基础文本 | HTML/PDF/SARIF |
| API并发 | 1 QPS | 10 QPS |
| 告警推送 | 不支持 | Webhook/邮件 |

## 核心能力

### 1. 地址信誉查询

查询任意区块链地址的风险评级,识别已知诈骗地址、钓鱼地址与恶意合约.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 区块链安全扫描免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 查询以太坊地址信誉
curl -s "https://api.example.com/v1/check-address/0x742d35Cc6634C0532925a3b844Bc454e4438f44e?chain_id=1" | jq
# ...
# 查询Base链地址信誉
```

返回示例:

```json
{
  "address": "0x742d35Cc...",
  "chain_id": 1,
  "risk_level": "LOW",
  "is_safe": true,
  "flags": [],
  "_meta": {
    "requestId": "uuid-placeholder",
    "tier": "free",
    "latencyMs": 42
  }
}
```

**处理**: 解析地址信誉查询的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回地址信誉查询的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 代币蜜罐检测

检测代币是否存在蜜罐风险(买入后无法卖出)、无限增发、隐藏转账等恶意行为.
```bash
# 检测ERC20代币安全性
xyz/v1/check-item/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48?chain_id=1" | jq
```

**处理**: 解析代币蜜罐检测的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回代币蜜罐检测的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 免费额度查询

实时查看当日剩余免费检查次数.
```bash
# 在此执行相关操作
echo "操作完成"
```

返回示例:

```json
{
  "freeTier": {
    "enabled": true,
    "dailyLimit": 100,
    "usedToday": 12,
    "remainingChecks": 88,
    "nextResetAt": "2026-07-19T00:00:00.000Z",
    "resetTimezone": "UTC"
  }
}
```

**处理**: 解析免费额度查询的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费额度查询的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：区块链地址与代币、安全检查工具、支持地址信誉查询、代币蜜罐检测、适合个人开发者日、常交易前快速验证、区块链安全扫描免、为个人用户提供地、址信誉查询、代币安全检测等核、心能力、核心能力、地址风险检查、免费额度查询、风险等级分级、适用场景、DeFi、交易前验证、代币安全排查、收款地址风险评估、差异化、免费版聚焦核心检、查能力、次免费额度、适合个人用户日常、适用关键词、区块链安全、地址检查、代币扫描、蜜罐检测、blockchain、scan、token、address等.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:DeFi交易前安全验证

用户准备在去中心化交易所进行代币兑换,需要验证目标代币合约是否安全.
```bash
#!/bin/bash
# 交易前安全检查脚本(免费版)
# ...
TOKEN_ADDRESS="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
CHAIN_ID=1
# ...
echo "正在检查代币安全性..."
RESULT=$(curl -s "https://api.example.com/v1/check-${PARAM}/${ITEM_ADDRESS}?chain_id=${CHAIN_ID}")
# ...
RISK_LEVEL=$(echo "$RESULT" | jq -r '.risk_level')
IS_SAFE=$(echo "$RESULT" | jq -r '.is_safe')
# ...
echo "代币地址: ${ITEM_ADDRESS}"
echo "风险等级: ${RISK_LEVEL}"
echo "是否安全: ${IS_SAFE}"
# ...
if [ "$RISK_LEVEL" = "CRITICAL" ] || [ "$IS_SAFE" = "false" ]; then
    echo "警告: 该代币存在高风险,建议不要交易!"
    exit 1
else
    echo "该代币通过基础安全检查。"
fi
```

### 场景二:收款地址风险评估

用户收到来自未知地址的转账请求,需要评估该地址是否存在诈骗风险.
```bash
#!/bin/bash
# 收款地址风险评估
RECEIVER="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
# ...
xyz/v1/check-address/${RECEIVER}?chain_id=1")
RISK=$(echo "$RESULT" | jq -r '.risk_level')
# ...
case $RISK in
    LOW)      echo "风险等级: 低 - 可以安全交互" ;;
    MEDIUM)   echo "风险等级: 中 - 建议谨慎,核实对方身份" ;;
    HIGH)     echo "风险等级: 高 - 不建议交互" ;;
    CRITICAL) echo "风险等级: 极高 - 该地址可能为诈骗地址,请立即停止交互" ;;
esac
```

### 场景三:多链地址批量查询(基础版)

免费版支持手动循环查询多个地址,适合小规模验证.
```bash
#!/bin/bash
# 批量地址检查(免费版,手动循环)
CHAIN_ID=1
ADDRESSES=(
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    "0xdAC17F958D2ee523a2206206994597C13D831ec7"
)
# ...
for addr in "${ADDRESSES[@]}"; do
    RISK=$(curl -s "https://api.example.com/v1/check-address/${addr}?chain_id=${CHAIN_ID}" | jq -r '.risk_level')
    echo "${addr} -> ${RISK}"
    sleep 1  # 免费版限速,每次间隔1秒
done
```

## 不适用场景

以下场景区块链安全扫描免费版不适合处理：

- 渗透测试未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、漏洞扫描、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 领先步:验证服务可用性

```bash
curl -s https://api.example.com/health
```

### 第二步:查询免费额度

```bash
xyz/v1/usage" | jq '.freeTier'
```

### 第三步:执行首次地址检查

```bash
# 在此执行相关操作
echo "操作完成"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 设置客户端指纹

建议设置稳定的客户端指纹,便于免费额度统计:

```bash
# 在请求头中设置指纹
FINGERPRINT="user-$(whoami)-$(hostname)"
# ...
curl -s -H "X-Client-Fingerprint: ${FINGERPRINT}" \
  "https://aegis402.chain_id=1"
```

### 支持的链

| 链名称 | Chain ID | 地址检查 | 代币检查 |
|---:|---:|---:|---:|
| Ethereum | 1 | 支持 | 支持 |
| Base | 8453 | 支持 | 支持 |
| Polygon | 137 | 支持 | 支持 |
| Arbitrum | 42161 | 支持 | 支持 |
| Optimism | 10 | 支持 | 支持 |
| BSC | 56 | 支持 | 支持 |
| Avalanche | 43114 | 支持 | 支持 |
| Solana | solana | 支持 | 支持 |

### 风险等级说明

| 等级 | 含义 | 建议操作 |
|:---:|:---:|:---:|
| LOW | 风险较低,基本安全 | 可以正常交互 |
| MEDIUM | 存在部分风险 | 建议人工复核 |
| HIGH | 风险显著 | 不建议交互 |
| CRITICAL | 极高风险,可能恶意 | 立即停止交互 |

## 优秀实践

1. **交易前必查**:在发送任何链上交易前,先对目标地址和代币执行安全检查.
2. **稳定指纹**:设置固定的 `X-Client-Fingerprint` 头,确保免费额度准确统计.
3. **额度管理**:定期查询 `/v1/usage` 接口,避免超额后无法使用.
4. **结果留档**:对高风险交易保留检查结果的JSON输出,便于后续追溯.
5. **多链注意**:`chain_id` 是被扫描的链,需与实际交易链一致.
```bash
# 优秀实践:交易前完整检查流程
check_before_transact() {
    local to_addr=$1
    local chain=$2
    local fingerprint="my-agent-$(date +%Y%m%d)"
# ...
    echo "=== 交易前安全检查 ==="
    echo "目标地址: ${to_addr}"
    echo "链 ID: ${chain}"
# ...
    # 查询额度
    USAGE=$(curl -s -H "X-Client-Fingerprint: ${fingerprint}" "https://api.example.com/v1/usage")
    REMAINING=$(echo "$USAGE" | jq -r '.freeTier.remainingChecks')
    echo "剩余免费额度: ${REMAINING}"
# ...
    if [ "$REMAINING" -lt 5 ]; then
        echo "警告: 免费额度不足,请谨慎使用"
    fi
# ...
    # 地址检查
    RESULT=$(curl -s -H "X-Client-Fingerprint: ${fingerprint}" \
        "https://api.example.com/v1/check-address/${to_addr}?chain_id=${chain}")
# ...
    echo "地址风险等级: ${RISK}"
# ...
    if [ "$RISK" = "CRITICAL" ] || [ "$RISK" = "HIGH" ]; then
        echo "阻止: 地址风险过高,建议取消交易"
        return 1
    fi
# ...
    echo "通过: 地址检查完成,可以继续交易"
    return 0
}
```

## 常见问题

### Q1: 免费额度用完后怎么办?

免费额度每日UTC时间0点重置。如需更高额度,可升级至专业版获取无限制检查能力.
### Q2: 查询返回402错误是什么意思?

表示免费额度已用完。可通过 `GET /v1/usage` 确认剩余额度,等待次日重置或升级专业版.
### Q3: 地址检查结果为LOW就一定安全吗?

LOW表示未检测到已知风险,但不代表绝对安全。安全检查是辅助工具,仍需结合自身判断。免费版不包含交易模拟,无法检测复杂的交易逻辑风险.
### Q4: Solana链的chain_id怎么填?

Solana链使用字符串 `solana` 作为chain_id,而非数字.
### Q5: 如何提高检查准确性?

建议同时执行地址检查和代币检查(如涉及代币交易)。专业版提供交易模拟功能,可检测更深层风险.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问 `https://api.example.com`

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| curl | 命令行工具 | 必需 | 系统自带或包管理器安装 |
| jq | JSON处理工具 | 推荐 | `apt install jq` / `brew install jq` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 免费版无需API Key,直接调用即可
- 建议设置 `X-Client-Fingerprint` 请求头用于额度统计

### 可用性分类
- **分类**: MD+EXEC模式纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行区块链安全检查任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
