---
name: ai-pm-playbook
description: "A comprehensive operating system for AI Product Management. Use this skill when planning, prototyping, evaluating, or launching AI-native products. It provides agentic workflows for roadmap planning under uncertainty, rapid prototyping, AI evaluations, cross-functional collaboration, go-to-market strategy, and responsible AI deployment."
---

# AI PM Playbook

## Overview

The **`ai-pm-playbook`** skill operationalizes the best practices of AI Product Management into executable, agentic workflows. It is designed to help product managers transition from traditional, process-heavy roles to the "builder mentality" required in the AI era.

This skill provides a structured approach to the entire AI product lifecycle, ensuring that products are built rapidly, evaluated rigorously, and deployed responsibly.

**Use this skill when:**
- Prototyping a new AI feature or product.
- Planning a product roadmap in a rapidly changing AI landscape.
- Designing and running evaluations (Evals) for an AI model.
- Structuring a cross-functional AI product team.
- Developing a Go-To-Market (GTM) strategy for an AI product.
- Implementing ethical guardrails and red teaming for responsible AI.

## The AI PM Operating System

This skill is built on the premise that AI automates low-value PM tasks (like writing detailed PRDs) and elevates the need for strategic vision, judgment, and technical fluency. The workflows below are designed to augment these higher-order skills.

## Core Workflows

Choose the appropriate workflow based on your current product development phase:

### 1. Prototyping and Rapid Experimentation
Move from static PRDs to interactive, "production-ready" prototypes.
- **Action:** Decompose features, plan with AI, and build interactive prototypes.
- **Reference:** See `references/prototyping_workflow.md` for the step-by-step guide.

### 2. Roadmap Planning Under Uncertainty
Shift from feature-based roadmaps to outcome-oriented planning.
- **Action:** Define desired behaviors, use the Now/Next/Later framework, and apply the U.S.I.D.O. model.
- **Reference:** See `references/roadmap_uncertainty.md` for the planning framework.
- **Template:** Use `templates/outcome_roadmap.md` to structure your plan.

### 3. AI Evaluation and Metrics (Evals)
Move beyond basic accuracy to measure user experience, safety, and reliability.
- **Action:** Define evaluator roles, supply context, set goals, and establish scoring rubrics.
- **Reference:** See `references/evaluation_metrics.md` for the evaluation framework.
- **Template:** Use `templates/ai_eval_rubric.md` to design your evals.

### 4. Cross-Functional Collaboration
Structure your team for success in the complex world of AI development.
- **Action:** Implement a hybrid team structure, prioritize data readiness, and foster psychological safety.
- **Reference:** See `references/cross_functional.md` for organizational best practices.

### 5. Go-To-Market Strategy and Trust
Launch AI products that meet evolving customer expectations and build trust.
- **Action:** Define the 7 GTM pillars and prioritize transparency in data usage.
- **Reference:** See `references/gtm_strategy.md` for the launch framework.

### 6. Ethics, Safety, and Responsible Deployment
Ensure your AI products are safe, trustworthy, and aligned with human values.
- **Action:** Implement multi-layered guardrails and conduct rigorous red teaming.
- **Reference:** See `references/responsible_ai.md` for the safety framework.
- **Template:** Use `templates/red_teaming_plan.md` to structure your testing.

## Self-Improving Loop

This skill incorporates a self-improving feedback loop to continuously refine your PM processes based on real-world execution data.

1. **Collect Telemetry:** After completing a major PM activity (e.g., a prototype sprint, an eval run, or a product launch), gather the outcomes, friction points, and user feedback.
2. **Run the Loop:** Execute `scripts/pm_feedback_loop.py` with the collected data.
3. **Analyze and Adapt:** The script will analyze the systemic friction and suggest updates to your templates, workflows, or evaluation rubrics to improve future performance.

## Resources

- **`scripts/pm_feedback_loop.py`**: The engine for continuous improvement of PM processes.
- **`references/`**: Detailed guides for each of the 6 core workflows.
- **`templates/`**: Standardized formats for roadmaps, evals, and red teaming plans.
