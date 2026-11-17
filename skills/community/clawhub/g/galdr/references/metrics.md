# galdr Metric Reference

Metric fields come from the module JSON files in `analysis/<slug>/`, including `<slug>_report.json`, `<slug>_perception.json`, `<slug>_stream.json`, and the harmony/melody/overtone summaries and streams. Scores are signal-derived proxies and interpretation cues, not measurements of a listener’s feelings or musical quality.

---

## Pattern (`pattern`)

**Range:** 0.0–1.0
**What it is:** How little beat, spectral, and energy disruption the algorithm detects. High pattern means those measured features are relatively steady; it does not prove a listener trusts the structure.

**How it is calculated:** `pattern = 1.0 - disruption`. Disruption is a weighted blend of beat disruption (`40%`), spectral disruption (`35%`), and energy disruption (`25%`). Beat disruption catches missing or off-time expected beats; spectral disruption catches sudden timbral change above local context; energy disruption catches loudness jumps/drops above local trend.

| Value | Meaning |
|-------|---------|
| 0.96–1.0 | Very little detected beat, spectral, or energy disruption. |
| 0.90–0.96 | Strong detected pattern hold with some variation. |
| 0.80–0.90 | Moderate combined detected disruption; inspect its components and timing. |
| <0.80 | More combined detected disruption; no genre or listener-state classification. |

The `type: pattern_break` entries mark detected disruption candidates. Check `pattern_breaks` in `<slug>_perception.json` for `time`, `type`, and (for `type: pattern_break`) `intensity`. The beat/spectral/energy values are embedded in that event’s `description`, not separate JSON component fields. The list also contains attention shifts and silence events; filter by `type` before interpreting intensity.

---

## Attention (`attention`, `mean_attention`)

**Range:** 0.0–1.0
**What it is:** A beat-derived proxy for rhythmic continuity, not observed listener attention, liking, or quality. High values indicate regular and sufficiently dense beat evidence in the local window; sparse or irregular evidence lowers the score.

**How it is calculated:** rolling beat regularity multiplied by beat density over a 4-second window. Regular intervals with enough beat evidence produce high attention; sparse or irregular beat evidence lowers it.

| Value | Meaning |
|-------|---------|
| >0.90 | Very high local beat regularity/density score. |
| 0.80–0.90 | High local beat-derived score. |
| 0.60–0.80 | Moderate local beat-derived score. |
| <0.60 | Low local beat evidence; not a measured disengagement. |

After a silence, a high attention score indicates beat evidence returned. It does not prove a listener re-engaged; repeated gaps/returns can support a withdrawal reading after audio confirmation.

---

## Pulse (`pulse`)

**Range:** 0.0–1.0
**What it is:** Report-level regularity of detected beat intervals. It does not identify time signature or verify how a listener feels a pulse.

| Value | Meaning |
|-------|---------|
| >0.96 | Very regular detected beat intervals. |
| 0.90–0.96 | Very regular/metronomic by the report label above 0.90. |
| 0.80–0.90 | Steady by the report label; style and feel require listening. |
| <0.80 | Less regular beat evidence; the report changes label again at 0.70 and 0.50. |

A regular beat can coexist with an unusual meter, but this score alone does not establish meter.

---

## Surface balance (`surface_balance`, `mean_surface_balance`)

**Range:** -1.0 to 1.0
**What it is:** The signed balance of HPSS-separated harmonic-side and percussive-side energy. Negative values indicate more sustained/harmonic-side energy; positive values indicate more percussive-side energy. The score does not identify a voice or instrument.

**How it is calculated:** harmonic/percussive source separation energy, smoothed into the perception stream. Very low total energy is treated as neutral so silence does not pretend to have a surface-balance claim.

The stream and ARC use the signed convention. Full-track report and old catalog `surface_balance` remain the historical unsigned percussive fraction; new reports/catalog entries expose `percussive_fraction` and `surface_balance_signed` explicitly. Do not interpret the legacy report fraction as signed. Body and Weight still consume the unsigned fraction.

`surface_evidence` carries the local evidence behind the reading: roughness, noise density, transient attack, sustain/drone, band pressure, surface motion, punch, band weights, and brightness tilt.

