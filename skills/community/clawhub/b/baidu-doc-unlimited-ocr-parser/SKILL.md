---
name: baidu-doc-Unlimited-OCR-parser 百度文档解析(Unlimited-OCR)
description: 调用百度 Unlimited-OCR API 解析文档，基于 Unlimited-OCR 开源方案的标准化服务，开箱即用免部署，直接返回 Markdown 结构化结果。支持 PDF、Word、PPT、图片等格式，适合复杂表格、多段落、多结构文档解析。触发词：文档解析、Unlimited-OCR、大模型 OCR、Markdown 解析、免部署 OCR、复杂表格、结构化文档。
license: MIT
---

# 百度文档解析（Unlimited-OCR）Skill

基于 **Unlimited-OCR** 开源方案的标准化 API 服务，无需部署即可调用，直接返回 Markdown 结构化结果。

## 功能概述

**Unlimited-OCR** 是基于开源方案打造的文档解析 API，具备：

- **开箱即用**：无需自行部署模型，云端一键调用
- **Markdown 直出**：解析结果为 Markdown 结构化文本，内嵌 HTML `<table>` 支持复杂表格（rowspan/colspan、居中、换行）
- **异步任务架构**：提交任务 → 轮询结果，适合批量处理
- **多格式支持**：PDF、Word、PPT、图片等主流格式
- **长文档友好**：单 PDF 最大 500 页

## 适用场景

当用户需要：
- 快速将 PDF/图片/Word/PPT 转换为 Markdown
- 处理含复杂表格（合并单元格、多层表头）的文档
- 免部署快速集成 OCR 能力
- 结构化解析长文档

## 与 PaddleOCR-VL 的区别

