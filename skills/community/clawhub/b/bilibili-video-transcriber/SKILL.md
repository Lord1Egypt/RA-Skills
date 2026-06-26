---
name: bilibili-video-transcriber
description: 【B站字幕获取】专业处理 B 站视频字幕问题，支持语音转文字、字幕下载、内容分析。基于实际 B 站字幕系统错误问题开发，提供完整的解决方案。
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      anyBins:
        - python3
        - ffmpeg
    os:
      - linux
      - darwin
      - win32
---

# 🎬 B 站视频转录专家

**专业处理 B 站视频字幕问题，支持语音转文字、字幕下载、内容分析**

## 📋 功能特性

### ✅ 核心功能
1. **智能字幕优先**：自动按优先级获取（CC 字幕 → AI 字幕 → 音频转录 → 视频下载）
2. **Cookie 安全存储**：多路径冗余存储 + immutable 写保护，防止误删
3. **自动失效检测**：每次处理视频前自动验证 Cookie 有效性
4. **飞书扫码通知**：Cookie 失效时自动生成二维码并通过飞书发送
5. **语音转文字**：使用 Whisper/Vosk 模型进行高精度语音识别（自动检测系统配置，按需下载）
6. **国内镜像支持**：自动使用国内镜像源
7. **批量处理**：支持批量处理多个 B 站视频
8. **大会员支持**：支持扫码登录获取大会员权限
9. **faster-whisper 按需安装**：安装时自动检测系统配置，不满足条件则跳过 faster-whisper，使用 Vosk 替代

### 🔧 Cookie 安全机制
```
存储路径（3重冗余）:
  1. 技能目录: ~/.openclaw/workspace/skills/.../.bilibili_cookie  ← immutable 保护
  2. 用户目录: ~/.bilibili_cookie_storage
  3. 配置目录: ~/.config/bilibili_transcriber/cookie
  
运行引用: ~/.bilibili_cookie.txt（自动同步，600权限）

失效时: → 自动检测 → 生成二维码 → 通过飞书发送 → 用户扫码 → 自动保存
```

## 🚀 快速开始

### 1. 安装依赖
```bash
# 安装技能包
clawhub install bilibili-transcriber-pro

# 或手动安装依赖
pip install bilibili-api requests pydub faster-whisper vosk qrcode
```

### 2. 扫码登录（推荐）
```bash
# 扫码登录（会自动保存到冗余存储）
bilibili-transcribe --login

# 检查登录状态
bilibili-transcribe --check-cookie
```

### 3. 基本使用
```bash
# 处理单个视频（自动验证Cookie，含评论获取）
bilibili-transcribe BV1txQGByERW

# 指定Cookie文件
bilibili-transcribe BV1txQGByERW --cookie ~/.bilibili_cookie.txt

# 批量处理
bilibili-transcribe --batch bv_list.txt
```

### 4. 输出特点：评论获取
```bash
# 处理视频时会自动获取热门评论（按点赞排序），包含：
# - 热评内容 + 点赞数
# - 热评下的回复
# - 评论写入 markdown 的 💬 评论区部分
# - CLI 直接展示前3条热评预览
```

## 📖 详细用法

### Cookie 管理（新增）
```bash
# 扫码登录（推荐方式）
bilibili-transcribe --login

# 检查Cookie状态
bilibili-transcribe --check-cookie
# 输出示例：
#   ✅ Cookie 有效
#   👤 用户: 你的B站用户名
#   🏆 大会员: ✅
#   📂 存储路径: ~/.bilibili_cookie.txt

# 手动更新Cookie
bilibili-transcribe --update-cookie "SESSDATA=xxx; bili_jct=xxx"

# 设置环境变量
export BILIBILI_COOKIE="SESSDATA=xxx; bili_jct=xxx"
```

