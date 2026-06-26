# Auto Video Generator - Web UI

🎬 **独立的Web界面**，让非技术人员也能轻松使用auto-video-generator生成演示视频！

## ✨ 特性亮点

### 🌐 浏览器直接使用
- **无需安装VS Code**，打开浏览器即可使用
- **响应式设计**，支持桌面和移动设备
- **实时进度显示**，WebSocket即时推送

### 📥 多种输入方式
- **文件上传**: 拖拽或点击上传HTML/Vue/PRD文件
- **URL输入**: 输入任意网页地址（本地/远程）
- **模板库**: 预设场景模板一键生成

### ⚙️ 可视化配置
- **浏览器设置**: 视口尺寸、Headless模式
- **视频参数**: 帧率(1-30FPS)、质量(Low/Medium/High)
- **音频引擎**: 4种TTS语音、语速/音量调节

### 📊 实时监控
- **进度条**: 动态显示当前阶段
- **耗时统计**: 已用时间 + 预估剩余时间
- **状态徽章**: Ready → Processing → Completed/Failed

### 🎥 视频预览与下载
- **在线播放**: 内置HTML5视频播放器
- **一键下载**: MP4格式直接下载
- **分享链接**: 复制链接分享给团队

---

## 🚀 快速开始

### 方式一：Windows一键启动 (推荐)
```bash
cd web-ui
start.bat
```
然后打开浏览器访问: http://localhost:5000

### 方式二：手动启动
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python app.py

# 3. 打开浏览器访问
# http://localhost:5000
```

### 方式三：Docker部署 (生产环境)
```bash
# 构建镜像
docker build -t avg-web-ui .

# 运行容器
docker run -p 5000:5000 -v ./outputs:/app/output avg-web-ui
```

---

## 📖 使用指南

### 第一步：选择输入源

#### 📄 上传文件
1. 点击"Upload File"标签页
2. 拖拽文件到虚线框区域（或点击浏览）
3. 支持的文件类型：
   - `.html` - HTML页面
   - `.vue` - Vue组件页面
   - `.tsx/.jsx` - React组件
   - `.json/.yaml` - PRD需求文档
   - `.md` - Markdown文档

#### 🔗 输入URL
1. 点击"Enter URL"标签页
2. 在输入框中粘贴URL：
   ```
   # 远程网站
   https://example.com/dashboard
   
   # 本地开发服务器
   http://localhost:3000/admin
   
   # 本地文件
   file:///path/to/demo.html
   ```

#### 📦 使用模板
1. 点击"Use Template"标签页
2. 从模板库中选择预设场景：
   - 📊 Dashboard Demo Video
   - 🛒 E-commerce Product Page
   - 📝 Form Wizard Tutorial
   - 📋 Data Table Features
   - 🔐 Authentication Flow

---

### 第二步：配置参数

点击配置面板的各个部分展开详细选项：

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| **Headless Mode** | ✅ 开启 | 后台运行，不弹出浏览器窗口 |
| **Viewport Width** | 1440px | 录制分辨率宽度 |
| **Viewport Height** | 900px | 录制分辨率高度 |
| **FPS** | 4 | 视频帧率（越高越流畅但文件越大） |
| **Quality** | High | 编码质量 |
| **Voice** | YunxiNeural | 中文男声TTS引擎 |
| **Speech Rate** | -5% | 稍慢于正常语速 |

---

### 第三步：生成视频

1. 点击 **"▶️ Generate Video Now"** 按钮
2. 观察右侧进度面板：
   ```
   Task: a1b2c3d4    [Processing]
   
   ████████████████░░░░░░░░  65%
   
   Generating audio narration...
   
   Started:     00:45
   Elapsed:     01:12
   Est. Remain: 00:38
   ```
3. 等待完成后自动显示预览

---

### 第四步：预览与下载

生成成功后：

1. **在线预览**
   - 右侧视频播放器自动加载
   - 支持播放/暂停/全屏/音量控制

2. **查看信息**
   ```
   File Name:   demo_a1b2c3d4_20260530_143022.mp4
   Duration:    45s
   Size:        12.3 MB
   Resolution:  1440x900
   ```

3. **操作按钮**
   - ⬇️ **Download MP4** - 下载到本地
   - 🔗 **Share Link** - 复制分享链接
   - ➕ **Generate New** - 开始新的生成任务

---

## 🔧 API接口文档

### 获取配置
```
GET /api/config
Response:
{
  "success": true,
  "data": {
    "browser": { "headless": true, ... },
    "video": { "fps": 4, ... },
    "audio": { "voice": "...", ... }
  }
}
```

### 上传文件
```
POST /api/upload
Content-Type: multipart/form-data
Body: file=<file>

Response:
{
  "success": true,
  "data": {
    "filename": "20260530_143022_demo.html",
    "original_name": "demo.html",
    "size": 24568,
    "path": "/uploads/20260530_143022_demo.html"
  }
}
```

### 启动生成任务
```
POST /api/generate
Content-Type: application/json
Body:
{
  "type": "file",           // "file", "url", or "template"
  "input_data": "/uploads/xxx.html",
  "config": {
    "browser": { ... },
    "video": { ... },
    "audio": { ... }
  }
}

