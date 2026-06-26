# alpha-pulse — A股次日短线收益最大化信号引擎

> 🤖 由 Jarvis 构建 | 专为 T+1 短线交易设计 | 每日收盘后自动生成 30 只高潜力标的

## ✅ 核心能力
| 命令 | 作用 |
|------|------|
| `alpha-pulse scan` | 扫描全市场（~5000只股票），计算10+短线动因因子 |
| `alpha-pulse predict` | 输出次日涨幅概率 Top 30 股票（含信号分、动因摘要） |
| `alpha-pulse report` | 生成 Markdown 报告 + CSV + 图表（可自动打开） |
| `alpha-pulse notify` | 推送信号至 Windows 弹窗/剪贴板/语音 |

## 🔬 短线动因因子（T+1 专属）
1. **资金面**：龙虎榜净买入强度、北向尾盘30分钟流入占比
2. **量价面**：量比 > 3.0 + 涨停封单/成交额 > 0.5
3. **技术面**：5日线上穿10日线 + RSI(6) 从30以下拐头向上
4. **消息面**：当日公告关键词（重组/订单/新品）+ 股吧热度突增
5. **情绪面**：融资余额环比增长 > 2% + 融券余额下降

## 🛡️ 风控规则（自动启用）
- 排除 ST/*ST、*退市风险警示
- 流通市值 < 50亿元 → 过滤
- 单行业持仓 ≤ 3 只（防行业黑天鹅）
- 信号分 < 70 → 不入选

## 📁 目录结构
```
skills/alpha-pulse/
├── SKILL.md
├── lib/
│   ├── __init__.py
│   ├── scanner.py      # 数据获取（akshare 优先）
│   ├── factors.py      # 因子计算（向量化，高效）
│   ├── predictor.py    # 概率模型（含 demo 训练脚本）
│   └── filter.py       # 熔断逻辑
├── config.yaml         # 日期、阈值、token
└── examples/
    └── run_tomorrow.py # 主入口：今日收盘后运行，输出明日信号
```

## ⚙️ 首次使用
1. 安装依赖：`pip install akshare pandas numpy xgboost`
2. （可选）配置 tushare token（提升龙虎榜数据质量）
3. 每日 15:30 后运行：`python skills/alpha-pulse/examples/run_tomorrow.py`

> 💡 提示：你只需说 `alpha-pulse predict`，我就会调用此技能生成信号。

---
**下一步**：我将立即创建 `config.yaml` 和 `lib/scanner.py` 骨架。  
你无需操作——除非你想调整某条风控规则或因子权重

继续？  
✅ 回复“继续” 或 “custom [需求]”