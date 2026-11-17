# 安全边界 / Security Policy · v0.1.2

ai-data-delivery在用户指定的本机项目中整理、编辑和验证语义。它有文件操作、网络验证与可选子进程能力；这些能力按下列范围实现，不能只凭安全声明判断可信。SKILL.md的capabilities是入口摘要，本页与实际代码共同供审查。

## 文件、数据与工作台

- CLI按输入/输出参数读写文件；这不是操作系统沙箱。不要把不可信文档中的路径或命令当成用户授权。
- 工作台仅绑定127.0.0.1，同源检查和临时会话令牌用于限制网页请求；不是多人身份认证服务，也不隔离同一系统账号下的恶意程序。
- 项目SQLite保存模型、历史和导入附件。私人备份含原始附件；交付ZIP不包含附件，但模型、问题与报告仍可能含业务敏感信息，分享前按接收者范围核对。
- 导入DDL只解析，模型用安全YAML解析。数据快照只读打开、query_only、关闭trusted_schema并限制查询时间。业务查询由有界编译器生成单表聚合及同范围明细；不提供任意SQL执行器、通用跨表SQL或生产写接口。
- 演示/测试在自身临时SQLite创建表和模拟记录；项目编辑写本机项目库。因此“业务快照只读”不等于整个工具从不写数据库。

## HTTP请求

网络请求只来自明确指定的endpoint/health-url。CLI可发送问题等验证请求、读取服务模型或结果；启用远端目标后会把请求内容发送给该目标，不能宣称绝不出网。

共享实现位于 `scripts/_network.py`：

- 仅HTTP(S)，不接受URL内用户名/密码、控制字符、片段或IPv6 scope。
- 默认允许精确localhost、回环及RFC1918/ULA私有IP。其他域名和公网IP需要显式 `--allow-remote`；不是一个“批准所有外部请求”的开关，仍须属于用户任务授权的目的地。
- 拒绝链路本地、未指定、多播、不可路由地址及已列出的云元数据IP/主机；即使allow-remote也不放行。
- DNS仅解析一次，检查全部答案，固定IP连接；HTTPS仍按原主机校验证书。不能通过第一次查安全IP、第二次换IP绕过。
- 不读取系统HTTP代理，不跟随重定向。重定向须由用户明确配置最终合法地址后重试。
- 响应最大4MB，请求受整体截止时间约束，包含慢速响应读取。HTTP失败、错误/拒绝/未知/等待状态不能凭相同数值被判为对账通过。

工作台已有消费者适配器的范围更窄：只允许本机IPv4回环，不使用上述远端开关。

## 子进程和环境

门禁、演示和mock只调用仓库内明确脚本，使用参数数组和最小环境。`scripts/rebuild.py`是可选的高级服务重建辅助工具，正常建模与首次体验不需要它。

- 默认环境由 `_contract.minimal_env`保留PATH、系统目录、临时目录、用户目录、语言等运行项，不整包继承CI/cloud/token变量。保留PATH/HOME仍不构成隔离沙箱。
- rebuild额外变量须逐一 `--pass-env NAME`，仅传指定名称，不打印值。用户指定程序仍可能读取自身配置或主动打印秘密，因此工具不会自动回显构建/服务日志；日志留在指定项目。
- 构建和启动使用argv、shell=False；直接shell解释器及.cmd/.bat入口被拒绝。建议JSON参数数组 `--build-argv` / `--start-argv` 避免路径解析歧义。显式指定的程序本身仍需可信，本工具不限制其全部行为。
- 先构建并核对产物，再替换旧实例；构建失败不停止旧实例。`--port`只检查占用，从不按端口杀进程。
- 仅停止本工具记录的进程：核对项目、可执行路径、创建时刻，用Windows原生handle或Linux pidfd操作同一实例。整数PID、过期或身份不符的记录拒绝处理。其他平台没有安全能力时拒绝，不降级为kill数字PID。
- 启动/就绪失败会清理本次创建的前台主进程；清理失败明确报错并保留身份记录供排查。启动命令必须持续前台运行，不可daemonize；不承诺通用进程树管理、生产部署或旧实例自动回滚。
- 就绪检查确认指定健康端点返回HTTP 2xx、被管理进程仍运行，不代表应用业务功能已验收。
- 默认记录为项目的 `.rebuild-process.json`；单独停止使用 `python scripts/rebuild.py --project-dir ./my-service --stop`。记录防误停与PID复用，不抵御同一系统账号恶意篡改记录。

## 对平台审计的处理

ClawHub公开报告针对平台0.1.1，展示的历史SKILL内部仍为0.0.7；不能直接当成本包扫描结论。历史动态模块加载和shell拼接已从相关路径移除。本版另修复遗漏的环境继承、端点判定/代理/重定向、健康检查及按端口停服务问题，并保留可复验测试。

中文内容本身不是恶意行为证据；网络和子进程也不能仅因用途正常就忽略实现风险。逐项以当前代码及负例判断，不把整个报告笼统称为误报。此版本尚未取得新的ClawHub审计结果。

## 审查与问题反馈

建议查看 `_network.py`、`_process.py`、`rebuild.py`，再看工作台service/serve与调用它们的入口；本次证据范围见[验证记录](references/v0.1.2-validation.md)。源码仓库的tests保留自动回归，纯净运行包不携带测试与本地记录。

安全问题可到[项目Issues](https://github.com/franklinxkk/ai-data-delivery/issues)反馈，请避免贴真实密钥、客户数据或未脱敏日志。

**English:** This is a local toolkit, not a sandbox. CLI HTTP targets are explicit; public IPs/other hostnames require opt-in, with DNS pinning, TLS verification, bounded responses/deadlines and no proxy or redirects. Child processes use argv and a minimal environment, with optional named passthrough. Rebuild manages only identity-checked foreground processes, never kills by port. Local tests do not constitute a new platform security audit or production certification.
