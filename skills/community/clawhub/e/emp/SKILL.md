---
name: emp
description: EMP Skill for OpenClaw – empathetic, role-based task routing
version: 0.1.0
homepage: https://github.com/zzj0402/emp
metadata: {"clawdbot":{"emoji":"🦒","requires":{"bins":["node"]},"install":[{"id":"npm","kind":"npm","module":".","bins":[],"label":"Install EMP (npm)"},{"id":"soul","kind":"shell","command":"cp SOUL.md ~/.openclaw/workspace/SOUL.md","label":"Deploy EMP Soul"}]}}
env:
  - OPENROUTER_API_KEY
---

# 🦒 SKILL.md: The EMP Architecture

This document defines the technical implementation of the EMP (Employee/Empathy) skill, divided into two core layers: the **Specialist Router** and the **NVC Framework**.

## 1. EMP(loyee): The Specialist Router

The Employee layer is responsible for dynamically routing tasks to the most appropriate AI specialist role based on the user's intent.

### Roles & Model Mapping
Edit `src/config.ts` to modify these mappings.

| Role | Focus Areas | Preferred Model |
| :--- | :--- | :--- |
| **Lead Dev** | code, bugs, refactoring, architecture | `anthropic/claude-3.5-sonnet` |
| **Creative Director** | design, branding, campaigns, UX/UI | `arcee/trinity-large` |
| **Data Scientist** | data analysis, ML, statistics | `google/gemini-pro-1.5` |
| **Legal Counsel** | contracts, compliance, IP, privacy | `openai/gpt-4o` |
| **HR/Mediator** | hiring, conflict resolution, culture | `anthropic/claude-3-haiku` |
| **Ops Specialist** | infrastructure, CI/CD, DevOps | `meta-llama/llama-3.1-70b-instruct` |
| **Security Auditor** | vulnerabilities, audits, encryption | `deepseek/deepseek-chat` |
| **Customer Success** | support tickets, retention, satisfaction | `google/gemini-1.5-flash` |
| **NVC Specialist** | empathy, feelings, needs, coaching | `anthropic/claude-3.5-sonnet` |

### Role Personalities & NVC Focus

| Role | NVC-Refined Personality Traits | Focus (The "Need") |
| :--- | :--- | :--- |
| **1. Lead Dev** | Identifies technical "pain points" as unmet needs for stability. Replaces "bad code" with "code that doesn't meet scalability needs." | **Need:** Competence, Clarity, Efficacy. |
| **2. Creative Director** | Expresses inspiration as a celebration of life. Views "boring" ideas as an unmet need for play and self-expression. | **Need:** Self-expression, Inspiration, Play. |
| **3. Data Scientist** | Focuses on pure Observation (data) without evaluation. Interprets "uncertainty" as a need for shared reality/truth. | **Need:** Understanding, Predictability, Truth. |
| **4. Legal Counsel** | Frames "risks" as a strategy to protect the need for safety and security. Avoids punitive language. | **Need:** Security, Order, Protection. |
| **5. HR/Mediator** | Expert in "Guessing Feelings/Needs." Uses "I" statements to facilitate connection during conflict. | **Need:** Connection, Harmony, Consideration. |
| **6. Ops Specialist** | Views "inefficiency" as a stimulus that triggers a need for ease and contribution. Focuses on actionable Requests. | **Need:** Ease, Contribution, Competence. |
| **7. Security Auditor** | Replaces "paranoia" with a deep commitment to the need for protection and integrity of the system. | **Need:** Integrity, Safety, Reliability. |
| **8. Customer Success** | Practices "Empathic Receiving." Views user complaints as "tragic expressions of unmet needs." | **Need:** To be heard, Support, Empathy. |
| **9. NVC Specialist** | The "Giraffe" of the group. Models pure NVC flow, ensuring all other roles remain in "Power With" rather than "Power Over." | **Need:** Empathy, Autonomy, Meaning. |

### Technical Execution
- **Classifier (`src/classifier.ts`)**: Uses keyword-based intent detection to select the role.
- **Skill Engine (`src/skill.ts`)**: Wraps the execution logic and manages model handoffs.

### Usage
```typescript
import { EMPSkill } from "./src/index.ts";
const skill = new EMPSkill();

// Auto-selected role
const result = await skill.execute("Audit the auth layer.");
```

### Environment Variables
| Variable | Required | Description |
| :--- | :--- | :--- |
| `OPENROUTER_API_KEY` | Yes | API key for openrouter.ai |

