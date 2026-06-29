# 挣值管理方法论

> **子技能定位**：独立于活动历时估算的核心全流程，单独触发、单独运行。
> 通过 `evm_knowledge.py` 存储在独立 `evm.db` 中，通过 `skill_registry` 与 `shared.db` 关联。
> 可插入结项报告书模板作为可选章节。

---

## 一、触发场景

**正向触发**：EVM / 挣值管理 / PV / EV / AC / SPI / CPI / EAC / 成本绩效 / 进度偏差 / 挣得值 / 计划价值 / 实际成本 / 成本偏差 / 费用偏差 / 费用绩效 / 进度绩效 / 完工估算 / 完工偏差 / 挣值分析 / 偏差分析 / 绩效分析 / 成本控制 / 进度控制 / 挣值管理系统

**不触发**：经济效益分析 / ROI / NPV / IRR / BCR / 投资回收期 / 蒙特卡洛模拟 / 三点估算 / 通用问题

---

## 二、基本术语

| 术语 | 英文 | 缩写 | 定义 |
|------|------|------|------|
| 计划价值 | Planned Value | PV | 截至分析时点，按计划应完成的工作所对应的预算金额 |
| 实际成本 | Actual Cost | AC | 截至分析时点，实际发生的全部成本 |
| 挣值 | Earned Value | EV | 已完成工作的预算价值，EV = PV x actual_progress / plan_progress |
| 总预算 | Budget at Completion | BAC | 项目的总预算金额 |

---

## 三、扩展指标与完工预测

### 3.1 偏差指标

| 指标 | 公式 | 计算方式 | 阈值说明 |
|------|------|----------|----------|
| 进度偏差 (SV) | SV = EV - PV | 绝对值 | SV > 0 进度超前；SV < 0 进度滞后 |
| 进度绩效指数 (SPI) | SPI = EV / PV | 相对值 | SPI > 1 进度高效；SPI < 1 进度低效 |
| 成本偏差 (CV) | CV = EV - AC | 绝对值 | CV > 0 成本节约；CV < 0 成本超支 |
| 成本绩效指数 (CPI) | CPI = EV / AC | 相对值 | CPI > 1 成本高效；CPI < 1 成本低效 |

### 3.2 完工预测指标

| 指标 | 公式 | 说明 |
|------|------|------|
| 完工估算 (EAC，不纠偏) | EAC = BAC / CPI | 按当前成本绩效推算，不做人工干预 |
| 完工估算 (EAC，纠偏) | EAC = AC + (BAC - EV) | 后续工作按原计划效率执行，剩余偏差已纠正 |
| 完工尚需估算 (ETC，不纠偏) | ETC = EAC - AC | 从当前时点到完工还需的成本（延续当前绩效） |
| 完工尚需估算 (ETC，纠偏) | ETC = EAC - EV | 从当前时点到完工还需的成本（后续按计划效率） |
| 完工偏差 (VAC) | VAC = BAC - EAC | VAC > 0 总成本节约；VAC < 0 总成本超支 |

> **注意**：VAC 基于 EAC 计算，EAC 分为不纠偏和纠偏两种模式，VAC 也对应分为 `vac_uncorrected` 和 `vac_corrected` 两个版本。

---

## 四、计算引擎 API

文件：`scripts/evm_engine.py`

### 核心 API

```python
from scripts.evm_engine import run_evm

# 输入：阶段列表，每个阶段包含累积 PV、AC、计划进度、实际进度
phases = [
    {
        "phase_name": "需求分析",
        "cumulative_days": 15,
        "pv": 200000,
        "ac": 180000,
        "plan_progress": 100,
        "actual_progress": 100,
    },
    {
        "phase_name": "设计与开发",
        "cumulative_days": 45,
        "pv": 500000,
        "ac": 520000,
        "plan_progress": 100,
        "actual_progress": 80,
    },
    {
        "phase_name": "测试与部署",
        "cumulative_days": 75,
        "pv": 300000,
        "ac": 280000,
        "plan_progress": 100,
        "actual_progress": 40,
    },
]

# 一次性完整计算（BAC = 各阶段 PV 之和）
result = run_evm(phases)
print(result.to_dict())
```

### 返回值结构

```json
{
  "bac": 1000000,
  "total_plan_duration": 75,
  "analysis_period": "当前",
  "cumulative_ev": 720000,
  "cumulative_pv": 1000000,
  "cumulative_ac": 980000,
  "sv": -280000,
  "spi": 0.72,
  "cv": -260000,
  "cpi": 0.7347,
  "eac_uncorrected": 1361111.11,
  "eac_corrected": 1260000,
  "etc_uncorrected": 381111.11,
  "etc_corrected": 540000,
  "vac_uncorrected": -361111.11,
  "vac_corrected": -260000,
  "phases": [
    {
      "phase_name": "需求分析",
      "cumulative_days": 15,
      "pv": 200000,
      "ac": 180000,
      "ev": 200000,
      "plan_progress": 100,
      "actual_progress": 100,
      "sv": 0,
      "spi": 1.0,
      "cv": 20000,
      "cpi": 1.1111
    },
    {
      "phase_name": "设计与开发",
      "cumulative_days": 45,
      "pv": 500000,
      "ac": 520000,
      "ev": 400000,
      "plan_progress": 100,
      "actual_progress": 80,
      "sv": -100000,
      "spi": 0.8,
      "cv": -120000,
      "cpi": 0.7692
    },
    {
      "phase_name": "测试与部署",
      "cumulative_days": 75,
      "pv": 300000,
      "ac": 280000,
      "ev": 120000,
      "plan_progress": 100,
      "actual_progress": 40,
      "sv": -180000,
      "spi": 0.4,
      "cv": -160000,
      "cpi": 0.4286
    }
  ]
}
```

