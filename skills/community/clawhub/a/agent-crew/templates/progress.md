# Role Progress Template

<!--
  使用说明:
  1. 此文件作为 .claude/teams/<team_name>/<role_name>/progress.md 的初始模板
  2. 角色完成任务后，在文件末尾追加完成记录
  3. progress.md 仅存摘要，详情放在 workspace/ 中
  4. 当前状态必须始终更新在文件顶部
-->

## Current Status

<!-- 一句话描述当前工作状态 -->

> 正在 <做什么>

## Completed Tasks

<!--
  每条完成任务格式:
  ### YYYY-MM-DD: <任务摘要>
  - **详情**: `<workspace/xxx_detail.md>` (引用工作区文档)
  - **结果**: <最终结果/产出>
-->

<!-- 示例:
### 2026-04-15: 完成 RAG 索引构建脚本
- **详情**: `workspace/rag-index-build.md`
- **结果**: 产出了可执行的 build_index.py 脚本
-->

## Pending Tasks

<!--
  每条待办格式:
  - [ ] <任务描述>
  - **阻塞**: <如有阻塞，说明原因>
  - **详情**: `<workspace/xxx_plan.md>` (可选，如有计划文档)
-->

<!-- 示例:
- [ ] 集成 Jina embedding 服务
  - **阻塞**: 等待 API key 配置
-->
