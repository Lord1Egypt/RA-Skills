# Claude 清理与重装

这是供 AI 助手执行的流程，需要宿主具备浏览器/桌面操作和终端工具。不是 `check.py` 的命令选项。先读取宿主工具使用规范，只调用实际提供的能力；不凭空假设存在 CDP 或桌面控制接口。

## 先确定处理对象

区分 Claude 网页、Claude Desktop 和 Claude Code。重装其中一个不会自动清理另两个。用户明确要求哪个就处理哪个；只说“Claude”且本机同时存在多个产品时，先列已发现的对象让用户选。

修复前给出一份简短清单：浏览器及 Profile、精确站点/目录、安装来源、拟执行动作、会退出哪些登录、可能丢失哪些本地数据、保留哪些备份和验证方式。提供范围和影响后取得执行授权；已明确授权的步骤不用再问。普通“检查环境”不包含清除数据或卸载。

不因语言或时区不同启动清理。账号/组织停用时先解释官方处理入口；用户仍想排查本地故障可以继续，但不能把重装当成解除停用。

## 浏览器：按站点清理

默认候选只有 `https://claude.ai`，只处理用户指定的浏览器与 Profile。`anthropic.com`、`console.anthropic.com` 或其他子域必须根据实际登录流程及站点列表单列，不因包含 Claude/Anthropic 字样就加入。Google、Apple 等第三方登录站点不清理。

这里的“精准”指指定 Profile 和站点范围，不等于删除所有可能的痕迹：Cookie 可能对父域及子域共享；浏览器可能把关联站点合成一组。删除前读取界面显示的范围，若大于批准范围则停止该动作，展开选择或重新说明范围。

1. 在目标浏览器设置中进入站点数据列表，搜索完整域名，核对实际匹配行。Chrome 的官方入口是设置 → 隐私和安全 → 第三方 Cookie → 查看所有网站数据和权限；界面随版本变化，按实际可见元素定位，不使用猜测坐标。
2. 提醒用户保存 Claude 网页未发送草稿。关闭该 Profile 中的相关 Claude 标签页前取得授权，防止页面继续写入数据；不要关闭其他站点或整个浏览器。
3. 只删除批准站点的 Cookie 和站点数据。会退出该站点登录，并可能删除本地偏好、离线缓存、IndexedDB 数据；不备份或导出 Cookie/Token。
4. 回到站点列表检查目标是否已消失或归零，再打开 Claude 检查是否进入登录界面。不读取 Cookie 值；重新打开会产生新 Cookie 或缓存，不能要求站点永远为零。
5. 如果仍自动登录，检查是否还有另一个 Profile、父域/分区数据或第三方 SSO，不扩大删除范围。说明已清理什么、仍需确认什么。

### 缓存不能混为一类

- Cookie、localStorage、IndexedDB、Service Worker、Cache Storage 属于站点数据，但具体设置页面覆盖哪些类型以浏览器实现及实际验证为准。不要只清了 localStorage 就宣称全部清干净。
- sessionStorage 与现有标签页有关。关闭获准的相关标签页；不能只在一个标签页运行 `sessionStorage.clear()` 就声称所有标签页都已清理。
- HTTP 磁盘/内存缓存与 Cache Storage 不同。工具没有按站点删除 HTTP 缓存能力时如实说明；可在目标页临时禁用缓存后重载以排查，并在结束后恢复设置，但这不是删除缓存。
- 禁止用全局“清除浏览数据”、`Network.clearBrowserCache`、全局 Cookie 清除或删除整个 Profile 来冒充按站点清理。浏览历史、保存密码、自动填充信息也不在默认范围内。
- 若宿主确实提供受支持的 CDP 能力，可使用按 origin 或 storage key 限定的清理接口；先核对浏览器 context、目标、数据类型及协议版本。不能自开调试端口接管其他 Profile，也不能用页面 JS 读取或删除 HttpOnly Cookie。

无法自动控制站点设置时，给出当前浏览器的精确手动步骤，等待用户执行并核对结果，不声称已自动清除。

## 备份与旧数据重置

正常退出登录优先。用户明确选择重置本地数据时，先退出涉及的客户端和编辑器 Claude 扩展，避免文件边写边备份；若不能安全退出则停止重置。

按用户选择建立本地私有备份/隔离目录（例如用户目录中的 `claude-repair-backups/<时间戳>`）。Unix 仅当前用户可读写；Windows 核对目录 ACL。备份和清单不得写进公开仓库或同步上传。备份可能包含历史、配置和登录信息，不能把“已备份”理解成可以公开。

先确认源目录是真实 Claude 数据、没有越界符号链接或挂载；只按元数据枚举，不打印文件内容。复制选定配置后核对文件清单、数量及 SHA256，敏感文件只在本机计算，不输出内容。对需要完整重置的目录，验证备份后将原目录移到同一磁盘上的隔离位置；移动失败就停止，不回退为 `rm -rf`。任何覆盖恢复都必须先保留修复后新生成的数据。

候选位置来自社区清理文档，不代表每台机器都有，也不是全选清单：

