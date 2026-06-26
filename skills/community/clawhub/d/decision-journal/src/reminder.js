/**
 * Reminder Module for Decision Journal
 * 
 * Handles review reminders and notifications for decisions
 * that are due for review.
 */

const { Storage } = require('./storage');

/**
 * Reminder class for managing review notifications
 */
class Reminder {
  /**
   * Create a new Reminder instance
   * @param {Storage} [storage] - Storage instance
   */
  constructor(storage = null) {
    this.storage = storage || new Storage();
  }

  /**
   * Get all decisions that are due for review
   * @returns {Array} Array of decisions due for review
   */
  getDueDecisions() {
    return this.storage.getDueReviews();
  }

  /**
   * Get decisions due within a specific number of days
   * @param {number} days - Number of days to look ahead
   * @returns {Array} Array of decisions due within the timeframe
   */
  getUpcomingReviews(days = 7) {
    const decisions = this.storage.loadDecisions();
    const today = new Date();
    const futureDate = new Date(today.getTime() + days * 24 * 60 * 60 * 1000);
    
    return decisions.filter(d => {
      if (!d.reviewDate || d.status === 'reviewed') {
        return false;
      }
      const reviewDate = new Date(d.reviewDate);
      return reviewDate <= futureDate && reviewDate >= today;
    });
  }

  /**
   * Get overdue decisions (past review date but not reviewed)
   * @returns {Array} Array of overdue decisions
   */
  getOverdueDecisions() {
    const decisions = this.storage.loadDecisions();
    const today = new Date().toISOString().split('T')[0];
    
    return decisions.filter(d => {
      if (!d.reviewDate || d.status === 'reviewed') {
        return false;
      }
      return d.reviewDate < today;
    }).sort((a, b) => {
      // Sort by how overdue (oldest first)
      return new Date(a.reviewDate) - new Date(b.reviewDate);
    });
  }

  /**
   * Generate a reminder message
   * @param {Object} options - Options for the reminder
   * @param {boolean} [options.includeOverdue=true] - Include overdue decisions
   * @param {boolean} [options.includeUpcoming=true] - Include upcoming decisions
   * @param {number} [options.upcomingDays=7] - Days to look ahead for upcoming
   * @returns {string} Formatted reminder message
   */
  generateReminderMessage(options = {}) {
    const includeOverdue = options.includeOverdue !== false;
    const includeUpcoming = options.includeUpcoming !== false;
    const upcomingDays = options.upcomingDays || 7;
    
    const overdue = includeOverdue ? this.getOverdueDecisions() : [];
    const upcoming = includeUpcoming ? this.getUpcomingReviews(upcomingDays) : [];
    
    if (overdue.length === 0 && upcoming.length === 0) {
      return null;
    }
    
    const lines = [];
    
    if (overdue.length > 0) {
      lines.push(`🔔 **Decision Review Reminders**`);
      lines.push('');
      lines.push(`⏰ **Overdue Reviews (${overdue.length}):**`);
      lines.push('');
      
      overdue.forEach((d, i) => {
        const daysOverdue = Math.floor(
          (new Date() - new Date(d.reviewDate)) / (1000 * 60 * 60 * 24)
        );
        lines.push(`${i + 1}. **${d.title}**`);
        lines.push(`   ID: \`${d.id}\` | Review: ${d.reviewDate} (${daysOverdue} days overdue)`);
        if (d.expected) {
          lines.push(`   Expected: ${d.expected.substring(0, 100)}${d.expected.length > 100 ? '...' : ''}`);
        }
        lines.push(`   → Run: \`decision review ${d.id} --outcome "..."\``);
        lines.push('');
      });
    }
    
    if (upcoming.length > 0) {
      if (overdue.length === 0) {
        lines.push(`🔔 **Decision Review Reminders**`);
        lines.push('');
      }
      
      lines.push(`📅 **Upcoming Reviews (${upcoming.length}):**`);
      lines.push('');
      
      upcoming.forEach((d, i) => {
        const daysUntil = Math.ceil(
          (new Date(d.reviewDate) - new Date()) / (1000 * 60 * 60 * 24)
        );
        const daysText = daysUntil === 0 ? 'today' : `in ${daysUntil} day${daysUntil > 1 ? 's' : ''}`;
        lines.push(`${i + 1}. **${d.title}**`);
        lines.push(`   ID: \`${d.id}\` | Review: ${d.reviewDate} (${daysText})`);
        lines.push('');
      });
    }
    
    return lines.join('\n');
  }

  /**
   * Generate a summary of review status
   * @returns {Object} Summary object with counts and details
   */
  getReviewSummary() {
    const overdue = this.getOverdueDecisions();
    const upcoming = this.getUpcomingReviews(7);
    const dueToday = upcoming.filter(d => {
      return d.reviewDate === new Date().toISOString().split('T')[0];
    });
    
    return {
      overdue: {
        count: overdue.length,
        decisions: overdue
      },
      upcoming: {
        count: upcoming.length,
        decisions: upcoming
      },
      dueToday: {
        count: dueToday.length,
        decisions: dueToday
      },
      hasReminders: overdue.length > 0 || upcoming.length > 0
    };
  }

  /**
   * Check if there are any reminders to show
   * @returns {boolean} True if there are reminders
   */
  hasReminders() {
    const due = this.getDueDecisions();
    const upcoming = this.getUpcomingReviews(7);
    return due.length > 0 || upcoming.length > 0;
  }

  /**
   * Get reminder for a specific decision
   * @param {string} decisionId - Decision ID
   * @returns {Object|null} Reminder details or null
   */
  getDecisionReminder(decisionId) {
    const decision = this.storage.getDecision(decisionId);
    
    if (!decision || !decision.reviewDate) {
      return null;
    }
    
    const today = new Date();
    const reviewDate = new Date(decision.reviewDate);
    const daysDiff = Math.floor((reviewDate - today) / (1000 * 60 * 60 * 24));
    
    return {
      decisionId: decision.id,
      title: decision.title,
      reviewDate: decision.reviewDate,
      daysUntil: daysDiff,
      isOverdue: daysDiff < 0,
      isDueToday: daysDiff === 0,
      status: decision.status
    };
  }
}

module.exports = { Reminder };
