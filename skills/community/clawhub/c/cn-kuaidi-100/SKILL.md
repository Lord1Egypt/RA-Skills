---
name: cn-express-tracker
description: |
  中文快递追踪助手。根据快递单号自动识别快递公司，查询实时物流状态。
  支持国内外主流快递，使用快递100免费接口，无需API Key。
  当用户说"快递"、"查快递"、"物流"、"单号"、"包裹到哪了"时触发。
  Keywords: 快递, 物流, 单号, 追踪, 包裹, delivery, tracking
metadata: {"openclaw": {"emoji": "📦"}}
---

# 📦 快递追踪助手

查快递，更轻松。

## 核心功能

| 功能 | 命令示例 |
|------|----------|
| 添加追踪 | `添加快递 SF1234567890` |
| 查询单个 | `查 SF1234567890` / `顺丰SF1234567890到哪了` |
| 查看列表 | `查快递` / `我的快递` |
| 删除快递 | `删除快递 SF1234567890` |
| 清除所有 | `清除快递` |

## 使用方式

```bash
# 添加快递到追踪列表
python3 scripts/express_tracker.py "添加快递 SF1234567890"

# 查询单个快递（自动识别公司）
python3 scripts/express_tracker.py "查 SF1234567890"

# 指定公司查询
python3 scripts/express_tracker.py "查 1234567890123 公司:顺丰"

# 查看所有追踪快递
python3 scripts/express_tracker.py "查快递"

# 删除追踪
python3 scripts/express_tracker.py "删除 SF1234567890"
```

## 支持的快递公司

顺丰速运、中通、圆通、韵达、申通、极兔、京东、EMS、中国邮政、德邦

## 技术说明

- 数据接口：快递100开放查询接口
- 认证方式：无需API Key，直接查询
- SSL策略：优先标准验证，失败时自动降级（兼容老旧环境）
- 数据存储：本地JSON文件，隐私安全

## 数据存储位置

`~/.qclaw/skills/cn-express-tracker/data/express.json`

## 注意事项

- 部分快递公司需要真实在途物流才可查询
- 首次查询会自动添加到追踪列表
- 自动识别主流快递公司单号格式
- 单号格式：SF/ET/YT/YD/ST前缀，或10-22位纯数字
