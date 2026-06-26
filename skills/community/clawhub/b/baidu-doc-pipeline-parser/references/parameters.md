# 百度文档解析 API 参数详解

## 接口概述

百度文档解析 API 支持对 doc、pdf、图片、xlsx 等 18 种格式文档进行解析，输出文档的版面、表格、阅读顺序、标题层级、旋转角度等信息，支持中、英、日、韩、法等 20 余种语言类型，识别准确率可达 90% 以上。

## API 接口地址

### 提交请求接口

```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/parser/task?access_token={access_token}
Content-Type: application/x-www-form-urlencoded
```

### 获取结果接口

```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/parser/task/query?access_token={access_token}
Content-Type: application/x-www-form-urlencoded
```

## 提交请求参数

### 文件参数（必选，二选一）

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| file_data | 和 file_url 二选一 | string | 文件的 base64 编码数据。版式文档：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd, ppt, pptx；流式文档：doc, docx, txt, xls, xlsx, wps, html, mhtml。文档大小不超过 50M，其中 PDF 文档最大支持 2000 页。若文档大小超过 50M，须从 file_url 方式上传。优先级：file_data > file_url，当 file_data 字段存在时，file_url 字段失效 |
| file_url | 和 file_data 二选一 | string | 文件数据 URL，URL 长度不超过 1024 字节，支持单个 URL 传入。PDF 文档大小不超过 300MB，非 PDF 文档大小不超过 50M，其中 PDF 文档最大支持 2000 页。优先级：file_data > file_url。**请注意关闭 URL 防盗链** |
| file_name | 是 | string | 文件名，请保证文件名后缀正确，例如 "1.pdf" |

### 核心功能参数

| 参数 | 必选 | 类型 | 可选值范围 | 说明 |
|------|------|------|----------|------|
| recognize_formula | 否 | bool | True/False | 是否对版式类型文档进行公式识别 |
| analysis_chart | 否 | bool | True/False | 是否对统计图表进行解析 |
| angle_adjust | 否 | bool | True/False | 是否对图片进行角度矫正 |
| parse_image_layout | 否 | bool | True/False | 是否返回文档中的图片位置信息 |

### 语言与格式参数

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| language_type | 否 | string | CHN_ENG | 识别语种类型 |
| switch_digital_width | 否 | string | auto | 是否对数字进行全半角转换。auto：不转换；half：半角输出；full：全角输出 |
| html_table_format | 否 | bool | True | 是否将识别出的表格转换为 HTML 格式返回 |

### 支持语种列表

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| CHN_ENG | 中英文 | DAN | 丹麦语 |
| JAP | 日语 | DUT | 荷兰语 |
| KOR | 韩语 | MAL | 马来语 |
| FRE | 法语 | SWE | 瑞典语 |
| SPA | 西班牙语 | IND | 印尼语 |
| POR | 葡萄牙语 | POL | 波兰语 |
| GER | 德语 | ROM | 罗马尼亚语 |
| ITA | 意大利语 | TUR | 土耳其语 |
| RUS | 俄语 | GRE | 希腊语 |
| HUN | 匈牙利语 | THA | 泰语 |
| VIE | 越南语 | ARA | 阿拉伯语 |
| HIN | 印地语 | - | - |

### 文档分块参数

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| return_doc_chunks | 否 | dict | - | 是否返回文档切分后的片段数据（按语义、字数、标点） |
| + switch | 否 | bool | False | 是否进行文档内容切分 |
| + split_type | 否 | str | chunk | 切分方式。chunk：按照 chunk_size 来切；mark：按照 separators 来切 |
| + separators | 否 | list | ['。','；','！','？',';','!','?'] | 切分标点 |
| + chunk_size | 否 | int | -1 | 切分块的大小，-1 表示按照语义自动切分，不限定块的大小 |

## 获取结果请求参数

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 发送提交请求时返回的 task_id |

## 返回结构

### 提交请求返回

| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | uint64 | 唯一的 log id，用于问题定位 |
| error_code | int | 错误码 |
| error_msg | string | 错误描述信息 |
| result | dict | 返回的结果列表 |
| + task_id | string | 该请求生成的 task_id，后续使用该 task_id 获取结果 |

成功返回示例：

```json
{
  "error_code": 0,
  "error_msg": "",
  "log_id": "10138598131137362685273585665433",
  "result": {
    "task_id": "task-3zy9Bg8CHt1M4pP0cX2q5bg28j268015"
  }
}
```

### 获取结果返回

| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | uint64 | 唯一的 log id，用于问题定位 |
| error_code | int | 错误码 |
| error_msg | string | 错误描述信息 |
| result | dict | 返回的结果列表 |
| + task_id | string | 任务 ID |
| + status | string | 任务状态：pending（排队中）、processing（运行中）、success（成功）、failed（失败） |
| + task_error | string | 解析报错信息，包含任务失败、额度不够 |
| + markdown_url | string | 文档解析结果的 Markdown 格式链接，链接有效期 30 天 |
| + parse_result_url | string | 文档解析结果的 BOS 链接，链接有效期 30 天 |

成功返回示例：

```json
{
  "error_code": 0,
  "error_msg": "",
  "result": {
    "task_id": "task-UnvGsgbYZp9pS3BZRHn11ifzjNvKzTgf",
    "status": "success",
    "task_error": null,
    "duration": 902.0,
    "parse_result_url": "https://xxxxxxxxxxxxxxxxxx"
  }
}
```

