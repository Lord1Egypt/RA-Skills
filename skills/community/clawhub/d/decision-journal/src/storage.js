/**
 * Storage Module for Decision Journal
 * 
 * Handles persistence of decisions, reviews, and patterns
 * using JSONL (JSON Lines) format for append-only logging.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { Decision, Review, Pattern } = require('./models');

// Default storage directory
const DEFAULT_STORAGE_DIR = path.join(os.homedir(), '.openclaw', 'decisions');

/**
 * Storage class for managing decision data persistence
 */
class Storage {
  /**
   * Create a new Storage instance
   * @param {string} [baseDir] - Base directory for storage (default: ~/.openclaw/decisions)
   */
  constructor(baseDir = DEFAULT_STORAGE_DIR) {
    this.baseDir = baseDir;
    this.decisionsFile = path.join(baseDir, 'decisions.jsonl');
    this.reviewsFile = path.join(baseDir, 'reviews.jsonl');
    this.patternsFile = path.join(baseDir, 'patterns.json');
    this.indexFile = path.join(baseDir, 'index.json');
    
    // Ensure storage directory exists
    this.ensureStorage();
  }

  /**
   * Ensure storage directory and files exist
   */
  ensureStorage() {
    if (!fs.existsSync(this.baseDir)) {
      fs.mkdirSync(this.baseDir, { recursive: true });
    }
    
    // Create files if they don't exist
    [this.decisionsFile, this.reviewsFile].forEach(file => {
      if (!fs.existsSync(file)) {
        fs.writeFileSync(file, '');
      }
    });
    
    // Create index if it doesn't exist
    if (!fs.existsSync(this.indexFile)) {
      fs.writeFileSync(this.indexFile, JSON.stringify({
        decisions: [],
        reviews: [],
        tags: {},
        stats: {
          totalDecisions: 0,
          totalReviews: 0,
          lastUpdated: null
        }
      }, null, 2));
    }
    
    // Create patterns file if it doesn't exist
    if (!fs.existsSync(this.patternsFile)) {
      fs.writeFileSync(this.patternsFile, JSON.stringify({ patterns: [] }, null, 2));
    }
  }

