# C-Cleaner 使用指南 🧹

Windows C 盘清理助手 - 快速开始

---

## 🚀 快速开始

### 1. 安装 Skill
```bash
# Skill 已复制到 workspace/skills/c-cleaner/
# 无需额外安装，OpenClaw 会自动发现
```

### 2. 配置凭证（必需）
```bash
# 设置环境变量（推荐）
export WINRM_HOST="WINDOWS_HOST_IP"
export WINRM_USER="user@domain.com"
export WINRM_PASS="YOUR_WINRM_PASSWORD"
export MIGRATION_TARGET="/path/to/migration-target/"

# 或者编辑 config/credentials.json（不要提交到版本控制！）
# cp config/credentials.example.json config/credentials.json
# 然后编辑 config/credentials.json 填入实际凭证
```

### 3. 配置 WinRM（首次使用）

**⚠️ 安全提醒：** 建议使用 WinRM over HTTPS，不要启用 AllowUnencrypted 或 Basic auth！

```powershell
# 在 Windows 上执行（管理员 PowerShell）
# 安全配置：WinRM over HTTPS
winrm quickconfig

# 创建自签名证书（用于 HTTPS）
$cert = New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My
$thumbprint = $cert.Thumbprint

# 配置 WinRM HTTPS 监听器
winrm create winrm/config/Listener?Address=*+Transport=HTTPS @{Hostname="$env:COMPUTERNAME"; CertificateThumbprint="$thumbprint"}

# 或者使用 HTTP（仅限内网测试环境）
# winrm create winrm/config/Listener?Address=*+Transport=HTTP
```

**更安全的替代方案：**
- 使用 SSH 远程执行 PowerShell
- 使用 Tailscale 组网后通过 loopback 访问
- 使用 SSH 隧道转发 WinRM 端口

### 3. 开始使用
```
直接对 Roxy 说：
- "扫描 C 盘"
- "清理 C 盘"
- "查找大文件"
- "C 盘分析"
```

---

## 📋 使用流程

### 标准流程
```
1. 用户触发 → "扫描 C 盘"
2. Roxy 扫描 → 分析 C 盘使用情况
3. Roxy 汇报 → 展示可清理项/大文件/重复文件
4. 用户确认 → 选择要清理/迁移的项目
5. Roxy 执行 → 执行删除/迁移操作
6. 记录日志 → 保存操作记录
```

### 安全确认流程
```
⚠️ 任何删除/迁移操作前：

Roxy: "喵～Roxy 准备执行以下操作，请老师确认喵！"
      [列出操作详情、影响范围、预计释放空间]
      "请老师回复：确认/取消/部分确认"

用户： "确认删除" 或 "只删除 Temp" 或 "取消"

Roxy: 根据用户回复执行或跳过
```

---

## 🔧 配置说明

### 修改白名单
编辑 `config/whitelist.json`，添加受保护的目录路径。

### 修改迁移目标
编辑 `config/migration.json`，设置迁移目标路径和文件分类规则。

### 修改扫描阈值
编辑 `config/thresholds.json`，设置大文件阈值、重复文件最小大小等。

---

## 📝 常见用法

### 只扫描不删除（安全）
```
"扫描 C 盘，只汇报不删除"
```

### 清理临时文件
```
"清理 C 盘临时文件"
→ Roxy 会列出可清理的临时文件
→ 用户确认后执行
```

### 查找大文件
```
"查找 C 盘大于 1GB 的文件"
→ Roxy 扫描并列出大文件
→ 用户决定是否迁移
```

### 迁移大文件
```
"把 C 盘大文件迁移到服务器"
→ Roxy 列出大文件
→ 用户确认后执行迁移
→ 迁移完成后询问是否删除原文件
```

---

## ⚠️ 安全提醒

### 核心安全原则
1. **任何删除操作都必须经过用户确认**
2. **白名单目录绝对不能删除**
3. **迁移前必须确认目标位置**
4. **所有操作都会记录日志**

### ⚠️ 数据迁移风险（重要！）

**迁移功能会将文件从 Windows 主机复制到代理服务器：**

```
C:\Users\xxx\Downloads\large-file.iso
       ↓ (网络传输)
/path/to/migration-target/VMware/large-file.iso
```

**如果你不想让文件离开 Windows 主机：**
- ❌ **不要设置** `MIGRATION_TARGET` 环境变量
- ❌ **不要使用** `migrate` 命令
- ✅ **只使用** `scan --safe` 或 `report` 命令

**凭证安全：**
- 使用环境变量存储凭证，不要明文写在配置文件中
- 使用专用的 WinRM 账户，限制权限
- 定期轮换密码
- 配置防火墙限制访问来源 IP

---

## 📁 日志位置

操作日志保存在：
```
/path/to/migration-target/upload-log.jsonl
```

---

## ❓ 常见问题

### Q: Roxy 会主动删除文件吗？
A: 不会！Roxy 必须先得到用户明确确认才能执行删除操作。

### Q: 如何查看已迁移的文件？
A: 查看 `/path/to/migration-target/` 目录和 `upload-log.jsonl` 日志。

### Q: 可以自定义白名单吗？
A: 可以！编辑 `config/whitelist.json` 添加或修改受保护的目录。

---

_更多详情请查看 SKILL.md_

🐾 —
