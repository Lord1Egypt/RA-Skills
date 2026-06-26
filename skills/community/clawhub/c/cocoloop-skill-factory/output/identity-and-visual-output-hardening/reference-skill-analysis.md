# 参考实现分析

## 本地生成链

- `factory-skill-builder/scripts/_spec_common.cjs`
  当前负责 slug 与展示名推导，需要改成优先读取显式字段。
- `factory-skill-builder/scripts/render_skill_from_spec.cjs`
  当前负责 render gate、manifest 生成和 `design_md` 资产复制，需要接入名称 gate 与视觉输出 gate。
- `factory-skill-builder/scripts/validate_platform_skill.cjs`
  当前负责 spec gate 与产物校验，需要接入新字段的机械校验。

## 本地搜索入口

- `utils/cli/search-registry.py`
  当前已能统一查询 `cocoloop`、`clawhub`、`github`。
  这轮继续补 `--exact-slug`，让它直接返回精确命中结果。

## 已有视觉链

- `design_md`
  已经能输出 `references/design.md`。
- `visual_storytelling`
  已经能承接视觉叙事型产物。
  这轮不改它的抽象层，只补“什么时候必须带 `design_md`”。
