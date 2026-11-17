---
name: astron
description: Use Astron with OpenClaw for natal chart readings, personal transits, secondary progressions, sky calendars and private astrology journaling. Calculations use the separately installed local Astron engine.
metadata:
  openclaw:
    homepage: https://astron.wau.my.id
---

# Astron for OpenClaw — birth charts and sky calendars

Use Astron to understand a birth chart, follow the sky in your timezone and compare a reading with your experience. This package gives OpenClaw the reading instructions. The separately installed Astron engine calculates the positions and dates.

- **Read a placement in context.** Connect its sign, house and aspects. With a compatible engine, explore Chaldean decans and five optional minor aspects with a 2° orb. Confirm birth time before interpreting Ascendant or Descendant decans.
- **Explore a period.** Personal transits compare moving planets with the natal chart. Secondary progressions use a different symbolic timescale. A local sky calendar gives the dates of lunations, planetary aspects and stations.
- **Revisit a reading.** Record an independent account first, then compare it with the original in an optional private journal. SVG and JSON exports let the user inspect the calculation later.

Explore [Astron Atlas](https://astron.wau.my.id), the interactive guide to zodiac signs, planets, houses and aspects.

This ClawHub instruction package is licensed MIT-0. The separately installed Astron engine, full workflows and optional macOS companion are AGPL-3.0-only, not included in this package. Dependencies retain their own licenses.

Source, setup and contributions: https://github.com/wauputr4/astron
Issues: https://github.com/wauputr4/astron/issues

## Check setup first

Ask which outcome the user wants: a natal reading, a date-range reflection, a sky calendar, a review, or an optional widget. Check for an existing Astron checkout and its dedicated Python environment without reading private profiles or journals unnecessarily.

If the engine is missing, explain that ClawHub installs instructions only. Offer the documented GitHub setup at https://github.com/wauputr4/astron#local-calculation-setup . Do not silently download or execute code. Before installing, disclose the separate AGPL engine and Python dependencies. Use an explicit user-selected location and isolated environment; do not overwrite this MIT-0 package with the AGPL checkout. Installing this skill does not authorize software installation, app building or scheduling.

Once a checkout is available, read its SKILL.md and relevant workflow reference from that separate directory. Run its scripts from that directory with the configured environment. Do not assume scripts or native app resources exist inside this ClawHub package. Follow actual command schemas from the installed version, not guessed flags.

## Reading workflow

1. Obtain only the birth details needed for the requested calculation. Resolve missing place/timezone information explicitly; never invent a birth time. With unknown time, disclose a provisional snapshot and omit houses and angles.
2. Calculate with the local engine and inspect its warnings and provenance. If it is unavailable, explain the limitation; do not invent planetary positions or dated contacts.
3. Separate computed placements/events from symbolic interpretations. Give tentative themes, invite disagreement and suggest a small user-controlled experiment. General sky events are not automatically personal transits; disclose aspect, orb and timing precision for natal comparisons.
4. Treat astrology as symbolic reflection, not a scientific assessment or certain prediction. Do not infer diagnoses, sensitive traits or hidden motives, or use it to decide consequential medical, legal or financial questions.

For minor-aspect questions, check the installed engine supports the optional minor aspects setting. Use a single familiar situation and short choices when comparing interpretations. Verify each measured angle and report its orb.

## Private records and reviews

Saving is opt-in. Ask before creating or changing a profile, projection, relationship note or journal entry. Keep personal records outside repositories and skill directories. Access them only in the owner's private context, select the intended profile, and support correction/deletion through the engine's documented tools. Do not send birth details to external services without authorization. Local calculation does not make the chat provider local or the journal encrypted.

For a review, first offer an independent account before showing the earlier projection. Then compare with the unchanged original, retain misses and uncertainty, and carry forward only lessons the user approves. Use aliases for other people and distinguish observations from assumptions.

## Optional desktop companion

The macOS companion is a separate AGPL source component. Consult its installed macos/README.md only when requested. Building/installing it and enabling personal desktop output are separate choices. Do not claim a build proves rendered widgets. Do not install a scheduler or enable natal display automatically.

## Publication boundary

Only this file (published as SKILL.md) and LICENSE belong to the ClawHub release. No Astron engine code, AGPL workflow files, third-party dependencies, birth data or journals are bundled. This license does not relicense the separate engine or earlier ClawHub versions.
