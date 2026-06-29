---
name: china-shopping-assistant
description: "China shopping flagship assistant. Input a product name or link; compare JD, Taobao, Tmall, PDD, Vipshop, SHEIN, and related shopping options by visible price, seller trust, review risk, promotion caveats, and after-sales fit. Safe boundary: no login, no order submission, no checkout, and no payment."
---

# China Shopping Assistant

Use this flagship skill when the user wants to buy, compare, or evaluate products across Chinese shopping platforms in any agent runtime that supports skills.

## User Promise

Input a product name or product link. Output where to buy, whether the visible price is worth it, seller/platform trust signals, review risks, promotion caveats, and buy/wait/switch-platform advice.

## Covered Platforms

- JD / 京东 / `jd-shopping` / `jingdong`
- Taobao / 淘宝 / `taobao-shopping`
- Tmall / 天猫 / `tianmao`
- PDD / 拼多多 / `pdd-shopping`
- Vipshop / 唯品会 / `vip`
- SHEIN / `shein-shopping`
- Broad discovery / `find-items` / `china-shopping` / `cn-online-shopping`

## Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit orders, click checkout, click final confirmation, or initiate payment.
- Treat visible prices as decision inputs, not guaranteed final payable prices.

## Example Prompts

1. `我想买一台 27 寸显示器，预算 1500，帮我比较京东、淘宝和拼多多。`
2. `这个淘宝链接值不值得买？帮我找京东和拼多多同款比较。`
3. `我想买空气炸锅，优先售后和正品，应该去哪个平台？`
4. `帮我看这件衣服在唯品会、天猫和淘宝哪个风险更低。`
5. `给我一个“买/等/换平台”的建议，并列出主要评论风险。`
