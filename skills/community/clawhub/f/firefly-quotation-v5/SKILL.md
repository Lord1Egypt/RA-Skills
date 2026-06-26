---
name: bj
description: >-
  萤火虫空压机报价单生成助手。根据产品型号和配置自动生成客户报价单，
  支持产品选型→后处理匹配→折扣计算→运费估算→税费处理→安装调试
  全流程报价。输出品牌 HTML 报价单或 Markdown 报价单，支持打印和
  PDF导出。Use when users ask for quotation, 报价, 报价单, price quote,
  sales quote for 萤火虫空压机 products.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: "💰"
    homepage: http://www.fireflies.net.cn
    os:
      - darwin
      - linux
      - windows
user-invocable: true
disable-model-invocation: false
---

# 萤火虫空压机报价单 / Firefly Compressor Quotation

## 品牌身份

- **公司**：广州市萤火虫智能装备技术有限公司（萤火虫空压机）
- **网址**：http://www.fireflies.net.cn
- **热线**：13825202084（邹先生）| 邮箱：aifirefly@163.com
- **地址**：广州市
- **品牌色**：绿 `#1B8C3A` | 蓝 `#1565C0` | 橙 `#F57C00`

## 架构：纯文本方案

ClawHub/OpenClaw 不支持二进制文件（PNG、XLSX、PDF），本 Skill 全部使用纯文本格式：

| 传统方式 | 纯文本替代 | 说明 |
|---------|----------|------|
| `logo.png` | `assets/brand-logo.svg` | SVG 矢量图，浏览器原生渲染 |
| `products.xlsx` | `data/products.yaml` | YAML 结构化数据，可直接读取 |
| 报价公式 | SKILL.md + `scripts/calculate.py` | 决策逻辑内嵌，脚本验算 |
| 输出 | `assets/quote-template.html` | 自包含 HTML，可打印/导出PDF |

```
bj/
├── SKILL.md                    # 本文件：报价流程 + 计算逻辑
├── README.md                   # 市场说明
├── scripts/
│   └── calculate.py            # 报价验算脚本
├── data/
│   └── products.yaml           # 产品数据库（替代 .xlsx）
├── assets/
│   ├── quote-template.html     # 报价单 HTML 模板
│   └── brand-logo.svg          # 公司 Logo（SVG）
└── references/
    └── pricing-rules.md        # 定价规则详解
```

## 数据来源

产品数据从 `data/products.yaml` 读取，包含：
- **空压机主机**（14 个型号）：永磁变频、双级压缩、工频、激光切割
- **后处理设备**（9 个型号）：冷干机、过滤器、储气罐
- **定价规则**：折扣阶梯、运费、税费、安装费、延保费

## 报价流程 / Quotation Workflow

### 第一步：产品选型

根据客户需求推荐型号：

```
客户信息收集：
1. 用气量需求（m³/min）或 功率需求（kW）
2. 工作压力（bar）
3. 预算倾向：经济型 / 高效节能型 / 高端定制型
4. 是否有激光切割等特殊用途

→ 从 products.yaml 匹配推荐型号
→ 如果客户直接指定型号，跳过此步
```

### 第二步：后处理配套

根据主机型号自动匹配后处理：

```
推荐配置：
- 冷冻干燥机（标配）→ 按主机排气量匹配 compatible_with
- 精密过滤器（标配）→ 三级过滤 C/T/A
- 储气罐（选配）→ 按排气量推荐容积
```

### 第三步：折扣计算

按定价规则 `discount_tiers` 阶梯计算：

| 设备总价（万元） | 折扣率 |
|-----------------|--------|
| < 10 | 无折扣 |
| 10-30 | 3% |
| 30-50 | 5% |
| 50-100 | 8% |
| ≥ 100 | 10% |

> 特殊折扣需人工审批，不在自动计算范围内。

### 第四步：费用叠加

```
设备总价 = Σ (主机价格 + 后处理价格)
折扣金额 = 设备总价 × 折扣率
折后总价 = 设备总价 - 折扣金额
运费     = freight 规则（200km内免费，超出5元/km）
安装调试 = 折后总价 × 3%（最低 1500 元）
备件包   = 0.18 万元（选配）
延保费   = 0.30 万元/年（选配）
不含税总价 = 折后总价 + 运费 + 安装调试 + 备件包 + 延保费
增值税   = 不含税总价 × 13%
含税总价 = 不含税总价 + 增值税
```

