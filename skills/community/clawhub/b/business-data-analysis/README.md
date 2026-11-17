# Business Data Analysis Skill

Transform raw order data into **interactive HTML analysis reports** with 6 tabs covering trends→comparison→time slots→users→traffic→operations, supporting desktop and mobile.

## Features

- 📊 **Overall Trends** - Daily average revenue line chart, orders+users dual-axis bars, frequency stack, new/old user stack, retention rate
- 🔍 **Monthly Comparison** - 5-period monthly comparison cards, daily avg orders/revenue, time slot breakdown, weekday/weekend analysis
- ⏱ **Time Analysis** - 5-period monthly line charts, heatmap, time slot bars, insight panels
- 👤 **User Structure** - New/old user stacked bars, frequency distribution, retention rate, active old user rate
- 📍 **Review Traffic** - Enabled: source pie + conversion funnel + deal table / Not enabled: status + analysis
- 🎯 **Operations Plan** - 3+3 strategy cards (P0/P1/P2) + competitor comparison

## Use Cases

- Venue operations (badminton/tennis/basketball/swimming)
- Restaurant stores
- Retail orders
- Service appointments
- Any business with order records

## Supported Data Formats

- Format: `.xlsx` / `.csv`
- Required fields: order date, order amount, user ID (phone/user ID)
- Optional fields: venue/product/service type, time slot, order status, discount amount

## Color Themes

5 preset themes available:
1. Purple-Blue (Premium/Sports)
2. Orange-Green (Vibrant/Venue)
3. Deep Blue (Tech/Finance)
4. Beige-Brown (Elegant/Restaurant)
5. Dark (Night/Luxury)

Also supports extracting main colors from logo images.

## Core Calculation Standard

All monthly comparisons use **full-month daily average** - no half-month or equal-length截取 comparison.

## Usage

1. Provide order Excel/CSV data file
2. Choose color theme (preset or custom)
3. Explain business scenario (has Dianping store or not)
4. AI automatically generates interactive analysis report

## Example

Full example: `references/example-badminton.html` — Xingchen Badminton Center, purple theme, 6 tabs

## Tech Stack

- Python (Pandas) - Data processing
- Chart.js - Data visualization
- HTML/CSS - Responsive reports

## License

MIT License
