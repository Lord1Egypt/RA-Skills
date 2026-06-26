# 懂车帝品牌全量数据提取 — 开发步骤与思路

## 背景

`car-cli` 的懂车帝适配器需要一张 **品牌中文名 → 品牌数字 ID** 的映射表，用于构建搜索 URL 的第 19 号路径槽位。初版仅收录了约 70 个热门品牌，来源是页面 `__NEXT_DATA__` 中 `pageProps.list`（`type: 1001` 的品牌推荐卡片），遗漏了大量品牌。

本文档记录将品牌表从 ~70 条扩充到 651 条的完整过程。

---

## 第一步：确认 URL 槽位映射

### 问题

之前的实现中，各路径槽位的对应关系有误（如品牌曾错放到槽位 0）。需要先用浏览器实测确认。

### 方法

使用 `cursor-ide-browser` MCP 工具，在浏览器中依次点击不同筛选条件，观察 URL 变化：

1. **默认页**：`/usedcar/x-x-x-x-...-x-110000-1-x-x-x-x-x`（28 段，全部为 `x`，仅城市和页码有值）
2. **点击"宝马"**：URL 变为 `/usedcar/x-x-...-x-4-x-110000-1-x-x-x-x-x`，宝马 ID `4` 出现在第 19 段
3. **点击"5-10万"**：URL 变为 `/usedcar/5,10-x-...-x-x-110000-1-x-x-x-x-x`，价格 `5,10` 出现在第 0 段
4. **叠加品牌+价格**：URL 为 `/usedcar/5,10-x-...-x-4-x-110000-1-x-x-x-x-x`，页面标题确认为"5-10万左右的二手宝马推荐"

### 结论

| 槽位索引 | 含义 | 示例值 |
|---------|------|--------|
| 0 | 价格范围（万元） | `5,10` |
| 1–18 | 其他筛选（车型、燃料、年份、里程等） | `x` |
| 19 | 品牌 ID | `4`（宝马） |
| 20 | 车系 ID | `x` |
| 21 | 城市行政区划码 | `110000`（北京） |
| 22 | 页码 | `1` |
| 23–27 | 保留 | `x` |

对应代码常量：

```python
_NUM_SLOTS = 28
_SLOT_PRICE = 0
_SLOT_BRAND = 19
_SLOT_SERIES = 20
_SLOT_CITY = 21
_SLOT_PAGE = 22
```

---

## 第二步：分析旧品牌数据的不足

### 旧方案

品牌表来自 `__NEXT_DATA__` 的 `pageProps.list`，筛选 `type == 1001` 的条目。该列表是**首页推荐的热门品牌卡片**，仅约 20 个品牌；加上手动补充，总共约 70 个。

### 缺失内容

- 新势力：深蓝、岚图、智己、飞凡、仰望、方程豹、极越、iCAR、乐道、享界等
- 传统国产：东风风行、北京汽车、海马、力帆、陆风等
- 子品牌：吉利银河、长安启源、奇瑞风云、捷途山海等
- 进口/小众：迈凯伦、科尼赛克、布加迪、帕加尼等
- 房车品牌、改装品牌、历史品牌等

---

## 第三步：寻找完整品牌数据源

### 尝试 1：curl 直接请求页面 HTML

```bash
curl -s 'https://www.dongchedi.com/usedcar/...' \
  -H 'User-Agent: ...' | python3 parse_next_data.py
```

**结果**：`__NEXT_DATA__` script 标签未出现在响应中。推测服务端对非浏览器请求返回了精简版 HTML 或触发了反爬机制。

### 尝试 2：猜测 API 端点

```bash
curl -s 'https://www.dongchedi.com/motor/pc/sh/sh_brand_list?aid=1839&app_name=auto_web_pc'
curl -s 'https://www.dongchedi.com/motor/pc/sh/brand_list?aid=1839&app_name=auto_web_pc'
```

**结果**：均返回空响应，这些端点不存在或需要特殊鉴权。

### 尝试 3：浏览器 UI 提取

通过 `cursor-ide-browser` 点击品牌展开面板，发现：

- 热门品牌区域使用 `<a>` 链接（role: link），可通过 `browser_get_attribute` 获取 `href`
- 完整 A–Z 品牌面板使用 `<li>` 列表项（role: listitem），**没有 href 属性**
- 无法执行页面内 JavaScript（MCP 无 `browser_javascript` 工具）

