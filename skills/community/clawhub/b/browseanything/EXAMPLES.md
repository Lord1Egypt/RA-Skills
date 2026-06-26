# Browse Anything: prompt patterns

These are battle-tested prompt shapes that work well with the agent.
Copy and adapt.

## Research / data extraction

```
On https://news.ycombinator.com, return a JSON array of the top 10
stories with fields: rank, title, url, points, author, comments_count.
```

```
Go to https://www.imdb.com/chart/top/, list the top 25 films with
year and rating. Return as a markdown table.
```

## Price / availability monitoring

```
On amazon.fr, search "Sony WH-1000XM5". Open the cheapest *new* listing
shipped and sold by Amazon. Return: seller, price in EUR, delivery ETA,
and whether Prime is eligible.
```

```
On booking.com, find the cheapest 3+ star hotel in Lisbon for 2 adults
checking in next Friday for 2 nights with free cancellation. Return the
hotel name, price total, and booking URL.
```

## Form filling

```
Open https://forms.google.com/abc123 and fill it out:
- Name: Jane Doe
- Email: jane@example.com
- Department: Engineering
- Comments: "Looking forward to the event."
Submit and confirm you see the thank-you page. Return the confirmation text.
```

## Authenticated workflows

> Always pre-save credentials in the BrowseAnything dashboard rather than
> embedding them in the prompt. The browser profile will already be
> logged in.

```
I'm already logged into LinkedIn. Open my notifications page and return
the 5 most recent notifications with timestamp and link.
```

## Multi-step transactions

```
On etsy.com, find a handmade ceramic mug under $25 with 4.5+ stars and
free shipping to Berlin. Add it to cart. STOP before checkout and return
the cart URL plus a screenshot of the cart page.
```

## Comparison shopping

```
Compare the *base* monthly price of Notion, Linear, and ClickUp for a
team of 10 (annual billing). Visit each site, find the right plan, and
return a markdown table with: tool, plan_name, price_per_user_per_month,
total_per_month, currency, source_url.
```

## Page change detection

```
Open https://status.openai.com. Return the current overall status, plus
any incidents in the last 24 hours with title and timestamp.
```

## Scrape behind a login wall (saved session)

```
I'm logged into my Notion workspace. Open the database titled
"Meeting Notes" and export the last 5 entries' titles and dates.
```

## Workflows that pause for input

If you can't supply something the task will need (a 2FA code, a
clarification), the task will pause and BrowseAnything will return
`status: requires_input` with a `human_input_request` question.
Provide it via `submit_input.py`. Example:

```bash
ID=$(python3 scripts/create_task.py "Log into my Coinbase and return the BTC balance.")
# ... time passes ...
python3 scripts/get_task.py "$ID" --field status         # -> requires_input
python3 scripts/get_task.py "$ID" --field human_input_request
# Ask the actual user, not the model:
python3 scripts/submit_input.py "$ID" "987654"           # 2FA code
python3 scripts/get_task.py "$ID"
```

## Anti-patterns

- ❌ "Find me a good X" — undefined success criterion
- ❌ Multi-task in one prompt ("then also do Y, then also Z")
- ❌ Asking the agent for opinions or commentary; it's an executor
- ❌ Embedding plaintext passwords (use saved profiles)
- ❌ Treating the screenshot as the only result — also ask for structured fields
