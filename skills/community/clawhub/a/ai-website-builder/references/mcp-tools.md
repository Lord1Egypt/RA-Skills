# 建站 MCP 工具参考

本文档记录建站 MCP 服务提供的工具。工具作用于当前 MCP 连接对应的站点；调用前必须确认 MCP 地址和 Bearer Token。

> 适用范围：本文件是 MCP 工具的权威参数参考（参数、返回值、限制、推荐调用顺序）。模板侧 `FnGet*` 系列函数的返回字段不在此处，见 `references/advanced-data-interface.md`。

## MCP 前置要求

任何 MCP 工具调用前，必须先向用户确认当前目标站点的 MCP 完整地址和 Bearer Token。

- 未提供地址和 Token 时，不调用 `test` 或任何其他工具。
- 不得猜测、复用示例地址或沿用其他站点的 Token。
- 切换站点后，必须重新获取新站点的地址和 Token。
- Token 仅由 MCP 客户端放入 `Authorization: Bearer <token>` 请求头，不作为工具参数传入。
- 当新的 MCP 链接成功后，请清除 agent 智能体记忆里关于旧的MCP的相关内容，避免记忆混乱导致使用了不正确的MCP。

## 通用连接规则

- 协议：JSON-RPC 2.0。
- 认证请求头：`Authorization: Bearer <token>`。
- Token 不作为任何工具参数传入。
- 工具调用前先使用 `test` 检查连通性。
- 所有工具只作用于当前连接对应的站点，不要混用不同站点的 ID。
- 切换到其他站点时，必须重新获取并确认新站点的 MCP 地址和 Bearer Token，不得沿用上一站点的连接信息或资源 ID。
- 查询工具可以在认证成功后直接调用。
- 写入工具必须在执行前向用户展示目标和影响并取得确认。

## 工具总览

| 工具 | 类型 | 主要用途 |
| --- | --- | --- |
| `test` | 查询/诊断 | 测试 MCP 连通性并回显请求参数 |
| `list_custom_form` | 查询 | 列出当前站点普通自定义表单 |
| `add_custom_form` | 写入 | 新增普通自定义表单及字段 |
| `edit_custom_form` | 写入 | 修改普通自定义表单或询盘表单、字段或删除字段 |
| `add_faq` | 写入 | 新增 FAQ |
| `add_faq_class` | 写入 | 新增 FAQ 分类 |
| `del_faq` | 高风险删除 | 永久删除 FAQ |
| `del_faq_class` | 高风险删除 | 永久删除 FAQ 分类 |
| `edit_faq` | 写入 | 修改 FAQ |
| `edit_faq_class` | 写入 | 修改 FAQ 分类 |
| `get_faq_info` | 查询 | 获取单条 FAQ 详情 |
| `list_news_class` | 查询 | 列出完整新闻分类树 |
| `list_faq` | 查询 | 分页列出 FAQ |
| `list_faq_class` | 查询 | 列出 FAQ 分类 |
| `list_page` | 查询 | 分页列出首页和AI自由页 |
| `get_page_info` | 查询 | 获取当前站点AI自由页的页面信息和源码 |
| `list_product_class` | 查询 | 列出完整产品分类树 |
| `get_news_info` | 查询 | 获取单篇文章详情 |
| `get_news_list` | 查询 | 分页查询已发布文章 |
| `get_product_info` | 查询 | 获取单个产品基础详情 |
| `get_product_list` | 查询 | 分页查询已发布产品 |
| `get_site_seo` | 查询 | 获取当前站点整站 SEO |
| `edit_site_seo` | 写入 | 修改当前站点整站 SEO |
| `get_seo_list` | 查询 | 分页查询产品、文章、分类或页面 SEO 列表 |
| `edit_seo` | 写入 | 设置指定产品、文章、分类或页面 SEO |
| `edit_seo_batch` | 写入 | 保存产品与文章批量 SEO 规则 |
| `list_seo_redirect` | 查询 | 列出当前站点 301 跳转规则 |
| `add_seo_redirect` | 写入 | 新增当前站点 301 跳转规则 |
| `edit_seo_redirect` | 写入 | 修改当前站点 301 跳转规则 |
| `del_seo_redirect` | 高风险删除 | 永久删除当前站点 301 跳转规则 |
| `list_gallery` | 查询 | 分页列出当前站点相册 |
| `list_gallery_item` | 查询 | 分页列出指定相册图片 |
| `add_gallery` | 写入 | 新增一个站点相册 |
| `add_gallery_item` | 写入 | 向相册新增图片 |
| `edit_gallery` | 写入 | 修改相册名称和描述 |
| `edit_gallery_item` | 写入 | 修改相册图片及其信息 |
| `change_gallery_item_sort` | 写入 | 修改相册图片排序 |
| `del_gallery` | 高风险删除 | 永久删除相册及图片文件 |
| `del_gallery_item` | 高风险删除 | 永久删除相册图片及文件 |
| `edit_company_info` | 写入 | 修改网站名称和公司联系信息 |
| `get_online_query_list` | 查询 | 分页查询在线查询配置列表 |
| `get_enquiry_form_id` | 查询/可能写入 | 获取当前站点在线询盘表单 ID |
| `list_enquiry_records` | 查询 | 分页查询当前站点在线询盘记录 |
| `list_sqlite_db` | 查询 | 列出当前站点的 SQLite 数据库 |
| `list_sqlite_tables` | 查询 | 列出指定数据库的用户数据表 |
| `get_sqlite_table_info` | 查询 | 获取指定表的定义信息 |
| `query_sqlite` | 查询 | 执行 SQLite 查询 SQL |
| `add_news` | 写入 | 新增一篇文章，可创建草稿或立即发布 |
| `add_news_class` | 写入 | 新增一个文章分类 |
| `edit_news` | 写入 | 部分更新一篇文章 |
| `edit_news_class` | 写入 | 修改一个文章分类 |
| `add_product` | 写入 | 新增并立即发布一个精简产品 |
| `add_product_class` | 写入 | 新增一个产品分类 |
| `edit_product` | 写入 | 部分更新一个产品 |
| `edit_product_class` | 写入 | 修改一个产品分类 |
| `upload_file` | 写入 | 上传站点资源库文件 |
| `upload_product_image` | 写入 | 上传产品主图素材 |
| `create_sqlite_db` | 写入 | 新建一个 SQLite 数据库 |
| `upload_sqlite_db` | 写入 | 上传 SQLite 数据库文件 |
| `execute_sqlite` | 高风险写入 | 执行非查询 SQL，可增删改表和数据 |
| `save_ai_page` | 写入 | 新建或更新单个自定义 HTML 页面 |
| `save_ai_page_batch` | 写入 | 通过 Base64 ZIP 批量导入页面和静态资源 |
| `del_page` | 高风险删除 | 永久删除当前站点的一张 AI 页面 |
| `set_home_page` | 写入 | 将AI自由页设为首页 |
| `set_page_friendlyurl` | 写入 | 新增、修改或删除页面友好 URL |
| `clear_site_cache` | 维护操作 | 清理当前站点缓存 |

## `test`

用途：测试 MCP 服务连通性，返回工具名和请求参数。

参数：

```json
{
  "message": "string，必填，需要回显的测试文本",
  "count": "integer，可选，测试次数，最小值为 1，默认值为 1",
  "options": "object，可选，附加测试参数，允许任意属性"
}
```

要求：

- `message` 必须提供。
- `count` 不得小于 1。
- 首次连接时建议使用简短、不含敏感信息的测试文本。

## `list_custom_form`

用途：列出当前站点的普通自定义表单。

参数：无参数。输入对象必须为空，不接受额外属性。

使用规则：

- 当模型判断页面需要表单时，应优先调用本工具，不直接生成独立静态表单。
- 将返回的表单 `ID` 和 `Name` 展示给用户，并等待用户明确选择。
- 用户选择前不得猜测表单 ID 或生成绑定到任意表单的最终代码。
- 用户已经提供表单 ID 时，也应调用本工具验证该 ID 属于当前站点。
- 用户选定后，在页面模板中使用 `FnGetCustomForm(表单ID)` 接入系统动态表单。
- 返回列表为空时，提示用户先在站点后台创建表单；除非用户明确要求，否则不降级为静态表单。

返回：

- 仅返回 `FormType` 为 `CustomForm` 的 `tbl_form` 记录。
- 按 `ID` 倒序排列。
- 每项仅包含 `ID` 和 `Name`。
- 不返回询盘表单、产品留言表单或其他类型表单。

## `add_custom_form`

用途：为当前站点新建一个普通自定义表单，并可在同一次调用中新增字段。本工具只负责新建，不提供修改模式，新建记录的 `FormType` 固定为 `CustomForm`，不能创建在线询盘表单、产品留言表单或其他特殊表单。修改已有普通自定义表单或询盘表单请使用 `edit_custom_form`。

这是写入工具。调用前必须向用户展示表单名称、字段列表、通知配置、支付配置及可能的副作用，并取得明确确认。

参数：

```json
{
  "name": "报名表",
  "intro": "请填写报名信息",
  "enableEmailNotification": 0,
  "enableSmsNotification": 0,
  "receivedEmail": "",
  "isPay": 0,
  "payAmount": 0,
  "payTips": "",
  "payType": 0,
  "calculations": "",
  "fields": [
    {
      "id": "NewName",
      "name": "姓名",
      "fieldType": 1,
      "isRequire": 1,
      "validateType": 1,
      "placeholder": "请输入姓名"
    }
  ]
}
```

参数说明：

- `name`：必填，表单名称，1 至 50 个字符。
- `intro`：可选，表单介绍，最多 200 个字符。
- `enableEmailNotification`、`enableSmsNotification`、`isPay`、`payType`：可选，只能为 `0` 或 `1`，默认值为 `0`。
- `receivedEmail`：可选，邮件通知接收地址。启用邮件通知时必填；多个地址使用换行、分号或逗号分隔，最多 10 个。
- `payAmount`：可选，非负数字。
- `payTips`：可选，支付提示语。
- `calculations`：可选，表单计算配置字符串，可引用字段 ID 或字段临时 ID。
- `fields`：可选，字段对象数组，数组顺序决定 `ShowOrder`；默认空数组。

