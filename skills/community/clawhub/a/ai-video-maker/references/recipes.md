# Creative recipes

These are plans for user-authorized work, not authorization to spend. Keep the
same actual payload between quote and creation, and use a fresh private recovery
state file for each new logical video. Never create a new task to recover a timeout.

## Product showcase from an image

User: “Animate this product image for a short showcase.”

1. Use their actual image. Ask what feature to highlight only when missing.
2. Write a motion-focused prompt using [prompting.md](prompting.md). Default to
   MiniMax, five seconds, 720p Turbo and 16:9 unless they specified otherwise.
3. With the connection's `firstVideo.flowId`, quote using `--action quote
--firstVideoFlow <flow_id> --scenario product --payload '<json>'`.
   The JSON must contain `content` and `imageUrl`, never `image`.
4. Show the actual quote, settings and balance. After sufficient spending approval,
   use the same arguments without `--action quote`, adding `--approved true
--maxCredits <approved_limit> --stateFile <absolute_private_state_path>`.
5. Deliver the actual playable URL, known charge and 24-hour saving reminder.
   A supplied photo does not guarantee perfect product lettering in every frame.

## Vertical social clip from an idea

User: “Make a five-second vertical clip of a bicycle in a rainy city.”

Use the user's topic and 9:16. Keep the action readable within five seconds.
Use the same quote/approval workflow with `--scenario social` and a `content`
payload. Preserve explicitly requested duration or resolution and quote that
configuration; do not substitute the setup verification quote.

## A transition between two frames

User: “Connect these opening and closing images.”

Confirm which image is first if ambiguous. Use the normal MiniMax workflow with
`content`, `imageUrl` and `lastFrameUrl`. Explain the motion connecting them;
do not mix in reference arrays. Quote, use the approved maximum and preserve a
stable key in a private state file. Do not claim the first-video product guide
provides an editing or assembly engine.

## A complete narrated or captioned production

Plan scenes and requested audio/captions before generation. This skill generates
individual clips; it does not assemble them or supply a dedicated TTS/subtitling
pipeline. Explain the additional tools needed. If a suitable authorized workflow
exists, quote each clip, track the total approved budget and inspect the first
clip before making the rest. Never deliver loose clips as a completed edited film.
