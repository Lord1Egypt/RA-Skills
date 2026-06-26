# Phase 2: Account Setup Guide

Complete step-by-step instructions for setting up every account needed to build and manage a website.
Walk the user through ONE account at a time. Confirm completion before moving to the next.

## Table of Contents
1. [GitHub](#1-github--your-code-storage)
2. [Vercel](#2-vercel--your-website-host)
3. [Sanity](#3-sanity--your-content-editor)
4. [Domain (Optional)](#4-domain-optional)
5. [Collecting API Keys](#5-collecting-api-keys)

---

## 1. GitHub — Your Code Storage

**What it is (explain to user):**
> "GitHub הוא כמו Google Drive אבל לקוד. כל הקוד של האתר שלך יישמר שם — בחינם לעולם. זה גם מה שמחבר אותנו ל-Vercel."
> ("GitHub is like Google Drive but for code. All your site's code will be saved there — free forever. It's also what connects to Vercel.")

**Steps:**
1. Go to `https://github.com`
2. Click **"Sign up"**
3. Enter email, create a password, choose a username
   - Tip: Use your real name if possible (e.g., `yourname` or `yourname-dev`) — GitHub profiles are public
4. Verify your email
5. Choose **"Free"** plan when asked

**Confirmation question:**
> "האם יצרת את חשבון GitHub? מה שם המשתמש שבחרת?"
> ("Did you create your GitHub account? What username did you choose?")

**GitHub CLI (optional but recommended for advanced users):**
If they're comfortable running commands, they can install GitHub CLI:
- Windows: `winget install GitHub.cli` or download from `https://cli.github.com`
- After install: `gh auth login` and follow prompts

---

## 2. Vercel — Your Website Host

**What it is (explain to user):**
> "Vercel הוא מה שמפרסם את האתר שלך לאינטרנט. כשנלחץ 'deploy', תוך 30 שניות האתר שלך יהיה חי בכתובת אינטרנט אמיתית. גם זה חינמי לאתרים אישיים."
> ("Vercel is what publishes your site to the internet. When we click 'deploy', within 30 seconds your site will be live at a real web address. Also free for personal sites.")

**Steps:**
1. Go to `https://vercel.com`
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"** — this links the two accounts automatically
4. Authorize Vercel to access your GitHub
5. You'll land on the Vercel dashboard

**Confirmation question:**
> "האם Vercel מחובר ל-GitHub שלך? האם אתה רואה את לוח הבקרה?"
> ("Is Vercel connected to your GitHub? Can you see the dashboard?")

**Getting Vercel API credentials (for advanced management):**
Only needed if using Claude Code to automate deployments:
1. Go to `https://vercel.com/account/tokens`
2. Click **"Create"**
3. Name it: `claude-website-manager`
4. Set expiry: **No expiration**
5. Copy the token — paste it in the `.env.local` file Claude will create for you

---

## 3. Sanity — Your Content Editor

**What it is (explain to user):**
> "Sanity הוא כמו מערכת ניהול תוכן חכמה — תוכל לשנות טקסטים, תמונות וכותרות באתר שלך בלי לגעת בקוד. כמו Google Docs אבל לאתר שלך."
> ("Sanity is like a smart content management system — you'll be able to change texts, images, and headings on your site without touching code. Like Google Docs but for your website.")

**Steps:**
1. Go to `https://sanity.io`
2. Click **"Start building for free"**
3. Sign up with Google (easiest) or email
4. When asked to create a project, name it: `[your-site-name]-content`
5. Choose **"Blog"** or **"Clean project"** template — Claude will replace it anyway

**Getting Sanity API credentials:**
After creating the project:
1. Go to `https://sanity.io/manage`
2. Click on your project
3. Go to **API** → **Tokens**
4. Click **"Add API token"**
5. Name: `claude-website-manager`
6. Permission: **"Editor"** (can read and write)
7. Copy the token — paste it in `.env.local`

Also note your **Project ID** — it's visible at the top of the manage page (looks like: `abc123de`)

**Confirmation question:**
> "האם יצרת פרויקט ב-Sanity? מה ה-Project ID שלך? (זה נראה כמו: abc123de)"
> ("Did you create a project in Sanity? What's your Project ID? (It looks like: abc123de)")

---

## 4. Domain (Optional)

**What it is (explain to user):**
> "Domain זה הכתובת של האתר שלך — כמו yourname.com. זה לא חובה להתחיל, אבל אם אתה רוצה כתובת מקצועית, זה עולה בסביבות 10-15 דולר לשנה."
> ("A domain is your site's address — like yourname.com. It's not required to start, but if you want a professional address, it costs around $10-15 per year.")

**Recommended registrars:**
- **Namecheap** — `https://namecheap.com` — Affordable, good UI
- **Cloudflare Registrar** — `https://cloudflare.com/products/registrar` — At-cost pricing, no markup
- **Google Domains** (now Squarespace) — Simple but slightly pricier

**Avoid:** GoDaddy (lots of upsells), Wix (locks you in)

**After buying, connect to Vercel:**
1. In Vercel → your project → **Settings → Domains**
2. Click **"Add"** → type your domain
3. Vercel shows you DNS records to add
4. In your registrar's DNS settings, add those records
5. Wait 10-60 minutes for it to propagate

---

## 5. Collecting API Keys

After all accounts are set up, Claude will create a `.env.local` file in the project.
This file stores all your private keys — it NEVER goes to GitHub (it's in `.gitignore`).

**Template to fill in together:**

```env
# Sanity
NEXT_PUBLIC_SANITY_PROJECT_ID=your_project_id_here
NEXT_PUBLIC_SANITY_DATASET=production
SANITY_API_TOKEN=your_sanity_token_here

# GitHub (only needed for automation)
GITHUB_TOKEN=your_github_token_here

# Vercel (only needed for automation)
VERCEL_TOKEN=your_vercel_token_here
VERCEL_TEAM_ID=your_team_id_here
VERCEL_PROJECT_ID=your_project_id_here
```

**Security rules to share with the user:**
- Never share this file with anyone
- Never paste tokens in chat or email
- If you accidentally share a token, go revoke it immediately and create a new one
- Never commit `.env.local` to GitHub

**Checking `.gitignore`:**
Make sure `.env.local` is in the `.gitignore` file. It usually is by default in Next.js projects, but always verify:
```
# Should already be there:
.env.local
.env*.local
```
