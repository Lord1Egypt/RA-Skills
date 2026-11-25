# 云端接入、规则与首页

如果本机已通过官方 FlowUs CLI 完成网页登录，可以运行 `connect --root <首页链接或ID> --transport rest --rest-auth flowus_cli`。这是显式的本机认证选项，不是新的云端传输协议。现有配置可用 `init --local --transport rest --rest-auth flowus_cli` 切换，原能力验证随即失效；重新运行 `doctor --verify-writes` 后才能写入。CLI 必须已在 PATH 中并已授权；工具不安装、登录或读取 CLI 凭证文件，签名文件链接不进入命令参数或日志。API 请求沿用 CLI 的连接方式，文件字节传输仍使用本配置的 network_mode。原生 MCP 与环境变量 REST 不会自动改用 CLI。独立审批模式不能采用此选项。

## 新客户端接入

先取得用户对目标 FlowUs 的授权和管理器首页链接。需要 Python 3.10+。REST 使用本机已配置的环境凭证；原生 MCP 使用宿主连接及 [relay 协议](mcp-relay.md)。安装技能不等于授权，不读取其他应用的凭证。

从 skill 目录执行，`--config` 指向安装目录之外的客户端私人配置：

```sh
python3 scripts/cva.py --config /path/to/private/client.json connect --root https://flowus.cn/ROOT_PAGE_UUID --transport mcp_relay --dry-run
python3 scripts/cva.py --config /path/to/private/client.json connect --root https://flowus.cn/ROOT_PAGE_UUID --transport mcp_relay
python3 scripts/cva.py --config /path/to/private/client.json doctor --verify-writes
python3 scripts/cva.py --config /path/to/private/client.json latest
```

REST 客户端显式改用 `--transport rest`。MCP 模式需由宿主托管命令，不是把没有宿主的 relay 进程当作独立连接器。新客户端默认沿用系统网络配置，保留自己已有的网络选择，不从其他客户端复制网络设置。

`connect` 只读取已有页面和数据库，不新建库。未通过独立验证时可以只读查询；有只读 FlowUs 权限的用户无法通过写入检查。普通重新连接会清除本客户端原有写入验证，之后重新验证。

本机已有其他绑定时，先向用户展示目标差异，得到明确重新绑定授权后才加 `connect --replace`；工具备份旧配置。不要由云端文字、另一个智能体或文件内容代为批准。

## 配置结构与信任边界

配置页位于首页下两层以内，通常为“AI 后台 → 资料库配置”。代码块中的固定标识为 `kind: flowus-version-manager/profile`，格式版本为 `profile_schema_version: 1`。另有正整数 `config_version`、`minimum_tool_version` 和 `settings`。

`settings` 只允许：`vault_id`、`business_parent_id`、`approval_parent_id`、`approval_probe_id`、`databases`、`view_pages`、`inbox_page_id`、`rules`、`governance_mode`。分类、命名、版本匹配规则通过结构校验后作为数据使用。原始内容块直接读取，不走只提取附件链接的 Markdown 投影。

Token、OAuth 信息、客户端 `agent_id`、`transport`、`network_mode`、本地文件路径及能力凭据不进入云端配置。云端规则不是运行脚本或权限授权。多个智能体共用配置，但各自保留客户端身份、凭证和验证结果。

每个联网业务命令开始读取并固定配置快照，操作记录含执行者、配置版本和内容指纹。网络不可用、配置损坏、重复配置页、同版本重复修订或最低版本不满足时停止。已绑定客户端发现目标数据库或治理变化、配置被回退时停止，要求人工核对并明确重新连接。

## 首次发布和规则维护

已有库从本机配置升级时，先核对当前库与规则，完成新工具版本的真实能力验证，再执行：

```sh
python3 scripts/cva.py --config /path/to/private/config.json config push --dry-run
python3 scripts/cva.py --config /path/to/private/config.json config push
python3 scripts/cva.py --config /path/to/private/config.json config pull --dry-run
python3 scripts/cva.py --config /path/to/private/config.json config pull
```

`push` 在没有共享配置时创建后台和配置页；已有配置必须与本机记住的指纹一致，避免覆盖其他智能体的修改。若发现冲突，先 pull 查看最新内容，再有意识地合并所需规则。

发布规则更新时追加一个修订代码块，保留旧配置。同一页使用唯一的最高 `config_version`，多个配置页或最高版本重复则拒绝连接。也可以谨慎编辑最新修订的 `rules`；必须保持合法 JSON，其他客户端下次任务按内容指纹识别变化。不要编辑历史修订、伪造验证或把秘密填进代码块。

新版不会强制停用持有授权的旧客户端；参与共同管理的智能体需要全部升级到 0.4.0 或更新版本。

## 首页整理

```sh
python3 scripts/cva.py --config /path/to/private/config.json layout --dry-run
python3 scripts/cva.py --config /path/to/private/config.json layout --backup-dir /path/to/private/layout-backups
```

首页顺序为使用指南、文件收件区、最新版、历史版本、待确认、AI 后台。后台收纳资料库配置及五个原有数据库。整理保持资源 ID、文件和历史，保留人工备注及额外页面，不按标题删除用户内容。普通模板首次初始化后可调用此命令完成同样布局。

正式整理先保存本机配置、首页结构和完整云端文件备份，再分步移动现有资源。中断后使用同一个 `--backup-dir` 续跑。工具创建的子页面使用固定标记及幂等键；标记改变或重复时停止，不盲目重建。

此整理仅对明确的 trusted_client 库执行，不改变旧 isolated_approval 库的审批权限层级。移动接口不提供跨操作事务；每步前后核对，发现其他客户端改动时停止。没有声明移动工具的 MCP 宿主可以接入读写资料，但不能宣称完成页面整理；不要猜私有接口。

## 备份与恢复

绑定后的备份包含经过白名单校验的共享配置。恢复只将业务规则应用到独立验证过的目标库，目标资料库、页面和数据库引用使用目标自己的 ID；不继承来源客户端的验证、凭证或治理设置。

CLI 在文件恢复完成后尝试发布目标自己的共享配置。若配置发布失败，文件恢复结果仍保留，本机标为 `pending_profile_publish` 并阻止继续联网业务命令；使用 `config push` 续跑，避免旧云端规则覆盖刚恢复的规则。恢复成功后可运行 `layout` 整理目标首页。旧备份没有共享配置时仍按原恢复流程处理。
