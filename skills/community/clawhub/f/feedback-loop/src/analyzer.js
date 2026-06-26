/**
 * Feedback Analyzer - Performs clustering, trend analysis, and pattern detection
 */
const Storage = require('./storage');

class FeedbackAnalyzer {
  constructor() {
    this.storage = new Storage();
  }

  /**
   * Analyze all feedback and generate insights
   * @param {Object} options - Analysis options
   * @param {string} options.timeRange - Time range (day, week, month, all)
   * @param {boolean} options.includeImplicit - Include implicit feedback
   */
  analyze(options = {}) {
    const timeRange = options.timeRange || 'week';
    const includeImplicit = options.includeImplicit !== false;

    // Get feedback data
    let feedbacks = this.storage.getAllFeedback();

    // Filter by time range
    const cutoffDate = this.getCutoffDate(timeRange);
    feedbacks = feedbacks.filter(f => new Date(f.timestamp) >= cutoffDate);

    if (!includeImplicit) {
      feedbacks = feedbacks.filter(f => f.type === 'explicit');
    }

    if (feedbacks.length === 0) {
      return {
        success: true,
        message: 'No feedback data available for analysis',
        insights: null
      };
    }

    // Perform analyses
    const clustering = this.performClustering(feedbacks);
    const trends = this.analyzeTrends(feedbacks, timeRange);
    const sentiment = this.analyzeSentiment(feedbacks);
    const categories = this.analyzeCategories(feedbacks);
    const patterns = this.detectPatterns(feedbacks);

    const analysis = {
      timestamp: new Date().toISOString(),
      timeRange,
      totalFeedback: feedbacks.length,
      clustering,
      trends,
      sentiment,
      categories,
      patterns
    };

    // Save analysis
    this.storage.saveAnalysis(analysis);

    return {
      success: true,
      message: 'Analysis completed',
      analysis
    };
  }

  /**
   * Perform clustering on feedback
   */
  performClustering(feedbacks) {
    const clusters = {
      byCategory: {},
      bySentiment: {},
      byRating: {}
    };

    // Cluster by category
    feedbacks.forEach(f => {
      const category = f.category || 'general';
      if (!clusters.byCategory[category]) {
        clusters.byCategory[category] = [];
      }
      clusters.byCategory[category].push(f);
    });

    // Cluster by sentiment
    feedbacks.forEach(f => {
      let sentiment;
      if (f.type === 'explicit') {
        sentiment = this.ratingToSentiment(f.rating);
      } else {
        sentiment = f.inferredSentiment || 'unknown';
      }
      if (!clusters.bySentiment[sentiment]) {
        clusters.bySentiment[sentiment] = [];
      }
      clusters.bySentiment[sentiment].push(f);
    });

    // Cluster by rating
    feedbacks.filter(f => f.type === 'explicit').forEach(f => {
      const rating = f.rating || 'unknown';
      if (!clusters.byRating[rating]) {
        clusters.byRating[rating] = [];
      }
      clusters.byRating[rating].push(f);
    });

    // Summarize clusters
    const summary = {
      byCategory: Object.entries(clusters.byCategory).map(([cat, items]) => ({
        category: cat,
        count: items.length,
        percentage: Math.round((items.length / feedbacks.length) * 100)
      })).sort((a, b) => b.count - a.count),

      bySentiment: Object.entries(clusters.bySentiment).map(([sent, items]) => ({
        sentiment: sent,
        count: items.length,
        percentage: Math.round((items.length / feedbacks.length) * 100)
      })).sort((a, b) => b.count - a.count),

      byRating: Object.entries(clusters.byRating).map(([rating, items]) => ({
        rating,
        count: items.length,
        percentage: Math.round((items.length / feedbacks.length) * 100)
      })).sort((a, b) => b.count - a.count)
    };

    return {
      totalClusters: Object.keys(clusters.byCategory).length,
      summary
    };
  }