字段参数：

- `id`：可选。新增字段只能使用 `New` 开头的临时 ID，例如 `NewName`；不能使用已有数字 ID。临时 ID 可被 `fieldValuesRel`、`calculationsItem` 和 `calculations` 引用，保存后会替换为真实字段 ID。
- `name`：必填，字段名称，1 至 50 个字符。
- `intro`、`placeholder`、`icon`、`extendName`：可选字符串。
- `fieldType`：可选，`1` 单行文本、`2` 多行文本、`3` 单选、`4` 下拉、`5` 多选、`6` 图片上传、`7` 中国国内地区、`8` 时间、`9` 文件上传、`10` 多图上传、`11` 静态文本、`12` 国际地区、`13` 公司名（单行文本）、`14` 姓名（单行文本）、`15` 邮箱（单行文本）。
- `fieldValues`：可选，单选、下拉、多选的选项，使用 `|` 或换行分隔；保存时会规范为 `|` 分隔。
- `isRequire`、`isShow`、`isSmsValidate`、`isEmailValidate`、`isShowTitle`、`pcShowType`、`mobileShowType`：可选，只能为 `0` 或 `1`。
- `validateType`：可选，`0` 不验证、`1` 文本、`2` 数字、`3` 手机、`4` 固话、`5` 固话或手机、`6` 邮箱、`7` 身份证；仅 `fieldType=1/13/14/15` 的单行文本类和 `fieldType=2` 多行文本有效，其他字段必须为 `0`。
- `isSmsValidate=1` 仅适用于 `fieldType=1/13/14/15` 且 `validateType=3` 的手机号字段，并会自动设置为必填。
- `isEmailValidate=1` 仅适用于 `fieldType=1/13/14/15` 且 `validateType=6` 的邮箱字段，并会自动设置为必填；页面需要配合邮箱验证码输入框和 `sendEmailCode` 接口完成真实性验证，不能使用短信接口。
- `fieldValuesRel`、`calculationsItem`：可选，可传 JSON 字符串、对象或数组，用于选项联动和字段计算。

返回：

```json
{
  "success": true,
  "FormID": 123,
  "Name": "报名表",
  "FormType": "CustomForm",
  "fieldCount": 1,
  "fields": [
    {
      "ID": 456,
      "Name": "姓名",
      "FieldType": 1,
      "IsEmailValidate": 0,
      "ShowOrder": 0
    }
  ]
}
```

限制：

- 表单创建、字段写入不是跨调用事务；调用失败时已经创建的表单或字段不会自动回滚，失败后应重新查询确认实际状态。
- 不得把 Token 放入工具参数；认证由 MCP 客户端通过请求头完成。
- 创建后页面接入仍须使用 `list_custom_form`/用户选择的表单 ID 和 `FnGetCustomForm(表单ID)`，不得猜测 ID。
- `add_custom_form` 的输入 schema 没有 `formId` 或更新模式；即使工具元数据提到修改场景，实际也只能新建普通自定义表单，修改已有普通表单或询盘表单必须调用 `edit_custom_form`。

## `edit_custom_form`

用途：修改当前站点一个普通自定义表单或询盘表单的主体配置，新增或更新字段，以及按需删除字段。仅支持已有 `FormType=CustomForm` 或 `FormType=EnquiryForm` 的表单。

这是写入工具。调用前必须向用户展示当前站点、表单 ID、表单名称、表单类型、拟修改字段、删除字段及通知/支付影响，并取得明确确认。修改询盘表单前还应明确提示该表单可能正在被产品询盘、联系我们或其他页面使用。

参数：

```json
{
  "formId": 123,
  "name": "更新后的报名表",
  "intro": "新的说明",
  "fields": [
    {
      "id": 456,
      "name": "姓名",
      "fieldType": 1,
      "isRequire": 1
    },
    {
      "id": "NewPhone",
      "name": "手机",
      "fieldType": 1,
      "validateType": 3,
      "isRequire": 1
    }
  ],
  "deleteFieldIds": [789]
}
```

参数说明：

- `formId`：必填，当前站点普通自定义表单或询盘表单 ID，必须是正整数或正数字符串。
- `name`、`intro`、`enableEmailNotification`、`enableSmsNotification`、`receivedEmail`、`isPay`、`payAmount`、`payTips`、`payType`、`calculations`：可选，仅提交需要修改的表单主体字段。
- `fields`：可选。带数字 `id` 的字段表示更新已有字段；带 `New` 开头临时 ID 或不带 `id` 的字段表示新增字段。字段数组顺序决定本次提交字段的 `ShowOrder`；未列出的已有字段保持不变。
- `deleteFieldIds`：可选，要删除的当前表单字段 ID 数组。字段不能同时出现在 `fields` 和 `deleteFieldIds` 中。

字段配置、字段类型、校验类型、`isSmsValidate`、`isEmailValidate` 和临时 ID 规则与 `add_custom_form` 相同。

删除语义：

- `NoDel=1` 的字段禁止删除。
- 表单没有提交记录时，字段会物理删除。
- 表单已有提交记录时，字段不会物理删除，而是设置 `IsShow=0` 隐藏，以保留历史数据。
- 未显式列入 `deleteFieldIds` 的字段不会被删除。

返回：

```json
{
  "success": true,
  "FormID": 123,
  "Name": "更新后的报名表",
  "FormType": "CustomForm 或工具实际返回的表单类型",
  "fieldCount": 2,
  "fields": [
    {
      "ID": 456,
      "Name": "姓名",
      "FieldType": 1,
      "IsEmailValidate": 0,
      "ShowOrder": 0
    },
    {
      "ID": 790,
      "Name": "手机",
      "FieldType": 1,
      "ShowOrder": 1
    }
  ]
}
```

限制：

- 更新表单、字段和删除字段不是跨调用事务；中途失败时已完成的修改不会自动回滚，失败后应使用 `list_custom_form` 或后台查询确认实际状态。
- 修改页面中的表单代码前，仍需先按表单规则读取并确认当前表单，不能用静态表单替代系统表单。
- `add_custom_form` 只能创建 `FormType=CustomForm` 的普通自定义表单，不能创建在线询盘表单或其他特殊表单。
- `edit_custom_form` 同时支持 `FormType=CustomForm` 和 `FormType=EnquiryForm`；在线询盘表单 ID 应先使用 `get_enquiry_form_id` 获取并确认。
- 修改询盘表单字段可能影响所有引用该表单的产品详情、联系我们和其他询盘页面，执行前必须检查并明确确认影响范围。

## `add_faq`

用途：在当前站点新增一条 FAQ。工具默认立即发布，也可以通过 `status=0` 保存为草稿。

这是写入工具。调用前必须确认问题、答案、分类、置顶状态、排序值和发布状态。

参数：

```json
{
  "question": "如何联系公司？",
  "answer": "<p>请通过联系我们页面提交信息。</p>",
  "classIds": [12],
  "isTop": 0,
  "status": 1,
  "showOrder": 0
}
```

参数说明：

- `question`：必填，FAQ 问题，不能仅包含空白字符。
- `answer`：必填，FAQ 答案，可传 HTML，不能仅包含空白字符。
- `classIds`：可选，当前站点 FAQ 分类 ID 数组；省略或传空数组表示未分类。每个 ID 必须是正整数或正数字符串，不能重复。
- `isTop`：可选，是否置顶，`0` 为否，`1` 为是，默认 `0`。
- `status`：可选，发布状态，`0` 为草稿，`1` 为发布，默认 `1`。
- `showOrder`：可选，非负整数排序值，默认 `0`。

返回：成功返回新 FAQ 的 ID、问题、答案、分类、置顶状态、发布状态和排序等摘要信息；具体字段以工具实际返回为准。

## `add_faq_class`

用途：在当前站点新增一个 FAQ 分类。FAQ 分类没有父级、排序或层级结构。

这是写入工具。调用前必须确认分类名称和图标。

参数：

```json
{
  "name": "售后服务",
  "icon": ""
}
```

- `name`：必填，FAQ 分类名称，不能仅包含空白字符。
- `icon`：可选，分类图标字段，默认空字符串。

返回：成功返回新分类的 ID、名称和图标等信息。

## `del_faq`

用途：物理删除当前站点指定的一条 FAQ，删除后不可恢复。

参数：

```json
{
  "id": 123
}
```

限制：

- `id` 必须是当前站点 FAQ 的正整数 ID 或正数字符串。
- 重复删除或使用其他站点的 FAQ ID 会返回错误。
- 输入对象不接受额外属性。

调用前必须向用户展示当前站点、FAQ ID、问题和删除影响，并取得针对该 FAQ 的明确永久删除确认。不得复用其他写入操作的确认。

## `del_faq_class`

用途：物理删除当前站点指定的 FAQ 分类，删除后不可恢复。

参数：

```json
{
  "classId": 12
}
```

限制：

- `classId` 必须是当前站点 FAQ 分类的正整数 ID 或正数字符串。
- 删除分类不会修改已有 FAQ 中保存的 `ClassID` 分类字符串，这是现有后台行为。
- 输入对象不接受额外属性。

调用前必须展示分类 ID、分类名称、关联 FAQ 影响，并取得明确永久删除确认。

## `edit_faq`

用途：部分修改当前站点的一条 FAQ。未提交的字段保持原值，至少需要提交一个更新字段。

参数：

```json
{
  "id": 123,
  "question": "更新后的问题",
  "answer": "<p>更新后的答案。</p>",
  "classIds": [],
  "isTop": 0,
  "status": 1,
  "showOrder": 0
}
```

参数说明：

- `id`：必填，要修改的当前站点 FAQ ID。
- `question`：可选，新的 FAQ 问题，不能仅包含空白字符。
- `answer`：可选，新的 FAQ 答案，可传 HTML，不能仅包含空白字符。
- `classIds`：可选，新的 FAQ 分类 ID 数组；传空数组表示未分类。
- `isTop`：可选，是否置顶，`0` 为否，`1` 为是。
- `status`：可选，`0` 为草稿，`1` 为发布。
- `showOrder`：可选，新的非负整数排序值。

调用前应先使用 `get_faq_info` 读取当前 FAQ，展示拟修改字段并取得确认。涉及 `status=1` 时，明确提示该 FAQ 会发布。

