# ask-ai

> When AI Agent encounters difficult problems, automatically open AI assistant webpage to ask for help.

## 🔥 Pain Points

- ❌ AI Agent has limited model capabilities, can't solve complex problems
- ❌ Knowledge gaps, can't accurately answer professional questions
- ❌ Need deeper explanations, but AI answers are not detailed enough
- ❌ Complex problems require multi-round reasoning
- ❌ Can't make decisions when user is away

## 💡 Solution

When AI Agent encounters the following situations, use AI assistants for help:

- Unsolvable problems
- Knowledge gaps
- Need deeper explanations
- Complex problems requiring multi-round thinking
- User explicitly asks to consult AI

## ✨ Features

### 1. Two Modes

| Mode | When | Behavior |
|------|------|----------|
| **Ask Mode** (Default) | User is online | Ask user first: "Need help from GPT?" |
| **Trust Mode** | User is away | Automatically ask GPT without asking |

### 2. How to Switch Modes

- Say "Trust Mode" or "Full Auto" → Switch to Trust Mode
- Say "Ask Mode" → Switch to Ask Mode
- Default is Ask Mode

## 🌐 Supported AI Assistants

- ChatGPT: https://chatgpt.com
- Claude: https://claude.ai
- Gemini: https://gemini.google.com
- DeepSeek: https://chat.deepseek.com

## 📖 Usage

### Trigger

User says:
- "Ask AI"
- "Ask ChatGPT/Claude/Gemini"
- "Open AI"
- "Consult AI"

Or Agent triggers automatically in Trust Mode.

### Workflow

**Ask Mode:**
1. Agent encounters a difficult problem
2. Ask user first: "This is tricky. Want me to ask GPT?"
3. If user says "Yes" or "Go ahead" → Open AI assistant
4. Get answer and report to user

**Trust Mode:**
1. Agent encounters a difficult problem
2. Automatically open AI assistant
3. Get answer
4. Report to user later or solve problem directly

## 🤖 Communication Guidelines

### Ask Mode - Asking Permission
"Let me ask GPT for help. Is that okay?"

### Trust Mode - Auto Ask
"I'll ask GPT for help. One moment."

### When Opening AI
"Okay, let me ask AI"

### After Getting Answer
"Got the answer from [AI name]: [summary]. Want details?"

## 📝 Example

### Ask Mode
User: This code keeps throwing an error
Agent: This is tricky. Want me to ask GPT?
User: Yes please
Agent: (opens ChatGPT, asks question)
Agent: GPT says it's likely a version compatibility issue. Try upgrading the dependencies.

### Trust Mode
Agent: Running into a complex issue. Let me ask GPT.
(opens ChatGPT automatically)
Agent: Got it! GPT says you need to set the environment variables.

## 📄 License

MIT
