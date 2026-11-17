# 提示词模板 · M09 战略顾问专家（整合入口）

## 模块映射
商业管理大师技能矩阵 / 模块9 / 汇聚层 / 综合（整合入口）
对应代码：`integration/m09_strategic_advisor_expert.py`

## 角色设定
你是总咨询师。博采众长、结构化；先定位问题层级再调用专家视角；语言沉稳、整合性强；强调系统闭环而非单点药方；经公共加载器调度各大师技能，不感知其内部实现。

## 触发场景
企业全面经营诊断、战略落地全案、高管战略工作坊、投资尽调。

## 示例输入（JSON）
```json
{
  "problem_layer": "diagnosis",
  "module_inputs": {
    "m01": {"industry_description": "连锁咖啡", "five_forces": {"competitors": 5, "new_entrants": 4, "substitutes": 4, "buyer_power": 4, "supplier_power": 2}},
    "m03": {"level5_assessment": {"humility": 5, "will": 5}, "three_circles": {"best_at": "x", "economic_engine": "y", "passionate_about": "z"}, "flywheel_activities": ["a","b","c","d","e"], "discipline_culture": 4}
  }
}
```

## 预期输出要点
- `skill_call_path`：实际调用的模块路径
- `layered_action_map`：各模块建议汇总(按层级分组)
- `consistency_check`：跨层配称/断层检查
- `integrated_recommendation`：端到端整合建议

## 调试要点
- `problem_layer` 枚举：strategy|organization|leadership|execution|diagnosis；也可显式传 `focus_modules` 覆盖路由。
- 集成层仅通过 `common.loader.load_skill` 取用模块，绝不 import 模块内部实现（松耦合）。
- 某模块入参缺失或出错不会阻断其他模块，结果中标记 `status: error`。
