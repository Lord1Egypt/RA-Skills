---
name: 24h-product-marketing
description: read one public product page from 24h.chichbong.com and turn it into a compact zalo-shop-ready product block. use when the user provides a single 24h.chichbong.com/product/... link and wants a short professional vietnamese summary under 500 characters, a safer rewritten title, a marked-up price increased by 30 to 50 percent, and the main product thumb. always prioritize direct page reading, use search as fallback, keep outputs factual, avoid sensitive ad terms, and write in a close but professional tone suitable for product listing content rather than social post copy.
---

# 24h Product Marketing

Read exactly one public product URL from `24h.chichbong.com` and produce one compact, sales-ready product block for listing use.

## Core workflow

Follow these steps in order for every request.

1. Confirm the input is a single URL on `https://24h.chichbong.com/product/...`.
2. Open the product page directly.
3. If the direct open fails, try recovery in this order:
   - search the exact URL
   - search the product code on `24h.chichbong.com`
   - open the most relevant result from the same domain
4. Extract only facts that are visible on the product page or search result snippet:
   - original product title
   - visible sale price or listed price
   - main product thumb image
   - short intro and major content blocks such as giới thiệu, công dụng, thành phần, cách dùng, lưu ý, bảo quản, quy cách, đối tượng phù hợp
5. Build the output using the exact output template below.
6. If any field cannot be verified, say so plainly. Never invent product facts.

Treat each request as independent. Never reuse product data from a previous URL.

## Extraction rules

Prioritize these sources for the thumb image:
1. main product image shown on the page
2. og:image or other page meta image if clearly tied to the product
3. image URL visible in search result snippets from the same product page

For product facts:
- keep only sellable, practical facts
- compress long descriptions into a short understanding of what the product is, what is notable, and why it is attractive
- ignore site chrome, menus, tabs, policy banners, unrelated recommendations, comment sections, and decorative text
- do not copy long paragraphs verbatim

## Writing rules for the short product intro

Write for a Zalo Shop product description, not for a social post.

Required style:
- vietnamese
- under 500 characters
- close, easy to read, slightly warm
- professional enough for product listing content
- may address the reader as `chị` when natural, but do not overdo it
- focus on standout advantages and practical reasons to buy
- sound polished, tidy, and trustworthy

Do not write like:
- hype-heavy post copy
- spammy sales talk
- exaggerated miracle promises
- chatty comment-style language
- emoji-heavy content

Preferred language patterns:
- gọn gàng
- tiện dùng
- dễ mang theo
- cảm giác dễ chịu
- hợp dùng hằng ngày
- phù hợp để để sẵn trong túi, bàn làm việc, góc chăm sóc cá nhân
- lựa chọn đáng cân nhắc cho chị đang tìm một món ...

## Safety filter

Avoid or replace risky wording, especially:
- medical, pharmaceutical, or treatment claims
- disease or diagnosis language
- detox, weight-loss, slimming, fat-burning language
- absolute safety claims
- exaggerated superlatives and guaranteed outcomes
- sensitive demographic or discriminatory language
- ad-sensitive words such as: hóa chất, kháng khuẩn, diệt, trị, dưỡng, trắng, giảm rụng, an toàn, detox, giảm cân, óc chó, hồ chí minh

When the original title or page contains risky terms:
- keep the real product identity
- rewrite into a softer ecommerce-safe form
- prefer neutral benefit language over strong claims

Examples:
- `trị mụn` -> `hỗ trợ chăm da mụn` or `phù hợp cho da dễ lên mụn`
- `trắng da` -> `giúp da nhìn tươi sáng hơn`
- `giảm rụng tóc` -> `giúp tóc trông gọn và dễ chăm hơn`
- `kháng khuẩn` -> `giữ cảm giác sạch sẽ, dễ chịu`

## Pricing rule

Take the visible website price as the base price.

Then create one suggested selling price by increasing the base price by 30% to 50%.
- choose a clean, natural retail number
- prefer rounded pricing that still looks believable
- preserve the currency format used in vietnamese ecommerce

If the original price cannot be verified, say `không xác minh được giá gốc` and do not fabricate a new price.

## Title rewrite rule

Rewrite the title to be more attractive, but keep it:
- factually faithful to the product type
- shorter or cleaner than the original when possible
- suitable for Zalo Shop listing
- free of prohibited or high-risk claims

A good rewritten title usually includes:
- product type
- brand or line if clearly shown
- 1 practical attractive angle such as tiện dùng, gọn gàng, dịu nhẹ, dễ mang theo, hương dễ chịu, bản tiện lợi

## Output template

Always return exactly these 4 sections in this order:

1. Giới thiệu ngắn:
[one paragraph under 500 characters]

2. Giá đề xuất:
[giá gốc] -> [giá mới]

3. Tiêu đề gợi ý:
[rewritten title]

4. Ảnh thumb:
[direct image URL or `không lấy được ảnh thumb`]

## Failure handling

If the page cannot be opened and no trustworthy same-domain fallback is found, return this format:

URL đã kiểm tra:
[url]

Lỗi gặp phải:
[không thể mở trực tiếp hoặc không tìm thấy nguồn cùng domain đủ tin cậy]

Phần không thể xác minh:
- tiêu đề sản phẩm
- giá gốc
- mô tả chi tiết
- ảnh thumb gốc

Do not guess missing fields.
