# AnswerBox agent API

Base URL is the `origin` in the session file. Send `Content-Type: application/json` and encode the body as UTF-8. A GBK body is still read correctly. Authenticated calls send `Authorization: Bearer {accessToken}`.

Recommend works with no account. Orders require a bearer token from verify or refresh.

## POST /api/agent/recommend

No account required. A bearer token, when you have one, attaches the conversation to that person.

```json
{
  "query": "最近睡不着",
  "history": [],
  "need": "",
  "locale": "zh-CN",
  "region": "CN",
  "conversationId": null,
  "visitorKey": "uuid"
}
```

`locale` is `zh-CN` or `en-US`. `region` is `CN` or `OVERSEAS`. `history` is earlier user lines only, and only when this message continues the same shelf.

`query` is the user's words, unchanged. Do not send a paraphrase. A new recommendation sends `history` as `[]` and `need` as `""`, so the returned `need` is understood from this message alone. A follow-up such as 换一本 sends the saved `need` and recent user lines.

```json
{
  "status": "shelf",
  "reply": "店员的一句回声",
  "need": "睡不着",
  "hotlines": [],
  "conversationId": "uuid",
  "books": [
    {
      "id": "uuid",
      "titleHint": "*静*",
      "sealNote": "书名先不写全，只留一个字。收到才揭晓。",
      "matchReason": "这一本把夜里的声音放得很轻。\n读起来不费劲。",
      "highlights": ["这一本把夜里的声音放得很轻。", "读起来不费劲。"],
      "tags": ["夜里"],
      "publishYear": 2018,
      "doubanRating": 8.6,
      "listPriceYuan": 48,
      "offerPriceYuan": 43.2,
      "canShip": true,
      "shippingNote": "由乐开书店推荐并为你发货。"
    }
  ]
}
```

`status` `crisis` includes `hotlines` and no books. `sealed` means this is not a book request. `error` returns `message` with HTTP 400 or 500. Query must be 1–500 characters.

The response never includes the title, author, cover, or summary. Do not add them from anywhere else.

`need` is the one-sentence understanding of what the person wants. Print it unchanged before the first book. `highlights` is the same reason the website shows, already split into separate lines. Print each line unchanged. `tags`, `publishYear`, and `doubanRating` are the same facts on the website card.

## POST /api/agent/otp

Creates the account if it does not exist. No password. No browser.

```json
{ "channel": "phone", "to": "13800138000" }
```

`channel` is `phone` or `email`. Phone accepts `13800138000`, `8613800138000`, or `+8613800138000`, and only mainland China. Email is a normal address. The email's Supabase template must contain the code (`{{ .Token }}`). Tell the user to paste the digits and ignore a link.

```json
{ "ok": true, "channel": "phone", "ttlSeconds": 300, "resendAfterSeconds": 60 }
```

HTTP 429: wait. HTTP 500 with the SMS-not-ready message: switch to email.

## POST /api/agent/otp/verify

```json
{ "channel": "phone", "to": "+8613800138000", "code": "482913" }
```

Phone codes are 6 digits. Email codes are 6 to 8 digits.

```json
{
  "ok": true,
  "accessToken": "",
  "refreshToken": "",
  "expiresAt": 1700000000,
  "userId": "uuid",
  "accountLabel": "+86 138****8000"
}
```

Write this into the session file. `expiresAt` is unix seconds. Do not show the tokens.

Wrong or expired codes return HTTP 400. After five wrong phone codes the code is dead: send a new one.

## POST /api/agent/session/refresh

```json
{ "refreshToken": "" }
```

Same payload as verify. HTTP 401 means bind again with a new code.

## POST /api/agent/orders

Bearer required. Price is calculated on the server. The book is always sealed.

```json
{
  "prescriptionId": "uuid from books[].id",
  "recipientName": "张三",
  "phone": "13800138000",
  "address": "上海市徐汇区某某路 1 号",
  "region": "CN"
}
```

`region` is `CN` or `OVERSEAS`. Omit it and the order ships to mainland China. Mainland shipping is free. Overseas adds `shippingFeeYuan` 50, once per order. The server sets the fee. Do not send a shipping amount.

```json
{
  "ok": true,
  "orderId": "uuid",
  "titleHint": "*静*",
  "listPriceYuan": 48,
  "offerPriceYuan": 43.2,
  "shippingFeeYuan": 0,
  "payableYuan": 43.2,
  "status": "pending",
  "checkoutReady": true,
  "checkoutUrl": "https://checkout.stripe.com/..."
}
```

`checkoutReady: false` means the order exists and the card page is not open. HTTP 401: refresh once, then bind again.

## GET /api/agent/orders

Bearer. Up to 20 recent orders: `id`, `label`, `listPriceYuan`, `offerPriceYuan`, `status`, `createdAt`, `paidAt`, `recipientName`.

## GET /api/agent/orders/{id}

Bearer. Adds `phone`, `address`, `shippingFeeYuan`, `vendorName`, `wechat`, `carrier`, `trackingNumber`. `status` is `pending`, `paid`, `shipped`, or `cancelled`. `label` is the mask.

## POST /api/agent/orders/{id}/pay

Bearer. A new card link for an order that is still `pending`.

```json
{ "ok": true, "orderId": "uuid", "checkoutReady": true, "checkoutUrl": "https://checkout.stripe.com/..." }
```

HTTP 409: do not pay again. HTTP 503: payment is not open.

After the card page, the user lands on `/agent/paid`. That page has no login. Wait for them to return, then read the order. Payment is confirmed only when `status` is `paid` or `shipped`.
