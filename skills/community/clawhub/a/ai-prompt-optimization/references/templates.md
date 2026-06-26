# Prompt Template Reference

## I. Writing Assistance

### Article Writing Template
```
# Role
You are a professional content creator in the [domain] field, skilled in [writing style].

# Task
Write a [type: article/blog/report] about [topic], targeting [audience].

# Requirements
- Topic: [core topic]
- Angle: [approach angle]
- Word Count: [word count requirement]
- Style: [formal/casual/professional]

# Structure
[Introduction requirements]
[Body outline]
[Conclusion requirements]

# Prohibited
- [Content to avoid]
```

### Translation Optimization Template
```
# Role
You are a professional translator proficient in [source language] and [target language].

# Source Text
[Content to be translated]

# Translation Requirements
- Style: [formal/colloquial/literary]
- Audience: [target readers]
- Terminology: [handling of specialized terms]

# Notes
[Special translation requirements]
```

## II. Code Generation

### Code Generation Basic Template
```
# Task
Implement [functional requirement] in [programming language].

# Environment
- Language Version: [version]
- Dependencies: [available libraries]

# Functional Requirements
1. [Core functionality]
2. [Edge case handling]

# Code Style
- Follow [coding standards]
- Include necessary [comments/documentation]

# Testing
[Test case requirements]
```

### Code Review Template
```
# Role
You are a senior [language] development engineer conducting a code review.

# Code
[Code to be reviewed]

# Review Focus
- [Security]
- [Performance]
- [Readability]
- [Best practices]

# Output Format
Issue classification → Specific suggestions → Priority
```

## III. Image Generation

### Midjourney / Stable Diffusion Prompt Template
```
# Subject
[Image subject description]

# Style
- [Artist style]
- [Art movement]
- [Era style]

# Composition
- [Perspective]
- [Shot distance]
- [Lighting]

# Parameters
- Aspect Ratio: [16:9/1:1 etc.]
- Quality: [HD/Standard]
- Render: [Engine selection]

# Negative Prompts
[Elements to avoid]
```

### Image Optimization Diagnosis
Checklist:
1. Is the subject clearly defined?
2. Is the style description specific?
3. Are lighting and atmosphere specified?
4. Is the composition/perspective indicated?
5. Are elements to avoid clearly stated?

## IV. Data Analysis

### Data Analysis Template
```
# Objective
Analyze [dataset/problem] to answer [core question].

# Data
[Data source or description]

# Analysis Requirements
- Method: [statistical/ML/visualization]
- Tools: [tool preference]
- Depth: [descriptive/diagnostic/predictive]

# Output
- Summary of conclusions
- Key findings
- Data visualizations (if needed)
- Recommended actions

# Constraints
- Time Range: [time range]
- Data Limitations: [known limitations]
```

## V. Q&A and Consultation

### Professional Consultation Template
```
# Background
[Problem background/context]

# Question
[Core question]

# Attempted Solutions
[Solutions already tried]

# Constraints
- [Budget/time/technical constraints]

# Expectations
[Desired outcome/answer type]

# Additional Information
[Any extra information that may be helpful]
```

## VI. General Optimization Framework

### CRISP Framework
- **C**larity: Is the objective clear?
- **R**elevance: Is the context sufficient?
- **I**nput: Is the necessary information provided?
- **S**tructure: Is the organization clear?
- **P**recision: Are the constraints explicit?

### Iterative Optimization Prompt
```
# Original Prompt
[User-provided prompt]

# Diagnosis Results
[Identified issues]

# Optimized Version
[Improved prompt]

# Explanation of Changes
[Rationale for each change]

# Suggested Tests
[Sample inputs to test this prompt]
```