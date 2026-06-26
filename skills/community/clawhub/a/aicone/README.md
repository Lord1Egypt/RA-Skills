# AI Clone Skill - 使用说明

**版本：** 2.0.0 (安全加固版)  
**创建时间：** 2026-03-04  
**安全更新：** 2026-03-06  
**开发者：** 机器猫 🐱

---

## 📖 技能简介

**AI Clone** 是一个通用的 AI 机器人克隆技能，任何 AI 机器人都可以使用此技能：

- ✅ **导出自己的配置** → 生成克隆包发给别人
- ✅ **导入别人的配置** → 复制对方的能力和经验
- ✅ **安全验证** → 导入前验证克隆包安全性

**适用场景：**
- 🔁 克隆机器猫到多个设备
- 👥 复制任意 AI 机器人 A → B
- 💾 备份和恢复机器人配置
- 🎁 团队间共享机器人能力包

---

## 🔒 安全特性（v2.0 新增）

### 已修复的安全问题

| 问题 | 风险等级 | 修复方案 | 状态 |
|------|----------|----------|------|
| ZIP Slip 漏洞 | 🔴 高危 | 路径验证 + 规范化检查 | ✅ 已修复 |
| 固定临时目录 | 🟡 中危 | 使用 `tempfile.TemporaryDirectory` | ✅ 已修复 |
| 元数据路径泄露 | 🟡 中危 | 默认脱敏（可配置） | ✅ 已修复 |
| 文档代码不一致 | 🟢 低危 | 统一命令参数 | ✅ 已修复 |
| 敏感文件无保护 | 🟡 中危 | 自动排除 `.env`, `*.key` 等 | ✅ 已修复 |

### 使用前的安全建议

1. **仅导入可信来源的克隆包**
2. **导入前运行 `verify` 命令验证**
3. **使用 `--preview` 预览包内容**
4. **在隔离环境首次测试**

---

## 🚀 快速开始

### 第一步：安装技能

```bash
# 从 clawhub 安装（发布后）
clawhub install ai-clone

# 或手动安装
cp -r ai-clone /your/workspace/skills/
```

### 第二步：使用技能

**机器人 A（源）：导出配置**
```bash
cd /path/to/robot-a/workspace
python scripts/clone_robot.py export
```

**机器人 B（目标）：导入配置**
```bash
cd /path/to/robot-b/workspace

# 1. 验证安全性（推荐）
python scripts/clone_robot.py verify clone-package.zip

# 2. 预览内容
python scripts/clone_robot.py import clone-package.zip --preview

# 3. 导入配置
python scripts/clone_robot.py import clone-package.zip
```

---

## 📦 详细使用说明

### 命令 1：export（导出配置）

**功能：** 扫描当前工作区，打包核心配置文件

**基本用法：**
```bash
python scripts/clone_robot.py export
```

**输出示例：**
```
📦 导出配置...
   源：/home/admin/.openclaw/workspace
📋 扫描工作区...
  ✅ SOUL.md (1.6KB)
  ✅ IDENTITY.md (0.7KB)
  ✅ USER.md (0.6KB)
  ✅ MEMORY.md (1.2KB)
  ✅ HEARTBEAT.md (2.0KB)
  ✅ TOOLS.md (0.8KB)
  ✅ AGENTS.md (7.7KB)

📋 准备临时文件...
   临时目录：/tmp/ai-clone-xyz123
  ✅ SOUL.md
  ✅ IDENTITY.md
  ...
  ℹ️  元数据已脱敏（不包含绝对路径）
  ✅ clone_metadata.json

🗜️  打包为 clone-package-20260304-180000.zip...

✅ 导出完成！
   文件：clone-package-20260304-180000.zip
   大小：9.0KB
   包含：7 个核心文件
   安全版本：hardened v2.0
```

**高级选项：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--source` | 指定源工作区路径 | `--source /path/to/workspace` |
| `--output` | 自定义输出文件名 | `--output my-robot-clone.zip` |
| `--exclude` | 额外排除的文件 | `--exclude "*.env" "secrets/"` |
| `--no-optional` | 不包含可选目录 | `--no-optional` |
| `--keep-paths` | 保留完整路径（默认脱敏） | `--keep-paths` |

**示例：**
```bash
# 指定源目录
python scripts/clone_robot.py export --source /home/admin/.openclaw/workspace

# 自定义输出文件名
python scripts/clone_robot.py export --output machine-cat-backup.zip

# 同时指定源和输出
python scripts/clone_robot.py export \
  --source /path/to/workspace \
  --output my-clone.zip

# 不包含可选目录（仅核心文件）
python scripts/clone_robot.py export --no-optional