### 独立函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `calc_ev(pv, actual_progress, plan_progress)` | float, float, float | float (EV) |
| `calc_sv(ev, pv)` | float, float | float (SV) |
| `calc_spi(ev, pv)` | float, float | float (SPI) |
| `calc_cv(ev, ac)` | float, float | float (CV) |
| `calc_cpi(ev, ac)` | float, float | float (CPI) |
| `calc_eac_uncorrected(bac, cpi)` | float, float | float (EAC) |
| `calc_eac_corrected(ac, bac, ev)` | float, float, float | float (EAC) |
| `calc_etc_uncorrected(eac, ac)` | float, float | float (ETC) |
| `calc_etc_corrected(eac_corrected, ev)` | float, float | float (ETC) |
| `calc_vac(bac, eac)` | float, float | float (VAC) |
| `run_evm(phases)` | list[dict] | EVMResult |

---

## 五、知识库存储

### 数据库文件：`evm.db`

独立于 `shared.db` 和 `economic.db`，存放于 `data/` 目录。

### 表结构

#### evm_analyses（主表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| project_id | INTEGER | 引用 shared.projects(id)，可为空 |
| project_name | TEXT | 项目名称（独立运行时） |
| bac | REAL | 总预算 |
| total_plan_duration | REAL | 计划总工期 |
| analysis_period | TEXT | 分析期次说明 |
| plan_progress | REAL | 计划进度（%），截至分析时点 |
| actual_progress | REAL | 实际进度（%），截至分析时点 |
| ev | REAL | 挣值（索引） |
| pv | REAL | 计划价值 |
| ac | REAL | 实际成本 |
| sv | REAL | 进度偏差 |
| spi | REAL | 进度绩效指数（索引） |
| cv | REAL | 成本偏差 |
| cpi | REAL | 成本绩效指数（索引） |
| eac_uncorrected | REAL | 完工估算（不纠偏） |
| eac_corrected | REAL | 完工估算（纠偏） |
| etc_uncorrected | REAL | 完工尚需估算（不纠偏） |
| etc_corrected | REAL | 完工尚需估算（纠偏） |
| vac_uncorrected | REAL | 完工偏差（不纠偏） |
| vac_corrected | REAL | 完工偏差（纠偏） |
| phases_json | TEXT | 各阶段明细 JSON |

索引：`project_id`, `ev`, `spi`, `cpi`

#### evm_periods（明细表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| analysis_id | INTEGER FK | 引用 evm_analyses(id) |
| phase_name | TEXT | 阶段名称 |
| cumulative_days | REAL | 累计天数 |
| pv | REAL | 该阶段计划价值 |
| ac | REAL | 该阶段实际成本 |
| plan_progress | REAL | 该阶段计划进度 |
| actual_progress | REAL | 该阶段实际进度 |

索引：`analysis_id`

### 标准查询接口

```python
from scripts.evm_knowledge import *

# 保存分析结果
save_analysis(project_name="XX系统开发", bac=1000000, total_plan_duration=75, ...)

# 按 ID 查询
get_analysis(1)

# 按 project_id 查询（跨库关联）
get_by_project(project_id=5)

# 按 SPI 区间查询（走索引）
find_by_spi(min_spi=0.8, max_spi=1.2)

# 按 CPI 区间查询（走索引）
find_by_cpi(min_cpi=0.9, max_cpi=1.1)

# 列出所有
list_all()
```

---

## 六、跨库引用规则

| 需要的数据 | 来源库 | 查询方式 |
|-----------|--------|---------|
| 项目阶段/工作包 | shared.db.work_packages | `get_project_phases(project_id)` |
| 项目基本信息 | shared.db.projects | `get_project_info(project_id)` |
| 同项目经济效益分析 | economic.db | `skill_registry → economic.db` |
| 自身历史记录 | evm.db | 直接查询 |

挣值分析**不要求**必须有 shared.db 的项目记录才能运行。
`project_id` 为可选字段，无关联时只使用 `project_name` 独立存储。

---

## 七、与结项报告书模板的集成

结项报告书模板中新增的 `evm_analysis` 章节默认不启用。
用户在定制模板时通过 `add_section()` 添加：

```python
from scripts.project_docs_engine import add_section

add_section(tpl, {
    "key": "evm_analysis",
    "title": "挣值分析",
    "type": "fields",
    "description": "基于 PV/EV/AC 计算 SPI、CPI、EAC 等进度与成本绩效指标",
    "fields": [
        {"key": "bac", "label": "总预算 (BAC)", "type": "text", "hint": "项目总预算金额"},
        {"key": "pv", "label": "计划价值 (PV)", "type": "text", "hint": "计划完成工作预算"},
        {"key": "ev", "label": "挣值 (EV)", "type": "text", "hint": "实际完成工作预算"},
        {"key": "ac", "label": "实际成本 (AC)", "type": "text", "hint": "实际发生成本"},
        {"key": "sv", "label": "进度偏差 (SV)", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "spi", "label": "进度绩效指数 (SPI)", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "cv", "label": "成本偏差 (CV)", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "cpi", "label": "成本绩效指数 (CPI)", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "eac_uncorrected", "label": "完工估算（不纠偏）", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "eac_corrected", "label": "完工估算（纠偏）", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "vac_uncorrected", "label": "完工偏差（不纠偏）", "type": "text", "hint": "由计算引擎自动生成"},
        {"key": "vac_corrected", "label": "完工偏差（纠偏）", "type": "text", "hint": "由计算引擎自动生成"},
    ],
    "reference_sources": ["estimation_result"],
}, after_key="performance_summary")
```
