# Hermes Agent Infographic Workflow Example

This document captures the complete workflow used to prepare an infographic for the "Technical Insight Interview Prep" document, demonstrating how to use the custom-infographic skill when image_generate is not available.

## Workflow Overview

When the `image_generate` tool is not available, the custom-infographic skill can still be used to:
1. Analyze source content
2. Generate structured content for infographic creation
3. Create a detailed prompt for external image generation services
4. Prepare all necessary files for manual or external infographic creation

## Files Created in This Session

### 1. source.md
- Exact copy of the source document
- Serves as the authoritative source for verbatim extraction

### 2. analysis.md
- Content analysis following the analysis-framework.md
- Includes:
  - Content type classification (overview/summary)
  - Learning objectives (3)
  - Audience analysis
  - Complexity assessment (moderate, 8 points)
  - Verbatim data points extraction
  - Layout × style signals
  - Recommended combinations

### 3. structured-content.md
- Transforms analysis into designer-ready format
- Includes:
  - Title and overview
  - Learning objectives
  - 8 detailed sections (Mindset, Environment, Skills, etc.)
  - For each section: Key Concept, Content (verbatim), Visual Element description, Text Labels
  - A Data Points (Verbatim) section for data-integrity verification only — never copied into the prompt
  - Design Instructions extracted from user preferences

### 4. prompts/infographic.md
- Complete prompt for image generation
- Combines:
  - Layout guidelines (bento-grid)
  - Style guidelines (chalkboard)
  - Base prompt template
  - Structured content from Step 2
  - The single canonical text-label list, enumerated exactly once in the CRITICAL block (never a second dump)
- Ready for use with external image generation services

## How to Use This Workflow When image_generate is Unavailable

1. **Complete Steps 1-5** of the custom-infographic workflow:
   - Analyze content → analysis.md
   - Generate structured content → structured-content.md
   - Generate prompt → prompts/infographic.md

2. **Use the prompt externally**:
   - Copy the contents of `prompts/infographic.md`
   - Paste into your preferred image generation service (Midjourney, DALL-E, Stable Diffusion, etc.)
   - Adjust aspect ratio mapping if needed (16:9 → landscape, etc.)

3. **Alternative approaches**:
   - Use the structured-content.md as a brief for a human designer
   - Convert sections to slides using presentation tools
   - Use available diagram skills (excalidraw, sketch) for individual sections

## Key Learnings

1. **Tool verification is crucial**: Always check for required tools before starting workflow
2. **Fallback preparation**: The skill should prepare users for manual completion when tools are unavailable
3. **Prompt quality matters**: A well-structured prompt (like the one created) yields better results from external services
4. **Modular approach works**: Breaking infographic creation into analysis → structure → prompt allows for external completion

## When to Use This Approach

Use this workflow when:
- You need to create an infographic but lack direct image generation capabilities
- You want to prepare content for professional design handoff
- You need to preserve exact verbatim content from source documents
- You're working in environments with restricted tool availability

This approach ensures that even without automated image generation, the core value of the custom-infographic skill (content analysis, structuring, and prompt preparation) is still delivered.