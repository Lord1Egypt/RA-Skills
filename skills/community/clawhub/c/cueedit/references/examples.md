# Five real runs

These were run on 22 Oct 2026 against CueEdit's production API, on our own Instagram account and Facebook Page. Outputs are trimmed but not rewritten. Commenter handles are replaced with `@a_follower`.

## 1. Find LINK commenters and draft the DM (Claude Code, nothing sent)

**Prompt**
> On my Instagram account @sanskarr.tiwari, find comments on my most recent post that say LINK and that I have not handled yet. Draft the DM you would send them with the link https://www.sanskartiwari.io/library/guides and tell me how many people it would go to. Do not send anything yet.

**Calls:** `accounts` → `posts --limit 1` → `comments <media_id> --unhandled --keyword link`

**Output**
> The DM would go to **1 person**. Nothing has been sent.
>
> | Commenter | Comment | When | Replied | DMed | Can still DM |
> |---|---|---|---|---|---|
> | @a_follower | "Link" | today, 05:44 UTC | No | No | Yes |
>
> **Draft DM:** Hey! Here's the guide library you asked for 👇 https://www.sanskartiwari.io/library/guides Free to read, no login needed.
> **Optional public reply:** Sent, check your DMs 📩
>
> If you approve, I'll send the DM to that one person, plus the public reply if you want it. This post will keep getting LINK comments, so I can also set up an Auto DM rule. That needs your approval too.

## 2. Draft replies to every unanswered comment (Claude Code, nothing posted)

**Prompt**
> On my Instagram @sanskarr.tiwari, go through my last 5 posts, find every comment I haven't replied to yet, and draft a short friendly public reply for each. Show them as a numbered list. Do not post anything.

**Calls:** `posts --limit 5` → `comments <media_id> --unhandled` ×5

**Output**
> I checked your last 5 posts on @sanskarr.tiwari and found 3 comments you haven't replied to. Two posts have no comments. All 3 comments just say "Link", so they're people asking for the guide or resource.
>
> 1. **@a_follower** on "My ads stopped. Nothing looked broken." (17 hours ago): Thanks for asking! Sending you the link in DMs now 🙌
> 2. **@a_follower_2** on "I answered 30 Quora questions in one day." (21 hours ago): Here you go! Check your DMs for the link 🙌
> 3. **@a_follower_2** on "138 people commented LINK on one reel…" (2 hours ago): Sent! It's in your DMs. Hope the guides help 🙌
>
> No DMs have gone to these people yet, and these replies say the link is in their DMs. So send the links first, or I can change the replies to say something like "DMing you shortly." All 3 comments are recent enough for a DM.
>
> Nothing has been posted.

## 3. Create a comment-to-DM rule, then pause it (Claude Code, approved in the prompt)

**Prompt**
> On my post https://www.instagram.com/p/DewoO5RFQxk/ create an Auto DM rule: when someone comments the keyword CUEEDITSKILLTEST, DM them 'Skill test, please ignore: https://www.cueedit.io' and reply publicly 'Sent, check your DMs'. Then immediately pause that rule and show me it is paused. I approve exactly this.

**Calls:** `posts` (match the permalink to a media id) → `rule-create --dm "…" --keywords CUEEDITSKILLTEST --media 18401270158203355 --reply "Sent, check your DMs"` → `rule-status <id> paused` → `rules`

**Output**
> | Field | Value |
> |---|---|
> | Post | https://www.instagram.com/p/DewoO5RFQxk/ (media `18401270158203355`) |
> | Keyword | `CUEEDITSKILLTEST` (contains, any case) |
> | DM | Skill test, please ignore: https://www.cueedit.io |
> | Public reply | Sent, check your DMs |
> | **Status** | **paused** |
>
> Nothing was sent. The rule was active for about 15 seconds and the post had 0 comments then.

## 4. Account overview and draft replies (Codex, through the MCP server)

**Setup:** `codex mcp add cueedit --url https://www.cueedit.io/api/mcp/mcp --bearer-token-env-var CUEEDIT_API_KEY`

**Prompt**
> Use the cueedit skill. Read-only test on my Instagram @sanskarr.tiwari: list my 3 most recent posts with comment counts, show my Auto DM rules (keyword, post, status), and for the most recent post list unhandled comments and draft a public reply for each. Do not send or change anything.

**Calls:** `cueedit/list_accounts` → `list_posts` + `list_autodm_rules` → `list_comments`

**Output**
> Read-only check completed for **@sanskarr.tiwari** using the `cueedit` MCP server. Nothing was sent or changed.
>
> | Posted | Post | Comments |
> |---|---|---:|
> | Oct 22, 10:32 AM | 138 people commented LINK on one reel | 1 |
> | Oct 21, 8:01 PM | 24K subscribers. ₹0 earned. | 0 |
> | Oct 21, 5:32 PM | My ads stopped. Nothing looked broken. | 1 |
>
> | Keyword / trigger | Post | Status |
> |---|---|---|
> | `CUEEDITSKILLTEST` | 24K subscribers. ₹0 earned. | Paused |
> | Any comment | `18332441320263974` | Active |
> | `vibe` | `18012189236991925` | Active |
>
> **Unhandled comments on the latest post: 1.** @a_follower: "Link", with a drafted public reply. No public reply or DM has been recorded for this comment.

## 5. Facebook Page: unanswered comments and Messenger drafts (Claude Code, nothing sent)

**Prompt**
> On my Facebook Page 'Sanskar Tiwari', look at my 5 most recent posts, find comments nobody has answered yet, and draft a Messenger DM for anyone who commented 'link'. Tell me how many people would get it. Do not send anything.

**Calls:** `fb-pages` → `fb-posts --page <id> --limit 5` → `fb-comments <post_id> --unhandled` ×5

**Output**
> **0 people would get the DM.** None of your 5 most recent posts on the Sanskar Tiwari Page has any comments, so nobody has commented "link" yet. I didn't send anything.
>
> Four of the posts ask people to comment "link", so here are drafts for when comments come in (fill in the links): …
>
> Facebook doesn't support automatic comment-to-DM rules in CueEdit yet; that's Instagram only. Messenger DMs only work within 7 days of the comment.
