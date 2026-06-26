# Schema Field Reference

## Required vs Recommended vs Optional

| Priority | Icon | Meaning |
|----------|------|---------|
| Required | 🔴 | Must be present for valid schema |
| Recommended | 🟡 | Significantly improves AI understanding |
| Optional | 🔵 | Nice to have, marginal impact |

---

## Organization Fields

### Required
- 🔴 `@type`: Must be "Organization"
- 🔴 `name`: Legal company name
- 🔴 `url`: Canonical website URL
- 🔴 `logo`: Logo image URL (minimum 112x112px)

### Recommended
- 🟡 `description`: 1-2 sentence factual description
- 🟡 `sameAs`: Array of social media URLs
- 🟡 `foundingDate`: ISO 8601 date (YYYY-MM-DD)
- 🟡 `contactPoint`: Customer service contact info
- 🟡 `address`: Headquarters location

### Optional
- 🔵 `legalName`: Full legal name (if different from name)
- 🔵 `alternateName`: DBA or brand name variations
- 🔵 `founders`: Array of Person objects
- 🔵 `employees`: Employee count (QuantitativeValue)
- 🔵 `parentOrganization`: Parent company
- 🔵 `subOrganization`: Subsidiaries
- 🔵 `knowsAbout`: Topics/areas of expertise

### Example with All Fields
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Stripe",
  "legalName": "Stripe, Inc.",
  "alternateName": "Stripe Payments",
  "url": "https://stripe.com",
  "logo": "https://stripe.com/img/logo.png",
  "description": "Financial infrastructure platform for internet businesses",
  "foundingDate": "2010-09-01",
  "founders": [
    {
      "@type": "Person",
      "name": "Patrick Collison"
    },
    {
      "@type": "Person",
      "name": "John Collison"
    }
  ],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "510 Townsend St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94103",
    "addressCountry": "US"
  },
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "contactType": "sales",
      "telephone": "+1-888-963-8442",
      "availableLanguage": ["English"]
    },
    {
      "@type": "ContactPoint",
      "contactType": "technical support",
      "telephone": "+1-888-963-8442",
      "availableLanguage": ["English", "French", "German"]
    }
  ],
  "sameAs": [
    "https://twitter.com/stripe",
    "https://www.linkedin.com/company/stripe",
    "https://github.com/stripe",
    "https://en.wikipedia.org/wiki/Stripe_(company)"
  ],
  "knowsAbout": ["Payments", "SaaS", "APIs", "Financial Technology"]
}
```

---

## Article Fields

### Required
- 🔴 `@type`: "Article" or "BlogPosting"
- 🔴 `headline`: Article title (max 110 chars)
- 🔴 `author`: Person or Organization
- 🔴 `datePublished`: ISO 8601 datetime

### Recommended
- 🟡 `description`: 150-character summary
- 🟡 `image`: Featured image (min 1200x800)
- 🟡 `publisher`: Organization (usually same as site owner)
- 🟡 `dateModified`: Last update datetime
- 🟡 `articleSection`: Category/section name
- 🟡 `wordCount`: Article length
- 🟡 `keywords`: Array of topic tags

### Optional
- 🔵 `articleBody`: Full article text
- 🔵 `backstory`: Background context
- 🔵 `speakable`: Sections for text-to-speech

---

## FAQPage Fields

### Required
- 🔴 `@type`: "FAQPage"
- 🔴 `mainEntity`: Array of Question objects

### Question Object Fields

#### Required
- 🔴 `@type`: "Question"
- 🔴 `name`: Question text (exactly as shown on page)
- 🔴 `acceptedAnswer`: Answer object

### Answer Object Fields

#### Required
- 🔴 `@type`: "Answer"
- 🔴 `text`: Full answer text

#### Recommended
- 🟡 `upvoteCount`: Number of upvotes (if applicable)

### Best Practices

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do I reset my password?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>To reset your password:</p><ol><li>Go to the login page</li><li>Click 'Forgot Password'</li><li>Enter your email</li><li>Check your inbox for reset link</li></ol><p>The link expires in 24 hours.</p>"
      }
    }
  ]
}
```

**Notes**:
- Answer text can contain HTML
- Match question exactly to page text
- Include full answer, not just summary
- 3-10 questions per page optimal

---

## Product Fields

### Required
- 🔴 `@type`: "Product"
- 🔴 `name`: Product name
- 🔴 `offers`: Offer or AggregateOffer

