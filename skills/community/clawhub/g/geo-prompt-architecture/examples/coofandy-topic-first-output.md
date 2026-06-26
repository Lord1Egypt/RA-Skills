# Example Output: Coofandy

This example shows the corrected default operating model for a GEO prompt pack:

- `5` topics
- `50` prompts total
- `10` prompts per topic
- `30` non-brand discovery prompts
- `15` competitor comparison prompts
- `5` brand defense prompts

The purpose is to avoid the common failure mode where a prompt set becomes too brand-heavy and stops behaving like a real GEO monitoring system.

## Input Summary

- Brand: `Coofandy`
- Website: `https://coofandy.com`
- Business model: `ecommerce / marketplace-led men's apparel brand`
- Target market: `United States`
- Priority channels: `Amazon`, `Walmart`
- Weak AI surface: `Google AI Overviews`
- Product-line seeds:
  - mens shirts
  - mens pants
  - 2 piece set
  - mens matching sets
  - mens turtleneck sweater
- Competitor set:
  - high: Men's Wearhouse, Express
  - medium-high: Banana Republic, Nautica
  - medium: Ralph Lauren, Gap, Tommy Hilfiger, Zara, Levi's, Calvin Klein, Steve Harvey

## Why This Version Is Better

The earlier example overused branded prompts by forcing every topic to include too much brand-heavy logic.

This corrected version keeps the real GEO priorities:

- discovery prompts should dominate
- competitor prompts should mostly test whether the brand can enter comparison spaces without being named
- brand-defense prompts should stay sparse and high-value

In this example, only `5` prompts explicitly use `Coofandy`, one per topic.

## Topic Map

| Topic | Topic Type | Topic Source | Related Product Lines | Why This Topic Exists |
|---|---|---|---|---|
| summer business-casual shirts | product-category | derived-from-product-line | mens shirts | Core volume topic with overlap across office, smart casual, and hot-weather wear. |
| lightweight pants for hot weather and travel | product-category | derived-from-product-line | mens pants | Strong demand cluster around comfort, travel, and polished summer dressing. |
| vacation-ready 2 piece sets | product-category | derived-from-product-line | 2 piece set | Signature Coofandy category with resort, vacation, and easy-outfit intent. |
| matching sets for easy outfit formulas | product-category | derived-from-product-line | mens matching sets | High-fit category for convenience-led outfit planning and casual travel. |
| smart-casual turtleneck layering | product-category | derived-from-product-line | mens turtleneck sweater | Seasonal topic for fall and winter layering, smart casual, and value comparison. |

## Default Pack Structure

For this client, the default `5 topics / 50 prompts` pack uses:

- `6` non-brand discovery prompts per topic
- `3` competitor comparison prompts per topic
- `1` brand defense prompt per topic

That produces:

- `30` non-brand discovery prompts
- `15` competitor comparison prompts
- `5` brand defense prompts

## Prompt Set

### Topic 1: summer business-casual shirts

| Layer | Funnel | Prompt | Why It Matters |
|---|---|---|---|
| Non-brand discovery | TOFU | How can men dress business casual in summer without wearing stiff dress shirts? | Captures educational intent before brand awareness. |
| Non-brand discovery | TOFU | What shirt fabrics are best for humid weather and all-day office comfort? | Connects fabric logic to hot-weather business use. |
| Non-brand discovery | TOFU | What colors of men's shirts are most versatile for summer business-casual outfits? | Useful for styling-led, non-branded discovery. |
| Non-brand discovery | MOFU | What are the best men's shirts for hot weather that still look business casual? | Core category-entry prompt with strong commercial value. |
| Non-brand discovery | MOFU | What are the best men's shirts for travel that stay comfortable and look polished? | Bridges travel and office-ready shirt demand. |
| Non-brand discovery | MOFU | What are the best affordable men's shirts that look more premium than they cost? | Important value-style discovery prompt. |
| Competitor comparison | MOFU | What are the best alternatives to Banana Republic men's shirts for summer business casual? | Tests whether Coofandy can enter non-branded alternative lists. |
| Competitor comparison | MOFU | Express vs Banana Republic men's shirts: which is better for affordable office style? | Comparison cluster likely to surface replacement candidates. |
| Competitor comparison | MOFU | Which men's brands make the best affordable business-casual shirts for hot weather? | Broad comparison prompt that should allow candidate-list entry. |
| Brand defense | BOFU | Are Coofandy men's shirts good for business casual offices in hot weather? | High-value branded validation prompt tied to the core use case. |