### Python API（Cookie 管理）
```python
from cookie_manager import (
    save_cookie, load_cookie, check_cookie_valid,
    needs_cookie_refresh, BilibiliQRLogin, send_qr_via_feishu
)

# 检查Cookie是否需要刷新
reason = needs_cookie_refresh()
if reason:
    print(f"⚠️ Cookie 需要刷新: {reason}")
    login = BilibiliQRLogin()
    qr_path = login.generate_qr_code()
    
    # 通过飞书发送二维码
    send_qr_via_feishu(qr_path)
    
    # 轮询等待扫码
    result = login.poll_login()
    if result['success']:
        print(f"✅ 登录成功: {result['username']}")
else:
    print("✅ Cookie 有效")
```

## 🛠️ 配置选项

### 配置文件 `~/.config/bilibili_transcriber/config.yaml`
```yaml
# Cookie 配置（增强版）
cookie:
  file: "~/.bilibili_cookie.txt"
  auto_refresh: true
  refresh_interval: 86400  # 24 小时
  redundant_storage: true   # 启用冗余存储
  storage_paths:
    - "~/.openclaw/workspace/skills/bilibili-video-transcriber/.bilibili_cookie"
    - "~/.bilibili_cookie_storage"
    - "~/.config/bilibili_transcriber/cookie"
  notify_on_expire: true    # Cookie失效时通知
  notify_channel: "feishu"  # 通知通道

# 模型配置
model:
  engine: "whisper"
  name: "base"
  device: "cpu"
  compute_type: "int8"
  language: "zh"

# 飞书通知配置
notify:
  channel: "feishu"  # 通知通道
  qr_temp_dir: "/tmp"
```

## 📊 输出格式

### 0. 评论获取（新增）
处理视频时自动按**点赞排序**获取热门评论，最多 30 条热评 + 每条热评 3 条回复。
- 数据保存在 markdown 的 `💬 热门评论` 部分
- JSON 格式包含 `comments` 数组
- CLI 输出展示前 3 条热评预览

### 1. 文本格式 (`transcript.txt`)
```
[0.00s -> 3.90s] 兄弟们 HermesAgent 刚刚发布了更新 4.13
[3.90s -> 5.76s] 那么这一次最大的一个升级呢
[5.76s -> 9.00s] 是它带来了本地的外部控制面板
...
```

### 2. JSON 格式 (`transcript.json`)
```json
{
  "video_info": {
    "bvid": "BV1txQGByERW",
    "title": "视频标题",
    "duration": 210,
    "up": "UP主名"
  },
  "transcript": [
    {"start": 0.0, "end": 3.9, "text": "内容", "confidence": 0.95}
  ],
  "cookie_status": {
    "valid": true,
    "user": "用户名",
    "is_vip": true
  }
}
```

### 3. Markdown 格式 (`summary.md`)
```markdown
# 视频标题

**视频信息**
- BV 号：BV1xxx
- 时长：210 秒
- UP 主：xxx
- Cookie 状态：✅ 有效 (用户: xxx)

**核心内容**
1. 要点一
2. 要点二

**完整转录**
[0.00s -> 3.90s] 内容
...
```

## 🔧 Cookie 管理详解

### 冗余存储机制
```
cookie_manager.py 负责管理 Cookie 的存储和生命周期：

┌─────────────────────────────────────────────────┐
│                  cookie_manager                   │
├─────────────────────────────────────────────────┤
│  1. save_cookie(cookie_str)                      │
│     → 写入活跃文件 (~/.bilibili_cookie.txt)      │
│     → 同步到3个冗余路径（含 immutable 保护）     │
│     → 设置 600 权限                              │
├─────────────────────────────────────────────────┤
│  2. load_cookie()                                │
│     → 依次查找所有存储路径                        │
│     → 如果从备份读到，自动补全到活跃路径          │
│     → 也检查环境变量 BILIBILI_COOKIE             │
├─────────────────────────────────────────────────┤
│  3. check_cookie_valid(cookie_str)               │
│     → 调用 bilibili_api 验证有效期               │
│     → 返回 {valid, username, is_vip, error}      │
├─────────────────────────────────────────────────┤
│  4. needs_cookie_refresh()                       │
│     → 快速检查是否需要刷新                        │
│     → 返回 None=有效, str=失效原因               │
├─────────────────────────────────────────────────┤
│  5. BilibiliQRLogin                              │
│     → generate_qr_code() → 生成二维码图片        │
│     → poll_login() → 轮询扫码结果               │
│     → poll_once() → 单次检查（供外部调用）       │
├─────────────────────────────────────────────────┤
│  6. send_qr_via_feishu(image_path)               │
│     → 写入信号文件（供代理处理器读取并发送）     │
└─────────────────────────────────────────────────┘
```

