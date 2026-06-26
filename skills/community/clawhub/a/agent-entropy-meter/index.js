'use strict';

/**
 * agent-entropy-meter
 * Measure information entropy and redundancy in agent group communications.
 */

/**
 * Shannon entropy H(X) = -Σ p(xi) log2 p(xi)
 * @param {number[]} probabilities - Array of probabilities (must sum to ~1)
 * @returns {number} Entropy in bits
 */
function shannonEntropy(probabilities) {
  let h = 0;
  for (const p of probabilities) {
    if (p > 0) {
      h -= p * Math.log2(p);
    }
  }
  return h;
}

/**
 * Maximum entropy for N categories = log2(N)
 * @param {number} n - Number of distinct categories
 * @returns {number} Max entropy in bits
 */
function maxEntropy(n) {
  return n > 1 ? Math.log2(n) : 0;
}

/**
 * Redundancy ratio R = 1 - H(X)/H_max
 * 0 = no redundancy (max diversity), 1 = total redundancy (single category)
 * @param {number[]} probabilities - Message category probability distribution
 * @returns {number} Redundancy ratio [0, 1]
 */
function redundancyRatio(probabilities) {
  const n = probabilities.filter(p => p > 0).length;
  if (n <= 1) return 1; // Single category = total redundancy
  const h = shannonEntropy(probabilities);
  const hMax = maxEntropy(n);
  return hMax > 0 ? 1 - (h / hMax) : 1;
}

/**
 * Build frequency distribution from raw messages.
 * @param {string[]} messages - Array of message category labels
 * @returns {number[]} Probability distribution
 */
function buildDistribution(messages) {
  if (!messages || messages.length === 0) return [];
  const counts = {};
  for (const m of messages) {
    counts[m] = (counts[m] || 0) + 1;
  }
  const total = messages.length;
  return Object.values(counts).map(c => c / total);
}

/**
 * Compute joint distribution for two agents' messages.
 * @param {string[]} msgsA - Agent A's message categories
 * @param {string[]} msgsB - Agent B's message categories
 * @param {string[]} allCategories - Union of all categories
 * @returns {{ joint: number[][], pA: number[], pB: number[] }}
 */
function jointDistribution(msgsA, msgsB, allCategories) {
  const n = allCategories.length;
  const catIndex = {};
  allCategories.forEach((c, i) => { catIndex[c] = i; });

  // Initialize joint count matrix
  const jointCounts = Array.from({ length: n }, () => new Array(n).fill(0));
  const countA = new Array(n).fill(0);
  const countB = new Array(n).fill(0);

  const minLen = Math.min(msgsA.length, msgsB.length);
  for (let i = 0; i < minLen; i++) {
    const idxA = catIndex[msgsA[i]];
    const idxB = catIndex[msgsB[i]];
    if (idxA !== undefined && idxB !== undefined) {
      jointCounts[idxA][idxB]++;
      countA[idxA]++;
      countB[idxB]++;
    }
  }

  const total = minLen || 1;
  const joint = jointCounts.map(row => row.map(c => c / total));
  const pA = countA.map(c => c / total);
  const pB = countB.map(c => c / total);

  return { joint, pA, pB };
}

/**
 * Mutual information I(A;B) = H(A) + H(B) - H(A,B)
 * @param {string[]} msgsA - Agent A's message categories
 * @param {string[]} msgsB - Agent B's message categories
 * @param {string[]} [allCategories] - Union of categories (auto-derived if omitted)
 * @returns {{ mutualInfo: number, hA: number, hB: number, hJoint: number }}
 */
function mutualInformation(msgsA, msgsB, allCategories) {
  if (!allCategories) {
    const set = new Set([...msgsA, ...msgsB]);
    allCategories = [...set];
  }

  const { joint, pA, pB } = jointDistribution(msgsA, msgsB, allCategories);
  const hA = shannonEntropy(pA.filter(p => p > 0));
  const hB = shannonEntropy(pB.filter(p => p > 0));

  // Joint entropy
  let hJoint = 0;
  for (const row of joint) {
    for (const p of row) {
      if (p > 0) {
        hJoint -= p * Math.log2(p);
      }
    }
  }

  const mutualInfo = hA + hB - hJoint;
  return { mutualInfo: Math.max(0, mutualInfo), hA, hB, hJoint };
}

/**
 * Knowledge overlap (Jaccard coefficient) between two topic sets.
 * @param {string[]|Set} setA - Agent A's topics
 * @param {string[]|Set} setB - Agent B's topics
 * @returns {number} Overlap coefficient [0, 1]
 */
function knowledgeOverlap(setA, setB) {
  const a = new Set(Array.isArray(setA) ? setA : []);
  const b = new Set(Array.isArray(setB) ? setB : []);
  if (a.size === 0 && b.size === 0) return 0;
  let intersection = 0;
  for (const item of a) {
    if (b.has(item)) intersection++;
  }
  const union = new Set([...a, ...b]).size;
  return union > 0 ? intersection / union : 0;
}

