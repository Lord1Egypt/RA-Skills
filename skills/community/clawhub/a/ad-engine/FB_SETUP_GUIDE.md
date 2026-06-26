# Facebook Ads API Setup Guide

**Purpose:** Get the 3 credentials needed to deploy ads from the ad-engine skill.
**Time:** ~20 minutes
**You need:** A Facebook personal account and a credit/debit card for ad billing.

---

## What You Need (3 Things)

| Credential | Format | Where It Goes |
|-----------|--------|---------------|
| Access Token | Long string starting with `EAA...` | `--setup` prompt |
| Ad Account ID | `act_XXXXXXXXXX` | `--setup` prompt |
| Page ID | Number like `123456789` | `--setup` prompt |

---

## Step 1: Facebook Business Manager (2 min)

**If you don't have one yet:**

1. Go to **https://business.facebook.com**
2. Click **"Create Account"**
3. Enter business name (e.g., "ClawAgents" or your name)
4. Enter your email
5. Done

**If you already have one:** skip to Step 2.

---

## Step 2: Create a Facebook Page (5 min)

You need a Page to run ads from. This is the "face" of the ad that people see.

1. In Business Manager → **Settings** (gear icon) → **Accounts** → **Pages**
2. Click **Add** → **Create a New Page**
3. Page name: "ClawAgents" (or whatever brand you want on the ads)
4. Category: "Consulting Agency" or "Technology Company"
5. Add a profile photo and cover image (can be simple, just needs to exist)
6. **Copy your Page ID:**
   - Go to your new Page
   - Click **About** (or **Page Transparency** on newer layouts)
   - Scroll down to find **"Page ID"** — it's a number like `123456789`
   - Save this number

---

## Step 3: Create Ad Account + Add Payment (5 min)

### Create Ad Account

1. In Business Manager → **Settings** → **Accounts** → **Ad Accounts**
2. Click **Add** → **Create a New Ad Account**
3. Name: "ClawAgents Ads" (or anything)
4. Currency: **USD** (or your preferred currency)
5. Timezone: Your timezone
6. Click **Create**

### Add Payment Method

1. In Business Manager → **Billing** → **Payment Settings**
2. Click **Add Payment Method**
3. Add a credit/debit card
4. This is how Facebook charges for ad spend

### Copy Ad Account ID

- Go to **Ad Accounts** in Business Manager settings
- Your Ad Account ID is shown — format: `act_XXXXXXXXXX`
- Or find it in the URL when you're in Ads Manager: `act_XXXXXXXXXX`
- **Include the `act_` prefix** when entering it later
- Save this ID

---

## Step 4: Create Developer App (5 min)

This connects the ad-engine script to your ad account.

### Create the App

1. Go to **https://developers.facebook.com**
2. Log in with the same Facebook account
3. Click **My Apps** (top right) → **Create App**
4. Use case: select **"Other"**
5. App type: select **"Business"**
6. App name: "AdEngine" (or anything)
7. Connect it to your Business Manager account when prompted
8. Click **Create App**

### Enable Marketing API

1. In your App Dashboard → left sidebar → **Add Products**
2. Find **"Marketing API"**
3. Click **Set Up**
4. This enables your app to create and manage ads

### Note Your App Credentials

1. In App Dashboard → **Settings** → **Basic**
2. Copy your **App ID** (a number)
3. Copy your **App Secret** (click "Show" to reveal)
4. Save both — you'll need them to extend your token

---

## Step 5: Generate Access Token (5 min)

### Get a Short-Lived Token

1. Go to **https://developers.facebook.com/tools/explorer/**
2. In the top-right dropdown, select your app ("AdEngine")
3. Click **"Generate Access Token"**
4. A permissions dialog appears — check these boxes:
   - `ads_management`
   - `ads_read`
   - `pages_read_engagement`
   - `pages_manage_ads`
5. Click **Generate Access Token**
6. Log in and authorize when prompted
7. Copy the token that appears (starts with `EAA...`)

**This token expires in ~1 hour.** You need to extend it.

### Extend to Long-Lived Token (lasts ~60 days)

**Option A — Via Facebook's Debug Tool:**

1. Go to **https://developers.facebook.com/tools/debug/accesstoken/**
2. Paste your short-lived token
3. Click **Debug**
4. At the bottom of the page, click **"Extend Access Token"**
5. Copy the new long-lived token
6. This token lasts ~60 days

**Option B — Via URL (if Option A doesn't show the extend button):**

Open this URL in your browser (replace the 3 values):

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
```

- `YOUR_APP_ID` — from Step 4 (App Dashboard → Settings → Basic)
- `YOUR_APP_SECRET` — from Step 4 (App Dashboard → Settings → Basic)
- `YOUR_SHORT_LIVED_TOKEN` — the token you just generated

The response will be JSON with your long-lived `access_token`. Copy it.

### Verify Your Token

1. Go to **https://developers.facebook.com/tools/debug/accesstoken/**
2. Paste the long-lived token
3. Click **Debug**
4. Verify:
   - **Expires:** should say ~60 days from now
   - **Scopes:** should include `ads_management`, `ads_read`
   - **App:** should show your app name

---

## Step 6: Run Setup on Server

SSH into the Contabo server and run:

```bash
python3 ~/.openclaw/workspace/skills/ad-engine/scripts/fb_deploy.py --setup
```

It will prompt for:
```
Access Token: [paste your long-lived token]
Ad Account ID (act_XXX): [paste act_XXXXXXXXXX]
Page ID: [paste your page ID number]
```

The script validates against the Facebook API and saves credentials to `~/.config/ad-engine/fb_config.json`.

---

## Step 7: Deploy Your First Ads

```bash
# Deploy Security Audit ad (DM "AUDIT")
python3 ~/.openclaw/workspace/skills/ad-engine/scripts/fb_deploy.py --deploy \
  --message-id 8556 \
  --image /tmp/2026-02-17-security-audit-ad.png \
  --landing-url "https://m.me/YOUR_PAGE_USERNAME" \
  --objective messages

# Deploy Setup Checklist ad (DM "SETUP")
python3 ~/.openclaw/workspace/skills/ad-engine/scripts/fb_deploy.py --deploy \
  --message-id 8558 \
  --image /tmp/2026-02-17-setup-checklist-ad.png \
  --landing-url "https://m.me/YOUR_PAGE_USERNAME" \
  --objective messages
```

Replace `YOUR_PAGE_USERNAME` with your Facebook Page username (the part after facebook.com/).

Both ads deploy PAUSED by default — review in Ads Manager, then unpause when ready.

---

## Token Renewal (Every 60 Days)

Long-lived tokens expire after ~60 days. To renew:

1. Go to Graph API Explorer → generate new short-lived token
2. Extend it using the debug tool or URL method above
3. Run `--setup` again with the new token

**Pro tip:** Set a calendar reminder for 55 days from now to renew before it expires.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Invalid OAuth access token" | Token expired — regenerate and run `--setup` |
| "User does not have permission" | Check that your token has `ads_management` scope |
| "Ad account is disabled" | Check payment method in Business Manager |
| "Page not found" | Make sure Page ID is correct and your app has `pages_manage_ads` |
| "The ad account is not enabled for this application" | In Business Manager → Settings → Apps → add your developer app |

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Business Manager | https://business.facebook.com |
| Developer Portal | https://developers.facebook.com |
| Graph API Explorer | https://developers.facebook.com/tools/explorer/ |
| Access Token Debugger | https://developers.facebook.com/tools/debug/accesstoken/ |
| Ads Manager | https://www.facebook.com/adsmanager |
| Marketing API Docs | https://developers.facebook.com/docs/marketing-apis |
