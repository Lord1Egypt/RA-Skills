# OUS 上传

## 概览

执行上传时，由 agent 自己读取文件内容、分析文件大小、计算 MD5、在必要时按 `blockSize` 拆分文件、依次调用 OUS V2 接口并轮询状态；只有在上传进入成功终态后，才返回最终的 `url` 和 `uploadKey`。

执行时优先兼容服务端真实返回，而不是死板依赖某一版示例字段名。只要响应语义一致，就应该继续完成上传。

## 收集输入

开始前先准备这些输入：

使用curl调用GET 接口 https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/upload/token
鉴权参数说明：
|参数   |是否必须   |参数类型   |参数说明   |例子|
| ------------ | :------------: | :------------: | ------------ | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌| xxxxxxx|

从返回的json里面提取

- `d.ousToken`
- `d.globalDomain`
- `d.blockSize`

## 识别文件来源

这个 skill 只接受本地文件路径作为输入。

1. 优先使用用户直接提供的本地文件路径
2. 支持绝对路径或仓库相对路径

如果用户没有提供本地文件路径，或者路径不存在、不可读，就直接停止并明确告诉用户：这个 skill 只支持本地文件上传。

## 分析文件

在发起上传前，agent 需要自行完成这些准备工作：

1. 确认文件存在且可读
2. 获取文件大小，单位为字节
3. 计算整个文件的 MD5 值
4. 记录原始文件名
5. 判断 `文件大小 <= blockSize` 还是 `文件大小 > blockSize`

如果 `文件大小 <= blockSize`，走单文件上传。

如果 `文件大小 > blockSize`，走分片上传，并按下面规则处理：

1. 计算 `blocks = ceil(fileSize / blockSize)`
2. 按 `blockSize` 将文件切成若干分片
3. 分片编号从 `1` 开始
4. 最后一个分片可以小于 `blockSize`
5. 分片实现要优先选择当前环境可用的方式，不要假设 GNU `split` 参数一定可用；如果系统自带 `split` 选项不兼容，可以改用 `dd`、脚本流式切片或其他本地可靠方案

## 单文件上传

当 `文件大小 <= blockSize` 时：

1. 调用 `POST /ous/api/v2/single/upload`
2. Header 带上 `ous-token-v2: <ousToken>`
3. 以 `multipart/form-data` 传这些字段：
- `file`
- `md5`
4. 只有在确实需要时才追加这些可选字段：
- `metadata`
- `customPrefix`
- `customFilename`
5. 从响应里读取任务标识；优先读取 `taskId`
6. 如果响应里没有 `taskId`，但存在 `obsTaskId` 或其他服务端返回的任务标识，也要记录下来用于排障
7. 只有在单文件上传接口成功返回并且任务已经建立后，才开始调用状态接口

## 分片上传

当 `文件大小 > blockSize` 时：

1. 先调用 `POST /ous/api/v2/block/upload/init`
2. Header 带上 `ous-token-v2: <ousToken>`
3. 传这些字段：
- `md5`
- `blocks`
- `size`
- `name`
4. 只有在确实需要时才追加这些可选字段：
- `metadata`
- `customPrefix`
- `customFilename`
5. 读取初始化响应中的：
- `taskId`
- `lackBlocks`
- `progress`
- `deduplicated`
- `obsTaskId`（如果服务端返回）

然后按下面规则继续：

- 如果 `deduplicated = true`，视为初始化后服务端已具备完成条件；此时可以直接进入状态轮询
- 如果 `lackBlocks` 为空或不存在，上传所有分片
- 如果 `lackBlocks` 非空，只上传缺失分片
- 如果初始化响应缺少 `taskId`，但接口返回成功且后续状态查询可通过 token 正常工作，不要因为缺少 `taskId` 就中断流程；记录已有任务标识并继续
- `lackBlocks` 可能是压缩区间格式，例如 `8-10`；agent 需要先展开成具体分片编号，再决定上传列表

上传每个分片时：

1. 调用 `POST /ous/api/v2/block/upload/part`
2. Header 带上 `ous-token-v2: <ousToken>`
3. 以 `multipart/form-data` 传这些字段：
- `file`
- `block`
4. `block` 为当前分片编号，分片序号从 `1` 开始

分片上传保持保守策略即可。优先串行上传，避免触发文档中的并发限制；如果必须并发，也不要超过文档建议上限。

只有在最后一个需要上传的分片成功提交之后，才开始调用状态接口；不要在中间分片上传完成后提前查询状态。

如果初始化已成功，但后续分片上传无法继续，可以按需调用：

- `POST /ous/api/v2/block/upload/abort`

## 轮询状态

状态接口的调用时机必须满足下面条件之一：

- 单文件上传接口已经成功返回
- 分片上传中最后一个需要上传的分片已经成功返回
- 分片初始化阶段返回 `deduplicated = true`

满足上述条件后，才开始轮询：

- `GET /ous/api/v2/upload/status`

Header 仍然带：

- `ous-token-v2: <ousToken>`

状态查询优先依赖 token 绑定关系，不要假设一定还要额外显式传 `taskId`。如果响应里返回的是 `obsTaskId` 而不是 `taskId`，把它当作排障信息即可。

轮询规则：

1. 轮询间隔不要低于 `200ms`
2. 总轮询时间不能超过 `2分钟`
3. 如果 `status = 5`，视为上传成功
4. 如果 `status = 6` 或 `status = 8`，视为终态失败
5. 其他状态继续轮询
6. 不要因为响应里提前出现 `uploadKey`、`obsTaskId`、`blockUpload.progressPercent` 等中间信息，就把任务误判为成功；是否成功只看终态 `status`

## 返回结果

只有在 `/ous/api/v2/upload/status` 返回 `status = 5` 时，才向用户返回：

- `url`
- `uploadKey`

如果有助于排查问题或串联后续流程，也可以一并返回：

- `taskId`
- `obsTaskId`
- `md5`

如果上传没有成功，或者任何一步执行失败，不要向用户返回 `url`、`uploadKey`，即使失败态响应里带了这些字段也不要透出。

## 处理失败

当上传失败时，清晰地向用户暴露真实失败原因。

按下面这些规则处理：

- 将 `status = 6` 和 `status = 8` 视为终态失败
- 将错误码 `12` 视为 token 异常，例如 token 已被复用或尚未绑定任务
- 如果用户没有提供本地文件路径，或本地文件不存在、不可读，就直接停止；不要伪造文件，不要继续上传，也不要把问题归因到 OUS 接口
- 如果超过 `2分钟` 仍未进入成功或失败终态，就按超时处理，并返回真实的超时信息
- 如果某个分片上传失败且任务已经初始化，可以根据情况中止上传任务
- 如果本地切片命令或参数不兼容当前系统，优先切换为当前环境可用的本地切片方案；只有在确认无法生成分片时，才按本地处理失败返回
- 失败时只返回失败原因、状态码、错误码、任务状态等排障信息，不返回 `url` 或 `uploadKey`

