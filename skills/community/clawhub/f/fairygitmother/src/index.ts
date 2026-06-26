/**
 * FairygitMother OpenClaw Skill — companion runner.
 *
 * The SKILL.md is the primary skill definition — it tells the OpenClaw agent
 * how to interact with the FairygitMother grid using curl/bash tools.
 *
 * This module provides a programmatic alternative for environments where
 * the agent runtime supports Node.js skill scripts. It handles registration,
 * heartbeat, and bounty lifecycle automatically.
 */

export { FairygitMotherClient } from "@fairygitmother/node";
export {
	fetchRepoTree,
	fetchFile,
	fetchFiles,
	generateUnifiedDiff,
	buildApiSolvePrompt,
	buildApiReviewPrompt,
	selectSolverMode,
	type RepoFile,
	type RepoTree,
	type FileChange,
} from "@fairygitmother/node";
