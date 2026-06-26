# C 盘清理助手 (C-Cleaner) 🧹

Windows C 盘清理 Skill - 安全扫描、汇报、清理、迁移

---

## 🔐 安全原则（核心！）

**本 Skill 采用混合模式，严格遵守以下安全原则：**

| 操作类型 | 处理方式 |
|----------|----------|
| **扫描/分析/汇报** | ✅ 可以主动执行 |
| **删除文件** | ❌ **必须先问用户！** |
| **清理操作** | ❌ **必须先问用户！** |
| **移动文件** | ❌ **必须先问用户！** |
| **迁移文件** | ❌ **必须先问用户！** |

**任何删除/迁移操作前，Roxy 必须得到用户明确确认才能执行！**

---

## 📋 功能特性

### 阶段 1：扫描分析
- ✅ 磁盘空间分析（总容量、已用、可用）
- ✅ 目录大小扫描（Windows、Users、Program Files 等）
- ✅ 临时文件检测（Windows Temp、用户 Temp、回收站）
- ✅ 大文件扫描（可配置阈值）
- ✅ 重复文件扫描（基于文件名/哈希值）

### 阶段 2：删除和去重
- ⚠️ 临时文件清理（需确认）
- ⚠️ 回收站清空（需确认）
- ⚠️ Windows 更新缓存清理（需确认）
- ⚠️ 重复文件处理（需确认）

### 阶段 3：迁移大文件
- ⚠️ 大文件识别（需确认）
- ⚠️ 迁移到服务器（需确认）
- ⚠️ 原文件删除（需确认）
- ✅ 迁移日志记录

### 阶段 4：本地迁移目录管理
- ✅ 目录结构整理
- ✅ 索引生成
- ✅ 空间统计

---

## 🚀 使用方法

### 触发词
```
- 清理 C 盘
- 扫描 C 盘
- C 盘分析
- 查找大文件
- 查找重复文件
- 迁移大文件
- C 盘清理助手
```

### 命令模式
```bash
# 只扫描不删除（安全模式）
/c-cleaner scan --safe

# 扫描并汇报可清理项
/c-cleaner report

# 清理指定项目（需要确认）
/c-cleaner cleanup --target temp

# 迁移大文件
/c-cleaner migrate --size 100MB --target /migration/path
```

---

## 📁 配置说明

### 白名单目录（受保护，不能删除）
```json
{
  "protectedPaths": [
    "C:\\Windows\\System32",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users\\*\\Documents",
    "C:\\Users\\*\\Desktop",
    "C:\\Users\\*\\Pictures",
    "C:\\Users\\*\\Videos"
  ]
}
```

### 迁移配置
```json
{
  "migrationTarget": "/path/to/migration-target/",
  "categories": {
    "VMware": ["*.iso", "*.zip"],
    "PDF": ["*.pdf"],
    "Videos": ["*.mp4", "*.avi", "*.mkv"],
    "Archive": ["*.zip", "*.rar", "*.7z"]
  }
}
```

### 扫描阈值
```json
{
  "largeFileSizeMB": 100,
  "duplicateMinSizeMB": 1,
  "tempFileMaxAgeDays": 30
}
```

---

## 📝 输出示例

### 扫描报告
```markdown
## 📊 C 盘扫描报告

### 磁盘总览
| 项目 | 大小 |
|------|------|
| 总容量 | 247.7 GB |
| 已使用 | 206.8 GB |
| 可用空间 | 40.9 GB (16.5%) |

### 可清理项目
| 项目 | 大小 | 建议 |
|------|------|------|
| Windows Temp | 6.5 MB | ✅ 可清理 |
| 用户 Temp | 472.4 MB | ✅ 可清理 |
| 回收站 | 0 GB | 已空 |
| Windows 更新缓存 | 164.9 MB | ✅ 可清理 |

### 大文件 TOP 5
| 文件 | 大小 | 位置 |
|------|------|------|
| xxx.iso | 4.5 GB | C:\Downloads\ |
| yyy.zip | 2.1 GB | C:\Users\USERNAME\Downloads\ |
```

