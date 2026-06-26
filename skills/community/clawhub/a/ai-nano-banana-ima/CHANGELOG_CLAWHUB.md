# Changelog — ai-nano-banana-ima

All notable changes to the **IMA Nano Banana Image Generator** skill will be documented in this file.

---

## [1.1.0] - 2026

### Changed (registry / security)

- **Registry metadata aligned with code and SKILL.md**
  - `clawhub.json`: Aligned structure with `ima-image-ai` — removed `optionalEnvVars`, added proper `requires.env`, `requires.primaryCredential`, `requires.credentialNote`, `persistence`, and `localPaths`.
  - `SKILL.md` frontmatter: Added `requires.env: [IMA_API_KEY]`, `persistence`, `version`, `category`, `author`, `keywords`, and `argument-hint` so scanners and registries can see required credentials and config paths.
  - `_meta.json`: Added `ownerid` field for registry consistency.
  - `SECURITY.md`: Simplified credential flow documentation to match `ima-image-ai` format.
- **Removed optional environment variable override mechanism**
  - Removed `IMA_UPLOAD_APP_ID` and `IMA_UPLOAD_APP_KEY` optional env vars.
  - Upload signing now uses fixed shared credentials (same as `ima-image-ai`).
  - Removed `--allow-secondary-upload-domain` CLI flag.
- Addresses ClawHub "Suspicious" review: metadata mismatch (SKILL.md frontmatter missing `requires.env`, `persistence`), and inconsistent manifest (`_meta.json` missing `ownerid`). No functional change; metadata alignment only.

### Requirements

- IMA API key (`IMA_API_KEY` or `--api-key`).
- Python 3, `requests`.

### Endpoints

- `api.imastudio.com` — main image generation API.
- `imapi.liveme.com` — image upload (used for image_to_image when input is a local file). IMA API key is sent to both; both are IMA Studio.

### Model Scope

- `gemini-3.1-flash-image` (Nano Banana 2) — budget option, 4-13 pts
- `gemini-3-pro-image` (Nano Banana Pro) — premium option, 10-18 pts
