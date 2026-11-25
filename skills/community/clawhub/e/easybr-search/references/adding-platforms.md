# 扩展一个搜索平台

现版优先验收百度、Google、Bing、抖音和小红书。微博、CSDN 等按同一协议逐步完善；平台目录可持续增加，单轮查询数和并发仍按任务预算执行。

常规扩展在脚本中完成，统一 SKILL 的“搜索→选源→读取→回答”指令继续复用。只有新增账号接入要求、特殊交互或新的授权范围时，才补相应的操作说明。

1. 在 `scripts/platforms.mjs` 注册平台 ID、名称、主机范围、公开搜索 URL、内容 URL 模式和 DOM 提示。查询必须作为一个参数编码；别名也在注册表中维护。模板要来自实际页面观察。
2. 在允许的浏览器环境只读搜索，观察正常结果、空态、登录和验证码状态。常规站点使用既有选择器提取器；复杂的公开跳转或卡片结构在 `scripts/extract.mjs` 中做窄适配。账号路由与签名地址放在运行目录的私有记录中。
3. 在 `tests/platforms.test.mjs` 和 `tests/extract.test.mjs` 加小型 DOM 夹具，验证内容 URL、标题、去重、阻断状态与实际正文范围。夹具使用合成内容与假签名，不复制整站页面。
4. 使用固定的 `platform-check` 对新平台实搜，修复后复测，记录真实状态。搜索和读正文分别验收；只有搜索卡片时返回 `search_page_only`，不能拼造未验证直链。
5. 沿用统一 `results.json`、`sources/`、流式事件与 `handoff.json`。读不到或搜索不了时生成原因和人工处理入口，其他授权分支继续；平台受限时由人工登录、验证或提供有效链接。

```sh
node scripts/platform-check.mjs --platforms PLATFORM_ID --query "实际测试问题" --output .local/new-platform-check
node --test tests/platforms.test.mjs tests/extract.test.mjs
```

`platforms` 列出已经注册的入口，实际可用性看当次运行回执。浏览器版本、平台页面和账号条件会变化，适配代码随版本回归后发布。
