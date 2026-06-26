# Discord Voice Agent upgrade roadmap

## Best next upgrades

1. **Repo hygiene**
   - make the project a clean standalone repo/release unit
   - keep runtime files out of source control

2. **Reliability**
   - reconnect/rejoin hardening
   - capture finalization cleanup
   - interruption handling during playback
   - safer fallback chains

3. **Latency**
   - faster acknowledgements
   - shorter reply compaction
   - cached answers for simple prompts
   - cut slow context before model calls

4. **Observability**
   - timing per stage: STT, reply, TTS, playback
   - fallback rate and error reasons
   - clearer `/status` output

5. **Soak testing**
   - long voice sessions
   - interruption-heavy sessions
   - voice turn edge cases

## Product ideas that make the skill more useful

- voice assistant for a Discord server
- OpenClaw-powered meeting helper
- live voice Q&A bot
- small-hardware local voice agent
- voice debugging/health dashboard

## What would make the skill feel premium

- quickstart that works in under 10 minutes
- opinionated defaults
- clear troubleshooting guidance
- reproducible smoke test
- release notes / versioning discipline
- visible health and status surfaces
- model-routing explanation that a new user can understand
