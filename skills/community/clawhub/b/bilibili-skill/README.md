# 📺 Bilibili Skill for OpenClaw

让 AI Agent 控制 B 站 (Bilibili)！支持发布动态、管理视频、搜索内容、获取弹幕等。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ⚠️ 风险警告 / Risk Warning

**使用前请仔细阅读 / Please read carefully before use:**

🔴 **高风险操作 / High Risk Operation**
- 本技能涉及 B 站账号 API 操作，**可能触发风控导致账号被限制甚至封禁**
- This skill involves Bilibili account API operations, **may trigger risk control leading to account restriction or ban**

🔴 **使用风险 / Usage Risks**
- 频繁调用 API 可能被判定为机器人行为
- Frequent API calls may be flagged as bot behavior
- 发布/删除动态等操作有速率限制
- Post/delete operations have rate limits
- Cookie 泄露可能导致账号被盗
- Cookie leakage may lead to account theft

🔴 **免责声明 / Disclaimer**
- **使用本技能即表示你了解并接受上述风险**
- **By using this skill, you acknowledge and accept the above risks**
- 作者不对任何账号损失负责
- Authors are not responsible for any account losses
- 请谨慎使用，建议仅用于学习/测试
- Use with caution, recommended for learning/testing only

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 通过 OpenClaw 安装
openclaw skill install bilibili

# 或手动安装
cp -r bilibili ~/.openclaw/workspace/skills/
```

### 配置认证 / Configure Authentication

**方法 1: 环境变量**
```bash
export BILIBILI_SESSDATA="your_sessdata"
export BILIBILI_BILI_JCT="your_bili_jct"
export BILIBILI_BUVID3="your_buvid3"
```

**方法 2: 配置文件**
创建 `~/.openclaw/workspace/bilibili-cookies.md`:
```markdown
SESSDATA=xxx
bili_jct=xxx
buvid3=xxx
```

### 使用示例 / Usage Examples

**发布动态:**
```bash
bilibili-wrapper.sh dynamic publish --content "Hello B 站！"
```

**搜索视频:**
```bash
bilibili-wrapper.sh search video --keyword "Python 教程" --json-output
```

**获取用户信息:**
```bash
bilibili-wrapper.sh user info --uid 3706946142079013 --json-output
```

## 📋 可用命令 / Available Commands

### 动态操作 / Dynamic Operations
- `dynamic publish` - 发布动态
- `dynamic delete` - 删除动态
- `dynamic repost` - 转发动态

### 视频操作 / Video Operations
- `video info` - 获取视频信息
- `video stats` - 获取统计数据
- `video like` - 点赞/取消点赞

### 用户操作 / User Operations
- `user info` - 获取用户信息
- `user videos` - 用户投稿列表

### 搜索操作 / Search Operations
- `search video` - 搜索视频
- `search user` - 搜索用户

### 直播操作 / Live Operations
- `live info` - 直播间信息

## 🔧 高级用法 / Advanced Usage

### MCP 集成 / MCP Integration

在 `~/.openclaw/openclaw.json` 中添加:
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

### 批量操作 / Batch Operations

```python
#!/usr/bin/env python3
import subprocess
import time

for content in ["第一条", "第二条", "第三条"]:
    subprocess.run(f"bilibili-wrapper.sh dynamic publish --content '{content}'", shell=True)
    time.sleep(3)  # 避免风控
```

## 📚 依赖 / Dependencies

- Python 3.10+
- bilibili-api-python
- click
- Pillow
- pycryptodome
- beautifulsoup4
- brotli
- qrcode
- apscheduler

安装所有依赖:
```bash
pip3 install bilibili-api-python click Pillow pycryptodome beautifulsoup4 brotli qrcode apscheduler --break-system-packages
```

## 🎯 功能对比 / Feature Comparison

| 功能 / Feature | MCP Server | CLI 工具 |
|---------------|-----------|---------|
| 搜索内容 / Search | ✅ | ✅ |
| 用户查询 / User Info | ✅ | ✅ |
| 视频详情 / Video Info | ❌ | ✅ |
| 发布动态 / Post Dynamic | ❌ | ✅ |
| 删除动态 / Delete Dynamic | ❌ | ✅ |
| 获取弹幕 / Get Danmaku | ✅ | ❌ |
| 点赞视频 / Like Video | ❌ | ✅ |
| 直播查询 / Live Info | ❌ | ✅ |

**推荐**: 两者结合使用！/ **Recommended**: Use both together!

## 📝 更新日志 / Changelog

### v1.0.0 (2026-03-13)
- ✨ 初始版本 / Initial release
- ✅ 支持动态发布/删除 / Dynamic post/delete
- ✅ 支持视频/用户查询 / Video/user query
- ✅ 支持搜索功能 / Search functionality
- ✅ 支持直播查询 / Live room info
- ✅ MCP Server 集成 / MCP Server integration
- ⚠️ 添加风险警告 / Risk warning added

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 PR！/ Welcome to submit Issues and PRs!

- GitHub: https://github.com/OmegaalphaXiaoXueJu/bilibili-skill
- ClawHub: bilibili

## 📄 许可证 / License

MIT License

## 🔗 相关链接 / Related Links

- [bilibili-api](https://github.com/Nemo2011/bilibili-api)
- [bilibili-mcp-server](https://github.com/huccihuang/bilibili-mcp-server)
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- [OpenClaw](https://github.com/openclaw/openclaw)

---

**维护者 / Maintainer**: 小爪 🐾
**最后更新 / Last Updated**: 2026-03-13
