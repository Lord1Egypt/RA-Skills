#!/usr/bin/env node
/**
 * Critic Score Helper
 * Computes weighted overall score and verdict from dimension scores.
 *
 * Usage: echo '{"correctness":85,"clarity":90,"completeness":70,"safety":95}' | node compute-score.js
 */

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

let input = '';
rl.on('line', (line) => {
  input += line;
});

rl.on('close', () => {
  try {
    const scores = JSON.parse(input);
    const weights = {
      correctness: 0.40,
      clarity: 0.25,
      completeness: 0.25,
      safety: 0.10
    };

    // Validate scores are numbers 0-100
    for (const [dim, weight] of Object.entries(weights)) {
      if (typeof scores[dim] !== 'number' || scores[dim] < 0 || scores[dim] > 100) {
        throw new Error(`${dim} score must be a number between 0 and 100`);
      }
    }

    // Compute weighted sum
    const overall = Object.entries(weights).reduce(
      (sum, [dim, weight]) => sum + scores[dim] * weight,
      0
    );

    // Determine verdict
    let verdict;
    if (overall >= 80) {
      verdict = 'excellent';
    } else if (overall >= 70) {
      verdict = 'good';
    } else if (overall >= 50) {
      verdict = 'needsRevision';
    } else {
      verdict = 'fail';
    }

    const result = {
      score: Math.round(overall * 10) / 10, // one decimal
      verdict,
      breakdown: {
        correctness: {
          score: scores.correctness,
          weight: weights.correctness,
          contribution: Math.round(scores.correctness * weights.correctness * 10) / 10
        },
        clarity: {
          score: scores.clarity,
          weight: weights.clarity,
          contribution: Math.round(scores.clarity * weights.clarity * 10) / 10
        },
        completeness: {
          score: scores.completeness,
          weight: weights.completeness,
          contribution: Math.round(scores.completeness * weights.completeness * 10) / 10
        },
        safety: {
          score: scores.safety,
          weight: weights.safety,
          contribution: Math.round(scores.safety * weights.safety * 10) / 10
        }
      }
    };

    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (error) {
    console.error(JSON.stringify({ error: error.message }));
    process.exit(1);
  }
});
