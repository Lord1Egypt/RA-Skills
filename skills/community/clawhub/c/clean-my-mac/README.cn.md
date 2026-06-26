# cleanMyMacSkill (中文文档)

[English](README.en.md) | 简体中文

---

一个轻量级、高性能、只读存储分析与清理助手。它能为 macOS、Windows 和 Linux 系统生成类似 CleanMyMac 的精美交互式 HTML 报告，并提供安全的本地 Web 服务以支持网页端一键移至垃圾桶或直接删除。

该项目专为 AI Agent（如 Claude Code, Gemini 等）设计，不仅能单独运行，还可以作为 AI 智能助手的扩展技能（Agent Skill），协助分析复杂的系统路径与垃圾占用。

---

## 功能特性

- **多平台原生支持 (macOS, Windows, Linux)**：自动识别当前操作系统并扫描相应路径。支持用户主目录、下载夹、临时缓存、系统日志、以及各类开发者缓存（pip, uv, npm, cargo, yarn, go, bun, gradle, docker, WSL 镜像等）。
- **高性能多线程并发扫描**：利用 Python 标准库的 `ThreadPoolExecutor` 并行评估各目录，配合智能路径排除机制（如在扫描主目录时自动跳过 Library 缓存，由专门的分类任务独立并行计算），规避重复遍历，使大型磁盘扫描在数十秒内闪电完成。
- **CleanMyMac 拟物风格仪表盘**：采用 Apple 设计规范的毛玻璃卡片（Glassmorphic）、窄高亮边框和弹性动效。顶部配备交互式环形进度表，支持 localStorage 自动记忆的深色与浅色模式切换，并支持中英文语言热切换。
- **安全删除三级护栏**：
  - 🟢 **建议自动清理 (Green)**：纯缓存、开发构建残留。支持网页端一键移入废纸篓或彻底删除。
  - 🟡 **建议手动审核 (Yellow)**：微信聊天记录、下载文件、Docker VM 镜像等。提供“在文件管理器中显示”或“仅移入废纸篓安全子目录”。
  - 🔴 **谨慎清理 (Red)**：应用本体二进制。提供 Apple 官方标准卸载指导，不支持网页后台直接删除，确保系统稳定。
- **完备的安全机制**：本地 Web 服务使用随机 Session Token 校验、Host 头防重绑定保护、双重物理路径安全范围检查，防止任意越界删除。

---

## 项目结构

```text
cleanMyMacSkill/
├── SKILL.md                 # 智能助手技能元数据定义
├── README.md                # 语言选择导航入口
├── README.cn.md             # 中文说明文档（本文件）
├── README.en.md             # 英文说明文档
├── assets/
│   └── report_template.html # 苹果交互风格双语 HTML 模板
├── references/              # 各平台存储布局参考指南
│   ├── macos.md
│   ├── windows.md
│   └── linux.md
└── scripts/
    ├── scan.py              # 多线程并发扫描脚本
    ├── build_report.py      # 静态报告编译器
    └── server.py            # 本地一键清理交互服务器
```

---

## 快速开始

本项目零外部依赖，仅需 **Python 3 标准库** 环境。

### 步骤 1：扫描磁盘占用
扫描磁盘并将元数据输出为 JSON 格式：
```bash
python3 scripts/scan.py > /tmp/cleanmymac_scan.json
```

### 步骤 2：生成静态报告
编译为独立的 HTML 报告（出于浏览器沙盒限制，静态模式下网页上的删除/定位按钮将不可点击）：
```bash
python3 scripts/build_report.py /tmp/cleanmymac_scan.json ~/Desktop/cleanmymac-report.html
```

### 步骤 3：启动一键清理网页服务（推荐）
启动本地服务器。这将在浏览器中自动打开精美的交互仪表盘，您可以在网页上流畅进行一键删除、移入废纸篓或在系统 Finder/资源管理器中高亮定位文件夹：
```bash
python3 scripts/server.py /tmp/cleanmymac_scan.json
```

---

## Linux 垃圾桶规范说明

在 Linux 系统上，清理后端完全遵循 **Freedesktop 垃圾桶规范**。当您在网页点击“移到废纸篓”时，文件会被安全移动到 `~/.local/share/Trash/files/`，且在 `~/.local/share/Trash/info/` 中自动写入带有删除时间及原始绝对路径的 `.trashinfo` 文件。这使得 GNOME Files (Nautilus) 或 KDE Dolphin 等系统管理器能够原生感知废纸篓内容，并支持直接右键还原。

---

## 反馈与技术支持
由 **TKHubs** 团队设计与维护。
有任何问题或功能建议，欢迎联系官方支持：[support@tkhubs.com](mailto:support@tkhubs.com)。
