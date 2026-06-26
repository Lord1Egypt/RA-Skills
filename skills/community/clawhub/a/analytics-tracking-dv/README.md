# Analytics & Tracking Setup

Tools for building UTM links, conversion pixels, and attribution tracking for digital products.

## Description

Analytics & Tracking Setup provides utilities for standardized marketing analytics configuration. It includes a UTM link builder for campaign tracking, a catalog of conversion pixel snippets (Facebook, Google Analytics 4, Google Ads), attribution configuration rules (first-touch, last-touch, multi-touch), and a strategic tracking plan template for product instrumentation.

## Key Features

- **UTM link builder** - CLI tool for standardized campaign URL tagging
- **Pixel catalog** - Ready-to-use conversion tracking snippets (FB, GA4, Google Ads)
- **Attribution rules** - Configurable first-touch, last-touch, multi-touch models
- **Tracking plan template** - Strategic framework for product-level instrumentation
- **Campaign consistency** - Enforces naming conventions across marketing channels
- **No code deployment** - Copy-paste pixel snippets for quick setup

## Quick Start

```bash
# Build a UTM-tagged URL
python3 scripts/utm_builder.py \
  --url https://example.com/product \
  --source newsletter \
  --medium email \
  --campaign spring_launch_2025

# Output: https://example.com/product?utm_source=newsletter&utm_medium=email&utm_campaign=spring_launch_2025

# View available pixel configs
cat data/pixel_configs.json

# View attribution rules
cat data/attribution_config.json
```

## Components

- **utm_builder.py** - Generate standardized UTM parameters
- **pixel_configs.json** - Conversion pixel library (FB Pixel, GA4, GADS)
- **attribution_config.json** - Channel attribution model definitions
- **TRACKING-PLAN.md** - Strategic tracking instrumentation guide

## What It Does NOT Do

- Does NOT provide analytics dashboards or reporting (integration only)
- Does NOT handle server-side tracking implementation
- Does NOT verify pixel installation or firing (manual testing required)
- Does NOT manage tag management systems like GTM (template generation only)
- Does NOT track user behavior beyond configured conversion events

## Requirements

- Python 3.8+
- No external dependencies (standard library only)
- Access to marketing platforms for pixel deployment (FB, Google, etc.)

## License

MIT
