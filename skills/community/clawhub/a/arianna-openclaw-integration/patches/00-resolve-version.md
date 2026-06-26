# Step 0: Resolve Exact Pi Version

**Why:** OpenClaw's `package.json` uses `^0.61.1` (caret range) for pi packages. The installed version may be `0.61.1`, `0.61.2`, etc. The pi-integration-skill must be applied to the **exact same version** to produce compatible compiled output.

## Action

```bash
cd ~/openclaw
pnpm ls @mariozechner/pi-coding-agent
```

Note the exact version (e.g. `0.61.1`). Then:

```bash
# Clone or checkout pi-mono at the matching tag
cd ~/filo-workspace  # or wherever you keep it
git clone https://github.com/badlogic/pi-mono.git pi-mono-<version>
cd pi-mono-<version>
git checkout v<version>  # e.g. v0.61.1
```

If the pi-mono checkout already exists at the correct version, skip the clone.

## Verify

```bash
cd ~/openclaw && pnpm ls @mariozechner/pi-coding-agent
# Should show e.g. @mariozechner/pi-coding-agent 0.61.1

cd ~/filo-workspace/pi-mono-<version>
git describe --tags --exact-match
# Should show e.g. v0.61.1
```

Both versions must match exactly.
