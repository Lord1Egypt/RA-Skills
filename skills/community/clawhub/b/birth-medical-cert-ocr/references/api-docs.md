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
            "traceId": "202604010000006",
            "originalFilename": "出生医学证明示例.jpg",
            "cosPath": "/ocr/202604/01/出生医学证明示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "出生医学证明示例.jpg",
                    "cosPath": "/ocr/202604/01/出生医学证明示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "BIRTH_MEDICAL_CERTIFICATE",
                    "confidence": 0.997,
                    "elements": {
                      "title": "出生医学证明",
                      "newbornName": "刘小玲",
                      "gender": "女",
                      "birthTime": "2024年3月26日18时26分",
                      "gestationalWeeks": "40",
                      "birthWeight": "2860",
                      "birthLength": "49.0",
                      "birthPlace": "北京市省市海淀区县(区)",
                      "medicalInstitutionName": "北京市海淀医院",
                      "motherName": "张靓丽",
                      "motherAge": "24",
                      "motherNationality": "中国",
                      "motherEthnicGroup": "汉族",
                      "motherAddress": "北京市海淀区永兴路昌盛街道**胡同*号院**号",
                      "motherIdType": "居民身份证",
                      "motherIdNumber": "1100***********214",
                      "fatherName": "刘大梁",
                      "fatherAge": "26",
                      "fatherNationality": "中国",
                      "fatherEthnicGroup": "汉族",
                      "fatherAddress": "北京市海淀区永兴路昌盛街道**胡同*号院**号",
                      "fatherIdType": "居民身份证",
                      "fatherIdNumber": "1100***********214",
                      "issuingAuthority": "北京市海淀医院",
                      "issueDate": "2024年04月03日",
                      "certificateNumber": "Y5******99"
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
