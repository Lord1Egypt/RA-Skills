---
name: dir-text-search
description: >
  This skill should be used when the user wants to search for text or regex patterns
  inside a directory, including inside ZIP / RAR / TAR / 7z archives recursively.
  Triggers include: search in directory, find text in files, grep in folder,
  search inside archives, find pattern in logs, or any request involving scanning
  log files, config files, or compressed archives for a specific string or regex.
---

# dir-text-search — 目录文本搜索技能

## 功能概述

在指定目录下递归搜索文本或正则表达式，支持：

- 文本文件（`.txt` `.log` `.cfg` `.conf` `.ini` `.md` `.json` `.xml` `.py` `.java` 等）
- 压缩包递归解压搜索（`.zip` `.rar` `.tar` `.tar.gz` `.tar.bz2` `.7z`）
- 嵌套压缩包（解压后继续递归扫描）
- 多编码自动探测（UTF-8 → GBK → latin-1）
- 超大文件（> 100 MB）自动跳过并警告
- 结果按时间戳自动命名，保存在 `search_results/` 子目录，不会覆盖旧结果

## 触发场景

以下用户请求应加载本 Skill：

- "在 `X` 目录下查找 `Y`"
- "搜索所有日志中包含 `error` 的行"
- "在压缩包里找 `Account_Main`"
- "帮我 grep `\d{4}-\d{2}-\d{2}` 这个模式"
- 任何需要在文件/压缩包中批量搜索字符串或正则的请求

## 核心脚本

脚本路径：`scripts/search_tool.py`

### 标准调用方式

```bash
python scripts/search_tool.py --path <目标目录> --pattern "<搜索文本或正则>"
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--path` | `-p` | 要搜索的目标目录路径 | 交互式输入 |
| `--pattern` | `-t` | 搜索文本或正则表达式 | 交互式输入 |
| `--output` | `-o` | 结果保存目录（非文件名） | 脚本所在目录下的 `search_results/` |
| `--no-regex` | — | 将 pattern 作为普通字符串（自动转义元字符） | 否（默认正则模式） |

### 结果文件位置

每次执行自动生成：
```
search_results/
  20260415_101252_Account_Main.txt
  20260415_110000_error.txt
```

## 执行流程

1. **收集参数**：从用户消息中提取目标目录和搜索关键词。
2. **运行脚本**：调用 `scripts/search_tool.py`，传入 `--path` 和 `--pattern`。
3. **展示结果**：
   - 告知用户结果文件路径。
   - 读取结果文件，汇总每个命中文件的匹配行数。
   - 如有特别关键的匹配内容，摘要呈现给用户。

## 依赖安装

脚本使用 Python 标准库，可选依赖：

```bash
pip install rarfile   # 支持 .rar 文件（还需系统安装 unrar）
pip install py7zr     # 支持 .7z 文件
```

RAR 所需系统工具：
- **Windows**：下载 unrar.exe → https://www.rarlab.com/rar_add.htm
- **macOS**：`brew install unrar`
- **Linux**：`sudo apt install unrar`

若用户未安装上述依赖，脚本会给出友好提示，ZIP/TAR 等格式不受影响仍可正常使用。

## 注意事项

- 不修改原始文件，只读。
- 解压到系统临时目录，搜索完成后自动清理。
- 防路径遍历攻击（对 ZIP/TAR 安全提取，拒绝含 `..` 的路径）。
- 对用户提供的 pattern，若不确定是否为正则，可加 `--no-regex` 参数安全处理。
