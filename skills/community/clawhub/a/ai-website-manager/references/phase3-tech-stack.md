# Phase 3: Tech Stack Decision Guide

This reference helps you recommend the right technology stack based on what the user wants to build.
Always explain the choice in plain language before building anything.

## Table of Contents
1. [Stack Decision Matrix](#stack-decision-matrix)
2. [Recommended Stack: Next.js + Sanity + Vercel](#recommended-stack-nextjs--sanity--vercel)
3. [Project Initialization](#project-initialization)
4. [Folder Structure](#folder-structure)
5. [Styling Conventions](#styling-conventions)
6. [Deployment Flow](#deployment-flow)

---

## Stack Decision Matrix

| Site Type | Recommended Stack | Reason |
|-----------|------------------|--------|
| Portfolio / Personal Brand | Next.js + Sanity + Vercel | Fast, beautiful, easy to update content |
| Business Landing Page | Next.js + Vercel (no CMS needed yet) | Simple, fast to build, easy to add CMS later |
| Blog-heavy site | WordPress + Next.js frontend (optional) | WordPress is built for blogging |
| E-commerce | Next.js + Stripe + Sanity + Vercel | Full control over design and checkout |
| Simple one-pager | Next.js + Vercel | Overkill to add a CMS for 1 page |
| Multi-language (HE+EN) | Next.js + Sanity + Vercel + `next-intl` | i18n support built-in |

### When to Skip Sanity
- The site has fewer than 5 pieces of changeable content
- The user will never update the site themselves
- It's a quick prototype or MVP

### When to Add WordPress
- The user wants to run a blog with many articles
- They're already familiar with WordPress
- SEO and content scheduling are top priorities

---

## Recommended Stack: Next.js + Sanity + Vercel

This is the gold standard for personal and business sites. Here's how to explain it to a non-technical user:

> "הנה איך זה עובד:
> - **Next.js** הוא המנוע — הוא בונה ומנהל את האתר שלך.
> - **Sanity** הוא עורך התוכן — שם תוכל לשנות טקסטים ותמונות בלי לגעת בקוד, כמו Google Docs.
> - **Vercel** הוא מי שמפרסם הכל לאינטרנט — בחינם.
> - **GitHub** הוא הגיבוי — שם כל הקוד נשמר בבטחה.
> יחד, הם אחד השילובים הכי פופולריים בעולם לאתרים מקצועיים."

---

## Project Initialization

### Step 1: Create the Next.js App
```bash
npx create-next-app@latest my-website --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

Flags explained (for the user):
- `--typescript` — TypeScript (safer code, better autocomplete)
- `--tailwind` — Tailwind CSS (easy styling)
- `--app` — uses the modern App Router
- `--src-dir` — puts code in `/src` folder (cleaner structure)

### Step 2: Add Sanity
```bash
cd my-website
npx sanity@latest init --env
```

During setup:
- Choose **"Create new project"** or **"Use existing project"** (if they already created one)
- Dataset: `production`
- Project output path: `src/sanity` (keep it organized)

### Step 3: Install Common Dependencies
```bash
npm install @sanity/image-url framer-motion lucide-react next-themes
```

- `@sanity/image-url` — handles image URLs from Sanity
- `framer-motion` — smooth animations
- `lucide-react` — clean icon library
- `next-themes` — dark/light mode toggle (if needed)

### Step 4: Push to GitHub
```bash
git init
git add .
git commit -m "Initial project setup"
```

Then create a GitHub repo and push:
```bash
gh repo create my-website --public --source=. --remote=origin --push
```

Or manually via `https://github.com/new`, then:
```bash
git remote add origin https://github.com/yourusername/my-website.git
git push -u origin main
```

### Step 5: Deploy to Vercel
```bash
npx vercel
```
Or go to `https://vercel.com/new`, import the GitHub repo, click Deploy.

**First deploy tip:** Even if the site looks empty, deploy early. It gives the user a live URL and proves the pipeline works.

---

## Folder Structure

Standard structure to use and explain to users:

```
my-website/
├── src/
│   ├── app/                    ← Pages and routes
│   │   ├── page.tsx            ← Homepage
│   │   ├── layout.tsx          ← Root layout (navbar, footer, fonts)
│   │   ├── about/page.tsx      ← /about page
│   │   └── studio/[[...tool]]/ ← Sanity Studio (admin panel)
│   ├── components/             ← Reusable UI pieces
│   │   ├── Navbar.tsx
│   │   ├── HeroSection.tsx
│   │   ├── Footer.tsx
│   │   └── ...
│   ├── sanity/
│   │   ├── schemas/            ← Content types (what can be edited)
│   │   ├── lib/
│   │   │   ├── client.ts       ← Sanity connection
│   │   │   └── queries.ts      ← Data fetching queries
│   │   └── schemaTypes.ts
│   └── lib/
│       └── utils.ts            ← Helper functions
├── public/                     ← Images, fonts, icons
├── .env.local                  ← API keys (never committed)
├── .gitignore
├── next.config.ts
├── tailwind.config.ts
└── package.json
```

Explain to the user:
> "תחשוב על זה ככה: `app/` הוא איפה הדפים נמצאים, `components/` הוא חלקים שמופיעים בהרבה מקומות (כמו ניווט ו-footer), ו-`sanity/` הוא החיבור לעורך התוכן שלך."

---

## Styling Conventions

### Tailwind CSS
Always use Tailwind utility classes. Avoid writing custom CSS unless absolutely necessary.

```tsx
// Good
<div className="bg-black text-white px-6 py-4 rounded-lg flex items-center gap-4">

// Avoid unless needed
<div style={{ backgroundColor: 'black', color: 'white', padding: '16px' }}>
```

### Color Palette Setup
Add custom brand colors in `tailwind.config.ts`:

```ts
theme: {
  extend: {
    colors: {
      brand: {
        primary: '#YOUR_MAIN_COLOR',    // e.g., orange CTA buttons
        secondary: '#YOUR_ACCENT_COLOR', // e.g., pink/magenta headings
        dark: '#0a0a0a',               // dark background
      }
    }
  }
}
```

### Dark Backgrounds
For dark sites, set global background in `layout.tsx`:
```tsx
<body className="bg-[#0a0a0a] text-white antialiased">
```

### Typography Scale
```tsx
// Hero heading
<h1 className="text-5xl md:text-7xl font-bold leading-tight">

// Section heading
<h2 className="text-3xl md:text-4xl font-semibold">

// Body text
<p className="text-base md:text-lg text-gray-300 leading-relaxed">
```

### Responsive Design
Always mobile-first. Use breakpoints:
- `sm:` = 640px+
- `md:` = 768px+
- `lg:` = 1024px+
- `xl:` = 1280px+

---

## Deployment Flow

### Automatic (Recommended)
Once GitHub is connected to Vercel:
1. Make changes → commit → `git push origin main`
2. Vercel detects the push automatically
3. New version is live within ~30 seconds

### Manual
```bash
vercel --prod
```

### Environment Variables on Vercel
Never put secrets in code. Always use Vercel's environment variables:
1. Vercel Dashboard → Project → Settings → Environment Variables
2. Add each key from `.env.local`
3. Make sure to add for **Production**, **Preview**, and **Development**

### Checking Deployment Status
```bash
vercel ls          # list recent deployments
vercel logs        # view deployment logs
```

Or in Vercel Dashboard under "Deployments" tab.
