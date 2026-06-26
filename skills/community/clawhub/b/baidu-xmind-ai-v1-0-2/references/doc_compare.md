# 百度智能文档分析平台 - 文档比对API

## 概述

文档比对支持精准比对文档的增删改差异，快速定位并高亮显示差异原文，支持导出完整的比对报告。

## API特点

- **异步接口**：需要先提交请求获取 taskId，然后轮询结果
- **建议轮询时间**：提交请求后 5～10 秒开始轮询
- **QPS限制**：提交请求接口 2 QPS，获取结果接口 10 QPS

## 支持的文件格式

- 图片：bmp/jpg/jpeg/png/tif/tiff
- 文档：doc/docx/wps/pdf/ofd
- 文件大小：不超过 50M

## 提交请求接口

**请求URL**：
```
POST https://aip.baidubce.com/file/2.0/brain/online/v1/textdiff/create_task?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| baseFile | file | 二选一 | 主版比对文档 |
| baseFileURL | string | 二选一 | 主版文档URL |
| compareFile | file | 二选一 | 副版比对文档 |
| compareFileURL | string | 二选一 | 副版文档URL |
| param | dict | 否 | 特殊差异识别参数 |

**param 参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| sealRecognition | bool | 是否识别印章差异（默认false） |
| fullWidthHalfWidthRecognition | bool | 是否识别中英文符号差异（默认false） |
| fontFamilyRecognition | bool | 是否识别字体差异（默认false） |
| fontSizeRecognition | bool | 是否识别字号差异（默认false） |
| handWritingRecognition | bool | 是否识别手写体差异（默认false） |

## 获取结果接口

**请求URL**：
```
POST https://aip.baidubce.com/file/2.0/brain/online/v1/textdiff/query_task?access_token={access_token}
```

## 返回结果说明

### 主要返回字段

| 字段 | 说明 |
|------|------|
| similarity | 两份文档的相似度 |
| totalDiff | 差异点数量 |
| diffItemList | 差异详情列表 |
| reportOssURL | 比对报告下载地址 |

### 差异类型

- `insert`：新增
- `delete`：删除
- `replace`：替换

## 前端SDK渲染

**URL格式**：
```
https://textmind-sdk.bce.baidu.com/textmind/sdk/textdiff/{taskId}?access_token={access_token}
```

## 使用示例

参见脚本：`scripts/doc_compare.py`

## 参考链接

- [官方API文档](https://ai.baidu.com/ai-doc/OCR/Glqd7jgmf)
- [智能文档分析平台](https://console.bce.baidu.com/textmind/application/textDiff/)
