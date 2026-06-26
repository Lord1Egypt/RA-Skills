# Limitations — Agent Scorecard

## What It Doesn't Do

### No Semantic Understanding
Automated checks are pattern-based, not semantic. The tool can detect sycophancy markers and hedge words, but it cannot judge whether a claim is factually correct. Accuracy scoring relies on manual evaluation or proxy signals (hedge word density).

### No LLM-as-Judge
This is deliberate. Agent Scorecard runs locally with zero API calls. The tradeoff is that automated checks catch surface-level quality signals only. For deep evaluation, use manual scoring mode.

### No Multi-Modal Support
Evaluates text only. Cannot score images, audio, code execution results, or tool-use sequences.

### No Real-Time Monitoring
Scorecard is a batch evaluation tool. It doesn't intercept agent outputs in real-time. You feed it text, it scores it. Integration with live pipelines requires your own glue code.

### No Statistical Significance Testing
Trend analysis uses simple linear regression. It doesn't compute confidence intervals, p-values, or run proper A/B test statistics. For rigorous statistical analysis, export the data and use proper tools.

### Pattern-Based Checks Are Blunt Instruments
- Sycophancy detection uses keyword matching — a response discussing the concept of sycophancy will trigger false positives
- Filler word detection doesn't understand context ("just" in "just-in-time" is not filler)
- Format checks verify structure presence, not structural quality
- Style consistency measures sentence length variance, not actual stylistic coherence

### No Cross-Agent Normalisation
Scores are absolute (1-5 per rubric). Comparing scores across different agents is meaningful only if they were evaluated against the same rubric with the same config. No built-in normalisation or calibration.

### History File Is Append-Only JSONL
No database, no indexing, no concurrent write safety. Works fine for hundreds or low thousands of evaluations. At scale, you'd want to export to a proper database.

### Manual Scoring Is Subjective
Two humans using the same rubric may score differently. The rubric helps but doesn't eliminate inter-rater variability. For team use, calibrate by having multiple raters score the same outputs and discussing discrepancies.
