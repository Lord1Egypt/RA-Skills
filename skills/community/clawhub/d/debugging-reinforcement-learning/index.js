'use strict';

/**
 * Debugging Non-Deterministic Agent Behavior in Reinforcement Learning Environments
 *
 * Provides four core modules:
 *   - stochasticityControl: Control and isolate randomness sources
 *   - reproducibilityTools: Make RL experiments reproducible
 *   - behaviorAnalysis: Analyze what the agent is actually doing
 *   - rewardDebugging: Diagnose reward-related issues
 */

// ─────────────────────────────────────────────────────────────
// 1. Stochasticity Control
// ─────────────────────────────────────────────────────────────

const stochasticityControl = {
  /**
   * Seed all known RNG sources deterministically.
   * Returns a seed manager object for tracking and resetting.
   * @param {number} masterSeed - Master seed to derive sub-seeds from
   * @returns {object} seedManager with methods: reset(), getSeed(label), report()
   */
  seedAll(masterSeed = 42) {
    const seeds = {};
    let _counter = 0;

    function deriveSeed(label) {
      // Simple but effective seed derivation: mix label hash with master + counter
      let hash = masterSeed;
      for (let i = 0; i < label.length; i++) {
        hash = ((hash << 5) - hash + label.charCodeAt(i)) | 0;
      }
      hash = (hash + _counter++) | 0;
      seeds[label] = Math.abs(hash) || 1; // ensure non-zero
      return seeds[label];
    }

    // Pre-seed common sources
    deriveSeed('stdlib_random');
    deriveSeed('numpy');
    deriveSeed('torch_cpu');
    deriveSeed('torch_cuda');
    deriveSeed('env_internal');

    return {
      masterSeed,
      seeds,
      getSeed(label) {
        if (!seeds[label]) deriveSeed(label);
        return seeds[label];
      },
      reset() {
        _counter = 0;
        for (const k of Object.keys(seeds)) delete seeds[k];
        deriveSeed('stdlib_random');
        deriveSeed('numpy');
        deriveSeed('torch_cpu');
        deriveSeed('torch_cuda');
        deriveSeed('env_internal');
      },
      report() {
        return { masterSeed, seeds: { ...seeds } };
      },
    };
  },

  /**
   * Monitor policy entropy over time to detect exploration collapse or excess randomness.
   * @param {number[]} actionLogProbs - Array of log-probabilities of taken actions
   * @param {number} windowSize - Sliding window size
   * @returns {object} entropyAnalysis with per-window metrics and alerts
   */
  monitorEntropy(actionLogProbs, windowSize = 100) {
    if (!Array.isArray(actionLogProbs) || actionLogProbs.length === 0) {
      return { error: 'actionLogProbs must be a non-empty array' };
    }

    const entropies = [];
    const alerts = [];

    for (let i = 0; i + windowSize <= actionLogProbs.length; i += windowSize) {
      const window = actionLogProbs.slice(i, i + windowSize);
      // Approximate entropy from log-probs: H = -sum(p * log(p))
      // Using mean of -log_probs as proxy for entropy magnitude
      const meanNegLogProb = window.reduce((s, lp) => s - lp, 0) / window.length;
      entropies.push({
        step: i,
        entropyProxy: meanNegLogProb,
      });
    }

    // Detect exploration collapse (entropy → 0) or explosion
    if (entropies.length >= 2) {
      const first = entropies[0].entropyProxy;
      const last = entropies[entropies.length - 1].entropyProxy;
      const ratio = last / (first || 1e-8);

      if (ratio < 0.1) {
        alerts.push({ type: 'exploration_collapse', severity: 'high', message: 'Policy entropy dropped >90% — agent may be stuck in a deterministic mode' });
      } else if (ratio < 0.3) {
        alerts.push({ type: 'low_entropy', severity: 'medium', message: 'Policy entropy dropped significantly — agent may be converging prematurely' });
      } else if (ratio > 5) {
        alerts.push({ type: 'entropy_explosion', severity: 'high', message: 'Policy entropy increased >5x — agent may have lost learned policy' });
      }
    }

    return { entropies, alerts, windowSize };
  },

  /**
   * Inspect action distribution at a given state.
   * @param {number[]} actionProbs - Probability distribution over actions
   * @returns {object} distribution analysis (mode, entropy, uniformity)
   */
  inspectActionDistribution(actionProbs) {
    if (!Array.isArray(actionProbs) || actionProbs.length === 0) {
      return { error: 'actionProbs must be a non-empty array' };
    }

    const sum = actionProbs.reduce((a, b) => a + b, 0);
    if (Math.abs(sum - 1.0) > 0.01) {
      return { error: `actionProbs do not sum to 1.0 (sum=${sum.toFixed(4)})` };
    }

    const modeIdx = actionProbs.indexOf(Math.max(...actionProbs));
    const entropy = actionProbs.reduce((h, p) => (p > 0 ? h + p * Math.log2(p) : h), 0);
    const negEntropy = -entropy; // H = -Σ p*log(p), negate to make positive
    const maxEntropy = Math.log2(actionProbs.length);
    const uniformity = maxEntropy > 0 ? negEntropy / maxEntropy : 0;

    return {
      mode: { action: modeIdx, probability: actionProbs[modeIdx] },
      entropy: negEntropy,
      maxEntropy,
      uniformity, // 1.0 = perfectly uniform, 0.0 = deterministic
      isNearDeterministic: uniformity < 0.05,
      isNearUniform: uniformity > 0.95,
    };
  },
};

