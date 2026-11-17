# Sugon-Scnet OCR API 文档摘要

> **⚠️ 数据外传警告**：调用本接口会将你上传的本地文件发送至 Scnet 外部 OCR 服务（`https://api.scnet.cn`）。提单等单据可能包含收发货人、航次、货量、联系方式等商业或个人信息，请确认你有权外传该文件内容，并仅上传可信来源文件。

## 接口地址
`POST https://api.scnet.cn/api/llm/v1/ocr/recognize`

## 请求头
- `Content-Type: multipart/form-data`
- `Authorization: Bearer <你的 API Key>`

## 请求参数（表单）
| 参数名  | 类型 | 必填 | 描述                                   |
| ------- | ---- | ---- | -------------------------------------- |
| file    | File | 是   | 需要识别的图片文件                     |
| ocrType | str  | 是   | 识别类型枚举，详见 SKILL.md 参数说明   |

## 响应结构
```json
{
  "code": "0",
  "msg": "success",
  "data": {
    "traceId": "12345678909",
    "originalFilename": "提单示例.jpg",
    "cosPath": "scnetAPIService/20260101/964a7f1e8e79499289c1b525cea7728b.jpg",
    "result": [
      {
        "status": 200,
        "originFilename": "提单示例.jpg",
        "cosPath": "scnetAPIService/20260101/964a7f1e8e79499289c1b525cea7728b.jpg",
        "fileIndex": 1,
        "cutIndex": 0,
        "coordinate": [],
        "classifyCode": "",
        "confidence": 0.8671,
        "elements": {
          "blNumber": "XMN9A1640400",
          "issueDate": "28May2019",
          "loadingPort": "XIAMEN, CHINA",
          "dischargePort": "SM SMKYO 1910E INCHON, REPUBLIC OF KOREA",
          "exporterName": "ABC CO.,LTD",
          "consigneeName": "TO THE ORDER OF INDUSTRIAL BANK OF KOREA",
          "notifyParty": "EDF CO.,LTD 1964, LONONGCHUNG-LONRO, LONWOL-LONON, LONEON-SI, LONONGGI-DO, LONUBLIC OF KOREA",
          "vessel": "SM SMKYO 1910E",
          "issuePlace": "XIAMEN, FUJIAN, CN"
        },
        "stamps": []
      }
    ]
  }
}
```
## 错误码
- `401 / 403: Token 无效或过期`
- `其他 4xx/5xx: 请检查请求参数或联系服务商`
- `业务错误码（如 code 非 0）：见返回的 msg 字段`

## 注意事项
- `支持单张图片、PDF 或多页压缩包（自动解压识别）`
- `识别结果位于 data[0].result[0].elements 中`
- `不同 ocrType 返回的 elements 字段不同，详见 assets/templates/fields-summary.md`
- `识别结果位于 data[0].result[0].stamps 中`
- `不同 ocrType 返回的 stamps 字段不同，详见 assets/templates/fields-summary.md`
