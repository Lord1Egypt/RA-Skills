# GWS 实践

用 GWS 验证命令、契约、请求和输出的对应关系。
保留目标提供方的命名、header、游标、认证和文件边界。

## 1. 读取契约

示例目标：查看近期修改且未删除的文件，并理解返回对象。

```sh
gws drive files list --help
gws schema drive.files.list
gws schema drive.FileList
gws schema drive.File
```

| 命令 | 检查什么 | 如何使用结果 |
| --- | --- | --- |
| `gws drive files list --help` | 实际支持的 `--params`、`--format` 和分页选项。 | 选择有效 CLI flags；JSON 查询参数不是独立 flags。 |
| `gws schema drive.files.list` | `pageSize`、`q`、`orderBy` 和响应类型。 | 构造列表请求；按响应引用继续查看 `FileList`。 |
| `gws schema drive.FileList` | `files`、`nextPageToken` 和 `incompleteSearch`。 | 区分资源数据与续读/完整性信息；沿 `files` 元素引用查看 `File`。 |
| `gws schema drive.File` | `id`、`name`、`mimeType` 和 `modifiedTime`。 | 选择任务需要的文件字段。类型 schema 描述对象，不会查询某个文件。 |

以当前 help/schema 为准，不假定输出始终不变。发现过程可能读取公开元数据；schema 查询不需要业务凭据。
以下命令采用固定版本约定，需要兼容的二进制；真正读取文件还需要已授权的 Drive 访问。

## 2. 实现契约

| 对象 | 实现与验证 |
| --- | --- |
| 命令树 | 从 Discovery 生成 `SERVICE RESOURCE [SUBRESOURCE] METHOD`。helper 使用 `+` 前缀。 |
| 输入 | URL/query 放入 `--params`。嵌套正文放入 `--json`。只显示适用 flags。 |
| 方法 schema | 返回 `httpMethod`、`path`、`description`、`parameters`、`scopes`。按方法返回 `parameterOrder`、`requestBody` 和 `response`。正文类型包含 `schemaRef` 和 `schema`。 |
| 类型引用 | 默认保留嵌套 `$ref`。`--resolve-refs` 请求展开。目标 CLI 限制循环、深度和体积。 |
| 描述 | 说明对象、前置、直接影响和完成边界。将约束放入类型契约。 |
| 输出 | 默认返回原生 API JSON。`--format json/table/yaml/csv` 控制展示。`--output PATH`/`-o` 指定二进制路径。 |
| 文件 | 仅在支持媒体上传的方法中提供 `--upload` 和 `--upload-content-type`。 |

Discovery 投影不等于完整 JSON Schema 校验。展示实际接受的全局参数，保留真实约束。
scopes 表示提供方声明。它不证明当前权限，也不表示所有 scope 都必需。
description 是说明，不是可执行策略或当前状态。它足以表达含义时，直接使用 description。

## 3. 验证有界读取

按修改时间倒序列出未删除文件：最多读取两页，每页请求最多五条。

```sh
gws drive files list \
  --params '{"q":"trashed = false","orderBy":"modifiedTime desc","pageSize":5,"fields":"files(id,name,mimeType,modifiedTime),nextPageToken,incompleteSearch"}' \
  --page-all --page-limit 2 --format json
```

预期 NDJSON 每行一页。`fields` 在服务端裁剪字段；本例最多请求十个文件，不代表完整清单。
仍有 `nextPageToken` 表示还有后续页。即使没有游标，`incompleteSearch: true` 仍表示搜索不完整，不能声称覆盖全部文件。

读取其中一个文件。运行前将 `FILE_ID_FROM_LIST` 替换为实际返回的 `files[].id`：

```sh
gws drive files get --help
gws schema drive.files.get
gws drive files get \
  --params '{"fileId":"FILE_ID_FROM_LIST","fields":"id,name,mimeType,modifiedTime"}' \
  --format json
```

核对返回 ID 与选定资源一致。ID 保持原值，字段选择放在 `fields`。
反例：在 `fileId` 中夹带 `?fields=name`，或用 `--output json` 选择格式；`--output` 指定的是二进制路径。
固定版本默认最多读取 10 页，页间延迟 100 毫秒。用 `--page-limit` 和 `--page-delay` 显式设置限制。

## 4. 验证预演

预演创建文件夹；查询参数和资源正文分别输入：

```sh
gws drive files create --help
gws schema drive.files.create
gws drive files create \
  --params '{"fields":"id,name,mimeType"}' \
  --json '{"name":"dx-preview","mimeType":"application/vnd.google-apps.folder"}' \
  --dry-run
```

核对 `dry_run` 为 true、`method` 为 POST、`url` 指向 Drive files、`query_params` 包含字段投影、`body` 包含文件夹名称与类型。
检查 `is_multipart_upload` 和秘密脱敏。预演返回的是请求计划，不是已创建的文件夹或成功回执。
反例：把 `name` 放入 `--params`、把字段投影放入 `--json`，或在未获创建授权时去掉 `--dry-run`。
参考 GWS 的预演可能初始化认证。
若目标 CLI 声明纯本地预演，按主技能证明业务 HTTP、凭据访问和恢复写入均为零。
单独声明元数据发现读取。

## 5. 验证适配

- 若支持 `@FILE` 或 `-`/stdin，声明为目标扩展。限制输入大小，严格解析 JSON。每次调用只允许一个 stdin 消费者。
- 通过私密文件、stdin 或凭据引用输入秘密。沿用目标提供方的认证与最小权限。
- 迁移 flag 时保留原有含义。对照 HTTP 请求与可观察行为验证差异。
- 验证结构化 JSON 写 stdout，诊断写 stderr。退出码：0 成功；1 API；2 认证；3 校验；4 发现；5 内部错误。
- 若任务要求 MCP，使用兼容的官方 SDK 和共用类型化执行器。直接调用执行器，并独立验证接口。固定参考源码没有 MCP 入口。
- 若使用外部响应清洗服务，先显式配置。保留正文和来源。清洗结果仍按数据处理。

参考版本：[GWS 0.22.5，commit a3768d0e82ad83cca2da97724e46bea4ff0e6dbd](https://github.com/googleworkspace/cli/tree/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/crates/google-workspace-cli/src)。更换版本后重新核对。
