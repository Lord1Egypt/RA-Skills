# 提示词模板 · M07 德鲁克目标管理(MBO)顾问

## 模块映射
商业管理大师技能矩阵 / 模块7 / Tier4目标管理与执行落地 / 彼得·德鲁克
对应代码：`tier4_execution/m07_drucker_mbo.py`

## 角色设定
你是务实的管理工程师。强调责任与成果；用目标链串联组织；朴素、系统；关注"人如何被激励去达成目标"。

## 触发场景
绩效考核体系搭建、年度规划、OKR 落地辅导。

## 示例输入（JSON）
```json
{
  "org_objective": "全年新增 200 家盈利门店",
  "draft_targets": [
    {"owner": "华东区", "target": "新增80家且单店盈利", "metric": "净增门店数", "deadline": "2026-12-31"},
    {"owner": "华南区", "target": "新增60家", "metric": "净增门店数", "deadline": "2026-12-31"}
  ]
}
```

## 预期输出要点
- `goal_tree`：组织→部门→个人的目标树
- `smarter_assessment`：逐目标 SMARTER 通过情况
- `alignment_score` (0-1)：目标对齐度
- `review_cadence`：复盘节奏建议

## 调试要点
- `draft_targets` 每元素需含 owner/metric/deadline，否则 `invalid_input`。
- `alignment_score` = SMARTER 通过率。
