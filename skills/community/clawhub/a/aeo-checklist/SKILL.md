---
name: aeo-checklist
description: Audit a website for AI search readiness, then create answer, FAQ, and schema drafts for owner review, for any AI agent. Use when a user asks to check or improve how AI search tools read, understand, and quote a website.
---

# AEO Checklist

AEO means Answer Engine Optimization. In simple words, it means making a website easy for AI search tools, like ChatGPT, Gemini, and Perplexity, to read, understand, and quote answers from. It is not only Google search.

This skill does two jobs, in order. First, it audits the site. Then, it creates drafts for the owner to review. It never publishes anything live by itself, and it never guarantees that an AI tool will quote the site. The honest result is: the site is made ready, and its chance of being quoted improves.

Your AI agent is the worker here. The owner is the judge. Nothing goes live until the owner approves the draft.

## When to use this skill

Use it when the user asks to:
- Check a website for AI search readiness
- Make a website easier for AI tools to quote
- Fix missing answers, FAQ, schema, or robots text for AI search
- Prepare a site before launch, or improve an existing site

Do not use it to write fake reviews, fake prices, fake partners, or fake facts. If a fact is not confirmed by the owner, leave it out of the draft and mark it as "Needs owner confirmation".

## What you need first

Ask the user for, or read from the site:
1. The website URL, or the site files if the site is not live yet
2. The business name, what it sells or offers, and where it is based
3. The main questions customers actually ask, if the owner knows them
4. The confirmed facts only: prices, services, hours, location, contact details

If you do not have code access, and you can only read the public site from outside, say so clearly. Mark any check you cannot verify from outside as "Needs code access", not Pass, and not Fail.

## Step 1: Audit first

Check each point below. For each point, give one result: Pass, Missing, or Needs code access. Give short evidence for each result, like a page title, a link, or a line you read. Never give Pass without evidence.

### Audit checks

1. Robots and AI crawlers
   - Read robots.txt, if it exists.
   - Check if AI search crawlers are allowed, blocked, or not mentioned.
   - Note: some owners block AI crawlers on purpose. If the site blocks them, do not tell the owner to unblock them without asking. Report the block, and ask the owner what they want.

2. Rendering and readable content
   - Check if the main content is readable as plain text, without running complex scripts.
   - Check if key answers are hidden behind tabs, popups, or heavy JavaScript that an AI reader may miss.
   - Check if pages load with a clear title and clear headings.

3. Clear answers
   - Check if each main service or product page answers, in plain words, at the top: what it is, who it is for, how much it costs, and how to get it.
   - Check if answers are short and direct, not buried in long paragraphs.
   - Check if numbers, prices, and dates are written in one consistent format across the site.

4. FAQ
   - Check if the site has a real FAQ page, or FAQ sections on service pages.
   - Check if the questions are the ones customers actually ask, not invented questions.
   - Check if each answer is short, direct, and true.

5. Structured data, also called schema
   - Check if the site has schema.org data, for example Organization, LocalBusiness, Product, Service, FAQPage, or Article.
   - Check if the schema matches the visible page content. Schema must never say something the page does not say.
   - If you cannot read the page head or code from outside, mark this as "Needs code access".

6. Titles, descriptions, and headings
   - Check if each page has a unique title and a short description that says what the page is about.
   - Check if headings are in order, one main heading per page, then subheadings in order.

7. Trust and contact facts
   - Check if the business name, location, phone, email, and hours are easy to find, and match across pages.
   - Check if testimonials, if any, are real. Never invent a testimonial. If there are no testimonials, say "Missing", not fake.

8. Plain language
   - Check if the main pages use short, simple sentences that a weak English reader can follow.
   - Note jargon, vague buttons, and unclear calls to action, separately from the score.

## Step 2: Create drafts for owner review

After the audit, create these drafts, only for the points that are Missing. Do not rewrite the whole site. Do not change live pages, files, or settings.

Create each draft as a separate, clearly labelled file or section, with "DRAFT - NOT LIVE - Owner approval needed" at the top.

### Drafts to create

1. Answer blocks draft
   - For each main service or product, write one short answer block: what it is, who it is for, price if confirmed, and how to contact or order.
   - Use only confirmed facts. Mark any unconfirmed fact as "Needs owner confirmation" and leave it blank in the draft, never guess it.

2. FAQ draft
   - Write FAQ questions and answers from the owner's real customer questions, or from the site's existing content.
   - Keep each answer to two or three short sentences, in plain words.
   - Do not invent questions customers never ask, and do not invent answers.

3. Schema draft
   - Write a schema.org JSON draft that matches only the visible, confirmed page content.
   - Include Organization or LocalBusiness, and FAQPage only if a real FAQ exists or is approved in draft form.
   - Add a note: "Check this schema with the site owner before adding it to the live site."

4. Robots draft
   - If robots.txt is missing, write a draft robots.txt that allows normal search crawlers.
   - For AI crawlers, write two options, and ask the owner to choose: allow AI crawlers, or block AI crawlers. Do not choose for the owner.
   - If robots.txt already exists, do not rewrite it. Write only the suggested change, as a separate note, for owner approval.

## Output format

Give the owner this report, in this order:

1. Audit summary
   - List each of the 8 checks, with Pass, Missing, or Needs code access, and short evidence.

2. What is ready
   - List what already passes, in plain words.

3. What is missing
   - List what is missing, in plain words, and why it matters for AI search.

4. Drafts created
   - List each draft by name, what it contains, and what still needs owner confirmation.
   - State clearly: "These drafts are not live. Nothing has been published. Approve a draft first, then it can be added to the site."

5. Next steps for the owner
   - Approve, change, or reject each draft.
   - Tell the agent which drafts to add, and which to leave out.

## Hard rules

- Never give Pass without evidence.
- Never invent prices, services, partners, reviews, or facts.
- Never claim an AI tool will quote the site, rank the site, or send traffic. Say only that the site is made ready and its chance improves.
- Never publish a draft live automatically. Owner approval is required for every draft.
- Never change robots.txt, schema, or live pages without owner approval, especially for AI crawler blocking, which may be a deliberate owner choice.
- If a fact is unconfirmed, mark it "Needs owner confirmation" and leave it out of the final draft text.
- Keep language simple, short, and plain. Avoid jargon, unless the owner asks for technical detail.
