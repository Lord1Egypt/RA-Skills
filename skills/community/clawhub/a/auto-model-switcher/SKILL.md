---
name: auto-model-switcher
description: "Automatically selects the best model based on task type and requirements. Use when: (1) Task requires specific capabilities (coding, analysis, multimodal, writing, research), (2) Need optimal performance/cost balance, (3) Working with long context or complex reasoning."
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "homepage": "https://github.com/mrcuo/auto-model-switcher"
      }
  }
---

# Auto Model Switcher

Intelligently selects the optimal model from available providers based on task characteristics.

## When to Use

- Task requires specific capabilities (coding, analysis, multimodal, writing, research)
- Need optimal performance/cost balance  
- Working with long context or complex reasoning
- User doesn't specify a model preference

## Available Models Analysis

### Qwen Series (bailian provider)

| Model | Context | Multimodal | Best For | Cost |
|-------|---------|------------|----------|------|
| **qwen3.5-plus** | 1M | ✅ Text+Image | General tasks, creative writing, balanced performance | Low |
| **qwen3-max** | 262K | ❌ Text only | Complex reasoning, deep analysis, research | High |
| **qwen3-coder-plus** | 1M | ❌ Text only | Code generation, debugging | Medium |

### Third-party Models (bailian provider)

| Model | Context | Multimodal | Best For |
|-------|---------|------------|----------|
| **glm-5** | 1M | ✅ Text+Image | Multimodal tasks, Chinese optimization |
| **kimi-k2.5** | 200K | ✅ Text+Image | Multimodal, research-oriented |
| **MiniMax-M2.5** | 1M | ✅ Text+Image | Long context multimodal |

## Selection Logic

### Task Type Detection

**Code Tasks** → `bailian/qwen3-coder-plus`
- Keywords: code, programming, debug, fix, implement, develop, coding, script
- File extensions: .py, .js, .ts, .java, .cpp, etc.
- Commands: git, npm, docker, build, compile

**Complex Analysis** → `bailian/qwen3-max`  
- Keywords: analyze, research, compare, evaluate, strategy, deep dive, business analysis
- Tasks requiring multi-step reasoning
- Financial/strategic analysis

**Research Tasks** → `bailian/qwen3-max`
- Keywords: research, investigate, study, survey, academic, literature review
- Complex information synthesis
- Multi-source analysis and comparison

**Writing/Copywriting Tasks** → `bailian/qwen3.5-plus`
- Keywords: write, draft, copywriting, content, article, blog, email, proposal, creative
- Marketing copy, social media content
- Creative writing and storytelling

**Multimodal Tasks** → `bailian/glm-5`
- Image analysis, OCR, visual understanding
- Audio processing (when supported)
- Mixed text+image inputs

**Long Context** → `bailian/qwen3.5-plus`
- Document processing > 200K tokens
- Summarization of large documents
- Historical context analysis

**General Tasks** → `bailian/qwen3.5-plus` (default)
- Chat, simple queries, basic tasks
- When no specific requirements detected

### Fallback Strategy

1. Primary model selection based on task type
2. If primary model fails, fallback to `qwen3.5-plus`
3. If still failing, use current session model

## Usage Examples

### Automatic Selection
```
User: Help me debug this Python code
→ Model: bailian/qwen3-coder-plus

User: Analyze our Q4 financial performance vs competitors  
→ Model: bailian/qwen3-max

User: Research the latest AI trends in marketing
→ Model: bailian/qwen3-max

User: Write a compelling product description for our new service
→ Model: bailian/qwen3.5-plus

User: What's in this image?
→ Model: bailian/glm-5

User: Summarize this 500-page document
→ Model: bailian/qwen3.5-plus
```

### Manual Override
Users can always specify models directly:
- `/model bailian/qwen3-max`
- `Use coder model for this task`

## Implementation Notes

- Always check if target model is available before switching
- Preserve current session context when switching
- Log model selections for learning and optimization
- Respect user's explicit model preferences

## Security Considerations

- Only switch between pre-configured models in openclaw.json
- Never attempt to use unconfigured or unknown models
- Validate model names against available list before switching

## Performance Metrics

Track these metrics for continuous improvement:
- Task completion success rate by model
- Response time by model and task type  
- User satisfaction feedback
- Cost per task type

This skill enables intelligent model routing without user intervention while maintaining full control when needed.

## Iteration Support

- Skills can be updated via `clawhub sync --all`
- Version updates maintain backward compatibility
- New task types can be added without breaking existing functionality