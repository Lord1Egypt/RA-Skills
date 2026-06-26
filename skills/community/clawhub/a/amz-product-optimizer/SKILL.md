---
name: amz-product-optimizer
description: |
  Use when user wants to optimize Amazon product listings, generate product images, improve titles, monitor CTR, or automate end-to-end Amazon product optimization workflows.
version: "1.0.0"
---


# Amazon Product Optimizer (AMZ Product Optimizer)

## Overview
Automate the complete Amazon product optimization pipeline: hot keyword extraction, title generation, detail image creation, and main‑image click‑through‑rate (CTR) monitoring. Suitable for sellers, product managers, and cross‑border e‑commerce teams.

## Core Workflow
1. **Get Hot Keywords** – Scrape top keywords for the target niche.
2. **Read Product Data** – Load products from a local JSON/CSV file.
3. **Optimize Titles** – Generate fluent titles using the standard structure `[Brand] + [Core Keyword] + [Feature] + [Spec]`.
4. **Generate Detail Images** – Create five scene‑based images via Taobao MCP.
5. **Save Results** – Update the product file with new titles and image URLs.
6. **CTR Monitoring (optional)** – Schedule daily checks of main‑image CTR, flagging products below the 5 % threshold.

## Execution Modes
| Mode | Description | Typical Use |
|------|-------------|-------------|
| `full` | Run the entire pipeline end‑to‑end. | First‑time bulk optimization |
| `keywords_only` | Retrieve hot keywords only. | Market research |
| `optimize_names` | Optimize product titles only. | When titles need refresh |
| `generate_images` | Produce detail images only. | After titles are final |
| `monitor` | Perform CTR monitoring only. | Daily health check |

## Parameters
- **keyword** (string, required) – The niche or product category, e.g. `"cat food"`.
- **product_file** (string, required) – Path to a JSON/CSV containing product records.
- **mode** (string, optional, default `"full"`) – One of the modes above.

## Usage Examples
```text
User: Optimize my cat food listings
Assistant: (mode: full, keyword: "cat food", product_file: "products.json")
```
```text
User: Show me hot keywords for dog beds
Assistant: (mode: keywords_only, keyword: "dog bed")
```
```text
User: Generate detail images for product ID 12345
Assistant: (mode: generate_images, product_file: "products.json", keyword: "cat food")
```
```text
User: Monitor main‑image CTR daily
Assistant: (mode: monitor)
```

## Reference Files
- `references/optimization-guide.md` – Detailed strategies for title optimization, image prompts, and CTR thresholds.
- `scripts/` – Helper scripts for keyword scraping, title generation, image creation, and monitoring (may be added later).

## Notes
- Titles must follow the standard structure and avoid keyword stuffing or "Hot Search" markers.
- Image prompts are scene‑based to maximize conversion.
- CTR threshold recommended at 5 %; adjust via configuration.
- All results are saved back to the provided `product_file`.


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
