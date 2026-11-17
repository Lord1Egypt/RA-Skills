# 商业管理大师专家技能矩阵 · 可执行技能工程包

> 将「战略 → 组织效能与创新 → 领导力与决策 → 目标与执行 → 战略顾问专家整合」逻辑递进的 9 个方法论模块，实现为**独立、松耦合、可程序化调用**的技能文件。
> 版本：v1.0.0 ｜ 语言：Python 3.10+（仅依赖标准库）

---

## 1. 目录结构

```
business-masters-skills/
├── README.md                      # 本说明
├── common/                        # 公共接口契约（所有模块共享，松耦合基石）
│   ├── interface.py               #   SkillResult / ParameterSpec / SkillContract / validate_params
│   ├── registry.py                #   技能注册表（模块 import 时自动登记）
│   └── loader.py                  #   技能加载器（按编号动态加载，集成层只依赖它）
├── tier1_strategy/                # 层级1 战略思维（顶层设计）
│   └── m01_porter_competitive_strategy.py
├── tier2_organization/            # 层级2 组织效能与创新（中层支撑）
│   ├── m02_christensen_disruptive_innovation.py
│   ├── m03_collins_good_to_great.py
│   └── m04_drucker_effective_executive.py
├── tier3_leadership/              # 层级3 领导力与决策（能力层）
│   ├── m05_collins_level5_leadership.py
│   └── m06_munger_decision_analysis.py
├── tier4_execution/               # 层级4 目标管理与执行落地（行动层）
│   ├── m07_drucker_mbo.py
│   └── m08_collins_flywheel_execution.py
├── integration/                   # 汇聚层（高阶整合入口）
│   └── m09_strategic_advisor_expert.py
├── tools/                         # 配套工具脚本
│   ├── batch_invoke.py            #   批量调用
│   ├── validate_params.py         #   参数校验
│   └── verify_result.py           #   结果验证
├── prompts/                       # 提示词模板（团队集成/调试）
│   ├── m01_porter.md ... m09_strategic_advisor.md
└── tests/
    └── sample_manifest.json       # 批量调用示例清单
```

---

## 2. 模块间关系与调用方式

- **松耦合原则**：模块之间**不直接 import 彼此内部实现**。所有交互通过 `common/interface.py` 的 `SkillResult` 结构与 `common/loader.py` 的 `load_skill(module_id)` 完成。每个模块在文件底部 `register()` 自身契约与 `invoke()`。
- **独立调用**：任意模块均可单独运行（文件含 `__main__` 演示），不依赖其他模块运行时状态。
- **汇聚路径**：`m09 战略顾问专家` 作为整合入口，按 `problem_layer` 路由，经加载器调用对应模块，做跨层一致性检查后输出端到端方案；它本身也不感知各模块内部逻辑，只消费公共结果结构。

```
战略(m01) ─┐
组织(m02/m03/m04) ─┤→ 领导力与决策(m05/m06) ─┤→ 目标与执行(m07/m08) ─┐
                                                        │
                                          汇聚 → m09 战略顾问专家 ──（回指战略）
```

---

## 3. 统一接口约定

每个模块对外暴露：
- `CONTRACT`：`SkillContract`（参数清单 + 输出字段说明）
- `invoke(params: dict) -> SkillResult`：核心逻辑
- 返回值：`SkillResult`（`module_id / module_name / status / data / insights / recommendations / warnings`）

参数规范见各模块文件头部「输入参数定义」；输出字段见「输出结果定义」。

---

## 4. 快速开始

```bash
# 进入项目根目录
cd business-masters-skills

# 1) 校验入参（调用前自检）
python tools/validate_params.py --module m01 --params '{"industry_description":"连锁咖啡","five_forces":{"competitors":5,"new_entrants":4,"substitutes":4,"buyer_power":4,"supplier_power":2}}'

# 2) 独立运行某个模块（自带演示）
python -m tier1_strategy.m01_porter_competitive_strategy

# 3) 批量调用（回归/联调）
python tools/batch_invoke.py --manifest tests/sample_manifest.json --out results.json

# 4) 验证输出结构
python tools/verify_result.py --result results.json

# 5) 整合层路由调用
python -m integration.m09_strategic_advisor_expert
```

> 注：脚本通过 `sys.path` 自动注入项目根目录，务必在**项目根目录**下执行。

---

## 5. 交付物说明

| 交付物 | 说明 |
| --- | --- |
| 9 个技能文件 | 模块 1-9，含编号/映射/版本头注、功能描述、参数定义、输出定义、核心逻辑 |
| common 接口层 | 统一契约，保障松耦合与独立调用 |
| tools 工具集 | 批量调用 / 参数校验 / 结果验证 |
| prompts 提示词 | 每个模块一份，便于 AI 集成与团队调试 |
| tests 样例 | 批量调用 manifest，开箱即测 |