### Offer Fields (Required)
- 🔴 `@type`: "Offer"
- 🔴 `price`: Numeric price
- 🔴 `priceCurrency`: ISO 4217 code (USD, EUR, etc.)

### Recommended
- 🟡 `description`: Product description
- 🟡 `brand`: Brand reference
- 🟡 `image`: Product images (array)
- 🟡 `sku`: Stock keeping unit
- 🟡 `mpn`: Manufacturer part number
- 🟡 `gtin8/12/13/14`: Global Trade Item Number
- 🟡 `aggregateRating`: Overall rating
- 🟡 `review`: Individual reviews
- 🟡 `offers.availability`: InStock, OutOfStock, etc.
- 🟡 `offers.priceValidUntil`: Sale end date
- 🟡 `offers.url`: Product page URL

### Optional
- 🔵 `color`: Product color
- 🔵 `material`: Material composition
- 🔵 `weight`: Product weight
- 🔵 `depth`, `width`, `height`: Dimensions

### Complete Example
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Acme Noise-Canceling Headphones",
  "image": [
    "https://acme.com/images/headphones-1x1.jpg",
    "https://acme.com/images/headphones-4x3.jpg",
    "https://acme.com/images/headphones-16x9.jpg"
  ],
  "description": "Premium wireless headphones with 30-hour battery and active noise cancellation",
  "sku": "ACH-3000-BLK",
  "mpn": "925872",
  "brand": {
    "@type": "Brand",
    "name": "Acme Audio"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.4",
    "reviewCount": "89"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://acme.com/headphones",
    "price": "299.99",
    "priceCurrency": "USD",
    "priceValidUntil": "2024-12-31",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Acme Electronics"
    }
  }
}
```

---

## HowTo Fields

### Required
- 🔴 `@type`: "HowTo"
- 🔴 `name`: Guide title
- 🔴 `step`: Array of HowToStep objects

### HowToStep Fields

#### Required
- 🔴 `@type`: "HowToStep"
- 🔴 `name`: Step title
- 🔴 `text`: Step instructions

#### Recommended
- 🟡 `url`: Direct link to step anchor
- 🟡 `image`: Step image
- 🟡 `video`: Step video clip

### HowTo Fields (Recommended)
- 🟡 `description`: Overall guide description
- 🟡 `totalTime`: Duration (PT30M format)
- 🟡 `estimatedCost`: Approximate cost
- 🟡 `tool`: Required tools (array)
- 🟡 `supply`: Required materials (array)
- 🟡 `image`: Guide images
- 🟡 `video`: Guide video

### Example
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Bake Sourdough Bread",
  "description": "A beginner's guide to baking artisan sourdough at home",
  "totalTime": "PT24H",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "5"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "Bread flour"
    },
    {
      "@type": "HowToSupply",
      "name": "Water"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Dutch oven"
    },
    {
      "@type": "HowToTool",
      "name": "Kitchen scale"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Mix the dough",
      "text": "Combine 500g flour and 350g water. Mix until no dry flour remains.",
      "url": "https://example.com/sourdough#step1"
    },
    {
      "@type": "HowToStep",
      "name": "Fold the dough",
      "text": "Perform stretch and folds every 30 minutes for 2 hours.",
      "url": "https://example.com/sourdough#step2"
    }
  ]
}
```

---

## Common Data Types

### Date/Time Formats (ISO 8601)

| Type | Format | Example |
|------|--------|---------|
| Date | YYYY-MM-DD | 2024-01-15 |
| DateTime | YYYY-MM-DDTHH:MM:SS | 2024-01-15T09:30:00 |
| DateTime with TZ | YYYY-MM-DDTHH:MM:SS±HH:MM | 2024-01-15T09:30:00-08:00 |
| Duration | P[n]Y[n]M[n]DT[n]H[n]M[n]S | PT30M (30 minutes) |

### URL Requirements
- Must be absolute (https://...)
- Must be accessible
- Should use canonical URLs
- Images: minimum sizes apply

### Text Guidelines
- No HTML in `name` fields
- HTML allowed in `description` and `text` fields
- Keep `headline` under 110 characters
- Keep `description` around 150 characters
- Use factual, non-promotional language

### Numeric Formats
- `price`: No currency symbol, just number (e.g., "29.99")
- `ratingValue`: Typically 1-5 scale
- `reviewCount`: Integer, no commas
- `position` (breadcrumbs): 1-indexed integer