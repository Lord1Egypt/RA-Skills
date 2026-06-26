# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2026-03-12

### Fixed

- `upload_product_image`: fixed TypeScript type error where `Buffer` was not assignable to `BodyInit`; multipart body is now correctly returned as `Uint8Array`

## [1.0.3] - 2026-03-12

### Changed

- `run_ecommerce_pipeline`: results are now grouped by category — each stage (产品展示图, 场景图, 卖点图, 模特图, 营销海报, 模特合成, 文案) is returned as a separate section with inline images, instead of a flat count summary
- `get_space_status`: when pipeline is complete, returns the same grouped image/text output instead of a raw progress table

### Fixed

- `run_ecommerce_pipeline` and `get_space_status` were referencing a non-existent `stages` field; corrected to use `pipelineOutputs` from the actual API response
- `PipelineStatus` type updated to match the real API response shape (`pipelineOutputs`, `runningStageId`, `failedTasks`); removed incorrect `stages` field

## [1.0.2] - 2026-03-12

### Fixed

- `upload_product_image`: local file upload now infers the correct MIME type (`image/jpeg` / `image/png` / `image/webp`) from the file extension instead of sending `application/octet-stream`, which was causing the server to reject the upload
- `upload_product_image`: URL upload now reads the `Content-Type` response header (with URL extension as fallback) instead of always assuming `image/jpeg`, preventing failures for PNG and WebP sources
- Extracted shared `buildMultipart()` helper to eliminate duplicated multipart body construction

## [1.0.1] - 2026-03-12

### Fixed

- Added `openclaw.extensions` field to `package.json` so `openclaw plugins install` registers the extension entry point correctly after `clawhub install`

## [1.0.0] - 2026-03-09

### Added

- Initial release to ClawHub marketplace
- **OAuth one-click authorization** — connect your AI Product Space account with a single click, no manual API key needed
- 7 tools for full ecommerce asset workflow:
  - `create_space` — create a product workspace
  - `upload_product_image` — upload product photo (local path or URL)
  - `run_ecommerce_pipeline` — generate full suite of assets (20+ images, marketing copy)
  - `generate_single_image` — generate custom scene/style images from prompt
  - `generate_video` — generate 8-second showcase video
  - `get_space_status` — check workspace and pipeline progress
  - `list_assets` — browse generated assets
- Support for 10 output languages (zh, en, ja, ko, fr, de, es, pt, ar, ru)
- Pipeline polling with configurable intervals and timeout
- Manual API key fallback for offline/headless environments