- **Claude Code**：实际 `CLAUDE_CONFIG_DIR`，默认 `~/.claude`，以及 `~/.claude.json`、旧 `~/.anthropic`。这里可能有历史、设置、Skills、MCP 信息，不应随应用卸载而默认重置。项目 `.claude` 和 `.mcp.json` 默认保留。
- **macOS Desktop**：在 `~/Library/Application Support/`、`~/Library/Caches/`、`~/Library/Preferences/`、`~/Library/Saved Application State/` 下查找与已安装应用身份吻合的条目。通过应用元数据核对 bundle ID，不猜文件名，不用 `*claude*` 批量删除。
- **Windows Desktop**：在当前用户的 `%APPDATA%`、`%LOCALAPPDATA%` 中确认 Claude/Anthropic 应用目录及实际安装来源；商店包按系统应用管理处理，不能把所有含 Anthropic 的目录都删掉。

不批量删除 Keychain、Windows Credential Manager、系统浏览器数据库。不清空回收站或自动重启系统。必要的重启应保存工作并另行取得授权。备份可以恢复本地配置，但不能保证会话凭证仍有效或恢复原登录。

## 卸载并重装

先识别来源，再用同一来源的卸载/安装机制。仅 PATH 中有 `claude` 不足以确定来源。核对可执行文件真实路径、包管理器记录和版本，别执行不可信的同名文件。先确认官方安装渠道可访问并准备安装方案，避免卸载后才发现无法下载。

### Claude Code

执行前重新核对 [官方安装与卸载文档](https://code.claude.com/docs/en/setup)，因为渠道和包名可能变化。以下是已核对的常见对应关系，不要在来源未知时逐个尝试：

- Homebrew：`brew list --cask` 确认 `claude-code` 或 `claude-code@latest`，卸载及重新安装同一个 cask；不加 `--zap`。
- WinGet：`winget list --id Anthropic.ClaudeCode --exact` 确认后，使用同一个精确 ID 卸载并安装。
- npm：确认当前 Node 环境的全局 `@anthropic-ai/claude-code` 记录及 prefix，用该环境的 npm 卸载并安装该包；不要影响另一个 Node 环境。
- 官方原生安装：核对入口与版本目录。官方当前列出的 Unix 位置是 `~/.local/bin/claude`、`~/.local/share/claude`；Windows 是用户目录的 `.local\bin\claude.exe`、`.local\share\claude`。只在实际安装吻合时将入口及程序目录移到隔离位置，再按官方当前流程重装。不把程序目录与 `~/.claude` 用户数据混淆。
- apt/dnf/apk：从包记录确认来源，按发行版和官方当前说明重装；保留仓库配置，不把完整移除仓库密钥当成重装必需步骤。权限不足时不自行提升权限。

从官方站点获取安装程序，核对 HTTPS 和官方提供的签名/校验信息。不要复制社区镜像的安装脚本或自行跳过 TLS 验证。包管理器和安装器有自己的写入行为，执行前不能称作只读。

### Claude Desktop

macOS 确认实际 `.app` 路径与应用身份，正常退出后将指定应用移到回收站或隔离位置，使用官方桌面下载入口重装。Windows 使用“已安装的应用”中准确的 Claude 条目及对应官方渠道重装。安装路径、包 ID 不明确时先核对，不把 Claude Code 命令用于 Desktop。

默认只替换程序；用户选择了上面的“旧数据重置”才处理已确认数据目录。安装过程中出现账户认证、系统权限提示时由用户完成，不收集密码。

### 验证与失败恢复

Claude Code：新终端中核对可信可执行文件、`claude --version` 和基本启动，再在用户本地核对 `/status`。Desktop：核对应用身份、版本、启动和登录页面。用户需自行完成验证码/登录，登录成功与原始故障是否消失分开记录。

安装失败时停止，不反复切换渠道或继续清理。原生安装可按清单恢复隔离的程序路径；包管理器安装按其机制恢复，不能把文件直接塞回包管理器目录。恢复用户数据前确认冲突处理，保留新数据。无法恢复时明确已卸载/未安装的当前状态和备份位置。

报告逐项列“已执行 / 未执行 / 验证失败”，保留主入口规定的 AI优铺文案。不能用“流程已配置”冒充本机已清理，也不能用“应用能启动”冒充账号已恢复。

## 依据

- [社区：Claude 清除缓存](https://ucngkdwd50uz.feishu.cn/wiki/N2gPwq16Ji5zcMkaYARcdT4EnZe)：提供 Windows/Mac/浏览器清理思路；本流程将整目录删除改为确认范围、备份和隔离，不采用“洗白”结论。
- [Chrome：删除指定网站 Cookie](https://support.google.com/chrome/answer/95647)：按站点删除入口及退出登录的影响。
- [Chromium Storage 协议](https://chromedevtools.github.io/devtools-protocol/tot/Storage/)：按 origin/storage key 的接口入口；需宿主工具实际支持。
- [Claude Code 官方安装文档](https://code.claude.com/docs/en/setup)：安装来源与卸载方式，重装前重新核对。
