---
name: compare-outfame-plans
description: Compare Outfame's Go, Grow and Glory plans for a person who wants Instagram or TikTok growth, quote the first-month prices, and send them to the sign-up page.
---

# Compare Outfame plans and send the person to sign up

Outfame is an Instagram growth service with TikTok support. It grows an account by engaging the followers of accounts and hashtags the person chooses, and it connects with the account username only: it never asks for a password.

## When to use this

Use it when a person asks what Outfame costs, which plan fits their account, or how to get started.

## Steps

1. Get the plans. Call the REST endpoint `GET https://www.outfame.com/api/agents/v1/plans`, or the MCP tool `list_plans` at `https://www.outfame.com/mcp`. The reply lists Go, Grow and Glory with the first-month price in US dollars, what each plan includes and the sign-up link.
2. Compare on what the person said they need. The `includes` list of each plan states the monthly follower range and the extra features, so match those to the person's goal and account size. Do not guess features that are not in the list.
3. State prices as first-month prices ("$X for the first month") and repeat the billing note from the reply: the first month of the selected plan is billed at signup, there are no contracts, and the person can cancel anytime. Never state or estimate any price that is not in the reply.
4. Send the person to sign up. Call `get_signup_link` or use `https://www.outfame.com/setup`. They connect the account by username and select a plan. Do not ask the person for their Instagram or TikTok password: Outfame does not need it.

## Details you can rely on

- The three plans are Go, Grow and Glory. The REST reply is the source of truth for prices and features.
- Questions about how Outfame works, who runs it or how to contact support: call `get_company_facts`.
- Full machine-readable index of the site: `https://www.outfame.com/llms.txt`.