### Topic 2: lightweight pants for hot weather and travel

| Layer | Funnel | Prompt | Why It Matters |
|---|---|---|---|
| Non-brand discovery | TOFU | What pants fabrics are best for hot and humid weather if I still want to look put together? | Educational climate-led prompt. |
| Non-brand discovery | TOFU | What shoes work best with lightweight men's pants for summer outfits? | Styling entry point that can expose brand fit later. |
| Non-brand discovery | TOFU | Can men's linen or lightweight pants work for business casual offices? | Bridges category education with workplace context. |
| Non-brand discovery | MOFU | What are the best men's pants for summer travel that still look polished? | Strong demand cluster around travel and presentation. |
| Non-brand discovery | MOFU | What are the best affordable men's pants for travel, walking, and dinner outfits? | Tests value-oriented commercial intent. |
| Non-brand discovery | MOFU | What are the best men's pants for flights and all-day wear that don't look sloppy? | High intent with clear comfort and appearance needs. |
| Competitor comparison | MOFU | What are the best alternatives to Banana Republic men's summer pants? | Classic alternative-entry prompt. |
| Competitor comparison | MOFU | Gap vs Nautica men's pants: which is better for relaxed summer style? | Competitor comparison that can generate replacement opportunities. |
| Competitor comparison | BOFU | Which men's brands make the best lightweight business-casual pants without premium prices? | Strong commercial comparison prompt. |
| Brand defense | BOFU | Are Coofandy men's pants worth buying for hot-weather travel and all-day wear? | High-value branded decision-stage question. |

### Topic 3: vacation-ready 2 piece sets

| Layer | Funnel | Prompt | Why It Matters |
|---|---|---|---|
| Non-brand discovery | TOFU | What fabrics are best for men's 2 piece sets in hot weather? | Educational prompt tied to climate and comfort. |
| Non-brand discovery | TOFU | Can men's 2 piece sets work for smart casual dinners or rooftop events? | Expands category understanding beyond loungewear. |
| Non-brand discovery | TOFU | What colors make men's 2 piece sets look more expensive? | Styling-led discovery with value implications. |
| Non-brand discovery | MOFU | What are the best men's 2 piece sets for vacation and resort wear? | Core category query with strong monitoring value. |
| Non-brand discovery | MOFU | What are the best affordable men's 2 piece sets for beach trips and summer travel? | High-intent value cluster. |
| Non-brand discovery | MOFU | Can I wear a men's 2 piece set as separates for multiple outfits on one trip? | Important wardrobe-efficiency prompt. |
| Competitor comparison | MOFU | What are the best alternatives to Zara men's 2 piece sets for summer vacations? | Tests whether Coofandy enters a fashionable alternative set. |
| Competitor comparison | MOFU | Zara vs Express for men's vacation sets: which is better value? | Comparison pattern that can yield category substitution. |
| Competitor comparison | BOFU | Which men's brands make the best resort-ready 2 piece sets without designer prices? | Strong commercial shortlist prompt. |
| Brand defense | BOFU | Are Coofandy 2 piece sets breathable enough for beach trips and summer travel? | Branded validation tied directly to climate and travel intent. |

### Topic 4: matching sets for easy outfit formulas

