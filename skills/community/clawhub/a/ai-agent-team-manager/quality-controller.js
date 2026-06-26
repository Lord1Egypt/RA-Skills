/**
 * AI Agent Team Manager - Quality Control Module
 * 
 * Implements comprehensive quality control for AI agent teams
 * Based on Otter Camp best practices and real-world experience
 */

class QualityController {
  constructor(config = {}) {
    this.config = {
      // Quality thresholds
      accuracyThreshold: config.accuracyThreshold || 0.95,
      completenessThreshold: config.completenessThreshold || 0.90,
      timelinessThreshold: config.timelinessThreshold || 0.85,
      
      // Review settings
      enablePeerReview: config.enablePeerReview !== false,
      enableHumanReview: config.enableHumanReview || false,
      reviewDepth: config.reviewDepth || 'comprehensive',
      
      // Performance metrics
      trackMetrics: config.trackMetrics !== false,
      performanceWindow: config.performanceWindow || 30, // days
      
      ...config
    };
    
    this.qualityStandards = this.loadQualityStandards();
    this.reviewCheckpoints = this.setupReviewCheckpoints();
  }

  /**
   * Load quality standards from configuration or defaults
   */
  loadQualityStandards() {
    return {
      // Output quality standards
      output: {
        accuracy: {
          description: "Factual accuracy and correctness",
          weight: 0.4,
          minScore: this.config.accuracyThreshold
        },
        completeness: {
          description: "Coverage of all required elements",
          weight: 0.3,
          minScore: this.config.completenessThreshold
        },
        clarity: {
          description: "Clear, concise, and well-structured",
          weight: 0.2,
          minScore: 0.8
        },
        relevance: {
          description: "Relevant to the original task",
          weight: 0.1,
          minScore: 0.9
        }
      },
      
      // Process quality standards
      process: {
        methodology: {
          description: "Sound methodology and approach",
          weight: 0.3,
          minScore: 0.85
        },
        documentation: {
          description: "Adequate documentation and reasoning",
          weight: 0.2,
          minScore: 0.8
        },
        efficiency: {
          description: "Resource and time efficiency",
          weight: 0.2,
          minScore: 0.75
        },
        compliance: {
          description: "Adherence to guidelines and constraints",
          weight: 0.3,
          minScore: 0.9
        }
      }
    };
  }

  /**
   * Setup automatic review checkpoints based on task complexity
   */
  setupReviewCheckpoints() {
    return {
      // Critical tasks: Full peer review + human review if enabled
      critical: {
        peerReview: true,
        humanReview: this.config.enableHumanReview,
        automatedChecks: ['accuracy', 'completeness', 'compliance']
      },
      
      // High priority tasks: Peer review + comprehensive automated checks
      high: {
        peerReview: true,
        humanReview: false,
        automatedChecks: ['accuracy', 'completeness', 'clarity', 'relevance']
      },
      
      // Medium priority tasks: Automated checks + spot peer review
      medium: {
        peerReview: 'spot', // Random selection for peer review
        humanReview: false,
        automatedChecks: ['accuracy', 'completeness']
      },
      
      // Low priority tasks: Basic automated checks only
      low: {
        peerReview: false,
        humanReview: false,
        automatedChecks: ['accuracy']
      }
    };
  }

  /**
   * Perform comprehensive quality assessment on agent output
   */
  async assessQuality(agentOutput, taskSpec, agentId) {
    const assessment = {
      taskId: taskSpec.id,
      agentId: agentId,
      timestamp: new Date().toISOString(),
      overallScore: 0,
      categoryScores: {},
      issues: [],
      recommendations: [],
      pass: false
    };

    // Assess output quality
    const outputAssessment = await this.assessOutputQuality(agentOutput, taskSpec);
    assessment.categoryScores.output = outputAssessment;
    
    // Assess process quality (if process logs available)
    if (taskSpec.processLogs) {
      const processAssessment = await this.assessProcessQuality(taskSpec.processLogs, taskSpec);
      assessment.categoryScores.process = processAssessment;
    }

    // Calculate overall score
    assessment.overallScore = this.calculateOverallScore(assessment.categoryScores);
    
    // Identify issues and recommendations
    assessment.issues = this.identifyIssues(assessment.categoryScores);
    assessment.recommendations = this.generateRecommendations(assessment.issues);
    
    // Determine if task passes quality threshold
    assessment.pass = assessment.overallScore >= this.config.accuracyThreshold;
    
    return assessment;
  }

