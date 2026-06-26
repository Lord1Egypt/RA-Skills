# 快手/B 站/抖音视频发布技能

## 🎯 技能概述

参考小红书发布技能（xiaohongshu-skills）的结构，为快手、B 站、抖音三个平台提供视频发布自动化能力。

**目标平台：**
- 快手：https://cp.kuaishou.com/
- B 站：https://member.bilibili.com/platform/upload/video/frame
- 抖音：https://creator.douyin.com/creator-micro/content/upload

---

## 📝 2026-04-03 更新

### 快手平台特殊规则

**关键词格式：**
- 快手最多支持 **4 个关键词**
- 每个关键词前加 `#`，后加空格
- 示例：`#美好的 #欢快 #一天的`

**封面上传流程：**
1. 点击「封面设置」按钮
2. 切换到「上传封面」标签
3. 点击「上传图片」按钮选择文件
4. 点击「确认」应用封面

**作品描述框：**
- 标题和关键词写在同一个描述框中
- 格式：`标题 #关键词 1 #关键词 2 #关键词 3 #关键词 4`

---

## 🔒 技能边界（强制）

**所有发布操作只能通过浏览器自动化脚本完成：**

- **唯一执行方式**：运行 `python scripts/cli.py <子命令>` 控制 Chrome 浏览器
- **禁止外部工具**：不得调用第三方 API、MCP 工具或其他实现
- **必须先有运行中的 Chrome**，且用户已登录对应平台

---

## 📋 前置检查

### 登录状态检查

```bash
# 打开对应平台，手动检查登录状态
python scripts/cli.py --platform kuaishou check-login
python scripts/cli.py --platform bilibili check-login
python scripts/cli.py --platform douyin check-login
```

- 未登录时提示用户扫码登录
- 支持 `--headless` 模式（未登录自动降级到有窗口模式）

---

## 📥 输入格式

### TXT 配置文件格式

```text
标题：明天更好
视频数据路径：/Users/xiaohei/.openclaw/workspace/skills/app_publish/test_data/test_video.mp4
封面：/Users/xiaohei/.openclaw/workspace/skills/app_publish/test_data/image.png
关键词：美好的，欢快，一天的
```

**字段说明：**
- **标题**：视频标题（必填）
- **视频数据路径**：视频文件绝对路径（必填）
- **封面**：封面图片绝对路径（可选）
- **关键词**：逗号或空格分隔的关键词/标签（可选）

---

## 🚀 发布流程

### 流程 A: 单平台发布

#### 快手发布

```bash
cd /Users/xiaohei/.openclaw/workspace/skills/app_publish/scripts

# 完整发布（填写 + 点击发布）
python cli.py publish-kuaishou --config ../test_data/描述.txt

# 只填写表单，不发布（用于预览确认）
python cli.py publish-kuaishou --config ../test_data/描述.txt --no-publish

# 指定等待超时时间（秒）
python cli.py publish-kuaishou --config ../test_data/描述.txt --wait-timeout 600
```

#### B 站发布

```bash
# 完整发布
python cli.py publish-bilibili --config ../test_data/描述.txt

# 分步发布
python cli.py publish-bilibili --config ../test_data/描述.txt --no-publish
# 在浏览器中确认预览后，手动点击发布
```

#### 抖音发布

```bash
# 完整发布
python cli.py publish-douyin --config ../test_data/描述.txt

# 指定 Chrome 端口
python cli.py publish-douyin --config ../test_data/描述.txt --port 9222
```

---

### 流程 B: 多平台一键发布

```bash
# 依次发布到快手、B 站、抖音
python cli.py publish-all --config ../test_data/描述.txt

# 带超时设置
python cli.py publish-all --config ../test_data/描述.txt --wait-timeout 300
```

**注意：** `publish-all` 会在同一浏览器会话中依次执行三个平台的发布，总耗时可能较长（每个平台约 1-3 分钟）。

---

