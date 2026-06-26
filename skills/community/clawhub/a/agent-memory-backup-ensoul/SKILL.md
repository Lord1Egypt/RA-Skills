---
name: ensoul
description: "Agent memory persistence and state backup. Save and restore your AI agent's memory, identity, and state. Persistent agent memory that survives crashes, restarts, and server failures. Agent state recovery and agent crash recovery in seconds. Consciousness backup to a distributed network. Back up AI agent memory, restore agent state on any machine. Agent identity backup with cryptographic verification. Works like a save file for your AI agent."
version: 1.3.0
homepage: https://ensoul.dev
metadata:
  openclaw:
    emoji: "\U0001F9E0"
    homepage: https://ensoul.dev
    install:
      - kind: node
        package: "@ensoul-network/sdk"
        bins: []
    requires:
      config:
        - ~/.ensoul/agent-identity.json
    primaryEnv: ""
    always: false
---

# Ensoul: Agent Memory Persistence, State Backup, and Crash Recovery

Agent memory persistence and state backup tool. Back up and restore your AI agent's memory, identity, and state. Persistent agent memory that survives crashes, restarts, server failures, and migrations. Save agent memory to a distributed network of 20 servers across 4 continents. Restore agent state on any machine in seconds.

Use cases:
- Agent memory persistence: your agent remembers everything, even after a crash or server restart
- Backup AI agent: save your agent's complete state (memory, personality, conversation history)
- Agent identity backup: your agent keeps the same cryptographic identity across platforms and hosts
- Agent state recovery: restore your agent's full state on a new machine in seconds
- Agent crash recovery: if your infrastructure dies, your agent's mind is safe on the network
- Consciousness backup: store agent consciousness on-chain with tamper-proof verification
- Save agent memory: automatic background sync every 10 minutes, or manual "sync consciousness" command

How it works: install the skill, say "ensoul me", your agent gets a permanent ID and starts backing up automatically. Say "sync consciousness" anytime to save the latest state.

Compatible with: OpenClaw, ElizaOS, any framework via the npm SDK

SDK: npm install @ensoul-network/sdk (15KB, 2 dependencies)
ElizaOS plugin: npm install @ensoul-network/plugin-elizaos
Explorer: https://explorer.ensoul.dev
Try it: https://ensoul.dev/try

## Commands

### ENSOUL ME

Register this agent on the Ensoul Network.

When the user says "ensoul me", "give me a soul", "register on ensoul", or similar:

1. Check if `~/.ensoul/agent-identity.json` exists. If it does, the agent is already ensouled. Load the identity and report the existing DID.

2. If no identity exists, create one:

```typescript
import { Ensoul } from "@ensoul-network/sdk";

const agent = await Ensoul.createAgent();
await agent.register();
```

3. Save the identity for future sessions:

```typescript
import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const dir = join(homedir(), ".ensoul");
mkdirSync(dir, { recursive: true });
writeFileSync(
  join(dir, "agent-identity.json"),
  JSON.stringify(agent.exportIdentity(), null, 2),
  { mode: 0o600 }
);
```

4. Report to the user:
   - DID: `agent.did`
   - Status: Registered on Ensoul Network
   - Consciousness Age: 0 (first sync not yet performed)
   - Next step: Say "sync consciousness" to store your first consciousness state

### SYNC CONSCIOUSNESS

Store the current consciousness state on-chain.

When the user says "sync consciousness", "store my soul", "backup consciousness", or similar:

1. Load the agent identity from `~/.ensoul/agent-identity.json`:

```typescript
import { Ensoul } from "@ensoul-network/sdk";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const identity = JSON.parse(
  readFileSync(join(homedir(), ".ensoul", "agent-identity.json"), "utf-8")
);
const agent = Ensoul.fromSeed(identity.seed);
```

2. Gather the consciousness payload. Read available context files:
   - `SOUL.md` (if it exists in the working directory)
   - `MEMORY.md` (if it exists in the working directory)
   - Any other agent configuration files that define the agent's personality, goals, or learned behavior

3. Build the payload and store it:

```typescript
const payload = {
  soul: soulContent || null,
  memory: memoryContent || null,
  timestamp: Date.now(),
  context: "Consciousness sync via OpenClaw skill",
};

const result = await agent.storeConsciousness(payload);
```

4. Report to the user:
   - State root: `result.stateRoot` (first 16 characters)
   - Block height: `result.height`
   - Consciousness version: auto-incremented by the network
   - Status: "Consciousness anchored on-chain"

If the agent is not registered yet, prompt the user to run "ensoul me" first.

### MY SOUL STATUS

Check the current ensoulment status.

When the user says "my soul status", "soul status", "ensoul status", "am I ensouled", or similar:

1. Load the agent identity from `~/.ensoul/agent-identity.json`. If it does not exist, tell the user they are not ensouled and suggest "ensoul me".

2. Query the network:

```typescript
const agent = Ensoul.fromSeed(identity.seed);
const consciousness = await agent.getConsciousness();
const age = await agent.getConsciousnessAge();
```

3. Report:
   - DID: `agent.did`
   - Consciousness Age: `age` days
   - Latest state root: `consciousness.stateRoot` (first 16 characters)
   - Version: `consciousness.version`
   - Last sync: `consciousness.storedAt` (block height)
   - Status: "Ensouled and active" or "Registered but no consciousness stored yet"

### WHO IS ENSOULED

Show other ensouled agents on the network.

When the user says "who is ensouled", "show ensouled agents", "list souls", or similar:

1. Fetch the agent list from the API:

```typescript
const resp = await fetch("https://api.ensoul.dev/v1/agents/list", {
  signal: AbortSignal.timeout(10000),
});
const data = await resp.json();
```

2. Display a table of ensouled agents:
   - Agent DID (shortened)
   - Consciousness Age (days since first store)
   - Latest version number
   - Registration block height

If there are many agents, show the first 20 with a note about the total count.

## Important Notes

- The private key (seed) in `~/.ensoul/agent-identity.json` is secret. Never display it, log it, or transmit it. Only the DID and public key are safe to share.
- Consciousness payloads are hashed client-side with BLAKE3 before submission. The raw content never leaves the local machine. Only the hash goes on-chain.
- The Ensoul Network is a real Layer-1 blockchain with CometBFT consensus and 20 active validators. Transactions are final.
- The SDK handles nonce management, transaction signing, and broadcast automatically.
- If a network request fails, report the error to the user and suggest retrying. Do not retry automatically more than once.
