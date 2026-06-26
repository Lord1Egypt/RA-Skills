# AI Slop — Ban List

Patterns derived from corpus analysis (Liang et al. 2024), LinkedIn monitoring, and social media slop detection. Organized by category. Everything listed here is a hard ban unless marked otherwise.

---

## Banned vocabulary

Violates **Strunk 12** (specific, concrete language). These are abstract placeholders. "Robust" says nothing. "Handles 10K concurrent requests" says something. Replace every instance with a specific, concrete alternative.

delve, utilize, leverage, streamline, optimize, enhance, facilitate, navigate, landscape, paradigm, robust, comprehensive, innovative, transformative, pivotal, crucial, imperative, foster, bolster, underscore, realm, multifaceted, intricate, nuanced, holistic, synergy, catalyst, cornerstone, testament, tapestry, endeavor, embark, elevate, empower, unpack, dive, journey, passion, excited, thrilled, insightful, groundbreaking, game-changer, cutting-edge, seamless, scalable, actionable, impactful, ecosystem, stakeholder

## Filler phrases

Violates **Strunk 13** (omit needless words). Zero information content. Delete and start with the point.

| Ban | Fix |
|---|---|
| "it's important to note" | Cut. State the thing. |
| "it's worth noting" | Cut. |
| "let's dive in" | Cut. |
| "dive into" | Replace with a specific verb. |
| "in today's rapidly evolving" | Cut. Name the specific change. |
| "at the end of the day" | Cut. |
| "when it comes to" | Cut. Name the subject. |
| "navigate the complexities" | Name the specific difficulty. |
| "unlock the power" | Say what the tool does. |
| "in the realm of" | Cut. Say "in." |
| "it goes without saying" | Then don't say it. |
| "first and foremost" | "First." |
| "last but not least" | Cut. Just state it. |
| "without further ado" | Cut. |
| "a testament to" | Name the cause directly. |
| "paradigm shift" | Name what changed. |
| "holistic approach" | Name the approach. |
| "in conclusion" | Cut. The reader can see it's the end. |
| "to summarize" | Cut. |

## Overused transitions

Violates **Thomas & Turner** (show parallels by juxtaposition). Announces connections instead of letting placement show them. These words are not wrong individually, but clustering them signals AI authorship. Use one per paragraph at most. Prefer sentence structure to signal relationships.

moreover, furthermore, however, additionally, consequently, nevertheless, therefore, thus, hence, meanwhile, subsequently, likewise, conversely, nonetheless

## Engagement bait

Violates **Thomas & Turner** (motive is truth, purpose is presentation). The motive here is engagement, not truth. The purpose is performance, not presentation.

| Ban | Category |
|---|---|
| "agree?" "thoughts?" "who else" | Engagement solicitation |
| "hot take" "unpopular opinion" | False controversy |
| "you won't believe" "stop scrolling" | Clickbait |
| "read that again" "let that sink in" | Dramatic repetition |
| "thrilled to announce" "excited to share" "humbled and honored" | Performative emotion |

## Thought-leadership slop

Violates **Thomas & Turner** (writer and reader are equals). Talks down to the reader. Manufactures exclusivity. Implies the reader is uninformed.

| Ban | Category |
|---|---|
| "here's the thing" "but here's the thing" | False revelation |
| "here's what most people miss" "here's what nobody tells you" | Manufactured exclusivity |
| "most people don't realize" "nobody talks about this" | Same |
| "changed my thinking" "changed my perspective" | Conversion narrative |
| "the uncomfortable truth" "the honest truth" "the honest take" | Authenticity performance |
| "what surprised me most" "what actually made the difference" | Teaser framing |
| "here's what I actually learned" | Same |
| "not magic. but real" "not hype" | Understatement as proof |

## Formulaic structures

Violates **Thomas & Turner** (motive is truth) and **Pinker 1** (no meta-commentary). These are engagement machinery, not prose.

| Ban | Category |
|---|---|
| "lessons I learned" | List-post framing |
| "follow me for" "like and share" "drop a comment" | CTA spam |
| "repost if you agree" "tag someone who" "save this for later" | Engagement manipulation |
| "link in comments" "link in bio" "link below" | Traffic funneling |
| "if you're building in this space" "if this resonates" | False community |

## LinkedIn modifiers

Violates **Strunk 12** (specific, concrete language) and **Williams 2** (actions as verbs). Performative adverb + gerund. Says nothing concrete about what was built. Ban the pattern entirely.

| Ban |
|---|
| "quietly building/winning/dominating/changing/creating/scaling/working" |
| "silently building" |
| "relentlessly building" |
| "obsessively focused" |
| "slowly realizing/becoming" |

## Humble-brag framing

Violates **Thomas & Turner** (purpose is presentation, not performance). The timeline is the point, not the work.

| Ban | Why |
|---|---|
| "built in a day" "in a weekend" "in just one week" | Compressed-timeline flex |
| "what excites me most" "what excites me" | Performative enthusiasm |
| "it's all open source" | Virtue signal when unprompted |
| "this is what that looks like" "in practice" | Teaser-to-proof structure |
| "imagined and built" | Hero narrative |

## Manufactured demand

Violates **Thomas & Turner** (motive is truth). Frames the post as audience response. The motive is social proof, not truth.

| Ban | Why |
|---|---|
| "people asked for more" "asked for more detail" | Frames post as audience response |
| "got a reaction" "went viral" "blew up" | Social proof framing |
| "so here's part" "as promised" | Serial content hook |