// ─────────────────────────────────────────────────────────────
// 2. Reproducibility Tools
// ─────────────────────────────────────────────────────────────

const reproducibilityTools = {
  /**
   * Create an episode recorder that captures full trajectories.
   * @returns {object} recorder with step(), getTrajectory(), reset() methods
   */
  createEpisodeRecorder() {
    let trajectory = [];
    let episodeCount = 0;
    let seed = null;

    return {
      setSeed(s) { seed = s; },
      step(observation, action, reward, done, info = {}) {
        trajectory.push({
          step: trajectory.length,
          observation,
          action,
          reward,
          done,
          info,
          seed,
        });
      },
      getTrajectory() {
        return {
          episodeId: episodeCount,
          seed,
          length: trajectory.length,
          totalReward: trajectory.reduce((s, t) => s + t.reward, 0),
          steps: [...trajectory],
        };
      },
      reset() {
        trajectory = [];
        episodeCount++;
        seed = null;
      },
    };
  },

  /**
   * Replay a recorded trajectory step-by-step, calling a callback for each step.
   * @param {object} trajectory - A trajectory object from createEpisodeRecorder
   * @param {function} callback - Called with (step, index) for each step
   * @param {object} [options] - Options: { fromStep, toStep, filterFn }
   * @returns {object} replay summary
   */
  replayTrajectory(trajectory, callback, options = {}) {
    if (!trajectory || !trajectory.steps) {
      return { error: 'Invalid trajectory: missing steps array' };
    }

    const { fromStep = 0, toStep = trajectory.steps.length, filterFn = null } = options;
    const steps = trajectory.steps.slice(fromStep, toStep);
    const filtered = filterFn ? steps.filter(filterFn) : steps;

    let callbackCount = 0;
    for (let i = 0; i < filtered.length; i++) {
      callback(filtered[i], i);
      callbackCount++;
    }

    return {
      totalSteps: trajectory.steps.length,
      replayed: callbackCount,
      filtered: steps.length - filtered.length,
      episodeId: trajectory.episodeId,
    };
  },

  /**
   * Compare two trajectories and find divergences.
   * @param {object} trajA - First trajectory
   * @param {object} trajB - Second trajectory
   * @param {object} [options] - Options: { compareFields, tolerance }
   * @returns {object} diff report with divergent steps
   */
  diffTrajectories(trajA, trajB, options = {}) {
    const { compareFields = ['observation', 'action', 'reward'], tolerance = 1e-6 } = options;

    if (!trajA.steps || !trajB.steps) {
      return { error: 'Both trajectories must have a steps array' };
    }

    const minLen = Math.min(trajA.steps.length, trajB.steps.length);
    const divergences = [];

    for (let i = 0; i < minLen; i++) {
      const stepA = trajA.steps[i];
      const stepB = trajB.steps[i];
      const diffs = {};

      for (const field of compareFields) {
        const valA = stepA[field];
        const valB = stepB[field];

        if (typeof valA === 'number' && typeof valB === 'number') {
          if (Math.abs(valA - valB) > tolerance) {
            diffs[field] = { a: valA, b: valB, delta: Math.abs(valA - valB) };
          }
        } else if (Array.isArray(valA) && Array.isArray(valB)) {
          const mismatch = valA.length !== valB.length ||
            valA.some((v, j) => typeof v === 'number' ? Math.abs(v - valB[j]) > tolerance : v !== valB[j]);
          if (mismatch) diffs[field] = { a: valA, b: valB };
        } else if (valA !== valB) {
          diffs[field] = { a: valA, b: valB };
        }
      }

      if (Object.keys(diffs).length > 0) {
        divergences.push({ step: i, diffs });
      }
    }

    return {
      lengthMismatch: trajA.steps.length !== trajB.steps.length,
      trajALength: trajA.steps.length,
      trajBLength: trajB.steps.length,
      divergenceCount: divergences.length,
      divergenceRate: divergences.length / (minLen || 1),
      divergences: divergences.slice(0, 50), // cap for readability
      firstDivergenceStep: divergences.length > 0 ? divergences[0].step : null,
    };
  },

  /**
   * Generate a deterministic seed cascade for parallel workers.
   * @param {number} masterSeed - Master seed
   * @param {number} numWorkers - Number of parallel workers
   * @param {number} seedsPerWorker - Seeds each worker needs
   * @returns {number[][]} 2D array of seeds [worker][seedIndex]
   */
  generateSeedCascade(masterSeed, numWorkers, seedsPerWorker = 1) {
    // Simple LCG-based PRNG for deterministic seed generation
    function lcg(seed) {
      let s = seed | 0;
      return function () {
        s = (s * 1664525 + 1013904223) | 0;
        return Math.abs(s);
      };
    }

    const rng = lcg(masterSeed);
    const cascade = [];

    for (let w = 0; w < numWorkers; w++) {
      const workerSeeds = [];
      for (let s = 0; s < seedsPerWorker; s++) {
        workerSeeds.push(rng());
      }
      cascade.push(workerSeeds);
    }

    // Verify no collisions
    const allSeeds = cascade.flat();
    const uniqueSeeds = new Set(allSeeds);
    if (uniqueSeeds.size !== allSeeds.length) {
      return { error: 'Seed collision detected — increase masterSeed or reduce workers', cascade: null };
    }

    return cascade;
  },
};

