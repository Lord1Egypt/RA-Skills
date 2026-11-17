# Four-Leaf MCP tools

Reference for the tools the hosted Four-Leaf MCP exposes. Read this when you need to know what's available, what each returns, or whether a tool needs a paid plan.

The MCP is at `https://four-leaf.ai/api/mcp`. Streamable HTTP. OAuth 2.1 + PKCE + DCR. Fifteen tools. Free tools work for any authenticated user.

The per-tool reference on https://four-leaf.ai/oss is generated from the same schemas and is the place to check an argument name if this file and the server ever disagree.

## Read tools (free, no daily limit)

### `list_roles`
The catalog of roles Four-Leaf has structured interview intelligence for. Returns role id, display name, and a one-line description. Every `role` argument on every other tool takes an id from here. Cheap and fast, so it doubles as the connection check.

### `get_role_intelligence`
For a single role id: the structured interview pipeline (rounds, duration, format, focus), experience-level calibration, question categories, the 5-dimension scoring rubric, resume guidance, and cover-letter guidance. Call this when the user wants depth on a role.

### `get_interview_questions`
Questions from the curated Four-Leaf bank, filtered by `role` and optionally `difficulty` (easy, medium, hard) or `questionType` (behavioral, technical, situational, coding, case). `limit` is 1-25, defaults to 10. Each question comes with context, a coaching tip, and the key points a strong answer covers. No sample answers, on purpose.

### `explain_interview_format`
For a `role` plus optional `experienceLevel` and `company`: the pipeline summary plus prose for what to expect, how to win, and red flags. The pipeline is Four-Leaf data; the prose is written from it by a model. Naming a company flavors the prose from public knowledge only, and the response returns `companyDataAvailable: false` to say so. Four-Leaf holds no company-specific interview data, so don't imply otherwise.

### `get_job`
The full posting for one `search_jobs` result, by `jobId` (the `id` on a search result). Returns everything the search row had plus `description` (first 12,000 characters, with `descriptionTruncated` when it was cut) and `active`, which is false when the posting has come down. This is how a job found through the MCP becomes text you can pass to `match_score`. No fetching, no WebFetch, no daily cap.

### `list_applications`
The user's application tracker on four-leaf.ai. Zero required arguments; the connection already knows whose list it is. Optional `status` (saved, applied, interviewing, rejected, withdrawn) and `limit` (1-50, defaults to 20). Returns company, title, status, posting URL, match score and salary range when set, dates, and a link to each application, most recently updated first. Job descriptions are deliberately not in the payload, so this answers "where am I with Stripe", not "score this again".

## Compute tools (free, daily limits apply)

Each limit is its own counter, so scoring three answers does not spend the question-generation budget. A paid subscription lifts all of them; a bare free trial does not.

### `search_jobs`
Natural-language search over 140,000+ active postings scraped nightly from Workday, Greenhouse, Ashby, SmartRecruiters, Lever, and Eightfold. `query` required; optional `location`, `remote`, and `limit` (1-10, defaults to 5). Returns each job's `id`, title, company, location, posted date, salary if the posting publishes one, a 300-character snippet, and a direct apply URL, plus `appliedFilters` (what it actually filtered on) and `ignoredHints` (parts of the query it could not filter on, like industry words or a salary floor). One role and one seniority per call; a named company is a hard filter. The `id` is the handle for `get_job` and `save_application`. Free tier: 30 searches/day, a budget shared with job search on four-leaf.ai.

### `generate_practice_questions`
Fresh practice questions on demand. `role` required; optional `type` (behavioral, technical, situational, coding, case), `difficulty` (easy, medium, hard), `company` for interview-style flavor, and `count` (1-10, defaults to 5). Each question comes back with a coaching tip and the key points a strong answer covers. No sample answers. Free tier: 20 generations/day.

### `score_answer`
Rubric-scored feedback on an answer the user typed in the conversation. `question` and `answer` required; optional `role` (calibrates the rubric), `experienceLevel` (entry, mid, senior, staff; defaults to mid), `questionType` (behavioral, technical, situational, coding; defaults to behavioral), and `company` for framing. Returns a **1-10** score (the floor is 1, there is no 0), `dimensionScores` for relevance, specificity, structure, role fit and communication, `strengths`, `improvements`, and `detailedFeedback`.

This is the same scoring the Four-Leaf practice page runs on typed answers. Nothing is saved: the attempt is not written to the user's history. The answer has to be at least 20 characters after trimming, and a one-line answer will score badly for the right reasons. Free tier: 20 scorings/day.

### `match_score`
Scores a resume against a job description. `resume` is **optional**: omit it and the tool scores the user's Four-Leaf master resume, which is the common path since every MCP user is signed in. Pass it only to score a different version. `jobDescription` is required, must be plain text, and must be 50-50,000 characters. The tool does not fetch URLs and rejects a bare URL with `job_description_is_a_url`, so get the text first (`get_job` for a posting from `search_jobs`, your own WebFetch for a URL from anywhere else). Returns a 0-100 overall score, breakdowns for skills / experience / role alignment, matched skills, missing required skills, `resumeSource: "master" | "pasted"`, and a link to tailor against the same posting. Free tier: 20 scores/day.

