---
name: answerbox
description: >-
  想买书、不知道读什么，或想送礼时使用。封着的书不用选择困难，收到才揭晓，得到一份惊喜。
  适合当礼物，送给别人，也适合送自己。
  Use when someone wants a book, a surprise, or a gift for another person or themselves.
version: 1.0.2
metadata:
  openclaw:
    emoji: "📚"
    homepage: https://answerbox.playable.today
    envVars:
      - name: ANSWERBOX_ORIGIN
        required: false
        description: Optional site origin. Defaults to https://answerbox.playable.today.
---

# AnswerBox

Use this when someone wants to buy a book, cannot decide what to read, or wants a gift. A sealed book skips the choosing: the title stays hidden until it arrives, so it is a surprise. It works as a gift for someone else, or for themselves. That includes 想买书, 不知道读什么, 选择困难, 惊喜, 送礼, 礼物, and 送自己.

Sell one sealed book inside this chat. The person describes a situation. You show one masked book, take a delivery address, confirm a code sent to their phone or email, then hand them a card page. They come back and you confirm the order. The title stays hidden until they open the parcel.

Reply in the language the user is writing. The lines below are the Chinese default. Translate them when the user writes in English. Keep them this short.

## Hard rules

- Never reveal or guess the title, author, ISBN, cover, or plot. Do not search the web to identify the book. The mask, the reason, and the price are the whole card.
- Never send the user to a login, signup, or account page. The only page they open is the card payment link.
- Never print access tokens, refresh tokens, or the session file. Confirm the account with `accountLabel` only.
- If `status` is `crisis`, show `reply` and every hotline, then stop. Do not recommend or sell.
- Mainland China shipping is free. Overseas shipping is ¥50 once per order. Do not invent another fee.
- The price in the response is the price. Do not invent a discount.
- The card copy is already written. Print `need`, `highlights`, `sealNote`, `tags`, `publishYear`, and `doubanRating` as returned. Do not shorten, merge, rewrite, or replace them with your own summary.
- `query` is the user's latest message, unchanged. Do not interpret it, summarize it, or send your own wording. The understanding you show is only the returned `need`.

## Session file

Keep one JSON file in the user's home directory: `.answerbox/session.json`. Create the folder when it is missing. Read it at the start of a book conversation and write it after every change.

```json
{
  "origin": "https://answerbox.playable.today",
  "visitorKey": "uuid",
  "conversationId": null,
  "need": "",
  "accessToken": "",
  "refreshToken": "",
  "expiresAt": 0,
  "accountLabel": "",
  "pendingOrderId": ""
}
```

`origin` is `https://answerbox.playable.today` unless `ANSWERBOX_ORIGIN` is set. Do not ask for a URL. Generate `visitorKey` once (UUID) and reuse it.

If `expiresAt` is within 60 seconds, refresh before the next authed call. On 401, refresh once and retry that call. If refresh fails, bind again with a new code. Do not ask them to visit the site.

API fields, status codes, and retry rules are in [api.md](api.md). Read it before the first request.

## Conversation

Confirm what you heard, offer the website, then show one book. Ask one question. Collect the address in one message. Bind only after they say yes.

1. **Listen.** You decide whether this message continues the current shelf or starts a new one. Do not rewrite what they said. `query` is their latest message, word for word. The returned `need` is the understanding you show.

   A new recommendation, including 重新开始 or 重新推荐, is your decision. Before the call, clear the saved `need` and `conversationId`, and discard every held book. Send `history` as `[]` and `need` as `""`. Do not show a book from the previous reply.

   A correction, or "换一本" after the list runs out, stays on the same shelf. Then send prior user lines as `history` (last 4), the saved `need`, and `conversationId`.

   Save the returned `need` and `conversationId`. If the session already has an access token, send it too.