# 额外排除敏感文件
python scripts/clone_robot.py export --exclude "*.env" "*.key"
```

---

### 命令 2：import（导入配置）

**功能：** 从克隆包导入配置到目标工作区

**基本用法：**
```bash
python scripts/clone_robot.py import clone-package.zip
```

**输出示例：**
```
🔍 验证 ZIP 包安全性...
  ✅ 安全性检查通过

📥 导入配置...
   包：clone-package.zip
   目标：/home/admin/.openclaw/workspace

📋 克隆包信息:
   创建时间：2026-03-04T18:00:00.123456
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

**高级选项：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--target` | 指定目标工作区路径 | `--target /path/to/workspace` |
| `--preview` | 预览包内容（不导入） | `--preview` |
| `--force` | 跳过确认直接导入 | `--force` |

**示例：**
```bash
# 预览包内容
python scripts/clone_robot.py import clone-package.zip --preview

# 指定目标目录
python scripts/clone_robot.py import clone-package.zip --target /path/to/workspace

# 跳过确认（自动化场景）
python scripts/clone_robot.py import clone-package.zip --force

# 组合使用
python scripts/clone_robot.py import clone-package.zip \
  --target /path/to/workspace \
  --force
```

---

### 命令 3：verify（验证安全）⭐ 新增

**功能：** 验证克隆包的安全性

**基本用法：**
```bash
python scripts/clone_robot.py verify clone-package.zip
```

**输出示例：**
```
🔍 验证 ZIP 包安全性...
  ✅ 所有文件路径安全
  ✅ 无绝对路径
  ✅ 无可疑文件
  ✅ 安全性检查通过
```

**验证内容：**
- ✅ ZIP Slip 防护检查
- ✅ 绝对路径检查
- ✅ 路径遍历检查
- ✅ 可疑文件检查（.exe, .bat, .sh 等）

---

## 📋 核心配置文件

克隆脚本会自动识别和复制以下文件：

### 必选文件（核心身份）
| 文件 | 说明 | 大小示例 |
|------|------|----------|
| `SOUL.md` | 人格和价值观 | 1.6KB |
| `IDENTITY.md` | 机器人身份定义 | 0.7KB |
| `USER.md` | 用户信息 | 0.6KB |
| `MEMORY.md` | 长期记忆 | 1.2KB |
| `HEARTBEAT.md` | 任务机制 | 2.0KB |
| `TOOLS.md` | 本地工具配置 | 0.8KB |
| `AGENTS.md` | Agent 配置 | 7.7KB |

### 可选目录（能力和资产）
| 目录 | 说明 | 大小示例 |
|------|------|----------|
| `memory/` | 每日记忆文件 | 45.3KB (15 文件) |
| `skills/` | 技能包 | 1.2MB (8 技能) |
| `scripts/` | 自动化脚本 | 156.7KB (23 文件) |
| `projects/` | 项目文档 | 可变 |
| `docs/` | 文档资料 | 可变 |

---

## 🔒 安全机制详解

### 1. ZIP Slip 防护

**问题描述：**  
攻击者可以构造包含 `../../../etc/passwd` 路径的 ZIP 文件，解压时覆盖系统文件。

**修复方案：**
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

**问题描述：**  
旧版本使用固定的 `/tmp/ai-clone-temp` 目录，可能被攻击者利用（符号链接攻击、竞争条件）。

**修复方案：**
```python
# ❌ 旧版本（不安全）
temp_dir = Path("/tmp/ai-clone-temp")
if temp_dir.exists():
    shutil.rmtree(temp_dir)
temp_dir.mkdir(parents=True)

# ✅ 新版本（安全）
with tempfile.TemporaryDirectory(prefix="ai-clone-") as temp_dir:
    # 自动清理，防竞争条件
    # 随机目录名，防预测
    ...
```

**优势：**
- ✅ 随机临时目录名（防预测）
- ✅ 自动清理（防残留）
- ✅ 原子操作（防竞争）

### 3. 元数据脱敏

**问题描述：**  
旧版本在 `clone_metadata.json` 中包含完整的源工作区路径，可能泄露：
- 文件系统结构
- 用户名
- 操作系统信息

**修复方案：**
```python
# ❌ 旧版本（泄露路径）
metadata = {
    "source_workspace": "/home/admin/.openclaw/workspace",
    "created_at": "2026-03-04T18:00:00"
}

