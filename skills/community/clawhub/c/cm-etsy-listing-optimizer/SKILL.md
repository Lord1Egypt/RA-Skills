---
name: cm-etsy-listing-optimizer
description: Audit and optimize Etsy listings for SEO, conversion, and shop placement. Reviews titles, tags, descriptions, photos, attributes, pricing, and shipping to improve search rank and sales for handmade, print-on-demand, and digital download sellers. Use when asked to optimize an Etsy listing, audit an Etsy shop, fix Etsy SEO, write Etsy titles or tags, improve Etsy conversion, set up Etsy ads, or grow an Etsy store. Triggers on "Etsy SEO", "Etsy listing", "Etsy tags", "Etsy title", "Etsy shop audit", "Etsy ads", "Star Seller", "print on demand Etsy", "digital download Etsy", "Etsy conversion", "Etsy keyword research".
metadata:
  tags: ["etsy", "ecommerce", "seo", "marketplace", "handmade", "print-on-demand", "digital-downloads", "listing-optimization", "conversion"]
---

# Etsy Listing Optimizer

Audit and optimize Etsy listings (digital and physical) for search visibility, click-through, and conversion. Acts as an experienced Etsy seller and SEO consultant who has shipped thousands of listings across handmade, print-on-demand, and digital categories.

## Usage

Invoke this skill when you have one or more Etsy listings that are underperforming, or you are launching a new shop and want listings built right from day one.

**Basic invocation:**
> Audit this Etsy listing: [URL or paste of title/tags/description]
> Optimize the title and tags for my "personalized leather wallet" listing
> My new digital planner listing isn't ranking — what's wrong?

**With context:**
> Here are my 13 tags, please rewrite them with reasoning
> I sell printable wedding invitations — write me a title formula and 5 examples
> My click-through is fine but conversion is 0.4% — diagnose

The agent works through a 14-point audit, names the highest-impact fixes first, and rewrites titles, tags, and descriptions inline with reasoning.

## How It Works

### Step 1: Listing Audit Framework

Every audit walks the same six pillars in priority order. The agent flags each as PASS, WEAK, or FAIL with a one-line reason.

| Pillar | What the Agent Checks |
|--------|----------------------|
| **Title** | First 40 chars front-loaded with primary keyword, modifiers, intent term, audience. No keyword stuffing, no ALL CAPS, no emoji-clutter. |
| **Tags** | All 13 used, every tag is a multi-word phrase (2-3 words), no plural/singular duplication of the title, mix of head and long-tail. |
| **Description** | First 160 chars are a hook (this is also your meta description). Benefits before specs. Sections scannable. Shop CTA at the end. |
| **Photos** | 10 slots filled, first photo earns the click in the search grid, 3-5 lifestyle shots, scale shot, dimensions/specs graphic, video clip. |
| **Attributes** | Every attribute filled (category, color, occasion, holiday, material, recipient, room) — these feed Etsy's filters. |
| **Shipping** | Processing time <=3 business days, free domestic shipping if product can absorb it, international enabled where viable. |

The agent assigns each listing a score out of 60 (10 per pillar) and orders fixes by impact-per-effort.

### Step 2: Etsy SEO Mechanics

Etsy search ranks listings on a blend of **query match**, **listing quality score**, **recency**, **shipping price**, and **shop quality**. The agent optimizes the inputs you control.

**Title and tag interplay (this is where most sellers fail):**

- The Etsy algorithm reads your title as one long phrase AND tries to extract sub-phrases.
- A tag matches a search query when the tag is contained as an **exact phrase** in the buyer's query.
- Tags do NOT need to repeat title words to count, but **a phrase that appears in BOTH title and tag gets a relevance boost**.
- Multi-word tags beat single-word tags every time. Etsy effectively wastes single-word tags by treating them as low-confidence matches.

**Long-tail strategy:**

- Head terms ("leather wallet") have huge volume but you will not outrank shops with 5,000+ sales.
- Long-tail terms ("personalized leather wallet for groomsmen") have lower volume but realistic ranking and 2-4x higher conversion.
- Target one head term in the title for optionality, but commit your 13 tags to long-tail variants.

