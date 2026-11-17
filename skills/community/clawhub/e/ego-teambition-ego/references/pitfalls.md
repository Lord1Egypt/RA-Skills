# 避坑（Teambition 测试用例）

读取和 Phase 2a 单条写都走 `page.fetch`，不把点页面当主要手段。下面这些是脚本已经按接口语义处理过的，Agent 不要另写一套请求。

1. **用例不在任务接口里。** `teambition_cli`、MCP token、任务 TQL 都拿不到 testplan 用例。读计划、分组、用例，以及创建、改正文、改状态，走 `https://www.teambition.com/testcase/api/`。唯一的例外是移到回收站：`POST /api/testcases/{testcaseId}/archive`，不在 `/testcase/api/` 下。
2. **只认浏览器会话。** Open API token 在本阶段不可用。`session.mjs` 里的 open 传输会直接失败。不要让用户粘贴 Cookie。
3. **先 login-check。** 退出码 `2` 必须停。缺 `ego-browser` 也是 soft-fail，不要硬调浏览器。
4. **401 表示要在 Ego 里登录 teambition.com。** 不要改去调 open.teambition.com。
5. **JSON 不严格。** 响应偶发含未转义控制字符。解析会先严格解析，失败后再去掉控制字符重试。
6. **排序不稳定。** 同一查询两次顺序可能不同。不要依赖顺序。
7. **`totalSize` 恒为 0。** 以翻页耗尽为准，不要用这个字段当总数。stderr 的「共 N 条」是拉回来的条数。
8. **`pageToken` 是偏移量。** `0`、`100`、`200`… 按 pageSize 递增，不是 opaque token。最后一页 `nextPageToken` 为空。单次命令最多 30 页。
9. **TQL 只拼两个已验证字段。** `(_testplanId = {planId})`，可选 `AND groupId = {groupId}`。`uniqueId` 不能当 TQL 过滤。`get` 在浏览器侧逐页扫描，找到即停。
10. **`needTestCaseResult=true` 才带每步执行结果。** 本阶段列表和详情都打开它，以便步骤里有实际结果和截图。
11. **分组响应的键不固定。** 可能是数组，或 `result`，或 `groups`。空的 `result` 会再看 `groups`。
12. **常驻空间名字是 `tb-testcase api`。** `plan` / `groups` / `cases` / `get` / `flow-statuses` / `create` / `update` / `set-status` / `delete` 不调用 `finish`，以便下次复用。看完如果要收尾，跑 `cleanup`，它执行 `finish({ keep: [] })`。`cleanup` 只关本机浏览器空间，不改 Teambition 数据。
13. **check-login 用另一个空间。** `teambition-login-check` 默认 `finish({ keep: [] })`。`--keep` 才 `handOff()`。它不会关掉用例空间。
14. **写操作只有白名单。** 允许 `create`、`update`（标题 / 前置 / 步骤）、`set-status`、`delete`（archive）。不要自己拼别的 POST / PUT / DELETE。分组创建、移动、批量、回写步骤执行结果、单独改执行人，都不在本阶段。Open 文档里的 create / flowStatus **不是**这些浏览器路径的替身。
15. **`delete` 是移到回收站，而且必须 `--yes`。** 没有 `--yes` 就拒绝，请求不会发出。Agent 在加上 `--yes` 之前，必须向用户复述这条用例的 `uniqueId` 和标题，得到明确同意。不要把它说成物理删除。
16. **写路径认内部 id，不认 `uniqueId`。** 执行用例 `_id` 用于改状态和 archive。更新正文用 `_fromHubTestcaseId`，`testhubId` 用 `GET …/testhub`（单数）。执行用例上的 `_testhubId` 经常是 null。CLI 接受 `uniqueId` 或执行用例 `_id`，脚本先在计划里查出记录再写。创建响应里的 `_fromHubTestcaseId` 要留给后面的 update。
17. **401 不重试写。** 映射成「请在 Ego 里重新登录」。不要自动再 POST 一次，以免重复创建。也不要改用 Open token。
18. **ego 内嵌 Node 不继承 shell 环境变量。** 参数写在临时 entry 的 JSON 里，再交给 `ego-browser nodejs`。不要指望 `VAR=x ego-browser` 能读到 `VAR`。
19. **路径用技能相对路径。** 文档和示例不写个人机器上的产品目录。调用方自己提供测试计划 URL 或 id。沙箱 id 只写在 references 里当例子。
