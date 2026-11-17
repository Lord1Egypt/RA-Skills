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
    "data":[ 
        {
            "traceId": "202604010000017",
            "originalFilename": "增值税发票示例.jpg",
            "cosPath": "/ocr/202604/01/增值税发票示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "增值税发票示例.jpg",
                    "cosPath": "/ocr/202604/01/增值税发票示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "VAT_INVOICE",
                    "confidence": 0.996,
                    "elements": {
                      "title": "厦门增值税专用发票",
                      "invoiceCode": "3502210221",
                      "invoiceNo": "04727777",
                      "printedCode": "3502210221",
                      "printedNo": "04727777",
                      "checkCode": "",
                      "machineCode": "499099900999",
                      "invoiceDate": "20220707",
                      "passwordArea": "03+6//8820/+688-+3>5<45-56>703+6//8820/+688-+3>5<45-56>703+6//8820/+688-+3>5<45-56>703+6//8820/+688-+3>5<45-56>7",
                      "buyerName": "中国思味银行股份有限公司厦门市分行",
                      "buyerCode": "913502008520082008",
                      "buyerAddressAndPhone": "厦门市思明区思明道05号05922105922",
                      "buyerBankAndAccount": "厦门分行营业部35350035003500013500",
                      "sellerName": "中国厦门厦门有限公司厦门分公司",
                      "sellerCode": "91350200720072007D",
                      "sellerAddressAndPhone": "厦门市思明路25号10000",
                      "sellerBankAndAccount": "思明厦门思明支行4100020009200020009",
                      "preTaxTotalAmount": "39622.64",
                      "totalTaxAmount": "2377.36",
                      "totalAmountUpper": "肆万贰仟圆整",
                      "totalAmountLower": "42000.00",
                      "invoiceForm": "第三联:发票联",
                      "remarks": "备注示例",
                      "payee": "张三",
                      "checker": "李四",
                      "drawer": "李明",
                      "goodsDetails": {
                        "goodsName": "*电信服务*增值电信服务",
                        "specification": "无",
                        "unit": "项",
                        "quantity": "1",
                        "unitPrice": "39622.64",
                        "itemAmount": "39622.64",
                        "taxRate": "6%",
                        "taxAmount": "2377.36"
                      }
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
