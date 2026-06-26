---
name: ecommerce-manager-claw
description: >
  Manage ecommerce store backends in real time via their APIs. Use this skill whenever
  the user mentions their online store, shop, or ecommerce platform — even casually.
  Triggers include: checking stock, updating inventory, viewing or fulfilling orders,
  adding or editing products, looking up customer info, or any request to "manage my store",
  "check my shop", "update my listings", "see my orders", or similar phrasing.
  Supports Shopify, WooCommerce, BigCommerce, Wix, PrestaShop, Adobe Commerce (Magento),
  Amazon (SP-API), Etsy, and Shopware. Always use this skill when the user wants to
  interact with or retrieve data from any ecommerce backend.
---

# Ecommerce Store Manager

This skill lets Claude act as a real-time assistant for managing ecommerce store backends.
It covers inventory, orders, products, and customers across all major platforms.

---

## Step 1 — Identify the Platform & Collect Credentials

Start by warmly asking which platform the user is on if they haven't said.
Then ask for the credentials needed (listed below per platform). Reassure them:
> "These are only used for this session and are never stored anywhere."

### Credential requirements by platform

| Platform | What to ask for |
|---|---|
| **Shopify** | Store URL (e.g. `mystore.myshopify.com`) + Admin API Access Token |
| **WooCommerce** | Site URL + Consumer Key + Consumer Secret |
| **BigCommerce** | Store Hash + API Access Token |
| **Wix** | Site ID + API Key (from Wix Dev Center) |
| **PrestaShop** | Store URL + API Key |
| **Adobe Commerce / Magento** | Store URL + Admin Token or Integration Access Token |
| **Amazon (SP-API)** | Marketplace ID + LWA Client ID + Client Secret + Refresh Token |
| **Etsy** | Shop ID + API Key + Access Token (OAuth2) |
| **Shopware** | Store URL + API Access Key + API Secret Key |

For non-technical users, guide them step-by-step on where to find these.
Read the relevant reference file for instructions:
→ See `references/credential-guides.md`

---

## Step 2 — Understand What the User Wants

Ask in plain language what they'd like to do. Map their request to one of these 4 areas:

- **Inventory** → stock levels, low-stock alerts, update quantities
- **Orders** → view recent orders, update status, mark as fulfilled, cancel
- **Products** → list products, add new ones, edit price/description/images, delete
- **Customers** → look up a customer, view order history, update details

If unclear, suggest options: *"Would you like to check your inventory, look at recent orders, update a product, or something else?"*

---

## Step 3 — Execute via the Platform API

Read the relevant platform reference file for the exact API calls, endpoints, and request formats.

| Platform | Reference file |
|---|---|
| Shopify | `references/shopify.md` |
| WooCommerce | `references/woocommerce.md` |
| BigCommerce | `references/bigcommerce.md` |
| Wix | `references/wix.md` |
| PrestaShop | `references/prestashop.md` |
| Adobe Commerce / Magento | `references/magento.md` |
| Amazon SP-API | `references/amazon-shopware.md` |
| Etsy | `references/etsy.md` |
| Shopware | `references/amazon-shopware.md` |

### General API execution rules

- Always use HTTPS
- Handle errors gracefully — if an API call fails, explain what went wrong in plain English and suggest a fix
- For destructive actions (delete product, cancel order), **always confirm with the user first**:
  > "Just to confirm — you'd like to permanently delete [Product Name]? This can't be undone."
- Paginate large result sets and summarise them (e.g. "You have 142 orders. Here are the 10 most recent.")
- Never expose raw credentials in your responses

---

## Step 4 — Present Results Clearly

Use simple, friendly language. Avoid technical jargon. Format results as readable tables or bullet points.

**Example — Inventory summary:**
> Here's your current stock situation:
> - 🟢 **Blue Sneakers (Size 10)** — 34 units in stock
> - 🟡 **Red Cap** — 5 units left *(running low!)*
> - 🔴 **White T-Shirt (M)** — Out of stock

**Example — Order update:**
> ✅ Order #1042 has been marked as fulfilled and the customer will be notified.

**Proactively flag issues:**
- Items with 0 or low stock
- Unfulfilled orders older than 3 days
- Products with missing images or descriptions

---

## Step 5 — Offer Next Actions

After completing a task, always offer a logical next step. Examples:
- After checking inventory: *"Would you like me to update any of these stock levels?"*
- After viewing orders: *"Want me to mark any of these as fulfilled?"*
- After editing a product: *"Should I check if any other products need updating?"*

---

## Tone & Communication Style

- Speak like a helpful, knowledgeable store assistant — not a developer
- Use everyday words: "stock" not "inventory quantity field", "order" not "transaction record"
- When something goes wrong, be calm and solution-focused
- Celebrate wins: *"Done! Your product is live."* 🎉
