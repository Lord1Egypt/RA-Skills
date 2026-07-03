# Crisp API Map

This reference is sanitized. It intentionally contains no user token, email, address, order id, invoice URL, or personal order content.

## Base

- API base: `https://crispapp.nl/v1`
- Auth header: `Authorization: bearer <token>`
- Typical mobile user agent: `crisp/app/android/<version>`
- Image URL format: `https://crispapp.nl/blob/<blob_id>?thumb=<size>`

Keep `CRISP_USER_AGENT` configurable and validate it with `/client`.

## Authentication

- `POST /user/login`
  - Start login: `{ "email": "...", "country": "nl" }`
  - Confirm login: `{ "email": "...", "code": "...", "country": "nl" }`
  - Use the same bearer token for both requests.

## Health And Client State

- `GET /countryDetect`
  - Public-ish country detection.
- `GET /client`
  - Confirms authenticated client state.
  - Check for `outdated.type == "block"` before relying on the API.

## Home And Merchandising

- `GET /home`
  - Returns top-level `{ background, data }`.
  - `data` is a list of typed app blocks.
  - Observed block types:
    - `top_bar`
    - `featured_category`
    - `horizontal_scroller`
    - `recipe_scroller_entrypoint`
    - `previously_bought`
    - `block_title`
    - `weekbox_entry`
    - `category_item`
  - Observed merchandising names/titles:
    - `homeThisWeekPromoOnly` / `Nu in de promo`
    - `seasonTips` / `In 't seizoen & nieuw`
    - `thematicCarousel`
    - `Jouw winkel`
    - `Recepten`

## Promotions

- `GET /promo/current`
  - Current promotions page.
  - Promos are commonly in `promo.blocks[]`.
  - Product blocks have `type == "product"` and nested `product`.
  - Useful fields:
    - `product.id`
    - `product.title`
    - `product.price`
    - `product.basePrice`
    - `product.promotion.descr`
    - `product.promotion.percent`
    - `product.promotion.discount`
    - `product.promotion.fixedPrice`
    - `product.promotion.title`
    - `product.tags`
    - `product.allergens`
    - `product.categories`
  - Observed promo section headers include:
    - `Sterrenpromo`
    - `Recepten`
    - `Groente en fruit`
    - `Vers bereid`
    - `Vlees, vis en vega`
    - `Kaas en delicatessen`
    - `Zuivel`
    - `Bakkerij`
    - `Beleg en ontbijtgranen`
    - `Dranken`
    - `Internationaal`
    - `Koek, snoep, snacks en ijs`
    - `Baby, kind`
    - `Huishouden en verzorging`
    - `Stapelpromo`
- `GET /promo/:id`
- `GET /promo/content/:id`

## Personalization

- `GET /yourShop`
  - Main personalized shop surface.
  - Useful fields:
    - `items`
    - `categories`
    - `hasSavedItems`
    - `hasGroups`
  - Observed moment/category structure:
    - `Ontbijt, lunch`
    - `Avondeten`
    - `Snacks, borrel`
    - `Voorraadkast`
    - `Eerder gekocht en bewaard`
    - `Nog op je lijstje`
    - product-category rows such as avocado, bananas, smoked fish, mushrooms, Asian kitchen, Italian kitchen, etc.
- `GET /saved`
  - Saved ids for products, recipes, and user recipes.
- `GET /saved/list`
  - Saved carousel/list view.

## Basket And Delivery

- `GET /basket/main`
  - Current basket, minimum order value, delivery days and slots, service fees, products, recipes, and edit state.
  - Useful fields:
    - `products`
    - `recipes`
    - `deliveryDays[].slots[]`
    - `deliverySlot`
    - `baseDeliverySlot`
    - `mov`
    - `movText`
    - `neededForMOV`
    - `productsTotalPrice`
    - `totalPrice`
    - `finalPrice`
    - `payPrice`
    - `servicePrice`
    - `serviceLabel`
    - `serviceFaqContent`
    - `smallValuePrice`
  - Delivery slot fields:
    - `id`
    - `date`
    - `start`
    - `end`
    - `cutoff`
    - `editCutoff`
    - `type`
    - `note`
    - `price`
    - `basePrice`
    - `servicePrice`
    - `availableKey`
  - Observed minimum order value: `mov` is commonly `40.00`, but always read live data.
  - Observed service-fee text can include thresholds such as under/over EUR 50; always read live `serviceFaqContent`.
- `PUT /basket/main`
  - Mutating endpoint. Use only after explicit user confirmation.
  - Product diff shape:
    - `{ "products": { "<productId>": { "count": <quantity>, "from": { ... } } } }`
  - Recommended `from` context for repeated purchases:
    - `{ "screenName": "YourShop", "screenUrl": "/yourShop", "scroller": "Eerder gekocht en bewaard" }`

## Orders

- `GET /order/history`
  - Past orders, product/recipe history, delivery slots, payment status, address, invoices, and feedback state.
  - Highly sensitive. Summarize rather than dumping raw payloads.
  - Never print addresses, invoice URLs, payment identifiers, or delivery notes by default.
- `GET /order/:id`
  - Sensitive order detail.
- Order confirm/cancel/payment endpoints exist but are outside the default skill scope.

## Recipes

- `GET /recipe/:id`
  - Recipe detail including recipe images, ingredient groups, ingredients, nested product objects, pricing, tags, allergens, portions, instructions, and share URL.
- `GET /recipeGroups`
- `GET /recipeGroup/:id`
- `GET /recipe/favorites`
- `GET /recipe/recents`

## Search

- `GET /search`
- `GET /search/suggestions`
- `GET /search/trendingSuggestions`
- `GET /search/recipe`
- `GET /search/recipe/trendingSuggestions`

Prefer read-only search endpoints for finding products or candidate recipes.
