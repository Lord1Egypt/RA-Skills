export function calculateScore(F, C, E, S, R) {
  const weights = [1, 1, 1, 1, 1];

  const numerator = Math.pow(F, weights[0]) *
                    Math.pow(C, weights[1]) *
                    Math.pow(E, weights[2]) *
                    Math.pow(S, weights[3]) *
                    Math.pow(R, weights[4]);

  const maxVal = Math.max(F, C, E, S, R);

  const score = Math.pow(numerator / maxVal, 1 / weights.length);

  return Number(score.toFixed(2));
}
export function runningAverage(scores, decay = 0.8) {
  let weightedSum = 0;
  let totalWeight = 0;

  scores.forEach((s, i) => {
    const weight = Math.pow(decay, scores.length - i - 1);
    weightedSum += s * weight;
    totalWeight += weight;
  });

  return Number((weightedSum / totalWeight).toFixed(2));
}