逐个获取 300+ 品牌的 href 不现实，此路不通。

### 尝试 4（成功）：Playwright 提取 `__NEXT_DATA__`

使用 Python Playwright 库，以真实 Chromium 浏览器加载页面，然后从 DOM 中读取 `<script id="__NEXT_DATA__">` 的文本内容：

```python
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.dongchedi.com/usedcar/x-x-...-110000-1-x-x-x-x-x",
              wait_until="networkidle")

    el = page.query_selector("#__NEXT_DATA__")
    data = json.loads(el.text_content())
    pp = data["props"]["pageProps"]
    # pp["brands"] 包含完整的 A-Z 品牌列表
```

**结果**：成功获取 `pageProps`，其中包含关键字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `brands` | `list[list[dict]]` | 按首字母分组的完整品牌列表（27 组，A–Z） |
| `allBrand` | `dict` | 包含 `brand`、`hot_brand`、`new_energy_hot_brand` |
| `tabData` | `dict` | 包含 `car_brand_list`、`car_series_list` |
| `list` | `list[dict]` | 首页推荐卡片（旧数据源） |

---

## 第四步：提取品牌映射

### 数据结构

`pageProps.brands` 是一个二维列表，外层按字母分 27 组：

```python
[
    [  # A 组
        {"type": 1000, "info": {"pinyin": "A"}},        # 字母分隔符
        {"type": 1001, "info": {"brand_id": 2, "brand_name": "奥迪", ...}},
        {"type": 1001, "info": {"brand_id": 483, "brand_name": "AITO", ...}},
        ...
    ],
    [  # B 组
        {"type": 1000, "info": {"pinyin": "B"}},
        {"type": 1001, "info": {"brand_id": 3, "brand_name": "奔驰", ...}},
        ...
    ],
    ...
]
```

### 提取逻辑

```python
brand_map = {}
for group in pp["brands"]:
    for item in group:
        if item.get("type") == 1001:
            info = item["info"]
            brand_map[info["brand_name"]] = str(info["brand_id"])
```

提取结果：**640 个品牌**。

---

## 第五步：更新代码

### 修改文件

`src/car_cli/models/cities.py` 中的 `BRAND_IDS` 字典：

- 替换原有 ~70 条为完整的 640 条
- 保留并扩充常用别名（如 `"吉利"` → `"73"`、`"问界"` → `"483"`）
- 新增别名：`"极狐"`、`"赛力斯"`、`"极星"`、`"几何"`

最终字典包含 **651 条**（640 个正式名称 + 11 个别名）。

### 验证

测试之前缺失的品牌能否正常搜索：

```bash
$ car search --city 北京 --brand 深蓝汽车
# ✓ 返回深蓝L07、深蓝G318、深蓝SL03 等结果

$ car search --city 北京 --brand 岚图
# ✓ 返回岚图FREE、岚图梦想家等结果
```

---

## 技术要点总结

1. **`__NEXT_DATA__` 是核心数据源**：懂车帝使用 Next.js SSR，服务端数据序列化在 `<script id="__NEXT_DATA__">` 中。但该标签的内容对 curl/httpx 等脚本请求可能不可见，需要真实浏览器渲染。

2. **Playwright 绕过反爬**：相比 `requests`/`httpx`，Playwright 启动真实 Chromium，能获取完整的 SSR 输出，包括 `__NEXT_DATA__`。

3. **`pageProps.brands` vs `pageProps.list`**：
   - `list` 仅包含首页推荐的 20 余个品牌卡片
   - `brands` 包含按 A–Z 分组的全部 640 个品牌

4. **品牌 ID 为整数字符串**：大部分 ID 在 1–1000 范围内，部分新品牌（房车、进口小众品牌）ID 在 10000+ 范围。

5. **静态字典的局限**：当前方案仍是静态硬编码。如需自动更新，可在运行时用 Playwright 或 headless 请求动态获取。

---

## 依赖

- `playwright`：需安装 Python 包及 Chromium 浏览器
  ```bash
  pip install playwright
  python -m playwright install chromium
  ```

## 时间线

- **2026-03-23**：完成全量品牌提取，从 ~70 扩充到 651 条
