---
name: discount-hunter
description: Find discount/promo codes for the current checkout page from across the internet, then automatically test each code in the promo field until one works. Never clicks Pay — only tests codes. Use when the user is on a payment or cart page with a promo/discount code field.
metadata:
  display-name: Discount Hunter
  enabled: "true"
  version: "1.0"
---

# Discount Hunter

## When to Use

Activate when the user:
- Is on a checkout, cart, or payment page that has a **promo/discount/coupon code input field**
- Asks to "find a discount code", "try coupon codes", "find a promo code", or "get a discount"

**Do NOT activate if:**
- There is no visible promo/discount/coupon/voucher code field on the page
- The user is not on a checkout or cart page

---

## Overview

1. **Detect** whether the current page has a promo/discount code field.
2. **Identify** the merchant/store name from the page.
3. **Hunt** for codes across multiple coupon sites in parallel background tabs.
4. **Collect & deduplicate** all found codes.
5. **Test** each code one by one in the promo field — stop as soon as one works.
6. **Report** results. Never click any payment/checkout/submit/pay button.

---

## Phase 1 — Safety Check & Field Detection

1. Take a `take_snapshot` of the user's current page.
2. Scan the snapshot for any input field with labels, placeholders, or nearby text matching patterns like:
   - "promo code", "discount code", "coupon code", "voucher code", "gift code", "referral code", "promotional code", "have a code?", "enter code", "redemption code"
3. **If NO such field is found:**
   > "I couldn't find a promo/discount code field on this page. This skill only works on checkout or cart pages that have a code input. Please navigate to the payment/cart page first."
   Stop here.
4. **If a field IS found:** Note its element ID for later use. Also note the location of any **Apply / Redeem / Submit code** button — this is the ONLY button that will ever be clicked. Identify and note any **Pay / Place Order / Complete Purchase / Confirm** buttons — these must **never** be clicked.
5. Use `get_page_content` to identify the **store/merchant name** (from page title, logo alt text, or domain).
6. Report to user: _"Found a promo code field on **[Store Name]**. Searching for codes now..."_

---

## Phase 2 — Code Hunting (Parallel Background Tabs)

Open a **hidden window** with `create_hidden_window` for research. Then open parallel tabs with `new_hidden_page` to search these sources simultaneously:

### Search Targets

| Tab | URL Pattern |
|-----|-------------|
| 1 | `https://www.google.com/search?q=<store>+promo+code+<current_year>` |
| 2 | `https://www.google.com/search?q=<store>+coupon+code+working+<current_year>` |
| 3 | `https://www.retailmenot.com/view/<store-domain>` |
| 4 | `https://www.honey.com/coupons/<store-slug>` (or search `https://www.joinhoney.com/shop/<store>`) |
| 5 | `https://www.coupert.com/coupons/<store-slug>` |
| 6 | `https://www.coupons.com/coupon-codes/<store-slug>/` |
| 7 | `https://dealspotr.com/#_=&query=<store>` |
| 8 | `https://slickdeals.net/coupons/<store-slug>/` |
| 9 | Reddit: `https://www.google.com/search?q=site:reddit.com+<store>+promo+code` |
| 10 | `https://www.wikibuy.com/stores/<store-slug>` |

Replace `<store>` with the merchant name (URL-encoded), `<store-domain>` with the root domain (e.g. `nike.com`), and `<current_year>` with the current year.

### Extraction per tab

For each tab, after the page loads:
1. Use `get_page_content` to extract text.
2. Use `evaluate_script` or regex pattern matching to find strings that look like promo codes:
   - Uppercase alphanumeric strings (e.g. `SAVE20`, `WELCOME10`, `SUMMER2024`)
   - Patterns: `[A-Z0-9]{4,20}` — typically 4–20 characters, often containing numbers or dashes
   - Look near text like "code:", "use code", "coupon:", "promo:", "copy code", "get code"
3. Collect all found codes into a running list.
4. Close the tab with `close_page` when done.

### Deduplication & Ranking

