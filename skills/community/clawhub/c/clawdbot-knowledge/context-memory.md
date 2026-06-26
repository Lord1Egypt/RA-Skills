# Context & Memory Reference

## Overview

"Context" refers to everything OpenClaw sends to the model for a run, limited by the model's context window. "Memory" can be stored on disk and loaded later; context is what's currently in the model's window.

## Context vs Memory

### Context
- **Definition**: Everything the model receives for a run
- **Limitation**: Limited by model's context window (token limit)
- **Duration**: Exists only during current model run
- **Content**: System prompt, conversation history, tool results, etc.

### Memory  
- **Definition**: Information stored on disk for later use
- **Limitation**: Limited only by storage space
- **Duration**: Persistent across sessions
- **Content**: Long-term knowledge, daily logs, curated memories

**Mental Model**: Context is like working memory - what you're thinking about right now. Memory is like long-term storage - what you know and can recall when needed.

## What Counts to Context Window

### Included Components
Everything the model receives counts toward context window, including:

#### System Prompt (All Sections)
- Tooling section with current tools
- Security guidelines and recommendations
- Capabilities and skills information
- Workspace and documentation references
- Bootstrap file injections
- Runtime information and metadata
- All other system prompt sections

#### Conversation History
- User messages and assistant responses
- Tool calls and tool results
- File attachments and uploads
- Image and audio transcriptions
- All conversational exchanges

#### Tool Execution Data
- Tool call parameters and arguments
- Tool execution results and outputs
- Tool error messages and debugging info
- Tool execution metadata and timing

#### Processing Artifacts
- Compaction summaries and condensed history
- Session cleanup and maintenance artifacts
- Processing overhead and wrapper data
- Model-specific formatting and padding

#### Hidden Content
- Provider "wrappers" or hidden headers
- Model-specific formatting requirements
- Protocol overhead and metadata
- Internal processing markers

**Note**: Hidden content isn't visible to users but still consumes context tokens.

## Context Inspection Commands

### /status
**Purpose**: Quick view of "How full is my window?" + session settings

**Usage**: `/status`

**Output**: 
- Context window usage percentage
- Current session settings
- Model information
- Token count summary

**When to Use**: Quick context health check, monitor usage trends

### /context list  
**Purpose**: What gets injected + approximate sizes (per file + total)

**Usage**: `/context list`

**Output**:
```
🧠 Context breakdown
Workspace: <workspaceDir>
Bootstrap max/file: 20,000 chars
Sandbox: mode=non-main sandboxed=false
System prompt (run): 38,412 chars (~9,603 tok) 
(Project Context 23,901 chars (~5,976 tok))
Injected workspace files:
- AGENTS.md: OK | raw 1,742 chars (~436 tok) | injected 1,742 chars (~436 tok)
- SOUL.md: OK | raw 912 chars (~228 tok) | injected 912 chars (~228 tok)
- TOOLS.md: TRUNCATED | raw 54,210 chars (~13,553 tok) | injected 20,962 chars (~5,241 tok)
- IDENTITY.md: OK | raw 211 chars (~53 tok) | injected 211 chars (~53 tok)
- USER.md: OK | raw 388 chars (~97 tok) | injected 388 chars (~97 tok)
- HEARTBEAT.md: MISSING | raw 0 | injected 0
- BOOTSTRAP.md: OK | raw 0 chars (~0 tok) | injected 0 chars (~0 tok)
Skills list (system prompt text): 2,184 chars (~546 tok) (12 skills)
Tools: read, edit, write, exec, process, browser, message, sessions_send, …
Tool list (system prompt text): 1,032 chars (~258 tok)
Tool schemas (JSON): 31,988 chars (~7,997 tok) (counts toward context; not shown as text)
Tools: (same as above)
Session tokens (cached): 14,250 total / ctx=32,000
```

**When to Use**: Understand what's consuming context, identify large components

### /context detail
**Purpose**: More detailed breakdown: size per file, per tool, per skill entry, system prompt size

**Usage**: `/context detail`

**Output**:
```
🧠 Context breakdown (detailed)…
Top skills (prompt entry size):
- frontend-design: 412 chars (~103 tok)
- oracle: 401 chars (~101 tok)
… (+10 more skills)

Top tools (schema size):
- browser: 9,812 chars (~2,453 tok)  
- exec: 6,240 chars (~1,560 tok)
… (+N more tools)
```

