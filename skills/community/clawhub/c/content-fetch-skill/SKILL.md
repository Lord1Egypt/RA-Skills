---
name: content-fetch-skill
description: 多站点网页内容抓取工具，基于 Playwright 浏览器自动化抓取 Twitter/X.com 推文、知乎文章/回答、微信公众号文章、今日头条、虎嗅等站点，以及任意通用网页。统一通过 URL 自动匹配站点并执行抓取，输出结构化 JSON、页面截图和图片。当用户要求"抓取/爬取/下载/获取"网页文章、推文、公众号文章、知乎回答、新闻内容时使用。触发词：抓取推文、爬取 Twitter、爬取 X、下载推文、抓取知乎、爬取知乎、抓取公众号、爬取微信文章、抓取头条、爬取头条、抓取虎嗅、爬取虎嗅、抓取网页、爬取文章、下载文章、获取网页内容、保存网页、采集内容。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: playwright
        bins: [playwright]
      - kind: uv
        package: pyyaml
    emoji: "📰"
---

# 多站点内容抓取技能 (content-fetch-skill)

基于 Playwright 浏览器自动化的多站点内容抓取工具。通过统一入口 `workflow.py` 接收 URL，自动识别目标站点并调度对应的爬取脚本，最终输出结构化的 JSON 数据、页面截图与图片资源。

## 适用场景

当用户提出以下需求时调用本技能：

- 抓取 Twitter/X.com 单条推文或长文 (Article)
- 抓取知乎专栏文章、问题回答
- 抓取微信公众号文章
- 抓取今日头条文章
- 抓取虎嗅网文章
- 抓取任意网页（通用模式，自动提取标题、正文、图片）

## 快速开始

```bash
# 安装依赖（首次使用）
pip install playwright pyyaml
playwright install chromium

# 通过统一入口运行（推荐，会自动匹配站点）
python workflow.py --url <目标URL>

# 显式指定参数
python workflow.py \
  --url https://x.com/some_user/status/1234567890 \
  --proxy http://127.0.0.1:17890 \
  --cookies x_cookie.json
```

首次运行后，配置会自动写入 `config.json`，下次运行无需重复输入。

## 核心架构

```
content-fetch-skill/
├── SKILL.md                  # 本文件，技能元信息和调用说明
├── workflow.py               # 统一入口：URL → 站点匹配 → 调度爬取
├── config.yaml               # 站点配置（代理、Cookie 路径、domain）
├── scripts/                  # 各站点爬取脚本，每个导出 scrape_task
│   ├── scrape_twitter.py     # Twitter/X.com（推文、长文）
│   ├── scrape_zhihu.py       # 知乎（文章、回答）
│   ├── scrape_wechat.py      # 微信公众号
│   ├── scrape_toutiao.py     # 今日头条
│   ├── scrape_huxiu.py       # 虎嗅
│   └── scrape_general.py     # 通用站点 fallback
├── references/
│   └── troubleshooting.md    # 故障排查（代理、Cloudflare、登录等）
├── x_cookie.json             # Twitter Cookie（需用户提供）
├── zhihu_cookie.json         # 知乎 Cookie（需用户提供）
└── fetch_data/               # 抓取结果输出根目录
    └── {站点}/{任务ID}/      # 每次任务一个独立目录
        ├── result.json       # 结构化抓取结果
        ├── page_screenshot.png  # 全页面截图
        └── images/           # 下载的图片资源
```

### URL → 站点匹配逻辑

`workflow.py` 解析 URL 域名，按以下优先级匹配 `config.yaml` 中的站点：

1. **精确匹配**：URL 域名包含站点配置的 `domain` 字段
2. **通用兜底**：未匹配到时使用 `general` 节点
3. **未知**：保存到 `fetch_data/unknown/`

## 站点能力一览

| 站点 | 标识 | Cookie | 代理 | 特殊能力 |
|------|------|--------|------|---------|
| Twitter/X.com | `twitter` | 必填 | 通常需要 | 自动展开"显示更多"、识别长文 Article、增量去重 |
| 知乎 | `zhihu` | 必填 | 可选 | 支持文章页和问题回答页 |
| 微信公众号 | `wechat` | 可选 | 可选 | 自动关闭登录弹窗 |
| 今日头条 | `toutiao` | 可选 | 可选 | - |
| 虎嗅 | `huxiu` | 可选 | 可选 | 智能清理正文头尾、过滤广告/相关推荐 |
| 通用网页 | `general` | 可选 | 可选 | 智能识别 article/content 容器 |

