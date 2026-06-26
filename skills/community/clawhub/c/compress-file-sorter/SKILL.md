---
name: file-sorter
description: 解析压缩文件并根据文件名关键词自动分类到指定目录。每当用户需要处理压缩文件时，请使用此技能。触发条件包括：提及"解压"、"文件解压"等。也用于将文件根据用户指定的方法进行分类处理。如果用户要求解压文件并将文件按指定文件名进行分类，请使用此技能。
---

## 核心功能

- 解压用户提供的压缩包（zip、rar、7z、tar、tar.gz、tar.bz2）
- 根据文件名中的关键词匹配预设分类规则
- 生成分类报告供用户确认，确认后执行文件移动或复制
- 分类规则持久化到 `data/rules.json`，跨会话复用
- 解压到临时目录，分类完成后可选清理

## 实现脚本

核心逻辑在 `data/file_sorter.py`，提供 CLI 和 Python API 两种调用方式。

### CLI 调用方式

所有操作通过 Bash 工具执行以下命令（`SKILL_DIR` 为本 skill 目录的绝对路径）：

```bash
# 初始化 rules.json（首次使用）
python SKILL_DIR/data/file_sorter.py init

# 添加分类规则（keywords 逗号分隔，mode 可选: contains/startswith/endswith/regex）
python SKILL_DIR/data/file_sorter.py add "合同" "合同,contract,协议" "合同文件" contains

# 删除规则
python SKILL_DIR/data/file_sorter.py delete "合同"

# 列出所有规则
python SKILL_DIR/data/file_sorter.py list

# 预览分类结果（不移动文件）
python SKILL_DIR/data/file_sorter.py classify "/path/to/archive.zip" "/path/to/output"

# 执行分类并移动文件
python SKILL_DIR/data/file_sorter.py execute "/path/to/archive.zip" "/path/to/output"

# 带密码解压
python SKILL_DIR/data/file_sorter.py execute "/path/to/archive.zip" "/path/to/output" "mypassword"
```
### Python API 调用方式

当需要更灵活的控制时（如分步确认），可在 Bash 中用 inline Python：

```python
import sys; sys.path.insert(0, "SKILL_DIR/data")
from file_sorter import load_config, extract, classify, generate_report, move_files

# 加载规则
rules, settings = load_config()["rules"], load_config()["settings"]

# 解压
dest, files = extract("/path/to/archive.zip")

# 分类（仅计算，不移动）
classified = classify(files, rules, settings)

# 生成报告
print(generate_report("archive.zip", classified))

# 用户确认后执行移动
ok, skipped = move_files(classified, "/path/to/output", settings["conflict_strategy"])
```

## 数据结构

所有分类规则存储在 `data/rules.json`。首次使用时自动创建，结构如下：

```json
{
  "rules": [],
  "settings": {
    "unmatched_dir": "_未分类",
    "conflict_strategy": "rename"
  }
}
```

### 规则对象

```json
{
  "name": "合同",
  "keywords": ["合同", "contract", "协议"],
  "target_dir": "合同文件",
  "match_mode": "contains"
}
```

字段说明：
- `name` — 分类名称，用于报告展示
- `keywords` — 文件名匹配关键词列表，任一命中即匹配
- `target_dir` — 目标目录路径（相对于用户指定的输出目录）
- `match_mode` — 匹配模式：`contains`（默认）、`startswith`、`endswith`、`regex`

### 全局设置

- `unmatched_dir` — 未匹配文件存放目录，默认 `_未分类`
- `conflict_strategy` — 文件名冲突策略：`rename`（默认）、`skip`、`overwrite`

## 工作流程

### 1. 初始化

**触发条件：** 首次对话，或 `data/rules.json` 不存在。

执行：
```bash
python SKILL_DIR/data/file_sorter.py init
```

然后引导用户添加第一条分类规则。

### 2. 管理规则

**添加规则：**
```bash
python SKILL_DIR/data/file_sorter.py add "规则名" "关键词1,关键词2" "目标目录" contains
```

**查看规则：**
```bash
python SKILL_DIR/data/file_sorter.py list
```

**删除规则：**
```bash
python SKILL_DIR/data/file_sorter.py delete "规则名"
```