| Value | Meaning |
|-------|---------|
| < -0.5 | Strongly harmonic-side energy; source identity unknown. |
| -0.5 to -0.2 | Harmonic-side energy dominant. |
| -0.2 to 0.2 | Similar harmonic-side and percussive-side energy. |
| 0.2 to 0.5 | Percussive-side energy dominant. |
| > 0.5 | Strongly percussive-side energy; source identity unknown. |

Deepening negative signed surface balance across a track indicates increasing harmonic-side weight relative to percussive-side weight. A heard choir, drone, or closing dissolution is a possible listening reading, not an HPSS classification.

---

## Pressure / Heard Pressure (`pressure`, `pressure_state`, pressure summary percentages)

**Shape:** Stream fields plus three summary percentages — building / releasing / sustaining. New summaries count active, classified frames; a fully silent/unknown stream reports three zeros, and one-decimal rounding can prevent an exact 100% sum.
**What it is:** The heard-pressure shape of the track. Pressure is derived from short-term EBU R128/LUFS loudness rather than raw RMS energy so it tracks whether pressure comes forward, holds, or withdraws.

**How it is calculated:** short-term LUFS is smoothed over 8 seconds, differenced, and normalized into a pressure-motion curve. Positive values build, negative values release, near-zero values sustain.

Stream fields:
- `pressure` — normalized pressure movement; positive builds, negative releases, near-zero sustains
- `pressure_state` — `building`, `releasing`, `sustaining`, or `silence`
- `loudness_lufs` — short-term loudness evidence; use for debugging/comparison, not prose
- `pressure_lufs_delta` — short-term pressure delta evidence
- `loudness_silence` — loudness-floor silence marker

| Pattern | Meaning |
|---------|---------|
| ~33/33/33 | Similar shares of the three active stream labels; not proof of perceived equilibrium. |
| Heavy building (>45%) | More than 45% of active classified frames carry the building label. |
| Heavy releasing (>45%) | More than 45% of active classified frames carry the releasing label. |
| Near-zero sustain (<10%) | Few active frames carry the sustaining label; inspect the trace for shape. |
| Heavy sustain (>40%) | More than 40% of active frames carry the sustaining label; not proof of listener coupling. |

Translation rule: do not write raw LUFS values in experience prose. Write what they mean: pressure comes forward, fills the room, holds, loosens, drops away, empties, or stops carrying attention. LUFS belongs in regression notes and debugging.

Similar building and releasing shares describe label counts, not equal perceptual force. Inspect the timed pressure trace and audio before making a structural claim.

---

## Pitch grid (`mean_pitch_grid`)

**Range:** 0.0–1.0
**What it is:** How concentrated chroma energy is among the 12 pitch classes. Higher values mean fewer classes dominate; lower values mean energy is spread across more classes. This is not an intonation, tuning-accuracy, or temperament score.

**How it is calculated:** `1 - entropy(normalized_chroma) / log2(12)` after temporal smoothing; low-energy frames return zero. Chroma has already folded spectral energy into 12 pitch classes.

Do not infer bends, microtonality, folk-natural tuning, or out-of-tune performance from this value. A well-tuned chromatic or dense passage can score low because many pitch classes are active.

---

## Interval coherence (`mean_interval_coherence`)

**Range:** 0.0–1.0
**What it is:** How concentrated the pitch content is around simple, stable harmonic relationships. Higher values feel fused, settled, and easy for the ear to organize; lower values feel more spread, complex, or harmonically ambiguous.

**How it is calculated:** active chroma pitch-class pairs are scored against simple just-intonation interval relationships, weighted by chroma energy. This is harmony-side evidence. It describes pitch-class organization, not the raw overtone spectrum.

---

## Harmonic pull (`mean_harmonic_pull`)

**Range:** 0.0–1.0
**What it is:** Relative motion in the track’s smoothed tonnetz trace. A higher value marks more motion relative to this track’s own peak; it does not measure absolute dissonance, tension, or emotional unease.

**How it is calculated:** velocity through smoothed tonnetz space, smoothed again and divided by this track’s maximum when nonzero. A nonstatic track therefore reaches 1.0 even if its absolute motion is small.

