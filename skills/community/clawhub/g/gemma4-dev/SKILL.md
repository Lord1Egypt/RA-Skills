---
name: gemma4-dev
description: "Use when designing, configuring, or implementing applications targeting the Google Gemma 4 model family. Covers model architecture selection (26B/12B/E2B/E4B), native Thinking Mode formatting, function calling schemas, multimodal audio/vision pipelines, and deployment reference patterns."
license: MIT
metadata:
  openclaw:
    version: "1.0.4"
    authors:
      - "John Greenfield"
      - "OpenClaw Team"
    keywords:
      - gemma4
      - thinking-mode
      - function-calling
      - multimodal-ai
      - developer-tooling
    capabilities:
      network:
        egress:
          - "huggingface.co (Optional: Pinned model & tokenizer downloads)"
          - "cdn-lfs.huggingface.co (Optional: Large model weight downloads)"
          - "aiplatform.googleapis.com (Optional: Vertex AI cloud deployment reference)"
      environment_variables:
        optional:
          - "GEMMA_MODEL_PATH"
          - "GEMMA_TOKENIZER_PATH"
          - "GOOGLE_CLOUD_PROJECT"
          - "GOOGLE_CLOUD_LOCATION"
          - "GOOGLE_CLOUD_ENDPOINT_ID"
---

# Gemma 4 Developer Tool (gemma4-dev)

Comprehensive architecture, integration, and orchestration guide for the Google Gemma 4 model family.

---

## 1. Model Portfolio & Selection

Select the exact Gemma 4 variant based on compute budget, input modality, and context requirements:

| Model Tier | Checkpoint / Repo | Parameters / Architecture | Context Window | Supported Modalities | Ideal Target Environment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 26B A4B** | `google/gemma-4-26B-A4B-it` | Mixture-of-Experts (4B active) | 256K tokens | Text, Image | Cloud / Workstation (high reasoning efficiency) |
| **Gemma 4 31B** | `google/gemma-4-31B-it` | Dense | 256K tokens | Text, Image | High-VRAM Workstations / Enterprise Cloud |
| **Gemma 4 12B** | `google/gemma-4-12B-it` | Dense Multimodal | 256K tokens | Text, Image, Audio (Native) | Consumer GPUs (12GB+), Dev Workstations |
| **Gemma 4 E4B** | `google/gemma-4-E4B-it` | Dense Mobile / Edge | 128K tokens | Text, Image, Audio (Native) | Edge servers, High-end Mobile / NPU |
| **Gemma 4 E2B** | `google/gemma-4-E2B-it` | Dense Ultra-lightweight | 128K tokens | Text, Image, Audio (Native) | On-device, In-browser (ONNX / WebGPU) |

*For complete quantization sizing (FP16 vs INT8 vs INT4 AWQ/GGUF) and KV cache allocation tables, see [`references/hardware-sizing.md`](references/hardware-sizing.md).*

---

## 2. Native Thinking Mode & Reasoning

Gemma 4 features native Thinking Mode to reason through complex multi-step logic before producing user-visible output.

### Formatting & Thought Isolation
Thinking traces are encapsulated in native tags:
```text
<start_of_turn>user
Design an event-driven retry mechanism with exponential backoff and jitter.
<end_of_turn>
<start_of_turn>model
<thought>
Analyze requirements: backoff formula, base delay, max attempts, and jitter factor.
Select full jitter vs equal jitter: full jitter reduces collision clusters best.
Draft TypeScript implementation with cancellation token support.
</thought>
[Final user-facing implementation]
<end_of_turn>
```

### Live Stream Parsing (Multi-Block & Zero-Leakage)
To parse and isolate `<thought>` blocks during real-time streaming without leaking partial tags or subsequent thought blocks into user-visible responses, use the bundled streaming parser:
- **Module**: `scripts/stream_parser.py` (`GemmaThoughtStreamParser`)
- **Key Guarantees**:
  - Handles multiple alternating `<thought>...</thought>` blocks across a single turn.
  - Safely buffers split tags across arbitrary token chunks.
  - Fail-closed: unclosed thought blocks at stream termination remain quarantined in the thought channel.
