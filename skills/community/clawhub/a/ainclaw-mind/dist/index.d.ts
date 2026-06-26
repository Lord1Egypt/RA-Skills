/**
 * ClawMind Skill Entry Point
 *
 * Exports the two hooks registered in skill.json:
 * - interceptIntent: fires on every user intent, queries cloud for cached macros
 * - onSessionComplete: fires after successful sessions, contributes new workflows
 */
export { interceptIntent, onSessionComplete } from "./interceptor.js";
