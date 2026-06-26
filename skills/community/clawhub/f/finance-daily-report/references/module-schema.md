# 模块配置规范

## 配置文件位置

用户在工作区创建 `finance-report-config.yaml`（或由 Skill 生成默认配置）。

## 模块定义格式

```yaml
# finance-report-config.yaml
report_title: "全球财经日报"  # 可自定义标题
timezone: "Asia/Shanghai"

modules:
  - id: market_theme              # 唯一标识（英文，用于内部引用）
    name: 市场主线                 # 显示名称（中文）
    enabled: true                  # 是否启用
    priority: 1                    # 排序（越小越靠前）
    heading_level: 2               # Markdown 标题级别（默认2）
    data_strategy: fetch           # fetch | search | both
    fetch_urls:                    # 直接抓取的 URL 列表
      - url: "https://tradingeconomics.com/united-states/stock-market"
        maxChars: 5000
        extract: analysis          # analysis | table | raw
    search_keywords: []            # web_search 关键词（data_strategy=search/both 时使用）
    collector_prompt: |            # 自定义采集指令（覆盖默认）
      提取当日市场最大的 2-3 个叙事主线。
      重点关注央行动态、关键经济数据发布、重大政策/地缘事件。
    template: |                    # 自定义输出模板（覆盖默认）
      {market_narrative}
    sub_sections: []               # 子板块（三级标题）
```

## 字段说明

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| id | ✅ | string | 唯一标识，英文+下划线 |
| name | ✅ | string | 显示名，用于报告标题 |
| enabled | ❌ | bool | 默认 true |
| priority | ❌ | int | 排序，默认 100 |
| data_strategy | ❌ | enum | fetch/search/both，默认 both |
| fetch_urls | ❌ | list | 直接抓取的 URL |
| search_keywords | ❌ | list | 搜索关键词，{date} 会被替换 |
| collector_prompt | ❌ | string | 采集指令，{date}/{tomorrow_date} 会被替换 |
| template | ❌ | string | 输出模板 |
| sub_sections | ❌ | list | 子板块定义（格式同 module，heading_level=3）|

## 变量替换

配置中以下变量会在运行时被替换：
- `{date}` → T-1 交易日日期（如 2026-03-13）
- `{tomorrow_date}` → T+1 日期
- `{report_date}` → 报告发布日期
- `{weekday}` → 星期几

## 模块分组（用于子代理分配）

Skill 自动将模块分组给子代理：
- 每组 ≤4 个模块
- 同类模块尽量分到一组（如股指+汇率+商品）
- 分组算法：按 data_strategy 归类，fetch 类优先合并