  /**
   * Assess output quality against standards
   */
  async assessOutputQuality(output, taskSpec) {
    const scores = {};
    const weights = {};
    
    // Accuracy assessment
    scores.accuracy = await this.assessAccuracy(output, taskSpec);
    weights.accuracy = this.qualityStandards.output.accuracy.weight;
    
    // Completeness assessment  
    scores.completeness = await this.assessCompleteness(output, taskSpec);
    weights.completeness = this.qualityStandards.output.completeness.weight;
    
    // Clarity assessment
    scores.clarity = await this.assessClarity(output);
    weights.clarity = this.qualityStandards.output.clarity.weight;
    
    // Relevance assessment
    scores.relevance = await this.assessRelevance(output, taskSpec);
    weights.relevance = this.qualityStandards.output.relevance.weight;
    
    return {
      scores,
      weights,
      weightedAverage: this.calculateWeightedAverage(scores, weights)
    };
  }

  /**
   * Assess process quality from logs
   */
  async assessProcessQuality(processLogs, taskSpec) {
    const scores = {};
    const weights = {};
    
    // Methodology assessment
    scores.methodology = await this.assessMethodology(processLogs, taskSpec);
    weights.methodology = this.qualityStandards.process.methodology.weight;
    
    // Documentation assessment
    scores.documentation = await this.assessDocumentation(processLogs);
    weights.documentation = this.qualityStandards.process.documentation.weight;
    
    // Efficiency assessment
    scores.efficiency = await this.assessEfficiency(processLogs);
    weights.efficiency = this.qualityStandards.process.efficiency.weight;
    
    // Compliance assessment
    scores.compliance = await this.assessCompliance(processLogs, taskSpec);
    weights.compliance = this.qualityStandards.process.compliance.weight;
    
    return {
      scores,
      weights,
      weightedAverage: this.calculateWeightedAverage(scores, weights)
    };
  }

  /**
   * Assess factual accuracy of output
   */
  async assessAccuracy(output, taskSpec) {
    // Implementation would use fact-checking APIs, knowledge bases, etc.
    // For now, using heuristic assessment
    
    let score = 1.0;
    const issues = [];
    
    // Check for obvious hallucinations or contradictions
    if (this.containsHallucinations(output, taskSpec)) {
      score -= 0.3;
      issues.push('Potential hallucinations detected');
    }
    
    // Check for consistency with provided context
    if (!this.isConsistentWithContext(output, taskSpec.context)) {
      score -= 0.2;
      issues.push('Inconsistent with provided context');
    }
    
    // Check for logical errors
    if (this.containsLogicalErrors(output)) {
      score -= 0.15;
      issues.push('Logical inconsistencies detected');
    }
    
    // Ensure score doesn't go below 0
    score = Math.max(0, score);
    
    return {
      score,
      maxScore: 1.0,
      issues,
      confidence: this.calculateConfidence(issues.length)
    };
  }

  /**
   * Assess completeness of output
   */
  async assessCompleteness(output, taskSpec) {
    const requiredElements = taskSpec.requiredElements || [];
    let completeness = 1.0;
    const missingElements = [];
    
    for (const element of requiredElements) {
      if (!this.containsElement(output, element)) {
        completeness -= 1.0 / requiredElements.length;
        missingElements.push(element);
      }
    }
    
    return {
      score: Math.max(0, completeness),
      maxScore: 1.0,
      missingElements,
      coverage: requiredElements.length > 0 ? 
        (requiredElements.length - missingElements.length) / requiredElements.length : 1.0
    };
  }