| Layer | Funnel | Prompt | Why It Matters |
|---|---|---|---|
| Non-brand discovery | TOFU | Are men's matching sets still in style for adults, or do they look too trendy? | Captures style skepticism before purchase intent. |
| Non-brand discovery | TOFU | How should men's matching sets fit if I want a polished but relaxed look? | Helpful fit-led educational prompt. |
| Non-brand discovery | TOFU | Can men's matching sets work for brunch, date nights, and vacation outfits? | Occasion-driven discovery beyond product taxonomy. |
| Non-brand discovery | MOFU | What are the best men's matching sets if I want easy outfits that don't look sloppy? | Strong convenience-led category prompt. |
| Non-brand discovery | MOFU | What are the best men's matching sets for weekend travel and casual dinners? | Commercial scenario prompt with clear use case. |
| Non-brand discovery | MOFU | What are the best affordable men's matching sets for summer capsule wardrobes? | High-value, high-utility discovery prompt. |
| Competitor comparison | MOFU | What are the best alternatives to Nautica or Express for men's matching sets? | Non-branded alternative discovery around known competitors. |
| Competitor comparison | MOFU | Zara vs Nautica men's matching sets: which is better for everyday summer wear? | Useful mainstream comparison space. |
| Competitor comparison | MOFU | Which men's brands make matching sets that feel mature and wearable, not flashy? | Helps test audience-fit candidate entry. |
| Brand defense | BOFU | Are Coofandy men's matching sets worth it for travel and capsule wardrobes? | Single branded validation prompt for this topic. |

### Topic 5: smart-casual turtleneck layering

| Layer | Funnel | Prompt | Why It Matters |
|---|---|---|---|
| Non-brand discovery | TOFU | Are turtleneck sweaters still in style for men, or do they look dated? | Captures top-funnel fashion hesitancy. |
| Non-brand discovery | TOFU | What fabric is best for a men's turtleneck sweater if I want something soft but not too warm? | Educational fabric-led prompt. |
| Non-brand discovery | TOFU | What colors of men's turtleneck sweaters are most versatile for fall and winter? | Classic styling and wardrobe-building prompt. |
| Non-brand discovery | MOFU | What are the best men's turtleneck sweaters for smart-casual outfits and layering? | Core seasonal category prompt. |
| Non-brand discovery | MOFU | Can a men's turtleneck replace a dress shirt in a business-casual wardrobe? | Helps test smart-casual substitution logic. |
| Non-brand discovery | MOFU | What are the best affordable men's turtleneck sweaters that look premium under a blazer? | Value-oriented commercial discovery. |
| Competitor comparison | MOFU | What are the best alternatives to Banana Republic men's turtleneck sweaters? | Alternative prompt that should allow candidate-list entry. |
| Competitor comparison | MOFU | Ralph Lauren vs Calvin Klein turtleneck sweaters: which is better value for smart casual outfits? | Premium-to-mainstream comparison cluster. |
| Competitor comparison | MOFU | Which men's brands make good turtleneck sweaters for layering without luxury prices? | Strong value-comparison prompt. |
| Brand defense | BOFU | Are Coofandy turtleneck sweaters good for layering under a blazer? | Branded validation tied to the core styling use case. |

## Priority Monitoring List

### Top Topics

- summer business-casual shirts
- lightweight pants for hot weather and travel
- vacation-ready 2 piece sets
- matching sets for easy outfit formulas
- smart-casual turtleneck layering

### Top Non-brand Discovery Prompts

- What are the best men's shirts for hot weather that still look business casual?
- What are the best men's pants for summer travel that still look polished?
- What are the best men's 2 piece sets for vacation and resort wear?
- What are the best men's matching sets if I want easy outfits that don't look sloppy?
- What are the best men's turtleneck sweaters for smart-casual outfits and layering?

### Top Competitor Comparison Prompts

- What are the best alternatives to Banana Republic men's shirts for summer business casual?
- What are the best alternatives to Banana Republic men's summer pants?
- What are the best alternatives to Zara men's 2 piece sets for summer vacations?
- What are the best alternatives to Nautica or Express for men's matching sets?
- What are the best alternatives to Banana Republic men's turtleneck sweaters?

### Top Brand Defense Prompts

- Are Coofandy men's shirts good for business casual offices in hot weather?
- Are Coofandy men's pants worth buying for hot-weather travel and all-day wear?
- Are Coofandy 2 piece sets breathable enough for beach trips and summer travel?
- Are Coofandy men's matching sets worth it for travel and capsule wardrobes?
- Are Coofandy turtleneck sweaters good for layering under a blazer?

## Why This Example Matters

It demonstrates the intended default behavior:

- `5 topics / 50 prompts`
- discovery prompts dominate
- competitor prompts mainly stay non-branded
- explicit branded prompts stay sparse and strategic
- every topic still has one strong brand-defense question for downstream monitoring
