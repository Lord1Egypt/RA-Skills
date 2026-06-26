---
name: capture-classification
description: Standard Operating Procedure (SOP) that routes unstructured text to Tasks or LanceDB based on urgency using atomic nodes.
os: all
requires:
  bins: [gog]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This workflow relies entirely on discrete, single-responsibility atomic nodes rather than a monolithic loop.
- **Standardized Work (Hyojun Sagyo):** This node represents a strict, step-by-step Standard Operating Procedure (SOP) for inbound text classification.
- **Jidoka (自働化):** Includes autonomous self-healing loops with hard verification stops between every step.

# Capture Classification SOP

This procedure guides the agent to act as a semantic router for inbound text using explicitly defined atomic nodes.

## Cognitive Directives
WHEN [Unstructured audio transcript or note text is captured]
THEN [
  Follow this strict Standard Operating Procedure:

  **Step 1: Classification**
  - Execute the `LLM-Classify-Intent` atomic skill with categories: ["Actionable", "Informational"].
  - **Jidoka Stop:** Verify the skill returns exactly one of the requested categories. IF it fails, instruct it to correct the output and retry. Do NOT proceed until a valid category is obtained.

  **Step 2: Routing Execution**
  - IF "Actionable": 
    - Execute the `Google Tasks Create Task` atomic node using the text as the title.
    - **Jidoka Stop:** Check if the node returns a successful JSON response. IF it fails, retry up to 3 times. IF it still fails, report the error and STOP.
  - IF "Informational": 
    - Execute the `Vector Store Upsert Memory` atomic node to save it as reference material.
    - **Jidoka Stop:** Verify the vector store confirms a successful upsert. IF it fails, retry up to 3 times. IF it still fails, report the error and STOP.
]

## Expected Output
A JSON log confirming the routed destination and action taken by the respective atomic node.
