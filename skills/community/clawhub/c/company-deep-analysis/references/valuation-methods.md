# 相对估值方法参考

本文件在 **Step5** 开始时加载。提供 10 个相对估值变体的方法选取、公式速查、可比公司选取原则、估值区间计算和交叉验证规则。

---

## §1 四步法：行业 → 估值方法决策

```
Step1：现金流稳不稳？
├─ 稳（消费/医药/公用）   → PE-TTM 首选，PE-Forward 补充
└─ 不稳（周期/初创）      → 走 Step2

Step2：资产重 vs 轻？
├─ 重（银行/地产/资源）   → PB-MRQ 首选，EV/EBITDA-TTM 补充
└─ 轻（互联网/软件）      → PS-TTM 首选，EV/Revenue 补充

Step3：行业特殊触发？
├─ 周期制造                → 周期中点 PE（替代 PE-TTM）
├─ SaaS / 互联网平台       → Rule of 40（替代 EV/Revenue）
├─ 半导体/航空/资源        → EV/EBITDA-TTM 优先
└─ 通用                    → 走完 Step1+2 即可

Step4：是否盈利用 Forward？
├─ 盈利可见 + 预测一致性好 → 加 Forward 变体
└─ 不可见 / 一致预期分歧大 → 不用 Forward
```

**实操入口**：`scripts/valuation.py` 的 `_classify_industry(data)` 已实现上述判定逻辑，输入申万一级行业自动返回首选方法 + 交叉验证方法。

---

## §2 10 个相对估值变体速查

| 变体 | 公式 | 适用行业 | 关键数据源 |
|---|---|---|---|
| **PE-TTM** | 合理股价 = TTM EPS × 可比 PE 中位数 | 消费/医药/公用 | `eps_ttm` / `quote` / peers |
| **PE-Forward** | 合理股价 = Forward EPS × 可比 PE 中位数 | 盈利可见的高增长 | `eps_forward`（ths_forecast） |
| **周期中点 PE** | 合理股价 = 历史 EPS 中位数 × 周期 PE 中位数 | 周期制造（钢/化/煤/航运） | `eps_history`（5-10 年） |
| **PB-MRQ** | 合理股价 = BVPS × 可比 PB 中位数 | 银行/地产/重资产 | `bvps` / `quote` / peers |
| **PB-Forward** | 合理 PB = (ROE - g) / (COE - g) | 银行/券商 | `bvps` + ROE 假设 |
| **PS-TTM** | 合理股价 = TTM SPS × 可比 PS 中位数 | 高成长未盈利 | `sps_ttm` / peers |
| **PS-Forward** | 合理股价 = Forward SPS × 可比 PS 中位数 | 增长可见的早期 | `sps_forward` |
| **EV/EBITDA-TTM** | 合理 EV = TTM EBITDA × 可比 EV/EBITDA | 资本密集（半导体/资源/航空） | `calc_ebitda(lrb+llb)` |
| **EV/EBITDA-Forward** | 合理 EV = Forward EBITDA × 可比 EV/EBITDA | 同上（用预测 EBITDA） | TTM EBITDA × 增长假设 |
| **EV/Revenue-TTM** | 合理 EV = TTM 营收 × 可比 EV/Revenue | 互联网平台/SaaS | `revenue_ttm` + `net_debt` |
| **Rule of 40** | 增速 + EBITDA 率 ≥ 40% → EV/Revenue × 1.5 | SaaS/互联网 | `revenue_growth` + `ebitda` |

---

## §3 行业 → 方法配对速查表

| 申万一级 | 行业类 | 首选方法 | 交叉验证 |
|---|---|---|---|
| 食品饮料 / 美容护理 / 家用电器 / 纺织服饰 | 品牌消费 | `val_pe_ttm` | `val_pe_forward`, `val_ev_ebitda_ttm` |
| 医药生物（成熟） | 品牌消费 | `val_pe_ttm` | `val_pe_forward` |
| 医药生物（亏损/创新药） | 创新药 | `val_ps_ttm` | `val_ev_revenue_ttm` |
| 银行 / 证券 / 非银金融 | 金融 | `val_pb_mrq` | `val_pb_forward`, `val_pe_ttm` |
| 房地产 | 地产 | `val_pb_mrq` | `val_ev_ebitda_ttm` |
| 公用事业 / 电力 / 水务 / 燃气 | 公用事业 | `val_pe_ttm` | `val_pb_mrq` |
| 钢铁 / 化工 / 煤炭 / 石油石化 / 建材 / 航运 | 周期制造 | `val_pe_cycle` | `val_pb_mrq`, `val_ev_ebitda_ttm` |
| 有色金属 / 采掘 / 矿业 | 资源 | `val_ev_ebitda_ttm` | `val_pb_mrq` |
| 半导体 / 航空 / 国防军工 | 资本密集 | `val_ev_ebitda_ttm` | `val_pe_ttm` |
| 计算机 / 传媒 / 软件 / 互联网 | 互联网/SaaS | `val_rule_of_40` | `val_ev_revenue_ttm`, `val_ps_ttm` |
| 通用兜底 | 通用 | `val_pe_ttm` | `val_pb_mrq`, `val_ev_ebitda_ttm` |

---

## §4 关键数据采集位置（已采 / 需补）

