# 经济效益分析方法论

> **子技能定位**：独立于活动历时估算的核心全流程，单独触发、单独运行。
> 通过 `economic_knowledge.py` 存储在独立 `economic.db` 中，通过 `skill_registry` 与 `shared.db` 关联。
> 可插入立项申请书模板作为可选章节。

---

## 一、触发场景

**正向触发**：经济效益分析 / 投资回报 / ROI / NPV / IRR / BCR / 投资回收期 / 可行性分析 / 项目经济效益 / 折现分析 / 多折现率对比

**不触发**：工期估算 / CPM / 蒙特卡洛 / 挣值管理 / 通用问题

---

## 二、术语与公式

### 2.1 静态指标

| 指标 | 公式 | 说明 |
|------|------|------|
| 静态 ROI | $\text{ROI} = \frac{\text{年净利}}{\text{投资总额}} \times 100\%$ | 年利润率，仅看当年回报 |
| 加权 ROI | $\text{ROI} = \frac{\text{年净利} \times (n-1) + \frac{\text{第n年现金流含终值} - \text{初始投资}}{n}}{\text{初始投资}} \times 100\%$ | 考虑终值和全周期的综合回报率 |
| 静态 PBP | 相同: $\text{PBP} = \frac{1}{\text{ROI}}$ | 投资回收期 |
| | 不同: $\text{PBP} = N - 1 + \frac{\mid\text{累计现金流}_{N-1}\mid}{\text{净现金流}_N}$ | $N$=累计现金流转正年份 |

### 2.2 动态指标

| 指标 | 公式 | 说明 |
|------|------|------|
| 净现值 (NPV) | $\text{NPV} = \sum_{t=1}^{n} \frac{\text{净现金流}_t}{(1+i)^t} - \text{初始投资}$ | $\text{NPV}>0$可行 |
| 内部收益率 (IRR) | $\text{IRR} = i_1 + \frac{\text{NPV}_1}{\text{NPV}_1 - \text{NPV}_2} \times (i_2 - i_1)$ | 插值法，$\text{IRR}>i$可行 |
| 效益成本比 (BCR) | $\text{BCR} = \frac{\sum \text{净现金流折现}}{\sum \text{折现成本}}$ | $\text{BCR}>1$具有经济效益 |
| 动态 PBP | $\text{PBP}_{动} = N - 1 + \frac{\mid\text{累计折现}_{N-1}\mid}{\text{折现净现金流}_N}$ | 折现后回收期 |

### 2.3 折现因子

$$ \text{DF}_t = \frac{1}{(1 + i)^t} $$

其中 $i$ 为折现率（%），$t$ 为年数。

---

## 三、计算引擎

文件：`scripts/economic_analysis_engine.py`

### 核心 API

```python
from scripts.economic_analysis_engine import EconomicParams, run_analysis

# 输入参数
params = EconomicParams(
    initial_investment=100,   # 初始投资（万元）
    annual_revenue=12,        # 年收益
    annual_cost=5,            # 年支出
    periods=5,                # 运营周期（年）
    terminal_value=200,       # 终值/残值
    discount_rate=10,         # 折现率（%）
    name="小作坊",            # 项目名称
)

# 一次性完整计算
result = run_analysis(params)
print(result.to_dict())
```

### 返回值结构

```json
{
  "project_name": "小作坊",
  "currency": "¥",
  "initial_investment": 100,
  "annual_revenue": 12,
  "annual_cost": 5,
  "annual_net": 7,
  "periods": 5,
  "terminal_value": 200,
  "discount_rate": 10,
  "roi_static": 7.0,
  "roi_weighted": 49.4,
  "npv": 50.72,
  "irr": 20.35,
  "bcr": 1.3719,
  "pbp_static": 4.35,
  "pbp_dynamic": 4.61,
  "cashflows": [
    {"year": 1, "revenue": 12, "cost": 5, "net_cashflow": 7,
     "net_discounted": 6.36, "discounted_cost": 95.45},
    ...
  ],
  "discount_comparison": {
    "10": {"rate": 10, "npv": 50.72, "bcr": 1.3719, "pbp_dynamic": 4.61},
    "15": {"rate": 15, "npv": 22.9, "bcr": 1.18, "pbp_dynamic": ...},
    ...
  }
}
```

