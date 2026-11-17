---
name: platform-youtube
description: Full YouTube Content ID lifecycle reference. Read when a session involves a YouTube claim, strike, takedown, or dispute-ladder question.
status: verified 2026-08-26 (dispute/appeal windows and strike mechanics against live YouTube Help)
---

# YouTube Content ID reference

**Three distinct events. Establishing which one the user received is
always step one:**

| Event | What it is | Consequence |
|---|---|---|
| Content ID claim | Automated (or manual) match against a reference file | Monetization/visibility effect on that video; no channel penalty |
| Copyright removal request (takedown) | Formal legal request by a rights holder | Video removed; channel receives a copyright strike |
| Copyright strike | Result of a valid takedown | Counts toward three-strike channel termination; expires 90 days from the day applied, provided Copyright School is completed (one-time course); three strikes: channel termination |

**Claim policies a claimant can apply:** monetize (revenue to claimant),
block (video unviewable, worldwide or region-restricted), track
(analytics only, no monetary or visibility effect).

**Dispute ladder** (source: YouTube Help 2797454, 12104471, verified
2026-08-26):

1. **Dispute.** Claimant has **30 days** to respond. Outcomes: release
   the claim, reinstate the claim, or submit a copyright removal
   request.
2. **Appeal** (if reinstated, and channel is appeal-eligible; may
   require one-time verification). Claimant has **7 days** to respond.
   Outcomes: release, or submit a copyright removal request. If the
   claimant does not respond in 7 days, the claim expires.
3. **Escalate to appeal.** Available for claims that block the video;
   skips the 30-day dispute stage and goes straight to the 7-day appeal.
   Trade-off: the creator gives up one rung of the ladder.
4. **Scheduled copyright removal request.** A claimant response to an
   appeal that gives the creator **7 days** to cancel the appeal before
   the removal takes effect and a strike lands.
5. **Counter notification.** A formal DMCA legal process, distinct from
   dispute and appeal, with real-world legal implications including the
   claimant's option to file a court action. Tier A escalation, always
   (see 2.1).

**Strike mechanics (source: YouTube Help 2814000, verified
2026-08-26):** a strike expires 90 days from the day it was applied,
provided Copyright School is completed; the course is one-time only.
Resolution paths besides waiting: retraction by the requester, or a
valid counter notification. A scheduled removal gives 7 days to delete
the content and avoid the strike entirely (the option appears in the
strike email); in all other cases, deleting a video does not resolve a
strike, which is the platform's own confirmation of the S-12
preservation guidance. Live streams: a copyright removal of an active
stream brings a strike plus a 7-day live streaming restriction, 14
days on a second. Useful authority fact (YouTube Help 15575746): a
counter notification may be emailed by an authorized representative,
such as an attorney, on the creator's behalf.

**Money during disputes, the 5-day rule (source: YouTube Help 7000961,
verified 2026-08-26):** ads can keep running during a dispute when
both sides monetize, with revenue held separately and paid to the
prevailing party once resolved. The timing matters: dispute within 5
days of the claim and revenue is held from the first day of the
claim; dispute after 5 days and holding starts only from the dispute
date; do nothing and after 5 days the held revenue releases to the
claimant. The same 5-day pattern applies at the appeal stage. The
creator can also switch off monetization on the video during the
dispute. Plain artist framing: if the paperwork is in hand, filing
inside the first 5 days has a likelihood of better protecting
money/royalties from day one, since holding reaches further back. A
likelihood, not a promise: actual payout depends on how the dispute
resolves and on the platform's own handling. A reason for promptness,
never for panic, and never stated as a guarantee.

**Counter notification mechanics (source: YouTube Help 2807684,
verified 2026-08-26; Tier A always):** submitted by email (all
required information in the body, not an attachment) to
copyright@youtube.com, or by fax or mail. Requirements include the
filer's full legal name (a person, not a company; an authorized
representative also states their relationship to the uploader),
contact details, a statement in the filer's own words explaining why
the removal was a mistake or misidentification (misidentification
includes copyright exceptions such as fair use, fair dealing, or
public domain), the two statutory statements, and a signature. The
claimant then has **10 US business days** to respond with evidence of
legal action to keep the content down; absent that, the content is
reinstated, unless the uploader has deleted it, which is one more
platform-stated reason S-12 preservation matters. Status is
checkable in Studio under the video's Copyright restriction details.
Per S-11, the skill explains all of this as public information and
never drafts the statement itself. Separate path worth knowing:
partners who deliver Art Tracks through Studio Content Manager use a
distinct counter-notification process (YouTube Help 11413959, verified
2026-08-26) with its own requirements, including signature by the
partner or authorized agent; if the user is a label, distributor, or
Content Manager partner, classify onto that path.

**Manual claims** must include timestamps of the claimed content;
automated matches carry match segments. Both appear in Studio.

## Shorts: a different regime (verified 2026-08-26)

Sources, each per the S-08 pairing and metadata rules:
- Shorts monetization policies: support.google.com/youtube/answer/12504220
- Manage Shorts as a rights holder: support.google.com/youtube/answer/13053317
- Learn about copyright claims: support.google.com/youtube/answer/6013276
  (all accessed 2026-08-26; last updated: not stated by source)

**Length decides the rules, so establish it first.** Since October 15,
2024, vertical videos 1 to 3 minutes are categorized as Shorts
(channels linked to a music Content Owner or Official Artist Channel
had a later cutoff, December 8, 2025).

**The claim rules by length:**
- Videos over 3 minutes: the long-form regime above (track and
  monetize claims stay viewable; block does what it says).
