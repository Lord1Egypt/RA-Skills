# The YC Canon: Product and Product-Market Fit

The half of the Y Combinator canon that deals with finding something people want — Michael Seibel, Gustaf Alströmer, Eric Migicovsky, Dalton Caldwell, Peter Reinhardt. These axioms cover the pre-PMF period: how to tell whether you have fit, how to find and study the first users, how to interview them without leading them, when to change the idea, and at what cadence to ship while you search.

Companion file: `yc-canon.md` carries the essay-derived remainder of the canon — Paul Graham on doing things that don't scale and on raising money, Livingston on measurement and denial, Altman on momentum and unit economics, Ralston's prioritization formula, Buchheit's 90/10 solution, Seibel on why fundraising rounds are not milestones, Harris on taking advice — plus YC's pocket guide.

Attribute axioms to their source when relevant. This material is the early-stage view by construction; later-stage wisdom diverges.

## Find product-market fit before optimizing anything (Michael Seibel)

**Product-market fit feels like the building is on fire.** Customers are buying as fast as you can make it. Servers are crashing. You're frantic trying to support the demand you didn't engineer. Before that signal arrives, you don't have PMF, regardless of how many employees, customers, or dollars raised you have. Acting as if you have PMF when you don't — by hiring, scaling burn, optimizing the product — is one of the most expensive mistakes a founder can make.

**"Hair on fire" customers are the only customers who matter early.** If your friend's hair was on fire, they would grab a brick to put it out, not wait for the perfect solution. Find customers in that much pain. They will adopt your half-built v1 because their need is acute. If you can't find them, you have a market problem, not a product problem.

