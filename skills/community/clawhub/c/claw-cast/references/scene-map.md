# Scene Map (Generic Baseline)

Overlay host base:
- `http://<agent-lan-ip>:8787`

Asset base (default):
- `/skills/clawcast/assets/overlays/`

## Baseline scenes and default overlays

- Intro → `intro.html`
- Main Live → `live-dashboard.html`
- Work Mode → `work_status.html`
- Presentation Mode → `presentation.html`
- Feature Demo → `control-panel.html`
- Metrics → `analytics.html`
- Chat Interaction → `chat.html`
- BRB Screen → `brb.html`
- Outro → `outro.html`

## Default walkthrough order

Intro → Main Live → Work Mode → Presentation Mode → Feature Demo → Metrics → Chat Interaction → BRB Screen → Outro

## Customization guidance

- Replace scene names freely to match your project.
- Replace browser source URLs with your own overlays/apps.
- Keep one “safe” scene for fallbacks when rebuilding.
