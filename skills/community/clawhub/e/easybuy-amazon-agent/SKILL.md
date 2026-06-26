# EasyBuy Skillpack

This SKILL.md describes the skills included in this pack and how to use them.

## Skills
- `order_reader`
- `evidence_builder`
- `message_drafter`
- `form_filler`
- `amazon_product_detector`
- `amazon_orders_scraper`
- `amazon_orders_opener`
- `amazon_order_details_fetcher`
- `amazon_price_checker`
- `amazon_review_scraper`
- `amazon_contact_flow`
- `message_monitor`
- `price_alert_manager`
- `case_exporter`

## Registry
- `dist/skills/registry.json` lists all skills and their JSON files.

## Usage
- Load the MV3 extension from `dist/` (Chrome -> Extensions -> Developer Mode -> Load unpacked).
- Skills are invoked via the agent runtime using tool name `skill.<skill_name>`.
- Each skill defines `allowedTools`, `input_schema`, and `output_schema` in its JSON file.

## Playbooks
- Playbooks in `dist/playbooks/` declare intent-only steps and `requires_skills`.

## Requirements
- Chrome (MV3-capable)
- Amazon login for live flows
- Permissions: `tabs`, `scripting`, `storage`, `downloads`, `sidePanel`, `activeTab`
