---
name: chaoxing-mcp-oauth
slug: chaoxing-mcp-oauth
title: 超星智雅 MCP 一键接入
displayName: 超星智雅 MCP 一键接入
summary: 三步接入超星智雅（StudyAI）MCP：本机回调授权换 JWT、自动写入 mcp.json、refresh_token 常驻保活，附 7 类故障速查表。
description: 指导用户将超星智雅/StudyAI MCP 服务接入 WorkBuddy 的完整流程：引导用户提供 OAuth2 凭据、本机起回调服务完成授权码换 JWT、写入 mcp.json、配置 refresh_token 常驻保活，并处理 grant_version_stale / scope_denied / invalid_scope 等故障。适用于用户要求连接超星智雅 MCP、令牌过期修复、或重新授权的场景。
version: 1.3.0
tags: ["chaoxing", "mcp", "oauth", "studyai", "education"]
license: MIT
metadata: {"clawdbot":{"emoji":"🎓","os":["linux","darwin","win32"]}}
agent_created: true
---

# 超星智雅 / StudyAI MCP 接入

帮助用户把超星智雅（StudyAI）的 MCP 服务接入 WorkBuddy。平台不提供 OAuth 发现文档，WorkBuddy 内置 OAuth 流程不可用，因此必须**本机起回调服务、人工授权换 JWT、以静态 Bearer 头写入 mcp.json、再用 refresh_token 常驻保活**。本技能自带三个脚本（`scripts/` 目录），**日常使用只需一键命令**。

## ⚡ 一键式自动接入（v1.1，推荐日常使用）

核心脚本：`scripts/chaoxing-mcp-auto.mjs`。一条命令自动完成：检查令牌 → 未过期直接验证 → 过期自动刷新 → 刷新失败自动弹授权页 → 写 mcp.json → 验证 → 自动关闭授权服务。

```bash
# 【仅首次·推荐】打开设置工作台（浏览器自动弹出，逐项填凭据 → 自动校验 → 自动授权 → 自动验证，全程不进对话、密钥不落对话）
node <技能目录>/scripts/chaoxing-mcp-auto.mjs --setup

# 【命令行党替代】直接保存凭据（之后永远不用再输）
node <技能目录>/scripts/chaoxing-mcp-auto.mjs --save <client_id> <client_secret> [scope]

# 【日常】一键确保连接（判断状态自动走刷新或授权，无需人工干预）
node <技能目录>/scripts/chaoxing-mcp-auto.mjs

# 其他
node <技能目录>/scripts/chaoxing-mcp-auto.mjs --status        # 只看状态不改任何东西
node <技能目录>/scripts/chaoxing-mcp-auto.mjs --reauth        # 强制重新授权
node <技能目录>/scripts/chaoxing-mcp-auto.mjs --daemon        # 常驻保活（剩10分钟内自动刷新，setInterval 无 unref，进程不会退）
node <技能目录>/scripts/chaoxing-mcp-auto.mjs --daemon-once   # 无人值守单次保活（计划任务用：只刷新不弹授权页，静默退出）
```

### 设置工作台（--setup）功能说明
- 本地起 `http://localhost:8765/setup` 页面并自动打开浏览器（15 分钟超时自动关闭）
- 页面内置**完整操作流程引导**：① 一键复制回调地址 + 先登记回调再授权的警告 → ② 三项凭据的抄写说明（Secret 仅显示一次/Scope 空格分隔）→ ③ 表单填写 → ④ 跳转学习通授权 → ⑤ 自动收尾
- 表单提交时**先用假 code 探测校验密钥有效性**（invalid_client=抄错了立即提示重抄，invalid_grant=密钥对），杜绝带错密钥进授权流程白跑一趟
- 校验通过 → 凭据保存到本地文件 → 页面自动跳转学习通授权页 → 用户点一次「确认授权」→ 回调自动换令牌、写 mcp.json、在线验证，**最终结果表格直接显示在页面里**（凭据✅/授权✅/验证✅/scope/令牌到期时间）
- Agent 使用守则：新装/重新配置时直接跑 `--setup` 并告诉用户"浏览器已弹出设置页，按页面引导操作即可"，**凭据全程不进对话**

