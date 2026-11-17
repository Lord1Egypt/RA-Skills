# Disclosure: every campaign clip says it's paid

A clip made for a paid clipping campaign is an ad, also when it is paid per view and the clipper
gives no opinion. Content Rewards says all content posted for one of its campaigns is a material
connection. Advertising law in the US (FTC), the UK (CMA, which can fine directly since the DMCC
Act) and the EU (consumer protection law) asks for a clear disclosure. A lawsuit filed in June 2026
targets a campaign that told clippers not to make it feel like an ad.

The skill makes disclosure part of the clip, not an option.

## Three places, every time

1. **On screen at the start.** `make_clips.py` draws the campaign's `on_screen.disclosure`
   ("Paid partnership with <brand>", or "Ad") at the top for the first seconds (4 by default).
   Content Rewards' terms say the disclosure for video clips must appear at the beginning.
2. **First in the caption.** The caption starts with `#ad` (or the brief's stronger wording), so it
   shows before "more". Not acceptable: `#sp`, `#spon`, `#collab`, a brand tag alone, a disclosure
   buried among hashtags or only in a comment.
3. **The platform's setting.** TikTok's paid partnership label is sent with the post
   (`isBrandedContent: true`). WoopSocial can't set Instagram's paid partnership label or YouTube's
   paid promotion box, so the plan page and the submission sheet list them as steps in the app,
   inside the 30-minute window.

If the user appears on camera or adds a voiceover, they also say it in the first 10 seconds
("This is a paid partnership with ...").

## What is refused

- A campaign file without a caption or on-screen disclosure, or one that doesn't say it's paid.
- `#ad` on the brief's banned list.
- A clip without the on-screen disclosure (`check_clips.py` reads it from the manifest; a clip the
  user made is declared after watching it).
- A caption that doesn't start with the disclosure, or that plays it down.
- A TikTok campaign post set to "only you" (TikTok doesn't allow branded content there, and it
  earns nothing).

## Brief text that asks to hide it

`campaign.py` flags sentences like "don't make it feel like an ad", "no #ad", "don't disclose",
"act natural", "don't use the paid partnership label", "posts with #ad will not be approved",
"disclosure is not required", "turn off the branded content toggle" or "nobody should know it's
sponsored". They are shown under "Never followed" on
the checklist and the plan page. Tell the user once, in plain words, and carry on with the
disclosure in place. If the user insists on removing it, decline: the skill doesn't make
undisclosed campaign posts.

Sentences that ask for a different wording of the disclosure are fine; only hiding it is refused.
"Posts without #ad will be rejected" asks for the disclosure and isn't flagged. A sentence where the
disclosure itself causes the rejection ("with #ad ... not approved", "looks like an ad ... rejected")
is flagged. Sentences about the disclosure next to a "no" or a rejection that the patterns can't
place are listed under "Read these sentences yourself": read each one. The patterns can't catch
every phrasing, so read the brief yourself as well.

## A brief that forbids the disclosure on screen

"No paid partnership text on the video", "no text overlays": the brief and this skill disagree.
`campaign.py` lists them under "Conflicts with the disclosure rule". The skill still draws the
disclosure. Tell the user to ask the campaign team in writing whether a short "Ad" for the first 2
seconds is accepted, or to skip the campaign.

## Your own content

A creator clipping their own content onto their own accounts isn't paid by anyone for it:
`"own_content": true` in campaign.json drops the paid disclosure. TikTok's "Your brand" label
(promotional content) is for clips that promote the creator's own product, service or business
(`"promotes_own_business": true`, asked); clips of their show or stream alone get no label. The
moment someone pays for the views, it is a campaign again: `campaign.py` refuses `own_content`
with a marketplace, a brand, a rate, a payout rule, a budget or a fee, or with a brief that talks
about hiding the ad. A creator who pays clippers runs a normal campaign, and the clippers' posts
are disclosed.

## Not legal advice

These are the marketplace's and regulators' published rules as of November 2026. A user with a
specific legal question should ask a lawyer where they live.
