#!/usr/bin/env node

import { httpsRequest, getApiKey, runUrl, readStdin, truncateBody } from './utils.mjs';
import { buildValue, parseOutputs, readImageFile } from './types.mjs';
import { fileURLToPath } from 'url';

/**
 * Build a full-image ROI covering the entire image bounds.
 */
export function fullImageROI(width, height) {
  return { id: '1', name: 'zone', kind: 'ROI', points: [0, 0, width, 0, width, height, 0, height] };
}

/**
 * Determine Yijian type from a field name heuristic.
 */
function detectFieldType(fieldName, fieldValue) {
  const lower = fieldName.toLowerCase();
  if (lower.includes('image') || lower.endsWith('image')) return 'Image';
  if (lower.includes('roi')) return 'ROI';
  if (lower.includes('tripwire')) return 'Tripwire';
  if (typeof fieldValue === 'number') return 'Integer';
  return 'String';
}

/**
 * Build the `inputs` array for the run request body.
 * Supports Image, ROI, Tripwire, Integer, and String types.
 * When autoROI is enabled and an Image field is present without a corresponding ROI,
 * automatically adds a full-image ROI.
 */
function buildRunInputs(userInputs, options = {}) {
  const { autoROI = false } = options;
  const inputs = [];

  for (const [inputName, inputData] of Object.entries(userInputs)) {
    const schema = [];
    let hasImage = false;
    let hasROI = false;
    let imagePath = null;

    for (const [fieldName, fieldValue] of Object.entries(inputData)) {
      const type = detectFieldType(fieldName, fieldValue);

      if (type === 'Image') {
        hasImage = true;
        imagePath = typeof fieldValue === 'object' && fieldValue !== null
          ? (fieldValue.file || fieldValue.image || null)
          : (typeof fieldValue === 'string' && !fieldValue.startsWith('data:') ? fieldValue : null);
      }
      if (type === 'ROI') hasROI = true;

      schema.push({
        name: fieldName,
        type: type,
        value: buildValue(type, fieldValue),
      });
    }

    // Auto-fill full-image ROI when enabled and not provided by user
    if (autoROI && hasImage && !hasROI && imagePath) {
      try {
        const img = readImageFile(imagePath);
        schema.push({
          name: 'roi',
          type: 'ROI',
          value: buildValue('ROI', fullImageROI(img.width, img.height)),
        });
      } catch (err) {
        // If we can't read the image for ROI, skip auto-fill
        // (buildValue('Image', ...) will read it again anyway and throw if invalid)
      }
    }

    inputs.push({ name: inputName, schema });
  }

  return inputs;
}

/**
 * Invoke a skill by epId with the given user inputs.
 *
 * @param {string} epId - Skill endpoint ID (e.g. "ep-public-xxx")
 * @param {object} userInputs - User input { input0: { image: "path", roi: {...} } }
 * @param {object} options
 * @param {boolean} options.autoROI - Auto-fill full-image ROI when not provided (default: true)
 * @returns {Promise<{success: boolean, epId: string, result?: object, message?: string}>}
 */
export async function runSkill(epId, userInputs = {}, options = {}) {
  const { autoROI = true } = options;
  const apiKey = getApiKey();

  const inputs = buildRunInputs(userInputs, { autoROI });
  const requestBody = JSON.stringify({ inputs });

  const response = await httpsRequest(runUrl(epId), {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: requestBody,
  });

  let result;
  try {
    result = JSON.parse(response.body);
  } catch {
    result = { rawResponse: response.body };
  }

  // Handle "no detection" responses:
  // The API returns HTTP 200 with { success: false, message: { code: "BadRequest", global: { detail: "...conditional branch did not hit..." } } }
  // This means the image didn't produce results matching the skill's conditions —
  // NOT an actual error. Treat as a successful invocation with no detections.
  if (result.success === false && result.message?.code === 'BadRequest') {
    const detail = result.message?.global?.detail || '';
    if (detail.includes('conditional branch did not hit')) {
      return {
        success: true,
        epId,
        result: { noDetection: true, detail, rawMessage: result.message },
      };
    }
  }

  if (response.statusCode !== 200) {
    throw new Error(`Skill invocation failed (${response.statusCode}): ${truncateBody(response.body)}`);
  }

  // Post-process: parse complex-type outputs
  if (result.result?.outputs) {
    parseOutputs(result.result.outputs);
  }

  return { success: true, epId, result };
}

/**
 * CLI entry point.
 */
async function main() {
  const epId = process.argv[2];
  let inputArg = process.argv[3];

  if (!epId) {
    console.error('Usage: node invoke.mjs <ep-id> \'<input-json>\' | -');
    console.error('Use - as input arg to read from stdin');
    console.error('');
    console.error('Input JSON format:');
    console.error('  { "input0": { "image": "/path/to/image.jpg" } }');
    console.error('  { "input0": { "image": "/path/to/image.jpg", "roi": { "id":"1","name":"zone","kind":"ROI","points":[...] } } }');
    process.exit(1);
  }

  // Parse user input JSON
  let userInputs;
  if (inputArg === '-') {
    inputArg = await readStdin();
  }
  if (!inputArg) {
    userInputs = {};
  } else {
    try {
      userInputs = JSON.parse(inputArg);
    } catch (err) {
      console.error(`Failed to parse input JSON: ${err.message}`);
      process.exit(1);
    }
  }

  try {
    const output = await runSkill(epId, userInputs, { autoROI: true });
    console.log(JSON.stringify(output, null, 2));
    process.exit(output.success ? 0 : 1);
  } catch (err) {
    console.error(JSON.stringify({ success: false, epId, error: err.message }, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
