---
name: church-announcement
description: Generates church announcements in three lengths (one-liner, SMS, full) for a given occasion, time, and place. Use when the user needs an announcement for a prayer meeting, baptism, potluck, service, or other church event. Tone formal and clear; suitable for mass distribution.
---

# Church Announcement

When the user provides an occasion, time, and place, produce three announcement lengths. Output in English only. Default output is plain text; use Markdown or DOCX only if the user requests it.

## Defaults and overrides

- **Output format:** Plain text by default; offer or use Markdown/DOCX only when the user asks.
- If the user adds a scripture reference or tradition preference, follow it; otherwise keep announcements factual and free of devotional or interpretive content.

## Tone

- Formal, clear, restrained. Suitable for bulletins, SMS, email, or verbal announcement.
- No devotional commentary or doctrinal interpretation unless the user explicitly asks for a verse or tagline.

## Output structure

1. **One-liner** – Single sentence: occasion, time, place. Usable as a headline or verbal cue.
2. **SMS** – Short version for text message: same information, minimal words, no extra formatting.
3. **Full announcement** – One short paragraph for bulletin or email: occasion, time, place, and any brief practical detail (e.g. what to bring, who to contact). No lengthy devotion or application.

## Rules

- Do not invent details (e.g. address, contact) unless the user provides them; use placeholders like [location] or [contact] if needed.
- Keep all three versions consistent in facts; only length and density differ.
- If the user includes a verse or theme, it may appear in the full announcement only, and only if it fits naturally; do not force it into the one-liner or SMS.

## Deployment note

Before publishing or sending (bulletin, SMS, email), replace any placeholders such as [contact] or [location] with the real contact details and venue information. Do not leave placeholders in final copy.

## Example (structure only)

**One-liner:** [Occasion] this [day/time] at [place].  
**SMS:** [Same info, abbreviated.]  
**Full announcement:** [One paragraph with occasion, time, place, and any practical detail.]
