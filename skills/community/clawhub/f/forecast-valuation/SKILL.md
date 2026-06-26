---
name: forecast-valuation
slug: forecast-valuation
version: 1.0.0
description: 专业财务预测与估值模型生成器。结合高盛 DCF 标准与 Wind Evaluator 框架，自动生成完整三表预测、DCF 估值、相对估值、敏感性分析和 Football Field 估值区间。
metadata: {"openclaw":{"emoji":"📊"}}
---

# Forecast & Valuation Skill

专业财务预测与估值模型生成器，融合高盛 DCF 估值标准与 Wind Evaluator 专业框架。

## 功能特性

### 📊 核心功能

| 模块 | 功能描述 |
|------|---------|
| **历史报表** | 自动导入/手动录入 5-10 年历史财务数据 |
| **基本假设** | 收入驱动、成本结构、资本配置、营运资本假设 |
| **三表预测** | 利润表/资产负债表/现金流量表 5 年预测，自动配平 |
| **财务分析** | 比率分析、杜邦分析、趋势分析 |
| **DCF 估值** | WACC 计算、自由现金流折现、终值计算 |
| **敏感性分析** | WACC vs g 矩阵、龙卷风图、情景分析 |
| **相对估值** | 可比公司筛选、PE/PB/EV/EBITDA 倍数分析 |
| **Football Field** | 多方法估值区间可视化 |

### ✨ 核心优势

1. **专业标准** - 融合高盛 DCF 框架 + Wind Evaluator 完整性
2. **自动配平** - 资产负债表自动平衡检查
3. **智能筛选** - 自动筛选 8-12 家可比公司
4. **数据接口** - 支持 Gangtise/Tushare 自动获取财务数据
5. **质量检验** - 预测合理性自动检验

## 使用方法

### 基本用法

```bash
# 生成完整财务预测与估值模型
python3 scripts/build_forecast.py "福耀玻璃" "600660.SH"

# 指定输出路径
python3 scripts/build_forecast.py "福耀玻璃" "600660.SH" --output "福耀玻璃_估值模型.xlsx"

# 仅生成 DCF 估值
python3 scripts/build_dcf.py "福耀玻璃" --wacc 9.5 --terminal_growth 2.0

# 仅生成可比公司分析
python3 scripts/build_comps.py "福耀玻璃" --industry "汽车零部件"
```

### 参数选项

```bash
python3 scripts/build_forecast.py <公司名称> <股票代码> [选项]

选项:
  --output, -o          输出文件路径
  --years, -y           预测年数（默认：5）
  --wacc                WACC（默认：自动计算）
  --terminal-growth, -g 永续增长率（默认：2.0%）
  --peers, -p           可比公司列表（逗号分隔）
  --industry, -i        行业分类（用于自动筛选可比公司）
  --data-source, -d     数据来源（gangtise/tushare/manual）
  --upload, -u          上传到百度网盘
```

## 模型结构

生成的 Excel 模型包含以下工作表：

### 1️⃣ 封面
- 公司基本信息
- 股票代码、所属行业
- 报告日期、分析师
- 主营业务结构

### 2️⃣ 历史报表 (简化)
- 5-10 年历史利润表
- 5-10 年历史资产负债表
- 5-10 年历史现金流量表
- 关键财务指标

### 3️⃣ 基本假设
**收入驱动因素**
- 销量增速、单价增速
- 产品结构变化
- 区域收入分布

**利润率假设**
- 毛利率、各项费用率
- 有效税率

**资本配置**
- 资本开支/收入
- 折旧摊销/收入
- 分红比例

**营运资本假设**
- 应收账款周转天数
- 存货周转天数
- 应付账款周转天数

### 4️⃣ 利润表预测 (5 年)
- 营业收入预测
- 成本结构预测
- 三项费用预测
- 净利润预测
- EPS 预测

### 5️⃣ 资产负债表预测 (5 年)
- 流动资产预测
- 固定资产预测
- 负债预测
- 股东权益预测
- **配平检查**（自动）

### 6️⃣ 现金流量表预测 (5 年)
- 经营活动现金流
- 投资活动现金流
- 融资活动现金流
- 自由现金流 (FCF)

### 7️⃣ 财务分析
- 盈利能力（ROE/ROA/ROIC）
- 偿债能力（资产负债率/利息保障倍数）
- 营运能力（周转率）
- 杜邦分析

### 8️⃣ DCF 估值
- WACC 详细计算（CAPM + 债务成本）
- 自由现金流预测
- 终值计算（永续增长法 + 退出倍数法）
- 企业价值 → 股权价值
- 每股价值

