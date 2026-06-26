#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取项目根目录（当前工作目录）
const projectRoot = process.cwd();
const claudeDir = path.join(projectRoot, '.claude');

// 解析命令行参数
const args = process.argv.slice(2);
const options = {
  type: 'fullstack',
  name: path.basename(projectRoot),
  force: false
};

args.forEach((arg, i) => {
  if (arg === '--type' && args[i + 1]) options.type = args[i + 1];
  if (arg === '--name' && args[i + 1]) options.name = args[i + 1];
  if (arg === '--force') options.force = true;
});

// 模板生成函数
const templates = {
  CLAUDE_MD: (name) => `# Project Instructions for Claude

## Role

You are a senior engineer working on the **${name}** project.

## Tech Stack

See \`context/stack.md\` for detailed tech stack information.

## Coding Rules

### General
- ALWAYS write production-ready code
- ALWAYS include error handling
- ALWAYS include types (TypeScript)
- NEVER use \`any\` type
- MUST follow existing code style

### When Generating Code
- MUST include proper types
- MUST include error handling
- MUST be production-ready (no TODOs in core logic)
- MUST follow project conventions from \`rules/\`
- SHOULD prefer composition over inheritance
- SHOULD write testable code

## Project Structure

See \`context/project.md\` for project overview and module boundaries.

## Quick Reference

- **Rules**: \`rules/\` - Hard constraints (MUST/ALWAYS/NEVER)
- **Context**: \`context/\` - Project knowledge and tech stack
- **Skills**: \`skills/\` - Reusable workflows
- **Prompts**: \`prompts/\` - Prompt templates
`,

  RULES_FRONTEND: `# Frontend Rules

## React

- MUST use functional components with hooks only
- NEVER use class components
- MUST use TypeScript for all components
- ALWAYS prefer composition over inheritance
- MUST include proper prop types

## Component Structure

- MUST export components as named exports (no default exports)
- MUST colocate related components and styles
- SHOULD keep components small and focused (single responsibility)

## State Management

- MUST use appropriate state management (Zustand/Context)
- NEVER mutate state directly
- SHOULD lift state to appropriate level

## Styling

- MUST follow design system tokens
- SHOULD use Tailwind utility classes consistently
- NEVER use inline styles except for dynamic values
`,

  RULES_TYPESCRIPT: `# TypeScript Rules

## Type System

- NEVER use \`any\` type - use \`unknown\` if truly needed
- MUST define return types for all functions
- SHOULD prefer \`type\` over \`interface\` for simple objects
- MUST use strict null checks

## Generics

- SHOULD use generics for reusable functions
- MUST constrain generics when possible

## Error Handling

- MUST handle errors explicitly (no silent failures)
- SHOULD use custom error types for domain errors
- MUST include error types in function signatures
`,

  RULES_COMMIT: `# Git Commit Rules

## Format

\`<type>(<scope>): <description>\`

### Types
- \`feat\`: New feature
- \`fix\`: Bug fix
- \`docs\`: Documentation changes
- \`style\`: Code style changes (formatting)
- \`refactor\`: Code refactoring
- \`test\`: Test changes
- \`chore\`: Build/config changes

## Rules

- MUST write commits in present tense ("add" not "added")
- MUST keep subject line under 72 characters
- SHOULD add body for complex changes
- MUST reference issues when applicable
`,

  CONTEXT_PROJECT: (name) => `# Project Overview: ${name}

## Description

This project is a web application.

## Key Modules

- **auth** - User authentication and authorization
- **core** - Core business logic and utilities
- **ui** - Reusable UI components
- **api** - API client and data fetching

## Architecture

- Frontend: Client-side SPA
- Backend: RESTful API
- Database: As defined in stack.md

## Getting Started

See README.md for development setup instructions.
`,

  CONTEXT_STACK: `# Tech Stack

## Frontend

- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Build**: Vite
- **Styling**: Tailwind CSS
- **State**: Zustand

## Backend

- **Runtime**: Node.js
- **Framework**: Fastify/Express
- **Database**: MySQL/PostgreSQL

## DevOps

- **CI/CD**: GitHub Actions
- **Deployment**: Vercel/Docker
- **Monitoring**: As configured

## AI Tools

- **Primary**: Claude Code
- **Config**: .claude/ directory
`,

  SKILLS_GENERATE_CRUD: `# Skill: Generate CRUD Operations

When user asks to create CRUD operations:

## Steps

1. **Define Types**
   - Create TypeScript interfaces for the entity
   - Include all required and optional fields

2. **Create API Client**
   - Generate API functions (list, get, create, update, delete)
   - Include proper error handling
   - Add request/response types

3. **Build UI Components**
   - List view with pagination
   - Detail/Edit form
   - Create modal/form
   - Delete confirmation

4. **Add Validation**
   - Form validation rules
   - Server-side validation
   - Error messages

5. **Write Tests**
   - Unit tests for utilities
   - Integration tests for API
   - E2E tests for critical flows

## Output Format

Always organize code in this order:
1. Types
2. API client
3. Components
4. Tests
`,

  PROMPTS_REVIEW: `# Prompt: Code Review

When reviewing code, follow this checklist:

## Security

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention

## Quality

- [ ] Types are correct and complete
- [ ] Error handling is adequate
- [ ] No console.log in production code
- [ ] Follows project conventions

## Performance

- [ ] No unnecessary re-renders
- [ ] Efficient data structures
- [ ] Proper caching where applicable

## Maintainability

- [ ] Code is well-organized
- [ ] Functions are small and focused
- [ ] Clear naming conventions
- [ ] Comments explain "why" not "what"

## Output Format

Provide feedback in this format:
1. Summary (1-2 sentences)
2. Critical issues (must fix)
3. Suggestions (nice to have)
4. Positive notes (what's good)
`
};

