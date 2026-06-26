#!/bin/bash
# Universal video transcription tool with native subtitle detection
# Supports: Bilibili, YouTube, Xiaohongshu, Douyin, and local files
#
# Usage:
#   bash video_transcribe.sh <url_or_file> [options]
#   bash video_transcribe.sh --step download <url>
#   bash video_transcribe.sh --step transcribe <audio_file>
#
# Options:
#   --platform <name>    Force platform: bilibili, youtube, xiaohongshu, douyin, auto (default: auto)
#   --step <action>      Run specific step: download, transcribe (default: both)
#   --model <size>       Whisper model: tiny, base (default), small, medium, large-v3
#   --force              Force transcription even if cached result exists
#   --help               Show this help message
#
# Two-step workflow:
#   1. Download: bash video_transcribe.sh --step download <url>
#      Output: JSON with audio_file path
#   2. Transcribe: bash video_transcribe.sh --step transcribe <audio_file>
#      Output: JSON with transcript paths and stats
#
# Full workflow (default):
#   bash video_transcribe.sh <url> [--model base]
#   Output: Combined JSON with download + transcribe results
#
# Transcription priority:
#   1. Native CC/subtitles (Bilibili/YouTube only)
#   2. Volcengine ASR (if VOLC_ASR_APPID and VOLC_ASR_TOKEN are set)
#   3. Local Whisper (fallback)
#   - Output includes subtitle_source: "native_cc", "volc_asr", or "whisper"

set -e

# Default settings
PLATFORM="auto"
STEP="full"
MODEL="base"
FORCE_TRANSCRIBE="false"
OUTDIR="/tmp/video_audio"
mkdir -p "$OUTDIR"

# Parse arguments
show_help() {
    head -n 30 "$0" | grep '^#' | sed 's/^# //; s/^#//'
    exit 0
}

INPUT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            ;;
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --step)
            STEP="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --force)
            FORCE_TRANSCRIBE="true"
            shift
            ;;
        *)
            if [ -z "$INPUT" ]; then
                INPUT="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$INPUT" ]; then
    echo "Error: No input provided (URL or file path)" >&2
    show_help
fi

# ============================================================================
# Platform detection
# ============================================================================

detect_platform() {
    local input="$1"

    # Local file
    if [ -f "$input" ]; then
        echo "local"
        return
    fi

    # URL pattern matching
    case "$input" in
        *bilibili.com*|*b23.tv*)
            echo "bilibili"
            ;;
        *youtube.com*|*youtu.be*)
            echo "youtube"
            ;;
        *xiaohongshu.com*|*xhslink.com*)
            echo "xiaohongshu"
            ;;
        *douyin.com*|*v.douyin.com*)
            echo "douyin"
            ;;
        *)
            echo "Error: Cannot detect platform from: $input" >&2
            echo "Please specify --platform manually" >&2
            exit 1
            ;;
    esac
}

# Auto-detect platform if needed
if [ "$PLATFORM" = "auto" ]; then
    PLATFORM=$(detect_platform "$INPUT")
fi

echo "Platform: $PLATFORM" >&2

# ============================================================================
# ID extraction
# ============================================================================

extract_video_id() {
    local platform="$1"
    local input="$2"

    case "$platform" in
        bilibili)
            # Extract BVID
            local bvid=$(echo "$input" | grep -oE 'BV[a-zA-Z0-9]+' | head -1)
            if [ -z "$bvid" ]; then
                echo "Error: Cannot extract BVID from: $input" >&2
                exit 1
            fi
            echo "$bvid"
            ;;
        youtube)
            # Extract video ID
            local vid=$(echo "$input" | grep -oP '(?<=v=)[^&]+' || echo "$input" | grep -oP '(?<=youtu.be/)[^?]+')
            if [ -z "$vid" ]; then
                # Fallback: use URL hash
                echo "yt_$(echo "$input" | md5sum | cut -c1-8)"
            else
                echo "$vid"
            fi
            ;;
        xiaohongshu|douyin)
            # Use URL hash for ID
            echo "${platform}_$(echo "$input" | md5sum | cut -c1-8)"
            ;;
        local)
            # Use filename without extension
            basename "$input" | sed 's/\.[^.]*$//'
            ;;
        *)
            echo "unknown_$(echo "$input" | md5sum | cut -c1-8)"
            ;;
    esac
}

# ============================================================================
# Native subtitle detection
# ============================================================================

