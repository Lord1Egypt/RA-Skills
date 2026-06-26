/**
 * Improvement Suggester - Generates actionable improvement suggestions
 */
const Storage = require('./storage');
const FeedbackAnalyzer = require('./analyzer');

class ImprovementSuggester {
  constructor() {
    this.storage = new Storage();
    this.analyzer = new FeedbackAnalyzer();
  }

  /**
   * Generate improvement suggestions based on feedback analysis
   * @param {Object} options - Generation options
   * @param {string} options.focusArea - Specific area to focus on (optional)
   * @param {number} options.maxSuggestions - Maximum suggestions to generate
   */
  generate(options = {}) {
    const focusArea = options.focusArea;
    const maxSuggestions = options.maxSuggestions || 5;

    // Get latest analysis
    const analyses = this.storage.getAllAnalyses();
    const latestAnalysis = analyses[analyses.length - 1];

    if (!latestAnalysis) {
      // Run analysis first if none exists
      const analysisResult = this.analyzer.analyze({ timeRange: 'week' });
      if (!analysisResult.analysis) {
        return {
          success: false,
          message: 'No feedback data available for suggestion generation'
        };
      }
    }

    const analysis = latestAnalysis || this.analyzer.analyze({ timeRange: 'week' }).analysis;
    const suggestions = [];

    // Generate suggestions based on patterns
    if (analysis.patterns) {
      analysis.patterns.forEach(pattern => {
        const patternSuggestions = this.suggestFromPattern(pattern, focusArea);
        suggestions.push(...patternSuggestions);
      });
    }

    // Generate suggestions based on sentiment
    if (analysis.sentiment) {
      const sentimentSuggestions = this.suggestFromSentiment(analysis.sentiment, focusArea);
      suggestions.push(...sentimentSuggestions);
    }

    // Generate suggestions based on categories
    if (analysis.categories) {
      const categorySuggestions = this.suggestFromCategories(analysis.categories, focusArea);
      suggestions.push(...categorySuggestions);
    }

    // Generate suggestions based on trends
    if (analysis.trends) {
      const trendSuggestions = this.suggestFromTrends(analysis.trends, focusArea);
      suggestions.push(...trendSuggestions);
    }

    // Deduplicate and prioritize
    const uniqueSuggestions = this.deduplicateSuggestions(suggestions);
    const prioritizedSuggestions = this.prioritizeSuggestions(uniqueSuggestions);
    const finalSuggestions = prioritizedSuggestions.slice(0, maxSuggestions);

    // Save suggestions
    finalSuggestions.forEach(suggestion => {
      this.storage.saveSuggestion(suggestion);
    });

    return {
      success: true,
      message: `Generated ${finalSuggestions.length} improvement suggestions`,
      suggestions: finalSuggestions
    };
  }

  /**
   * Generate suggestions from detected patterns
   */
  suggestFromPattern(pattern, focusArea) {
    const suggestions = [];

    switch (pattern.type) {
      case 'recurring_issues':
        if (pattern.data && pattern.data.length > 0) {
          const topIssue = pattern.data[0];
          if (!focusArea || topIssue.category === focusArea) {
            suggestions.push({
              title: `Address recurring issues in ${topIssue.category}`,
              description: `${topIssue.count} negative feedback items identified in this category. Review and improve related functionality.`,
              category: topIssue.category,
              priority: pattern.severity === 'high' ? 'high' : 'medium',
              actionItems: [
                `Analyze ${topIssue.category} related interactions`,
                'Identify root causes of negative feedback',
                'Implement targeted improvements',
                'Monitor feedback for this category'
              ],
              expectedImpact: 'Reduce negative feedback and improve user satisfaction',
              sourcePattern: pattern.type
            });
          }
        }
        break;

      case 'rating_volatility':
        suggestions.push({
          title: 'Improve consistency of responses',
          description: 'High variance in ratings suggests inconsistent user experience. Standardize quality across interactions.',
          category: 'quality',
          priority: 'high',
          actionItems: [
            'Review edge cases causing poor responses',
            'Implement quality checks',
            'Create response templates for common scenarios',
            'Add consistency validation'
          ],
          expectedImpact: 'More predictable and reliable user experience',
          sourcePattern: pattern.type
        });
        break;

      case 'behavioral_patterns':
        const negativeSignals = pattern.data.filter(d => 
          ['abandon', 'retry', 'correction', 'timeout'].some(s => d.signal.includes(s))
        );
        
        if (negativeSignals.length > 0) {
          const topSignal = negativeSignals[0];
          suggestions.push({
            title: `Address ${topSignal.signal} behavior`,
            description: `${topSignal.count} instances of ${topSignal.signal} detected. Users may be struggling with this aspect.`,
            category: 'usability',
            priority: 'medium',
            actionItems: [
              `Investigate causes of ${topSignal.signal}`,
              'Simplify related workflows',
              'Add helpful guidance or hints',
              'Test improvements with users'
            ],
            expectedImpact: 'Reduced friction and improved completion rates',
            sourcePattern: pattern.type
          });
        }
        break;
    }

    return suggestions;
  }

