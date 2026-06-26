# 1688招商活动商品信息及建议价查询指南

## 功能说明

根据活动ID和商品ID，查询商品信息及建议提报价格。报名前必须先调用此接口，让商家确认建议价后再提交报名。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 已知活动ID（可通过 `1688_enroll_activity_query` 获取）
- 已知商品ID

## CLI 调用

```bash
python3 {baseDir}/cli.py 1688_enroll_offer_query --activityId 12345 --itemId 67890
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 类型 | 说明 |
|------|------|----------|------|------|
| `--activityId` | `-a` | ✅ 是 | Integer | 活动Id |
| `--itemId` | `-i` | ✅ 是 | Integer | 商品Id |

### 调用示例

```bash
python3 {baseDir}/cli.py 1688_enroll_offer_query -a 12345 -i 67890
```

## 输出格式

### 成功 — 无SKU商品（价格在商品级别）

```json
{
  "success": true,
  "markdown": "",
  "data": {
    "itemId": 67890,
    "title": "商品名称",
    "price": 100,
    "suggestPrice": 80,
    "skuList": []
  }
}
```

### 成功 — 有SKU商品（价格在SKU级别）

```json
{
  "success": true,
  "markdown": "",
  "data": {
    "itemId": 67890,
    "title": "商品名称",
    "price": null,
    "suggestPrice": null,
    "skuList": [
      {
        "skuId": 111,
        "title": "红色/XL",
        "price": 100,
        "suggestPrice": 80
      },
      {
        "skuId": 222,
        "title": "蓝色/L",
        "price": 120,
        "suggestPrice": 95
      }
    ]
  }
}
```

> **注意**：`skuList` 为空时，商品级别的 `price` 和 `suggestPrice` 有值；`skuList` 不为空时，价格在 SKU 级别，商品级别的 `price` 和 `suggestPrice` 为空。价格单位为分。

## Agent 处理流程

```
1. 用户选定活动后，询问要报名的商品ID
2. 执行 python3 {baseDir}/cli.py 1688_enroll_offer_query --activityId <活动ID> --itemId <商品ID>
3. 检查输出：
   - success=true → 展示商品信息和建议提报价，询问商家是否确认以该价格提报
   - success=false → 原样输出错误信息
4. 商家确认价格后，继续调用报名接口
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（activityId/itemId） | 提示用户补充缺少的参数 |
| 商品不存在或不符合活动要求 | 原样输出错误信息，建议用户确认商品ID |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 SKILL.md 异常处理章节。
