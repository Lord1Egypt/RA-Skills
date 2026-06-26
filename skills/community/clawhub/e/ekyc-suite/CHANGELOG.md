# Changelog

## 1.0.1 (2026-03-31)

- Improved skill description for better discoverability across KYC, eKYC, identity verification, face recognition, liveness detection, deepfake detection, OCR, biometric, AML, compliance, and fintech search queries

## 1.0.0 (2026-03-28)

Initial public release.

### Capabilities

- **Face Comparison** — Compare two face photos, return similarity score 0-100
- **Photo Liveness Detection** — Detect AI-generated, replayed, or synthetic face photos
- **Video Liveness Detection** — Detect deepfake or spoofed face videos with auto-retry
- **ID Card OCR** — Extract structured info from Chinese national ID card
- **Bank Card OCR** — Extract card number and expiry from bank card photo
- **Driver's License OCR** — Extract info from Chinese driver's license
- **Vehicle License OCR** — Extract info from Chinese vehicle license
- **Media Labeling** — Analyze images/videos for 15+ attribute labels

### Features

- Dual credential sets: Key A (capabilities 1-7) and Key B (capability 8) independently configurable
- SHA1 signature with assertion guards
- SSRF protection on URL inputs
- File size validation (20MB limit)
- Auto-retry on network errors with exponential backoff
- Credential sanitization in error messages
