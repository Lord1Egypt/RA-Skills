---
name: export-conversation
description: Export current Claude Code conversation to markdown document with full dialogue context and model operations
---

# Export Conversation to Markdown

Extract the current Claude Code conversation from internal JSONL storage and format it as a readable markdown document showing:
- All user questions
- All model responses with associated operations (files read/edited, searches, commands, documentation lookups)
- Timeline of the conversation flow

## When to Use

Use this skill when the user asks to:
- "Export this conversation" / "Save our chat"
- "把对话保存成文档" / "保存对话记录"
- Document a problem-solving session
- Create a record of what was discussed and changed
- Generate a conversation transcript

## Process

### Step 1: Locate Current Conversation File

The conversation is stored in `~/.claude/projects/-Users-{user}-{project_path}/` as a JSONL file.

```bash
# Find the most recent conversation file
PROJECT_DIR=$(pwd | sed 's|/||g' | sed 's| |-|g')
CONV_DIR="$HOME/.claude/projects/-Users-$(whoami)-$PROJECT_DIR"
LATEST_CONV=$(ls -t "$CONV_DIR"/*.jsonl 2>/dev/null | head -1)
```

### Step 2: Use Task Agent to Parse and Extract

Launch a `general-purpose` agent to:
1. Read the JSONL conversation file
2. Parse each line as JSON
3. Extract user messages and assistant messages
4. For assistant messages, identify tool calls and operations
5. Format as markdown with clear structure

**Task prompt template:**

```
Read and parse the JSONL conversation file at `{CONVERSATION_FILE_PATH}`.

This is a Claude Code conversation log. Each line is a JSON object representing a message.

Extract ALL user messages and assistant messages in chronological order.

For each assistant message, identify:
- Files read (Read tool)
- Files edited/written (Edit/Write tools)
- Searches performed (Grep/Glob tools)
- Commands executed (Bash tool)
- Documentation lookups (Context7, web searches)
- Skills invoked (Skill tool)
- Agents dispatched (Task tool)
- Token usage for this turn (from JSONL metadata)
- Text responses to the user

Write the extracted conversation to `{OUTPUT_PATH}` in this format:

```markdown
# {Conversation Title}

## 日期: {YYYY-MM-DD}

---

### 用户 #{N}
[user message text]

### 模型 #{N}
**操作:**
- 浏览文件: [list of files read]
- 编辑文件: [list of files edited]
- 搜索: [searches performed]
- 执行命令: [bash commands]
- 查阅资料: [documentation lookups]

**回复:**
[assistant text response]

**Token 消耗:** [tokens used in this turn]

---
```

After all conversation turns, add:

## 对话统计

- **总轮次:** [total user-assistant exchanges]
- **总时长:** [duration from first to last message, e.g., "2小时15分"]
- **Token 消耗总计:** [total tokens across all turns]

## 对话评价

### 用户 Prompt 质量评分: X/10

**评分维度:**
- **问题清晰度** (3分): 问题表述是否明确、无歧义
- **技术细节精准度** (4分): 技术术语使用是否准确、错误描述是否完整
- **上下文提供** (3分): 是否提供足够背景信息（截图、报错、代码片段等）

**优点:**
- [列出用户提问做得好的地方]

**待改进:**
- [列出可以提升的地方，附具体建议]

**典型案例:**
- 好的提问示例: [引用对话中的好例子]
- 可改进示例: [引用对话中可以更精确的例子，并说明如何改进]

---

### 模型表现评分: Y/10

**评分维度:**
- **操作正确性** (2分): 读取/编辑文件、搜索、命令执行是否准确
- **上下文理解** (3分): 是否正确理解用户意图和项目状态
- **解决方案质量** (3分): 提供的方法/代码是否正确、高效、符合最佳实践
- **效率** (2分): 是否走弯路、是否及时查资料、是否避免重复操作

**优点:**
- [列出模型做得好的地方]

**问题:**
- [列出模型的失误，分析根本原因]

**典型案例:**
- 正确操作示例: [引用做得好的回合]
- 失误案例: [引用走弯路的回合，分析为什么]

---

### 改进建议

**给用户:**
1. [具体建议1]
2. [具体建议2]

**给模型:**
1. [具体建议1]
2. [具体建议2]
```

Important:
- Skip internal/system messages
- Preserve original language (Chinese/English)
- Summarize tool operations (don't dump raw JSON)
- Include ALL rounds of conversation
- Create output directory if needed
```

### Step 3: Confirm Output Location

After the agent completes:
1. Read the first 50 lines of the output file to verify format
2. Report the file path to the user
3. Provide line count and file size

## Example Usage

**User says:** "把这轮对话保存成文档"

**Agent does:**
1. Find conversation file: `~/.claude/projects/-Users-yz-dev3-demo3/ca50434c-b83d-4f88-ac4c-6b4c722cb460.jsonl`
2. Launch agent to parse and extract to `docs/2025-02-27-conversation.md`
3. Report: "对话已保存到 `docs/2025-02-27-conversation.md` (536 行)"

## Output Format

The markdown document should include:

### Header
- Title (derived from conversation topic)
- Date
- Project name/path

### Body
- Numbered dialogue turns
- User questions (verbatim)
- Model responses with:
  - **操作** section listing all tool operations
  - **回复** section with text response to user
- Preserve code blocks, images, formatting

### Footer
- Summary of files involved
- Key technical points discussed
- Total conversation turns
- **Conversation metadata:**
  - Total duration (start to end timestamp)
  - Token usage per turn (if available in JSONL)
  - Total tokens consumed
- **Conversation evaluation:**
  - User prompt quality score (1-10)
    - Clarity and specificity of questions
    - Technical detail accuracy
    - Problem description completeness
  - Model performance score (1-10)
    - Operation correctness (file reads/edits/searches)
    - Context understanding accuracy
    - Solution quality and code correctness
    - Efficiency (avoiding unnecessary detours)
  - Key strengths and weaknesses for both sides
  - Suggestions for improvement

## Tips

- Use `general-purpose` agent type (has access to all tools needed)
- Default output to `docs/{YYYY-MM-DD}-conversation.md`
- Ask user for output path if they specify one
- Handle large JSONL files (read in chunks if needed)
- Preserve markdown formatting in original messages
- Don't include this skill's own invocation in the exported conversation
