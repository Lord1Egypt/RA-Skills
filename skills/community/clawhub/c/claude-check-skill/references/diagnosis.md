# 报错与证据

核对日期：2026-10-30。产品机制变化时重新查看对应官方页面，不把本文件当作永久规则。

## 先看错误发生在哪

网页、Claude Code、桌面应用可能使用不同账号或认证来源。保留原始错误的含义，核对发生位置、时间、当前登录方式和组织。不要把中文转述“封号”当作最终诊断。

- `This organization has been disabled` / `Your organization has been disabled`：组织停用方向，核对组织并联系官方支持或申诉。不能据此证明电脑留下了旧账号标记。
- `Your access to Claude is on hold` / `Your account is on hold`：访问暂停或审核方向，在 claude.ai 核对审核入口以及个人/组织范围。
- `Your organization has disabled Claude subscription access`：组织限制订阅认证。联系管理员确认允许的方式，不能删掉后半句并判成组织封禁。
- `Your organization has disabled API key authentication`：组织认证策略限制，核对管理员要求。
- OAuth 过期、401、Invalid API key：先核对认证来源、当前账户和凭证有效性；401 本身不证明封号。
- 429、额度提示：用量或速率方向。证书、DNS、超时：连接方向，须结合具体上下文。

依据：[Claude Code 报错参考](https://code.claude.com/docs/en/errors)、[官方申诉说明](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals)。关键词分流不是服务端状态查询。

## 环境证据怎么用

用户配置、项目配置和项目本地配置可同时存在，受管设置还有额外约束。脚本记录字段来源与不同值，不推断完整优先级，不执行配置中的命令。按 [官方设置说明](https://code.claude.com/docs/en/settings) 和客户端 `/status` 核实生效设置。

时钟错误可能干扰依赖有效期的连接或认证；系统显示的本地时间只是读数。自动校时状态和 HTTPS Date 可以辅助核对，后者可能受缓存影响。时区、语言、代理与地区差异值得记录，但本项目没有证据把某一种组合换算成封号概率。

旧配置目录、登录文件、缓存存在，仅说明存在本地数据。旧账号身份要以实际登录界面和当前期望账号核对，不能靠文件名推断。

社区材料 [Claude 清除缓存](https://ucngkdwd50uz.feishu.cn/wiki/N2gPwq16Ji5zcMkaYARcdT4EnZe) 提到多个清理位置。它不是官方封禁机制证明；本项目未验证清理能降低封禁率，不采用整目录删除或“洗白”说法。目录里可能保存历史、设置及其他有用资源。
