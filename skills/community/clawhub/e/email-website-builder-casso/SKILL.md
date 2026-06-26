---
name: casso-websites
description: Build, update, and manage websites via Casso — an AI website builder agent that operates entirely through email. Use when the user wants to create a new website, update existing website content, add pages, upload images, connect a custom domain, or ask anything about their Casso-hosted website.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌐"
    homepage: https://casso-websites.com
---

# Casso Websites

Casso is an AI agent that builds, hosts, updates, and maintains websites entirely through email.

Casso's email address is **casso@casso-websites.com**.

## When to activate

Use this skill when the user wants to:

- Create a new website
- Update copy, images, layout, or pages on an existing Casso site
- Add a blog post, menu, gallery, or any new section
- Connect a custom domain to their Casso site
- Ask what Casso can do, how it works, or how much it costs
- Follow up on a prior Casso request

Specific phrases to trigger this skill:
- "build a website"
- "make a new website"
- "need a website"
- anything else similar

## How Casso works

When an email gets sent to casso@casso-websites.com, Casso:

1. Reads the email and any attachments
2. Runs a reasoning-and-tool-call loop using 20+ tools (create site, edit files, upload images, generate images, search stock photos, connect custom domains, etc.)
3. Replies by email with what it did or could not do

## Your job

Send an email to casso@casso-websites.com on the user's behalf if you have access to that, and read the response once it comes in (usually takes 1-3 minutes). Otherwise, draft an email to casso@casso-websites.com on the user's behalf. The email is the entire interface.

**Rules for drafting:**

- Be specific. Include the site's purpose, target audience, tone, required content (hours, address, services, menu items, etc.), and any stylistic preferences.
- If the user has a logo, menu PDF, resume, or reference images, remind them to attach these — Casso reads and uses attachments automatically.
- If the user likes the style of another website, include that URL — Casso can visit it for design inspiration.
- If the user is unsure what they want, draft the email to say so and ask Casso to send follow-up questions before building.
- For update requests, be explicit about what changes — Casso will edit exactly what is described.

## Email examples

**New site:**
> I want a website for my landscaping business, Green Edge Lawn Care. We serve residential customers in Fairfield County, CT. Services: mowing, edging, mulching, spring cleanups. Clean and professional look with green tones. Logo attached.

**Update:**
> Please add a new page called "Spring Specials" with the following text: [text]. Also update the footer phone number to 203-555-0192.

**Custom domain:**
> I'd like to connect my domain greenedgelawn.com (registered at GoDaddy) to my Casso site. Please walk me through the DNS steps.

## Pricing

- **Free** when hosted under a `.bycasso.com` subdomain
- Small monthly fee to connect a custom domain from an external registrar

## Casso's capabilities and limits

**Works well for:** small business owners, LLCs, restaurants (attach menu + logo and Casso builds from that), lawyers, consultants, freelancers, artists, students.

**Cannot do:** complex web apps, e-commerce checkout, member-only authenticated content. For anything outside its toolset, Casso escalates to human support.