# Second Pass Reading: Content Grasp for Computer Science Papers

## Objective
Grasp the paper's content, evidence, and reasoning in up to 1 hour. Understand the contribution without getting lost in details.

## Execution Steps

### 1. Read with Greater Care
- **Focus on**: Figures, diagrams, tables, algorithms
- **Ignore**: Proofs, implementation minutiae, low-level details
- **Take notes**: Key points in margins or separate document

### 2. Analyze Visual Elements
- **Figures**: What do they demonstrate? Are captions clear?
- **Tables**: What comparisons are made? Are metrics appropriate?
- **Algorithms**: What is the core logic? Complexity?
- **Diagrams**: System architecture? Data flow?

### 3. Mark Relevant References
- Identify unread papers that seem important
- Note which references are cited for key claims
- Prioritize for later reading

### 4. Understand Methodology
- **Problem Formulation**: How is the problem formalized?
- **Approach**: What is the proposed solution?
- **Innovation**: What is novel compared to prior work?
- **Assumptions**: What assumptions are made?

### 5. Evaluate Experimental Design
- **Baselines**: What are compared against?
- **Datasets**: Are they appropriate and sufficient?
- **Metrics**: Do they measure what matters?
- **Ablations**: Are component contributions isolated?

## Core Tasks

### Computer Science Paper Sections Analysis

#### Method/Model Section
- Identify the core algorithm or system design
- Understand input/output specifications
- Note complexity claims (time/space)
- Identify key innovations

#### Experiments Section
- **Setup**: Datasets, baselines, hyperparameters
- **Research Questions**: What do experiments aim to show?
- **Main Results**: Headline numbers and comparisons
- **Ablations**: Component-wise contributions

#### Results Analysis
- **Strengths**: Where does the method excel?
- **Weaknesses**: Where does it fall short?
- **Statistical Significance**: Are differences meaningful?
- **Reproducibility**: Sufficient detail to replicate?

### Create Structured Summary

#### Paper Summary Template
```markdown
## Paper Summary
**Title**: [Full title]
**Authors**: [Key authors]
**Venue**: [Conference/Journal and year]

### Problem Statement
- What problem is being solved?
- Why is it important?
- What are the limitations of existing approaches?

### Proposed Approach
- Core idea in 2-3 sentences
- Key innovation
- Technical approach overview

### Experimental Evaluation
- Datasets used
- Baselines compared
- Main results (quantitative)
- Key findings

### Strengths and Weaknesses
**Strengths**:
1. [Strength 1]
2. [Strength 2]

**Weaknesses**:
1. [Weakness 1]
2. [Weakness 2]

### Relevance to Your Work
- How does this relate to your research?
- What can you learn/apply?
- What questions does it raise?
```

## Checkpoint Criteria

### Must Complete Before Proceeding
- [ ] Can summarize the paper's main thrust with supporting evidence
- [ ] Can explain the method to someone else
- [ ] Can identify the key innovation
- [ ] Can list the main experimental findings
- [ ] Can identify at least 2 strengths and 2 weaknesses
- [ ] Can assess relevance to your research
- [ ] Decision: Proceed to third pass? (Yes/No)

### Time Budget
- **Maximum time**: 1 hour
- **If exceeding**: Prioritize remaining sections

## Output Format
```markdown
## Second Pass Summary
- **Core Contribution**: [2-3 sentences]
- **Key Innovation**: [What's new]
- **Main Results**: [Quantitative summary]
- **Strengths**: [2-3 points]
- **Weaknesses**: [2-3 points]
- **Related Papers to Read**: [List]
- **Relevance Score**: [High/Medium/Low]
```

## Common Pitfalls
- Getting stuck on mathematical proofs
- Not taking notes while reading
- Ignoring figures and tables
- Not checking experimental setup fairness
- Skipping related work section