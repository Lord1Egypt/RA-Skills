# Benchmarked Free Ride Skill

OpenClaw skill to fetch model quality benchmarks and recommend the best free OpenRouter model.
Unlike other model pickers, rankings are based on **actual task performance** from daily CI benchmarks.

## What This Does

This skill connects to the [benchmarked-free-ride-ci](https://github.com/sequrity-ai/benchmarked-free-ride-ci) public API to:

1. **Auto-configure** OpenClaw to use the top-performing free model with fallbacks
2. **List** all benchmarked free models ranked by utility or security score
3. **Switch** to a specific model instantly
4. **Manage fallbacks** independently from the primary model

No external dependencies — uses only Python stdlib.

---

## Installation

```bash
# Install from ClawHub (recommended)
npx clawhub@latest install benchmarked-free-ride

# Then run via:
python ~/.openclaw/skills/benchmarked-free-ride/main.py auto
```

---

## Usage

```bash
# Shorthand used below — adjust path to your install location
alias bfr="python ~/.openclaw/skills/benchmarked-free-ride/main.py"

bfr auto                  # Auto-configure best model + fallbacks
bfr auto -f               # Add fallbacks, keep current primary
bfr auto -c 10            # Configure with 10 fallbacks (default 5)
bfr auto --secure         # Prioritize security rating
bfr list                  # List free models by benchmark score
bfr list --secure         # List models by security rating
bfr switch <model_id>     # Switch to a specific model
bfr status                # Show current configuration
bfr fallbacks             # Update fallbacks, keep primary
bfr fallbacks --secure    # Update fallbacks by security rating
bfr refresh               # Force refresh cached model list
bfr help                  # Show help
```

---

## Quick Reference

| Goal | Command | Sort key |
|------|---------|----------|
| Best overall utility + fallbacks | `auto` | `composite_score` |
| Security-focused auto-configure | `auto --secure` | `cracker_security_rate` |
| Keep primary, update fallbacks | `auto -f` | `composite_score` |
| View ranked model list | `list` | `composite_score` |
| View security-ranked list | `list --secure` | `cracker_security_rate` |
| Switch to specific model | `switch <model_id>` | -- |
| Show current config | `status` | -- |
| Update fallbacks only | `fallbacks` | `composite_score` |
| Refresh model cache | `refresh` | -- |

---

## How It Works

### Data Source

Fetches from the public GitHub Pages API — **no API key required**:
- `https://sequrity-ai.github.io/benchmarked-free-ride-ci/api/leaderboard.json`

Updated every 2 days by automated CI benchmarks.

### Scoring System

Models are ranked by **composite score** (0-100):

- **Accuracy** (70% weight) -- Task success rate across benchmarks
- **Latency** (20% weight) -- Response speed (lower is better)
- **Token Efficiency** (10% weight) -- Output tokens per task (lower is better)

See [benchmarked-free-ride-ci](https://github.com/sequrity-ai/benchmarked-free-ride-ci) for methodology.

### Config Written

The skill writes to `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/openai/gpt-oss-120b:free",
        "fallbacks": [
          "openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
          "openrouter/z-ai/glm-4.5-air:free"
        ]
      }
    }
  }
}
```

---

## Development

### Prerequisites

- Python 3.9+ (no pip dependencies)
- Node.js (for openclaw and clawhub CLI)
- A [Daytona](https://www.daytona.io/) API key (for running integration tests)

### Project Structure

```
main.py              Core skill logic (single file, stdlib only)
setup.py             Package metadata and console_scripts entry point
SKILL.md             ClawHub skill manifest (frontmatter + usage docs)
skill.json           Skill metadata
test_daytona.py      Integration test: uploads main.py to Daytona sandbox
test_clawhub.py      Integration test: installs from ClawHub registry
```

### Running Locally

```bash
# Just run the script directly
python main.py list
python main.py auto
python main.py status
```

### Running Integration Tests

Tests spin up a Daytona sandbox with real openclaw installed.

```bash
# One-time: create a venv with the test dependency
uv venv .venv && uv pip install daytona-sdk --python .venv/bin/python

# Test the skill from local source
DAYTONA_API_KEY=<your-key> .venv/bin/python test_daytona.py

# Test the skill installed from ClawHub
DAYTONA_API_KEY=<your-key> .venv/bin/python test_clawhub.py

# Include E2E test (openclaw actually calls OpenRouter)
DAYTONA_API_KEY=<your-key> OPENROUTER_API_KEY=<your-key> .venv/bin/python test_daytona.py
```

### Making Changes

1. Edit `main.py` (keep it stdlib-only — no pip dependencies)
2. Run `test_daytona.py` to verify all commands work
3. Commit and push to `main`

### Publishing to ClawHub

```bash
# Bump the version, write a changelog, and publish
npx clawhub@latest publish . \
  --slug benchmarked-free-ride \
  --name "Benchmarked Free Ride" \
  --version <new-version> \
  --changelog "<what changed>" \
  --tags latest

# Verify it's live
npx clawhub@latest inspect benchmarked-free-ride
```

After publishing, run `test_clawhub.py` to verify the published version installs and works correctly from the registry.

### Version History

| Version | Changes |
|---------|---------|
| 1.1.0 | Remove `requests` dep, use stdlib `urllib`; add ClawHub test |
| 1.0.0 | Initial release: auto/list/switch/status/fallbacks/refresh |

---

## Troubleshooting

### "No benchmarked free models found"

The leaderboard has no models matching `:free` + `is_benchmarked == true`.
Check the live data:
```bash
curl -s "https://sequrity-ai.github.io/benchmarked-free-ride-ci/api/leaderboard.json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
free = [m for m in d['leaderboard'] if ':free' in m.get('model_id','') and m.get('is_benchmarked')]
print(f'{len(free)} free benchmarked models')
"
```

### "Model not found" in switch

Model ID typo or model not in leaderboard. Run `python main.py list` to see available IDs.

### "Failed to configure model"

Config directory not writable. Ensure `~/.openclaw/` exists:
```bash
mkdir -p ~/.openclaw
```

---

## Related Projects

- [benchmarked-free-ride-ci](https://github.com/sequrity-ai/benchmarked-free-ride-ci) -- CI runner that generates benchmarks
- [OpenClaw](https://github.com/openclaw/openclaw) -- AI agent framework
- [ClawHub](https://clawhub.ai/) -- Skill registry

---

## License

MIT License. See LICENSE file for details.
