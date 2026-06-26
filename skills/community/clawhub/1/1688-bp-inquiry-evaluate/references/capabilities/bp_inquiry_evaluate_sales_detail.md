```markdown
# 业务员评估详情查询指南

## 功能说明

通过 CLI 调用智客通接口，查询业务员能力评估详情。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 当上下文中未提供业务员身份ID或者仅提供业务员名称，先调用工具 `bp_inquiry_evaluate_summary`匹配业务员身份ID

## CLI 调用

```bash
python3 {baseDir}/cli.py bp_inquiry_evaluate_sales_detail --saleIdentityId <saleIdentityId> --startAt <startAt> --endAt <endAt>
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 说明 |
|------|------|----------|------|
| `--saleIdentityId` | `-sid` | ✅ 是 | 业务员身份ID，数值类型 |
| `--startAt` | `-s` | ✅ 是 | 开始日期，字符串类型，格式：yyyyMMdd |
| `--endAt` | `-e` | ✅ 是 | 结束日期，字符串类型，格式：yyyyMMdd |

## 输出格式

### 成功

```json
{
  "success": true,
  "data": {
    "data": {
      "score": 22,
      "inquiryCnt": 5,
      "inquiryTip": "仅统计有商家价值的询盘，已排除售后或仅打招呼等无效询盘",
      "inquiryDetails": [
        {
          "advantageDetails": [
            "首条响应及时，态度友好，符合基础服务规范。"
          ],
          "msgListLength": 21,
          "inquiryScore": 45,
          "inquirySummary": {
            "inquirySummary": "客服未挖掘买家采购用途与数量，对包邮需求未回应，全程敷衍应答，缺乏促单动作，导致流失。",
            "inquiryResult": "当天未成交",
            "purchaseRequirements": "采购塑料泡沫，数量未明确，意向金额未明确"
          },
          "purchaseLevel": "低",
          "itemIds": [
            "851069411772"
          ],
          "communicates": [
            {
              "role": "买家",
              "num": "0",
              "id": "0",
              "content": "https://detail.1688.com/offer/851069411772.html?skuId=5644254456781&spm=a262eq.8274978.im_chat_detail.pc",
              "sendTime": "2026-04-24 08:00:07"
            },
            {
              "positiveSuggest": "响应及时态度好",
              "role": "商家",
              "num": "1",
              "id": "1",
              "content": "您好，在的",
              "sendTime": "2026-04-24 08:00:08"
            }
          ],
          "purchaseGmv": 0,
          "inquiryLevel": "较差",
          "inquiryResult": "当天未成交",
          "purchaseQuantity": 0,
          "name": "买家aaaa",
          "isLargeOrder": 0,
          "userType": "新客",
          "improvementDetails": [
            "应主动询问采购用途、数量，明确优惠方式，并针对包邮诉求快速确认政策以推动成交。"
          ]
        }
      ],
      "saleIdentityName": "xxx业务员",
      "evaluateSummary": {
        "serviceAbility": "业务员表现：建议在需求挖掘能力和促单技巧能力上进一步提升，重点加强主动追问定制细节、使用场景及提供替代方案，结合小批量采购设计专属促单话术。",
        "importantInquiry": "重要询盘：4月24日，买家旺旺ID买家aaaa暂未成交，请重点跟进。",
        "markOptions": [
          "买家aaaa",
        ]
      },
      "saleIdentityId": "123123",
      "indicators": [
        {
          "name": "成交金额",
          "value": "0元"
        }
      ]
    }
  }
}
```

### 失败 — AK 未配置

```json
{
  "success": false,
  "message": "❌ AK 未配置，无法查询。\n\n运行: `cli.py configure YOUR_AK`"
}
```

### 失败 — 其他异常

```json
{
  "success": false,
  "message": "错误描述信息"
}
```

## Agent 处理流程

```
1. 从用户消息中提取：开始日期、结束日期
2. 执行 python3 {baseDir}/cli.py bp_inquiry_evaluate_sales_detail --saleIdentityId <saleIdentityId> --startAt <开始日期> --endAt <结束日期>
3. 检查输出：
   - success=true → 告知用户"查询成功"
   - success=false → 原样输出错误信息
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（startAt/endAt） | 提示用户补充缺少的参数 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |
```
