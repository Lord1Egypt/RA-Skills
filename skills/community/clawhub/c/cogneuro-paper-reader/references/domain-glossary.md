# Domain Glossary — Attention, Memory, & Population Neuroscience

Use these definitions when explaining terms in a paper summary. Definitions are
written for a reader with no specialized background.

## Attention & mind-wandering

- **Sustained attention** — the ability to stay focused on a task over a long,
  monotonous period. Measured with continuous performance tasks.
- **Continuous performance task (CPT)** — a task that requires constant
  responding so that attention can be tracked continuously over time.
- **PVT (Psychomotor Vigilance Task)** — a CPT in which the participant responds
  as fast as possible to a rare, unpredictable stimulus; classic measure of
  vigilance and fatigue.
- **SART (Sustained Attention to Response Task)** — a CPT requiring frequent
  "go" responses to a common stimulus and withholding the response to a rare
  target; errors on rare trials mark lapses of attention.
- **gradCPT (gradual-onset CPT)** — a CPT with gradual image transitions used to
  track moment-to-moment attention fluctuations.
- **Attentional lapse** — a transient failure of attention; a "bad" state often
  marked by errors on rare trials or by unusually fast responding.
- **Mind-wandering** — task-unrelated thought (TUT); the mind drifts from the task.
- **Task-unrelated thought (TUT)** — thoughts unrelated to the current task; a
  common operationalization of mind-wandering.
- **Zone out / tune out** — mind-wandering with vs. without awareness. Zoning out
  (no awareness) is usually more harmful to performance than tuning out.
- **"In the zone" / "zoning out"** — terms from Esterman et al. for optimal vs.
  suboptimal attentional states.
- **Perceptual decoupling** — reduced processing of external stimuli during
  mind-wandering; a proposed mechanism for memory-encoding failures.
- **Vigilance decrement** — the decline in performance over time during a long,
  monotonous task.

## Reaction time & triggering methods

- **Response time / reaction time (RT)** — the time from stimulus onset to the
  response, in milliseconds.
- **Trailing average RT** — the mean RT over the most recent few trials (often 3),
  used as a running index of current response speed.
- **Cumulative mean (μ) / standard deviation (σ)** — running statistics over all
  trials so far; used to set individual, adaptive thresholds.
- **Fast / slow threshold** — bounds such as μ − σ (fast) and μ + σ (slow) that
  flag unusually fast (low-attention) or slow (high-attention) responding.
- **Real-time triggering** — a closed-loop design that computes RT statistics
  online and, when a threshold is crossed, triggers an event (e.g. a memory probe)
  in the same session.
- **RT variability** — the standard deviation of RTs; higher variability indicates
  poorer attentional control.

## Working memory

- **Working memory** — the short-term holding and manipulation of information.
- **Working memory capacity (K)** — the number of items held in mind; often
  estimated as K = N × (hit rate − false-alarm rate).
- **Change detection task** — a working-memory task: remember an array, then judge
  whether one item changed.
- **Whole-report task** — a working-memory task that asks the participant to report
  every item (not just one), giving trial-by-trial resolution of the number stored.
- **Continuous report / colour-wheel task** — report a remembered colour on a
  continuous wheel; yields response error and precision rather than a count.
- **Response error** — the angular deviation between the reported and true colour.
- **Precision (s.d.) vs. guessing (g)** — a mixture model of response errors: a
  von Mises distribution (precision) plus a uniform distribution (guessing rate).

## Neural population doctrine (from Ebitz & Hayden, 2021)

- **Population doctrine** — the view that the neural population, not the single
  neuron, is the fundamental unit of computation.
- **Single-neuron doctrine** — the traditional view focused on one neuron at a time.
- **Neural state** — the pattern of activity across a population of neurons at a
  moment; a point in neuron-dimensional space.
- **State space** — the abstract space whose axes are neurons; each neural state is
  a point/vector in it.
- **Trajectory** — the path a neural state traces through state space over time.
- **Manifold** — the lower-dimensional surface within state space that observed
  neural states occupy.
- **Coding dimension** — a direction in state space along which activity covaries
  with a task variable (stimulus, choice, value).
- **Subspace** — a lower-dimensional projection of state space encoding a variable
  or function; a **nullspace** is a subspace with no relationship to a given variable.
- **Dynamics** — the hidden network forces that shape how trajectories evolve.
- **Attractor** — a stable state toward which nearby activity evolves.
- **Dimensionality reduction** — methods (e.g. PCA) that compress many-neuron
  activity onto a few axes.
- **PCA (principal component analysis)** — finds orthogonal directions explaining
  the most variance; used both for visualization and as an analytic method.
- **Decoding** — predicting task information (e.g. stimulus, choice) from neural
  activity, often via linear/logistic regression.
- **Mixed selectivity** — neurons that respond to combinations of variables rather
  than a single one.
- **RSA (representational similarity analysis)** — comparing the similarity
  structure of neural responses across conditions or regions.
- **Pseudopopulation** — a population assembled from non-simultaneously recorded
  neurons via bootstrapping.
