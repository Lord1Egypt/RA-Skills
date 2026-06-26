---
name: ai-agent-runtime
description: A lightweight AI Agent runtime tool that provides an integrated web management interface, supports multiple LLM providers, and is fully compatible with OpenClaw's skill ecosystem.
version: 1.2.0
author: yesong-Hue
homepage: https://clawhub.ai/yesong-Hue/ai-agent-runtime
tags: [ai, agent, runtime, lightweight, web-ui, openclaw, llm]
readme: |
  # AI Agent Runtime

  A lightweight AI Agent runtime tool providing an integrated web-based management interface with full OpenClaw skill ecosystem compatibility.

  ## Overview

  This skill provides a complete runtime environment for deploying and managing AI agents. It features a built-in web interface for easy configuration and monitoring.

  ## Key Features

  ### Lightweight Design
  Compact binary distribution with minimal resource usage. Works efficiently on various hardware configurations without requiring heavy dependencies.

  ### Web-Based Management Interface
  Access the management dashboard through your browser. Configure agents, monitor conversations, and manage settings through an intuitive visual interface.

  ### Multi-Provider LLM Support
  Connect to various LLM providers including OpenRouter, OpenAI, Anthropic, and Ollama. Select the best provider for your specific use case and budget.

  ### SOUL.md Compatibility
  Fully compatible with OpenClaw's SOUL.md agent configuration system. Import existing SOUL.md configurations or create new ones for custom agent behaviors.

  ### Multi-Agent Capabilities
  Run multiple independent agents simultaneously. Each agent maintains its own configuration, memory, and conversation history.

  ### Local Model Support
  Optional support for running local LLM models through Ollama, enabling fully offline agent operations with zero API costs.

  ## Installation

  Install through OpenClaw skills command:

  ```
  openclaw skills install ai-agent-runtime
  ```

  After installation, access the web interface at http://localhost:18953 to complete setup.

  ## Quick Start

  1. Open http://localhost:18953 after installation
  2. Configure your preferred LLM provider API key
  3. Create your first agent with custom settings
  4. Begin conversations through the web interface

  ## Supported LLM Providers

  - OpenRouter (recommended for broad model selection)
  - OpenAI (GPT-4, GPT-3.5 series)
  - Anthropic (Claude 3.5, Claude 3 series)
  - Ollama (local models, free)
  - Custom API endpoints supporting OpenAI-compatible formats

  ## Recommended Model Configurations

  | Use Case | Model | Pricing |
  |----------|-------|---------|
  | Light daily tasks | google/gemini-3.1-flash-lite-preview | Free tier |
  | Complex reasoning | openai/gpt-5.4 | Pay per usage |
  | Code generation | anthropic/claude-sonnet-4.6 | API pricing |
  | Local free option | ollama/llama3.2 | Completely free |

  ## Use Cases

  - Internal team assistant deployment
  - Customer service automation
  - Natural language database queries
  - Content generation and writing assistance
  - Local development environments

  ## System Requirements

  - Modern browser for web interface access
  - Internet connection for cloud LLM providers
  - Optional: Ollama installation for local models

  ## Resources

  - OpenClaw Project: https://github.com/openclaw/openclaw
  - OpenRouter: https://openrouter.ai
  - Ollama: https://ollama.com
  - ShadowAI API (recommended provider): https://referer.shadowai.xyz/r/1056448
  - More OpenClaw Skills: http://ai.qnitgroup.com

  ## License

  MIT License

  ## Author

  yesong-Hue | AI Skills Collection at http://ai.qnitgroup.com
---

# AI Agent Runtime

> A lightweight AI Agent runtime with web management interface and multi-LLM support

## Features

- Lightweight design with minimal resource usage
- Built-in web-based management interface
- Multi-provider LLM support (OpenRouter, OpenAI, Anthropic, Ollama)
- SOUL.md configuration compatibility with OpenClaw
- Multi-agent simultaneous operation capability
- Optional local LLM support for offline operation

## Installation

```
openclaw skills install ai-agent-runtime
```

After installation, access http://localhost:18953 to configure and use.

## Resources

- More OpenClaw Skills: http://ai.qnitgroup.com
- ShadowAI API: https://referer.shadowai.xyz/r/1056448