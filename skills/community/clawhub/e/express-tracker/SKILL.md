---
name: express-tracker
description: 快递物流查询技能，支持圆通、中通、申通、韵达、顺丰、京东等主流快递公司。自动识别快递公司，生成快递100查询链接。使用场景：(1) "查询快递 YT2538259220416"，(2) "我的快递到哪了"，(3) "批量查询几个快递单号"。
---

# 快递物流查询技能

快速生成国内主流快递公司的查询链接，支持自动识别快递公司。

## 支持的快递公司

- **圆通速递** (YT)
- **中通快递** (ZT)
- **申通快递** (ST)
- **韵达快递** (YD)
- **顺丰速运** (SF)
- **京东物流** (JD)
- **邮政EMS** (EMS)
- **极兔速递** (JTSD)
- **德邦快递** (DBL)
- 等 3000+ 家快递公司

## 快速开始

### 单票查询

```bash
# 自动识别快递公司并生成查询链接
python3 scripts/track_express.py --nu YT2538259220416

# 自动在浏览器中打开查询链接（macOS）
python3 scripts/track_express.py --nu YT2538259220416 --open
```

### 批量查询

```bash
# 从文件批量生成查询链接
python3 scripts/batch_track.py --file express_list.txt

# 命令行指定多个单号
python3 scripts/batch_track.py --nus YT2538259220416,SF1234567890
```

## 详细用法

### 单票查询脚本

```bash
python3 scripts/track_express.py [选项]

选项:
  --nu NU            快递单号（必需）
  --com COM          快递公司代码（可选，自动识别）
  --format FORMAT    输出格式：text/json/markdown（默认：text）
  --output FILE      输出到文件（可选）
  --open             自动在浏览器中打开查询链接（macOS）
```

示例：
```bash
# 基本查询
python3 scripts/track_express.py --nu YT2538259220416

# 自动在浏览器打开
python3 scripts/track_express.py --nu YT2538259220416 --open

# 输出 JSON 格式
python3 scripts/track_express.py --nu YT2538259220416 --format json

# 保存到文件
python3 scripts/track_express.py --nu YT2538259220416 --output result.md
```

### 批量查询脚本

```bash
python3 scripts/batch_track.py [选项]

选项:
  --file FILE        快递列表文件（每行一个单号）
  --nus NUS          快递单号列表，逗号分隔
  --format FORMAT    输出格式：text/json/markdown（默认：text）
  --output FILE      输出到文件（可选）
```

示例：
```bash
# 从文件批量查询
python3 scripts/batch_track.py --file my_express.txt

# 命令行批量查询
python3 scripts/batch_track.py --nus YT2538259220416,SF1234567890

# 输出 Markdown 报告
python3 scripts/batch_track.py --file my_express.txt --format markdown
```

### 快递列表文件格式

创建一个文本文件，每行一个快递单号：

```
# my_express.txt
YT2538259220416
SF1234567890
JD0123456789012
```

## 快递公司代码参考

| 快递公司 | 代码 | 单号前缀 |
|---------|------|---------|
| 圆通速递 | yuantong | YT |
| 中通快递 | zhongtong | ZT |
| 申通快递 | shentong | ST |
| 韵达快递 | yunda | YD |
| 顺丰速运 | shunfeng | SF |
| 京东物流 | jd | JD |
| 邮政EMS | ems | 10/11/50 |
| 极兔速递 | jtexpress | JT |
| 德邦快递 | deppon | DPL |

## 数据来源

- **快递100** - 提供查询链接（无需密钥）
- 支持 3000+ 家快递公司

## 输出示例

### 文本格式

```
📦 快递单号：YT2538259220416
🏢 快递公司：圆通速递
🔗 查询链接：https://www.kuaidi100.com/chaxun?nu=YT2538259220416

💡 提示：点击上方链接查看详细物流信息
```

### JSON 格式

```json
{
  "nu": "YT2538259220416",
  "com": "yuantong",
  "com_name": "圆通速递",
  "query_url": "https://www.kuaidi100.com/chaxun?nu=YT2538259220416"
}
```

## 技能文件结构

```
express-tracker/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── track_express.py        # 单票查询脚本
│   ├── batch_track.py          # 批量查询脚本
│   └── express_codes.py        # 快递公司代码库
└── examples/
    └── example_list.txt        # 快递列表示例
```

## 常见问题

**Q: 如何自动识别快递公司？**
A: 脚本会根据单号前缀自动识别，常见单号前缀如 YT（圆通）、SF（顺丰）等。

**Q: 为什么不直接显示物流信息？**
A: 页面解析比较复杂且容易失效，提供查询链接是最稳定可靠的方式。

**Q: 支持国际快递吗？**
A: 主要支持国内快递，部分国际快递（如 DHL、FedEx）可以在快递100网站查询。

**Q: 为什么不用快递100的API？**
A: 快递100的正式API需要申请密钥，这个技能使用免费的公开查询方式，开箱即用。
