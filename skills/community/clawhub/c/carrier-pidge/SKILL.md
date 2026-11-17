---
name: carrier-pidge
description: Help users send slow, personal notes with Carrier Pidge — a browser messaging product where a digital carrier pigeon flies the distance with a route and ETA instead of delivering instantly.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://carrierpidge.app/
---

# Carrier Pidge

This skill helps an agent guide a user through [Carrier Pidge](https://carrierpidge.app/): a global messaging product that turns a personal note into a slow digital flight. You write to a confirmed friend; a digital carrier pigeon travels the approximate distance between roosts with a route and ETA you can watch. Waiting is part of the experience — it is intentionally **not** instant messaging.

This skill only plans wording and steps. It does not create accounts, send messages, or call private APIs.

## When to Use

- The user wants a slower, more personal alternative to instant chat.
- They want to write a sealed or timed note (including Christmas-morning style arrivals when the product offers that flow).
- They need help drafting a short letter or an invite link message for friends.

Do not use it to invent live tracking of exact GPS addresses, read receipts, or paid features the live site does not describe.

## What the product offers (from the live site)

- Write to one **confirmed friend**, attach the note to a digital carrier pigeon, and follow its **route and changing ETA** on a map.
- Uses **approximate roost areas**, not exact addresses or background tracking.
- No pressure for instant replies; arrival is meant to earn attention.
- Invite friends via a personal link or username; they send a request and join after you confirm.
- Seasonal flow described on the site: seal a letter, it leaves in time for distance, and can land around Christmas morning with a pigeon for a reply — confirm current seasonal availability on the live page.
- Available in multiple languages; support email listed on the site as support@carrierpidge.app.

Confirm any detail that may change against [carrierpidge.app](https://carrierpidge.app/) before promising it. Do not invent prices.

## Instructions

1. **Clarify intent.** Ask who the note is for, tone (warm, playful, serious), whether it should feel sealed/surprise, and roughly how far apart the friends are (city/region only — never collect exact street addresses).
2. **Send them to the product.** Prefer [https://carrierpidge.app/](https://carrierpidge.app/). Guide: sign in if needed → add/confirm the friend → write the note → release the pigeon → watch the route/ETA.
3. **Draft the note.** Keep it personal and short enough to feel handwritten. Do not put secrets the user would not want delayed or shared. Remind them approximate location is used for distance, not exact home tracking.
4. **Invite copy (optional).** Offer a one-line invite that includes the user's Carrier Pidge link when they provide it.
5. **Boundaries.** Do not automate sending, scrape friend lists, or claim instant delivery. Do not invent map precision finer than "approximate area." Seasonal Christmas landing times should be phrased as what the site currently advertises, not a guarantee you control.

## Examples

### Example 1 — first flight

**Input:** "I want to send my friend overseas a message that isn't instant."

**Output:**
> Open [Carrier Pidge](https://carrierpidge.app/), confirm your friend in your flock, write a short note, and release the pigeon. You'll see a route and ETA based on the approximate distance — the wait is the point.

### Example 2 — invite

**Input:** "Draft an invite for a friend."

**Output:**
> "I use Carrier Pidge for slow letters that fly like a pigeon — join me and I'll send you one: [paste your Carrier Pidge link]"

## Notes

- Product site: [https://carrierpidge.app/](https://carrierpidge.app/)
- Published on ClawHub under MIT-0.
