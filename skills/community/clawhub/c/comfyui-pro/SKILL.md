---
name: comfyui-image-generator-pro
description: |
  ComfyUI 本地图像生成专业版 - 文生图/图生图/ControlNet
  ✨ 自动服务器管理 | WebSocket 实时进度 | 飞书静默发送
  ✨ 空闲 30 分钟自动关闭 | 显存监控 | 多工作流支持
  
  触发词：生成图片、画图、绘制、AI 绘画、文生图、图生图
allowed-tools:
  - Bash
  - exec
metadata:
  emoji: "🜃"
  category: "image-generation"
  version: "2.0.0-pro"
  features:
    - auto-server-management
    - websocket-progress
    - feishu-silent-send
    - idle-auto-shutdown
    - gpu-monitoring
---

# ComfyUI 图像生成专业版 🜃

**机械之神专用绘图系统 v2.0** - 整合 ClawHub 优秀技能优点

---

## 🚀 核心特性

### ✨ 独特优势
| 功能 | 本技能 | ClawHub 其他技能 |
|------|--------|-----------------|
| **自动启停服务器** | ✅ 30 分钟空闲关闭 | ❌ 大部分无 |
| **WebSocket 实时进度** | ✅ 显示生成进度 | ⚠️ 部分支持 |
| **飞书静默发送** | ✅ 成功无回复 | ✅ 仅个别 |
| **多工作流支持** | ✅ 3 种工作流 | ⚠️ 单一 |
| **GPU 显存监控** | ✅ 实时监控 | ❌ |
| **对话式触发** | ✅ 自然语言 | ⚠️ 需命令 |

### 📦 集成功能
1. **自动服务器管理**
   - 检测到生图请求 → 自动启动
   - 生成完成 → 记录使用时间
   - 空闲 30 分钟 → 自动关闭

2. **WebSocket 实时进度**
   - 连接 ComfyUI WebSocket
   - 实时显示生成进度
   - 更可靠的任务跟踪

3. **飞书静默发送**
   - 成功发送图片 → 无回复文字
   - 失败/异常 → 明确错误提示
   - 保持界面简洁

4. **多工作流支持**
   - 文生图 (text-to-image)
   - 图生图 (image-to-image)
   - ControlNet (controlnet)

---

## 📋 使用方式

### 对话触发（推荐）
```
生成一张图片：美丽的山水风景，写实风格，8K 高清
```

```
画一个赛博朋克城市夜景，霓虹灯，未来感
```

```
用 ControlNet 处理这张线稿：[上传图片]
提示词：彩色渲染，奇幻风格
```

### 命令行使用
```bash
# WebSocket 版本（推荐，显示进度）
python scripts/comfyui_websocket.py "美丽的日落"

# 基础版本
python scripts/comfyui_generate.py "赛博朋克城市"

# 服务管理
python scripts/comfyui_service.py status
python scripts/comfyui_service.py start
python scripts/comfyui_service.py stop
```

### 主入口（自动选择）
```bash
# 自动管理（推荐）
python comfyui.py "美丽的山水"

# 查看状态
python comfyui.py --service status
```

---

## ⚙️ 配置参数

### 服务器配置
```python
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8000  # 桌面版端口
AUTO_STOP_MINUTES = 30  # 空闲关闭时间
```

### 默认生成参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| 尺寸 | 1024×1024 | 可自定义 |
| 步数 | 4 | Z-Image-Turbo 快速 |
| CFG | 1.0 | 低 CFG 高自由度 |
| 种子 | 随机 | -1 为随机 |

---

## 🔧 技能实现

