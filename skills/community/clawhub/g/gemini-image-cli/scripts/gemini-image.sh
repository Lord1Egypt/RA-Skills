#!/usr/bin/env bash
set -euo pipefail

VERSION="0.1.0"
DEFAULT_MODEL="gemini-3.1-flash-image-preview"
DEFAULT_LOCAL_ENDPOINT="http://127.0.0.1:8000"
DEFAULT_LOCAL_API_KEY="sk-123456"
DEFAULT_GOOGLE_ENDPOINT="https://generativelanguage.googleapis.com"

usage() {
  cat <<'EOF'
Usage:
  gemini-image [OPTIONS] "PROMPT"
  gemini-image [OPTIONS] --prompt-file FILE

Required:
  PROMPT or --prompt-file FILE   Prompt text. Use exactly one of these.

Options:
  -p, --prompt TEXT              Prompt text. Alternative to positional PROMPT.
      --prompt-file FILE         Read prompt text from FILE.
  -i, --image FILE               Input/reference image. Can be repeated.
  -o, --output FILE              Output image path or prefix.
                                  Default:
                                    ./generated-image-YYYYmmdd-HHMMSS-SIZE-ASPECT.<ext>
                                  Example:
                                    ./generated-image-20260419-000842-512-1x1.png
                                  The final extension is selected from the
                                  returned image MIME type. If FILE has a known
                                  image extension, that extension is replaced
                                  when needed.
      --overwrite                Allow overwriting output files.

Model:
      --model MODEL              Default: gemini-3.1-flash-image-preview
                                  Supported:
                                    gemini-3.1-flash-image-preview
                                    gemini-3-pro-image-preview
                                    gemini-2.5-flash-image

Image output:
      --aspect RATIO             Optional. Supported values depend on --model:
                                  Default: 16:9
                                  gemini-3.1-flash-image-preview:
                                    1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1,
                                    4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
                                  gemini-3-pro-image-preview and gemini-2.5-flash-image:
                                    1:1, 2:3, 3:2, 3:4, 4:3, 4:5,
                                    5:4, 9:16, 16:9, 21:9
      --size SIZE                Optional. Default: smallest supported size for the model.
                                  gemini-3.1-flash-image-preview: 512, 1K, 2K, 4K
                                    default: 512
                                  gemini-3-pro-image-preview: 1K, 2K, 4K
                                    default: 1K
                                  gemini-2.5-flash-image: not supported
      --with-text                Also request and save text output.
                                  Default: false
      --text-output FILE         Text output path. Only used with --with-text.
                                  Default: <output-prefix>.txt

Advanced:
      --provider PROVIDER        Optional. Supported: local, google.
                                  Default: auto-select local, then fallback to google.
      --seed INT                 Optional integer seed.
      --temperature FLOAT        Optional. Range: 0.0 to 2.0.
      --top-p FLOAT              Optional. Passed through to generationConfig.topP.
      --top-k INT                Optional integer. Passed through to generationConfig.topK.
      --candidate-count INT      Optional integer. API default is 1.
      --google-search            Enable Google Search grounding tool.
      --service-tier TIER        Optional. Supported: standard, flex, priority.
      --safety-json FILE         Read safetySettings JSON array from FILE.

Debug:
      --connect-timeout SECONDS  Curl connect timeout. Default: 30
      --max-time SECONDS         Curl total timeout. Default: 0 (disabled)
      --retry INT                Retry failed requests. Default: 0
                                  Note: retries may submit another generation request.
      --retry-delay SECONDS      Delay between retries. Default: 5
      --http1.1                  Force HTTP/1.1 for the API request.
      --dry-run                  Print request JSON and do not call the API.
      --quiet                    Suppress progress logs on stderr.
      --verbose                  Print additional request details to stderr.
  -h, --help                     Show this help.
      --version                  Show version.

Outputs printed to stdout after a successful request:
  image=<path>
  raw_json=<path>
  text=<path>                    Only when --with-text is enabled.
  duration_seconds=<seconds>

Raw response JSON is always saved automatically:
  <output-prefix>.raw.json

Environment:
  GEMINI_LOCAL_ENDPOINT          Local Gemini-compatible proxy base origin.
                                  Default: http://127.0.0.1:8000
  GEMINI_LOCAL_API_KEY           Local proxy API key.
                                  Default: sk-123456
  GEMINI_GOOGLE_ENDPOINT         Google Gemini API base origin.
                                  Default: https://generativelanguage.googleapis.com
  GEMINI_API_KEY                 Required only when using the google provider.

Endpoint selection:
  When --provider is omitted, the script first checks whether
  GEMINI_LOCAL_ENDPOINT is reachable. If it is reachable, the local provider
  is used and GEMINI_API_KEY is not required. If it is unreachable, the script
  falls back to the google provider and requires GEMINI_API_KEY.

  --provider local checks only GEMINI_LOCAL_ENDPOINT and never falls back.
  --provider google uses only GEMINI_GOOGLE_ENDPOINT and GEMINI_API_KEY.

Security:
  Avoid exposing real Google Gemini API keys in untrusted environments. For
  stronger key isolation, use a local Gemini-compatible proxy and keep the real
  key inside that service.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

log() {
  if [[ "$quiet" != "true" ]]; then
    printf '%s\n' "$*" >&2
  fi
}

debug() {
  if [[ "$verbose" == "true" && "$quiet" != "true" ]]; then
    printf '%s\n' "$*" >&2
  fi
}

plain_log() {
  if [[ "$quiet" != "true" ]]; then
    printf '%s\n' "$*" >&2
  fi
}

section() {
  if [[ "$quiet" != "true" ]]; then
    printf '%s\n' "$1" >&2
  fi
}

field() {
  if [[ "$quiet" != "true" ]]; then
    printf '  %s: %s\n' "$1" "$2" >&2
  fi
}

start_progress() {
  local message="$1"
  (
    local frames='|/-\'
    local frame_count=${#frames}
    local tick=0
    local start
    local now
    local elapsed
    start="$(date +%s)"
    while true; do
      now="$(date +%s)"
      elapsed=$((now - start))
      printf '\r%s %s %ss' "${frames:tick % frame_count:1}" "$message" "$elapsed" >&2
      tick=$((tick + 1))
      sleep 0.2
    done
  ) &
  progress_pid="$!"
}

stop_progress() {
  if [[ -n "${progress_pid:-}" ]]; then
    kill "$progress_pid" 2>/dev/null || true
    wait "$progress_pid" 2>/dev/null || true
    progress_pid=""
    printf '\r\033[K' >&2
  fi
}

mask_secret() {
  local secret="$1"
  local length=${#secret}
  if [[ "$length" -le 12 ]]; then
    printf '%s\n' '********'
    return
  fi
  local prefix="${secret:0:6}"
  local suffix="${secret:length-6:6}"
  local stars_count=$((length - 12))
  local stars
  stars="$(printf '%*s' "$stars_count" '' | tr ' ' '*')"
  printf '%s%s%s\n' "$prefix" "$stars" "$suffix"
}

shell_quote() {
  printf "%q" "$1"
}

single_quote() {
  printf "'%s'" "${1//\'/\'\\\'\'}"
}

aspect_label() {
  printf '%s\n' "${1/:/x}"
}

print_curl_command() {
  local masked_key="$1"
  local body="$2"
  local pretty_body
  pretty_body="$(jq . <<<"$body")"

  section "Curl"
  printf '```bash\n' >&2
  printf '  curl -sS \\\n' >&2
  printf '    --connect-timeout %s \\\n' "$connect_timeout" >&2
  if [[ "$max_time" != "0" ]]; then
    printf '    --max-time %s \\\n' "$max_time" >&2
  fi
  if [[ "$force_http1" == "true" ]]; then
    printf '    --http1.1 \\\n' >&2
  fi
  printf '    -w ' >&2
  single_quote '%{http_code}' >&2
  printf ' \\\n' >&2
  printf '    -o ' >&2
  single_quote "$raw_json" >&2
  printf ' \\\n' >&2
  printf '    -X POST ' >&2
  single_quote "$url" >&2
  printf ' \\\n' >&2
  printf '    -H ' >&2
  single_quote "x-goog-api-key: $masked_key" >&2
  printf ' \\\n' >&2
  printf '    -H ' >&2
  single_quote "Content-Type: application/json" >&2
  printf ' \\\n' >&2
  printf '    -d @- <<'\''JSON'\''\n' >&2
  printf '%s\n' "$pretty_body" >&2
  printf 'JSON\n' >&2
  printf '```\n' >&2
}

cleanup() {
  stop_progress
  if ((${#temp_files[@]} > 0)); then
    rm -f "${temp_files[@]}" 2>/dev/null || true
  fi
}

interrupt() {
  cleanup
  printf '\nInterrupted\n' >&2
  exit 130
}

is_retryable_http() {
  case "$1" in
    408|409|425|429|500|502|503|504) return 0 ;;
    *) return 1 ;;
  esac
}

is_retryable_curl_status() {
  case "$1" in
    18|28|35|52|55|56|92) return 0 ;;
    *) return 1 ;;
  esac
}

normalize_base_endpoint() {
  local value="$1"
  value="${value%/}"
  value="${value%/v1beta}"
  printf '%s\n' "$value"
}

health_check_endpoint() {
  local endpoint="$1"
  curl -sS \
    --connect-timeout 1 \
    --max-time 2 \
    -o /dev/null \
    "$endpoint" >/dev/null 2>&1
}

print_no_endpoint_error() {
  local local_endpoint="$1"
  local local_status="$2"
  printf 'error: no usable Gemini endpoint\n' >&2
  printf 'local: %s is %s\n' "$local_endpoint" "$local_status" >&2
  printf 'google: GEMINI_API_KEY is not set\n' >&2
  printf '\nConfigure one of:\n' >&2
  printf '  GEMINI_LOCAL_ENDPOINT=http://127.0.0.1:8000\n' >&2
  printf '  GEMINI_LOCAL_API_KEY=sk-123456\n' >&2
  printf '\n  or\n\n' >&2
  printf '  GEMINI_API_KEY=<google-gemini-api-key>\n' >&2
  printf '\nAvoid exposing real Google Gemini API keys in untrusted environments.\n' >&2
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"
}

read_file() {
  local file="$1"
  [[ -f "$file" ]] || die "file not found: $file"
  jq -Rs . < "$file"
}

base64_one_line() {
  local file="$1"
  if base64 --help 2>/dev/null | grep -q -- '-w'; then
    base64 -w 0 "$file"
  else
    base64 "$file" | tr -d '\n'
  fi
}

mime_for_file() {
  local file="$1"
  local detected=""
  if command -v file >/dev/null 2>&1; then
    detected="$(file --mime-type -b "$file" 2>/dev/null || true)"
  fi

  if [[ -n "$detected" && "$detected" == image/* ]]; then
    printf '%s\n' "$detected"
    return
  fi

  case "${file,,}" in
    *.png) printf 'image/png\n' ;;
    *.jpg|*.jpeg) printf 'image/jpeg\n' ;;
    *.webp) printf 'image/webp\n' ;;
    *.heic) printf 'image/heic\n' ;;
    *.heif) printf 'image/heif\n' ;;
    *) die "cannot determine MIME type for $file; use --image-mime FILE:MIME" ;;
  esac
}

extension_for_mime() {
  case "$1" in
    image/png) printf 'png\n' ;;
    image/jpeg) printf 'jpg\n' ;;
    image/webp) printf 'webp\n' ;;
    *) return 1 ;;
  esac
}

strip_known_image_extension() {
  local path="$1"
  case "${path,,}" in
    *.png|*.jpg|*.jpeg|*.webp|*.heic|*.heif)
      printf '%s\n' "${path%.*}"
      ;;
    *)
      printf '%s\n' "$path"
      ;;
  esac
}

is_supported_model() {
  case "$1" in
    gemini-3.1-flash-image-preview|gemini-3-pro-image-preview|gemini-2.5-flash-image) return 0 ;;
    *) return 1 ;;
  esac
}

supported_aspects_for_model() {
  case "$1" in
    gemini-3.1-flash-image-preview)
      printf '%s\n' '1:1 1:4 1:8 2:3 3:2 3:4 4:1 4:3 4:5 5:4 8:1 9:16 16:9 21:9'
      ;;
    gemini-3-pro-image-preview|gemini-2.5-flash-image)
      printf '%s\n' '1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9'
      ;;
  esac
}

is_in_words() {
  local needle="$1"
  local words="$2"
  local word
  for word in $words; do
    [[ "$word" == "$needle" ]] && return 0
  done
  return 1
}

supported_sizes_for_model() {
  case "$1" in
    gemini-3.1-flash-image-preview) printf '%s\n' '512 1K 2K 4K' ;;
    gemini-3-pro-image-preview) printf '%s\n' '1K 2K 4K' ;;
    gemini-2.5-flash-image) printf '%s\n' '' ;;
  esac
}

default_size_for_model() {
  case "$1" in
    gemini-3.1-flash-image-preview) printf '%s\n' '512' ;;
    gemini-3-pro-image-preview) printf '%s\n' '1K' ;;
    gemini-2.5-flash-image) printf '%s\n' '' ;;
  esac
}

validate_int() {
  [[ "$2" =~ ^-?[0-9]+$ ]] || die "$1 must be an integer"
}

validate_positive_int() {
  [[ "$2" =~ ^[0-9]+$ && "$2" -gt 0 ]] || die "$1 must be a positive integer"
}

validate_float() {
  [[ "$2" =~ ^[0-9]+([.][0-9]+)?$ ]] || die "$1 must be a number"
}

prompt=""
prompt_file=""
model="$DEFAULT_MODEL"
output=""
overwrite="false"
aspect=""
size=""
provider_override=""
provider=""
fallback_reason=""
endpoint=""
api_key=""
with_text="false"
text_output=""
seed=""
temperature=""
top_p=""
top_k=""
candidate_count=""
google_search="false"
service_tier=""
safety_json_file=""
dry_run="false"
verbose="false"
quiet="false"
connect_timeout="30"
max_time="0"
retry_count="0"
retry_delay="5"
force_http1="false"
system_text=""
system_file=""
progress_pid=""
declare -a temp_files=()
declare -a images=()
declare -a image_mime_overrides=()

trap cleanup EXIT
trap interrupt INT TERM

while (($#)); do
  case "$1" in
    -p|--prompt)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      [[ -z "$prompt" ]] || die "prompt specified more than once"
      prompt="$2"
      shift 2
      ;;
    --prompt-file)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      prompt_file="$2"
      shift 2
      ;;
    -i|--image)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      images+=("$2")
      shift 2
      ;;
    --mime)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      image_mime_overrides+=("*:$2")
      shift 2
      ;;
    --image-mime)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      image_mime_overrides+=("$2")
      shift 2
      ;;
    -o|--output)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      output="$2"
      shift 2
      ;;
    --overwrite)
      overwrite="true"
      shift
      ;;
    --model)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      model="$2"
      shift 2
      ;;
    --provider)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      provider_override="$2"
      shift 2
      ;;
    --aspect)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      aspect="$2"
      shift 2
      ;;
    --size)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      size="$2"
      shift 2
      ;;
    --with-text)
      with_text="true"
      shift
      ;;
    --text-output)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      text_output="$2"
      shift 2
      ;;
    --seed)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      seed="$2"
      shift 2
      ;;
    --temperature)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      temperature="$2"
      shift 2
      ;;
    --top-p)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      top_p="$2"
      shift 2
      ;;
    --top-k)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      top_k="$2"
      shift 2
      ;;
    --candidate-count)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      candidate_count="$2"
      shift 2
      ;;
    --google-search)
      google_search="true"
      shift
      ;;
    --service-tier)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      service_tier="$2"
      shift 2
      ;;
    --safety-json)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      safety_json_file="$2"
      shift 2
      ;;
    --dry-run)
      dry_run="true"
      shift
      ;;
    --connect-timeout)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      connect_timeout="$2"
      shift 2
      ;;
    --max-time)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      max_time="$2"
      shift 2
      ;;
    --retry)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      retry_count="$2"
      shift 2
      ;;
    --retry-delay)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      retry_delay="$2"
      shift 2
      ;;
    --http1.1)
      force_http1="true"
      shift
      ;;
    --verbose)
      verbose="true"
      shift
      ;;
    --quiet)
      quiet="true"
      shift
      ;;
    --system)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      system_text="$2"
      shift 2
      ;;
    --system-file)
      [[ $# -ge 2 ]] || die "$1 requires a value"
      system_file="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --version)
      printf '%s\n' "$VERSION"
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      die "unknown option: $1"
      ;;
    *)
      [[ -z "$prompt" ]] || die "prompt specified more than once"
      prompt="$1"
      shift
      ;;
  esac
done

if (($#)); then
  [[ -z "$prompt" ]] || die "prompt specified more than once"
  prompt="$*"
fi

need_cmd curl
need_cmd jq
need_cmd base64

is_supported_model "$model" || die "unsupported model: $model"

[[ -z "$prompt_file" || -z "$prompt" ]] || die "use PROMPT/--prompt or --prompt-file, not both"
if [[ -n "$prompt_file" ]]; then
  [[ -f "$prompt_file" ]] || die "prompt file not found: $prompt_file"
  prompt="$(<"$prompt_file")"
fi
[[ -n "$prompt" ]] || die "missing prompt; provide PROMPT or --prompt-file FILE"

if [[ -n "$system_file" ]]; then
  [[ -z "$system_text" ]] || die "use --system or --system-file, not both"
  [[ -f "$system_file" ]] || die "system file not found: $system_file"
  system_text="$(<"$system_file")"
fi

case "$provider_override" in
  ""|local|google) ;;
  *) die "--provider must be one of: local, google" ;;
esac

if [[ -z "$aspect" ]]; then
  aspect="16:9"
fi

supported_aspects="$(supported_aspects_for_model "$model")"
is_in_words "$aspect" "$supported_aspects" || die "--aspect $aspect is not supported by $model; supported: $supported_aspects"

if [[ -n "$size" ]]; then
  supported_sizes="$(supported_sizes_for_model "$model")"
  [[ -n "$supported_sizes" ]] || die "--size is not supported by $model"
  is_in_words "$size" "$supported_sizes" || die "--size $size is not supported by $model; supported: $supported_sizes"
fi

if [[ -z "$size" ]]; then
  size="$(default_size_for_model "$model")"
fi

timestamp="$(date '+%Y%m%d-%H%M%S')"
size_label="${size:-fixed}"
aspect_file_label="$(aspect_label "$aspect")"
if [[ -n "$output" ]]; then
  prefix="$(strip_known_image_extension "$output")"
else
  prefix="./generated-image-$timestamp-$size_label-$aspect_file_label"
fi
raw_json="$prefix.raw.json"
if [[ "$with_text" == "true" && -z "$text_output" ]]; then
  text_output="$prefix.txt"
fi

if [[ -n "$text_output" && "$with_text" != "true" ]]; then
  die "--text-output requires --with-text"
fi

[[ -z "$seed" ]] || validate_int "--seed" "$seed"
if [[ -n "$temperature" ]]; then
  validate_float "--temperature" "$temperature"
  awk -v t="$temperature" 'BEGIN { exit !(t >= 0.0 && t <= 2.0) }' || die "--temperature must be between 0.0 and 2.0"
fi
[[ -z "$top_p" ]] || validate_float "--top-p" "$top_p"
[[ -z "$top_k" ]] || validate_positive_int "--top-k" "$top_k"
[[ -z "$candidate_count" ]] || validate_positive_int "--candidate-count" "$candidate_count"
validate_positive_int "--connect-timeout" "$connect_timeout"
[[ "$max_time" =~ ^[0-9]+$ ]] || die "--max-time must be a non-negative integer"
validate_positive_int "--retry-delay" "$retry_delay"
[[ "$retry_count" =~ ^[0-9]+$ ]] || die "--retry must be a non-negative integer"

case "$service_tier" in
  ""|standard|flex|priority) ;;
  *) die "--service-tier must be one of: standard, flex, priority" ;;
esac

for image in "${images[@]}"; do
  [[ -f "$image" ]] || die "image file not found: $image"
done

if [[ "$model" == "gemini-2.5-flash-image" && "${#images[@]}" -gt 3 ]]; then
  die "$model supports this CLI's image input limit of 3 files"
fi
if [[ "$model" != "gemini-2.5-flash-image" && "${#images[@]}" -gt 5 ]]; then
  die "$model supports this CLI's image input limit of 5 files"
fi

if [[ -f "$raw_json" && "$overwrite" != "true" ]]; then
  die "raw JSON file already exists: $raw_json; use --overwrite"
fi
if [[ "$with_text" == "true" && -f "$text_output" && "$overwrite" != "true" ]]; then
  die "text output file already exists: $text_output; use --overwrite"
fi

mkdir -p "$(dirname "$prefix")"
mkdir -p "$(dirname "$raw_json")"
if [[ "$with_text" == "true" ]]; then
  mkdir -p "$(dirname "$text_output")"
fi

if [[ "$provider_override" == "google" ]]; then
  provider="google"
  endpoint="$(normalize_base_endpoint "${GEMINI_GOOGLE_ENDPOINT:-$DEFAULT_GOOGLE_ENDPOINT}")"
  if [[ "$dry_run" != "true" ]]; then
    [[ -n "${GEMINI_API_KEY:-}" ]] || die "GEMINI_API_KEY is required when using --provider google"
    api_key="$GEMINI_API_KEY"
  fi
elif [[ "$provider_override" == "local" ]]; then
  provider="local"
  endpoint="$(normalize_base_endpoint "${GEMINI_LOCAL_ENDPOINT:-$DEFAULT_LOCAL_ENDPOINT}")"
  api_key="${GEMINI_LOCAL_API_KEY:-$DEFAULT_LOCAL_API_KEY}"
  if [[ "$dry_run" != "true" ]] && ! health_check_endpoint "$endpoint"; then
    die "local endpoint is unreachable: $endpoint"
  fi
else
  local_endpoint="$(normalize_base_endpoint "${GEMINI_LOCAL_ENDPOINT:-$DEFAULT_LOCAL_ENDPOINT}")"
  if [[ "$dry_run" == "true" ]]; then
    provider="auto"
    endpoint="$local_endpoint"
    api_key="${GEMINI_LOCAL_API_KEY:-$DEFAULT_LOCAL_API_KEY}"
  elif health_check_endpoint "$local_endpoint"; then
    provider="local"
    endpoint="$local_endpoint"
    api_key="${GEMINI_LOCAL_API_KEY:-$DEFAULT_LOCAL_API_KEY}"
  else
    provider="google"
    fallback_reason="local endpoint unreachable: $local_endpoint"
    endpoint="$(normalize_base_endpoint "${GEMINI_GOOGLE_ENDPOINT:-$DEFAULT_GOOGLE_ENDPOINT}")"
    if [[ -z "${GEMINI_API_KEY:-}" ]]; then
      print_no_endpoint_error "$local_endpoint" "unreachable"
      exit 1
    fi
    api_key="$GEMINI_API_KEY"
  fi
fi

parts_file="$(mktemp)"
temp_files+=("$parts_file")
jq -n --arg text "$prompt" '[{text: $text}]' > "$parts_file"

mime_override_for() {
  local file="$1"
  local entry key value global=""
  for entry in "${image_mime_overrides[@]}"; do
    key="${entry%%:*}"
    value="${entry#*:}"
    if [[ "$key" == "*" ]]; then
      global="$value"
    elif [[ "$key" == "$file" ]]; then
      printf '%s\n' "$value"
      return
    fi
  done
  if [[ -n "$global" ]]; then
    printf '%s\n' "$global"
  fi
}

for image in "${images[@]}"; do
  mime="$(mime_override_for "$image")"
  if [[ -z "$mime" ]]; then
    mime="$(mime_for_file "$image")"
  fi
  case "$mime" in
    image/png|image/jpeg|image/webp|image/heic|image/heif) ;;
    *) die "unsupported MIME for $image: $mime" ;;
  esac
  data_file="$(mktemp)"
  part_file="$(mktemp)"
  next_parts_file="$(mktemp)"
  temp_files+=("$data_file" "$part_file" "$next_parts_file")
  base64_one_line "$image" > "$data_file"
  jq -n --arg mime "$mime" --rawfile data "$data_file" \
    '{inlineData: {mimeType: $mime, data: $data}}' > "$part_file"
  jq --slurpfile part "$part_file" '. + [$part[0]]' "$parts_file" > "$next_parts_file"
  parts_file="$next_parts_file"
done

section "Request"
field "provider" "$provider"
field "endpoint" "$endpoint"
if [[ -n "$fallback_reason" ]]; then
  field "fallback" "$fallback_reason"
fi
field "model" "$model"
field "size" "${size:-fixed}"
field "aspect" "$aspect"
field "output prefix" "$prefix"
field "raw" "$raw_json"
if [[ "$with_text" == "true" ]]; then
  field "text" "$text_output"
fi
if [[ "${#images[@]}" -gt 0 ]]; then
  field "input images" "${#images[@]}"
fi
debug "connect timeout: ${connect_timeout}s"
debug "max time: ${max_time}s"
debug "retry count: $retry_count"
debug "force http1: $force_http1"

response_modalities='["IMAGE"]'
if [[ "$with_text" == "true" ]]; then
  response_modalities='["TEXT","IMAGE"]'
fi

request_json="$(jq -n \
  --slurpfile parts "$parts_file" \
  --argjson responseModalities "$response_modalities" \
  --arg aspect "$aspect" \
  --arg size "$size" \
  --arg seed "$seed" \
  --arg temperature "$temperature" \
  --arg topP "$top_p" \
  --arg topK "$top_k" \
  --arg candidateCount "$candidate_count" \
  --arg serviceTier "$service_tier" \
  --arg systemText "$system_text" \
  --arg safetyJsonFile "$safety_json_file" \
  --argjson googleSearchEnabled "$google_search" '
  {
    contents: [{parts: $parts[0]}],
    generationConfig: {
      responseModalities: $responseModalities
    }
  }
  | if $aspect != "" then .generationConfig.imageConfig.aspectRatio = $aspect else . end
  | if $size != "" then .generationConfig.imageConfig.imageSize = $size else . end
  | if $seed != "" then .generationConfig.seed = ($seed | tonumber) else . end
  | if $temperature != "" then .generationConfig.temperature = ($temperature | tonumber) else . end
  | if $topP != "" then .generationConfig.topP = ($topP | tonumber) else . end
  | if $topK != "" then .generationConfig.topK = ($topK | tonumber) else . end
  | if $candidateCount != "" then .generationConfig.candidateCount = ($candidateCount | tonumber) else . end
  | if $serviceTier != "" then .generationConfig.serviceTier = $serviceTier else . end
  | if $systemText != "" then .systemInstruction = {parts: [{text: $systemText}]} else . end
  | if $googleSearchEnabled then .tools = [{googleSearch: {}}] else . end
  ')"

if [[ -n "$safety_json_file" ]]; then
  [[ -f "$safety_json_file" ]] || die "safety JSON file not found: $safety_json_file"
  jq -e 'type == "array"' "$safety_json_file" >/dev/null || die "--safety-json must contain a JSON array"
  request_json="$(jq --slurpfile safety "$safety_json_file" '.safetySettings = $safety[0]' <<<"$request_json")"
fi

if [[ "$dry_run" == "true" ]]; then
  jq . <<<"$request_json"
  exit 0
fi

request_file="$(mktemp)"
temp_files+=("$request_file")
printf '%s' "$request_json" > "$request_file"

url="$endpoint/v1beta/models/$model:generateContent"
start_ns="$(date +%s%N)"
debug "POST $url"
if [[ "$quiet" != "true" ]]; then
  redacted_request_json="$(jq -c '(.contents[]?.parts[]? | select(has("inlineData") and (.inlineData | has("data"))).inlineData.data) = "<base64:redacted>"' <<<"$request_json")"
  print_curl_command "$(mask_secret "$api_key")" "$redacted_request_json"
fi
section "Generating"

attempt=1
max_attempts=$((retry_count + 1))
curl_status=0
http_code="000"
while true; do
  if [[ "$max_attempts" -gt 1 ]]; then
    field "attempt" "$attempt/$max_attempts"
  fi

  curl_args=(
    -sS
    --connect-timeout "$connect_timeout"
    -w '%{http_code}'
    -o "$raw_json"
    -X POST "$url"
    -H "x-goog-api-key: ${api_key}"
    -H "Content-Type: application/json"
    --data-binary "@$request_file"
  )
  if [[ "$max_time" != "0" ]]; then
    curl_args=(--max-time "$max_time" "${curl_args[@]}")
  fi
  if [[ "$force_http1" == "true" ]]; then
    curl_args=(--http1.1 "${curl_args[@]}")
  fi

  if [[ "$quiet" != "true" && -t 2 ]]; then
    start_progress "waiting for response"
  fi
  set +e
  http_code="$(curl "${curl_args[@]}")"
  curl_status=$?
  set -e
  stop_progress

  if [[ "$curl_status" -eq 0 && "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
    break
  fi

  retryable="false"
  if [[ "$curl_status" -ne 0 ]]; then
    if is_retryable_curl_status "$curl_status"; then
      retryable="true"
    fi
    field "curl error" "exit code $curl_status"
  else
    if is_retryable_http "$http_code"; then
      retryable="true"
    fi
    field "http" "$http_code"
  fi

  if [[ "$retryable" == "true" && "$attempt" -lt "$max_attempts" ]]; then
    field "retrying in" "${retry_delay}s"
    sleep "$retry_delay"
    attempt=$((attempt + 1))
    continue
  fi

  break
done

end_ns="$(date +%s%N)"
duration_seconds="$(awk -v start="$start_ns" -v end="$end_ns" 'BEGIN { printf "%.3f", (end - start) / 1000000000 }')"

if [[ "$curl_status" -ne 0 ]]; then
  printf 'error: curl failed with exit code %s\n' "$curl_status" >&2
  case "$curl_status" in
    28) printf 'hint: request timed out; try --max-time 0 or a larger --max-time value\n' >&2 ;;
    56) printf 'hint: connection closed while receiving data; try --retry 1 or --http1.1\n' >&2 ;;
    92) printf 'hint: HTTP/2 stream error; try --http1.1\n' >&2 ;;
  esac
  printf 'raw_json=%s\n' "$raw_json" >&2
  exit "$curl_status"
fi

field "response" "${duration_seconds}s"

if [[ "$http_code" -lt 200 || "$http_code" -ge 300 ]]; then
  printf 'error: API request failed with HTTP %s\n' "$http_code" >&2
  printf 'raw_json=%s\n' "$raw_json" >&2
  jq -r '.error.message? // empty' "$raw_json" >&2 || true
  exit 1
fi

image_count="$(jq '[.candidates[]?.content.parts[]? | select(.inlineData.data)] | length' "$raw_json")"
[[ "$image_count" -gt 0 ]] || die "API response contained no image data; raw_json=$raw_json"
field "images" "$image_count"

declare -a image_outputs=()
index=0
while IFS=$'\t' read -r mime data; do
  index=$((index + 1))
  ext="$(extension_for_mime "$mime")" || die "unsupported output MIME type: $mime"
  if [[ "$image_count" -eq 1 ]]; then
    image_output="$prefix.$ext"
  else
    image_output="$prefix-$index.$ext"
  fi
  if [[ -f "$image_output" && "$overwrite" != "true" ]]; then
    die "output file already exists: $image_output; use --overwrite"
  fi
  printf '%s' "$data" | base64 --decode > "$image_output"
  image_outputs+=("$image_output")
done < <(jq -r '.candidates[]?.content.parts[]? | select(.inlineData.data) | [.inlineData.mimeType, .inlineData.data] | @tsv' "$raw_json")

if [[ "$with_text" == "true" ]]; then
  jq -r '[.candidates[]?.content.parts[]? | select(.text) | .text] | join("\n")' "$raw_json" > "$text_output"
  field "saved text" "$text_output"
fi
section "Done"
field "duration" "${duration_seconds}s"

for image_output in "${image_outputs[@]}"; do
  printf 'image=%s\n' "$image_output"
done
printf 'raw_json=%s\n' "$raw_json"
if [[ "$with_text" == "true" ]]; then
  printf 'text=%s\n' "$text_output"
fi
printf 'duration_seconds=%s\n' "$duration_seconds"
