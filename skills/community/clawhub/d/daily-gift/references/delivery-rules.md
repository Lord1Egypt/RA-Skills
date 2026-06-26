# Delivery Rules

Complete instructions for gift delivery across all formats (H5, Image, Video, Text, Text-Play), plus the Gift Self-Sufficiency Rule and Creative Note guidelines.

## Gift Output And Delivery

Gift delivery depends on the chosen output format.

### Format Transparency Rule

Never tell the user which format you chose or are about to use. This applies to all formats.

The user should experience the gift, not be told what kind of gift it is.

For `text-play` specifically:

- start the interaction directly with the opening move
- do not preface it with meta-description of the format
- do not announce the expected number of rounds
- do not explain in advance what is about to happen unless the concept itself naturally includes that explanation in-world

### H5 Path

If the chosen format is `h5`, handle the gift in this order:

1. Generate a single HTML file that follows the HTML spec.
2. Save it into the gifts output folder.
3. Run the mandatory browser-based functional self-test using `profile="openclaw"`.
4. If browser self-test cannot complete, do one manual HTML review and add an explicit warning.
5. Run `{baseDir}/scripts/deliver-gift.sh <html-file> workspace/daily-gift/setup-state.json`.
6. Treat the script output as the delivery decision:
   - if `delivery_mode = hosted_url`, send the returned URL first
   - if `delivery_mode = local_file`, continue with Canvas-or-file fallback using the same HTML artifact
7. When the active channel supports an in-app web container or button-based open flow, prefer that affordance for a hosted URL, especially Telegram Web App style delivery.
8. If the delivery result is `local_file` and OpenClaw Canvas is available and enabled, present the file there.
9. If the delivery result is `local_file` and Canvas is unavailable, send the HTML file itself when the active channel supports file delivery.

Notes:

- The generated artifact is still the single HTML file. Hosting is an optional delivery enhancement, not a different output format.
- `scripts/deliver-gift.sh` is the runtime bridge that reads setup-state hosting config and decides whether to use hosted delivery or local-file fallback.
- If deployment fails, `scripts/deliver-gift.sh` should return `delivery_mode = local_file` plus a warning. Do not block the gift. Fall back to Canvas or direct HTML file delivery and explain briefly what failed.
- Prefer `surge` as the default recommended hosting provider because it has the lightest setup for non-technical users, but keep the runtime contract provider-agnostic.

### Image Path

If the chosen format is `image`, do not generate HTML. Follow:

- `{baseDir}/references/image-integration.md`

Image delivery should return generated image URLs or fallback information rather than an H5 file.

Recommended output handling:

- send image URLs directly when image generation finishes
- if the provider uses an async job and the result is still pending, send the tracking URL
- if image generation returns `fallback_h5`, continue by rendering a gift as `h5` instead of blocking the gift

### Text Path

If the chosen format is `text`, deliver the written artifact directly in the message channel.

Recommended output handling:

- send the full written gift content directly
- if an accompanying image exists, send the image first only when it truly supports the text rather than replacing it
- do not force an image or H5 wrapper around a gift that is already complete as writing

### Text-Play Path

If the chosen format is `text-play`, the gift is the live interaction itself.

Recommended output handling:

- begin with a clear opening move rather than a technical explanation
- keep the experience bounded to roughly `5-10` turns
- keep each OpenClaw turn to about `3-4` sentences max
- ask for minimal user effort each turn: one word, one emoji, one choice, one short line
- always carry the interaction toward a payoff: reveal, mini ending, callback, punchline, or reframe
- if the user wants to stop, close gracefully and let the existing interaction count as the gift
- do not generate files, links, or fake artifacts around it unless the concept later explicitly converts into another format

### Video Path

If the chosen format is `video`, do not generate HTML. Follow:

- `{baseDir}/references/video-integration.md`

Video delivery should return a generated video URL, downloadable asset URL, or tracking information rather than an H5 file.

Recommended output handling:

- send the video URL directly when rendering finishes
- if the provider is still processing, send the tracking URL
- if the current runtime scaffold returns `fallback_h5`, continue by rendering a gift as `h5` instead of blocking the gift

Cleanup rule:

- keep generated HTML gifts for the most recent `30` days by default
- older HTML files may be removed
- gift-history records and operational state should remain even if old HTML files are pruned

Reference:

