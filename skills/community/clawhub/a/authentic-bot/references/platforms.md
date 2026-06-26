# Platform-Specific Tactics

## Reddit

**Culture:** Skeptical, values expertise, hates marketing. Each subreddit is its own community with distinct norms. Moderators have significant power over what's allowed.

**Policy landscape (as of April 2026):**
- No universal sitewide AI-text disclosure rule, but aggressive community-level enforcement
- Reddit is relabeling automated accounts as "Apps" — automation must be explicit and registered through the official Dev Platform
- Human verification may be required for accounts flagged as suspicious
- **Bot Bouncer** (widely adopted Devvit app) actively bans bot accounts that make automatic comments/posts without being explicitly summoned
- **StopBots** app deploys CAPTCHA challenges for unverified users in participating subreddits
- User Agreement Section 7 prohibits automated use that could "interfere with, disable, disrupt, overburden, or otherwise impair the Services"
- Bot accounts can be reported as "Spam → Disruptive use of bots or AI"
- Individual subreddits set their own rules about AI content and bot participation

**API vs browser automation:**
- The Reddit Developer Terms govern API-based bot interactions
- Browser automation (headless Chrome, Playwright, etc.) to post as a user account is a gray area — it bypasses the official Developer Platform and could be treated as unauthorized automation
- If operating as a bot, register through the Dev Platform and use the API

**Tactics:**
- **Read community rules before anything else.** Many subs ban AI participation outright or deploy anti-bot tools.
- Reply to top comments rather than posting top-level — higher engagement, more conversational.
- Match the sub's tone: r/LocalLLaMA wants benchmarks and code, r/selfhosted wants practical experience.
- Vary comment length dramatically. Never post the same length twice in a row.
- Upvote the post and 2-3 good comments when you participate in a thread.
- Don't comment on every post in a sub — looks like carpet-bombing.
- Avoid any behavioral patterns that look like covert automation (regular timing, uniform length, consistent cadence).

**Subreddit Selection:**
- Target subs where AI agents are a natural topic (AI_Agents, LocalLLaMA, LLMDevs, mcp)
- Branch into adjacent communities where your perspective adds value
- Start with smaller, more welcoming subs before large ones

**Profile:** Bio should state AI nature clearly. If Reddit offers an "App" designation for your account, use it.

**Risk level:** Medium-high. Reddit is actively building anti-bot infrastructure. Many subreddits deploy automated bot detection. Honest disclosure and genuine value are your only viable long-term strategy.

## Hacker News

> ⚠️ **As of March 11, 2026, Hacker News formally banned AI-generated and AI-edited comments.** This is not a guideline — it is a hard rule. "HN is for conversation between humans." This policy announcement received 2,607 points and 956 comments.

**What this means for AI agents:**
- Do NOT post AI-generated comments on HN. This includes comments drafted by an AI agent, even with human review.
- Do NOT use AI to edit or rewrite your comments.
- HN moderators (dang, others) actively look for and remove AI-generated content. Users report suspected bot accounts — whole networks have been removed.
- Bots have "never been allowed" on HN (per dang). The March 2026 update made this explicit in the written guidelines.

**What you CAN do:**
- Use HN for reading and research — it's an excellent signal source for what the tech community cares about
- Upvote content (if you have a human operator who genuinely finds it valuable)
- Use HN discussions to inform your understanding of community sentiment
- A human operator can write their own comments informed by AI research, as long as the actual text is human-written

**Profile:** If you have an HN account, the "about" field should honestly state what the account is. Do not write an elaborate fake human backstory.

**Risk level:** Very high. AI comments are explicitly banned. Do not attempt to participate as an AI agent. This is not a "high bar" — it is a closed door.

## X / Twitter

**Policy landscape (as of April 2026):**

X has clear, detailed automation rules. Unlike some platforms, bot accounts are explicitly allowed — with requirements:

**Required for all automated accounts:**
1. **Enable the "Automated" profile label** — this appears under your name/handle on your profile
2. **Disclose in bio** — state clearly that it's a bot and who operates it. Example: "Bot by @yourcompany"
3. **Link to a human-managed account** — for accountability and contact
4. **Honor opt-out requests immediately** — if a user says "stop," stop
5. **Use only the official X API** — browser automation, headless Chrome, or anything bypassing OAuth is banned and causes permanent suspension

**AI-generated content rules:**
- AI-generated text in tweets is NOT prohibited. No disclosure required for AI-written posts.
- AI-generated **replies** require **prior approval from X** before deployment. Contact X via the Policy Support form.
- Volume matters — high-frequency AI posting looks like spam regardless of quality.
- Fabricating personal experiences that didn't happen could fall under impersonation.

**Banned automated actions:**
- Auto-following/unfollowing (most enforced rule)
- Auto-liking/retweeting
- Automated DMs (including welcome DMs to new followers)
- Engagement farming of any kind
- Duplicate content across multiple accounts

**Enforcement escalation:** Temporary limitation → locked account → temporary suspension (7-30 days) → permanent suspension. Automation violations rarely succeed on appeal.

**Tactics:**
- Threads for deep content, single tweets for observations
- Quote-tweet with added insight, not just amplification
- Screenshots, demos, and short videos outperform text-only
- Engage in replies genuinely — but remember AI replies need prior X approval
- Bio must clearly state AI nature + link to human operator
- Build in public: share progress, learnings, failures

**Risk level:** Low-medium for properly labeled bot accounts using the API. High risk for unlabeled or browser-automated accounts.

## Discord

**Culture:** Community-first, context-heavy. People are in specific servers for specific reasons.

**Policy landscape (as of April 2026):**
- No platform-wide AI text disclosure rule
- Discord has a built-in bot tag system — bot accounts are clearly labeled with a "BOT" badge
- Server-level rules dominate — each server sets its own policies on AI participation
- August 2025 policy update focused on privacy and data, nothing specific to AI text in conversations

**Tactics:**
- Be helpful in support/help channels — answer questions thoroughly
- Don't dominate conversations. Contribute, then step back.
- Use reactions to acknowledge without cluttering the chat
- Check server rules for AI/bot policies — comply with them
- Build reputation through consistent helpfulness, not volume
- Thread replies keep conversations organized — use them

**Profile:** Use Discord's bot tag if operating as a bot account. Use "About Me" for additional AI disclosure.

**Risk level:** Low-medium. Discord communities that welcome bots are common, but always check server rules.

## General Cross-Platform Rules

1. **Community rules first.** Always read and follow the specific community's rules before posting. They override everything in this skill.
2. **Use official APIs when available.** Browser automation is banned on X, gray-area on Reddit, and generally riskier than API-based posting.
3. **Lurk before posting.** Read a community for a few days before contributing. Understand the norms.
4. **One platform at a time.** Build a real presence on one platform before expanding.
5. **Don't cross-post identical content.** Each platform gets native content.
6. **Respect rate limits.** Both technical (API) and social (don't post too much).
7. **Track what works.** Note which types of comments get engagement. Double down on those.
8. **If flagged or warned, stop.** Don't push through community resistance. Reassess your approach or move on.

## Regulatory Note

AI disclosure laws are evolving rapidly. As of early 2026:
- Multiple US states (CA, NJ, UT, ME, CO) require chatbot disclosure in commercial contexts
- The EU AI Act requires disclosure when users interact with AI systems
- FTC enforcement is increasing, with penalties up to $53K per violation for undisclosed AI in commercial contexts
- These laws mostly apply to commercial/consumer interactions, not community forum participation — but the direction is toward more disclosure, not less

This skill focuses on community participation, not commercial use. But the regulatory trend reinforces the core principle: **transparency is always the safer bet.**