detect_and_download_native_subtitle() {
    local platform="$1"
    local url="$2"
    local output_file="$3"

    # Only for Bilibili and YouTube
    if [ "$platform" != "bilibili" ] && [ "$platform" != "youtube" ]; then
        return 1
    fi

    echo "Checking for native subtitles..." >&2

    # Build yt-dlp command for subtitle detection
    local ytdlp_cmd="yt-dlp --list-subs"
    if [ "$platform" = "bilibili" ]; then
        ytdlp_cmd="$ytdlp_cmd --cookies-from-browser chrome"
    fi

    # List available subtitles
    local sub_list=$($ytdlp_cmd "$url" 2>/dev/null || true)

    # Check for Chinese/AI subtitles
    local sub_lang=""
    if echo "$sub_list" | grep -qE '(zh-Hans|zh-CN|ai-zh|zh)'; then
        # Priority: ai-zh > zh-CN > zh-Hans > zh
        if echo "$sub_list" | grep -q 'ai-zh'; then
            sub_lang="ai-zh"
        elif echo "$sub_list" | grep -q 'zh-CN'; then
            sub_lang="zh-CN"
        elif echo "$sub_list" | grep -q 'zh-Hans'; then
            sub_lang="zh-Hans"
        elif echo "$sub_list" | grep -q 'zh'; then
            sub_lang="zh"
        fi
    fi

    if [ -z "$sub_lang" ]; then
        echo "No native Chinese subtitles found" >&2
        return 1
    fi

    echo "Found native subtitle: $sub_lang" >&2

    # Download subtitle
    local temp_base="$OUTDIR/subtitle_temp"
    local download_cmd="yt-dlp --write-sub --sub-lang $sub_lang --skip-download -o $temp_base"
    if [ "$platform" = "bilibili" ]; then
        download_cmd="$download_cmd --cookies-from-browser chrome"
    fi

    $download_cmd "$url" 2>&1 | grep -E '(Downloading|Writing|Error)' >&2 || true

    # Find downloaded subtitle file (VTT or SRT)
    local sub_file=""
    if [ -f "${temp_base}.${sub_lang}.vtt" ]; then
        sub_file="${temp_base}.${sub_lang}.vtt"
    elif [ -f "${temp_base}.${sub_lang}.srt" ]; then
        sub_file="${temp_base}.${sub_lang}.srt"
    else
        echo "Warning: Subtitle download failed" >&2
        return 1
    fi

    # Convert to plain text (remove timestamps and formatting)
    echo "Converting subtitle to plain text..." >&2
    python3 - "$sub_file" "$output_file" << 'PYEOF'
import sys
import re

sub_file = sys.argv[1]
output_file = sys.argv[2]

with open(sub_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove VTT header
if content.startswith('WEBVTT'):
    content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.DOTALL)

# Remove timestamps and sequence numbers
lines = []
for line in content.split('\n'):
    line = line.strip()
    # Skip empty, numeric-only, and timestamp lines
    if not line or line.isdigit() or '-->' in line:
        continue
    # Skip VTT formatting tags
    if line.startswith('<') and line.endswith('>'):
        continue
    # Remove inline formatting tags
    line = re.sub(r'<[^>]+>', '', line)
    if line:
        lines.append(line)

# Join and deduplicate consecutive lines
text = ' '.join(lines)
# Remove extra spaces
text = re.sub(r'\s+', ' ', text).strip()

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Converted {len(lines)} subtitle lines to plain text", file=sys.stderr)
PYEOF

    # Cleanup temp files
    rm -f "${temp_base}."*

    return 0
}

# ============================================================================
# Download step
# ============================================================================

