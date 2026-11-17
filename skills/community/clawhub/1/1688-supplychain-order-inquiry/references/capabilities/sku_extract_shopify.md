# sku_extract_shopify（Shopify 商品 SKU 提取）

从用户提供的 Shopify 商品链接中，通过访问商品 JSON API 提取所有 SKU 变体信息，以 **JSON 数组**格式输出，每个 SKU 包含 `image`（图片链接）和 `query`（SKU 属性组合，多个属性用逗号分割）两个字段。

**执行方式**：优先使用内置 `browser` 工具；若无 `browser` 工具可用，降级为纯 HTTP 的 Python 脚本（基于 `requests`，无需浏览器，见下文「备选方案：纯 HTTP Python 脚本」）。两种方式均不走 `cli.py`。

> **Shopify 特有优势**：Shopify 商品页原生支持 `<商品URL>.json` API，纯 HTTP GET 即可获取完整变体数据，**无需 Playwright 或任何浏览器渲染**，比 AliExpress 方案轻量得多。

## 适用意图

用户提供 Shopify 店铺的商品链接，希望获取该商品的 SKU / 变体信息时使用。

- 触发词：获取 SKU、提取 SKU、提取变体、Shopify 商品信息、SKU 信息、变体规格
- 链接特征：Shopify 独立站商品页，路径通常含 `/products/<handle>`；域名可为 `*.myshopify.com` 或自定义域名

不适用：AliExpress / 速卖通链接（走 `sku_extract_aliexpress`）、1688 订单询盘类诉求（走 `inquiry_send` 等命令）。

## 规则

- 最终输出为 JSON 数组，每个元素代表一个 SKU 粒度的变体，包含两个字段：
  - `image`：该 SKU 对应的图片原图 URL（去除 Shopify CDN 尺寸后缀如 `_720x` 等）
  - `query`：该 SKU 的属性组合，多个属性（如颜色、尺寸）用英文逗号分割，例如 `"Grøn,38"`
- 不输出店铺信息、商品描述、价格、库存等无关内容
- 每个变体独立一条记录，不做分组合并

## 执行步骤

### 1. 打开商品页面

使用 browser navigate 打开用户提供的 Shopify 商品链接，参数 `wait_until=networkidle`、`timeout=60000`。

**成功标准**：页面标题非空，非 404 页面。

### 2. 通过 JSON API 提取商品数据

Shopify 店铺的商品页面支持在 URL 末尾追加 `.json` 获取结构化数据。使用 browser evaluate 执行异步脚本（内含三级降级：product.json API → 页面内嵌 JSON → ShopifyAnalytics meta）：

```javascript
(async () => {
  // 方法1：尝试 product.json API
  const path = window.location.pathname.replace(/\/$/, '');
  const resp = await fetch(path + '.json');
  if (resp.ok) {
    const json = await resp.json();
    const product = json.product;
    const variants = product.variants || [];
    const images = product.images || [];

    // 构建 variant_id → image 映射
    const variantImageMap = {};
    for (const img of images) {
      if (img.variant_ids && img.variant_ids.length > 0) {
        for (const vid of img.variant_ids) {
          variantImageMap[vid] = img.src;
        }
      }
    }

    const results = variants.map(v => ({
      title: v.title || v.public_title || '',
      price: v.price,
      sku: v.sku || null,
      available: v.available,
      image: variantImageMap[v.id] || (images.length > 0 ? images[0].src : null)
    }));

    return JSON.stringify({
      success: true,
      productTitle: product.title,
      vendor: product.vendor,
      totalVariants: variants.length,
      variants: results
    });
  }

  // 方法2：从页面内嵌JSON中提取
  const scripts = document.querySelectorAll('script[type="application/json"]');
  for (const script of scripts) {
    try {
      const data = JSON.parse(script.textContent);
      if (data.product && data.product.variants) {
        const variants = data.product.variants;
        return JSON.stringify({
          success: true,
          productTitle: data.product.title,
          vendor: data.product.vendor,
          totalVariants: variants.length,
          variants: variants.map(v => ({
            title: v.title || v.public_title || v.name || '',
            price: v.price,
            sku: v.sku || null,
            available: v.available !== false,
            image: null
          }))
        });
      }
    } catch(e) {}
  }

  // 方法3：从 ShopifyAnalytics meta 提取
  if (window.ShopifyAnalytics && window.ShopifyAnalytics.meta && window.ShopifyAnalytics.meta.product) {
    const meta = window.ShopifyAnalytics.meta.product;
    return JSON.stringify({
      success: true,
      productTitle: meta.type || 'Unknown',
      vendor: meta.vendor || '',
      totalVariants: (meta.variants || []).length,
      variants: (meta.variants || []).map(v => ({
        title: v.name || v.public_title || '',
        price: v.price,
        sku: v.sku || null,
        available: true,
        image: null
      }))
    });
  }

  return JSON.stringify({ success: false, error: '无法从页面提取商品变体数据' });
})()
```

