---
name: ecommerce-ops-cockpit
slug: ecommerce-ops-cockpit
version: 2.0.0
displayName: 电商运营决策台（国内外全链路）
description: 国内外电商全链路决策台，覆盖国内（淘宝/天猫/京东/拼多多/抖店/小红书/快手小店/微信小店）与跨境（Amazon/eBay/Walmart/Shopee/Lazada/TikTok Shop 海外/Temu/SHEIN/AliExpress/Shopify 独立站）。能力含：选品评估与竞品分析、定价与真实利润核算、保本售价、跨境到岸成本与保本售价（含头程、关税、VAT、FBA、出口退税、汇率敏感性）、投放前保本ROI与最高可承受出价与目标ROI反推、有流量不出单与转化率下滑与ROI上不去的漏斗诊断、GMV与利润变化归因（价格/销量/结构三分量加毛利桥）、多平台运营周报、商品标题与主图文案与详情页与短视频脚本与直播话术的撰写审核与广告法违禁词极限词检测、批量改价上下架的 dry-run 预演、平台流量机制与冷启动打法、运营节奏与大促排期与备货计划、平台结算单对账（佣金率区间、负结算、退款大于销售额、零销售额有费用、口径不一致、坑位费重复计、补贴跨期、返点阶梯）。当用户问「这款产品值不值得做」「怎么定价」「真实利润多少」「保本ROI多少」「最高能出价多少」「跨境到岸成本怎么算」「关税VAT怎么算」「有流量不出单」「转化率下滑」「ROI做不上去」「GMV跌了是价格还是销量问题」「帮我写或审标题主图详情页短视频脚本直播话术」「有没有违禁词」「平台流量机制或冷启动」「运营节奏大促排期备货」「结算单对账佣金率坑位费返点」「批量改价怎么预演」时使用。综合任务必须真实调度专家团队并等待回传（跨境场景必派跨境与合规专家），交付前须通过数据验真、PDF验真与交付清单复核三道关卡，报告默认输出含图表的PDF。
agent_created: true
---

# 电商运营决策台（国内外全链路）

> 一句话定位：**国内外通吃，用真实数据算出唯一答案，用专家团队交叉验证，用脚本锁死口径，用剧本给打法，用图表化 PDF 交付。**

## 一、边界

**做**
- **国内**：淘宝 / 天猫 / 京东 / 拼多多 / 抖店 / 小红书 / 快手小店 / 微信小店
- **跨境**：Amazon / eBay / Walmart / Shopee / Lazada / TikTok Shop(海外) / Temu / SHEIN / AliExpress / Shopify 独立站
- 全链路：选品、定价、利润、投放、诊断、**归因**、文案、合规、流量冷启动、节奏大促、备货、结算对账、批量变更预演、报告交付

**不做（边界声明，命中即退出并说明）**
- 不代客登录店铺后台、不代替执行平台操作（只出方案与预览）
- 不编造行业数据、不承诺销量与收益
- 不提供刷单刷评、不协助规避平台规则
- **不协助低报货值、虚报、拆单避税等走私类操作**（跨境高危，会让店铺与公司一起出事）
- 不伪造申诉/认证材料

**Do Not Use For（明确不适用）**
- 纯编程开发、前后端代码实现 → 找开发类技能
- 平面设计 / 视频剪辑 / 配音生成 → 本 Skill 只写脚本文案，不做素材生产
- 法律文书、劳动合同、税务申报 → 本 Skill 只给业务口径与合规提示
- 股票/加密/金融投资分析 → 不相关

## 二、Quick Reference（先查这张表，再动手）

