# Metrics and periods

## Revenue layers

Define the exact layer used in each visual. Common layers are gross merchandise value, list amount, customer-paid amount, refunds, net paid amount, platform settlement, recognized revenue, cost, gross profit, and contribution profit.

Do not call `(revenue - ingredient cost) / revenue` a generic profit margin when only ingredient cost is available. Use `毛利率` only when the business definition supports it, and state the included costs.

## Core metrics

- Net revenue = eligible paid amount minus eligible refunds, adjusted only by documented accounting rules.
- Average order value = net revenue divided by valid completed orders.
- Purchase frequency = valid completed transactions divided by identifiable active customers in the period.
- New customer = first observed valid transaction within the available identity history, not merely first transaction inside the filter.
- Returning customer = an identifiable active customer whose first observed transaction predates the period or who has a later repeat under the defined view.
- Next-month retention = new customers in month M who make a valid transaction in M+1 divided by identifiable new customers in M. The last month has no complete observation window.
- Repeat rate and retention are different. Name the metric precisely.

Domain metrics such as utilization, conversion, churn, renewal, sell-through, and project margin require valid denominators. Do not calculate them from incomplete proxy data without labeling the proxy.

## Period behavior

- Use month selectors by default.
- If start month equals end month, remove monthly comparison panels. Show compact structure, ranked bars, share, within-month weekday or daypart patterns, and available comparison cards only when a valid preceding period exists.
- If two or more months are selected, show one point per month for core trends and customer changes.
- Compare the selected period with the immediately preceding period of equal month count.
- Add year-over-year comparison only when every matching prior-year month is sufficiently complete.
- Partial months must be labeled and compared only with aligned elapsed days when the comparison is useful.

## Driver decomposition

Explain changes with an additive or otherwise reconcilable framework. Examples:

- Revenue change: order volume effect + average order value effect + interaction.
- Customer revenue: active-customer effect + frequency effect + average order value effect + interaction.
- Net settlement: gross paid change - refund change - merchant discount change - platform fee change, using the source's accounting definitions.

Show a waterfall when the components reconcile. Use a concise ranked driver view when they do not. Never place unrelated percentage changes into a single additive chart.

## Chart axes

- Bars start at zero unless the chart explicitly represents a signed change around zero.
- Lines may use a non-zero lower bound when it improves readability; keep axis ticks, units, and the scale visible so the change is not misleading.
- Use a second axis only for different units, such as revenue bars plus growth-rate line. Label both axes and combine the tooltip by x-value.
