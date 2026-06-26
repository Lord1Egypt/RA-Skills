# Changelog — gcp-fullstack

All notable changes to this skill will be documented in this file.

## [2.0.0] — 2026-02-25

### Added
- Migration guide from v1.x to v2.0.0
- Complete lifecycle coverage in a single skill
- Service selection decision trees (Cloud Run vs Functions vs App Engine)
- Database selection guide (Firestore vs Cloud SQL)
- Cloudflare CDN/security integration
- LLM-based QA evaluation (optional, via OpenRouter)

### Changed
- Consolidated multiple GCP skills into one super-skill
- QA gate extracted to separate `qa-gate-gcp` skill
- Docker now required for Cloud Run builds

### Breaking
- v1.x separate skills replaced by single consolidated skill
- QA validation moved to `qa-gate-gcp`

## [1.0.0] — 2025-02-18

### Added
- Initial release
- Basic GCP scaffold and deploy functionality
