# PDF报告排版说明

## 报告结构（当前版本）

### 第1页：招标信息概况（日报）

**标题**：招投标信息概况
**内容**：
- 报告日期
- 汇总表格（5列）：网站名称 | 当日条数 | 当月条数 | 爬虫策略 | 筛选策略
- 当日总计 + 当月总计

**表格样式**：
- 表头背景：浅灰色 (`colors.lightgrey`)
- 边框：灰色细线 0.5pt
- 字体：中文，9pt，数据格居中，策略格左对齐
- **关键**：所有单元格均为 `Paragraph` 对象，`VALIGN='TOP'`，无固定行高，支持自动换行

---

### 第2页：月度概况（月报）

**标题**：招投标信息月度报告
**内容**：
- 报告时间 + 统计范围（当月第一天 至 最后一天）
- 汇总表格（6列）：网站名称 | 数据条数 | 当日数据 | 前一日数据 | 爬虫策略 | 筛选策略
- 底部求和行（背景色 `#d9e2f3`）
- 按 SITE_ORDER 固定顺序排列

**表格样式**：
- 表头背景：深蓝色 (`#1f4e79`)，白字
- 边框：灰色细线 0.5pt
- 字体：中文，9pt
- **关键**：所有单元格均为 `Paragraph` 对象（含白字表头样式），`VALIGN='TOP'`，无固定行高

---

### 第3页开始：月度平台明细（月报）

**结构**：每个平台独立一页，按 SITE_ORDER 排序

**每页内容**：
- 标题：平台名称（共X条）
- 项目清单表格（4列）：网站 | 日期 | 项目名称 | 链接

**表格样式**：
- 表头背景：深蓝色 (`#1f4e79`)，白字，居中
- 边框：灰色细线 0.3pt
- 字体：中文，9pt
- 行背景：白色和whitesmoke交替
- **关键**：所有单元格均为 `Paragraph` 对象，`VALIGN='TOP'`，无固定行高

---

## 技术实现要点

### Paragraph + 自动换行（核心）

ReportLab 表格只有 `Paragraph` 对象才触发 `wordWrap`，普通字符串不会换行：

```python
# 单元格样式
cell_style = ParagraphStyle(
    'Cell',
    fontName=self.chinese_font,
    fontSize=9,
    alignment=TA_LEFT,
    leading=11,
    wordWrap='CJK',      # 中文换行
)

# 表头样式（白字）
header_style = ParagraphStyle(
    'Header',
    fontName=self.chinese_font,
    fontSize=10,
    alignment=TA_CENTER,
    leading=12,
    wordWrap='CJK',
    textColor=colors.white,  # 白字
)

# 表格数据用 Paragraph 包裹
table_data = [[
    Paragraph('网站名称', header_style),
    Paragraph('2026-05-07', cell_style),
    Paragraph(project_name, cell_style),  # 触发自动换行
    Paragraph('<link href="...">点击查看</link>', link_style),  # 可点击
]]
```

### TableStyle 关键设置

```python
table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),      # 顶部对齐（不是MIDDLE）
    ('TOPPADDING', (0, 0), (-1, -1), 4),      # 单元格内边距
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    # 禁止设置固定 ROWHEIGHT，否则换行失效
]))
```

### 可点击超链接

```python
link_style = ParagraphStyle(
    'Link',
    fontName=self.chinese_font,
    fontSize=8,
    textColor=colors.blue,
    leading=10,
    wordWrap='LTR',
)

if url:
    link_para = Paragraph(
        f"<link href='{url}' color='blue' underline='yes'>{url}</link>",
        link_style
    )
```

---

## 数据统计规则

### 当日统计
- 查询条件：`publish_date = 指定日期`
- 分组字段：`source_site`

### 当月统计
- 查询条件：`publish_date BETWEEN 当月第一天 AND 当月最后一天`
- 分组字段：`source_site`

### 月度概况页"当日数据"和"前一日数据"
- 调用 `_get_daily_count_for_site(site, date)` 实时查询
- 用于展示最新一天的数据

---

## PDF文件规范

### 文件命名
- 月报：`招投标信息月报_<年份>年<月份>月.pdf`
- 示例：`招投标信息月报_2026年05月.pdf`

### 文件存储
- 目录：`~/.openclaw/workspace/skills/bidding-assistant/招投标数据/daily/`

### 页面设置
- 页面大小：A4
- 边距：1.5cm（上、下、左、右）
- 方向：纵向

---

## 中文字体配置

系统自动查找，macOS 优先使用苹方：

```python
def get_chinese_font(self):
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',       # macOS
        'C:/Windows/Fonts/msyh.ttc',                 # Windows
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # Linux
    ]
```

---

## 版本历史

- **v3.0** (2026-05-07)：全表Paragraph换行优化
  - 所有表格所有列均改为 `Paragraph` 对象
  - `VALIGN='TOP'`，去掉所有固定 `ROWHEIGHT`
  - 链接改为可点击超链接（不截断URL）
  - 月度概况表新增"当日数据""前一日数据"两列 + 求和行
  - 所有页面均按 SITE_ORDER 固定顺序排列

- **v2.0** (2026-04-12)：重新设计排版结构
  - 第1页：招标信息概况
  - 第2页：当日清单
  - 第3页开始：分平台清单

- **v1.0** (2026-04-12)：初始版本

---

**文档版本**：3.0
**最后更新**：2026-05-07