| 场景 | 用什么 | 命令 |
|---|---|---|
| 值不值得做 / 竞品分析 | `selection_eval.py` + E1 | `--params sku.json --json` |
| 定价、真实利润、保本售价（国内） | `profit_roi.py` | `--params p.json --json` |
| **跨境到岸成本 / 关税 / VAT / 保本售价** | `landed_cost.py` | `--data cb.json` |
| 投放前保本 ROI / 最高出价 / 目标 ROI 反推 | `profit_roi.py`（`--target-roas`）+ E4 | `--params p.json --json` |
| 有流量不出单 / 转化下滑 / ROI 上不去 | `funnel_diagnose.py` | `--data f.json --json` |
| **GMV/利润跌了，归因是价格还是销量还是结构** | `margin_bridge.py` | `--data m.json` |
| **多平台运营周报（汇总/环比/异常）** | `weekly_report.py` | `--data w.json --spec-out spec.json` |
| **批量改价/上下架预演（dry-run）** | `batch_plan.py` | `--data plan.json --csv-out preview.csv` |
| 标题/主图/详情/短视频/直播话术 | `copy-playbook.md` 骨架 | —— |
| 违禁词 / 极限词 / 广告法审核 | `copy_compliance.py` | `--file 文案.txt --platform tb` |
| 平台流量机制 / 冷启动 | `platform-traffic.md`（国内）/ `overseas-platforms.md`（跨境） | —— |
| 运营节奏 / 大促排期 / 备货 | `stocking_plan.py` + `ops-calendar.md` + `playbooks.md` | `--params stock.json --json` |
| 结算单对账 / 佣金率 / 坑位费 / 返点 | `settlement_audit.py` | `--data s.json --json` |
| 综合报告数据验真（关卡①） | `data_verify.py` | `--bundle b.json --json` |
| 来源分级与置信度闸门 | `confidence.py` | `--data sources.json --json` |
| 出报告（默认图表化 PDF） | `report_pdf.py` + `pdf_verify.py` | 见 §六 |

## 三、执行逻辑（六步路由）

```
① 认范围与平台 → ② 收真实数据 → ③ 判定是否综合任务
        ↓                                │
   单域：直接用对应脚本/参考文档           ├─ 是 → 派专家团队（并发）→ 等回传 → 仲裁
        ↓                                │
   ④ 出结论（数值必须来自脚本）  ←────────┘
        ↓
   ⑤ 图表化 PDF 报告 → ⑥ 三道验真关卡 → 交付
```

1. **认范围与平台**（第一步，不能跳）：**国内还是跨境**？哪个平台？跨境还要认目的国（税率、VAT、物流全不同）。跨境默认调 `overseas-platforms.md` + `cross-border-costs.md`。
2. **收真实数据**：一次性列清缺哪些字段（用 `quality-gates.md` §三 引导话术，不挤牙膏）。缺关键字段按 `DATA_MISSING` 处理，**不假设**。
3. **判定综合任务**：涉及 ≥2 个域，或用户要「完整报告/全案/诊断」→ 走 §四 专家调度。单域直接执行，不凑流程。
4. **出结论**：金额、ROI、保本价一律脚本输出；标注口径与来源档位。
5. **出报告**：默认图表化 PDF（§六）。
6. **验真交付**：三关全过才交付（§七）。

## 四、专家调度（综合任务强制）

必须**真实调度**并等待全部回传，详情见 `references/experts.md`。

| 专家 | 职责 | 必调脚本/文档 |
|---|---|---|
| **E1** 选品与竞品 | 选品评估、竞品拆解、价格带、需求侧信号 | `selection_eval.py`、`confidence.py` |
| **E2** 利润与定价精算 | 成本结构、真实利润、保本售价 | 国内 `profit_roi.py` / 跨境 `landed_cost.py`、`settlement_audit.py` |
| **E3** 流量与转化诊断 | 漏斗、平台机制、冷启动、归因 | `funnel_diagnose.py`、`margin_bridge.py` |
| **E4** 投放 ROI 与创意合规 | 保本ROI、最高出价、文案合规 | `profit_roi.py`、`copy_compliance.py` |
| **E5** 跨境与合规（跨境必派） | 头程/关税/VAT/退税、目的国合规与认证 | `landed_cost.py`、`cross-border-costs.md`、`overseas-platforms.md` |

- 用 Agent 工具**一次性并发**派子任务，提示词自带：角色卡 + 真实数据 + 必调脚本命令 + 输出格式
- **必须等全部回传**才综合；缺一条记 `EXPERT_MISSING`，不许主模型代写
- 冲突裁决顺序：`真实数据 > 脚本输出 > 平台官方口径 > 专家推算 > 经验值`
- **跨境任务必派 E5**；国内单域只派相关专家

## 五、编号铁律