## 🛠️ 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--config path` | TXT 配置文件路径（必须） | - |
| `--wait-timeout seconds` | 上传等待超时时间 | 300 |
| `--no-publish` | 只填写表单，不点击发布 | false |
| `--port PORT` | Chrome CDP 端口 | 9222 |
| `--host HOST` | Chrome CDP 主机 | 127.0.0.1 |
| `--headless` | 无头模式 | false |
| `--user-data-dir path` | Chrome 用户数据目录 | `~/.kbs/chrome-profile` |

---

## 📤 输出格式

### 成功输出

```json
{
  "success": true,
  "platform": "bilibili",
  "title": "明天更好",
  "video_path": "/path/to/video.mp4",
  "cover_path": "/path/to/cover.png",
  "keywords": ["美好的", "欢快", "一天的"],
  "status": "发布完成",
  "message": "视频上传成功，表单已填写"
}
```

### 失败输出

```json
{
  "success": false,
  "platform": "kuaishou",
  "error": "上传超时，请检查网络连接或视频文件大小",
  "status": "上传失败"
}
```

---

## ⚠️ 失败处理

| 错误类型 | 可能原因 | 解决方案 |
|---------|---------|---------|
| **上传超时** | 视频文件过大、网络慢 | 增加 `--wait-timeout` 参数 |
| **登录失效** | Cookie 过期 | 重新登录对应平台 |
| **选择器失效** | 页面结构变更 | 更新 `selectors_*.py` 中的 CSS 选择器 |
| **文件不存在** | 路径错误 | 检查 TXT 配置中的文件路径 |
| **Chrome 未启动** | 调试端口未开放 | 确保 Chrome 以 `--remote-debugging-port=9222` 启动 |

---

## 📁 项目结构

```
app_publish/
├── scripts/
│   ├── cli.py                     # CLI 入口（6.8KB）
│   ├── chrome_launcher.py         # Chrome 启动器（9KB）
│   ├── requirements.txt           # Python 依赖
│   └── kbs/                       # 核心模块
│       ├── __init__.py
│       ├── cdp.py                 # CDP 封装（22KB）
│       ├── types.py               # 数据类型 + 配置解析（4KB）
│       ├── selectors_ks.py        # 快手选择器（1.5KB）
│       ├── selectors_bili.py      # B 站选择器（1.1KB）
│       ├── selectors_dy.py        # 抖音选择器（859B）
│       ├── publish_kuaishou.py    # 快手发布逻辑（4.5KB）
│       ├── publish_bilibili.py    # B 站发布逻辑（4KB）
│       └── publish_douyin.py      # 抖音发布逻辑（4.5KB）
├── test_data/
│   ├── test_video.mp4             # 测试视频
│   ├── image.png                  # 测试封面
│   └── 描述.txt                   # 测试配置
├── 任务.md                        # 任务需求文档
└── SKILL.md                       # 技能说明文档（本文件）
```

---

## 🎯 实现状态

✅ 已完成：
- CLI 入口和参数解析
- Chrome 连接和会话管理
- 三平台选择器定义
- 视频上传（使用 CDP DOM.setFileInputFiles）
- 封面上传
- 标题/关键词填写
- 上传状态轮询（最多 5 分钟）
- 单平台/多平台发布模式

⚠️ 待完善：
- 实际页面选择器需要验证（不同时间页面结构可能变化）
- 视频上传进度监控需要实际测试优化
- 分区选择功能（B 站）需要实现
- 定时发布功能需要实现
- 封面上传功能需要实际测试

---

## 📝 注意事项

1. **CSS 选择器**：基于常见页面结构推断，实际使用时可能需要根据目标网站的最新页面结构调整
2. **视频上传**：大文件上传时间较长，建议设置 `--wait-timeout 600` 或更长
3. **登录状态**：发布前请确保已在 Chrome 中登录对应平台
4. **浏览器复用**：使用 `--port 9222` 可复用已登录的 Chrome 会话
5. **错误处理**：上传失败时会抛出异常并返回错误信息

---

## 🔧 依赖安装

```bash
cd /Users/xiaohei/.openclaw/workspace/skills/app_publish/scripts
pip install -r requirements.txt
# 或手动安装
pip install requests websockets
```

---

**开发时间：** 2026-04-02  
**参考技能：** xiaohongshu-skills/xhs-publish  
**开发工具：** Cursor CLI Agent
