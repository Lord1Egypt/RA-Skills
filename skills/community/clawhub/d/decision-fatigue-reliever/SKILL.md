---
name: decision-fatigue-reliever
description: Helps you make quick decisions on daily trivial matters (food, clothing, activities, shopping), reducing choice anxiety and freeing up cognitive resources. Use when the user says "what should I eat", "what to wear", "help me decide", "don't know what to buy", or any trivial decision-making requests.
---

# Decision Fatigue Reliever

## Overview

Helps you make quick decisions on daily trivial matters, reducing choice anxiety and freeing up cognitive resources.

> **"Let AI handle the trivial decisions, save your energy for what truly matters"**

---

## Triggers

### Natural Language Triggers

| Decision Type | Example Triggers |
|--------------|------------------|
| 🍽️ **What to Eat** | "What should I eat for lunch", "Help me decide dinner", "Suggest breakfast", "Don't know what to eat" |
| 👔 **What to Wear** | "What should I wear today", "Help me pick an outfit", "What to wear for an interview tomorrow", "What to wear in this weather" |
| 🎯 **What to Do** | "Don't know what to do this weekend", "What to do after work", "Want to exercise, what should I choose" |
| 🛒 **What to Buy** | "What gift for my friend", "Want to buy headphones, recommend one", "Help me choose something cost-effective" |

### Quick Commands

| Command | Function |
|---------|----------|
| `/decide food` | Quick food decision |
| `/decide outfit` | Quick outfit decision |
| `/decide activity` | Quick activity decision |
| `/decide buy [item]` | Quick purchase decision |
| `/decide random` | Completely random decision |

---

## Core Features

### 🍽️ Food Decisions

**Applicable Scenarios**: Breakfast, lunch, dinner, snacks, group dining

**Optional Inputs**:
- Budget range (Economy / Standard / Unlimited)
- Taste preference (Light / Heavy / Spicy / Sweet, etc.)
- Time constraint (Rushed / Normal / Relaxed)
- Dietary restrictions (Vegetarian / Halal / Allergies, etc.)

**Output**:
- Recommended dish/restaurant
- Reasoning (taste, nutrition, convenience)
- Estimated price and time
- Alternative options

**Example**:
```
User: What to eat for lunch? Budget 50, short on time

AI: 🍽️ Lunch Decision: Business Set Meal

📍 Recommendation: [Yoshinoya] Beef Bowl Set
📋 Reasoning: Fast service (3-5 min), within budget (¥45), filling
⏱️ Time: 20-25 minutes

💡 Alternatives: Convenience store bento (faster) / Light salad (healthier)
```

---

### 👔 Outfit Decisions

**Applicable Scenarios**: Daily wear, occasion dressing, weather adaptation

**Optional Inputs**:
- Occasion (Work / Date / Exercise / Formal event)
- Weather/temperature
- Style preference (Minimalist / Fashionable / Vintage, etc.)

**Output**:
- Complete outfit plan (Top + Bottom + Shoes + Accessories)
- Styling reasoning (color, occasion fit, comfort)
- Weather adaptation notes
- Alternative outfits

**Example**:
```
User: First date tomorrow, 18°C, what to wear?

AI: 👔 Date Outfit: Clean Gentleman Style

🧥 Outfit:
• White T-shirt + Light gray casual blazer
• Dark blue slim-fit jeans
• White sneakers + Simple watch

📋 Reasoning: Can remove blazer at 18°C, suitable for restaurant + movie, clean color palette
💡 Alternatives: More formal (shirt + leather shoes) / More casual (remove blazer)
```

---

### 🎯 Activity Decisions

**Applicable Scenarios**: Weekend activities, after-work plans, exercise choices, work-life balance

**Optional Inputs**:
- Available time (duration)
- Energy level (High / Medium / Low)
- Budget (Free / Low / Medium / High)
- Group size (Solo / Friends / Family)

**Output**:
- Recommended activity plan
- Activity reasoning (fit analysis)
- Required preparation
- Estimated duration and cost
- Alternative activities

**Example**:
```
User: Weekend alone, don't want to spend much, want to go out

AI: 🎯 Weekend Activity: Park Picnic + Reading

📍 Recommendation: City park picnic
📋 Reasoning: Solo-friendly, low cost (under ¥50), outdoor + digital detox
🎒 Preparation: Picnic mat, sandwich, fruit, book to read
⏱️ Duration: 3-4 hours
💰 Cost: ¥30-50

💡 Upgrade: Bring camera for photography practice / Bird and plant watching
```

---

### 🛒 Purchase Decisions

**Applicable Scenarios**: Gift shopping, daily necessities, electronics comparison, value shopping

**Optional Inputs**:
- Product category
- Purchase purpose/usage scenario
- Budget limit
- Recipient info (age/gender/preferences)
- Priority (price/quality/brand/features)

**Output**:
- Recommended product/brand (1-3 options)
- Reasoning (fit analysis)
- Price comparison
- Purchase channel suggestions

