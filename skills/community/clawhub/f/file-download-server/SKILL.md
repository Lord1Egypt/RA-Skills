---
name: file-download-server
description: 快速搭建临时文件下载服务器，支持HTTP下载、美观的下载页面、防火墙端口自动开放。适用于需要向用户发送文件但聊天工具不支持直接文件传输的场景。触发词：下载服务器、文件下载、发送文件、搭建下载链接
---

# 文件下载服务器 (File Download Server)

快速搭建临时 HTTP 文件下载服务器，解决文件传输问题。

## 功能特性

- ✅ 一键启动 HTTP 服务器
- ✅ 自动生成美观的下载页面
- ✅ 自动开放防火墙端口
- ✅ 支持大文件下载
- ✅ 后台运行管理

## 快速开始

### 启动下载服务器

```bash
# 使用默认端口 4000
python3 {baseDir}/scripts/start_server.py /path/to/files

# 指定端口
python3 {baseDir}/scripts/start_server.py /path/to/files --port 8080

# 后台运行
python3 {baseDir}/scripts/start_server.py /path/to/files --daemon
```

### 生成下载页面

```bash
# 为单个文件生成下载页面
python3 {baseDir}/scripts/generate_index.py /path/to/file.pdf

# 为整个目录生成下载页面
python3 {baseDir}/scripts/generate_index.py /path/to/directory
```

### 开放防火墙端口

```bash
# 开放指定端口
python3 {baseDir}/scripts/open_port.py 4000

# 同时开放多个端口
python3 {baseDir}/scripts/open_port.py 4000 8080 9999
```

## 使用示例

### 示例 1: 发送论文 PDF

```python
# 1. 确保文件存在
pdf_path = "/root/.openclaw/workspace/papers/casting-defect-detection.pdf"

# 2. 生成下载页面
from scripts.generate_index import generate_download_page
generate_download_page(pdf_path, title="论文下载", description="这是一篇关于铸件缺陷检测的论文")

# 3. 启动服务器
from scripts.start_server import start_download_server
server = start_download_server(
    directory="/root/.openclaw/workspace/papers",
    port=4000,
    daemon=True
)

# 4. 给用户发送下载链接
print("📥 下载链接: http://your-server-ip:4000/")
```

### 示例 2: 批量文件分享

```bash
# 为整个项目目录创建下载服务
python3 {baseDir}/scripts/start_server.py /path/to/project --port 8080 --daemon

# 用户可以访问 http://your-ip:8080/ 浏览和下载所有文件
```

## 脚本说明

### scripts/start_server.py
启动文件下载服务器的主脚本。

**参数:**
- `directory`: 要分享的文件目录路径
- `--port PORT`: 服务器端口（默认: 4000）
- `--daemon`: 后台运行
- `--bind ADDRESS`: 绑定地址（默认: 0.0.0.0）

### scripts/generate_index.py
生成美观的下载页面。

**参数:**
- `path`: 文件或目录路径
- `--title TITLE`: 页面标题
- `--description DESC`: 页面描述
- `--output FILE`: 输出 HTML 文件路径

### scripts/open_port.py
开放防火墙端口。

**参数:**
- `ports`: 要开放的端口列表（可多个）

## 下载页面特性

生成的 HTML 下载页面包含：
- 🎨 现代化渐变设计
- 📄 文件信息展示（标题、描述、大小）
- ⬇️ 醒目的下载按钮
- 📱 响应式布局，支持手机访问
- 🔒 安全提示信息

## 服务管理

### 查看运行状态
```bash
# 查看 Python HTTP 服务器进程
ps aux | grep "python3 -m http.server"
```

### 停止服务器
```bash
# 查找并杀死进程
pkill -f "python3 -m http.server.*4000"
```

### 重启服务器
```bash
# 先停止，再启动
pkill -f "python3 -m http.server.*4000"
python3 {baseDir}/scripts/start_server.py /path/to/files --port 4000 --daemon
```

## 安全提示

⚠️ **重要安全注意事项:**

1. **临时使用**: 此服务器仅用于临时文件分享，不要长期运行
2. **端口安全**: 使用后及时关闭防火墙端口
3. **文件权限**: 确保只分享必要的文件
4. **访问控制**: 生产环境建议添加认证机制
5. **及时停止**: 文件下载完成后立即停止服务器

## 故障排除

### 问题：无法访问下载链接

**检查清单:**
1. 确认服务器正在运行: `ps aux | grep http.server`
2. 确认防火墙端口已开放: `iptables -L -n | grep 4000`
3. 确认云服务器安全组已放行该端口
4. 检查文件路径是否正确

### 问题：下载速度慢

**解决方案:**
- 使用更靠近用户的端口
- 压缩大文件后再分享
- 考虑使用专业的文件传输服务

### 问题：端口被占用

**解决方案:**
```bash
# 查找占用端口的进程
lsof -i :4000

# 杀死进程或换用其他端口
python3 {baseDir}/scripts/start_server.py /path/to/files --port 8080
```

## 高级用法

### 自定义下载页面

编辑 `assets/download_template.html` 来自定义页面样式。

### 支持的文件类型

下载页面会自动识别并适配：
- 📄 PDF 文档
- 📊 Excel/CSV 表格
- 🖼️ 图片文件 (PNG, JPG, GIF)
- 📦 压缩文件 (ZIP, RAR)
- 🎬 视频文件 (MP4, AVI)
- 📝 其他任意文件类型

### 多端口服务

可以同时启动多个服务器：
```bash
# 论文分享（端口 4000）
python3 {baseDir}/scripts/start_server.py /papers --port 4000 --daemon

# 数据分享（端口 8080）
python3 {baseDir}/scripts/start_server.py /data --port 8080 --daemon
```

## 参考资料

- Python http.server 文档: https://docs.python.org/3/library/http.server.html
- iptables 防火墙配置: https://netfilter.org/projects/iptables/
