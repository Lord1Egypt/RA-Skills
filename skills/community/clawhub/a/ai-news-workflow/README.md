# AI资讯自动化工作流（ClawHub Skill）

本项目用于自动抓取 AI 产业资讯（RSS + 网页），完成筛选、企业匹配与拆分、分类、去重（保留最早）、豆包（火山方舟）标题/摘要生成与重点事件筛选，并输出 Excel 信息表与 Word 简报。

**入口脚本：** `skill_entry.py`  
**输出目录：** `./output/excel`、`./output/word`

---

## 1. 功能概览

### 1) 资讯来源
- **RSS 来源**：从 `input/source_config.xlsx` 配置读取（`fetch_method=rss`）
- **网页来源**：从 `input/web_source_config.xlsx` 配置读取（`fetch_method=webpage/web`），适用于无 RSS 的机构/平台网站

### 2) 处理流程（概念）
1. 抓取（RSS + Web）
2. 企业匹配（基于企业名单）
3. 企业级拆分：一条资讯只对应一家企业
4. 来源地区约束过滤（国内来源只匹配中国企业等）
5. 分类 / 重要性 / 相关性（按你的服务实现）
6. 去重：批次内去重 + 数据库去重（保留更早发布时间）
7. 豆包生成中文标题 + 摘要（可选，字数80字左右，上限约120）
   - 全球AI产业动态：判断国内/国际
   - 全球AI产业动态：重点事件打分与标记（供 Word Top5 使用）
8. 输出：Excel（完整版+简版） + Word

### 3) 输出文件
- **完整 Excel**：多 sheet（有效、重复、无效等）
- **有效数据简表 Excel**：仅保留关键列 + 颜色/冻结表头
- **Word 简报**：两大部分（企业动态 + 全球动态；全球动态可只写 Top5 重点事件）

---

## 2. 目录结构

运行后目录大致如下：
ai_news_workflow/
app/ # 核心代码
input/ # 输入文件（需准备）
企业名单.xlsx
source_config.xlsx
web_source_config.xlsx
output/ # 输出文件（运行后生成）
excel/
word/
data/ # sqlite 数据库（运行后生成）
logs/ # 日志（运行后生成）
templates/ # 可选：放模板文件
input_templates/
config.yaml # 当前运行配置（不存在时可由默认配置生成）
config.default.yaml # 默认配置（相对路径版，推荐）
requirements.txt
skill.yaml
skill_entry.py # Skill 入口（推荐运行它）
run.py # 主流程

---

## 3. 环境要求

- Python 3.10+（推荐 3.11）
- 能访问资讯来源站点（RSS/网页）
- 若启用豆包摘要：需要火山方舟 API Key（环境变量 `ARK_API_KEY`）

---

## 4. 安装依赖

在项目目录下执行：

