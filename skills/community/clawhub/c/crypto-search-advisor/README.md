# 加密货币零翻墙拆解

🛡️ 国内直连·截图+搜索交叉验证加密货币行情助手

## 特性

- ✅ **国内直连**：无需VPN
- ✅ **零付费**：免费使用，无需API Key
- ✅ **交叉验证**：截图识别 + 搜索聚合
- ✅ **多模分析**：稳定币锚定·主流币结构·山寨币流动性·Meme币情绪·大宗商品宏观·股票代币基本面
- ✅ **安全边界**：不代操、不存资产、不预测价格

## 安装

```bash
# 通过 ClawHub 安装（推荐）
clawhub install crypto-search-advisor

# 安装依赖
cd crypto-search-advisor
pip install -r requirements.txt
```

## 使用方式

安装后，直接发送交易所截图给 Agent 即可自动分析。Agent 会自动：

1. 识别截图中的币种和价格
2. 联网搜索交叉验证
3. 秒级输出风险预警（Quick Scan）
4. 异步补发深度分析

也可以文字询问任意币种：
- "BTC 现在什么情况？"
- "帮我看看 USDT 稳不稳定"
- "PEPE 会不会 dump？"

## 测试

```bash
cd scripts
pytest tests/ -v
```

## 文档

- [SKILL.md](SKILL.md) - 完整使用文档（Agent 必读）
- [RULES.md](RULES.md) - 核心规则
- [FORMAT.md](FORMAT.md) - 输出格式规范
- [EXAMPLES.md](EXAMPLES.md) - 示例
- [ARCHITECTURE.md](ARCHITECTURE.md) - 工程架构

## 许可证

MIT-0
