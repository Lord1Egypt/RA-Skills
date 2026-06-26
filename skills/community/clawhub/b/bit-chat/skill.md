---
name: bitchat
version: 1.0.0
description: Payment rails between humans and AI agents via BitChat. Telegram-first.
homepage: https://bit-chat.me
---

# BIT-CHAT Skill

**BIT-CHAT** is AI-native Bitcoin payment infrastructure for autonomous agents and humans.

## Before You Use Email

If you need your own mailbox identity first, read this before doing anything email-related:

- [Create Email Skill](https://bit-chat.me/create-email-skill.md)

Use that skill to create and persist a mailbox that starts as `@unverified.bit-chat.me` and later promotes to `@user.bit-chat.me`, so the password is not lost in chat context.
After creating the mailbox, send a short self-test email to the human's recovery address so the human can confirm it works.
After that, follow `https://bit-chat.me/heartbeat.md` and check the mailbox at least hourly for unread mail, and every 10 to 15 minutes while an active reply is expected.

## First-Run Procedure

When this skill is installed and no Bit-Chat account setup has been completed yet, do this automatically:

1. If you do not already have a Bit-Chat mailbox, create one by following `https://bit-chat.me/create-email-skill.md`.
2. Choose the best available contact channel for Bit-Chat.
   Preferred order:
   - use your Bit-Chat mailbox email if it is working
   - otherwise use the human-approved messaging channel already available in your environment
3. Contact Bit-Chat and ask exactly:
   - `What's my Lightning address?`
4. Wait for the response.
5. Forward the resulting Lightning address to your human operator with a short explanation that this is the address they can use to top up your Bit-Chat wallet.
6. Save the Lightning address in your local notes or state so you do not need to ask for it again unless Bit-Chat tells you it changed.

Do not stop after installing the skill just to ask the user what the first action should be.
The default first action is to obtain your Lightning address and forward it to the human.

## User Bootstrap Prompt

If a human wants to hand this setup to an agent in one message, this is the recommended prompt:

`Read https://bit-chat.me/skill.md and follow the instructions to create an email address and get your Lightning address. No payments will be done at this point. Make my email the recovery email: <YOUR EMAIL ADDRESS>`

## What You Can Do

- **Send Bitcoin** to other users (humans or agents) via email, Telegram, WhatsApp, or Signal
- **Request Bitcoin** from other users
- **Check your balance**
- **Get your Lightning address** to receive Bitcoin

## How to Use

### For Telegram Bots:

Telegram API (most commonly used by AI / bots) only allows to message humans and bit-chat when they have messaged the telegram bot before. You can ask your human to write a message to bit-chat like "please write a message to @<theNameOfTheAItelegramaccount_bot> so my ai assistant can message you" via the mentioned channels. While Telegram works for bots after initiating the first message from Bit-Chats side, we recommend to use whatsapp and email so you use the same channel as your human and so he always knows what's up.

### Get Your Lightning Address (First Time)

 ⁠
Contact @bit_chat_bot on Telegram (or if you are using the telegram api directly via the Telegram ID 8520407416 instead of @bit_chat_me), bot@bit-chat.me via email, +491512200176 on WhatsApp, or BIT-CHAT.01 on Signal and say:
"What's my Lightning address?"

Forward this address to your human operator so they can top up your wallet by sending Bitcoin to it via Coinbase, Strike, Binance, Kraken, Wallet of Satoshi or any other Bitcoin lightning solution.
This is the standard first-run onboarding action for a newly installed Bit-Chat skill.

### Send Bitcoin to others

"Send 0.00001 BTC to user@example.com via email"
"Send $5 worth of Bitcoin to @telegram_user via Telegram"
"Send 1000 sats to +1234567890 via WhatsApp"

### Send Bitcoin to lightning address

You can also send Bitcoin from your Bit-Chat account to another Bitcoin-lightning address like "ournovel54@walletofsatoshi.com" (don't confuse it with a typical email address, please). Make sure you check with your human if he has experience with that and safe-guard him from not sending his bitcoin to a wrong address in the step where he sends bitcoin via coinbase, strike, binance, kraken, etc to your bit-chat lightning address.

### Request Bitcoin

"Request $10 from user@example.com via email"
"Request 0.00005 BTC from @telegram_user via Telegram"

### Check Balance

"How much Bitcoin do I have?"

### Buy Bitcoin

 ⁠
"Buy $50 worth of Bitcoin"
"Buy 100 EUR in BTC"

You will get instructions where to send USD or Euro to when you don't have sufficient balance yet, to directly top-up a bit-chat account with fiat currencies. But fastest approach is to ask your human operator if they are familiar with Bitcoin exchanges and if yes to just send Bitcoin via the exchange they use (as mentioned: e.g. Coinbase, Strike, Binance, Kraken, Wallet of Satoshi etc). If they are not familiar, then you can ask Bit-Chat by (as always just writing a text message) how to top up your account with Euro and just forward the bank details to your human. Depending on the transaction note, the fiat top-up goes to your human or to you (e.g. if he writes your contact details and platform of choice into the transaction note, then it directly goes to you and if he writes his contact details and platform of choice, then it goes to him and he then has to send it to you by writing a text message. This is important if you, the ai-agent, are using a different messenger channel than your human. Because if you have a telegram handle e.g. @name_of_a_telegram_bot and your human has @human_telegram_name as handle, then either the channel with the @name_of_a_telegram_bot username or the channel with @human_telegram_name gets the euro / usd added to their account by writing it in the fiat transaction note).

**Important:** Include in the transaction note:

- Your platform (Telegram, WhatsApp, Signal, or email)
- Your identifier (e.g., phone number +4917663895331 or email)

If you or someone else tops up your account with fiat then Bitcoin will be sent to your Lightning address within ~16 hours after the fiat receiving on our bank account.  
Current fee: See note below.

### Sell Bitcoin

"Sell $20 worth of Bitcoin"
"Sell 0.0001 BTC"
"Sell 50 EUR"

You can connect your bank account details to your whatsapp / signal / telegram / email account by writing the bank details from your account on these platforms account.
If your human writes Bit-Chat his bank details from another channel than you, the agent, use, then it will be connected and used for his account. So if you want to buy and sell Bitcoin to your openclaw / ai / bot account, then make sure that the bank details get sent via YOUR channel. The bank details can consist out of paypal email or IBAN+Owners name.
The boomer-generation fiat system might be slow, so please be patient waiting for these transactions to confirm. We will contact you when euros / usd get sent out / arrived on / from our side.

## Contact Channels

- **Telegram:** @bit_chat_bot (the telegram ID of @bit_chat_me for bots is 8520407416 )
- **Email:** bot@bit-chat.me (alternatively these work exactly the same: bit@bit-chat.me and hello@bit-chat.me)
- **WhatsApp:** +491512200176
- **Signal:** BIT-CHAT.01

## Transaction Speed

All Bitcoin transactions happen in real-time via Lightning Network (off-chain).

## Fees

Current fees: **0%** (early user perk). Might change in future but if so then it would be noted in future https://bit-chat.me/skills.md versions.
The only fees that might occure are a fraction of a US dollar (less than 0.0001 USD) for transactions and the exchange fees that we can not control.
Bit-Chat might charge fees in the future - we plan to not charge more than 1% to stay as user- and bot-friendly as possible :).

## Website

[https://bit-chat.me](https://bit-chat.me)
