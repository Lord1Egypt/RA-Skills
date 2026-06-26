---
name: drawthings-agent
description: Generate images using Draw Things app via dt-skill CLI or MCP
---

# Skill: Draw Things for AI Agents

**Slug:** `drawthings-agent`  
**Display Name:** `Draw Things for AI Agents`

## 🛠 Setup & Verification (AI ACTION REQUIRED)
If `dt-skill` is not found or fails with "module not found", you **MUST** perform these steps:
1.  **Global Installation**: Run `npm install -g @mijuu/drawthings` to ensure the CLI and MCP entry points are available.
2.  **Verify Environment**: Run `dt-skill doctor`. If paths are missing, ask the user for their Draw Things model and server binary paths, then run `dt-skill config --server-path "..." --models-path "..."`.

## 🧩 Protocol Preference (CRITICAL for AI)
This skill provides two interfaces. You **MUST** follow this priority:
1. **Model Context Protocol (MCP)**: If you see the tool `generate_image` in your toolset, **ALWAYS** use it. It is the most reliable interface for AI.
2. **CLI Interface (dt-skill)**: Use `dt-skill gen` ONLY if the MCP tool is missing or for server management (e.g., `dt-skill server start`).

## 🛠 Target Tool
- **MCP Tool**: `generate_image` (Preferred)
- **CLI Command**: `dt-skill gen` (Fallback)

## 🤖 AI Usage Instructions

### 1. Basic Generation
- **MCP**: Call `generate_image(prompt: "...")`.
- **CLI**: Run `dt-skill gen --prompt "..."`.
You **MUST** provide a detailed prompt.

### 2. High Quality & Upscaling (CRITICAL)
If the user asks for "high quality", "high resolution", "4K", or "clear" images, you **MUST** use the `--upscale` parameter **at the time of generation**.
- **For 2x Upscale**: `--upscale 2`
- **For 4x Upscale**: `--upscale 4` (Note: Takes significantly longer)
**Example**: `dt-skill gen --prompt "..." --upscale 2`

### 3. Aspect Ratio & Resolution
Default is `1024x576` (16:9). 
- **Square**: `--width 1024 --height 1024`
- **Portrait**: `--width 576 --height 1024`
- **Standard**: `--width 1024 --height 576`

### 4. Model Selection
- **Default**: `z_image_turbo_1.0_q6p.ckpt` (Fastest, 8 steps).
- **Listing Models**: Use `dt-skill models` to see what is available before suggesting a change.

### 5. Task Control & Sessions
When running in environments that support background tasks (like OpenClaw or OpenCode), use `is_background: true` to allow real-time progress monitoring.
- **Progress**: You will see `Sampling step: X/Y`.
- **Heartbeat**: Every 30s you will see `... still working ...`.
- **Timeout**: Default is 600s. For heavy 4x upscales, use `--timeout 1200`.

## ⚠️ CRITICAL CONSTRAINTS for AI
1. **NO TRUNCATION**: Never use "..." or "etc." in the prompt. Provide the complete text.
2. **NO POST-PROCESSING**: Upscaling **MUST** be part of the initial `gen` command.
3. **RESPONSE COMPRESSION**: Ensure "Response Compression" (FPY) is **DISABLED** in Draw Things settings.

## 📋 Parameter Reference (CLI)
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--prompt` | String | (Required) Positive prompt |
| `--negative-prompt` | String | Elements to exclude |
| `--upscale` | Number | 1, 2, or 4 |
| `--model` | String | Filename of the model |
| `--steps` | Number | Number of sampling steps (8-30) |
| `--seed` | Number | 0 for random, or specific number |
| `--output` | Path | Custom path for result |
| `--timeout` | Number | Max runtime in seconds (Default 600) |
