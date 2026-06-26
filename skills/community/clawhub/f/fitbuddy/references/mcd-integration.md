# 🍔 fitbuddy × McDonald's MCP Integration

## Overview

fitbuddy can integrate with the McDonald's MCP server to provide precise nutrition data, smart meal recommendations, and diet plans. This is an **optional** enhancement — fitbuddy works perfectly without it.

### Neutral Position Principle

- McDonald's data is a **nutrition source**, not a recommendation engine
- Never proactively suggest any specific restaurant
- All food recommendations are nutrition-driven and include all sources equally
- User makes all decisions; fitbuddy provides data

---

## Setup Guide

### Step 1: Get McDonald's MCP Authorization

1. Visit 👉 <https://open.mcd.cn/mcp>
2. Log in or register a McDonald's account
3. Copy your Authorization Token

### Step 2: Configure MCP

**If you have mcporter installed (recommended):**

```bash
# Add McDonald's MCP server (replace "YOUR_TOKEN" with the token from Step 1)
mcporter config add mcd-mcp "https://mcp.mcd.cn" --header "Authorization=Bearer YOUR_TOKEN"

# Verify configuration
mcporter list mcd-mcp
```

**If you don't have mcporter:**

```bash
# Install mcporter first
npm install -g mcporter

# Then run the config add command above
```

**If you prefer manual config, create `config/mcporter.json` in your workspace:**

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

### Step 3: Enable in fitbuddy

Tell your AI assistant: "启用麦当劳集成" / "enable McDonald's integration"

fitbuddy will auto-detect the MCP config and guide you through feature selection.

---

## Features

| Feature | Description | Default |
|---------|-------------|---------|
| 📊 Precise Nutrition Logging | Say "ate a Big Mac" → auto-fetch exact macros from McDonald's | ON |
| 🍽️ Smart Recommendations | Include restaurant options in meal suggestions (alongside other foods, equally ranked) | ON |
| 📋 Restaurant Diet Plan | Create a diet plan with McDonald's meals (user must explicitly request) | ON |
| 🎫 Promo Notifications | Push deals that match your nutrition goals | **OFF** |
| 🎫 Auto-claim Coupons | Automatically claim available coupons | **OFF** |

---

## Feature Details

### 1. Precise Nutrition Logging

When user mentions eating a McDonald's item:

```
User: "午餐吃了巨无霸"
  → Check restaurant_integration.enabled
  → If enabled + mcd-mcp available:
    → Call MCP query-meal-detail for exact nutrition
    → Record to fitbuddy, cache to food-db (source: "麦当劳MCP")
    → Output standard record template
  → If disabled or MCP unavailable:
    → Fall back to estimation flow (nutrition-guide.md)
```

### 2. Smart Recommendations (Neutral)

When user asks "what should I eat" / "不知道吃啥":

```
  → Calculate remaining macros
  → Recommend from all sources equally:
    1. Home-cooked meals (based on diet_habits + budget)
    2. Food database combinations
    3. [If restaurant integration enabled] Restaurant menu options
  → Mix all recommendations, sort by nutrition match
  → No source highlighting, user decides
```

### 3. Restaurant Diet Plan

When user explicitly asks "帮我制定麦当劳减脂计划":

```
  → Confirm intent: "Only McDonald's, or mixed with home cooking?"
  → Fetch full menu nutrition via MCP
  → Generate plan aligned with carb cycling strategy
  → Always include home-cooking alternatives (never recommend 3 fast-food meals/day)
```

### 4. Promo Notifications (Opt-in Only)

Only active when user enables `promo_notifications: true` in profile.

```
  → Cron checks campaign-calendar + available-coupons
  → If promo_filter: "diet_friendly" → only push high-protein/low-cal deals
  → If promo_filter: "all" → push all deals
  → Respect promo_frequency: "daily" / "weekly"
  → User can disable anytime
```

---

## Profile Configuration

Auto-generated during setup, or manually edit `fitbuddy-data/profile.json`:

```json
{
  "restaurant_integration": {
    "enabled": true,
    "mcd": {
      "enabled": true,
      "mcp_server": "mcd-mcp",
      "features": {
        "precise_nutrition": true,
        "smart_recommend": true,
        "diet_plan": true,
        "promo_notifications": false,
        "promo_frequency": "weekly",
        "promo_filter": "diet_friendly",
        "auto_claim_coupons": false
      },
      "preferred_store": null,
      "order_type": "pickup"
    }
  }
}
```

---

## Safety Rules

- `promo_notifications` defaults to **OFF**
- `promo_filter: "diet_friendly"` filters out nutritionally poor options
- Restaurant diet plans must include home-cooking alternatives
- Never frame restaurant options as "better" than home cooking
- All recommendations are nutrition-driven, never commercially motivated
