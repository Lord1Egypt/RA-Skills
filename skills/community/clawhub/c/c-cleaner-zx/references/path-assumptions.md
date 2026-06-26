# 📁 路径假设说明

**本 Skill 涉及两种不同的路径系统，请仔细阅读理解**

---

## 🖥️ Windows 目标路径（远程主机）

这些路径在**远程 Windows 主机**上，通过 WinRM 访问：

| 路径 | 说明 | 操作权限 |
|------|------|----------|
| `C:\` | Windows 系统盘 | 只读扫描，删除需确认 |
| `C:\Windows\Temp` | 系统临时文件 | 可清理（需确认） |
| `C:\Users\*\AppData\Local\Temp` | 用户临时文件 | 可清理（需确认） |
| `C:\$Recycle.Bin` | 回收站 | 可清空（需确认） |
| `C:\Windows\SoftwareDistribution\Download` | Windows 更新缓存 | 可清理（需确认） |
| `C:\Program Files` | 程序安装目录 | ⚠️ **白名单保护** |
| `C:\Users\*\Documents` | 用户文档 | ⚠️ **白名单保护** |

**访问方式：** WinRM/PowerShell Remoting

---

## 🐧 迁移目标路径（代理服务器）

这些路径在**代理服务器**上（通常是 Linux）：

| 路径 | 说明 | 操作权限 |
|------|------|----------|
| `/path/to/migration-target/` | 迁移文件根目录 | 完全访问 |
| `/path/to/migration-target/VMware/` | VMware 相关文件 | 完全访问 |
| `/path/to/migration-target/PDF/` | PDF 文件 | 完全访问 |
| `/path/to/migration-target/Videos/` | 视频文件 | 完全访问 |
| `/path/to/migration-target/Archive/` | 压缩文件 | 完全访问 |
| `/path/to/migration-target/upload-log.jsonl` | 迁移日志 | 追加写入 |

**访问方式：** 本地文件系统（代理服务器可直接访问）

---

## 🔄 文件传输流程

```
┌─────────────────────────────────────────────────────────────┐
│  Windows 目标主机 (WINDOWS_HOST_IP)                              │
│                                                             │
│  C:\Users\USERNAME\Downloads\large-file.iso (4.5 GB)            │
│                          │                                  │
│                          │ WinRM/SCP/SMB                    │
│                          ▼                                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ 网络传输
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  代理服务器 (Linux)                                         │
│                                                             │
│  /path/to/migration-target/VMware/                   │
│    └── large-file.iso (4.5 GB)                             │
│                                                             │
│  /path/to/migration-target/upload-log.jsonl          │
│    └── 记录迁移日志                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ 重要说明

### 1. 路径不要混淆
- `C:\` 开头的路径 → Windows 远程主机
- `/home/` 开头的路径 → 代理服务器（Linux）

### 2. 文件迁移方向
```
Windows 主机 → 代理服务器
（C 盘文件迁移到 Linux 服务器存储）
```

### 3. 网络要求
- Windows 主机和代理服务器之间需要网络连通
- 推荐使用 WinRM over HTTPS (端口 5986)
- 或者使用 SCP/SFTP (端口 22)
- 或者使用 SMB (端口 445)

### 4. 凭证要求
- **WinRM 凭证**：访问 Windows 主机需要用户名和密码
- **迁移目标权限**：代理服务器上的迁移目录需要写入权限
- **凭证存储**：建议使用环境变量或密钥管理服务，不要明文存储

---

## 🔐 安全建议

1. **WinRM over HTTPS** - 不要使用 HTTP 或 AllowUnencrypted
2. **限制访问来源** - 配置防火墙只允许代理服务器 IP 访问
3. **使用专用账户** - 为 WinRM 创建专用账户，限制权限
4. **定期轮换凭证** - 定期更换 WinRM 密码
5. **审计日志** - 定期检查 upload-log.jsonl 日志

---

_理解路径假设对于正确使用本 Skill 至关重要！_

🐾 说明
