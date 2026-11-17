# Polish checklist

## Layout check (every batch)

At 375, 768, 1024, 1280 and 1440, look at every home section and every app page (dialogs, toasts and empty states included):

- One fixed spacing scale (which values for section spacing, block spacing, card padding), used site-wide, no one-off numbers.
- Consistent vertical spacing between headings, body text and buttons.
- Left and right edges on the same lines.
- The first screen neither cramped nor empty; the navigation fits on one line.
- Bottom navigation and floating buttons do not cover content; the last block leaves a safe bottom margin.
- No text overflowing or clipped; button labels do not wrap.
- Images keep their aspect ratio.
- No horizontal scrolling, no big empty strip on one side.

Screenshot with viewport emulation (headless browsers have a minimum window width, so a plain 375px window is inaccurate). The automated part is `layout_check.py`; usage and how to read the report are in `scripts.md`.

## Easy to use

- Count the clicks in the core flow and cut every step you can: remember last choices, defaults, one-click repeat.
- One main action per page; the button label is the action itself.
- Key information sits in the first screen (main result, next-step button); never make users scroll for it. Measure before adding a hint bar or explanation so it does not push them out.
- Whatever looks clickable must be clickable: words that name an action (copy, share, download) and anything shaped like a button respond across their whole block. If only a small part responds, reviewers cap it as "no response on click".
- Copy: see "Copy" below.
- **Broken links get a proper page too**: share and invite links often lose characters in chat apps. Anything that fails to decode, validate or parse shows the same "this page can't be opened" page with a way to continue; never a white screen, never a crash in parameter parsing. Test it by opening the link with 1, 2, 3 and 10 characters cut off and with one character changed in the middle.
- **Enter and the mobile keyboard's "Go"**: Enter in the last field submits when all required fields are filled, otherwise jumps to the empty one.
- **Submitting with empty fields**: the button says what is missing, and the empty fields turn red and shake; changing only the button text is not enough.

## Copy

- Headings say something specific: who this product helps get what done, never "redefine" or "a new era".
- Buttons name the action ("Start test", "Approve fix"), never "OK", "Submit", "Learn more".
- One name per thing across the whole site; keep a glossary in the log.
- Write empty, error and waiting states: empty states say how to start, errors say what happened and what to do next, long waits say what is happening.
- When done, run the whole site through a de-AI rewrite (e.g. humanizer) to remove AI tone, forced lists, dashes and filler.
- For bilingual products, check lengths in both languages: one language often runs longer, and buttons and labels must not burst.

## Good-looking