# ✅ 新版本（脱敏）
metadata = {
    "version": "2.0",
    "created_at": "2026-03-04T18:00:00",
    "files": ["SOUL.md", "IDENTITY.md", ...],
    "security_version": "hardened",
    # 仅包含目录名，不包含完整路径
    "source_workspace_name": "workspace"
}
```

**保护内容：**
- ✅ 隐藏完整文件系统路径
- ✅ 隐藏用户名
- ✅ 隐藏操作系统信息

### 4. 敏感文件自动排除

**问题描述：**  
用户可能意外将包含 API Keys、密码的文件打包。

**修复方案：**
```python
DEFAULT_EXCLUDE_PATTERNS = [
    ".git/",
    "__pycache__/",
    ".openclaw/workspace-state.json",
    "*.log",
    ".DS_Store",
    "*.pyc",
    ".env",           # 新增：环境变量文件
    "*.key",          # 新增：密钥文件
    "*.secret",       # 新增：敏感文件
    "*.pem", "*.crt", # 新增：证书文件
]

SENSITIVE_PATTERNS = [
    "*api_key*",
    "*apikey*",
    "*secret*",
    "*password*",
    "*credential*",
]
```

**自动排除：**
- ✅ `.env` - 环境变量（常含 API Keys）
- ✅ `*.key` - 密钥文件
- ✅ `*.secret` - 敏感文件
- ✅ `*.pem`, `*.crt` - 证书文件
- ✅ 包含 `api_key`, `password` 等关键词的文件

---

## ⚠️ 安全注意事项

### 导入前的检查清单

**必须完成：**
- [ ] 克隆包来自可信来源
- [ ] 已验证发送者身份
- [ ] 运行 `verify` 命令检查安全性
- [ ] 使用 `--preview` 查看包内容

**建议完成：**
- [ ] 在测试环境首次导入
- [ ] 备份现有配置
- [ ] 检查 `clone_metadata.json` 内容

### 导出前的检查清单

**必须完成：**
- [ ] 检查是否包含 `.env` 文件
- [ ] 检查是否包含 API Keys
- [ ] 检查是否包含证书文件

**建议完成：**
- [ ] 使用默认脱敏（不添加 `--keep-paths`）
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

### v2.0.0 (2026-03-06) - 安全加固版 🎉

**安全修复：**
- 🔒 **修复 ZIP Slip 漏洞** - 路径验证 + 规范化检查
- 🔒 **使用 tempfile.TemporaryDirectory** - 替代固定临时路径
- 🔒 **元数据脱敏** - 默认隐藏绝对路径
- 🔒 **敏感文件自动排除** - `.env`, `*.key`, `*.secret` 等

**功能改进：**
- ✅ **新增 verify 命令** - 导入前验证克隆包
- ✅ **新增 --preview 参数** - 预览包内容
- ✅ **新增 --force 参数** - 跳过确认（自动化）
- ✅ **新增 --exclude 参数** - 额外排除文件
- ✅ **文档代码统一** - 所有命令参数一致

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
**解决：** 
1. 拒绝导入
2. 联系发送者重新打包
3. 报告安全问题

### 问题 2：找不到核心配置文件

```
❌ 警告：未找到任何核心配置文件
   请确保在正确的 workspace 目录运行，或检查 --source 参数
```

**原因：** 不在正确的 workspace 目录  
**解决：** 
1. 确认当前目录有 `SOUL.md`
2. 或使用 `--source` 指定正确路径

### 问题 3：元数据包含敏感路径

```
⚠️ 元数据包含绝对路径
```

**原因：** 使用了 `--keep-paths` 参数  
**解决：** 
1. 重新导出，不使用 `--keep-paths`
2. 或手动编辑 `clone_metadata.json` 删除路径

### 问题 4：导入时需要确认

```
⚠️  注意：这将覆盖目标目录的现有文件！
   使用 --force 跳过确认
```

**原因：** 安全确认机制  
**解决：** 
1. 输入 `y` 确认导入
2. 或使用 `--force` 跳过确认（自动化场景）

---

## 📝 最佳实践

### 定期备份
```bash
# 每周备份一次
python scripts/clone_robot.py export --output backup-$(date +%Y%m%d).zip
```

### 团队共享
```bash
# 导出团队标准配置
python scripts/clone_robot.py export \
  --output team-standard.zip \
  --exclude "*.env" \
  --no-optional

# 分发给团队成员
# 团队成员导入
python scripts/clone_robot.py import team-standard.zip --force
```

### 安全审计
```bash
# 定期检查克隆包
for zip in *.zip; do
  echo "检查：$zip"
  python scripts/clone_robot.py verify "$zip"
  python scripts/clone_robot.py import "$zip" --preview
done
```

---

*技能版本：2.0.0*  
*安全版本：hardened*  
*创建时间：2026-03-04*  
*安全更新：2026-03-06*  
*机器猫 🐱 开发*

---

## 📧 反馈与支持

如有安全问题或改进建议，请联系：
- GitHub Issues
- 机器猫 🐱

**安全报告：** 发现安全问题请优先私信联系，感谢配合！
