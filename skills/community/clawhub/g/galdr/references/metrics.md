# galdr Metric Reference

All metrics come from `report.json` and the perception/harmony/melody/overtone stream files in `analysis/<slug>/`.

---

## Pattern (`pattern`)

**Range:** 0.0–1.0
**What it is:** How reliably the music keeps its pattern intact. High pattern means the listener can trust the structure: the pulse, texture, and energy are not suddenly breaking away.

**How it is calculated:** `pattern = 1.0 - disruption`. Disruption is a weighted blend of beat disruption (`40%`), spectral disruption (`35%`), and energy disruption (`25%`). Beat disruption catches missing or off-time expected beats; spectral disruption catches sudden timbral change above local context; energy disruption catches loudness jumps/drops above local trend.

| Value | Meaning |
|-------|---------|
| 0.96–1.0 | Exceptional hold. Listener rarely disrupted. Ritual, minimalist, or tightly composed. |
| 0.90–0.96 | Strong hold. Some variation but listener remains locked. Most engaging tracks. |
| 0.80–0.90 | Moderate disruption. Energy varies meaningfully. |
| <0.80 | Frequent disruption. Chaotic, experimental, or fragmentary. |

**Pattern breaks** are the moments where pattern drops suddenly. Check `pattern_breaks` in report.json for timestamps, intensity, and component breakdown (`beat`, `spectral`, `energy`). Those components tell you whether the break is rhythmic, textural, dynamic, or compound.

---

## Attention (`attention`, `mean_attention`)

**Range:** 0.0–1.0
**What it is:** How strongly attention is being carried forward by the track. Not speed, loudness, or quality — grip. High attention means the music keeps the listener coupled even through quiet or sparse passages.

**How it is calculated:** rolling beat regularity multiplied by beat density over an 8-second window. Regular intervals with enough beat evidence produce high attention; sparse or irregular beat evidence lowers it.

| Value | Meaning |
|-------|---------|
| >0.90 | Rare sustained pull. Track barely lets listener breathe. |
| 0.80–0.90 | Strong. Most engaging passages. |
| 0.60–0.80 | Fluctuating. Energy ebbs and flows. |
| <0.60 | Low continuity. Listener may disengage. |

After a silence, attention re-locking above 0.93 signals the listener has been re-engaged. Multiple re-lock events with deepening silences = structured withdrawal (Helvegen pattern).

---

## Pulse (`pulse`)

**Range:** 0.0–1.0
**What it is:** How steady the underlying pulse feels. Orthogonal to metric complexity — a 7/8 piece can have perfect pulse stability if the body can still trust where the beat lives.

| Value | Meaning |
|-------|---------|
| >0.96 | Clockwork. Ritual, electronic, or highly disciplined performance. |
| 0.90–0.96 | Tight but human. Most performed music. |
| 0.80–0.90 | Loose. Jazz feel, rubato, or intentional groove. |
| <0.80 | Irregular. Experimental or very free. |

High pulse + complex time signature (5/8, 7/8) = metric complexity is orthogonal to pulse stability.

---

## Surface balance (`surface_balance`, `mean_surface_balance`)

**Range:** -1.0 to 1.0
**What it is:** Where the track's weight sits between sustained harmonic sound and percussive impact. Negative values feel more tonal, vocal, droning, or atmospheric; positive values feel more struck, rhythmic, attack-heavy, or drum-forward.

**How it is calculated:** harmonic/percussive source separation energy, smoothed into the perception stream. Very low total energy is treated as neutral so silence does not pretend to have a surface-balance claim.

`surface_evidence` carries the local evidence behind the reading: roughness, noise density, transient attack, sustain/drone, band pressure, surface motion, punch, band weights, and brightness tilt.

| Value | Meaning |
|-------|---------|
| < -0.5 | Strongly harmonic. Warm, tonal, sustained. Choirs, strings, pads. |
| -0.5 to -0.2 | Harmonic dominant with surface detail. |
| -0.2 to 0.2 | Balanced. Mixed character. |
| 0.2 to 0.5 | Percussive with harmonic content. |
| > 0.5 | Strongly percussive. Drum-forward, rhythmic emphasis. |

Deepening negative surface balance across a track = harmonic weight increasing (dissolution, closing, ending accumulation).

---

## Pressure / Heard Pressure (`pressure`, `pressure_state`, pressure summary percentages)

**Shape:** Stream fields plus three summary percentages — building / releasing / sustaining — summing to 100%.
**What it is:** The heard-pressure shape of the track. Pressure is derived from short-term EBU R128/LUFS loudness rather than raw RMS energy so it tracks whether pressure comes forward, holds, or withdraws.

