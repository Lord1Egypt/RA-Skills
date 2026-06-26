# MiniMax Toolkit Modalities

## Read this file when
- You need exact CLI examples for a specific modality
- You need to know which script handles which task
- You are choosing between image / video / speech / music workflows

## Capabilities Map

| Modality | Unified Entry | Legacy Script | Typical use |
|---|---|---|---|
| Image generation | `mm.py image` | `mm_image.py` | Text → image |
| Image-to-image | `mm.py i2i` | `mm_i2i.py` | Ref image + prompt → transformed image |
| Video generation | `mm.py video` | `mm_video.py` | Text → video |
| Video template | `mm.py video-template` | `mm_video_template.py` | Template-driven short video |
| Speech synthesis | `mm.py speech` | `mm_speech.py` | Short text → speech |
| Async long-text speech | `mm.py async-speech` | `mm_async_speech.py` | Long text / file → speech |
| Voice clone | `mm.py voice-clone` | `mm_voice_clone.py` | Audio sample → reusable voice |
| Voice design | `mm.py voice-design` | `mm_voice_design.py` | Text description → voice profile |
| Music generation | `mm.py music` | `mm_music.py` | Prompt / lyrics → music |

## Common options
Most generation commands support:
- `--project <ProjectName>`: create a project subdirectory under the output root
- `--output-dir <path>`: override the output root directly
- `--estimate`: print Token Plan usage estimate without executing

## Governance commands

### Real-time remains
```bash
python3 scripts/mm.py remains
```

### Official doc check
```bash
python3 scripts/mm.py check-docs
```

This writes a report to `references/checks/latest-check.md`.

## Unified Entry Examples (Recommended)

### 1. Image generation
```bash
python3 scripts/mm.py image "A cyberpunk cat" --ratio 16:9 --project Demo
```

### 2. Image-to-image
```bash
python3 scripts/mm.py i2i "transform to anime style" --ref ~/photo.jpg --project Demo
```

### 3. Video generation
```bash
python3 scripts/mm.py video "Cinematic flight over ruins" --project Demo
```

### 4. Video template
```bash
# Available templates: labubu, diving, mcdonalds, love_letter, four_seasons
python3 scripts/mm.py video-template labubu --media ~/me.jpg --project Demo
```

### 5. Speech synthesis (short text)
```bash
python3 scripts/mm.py speech "你好！(laughs)" --voice male-qn-qingse --project Demo
```

### 6. Long-text async speech
```bash
python3 scripts/mm.py async-speech ~/long_script.txt --voice male-qn-qingse --project Demo
```
说明：当前按官方最新文档，异步语音创建接口为 `t2a_async_v2`，查询接口为 `query/t2a_async_query_v2`。

### 7. Voice clone
```bash
python3 scripts/mm.py voice-clone ~/my_voice.wav --voice-id my-voice
```

### 8. Voice design
```bash
python3 scripts/mm.py voice-design "A warm, deep male voice" --voice-id new-voice
```

### 9. Music generation
```bash
python3 scripts/mm.py music "Upbeat lo-fi beat" --instrumental --project Demo
```

## Legacy Script Examples

If you need direct script access or more control:

```bash
# Direct script calls still work
python3 scripts/mm_image.py "A red apple" --ratio 16:9 --project Demo
python3 scripts/mm_video.py "Cinematic ruins" --project Demo
python3 scripts/mm_speech.py "Hello" --voice male-qn-qingse --project Demo
python3 scripts/mm_music.py "Lo-fi beat" --instrumental --project Demo
```
mo
```
mo
python3 scripts/mm_speech.py "Hello" --voice male-qn-qingse --project Demo
python3 scripts/mm_music.py "Lo-fi beat" --instrumental --project Demo
```
"Upbeat lo-fi beat" --instrumental --project Demo
```

## Legacy Script Examples

If you need direct script access or more control:

```bash
# Direct script calls still work
python3 scripts/mm_image.py "A red apple" --ratio 16:9 --project Demo
python3 scripts/mm_video.py "Cinematic ruins" --project Demo
python3 scripts/mm_speech.py "Hello" --voice male-qn-qingse --project Demo
python3 scripts/mm_music.py "Lo-fi beat" --instrumental --project Demo
```
