# 电商运营决策台（ecommerce-ops-cockpit）

国内外电商全链路决策 Skill：**用真实数据算出唯一答案，用专家团队交叉验证，用脚本锁死口径，用剧本给打法，用图表化 PDF 交付。**

- **国内**：淘宝 / 天猫 / 京东 / 拼多多 / 抖店 / 小红书 / 快手小店 / 微信小店
- **跨境**：Amazon / eBay / Walmart / Shopee / Lazada / TikTok Shop(海外) / Temu / SHEIN / AliExpress / Shopify 独立站

> 零依赖：全部脚本只用 Python 标准库，无需 pip 安装。

---

## 它能做什么

| 能力 | 脚本 |
|---|---|
| 选品评估与竞品分析（六维评分 → 做/不做） | `selection_eval.py` |
| 定价、真实利润、保本售价、保本 ROI、最高出价、目标 ROI 反推 | `profit_roi.py` |
| **跨境到岸成本**：头程/关税/VAT/FBA/出口退税/汇率敏感性 | `landed_cost.py` |
| 变化归因：GMV 涨跌拆成**价格 / 销量 / 结构**三分量 + 毛利桥 | `margin_bridge.py` |
| 漏斗诊断：有流量不出单 / 转化下滑 / ROI 上不去 | `funnel_diagnose.py` |
| 多平台运营周报：汇总 / 环比 / 异常标记 | `weekly_report.py` |
| 批量改价上下架 **dry-run 预演**（风险标记，只预览不执行） | `batch_plan.py` |
| 结算单对账：C1–C9 九类异常，每条给金额影响 | `settlement_audit.py` |
| 违禁词 / 极限词 / 广告法合规检测 | `copy_compliance.py` |
| 来源四档标注 + 分项置信度 + 交付闸门 | `confidence.py` |
| 交付前数据验真（关卡①） | `data_verify.py` |
| 图表化 PDF 报告生成 + 九项验真 | `report_pdf.py` / `pdf_verify.py` |

## 快速开始

```bash
# 1. 全量自检（改动后必跑）
python3 tests/run_all.py

# 2. 定价 / 利润 / 保本 ROI
python3 scripts/profit_roi.py --params params.json

# 3. 跨境到岸成本（含关税/VAT/汇率敏感性）
python3 scripts/landed_cost.py --data cross_border.json

# 4. GMV 跌了？归因到价格/销量/结构
python3 scripts/margin_bridge.py --data monthly.json

# 5. 数据类脚本可直接产出图表 spec，再生成 PDF 并验真
python3 scripts/landed_cost.py --data cb.json --spec-out spec.json
python3 scripts/report_pdf.py --spec spec.json --out report.pdf
python3 scripts/pdf_verify.py --pdf report.pdf --pages 2 --charts 2 --tables 2 --expect-text "净利"
```

每个脚本都支持 `--self-test` 与 `--json`，退出码语义统一（见下）。

## 目录结构

```
ecommerce-ops-cockpit/
├── SKILL.md                  # 主文件：边界 / 路由 / 铁律 R1–R27 / 交付关卡
├── README.md
├── LICENSE                   # MIT
├── assets/forbidden_words.json   # 广告法违禁词库（P0/P1/P2 + 豁免短语）
├── scripts/                  # 14 个零依赖脚本（各自带 --self-test）
├── references/               # 参考文档（分层加载：入门 / 按场景 / 排查）
│   ├── overseas-platforms.md     # 跨境：10 个海外平台费率·物流·流量·合规
│   ├── cross-border-costs.md     # 跨境：头程·关税·VAT·FBA·退税·退货
│   ├── playbooks.md              # 10 个场景剧本（新品/不出单/断货/清仓…）
│   ├── glossary.md               # 国内外术语与口径表
│   ├── experts.md                # 专家团队角色卡（含跨境 E5）
│   ├── quality-gates.md          # 来源分级·退出码·引导话术·降级链
│   └── ...（平台流量 / 定价 / 投放 / 文案 / 对账 / 节奏 / 报告规范）
└── tests/run_all.py          # 全量自检
```

## 设计原则

- **真实数据唯一**：缺数据写 `DATA_MISSING`，禁止用行业均值/经验值填补
- **数值一律脚本算**：金额、ROI、保本价不得心算，公式以脚本内恒等式为准
- **口径写死**：转化率用支付买家数；ROAS/ROI 同源同窗口，禁止平台与广告后台混算
- **来源可核验**：每个数字标 S1 原始 / S2 单方 / S3 公开 / S4 推算；推算值不作决策主证据
- **变化必须归因**：不只报"环比 -2%"，要拆成价格 / 销量 / 结构（R24）
- **数据结论配图**：数据类脚本支持 `--spec-out` 直接产出图表 spec（R27）
- **不可逆先确认**：批量改价/上下架先 dry-run 预演，P0 清零才谈执行（R25）；拒绝后不绕道
- **不测不发**：14 个脚本全带自测，`tests/run_all.py` 汇总

## 退出码约定

| 退出码 | 含义 |
|---|---|
| 0 | 正常 / 无严重问题 |
| 1 | **检出问题**（对账 P0、命中违禁词、预演有 P0、置信度未达标）——业务发现，非程序故障 |
| 2 | 输入错误（文件不存在 / JSON 解析失败 / 缺字段） |

> 注意：退出码 1 是"正确检出问题"，不要当成 bug 去"修好"。

## 边界（明确不做）

- 不代客登录店铺后台、不执行平台操作——只出方案与预览
- **不协助低报货值、虚报、拆单避税**（跨境高危，会让店铺与公司一起出事）
- 不提供刷单刷评、不协助规避平台规则、不承诺销量与收益
- 不适用：纯编程开发、剪辑配音、法律税务文书、金融投资分析

## 环境要求

- Python 3.8+（仅用标准库）
- PDF 中文字体：脚本自动从系统字体目录选取（Windows 常见 `C:/Windows/Fonts/simhei.ttf`）
- 临时目录可用环境变量 `ECOMMERCE_OPS_TMP` 指定（默认尽量不写系统盘）

## License

MIT
