---
name: ai-prompt-optimization
description: Use when users need to optimize prompts for AI conversations, generate structured templates, create few-shot examples, design chain-of-thought guidance, or diagnose and improve existing prompts. Applicable to prompt optimization for various AI tools such as ChatGPT, Claude, Midjourney, etc.
---

# AI Prompt Optimization

## Core Capabilities

When users seek prompt optimization assistance, provide the following services:

1. **Diagnosis & Optimization** - Analyze existing prompt issues and provide specific improvement plans
2. **Template Generation** - Generate structured prompt templates for different scenarios
3. **Few-Shot Generation** - Create example-driven few-shot prompts
4. **Chain-of-Thought Guidance** - Design CoT (Chain of Thought) prompts

## Usage

### 1. Diagnosis & Optimization Workflow

When a user provides a prompt for optimization:

```
Analyze Structure → Identify Issues → Provide Improved Version → Explain Changes
```

**Diagnosis Checklist**:
- [ ] Is the role/identity clearly defined?
- [ ] Is the task objective specific and clear?
- [ ] Are output format/style constrained?
- [ ] Is the necessary context/background information provided?
- [ ] Are boundary conditions and exceptions specified?
- [ ] Are there clear success criteria?

### 2. Template Generation

Generate structured templates based on user scenarios. Core template format:

```
# Role Definition
You are a [role] in [professional domain], skilled at [core competency].

# Task Description
Please help me [specific task], with the goal of [expected outcome].

# Context Information
- Background: [relevant background]
- Audience: [target users]
- Constraints: [boundary conditions]

# Output Requirements
- Format: [desired format]
- Style: [language style]
- Length: [length requirement]

# Quality Standards
[Key metrics for evaluating output]
```

### 3. Few-Shot Example Generation

Generate few-shot examples for complex tasks:

1. **Select Representative Samples** - 3-5 examples covering different variants
2. **Format Examples** - Input → Output structure
3. **Add Explanations** - Explain the rationale for selecting each example

### 4. Chain-of-Thought Design

Design CoT prompts for tasks requiring reasoning:

```
Before giving your final answer, please think through the following steps:
1. [Understand the Problem] - ...
2. [Decompose the Problem] - ...
3. [Step-by-Step Reasoning] - ...
4. [Verify the Conclusion] - ...
```

## Scenario Reference

For complete scenario templates and examples, see `references/templates.md`:
- Writing assistance prompts
- Code generation prompts
- Image generation prompts
- Data analysis prompts
- Q&A and consultation prompts

## Optimization Principles

1. **Specific > Vague** - Clearly specify what is wanted and what is not
2. **Structured > Scattered** - Use clear segmentation and markers
3. **Constrained > Free** - Appropriate constraints improve output quality
4. **Iterative > One-Shot** - Encourage users to continuously optimize based on output