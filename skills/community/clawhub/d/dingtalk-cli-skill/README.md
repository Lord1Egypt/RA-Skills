# WorkBuddy 钉钉 dws Skill 安装包

一键将钉钉 CLI (dws) 集成到 WorkBuddy，作为 Agent Skill 使用。

支持全部钉钉产品：**AI 表格 / 日历 / 通讯录 / 群聊机器人 / 待办 / 审批 / 考勤 / 日报周报 / DING 消息 / 工作台**，共 12 个产品、86 条命令。

---

## 安装

### 方法一：下载后审查再运行（推荐）

> :warning: **安全建议**：永远不要直接运行 `irm <URL> | iex`，先下载到本地审查脚本内容，再决定是否执行。

```powershell
# Step 1: 下载安装脚本到本地
$scriptPath = "$env:TEMP\install_dws.ps1"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.ps1" -OutFile $scriptPath -UseBasicParsing

# Step 2: 打开查看（用 notepad 或 VS Code 审查脚本内容）
notepad $scriptPath

# Step 3: 确认脚本内容可信后，再执行
& $scriptPath
```

### 方法二：手动分步安装

**Step 1：下载 dws CLI（v1.0.8）**

访问 [GitHub Release 页面](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/latest)，下载 `dws-windows-amd64.zip`，解压得到 `dws.exe`，保存到 `~\.local\bin\dws.exe`。

> **SHA256 校验**（可选）：下载 `checksums.txt`，确认 `dws-windows-amd64.zip` 的哈希值为 `7dc4e568b1386423784e6baf17fe675c11eb6c075bd887dcb0ede53cdded85e8`。

**Step 2：下载 Skill 文件**

访问 [GitHub Skills 目录](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/tree/main/skills)，下载全部文件，保存到 `~\.workbuddy\skills\dws\`。

**Step 3：认证**

```powershell
& "$HOME\.local\bin\dws.exe" auth login
```

> 安装过程中会**打开浏览器**引导钉钉扫码登录（只需操作一次）。

---

## 安装内容

| 内容 | 说明 |
:|------|------|
| dws CLI | 钉钉官方跨平台命令行工具，安装到 `~\.local\bin\dws.exe` |
| WorkBuddy Skill | 全部产品参考文档 + 自动路由指南，写入 `~\.workbuddy\skills\dws\` |

---

## 安装前检查清单

- Windows 10/11 + PowerShell 5.1+
- 网络可访问 GitHub（下载 CLI + Skill 文件）
- 有钉钉账号（扫码登录用）

---

## 安装后使用

### 重启 WorkBuddy

安装完成后**重启 WorkBuddy**，Skill 自动生效。

### 常用命令示例

| 场景 | 指令 |
:|------|------|
| 查待办列表 | `dws todo task list` |
| 创建待办 | `dws todo task create --title "完成报告" --deadline 2026-04-15` |
| 查看日历 | `dws calendar event list` |
| 发群消息 | `dws chat bot send-by-group --group-id <群ID> --content "开会了"` |
| 查收日报 | `dws report inbox list` |
| 搜索同事 | `dws contact user search --keyword "张三"` |
| AI 表格列表 | `dws aitable base list` |
| 查看 AI 表格记录 | `dws aitable record query --base-id <表ID>` |

### 重新认证

Token 过期后，重新运行：

```powershell
& "$HOME\.local\bin\dws.exe" auth login
```

---

## 常见问题

**Q: dws 命令找不到？**
重启 PowerShell，或手动将 `~\.local\bin` 加入 PATH：
```powershell
$env:PATH = "$HOME\.local\bin;$env:PATH"
```

**Q: 认证失败？**
确认钉钉账号有对应应用权限，运行 `dws auth login` 重新授权。

**Q: Skill 不生效？**
WorkBuddy 重启后 Skill 自动加载；也可在 WorkBuddy 设置中手动刷新 Skill。

---

## 卸载

```powershell
Remove-Item -Recurse -Force "$HOME\.workbuddy\skills\dws"
# CLI 卸载需手动删除 dws.exe
```

---

## 技术说明

- **dws CLI**：[DingTalk-Real-AI/dingtalk-workspace-cli](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- **安装脚本**：从 GitHub 下载后本地执行，不会上传任何个人信息
- **认证**：OAuth 设备流，数据不上传第三方
- **CLI 校验和**：SHA256 = `7dc4e568b1386423784e6baf17fe675c11eb6c075bd887dcb0ede53cdded85e8`（来源：GitHub Release checksums.txt）
