# Phase 1: Discovery & Design Inspiration

## Table of Contents
1. [Discovery Questions](#discovery-questions)
2. [Finding Design Inspiration](#finding-design-inspiration)
3. [Brand Identity Collection](#brand-identity-collection)
4. [RTL vs LTR Decision](#rtl-vs-ltr-decision)

---

## Discovery Questions

Ask these one at a time. Wait for the answer before asking the next one.

### Round 1: Purpose
- "מה מטרת האתר? / What is the main purpose of the site?"
  - Portfolio (show your work)
  - Business landing page (get clients / sell services)
  - Blog / content site (share articles)
  - Personal brand (mix of all above)
  - E-commerce (sell products)

### Round 2: Audience
- "מי יגיע לאתר? / Who will visit this site?"
  - Potential employers / clients
  - General public
  - Existing customers
  - Both Hebrew and international visitors?

### Round 3: Content
- "מה אתה רוצה שיראו? / What do you want visitors to see or do?"
  - See your work/portfolio
  - Contact you
  - Read your writing
  - Buy something
  - Learn about your business

### Round 4: Timeline
- "האם יש deadline? / Do you have a launch deadline?"
  - This helps prioritize what to build first vs later.

---

## Finding Design Inspiration

This is THE most important step. Without a visual reference, the agent has to guess what you want — and usually gets it wrong.

### How to Find Inspiration (Guide the User)

Tell them:
> "לפני שנתחיל לכתוב קוד, בואו נמצא דוגמאות של אתרים שאתה אוהב את המראה שלהם. זה יחסוך לנו הרבה זמן."
> ("Before we write any code, let's find examples of websites whose design you love. This will save us a lot of time.")

**Send them to these resources:**

1. **Awwwards** — `https://www.awwwards.com` — Award-winning web design. Filter by category (portfolio, agency, etc.)

2. **Dribbble** — `https://dribbble.com` — UI/UX designs. Search "portfolio website" or "agency landing page"

3. **Behance** — `https://behance.net` — Designer portfolios. Great for seeing real finished sites.

4. **Lapa Ninja** — `https://lapa.ninja` — Landing page inspiration specifically.

5. **Land-book** — `https://land-book.com` — Curated landing page gallery.

6. **One Page Love** — `https://onepagelove.com` — If they want a single-page site.

**Instructions to give the user:**
> "תסתכל על כמה מהאתרים האלה ושלח לי 2-3 קישורים לאתרים שאתה אוהב את המראה שלהם — לא חייב שהם יעסקו באותו תחום שלך. רק המראה והתחושה."
> ("Look at a few of these sites and send me 2-3 links to websites whose look you love — they don't need to be in your industry. Just the look and feel.")

### Analyzing the References

Once they share links, study them and extract:
1. **Color palette** — What colors dominate? Dark/light? Accent colors?
2. **Typography** — Big bold headlines? Clean minimalist text?
3. **Layout** — Full-width sections? Cards? Asymmetric?
4. **Animation** — Subtle fade-ins? Bold transitions? None?
5. **Mood** — Professional/corporate? Creative/playful? Minimal/clean? Bold/loud?

Summarize back to them:
> "מהאתרים ששלחת, אני רואה שאתה נמשך למראה כהה עם הדגשות בצבע כתום, עם טיפוגרפיה גדולה ונועזת. זה נכון? האם יש עוד משהו שרצית לשלב?"
> ("From the sites you shared, I can see you're drawn to a dark look with orange accents and bold typography. Is that right? Is there anything else you'd like to combine?")

---

## Brand Identity Collection

Collect these before building anything:

### Required
- [ ] Site name / your name
- [ ] Main color (even just "I like blue" is enough to start)
- [ ] Logo (if they have one — PNG with transparent background preferred)
- [ ] Tagline or one-sentence description

### Nice to Have
- [ ] Secondary color / accent color
- [ ] Font preference (if any — e.g., "I like clean and modern" or "I want something elegant")
- [ ] Social media links (LinkedIn, Instagram, GitHub, etc.)
- [ ] Email / contact info to show

### Content
- [ ] Headings / section titles
- [ ] About text (even a draft)
- [ ] Work samples / project descriptions (for portfolio)
- [ ] Photo or avatar (for personal sites)

If they don't have content yet, that's fine:
> "אין בעיה אם אין לך את כל התוכן עכשיו. נוכל לשים תוכן זמני ('placeholder') ולהחליף אותו אחר כך."
> ("No problem if you don't have all the content yet. We can use placeholder text and swap it out later.")

---

## RTL vs LTR Decision

**ALWAYS ask explicitly.** Never assume.

> "האם האתר יהיה בעברית (מימין לשמאל) או באנגלית (משמאל לימין) — או שניהם?"
> ("Will the site be in Hebrew (right-to-left) or English (left-to-right) — or both?")

### Technical Implications
- **Hebrew only (RTL):** Add `dir="rtl"` to `<html>` tag, use `font-family` that supports Hebrew (Heebo, Assistant, Rubik are free on Google Fonts)
- **English only (LTR):** Standard setup, no special handling
- **Bilingual:** Add language toggle, use `next-i18n` or manual route-based switching
- **Default:** If unsure, build in English first, add Hebrew as second step

### Recommended Hebrew Fonts (Google Fonts — free)
- **Heebo** — Clean, modern, great for professional sites
- **Assistant** — Slightly rounder, friendly feel
- **Rubik** — Bold headlines, very readable
- **Frank Ruhl Libre** — Classic/editorial look
