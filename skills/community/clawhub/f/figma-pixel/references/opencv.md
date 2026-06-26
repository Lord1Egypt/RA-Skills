# OpenCV post-processing

This skill can optionally run an OpenCV.js-based diff analysis after `pixelmatch`.

## Purpose

The post-processing step is used as an enrichment layer, not as a replacement for the main comparison flow.
It converts raw diff pixels into larger, more meaningful mismatch regions.

## Current outputs

When available, this step produces:
- `pixelmatch/opencv-report.json`
- grouped diff regions with bounding boxes
- rough zone labels such as `top-left`, `middle-center`, `bottom-right`
- short human-readable mismatch summaries

## Runtime expectation

Preferred runtime:
- `node`
- `@techstark/opencv-js`
- `pngjs`

If this step is unavailable, the main pipeline should continue and fall back to standard `pixelmatch` output.
This step is optional enrichment, not a hard blocker.

## Integration point

Run the OpenCV analysis after:
1. reference image export
2. page render capture

Then run pixelmatch and merge the resulting findings into `final/report.json` and `final/summary.md`.
This post-processing now complements the main `Playwright render -> OpenCV.js region detection -> pixelmatch` flow.
