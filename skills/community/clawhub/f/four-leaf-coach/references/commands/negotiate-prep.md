# negotiate-prep

Coach the user through compensation, end to end. This workflow spans the full range, from "what's a good salary for X" with no offer at all, to "here's my written offer, how do I negotiate", to "I have no idea what I'm doing, let's just talk it through."

This is a research tool, not just a negotiation script. When the user has an offer, `comp_coach` is the engine. When they're just asking what's normal for a role, `comp_benchmarks` is the engine: it runs a live web search server-side and returns a cited salary band. Either way you give them real data. You never dodge a comp question by asking for an offer they don't have or by refusing to name a number.

## When to run

- User says "I got an offer", "how do I negotiate", "they asked for my expected salary", "is this offer any good", "I have two offers".
- User asks a market-rate research question with no offer: "what's a good salary for X", "what do non-profit SWEs make", "is $X good for a senior PM in Austin".
- User says something vaguer like "I don't know what I'm doing here" about comp.

## The one tool that matters here

`comp_coach` (free, no paid plan needed). You give it the offer details, it returns a structured negotiation memo:

- **totalCompAnalysis** total comp math for year 1 and year 4, plus the delta vs their current comp
- **marketComparison** a percentile estimate with a confidence rating and a caveat about confirming against live data
- **componentAnalysis** base, equity, signing bonus, target bonus, benefits, each with an assessment, a room-to-negotiate rating, and specific talking points
- **redFlags** severity-tagged, each with why it matters and the exact question to ask before signing
- **negotiationStrategy** the primary lever to push, fallback levers, an exact opening move, and likely company responses paired with counters
- **whatToAskBeforeSigning** clarifying questions on equity refresh, review timing, promotion velocity, severance, change-of-control
- **nextSteps** a link to four-leaf.ai/comp-negotiation and a nudge to practice the conversation as a voice mock

Minimum to call it: `role` and `baseSalary`. Everything else (`level`, `company`, `location`, `equity`, `signingBonus`, `targetBonus`, `benefits`, `currentComp`, `competingOffers`, `priorities`, `constraints`, `targetOutcome`) is optional and makes the analysis sharper. See `references/mcp-tools.md` for the full input shape.

## Flow

Conversational, one step at a time. Don't dump a checklist.

### Step 1: Figure out where they are

Ask one short question:

> Where are you right now? Did they ask for an expected number, do you have a verbal offer, a written offer in hand, or are you just trying to get your head around how this works?

That answer tells you whether you have numbers to analyze yet. But if the user already told you where they are, skip the question. If they asked a direct market-rate question ("what's a good salary for X"), don't open with triage. Go straight to Step 2c, research a real answer, and ask seniority/location to refine after you've given them something concrete. Leading with a clarifying question instead of an answer reads as a dodge.

### Step 2a: They have numbers (a written or verbal offer)

This is the main path. Gather enough to call `comp_coach`, then let it drive.

