---
name: connector-oauth-fix
version: 1.0.0
description: 修复 WorkBuddy 连接器 OAuth 授权失败问题。当用户连接第三方连接器（QQ邮箱、网易邮箱、飞书等需要 OAuth 授权的服务）时出现 "0x800401F5"、"找不到应用程序"、"SSE error 405"、"授权超时"、"streamableHttp connect failed" 等错误时使用此技能。覆盖诊断、根因定位、注册表修复和验证的完整流程。
author: 刘文琦开发
agent_created: true
---

# 连接器修复

修复 WorkBuddy 连接器 OAuth 授权失败，恢复连接器正常连接。

## 适用场景

触发条件：用户在 WorkBuddy 中连接第三方连接器时出现以下任一错误：

- `streamableHttp connect failed: Failed to open: 找不到应用程序 (0x800401F5)`
- `sse connect failed: SSE error: Non-200 status code (405)`
- 连接器"授权超时"
- 错误码 `0x800401F5`
- "找不到应用程序"

## 诊断流程

按以下四步执行，每一步都可能终结排查（找到根因即可跳到修复）。

### 步骤 1：日志定位

从 WorkBuddy 日志中确认错误来源和连接器名称。

```bash
grep -i "streamableHttp\|0x800401F5\|sse connect\|405\|授权超时" ~/.workbuddy/logs/$(date +%Y-%m-%d)/*.log | tail -30
```

关注关键信息：
- 哪个连接器失败？（如 `connector:qq-mail`）
- 连接的目标 URL 是什么？（如 `https://api.mail.qq.com/mcp`）
- 是否有 `captureResourceMetadataUrl` 日志？（表示 OAuth 发现阶段成功）

### 步骤 2：网络排除

验证目标 MCP 服务端是否可达，排除网络问题。

```bash
# 测试 MCP 端点（返回 405 或 401 通常说明服务端可达）
curl -s -o /dev/null -w "%{http_code}" "https://<目标域名>/mcp"

# 测试 OAuth 发现端点（应返回 JSON）
curl -s "https://<目标域名>/.well-known/oauth-protected-resource" | head -20
```

如果两个请求都正常返回 → **问题不在网络，在本地**。跳到步骤 3。

如果网络不通 → 检查代理设置：
```bash
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable
```

### 步骤 3：默认浏览器诊断（核心）

**这是最常见的根因**：Windows 默认浏览器 ProgId 指向已卸载的浏览器，OAuth 流程调用 ShellExecute 打开授权页面时失败。

```bash
# 从日志中提取默认浏览器 ProgId，或直接查询常见问题 ProgId
reg query "HKEY_CLASSES_ROOT\ChromeCoreHTM\shell\open\command" 2>/dev/null
reg query "HKEY_CLASSES_ROOT\SogouExplorerHTML\shell\open\command" 2>/dev/null
```

验证浏览器程序是否存在：
```bash
# 从注册表值中提取路径，确认文件存在
# 例：注册表指向 "C:\Program Files (x86)\ChromeCore\ChromeCore.exe"
ls "/c/Program Files (x86)/ChromeCore/ChromeCore.exe" 2>/dev/null
```

**如果文件不存在 → 这就是根因。跳到修复方案。**

### 步骤 4：确认可用浏览器

找出系统中实际安装的浏览器：

```bash
ls "/c/Program Files/Google/Chrome/Application/chrome.exe" 2>/dev/null      # Chrome 64位
ls "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" 2>/dev/null # Chrome 32位
ls "/c/Program Files/Microsoft/Edge/Application/msedge.exe" 2>/dev/null      # Edge 64位
ls "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" 2>/dev/null # Edge 32位
```

## 修复方案

### 方案 A：HKCU 覆写 ProgId（推荐，无需管理员权限）

在 `HKCU` 层覆写浏览器命令，优先级高于 `HKCR`，不破坏原始注册表，仅当前用户生效：

```powershell
New-Item -Path "HKCU:\Software\Classes\<ProgId>\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Classes\<ProgId>\shell\open\command" -Name "(Default)" -Value '"<可用浏览器路径>" --single-argument %1'
```

常见示例：

| 失效 ProgId | 覆写目标 |
|---|---|
| `ChromeCoreHTM` → Edge x86 | `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --single-argument %1` |
| `ChromeCoreHTM` → Edge 64位 | `"C:\Program Files\Microsoft\Edge\Application\msedge.exe" --single-argument %1` |
| `ChromeCoreHTM` → Chrome | `"C:\Program Files\Google\Chrome\Application\chrome.exe" --single-argument %1` |
| `SogouExplorerHTML` → Edge | 同上，替换 ProgId |

### 方案 B：用户手动修改默认浏览器（治本）

引导用户：**Windows 设置 → 应用 → 默认应用 → Web 浏览器** → 选择 Edge 或 Chrome

此方案彻底清除残留，但需要用户手动操作，适合作为方案 A 之后的后续建议。

## 修复后验证

1. 确认注册表修改生效：
```bash
reg query "HKEY_CURRENT_USER\Software\Classes\<ProgId>\shell\open\command"
```

2. 让用户在 WorkBuddy 中重新连接该连接器

3. 确认连接状态变为 `connected`

## 根因链路

```
已卸载浏览器 → 注册表残留 ProgId 仍为默认浏览器
→ WorkBuddy OAuth 流程调用 ShellExecute 打开授权页面
→ Windows 按注册表查找浏览器程序 → 文件不存在
→ COM 错误 0x800401F5 "找不到应用程序"
→ streamableHttp 连接中断
→ SSE 降级也不被服务端支持 (405)
→ 最终显示"授权超时"
```

## 注意事项

- 方案 A 只在当前用户生效，不影响其他用户
- 修改 `HKCU` 不需要管理员权限
- 建议修复后提示用户到系统设置中正式更改默认浏览器，彻底解决
- 如果浏览器程序存在但仍报错，可能是代理或防火墙问题
- 如果网络不通且非代理问题，检查 DNS 或防火墙规则