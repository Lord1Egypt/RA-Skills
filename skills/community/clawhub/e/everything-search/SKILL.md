---
name: everything-search
description: "Everything Windows 文件搜索技能 — HTTP API 快速搜索、中英文模糊匹配、文件类型过滤"
version: "1.0.0"
author: Steve-Shi-Web
license: MIT
keywords: ["files", "search", "windows", "everything", "productivity"]
---

# Everything Search 技能说明

## 📋 技能概述

通过 Everything HTTP Server API 实现快速文件搜索功能。支持中文/英文搜索、模糊匹配、文件类型过滤。

---

## 🔧 配置步骤

### 1. 安装 Everything

- 下载地址：https://www.voidtools.com/
- 安装路径：`D:\Program Files\Everything\`

### 2. 启用 HTTP 服务器

**⚠️ 关键步骤 - 必须手动操作：**

1. 打开 Everything 窗口
2. 按 **Ctrl+P** 打开选项（或 Tools → Options）
3. 点击左侧 **"HTTP Server"**
4. **勾选** `☑ Enable HTTP server`
5. 设置端口：`2853`
6. 点击 **OK** 保存

### 3. 验证配置

```bash
# 测试 HTTP 服务器是否运行
python -c "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:2853/', timeout=5); print('OK:', r.status)"
```

---

## ⚠️ 注意事项

### 1. HTTP 服务器必须手动启用

**问题：** 配置文件不会自动启用 HTTP 服务器

**原因：** Everything 的安全设计，必须在 GUI 界面中手动勾选

**解决方案：**
- 必须在 Everything 窗口中按 Ctrl+P → HTTP Server → 勾选启用
- 仅修改配置文件 `Everything.ini` 不会生效

### 2. 服务实例 vs 用户实例

**问题：** 有时有两个 Everything 进程运行，其中一个可能不读取用户配置

**症状：** 
- 配置已保存但 HTTP 服务器不响应
- 端口未被监听

**解决方案：**
1. 完全退出 Everything（系统托盘右键 → Exit）
2. 重新启动 Everything
3. 再次确认 HTTP Server 已勾选

### 3. 配置生效需要重启

**问题：** 修改配置后 HTTP 服务器未立即响应

**解决方案：**
- 修改配置后完全退出并重启 Everything
- 等待 3-5 秒让服务完全启动

### 4. 端口占用检查

**问题：** 端口 2853 无法连接

**诊断方法：**
```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 2853))
if result == 0:
    print("端口开放")
else:
    print("端口关闭")
```

### 5. API 端点格式

**正确的 API 格式：**
```
http://127.0.0.1:2853/?search=关键词&json=1&maxresults=20
```

**错误的 API 格式（会导致 404）：**
```
http://127.0.0.1:2853/everything/?search=关键词&json=1
http://127.0.0.1:2853/api/search?query=关键词&json=1
```

---

## 🐛 今天遇到的问题及解决方案

### 问题 1：HTTP 服务器无法连接

**症状：**
```
✗ Connection failed: [WinError 10061] 由于目标计算机积极拒绝，无法连接
```

**排查过程：**
1. ✓ 确认 Everything 进程在运行（tasklist 检测到 2 个实例）
2. ✓ 配置文件已正确写入 `Everything.ini`
3. ✗ 端口 2853 未被监听（netstat 检查）
4. ✗ 多个常用端口测试（80, 8080, 8081, 8082）均无响应

**根本原因：**
- 配置文件中的 `enabled=1` 不会自动启用 HTTP 服务器
- 必须在 GUI 界面中手动勾选复选框

**解决方案：**
1. 打开 Everything 窗口
2. Ctrl+P → HTTP Server
3. 确认 `☑ Enable HTTP server` 已勾选
4. 点击 OK
5. 完全退出并重启 Everything

**验证命令：**
```python
python /workspace/check-port.py
# 输出：✓ Port 2853 is OPEN and listening!
```

---

### 问题 2：API 返回 404

**症状：**
```
✗ Search failed: HTTP Error 404: Not Found
```

**排查过程：**
1. ✓ HTTP 服务器已启动（端口 2853 可连接）
2. ✓ 根路径 `/` 返回正常 HTML
3. ✗ `/everything/?search=test` 返回 404
4. ✗ `/api/search?query=test` 返回 404
5. ✓ `/?search=test&json=1` 返回正常 JSON

**根本原因：**
- Everything HTTP API 的端点是根路径 `/`，不是 `/everything/`

**解决方案：**
使用正确的 API 格式：
```
http://127.0.0.1:2853/?search=关键词&json=1&maxresults=20
```

---

### 问题 3：文件大小显示为 0

**症状：**
- 搜索结果中所有文件大小都显示为 `0 B`

**原因：**
- Everything 默认不返回文件大小信息
- 需要在 API 请求中添加参数

**解决方案：**
在 API URL 中添加 `&size=1` 参数：
```
http://127.0.0.1:2853/?search=关键词&json=1&size=1&maxresults=20
```

---

### 问题 4：中文搜索乱码

**症状：**
- 搜索中文关键词返回空结果或错误

**原因：**
- URL 中的中文需要 URL 编码

**解决方案：**
使用 `urllib.parse.quote()` 编码中文：
```python
import urllib.parse
keyword = "数据资产"
encoded = urllib.parse.quote(keyword)
url = f"http://127.0.0.1:2853/?search={encoded}&json=1"
```

---

## 📝 使用示例

### Python 搜索脚本

```python
#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

