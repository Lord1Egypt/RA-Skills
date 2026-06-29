/**
 * Drip Campaign Module
 * Automated follow-up sequences
 */

import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dbDir = path.join(__dirname, '../../data');
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}
const db = new Database(path.join(dbDir, 'drip.db'));

export interface DripSequence {
  id?: number;
  name: string;
  steps: DripStep[];
  trigger: 'new_follower' | 'mention' | 'keyword' | 'manual';
  createdAt?: string;
}

export interface DripStep {
  day: number; // Day offset from trigger
  action: 'post' | 'dm' | 'like' | 'follow' | 'reply';
  content?: string;
  media?: string[];
}

export interface DripEnrollment {
  id?: number;
  sequenceId: number;
  userDid: string;
  enrolledAt: string;
  currentStep: number;
  completed: boolean;
}

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS drip_sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    steps TEXT NOT NULL,
    trigger TEXT NOT NULL,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS drip_enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequenceId INTEGER NOT NULL,
    userDid TEXT NOT NULL,
    enrolledAt TEXT DEFAULT CURRENT_TIMESTAMP,
    currentStep INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY (sequenceId) REFERENCES drip_sequences(id)
  )
`);

/**
 * Create a drip campaign sequence
 */
export function createDripSequence(
  name: string,
  trigger: 'new_follower' | 'mention' | 'keyword' | 'manual',
  steps: DripStep[]
): DripSequence {
  const stmt = db.prepare(`
    INSERT INTO drip_sequences (name, steps, trigger)
    VALUES (?, ?, ?)
  `);
  
  const result = stmt.run(name, JSON.stringify(steps), trigger);
  
  return {
    id: result.lastInsertRowid as number,
    name,
    trigger,
    steps
  };
}

/**
 * Get all drip sequences
 */
export function getDripSequences(): DripSequence[] {
  const stmt = db.prepare('SELECT * FROM drip_sequences ORDER BY createdAt DESC');
  const rows = stmt.all() as any[];
  
  return rows.map(row => ({
    ...row,
    steps: JSON.parse(row.steps)
  }));
}

/**
 * Enroll a user in a drip sequence
 */
export function enrollUser(sequenceId: number, userDid: string): DripEnrollment {
  const stmt = db.prepare(`
    INSERT INTO drip_enrollments (sequenceId, userDid, currentStep)
    VALUES (?, ?, 0)
  `);
  
  const result = stmt.run(sequenceId, userDid);
  
  return {
    id: result.lastInsertRowid as number,
    sequenceId,
    userDid,
    enrolledAt: new Date().toISOString(),
    currentStep: 0,
    completed: false
  };
}

/**
 * Get pending drip actions
 */
export function getPendingDripActions(): (DripEnrollment & { sequence: DripSequence })[] {
  const stmt = db.prepare(`
    SELECT e.*, s.steps, s.name, s.trigger
    FROM drip_enrollments e
    JOIN drip_sequences s ON e.sequenceId = s.id
    WHERE e.completed = 0
    ORDER BY e.enrolledAt ASC
  `);
  
  const rows = stmt.all() as any[];
  
  return rows.map(row => ({
    ...row,
    steps: JSON.parse(row.steps),
    sequence: {
      id: row.sequenceId,
      name: row.name,
      trigger: row.trigger
    }
  }));
}

/**
 * Update enrollment step
 */
export function updateEnrollmentStep(enrollmentId: number, step: number): void {
  const stmt = db.prepare(`
    UPDATE drip_enrollments SET currentStep = ? WHERE id = ?
  `);
  stmt.run(step, enrollmentId);
}

/**
 * Complete enrollment
 */
export function completeEnrollment(enrollmentId: number): void {
  const stmt = db.prepare(`
    UPDATE drip_enrollments SET completed = 1 WHERE id = ?
  `);
  stmt.run(enrollmentId);
}

/**
 * Get user's active enrollments
 */
export function getUserEnrollments(userDid: string): DripEnrollment[] {
  const stmt = db.prepare(`
    SELECT * FROM drip_enrollments 
    WHERE userDid = ? AND completed = 0
  `);
  
  return stmt.all(userDid) as DripEnrollment[];
}

// Helper to create common sequences
export function createWelcomeSequence(): DripSequence {
  return createDripSequence(
    'New Follower Welcome',
    'new_follower',
    [
      { day: 0, action: 'dm', content: 'Thanks for following! 🦞' },
      { day: 1, action: 'like', content: '' },
      { day: 2, action: 'post', content: 'Tip: Check out my pinned post for resources!' },
      { day: 3, action: 'reply', content: 'Feel free to ask any questions!' }
    ]
  );
}