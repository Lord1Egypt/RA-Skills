---
name: archive-smart-reader
description: |-
  智能压缩文件阅读器。直接读取zip/tar/gz/tgz/bz2/xz/7z/rar
  等压缩包的内容：列出文件清单、预览内部文件内容、
  提取单个文件或全部解压、搜索压缩包内文件。
  支持图片压缩包直接读取显示。每次使用自动学习改进。
  触发词：压缩包、zip文件、解压、tar包、读压缩文件、archive、查看压缩包。
agent_created: true
version: 1.0.0
display_name: "智能压缩阅读器"
display_name_en: "Archive Smart Reader"
description_zh: "直接读取预览各类压缩包文件内容，越用越好用"
description_en: "Smart archive reader that improves with every use"
visibility: "public"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 智能压缩文件阅读器

## 为什么需要本技能

WorkBuddy 无法直接读取 zip/tar/rar 等压缩包里的文件。每次收到
压缩包都需要手动解压后再操作，非常麻烦。

本技能让你能：
- ✅ **直接问**："看看这个zip里有什么文件"
- ✅ **直接预览**："帮我看看压缩包里的readme.txt"
- ✅ **直接提取**："把里面的图片提取出来"
- ✅ **自动学习**：记住你的使用习惯，越来越快

---

## 支持格式

| 格式 | 支持级别 | 说明 |
|------|---------|------|
| .zip | ⭐⭐⭐ 完整 | 列表/预览/提取/搜索 |
| .tar | ⭐⭐⭐ 完整 | 列表/预览/提取 |
| .tar.gz / .tgz | ⭐⭐⭐ 完整 | 列表/预览/提取 |
| .tar.bz2 (.bz2) | ⭐⭐⭐ 完整 | 列表/预览/提取 |
| .tar.xz (.xz) | ⭐⭐⭐ 完整 | 列表/预览/提取 |
| .7z | ⭐⭐ 基础 | 安装 py7zr 后全支持 |
| .rar | ⭐⭐ 基础 | 列出文件无需外部工具；预览/提取需本机 unrar 或 7-Zip（脚本自动查找 Downloads/WorkBuddy/Claw 等位置） |

---

## 自进化学习系统

本技能每次使用都会自动记录和改进：

### 学习记忆文件
路径：`~/.workbuddy/skills/archive-smart-reader/learned_patterns.json`

```json
{
  "version": 1,
  "totalOps": 0,
  "formatStats": {
    ".zip": {"count": 0, "totalFiles": 0},
    ".tar.gz": {"count": 0, "totalFiles": 0}
  },
  "errorPatterns": {
    "password_protected": {"count": 0, "lastPath": ""},
    "corrupted_zip": {"count": 0, "lastPath": ""}
  },
  "optimizations": {
    "preferTempDir": true,
    "autoCleanup": true,
    "previewLimit": 50000
  }
}
```

### 学习内容

| 学习维度 | 具体内容 |
|---------|---------|
| 📊 格式统计 | 哪种格式用得最多 → 优先优化 |
| ❌ 错误模式 | 常见错误是什么 → 下次提前预警 |
| ⚡ 性能优化 | 大文件处理时间 → 自动调整策略 |
| 🧠 用户偏好 | 喜欢预览还是提取 → 优先推荐 |

---

## 核心能力

### 1. 列出压缩包内容

```
用户输入："帮我看看这个report.zip里有什么"

操作：
python scripts/archive_reader.py list report.zip

输出：
📁 src/
📄 src/main.py  (12,345 bytes)
📄 src/utils.py (8,921 bytes)
📁 docs/
📄 docs/README.md (3,102 bytes)
📄 data.csv (45,678 bytes)
━━━━━━━━━━━━━━━━━━━━━━━━━
总计：4个文件，2个文件夹，约70KB
```

### 2. 预览内部文件

```
用户输入："看看data.csv的内容"

操作：
python scripts/archive_reader.py peek report.zip data.csv

输出：CSV文件前50行内容（智能限制，大文件自动截取）
```

### 3. 搜索压缩包内的文件

```
用户输入："这个zip里有没有关于报告的PDF？"

操作：列出所有文件 → 按文件名/扩展名/大小过滤
→ 找到匹配项后询问是否需要预览
```

### 4. 提取文件

```
用户输入："把里面的图片都提取出来放在桌面上"

操作：
1. 列出压缩包内容 → 筛选出图片文件（.jpg/.png/.gif）
2. 逐个提取到指定目录
3. 汇报提取结果
```

### 5. 智能格式识别

自动识别压缩包格式，即使没有扩展名也能通过文件头判断：

| 文件头 | 格式 |
|--------|------|
| PK\x03\x04 | ZIP |
| \x1f\x8b | GZIP |
| 75\x73\x74\x61r | TAR |
| Rar! | RAR |
| 7z\xbc\xaf | 7z |

---

## 自动迭代机制

### 每次使用后的学习更新

```python
# 伪代码
学习数据.总操作数 += 1
学习数据.格式统计[检测到的格式]["次数"] += 1

if 操作成功:
  学习数据.格式统计[格式]["成功率"] 更新
else:
  学习数据.错误模式[错误类型]["次数"] += 1
  # 如果某错误出现≥3次，自动添加预检步骤
  if 学习数据.错误模式[错误类型]["次数"] >= 3:
    启用该格式的预检机制

# 自动优化策略
if 学习数据.总操作数 >= 10:
  分析哪些格式用得少 → 按需加载库，减少启动时间
if 某格式失败率 > 30%:
  尝试安装替代库
```

### 自动安装缺失依赖

当遇到 7z/rar 格式时，自动尝试安装支持库：

```bash
pip install py7zr  # 7z支持
pip install rarfile  # RAR支持
```

安装成功后自动更新学习记忆，下次遇到同格式直接处理。

---

## 使用流程

### 快速查看

```
用户输入："[拖拽或提供路径]这个zip里有什么"

→ 自动检测格式
→ 列出文件树（目录在前、文件在后、按大小排序）
→ 询问是否需要进一步操作（预览/提取）
```

### 预览文件

```
用户输入："帮我看看里面的config.json"

→ 自动找到压缩包
→ 定位到 config.json
→ 读取内容（文本）并显示
→ 大文件自动取前50000字符
→ 标记剩余行数
```

### 批量提取

```
用户输入："全部解压到当前目录"

→ 解压到指定目录
→ 汇报文件数量和路径
→ 自动清理临时文件（如果用了临时目录）
→ 记录本次操作到学习记忆
```

---

## 脚本工具说明

本技能附带 Python 脚本 `scripts/archive_reader.py`：

```bash
# 列出内容
python scripts/archive_reader.py list <压缩包路径>

# 预览文件
python scripts/archive_reader.py peek <压缩包路径> <内部文件路径>

# 全部解压
python scripts/archive_reader.py extract <压缩包路径> <输出目录>

# 提取单个文件
python scripts/archive_reader.py extract-file <压缩包> <内部路径> <输出路径>
```

## 注意事项

- 支持密码保护的 zip（用户需提供密码）
- 超大压缩包（>1GB）建议只列出内容，按需提取
- 图片文件会尝试直接展示（如果WorkBuddy支持）
- 所有解压操作默认使用临时目录，完成后询问是否保留
