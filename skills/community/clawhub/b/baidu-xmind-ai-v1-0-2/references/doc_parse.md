# 百度智能文档分析平台 - 文档解析API

## 概述

文档解析支持对doc、pdf、图片、xlsx等18种格式文档进行解析，输出文档的版面、表格、阅读顺序、标题层级、旋转角度等信息，支持中、英、日、韩、法等20余种语言类型，可返回Markdown格式内容，将非结构化数据转化为易于处理的结构化数据，识别准确率可达 90% 以上。

## API特点

- **异步接口**：需要先调用提交请求接口获取 task_id，然后调用获取结果接口进行结果轮询
- **建议轮询时间**：提交请求后 **5～10秒** 开始轮询
- **QPS限制**：提交请求接口 2 QPS，获取结果接口 10 QPS

## 支持的文件格式

### 版式文档
- PDF、JPG、JPEG、PNG、BMP、TIF、TIFF、OFD、PPT、PPTX
- **大小限制**：不超过50M，PDF最大2000页
- **超过50M**：须使用file_url方式上传

### 流式文档
- DOC、DOCX、TXT、XLS、XLSX、WPS、HTML、MHTML
- **大小限制**：不超过50M

## 提交请求接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/parser/task?access_token={access_token}
```

**请求参数**：

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| file_data | 二选一 | string | 文件base64编码（优先级高于file_url） |
| file_url | 二选一 | string | 文件URL，长度不超过1024字节 |
| file_name | 是 | string | 文件名，必须保证后缀正确，如 "1.pdf" |
| recognize_formula | 否 | bool | 是否公式识别 |
| analysis_chart | 否 | bool | 是否图表解析 |
| angle_adjust | 否 | bool | 是否图片矫正 |
| parse_image_layout | 否 | bool | 是否返回图片位置信息 |
| language_type | 否 | string | 识别语种（默认CHN_ENG） |
| switch_digital_width | 否 | string | 数字全半角转换（auto/half/full） |
| html_table_format | 否 | bool | 表格转HTML格式（默认True） |
| return_doc_chunks | 否 | dict | 返回文档切分片段 |

### language_type 可选值

| 值 | 说明 |
|-----|------|
| CHN_ENG | 中英文（默认） |
| JAP | 日语 |
| KOR | 韩语 |
| FRE | 法语 |
| SPA | 西班牙语 |
| POR | 葡萄牙语 |
| GER | 德语 |
| ITA | 意大利语 |
| RUS | 俄语 |
| DAN | 丹麦语 |
| DUT | 荷兰语 |
| MAL | 马来语 |
| SWE | 瑞典语 |
| IND | 印尼语 |
| POL | 波兰语 |
| ROM | 罗马尼亚语 |
| TUR | 土耳其语 |
| GRE | 希腊语 |
| HUN | 匈牙利语 |
| THA | 泰语 |
| VIE | 越南语 |
| ARA | 阿拉伯语 |
| HIN | 印地语 |

### switch_digital_width 可选值

| 值 | 说明 |
|-----|------|
| auto | 不转换，按模型识别结果输出（默认） |
| half | 转换为半角 |
| full | 转换为全角 |

### return_doc_chunks 参数

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| switch | 否 | bool | 是否进行文档内容切分（默认False） |
| split_type | 否 | string | 切分方式：chunk/mark（默认chunk） |
| separators | 否 | list | 切分标点（默认['。', '；', '！', '？', ';', '!', '?']） |
| chunk_size | 否 | int | 切分块大小（-1表示自动切分） |

## 获取结果接口

**请求URL**：
```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/parser/task/query?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| task_id | string | 是 | 提交请求返回的任务ID |

## 返回结果说明

| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务ID |
| status | string | 任务状态：success/failed |
| task_error | string | 错误信息 |
| duration | float | 处理时长（秒） |
| parse_result_url | string | 解析结果下载地址 |
| pages | array | 页面列表 |
| chunks | array | 文档切分片段（可选） |

## 使用示例

### 命令行

```bash
# 基础解析
python scripts/baidu_doc_cli.py parse --file document.pdf

# 完整参数
python scripts/baidu_doc_cli.py parse \
  --file document.pdf \
  --recognize-formula \
  --analysis-chart \
  --angle-adjust \
  --parse-image-layout \
  --language-type CHN_ENG \
  --switch-digital-width auto \
  --html-table-format

# 文档切分
python scripts/baidu_doc_cli.py parse \
  --file document.pdf \
  --return-doc-chunks \
  --split-type chunk \
  --chunk-size 500
```

### Python调用

```python
from baidu_api_client import BaiduDocAIClient

client = BaiduDocAIClient()

# 基础调用
result = client.parse(
    file_data=file_data,
    file_name="document.pdf"
)

# 完整参数
result = client.parse(
    file_data=file_data,
    file_name="document.pdf",
    recognize_formula=True,
    analysis_chart=True,
    angle_adjust=True,
    parse_image_layout=True,
    language_type="CHN_ENG",
    switch_digital_width="auto",
    html_table_format=True,
    return_doc_chunks={
        "switch": True,
        "split_type": "chunk",
        "chunk_size": -1
    }
)
```

## 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 282003 | 缺少参数 | 检查必填参数 |
| 282007 | 任务不存在 | 检查task_id是否正确 |
| 282000 | 内部错误 | 重试或联系技术支持 |

## 参考链接

- [智能文档分析平台控制台](https://console.bce.baidu.com/textmind/application/textParser)
- [官方API文档](https://ai.baidu.com/ai-doc/OCR/llxst5nn0)
