# deep-investment-research

系统化投研能力中枢 —— 可复用的投资研究方法论 + 多源一手数据采集工具，作为 OpenClaw Agent Skill 使用。

完整能力与用法见 [SKILL.md](./SKILL.md)；方法论框架在 `methodology/`，数据采集脚本在 `scripts/`。

**定位**：纯研究 —— 产出判断、依据、风险、赔率结构与可选路径；不做盯盘/交易信号/交易执行。

## 7 类研究框架
宏观 · 行业 · 公司研究（看懂生意）· 个股深度研究（投资判断）· 政策 · 投资可行性 · 风险 · 投资规划

## 研究内核
9 红线 · 命门变量聚焦（2-3个+70%火力）· 5步法(A→B→C→D) · 七棱镜多维扫描 · 反共识引擎 · 非对称赔率(上下比+期望值+敏感性测试) · 反证5问 · 质量门控

## 依赖
- 必需：`python3`
- 数据脚本（可选）：yfinance / akshare / fredapi 等；API key 读环境变量（FINNHUB_API_KEY / FRED_API_KEY），未设置则跳过该源
- 联网搜索（可选软依赖）：优先 web-search-plus / tavily skill，未装则降级用内置 web_search

## 可配置环境变量（均带默认值）
| 变量 | 默认值 |
|------|--------|
| `RESEARCH_OUTPUT_DIR` | `~/research-output` |
| `RESEARCH_DATA_ROOT` | `~/research-data` |
| `SEARCH_SKILL_PATH` | `~/.openclaw/skills/web-search-plus/scripts/search.py` |

## 许可
MIT，见 [LICENSE](./LICENSE)。