### 独立函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `calc_roi_static(params)` | EconomicParams | float (%) |
| `calc_roi_weighted(params)` | EconomicParams | float (%) |
| `calc_pbp_static(params)` | EconomicParams | float (年) |
| `calc_pbp_dynamic(params)` | EconomicParams | float (年) |
| `calc_npv(params)` | EconomicParams | float |
| `calc_irr(params)` | EconomicParams | float (%) |
| `calc_bcr(params)` | EconomicParams | float |
| `calc_cashflows(params)` | EconomicParams | list[dict] |
| `calc_discount_comparison(params, rates)` | EconomicParams, list | dict |

---

## 四、知识库存储

### 数据库文件：`economic.db`

独立于 `shared.db` 和 `evm.db`，存放于 `data/` 目录。

### 表结构

#### economic_analyses（主表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| project_id | INTEGER | 引用 shared.projects(id)，可为空 |
| project_name | TEXT | 项目名称（独立运行时） |
| discount_rate | REAL | 基准折现率（%） |
| periods | INTEGER | 运营周期（年） |
| initial_investment | REAL | 初始投资额 |
| annual_revenue | REAL | 年收益 |
| annual_cost | REAL | 年支出 |
| terminal_value | REAL | 终值 |
| currency | TEXT | 货币单位 |
| npv | REAL | 净现值（索引） |
| irr | REAL | 内部收益率（索引） |
| bcr | REAL | 效益成本比 |
| roi_static | REAL | 静态ROI |
| roi_weighted | REAL | 加权ROI |
| pbp_static | REAL | 静态回收期 |
| pbp_dynamic | REAL | 动态回收期 |
| cashflows_json | TEXT | 逐年现金流明细 |
| params_json | TEXT | 完整输入参数 |

索引：`project_id`, `npv`, `irr`

#### economic_cashflows（明细表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| analysis_id | INTEGER FK | 引用 economic_analyses(id) |
| year | INTEGER | 年份 |
| revenue | REAL | 年收益 |
| cost | REAL | 年支出 |
| net_cashflow | REAL | 净现金流 |
| net_discounted | REAL | 净现金流折现 |
| discounted_cost | REAL | 折现成本 |

索引：`analysis_id`

### 标准查询接口

```python
from scripts.economic_knowledge import *

# 保存分析结果
save_analysis(project_name="小作坊", discount_rate=10, periods=5, ...)

# 按 ID 查询
get_analysis(1)

# 按 project_id 查询（跨库关联）
get_by_project(project_id=5)

# 按 IRR 区间查询（走索引）
find_by_irr(min_irr=15, max_irr=25)

# 按 NPV 查询（走索引）
find_by_npv(min_npv=0)

# 列出所有
list_all()
```

---

## 五、跨库引用规则

| 需要的数据 | 来源库 | 查询方式 |
|-----------|--------|---------|
| 项目工期/周期 | shared.db.projects.total_duration | `get_project_duration(project_id)` |
| 项目基本信息 | shared.db.projects | `ATTACH shared.db` |
| 同项目挣值分析 | evm.db | `skill_registry → evm.db` |
| 自身历史记录 | economic.db | 直接查询 |

经济效益分析**不要求**必须有 shared.db 的项目记录才能运行。
`project_id` 为可选字段，无关联时只使用 `project_name` 独立存储。

---

## 六、与立项申请书模板的集成

立项申请书模板中新增的 `economic_analysis` 章节默认不启用。
用户在定制模板时通过 `add_section()` 添加：

```python
from scripts.project_docs_engine import add_section

add_section(tpl, {
    "key": "economic_analysis",
    "title": "经济效益分析",
    "type": "fields",
    "description": "基于投资总额、收益和成本计算 ROI/NPV/IRR/BCR 等经济效益指标",
    "fields": [
        {"key": "initial_investment", "label": "初始投资总额", "type": "text", "hint": "一次性资本投入"},
        {"key": "annual_revenue", "label": "年收益", "type": "text", "hint": "持续运营收入"},
        {"key": "annual_cost", "label": "年支出", "type": "text", "hint": "持续运营成本"},
        {"key": "discount_rate", "label": "折现率", "type": "text", "hint": "基准折现率（%）"},
        {"key": "periods", "label": "计算周期", "type": "text", "hint": "运营年数"},
        {"key": "terminal_value", "label": "终值/残值", "type": "text", "hint": "期末资产处置收入"},
        {"key": "npv", "label": "净现值（NPV）", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "irr", "label": "内部收益率（IRR）", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "bcr", "label": "效益成本比（BCR）", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "pbp_static", "label": "静态投资回收期", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "pbp_dynamic", "label": "动态投资回收期", "type": "text", "hint": "由计算引擎自动生成"},
    ],
    "reference_sources": ["estimation_result"],
}, after_key="budget")
```
