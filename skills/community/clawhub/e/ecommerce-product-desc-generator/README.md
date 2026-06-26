# 🛒 电商产品描述批量生成器

为电商卖家打造的**一键多平台产品描述生成工具**。支持亚马逊、淘宝、拼多多、TikTok Shop、Shopify 五大平台，输入产品名称即可生成各平台适配的标题、卖点描述和详情页文案。

**无需 API，即装即用。**

---

## ✨ 功能特点

- 🌐 **5大平台覆盖**：亚马逊（英文）、淘宝（中文）、拼多多（中文）、TikTok Shop（口语英文）、Shopify（品牌英文）
- 📦 **批量生成**：CSV 导入，一次生成多产品描述
- 📝 **平台适配**：每个平台使用对应的文案风格和格式
- 📁 **多格式导出**：Markdown / TXT / CSV
- 🔄 **可复现**：支持随机种子，确保结果可重现
- ⚡ **纯本地**：无需网络，无需 API Key

---

## 📦 安装

```bash
# 克隆项目
git clone <repo-url>
cd ecommerce-product-desc-generator

# 安装（如需要）
pip install -r requirements.txt

# 直接运行
python cli.py --help
```

---

## 🚀 快速开始

### 单产品生成（单平台）

```bash
# 亚马逊英文文案
python cli.py "蓝牙耳机" "3C数码" --keywords "无线,降噪,运动" --platforms amazon

# 淘宝中文文案
python cli.py "真丝围巾" "服饰" --keywords "保暖,高档" --platforms taobao
```

### 单产品生成（全平台）

```bash
python cli.py "蓝牙耳机" "3C数码" --keywords "无线,降噪" --all-platforms
```

### 指定输出格式

```bash
python cli.py "充电宝" "电子产品" --all-platforms --format txt --output desc.txt
python cli.py "充电宝" "电子产品" --all-platforms --format csv --output desc.csv
```

### 批量生成（CSV）

准备 `products.csv`：
```csv
product_name,category,keywords,brand,price
蓝牙耳机,3C数码,无线,某品牌,199
充电宝,电子产品,大容量,某品牌,89
真丝围巾,服饰,保暖,某品牌,299
```

运行：
```bash
python cli.py --csv products.csv --format markdown --output result.md
```

---

## 📋 输出示例

### 亚马逊输出（Markdown）

```markdown
## 🏪 亚马逊

**标题**: Premium 蓝牙耳机 - Multifunctional High-Quality Stainless Steel for Home & Everyday Use

**卖点 (Bullet Points)**:
1. **PREMIUM QUALITY**: High-Quality Stainless Steel ensures durability and long-lasting performance...
2. **EASY TO USE**: Waterproof design allows effortless operation — perfect for Home...
...
```

### 淘宝输出（Markdown）

```markdown
## 🏪 淘宝

**标题**: 【热卖】蓝牙耳机防水优质 不锈钢 3C数码

**详情描述**:
【产品名称】蓝牙耳机

【产品特点】
✨ 便携式设计，简约时尚
✨ 优质不锈钢，坚固耐用
...
```

---

## 🧪 运行测试

```bash
pytest tests/test_generator.py -v
```

---

## 🏗️ 项目结构

```
ecommerce-product-desc-generator/
├── generator.py        # 核心生成引擎
├── cli.py              # CLI 入口
├── tests/
│   └── test_generator.py
├── requirements.txt
├── SKILL.md            # ClawHub 发布用
└── README.md
```

---

## 💡 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| Free | 免费 | 单产品单平台生成 |
| Pro | ¥29/月 | 批量生成（50产品/次），全平台，CSV 导入导出 |
| Team | ¥99/月 | 无限生成，API 调用，白标定制 |

---

## 📝 许可

MIT License