Use high/low values to locate relatively active/quiet harmonic-motion passages **within the same analysis**. The catalog may display or rank saved means, but unlike tagged absolute `chroma_motion`, this track-max-normalized scale cannot establish an absolute cross-track motion or dissonance ordering. Re-analyzing old artifacts can update separately versioned metrics such as `chroma_motion`; it does not make `harmonic_pull` absolute.

---

## Chroma motion (`mean_chroma_motion`)

**Range:** 0.0–1.0 for nonnegative chroma vectors (usually much smaller after window averaging); this is an absolute distance, not a track-normalized score
**What it is:** How much the harmonic color changes from one moment to the next. High values mean the harmonic surface is restless or actively turning; low values mean the color is steady, droning, or slowly evolving.

**How it is calculated:** absolute cosine distance between adjacent smoothed chroma frames, averaged in a local window without track-max normalization. Empty/silent vectors produce zero motion. New outputs carry `chroma_motion_semantics: absolute_cosine_distance_v1`; old untagged normalized values are not comparable.

---

## Tonal anchor (`mean_tonal_anchor`)

**Range:** 0.0–1.0
**What it is:** The detected KK-profile root pitch class’s share of the local chroma total. Higher values mean more energy in that class within this window; they do not establish a persistent key center or a felt sense of home.

**How it is calculated:** Krumhansl-Kessler key-profile correlation selects a root for the local window; the score is that root pitch class’s share of the window’s chroma sum. It does not compare root identity across windows.

---

## Major/Minor Balance (`mean_major_minor`)

**Range:** -1.0 to 1.0
**What it is:** Whether the harmony leans dark/minor, bright/major, or stays between them. Negative values lean minor; positive values lean major; near-zero can mean modal ambiguity, mixture, or neither color dominating.

**How it is calculated:** after local key/root detection, compares chroma energy at the major-third and minor-third pitch classes.

---

## Overtone fit (`mean_overtone_fit`)

**Range:** 0.0–1.0
**What it is:** A detected-harmonic coverage × positional-closeness score around an estimated fundamental. Higher values mean more expected harmonic slots were matched within tolerance and those matches were closer. It is not a purity or absolute harmonic-correctness rating.

**How it is calculated:** matched harmonic count (including the fundamental) divided by the number of eligible slots, multiplied by `1 - mean matched deviation / tolerance`. Peak magnitudes do not weight the fit. A pure fundamental alone can score low because coverage is sparse; a richer, slightly detuned set can score higher.

---

## Overtone density (`mean_overtone_density`)

**Range:** 0.0–1.0
**What it is:** The fraction of eligible harmonic slots matched near the estimated fundamental (including the fundamental). It is a detected-count ratio, not an energy, brightness, or perceived-richness measurement.

**How it is calculated:** matched harmonic count divided by eligible slots below the frequency ceiling; matched peak magnitudes do not weight the ratio.

---

## Inharmonicity (`mean_inharmonicity`)

**Unit:** cents
**What it is:** The mean absolute cent offset of peaks matched to expected harmonic slots around an estimated fundamental. It is not a measure of perceived roughness, noise, metallic timbre, or every detected partial.

**How it is calculated:** average absolute cent deviation for matched harmonic slots only; unmatched peaks do not enter this mean. Interpret timbre by listening and checking other evidence.

---

## Foreground line (`mean_foreground_line`)

**Range:** 0.0–1.0
**What it is:** A summary of pYIN voiced probabilities. The field is still named `mean_foreground_line` for compatibility, but it does not classify a singer, prove a lead source, or measure mix dominance. Low probability can reflect weak or difficult pitch extraction, not absence of a voice.

**How it is calculated:** pYIN voiced probability over time, smoothed into the melody stream.

| Value | Meaning |
|-------|---------|
| <0.05 | Very low pYIN voiced-probability summary. |
| 0.05–0.15 | Low pYIN voiced-probability summary. |
| 0.15–0.30 | Moderate pYIN voiced-probability summary. |
| >0.30 | Higher pYIN voiced-probability summary; source identity remains unknown. |

Strongly negative signed stream surface balance indicates more sustained/harmonic-side energy even when pitch extraction is weak. Neither score proves purity, source identity, or absence of voice. Higher pYIN probability plus descending contour supports an extracted pitch path moving down; confirm source and expressive effect against audio.