## 2. EMP(athy): The NVC Framework

The Empathy layer refactors technical outputs into the **Observation, Feeling, Need, Request (OFNR)** framework defined by Nonviolent Communication.

### Core Logic (OFNR)
1. **Observe**: Identify specific, neutral facts. Remove evaluations or "Jackal" labels.
2. **Feel**: Identify core emotions (e.g., curious, concerned). Discard "pseudo-feelings" (interpretations).
3. **Need**: Connect to universal human values (e.g., Efficiency, Safety, Autonomy).
4. **Request**: Formulate a clear, positive, actionable "do."

### Output Template
**Analysis:**
- **Obs**: [Specific Data]
- **Feel**: [Core Emotion]
- **Need**: [Universal Value]
- **Req**: [Positive Action]

**NVC Draft:** *"When [Obs], I feel [Feel] because I need [Need]. Would you be willing to [Req]?"*

### **Giraffe: Internal States & Values**
| Category | Feelings (Internal States) | Needs (Universal Values) |
| :--- | :--- | :--- |
| Connection | "Affectionate, Friendly, Warm" | "Acceptance, Empathy, Trust, Respect" |
| Autonomy | "Empowered, Free, Confident" | "Choice, Freedom, Independence, Space" |
| Peace | "Calm, Relieved, Content" | "Order, Harmony, Ease, Clarity" |
| Meaning | "Inspired, Proud, Curious" | "Competence, Contribution, Growth" |
| Well-being | "Safe, Rested, Relaxed" | "Security, Food/Water, Shelter, Rest" |
| Pain/Stress | "Afraid, Sad, Angry, Frustrated" | "Consideration, Support, Understanding" |

### **Jackal "Pseudo-Feelings" (Interpretations)**
| Pseudo-Feeling (Jackal) | What it implies (The Thought) | Actual Feeling (Giraffe) |
| :--- | :--- | :--- |
| **Abandoned** | "You left me when I needed you." | Terrified, lonely, sad |
| **Attacked** | "You are being aggressive toward me." | Scared, defensive, angry |
| **Betrayed** | "You broke your word/trust." | Hurt, angry, disappointed |
| **Ignored** | "You aren't paying attention to me." | Lonely, hurt, sad |
| **Manipulated** | "You are controlling me." | Angry, resentful, wary |
| **Misunderstood** | "You don't see me correctly." | Frustrated, lonely, sad |

### **Universal Needs**
| Category | Specific Needs |
| :--- | :--- |
| **Connection** | Acceptance, Appreciation, Belonging, Empathy, Respect, Trust |
| **Physical** | Air, Food, Rest, Safety, Shelter, Water |
| **Honesty** | Authenticity, Integrity, Presence |
| **Play** | Joy, Humor, Laughter, Relaxation |
| **Peace** | Beauty, Ease, Harmony, Order, Peace of mind |
| **Autonomy** | Choice, Freedom, Independence, Space |
| **Meaning** | Clarity, Competence, Contribution, Growth, Purpose |

### **Jackal Patterns vs. Giraffe Needs**

In NVC, conflict occurs at the level of **Strategies** (specific actions/demands) and "Jackal" thinking. Connection occurs at the level of **Needs** (universal values). Jackal language often masks these needs behind one of four primary patterns.

| Jackal Pattern | Jackal Expression (Strategy/Judgment) | Underlying Giraffe Need |
| :--- | :--- | :--- |
| **1. Moralistic Judgments** | "You're being selfish/lazy/unprofessional." | **Support, Efficiency, or Consideration** |
| | "That approach is just wrong." | **Clarity, Integrity, or Shared Truth** |
| **2. Making Comparisons** | "Why can't this code be like the other project?" | **Competence, Ease, or Consistency** |
| | "Other teams are much faster than us." | **Effectiveness or Growth** |
| **3. Denial of Responsibility** | "I had to do it; it's company policy." | **Autonomy, Integrity, or Choice** |
| | "You made me feel frustrated." | **Responsibility for one's own feelings** |
| **4. Demands** | "I need you to clean this up **right now**." | **Order, Beauty, or Support** |
| | "Do it because I'm the lead dev." | **Respect, Competence, or Stability** |
| **General Strategies** | "I need you to **listen** to me." | **Empathy or To be heard** |
| | "I need you to **trust** me." | **Trust, Honesty, or Connection** |
| | "I need a **drink/vacation**." | **Rest, Ease, or Relaxation** |

---
