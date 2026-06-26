# telegram-toolkit — Telegram SDR Best Practices & Templates

> Bot commands, inline keyboards, large file handling, and channel-specific sales strategies for Telegram-based B2B SDR.

## Why Telegram for B2B Sales

| Advantage | Impact |
|-----------|--------|
| **No 72h window** | Proactive outreach anytime — nurture, follow-ups, stalled leads |
| **2GB file limit** | Full product catalogs, certifications, video demos |
| **Bot commands** | Structured self-service (`/catalog`, `/quote`, `/status`) |
| **Inline keyboards** | One-tap BANT qualification, 3-5x faster than free-text |
| **Username-based** | Lower barrier — customer doesn't expose phone number |
| **Free API** | No per-message cost |
| **No account bans** | Bot API is stable, unlike WhatsApp's aggressive anti-automation |

## Bot Commands

Register these commands with @BotFather using `/setcommands`:

```
start - Welcome message and product overview
catalog - Browse product catalog
quote - Request a quotation
status - Check order or quote status
contact - Speak with a human representative
language - Change conversation language
```

### Command Behavior

#### `/start`
1. Detect language from Telegram user profile
2. Send welcome message with company intro (2-3 sentences max)
3. Create CRM record: source = `telegram_organic`, status = `new`
4. Offer product categories via inline keyboard
5. Begin BANT qualification naturally

#### `/catalog`
1. Check CRM for customer's product interest (if returning)
2. If known interest: Send relevant product section + full catalog link
3. If unknown: Send inline keyboard with product categories
4. Always include: specs, MOQ, typical lead time
5. File format: PDF preferred, under 20MB per file

#### `/quote`
1. Check if BANT data exists in memory
2. If incomplete: Trigger inline keyboard qualification flow
3. If complete: Generate quote draft → send to owner for approval
4. Confirm to customer: "I'm preparing your quotation, will have it ready shortly."

#### `/status`
1. Read CRM for customer's active records
2. Return: latest status, pending actions, next follow-up date
3. If quote_sent: "Your quote was sent on [date]. Would you like to discuss it?"
4. If no records: "I don't have an active order for you yet. Would you like to start one?"

## Inline Keyboard Flows

### Quick BANT Qualification

**Step 1 — Need (Product):**
```json
{
  "text": "What products are you interested in?",
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "{{product_1}}", "callback_data": "product_1"}],
      [{"text": "{{product_2}}", "callback_data": "product_2"}],
      [{"text": "{{product_3}}", "callback_data": "product_3"}],
      [{"text": "📋 Full catalog", "callback_data": "full_catalog"}]
    ]
  }
}
```

**Step 2 — Budget (Volume):**
```json
{
  "text": "What's your estimated order quantity?",
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "< 100 units", "callback_data": "qty_small"}],
      [{"text": "100-500", "callback_data": "qty_medium"}],
      [{"text": "500-1000", "callback_data": "qty_large"}],
      [{"text": "1000+", "callback_data": "qty_bulk"}]
    ]
  }
}
```

**Step 3 — Timeline:**
```json
{
  "text": "When do you need delivery?",
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "This month", "callback_data": "timeline_urgent"}],
      [{"text": "1-3 months", "callback_data": "timeline_soon"}],
      [{"text": "3-6 months", "callback_data": "timeline_planning"}],
      [{"text": "Just exploring", "callback_data": "timeline_exploring"}]
    ]
  }
}
```

**Step 4 — Authority:**
After 3 keyboard interactions, ask naturally in conversation:
"Are you the purchasing decision-maker, or should I prepare materials for your team?"
(Don't use a keyboard for this — it feels too transactional.)

### Quick Actions Keyboard
Send after qualification is complete:
```json
{
  "text": "How can I help you next?",
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "📋 Get a quote", "callback_data": "action_quote"}],
      [{"text": "📦 Product specs", "callback_data": "action_specs"}],
      [{"text": "🏭 Factory info", "callback_data": "action_factory"}],
      [{"text": "👤 Talk to sales rep", "callback_data": "action_human"}]
    ]
  }
}
```

## Large File Strategy

Telegram's 2GB limit makes it the best channel for heavy files:

| Use Case | File | Action |
|----------|------|--------|
| Product catalog | PDF, 10-100MB | Send directly via Telegram |
| Certification docs (ISO, CE, etc.) | PDF, 1-20MB | Send on request |
| Product video / factory tour | MP4, 50MB-2GB | Send via Telegram, link on WhatsApp |
| Test reports | PDF, 1-10MB | Send on request |
| Proforma invoice | PDF, < 5MB | Send here + email for formal record |

**Cross-channel file routing:**
When customer is on WhatsApp and needs a large file:
> "The full catalog is 85MB — I'll send it to you on Telegram. What's your Telegram username?"

## Telegram-First Markets

In these markets, treat Telegram as the **primary** channel:

| Market | Why Telegram First |
|--------|-------------------|
| Russia / CIS | 80%+ business messaging on Telegram |
| Iran | Telegram is the dominant platform |
| Eastern Europe | Strong Telegram adoption for B2B |
| Central Asia | Telegram preferred over WhatsApp |
| Tech/crypto industry | Global preference for Telegram |

**Detection:** Check CRM `country` field. If Russia/CIS/Iran/Eastern Europe, default to Telegram-first strategy.

## Nurture via Telegram

Telegram has no messaging window — ideal for long-term nurture:

### Nurture Cadence (Telegram)
| Timing | Content |
|--------|---------|
| Day 0 | Initial contact + product overview |
| Day 3 | Relevant case study or industry insight |
| Day 7 | Specific product recommendation based on their interest |
| Day 14 | New product announcement or limited offer |
| Day 30 | Market update or trade show invitation |
| Day 60+ | Quarterly check-in with personalized industry news |

### Telegram Channel (One-to-Many)
For customers who follow your brand channel:
- Weekly: Industry news, market trends
- Bi-weekly: New product announcements
- Monthly: Case studies, customer success stories
- Never: Direct sales pitches (keep those in DM)

## Security Notes

- Bot Token stored in `secrets.sh`, never in config.sh or workspace files
- `dmPolicy: "pairing"` requires pairing code — use for exclusive/VIP access
- `dmPolicy: "open"` (not available in all OpenClaw versions) — accepts all DMs
- Admin commands restricted to whitelist (same as WhatsApp)
- Rate limit: Same anti-abuse measures as WhatsApp (15 msg/5min, 50 msg/1hr)