/**
 * ASCII bar chart helper
 * @param {number} value - Value in [0,1]
 * @param {number} width - Bar width in chars
 * @returns {string}
 */
function barChart(value, width = 20) {
  const filled = Math.round(value * width);
  return '[' + '█'.repeat(filled) + '░'.repeat(width - filled) + ']';
}

/**
 * Generate a full entropy & redundancy report for agent group data.
 * @param {Object} agentData - { agents: { name: string, messages: string[], topics: string[] }[] }
 * @returns {string} Human-readable report
 */
function report(agentData) {
  const agents = agentData.agents || [];
  if (agents.length === 0) return 'No agent data provided.';

  const lines = [];
  lines.push('═══════════════════════════════════════════');
  lines.push('  Agent Group Entropy & Redundancy Report  ');
  lines.push('═══════════════════════════════════════════');
  lines.push('');

  // Per-agent entropy & redundancy
  lines.push('── Per-Agent Metrics ──');
  for (const agent of agents) {
    const dist = buildDistribution(agent.messages || []);
    const h = dist.length > 0 ? shannonEntropy(dist) : 0;
    const hMax = maxEntropy(dist.filter(p => p > 0).length);
    const r = dist.length > 0 ? redundancyRatio(dist) : 1;
    lines.push(`  ${agent.name}:`);
    lines.push(`    Entropy H  = ${h.toFixed(3)} / ${hMax.toFixed(3)} bits  ${barChart(hMax > 0 ? h / hMax : 0)}`);
    lines.push(`    Redundancy = ${(r * 100).toFixed(1)}%  ${barChart(r)}`);
  }
  lines.push('');

  // Pairwise mutual information
  if (agents.length >= 2) {
    lines.push('── Pairwise Mutual Information ──');
    for (let i = 0; i < agents.length; i++) {
      for (let j = i + 1; j < agents.length; j++) {
        const a = agents[i];
        const b = agents[j];
        const allCats = [...new Set([...(a.messages || []), ...(b.messages || [])])];
        const mi = mutualInformation(a.messages || [], b.messages || [], allCats);
        const normMI = mi.hA > 0 && mi.hB > 0
          ? mi.mutualInfo / Math.min(mi.hA, mi.hB)
          : 0;
        lines.push(`  ${a.name} ↔ ${b.name}:`);
        lines.push(`    I(A;B)     = ${mi.mutualInfo.toFixed(3)} bits`);
        lines.push(`    Normalized = ${(normMI * 100).toFixed(1)}%  ${barChart(normMI)}`);
        lines.push(`    H(A)=${mi.hA.toFixed(2)} H(B)=${mi.hB.toFixed(2)} H(A,B)=${mi.hJoint.toFixed(2)}`);
      }
    }
    lines.push('');
  }

  // Knowledge overlap
  if (agents.length >= 2) {
    lines.push('── Knowledge Overlap (Jaccard) ──');
    for (let i = 0; i < agents.length; i++) {
      for (let j = i + 1; j < agents.length; j++) {
        const ko = knowledgeOverlap(agents[i].topics || [], agents[j].topics || []);
        lines.push(`  ${agents[i].name} ↔ ${agents[j].name}: ${(ko * 100).toFixed(1)}%  ${barChart(ko)}`);
      }
    }
    lines.push('');
  }

  // Group-level summary
  const allMessages = agents.flatMap(a => a.messages || []);
  const groupDist = buildDistribution(allMessages);
  const groupH = groupDist.length > 0 ? shannonEntropy(groupDist) : 0;
  const groupR = groupDist.length > 0 ? redundancyRatio(groupDist) : 1;
  lines.push('── Group Summary ──');
  lines.push(`  Total messages: ${allMessages.length}`);
  lines.push(`  Distinct categories: ${groupDist.filter(p => p > 0).length}`);
  lines.push(`  Group entropy: ${groupH.toFixed(3)} bits`);
  lines.push(`  Group redundancy: ${(groupR * 100).toFixed(1)}%  ${barChart(groupR)}`);
  lines.push('');

  // Diagnosis
  lines.push('── Diagnosis ──');
  if (groupR > 0.6) {
    lines.push('  ⚠ HIGH REDUNDANCY: Agent group acts as echo chamber. Consider diversifying roles.');
  } else if (groupR > 0.3) {
    lines.push('  ⚡ MODERATE REDUNDANCY: Some overlap exists. Review pairwise MI for hotspots.');
  } else {
    lines.push('  ✅ LOW REDUNDANCY: Good information diversity across agents.');
  }
  lines.push('═══════════════════════════════════════════');

  return lines.join('\n');
}

module.exports = {
  shannonEntropy,
  maxEntropy,
  redundancyRatio,
  buildDistribution,
  jointDistribution,
  mutualInformation,
  knowledgeOverlap,
  barChart,
  report
};