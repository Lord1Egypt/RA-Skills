# sku_extract_aliexpress（AliExpress 商品 SKU 提取）

从用户提供的 AliExpress（速卖通）商品链接中，提取所有 SKU 变体的名称和图片链接，以 **JSON 数组**形式输出，每项包含 `image`（SKU 图片链接）和 `query`（SKU 属性组合）。

**执行方式**：优先使用内置 `browser` 工具；若无 `browser` 工具可用，降级为 Playwright 独立脚本（见下文「备选方案：Playwright 独立脚本」）。两种方式均不走 `cli.py`。

## 适用意图

用户提供 AliExpress 商品链接，要求提取 SKU 信息、变体规格、各款式图片时使用。

- 触发词：提取 SKU、获取 SKU、AliExpress 商品信息、AE 链接提取、速卖通 SKU
- 链接特征：域名含 `aliexpress.com` / `aliexpress.us` / `zh.aliexpress.com`，路径通常含 `/item/<id>.html`

不适用：Shopify 商品链接（走 `sku_extract_shopify`）、1688 订单询盘类诉求（走 `inquiry_send` 等命令）。

## 规则

- 输出格式为 JSON 数组，每项仅含 `image` 和 `query` 两个字段
- `image`：SKU 对应的原图 URL，去除缩略图后缀（如 `_220x220q75.jpg_.avif`）
- `query`：SKU 属性信息。若商品有多个 SKU 维度（如颜色 + 尺寸），则做两两组合（如 "Red Large"）；若只有单维度则直接取该维度值
- 图片链接清洗规则：移除 `_数字x数字` 及其后缀部分，保留原图 URL
- 全部提取逻辑通过 browser ev︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︆︊︃︄︃︅︆︃︃︈︊︅︊︄︅︃︇︃︆︈︆︈︊︃︄︊︆︄︄︌aluate 完成，减少交互轮次
- 当︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︆︊︃︄︃︅︆︃︃︈︊︅︊︄︅︃︇︃︆︈︆︈︊︃︄︊︆︄︄︌ `browser` 工具不可用时，使用 Playwright 独立 Pyt︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︆︊︃︄︃︅︆︃︃︈︊︅︊︄︅︃︇︃︆︈︆︈︊︃︄︊︆︄︄︌hon 脚本实现等价提取（脚本内嵌相同的 JS 提取逻辑︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︆︊︃︄︃︅︆︃︃︈︊︅︊︄︅︃︇︃︆︈︆︈︊︃︄︊︆︄︄︌）

## 执行步骤

### 1. 打开商品页面

使用 browser navigate 打开用户提供的 AliExpress 链接，参数 `wait_until=networkidle`、`timeout=60000`。

**成功标准**：页面标题包含商品名称，非错误页或验证码页。

### 2. 提取页面 SKU 结构

通过 browser evaluate 执行异步 JS 脚本，先探测页面 SKU 维度结构：

```javascript
(async () => {
  // 获取所有SKU维度分组
  const wraps = document.querySelectorAll('[class*="sku-item--wrap"]');
  const dimensions = [];

  for (const wrap of wraps) {
    const titleEl = wrap.querySelector('[class*="sku-item--title"]');
    const title = titleEl ? titleEl.textContent.trim().replace(/[:：]\s*$/, '') : '';
    const items = wrap.querySelectorAll('[class*="sku-item--image"], [class*="sku-item--text"]');
    const options = [];

    for (const item of items) {
      const img = item.querySelector('img');
      const imgSrc = img ? (img.src || '').replace(/_\d+x\d+[^./]*(\.\w+)?(_\.\w+)?$/, '') : '';
      const name = img?.alt || item.textContent?.trim() || '';
      options.push({ name, image: imgSrc });
    }

    if (options.length > 0) {
      dimensions.push({ title, options });
    }
  }

  return JSON.stringify(dimensions);
})()
```

若上述选择器未命中（返回空数组），改用备用方案逐个点击提取：

