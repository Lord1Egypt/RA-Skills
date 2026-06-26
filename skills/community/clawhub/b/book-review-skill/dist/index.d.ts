/**
 * Book Review Skill
 * Expand reading insights into in-depth reviews
 * 
 * SAFE VERSION: No external API calls, no filesystem access, pure local processing
 */

import { Skill } from 'openclaw';

export interface BookReviewOptions {
  insight: string;
  depth?: 'brief' | 'detailed' | 'comprehensive';
  includeReferences?: boolean;
}

/**
 * Safe template-based book review expansion
 * 
 * This implementation uses only local templates and does NOT:
 * - Call external APIs
 * - Access filesystem
 * - Require API keys or secrets
 * - Send user data outside the local environment
 */
export declare function expandBookReview(options: BookReviewOptions): Promise<string>;

/**
 * Local reference suggestion (no external search)
 */
export declare function suggestRelatedConcepts(insight: string, limit?: number): Promise<string[]>;

/**
 * Main skill handler for OpenClaw - SAFE VERSION
 */
export declare const bookReviewSkill: Skill;

export default bookReviewSkill;