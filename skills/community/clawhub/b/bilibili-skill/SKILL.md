---
name: bilibili
description: B 站 (Bilibili) CLI 工具 - 发布动态、管理视频、搜索内容、获取弹幕
metadata: {"openclaw":{"emoji":"📺","requires":{"bins":["python3","bilibili-cli"]},"install":[{"id":"pip","kind":"pip","package":"bilibili-api-python click","bins":["bilibili-cli"],"label":"安装 B 站 CLI 依赖"}]}}
---

# Bilibili Skill for OpenClaw

📺 让 AI Agent 控制 B 站！支持发布动态、管理视频、搜索内容、获取弹幕等。

## 🚀 快速开始

### 安装依赖

```bash
pip3 install bilibili-api-python click Pillow pycryptodome beautifulsoup4 brotli qrcode apscheduler --break-system-packages
```

### 配置认证

在调用命令时提供 Cookies：

```bash
bilibili-cli.py \
  --sessdata "你的 SESSDATA" \
  --bili_jct "你的 bili_jct" \
  --buvid3 "你的 buvid3" \
  dynamic publish --content "Hello B 站！"
```

或者将 Cookies 保存到文件：
```bash
# Cookies 已保存在 /root/.openclaw/workspace/bilibili-cookies.md
```

## 📋 可用命令

### 动态操作

**发布原创动态**:
```bash
bilibili-cli.py \
  --sessdata "$SESSDATA" --bili_jct "$BILI_JCT" --buvid3 "$BUVID3" \
  dynamic publish --content "动态内容" --img /path/to/image.jpg
```

**删除动态**:
```bash
bilibili-cli.py \
  --sessdata "$SESSDATA" --bili_jct "$BILI_JCT" \
  dynamic delete --dyn-id 1179226104862343192
```

**转发动态**:
```bash
bilibili-cli.py \
  --sessdata "$SESSDATA" --bili_jct "$BILI_JCT" \
  dynamic repost --dyn-id 123456 --content "转发评论"
```

### 视频操作

**获取视频信息**:
```bash
bilibili-cli.py video info --bvid BV1uv411q7Mv --json-output
```

**获取视频统计**:
```bash
bilibili-cli.py video stats --bvid BV1uv411q7Mv
```

**点赞视频**:
```bash
bilibili-cli.py \
  --sessdata "$SESSDATA" --bili_jct "$BILI_JCT" \
  video like --bvid BV1uv411q7Mv --status true
```

### 用户操作

**获取用户信息**:
```bash
bilibili-cli.py user info --uid 3706946142079013 --json-output
```

**获取用户投稿**:
```bash
bilibili-cli.py user videos --uid 3706946142079013 --ps 10
```

### 搜索操作

**搜索视频**:
```bash
bilibili-cli.py search video --keyword "Python 教程" --page 1 --json-output
```

**搜索用户**:
```bash
bilibili-cli.py search user --keyword "老番茄" --json-output
```

### 直播操作

**获取直播间信息**:
```bash
bilibili-cli.py live info --room-id 22708562 --json-output
```

## 🤖 AI Agent 集成

### OpenClaw MCP 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "mcp": {
    "servers": {
      "bilibili": {
        "command": "python3",
        "args": ["/root/.openclaw/workspace/external/bilibili-mcp-server/bilibili.py"],
        "transport": "stdio"
      }
    }
  }
}
```

### 环境变量方式

```bash
export BILIBILI_SESSDATA="0bc2bad7%2C1788944530%2Ce3acf%2A31..."
export BILIBILI_BILI_JCT="94c0e8c198bc26f5c58c11490bd8ef62"
export BILIBILI_BUVID3="BEDF1095-927E-9F61-3920-7364E75F194027291infoc"
```

然后在命令中使用：
```bash
bilibili-cli.py \
  --sessdata "$BILIBILI_SESSDATA" \
  --bili_jct "$BILIBILI_BILI_JCT" \
  --buvid3 "$BILIBILI_BUVID3" \
  dynamic publish --content "Hello!"
```

## 📊 功能对比

| 功能 | MCP Server | CLI 工具 |
|------|-----------|---------|
| 搜索内容 | ✅ | ✅ |
| 用户查询 | ✅ | ✅ |
| 视频详情 | ❌ | ✅ |
| 发布动态 | ❌ | ✅ |
| 删除动态 | ❌ | ✅ |
| 获取弹幕 | ✅ | ❌ |
| 点赞视频 | ❌ | ✅ |
| 直播查询 | ❌ | ✅ |

**推荐**: 两者结合使用！
- MCP Server 用于搜索/查询（AI 自然调用）
- CLI 工具用于发布/删除（脚本化操作）

## 🔧 高级用法

### 批量发布动态

```python
#!/usr/bin/env python3
import subprocess
import time

cookies = "--sessdata 'xxx' --bili_jct 'xxx' --buvid3 'xxx'"
contents = [
    "第一条动态",
    "第二条动态",
    "第三条动态"
]

for content in contents:
    cmd = f"bilibili-cli.py {cookies} dynamic publish --content '{content}'"
    subprocess.run(cmd, shell=True)
    time.sleep(3)  # 避免风控
```

### 获取视频弹幕（通过 MCP）

```python
from mcp import Client
from bilibili import get_video_danmaku

danmaku = get_video_danmaku("BV1uv411q7Mv")
print(danmaku)
```

## ⚠️ 注意事项

1. **速率限制**: 避免快速连续调用（建议间隔 2-3 秒）
2. **风控策略**: 大量操作可能需要代理
3. **Cookie 有效期**: SESSDATA 会过期，需定期更新
4. **合法使用**: 仅用于学习和测试，禁止滥用

## 📚 相关资源

- **bilibili-api**: https://github.com/Nemo2011/bilibili-api
- **B 站 MCP Server**: https://github.com/huccihuang/bilibili-mcp-server
- **CLI-Anything**: https://github.com/HKUDS/CLI-Anything
- **Cookies 配置**: `/root/.openclaw/workspace/bilibili-cookies.md`

## 🎯 使用示例

### 示例 1: 发布 Ollama 推荐动态

```bash
bilibili-cli.py \
  --sessdata "$SESSDATA" --bili_jct "$BILI_JCT" --buvid3 "$BUVID3" \
  dynamic publish --content "🦙 Ollama：让大模型在你本地电脑运行！

2026 年了还在把数据发给云端 AI？Ollama 让你一键运行 Llama、Mistral 等大模型！

✅ 完全免费 ✅ 隐私安全 ✅ 离线可用

安装超简单：
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.2

5 分钟就有自己的私有 AI 助手！🎉

#Ollama #AI #大语言模型 #开源 #本地 AI"
```

### 示例 2: 搜索 UP 主

```bash
bilibili-cli.py search user --keyword "老番茄" --json-output
```

输出：
```json
{
  "result": [
    {
      "uname": "老番茄",
      "mid": 546195,
      "fans": 2500000,
      "videos": 500,
      "level": 6
    }
  ]
}
```

### 示例 3: 获取视频信息

```bash
bilibili-cli.py video info --bvid BV1uv411q7Mv
```

输出：
```
标题：爆肝 98 小时！在 MC 中还原糖调小镇
UP 主：糖调
播放：1234567
点赞：98765
时长：3600 秒
```

---

**Skill 版本**: 1.0.0
**最后更新**: 2026-03-13
**维护者**: 小爪 🐾
