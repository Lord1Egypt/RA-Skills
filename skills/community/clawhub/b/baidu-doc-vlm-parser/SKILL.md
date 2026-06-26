---
name: baidu-doc-vlm-parser 百度文档解析(PaddleOCR-VL)
description: 调用百度PaddleOCR-VL大模型API解析文档。基于PaddleOCR-VL-1.5多模态大模型，支持PDF、Word、PPT、图片等格式，精准识别印刷文本、手写文本、表格、公式、图表、印章等复杂元素，支持111种语言，可处理不规则布局和长文档跨页解析。触发词：文档解析、VLM解析、大模型OCR、PaddleOCR、多模态文档、手写识别、公式识别、复杂版面。
license: MIT
---

# 百度文档解析（PaddleOCR-VL）Skill

基于 PaddleOCR-VL-1.5 多模态大模型，提供开箱即用的文档智能解析能力。

## 功能概述

**PaddleOCR-VL-1.5-0.9B** 是多模态文档解析领域的 SOTA 方案，具备：

- **全要素精准解析**：高效识别印刷文本、手写文本、表格、公式、图表、印章等复杂文档元素
- **智能阅读顺序**：基于人类阅读习惯推断内容排列顺序，将零散页面信息转化为有序带标签的结构化元素序列
- **行级别坐标**：支持精准的行级别坐标输出
- **111 种语言**：覆盖中、英、日、韩、拉丁文等全球化多语种文档
- **不规则布局定位**：攻克复杂版面解析难点
- **长文档跨页解析**：支持跨页表格合并等企业级场景
- **直接 Markdown/JSON 输出**：无需额外处理

## 与文档解析（标准版）的区别

| 特性 | PaddleOCR-VL（本 Skill） | 标准版（pipeline-parser） |
|------|-------------------------|--------------------------|
| 底层模型 | 多模态大模型 VLM | 传统 Pipeline |
| 语言支持 | 111 种 | 20+ 种 |
| 公式/图片识别 | 默认开启，无需配置 | 需手动开启参数 |
| 语种识别 | 自动识别，无需指定 | 需指定 language_type |
| 版面类型 | 24 种细粒度类型 | 8 种基础类型 |
| 行坐标 | 支持 | 不支持 |
| 多边形坐标 | 支持（polygon） | 仅矩形框 |
| 文件大小 | 版式 ≤100M，PDF ≤500 页 | PDF ≤300M，≤2000 页 |

## 适用场景

当用户需要：
- 解析复杂版面文档（多栏、不规则布局）
- 精准识别手写文本、数学公式、图表
- 处理多语种混合文档
- 获取行级别坐标信息
- 长文档跨页表格合并
- 免配置自动识别文档内容

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

**版式文档**：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd（图片最长边不大于 4096px）

**流式文档**：doc, docx, txt, wps, ppt, pptx

## 支持语言

111 种语言，包括中文、英文、日文、韩文、拉丁文等，**无需手动指定，大模型自动识别**。

## 使用方式

```bash
python3 scripts/baidu_doc_vlm_parser.py --file_data <文件的base64编码> --file_name "test.pdf"
python3 scripts/baidu_doc_vlm_parser.py --file_url <文件公网URL> --file_name "test.pdf"
```

## API 接口

文档解析（PaddleOCR-VL）API 服务为异步接口，需要先调用**提交请求接口**获取 task_id，然后调用**获取结果接口**进行结果轮询。

### 提交请求接口

- **HTTP 方法**：POST
- **请求 URL**：`https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task?access_token={token}`
- **Content-Type**：`application/x-www-form-urlencoded`

### 获取结果接口

- **HTTP 方法**：POST
- **请求 URL**：`https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task/query?access_token={token}`
- **Content-Type**：`application/x-www-form-urlencoded`
- **请求参数**：`task_id`（必填，提交请求时返回的 task_id）

## 请求参数

### 文件参数（必选，二选一）

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `file_data` | 和 file_url 二选一 | string | 文件 Base64 编码数据。版式文档：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd（图片最长边不大于 4096px）；流式文档：doc, docx, txt, wps, ppt, pptx。图片不超过 10M，版式文档不超过 100M，流式文档不超过 50M，PDF 最大 500 页。超过 50M 须使用 file_url。优先级：file_data > file_url |
| `file_url` | 和 file_data 二选一 | string | 文件数据 URL，长度不超过 1024 字节。PDF 文档不超过 100M，最大 500 页。**请注意关闭 URL 防盗链** |
| `file_name` | 是 | string | 文件名，请保证文件名后缀正确，例如 "1.pdf" |

### 功能参数

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `recognize_formula` | - | bool | **无需开启**，大模型默认对版式类型文档进行公式识别 |
| `analysis_chart` | 否 | bool | 是否对统计图表进行解析 |
| `parse_image_layout` | - | bool | **无需开启**，大模型默认解析文档中的所有图片 |
| `language_type` | - | string | **无需开启**，大模型默认识别语种类型 |
| `merge_tables` | 否 | bool | 是否将跨页表格合并输出，开启后 tables 内返回跨页表格合并标识 |
| `relevel_titles` | 否 | bool | 是否对段落标题（paragraph_title）进行分级，开启后在 sub_type 中输出标题级别 |
| `recognize_seal` | 否 | bool | 是否识别印章内容 |
| `return_span_boxes` | 否 | bool | 是否返回行坐标 |

