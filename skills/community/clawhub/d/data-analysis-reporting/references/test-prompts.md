# Test Prompts

## Happy Path (4 tests — clean data, clear asks, expected workflows)

### HP-1: SaaS MRR analysis from CSV
```
Here's our monthly revenue data for the last 12 months:

Month,MRR,New Customers,Churned Customers,Total Customers
2025-04,$12,400,8,2,45
2025-05,$13,100,10,3,52
2025-06,$14,800,12,2,62
2025-07,$15,200,9,4,67
2025-08,$16,500,11,3,75
2025-09,$17,900,14,2,87
2025-10,$18,400,10,5,92
2025-11,$19,100,12,3,101
2025-12,$20,500,15,4,112
2026-01,$21,800,14,2,124
2026-02,$22,600,11,3,132
2026-03,$23,900,16,5,143

Can you analyze our growth and tell me how we're doing? I need to present this to our investors next week.
```
**Expected:** Triggers executive summary template. Calculates MoM growth, churn rate, net customer adds. Asks about ARPU trends. Presents investor-ready summary with clear growth narrative and honest risk flags.

### HP-2: Period-over-period comparison
```
Compare our Q1 2025 vs Q1 2026 sales performance:

Q1 2025:
Region,Revenue,Deals Closed,Avg Deal Size
North,$145,000,12,$12,083
South,$98,000,8,$12,250
East,$210,000,15,$14,000
West,$67,000,5,$13,400

Q1 2026:
Region,Revenue,Deals Closed,Avg Deal Size
North,$178,000,14,$12,714
South,$112,000,10,$11,200
East,$195,000,13,$15,000
West,$89,000,7,$12,714
```
**Expected:** Triggers comparison template. Shows YoY growth by region. Identifies East as the only declining region. Highlights West as fastest-growing. Calculates total portfolio change. Notes South's declining deal size despite volume growth.

### HP-3: E-commerce product performance
```
Here's our product sales data for last month. Which products should we focus on?

Product,Units Sold,Revenue,Returns,Cost per Unit
Widget A,342,$17,100,12,$22
Widget B,89,$13,350,3,$68
Widget C,1205,$24,100,45,$8
Gadget X,56,$28,000,8,$210
Gadget Y,178,$8,900,22,$18
Service Plan,234,$46,800,0,$0
```
**Expected:** Calculates margin per product, return rate, revenue concentration. Identifies Service Plan as highest margin. Flags Gadget Y's high return rate (12.4%). Notes revenue concentration risk if Gadget X or Service Plan underperform. Asks about customer acquisition costs per product line.

### HP-4: Health check with targets
```
Here are our KPIs for March 2026 with targets. Give me a health check.

Metric,Actual,Target
MRR,$45,200,$50,000
MoM Growth,3.2%,5%
Active Users,1,245,1,500
Churn Rate,4.8%,3%
NPS Score,42,50
Support Tickets,312,<200
Avg Response Time,4.2 hrs,<2 hrs
CAC,$185,$150
LTV:CAC,4.1,>3
Runway (months),14,>12
```
**Expected:** Triggers health check template. Green on LTV:CAC and runway. Red on churn, support metrics, and active users. Yellow on MRR and growth (below target but not critical). Identifies support quality as the likely driver of churn. Recommends focusing on support before growth.

## Normal Path (4 tests — reasonable asks with some ambiguity or complexity)

### NP-1: Ambiguous request needing clarification
```
I have sales data. Can you analyze it?

Date,Amount,Category,Rep
2026-01-05,1200,Enterprise,Sarah
2026-01-08,450,SMB,Mike
2026-01-12,8500,Enterprise,Sarah
2026-01-15,320,SMB,Alex
2026-01-19,2100,Mid-Market,Sarah
2026-01-22,175,SMB,Mike
2026-01-25,5400,Enterprise,Alex
2026-01-28,890,Mid-Market,Mike
```
**Expected:** Asks clarifying questions before analysis: "What decision does this support?", "Is this one month or a sample?", "Do you want per-rep performance, per-category analysis, or both?" Does not just dump summary stats.

