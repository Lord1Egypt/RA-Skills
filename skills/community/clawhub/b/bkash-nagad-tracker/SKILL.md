---
name: bkash-nagad-tracker
description: >
  Log bKash, Nagad, Rocket, and cash transactions
  conversationally in Bengali or English. Get weekly
  spending digests every Sunday. Built for Bangladesh.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🇧🇩"
    primaryEnv: ANTHROPIC_API_KEY
    requires:
      env:
        - ANTHROPIC_API_KEY
      bins:
        - python3
    os:
      - linux
      - darwin
      - win32
    heartbeat:
      schedule: "0 9 * * 0"
      command: "python3 {baseDir}/summarizer.py weekly"
---

# bKash / Nagad Transaction Tracker 🇧🇩

Track your daily spending across bKash, Nagad, Rocket,
and cash — in Bengali or English — and get an automatic
weekly digest every Sunday morning.

---

## When to activate this skill

Activate when the user says anything that contains:

**Transaction logging signals:**
- Any amount in taka, tk, ৳, or BDT
- Words: bKash, Nagad, Rocket, cash, paid, bought,
  sent, spent, খরচ, পাঠালাম, কিনলাম, দিলাম
- "log", "track", "record" + any amount
- Bengali amounts: "পাঁচশো টাকা", "এক হাজার"

**Summary signals:**
- "summary", "digest", "report", "weekly"
- "এই সপ্তাহে কত খরচ", "spending this week"
- "show my transactions", "কত টাকা গেলো"

**Delete/edit signals:**
- "delete last", "undo", "শেষেরটা মুছো"
- "edit transaction", "correct last entry"

---

## How to log a transaction

### Step 1 — Parse the message

Call the parser to extract structured data:

```bash
python3 {baseDir}/parser.py "{user_message}"
```

This returns JSON:
```json
{
  "amount": 500,
  "method": "bkash",
  "category": "food",
  "note": "lunch",
  "confidence": "high"
}
```

If `amount` is null → ask the user:
"কত টাকা? / How much?"

If `confidence` is "low" → confirm before saving:
"Did you mean: 500৳ for food via bKash? (yes/no)"

### Step 2 — Save the transaction

```bash
python3 {baseDir}/logger.py log \
  --amount {amount} \
  --method {method} \
  --category {category} \
  --note "{note}"
```

### Step 3 — Confirm to user

Reply in the same language the user wrote in:

**English:** "✅ Logged: {amount}৳ — {category} ({method_emoji})"

**Bengali:** "✅ লগ হয়েছে: {amount}৳ — {category} ({method_emoji})"

**Method emojis:**
- bKash → 🔴
- Nagad → 🟠
- Rocket → 🟣
- Cash → 💵

---

## How to generate a summary

### On-demand summary

When user asks for summary/digest:

```bash
python3 {baseDir}/summarizer.py weekly
```

Format the output as a clean digest message and send.

### Automatic weekly digest (Heartbeat)

Every Sunday at 9:00 AM local time:
1. Run `python3 {baseDir}/summarizer.py weekly`
2. Send digest to user automatically
3. No user prompt needed

---

## How to delete/undo last transaction

```bash
python3 {baseDir}/logger.py undo
```

Reply: "✅ Last transaction deleted."

---

## How to show recent transactions

When user asks "what did I log today" or "recent":

```bash
python3 {baseDir}/logger.py recent --n 5
```

Format as a simple numbered list.

---

## Category mapping reference

Use this to classify ambiguous messages:

| Keywords | Category |
|---|---|
| food, lunch, dinner, breakfast, restaurant, খাবার, রেস্তোরাঁ | food |
| rickshaw, CNG, Uber, bus, train, ভাড়া, যাতায়াত | transport |
| rent, বাড়িভাড়া | rent |
| electricity, gas, water, internet, bill, বিল | utilities |
| mum, dad, family, bhai, apa, মা, বাবা, ভাই, আপা, sent to | remittance |
| medicine, doctor, hospital, ডাক্তার | medical |
| school, tuition, books, পড়াশোনা | education |
| clothes, shoes, shopping, কেনাকাটা | shopping |
| everything else | other |

---

## Example conversations

**English input:**
```
User:  "bkash 450 lunch"
Agent: ✅ Logged: 450৳ — Food 🔴

User:  "sent 5000 to mum nagad"
Agent: ✅ Logged: 5000৳ — Remittance 🟠

User:  "show my spending this week"
Agent: [weekly digest]
```

**Bengali input:**
```
User:  "৳৮৫০ বিকাশে বাজার করলাম"
Agent: ✅ লগ হয়েছে: 850৳ — Shopping 🔴

User:  "রিকশায় ৮০ টাকা নগদ"
Agent: ✅ লগ হয়েছে: 80৳ — Transport 💵

User:  "এই সপ্তাহে কত খরচ হলো"
Agent: [সাপ্তাহিক সারসংক্ষেপ]
```

**Mixed input:**
```
User:  "electricity bill 1200 bkash dilam"
Agent: ✅ Logged: 1200৳ — Utilities 🔴
```

---

## Error handling

- **Python not found:** Tell user to install Python 3.10+
- **Parse fails:** Ask user to rephrase: "Could you say
  that again with the amount? e.g. '500 taka food bKash'"
- **Storage error:** Log error, tell user to try again
- **No transactions this week:** Reply "No transactions
  logged yet this week. Start by sending me your first
  expense!"