### 第五步：生成报价单

**Markdown 输出（默认）**：直接输出标准报价单

**HTML 输出（用户要求时）**：
1. 读取 `assets/quote-template.html` 模板
2. 替换所有 `{{占位符}}` 为实际数据
3. 输出自包含 HTML 文件

## 报价单模板 / Output Template

### Markdown 输出

```markdown
# 萤火虫空压机 报价单 / Quotation

**报价单号**：{{QUOTE_NO}}
**日期**：{{QUOTE_DATE}}
**有效期**：30 天

---

## 客户信息
- **客户名称**：{{CUSTOMER_NAME}}
- **联系人**：{{CONTACT_PERSON}}
- **联系电话**：{{CONTACT_PHONE}}
- **项目名称**：{{PROJECT_NAME}}

## 设备清单

| 序号 | 型号 | 名称 | 数量 | 单价(万元) | 金额(万元) |
|------|------|------|------|-----------|-----------|
{{LINE_ITEMS}}

| | | | **设备总价** | **{{TOTAL_PRICE}} 万元** |

## 费用明细

| 项目 | 金额(万元) | 备注 |
|------|-----------|------|
| 设备总价 | {{TOTAL_PRICE}} | |
| 折扣 ({{DISCOUNT_PCT}}%) | -{{DISCOUNT_AMOUNT}} | |
| 运费 | {{FREIGHT_AMOUNT}} | {{FREIGHT_NOTE}} |
| 安装调试费 | {{INSTALL_AMOUNT}} | 标准安装 |
{{OPTIONAL_FEES}}
| **不含税合计** | **{{SUBTOTAL}}** | |
| 增值税 (13%) | {{VAT_AMOUNT}} | |
| **含税总价** | **{{GRAND_TOTAL}} 万元** | |

## 商务条款

| 条款 | 内容 |
|------|------|
| 交货期 | {{LEAD_TIME}} 天 |
| 付款方式 | 合同签订预付 30%，发货前付 60%，验收后付 10% |
| 质保期 | {{WARRANTY}} 年 |
| 运输方式 | 汽运 |
| 安装调试 | 卖方负责，含设备就位、管道连接、调试运行 |
| 售后服务 | 24 小时响应，终身技术支持 |

## 联系方式

📞 **13825202084**（邹先生）
📧 aifirefly@163.com
🌐 www.fireflies.net.cn
📍 广州市

---
*本报价单由萤火虫空压机制作 | 报价有效期 30 天 | 最终价格以合同为准*
```

## 典型示例

### 示例 1：客户指定型号
```
用户："报个价，YDV-75 一台"
→ 匹配 YDV-75（16.50 万）
→ 推荐 HD-75 冷干机（1.50 万）+ PF-75 过滤器（0.45 万）
→ 设备总价 18.45 万 → 折扣 3% = -0.55 万
→ 选配储气罐 ST-3（1.10 万）+ 备件包（0.18 万）
→ 运费估算 0.15 万，安装 0.55 万
→ 含税总价 ≈ 22.3 万
→ 输出报价单
```

### 示例 2：按需求选型
```
用户："我需要一台 15m³/min 的空压机报价"
→ 匹配 YDV-75（14.0 m³/min，最接近）
→ 同上流程
```

## 关键规则

### 必须遵守
- 报价前确认客户需求（型号或用气量）
- 默认含税报价（增值税 13%）
- 报价单标注有效期 30 天
- 金额统一"万元"，精确到小数点后 2 位
- 始终附带公司联系方式

### 降级处理
- 如果用户只指定型号，自动推荐配套后处理
- 如果用户不知道型号，按排气量匹配最近型号
- 如遇特殊折扣要求，提示"该折扣需人工审批"
- Python 不可用时，Claude 直接读取 YAML 并心算报价

### 参考文件
- `data/products.yaml` — 每次报价必须读取，获取最新产品数据
- `references/pricing-rules.md` — 详细定价规则
- `assets/quote-template.html` — HTML 报价单模板（用户要求时读取）
- `scripts/calculate.py` — 报价验算脚本（可选）
