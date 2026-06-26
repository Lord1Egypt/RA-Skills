# Structure Extract Payload Notes

## Job Type Mapping
1. User-facing structure extraction -> `img2mol`

## `/api/jobs` Required Form Fields
1. `name`
2. `type` (`img2mol`)
3. `args` (JSON string)
4. `ws_id`
5. `expect_tokens`, `avail_tokens` (required in non-private mode)

## `args` Required Fields
1. `dataset_id` (input PDF/image dataset id)
2. `page_list` (integer list)

## Dataset Requirement
1. `dataset_id` must have `extras.osskey` (check via `GET /api/dataset/{dataset_id}/metainfo`).
2. Generic `/api/dataset/upload` datasets often do not satisfy this requirement.

## `args` Optional Fields
1. `account` (`person` or `team`)

## Minimal Stable Template
```json
{
  "dataset_id": "YOUR_DATASET_ID",
  "page_list": [1, 2, 3],
  "account": "person"
}
```

## Token Estimate Mapping
Use `/api/token/estimate` with:
1. `task_type = img2mol`
2. `input_amount = len(page_list)`
3. `extra_multiples = 1`

Backend billing logic is `len(page_list) * task_token_map['img2mol']`.

## Page List Notes
1. Page index is integer and typically 1-based in UI workflows.
2. Use a non-empty list; empty list usually creates a zero-work job.

## Common Errors
1. `dataset_id` missing in `args`
2. `page_list` malformed (not integer list)
3. `${field} must be provided`: missing top-level field in `/api/jobs`
4. `Insufficient account balance`: available token insufficient for selected pages
5. `dataset ... not found`: dataset id invalid or inaccessible