**The market pulls the product out of the startup.** (Andreessen's framing, which Seibel quotes.) Founders fall in love with their solutions and hold them too tightly. The opportunity is in the problem, not in the founder's particular v1 idea about how to solve it. Launch, listen, iterate — repeat until the market starts pulling.

**Hijacker users are leading you into a consulting business.** If users with very different problems start signing up, ask whether they represent a larger underserved segment — or whether they're a one-off who will pull your roadmap apart. Saying "no" politely to off-target users is a core PMF discipline. Don't pivot for one user. Do pivot if the off-target users are clearly more numerous and more desperate than your target.

## The Sean Ellis / Superhuman 40% PMF Test

**Survey active users with one question: "How would you feel if you could no longer use this product?"** Three answers: (a) Very disappointed, (b) Somewhat disappointed, (c) Not disappointed. The share answering "very disappointed" is your score. It is the most concrete PMF test in widespread use, and the only one that produces a number before the revenue does.

**40% is Sean Ellis's benchmark, not a definition of product-market fit.** Ellis arrived at it by benchmarking nearly a hundred startups: the ones that struggled to grow almost always scored under 40%, the ones with strong traction almost always cleared it. That makes it a leading indicator correlated with sustainable growth, not a gate that overrides every other piece of evidence — a company drowning in demand at 38% has fit, whatever the survey says.

**A score below 40% is a starting point you systematically improve, not a verdict.** (Rahul Vohra, Superhuman; First Round Review, "How Superhuman Built an Engine to Find Product-Market Fit.") Superhuman measured 22%, segmented to the users who loved it most and got 32%, then reached 58% within three quarters. The method: profile the High-Expectation Customer (HXC) — Julie Supan's framework, which Vohra applied to the Ellis survey — then split the roadmap in half, doubling down on what the "very disappointed" cohort already loves and removing whatever holds the somewhat-disappointed back. See `product.md` for the PMF Engine mechanics.

The limit is in the aggregate number: low-frequency B2B products, marketplaces, and multi-persona products routinely sit below 40% overall while having durable fit with one segment. That is what the segmentation step is for.

Pair the score with Marc Andreessen's qualitative description — "the customers are buying the product just as fast as you can make it — or usage is growing just as fast as you can add more servers. Money from customers is piling up in your company checking account," quoted in Seibel's "The Real Product Market Fit" — and Michael Seibel's frantic-founder test ("you're swamped just keeping it up and running") for triangulation.

## Minimum Evolvable Product (Gustaf Alströmer)

**Build a Minimum Evolvable Product, not just a Minimum Viable Product.** An MVP asks "does this solve the problem at all?" An MEP asks "can this adapt to what we learn from early users?" The earliest version of your product only needs to do one thing: survive contact with those first users. You're not building the final form. You're building something that can evolve.

**Think of a startup as a phylogenetic tree.** The root node is an amoeba. The leaf nodes are complex multicellular organisms. Almost every successful product ran an evolutionary process — from a simple set of functions to a refined, fully-evolved product. The path you take through that tree isn't random; it's determined by your early adopters.

**Finding your first users is a search problem, not a persuasion problem.** You're not trying to convince skeptics. You're trying to find the rare individuals who are already predisposed to try new things — or who have such a burning problem that they'll give any potential solution a shot. The shift from persuasion to search changes everything about how you spend your time.

**Two types of early adopters:**
- **Natural early adopters** — people who genuinely enjoy trying new products. They exist in every organization. They get excited when a founder cold-emails them with something new.
- **People with burning problems** — those with such an urgent issue that they'll try any solution that looks plausible. Reputation, founder pedigree, and company size are irrelevant to them. The acute pain overrides their preferences.

Most founders waste time on the early majority (34% of the market, in Everett Rogers' classic adoption curve) who won't touch unproven products from unknown companies. The job in the first year or two is to find and win the first ~16% — the innovators and early adopters. Everyone else is a distraction.

**The product you ship in five years is a direct descendant of the one you build for your first users.** Path dependency is real: early users shape your product's DNA. Tesla's Roadster wasn't just a fundraising vehicle for the Model S. It was a search for the early adopters who would tolerate an impractical $150K car with limited range — tech enthusiasts who valued acceleration and innovation over comfort. That's why today's mass-market Model Y still leads with sports-car acceleration and has worse suspension than a Toyota. Early adopter preferences became permanent product DNA. Choose your first users accordingly.

**Charge real money early.** Counter-intuitive but consistent across YC's experience. Early adopters and people with burning problems are rarely price-sensitive. The goal of charging isn't revenue — it's feedback quality. Paying customers tell you the truth; free users tell you what you want to hear. An angry paying customer who paid real money will give you sharper feedback than a hundred enthusiastic free users. *(Stage: Pre-PMF.)*

**Counterintuitive rules for getting early users:**
- Targeted, personal outreach beats scaled marketing. Cold emails to specific people. Direct messages. Knocking on doors. Early-adopter acquisition is intimate and specific, not broad and scalable. Broad and scalable comes later.
- Study early users like an anthropologist. How do they make decisions? Why did they take the strange step of trusting you? What do they actually want versus what they say they want?
- Experiment fast and don't fear churn. The relationship is personal at this stage; if you annoy someone, you can usually fix it. If they leave, that's data. There are more potential users out there who haven't even heard of you yet.
- Don't try to convert skeptics. If someone isn't excited after a short explanation, they're probably not an early adopter. Don't spend weeks convincing them. Spend those weeks finding someone who gets it immediately.

## The Five User-Interview Questions (Eric Migicovsky)

The "Mom Test" frame, from Rob Fitzpatrick's book of the same name: user interviews exist to extract information from the user, not to sell them on your idea. Three common mistakes:
1. Talking about your own idea and life
2. Asking about hypotheticals ("would you use it if we built X?")
3. Talking more than listening

Five questions that work in nearly every user interview:

1. **What's the hardest part about [doing this thing]?** Tests whether the problem you're working on is something real users actually feel as a pain point.
2. **Tell me about the last time you encountered that problem.** Forces specifics rather than hypotheticals; surfaces the actual context.
3. **Why was that hard?** Customers don't buy the "what" — they buy the "why." This question informs your positioning and explains the value you provide.
4. **What, if anything, have you done to try to solve the problem?** If they haven't tried anything, the problem may not be acute enough. If they've cobbled together hacks and workarounds, you've found someone with hair on fire.
5. **What don't you like about the solutions you've tried?** Inherent flaws in current alternatives. This becomes your wedge.

**Avoid features questions.** "What features would you like?" is not the customer's job to answer; it's yours. Users are better at identifying problems than identifying solutions. (Henry Ford's possibly apocryphal "faster horses" — true or not, it captures the failure mode.)

## Reinhardt on Validation (Peter Reinhardt, Segment)

**The most common startup failure mode is solving problems no one has.** 80% of founders fail to find PMF. Most fail by deluding themselves into building things customers don't need, rather than building things badly. The failure is in conception, not execution.

**For technical founders, building is the least useful way to reduce risk.** (Reinhardt, "Finding Product Market Fit," 2016; the odds below are his own illustration, not a measurement.) A non-technical team has ~15% odds of being able to build it and ~60% odds of solving a real problem. A technical team has ~90% odds of being able to build it and ~10% odds of solving a real problem. If you're a technical founder, you can build. What you can't reliably do is identify a real problem — that's where to focus your effort.

**Skepticism is the antidote to founder delusion.** There's a fine line between the "reality distortion field" founders create and delusion. Founders typically force ideas through without ever truly questioning whether anyone has the problem. The remedy is forcing real validation work: hour-long interviews with potential users digging into what frustrates them, until you find a real problem (or determine there isn't one for you to solve).

**Sometimes you find the real problem accidentally, as a side project.** Segment's analytics.js was a thin abstraction layer they built so they wouldn't have to choose between three analytics services. It became a 500-line open-source side project while they spent a year and a half on a "real" product nobody wanted. When they finally tested whether analytics.js could be a business, it hit #1 on Hacker News in a day. The validated side project was hiding in plain sight for 18 months.

## Caldwell's Pivot Framework

**A pivot is just changing your idea.** Demystify it. The word "pivot" has accumulated drama; treat it as routine. At pre-launch or just-after-launch stage, changing your idea constantly is the norm. If you're not rapidly changing ideas or assumptions in quick succession, you're probably moving too slowly.

**Why pivot? Opportunity cost.** You can only really work on one thing at a time. Working on something that's not working has the cost of not working on something else. The longer you've been at it without working, the stronger the signal.

**Good reasons to pivot:**
- You hate working on it
- It's not growing
- You're not the right person for the idea (founder-market misfit)
- You're relying on an external factor outside your control (mainstream VR adoption, crypto going mainstream, etc.)
- You're out of ideas on how to make the current thing work

**Bad reasons to pivot:**
- You're running away from doing hard work (e.g., always pivoting right before sales time)
- You're a chronic pivoter who never sees anything through
- You read about a hot new thing on TechCrunch and want in

**Why people take too long to pivot:**
- **Loss aversion.** You feel you've invested too much to abandon it. The math doesn't care.
- **A little bit of traction.** One customer, a few users. Just enough to keep hoping.
- **Politeness confused with traction.** People rarely tell you your idea is bad. They say "interesting, maybe add a few features and come back," and you iterate against polite signals for years.
- **Fear of defeat.** Pivoting feels like giving up.
- **Blaming external factors.** "The world isn't ready for this." Usually wrong.
- **Inspirational anecdotes about persistence.** True but not actionable. Stories of people who persisted for years and eventually succeeded are real, but so are lottery winners. Don't structure your life around the rare anecdote.

**The uncanny valley of product-market fit.** A founder whose idea is a total, immediate failure is actually at an advantage versus one with a little bit of traction. Total failure forces decisive action; modest signal traps founders for years. Counterintuitive but consistently observed.

**Caldwell's idea-quality score** — rate each on 1–10:
1. **Size.** Could this be a publicly traded company? Tesla, a new bank, a new car company: yes. A Subway franchise: no.
2. **Founder-market fit.** Are you the right person for this idea? "I built self-driving cars throughout college" → 10/10 for self-driving cars. "I don't know how to program" → 0/10 for an AI startup.
3. **Ease of getting started.** Wildly underrated. Many great ideas never work because the founders can't figure out how to start. Choose ideas that are easy to start with.
4. **Early market feedback.** Do people want it immediately, or does it require months of education?

Average these for a rough quality score. Compare candidate ideas this way. Real YC pivot examples Caldwell scores:
- **Brex:** Pre-pivot VR work-headset (2.5/10). Post-pivot credit card for startups (7.75/10).
- **Retool:** Pre-pivot Venmo-for-UK (5/10). Post-pivot no-code internal tools (~7/10).
- **Segment:** Pre-pivot classroom feedback tool. Post-pivot the data-routing library that they had open-sourced as a side project — the market begged for it before they recognized it as the company.

**Whiplash kills companies more than bad ideas do.** Pivoting too often makes founders sad, and sad founders give up. It's weirdly *better* to work on an idea that isn't the best one if you're having fun, than to whiplash through ideas until you hate your life. Find the happy medium.

**Don't hire while pivoting.** It slows you down and makes employees sad. Only add team members after you have confidence in the idea. *(Stage: Pre-PMF.)*

**It's okay to work on a non-venture-scale idea.** Most businesses in the world don't require venture capital. If you don't want to raise VC, plenty of good companies are still possible — they just won't look like the ones in TechCrunch. Be self-aware about this when choosing what to work on.

## The Eight Mistakes (Michael Seibel)

Drawn from Seibel's "Biggest Mistakes First-Time Founders Make":

1. **Solving a problem you don't care about.** Not fatal — some founders learn to love their problem later. But many startups die because the founders lose motivation, and lack of genuine interest in the problem is a primary cause. The problem you choose should be something you'd commit five-plus years to.
2. **Helping users you don't care about.** Justin.tv struggled in part because the founders weren't in love with their early user base. Twitch worked because the founders genuinely loved the gamer community. The user love has to be there or it will leak out into the product.
3. **Choosing co-founders you don't know well.** Pre-existing relationships (friend, coworker, classmate) matter because startups will stress-test everything. Strangers who incorporate together usually break up.
4. **Not having transparent conversations with co-founders.** The drama-inducing topics that founders avoid: Is my co-founder working as hard as I am? Are we trying to accomplish the same goal? Whose job is engineering vs. product? Resentment builds, then erupts.
5. **Not launching.** Founders imagine launch as a press event that will expose them to harsh public scrutiny. In reality, no one notices. You don't remember the day Instagram launched, or Uber, or Snapchat. Launch sooner.
6. **Not using analytics.** Build with event-based analytics from day one (Mixpanel, Amplitude, etc.). Google Analytics is not enough. You need to know what users actually do, not just where they came from.
7. **Not knowing where your first users will come from.** If you can't name the first 3–10 people you'll get to use the product before you've written a line of code, you don't actually understand who has the problem. Your first users should come from people you already know — friends, former colleagues, your existing network. The "how do I get 100 users" question comes later.
8. **Poor prioritization.** Founders chase sizzle (PR, conferences, investor meetings, hiring) over steak (shipping product, talking to users). Real startup work is making the product better and getting it in front of more people. Everything else is secondary at this stage.

## Building Product Cadence (Michael Seibel)

**Cadence: one to two-week release cycles, maximum.** Anything longer and you're losing the iteration loop that makes startups work.

**The Easy/Medium/Hard triage:**
- Easy ideas: implementable in <1 day
- Medium ideas: 1–2 days
- Hard ideas: a developer's whole cycle

For hard ideas, decompose: which parts are useless, and which are hard? Most hard ideas are also useless — remove them. Build the genuinely valuable hard things first when you have to build hard things at all.

**It will take 2+ years of constant iteration to reach PMF.** This is the realistic expectation. Founders who expect PMF in six months either get incredibly lucky or quit before they would have found it. *(Stage: Pre-PMF.)*

**Identifying the problem is the genius part, not the technology.** Google wasn't a search engine at first. Facebook wasn't a social network at first. Justin.tv wasn't a streaming service for gamers at first. The technology becomes obvious once the problem is clearly identified. The reverse is rarely true.
