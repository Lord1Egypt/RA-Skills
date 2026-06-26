# 1688招商活动报名指南

## 功能说明

提交1688招商活动报名，报品同时报商。提交前需先通过 `1688_enroll_offer_query` 查询建议价并获得商家确认。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 已通过 `1688_enroll_offer_query` 查询商品建议价
- 商家已确认提报价格

## CLI 调用

```bash
python3 {baseDir}/cli.py 1688_enroll_submit_item --activityId 12345 --itemId 67890 --fillFormDataList '[{"inputKey":"fixPrice","inputValue":"0.8"}]'
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 类型 | 说明 |
|------|------|----------|------|------|
| `--activityId` | `-a` | ✅ 是 | Integer | 活动Id |
| `--itemId` | `-i` | ✅ 是 | Integer | 商品Id |
| `--fillFormDataList` | `-f` | ✅ 是 | JSON String | 价格等表单填充数据列表 |

### fillFormDataList 格式

JSON 数组，每项包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `inputKey` | String | 表单key |
| `inputValue` | String | 表单值，商品无SKU时填此项 |
| `inputValueSku` | Object | 表单值，商品有SKU时填此项，key为skuId，value为对应值 |

#### 无SKU商品示例

```json
[{"inputKey": "fixPrice", "inputValue": "0.8"}]
```

#### 有SKU商品示例

```json
[{"inputKey": "fixPrice", "inputValueSku": {"111": "0.8", "222": "0.75"}}]
```

### 调用示例

```bash
# 无SKU商品报名
python3 {baseDir}/cli.py 1688_enroll_submit_item -a 12345 -i 67890 -f '[{"inputKey":"fixPrice","inputValue":"0.8"}]'

# 有SKU商品报名
python3 {baseDir}/cli.py 1688_enroll_submit_item -a 12345 -i 67890 -f '[{"inputKey":"fixPrice","inputValueSku":{"111":"0.8","222":"0.75"}}]'
```

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "✅ 报名成功！记录ID: 99999",
  "data": {
    "success": true,
    "recordId": 99999,
    "message": ""
  }
}
```

### 失败

```json
{
  "success": false,
  "markdown": "❌ 报名失败：xxx原因",
  "data": {
    "success": false,
    "recordId": null,
    "message": "失败原因"
  }
}
```

## Agent 处理流程

```
1. 商家确认建议价后，根据商品是否有SKU构造 fillFormDataList，注意价格单位需要转为元
2. 执行 python3 {baseDir}/cli.py 1688_enroll_submit_item --activityId <活动ID> --itemId <商品ID> --fillFormDataList '<JSON>'
3. 检查输出：
   - success=true → 告知商家报名成功，展示记录ID
   - success=false → 原样输出错误信息
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失 | 提示用户补充缺少的参数 |
| fillFormDataList 格式错误 | 提示用户检查 JSON 格式 |
| 报名失败（业务原因） | 原样输出错误信息中的 message |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 SKILL.md 异常处理章节。
