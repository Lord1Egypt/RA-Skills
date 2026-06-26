# Sugon-Scnet OCR API 文档摘要

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
    "data": [
        {
            "traceId": "202604010000011",
            "originalFilename": "营业执照示例.jpg",
            "cosPath": "/ocr/202604/01/营业执照示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "营业执照示例.jpg",
                    "cosPath": "/ocr/202604/01/营业执照示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "BUSINESS_LICENSE",
                    "confidence": 0.996,
                    "elements": {
                        "title": "营业执照",
                        "socialCreditCode": "9141225973G225973G",
                        "name": "技术开发电子科技有限公司",
                        "capital": "陆佰壹拾万圆整",
                        "type": "有限责任公司(自然人投资或控股的法人独资)",
                        "date": "2003年04月28日",
                        "directorType": "法定代表人",
                        "director": "张开发",
                        "businessTerm": "2003年04月28日至2028年04月01日",
                        "businessScope": "电子产品的技术开发, 安全生产检测检验(凭有效资质证经营)。(依法须经批准的项目, 经相关部门批准后方可开展经营活动)",
                        "address": "山州市圆山路330号院307室"
                    },
                    "stamps": []
                }
            ]
        }
    ]
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