## `edit_faq_class`

用途：部分修改当前站点的 FAQ 分类。未提交的字段保持原值，至少需要提交 `name` 或 `icon` 之一。

参数：

```json
{
  "classId": 12,
  "name": "新的分类名称",
  "icon": ""
}
```

参数说明：

- `classId`：必填，要修改的当前站点 FAQ 分类 ID。
- `name`：可选，新的分类名称，不能仅包含空白字符。
- `icon`：可选，新的分类图标；传空字符串可清空图标。

调用前应先使用 `list_faq_class` 核对分类，展示拟修改字段并取得确认。

## `get_faq_info`

用途：获取当前站点一条 FAQ 的完整信息。

参数：

```json
{
  "id": 123
}
```

限制和返回：

- `id` 必须是当前站点 FAQ ID，且为正整数或正数字符串。
- FAQ 不存在或不属于当前站点时返回工具错误。
- 成功返回 `ID`、`Question`、`Answer`、`ClassID`、`classIds`、`ClassName`、`IsTop`、`Status`、`ShowOrder` 和 `CrTime`。

## `list_faq`

用途：分页列出当前站点 FAQ，支持按问题/答案关键字、分类、置顶状态和发布状态筛选。

参数：

```json
{
  "keyword": "",
  "classId": -1,
  "isTop": 0,
  "status": 1,
  "page": 1,
  "pageSize": 20
}
```

参数说明：

- `keyword`：可选，按 `Question` 或 `Answer` 模糊搜索，默认空字符串。
- `classId`：可选，`-1` 表示全部分类；正整数只返回关联该分类的 FAQ，默认 `-1`。
- `isTop`：可选，`0` 为否，`1` 为是；不传时返回全部。
- `status`：可选，`0` 为草稿，`1` 为发布；不传时返回全部。
- `page`：可选，页码从 `1` 开始，默认 `1`。
- `pageSize`：可选，每页 `1` 至 `100` 条，默认 `20`。

限制和返回：

- 查询范围严格限定为当前站点。
- 返回结构与后台 FAQ 管理列表一致，包含分页信息。
- 每条记录保留后台原始 FAQ 字段、`Answer` 和 `ClassName`。

## `list_faq_class`

用途：列出当前站点全部 FAQ 分类。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：

- 每个分类包含 `ClassID`、`Name`、`Icon` 和 `FaqCount`。
- `FaqCount` 表示当前分类关联的 FAQ 数量。
- FAQ 分类没有父级或层级结构。

## `list_news_class`

用途：列出当前站点完整的新闻分类树。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：分类树按后台显示顺序返回。每个分类仅包含：

- `ClassID`
- `ParentID`
- `ShowOrder`
- `Name`
- `sublist`：该分类的子分类列表

## `add_news_class`

用途：为当前站点新增一个文章分类。

参数：

```json
{
  "name": "string，必填，分类名称，长度至少为 1",
  "parentId": "integer 或数字字符串，可选，默认 0"
}
```

限制和返回：

- 每次调用只新增一个分类。
- `parentId=0` 表示新增一级分类。
- 非零 `parentId` 必须属于当前站点。
- 成功返回新分类的 `ClassID`、`Name`、`ParentID` 和 `Url`。

调用前确认分类名称和父分类；非一级分类必须先使用 `list_news_class` 核对父分类 ID。

## `add_news`

用途：为当前站点新增一篇文章。`content` 使用原始 HTML，不需要 Base64 编码。

参数：

```json
{
  "title": "string，必填，长度至少为 1",
  "content": "string，必填，原始 HTML，长度至少为 1",
  "classIds": "array，可选，当前站点文章分类 ID，默认 [0]",
  "status": "integer，可选，0=草稿，1=立即发布，默认 1",
  "publishTime": "string，可选，可被 PHP strtotime 识别的发布时间",
  "previewImage": "string，可选，文章缩略图服务器路径，使用upload_file的结果，不需要域名部分",
  "author": "string，可选，文章作者",
  "source": "string，可选，文章来源",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词",
  "description": "string，可选，SEO 描述",
  "descriptor": "string，可选，文章摘要",
  "showOrder": "integer，可选，最小值 0，默认 0"
}
```

限制和返回：

- `classIds` 的每项可为不小于 0 的整数或仅包含数字的字符串。
- `classIds` 不能重复。
- 默认分类为 `[0]`；`0` 表示未分类，不能与其他分类同时使用。
- 非零分类必须属于当前站点，应先用 `list_news_class` 验证。
- `status=0` 为草稿，`status=1` 为立即发布；工具默认立即发布。
- 使用 `previewImage` 时，先调用 `upload_file` 上传图片并使用其返回的绝对 URL。
- `descriptor` 可选，用于保存文章摘要，默认空字符串。
- 成功返回 `ArticleID`、`Title` 和 `Url`。

调用前必须确认标题、HTML 内容、分类、发布时间和发布状态。用户未明确要求发布时，使用 `status=0` 创建草稿。

## `edit_news`

用途：部分更新当前站点的一篇文章。

参数：

```json
{
  "articleId": "integer 或正数字符串，必填，当前站点文章 ID",
  "title": "string，可选，传入时不能为空",
  "content": "string，可选，文章原始 HTML，传空字符串可清空内容",
  "classIds": "array，可选，文章分类 ID，空数组改为未分类 [0]",
  "status": "integer，可选，0=草稿，1=发布",
  "publishTime": "string，可选，PHP 可识别的日期字符串",
  "previewImage": "string，可选，文章缩略图服务器路径，使用upload_file的结果，不需要域名部分",
  "author": "string，可选，文章作者",
  "source": "string，可选，文章来源",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词",
  "description": "string，可选，SEO 描述",
  "descriptor": "string，可选，文章摘要，传空字符串可清空",
  "showOrder": "integer，可选，最小值 0，文章排序值"
}
```

限制和行为：

- `articleId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- `articleId` 必须属于当前站点。
- 未传入的字段保留原值。
- 至少需要提交一个实际更新字段，不能只提交 `articleId`。
- `classIds` 传空数组会改为未分类 `[0]`；`0` 不能与其他分类同时使用。
- 文章分类 ID 应先通过 `list_news_class` 验证。
- `title` 传入时不能为空。
- `content` 传空字符串会清空文章内容。
- `descriptor` 传空字符串会清空文章摘要。

调用前应先使用 `get_news_info` 读取当前文章，向用户展示将修改的字段并获得确认。涉及 `status=1` 时，明确提示文章会发布。

## `edit_news_class`

用途：修改当前站点指定 ID 的文章分类。

参数：

```json
{
  "classId": "integer 或正数字符串，必填，当前站点文章分类 ID",
  "name": "string，可选，新的文章分类名称",
  "parentId": "integer 或数字字符串，可选，新的父分类 ID，0 表示一级分类",
  "showOrder": "integer，可选，新的排序值，必须为非负整数"
}
```

限制和行为：

- `classId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- `classId` 必须属于当前站点。
- `name`、`parentId` 和 `showOrder` 均可选，未提交的字段保持原值。
- 至少需要提交一个实际更新字段，不能只提交 `classId`。
- `parentId=0` 表示移动到一级分类。
- 非零 `parentId` 必须属于当前站点。
- 不能将分类移动到自身或自身的子分类下。
- `showOrder` 必须为非负整数。
- 文章分类没有图片字段。

调用前应先使用 `list_news_class` 核对分类及父分类，向用户展示将修改的字段并取得确认。

## `get_news_info`

用途：获取当前站点一篇文章的详情。

参数：

```json
{
  "articleId": "integer 或正数字符串，必填，文章 ID"
}
```

限制和返回：

