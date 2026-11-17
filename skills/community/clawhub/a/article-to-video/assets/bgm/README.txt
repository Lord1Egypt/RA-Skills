BGM Directory Structure
========================

Place royalty-free background music files in the appropriate style folder.
Supported formats: .mp3, .m4a, .wav
The system will auto-select the first file found in the matching folder.

Folders:
  corporate/   - Business/finance content (calm, professional)
  acoustic/     - Lifestyle/blog content (light, acoustic guitar)
  electronic/   - Technology content (upbeat, electronic)
  cinematic/    - Science/documentary content (orchestral, dramatic)
  soft/         - Education content (gentle, soft piano)

Content Type → BGM Style mapping (configured in config.py):
  finance      → corporate
  business     → corporate
  technology   → electronic
  science      → cinematic
  education    → soft
  news         → corporate
  lifestyle    → acoustic
  default      → corporate

To add your own BGM:
  1. Find royalty-free music (e.g., from YouTube Audio Library, Free Music Archive)
  2. Place the .mp3 file in the matching style folder
  3. The system will automatically use it when the content type matches
