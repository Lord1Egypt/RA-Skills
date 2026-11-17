---
name: crag-finder
description: 当用户提及查找野攀岩场、攀岩区域、抱石场所，或询问特定地区/国家/城市的攀岩目的地时，应使用此技能。它利用 theCrag.com 搜索并获取攀岩区域信息。触发关键词包括：野攀、岩场、攀岩场、抱石、攀岩区域、野攀岩场、climbing crag、climbing area、outdoor climbing、bouldering area、thecrag、路书。
---

# 野攀岩场查找器

## 概述

本技能用于在 theCrag.com（全球最大的攀岩与抱石协作平台）上搜索野攀和抱石区域（岩场），获取岩场名称、路线数量、难度等级、GPS 坐标、接近信息和热门路线等关键信息。

## 工作流程

### 第一步：确定搜索目标

从对话中提取用户想要搜索的地点。可能的形式包括：

- 国家名称（如"中国"、"日本"、"泰国"）
- 省份/州（如"云南"、"广西"、"阳朔"）
- 城市（如"昆明"、"丽江"、"怀集"）
- 具体岩场名称（如"南高峰"、"黎明"、"燕玺"）

如果用户未指定地点，询问其想搜索哪个区域。

### 第二步：构造 theCrag.com 网址

theCrag.com 使用层级式 URL 结构组织攀岩区域：

- **国家级别**：`https://www.thecrag.com/climbing/{国家slug}`
  - 示例：`https://www.thecrag.com/climbing/china`
  - 示例：`https://www.thecrag.com/climbing/japan`
  - 示例：`https://www.thecrag.com/climbing/thailand`

- **区域/省份级别**：`https://www.thecrag.com/climbing/{国家slug}/{区域slug}`
  - 示例：`https://www.thecrag.com/climbing/china/yangshuo`
  - 示例：`https://www.thecrag.com/climbing/china/yunnan`

- **具体岩场级别**：`https://www.thecrag.com/climbing/{国家slug}/{区域slug}/{岩场slug}`
  - 示例：`https://www.thecrag.com/climbing/china/yangshuo/moon-hill`

- **直接搜索**：`https://www.thecrag.com/zh_hans/search?q={关键词}`

slug 通常为小写字母，空格用连字符替换。常用国家 slug 包括：
- china、japan、thailand、vietnam、indonesia、australia、usa、france、spain、italy、greece、turkey

对于中国地点，使用英文 slug（如 "china"、"yangshuo"、"yunnan"、"liming"、"huaiji"）。

### 第三步：获取并提取信息

使用 `web_fetch` 工具获取页面内容。注意 theCrag.com 有反爬保护，可能会返回 403 错误。此时：

1. 回退使用 `web_search`，搜索词格式为：`thecrag.com {地点} 攀岩 岩场`
2. 利用搜索结果构造 URL 并提供给用户手动打开
3. 从搜索结果摘要中汇总已有信息

如果页面成功获取，提取以下关键信息：

- **区域名称**：页面主标题
- **路线总数**：已记录的攀岩路线数量
- **难度范围**：可攀爬的难度等级区间
- **攀岩类型**：运动攀、传统攀、抱石等
- **热门子岩场**：页面列出的下级区域
- **GPS 坐标**：位置数据（如有）
- **接近信息**：关于接近路线、限制或最佳季节的说明

### 第四步：呈现结果

以结构化的格式呈现搜索结果，使用中文描述：

```
## 🧗 {岩场名称} 岩场信息

**位置**：{区域/国家}
**路线总数**：{路线数量}
**难度范围**：{难度区间}
**攀岩类型**：{攀岩类型}
**热门子岩场**：
- {子岩场1} - {路线数} 条路线
- {子岩场2} - {路线数} 条路线
...

**GPS 坐标**：{如有}
**接近信息**：{如有}
**最佳季节**：{如有}

**🔗 详情链接**：{theCrag.com 网址}
```

### 第五步：处理多个结果

如果搜索返回多个区域或用户正在浏览，先提供概览列表，再让用户深入查看具体区域。

## 重要提示

- theCrag.com 有 Cloudflare 反爬保护。如果 `web_fetch` 返回 403，始终回退使用 `web_search`，并提供直接 URL 供用户在浏览器中打开。
- 网站支持多语言。在 URL 路径中使用 `zh_hans`（如 `https://www.thecrag.com/zh_hans/climbing/china`）可加载简体中文界面。
- theCrag 上的信息由用户贡献。路线数量和难度等级为社区维护，可能不完整。
- 中国区域的岩场正被岩友积极维护，许多有中文路线名称和描述。
- 优先使用 `web_search` 获取信息，因为搜索结果摘要中通常直接包含路线数量和难度范围等关键数据。

## 资源

### references/
- `url_patterns.md` - theCrag.com URL 结构详细参考，含全球各区域示例
