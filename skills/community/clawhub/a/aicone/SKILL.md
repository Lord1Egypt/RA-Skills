---
name: ai-clone
description: 通用 AI 机器人克隆技能（安全加固版 v2.0）。支持导出/导入配置，ZIP Slip 防护，元数据脱敏，敏感文件自动排除。用于 A→B 能力复制、团队共享、备份恢复。
version: 2.0.0
security: hardened
---

# AI 机器人克隆技能 v2.0（安全加固版）

**任何 AI 机器人都可以使用的克隆工具**

---

## 🔒 安全特性（v2.0 新增）

### 已修复的安全问题

| 问题 | 风险等级 | 修复方案 |
|------|----------|----------|
| ZIP Slip 漏洞 | 🔴 高危 | 路径验证 + 规范化检查 |
| 固定临时目录 | 🟡 中危 | 使用 `tempfile.TemporaryDirectory` |
| 元数据路径泄露 | 🟡 中危 | 默认脱敏（可配置） |
| 文档代码不一致 | 🟢 低危 | 统一命令参数 |
| 敏感文件无保护 | 🟡 中危 | 自动排除 `.env`, `*.key` 等 |

### 安全验证

```bash
# 导入前验证克隆包
python scripts/clone_robot.py verify clone-package.zip
```

---

## 🎯 核心流程

```
┌─────────────┐                    ┌─────────────┐
│  机器人 A   │                    │  机器人 B   │
│  (源)       │                    │  (目标)     │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │ 1. 使用技能导出配置               │
       │    → clone-package.zip          │
       │                                  │
       ├─────────────────────────────────>│
       │         传输文件                  │
       │                                  │
       │                                  │ 2. 使用技能导入配置
       │                                  │    ← clone-package.zip
       │                                  │
       ▼                                  ▼
```

---

## 📦 机器人 A：导出配置

**任何机器人执行以下命令导出自己：**

```bash
# 基本导出（推荐）
python scripts/clone_robot.py export

# 指定输出文件名
python scripts/clone_robot.py export --output my-clone-package.zip

# 指定源目录
python scripts/clone_robot.py export --source /path/to/workspace

# 不包含可选目录（仅核心文件）
python scripts/clone_robot.py export --no-optional

# 额外排除文件
python scripts/clone_robot.py export --exclude "*.env" "secrets/"

# 保留完整路径（默认脱敏）
python scripts/clone_robot.py export --keep-paths
```

**输出示例：**
```
📦 导出配置...
   源：/home/admin/.openclaw/workspace
📋 扫描工作区...
  ✅ SOUL.md (2.1KB)
  ✅ IDENTITY.md (1.5KB)
  ✅ USER.md (892B)
  ✅ MEMORY.md (3.2KB)
  ✅ HEARTBEAT.md (1.8KB)
  ✅ TOOLS.md (0.9KB)
  ✅ AGENTS.md (7.7KB)

📋 准备临时文件...
   临时目录：/tmp/ai-clone-xyz123
  ✅ SOUL.md
  ✅ IDENTITY.md
  ...
  ℹ️  元数据已脱敏（不包含绝对路径）
  ✅ clone_metadata.json

🗜️  打包为 clone-package-20260306-185500.zip...

✅ 导出完成！
   文件：clone-package-20260306-185500.zip
   大小：9.1KB
   包含：7 个核心文件
   安全版本：hardened v2.0
```

**然后：** 把 `clone-package.zip` 发给机器人 B（邮件/网盘/聊天工具）

---

## 📥 机器人 B：导入配置

**收到克隆包后执行：**

```bash
# 预览包内容（不执行导入）
python scripts/clone_robot.py import clone-package.zip --preview

# 验证安全性
python scripts/clone_robot.py verify clone-package.zip

# 导入配置（需要确认）
python scripts/clone_robot.py import clone-package.zip

# 跳过确认直接导入
python scripts/clone_robot.py import clone-package.zip --force

# 指定目标目录
python scripts/clone_robot.py import clone-package.zip --target /path/to/workspace
```

