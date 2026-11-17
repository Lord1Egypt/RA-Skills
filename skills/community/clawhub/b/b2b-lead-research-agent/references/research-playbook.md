# Research playbook (US B2B)

## 1. Define the ICP before you look at a single account

An ICP that is not written down cannot be scored. Minimum viable definition:

| Field | Example |
| --- | --- |
| Industry | Commercial HVAC services, commercial plumbing, facility management |
| Employees | 20-200 (2-200 field techs) |
| Revenue | $5M-$50M |
| Geography | US, excluding [states] |
| Tech stack | [only if you sell into it] |
| Trigger | Recent: hiring 5+ field techs, new service contract, expansion into a new metro |
| Disqualifier | No field service arm, under 10 employees, franchise-owned with no purchasing authority |

Then answer two questions for a rep:

1. **Why this account?** (one sentence, evidence-backed)
2. **Who do I talk to?** (role, and why that role owns the budget)

If you cannot answer both, the account is Tier C.

## 2. Discovery: where US accounts actually come from

Ranked by signal quality for a US B2B audience:

1. **Your own customers and lost deals** - highest intent, ever.
2. **Public lists you can legitimately work**: conference exhibitor lists, trade
   association member directories, state license and certification registries,
   public procurement portals, SBA dynamic small business search, public award
   announcements.
3. **Public company research**: newsroom, press releases, job postings, careers
   pages, investor relations pages, funding announcements.
4. **Competitor-adjacent**: who else serves the same customer.
5. **Licensed providers**: Apollo, ZoomInfo, Clay, HubSpot Breeze Intelligence,
   RocketReach, Hunter, LinkedIn Sales Navigator (manual, per their terms).

Do not scrape a directory that forbids it, and do not automate a platform that
forbids it.

## 3. The trigger list (US B2B)

The reason to contact today. Without one, you are sending noise.

| Trigger | Where to see it |
| --- | --- |
| Funding round / acquisition | Press release, Crunchbase public page, company newsroom |
| New VP/Director of Sales or Ops | Company leadership page, LinkedIn (manual) |
| Hiring surge in a role you sell into | Public job postings on their careers page |
| New service line or product | Press release, product page changelog |
| Geographic expansion | New location on the contact page, "now serving" language |
| Compliance deadline | Industry-specific (state rules, contract renewals) |
| Contract ending | Renewal cycles, public contracts expiring |
| Tech-stack change | Job postings naming the tool, public integrations page |
| Leadership change | Company newsroom, PR releases |
| Review-site spike | Public review pages (a 5-star surge with recent dates is a signal) |
| Website rebrand or redesign | Their site, their announcement |

## 4. Qualifying questions to answer from public sources

- What do they sell, and to whom?
- How big are they (employees, locations, revenue if public)?
- Who owns the budget for what you sell (role, not personal data)?
- What changed recently?
- Which of their words can you use back to them (their own phrasing from their
  site or press release)?
- Why is now the time?

## 5. Writing the account note

Five fields, one line each:

```
Company      : Northwind Mechanical (Boise, ID)
What they do : Commercial HVAC service and maintenance, 3rd gen family business
Size         : ~140 employees, 4 service areas
Trigger      : Posted 9 field technician roles in 60 days
My angle     : Their dispatch is manual (they post a "dispatcher" role), 4 territories, no self-scheduling
Ask          : 15 minutes on how they schedule techs across 4 territories
```

Keep it under 100 words. A rep should be able to read it in 15 seconds.

## 6. Volume and pace (US B2B, small team)

| Stage | Accounts/day | Messages/day |
| --- | --- | --- |
| Pilot week | 10 researched, 5 contacted | 5 |
| Week 2-3 | 25 researched, 15 contacted | 15 |
| Month 2+ | 50 researched, 30 contacted | 30 |

Quality per message drops fast above ~50 messages/day from one domain. Ramp the
domain reputation first: SPF, DKIM, DMARC aligned, warm the sending mailbox
with real conversations before cold volume.

## 7. Stop conditions

Stop researching and stop sending to an account when:

- the person asks to be removed (permanent suppression)
- the data source turns out to be inaccurate
- the trigger is older than 90 days
- the role you identified does not own the budget
- the account matches a disqualifier
- the deliverability signals go bad (hard bounce rate above 5%)

## 8. What not to research

- Personal social media activity, family, health, finances, location.
- Anything from a breach, dump, or leaked database.
- Personal email addresses not published by a company for business contact.
- Anything a company published for a specific purpose, repurposed for another
  (a support address used for marketing).
