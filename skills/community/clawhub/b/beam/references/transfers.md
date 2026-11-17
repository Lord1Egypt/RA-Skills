# Beam transfers reference

## How a transfer runs

1. The helper (the Beam Python SDK) reads the source object's size and signs
   short-lived, chunk-scoped access to the source and every destination **in its
   own process**. Storage credentials are never sent to Beam or to workers.
2. BeamCore splits the object into chunks (40 MiB minimum, larger for big
   objects) and assigns them to competing orchestrators. Their workers read each
   chunk from the source and write it to every destination.
3. When every chunk is verified, BeamCore completes the destination objects and
   the transfer becomes `completed`.

While the transfer runs, the helper re-signs routes that expire and answers
integrity checks. That is why its process must live until the final event.

## Credentials and permissions

Credentials must not be restricted to specific IP addresses or networks:
independent workers use the signed routes from their own hosts.

**Amazon S3 and S3-compatible stores** (`s3://`, `s3c://`). The source needs
`s3:GetObject`, plus `s3:GetObjectVersion` on a versioned bucket. The destination
needs:

```json
[
  {
    "Effect": "Allow",
    "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject",
               "s3:AbortMultipartUpload", "s3:ListMultipartUploadParts"],
    "Resource": "arn:aws:s3:::DESTINATION-BUCKET/*"
  },
  { "Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": "arn:aws:s3:::DESTINATION-BUCKET" }
]
```

The destination needs read and delete too: the SDK reads uploaded parts back to
check them, and cleans up temporary objects under `<destination-key>.beam-recovery/`.

**Cloudflare R2** (`r2://`). Use an R2 API token with **Object Read only** for a
source bucket and **Object Read & Write** for a destination bucket. The endpoint
is `https://<account-id>.r2.cloudflarestorage.com` unless `R2_ENDPOINT_URL` is set.

**Hippius** (`hippius://`). One API token. Workers never receive it.

**Hugging Face** (`hf://`). A token that can read the source repo, and write to
the destination repo. Uploading to the Hub from a non-Hub source needs
`--hf-allow-source-rehash`, because the Hub requires the file's sha256 before it
issues upload URLs, so the SDK reads the source once. `--hf-commit-message` and
`--hf-create-pr` shape the commit. A Hugging Face destination takes exactly one
source.

**Different accounts on each side.** Append `?env=PREFIX` to a URI and the helper
reads `PREFIX_<VAR>` for that endpoint, for example `s3://bucket/key?env=DST`
reads `DST_AWS_ACCESS_KEY_ID` and `DST_AWS_SECRET_ACCESS_KEY`.

## Statuses

| Status | Meaning |
| --- | --- |
| `pending` | Created, awaiting assignment |
| `in_progress` | Chunks are moving |
| `completed` | All chunks verified, destination objects complete |
| `failed` | Terminal error; read `error_message` |
| `cancelled` | Cancelled by the client or a timeout |

If an orchestrator or worker stalls, Beam reassigns its chunks automatically. No
action is needed.

## Errors

| Signal | Cause | What to do |
| --- | --- | --- |
| `error_message` starts with `source_access_denied` | The source storage refused Beam's signed reads | Check read permission and remove any IP or network restriction |
| `error_message` starts with `destination_access_denied` | The destination storage refused the writes | Check the destination permissions above |
| `kind: insufficient_credits` (HTTP 402) | The estimate exceeds the organization's credits | The user adds credits or turns on auto top-up in the Console |
| `kind: auth`, exit 4 | Beam refused the API key, or the key may not create transfers | Get a valid key from the Console's **API Keys** page |
| `kind: source_unreadable` | `estimate` could not read the source size | Check the URI, the credentials and the endpoint |
| `kind: missing_env`, exit 2 | A variable the URI needs is unset | Ask the user to set the variable named in `variable` |

A transfer that was already running when credits ran out still completes and is
charged, so the balance can go below zero.

## Costs

