# 执行环境权限说明

## 🔒 当前执行环境限制

QClaw/OpenClaw 的执行环境有以下安全限制：

| 限制项 | 状态 | 说明 |
|--------|------|------|
| 文件写入 | ❌ 受限 | 无法写入用户目录（如 Desktop、Downloads） |
| 软件安装 | ❌ 受限 | 无法自动安装 Python、yt-dlp 等依赖 |
| 临时目录 | ⚠️ 受限 | 部分临时目录无法访问 |
| 网络下载 | ✅ 可用 | 可以下载网页内容 |
| 命令执行 | ✅ 可用 | 可以运行已安装的命令 |

## 🎯 影响的功能

以下 Skill 功能**需要用户手动执行**：

- ❌ 自动下载视频到本地
- ❌ 自动安装 Python/yt-dlp
- ❌ 写入文件到用户目录

以下功能**可以正常使用**：

- ✅ 搜索视频信息
- ✅ 获取视频详情（标题、播放量等）
- ✅ 列出可用清晰度
- ✅ 生成下载命令

## 🔧 解决方案（可选）

### 方案 A：增加写入权限（推荐高级用户）

如果你希望 AI 能直接帮你下载文件，可以：

#### Windows

1. **以管理员身份运行 QClaw**
   - 右键点击 QClaw 快捷方式
   - 选择"以管理员身份运行"

2. **修改执行策略**
   ```powershell
   # 以管理员身份运行 PowerShell，执行：
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **创建专用下载目录**
   ```powershell
   # 创建一个 AI 可写入的目录
   mkdir C:\AI-Downloads
   icacls C:\AI-Downloads /grant Everyone:F
   ```

#### macOS/Linux

1. **修改目录权限**
   ```bash
   # 创建专用目录并设置权限
   mkdir -p ~/AI-Downloads
   chmod 755 ~/AI-Downloads
   ```

2. **使用 sudo（不推荐）**
   ```bash
   # 临时提升权限（谨慎使用）
   sudo -S command
   ```

### 方案 B：手动执行（推荐普通用户）

保持当前安全设置，AI 只提供**下载命令**，你自己执行：

```powershell
# AI 生成这个命令，你复制粘贴运行
yt-dlp "https://www.bilibili.com/video/BV18NzvB5EZu" -o "$HOME\Downloads\%(title)s.%(ext)s"
```

**优点**：
- ✅ 更安全，AI 不会误删文件
- ✅ 你完全控制下载位置
- ✅ 符合最小权限原则

## 🛡️ 安全建议

| 场景 | 建议 |
|------|------|
| 日常使用 | **保持限制**，手动执行下载命令 |
| 批量下载 | 临时提升权限，完成后恢复 |
| 敏感环境 | **不要**提升权限，始终手动执行 |
| 服务器部署 | 使用专用低权限账户运行 |

## 📝 配置示例

### 创建 AI 专用工作目录

```powershell
# Windows
$aiWorkspace = "C:\AI-Workspace"
New-Item -ItemType Directory -Force -Path $aiWorkspace
icacls $aiWorkspace /grant "$env:USERNAME:(OI)(CI)F"

# 然后在 QClaw 配置中设置此目录为工作区
```

```bash
# macOS/Linux
export AI_WORKSPACE="$HOME/AI-Workspace"
mkdir -p $AI_WORKSPACE
chmod 755 $AI_WORKSPACE

# 然后在 QClaw 配置中设置此目录为工作区
```

## ⚠️ 风险提示

提升权限可能带来以下风险：

- 🔴 AI 可能意外覆盖重要文件
- 🔴 恶意 Skill 可能利用高权限执行危险操作
- 🔴 系统安全性降低

**建议**：仅在必要时临时提升权限，使用完成后立即恢复。

## 🔗 相关文档

- [OpenClaw 安全文档](https://docs.openclaw.ai/security)
- [PowerShell 执行策略](https://docs.microsoft.com/powershell/module/microsoft.powershell.security/set-executionpolicy)
- [yt-dlp 使用指南](https://github.com/yt-dlp/yt-dlp#usage)

---

**注意**：本 Skill 默认采用"方案 B"（手动执行），如需自动下载请按上述步骤配置权限。