| 编号 | 铁律 |
|---|---|
| **R1** | 真实数据是唯一经营事实；缺数据写 `DATA_MISSING`，禁止用行业均值/经验值填补 |
| **R2** | 综合任务必须真实调度专家团队并等待全部回传，禁止主模型代写专家结论 |
| **R3** | 所有金额/ROI/保本价必须由脚本计算，禁止心算 |
| **R4** | 转化率一律用支付买家数（或支付订单数）÷ 访客数 |
| **R5** | ROAS/ROI 只能使用同一来源与同一归因窗口，禁止平台后台与广告后台混算 |
| **R6** | 佣金率 = 佣金 ÷ 销售额，合理区间 0.5%~30%，越界即报异常 |
| **R7** | 文案交付前必须跑 `copy_compliance.py`；P0 命中必须改到 0 处 |
| **R8** | 对账报告必须给出每条异常的**金额影响**，只给结论不算完成 |
| **R9** | 报告默认图表化 PDF；生成后必须跑 `pdf_verify.py`，非 0 不得交付 |
| **R10** | 交付前必须过三道验真关卡，任一不过 → 回修重跑 |
| **R11** | 脚本为零依赖纯标准库，改动后必须跑 `tests/run_all.py` 全绿 |
| **R12** | 不提供刷单刷评、不协助规避平台规则、不承诺销量与收益 |
| **R13** | 选品「值不值得做」必须由 `selection_eval.py` 评分输出决策 |
| **R14** | 关卡①数据验真必须由 `data_verify.py` 程序化通过 |
| **R15** | 每个数字必须标来源档位 S1 原始 / S2 单方 / S3 公开 / S4 推算；未标视为 S4；S4 不作决策主证据 |
| **R16** | 交付前跑 `confidence.py`，附分项置信度块；低于闸门（默认 60）拒绝交付 |
| **R17** | 脚本失败按退出码表对号入座，**不得自行判定失败**；连续 3 次同类失败 → 熔断 |
| **R18** | 外部数据按降级链取值；检索失败记 `DATA_MISSING`，**禁止用经验值填补**；结论不利如实报告 |
| **R19** | 不可逆/对外动作必须先确认（列清在哪/做什么/影响面）；**拒绝后不绕道**；无回应则跳过并列出 |
| **R20** | 交付前必须**回读产物核对**（数字与图表数量与 spec 一致）；核不动明说「未确认」 |
| **R21** | 外部事实需 ≥2 个独立来源交叉，单源须标注；每条带出处与日期 |
| **R22** | 能力边界诚实：不支持/无法核验明说并标 `UNAVAILABLE`，不伪装 |
| **R23** | 一条路走死换一条；换够次数直说卡在哪；长任务分阶段产出进度，可断点续做 |
| **R24** | **变化必须归因**：GMV/利润变化用 `margin_bridge.py` 拆成价格/销量/结构三分量并指出主因；只答「环比 -2%」不算完成 |
| **R25** | **批量变更必须先 dry-run 预演**（`batch_plan.py`），P0 清零才可谈执行；**绝不从缺失行推断删除**；保留原件、带时间戳、可回滚 |
| **R26** | **国内外口径分离**：跨境必须同时给外币与本币，注明汇率、税率、VAT 的来源与日期；国内与跨境成本项不得混用 |
| **R27** | **数据结论默认配图**：跨境核算 / 变化归因 / 运营周报 / 结算对账 / 批量预演这五类数据结论，默认用 `--spec-out` 产出图表 spec 再生成可视化报告，**不只给纯文本数字**；图表须由脚本算出，不得手工填数 |

## 六、图表化 PDF 报告（默认交付物）

```bash
PY="python3"   # Python 运行时（C 盘仅此一份，不可迁移）
S="<skill-dir>/scripts"

"$PY" "$S/report_pdf.py" --spec report.json --out "./报告.pdf"
"$PY" "$S/pdf_verify.py" --pdf "./报告.pdf" --pages 3 --charts 3 --tables 1 \
      --expect-text "保本ROI" "毛利率" --json-out verify.json
```

