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
            "traceId": "202604010000020",
            "originalFilename": "通用机打发票示例.jpg",
            "cosPath": "/ocr/202604/01/通用机打发票示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "通用机打发票示例.jpg",
                    "cosPath": "/ocr/202604/01/通用机打发票示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "MEDICAL_INVOICE",
                    "confidence": 0.995,
                    "elements": {
                      "title": "广东通用机打发票(电子)",
                      "invoiceCode": "010002010010",
                      "invoiceNo": "18933189",
                      "invoiceDate": "2021年08月17日",
                      "checkCode": "00189001893518942001",
                      "buyerName": "公司工会科技有限责任公司工会",
                      "buyerCode": "18918918920212021",
                      "buyerAddressAndPhone": "广州市荔湾区178178178178",
                      "buyerBankAndAccount": "广州市荔湾区支行2021202120212021",
                      "sellerName": "广州市荔湾区水果店",
                      "sellerCode": "92492401MA5CXNG924",
                      "sellerAddressAndPhone": "广州市荔湾区荔湾路68号1741741781",
                      "sellerBankAndAccount": "中国工商银行广州同德支行22352235223522352235",
                      "preTaxTotalAmount": "297.03",
                      "totalTaxAmount": "2.97",
                      "totalAmountUpper": "叁佰圆整",
                      "totalAmountLower": "300.00",
                      "remarks": "(自主申报)",
                      "payee": "刘申申",
                      "checker": "黄申申",
                      "drawer": "纪申",
                      "goodsDetails": [
                        {
                          "goodsName": "*水果*阳光冬枣",
                          "specification": "斤",
                          "unit": "斤",
                          "quantity": "10.03",
                          "unitPrice": "29.61412791",
                          "itemAmount": "297.03",
                          "taxRate": "1%",
                          "taxAmount": "2.97"
                        }
                      ]
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
