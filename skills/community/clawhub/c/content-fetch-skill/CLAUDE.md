# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

多站点网页内容抓取工具，基于 Playwright 浏览器自动化，支持 Twitter/X、知乎、微信公众号、今日头条、虎嗅等站点，以及通用网页抓取。作为 Claude Code Skill 使用，通过 URL 自动匹配对应站点的爬取脚本。

## 运行命令

```bash
# 安装依赖
pip install playwright pyyaml
playwright install chromium

# 通过统一入口运行（自动匹配站点）
python workflow.py --url <目标URL>

# 直接运行单个站点脚本
python scripts/scrape_twitter.py --proxy http://127.0.0.1:17890 --cookies x_cookie.json --url <推文URL>
```

## 架构

入口是 `workflow.py`，核心流程：
1. 解析 URL → 通过 `config.yaml` 中的 domain 字段匹配站点
2. 动态加载 `scripts/scrape_{站点标识}.py` 模块
3. 调用模块导出的 `scrape_task()` 异步函数
4. 结果保存到 `fetch_data/{站点标识}/{时间戳任务ID}/result.json`

每个站点脚本必须导出 `scrape_task` 异步函数，签名统一为：
```python
async def scrape_task(proxy, url, cookies, headless, output_dir, output) -> List[Dict]
```

## 站点配置

`config.yaml` 管理站点配置，结构为 `fetch_site.{站点标识}`，每个站点包含 `proxy`、`cookies_path`、`domain` 字段。匹配优先级：精确站点 > general > unknown。首次运行时如果存在旧版 `config.json` 会自动迁移为 YAML。

## Cookie 管理

- Twitter/知乎：必须提供 Cookie 文件（JSON 格式，Playwright 兼容）
- 微信/头条/虎嗅/general：Cookie 可选

## 新增站点

1. 在 `scripts/` 下创建 `scrape_{站点标识}.py`，导出 `scrape_task` 函数
2. 在 `config.yaml` 的 `fetch_site` 中添加站点配置（含 domain 用于 URL 匹配）
3. 如果 Cookie 可选，在 `workflow.py` 的 `SITES_REQUIRING_COOKIE` 列表中不添加该站点标识
