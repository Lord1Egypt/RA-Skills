---
name: art-knowledge-helper
description: 艺术知识库管理技能包。用于维护藏书整理、散文件清理、百度网盘同步、新书归档、藏书统计等日常管理工作。配合 art-tutor 技能使用。首次使用前请在 config.json 中填写知识库路径。
tags: [art, knowledge-base, management]
version: 1.1.0
---

# 🎨 艺术知识库 · 管理助手

本技能用于维护艺术知识库藏书，支持：扫描下载目录归档新书、清理 EPUB 散文件、百度网盘双向同步、藏书量统计、生成藏书清单。

---

## ⚙️ 首次配置（必须）

**编辑 `config.json`**，填写你自己的路径：

```json
{
  "knowledge_base_path": "D:\\艺术知识库",
  "baidu_path": "D:\\BaiduSyncdisk\\小艺\\艺术知识库",
  "downloads_path": "C:\\Users\\你的用户名\\Downloads"
}
```

> **三个路径均可自定义**。只需改 `config.json`，所有脚本自动读取，无需修改脚本。

---

## 功能概览

| 脚本 | 功能 |
|------|------|
| `scan_downloads.py` | 扫描下载目录近30天内艺术类书籍 |
| `archive_books.py` | 将下载的新书归档到知识库对应分类 |
| `kb_stats.py` | 统计藏书总量、各分类数量、总大小 |
| `sync_to_baidu.py` | 双向同步本地与百度盘 |
| `verify_sync.py` | 验证两边是否完全一致 |

---

## 快速开始

### 1. 安装

下载本技能包，解压到 OpenClaw 工作目录：

```
skills/art-knowledge-helper/
├── SKILL.md
├── config.json        ← 【首次必填】路径配置
├── SOUL.md
├── USER.md
├── README_SKILL.md
├── SHARE_GUIDE.md
├── FRIEND_TUTORIAL.md
└── scripts/
    ├── scan_downloads.py
    ├── archive_books.py
    ├── kb_stats.py
    ├── sync_to_baidu.py
    └── verify_sync.py
```

### 2. 配置路径

编辑 `config.json`（见上方）。

### 3. 扫描新书

```powershell
python scripts/scan_downloads.py
```

### 4. 归档新书

```powershell
python scripts/archive_books.py
```

### 5. 统计藏书

```powershell
python scripts/kb_stats.py
```

### 6. 同步百度盘

```powershell
python scripts/sync_to_baidu.py
```

### 7. 验证同步

```powershell
python scripts/verify_sync.py
```

---

## 目录结构说明

```
skills/
├── art-tutor/              ← 艺术学习助手（推荐藏书、规划路径）
│   └── references/
│       ├── corpus.md
│       └── learning_paths.md

└── art-knowledge-helper/   ← 知识库管理（藏书整理、同步、归档）
    ├── config.json          ← 【必填】路径配置
    ├── scripts/             ← 管理脚本（自动读 config.json）
    ├── SOUL.md
    ├── USER.md
    └── README_SKILL.md
```

---

## 依赖

- Python 3
- PowerShell 5+（Windows）

---

## 更新日志

- **v1.1.0**（2026-04-22）：路径配置从硬编码改为 `config.json`，所有脚本统一读取，路径完全自定义。
- **v1.0.0**（2026-04-22）：初始版本，包含5个管理脚本和完整文档。