**成功标准**：返回的 JSON 中 `success` 为 true，且 `variants` 数组非空。

> 脚本返回体中还带有 `price`、`sku`、`available` 等字段，属于历史遗留，**第 3 步一律忽略**，只取 `title` 与 `image`。

### 3. 输出结果

将提取的数据整理为 JSON 数组输出，每个 SKU 变体对应一条记录：

- **图片处理**：去除 URL 中的 CDN 尺寸后缀（如 `_720x`），保留原图链接；无图片时值为 `null`
- **query 组合**：取变体 title 中 ` / ` 分隔的各属性，用英文逗号拼接。例如 title 为 `"Grøn / 38"` → query 为 `"Grøn,38"`；title 为 `"Default Title"` → query 为 `"Default Title"`

输出格式示例：

```json
[
  {"image": "https://cdn.shopify.com/s/files/1/xxx/files/photo.jpg?v=123", "query": "Grøn,35"},
  {"image": "https://cdn.shopify.com/s/files/1/xxx/files/photo.jpg?v=123", "query": "Grøn,36"}
]
```

**禁止**附加汇总行或任何自然语言文字。最终输出仅为裸 JSON 数组（首字符 `[`，末字符 `]`），不包裹代码块标记、不附加任何说明。

**成功标准**：输出包含所有变体的完整 JSON 数组，每条记录的 image 和 query 字段准确无误。

## Agent 输出格式

本能力属于**商品 SKU 提取域**，交付物 = **纯 JSON 数组**（无︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︄︃︇︆︅︄︃︆︈︄︅︆︄︈︅︅︅︉︅︄︉︆︅︄︃︄︃︄︇︃︆︆︆︄︆︉︃︈︄︅︅︇︃︉︉︃︅︆︄︊︇︌代码块包裹、无汇总、无任何附加文字），与域 A 的纯 JSON 契约对齐︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︄︃︇︆︅︄︃︆︈︄︅︆︄︈︅︅︅︉︅︄︉︆︅︄︃︄︃︄︇︃︆︆︆︄︆︉︃︈︄︅︅︇︃︉︉︃︅︆︄︊︇︌。

## 注意事项

- 脚本三级降级依次尝试，任一级成功即返回；全部失败返回 `{"success": false, "error": "..."}`，此时向用户说明未能提取并给出可能原因（非 Shopify 站点 / 页面需登录 / 链接失效）
- 不要为了「凑数」编造变体、图片链接或属性组合，所有字段必须来自脚本返回
- 不要在输出中夹带价格、库存、店铺、商品描述等字段——本能力只交付 `image` 与 `query`
- 用户一次给出多个链接时，逐个执行并分节︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌输出，每节标明商品标题︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌

---

## 备选方案：纯 HTTP Python 脚本

当运行环境︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌**没有内置︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `browser` 工具**时，使用以下纯 HTTP Python 脚本︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌实现等价的 SKU 提取。利用 Shopify 原生︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `.json` API，**仅︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌依赖︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `requests`，无需 Playwright 或任何浏览器**，响应速度︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ < 2 秒。

提取逻辑、降级策略、输出格式均与上文︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `browser` 方案完全一致︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌。

### 环境准备

```bash
# requests 通常已预装；若未安装：
pip install requests
```

### 完整脚本