**How it is calculated:** short-term LUFS is smoothed over 20 seconds, differenced, and normalized into a pressure-motion curve. Positive values build, negative values release, near-zero values sustain.

Stream fields:
- `pressure` — normalized pressure movement; positive builds, negative releases, near-zero sustains
- `pressure_state` — `building`, `releasing`, `sustaining`, or `silence`
- `loudness_lufs` — short-term loudness evidence; use for debugging/comparison, not prose
- `pressure_lufs_delta` — short-term pressure delta evidence
- `loudness_silence` — loudness-floor silence marker

| Pattern | Meaning |
|---------|---------|
| ~33/33/33 | Equilibrium. Pressure gives and takes evenly. |
| Heavy building (>45%) | Accumulating track. Pressure keeps coming forward. |
| Heavy releasing (>45%) | Withdrawal dominates, even if the track still feels held. |
| Near-zero sustain (<10%) | No held pressure — constant motion up or down. |
| Heavy sustain (>40%) | Stable hold. The music keeps the listener coupled instead of continually climbing or falling. |

Translation rule: do not write raw LUFS values in experience prose. Write what they mean: pressure comes forward, fills the room, holds, loosens, drops away, empties, or stops carrying attention. LUFS belongs in regression notes and debugging.

Near-symmetry between building and releasing indicates the track takes exactly as much as it gives — rare and structurally notable.

---

## Pitch grid (`mean_pitch_grid`)

**Range:** 0.0–1.0
**What it is:** How cleanly the harmony sits inside familiar equal-tempered pitch space. Higher values feel centered, resolved, and conventionally tuned; lower values can feel bent, smeared, folk-natural, microtonal, or intentionally outside the grid.

**How it is calculated:** concentration of chroma energy across equal-tempered pitch classes.

Do not read low pitch_grid as a defect by itself. Some traditions deliberately live between the standard pitch bins. Treat it as evidence about tuning world, not as a quality score.

---

## Interval coherence (`mean_interval_coherence`)

**Range:** 0.0–1.0
**What it is:** How concentrated the pitch content is around simple, stable harmonic relationships. Higher values feel fused, settled, and easy for the ear to organize; lower values feel more spread, complex, or harmonically ambiguous.

**How it is calculated:** active chroma pitch-class pairs are scored against simple just-intonation interval relationships, weighted by chroma energy. This is harmony-side evidence. It describes pitch-class organization, not the raw overtone spectrum.

---

## Harmonic pull (`mean_harmonic_pull`)

**Range:** 0.0–1.0
**What it is:** How much the harmony is pulling, shifting, or refusing to settle over time. High values feel like motion, pressure, searching, or harmonic unease; low values feel anchored, suspended, static, or resolved.

**How it is calculated:** velocity through smoothed tonnetz space, normalized across the track.

| Value | Meaning |
|-------|---------|
| <0.25 | Consonant, settled. Easy listening, tonal resolution. |
| 0.25–0.40 | Mild tension. Character without instability. |
| 0.40–0.55 | Significant tension. Unresolved, complex harmonically. |
| >0.55 | High dissonance. Deliberately unsettled. |

Catalog note: Teardrop (Massive Attack) has the highest cataloged tension at 0.421.

---

## Chroma motion (`mean_chroma_motion`)

**Range:** 0.0–1.0
**What it is:** How quickly the harmonic color changes from one moment to the next. High values mean the harmonic surface is restless or actively turning; low values mean the color is steady, droning, or slowly evolving.

**How it is calculated:** cosine distance between adjacent smoothed chroma frames, averaged in a local window and normalized.

---

## Tonal anchor (`mean_tonal_anchor`)

**Range:** 0.0–1.0
**What it is:** How strongly the current window stays anchored to its tonal center. High values feel grounded or centered; low values feel wandering, suspended, or harmonically diffuse.

**How it is calculated:** Krumhansl-Kessler key profile correlation identifies a local key/root, then tonal stability measures how dominant that tonic pitch class is in the local chroma profile.

---

## Major/Minor Balance (`mean_major_minor`)

**Range:** -1.0 to 1.0
**What it is:** Whether the harmony leans dark/minor, bright/major, or stays between them. Negative values lean minor; positive values lean major; near-zero can mean modal ambiguity, mixture, or neither color dominating.

**How it is calculated:** after local key/root detection, compares chroma energy at the major-third and minor-third pitch classes.

---

## Overtone fit (`mean_overtone_fit`)

**Range:** 0.0–1.0
**What it is:** How strongly the sound itself locks onto natural overtone relationships. High values feel pure, fused, bell-like, vocal, or resonant; low values feel noisier, rougher, more inharmonic, or more textural.

