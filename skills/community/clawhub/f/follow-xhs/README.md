# Follow-XHS

小红书笔记搜索和内容获取工具，支持笔记搜索、详情获取，可配合 AI 生成结构化分析报告。

## 功能

- **笔记搜索** - 按关键词搜索小红书笔记，支持分页、排序、时间过滤
- **笔记详情** - 获取指定笔记的完整内容
- **用户笔记** - 获取指定用户发布的笔记列表
- **用户信息** - 获取当前登录用户信息
- **请求加密** - 自动处理小红书 Web 端请求签名和 Cookie 生成
- **代理支持** - 支持 HTTP/SOCKS5 代理
- **频率限制** - 内置请求频率控制和重试机制

## 项目结构

```
├── prompts/
│   └── summary_prompt.md         # AI 分析报告提示词
├── scripts/
│   ├── request/
│   │   └── web/
│   │       ├── apis/             # API 接口封装
│   │       │   ├── auth.py       # 认证相关
│   │       │   └── note.py       # 笔记搜索与详情
│   │       ├── encrypt/          # 请求加密模块
│   │       │   ├── config.py     # 加密配置加载
│   │       │   ├── xhs_encrypt.py # 加密入口
│   │       │   ├── cookie/       # Cookie 生成
│   │       │   ├── header/       # 请求头签名
│   │       │   └── other/        # 指纹生成等
│   │       ├── exceptions/       # 异常定义
│   │       ├── config.json       # 运行时配置（需自行创建）
│   │       ├── config.example.json # 配置模板
│   │       ├── search_config_loader.py # 配置加载器
│   │       └── xhs_session.py    # 会话管理
│   └── units/                    # 工具模块
├── skill.md                      # Skill 定义文件
└── requirements.txt
```

## 安装

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/follow-xhs.git
cd follow-xhs

# 安装依赖
pip install -r requirements.txt
```

## 配置

1. 复制配置模板：

```bash
cp scripts/request/web/config.example.json scripts/request/web/config.json
```

2. 编辑 `config.json`，填入你的 `web_session` cookie 值：

```json
{
  "web_session": {
    "value": "你的web_session值"
  }
}
```

> **获取 web_session**：浏览器登录 [小红书](https://www.xiaohongshu.com)，打开开发者工具 (F12) -> Application -> Cookies，找到 `web_session` 的值。

### 可选配置

- **代理** - 设置 `proxy.enabled` 为 `true` 并填入代理地址
- **搜索参数** - 调整 `search` 下的默认分页大小、排序方式等
- **频率限制** - 修改 `rate_limit` 下的请求间隔和重试次数

## 依赖

- Python 3.10+
- aiohttp
- loguru
- pycryptodome
- getuseragent

## 免责声明

本项目仅供学习交流使用，请勿用于商业用途或违法活动。使用本工具的一切后果由使用者自行承担。

## License

MIT
