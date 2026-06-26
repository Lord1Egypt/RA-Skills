/**
 * Core Data Models for Decision Journal
 * 
 * This module defines the data structures for:
 * - Decision: A decision entry with context, options, and outcomes
 * - Review: A review record for tracking decision outcomes
 * - Pattern: Extracted patterns from decision history
 */

const crypto = require('crypto');

/**
 * Generate a unique ID for entities
 * @returns {string} 8-character alphanumeric ID
 */
function generateId() {
  return crypto.randomBytes(4).toString('hex');
}

/**
 * Get current timestamp in ISO format
 * @returns {string} ISO timestamp
 */
function now() {
  return new Date().toISOString();
}

/**
 * Decision Model
 * Represents a single decision entry
 */
class Decision {
  /**
   * Create a new Decision
   * @param {Object} data - Decision data
   * @param {string} data.title - Decision title/summary
   * @param {string} [data.situation] - Context/situation
   * @param {string[]} [data.options=[]] - Options considered
   * @param {string} [data.decision] - The decision made
   * @param {string} [data.reasoning] - Reasoning behind the decision
   * @param {string} [data.expected] - Expected outcomes
   * @param {string} [data.tag] - Category tag
   * @param {number} [data.importance=3] - Importance level (1-5)
   * @param {boolean} [data.reversible=true] - Whether decision is reversible
   * @param {string} [data.reviewDate] - Scheduled review date (YYYY-MM-DD)
   * @param {string} [data.id] - Unique ID (auto-generated if not provided)
   * @param {string} [data.createdAt] - Creation timestamp
   * @param {string} [data.status='pending'] - Decision status
   */
  constructor(data = {}) {
    this.id = data.id || generateId();
    this.title = data.title || 'Untitled Decision';
    this.situation = data.situation || '';
    this.options = data.options || [];
    this.decision = data.decision || '';
    this.reasoning = data.reasoning || '';
    this.expected = data.expected || '';
    this.tag = data.tag || 'uncategorized';
    this.importance = data.importance || 3;
    this.reversible = data.reversible !== undefined ? data.reversible : true;
    this.reviewDate = data.reviewDate || null;
    this.createdAt = data.createdAt || now();
    this.updatedAt = data.updatedAt || null;
    this.status = data.status || 'pending';
    this.outcome = data.outcome || null;
    this.lessons = data.lessons || '';
    this.satisfaction = data.satisfaction || null;
    this.reviewedAt = data.reviewedAt || null;
    this.metadata = data.metadata || {};
  }

  /**
   * Convert to plain object for serialization
   * @returns {Object} Plain object representation
   */
  toJSON() {
    return {
      id: this.id,
      title: this.title,
      situation: this.situation,
      options: this.options,
      decision: this.decision,
      reasoning: this.reasoning,
      expected: this.expected,
      tag: this.tag,
      importance: this.importance,
      reversible: this.reversible,
      reviewDate: this.reviewDate,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      status: this.status,
      outcome: this.outcome,
      lessons: this.lessons,
      satisfaction: this.satisfaction,
      reviewedAt: this.reviewedAt,
      metadata: this.metadata
    };
  }

  /**
   * Create Decision from JSON object
   * @param {Object} json - JSON object
   * @returns {Decision} Decision instance
   */
  static fromJSON(json) {
    return new Decision(json);
  }

  /**
   * Update decision with review data
   * @param {Object} reviewData - Review data
   * @param {string} reviewData.outcome - Actual outcome
   * @param {string} [reviewData.lessons] - Lessons learned
   * @param {number} [reviewData.satisfaction] - Satisfaction level (1-5)
   */
  addReview(reviewData) {
    this.outcome = reviewData.outcome || this.outcome;
    this.lessons = reviewData.lessons || this.lessons;
    this.satisfaction = reviewData.satisfaction || this.satisfaction;
    this.reviewedAt = now();
    this.status = 'reviewed';
    this.updatedAt = now();
  }

  /**
   * Check if decision is due for review
   * @returns {boolean} True if review date has passed
   */
  isDueForReview() {
    if (!this.reviewDate || this.status === 'reviewed') {
      return false;
    }
    const today = new Date().toISOString().split('T')[0];
    return this.reviewDate <= today;
  }

  /**
   * Get decision summary for display
   * @returns {string} Formatted summary
   */
  getSummary() {
    const stars = '⭐'.repeat(this.importance);
    const statusEmoji = {
      'pending': '⏳',
      'reviewed': '✅',
      'completed': '✅',
      'archived': '📦'
    }[this.status] || '⏳';

    return `${statusEmoji} ${this.title} (${this.id})\n` +
           `   Date: ${this.createdAt.split('T')[0]} | Tag: ${this.tag} | Importance: ${stars}`;
  }

