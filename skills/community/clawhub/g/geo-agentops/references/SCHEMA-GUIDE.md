# Schema标记指南

## 什么是Schema标记

Schema标记是一种结构化数据格式，帮助搜索引擎和AI理解网页内容。

## GEO核心Schema类型

### 1. Product Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "产品名称",
  "description": "产品描述",
  "brand": {
    "@type": "Brand",
    "name": "品牌名称"
  },
  "offers": {
    "@type": "Offer",
    "price": "99.00",
    "priceCurrency": "CNY",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "120"
  }
}
```

### 2. FAQPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "问题1",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "答案1"
      }
    },
    {
      "@type": "Question",
      "name": "问题2",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "答案2"
      }
    }
  ]
}
```

### 3. Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "author": {
    "@type": "Person",
    "name": "作者名称"
  },
  "datePublished": "2026-04-12",
  "dateModified": "2026-04-12",
  "articleBody": "文章正文",
  "wordCount": 1500
}
```

### 4. Organization Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "公司名称",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "support@example.com"
  }
}
```

---

## 部署方式

### HTML嵌入

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  ...
}
</script>
```

### 验证工具

- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)

---

## GEO最佳实践

1. **每个页面至少一个Schema**
2. **FAQPage提升AI引用率**
3. **数据必须与页面内容一致**
4. **定期更新Schema数据**
