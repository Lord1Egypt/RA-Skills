```markdown
# 业务员评估概览查询指南

## 功能说明

通过 CLI 调用智客通接口，查询业务员能力评估概览。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py bp_inquiry_evaluate_summary --startAt "20260501" --endAt "20260510"
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 说明 |
|------|------|----------|------|
| `--startAt` | `-s` | ✅ 是 | 开始日期，格式：yyyyMMdd |
| `--endAt` | `-e` | ✅ 是 | 结束日期，格式：yyyyMMdd |

## 输出格式

### 成功

```json
{
  "success": true,
  "data": {
    "data": {
      "evaluateSummary": {
        "indicators": [
          {
            "avgCate": "27%",
            "name": "询盘转化率",
            "description": "已成单的询盘数/有效询盘接待数",
            "value": "0%",
            "contrastCate": "-100%"
          }
        ]
      },
      "salesman": 1,
      "evaluateDetails": [
        {
          "saleIdentityName": "测试商家111",
          "saleIdentityId": 123456,
          "indicators": [
            {
              "name": "成交金额",
              "value": "0元"
            }
          ]
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
2. 执行 python3 {baseDir}/cli.py bp_inquiry_evaluate_summary --startAt <开始日期> --endAt <结束日期>
3. 检查输出：
   - success=true → 告知用户"查询成功"
   - success=false → 原样输出错误信息
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（title/userId/text） | 提示用户补充缺少的参数 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

