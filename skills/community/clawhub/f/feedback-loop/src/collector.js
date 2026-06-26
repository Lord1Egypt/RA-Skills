/**
 * Feedback Collector - Handles explicit and implicit feedback collection
 */
const Storage = require('./storage');

class FeedbackCollector {
  constructor() {
    this.storage = new Storage();
  }

  /**
   * Collect explicit feedback from user
   * @param {Object} data - Feedback data
   * @param {string} data.sessionId - Session identifier
   * @param {string} data.rating - Rating (1-5 or thumbs_up/thumbs_down)
   * @param {string} data.comment - Optional comment
   * @param {string} data.category - Feedback category (accuracy, speed, helpfulness, etc.)
   * @param {Object} data.metadata - Additional context
   */
  collectExplicit(data) {
    const feedback = {
      type: 'explicit',
      sessionId: data.sessionId || 'unknown',
      rating: data.rating,
      comment: data.comment || '',
      category: data.category || 'general',
      metadata: data.metadata || {},
      source: data.source || 'cli'
    };

    this.storage.addFeedback(feedback);
    return {
      success: true,
      message: 'Explicit feedback recorded',
      feedback
    };
  }

  /**
   * Collect implicit feedback from interaction patterns
   * @param {Object} data - Implicit feedback data
   * @param {string} data.sessionId - Session identifier
   * @param {string} data.signal - Signal type (completion, correction, retry, abandon, etc.)
   * @param {Object} data.metrics - Quantitative metrics
   * @param {Object} data.context - Context information
   */
  collectImplicit(data) {
    const feedback = {
      type: 'implicit',
      sessionId: data.sessionId || 'unknown',
      signal: data.signal,
      metrics: data.metrics || {},
      context: data.context || {},
      inferredSentiment: this.inferSentiment(data.signal, data.metrics)
    };

    this.storage.addFeedback(feedback);
    return {
      success: true,
      message: 'Implicit feedback recorded',
      feedback
    };
  }

  /**
   * Infer sentiment from implicit signals
   */
  inferSentiment(signal, metrics) {
    const positiveSignals = ['completion', 'success', 'quick_accept', 'share', 'save'];
    const negativeSignals = ['correction', 'retry', 'abandon', 'timeout', 'error', 'complaint'];
    const neutralSignals = ['view', 'scroll', 'hover'];

    if (positiveSignals.includes(signal)) return 'positive';
    if (negativeSignals.includes(signal)) return 'negative';
    if (neutralSignals.includes(signal)) return 'neutral';

    // Infer from metrics
    if (metrics) {
      if (metrics.responseTime && metrics.responseTime > 10000) return 'negative';
      if (metrics.retryCount && metrics.retryCount > 2) return 'negative';
      if (metrics.completionRate && metrics.completionRate > 0.8) return 'positive';
    }

    return 'unknown';
  }

  /**
   * Auto-detect feedback from session patterns
   * @param {Object} sessionData - Session interaction data
   */
  autoDetect(sessionData) {
    const detections = [];

    // Detect frustration patterns
    if (sessionData.retryCount > 3) {
      detections.push({
        signal: 'high_retry_rate',
        confidence: 0.8,
        inferredIssue: 'user struggling with response'
      });
    }

    // Detect satisfaction
    if (sessionData.completionRate === 1 && sessionData.responseTime < 5000) {
      detections.push({
        signal: 'smooth_completion',
        confidence: 0.9,
        inferredIssue: null
      });
    }

    // Detect abandonment
    if (sessionData.abandoned && sessionData.timeSpent < 10000) {
      detections.push({
        signal: 'early_abandonment',
        confidence: 0.7,
        inferredIssue: 'response not meeting expectations'
      });
    }

    // Detect engagement
    if (sessionData.followUpQuestions > 2) {
      detections.push({
        signal: 'high_engagement',
        confidence: 0.75,
        inferredIssue: null
      });
    }

    // Record implicit feedback for each detection
    detections.forEach(detection => {
      this.collectImplicit({
        sessionId: sessionData.sessionId,
        signal: detection.signal,
        metrics: {
          confidence: detection.confidence,
          ...sessionData
        },
        context: {
          autoDetected: true,
          inferredIssue: detection.inferredIssue
        }
      });
    });

    return {
      success: true,
      detections,
      count: detections.length
    };
  }

  /**
   * Get feedback for a specific session
   */
  getSessionFeedback(sessionId) {
    return this.storage.getFeedbackBySession(sessionId);
  }

  /**
   * Get all feedback with optional filtering
   */
  getAllFeedback(filters = {}) {
    let feedbacks = this.storage.getAllFeedback();

    if (filters.type) {
      feedbacks = feedbacks.filter(f => f.type === filters.type);
    }
    if (filters.category) {
      feedbacks = feedbacks.filter(f => f.category === filters.category);
    }
    if (filters.since) {
      const sinceDate = new Date(filters.since);
      feedbacks = feedbacks.filter(f => new Date(f.timestamp) >= sinceDate);
    }
    if (filters.limit) {
      feedbacks = feedbacks.slice(-filters.limit);
    }

    return feedbacks;
  }
}

module.exports = FeedbackCollector;