**How it is calculated:** detected overtone partials are compared with ideal harmonic-series positions around the detected fundamental. This is overtone-side evidence. It describes spectral structure around the detected fundamental, not the chord progression.

---

## Overtone density (`mean_overtone_density`)

**Range:** 0.0–1.0
**What it is:** How many upper harmonics are present in the sound. High richness feels dense, bright, saturated, or full of upper partials; low richness feels simpler, darker, hollower, or more sine-like.

**How it is calculated:** relative energy across detected upper partials.

---

## Inharmonicity (`mean_inharmonicity`)

**Unit:** cents
**What it is:** How far the overtones drift from ideal harmonic positions. Higher values feel rougher, noisier, more metallic, more bell-like in the unstable sense, or more textural. Lower values feel cleaner and more tonally fused.

**How it is calculated:** average cent deviation between detected partials and ideal harmonic-series positions.

---

## Foreground line (`mean_foreground_line`)

**Range:** 0.0–1.0
**What it is:** How much foreground pitched material is carrying the track. The field is still named `mean_foreground_line` for compatibility, but read it as pitch-extraction confidence, not proof of a literal singer. High values mean a voice or lead pitch is structurally present; low values mean the voice/lead is absent, textural, buried, unpitched, or not the main carrier.

**How it is calculated:** pYIN voiced probability over time, smoothed into the melody stream.

| Value | Meaning |
|-------|---------|
| <0.05 | Minimal / drone-like. Voice is texture, not foreground. |
| 0.05–0.15 | Voice present but mixed into the ensemble. |
| 0.15–0.30 | Clear vocal lead. |
| >0.30 | Voice dominates the mix. |

Low foreground pitch evidence + deeply negative surface balance = pure harmonic surface. High foreground pitch evidence + descending melody = voice/lead-forward with falling contour (often resignation/descent arc).

---

## Silences

**Structure:** Each silence has `start`, `end`, `duration`, `depth_db`, `recovery_attention`.

| Depth | Meaning |
|-------|---------|
| -30 to -45 dB | Soft silence. Still some signal present. |
| -45 to -60 dB | Clear silence. Listener attention sharpens. |
| -60 to -75 dB | Deep silence. Structural weight. |
| < -75 dB | Near-absolute. Very deliberate. |

`recovery_attention` after silence: if >0.93, listener re-locked. If <0.80, attention didn't recover — track may not re-engage.

Multiple silences with deepening depth and consistent re-lock = structured withdrawal (dissolution pattern). Compressing silence intervals toward end = listener being walked to the edge.

---

## Melody Contour

**Shape:** Percentage ascending / holding / descending.
**What it is:** The average shape of the foreground pitched line: whether it rises, falls, or holds its ground over time.

Heavily holding (>60%) with high foreground pitch evidence = melody uses repetition or narrow range as expressive strategy — not a limitation.
Heavily descending + resigned lyrics = structural confirmation of emotional content.
Ascending contour during climax = conventional arc. Descending during what sounds like climax = tension through contradiction.

---

## Metric Evidence Cheat Sheet

| Metric | Primary evidence |
|---|---|
| `attention` | Beat regularity × beat density in rolling windows |
| `pressure` / `pressure_state` | Short-term LUFS movement |
| `pattern` | `1.0 - disruption`; disruption = beat + spectral + energy expectation failures |
| `surface_balance` | Harmonic/percussive separated energy |
| `pitch_grid` | Chroma concentration in equal-tempered pitch classes |
| `interval_coherence` | Chroma interval relationships weighted by energy |
| `harmonic_pull` | Tonnetz velocity |
| `chroma_motion` | Cosine distance between adjacent chroma frames |
| `tonal_anchor` | Dominance of detected tonic pitch class |
| `major_minor` | Major-third vs minor-third chroma energy around detected root |
| `overtone_fit` | Overtone partial alignment around detected fundamentals |
| `overtone_density` | Upper-partial energy |
| `inharmonicity` | Cent deviation from ideal harmonic partials |
| `mean_foreground_line` | pYIN voiced probability; foreground pitch evidence |
| `silences` | dB-floor intervals plus recovery attention |

---

## Pattern Breaks

Each break has: `timestamp`, `intensity` (0–1), `beat` / `spectral` / `energy` component scores.

**Intensity interpretation:**
- < 0.3: Subtle shift. Texture change rather than structural break.
- 0.3–0.6: Clear break. Listener notices.
- > 0.6: Significant disruption. Track changes character.

**Component breakdown:**
- High `beat` + low others = rhythmic disruption only
- High `spectral` = timbral/textural shift
- High `energy` = dynamic change

**Distribution:**
- Clustered at end (final 10%) = planned release
- Distributed across track = varied, episodic structure
- Single large break = pivot point; track has two halves
