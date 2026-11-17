<div align="center">

# Air-chart

**一句话，让 AI 给你画出全球空气质量专业图表。**

[English](README.md) | 简体中文 | [Español](README.es.md) | [हिन्दी](README.hi.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 这个 Skill 能干嘛？

你在 AI 对话里随口一句话，它就能**自动找站点、拉数据、出图表**，几秒给你一个由 x-cmd Draw 渲染的图表链接——数据和图都在 URL 里，直接贴进 Markdown 或报告：

> 💬 "看看北京最近一周 PM2.5 走势"
> 💬 "对比东京和首尔过去 7 天的空气质量"
> 💬 "德里过去 30 天 PM10，和 WHO 标准对比一下"
> 💬 "新加坡最近 48 小时臭氧的小时变化"
> 💬 "北京各个监测点现在谁最脏？"

背后发生的是一条全自动管道：解析城市 → 在全球最大的开放空气质量平台 **OpenAQ**（100+ 国家的政府参考级监测数据）里挑选**仍在正常更新**的监测站 → 清洗异常值与缺失时段 → 渲染成专业图表。

**为什么值得用：**

- **图表即链接，链接即数据**：默认交付的是一个 `x-cmd.com/draw` 链接——图和数据都在 URL 里。直接贴进 Markdown 当图片用、转发给别人，或者顺手把 URL 里某个数值改掉，图立刻跟着变。想要文件？`--out 图.svg`（或 `.png`）下载即可。
- **渲染交给 x-cmd Draw**：本地管线保持纯 `bash`/`jq`/`awk`/`curl`，图表引擎用 [x-cmd Draw](https://x-cmd.com/draw)——持续增加的图表类型（折线、柱状、面积、饼图、雷达、仪表盘、桑基图、甘特图、思维导图等）、明暗主题、多语言渲染、在线编辑器开箱即用，渲染代码零维护、零安装。
- **专业可信**：优先选用政府参考级监测站，图上标注物理浓度（µg/m³），并把 **WHO 24 小时安全基准**作为参考序列画进图里——限值和数据同行，一眼看出达不达标。不是花哨的 AQI 指数，是可写进报告的数据。
- **全球覆盖 + 智能纠错**：内置 250+ 城市坐标库，模糊输入（`delhi`、`tOKyo`、`中山`）都能识别，还支持直接传经纬度。
- **真实世界数据，不是玩具**：自动剔除停更的"僵尸站点"和传感器故障尖峰，数据缺失时段从坐标轴整段丢弃，绝不瞎补零。

## 效果演示

以下图表全部来自 **OpenAQ 真实监测数据**，由数据自带的 x-cmd Draw URL 实时渲染——仓库不存放任何图片文件。点开任意一张图即可进入编辑器改数据、看图变化。

| 多城 PM2.5 对比（最近 7 天：东京 · 首尔 · 伦敦） | 新德里 PM2.5 / PM10（最近 14 天） |
| --- | --- |
| ![多城 PM2.5 对比][sc1] | ![新德里多指标][sc3] |

| 伦敦臭氧（O3）48 小时逐时曲线 | 新德里各监测点 PM10 实时快照 |
| --- | --- |
| ![伦敦臭氧 48h][sc2] | ![新德里站点快照][sc4] |

| 深色主题：多城 PM2.5 对比 | 新德里 PM2.5（最近 30 天） |
| --- | --- |
| ![深色多城对比][sc5] | ![新德里 30 天][sc6] |

[sc1]: https://x-cmd.com/draw?type=line&title=PM2.5%20%E8%B5%B0%E5%8A%BF%E5%AF%B9%E6%AF%94%20%C2%B7%20%E6%9C%80%E8%BF%91%207d%20%C2%B7%20%E5%A4%9A%E5%9F%8E%E5%B8%82%E5%90%8C%E6%8C%87%E6%A0%87%E5%AF%B9%E6%AF%94&unit=%C2%B5g%2Fm%C2%B3&labels=11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:5.14,2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:9.46,7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:37.3,58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024h:15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc2]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%2F%20PM10%20%E8%B6%8B%E5%8A%BF%20%C2%B7%20%E6%9C%80%E8%BF%91%2014d%20%C2%B7%20%E5%8D%95%E5%9F%8E%E5%B8%82%E5%A4%9A%E6%8C%87%E6%A0%87%E5%AF%B9%E6%AF%94&unit=%C2%B5g%2Fm%C2%B3&labels=10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=New%20Delhi%20PM10:56.7,156,283,320,345,396,427,409,438,328,162,198,196,286,222&series=WHO%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc3]: https://x-cmd.com/draw?type=line&title=London%20O3%20%E8%B6%8B%E5%8A%BF%20%C2%B7%20%E6%9C%80%E8%BF%91%2048h%20%C2%B7%20%E7%AB%99%E7%82%B9%E5%BD%93%E5%9C%B0%E6%97%B6%E9%97%B4%20%28Europe%2FLondon%29&unit=%C2%B5g%2Fm%C2%B3&labels=11-11%2022%3A00,11-12%2000%3A00,11-12%2001%3A00,11-12%2002%3A00,11-12%2003%3A00,11-12%2004%3A00,11-12%2005%3A00,11-12%2006%3A00,11-13%2000%3A00,11-13%2001%3A00,11-13%2002%3A00,11-13%2003%3A00,11-13%2004%3A00,11-13%2005%3A00,11-13%2006%3A00,11-13%2007%3A00&series=London%20O3:44.6,51.1,52.7,51.2,42.7,43.1,41,31.4,42.7,44.9,46.5,48.3,39.6,17.1,15.4,17&series=WHO%2024h:100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100&w=960&h=500&t=opendata
[sc4]: https://x-cmd.com/draw?type=hbar&title=New%20Delhi%20%E5%90%84%E7%AB%99%E7%82%B9%20PM10%20%E5%AE%9E%E6%97%B6%E5%BF%AB%E7%85%A7%20%C2%B7%202026-11-14%2009%3A37%20IST%20%C2%B7%2025km%20%E5%8D%8A%E5%BE%84&unit=%C2%B5g%2Fm%C2%B3&labels=Alipur,Anand%20Vihar,Ashok%20Vihar,Aya%20Nagar,Bawana,Burari%20Crossing&values=378.0,347.0,337.0,324.0,346.0,497.0&num=all&w=960&h=480&t=evil-glow
[sc5]: https://x-cmd.com/draw?type=line&title=PM2.5%20%E8%B5%B0%E5%8A%BF%E5%AF%B9%E6%AF%94%20%C2%B7%20%E6%9C%80%E8%BF%91%207d%20%C2%B7%20%E5%A4%9A%E5%9F%8E%E5%B8%82%E5%90%8C%E6%8C%87%E6%A0%87%E5%AF%B9%E6%AF%94&unit=%C2%B5g%2Fm%C2%B3&labels=11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:5.14,2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:9.46,7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:37.3,58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024h:15,15,15,15,15,15,15,15&w=960&h=500&scheme=dark&t=opendata
[sc6]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%E8%B6%8B%E5%8A%BF%20%C2%B7%20%E6%9C%80%E8%BF%91%2030d%20%C2%B7%20%E7%AB%99%E7%82%B9%E5%BD%93%E5%9C%B0%E6%97%B6%E9%97%B4%20%28Asia%2FKolkata%29&unit=%C2%B5g%2Fm%C2%B3&labels=10-14,10-15,10-16,10-17,10-18,10-19,10-20,10-21,10-22,10-23,10-27,10-28,10-29,10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:104,73.6,65.7,94,127,94,125,142,136,142,138,131,95,44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=WHO%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata

## 特性

- **零重型依赖**：仅需 `bash` / `jq` / `awk` / `curl`——数据管道自研，渲染交给 x-cmd Draw，不需要 Python、Matplotlib 或 Node.js。
- **全球覆盖**：内置 200+ 全球主要城市坐标库，也支持直接传入 `lat,lon`。
- **智能站点优选**：25km 半径检索 → 剔除 24h（必要时 72h）未更新的僵尸站点 → 优先选择政府参考级监测站（Reference-grade）。
- **专业视觉**：醒目标注物理浓度单位（µg/m³），默认叠加 WHO 空气质量指南 24 小时基准虚线（PM2.5=15 / PM10=45 / O3=100 / NO2=25 / SO2=40 / CO=4），浅/深双主题。
- **工程化**：本地缓存（小时级 20min / 日级 2h TTL）、429 限流指数退避、数据断点（缺失时段折线断开而非错误插值）、UTC→站点当地时间自动对齐。

## 快速开始

### 1. 配置 API Key（免费，约 1 分钟）

1. 打开 [OpenAQ Explorer 注册页](https://explore.openaq.org/register) 注册或[直接登录](https://explore.openaq.org/login)。
2. 登录后打开[账户页](https://explore.openaq.org/account)，页面下方即可看到并复制你的 API Key。
3. 任选其一配置：

```bash
export OPENAQ_API_KEY="你的key"                                # 临时 / CI
echo 'OPENAQ_API_KEY=你的key' > ~/.config/air-chart/config     # 持久
```

> 凭证策略刻意保持轻量：OpenAQ Key 属免费公共服务凭证，无需系统钥匙串，明文配置文件即可。
> 没有 Key 也能用 `--demo` 演示模式预览完整效果。

### 2. 运行

```bash
# 单城市 7 天 PM2.5 趋势
./scripts/air_chart.sh --city Beijing --param pm25 --period 7d

# 多城市对比（最多 4 城）
./scripts/air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d

# 单城市多指标（如 PM2.5 + PM10）
./scripts/air_chart.sh --city Beijing --param pm25 --param pm10 --period 30d

# 48 小时小时级曲线（观察昼夜规律）
./scripts/air_chart.sh --city Singapore --param o3 --period 48h

# 同城多站点实时快照（柱状图）
./scripts/air_chart.sh --city Delhi --param pm10 --snapshot

# 深色主题 + 指定输出
./scripts/air_chart.sh --city London --param no2 --period 14d --theme dark -o london.svg
```

### 3. 作为 AI Agent Skill 安装

将本仓库（或其中 `SKILL.md` + `scripts/` + `data/`）放入你的 Agent skills 目录即可，例如：

```bash
git clone https://github.com/qiakai/air-chart.git ~/.claude/skills/air-chart
# 或: npx skills add qiakai/air-chart
```

之后对 Agent 说"对比东京和首尔过去 7 天的 PM2.5 走势"即可自动调用。

`SKILL.md` 为英文版（兼容各平台收录与路由），中文版见 `SKILL.zh.md`。

## 命令参数

| 参数 | 说明 | 取值 |
| --- | --- | --- |
| `--city, -c` | 城市名（可重复，≤4 个）或坐标 `"lat,lon"` | `Beijing`、`New Delhi`、`39.9,116.4` |
| `--param, -p` | 污染物指标（默认 `pm25`） | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | 时间跨度（默认 `7d`） | `24h` `48h`（小时级）· `7d` `14d` `30d`（日级） |
| `--snapshot` | 同城多站点实时快照柱状图 | 开关 |
| `--theme` | 主题 | `light` / `dark` |
| `--lang` | 输出语言（图表 + 提示文案） | `en` `zh` `es` `hi` `ja` `ko` `fr`（默认按系统 locale 自动检测） |
| `--out, -o` | 下载图表为 `.svg` 或 `.png` | 默认仅输出 x-cmd Draw 链接 |
| `--demo` | 演示模式（免 API Key） | 开关 |

## 架构

```text
[城市/指标/时间跨度]
   │
   ▼
geo_resolve.sh      城市名 → 坐标+时区（内置坐标库 / 坐标直传）
   │
   ▼
openaq_client.sh    OpenAQ API v3：鉴权、User-Agent 标识、md5 缓存、
                    429 指数退避、活性过滤(24h/72h)、按参数固定 ID
                    匹配传感器、参考级站点优选
   │
   ▼
data_transform.awk  清洗(负值/超物理上限尖峰)、断点检测(缺失时段
                    断开, 严禁填 0)、统计聚合、当地时区标签
   │
   ▼
render_draw.sh      x-cmd Draw URL 拼接器 (URL 即数据; 可下载 .svg/.png)
```

`data/parameters.tsv` 为静态参数字典（对齐 openaq-api 污染物固定 ID）：slug / param_id / 名称 / 单位 / WHO 24h 基准 / 物理上限 / 指标专属色，消除冗余 `/parameters` 探测。视觉规范对齐 openaq-explorer：指标专属色板（PM2.5 `#E65100`、PM10 `#6A1B9A`、O3 `#0277BD`、NO2 `#00838F`）、多城色盲友好色板、WHO 基准线达标绿 `#10B981` / 超标红 `#EF4444`；站点单位与默认单位不一致时自动隐藏 WHO 线以防量纲误导。

## 退出码

| 码 | 含义 |
| --- | --- |
| 3 | 未配置 API Key（附注册引导） |
| 4 | 网络 / API 异常 / 限流重试耗尽 |
| 5 | 无活性站点或无有效数据 |
| 2 | 城市名无法解析（附相近候选） |

## License

MIT
