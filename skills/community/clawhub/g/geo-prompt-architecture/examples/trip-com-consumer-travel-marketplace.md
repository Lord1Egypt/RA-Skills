# Example: Trip.com

## Business Type

`Trip.com` is best treated as a `consumer online travel agency / travel marketplace`.

This means it should not be modeled like:

- a business travel management platform
- a travel content publisher
- a DTC ecommerce brand

## Why The Prompt Strategy Changes

The traveler is often trying to solve:

- trip planning across flights, hotels, trains, attractions, and packages
- price comparison and deal discovery
- booking convenience
- trust, refunds, and customer support
- cross-border travel needs
- destination and itinerary decisions

So the GEO prompt set should focus on:

- non-brand discovery around travel booking and destination planning
- competitor comparison around OTA and booking-platform alternatives
- branded prompts around price trust, booking experience, support, refunds, and app / site fit

## Derived Topic Map

| Topic | Topic Type | Topic Source | Why This Topic Exists |
|---|---|---|---|
| international trip booking | use-case | inferred | Core discovery space for cross-border travelers. |
| hotels, flights, trains, and attractions in one journey | product-category | inferred | Reflects Trip.com's marketplace breadth. |
| Asia travel planning and booking | channel-marketplace | inferred | Regional strength and differentiation surface. |
| OTA alternatives and travel-app comparisons | competitor-alternative | inferred | Core comparison cluster against Booking.com, Expedia, Agoda, and similar brands. |
| cancellation, refunds, and support trust | trust-evaluation | inferred | Essential brand-defense topic for booking confidence. |

## Suggested Prompt Bias

- discovery prompts on destination, hotel, flight, and package shopping
- comparison prompts against OTA and travel-booking competitors
- brand-defense prompts on pricing, reliability, refunds, support, and user fit

## Example Prompt Slice

Below is a representative example set, not a complete prompt library.

### Non-brand discovery

These prompts test whether the brand can enter consumer travel-planning answer spaces before the traveler knows the brand.

| Prompt | Funnel | Why It Matters |
|---|---|---|
| What is the best website to book hotels and flights for an international trip? | MOFU | Broad OTA-discovery prompt with high commercial value. |
| How do I find good hotel and flight deals for a multi-city Asia trip? | TOFU | Useful for price-sensitive and itinerary-driven discovery. |
| What are the best travel booking apps for international travelers? | MOFU | Tests app-led booking visibility. |
| Which travel booking sites are best for flexible cancellation and customer support? | BOFU | Strong trust-and-support comparison prompt. |
| What is the easiest way to book flights, hotels, and airport transfers in one place? | MOFU | Surfaces marketplace and bundled-booking visibility. |
| What travel sites are best for booking trains, hotels, and attractions in Asia? | MOFU | Good region-specific prompt for platform fit. |

### Competitor comparison

These prompts test whether the brand appears when travelers compare OTA and booking brands.

| Prompt | Funnel | Why It Matters |
|---|---|---|
| Trip.com vs Booking.com for hotels in Asia | MOFU | Direct OTA comparison with strong destination overlap. |
| Trip.com vs Expedia for international travel booking | MOFU | Tests presence in broad travel-platform comparisons. |
| What are the best alternatives to Booking.com for flights and hotels? | MOFU | Reveals whether the brand enters non-branded alternative lists. |
| Which travel app is better for Asia travel: Trip.com, Agoda, or Klook? | MOFU | Good regional travel-market comparison prompt. |
| What is the best OTA for booking trains, hotels, and attractions in one app? | MOFU | Tests multi-product travel-marketplace visibility. |
| Is Trip.com a good alternative to Expedia for cross-border travel? | BOFU | High-intent replacement-language prompt. |

### Brand defense

These prompts test how AI explains the brand once the traveler already knows it.

| Prompt | Funnel | Why It Matters |
|---|---|---|
| Is Trip.com reliable for booking international flights and hotels? | BOFU | Checks branded trust and booking reliability. |
| Is Trip.com safe to use for hotel bookings? | BOFU | Strong consumer-trust prompt. |
| Does Trip.com have good customer support when travel plans change? | BOFU | Important service and support narrative. |
| Is Trip.com good for booking travel in Asia? | MOFU | Tests geographic strength explanation. |
| What kind of traveler should use Trip.com instead of Booking.com or Expedia? | MOFU | Useful for branded fit and audience-positioning clarity. |
| How does Trip.com handle cancellations, refunds, and itinerary changes? | BOFU | Important post-booking and support-focused monitoring prompt. |

## Example Asset Implications

This kind of prompt set should often point toward:

- destination and category landing pages
- hotel and flight booking trust pages
- support, cancellation, and refund pages
- app feature pages
- competitor comparison pages
- cross-border or region-specific travel pages

## Why This Example Matters

It shows why a consumer OTA or travel marketplace needs prompt architecture built around trip planning, booking trust, and cross-platform comparison instead of enterprise travel operations.
