---
name: aios-transfer-file
description: 通过兼容 AWS S3 的 SDK 为 OpenClaw 和 AIOS agent 处理文件传输。当 agent 收到 `file_input://...` URI、需要把输入文件下载到工作区，或需要把本地文件上传后以 `file_output://...` URI 返回给用户时，必须使用这个 skill。不要使用 `aws` CLI 或任何外部 S3 客户端程序完成这些传输。
---

# AIOS 文件传输

> 本技能只适用于受控 AIOS 部署。它可能访问真实业务系统，必须按最小权限配置。只读操作可以自动执行；任何会改变状态的操作，包括创建、更新、提交、审批、驳回、删除或触发，都必须先预览目标应用、命令和请求体，并获得明确人工确认。CLI 必须固定到经过评审的版本，Ontology 来源必须可信且可审计。

在 OpenClaw 中，所有文件和图片传输，包括接受用户发来的文件，和给用户发送文件，都必须使用兼容 AWS S3 的 SDK。这适用于附件、`file_input://` 消息，以及任何需要把文件返回给用户的场景。

## 不可违反的规则

- 始终使用 S3 SDK。不要调用 `aws`、`s3cmd`、`mc` 或任何其他外部客户端程序。
- 本项目统一使用 TypeScript 和 JavaScript。不要为这个 skill 添加 Python 脚本或基于 Python 的传输流程。
- 在处理任何 `file_input://...` URI 之前，或在发送任何本地文件给用户之前，先触发这个 skill。
- 传输操作优先使用内置脚本 `scripts/transfer_s3.mjs`，不要在对话中临时写新的传输脚本。
- 如果工作区中还没有 `file_input` 和 `file_output` 目录，使用前先创建。
- 下载和上传都必须限制在工作区内进行。
- 在 SDK 上传成功之前，不要声称文件已经发送完成。
- 当你需要返回一个可下载文件时，最终回复必须是单独一条 `file_output://...` 消息，不能附带其他文字。

## 运行时配置

使用 AIOS 环境变量构建 S3 客户端：

- `AIOS_S3_ENDPOINT`
- `AIOS_S3_REGION`
- `AIOS_S3_ACCESS_KEY_ID`
- `AIOS_S3_SECRET_ACCESS_KEY`
- `AIOS_S3_FORCE_PATH_STYLE`

使用以下 bucket 变量：

- 收件箱 bucket：`AIOS_S3_AGENT_INBOX_BUCKET`
- 发件箱 bucket：`AIOS_S3_AGENT_OUTBOX_BUCKET`

发件箱变量统一使用 `AIOS_S3_AGENT_OUTBOX_BUCKET`，不要引入其他别名。

构造 SDK 客户端时：

- 从 `AIOS_S3_ENDPOINT` 设置自定义 endpoint。
- 从 `AIOS_S3_REGION` 设置 region。
- 显式传入 `AIOS_S3_ACCESS_KEY_ID` 和 `AIOS_S3_SECRET_ACCESS_KEY` 作为访问凭证。
- 当 `AIOS_S3_FORCE_PATH_STYLE` 为真值时启用 path-style，例如 `1`、`true` 或 `TRUE`。

与 `aios-agent-management-console` 保持一致，使用 TypeScript 或 JavaScript，并采用 AWS SDK for JavaScript v3，具体为 `@aws-sdk/client-s3`。

## 内置脚本

优先使用内置 JavaScript 工具：

```bash
node scripts/transfer_s3.mjs download-uri --uri "file_input://bucket/path/to/file.bin" --workspace .
node scripts/transfer_s3.mjs upload-file --source "/abs/path/to/file.bin" --workspace .
```

内置脚本的行为：

- 使用 `@aws-sdk/client-s3` 和上面的 AIOS S3 环境变量。
- 与 `aios-agent-management-console` 保持同样风格：ESM、动态导入本地安装的包、显式构造 `S3Client`、显式传入凭证，并且 `AIOS_S3_FORCE_PATH_STYLE` 默认取 `true`。
- 自动创建 `file_input` 和 `file_output` 目录。
- 把 `file_input://...` URI 下载到 `file_input`。
- 把待发送文件复制到 `file_output`，重命名为要求的时间戳前缀格式，并上传到发件箱 bucket 根目录。
- 输出描述传输结果的 JSON。
- 支持 `--uri-only`，用于最终上传回复步骤。

依赖位置：