After all tabs are processed:
1. Deduplicate the list (case-insensitive).
2. Prioritize codes that appeared on multiple sources (more likely to work).
3. Deprioritize obviously expired codes (those next to "expired" labels).
4. Cap the list at **20 codes** to keep testing time reasonable.
5. Close the hidden window with `close_window`.
6. Report: _"Found **N** unique promo codes. Testing them now..."_

---

## Phase 3 — Code Testing Loop

⚠️ **CRITICAL SAFETY RULES — must be followed throughout this phase:**
- ✅ ONLY interact with the **promo/discount code input field** and its **Apply/Redeem button**
- ❌ NEVER click any button labeled: Pay, Place Order, Complete Purchase, Confirm Order, Buy Now, Checkout, Submit Payment, or any equivalent
- ❌ NEVER fill in payment details (card number, CVV, billing address)
- ❌ NEVER click any button that would advance past the current checkout step
- If at any point the page changes unexpectedly (navigates away from checkout), stop immediately and alert the user

### Testing each code

For each code in the list:

1. Re-take `take_snapshot` to ensure the promo field element ID is still valid (page may have refreshed).
2. `clear` the promo code input field.
3. `fill` the promo code input with the current code.
4. Click the **Apply / Redeem** button (not any payment button).
5. Wait for page feedback — use `take_snapshot` or `get_page_content` to check for:
   - ✅ **Success signals**: "Code applied!", "Discount added", price reduction visible, green checkmark, "You saved X"
   - ❌ **Failure signals**: "Invalid code", "Code not found", "This code has expired", "Code does not apply", red error text
6. Report progress in chat after each attempt: _"Testing `SAVE20`... ❌ Invalid. Testing `WELCOME15`... ✅ Code applied! You saved $12.00"_

**Stop testing as soon as a code succeeds.**

If the apply action causes a page reload or navigation, re-verify you are still on the checkout page before continuing.

### Handle "apply" button edge cases

- Some sites apply the code automatically on input (no button needed) — watch for real-time feedback after `fill`.
- Some sites require pressing `Enter` — use `press_key` with `"Enter"` if no apply button is found.
- If the field clears itself after each failed attempt, simply re-fill and retry.

---

## Phase 4 — Report Results

### If a working code was found:

> ✅ **Discount code found: `WELCOME15`**
> This code has been applied to your cart. You saved **$12.00** (15% off).
> Your new total is visible on the page. You're ready to complete your purchase when you're ready.

Show a summary table of all codes tested:

```
| Code        | Source          | Result     |
|-------------|-----------------|------------|
| SAVE20      | RetailMeNot     | ❌ Expired  |
| SUMMER10    | Coupons.com     | ❌ Invalid  |
| WELCOME15   | Honey / Reddit  | ✅ Applied! |
```

### If NO working code was found:

> ❌ **No working codes found** after testing **N** codes.
> The following codes were tried: `CODE1`, `CODE2`, ...
> Unfortunately none applied a discount. You may want to check the store's official newsletter or social media for current promotions.

---

## Error Handling

- **Promo field disappears mid-loop**: Re-take snapshot, search for it again. It may be inside a collapsible section — try clicking "Have a promo code?" toggles.
- **Rate limiting / CAPTCHA on coupon sites**: Skip that source, continue with others.
- **Page navigates away accidentally**: Stop immediately, alert user: _"The page navigated away unexpectedly. Please go back to your checkout page and run the skill again."_
- **Store name not identifiable**: Ask the user: _"What store are you checking out on? I'll search for codes specific to them."_
- **Code field is greyed out or disabled**: Inform the user: _"The promo code field appears to be disabled on this page. It may require a minimum cart value or the field may only be available at a different checkout step."_

---

## Notes

- This skill **only tests codes** — it does not complete any purchase.
- All coupon site browsing happens in a hidden window, so the user's checkout tab is never disturbed.
- The skill works best on standard e-commerce checkout pages. It may not work on heavily dynamic single-page checkouts that re-render the DOM on every interaction.
- If the store uses a multi-step checkout and the promo field is on a specific step, make sure the user is on that step before activating.
