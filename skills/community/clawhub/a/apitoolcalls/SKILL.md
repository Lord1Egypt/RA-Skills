---
name: apitoolcalls
description: "Describes remote MCP tools and connection settings for API Tool Calls for requests involving SVG QR codes, barcode scans and SVG barcodes, public YouTube captions, public pages converted to Markdown, full data source plans, CPSC recall notices, possible basement water causes, fixed SEO checks, company facts and proofreading with an OpenRouter key, or résumé skill gaps against Columbus, Ohio job postings. Applies when configuring or calling these tools."
---

# [API Tool Calls](https://apitoolcalls.com)

[API Tool Calls](https://apitoolcalls.com): connect once to one small MCP door at https://apitoolcalls.com/mcp. Its 3 meta tools find, describe and call any of our 90 tools, with under 1k tokens of definitions at connection time however many tools ship. Directory scanners and clients that need the full tool listing can read https://apitoolcalls.com/mcp?tools=all.

```text
search_tools(query="qr code")
get_tool_schema(name="make_qr")
call_tool(name="make_qr", arguments={"text":"https://example.com"})
```

## Connect

- Remote MCP endpoint: `https://apitoolcalls.com/mcp`, Streamable HTTP.
- Command line by [API Tool Calls](https://apitoolcalls.com) (Cowerx), Python 3.8+: install from `https://apitoolcalls.com/apitc`, then `apitc search "qr code"` and `apitc call make_qr --arg text=https://example.com -o qr.json`.
- No key uses the free allowance, or set `APITC_KEY` / `--key` for an existing key.

## Tools

| Tool | Function |
| --- | --- |
| `apa_citation_generator` | Format an APA reference and in-text citations from entered source metadata. |
| `average_calculator` | Compute mean, median, modes, range, sum, count, population and sample standard deviation, plus an optional separately weighted average. |
| `base_convert` | Converts a bounded integer string between bases 2 through 36 using exact BigInt arithmetic. Inputs contain 1–4096 digits and must be valid in the source base. Optional bitWidth (1–4096) validates a bit pattern; signed=true requires a width and reads the source value as two’s complement. Unsigned is the default. |
| `basement_water_cause` | Eight observation groups return every rule-matched possible cause, evidence, safe first checks, trade referrals and sources. Hazard stops come first; no probabilities or structural diagnosis. Pure rules, no network or model. |
| `bmi_calculator` | Calculate adult BMI and its band from weight, height and units. |
| `board_feet` | Sum board-foot lumber volumes from entered dimensions and whole piece counts, with per-row optional prices and a priced subtotal. |
| `body_fat_calculator` | Calculate Navy body fat percentage from sex and tape measurements. |
| `calendar_age_difference` | Calculate years, months, days and total days between two birth dates. Use explicit Gregorian dates and a stated month-end convention, free in your browser. |
| `calorie_calculator` | Calculate resting energy and daily calories from adult measurements, formula and activity level. |
| `character_count` | Count Unicode characters, words, lines and UTF-8 bytes from text. |
| `combinations` | Compute exact combinations nCr or permutations nPr for bounded integer inputs. |
| `company_facts` | Read a business's own home, about and contact pages and return its name, address, phone, email, founding year and what it does, each with the page it came from; needs your OpenRouter key. |
| `compound_interest_calculator` | Calculate compound or simple interest, balance, total contributed, interest earned, modeled APY and yearly balances from principal, nominal rate, term and deposit timing. |
| `concrete_calculator` | Computes slab, footing, cylindrical-column or solid-step concrete volume, waste allowance and whole 40/60/80 lb bag counts from QUIKRETE No. 1101 yields. |
| `date_calculator` | Count signed calendar days or weekdays between dates, or add and subtract calendar units with month-end clamping. |
| `debt_to_income` | Arithmetic on entered numbers only: sum up to 100 entered monthly debt payments and divide by positive gross monthly income. Shows the sum and ratio percentage, rounded half up to two decimal places, with no comparison bands or classification. |
| `decimal_to_fraction` | Converts a terminating or explicitly repeating decimal to an exact simplified fraction, mixed number and decimal display. |
| `discount_calculator` | Calculate a discounted price, ordered stacked percentage discounts, savings, effective discount and total with an entered sales tax percentage after discounts. |
| `driveway_cost` | Returns national installed ranges with no published typical figure. One call compares all ten surfaces. Base, drainage and permits are not priced; removal is priced only for an existing concrete driveway. Includes unpriced checks, two separate national reference cards and dated sources. Pure arithmetic, no network or model. |
| `epoch_convert` | Converts a Unix timestamp (seconds or milliseconds, detected by size) or an ISO 8601 date string to epoch seconds, epoch milliseconds, an ISO UTC time, the same moment in an optional IANA time zone, and the weekday there. A date string with no offset is read in the given zone, UTC by default. Pure standard-library rules, no network, model or clock. |
| `ev_charger_install_cost` | Returns safety first, the exact 125% minimum breaker calculation, panel triage, unpriced extras and dated federal 30C rules. Reference cards are utility and DOE program figures, not a price for this home. A licensed electrician and permit are needed; confirm local requirements and inspection. Pure rules and Decimal, no network, model or clock. Web and MCP share the free daily allowance. |
| `fence_cost` | Returns calculated low, median bid and high bounds from exact City of Sunrise FL 2020 municipal bid rows, their scope and sources, and local permit guidance. Historical public bid observations are not current homeowner prices. |
| `find_data` | Get a full free Data Finder plan for up to three sources: fit, cost at your monthly volume, resale terms with recorded clause, URL and read date, and build-it-yourself guidance. No live source lookup. Defaults: volume 0, US, no resale. |
| `flooring_cost` | Returns national installed ranges (labor and materials), no labor-only figure, and no published typical figure. One call compares all eight materials using net room area, with hardwood order guidance, an unpriced prep checklist, a separate historical Census reference card and dated sources. Pure arithmetic, no network or model. |
| `font_generator` | Convert text to a selected Unicode letter style. |
| `fraction_calculator` | Computes exact addition, subtraction, multiplication or division of fractions and mixed numbers, with simplified, mixed and decimal forms. |
| `fuel_cost` | Calculate trip fuel quantity and cost from entered distance, fuel economy, fuel price and currency; supports US mpg, L/100 km and km/L. |
| `funeral_cost` | Returns FTC Funeral Rule rights first. Reference figures are NFDA 2023 national medians from an industry member survey, not local prices. Bundle cards apply only to services with viewing; direct services have no citable national bundle figure. The worksheet adds up the family's own itemized prices and keeps missing prices visible. Pure rules and Decimal money, no network or model. Web and MCP share the free daily allowance. |
| `furnace_age` | Calculates age at your selected as-of date, keeps NAHB and InterNACHI life guidance separate, applies EPA age guidance and the DOE repair comparison to your own quotes, and returns separately labeled historical and modeled replacement references. |
| `gcf_calculator` | Compute the greatest common factor of 2–20 integers with exact BigInt arithmetic and complete prime factorizations. |
| `get_transcript` | Read public YouTube captions as timestamped plain text. Captions only, no video or audio. |
| `gpa_calculator` | Computes credit-weighted GPA with A=4, B=3, C=2, D=1, F=0 and optional common honors +0.5/AP +1.0 bonuses for passing grades; school conventions vary. |
| `grade_calculator` | Computes a weighted category average and optionally the final-exam percentage needed to reach a target course grade. |
| `gravel_calculator` | Calculate gravel layer volume and US short tons from rectangle dimensions, circle diameter or total area, depth in inches and editable bulk density. |
| `heart_rate_zones` | Calculate adult maximum heart rate and moderate and vigorous target zones from age and optional measured rates. |
| `hours_calculator` | Calculate worked minutes, decimal hours and H:MM from clock times, an overnight flag and an unpaid break. |
| `inflation_calculator` | Convert US dollars between published BLS CPI-U months or annual averages since 1913. Reports equivalent value, cumulative inflation, average annual rate and yearly table. Omit both months for annual mode; unavailable periods are rejected. Arithmetic on CPI, not financial advice. |
| `json_formatter` | Format, minify or validate JSON text while preserving number tokens. |
| `julian_day_convert` | Convert explicit UTC civil timestamps to Julian day and back using the proleptic Gregorian calendar. See the noon epoch, time-scale convention and ordinal day. |
| `kitchen_remodel_cost` | Size and scope return a national planning estimate range rounded to the nearest 100 dollars, with no published typical figure, two separate dated reference cards and sources. The result has no line items or labor/material split: the published bands include both, and no public source we trust splits them for a typical kitchen. Pure arithmetic, no network or model. |
| `lcm_calculator` | Compute the least common multiple of 2–20 integers with exact BigInt arithmetic and complete prime factorizations. |
| `loan_schedule` | Computes fixed-rate monthly principal and interest payments, total interest, payoff month and a complete amortization table of at most 360 rows from entered amounts and a nominal annual rate. Optional down payment reduces principal; extra monthly principal payments shorten the modeled term. Uses exact rational arithmetic and nearest-cent half-up rounding. Taxes, insurance, PMI and fees are excluded. |
| `logarithm` | Compute a logarithm for a positive value and any positive base other than 1. |
| `long_divide` | Divide decimal strings exactly with long division steps, an integer quotient and remainder. See terminating, repeating or truncated decimals in your browser. |
| `make_barcode` | Make an SVG barcode. Validates retail check digits and lengths. GS1-128 and GS1 DataMatrix accept bracketed (01)GTIN(17)YYMMDD(10)lot; use make_qr for QR codes. |
| `make_qr` | Make an SVG QR code for text, a URL, or Wi-Fi network details. |
| `make_run_loop` | Make walking/running loops that start and end at one point, each within 3% of the target distance. Returns Google Maps links and an encoded polyline. Routes and map data © OpenStreetMap contributors (ODbL); routing and elevation: Valhalla on FOSSGIS servers. |
| `margin_calculator` | Calculate cost, selling price, gross profit, margin percentage and markup percentage from two independent values including cost or price. |
| `mass_volume_convert` | Convert mass to volume or reverse with named units and either a USDA FoodData Central ingredient cup-weight preset or an entered positive density in g/mL. |
| `mulch_calculator` | Calculate mulch layer volume and whole 2 cu ft and 3 cu ft bag counts from rectangle dimensions, circle diameter or total area and depth in inches. |
| `one_rep_max_calculator` | Calculate Epley and Brzycki one-rep maximum estimates from lifted weight and repetitions. |
| `pace_calculator` | Calculate running distance, elapsed time or pace from exactly two values and distance units. |
| `page_check` | Check whether one public HTML page shows content. Returns working, suspect or broken, findings with reasons and bounded snippets, status, final URL and text length. No JavaScript rendering; 10 seconds overall, 2 MB HTML. Public HTTP/HTTPS ports 80/443 only. |
| `page_to_markdown` | Read one public HTML page as clean Markdown with title, headings, lists, tables and absolute links. No logins, paywalls or JavaScript rendering; 2 MB HTML limit. |
| `paint_quantity` | Calculate paint volume and whole containers from entered area or supported surface geometry, openings, whole coats and user-supplied per-coat coverage. |
| `pay_convert` | Convert gross annual salary to hourly pay or hourly pay to annual salary using your entered weekly hours and paid weeks. Free arithmetic in your browser. |
| `percentage_calculator` | Calculate X percent of Y, X as a percentage of Y, or signed percentage change from X to Y. |
| `pickleball_court_cost` | Returns rulebook footprints and one-court fit in either orientation, separate cost cards, and unpriced scope. Cost cards are public city project and planning figures, not a price for this court. Pure rules and Decimal, no network, model or clock. Web and MCP share the free daily allowance. |
| `pole_barn_cost` | Returns national construction ranges for the building only, with no published typical figure. Site work/slab/doors/height/permits are not priced. use=residential adds the separate living-space build-out band with an open top and a combined planning estimate. Includes an unpriced checklist, two separate unscaled reference cards and dated sources. Pure arithmetic, no network or model. |
| `power` | Compute a real number raised to an entered exponent with bounded inputs and explicit domain errors. |
| `prime_number_checker` | Compute deterministic primality below 3.3 × 10^24 using the 13 prime Miller–Rabin bases through 41, plus complete factorization through 10^12 or a smallest factor through 10000. |
| `proofread` | Fix spelling, grammar, punctuation and word choice while keeping meaning and voice; needs your OpenRouter key. |
| `pythagorean_theorem_calculator` | Compute the third right-triangle side from exactly two measured sides, both acute angles, the right angle and area using the Pythagorean theorem. |
| `quadratic_solve` | Solve ax² + bx + c = 0 from entered coefficients. See real or complex roots, the discriminant and linear or constant cases, free in your browser. |
| `ratio_calculator` | Simplify decimal A:B ratios, solve A:B = C:?, or scale the ratio to a target term or total. |
| `read_barcode` | Read every barcode in a base64 PNG, JPEG or WebP (or data URL). At most 2 MB decoded and 4000 by 4000 pixels. Returns text, format, corner positions and GS1 product number, expiry and lot when present. |
| `recall_check` | Search local U.S. CPSC data for up to 10 recall notices that may match — check the notice. May not cover every batch or country; read the notice. No CPSC endorsement. |
| `resume_gap` | Compare résumé skills with Columbus, Ohio job postings. Résumé is not stored; full check and rewrite at https://jobs.cowerx.dev. |
| `retirement_drawdown` | Arithmetic on entered numbers only: level end-of-period withdrawal, total withdrawn and complete period table from a balance, fixed entered nominal annual return and term. Monthly, quarterly or annual periods; nearest-cent half-up rounding; final withdrawal clears residue. Rates are entered, never fetched. |
| `roi` | Compute net gain and return on investment percentage from entered cost and final value, with optional annualization. |
| `roman_numeral` | Convert whole numbers from 1 to 3999 to canonical Roman numerals, or convert canonical Roman numerals to numbers. |
| `roof_replacement_cost` | Calculates optional shingle purchase allowance, historical asphalt installation and matched removal scenarios, verified historical standing-seam bid endpoints, and a benchmark subtotal with your separately quoted extras; missing local prices remain get a local quote. |
| `round_decimal` | Round decimal strings exactly to decimal places, tens, hundreds or other powers of ten. Choose half away from zero or half even, including negative ties. |
| `round_sig_figs` | Round a decimal string to a chosen number of significant figures using exact decimal half-up rounding; return plain and scientific notation. |
| `scientific_evaluate` | Evaluate arithmetic, powers, roots, logs and trigonometric functions with parentheses. Choose degrees or radians and get finite real results in your browser. |
| `scientific_notation` | Normalize decimal strings to scientific notation or expand exponent notation exactly. Keep all entered numerical digits without binary float conversion. |
| `seo_check` | Check one public HTML page with fixed SEO rules. Returns schema 1, score, strengths, ranked fixes and facts. No JavaScript rendering; 10 seconds overall, 2 MB HTML and at most 20 links. Public HTTP/HTTPS ports 80/443 only. |
| `simplify_sqrt` | Rewrite the square root of an integer from 0 to 10^12 as a√b using exact integer factors. |
| `slope_calculator` | Compute slope, y-intercept, slope-intercept and point-slope equations, distance, midpoint and line inclination from two distinct points, including vertical lines. |
| `square_footage_calculator` | Computes and sums rectangle, circle, triangle and L-shaped room areas in square feet and square metres. |
| `time_card_calculator` | Sum up to seven clock-time shifts and optionally split the total into regular minutes and minutes past 40 hours. |
| `tip_calculator` | Calculate a bill tip and equal per-person shares, with cent rounding or optional whole-dollar rounding up. |
| `unit_convert` | Convert a bounded decimal or fraction quantity between explicit compatible mass, volume, international length, speed or item-count units. Reject incompatible dimensions; no density is inferred. |
| `unit_price` | Compare package prices per equal mass, volume or whole item count in one entered currency, with exact tie detection and compatible units only. |
| `volume_calculator` | Computes cube, box, cylinder, cone, sphere or rectangular-pyramid volume with its formula and cubic-unit conversions. |
| `water_softener_size` | Gallons per person per day is required (no national default used), for softened water only. Iron is optional; unknown when absent, and changes the setting per EcoPure's clear-water ferrous iron rule (5 gpg per ppm); other makers differ. Returns grains per day, working capacity before reserve, optional paired model ratings, three idealized EP42 test-rating examples, notes, assumptions and dated primary sources. Costs are salt only. Pure Decimal arithmetic, no network or model. |
| `wheelchair_ramp` | Returns the minimum horizontal run under ADA 2010 §405.2, cited width, landing, rise-per-run and handrail dimensions, and separate historical HUD accessibility cost cards with missing price cells visible. This is a planning guide, not a code inspection. |
| `word_count` | Count words, characters, sentences and paragraphs and estimate reading and speaking times from text. |
| `yard_drainage_cause` | Returns likely causes to investigate, not a diagnosis, with explainable observed-code rules, safety escalations, options and who does them. Prices are dated public planning estimates, with distinct scopes and source years; no 2026 price adjustment. Omit unknown groups; [] means none observed. Optional numbers price only agreed areas, designed storage or counted downspout sets; the soil check screens root-zone drainage. No network or model. Web and MCP share the free daily allowance. |
| `z_score` | Compute the standardized z score from an entered value, mean and positive standard deviation. |

Input schemas come from `get_tool_schema(name=...)` on `/mcp`, or the full listing at `https://apitoolcalls.com/mcp?tools=all`.

## Limits and errors

Without an [API Tool Calls](https://apitoolcalls.com) key: 20 tool calls per IP per UTC day, shared across tools. Free calls also share a global ceiling of 2,000 per UTC day; recall has no separate tool cap.
Agent calls have no [API Tool Calls](https://apitoolcalls.com) charge; no key is sold. The proofreader requires your OpenRouter key and bills the provider request to you. Existing keys still work: 1,000 calls per UTC month, shared across tools.
Validated calls can count even if processing fails.

Proofreader validation and provider errors arrive as MCP `result.isError` with text content, even with HTTP 200. A missing OpenRouter key spends no free call.

Other MCP errors arrive as JSON-RPC `error.code` and `error.message`, even with HTTP 200:

| Code | Meaning / typical message |
| --- | --- |
| `-32602` | Invalid arguments; message names the field or unknown tool. |
| `-32000` | Free daily limit reached; the message says it resets at midnight UTC. |
| `-32001` | Unknown, invalid or inactive [API Tool Calls](https://apitoolcalls.com) key. |
| `-32002` | `Monthly key limit reached (1,000 calls this UTC month).` |
| `-32003` | Captions disabled/missing, unavailable video, résumé input/data error, or unreadable/blocked/oversize HTML page; read the message. |
| `-32004` | `YouTube did not answer; try again later`, `Résumé check is unavailable; try again later`, `Could not read this page; try again later`, `Data Finder is unavailable; try again later`, or `Recall data is updating, try later`. |

For a key the user already has, add the HTTP header
`Authorization: Bearer ot_live_...` in the client's MCP configuration.
Keep the key in client credentials or environment settings, outside tool arguments.
For tools without BYOK, free access omits the Authorization header. Proofreader requests still require X-OpenRouter-Key. Agent tool information is at
`https://apitoolcalls.com/api/`. Client setup is documented in the pack README.
