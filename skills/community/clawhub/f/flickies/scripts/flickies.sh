#!/usr/bin/env bash
# Submit a flickies video-producing job async, poll it to a terminal state,
# and download the staged result. Uses only real endpoints:
#   POST /v1/video/<endpoint>   (async_job forced true)
#   GET  /v1/jobs/{job_id}       (poll until complete/failed/cancelled)
#   GET  /v1/files/{path}        (download the auto-staged result)
#
# Usage:
#   flickies.sh <endpoint> <json-body> [output-file]
#
#   <endpoint>     One of the async-capable video ops:
#                    lipsync | restore | trim | concat | transcode | scale | mux_audio
#   <json-body>    The request body as a JSON string. Do NOT set async_job /
#                    output_path / output_url yourself — the script forces
#                    async_job=true and lets the server auto-stage the result
#                    to jobs/{job_id}.{ext}. Anything else in the body
#                    (file_url, engine, start_sec, ...) is passed through.
#   [output-file]  Local path to download the result to. If omitted, the
#                    staged server path is printed and nothing is downloaded.
#
# Environment:
#   FLICKIES_URL          Base URL of the flickies server (default: http://localhost:8000)
#   FLICKIES_AUTH_TOKEN   Optional bearer token (sent on every request if set)
#   FLICKIES_FORMAT       Output container ext for the staged file (default: mp4).
#                           Must match the body's output_format if you set one.
#   FLICKIES_POLL_SECS    Seconds between status polls (default: 3)
#   FLICKIES_TIMEOUT_SECS Give up after this many seconds (default: 1800)
#
# Exit: 0 on job status=complete, 1 on failed/cancelled/timeout, 2 on usage/setup error.

set -euo pipefail

FLICKIES_URL="${FLICKIES_URL:-http://localhost:8000}"
FLICKIES_FORMAT="${FLICKIES_FORMAT:-mp4}"
FLICKIES_POLL_SECS="${FLICKIES_POLL_SECS:-3}"
FLICKIES_TIMEOUT_SECS="${FLICKIES_TIMEOUT_SECS:-1800}"

if [[ $# -lt 2 ]]; then
    echo "usage: $0 <endpoint> <json-body> [output-file]" >&2
    exit 2
fi

endpoint="$1"
body="$2"
out_file="${3:-}"

case "$endpoint" in
    lipsync|restore|trim|concat|transcode|scale|mux_audio) ;;
    *)
        echo "error: unsupported/non-async endpoint: $endpoint" >&2
        echo "       use one of: lipsync restore trim concat transcode scale mux_audio" >&2
        exit 2
        ;;
esac

if ! command -v jq >/dev/null 2>&1; then
    echo "error: jq is required" >&2
    exit 2
fi

auth_args=()
if [[ -n "${FLICKIES_AUTH_TOKEN:-}" ]]; then
    auth_args=(-H "Authorization: Bearer ${FLICKIES_AUTH_TOKEN}")
fi

# Verify the server is reachable before submitting (/healthz is auth-exempt).
if ! curl -sf "$FLICKIES_URL/healthz" >/dev/null; then
    echo "error: $FLICKIES_URL/healthz unreachable — is the container running?" >&2
    exit 2
fi

# Force async_job=true; strip any output_path/output_url so the server
# auto-stages to jobs/{job_id}.{ext}.
submit_body="$(
    echo "$body" | jq -c '. + {async_job: true} | del(.output_path, .output_url)'
)"

submit_resp="$(
    curl -s "${auth_args[@]}" \
        -H "Content-Type: application/json" \
        -X POST "$FLICKIES_URL/v1/video/${endpoint}" \
        -d "$submit_body"
)"

job_id="$(echo "$submit_resp" | jq -r '.job_id // empty')"
if [[ -z "$job_id" ]]; then
    echo "error: submit did not return a job_id:" >&2
    echo "$submit_resp" >&2
    exit 1
fi
echo "[flickies] submitted ${endpoint} → job ${job_id}"

deadline=$(( $(date +%s) + FLICKIES_TIMEOUT_SECS ))
status=""
result=""
while :; do
    poll="$(curl -s "${auth_args[@]}" "$FLICKIES_URL/v1/jobs/${job_id}")"
    status="$(echo "$poll" | jq -r '.status // "unknown"')"

    case "$status" in
        complete)
            result="$(echo "$poll" | jq -c '.result')"
            echo "[flickies] job ${job_id} complete: ${result}"
            break
            ;;
        failed|cancelled)
            echo "[flickies] job ${job_id} ${status}:" >&2
            echo "$poll" | jq -c '.error' >&2
            exit 1
            ;;
        pending|running)
            : # keep polling
            ;;
        *)
            echo "[flickies] unexpected status '${status}':" >&2
            echo "$poll" >&2
            exit 1
            ;;
    esac

    if [[ "$(date +%s)" -ge "$deadline" ]]; then
        echo "[flickies] timed out after ${FLICKIES_TIMEOUT_SECS}s (last status: ${status})" >&2
        exit 1
    fi
    sleep "$FLICKIES_POLL_SECS"
done

# Prefer the path the server reported; fall back to the conventional staged name.
staged_path="$(echo "$result" | jq -r '.path // empty')"
[[ -z "$staged_path" ]] && staged_path="jobs/${job_id}.${FLICKIES_FORMAT}"

if [[ -z "$out_file" ]]; then
    echo "[flickies] staged at: ${staged_path}  (fetch via GET /v1/files/${staged_path})"
    exit 0
fi

http_code="$(
    curl -s -o "$out_file" -w '%{http_code}' \
        "${auth_args[@]}" \
        "$FLICKIES_URL/v1/files/${staged_path}" \
        || echo "000"
)"
if [[ "$http_code" != "200" ]]; then
    echo "[flickies] download failed ($http_code) for ${staged_path}" >&2
    rm -f "$out_file"
    exit 1
fi
echo "[flickies] downloaded → ${out_file}"
