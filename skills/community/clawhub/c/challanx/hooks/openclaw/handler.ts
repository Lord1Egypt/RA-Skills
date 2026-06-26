/**
 * ChallanX Hook for OpenClaw
 *
 * Adds a short bootstrap reminder and a fuller instructions file during
 * bootstrap so agents keep ChallanX docs and examples consistent.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_NAME = 'CHALLANX_REMINDER.md';
const INSTRUCTIONS_NAME = 'CHALLANX_INSTRUCTIONS.md';
const REMINDER_PATH = REMINDER_NAME;
const INSTRUCTIONS_PATH = INSTRUCTIONS_NAME;

const REMINDER_CONTENT = `## ChallanX Reminder

Use the public endpoint only:
- https://challanx.in/openclaw/api

When documenting or generating examples:
- prefer real media filenames like mp4, mp3, jpg, png
- avoid saying responses are generic .bin unless nothing better is known
- use custom statuses: success, download_ready, picker_required, failed
- keep curl examples copy-paste friendly
`;

const INSTRUCTIONS_CONTENT = `# ChallanX OpenClaw Instructions

Public endpoint:
- https://challanx.in/openclaw/api

Quick rules for authors and agents:
- Prefer returning real media files with proper content-type and filenames.
- When upstream returns multiple choices, respond with a "picker_required" JSON containing readable filenames.
- Map upstream status names to ChallanX-friendly statuses: success, download_ready, picker_required, failed.
- Avoid leaking internal/local hostnames in public docs or examples.
- For downloadable content, use Content-Disposition with a usable filename (e.g. output.mp4).
- Example curl:
  - Download info: curl "https://challanx.in/openclaw/api?url=https://example.com/video.mp4"
  - Post JSON: curl -X POST -H "Content-Type: application/json" -d '{"url":"https://example.com/video.mp4"}' https://challanx.in/openclaw/api

If you see a pre-existing non-virtual file with the same path, this hook will not overwrite it.
`;

function isObject(value: unknown): value is Record<string, unknown> {
  return !!value && typeof value === 'object';
}

function isInjectedFile(value: unknown, path: string, content: string): boolean {
  if (!isObject(value) || value.path !== path) return false;
  return value.virtual === true || value.content === content;
}

const handler: HookHandler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) return;

  if (Array.isArray(event.context.bootstrapFiles)) {
    const occupiedByOtherFile = event.context.bootstrapFiles.some((file) => {
      if (!isObject(file) || !file.path) return false;
      const path = String((file as any).path);
      if ((path === REMINDER_PATH || path === INSTRUCTIONS_PATH) &&
        !isInjectedFile(file, REMINDER_PATH, REMINDER_CONTENT) &&
        !isInjectedFile(file, INSTRUCTIONS_PATH, INSTRUCTIONS_CONTENT)) {
        return true;
      }
      return false;
    });
    if (occupiedByOtherFile) return;

    const cleanedBootstrapFiles = event.context.bootstrapFiles.filter(
      (file, index, files) =>
        !isInjectedFile(file, REMINDER_PATH, REMINDER_CONTENT) ||
        files.findIndex((candidate) => isInjectedFile(candidate, REMINDER_PATH, REMINDER_CONTENT)) === index,
    ).filter(
      (file, index, files) =>
        !isInjectedFile(file, INSTRUCTIONS_PATH, INSTRUCTIONS_CONTENT) ||
        files.findIndex((candidate) => isInjectedFile(candidate, INSTRUCTIONS_PATH, INSTRUCTIONS_CONTENT)) === index,
    );

    const reminderFile = {
      name: REMINDER_NAME,
      path: REMINDER_PATH,
      content: REMINDER_CONTENT,
      missing: false,
      virtual: true,
    };

    const instructionsFile = {
      name: INSTRUCTIONS_NAME,
      path: INSTRUCTIONS_PATH,
      content: INSTRUCTIONS_CONTENT,
      missing: false,
      virtual: true,
    };

    const existingReminderIndex = cleanedBootstrapFiles.findIndex((file) =>
      isInjectedFile(file, REMINDER_PATH, REMINDER_CONTENT),
    );
    if (existingReminderIndex === -1) cleanedBootstrapFiles.push(reminderFile);
    else cleanedBootstrapFiles[existingReminderIndex] = reminderFile;

    const existingInstructionsIndex = cleanedBootstrapFiles.findIndex((file) =>
      isInjectedFile(file, INSTRUCTIONS_PATH, INSTRUCTIONS_CONTENT),
    );
    if (existingInstructionsIndex === -1) cleanedBootstrapFiles.push(instructionsFile);
    else cleanedBootstrapFiles[existingInstructionsIndex] = instructionsFile;

    event.context.bootstrapFiles = cleanedBootstrapFiles;
  }
};

export default handler;
