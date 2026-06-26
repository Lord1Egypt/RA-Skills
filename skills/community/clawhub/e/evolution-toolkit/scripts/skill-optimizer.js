#!/usr/bin/env node
/**
 * skill-optimizer.js - Iterative playbook optimizer
 *
 * Pattern:
 *   run playbook -> evaluate output -> diagnose gaps -> improve prompt -> repeat
 *
 * Usage:
 *   node scripts/skill-optimizer.js --config ./config.json --skill customer-support --iterations 3
 *   node scripts/skill-optimizer.js --config ./config.json --skill customer-support --eval-only
 *   node scripts/skill-optimizer.js --config ./config.json --report
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const WORKSPACE = process.env.EVOLUTION_TOOLKIT_WORKSPACE
  || (process.env.HOME ? require('path').join(process.env.HOME, '.openclaw/workspace') : process.cwd());
const TOOLKIT_ROOT = path.resolve(__dirname, '..');
const HISTORY_PATH = path.join(WORKSPACE, 'memory', 'skill-optimizer-history.json');

function parseFlags(argv) {
  const flags = {};
  argv.forEach((arg, i) => {
    if (!arg.startsWith('--')) return;
    const key = arg.slice(2);
    const next = argv[i + 1];
    flags[key] = next && !next.startsWith('--') ? next : true;
  });
  return flags;
}

function ensureWritableDir(dirPath, label) {
  try {
    fs.mkdirSync(dirPath, { recursive: true });
    fs.accessSync(dirPath, fs.constants.W_OK);
  } catch (err) {
    console.error(`Write access required: ${label}`);
    console.error(dirPath);
    console.error('Set EVOLUTION_TOOLKIT_WORKSPACE to a writable workspace and try again.');
    process.exit(1);
  }
}

function fileExists(filePath) {
  try {
    fs.accessSync(filePath, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

function resolvePathMaybe(value, baseDir = TOOLKIT_ROOT) {
  if (!value) return value;
  if (path.isAbsolute(value)) return value;

  const candidates = [
    path.resolve(baseDir, value),
    path.resolve(TOOLKIT_ROOT, value),
    path.resolve(WORKSPACE, value),
  ];

  return candidates.find(fileExists) || path.resolve(baseDir, value);
}

function loadSecrets() {
  const secretsPath = path.join(WORKSPACE, '.secrets');
  const secrets = {};
  if (!fileExists(secretsPath)) return secrets;

  fs.readFileSync(secretsPath, 'utf8').split('\n').forEach((line) => {
    const match = line.match(/^([A-Z0-9_]+)=(.+)$/);
    if (match) secrets[match[1]] = match[2].trim();
  });
  return secrets;
}

function getApiKey(config = {}) {
  const envKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
  if (envKey) return envKey;

  const secrets = loadSecrets();
  if (secrets.GEMINI_API_KEY) return secrets.GEMINI_API_KEY;
  if (secrets.GOOGLE_API_KEY) return secrets.GOOGLE_API_KEY;

  if (config.apiKeyEnvVar && process.env[config.apiKeyEnvVar]) {
    return process.env[config.apiKeyEnvVar];
  }

  return null;
}

function getConfigPath(flags) {
  if (flags.config) return path.resolve(process.cwd(), flags.config);
  const localConfig = path.join(TOOLKIT_ROOT, 'config.json');
  if (fileExists(localConfig)) return localConfig;
  return null;
}

function loadOptimizerConfig(configPath) {
  if (!configPath || !fileExists(configPath)) {
    console.error('Config file not found. Pass --config /path/to/config.json.');
    process.exit(1);
  }

  const raw = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const baseDir = path.dirname(configPath);
  const skills = raw.skillOptimizer?.skills || raw.skills;

  if (!skills || typeof skills !== 'object') {
    console.error('Config must include skillOptimizer.skills or skills.');
    process.exit(1);
  }

  const normalized = {};
  for (const [skillName, skill] of Object.entries(skills)) {
    const promptPath = resolvePathMaybe(skill.promptPath, baseDir);
    const outputPath = resolvePathMaybe(skill.outputPath || promptPath, baseDir);
    normalized[skillName] = {
      name: skill.name || skillName,
      promptPath,
      outputPath,
      generatorPrompt: skill.generatorPrompt || 'Produce the requested output using the playbook exactly.',
      model: skill.model || raw.skillOptimizer?.model || 'gemini-2.5-flash-lite',
      improvementModel: skill.improvementModel || raw.skillOptimizer?.improvementModel || skill.model || 'gemini-2.5-flash-lite',
      testCases: skill.testCases || [],
      evalCriteria: skill.evalCriteria || [],
    };
  }

  return {
    raw,
    skills: normalized,
  };
}

async function callGemini(prompt, apiKey, model = 'gemini-2.5-flash-lite') {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 2048 }
    });

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/${model}:generateContent?key=${apiKey}`,
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const text = json.candidates?.[0]?.content?.parts?.[0]?.text;
          if (!text) {
            reject(new Error(`No text in response: ${data.slice(0, 200)}`));
            return;
          }
          resolve(text);
        } catch (err) {
          reject(new Error(`Parse error: ${err.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function generateOutput(skill, testCase, playbook, apiKey) {
  const prompt = `You are improving a reusable playbook through realistic task trials.

TASK CASE:
${JSON.stringify(testCase, null, 2)}

PLAYBOOK:
"""
${playbook}
"""

GENERATION INSTRUCTION:
${skill.generatorPrompt}

Output ONLY the final artifact for this test case.`;

  return callGemini(prompt, apiKey, skill.model);
}

async function evaluateOutput(output, testCase, criteria, apiKey, model) {
  const criteriaList = criteria.map((c, i) => `${i + 1}. ${c.name}: ${c.description}`).join('\n');
  const prompt = `You are a strict evaluator for playbook outputs.

TASK CASE:
${JSON.stringify(testCase, null, 2)}

OUTPUT TO EVALUATE:
"""
${output}
"""

CRITERIA (score each 0-10, where 10 is perfect):
${criteriaList}

Return EXACTLY this JSON:
{"scores":[{"name":"<criterion_name>","score":0,"note":"<brief note>"}],"overall_note":"<brief overall note>"}`;

  const result = await callGemini(prompt, apiKey, model);
  const jsonMatch = result.match(/\{[\s\S]*\}/);
  if (!jsonMatch) return null;
  return JSON.parse(jsonMatch[0]);
}

function diagnoseWeaknesses(evalResults, criteria) {
  const avgScores = {};
  criteria.forEach((criterion) => {
    avgScores[criterion.name] = {
      total: 0,
      count: 0,
      weight: criterion.weight,
      notes: [],
    };
  });

  evalResults.forEach((result) => {
    if (!result?.scores) return;
    result.scores.forEach((score) => {
      if (!avgScores[score.name]) return;
      avgScores[score.name].total += score.score;
      avgScores[score.name].count += 1;
      if (score.note) avgScores[score.name].notes.push(score.note);
    });
  });

  const weaknesses = Object.entries(avgScores).map(([name, data]) => {
    const avg = data.count > 0 ? data.total / data.count : 0;
    return {
      name,
      avgScore: Math.round(avg * 10) / 10,
      weightedScore: Math.round(avg * data.weight * 10) / 10,
      weight: data.weight,
      sampleNotes: data.notes.slice(0, 3),
    };
  });

  weaknesses.sort((a, b) => a.weightedScore - b.weightedScore);
  return weaknesses;
}

async function improvePlaybook(currentPlaybook, weaknesses, apiKey, model) {
  const weakStr = weaknesses.slice(0, 4).map((weakness) =>
    `- ${weakness.name} (avg: ${weakness.avgScore}/10, weight: ${weakness.weight}x): ${weakness.sampleNotes.join(' | ')}`
  ).join('\n');

  const prompt = `You are revising a reusable playbook based on evaluation data.

CURRENT PLAYBOOK:
"""
${currentPlaybook.slice(0, 4000)}
"""

TOP WEAKNESSES:
${weakStr}

RULES:
- Keep the structure unless a weakness clearly requires a change
- Preserve strong instructions
- Add specific rules, not vague advice
- Keep it concise and practical

Output ONLY the improved playbook text.`;

  return callGemini(prompt, apiKey, model);
}

function loadHistory() {
  try {
    return JSON.parse(fs.readFileSync(HISTORY_PATH, 'utf8'));
  } catch {
    return [];
  }
}

function saveHistory(history) {
  ensureWritableDir(path.dirname(HISTORY_PATH), 'The optimization history directory is not writable.');
  fs.writeFileSync(HISTORY_PATH, JSON.stringify(history, null, 2));
}

function validateSkill(skillName, skill) {
  if (!fileExists(skill.promptPath)) {
    console.error(`Prompt file not found for ${skillName}: ${skill.promptPath}`);
    process.exit(1);
  }
  if (!Array.isArray(skill.testCases) || skill.testCases.length === 0) {
    console.error(`Skill ${skillName} must define at least one test case.`);
    process.exit(1);
  }
  if (!Array.isArray(skill.evalCriteria) || skill.evalCriteria.length === 0) {
    console.error(`Skill ${skillName} must define at least one evaluation criterion.`);
    process.exit(1);
  }
}

async function optimize(skillName, skill, iterations, dryRun, apiKey) {
  validateSkill(skillName, skill);
  let playbook = fs.readFileSync(skill.promptPath, 'utf8');
  let history = loadHistory();

  console.log(`\nSkill Optimizer - ${skill.name}`);
  console.log(`Iterations: ${iterations} | Test cases: ${skill.testCases.length} | Criteria: ${skill.evalCriteria.length}`);
  console.log(dryRun ? 'Mode: DRY RUN\n' : 'Mode: LIVE\n');

  let bestScore = 0;
  let bestPlaybook = playbook;
  let bestIteration = -1;

  for (let iter = 0; iter < iterations; iter += 1) {
    console.log(`Iteration ${iter + 1}/${iterations}`);
    const replies = [];

    for (const testCase of skill.testCases) {
      process.stdout.write(`  Generate ${testCase.id || testCase.name || 'case'}...`);
      try {
        const reply = await generateOutput(skill, testCase, playbook, apiKey);
        replies.push({ testCase, reply });
        console.log(` ok (${reply.split(/\s+/).length} words)`);
      } catch (err) {
        console.log(` failed: ${err.message}`);
      }
      await new Promise((resolve) => setTimeout(resolve, 1500));
    }

    const evalResults = [];
    for (const { testCase, reply } of replies) {
      process.stdout.write(`  Evaluate ${testCase.id || testCase.name || 'case'}...`);
      try {
        const result = await evaluateOutput(reply, testCase, skill.evalCriteria, apiKey, skill.improvementModel);
        evalResults.push(result);
        if (result?.scores) {
          const avg = result.scores.reduce((sum, item) => sum + item.score, 0) / result.scores.length;
          console.log(` ${avg.toFixed(1)}/10`);
        } else {
          console.log(' no scores');
        }
      } catch (err) {
        console.log(` failed: ${err.message}`);
      }
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    const weaknesses = diagnoseWeaknesses(evalResults, skill.evalCriteria);
    const totalWeighted = weaknesses.reduce((sum, weakness) => sum + weakness.weightedScore, 0);
    const totalWeight = weaknesses.reduce((sum, weakness) => sum + weakness.weight, 0) || 1;
    const overallScore = totalWeighted / totalWeight;

    console.log(`  Overall weighted score: ${overallScore.toFixed(2)}/10`);
    weaknesses.slice(0, 3).forEach((weakness) => {
      console.log(`  Weakest: ${weakness.name} ${weakness.avgScore}/10 (${weakness.weight}x)`);
    });

    if (overallScore > bestScore) {
      bestScore = overallScore;
      bestPlaybook = playbook;
      bestIteration = iter;
    }

    history.push({
      skill: skillName,
      iteration: iter,
      timestamp: new Date().toISOString(),
      overallScore: Math.round(overallScore * 100) / 100,
      weaknesses: weaknesses.map((weakness) => ({ name: weakness.name, avg: weakness.avgScore })),
      sampleOutput: replies[0]?.reply?.slice(0, 300),
      improved: iter < iterations - 1,
    });

    if (iter < iterations - 1) {
      process.stdout.write('  Improve playbook...');
      try {
        const improved = await improvePlaybook(playbook, weaknesses, apiKey, skill.improvementModel);
        if (improved && improved.length > 100) {
          playbook = improved;
          console.log(' ok');
        } else {
          console.log(' skipped');
        }
      } catch (err) {
        console.log(` failed: ${err.message}`);
      }
      await new Promise((resolve) => setTimeout(resolve, 1500));
    }
  }

  saveHistory(history);
  console.log(`History saved: ${HISTORY_PATH}`);

  if (!dryRun && bestIteration >= 0) {
    ensureWritableDir(path.dirname(skill.outputPath), 'The optimized playbook directory is not writable.');
    fs.writeFileSync(skill.outputPath, bestPlaybook);
    console.log(`Best playbook saved: ${skill.outputPath}`);
  }

  console.log(`Best score: ${bestScore.toFixed(2)}/10 (iteration ${bestIteration + 1})`);
}

async function evalOnly(skillName, skill, apiKey) {
  validateSkill(skillName, skill);
  const playbook = fs.readFileSync(skill.promptPath, 'utf8');
  const allEvals = [];

  console.log(`\nEvaluating ${skill.name} (${skill.testCases.length} cases)\n`);
  for (const testCase of skill.testCases) {
    process.stdout.write(`  ${testCase.id || testCase.name || 'case'}...`);
    try {
      const output = await generateOutput(skill, testCase, playbook, apiKey);
      const result = await evaluateOutput(output, testCase, skill.evalCriteria, apiKey, skill.improvementModel);
      allEvals.push(result);
      if (result?.scores) {
        const avg = result.scores.reduce((sum, item) => sum + item.score, 0) / result.scores.length;
        console.log(` ${avg.toFixed(1)}/10`);
      } else {
        console.log(' no scores');
      }
    } catch (err) {
      console.log(` failed: ${err.message}`);
    }
    await new Promise((resolve) => setTimeout(resolve, 1500));
  }

  const weaknesses = diagnoseWeaknesses(allEvals, skill.evalCriteria);
  const totalWeighted = weaknesses.reduce((sum, weakness) => sum + weakness.weightedScore, 0);
  const totalWeight = weaknesses.reduce((sum, weakness) => sum + weakness.weight, 0) || 1;
  console.log(`\nBaseline score: ${(totalWeighted / totalWeight).toFixed(2)}/10`);
  weaknesses.forEach((weakness) => {
    console.log(`  ${weakness.name}: ${weakness.avgScore}/10 (${weakness.weight}x)`);
  });
}

function showReport() {
  if (!fileExists(HISTORY_PATH)) {
    console.log('No optimization history found.');
    return;
  }

  const history = JSON.parse(fs.readFileSync(HISTORY_PATH, 'utf8'));
  console.log(`\nSkill Optimization History (${history.length} iterations)\n`);

  const bySkill = {};
  history.forEach((entry) => {
    if (!bySkill[entry.skill]) bySkill[entry.skill] = [];
    bySkill[entry.skill].push(entry);
  });

  Object.entries(bySkill).forEach(([skill, runs]) => {
    console.log(`${skill}:`);
    runs.forEach((run) => {
      console.log(`  Iter ${run.iteration + 1}: ${run.overallScore}/10 - ${run.timestamp.split('T')[0]}`);
    });
  });
}

async function main() {
  const flags = parseFlags(process.argv.slice(2));
  if (flags.report) {
    showReport();
    return;
  }

  const configPath = getConfigPath(flags);
  const config = loadOptimizerConfig(configPath);
  const apiKey = getApiKey(config.raw.skillOptimizer || {});

  if (!apiKey) {
    console.error('Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY, or provide it via workspace secrets.');
    process.exit(1);
  }

  const skillName = flags.skill || Object.keys(config.skills)[0];
  const skill = config.skills[skillName];
  if (!skill) {
    console.error(`Unknown skill: ${skillName}. Available: ${Object.keys(config.skills).join(', ')}`);
    process.exit(1);
  }

  if (flags['eval-only']) {
    await evalOnly(skillName, skill, apiKey);
    return;
  }

  const iterations = parseInt(flags.iterations, 10) || 3;
  const dryRun = Boolean(flags['dry-run']);
  await optimize(skillName, skill, iterations, dryRun, apiKey);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