PORT = 2853
KEYWORD = "数据资产"

# 编码关键词
encoded = urllib.parse.quote(KEYWORD)
url = f"http://127.0.0.1:{PORT}/?search={encoded}&json=1&maxresults=20"

# 发送请求
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')

with urllib.request.urlopen(req, timeout=10) as response:
    data = json.loads(response.read().decode())
    
    total = data.get("totalResults", 0)
    results = data.get("results", [])
    
    print(f"找到 {total} 个结果")
    
    for item in results[:10]:
        name = item.get("name", "Unknown")
        path = item.get("path", "")
        full_path = f"{path}\\{name}" if path else name
        print(f"  - {full_path}")
```

### 搜索图片文件

```python
# 搜索特定类型的文件
keywords = [
    "张三 jpg",      # 搜索 JPG 照片
    "张三 png",      # 搜索 PNG 图片
    "数据资产 xlsx",   # 搜索 Excel 文件
    "报告 pdf",        # 搜索 PDF 文档
]

for keyword in keywords:
    encoded = urllib.parse.quote(keyword)
    url = f"http://127.0.0.1:2853/?search={encoded}&json=1&maxresults=10"
    # ... 处理结果
```

---

## 🔍 高级搜索语法

### 文件类型过滤

```
# 只搜索文件（不包括文件夹）
关键词 file:

# 只搜索文件夹
关键词 folder:

# 搜索特定扩展名
关键词 ext:jpg
关键词 ext:png
```

### 路径过滤

```
# 在特定路径中搜索
关键词 path:"D:\Documents"

# 排除特定路径
关键词 !path:"C:\Windows"
```

### 大小过滤

```
# 大于 1MB 的文件
关键词 size:>1mb

# 小于 100KB 的文件
关键词 size:<100kb
```

### 日期过滤

```
# 今天修改的文件
关键词 dm:today

# 本周修改的文件
关键词 dm:thisweek

# 特定日期之后修改的文件
关键词 dm:>2024-01-01
```

---

## 🛠️ 诊断工具

### 检查端口状态

```python
# check-port.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
result = sock.connect_ex(('127.0.0.1', 2853))

if result == 0:
    print("✓ Port 2853 is OPEN")
else:
    print("✗ Port 2853 is CLOSED")
```

### 测试 API 端点

```python
# test-api.py
import urllib.request

endpoints = [
    "/",
    "/?search=test&json=1",
    "/version",
]

for endpoint in endpoints:
    url = f"http://127.0.0.1:2853{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            print(f"✓ {endpoint} - {r.status}")
    except Exception as e:
        print(f"✗ {endpoint} - {e}")
```

---

## 📚 参考资料

- Everything 官方文档：https://www.voidtools.com/support/everything/
- HTTP Server 配置：https://www.voidtools.com/support/everything/http_server/
- 搜索语法：https://www.voidtools.com/support/everything/search_commands/

---

## 📅 更新日志

### 2026-04-02
- ✅ 批量替换敏感人名"史周平"为"张三"（共 14 处）
- ✅ 更新 badges 为现代 flat-square 样式
- ✅ 设置仓库为公开可见
- ✅ 更新联系方式：问题反馈由 GitHub Issues 更改为 441457345@qq.com

### 2024-04-02
- ✅ 完成 Everything HTTP Server 配置
- ✅ 解决 HTTP 服务器无法连接问题（需手动勾选启用）
- ✅ 解决 API 404 错误（使用正确的端点格式）
- ✅ 测试中文搜索功能
- ✅ 创建诊断工具和测试脚本

---

## 🎯 快速检查清单

配置 Everything 后，按此清单检查：

- [ ] Everything 正在运行
- [ ] HTTP Server 已勾选启用（Ctrl+P → HTTP Server → ☑ Enable）
- [ ] 端口设置为 2853
- [ ] 完全退出并重启了 Everything
- [ ] 端口 2853 可连接（运行 check-port.py 验证）
- [ ] API 返回正常 JSON（运行 test-api.py 验证）
- [ ] 中文搜索正常工作

---

**最后更新：** 2026-04-02  
**作者：** nanobot  
**版本：** 1.0