- One accent color, one radius set, one shadow set, site-wide.
- **Category and status colors stay distinct in every theme**: when adding colors to tell categories apart (article tags, status badges), read the actual background and text colors in both light and dark themes (`getComputedStyle`); every pair of backgrounds must be clearly distinct and text contrast at least 4.5:1. Checking one theme does not count; dark themes easily collapse several dark colors into one.
- **CJK line breaking**: headings, short card lines and text set inside a canvas break only between phrases, never inside a word, and never leave one character alone on the last line. For web text insert `<wbr>` between phrases with BudouX and use `word-break: keep-all; text-wrap: balance`; when setting text in a canvas, break only where both BudouX and the browser's `Intl.Segmenter` agree, preferably after punctuation; short lines that fit stay on one line. Either tool alone, or splitting by character count, breaks words.
- **When removing something reviewers disliked, replace it with something equally substantial**: swap a murky background photo for plain black and the next review says "too dark, no atmosphere". When you remove a layer, fill it with something tied to the brand concept (large soft light following the theme color, the brand's dot texture).
- Icons and illustrations share one style.
- **Prefer generated images**: map bases, illustrations, scenes, decoration, backgrounds, empty states and badges all come from an image generator first, not SVG, CSS shapes or line drawings, which look flat by comparison. SVG or CSS is only for two things: what sits on top of images and moves or follows data (route animations, highlights, progress), and small action icons. Animated pictures are "generated image underneath + SVG animation on top". Before every batch, list every picture that is still drawn, and put them all on the list.
- **Third-party image generators**: reference sketches and prompts leave this machine and are sent to that service. Get the user's authorization before the first send. Do not send secrets or personal data. Do not switch providers silently; stay with the generator the user authorized.
- **Routes, markers and labels on images: fix the layout before generating**: in a generated image, roads and buildings land anywhere; generate first and guess later, and overlays will never line up. Do it this way:
  1. Sketch the layout with simple lines and boxes: road network, key places, routes.
  2. Feed the sketch to the image generator as a reference, keeping positions and only changing it to an illustrated or photographic look. Only send it after the user has authorized that generator, as in "Third-party image generators" above.
  3. After generating, place overlays by code: detect the road surface (or other carrying area) by color, run routes along real roads, put markers on routes and labels next to their places. Position overlays from layout sizes (offsetLeft, offsetTop, clientWidth and the like), not getBoundingClientRect, which includes transforms, so annotations drift while images slide in or scale on hover. Measure only after images load and entrance animations end.
  4. Accept by the numbers, every item with a value (checking only "on the road" is not enough; one clickable prototype failed exactly there):
     - At least 95% of route sample points on the road surface.
     - Endpoints connect: route start to the start place's door, end to the end place's door, waypoints to both route segments, all within 8px.
     - No gaps: adjacent sample points at most 10px apart.
     - Start, end and waypoints fully inside the frame, not clipped.
     - The base image fills the frame with no blank edges or white borders.
     - Overlays and labels do not cover the route, start, end or waypoints.
     - With animation: accept the final frame after it ends, plus 2 shots mid-animation, none of which may look broken.
     - Places sit on the right things: each place's dot inside its object or within 8px of its door, never on water, lawns or empty ground; types match (each kind of place on something that looks like that kind).
     - Routes do not cut through: 0% of route pixels on water, roofs or lawns. Find the route by code on the road area (e.g. A*), and compute distance and "how many extra minutes" from that real path, not a straight line.
     - When the camera zooms, rotates or pans, no frame ever shows the base image's edge or white borders (limit the camera, or generate the base larger than the frame).
     - Every image size passes; look again at 2x zoom. Redraw or adjust anything that fails.
  5. **A demo only needs to read at a glance**: several images on one page may look different and need not form one world or be engineering-accurate. Sketch each image for the one thing it explains, with as few elements as possible. The only non-negotiables are "readable" and "no common-sense errors" (places not in water, routes not through buildings or lakes, both ends connected, no white edges). Accept with the "3-second test": give the screenshot to a fresh small reviewer who sees only that image and must say who goes from where to where, where the key points are and why, and find nothing wrong; the numeric checks above only catch obvious errors.
  6. **Every instance passes**: a page often has several such images (first-screen map, intro map, small maps in lists, detail map, route thumbnails on cards); build and check each one this way, not just the one that was pointed out.
  Put this check in every batch's self-check instead of waiting for reviewers. Reviewers usually only see the symptom ("misaligned") and not the cause ("generated first, positions guessed later"), so the developer keeps nudging coordinates by hand.
- **Icons that carry meaning are pictures too**: rule categories, statuses (pending, done, complaint, privacy), badges, urgent markers, empty states, bottom navigation and celebrations are generated as a set (one style, one size, transparent background) matching existing generated icons. Only **action symbols** keep an SVG icon library: back, close, check, dropdown, plus/minus, stars, arrows, search, refresh.
- **Exception for dense interfaces like back offices and tables**: status tags (passed, failed, needs fix) and small table icons use text with colored pills or an icon library, not bitmaps, for clarity at small sizes. Generated images are for illustrations, empty states and large pictures.
- **How to take stock**: before every batch, search the code for `<svg`, icon library imports (e.g. `@phosphor-icons/react`), CSS gradients and drawn decorations; decide for each whether it is "action symbol / animated overlay" or "picture", and put every picture on this batch's list.
- Image order: use the image generator the user authorized. When it is out of quota, ask before using another generator (ChatGPT, Gemini, or Grok in a browser). Do not switch providers silently. Image replacement rules are in the SKILL.md red lines.
- Tabular numerals for numbers, so amounts and scores line up.

## Smooth

- No white flash or jump between pages; skeletons shaped like the real content.
- Presses give tactile feedback (slight scale or press-down); toasts do not stack, do not cover content, and disappear on time.
- Motion follows "Motion standards" below.
- **No ghosting between screens**: cross-fading old and new screens at half opacity at the same time muddles both screens' text. Fade the leaving screen out fast (100-150ms) and fade the new one in after 100ms (separate transitions for leaving and entering states in CSS).
- Guard against white screens from stale caches after deploys (reload on load failure, keep the previous bundle files).

## Motion standards (set at kickoff, in the log, used site-wide)

Award sites move well because of one consistent rhythm. Set these values at kickoff:

- **Three duration tiers**: small feedback like press and hover 120-180ms; card expansion, dialogs, toasts 200-300ms; page changes and large content entering 300-450ms. Anything over 500ms is reserved for signature moments and must not block the next action.
- **Easing**: ease-out for entering, ease-in for leaving, spring for direct manipulation like dragging and swiping. Two or three curves site-wide, as variables.
- **Stagger**: when a group enters together, 30-60ms apart, at most 500ms in total.
- **Animate only transform and opacity**: not size, position or margins, which stutter.
- **Connect the same thing across pages**: when a list card opens into a detail page, let it grow from its place instead of vanishing and reappearing. With View Transitions, name only the clicked element and its target: naming every card in the list turns every card on screen into a separate layer fading at the browser's default duration, and they ghost.
- **reduced-motion**: when the system asks for reduced motion, replace movement and scaling with fades and stop looping animations.
- **How to verify**: record each signature moment frame by frame on a virtual clock with `scripts/record_moment.py` (`--every 40`, `"frames": 800` on the step to record). Check that durations and easing in `animations.json` fall into the tiers above, how long the picture moves in `motion.json`, and flip through the frames for jumps, breaks or flashes. The script drives time, so a busy machine does not change the result.

## Detail checklist (before the first review and before every release)

Finishing details jurors and users notice, pass/fail only:

- Every page's title (the browser tab text) is that page's own name.
- Share card: pasting the link into a chat app shows a title, a one-line description and a purpose-made preview image (1200x630). Blank or random screenshots do not count.
- Favicon and home-screen icon are your own.
- 404 and error pages follow the site's style and offer a way back home.
- On desktop every clickable thing has a hover state and a pointer cursor; text selection color and scrollbars match the site.
- Going back returns to the scroll position you left; refresh stays on the current page instead of jumping home.
- External links open in a new tab; no placeholder text on any page (Lorem ipsum, TODO, test data).
- **After editing shared fragments, search the whole site for the old text**: footers, headers and navigation appear on every page, and template-generated pages and hand-written pages are often mixed, while the generator only updates the former. Rerun the generator, confirm the rerun changes nothing else, then grep for the old text and fix the remaining pages by hand.
- Run the core flow once in Chrome and once in Safari (Safari often differs on blur, filters and sticky positioning); turn motion all the way up and check for dropped frames on an ordinary laptop.

## Performance and accessibility (pass/fail; every 3 batches, when images, fonts or loading change, and before every release)

Test on a local production build (dev mode numbers do not count), phones on a throttled network. Run this pinned Lighthouse from the command line and save the JSON for the log. Do not drop the version.

```
npx lighthouse@13.6.0 SITE_URL --only-categories=performance,accessibility --output=json --output-path=lh-mobile.json --chrome-flags="--headless"
npx lighthouse@13.6.0 SITE_URL --preset=desktop --only-categories=performance,accessibility --output=json --output-path=lh-desktop.json --chrome-flags="--headless"
```

- **Lighthouse**: performance at least 90 on desktop and 80 on mobile; accessibility at least 90. When below-the-fold styles load late, online speed tools sometimes check accessibility before the styles arrive and the same version scores differently: test each page 3 times and only count issues reported every time.
- **First screen speed**: Largest Contentful Paint (LCP) at most 2.5 s.
- **No jumping**: Cumulative Layout Shift (CLS) under 0.1. Fix aspect ratios for images and videos; text must not jump while fonts load.
- **Images**: WebP or AVIF at display size; single first-screen images around 300KB at most; lazy-load below the fold. Generated images are often huge; always compress before release.
- **Fonts**: subset CJK fonts to the characters used, or use system fonts; preload key fonts.
- **Keyboard**: Tab and Enter alone complete the core flow, focus rings are visible, dialogs close with Esc.
- **Other**: images have alt text; buttons and links have readable names; text contrast meets WCAG AA.

Record a number for each; failures go on this batch's list.

## Worth coming back

- Progress: how far an order or task has got.
- Growth: progress bars for levels, points or trust, and how far to the next level.
- Achievement: a small, restrained celebration when done.
- Recap: income or results summarized by month and year.
- Shortcuts: one-click repeat of common tasks.
- **The shared page gets a signature moment too** (campaigns, generators): when someone opens a share link, replay the generation animation on the phone page (while waiting, the result glows faintly in the dark so it does not look unloaded, about 2 s), with a replay button below.
- **Saving as a short video**: record the signature moment's canvas with `canvas.captureStream()` and `MediaRecorder`, with sound via `MediaStreamDestination`; record mp4 when the browser supports it, otherwise webm; recording does not work on pages opened as local files, so the button is disabled there.
- **Long share image with a QR code**: some social platforms do not make links clickable. "Share with friends" builds a long image: the result, an invitation line and a QR code for this page; on phones send the image directly with `navigator.share({files})`, otherwise save the image and copy the link. Decode the QR code in the image (OpenCV or similar) to confirm it points at this page.

## Signature moments

Pick 4-6 of the most important beats in the core flow, write them in the log and polish each:

- The first look at the first screen
- The moment the core action completes (order, submit, confirm)
- The result reveal (code, result, match)
- Value moving (money, points, trust changing), with visible number rolls and state changes
- Transitions between pages

The bar is feeling solid, satisfying and wanting to click again. Motion added only to look fancy does not meet it.

## Check states after interactions too (what a person spotted at a glance when a clickable prototype wrapped up)

- Screenshots of static pages with the initial demo data are not enough. Walk the guided tour fully as both roles and **screenshot after every action**; capture every business state (pending, in progress, awaiting confirmation, done, cancelled) in both list and detail; highlights, selections, expansions, dialogs, toasts and empty states all count.
- Automated checks also look for **clipped outlines and shadows** (`clipped` in `layout_check.py`), including icons poking out of their pill or tag.
- Keep similar elements consistent: type and status tags on one card use the same pill style; subtitles do not repeat what the title already says.

## Demo guides point at what to click (settled after people walked a clickable prototype themselves)

- For prototypes shown to reviewers or demo audiences, a guide cannot be just a line of text. Every step highlights the element to press (glowing outline or ring plus an arrow bubble "Click here: Publish") and scrolls to it if it is off screen; steps like switching roles, filling in a field or submitting a rating highlight the control the same way, with the value to enter in the bubble.
- Ask before guiding: on first visit a small dialog asks whether they want a guide ("Walk me through" / "I'll look around"); start only on yes and stay quiet on no; remember the choice and keep a "guide" entry to restart any time. Never force the guide on arrival.
- Acceptance: a fresh subagent told only "follow the on-screen hints to the end", with nothing else, once on phone and once on desktop. Getting stuck or not knowing what to click fails.
- Log the guide frame by frame: for 2.5 s after each click, record the guide bar's text, step number and highlighted target every 0.1 s. Screenshots only catch the settled state and miss flashes like "the new target has not appeared and the bar still shows the previous step" or "the ring circles the old button before jumping", which users see at every step.
- When the project's verification notes include a feature map, state the preconditions for anything that only appears in some state (e.g. "the reminder toggle is only in the wrap-up card after finishing an order, not on the profile page"); a bare URL sends whoever follows it to the wrong place.

## Phone and desktop versions (for demo prototypes)

- One product, one set of data, a phone interface and a desktop interface; do not split it into two apps, and do not fake it with "two phones side by side".
- Let viewers choose: two cards at the entrance (each with a preview image and a line), and a switch at the top inside that keeps the data and current page; each interface has its own shareable URL. Default by device, but any device can switch.
- The desktop version truly uses a desktop layout (left navigation, list in the middle, details on the right). A scaled-up phone interface is not a desktop version. When someone picks desktop on a phone, it must still be readable, or suggest "looks better on a computer".

## Scaled canvases (booth screens, demo frames, fixed-size canvases)

Screens designed at a fixed size and scaled as a whole (say a 1080x1920 booth screen inside a desktop demo frame or opened directly on a phone) shrink their CSS font sizes and buttons on screen, and reviewers on phones and laptops deduct responsive, typography and usability right away.
- **On phones, set the logical width from the screen ratio**: on tall phones narrow the logical width to about 900 (height still filling), so the same text and buttons are about 20% larger; tablets and the real device keep the original size.
- **Accept by rendered size**: smallest text at least 12px, body at least 14px, visible size of anything clickable at least 44px (on a shrunk canvas, enlarging hit areas with transparent pseudo-elements does not count; people cannot find the button). `smallText`, `smallTargets` and `smallVisible` from `layout_check.py` already account for scaling, and on these canvases `smallVisible` entries fail too.
- **Make the screen as large as possible in a desktop demo frame**: frame decoration (top, bezel, stand) as thin as possible, the screen large enough at 1440x900 and 1280x720; when the window is short, decide for each side panel whether it fits and fold only the one that does not.
- **On phones, drop what phones cannot use**: a "scan to join the queue" QR code on a booth screen cannot scan itself on a phone, so leave it out there; booth rules like countdowns stop when the demo runs on a phone.

## Generated assets in bulk

- When they come back, first lay them next to existing assets to check the style matches, then **put them into the real layout** (posters, cards, backgrounds behind text): a thumbnail may look fine while a low composition collides with the text area, or it may be fine because a text panel covers that part.
- When a generator caps how many images one run makes, batch by that cap and check the returned set against the list.
- **Images match their names**: each image shows exactly what the text next to it names. A cheeseburger cannot be illustrated with a chicken wrap, and an article about pour-over coffee needs a pour-over kettle in its header; reviewers deduct for "not real" when a generic image stands in. Spell out the item's look in the prompt (shape, ingredients, what to avoid), and check every returned image against its name. When the library only has generic images, make specific ones and update the image rules so they get used.
