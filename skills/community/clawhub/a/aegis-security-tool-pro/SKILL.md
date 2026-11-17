---
slug: aegis-security-tool-pro
name: aegis-security-tool-pro
version: 1.0.0
displayName: 区块链安全扫描专业版
summary: 企业级区块链安全工具,支持交易模拟、批量地址检查、多链覆盖、风险报告导出与告警推送,适合DeFi团队与机构用户.
license: Proprietary
edition: pro
description: 区块链安全扫描专业版,为DeFi团队与机构用户包含全方位链上安全防护. 适合需要aegis security tool相关能力的开发场景,提供结构化工作流程和配置说明。适用于独立开发者、企业团队和自动化工作流场景，提供结构化输出与错误处理机制，支持中文交互，即开即用。Use when 用户需要区块链安全扫描专业版相关功能时使用。不适用于超出本技能能力范围的复杂需求。
  该工具经过差异化改进,针对实际使用场景优化了实用性。Use when 用户需要区块链安全扫描专业版相关功能时使用。不适用于超出本技能能力范围的复杂需求。
tags:
- 安全
- 区块链
- DeFi
- 企业版
- 交易模拟
- 加密
- 工具
- sarif
- chain_id
- address
tools:
- read
- exec
homepage: ''
category: Security
homepage: ""
pricing_tier: "L2-标准级"
---
> **核心功能**: 本技能提供中文交互、化工作流场景等能力。
# 区块链安全扫描专业版
## 总览
专业版为DeFi团队、机构交易者和安全审计人员提供企业级区块链安全检查能力。在免费版地址检查与代币检测的基础上,新增交易模拟、批量地址筛查、多链深度扫描、SARIF/HTML报告导出、Webhook实时告警等高级功能。专业版完全兼容免费版接口,已有免费版集成可无缝升级.
### 专业版核心优势
| 优势 | 说明 |
|---|---|
| 交易模拟 | 在链上执行前模拟交易,检测revert、滑点、授权风险 |
| 无限额度 | 不受每日100次限制,支持高频交易场景 |
| 批量操作 | CSV批量导入地址,一次检查数百个地址 |
| 多链覆盖 | 支持15条链及测试网,覆盖全部主流生态 |
| 报告导出 | 生成SARIF/HTML/PDF格式合规报告 |
| 告警推送 | Webhook/邮件实时告警,领先时间发现风险 |
| 高并发 | 10 QPS并发能力,满足批量检查需求 |
| 优先支持 | 专属技术支持通道,SLA保障 |
## 主要能力
### 1. 交易模拟(专业版独有)
在发送真实交易前,模拟交易执行过程,检测潜在revert、异常滑点、恶意授权等风险.
## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 区块链安全扫描专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```bash
curl -s -X POST "https://api.example.com/v1/simulate-tx" \
  -H "Content-Type: application/json" \
  -H "X-Client-Fingerprint: pro-agent-001" \
  -d '{
    "from": "0xYourWalletAddress",
    "to": "0xContractAddress",
    "value": "0",
    "data": "0x095ea7b3000000000000000000000000router0000000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "chain_id": 1
  }' | jq
```
模拟结果包含:
- 交易是否成功执行
- Gas消耗预估
- 状态变更详情
- 授权变更检测
- 潜在风险标记
**处理**: 解析交易模拟(专业版独有)的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回交易模拟(专业版独有)的响应数据,含状态码、结果数据和运行日志.
### 2. 批量地址检查(专业版独有)
通过CSV文件批量导入地址,一次检查数百个地址,适合机构级筛查.
```bash
#!/bin/bash
CHAIN_ID=1
INPUT_FILE="addresses.csv"
OUTPUT_FILE="batch_results.json"
echo "[" > "$OUTPUT_FILE"
FIRST=true
while IFS=',' read -r address label; do
    [ -z "$address" ] && continue
    RESULT=$(curl -s -H "X-Client-Fingerprint: pro-batch" \
        "https://api.example.com/v1/check-address/${address}?chain_id=${CHAIN_ID}")
    RISK=$(echo "$RESULT" | jq -r '.risk_level')
    echo "${label} (${address}): ${RISK}"
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$OUTPUT_FILE"
    fi
    echo "$RESULT" | jq --arg label "$label" '{address: .address, risk: .risk_level, label: $label}' >> "$OUTPUT_FILE"