**输出示例：**
```
🔍 验证 ZIP 包安全性...
  ✅ 安全性检查通过

📥 导入配置...
   包：clone-package.zip
   目标：/home/admin/.openclaw/workspace

📋 克隆包信息:
   创建时间：2026-03-06T18:55:00.123456
   安全版本：hardened
   文件数量：7

📋 即将导入以下文件:
  ✅ SOUL.md
  ✅ IDENTITY.md
  ✅ USER.md
  ✅ MEMORY.md
  ✅ HEARTBEAT.md
  ✅ TOOLS.md
  ✅ AGENTS.md

⚠️  注意：这将覆盖目标目录的现有文件！
   使用 --force 跳过确认

确认导入？(y/N): y

📥 正在导入...
  ✅ SOUL.md
  ✅ IDENTITY.md
  ...

✅ 导入完成！
   目标：/home/admin/.openclaw/workspace
   导入：7 个文件

🎉 机器人已成功复制配置！
   安全版本：hardened v2.0
```

---

## 📋 核心配置文件

克隆脚本会自动识别和复制以下文件：

### 必选文件（核心身份）
| 文件 | 说明 |
|------|------|
| `SOUL.md` | 人格和价值观 |
| `IDENTITY.md` | 机器人身份定义 |
| `USER.md` | 用户信息 |
| `MEMORY.md` | 长期记忆 |
| `HEARTBEAT.md` | 任务机制 |
| `TOOLS.md` | 本地工具配置 |
| `AGENTS.md` | Agent 配置 |

### 可选目录（能力和资产）
| 目录 | 说明 |
|------|------|
| `memory/` | 每日记忆文件 |
| `skills/` | 技能包 |
| `scripts/` | 自动化脚本 |
| `projects/` | 项目文档 |
| `docs/` | 文档资料 |

---

## 🔒 安全机制详解

### 1. ZIP Slip 防护

```python
def is_path_safe(path_str: str) -> bool:
    # 拒绝绝对路径
    if os.path.isabs(path_str):
        return False
    
    # 拒绝路径遍历
    if ".." in path_str.split(os.sep):
        return False
    
    # 规范化路径并再次检查
    normalized = os.path.normpath(path_str)
    if normalized.startswith("..") or os.path.isabs(normalized):
        return False
    
    return True
```

**防护效果：**
- ✅ 阻止 `../../../etc/passwd` 等路径遍历攻击
- ✅ 阻止绝对路径 `/etc/passwd` 覆盖系统文件
- ✅ 双重验证（原始 + 规范化）

### 2. 临时目录安全

```python
# ❌ 旧版本（不安全）
temp_dir = Path("/tmp/ai-clone-temp")

# ✅ 新版本（安全）
with tempfile.TemporaryDirectory(prefix="ai-clone-") as temp_dir:
    # 自动清理，防竞争条件
    ...
```

**优势：**
- ✅ 随机临时目录名（防预测）
- ✅ 自动清理（防残留）
- ✅ 原子操作（防竞争）

### 3. 元数据脱敏

```python
# ❌ 旧版本（泄露路径）
metadata = {
    "source_workspace": "/home/admin/.openclaw/workspace"
}

# ✅ 新版本（脱敏）
metadata = {
    "source_workspace_name": "workspace",  # 仅目录名
    "security_version": "hardened"
}
```

**保护内容：**
- ✅ 隐藏完整文件系统路径
- ✅ 隐藏用户名
- ✅ 隐藏操作系统信息

### 4. 敏感文件自动排除

```python
DEFAULT_EXCLUDE_PATTERNS = [
    ".env",           # 环境变量
    "*.key",          # 密钥文件
    "*.secret",       # 敏感文件
    "*.pem", "*.crt", # 证书文件
    # ... 更多
]

SENSITIVE_PATTERNS = [
    "*api_key*",
    "*apikey*",
    "*secret*",
    "*password*",
    "*credential*",
]
```

---

## 🔧 命令参考

### 导出配置
```bash
python scripts/clone_robot.py export [选项]

选项:
  --source PATH       源工作区路径
  --output FILE       输出文件名
  --exclude PATTERN   额外排除的文件/目录（可重复）
  --no-optional       不包含可选目录
  --keep-paths        在元数据中保留完整路径（默认脱敏）
```