**系统级保活（已配置，2026-09-23）**：Windows 计划任务 `ChaoxingMCP-KeepAlive` 每 15 分钟跑一次 `--daemon-once`（留余量充足，脚本内部"剩余>15分钟则跳过"），与 WorkBuddy 会话完全解耦——只要电脑开着，令牌永远自动续期，任何会话里的 MCP 调用都不会再遇到 401。管理命令：`Get-ScheduledTask -TaskName ChaoxingMCP-KeepAlive` / `Start-ScheduledTask ChaoxingMCP-KeepAlive` / `Unregister-ScheduledTask -TaskName ChaoxingMCP-KeepAlive -Confirm:$false`。注册要点：Action 用托管 node 绝对路径 + 脚本绝对路径，Trigger 用 `-Once -RepetitionInterval 15min -RepetitionDuration 3650d`，Settings 加 `-StartWhenAvailable -AllowStartIfOnBatteries -ExecutionTimeLimit 5min`。

**官方文档确认的边界**（https://sharewh2.xuexi365.com/share/1ee530c1-4542-444e-8ef8-5f56247a26fa）：授权必须用户人工点一次「确认授权」（无 client_credentials/免确认模式），这是平台安全红线——一键自动化的极限即 v1.1 现状：授权环节仅保留一次人工点击，其余全自动。另注意：智雅平台「重置密钥/停止授权」会立即冻结数据通道（表现为令牌未过期却 403），遇到时让用户去智雅「第三方授权管理」检查授权状态是否「启用中」。

凭据优先级：环境变量 `CX_CLIENT_ID`/`CX_CLIENT_SECRET` > `~/.workbuddy/chaoxing-credentials.json`（`--save` 写入）。
授权成功后脚本会记住成功的 scope 写回凭据文件，下次授权免输入。
Agent 使用守则：**会话里遇到 MCP 401/403，或用户要求连接超星 MCP 时，直接跑一键命令**（Windows 下 node 用 WorkBuddy 托管路径 `~/.workbuddy/binaries/node/versions/<ver>/node.exe`，凭据文件已存在则无需问用户）。只有一键命令走到「自动授权」分支时才需要用户在浏览器点一次「确认授权」。

**安全红线（必须遵守）**：
- 绝不把用户的 client_id / client_secret / 令牌 / 账号信息写入本技能任何文件、对话输出或日志
- 凭据通过**环境变量**或 `--save` 存入 `~/.workbuddy/chaoxing-credentials.json`（本机专用），泄露时在智雅「密钥管理 → 重置密钥」作废重来

## 平台关键事实（实测结论，勿重复探测）

- MCP 端点：`https://api.chaoxing.com/openai/studyai/data`，仅 POST，JSON-RPC 2.0
- 授权端点：`https://api.chaoxing.com/auth/oauth2/authorize`（302 → passport2.chaoxing.com，用户需登录学习通）
- 令牌端点：`https://api.chaoxing.com/auth/oauth2/token`
- 仅支持 **authorization_code** 授权码模式（client_credentials → `unauthorized_client`，password → `unsupported_grant_type`）
- 无 `.well-known` 发现文档 → WorkBuddy 内置 OAuth 不可用；WorkBuddy 的 mcp.json 也不支持 OAuth 端点字段，但 **headers 里已有 Authorization 时客户端会跳过内置 OAuth**
- access_token 是 JWT，寿命 1 小时；refresh_token 长期有效，刷新不递增授权版本

## 实测踩坑记录（2026-09-22 接入实录）

1. **授权页 Whitelabel 400** = 回调地址未在智雅登记。先在授权记录「继续配置」里填 `http://localhost:8765/callback` 保存，再点授权
2. **401 `invalid_client`** = client_secret 错（client_id 对错与 secret 无关：code 能拿到说明 client_id 对）。截图抄密钥极易抄错相似字符（l/1/I、0/O/D、rn/m、cK/ck）。**假 code 诊断法**：用假 code 调令牌端点，返回 `invalid_client`=密钥错、`invalid_grant`=密钥对——最快定位手段。**重要经验（2026-09-23 实战）**：凭据文件已存在时用户又手动粘贴密钥，大概率粘的是重置前的旧密钥——此时直接引导用户走 `--setup` 工作台（表单留空 secret 可沿用已存值），不要在实验台反复试粘贴密钥
3. **scope 多值用空格分隔**，逗号直接 `invalid_scope`。本项目实际生效 scope：`statistic:studyai:read`
4. **重复点授权会作废令牌**（grant_ver+1，403 `grant_version_stale`）。拿到 tools/list 200 后立即停授权服务；踩掉后跑 refresh 即可恢复，无需重新授权
5. **refresh 脚本内置 setInterval 用了 `.unref()`，Node 进程会自动退出**——常驻保活要么用 auto.mjs 的 `--daemon`（无 unref），要么用外层循环包 `--once`
6. **PowerShell 的 Invoke-WebRequest / HttpWebRequest / curl 调 MCP 端点会莫名 400/401/NullRef**（编码/头处理问题），Node fetch 一切正常——验证 MCP 一律写临时 .mjs 用 node 跑
7. mcp.json 是合并写入：保留其他条目，只更新 `chaoxing-studyai`，损坏时自动备份 .bak