  /**
   * Load all decisions from storage
   * @returns {Decision[]} Array of Decision objects
   */
  loadDecisions() {
    const decisions = [];
    
    if (!fs.existsSync(this.decisionsFile)) {
      return decisions;
    }
    
    const content = fs.readFileSync(this.decisionsFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    for (const line of lines) {
      try {
        const data = JSON.parse(line);
        decisions.push(Decision.fromJSON(data));
      } catch (e) {
        // Skip invalid lines
        continue;
      }
    }
    
    // Sort by date descending
    return decisions.sort((a, b) => 
      new Date(b.createdAt) - new Date(a.createdAt)
    );
  }

  /**
   * Load decisions with optional filtering
   * @param {Object} filters - Filter options
   * @param {string} [filters.tag] - Filter by tag
   * @param {string} [filters.status] - Filter by status
   * @param {number} [filters.limit] - Limit number of results
   * @param {string} [filters.since] - Filter by date (YYYY-MM-DD)
   * @returns {Decision[]} Filtered decisions
   */
  loadDecisionsFiltered(filters = {}) {
    let decisions = this.loadDecisions();
    
    if (filters.tag) {
      decisions = decisions.filter(d => d.tag === filters.tag);
    }
    
    if (filters.status) {
      decisions = decisions.filter(d => d.status === filters.status);
    }
    
    if (filters.since) {
      decisions = decisions.filter(d => d.createdAt >= filters.since);
    }
    
    if (filters.limit) {
      decisions = decisions.slice(0, filters.limit);
    }
    
    return decisions;
  }

  /**
   * Get a single decision by ID
   * @param {string} id - Decision ID
   * @returns {Decision|null} Decision object or null if not found
   */
  getDecision(id) {
    const decisions = this.loadDecisions();
    return decisions.find(d => d.id === id) || null;
  }

  /**
   * Save a decision to storage
   * @param {Decision} decision - Decision to save
   * @returns {Decision} Saved decision
   */
  saveDecision(decision) {
    const line = JSON.stringify(decision.toJSON()) + '\n';
    fs.appendFileSync(this.decisionsFile, line);
    this.updateIndex('decision', decision);
    return decision;
  }

  /**
   * Update an existing decision
   * @param {Decision} decision - Decision to update
   * @returns {boolean} True if updated successfully
   */
  updateDecision(decision) {
    const decisions = this.loadDecisions();
    const index = decisions.findIndex(d => d.id === decision.id);
    
    if (index === -1) {
      return false;
    }
    
    decisions[index] = decision;
    
    // Rewrite entire file
    const lines = decisions.map(d => JSON.stringify(d.toJSON())).join('\n') + '\n';
    fs.writeFileSync(this.decisionsFile, lines);
    
    this.rebuildIndex();
    return true;
  }

  /**
   * Load all reviews from storage
   * @returns {Review[]} Array of Review objects
   */
  loadReviews() {
    const reviews = [];
    
    if (!fs.existsSync(this.reviewsFile)) {
      return reviews;
    }
    
    const content = fs.readFileSync(this.reviewsFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    for (const line of lines) {
      try {
        const data = JSON.parse(line);
        reviews.push(Review.fromJSON(data));
      } catch (e) {
        continue;
      }
    }
    
    return reviews.sort((a, b) => 
      new Date(b.createdAt) - new Date(a.createdAt)
    );
  }

  /**
   * Get reviews for a specific decision
   * @param {string} decisionId - Decision ID
   * @returns {Review[]} Array of Review objects
   */
  getReviewsForDecision(decisionId) {
    const reviews = this.loadReviews();
    return reviews.filter(r => r.decisionId === decisionId);
  }

  /**
   * Save a review to storage
   * @param {Review} review - Review to save
   * @returns {Review} Saved review
   */
  saveReview(review) {
    const line = JSON.stringify(review.toJSON()) + '\n';
    fs.appendFileSync(this.reviewsFile, line);
    this.updateIndex('review', review);
    return review;
  }

  /**
   * Load all patterns from storage
   * @returns {Pattern[]} Array of Pattern objects
   */
  loadPatterns() {
    if (!fs.existsSync(this.patternsFile)) {
      return [];
    }
    
    try {
      const content = fs.readFileSync(this.patternsFile, 'utf-8');
      const data = JSON.parse(content);
      return (data.patterns || []).map(p => Pattern.fromJSON(p));
    } catch (e) {
      return [];
    }
  }

  /**
   * Save a pattern to storage
   * @param {Pattern} pattern - Pattern to save
   * @returns {Pattern} Saved pattern
   */
  savePattern(pattern) {
    const patterns = this.loadPatterns();
    const existingIndex = patterns.findIndex(p => p.id === pattern.id);
    
    if (existingIndex >= 0) {
      patterns[existingIndex] = pattern;
    } else {
      patterns.push(pattern);
    }
    
    fs.writeFileSync(this.patternsFile, JSON.stringify({ patterns }, null, 2));
    return pattern;
  }

  /**
   * Delete a pattern
   * @param {string} patternId - Pattern ID to delete
   * @returns {boolean} True if deleted
   */
  deletePattern(patternId) {
    const patterns = this.loadPatterns();
    const filtered = patterns.filter(p => p.id !== patternId);
    
    if (filtered.length === patterns.length) {
      return false;
    }
    
    fs.writeFileSync(this.patternsFile, JSON.stringify({ patterns: filtered }, null, 2));
    return true;
  }

  /**
   * Update the index with new entry
   * @param {string} type - Entry type ('decision' or 'review')
 * @param {Decision|Review} entry - Entry to index
   */
  updateIndex(type, entry) {
    let index;
    try {
      index = JSON.parse(fs.readFileSync(this.indexFile, 'utf-8'));
    } catch (e) {
      index = {      decisions: [],
        reviews: [],
        tags: {},
        stats: { totalDecisions: 0, totalReviews: 0, lastUpdated: null }
      };
    }
    
    if (type === 'decision') {
      index.decisions.push({
        id: entry.id,
        title: entry.title,
        tag: entry.tag,
        status: entry.status,
        createdAt: entry.createdAt,
        reviewDate: entry.reviewDate
      });
      
      // Update tag counts
      if (!index.tags[entry.tag]) {
        index.tags[entry.tag] = 0;
      }
      index.tags[entry.tag]++;
      
      index.stats.totalDecisions++;
    } else if (type === 'review') {
      index.reviews.push({
        id: entry.id,
        decisionId: entry.decisionId,
        createdAt: entry.createdAt
      });
      index.stats.totalReviews++;
    }
    
    index.stats.lastUpdated = new Date().toISOString();
    fs.writeFileSync(this.indexFile, JSON.stringify(index, null, 2));
  }

  /**
   * Rebuild the entire index from data files
   */
  rebuildIndex() {
    const decisions = this.loadDecisions();
    const reviews = this.loadReviews();
    
    const tags = {};
    decisions.forEach(d => {
      if (!tags[d.tag]) tags[d.tag] = 0;
      tags[d.tag]++;
    });
    
    const index = {
      decisions: decisions.map(d => ({
        id: d.id,
        title: d.title,
        tag: d.tag,
        status: d.status,
        createdAt: d.createdAt,
        reviewDate: d.reviewDate
      })),
      reviews: reviews.map(r => ({
        id: r.id,
        decisionId: r.decisionId,
        createdAt: r.createdAt
      })),
      tags,
      stats: {
        totalDecisions: decisions.length,
        totalReviews: reviews.length,
        lastUpdated: new Date().toISOString()
      }
    };
    
    fs.writeFileSync(this.indexFile, JSON.stringify(index, null, 2));
  }

  /**
   * Get decisions that are due for review
   * @returns {Decision[]} Decisions due for review
   */
  getDueReviews() {
    const decisions = this.loadDecisions();
    const today = new Date().toISOString().split('T')[0];
    
    return decisions.filter(d => 
      d.reviewDate && 
      d.reviewDate <= today && 
      d.status !== 'reviewed'
    );
  }

  /**
   * Get statistics about decisions
   * @returns {Object} Statistics object
   */
  getStats() {
    const decisions = this.loadDecisions();
    const reviews = this.loadReviews();
    
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
      totalDecisions: decisions.length,
      totalReviews: reviews.length,
      reviewedDecisions: reviewedCount,
      pendingReviews: decisions.filter(d => d.isDueForReview()).length,
      averageImportance: decisions.length > 0 ? totalImportance / decisions.length : 0,
      averageSatisfaction: reviewedCount > 0 ? totalSatisfaction / reviewedCount : 0,
      byTag,
      byStatus
    };
  }

  /**
   * Export all data to a specific format
   * @param {string} format - Export format ('json', 'markdown', 'csv')
   * @returns {string} Exported data
   */
  exportData(format = 'json') {
    const decisions = this.loadDecisions();
    
    switch (format.toLowerCase()) {
      case 'json':
        return JSON.stringify(decisions.map(d => d.toJSON()), null, 2);
      
      case 'markdown':
        return this.exportToMarkdown(decisions);
      
      case 'csv':
        return this.exportToCSV(decisions);
      
      default:
        throw new Error(`Unsupported format: ${format}`);
    }
  }

  /**
   * Export decisions to Markdown format
   * @param {Decision[]} decisions - Decisions to export
   * @returns {string} Markdown content
   */
  exportToMarkdown(decisions) {
    const lines = ['# Decision Journal Export\n'];
    
    decisions.forEach(d => {
      lines.push(`## ${d.title}`);
      lines.push(`- **ID:** ${d.id}`);
      lines.push(`- **Date:** ${d.createdAt.split('T')[0]}`);
      lines.push(`- **Status:** ${d.status}`);
      lines.push(`- **Tag:** ${d.tag}`);
      lines.push(`- **Importance:** ${'⭐'.repeat(d.importance)}`);
      
      if (d.situation) lines.push(`- **Situation:** ${d.situation}`);
      if (d.options && d.options.length > 0) {
        lines.push(`- **Options:** ${d.options.join(', ')}`);
      }
      if (d.decision) lines.push(`- **Decision:** ${d.decision}`);
      if (d.reasoning) lines.push(`- **Reasoning:** ${d.reasoning}`);
      if (d.expected) lines.push(`- **Expected:** ${d.expected}`);
      if (d.reviewDate) lines.push(`- **Review Date:** ${d.reviewDate}`);
      if (d.outcome) lines.push(`- **Outcome:** ${d.outcome}`);
      if (d.lessons) lines.push(`- **Lessons:** ${d.lessons}`);
      if (d.satisfaction) lines.push(`- **Satisfaction:** ${'⭐'.repeat(d.satisfaction)}`);
      
      lines.push('');
    });
    
    return lines.join('\n');
  }

  /**
   * Export decisions to CSV format
   * @param {Decision[]} decisions - Decisions to export
   * @returns {string} CSV content
   */
  exportToCSV(decisions) {
    if (decisions.length === 0) return '';
    
    const headers = ['id', 'title', 'situation', 'decision', 'tag', 'importance', 
                     'status', 'createdAt', 'reviewDate', 'outcome', 'satisfaction'];
    
    const escapeCSV = (value) => {
      if (value === null || value === undefined) return '';
      const str = String(value);
      if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };
    
    const lines = [headers.join(',')];
    
    decisions.forEach(d => {
      const row = headers.map(h => escapeCSV(d[h]));
      lines.push(row.join(','));
    });
    
    return lines.join('\n');
  }
}

module.exports = { Storage, DEFAULT_STORAGE_DIR };
