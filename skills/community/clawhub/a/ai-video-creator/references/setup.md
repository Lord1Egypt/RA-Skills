# 环境配置指南

## 1. 火山引擎即梦 API

用于 AI 视频生成。

### 获取 API Key

1. 注册 [火山引擎](https://www.volcengine.com/) 账号
2. 开通 [即梦AI](https://www.volcengine.com/docs/85621/1544715) 视频生成服务
3. 在控制台获取 Access Key 和 Secret Key

### 配置环境变量

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export VOLCENGINE_ACCESS_KEY="your_access_key"
export VOLCENGINE_SECRET_KEY="your_secret_key"
```

### 验证

```bash
source ~/.zshrc
echo $VOLCENGINE_ACCESS_KEY | head -c 5
# 应输出 key 的前5个字符
```

### 费用参考

| 模型 | 费用 |
|------|------|
| 视频生成 3.0 720P | ¥0.28/秒 |
| 视频生成 3.0 1080P | ¥0.63/秒 |
| 视频生成 3.0 Pro | ¥1.00/秒 |

默认使用 720P，每日 20 秒视频约 ¥5.6。

## 2. 小红书 MCP Server

用于视频发布到小红书。

### 安装

从 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu) 下载或编译二进制文件。

### 启动

```bash
./xiaohongshu-mcp -headless=true -port :18060
```

### 首次登录

首次使用需要扫码登录小红书账号，按 MCP Server 文档操作。

### 验证

```bash
python3 scripts/xhs_publish.py status
# 应输出: Logged in as: <your_username>
```

## 3. 系统依赖

### ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# 验证
ffmpeg -version
```

### Python 依赖

```bash
pip install -r requirements.txt
```

### 中文字体（文字叠加用）

默认使用 macOS 系统字体。其他系统需设置环境变量：

```bash
# Linux 示例
export VIDEO_FONT="/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
```

## 4. BGM 背景音乐

将无版权 `.mp3` 文件放入 `bgm/` 对应子目录：

```
bgm/
├── healing/     # 治愈温暖
├── quiet/       # 安静平和
├── warm/        # 温馨感动
├── melancholy/  # 淡淡忧伤
├── dreamy/      # 梦幻飘渺
├── citynight/   # 都市夜景
└── nature/      # 自然之声
```

推荐来源：[Pixabay Music](https://pixabay.com/music/) / [Free Music Archive](https://freemusicarchive.org/)

## 排查问题

| 问题 | 解决方案 |
|------|---------|
| `VOLCENGINE_ACCESS_KEY not set` | 检查环境变量，运行 `source ~/.zshrc` |
| `Cannot connect to MCP server` | 确认 xiaohongshu-mcp 已启动 |
| `Access Denied: api forbidden` | API 额度用完或密钥过期，检查火山引擎控制台 |
| `Font not found` | 设置 `VIDEO_FONT` 环境变量指向中文字体 |
| 视频无声音 | 检查 `bgm/` 目录下是否有音乐文件 |