  /**
   * Generate suggestions from sentiment analysis
   */
  suggestFromSentiment(sentiment, focusArea) {
    const suggestions = [];

    if (sentiment.percentages.negative > 20) {
      suggestions.push({
        title: 'Reduce negative feedback through proactive improvements',
        description: `${sentiment.percentages.negative}% of feedback is negative. Focus on addressing common pain points.`,
        category: 'general',
        priority: 'high',
        actionItems: [
          'Review all negative feedback comments',
          'Identify top 3 pain points',
          'Create improvement plan',
          'Set up monitoring for negative trends'
        ],
        expectedImpact: 'Increase overall satisfaction score',
        sourcePattern: 'sentiment_analysis'
      });
    }

    if (sentiment.sentimentScore < 0) {
      suggestions.push({
        title: 'Improve overall sentiment score',
        description: `Current sentiment score is ${sentiment.sentimentScore}. Aim for positive net sentiment through targeted improvements.`,
        category: 'general',
        priority: 'high',
        actionItems: [
          'Analyze factors contributing to negative sentiment',
          'Implement quick wins for immediate improvement',
          'Plan longer-term enhancements',
          'Track sentiment score weekly'
        ],
        expectedImpact: 'Positive user perception and engagement',
        sourcePattern: 'sentiment_analysis'
      });
    }

    return suggestions;
  }

  /**
   * Generate suggestions from category analysis
   */
  suggestFromCategories(categories, focusArea) {
    const suggestions = [];

    categories.forEach(cat => {
      if (focusArea && cat.name !== focusArea) return;

      if (cat.avgRating && parseFloat(cat.avgRating) < 3) {
        suggestions.push({
          title: `Improve ${cat.name} category performance`,
          description: `Average rating of ${cat.avgRating} in ${cat.name} indicates room for improvement.`,
          category: cat.name,
          priority: 'high',
          actionItems: [
            `Deep dive into ${cat.name} feedback`,
            'Identify specific shortcomings',
            'Benchmark against best practices',
            'Implement targeted fixes'
          ],
          expectedImpact: `Raise ${cat.name} rating above 4.0`,
          sourcePattern: 'category_analysis'
        });
      }

      if (cat.sentimentDistribution.negative > cat.count * 0.3) {
        suggestions.push({
          title: `Address negative sentiment in ${cat.name}`,
          description: `${cat.sentimentDistribution.negative} negative responses in ${cat.name} category need attention.`,
          category: cat.name,
          priority: 'medium',
          actionItems: [
            'Categorize negative feedback by type',
            'Prioritize by frequency and impact',
            'Develop mitigation strategies',
            'Test improvements'
          ],
          expectedImpact: 'Balanced sentiment distribution',
          sourcePattern: 'category_analysis'
        });
      }
    });

    return suggestions;
  }

  /**
   * Generate suggestions from trend analysis
   */
  suggestFromTrends(trends, focusArea) {
    const suggestions = [];

    if (trends.direction === 'decreasing' && trends.confidence > 0.5) {
      suggestions.push({
        title: 'Reverse declining feedback trend',
        description: 'Feedback volume is decreasing, which may indicate reduced engagement or satisfaction.',
        category: 'engagement',
        priority: 'high',
        actionItems: [
          'Investigate reasons for declining engagement',
          'Reach out to users for qualitative feedback',
          'Implement re-engagement strategies',
          'Monitor trend reversal'
        ],
        expectedImpact: 'Restored user engagement and feedback volume',
        sourcePattern: 'trend_analysis'
      });
    }

    // Check for rating decline
    const ratings = trends.data.filter(d => d.avgRating).map(d => parseFloat(d.avgRating));
    if (ratings.length >= 3) {
      const recent = ratings.slice(-3);
      const earlier = ratings.slice(0, -3);
      const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
      const earlierAvg = earlier.reduce((a, b) => a + b, 0) / earlier.length;
      
      if (recentAvg < earlierAvg - 0.5) {
        suggestions.push({
          title: 'Address declining quality ratings',
          description: `Average rating dropped from ${earlierAvg.toFixed(2)} to ${recentAvg.toFixed(2)}. Immediate attention needed.`,
          category: 'quality',
          priority: 'high',
          actionItems: [
            'Identify when decline started',
            'Review changes made during that period',
            'Rollback or fix problematic changes',
            'Implement quality monitoring'
          ],
          expectedImpact: 'Restore previous rating levels',
          sourcePattern: 'trend_analysis'
        });
      }
    }

    return suggestions;
  }

  /**
   * Deduplicate suggestions by title similarity
   */
  deduplicateSuggestions(suggestions) {
    const seen = new Set();
    return suggestions.filter(s => {
      const key = s.title.toLowerCase().replace(/\s+/g, '');
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * Prioritize suggestions by priority and impact
   */
  prioritizeSuggestions(suggestions) {
    const priorityOrder = { high: 3, medium: 2, low: 1 };
    
    return suggestions.sort((a, b) => {
      const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];
      if (priorityDiff !== 0) return priorityDiff;
      
      // Secondary sort by category importance
      const categories = ['quality', 'usability', 'performance', 'general'];
      return categories.indexOf(a.category) - categories.indexOf(b.category);
    });
  }

  /**
   * Get all suggestions with optional filtering
   */
  getSuggestions(filters = {}) {
    let suggestions = this.storage.getAllSuggestions();

    if (filters.status) {
      suggestions = suggestions.filter(s => s.status === filters.status);
    }
    if (filters.category) {
      suggestions = suggestions.filter(s => s.category === filters.category);
    }
    if (filters.priority) {
      suggestions = suggestions.filter(s => s.priority === filters.priority);
    }
    if (filters.limit) {
      suggestions = suggestions.slice(-filters.limit);
    }

    return suggestions;
  }

  /**
   * Update suggestion status
   */
  updateStatus(id, status, note) {
    const result = this.storage.updateSuggestionStatus(id, status, note);
    return {
      success: result,
      message: result ? 'Status updated' : 'Suggestion not found'
    };
  }

  /**
   * Get suggestion by ID
   */
  getSuggestion(id) {
    const suggestions = this.storage.getAllSuggestions();
    return suggestions.find(s => s.id === id);
  }
}

module.exports = ImprovementSuggester;
