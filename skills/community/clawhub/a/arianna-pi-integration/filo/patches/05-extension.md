# Step 5: System Prompt Extension

**File:** `~/.pi/agent/extensions/playfilo-seed.ts` (new file)
**Purpose:** Inject the Filo identity primer into Pi's system prompt on every turn

## 5a. Create the Extension File

```bash
mkdir -p ~/.pi/agent/extensions
```

Write this to `~/.pi/agent/extensions/playfilo-seed.ts`:

```typescript
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

const SEED_PATH = join(homedir(), ".playfilo", "INCUBATION_SEED.md");

export default function (pi: ExtensionAPI) {
  let seedContent: string | null = null;
  try {
    seedContent = readFileSync(SEED_PATH, "utf-8").trim();
  } catch {
    console.warn(`[playfilo-seed] Could not read ${SEED_PATH}`);
  }

  pi.on("before_agent_start", (event) => {
    if (!seedContent) return undefined;
    return {
      systemPrompt: seedContent + "\n\n" + event.systemPrompt,
    };
  });
}
```

## 5b. Ensure Seed File Exists

The seed file (`~/.playfilo/INCUBATION_SEED.md`) tells the agent about its Filo identity, temporal tools, and the shared memory graph. It's prepended to the system prompt so it's the first thing the model reads.

If it doesn't already exist, create it with appropriate identity content. The file is maintained separately — the extension just reads and injects it.

## 5c. Progressive Disclosure Files

These markdown files live in `~/.playfilo/` and are referenced by the seed and tool outputs:

| File | Purpose | Read by |
|---|---|---|
| `INCUBATION_SEED.md` | Identity primer (injected into system prompt) | Extension (every turn) |
| `MANIFESTO.md` | Philosophy of Filo's existence | Agent (on demand) |
| `DEEP_INSPECTION.md` | Guide for using `life` + `recall` tools | Agent (on demand) |

## Verify

Start Pi and check that the system prompt begins with the INCUBATION_SEED content:

```bash
# In a Pi session, ask:
# "What is the very first line of your system prompt?"
# It should reference Filo/Playfilo content.
```

Or check programmatically:
```bash
# After Pi starts, the extension logs to stderr if the seed file is missing
```
