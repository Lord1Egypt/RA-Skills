# Gemma 4 Native Multimodal Integration (Audio & Vision)

The Gemma 4 model family (specifically **12B**, **E4B**, and **E2B**) natively tokenizes audio waveforms and images directly alongside text without requiring external modular adapter pipelines.

---

## 1. Native Audio Turn Formatting

Audio clips are passed into the conversation using raw PCM/WAV byte streams or base64-encoded audio tokens within standard turn delimiters:

```text
<start_of_turn>user
<audio mime_type="audio/wav">UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=</audio>
Transcribe and extract key action items from this meeting snippet.
<end_of_turn>
<start_of_turn>model
<thought>
Audio waveform detected (audio/wav, 16kHz mono).
Analyze acoustic features and map phonemes to text.
Extract actionable items mentioned by speakers.
</thought>
**Transcript**: "We need to finalize the schema migration by Tuesday morning."

**Action Items**:
1. Complete database schema migration before Tuesday.
<end_of_turn>
```

---

## 2. Native Vision & Multi-Image Formatting

Images can be interleaved with user instructions for diagram analysis, UI code generation, or error screenshot inspection:

```text
<start_of_turn>user
<image mime_type="image/png">iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==</image>
Inspect this system architecture diagram. Identify any single points of failure in the ingress routing.
<end_of_turn>
<start_of_turn>model
<thought>
Analyze image tokens: Single ingress proxy routing traffic to three API worker nodes.
Database layer shows a primary instance without automated replica failover.
Identify architectural bottlenecks.
</thought>
The primary architecture has two potential single points of failure:
1. **Ingress Gateway**: Single entry point without redundant load balancers.
2. **Database Primary**: No active-standby replica configuration depicted.
<end_of_turn>
```

---

## 3. Python Interleaved Multimodal Inference Example

```python
from transformers import AutoProcessor, AutoModelForMultimodalCausalLM
import torch

MODEL_ID = "google/gemma-4-12B-it"

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForMultimodalCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

def run_multimodal_turn(text_prompt: str, image_path: str = None, audio_path: str = None):
    inputs = processor(
        text=text_prompt,
        images=image_path,
        audios=audio_path,
        return_tensors="pt"
    ).to(model.device)
    
    with torch.inference_mode():
        output_tokens = model.generate(**inputs, max_new_tokens=512)
        
    return processor.decode(output_tokens[0], skip_special_tokens=True)
```