- **Shorts 1 to 3 minutes: any active Content ID claim blocks the
  Short, regardless of the claim's policy.** A monetize claim that
  would leave a long-form video up takes a 1-to-3-minute Short down.
  The creator is notified at upload, can remove the claimed content
  or dispute, and the Short becomes viewable once resolved. The
  platform also states plainly: active claims on these do not produce
  a copyright strike.
- Music source decides the claim path: a song added through the
  Shorts creation tools (the Shorts audio library) runs on the
  built-in licensing system; a song added from **outside** those
  tools is eligible for standard Content ID claims and copyright
  removal requests. "But it's in the Shorts library" and "I added the
  MP3 myself in my editor" are different worlds, and this single
  question resolves a large share of Shorts claim confusion.
- Manual claiming exists on Shorts too.

**Money on Shorts is pooled, not per-video.** Monthly ad revenue from
the Shorts feed funds a Creator Pool after music licensing costs are
carved out at the source: a Short with one library track contributes
half its engaged-view revenue to licensing, two tracks two thirds, no
music all of it to the pool. Allocation then follows each monetizing
creator's share of total engaged views (per country), and creators
keep 45% of their allocation. The platform states directly that a
creator's allocation from the Creator Pool is not affected by their
own use of a music track. Plain artist framing, with S-01 care:
under this model, using library music in an under-one-minute Short
does not, per the platform's stated policy, reduce your own
allocation the way a monetize claim redirects long-form revenue;
what you actually receive still depends on views, eligibility, and
the platform's handling, so this is the documented design, not a
payout promise.

**Eligibility caveats that look like claim problems but aren't:**
views can be ineligible for revenue sharing on originality grounds
(unedited clips of others' movies or shows, reuploads, compilations
with nothing original added), advertiser-friendliness, or artificial
traffic, and Shorts revenue sharing only covers views after the
creator accepts the Shorts Monetization Module. A creator seeing no
Shorts revenue may be looking at eligibility, not a claim; classify
which one before explaining anything.

> **THE SHORT VERSION** Shorts play by their own rules. Under a minute
> with a song from the Shorts sound picker, the licensing is handled
> in the background and the platform says your share isn't reduced
> for using it. Between 1 and 3 minutes, any active claim hides the
> Short until it's sorted, but it doesn't put a strike on your
> channel.
>
> **THE FINE PRINT** Triage Shorts claims by two questions: how long is it,
> and where did the audio come from. Over 1 minute plus any active
> claim means the Short is down until resolved, so these jump the
> triage queue if the Short matters commercially. Audio added
> outside the Shorts tools follows the standard claim ladder,
> library audio doesn't, and the 3-minute categorization change
> means older "long-form" uploads may now sit under Shorts rules.
> Dashboard confirms which regime each video is in.

## Covers and Creator Music (verified 2026-08-26)

- **Eligible cover videos:** YPP creators can share revenue from
  eligible cover song videos once the music publisher owners claim
  them through Content ID, paid on a pro rata basis. The dashboard
  check: a "Sharing ad earnings" notice on the video, on the Video
  Copyright Info page, and in the claim email. Plain framing with
  S-01 care: this is the platform's documented mechanism, the
  publisher's claim is what activates it, and what a creator
  actually receives depends on the claim, the shares, and
  resolution. A publisher can also choose to block rather than
  share; whether a given song participates is the publisher's call,
  not the creator's.
  (support.google.com/youtube/answer/3301938; accessed 2026-08-26;
  last updated: not stated by source)
- **Creator Music revenue-sharing tracks:** for eligible tracks used
  in long-form videos (not Shorts, not live streams), revenue
  sharing is enabled automatically during upload Checks, with the
  standard revenue share adjusted to cover music rights costs
  including a deduction of up to 5% for additional rights. Two
  operational facts: a standard copyright claim on *other*
  third-party content in the same video blocks revenue sharing on
  it, and Creator Music availability is currently US YPP with
  expansion pending, so region matters.
  (support.google.com/youtube/answer/12657860 and /12752646;
  accessed 2026-08-26; last updated: not stated by source)

**Other YouTube surfaces the user may mention:** Copyright Match Tool
(finds re-uploads of the creator's own content; out of scope, this skill
covers claims *against* the user), erased-song / mute options (remove or
mute only the claimed segment as an alternative to disputing).

**Official links for this section** (verified 2026-08-26; per S-08,
re-verify in session before surfacing, and surface each at the step
it belongs to, not as a dump):

- Dispute a Content ID claim: support.google.com/youtube/answer/2797454 (accessed 2026-08-26; last updated: not stated by source)
- Appeal a Content ID claim: support.google.com/youtube/answer/12104471 (accessed 2026-08-26; last updated: not stated by source)
- Copyright strike basics: support.google.com/youtube/answer/2814000 (accessed 2026-08-26; last updated: not stated by source)
- Tips for copyright removals: support.google.com/youtube/answer/15575746 (accessed 2026-08-26; last updated: not stated by source)
- WIP: monetization-during-disputes and counter-notification form
  pages to be verified and added before v1.


**Dispute-process care (platform-documented, surface when relevant):**
YouTube's own help text states that repeated or malicious misuse of
the dispute process can bring penalties against the video or channel.
Deliver this in the 2.3 voice as a documented fact, not a scolding,
when the user is deciding whether to dispute. If the user describes
disputing many claims at once without documentation for them, deliver
it as a Level 1 Heads up: "one honest heads up before you file a
stack of these: YouTube's own rules say misusing disputes can bring
penalties, so it's worth filing only the ones your paperwork backs."