```python
#!/usr/bin/env python3
"""
Shopify 商品 SKU 提取工具（纯 HTTP 版，无需浏览器）
用法：
    python3 sku_extract_shopify.py <商品链接>
    python3 sku_extract_shopify.py <商品链接> -o result.json
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse

import requests


def clean_image_url(url):
    """移除 Shopify CDN 尺寸后缀（如 _720x、_480x480）"""
    if not url:
        return None
    return re.sub(r'_\d+x\d*', '', url)


def _find_product(obj, depth=0):
    """递归查找包含 variants 数组的 product 对象"""
    if depth > 5:
        return None
    if isinstance(obj, dict):
        if "variants" in obj and isinstance(obj["variants"], list):
            return obj
        if "product" in obj and isinstance(obj["product"], dict):
            return _find_product(obj["product"], depth + 1)
        for v in obj.values():
            result = _find_product(v, depth + 1)
            if result:
                return result
    return None


def _parse_product(product):
    """将 Shopify product 对象转为 image + query 标准输出"""
    title = product.get("title", "Unknown")
    variants = product.get("variants", [])
    images = product.get("images", [])

    # variant_id → image 映射
    variant_image_map = {}
    for img in images:
        src = clean_image_url(img.get("src", ""))
        for vid in img.get("variant_ids", []):
            variant_image_map[vid] = src

    default_image = clean_image_url(images[0]["src"]) if images else None

    skus = []
    for v in variants:
        image = variant_image_map.get(v.get("id")) or default_image
        raw_title = v.get("title") or v.get("public_title") or v.get("name") or ""
        query = ",".join(part.strip() for part in raw_title.split(" / "))
        skus.append({"image": image, "query": query})

    return {"success": True, "product_title": title, "skus": skus}


def extract_skus(url, timeout=30):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    if not path.startswith("/products/"):
        return {"success": False, "skus": [],
                "error": "链接路径不含 /products/<handle>，非 Shopify 商品页"}

    # ── 方法1：product.json API（推荐） ──
    json_url = f"{parsed.scheme}://{parsed.netloc}{path}.json"
    try:
        resp = requests.get(json_url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            product = resp.json().get("product", {})
            return _parse_product(product)
    except requests.RequestException:
        pass

    # ── 方法2：从 HTML 页面内嵌 JSON 提取 ──
    page_url = f"{parsed.scheme}://{parsed.netloc}{path}"
    try:
        resp = requests.get(
            page_url,
            headers={**headers, "Accept": "text/html"},
            timeout=timeout,
        )
        resp.raise_for_status()
        html = resp.text

        # 尝试 <script type="application/json"> 标签
        json_blocks = re.findall(
            r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>',
            html, re.DOTALL,
        )
        for block in json_blocks:
            try:
                obj = json.loads(block)
                product = _find_product(obj)
                if product:
                    return _parse_product(product)
            except json.JSONDecodeError:
                continue

        # 尝试内嵌 JS 变量
        for pattern in [
            r'var\s+meta\s*=\s*(\{.*?"product".*?\});',
            r'"product"\s*:\s*(\{.*?"variants"\s*:\s*\[.*?\]\s*.*?\})',
        ]:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    obj = json.loads(match.group(1))
                    product = obj.get("product", obj)
                    if "variants" in product:
                        return _parse_product(product)
                except json.JSONDecodeError:
                    continue

    except requests.RequestException as e:
        return {"success": False, "skus": [], "error": f"请求失败: {e}"}

    return {"success": False, "skus": [], "error": "无法从页面提取商品变体数据"}


def main():
    parser = argparse.ArgumentParser(
        description="Shopify SKU 提取（纯 HTTP，无需浏览器）"
    )
    parser.add_argument("url", help="Shopify 商品链接")
    parser.add_argument("-o", "--output", help="输出 JSON 文件路径")
    parser.add_argument("--timeout", type=int, default=30, help="超时秒数")
    args = parser.parse_args()

    result = extract_skus(args.url, timeout=args.timeout)

    if not result["success"]:
        print(f"错误: {result.get('error', '未知')}")
        sys.exit(1)

    skus = result["skus"]
    json_out = json.dumps(skus, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_out)
        print(f"已保存到 {args.output}（共 {len(skus)} 条）")
    else:
        print(json_out)

    # 汇总
    colors, sizes = set(), set()
    for s in skus:
        parts = s["query"].split(",")
        if len(parts) >= 2:
            colors.add(parts[0]); sizes.add(parts[1])
        elif len(parts) == 1:
            colors.add(parts[0])
    summary = f"共 {len(skus)} 个 SKU"
    if colors and sizes:
        summary += f"，{len(colors)} 种颜色/款式 × {len(sizes)} 个尺码"
    print(summary)


if __name__ == "__main__":
    main()
```

### 使用方式

```bash
# 终端输出
python3 sku_extract_shopify.py "https://valmerecopenhagen.com/products/liliana-sko"

# 保存到文件
python3 sku_extract_shopify.py "https://valmerecopenhagen.com/products/liliana-sko" -o skus.json
```

### 方案选择策略

| 条件 | 选︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌择︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ |
|------|------|
| 环︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌境有内置︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `browser` 工具 | 走上文「执行步骤」的 browser na︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌vigate + evaluate 流程 |
| 无︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `browser` 工具，有 P︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ython︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ + `requests` | **优先走本方案**（纯 HTTP，无需浏览器，< 2 秒响应） |
| 两者︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌都不可用 | 如实告知用户当前环境不支持 Shopify SKU 提取︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ |

### 与 AliExpress 备选方案的差异

| 维度 | Shopify 备选方案︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ | AliExpress 备选方案︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ |
|------|-----------------|-------------------|
| **核心︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌依赖︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌** | `requests`（通常已预装） | Playwright + Chromium（~95MB） |
| **是否需要浏览器** | ❌ 不需︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌要 | ✅ 必须 |
| **速度** | < 2 秒 | 5-15 秒 |
| **原因** | Shopify 有原生︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ `.json` API | AliExpress︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ 纯客户端渲染，无公开 API︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︆︊︆︅︅︄︅︃︃︉︄︄︈︅︅︅︉︄︉︇︃︊︃︃︄︃︃︃︅︅︆︆︅︆︈︃︉︉︄︈︇︆︅︄︃︃︈︃︃︊︌ |