### 飞书扫码登录流程
```
1. 用户发送 B 站链接 or 调用 --login
2. cookie_manager 检测到 Cookie 不存在/失效
3. BilibiliQRLogin 生成二维码图片
4. send_qr_via_feishu 写入信号文件
5. [代理处理器] 读取信号 → 上传飞书图片 → 发送给用户
6. 用户扫码 → poll_login 轮询到成功
7. save_cookie 保存到冗余存储
8. 继续处理视频
```

### 安全特性
- **权限 600**：仅文件所有者可读写
- **chattr +i**：对技能目录内的 Cookie 设置 immutable 标记，不可删除/修改
- **多路径冗余**：3个独立存储位置，任一被删都能从其他路径恢复
- **自动恢复**：load_cookie 发现活跃文件被删时，自动从备份恢复

## 🔗 与其他技能的集成

### 与 cookie_manager 的集成
```python
# 在任何脚本中都可以使用
from cookie_manager import (
    save_cookie, load_cookie, check_cookie_valid,
    needs_cookie_refresh
)

# 获取当前 Cookie（自动加载、自动恢复）
cookie_str = load_cookie()
if cookie_str:
    status = check_cookie_valid(cookie_str)
    print(f"用户: {status['username']}, 有效: {status['valid']}")
```

## 🔍 故障排除

### Cookie 相关问题

#### 1. 提示 "Cookie 已失效"
```bash
# 重新扫码登录
bilibili-transcribe --login

# 或手动更新
bilibili-transcribe --update-cookie "SESSDATA=xxx; bili_jct=xxx"
```

#### 2. Cookie 文件被误删
```
不用担心，cookie_manager 会自动从备份路径恢复。
备份位置：
  ~/.openclaw/workspace/skills/bilibili-video-transcriber/.bilibili_cookie
  ~/.bilibili_cookie_storage
  ~/.config/bilibili_transcriber/cookie

技能目录内的备份设置了 immutable 保护，不可删除。
```

#### 3. 检查 Cookie 存储状态
```bash
bilibili-transcribe --check-cookie
```

## 📝 飞书文档创建经验

### ⚠️ lark-cli 1.0.18 已知问题

**问题**：`lark-cli docs +create --markdown ./file.md` 会错误地将**文件名本身**写入内容，而非文件内容。

**解决方法**：使用 pipe 方式传入 Markdown 内容：
```bash
cat content.md | lark-cli docs +create \
  --title "[视频总结] UP主名 - 标题 - 日期" \
  --markdown - \
  --wiki-space "知识空间ID"
```

### 📍 飞书自定义域名

飞书返回的 `doc_url` 为 `https://www.feishu.cn/wiki/...`，但企业可能使用自定义域名（如 `https://企业名.feishu.cn/wiki/...`）。

直接点返回的 `doc_url` 可能跳转失败，需要**在知识库内找到实际链接**，用企业自定义域名格式发送给用户。

### 📑 Markdown 格式注意

1. **表格**：必须使用 `<lark-table>` 标签格式，标准 Markdown 表格（`| ... |`）在飞书中可能不渲染
2. **高亮块**：使用 `<callout emoji="🎬" background-color="light-blue">...</callout>` 标签
3. **分栏**：使用 `<grid cols="2"><column>...</column></grid>` 标签
4. **一级标题**：文档标题通过 `--title` 参数设置，Markdown 内容中**不要**包含相同的一级标题（`#`）
5. **emoji 参数**：在 `<callout>` 标签的 `emoji` 属性中使用实际 emoji 字符（如 `🎬`），而非名称（如 `clapper`）