  /**
   * Analyze trends over time
   */
  analyzeTrends(feedbacks, timeRange) {
    const timeBuckets = this.createTimeBuckets(timeRange);
    
    // Group feedback by time bucket
    feedbacks.forEach(f => {
      const bucket = this.getTimeBucket(f.timestamp, timeBuckets);
      if (bucket) {
        if (!bucket.feedbacks) bucket.feedbacks = [];
        bucket.feedbacks.push(f);
      }
    });

    // Calculate trend metrics
    const trendData = timeBuckets.map(bucket => {
      const bucketFeedbacks = bucket.feedbacks || [];
      const explicit = bucketFeedbacks.filter(f => f.type === 'explicit');
      
      return {
        period: bucket.label,
        count: bucketFeedbacks.length,
        explicitCount: explicit.length,
        implicitCount: bucketFeedbacks.filter(f => f.type === 'implicit').length,
        avgRating: explicit.length > 0 
          ? (explicit.reduce((sum, f) => sum + this.normalizeRating(f.rating), 0) / explicit.length).toFixed(2)
          : null,
        positiveRatio: bucketFeedbacks.length > 0
          ? (bucketFeedbacks.filter(f => {
              const sent = f.type === 'explicit' ? this.ratingToSentiment(f.rating) : f.inferredSentiment;
              return sent === 'positive';
            }).length / bucketFeedbacks.length).toFixed(2)
          : 0
      };
    });

    // Detect trend direction
    const trendDirection = this.detectTrendDirection(trendData);

    return {
      data: trendData,
      direction: trendDirection.direction,
      confidence: trendDirection.confidence,
      summary: {
        peakPeriod: trendData.reduce((max, curr) => curr.count > max.count ? curr : max, trendData[0]),
        lowestPeriod: trendData.reduce((min, curr) => curr.count < min.count ? curr : min, trendData[0])
      }
    };
  }

  /**
   * Analyze overall sentiment
   */
  analyzeSentiment(feedbacks) {
    const sentiments = {
      positive: 0,
      negative: 0,
      neutral: 0,
      unknown: 0
    };

    feedbacks.forEach(f => {
      let sentiment;
      if (f.type === 'explicit') {
        sentiment = this.ratingToSentiment(f.rating);
      } else {
        sentiment = f.inferredSentiment || 'unknown';
      }
      sentiments[sentiment]++;
    });

    const total = feedbacks.length;
    const dominant = Object.entries(sentiments).reduce((max, [sent, count]) => 
      count > max.count ? { sentiment: sent, count } : max
    , { sentiment: 'unknown', count: 0 });

    return {
      distribution: sentiments,
      percentages: {
        positive: Math.round((sentiments.positive / total) * 100),
        negative: Math.round((sentiments.negative / total) * 100),
        neutral: Math.round((sentiments.neutral / total) * 100),
        unknown: Math.round((sentiments.unknown / total) * 100)
      },
      dominant: dominant.sentiment,
      sentimentScore: ((sentiments.positive - sentiments.negative) / total).toFixed(2)
    };
  }

  /**
   * Analyze by categories
   */
  analyzeCategories(feedbacks) {
    const categories = {};

    feedbacks.forEach(f => {
      const cat = f.category || 'general';
      if (!categories[cat]) {
        categories[cat] = { count: 0, ratings: [], sentiments: [] };
      }
      categories[cat].count++;
      
      if (f.type === 'explicit' && f.rating) {
        categories[cat].ratings.push(this.normalizeRating(f.rating));
      }
      
      const sentiment = f.type === 'explicit' 
        ? this.ratingToSentiment(f.rating) 
        : f.inferredSentiment;
      categories[cat].sentiments.push(sentiment);
    });

    return Object.entries(categories).map(([name, data]) => ({
      name,
      count: data.count,
      avgRating: data.ratings.length > 0 
        ? (data.ratings.reduce((a, b) => a + b, 0) / data.ratings.length).toFixed(2)
        : null,
      sentimentDistribution: {
        positive: data.sentiments.filter(s => s === 'positive').length,
        negative: data.sentiments.filter(s => s === 'negative').length,
        neutral: data.sentiments.filter(s => s === 'neutral').length
      }
    })).sort((a, b) => b.count - a.count);
  }

  /**
   * Detect patterns in feedback
   */
  detectPatterns(feedbacks) {
    const patterns = [];

    // Pattern 1: Recurring issues
    const issues = feedbacks.filter(f => {
      if (f.type === 'explicit') {
        return this.normalizeRating(f.rating) <= 2;
      }
      return f.inferredSentiment === 'negative';
    });

    if (issues.length > 0) {
      const issueCategories = {};
      issues.forEach(f => {
        const cat = f.category || 'general';
        issueCategories[cat] = (issueCategories[cat] || 0) + 1;
      });
      
      const topIssues = Object.entries(issueCategories)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);
      
      if (topIssues.length > 0) {
        patterns.push({
          type: 'recurring_issues',
          description: 'Categories with most negative feedback',
          data: topIssues.map(([cat, count]) => ({ category: cat, count })),
          severity: issues.length > feedbacks.length * 0.3 ? 'high' : 'medium'
        });
      }
    }

    // Pattern 2: Time-based patterns
    const hourlyDistribution = {};
    feedbacks.forEach(f => {
      const hour = new Date(f.timestamp).getHours();
      hourlyDistribution[hour] = (hourlyDistribution[hour] || 0) + 1;
    });
    