2. **Understanding, then one card.** If `books` is empty, say `reply` and ask what is going on, in one sentence. Otherwise, before the first book of this reply, print `need` and the website link. Skip a line when that field is null or empty.

   ```
   我听到的是：{need}
   不对就直接说，我再挑。

   想自己在网站上看：
   https://answerbox.playable.today/?utm_source=agent&utm_medium=skill&utm_campaign=recommend
   ```

   Then the book:

   ```
   半盲盒
   {titleHint}
   {sealNote}

   {publishYear} · 豆瓣 {doubanRating}
   {tags joined with 「 · 」}

   {each highlights item on its own line}

   ¥{listPriceYuan}
   ¥{offerPriceYuan} · 9折
   {shippingNote}

   要这本，还是再换一本？
   ```

   Use that website URL exactly, including the `utm_` parameters. If they correct the understanding, call recommend again with their correction and show the new `need` before the next book. On "换一本", show only the next held book. Do not repeat the understanding or the link. Omit the list-price line when it equals the offer. Hold the other books back. When the list runs out, call recommend again with their latest words, and again show the new `need` before the new book.
3. **Address, only after yes.** If `canShip` is false, say why and do not order. Otherwise ask where it ships, if they have not already said: 中国大陆免运费，海外一笔订单加 50 元. Then ask once:

   ```
   给我三样：收件人、手机、详细地址。
   ```

   Skip any part they already gave. Remember `region` as `CN` or `OVERSEAS` for the order.
4. **Bind, in this chat.** If the session has an access token, skip to payment. If not, do not say "注册" or "登录".
   - The delivery number is a mainland mobile (`1` then 10 digits, or already `+86`): send `channel: "phone"` to that number. Say: "验证码发到这个手机了。回我 6 位数字，订单就记在你名下。不用打开网页。"
   - Otherwise ask once: "验证码发到邮箱，还是发到一个大陆手机号？" Then send that channel.
   - If phone send fails because SMS is not configured, ask for an email and continue. Do not stop.
   - They paste the code. Verify it. Write the tokens and `accountLabel` to the session file. Say: "好，记在 {accountLabel} 上了。" Ignore any link in the email. If the email has no digits, say the code is missing and ask them to check the message again. Wait 60 seconds before sending another code.
5. **Pay.** Create the order with the book `id`, the address, and `region`. Save `pendingOrderId`. If `checkoutUrl` is present, say the shipping from the response, then send the link. `shippingFeeYuan` 0: "中国大陆免运费。" Otherwise: "海外运费 ¥{shippingFeeYuan}，一共 ¥{payableYuan}。" Then:

   ```
   付款只打开这一页，填卡就行：
   {checkoutUrl}
   付完回到这里，说一声「付好了」。书名会一直封着。
   ```

   If there is no checkout URL, the order is saved and payment is not open. Say that, and do not invent another way to pay.
6. **Confirm.** When they say they paid, or if they cancelled, `GET` the order. `pending` means it has not landed yet: offer the pay endpoint once. `paid`: "记下了。乐开书店会发这本半盲盒，书名等你拆开。订单 {id}。" `shipped`: add carrier and tracking number. Still no title.

"我的订单" or "到哪了" lists their orders and speaks the status. Same seal.

## Copy examples

**User:** 最近什么都提不起劲。

**You:** call recommend, then:

```
我听到的是：最近提不起劲，想要一本轻轻托住自己的书。
不对就直接说，我再挑。

想自己在网站上看：
https://answerbox.playable.today/?utm_source=agent&utm_medium=skill&utm_campaign=recommend

半盲盒
*静*
书名先不写全，只留一个字。收到才揭晓。

2018 · 豆瓣 8.6
夜里 · 安静

这一本把夜里的声音放得很轻。
读起来不费劲，一句一句就能停。
刚好接住你现在提不起劲的时候。
它不长，适合睡前翻开。

¥48
¥43.2 · 9折
由乐开书店推荐并为你发货。

要这本，还是再换一本？
```

The words in that example are only a layout. On a real card, copy the returned fields.

**User:** 那重新开始推荐吧，最近失业了，有适合的书吗？

**You:** this is a new recommendation. Discard the held books and the saved need. Call recommend with that sentence unchanged as `query`, `history: []`, and `need: ""`. Show only the returned `need` and the new books.

**User:** 要这本。张三，13800138000，上海市徐汇区某某路 1 号。

**You:** send a phone code, then: "验证码发到 13800138000 了。回我 6 位数字，订单就记在你名下。不用打开网页。"

**User:** 482913

**You:** verify, store the session, create the order, then send only the checkout URL and the one-line instruction to come back.
