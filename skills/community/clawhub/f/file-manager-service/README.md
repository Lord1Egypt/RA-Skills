# File Manager Service

基于 Flask 的文件管理服务，提供 Web 界面和命令行工具来管理 `~/.openclaw/workspace/projects` 目录。

## 功能特性

- 📁 **文件浏览** - 可视化浏览目录结构和文件
- 📝 **文件编辑** - 查看和编辑多种文本格式文件
- 🔍 **搜索功能** - 快速查找文件和目录，支持正则表达式
- ➕ **创建文件/目录** - 支持递归创建父目录
- ⬆️ **文件上传** - 支持单文件和批量上传（Web 界面和命令行）
- 🗑️ **删除操作** - 安全删除文件和目录
- 📦 **打包下载** - 目录自动打包为 ZIP 下载
- 🏷️ **目录备注** - 为目录添加注释说明
- 🔒 **安全限制** - 所有操作限制在指定目录内
- 🎨 **友好界面** - 响应式设计，支持网格/列表视图切换

## 快速开始

### 安装依赖

```bash
pip install flask requests
```

### 启动服务

```bash
cd ~/.openclaw/skills/file-manager-service
python scripts/file_manager.py start
```

### 打开 Web 界面

```bash
python scripts/file_manager.py open
```

或直接访问：http://127.0.0.1:8888

### 停止服务

```bash
python scripts/file_manager.py stop
```

## 命令行用法

### 服务管理

```bash
python scripts/file_manager.py start      # 启动服务
python scripts/file_manager.py stop       # 停止服务
python scripts/file_manager.py restart    # 重启服务
python scripts/file_manager.py status     # 查看状态
python scripts/file_manager.py open       # 打开浏览器
```

### 文件操作

```bash
# 浏览
python scripts/file_manager.py list                     # 列出根目录
python scripts/file_manager.py list project-name        # 列出指定目录
python scripts/file_manager.py tree                     # 显示目录树

# 查看
python scripts/file_manager.py cat path/to/file.md      # 查看文件内容

# 搜索
python scripts/file_manager.py search README            # 搜索文件
python scripts/file_manager.py search ".*\.py$" --regex # 正则搜索

# 统计
python scripts/file_manager.py stats                    # 统计信息

# 创建（自动递归创建父目录）
python scripts/file_manager.py mkdir parent NewDir      # 创建目录
python scripts/file_manager.py mkdir path name content  # 创建文件

# 删除
python scripts/file_manager.py delete path/to/item      # 删除文件/目录

# 移动
python scripts/file_manager.py move source dest         # 移动文件/目录

# 备注
python scripts/file_manager.py note dir-name            # 获取备注
python scripts/file_manager.py note dir-name "备注内容"  # 设置备注

# 上传（支持多个文件）
python scripts/file_manager.py upload file1.md file2.py                    # 上传到当前目录
python scripts/file_manager.py upload *.txt -p project/docs                # 上传到指定目录
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/files` | GET | 列出目录内容 |
| `/api/file/content` | GET | 获取文件内容 |
| `/api/file/save` | POST | 保存文件 |
| `/api/file/download` | GET | 下载文件 |
| `/api/delete` | POST | 删除文件/目录 |
| `/api/create/dir` | POST | 创建目录 |
| `/api/create/file` | POST | 创建文件 |
| `/api/move` | POST | 移动文件/目录 |
| `/api/search?q=xxx&regex=true` | GET | 搜索文件（支持正则） |
| `/api/stats` | GET | 统计信息 |
| `/api/notes/get` | GET | 获取目录备注 |
| `/api/notes/save` | POST | 保存目录备注 |
| `/api/tree` | GET | 获取目录树 |
| `/api/download` | GET | 下载目录（ZIP） |
| `/api/upload` | POST | 上传单个文件 |
| `/api/upload-folder` | POST | 批量上传多个文件 |

## 目录结构

```
file-manager-service/
├── SKILL.md                      # OpenClaw Skill 定义
├── README.md                     # 本文档
├── _meta.json                    # 元数据
├── .gitignore                    # Git 忽略文件
└── scripts/
    ├── file_manager.py           # 客户端脚本（服务管理 + CLI）
    ├── server.py                 # Flask 服务端
    ├── templates/
    │   └── index.html            # Web 界面模板
    ├── .service.pid              # 服务进程 ID（运行时）
    └── .service.log              # 服务日志（运行时）
```

## 配置

### 修改端口

编辑 `file-manager-service/app.py`：

```python
app.run(host='0.0.0.0', port=9999, debug=False)  # 修改端口
```

编辑 `scripts/file_manager.py`：

```python
BASE_URL = "http://127.0.0.1:9999"  # 同步修改
```

### 修改管理目录

编辑 `file-manager-service/app.py`：

```python
BASE_DIR = Path('/your/custom/path')  # 修改管理的目录
```

## 支持的文件类型

**上传：** 不限制文件类型，支持任意格式（PDF、Word、Excel、图片、视频、压缩包等）

**在线查看/编辑：** `.txt`, `.md`, `.html`, `.py`, `.js`, `.json`, `.yaml`, `.yml`, `.css`, `.xml`, `.log`, `.sh`, `.bash`, `.sql`, `.java`, `.go`, `.rs`, `.ts`, `.jsx`, `.tsx`, `.htm`, `.svg`

**注意：** 非文本文件可上传下载，但无法在线预览

## 安全说明

- 所有操作限制在 `BASE_DIR` 目录内
- 无法删除根目录
- 隐藏文件（`.` 开头）不显示
- 目录备注仅支持第一级子目录

## 故障排除

### 服务启动失败

查看日志：
```bash
cat scripts/.service.log
```

### 端口被占用

```bash
lsof -ti :8888 | xargs kill -9
python scripts/file_manager.py restart
```

### 权限错误

确认家目录可写：
```bash
ls -la ~ | grep .openclaw
```

macOS 用户注意：不要使用 `/root` 路径，应使用 `~` 或 `/Users/用户名`

## 作为 OpenClaw Skill 使用

将此目录复制到 OpenClaw skills 目录：

```bash
cp -r file-manager-service ~/.openclaw/skills/
```

然后在 OpenClaw 中直接使用自然语言命令：
- "启动文件管理服务"
- "打开文件管理页面"
- "列出 projects 目录"
- "搜索 README 文件"
- "创建目录 ai-agent"

## 版本

- **1.0.0** - 初始版本
- **1.1.0** - 添加递归创建父目录、跨平台支持
- **1.1.1** - 修复 macOS 上停止服务功能（跨平台 PID 查找支持）
- **1.1.2** - UI 布局优化（紧凑设计）、搜索支持正则表达式
- **1.1.3** - 现代化 UI 重构（Apple 风格）、删除/备注/移动模态框优化

## 许可证

MIT