### parse_result_url 返回的 JSON 结构

通过 `parse_result_url` 下载解析结果的 JSON 文件，结构如下：

#### 顶层结构

| 字段 | 类型 | 说明 |
|------|------|------|
| file_name | string | 文档名称 |
| file_id | string | 文档 ID |
| pages | list | 文件单页解析内容 |
| chunks | list | 文件内容切分结果（return_doc_chunks 中 switch 为 True 时有值） |

#### 页面对象（pages[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| page_id | string | 页码 ID |
| page_num | int | 页码数 |
| text | string | 当前页的所有纯文字内容 |
| layouts | list | 页面内容版式分析的结果 |
| tables | list | 页面表格解析结果 |
| images | list | 页面中图片解析结果 |
| meta | dict | 页元信息 |

#### 页面元信息（meta）

| 字段 | 类型 | 说明 |
|------|------|------|
| page_width | int | 页面宽度 |
| page_height | int | 页面高度 |
| is_scan | bool | 是否扫描件 |
| page_angle | int | 页面倾斜角度 |
| page_type | string | 页面属性：text（正文）、contents（目录）、appendix（附录）、others（其他） |
| sheet_name | string | Excel 的 sheet 名 |

#### 版面元素（layouts[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| layout_id | string | layout 元素唯一标志，以 "xxxxx-layout-{global_layout_index}" 形式，global_layout_index 为 layout 元素整个文档的全局索引 |
| text | string | layout 对应的文本内容。注：当 type 为 table、image 时该字段为空，需根据 type 和 layout_id 分别到 tables、images 字段里找到对应的内容 |
| position | list | layout 元素在页面中的位置，[x, y, w, h] box 框，左上角和宽高 |
| type | string | 版面元素类型（见下表） |
| sub_type | string | 版面元素子类型（见下表） |
| parent | string | 标题层级树中父节点的 layout_id，若当前 layout 为一级标题，其 parent 为 "root"。在 table 和 image 的内版面信息中暂时都为空 |
| children | list | 标题层级树中子节点的 layout_id。在 table 和 image 的内版面信息中暂时都为空 |

**版面类型（type）取值**：

| 类型 | 说明 |
|------|------|
| para | 段落 |
| table | 表格 |
| image | 文档中的插图 |
| head_tail | 页面顶部 |
| contents | 目录 |
| seal | 印章 |
| title | 标题 |
| formula | 公式 |

**子类型（sub_type）取值**：

当 type 为 title 或 image 时，sub_type 有值：

- **title 的 sub_type**：
  - `title_{n}`：代表 n 级标题，比如 title_2 代表二级标题
  - `image_title`：图标题
  - `table_title`：表标题

- **image 的 sub_type**：
  - `chart`：统计图表
  - `figure`：普通插图
  - `QR_code`：二维码
  - `Bar_code`：条形码

#### 表格对象（tables[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| layout_id | string | layout ID，与 layouts 中的 type 为 table 的元素的 layout ID 对应 |
| markdown | string | 表格内容的 Markdown 形式 |
| table_title_id | list | 表格标题对应的 layout_id，默认为 null |
| position | list | 边框数据 [x, y, w, h]（以页面坐标为原点），版式格式时有效 |
| cells | list | 单元格的内版面信息，layout 类型为表格时有值 |
| matrix | list | 二位数组，表示表格内布局位置信息，每个元素对应 cells 列表中元素的索引 |
| merge_table | string | 跨页表格标记："begin"（开始）、"inner"（中间，表格跨页超过两页）、"end"（结束）；非跨页表格该字段为空 |

#### 图片对象（images[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| layout_id | string | layout ID，与 layouts 中 type 为 image 的元素的 layout ID 对应 |
| image_title_id | list | 图片标题对应的 layout_id，默认为 null |
| position | list | 边框数据 [x, y, w, h] |
| content_layouts | list | 图片的内版面信息 |
| data_url | string | 图片存储链接 |
| image_description | string | 对统计图表进行内容解析和描述，输出结果为 JSON 字符串，可通过 json.loads 结构化为 JSON 格式 |

#### 分块对象（chunks[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| chunk_id | string | 切片的 ID |
| content | string | 切片的内容 |
| type | string | 切片类型，为 text 或者 table |
| meta | dict | chunk 元信息 |
| + title | list | chunk 所属的多级标题内容 |
| + position | list | chunk 的位置，根据分块算法有可能 chunk 跨多个页 |
| + box | list | chunk 的位置坐标 |
| + page_num | int | chunk 内容所在页数 |

## 文件限制

| 限制项 | 说明 |
|--------|------|
| 文件大小（file_data） | ≤ 50MB，超过 50M 须使用 file_url |
| 文件大小（file_url） | PDF ≤ 300MB，非 PDF ≤ 50MB |
| URL 长度 | ≤ 1024 字节 |
| 页数限制 | PDF ≤ 2000 页 |
| 优先级 | file_data > file_url（同时存在时 file_url 字段失效） |

## QPS 限制

- 提交请求接口：2 QPS
- 获取结果接口：10 QPS

## 轮询建议

- 提交请求后 5~10 秒开始轮询
- 轮询间隔：5 秒
- 最大轮询时间：300 秒

## 相关文档

- [官方 API 文档](https://ai.baidu.com/ai-doc/OCR/llxst5nn0)
- [错误码参考](error_codes.md)
- [API Key 配置指南](apikey-fetch.md)
