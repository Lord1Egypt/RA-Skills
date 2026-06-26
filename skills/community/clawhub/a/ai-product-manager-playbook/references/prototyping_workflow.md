# Prototyping and Rapid Experimentation Workflow

This workflow guides the AI PM through the process of moving from a static PRD to an interactive, "production-ready" prototype.

## When to use this workflow
- Validating a new feature idea.
- Communicating complex interactions to engineering and design.
- Testing user flows before committing to full development.

## Step 1: Decompose the Feature
Do not attempt to prototype an entire application at once. Break the feature down into its smallest constituent parts.
- **Action:** Identify the core experience, the underlying rules, the discovery mechanism, and the feedback loop.
- **Example:** Instead of "build a referral program," prototype just the "generate referral link" component first.

## Step 2: Plan Before You Build
Engage in a dialogue with your chosen AI tool before generating any code.
- **Action:** Describe the desired outcome, provide context (e.g., existing design system guidelines), and ask the AI to propose an implementation plan.
- **Goal:** Ensure alignment and reduce the likelihood of rework.

## Step 3: Choose the Right Tool
Select the prototyping tool that matches the complexity of the task.
- **Chatbots (ChatGPT, Claude):** Best for simple, single-page prototypes or generating specific code snippets.
- **Cloud Development Environments (Replit, v0, Bolt):** Ideal for multi-page applications with basic backend logic.
- **Local IDE Assistants (Cursor, Copilot):** Best when integrating the prototype directly into your existing codebase.

## Step 4: Execute and Preview in Context
Generate the code and preview it.
- **Action:** If possible, use tools that integrate with your existing codebase to preview the new feature within the context of your actual product.
- **Goal:** Avoid the "rebuild tax" where prototypes are discarded because they don't match production standards.

## Step 5: Refine and Iterate
AI will get you 80-90% of the way there.
- **Action:** Use visual editors or iterative prompting to tweak layouts, styling, and interactions until the prototype meets your standards.

## Step 6: Ship or Discard
The goal of a prototype is to learn quickly.
- **Action:** Test the prototype with users or stakeholders. If it validates the assumption, move it toward production. If it fails, discard it and start a new experiment.