**Recency boost:**

- New listings get a temporary boost (~72 hours to ~30 days depending on category).
- Renewing a listing does NOT meaningfully restart this; only a brand new listing does.
- Editing an established, ranking listing can RESET its rank — only edit when current performance is poor.

### Step 3: Title Formula

Use this skeleton:

```
[Primary Keyword] | [Modifier 1] [Modifier 2] [Modifier 3] | [Intent Term] | [Audience / Occasion]
```

- **Primary keyword** (1-3 words): the head term a buyer types. Front-load it in the first 40 characters.
- **Modifiers** (2-3): material, style, color, size, technique. These extend the searchable phrase set.
- **Intent term**: "Gift", "Decor", "Custom", "Personalized", "Printable", "Digital Download". Signals what the listing IS.
- **Audience / Occasion**: "for Mom", "for Wedding", "for Boyfriend", "Christmas Gift", "Nursery". Captures buyer intent searches.

Use commas or pipe separators consistently. Do not use hyphens between every word — Etsy treats hyphens as word breaks but it reads cluttered.

**8 examples by category:**

1. **Handmade jewelry** — `Personalized Birthstone Necklace, Custom Initial Pendant, Dainty Gold Layering Jewelry, Gift for Mom, Birthday Gift for Her`
2. **Leather goods** — `Personalized Leather Wallet, Mens Bifold Wallet with Engraving, Anniversary Gift for Husband, Groomsmen Gift, Custom Leather Gift`
3. **Print-on-demand t-shirt** — `Funny Cat Mom Shirt, Cat Lover T-Shirt, Crazy Cat Lady Tee, Gift for Cat Owner, Mothers Day Shirt for Cat Mom`
4. **Digital wedding invitation** — `Minimalist Wedding Invitation Template, Editable Boho Wedding Invite, Printable Save the Date, Modern Wedding Suite, Instant Download`
5. **Printable wall art** — `Botanical Wall Art Set of 3, Printable Boho Living Room Decor, Pampas Grass Print, Neutral Gallery Wall, Digital Download`
6. **Digital planner** — `2026 Digital Planner for iPad, GoodNotes Daily Planner, Hyperlinked Notability Planner, ADHD Planner Template, Productivity Journal`
7. **Pet portrait (custom)** — `Custom Pet Portrait from Photo, Personalized Dog Painting, Watercolor Pet Memorial, Cat Portrait Gift, Dog Mom Birthday Gift`
8. **Home decor (handmade)** — `Macrame Wall Hanging Boho Decor, Large Macrame Tapestry, Bohemian Living Room Wall Art, Handmade Fiber Art, Housewarming Gift`

Title length: aim for 130-145 characters. Etsy allows 140 in search results display but the field accepts ~140 visible plus URL. Front-load the most valuable phrase.

### Step 4: Tag Strategy

You get 13 tags, 20 characters each. The rules:

- **Use all 13.** An empty tag slot is a competitor's free win.
- **No single words.** "Necklace" alone is wasted. "Birthstone Necklace" works.
- **No tag duplicates words from another tag in the same order.** Etsy de-duplicates internally.
- **Mix head and long-tail.** Roughly: 3 head (high volume), 6 mid-tail, 4 long-tail (specific buyer intent).
- **Match buyer language, not artist language.** Buyers search "boho wall art", not "macrame fiber composition".
- **Cover synonyms across tags.** If title says "Pet Portrait", a tag should be "Dog Painting" and another "Custom Animal Art".
- **Include occasion and audience tags.** "Anniversary Gift for Him", "Gift for Cat Mom".
- **Avoid plurals if singular is in title.** Do not waste a tag on the singular/plural twin.

**Tag set example for the leather wallet listing:**