// ─────────────────────────────────────────────────────────────
// 3. Behavior Analysis
// ─────────────────────────────────────────────────────────────

const behaviorAnalysis = {
  /**
   * Cluster trajectories by similarity to identify behavioral modes.
   * Uses simple distance-based clustering on episode return + length.
   * @param {object[]} trajectories - Array of trajectory objects
   * @param {object} [options] - Options: { maxClusters, minClusterSize }
   * @returns {object} clustering result with clusters and outliers
   */
  clusterTrajectories(trajectories, options = {}) {
    const { maxClusters = 5, minClusterSize = 2 } = options;

    if (!Array.isArray(trajectories) || trajectories.length === 0) {
      return { error: 'trajectories must be a non-empty array' };
    }

    // Feature vector: [totalReward, length]
    const features = trajectories.map((t) => ({
      reward: t.totalReward || (t.steps ? t.steps.reduce((s, st) => s + st.reward, 0) : 0),
      length: t.length || (t.steps ? t.steps.length : 0),
      id: t.episodeId,
    }));

    // Normalize features
    const rewards = features.map((f) => f.reward);
    const lengths = features.map((f) => f.length);
    const rMin = Math.min(...rewards), rMax = Math.max(...rewards);
    const lMin = Math.min(...lengths), lMax = Math.max(...lengths);
    const rRange = rMax - rMin || 1;
    const lRange = lMax - lMin || 1;

    const normalized = features.map((f) => [
      (f.reward - rMin) / rRange,
      (f.length - lMin) / lRange,
    ]);

    // Simple k-means-ish clustering
    const clusters = [];
    const assigned = new Array(normalized.length).fill(-1);

    // Initialize: pick first point as centroid, then farthest points
    const centroids = [normalized[0].slice()];
    for (let k = 1; k < maxClusters; k++) {
      let maxDist = -1;
      let farthest = 0;
      for (let i = 0; i < normalized.length; i++) {
        const minDistToCentroid = Math.min(
          ...centroids.map((c) =>
            Math.sqrt(normalized[i].reduce((s, v, d) => s + (v - c[d]) ** 2, 0))
          )
        );
        if (minDistToCentroid > maxDist) {
          maxDist = minDistToCentroid;
          farthest = i;
        }
      }
      centroids.push(normalized[farthest].slice());
    }

    // Assign & iterate (3 rounds)
    for (let round = 0; round < 3; round++) {
      // Assign
      for (let i = 0; i < normalized.length; i++) {
        let bestK = 0;
        let bestDist = Infinity;
        for (let k = 0; k < centroids.length; k++) {
          const dist = Math.sqrt(normalized[i].reduce((s, v, d) => s + (v - centroids[k][d]) ** 2, 0));
          if (dist < bestDist) { bestDist = dist; bestK = k; }
        }
        assigned[i] = bestK;
      }

      // Update centroids
      for (let k = 0; k < centroids.length; k++) {
        const members = normalized.filter((_, i) => assigned[i] === k);
        if (members.length > 0) {
          centroids[k] = [
            members.reduce((s, m) => s + m[0], 0) / members.length,
            members.reduce((s, m) => s + m[1], 0) / members.length,
          ];
        }
      }
    }

    // Build clusters
    for (let k = 0; k < centroids.length; k++) {
      const members = features.filter((_, i) => assigned[i] === k);
      if (members.length >= minClusterSize) {
        clusters.push({
          clusterId: k,
          size: members.length,
          avgReward: members.reduce((s, m) => s + m.reward, 0) / members.length,
          avgLength: members.reduce((s, m) => s + m.length, 0) / members.length,
          episodes: members.map((m) => m.id),
        });
      }
    }

    const outliers = features.filter((_, i) => {
      const cluster = clusters.find((c) => c.episodes.includes(features[i].id));
      return !cluster;
    });

    return {
      clusterCount: clusters.length,
      clusters,
      outlierCount: outliers.length,
      outliers: outliers.map((o) => o.id),
    };
  },

  /**
   * Check policy consistency: does the same (or similar) state produce the same action distribution?
   * @param {object[]} stateActionPairs - Array of { state, actionProbs } entries
   * @param {object} [options] - Options: { stateTolerance, probTolerance }
   * @returns {object} consistency report
   */
  policyConsistencyCheck(stateActionPairs, options = {}) {
    const { stateTolerance = 1e-3, probTolerance = 0.05 } = options;

    if (!Array.isArray(stateActionPairs) || stateActionPairs.length < 2) {
      return { error: 'Need at least 2 state-action pairs for consistency check' };
    }

    const inconsistencies = [];
    const groups = new Map();

    // Group by state similarity
    for (let i = 0; i < stateActionPairs.length; i++) {
      const entry = stateActionPairs[i];
      let matched = false;

      for (const [key, group] of groups) {
        const existingState = group[0].state;
        if (Array.isArray(entry.state) && Array.isArray(existingState)) {
          const similar = entry.state.length === existingState.length &&
            entry.state.every((v, j) => Math.abs(v - existingState[j]) < stateTolerance);
          if (similar) {
            group.push(entry);
            matched = true;
            break;
          }
        } else if (entry.state === existingState) {
          group.push(entry);
          matched = true;
          break;
        }
      }

      if (!matched) {
        groups.set(`state_${i}`, [entry]);
      }
    }

    // Check action distribution consistency within each group
    for (const [key, group] of groups) {
      if (group.length < 2) continue;

      for (let i = 0; i < group.length; i++) {
        for (let j = i + 1; j < group.length; j++) {
          const probsA = group[i].actionProbs;
          const probsB = group[j].actionProbs;

          if (!Array.isArray(probsA) || !Array.isArray(probsB)) continue;
          if (probsA.length !== probsB.length) {
            inconsistencies.push({
              stateKey: key,
              pairIndices: [i, j],
              issue: 'action_dim_mismatch',
              dims: [probsA.length, probsB.length],
            });
            continue;
          }

          const maxDiff = Math.max(...probsA.map((p, k) => Math.abs(p - probsB[k])));
          if (maxDiff > probTolerance) {
            inconsistencies.push({
              stateKey: key,
              pairIndices: [i, j],
              issue: 'action_distribution_divergence',
              maxProbDiff: maxDiff,
            });
          }
        }
      }
    }

    return {
      stateGroups: groups.size,
      totalPairs: stateActionPairs.length,
      inconsistencyCount: inconsistencies.length,
      isConsistent: inconsistencies.length === 0,
      inconsistencies: inconsistencies.slice(0, 20),
    };
  },

  /**
   * Detect temporal correlations in action sequences (sign of non-Markov behavior).
   * @param {number[]} actions - Sequence of action indices
   * @param {number} maxLag - Maximum lag to check
   * @returns {object} correlation report
   */
  detectTemporalCorrelation(actions, maxLag = 5) {
    if (!Array.isArray(actions) || actions.length < maxLag + 10) {
      return { error: `Need at least ${maxLag + 10} actions for lag-${maxLag} correlation check` };
    }

    const uniqueActions = [...new Set(actions)];
    const correlations = [];

    for (const actionVal of uniqueActions) {
      const binary = actions.map((a) => (a === actionVal ? 1 : 0));
      const mean = binary.reduce((s, v) => s + v, 0) / binary.length;
      const variance = binary.reduce((s, v) => s + (v - mean) ** 2, 0) / binary.length;

      if (variance === 0) continue;

      for (let lag = 1; lag <= maxLag; lag++) {
        let autoCov = 0;
        const n = binary.length - lag;
        for (let i = 0; i < n; i++) {
          autoCov += (binary[i] - mean) * (binary[i + lag] - mean);
        }
        autoCov /= n;
        const autocorrelation = autoCov / variance;

        if (Math.abs(autocorrelation) > 0.3) {
          correlations.push({
            action: actionVal,
            lag,
            autocorrelation,
            severity: Math.abs(autocorrelation) > 0.7 ? 'high' : 'medium',
          });
        }
      }
    }

    return {
      totalActions: actions.length,
      uniqueActions: uniqueActions.length,
      significantCorrelations: correlations.length,
      correlations,
      hasTemporalCorrelation: correlations.length > 0,
    };
  },
};