- Transfer: **0.01 credit per GB delivered**, rounded up per transfer to the next
  0.01 credit. GB is decimal (10^9 bytes). 1 credit = $0.50, so $5 per TB.
- Fan-out delivers the object once per destination: 1 TB to 3 destinations is
  about 30 credits.
- Room start: 1 credit. A Studio workflow run: 1 credit plus its transfers.

The helper's `estimated_credits` uses this formula. The Console shows the actual
charge.

## Limits

- **Size must be known.** The helper reads it from the source object, so the
  object must be complete. A growing or live source belongs on a Room `stream`
  or `media` channel.
- **Small objects gain nothing.** Below 40 MiB an object is a single chunk on a
  single worker. Bundle many small files into one archive first.
- **Whole objects only.** There is no sync, delta or deduplication. Work out what
  changed yourself and transfer those objects.
- **Cloudflare R2 range caveat.** Some completed R2 multipart objects with gaps in
  their part numbers return a truncated body for a range that crosses a part
  boundary. A transfer from such a source can fail on a length check. A good
  full-file checksum does not rule this out. Use independently uploaded,
  range-verified source objects.
- **Hippius verification differs.** Hippius uses non-multipart routes, so its
  completion checks differ from S3 multipart. Confirm the destination object
  afterwards if the user needs end-to-end verification.
- **Unsupported endpoints.** Google Cloud Storage and Azure Blob are not
  supported. Plain HTTP sources and destinations work only from code with the
  SDK's HTTP connector (https://docs.b1m.ai/docs/connectors/http), where workers
  receive the URLs and headers directly.

## Helper output

Every stdout line is a JSON object with an `event` field.

| Event | Fields |
| --- | --- |
| `plan` (`--dry-run`) | `source`, `destinations` (each `uri` and the `env` variable names it uses), `name`, `timeout_seconds` |
| `estimate` | `source`, `destinations`, `size_bytes`, `delivered_bytes`, `estimated_credits`, `estimated_usd` |
| `created` | `transfer_id`, `source`, `destinations`, `size_bytes`, `chunks`, `delivery_tasks`, `estimated_credits` |
| `progress` | `transfer_id`, `status`, `bytes_transferred`, `total_bytes`, `percent` |
| `completed` | `transfer_id`, `size_bytes`, `delivered_bytes`, `destinations_completed`, `started_at`, `completed_at`, `integrity_check_warning` |
| `failed` | `transfer_id`, `error_message`, and `code`/`hint` for storage access errors |
| `cancelled`, `timeout`, `interrupted` | `transfer_id`, plus a `hint` on what to do next |
| `status` | `transfer`, the API object below |
| `cancel` | `transfer_id`, `success`, `message` |
| `error` | `kind`, `message`, and context such as `variable` or `status_code` |

Credential values never appear in the output.

## Reading transfers over HTTP

`https://beamcore.b1m.ai` reads the organization's transfers with the header
`X-Api-Key`. It cannot create transfers. Pass the header through stdin so the key
stays out of the process list:

```bash
printf 'X-Api-Key: %s\n' "$BEAM_API_KEY" | curl -fsS -H @- "https://beamcore.b1m.ai/transfers/$TRANSFER_ID"
printf 'X-Api-Key: %s\n' "$BEAM_API_KEY" | curl -fsS -H @- "https://beamcore.b1m.ai/transfers?status=completed&limit=10"
```

`GET /transfers` takes `limit` (default 20, at most 100), `offset`, `status`,
`order_by` (`created_at` or `completed_at`) and `completed_after` (ISO 8601). To
pick up newly finished transfers, poll with `order_by=completed_at` and
`completed_after` set to the last `completed_at` seen.

A transfer object has `id`, `transfer_key`, `status`, `total_bytes`,
`bytes_transferred`, `error_message`, `metadata`, `created_at`, `started_at` and
`completed_at`. The transfer name is not returned. An unknown ID, or one from
another organization, returns `404`.
