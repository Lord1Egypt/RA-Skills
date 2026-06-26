/**
 * Session discovery utilities for OpenClaw transcripts
 */
interface SessionInfo {
    sessionId: string;
    sessionKey: string;
    agentId: string;
    filePath: string;
    updatedAt?: number;
}
interface SessionsStore {
    [sessionKey: string]: {
        sessionId: string;
        updatedAt?: number;
        [key: string]: unknown;
    };
}
/**
 * Get the OpenClaw agents directory
 */
declare function getOpenClawAgentsDir(): string;
/**
 * Get the sessions directory for an agent
 */
declare function getSessionsDir(agentId: string): string;
/**
 * Get the path to sessions.json for an agent
 */
declare function getSessionsJsonPath(agentId: string): string;
/**
 * Get the path to a session JSONL file
 */
declare function getSessionFilePath(agentId: string, sessionId: string): string;
/**
 * List all available agents
 */
declare function listAgents(): string[];
/**
 * Load sessions.json for an agent
 */
declare function loadSessionsStore(agentId: string): SessionsStore | null;
/**
 * Find the current/main session for an agent
 */
declare function findMainSession(agentId: string): SessionInfo | null;
/**
 * Find a session by ID
 */
declare function findSessionById(agentId: string, sessionId: string): SessionInfo | null;
/**
 * List all sessions for an agent
 */
declare function listSessions(agentId: string): SessionInfo[];
/**
 * Create a backup of a session file
 */
declare function backupSession(filePath: string): string;

export { type SessionInfo, type SessionsStore, backupSession, findMainSession, findSessionById, getOpenClawAgentsDir, getSessionFilePath, getSessionsDir, getSessionsJsonPath, listAgents, listSessions, loadSessionsStore };