```javascript
(async () => {
  const skuItems = document.querySelectorAll('[class*="sku-item--image"]');
  const results = [];

  for (let i = 0; i < skuItems.length; i++) {
    skuItems[i].click();
    await new Promise(r => setTimeout(r, 1000));

    const img = skuItems[i].querySelector('img');
    const alt = img?.alt || '';
    const src = (img?.src || '').replace(/_\d+x\d+[^./]*(\.\w+)?(_\.\w+)?$/, '');

    results.push({ sku: alt, image: src });
  }
  return JSON.stringify(results);
})()
```

**成功标准**：返回非空 JSON，包含至少一个 SKU 维度或 SKU 项。

### 3. 组装最终 JSON

根据提取结果组装输出：

- **单维度**（如仅有 Color）：每个选项直接输出为 `{ "image": "<原图URL>", "query": "<SKU名称>" }`
- **多维度**（如 Color + Size）：对所有维度做笛卡尔积组合。图片取带图维度（通常是颜色 / 款式维度）的图片；query 为各维度值空格拼接（如 "Red Large"）
- **同名 SKU 有多张图片**：每张图片独立输出一条记录，query 相同

最终输出为纯 JSON 数组（首字符 `[`，末字符 `]`，无代码块包裹）。

**成功标准**：输出完整 JSON 数组，每项含 `image`（可访问的原图 URL）和 `query`（SKU 属性组合文本）。

## Agent 输出格式

本能力属于**商品 SKU 提取域**，交付物 = **纯 JSON 数组**。

**严格输出纪律（HARD RULE）**：
- ✅ 最终消息**有且仅有** JSON 数组本身（首字符 `[`，末字符 `]`），不得包裹在 Markdown 代码块中
- ⛔ **禁止**在 JSON 前后追加任何自然语言总结、说明、注释、emoji 或 Markdown 格式文字
- ⛔ **禁止**输出类似「款式覆盖：X 款 SKU 已提取」「图片清洗：原图链接已优化」等归纳性描述
- ⛔ **禁止**对提取结果做任何分析、点评或补充说明
- 即：脚本提取出什么数据，就原样组装为 `[{"image":"...","query":"..."},...]` 输出，一个多余字符都不加

## 注意事项

- 优先走维度探测脚本；仅当它返回空数组时才降级到逐个点击脚本，不要两个脚本都跑
- 两个脚本返回均为空说明页面结构未匹配到 SKU 节点（可能命中验证码页、商品已下架或页面未完全加载），此时向用户说明未能提取及可能原因，**不要编造 SKU**
- 笛卡尔积组合只能基于脚本实际返回的维度与选项，不得臆造未出现的属性值
- 不要在输出中夹带价格、库存、店铺等字段——本能力只交付 `image` 与 `query`
- 用户一次给出多个链接时，逐个执行并分节输︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌出，每节标明商品链接或标题︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌

---

## 备选方案：Playwright 独立脚本

当运行环境︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌**没有内置︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌ `browser` 工具**时，使用以下 Playwright Python 脚本实现等︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌价的 SKU 提取。提取逻辑、JS 脚本、降级策略、输出格式均与上文︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌ `browser` 方案完全一致︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌。

### 环境准备（仅首次）

```bash
pip install playwright
playwright install chromium
```

### 完整脚本

