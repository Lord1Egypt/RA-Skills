# 查询词策略

## 基础流程

1. 抽取主体：公司、产品、人物、地点、机构、事件、概念。
2. 抽取图片目的：证据、解释、对比、现场、封面、产品、文档。
3. 生成中文查询。
4. 生成英文查询。
5. 添加图片类型词。
6. 添加排除词。
7. 必要时添加站点或来源限定。

## 查询模板

### 官方或产品图

```text
{产品名} official screenshot
{产品名} interface
{公司名} product page image
site:{official_domain} {产品名} screenshot
```

### 报告、数据、图表

```text
{主题} report chart
{机构名} {主题} PDF chart
{指标名} {年份} chart
site:{domain} {主题} filetype:pdf
```

### 事件现场

```text
{事件名} {地点} {日期} photo
{event name} {location} {year} press release image
site:{official_or_news_domain} {event name} photo
```

### 人物或机构

```text
{人物名} Wikimedia Commons
{person name} official portrait
{机构名} headquarters photo
```

### 解释图

```text
{概念} diagram
{机制} infographic
{流程} flowchart
{技术名} architecture diagram
```

### 图库场景图

```text
{主题关键词} workplace
{行业} team meeting
{场景} portrait landscape
```

## 排除词

按搜索工具支持情况添加：

```text
-logo -advertisement -wallpaper -poster -icon -avatar -stock -AI-generated
```

注意：图库搜索中不要排除 `stock`，因为图库本身就是素材库；全网搜索中通常要排除。

## 中文到英文

- 中国本土政策、机构、地点：先中文，再英文。
- 国际公司、技术、产品：先英文，再中文。
- 热点事件：同时用原语言、英文通用名、中文报道名。
- 不确定英文名时，先搜实体官网或百科页确认标准写法。

## 查询质量判断

好的查询能让前 20 个结果中出现具体主体。若结果都是氛围图或泛化插画，应收窄：

- 加年份、地点、版本号。
- 加官方域名或来源机构。
- 加图片类型词。
- 改用英文实体名。
- 改查原始报告、公告或文档。
