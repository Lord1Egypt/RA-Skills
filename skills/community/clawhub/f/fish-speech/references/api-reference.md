# API Reference

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/audio/speech` | Single synthesis |
| POST | `/v1/audio/speech/batch` | Batch (≤32 items) |
| GET | `/v1/audio/voices` | List voices |
| POST | `/v1/audio/voices` | Upload voice |
| DELETE | `/v1/audio/voices/{name}` | Delete voice |

## POST /v1/audio/speech

**Standard parameters:** `input` (required), `model`, `voice` (default "default"), `response_format` (wav/mp3/flac/pcm/aac/opus), `speed` (0.25-4.0)

**Fish Speech extensions:** `ref_audio` (URL/base64/file://), `ref_text`, `max_new_tokens` (default 2048), `stream` (requires pcm format), `temperature`, `top_p`, `top_k`, `repetition_penalty`, `seed`

Returns binary audio, Content-Type such as `audio/wav`.

## POST /v1/audio/speech/batch

```json
{
  "items": [{"input": "Text 1"}, {"input": "Text 2"}],
  "voice": "default", "ref_audio": "https://...", "ref_text": "..."
}
```
Returns: `{"results": [{"index": 0, "status": "success", "audio_data": "<base64>", "media_type": "audio/wav"}, ...], "total": ..., "succeeded": ..., "failed": ...}`

```python
import base64, httpx
resp = httpx.post(".../v1/audio/speech/batch", json={"items": [{"input": "Hello."}]})
for r in resp.json()["results"]:
    if r["status"] == "success":
        with open(f"out_{r['index']}.wav", "wb") as f: f.write(base64.b64decode(r["audio_data"]))
```

## Voice Management

**Upload:**
```bash
curl -X POST http://localhost:8091/v1/audio/voices \
  -F "audio_sample=@voice.wav" -F "consent=user_id" \
  -F "name=my_voice" -F "ref_text=Transcript." -F "speaker_description=warm narrator"
```
Parameters: `audio_sample` (required, ≤10MB), `consent` (required), `name` (required), `ref_text`, `speaker_description`

After upload: `"voice": "my_voice"`. Persisted to `~/.cache/vllm-omni/speakers/*.safetensors`.

**Delete:** `curl -X DELETE .../voices/my_voice`

## Streaming Output

**vLLM:** `"stream": true, "response_format": "pcm"` → raw PCM stream (44100 Hz)
```bash
curl -N ... -d '{"input":"...", "stream":true, "response_format":"pcm"}' --no-buffer | play -t raw -r 44100 -e signed -b 16 -c 1 -
```

**SGLang:** SSE protocol, events contain base64 WAV chunks:
```python
import requests, json, base64, io, wave

with requests.post(..., json={..., "stream": True}, stream=True) as s:
    chunks, fmt = [], None
    for line in s.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: ") or "[DONE]" in line: continue
        b64 = json.loads(line[6:]).get("audio", {}).get("data")
        if not b64: continue
        with wave.open(io.BytesIO(base64.b64decode(b64)), "rb") as w:
            if not fmt: fmt = (w.getnchannels(), w.getsampwidth(), w.getframerate())
            chunks.append(w.readframes(w.getnframes()))

nc, sw, fr = fmt
with wave.open("out.wav", "wb") as w:
    w.setnchannels(nc); w.setsampwidth(sw); w.setframerate(fr)
    w.writeframes(b"".join(chunks))
```

## SGLang Parameters

Similar to vLLM, with additional `references: [{audio_path, text}]`. Others: `temperature`, `top_p`, `top_k`, `repetition_penalty`, `seed`.