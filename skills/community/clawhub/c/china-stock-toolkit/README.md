# 🌍 全球市场实时仪表盘 - ClawHub Skill

> 一个技能看遍全球市场：A股、港股、美股、贵金属、外汇，全在同一个仪表盘里。

## 🔗 安装

```bash
clawhub install china-stock-toolkit
```

或

```bash
npx clawhub@latest install china-stock-toolkit
```

## ✨ 为什么选择这个技能？

### 🚀 开箱即用，零配置

不需要任何 API Key，安装后直接用：
- 🇨🇳 A股大盘指数（上证/深证/创业板/科创50/北证50）
- 🇭🇰 港股恒生指数
- 💰 贵金属实时行情（黄金/白银）
- 📈 A股个股实时查询（如贵州茅台、比亚迪等）

```bash
# 安装后直接问：
"今天A股怎么样？"
→ 自动展示5大指数实时数据

"黄金现在什么价？"
→ 黄金XAU 4631.68美元 -1.07%
```

### 🎨 漂亮的图形化仪表盘

内置零CDN依赖的 HTML 仪表盘，脱离 Agent 也能独立使用：
- 🔴🟢 红涨绿跌（符合A股投资者习惯）
- 🌙 暗色主题，护眼舒适
- 📱 响应式布局，手机电脑都能用
- 🔄 多市场一键切换

### 🔌 你自己的数据，你做主

不只是免费数据！支持用户自定义数据源：
- 接入 Yahoo Finance → 看美股、日经225、韩国KOSPI
- 接入 Alpha Vantage → 看外汇、商品期货
- 配置 HTTP 代理 → 解锁更多被墙数据源

```yaml
# ~/.config/stock-toolkit/config.yaml
datasources:
  yahoo_finance:
    api_key: "your_key"
  proxy:
    http: "http://127.0.0.1:7890"
```

### 🔄 多源聚合 + 交叉验证

同一份数据，三个来源交叉验证，确保可靠性：

```
查询上证指数：
  腾讯财经 → 4078.64
  新浪财经 → 4078.60
  东方财富 → 4078.65
  ──────────────────
  结果：4078.64 ✅ 多数一致，可信度高
```

### 🧮 内置交易税费计算器

精确计算 A 股交易费用，自动代入当前价格：
- 印花税（卖出千分之0.5）
- 佣金（默认万分之三，可自定义）
- 过户费（十万分之一）
- 一键计算盈亏和收益率

### 📈 个股详情分析

点击任意股票，查看多维度数据：
- 实时行情（价格/涨跌幅/成交量）
- 日内高低价
- 成交额
- 结合税费计算器，一键算"如果现在卖能赚多少"

## 🌍 支持的市场

| 市场 | 数据 | 状态 |
|------|------|------|
| 🇨🇳 A股指数 | 上证/深证/创业板/科创50/北证50 | ✅ 开箱即用 |
| 🇭🇰 港股 | 恒生指数 | ✅ 开箱即用 |
| 💰 贵金属 | 黄金/白银 | ✅ 开箱即用 |
| 🇺🇸 美股 | 道琼斯/纳斯达克/标普500 | 🔧 需配置 |
| 🌏 日韩 | 日经225/韩国KOSPI | 🔧 需配置 |
| 💱 外汇 | 美元/人民币等 | 🔧 需配置 |

## 💻 使用示例

```bash
# 查看所有市场
python scripts/stock_toolkit.py --action all

# 查看A股指数
python scripts/stock_toolkit.py --action indices

# 查看个股
python scripts/stock_toolkit.py --action stock --code sh600519

# 税费计算
python scripts/stock_toolkit.py --action calc_tax --buy_price 1800 --sell_price 1850 --volume 100
```

## 🔗 链接

- **ClawHub:** https://clawhub.ai/darbling/china-stock-toolkit
- **GitHub:** https://github.com/darbling/clawhub-skills
- **作者:** Lin Hui

## 📜 License

MIT License - 自由使用、修改、分发

---

*⚠️ 免责声明：本工具仅供学习研究，不构成任何投资建议。投资有风险，入市需谨慎。*
