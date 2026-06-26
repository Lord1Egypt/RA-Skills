# Local TTS Queue Performance SLOs

## Targets
- Enqueue latency (producer):
  - p50 <= 20 ms
  - p95 <= 50 ms
- Queue wait under light load:
  - p50 <= 500 ms
- Synth API latency (single request baseline):
  - p50 <= 600 ms
- Burst behavior (3 quick jobs):
  - queue wait should not grow linearly with full playback time for each item

## Measurement method
Use:
```bash
skills/autonoannounce/scripts/benchmark-autonoannounce.sh
```

Collect:
- enqueue timings
- optional direct synth timings
- worker-derived queue wait and end-to-end timings (if available in logs)

## Interpretation
- Fast enqueue + slow end-to-end usually indicates worker/playback bottleneck.
- Linear queue-wait growth indicates strict serial playback pressure; mitigate with coalescing, earcon tuning, and stale-item drops.
- API latency spikes with stable local timings indicate upstream service variance.
