# 百度智能文档分析平台 - 文档抽取API

## 概述

文档抽取支持自定义配置字段，无需训练即可抽取文档字段信息，精准定位字段值，适用于合同、票据、订单等各类文档场景。

## API特点

- **异步接口**：需要先调用提交请求接口获取 taskId，然后调用获取结果接口进行结果轮询
- **建议轮询时间**：提交请求后 **30秒** 开始轮询
- **QPS限制**：提交请求接口 2 QPS，获取结果接口 10 QPS

## 支持的文件格式

- 图片：jpg/jpeg/png/bmp/tif/tiff
- 文档：doc/docx/pdf/xlsx/xls/ofd
- 文件大小：不超过 50M
- 图像最短边至少 15px，最长边最大 4096px

## 提交请求接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/brain/online/v1/extract/task?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| file | string | 和 fileURLs 二选一 | 文件的base64编码，需去掉编码头 |
| fileURLs | string | 和 file 二选一 | 文件数据URL，URL长度不超过1024字节 |
| fileName | string | file不为空时必传 | 文档名称，例如 test.docx |
| manifestVersionId | string | 和 manifest 二选一 | 用户在智能文档分析平台配置的清单版本id |
| manifest | string | 和 manifestVersionId 二选一 | 抽取字段配置（JSON格式） |
| removeDuplicates | bool | 否 | 是否开启字段值去重 |
| pageRange | string | 否 | 指定页抽取，如: 1,5-10,15 |
| extractSeal | bool | 否 | 是否开启印章抽取 |
| eraseWatermark | bool | 否 | 是否开启水印去除 |
| docCorrect | bool | 否 | 是否开启图像矫正 |

### manifest 字段格式

```json
[
  {
    "parentKey": "root",
    "key": "字段名称",
    "description": "字段说明（可选，辅助大模型提升抽取效果）"
  },
  {
    "parentKey": "父字段",
    "key": "子字段",
    "description": ""
  }
]
```

**字段命名规则**：
- 支持中英文、数字、下划线、中划线、斜杠、冒号和括号
- 中横线、下划线、斜杠和冒号不能作为开头和结尾
- key和parentKey字符数不超过30
- description字符数不超过100
- key的数量不能超过100

### pageRange 格式说明

- 页码从1开始
- 使用英文逗号分隔单个页码
- 用连字符表示页码范围
- 例如：`1,5-10,15` 表示抽取第1页、第5至10页和第15页

### 参数优先级

- **文件参数**：file > fileURLs
- **抽取字段配置**：manifestVersionId > manifest

**返回示例**：
```json
{
  "error_code": 0,
  "error_msg": "",
  "log_id": "088d6639-bafd-4007-be27-dcddbb651322",
  "result": {
    "taskId": "task-6tb7mgduz9rqaxzi"
  }
}
```

## 获取结果接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/brain/online/v1/extract/query_task?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| taskId | string | 是 | 提交请求返回的任务ID |

**返回参数**：

| 字段 | 类型 | 说明 |
|------|------|------|
| taskId | string | 任务ID |
| status | string | 任务状态：Success/Failed |
| reason | string | 失败原因 |
| extractLabelInfo | array | 抽取字段配置 |
| extractResult | array | 抽取结果列表 |

**extractResult 结构**：
```json
{
  "docId": "文档ID",
  "docName": "文档名称",
  "pdfUrl": "文档下载地址",
  "data": {
    "singleKey": {
      "字段名": [{
        "word": "字段值",
        "valuePositions": [{
          "box": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]],
          "cbox": [x, y, width, height],
          "pageNo": 页码
        }]
      }]
    },
    "comboKey": {
      "父字段名": [{
        "子字段名1": {...},
        "子字段名2": {...}
      }]
    }
  }
}
```

## 前端SDK渲染

**URL格式**：
```
https://textmind-sdk.bce.baidu.com/textmind/sdk/textExtract/{taskId}?access_token={access_token}
```

**iframe引入方式**：
```html
<iframe src="https://textmind-sdk.bce.baidu.com/textmind/sdk/textExtract/{taskId}?access_token={access_token}" />
```

## 使用示例

参见脚本：`scripts/doc_extract.py`

### 基础用法

```bash
# 使用文件URL
python scripts/doc_extract.py --file_url "文档URL" --fields '[{"key": "合同金额"}]'

# 使用文件base64编码
python scripts/doc_extract.py --file_data "base64编码" --file_name "document.pdf" --fields '[{"key": "合同金额"}]'

# 使用清单版本ID
python scripts/doc_extract.py --file_url "文档URL" --manifest_version_id "清单版本ID"
```

### 高级用法

```bash
# 开启印章抽取和水印去除
python scripts/doc_extract.py --file_url "文档URL" --fields '[{"key": "合同金额"}]' \
  --extract_seal --erase_watermark

# 指定页码抽取
python scripts/doc_extract.py --file_url "文档URL" --fields '[{"key": "合同金额"}]' \
  --page_range "1,5-10,15"

# 开启所有增强功能
python scripts/doc_extract.py --file_url "文档URL" --fields '[{"key": "合同金额"}]' \
  --remove_duplicates \
  --extract_seal \
  --erase_watermark \
  --doc_correct
```

## 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 283016 | 参数格式错误 | 检查字段名称格式 |
| 282000 | 内部错误 | 重试或联系技术支持 |

## 参考链接

- [智能文档分析平台控制台](https://console.bce.baidu.com/textmind/application/textExtract)
- [官方API文档](https://ai.baidu.com/ai-doc/OCR/klzkwzdch)
