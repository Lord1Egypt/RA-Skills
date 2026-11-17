# 前端上线手册（Storefront Launch Playbook）

> 配套 [skills/storefront-builder](../skills/storefront-builder/SKILL.md)。把「高转化电商前端」落成一份可勾选的上线清单，
> 含组件优先级、SEO 结构化数据、移动适配与性能门槛。子技能讲模式，本篇讲「上线前别漏」。

## 1. 决策树：先搭哪个组件？

```
新建站点？
 ├─ 是 → 按转化漏斗优先级：导航 → 商品列表 → 商品详情 → 购物车 → 结账
 │        （前 3 个决定首屏体验，优先于购物车/结账）
 └─ 已有站点？
     ├─ 转化率低 → 先查商品详情页（画廊/变体/信任信号）
     ├─ 弃单高   → 先查结账流程（步骤数/移动适配）
     └─ 流量大但无单 → 先查 SEO 与首屏性能（LCP）

后端来源？
 ├─ Shopify Storefront API → 用其 GraphQL，注意 rate limit 与缓存
 ├─ Medusa                 → 直接调 `/store` 路由
 └─ 自定义 REST            → 封装数据层，隔离组件与接口
```

**原则**：框架无关。组件按「数据流契约」而非「框架 API」设计，便于平移到
Next.js / SvelteKit / Nuxt。

## 2. 选型矩阵：框架与渲染策略

| 框架 | 渲染 | 最适合 | SEO | 备注 |
|------|------|--------|-----|------|
| Next.js (App Router) | SSR/RSC | 内容型+交易型 | 强 | 默认选择，ISR 缓存商品页 |
| SvelteKit | SSR | 轻量高交互 | 强 | 包体小，TBT 低 |
| Nuxt (Vue) | SSR | Vue 团队 | 强 | 生态完整 |
| 纯 SPA (Vite+React) | CSR | 内部/低 SEO | 弱 | 需额外预渲染，不推荐电商主站 |

## 3. 可运行命令 / 代码

### 3.1 商品详情页 Product 结构化数据（JSON-LD）
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{ product.title }}",
  "image": ["{{ product.images[0] }}"],
  "description": "{{ product.description }}",
  "offers": {
    "@type": "Offer",
    "price": "{{ product.price }}",
    "priceCurrency": "{{ product.currency }}",
    "availability": "https://schema.org/InStock",
    "url": "{{ product.url }}"
  }
}
</script>
```
面包屑也加 `BreadcrumbList`，富媒体在搜索结果里提升点击率。

### 3.2 变体选择（框架无关伪码）
```ts
function selectVariant(variants, selected) {
  return variants.find(v =>
    v.options.every((opt, i) => opt.value === selected[i])
  ) ?? null;   // 找不到返回 null → UI 禁用「加入购物车」
}
// 关键：禁用不存在的 SKU 组合，避免下单后才发现无库存
```

### 3.3 移动端安全区与触控目标
```css
.add-to-cart {
  min-height: 44px;            /* 触控目标下限 */
  padding-bottom: env(safe-area-inset-bottom); /* iPhone 底部安全区 */
}
@media (max-width: 640px) {
  .checkout-steps { flex-direction: column; }
}
```

### 3.4 用脚本校验商品信息流（确定性，复用 assets 模板）
```bash
# 上线前先校验 CMS/ERP 导出的商品 CSV 是否缺字段或含占位符
python3 scripts/validate_product_feed.py --feed export/products.csv
# 退出码非 0 说明有缺陷，先修再发，避免脏数据进生产
```

## 4. 性能预算（确定性门槛）

| 指标 | 设备 | 良好线 | 合格线 | 测量 |
|------|------|--------|--------|------|
| LCP | 移动 4G | ≤2.5s | ≤4.0s | 字段 p75 |
| INP | 移动 | ≤200ms | ≤500ms | 字段 p75 |
| CLS | 全端 | ≤0.1 | ≤0.25 | 字段 p75 |
| TTFB | 全端 | ≤0.8s | ≤1.8s | 字段 |
| 包体 | 首屏 JS | ≤150KB | ≤300KB | 构建产物 |

```bash
# 本地用 Lighthouse CI 卡门禁（需全局装 lighthouse）
npx lighthouse https://shop.example.com/p/blue-shirt --preset=desktop --output=json \
  | node -e 'const r=JSON.parse(require("fs").readFileSync(0));console.log("LCP",r.audits["largest-contentful-paint"].displayValue)'
