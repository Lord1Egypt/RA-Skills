
# 🎭 Devil's Advocate - OpenClaw Skill

Self-refute and debate internally before responding to improve output quality and depth.

## 💡 Design Philosophy

Have you ever encountered this situation: AI gives an answer that sounds reasonable, but upon closer inspection, there are obvious issues?

The core idea of this skill is: **Let AI debate with itself first, then give you the answer.**

Through internal pro and con discussions, AI can:
- Discover logical flaws in its own reasoning
- Consider overlooked edge cases
- Identify potential risks and problems
- Provide more balanced and comprehensive perspectives

## 🔄 How It Works

```
User Question
    ↓
[Pro] Draft initial answer
    ↓
[Con] Self-refute, challenge flaws
    ↓
[Integrate] Synthesize perspectives, refine answer
    ↓
Output final response
```

## 📋 Self-Refutation Checklist

During internal thinking, AI will check each item:

| Check Item | Description |
|-----------|-------------|
| 🧠 Logic Verification | Is the reasoning chain complete? |
| 🤔 Assumption Challenging | Are implicit assumptions necessarily valid? |
| ⚠️ Edge Cases | Are there any exceptions? |
| 🚨 Risk Assessment | What are the potential risks? |
| ❌ Counterexample Search | Are there counterexamples that can disprove? |
| 🔄 Alternative Approaches | Are there other options? |

## 🚀 Quick Start

### Installation

```powershell
# Copy to OpenClaw skills directory
xcopy /E /I devil-advocate %USERPROFILE%\.openclaw\skills\devil-advocate

# Restart Gateway
openclaw restart
```

### Usage

Automatically effective after installation, no additional configuration needed!

## 📁 Directory Structure

```
devil-advocate/
├── SKILL.md      # Skill definition
├── CLAUDE.md      # Core instructions (auto-injected)
├── README.md     # This file
├── INSTALL.md    # Installation guide
└── EXAMPLES.md   # Usage examples
```

## ✨ Effect Comparison

### Without Refutation
&gt; "Use MongoDB, it's more flexible and has higher development efficiency."

### With Refutation
&gt; "It depends on your specific needs:
&gt;
&gt; **MongoDB is good for:** Unstructured data, rapid prototyping...
&gt; **PostgreSQL is good for:** Need transactions, complex queries...
&gt;
&gt; Things to consider: Team skills, data consistency requirements, existing tech stack...
&gt;
&gt; Suggestion: If unsure, start with PostgreSQL as it also supports JSON fields."

## 🎯 Use Cases

- Technical solution selection
- Architecture design decisions
- Code optimization suggestions
- Problem root cause analysis
- Any scenario requiring deep thinking

## 📚 Related Concepts

- **Critical Thinking**
- **Red Teaming**
- **Devil's Advocate**
- **First Principles Thinking**

---

**New skill created successfully!** 🎉

📝 Review Note:
- Please check if skill functionality meets expectations
- Verify security risks and permission settings
- Confirm before putting into production use