done < "$INPUT_FILE"
echo "]" >> "$OUTPUT_FILE"
echo "批量检查完成,结果已保存至 ${OUTPUT_FILE}"
```
**处理**: 解析批量地址检查(专业版独有)的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回批量地址检查(专业版独有)的响应数据,含状态码、结果数据和运行日志.
- `input_params`参数控制执行,支持创建/查询/导出
### 3. 地址信誉查询(兼容免费版)
```bash
curl -s -H "X-Client-Fingerprint: pro-agent" \
  "https://api.example.com/v1/check-address/0x742d35Cc6634C0532925a3b844Bc454e4438f44e?chain_id=1&include_history=true" | jq
```
**处理**: 解析地址信誉查询(兼容免费版)的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回地址信誉查询(兼容免费版)的响应数据,含状态码、结果数据和运行日志.
- `input_params`参数控制执行,支持创建/查询/导出
### 4. 代币深度检测(兼容免费版增强)
```bash
curl -s -H "X-Client-Fingerprint: pro-agent" \
  "https://api.example.com/v1/check-item/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48?chain_id=1&deep_scan=true" | jq
```
**处理**: 解析代币深度检测(兼容免费版增强)的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回代币深度检测(兼容免费版增强)的响应数据,含状态码、结果数据和运行日志.
- `input_params`参数控制执行,支持创建/查询/导出
### 5. SARIF报告导出(专业版独有)
生成符合SARIF标准的报告,可直接集成到GitHub代码扫描与CI/CD流水线.
```bash
  -H "Content-Type: application/json" \
  -H "X-Client-Fingerprint: pro-agent" \
  -d '{
    "format": "sarif",
    "checks": [
      {"type": "address", "address": "0x742d35Cc...", "chain_id": 1},
      {"type": "token", "address": "0xA0b86991...", "chain_id": 1}
    ]
  }' -o security_report.sarif
echo "SARIF报告已生成: security_report.sarif"
```
**处理**: 解析SARIF报告导出(专业版独有)的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回SARIF报告导出(专业版独有)的响应数据,含状态码、结果数据和运行日志.
**能力覆盖范围**：本技能覆盖以下场景：企业级区块链安全、支持交易模拟、批量地址检查、多链覆盖、风险报告导出与告、警推送、DeFi、团队与机构用户、区块链安全扫描专、团队与机构用户提、供全方位链上安全、核心能力、交易模拟、多链深度扫描、SARIF、报告导出、Webhook、高并发、API、适用场景、协议安全审计、机构级交易风控、批量地址筛查、安全门禁、差异化、专业版兼容免费版、新增交易模拟、批量操作与企业级、报告能力、满足合规与规模化、适用关键词、区块链安全、批量扫描、风险报告、blockchain、simulate、batch等.
- `input_params`参数控制执行,支持创建/查询/导出
## 使用场景
### 场景一:DeFi协议安全审计
DeFi协议上线前,对涉及的所有合约地址与代币进行全面安全扫描.
```bash
#!/bin/bash
PROTOCOL_NAME="MyDeFiProtocol"
CHAIN_ID=1
CONTRACTS=(
    "0xRouter1...|路由合约"
    "0xPool1...|流动性池"
    "0xToken1...|协议代币"
    "0xOracle1...|价格预言机"
)
echo "============================================"
echo "DeFi协议安全审计: ${PROTOCOL_NAME}"
echo "审计时间: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "============================================"
CRITICAL_COUNT=0
HIGH_COUNT=0
for entry in "${CONTRACTS[@]}"; do
    IFS='|' read -r addr label <<< "$entry"
    ADDR_RESULT=$(curl -s -H "X-Client-Fingerprint: pro-audit" \
xyz/v1/check-address/${addr}?chain_id=${CHAIN_ID}")
    ADDR_RISK=$(echo "$ADDR_RESULT" | jq -r '.risk_level')
    TOKEN_RESULT=$(curl -s -H "X-Client-Fingerprint: pro-audit" \
xyz/v1/check-item/${addr}?chain_id=${CHAIN_ID}")
    TOKEN_RISK=$(echo "$TOKEN_RESULT" | jq -r '.risk_level // "N/A"')
    echo ""
    echo "--- ${label} (${addr}) ---"
    echo "地址风险: ${ADDR_RISK}"
    echo "代币风险: ${TOKEN_RISK}"
    case $ADDR_RISK in
        CRITICAL) ((CRITICAL_COUNT++)) ;;
        HIGH) ((HIGH_COUNT++)) ;;
    esac
done
echo ""
echo "============================================"
echo "审计摘要"
echo "  CRITICAL: ${CRITICAL_COUNT}"
echo "  HIGH: ${HIGH_COUNT}"
echo "============================================"
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "阻止: 存在极高风险合约,协议不可上线"
    exit 1
