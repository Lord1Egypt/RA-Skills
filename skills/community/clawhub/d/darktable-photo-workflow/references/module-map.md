# Current module map for editing advice

## Contents

- Tone and exposure
- Color
- Optical and sensor correction
- Detail, noise, and local contrast
- Geometry and cleanup
- Effects and output
- Deprecated-module rule

Use the English module name in backticks so the user can search for it in the darkroom right panel. Group placement can vary with the selected module-layout preset.

## Tone and exposure

| Need | Preferred module | Use | Main caution |
|---|---|---|---|
| Overall scene brightness | `exposure` | Set global mid-gray/brightness; create masked instances for local dodge/burn | Lens correction and white balance can change the result; black-level correction is not a density control |
| Current default display transform | `sigmoid` | Compact scene-to-display mapping; contrast/skew and primaries | Avoid activating another tone mapper on top without intent |
| Advanced display transform and color handling | `AgX` | Set input range, curve/look, and primaries before/after tone mapping | Many controls interact; start from a preset and change one section at a time |
| Existing filmic workflow | `filmic rgb` | Map black/white relative exposure, contrast, shoulder/toe, and reconstruct highlights | The introductory tutorial is filmic-specific; it is not the current default |
| Broad tonal zones | `tone equalizer` | Lift/darken ranges such as sky, face, or shadows | Check mask smoothing and avoid flat, haloed transitions |
| Simple local-contrast boost | `local contrast` | Quick global local contrast | Can amplify noise and halos |
| Display-referred curve work | `tone curve`, `rgb curve`, `rgb levels` | Use when deliberately working at their pipeline stage or maintaining an old edit | Do not substitute them blindly for a scene-referred tone mapper |

## Color

| Need | Preferred module | Use | Main caution |
|---|---|---|---|
| Illuminant and chromatic adaptation | `color calibration` | CAT tab, CCT picker, channel mixing, monochrome tab | Keep `white balance` in Camera Reference mode in the standard scene workflow |
| Raw white-balance reference | `white balance` | Maintain camera reference for `color calibration`; use directly in legacy/special cases | Manual adjustment can conflict with color calibration and trigger warnings |
| Global and tonal-range grading | `color balance rgb` | Global colorfulness/vibrance; shadows, mid-tones, highlights; masks | Large chroma changes can push colors out of gamut or create noisy shadows |
| Hue-dependent correction | `color equalizer` | Change hue, saturation, or brightness according to current hue | Guided-filter tradeoff: precise targeting versus noise, bleeding, or harsh transitions |
| Palette/harmony shift | `color harmonizer` | Pull hues toward harmony nodes; sync with RYB vectorscope | This changes hue relationships; protect neutrals and use a clear visual reason |
| Primary/gamut shaping | `rgb primaries` | Move primaries and control gamut creatively or correctively | Easy to alter many colors at once; avoid as a casual saturation tool |
| Lookup-table look | `LUT 3D` | Apply a known LUT in a controlled color-space workflow | Verify expected input/output space and intensity |
| Monochrome conversion | `color calibration` gray tab | Mix channels and use film-emulation presets | Check skin/sky separation and noise after channel weighting |
| Legacy selective color | `color zones` | Maintain old edits or intentionally work at its stage | For new scene-referred edits, prefer `color equalizer` where suitable |

## Optical and sensor correction

| Need | Preferred module | Use | Main caution |
|---|---|---|---|
| Lens distortion, vignetting, lens TCA | `lens correction` | Auto-detect lens/profile; enable early | Vignetting correction changes exposure; profile detection can be wrong or incomplete |
| Raw-stage chromatic aberration | `raw chromatic aberrations` | Correct Bayer/X-Trans color fringes before demosaic when applicable | RAW-only and sensor-dependent |
| Remaining RGB chromatic aberration | `chromatic aberrations` | Tune guide, radius, strength, correction mode; use masks/instances for hard cases | Excess strength can wash out colorful edges |
| Clipped raw highlights | `highlight reconstruction` | Try reconstruction methods before downstream contrast exaggerates artifacts | Reconstruction cannot recover data that the sensor never recorded; inspect color/edge artifacts |
| Hot/stuck pixels | `hot pixels` | Detect and correct isolated sensor pixels | Check stars and fine lights so they are not mistaken for defects |
| Demosaic behavior | `demosaic` | Change algorithm only for a specific detail/noise/maze problem | Algorithm tradeoffs affect fine detail, false color, and speed |
| Raw black/white point | `raw black/white point` | Correct faulty sensor black/white metadata when diagnosed | Incorrect changes can clip or bias the entire raw pipeline |

