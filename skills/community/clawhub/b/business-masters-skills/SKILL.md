# SKILL.md · 商业管理大师专家技能矩阵

> 本文件用于向调用者快速概述本技能包的用途、调用方式与约束。详细工程说明见 `README.md`。

---

## 一、技能名称与简要描述

**技能名称**：商业管理大师专家技能矩阵（Business Masters Skill Matrix）
**版本**：v1.0.0 ｜ **运行环境**：Python 3.10+（仅依赖标准库）

将德鲁克、吉姆·柯林斯、克莱顿·克里斯坦森、迈克尔·波特、查理·芒格等商业管理大师的核心方法论，实现为 **9 个独立、松耦合、可程序化调用** 的技能模块。每个模块接收结构化商业输入，输出对应大师理论框架下的诊断结论与可落地行动建议。模块 M09「战略顾问专家」为整合入口，可路由并综合调用其余模块，形成端到端经营诊断。

| 编号 | 模块 | 大师 | 层级 |
| --- | --- | --- | --- |
| M01 | 波特竞争战略顾问 | 波特 | Tier1 战略 |
| M02 | 克里斯坦森颠覆式创新顾问 | 克里斯坦森 | Tier2 组织效能与创新 |
| M03 | 柯林斯从优秀到卓越顾问 | 柯林斯 | Tier2 组织效能与创新 |
| M04 | 德鲁克卓有成效的管理者 | 德鲁克 | Tier2 组织效能与创新 |
| M05 | 柯林斯第五级领导力顾问 | 柯林斯 | Tier3 领导力与决策 |
| M06 | 芒格第一性原理决策顾问 | 芒格 | Tier3 领导力与决策 |
| M07 | 德鲁克目标管理(MBO)顾问 | 德鲁克 | Tier4 目标与执行 |
| M08 | 柯林斯执行飞轮顾问 | 柯林斯 | Tier4 目标与执行 |
| M09 | 战略顾问专家（整合入口） | 综合 | 汇聚层 |

---

## 二、适用场景说明

- **战略规划**：新市场进入、竞争格局复盘、战略定位重塑（M01）。
- **创新管理**：第二曲线孵化、大企业创新防御、初创产品定位（M02）。
- **组织效能**：增长瓶颈突破、组织转型、管理者效能提升（M03/M04）。
- **领导力发展**：高管继任、领导力梯队建设、第五级领导测评（M05）。
- **决策分析**：重大投资/并购决策、战略风险评估（M06）。
- **目标与执行**：绩效体系搭建、OKR 落地、飞轮执行落地（M07/M08）。
- **综合诊断**：企业全面经营诊断、战略落地全案、投资尽调（M09 整合入口）。

> 目标用户：CEO / 战略负责人 / HRD / 创新负责人 / 投资机构；亦可作为 AI 顾问 Agent 的后端能力被程序化调用。

---

## 三、输入参数及格式要求

所有模块统一约定：`invoke(params: dict) -> SkillResult`。各模块参数详见对应文件头部「输入参数定义」。常用参数格式示例如下：

| 模块 | 关键参数 | 类型 | 格式/约束 |
| --- | --- | --- | --- |
| M01 | `industry_description` | str | 必填，非空 |
| M01 | `five_forces` | dict | 必填，5 键(competitors/new_entrants/substitutes/buyer_power/supplier_power)，各 1-5 整数 |
| M02 | `market_type` | enum | 必填，`non_consumption`\|`new_market`\|`low_end` |
| M02 | `rpv_assessment` | dict | 必填，resources/processes/values 各 1-5 整数 |
| M03 | `level5_assessment` | dict | 必填，humility/will 各 1-5 整数 |
| M04 | `current_habits` | dict | 必填，5 项习惯各 1-5 整数 |
| M05 | `self_rating` | dict | 必填，humility/professional_will/credit_to_others/blame_self 各 1-5 |
| M06 | `decision_question` / `options` | str / list | 必填；options 非空列表 |
| M07 | `draft_targets` | list | 必填，每元素含 owner/metric/deadline |
| M08 | `flywheel_steps` | list | 必填，有序字符串列表(≥3 项方判定闭环) |
| M09 | `problem_layer` / `module_inputs` | enum / dict | 必填；layer∈strategy\|organization\|leadership\|execution\|diagnosis |

**通用规则**：必填缺省 → 返回 `invalid_input`；可选缺省 → 自动填充默认值；类型/枚举/取值范围不符 → 返回错误说明。调用前可用 `tools/validate_params.py` 自检。

---

## 四、输出结果说明

所有模块返回统一结构 `SkillResult`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `module_id` | str | 模块编号（m01–m09） |
| `module_name` | str | 模块名称 |
| `status` | str | `success` \| `invalid_input` \| `error` |
| `data` | dict | 结构化业务结果（各模块字段不同，见文件头「输出结果定义」） |
| `insights` | list | 关键洞察 |
| `recommendations` | list | 可落地行动建议 |
| `warnings` | list | 预警/假设提示 |

示例（M01 `data` 部分字段）：`industry_attractiveness`、`recommended_strategy`、`five_forces_diagnosis`、`tradeoffs`。

---

## 五、使用示例

```bash
# 进入项目根目录（务必在根目录执行，脚本会自动注入 sys.path）
cd business-masters-skills

# 1) 调用前参数自检
python tools/validate_params.py --module m01 \
  --params '{"industry_description":"连锁咖啡","five_forces":{"competitors":5,"new_entrants":4,"substitutes":4,"buyer_power":4,"supplier_power":2}}'

# 2) 独立运行单个模块（自带演示样例）
python -m tier1_strategy.m01_porter_competitive_strategy

# 3) 批量调用并落盘
python tools/batch_invoke.py --manifest tests/sample_manifest.json --out results.json

# 4) 验证输出结构合法性
python tools/verify_result.py --result results.json

# 5) 整合层路由调用（综合诊断入口）
python -m integration.m09_strategic_advisor_expert
```

代码内调用（松耦合，仅通过加载器取用公开接口）：

```python
import sys; sys.path.insert(0, ".")
from common.loader import load_skill

entry = load_skill("m01")                 # 按编号加载
result = entry["invoke"]({                 # 传入参数字典
    "industry_description": "连锁咖啡",
    "five_forces": {"competitors": 5, "new_entrants": 4,
                    "substitutes": 4, "buyer_power": 4, "supplier_power": 2},
})
print(result.status, result.data["recommended_strategy"])
```

---

## 六、注意事项与限制条件

1. **执行目录**：所有脚本须在项目根目录 `business-masters-skills/` 下执行，否则 `sys.path` 无法定位 `common` 包。
2. **松耦合边界**：模块间**不直接 import 彼此内部实现**，一律通过 `common.loader.load_skill()` + `SkillResult` 交互；请勿绕过契约直接引用内部函数。
3. **入参校验**：评分类参数均为 **1-5 整数**、枚举须精确匹配；不合法将返回 `status="invalid_input"` 而非抛异常，请检查 `warnings`。
4. **结果性质**：输出为**基于规则(heuristic)的方法论辅助建议**，用于结构化思考与决策支持，**不构成投资/法律/财务专业意见**，重大决策请结合专家人工研判。
5. **M09 容错**：整合层中某子模块入参缺失或出错**不会阻断**其他模块，该模块结果标记 `status="error"`，请检查各模块返回。
6. **依赖**：仅使用 Python 标准库，无需 pip 安装；Python 版本需 ≥ 3.10。
7. **编码**：所有文件为 UTF-8；Windows 终端如遇中文乱码，请将控制台代码页切换为 UTF-8（`chcp 65001`）。
