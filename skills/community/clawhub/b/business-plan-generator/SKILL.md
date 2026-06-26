# Business Plan Generator

**Category:** Business & Entrepreneurship  
**Version:** 1.0.0  
**Author:** max_0x1  
**License:** MIT-0

## What This Skill Does

Generates investor-ready business plan sections from your startup or small business idea. Four targeted prompts cover every component a bank, investor, or accelerator needs to see — from executive summary through financial projections.

Stop paying $2,000–$10,000 for a business plan writer. Generate a professional-grade plan in under an hour.

## Prompts

### 1. `executive-summary.md`
Generates a 1–2 page executive summary: problem/solution, target market, value proposition, business model, traction, funding ask, and vision statement.

**Input:** Business name, industry, what problem it solves, how it solves it, target customer, revenue model, stage (idea/pre-revenue/revenue), funding needed (optional)

### 2. `market-analysis.md`
Generates market analysis + competitive landscape: TAM/SAM/SOM sizing, target customer persona, 5–7 competitor comparison matrix, competitive advantages, market trends.

**Input:** Business name, industry, product/service, target geography, known competitors (optional)

### 3. `financial-projections.md`
Generates 3-year revenue model + financials: pricing assumptions, revenue streams, Month 1–12 monthly projections, Year 2–3 annual projections, break-even analysis, key financial assumptions.

**Input:** Business name, revenue model (subscription/one-time/usage/services), pricing tiers, estimated CAC, estimated monthly overhead, funding amount (if any)

### 4. `operations-gtm.md`
Generates operations plan + go-to-market strategy: team/roles, tech stack or operational requirements, GTM channels, 90-day launch plan, key milestones, risk factors + mitigations.

**Input:** Business name, founding team (roles/backgrounds), product/service delivery method, primary sales channels, launch timeline

## Pricing

- **Free tier:** Executive Summary prompt only
- **Pro:** All 4 prompts — $29 one-time
- **Done-For-You:** Full business plan written for your business — $197

## Who This Is For

- Entrepreneurs writing their first business plan
- Founders applying for SBA loans or bank financing
- Startups pitching angel investors or accelerators (YC, Techstars)
- Small business owners applying for grants
- MBA students building business plan projects
- Freelancers pitching corporate clients with formal proposals

## Example Output

See `examples/fittrack-saas/` — complete business plan for FitTrack, a SaaS platform for personal trainers. All 4 sections included.

## Usage

Copy any prompt file, fill in the `[BRACKETS]`, and run in Claude. Each prompt is self-contained — use all four for a complete plan or pick the sections you need.