  /**
   * Assess clarity and structure
   */
  async assessClarity(output) {
    // Assess readability, structure, and coherence
    const readabilityScore = this.calculateReadability(output);
    const structureScore = this.assessStructure(output);
    const coherenceScore = this.assessCoherence(output);
    
    const clarity = (readabilityScore + structureScore + coherenceScore) / 3;
    
    return {
      score: clarity,
      maxScore: 1.0,
      readability: readabilityScore,
      structure: structureScore,
      coherence: coherenceScore
    };
  }

  /**
   * Assess relevance to original task
   */
  async assessRelevance(output, taskSpec) {
    const taskKeywords = this.extractKeywords(taskSpec.description);
    const outputKeywords = this.extractKeywords(output);
    
    const relevance = this.calculateKeywordOverlap(taskKeywords, outputKeywords);
    
    return {
      score: relevance,
      maxScore: 1.0,
      keywordMatch: relevance,
      offTopicPenalty: this.calculateOffTopicPenalty(output, taskSpec)
    };
  }

  /**
   * Assess methodology quality from process logs
   */
  async assessMethodology(processLogs, taskSpec) {
    // Check if agent followed appropriate methodology
    const methodology = processLogs.methodology || 'unknown';
    const expectedMethodology = taskSpec.expectedMethodology || 'flexible';
    
    if (expectedMethodology === 'flexible') {
      return { score: 0.9, maxScore: 1.0, notes: 'Flexible methodology accepted' };
    }
    
    const matchScore = this.calculateMethodologyMatch(methodology, expectedMethodology);
    
    return {
      score: matchScore,
      maxScore: 1.0,
      methodologyUsed: methodology,
      methodologyExpected: expectedMethodology
    };
  }

  /**
   * Assess documentation quality
   */
  async assessDocumentation(processLogs) {
    const hasReasoning = !!processLogs.reasoning;
    const hasSteps = !!processLogs.steps;
    const hasSources = !!processLogs.sources;
    
    let documentationScore = 0;
    if (hasReasoning) documentationScore += 0.4;
    if (hasSteps) documentationScore += 0.3;
    if (hasSources) documentationScore += 0.3;
    
    return {
      score: documentationScore,
      maxScore: 1.0,
      hasReasoning,
      hasSteps,
      hasSources
    };
  }

  /**
   * Assess efficiency from process logs
   */
  async assessEfficiency(processLogs) {
    const executionTime = processLogs.executionTime || 0;
    const tokenUsage = processLogs.tokenUsage || 0;
    const toolCalls = processLogs.toolCalls || 0;
    
    // Normalize against task complexity
    const complexity = processLogs.taskComplexity || 1;
    const timeEfficiency = Math.max(0, 1 - (executionTime / (complexity * 300))); // 5 minutes per complexity unit
    const resourceEfficiency = Math.max(0, 1 - (tokenUsage / (complexity * 10000))); // 10k tokens per complexity unit
    const toolEfficiency = Math.max(0, 1 - (toolCalls / (complexity * 10))); // 10 tool calls per complexity unit
    
    const efficiency = (timeEfficiency + resourceEfficiency + toolEfficiency) / 3;
    
    return {
      score: efficiency,
      maxScore: 1.0,
      timeEfficiency,
      resourceEfficiency,
      toolEfficiency,
      executionTime,
      tokenUsage,
      toolCalls
    };
  }

  /**
   * Assess compliance with guidelines
   */
  async assessCompliance(processLogs, taskSpec) {
    const guidelines = taskSpec.guidelines || [];
    let compliance = 1.0;
    const violations = [];
    
    for (const guideline of guidelines) {
      if (!this.compliesWithGuideline(processLogs, guideline)) {
        compliance -= 1.0 / guidelines.length;
        violations.push(guideline);
      }
    }
    
    return {
      score: Math.max(0, compliance),
      maxScore: 1.0,
      violations,
      complianceRate: guidelines.length > 0 ? 
        (guidelines.length - violations.length) / guidelines.length : 1.0
    };
  }

