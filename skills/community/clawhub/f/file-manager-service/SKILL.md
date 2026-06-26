---
name: file-manager-service
description: 文件管理服务，支持服务启停、Web 界面浏览、文件上传下载和目录管理
---

# File Manager Service Skill

操作运行在 `http://127.0.0.1:8888` 的文件管理服务，管理用户家目录下的 `~/.openclaw/workspace/projects` 目录。

## 目录结构

```
file-manager-service/
├── SKILL.md                      # Skill 定义
├── README.md                     # 使用说明
├── _meta.json                    # 元数据
├── .gitignore                    # Git 忽略文件
└── scripts/
    ├── file_manager.py           # 客户端脚本（含服务管理）
    ├── server.py                 # Flask 服务端
    ├── templates/
    │   └── index.html            # Web 界面模板
    ├── .service.pid              # 服务进程 ID（运行时生成）
    └── .service.log              # 服务日志（运行时生成）
```

## 快速开始

### 服务管理

```bash
# 启动服务
python scripts/file_manager.py start

# 停止服务
python scripts/file_manager.py stop

# 重启服务
python scripts/file_manager.py restart

# 查看状态
python scripts/file_manager.py status

# 打开 Web 页面
python scripts/file_manager.py open
```

### 文件管理

```bash
# 列出文件
python scripts/file_manager.py list

# 列出指定目录
python scripts/file_manager.py list ai-agent-enterprise-design

# 查看文件内容
python scripts/file_manager.py cat path/to/file.md

# 搜索文件
python scripts/file_manager.py search 关键词

# 统计信息
python scripts/file_manager.py stats

# 创建目录（自动递归创建父目录）
python scripts/file_manager.py mkdir parent/path NewDirName

# 删除文件/目录
python scripts/file_manager.py delete path/to/item

# 移动文件/目录
python scripts/file_manager.py move source/path dest/path

# 获取/设置目录备注
python scripts/file_manager.py note directory-name
python scripts/file_manager.py note directory-name 备注内容

# 上传文件（支持多个文件）
python scripts/file_manager.py upload file1.md file2.py
python scripts/file_manager.py upload *.txt -p project/docs
```

### 直接调用 API

| 操作 | 端点 | 方法 |
|------|------|------|
| 列出文件 | `/api/files?path=xxx` | GET |
| 获取文件内容 | `/api/file/content?path=xxx` | GET |
| 保存文件 | `/api/file/save` | POST |
| 下载文件 | `/api/file/download?path=xxx` | GET |
| 删除 | `/api/delete` | POST |
| 移动 | `/api/move` | POST |
| 创建目录 | `/api/create/dir` | POST |
| 创建文件 | `/api/create/file` | POST |
| 搜索 | `/api/search?q=xxx&regex=true` | GET |
| 统计 | `/api/stats` | GET |
| 获取备注 | `/api/notes/get?path=xxx` | GET |
| 保存备注 | `/api/notes/save` | POST |
| 目录树 | `/api/tree?path=xxx` | GET |
| 下载目录 | `/api/download?path=xxx` | GET |
| **上传文件** | `/api/upload` | POST |
| **批量上传** | `/api/upload-folder` | POST |

## 使用示例

### 启动服务并打开页面

```bash
python scripts/file_manager.py start
python scripts/file_manager.py open
```

### 查看服务状态

```bash
python scripts/file_manager.py status
```

输出：
```json
{
  "running": true,
  "pid": 84078,
  "url": "http://127.0.0.1:8888",
  "service_dir": "/Users/lengyanhua/.openclaw/skills/file-manager-service/file-manager-service"
}
```

### 递归创建目录

```bash
# 自动创建 a/b/c 目录链
python scripts/file_manager.py mkdir a/b NewDir
```

### 创建文件到不存在的目录

```bash
# 自动创建父目录后创建文件
python scripts/file_manager.py mkdir x/y test.txt "文件内容"
```

## 支持的文件类型

**上传：** 不限制文件类型，支持任意格式（.pdf, .docx, .xlsx, .zip, 图片，视频等）

**在线查看/编辑：** `.txt`, `.md`, `.html`, `.py`, `.js`, `.json`, `.yaml`, `.yml`, `.css`, `.xml`, `.log`, `.sh`, `.bash`, `.sql`, `.java`, `.go`, `.rs`, `.ts`, `.jsx`, `.tsx`, `.htm`, `.svg`

**注意：** 非文本文件（如 PDF、图片）可上传和下载，但无法在线预览编辑

## 安全限制

- 所有路径必须在 `~/.openclaw/workspace/projects` 内
- 不能删除根目录
- 隐藏文件（以 `.` 开头）不显示
- 目录备注仅支持第一级子目录

## 故障排除

**服务启动失败**：检查 `scripts/.service.log` 日志文件

**端口被占用**：`lsof -ti :8888 | xargs kill -9` 然后重新启动

**路径非法**：确保路径在允许的根目录内

**文件类型不支持**：检查文件扩展名是否在允许列表中

**权限错误**：确认家目录可写（macOS 上不要使用 `/root` 路径）

## 特性

- ✅ 自动递归创建父目录
- ✅ 跨平台支持（macOS/Linux，自动检测家目录）
- ✅ Web 界面浏览和管理文件
- ✅ 目录备注功能
- ✅ 搜索文件和目录（支持正则表达式）
- ✅ 目录打包下载（ZIP）
- ✅ 移动文件/目录自动避免覆盖
- ✅ 现代化 UI 设计（Apple 风格，毛玻璃效果）
- ✅ 优化的删除/备注/移动确认对话框
