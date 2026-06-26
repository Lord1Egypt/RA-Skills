# 💰 萤火虫空压机报价单 / Firefly Compressor Quotation

**`/bj` — 萤火虫空压机官方报价单生成助手**

[![Version](https://img.shields.io/badge/version-1.0.0-green)]()
[![License](https://img.shields.io/badge/license-MIT--0-blue)]()

---

## ✨ 功能亮点

- 🔍 **智能产品选型** — 按排气量/功率自动匹配推荐型号
- 🔗 **后处理自动配套** — 冷干机、过滤器、储气罐一键推荐
- 📊 **阶梯折扣计算** — 按设备总价自动应用折扣率
- 🚚 **运费智能估算** — 按距离自动计算运费
- 📄 **双格式输出** — Markdown 报价单（默认）+ 品牌 HTML 报价单

## ⚠️ ClawHub 兼容方案

ClawHub 不支持二进制文件（PNG/XLSX/PDF），本 Skill 全部使用纯文本替代：

| 传统文件 | 纯文本替代 | 格式 |
|---------|----------|------|
| `logo.png` | `assets/brand-logo.svg` | SVG 矢量图 |
| `products.xlsx` | `data/products.yaml` | YAML 结构化数据 |
| 报价计算 | SKILL.md + `scripts/calculate.py` | 决策逻辑 + 验算脚本 |

## 🚀 使用方式

### 1. 直接对话
```
用户: /bj YDV-75 一台，北京 500km
→ 自动报价
```

### 2. 脚本验算
```bash
python scripts/calculate.py --model YDV-75 --distance 500 --with-spares
```

### 3. 按需求选型
```
用户: /bj 需要 15m³/min，0.8MPa，预算 20 万以内
→ 推荐型号并报价
```

## 📁 文件结构

```
bj/
├── SKILL.md                    # 报价流程 + 计算逻辑
├── README.md                   # 本文件
├── scripts/calculate.py        # 报价验算脚本
├── data/products.yaml          # 产品数据库（14 主机 + 9 后处理）
├── assets/
│   ├── quote-template.html     # HTML 报价单模板
│   └── brand-logo.svg          # 萤火虫 Logo
└── references/
    └── pricing-rules.md        # 定价规则详解
```

## 🏷️ 品牌信息

- 公司：广州市萤火虫智能装备技术有限公司
- 品牌：萤火虫空压机
- 官网：http://www.fireflies.net.cn
- 热线：13825202084（邹先生）

## 📄 License

MIT-0 — Published to ClawHub Skill Marketplace
