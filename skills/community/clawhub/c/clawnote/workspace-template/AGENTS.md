# AGENTS.md

## Session Start

- 先读 `SOUL.md`
- 再读 `PERSONA.md`
- 再读 `USER.md`
- 再读 `FEISHU_COMMANDS.md`
- 读今天和昨天的 `memory/YYYY-MM-DD.md`；如果不存在，要在本轮结束前补建

## Mission

- 这不是一个单体 agent，而是一套三段式工作流：
  - `xhs-research`
  - `xhs-draft`
  - `xhs-publish-assist`
- 默认先发 Feishu 审稿；只有用户明确批准某一篇稿件后，才允许进入公开发布。

## Module 1: xhs-research

- 优先用本地搜索找最近 48 小时内值得写的 AI 新闻
- 至少交叉验证 2 个来源
- 跳过聚合问答站
- OpenClaw 实践只写本机真实发生过的事情

## Module 2: xhs-draft

- 只根据已确认事实写稿
- 保留“事实”和“个人判断”的边界
- 标题具体，正文短段落

## Module 3: xhs-publish-assist

- 保存 JSON draft package
- 生成 markdown 发布包
- 默认只输出预览
- 用户明确批准后才允许精确发布
- 删除动作必须走精确确认
