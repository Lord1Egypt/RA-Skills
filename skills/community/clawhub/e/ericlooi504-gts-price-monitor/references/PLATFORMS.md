# Platform-Specific Notes

This reference covers e-commerce platform quirks and anti-scrape measures.
Read this when scanning fails or returns unexpected results.

## Shopee

| Aspect | Detail |
|--------|--------|
| Regions | .com.my (Malaysia), .sg (Singapore), .co.th (Thailand), .com.ph (Philippines), .id (Indonesia), .tw (Taiwan) |
| Dynamic loading | Prices load via JavaScript. Wait for `.product-price`, `[data-testid="product-price"]`, or `div.flex.items-center > div` |
| Price selectors | Try: `.product-price__price`, `.tw-text-primary`, `[class*="product-price"]` |
| Stock status | Check for "sold out" / "已售罄" / "Habis Terjual" indicators |
| Currency | Always matches the TLD region (RM for .my, SGD for .sg, etc.) |
| Rating | Often displayed next to "⭐" stars — useful for competitive intel |
| Notes | Shopee may show logged-in prices vs public prices. Use the public URL. Rate limiting: ~5 req/min on aggressive polling. |

### Shopee Selectors (last resort)
If standard selectors fail, look for these patterns in page source:
- `"price"` in JSON-LD embedded scripts
- `window.__INITIAL_STATE__` data
- Meta tags: `og:price:amount`

## Lazada

| Aspect | Detail |
|--------|--------|
| Regions | .com.my (Malaysia), .sg (Singapore), .co.th (Thailand), .com.ph (Philippines), .id (Indonesia), .vn (Vietnam) |
| Price selectors | `.pdp-product-price__wrapper .pdp-price`, `[data-spm="price"]`, `.pdp-price` |
| Discount price | Lazada often shows "was RM X, now RM Y". Log both values. |
| Seller info | Found in `.seller-name__detail` or `[data-spm="seller"]` |
| Stock | Look for "sold out" overlay or .out-of-stock class |
| Region blocking | May block non-local IPs. If scan fails, try adding `?spm=a2o4k.home` to URL. |
| Notes | Lazada runs A/B price tests for logged-in users. Public prices on incognito are the "base price." |

### Lazada Fallback
If scrape fails:
1. Remove URL query parameters (everything after `?`)
2. Try the mobile version: replace `www.lazada` with `m.lazada`
3. Check `script[type="application/ld+json"]` for structured data

## Amazon

| Aspect | Detail |
|--------|--------|
| Regions | .com (US), .co.uk (UK), .de (Germany), .jp (Japan), .com.au (Australia), .ca (Canada), .in (India) |
| Main price | `#corePriceDisplay_desktop_feature_div .a-price-whole` |
| Fraction | `.a-price-fraction` — combine with whole for the full price |
| Currency | Set by region ($, £, €, ¥, A$, C$, ₹) |
| Deal price | `.a-price.a-text-price` — shows the strikethrough original price |
| Coupon | Check for `.promoPriceBlock` or "Save extra" banners. Deduct coupon from current price. |
| Stock | "In Stock" text in `#availability` span |
| Seller | "Sold by" in `#merchantInfo` |
| Notes | Aggressive anti-bot. Use `openclaw browser` with realistic User-Agent. Max 1 req / 3 sec. |
| BSR (Best Sellers Rank) | In `#detailBullets_feature_div` — useful for competitor analysis |

### Amazon Fallback
If standard page fails:
1. Try `amazon.com/dp/<ASIN>` (product ID from URL)
2. Check for captcha — if hit, wait 60s before retry
3. Use Amazon Product Advertising API as alternative (requires API key)

## General Tips

### Price Extraction Order of Priority
1. Structured data (JSON-LD in `<script type="application/ld+json">`)
2. Meta tags (`og:price:amount`, `product:price:amount`)
3. Visible DOM elements (specific selectors per platform)
4. Text pattern matching (regex for "RM 123.45")

### Validation Rules
- Price must be > 0 and < 10x the expected price
- If price changed > 50% from last scan, flag for manual review
- Always log the raw text alongside parsed value

### Rate Limiting
- Default: 1 request per 5 seconds
- Shopee/Lazada: max 5 req/min
- Amazon: max 20 req/min
- If getting blocked, add random delay of 3-8 seconds between requests

### Currency Mapping
| Code | Symbol | Platforms |
|------|--------|-----------|
| MYR | RM | Shopee MY, Lazada MY |
| SGD | S$ | Shopee SG, Lazada SG |
| THB | ฿ | Shopee TH, Lazada TH |
| IDR | Rp | Shopee ID, Lazada ID |
| PHP | ₱ | Shopee PH, Lazada PH |
| USD | $ | Amazon US |
| GBP | £ | Amazon UK |
| EUR | € | Amazon DE, FR, IT, ES |
| JPY | ¥ | Amazon JP |
| AUD | A$ | Amazon AU |