### 📦 文档存储结构
```markdown
文档结构模板：
1. <callout> 高亮块 — 说明文字
2. ## 📋 视频信息 — lark-table 行列式表格
3. ## 📝 结构化内容总结 — 分段详解（源自字幕/转写）
4. ## 🔑 核心要点 — 提炼的干货要点
5. ## 💬 热门评论 — 评论区精选
6. ## 🔗 字幕文件 — 原始文件说明
```

### 🔐 认证说明

- 使用 `lark-cli` 前需先完成 `lark-cli auth login`
- 认证后凭体验证 `lark-cli docs +create` 可用
- 文档创建到知识空间需指定 `--wiki-space` 参数

## 💻 低资源服务器转写策略

### ⚠️ faster-whisper 按需安装机制

**安装时自动检测系统配置**（setup.py 中 `check_system_capability` 函数）：
- 有 GPU → 安装 faster-whisper（GPU 模式）
- ≥4GB 内存（无 GPU）→ 安装 faster-whisper（CPU 模式）
- <4GB 内存（无 GPU）→ **跳过** faster-whisper 安装，使用 Vosk 离线引擎

**运行时自动路由**（bilibili_transcriber.py 中 `_detect_system_resources` 函数）：
- 自动检测 faster-whisper 是否已安装
- 已安装 + 有 GPU → Whisper medium + cuda
- 已安装 + ≥8GB 内存 → Whisper base + cpu
- 已安装 + ≥2GB 内存 → Whisper tiny + cpu
- 未安装或内存 <2GB → Vosk 离线引擎（分块处理）

### 硬件环境参考
- **CPU**：2核
- **内存**：1.6GB（可用常 < 500MB）
- **模型**：VOsk small-cn-0.22（66MB）

### 策略对比

| 方案 | 结果 | 说明 |
|------|------|------|
| Whisper tiny/base | ❌ OOM | 即使 tiny 也会被杀 |
| faster-whisper base | ❌ 被 kill | 39分钟后被 OOM kill |
| Vosk small (66MB) | ✅ 可行 | 16分钟视频214秒转写完成 |
| Vosk + chunk | ✅ 稳定 | 6×180秒分块处理，避免一次性加载 |

### 推荐流程（无字幕时）

```bash
# 1. 下载音频（优先 dash audio）
# 2. ffmpeg 转 WAV（16kHz, mono, 16bit）
# 3. 分块处理（每块 ≤3 分钟）
# 4. Vosk 逐块识别 → 拼接
```

### 输出目录命名
```
bilibili_transcripts/{UP主名称}_{视频标题}/  # 取代 BV号 格式
├── transcript.json   # 含转写+评论的完整数据
├── transcript.txt    # 纯文本
├── summary.md        # 结构化总结
├── summary_full.md   # 详细总结（含评论）
└── comments.json     # 评论数据
```

## 📄 许可证

MIT License

---

**最后更新：** 2026-05-17

**本次更新内容：**
1. ✅ 新增 `get_comments()` 方法：自动获取视频热门评论（按热度排序）
2. ✅ `ProcessingResult` 新增 `comments` 字段
3. ✅ `save_transcript()` markdown 格式新增 `💬 热门评论` 区块
4. ✅ `print_result()` CLI 输出展示前 3 条热评
5. ✅ 评论获取非关键步骤，失败不影响主流程
6. ✅ 支持热评下的回复获取
7. ✅ 飞书文档创建经验：`lark-cli 1.0.18 --markdown` bug 及 workaround
8. ✅ Vosk 分块转写策略：chunk 180s × 6，适用于 2GB 内存服务器
9. ✅ 输出目录命名：采用 `{up_name}_{video_title}` 而非 BV 号
10. ✅ 飞书自定义域名适配：返回知识库内正确域名链接
