# MapSpecV1 notes

- `version` must be `1`.
- `paths[].waypoints` accepts airport codes, city names, or coordinate objects.
- `projection.mode` should usually stay `auto` unless the user explicitly wants a projection comparison.
- `etops.enabled` should be `true` only when the user is asking about diversion coverage or alternates.
- `mapStyle.globeTexture` affects the rendered look but not route geometry.

Quick examples:

```json
{
  "version": 1,
  "paths": [
    {
      "waypoints": ["JFK", "LHR"],
      "type": "geodesic"
    }
  ]
}
```

```json
{
  "version": 1,
  "paths": [
    {
      "waypoints": ["LAX", "HNL", "NRT"],
      "type": "geodesic"
    }
  ],
  "etops": {
    "enabled": true,
    "ruleTimes": [180],
    "engineOutSpeed": 420,
    "speedUnit": "kts"
  }
}
```
