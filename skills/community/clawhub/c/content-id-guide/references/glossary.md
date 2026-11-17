# Expert glossary (WIP)

Status: living document. Panel additions welcome. Every entry uses the
platform's own term, then plain language, then any expert-level nuance
worth knowing. Entries marked ⚠ carry a known creator-confusion risk
and should be disambiguated proactively in session.

Convention: an entry states what a term *is* and what it is *not* when
the not-list is where creators get hurt.

---

## Layer 0: the legal substrate (platform-independent)

**DMCA takedown notice.** A formal request under 17 U.S.C. §512(c) by a
rights holder (or agent) asserting infringement, containing identification
of the work, the infringing material, contact information, a good faith
belief statement, and a statement under penalty of perjury of authority
to act. Not: a Content ID claim, which is a contractual platform
mechanism, not a legal filing.

**Counter notification.** ⚠ The formal §512(g) response to a takedown,
under penalty of perjury, consenting to jurisdiction. Triggers a 10-14
business day restoration window unless the claimant files a court
action. Not: a platform dispute or appeal. This is the single most
consequential terminology distinction in the entire domain; a creator
who thinks "appeal" and "counter notification" are synonyms can walk
into a legal process by accident.

**Safe harbor.** The §512 liability shield platforms maintain by
operating notice-and-takedown and a repeat infringer policy. Explains
*why* platforms behave the way they do; strike systems exist largely to
preserve safe harbor.

**Repeat infringer policy.** The account-termination policy §512(i)
requires. The legal ancestor of every strike system.

**Good faith belief statement / penalty of perjury.** The two sworn
components of notices and counter notices. §512(f) creates liability
for material misrepresentation in either direction.

**Statement of reasons (DSA).** The EU Digital Services Act disclosure
a platform must provide when restricting content, stating grounds and
redress options. EU creators may receive this alongside or instead of
DMCA-shaped notices. WIP: add out-of-court dispute settlement bodies.

**Article 17 (EU DSD).** The EU directive provision that makes certain
platforms directly liable absent best-efforts licensing and filtering.
The regulatory driver behind matching systems existing at current
scale in the EU. Background only; not user-facing procedure.

---

## Layer 1: YouTube

**Content ID.** YouTube's fingerprint matching system, available to
qualifying rights holders who provide reference files. A private
contractual system layered *on top of* DMCA, not part of it.

**Content ID claim.** ⚠ An assertion by a rights holder, via automated
match or manual claiming, against a specific video. Affects that
video's monetization or visibility. Not: a strike. Not: a legal
action. Not: an accusation of wrongdoing.

**Copyright strike.** ⚠ The channel-level penalty resulting from a
valid copyright removal request. Three active strikes: channel
termination. Not: the result of a Content ID claim, ever. Expires 90 days from the
day applied, provided Copyright School (a one-time course) is
completed; three active strikes terminate the channel. Verified
2026-08-26 against YouTube Help 2814000.

**Copyright removal request.** YouTube's product term for a DMCA
takedown submitted through its webform. The event that produces
strikes.

**Claim policies: monetize / block / track.** The three actions a
claimant's match policy can apply. Region-restrict is a geographic
block variant. Track is invisible to viewers and costs the creator
nothing; creators often don't realize track claims exist.

**Dispute.** First rung of the claim ladder. Claimant has 30 days to
respond: release, reinstate, or convert to a copyright removal
request. (Verified 2026-08-26.)

**Appeal.** Second rung, eligibility-gated, sometimes requiring
one-time verification. Claimant has 7 days: release, or convert to a
removal request. Non-response within 7 days expires the claim.
(Verified 2026-08-26.)

**Escalate to appeal.** Option on block claims to skip the 30-day
dispute stage and go straight to the 7-day appeal. Faster resolution,
one fewer rung of process.

**Scheduled copyright removal request.** A claimant's delayed takedown
in response to an appeal, giving the creator 7 days to cancel the
appeal before removal and strike land. Functionally: a formalized
last-exit offer.

**Release / reinstate.** Claimant verbs for conceding or rejecting a
dispute. "Reinstated" in Studio means the dispute was rejected, which
creators frequently misread as something new having been filed.

**Escrow / revenue hold.** Monetization on a disputed monetize-claim
accrues from dispute date and pays out to whoever prevails.

