# Business routing and analysis modes

Choose modules after inspecting the data. Business mode controls the questions, metrics, chart types, page vocabulary, and visual tone.

## Food, beverage, and local retail

Core questions: revenue quality, orders, average ticket, product mix, discounts, gross margin, daypart, weekday, channel, new and returning customers, frequency, and retention.

Useful modules: overview, product operations, customers, channels, time patterns, stores, and action plan. Use menu, SKU, category, size, add-on, dine-in, pickup, and delivery language only when present.

## Venue, class, reservation, and service businesses

Core questions: bookings, recognized revenue, utilization, capacity, cancellations, peak slots, weekday-hour patterns, repeat bookings, membership, package consumption, instructor or resource productivity.

Useful modules: overview, booking and capacity, customers or members, time slots, resources, channels, and action plan. A weekday-hour heatmap or hourly curves can be more valuable than a product ranking.

## Ecommerce and marketplace retail

Core questions: GMV, paid revenue, net revenue, conversion where traffic exists, refunds, discounts, platform fees, contribution margin, SKU and category mix, customer acquisition source, repurchase, and inventory risk.

Useful modules: overview, merchandise, customers, acquisition and channels, refunds, inventory, and action plan. Distinguish order time, payment time, fulfillment time, and refund time.

## Subscription, membership, SaaS, and recurring services

Core questions: new revenue, recurring revenue, activation, renewal, churn, cohort retention, plan mix, expansion and contraction, account health, and acquisition efficiency.

Useful modules: overview, revenue movement, cohorts, customers or accounts, plans, acquisition, and action plan. Do not force order-frequency charts onto subscription records.

## B2B, project, and lead-based businesses

Core questions: pipeline, stage conversion, sales cycle, win rate, recognized revenue, receivables, customer concentration, project margin, delivery status, and renewal.

Useful modules: overview, funnel, customers, projects, sales channels, collections, and action plan. Respect the difference between contracted, invoiced, collected, and recognized revenue.

## Generic transaction mode

Use this mode when the domain is unclear. Infer entities and propose neutral modules from the available fields. Use business-neutral labels until the data establishes the domain.

## Routing rules

- A field's presence does not guarantee its quality. Check null rate, uniqueness, status coverage, and time coverage.
- Combine modes when appropriate, such as cafe plus membership or venue plus ecommerce.
- Omit unsupported modules. Never fill missing modules with fabricated examples.
- Match visual tone to the business and brand: warm editorial for hospitality, clean commerce for retail, energetic spatial views for venues, and compact technical layouts for SaaS or B2B. Brand evidence overrides these defaults.
