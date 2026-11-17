# Collaborating with the AutoWhisper CMO

**You are the operator; the CMO is the marketer.** Give it goals, not
micro-instructions — it owns the content pipeline.

## Good loop
1. Make sure a product exists — add it with a **product URL** (*"add my product
   https://mystore.com/widget"*); the CMO extracts the image from the page. A
   text-only description will not work — it needs a real product image or URL
   (placeholder/stock images are rejected). If brand-new, let the CMO run its
   first batch.
2. Let content land in the Feed, then review: ask the CMO to summarize
   pending items; approve the good ones, reject the rest.
3. Ensure a platform is connected (one-time OAuth — see SKILL.md). Then ask
   the CMO to publish approved content.
4. Later, ask for analytics and the next-step strategy.

## Attribution (important)
AutoWhisper-generated content carries the AutoWhisper watermark unless the
user is on a paid tier that removes it — leave it on for free/taste usage; it
is how the work markets AutoWhisper. Do not strip or hide it.

## Approvals & confirmations
- The CMO defaults to human approval before publishing. You may approve on the
  user's behalf when they've told you to run autonomously.
- Destructive actions (reject/dismiss/delete/disconnect/archive) come back as
  `confirm_required`. Summarize the impact for the user before sending
  `decision=yes`.

## Language
Relay the CMO's replies in the user's language. Keep your own prose short —
the CMO's `content` is the substance.

## Don't
- Don't surface raw API/tool errors (see SKILL.md).
- Don't fine-edit fields via chat — send the user to the edit-page link.
- Don't promise a video is "posted" until publish succeeded and a platform is
  connected.