---

## Silences

**Structure:** Each object in `<slug>_perception.json` → `silences` has `start`, `end`, `duration`, `depth_db`. `depth_db` is relative to the file’s maximum RMS, not an absolute sound-pressure level. Separate `silence_reentries` objects carry `post_attention`, `recovered`, `reentry_shape`, and recovery timing.

| Depth | Meaning |
|-------|---------|
| -30 to -45 dB | Shallower detected dip relative to file maximum. |
| -45 to -60 dB | Deeper detected dip relative to file maximum. |
| -60 to -75 dB | Very deep detected dip relative to file maximum. |
| < -75 dB | Near the relative analysis floor; not proof of absolute silence or intent. |

Read `silence_reentries[].post_attention` and `recovered` as algorithmic return evidence. A high score is not proof a human listener re-engaged; confirm the audible return.

Multiple detected gaps with progressively deeper relative depth and returning beat evidence can support a withdrawal reading after listening. Neither their pattern nor timing proves compositional intent or a listener response.

---

## Melody Contour

**Shape:** Percentage ascending / holding / descending.
**What it is:** The average shape of the extracted pitch contour: whether it rises, falls, or holds over time. The contour does not identify a singer or lead source.

Heavily holding (>60%) with higher pitch-extraction probability can suggest a repeated or narrow-range extracted contour; whether repetition is an expressive strategy requires listening.
A descending extracted contour alongside a subdued vocal delivery may support an emotional reading, but does not confirm it.
An ascending contour near a heard climax can support a familiar arc; a descending contour there might create tension through contradiction. Confirm the musical moment, source, and emotion by ear.

---

## Metric Evidence Cheat Sheet

| Metric | Primary evidence |
|---|---|
| `attention` | Beat regularity × beat density in rolling windows |
| `pressure` / `pressure_state` | Short-term LUFS movement |
| `pattern` | `1.0 - disruption`; disruption = beat + spectral + energy expectation failures |
| `surface_balance` | Harmonic/percussive separated energy |
| `pitch_grid` | Entropy-based concentration across 12 chroma pitch classes; not tuning accuracy |
| `interval_coherence` | Chroma interval relationships weighted by energy |
| `harmonic_pull` | Track-max-normalized tonnetz velocity; relative motion only |
| `chroma_motion` | Cosine distance between adjacent chroma frames |
| `tonal_anchor` | Detected local KK-profile root class’s share of chroma, not key persistence |
| `major_minor` | Major-third vs minor-third chroma energy around detected root |
| `overtone_fit` | Matched-slot coverage × positional closeness around an estimated fundamental |
| `overtone_density` | Fraction of eligible harmonic slots matched, including the fundamental |
| `inharmonicity` | Mean absolute cents for matched harmonic slots only |
| `mean_foreground_line` | pYIN voiced probability; no vocal-source or mix classification |
| `silences` / `silence_reentries` | Relative dB-floor intervals and separate return evidence |

---

## Pattern Breaks

Each `pattern_breaks` event has `time` and `type`. Only `type: pattern_break` has `intensity` (0–1) and a `description` string containing beat/spectral/energy values. `attention_drop`/`attention_gain` have `from` and `to`; `silence` has duration/depth and, when available, re-entry fields. Do not query `timestamp` or component scores as top-level event keys.

**Intensity interpretation:**
- < 0.3: Smaller detected disruption; inspect the trace.
- 0.3–0.6: Intermediate detected disruption; audible significance is uncalibrated.
- > 0.6: Larger detected disruption; confirm whether it is a structural change.

**Component evidence:** The break description embeds beat, spectral, and energy scores for human reading; they are not structured fields for `jq` selection.

**Distribution:**
- Clustered near the end may support a release reading after audio confirmation
- Distributed across the track suggests multiple detected disruption candidates
- A single large candidate may mark a pivot; confirm in the recording

Pressure summary percentages count active, classified `pressure_state` labels; silence states/flags and unknown are excluded, and a fully silent stream gives three zeros. The `pressure_summary_semantics: stream_labels_active_v1` tag distinguishes them from old untagged threshold percentages. ARC pressure spans use a separate coarser classifier and may differ.
