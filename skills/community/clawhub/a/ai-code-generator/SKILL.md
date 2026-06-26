---
name: ai-code-generator
description: AI code generator using Plan-and-Solve + ReAct for generating complete, runnable code from requirements and specifications.
---

# AI Code Generator

AI-powered code generation tool that combines structured planning (Plan-and-Solve) with tool use (ReAct) to generate complete, production-ready code from natural language requirements.

---

## Features

### 📝 Requirement Analysis

- **Understanding**: Parse natural language requirements
- **Clarification**: Ask clarifying questions when needed
- **Specification**: Generate technical specification

### 🏗️ Code Generation

- **Full-stack Support**: Frontend, backend, database
- **Multiple Languages**: JavaScript, Python, TypeScript, Go
- **Best Practices**: Clean code, design patterns
- **Complete Projects**: Full project structure

### 🔧 Tool Integration

- **File Generation**: Create multiple files
- **Dependency Management**: package.json, requirements.txt
- **Testing**: Generate unit tests
- **Documentation**: README, API docs

---

## Usage

### Basic Code Generation

```javascript
const generator = new CodeGenerator();

const project = await generator.generate({
  requirements: 'Create a REST API for a todo app with user authentication',
  language: 'javascript',
  framework: 'express',
  database: 'mongodb'
});

console.log(project.files);
console.log(project.instructions);
```

### Advanced Options

```javascript
const generator = new CodeGenerator({
  style: 'professional',
  includeTests: true,
  includeDocs: true,
  verbose: true
});

const project = await generator.generate({
  requirements: 'Build a real-time chat application',
  language: 'typescript',
  framework: 'nestjs',
  database: 'postgresql',
  features: ['websocket', 'jwt-auth', 'message-history']
});
```

---

## Example Output

```
project/
├── src/
│   ├── controllers/
│   │   └── todo.controller.js
│   ├── models/
│   │   └── todo.model.js
│   ├── routes/
│   │   └── todo.routes.js
│   └── middleware/
│       └── auth.middleware.js
├── tests/
│   └── todo.test.js
├── package.json
├── .env.example
└── README.md
```

---

## Workflow

```
User Requirements
    ↓
Plan-and-Solve Agent
    ├─ Phase 1: Analyze requirements
    ├─ Phase 2: Design architecture
    ├─ Phase 3: Plan file structure
    └─ Phase 4: Generate code
    ↓
ReAct Agent (for each file)
    ├─ Research best practices
    ├─ Generate code
    ├─ Review and fix
    └─ Write to file
    ↓
Complete Project
```

---

## Installation

```bash
clawhub install ai-code-generator
```

---

## License

MIT

---

## Version

1.0.0

---

## Created

2026-04-02
