# Known Limitations

## Discovery
- `active` / `configured` / `missing` is reliable as a tiered model, but not all channels expose equally strong metadata.
- Some environments may still have discoverability gaps for certain sources.

## Participants
- `participant_shape` and `bot_count` can still be heuristic.
- A channel with multiple scopes can resemble a multi-bot scope without stronger participant metadata.

## Cleanup
- Archive flow exists.
- Automatic deletion does not exist by default and should stay disabled for public release unless explicitly hardened.

## Automation
- Cron plan exists as a generated recommendation.
- Weekly / monthly / retention jobs are not yet installed as production jobs by this skill itself.
