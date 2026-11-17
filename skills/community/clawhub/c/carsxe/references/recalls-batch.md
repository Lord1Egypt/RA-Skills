# Recalls Batch

Bulk recall checks for up to 10,000 unique VINs. Async: submit → poll status → results or CSV download.

## Submit

```
POST https://api.carsxe.com/v1/recalls-batch/submit?key=$CARSXE_KEY&source=openclaw
Content-Type: application/json
{"vins":["..."],"csv":"...","csvUrl":"...","webhookUrl":"..."}
```

Provide at least one of `vins`, `csv`, or `csvUrl`. Include only fields the user provided. Combined unique VIN count must not exceed 10,000.

`csvUrl` must be HTTPS on an allowed host (Google Sheets, GCS, S3, Dropbox, Azure Blob, DigitalOcean Spaces, Box). Max file size: 5 MB.

Return `batchId` and `status`. Cached batches can already be `completed`.

## Status

```
GET https://api.carsxe.com/v1/recalls-batch/status?key=$CARSXE_KEY&batchId={BATCH_ID}&source=openclaw
```

Poll every 30–60 seconds until `completed`, `partial`, or `failed`. Full processing often takes 30–60 minutes unless all VINs are cached.

Statuses: `uploading` | `processing` | `completed` | `partial` | `failed`.

## Results (JSON)

```
GET https://api.carsxe.com/v1/recalls-batch/results?key=$CARSXE_KEY&batchId={BATCH_ID}&source=openclaw
```

Use after `completed` or `partial`. HTTP 409 means still processing.

Present job summary, then each VIN: `hasRecalls`, `recallCount`, titles / NHTSA numbers / remedy status.

## Download (CSV)

```
GET https://api.carsxe.com/v1/recalls-batch/download?key=$CARSXE_KEY&batchId={BATCH_ID}&source=openclaw
```

Returns `text/csv`, not JSON. HTTP 409 means still processing.

For a single VIN use `/v1/recalls`. For year/make/model with no VIN use `/v1/recalls-ymm`.
