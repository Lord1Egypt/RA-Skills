# Fulcra Annotation API Notes

Loaded only when schema details matter.

## Definition Endpoints

The public OpenAPI document is served from:

`https://api.fulcradynamics.com/openapi.json`

Documented annotation definition endpoints:

- `GET /user/v1alpha1/annotation`
- `POST /user/v1alpha1/annotation`
- `GET /user/v1alpha1/annotation/{annotation_id}`
- `PUT /user/v1alpha1/annotation/{annotation_id}`
- `DELETE /user/v1alpha1/annotation/{annotation_id}`
- `POST /user/v1alpha1/annotation/{annotation_id}/cancel_deletion`

Supported definition types:

- `moment`
- `boolean`
- `numeric`
- `scale`
- `duration`
- `people`

## Event Ingest

The generic ingest endpoint is:

`POST /ingest/v1/record`

Payload shape:

```json
{
  "specversion": 1,
  "data": "{\"note\":\"optional note\",\"value\":4}",
  "metadata": {
    "data_type": "ScaleAnnotation",
    "recorded_at": "2026-05-14T19:30:00Z",
    "source": [
      "com.example.agent",
      "com.fulcradynamics.annotation.<annotation-id>"
    ],
    "tags": [],
    "content_type": "application/json"
  }
}
```

Observed readback data classes:

- Moment annotations: `/data/v1alpha1/event/MomentAnnotation`
- Duration annotations: `/data/v1alpha1/event/DurationAnnotation`
- Boolean annotations: `/data/v1alpha1/metric/BooleanAnnotation`
- Numeric annotations: `/data/v1alpha1/metric/NumericAnnotation`
- Scale annotations: `/data/v1alpha1/metric/ScaleAnnotation`

## Current Gaps

The beta CLI currently does not expose annotation write commands or Magic Link retrieval. Prefer the bundled REST script until upstream CLI support lands.