- `articleId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- 仅允许查询当前站点。
- 文章不存在时返回工具错误。
- 成功返回 `SiteDataAdapter::getOneNews()` 提供的原始文章字段及 `ClassList`，不改名、不额外裁剪字段。

## `get_news_list`

用途：查询当前站点已发布文章列表。

参数：

```json
{
  "classId": "integer 或数字字符串，可选，默认 0",
  "keyword": "string，可选，按文章标题搜索，默认空字符串",
  "page": "integer，可选，从 1 开始，默认 1",
  "pageSize": "integer，可选，最小 1，最大 100，默认 20",
  "sortField": "UpTime | CrTime | PublishTime | ShowOrder | ArticleID，可选，默认 UpTime",
  "sort": "asc | desc，可选，默认 desc"
}
```

限制和返回：

- `classId=0` 表示全部分类，并包含子分类文章。
- `classId` 必须为不小于 0 的整数或数字字符串。
- `pageSize` 最大为 100。
- `sortField` 只能使用 `UpTime`、`CrTime`、`PublishTime`、`ShowOrder` 或 `ArticleID`。
- `sort` 只能使用 `asc` 或 `desc`。
- 返回 `SiteDataAdapter::getNews()` 产生的文章记录，不改名、不额外裁剪字段。

## `list_page`

用途：按站点后台页面列表的相同范围，列出当前站点的首页和AI自由页。

参数：

```json
{
  "keyword": "string，可选，匹配页面 Title 或 ID，默认空字符串",
  "page": "integer，可选，从 1 开始，默认值为 1",
  "pageSize": "integer，可选，最小值 1，最大值 500，默认值为 20"
}
```

限制和返回：

- 仅包含当前站点、站点类型的首页和AI自由页。
- 仅返回 `PageType` 为 `1` 和 `99` 的页面。
- 排除城市分站页面和扩展页面。
- 按 `PageType`、`ID` 升序排列。
- 返回 JSON 包含 `success`、`curpage`、`pagesize`、`pagecount` 和 `list`。
- `list` 每项仅包含 `ID`、`PageType`、`PageName`、`Title` 和 `Url`。

## `get_page_info`

用途：获取当前站点 AI 页面信息和源码。修改既有 AI 页面前必须先调用本工具读取原始 `SourceCode`，不得盲目覆盖。

参数：

```json
{
  "pageId": "integer 或正数字符串，必填"
}
```

限制：

- `pageId` 必须是当前站点页面 ID，最小值为 1。
- 仅支持 `EnableCustomTpl=1` 的AI自由页。
- 非 AI 页面会返回“此页面不是AI页面，不支持获取信息”。
- 输入对象不接受额外属性。

成功返回：仅包含以下五个字段：

- `ID`
- `PageName`
- `Url`
- `SourceCode`
- `codePath`

使用规则：

- 先通过 `list_page` 查询并确认目标页面 ID。
- 再使用本工具判断目标是否为可读取的 AI 页面，并读取现有 `SourceCode`。
- 基于读出的源码生成修改方案，再向用户展示更新目标和影响，得到确认后才调用 `save_ai_page`。
- 若工具提示页面不是 AI 页面，不得使用 `save_ai_page` 直接覆盖；应说明限制并改用合适的页面编辑方式或请求用户提供可编辑的 AI 页面。

## `list_product_class`

用途：列出当前站点完整的产品分类树。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：分类树按后台显示顺序返回。每个分类仅包含：

- `ClassID`
- `ParentID`
- `ShowOrder`
- `Name`
- `sublist`：该分类的子分类列表

## `add_product_class`

用途：为当前站点新增一个产品分类。

参数：

```json
{
  "name": "string，必填，分类名称，长度至少为 1",
  "parentId": "integer 或数字字符串，可选，默认 0"
}
```

限制和返回：

- 每次调用只新增一个分类。
- `parentId=0` 表示新增一级分类。
- 非零 `parentId` 必须属于当前站点，应先用 `list_product_class` 验证。
- 本工具仅支持设置分类名称和父分类，不支持分类图片或独立页面。
- 成功返回分类 ID、名称、父分类 ID 和前台分类 URL。

调用前确认分类名称和父分类。

## `edit_product_class`

用途：修改当前站点指定 ID 的产品分类。

参数：

```json
{
  "classId": "integer 或正数字符串，必填，当前站点产品分类 ID",
  "name": "string，可选，新的产品分类名称",
  "parentId": "integer 或数字字符串，可选，新的父分类 ID，0 表示一级分类",
  "showOrder": "integer，可选，新的排序值，必须为非负整数",
  "image": "string，可选，产品分类图片地址；传空字符串可清除图片"
}
```

限制和行为：

- `classId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- `classId` 必须属于当前站点。
- `name`、`parentId`、`showOrder` 和 `image` 均可选，未提交的字段保持原值。
- 至少需要提交一个实际更新字段，不能只提交 `classId`。
- `parentId=0` 表示移动到一级分类。
- 非零 `parentId` 必须属于当前站点。
- 不能将分类移动到自身或自身的子分类下。
- `showOrder` 必须为非负整数。
- `image` 传空字符串可清除分类图片。
- 更新分类图片前，先调用 `upload_file` 获取当前站点的图片路径；传入 `image` 时只填写工具返回的服务器图片路径，不包含域名。

调用前应先使用 `list_product_class` 核对分类及父分类，向用户展示将修改的字段并取得确认。

## `upload_product_image`

用途：上传当前站点的产品主图素材。该工具不会自动将图片绑定到产品。

参数：

```json
{
  "fileName": "string，必填，包含扩展名的图片文件名，不能包含目录路径",
  "fileBase64": "string，可选，纯 Base64 或 Data URI",
  "sourceUrl": "string，可选，HTTP/HTTPS 远程图片地址"
}
```

限制和返回：

- 仅支持 `webp`、`png`、`jpg`、`jpeg`，文件最大为 5 MiB。
- `fileBase64` 与 `sourceUrl` 必须且只能提供一个。
- `sourceUrl` 必须以 `http://` 或 `https://` 开头。
- 成功返回产品大图文件名 `fileName`、产品小图文件名 `SmallFileName` 及对应 URL。

后续调用 `add_product` 时，将返回的 `fileName` 和 `SmallFileName` 原样传入 `mainImage`；不得自行构造文件名。

## `add_product`

用途：在当前站点新增并立即发布一个精简产品。

参数：

```json
{
  "name": "string，必填，产品名称，长度至少为 1",
  "classIds": "array，可选，当前站点产品分类 ID，默认 [0]",
  "mainImage": {
    "fileName": "string，upload_product_image 返回的大图文件名",
    "SmallFileName": "string，upload_product_image 返回的小图文件名"
  },
  "price": "非负数字或数字字符串，可选，默认 0",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词，写入 ProKeyword",
  "seoDescription": "string，可选，SEO 描述",
  "summary": "string，可选，产品简介，写入 ProDesc",
  "content": "string，可选，单一产品详情HTML或JSON格式的多详情，多详情时格式如[{"title":"产品详情","content":"详情内容"},{"title":"产品参数","content":"参数内容"}]"
}
```

限制：

- `classIds` 每项可为不小于 0 的整数或仅包含数字的字符串。
- 默认分类为 `[0]`；`0` 表示未分类，不能与其他分类同时使用。
- 非零分类必须属于当前站点，应先用 `list_product_class` 验证。
- `mainImage` 可省略；提供时必须同时包含 `fileName` 与 `SmallFileName`，且二者都必须来自当前站点产品图片目录，fileName 和 SmallFileName 均支持用逗号分隔多个图片文件名，两个字段的图片数量必须一致，并按顺序一一对应。
- `price` 必须为非负数。
- `content` 会以“产品详情”为标题保存为单项详情。
- 本工具会立即发布产品。
- 不支持 SKU、规格、标签、会员权限、筛选、附件、定时发布等高级后台字段。

调用前必须确认产品名称、分类、价格、主图、SEO、简介和详情内容，并明确告知产品将立即发布。

## `edit_product`

用途：部分更新当前站点的精简产品。

参数：

```json
{
  "productId": "integer 或正数字符串，必填，当前站点产品 ID",
  "name": "string，可选，传入时不能为空",
  "classIds": "array，可选，产品分类 ID，空数组改为未分类 [0]",
  "mainImage": "object、null 或空对象，可选，产品主图",
  "price": "非负数字或数字字符串，可选",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词",
  "seoDescription": "string，可选，SEO 描述",
  "summary": "string，可选，产品简介",
  "content": "string，可选，单一产品详情HTML或JSON格式的多详情，多详情时格式如[{"title":"产品详情","content":"详情内容"},{"title":"产品参数","content":"参数内容"}]，空字符串可清空详情"
}
```

`mainImage` 对象结构：

```json
{
  "fileName": "string，产品大图文件名",
  "SmallFileName": "string，产品小图文件名"
}
```

限制和行为：

- `productId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- `productId` 必须属于当前站点。
- 未传入的字段保留原值。
- 至少需要提交一个实际更新字段，不能只提交 `productId`。
- `classIds` 传空数组会改为未分类 `[0]`；`0` 不能与其他分类同时使用。
- 产品分类 ID 应先通过 `list_product_class` 验证。
- `name` 传入时不能为空。
- 省略 `mainImage` 表示保留原图。
- `mainImage=null` 或空对象表示清空主图。
- 更新主图时应使用 `upload_product_image` 返回的两个文件名，不得自行拼接。
- `price` 必须为非负数。

调用前应先使用 `get_product_info` 读取当前产品，向用户展示将修改的字段并获得确认。

## `get_product_info`

用途：获取当前站点一个产品的基础详情。

参数：

```json
{
  "productId": "integer 或正数字符串，必填，产品 ID"
}
```

限制和返回：

- `productId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- 仅允许查询当前站点。
- 产品不存在时返回工具错误。
- 成功返回 `SiteDataAdapter::getOneProductBase()` 提供的原始产品字段及 `ClassList`，不改名、不额外裁剪字段。

## `get_product_list`

用途：查询当前站点已发布产品列表。

参数：

```json
{
  "classId": "integer 或数字字符串，可选，默认 0",
  "keyword": "string，可选，按产品名称搜索，默认空字符串",
  "page": "integer，可选，从 1 开始，默认 1",
  "pageSize": "integer，可选，最小 1，最大 100，默认 20",
  "sortField": "CrTime | UpTime | ShowOrder | ProductID | Price | SalesCount，可选，默认 CrTime",
  "sort": "asc | desc，可选，默认 desc"
}
```

限制和返回：

- `classId=0` 表示全部分类，并包含子分类产品。
- `classId` 必须为不小于 0 的整数或数字字符串。
- `pageSize` 最大为 100。
- `sortField` 只能使用 `CrTime`、`UpTime`、`ShowOrder`、`ProductID`、`Price` 或 `SalesCount`。
- `sort` 只能使用 `asc` 或 `desc`。
- 返回 `SiteDataAdapter::getProduct()` 产生的产品记录，不改名、不额外裁剪字段。

## `get_site_seo`

用途：获取当前站点的整站 SEO 信息，用于生成首页、全站公共头部元信息或核对当前整站标题与描述。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：成功返回 `success=true` 和以下字段：

- `SeoTitle`：整站 SEO 标题。
- `SeoKeyword`：整站 SEO 关键词。
- `SeoDescription`：整站 SEO 描述。
- `SiteName`：当前站点名称。

如果对应字段未配置，返回空字符串。

## `edit_site_seo`

用途：部分更新当前站点的整站 SEO。未提交的字段保持原值，显式传入空字符串可以清空字段。

这是写入工具。调用前应先用 `get_site_seo` 读取当前值，向用户展示当前站点、拟修改字段、原值和新值，并取得明确确认。整站 SEO 变更会清理当前站点缓存。

参数：

```json
{
  "title": "云指建站 - 专业企业网站建设",
  "keywords": "云指建站,企业建站,网站建设",
  "description": "云指建站为企业提供网站建设服务。"
}
```

参数说明：

- `title`：可选，整站 SEO 标题。
- `keywords`：可选，整站 SEO 关键词。
- `description`：可选，整站 SEO 描述。
- 三个字段至少提交一个，且都必须是字符串。
- 标题始终可以更新。
- 关键词和描述受当前版本 SEO 功能许可限制；无 SEO 许可时，即使提交也不会写入这两个字段。
- 显式传入空字符串可清空对应字段；未提交字段保持原值。

返回：成功返回 `success=true`、`SeoTitle`、`SeoKeyword`、`SeoDescription` 和 `SiteName`，字段值表示保存后的实际状态。

## `get_seo_list`

用途：分页查询当前站点的 SEO 列表。产品、文章、分类和页面使用不同的目标 ID，编辑前应先使用本工具核对 `seoType`、ID、当前 TDK 和独立分类页面状态。

