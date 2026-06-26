# ClawTK Config Patches

Every change ClawTK makes to your OpenClaw config, explained.

## Heartbeat Isolation (`isolatedSession: true`, `lightContext: true`)

**What it does**: Runs heartbeat checks in a separate, minimal session instead of your main session.

**Why it saves money**: A default heartbeat sends your entire session context (~100K tokens) with every check. With isolation, heartbeats only send ~3K tokens. If your heartbeat fires every 30 minutes, that's 100K wasted tokens every half hour.

**Savings**: ~97% reduction per heartbeat call.

## Heartbeat Interval (`every: "55m"`)

**What it does**: Changes how often OpenClaw checks for new messages/events.

**Why 55 minutes**: Anthropic's prompt cache has a 60-minute TTL. By firing at 55 minutes, we keep the cache warm so the next real interaction gets the 90% cache discount. The default 30-minute interval means nearly double the heartbeat calls.

**Savings**: ~45% fewer heartbeat API calls.

## Heartbeat Model (`model: "google/gemini-2.5-flash-lite"`)

**What it does**: Uses Google's cheapest model for heartbeat checks instead of your primary model.

**Why it's safe**: Heartbeats are simple "has anything changed?" checks. They don't need Opus-level reasoning. Flash Lite costs ~98% less per token.

**Savings**: ~98% cost reduction per heartbeat.

## Context Token Cap (`contextTokens: 100000`)

**What it does**: Limits the context window to 100K tokens instead of the default 200K.

**Why it saves money**: Larger context = more tokens billed per API call. Most tasks work fine within 100K. The default 200K causes unnecessary context accumulation.

**Savings**: Prevents runaway costs from context bloat.

## Image Downscaling (`imageMaxDimensionPx: 800`)

**What it does**: Resizes images to max 800px before sending to the model (default is 1200px).

**Why it's safe**: 800px captures all readable text and UI detail. The extra resolution at 1200px rarely adds useful information but costs ~40% more in vision tokens.

**Savings**: ~40% fewer vision tokens.

## Compaction Model (`compaction.model: "google/gemini-2.5-flash-lite"`)

**What it does**: Uses a cheap model for context compaction (summarizing old messages to free up context space).

**Why it's safe**: Compaction is summarization, not complex reasoning. A cheaper model does this equally well.

**Savings**: Reduces compaction costs to near-zero.

---

## Restoring Your Config

All patches are fully reversible. Run `/clawtk restore` to revert to your original config (backed up before any changes).