// 检查是否已存在 .claude 目录
function checkExisting() {
  if (fs.existsSync(claudeDir)) {
    const files = fs.readdirSync(claudeDir);
    if (files.length > 0) {
      console.log('⚠️  .claude/ directory already exists with content:');
      console.log(`   Files: ${files.join(', ')}`);
      console.log('\n💡 Skipping creation to avoid overwriting existing configuration.\n');
      console.log('   Tip: Let Claude Code maintain this directory during development.\n');
      return true;
    }
  }
  return false;
}

// 创建目录结构
function createDirectoryStructure() {
  const dirs = [
    claudeDir,
    path.join(claudeDir, 'rules'),
    path.join(claudeDir, 'context'),
    path.join(claudeDir, 'skills'),
    path.join(claudeDir, 'prompts')
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`✅ Created: ${path.relative(projectRoot, dir)}`);
    }
  });
}

// 创建文件
function createFiles() {
  const files = [
    { path: 'CLAUDE.md', content: templates.CLAUDE_MD(options.name) },
    { path: 'rules/frontend.md', content: templates.RULES_FRONTEND },
    { path: 'rules/typescript.md', content: templates.RULES_TYPESCRIPT },
    { path: 'rules/commit.md', content: templates.RULES_COMMIT },
    { path: 'context/project.md', content: templates.CONTEXT_PROJECT(options.name) },
    { path: 'context/stack.md', content: templates.CONTEXT_STACK },
    { path: 'skills/generate-crud.md', content: templates.SKILLS_GENERATE_CRUD },
    { path: 'prompts/review.md', content: templates.PROMPTS_REVIEW }
  ];

  files.forEach(file => {
    const filePath = path.join(claudeDir, file.path);
    if (!fs.existsSync(filePath) || options.force) {
      fs.writeFileSync(filePath, file.content.trim());
      console.log(`✅ Created: ${path.relative(projectRoot, filePath)}`);
    } else {
      console.log(`⊘  Skipped (exists): ${path.relative(projectRoot, filePath)}`);
    }
  });
}

// 主函数
function main() {
  console.log(`\n🚀 Setting up .claude/ for project: ${options.name}`);
  console.log(`   Type: ${options.type}\n`);

  // 检查是否已存在，避免画蛇添足
  if (!options.force && checkExisting()) {
    process.exit(0);
  }

  createDirectoryStructure();
  createFiles();

  console.log('\n✅ .claude/ setup complete!\n');
  console.log('📁 Directory structure:');
  console.log(`
.claude/
├── CLAUDE.md              # ⭐ Project-wide instructions (read first)
├── rules/
│   ├── frontend.md        # Frontend coding standards
│   ├── typescript.md      # TypeScript rules
│   └── commit.md          # Git commit conventions
├── context/
│   ├── project.md         # Project overview
│   └── stack.md           # Tech stack details
├── skills/
│   └── generate-crud.md   # CRUD generation workflow
└── prompts/
    └── review.md          # Code review checklist
`);

  console.log('💡 Tip: Claude Code will automatically read these files when working in this project.\n');
  console.log('👤 Role: You are the supervisor - let Claude Code maintain this directory during development.\n');
}

main();
