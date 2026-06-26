---
name: fastcp
version: 1.0.1
description: "Multi-target parallel file copy CLI. Reads source once into memory, writes to multiple USB drives concurrently. | 多目标并行复制工具，源文件只读一次，同时写入多个U盘。"
user_invocable: true
---

# FastCP - 多目标并行复制 / Multi-target Parallel Copy

将源目录一次性读入内存，并行复制到多个目标（U盘）。专为 AI 工具自动化调用设计。

Read source directory into memory once, copy to multiple targets (USB drives) in parallel. Designed for AI tool automation.

## 使用场景 / When to use
- 同一份文件同时复制到多个U盘 / Copy same files to multiple USB drives
- 批量部署文件到多个目标目录 / Batch deploy to multiple destinations
- 需要复制后校验完整性 / Copy with integrity verification

## 安装 / Install

从 GitHub Releases 下载或源码编译：

```bash
go install github.com/dongsheng123132/fastcp@latest
```

## 用法 / Usage

```bash
# 复制到多个U盘 / Copy to multiple USB drives
fastcp <source_dir> <target1> <target2> [target3] ...

# Windows 示例
fastcp.exe D:\源文件夹 E:\ F:\ G:\ H:\

# Linux/macOS 示例
fastcp /path/to/source /media/usb1 /media/usb2 /media/usb3

# 带校验 / With verification (xxhash)
fastcp --verify <source> <target1> <target2>

# 增量复制 / Incremental (skip unchanged)
fastcp --incremental <source> <target1>

# 控制并发数 / Control parallelism (default 3)
fastcp -c 2 <source> <target1> <target2> <target3>

# 预览模式 / Preview without copying
fastcp --dry-run <source> <target1> <target2>
```

## 参数 / Flags
- `-c, --concurrency N`: 同时写入目标数 / simultaneous target writes (default 3)
- `-b, --buffer-size`: 写缓冲区 / write buffer (default 4M)
- `--verify`: xxhash 校验 / integrity check after copy
- `--incremental`: 跳过未变更文件 / skip unchanged files
- `--dry-run`: 预览不复制 / preview only
- `--preload-all`: 强制全量预加载 / force all files into memory

## 典型流程 / Typical workflow
1. 确认U盘挂载盘符 / Identify mounted drives
2. 执行: `fastcp --verify D:\source E:\ F:\ G:\`
3. 检查校验结果 / Check verification output