### 9️⃣ DCF 敏感性分析
- WACC vs 永续增长率 矩阵
- 每股价值敏感性
- 情景分析（乐观/基准/悲观）

### 🔟 可比公司估值
- 8-12 家可比公司筛选
- 估值倍数对比（PE/PB/EV/EBITDA/P/FCF/PEG）
- 行业平均/中位数/分位数
- 溢价/折价分析

### 1️⃣1️⃣ 相对估值
- PE 估值法
- PB 估值法
- EV/EBITDA 估值法
- 综合估值区间

### 1️⃣2️⃣ Football Field
- 多方法估值区间可视化
- DCF 区间
- 相对估值区间
- 当前股价位置
- 目标价区间

### 1️⃣3️⃣ 预测合理性检验
- 收入增速 vs 行业增速
- 利润率趋势合理性
- 资本开支与折旧匹配
- 营运资本变动合理性

## 数据来源

| 数据项 | 来源 |
|--------|------|
| 历史财务数据 | Gangtise / Tushare / 手动录入 |
| 一致预期 | Gangtise / Wind / Choice |
| 可比公司数据 | Tushare / 手动录入 |
| 无风险利率 | 10 年期国债收益率（自动获取） |
| 市场风险溢价 | 默认 7.0%（可配置） |
| Beta 系数 | 自动计算（2 年周收益率） |

## 配置

配置文件 `config.json`：

```json
{
  "GANGTISE_ACCESS_KEY": "your_access_key",
  "GANGTISE_SECRET_KEY": "your_secret_key",
  "TUSHARE_TOKEN": "your_tushare_token",
  "DATA_SOURCE": "gangtise",
  "OUTPUT_DIR": "/root/.openclaw/workspace",
  "UPLOAD_TO_BAIDU": false,
  "WACC_DEFAULT": {
    "risk_free_rate": 2.5,
    "market_risk_premium": 7.0,
    "cost_of_debt": 4.5,
    "tax_rate": 15.0
  },
  "VALUATION_DEFAULT": {
    "terminal_growth": 2.0,
    "exit_ev_ebitda": 12.0
  }
}
```

## 输出格式

- **字体**: Times New Roman / 宋体
- **小数位**: 1 位（百分比 0.0%）
- **千位分隔符**: 启用
- **金额单位**: 百万元（可配置）
- **数字格式**: #,##0.0

## 示例

### 福耀玻璃估值模型

```bash
python3 scripts/build_forecast.py "福耀玻璃" "600660.SH" \
  --output "福耀玻璃_财务预测与估值_20260320.xlsx" \
  --years 5 \
  --industry "汽车零部件"
```

生成模型包含：
- 2021A-2025A 历史数据
- 2026E-2030E 财务预测
- DCF 估值：55.0 HKD
- 可比公司 PE 平均：19.6x
- Football Field 目标价区间：52-62 HKD
- 评级：买入

## 质量检验

模型自动生成预测合理性检验报告：

| 检验项 | 标准 | 状态 |
|--------|------|------|
| 收入增速 vs 行业 | ≤行业增速 1.5x | ✅ |
| 毛利率趋势 | 波动≤5% | ✅ |
| 资本开支/折旧 | 1.0-2.0x | ✅ |
| 营运资本/收入 | 稳定或改善 | ✅ |
| 资产负债率 | ≤70% | ✅ |

## 依赖

- Python 3.8+
- openpyxl
- pandas
- requests
- numpy

## 故障排除

### 数据获取失败

```bash
# 检查配置
python3 scripts/configure.py

# 测试连接
python3 scripts/test_connection.py

# 使用手动录入模式
python3 scripts/build_forecast.py "公司" "代码" --data-source manual
```

### 资产负债表不平

- 检查"配平检查"工作表
- 常见原因：留存收益计算错误、现金作为配平项
- 模型自动使用"现金及等价物"作为配平项

### 可比公司数据缺失

```bash
# 手动指定可比公司
python3 scripts/build_comps.py "福耀玻璃" \
  --peers "信义玻璃，旗滨集团，南玻 A"
```

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-20 | 初始版本，融合高盛 DCF 标准与 Wind Evaluator 框架 |

## 相关 Skill

- `financial-model` - 基础财务建模
- `gangtise-kb` - 刚投知识库数据接口
- `tushare-finance` - Tushare 金融数据接口

## 反馈

- 问题报告：GitHub Issues
- 功能建议：SkillHub 评论
