# 配置、连接与迁移

需要 Python 3.10+，无第三方运行依赖。安装包自包含；私人配置、原件、备份和凭证放在 skill 目录之外。升级只替换工具，保留私人配置。同一资料库的各设备共用 vault_id、数据库 ID 和业务规则，各自配置 agent_id。

已有管理器首页时，优先按 [云端接入](cloud-connect.md) 使用 connect，不要用下面的新建流程重复建库。原有本机配置仍可使用；完成新版本能力验证后，可通过 layout 或 config push 发布共享配置。

## 默认：可信客户端＋聊天确认

FlowUs 是存储，skill 和工具执行治理规则。新配置默认 `governance_mode: trusted_client`，只需要一个有业务读写权限的集成。已有原生 MCP OAuth 时，优先按 [mcp-relay.md](mcp-relay.md) 显式选择 `transport: mcp_relay`，由客户端保存和刷新凭证，Python 不读取凭证。下面的直接终端命令适用于 REST 模式；REST 使用 `FLOWUS_API_TOKEN` 或已经存在的 `FLOWUS_TOKEN`。不要读取其他应用的凭证，也不要要求用户在聊天中提供密钥。

从 skill 目录运行：

```sh
python3 scripts/cva.py --config /path/to/private/config.json init --local --business-parent BUSINESS_PAGE_ID
python3 scripts/cva.py --config /path/to/private/config.json doctor --offline
python3 scripts/cva.py --config /path/to/private/config.json --prompt-credentials init --provision
python3 scripts/cva.py --config /path/to/private/config.json --prompt-credentials doctor --verify-writes
```

`--prompt-credentials` 在终端隐藏输入，仅保留在当前进程内存，不保存。环境变量已配置时不会再次询问。

初始化在业务页面内创建文档目录、文件版本、操作记录、变更提案、审批记录，并创建文件收件区和最新版、历史版本、待确认三个目录页。聊天确认依据写入操作记录；审批记录库保留作旧流程兼容，不需要用户手动维护。

初始化逐步保存资源 ID。数据库创建发生不确定网络失败时，先核对 FlowUs 里是否已创建，再填写已有 ID 续跑，不能盲目重复创建。

### 旧配置的显式切换

缺少 governance_mode 的旧配置保留原来的 `isolated_approval`，不会默默放宽规则。用户明确选择新方式后运行：

```sh
python3 scripts/cva.py --config /path/to/private/config.json init --local --governance-mode trusted_client
```

切换会使旧能力检查结果失效，需要重新验证。既有数据库和私人规则保留；不自动移动或覆盖已有审批资料。

旧的 isolated_approval 模式仍要求业务写入、审批只读两个集成，以及初始化时的临时审批写入凭证；仍使用 `apply-approved`。除非用户选择旧模式，不要求这些额外凭证。

## 真实能力门槛

`doctor --verify-writes` 只使用标记为 probe 的虚构记录和附件：

- 相同创建请求和幂等键必须返回同一个页面。
- 上传后能重新下载，SHA-256 与本地一致。
- 读取 ETag 后，服务器必须拒绝使用过期 ETag 更新。
- 旧模式额外验证审批权限隔离；可信客户端模式不要求这项。

只有全部必需检查通过才启用写入和迁移。更换工具版本、凭证、数据库或治理模式后重新验证。失败结果保存在私人配置的 last_capability_report，不能拿模拟测试替代。

附件 API 可能只返回 oss_name 和 size。如果没有临时下载 URL，工具从所属页面的官方 Markdown 导出中取得实际链接，并核对完整存储路径。无法匹配时才核对当前公开 OpenAPI 中是否另有授权下载接口。不要把兼容 file_url 当作 external 文件块，也不要猜私有接口、拼接 CDN 链接或把集成 Token 发给对象存储。没有可靠下载途径时，保留诊断结果并停止正式迁移。

有效的 cdn2.flowus.cn 签名下载地址还需要 FlowUs 来源头；工具下载时自动添加 `Referer: https://flowus.cn/`，不向对象存储发送集成凭证。`/preview/块编号` 是预览网页，不是文件直链。手工复制的签名直链可用于单附件诊断，不代表工具已能自动取得或刷新全库附件地址；不将直链的 token 等查询参数写入配置、日志或公开包，也不据此跳过迁移门槛。

### 建库前的只读下载检查

如果已有虚构测试附件，可在业务数据库尚未初始化时运行：

```sh
python3 scripts/cva.py --config /path/to/private/config.json --prompt-credentials doctor --probe-block TEST_BLOCK_ID --expected-sha256 ORIGINAL_SHA256
```

