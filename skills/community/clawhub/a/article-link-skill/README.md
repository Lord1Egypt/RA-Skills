# article-link

文章链接提取工具 — 基于 [pick-read.vip](https://pick-read.vip) 接口，提交付费媒体文章链接，自动匹配已有内容并返回英文全文，或排队提取。

## 功能

- **查看媒体** — 查看支持提交的 15 家媒体来源
- **提交链接** — 提交文章 URL，匹配成功时自动返回英文全文
- **查询状态** — 查看提交任务的处理进度，完成时自动获取全文
- **获取全文** — 通过文章 ID 直接获取英文全文
- **配额管理** — 查看今日剩余提交次数

## 支持平台

本工具以 Skill 方式运行在以下 AI 平台：

| 平台 | 地址 |
|---|---|
| QClaw | https://qclaw.qq.com/ |
| WorkBuddy | https://copilot.tencent.com/work/ |
| OpenClaw | https://github.com/openclaw/openclaw |

## 快速开始

1. 下载本仓库（Code → Download ZIP）
2. 复制 `config.example.json` 为 `config.json`，填入你的导入令牌：

```bash
cp config.example.json config.json
```

```json
{
    "api_base": "https://pick-read.vip/api",
    "import_token": "imp-你的令牌填这里"
}
```

> ⚠️ `config.json` 已被 .gitignore 排除，不会被提交到仓库。

3. 在支持 Skills 的平台中安装本工具，即可直接使用

**导入令牌在哪里获取？** 登录 [pick-read.vip](https://pick-read.vip) → 账户页 → 导入令牌 → 生成令牌。

## 推荐提示词

```
帮我看看这篇华尔街日报文章讲了什么 https://www.wsj.com/articles/xxx
提交这个 FT 链接 https://www.ft.com/content/xxx
帮我深度解析这篇文章 https://www.economist.com/xxx
查看我今天还能提交多少次
查看支持哪些媒体
```

## 命令行使用

```bash
# 查看支持的媒体
python3 scripts/article_link.py media

# 查看今日配额
python3 scripts/article_link.py quota

# 提交文章链接（匹配成功时自动返回英文全文）
python3 scripts/article_link.py submit "https://www.wsj.com/articles/xxx"

# 深度解析模式（需确认）
python3 scripts/article_link.py submit "https://www.ft.com/content/xxx" --deep

# 查询任务状态
python3 scripts/article_link.py status "job-id-here"

# 获取文章英文全文
python3 scripts/article_link.py article "article-id-here"

# 查看近期任务
python3 scripts/article_link.py jobs
```

## 每日次数限制

| 模式 | 上限 | 说明 |
|---|---|---|
| 基础模式 | 50 次/天 | 先匹配已有内容，未命中排队提取 |
| 深度解析 | 5 次/天 | 跳过匹配，强制重新提取 |

## 说明

- 所有操作（除查看媒体列表）都需要有效的 Import Token
- Import Token 同时验证用户身份和订阅状态
- 任务结果保留 24 小时后自动过期
- 本工具无第三方依赖，仅使用 Python 标准库