| 特性 | Unlimited-OCR（本 Skill） | PaddleOCR-VL |
|------|-------------------------|--------------|
| 输出格式 | Markdown（含 HTML 表格） | Markdown + 结构化 JSON（版面/坐标/图片） |
| 版面结构信息 | 不返回细粒度版面 | 返回 24 种版面元素及位置坐标 |
| 表格 | HTML `<table>`（Markdown 内嵌） | 独立 `tables[]` 对象，含 cells/matrix |
| 印章/公式/图表专项 | 不专门标注 | 支持 seal/formula/chart 类型识别 |
| 计费 | **限时免费** | 按页计费（见对应 Skill） |
| 复杂度 | 简单直接 | 更细粒度、可编程 |
| 适用 | 快速 Markdown 转换 | 需要结构化数据/位置信息 |
## 免费资源领取和计费说明
[百度智能文档分析平台 领取免费测试资源](https://cloud.baidu.com/doc/OCR/s/fk3h7xu7h)


[百度智能文档分析平台计费与购买方式](https://cloud.baidu.com/doc/OCR/s/Fls06fa15#%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90%EF%BC%88paddleocr-vl%EF%BC%89)


| 用户类型 | 免费额度 |
|---------|---------|
| 个人实名认证用户 | **200 页** |
| 企业实名认证用户 | **1000 页** |

## API 配置

### 额度获取方式

您可通过百度智能云平台获取[免费额度](https://cloud.baidu.com/doc/OCR/s/fk3h7xu7h)与[购买调用资源](https://cloud.baidu.com/doc/OCR/s/Fls06fa15#%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90%EF%BC%88paddleocr-vl%EF%BC%89)

### 环境变量（必须）

使用前请设置以下环境变量：

```bash
export BAIDU_DOC_AI_API_KEY="your_api_key"
export BAIDU_DOC_AI_SECRET_KEY="your_secret_key"
```

### 认证方式

通过 API Key 和 Secret Key 换取 access_token（OAuth 2.0，有效期 30 天）。所有接口请求需以 URL 参数 `access_token` 携带。

OAuth Token 端点：`https://aip.baidubce.com/oauth/2.0/token`（`grant_type=client_credentials`）

## 支持格式

**版式文档**：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd（图片最长边不大于 8192px）

**流式文档**：doc, docx, txt, wps, ppt, pptx

## 使用方式

```bash
python3 scripts/baidu_doc_unlimited_ocr_parser.py --file_data <文件的base64编码> --file_name "test.pdf"
python3 scripts/baidu_doc_unlimited_ocr_parser.py --file_url <文件公网URL> --file_name "test.pdf"
```

## API 接口

Unlimited-OCR 是**异步接口**，需先调用**提交请求接口**获取 task_id，再调用**获取结果接口**轮询结果。

### 提交请求接口

- **HTTP 方法**：POST
- **请求 URL**：`https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task?access_token={token}`
- **Content-Type**：`application/x-www-form-urlencoded`

#### Python 示例

```python
import base64
import os
import requests

API_KEY = "你的API_KEY"
SECRET_KEY = "你的SECRET_KEY"
FILE_PATH = "./test.pdf"


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    return requests.get(url, params=params, timeout=30).json()["access_token"]


def create_task(url, file_path):
    with open(file_path, "rb") as f:
        file_data = base64.b64encode(f.read()).decode()
    data = {
        "file_data": file_data,
        "file_name": os.path.basename(file_path),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(url, headers=headers, data=data, timeout=120)


if __name__ == "__main__":
    access_token = get_access_token()
    url = (
        "https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task"
        f"?access_token={access_token}"
    )
    response = create_task(url, FILE_PATH)
    print(response.json())
```

**成功响应示例：**

```json
{
  "error_code": 0,
  "error_msg": "",
  "log_id": "10138598131137362685273505665433",
  "result": { "task_id": "taREDACTED-SECRET" }
}
```

**失败响应示例：**

```json
{
  "error_code": 282003,
  "error_msg": "missing parameters",
  "log_id": "37507631033585544507983253924141",
  "result": "null"
}
```

### 获取结果接口

- **HTTP 方法**：POST
- **请求 URL**：`https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task/query?access_token={token}`
- **Content-Type**：`application/x-www-form-urlencoded`
- **请求参数**：`task_id`（必填，提交时返回的 task_id）

#### Python 示例

```python
import requests


def query_task(url, task_id):
    data = {"task_id": task_id}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(url, headers=headers, data=data, timeout=60)


access_token = "your_access_token"
url = (
    "https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task/query"
    f"?access_token={access_token}"
)
print(query_task(url, "task_id").json())
```

**成功响应示例：**

```json
{
  "log_id": "23596597899286921761579365582373",
  "error_code": 0,
  "error_msg": "",
  "result": {
    "task_id": "taREDACTED-SECRET",
    "status": "success",
    "task_error": null,
    "markdown_url": "https://xxxxxxxxxxxxxxxxxxx",
    "parse_result_url": "https://xxxxxxxxxxxxxxxxxxx"
  }
}
```

**失败响应示例：**

```json
{
  "log_id": "13665091038742503867108513247608",
  "error_code": "282007",
  "error_msg": "task not exist, please check task id",
  "result": "null"
}
```

## 请求参数

### 文件参数（必选，二选一）

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `file_data` | 和 file_url 二选一 | string | 文件 Base64 编码数据。版式文档：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd（图片最长边不大于 8192px）；流式文档：doc, docx, txt, wps, ppt, pptx。图片≤10M，版式文档≤100M，流式文档≤50M，PDF≤500 页。超过 50M 须使用 file_url。**优先级：file_data > file_url** |
| `file_url` | 和 file_data 二选一 | string | 文件数据 URL，长度不超过 1024 字节。PDF 文档大小不超过 100M，最大支持 500 页。**请注意关闭 URL 防盗链** |
| `file_name` | 是 | string | 文件名，请保证文件名后缀正确，例如 "1.pdf" |

### 图像预处理参数（可选）

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `angle_adjust` | 否 | bool | True | 是否对图片进行角度矫正 |
| `angle_mode` | 否 | string | direction | 角度矫正模式，开启角度矫正后生效。可选：direction（四方向）、arbitrary（任意方向） |
| `erase_seal` | 否 | bool | False | 是否进行印章擦除 |
| `erase_watermark` | 否 | bool | False | 是否进行水印擦除 |
| `unwarp` | 否 | bool | False | 是否进行图像扭曲矫正 |

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
| `log_id` | uint64 | 唯一的 log id，用于问题定位 |
| `error_code` | int | 错误码 |
| `error_msg` | string | 错误描述信息 |
| `result.task_id` | string | 任务 ID |
| `result.status` | string | 任务状态：pending（排队中）、running（运行中）、success（成功）、failed（失败） |
| `result.task_error` | string | 解析报错信息（任务失败、额度耗尽等） |
| `result.markdown_url` | string | Markdown 格式结果链接，**有效期 30 天** |
| `result.parse_result_url` | string | JSON 格式结果 BOS 链接，**有效期 30 天** |

### 解析结果格式

- **主输出**：`markdown_url` 指向的 Markdown 文件，包含结构化文本；复杂表格以 HTML `<table>` 元素内嵌（支持 rowspan/colspan、居中、换行等样式），可直接渲染。
- **辅助输出**：`parse_result_url` 指向的 JSON 文件（未来能力扩展保留）。

## API 特性

### 异步处理流程

1. 调用提交请求接口 → 获取 `task_id`
2. 通过 `task_id` 调用获取结果接口轮询
3. `status=success` 后从 `markdown_url` 下载 Markdown 结果

### 轮询建议

- 提交请求后 **5~10 秒**开始轮询
- 轮询间隔：**5 秒**
- 最大轮询时间：**300 秒**

### QPS 限制

- 提交请求接口：**2 QPS**
- 获取结果接口：**5 QPS**

## 文件限制

| 限制项 | 说明 |
|--------|------|
| 图片大小 | ≤ 10M，最长边 ≤ 8192px |
| 版式文档大小 | ≤ 100M |
| 流式文档大小 | ≤ 50M |
| PDF 页数 | ≤ 500 页 |
| URL 长度 | ≤ 1024 字节 |
| 优先级 | file_data > file_url |

## 错误处理

常见错误码示例：

| 错误码 | 说明 |
|--------|------|
| `282003` | missing parameters（缺少必要参数） |
| `282007` | task not exist, please check task id（任务不存在） |

完整错误码参见 `references/error_codes.md`。

## 产品计费与购买方式

**接口限时免费**。免费额度自动发放：

| 用户类型 | 免费额度 |
|---------|---------|
| 个人实名认证用户 | **200 页** |
| 企业实名认证用户 | **1000 页** |

登录[文字识别控制台](https://console.bce.baidu.com/ai/)自动领取。后续正式定价以官方[计费说明](https://cloud.baidu.com/doc/OCR/s/Fls06fa15)为准。

## 脚本

- `scripts/baidu_doc_unlimited_ocr_parser.py`：文档解析主程序，支持命令行快速调用

## 参考文档

- `references/parameters.md`：完整 API 参数与返回结构详解
- `references/error_codes.md`：完整错误码参考
- `references/apikey-fetch.md`：API Key 配置指南

## 相关链接

- [官方技术文档](https://cloud.baidu.com/doc/OCR/s/fmr1p39gb)
- [OCR 计费说明](https://cloud.baidu.com/doc/OCR/s/Fls06fa15)
- [百度云控制台](https://console.bce.baidu.com/ai/)
- [智能文档分析平台](https://ai.baidu.com/solution/intelligent-document-analysis)