    const peakHours = Object.entries(hourlyDistribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([hour, count]) => ({ hour: parseInt(hour), count }));
    
    patterns.push({
      type: 'time_patterns',
      description: 'Peak activity hours',
      data: peakHours,
      severity: 'info'
    });

    // Pattern 3: Rating volatility
    const explicitRatings = feedbacks
      .filter(f => f.type === 'explicit' && f.rating)
      .map(f => this.normalizeRating(f.rating));
    
    if (explicitRatings.length > 5) {
      const variance = this.calculateVariance(explicitRatings);
      if (variance > 2) {
        patterns.push({
          type: 'rating_volatility',
          description: 'High variance in ratings indicates inconsistent experience',
          data: { variance: variance.toFixed(2) },
          severity: 'medium'
        });
      }
    }

    // Pattern 4: Implicit signal patterns
    const implicitSignals = feedbacks.filter(f => f.type === 'implicit');
    if (implicitSignals.length > 0) {
      const signalCounts = {};
      implicitSignals.forEach(f => {
        signalCounts[f.signal] = (signalCounts[f.signal] || 0) + 1;
      });
      
      const topSignals = Object.entries(signalCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
      
      patterns.push({
        type: 'behavioral_patterns',
        description: 'Most common implicit user behaviors',
        data: topSignals.map(([signal, count]) => ({ signal, count })),
        severity: 'info'
      });
    }

    return patterns;
  }

  // Helper methods
  getCutoffDate(timeRange) {
    const now = new Date();
    switch (timeRange) {
      case 'day':
        return new Date(now - 24 * 60 * 60 * 1000);
      case 'week':
        return new Date(now - 7 * 24 * 60 * 60 * 1000);
      case 'month':
        return new Date(now - 30 * 24 * 60 * 60 * 1000);
      case 'all':
      default:
        return new Date(0);
    }
  }

  createTimeBuckets(timeRange) {
    const buckets = [];
    const now = new Date();
    
    switch (timeRange) {
      case 'day':
        for (let i = 23; i >= 0; i--) {
          const d = new Date(now - i * 60 * 60 * 1000);
          buckets.push({
            start: d,
            label: `${d.getHours()}:00`
          });
        }
        break;
      case 'week':
        for (let i = 6; i >= 0; i--) {
          const d = new Date(now - i * 24 * 60 * 60 * 1000);
          buckets.push({
            start: new Date(d.setHours(0, 0, 0, 0)),
            label: d.toLocaleDateString('zh-CN', { weekday: 'short', month: 'short', day: 'numeric' })
          });
        }
        break;
      case 'month':
        for (let i = 29; i >= 0; i--) {
          const d = new Date(now - i * 24 * 60 * 60 * 1000);
          buckets.push({
            start: new Date(d.setHours(0, 0, 0, 0)),
            label: `${d.getMonth() + 1}/${d.getDate()}`
          });
        }
        break;
      default:
        buckets.push({ start: new Date(0), label: 'all' });
    }
    
    return buckets;
  }

  getTimeBucket(timestamp, buckets) {
    const date = new Date(timestamp);
    for (let i = buckets.length - 1; i >= 0; i--) {
      if (date >= buckets[i].start) {
        return buckets[i];
      }
    }
    return buckets[0];
  }

  ratingToSentiment(rating) {
    const num = this.normalizeRating(rating);
    if (num >= 4) return 'positive';
    if (num <= 2) return 'negative';
    return 'neutral';
  }

  normalizeRating(rating) {
    if (typeof rating === 'number') return rating;
    if (rating === 'thumbs_up') return 5;
    if (rating === 'thumbs_down') return 1;
    const num = parseInt(rating);
    return isNaN(num) ? 3 : num;
  }

  calculateVariance(values) {
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    return values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
  }

  detectTrendDirection(trendData) {
    const counts = trendData.map(d => d.count);
    if (counts.length < 2) return { direction: 'stable', confidence: 0 };
    
    const firstHalf = counts.slice(0, Math.floor(counts.length / 2));
    const secondHalf = counts.slice(Math.floor(counts.length / 2));
    
    const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;
    
    const diff = secondAvg - firstAvg;
    const confidence = Math.min(Math.abs(diff) / firstAvg, 1);
    
    if (diff > firstAvg * 0.1) return { direction: 'increasing', confidence };
    if (diff < -firstAvg * 0.1) return { direction: 'decreasing', confidence };
    return { direction: 'stable', confidence: 1 - confidence };
  }

  /**
   * Get recent analyses
   */
  getRecentAnalyses(limit = 10) {
    return this.storage.getAllAnalyses().slice(-limit);
  }
}

module.exports = FeedbackAnalyzer;
