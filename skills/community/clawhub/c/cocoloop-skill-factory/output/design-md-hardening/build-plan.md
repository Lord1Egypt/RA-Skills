# 构建计划

## 当前回合

1. 更新本地 `ref/design-md/` 预设库与索引
2. 新增 `design_md` 协议字段并同步文档
3. 修改生成链，输出 `references/design.md` 与 `references/design-md/`
4. 修改平台校验逻辑，检查设计资产
5. 用独立 `gpt-5.4` 子 agent 生成“研究生毕业答辩 PPT skill”并产出示例 PPT

## 测试产物建议

- `output/design-md-hardening/spec.yaml`
- `output/design-md-hardening/test-graduate-defense/`
  - `spec.yaml`
  - 渲染出的测试 Skill
  - 示例 PPT 或其导出结果

## 后续可选项

- 为 `design_md` 增加更细的品牌 token 结构
- 接入更多设计预设
- 为最终 Skill 增加字体或模板资产复制