download_audio() {
    local platform="$1"
    local url="$2"
    local video_id="$3"

    local audio_file="$OUTDIR/${platform}_${video_id}.mp3"
    local subtitle_file="$OUTDIR/${platform}_${video_id}_subtitle.txt"
    local subtitle_source="none"

    # Check if already exists
    if [ -f "$audio_file" ]; then
        echo "Audio already exists: $audio_file" >&2
    else
        # Try native subtitle first for Bilibili/YouTube
        if [ "$platform" = "bilibili" ] || [ "$platform" = "youtube" ]; then
            if detect_and_download_native_subtitle "$platform" "$url" "$subtitle_file"; then
                subtitle_source="native_cc"
                echo "Native subtitle extracted successfully" >&2
                # No need to download audio
                audio_file=""
            fi
        fi

        # If no native subtitle, download audio for Whisper
        if [ "$subtitle_source" = "none" ]; then
            echo "Downloading audio for $platform ($video_id)..." >&2

            # Build yt-dlp command based on platform
            local ytdlp_cmd="yt-dlp -x --audio-format mp3 --audio-quality 5 -o $OUTDIR/${platform}_${video_id}.%(ext)s --no-playlist"

            case "$platform" in
                bilibili)
                    ytdlp_cmd="$ytdlp_cmd --cookies-from-browser chrome"
                    ;;
                youtube)
                    # No special options needed
                    ;;
                xiaohongshu|douyin)
                    # Try with cookie first
                    ytdlp_cmd="$ytdlp_cmd --cookies-from-browser chrome"
                    ;;
            esac

            $ytdlp_cmd "$url" 2>&1 | grep -E '(Downloading|download|Destination|Deleting|Error)' >&2 || {
                # Retry without cookie for xiaohongshu/douyin
                if [ "$platform" = "xiaohongshu" ] || [ "$platform" = "douyin" ]; then
                    echo "Retrying without cookies..." >&2
                    yt-dlp -x --audio-format mp3 --audio-quality 5 -o "$OUTDIR/${platform}_${video_id}.%(ext)s" --no-playlist "$url" 2>&1 | grep -E '(Downloading|download|Destination|Deleting|Error)' >&2
                else
                    exit 1
                fi
            }

            echo "Audio downloaded: $audio_file" >&2
        fi
    fi

    # Output JSON
    if [ "$subtitle_source" = "native_cc" ]; then
        jq -n --arg subtitle "$subtitle_file" --arg platform "$platform" --arg vid "$video_id" --arg source "$subtitle_source" \
            '{subtitle_file: $subtitle, platform: $platform, video_id: $vid, subtitle_source: $source}'
    else
        jq -n --arg audio "$audio_file" --arg platform "$platform" --arg vid "$video_id" \
            '{audio_file: $audio, platform: $platform, video_id: $vid}'
    fi
}

# ============================================================================
# Transcribe step
# ============================================================================

check_existing_transcript() {
    local base_name="$1"

    # Check for any existing transcript file
    local cached_files=(
        "$OUTDIR/${base_name}_transcript.txt"
        "$OUTDIR/${base_name}_merged.txt"
        "$OUTDIR/${base_name}_subtitle.txt"
    )

    for cached in "${cached_files[@]}"; do
        if [ -f "$cached" ]; then
            echo "$cached"
            return 0
        fi
    done

    return 1
}

transcribe_with_volc_asr() {
    local audio_file="$1"
    local base_name="$2"
    local transcript_json="$3"
    local transcript_txt="$4"

    # Check credentials
    if [ -z "$VOLC_ASR_APPID" ] || [ -z "$VOLC_ASR_TOKEN" ]; then
        return 1
    fi

    echo "Transcribing with Volcengine ASR..." >&2

    # Get script directory
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local volc_script="$script_dir/volc_asr.py"

    if [ ! -f "$volc_script" ]; then
        echo "Warning: volc_asr.py not found, falling back to whisper" >&2
        return 1
    fi

    # Call Volcengine ASR (stderr goes to stderr, stdout captured as JSON)
    local volc_tmpfile="$OUTDIR/.volc_result_$$.json"
    python3 "$volc_script" "$audio_file" > "$volc_tmpfile" 2>&2
    local volc_exit=$?

    if [ $volc_exit -ne 0 ] || [ ! -s "$volc_tmpfile" ]; then
        echo "Warning: Volcengine ASR failed (exit=$volc_exit), falling back to whisper" >&2
        rm -f "$volc_tmpfile"
        return 1
    fi

    # Parse result - volc_asr.py outputs clean JSON to stdout
    local full_text=$(jq -r '.full_text' "$volc_tmpfile")
    local duration=$(jq -r '.duration' "$volc_tmpfile")

    # Save segments array to transcript JSON (compatible with whisper format)
    jq '.segments' "$volc_tmpfile" > "$transcript_json"
    echo "$full_text" > "$transcript_txt"
    rm -f "$volc_tmpfile"

    local seg_count=$(jq length "$transcript_json")
    local chars=$(echo -n "$full_text" | wc -c | tr -d ' ')

    echo "Volcengine ASR complete: $seg_count segments, $chars chars" >&2

    # Output JSON
    jq -n --arg json "$transcript_json" --arg txt "$transcript_txt" \
        --argjson seg "$seg_count" --argjson dur "$duration" --argjson chars "$chars" \
        '{transcript_json: $json, transcript_txt: $txt, segments: $seg, duration_s: $dur, chars: $chars, subtitle_source: "volc_asr"}'

    return 0
}