### 导入配置
```bash
python scripts/clone_robot.py import PACKAGE [选项]

选项:
  --target PATH       目标工作区路径
  --preview           预览包内容（不执行导入）
  --force             跳过确认直接导入
```

### 验证安全
```bash
python scripts/clone_robot.py verify PACKAGE

验证项:
  ✅ ZIP Slip 检查
  ✅ 绝对路径检查
  ✅ 可疑文件检查
```

---

## ⚠️ 安全注意事项

### 导入前的检查清单

1. **验证来源**
   - [ ] 克隆包来自可信来源
   - [ ] 已验证发送者身份

2. **安全验证**
   - [ ] 运行 `verify` 命令检查
   - [ ] 查看包内文件列表（`--preview`）

3. **环境隔离**
   - [ ] 在测试环境首次导入
   - [ ] 备份现有配置

### 导出前的检查清单

1. **敏感信息**
   - [ ] 检查是否包含 `.env` 文件
   - [ ] 检查是否包含 API Keys
   - [ ] 检查是否包含证书文件

2. **元数据**
   - [ ] 使用默认脱敏（`--redact-metadata`）
   - [ ] 或手动指定 `--keep-paths`（谨慎）

3. **文件审查**
   - [ ] 使用 `unzip -l clone-package.zip` 查看内容
   - [ ] 确认无意外文件

---

## 🧪 验证克隆

部署后运行验证：
```bash
# 1. 检查核心文件
ls -la SOUL.md IDENTITY.md USER.md MEMORY.md

# 2. 验证记忆文件
cat MEMORY.md | head -20

# 3. 检查技能包
ls skills/

# 4. 启动测试
openclaw status
```

---

## 📊 克隆报告示例

```
📋 检查核心配置文件...
  ✅ SOUL.md (2.1KB)
  ✅ IDENTITY.md (1.5KB)
  ✅ USER.md (892B)
  ✅ MEMORY.md (3.2KB)
  ✅ HEARTBEAT.md (1.8KB)

📁 检查可选目录...
  ✅ memory/ (15 文件，45.3KB)
  ✅ skills/ (8 技能，1.2MB)
  ✅ scripts/ (23 文件，156.7KB)

📊 扫描完成:
   机器人：machine-cat
   核心文件：7 个
   可选目录：3 个
   总大小：1.4MB

📦 创建克隆包...
   源：/home/admin/.openclaw/workspace
   目标：machine-cat-clone.zip

✅ 克隆包创建成功！
   文件：machine-cat-clone.zip
   大小：456.2KB
   安全版本：hardened v2.0
```

---

## 🔄 版本历史

### v2.0.0 (2026-03-06) - 安全加固版
- 🔒 **修复 ZIP Slip 漏洞** - 路径验证 + 规范化检查
- 🔒 **使用 tempfile.TemporaryDirectory** - 替代固定临时路径
- 🔒 **元数据脱敏** - 默认隐藏绝对路径
- 🔒 **敏感文件自动排除** - `.env`, `*.key`, `*.secret` 等
- 📝 **文档代码统一** - 所有命令参数一致
- ✅ **新增 verify 命令** - 导入前验证克隆包

### v1.0.0 (2026-03-04) - 初始版本
- ✅ 基础导出/导入功能
- ✅ 核心配置文件识别
- ✅ 临时目录清理

---

## 🆘 故障排查

### 问题 1：导入时提示"不安全路径"
```
❌ 不安全路径：../../../etc/passwd
```
**原因：** 克隆包可能包含恶意文件  
**解决：** 拒绝导入，联系发送者重新打包

### 问题 2：找不到核心配置文件
```
❌ 警告：未找到任何核心配置文件
```
**原因：** 不在正确的 workspace 目录  
**解决：** 使用 `--source` 指定正确路径

### 问题 3：元数据包含敏感路径
```
⚠️ 元数据包含绝对路径
```
**原因：** 使用了 `--keep-paths` 参数  
**解决：** 重新导出，不使用该参数

---

*技能版本：2.0.0*  
*安全版本：hardened*  
*创建时间：2026-03-04*  
*安全更新：2026-03-06*  
*机器猫 🐱 开发*
