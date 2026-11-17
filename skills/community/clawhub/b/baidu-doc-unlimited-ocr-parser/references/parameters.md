# 百度文档解析（Unlimited-OCR）API 参数详解

## 接口概述

基于 Unlimited-OCR 开源方案的标准化 API 服务，无需部署即可调用，直接返回 Markdown 结构化结果。适合复杂表格、多段落、多结构文档解析。

## API 接口地址

### 提交请求接口

```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task?access_token={access_token}
Content-Type: application/x-www-form-urlencoded
```

### 获取结果接口

```
POST https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task/query?access_token={access_token}
Content-Type: application/x-www-form-urlencoded
```

## 提交请求参数

### 文件参数（必选，二选一）

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| file_data | 和 file_url 二选一 | string | 文件 Base64 编码。版式文档：pdf, jpg, jpeg, png, bmp, tif, tiff, ofd（图片最长边≤8192px）；流式文档：doc, docx, txt, wps, ppt, pptx。图片≤10M，版式文档≤100M，流式文档≤50M，PDF≤500 页。超过 50M 须用 file_url。优先级：file_data > file_url |
| file_url | 和 file_data 二选一 | string | 文件 URL，≤1024 字节。PDF≤100M，最大 500 页。请关闭 URL 防盗链 |
| file_name | 是 | string | 文件名，后缀须正确，如 "1.pdf" |

### 图像预处理参数（可选）

| 参数 | 必选 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| angle_adjust | 否 | bool | True | 角度矫正 |
| angle_mode | 否 | string | direction | 角度矫正模式，开启角度矫正后生效。direction：四方向；arbitrary：任意方向 |
| erase_seal | 否 | bool | False | 印章擦除 |
| erase_watermark | 否 | bool | False | 水印擦除 |
| unwarp | 否 | bool | False | 图像扭曲矫正 |

## 提交请求返回

| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | uint64 | 唯一的 log id，用于问题定位 |
| error_code | int | 错误码 |
| error_msg | string | 错误描述信息 |
| result.task_id | string | 该请求生成的 task_id |

## 获取结果请求参数

| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 提交请求接口返回的 task_id |

## 获取结果返回

| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | uint64 | 唯一 log id |
| error_code | int | 错误码 |
| error_msg | string | 错误描述 |
| result.task_id | string | 任务 ID |
| result.status | string | pending（排队中）/ running（运行中）/ success（成功）/ failed（失败） |
| result.task_error | string | 解析报错信息 |
| result.markdown_url | string | Markdown 结果链接（30 天有效） |
| result.parse_result_url | string | JSON 结果 BOS 链接（30 天有效） |

## 输出说明

- Markdown 主输出：`markdown_url` 指向的文件是完整 Markdown 文档；复杂表格以 HTML `<table>` 元素内嵌，支持 rowspan/colspan、居中对齐、单元格换行等排版。
- Markdown 结果可直接在 Markdown 渲染器中查看，也可用于下游 RAG、知识库入库等场景。

## QPS 限制

- 提交请求接口：2 QPS
- 获取结果接口：5 QPS

## 相关文档

- [官方 API 文档](https://cloud.baidu.com/doc/OCR/s/fmr1p39gb)
- [错误码参考](error_codes.md)
- [API Key 配置指南](apikey-fetch.md)
