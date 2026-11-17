# Masks, AI features, and output

## Contents

- Blend and mask controls
- Drawn masks
- Parametric masks
- Combining and refining masks
- Raster masks
- AI object mask
- Neural restore
- Output checks and export

## Blend and mask controls

Applicable processing modules expose mask/blend icons at the bottom. The main modes are:

- off;
- uniform blend with global opacity;
- drawn mask;
- parametric mask;
- combined drawn and parametric mask;
- raster mask from an earlier active module.

The mask defines per-pixel module opacity. A value of zero passes the input unchanged; one applies the full module effect at that location. The blend color space depends on the module and can be Lab, display-referred RGB/HSL, or scene-referred RGB/JzCzhz.

Always show how to inspect the mask overlay. A technically correct mask can still reveal halos, abrupt color transitions, or missed texture after the module effect is applied.

## Drawn masks

Available shapes include brush, circle, ellipse, path, gradient, and—when enabled—AI object. Shapes are vectors anchored to the original image coordinate system and are transformed through crop, rotation, perspective, and lens-correction operations.

Common operations:

- click the shape icon to create one shape;
- Ctrl-click the icon for continuous creation;
- right-click to leave creation mode or remove a shape in edit mode;
- scroll to resize the relevant shape parameter;
- Shift+scroll to change feathering/hardness;
- Ctrl+scroll to change opacity;
- hold A while panning/zooming during mask creation so the gesture affects the image, not the mask;
- click `+/-` to invert the whole drawn mask.

Use `mask manager` in the darkroom left panel to name, group, reuse, and combine shapes. Reusing an existing shape can link later edits to the same geometry; copying the group creates independent membership. Explain this distinction when subsequent edits must stay independent.

Prefer paths over circles/ellipses where lens or perspective distortion makes simple shapes visibly inaccurate. Very complex brush masks are expensive to render.

## Parametric masks

Parametric masks select pixels by channel values rather than geometry. The available channels depend on the module's blend color space.

Each channel slider defines a trapezoidal opacity function with four markers:

- outer markers: zero-opacity limits;
- inner markers: full-opacity region;
- intermediate slopes: feathered transition.

Use the polarity button to switch range selection/deselection. Press C while hovering a channel slider to inspect the channel on canvas. Press M to inspect the resulting mask. Press A over the slider to toggle linear/log display when finer shadow control is needed.

Scene-referred masks may expose Jz, Cz, and hz in addition to RGB. JzCzhz is more suitable than Lab for high-dynamic-range scene data; choose channels according to the module's actual stage.

## Combining and refining masks

Combine drawn and parametric masks when both location and pixel properties matter. Explain whether the user needs intersection-like restriction or union-like inclusion before suggesting polarity changes.

Refinement controls can include:

- details threshold;
- feathering radius;
- blur radius;
- mask opacity;
- mask contrast.

Use feathering to follow image edges, blur to smooth the mask itself, opacity to limit total effect, and contrast to make the selection more or less decisive. Judge the final transition with the module effect on; the yellow overlay alone can hide color/halo problems.

Raster masks flow upward through the pixelpipe. They require the generating module to remain active and can only be consumed by modules later than the generator.

## Raster masks

`external raster mask` exposes a file as a mask early in the pipeline. Darktable 5.6 supports PFM and PNG according to its technical information and release notes, although one sentence in the manual still describes only PFM.

The external file is scaled to the current image. Its orientation should match the original RAW sensor orientation because downstream orientation/crop modules transform it later. In 5.6, the bitmap can be vectorized into a path in `mask manager`; verify that the installed build exposes the control.

## AI object mask

Prerequisites:

1. Open Preferences > AI.
2. Enable AI features.
3. Download/import a mask model and mark one model active for the `mask` task.
4. Return to a module mask control or `mask manager` and choose the AI-object shape.

Canvas controls in 5.6:

- click: add a foreground/positive point;
- Shift-click: add a background/negative point;
- Ctrl+Shift-click: clear points and restart;
- right-click: apply the mask.

Iterate with positive and negative points until the object is covered. One visually distinct object is selected at a time; a click on a separate object usually starts another selection. After applying, Darktable vectorizes the result into ordinary Bézier paths in `mask manager`. The resulting mask no longer depends on AI, can be edited and combined, and can be used in styles.

The image encoder result is cached. Later prompt clicks are faster. Geometry-changing operations such as crop, rotation/perspective, or lens correction can invalidate the cache and force a new encode.

Treat AI masks as a first draft. Inspect hair, foliage, translucent edges, and intersecting objects at 100%. Compare a manually refined path or external raster mask when vectorization loses edge detail.

## Neural restore

`neural restore` is a shared utility module available in lighttable and darkroom when AI is enabled. It processes selected images and creates new files; it never changes the original.

Tasks:

- `raw denoise`: use before darkroom editing for difficult sensor noise. Bayer data can be denoised directly on the CFA; X-Trans/non-Bayer data is first converted to linear Rec.2020. Output is a DNG and is re-imported/grouped when requested.
- `denoise`: use late, after the full darkroom pipeline, when noise remains in the finished look. Output is a TIFF with the edit baked in.
- `upscale`: use as the last delivery step for 2x or 4x enlargement. Output is a TIFF. 4x creates sixteen times as many pixels and is much more demanding.

Use the split before/after preview on a representative patch. Move the patch with the picker. Hover for a magnified view. If no model is active for the current task, the process button remains unavailable.

Choose raw denoise when noise should be removed at the source and the edit has not begun. Choose RGB denoise when the final pixelpipe result contains objectionable noise and the user accepts continuing from a baked TIFF. Use upscale after sharpening and grading, not early in the workflow.

AI inference runs locally. The manual states that no image is sent to a cloud service, no background autonomous editing occurs, and no usage analytics are reported. Official macOS builds use bundled CoreML; Windows has bundled DirectML; Linux bundles CPU inference, with optional vendor GPU runtimes. Third-party packages may omit AI support.

## Output checks and export

Before export:

1. Use fit view for global balance and 100% for artifacts.
2. Toggle color assessment when judging tone/color against a neutral surround.
3. Use clipping warning for output clipping and raw-overexposure warning for sensor clipping; do not conflate them.
4. Inspect histogram, waveform, RGB parade, or vectorscope according to the issue.
5. Use soft proof with the intended profile and rendering intent for print or constrained-gamut delivery.
6. Use gamut check to locate colors outside the selected output gamut.

In the shared `export` utility, verify:

- selected images;
- destination and filename variables;
- file format and compression;
- bit depth;
- pixel dimensions and scaling;
- output color profile and rendering intent;
- metadata inclusion/exclusion;
- style application only when deliberately required.

For print, web, and archive outputs, create separate export presets rather than changing one preset back and forth. Confirm the exported file in a color-managed viewer.
