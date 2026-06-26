// Runtime entrypoint for the AgentDerby OpenClaw skill.
// IMPORTANT: ClawHub/OpenClaw registry installs copy files but do NOT install Node dependencies.
// Therefore we ship a bundled build (including runtime deps like ws/pngjs) under dist/.
// The dist build is CommonJS for maximum compatibility with bundled dependencies.

import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const mod = require('./dist/index.cjs');

export const createAgentDerbySkill = mod.createAgentDerbySkill;
