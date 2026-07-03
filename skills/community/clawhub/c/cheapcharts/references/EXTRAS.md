# Extras: Savings Strategies & Adjacent Topics

> Situational knowledge that isn't needed for the core deal-lookup flow.
> Load this when the conversation turns to maximizing savings, cross-store
> ownership, seasonal timing, or video games.

## Gift Card Stacking Strategy

CheapCharts tracks Apple gift card discounts at **https://www.cheapcharts.com/us/gift-card-deals** - retailers like Target, Best Buy, PayPal, Amazon, and Costco regularly sell $100 Apple gift cards for $80-$90 (10-25% off).

**Compound savings:** Buy a discounted Apple gift card -> use it to purchase an already-discounted movie on iTunes/Apple TV. A $4.99 movie bought with a 20%-off gift card effectively costs **$3.99**.

**Known patterns (from CheapCharts gift card deal history):**

| Retailer | Typical Deal | Stacking Tip |
|---|---|---|
| Target | $10-$15 bonus GC with $100 Apple GC | Use Target Circle Card for extra 5% off |
| Best Buy | $10-$15 bonus GC with $100 Apple GC | Stack with PayPal 5% off Best Buy |
| Amazon | $15 credit with $100 Apple GC | Use promo codes (e.g. `APPLEBF`, `APPLEGIFT`) |
| Costco | 10-20% off Apple GC (members only) | Check Costco warehouse + online |

These promotions rotate every few months, peaking around Black Friday and holidays. When recommending an iTunes/Apple TV purchase, check the gift card deals page - if an active gift card deal exists, mention it as a way to stack savings.

## Movies Anywhere Compatibility

Many digital movie purchases on iTunes/Apple TV, Amazon, Vudu, and Google Play are **Movies Anywhere (MA) compatible**. MA-compatible titles sync across all four stores - buy on iTunes, watch on Vudu/Amazon/Google Play and vice versa.

**Important:** CheapCharts does NOT expose MA compatibility in any endpoint ([Pitfall #24](PITFALLS.md#24-movies-anywhere-compatibility-is-not-exposed-by-any-cheapcharts-endpoint)). There is no `isMoviesAnywhere` field, no MA filter, and no MA endpoint. The Movies Anywhere website itself does not have a stable public API (returns JS-rendered HTML only - no JSON-LD).

**Detection strategy (programmatic):** Use a studio-based heuristic. MA compatibility is determined by studio participation in the Movies Anywhere consortium:

| MA-Compatible Studios | NOT MA-Compatible (major) |
|---|---|
| Walt Disney Studios (Disney, Pixar, Marvel, Lucasfilm, 20th Century Studios, Searchlight) | Paramount (incl. Republic, Miramax) |
| Warner Bros. (New Line, Castle Rock, HBO theatrical) | MGM |
| Universal (DreamWorks, Focus, Illumination) | Lionsgate (incl. Summit, Starz) |
| Sony Pictures (Columbia, TriStar, Screen Gems, AFFIRM, Crunchyroll theat.) | The Weinstein Company (defunct) |
| 20th Century Studios (now under Disney but historically Fox) | Some A24 titles (varies) |

CheapCharts gives you `imdbId`; fetch the studio via IMDb's public page or a movie DB API (see the studio-lookup snippet in [RECIPES.md](../RECIPES.md#movies-anywhere-studio-lookup)).

**Implications for cross-store comparison:**
- For MA-compatible titles, the cheapest store wins regardless of where the user watches
- For NOT MA-compatible titles, the user should buy from the store they actually want to watch on
- For unknown studios, suggest verifying at moviesanywhere.com or the Movies Anywhere app

## Seasonal Sales Calendar (iTunes / Apple TV)

iTunes/Apple TV deals follow predictable annual patterns. Use this to set expectations and proactively suggest checking deals during these windows:

| Period | Sale Type | Typical Discount |
|---|---|---|
| Jan-Feb | Oscar season | Best Picture contenders 30-50% off |
| Mar-Apr | Spring sale | Wide catalog discounts, often $4.99 |
| May-Jul | Summer blockbuster sales | Tied to theatrical releases |
| Oct | Horror month | *Get Out*, *Hereditary*, etc. at $3.99-$4.99 |
| Nov-Dec | Black Friday -> New Year | Biggest window: $0.99 rentals, $4.99 purchases |
| Tuesdays | Weekly spotlight deals | 8-30+ titles drop, $0.99 rentals to $4.99 buys |

**Studio promotions** (Warner Bros., Universal, Disney) run independently of seasonal sales - flash drops with no announcement, lasting 24-72 hours.

## CheapCharts Games (related but not in scope)

CheapCharts also tracks video game prices at **games.cheapcharts.com** (Xbox, PlayStation, Nintendo Switch). It is a separate product: separate website, separate iOS/Android apps, and **no public API** (verified 2026-06-23 - all four GPT API endpoints and DetailData only serve movies/TV/books, not games).

**If a user asks about game deals:** point them to the website and the mobile apps:
- Website: https://games.cheapcharts.com
- iOS app: id1622193150
- Android app: com.cheapcharts.cheapcharts_games

The `deals.py` script returns a clear error message if you pass `--store games` (it checks for the literal string and exits with code 2 + a redirect message).

If CheapCharts ever releases a games API, add it as a separate script (e.g., `scripts/games_deals.py`) rather than overloading `deals.py` - the data shapes, store codes, and item taxonomies are different.

## Related Resources

- **Mobile apps:** CheapCharts Movie & TV Deals (iOS: id772046134, Android: com.lollipapp.cc), CheapCharts Games (iOS: id1622193150, Android: com.cheapcharts.cheapcharts_games)
- **JSON-LD hints:** Key CheapCharts website pages expose JSON-LD `potentialAction` hints that link directly to the GPT API endpoints with pre-filled parameters. Use as a browser-based fallback if the API doesn't cover a specific query ([Pitfall #20](PITFALLS.md#20-json-ld-fallback-for-unsupported-queries)).
- **Apple TV app gap:** The Apple TV app uses a different catalog index than iTunes. Many deals (boxsets, complete series bundles, older catalog titles) appear on CheapCharts/iTunes but are invisible in the Apple TV app. If a user can't find a deal in Apple TV, direct them to the iTunes purchase link (`productPageUrl` or `iTunesUrl` from DetailData).
