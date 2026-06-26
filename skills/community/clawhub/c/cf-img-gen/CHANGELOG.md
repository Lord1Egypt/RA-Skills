# Changelog

All notable changes to the CF Image Gen skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.0.1] — 2026-05-15

### Added

- **Initial release** of `cf-img-gen`, a Cloudflare Workers AI image generation skill with dual prompt enhancement paths.
- Core `generate()` function that sends text prompts to the Cloudflare Workers AI REST API and returns the generated image as a local JPEG file.
- Support for 4 Cloudflare Workers AI models:
  - `flux-schnell` (FLUX.1-schnell) — fast, good quality (~1-3s)
  - `flux-dev` (FLUX.1-dev) — slower, higher quality (~5-10s)
  - `sdxl` (Stable Diffusion XL) — SDXL-style outputs (~3-5s)
  - `dreamshaper` (DreamShaper 8 LCM) — artistic/stylized (~2-4s)
- **Dual prompt enhancement system:**
  - **Path 1 — Primary LLM agent enhancement:** The calling AI agent (e.g. Jerith) enhances the prompt before passing it via `llm.enhancedPrompt`. Higher quality, context-aware, creative, no extra infrastructure needed.
  - **Path 2 — Ollama enhancement:** A local or remote Ollama LLM handles enhancement automatically via the `ollama` option. Good for standalone/automated use.
  - Enhancement priority: `llm.enhancedPrompt` > `ollama` > original prompt
- Standalone `enhancePromptOllama()` function for prompt enhancement without image generation.
- CLI interface with options for prompt, width, height, model, steps, Ollama settings, and pre-enhanced prompts (`--enhanced-prompt`).
- Programmatic API for use as a Node.js module (`require('./cf-img-gen')`).
- Credential management via env file at `ACCESS/cloudflare-workers-ai.env` (reads `CF_WORKERS_AI_TOKEN` and `CF_WORKERS_AI_ACCOUNT`).
- Ollama configuration via CLI flags (`--ollama`, `--ollama-model`, `--ollama-host`, `--ollama-timeout`), API options, or environment variables (`OLLAMA_HOST`, `OLLAMA_MODEL`).
- Automatic output directory creation at `~/.openclaw/media/cf-img-gen/`.
- Images saved as JPEG with timestamp-based filenames (e.g., `cf-img-1700000000000.jpg`).
- Rich return object including original prompt, enhanced prompt, enhancement source (`llm`/`ollama`), Ollama metadata, and image details.
- Comprehensive `SKILL.md` with installation guide, configuration instructions, usage examples (module + CLI + Discord), both enhancement paths with pros/cons, Ollama setup (local + remote), LLM agent workflow, API reference, and troubleshooting.
- Example env file template (`cloudflare-workers-ai.env.example`) with placeholder values for easy setup. (Removed in post-audit cleanup — users now create the env file directly via the installation instructions.)

### Design Decisions

- **No premium fallback:** Unlike the original nexpix skill this was derived from, `cf-img-gen` is Cloudflare-only. No EvoLink or other paid fallback providers. Keeps the code simple and the cost at $0.
- **Free tier only:** Designed around Cloudflare's free tier (10K neurons/day ≈ 50-100 images). No paid tier logic.
- **Simplified routing:** No complex routing logic. The user picks a model directly via the `model` parameter.
- **No usage tracking:** No local tracking of neuron usage or cost. Relies on Cloudflare's own quota enforcement.
- **Single-file module:** Everything in one `cf-img-gen.js` file for easy portability and maintenance.
- **Dual enhancement paths:** LLM agent enhancement is the primary/recommended path — it's higher quality and uses the agent that's already running. Ollama is the fallback/standalone path for when no LLM agent is involved (scripts, automation, CLI-only usage).
- **LLM enhancement takes priority:** When `llm.enhancedPrompt` is provided, Ollama is skipped entirely. The agent's enhancement is trusted over Ollama's.
- **Graceful Ollama degradation:** Ollama failures (timeout, connection error, empty response) log a warning and fall back to the original prompt. The image generation still proceeds.
- **Ollama defaults to local:** Default host is `http://localhost:11434` with model `llama3.2:3b`. Remote Ollama is supported via CLI flags, API options, or environment variables.
- **Enhancement is optional:** The skill works fully without any prompt enhancement. Both `llm` and `ollama` are opt-in.

### Known Limitations

- Images are always saved as JPEG regardless of model output format.
- No image-to-image (img2img) support — Cloudflare Workers AI is text-to-image only.
- No batch generation — one prompt per API call.
- No built-in prompt moderation — Cloudflare's own content filters apply.
- Free tier quota (10K neurons/day) is enforced by Cloudflare, not tracked locally.
- Ollama enhancement adds latency (typically 1-5s depending on model and hardware).
- Ollama prompt enhancement is English-only (depends on the Ollama model used).
- LLM agent enhancement quality depends on the capability of the calling agent.

### Credits

- Derived from the `nexpix` skill (finndottllc-ui/nexpix on ClawHub), which was used as a reference for the Cloudflare Workers AI API interaction pattern.
- Simplified and cleaned up by Jerith for the Creator Junction community.
- Custom emoji art by NoodlyPanda 💜
