# Calibration Examples and Failure Modes

Read this reference only when a scene resembles an example or a result is drifting toward over-detail, generic symbolism, or pseudo-flat rendering. These examples calibrate the general rules; they are not fixed templates or exhaustive scene categories.

## People calibration

Preserve identity anchors such as head or hair silhouette, identity-anchor accessories, clothing silhouette, pose and orientation, and scale or positional relationships. Remove detailed facial anatomy from subordinate figures and merge distant people when possible.

### Seated people beside a main-yellow palette wall — target 5 to 6

- **Systems**: a seated-person sequence, a main-yellow palette wall field, and an oversized foreground profile at the right edge.
- **Identity anchors**: large right-edge head and shoulder, central seated figure with a darkest-palette cap, people receding leftward, main-yellow palette wall beside main-blue or secondary-blue palette space, and strong foreground-to-background scale shift.
- **Delete or demote**: detailed faces, phones, cups, shoes, small furniture, exact wall text, ceiling fixtures, distant architecture, and clothing folds.
- **Output**: merge distant people into simple head-and-torso masses. Handle wall writing according to Source Cleanup.

### Bearded man in a kitchen — target 4 to 5

- **Systems**: the central man, a brightest-palette counter plane, and a large extractor-hood structure.
- **Identity anchors**: main-yellow or secondary-orange palette glasses, warm secondary-orange or accent-purple palette beard, secondary-blue or darkest-palette jacket silhouette, both hands on the counter, and centered frontal pose beneath the hood.
- **Delete**: social-media UI, numbers, subtitles, watermarks, small kitchen objects, fabric texture, folds, detailed facial anatomy, and metal reflections.
- **Output**: use solid skin, beard, glasses, jacket, counter, and background blocks with no metallic gradient, lens shine, glow, or soft shadow.

## Architecture calibration

All examples use the fixed HSB palette through role assignment, not color matching to the reference photograph.

Treat clustered buildings as one skyline system when they share a structural role. Preserve landmark silhouettes, height hierarchy, dominant skyline rhythm, distinctive adjacent structures, and the overall sky-to-city proportion. Apply the bright-source-shape rules in `generation-spec.md` to lit windows and signs.

### Night city skyline with a landmark tower — target 5 to 6

- **Systems**: one tall needle-like landmark, one grouped stepped skyline, and one broad main-blue or secondary-blue palette night-sky field.
- **Identity anchors**: extremely tall narrow central tower, small brightest-palette cap, dense darkest or secondary-blue palette lower skyline, distinctive neighboring towers to the right, and broad uninterrupted sky.
- **Delete or demote**: most windows, facade grids, signs, readable logos, cloud texture, aerial haze, reflections, and luminous bloom.
- **Output**: use a uniform main-blue or secondary-blue palette sky, a few hard-edged solid tower planes, grouped brightest-palette window marks, and discrete darkest or secondary-blue building tones. Keep brightness contained within each window-shape boundary, with no glow, spill, diffusion, or illumination extending onto surrounding surfaces. Depth comes from overlap and tone steps.

## Food and organic-form calibration

Merge scattered pieces into one or two organic masses. Preserve the overall outer contour, distinctive crossing or connecting forms, an identity-establishing container, and a limited set of flat organic color patches. Remove oil sheen, translucency, char texture, folds, and micro-contours.

### Plate of cooked meat — target 3 to 4

- **Systems**: one irregular secondary-orange or accent-purple food mass, one brightest-palette plate, and two crossing stick-like or bone-like forms.
- **Identity anchors**: broad mound centered on the plate, two long diagonal forms crossing the mound, small secondary-orange accents, and brightest-palette plate against a main-yellow palette field.
- **Delete**: individual slices, oil sheen, translucency, char texture, fragments, realistic shadows, and highlights.
- **Output**: use several secondary-orange or accent-purple organic patches inside one grouped silhouette, with hard boundaries and no glossy effects.

## Common failure comparison

- **Style-only simplification**: every source object remains, merely with fewer lines. Semantic complexity has not decreased.
- **Generic iconification**: a specific scene becomes a generic category symbol. Identity anchors and spatial relationships were removed.
- **Over-compression**: supporting elements that establish scale, spatial relationships, or composition-specific identity are removed, making the result simpler but less recognizable.
- **Pseudo-flat rendering**: gradients, bloom, soft shadows, ambient occlusion, or haze remain. The result is not truly flat-vector.
- **Correct result**: the dominant arrangement and identity anchors survive; repeated content is grouped; there is one clear focal hierarchy; fills and boundaries remain crisp; the image reads at small size.

## Anti-generic calibration

Too generic:

- a man in a kitchen;
- people sitting indoors;
- a city at night.

Reference-specific:

- a bearded man with main-yellow or secondary-orange palette glasses leaning symmetrically on a brightest-palette counter below a large extractor hood;
- a seated row beside a main-yellow palette wall with an oversized foreground profile on the right;
- a needle-like landmark tower centered above a dense darkest or secondary-blue palette skyline under a broad main-blue palette sky.
