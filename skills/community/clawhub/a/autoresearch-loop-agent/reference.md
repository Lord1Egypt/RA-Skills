# Autoresearch Reference

## Origin

Autoresearch was created as a framework for autonomous AI research, inspired by the idea of fully autonomous research organizations run by AI agents. The original implementation focused on LLM training optimization (minimizing validation bits-per-byte for a GPT model in a fixed 5-minute time budget).

The methodology proved remarkably effective: in one session, an agent ran 3,000+ experiments overnight, finding 125 improvements that collectively reduced val_bpb by 2.83%. Many of these were changes humans wouldn't have thought to try.

## Why It Works

### The Freedom-Constraint Balance

The deeper insight behind autoresearch is the balance between freedom and constraints:

- **Too much freedom**: Agent veers off course, makes random changes, can't evaluate progress
- **Too little freedom**: Agent can't explore, misses creative solutions
- **The sweet spot**: Humans set direction and constraints, agents explore exhaustively within boundaries

Humans bring **taste** — which problems are worth solving, which metrics matter, what counts as "good." Agents bring **tirelessness** — trying every combination, running every ablation, patiently working through plateaus where humans would have given up.

### Fixed Time Budget

Making every experiment take the same amount of time (wall clock or compute budget) is crucial. It means:
- All results are directly comparable
- No experiment gets unfair advantage from running longer
- The agent can make meaningful before/after comparisons
- Progress is measured in improvement-per-experiment, not improvement-per-hour

### Git as Lab Notebook

Using git history as the experiment record is elegant because:
- Every kept experiment is a commit with a message explaining what changed
- The diff shows exactly what was modified
- The branch shows the trajectory of improvements
- Discarded experiments leave no trace on the branch (clean history)
- results.tsv provides the quantitative companion to git's qualitative record

### One Variable at a Time

This is the scientific method applied to code optimization. When you change one thing:
- If the metric improves → the change caused it
- If the metric worsens → the change caused it
- You learn something either way

When you change two things at once:
- If the metric improves → which change helped? Maybe both? Maybe one helped and one hurt, but the net was positive?
- You learn almost nothing

The discipline of single-variable changes is what makes the exploration **informative** rather than just random.

## Results TSV Format

Tab-separated values, one row per experiment:

```
commit	<metric_name>	status	description
```

- **commit**: 7-character git hash (or "baseline" for first run)
- **metric**: The measured value (0.0 for crashes)
- **status**: `keep`, `discard`, or `crash`
- **description**: Brief explanation of what was tried

Example:
```
commit	val_bpb	status	description
baseline	0.997900	keep	baseline run, no changes
a1b2c3d	0.993200	keep	increase learning rate to 0.04
b2c3d4e	1.005000	discard	switch to GeLU activation
c3d4e5f	0.000000	crash	double model width (OOM)
d4e5f6g	0.990100	keep	reduce batch size by half
e5f6g7h	0.991000	discard	add dropout 0.1
```

## Config File Format

`autoresearch.config.md` stores the experiment protocol. It should contain:

1. **Goal**: What we're optimizing and why
2. **Metric**: Name, direction (lower/higher is better), extraction command
3. **Target files**: What the agent can modify
4. **Read-only files**: What must not be touched
5. **Run command**: How to execute one experiment
6. **Time budget**: Duration per experiment and kill timeout
7. **Constraints**: Hard limits on what the agent can and cannot do
8. **Branch name**: `autoresearch/<tag>`

## Tips for Effective Autoresearch

### For the human (setting up)

1. **Choose one clear metric**. If you have multiple goals, combine them into a single number (weighted sum, harmonic mean, etc.) before starting.
2. **Make the metric cheap to compute**. The faster each experiment runs, the more you can explore.
3. **Constrain the search space**. Don't let the agent modify everything — focus on the files/parameters most likely to matter.
4. **Set a meaningful baseline**. The agent needs a starting point to improve from.
5. **Write good constraints**. The agent will push boundaries — be explicit about what's off-limits.

### For the agent (running experiments)

1. **Read the history before each experiment**. Don't repeat what's been tried.
2. **Start with high-impact changes**. 2x/0.5x sweeps of important parameters first.
3. **Learn from failures**. A crash tells you something. A metric regression tells you something. Use this information.
4. **Try bold changes occasionally**. Small incremental tweaks are safe but may miss global optima. Every 10-20 experiments, try something significantly different.
5. **Simplify when possible**. If removing code doesn't hurt the metric, keep the simpler version. Less code = less surface area for bugs.
6. **Don't give up on a direction too quickly**. Sometimes a change needs to be combined with another adjustment (but test each one separately!).

## Comparison with Other Approaches

| Approach | Pros | Cons |
|----------|------|------|
| Grid search | Exhaustive | Exponential in dimensions, wastes time on bad regions |
| Random search | Better coverage | No learning between trials |
| Bayesian optimization | Sample-efficient | Complex setup, hard to reason about |
| **Autoresearch** | Agent learns from history, creative exploration, simple to set up | Slower per-trial than automated methods |

Autoresearch's unique advantage is that the agent **reasons** about what to try next based on the full history of experiments. It's not just sampling from a distribution — it's forming hypotheses and testing them. This makes it especially effective in spaces where the relationship between parameters and outcomes is complex and poorly understood.