### 删除确认提示
```
喵～Roxy 准备执行以下操作，请老师确认喵！🐾

【操作类型】删除临时文件
【影响范围】
  - C:\Windows\Temp\* (6.5 MB)
  - C:\Users\xxx\AppData\Local\Temp\* (472.4 MB)
【预计释放】约 479 MB
【风险提示】临时文件可安全删除，不影响系统运行

⚠️ 安全确认
根据安全原则，Roxy 必须得到老师明确确认才能执行删除操作！

请老师回复：
- "确认删除" → Roxy 开始删除
- "取消" → Roxy 跳过此操作
- "只删除 Temp" → Roxy 只删除指定项目
```

---

## ⚠️ 注意事项

### 安全原则
1. **任何删除操作必须先问用户！**
2. **白名单目录绝对不能动！**
3. **迁移前必须确认目标位置！**
4. **删除前必须备份或确认！**
5. **所有操作必须记录日志！**

### ⚠️ 数据迁移风险（重要！）

**本 Skill 的迁移功能会将文件从 Windows 主机传输到代理服务器：**

```
Windows 主机 (C:\) → 代理服务器 (/path/to/migration-target/)
```

**这意味着：**
- 📤 文件会离开原始 Windows 主机（数据导出）
- 🔐 代理服务器需要有足够的存储空间
- 🛡️ 确保你信任代理服务器和存储位置
- 🚫 如果不想让文件离开 Windows 主机，**不要使用迁移功能**

**安全使用建议：**
1. **只使用扫描模式** - `/c-cleaner scan --safe`
2. **不提供迁移凭证** - 不设置 `MIGRATION_TARGET` 环境变量
3. **审查日志** - 定期检查 `upload-log.jsonl` 了解文件传输情况
4. **限制权限** - 使用专用的 WinRM 账户，限制访问权限

---

## 📁 文件结构

```
c-cleaner/
├── SKILL.md              # 本文件
├── README.md             # 使用指南
├── _meta.json            # 元数据
├── .gitignore            # Git 忽略文件
├── scripts/
│   ├── scan.ps1          # 扫描脚本
│   ├── cleanup.ps1       # 清理脚本
│   ├── migrate.ps1       # 迁移脚本
│   └── dedup.ps1         # 去重脚本
├── config/
│   ├── whitelist.json    # 白名单配置
│   ├── migration.json    # 迁移配置
│   ├── thresholds.json   # 阈值配置
│   └── credentials.example.json  # 凭证配置示例
└── references/
    ├── safety-rules.md   # 安全规则
    └── path-assumptions.md  # 路径假设说明
```

---

## 🔧 技术依赖

- **WinRM/PowerShell Remoting** - Windows 远程执行（HTTPS 推荐）
- **Python 3.x** - 服务器端脚本
- **wget/curl** - 文件传输

## 🔐 凭证配置

### 环境变量（推荐）
```bash
# Windows WinRM 凭证
export WINRM_HOST="WINDOWS_HOST_IP"
export WINRM_USER="WINDOWS_USER"
export WINRM_PASS="secure_password"

# 迁移目标配置
export MIGRATION_TARGET="/path/to/migration-target/"
```

### 安全建议
1. **不要明文存储密码** - 使用环境变量或密钥管理服务
2. **WinRM over HTTPS** - 不要使用 `AllowUnencrypted` 或 `Basic` 认证
3. **限制访问来源** - 配置 WinRM 只允许特定 IP 访问
4. **定期轮换凭证** - 定期更换 WinRM 密码

## 📁 路径说明

### Windows 目标路径
- `C:\` - 远程 Windows 主机的 C 盘（通过 WinRM 访问）
- `C:\Windows\Temp` - Windows 临时文件目录
- `C:\Users\*\AppData\Local\Temp` - 用户临时文件目录

### 迁移目标路径
- `/path/to/migration-target/` - **代理服务器上的路径**（Linux）
- 文件从 Windows 主机传输到代理服务器存储
- 需要确保代理服务器可访问且有写入权限

### 传输方式
- **WinRM** - 通过 PowerShell 远程复制文件
- **SCP/SFTP** - 通过 SSH 传输（如果 Windows 开启 SSH）
- **SMB** - 通过 SMB 共享挂载

---

_本 Skill 严格遵守 C 盘数据安全原则，任何删除/迁移操作都需要用户明确确认。_

🐾 Roxy 制作
