# 🎯 bid-collection

**招投标商机采集 Skill for Claude Code**

7×24 监控全网公开招投标信息，基于公司业务赛道智能筛选高价值商机线索，实现招投标项目早发现、早跟进、早布局。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Cryptocxf%2Fbid--collection-blue)](https://github.com/Cryptocxf/bid-collection)

---

## 安装

将 `bid-collection` 文件夹放入 `Desktop/skills/` 目录，然后在 Claude Code 中输入：

```
/bid-collection
```

技能自动加载（无参数时仅显示命令帮助菜单，不自动采集）。

## 使用方式

| 命令 | 功能 | 副作用 |
|------|------|--------|
| `/bid-collection`（无参数） | 显示帮助菜单 | 无出站请求、无本地写入 |
| `/bid-collection scan <关键词>` | 实时扫描招投标商机 | 出站请求 + 写入 `leads-output/bid/` |
| `/bid-collection monitor` | 启动定时监控（需确认） | 创建 cron 任务 + 周期出站请求 + 通知 + 日志 |
| `/bid-collection monitor --stop` | 停止监控并清理 cron | 清理宿主调度任务 |
| `/bid-collection report` | 生成汇总报告 | 纯本地，无出站请求 |
| `/bid-collection list-sources` | 查看监控渠道 | 无出站请求 |
| `/bid-collection add-source <url>` | 添加监控源（需确认） | 会向该 URL 发起出站请求（SSRF 风险） |
| `/bid-collection remove-source <url>` | 移除监控源 | 无出站请求 |

## 采集范围

- **政府平台**：中国政府采购网、各省/市公共资源交易中心、中国招标投标公共服务平台
- **国企采购**：中国移动、中国联通、中国电信、国家电网、中石油、中铁等
- **行业网站**：AI/大模型、数字化转型、IT服务、算力、智慧应用等
- **第三方聚合**：千里马、采招网、招标雷达、比地招标、剑鱼标讯等
- **自定义关键词**：监控关键词与行业场景可配置

## 核心价值

- 🌐 **全域覆盖**：政府平台、国企采购、行业网站一站聚合
- ⏰ **实时同步**：招标预告 → 正式招标 → 变更 → 中标，全周期跟踪
- 🧠 **智能匹配**：基于 10 大业务赛道自动筛选高适配商机
- 📊 **标准展示**：项目名称、采购方、预算、时间、需求、联系方式一键掌握

## CLI 参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--days=N` | 3 | 搜索时间窗口（天） |
| `--budget-min=N` | 不限 | 最低预算（人民币元） |
| `--budget-max=N` | 不限 | 最高预算（人民币元） |
| `--track=core` | 全部 | 仅核心赛道 |
| `--priority=urgent` | 全部 | 仅紧急商机 |
| `--output=detail` | 简版 | 含内容摘要 |
| `--interval=N` | 120 | monitor 扫描间隔（分钟） |
| `--max-runs=N` | 48 | monitor 最大运行轮数 |
| `--persist` | 关 | monitor cron 跨会话持久化 |
| `--stop` | — | 停止 monitor 并清理 cron |

---

## 🔒 安全说明

- **仅采集公开信息**：所有目标均为公开招投标公告页面，不读取非公开/需登录内容，不绕过访问控制
- **不读取用户敏感配置**：本技能不读取环境变量、API Key、`.env`、密钥文件或任何系统敏感配置
- **出站请求显式化**：`scan` / `monitor` / `add-source` 均会向外部平台发起出站 HTTP 请求；执行前会在控制台输出将要请求的域名范围，用户可中断
- **本地写入受控**：结果默认写入技能同级 `leads-output/bid/` 目录，不静默写入 Desktop 或其他位置
- **monitor 需显式确认**：`monitor` 会创建宿主 cron 任务（修改宿主调度）、周期性发起出站请求、发送系统通知、写入本地日志；执行前必须告知用户并获得确认；使用完毕请执行 `monitor --stop` 清理
- **add-source 的 SSRF 风险**：`add-source <url>` 会使技能向该 URL 发起出站请求；仅添加可信公开平台，添加内网/本地/元数据地址会被拒绝
- **合规使用**：遵守目标网站 `robots.txt` 与使用条款

详见 `SKILL.md` 顶部的完整《隐私、合规与安全边界》声明。

---

## 链接

- **GitHub**: https://github.com/Cryptocxf/bid-collection
- **Issues**: https://github.com/Cryptocxf/bid-collection/issues

## License

MIT
