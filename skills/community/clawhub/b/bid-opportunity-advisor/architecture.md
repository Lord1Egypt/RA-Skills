# 架构草案：bid-opportunity-advisor

## 设计原则（来自用户需求优先级）

1. 可信判决 > 数据量 > 图表美观
2. 对齐「我的公司」> 泛泛市场分析
3. 开箱即用、尊重隐私 > 自动代理
4. 诚实标注数据边界 > 假装严谨

## 分层架构

```
┌─────────────────────────────────────────────┐
│  输入层  │ 用户提问 + 公司画像(~/.bidprofile.json) │
├─────────────────────────────────────────────┤
│  数据接入层  │ agent WebFetch/Bash 取原始HTML落盘    │
│             │ + fetch_ccgp.py(ccgp) / fetch_ceb.py(ceb,--merge并入) 解析 │
│             │ + cebpubservice(bulletin子站) + WebSearch兜底 │
│             │ 取数后先报 N条/覆盖/缺失              │
├─────────────────────────────────────────────┤
│  画像匹配层  │ fit评分: 产品/地域/规模/资质          │
├─────────────────────────────────────────────┤
│  决策引擎层  │ 机会评分(真实regional) + 置信度       │
│             │ + Go/No-Go + 竞品定价空间            │
├─────────────────────────────────────────────┤
│  输出层  │ 对话态(判决+清单) / 可选HTML(自包含SVG)  │
└─────────────────────────────────────────────┘
```

## 关键设计决策

- **数据源默认免费公开源（实测可用）**：主路径由 **agent 用 WebFetch/Bash 取原始 HTML 落盘**，`scripts/fetch_ccgp.py`（ccgp 源）与 `scripts/fetch_ceb.py`（cebpubservice / 省级平台源）仅解析、不擅自联网；`fetch_ceb.py` 用 `--merge` 把 ceb 解析结果并入 ccgp 记录再交引擎统一去重。ccgp 详情页补金额/供应商/评分；工程建设类走 cebpubservice 的 bulletin 子站；WebSearch 作跨源兜底（返回全文更细）。`--kw` 直连 bxsearch 为离线补充（可能限流），非主推。商业 API Key 为可选增强。详见 `references/data_sources.md`。
- **无静默自动注册**：凭证靠用户显式配置（环境变量/文件）。任何需要第三方账号的动作先问。
- **公司画像被动读取**：仅当用户显式创建 `~/.bidprofile.json` 才用，绝不自动生成或落盘。
- **图表自包含**：HTML 报告用内联 SVG 绘制，不引外部 CDN（离线可看、无外链追踪）。
- **置信度贯穿**：样本薄→置信低→建议试水，不伪造。

## 文件布局

```
bid-opportunity-advisor/
├── SKILL.md
├── manifest.yaml
├── README.md
├── references/
│   ├── decision_framework.md
│   └── data_sources.md
├── architecture.md
└── scripts/
    ├── fetch_ccgp.py
    ├── fetch_ceb.py
    ├── make_profile.py
    ├── selftest.py
    └── opportunity_engine.py
```
