# 百度智能文档分析平台 - 文档格式转换API

## 概述

文档格式转换可识别图片/PDF文档版面布局，提取文字内容，并转换为保留原文档版式的Word、Excel文档。

## API特点

- **异步接口**：需要先提交请求获取 task_id，然后轮询结果
- **建议轮询时间**：提交请求后 5～10 秒开始轮询
- **QPS限制**：提交请求接口 2 QPS，获取结果接口 10 QPS

## 支持的文件格式

- 图片：jpg/jpeg/png/bmp
- PDF文档
- 文件大小：base64编码后不超过4M（图片）/ 10M（PDF）

## 提交请求接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/ocr/v1/doc_convert/request?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| image | string | 三选一 | 图片base64编码 |
| url | string | 三选一 | 图片URL |
| pdf_file | string | 三选一 | PDF文件base64编码 |
| pdf_file_num | string | 否 | PDF页码，不传则识别所有页 |

## 获取结果接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/ocr/v1/doc_convert/get_request_result?access_token={access_token}
```

## 返回结果说明

### 主要返回字段

| 字段 | 说明 |
|------|------|
| ret_code | 识别状态：1-未开始，2-进行中，3-已完成 |
| percent | 转换进度（百分比） |
| result_data.word | Word文档下载地址 |
| result_data.excel | Excel文档下载地址 |

## 使用示例

参见脚本：`scripts/doc_convert.py`

## 参考链接

- [官方API文档](https://ai.baidu.com/ai-doc/OCR/Elf3sp7cz)
- [智能文档分析平台](https://console.bce.baidu.com/textmind/application/converter/)
