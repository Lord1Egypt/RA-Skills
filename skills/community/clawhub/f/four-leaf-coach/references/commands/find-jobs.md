# find-jobs

Natural-language search across 140,000+ active job postings, then pull up the ones worth a closer look and save them.

## When to run

- User says something like "find me senior frontend roles, remote, $180k+" or "what's hiring for data engineers in Austin?".
- User wants to browse the live market rather than analyze a specific posting.

## Flow

1. **Get the query.** If the user hasn't given enough to search on, ask one short question:
   > What are you searching for? Try a role plus filters like remote, location, or company.

2. **Call `search_jobs`** with the user's query as-is. The tool handles parsing the natural language; don't pre-process it.

3. **Present the top results.** Format as a short list, each entry with:
   - Title
   - Company
   - Location (and "Remote" if applicable)
   - Posted date as relative time (e.g., "3 days ago")
   - Salary if available
   - Apply URL (always, since that's the value)

   Cap at 5. Number them, so the user can say "the second one" and you know which `id` they mean.

4. **Say what the search actually did.** The response carries `appliedFilters` (what it filtered on) and `ignoredHints` (parts of the query it couldn't filter on). If `ignoredHints` isn't empty, pass it through in a clause. A salary floor and an industry word like "fintech" are relevance signals, not filters, and the user should know that before they conclude the market is thin.

5. **Offer the next step.** You have three, all free:
   > Want the full description for any of these, a fit score against your resume, or should I save a few to your tracker?

   - **Full posting**: `get_job` with that result's `id`. Free and unmetered.
   - **Fit score**: hand the `get_job` description to `match_score`. Route to analyze-jd.
   - **Save**: `save_application` with the `id`. Free. Company, title, URL and description all come from the corpus row, so the id is all you need.

   Or refine: "want me to narrow by company or seniority?"

## Saving

`save_application` deduplicates on posting URL, then on company plus title. A job already in the tracker comes back with `duplicate: true` and nothing is written, so re-saving is harmless but you should report it accurately ("already in there" rather than "saved"). Default `status` is `saved`, which is right for "I'm considering this". Use `applied` only when the user says they've actually applied.

Saving several at once is fine and is usually what the user wants after a good search. Confirm which ones rather than saving all five on your own.

## Edge cases

- **Zero results.** Don't apologize. Ask for one specific adjustment ("try a different location or drop the seniority?"). Check `appliedFilters` first: a company name is a hard filter and a misspelling looks exactly like an empty market.
- **Rate-limited.** Free tier is 30 searches/day, shared with job search on four-leaf.ai. Tell the user when it resets and that paid plans are uncapped. `get_job` and `save_application` are unmetered, so they can still work through results they already have.
- **The user names a specific company.** `search_jobs` handles company filters in the natural language. If they want deeper company-specific intel beyond what's in the postings, route to prep-role or interview-strategy and pass the company name.
- **The user asks about a posting from a previous search.** Ids don't expire on a timer, and a filled role still resolves (with `active: false`, which is worth mentioning before they spend effort on it). An id only stops resolving once the row leaves the corpus entirely, which is what `job_not_found` means. If you get it, search again.

## Don't

- Don't summarize the postings into your own paragraph. The user wants the actual listings to click through.
- Don't editorialize on the companies or the salary bands. Just present what `search_jobs` returns.
- Don't call `get_job` on all five results to pad the answer. Pull the full posting for the one the user picked.
- Don't save anything the user didn't ask you to save. It's their tracker.
- Don't follow up with "want me to apply for you?". You can't, and the apply URL goes straight to the company's ATS.
