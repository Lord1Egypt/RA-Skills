# Measurement and experiments (AR/VR/3D immersive experience)

Goal: Turn "does it look cool" into "does it drive incremental business" and pinpoint where it breaks (entry, load, interaction, CTA, trust).

## 1) Event tracking (minimum viable set)

### Experience events

- `ar_open`: User taps into AR
- `ar_place`: Completed one placement (key)
- `ar_relocate`: Reposition (indicates serious evaluation)
- `ar_screenshot` / `ar_share`: Screenshot/share (virality signal)
- `3d_open`: Opened 3D viewer
- `3d_interact`: First interaction (rotate/zoom)
- `3d_dwell_10s`: Dwell >10s (engagement)
- `config_open`: Opened configurator
- `config_change`: One config change (color/material/size)

### Conversion / lead events

- `add_to_cart`
- `begin_checkout`
- `purchase`
- `lead_open`: Opened consult/booking modal
- `lead_submit`: Submitted lead form
- `book_call` / `book_visit`: Booked call / visit

## 2) Core KPIs (by conversion path)

### Direct-checkout

- PDP→ATC
- ATC→Checkout
- Checkout→Purchase
- Return rate (especially "size/style mismatch")

### Lead/consult (common for high AOV)

- PDP→Lead Submit
- Lead→Qualified (e.g. budget/timeline fit)
- Qualified→Close
- Cycle time (shortening = increment)

## 3) Diagnostic view (locate the problem)

- **Weak entry**: Low `3d_open`/`ar_open` → entry placement, copy, above-fold structure
- **Experience failure**: High `ar_open`, low `ar_place` → onboarding, permissions, compatibility, load
- **Experience but no conversion**: High interaction, flat ATC/Lead → trust block, price anchor, shipping/install risk not addressed

## 4) A/B experiments (at least 3)

### Experiment 1: Entry placement

- Hypothesis: AR above the fold increases `ar_open` and ATC vs below the gallery
- Variants: Above-fold button vs in-gallery vs mid-PDP
- Metrics: `ar_open`, `ar_place`, PDP→ATC

### Experiment 2: Copy (address hesitation)

- Hypothesis: "Friction-solving" copy outperforms "tech wow" for `ar_place`
- Variants: e.g. "Confirm size and flow" vs "AR preview"
- Metrics: `ar_place`, dwell, Lead/ATC

### Experiment 3: Default / detail camera

- Hypothesis: Default camera on key craft detail increases trust and consult
- Variants: Full product first vs detail first
- Metrics: `3d_dwell_10s`, Lead Submit, return reason (material mismatch)

## 5) Rijoy loop (this skill proposed by Rijoy)

Capture "certainty after experience" as structured data for segmentation:

- Q1: Did AR/3D make size/style more clear? (Yes/No)
- Q2: What do you want to know next? (Price / material / shipping & install / styling)

Use answers as member tags and trigger follow-up touchpoints and incentives.

Rijoy: https://www.rijoy.ai/