**When to Use**: Deep analysis of context usage, identify specific resource consumers

### /usage tokens
**Purpose**: Add usage stats footer to normal responses

**Usage**: `/usage tokens`

**Output**: Normal response with token usage footer:
```
[Response content...]

---
Tokens: 1,234 used | Cost: $0.012 | Context: 45% full
```

**When to Use**: Monitor costs and usage during conversations

### /compact
**Purpose**: Summarize older historical data in compact entry to save window space

**Usage**: `/compact`

**Behavior**: 
- Analyzes conversation history
- Creates summary of older exchanges
- Replaces detailed history with compact summary
- Preserves recent conversation detail

**When to Use**: Context window nearly full, need to continue conversation

## Context Window Limits

### Model-Specific Limits
Different models have different context window sizes:

| Model | Context Window | Approx Tokens |
|-------|---------------|---------------|
| GPT-3.5 | 4K | ~4,000 tokens |
| GPT-4 | 8K/32K/128K | ~8K/32K/128K tokens |
| Claude | 100K/200K | ~100K/200K tokens |
| Local Models | Variable | Model-dependent |

### Context Management Strategies

#### Automatic Compaction
- **Trigger**: When context approaches limit
- **Action**: Summarize older history, preserve recent conversation
- **Result**: Frees up space for continued conversation

#### Manual Compaction
- **Command**: `/compact`
- **Control**: User-initiated context cleanup
- **Precision**: Can target specific conversation ranges

#### File Size Limits
- **Bootstrap Files**: Limited by `agents.defaults.bootstrapMaxChars` (default 20,000)
- **Large Files**: Automatically truncated with truncation marker
- **Skills**: Loaded on-demand to conserve context

#### Tool Schema Optimization
- **Large Schemas**: Some tools have large JSON schemas
- **Impact**: Can consume significant context
- **Monitoring**: Use `/context detail` to identify large tool schemas

## Memory Architecture

### Memory Types

#### Daily Notes (`memory/YYYY-MM-DD.md`)
- **Purpose**: Raw logs of what happened each day
- **Creation**: Create `memory/` directory if needed
- **Content**: Chronological record of events, decisions, conversations
- **Usage**: Read today + yesterday at session start
- **Format**: Free-form text, can include timestamps and structure

#### Long-Term Memory (`MEMORY.md`)
- **Purpose**: Curated memories like human's long-term memory
- **Loading**: ONLY in main session (direct chats with human)
- **Security**: DO NOT load in shared contexts (Discord, group chats)
- **Content**: Significant events, thoughts, decisions, opinions, lessons learned
- **Maintenance**: Review daily files and update with what's worth keeping

### Memory Loading Rules

#### MEMORY.md Security Restrictions
- **Main Session Only**: Load only in direct chats with human
- **Shared Contexts**: Never load in group chats or shared contexts
- **Reason**: Contains personal context that shouldn't leak to strangers
- **Compliance**: Agent must respect these restrictions

#### Daily File Reading
- **Automatic**: Read today and yesterday's memory files at session start
- **Optional**: Can read additional files as needed
- **Purpose**: Provide recent context and continuity
- **Scope**: Session-specific memory and context

### Memory Management Best Practices

#### Write It Down - No "Mental Notes"!
- **Memory is Limited**: If you want to remember something, WRITE IT TO A FILE
- **Session Boundaries**: "Mental notes" don't survive session restarts. Files do.
- **Explicit Storage**: When someone says "remember this" → update appropriate file
- **Lesson Learning**: When you learn a lesson → update AGENTS.md, TOOLS.md, or skill
- **Mistake Documentation**: When you make a mistake → document so future-you doesn't repeat it
- **Principle**: Text > Brain 📝

#### Memory Maintenance (During Heartbeats)
Periodically (every few days), use heartbeat to:
1. **Read Recent Files**: Read through recent `memory/YYYY-MM-DD.md` files
2. **Identify Significance**: Identify significant events, lessons, or insights worth keeping long-term
3. **Update MEMORY.md**: Update `MEMORY.md` with distilled learnings
4. **Remove Outdated Info**: Remove outdated info from MEMORY.md that's no longer relevant

**Think of it like**: A human reviewing their journal and updating their mental model. Daily files are raw notes; MEMORY.md is curated wisdom.

#### Memory File Organization
```
memory/
├── 2026-02-07.md     # Today's memory
├── 2026-02-06.md     # Yesterday's memory  
├── 2026-02-05.md     # Earlier memory
└── MEMORY.md         # Curated long-term memory
```