**编辑规则：** 先 delete 再 add，或直接用 Read/Edit 工具修改 `data/rules.json`。

**修改全局设置：** 直接用 Edit 工具修改 `data/rules.json` 中的 `settings` 字段。
### 3. 分类文件（核心流程）

**触发条件：** 用户提供压缩文件路径，或说"分类这个文件"、"整理这个压缩包"等。

**步骤 1 — 预览：**
```bash
python SKILL_DIR/data/file_sorter.py classify "/path/to/archive.zip" "/path/to/output"
```
这会解压到临时目录、匹配规则、输出分类报告，但不移动文件。

**步骤 2 — 展示报告并询问用户确认。**

**步骤 3 — 用户确认后执行：**
```bash
python SKILL_DIR/data/file_sorter.py execute "/path/to/archive.zip" "/path/to/output"
```
这会解压、分类、移动文件，并自动清理临时目录。

### 4. 预览模式

与步骤 1 相同，使用 `classify` 命令。明确告知用户这是预览，文件未移动。

### 5. 批量处理

逐个对每个压缩文件执行 `classify` 或 `execute`：
```bash
for f in "/path/a.zip" "/path/b.zip"; do
  python SKILL_DIR/data/file_sorter.py execute "$f" "/path/to/output"
done
```

## 支持的压缩格式

| 格式 | 扩展名 | 实现方式 |
|---|---|---|
| ZIP | `.zip` | Python `zipfile`（内置） |
| TAR | `.tar` | Python `tarfile`（内置） |
| TAR+GZ | `.tar.gz`, `.tgz` | Python `tarfile`（内置） |
| TAR+BZ2 | `.tar.bz2`, `.tbz2` | Python `tarfile`（内置） |
| 7-Zip | `.7z` | `py7zr` 库 或 `7z` 命令行 |
| RAR | `.rar` | `rarfile` 库 或 `unrar` 命令行 |

zip/tar 格式无需额外安装。7z/rar 格式需要额外依赖，缺失时脚本会自动尝试命令行工具，若都不可用则报错提示安装：
```bash
pip install py7zr   # 7z 支持
pip install rarfile  # rar 支持
```

## 分类报告格式

脚本自动生成 Markdown 表格：

```
📂 分类报告 — example.zip（共 15 个文件）

| # | 文件名 | 匹配规则 | 目标目录 |
|---|--------|----------|----------|
| 1 | 合同_2026.pdf | 合同 | 合同文件/ |
| 2 | 发票_03.jpg | 发票 | 财务发票/ |
| 15 | readme.txt | ⚠️ 未匹配 | _未分类/ |

📊 统计：合同 5 个 | 发票 4 个 | ⚠️ 未匹配 3 个
```

## 错误处理

脚本内置以下错误处理，出错时会抛出明确的中文错误信息：
- `FileNotFoundError` — 文件不存在
- `ValueError` — 格式不支持，或归档包含危险路径成员（安全拒绝）
- `RuntimeError` — 命令行工具执行失败（7z/unrar）
- `zipfile.BadZipFile` — 压缩文件损坏
- 密码保护 — 通过第 4 个参数传入密码

## 安全机制

脚本在解压前对所有归档成员执行路径安全校验：
- 拒绝绝对路径成员（如 `/etc/passwd`）
- 拒绝包含 `..` 的路径遍历成员（如 `../../etc/passwd`）
- 校验解压目标路径确实在指定目录内（resolve 后比较前缀）
- TAR 格式额外跳过符号链接和特殊文件（设备文件等）
- 命令行工具（7z/unrar）解压后二次校验所有文件位置

如果归档包含任何危险成员，脚本会中止解压并列出具体的危险条目。

## 快速参考

| 用户意图 | 执行的命令 |
|---|---|
| 首次使用 | `python .../file_sorter.py init` → 引导添加规则 |
| 添加规则 | `python .../file_sorter.py add ...` |
| 查看规则 | `python .../file_sorter.py list` |
| 删除规则 | `python .../file_sorter.py delete ...` |
| 分类文件 | `python .../file_sorter.py classify ...` → 确认 → `execute ...` |
| 预览 | `python .../file_sorter.py classify ...` |
| 批量处理 | 循环调用 `execute` |

