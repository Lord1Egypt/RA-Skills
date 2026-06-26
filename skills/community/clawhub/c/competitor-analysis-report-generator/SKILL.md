---
name: competitor-analysis-report-generator
version: 1.0.0
description: |
  Generate comprehensive competitive analysis reports with data-driven insights. Analyzes competitors across multiple dimensions: products, pricing, marketing, and technology. Produces actionable strategic recommendations with SWOT analysis. Supports Markdown, PDF, and PPT export formats.
tags: ["competitor-analysis", "market-research", "swot", "business-intelligence", "strategy", "reporting"]
---

# Competitor Analysis Report Generator

> 📊 Generate professional competitive analysis reports with data-driven insights

## Skill Overview

This skill helps AI Agents generate comprehensive competitive analysis reports. By analyzing competitor information from multiple dimensions (products, pricing, marketing, technology), it produces actionable insights and strategic recommendations. Ideal for market research, business planning, and strategic decision-making.

## Core Capabilities

- **Multi-source Data**: Combine web search, API data, and public information
- **Multi-dimensional Analysis**: Products, pricing, positioning, marketing, technology
- **Visual Reports**: Auto-generate charts, tables, and infographics
- **Actionable Insights**: Provide specific strategic recommendations
- **Format Options**: Markdown, PDF, PPT, and custom formats

## Trigger Keywords

- `/competitor-analysis`
- `/competitive-research`
- `/market-analysis`
- `/swot-analysis`
- `/industry-research`
- `/competitor-brief`

## How to Use

### Basic Usage

```
User: Generate a competitor analysis report for Tesla
Agent: 🔍 Starting competitor analysis...
     
     ✅ Analysis complete!
     
     # Tesla Competitive Analysis Report
     
     ## Executive Summary
     Tesla dominates the EV market with brand power, 
     technology advantages, and vertical integration...
     
     ## Competitor Overview
     | Competitor | Market Share | Key Products | Strengths |
     |------------|-------------|--------------|----------|
     | BYD | 18% | Han, Seal | Battery tech, cost |
     | NIO | 8% | ES6, ES8 | Premium service |
     | Rivian | 5% | R1T, R1S | Adventure focus |
```

### Advanced Usage

```
User: Generate a detailed competitive analysis for the smartphone market
      Competitors: Apple, Samsung, Google, OnePlus, Xiaomi
      Focus: Global market, Q4 2024
      Output: Comprehensive report with SWOT

Agent: 🔍 Generating comprehensive analysis...
     
     ✅ Report generated successfully!
     
     # Smartphone Market Competitive Analysis
     Global Market | Q4 2024
     
     ## Market Overview
     - Total Market Size: 320 million units
     - YoY Growth: -3%
     - Market Concentration: Top 5 = 85%
     
     ## Competitor Profiles
     [Full analysis for each competitor]
     
     ## SWOT Analysis Matrix
     [Comprehensive SWOT]
     
     ## Strategic Recommendations
     [Actionable strategies with priorities]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| industry | Yes | Industry or product category |
| competitors | No | Specific competitors to analyze |
| market | No | Geographic market focus |
| time_period | No | Analysis time period |
| output_format | No | Report format: markdown/pdf/ppt |

## Analysis Dimensions

### 1. Product Analysis

| Metric | Description |
|--------|-------------|
| Product Portfolio | Product lines and positioning |
| Feature Comparison | Core features matrix |
| Innovation Rate | New product launch frequency |
| Quality Assessment | User ratings and reviews |
| Price Range | Product line distribution |

### 2. Market Analysis

| Metric | Description |
|--------|-------------|
| Market Share | Revenue and unit market share |
| Growth Rate | YoY and QoQ growth |
| Geographic Distribution | Regional market presence |
| Channel Strategy | Sales channel breakdown |
| Target Segments | Customer segment targeting |

### 3. Marketing Analysis

| Metric | Description |
|--------|-------------|
| Brand Awareness | Brand recognition metrics |
| Marketing Spend | Advertising investment |
| Social Presence | Social media engagement |
| Content Strategy | Content themes and frequency |
| Influencer Marketing | KOL and influencer collaborations |

### 4. Technology Analysis

| Metric | Description |
|--------|-------------|
| R&D Investment | R&D spend as % of revenue |
| Patent Portfolio | Patent count and quality |
| Technology Stack | Core technologies |
| Innovation Pipeline | Upcoming technologies |
| Tech Partnerships | Strategic tech partnerships |

## Report Structure

```markdown
# [Industry] Competitive Analysis Report
[Market] | [Time Period]

## Executive Summary
- Key findings (3-5 points)
- Strategic recommendations
- Risk alerts

## Market Overview
- Market size and growth
- Market trends
- Key drivers

## Competitor Profiles
### [Competitor 1]
- Company overview
- Product portfolio
- Market performance
- SWOT analysis

### [Competitor 2]
[...]

## Comparative Analysis
### Feature Matrix
### Price Positioning
### Market Share Trends

## SWOT Analysis
### Strengths
### Weaknesses
### Opportunities
### Threats

## Competitive Landscape Map
[Visual positioning map]