- 这个 skill 在 `package.json` 中声明了 `@aws-sdk/client-s3`。
- 在一个全新的工作区首次传输前，先检查这个 skill 的本地依赖是否已经安装。
- 必须在这个 skill 目录中完成依赖检查，例如确认 `node_modules/@aws-sdk/client-s3` 是否存在，或运行 `npm ls @aws-sdk/client-s3 --depth=0`。
- 如果依赖缺失，在运行内置脚本前，先在这个 skill 目录执行 `npm install` 本地安装依赖。
- 只允许从本地安装位置动态加载该包；不要依赖其他项目中的兜底导入，也不要依赖任意文件路径。
- 如果本地包缺失，要明确报告依赖错误。除非用户明确要求修改内置脚本，否则不要在对话里写一个替代传输脚本。

依赖处理流程：

1. 在检查依赖或执行安装命令前，先切换到这个 skill 目录。
2. 确认 `node` 和 `npm` 可用。
3. 检查 `@aws-sdk/client-s3` 是否已经本地安装。
4. 只有在本地依赖检查确认缺失时，才运行 `npm install`。
5. 安装完成后，仍然要从这个 skill 目录运行内置脚本，确保它能正确解析本地依赖。

## 接收文件

当消息以 `file_input://` 开头时：

1. 解析 URI，并忽略第一个空格之后的所有内容。
2. 从 URI 中提取 `bucket` 和完整的 `key`。
   示例：`file_input://bname/path/to/fname.bin extra text`
   - bucket: `bname`
   - key: `path/to/fname.bin`
3. 在下载目标元数据中保留完整 key。识别远端对象时，不要把它压缩成只有 basename。
4. 把对象下载到工作区的 `file_input` 目录。
5. 本地文件名使用原始 basename，但前面加上时间戳前缀，例如 `123456_fname.bin`。
6. 如果 basename 本身已经带有时间戳前缀，则替换原有前缀，不要再叠加一个。
7. 下载完成后，把本地绝对路径加入工作上下文，再继续处理用户请求。

实现要求：

- 下载请求必须以解析得到的 URI bucket 和 key 为准。
- 你可以把 URI bucket 与 `AIOS_S3_AGENT_INBOX_BUCKET` 做诊断比较，但下载时不要改写 URI bucket。
- 使用 SDK 流式下载对象，不要通过 shell 调用客户端可执行程序。
- 优先调用 `scripts/transfer_s3.mjs download-uri ...`，不要写一次性的 SDK 代码。

## 发送文件

当你需要把本地文件发回给用户时：

1. 先用普通 assistant 消息说明文件内容以及用户该如何使用。
2. 从 `AIOS_S3_AGENT_OUTBOX_BUCKET` 解析发件箱 bucket。
3. 把文件复制到工作区的 `file_output` 目录。
4. 将复制后的文件重命名为带时间戳前缀的格式，例如 `123456_fname.bin`。
5. 如果原始 basename 已经有时间戳前缀，则替换原前缀，不要叠加。
6. 将最终文件名中的所有空格替换为 `_`。
7. 远端目标必须使用发件箱 bucket 根目录，不要额外添加子目录。
8. 如果发件箱 bucket 不存在，通过 SDK 先创建，再上传。
9. 使用 SDK 上传复制后的文件。
10. 上传成功后，再发送第二条回复，内容只能是 `file_output://<bucket>/<new_name>`。

实现要求：

- 远端 key 必须始终精确等于 bucket 根目录下的时间戳文件名。
- 说明性消息和 `file_output://...` 回复不能合并在同一条 assistant 消息里。
- 在上传成功之前，不要输出 `file_output://...`。
- 优先调用 `scripts/transfer_s3.mjs upload-file ...`，不要写一次性的 SDK 代码。

## 文件名规则

下载和上传都使用以下规则：

- 时间戳前缀格式：`<timestamp>_filename.ext`
- 如果文件名已经以 `<digits>_` 开头，则把这个前导数字前缀替换成新的时间戳。
- 除了上传时必须把空格替换为 `_` 之外，文件名其余部分保持原样。

## SDK 行为

使用 SDK 的标准对象操作，不要拉起外部客户端：

- 下载：`GetObject` 或等价接口
- 上传：`PutObject` 或托管上传助手
- 检查 bucket 是否存在：`HeadBucket` 或等价接口
- bucket 缺失时创建：`CreateBucket` 或等价接口

对于大文件，优先使用流式 API；当 SDK 支持流式处理时，避免把整个文件一次性读入内存。

## 失败处理

- 如果缺少必需的 S3 配置，停止执行，并准确指出缺失的是哪个环境变量。
- 如果 URI 格式错误，无法同时提取 bucket 和 key，停止执行，并报告输入格式有问题。
- 如果下载或上传失败，报告真实失败原因，不要假装传输已经完成。
- 如果上传失败，不要发送 `file_output://...` URI。