fi
```
### 场景二:机构级交易风控
机构在执行大额交易前,通过交易模拟与多重检查确保资金安全.
```python
#!/usr/bin/env python3
"""专业版机构级交易风控示例"""
import requests
import json
from datetime import datetime
class BlockchainRiskControl:
    BASE_URL = "https://api.example.com/v1"
    def __init__(self, fingerprint="institutional-pro"):
        self.headers = {
            "X-Client-Fingerprint": fingerprint,
            "Content-Type": "application/json"
        }
        self.blocked = False
        self.warnings = []
    def check_address(self, address, chain_id=1):
        """地址信誉检查"""
        resp = requests.get(
            f"{self.BASE_URL}/check-address/{address}",
            params={"chain_id": chain_id},
            headers=self.headers
        )
        return resp.json()
    def check_token(self, token_address, chain_id=1):
        """代币安全检测"""
            f"{self.BASE_URL}/check-item/{token_address}",
            params={"chain_id": chain_id},
        )
        return resp.json()
    def simulate_transaction(self, from_addr, to_addr, value, data="0x", chain_id=1):
        """交易模拟(专业版独有)"""
        payload = {
            "from": from_addr,
            "to": to_addr,
            "value": str(value),
            "data": data,
            "chain_id": chain_id
        }
            f"{self.BASE_URL}/simulate-tx",
            json=payload,
        )
        return resp.json()
    def pre_trade_check(self, from_addr, to_addr, token_addr, value, chain_id=1):
        """交易前全面风控检查"""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "checks": []
        }
        addr_result = self.check_address(to_addr, chain_id)
        report["checks"].append({
            "check": "address_reputation",
            "risk": addr_result.get("risk_level", "UNKNOWN"),
            "safe": addr_result.get("is_safe", False)
        })
        if addr_result.get("risk_level") in ["HIGH", "CRITICAL"]:
            self.blocked = True
            report["decision"] = "BLOCKED"
            return report
        if token_addr:
            token_result = self.check_token(token_addr, chain_id)
                "check": "token_safety",
                "risk": token_result.get("risk_level", "UNKNOWN"),
                "honeypot": token_result.get("is_honeypot", False)
            })
            if token_result.get("is_honeypot"):
                self.blocked = True
                report["decision"] = "BLOCKED"
                return report
        sim_result = self.simulate_transaction(from_addr, to_addr, value, chain_id=chain_id)
            "check": "transaction_simulation",
            "success": sim_result.get("success", False),
            "gas_estimate": sim_result.get("gas_estimate", 0),
            "revert_reason": sim_result.get("revert_reason", None)
        })
        if not sim_result.get("success"):
            self.blocked = True
            report["decision"] = "BLOCKED"
            return report
        report["decision"] = "ALLOWED"
        return report
if __name__ == "__main__":
    rc = BlockchainRiskControl()
    report = rc.pre_trade_check(
        from_addr="0xYourWallet",
        to_addr="0xContractAddr",
        token_addr="0xTokenAddr",
        value=0,
        chain_id=1
    )
    print(json.dumps(report, indent=2))
```
### 场景三:CI/CD安全门禁
将区块链安全检查集成到CI/CD流水线,作为部署前的安全门禁.
```yaml
name: Blockchain Security Gate
on: [push, pull_request]
jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check contract addresses
        run: |
          CRITICAL=0
          for addr in $(cat contracts.txt); do
            RISK=$(curl -s -H "X-Client-Fingerprint: ci-pro" \
chain_id=1" | jq -r '.risk_level')
            echo "${addr}: ${RISK}"
            if [ "$RISK" = "CRITICAL" ]; then
              CRITICAL=$((CRITICAL + 1))
            fi
          done
          if [ "$CRITICAL" -gt 0 ]; then
            echo "Security gate FAILED: ${CRITICAL} critical findings"
            exit 1
          fi
          echo "Security gate PASSED"
```
## 实操说明
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 从免费版升级
专业版完全兼容免费版接口,仅需更换指纹标识即可启用专业版能力:
```bash
curl -s "https://api.example.com/v1/check-address/0x..."
curl -s -H "X-Client-Fingerprint: pro-agent" \
  "https://aegis402..."
```bash
# 在此执行相关操作
echo "操作完成"
```bash
xyz/v1/simulate-tx" \
  -H "Content-Type: application/json" \
  -H "X-Client-Fingerprint: pro-agent" \
  -d '{
    "from": "0xSender...",
    "to": "0xRecipient...",
    "value": "1000000000000000000",
    "data": "0x",
    "chain_id": 1
  }' | jq