```

**原则**：字段数据（真实用户）优先于实验室数据（Lighthouse）。上线后用 RUM 看 p75，
Lighthouse 只用于本地回归。

## 5. 可访问性清单（合规 + 转化双收益）

- 所有图片有 `alt`；装饰图 `alt=""` 或 `aria-hidden`。
- 颜色对比 ≥ 4.5:1（正文）/ 3:1（大字与 UI 控件）。
- 价格/库存用文本而非仅靠颜色传达（色盲友好）。
- 标签页可达：焦点环可见，`Tab` 能走完加购与结账。
- 商品画廊支持键盘左右切换，不只有鼠标悬停。
- 表单错误用 `aria-invalid` + 文字说明，不只红框。

## 6. 典型坑与规避

1. **LCP 爆掉**：商品图未压缩/未用现代格式 → 用 WebP/AVIF，尺寸按需下发，
   `loading="lazy"` 仅用于首屏以下，`fetchpriority="high"` 给主图。
2. **变体组合爆炸**：n 个选项维度笛卡尔积后大量无库存组合暴露给用户 →
   仅渲染库存为正的组合，禁用非法组合。
3. **SEO 重复页**：`?ref=`/`?utm=` 生成同内容多 URL → 加 `canonical`，
   分页用 `rel=next/prev` 或无限滚动 + 正确索引。
4. **结账步骤过多**：3 步以上弃单率陡升 → 支持游客结账、地址自动补全、
   默认展开配送/支付同地址。
5. **移动端底部导航遮挡**：fixed 底栏盖住 CTA → 用 `env(safe-area-inset-bottom)`。
6. **Core Web Vitals 不监控**：上线后无字段数据 → 接 RUM（Web Vitals），
   以真实用户 p75 为准，而非仅看 Lighthouse。
7. **信任信号缺失**：无退货政策/安全支付标 → 详情页与结账页显式展示，
   降低决策摩擦。
8. **图片尺寸写死**：`<img width=1200>` 在小屏加载原图 → 用 `srcset` + `sizes`
   按视口下发，避免移动端拉满宽带。
9. **水合卡顿（Hydration）**：SSR 后整页 JS 水合阻塞交互 → 用 RSC/岛屿架构，
   把购物车按钮按岛屿拆分，首屏可交互时间提前。
10. **富媒体未审核**：JSON-LD 字段与页面实际不符（价不对/库存错）→
    被搜索引擎判为结构化的欺骗，降权。详情页渲染后跑一次 `validate_product_feed.py`
    同源校验逻辑，确保展示价 = 结构化数据价。

## 国际化与多语言（i18n）

- URL 用 `/{locale}/` 或 `?lang=`，配合 `hreflang` 标注互为翻译版本，避免 SEO 互相竞争。
- 价格/币种跟随 locale，但税务按收货国算（见 [references/cross-border-compliance.md](cross-border-compliance.md)），
  两者解耦：展示币种 ≠ 征税辖区。
- 文案长度差异：德文比英文长约 30%，UI 容器留弹性，别写死宽度导致换行截断。
- 数字/日期本地化：`Intl.NumberFormat` / `Intl.DateTimeFormat`，别手工拼格式。
- RTL（阿拉伯语等）用 `dir="rtl"` + CSS 逻辑属性（`margin-inline` 而非 `margin-left`）。

## 7. 上线前检查清单

- [ ] 组件按优先级实现：导航 → 列表 → 详情 → 购物车 → 结账
- [ ] 商品详情页含 Product JSON-LD + 面包屑 BreadcrumbList
- [ ] 变体选择禁用无库存/非法组合
- [ ] 主图 WebP/AVIF + 首屏 `fetchpriority="high"`，下方 `loading="lazy"`
- [ ] 移动端触控目标 ≥44px，底部安全区已处理
- [ ] 结账支持游客模式，步骤 ≤3
- [ ] 商品信息流已用 [scripts/validate_product_feed.py](../scripts/validate_product_feed.py) 校验 0 缺陷
- [ ] canonical / 分页语义已配置，无重复内容
- [ ] 字段数据 Core Web Vitals（LCP/INP/CLS）p75 达标
- [ ] 信任信号（退货/安全支付）在详情页与结账页可见
- [ ] 接后端（Shopify/Medusa/自定义）的数据层已隔离，便于换源

## 8. 与路由的衔接

- 商品数据接入 Shopify → [skills/shopify-manager](../skills/shopify-manager/SKILL.md)
- 支付/订阅结账 → [references/payment-integration-checklist.md](payment-integration-checklist.md)
- 跨境税务与货币 → [references/cross-border-compliance.md](cross-border-compliance.md)
- 完整组件模式 → [skills/storefront-builder](../skills/storefront-builder/SKILL.md)