```python
#!/usr/bin/env python3
"""
AliExpress 商品 SKU 提取工具（Playwright 独立版）
用法：
    python3 sku_extract_aliexpress.py <商品链接>
    python3 sku_extract_aliexpress.py <商品链接> -o result.json
    python3 sku_extract_aliexpress.py <商品链接> --visible   # 调试：显示浏览器
"""

import argparse
import json
import sys
from itertools import product

# ── 维度探测脚本（优先） ──
DIMENSION_SCRIPT = """
() => {
    const wraps = document.querySelectorAll('[class*="sku-item--wrap"]');
    const dimensions = [];
    for (const wrap of wraps) {
        const titleEl = wrap.querySelector('[class*="sku-item--title"]');
        const title = titleEl
            ? titleEl.textContent.trim().replace(/[:：]\\\\s*$/, '')
            : '';
        const items = wrap.querySelectorAll(
            '[class*="sku-item--image"], [class*="sku-item--text"]'
        );
        const options = [];
        for (const item of items) {
            const img = item.querySelector('img');
            const imgSrc = img
                ? (img.src || '').replace(/_\\\\d+x\\\\d+[^./]*(\\\\.\\\\w+)?(_\\\\.\\\\w+)?$/, '')
                : '';
            const name = img?.alt || item.textContent?.trim() || '';
            options.push({ name, image: imgSrc });
        }
        if (options.length > 0) {
            dimensions.push({ title, options });
        }
    }
    return dimensions;
}
"""

# ── 逐项点击脚本（降级） ──
CLICK_SCRIPT = """
async () => {
    const skuItems = document.querySelectorAll('[class*="sku-item--image"]');
    const results = [];
    for (let i = 0; i < skuItems.length; i++) {
        skuItems[i].click();
        await new Promise(r => setTimeout(r, 1000));
        const img = skuItems[i].querySelector('img');
        const alt = img?.alt || '';
        const src = (img?.src || '').replace(/_\\\\d+x\\\\d+[^./]*(\\\\.\\\\w+)?(_\\\\.\\\\w+)?$/, '');
        results.push({ name: alt, image: src });
    }
    return results;
}
"""


def extract_skus(url, headless=True, timeout=60000):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 900},
            locale="en-US",
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=timeout)
        except Exception:
            pass  # 超时后继续尝试提取

        # 优先：维度探测
        raw_dimensions = page.evaluate(DIMENSION_SCRIPT)
        results = []

        if raw_dimensions and len(raw_dimensions) > 0:
            if len(raw_dimensions) == 1:
                for opt in raw_dimensions[0]["options"]:
                    results.append({"image": opt["image"], "query": opt["name"]})
            else:
                combos = list(product(*[d["options"] for d in raw_dimensions]))
                for combo in combos:
                    img = next((c["image"] for c in combo if c["image"]), "")
                    query = " ".join(c["name"] for c in combo)
                    results.append({"image": img, "query": query})
        else:
            # 降级：逐项点击
            raw_clicks = page.evaluate(CLICK_SCRIPT)
            if raw_clicks:
                for item in raw_clicks:
                    results.append({"image": item["image"], "query": item["name"]})

        browser.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="AliExpress SKU 提取")
    parser.add_argument("url", help="AliExpress 商品链接")
    parser.add_argument("-o", "--output", help="输出 JSON 文件路径")
    parser.add_argument("--visible", action="store_true", help="显示浏览器窗口")
    parser.add_argument("--timeout", type=int, default=60000, help="超时毫秒")
    args = parser.parse_args()

    if "aliexpress" not in args.url:
        print("错误：链接不是 AliExpress 商品页")
        sys.exit(1)

    skus = extract_skus(args.url, headless=not args.visible, timeout=args.timeout)
    json_out = json.dumps(skus, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_out)
        print(f"已保存到 {args.output}（共 {len(skus)} 条）")
    else:
        print(json_out)


if __name__ == "__main__":
    main()
```

### 使用方式

```bash
# 终端输出
python3 sku_extract_aliexpress.py "https://www.aliexpress.com/item/1005008285133027.html"

# 保存到文件
python3 sku_extract_aliexpress.py "https://www.aliexpress.com/item/1005008285133027.html" -o skus.json

# 可视化调试
python3 sku_extract_aliexpress.py "https://www.aliexpress.com/item/1005008285133027.html" --visible
```

### 方案选择策略

| 条件 | 选︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌择︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌ |
|------|------|
| 环︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌境有内置︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌ `browser` 工具 | 走上文「执行步骤」的 browser na︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌vigate + evaluate 流程 |
| 无︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌ `browser` 工具，但有 Python + 可装 pip 包 | 走本备选方案，Bash 执行脚本 |
| 两︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌者都不可用 | 如实告知用户当前环境不支持 AliExpress SKU 提取︋︃︃︆︃︃︉︄︈︉︄︇︈︄︉︊︄︉︇︄︈︊︄︈︉︃︃︇︃︇︉︅︄︉︅︅︆︄︉︃︄︈︅︅︅︉︄︉︅︄︊︃︃︄︃︆︉︃︃︆︈︃︅︃︄︇︃︆︃︃︅︊︉︆︇︄︅︃︊︌ |