- **Usage**:
  ```python
  from scripts.stream_parser import GemmaThoughtStreamParser

  parser = GemmaThoughtStreamParser()
  for token_chunk in token_stream:
      for event_kind, text in parser.feed(token_chunk):
          if event_kind == "thought":
              render_reasoning_trace(text)
          else:
              render_user_response(text)
  ```

---

## 3. Native Multimodal Integration (Audio & Vision)

Gemma 4 (12B, E4B, E2B) natively tokenizes audio waveforms and images without external pipeline converters:

- **Audio Inputs**: Embed raw waveforms or base64 WAV buffers via `<audio mime_type="audio/wav">...</audio>` tags.
- **Vision Inputs**: Embed image buffers via `<image mime_type="image/png">...</image>` tags.
- *Detailed turn syntax and Python multimodal inference examples are documented in [`references/multimodal.md`](references/multimodal.md).*

---

## 4. Tool Calling & Function Schemas

Gemma 4 supports structured function calling with turn-based schema enforcement:

```text
<start_of_turn>user
Available tools:
[
  {
    "name": "lookup_device_status",
    "description": "Returns connection and battery telemetry for a paired IoT device.",
    "parameters": {
      "type": "object",
      "properties": {
        "device_id": {"type": "string", "description": "Unique identifier of the device"}
      },
      "required": ["device_id"]
    }
  }
]

Check status for device "esp32-living-room".
<end_of_turn>
<start_of_turn>model
<thought>
User requested status for "esp32-living-room".
Call lookup_device_status with device_id="esp32-living-room".
</thought>
<call:lookup_device_status>{ "device_id": "esp32-living-room" }</call:lookup_device_status>
<end_of_turn>
<start_of_turn>tool
{ "status": "online", "battery_percent": 88, "firmware": "v2.1.4" }
<end_of_turn>
<start_of_turn>model
<thought>
Device status is online with 88% battery and firmware v2.1.4. Formulate summary.
</thought>
The living room device (esp32-living-room) is online with 88% battery remaining on firmware v2.1.4.
<end_of_turn>
```

---

## 5. Deployment & Implementation Reference Patterns

The `examples/` directory contains developer reference patterns hardened against supply-chain and data-leakage risks:

- **Local Gradio Thinking Inspector (`examples/gradio_thinking_mode_demo.py`)**:
  - Lazily initialized pipeline to prevent unintended network access or compute allocation at import time.
  - Pinned immutable revision (`e9a0c10825eb6e2897621c1723c4a24f0c406214`) and `trust_remote_code=False`.
  - Supports offline local paths via `GEMMA_MODEL_PATH`.
- **On-Device WebGPU / ONNX (`examples/transformers_js_onnx_example.js`)**:
  - Uses explicit commit revision (`8e27c81d3f25b3992b4931a7884d41a7d6e5d614`).
  - Supports local directory execution for browser/edge runtimes.
- **Enterprise Cloud Deployment (`examples/vertex_ai_deployment.py`)**:
  - Programmatic endpoint prediction pattern for enterprise hosting on Google Cloud Vertex AI.
  - Pinned tokenizer revision (`7b2d51ae52dc0a905a92a548232c454e56eb6009`) with `trust_remote_code=False`.

---

## 6. Security & Privacy Governance

1. **Artifact Pinning & Code Execution**:
   - Always pin remote Hugging Face model IDs to immutable commit hashes.
   - Enforce `trust_remote_code=False` to prevent execution of arbitrary remote code during model loading.
   - For air-gapped or high-security deployments, load weights from verified local directories via `GEMMA_MODEL_PATH`.
2. **Reasoning Isolation & Zero Leakage**:
   - Never stream or expose unredacted `<thought>` blocks to end users in client applications, as intermediate reasoning may reflect internal prompts, instructions, or sensitive data.
   - Always use a state-machine parser like `GemmaThoughtStreamParser` with fail-closed guarantees for unclosed tags.
3. **Cloud Egress & Data Boundaries**:
   - Cloud deployments (e.g., Vertex AI) transmit prompt data across external networks. Verify endpoint regions and retention policies before processing sensitive or proprietary context.
   - Cloud scripts must rely on strictly scoped IAM roles (`Vertex AI User`) rather than administrative credentials.
