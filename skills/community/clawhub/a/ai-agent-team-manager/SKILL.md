---
name: ai-agent-team-manager
description: Professional AI agent team management system for coordinating multiple OpenClaw agents. Implements the proven Otter Camp methodology with task assignment, progress tracking, quality control, and performance evaluation.
metadata:
  openclaw:
    requires:
      env:
        - OPENCLAW_WORKSPACE
      bins:
        - git
        - node
        - python3
---

# AI Agent Team Manager

## Overview
This skill implements a professional AI agent team management system based on the Otter Camp methodology. It enables you to coordinate multiple OpenClaw agents working together on complex projects with proper task assignment, progress tracking, quality control, and performance evaluation.

## When to Use This Skill
Use this skill when you need to:
- Manage multiple AI agents working on the same project
- Implement structured workflows for complex tasks
- Track progress and ensure quality across agent teams
- Evaluate agent performance and optimize workflows
- Scale AI operations beyond single-agent capabilities

## Core Features

### Task Assignment & Coordination
- Intelligent task decomposition and assignment
- Agent role definition and specialization
- Dependency management between tasks
- Resource allocation and load balancing

### Progress Tracking & Monitoring
- Real-time progress dashboards
- Milestone tracking and deadline management
- Automated status reporting
- Issue detection and escalation

### Quality Control & Review
- Multi-layer quality assurance processes
- Peer review between agents
- Human-in-the-loop checkpoints
- Automated testing and validation

### Performance Evaluation
- Agent performance metrics and scoring
- Workflow optimization recommendations
- Cost-benefit analysis of agent configurations
- Continuous improvement through learning

## Usage Examples

### Basic Team Setup
```javascript
const teamManager = new AIAgentTeamManager({
  workspace: '/path/to/workspace',
  agents: ['xiaolv', 'laogou', 'xiaoqiu', 'xiaozhu'],
  methodology: 'otter-camp'
});
```

### Task Coordination
```javascript
await teamManager.assignTask({
  taskId: 'email-analysis-2026',
  description: 'Analyze 3,418 emails from QQ mailbox',
  assignee: 'xiaolv',
  reviewers: ['laogou'],
  deadline: '2026-03-10',
  qualityChecks: ['accuracy', 'completeness', 'formatting']
});
```

### Performance Reporting
```javascript
const report = await teamManager.generatePerformanceReport({
  period: 'last-30-days',
  metrics: ['tasksCompleted', 'qualityScore', 'efficiency', 'cost']
});
```

## Integration Points
- Works seamlessly with existing OpenClaw agents
- Integrates with Git for version control
- Supports custom agent roles and specializations
- Compatible with all OpenClaw skill types

## Best Practices
- Start with small teams (2-4 agents) and scale gradually
- Implement regular quality reviews and checkpoints
- Use human oversight for critical decisions
- Continuously optimize based on performance data
- Maintain clear documentation of team workflows

## Security & Compliance
- All data remains in your local workspace
- No external API calls without explicit permission
- Full audit trail of all agent activities
- Compliant with enterprise security requirements