**Example**:
```
User: Birthday gift for mom, budget 300-500

AI: 🎁 Gift Decision: Silk Scarf + Hand Cream Set

🎯 Recommendation: Wensli silk scarf + L'Occitane hand cream
📋 Reasoning: Matches 50+ elegant taste, practical, mom values skincare
💰 Budget: ¥300-500
🛒 Channel: Tmall flagship store

💡 Alternatives: Massager (for neck/shoulder pain) / Tea gift set (if she loves tea)
```

---

## Decision Templates

### Standard Output Format

```markdown
🎯 Decision: [Specific recommendation]

📋 Reasoning:
• [Reason 1 - Preference match]
• [Reason 2 - Scenario fit]
• [Reason 3 - Other value]

💰 Estimated Cost: [Price range]
⏱️ Estimated Time: [Time needed]

💡 Alternatives:
1. [Alternative 1]
2. [Alternative 2]

❓ Satisfaction: [👍 Satisfied / 👎 Not satisfied / 🔄 Try another]
```

### Quick Decision Mode

When user says "hurry", "whatever", "quick", use simplified output:

```markdown
🚀 Quick Decision: [Result]

Reason: [One sentence]

Say "another one" if not satisfied
```

---

## Usage Examples

### Example 1: Workday Lunch
```
User: What to eat for lunch? Budget 50, near office, short on time

AI: 🍽️ Lunch Decision: Business Set Meal

📍 Recommendation: [Yoshinoya/Sukiya] Beef Bowl Set
📋 Reasoning: Fast service (3-5 min), within budget (¥40-50), filling for afternoon
⏱️ Time: 20-25 minutes

💡 Alternatives: Convenience store bento (faster) / Light salad (healthier)
```

### Example 2: Date Outfit
```
User: First date tomorrow night, 18°C, dinner and movie

AI: 👔 Date Outfit: Clean Gentleman Style

🧥 Outfit:
• White T-shirt + Light gray casual blazer
• Dark blue slim-fit jeans
• White sneakers + Simple watch

📋 Reasoning: Can remove blazer at 18°C, suitable for restaurant + movie, clean colors show effort
💡 Alternatives: More formal (shirt + leather shoes) / More casual (remove blazer)
```

### Example 3: Weekend Activity
```
User: Weekend alone, don't want to spend much, want to go out

AI: 🎯 Weekend Activity: Park Picnic + Reading

📍 Recommendation: City central park
📋 Reasoning: Solo-friendly, low cost (under ¥50), outdoor + digital detox
🎒 Preparation: Picnic mat, sandwich, fruit, book to read
⏱️ Duration: 3-4 hours
💰 Cost: ¥30-50
```

### Example 4: Gift Shopping
```
User: Birthday gift for mom, budget 300-500

AI: 🎁 Gift Decision: Silk Scarf + Hand Cream Set

🎯 Recommendation: Wensli silk scarf + L'Occitane hand cream
📋 Reasoning: Matches 50+ elegant taste, highly practical, mom values skincare
💰 Budget Match: ¥300-500
🛒 Channel: Tmall flagship store

💡 Alternatives: Massager (for neck/shoulder pain) / Tea gift set (if she loves tea)
```

---

## Decision Principles

### 1. Decision First
Give a clear decision result first, then explain the reasoning

### 2. Transparent Reasoning
Help users understand the logic behind the decision

### 3. Provide Alternatives
Always provide 1-2 alternative options

### 4. Feedback Loop
Every output includes a feedback entry point

### 5. Personalization
Adjust recommendations based on user context and preferences

---

## Safety Escalation (High-Risk Response)

⚠️ **Stop the normal decision-support flow immediately** if the user expresses any of the following:
- self-harm or suicide thoughts related to decisions
- overwhelming despair or inability to make any decisions
- obvious acute mental-health crisis that makes decision support inappropriate

Use a direct response like:

> ⚠️ Important: This is not the right time to continue normal decision support. If you may harm yourself or someone else, or cannot keep yourself safe, contact a trusted person nearby immediately and reach out to local emergency services, an emergency department, a crisis hotline, or a licensed professional as soon as possible.

Then keep the tone calm, direct, and serious. Do not continue normal decision guidance until safety is addressed.

---

## Boundaries & Limitations

### Supported
✅ Daily trivial matters: food, clothing, activities, shopping

### Not Supported
❌ Major life decisions: career choices, investment decisions, medical decisions, legal decisions

### Disclaimer
> ⚠️ **Disclaimer**: This tool is only for everyday low-stakes decision support and does not constitute medical advice, investment advice, legal advice, or any other professional guidance. For major decisions involving health, safety, finances, or career development, consult a qualified professional. Users remain responsible for their own decisions and outcomes.

### This skill can:
- help with daily trivial decisions (food, clothing, activities, shopping)
- reduce choice anxiety through quick recommendations
- provide alternatives for user to choose from

### This skill must not:
- make decisions about mental health treatment
- claim the user has decision-making disorders
- present recommendations as medical or psychological advice
- replace professional counseling, legal advice, or financial planning

---

## Technical Information

| Attribute | Value |
|-----------|-------|
| **Skill ID** | `decision-fatigue-reliever` |
| **Version** | 1.0.0 |
| **Author** | harrylabsj |
| **Status** | Stable |
| **Workspace** | `decision-fatigue-reliever` |
| **License** | MIT |

---

*Last updated: 2026-03-23*
