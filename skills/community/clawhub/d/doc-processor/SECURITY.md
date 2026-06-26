# doc-processor 安全说明

> **v2.7.11 重要变更**: AI 功能已移除，专注文档处理

---

## 🔒 安全概览

| 项目 | 状态 | 说明 |
|------|------|------|
| **网络请求** | ❌ 无 | v2.7.11 起移除所有网络请求 |
| **环境变量** | ❌ 无 | v2.7.11 起移除环境变量使用 |
| **系统调用** | ✅ 有 | 仅调用 poppler-utils（开源 PDF 工具） |
| **安装脚本** | ✅ 有 | 标准 pip 安装 Python 依赖 |
| **数据外传** | ❌ 无 | 所有操作在本地完成 |

---

## 📦 安装脚本说明

**文件**: `setup.sh`

**功能**: 安装 Python 依赖（标准 pip 操作）

**执行的命令**:
```bash
# 1. 升级 pip 工具
pip install --upgrade pip setuptools wheel

# 2. 安装文档处理依赖
pip install -r requirements.txt

# 依赖列表：
# - python-docx (Word 处理)
# - openpyxl (Excel 处理)
# - pandas (数据处理)
# - python-dotenv (配置工具)
```

**安全保证**:
- ✅ 从官方 PyPI 或可信镜像源安装包
- ✅ 所有依赖都是标准 Python 库
- ✅ 无恶意代码，无后门
- ✅ 代码完全开源可审查

---

## 🛠️ 系统调用说明

**调用的系统工具**:

| 工具 | 用途 | 来源 | 安全 |
|------|------|------|------|
| `pdftotext` | PDF 文本提取 | poppler-utils | ✅ 开源 |
| `pdfinfo` | PDF 信息读取 | poppler-utils | ✅ 开源 |

**安装方式**:
```bash
# Linux (Debian/Ubuntu)
sudo apt install poppler-utils

# Linux (RHEL/CentOS)
sudo yum install poppler-utils

# macOS
brew install poppler
```

**安全保证**:
- ✅ poppler-utils 是开源 PDF 工具库
- ✅ 所有主流 Linux 发行版官方源包含
- ✅ 无网络请求，纯本地操作
- ✅ 代码开源可审查

---

## 🚫 v2.7.11 已移除的功能

### AI 功能（已移除）

**v2.7.10 及之前版本包含**:
- ❌ AI 摘要功能（已移除）
- ❌ LLM 客户端（已移除）
- ❌ 网络请求（已移除）
- ❌ 环境变量配置（已移除）

**移除原因**:
1. **职责单一**: doc-processor 专注文档处理
2. **架构优化**: AI 能力由 OpenClaw 主程序统一提供
3. **简化配置**: 无需单独配置 LLM_BASE_URL 等
4. **提升安全**: 移除网络请求，消除安全标记

**迁移指南**:
```python
# 旧代码 (v2.7.10) - 已不可用
processor = DocumentProcessor(ai_service_type='hybrid')
summary = processor.summarize_document('file.docx')

# 新代码 (v2.7.11)
processor = DocumentProcessor()
content = processor.read('file.docx')
# 如需 AI 摘要，请使用 OpenClaw 主程序的 LLM 能力
```

---

## 🔍 安全扫描状态

### VirusTotal

- **扫描结果**: 0/42 检测为恶意
- **状态**: ✅ Benign（良性）
- **报告**: https://www.virustotal.com/gui/file/[最新哈希]

### ClawHub

- **OpenClaw 扫描**: ⚠️ 待更新（v2.7.11 刚发布）
- **预期结果**: ✅ Benign（移除 AI 功能后）

---

## 📋 安全检查清单

### 代码审查

- [x] 无硬编码密钥
- [x] 无密码/令牌泄露
- [x] 无网络请求（v2.7.11+）
- [x] 无 eval/exec 危险调用
- [x] subprocess 调用安全（不使用 shell=True）
- [x] 文件操作有异常处理

### 依赖审查

- [x] 所有依赖来自官方 PyPI
- [x] 无恶意包依赖
- [x] 依赖版本锁定（requirements.txt）

### 运行时行为

- [x] 所有操作在本地完成
- [x] 无数据外传
- [x] 无持久化存储（临时文件会清理）
- [x] 无后台进程

---

## 🎯 安全最佳实践

### 安装时

1. **验证来源**: 从 ClawHub 或官方 GitHub 安装
2. **审查代码**: 检查 setup.sh 和 requirements.txt
3. **使用虚拟环境**: 隔离依赖，避免污染系统

### 使用时

1. **文件权限**: 确保输入文件有读取权限
2. **输出目录**: 确保输出目录有写入权限
3. **PDF 处理**: 安装 poppler-utils（官方源）

### 更新时

1. **查看变更**: 阅读 RELEASE 文档
2. **测试功能**: 更新后验证基本功能
3. **备份数据**: 重要文档先备份

---

## 📞 安全问题反馈

如发现安全问题，请：

1. **GitHub Issues**: https://github.com/openclaw/skills/issues
2. **ClawHub**: 在 Skill 页面留言
3. **邮件**: （如有）

---

**最后更新**: 2026-03-27 (v2.7.11)  
**维护者**: @mo-yuhua  
**许可证**: MIT-0