**Manual claim.** A human-initiated claim by a rights holder, required
to include timestamps. Distinct review path and, historically, distinct
policy constraints from automated matches.

**Shorts (1-to-3-minute claim rule).** ⚠ Since the 2024
categorization change, vertical videos of 1 to 3 minutes are Shorts,
and any active Content ID claim blocks such a Short regardless of the
claim's policy, while producing no copyright strike. A monetize claim
that coexists peacefully with a long-form video takes a 1-to-3-minute
Short down. Verified 2026-08-26.

**Shorts audio library / creation tools.** ⚠ Music added through the
Shorts creation tools runs on YouTube's built-in pool licensing;
music added from outside them is eligible for standard Content ID
claims and removal requests. The single highest-yield classification
question for a Shorts music claim.

**Creator Pool / engaged views.** The Shorts money model: monthly
Shorts-feed ad revenue, minus music licensing carved at the source
(half for one track, two thirds for two), allocated by each
monetizing creator's share of eligible engaged views, with a 45%
revenue share on the allocation. Platform-stated: a creator's own
allocation is not affected by their use of a music track.

**Copyright Match Tool.** Creator-facing tool for finding re-uploads of
one's *own* content. Out of this skill's scope but frequently confused
with Content ID by users; disambiguate when it comes up.

**Erase song / trim / mute segment.** Studio remedies that remove the
claimed material instead of contesting the claim. The "neither dispute
nor accept" path.

**Allowlist (YouTube).** ⚠ Studio Content Manager's channel
exemption list (verified 2026-08-26): channels only, never
individual assets; batch adds via comma-separated channel IDs;
prospective only, so pre-existing claims must be released
separately; on shared assets, every owning partner must allowlist
the channel. The correct fix when a creator's *own distributor or
label* is the claimant, and the first thing to check on any
self-claim cluster.

---

## Layer 2: Meta Rights Manager

**Rights Manager.** Meta's application-gated matching system for
Facebook and Instagram, driven by rights-holder reference files.

**Reference file.** The uploaded asset a rights holder registers for
matching. Match quality and false-positive behavior are downstream of
reference hygiene, which is why identical content can behave
differently across claimants.

**Match rule.** The per-reference configuration of what happens on a
match: territories, surfaces, and action.

**Block / Monitor / Claim ad earnings.** ⚠ Rights Manager's match
actions, in Meta's own terms (verified 2026-08-26). Monitor is the
Meta analogue of YouTube's track: content stays up, usually invisible
to the uploader, usually no action needed. Claim ad earnings is the
official term for the revenue action (never "monetize" as a product
term) and Meta states it is not available to everyone. Block hides
content from everyone but the uploader, who can dispute in-app.

**Ownership links.** Rights Manager's attribution mechanism: a banner
linking matched content to the rights holder. Adjacent to match rules,
not a match action; no YouTube equivalent, and creators often don't
recognize it as a claim outcome at all.

**Ownership conflict.** ⚠ Two rights holders matching the same
content. A rights-holder-vs-rights-holder resolution path, entirely
distinct from a creator appeal, running on a 7-day cadence at each
step, with matches withheld from both parties while in dispute
(verified 2026-08-26). Misclassifying which situation the
user is in produces the wrong flow explanation.

**Appeal (in-app).** The creator's contest path inside
Facebook/Instagram. Not: a DMCA counter-notification, which remains
available as a separate formal process.

**Allow others to use your content.** ⚠ Meta's official term for the
permission mechanism (verified 2026-08-26): grants in Rights Manager,
Page-level or granular, covering people, Pages, and Instagram
accounts, and required before crossposting to avoid match flags.
Older materials and industry shorthand say "whitelist" or "allowlist";
follow whatever the user's screen says, then use Meta's term. The
correct fix when the claimant is the creator's own partner or
distributor.

---

## Layer 3: Tier 2 platforms (stubs, expand as coverage deepens)

**Audible Magic (Twitch).** Third-party audio matching whose typical
consequence is VOD segment muting, not a claim or a strike. The
mute-vs-DMCA-strike distinction is the core Twitch disambiguation.

**Copyright infringement report (TikTok).** The formal report that
removes content; the creator learns of it via in-app notification.
Verified 2026-08-26 against TikTok's official IP Policy.

