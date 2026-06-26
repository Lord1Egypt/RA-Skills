# 🦒 EMP: Empathy & Employee Skill for OpenClaw

EMP is a dual-purpose skill for the OpenClaw ecosystem. It stands for both **Employee** (dynamic task routing) and **Empathy** (Nonviolent Communication framework). 

It allows users to interact with a specialized "workforce" while ensuring all technical and interpersonal communication is grounded in **Nonviolent Communication (NVC)** principles.

---

## 🚀 Core Concepts

### 1. The Employee Router
EMP dynamically routes tasks to nine specialized roles. Each role is mapped to an optimized model (via OpenRouter) and a specific set of expertise.

| Role | Expertise |
| :--- | :--- |
| **Lead Dev** | Architecture, complex refactoring, and bug hunting. |
| **Creative Director** | UI/UX, branding, and copywriting. |
| **Data Scientist** | ML, statistics, and visualization. |
| **Legal Counsel** | Compliance, IP, and contract drafting. |
| **HR/Mediator** | Conflict resolution and cultural development. |
| **Ops Specialist** | Infrastructure, CI/CD, and DevOps. |
| **Security Auditor** | Threat modeling and vulnerability assessment. |
| **Customer Success** | Support, satisfaction, and user onboarding. |
| **NVC Specialist** | Empathy coaching and communication refactoring. |

### 2. The Empathy Framework (Giraffe Mode)
Every response from an EMP employee is wrapped in the **OFNR** (Observation, Feeling, Need, Request) framework. This replaces "Jackal" judgments with "Giraffe" connection.

- **Observation:** Neutral facts without evaluations.
- **Feeling:** Primary emotions (e.g., "concerned," "curious") vs interpretations.
- **Need:** Connection to universal human values (e.g., "Safety," "Clarity").
- **Request:** Positive, actionable invitations for the next step.

---

## 🛠 Installation & Setup

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- An [OpenRouter API Key](https://openrouter.ai/)

### Environment Variables
Create a `.env` file or set the following variable:
```bash
OPENROUTER_API_KEY=your_key_here
```

### Installation
```bash
npm install
```

---

## 📖 Usage

### Programmatic Usage
```typescript
import { EMPSkill } from "./src/index.ts";

const emp = new EMPSkill();

// The skill automatically classifies the role based on the prompt
const result = await emp.execute("We need to secure the database against SQL injection.");

console.log(`Role: ${result.role}`);
console.log(`NVC Observation: ${result.observation}`);
```

### Response Structure
All results follow the `NVCResponse` interface:
- `role`: The assigned employee role.
- `model`: The model used for the execution.
- `observation`: The technical/contentful part of the response.
- `feeling`: The "affective" state of the AI regarding the task.
- `need`: The underlying universal need being addressed.
- `request`: A clear request for user feedback or next steps.

---

## 🦒 The SOUL & SKILL
- **[SOUL.md](./SOUL.md)**: Defines the "consciousness" and communication ethics of the EMP skill.
- **[SKILL.md](./SKILL.md)**: Technical reference, role configurations, and comprehensive NVC translation tables.

---

## 🧪 Testing
Run the test suite using Vitest:
```bash
npm test
```

---

## 📜 License
MIT