  /**
   * Calculate overall quality score
   */
  calculateOverallScore(categoryScores) {
    if (!categoryScores.output) return 0;
    
    let totalScore = 0;
    let totalWeight = 0;
    
    // Output quality (70% weight)
    totalScore += categoryScores.output.weightedAverage * 0.7;
    totalWeight += 0.7;
    
    // Process quality (30% weight) if available
    if (categoryScores.process) {
      totalScore += categoryScores.process.weightedAverage * 0.3;
      totalWeight += 0.3;
    }
    
    return totalWeight > 0 ? totalScore / totalWeight : 0;
  }

  /**
   * Calculate weighted average of scores
   */
  calculateWeightedAverage(scores, weights) {
    let total = 0;
    let weightSum = 0;
    
    for (const [key, score] of Object.entries(scores)) {
      const weight = weights[key] || 0;
      total += score * weight;
      weightSum += weight;
    }
    
    return weightSum > 0 ? total / weightSum : 0;
  }

  /**
   * Identify quality issues from assessment
   */
  identifyIssues(categoryScores) {
    const issues = [];
    
    if (categoryScores.output) {
      const output = categoryScores.output.scores;
      const standards = this.qualityStandards.output;
      
      if (output.accuracy < standards.accuracy.minScore) {
        issues.push({
          category: 'accuracy',
          severity: 'high',
          description: `Accuracy below threshold (${output.accuracy.toFixed(2)} < ${standards.accuracy.minScore})`
        });
      }
      
      if (output.completeness < standards.completeness.minScore) {
        issues.push({
          category: 'completeness', 
          severity: 'medium',
          description: `Completeness below threshold (${output.completeness.toFixed(2)} < ${standards.completeness.minScore})`
        });
      }
      
      if (output.clarity < standards.clarity.minScore) {
        issues.push({
          category: 'clarity',
          severity: 'low',
          description: `Clarity below threshold (${output.clarity.toFixed(2)} < ${standards.clarity.minScore})`
        });
      }
    }
    
    if (categoryScores.process) {
      const process = categoryScores.process.scores;
      const standards = this.qualityStandards.process;
      
      if (process.compliance < standards.compliance.minScore) {
        issues.push({
          category: 'compliance',
          severity: 'high',
          description: `Compliance below threshold (${process.compliance.toFixed(2)} < ${standards.compliance.minScore})`
        });
      }
    }
    
    return issues;
  }

  /**
   * Generate recommendations based on identified issues
   */
  generateRecommendations(issues) {
    const recommendations = [];
    
    const issueMap = {
      accuracy: 'Review fact-checking procedures and verify sources',
      completeness: 'Ensure all required elements are addressed in output',
      clarity: 'Improve structure and readability of responses',
      compliance: 'Strictly adhere to provided guidelines and constraints'
    };
    
    for (const issue of issues) {
      recommendations.push({
        issue: issue.category,
        recommendation: issueMap[issue.category] || 'General quality improvement needed',
        priority: issue.severity
      });
    }
    
    return recommendations;
  }

  /**
   * Determine if peer review is needed based on task priority
   */
  needsPeerReview(taskPriority) {
    const checkpoint = this.reviewCheckpoints[taskPriority] || this.reviewCheckpoints.medium;
    return checkpoint.peerReview;
  }

  /**
   * Determine if human review is needed
   */
  needsHumanReview(taskPriority) {
    const checkpoint = this.reviewCheckpoints[taskPriority] || this.reviewCheckpoints.medium;
    return checkpoint.humanReview;
  }

  /**
   * Get required automated checks for task priority
   */
  getRequiredAutomatedChecks(taskPriority) {
    const checkpoint = this.reviewCheckpoints[taskPriority] || this.reviewCheckpoints.medium;
    return checkpoint.automatedChecks;
  }

