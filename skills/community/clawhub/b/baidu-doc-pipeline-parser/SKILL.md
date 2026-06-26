---
name: baidu-doc-pipeline-parser 百度文档解析
description: 调用百度文档解析API解析文档。支持PDF、Word、Excel、PPT、图片等18+格式。提取文本、表格、版面分析、OCR识别及RAG文档分块。当用户需要解析文档、提取文本/表格、分析文档结构、处理扫描件时使用。触发词：文档解析、PDF解析、Word解析、表格提取、OCR、文档分析、提取文本、文档结构、扫描识别。
license: MIT
---

# 百度文档解析 Skill

基于百度智能文档分析平台 API，提供文档解析能力。

## 功能概述

- 支持对 doc、pdf、图片、xlsx 等 18 种格式文档进行解析
- 输出文档的版面、表格、阅读顺序、标题层级、旋转角度等信息
- 支持中、英、日、韩、法等 20 余种语言类型
- 可返回 Markdown 格式内容，将非结构化数据转化为易于处理的结构化数据
- 识别准确率可达 90% 以上
- 文档分块（适用于 RAG 场景）

## 适用场景

当用户需要：
- 解析 PDF、Word、Excel 等格式文档
- 从文档中提取文本内容
- 识别并提取表格数据
- 分析文档结构（标题层级、章节、版面布局）
- 对扫描件进行 OCR 文字识别
- 将文档分块用于 RAG 应用

## API 配置

### 环境变量（必须）

