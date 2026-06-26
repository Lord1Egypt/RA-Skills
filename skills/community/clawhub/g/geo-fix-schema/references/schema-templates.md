# Schema.org JSON-LD Templates for AI Visibility

Reference templates for common schema types. All templates follow schema.org spec and are optimized for AI engine discoverability.

## Core Identity

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "TODO: Company Name",
  "url": "TODO: https://example.com",
  "logo": "TODO: https://example.com/logo.png",
  "description": "TODO: One-sentence company description",
  "foundingDate": "TODO: 2020",
  "sameAs": [
    "TODO: https://linkedin.com/company/example",
    "TODO: https://twitter.com/example",
    "TODO: https://github.com/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "url": "TODO: https://example.com/contact"
  }
}
```

**AI impact**: Primary entity signal. AI uses this to match your brand against knowledge graph entries and verify cross-source consistency.

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "TODO: Business Name",
  "url": "TODO: https://example.com",
  "logo": "TODO: https://example.com/logo.png",
  "description": "TODO: Business description",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "TODO: 123 Main St",
    "addressLocality": "TODO: City",
    "addressRegion": "TODO: State",
    "postalCode": "TODO: 12345",
    "addressCountry": "TODO: US"
  },
  "telephone": "TODO: +1-555-000-0000",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "TODO: 40.7128",
    "longitude": "TODO: -74.0060"
  },
  "sameAs": []
}
```

**AI impact**: Critical for local search in AI. NAP (Name/Address/Phone) consistency across structured data and third-party listings is a top trust signal.

### WebSite + SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "TODO: Site Name",
  "url": "TODO: https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "TODO: https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

**AI impact**: Enables sitelinks search box. Only include SearchAction if the site has a working search function.

---

## Content Schema

### Article / BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "TODO: Article Title",
  "author": {
    "@type": "Person",
    "name": "TODO: Author Name",
    "url": "TODO: https://example.com/team/author"
  },
  "datePublished": "TODO: 2026-01-15T08:00:00+00:00",
  "dateModified": "TODO: 2026-03-01T10:30:00+00:00",
  "description": "TODO: Article summary",
  "image": "TODO: https://example.com/images/article.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "TODO: Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "TODO: https://example.com/logo.png"
    }
  },
  "mainEntityOfPage": "TODO: https://example.com/blog/article-slug",
  "wordCount": 1500,
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".article-summary", ".article-body p:first-of-type"]
  }
}
```

**AI impact**: `dateModified` signals freshness (AI has strong recency bias). `speakable` marks which passages AI should quote directly. `wordCount` helps AI judge content depth.

### Person (Author)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "TODO: Full Name",
  "url": "TODO: https://example.com/team/name",
  "jobTitle": "TODO: Senior Engineer",
  "worksFor": {
    "@type": "Organization",
    "name": "TODO: Company Name"
  },
  "sameAs": [
    "TODO: https://linkedin.com/in/name",
    "TODO: https://twitter.com/name"
  ]
}
```

**AI impact**: Strengthens E-E-A-T signals. AI cross-references author entities with LinkedIn, publications, and other sources to assess expertise.

---

## AI-Boost Schema

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "TODO: What is your product?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "TODO: Clear, self-contained answer in 2-3 sentences."
      }
    },
    {
      "@type": "Question",
      "name": "TODO: How much does it cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "TODO: Direct answer with specific pricing details."
      }
    }
  ]
}
```

**AI impact**: Highest-value AI-boost schema. Q&A pairs map directly to how users query AI engines. Self-contained answers are ideal citation candidates.

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "TODO: How to Set Up Your Account",
  "description": "TODO: Step-by-step guide description",
  "step": [
    {
      "@type": "HowToStep",
      "name": "TODO: Create an account",
      "text": "TODO: Visit example.com/signup and fill in your details."
    },
    {
      "@type": "HowToStep",
      "name": "TODO: Configure settings",
      "text": "TODO: Navigate to Settings > General and set your preferences."
    }
  ]
}
```

**AI impact**: Tutorial/documentation patterns are heavily cited by AI. HowTo schema makes step sequences machine-readable.

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "TODO: https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "TODO: Section",
      "item": "TODO: https://example.com/section"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "TODO: Page Title",
      "item": "TODO: https://example.com/section/page"
    }
  ]
}
```

**AI impact**: Provides hierarchical context. AI uses breadcrumb structure to understand content taxonomy and site architecture.

### Product (E-commerce)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "TODO: Product Name",
  "description": "TODO: Product description",
  "image": "TODO: https://example.com/product.jpg",
  "brand": {
    "@type": "Brand",
    "name": "TODO: Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "price": "TODO: 49.99",
    "priceCurrency": "TODO: USD",
    "availability": "https://schema.org/InStock",
    "url": "TODO: https://example.com/products/item"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "TODO: 4.5",
    "reviewCount": "TODO: 120"
  }
}
```

**AI impact**: Product schema directly feeds shopping AI and comparison queries. Price + availability + ratings are the top data points AI extracts for purchase recommendations.

---

## Format Rules

1. **Always use JSON-LD** — preferred by Google, most reliable for AI parsing
2. **One `<script type="application/ld+json">` per schema type** — avoid nesting multiple types in one block
3. **Use absolute URLs** — never relative paths
4. **ISO 8601 dates** — `2026-01-15T08:00:00+00:00` format
5. **Validate before deploying** — use https://validator.schema.org/
