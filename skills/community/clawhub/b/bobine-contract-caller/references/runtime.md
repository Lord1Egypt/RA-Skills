# Runtime and env

## Reference links

- Concept overview: <https://www.bobine.tech/>
- Bobine project: <https://github.com/hazae41/bobine>
- Standard libraries for Bobine WebAssembly VM: <https://github.com/hazae41/stdbob>

## Required env vars

```bash
node ./scripts/keygen.mjs
```

This prints:

```json
{
  "sigkey": "<pkcs8-hex>",
  "pubkey": "<spki-hex>"
}
```

## Call interface

Use one command for Bobine interactions:

```bash
node ./scripts/call_bobine.mjs \
  --server http://localhost:8080 \
  --module <target-module> \
  --method <target-method> \
  [--param <typed-param>]... \
  [--auth-module <ed25519-module>] \
  [--sigkey <private-ed25519-pkcs8-hex>] \
  [--pubkey <public-ed25519-spki-hex>] \
  [--spark-effort <target>] \
  [--spark-hex <single-spark-hex>]
```

Required for every call:

- `--server`
- `--module`
- `--method`

Required only for signed calls:

- `--auth-module`
- `--sigkey`
- `--pubkey`

Optional spark controls:

- `--spark-effort`
  - default inline target: `1048576`
- `--spark-hex`
  - use only when you explicitly want to provide a single spark for this exact call

## Script outputs

Success output is JSON:

```json
{
  "logs": ["..."],
  "returned": { "type": "text", "value": "ok" },
  "sparkHex": "abcd...",
  "reportedSparks": "1"
}
```

`reportedSparks` is whatever the Bobine server reports in the proof tuple.

## Failure modes

- Missing required CLI args: immediate usage error
- Invalid param syntax: parser error before network call
- Non-2xx HTTP status: error includes status and response body
- Invalid session or unauthorized call: Bobine logs usually explain the rejection

## Performance notes

- Automatic spark generation is CPU-bound
- The default behavior is to generate one spark inline per call
- Only pass `--spark-hex` when you already have a single spark you want to consume immediately
