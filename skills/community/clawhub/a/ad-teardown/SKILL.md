---
name: ad-teardown
description: Tear down a competitor's ads into a playbook you can act on. Classify every ad's opening into 7 hook types, cluster the ads into themes, read run-length as the proof of what works, find the angles nobody is running, and write counter-briefs plus a "never say" list. Works from ads you collected yourself (ad libraries, screenshots, transcripts).
license: MIT
---

# Ad teardown

A teardown answers one question: **what is this competitor's playbook, and where is the opening for us?** It works on
the competitor's real ads, collected from the public ad libraries (see the `ad-library-research` skill) or from
screenshots and transcripts the user hands you. Ten to thirty ads from one advertiser is the right size.

## Rule zero: describe only what you were shown

The hook a viewer meets is the **first two seconds of the video**, not the caption. If you have only the copy, say the
teardown is copy-only. Never describe a visual, a statistic or an offer that is not in the material. A teardown that
invents evidence is worse than none, because it gets acted on.

## 1. Log every ad in one line

| Field | What to write |
|---|---|
| Format | image, video, carousel |
| Opening | the first line or first frame, quoted |
| Hook type | one of the 7 below |
| Angle | the promise in a few words ("sleep through the night") |
| Offer | discount, trial, bundle, none |
| Proof | review, number, demo, authority, none |
| CTA | the button or spoken ask |
| Running | start date and how long it has run |

## 2. Classify the openings into 7 hook types

| Type | Looks like |
|---|---|
| Problem-agitate | opens on the pain and makes it worse |
| Social proof | "50,000 people switched", reviews, a creator vouching |
| Question | a direct question the viewer answers in their head |
| Stat shock | a surprising number as the first thing on screen |
| Lifestyle aspiration | the after-state, no problem shown |
| Offer-led | the discount or deal is the opening |
| Curiosity gap | withholds the payoff ("I didn't expect this...") |

Report only the types that appear, each with a count and one quoted example. A brand that runs 80% offer-led openings
is telling you it competes on price.

## 3. Cluster into themes, and weight by run-length

Group the ads by angle. Then sort each group by how long its ads have run. **An ad still live after 60 days or more is
paying for itself**; the advertiser has had every chance to turn it off. The longest-running cluster is their proven
winner. New ads that all share an angle are what they are testing now.

## 4. Find the white space

List 2 to 4 angles that **nobody in the set runs**. Typical gaps: an audience they never address (men, older buyers,
businesses), a use case they ignore, a proof type they never use (a demo, a comparison), an objection they never answer.

## 5. Write the moves

- **Counter-briefs (2 to 3).** Each one exploits a specific weakness you saw: a hook type they over-rely on, a claim
  they cannot make, an audience they ignore. A brief is concrete enough to hand to a designer or a video tool: format,
  hook (with its mechanic), the line, the proof, the ask.
- **Never say (3 to 6 items).** Phrases, claims or territory the competitor already owns. Copying their language makes
  your ad read as theirs. Make each one specific ("'clinically proven sleep'", not "health claims").

## Output shape

```
Competitor: <name> · <n> ads · collected <date> from <sources>
Hook types: problem-agitate 9 ("..."), offer-led 6 ("..."), ...
Themes: 1) <angle>, 4 ads, longest 140 days. 2) ...
Proven winner: <the longest-running ad, quoted, with its run-length>
White space: ...
Counter-briefs: 1) ... 2) ...
Never say: ...
Gaps in this teardown: <what you could not see, e.g. "copy only, no video watched">
```

The last line matters. Say what the teardown could not see, so nobody treats a copy-only read as a full one.