  /**
   * Get full formatted representation
   * @returns {string} Detailed formatted output
   */
  format() {
    const lines = [
      `📋 Decision: ${this.title}`,
      `   ID: ${this.id}`,
      `   Date: ${this.createdAt.split('T')[0]}`,
      `   Status: ${this.status}`,
    ];

    if (this.tag) lines.push(`   Tag: ${this.tag}`);
    if (this.importance) lines.push(`   Importance: ${'⭐'.repeat(this.importance)}`);
    if (this.situation) lines.push(`   Situation: ${this.situation}`);
    if (this.options && this.options.length > 0) {
      lines.push(`   Options: ${this.options.length} considered`);
    }
    if (this.decision) lines.push(`   Decision: ${this.decision}`);
    if (this.reviewDate) lines.push(`   Review: ${this.reviewDate}`);
    if (this.outcome) lines.push(`   Outcome: ${this.outcome}`);
    if (this.satisfaction) lines.push(`   Satisfaction: ${'⭐'.repeat(this.satisfaction)}`);

    return lines.join('\n');
  }
}

/**
 * Review Model
 * Represents a review record for a decision
 */
class Review {
  /**
   * Create a new Review
   * @param {Object} data - Review data
   * @param {string} data.decisionId - ID of the decision being reviewed
   * @param {string} data.outcome - Actual outcome
   * @param {string} [data.lessons] - Lessons learned
   * @param {number} [data.satisfaction] - Satisfaction level (1-5)
   * @param {number} [data.processQuality] - Process quality score (1-5)
   * @param {number} [data.outcomeAccuracy] - Outcome accuracy (0-1)
   * @param {string} [data.id] - Unique ID
   * @param {string} [data.createdAt] - Creation timestamp
   */
  constructor(data = {}) {
    this.id = data.id || generateId();
    this.decisionId = data.decisionId;
    this.outcome = data.outcome || '';
    this.lessons = data.lessons || '';
    this.satisfaction = data.satisfaction || null;
    this.processQuality = data.processQuality || null;
    this.outcomeAccuracy = data.outcomeAccuracy || null;
    this.surprises = data.surprises || '';
    this.wouldRepeat = data.wouldRepeat || null;
    this.createdAt = data.createdAt || now();
    this.metadata = data.metadata || {};
  }

  /**
   * Convert to plain object for serialization
   * @returns {Object} Plain object representation
   */
  toJSON() {
    return {
      id: this.id,
      decisionId: this.decisionId,
      outcome: this.outcome,
      lessons: this.lessons,
      satisfaction: this.satisfaction,
      processQuality: this.processQuality,
      outcomeAccuracy: this.outcomeAccuracy,
      surprises: this.surprises,
      wouldRepeat: this.wouldRepeat,
      createdAt: this.createdAt,
      metadata: this.metadata
    };
  }

  /**
   * Create Review from JSON object
   * @param {Object} json - JSON object
   * @returns {Review} Review instance
   */
  static fromJSON(json) {
    return new Review(json);
  }
}

/**
 * Pattern Model
 * Represents an extracted pattern from decision history
 */
class Pattern {
  /**
   * Create a new Pattern
   * @param {Object} data - Pattern data
   * @param {string} data.name - Pattern name
   * @param {string} data.description - Pattern description
   * @param {string} data.type - Pattern type (bias, strength, weakness, habit)
   * @param {string[]} data.decisionIds - Related decision IDs
   * @param {number} [data.frequency=1] - How often this pattern appears
   * @param {number} [data.confidence=0.5] - Confidence level (0-1)
   * @param {string} [data.id] - Unique ID
   * @param {string} [data.createdAt] - Creation timestamp
   * @param {string} [data.lastObserved] - Last observed timestamp
   */
  constructor(data = {}) {
    this.id = data.id || generateId();
    this.name = data.name || 'Unnamed Pattern';
    this.description = data.description || '';
    this.type = data.type || 'observation'; // bias, strength, weakness, habit, observation
    this.decisionIds = data.decisionIds || [];
    this.frequency = data.frequency || 1;
    this.confidence = data.confidence || 0.5;
    this.createdAt = data.createdAt || now();
    this.lastObserved = data.lastObserved || now();
    this.metadata = data.metadata || {};
  }

  /**
   * Convert to plain object for serialization
   * @returns {Object} Plain object representation
   */
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      type: this.type,
      decisionIds: this.decisionIds,
      frequency: this.frequency,
      confidence: this.confidence,
      createdAt: this.createdAt,
      lastObserved: this.lastObserved,
      metadata: this.metadata
    };
  }

  /**
   * Create Pattern from JSON object
   * @param {Object} json - JSON object
   * @returns {Pattern} Pattern instance
   */
  static fromJSON(json) {
    return new Pattern(json);
  }

  /**
   * Add a decision to this pattern
   * @param {string} decisionId - Decision ID
   */
  addDecision(decisionId) {
    if (!this.decisionIds.includes(decisionId)) {
      this.decisionIds.push(decisionId);
      this.frequency = this.decisionIds.length;
      this.lastObserved = now();
    }
  }

  /**
   * Get pattern summary for display
   * @returns {string} Formatted summary
   */
  getSummary() {
    const typeEmoji = {
      'bias': '⚠️',
      'strength': '💪',
      'weakness': '⚡',
      'habit': '🔄',
      'observation': '👁️'
    }[this.type] || '👁️';

    return `${typeEmoji} ${this.name} (${this.frequency}x)\n` +
           `   Type: ${this.type} | Confidence: ${Math.round(this.confidence * 100)}%`;
  }
}

module.exports = {
  Decision,
  Review,
  Pattern,
  generateId,
  now
};
