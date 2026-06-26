/**
 * Effect Tracker - Tracks implementation progress and measures impact
 */
const Storage = require('./storage');
const FeedbackAnalyzer = require('./analyzer');

class EffectTracker {
  constructor() {
    this.storage = new Storage();
    this.analyzer = new FeedbackAnalyzer();
  }

  /**
   * Track the implementation of a suggestion
   * @param {string} suggestionId - ID of the suggestion being tracked
   * @param {Object} data - Tracking data
   */
  track(suggestionId, data) {
    const suggestion = this.storage.getAllSuggestions().find(s => s.id === suggestionId);
    
    if (!suggestion) {
      return {
        success: false,
        message: 'Suggestion not found'
      };
    }

    const trackingEntry = {
      suggestionId,
      category: suggestion.category,
      phase: data.phase || 'implementation',
      metrics: data.metrics || {},
      notes: data.notes || '',
      status: data.status || 'in_progress'
    };

    this.storage.addTrackingEntry(trackingEntry);

    return {
      success: true,
      message: 'Tracking entry recorded',
      entry: trackingEntry
    };
  }

  /**
   * Measure the impact of implemented suggestions
   * @param {string} suggestionId - ID of the suggestion
   * @param {Object} options - Measurement options
   */
  measureImpact(suggestionId, options = {}) {
    const suggestion = this.storage.getAllSuggestions().find(s => s.id === suggestionId);
    
    if (!suggestion) {
      return {
        success: false,
        message: 'Suggestion not found'
      };
    }

    const trackingEntries = this.storage.getTrackingBySuggestion(suggestionId);
    const category = suggestion.category;
    
    // Get feedback before and after implementation
    const beforeDate = suggestion.timestamp;
    const afterDate = trackingEntries.length > 0 
      ? trackingEntries[0].timestamp 
      : new Date().toISOString();

    const beforeAnalysis = this.analyzer.analyze({ 
      timeRange: options.beforeRange || 'week' 
    });
    
    const afterAnalysis = this.analyzer.analyze({ 
      timeRange: options.afterRange || 'week' 
    });

    // Calculate impact metrics
    const impact = this.calculateImpact(beforeAnalysis.analysis, afterAnalysis.analysis, category);

    return {
      success: true,
      suggestion,
      trackingEntries,
      impact
    };
  }

  /**
   * Calculate impact metrics
   */
  calculateImpact(before, after, category) {
    if (!before || !after) {
      return {
        available: false,
        reason: 'Insufficient data for comparison'
      };
    }

    const impact = {
      available: true,
      metrics: {}
    };

    // Sentiment improvement
    if (before.sentiment && after.sentiment) {
      const beforeScore = parseFloat(before.sentiment.sentimentScore);
      const afterScore = parseFloat(after.sentiment.sentimentScore);
      impact.metrics.sentimentChange = (afterScore - beforeScore).toFixed(3);
      impact.metrics.sentimentImproved = afterScore > beforeScore;
    }

    // Rating improvement in specific category
    if (before.categories && after.categories) {
      const beforeCat = before.categories.find(c => c.name === category);
      const afterCat = after.categories.find(c => c.name === category);
      
      if (beforeCat && afterCat && beforeCat.avgRating && afterCat.avgRating) {
        const ratingChange = parseFloat(afterCat.avgRating) - parseFloat(beforeCat.avgRating);
        impact.metrics.ratingChange = ratingChange.toFixed(2);
        impact.metrics.ratingImproved = ratingChange > 0;
      }
    }

    // Overall feedback volume change
    impact.metrics.feedbackVolumeChange = after.totalFeedback - before.totalFeedback;

    // Negative feedback reduction
    if (before.sentiment && after.sentiment) {
      const beforeNegative = before.sentiment.percentages.negative;
      const afterNegative = after.sentiment.percentages.negative;
      impact.metrics.negativeReduction = (beforeNegative - afterNegative).toFixed(1);
    }

    // Overall assessment
    const positiveMetrics = Object.values(impact.metrics).filter(m => 
      (typeof m === 'number' && m > 0) || m === true
    ).length;
    
    const negativeMetrics = Object.values(impact.metrics).filter(m => 
      (typeof m === 'number' && m < 0) || m === false
    ).length;

    impact.overall = positiveMetrics > negativeMetrics ? 'positive' : 
                     negativeMetrics > positiveMetrics ? 'negative' : 'neutral';

    return impact;
  }

  /**
   * Get tracking report for all suggestions
   */
  getReport(options = {}) {
    const suggestions = this.storage.getAllSuggestions();
    const tracking = this.storage.getAllTracking();
    
    const report = {
      generated: new Date().toISOString(),
      summary: {
        totalSuggestions: suggestions.length,
        implemented: suggestions.filter(s => s.status === 'implemented').length,
        inProgress: suggestions.filter(s => s.status === 'in_progress').length,
        pending: suggestions.filter(s => s.status === 'pending').length,
        rejected: suggestions.filter(s => s.status === 'rejected').length
      },
      tracking: {
        totalEntries: tracking.length,
        byPhase: this.groupByPhase(tracking),
        byCategory: this.groupByCategory(tracking)
      },
      suggestions: suggestions.map(s => ({
        id: s.id,
        title: s.title,
        category: s.category,
        priority: s.priority,
        status: s.status,
        createdAt: s.timestamp,
        updatedAt: s.updatedAt,
        trackingCount: tracking.filter(t => t.suggestionId === s.id).length
      }))
    };

    // Add impact summaries for implemented suggestions
    report.impactSummaries = suggestions
      .filter(s => s.status === 'implemented')
      .map(s => {
        const impact = this.measureImpact(s.id, options);
        return {
          suggestionId: s.id,
          title: s.title,
          impact: impact.impact
        };
      });

    return report;
  }

  /**
   * Group tracking entries by phase
   */
  groupByPhase(tracking) {
    const phases = {};
    tracking.forEach(t => {
      phases[t.phase] = (phases[t.phase] || 0) + 1;
    });
    return phases;
  }

  /**
   * Group tracking entries by category
   */
  groupByCategory(tracking) {
    const categories = {};
    tracking.forEach(t => {
      categories[t.category] = (categories[t.category] || 0) + 1;
    });
    return categories;
  }

  /**
   * Get tracking entries for a suggestion
   */
  getTracking(suggestionId) {
    return this.storage.getTrackingBySuggestion(suggestionId);
  }

  /**
   * Get all tracking entries
   */
  getAllTracking(filters = {}) {
    let tracking = this.storage.getAllTracking();

    if (filters.suggestionId) {
      tracking = tracking.filter(t => t.suggestionId === filters.suggestionId);
    }
    if (filters.phase) {
      tracking = tracking.filter(t => t.phase === filters.phase);
    }
    if (filters.category) {
      tracking = tracking.filter(t => t.category === filters.category);
    }
    if (filters.limit) {
      tracking = tracking.slice(-filters.limit);
    }

    return tracking;
  }

  /**
   * Export tracking data
   */
  exportData(format = 'json') {
    const tracking = this.storage.getAllTracking();
    const suggestions = this.storage.getAllSuggestions();
    
    if (format === 'json') {
      return JSON.stringify({ tracking, suggestions }, null, 2);
    }
    
    if (format === 'csv') {
      const headers = ['id', 'suggestionId', 'category', 'phase', 'timestamp', 'status', 'notes'];
      const rows = tracking.map(t => 
        headers.map(h => `"${t[h] || ''}"`).join(',')
      );
      return [headers.join(','), ...rows].join('\n');
    }

    return JSON.stringify({ tracking, suggestions }, null, 2);
  }
}

module.exports = EffectTracker;