## What /context Actually Reports

### System Prompt Sources
`/context` prefers the latest system prompt report created by the system:

#### System Prompt (run)
- **Source**: From last embedded (tool-capable) run
- **Storage**: Captured and stored in session memory
- **Accuracy**: Most accurate representation of actual context

#### System Prompt (estimate)  
- **Source**: Dynamically calculated when no execution report exists
- **Trigger**: CLI backend execution or missing run report
- **Accuracy**: Estimated but generally reliable

### Reporting Behavior
In both cases, `/context` reports:
- **Sizes and Major Contributors**: Approximate sizes of context components
- **Token Counts**: Estimated token usage for major sections
- **File Status**: Which files are loaded, truncated, or missing
- **Tool Information**: Available tools and their schema sizes

### Limitations
- **No Complete Prompt**: Never shows complete system prompt or tool schemas
- **Estimation**: Some values are estimates, not exact counts
- **Dynamic**: Context can change during execution
- **Model Dependencies**: Exact limits depend on specific model

## Context Optimization Strategies

### Proactive Optimization

#### File Size Management
- **Large Bootstrap Files**: Reduce size or move to references
- **Tool Schema Optimization**: Use tools with smaller schemas when possible
- **Skill Loading**: Load skills on-demand, not all at once

#### Conversation Management
- **Regular Compaction**: Use `/compact` before context becomes critical
- **Selective History**: Keep only relevant conversation history
- **Memory Offloading**: Move important information to memory files

#### Model Selection
- **Larger Context**: Choose models with larger context windows for complex tasks
- **Cost Consideration**: Balance context needs with cost constraints
- **Performance**: Consider model performance alongside context size

### Reactive Optimization

#### When Context is Full
1. **Use `/compact`**: Summarize older conversation
2. **Reduce Bootstrap Files**: Remove or truncate large files
3. **Change Model**: Switch to model with larger context
4. **Split Conversation**: Start new session for complex topics

#### Emergency Measures
- **Minimal Mode**: Use prompt mode "minimal" for subagents
- **Tool Reduction**: Disable unnecessary tools
- **File Exclusion**: Exclude non-essential bootstrap files

## Troubleshooting Context Issues

### Common Problems

#### Context Window Full
- **Symptoms**: Model refuses to respond, responses cut off mid-sentence
- **Solution**: Use `/compact`, reduce file sizes, increase model context limit
- **Prevention**: Monitor context usage with `/status`

#### Large File Impact
- **Symptoms**: Single file consuming excessive context
- **Solution**: Edit file to reduce size, move to references
- **Prevention**: Check file sizes with `/context list`

#### Tool Schema Overhead
- **Symptoms**: Tools with large JSON schemas consuming context
- **Solution**: Use alternative tools, reduce tool usage
- **Prevention**: Monitor tool schema sizes with `/context detail`

#### Memory Loading Issues
- **Symptoms**: MEMORY.md not loading in main session
- **Solution**: Check file permissions, verify session type
- **Prevention**: Follow memory loading rules strictly

### Debug Commands
```bash
# Check current context usage
openclaw context status

# Detailed context breakdown
openclaw context detail

# Compact conversation history
openclaw context compact

# Show memory file status
openclaw memory list

# Test memory loading
openclaw memory test
```

### Context Monitoring
Regular monitoring helps prevent context issues:
- **Before Complex Tasks**: Check context with `/status`
- **During Long Conversations**: Monitor usage trends
- **After Adding Files**: Verify impact with `/context list`

## Best Practices

### Context Management
1. **Monitor Regularly**: Use `/status` to track context usage
2. **Compact Proactively**: Use `/compact` before reaching limits
3. **Optimize Files**: Keep bootstrap files concise and relevant
4. **Choose Models Wisely**: Select appropriate context size for tasks

### Memory Management  
1. **Write Everything**: Never rely on "mental notes"
2. **Review Regularly**: Update MEMORY.md from daily files
3. **Maintain Security**: Never load MEMORY.md in shared contexts
4. **Keep Organized**: Use consistent file organization

### Performance Optimization
1. **Balance Context and Cost**: Choose appropriate models
2. **Use Tools Efficiently**: Select tools with smaller schemas
3. **Load Skills On-Demand**: Don't load all skills simultaneously
4. **Monitor Performance**: Track context usage and response times