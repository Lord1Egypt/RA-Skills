# Ghostclaw Profiling Guide

## Quick Start

```bash
cd ghostclaw-clone
OPENAI_API_KEY=dummy python scripts/ghostclaw_profiler.py [OPTIONS] [REPO_PATH]
```

## Options

- `--no-cache` Disable analysis caching (default: cache enabled)
- `--no-parallel` Disable parallel file scanning (WARNING: causes 300× slowdown!)
- `--concurrency-limit N` Set max concurrent operations (default: 32)
- `--no-profile` Disable cProfile (only phase timers)
- `--save-profile FILE` Save raw cProfile data to binary file

## Examples

```bash
# Profile default configuration (parallel enabled)
python scripts/ghostclaw_profiler.py

# Profile with AI synthesis (dry-run to avoid real API)
python scripts/ghostclaw_profiler.py --use-ai  # Note: may need --dry-run flag added

# Profile with high concurrency
python scripts/ghostclaw_profiler.py --concurrency-limit 64

# Profile without parallel (for comparison - will be slow!)
python scripts/ghostclaw_profiler.py --no-parallel

# Save raw profile data for snakeviz
python scripts/ghostclaw_profiler.py --save-profile profile.pstats
snakeviz profile.pstats
```

## Key Metrics

- **Total time**: Target < 1s for typical repos (<1000 files)
- If > 10s, check `parallel_enabled` is true
- Function-level breakdown in cProfile output

## Interpreting Results

- Look for high cumulative time in `asyncio/base_events.py:_run_once` → indicates too many small async tasks
- `{method 'poll' of 'select.epoll'}` → I/O wait time
- Functions > 0.5s are candidates for optimization

See `TIMING-ANALYSIS.md` for full report.
