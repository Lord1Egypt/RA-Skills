// ============================================================================
// EO Session Manager - Collaboration Session Lifecycle
// ============================================================================

import type { CollaborationSession, ExpertResult, ExpertTeam } from '../types/index.js';
import { teamManager } from './team-manager.js';

// Use crypto.randomUUID if available, fallback
function generateId(): string {
  try {
    return crypto.randomUUID();
  } catch {
    return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
  }
}

// ---------------------------------------------------------------------------
// Session State
// ---------------------------------------------------------------------------

const activeSessions = new Map<string, CollaborationSession>();
const sessionHistory: CollaborationSession[] = [];

// ---------------------------------------------------------------------------
// Session Manager
// ---------------------------------------------------------------------------

export class SessionManager {
  private sessions = activeSessions;
  private history = sessionHistory;
  private maxHistory = 100;

  /**
   * Create a new collaboration session
   */
  createSession(task: string, context?: Record<string, unknown>): CollaborationSession {
    const session: CollaborationSession = {
      id: generateId(),
      task,
      context: context ?? {},
      teams: [],
      results: [],
      status: 'running',
      createdAt: Date.now(),
    };
    this.sessions.set(session.id, session);
    return session;
  }

  /**
   * Get a session by ID
   */
  getSession(sessionId: string): CollaborationSession | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * Add a team to a session
   */
  addTeamToSession(sessionId: string, team: ExpertTeam): boolean {
    const session = this.sessions.get(sessionId);
    if (!session) return false;
    teamManager.setTeamStatus(team.id, 'active');
    session.teams.push(team);
    return true;
  }

  /**
   * Add a result from an expert to a session
   */
  addExpertResult(sessionId: string, result: ExpertResult): boolean {
    const session = this.sessions.get(sessionId);
    if (!session) return false;
    session.results.push(result);
    return true;
  }

  /**
   * Complete a session
   */
  completeSession(sessionId: string, status: 'completed' | 'failed' = 'completed'): boolean {
    const session = this.sessions.get(sessionId);
    if (!session) return false;
    session.status = status;
    session.completedAt = Date.now();

    // Mark all teams as completed
    for (const team of session.teams) {
      teamManager.setTeamStatus(team.id, status === 'completed' ? 'completed' : 'failed');
    }

    // Move to history
    this.history.push(session);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }

    this.sessions.delete(sessionId);
    return true;
  }

  /**
   * List all active sessions
   */
  listActiveSessions(): CollaborationSession[] {
    return Array.from(this.sessions.values());
  }

  /**
   * List recent completed sessions
   */
  listRecentSessions(limit = 10): CollaborationSession[] {
    return this.history.slice(-limit).reverse();
  }

  /**
   * Get session summary
   */
  getSessionSummary(sessionId: string): string {
    const session = this.sessions.get(sessionId) ?? this.history.find(s => s.id === sessionId);
    if (!session) return `Session ${sessionId} not found`;

    const lines = [
      `## Session: ${session.id}`,
      `**Task:** ${session.task}`,
      `**Status:** ${session.status}`,
      `**Created:** ${new Date(session.createdAt).toISOString()}`,
      `**Teams:** ${session.teams.length}`,
      `**Results:** ${session.results.length}`,
    ];

    if (session.completedAt) {
      const duration = session.completedAt - session.createdAt;
      lines.push(`**Duration:** ${(duration / 1000).toFixed(1)}s`);
    }

    if (session.results.length > 0) {
      lines.push('\n### Expert Results:');
      for (const r of session.results) {
        lines.push(`- **${r.expertName}**: ${r.success ? '✓' : '✗'} ${r.output.slice(0, 100)}`);
      }
    }

    return lines.join('\n');
  }

  /**
   * Clean up stale sessions
   */
  cleanupStaleSessions(maxAgeMs = 3600000): number {
    const now = Date.now();
    let cleaned = 0;
    for (const [id, session] of this.sessions) {
      if (now - session.createdAt > maxAgeMs) {
        this.completeSession(id, 'failed');
        cleaned++;
      }
    }
    return cleaned;
  }
}

// Global singleton
export const sessionManager = new SessionManager();