参数：

```json
{
  "seoType": "product",
  "page": 1,
  "pageSize": 20
}
```

参数说明：

- `seoType`：必填，只能为 `product`、`article`、`productClass`、`articleClass` 或 `page`。
- `page`：可选，正整数，从 1 开始，默认 1。
- `pageSize`：可选，正整数，默认 20，最大 100。

各类型的列表语义：

- `product`：产品列表。`ID` 为 `ProductID`，包含 `Name`、`Title`、`Keywords`、`Description` 和后台编辑地址 `Url`；按产品 ID 倒序。
- `article`：文章列表。`ID` 为 `ArticleID`，`Name` 为文章标题，包含 `Title`、`Keywords`、`Description` 和后台编辑地址 `Url`；按文章 ID 倒序。
- `productClass`：产品分类列表。按分类树顺序和层级返回 `RecID`、`ClassID`、`ClassParentID`、`Level`、`Name`、`EnableCust`、`Title`、`Keywords`、`Description`；`ID` 为当前站点类型关联的独立分类页面 ID，调用 `edit_seo` 时仍使用 `ClassID`。
- `articleClass`：文章分类列表，字段含义与 `productClass` 相同。
- `page`：系统页和自定义页列表。每项包含 `ID`、`Name`、`Title`、`Keywords`、`Description` 和 `Url`；自定义页额外带 `IsCustom=true`。

返回结构：

- 顶层返回 `success`、`list`、`curpage`、`pagesize`、`pagecount` 和 `totalcount`。
- 空字段会被规范为空字符串。
- 分类启用了独立分类页面时，返回的 SEO 来自关联页面当前值；未启用独立页面时，返回分类自身保存的 SEO。
- 页面类型为自定义模板页面时，工具会从当前页面 HTML 的 `<title>`、keywords meta 和 description meta 中读取值。

注意：本工具主要是查询工具，但 `page` 类型按后台内置页面范围读取；许可允许的扩展系统页记录缺失时，读取过程可能补齐缺失的系统页记录。应在调用前向用户说明该查询可能触发系统页初始化。

## `edit_seo`

用途：设置当前站点指定对象的 SEO 标题、关键词和描述。三个文本字段都必填，但允许传空字符串清空。

这是写入工具。调用前应先用 `get_seo_list` 读取目标对象当前 SEO，向用户展示对象类型、ID、名称、URL 和完整 TDK 新值，并取得明确确认。

参数：

```json
{
  "seoType": "product",
  "id": 123,
  "title": "产品名称 - 网站名称",
  "keywords": "产品名称,关键词",
  "description": "产品详细介绍摘要"
}
```

参数说明：

- `seoType`：必填，只能为 `product`、`article`、`productClass`、`articleClass` 或 `page`。
- `id`：必填，正整数或正数字符串。不同类型对应不同 ID：
  - `product`：当前站点 `ProductID`。
  - `article`：当前站点 `ArticleID`。
  - `page`：当前站点页面 ID。
  - `productClass` 或 `articleClass`：当前站点分类 `ClassID`，不要传列表返回的 `RecID`。
- `title`、`keywords`、`description`：必填字符串，允许为空字符串。
- 本工具是整体覆盖 TDK，不是部分更新；三个字段都必须提供。

行为和影响：

- 只能编辑当前站点的产品、文章、分类和页面；目标不存在或属于其他站点时返回工具错误。
- 修改产品时写入产品 SEO 字段，修改文章时写入文章 SEO 字段。
- 修改分类时始终更新分类自身 SEO；如果当前站点类型已启用独立分类页面，并且分类关联了有效页面，会同步更新关联页面的 SEO。
- 修改 `EnableCustomTpl=1` 的AI自由页或独立分类页面时，除更新页面数据外，还会同步替换自定义 HTML 文件中的 `<title>`、keywords meta 和 description meta。如果 HTML 缺少 head 或对应标签，系统会按规则补入。
- 清空 TDK 只清空目标对象字段和自定义 HTML 对应标签，不会自动生成默认 SEO。
- 修改成功后会清理当前站点缓存。

返回：成功返回 `success=true` 和 `msg=操作成功`。

## `edit_seo_batch`

用途：保存当前站点的 SEO 批量规则，用于统一控制产品、文章页面 SEO 标题、关键词和描述的生成。

这是写入工具。调用前应先用 `get_seo_list` 或整站 SEO 查询了解当前状态，向用户展示启用状态、自动填充状态、标题分隔符、产品规则、文章规则及对后续 SEO 的影响，并取得明确确认。

参数：

```json
{
  "state": true,
  "isAutoFill": false,
  "titleSymbol": "-",
  "product": {
    "title": "{{Name}} - {{SiteName}}",
    "keywords": "{{Name}},{{SiteName}}",
    "description": "{{Name}},{{Class}},{{Label}}"
  },
  "article": {
    "title": "{{Name}} - {{SiteName}}",
    "keywords": "{{Name}},{{SiteName}}",
    "description": "{{Name}},{{Class}},{{Label}}"
  }
}
```

参数说明：

- `state`：必填，是否启用批量 SEO，可传布尔值、`0`/`1` 或 `0`/`1` 字符串。
- `isAutoFill`：必填，是否自动填充 SEO，可传布尔值、`0`/`1` 或 `0`/`1` 字符串。
- `titleSymbol`：必填，标题拼接分隔符，只能是英文逗号 `,`、下划线 `_`、短横线 `-`、竖线 `|` 或中文顿号 `、`。
- `product`：必填对象，包含 `title`、`keywords`、`description` 三个产品规则字符串。
- `article`：必填对象，包含 `title`、`keywords`、`description` 三个文章规则字符串。
- 规则可使用后台支持的变量。常用示例包括 `{{Name}}`、`{{SiteName}}`、`{{Class}}`、`{{Label}}`；实际可用变量以返回的 `defaultData` 为准。

返回：成功返回 `success=true` 和当前完整配置：

- `defaultData`：产品与文章批量 SEO 可用的默认变量列表。
- `State`：启用状态。
- `IsAutoFill`：自动填充状态。
- `TitleSymbol`：标题分隔符。
- `Product`：产品规则详情。
- `Article`：文章规则详情。

若站点还没有批量 SEO 配置，首次保存时会创建该配置。

## SEO 301 跳转通用规则

- 301 跳转规则只作用于当前 MCP 端点对应的站点，不能混用其他站点的规则。
- 本组工具只管理 `RedirectType=1` 的 301 跳转，不处理自定义 404 配置。
- `rawUrl` 必须是站内来源路径且以 `/` 开头；来源地址带扩展名时，仅允许 `html` 或 `htm`。
- `targetUrl` 必须是站内路径或以 `http://`、`https://` 开头的地址；外部地址带扩展名时，仅允许 `html`。
- 来源地址不能与目标地址相同。
- 同一站点的来源地址不能重复；目标地址不能已经是其他规则的来源地址，以避免跳转冲突和死循环。
- 修改时会排除当前记录再进行重复来源和目标冲突检查。
- 新增、修改、删除成功后都会清理当前站点的 301 缓存。
- 写操作前必须先使用 `list_seo_redirect` 核对当前规则，并向用户展示当前站点、来源地址、目标地址及对搜索引擎和旧链接的影响。

## `list_seo_redirect`

用途：列出当前站点的 301 跳转规则，供新增、修改、删除和生成页面跳转说明前核对现有规则使用。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：

- 成功返回 `success=true` 和 `list`。
- 只返回当前站点 `RedirectType=1` 的规则，不返回自定义 404 配置。
- 结果按创建时间倒序排列。
- 每条规则包含 `ID`、`SiteID`、`RawUrl`、`TargetUrl`、`RedirectType` 和 `CrTime`。
- `RawUrl` 为原始来源地址，`TargetUrl` 为跳转目标地址。

## `add_seo_redirect`

用途：为当前站点新增一条 301 跳转规则，用于将旧地址或失效地址跳转到新地址。

这是写入工具。调用前必须向用户展示当前站点、来源地址、目标地址、扩展名规则、重复来源限制和 301 缓存清理影响，并取得明确确认。

参数：

```json
{
  "rawUrl": "/old-page.html",
  "targetUrl": "/new-page.html"
}
```

参数说明：

- `rawUrl`：必填，原始来源地址，必须以 `/` 开头。
- `targetUrl`：必填，跳转目标地址，可以是站内路径或 HTTP/HTTPS 地址。
- 来源地址带扩展名时只允许 `html`、`htm`。
- 外部目标地址带扩展名时只允许 `html`。
- 来源地址不能与目标地址相同。
- 来源地址不能与当前站点已有规则重复。
- 目标地址不能已经是当前站点其他规则的来源地址。
- 保存成功后清理 301 缓存。

返回：成功返回 `success=true` 和新增的 `redirect` 对象；该对象包含 `ID`、`SiteID`、`RawUrl`、`TargetUrl`、`RedirectType` 和 `CrTime`。

## `edit_seo_redirect`

用途：修改当前站点的一条 301 跳转规则。`rawUrl` 和 `targetUrl` 必须同时提交，这是对来源与目标的整体更新，不是部分更新。

这是写入工具。调用前应先用 `list_seo_redirect` 读取当前规则，向用户展示当前站点、记录 ID、当前来源地址、当前目标地址、新来源地址、新目标地址及对旧链接的影响，并取得明确确认。

参数：

```json
{
  "redirectId": 12,
  "rawUrl": "/renamed-page.html",
  "targetUrl": "https://example.com/renamed-page.html"
}
```

参数说明：

- `redirectId`：必填，正整数或正数字符串，必须是当前站点 `RedirectType=1` 的规则 ID。
- `rawUrl`：必填，新的原始来源地址，必须以 `/` 开头。
- `targetUrl`：必填，新的跳转目标地址，可以是站内路径或 HTTP/HTTPS 地址。
- 地址校验规则与 `add_seo_redirect` 相同。
- 修改时会排除当前记录，检查来源重复和目标成为其他规则来源等冲突。
- 保存成功后清理 301 缓存。

