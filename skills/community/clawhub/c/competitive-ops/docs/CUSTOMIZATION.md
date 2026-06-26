# Customization Guide

## Profile (config/profile.yml)

This is the single source of truth for your company. All modes read from here.

Key sections:
- **company**: Name, website, product, target market
- **analysis**: Competitor archetypes, scan frequency
- **outputs**: Report formats, design system
- **competitors**: List of competitors to track

## Competitor Archetypes (config/profile.yml)

The archetype list determines how competitors are categorized:
- **Direct Competitor**: Same target market, similar product
- **Indirect Competitor**: Different approach, same customer needs

## Data Sources (config/sources.yml)

Configure which sources to use for competitive intelligence:
- **tavily**: AI-powered search (API key required)
- **company_website**: Direct competitor website analysis
- **g2**: User reviews and ratings
- **glassdoor**: Company culture and employee insights
- **linkedin**: Company information and hiring trends

## Pricing Alerts (config/pricing-alerts.yml)

Configure pricing monitoring:
- **frequency**: How often to check for price changes
- **threshold**: Minimum change percentage to trigger alert
- **sources**: Priority order for pricing data

## Change Detection (config/change-detection.yml)

Configure what changes to monitor:
- **pricing**: Price changes above threshold
- **features**: New or removed features

## Report Templates (templates/report/)

Customize report output:
- **markdown/**: Markdown report templates
- **html/**: HTML report templates

## Modes (modes/)

Skill modes for different operations:
- **add-competitor.md**: Add new competitor workflow
- **analyze.md**: Competitive analysis workflow
- **report.md**: Report generation workflow
- **diff.md**: Change detection workflow
- **pricing.md**: Pricing monitoring workflow