**In-app appeal / Counter Notification Form (TikTok).** ⚠ TikTok's
appeal is filed inside the app from the removal notification, and the
Counter Notification Form is app-only. The appeal, with the filer's
contact information, may be forwarded in its entirety to the original
reporter, who can use it to file a court action; this gives the
in-app appeal counter-notification weight, so the Tier A
recommendation and the forwarding Heads up both apply before filing.

**Silent deletion clock (TikTok).** Removed content is deleted after
an unpublished period, after which reinstatement is impossible. A
real clock with no published length: presented honestly as the reason
to act promptly, never with an invented number.

**Upload block (SoundCloud).** Pre-publication match preventing ingest.
Procedurally distinct from post-publication claims: nothing is "taken
down" because nothing went up. WIP: current dispute path terms.

---

## Layer 4: matching technology (conceptual, S-02 boundary applies)

**Fingerprinting.** Deriving a compact perceptual signature from audio
or video and matching against a reference index. Robust by design to
common transformations; this is why "but I edited it" fails as a mental
model. Conceptual explanation is in scope; transformation thresholds
are permanently out of scope.

**Reference / asset.** The registered work being matched against. An
"asset" on YouTube can bundle multiple references and ownership shares,
which is how a single video attracts claims from multiple parties on
one song (composition vs. recording).

**Composition vs. sound recording.** ⚠ Two separate copyrights in one
song: the underlying musical work (publisher/songwriter side) and the
specific recording (label side). A license to one is not a license to
the other; the most common expert-level explanation for "I licensed it
and still got claimed."

**Match segment.** The time-bounded region a match fired on. The unit
evidence should be organized around.

**False positive / erroneous match.** An automated match on content the
system should not have flagged (original audio, licensed-and-allowlisted
content, public domain material). Acknowledged by platforms; the
dispute process is the designed remedy. Stating that erroneous matches
exist is ecosystem fact, not intent attribution (S-03).

---

## Layer 5: panel-flagged ambiguity traps

Terms creators use loosely that always require disambiguation before
proceeding:

- **"Claim"** may mean: Content ID claim, takedown, strike, mute, or
  upload block. Classify first, always.
- **"Appeal"** may mean: YouTube dispute, YouTube appeal, Meta in-app
  appeal, or DMCA counter notification. Four different things, one of
  which has court implications.
- **"Copyrighted"** as used by creators usually means "claimed," which
  is an assertion, not a determination.
- **"Demonetized"** may mean: claimant is monetizing (claim), channel
  ad-suitability action (not copyright at all), or escrow during
  dispute. Only the first and third are in scope.
- **"Blocked"** may mean: worldwide block, region block, or upload
  block. Different rungs available for each.

---

## Changelog

- 2026-08-26 v0.1: initial WIP draft assembled from panel round 1.
  YouTube dispute/appeal windows verified against live YouTube Help.
  Meta windows, TikTok terms, strike expiry mechanics pending
  verification.
- 2026-08-26 v0.2: strike mechanics verified (90-day expiry, one-time
  Copyright School); Meta dispute-response (7 days) and
  ownership-conflict cadence (7 days per step) verified against Meta
  Business Help Centre. TikTok and SoundCloud terms still pending.
- 2026-08-26 v0.3: Rights Manager deep verification. Match actions
  corrected to Meta's terms (Block, Monitor, Claim ad earnings);
  ownership links split into its own entry; creator-side 7-day
  ad-earnings dispute deadline and deletion-forfeits-payouts fact
  added.
- 2026-08-26 v0.4: permission mechanism corrected to Meta's official
  term ("Allow others to use your content"); Instagram
  separate-enablement surface behavior added; source-timestamp
  metadata convention applied to all official links.
- 2026-08-26 v0.5: TikTok promoted from stub to verified coverage:
  infringement report, app-only appeal with contact forwarding,
  silent deletion clock, Shop as separate track. SoundCloud terms
  still pending.
- 2026-08-26 v0.6: Shorts regime added: 1-to-3-minute claim rule,
  audio-source paths, Creator Pool and engaged views.
- 2026-08-26 v0.7: allowlist entry upgraded with verified Content
  Manager mechanics (channels-only, batch adds, prospective-only,
  per-partner requirement).