## Detail, noise, and local contrast

| Need | Preferred module | Use | Main caution |
|---|---|---|---|
| Profiled sensor noise | `denoise (profiled)` | Start with camera/ISO profile and default chroma/luma behavior | Over-denoising removes texture; check at 100% and fit view |
| Raw-stage classical denoise | `raw denoise` | Treat raw CFA noise before demosaic in specific cases | Limited controls/use cases compared with profiled or neural approaches |
| Flexible sharpening/deblur/local contrast | `diffuse or sharpen` | Start from a named preset, then tune iterations/radii | Computationally expensive; can create halos, texture exaggeration, or noise |
| Contrast by feature size | `contrast equalizer` | Target fine, medium, or coarse detail | Strong curves can halo or amplify noise |
| Anti-alias capture sharpening | `sharpen` | Maintain compatible edits or a specific AA-filter correction | The manual generally prefers newer methods such as `diffuse or sharpen` |
| Surface-preserving blur | `surface blur` | Reduce texture/noise while preserving selected edges | Edge thresholds can produce plastic texture or boundary artifacts |
| Simple haze correction | `haze removal` | Adjust atmospheric haze with few controls | Strong settings shift color and deepen shadows |

`neural restore` is a shared utility module rather than an ordinary pixelpipe processing module. It creates a new DNG or TIFF; see the AI reference.

## Geometry and cleanup

| Need | Preferred module | Use | Main caution |
|---|---|---|---|
| Crop/aspect | `crop` | Set frame and aspect; 5.6 shows aspect ratio in the crop preview | Do not confuse crop composition with final export resizing |
| Horizon/keystone | `rotate and perspective` | Correct rotation and converging lines; use guides | Over-correction stretches edges and changes composition |
| Pixel rotation helper | `rotate pixels` | Specialized pixel rotation at its pipeline stage | Not a general substitute for `rotate and perspective` |
| Object/dust/blemish removal | `retouch` | Heal/clone/fill with wavelet scale control | Repeating texture, mismatched source lighting, and edge seams |
| Liquify geometry | `liquify` | Local geometric deformation | Easy to distort context or introduce implausible shapes |
| Add canvas before framing/composite | `enlarge canvas` | Expand working canvas | Check how downstream modules and export dimensions respond |

## Effects and output

| Need | Preferred module | Use | Main caution |
|---|---|---|---|
| Film grain | `grain` | Add controlled texture after core correction | Judge at final output size; grain can hide or amplify noise perception |
| Vignette | `vignetting` | Direct attention or reproduce lens falloff | Avoid obvious rings and crushed corners |
| Border/frame | `framing` | Add colored frame and set aspect/output geometry | Confirm final pixel dimensions and print crop |
| Bloom/softening | `bloom`, `soften` | Controlled highlight glow or diffusion | Can reduce local contrast and make clipping look worse |
| Composite/overlay | `composite` | Place an overlay within the pipeline | Verify alpha, alignment, color space, and OpenCL/CPU result |
| External mask | `external raster mask` | Read PFM/PNG masks early in the pipeline and expose them as raster masks | File orientation must correspond to original sensor orientation; see version note |
| Working/output transform | `output color profile` | Convert to display/export profile at the correct stage | The export profile choice must match delivery requirements |
| Banding control | `dither or posterize` | Add dither before low-bit-depth output | Inspect at intended size; too much dither becomes visible noise |
| Final export | shared `export` utility | Format, bit depth, size, profile, intent, metadata | A good darkroom view does not guarantee correct output settings |

## Deprecated-module rule

Do not recommend a deprecated module for a new edit unless it solves a documented compatibility need or the user is maintaining an existing history. Examples include deprecated basic adjustments, channel mixer, contrast/brightness/saturation, crop and rotate, defringe, fill light, global tonemap, invert, levels, spot removal, tone mapping, vibrance, and zone system.
