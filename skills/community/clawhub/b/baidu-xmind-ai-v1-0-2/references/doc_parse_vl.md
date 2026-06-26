# 百度智能文档分析平台 - 文档解析(PaddleOCR-VL) API

## 概述

PaddleOCR-VL-1.5-0.9B：多模态文档解析领域的 SOTA 方案，具备全要素精准解析能力，可高效识别印刷文本、手写文本、表格、公式、图表、印章等复杂文档元素。

## 特点

- **全要素解析**：印刷文本、手写文本、表格、公式、图表、印章
- **多语言支持**：支持中、英、日、韩、拉丁文等 111 种语言
- **智能排序**：基于人类阅读习惯推断内容排列顺序
- **精准坐标**：支持行级别坐标精准输出
- **跨页表格**：支持长文档跨页表格合并

## API特点

- **异步接口**：需要先提交请求获取 task_id，然后轮询结果
- **建议轮询时间**：提交请求后 5～10 秒开始轮询
- **QPS限制**：提交请求接口 2 QPS，获取结果接口 10 QPS

## 支持的文件格式

- 版式文档：pdf、jpg、jpeg、png、bmp、tif、tiff
- 图片最长边不大于 4096px
- 文档大小不超过 100M
- PDF 文档最大支持 500 页

## 提交请求接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| file_data | string | 二选一 | 文件的base64编码数据 |
| file_url | string | 二选一 | 文件数据URL |
| file_name | string | 是 | 文件名，请保证文件名后缀正确 |
| analysis_chart | bool | 否 | 是否对统计图表进行解析 |
| merge_tables | bool | 否 | 是否将跨页表格合并输出 |
| relevel_titles | bool | 否 | 是否对段落标题进行分级 |
| recognize_seal | bool | 否 | 是否识别印章内容 |
| return_span_boxes | bool | 否 | 是否返回行坐标 |

## 获取结果接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task/query?access_token={access_token}
```

## 返回结果说明

### 主要返回字段

| 字段 | 说明 |
|------|------|
| task_id | 任务ID |
| status | 任务状态 |
| markdown_url | Markdown格式结果链接 |
| parse_result_url | 完整解析结果JSON链接 |

### 解析结果结构

解析结果包含：

- **pages**: 页面列表
  - **layouts**: 版面元素列表
    - type: 元素类型（title/text/table/image/formula/seal等）
    - text: 文本内容
    - position: 位置坐标
  - **tables**: 表格列表
    - markdown: Markdown格式表格
    - cells: 单元格列表
    - matrix: 单元格布局矩阵
  - **images**: 图片列表
  - **meta**: 页面元信息

### Layout 类型

| 类型 | 说明 |
|------|------|
| abstract | 摘要 |
| text | 文本 |
| title | 标题 |
| paragraph_title | 段落标题 |
| table | 表格 |
| image | 图片 |
| display_formula | 公式 |
| seal | 印章 |
| header | 页眉 |
| footer | 页脚 |
| footnote | 脚注 |
| reference | 参考文献 |

## 使用示例

参见脚本：`scripts/doc_parse_vl.py`

```bash
# 基础用法
python scripts/doc_parse_vl.py --file_url "文档URL" --file_name "document.pdf"

# 启用所有高级功能
python scripts/doc_parse_vl.py --file_url "文档URL" --file_name "document.pdf" \
  --analysis_chart --merge_tables --relevel_titles --recognize_seal --return_span_boxes
```

## 参考链接

- [官方API文档](https://ai.baidu.com/ai-doc/OCR/3mi73at9o)
- [智能文档分析平台](https://console.bce.baidu.com/textmind/application/textParser)
