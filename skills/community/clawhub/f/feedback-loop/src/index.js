/**
 * Feedback Loop Skill - Main Entry Point
 * 
 * A comprehensive feedback collection, analysis, and improvement tracking system
 * for OpenClaw agents.
 */

const Storage = require('./storage');
const FeedbackCollector = require('./collector');
const FeedbackAnalyzer = require('./analyzer');
const ImprovementSuggester = require('./suggester');
const EffectTracker = require('./tracker');

class FeedbackLoop {
  constructor() {
    this.storage = new Storage();
    this.collector = new FeedbackCollector();
    this.analyzer = new FeedbackAnalyzer();
    this.suggester = new ImprovementSuggester();
    this.tracker = new EffectTracker();
  }

  /**
   * Provide feedback (explicit or implicit)
   */
  provide(data) {
    if (data.type === 'implicit' || data.signal) {
      return this.collector.collectImplicit(data);
    }
    return this.collector.collectExplicit(data);
  }

  /**
   * Analyze feedback data
   */
  analyze(options = {}) {
    return this.analyzer.analyze(options);
  }

  /**
   * Generate improvement suggestions
   */
  suggest(options = {}) {
    return this.suggester.generate(options);
  }

  /**
   * Track implementation progress
   */
  track(suggestionId, data) {
    return this.tracker.track(suggestionId, data);
  }

  /**
   * Measure impact of implemented suggestions
   */
  measureImpact(suggestionId, options = {}) {
    return this.tracker.measureImpact(suggestionId, options);
  }

  /**
   * Get statistics
   */
  getStats() {
    return this.storage.getStats();
  }

  /**
   * Get all feedback
   */
  getFeedback(filters = {}) {
    return this.collector.getAllFeedback(filters);
  }

  /**
   * Get all suggestions
   */
  getSuggestions(filters = {}) {
    return this.suggester.getSuggestions(filters);
  }

  /**
   * Update suggestion status
   */
  updateSuggestionStatus(id, status, note) {
    return this.suggester.updateStatus(id, status, note);
  }

  /**
   * Get tracking report
   */
  getReport(options = {}) {
    return this.tracker.getReport(options);
  }

  /**
   * Auto-detect feedback from session data
   */
  autoDetect(sessionData) {
    return this.collector.autoDetect(sessionData);
  }

  /**
   * Export data
   */
  exportData(format = 'json') {
    return this.tracker.exportData(format);
  }
}

// Export for use as module
module.exports = FeedbackLoop;

// Export individual components
module.exports.Storage = Storage;
module.exports.FeedbackCollector = FeedbackCollector;
module.exports.FeedbackAnalyzer = FeedbackAnalyzer;
module.exports.ImprovementSuggester = ImprovementSuggester;
module.exports.EffectTracker = EffectTracker;

// CLI execution
if (require.main === module) {
  const cli = require('../bin/cli');
  cli.run(process.argv);
}