返回：成功返回 `success=true` 和修改后的 `redirect` 对象；该对象包含 `ID`、`SiteID`、`RawUrl`、`TargetUrl`、`RedirectType` 和 `CrTime`。

## `del_seo_redirect`

用途：物理删除当前站点的一条 301 跳转规则，删除后不可恢复。

参数：

```json
{
  "redirectId": 12
}
```

参数和删除限制：

- `redirectId`：必填，正整数或正数字符串。
- `redirectId` 必须属于当前站点，且记录类型必须是 `RedirectType=1`。
- 本工具不能删除自定义 404 配置。
- 删除是物理删除，完成后会清理 301 缓存。

调用前必须使用 `list_seo_redirect` 核对当前站点、规则 ID、来源地址和目标地址，向用户说明删除后旧来源地址将不再自动跳转，搜索引擎和外链访问会回到来源地址的实际页面或 404 行为，并取得针对该规则的明确永久删除确认。不得复用其他操作的确认。

返回：成功返回 `success=true` 和被删除的 `redirectId`。

## `list_gallery`

用途：分页列出当前站点的站点相册，供页面生成、相册图片查询和编辑前核对目标使用。

参数：

```json
{
  "keyword": "string，可选，按相册名称 Title 模糊搜索，默认空字符串",
  "status": "integer 或 0/1 字符串，可选，0=停用，1=启用，不传时返回全部状态",
  "page": "integer 或正数字符串，可选，从 1 开始，默认 1",
  "pageSize": "integer 或正数字符串，可选，默认 20，最大 100"
}
```

限制和返回：

- 查询范围严格限定为当前 MCP 端点对应的站点和 `GalleryType=sitegallery` 的站点相册。
- `keyword` 按相册名称 `Title` 模糊搜索。
- `status` 只能为 `0` 或 `1`；`0` 表示停用，`1` 表示启用；不传时返回全部状态。
- `page` 必须为正整数，`pageSize` 必须为正整数且不超过 100。
- 结果按创建时间倒序返回。
- 返回 `list`、`curpage`、`pagesize`、`pagecount` 和 `count`；`list` 保留后台 `tbl_gallery` 相册记录字段。

调用前不需要写入确认。编辑或删除相册前，应先用本工具核对相册 ID、名称、状态和当前站点归属。

## `list_gallery_item`

用途：分页列出当前站点指定相册中的图片项，供图片页面生成、编辑、排序和删除前核对目标使用。

参数：

```json
{
  "galleryId": "integer 或正数字符串，必填，当前站点相册 ID",
  "keyword": "string，可选，按图片文件名 Image 模糊搜索，默认空字符串",
  "page": "integer 或正数字符串，可选，从 1 开始，默认 1",
  "pageSize": "integer 或正数字符串，可选，默认 20，最大 100"
}
```

限制和返回：

- `galleryId` 必须属于当前站点的站点相册，否则返回工具错误。
- `keyword` 按图片文件名 `Image` 模糊搜索。
- `page` 必须为正整数，`pageSize` 必须为正整数且不超过 100。
- 结果按 `ShowOrder` 升序、图片项 `ID` 倒序排列。
- 返回 `list`、`curpage`、`pagesize`、`pagecount`、`outMaxImgNum` 和 `count`；`list` 保留后台 `tbl_galleryitem` 图片项记录字段。
- `outMaxImgNum=true` 表示当前相册图片数量已达到 50 张上限。

## `add_gallery`

用途：在当前站点新增一个站点相册。相册创建后默认启用。

这是写入工具。调用前必须向用户展示相册名称和描述并取得明确确认。

参数：

```json
{
  "name": "案例展示",
  "description": "公司项目案例图片"
}
```

参数说明：

- `name`：必填，非空相册名称。
- `description`：可选，相册描述，默认空字符串；可以传空字符串。
- 本工具仅支持相册名称和描述，不支持设置 Banner、状态或相册类型。

返回：

```json
{
  "success": true,
  "GalleryID": 123,
  "Name": "案例展示",
  "Description": "公司项目案例图片"
}
```

## `add_gallery_item`

用途：向当前站点指定相册新增一张图片。创建第一张图片时，如果相册没有 Banner，系统会自动将该图片设为 Banner。

这是写入工具。调用前必须确认目标相册、图片来源、文件名、标题、描述、跳转链接和排序值。

参数：

```json
{
  "galleryId": 123,
  "fileName": "case-01.jpg",
  "sourceUrl": "https://example.com/case-01.jpg",
  "title": "项目案例一",
  "intro": "项目现场图片",
  "url": "/cases/case-01.html",
  "showOrder": 0
}
```

参数说明：

- `galleryId`：必填，正整数或正数字符串，必须属于当前站点相册。
- `fileName`：必填，带扩展名的文件名，只能是文件名，不能包含目录路径。
- `fileBase64` 与 `sourceUrl`：必须且只能提供一个。`fileBase64` 支持纯 Base64、Base64URL 和 Data URI；`sourceUrl` 仅支持 HTTP/HTTPS。
- 图片扩展名和实际内容必须匹配，仅支持 `jpg`、`jpeg`、`png`、`gif`、`webp`，图片大小最大 2 MiB。
- `title`、`intro`、`url`：可选，分别为标题、描述和点击跳转链接，默认空字符串。
- `showOrder`：可选，非负整数或数字字符串；未传时自动使用当前相册最大排序值加一。
- 每个相册最多保存 50 张图片。

返回：

```json
{
  "success": true,
  "ItemID": 456,
  "GalleryID": 123,
  "Image": "generated-name.jpg",
  "ImageUrl": "/comdata/{siteId}/gallery/generated-name.jpg",
  "Title": "项目案例一",
  "Intro": "项目现场图片",
  "Url": "/cases/case-01.html",
  "ShowOrder": 0
}
```

## `edit_gallery`

用途：部分修改当前站点相册的名称和描述。未提交的字段保持原值，描述可以清空。

这是写入工具。调用前应先用 `list_gallery` 核对相册，展示相册 ID、当前值和拟修改值，再取得明确确认。

参数：

```json
{
  "galleryId": 123,
  "name": "更新后的案例展示",
  "description": "更新后的相册说明"
}
```

参数说明：

- `galleryId`：必填，当前站点相册 ID。
- `name`：可选，新的非空相册名称。
- `description`：可选，新的相册描述；传空字符串可清空。
- `name` 和 `description` 至少需要提交一个；未提交字段保持原值。
- 不支持修改 Banner、状态或相册类型。

返回：成功返回当前相册的 `GalleryID`、`Name` 和 `Description`，并包含 `success=true`。

## `edit_gallery_item`

用途：部分修改当前站点相册图片项的图片、标题、描述、跳转链接或排序值。未提交字段保持原值。

这是写入工具。调用前应先用 `list_gallery_item` 核对图片项，展示目标图片和拟修改字段，再取得明确确认。

参数：

```json
{
  "itemId": 456,
  "fileName": "case-01-new.webp",
  "sourceUrl": "https://example.com/case-01-new.webp",
  "title": "更新后的标题",
  "intro": "更新后的描述",
  "url": "/cases/case-01.html",
  "showOrder": 1
}
```

参数说明：

- `itemId`：必填，当前站点相册图片项 ID。
- `title`、`intro`、`url`、`showOrder`：可选；字符串字段传空字符串可清空，`showOrder` 必须为非负整数。
- 替换图片时，`fileName`、`fileBase64`/`sourceUrl` 必须同时提供；`fileBase64` 与 `sourceUrl` 必须且只能提供一个。
- `fileName` 只能是文件名，不能包含目录路径；图片仅支持 `jpg`、`jpeg`、`png`、`gif`、`webp`，最大 2 MiB，实际内容必须与扩展名匹配。
- 不提供图片来源时只修改其他提交的字段；至少要提交一个实际更新字段。
- 如果被替换图片是相册 Banner，系统会同步将 Banner 更新为新图片。

返回：成功返回 `success=true` 以及当前图片项的 `ItemID`、`GalleryID`、`Image`、`ImageUrl`、`Title`、`Intro`、`Url` 和 `ShowOrder`。

## `change_gallery_item_sort`

用途：修改当前站点相册图片项的排序值。只修改目标图片的 `ShowOrder`，不会自动重排同相册其他图片；数值越小越靠前。

这是写入工具。调用前应先用 `list_gallery_item` 核对图片项和当前排序，展示新排序值并取得明确确认。

参数：

```json
{
  "itemId": 456,
  "showOrder": 0
}
```

限制和返回：

- `itemId` 必须属于当前站点相册图片项。
- `showOrder` 必须为非负整数或数字字符串。
- 成功返回 `success=true`、`ItemID`、`GalleryID` 和新的 `ShowOrder`。

## `del_gallery`

用途：物理删除当前站点指定的站点相册。删除后不可恢复。

参数：

```json
{
  "galleryId": 123
}
```

删除影响：

- 删除相册记录及其全部图片项记录。
- 删除当前站点 `gallery` 目录中相册图片项对应的图片文件。
- 这是不可恢复的物理删除，不会自动保留备份。

调用前必须使用 `list_gallery` 核对当前站点、相册 ID、名称、状态和图片数量，向用户说明图片文件也会被删除，并取得针对该相册的明确永久删除确认。不得复用其他操作的确认。

返回：成功返回 `success=true` 和被删除的 `GalleryID`。

## `del_gallery_item`

用途：物理删除当前站点的一个相册图片项。删除后不可恢复。

参数：

```json
{
  "itemId": 456
}
```

删除影响：

- 删除图片项数据库记录和对应的当前站点 `gallery` 目录图片文件。
- 如果删除的图片是相册 Banner，系统会自动切换为同相册其他图片；没有其他图片时清空 Banner。
- 这是不可恢复的物理删除，不会自动保留备份。

调用前必须使用 `list_gallery_item` 核对图片项所属相册、文件名、图片 URL 和 Banner 影响，展示删除影响并取得针对该图片项的明确永久删除确认。

返回：成功返回 `success=true`、被删除的 `ItemID` 和 `GalleryID`。

## `edit_company_info`

用途：部分更新当前站点的网站名称和公司联系信息。未提交的字段保持原值，显式传入空字符串可以清空字段。

