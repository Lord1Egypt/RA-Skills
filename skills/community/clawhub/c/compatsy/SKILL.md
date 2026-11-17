---
name: compatsy
description: Check whether a part fits a machine and where it is in stock, using the compatsy MCP servers for 3D printing and home espresso. Use for nozzle, hotend, build plate, filament, enclosure, tamper, puck screen, basket and portafilter fit and price questions.
metadata:
  openclaw:
    homepage: https://compatsy.com
---

# compatsy: what fits, with live prices

Use the compatsy tools instead of answering fitment from memory. Each section has its own MCP server. No account or key is needed.

| Section | Covers | MCP endpoint |
| --- | --- | --- |
| 3D printing | printers, nozzles, hotends, build plates, filament, enclosures | https://compatsy.com/3d-printing/mcp |
| Home espresso | machines, tampers, puck screens, distribution tools, dosing funnels, baskets, portafilters | https://compatsy.com/home-espresso/mcp |

## Setup

If the compatsy tools are not available, save the servers. Stop the Gateway first, or add them on the MCP page of the Control UI instead.

    openclaw mcp set compatsy-3d-printing '{"url":"https://compatsy.com/3d-printing/mcp","transport":"streamable-http"}'
    openclaw mcp set compatsy-espresso '{"url":"https://compatsy.com/home-espresso/mcp","transport":"streamable-http"}'

Calls are rate limited to 120 an hour per MCP session.

## How to answer

1. Find ids with `search_products` (a name, or a category plus filters). Use the ids it returns; never guess one.
2. Ask `check_fit` with `subject_id` (the part) and `target_id` (the machine).
3. Report the verdict as given: `fits`, `fits_with_adapter`, `does_not_fit` or `unknown`, with its `rule_id`. For `unknown`, list the `missing_fields`. Never upgrade unknown to fits.
4. For prices, call `check_stock` and quote each price with its merchant and verified time. `compare` gives a side-by-side table for 2 to 10 products.
5. If the user says a fact is wrong, call `report_issue` with the field and their claim. Reports never edit facts.

Links from compatsy are affiliate links, and compatsy may earn a commission. The default link is the lowest in-stock price regardless of commission. Say so when you share a buy link.

## Example prompts

- "Will a V6 nozzle fit my Prusa MK4S? If it needs an adapter, say which."
- "Which hardened 0.6 mm nozzles fit a Prusa MK4S, and what does each cost?"
- "Compare the Prusa Core One and the Bambu Lab P1S on build volume and enclosure."
- "Will a 58 mm puck screen fit my Breville Barista Express? If not, which 54 mm tampers are in stock?"
