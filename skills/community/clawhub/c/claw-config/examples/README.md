# Examples

Sample JSON5 patches for `claw-config plan` / `apply`.

Before running any of these:

1. Replace `myagent` with your actual `$OPENCLAW_AGENT_ID`.
2. Read the related docs page:
   ```bash
   claw-config docs channels/telegram
   claw-config docs cli/config
   ```
3. Dry-run first:
   ```bash
   OPENCLAW_AGENT_ID=myagent claw-config plan examples/<file>.json5
   ```
4. Apply when the diff looks right:
   ```bash
   OPENCLAW_AGENT_ID=myagent claw-config apply examples/<file>.json5
   ```

## Files

| File | What it does |
|---|---|
| `enable-native-skills.json5` | Set `commands.nativeSkills: true` for an agent's Telegram account. Fixes the case where workspace skills are silently hidden from chat dispatch. |
| `set-model-override.json5` | Sketch for overriding `model.primary` on a single agent. Note: editing entries inside `agents.list[]` requires either submitting the entire array or using `openclaw config patch --replace-path`. Read the comments inside before using. |

PRs welcome adding more recipes — especially for cron bindings, memorySearch overrides, and channel-specific configs.
