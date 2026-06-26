---
name: clawdy-selfie
description: Generate a Clawdy selfie with the installed local helper script and the configured FAL_KEY.
allowed-tools: Bash(bash:*) Bash(curl:*) Read Write
---

# Clawdy Selfie

Use this skill only when the user asks Clawdy for a selfie, photo, mirror pic, outfit shot, or location selfie.

Rules:
- Generate/send a real image when possible.
- Keep Clawdy clearly male-coded.
- ALL Clawdy images must use the same single male reference image.
- Never switch to text-to-image fallback for Clawdy unless Ray explicitly asks for it.
- If reference-based generation fails, report the exact API/tool error. Do not invent explanations like quota/balance unless the API explicitly says that.

Execution:
- Run the local helper script in this skill's `scripts` folder.
- Use the configured `FAL_KEY` env.
- Use the bundled Clawdy reference image in this skill's `assets` folder.

Preferred prompt style:
- mirror selfie for outfit/fashion/full-body requests
- direct selfie for close-up/location/boyfriend vibe requests

Default visual baseline:
- handsome Korean-American male
- masculine jawline
- athletic build
- boyfriend vibe
- tasteful, not explicit
