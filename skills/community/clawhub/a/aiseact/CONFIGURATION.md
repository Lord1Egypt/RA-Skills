# Configuration Guide

> How to customize AISEACT behavior to match your preferences.

---

## Invocation Mode

### Option 1: Manual Mode (Recommended, Default)

**Behavior**: AISEACT only runs when you explicitly request it.

**How to use**:
```
User: "请用AISEACT搜索..."
User: "Use AISEACT to research..."
User: "用AISEACT验证这个说法"
```

**Best for**: Users who want control over when the methodology is applied.

---

### Option 2: Autonomous Mode (Opt-in)

**Behavior**: AISEACT can be automatically invoked for relevant queries.

**How to enable**:
Set `disable-model-invocation: false` for the aiseact skill in your AI platform configuration.

**Even in autonomous mode**:
- You can override with: "不用AISEACT，直接搜索..."
- You can request specific sources regardless of ratings
- The AI will indicate when it's using AISEACT methodology

**Best for**: Users who consistently want high-quality, well-sourced answers and don't mind the additional processing time.

---

## Customization Options

### Source Preference Level

Adjust how strictly the methodology filters sources:

| Level | Description | Use Case |
|-------|-------------|----------|
| **Strict** (Default) | Strongly prefer primary sources; avoid listed low-credibility sources | Academic research, professional analysis, fact-checking |
| **Moderate** | Prefer primary sources but include secondary sources freely; warn about low-credibility sources | General research, balanced overview |
| **Minimal** | Use source lists as reference only; include all relevant sources | Diverse perspectives, media analysis, exploring different viewpoints |

**How to set**: Mention in your query: "使用严格/中等/宽松模式"

---

### Workflow Depth

Adjust how many phases of the workflow to apply:

| Depth | Phases | Use Case |
|-------|--------|----------|
| **Quick** | Phases 0, 1, 6 (Planning → Single Search → Answer) | Simple questions, time-sensitive |
| **Standard** | Phases 0, 1, 2, 3, 6 (Adds assessment and targeted search) | Most research questions |
| **Thorough** | All phases including validation and cross-checking | Critical research, high-stakes decisions |

**How to set**: Mention in your query: "快速搜索" / "标准搜索" / "深度搜索"

---

### Language/Source Region Preference

Prioritize sources from specific regions:

| Preference | Behavior |
|------------|----------|
| **Global** (Default) | Balance sources across regions |
| **Chinese-priority** | Prioritize Chinese-language and China-focused sources |
| **English-priority** | Prioritize English-language sources |
| **Specific region** | Prioritize sources from a specific country/region |

**How to set**: Mention in your query: "优先中文来源" / "优先英文来源" / "优先欧洲来源"

---

## Override Commands

When AISEACT is active, you can override its behavior:

| Command | Effect |
|---------|--------|
| "包含 [source]" / "Include [source]" | Include information from a specific source regardless of its rating |
| "排除 [source]" / "Exclude [source]" | Exclude a specific source |
| "显示所有来源" / "Show all sources" | Don't filter; show everything found |
| "不用AISEACT" / "Without AISEACT" | Skip the methodology for this query |
| "用标准搜索" / "Standard search" | Use normal search without AISEACT |

---

## Per-Session Preferences

You can set preferences for your current conversation:

```
User: "在这次对话中，请使用中等严格度，优先中文来源"
User: "For this session, use moderate filtering and prioritize academic sources"
```

These preferences will apply to subsequent AISEACT invocations in the same conversation.

---

## Platform-Specific Configuration

### Kimi Code CLI / Kimi IDE

Configuration is typically managed through the AI platform's skill management interface:

1. **Check skill settings**: Look for AISEACT in your skill registry
2. **Set invocation mode**: Enable/disable autonomous invocation
3. **Set defaults**: Configure default preference levels if supported

### Generic AI Platforms

If your platform supports skill configuration files:

```yaml
# Example configuration structure
skills:
  aiseact:
    # Invocation settings
    disable-model-invocation: true  # Set to false for autonomous mode
    
    # Default behavior
    default-strictness: moderate     # strict / moderate / minimal
    default-depth: standard          # quick / standard / thorough
    default-language-priority: global # global / chinese / english / etc.
    
    # Source preferences (if customization is supported)
    source-preferences:
      always-include: []             # List of sources to always include
      always-exclude: []             # List of sources to always exclude
```

**Note**: Actual configuration format depends on your AI platform.

---

## Recommended Configurations by Use Case

### Academic Research
```
Strictness: Strict
Depth: Thorough
Language: Based on research topic
Autonomous: Optional
```

### Business Analysis
```
Strictness: Strict
Depth: Standard to Thorough
Language: Based on company location
Autonomous: Optional
```

### General Knowledge
```
Strictness: Moderate
Depth: Quick to Standard
Language: User preference
Autonomous: Not recommended (manual use)
```

### Media Analysis / Diverse Perspectives
```
Strictness: Minimal
Depth: Standard
Language: Global
Autonomous: Not recommended
Note: Explicitly request sources from different viewpoints
```

### Breaking News / Time-Sensitive
```
Strictness: Minimal
Depth: Quick
Language: Based on event location
Autonomous: Not recommended
Note: Primary sources may not be available immediately
```

---

## Checking Current Configuration

To see your current AISEACT settings:

```
User: "AISEACT当前配置是什么?"
User: "What are my current AISEACT settings?"
```

---

*Configuration options may vary based on your AI platform's capabilities.*
