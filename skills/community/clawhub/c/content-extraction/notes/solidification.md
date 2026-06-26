# Solidification: content-extraction

## 固化目标

把 content-extraction 从“说明型技能”固化成“路由 + 执行计划 + 输出规范”的可复用模块。

## 已固化

- 路由识别：公众号 / 飞书文档 / 飞书知识库 / YouTube / 通用网页
- 执行计划：router 可直接输出可执行 spec
- 输出契约：统一 Markdown / frontmatter / 摘要 / 保存路径
- 失败契约：每层失败原因必须可解释
- 飞书映射：block → Markdown
- 示例集：公众号 / 飞书 / YouTube / 通用网页

## 固化后的使用方式

1. 先运行 router 识别来源
2. 再运行 executor 生成执行规范
3. 最后由工具层真正抓取并写出 Markdown

## 下一阶段

- 接真实 OpenClaw browser / feishu / transcript 调用
- 增加真实 URL 回归测试
- 归档保存策略和目录结构