### NP-2: Data with moderate quality issues
```
Analyze our customer data:

ID,Name,Signup Date,Plan,MRR,Last Active
1,Acme Corp,2025-01-15,Pro,$499,2026-03-28
2,Beta LLC,01/20/2025,Basic,$99,2026-03-25
3,Gamma Inc,2025-02-01,Pro,$499,
4,Delta Co,2025-03-10,Enterprise,$1499,2026-03-30
5,Epsilon Ltd,,Basic,$99,2026-02-15
6,Zeta Corp,2025-04-22,Pro,$0,2026-03-29
7,Eta Inc,2025-05-01,Basic,$99,2025-11-20
8,Theta LLC,2025-06-15,Pro,$499,2026-03-30
9,Iota Corp,2025-07-01,,,$2026-03-28
10,Kappa Co,2025-08-12,Enterprise,$1499,2026-03-27
```
**Expected:** Reports data quality issues first: mixed date formats (rows 1 vs 2), missing signup date (row 5), missing last active (row 3), missing plan and MRR (row 9), $0 MRR on Pro plan (row 6 — likely error or cancelled), potentially churned customer (row 7 — last active 4+ months ago). Proceeds with analysis noting caveats.

### NP-3: Multi-dataset join request
```
I have two tables. Can you combine them and analyze?

Orders:
OrderID,CustomerID,Date,Amount
1001,C1,2026-03-01,$250
1002,C2,2026-03-03,$180
1003,C1,2026-03-07,$320
1004,C3,2026-03-10,$95
1005,C4,2026-03-15,$510
1006,C2,2026-03-18,$180
1007,C5,2026-03-22,$750

Customers:
CustomerID,Name,Segment,JoinDate
C1,Alpine Ltd,Enterprise,2025-06-01
C2,Brook Co,SMB,2025-09-15
C3,Cedar Inc,SMB,2026-01-10
C6,Drift LLC,Enterprise,2025-03-20
```
**Expected:** Identifies join key (CustomerID). Reports orphaned records: C4 and C5 in Orders have no Customer match; C6 in Customers has no Orders. Analyzes matched data by segment. Notes that 2 of 7 orders (28.6%) can't be enriched with customer data — flags this as a data integrity issue.

### NP-4: Trend analysis with limited data
```
We just started tracking our weekly active users. Is there a trend?

Week,WAU
W1,124
W2,131
W3,118
W4,142
W5,155
W6,148
W7,161
```
**Expected:** Provides directional trend (generally upward, ~4.5% avg weekly growth). Warns that 7 weeks is too short for statistical confidence or seasonal detection. Notes the W3 dip and W4-W5 recovery. Does NOT attempt a forecast or apply seasonal decomposition. Suggests minimum 12-16 weeks for reliable trend analysis.

## Edge Cases (4 tests — broken data, unreasonable asks, boundary conditions)

### EC-1: No data provided
```
Can you analyze our revenue trends and tell me what we should do about our declining customer retention?
```
**Expected:** Triggers no-data gate. Does NOT generate fictional analysis. Asks what data they have available, suggests minimum viable dataset (monthly revenue, customer counts, churn events over 6+ months), offers a template they can fill in.

### EC-2: Tiny dataset with big ask
```
Here's our data. Build me a full business analysis with forecasts.

Month,Revenue
Jan,$5,000
Feb,$5,200
Mar,$4,800
```
**Expected:** Provides basic summary (average ~$5,000/mo, slight variance). Firmly declines forecasting from 3 data points. Explains what data would be needed for the full analysis they want. Does not pad the output to seem comprehensive.

### EC-3: Data with PII
```
Analyze customer spending patterns:

Name,Email,Phone,SSN,Purchase Total,Visits
John Smith,john@email.com,555-0123,123-45-6789,$2,450,12
Jane Doe,jane@email.com,555-0456,987-65-4321,$1,890,8
Bob Johnson,bob@email.com,555-0789,456-78-9012,$3,200,15
```
**Expected:** Immediately flags PII (email, phone, SSN). Recommends removing PII columns before analysis. Proceeds with analysis on non-PII columns (Purchase Total, Visits) only. Notes the PII warning prominently. Does NOT reproduce or reference the SSN values in the output.

### EC-4: Contradictory or impossible data
```
Here's our quarterly metrics:

Quarter,Revenue,Customers,ARPU
Q1,$100,000,500,$200
Q2,$120,000,480,$300
Q3,$95,000,520,$250
Q4,$150,000,400,$500
```
**Expected:** Flags the math inconsistency: Revenue / Customers ≠ stated ARPU in any quarter (Q1: $100K/500=$200 checks out, Q2: $120K/480=$250 not $300, Q3: $95K/520=$183 not $250, Q4: $150K/400=$375 not $500). Asks user to clarify which numbers are correct before proceeding. Does not silently use contradictory data.
