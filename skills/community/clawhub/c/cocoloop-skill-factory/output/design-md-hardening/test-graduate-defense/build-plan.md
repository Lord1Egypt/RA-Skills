# 构建计划

## 当前步骤

1. 编写测试 `spec.yaml`
2. 调用 builder 渲染最小测试 Skill
3. 检查渲染结果中是否包含 `references/design.md`
4. 生成示例 `.pptx`
5. 保留结构化 `slides.md` 作为备用内容稿

## 当前结果

- 已生成 `graduate-defense-demo.pptx`
- 已保留 `slides.md` 作为内容稿

## 仍存在的限制

- 当前环境没有现成的 PPT 渲染预览工具链
- `slides_test.py` 依赖 `numpy`，本地未安装