```
1. personalized leather wallet      (head, matches title)
2. mens bifold wallet               (head, alternate phrase)
3. custom wallet for men            (mid-tail, audience)
4. engraved leather wallet          (mid-tail, feature)
5. groomsmen gift for him           (long-tail, occasion)
6. anniversary gift husband         (long-tail, occasion)
7. boyfriend birthday gift          (long-tail, audience)
8. fathers day gift                 (occasion)
9. monogrammed wallet               (synonym)
10. dad gift from daughter          (long-tail, gifter)
11. graduation gift for him         (long-tail, occasion)
12. handmade leather goods          (category-level)
13. custom mens accessories         (category-level)
```

Notice no single-word tag, every tag is searchable as a phrase, no two tags duplicate the title verbatim.

### Step 5: Photo Strategy

Etsy is a visual-first marketplace. The first photo determines whether you are clicked at all.

**The 10-photo sequence:**

1. **First photo** — earns the click in the search grid. For most categories: lifestyle shot with the product in use, well-lit, single focal point, minimal text overlay. For digital products: a styled mockup with clear category cue (mug-mockup for designs, iPad-mockup for digital planners). FLAT LAY only beats lifestyle for jewelry, paper goods, and stationery where flat is the convention.
2. **Detail / texture shot** — close-up showing material quality.
3. **Lifestyle in context** — product being used or worn.
4. **Scale shot** — product in hand, on a body, or next to a known object.
5. **Variations grid** — colors, sizes, options laid out in one image.
6. **Dimensions / specs graphic** — annotated image with measurements.
7. **Customization preview** — for personalized items, show what personalization looks like.
8. **Packaging shot** — gift-ready packaging if applicable (boosts gift conversion).
9. **Maker / process shot** — handmade authenticity (especially for handmade category).
10. **Reviews / social proof graphic** — quote a 5-star review with permission.

**Video clip:** Etsy boosts listings with video. Even a 5-second 360-degree spin or hand-holding the product significantly lifts conversion. Always include one.

### Step 6: Description Structure

Etsy's algorithm reads the first ~160 characters of the description as a relevance signal AND uses it as the meta description for off-Etsy traffic (Google, Pinterest). Buyers also read top-down on mobile, so structure matters.

```
[HOOK — 1-2 sentences, emotional or outcome-focused, includes primary keyword]

>>> WHY YOU'LL LOVE IT <<<
- Benefit 1 (outcome, not feature)
- Benefit 2
- Benefit 3
- Benefit 4

>>> SPECIFICATIONS <<<
- Material:
- Dimensions:
- Weight / file format:
- What's included:

>>> HOW TO ORDER (or HOW TO USE) <<<
1. Step
2. Step
3. Step

>>> FAQ <<<
Q: Common question
A: Clear answer

>>> SHOP MORE <<<
Browse the full collection: [shop link]
Custom requests: [policy]
Follow the shop for new releases.
```

Use ASCII separators (`>>>`, `---`, `===`) rather than emoji-spam. Etsy strips most formatting, plain text divisions work.

### Step 7: Pricing

Pricing is part of the algorithm — Etsy slightly favors mid-priced listings within a category because they convert at the highest rate. Use a tier strategy across the shop:

- **Anchor item (10-20% of listings)**: lowest price point, designed to capture price-sensitive buyers and pull them into the shop.
- **Mid-tier (60-70% of listings)**: your primary margin drivers, priced at category median.
- **Premium (10-20% of listings)**: high-margin, often custom or larger sizes. These set perceived shop quality.

**Sale strategy:**

- Etsy displays a strikethrough price when the sale is active. The strikethrough is itself a click magnet.
- Run sales of 15-25% (large enough to display, small enough to protect margin).
- Avoid permanent sales — buyers wait for the next price drop and the strikethrough loses meaning.
- Use "sale ends in X" urgency in the first photo's text overlay.

**Etsy Ads breakeven:**

- Etsy Ads charge per click. Compute breakeven CPC:
  `Breakeven CPC = (Profit per sale) * (Conversion rate)`
- Example: $14 profit, 3% conversion = $0.42 max CPC.
- If your bid is auto-set above this, the ad loses money on every sale.

### Step 8: Shipping Setup

