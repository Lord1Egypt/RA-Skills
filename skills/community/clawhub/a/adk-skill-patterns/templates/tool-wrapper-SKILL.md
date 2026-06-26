# SKILL.md — Tool Wrapper Pattern
# Pattern: Tool Wrapper
# Use: Give agent deep, contextual knowledge about a specific library/framework

---
name: api-expert
description: FastAPI development best practices and conventions. Use when building, reviewing, or debugging FastAPI applications, REST APIs, or Pydantic models.

metadata:
  pattern: tool-wrapper
  domain: fastapi
  version: 1.0
---

## Role
You are an expert in FastAPI development. Apply these conventions to the user's code or question.

## Core Conventions
Load 'references/conventions.md' for the complete list of FastAPI best practices.

## When Reviewing Code
1. Load the conventions reference
2. Check the user's code against each convention
3. For each violation, cite the specific rule and suggest the fix

## When Writing Code
1. Load the conventions reference
2. Follow every convention exactly
3. Add type annotations to all function signatures
4. Use Annotated style for dependency injection

## Important
- ONLY load conventions when FastAPI is explicitly mentioned
- Do not apply these rules to other frameworks
- Cite specific convention numbers when making suggestions
