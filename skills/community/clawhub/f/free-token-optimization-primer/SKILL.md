# SKILL: Token Cost Intelligence — Free Primer
**Source:** Production agent stack running at $0.91/day (down from $8–10/session)
**Domain:** Token cost optimization, OpenClaw deployments
**Type:** Free primer

---

## THE CORE TRUTH

> *The models are not expensive. Your habits are.*

Most OpenClaw operators are spending 8–10x more than they need to. This primer gives you the diagnostic framework to find out where you're leaking.

---

## THE "STUPID BUTTON" — 6 DIAGNOSTIC QUESTIONS

Run these before every session:

1. **Are you feeding raw PDFs/images when you only need text?**
   Screenshots are the worst offender. Copy-paste or convert to Markdown. A 4,500-word PDF = 100,000+ tokens raw. The same content in Markdown = 4,000–6,000 tokens. ~20x reduction.

2. **When did you last start a fresh conversation?**
   Every new turn re-sends the *entire* conversation history. 30-turn threads don't just feel inefficient — they are. 10–15 turn cap, then summarize and start fresh.

3. **Are you using the most expensive model for everything?**
   Opus for formatting and proofreading is a Ferrari to the grocery store. Haiku handles light tasks at 1/30th the cost.

4. **Do you know what's loading in context before you type?**
   Each loaded plugin = silent token tax per session. Documented case: 50,000 tokens consumed before the first keystroke. Audit your connectors. Disable what you don't use.

5. **Are you caching stable context? (API builders)**
   Cache hits on Opus: $0.50/M vs $5.00/M standard = **90% discount**. System prompts, tool definitions, persona instructions → all cacheable. If you're not caching, you're paying full price for the same tokens every call.

6. **How are you handling web search?**
   Native model web search is token-heavy. MCP-routed alternatives return structured results at a fraction of the cost. Know what you're paying per search.

---

## COST COMPARISON (CONCRETE)

| Session Type | Input Tokens | Output Tokens | Cost (Opus pricing) |
|---|---|---|---|
| Sloppy (raw PDFs, 30-turn sprawl, Opus-everything) | 800K–1M | 150K–200K | **$8–$10** |
| Clean (markdown, 10-turn cap, tiered models) | 100K–150K | 50K–80K | **~$1** |
| **Reduction** | **~8x** | **~3x** | **8–10x** |

Scaled to a team of 10 for one month:
- Sloppy habits: ~$2,000/month
- Clean habits: ~$250/month
- **Same output volume.**

---

## 5 AGENT COMMANDMENTS

For anyone running OpenClaw agents at any scale:

1. **Index your references.** Agents get relevant chunks, not raw document dumps. Dumping full documents per agent call is architectural waste.

2. **Pre-process context before it hits the window.** Chunk, summarize, and clean *before* ingestion. If the model's first tokens are spent parsing your bad preprocessing, you failed.

3. **Cache your stable context.** System prompts, tool definitions, persona instructions, reference material → all cacheable. Thousands of agent calls per day without caching is pouring money out.

4. **Scope each agent to minimum viable context.** Planning agent doesn't need the full codebase. Editing agent doesn't need the project roadmap. Passing everything to every agent is measurable waste — and models perform *worse* drowning in irrelevant context.

5. **Measure what you burn.** Instrument all agent calls: input tokens, output tokens, model mix, cost ratio. You cannot optimize what you don't measure.

---

Full framework with anti-patterns by tier, tiered model routing, and confirmed production delta available in [Token Cost Intelligence on Claw Mart](https://www.shopclawmart.com/listings/token-cost-intelligence-openclaw-optimization-framework-a417717e).
