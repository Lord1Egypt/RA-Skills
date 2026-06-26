# 🧠 Recommendation Engine (The Brain)

This directory contains the logic for **Content Analysis** and **Style Mapping**. It defines *how* the Copilot decides which Style + Layout to use.

## Decision Logic (Pseudo-Code)

### 1. Analyze User Input (Content Classification)

Input: "I want a page for a children's book reading event."

*   **Keywords**: "children", "book", "reading", "event".
*   **Sentiment**: Warm, Playful, Safe, Educational.
*   **Industry**: Education / Entertainment.

### 2. Map to Attributes

| Attribute | Value | Reason |
|-----------|-------|--------|
| `formal_level` | Low | Kids prefer informal |
| `color_temp` | Warm | Welcoming |
| `contrast` | High | Readability for kids |
| `complexity` | Low | Simple navigation |

### 3. Select Style & Layout

*   **Style Match**: `neo-brutalism` (Playful variant) OR `warm-academia` (if serious).
    *   *Decision*: Let's go with a custom mix: **"Playful Paper"** (Warm colors + Soft rounded shapes).
*   **Layout Match**: `poster-zine` (if single page) or `hero-split` (if info page).

## Output Generation

The Engine combines the selected **Style** + **Layout** to generate the final **Design Spec**.
