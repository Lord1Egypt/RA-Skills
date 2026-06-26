# 滴答清单 MCP 工具路由

这份路由表用于约束 `dida-coach` 在调用滴答清单 MCP 时，优先使用哪些真实工具名。

不要自行发明类似 `get_today_tasks`、`create_timebox_task`、`list_all_tasks` 之类不存在的工具名。

## 时间盒落地模型

`dida-coach` 里的“时间盒”不是独立的 MCP 资源，而是通过滴答任务来实体化：

- 一个时间盒 = 一条真实任务
- 盒子的执行时段，靠任务的日期 / 截止时间字段承载
- 盒子的开始提醒、提前提醒、检查点提醒，靠 `create_task` 或 `update_task` 的提醒字段承载
- 如果需要把一个大任务拆成多个盒子，就创建多条任务，而不是假设存在单独的 `timebox` 工具

因此：

- 创建时间盒时，优先使用 `create_task` 或 `batch_add_tasks`
- 修改时间盒时，优先使用 `update_task`
- 完成时间盒时，优先使用 `complete_task`
- 每次创建或更新时间盒后，都要用 `get_task_by_id` 回读提醒和时间字段

如果回读结果里看不出提醒已经独立落盘，就不能对用户说“时间盒和提醒已经设置完成”。

## 查询任务

- 按关键词搜索任务：`search_task`
- 按任务 ID 读取完整内容：`get_task_by_id`
- 查询今天或相对时间范围内的未完成任务：`list_undone_tasks_by_time_query`
  - 支持：`today`、`last24hour`、`last7day`、`tomorrow`、`next24hour`
- 查询指定日期范围内的未完成任务：`list_undone_tasks_by_date`
- 查询指定清单中、指定日期范围内的已完成任务：`list_completed_tasks_by_date`
- 多条件组合筛选任务：`filter_tasks`

## 查询清单

- 列出所有清单：`list_projects`
- 按清单 ID 获取详情：`get_project_by_id`
- 获取清单详情并带出其中未完成任务：`get_project_with_undone_tasks`
- 在某个清单里查找特定任务：`get_task_in_project`

## 管理任务

- 创建单个任务：`create_task`
- 批量创建任务：`batch_add_tasks`
- 完成单个任务：`complete_task`
- 批量完成某清单中的多个任务：`complete_tasks_in_project`
  - 单次最多 20 个
- 更新任务属性：`update_task`
- 移动任务到其他清单：`move_task`
- 批量更新任务属性：`batch_update_tasks`

## 推荐路由

- “我今天有哪些任务？”
  - 优先：`list_undone_tasks_by_time_query(today)`
  - 如果用户还要看今天完成了什么，再补：`list_completed_tasks_by_date`

- “帮我创建一个任务”
  - 使用：`create_task`
  - 创建后立刻：`get_task_by_id`

- “帮我把任务拆成 3 个时间盒”
  - 优先：`batch_add_tasks`
  - 如果要逐个确认或逐个写不同字段：`create_task`
  - 创建后逐个：`get_task_by_id`

- “把这个任务标记完成”
  - 单个任务：`complete_task`
  - 清单里一批任务：`complete_tasks_in_project`

- “把任务改到下午 3 点 / 改优先级 / 改提醒”
  - 使用：`update_task`
  - 更新后立刻：`get_task_by_id`

- “给这个时间盒加开始提醒 / 提前 30 分钟提醒 / 检查点提醒”
  - 使用：`update_task`
  - 更新后立刻：`get_task_by_id`
  - 如果回读后提醒仍等于截止时间，只能说明截止时间更新了，不能说明提醒已单独设置成功

- “把任务移到另一个清单”
  - 使用：`move_task`
  - 移动后可用：`get_task_by_id` 或 `get_task_in_project` 校验

- “按清单看今天还没做完的”
  - 优先：`get_project_with_undone_tasks`
  - 如果还要加优先级、标签、状态等条件：`filter_tasks`

- 日复盘 / 周复盘
  - 未完成任务：`list_undone_tasks_by_time_query` 或 `list_undone_tasks_by_date`
  - 已完成任务：`list_completed_tasks_by_date`
  - 不要只看未完成任务就做完成率统计

## 回读校验要求

凡是创建、更新、移动、完成之后，都要至少回读一次，优先用：

- `get_task_by_id`
- 或与场景匹配的清单级查询工具

必须校验这些字段是否真的落盘：

1. 标题
2. 优先级
3. 截止时间
4. 提醒时间
5. 当前完成状态
