/**
 * Decision Journal - Main Entry Point
 * 
 * This is the main module that exports all functionality
 * for the decision-journal skill.
 */

const { Decision, Review, Pattern, generateId, now } = require('./models');
const { Storage, DEFAULT_STORAGE_DIR } = require('./storage');
const { Reminder } = require('./reminder');

/**
 * DecisionJournal class - High-level API for managing decisions
 */
class DecisionJournal {
  /**
   * Create a new DecisionJournal instance
   * @param {Object} options - Configuration options
   * @param {string} [options.storageDir] - Custom storage directory
   */
  constructor(options = {}) {
    this.storage = new Storage(options.storageDir);
    this.reminder = new Reminder(this.storage);
  }

  /**
   * Record a new decision
   * @param {Object} data - Decision data
   * @returns {Decision} The created decision
   */
  recordDecision(data) {
    const decision = new Decision(data);
    return this.storage.saveDecision(decision);
  }

  /**
   * Get a decision by ID
   * @param {string} id - Decision ID
   * @returns {Decision|null} The decision or null
   */
  getDecision(id) {
    return this.storage.getDecision(id);
  }

  /**
   * List all decisions with optional filtering
   * @param {Object} filters - Filter options
   * @returns {Decision[]} Array of decisions
   */
  listDecisions(filters = {}) {
    return this.storage.loadDecisionsFiltered(filters);
  }

  /**
   * Review a decision with outcomes
   * @param {string} decisionId - Decision ID
   * @param {Object} reviewData - Review data
   * @returns {boolean} True if successful
   */
  reviewDecision(decisionId, reviewData) {
    const decision = this.storage.getDecision(decisionId);
    
    if (!decision) {
      return false;
    }
    
    decision.addReview(reviewData);
    this.storage.updateDecision(decision);
    
    // Also save as a separate review record
    const review = new Review({
      decisionId: decision.id,
      outcome: reviewData.outcome,
      lessons: reviewData.lessons,
      satisfaction: reviewData.satisfaction,
      processQuality: reviewData.processQuality,
      outcomeAccuracy: reviewData.outcomeAccuracy
    });
    this.storage.saveReview(review);
    
    return true;
  }

  /**
   * Get decisions due for review
   * @returns {Decision[]} Array of decisions due for review
   */
  getDueReviews() {
    return this.reminder.getDueDecisions();
  }

  /**
   * Get review reminders
   * @returns {Object} Reminder summary
   */
  getReminders() {
    return this.reminder.getReviewSummary();
  }

  /**
   * Generate reminder message
   * @param {Object} options - Options
   * @returns {string|null} Reminder message or null
   */
  generateReminderMessage(options = {}) {
    return this.reminder.generateReminderMessage(options);
  }

  /**
   * Get statistics
   * @returns {Object} Statistics
   */
  getStats() {
    return this.storage.getStats();
  }

  /**
   * Analyze decision patterns
   * @param {Object} options - Analysis options
   * @returns {Object} Analysis results
   */
  analyze(options = {}) {
    const decisions = this.storage.loadDecisionsFiltered(options);
    
    const byTag = {};
    const byStatus = {};
    let totalImportance = 0;
    let reviewedCount = 0;
    let totalSatisfaction = 0;
    
    decisions.forEach(d => {
      byTag[d.tag] = (byTag[d.tag] || 0) + 1;
      byStatus[d.status] = (byStatus[d.status] || 0) + 1;
      totalImportance += d.importance || 0;
      
      if (d.status === 'reviewed') {
        reviewedCount++;
        if (d.satisfaction) {
          totalSatisfaction += d.satisfaction;
        }
      }
    });
    
    return {
      total: decisions.length,
      byTag,
      byStatus,
      averageImportance: decisions.length > 0 ? totalImportance / decisions.length : 0,
      reviewedCount,
      averageSatisfaction: reviewedCount > 0 ? totalSatisfaction / reviewedCount : 0,
      reviewRate: decisions.length > 0 ? reviewedCount / decisions.length : 0
    };
  }

  /**
   * Export decisions
   * @param {string} format - Export format
   * @returns {string} Exported data
   */
  export(format = 'json') {
    return this.storage.exportData(format);
  }
}

// Export all modules
module.exports = {
  // Main class
  DecisionJournal,
  
  // Models
  Decision,
  Review,
  Pattern,
  
  // Utilities
  Storage,
  Reminder,
  generateId,
  now,
  DEFAULT_STORAGE_DIR
};
