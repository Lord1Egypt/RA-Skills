---
name: crypto-morning-briefing
description: "Generate structured crypto market morning briefing via public web search. Get latest market overview, key asset trends, macro/regulatory news, risk warnings, and information sources. No API key required."
homepage: https://github.com/openclaw/openclaw/tree/main/skills/crypto-morning-briefing
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["curl", "jq"] },
        "install":
          [
            {
              "id": "system-deps",
              "kind": "shell",
              "command": "apt-get update && apt-get install -y curl jq",
              "bins": ["curl", "jq"],
              "label": "Install curl and jq",
            },
          ],
      },
  }
---

# 加密货币市场晨报 Skill

基于公开网页检索和公开加密货币数据接口，生成最新的结构化加密货币市场晨报。

## 适用场景 ✅

- "生成今日加密货币市场晨报"
- "最新加密货币市场情况"
- "加密货币宏观监管最新消息"
- "加密货币市场风险提示"

## 不适用场景 ❌

- 历史行情回测/深度量化分析 → 使用专业量化平台
- 专业投资建议 → 本skill仅做信息汇总，不构成投资建议
- 实时逐笔交易数据 → 使用交易所原生接口
- 非加密货币类金融市场简报 → 使用对应金融skill

## 输出字段说明

所有输出严格包含以下结构化字段：
1. **市场概览**：整体市值、24小时涨跌幅、全网交易活跃度、多头/空头占比
2. **重点资产动态**：BTC、ETH等主流资产的24小时价格表现、大额异动、链上数据
3. **宏观/监管消息**：全球最新宏观政策、监管动态、行业重大事件
4. **风险提示**：市场波动风险、监管风险、技术风险提示
5. **信息来源**：所有信息对应的公开来源链接/名称

## 调用命令

### 生成最新结构化晨报
```bash
/root/.openclaw/workspace/skills/crypto-morning-briefing/run.sh
```

### 仅返回JSON格式结果
```bash
/root/.openclaw/workspace/skills/crypto-morning-briefing/run.sh --json
```

## 实现逻辑
1. 从CoinGecko公开API获取全局市场概览和主流资产数据
2. 调用公开网页检索获取最近24小时加密货币相关新闻和监管消息
3. 自动过滤低质量信息，整理为规范结构化字段
4. 标注所有信息来源，确保可追溯

## 注意事项
- 所有数据来自公开免费接口，存在最多15分钟延迟
- 本skill输出仅为信息汇总，不构成任何投资建议
- 速率限制：每小时最多调用10次，避免触发公开接口限流
