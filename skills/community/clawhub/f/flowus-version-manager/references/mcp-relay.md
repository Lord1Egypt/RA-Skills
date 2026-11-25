# 原生 MCP 模式

客户端先完成 FlowUs 原生 OAuth，并确认 initialize 和 tools/list 成功。凭证由客户端保存和刷新；Python 不读取 OAuth 存储，不向客户端索取 Token。

显式选择模式，保留既有私人规则和数据库标识：

```sh
python3 scripts/cva.py --config /path/to/private/config.json init --local --transport mcp_relay --governance-mode trusted_client
```

旧配置默认仍为 REST。切换后旧能力凭据失效。MCP 模式目前支持可信客户端治理，不自动放宽旧的独立审批配置。

## 运行协议

由能调用原生 FlowUs MCP 工具的智能体托管命令。进程只在本次操作期间运行，无后台服务。可使用配套 assets/codex-mcp-driver.js 作为 Codex functions 主机驱动；其他客户端可实现相同 JSON 协议。

1. 使用 `--result-file /path/to/private/result.json` 启动正常的 doctor、init、ingest、migrate、backup 或 restore 命令。
2. Python 输出 `CVA_MCP_REQUEST` 加一行 JSON，含 id、tool、request_file 和 request_chars。请求参数位于临时文件，防止长文档被终端截断。
3. 主机读取请求，首次调用相应业务工具前执行 flowus_help(detail="input")；只调用声明的原生 MCP 工具，不转换为静态 Token 或私有接口。
4. 将真实工具结果写入标准输入：`{"id":1,"ok":true,"data":{...}}`。MCP 错误使用 `ok:false,error:{code,statusCode}`；不把失败包装成成功。
5. 上传事务和签名下载地址只经内存传递。使用管道或关闭回显的独立终端，不打印、缓存或写入这些敏感响应。普通长元数据可以使用同一受限临时目录下的 response.json，以短 response_file 回执交给 Python，读取后立即清除；目录只对当前用户开放。敏感事务使用可审查的明文 JSON，超过宿主传输上限时停止，不能编码隐藏或分段规避审查。普通正文中的非鉴权网址查询参数不等于签名凭据；存储地址查询、已知鉴权参数和上传事务始终走内存。Python 严格验证响应结构、路径和请求编号，拒绝编码帧、额外顶层字段及非 JSON 输入。
6. Python 校验顺序、执行规则和文件哈希，完成后输出结果文件回执并退出。中断时复用原命令和操作编号续跑。

主机不能擅自执行额外业务变更。人工批准仍来自当前聊天的真实用户，不能由 relay 生成。模式以可信客户端为前提，不防止有权限的主机伪造工具结果。

## 下载与并发

文件块可能只返回 oss_name。工具从其父页面的官方 Markdown 导出中取得实际签名链接，按完整存储路径匹配，不按文件显示名匹配或拼接 CDN 地址。嵌套内容块需追溯所属页面；匹配不唯一或内容哈希不符时停止。拒绝的链接只刷新一次，不重复上传。

主机驱动对此导出仅保留原文中实际出现的 HTTPS 链接候选，并明确标记为 official_export_link_candidates；不传输导出中重复的数据库属性前置文本。版本元数据仍由页面和数据库查询完整读取，原件仍逐文件下载校验。此投影不用于读取普通页面全文。

MCP 页面结果未附带 HTTP 响应头时，依据官方弱 ETag 约定使用 `W/"last_edited_time"`。每个客户端必须通过正常条件更新成功、旧条件更新被拒绝的真实验证，才能授权写入；不使用无条件更新。切换 OAuth 身份后需要重新验证。

doctor 的 `native_mcp_help` 合同投影只代表 MCP 实际声明的工具，不是完整 OpenAPI。只读附件检查不会签发允许迁移的能力凭据；仍须在隔离区域完成完整 doctor、规则演练和恢复验收。
