---
name: asr
description: Transcribe audio and video for agents by Speech is Cheap. Fast, high-quality, and cost-effective ($0.06 - $0.12/hr). Use an API key or x402 USDC.
required_environment_variables:
  - name: SIC_API_KEY
    help: https://speechischeap.com/
    required_for: API-key mode
    optional: true
metadata:
  openclaw:
    primaryEnv: SIC_API_KEY
    requires:
      bins: [bash]
      anyBins: [curl, node]
    envVars:
      - name: SIC_API_KEY
        required: false
        description: Required for API-key commands only.
      - name: SIC_X402_WALLET_MODULE
        required: false
        description: Existing wallet module path for new x402 purchases and cancellation.
      - name: SIC_X402_API_BASE
        required: false
        description: Optional x402 API base override; unset uses https://api.speechischeap.com/v2.
---

# Speech is Cheap ASR

Transcribe a media URL or local audio/video file. Jobs are asynchronous;
prefer a caller-supplied webhook, or poll at the caller's chosen interval.
`{baseDir}` is the folder containing this file. Run the helper with `bash`,
because installs can drop its executable bit.

## Data handling

Transcription sends the media URL or file, the chosen options, and any webhook
URL to Speech is Cheap. Send only media the caller asked to transcribe, and
suggest `--private` for sensitive recordings. See the
[Privacy Policy](https://speechischeap.com/privacy/) and
[Security](https://speechischeap.com/company/security/) pages.

## API-key mode

Use the caller's configured `SIC_API_KEY` with Bash and curl. Keep the key out
of output. If it is missing, direct the caller to
[Speech is Cheap](https://speechischeap.com/) for setup. Wallet spending
requires the caller's explicit choice of `--x402`.

OpenClaw sandboxes start without network access or the
`skills.entries.asr.apiKey` setting. To use API-key mode there, enable sandbox
network access and set `SIC_API_KEY` in `agents.defaults.sandbox.docker.env`.
Wallet mode runs only on the host.

```sh
bash {baseDir}/scripts/asr.sh transcribe --url "https://example.com/audio.mp3"
bash {baseDir}/scripts/asr.sh transcribe --file "./audio.wav" \
  --webhook "https://your-domain.com/transcription"
bash {baseDir}/scripts/asr.sh status "job-id-here"
```

## Wallet mode

Wallet mode buys one asynchronous job through x402 and pays native USDC on Base
from the caller's wallet. It needs no Speech is Cheap account, API key, or
Stripe credentials. It needs Node.js 22 or newer and dependencies installed
with `pnpm install --frozen-lockfile` in `{baseDir}`.

Set `SIC_X402_WALLET_MODULE` to the absolute path of the caller's existing
module exporting `signer`, an EVM signer with `address` and `signTypedData`.
Cancellation also needs `signMessage`. Reuse its signing approval and spending
controls. Key custody stays with the caller's wallet.

Obtain the caller's duration in seconds, from 6 to 86,400, and an approved
`--max-usd` price ceiling before buying. Each started minute costs $0.002, plus
$0.002 with `--speakers`, $0.001 with `--words`, and $0.0002 with `--labels`;
the total rounds up to whole cents. For example, 200 seconds without options
costs $0.01. The helper does not measure media. It accepts only x402 v2
`exact` with native USDC on Base, `eip155:8453`, and rejects quotes above the
ceiling before signing. The quote freezes options, the webhook, and the
purchased duration allowance. Keep `--url` and `--webhook` within 2,048
characters, `--user-agent` within 256, and `--language` within 16. The
service declines an authorization that does not expire 6 to 360 seconds after
its own clock, so keep the system clock accurate.

Choose a new `--state` path outside the repository and installed skill for
each purchase. The helper saves the request and proof before sending payment,
with owner-only permissions. Keep the state, temporary files, and upload
tokens out of logs, attachments, and version control.

```sh
mkdir -p "$HOME/.local/state/asr"
bash {baseDir}/scripts/asr.sh --x402 transcribe \
  --url "https://example.com/audio.mp3" --duration 200 --max-usd 0.01 \
  --state "$HOME/.local/state/asr/recording-001.json"
bash {baseDir}/scripts/asr.sh --x402 transcribe \
  --file "./audio.wav" --duration 200 --max-usd 0.01 \
  --state "$HOME/.local/state/asr/recording-002.json" \
  --webhook "https://your-domain.com/transcription"
```

File mode uploads the same file through the one-use continuation after paying
once. Start within 300 seconds of readiness; an accepted transfer can run for
up to one hour. Retries preserve these deadlines and the original file.
Readiness starts when the service confirms payment, which can happen after the
paid request returns. While confirmation is pending, the helper replays the
purchase every 30 seconds for up to 10 minutes. If it still reports a pending
`payment_status`, resume at least once a minute until the upload starts.

## Recovery, status, and cancellation

```sh
bash {baseDir}/scripts/asr.sh --x402 resume --state "$HOME/.local/state/asr/recording-002.json"
bash {baseDir}/scripts/asr.sh --x402 status "job-id-here"
bash {baseDir}/scripts/asr.sh --x402 cancel "job-id-here"
```

Resume accepts no replacement options. An existing proof is replayed
unchanged; a saved request without a proof needs the configured signer and
gets a new quote. Keep the state while settlement or provider submission is
pending, and resolve an uncertain reply with resume or free status. Resume
checks the purchase before every upload, so a failed transfer or a missed start
window reports `FAILED` or `EXPIRED` instead of retrying the upload.

The helper reports these payment outcomes:

- "Payment was declined" and "Settlement was declined" mean the service
  rejected the proof and took no payment, for example for insufficient funds
  or an inaccurate clock. The helper discards that proof, and the service never
  submits it again. Fix the cause, then resume to sign a new quote. If Base
  later shows that transfer anyway, the service treats it as paid: a URL job
  still runs, and an upload purchase expires with a full refund.
- HTTP 404 or 410 means the quote or its authorization expired and the service
  took no payment. Start a new purchase with a new `--state` path.
- "Quote requests are rate limited" names the seconds to wait before
  requesting another quote. Paid requests are never rate limited.

If a purchase stays pending, send its purchase or job ID to
support@speechischeap.com. An existing state path cannot create a second
purchase. After a crash, confirm the PID recorded in `.lock` has stopped
before removing only that stale lock.

Wallet-mode status uses free `GET /v2/jobs/:jobId` without a wallet or API key.
Cancellation requires the original paying wallet and an auth-only SIWX
signature. It creates no payment. `requested` is pending; `confirmed` means
cancellation succeeded, with a full refund owed; `terminal` means the job
finished first.

## Transcription options and results

Both modes support `--speakers` for speaker labels, `--words` for word
timestamps, and `--labels` for sound labels. Use `--language <code>` to select
a language, `--confidence <0..1>` for confidence, and
`--segment-duration <6..30>` for segment length. Defaults are automatic
language detection, confidence 0.5, and 30-second segments.

Omit `--format` for JSON; use `--format srt`, `vtt`, or `webvtt` for subtitles.
`--private` redacts the input URL and deletes transcript segments after 12
hours. `--webhook <url>` supplies the caller's callback; this skill hosts none.
API-key mode supports `--stream`. Wallet mode is asynchronous and also accepts
`--split-channel` and `--user-agent <value>`.

A transcript and its refund have separate outcomes. Failure, confirmed
cancellation, and unused upload expiry receive full refunds; shorter successful
input can receive a partial refund. If the service cannot fetch `--url` after
payment, or a file transfer fails, the result is `FAILED` with a `purchase_id`,
no job ID, and a full refund. An unused upload purchase reports `EXPIRED` the
same way. To try again, start a new purchase with a new `--state` path.
Refunds return to the original payer; a pending refund is not a
completed transfer. Deduplicate x402 webhooks by `X-SiC-Event-ID`. For
duration errors, refund rules, and webhook event formats, see
[Errors](https://docs.speechischeap.com/errors/),
[Payments and Refunds](https://docs.speechischeap.com/x402-v2/payments/),
and [x402 Webhooks](https://docs.speechischeap.com/x402-v2/webhooks/).
