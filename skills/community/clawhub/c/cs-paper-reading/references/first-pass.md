# First Pass Reading: Quick Scan for Computer Science Papers

## Objective
Get a bird's-eye view of the paper in 5-10 minutes. Determine relevance and decide whether to proceed to second pass.

## Execution Steps

### 1. Read Title, Abstract, and Introduction
- **Title**: Identify the core contribution and scope
- **Abstract**: Extract problem, method, results, and conclusions
- **Introduction**: Understand motivation, research gap, and paper structure

### 2. Scan Section Headings
- **Computer Science Paper Structure**:
  - Abstract/Summary
  - Introduction (Problem Statement, Motivation, Contributions)
  - Related Work / Background
  - Method / Model / System Design
  - Experiments / Evaluation
  - Results / Analysis
  - Conclusion / Future Work
  - References
- **Ignore**: Detailed content, proofs, implementation details

### 3. Review Conclusion
- Identify main findings and contributions
- Note any limitations mentioned

### 4. Check References
- Mentally tick off papers you've already read
- Identify key authors and seminal works

## Core Tasks

### Answer the Five Cs (Computer Science Adaptation)

1. **Category**: What type of CS paper is this?
   - Algorithm/Theory paper
   - Systems paper
   - Empirical/Experimental paper
   - Survey/Tutorial paper
   - Position/Vision paper

2. **Context**: Which other papers is it related to?
   - Key references in the field
   - Theoretical foundations used
   - Building upon which prior work

3. **Correctness**: Do the assumptions appear valid?
   - Problem formulation合理性
   - Baseline comparisons fairness
   - Evaluation metrics appropriateness

4. **Contributions**: What are the paper's main contributions?
   - Novel algorithm/method
   - Theoretical insight
   - Empirical findings
   - System implementation
   - Dataset/benchmark

5. **Clarity**: Is the paper well written?
   - Logical flow
   - Clear problem statement
   - Reproducibility considerations

## Checkpoint Criteria

### Must Complete Before Proceeding
- [ ] Can summarize the paper in 1-2 sentences
- [ ] Can identify the paper type and contribution category
- [ ] Can list 3-5 key related papers/authors
- [ ] Can state whether assumptions seem reasonable
- [ ] Can describe the main contribution clearly
- [ ] Decision: Proceed to second pass? (Yes/No)

### Time Budget
- **Maximum time**: 10 minutes
- **If exceeding**: Stop and decide whether to continue

## Output Format
```markdown
## First Pass Summary
- **Paper Type**: [Category]
- **Core Problem**: [1 sentence]
- **Main Contribution**: [1 sentence]
- **Key Related Work**: [2-3 papers/authors]
- **Assumptions Validity**: [Yes/No/Partial]
- **Relevance Decision**: [Proceed/Stop]
```

## Common Pitfalls
- Spending too long on mathematical content during first pass
- Getting bogged down in implementation details
- Not checking references for prior knowledge
- Skipping conclusion and jumping to experiments