```
**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 配置示例
### Webhook告警配置
```json
{
  "webhook": {
    "url": "https://your-alert-server.com/webhook",
    "events": ["CRITICAL", "HIGH"],
    "retry_count": 3,
    "timeout_seconds": 10
  }
}
```bash
# 在此执行相关操作
echo "操作完成"
```csv
address,label,chain_id
0x742d35Cc6634C0532925a3b844Bc454e4438f44e,主要合约,1
0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48,USDC代币,1
0xdAC17F958D2ee523a2206206994597C13D831ec7,USDT代币,1
```
### 专业版支持的链(15条)
| 链名称 | Chain ID | 地址检查 | 代币检查 | 交易模拟 |
|---:|---:|---:|---:|---:|
| Ethereum | 1 | 支持 | 支持 | 支持 |
| Base | 8453 | 支持 | 支持 | 支持 |
| Polygon | 137 | 支持 | 支持 | 支持 |
| Arbitrum | 42161 | 支持 | 支持 | 支持 |
| Optimism | 10 | 支持 | 支持 | 支持 |
| BSC | 56 | 支持 | 支持 | 支持 |
| Avalanche | 43114 | 支持 | 支持 | 支持 |
| Solana | solana | 支持 | 支持 | 不适用 |
| Fantom | 250 | 支持 | 支持 | 支持 |
| Linea | 59144 | 支持 | 支持 | 支持 |
| Scroll | 534352 | 支持 | 支持 | 支持 |
| Mantle | 5000 | 支持 | 支持 | 支持 |
| Sepolia(测试网) | 11155111 | 支持 | 支持 | 支持 |
| Base Sepolia | 84532 | 支持 | 支持 | 支持 |
| Holesky(测试网) | 17000 | 支持 | 支持 | 支持 |
## 推荐做法
1. **三层检查**:对每笔交易执行地址检查、代币检查、交易模拟三层验证.
2. **批量筛查**:使用CSV批量检查功能,定期筛查协议涉及的全部地址.
3. **CI/CD集成**:将SARIF报告集成到代码扫描流水线,实现自动化安全门禁.
4. **告警配置**:配置Webhook告警,在检测到CRITICAL风险时领先时间通知团队.
5. **额度监控**:专业版虽然无限制,仍建议监控API使用量,优化调用效率.
6. **报告归档**:定期导出HTML/PDF报告,满足合规审计要求.
## 热门问题
### Q1: 专业版与免费版接口是否兼容?
完全兼容。专业版使用相同的API端点,仅需在请求头中使用专业版指纹标识即可启用高级功能。已有免费版集成代码无需修改.
### Q2: 交易模拟会消耗Gas吗?
不会。交易模拟在沙盒环境中执行,不会广播到链上,不消耗真实Gas费用.
### 已知限制
专业版单次批量检查建议不超过500个地址,超过时可分批执行。API并发限制为10 QPS.

... (更多问答请参考完整文档)

## 环境要求
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问 `https://api.example.com`
- **Python**: 3.8+(使用Python风控脚本时需要)
### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| curl | 命令行工具 | 必需 | 系统自带或包管理器安装 |
| jq | JSON处理工具 | 推荐 | `apt install jq` / `brew install jq` |
| python3 | 运行时环境 | 可选 | python.org 下载 |
| requests | Python库 | 可选 | `pip install requests` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
### API Key 配置
- 专业版使用 `X-Client-Fingerprint` 头标识专业版身份
- 建议使用专属指纹标识,如 `pro-agent-{team-name}`
- 交易模拟与批量检查功能需专业版指纹
### 可用性分类
- **分类**: MD+EXEC模式纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行企业级区块链安全检查与交易模拟任务
- API Key通过环境变量配置: export API_KEY=your_key
## 异常处理策略
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 安全守则
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量传入,不在代码中硬编码 |
| 命令执行风险 | 命令执行受白名单约束,避免注入用户输入 |
| 网络通信安全 | 通信使用HTTPS并校验证书有效性 |
| 敏感数据暴露 | 输出不含敏感凭据 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 疑问速答
### Q1: 区块链安全扫描专业版支持哪些输入格式？
A1: 企业级区块链安全工具,支持交易模拟、批量地址检查、多链覆盖、风险报告导出与告警推送,适合DeFi团队与机构用户.。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 即刻上手
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