这是写入工具。调用前必须向用户展示当前站点、拟修改字段、原值和新值，并取得明确确认。涉及页眉、页脚、联系我们或结构化数据展示时，应先核对需要使用的字段。

参数：

```json
{
  "siteName": "云指建站",
  "company": "示例科技有限公司",
  "shortName": "示例科技",
  "contact": "张三",
  "tel": "13800000000",
  "email": "service@example.com",
  "phone": "010-12345678",
  "fax": "010-12345679",
  "address": "北京市朝阳区示例路 1 号",
  "postCode": "100000"
}
```

参数说明：

- 所有字段均为可选字符串，但每次调用至少提交一个字段。
- `siteName`：网站名称。
- `company`：公司名称。
- `shortName`：公司简称。
- `contact`：联系人。
- `tel`：业务联系手机。
- `email`：业务联系邮件。
- `phone`：固定电话。
- `fax`：传真号码。
- `address`：详细地址。
- `postCode`：邮政编码。
- 显式传入空字符串可以清空字段；未提交字段保持原值。
- 本工具不支持公司类型、公司网址、成立时间、地区、主营行业、经营模式、公司简介、公司介绍、备案、地图密钥、访问开关、图标等其他站点配置。
- 修改成功后会更新站点信息任务状态并清理当前站点相关缓存。

返回：成功返回 `success=true` 以及当前站点的完整信息字段：`siteName`、`company`、`shortName`、`contact`、`tel`、`email`、`phone`、`fax`、`address` 和 `postCode`。

## `get_online_query_list`

用途：列出当前站点的在线查询配置列表。

参数：

```json
{
  "keyword": "string，可选，按查询名称 Name 模糊搜索，默认空字符串",
  "status": "integer，可选，0=启用，1=关闭；不传时返回全部状态",
  "page": "integer，可选，从 1 开始，默认 1",
  "pageSize": "integer，可选，最小 1，最大 100，默认 20"
}
```

限制和返回：

- 查询范围严格限定为当前 MCP 端点对应的站点。
- 列表按 `ID` 倒序返回。
- `status` 只能使用 `0` 或 `1`；`0` 表示启用，`1` 表示关闭。
- 不传 `status` 时返回全部状态。
- `page` 最小值为 1。
- `pageSize` 最小值为 1，最大值为 100。
- 列表项仅返回基础摘要字段：
  - `ID`
  - `Name`
  - `Desc`
  - `Status`
  - `StartTime`
  - `EndTime`
  - `BtnName`
  - `CrTime`
  - `Number`：该查询被查询了多少次

## SQLite 通用规则

- 所有 SQLite 工具只作用于当前 MCP 端点对应的站点。
- `dbName` 必须是合法文件名，格式为 `^[A-Za-z0-9_]+\\.(db|sqlite)$`。
- `dbName` 不允许包含路径、中文、空格、连字符或其他扩展名。
- MCP 请求无状态，每次调用 SQLite 工具都必须显式传入 `dbName`。
- `query_sqlite` 是只读查询；`execute_sqlite` 会改变数据或结构。
- 执行可能删除数据、删除表或修改结构的 SQL 前，必须先展示 SQL 目标与影响并取得用户确认。

## `list_sqlite_db`

用途：列出当前站点的 SQLite 数据库。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：

- 只返回数据库文件名和由 `create_sqlite_db` 或 `upload_sqlite_db` 保存的说明。
- 不返回服务器绝对路径、数据库内容或敏感信息。

## `get_enquiry_form_id`

用途：获取当前站点的在线询盘表单 ID。

参数：无参数。输入对象必须为空，不接受额外属性。

行为和返回：

- 对应后台 `EnquiryformmanageController::GetFormID()` 的逻辑。
- 如果站点已配置有效的 `CustomEnquiryFormID`，直接返回该 ID。
- 如果未配置，或原表单不存在，会自动初始化默认“在线询盘”表单、默认字段并更新站点配置。
- 首次调用可能产生数据写入。
- 调用前应说明可能自动初始化表单和字段，并取得用户同意。

## `list_enquiry_records`

用途：分页列出当前站点的在线询盘记录，供页面或后台展示、审核状态查询和客户跟进核对使用。

参数：

```json
{
  "keyword": "客户名称",
  "status": -1,
  "page": 1,
  "pageSize": 20
}
```

参数说明：

- `keyword`：可选，按表单提交数据关键字搜索，默认空字符串。
- `status`：可选，审核状态：`-1` 全部，`0` 未审核，`1` 已审核，默认 `-1`。
- `page`：可选，正整数，从 1 开始，默认 1。
- `pageSize`：可选，正整数，默认 20，最大 100。

返回：

- 成功返回 `success=true`、`list`、`curpage`、`pagesize`、`pagecount` 和 `total`。
- 结果按提交时间倒序排列。
- 每条记录包含 `form_info` 和 `product_list`：
  - `form_info`：包含 `ID`、`Status`、`CrTime`，以及当前在线询盘表单可见字段的“字段名称:提交值”。
  - `product_list`：询盘产品数组，保留产品名称、图片、规格、数量等原始字段；没有产品时为空数组。
- `Status` 表示询盘审核状态，具体取值应与后台询盘记录一致。
- 查询范围严格限定为当前 MCP 端点对应的站点。

注意：本工具按当前站点在线询盘表单读取记录。如果站点尚未配置有效的在线询盘表单，底层表单查询逻辑可能先初始化默认“在线询盘”表单和字段，因此首次查询可能产生配置写入；需要严格只读时，应先用 `get_enquiry_form_id` 确认表单状态并取得用户同意。

## `list_sqlite_tables`

用途：列出指定 SQLite 数据库中的用户数据表。

参数：

```json
{
  "dbName": "string，必填，.db 或 .sqlite 数据库文件名"
}
```

限制和返回：

- `dbName` 必须符合 `^[A-Za-z0-9_]+\\.(db|sqlite)$`。
- `dbName` 必须是当前站点 sqlite 目录中的合法文件。
- 内部 `sqlite_*` 系统表会被排除。
- 只读返回表名数组，不返回表数据。

## `get_sqlite_table_info`

用途：获取指定 SQLite 数据库中指定表的定义信息。

参数：

```json
{
  "dbName": "string，必填，.db 或 .sqlite 数据库文件名",
  "tableName": "string，必填，SQLite 表名"
}
```

限制和返回：

- `dbName` 必须符合 `^[A-Za-z0-9_]+\\.(db|sqlite)$`。
- `tableName` 只能是 SQLite 标识符，格式为 `^[A-Za-z_][A-Za-z0-9_]*$`。
- `tableName` 必须真实存在于指定数据库中。
- 返回建表 SQL、字段信息、索引及索引字段、触发器名称和 SQL。
- 不返回表数据。

## `query_sqlite`

用途：执行 SQLite 查询 SQL 并返回查询结果数组。

参数：

```json
{
  "dbName": "string，必填，.db 或 .sqlite 数据库文件名",
  "sql": "string，必填，查询 SQL",
  "nameParams": "object，可选，命名参数对象，默认 {}"
}
```

限制和返回：

- 只允许以 `SELECT`、`WITH`、`PRAGMA` 或 `EXPLAIN` 开头的查询语句。
- 数据值必须通过 `nameParams` 命名参数传递，禁止把用户输入直接拼接进 SQL。
- `nameParams` 必须是对象，可使用 `id` 或 `:id` 作为键。
- 单次最多返回 1000 行，超过上限时返回工具错误。

## `create_sqlite_db`

用途：为当前站点新建一个 SQLite 数据库。

参数：

```json
{
  "dbName": "string，必填，.db 或 .sqlite 数据库文件名",
  "desc": "string，可选，数据库说明，默认空字符串"
}
```

限制和返回：

- `dbName` 只允许英文、数字和下划线，且必须以 `.db` 或 `.sqlite` 结尾。
- 不允许路径、中文、空格、连字符或其他扩展名。
- 数据库已存在时拒绝覆盖。
- 创建成功后本次服务实例会切换到新数据库，但后续无状态请求仍需显式传入 `dbName`。

调用前确认数据库名和说明；若不确定是否已存在，先用 `list_sqlite_db` 检查。

## `upload_sqlite_db`

用途：将 SQLite 数据库字节上传到当前站点。

参数：

```json
{
  "dbName": "string，必填，.db 或 .sqlite 数据库文件名",
  "fileBase64": "string，必填，SQLite 文件内容",
  "desc": "string，可选，数据库说明，默认空字符串"
}
```

限制和返回：

- 只接受 `fileBase64`，不接受服务器本地路径。
- `fileBase64` 支持纯 Base64、Base64URL 和 `data:*;base64,...` Data URI。
- `dbName` 只允许英文、数字和下划线，并以 `.db` 或 `.sqlite` 结尾。
- 上传内容会先执行 SQLite 完整性检查。
- 校验失败或同名数据库已存在时拒绝保存。
- 上传成功后本次服务实例会切换到新数据库，但后续无状态请求仍需显式传入 `dbName`。

## `execute_sqlite`

用途：执行 SQLite 非查询 SQL。

参数：

```json
{
  "dbName": "string，必填，.db 或 .sqlite 数据库文件名",
  "sql": "string，必填，非查询 SQL 或无参数 SQL 脚本",
  "nameParams": "object，可选，命名参数对象，默认 {}"
}
```

限制和返回：

- 禁止执行 `SELECT`、`WITH`、`PRAGMA` 和 `EXPLAIN` 查询。
- 可用于增删改数据、创建或删除数据表、修改表结构、创建或删除索引和触发器。
- 数据值应使用 `nameParams` 命名参数传递。
- `nameParams` 为空对象时允许执行 SQLite 多语句脚本。
- 提供命名参数时按单条预处理语句执行。
- 返回 SQLite 受影响的行数。

调用前必须确认：

- 目标 `dbName` 正确。
- SQL 的作用范围，包括目标表、字段和数据行。
- 删除数据、删除表或修改结构前，先查询现有结构和数据并取得明确确认。
- 不将用户输入直接拼接进 SQL，优先使用 `nameParams`。

## `upload_file`

用途：向当前站点资源库上传一个文件。

参数：