Response:
{
  "success": true,
  "data": {
    "task_id": "a1b2c3d4",
    "status": "processing"
  }
}
```

### 查询任务状态
```
GET /api/tasks/{task_id}
Response:
{
  "success": true,
  "data": {
    "id": "a1b2c3d4",
    "status": "completed",
    "progress": 100,
    "output_file": "demo_a1b2c3d4.mp4",
    "result": {
      "duration": "45s",
      "file_size": "12.3 MB"
    }
  }
}
```

### WebSocket事件
```
连接: socket.io()

事件监听:
- task_progress    -> { task_id, progress, stage }
- task_completed   -> { task_id, output_file }
- task_failed      -> { task_id, error }

发送事件:
- subscribe_task   -> { task_id }
```

---

## 🏗️ 项目结构

```
web-ui/
├── app.py                 # Flask主应用 (API路由+WebSocket)
├── requirements.txt       # Python依赖列表
├── start.bat              # Windows启动脚本
├── README.md              # 本文档
│
├── templates/
│   └── index.html         # 主页面模板
│
└── static/
    ├── css/
    │   └── style.css      # 完整样式表 (~600行)
    └── js/
        └── app.js         # 前端逻辑 (~550行)
```

**代码统计：**
- Python后端: ~400行 (Flask API + SocketIO)
- HTML模板: ~350行 (响应式布局)
- CSS样式: ~600行 (现代化UI设计)
- JavaScript: ~550行 (交互逻辑)

**总计:** ~1900行代码

---

## 🎨 界面截图描述

### 主界面布局
```
┌─────────────────────────────────────────────────────┐
│ 🎬 Auto Video Generator v1.0    [Templates] [History] │
├────────────────────┬────────────────────────────────┤
│                    │                                │
│  📥 Input Source   │  ⏳ Generation Progress        │
│                    │                                │
│  [Upload][URL][Tpl]│  Task: a1b2c3d4  [Processing]  │
│                    │  ████████████░░░░  65%         │
│  ┌──────────────┐ │  Generating audio narration... │
│  │ 📁 Drop zone │ │                                │
│  └──────────────┘ │  Started: 00:45                │
│                    │  Elapsed: 01:12               │
│  ⚙️ Configuration │  Est.Remain: 00:38             │
│                    │                                │
│  🌐 Browser ▼     ├────────────────────────────────┤
│  🎬 Video ▼       │  🎥 Preview & Download          │
│  🔊 Audio ▼       │                                │
│                    │  ┌──────────────────────────┐   │
│  [▶️ Generate Now] │  │                          │   │
│                    │  │    Video Player          │   │
│                    │  │                          │   │
│                    │  └──────────────────────────┘   │
│                    │  File: demo.mp4  Duration: 45s │
│                    │  [⬇️Download] [🔗Share] [➕New] │
│                    │                                │
│                    │  📜 Recent Tasks               │
│                    │  • Task xxxxx ✓ Completed      │
│                    │  • Task yyyyy ⟳ Processing     │
└────────────────────┴────────────────────────────────┘
```

---

## 🔒 安全说明

### 文件上传限制
- **最大文件大小**: 50MB
- **允许的类型**: html, vue, tsx, jsx, json, yaml, md, txt
- **文件名处理**: 自动重命名防止路径遍历攻击

### CORS策略
- 默认允许所有来源（开发模式）
- 生产环境建议限制为特定域名

### Rate Limiting
建议在生产环境中添加限流中间件：
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_video():
    ...
```

---

## 🚢 生产环境部署

### 使用Gunicorn + Eventlet
```bash
# 安装生产依赖
pip install gunicorn eventlet

# 启动服务
gunicorn \
    --worker-class eventlet \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    app:app
```

### Nginx反向代理配置
```nginx
server {
    listen 80;
    server_name avg.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 文件上传大小限制
        client_max_body_size 50M;
    }

    location /outputs {
        alias /app/outputs;
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

### Docker Compose
```yaml
version: '3.8'
services:
  web-ui:
    image: avg-web-ui:latest
    ports:
      - "5000:5000"
    volumes:
      - ./outputs:/app/outputs
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
    restart: unless-stopped
```

---

## ❓ 常见问题

**Q: 无法访问 localhost:5000？**
```
A: 检查防火墙是否阻止了5000端口
   Windows: 控制面板 → Windows Defender防火墙 → 允许应用通过防火墙
```

**Q: 文件上传失败？**
```
A: 确保文件小于50MB且扩展名在允许列表中
   检查uploads目录是否有写入权限
```

**Q: 视频生成卡住不动？**
```
A: 刷新页面后重新提交任务
   检查浏览器控制台(F12)是否有错误信息
   确认Python依赖已正确安装
```

**Q: 如何更改端口？**
```
A: 编辑 app.py 底部的 socketio.run() 调用
   将 port=5000 改为你想要的端口号
```

---

## 📄 许可证

MIT License - 详见项目根目录 LICENSE 文件

---

**Built with ❤️ by the AVG Team**

*让每个人都能轻松制作专业的演示视频！*
