# AIRS 产业研究订单采集 Skills

Repository: `airs-embodied-intelligence-research-skills`

AIRS 产业研究订单采集 Skills 面向具身智能、机器人、新能源汽车、低空经济、半导体装备等多行业产业研究，把企业主体确认、公开证据采集、第三方订单核查、招投标案例提取、标准入库表生成和案例质量复查组织成可复用的研究 Skill。

## Skills

| Skill | 路径 | 命令 |
| --- | --- | --- |
| 企业全称确认 | `skills/company-identity/SKILL.md` | `npm run search` |
| 天眼查中标公告采集 | `skills/bidding-crawl/SKILL.md` | `npm run crawl` |
| 第三方订单核查 | `skills/thirdparty-verify/SKILL.md` | `npm run verify` |
| 招投标案例提取 | `skills/case-extract/SKILL.md` | `npm run extract` |
| 标准入库表生成 | `skills/case-ingest/SKILL.md` | `npm run ingest` |
| 案例质量复查 | `skills/case-quality-review/SKILL.md` | `npm run quality:review` |

## Quick Start

```bash
npm install
cp config/settings.example.json config/settings.json
```

然后在本地 `config/settings.json` 中填写 OpenAI-compatible API key。

按需运行对应 Skill 命令：

```bash
npm run search
npm run crawl
npm run extract
npm run ingest
```

## Browser Requirement

涉及天眼查搜索、公告采集和第三方订单核查的 Skill 需要 Chrome 以远程调试模式启动，并在该浏览器会话中登录天眼查。

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

## Data And Secrets

真实数据、进度文件、输出文件和本地配置默认不进入仓库：

- `data/`
- `config/settings.json`
- `*.xlsx`
- `*.docx`

发布前请确认没有提交 API Key、天眼查登录信息、内部 Excel 或真实客户数据。

## Catalog

- Skill 目录：`skills/catalog.json`
