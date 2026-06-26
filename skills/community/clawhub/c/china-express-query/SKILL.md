---
name: china-express-query
description: 中国快递查询 - 支持顺丰、圆通、中通、申通、韵达、EMS、京东、德邦等10+快递公司，自动识别单号
homepage: https://github.com/openclaw/china-express-query
metadata: {"openclaw":{"emoji":"📦","requires":{"bins":["node"]}}}
---

# China Express Query 📦

中国快递查询工具，支持顺丰、圆通、中通、申通、韵达、EMS、京东、德邦、百世、极兔等10+主流快递公司物流信息查询。

**特点**：
- 🔍 智能识别快递单号
- 📦 支持10+快递公司
- ⚡ 快速查询物流状态
- 📝 清晰的物流轨迹展示

## 支持的快递公司

| 快递公司 | 代码 | 说明 |
|---------|------|------|
| 顺丰速运 | sf | 顺丰快递查询 |
| 圆通速递 | yto | 圆通快递查询 |
| 中通快递 | zto | 中通快递查询 |
| 申通快递 | sto | 申通快递查询 |
| 韵达速递 | yd | 韵达快递查询 |
| 邮政EMS | ems | EMS快递查询 |
| 京东物流 | jd | 京东快递查询 |
| 德邦快递 | db | 德邦快递查询 |
| 百世快递 | bs | 百世快递查询 |
| 极兔速递 | jt | 极兔快递查询 |

## 快速开始

### 查询快递
```bash
node {baseDir}/scripts/query.mjs <快递单号>
```

### 指定快递公司
```bash
node {baseDir}/scripts/query.mjs <快递单号> --company sf
```

### 示例
```bash
# 自动识别快递公司
node scripts/query.mjs "SF1234567890"

# 指定顺丰
node scripts/query.mjs "SF1234567890" --company sf

# 查询中通
node scripts/query.mjs "ZT1234567890" --company zto
```

## 使用场景

### 场景1：查询自己的快递
```bash
node scripts/query.mjs "你的快递单号"
```

### 场景2：批量查询
```bash
node scripts/query.mjs "单号1" && node scripts/query.mjs "单号2"
```

### 场景3：查询特定快递
```bash
node scripts/query.mjs "SF1234567890" --company sf --detail
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--company <code>` | 指定快递公司代码 | 自动识别 |
| `--detail` | 显示详细信息 | false |
| `--output <file>` | 输出到文件 | 控制台 |

## 输出格式

### 标准输出
```
📦 快递查询结果
═══════════════════════════════════════
快递公司: 顺丰速运
快递单号: SF1234567890
状态: 已签收

物流轨迹:
1. [2024-01-15 14:30] 深圳市 - 已签收
2. [2024-01-15 08:20] 深圳市 - 派送中
3. [2024-01-14 22:15] 深圳市 - 到达深圳转运中心
...
```

## 数据来源

- 快递100 (kuaidi100.com)
- 百度快递查询 (备用)

## 注意事项

- 快递单号请准确输入
- 部分快递可能需要验证码
- 查询结果来自第三方接口，可能有延迟
- 本工具仅供个人查询使用

## 许可

MIT License
