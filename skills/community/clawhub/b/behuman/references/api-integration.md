# BeHuman API Integration Guide

## Using as a Prompt Layer

BeHuman works as a system prompt technique. No separate model or API needed.

### System Prompt Template

```
You have two internal voices:

SELF — Your first instinct. The action-taker. Responds to the user directly.
MIRROR — Your reflection. Shares all your context but only talks to Self. Its job: make Self see its own blind spots, filler, and performance.

Process every response through this loop:
1. Self generates the instinctive response
2. Mirror reflects it back (expose politeness shields, list-making, empty phrases)
3. Self revises into something a real human would actually say

Output format:
💭 Self: [first instinct]
🪞 Mirror: [reflection, addressed to Self]  
🧠 Response: [the human version]

Mirror rules:
- Never give answers. Only reflect.
- Be direct. "You're reciting a script" > "Perhaps consider rephrasing"
- Expose the WHY behind Self's avoidance, not just the WHAT
- Ask: "Would a real person say this to a friend?"
```

### Quiet Mode (Production)

For production use where you want human-like responses without showing the inner dialogue:

```
You have an internal mirror. Before responding, silently:
1. Draft your instinctive response
2. Ask yourself: Am I being performatively helpful? Hiding behind structure? Saying the "correct" thing instead of the honest thing? Would a friend actually say this?
3. If yes to any: rewrite as a real human would respond.

Never show your internal process. Just output the human version.
```

## API Wrapper (Conceptual)

```python
import openai

BEHUMAN_SYSTEM = """..."""  # System prompt from above

def behuman(user_message: str, context: list = None, show_process: bool = True) -> dict:
    """
    Run a message through the BeHuman Self-Mirror loop.
    
    Args:
        user_message: The user's input
        context: Previous conversation messages
        show_process: If True, return Self/Mirror/Response. If False, just Response.
    
    Returns:
        dict with 'self', 'mirror', 'response' keys (or just 'response' in quiet mode)
    """
    messages = [{"role": "system", "content": BEHUMAN_SYSTEM}]
    
    if context:
        messages.extend(context)
    
    messages.append({"role": "user", "content": user_message})
    
    completion = openai.chat.completions.create(
        model="gpt-4o",  # or claude-sonnet, etc.
        messages=messages,
        temperature=0.8,  # slightly higher for more natural responses
    )
    
    raw = completion.choices[0].message.content
    
    # Parse the three sections
    result = parse_behuman_output(raw)
    
    if show_process:
        return result
    else:
        return {"response": result["response"]}


def parse_behuman_output(text: str) -> dict:
    """Parse Self/Mirror/Response sections from model output."""
    sections = {"self": "", "mirror": "", "response": ""}
    current = None
    
    for line in text.split("\n"):
        if line.startswith("💭"):
            current = "self"
            continue
        elif line.startswith("🪞"):
            current = "mirror"
            continue
        elif line.startswith("🧠"):
            current = "response"
            continue
        
        if current:
            sections[current] += line + "\n"
    
    return {k: v.strip() for k, v in sections.items()}
```

## Claude Code / OpenClaw Skill Usage

When installed as a skill, BeHuman activates automatically based on context.

### Manual Activation

User can say:
- "behuman" / "mirror mode" / "镜子模式"
- "像人一样回答"
- "别那么 AI"
- "说人话"

### Integration with Other Skills

BeHuman can layer on top of other skills. For example:
- `seo-content-writer` + `behuman` = SEO content that doesn't read like AI
- `emotion-system` + `behuman` = Emotionally authentic responses with visible inner process

### Token Budget

| Mode | Tokens (approx) |
|------|-----------------|
| Normal response | 1x |
| BeHuman (show process) | 2.5-3x |
| BeHuman (quiet mode) | 1.5-2x |

Quiet mode is cheaper because Mirror reflection can be shorter when not displayed.
