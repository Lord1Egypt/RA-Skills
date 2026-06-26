# 路由示例

这份参考只在任务边界不清、或一个请求可能落到多个技能时再读取。

## 单技能直达

- “帮我分析这个项目入口和主流程”
  路由到 `$code-explore`

- “先别改代码，帮我设计实现方案”
  路由到 `$code-architect`

- “直接把这个功能实现出来”
  路由到 `$code-write`

- “这个报错怎么修”
  路由到 `$code-debug`

- “不改行为，帮我重构一下”
  路由到 `$code-refactor`

- “检查这里有没有 SQL 注入或越权”
  路由到 `$code-security`

- “帮我跑测试和 lint”
  路由到 `$shell-safe-exec`

- “帮我整理分支和提交信息”
  路由到 `$git-discipline`

## 多技能串联

- “给这个老项目加一个新接口”
  推荐顺序: `$code-explore` -> `$code-architect` -> `$code-write` -> `$shell-safe-exec`

- “这个接口报 500，修一下并确认测试通过”
  推荐顺序: `$code-explore` -> `$code-debug` -> `$code-write` -> `$shell-safe-exec`

- “把这块逻辑整理干净，但不要影响线上行为”
  推荐顺序: `$code-explore` -> `$code-refactor` -> `$shell-safe-exec`

- “审一下这个上传流程的安全问题，顺手修掉”
  推荐顺序: `$code-explore` -> `$code-security` -> `$code-write` -> `$shell-safe-exec`

- “改完之后帮我整理成一笔干净提交”
  推荐顺序: `$code-explore` -> `$code-write` -> `$shell-safe-exec` -> `$git-discipline`

## 决策规则

- 用户强调“先看、先分析、不要改”，优先 `$code-explore`
- 用户强调“给方案、拆步骤”，优先 `$code-architect`
- 用户强调“直接改、直接写”，优先 `$code-write`
- 用户强调“报错、异常、失败、崩溃”，优先 `$code-debug`
- 用户强调“优化结构、提取重复、提高可读性”，优先 `$code-refactor`
- 用户强调“漏洞、权限、注入、敏感信息”，优先 `$code-security`
- 用户强调“执行命令、跑测试、安装依赖”，优先 `$shell-safe-exec`
- 用户强调“分支、提交、历史、安全推送”，优先 `$git-discipline`