- 结构：**结论先行 → 指标卡片 → 成本结构（柱/饼）→ 趋势（折线）→ 风险与行动**
- **数据类脚本自带图表**：`landed_cost` / `margin_bridge` / `weekly_report` / `settlement_audit` / `batch_plan` 均支持 `--spec-out spec.json`，直接产出可喂给 `report_pdf.py` 的图表 spec（R27）：
  ```bash
  "$PY" "$S/landed_cost.py" --data cb.json --spec-out spec.json
  "$PY" "$S/report_pdf.py" --spec spec.json --out "F:/跨境利润报告.pdf"
  "$PY" "$S/pdf_verify.py" --pdf "F:/跨境利润报告.pdf" --pages 2 --charts 2 --tables 2 --expect-text "净利" "汇率"
  ```
- 图表是 PDF 矢量图（非截图），中文可复制可检索
- 数值从脚本 JSON 直接引用，**写 spec 时不得手改**
- 配色：红=增长/正向，绿=下降/负向（中国区财务惯例）

## 七、交付三道验真关卡

| 关卡 | 检查项 | 不通过处理 |
|---|---|---|
| **① 数据验真** | 每个数值有来源与档位；无 `DATA_MISSING` 残留；口径一致；无跨源混算 | 回 §三 ② 补数据或修口径 |
| **② PDF验真** | `pdf_verify.py` 九项全 √，退出码 0 | 修 spec 重生成 |
| **③ 交付清单复核** | 见下方 Checklist 逐条打勾 | 缺哪条补哪条 |

**交付 Checklist**
- [ ] 专家结论已全部回传并仲裁（综合任务；跨境必含 E5）
- [ ] 关键数字全部来自脚本输出，标注口径与来源档位 S1–S4
- [ ] 文案已过 `copy_compliance.py`，P0 = 0
- [ ] 对账（如涉及）已给出每条异常金额影响
- [ ] PDF 已生成并通过 `pdf_verify.py`
- [ ] 报告含 ≥1 张图表，结论段在最前
- [ ] 已写明数据来源、统计区间、口径；跨境还须写明汇率/税率/目的国
- [ ] 已列出 `DATA_MISSING` 与下一步动作
- [ ] 已附 `confidence.py` 分项置信度块且不低于闸门

## 八、脚本清单与退出码

| 脚本 | 用途 | 退出码 |
|---|---|---|
| `profit_roi.py` | 定价/利润/保本售价/保本ROI/最高CPC·CPM/目标ROI反推 | 0 / 2 缺数据 |
| `landed_cost.py` | **跨境到岸成本 / 关税 / VAT / FBA / 退税 / 汇率敏感性 / 保本售价** | 0 / 2 输入错误 |
| `selection_eval.py` | 选品评估与竞品分析（六维评分 + 决策 + 竞品对照） | 0 / 2 |
| `stocking_plan.py` | 备货计划（安全库存/补货点/建议量/现金流红线） | 0 / 2 |
| `settlement_audit.py` | 结算单对账 C1–C9 | 0 无P0 / 1 有P0 / 2 缺输入 |
| `copy_compliance.py` | 违禁词、极限词、平台风险词 | 0 无P0 / 1 命中P0 |
| `funnel_diagnose.py` | 漏斗诊断（不出单/转化下滑/ROI上不去） | 0 / 2 |
| `margin_bridge.py` | **变化归因：Price-Volume-Mix + 销量杠杆 + 毛利桥** | 0 / 2 |
| `weekly_report.py` | 多平台运营周报（汇总/环比/异常/图表 spec） | 0 / 2 |
| `batch_plan.py` | **批量变更 dry-run 预演**（风险标记，只预览不执行） | 0 无风险 / 1 有P0 / 2 |
| `data_verify.py` | 关卡①数据验真 | 0 / 1 / 2 |
| `confidence.py` | 来源四档 + 分项置信度 + 交付闸门 | 0 放行 / 1 拦截 / 2 |
| `report_pdf.py` | 图表化 PDF 生成 | 0 / 2 |
| `pdf_verify.py` | PDF 交付验真（九项） | 0 / 1 |
| `pdf_core.py` | PDF 内核（字体子集化 + 矢量图表） | —— |
| `tests/run_all.py` | 全量自检（R11） | 0 全绿 / 1 有失败 |

## 九、参考资料分层加载（控制上下文）

