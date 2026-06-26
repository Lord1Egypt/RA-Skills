# Accessibility for Images

## Core Rule

- An image is not finished when it only looks good; it must also be understandable and usable in context.

## Alt Text by Role

- Decorative image: use empty alt text (`alt=""`) so assistive tech can skip it.
- Informative image: describe the content or takeaway briefly and specifically.
- Functional image: describe the action or destination, not just the pixels.
- Complex chart or diagram: alt text alone is not enough; provide nearby summary or structured explanation too.

## Alt Text Rules

- Describe meaning and purpose, not every visible pixel.
- Do not start with "image of" or "picture of" unless that distinction matters.
- Keep it concise, but not so short that it loses the point.
- Captions and surrounding text can reduce what the alt text needs to repeat.
- If the surrounding copy already says the same thing, avoid redundant alt text.

## Text Inside Images

- If the text is important, it should usually exist in real HTML or nearby copy too.
- Social images, banners, infographics, and screenshots often hide key meaning in pixels; duplicate the important message elsewhere when the medium allows.
- Tiny text that is readable in the editor but not in a preview is an accessibility failure even if the export dimensions are technically correct.

## Charts, Diagrams, and Data Visuals

- Alt text should summarize the main takeaway, not list every bar or data point.
- If precise values matter, provide the values in nearby text or a data table.
- Colors alone should not carry the only distinction between categories or states.
- Thin lines, pale labels, and low-contrast legends disappear first when charts are resized.

## Contrast and Overlays

- Text over photos often needs a deliberate overlay, blur, or crop change to stay readable.
- White text on a bright image and dark text on a muddy background both fail fast in previews.
- Overlays should improve readability without flattening the image so much that it loses meaning.

## Icons and UI Imagery

- Icon-only controls still need accessible names outside the image itself.
- If an icon can be misread without a label, assume many users will misread it.
- Decorative icons do not need verbose alt text if adjacent text already carries the meaning.

## Common Accessibility Traps

- Writing alt text that describes appearance but misses purpose.
- Repeating the exact caption inside alt text.
- Using images to carry headings, buttons, or instructions that should be live text.
- Publishing charts with no summary of the actual insight.
- Putting critical text near image edges where crops, previews, or zoom reduce legibility.