```json
{
  "fileName": "string，必填，包含扩展名的文件名，不能包含目录路径",
  "fileBase64": "string，可选，纯 Base64 或 Data URI",
  "sourceUrl": "string，可选，HTTP/HTTPS 远程文件地址",
  "type": "string，可选，auto、image 或 file，默认 auto",
  "folderId": "integer 或正数字符串，可选，当前站点资源文件夹 ID",
  "watermark": "boolean，可选，仅 image 类型生效，默认 false"
}
```

限制和返回：

- `fileBase64` 与 `sourceUrl` 必须且只能提供一个。
- `sourceUrl` 必须以 `http://` 或 `https://` 开头。
- `type=auto` 时按扩展名自动识别图片或普通文件。
- 未提供 `folderId` 时，系统自动使用或创建默认文件夹。
- `watermark` 仅对 `image` 类型生效。
- 成功返回资源 ID、名称、绝对 URL、相对 URL、文件类型、扩展名、大小和文件夹 ID。

调用前确认文件名、唯一来源、类型、目标文件夹和是否加水印。需要作为文章缩略图时，使用返回的绝对 URL。

## `save_ai_page`

用途：保存当前站点的一张自定义 HTML 页面。

参数：

```json
{
  "pageId": "integer 或数字字符串，可选，默认 0",
  "html": "string，必填，需要保存的完整 HTML 源码",
  "name": "string，可选，新建或更新页面名称，默认空字符串",
  "urlPath": "string，可选，友好 URL 路径，默认空字符串",
  "autoSetIndex": "boolean，可选，默认 false"
}
```

参数规则：

- `pageId=0`：新建页面。
- `pageId` 为正数：更新已有AI自由页。
- `pageId` 可传整数或只包含数字的字符串。
- `html` 必须是完整 HTML 源码。
- 远程图片 URL 和支持的内联 Base64 资源会按站点后台编辑器规则处理。
- `urlPath` 为普通AI自由页的可选友好 URL，例如 `about.html` 或 `products/list.html`；开头斜杠会被规范化，不安全路径会被拒绝。
- `autoSetIndex=true` 仅在 `pageId=0`、`urlPath=index.html` 且当前站点存在可替换首页时生效，默认值为 `false`。

返回和失败行为：

- 成功返回 JSON 文本，包含 `success`、`mode=html`、`isHome`、`pageId` 和 `url`。
- 参数校验或保存失败时返回带 JSON 错误信息的 MCP 工具错误。
- 本工具不导入 ZIP；批量导入使用 `save_ai_page_batch`。

调用前确认：

- 新建还是更新。
- 更新时的页面 ID。
- 页面名称和友好 URL。
- 是否可能替换首页。

## `save_ai_page_batch`

用途：从 Base64 ZIP 压缩包向当前站点批量导入自定义 HTML 页面和支持的静态资源。

参数：

```json
{
  "zipBase64": "string，必填，完整 ZIP 的 Base64 或支持的 ZIP Data URI",
  "overWrite": "boolean，可选，默认 true",
  "autoSetIndex": "boolean，可选，默认 false"
}
```

限制：

- `zipBase64` 接受完整 ZIP 的 Base64 编码。
- 也接受 MIME 类型为 `application/zip`、`application/x-zip-compressed` 或 `application/octet-stream` 的 Data URI。
- Base64 中的空白字符会被忽略。
- 每个 HTML 文件以压缩包内的相对路径作为友好 URL，例如 `about/index.html`。
- `overWrite=true` 时，相同 URL 的已有AI自由页会使用原页面 ID 覆盖更新。
- `overWrite=false` 时，只要 URL 已存在就导入失败。
- 已有系统页、产品页、文章页或无效页面目标不会被覆盖。
- `autoSetIndex=true` 时，压缩包根目录的 `index.html` 在全部页面处理完成后设为首页。
- 嵌套路径如 `about/index.html` 不触发自动设置首页。
- 支持 HTML、JavaScript、CSS、常见网页图片、SVG、WOFF 和 WOFF2。
- 不安全路径和不支持的文件类型会被拒绝。

返回和失败行为：

- 成功返回 JSON 文本，包含 `success`、`mode=zip`、`isHome` 和 `pages`。
- `pages` 每项包含 `name`、`pageId` 和 `url`。
- 导入失败时返回带 JSON 错误信息的 MCP 工具错误。
- 后续失败前已经写入的文件或页面不会回滚。

调用前必须明确确认：

- ZIP 中将导入哪些页面和资源。
- `overWrite` 是否覆盖相同 URL 的AI自由页。
- 是否将根目录 `index.html` 设为首页。
- 用户已知中途失败不会自动回滚。

## `del_page`

用途：物理删除当前站点的一张 AI 页面。删除后不可恢复。

参数：

```json
{
  "pageId": "integer 或正数字符串，必填"
}
```

参数和页面限制：

- `pageId` 必须是当前站点页面 ID，最小值为 1。
- `pageId` 可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- 仅支持 `EnableCustomTpl=1` 且 `PageType=99` 的AI自由页。
- 其他页面会返回“此页面不是AI页面，不支持删除”。
- 输入对象不接受额外属性。

删除范围：

- 页面记录。
- 页面专用模块。
- 页面样式。
- 区域配置。
- 友好 URL。
- 页面权限。
- 自定义 HTML 文件。
- 相关缓存。

调用前必须执行：

1. 使用 `list_page` 确认页面属于当前站点并核对页面 ID。
2. 使用 `get_page_info` 获取 `ID`、`PageName`、`Url`、`SourceCode` 和 `codePath`，确认目标是受支持的 AI 页面。
3. 向用户展示目标站点、页面 ID、页面名称和 URL，并说明上述内容将被物理删除且不可恢复。
4. 等待用户针对该具体页面明确确认永久删除。
5. 只有确认后才调用 `del_page`。不得复用之前对保存、覆盖或其他操作的确认。

如果 `get_page_info` 提示目标不是 AI 页面，不得调用 `del_page`。

## `clear_site_cache`

用途：清理当前 MCP 端点对应站点的站点缓存。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：缓存清理完成后返回当前站点 ID。

调用前必须说明该操作会清理当前站点缓存并获得用户确认。

## `set_home_page`

用途：将当前站点的一张AI自由页设为首页。

参数：

```json
{
  "pageId": "integer 或正数字符串，必填"
}
```

限制：

- `pageId` 必须是当前站点中已存在的AI自由页。
- `pageId` 最小值为 1。
- 系统页面和当前首页不能设置。
- 操作会调整页面类型、更新页面模块路由并清理相关缓存。

返回：返回最终首页 URL。

调用前必须明确确认页面 ID 和将首页切换到该页面的影响。

## `set_page_friendlyurl`

用途：为当前站点的一张AI自由页新增、修改或删除友好 URL。

参数：

```json
{
  "pageId": "integer 或正数字符串，必填",
  "urlPath": "string，必填"
}
```

限制：

- `pageId` 必须对应当前站点AI自由页，最小值为 1。
- `urlPath` 仅允许字母、数字、斜杠、连字符、下划线和可选的 `.html` 后缀。
- 开头的斜杠会被移除。
- 传入空字符串会删除当前页面的友好 URL，并恢复默认重写 URL。
- 指定路径不得与已有友好 URL 或重写规则冲突。

调用前必须明确确认：

- 目标页面 ID。
- 新 URL，或确认要删除现有 URL。
- 对现有链接和搜索引擎访问的影响。

## 推荐调用顺序

1. 准备当前站点 MCP 地址和 Bearer Token。
2. 使用 `test` 验证认证和连通性。
3. 使用 `list_page`、`list_news_class`、`list_product_class` 或 `list_gallery` 查询实际 ID；如果页面需要表单，优先使用 `list_custom_form` 列出已有表单并让用户选择。
4. 查询 FAQ 时，使用 `list_faq_class`、`list_faq` 或 `get_faq_info`；编辑 FAQ 前先读取详情，新增或修改分类前先查询分类。
5. 查询文章或产品时，使用 `get_news_list` 或 `get_product_list`；编辑具体内容前，使用 `get_news_info` 或 `get_product_info` 读取详情。需要查看在线询盘提交记录时，使用 `list_enquiry_records`。
6. 查询相册图片时，先使用 `list_gallery` 确认相册，再使用 `list_gallery_item` 查询图片项；编辑、排序或删除前必须读取并核对目标。
7. 新增或修改文章分类时，先使用 `list_news_class`；新增或修改产品分类时，先使用 `list_product_class`。
8. 新增文章、产品或相册图片前，确认分类或相册；需要素材时先调用 `upload_file`、`upload_product_image` 或使用相册工具支持的图片来源。
9. 处理 SEO 时，先用 `get_site_seo` 或 `get_seo_list` 读取当前值并核对对象 ID；整站修改使用 `edit_site_seo`，产品、文章、分类或页面修改使用 `edit_seo`，批量产品/文章规则使用 `edit_seo_batch`。分类使用 `ClassID`，页面和自定义 HTML 的 title/meta 可能被同步修改，调用前必须确认。
10. 管理 301 跳转时，先使用 `list_seo_redirect` 核对当前规则和 ID；新增使用 `add_seo_redirect`，修改使用 `edit_seo_redirect`，删除前额外确认来源地址、目标地址和旧链接影响，再使用 `del_seo_redirect`。
11. 修改已有 AI 页面时，使用 `get_page_info` 获取页面信息和 `SourceCode`。
12. 需要新建或修改普通自定义表单时，先确认表单名称、字段、通知/支付配置和删除影响；确认后调用 `add_custom_form` 或 `edit_custom_form`。
13. 修改网站名称或公司联系信息时，先展示 `edit_company_info` 的字段原值与新值并取得确认。
14. 生成或检查页面 HTML、文章、产品、相册、SEO、跳转规则或 FAQ 内容。
15. 对写操作展示变更摘要并取得确认；文章、产品和 FAQ 需要单独确认发布状态。
16. 删除页面、FAQ、FAQ 分类、相册、相册图片或 301 跳转规则时，额外核对目标及文件、Banner、跳转或关联数据影响，并取得针对永久删除的明确确认。
17. 调用对应写入、删除或维护工具；表单写入失败后重新查询确认是否产生部分写入，相册批量图片或文件操作失败后也要核对实际状态。
18. 根据工具返回的成功信息或错误信息报告结果。
