# PowerMatrix GEO 30s Video

This folder contains a HyperFrames-style 9:16 composition for:

《GEO 不是以量取胜》

## Files

- DESIGN.md - visual system used by the composition
- index.html - HyperFrames source composition, 1080 x 1920, 30 seconds
- script.md - timed script, subtitles, and voiceover text

## Local Review

Open index.html?preview=1 in a browser to use the built-in lightweight preview mode. The source still keeps HyperFrames data-composition, data-start, data-duration, data-track-index, and window.__timelines structure for later CLI rendering.

## Render Note

The HyperFrames CLI could not be fetched in this environment because npm DNS resolution failed. Once the CLI is available, run from this folder:

~~~bash
npx hyperframes lint
npx hyperframes inspect --samples 15 --at 1.5,5.5,11.5,19,26.5
npx hyperframes preview --port 3017
npx hyperframes render --output powermatrix-geo-not-volume.mp4 --quality standard
~~~