## Strategic Recommendations
### Short-term (0-6 months)
### Medium-term (6-12 months)
### Long-term (12+ months)

## Appendix
- Data sources
- Methodology
- Additional charts
```

## Usage Examples

### Example 1: SaaS Market Analysis

```
User: Generate competitive analysis for project management SaaS
      Competitors: Asana, Monday.com, Notion, Trello, ClickUp
Agent: 🔍 Analyzing SaaS market...
     
     ✅ Analysis complete!
     
     # Project Management SaaS Competitive Analysis
     
     ## Market Overview
     Total Market: $5.2B
     Growth Rate: 15% YoY
     
     | Platform | Market Share | Pricing | Key Differentiator |
     |----------|-------------|---------|-------------------|
     | Asana | 22% | $10.99/user | Workflow automation |
     | Monday | 20% | $9/user | Visual simplicity |
     | Notion | 18% | $8/user | All-in-one workspace |
     | Trello | 15% | $5/user | Kanban simplicity |
     | ClickUp | 12% | $7/user | Feature depth |
     
     ## Key Insights
     1. Notion growing fastest at 35% YoY
     2. Enterprise segment seeing consolidation
     3. AI features becoming table stakes
```

### Example 2: Quick Competitor Brief

```
User: Quick brief for new coffee brand entering the US market
Agent: 🔍 Generating quick brief...
     
     ☕ Quick Competitive Brief: US Coffee Market
     
     **Key Players:**
     1. Starbucks (28% share) - Premium positioning
     2. Dunkin (18% share) - Value + convenience
     3. Peet's Coffee (8% share) - Specialty focus
     
     **Market Opportunities:**
     - Ready-to-drink segment growing 20% YoY
     - Sustainability is top consumer concern
     
     **Recommendations:**
     - Position in premium-but-accessible tier
     - Lead with sustainability story
     - Focus on grab-and-go occasions
```

### Example 3: E-commerce Platform Analysis

```
User: Compare Shopify vs WooCommerce vs BigCommerce
Agent: 🔍 Analyzing e-commerce platforms...
     
     ✅ Analysis complete!
     
     # E-commerce Platform Comparison
     
     ## Feature Comparison
     
     | Feature | Shopify | WooCommerce | BigCommerce |
     |---------|---------|-------------|-------------|
     | Starting Price | $29/mo | Free (plugin $59+) | $29/mo |
     | Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
     | Customization | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
     | SEO | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
     | Scalability | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
     
     ## Positioning Map
     [Ease of Use vs Customization matrix]
     
     ## Recommendations
     - Small business, quick start: Shopify
     - Developers, full control: WooCommerce
     - Growing mid-market: BigCommerce
```

## Data Sources

| Source Type | Examples |
|-------------|----------|
| Public Data | Annual reports, SEC filings, news |
| Market Research | IDC, Gartner, eMarketer reports |
| Social Listening | Brand mentions, sentiment analysis |
| Price Monitoring | Competitor pricing changes |
| User Reviews | App stores, review platforms |

## Report Formats

### Available Formats

| Format | Use Case |
|--------|----------|
| Markdown | Digital sharing, editing |
| PDF | Formal presentation, printing |
| PPT | Investor presentations |
| Excel | Data analysis, further processing |
| JSON | API integration, automation |

### Customization Options

- Executive summary length (1 page / 3 page / full)
- Deep-dive sections (selective depth)
- Visualization preferences (charts, tables, infographics)
- Data freshness (real-time / monthly snapshot)

## Notes

1. **Data Accuracy**: Verify critical data points from multiple sources
2. **Timeliness**: Use most recent data available (标注 data date)
3. **Objectivity**: Present facts without personal bias
4. **Actionability**: Ensure recommendations are practical
5. **Regular Updates**: Update reports quarterly for ongoing tracking

## Use Cases

- 📈 **Market Entry**: Assess competitive landscape before entering new market
- 📊 **Business Planning**: Strategic planning and forecasting
- 💼 **Investor Relations**: Prepare investment theses
- 🚀 **Product Development**: Identify gaps and opportunities
- 📢 **Marketing Strategy**: Positioning and messaging
- 🔍 **Due Diligence**: M&A and partnership evaluation

## Technical Implementation

### Analysis Workflow

```
1. Data Collection
   ├── Web search for public data
   ├── API calls for market data
   └── Structured data compilation
   
2. Data Processing
   ├── Data cleaning and validation
   ├── Cross-reference verification
   └── Gap analysis
   
3. Analysis
   ├── Descriptive analysis
   ├── Comparative analysis
   ├── Trend analysis
   └── Predictive modeling
   
4. Report Generation
   ├── Template selection
   ├── Content filling
   ├── Visualization creation
   └── Quality check
   
5. Output
   ├── Format conversion
   ├── Distribution
   └── Archive
```

## Changelog

### v1.0.0 (2024-01-20)
- Initial release
- Multi-competitor analysis support
- Multiple output formats (Markdown, PDF, PPT)
- SWOT analysis framework
- Strategic recommendations engine

## Author Info

- Author: AI Agent Helper
- Version: 1.0.0
- Framework: OpenClaw
