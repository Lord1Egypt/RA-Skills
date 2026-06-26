# E-commerce Product Images

## Resolution and Framing

- Minimum working baseline: **1000 × 1000 px**
- Better zoom-safe default: **2000 × 2000 px**
- Main catalog images often want **1:1**
- Small products and detail shots usually need more source resolution, not more sharpening

## Background and Edge Quality

- Main marketplace image often needs pure white or near-pure-white background.
- Product fill commonly should sit around **85-95%** of the frame for major marketplaces.
- Edges must be clean: no halos, dirty masks, or fringing.
- If shadows are allowed, keep them subtle and consistent across the catalog.
- Keep enough padding that the product does not feel cramped after marketplace cropping or thumbnail rounding.

## Color and Consistency

- Use sRGB for marketplace delivery.
- Do not auto-enhance product color without validating against the real item.
- Keep crop margins, lighting direction, and white balance consistent across the set.
- Catalog inconsistency makes the whole store feel lower quality even when each image is individually acceptable.
- Variant images should preserve a consistent camera angle and scale unless the marketplace expects a different shot type.
- If background removal is used, inspect edges around hair, glass, reflective metal, and fabric fringing at 100%.

## Marketplace Rules

| Platform | Typical baseline |
|----------|------------------|
| Amazon | White main image, square-safe, zoom-friendly |
| Shopify | Flexible background, but consistency matters |
| Etsy | Stronger lifestyle freedom, but thumbnails still need clarity |
| Walmart | White-background expectations are stricter |

- Marketplace uploaders normalize aggressively; validate the processed result after upload when it matters.
- Some catalogs require the main image to be cleaner and stricter than secondary lifestyle images; do not apply one styling rule to both.
- If a store theme renders product cards larger than the uploaded image can support, the fix is usually source dimensions and theme sizing together, not more sharpening alone.

## Product-Image Traps

- Product too small in frame
- Background not truly white where required
- Detail lost because the source was over-compressed
- Variant images cropped inconsistently
- Reflection, shadow, or mask style changing from product to product
- Text overlays or badges that are not allowed on main images
- Cutout edges that look fine zoomed out but fail at zoom or marketplace moderation
- Uploading already heavily compressed files and then letting the marketplace compress them again

## Quality Checklist

```
□ Product fills the frame appropriately
□ White-background requirement checked
□ Edge cleanup verified at 100%
□ Zoom/detail still holds up
□ Catalog crop and lighting look consistent
□ Metadata/privacy decision made
```
