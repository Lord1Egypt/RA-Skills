# 快速开始指南

## 30秒快速上手

### 最简单的用法

```bash
# 1. 进入技能目录
cd /path/to/skills/file-download-server

# 2. 生成下载页面
python3 scripts/generate_index.py /path/to/your/file.pdf --title "我的文件"

# 3. 启动服务器
python3 scripts/start_server.py /path/to/your/file --daemon

# 4. 完成！把链接发给用户
# 下载链接: http://your-server-ip:4000/
```

---

## 一步到位（推荐）

如果你已经有文件要分享，直接运行这个组合命令：

```bash
# 假设你的文件在 /data/files/ 目录
cd /data/files

# 生成下载页面 + 启动服务器（一行命令）
python3 /path/to/skills/file-download-server/scripts/generate_index.py . --title "文件分享" && \
python3 /path/to/skills/file-download-server/scripts/start_server.py . --port 8080 --daemon
```

---

## 常见场景

### 场景 1: 发送论文给用户

```python
from skills.file-download-server.scripts.generate_index import generate_download_page
from skills.file-download-server.scripts.start_server import start_download_server

# 生成页面
generate_download_page(
    "/papers/casting-defect.pdf",
    title="论文下载",
    description="关于铸件缺陷检测的研究论文"
)

# 启动服务器
server = start_download_server("/papers", port=4000, daemon=True)

# 给用户发送链接
print("📥 请访问: http://81.70.47.140:4000/")
```

### 场景 2: 批量文件分享

```bash
# 为整个项目目录创建下载服务
python3 scripts/generate_index.py /project --title "项目文件"
python3 scripts/start_server.py /project --port 8080 --daemon
```

### 场景 3: 临时快速分享

```bash
# 最简单，不需要生成页面，直接用 Python 内置服务器
cd /path/to/files
python3 -m http.server 4000 --bind 0.0.0.0 &

# 然后手动开放端口
iptables -I INPUT -p tcp --dport 4000 -j ACCEPT
```

---

## 停止服务器

```bash
# 查找并停止特定端口的服务器
pkill -f "http.server.*4000"

# 或者停止所有 Python HTTP 服务器
pkill -f "python3 -m http.server"
```

---

## 检查服务器状态

```bash
# 查看是否在运行
ps aux | grep "http.server"

# 查看端口监听
netstat -tlnp | grep 4000
# 或者
ss -tlnp | grep 4000
```

---

## 故障快速排查

| 问题 | 检查项 |
|------|--------|
| 打不开链接 | 1. 服务器在运行吗？ 2. 防火墙端口开了吗？ 3. 云服务器安全组配置了吗？ |
| 下载慢 | 换个端口试试，或者压缩文件 |
| 端口被占用 | 用 `lsof -i :4000` 查看，换端口或 kill 进程 |
| 404 错误 | 检查文件路径是否正确，index.html 是否在正确位置 |

---

## 需要帮助？

查看完整的 SKILL.md 文档了解更多高级功能！
