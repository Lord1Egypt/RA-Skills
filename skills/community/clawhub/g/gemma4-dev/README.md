# Gemma 4 Developer Tool (gemma4-dev)

The **Gemma 4 Developer Tool** for OpenClaw provides architecture guidance, deployment reference patterns, and orchestration utilities for building with Google's Gemma 4 models.

## Features

- **Model Selection & Sizing**: Comprehensive hardware and VRAM sizing across 26B (MoE), 31B, 12B, and E2B/E4B (`references/hardware-sizing.md`).
- **Thinking Mode Orchestration**: Native `<thought>` tag encapsulation with real-time stream parsing (`scripts/stream_parser.py`).
- **Native Multimodality**: First-class support for native audio waveforms and image tokens (`references/multimodal.md`).
- **Tool Calling**: Turn-based schema definitions for robust agentic tool loops.
- **Reference Deployments**: Safe, modular patterns for WebGPU/ONNX and Vertex AI cloud hosting (`examples/`).

## Installation

```bash
clawhub install gemma4-dev
```

## Running Tests

```bash
python3 tests/test_stream_parser.py
```

## Security & Compliance

This tool adheres strictly to the OpenClaw AgentSkills specification:
- Principle of Least Privilege: Zero ambient network egress or disk access in core guidelines.
- Cloud Egress Governance: Cloud deployment examples explicitly declare network requirements (`aiplatform.googleapis.com`) and required IAM scopes.
- Zero External Injections: All prompts and function signatures are validated within local sandbox boundaries.
