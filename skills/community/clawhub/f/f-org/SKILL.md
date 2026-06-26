---
name: file-organizer
description: |
  自动文件归档与整理技能。当需要整理工作空间文件、创建新文件需要决定存放位置、
  从外部获取文件（下载、复制、接收）需要归档、或发现目录混乱需要整理时触发。
  用于保持工作空间目录整洁清爽，分类分级存放文件。不用于已结构化的项目目录。
---

# File Organizer - 文件自动归档技能

## 核心原则

1. **原有openclaw文件目录不动**：SOUL.md、USER.md、AGENTS.md、HEARTBEAT.md、MEMORY.md、TOOLS.md、skills/、memory/等 OpenClaw 原生文件和目录保持不变
2. **新增文件集中存放**：所有我创建、生成、下载、复制的新文件放入 `user/` 目录
3. **分类分级**：`user/` 下按文件性质子类分类

## 目录结构规范

```
workspace/
├── user/                  # 【新增】所有非Openclaw原生的文件集中存放
│   ├── docs/              # 文档资料
│   ├── scripts/           # 脚本工具
│   ├── archives/          # 归档文件
│   ├── downloads/          # 临时下载
│   ├── temp/              # 临时文件
│   └── [其他]/            # 按需创建
├── (OpenClaw原生保持不变)
│   ├── skills/
│   ├── memory/
│   ├── tools/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── USER.md
│   ├── HEARTBEAT.md
│   ├── MEMORY.md
│   └── TOOLS.md
```

## 触发场景

| 场景 | 操作 |
|------|------|
| 创建新文件 | 默认放 user/ 对应子类，无合适则创建 |
| 下载文件 | 先放 user/downloads/，后续归档 |
| 复制/接收文件 | 识别性质，归入 user/ 相应目录 |
| 发现零散文件 | 移动到 user/ 相应目录 |
| 备份/还原 | user/ 目录可单独备份 |

## 文件识别规则

### 文档类
- `.md`, `.txt`, `.pdf`, `.doc(x)` → `user/docs/`
- 方案/报告 → `user/docs/reports/`

### 代码/脚本
- 脚本 `.sh`, `.py` → `user/scripts/`
- 项目代码 → `user/projects/项目名/`

### 媒体类
- 照片/截图 → `user/media/photos/`
- 视频 → `user/media/videos/`

### 压缩包
- 临时 → `user/downloads/` 或 `user/archives/`

## 禁止操作

- ❌ 移动/修改 OpenClaw 原生文件（SOUL.md、skills/ 等）
- ❌ 移动结构化项目目录
- ❌ 删除他人创建的系统文件

## 示例

```
# 创建了新文档
→ user/docs/项目名/

# 下载了文件
→ user/downloads/ → 后续归档到 user/archives/

# 收到压缩包
→ user/archives/
```