// ─────────────────────────────────────────────────────────────
// 4. Reward Debugging
// ─────────────────────────────────────────────────────────────

const rewardDebugging = {
  /**
   * Decompose a multi-component reward into individual signals.
   * @param {object[]} steps - Array of { reward, rewardComponents?: { [name]: number } }
   * @returns {object} decomposition analysis
   */
  decomposeReward(steps) {
    if (!Array.isArray(steps) || steps.length === 0) {
      return { error: 'steps must be a non-empty array' };
    }

    const componentNames = new Set();
    for (const step of steps) {
      if (step.rewardComponents) {
        for (const name of Object.keys(step.rewardComponents)) {
          componentNames.add(name);
        }
      }
    }

    const components = {};
    for (const name of componentNames) {
      const values = steps
        .filter((s) => s.rewardComponents && s.rewardComponents[name] !== undefined)
        .map((s) => s.rewardComponents[name]);

      if (values.length === 0) continue;

      const total = values.reduce((a, b) => a + b, 0);
      const mean = total / values.length;
      const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length;

      components[name] = {
        total,
        mean,
        variance,
        stdDev: Math.sqrt(variance),
        min: Math.min(...values),
        max: Math.max(...values),
        sparsity: values.filter((v) => v === 0).length / values.length,
        count: values.length,
      };
    }

    const totalRewards = steps.map((s) => s.reward || 0);
    const totalRewardSum = totalRewards.reduce((a, b) => a + b, 0);

    // Check if component sums match total
    let componentSumTotal = 0;
    for (const name of componentNames) {
      componentSumTotal += components[name] ? components[name].total : 0;
    }

    return {
      episodeLength: steps.length,
      totalReward: totalRewardSum,
      componentCount: componentNames.size,
      components,
      sumMatchesTotal: Math.abs(componentSumTotal - totalRewardSum) < 0.01,
      dominantComponent: Object.entries(components).sort(
        (a, b) => Math.abs(b[1].total) - Math.abs(a[1].total)
      )[0]?.[0] || null,
    };
  },

  /**
   * Analyze reward scale to detect component mismatches.
   * @param {object} decomposition - Output from decomposeReward
   * @returns {object} scale analysis with alerts
   */
  analyzeRewardScale(decomposition) {
    if (!decomposition || !decomposition.components) {
      return { error: 'Invalid decomposition input' };
    }

    const alerts = [];
    const scales = {};

    for (const [name, stats] of Object.entries(decomposition.components)) {
      scales[name] = {
        range: stats.max - stats.min,
        stdDev: stats.stdDev,
        magnitude: Math.max(Math.abs(stats.max), Math.abs(stats.min), Math.abs(stats.mean)),
      };
    }

    // Detect scale mismatches (one component dominates by >100x)
    const magnitudes = Object.entries(scales).map(([name, s]) => ({ name, mag: s.magnitude }));
    if (magnitudes.length >= 2) {
      magnitudes.sort((a, b) => b.mag - a.mag);
      const maxMag = magnitudes[0].mag;
      const minMag = magnitudes[magnitudes.length - 1].mag;

      if (maxMag > 0 && minMag / maxMag < 0.01) {
        alerts.push({
          type: 'scale_mismatch',
          severity: 'high',
          message: `Reward component "${magnitudes[0].name}" dominates by >100x over "${magnitudes[magnitudes.length - 1].name}"`,
          ratio: maxMag / (minMag || 1e-8),
        });
      }
    }

    // Detect zero-variance components (constant reward — likely a bug or useless signal)
    for (const [name, stats] of Object.entries(decomposition.components)) {
      if (stats.variance === 0 && stats.mean !== 0) {
        alerts.push({
          type: 'zero_variance',
          severity: 'medium',
          message: `Reward component "${name}" has zero variance (constant = ${stats.mean})`,
          component: name,
        });
      }
    }

    // Detect extreme sparsity (reward active <1% of steps)
    for (const [name, stats] of Object.entries(decomposition.components)) {
      if (stats.sparsity > 0.99 && stats.mean !== 0) {
        alerts.push({
          type: 'extreme_sparsity',
          severity: 'low',
          message: `Reward component "${name}" is non-zero only ${((1 - stats.sparsity) * 100).toFixed(1)}% of steps`,
          component: name,
        });
      }
    }

    return { scales, alerts, alertCount: alerts.length };
  },

  /**
   * Trace sparse reward events: for each reward > threshold, show the trajectory context.
   * @param {object[]} steps - Array of step objects with { reward, ... }
   * @param {number} [threshold] - Reward magnitude threshold for "interesting" events
   * @param {number} [contextWindow] - Steps before/after to include as context
   * @returns {object} sparse reward trace
   */
  traceSparseRewards(steps, threshold = 0.01, contextWindow = 5) {
    if (!Array.isArray(steps) || steps.length === 0) {
      return { error: 'steps must be a non-empty array' };
    }

    const events = [];
    for (let i = 0; i < steps.length; i++) {
      if (Math.abs(steps[i].reward || 0) > threshold) {
        const startIdx = Math.max(0, i - contextWindow);
        const endIdx = Math.min(steps.length - 1, i + contextWindow);
        events.push({
          step: i,
          reward: steps[i].reward,
          contextStart: startIdx,
          contextEnd: endIdx,
          context: steps.slice(startIdx, endIdx + 1).map((s, j) => ({
            relativeStep: startIdx + j - i,
            reward: s.reward,
            action: s.action,
          })),
        });
      }
    }

    return {
      totalSteps: steps.length,
      rewardEventCount: events.length,
      rewardDensity: events.length / steps.length,
      events,
    };
  },

  /**
   * Detect potential reward hacking: agent achieves high reward via unintended strategies.
   * Flags when reward increases monotonically while domain-specific heuristics degrade.
   * @param {object[]} episodes - Array of { reward, heuristicScores: { [name]: number } }
   * @returns {object} hacking detection report
   */
  detectRewardHacking(episodes) {
    if (!Array.isArray(episodes) || episodes.length < 3) {
      return { error: 'Need at least 3 episodes for hacking detection' };
    }

    const alerts = [];
    const rewards = episodes.map((e) => e.reward || 0);

    // Check for monotonic reward increase with degrading heuristics
    const heuristicNames = new Set();
    for (const ep of episodes) {
      if (ep.heuristicScores) {
        for (const name of Object.keys(ep.heuristicScores)) {
          heuristicNames.add(name);
        }
      }
    }

    // Simple trend detection: compare first third vs last third
    const third = Math.floor(episodes.length / 3);
    const earlyRewards = rewards.slice(0, third);
    const lateRewards = rewards.slice(-third);
    const earlyMean = earlyRewards.reduce((a, b) => a + b, 0) / earlyRewards.length;
    const lateMean = lateRewards.reduce((a, b) => a + b, 0) / lateRewards.length;

    const rewardIncreasing = lateMean > earlyMean;

    for (const name of heuristicNames) {
      const earlyH = episodes.slice(0, third).filter((e) => e.heuristicScores?.[name] !== undefined);
      const lateH = episodes.slice(-third).filter((e) => e.heuristicScores?.[name] !== undefined);

      if (earlyH.length === 0 || lateH.length === 0) continue;

      const earlyHMean = earlyH.reduce((s, e) => s + e.heuristicScores[name], 0) / earlyH.length;
      const lateHMean = lateH.reduce((s, e) => s + e.heuristicScores[name], 0) / lateH.length;

      if (rewardIncreasing && lateHMean < earlyHMean * 0.8) {
        alerts.push({
          type: 'reward_hacking_suspected',
          severity: 'high',
          message: `Reward increasing while heuristic "${name}" degrading (${earlyHMean.toFixed(2)} → ${lateHMean.toFixed(2)})`,
          heuristic: name,
          earlyValue: earlyHMean,
          lateValue: lateHMean,
        });
      }
    }

    // Check for reward stagnation (agent stops improving)
    if (!rewardIncreasing && Math.abs(lateMean - earlyMean) < Math.abs(earlyMean) * 0.05) {
      alerts.push({
        type: 'reward_stagnation',
        severity: 'medium',
        message: 'Reward has stagnated — agent may be stuck at local optimum',
        earlyMean,
        lateMean,
      });
    }

    return {
      episodeCount: episodes.length,
      rewardTrend: rewardIncreasing ? 'increasing' : (lateMean < earlyMean ? 'decreasing' : 'stagnant'),
      alertCount: alerts.length,
      alerts,
    };
  },

  /**
   * Sanity check for discounted return computation.
   * @param {number[]} rewards - Array of per-step rewards
   * @param {number} [gamma] - Discount factor
   * @returns {object} validation result
   */
  validateReturnComputation(rewards, gamma = 0.99) {
    if (!Array.isArray(rewards) || rewards.length === 0) {
      return { error: 'rewards must be a non-empty array' };
    }

    if (gamma < 0 || gamma >= 1) {
      return { error: 'gamma must be in [0, 1)' };
    }

    // Forward computation
    let discountedSum = 0;
    let discountFactor = 1;
    const stepReturns = [];

    for (let i = 0; i < rewards.length; i++) {
      discountedSum += discountFactor * rewards[i];
      stepReturns.push(discountedSum);
      discountFactor *= gamma;
    }

    // Backward computation (reverse)
    let reverseSum = 0;
    for (let i = rewards.length - 1; i >= 0; i--) {
      reverseSum = rewards[i] + gamma * reverseSum;
    }

    // They should match for the total
    const match = Math.abs(discountedSum - reverseSum) < 1e-10;

    // Check for common bugs
    const alerts = [];
    if (gamma === 1.0) {
      alerts.push({ type: 'no_discounting', severity: 'high', message: 'gamma=1.0 means no discounting — returns may diverge for infinite horizons' });
    }

    const effectiveHorizon = gamma < 1 ? Math.ceil(Math.log(0.01) / Math.log(gamma)) : Infinity;
    if (effectiveHorizon < rewards.length / 3) {
      alerts.push({
        type: 'short_horizon',
        severity: 'low',
        message: `Effective horizon (${effectiveHorizon} steps) is much shorter than episode length (${rewards.length} steps) — later rewards have negligible impact`,
      });
    }

    return {
      totalReturn: discountedSum,
      gamma,
      effectiveHorizon,
      forwardBackwardMatch: match,
      stepReturns,
      alerts,
    };
  },
};

// ─────────────────────────────────────────────────────────────
// Exports
// ─────────────────────────────────────────────────────────────

module.exports = {
  stochasticityControl,
  reproducibilityTools,
  behaviorAnalysis,
  rewardDebugging,
};