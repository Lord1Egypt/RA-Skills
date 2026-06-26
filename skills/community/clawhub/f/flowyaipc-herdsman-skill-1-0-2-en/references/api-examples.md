# Herdsman API Call Examples

## Basic Info

- Service root: `http://127.0.0.1:8080`
- OpenAI root path: `http://127.0.0.1:8080/v1`
- Anthropic endpoint: `http://127.0.0.1:8080/v1/anthropic/messages`
- Authentication: if the service has `api_key` configured, include `Authorization: Bearer <key>`

## Principles

- Prefer using Python scripts under `scripts/`
- Run `check_model.py` for model discovery first, then send actual requests
- Do not construct long JSON for image, OCR, or speech tasks directly in shell

## 1. Model Discovery

List all discovered models:

```bash
python headsman-skill/scripts/check_model.py
```

Query a single model:

```bash
python headsman-skill/scripts/check_model.py "qwen2.5-7b-instruct"
```

Output JSON:

```bash
python headsman-skill/scripts/check_model.py --json
```

## 2. OpenAI Chat Completion

Minimal call:

```bash
python headsman-skill/scripts/chat_completion.py "Hello, please introduce yourself" --model qwen2.5-7b-instruct
```

With system prompt:

```bash
python headsman-skill/scripts/chat_completion.py "Explain quantum mechanics" --model qwen2.5-7b-instruct --system "You are a rigorous science educator"
```

Streaming output:

```bash
python headsman-skill/scripts/chat_completion.py "Write a product description" --model qwen2.5-7b-instruct --stream
```

Enable reasoning mode (reasoning_effort / thinking):

```bash
python headsman-skill/scripts/chat_completion.py "1+1=?" --model deepseek-r1-distill-qwen-7b --reasoning-effort high
python headsman-skill/scripts/chat_completion.py "complex reasoning question" --model your-model --thinking-enabled --thinking-tokens 2048
```

Pass full messages via JSON file:

```bash
python headsman-skill/scripts/chat_completion.py --model qwen2.5-7b-instruct --messages-json messages.json --json
```

## 3. OpenAI Embeddings

```bash
python -c "
from herdsman_client import HerdsmanClient
c = HerdsmanClient()
r = c.embeddings(model='bge-small-zh', input_text='Hello world')
print(r)
"
```

## 4. OpenAI Rerank

```bash
python -c "
from herdsman_client import HerdsmanClient
c = HerdsmanClient()
r = c.rerank(model='bge-reranker', query='Beijing weather', documents=['It is sunny in Beijing today', 'It is raining in Shanghai', 'Guangzhou is cloudy'])
print(r)
"
```

## 5. OpenAI Image Generation

Get URL only:

```bash
python headsman-skill/scripts/generate_image.py "A cute cat sleeping in the sun" --model zimage-turbo
```

Auto-download to `outputs/`:

```bash
python headsman-skill/scripts/generate_image.py "Cyberpunk city night" --model zimage-turbo --auto-save --download
```

Return `b64_json` and save directly:

```bash
python headsman-skill/scripts/generate_image.py "Minimalist poster" --model zimage-turbo --format b64_json --auto-save
```

## 6. OpenAI Image Editing

Edit a local image and download the result:

```bash
python headsman-skill/scripts/edit_image.py "Change the sky to sunset effect" --model your-image-edit-model --image .\input.png --auto-save --download
```

With mask for local editing:

```bash
python headsman-skill/scripts/edit_image.py "Change only the cup in the person's hand to a transparent glass" --model your-image-edit-model --image .\input.png --mask .\mask.png --auto-save --download
```

## 7. OpenAI img2img

Style transfer or full repaint:

```bash
python headsman-skill/scripts/img2img.py "Watercolor illustration style" --model your-img2img-model --image .\input.png --auto-save --download
```

## 8. OCR Text Recognition

Recognize text from a local image, print full page text:

```bash
python headsman-skill/scripts/ocr.py ./invoice.jpg --model paddleocr-ppocrv5-server
```

Output full JSON (per-line text, confidence, bounding box coordinates):

```bash
python headsman-skill/scripts/ocr.py ./screenshot.png --model paddleocr-ppocrv5-server --json
```

Save results to file:

```bash
python headsman-skill/scripts/ocr.py ./receipt.jpg --model paddleocr-ppocrv5-server --output "D:/ocr_result.json"
```

Call client directly via Python:

```bash
python -c "
from herdsman_client import HerdsmanClient, file_to_data_url
c = HerdsmanClient()
r = c.ocr(model='paddleocr-ppocrv5-server', image_base64=file_to_data_url('./test.png'))
print(r['text'])
"
```

## 9. OpenAI Audio Transcription

Transcribe local audio:

```bash
python headsman-skill/scripts/transcribe_audio.py .\meeting.wav --model whisper-base
```

Specify language and output full JSON:

```bash
python headsman-skill/scripts/transcribe_audio.py .\interview.wav --model whisper-base --language zh --json
```

Transcribe remote audio URL:

```bash
python headsman-skill/scripts/transcribe_audio.py "https://example.com/demo.wav" --model whisper-base
```

## 10. OpenAI Speech Synthesis (TTS)

Basic TTS:

```bash
python headsman-skill/scripts/audio_speech.py "This is a text-to-speech test" --model edge-tts --voice zh-CN-YunxiNeural --auto-save
```

VoiceDesign mode (natural language voice description):

```bash
python headsman-skill/scripts/audio_speech.py "Welcome to today's news" --model qwen3-tts-customvoice --voice-description "Gentle female voice, moderate pace" --language Chinese --auto-save
```

VoiceClone mode:

```bash
python headsman-skill/scripts/audio_speech.py "Voice clone test" --model qwen3-tts-customvoice --ref-audio .\sample.wav --ref-text "Reference audio text content" --language Chinese --auto-save
```

Streaming TTS (returns stream_url):

```bash
python headsman-skill/scripts/audio_speech.py "This is a long text for streaming output" --model edge-tts --voice zh-CN-YunxiNeural --stream --json
```

## 11. Query Audio Service Capabilities

Note: case-sensitive:

```bash
python -c "
from herdsman_client import HerdsmanClient
c = HerdsmanClient()
print(c.audio_info('qwen3-tts-customvoice'))
print(c.audio_info('whisper-base'))
print(c.audio_info('funasr'))
"
```

## 12. Anthropic Messages Compatible Call

```bash
python headsman-skill/scripts/anthropic_messages.py "Please summarize the key points of this text" --model qwen2.5-7b-instruct
```

With system prompt:

```bash
python headsman-skill/scripts/anthropic_messages.py "Please rewrite the following content as a more formal announcement" --model qwen2.5-7b-instruct --system "You are a professional copywriter"
```

## 13. Reuse the Generic Client Directly

If other agent platforms need to generate their own temporary scripts, directly reuse `herdsman_client.py`:

```python
from herdsman_client import HerdsmanClient

client = HerdsmanClient(base_url="http://127.0.0.1:8080", api_key="")
result = client.chat_completions(
    model="qwen2.5-7b-instruct",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7,
)
print(result["choices"][0]["message"]["content"])
```

OCR example:

```python
from herdsman_client import HerdsmanClient, file_to_data_url

client = HerdsmanClient()
result = client.ocr(model="paddleocr-ppocrv5-server", image_base64=file_to_data_url("invoice.png"))
print(result["text"])
for line in result["lines"]:
    print(f"[{line['score']:.2f}] {line['text']}")
```