| 数据 | 已采？ | 位置 | 备注 |
|---|---|---|---|
| 当前股价 | ✅ | `data["price"]` | 实时 |
| 总股本 | ✅ | `data["total_shares"]` | quote 字段 |
| 归母净利润 | ✅ | `data["finance"]` / `data["lrb"]` | — |
| 归母净资产 | ✅ | `data["finance"]` | — |
| 滚动 EPS / BVPS | ⚠️ 需算 | `eps_ttm = 归母净利润 × 4 / latest_quarter / 总股本` | 脚本自动算 |
| Forward EPS | ✅ | `data["ths_forecast"]` | 一致预期 |
| 营收（TTM） | ✅ | `data["finance"]` 营收字段 | — |
| 营收增速 | ⚠️ 需算 | `(revenue_ttm / revenue_prev_year) - 1` | — |
| 历史 EPS（5-10 年） | ⚠️ 缺 | 需联网搜年报 | 周期 PE 必需 |
| 净负债（短借+长借-货币） | ⚠️ 需算 | `data["fzb"]` 三个字段 | EV 必需 |
| EBITDA | ⚠️ **本 skill 自动拆解** | `westock_data.calc_ebitda(lrb, llb)` | 见 §5 |
| 可比公司 PE/PB/PS 中位数 | ✅ 自动获取 | `WebSearch（行业竞品）` + `finance` 循环 + `pandas.median()` | 申万行业自动拉，**无手工拍板** |

---

## §5 EBITDA 拆解（`calc_ebitda` 已落地）

**位置**：`scripts/westock_data.py:297`

**公式**：
```
EBITDA = 净利润 + 利息 + 税 + 折旧摊销
       = 归属于母公司股东的净利润
       + 财务费用（含利息支出 - 利息收入 + 汇兑损益）
       + 所得税费用
       + 折旧与摊销（llb 补充资料）
```

**容错机制**：
- 净利润缺失 → 退而用 `lrb.净利润`
- 财务费用缺失 → 退而用 `利息支出 - 利息收入`
- 折旧/摊销缺失 → 尝试 4 个备胎字段名（"折旧与摊销"合并 / "固定资产折旧"分列 / "无形资产摊销" / "长期待摊费用摊销"）
- **数据完全缺失时返回 `{"error": "..."}`，不硬算**

**权威背书**：
- Damodaran《Investment Valuation》Ch.11 公式
- 国内卖方研报 EBITDA 拆解标准（中信/华泰/中金）

---

## §6 可比公司选取原则

### 6.1 选取标准

1. **同行业、同细分赛道**：申万二级行业分类相同
2. **市值规模相近**：市值差异不超过 5 倍
3. **增长阶段相近**：增速差异不超过 2 倍
4. **业务模式相似**：主营产品/客户群体/商业模式可类比
5. **数量要求**：至少 3 家，最多 5 家

### 6.2 数据获取

| 数据 | 来源 |
|---|---|
| 目标公司 PE/PB/市值 | `/tmp/{code}_data.json` 的 `quote` 字段（Step0 已采） |
| 可比公司 PE/PB/市值 | `python3 scripts/collect_data.py --quotes 代码1,代码2,...` |
| 机构 EPS 预测 | `data["reports"]`（东财研报，已采） |
| 一致预期 EPS | `data["ths_forecast"]`（同花顺，已采） |

---

## §7 交叉验证

### 7.1 多方法对比

| 方法 | 估值中枢 | 当前市值 | 上行/下行空间 |
|---|---|---|---|
| 首选方法 | __亿 | __亿 | __% |
| 交叉验证1 | __亿 | __亿 | __% |
| 交叉验证2 | __亿 | __亿 | __% |
| **综合估值**（中位数） | __亿 | __亿 | __% |

### 7.2 偏差处理

- 多方法结果偏差 **< 15%**：取均值作为综合估值
- 偏差 **15% - 30%**：取均值但标注分歧原因
- 偏差 **> 30%**：必须分析分歧原因（周期性/特殊项目/会计差异），取更保守的估值

### 7.3 合理性检查

| 检查项 | 标准 | 不通过时处理 |
|---|---|---|
| 估值隐含增速 | 与历史增速和行业增速比较 | 偏差过大则调整估值区间 |
| PE 合理性 | 估值 PE 是否在行业历史区间内 | 超出历史区间需说明 |
| 市值合理性 | 估值市值与行业地位是否匹配 | 不匹配需说明 |
| 数据完整度 | `valuation.py` 输出的 `数据完整度` ≥ 60% | < 60% 时提示补充行业数据 |

---

## §8 报告输出格式（只展示数字）

报告正文**不展示公式**，只展示结论：

```markdown
## 估值（相对估值）

### 行业分类
[申万一级] → [行业类]

### 估值结果
| 维度 | 数值 |
|---|---|
| 首选方法 | 周期中点 PE（7年） |
| 合理股价 | 12.30 元 |
| 当前股价 | 10.50 元 |
| 上行空间 | +17.1% |
| 合理市值 | 270.6 亿 |
| 当前市值 | 231.0 亿 |
| 数据完整度 | 67% |

### 交叉验证
- PB-MRQ：合理价 11.80 元（差异 -4.1%）
- EV/EBITDA-TTM：合理价 12.50 元（差异 +1.6%）

### 关键假设
- 周期 PE 中位数 = 8.0x（行业 5 年平均）
- 7 年 EPS 中位数 = 1.54 元
- 净负债 = 0（货币资金充裕）

### 局限性
- [数据完整度提示]
- [行业假设提示]
```

**公式 / 推导 / 行业倍数**只放在 `valuation-methods.md`（本文）和 `scripts/valuation.py`，**不进报告**。
