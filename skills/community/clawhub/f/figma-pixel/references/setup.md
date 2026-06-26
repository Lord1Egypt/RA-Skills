# Setup

Provide the runtime prerequisites outside the skill package.

## Required runtime

The environment running this skill should already provide:
- `playwright`
- `pixelmatch`
- `pngjs`
- `@techstark/opencv-js`
- a Chromium-compatible browser executable, or `CHROMIUM_PATH`

## Credentials

This skill expects:
- `FIGMA_TOKEN`

The token is used only for official Figma API requests.
Do not persist the token in logs or artifacts.

## Module resolution overrides

If the runtime does not resolve modules normally, use environment overrides:
- `PLAYWRIGHT_MODULE_PATH`
- `PNGJS_MODULE_PATH`
- `PIXELMATCH_MODULE_PATH`
- `CHROMIUM_PATH`

## Failure handling

If dependencies are missing:
- do not attempt installation from inside the skill
- stop and report the missing package or browser clearly
- prefer explicit prerequisite errors over fallback setup logic