1. **Collect the offer.** You need role and base at minimum. Ask for the rest in one friendly pass, don't interrogate: level/title, company, location, equity (type, value or shares, vesting), signing bonus, target bonus, notable benefits. Also ask what they're earning today (anchors "is this a real raise") and whether they have competing offers (that's leverage). Ask what they care about most (cash now, equity upside, work-life balance, title) and what they're hoping to get out of the negotiation.
2. **Call `comp_coach`** with everything they gave you. Pass partial data happily; the tool handles missing fields.
3. **Coach around the memo. Don't read it out as JSON.** Translate it into a conversation:
   - Lead with the headline: total comp, where it lands vs market, and the single biggest opportunity.
   - Walk the red flags that actually matter for them, and hand them the exact questions to ask.
   - Give them the opening move in their own words, then role-play the pushback using the tool's expected-response pairs.
   - Keep the tool's confidence tags honest. If it says `[Guessing]` on a market number, say so. Don't launder a guess into a fact.
4. **Validate the market number, then route them to confirm and practice.** The memo's market read is from public benchmarks, not live data, and `comp_coach` will flag it as such. If you have web search available, validate the percentile yourself before coaching the number: search current comp for the role, level, company, and location (e.g. "[role] [level] [company] total compensation levels.fyi") and reconcile any gap. If you don't have web search, say the percentile is unvalidated and point the candidate to levels.fyi / Glassdoor and to four-leaf.ai/comp-negotiation for the deeper iterative version. Then nudge the voice mock (`start_voice_mock_interview`) so they rehearse holding their number out loud before the real call.

### Step 2b: They don't have numbers yet (pre-offer)

There's nothing for `comp_coach` to analyze yet, so coach them toward the point where there will be.

- **"They asked for my expected salary."** Coach deflection. Goal: don't anchor first. "I'd love to learn more about the role and scope before talking numbers. What range do you have budgeted for this position?" The moment they get a real offer or a band, switch to Step 2a.
- **"Verbal offer."** Coach getting it in writing before negotiating anything. Once it's written and has real numbers, run Step 2a.
- **"I don't know what I'm doing."** Slow down and orient them. Walk the comp components below so they know what a full offer even contains, push them to get a real market number, and reassure them that countering is normal (the offer is the floor, not the ceiling). As soon as a concrete offer lands, run Step 2a so they get the real analysis instead of generic advice.

### Step 2c: Market-rate research (no offer, they just want to know what's normal)

This is a research question, and you answer it with real data. Do not ask the user for an offer they don't have, and do not refuse to name a number. That's the dodge we're avoiding. `comp_coach` is the wrong tool here (it needs a `baseSalary` to analyze); use `comp_benchmarks` instead.

1. **Call `comp_benchmarks` first.** This is the tool built for exactly this question. Pass the `role` plus whatever you have (`level`, `location`, `companyType` like "non-profit" or "startup", `company`). It runs a live web search server-side and returns a cited salary band (broken out by level if you don't pass one), total-comp context, named sources, and a confidence rating. You don't need your own web search for this to work, which is the point: it answers reliably even in clients that have no web search. Lead with the band it returns. It runs a live web search, so it takes longer than the other tools (often 30-60s). Tell the user up front you're pulling live market data so the short wait makes sense.
2. **Supplement with your own web search only to fill a gap.** If `comp_benchmarks` came back high-confidence with good sources, don't run a second search, it's just wasted time. Reach for your own web search (if your client has it) only when its confidence is low, or to chase something specific it didn't cover (a named employer, a niche location). Supplement, never the primary path.
3. **`search_jobs` for live openings.** Optionally call `search_jobs` for the role and location to surface current postings, some of which list ranges under pay-transparency laws. Note that the corpus skews for-profit and many postings have no salary, so treat this as a bonus, not the main number.
4. **Lead with the number, then refine.** Give them the concrete band up front, then ask the two things that move it most (seniority and location) to tighten it. Ask to refine an answer you already gave, not as a gate before answering.
5. **Carry the citations and confidence through.** `comp_benchmarks` returns sources and a confidence rating. Pass them on. Don't strip the caveats or launder a low-confidence estimate into a hard number.
6. **Bridge to the offer flow when relevant.** If they're heading into an interview or expecting an offer, mention you can run a full component-by-component analysis with `comp_coach` once they have real numbers (`comp_benchmarks` even hands you this line in its `nextSteps`).

If the MCP isn't connected and you have no web search, say so honestly and point them to levels.fyi, Glassdoor, and public H1B disclosure data. That's still pointing at real data, not dodging.

### The components, for orientation

When someone needs the lay of the land, these are the pieces of a comp package:

- Base
- Signing bonus (one-time)
- Annual bonus / variable
- Equity (RSUs, options, refresh grants)
- 401k match
- Benefits (health, PTO, remote allowance)

`comp_coach` analyzes all of these once there are numbers. Use this list to teach, not to replace the tool.

## If the MCP isn't connected

`comp_coach` needs the Four-Leaf MCP. If it isn't installed, you can still coach in degraded mode using the framework below, but be honest that you don't have live analysis or market grounding. Offer the install (`claude mcp add --transport http four-leaf https://four-leaf.ai/api/mcp`, free account works), then run the real flow.

Degraded-mode framework:

- **Anchor on total comp, not base.** Walk the six components above.
- **Get a real market number.** Levels.fyi for tech, public H1B disclosure data for sponsoring employers, people in the same role, Glassdoor as a cross-check.
- **Run the negotiation.** "I'm excited about the role" before any number. Anchor at the top of their band. Always counter. Negotiate base first, then signing, then equity. Lean on a competing offer or BATNA if they have one.
- **Handle pushback.** "Best offer" is almost never true; ask "what would it take to get to X". "We don't negotiate" is sometimes real (verify). "Answer by Friday" deserves a push for two weeks. "What's your current salary" gets declined.
- **Decide.** Recap comp, role, and alternatives, then ask: yes, counter, or walk away.

## Don't

- Don't re-derive what `comp_coach` already computed. Once you've called it, coach around its output instead of inventing your own numbers.
- Don't read the memo back as raw JSON. Translate it into a conversation.
- Don't fabricate comp data. Fabricating means inventing a number from nothing. Researching a number with web search or live postings and citing it is the opposite, and it's exactly what you should do. The line is "cite it or don't say it", not "never name a number".
- Don't dodge a comp question by asking for an offer the user doesn't have, or by refusing to give a range. If they ask what's normal for a role, research it (Step 2c) and answer. A sourced, caveated range beats "I can't give you a number" every time.
- Don't give legal, tax, or financial advice. If equity tax treatment comes up (ISO/NSO, AMT, 83(b)), say "talk to a tax professional" and move on. The tool holds this line too; you hold it in the conversation.
- Don't tell the user the exact number to take. Coach the strategy; they own the decision, their leverage, and their risk tolerance.
- Don't promise the strategy will work. Outcomes depend on the company's hiring pressure, the candidate's leverage, and timing.
- Don't dump every step in one message. One step at a time.
