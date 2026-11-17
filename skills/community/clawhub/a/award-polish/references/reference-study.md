# Studying award-winning sites: how to look, what to note

## Where to look

- Awwwards: Sites of the Day (SOTD), Sites of the Month (SOTM), Developer Award. Filter by a category close to the product (Mobile & Apps, Business & Corporate, E-commerce, Education, etc.).
- Webby Awards: winners or nominees of the last two years in the Websites and Mobile Sites categories.
- FWA: FWA of the Day / of the Month.

Prefer sites from **the last year or two** that are **products, apps or services**; pick few pure art showcases, whose techniques rarely transfer to products.
6-8 sites are enough, at least 2 with a mobile experience to look at. For tools and back offices: 4-6 award sites plus 3 back-office UIs.
The SOTD list does not show categories; filter with Awwwards Categories or open the detail page for tags.

## For tools and back-office products

Award sites are mostly marketing pages, with few back-office or tool UIs to look at. When the product is a back office, dashboard or developer tool:

- Still study award sites; they remain the quality ruler: home pages, marketing pages, and the well-made interactions and motion on them.
- Add 3 **widely praised product UIs** as references, e.g. the Linear, Vercel or Stripe dashboards. They all need a login; **do not sign up or log in**: use screenshots from official docs, product pages and changelogs, or real-app screenshot libraries like Mobbin, and note the source.
- Look instead at: how one screen ranks information, how tables and lists are laid out, how status and progress show, how empty states and errors are written, what long tasks show while waiting.
- Same note format, with "widely praised product UI" in the award slot. The ruler does not change: 10 is still Awwwards award level.

## How to look at each site

Actually open it; thumbnails are not enough. With browser automation: dismiss the cookie banner first (necessary cookies only) or it blocks screenshots; take scrolling screenshots with `scripts/layout_check.py --slices`, record motion with `scripts/record_moment.py`, or watch the video on the Awwwards detail page. Hovers and clicks on other people's sites often time out; if a recording fails, do not force it, note "not captured".

1. Stay on the first screen for 3 seconds: what you notice first, how many heading lines, where the main button is.
2. Scroll slowly: how sections transition, the whitespace rhythm, any scroll storytelling.
3. Click a few things: button press, hover, page change, expand and collapse; how fast the feedback is and how the motion feels.
4. Look again at phone width (emulate 375px).

## What to note (the "reference notes" in the log)

One short entry per site:

```
### <site> (<award> · <year> · <link>)
- What is good: <specific techniques, e.g. "2-line heading with a single button below; sections about 160px apart, images scale and fade in on scroll">
- Worth borrowing: <one or two, saying which of our pages and moments>
- Screenshot: refs/<site>-<screen>.png
- Jury score: if the Awwwards site page (awwwards.com/sites/<site>) shows SOTD scores, record design / usability / creativity / content and the total. The score is the x.xx/10 after "SCORE"; the 40% / 30% / 20% / 10% next to it are weights. This is the real bar we chase (Honorable Mention needs 6.5+, SOTD weighted usually 7.2-7.7).
```

For "what is good", pick the strongest of these 8 dimensions, not all of them: typography, whitespace, hierarchy, color, motion, micro-interactions, responsive, originality.

## Find the gaps

For new sites there is nothing to compare yet; do this step once the first version exists.

After the notes, put screenshots of our home and core pages next to them, write one line of "where we fall short" per dimension, sort the gaps into a to-do list, biggest first, and put it in the log. Every batch works from that list.

## Notes

- Borrow techniques only; never copy layouts, colors, copy or assets.
- Award sites are the quality bar. A borrowed technique must serve ease of use, looks, smoothness or wanting to return; otherwise skip it.
- refs/ stays local, in .gitignore, never committed (other people's screenshots do not belong in a public repo).
