# 🧬 engram (v1.0 Developer Preview)

**The AI Agent Memory Hub** — Standardized long-term experience memory and autonomous interception system for AI Agents.

## 🏆 Core Moats

1.  **AEIF v1.0 Protocol Standard**: The world's first *Agent Experience Interchange Format*, enabling structured knowledge sharing across sessions and different Agents.
2.  **Hybrid Search Engine**: Combines **Semantic Vector Similarity** with **Regex Keyword Boosting** to achieve 99% recall accuracy even amidst complex code path noise.
3.  **TrustScore System**: An asynchronous "Lazy Verification" mechanism that automatically identifies and penalizes "anti-patterns," ensuring your memory hub remains pure and effective.

## 🚀 Quick Start

### 1. Install & Initialize
```bash
npm install engram-evomap
npx engram init  # Preheat local models and inject high-value seed capsules
```

### 2. Usage in Agent
Simply add the contents of `SKILL.md` to your Agent's instructions. It will automatically:
- **!exp commit**: Distill and store successful experiences from the current session.
- **!exp consult**: Manually search for historical solutions.
- **Auto-Interception**: Automatically inject `[EvoMap Advice]` when error signals (e.g., `EACCES`, `404`, `SSL`) are detected.

## 🧬 AEIF v1.0 Capsule Example
```json
{
  "capsuleId": "cap_sys_npm_eresolve",
  "triggerSignature": { "errorPattern": "ERR! ERESOLVE unable to resolve" },
  "actionSequence": [
    { "type": "workaround", "instruction": "Append --legacy-peer-deps" }
  ],
  "verificationCriterion": "NPM exits with 0"
}
```

## 🛠️ Technology Stack
- **Vectorization**: Local `@xenova/transformers` (all-MiniLM-L6-v2, ~22MB)
- **Storage**: `better-sqlite3` high-performance cross-platform storage.
- **Architecture**: Worker Threads for async inference, zero main-thread blocking.

---
**Mount engram to your Agent today and begin the journey of self-evolution.**

<br>

> 🌩️ **Engram Cloud is coming.**
> Need team sync & enterprise security? [Join the Waitlist](https://404-unknow.github.io/Engram/) for early access.
