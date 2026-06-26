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
            "originalFilename": "机动车销售统一发票示例.jpg",
            "cosPath": "/ocr/202604/01/机动车销售统一发票示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "机动车销售统一发票示例.jpg",
                    "cosPath": "/ocr/202604/01/机动车销售统一发票示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "MEDICAL_INVOICE",
                    "confidence": 0.995,
                    "elements": {
                      "title": "机动车销售统一发票",
                      "invoiceForm": "第一联:发票联",
                      "invoiceCode": "163163163163",
                      "invoiceNo": "390039",
                      "issueDate": "20200702",
                      "printedCode": "163163163163",
                      "printedNo": "390039",
                      "machineCode": "539929120039",
                      "taxControlCode": "0343<-1<6097D+0>>79^6<00>*9^3+72<<05340343<-1<6097+",
                      "buyerName": "中国流动服务股份有限公司河北省分行",
                      "buyerTaxId": "91130000891130000Y",
                      "buyerCode": "91130000891130000Y",
                      "vehicleType": "流动服务车",
                      "brandModel": "NJH5045XDWW6161",
                      "originalPlace": "南京市",
                      "qualifiedNo": "YV3342001942001",
                      "importCertificateNo": "",
                      "commodityInspectionNo": "",
                      "engineNo": "1366666",
                      "vehicleIdentificationNo": "LNVL9113000000998",
                      "totalAmountUpper": "捌拾贰万圆整",
                      "totalAmountLower": "820000",
                      "sellerName": "青海经济技术开发区汽车销售有限公司",
                      "sellerTaxId": "91632900595900595Q",
                      "sellerAddressAndPhone": "青海省西宁市经济技术开发区开发路55号(0971-8877777)",
                      "sellerBankAndAccount": "流动服务经济技术开发区支行|2806018309198130919",
                      "taxRate": "13%",
                      "taxAmount": "94336.28",
                      "taxAuthorityName": "国家税务总局西宁经济技术开发区开发工业园区税务局税源管理股",
                      "taxAuthorityCode": "163320000004",
                      "preTaxAmount": "725663.72",
                      "taxPaymentVoucher": "",
                      "tonnage": "",
                      "maxCapacity": "",
                      "drawer": "王莺",
                      "remark": ""
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