  // Helper methods (simplified implementations)
  containsHallucinations(output, taskSpec) {
    // Simplified check - in reality would use more sophisticated methods
    return output.toLowerCase().includes('i made up') || 
           output.toLowerCase().includes('fictional') ||
           this.hasInconsistentClaims(output);
  }
  
  isConsistentWithContext(output, context) {
    if (!context) return true;
    // Check if output contradicts context
    return !this.hasContradictions(output, context);
  }
  
  containsLogicalErrors(output) {
    // Simplified logic error detection
    return this.hasInternalContradictions(output);
  }
  
  containsElement(output, element) {
    return output.toLowerCase().includes(element.toLowerCase());
  }
  
  calculateReadability(output) {
    // Simplified readability calculation
    const words = output.split(/\s+/).length;
    const sentences = output.split(/[.!?]+/).length;
    const avgWordsPerSentence = words / Math.max(1, sentences);
    // Prefer 10-20 words per sentence
    if (avgWordsPerSentence >= 10 && avgWordsPerSentence <= 20) return 0.9;
    if (avgWordsPerSentence >= 5 && avgWordsPerSentence <= 25) return 0.7;
    return 0.5;
  }
  
  assessStructure(output) {
    // Check for clear structure (headings, paragraphs, lists)
    const hasHeadings = /[#*].+\n/.test(output);
    const hasParagraphs = output.split('\n\n').length > 2;
    const hasLists = /[-*]\s/.test(output) || /\d+\.\s/.test(output);
    
    let score = 0.3; // Base score
    if (hasHeadings) score += 0.3;
    if (hasParagraphs) score += 0.2;  
    if (hasLists) score += 0.2;
    
    return Math.min(1.0, score);
  }
  
  assessCoherence(output) {
    // Check for logical flow and transitions
    const transitionWords = ['however', 'therefore', 'furthermore', 'consequently', 'meanwhile'];
    const hasTransitions = transitionWords.some(word => 
      output.toLowerCase().includes(word)
    );
    
    return hasTransitions ? 0.8 : 0.6;
  }
  
  extractKeywords(text) {
    // Simple keyword extraction
    const words = text.toLowerCase().match(/\b\w{3,}\b/g) || [];
    const commonWords = new Set(['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'way', 'will', 'too']);
    return words.filter(word => !commonWords.has(word));
  }
  
  calculateKeywordOverlap(keywords1, keywords2) {
    if (keywords1.length === 0 || keywords2.length === 0) return 0;
    const set1 = new Set(keywords1);
    const set2 = new Set(keywords2);
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    return intersection.size / Math.max(set1.size, set2.size);
  }
  
  calculateOffTopicPenalty(output, taskSpec) {
    // Simplified off-topic detection
    const taskWords = this.extractKeywords(taskSpec.description);
    const outputWords = this.extractKeywords(output);
    const overlap = this.calculateKeywordOverlap(taskWords, outputWords);
    return Math.max(0, 1 - overlap);
  }
  
  calculateMethodologyMatch(actual, expected) {
    // Simplified methodology matching
    return actual.toLowerCase() === expected.toLowerCase() ? 1.0 : 0.5;
  }
  
  compliesWithGuideline(processLogs, guideline) {
    // Simplified compliance check
    return processLogs.guidelinesFollowed?.includes(guideline) || 
           !processLogs.guidelinesViolated?.includes(guideline);
  }
  
  hasInconsistentClaims(output) {
    // Very simplified inconsistency detection
    return false; // Would need more sophisticated NLP in reality
  }
  
  hasContradictions(output, context) {
    return false; // Would need more sophisticated NLP in reality  
  }
  
  hasInternalContradictions(output) {
    return false; // Would need more sophisticated NLP in reality
  }
  
  calculateConfidence(issueCount) {
    if (issueCount === 0) return 0.95;
    if (issueCount === 1) return 0.85;
    if (issueCount === 2) return 0.75;
    return 0.6;
  }
}

module.exports = QualityController;