### `comp_coach`
Compensation negotiation analysis for an offer the user already has. Takes a structured offer (`role` and `baseSalary` required; `level`, `company`, `location`, `equity`, `signingBonus`, `targetBonus`, `benefits`, `currentComp`, `competingOffers`, `priorities`, `constraints`, `targetOutcome` all optional) and returns a negotiation memo: total comp math for year 1 and year 4 with the delta vs current comp, a market percentile estimate with confidence and caveats, component-by-component analysis with talking points, severity-tagged red flags with the exact question to ask, a negotiation strategy (primary lever, fallbacks, an opening move, expected company responses paired with counters), questions to ask before signing, and a link to four-leaf.ai/comp-negotiation. The market percentile is a model estimate from public benchmarks, not live data, and the response says so. Never gives legal or tax advice. For a market-rate question with no offer, use `comp_benchmarks`. Free tier: 20 analyses/day.

### `comp_benchmarks`
Web-search-grounded market salary lookup, for "what does role X pay" when there is no offer yet. `role` required, plus optional `level`, `location`, `companyType` (non-profit, startup, big tech, government, enterprise), and `company`. Runs up to three searches server-side and returns a cited salary band (broken out by level when no level is given), total-comp context, named sources with URLs, a confidence rating, and caveats. Because the search runs server-side, it works in clients with no web search of their own. Sources can come back empty at low confidence. It typically takes 20-45 seconds and a lookup over 50 seconds is stopped with an error, so tell the user you're pulling live data before you call it. Free tier: 20 lookups/day.

## Write tool (free, no daily limit)

### `save_application`
The only tool on the server that writes something the user keeps. Saves a job to their application tracker, either by `jobId` from a `search_jobs` result (company, title, URL and description are taken from the corpus row and the other arguments are ignored) or by `company` plus `title` for a posting found anywhere else, with optional `jobUrl`, `jobDescription`, and `status` (saved or applied, defaults to saved). Returns the application id, status, and a link to it.

It deduplicates on posting URL first, then on company plus title. A job already in the tracker comes back as-is with `duplicate: true` and nothing is written, so a repeat call is safe. Say what happened either way: "already in your tracker" is different from "saved".

## Paid tools (return `upgrade_required` for free users)

### `start_voice_mock_interview`
Returns a link to Four-Leaf's voice mock interview setup page, pre-filled with `role` plus optional `interviewType` (recruiter, technical, behavioral, case, coding, system_design), `experienceLevel`, and `company`. **No session is created by this tool.** The practice itself runs on the page: spoken answers, adaptive follow-ups, rubric-scored feedback. The response says whether the requested round was pre-selected and lists the rounds the role actually offers, because not every role has a case or technical round. Requires paid access, which a live free trial grants.

### `tailor_resume`
Live. Returns a link to Four-Leaf's Tailor Resume page for the user's master resume against a specific posting (AI rewrite per bullet, ATS keyword matching, side-by-side compare). `role` is required and must be an id from `list_roles`, so resolve it before calling (a pasted JD doesn't give you one). Optional `jobDescription` (50-20,000 characters) is stored in a single-use 15-minute stash whose id rides in the link, so the page opens with the posting already filled in. Optional `company`. Requires paid access, which a live free trial grants. `match_score` assesses fit against the same posting for free.

## Error shapes to expect

Every tool returns either its happy-path JSON or an error of the shape:

```json
{
  "error": "daily_limit_exceeded",
  "message": "human-readable explanation",
  "upgradeUrl": "https://four-leaf.ai/pricing?ref=mcp_<surface>"
}
```

`upgradeUrl` is present on the two gate errors and absent on the rest. The codes you will actually see:

- **`daily_limit_exceeded`**: a metered tool's free-tier budget is spent for the day. Say which budget, note that it resets daily and that the other counters are untouched, and offer a free tool that still works.
- **`upgrade_required`**: a paid tool on a free account. Surface `upgradeUrl` verbatim, explain in one sentence what's behind it, offer the free alternative. See `upgrade-flow.md`.
- **`role_not_found`**: call `list_roles` and suggest the closest match. On `score_answer` you can also just drop the `role` argument and score against the general rubric.
- **`job_not_found`**: the `jobId` is not in the corpus at all. A filled posting still resolves and comes back with `active: false`, so this means the row is gone, not that the role closed. Re-run `search_jobs`, or save it by company and title instead.
- **`no_master_resume`** (`match_score`): no resume on the account. Surface the `uploadResumeUrl` it carries and retry once the user says they've uploaded. Don't scrape a resume out of the chat history as a workaround.
- **`job_description_is_a_url`** (`match_score`): you passed a URL where text belongs. Get the text first.
- **`answer_too_short`** (`score_answer`): the answer or the question is below the minimum. Neither costs a credit, so ask for a real answer and call again.
- **`missing_fields`** (`save_application`): pass `jobId`, or both `company` and `title`.
- **Anything ending in `_failed`** (`scoring_failed`, `lookup_failed`, `generation_failed`, `analysis_failed`, `save_failed`, `search_failed`): the tool errored. Say so plainly, offer to retry once, and continue without it rather than inventing the output it would have returned.