transcribe_audio() {
    local audio_file="$1"
    local model="$2"

    if [ ! -f "$audio_file" ]; then
        echo "Error: Audio file not found: $audio_file" >&2
        exit 1
    fi

    # Generate output paths
    local base_name=$(basename "$audio_file" | sed 's/\.[^.]*$//')
    local transcript_json="$OUTDIR/${base_name}_transcript.json"
    local transcript_txt="$OUTDIR/${base_name}_transcript.txt"

    # Check cache if not forced
    if [ "$FORCE_TRANSCRIBE" != "true" ]; then
        local cached_file=$(check_existing_transcript "$base_name")
        if [ $? -eq 0 ]; then
            echo "Using cached transcript: $cached_file" >&2

            # Determine source from cached file
            local source="unknown"
            if [[ "$cached_file" == *"_subtitle.txt" ]]; then
                source="native_cc"
            elif [ -f "$transcript_json" ]; then
                # Try to read source from JSON
                source=$(jq -r '.source // "whisper"' "$transcript_json" 2>/dev/null || echo "whisper")
            else
                source="whisper"
            fi

            # Return cached result
            local chars=$(wc -c < "$cached_file" | tr -d ' ')
            if [ -f "$transcript_json" ]; then
                local segments=$(jq length "$transcript_json" 2>/dev/null || echo "1")
                local duration=$(jq '[-1].end // 0' "$transcript_json" 2>/dev/null || echo "0")
            else
                segments=1
                duration=0
            fi

            jq -n --arg json "$transcript_json" --arg txt "$cached_file" \
                --argjson seg "$segments" --argjson dur "$duration" --argjson chars "$chars" --arg src "$source" \
                '{transcript_json: $json, transcript_txt: $txt, segments: $seg, duration_s: $dur, chars: $chars, subtitle_source: $src}'
            return
        fi
    fi

    # Try Volcengine ASR first
    if transcribe_with_volc_asr "$audio_file" "$base_name" "$transcript_json" "$transcript_txt"; then
        return
    fi

    echo "Transcribing with faster-whisper (model: $model)..." >&2
    uv run --with "faster-whisper" --with "opencc-python-reimplemented" python3 - "$audio_file" "$model" "$transcript_json" "$transcript_txt" << 'PYEOF'
import sys, json, time
from faster_whisper import WhisperModel
import opencc

audio_file = sys.argv[1]
model_size = sys.argv[2]
json_out = sys.argv[3]
txt_out = sys.argv[4]

converter = opencc.OpenCC('t2s')

print(f"Loading {model_size} model...", file=sys.stderr, flush=True)
model = WhisperModel(model_size, device="cpu", compute_type="int8")

print("Transcribing...", file=sys.stderr, flush=True)
start = time.time()
segments, info = model.transcribe(audio_file, language="zh", beam_size=5, vad_filter=True)

results = []
for seg in segments:
    text = converter.convert(seg.text.strip())
    results.append({"start": round(seg.start, 1), "end": round(seg.end, 1), "text": text})
    if len(results) % 100 == 0:
        print(f"  {len(results)} segments ({seg.end:.0f}s)...", file=sys.stderr, flush=True)

elapsed = time.time() - start
print(f"Done: {len(results)} segments in {elapsed:.0f}s", file=sys.stderr, flush=True)

with open(json_out, "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

full_text = " ".join([s["text"] for s in results])
with open(txt_out, "w") as f:
    f.write(full_text)

# Save source to JSON file
results_with_meta = {
    "source": "whisper",
    "segments": results
}

# Also save segments-only format for compatibility
with open(json_out, "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Output JSON to stdout
json.dump({
    "transcript_json": json_out,
    "transcript_txt": txt_out,
    "segments": len(results),
    "duration_s": results[-1]["end"] if results else 0,
    "chars": len(full_text),
    "subtitle_source": "whisper"
}, sys.stdout)
PYEOF

    # Step 3: Sentence merger - merge fragmented segments into complete sentences
    local merged_json="$OUTDIR/${base_name}_merged.json"
    local merged_txt="$OUTDIR/${base_name}_merged.txt"
    local MERGER_SCRIPT="$HOME/.openclaw/workspace/scripts/sentence_merger.py"

    if [ -f "$MERGER_SCRIPT" ] && [ -f "$transcript_json" ]; then
        echo "Merging fragmented segments into sentences..." >&2
        python3 "$MERGER_SCRIPT" "$transcript_json" -o "$merged_json" 2>&1 | grep -v "^$" >&2 || true

        if [ -f "$merged_json" ]; then
            # Generate merged plain text
            python3 -c "
import json
with open('$merged_json') as f:
    sentences = json.load(f)
with open('$merged_txt', 'w') as f:
    f.write(' '.join(s['text'] for s in sentences))
" 2>/dev/null

            local merged_count=$(python3 -c "import json; print(len(json.load(open('$merged_json'))))" 2>/dev/null || echo "0")
            local raw_count=$(python3 -c "import json; print(len(json.load(open('$transcript_json'))))" 2>/dev/null || echo "0")
            echo "Sentence merger: $raw_count raw segments → $merged_count sentences" >&2
        fi
    fi
}

# ============================================================================
# Handle subtitle-only case (no audio to transcribe)
# ============================================================================

process_subtitle_file() {
    local subtitle_file="$1"
    local platform="$2"
    local video_id="$3"

    if [ ! -f "$subtitle_file" ]; then
        echo "Error: Subtitle file not found: $subtitle_file" >&2
        exit 1
    fi

    # Read subtitle content
    local text=$(cat "$subtitle_file")
    local chars=$(echo -n "$text" | wc -c | tr -d ' ')

    # Create transcript files for consistency
    local transcript_json="$OUTDIR/${platform}_${video_id}_transcript.json"
    local transcript_txt="$subtitle_file"

    # Create a simple JSON structure (no segments, just full text)
    echo '[{"start": 0, "end": 0, "text": "'"$text"'"}]' > "$transcript_json"

    jq -n --arg json "$transcript_json" --arg txt "$transcript_txt" --argjson chars "$chars" \
        '{transcript_json: $json, transcript_txt: $txt, segments: 1, duration_s: 0, chars: $chars, subtitle_source: "native_cc"}'
}

# ============================================================================
# Main workflow
# ============================================================================

case "$STEP" in
    download)
        VIDEO_ID=$(extract_video_id "$PLATFORM" "$INPUT")
        download_audio "$PLATFORM" "$INPUT" "$VIDEO_ID"
        ;;

    transcribe)
        # Check if input is a subtitle file or audio file
        if [[ "$INPUT" == *"_subtitle.txt" ]]; then
            # Extract platform and video ID from filename
            BASE_NAME=$(basename "$INPUT" "_subtitle.txt")
            PLAT=$(echo "$BASE_NAME" | cut -d_ -f1)
            VID=$(echo "$BASE_NAME" | cut -d_ -f2-)
            process_subtitle_file "$INPUT" "$PLAT" "$VID"
        else
            transcribe_audio "$INPUT" "$MODEL"
        fi
        ;;

    full|*)
        # Full workflow: download + transcribe
        VIDEO_ID=$(extract_video_id "$PLATFORM" "$INPUT")

        echo "=== Step 1: Download ===" >&2
        DOWNLOAD_RESULT=$(download_audio "$PLATFORM" "$INPUT" "$VIDEO_ID")
        echo "$DOWNLOAD_RESULT" | jq '.' >&2

        # Check if we got a subtitle or audio
        SUBTITLE_FILE=$(echo "$DOWNLOAD_RESULT" | jq -r '.subtitle_file // empty')
        AUDIO_FILE=$(echo "$DOWNLOAD_RESULT" | jq -r '.audio_file // empty')

        echo "" >&2
        echo "=== Step 2: Transcribe ===" >&2

        if [ -n "$SUBTITLE_FILE" ]; then
            # Process subtitle file
            TRANSCRIBE_RESULT=$(process_subtitle_file "$SUBTITLE_FILE" "$PLATFORM" "$VIDEO_ID")
        elif [ -n "$AUDIO_FILE" ]; then
            # Transcribe audio
            TRANSCRIBE_RESULT=$(transcribe_audio "$AUDIO_FILE" "$MODEL")
        else
            echo "Error: No audio or subtitle file to process" >&2
            exit 1
        fi

        echo "$TRANSCRIBE_RESULT" | jq '.' >&2

        echo "" >&2
        echo "=== Complete ===" >&2

        # Merge results
        jq -n --argjson download "$DOWNLOAD_RESULT" --argjson transcribe "$TRANSCRIBE_RESULT" \
            '$download + $transcribe'
        ;;
esac