[百度智能文档分析平台 领取免费测试资源](https://ai.baidu.com/ai-doc/OCR/dk3iqnq51)

使用前请设置以下环境变量：

```bash
export BAIDU_DOC_AI_API_KEY="your_api_key"
export BAIDU_DOC_AI_SECRET_KEY="your_secret_key"
```

### 认证方式

通过 API Key 和 Secret Key 获取 access_token，有效期 30 天。

## 支持格式

**版式文档**：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd, ppt, pptx

**流式文档**：doc, docx, txt, xls, xlsx, wps, html, mhtml

## 支持语言

CHN_ENG（中英文）、JAP（日语）、KOR（韩语）、FRE（法语）、SPA（西班牙语）、POR（葡萄牙语）、GER（德语）、ITA（意大利语）、RUS（俄语）、DAN（丹麦语）、DUT（荷兰语）、MAL（马来语）、SWE（瑞典语）、IND（印尼语）、POL（波兰语）、ROM（罗马尼亚语）、TUR（土耳其语）、GRE（希腊语）、HUN（匈牙利语）、THA（泰语）、VIE（越南语）、ARA（阿拉伯语）、HIN（印地语）

## 使用方式

```bash
python3 scripts/baidu_doc_parser.py --file_data <文件的base64编码>
python3 scripts/baidu_doc_parser.py --file_url <文件公网URL>
```

## API 接口

文档解析 API 服务为异步接口，需要先调用**提交请求接口**获取 task_id，然后调用**获取结果接口**进行结果轮询。

### 提交请求接口

- **HTTP 方法**：POST
- **请求 URL**：`https://aip.baidubce.com/rest/2.0/brain/online/v2/parser/task?access_token={token}`
- **Content-Type**：`application/x-www-form-urlencoded`

### 获取结果接口

- **HTTP 方法**：POST
- **请求 URL**：`https://aip.baidubce.com/rest/2.0/brain/online/v2/parser/task/query?access_token={token}`
- **Content-Type**：`application/x-www-form-urlencoded`
- **请求参数**：`task_id`（必填，提交请求时返回的 task_id）

## 请求参数

### 文件参数（必选，二选一）

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `file_data` | 和 file_url 二选一 | string | 文件 Base64 编码数据。版式文档：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd, ppt, pptx；流式文档：doc, docx, txt, xls, xlsx, wps, html, mhtml。文档大小不超过 50M，PDF 最大支持 2000 页。**若文档大小超过 50M，须从 file_url 方式上传**。优先级：file_data > file_url |
| `file_url` | 和 file_data 二选一 | string | 文件数据 URL，长度不超过 1024 字节，支持单个 URL 传入。PDF 文档大小不超过 300MB，非 PDF 不超过 50M，PDF 最大支持 2000 页。**请注意关闭 URL 防盗链** |
| `file_name` | 是 | string | 文件名，请保证文件名后缀正确，例如 "1.pdf" |

### 核心功能参数

| 参数 | 必选 | 类型 | 可选值范围 | 说明 |
|------|------|------|----------|------|
| `recognize_formula` | 否 | bool | True/False | 是否对版式类型文档进行公式识别 |
| `analysis_chart` | 否 | bool | True/False | 是否对统计图表进行解析 |
| `angle_adjust` | 否 | bool | True/False | 是否对图片进行角度矫正 |
| `parse_image_layout` | 否 | bool | True/False | 是否返回文档中的图片位置信息 |

### 语言与格式参数

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `language_type` | 否 | string | 识别语种类型，默认为 CHN_ENG（中英文） |
| `switch_digital_width` | 否 | string | 是否对数字进行全半角转换，默认为 auto。可选：auto（不转换）、half（半角输出）、full（全角输出） |
| `html_table_format` | 否 | bool | 是否将识别出的表格转换为 HTML 格式返回，**default=True** |

### 文档分块参数

`return_doc_chunks` 为字典类型，用于返回文档切分后的片段数据（按语义、字数、标点）：

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `switch` | 否 | bool | False | 是否进行文档内容切分 |
| `split_type` | 否 | str | chunk | 切分方式：chunk（按 chunk_size 来切）/ mark（按 separators 来切） |
| `separators` | 否 | list | ['。','；','！','？',';','!','?'] | 切分标点 |
| `chunk_size` | 否 | int | -1 | 切分块的大小，-1 表示按照语义自动切分，不限定块的大小 |

## 返回结构

### 提交请求返回

| 字段 | 类型 | 说明 |
|------|------|------|
| `log_id` | uint64 | 唯一的 log id，用于问题定位 |
| `error_code` | int | 错误码 |
| `error_msg` | string | 错误描述信息 |
| `result.task_id` | string | 该请求生成的 task_id，后续使用该 task_id 获取审查结果 |

### 获取结果返回

| 字段 | 类型 | 说明 |
|------|------|------|
| `log_id` | uint64 | 唯一的 log id |
| `error_code` | int | 错误码 |
| `error_msg` | string | 错误描述信息 |
| `result.task_id` | string | 任务 ID |
| `result.status` | string | 任务状态：pending（排队中）、processing（运行中）、success（成功）、failed（失败） |
| `result.task_error` | string | 解析报错信息，包含任务失败、额度不够 |
| `result.markdown_url` | string | 文档解析结果的 Markdown 格式链接，**链接有效期 30 天** |
| `result.parse_result_url` | string | 文档解析结果的 BOS 链接（JSON），**链接有效期 30 天** |

### 解析结果 JSON 结构（parse_result_url）

#### 顶层结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `file_name` | string | 文档名称 |
| `file_id` | string | 文档 ID |
| `pages` | list | 文件单页解析内容 |
| `chunks` | list | 文件内容切分结果（return_doc_chunks.switch=True 时有值） |

#### 页面对象（pages[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `page_id` | string | 页码 ID |
| `page_num` | int | 页码数 |
| `text` | string | 当前页的所有纯文字内容 |
| `layouts` | list | 页面内容版式分析的结果 |
| `tables` | list | 页面表格解析结果 |
| `images` | list | 页面中图片解析结果 |
| `meta` | dict | 页元信息 |

#### 页面元信息（meta）

| 字段 | 类型 | 说明 |
|------|------|------|
| `page_width` | int | 页面宽度 |
| `page_height` | int | 页面高度 |
| `is_scan` | bool | 是否扫描件 |
| `page_angle` | int | 页面倾斜角度 |
| `page_type` | string | 页面属性：text（正文）、contents（目录）、appendix（附录）、others（其他） |
| `sheet_name` | string | Excel 的 sheet 名 |

#### 版面元素（layouts[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `layout_id` | string | layout 元素唯一标志，格式 "xxxxx-layout-{global_layout_index}" |
| `text` | string | layout 对应的文本内容。注：当 type 为 table/image 时该字段为空，需根据 type 和 layout_id 分别到 tables/images 字段里找到对应内容 |
| `position` | list | 元素在页面中的位置 [x, y, w, h]，左上角和宽高 |
| `type` | string | 版面元素类型（见下表） |
| `sub_type` | string | 版面元素子类型（见下表） |
| `parent` | string | 标题层级树中父节点的 layout_id，若为一级标题则 parent 为 "root" |
| `children` | list | 标题层级树中子节点的 layout_id 列表 |

**版面类型（type）**：

| 类型 | 说明 |
|------|------|
| `para` | 段落 |
| `table` | 表格 |
| `image` | 文档中的插图 |
| `head_tail` | 页面顶部（页眉/页脚） |
| `contents` | 目录 |
| `seal` | 印章 |
| `title` | 标题 |
| `formula` | 公式 |

**子类型（sub_type）**：

- **title 类**：`title_{n}`（n 级标题，如 title_2 代表二级标题）、`image_title`（图标题）、`table_title`（表标题）
- **image 类**：`chart`（统计图表）、`figure`（普通插图）、`QR_code`（二维码）、`Bar_code`（条形码）

#### 表格对象（tables[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `layout_id` | string | 与 layouts 中 type 为 table 的元素的 layout ID 对应 |
| `markdown` | string | 表格内容的 Markdown 形式 |
| `table_title_id` | list | 表格标题对应的 layout_id，默认为 null |
| `position` | list | 边框数据 [x, y, w, h]（以页面坐标为原点），版式格式时有效 |
| `cells` | list | 单元格的内版面信息，layout 类型为表格时有值 |
| `matrix` | list | 二位数组，表示表格内布局位置信息，每个元素对应 cells 列表中元素的索引 |
| `merge_table` | string | 跨页表格标记：begin（开始）、inner（中间，超过两页）、end（结束）；非跨页表格该字段为空 |

#### 图片对象（images[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `layout_id` | string | 与 layouts 中 type 为 image 的元素的 layout ID 对应 |
| `image_title_id` | list | 图片标题对应的 layout_id，默认为 null |
| `position` | list | 边框数据 [x, y, w, h] |
| `content_layouts` | list | 图片的内版面信息 |
| `data_url` | string | 图片存储链接 |
| `image_description` | string | 对统计图表进行内容解析和描述，输出结果为 JSON 字符串 |

#### 分块对象（chunks[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `chunk_id` | string | 切片的 ID |
| `content` | string | 切片的内容 |
| `type` | string | 切片类型：text 或 table |
| `meta.title` | list | chunk 所属的多级标题内容 |
| `meta.position` | list | chunk 的位置，根据分块算法有可能 chunk 跨多个页 |
| `meta.box` | list | chunk 的位置坐标 |
| `meta.page_num` | int | chunk 内容所在页数 |

## API 特性

### 异步处理流程

1. 调用提交请求接口 → 获取 `task_id`
2. 通过 `task_id` 调用获取结果接口轮询

### 轮询建议

- 提交请求后 5~10 秒开始轮询
- 轮询间隔：5 秒
- 最大轮询时间：300 秒

### QPS 限制

- 提交请求接口：2 QPS
- 获取结果接口：10 QPS

## 文件限制

| 限制项 | 说明 |
|--------|------|
| 文件大小（file_data） | ≤ 50MB，超过 50M 须使用 file_url |
| 文件大小（file_url） | PDF ≤ 300MB，非 PDF ≤ 50MB |
| URL 长度 | ≤ 1024 字节 |
| 页数限制 | PDF ≤ 2000 页 |
| 优先级 | file_data > file_url（同时存在时 file_url 字段失效） |

## 错误处理

常见错误码：

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 110/111 | access_token 无效或过期 | 重新获取 access_token |
| 216200 | 文件或 URL 为空 | 提供 file_data 或 file_url |
| 216201 | 文件格式错误 | 检查文件格式是否支持 |
| 216202 | 文件大小超限 | 缩减文件大小 |
| 282000 | 内部错误 | 重试或联系技术支持 |
| 282003 | 缺少必要参数 | 检查必填参数 |
| 282007 | 任务不存在 | 检查 task_id 是否正确 |
| 282018 | 服务繁忙 | 降低请求频率 |

完整错误码参见 `references/error_codes.md`

## 在线调试

可在 [示例代码中心](https://console.bce.baidu.com/tools/#/api?product=AI&project=%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB&parent=%E6%99%BA%E8%83%BD%E6%96%87%E6%A1%A3%E5%88%86%E6%9E%90%E5%B9%B3%E5%8F%B0&api=rest/2.0/brain/online/v2/parser/task&method=post) 申请试该接口，可进行签名验证、查看在线调用的请求内容和返回结果、示例代码的自动生成。

## 脚本

- `scripts/baidu_doc_parser.py`：文档解析主程序，支持命令行快速调用

## 参考文档

- `references/parameters.md`：完整 API 参数与返回结构详解
- `references/error_codes.md`：完整错误码参考
- `references/apikey-fetch.md`：API Key 配置指南

## 相关链接

- [官方 API 文档](https://ai.baidu.com/ai-doc/OCR/llxst5nn0)
- [百度云控制台](https://console.bce.baidu.com/ai/)
- [智能文档分析平台](https://ai.baidu.com/solution/intelligent-document-analysis)