该检查只发 GET 请求，检查 API 连接、公开接口、附件元数据、自动取链和下载哈希；不会创建数据库或生成允许迁移的能力凭据。输出不包含签名直链。失败返回非零退出码，未执行的幂等和并发检查明确标为 not_run。检查通过后仍须初始化并执行 `doctor --verify-writes`。

签名下载被拒绝时，工具最多重新读取一次原附件，从官方 API 获取刷新后的地址；附件存储标识发生变化则停止。刷新失败不重新上传文件，不切换最新版。

### 网络与 TLS

`network_mode` 默认为 `system`，沿用系统代理；已有配置保持原行为。只有确认需要直连时，显式选择：

```sh
python3 scripts/cva.py --config /path/to/private/config.json init --local --network-mode direct
```

此设置只作用于本工具，不修改系统代理，不自动切换线路；两种方式均验证证书和主机名。诊断区分 TLS 意外断开、证书验证、DNS 和超时，不输出底层异常中的链接、代理凭证或服务器正文。改变连接方式会使旧能力凭据失效，需要重新验证。遇到证书验证失败时不关闭验证。

在 MCP 模式中，这个设置只控制 Python 的附件字节传输。原生 MCP 连接由客户端独立管理；Python 直连成功不能证明 MCP 的网络路径可用。遇到 `mcp_transport` 诊断时先修复客户端连接，不重新索取 Token 或跳过验证。

官方依据：[概览](https://flowus.cn/developer-api/v2/zh/getting-started/overview)、[文件上传](https://flowus.cn/developer-api/v2/zh/advanced/file-upload)、[并发约定](https://flowus.cn/developer-api/v2/zh/reference/conventions)。

## 日常运行

```sh
python3 scripts/cva.py --config /path/to/private/config.json ingest /path/to/file --dry-run
python3 scripts/cva.py --config /path/to/private/config.json ingest /path/to/file
python3 scripts/cva.py --config /path/to/private/config.json ingest --cloud-inbox
python3 scripts/cva.py --config /path/to/private/config.json latest "项目"
python3 scripts/cva.py --config /path/to/private/config.json timeline "项目"
python3 scripts/cva.py --config /path/to/private/config.json ask "最近两版有哪些相关内容"
python3 scripts/cva.py --config /path/to/private/config.json refresh
```

直接上传到 FlowUs 收件区不会触发后台任务，下次调用时处理。原始收件块保留，通过操作记录跳过已完成项。批量本地入库返回新增、重复、待确认和失败统计；部分失败返回非零退出状态，已完成项目保留。提取内容不完整时说明限制，不自动调用其他模型服务。

目录页是自动生成的显示快照，操作记录数据库保留实际变更。可在生成段落之外追加备注；工具不会替换这些额外内容。生成标记被修改时停止刷新并保留页面。并发刷新发现源数据变化时返回 changed_during_refresh，重新运行 refresh；文件的权威最新版引用不受目录刷新影响。

## 首次迁移、备份和恢复

先用虚构数据演练普通版本、终稿保护、持续台账和待确认，再迁移真实文件。现有日期、命名、内容匹配和私人分类规则保留；规则通过 init --local --rules 导入，不进入公开包。

```sh
python3 scripts/cva.py --config /path/to/private/config.json migrate /path/to/local-vault --dry-run
python3 scripts/cva.py --config /path/to/private/config.json migrate /path/to/local-vault --backup /path/to/private/local-before-cloud.zip
python3 scripts/cva.py --config /path/to/private/config.json backup /path/to/private/cloud-backup.zip
```

迁移先验证备份，再逐版本上传，最后登记最新版。核对文件数、版本线、来源、备注、历史事件以及逐文件哈希；重复内容也保留原索引记录的来源和历史语义。源数据变化或目标存在其他批次数据时停止。原 Library、Index、Inbox 和 Qsync 不移动、不清空。

迁移后再次提交相同内容时，只在已识别的同一版本线内复用已验证的旧记录；保留迁移时的全部历史记录和既有最新版引用。不同版本线之间不按哈希自动归并。预览中的 duplicate 字段会明确标记重复文件。

恢复使用新的测试区域、新配置和数据库，先通过同样的能力验证：

```sh
python3 scripts/cva.py --config /path/to/private/restore-config.json restore /path/to/private/cloud-backup.zip --dry-run
python3 scripts/cva.py --config /path/to/private/restore-config.json restore /path/to/private/cloud-backup.zip
```

恢复不覆盖来源数据库，旧提案和审批只作为历史证据，不激活为新权限。正式迁移和恢复演练都通过后才切换主库；本地库保留为迁移备份，第一版不启用 Qsync 双向同步。无后台监控、自动更新或自动发布。