### 文档分块参数

`return_doc_chunks` 为字典类型：

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `switch` | 否 | bool | False | 是否进行文档内容切分 |
| `chunk_size` | 否 | int | -1 | 切分块的大小，-1 表示按照语义自动切分 |

## 返回结构

### 提交请求返回

| 字段 | 类型 | 说明 |
|------|------|------|
| `log_id` | uint64 | 唯一的 log id，用于问题定位 |
| `error_code` | int | 错误码 |
| `error_msg` | string | 错误描述信息 |
| `result.task_id` | string | 该请求生成的 task_id |

### 获取结果返回

| 字段 | 类型 | 说明 |
|------|------|------|
| `result.task_id` | string | 任务 ID |
| `result.status` | string | 任务状态：pending（排队中）、processing（运行中）、success（成功）、failed（失败） |
| `result.task_error` | string | 解析报错信息 |
| `result.markdown_url` | string | Markdown 格式结果链接，**有效期 30 天** |
| `result.parse_result_url` | string | JSON 格式结果 BOS 链接，**有效期 30 天** |

### 解析结果 JSON 结构（parse_result_url）

#### 页面对象（pages[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `page_id` | string | 页码 ID |
| `page_num` | int | 页码数 |
| `text` | string | 当前页所有纯文字内容 |
| `layouts` | list | 版式分析结果 |
| `tables` | list | 表格解析结果 |
| `images` | list | 图片解析结果 |
| `meta` | dict | 页面元信息（page_width, page_height） |

#### 版面元素（layouts[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `layout_id` | string | 唯一标志，格式 "xxxxx-layout-{global_layout_index}" |
| `text` | string | 文本内容（type 为 table/image 时为空） |
| `position` | list | 位置 [x, y, w, h] |
| `polygon` | list | 顶点坐标列表，可围合成多边形 |
| `span_boxes` | list | 行信息（开启 return_span_boxes 后生效），含 text 和 location |
| `type` | string | 版面元素类型（见下表） |
| `sub_type` | string | 标题层级（开启 relevel_titles 后生效） |

**版面类型（type）— 24 种细粒度类型**：

| 类型 | 说明 | 类型 | 说明 |
|------|------|------|------|
| `text` | 文本 | `table` | 表格 |
| `image` | 图片 | `chart` | 图表 |
| `doc_title` | 文档标题 | `paragraph_title` | 段落标题 |
| `figure_title` | 图片标题 | `display_formula` | 公式 |
| `inline_formula` | 行内公式 | `formula_number` | 公式编号 |
| `header` | 页眉 | `footer` | 页脚 |
| `header_image` | 页眉图片 | `footer_image` | 页脚图片 |
| `number` | 页码 | `abstract` | 摘要 |
| `algorithm` | 算法 | `aside_text` | 旁注文本 |
| `content` | 目录 | `footnote` | 脚注 |
| `reference` | 参考文献 | `reference_content` | 参考文献内容 |
| `seal` | 印章 | `vertical_text` | 竖排文本 |

#### 表格对象（tables[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `layout_id` | string | 对应 layouts 中 type 为 table 的 layout ID |
| `markdown` | string | 表格 Markdown 形式 |
| `position` | list | 边框数据 [x, y, w, h] |
| `cells` | list | 单元格内版面信息 |
| `matrix` | list | 单元格索引矩阵 |
| `merge_table` | string | 合并标识（开启 merge_tables 后）：begin（开始）、end（结束） |

#### 图片对象（images[]）

| 字段 | 类型 | 说明 |
|------|------|------|
| `layout_id` | string | 对应 layouts 中 type 为 image 的 layout ID |
| `position` | list | 边框数据 [x, y, w, h] |
| `data_url` | string | 图片存储链接 |
| `image_description` | string | 统计图表内容解析（JSON 字符串） |

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
| 图片大小 | ≤ 10M，最长边 ≤ 4096px |
| 版式文档大小 | ≤ 100M |
| 流式文档大小 | ≤ 50M |
| PDF 页数 | ≤ 500 页 |
| URL 长度 | ≤ 1024 字节 |
| 优先级 | file_data > file_url |

## 错误处理

常见错误码参见 `references/error_codes.md`

## 脚本

- `scripts/baidu_doc_vlm_parser.py`：文档解析主程序，支持命令行快速调用

## 参考文档

- `references/parameters.md`：完整 API 参数与返回结构详解
- `references/error_codes.md`：完整错误码参考
- `references/apikey-fetch.md`：API Key 配置指南

## 相关链接

- [官方 API 文档](https://ai.baidu.com/ai-doc/OCR/3mi73at9o)
- [百度云控制台](https://console.bce.baidu.com/ai/)
- [智能文档分析平台](https://ai.baidu.com/solution/intelligent-document-analysis)
