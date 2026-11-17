# Sugon-Scnet OCR API 文档摘要

> **⚠️ 隐私与安全提示**：调用本接口会将本地文件内容上传至第三方 Scnet 云端服务（`api.scnet.cn`）。商业发票通常包含公司名称、地址、发票金额、信用证号、合同号、贸易条款等敏感商业信息。请确保用户已知情并同意文件外传后再调用。

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
    "originalFilename": "商业发票示例.jpg",
    "cosPath": "scnetAPIService/20260101/a5360b6f3b0a4514aaf4cbe10be00dbf.jpg",
    "result": [
      {
        "status": 200,
        "originFilename": "商业发票示例.jpg",
        "cosPath": "scnetAPIService/20260101/a5360b6f3b0a4514aaf4cbe10be00dbf.jpg",
        "fileIndex": 1,
        "cutIndex": 0,
        "coordinate": [],
        "classifyCode": "",
        "confidence": 0.9642,
        "elements": {
          "invoiceNo": "BHGX-W201920192019",
          "invoiceDate": "MAY 26, 2019",
          "totalAmount": "61752.72",
          "issuerName": "ANJIAN IONLION TECH-TECH MATERIAL INDUSTRY CO.,LTD",
          "issuerAddress": "INDUST INDUSTRIAL AREA,LONLON TOWN,LONANG CITY,FUJIAN,CHINA  DADADA",
          "lcNumber": " LM90490420192019",
          "lcDate": " MAY 19, 2019",
          "contractNumber": " BHGX-W20192019202019",
          "priceTerm": " CIF INCHON, REPUBLIC OF KOREA"
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
