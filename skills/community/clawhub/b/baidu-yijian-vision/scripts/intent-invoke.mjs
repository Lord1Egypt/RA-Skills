#!/usr/bin/env node

import { querySkills } from './query.mjs';
import { callMultimodal } from './multimodal.mjs';
import { runSkill } from './invoke.mjs';
import { getWorkspaceSkills } from './workspace.mjs';
import { fileURLToPath } from 'url';

const DEFAULT_CONFIDENCE_THRESHOLD = 0.7;
const MAX_SKILL_RETRIES = 3;

/**
 * Determine if we should use the skill based on confidence threshold.
 */
export function shouldUseSkill(skill, threshold = DEFAULT_CONFIDENCE_THRESHOLD) {
  return !!(skill && skill.epId && typeof skill.confidence === 'number' && skill.confidence >= threshold);
}

/**
 * Format the final result consistently.
 */
export function formatResult(mode, skill, detections = [], detail = null) {
  return {
    success: true,
    mode,
    epId: skill?.epId ?? null,
    skillName: skill?.name || skill?.displayName || null,
    confidence: skill?.confidence ?? null,
    count: detections.length,
    detections,
    detail,
  };
}

/**
 * Extract detections array from a runSkill() result.
 */
export function extractDetections(result) {
  if (result?.noDetection) return [];
  const outputs = result?.result?.outputs;
  if (!outputs || outputs.length === 0) return [];
  // Collect detections from all outputs (not just the first)
  const allDetections = [];
  for (const output of outputs) {
    if (output?.parsedValue && Array.isArray(output.parsedValue)) {
      allDetections.push(...output.parsedValue);
    }
  }
  return allDetections;
}

/**
 * Extract a structured result from a multimodal API response.
 * The multimodal API returns an OpenAI-style chat completion object,
 * not a detections array. This function normalizes it into a consistent format.
 *
 * @param {object} rawResponse - Raw response from callMultimodal()
 * @returns {Array} Array of result objects with `answer` field
 */
export function extractMultimodalResult(rawResponse) {
  if (!rawResponse) return [];

  // OpenAI-style: { choices: [{ message: { content: "..." } }] }
  const content = rawResponse?.choices?.[0]?.message?.content;
  if (content && typeof content === 'string') {
    return [{ answer: content }];
  }

  return [];
}

/**
 * Main orchestration function:
 * 1. Query router for skills matching intent
 * 2. Try top skills one by one (up to MAX_SKILL_RETRIES)
 * 3. If all skills fail, fallback to multimodal
 */
export async function intentInvoke(intent, imagePath, options = {}) {
  const { threshold = DEFAULT_CONFIDENCE_THRESHOLD, topK = 5, forceRefresh = false } = options;

  // Step 1: Query for matching skills
  let skills;
  try {
    skills = await querySkills(intent, { topK });
  } catch (err) {
    // Query failed, will fallback to multimodal
    skills = [];
  }

  // Step 2: Try top skills one by one (skills require an image)
  const candidates = imagePath
    ? skills.filter(s => shouldUseSkill(s, threshold)).slice(0, MAX_SKILL_RETRIES)
    : [];
  for (const skill of candidates) {
    try {
      const { result } = await runSkill(skill.epId, { input0: { image: imagePath } }, { autoROI: true });
      const detections = extractDetections(result);
      const detail = result?.noDetection ? (result.detail || 'conditional branch did not hit') : null;
      return formatResult('skill', skill, detections, detail);
    } catch (err) {
      console.error(`Skill ${skill.epId} (${skill.name}) failed: ${err.message}`);
      // Continue to next skill
    }
  }

  // Step 3: Public skills all failed — search private workspace
  try {
    const privateSkills = await getWorkspaceSkills({ forceRefresh });
    if (privateSkills.length > 0) {
      const result = formatResult('workspace-search', null, []);
      result.privateSkills = privateSkills.map(s => ({
        epId: s.epId,
        displayName: s.displayName,
        description: s.description,
      }));
      result.hint = '公共技能无匹配。请从 privateSkills 列表中选择最匹配的技能，使用 invoke.mjs 调用。如无合适技能，可调用 multimodal.mjs 回退。';
      return result;
    }
  } catch (err) {
    console.error(`Private workspace search failed: ${err.message}`);
    // Continue to multimodal fallback
  }

  // Step 4: Fallback to multimodal
  try {
    const rawResult = await callMultimodal(intent, imagePath);
    const detections = extractMultimodalResult(rawResult);
    return formatResult('multimodal', null, detections);
  } catch (err) {
    return {
      success: false,
      error: err.message,
      mode: 'multimodal',
      epId: null,
      detections: []
    };
  }
}

/**
 * CLI entry point.
 */
async function main() {
  const args = process.argv.slice(2);
  const forceRefresh = args.includes('--refresh');
  const positional = args.filter(a => !a.startsWith('--'));

  const intent = positional[0];
  const imagePath = positional[1];
  const threshold = parseFloat(positional[2]) || DEFAULT_CONFIDENCE_THRESHOLD;

  if (!intent) {
    console.error('Usage: node intent-invoke.mjs <intent> [image-path] [threshold] [--refresh]');
    console.error('Example: node intent-invoke.mjs "detect people falling" photo.jpg 0.8');
    console.error('');
    console.error('Parameters:');
    console.error('  intent      - Description of what to detect (required)');
    console.error('  image-path  - Path to image file (optional)');
    console.error('  threshold   - Confidence threshold 0.0-1.0 (default: 0.7)');
    console.error('  --refresh   - Force refresh workspace skill cache');
    process.exit(1);
  }

  try {
    const result = await intentInvoke(intent, imagePath, { threshold, forceRefresh });
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  } catch (err) {
    console.error(JSON.stringify({
      success: false,
      error: err.message
    }, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
