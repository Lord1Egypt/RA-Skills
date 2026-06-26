# SKU -> 电商套图流水线使用说明

脚本：`scripts/sku_to_ecommerce_kit.py`

## 目的

输入 SKU，自动：
1. 从数据库读取产品基础信息（标题、图片 URL、文案）
2. 调用 DesignKit 套图接口（style_create -> style_poll -> render_submit -> render_poll）
3. 输出 7-8 张套图结果（远端 URL + 本地下载路径）

## 先决条件

- 已配置 `DESIGNKIT_OPENCLAW_AK`
- 能访问数据库（默认读取 `workspace-codex/sql_flow/search_flow_yibai/.env`）
- Python 依赖：`psycopg2`

## 示例

### 1) 仅校验 SKU 数据能否读到（不生成套图）

```bash
python3 scripts/sku_to_ecommerce_kit.py \
  --sku 1413220188412 \
  --target-preset walmart \
  --dry-run
```

### 2) 生成 Walmart 套图（全流程）

```bash
python3 scripts/sku_to_ecommerce_kit.py \
  --sku 1413220188412 \
  --target-preset walmart
```

### 3) 生成 MercadoLibre 套图（全流程）

```bash
python3 scripts/sku_to_ecommerce_kit.py \
  --sku 1413220188412 \
  --target-preset mercadolibre
```

### 4) 指定输出目录

```bash
python3 scripts/sku_to_ecommerce_kit.py \
  --sku 1413220188412 \
  --target-preset walmart \
  --output-dir /root/.openclaw/workspace-main/output/walmart
```

## 输出字段

成功时返回 JSON（关键字段）：

- `sku`
- `title`
- `image_url`
- `selling_points`
- `styles_count`
- `media_urls`（远端图片）
- `local_paths`（本地下载路径）
- `output_dir`

## 说明

- `--target-preset walmart` 会自动映射到 amazon+US+English+1:1，并注入 Walmart 主图规范。
- `--target-preset mercadolibre` 会自动映射到 amazon+ES+Spanish+1:1，并注入 MercadoLibre 风格约束。