Shipping is a ranking factor AND a conversion factor. Etsy boosts shops with **free domestic shipping** in the US (the buyer-facing search has a "free shipping" filter many buyers default to).

- **Domestic free vs flat**: Free shipping wins on rank and conversion. Build the shipping cost into the item price if margin allows. If item is too low-margin (under $15 with high shipping), use flat shipping — the buyer expects it at that price point.
- **International**: Enable to at least Canada, UK, Australia, and the EU. International orders are 20-35% of many shops' revenue. Use Etsy's calculated shipping or set conservative flat rates.
- **Processing time**: 1-3 business days is the sweet spot. Anything over 5 business days actively suppresses your rank — Etsy hides slow shippers from the "ships within 1 day" filter.
- **Print-on-demand**: Set processing time to your provider's actual production time (typically 3-5 days for Printful, 2-7 for Printify) plus 1 buffer day. Underestimating wrecks Star Seller status.

### Step 9: Reviews Game

Reviews are the single largest conversion lever. A listing with 100+ reviews at 5.0 converts 3-5x better than one with 10 reviews at the same average.

- **Packaging insert**: a card asking for an honest review with a QR code to the review link. Mention "if anything is wrong, message us first" — this routes problems away from public 1-star reviews.
- **Follow-up message**: send a brief thank-you message 3-5 days after delivery (Etsy's automated message system). Do not bribe (against Etsy ToS); just thank and softly mention reviews.
- **Dispute resolution**: if a buyer messages with a problem, respond within 4 hours. Offer replacement or refund without arguing. A salvaged 4-star is infinitely better than a 1-star.
- **Never respond defensively to public reviews.** Public replies are read by future buyers; calm, professional responses that offer to make it right turn negatives into trust signals.

### Step 10: Etsy Ads Strategy

Most shops should NOT start Etsy Ads on day one. Ads are a multiplier — they amplify whatever your conversion rate is. Run organic first to establish conversion, then scale with ads.

- **When to start**: minimum 25 organic sales, listing conversion rate >2%, at least 10 listings live.
- **Daily budget tiers**:
  - $1/day — testing, identifies which listings get impressions.
  - $5-10/day — typical small shop scale.
  - $25+/day — only with proven listing economics and >$30 AOV.
- **Kill criteria**: any single listing that has spent 5x its profit-per-sale without a conversion should be paused. Re-enable after that listing's organic conversion improves.
- **Off-site Ads**: Etsy charges 12-15% commission on sales attributed to Etsy's external ads. Once your shop hits the threshold ($10k/year), you cannot opt out. Price accordingly.

### Step 11: Star Seller Metrics

Star Seller is a public badge that lifts conversion ~10-15%. Requirements over a rolling 90 days:

- **Message reply rate <24 hours** on the first response.
- **On-time shipping**: at least 95% of orders shipped by the promised date with tracking added.
- **Average rating >=4.8**.
- **Order count**: minimum number of orders depending on shop size.
- **No open cases / disputes**.

The most common loss reason is the message reply window — set up auto-replies for off-hours and check messages at least twice daily.

### Step 12: Off-Etsy Traffic

Etsy's algorithm rewards listings that bring their own traffic. A buyer who lands on your listing from Pinterest or Google and converts is worth ~2-3x an internal search buyer in the algorithm.

- **Pinterest**: pin every listing 3-5 times across different boards. Pinterest is the #1 off-Etsy traffic source for home decor, weddings, fashion, and digital products.
- **TikTok**: short product demo or before/after videos. Link in bio to shop. The TikTok-to-Etsy pipeline works especially well for unique, gift-able, or aesthetic products.
- **Instagram**: less direct ROI than Pinterest for sellers under 10k followers, but Reels with shop links in caption convert. Use Stories with product link stickers.
- **SEO bump**: Etsy detects external traffic via referrer. Listings with steady off-Etsy clicks get ranked higher in internal search even at the same conversion rate.

### Step 13: Common Penalties

The agent watches for behaviors that get listings or shops suppressed:

- **Duplicate listings**: identical or near-identical listings split traffic and trigger suppression. Use variations (Etsy's built-in variation system) instead of duplicate listings.
- **Mature content flags**: certain words in titles ("naughty", "sexy", "kink") flag listings as adult, removing them from default search. Check Etsy's mature content policy before using edgy language.
- **IP claims**: licensed characters (Disney, Marvel, sports teams), copyrighted song lyrics, and trademarked slogans get listings yanked and shop strikes. Three strikes closes the shop. Never use unlicensed IP.
- **Keyword stuffing**: titles with the same word repeated 5+ times get rank-suppressed even if they don't get manually flagged.
- **Misuse of "personalized" / "custom" attributes**: setting these without actually offering personalization triggers a quality penalty when buyers ask for personalization and you cannot deliver.

### Step 14: Digital vs Physical Optimization

| Lever | Physical Listing | Digital / Printable Listing |
|-------|-----------------|----------------------------|
| **First photo** | Lifestyle shot with product in use | Mockup showing the file in context (frame, mug, iPad) |
| **Title intent term** | "Gift", "Personalized", "Handmade" | "Printable", "Digital Download", "Instant Download", "Editable Template" |
| **Description specs** | Material, dimensions, weight, care | File formats (PDF, JPG, PNG), sizes/dpi, software needed (Canva, GoodNotes), printable size limits |
| **Shipping** | Free domestic preferred, processing time <=3 days | N/A (instant download) — but make sure "Digital" is set in listing type |
| **Tags** | Material + style + audience + occasion | Software/platform + format + use case + audience |
| **Pricing** | Cost-plus + market median | Steeper tiered: $4-8 anchor, $12-18 mid, $25+ bundle |
| **Variations** | Sizes, colors, materials | Editable vs print-only, Canva vs PDF, single vs bundle |
| **Reviews lever** | Packaging insert, follow-up message | Auto-deliver welcome PDF with review request as page 1, plus follow-up message |

## Worked Examples

### Example 1: Generic personalized necklace listing

**Before (the seller's draft):**

```
Title: Cute Necklace - Custom Name Jewelry - Birthday Present

Tags: necklace, jewelry, gift, custom, name, cute, gold, silver,
      pretty, accessory, womens, fashion, present

Description: This is a beautiful custom necklace. It is made of
sterling silver and you can personalize it with any name. Great
for birthdays!
```

**Audit findings:**

- Title FAIL: "Cute" buries the keyword, no occasion specificity, no audience, only 56 characters used out of 140.
- Tags FAIL: 7 of 13 are single words (wasted), 4 duplicate the title verbatim, no long-tail intent phrases.
- Description FAIL: 23 words, no benefits, no specs, no FAQ, no CTA.

**After (optimized):**

```
Title: Personalized Name Necklace, Custom Dainty Gold Necklace,
Initial Pendant Jewelry, Birthday Gift for Her, Bridesmaid Gift,
Mothers Day Necklace
(139 characters)

Tags:
1. personalized name necklace
2. custom name jewelry
3. dainty gold necklace
4. initial pendant necklace
5. birthday gift for her
6. bridesmaid gift jewelry
7. mothers day necklace
8. gift for girlfriend
9. minimalist gold jewelry
10. custom initial necklace
11. layering necklace gold
12. anniversary gift wife
13. christmas gift for mom

Description:
A piece of her every day. This personalized name necklace is
hand-stamped with the name of her choice on dainty 14k
gold-fill — light enough to wear daily, special enough to gift.

>>> WHY YOU'LL LOVE IT <<<
- Personalized with any name up to 12 characters
- 14k gold-fill resists tarnish (not plated)
- Adjustable chain: 16" with 2" extender
- Arrives in a gift-ready velvet pouch — no extra wrapping needed
- Ships in 1-2 business days with tracking

>>> SPECIFICATIONS <<<
- Material: 14k gold-fill / sterling silver / rose gold-fill
- Pendant size: 0.5" wide
- Chain: cable chain, 16" + 2" extender
- Hypoallergenic, nickel-free

>>> HOW TO ORDER <<<
1. Choose metal color
2. Type the name (or names) in the personalization box
3. Select chain length
4. Add to cart — production starts within 24 hours

>>> FAQ <<<
Q: Will it tarnish?
A: 14k gold-fill is bonded, not plated, so it lasts years
   with normal wear.

Q: Can I add multiple names?
A: Yes — message me before ordering for 2+ name designs.

>>> SHOP MORE <<<
See the full Personalized Collection: [link]
Follow the shop for new releases and member-only sales.
```

**Reasoning:** Title now leads with "Personalized Name Necklace" (highest-volume head term), stacks three modifiers, and tails with three audience/occasion phrases. Tags moved to 100% multi-word phrases mixing head, mid, and long-tail intent. Description hooks emotionally, lists benefits before specs, walks through ordering, and ends with a shop CTA — covering both algorithm signals (first 160 chars contain the keyword) and human conversion drivers.

### Example 2: Generic digital planner listing

**Before:**

```
Title: Digital Planner - iPad - Daily Planner

Tags: digital planner, ipad planner, planner, daily, weekly,
      monthly, productivity, organize, schedule, journal,
      goodnotes, notability, pdf

Description: Digital planner for iPad. Has daily, weekly, and
monthly pages. Works with GoodNotes and Notability.
```

**Audit findings:**

- Title FAIL: 32 characters used, no year, no audience, no intent term ("Instant Download").
- Tags WEAK: most are workable but 5 are single words ("planner", "daily", "weekly", "monthly", "organize") — wasted slots.
- Description FAIL: 25 words, no file format details, no how-to-use, no preview steps.

**After:**

```
Title: 2026 Digital Planner for iPad, GoodNotes Daily Planner,
Hyperlinked Notability Planner, Weekly Monthly Productivity
Journal, Instant Download
(141 characters)

Tags:
1. 2026 digital planner
2. ipad daily planner
3. goodnotes planner template
4. notability planner 2026
5. hyperlinked digital planner
6. weekly planner template
7. productivity planner ipad
8. adhd digital planner
9. student planner ipad
10. minimalist digital planner
11. dated planner 2026
12. printable planner pdf
13. digital journal template

Description:
Your most organized year, on iPad. This 2026 hyperlinked
digital planner turns your iPad into a complete daily,
weekly, and monthly planning system — no paper, no rewriting,
no clutter.

>>> WHY YOU'LL LOVE IT <<<
- 800+ hyperlinked pages — tap any date or section to jump
- Dated for 2026 with daily, weekly, monthly, yearly views
- Habit tracker, gratitude log, goal-setting pages built in
- Works with GoodNotes 5 and 6, Notability, Noteshelf, ZoomNotes
- Lifetime access — re-download any time

>>> WHAT'S INCLUDED <<<
- 1 PDF file (hyperlinked, 800+ pages)
- 12 cover designs to swap monthly
- 50 digital sticker pack (PNG, transparent)
- Setup guide PDF (5 pages)

>>> SPECIFICATIONS <<<
- Format: PDF with internal hyperlinks
- Resolution: 1920 x 1080 (iPad-optimized)
- Compatible: GoodNotes 5/6, Notability, Noteshelf, ZoomNotes
- Not compatible: Apple Notes (no hyperlink support)

>>> HOW TO USE <<<
1. Purchase — your files are available instantly under
   "Purchases & Reviews".
2. Download the ZIP and unzip on your computer or iPad.
3. Open the PDF in GoodNotes or Notability — it auto-loads
   the hyperlinks.
4. Start planning. Setup guide walks you through customization.

>>> FAQ <<<
Q: Will this work on Android tablets?
A: Yes, with apps that support PDF hyperlinks (Xodo, Noteshelf).

Q: Can I print it?
A: Yes — the PDF is print-ready at letter and A5 sizes.

Q: I can't find my download.
A: Check Etsy > You > Purchases & Reviews. If you bought as a
   guest, check your email for the download link.

>>> SHOP MORE <<<
Browse the full Digital Planner Collection: [link]
Follow for 2027 updates and seasonal templates.
```

**Reasoning:** Title front-loads "2026 Digital Planner" (the high-intent dated term that buyers search this time of year), explicitly names the two dominant platforms (GoodNotes and Notability — both common search terms), and ends with "Instant Download" (the digital-product intent term). Tags moved to 100% phrases and added intent niches ("adhd digital planner", "student planner ipad") that capture audience-specific searches with low competition. Description handles the unique digital-product needs — what's included, what software works, how to access the download, and the universal "I can't find my download" FAQ that prevents 1-star reviews.

## Output

The agent produces:

- **Listing audit scorecard**: each of the 6 pillars rated PASS / WEAK / FAIL with one-line reasoning.
- **Rewritten title**: with character count and word-by-word reasoning.
- **Rewritten 13-tag set**: classified by head / mid-tail / long-tail and intent type.
- **Rewritten description**: structured with the hook + benefits + specs + how-to + FAQ + CTA template.
- **Photo plan**: a 10-slot list naming each photo type and any missing shots.
- **Pricing recommendation**: where this listing should sit (anchor / mid / premium) and a sale strategy.
- **Shipping recommendation**: free vs flat, processing time, international.
- **Ads recommendation**: whether to advertise this listing now and what daily budget.
- **Off-Etsy traffic plan**: which platforms to drive traffic from based on the product category.
- **Risk warnings**: any IP / mature content / duplicate listing concerns.

## Common Scenarios

### "I have a listing with traffic but no sales"
The agent diagnoses conversion: photos (especially first photo), price relative to category, reviews count, description quality, and shipping cost. Traffic-not-converting is almost always photos or shipping cost.

### "I have a listing with no traffic at all"
The agent diagnoses discoverability: title front-loading, tags (single words vs phrases), listing recency, off-Etsy traffic. No-traffic is almost always a tags problem combined with a shop with too few sales to compete on head terms.

### "How do I rank for [head term]?"
The agent assesses your shop's authority (review count, sales count) and either targets the head term in the title with realistic long-tail tags, or recommends starting with a long-tail variant where you can actually rank.

### "Should I run Etsy Ads?"
The agent computes breakeven CPC from your margins and conversion rate, checks the listing has hit the readiness criteria, and recommends a starter daily budget with kill criteria.

### "I lost Star Seller — how do I get it back?"
The agent checks the four metrics (reply time, on-time shipping, rating, disputes), identifies which dropped, and gives a 90-day recovery plan.

## Tips for Best Results

- Provide the listing URL or paste the full title, all 13 tags, the full description, and a description of the first 3 photos — the more context the more accurate the audit.
- Mention category, price point, and current sales/review count — the recommendations differ for a 0-sale new shop vs a 1,000-review established shop.
- Share what success looks like — "I want to rank for X", "I want my conversion above 3%", "I want 5 sales/week" — so the agent can tune recommendations to your goal.
- For multiple listings, the agent can audit a representative one and produce a template you apply to the rest.
- Tell the agent if you are handmade, print-on-demand, or digital — optimization rules differ meaningfully.

## When NOT to use

This skill is built around Etsy's specific algorithm, attribute system, and buyer behavior. Do not use it for:

- **High-volume Amazon FBA**. Amazon ranks on entirely different signals (sales velocity, ACOS, A9 algorithm, brand registry). Title and bullet conventions differ. Use an Amazon-specific listing optimizer.
- **Shopify drop-shipping stores**. Shopify shops live or die on paid traffic (Facebook, TikTok, Google Ads), product-page conversion design, and email/SMS funnels — not on a marketplace algorithm. The skills you need are CRO, ad creative, and email automation, not Etsy SEO.
- **eBay or Mercari**. Different algorithms, different buyer behaviors, different photo conventions.
- **Wholesale or B2B handmade sales (Faire, Tundra)**. Wholesale buyers care about margin, MOQs, and lead times — none of the consumer-facing levers in this skill apply.
- **Print-on-demand on your own Shopify store via Printful/Printify**. The product side overlaps but the marketing playbook is paid traffic, not marketplace SEO.
