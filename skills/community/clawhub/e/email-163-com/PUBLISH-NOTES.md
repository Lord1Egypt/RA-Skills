# email-163-com v1.0.4 发布说明

**发布日期**: 2026-04-11  
**发布类型**: 安全修复版本  
**上一版本**: 1.0.0  

---

## 🔒 安全修复

本版本修复了 Security Scan 发现的所有问题：

### 高优先级问题
- ✅ 添加凭证声明到 package.json (`requiredCredentials`, `requiredEnvVars`)
- ✅ 创建 CLI wrapper 可执行脚本 (`email-163-com`)
- ✅ 创建安装脚本 (`INSTALL.sh`)

### 中优先级问题
- ✅ 更新 `_meta.json` 添加来源和安全信息
- ✅ 创建 `SECURITY.md` 详细安全说明

### 低优先级问题
- ✅ 统一文档中的路径引用（`email.py` → `main.py`）
- ✅ 更新 `TEST-REPORT.md` 添加详细测试结果

---

## 📦 新增文件

| 文件 | 用途 |
|------|------|
| `email-163-com` | CLI wrapper 可执行脚本 |
| `INSTALL.sh` | 自动化安装脚本 |
| `SECURITY.md` | 安全审计说明 |

---

## 📝 更新文件

| 文件 | 更新内容 |
|------|---------|
| `package.json` | 添加 `requiredCredentials`, `requiredEnvVars`, `security` 字段 |
| `_meta.json` | 添加 `source`, `security` 字段 |
| `TEST-REPORT.md` | 添加详细功能/安全/性能测试结果 |
| `SKILL.md` | 修复路径引用 |
| `README.md` | 修复路径引用 |

---

## ✅ 测试结果

### 功能测试
- ✅ 发送邮件（文本/HTML/附件）
- ✅ 接收邮件（IMAP ID 认证）
- ✅ 搜索邮件
- ✅ 文件夹管理
- ✅ 附件管理
- ✅ 批量操作（删除/移动）
- ✅ 邮件标记（已读/未读/星标）

### 安全测试
- ✅ 凭证文件权限 600
- ✅ TLS 加密连接
- ✅ 仅连接官方服务器
- ✅ 无日志记录凭证
- ✅ 无远程代码执行

### 安装测试
- ✅ 自动安装脚本
- ✅ CLI wrapper 正常工作
- ✅ 配置文件自动创建

---

## 🔧 技术规格

| 项目 | 值 |
|------|-----|
| **Python 版本** | 3.6+ |
| **Node.js 版本** | 14.0+ |
| **操作系统** | Linux, macOS, Windows |
| **架构** | x64, arm64 |
| **依赖** | 无（使用 Python 标准库） |

---

## 📋 安装说明

```bash
# 方法 1: 通过 ClawHub
clawhub install email-163-com

# 方法 2: 手动安装
unzip email-163-com-1.0.4.zip
cd email-163-com
bash INSTALL.sh
```

---

## 🎯 升级建议

**所有用户都应升级到 v1.0.4**，因为：
- 修复了 Security Scan 问题
- 提高了透明度和可信度
- 改进了安装体验
- 添加了完整的安全说明

---

## 📞 联系方式

- **GitHub**: https://github.com/openclaw/skills
- **ClawHub**: https://clawhub.com/skills/email-163-com
- **安全报告**: security@email-163-com.skill

---

**发布者**: OpenClaw Team  
**发布日期**: 2026-04-11  
**版本**: 1.0.4