```bash
pip install -r requirements.txt

## 5. 配置文件说明（config.yaml）
推荐做法
保留 config.default.yaml（相对路径）
若根目录下没有 config.yaml，运行 skill_entry.py 时会从 config.default.yaml 复制生成

关键配置项（常用）
paths.company_file：企业名单路径
paths.source_file：RSS 来源配置路径
paths.web_source_file：网页来源配置路径
crawler.rss_lookback_days：RSS 抓取回看天数（建议 3）
crawler.web_lookback_days：网页抓取回看天数（建议 3）
time_window.*：最终统计窗口（日报口径）
ark.*：豆包调用参数（建议 API Key 用环境变量）

##6. 输入文件准备（必须）

把以下 3 个文件放到 ./input/：
企业名单.xlsx
至少包含：企业名称、国家/地区等你代码里会用到的字段
source_config.xlsx（RSS 来源）
含 RSS 源 URL 及启用状态等
web_source_config.xlsx（网页来源）
用于配置无 RSS 的网站抓取规则（列表页 URL、链接过滤、选择器等）
网页来源（web_source_config.xlsx）建议字段
（列名需与你的 SourceLoader 匹配；如果你已跑通测试，就按你现有表头继续）
来源名称
是否启用（TRUE/1）
抓取方式（webpage/web）
地区（国内/国际）
来源类型（official/media/other）
url（建议填写，与 list_url 一致也可）
list_url
url_prefix
link_selector（可空）
link_href_contains（强烈推荐，用于过滤“查看详情”链接）
title_selector/date_selector/content_selector（可空，先用 fallback）

##7. 启用豆包（火山方舟）标题/摘要生成（可选但推荐）

推荐用环境变量，不要把 Key 写进配置文件。
Windows PowerShell：
$env:ARK_API_KEY="你的真实方舟APIKey"
Linux/macOS bash：
export ARK_API_KEY="你的真实方舟APIKey"
注意：环境变量里只放纯 Key，不要加 “Bearer ” 前缀，不要包含中文。

##8. 运行方式
方式 A：初始化（只创建目录与生成默认 config.yaml）
python skill_entry.py --init
会做：
创建 input/output/data/logs/templates 等目录（如不存在）
若没有 config.yaml，从 config.default.yaml 复制生成

方式 B：运行一次完整流程（推荐）
python skill_entry.py
成功后输出：
./output/excel/ 下生成 Excel
./output/word/ 下生成 Word

方式 C：指定配置文件运行
python skill_entry.py --config config.yaml

##9. 输出说明
1) Excel（完整）
一般包含：
news_table（有效数据）
duplicate_items（重复数据）
invalid_items（无效数据）
以及其它辅助 sheet（视你的 exporter 实现）

2) Excel（有效数据简表）
表头蓝底 + 冻结首行
按一级分类排序
行底色区分不同一级类别
可扩展：全球AI产业动态内按 “国内/国际” 排序

3) Word 简报
仅保留两部分：
一、“一带”AI领军企业动态
二、全球AI产业动态
可选逻辑：
全球AI产业动态只输出 5 个重点事件（由豆包综合“机构全球知名度 + 事件产业影响力”打分选出 Top5）
Excel 不变

##10. 常见问题排查
Q1：运行秒结束，没有输出文件
确认你运行的是 skill_entry.py（而不是只 import 的文件）
skill_entry.py 必须包含：
if __name__ == "__main__": ...
并且在里面调用 main(...)

Q2：web_sources=0（网页来源没被读到）
检查：
config.yaml 是否配置了 paths.web_source_file
web_source_config.xlsx 的 sheet 名是否为 sources（或与你 loader 默认一致）
“是否启用”是否为 TRUE/1
“抓取方式”是否为 webpage/web

Q3：网页来源抓到 0 条
检查：
list_url 是否可访问
link_href_contains 是否写对（建议用来过滤详情页链接）
网站是否强前端渲染（需要 Playwright 才能抓）——若是这种站，需要单独升级 crawler

Q4：豆包调用失败/被跳过
检查：
是否设置了 ARK_API_KEY
Key 是否包含中文、空格、或 “Bearer ” 前缀
网络是否可访问火山方舟接口
是否有调用额度/配额限制

Q5：Word 比有效数据简表少
常见原因：
Word 的全球AI产业动态只输出 Top5 重点事件（这是设计要求）
或你的 briefing_service.py 做了筛选/截断（建议对齐逻辑）

11. 生产化建议（定时任务）
Windows：任务计划程序（Task Scheduler）
Linux：crontab
建议每天定时执行：
python skill_entry.py

并将：
time_window 设置为日报口径（例如前一天 00:00 ~ 当天 00:00）
抓取回看天数设置为 3 天以上（防止来源延迟更新）

## 运行参数（覆盖 config.yaml）

参数优先级：命令行参数 > config.yaml > 默认值

### 抓取回看范围（Lookback Days）
- `--rss-lookback-days N`：RSS 抓取回看 N 天
- `--web-lookback-days N`：网页抓取回看 N 天

示例：抓取最近 7 天
```bash
python skill_entry.py --rss-lookback-days 7 --web-lookback-days 7

12. 版本信息
v0.1.1：支持 RSS+网页抓取、企业匹配与拆分、去重、豆包摘要与重点事件、Excel+Word 输出、统计时间自定义