## 输出格式

所有站点统一返回 List[Dict]，字段对齐：

```json
[
  {
    "title": "标题",
    "content": "正文纯文本",
    "url": "原始页面 URL",
    "images": [
      {"url": "图片URL", "alt": "alt文本", "local_path": "images/image_1.jpg"}
    ],
    "created_at": "发布时间",
    "author": "作者",
    "like_count": 0,
    "retweet_count": 0,
    "reply_count": 0,
    "screenshot": "page_screenshot.png"
  }
]
```

## 命令行参数

`workflow.py` 支持的参数：

| 参数 | 说明 | 必填 |
|------|------|------|
| `--url` | 目标 URL（任意支持的站点链接） | 是 |
| `--proxy` | 代理地址，例如 `http://127.0.0.1:17890`，传 `none` 表示不使用代理 | 否 |
| `--cookies` | Cookie 文件路径（JSON 格式，Playwright 兼容） | 视站点而定 |
| `--headless` | 无头模式，默认开启 | 否 |
| `--no-save-config` | 本次运行不保存配置到 `config.yaml` | 否 |

## 配置文件 (config.yaml)

每个站点独立配置，结构示例：

```yaml
fetch_site:
  proxy: none
  twitter:
    proxy: http://127.0.0.1:17890
    cookies_path: x_cookie.json
    domain: x.com
  zhihu:
    proxy: none
    cookies_path: zhihu_cookie.json
    domain: zhihu.com
  general:
    proxy: none
    cookies_path: ''

headless: true
default_url: ''
```

参数优先级：命令行参数 > 站点专属配置 > 全局默认 > 用户交互输入。首次运行时如果存在旧版 `config.json`，会自动迁移为 YAML 格式。

## 扩展新站点

新增站点的标准流程：

1. 在 `scripts/` 下创建 `scrape_{站点标识}.py`
2. 必须导出异步函数 `scrape_task`，签名固定：
   ```python
   async def scrape_task(
       proxy: str,
       url: str,
       cookies: str = '',
       headless: bool = True,
       output_dir: str = '',
       output: str = ''
   ) -> List[Dict]:
       ...
   ```
3. 在 `config.yaml` 的 `fetch_site` 下添加站点配置（含 `domain` 用于 URL 匹配）
4. 如该站点 Cookie 是可选的，无需修改；如必须登录，在 `workflow.py` 的 `SITES_REQUIRING_COOKIE` 中加入站点标识

## Cookie 准备

Twitter、知乎需要登录态。推荐使用浏览器扩展（如 EditThisCookie）导出 JSON 后保存到项目根目录：

- Twitter Cookie → `x_cookie.json`
- 知乎 Cookie → `zhihu_cookie.json`

脚本会自动转换 EditThisCookie 格式（包括 `expirationDate`、数字型 `sameSite`）为 Playwright 兼容格式。

**交互式选择文件**：在步进式提问的 Cookie 步骤输入 `[dialog]` 可弹出系统文件选择对话框（基于 tkinter，无 GUI 环境会自动降级为文本输入）。

## 故障排查

完整问题清单见 `references/troubleshooting.md`，常见情况：

| 问题 | 解决方案 |
|------|----------|
| Cloudflare 拦截（403） | 使用住宅 IP 代理替代数据中心 IP |
| 代理连接失败 | `curl -x http://127.0.0.1:17890 -s https://x.com` 验证代理 |
| Cookie 失效 / 被重定向到登录页 | 重新导出最新 Cookie |
| 推文内容截断 | 脚本已自动点击"Show more"，检查日志中的"点击展开"输出 |
| 图片下载失败 | 部分站点需要 Referer 头，虎嗅脚本已内置；通用站点可能拿不到 |

## 注意事项

- 仅用于个人合规的内容采集与归档，请遵守目标站点的 robots.txt 和服务条款
- Twitter/X 抓取建议使用住宅代理，避免数据中心 IP 被 Cloudflare 拦截
- 输出目录按站点和时间戳隔离，多次抓取互不覆盖
- Twitter 脚本支持基于 ID 的增量合并，重复抓取同一用户不会丢失历史数据
