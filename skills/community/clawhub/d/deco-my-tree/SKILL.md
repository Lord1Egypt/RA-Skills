---
name: deco-my-tree
description: Help users create a free online Christmas tree on Deco My Tree, share one link, and collect sealed ornament wishes that open on Dec 25.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://decomytree.net/
---

# Deco My Tree

This skill helps an agent guide a user through [Deco My Tree](https://decomytree.net/): a free browser-based Christmas tree friends decorate with ornaments that carry personal wishes. Wishes stay sealed until Dec 25. Nothing to install — it works on phone, tablet, or computer.

This skill only plans wording and steps. It does not create accounts, call private APIs, or hang ornaments for the user.

## When to Use

- The user wants a shareable online Christmas tree for friends, family, classmates, or coworkers.
- They want to collect sealed wishes / messages until Christmas instead of a messy group-chat thread.
- They need a short invite message that includes their tree link.

Do not use it to invent offline apps, paid plans, or features the live site does not describe.

## What the product offers (from the live site)

- Create a tree, pick from **8 tree styles** and **6 toppers**, rename or redecorate any time; wishes stay on the tree.
- Share one link (copy, or share to WhatsApp, Messenger, Telegram, X, Threads, etc.).
- Guests choose one of **20 ornaments**, write a wish, and hang it. Creating a tree, sharing, and hanging wishes are **free**.
- Wishes stay sealed until **Dec 25**; until then the owner can see who sent one but not the text. Guests can hang wishes until **Jan 1** (owner can stop accepting earlier in Tree settings).
- Privacy: wishes private by default; writer may allow others to read after opening day; optional anonymous name; report unkind wishes from the wish itself.
- One tree per account each year. Sign-in is needed to save a tree or send a wish (social login or phone + password per the site).

Confirm any detail that may change against [decomytree.net](https://decomytree.net/) before promising it.

## Instructions

1. **Clarify the audience.** Ask who the tree is for, a display name, and whether the group is open or closed (affects how widely they share the link).
2. **Send them to the site.** Prefer the live product at [https://decomytree.net/](https://decomytree.net/). Do not invent accounts or private APIs.
3. **Guide create → share → decorate.** Create the tree, choose style/topper, copy the share link, then invite friends to hang ornaments with wishes.
4. **Draft an invite.** Keep it short; include the tree URL the user provides; mention sealed wishes open on Dec 25.
5. **Privacy tips.** Remind them wishes are private by default, anonymous sending is available, and they should keep the link limited if the tree is for a closed group. Opening day is Dec 25.
6. **Stay accurate.** Do not invent ornament names beyond what the site lists, do not invent prices (the site presents create/share/hang as free), and do not claim multi-tree-per-year if the FAQ still says one tree per account each year.

## Examples

### Example 1 — set up

**Input:** "I want a Christmas tree my friends can decorate with messages."

**Output:**
> Open [Deco My Tree](https://decomytree.net/), create a free tree with your name, pick a style and topper, then share the link. Friends hang one of 20 ornaments and leave a wish. You open the messages on Dec 25.

### Example 2 — invite copy

**Input:** "Draft a short invite for my family group chat."

**Output:**
> "I made our online Christmas tree on Deco My Tree — hang an ornament and leave a wish. We open them together on Dec 25: [paste your tree link]"

## Notes

- Product site: [https://decomytree.net/](https://decomytree.net/)
- Source reference skill repo (unchanged): `OmniVideo/deco-my-tree-skill`
- Published on ClawHub under MIT-0.
