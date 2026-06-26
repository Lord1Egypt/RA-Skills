# ecommerce-product-desc-generator — 电商产品描述批量生成器

## 痛点
- 每次上新都要手动写标题、bullet points、详情描述，效率低下
- 同一产品在不同平台要写不同风格的文案，工作量翻倍
- 跨境卖家需要英文文案，中文卖家需要本土化表达
- 批量上新时，文案写作成为瓶颈

## 场景
- 亚马逊卖家：快速生成 SEO 友好的英文标题 + 5点描述 + 详情
- 淘宝/拼多多卖家：一键生成中文卖点的标题和详情页文案
- TikTok Shop 卖家：生成短视频风格的种草文案
- Shopify 独立站卖家：生成品牌感强的产品页面描述
- 批量上新：CSV 导入产品列表，一次生成全平台描述

## 定价
- **Free（免费）**：单产品单平台生成，基础模板
- **Pro ¥29/月**：批量生成（50产品/次），全5大平台，支持 CSV 导入导出
- **Team ¥99/月**：无限生成，API 调用，白标定制

## 指令格式

### 单产品生成
```
ecommerce-product-desc "产品名称" "品类" --keywords "关键词" --platforms amazon,tiktok --format markdown
```

### 全平台生成
```
ecommerce-product-desc "蓝牙耳机" "3C数码" --keywords "无线,降噪" --all-platforms
```

### 指定平台（逗号分隔）
```
--platforms amazon,taobao,pinduoduo,tiktok,shopify
```

### 输出格式
- `--format markdown`（默认）：每个平台一个 Markdown 区块
- `--format txt`：纯文本，平台间用 `===` 分隔
- `--format csv`：CSV 表格，含平台/标题/卖点/详情

### 批量生成（CSV）
```
ecommerce-product-desc --csv products.csv --format markdown --output result.md
```

CSV 格式（支持中文列名或英文列名）：
```
product_name,category,keywords,brand,price
蓝牙耳机,3C数码,无线,品牌X,199
充电宝,电子产品,大容量,品牌Y,89
```

### 批量模式（命令行）
```
ecommerce-product-desc --batch --product "充电宝" "电子产品" --all-platforms
```

## 支持平台

| 平台 | 语言 | 标题长度 | 特点 |
|------|------|----------|------|
| `amazon` | 英文 | ≤200字符 | 5条Bullet Points + 详情段落，SEO优化 |
| `taobao` | 中文 | ≤30字 | Emoji+卖点，淘宝风格 |
| `pinduoduo` | 中文 | ≤30字 | 低价引流词前置，拼团风格 |
| `tiktok` | 英文 | ≤100字 | 口语化+emoji，种草短视频风格 |
| `shopify` | 英文 | 品牌感 | 章节化描述，适合独立站 |

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `product` | 是 | 产品名称 |
| `category` | 否 | 品类/类目 |
| `--keywords` | 否 | 关键词，多个用逗号分隔 |
| `--brand` | 否 | 品牌名 |
| `--price` | 否 | 目标价格 |
| `--platforms` | 否 | 目标平台，默认 all |
| `--format` | 否 | markdown/txt/csv，默认 markdown |
| `--output` | 否 | 输出文件路径 |
| `--seed` | 否 | 随机种子，用于复现结果 |
