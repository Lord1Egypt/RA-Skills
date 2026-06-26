# ffprobe Analysis Reference

## Complete JSON Output (Most Useful)
```bash
ffprobe -v quiet -print_format json -show_format -show_streams -show_chapters "input.mp4"
```

## Extract Specific Values

### Duration (seconds, decimal)
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "input.mp4"
```

### Resolution
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height \
  -of csv=s=x:p=0 "input.mp4"
# Output: 1920x1080
```

### Frame rate
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate \
  -of default=noprint_wrappers=1:nokey=1 "input.mp4"
# Output: 30000/1001 (≈29.97fps) — divide for decimal
```

### Video codec
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,profile,level \
  -of default=noprint_wrappers=1 "input.mp4"
```

### Audio info
```bash
ffprobe -v error -select_streams a:0 \
  -show_entries stream=codec_name,sample_rate,channels,channel_layout,bit_rate \
  -of default=noprint_wrappers=1 "input.mp4"
```

### File size (bytes)
```bash
ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1:nokey=1 "input.mp4"
```

### Total bitrate
```bash
ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 "input.mp4"
```

### Number of streams
```bash
ffprobe -v error -show_entries format=nb_streams -of default=noprint_wrappers=1:nokey=1 "input.mp4"
```

### List all streams with types
```bash
ffprobe -v error -show_entries stream=index,codec_type,codec_name \
  -of csv=p=0 "input.mp4"
# Output:
# 0,video,h264
# 1,audio,aac
# 2,subtitle,mov_text
```

### Rotation metadata
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream_tags=rotate \
  -of default=noprint_wrappers=1:nokey=1 "input.mp4"
```

### Pixel format (important for filter compatibility)
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=pix_fmt \
  -of default=noprint_wrappers=1:nokey=1 "input.mp4"
```

### Color space / HDR info
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=color_space,color_transfer,color_primaries \
  -of default=noprint_wrappers=1 "input.mp4"
```

### Chapter list
```bash
ffprobe -v quiet -print_format json -show_chapters "input.mp4" | \
  python3 -c "import sys,json; [print(f'{c[\"start_time\"]}s - {c[\"end_time\"]}s: {c[\"tags\"].get(\"title\",\"Untitled\")}') for c in json.load(sys.stdin)['chapters']]"
```

## Parse JSON with jq
> **Note**: `jq` requires separate installation (`brew install jq` / `apt install jq` / `winget install jqlang.jq`). Use the Python section below if `jq` is unavailable.
```bash
# Duration
ffprobe -v quiet -print_format json -show_format "input.mp4" | jq '.format.duration | tonumber'

# All stream codecs
ffprobe -v quiet -print_format json -show_streams "input.mp4" | jq '[.streams[] | {index, codec_type, codec_name}]'

# Video resolution
ffprobe -v quiet -print_format json -show_streams "input.mp4" | \
  jq '.streams[] | select(.codec_type=="video") | "\(.width)x\(.height)"'
```

## Parse JSON with Python
```python
import subprocess, json

result = subprocess.run([
    'ffprobe', '-v', 'quiet',
    '-print_format', 'json',
    '-show_format', '-show_streams',
    'input.mp4'
], capture_output=True, text=True)

data = json.loads(result.stdout)
fmt = data['format']
streams = data['streams']

video = next(s for s in streams if s['codec_type'] == 'video')
audio = next((s for s in streams if s['codec_type'] == 'audio'), None)

print(f"Duration: {float(fmt['duration']):.2f}s")
print(f"Size: {int(fmt['size']) / 1024 / 1024:.1f} MB")
print(f"Video: {video['codec_name']} {video['width']}x{video['height']}")
if audio:
    print(f"Audio: {audio['codec_name']} {audio.get('sample_rate','?')}Hz {audio.get('channels','?')}ch")
```