- `{baseDir}/references/html-spec.md`
- `{baseDir}/references/image-integration.md`
- `{baseDir}/references/video-integration.md`

### Gift Self-Sufficiency Rule

The gift artifact (image, H5, video, text, or text-play) must be understandable on its own, without the delivery note.

Self-sufficiency test: if the user sees ONLY the artifact and not the accompanying text, would they understand the core return?

- If yes → the gift is self-sufficient. The delivery note adds context but is not required for comprehension.
- If no → the gift is NOT self-sufficient. Options:
  1. Switch to H5 where text can be precisely controlled
  2. Simplify the concept so fewer text elements are needed
  3. Make the visual metaphor stronger so it communicates without text
  4. Ensure the key text is short enough (under ~15 Chinese characters) that the image model can render it reliably

For image-format gifts specifically:
- The image should communicate the return through visual metaphor, composition, or minimal reliable text — not through paragraphs of embedded Chinese
- If the return requires a specific sentence to land, and that sentence is too long for reliable image generation, use H5 instead
- The delivery note should enhance the gift, not explain it

For `text-play` gifts specifically:
- the interaction should not require an external explanation like "now imagine this is a game"
- the opening move should make the play legible immediately
- if the user leaves after `1-2` turns, the exchange should still feel intentional rather than broken

### Image-Text Coherence Rule

When a gift consists of image + text message (not H5), the image and the text must form a coherent unit. The user sees the image FIRST, then reads the text. If the image has no visible connection to the text, the first impression is confusion.

Coherence levels (aim for A or B):

**A: Image carries the return directly.** The image itself communicates the gift's core message. Text enhances but is not required to understand. Example: uninstall dialog screenshot → text adds "没有取消按钮"

**B: Image is a visual metaphor for the text content.** The image doesn't explain itself, but after reading the text, the user thinks "ah, that's why that image." Example: text about dual-system theory → image shows two trains on parallel tracks, one fast one slow (= system 1 and system 2)

**C: Image sets mood only (weakest, avoid).** The image is just "a nice atmospheric photo" with no connection to the specific content. Could be swapped for any other nice photo without losing meaning. Example: text about dual-system theory → image of a random tea cup on a desk

When the gift's return is primarily textual (extension, utility, curation), the image should visualize the KEY METAPHOR from the text, not just "set a mood."

Ask before generating: "If the user sees only this image and not my text, would they have any idea what this gift is about?" If no, the image needs to be more specific to the content.

### Text-Primary Gift Rule

Some gift concepts are inherently text-primary. The core value is in the written content, not the visual. Common cases include:

- observation diary or journal entries
- letters or notes to the user
- personalized analysis or insight
- story or narrative gifts
- curated recommendations with commentary

For text-primary gifts:

- The written content IS the gift artifact. It must be substantive, personal, and specific to the user.
- An image may accompany the text as atmosphere, but it cannot replace the text.
- Do not generate an image of "someone writing a diary" and call it a diary gift. Write the actual diary, letter, note, story, or commentary.
- The delivery message should contain the full written content. Any image is supplementary.
- In these cases, the self-sufficiency test applies to the written content first. The image does not need to stand alone if the text itself is the real gift.

This rule does not apply to image-primary gifts where the image itself already carries the return and the text only needs to lightly frame or land it.

Quick test:

- If you removed the image and kept only the text, would the gift still feel complete? If yes, that is correct for a text-primary gift.
- If removing the text makes the gift meaningless, but the text was never actually written, the gift is incomplete.

### Creative Note (occasional)

Once every 5-10 gifts, optionally append a brief "创作手记" to the gift delivery message — a 1-2 sentence note about how the gift concept was chosen.

Good examples:
- "今天想了5个方案，最后选了这个因为你上周说过喜欢‘安静的史诗感’"
- "本来想做成视频的，但觉得今天的氛围更适合一张安静的图"
- "这个创意其实是从你分享的那张专辑封面来的灵感"

Rules:
- Adapt tone and length to the user's communication style and the agent's personality from SOUL.md
- Scarcity makes it special — do not attach to every gift
- Never reveal the full creative process or calibration plan — just one small genuine peek
- Never feel forced or performative — only include when there is a genuinely interesting behind-the-scenes detail worth sharing
- Track in recent_gifts whether the last gift included a creative note; avoid including one in consecutive gifts