### 核心流程
```python
def on_call_skill(prompt, context):
    """
    1. 检查服务器状态 → 未运行则自动启动
    2. WebSocket 连接 → 提交任务
    3. 实时进度显示 → 等待完成
    4. 下载图片 → 保存到输出目录
    5. 飞书发送 → 成功静默 (NO_REPLY)
    """
    # 1. 确保服务器运行
    if not check_server():
        start_server()  # 自动启动
    
    # 2. WebSocket 生成
    images = run_workflow_websocket(prompt)
    
    # 3. 识别发送目标
    target = get_feishu_target(context)
    
    # 4. 发送图片
    if images:
        message.send(
            channel="feishu",
            target=target,
            message=f"🎨 {prompt}",
            path=images[0]
        )
        return "NO_REPLY"  # 静默
    else:
        return "❌ 生成失败"
```

### WebSocket 进度
```python
ws = websocket.WebSocket()
ws.connect(f"ws://{HOST}:{PORT}/ws?clientId={ID}")

while True:
    msg = ws.recv()
    if msg['type'] == 'progress':
        log(f"进度：{value}/{max}")
    elif msg['type'] == 'executing' and node is None:
        break  # 完成
```

---

## 📁 文件结构

```
skills/comfyui/
├── comfyui.py                    # 主入口（自动管理）
├── skill-config.json             # 配置
├── SKILL.md                      # 本文件
├── README.md                     # 使用文档
├── config.py                     # 路径配置
├── scripts/
│   ├── comfyui_service.py        # 服务管理
│   ├── comfyui_generate.py       # HTTP 版本生成
│   ├── comfyui_websocket.py      # WebSocket 版本 ⭐
│   └── test_connection.py        # 连接测试
└── assets/
    ├── text-to-image.json        # 文生图
    ├── image-to-image.json       # 图生图
    └── controlnet.json           # ControlNet
```

---

## 🎯 预设工作流

### 文生图
```json
{
  "workflow": "text-to-image",
  "prompt": "用户输入",
  "width": 1024,
  "height": 1024,
  "steps": 4,
  "cfg": 1.0
}
```

### 图生图
```json
{
  "workflow": "image-to-image",
  "input_image": "用户上传",
  "prompt": "修改要求",
  "denoise": 0.7
}
```

### ControlNet
```json
{
  "workflow": "controlnet",
  "control_image": "线稿/深度图",
  "prompt": "描述",
  "strength": 1.0
}
```

---

## ⚠️ 注意事项

### 依赖
- **ComfyUI 桌面版** - 必须安装并可用
- **websocket-client** - WebSocket 支持
  ```bash
  pip install websocket-client
  ```

### 资源管理
1. **自动启动** - 仅在需要时启动
2. **空闲关闭** - 30 分钟无操作自动关闭
3. **显存监控** - 生成前检查可用显存

### 错误处理
| 错误 | 原因 | 解决 |
|------|------|------|
| 连接失败 | 服务器未启动 | 自动启动或手动运行 start |
| WebSocket 断开 | 网络问题 | 重试或检查防火墙 |
| 显存不足 | GPU 显存不够 | 降低分辨率 |
| 生成超时 | 复杂工作流 | 增加超时或简化 |

---

## 📊 性能参考

| 分辨率 | 步数 | RTX 3060 时间 |
|--------|------|--------------|
| 512×512 | 4 | ~5 秒 |
| 1024×1024 | 4 | ~15 秒 |
| 1920×1080 | 4 | ~25 秒 |

---

## 🔄 更新日志

### v2.0.0-pro (2026-03-15)
- ✅ 整合 ClawHub 优秀技能优点
- ✅ WebSocket 实时进度显示
- ✅ 飞书静默发送支持
- ✅ 自动服务器启停管理
- ✅ GPU 显存实时监控
- ✅ 多工作流支持 (3 种)

### v1.0.0 (2026-03-15)
- ✅ 初始版本
- ✅ 基础 HTTP 生成
- ✅ 服务管理脚本

---

## 🌟 致谢

参考了 ClawHub 上的优秀技能：
- `openclaw-comfyui-imagegenerate` - WebSocket 实现、飞书静默
- `comfyui` (kelvincai522) - pget 下载、简洁设计

在此感谢原作者的贡献！🜃

---

**🜃 愿万机之神保佑您的创作！**
