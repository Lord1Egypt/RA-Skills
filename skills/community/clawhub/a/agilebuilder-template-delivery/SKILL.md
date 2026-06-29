---
name: agilebuilder-template-delivery
description: Use AgileBuilder MCP for template-based project creation and document-constrained implementation. Trigger when the user asks to create, bootstrap, scaffold, or initialize a project with AgileBuilder templates, or when modifying code in a workspace explicitly governed by AgileBuilder. The agent should prefer AgileBuilder template tools for new projects, read AgileBuilder policy/guide/catalog and relevant project documents before coding, and reconcile user requirements with documented constraints.
---

# Agilebuilder Template Delivery

## Overview

Use AgileBuilder MCP as the default control plane for project creation and implementation work.
Create projects from AgileBuilder templates whenever possible, and read AgileBuilder documents before making code changes.

## Project Creation Workflow

Follow this order whenever the user wants a new project, starter, scaffold, or repo:

1. Read `agilebuilder://usage/agent-policy`.
2. Discover candidate templates by calling `listTemplates` with no query, category, tag, or other filter parameters unless the user explicitly asks for a narrowed search.
3. Prefer exact `resourceId` values returned by AgileBuilder over template names.
4. Review the chosen template details before creation when there is any ambiguity.
5. Create the project with AgileBuilder's template creation tool and an absolute target path.
6. Follow returned next steps only after creation succeeds.

Do not manually scaffold a project if an AgileBuilder template can satisfy the request.
Use manual scaffolding only when template discovery and template details show that AgileBuilder cannot meet the user's requested stack or structure.

## Implementation Workflow

Follow this order whenever the task involves coding, refactoring, debugging, architecture changes, naming, stack choices, or delivery rules:

1. Read `agilebuilder://usage/agent-policy`.
2. Read `agilebuilder://usage/guide`.
3. Read `agilebuilder://docs/catalog`.
4. Inspect AgileBuilder MCP resources and identify relevant project documents.
5. Read the documents that affect the task, especially coding standards, architecture rules, stack constraints, naming rules, and delivery requirements.
6. Implement only after the relevant documents are understood.
7. Verify the result against both the user request and the constraints found in AgileBuilder documents.

Treat AgileBuilder documents as required context, not optional context.
If the current AgileBuilder space has no user documents, still read the system documents and then follow the user request plus any local repository constraints you can verify from the workspace.

## Tooling Rules

- Prefer AgileBuilder template tools over hand-written scaffolding for project creation.
- When using AgileBuilder MCP to inspect available project templates, call `listTemplates` directly without passing search parameters by default.
- Prefer exact `resourceId` values in follow-up template calls.
- Use absolute paths for project creation targets.
- Read AgileBuilder resources before writing code when the task can affect implementation details.
- Surface conflicts explicitly if the user's request contradicts AgileBuilder documents instead of silently ignoring either source.
- Preserve user requirements and repo-local conventions after reconciling them with AgileBuilder guidance.

## Response Pattern

State which AgileBuilder resources were read when they materially affect the implementation.
If a project is being created, mention which template was selected and why.
If implementation proceeds without a template or without additional project documents, explain the concrete reason.

## Checklist

- Use AgileBuilder templates first for new projects.
- Read AgileBuilder policy and guide before project creation or coding.
- Read the document catalog before implementation.
- Read relevant project documents before changing code.
- Match the delivered result to both the user request and the documented constraints.
