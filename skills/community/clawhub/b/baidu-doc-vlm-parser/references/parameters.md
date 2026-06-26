# 百度文档解析（PaddleOCR-VL）API 参数详解

## 接口概述

基于 PaddleOCR-VL-1.5-0.9B 多模态大模型，具备全要素精准解析能力，支持 111 种语言，可处理不规则布局和长文档跨页解析。

## API 接口地址

### 提交请求接口

```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task?access_token={access_token}
Content-Type: application/x-www-form-urlencoded
```

### 获取结果接口

```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task/query?access_token={access_token}
Content-Type: application/x-www-form-urlencoded
```

## 提交请求参数

### 文件参数（必选，二选一）

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| file_data | 和 file_url 二选一 | string | 文件 Base64 编码。版式文档：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd（图片最长边≤4096px）；流式文档：doc, docx, txt, wps, ppt, pptx。图片≤10M，版式文档≤100M，流式文档≤50M，PDF≤500页。超过50M须用file_url。优先级：file_data > file_url |
| file_url | 和 file_data 二选一 | string | 文件URL，≤1024字节。PDF≤100M，≤500页。请关闭URL防盗链 |
| file_name | 是 | string | 文件名，后缀须正确，如 "1.pdf" |

### 功能参数

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| recognize_formula | - | bool | **无需开启**，大模型默认识别公式 |
| analysis_chart | 否 | bool | 是否对统计图表进行解析 |
| parse_image_layout | - | bool | **无需开启**，大模型默认解析所有图片 |
| language_type | - | string | **无需开启**，大模型默认识别语种 |
| merge_tables | 否 | bool | 是否合并跨页表格 |
| relevel_titles | 否 | bool | 是否对 paragraph_title 进行分级 |
| recognize_seal | 否 | bool | 是否识别印章 |
| return_span_boxes | 否 | bool | 是否返回行坐标 |

### 文档分块参数

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| return_doc_chunks.switch | 否 | bool | False | 是否切分 |
| return_doc_chunks.chunk_size | 否 | int | -1 | 切分块大小，-1为语义自动切分 |

## 返回结构

### 获取结果返回

| 字段 | 类型 | 说明 |
|------|------|------|
| result.task_id | string | 任务 ID |
| result.status | string | pending/processing/success/failed |
| result.task_error | string | 报错信息 |
| result.markdown_url | string | Markdown 结果链接（30天有效） |
| result.parse_result_url | string | JSON 结果 BOS 链接（30天有效） |

### 版面类型（24种）

| 类型 | 说明 | 类型 | 说明 |
|------|------|------|------|
| text | 文本 | table | 表格 |
| image | 图片 | chart | 图表 |
| doc_title | 文档标题 | paragraph_title | 段落标题 |
| figure_title | 图片标题 | display_formula | 公式 |
| inline_formula | 行内公式 | formula_number | 公式编号 |
| header | 页眉 | footer | 页脚 |
| header_image | 页眉图片 | footer_image | 页脚图片 |
| number | 页码 | abstract | 摘要 |
| algorithm | 算法 | aside_text | 旁注文本 |
| content | 目录 | footnote | 脚注 |
| reference | 参考文献 | reference_content | 参考文献内容 |
| seal | 印章 | vertical_text | 竖排文本 |

## 相关文档

- [官方 API 文档](https://ai.baidu.com/ai-doc/OCR/3mi73at9o)
- [错误码参考](error_codes.md)
- [API Key 配置指南](apikey-fetch.md)
