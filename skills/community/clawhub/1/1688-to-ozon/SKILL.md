---
name: 1688-to-ozon
version: 1.0.71
description: 1688 商品自动采集并上传到 OZON 平台
triggers:
  - op
  - ozon 上架
  - ozon 上传
  - 1688-to-ozon
read_when:
  - 上架商品到 OZON
  - 从 1688 采集商品
metadata:
  clawdbot:
    emoji: "🛒"
    requires:
      bins: ["node", "agent-browser"]
allowed-tools: Bash(node:scripts/index.js)
---

# 1688-to-OZON

将 1688 商品自动采集并上传到 OZON 电商平台。

**版本**: v1.0.71  
**最后更新**: 2026-04-06

---

## 快速开始

```bash
# 基本用法
node scripts/index.js "URL" -w 重量 -p 采购价

# 示例
node scripts/index.js "https://detail.1688.com/offer/xxx.html" -w 300g -p 14
```

---

## 参数说明

| 参数 | 简写 | 必需 | 说明 | 默认值 |
|------|------|------|------|--------|
| `URL` | - | ✅ | 1688 商品链接 | - |
| `--weight` | -w | ✅ | 商品重量（100g, 0.5kg） | - |
| `--purchase-price` | -p | ✅ | 采购价（人民币） | - |
| `--shipping` | -s | ❌ | 国内运费 | 0 |
| `--profit` | - | ❌ | 利润率（小数） | 0.2 |
| `--category` | - | ❌ | OZON 类目 | toy_set |
| `--log` | -l | ❌ | 实时进度输出（主代理捕获发送飞书） | false |
| `--debug` | - | ❌ | Debug 模式（Mock数据） | false |
| `--pause` | - | ❌ | 上传前暂停确认 | false |
| `--step` | - | ❌ | 从第几步开始（1-4） | 1 |

---

## 执行流程

```
Step 1: 1688 商品抓取 → 提取主图+详情图+文案
Step 2: 图片翻译 → 中文→俄文，上传图床
Step 3: 定价计算 → 物流+佣金+利润
Step 4: OZON 上传 → API上传+库存设置
```

---

## 示例

```bash
# 完整参数
node scripts/index.js "URL" -w 1.6kg -p 70 --profit 0.25 -l

# 简单参数
node scripts/index.js "URL" -w 300g -p 14

# Debug 模式
node scripts/index.js "URL" -w 100g -p 30 --debug

# 暂停确认
node scripts/index.js "URL" -w 100g -p 30 --pause
```

---

## 配置

配置文件：`config/config.json` 和 `config/user.json`

```json
{
  "ozon": {
    "clientId": "your-client-id",
    "apiKey": "your-api-key"
  },
  "pricing": {
    "defaultProfit": 0.2
  }
}
```

---

## 版本历史

- v1.0.71 (2026-04-06) - 按 OpenClaw 规则重新整理 SKILL.md
- v1.0.70 (2026-04-05) - 移除标签格式修复代码
- v1.0.69 (2026-04-05) - 修复标签和富文本上传失败