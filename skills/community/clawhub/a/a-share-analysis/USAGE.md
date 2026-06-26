# A 股专业分析系统 - 使用说明

**版本**: 2.0 专业版  
**更新日期**: 2026-03-01

---

## 🚀 快速开始

### 基本用法

```bash
cd C:\Users\fj\.openclaw\workspace\skills\a-share-analysis\scripts

# 分析单只股票
python analyze_stock_pro.py 603258 电魂网络

# 分析贵州茅台
python analyze_stock_pro.py 600519 贵州茅台

# JSON 输出（程序调用）
python analyze_stock_pro.py 600519 贵州茅台 --json
```

---

## 📊 系统功能

### 1. 实时行情获取
- **数据源**: 新浪财经 API（免费）
- **支持**: 上海/深圳市场股票
- **数据**: 价格、涨跌幅、成交量、成交额等

### 2. 技术分析（免费数据源）
- **数据源**: 东方财富网（免费）
- **指标**:
  - MA 均线（5/10/20/60 日）
  - MACD（DIF/DEA/MACD 柱）
  - RSI 相对强弱指标
  - 成交量比
  - 支撑位/阻力位
- **信号**: 多头/空头/中性

### 3. 新闻情绪分析
- **数据源**: Firecrawl 网页抓取
- **功能**: 
  - 自动抓取财经新闻
  - AI 情绪分析（看多/看空/中性）
  - 情绪评分（0-1）

### 4. 历史记忆存储
- **系统**: Elite Long-term Memory
- **存储位置**:
  - `memory/YYYY-MM-DD.md` - 每日日志
  - `memory/a-share/{code}.json` - 股票历史
  - `SESSION-STATE.md` - 活跃上下文
  - `MEMORY.md` - 重要分析归档

### 5. 专业报告生成
- **格式**: 固定模板，ASCII 美化边框
- **内容**:
  - 核心摘要（综合评分 0-10 分）
  - 实时行情
  - 技术分析详情
  - 新闻情绪分析
  - 历史分析回顾
  - 投资建议（目标价/止损价）
  - 风险提示

---

## 📁 文件结构

```
a-share-analysis/
├── scripts/
│   ├── analyze_stock_pro.py        # 主入口（专业版）
│   ├── fetch_realtime_data.py      # 实时行情（新浪财经）
│   ├── fetch_technical_indicators_free.py  # 技术分析（东方财富）
│   ├── fetch_news_sentiment.py     # 新闻情绪（Firecrawl）
│   ├── memory_store.py             # 记忆存储（Elite Memory）
│   ├── generate_report_pro.py      # 专业报告生成
│   └── firecrawl_auto_auth.py      # Firecrawl 自动认证
├── a-share-reports/                 # 报告输出目录
└── memory/
    ├── YYYY-MM-DD.md               # 每日日志
    └── a-share/                     # 股票历史
        └── {code}.json             # 个股分析历史
```

---

## 🔧 配置说明

### 1. Firecrawl 认证（可选）

Firecrawl 用于新闻情绪分析，未认证时自动跳过。

**自动认证**:
```bash
python firecrawl_auto_auth.py
```

**手动认证**:
```bash
# 方法 1: 浏览器认证
firecrawl login --browser

# 方法 2: 设置环境变量
setx FIRECRAWL_API_KEY "your-api-key"
```

**免费 API 密钥**:
- 访问 https://www.firecrawl.dev/app
- 注册免费账户
- 获取 API 密钥（有免费额度）

### 2. Elite Memory 配置

在 `~/.openclaw/openclaw.json` 中启用：

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai"
  },
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "enabled": true
      }
    }
  }
}
```

---

## 📊 报告示例

### 综合评分系统

| 评分 | 等级 | 建议 |
|------|------|------|
| 8-10 | ★★★ | 强烈推荐 |
| 6-8  | ★★☆ | 推荐 |
| 4-6  | ★☆☆ | 观望 |
| 2-4  | ☆☆☆ | 谨慎 |
| 0-2  | ☆☆☆ | 回避 |

### 报告内容

```
╔══════════════════════════════════════════════════════════════╗
║           A 股专业分析报告                                   ║
╠══════════════════════════════════════════════════════════════╣
║  股票名称：电魂网络                                ║
║  股票代码：603258                                  ║
║  分析时间：2026-03-01 10:31:16                       ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│                    ★ 核心摘要                                │
├──────────────────────────────────────────────────────────────┤
│  当前价格：¥     19.11   涨跌幅：   +1.22%                  │
│  技术信号：   neutral   趋势：   neutral                    │
│  综合评分：  5.0 / 10  观望                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 使用场景

### 场景 1: 日常股票分析
```bash
python analyze_stock_pro.py 600519 贵州茅台
```
→ 生成完整分析报告，存储历史记录

### 场景 2: 批量分析
```bash
# 创建批处理文件
echo 600519 贵州茅台 >> stocks.txt
echo 000858 五粮液 >> stocks.txt
echo 603258 电魂网络 >> stocks.txt

# 批量分析
for /f "tokens=1,2" %a in (stocks.txt) do python analyze_stock_pro.py %a %b
```

### 场景 3: 程序调用
```python
import subprocess
import json

result = subprocess.run(
    ["python", "analyze_stock_pro.py", "600519", "贵州茅台", "--json"],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

data = json.loads(result.stdout.split("JSON 输出:")[1])
print(f"综合建议：{data['recommendation']}")
```

---

## ⚠️ 注意事项

### 数据源说明
1. **实时行情**: 新浪财经 API，可能有 1-2 秒延迟
2. **技术指标**: 东方财富网，免费数据源
3. **新闻情绪**: Firecrawl，需要 API 认证

### 投资风险提示
- 本报告仅供参考，不构成投资建议
- 股市有风险，投资需谨慎
- 请结合个人风险承受能力做出决策

### 技术限制
- 技术分析基于历史数据，不保证未来表现
- 新闻情绪分析基于公开信息，可能存在滞后
- 综合评分为算法生成，仅供参考

---

## 🔍 常见问题

### Q: Firecrawl 认证失败？
A: 可以跳过，系统会自动使用简化分析模式。

### Q: 技术分析数据获取失败？
A: 检查网络连接，东方财富 API 可能需要稳定网络。

### Q: 如何查看历史分析？
A: 查看 `memory/a-share/{code}.json` 文件。

### Q: 如何自定义报告模板？
A: 修改 `generate_report_pro.py` 中的模板函数。

---

## 📝 更新日志

### v2.0 专业版 (2026-03-01)
- ✅ 使用免费技术分析数据源（东方财富）
- ✅ 固定报告格式，ASCII 美化边框
- ✅ 新增综合评分系统（0-10 分）
- ✅ 新增历史分析回顾
- ✅ 新增 Firecrawl 自动认证模块
- ✅ 优化输出编码，解决 Windows 乱码

### v1.0 基础版 (2026-02-27)
- 初始版本，支持基本行情和技术分析

---

## 📞 技术支持

如有问题，请查看：
- 日志文件：`a-share-reports/` 目录
- 记忆文件：`memory/` 目录
- 配置说明：本文档

---

**感谢使用 A 股专业分析系统！**