## mcp.json 条目格式

```json
{
  "mcpServers": {
    "chaoxing-studyai": {
      "type": "http",
      "url": "https://api.chaoxing.com/openai/studyai/data",
      "headers": { "Authorization": "Bearer <JWT>" },
      "description": "超星智雅 StudyAI（OAuth2 授权码 + 静态 Bearer）"
    }
  }
}
```

## 手动分步流程（需要精细控制时才用）

### 第 0 步：收集凭据（问用户要三样）
1. client_id 与 client_secret（智雅 → 个人工作台 → 权限管理 → 第三方授权管理 → 密钥管理）
2. 凭证页「数据范围（Scope）」一栏的原文
3. 确认回调地址已登记：在授权记录「继续配置」里填 `http://localhost:8765/callback` 并保存（**先填回调、再点授权**，顺序反了会 400）

### 第 1 步：启动授权实验台（scope 探测，仅 scope 未知时用）
```bash
CX_CLIENT_ID=<id> CX_CLIENT_SECRET=<secret> node <技能目录>/scripts/chaoxing-mcp-lab.mjs
```
- 本机起 `http://localhost:8765/lab` 页面（后台运行），把页面链接给用户
- 用户点对应 scope 的按钮 → 登录学习通 → 点「确认授权」→ 跳回本机回调
- 脚本自动：换 JWT → 导出令牌对到 `~/.workbuddy/chaoxing-studyai-token.json` → 写 `~/.workbuddy/mcp.json`（`chaoxing-studyai` 条目）→ 跑 `tools/list` 验证
- **成功拿到 tools/list 200 后，立即停掉实验台进程**，防止用户再点导致 grant_ver 变化

### 第 2 步：启动保活守护
```bash
node <技能目录>/scripts/chaoxing-mcp-refresh.mjs --once   # 单次刷新
node <技能目录>/scripts/chaoxing-mcp-refresh.mjs          # 常驻（注意 .unref() 坑，见上）
```

### 第 3 步：让用户激活
WorkBuddy「连接器管理 → 右上角自定义连接器」对 `chaoxing-studyai` 点「信任」（MCP 配置不会自动生效）。

## 故障速查

| 报错 | 原因 | 处置 |
|---|---|---|
| `access_denied / client_id` | 授权请求没带 scope | 一键命令或实验台带 scope 重试 |
| `invalid_scope` | scope 值不对 | 从智雅凭证页抄「数据范围」原文 |
| 401 `invalid_client`（换令牌时） | client_secret 错 | 假 code 诊断确认后，重置密钥 + `--save` 新密钥 |
| 403 `scope_denied` | 令牌 scope 不含所需范围（如只授了 openid） | 用正确 scope 重新授权一次 |
| 403 `grant_version_stale` | 之后又走过一次完整授权 | 跑一键命令（自动 refresh）即可恢复 |
| 换令牌失败 `invalid_grant` | code 过期/已用，或回调与登记不一致 | 重新授权；核对回调地址 = `http://localhost:8765/callback` |
| 授权页 400（Whitelabel Error Page） | 回调地址未在智雅登记 | 先在智雅「继续配置」里填回调地址再授权 |
| 多 scope 写法 | 平台只认**空格**分隔，逗号会 `invalid_scope` | 合并值用空格 |

## 可用工具（授权 StudyAI 数据范围后）

- `get_course_clazz_list(courseId)` — 课程下的班级列表
- `get_my_teach_course_list()` — 我教的课程列表
- `studyAi_agent_talk(courseid, clazzids, content)` — 与课程智能体流式对话

## 会话恢复注意

保活守护随会话结束而停止。若新会话中 MCP 调用报 401/403，**跑一键命令 `node <技能目录>/scripts/chaoxing-mcp-auto.mjs`**（凭据已在本地文件中），自动刷新或引导重新授权，通常 10 秒内恢复。