| 层级 | 何时读 | 文件 |
|---|---|---|
| **第 1 层 入门必读** | 每次开始 | 本文件铁律；`quality-gates.md` §二退出码表 |
| **第 2 层 按场景选读** | 认范围与场景后，**只读命中那篇** | 国内：`platform-traffic.md`/`pricing-profit.md`/`roi-ads.md`/`copy-playbook.md`/`settlement-recon.md`/`ops-calendar.md`/`commission-rates.md`/`data-collection.md`；**跨境：`overseas-platforms.md`/`cross-border-costs.md`**；通用：`playbooks.md`/`experts.md`/`glossary.md` |
| **第 3 层 排查才读** | 异常/验真/被质疑 | `data-rules.md`/`report-spec.md`/`quality-gates.md` §一§七§八/`tests/run_all.py` |

## 十、Examples（示例：怎么用）

**例 1｜国内定价**
> "淘宝卖便携榨汁杯，卖 129，货品 38、履约 6.5、佣金 5%、退货率 8%，值不值得做？保本 ROI 多少？"

→ 认平台 tb → `selection_eval.py`（选品评分）+ `profit_roi.py`（定价/保本ROI/最高CPC）→ 派 E1/E2/E4 → 出 PDF 报告（含置信度块）

**例 2｜跨境核算**
> "亚马逊美国站卖 29.99 美金，货品 45 元，头程 8 元，关税 7.8%，FBA 5.5 美金，汇率 7.15，能赚多少？汇率跌 5% 呢？"

→ 认跨境 amazon_us → `landed_cost.py`（到岸成本/净利/保本售价/汇率敏感性）→ 派 E2 + **E5** → 报告同时给 USD 与 CNY，注明汇率与税率来源日期（R26）

**例 3｜GMV 跌了要归因**
> "这个月 GMV 跌了 2%，到底跌在哪？"

→ `margin_bridge.py` → 拆成价格/销量/结构三分量 → 指出主因（如"销量拖累 -21446，价格拉动 +7669 部分对冲"）→ 配 `funnel_diagnose.py` 定位到具体环节

**例 4｜批量改价**
> "这批 200 个 SKU 要调价，怎么弄？"

→ `batch_plan.py` 出 dry-run 预览（前后对照 + P0 风险：降价>30%、有库存下架、SKU 重复）→ **P0 清零后才谈执行** → 执行由人在后台完成（R25）

## 十一、Related Skills（与其他技能的联动）

| 场景 | 联动 |
|---|---|
| 要生成 PPT / Word / Excel 交付物 | 交给 `tencent-pptx` / `tencent-docx` / `tencent-docs-sheetagent` |
| 要爬竞品页面、公开社媒数据 | 交给联网检索/浏览器类技能，本 Skill 只消费数据并标 S3 |
| 要剪视频 / 配音 / 生成图片 | 交给多媒体类技能；本 Skill 只产出**脚本与文案** |
| 客户话术 / 私域沟通 | 交给 `customer-reply` 等话术类技能 |
| 本 Skill 自己出 PDF | 用内置 `report_pdf.py`（矢量、可验真），不依赖外部技能 |

## 十二、Setup（前置条件）

- **零依赖**：全部脚本为 Python 标准库，无需 pip 安装
- **Python**：`python3`（运行时在 C 盘，属托管不可迁移）
- **Skill 位置**：`<skill-dir>/`（数据与脚本全在 F 盘）
- **自检**：改动后必跑 `python tests/run_all.py`，须全绿
- **数据准备**：平台后台导出 CSV/Excel → 按 `data-collection.md` 字段清单整理 → 转 JSON 喂脚本

## 十三、常见失败模式

- 用行业均值替代用户真实数据 → 违反 R1
- 专家未回传就写结论 → 违反 R2，重做
- 拿点击数当访客数算 CVR → 出价上限虚高
- 只报"环比跌 2%"不给归因 → 违反 R24
- 报告没跑 `pdf_verify.py` 就交付 → 违反 R9
- 只说「有异常」不给金额影响 → 违反 R8
- 数字不标来源档位、用推算值冒充真实数据 → 违反 R15/R18
- 脚本报错后改参数重试到「通过」→ 违反 R17
- 跨境只给人民币不给外币、不注明汇率税率日期 → 违反 R26
