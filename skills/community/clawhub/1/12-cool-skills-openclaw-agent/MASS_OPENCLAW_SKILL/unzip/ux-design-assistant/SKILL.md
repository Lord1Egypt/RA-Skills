---
name: ux-design-assistant
description: Analyzes Figma design pages and proposes UX improvements. Use this when a user requests an analysis of a Figma design or suggestions for UX enhancements.
---

# UX Design Assistant for Figma

This skill provides guidance for analyzing Figma design pages and generating actionable UX improvement suggestions. It leverages core UX principles and user-provided directives to offer tailored feedback.

## Prerequisites

To use this skill, the user MUST be logged into Figma and provide a shareable link to the specific Figma design page they wish to have analyzed. The agent will use browser tools to access and interpret the design.

## Workflow

When a user requests a UX analysis of a Figma design, follow these steps:

### 1. Obtain Figma URL and User Directives

- **Request Figma URL**: Ask the user for the direct URL to the Figma design page. Ensure it's a shareable link that allows viewing.
- **Ask for Specific Directives**: Prompt the user for any specific design guidelines, principles, or areas of focus they want the analysis to adhere to (e.g., "Focus on accessibility," "Ensure compliance with Material Design," "Improve conversion rates"). If no specific directives are given, proceed with a general UX analysis based on standard principles.

### 2. Navigate and Analyze Figma Design

- **Open Figma in Browser**: Use your browser tool to navigate to the provided Figma URL. The user must be logged in for the page to load correctly.
- **Visual Inspection**: Perform a thorough visual inspection of the design, focusing on:
    - **Layout and Structure**: How elements are organized on the page.
    - **Information Hierarchy**: How important information is presented and prioritized.
    - **Interactivity**: Identify interactive elements (buttons, forms, navigation) and assess their clarity and discoverability.
    - **Visual Design**: Evaluate color usage, typography, iconography, and overall aesthetic appeal.
    - **Consistency**: Check for consistent application of design patterns, components, and branding.
    - **Apply UX Principles**: Refer to `references/ux_principles.md` for a comprehensive list of UX principles and a design analysis checklist. Apply these systematically during your inspection.
    - **Incorporate User Directives**: Integrate any specific directives provided by the user into your analysis, prioritizing them as key evaluation criteria.

### 3. Propose UX Improvements

Based on your analysis, generate a list of concrete and actionable UX improvement suggestions. Each suggestion should:

- Clearly identify the problem or area for improvement.
- Explain why it's an issue (e.g., violates a UX principle, contradicts user directive).
- Propose a specific solution or change.
- Prioritize suggestions based on impact and feasibility.

### 4. Present Findings to User

Deliver your analysis and improvement suggestions to the user. Structure your report clearly, highlighting key findings and actionable recommendations. Offer to refine the suggestions or perform further analysis based on their feedback.

## References

- `references/ux_principles.md`: Contains core UX principles and a design analysis checklist to guide the evaluation process.