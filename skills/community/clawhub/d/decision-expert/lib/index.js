/**
 * Decision Expert Core Library
 * 
 * This library provides the core decision analysis functionality
 * that can be used both from CLI and programmatically.
 */

class Decision {
  constructor(description, options = []) {
    this.id = Date.now().toString(36) + Math.random().toString(36).substr(2);
    this.description = description;
    this.options = options.map(opt => (typeof opt === 'string' ? { name: opt } : opt));
    this.criteria = [];
    this.analysis = null;
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  addCriterion(name, weight = 1, description = '') {
    this.criteria.push({
      id: `crit_${Date.now()}_${Math.random().toString(36).substr(2)}`,
      name,
      weight,
      description,
      maxScore: 10 // Default max score for normalization
    });
    this.updatedAt = new Date();
    return this;
  }

  addOption(name, description = '') {
    this.options.push({
      id: `opt_${Date.now()}_${Math.random().toString(36).substr(2)}`,
      name,
      description
    });
    this.updatedAt = new Date();
    return this;
  }

  toJSON() {
    return {
      id: this.id,
      description: this.description,
      options: this.options,
      criteria: this.criteria,
      analysis: this.analysis,
      createdAt: this.createdAt.toISOString(),
      updatedAt: this.updatedAt.toISOString()
    };
  }
}

class DecisionEngine {
  constructor() {
    this.frameworks = {};
    this.registerDefaultFrameworks();
  }

  registerFramework(name, framework) {
    this.frameworks[name] = framework;
    return this;
  }

  registerDefaultFrameworks() {
    // Pros & Cons Framework
    this.registerFramework('pros-cons', {
      name: 'Pros & Cons',
      analyze: (decision, params = {}) => {
        const { pros = [], cons = [], weighted = false } = params;
        
        const analysis = {
          framework: 'pros-cons',
          pros: pros.map(pro => ({ text: pro, weight: 1 })),
          cons: cons.map(con => ({ text: con, weight: 1 })),
          summary: '',
          recommendation: ''
        };

        if (weighted) {
          // In weighted mode, allow assigning importance weights
          analysis.weighted = true;
        }

        const proCount = pros.length;
        const conCount = cons.length;
        
        if (proCount > conCount) {
          analysis.summary = `Pros outweigh cons (${proCount} vs ${conCount})`;
          analysis.recommendation = 'Consider proceeding with the decision';
        } else if (conCount > proCount) {
          analysis.summary = `Cons outweigh pros (${conCount} vs ${proCount})`;
          analysis.recommendation = 'Consider rejecting or modifying the decision';
        } else {
          analysis.summary = `Balanced (${proCount} pros vs ${conCount} cons)`;
          analysis.recommendation = 'Need additional analysis or tie-breaking criteria';
        }

        return analysis;
      }
    });

    // SWOT Framework
    this.registerFramework('swot', {
      name: 'SWOT Analysis',
      analyze: (decision, params = {}) => {
        const { strengths = [], weaknesses = [], opportunities = [], threats = [] } = params;
        
        return {
          framework: 'swot',
          quadrants: {
            strengths: strengths.map(s => ({ text: s, type: 'internal', impact: 'positive' })),
            weaknesses: weaknesses.map(w => ({ text: w, type: 'internal', impact: 'negative' })),
            opportunities: opportunities.map(o => ({ text: o, type: 'external', impact: 'positive' })),
            threats: threats.map(t => ({ text: t, type: 'external', impact: 'negative' }))
          },
          strategies: [],
          summary: `SWOT Analysis: ${strengths.length} strengths, ${weaknesses.length} weaknesses, ${opportunities.length} opportunities, ${threats.length} threats`
        };
      }
    });

    // Decision Matrix Framework
    this.registerFramework('matrix', {
      name: 'Decision Matrix',
      analyze: (decision, params = {}) => {
        const { criteriaWeights = [], optionScores = [] } = params;
        
        // Normalize weights to sum to 1
        const totalWeight = criteriaWeights.reduce((sum, w) => sum + w, 0);
        const normalizedWeights = criteriaWeights.map(w => w / totalWeight);
        
        // Calculate weighted scores for each option
        const optionsWithScores = decision.options.map((option, optionIndex) => {
          let totalScore = 0;
          const criterionScores = [];
          
          normalizedWeights.forEach((weight, critIndex) => {
            const score = optionScores[optionIndex]?.[critIndex] || 5; // Default score
            const weightedScore = score * weight;
            totalScore += weightedScore;
            criterionScores.push({
              criterion: decision.criteria[critIndex]?.name || `Criterion ${critIndex + 1}`,
              score,
              weight,
              weightedScore
            });
          });
          
          return {
            option: option.name,
            totalScore,
            criterionScores,
            rank: 0 // Will be set after all options are calculated
          };
        });
        
        // Rank options by total score
        optionsWithScores.sort((a, b) => b.totalScore - a.totalScore);
        optionsWithScores.forEach((option, index) => {
          option.rank = index + 1;
        });
        
        return {
          framework: 'decision-matrix',
          criteriaWeights: normalizedWeights,
          options: optionsWithScores,
          recommendation: optionsWithScores.length > 0 
            ? `Top recommendation: ${optionsWithScores[0].option} (score: ${optionsWithScores[0].totalScore.toFixed(2)})`
            : 'No options to evaluate'
        };
      }
    });
  }

  analyze(decision, frameworkName, params = {}) {
    const framework = this.frameworks[frameworkName];
    if (!framework) {
      throw new Error(`Framework '${frameworkName}' not found. Available: ${Object.keys(this.frameworks).join(', ')}`);
    }
    
    const analysis = framework.analyze(decision, params);
    decision.analysis = analysis;
    decision.updatedAt = new Date();
    
    return analysis;
  }

  getAvailableFrameworks() {
    return Object.keys(this.frameworks).map(name => ({
      name,
      displayName: this.frameworks[name].name
    }));
  }
}

// Utility functions
const utils = {
  /**
   * Parse comma-separated string into array
   */
  parseCSV: (str, defaultValue = []) => {
    if (!str || typeof str !== 'string') return defaultValue;
    return str.split(',').map(item => item.trim()).filter(item => item.length > 0);
  },

  /**
   * Parse comma-separated numbers into array
   */
  parseNumbers: (str, defaultValue = []) => {
    if (!str || typeof str !== 'string') return defaultValue;
    return str.split(',').map(item => parseFloat(item.trim())).filter(n => !isNaN(n));
  },

  /**
   * Normalize weights to sum to 1 (or 100%)
   */
  normalizeWeights: (weights, asPercentage = false) => {
    const total = weights.reduce((sum, w) => sum + w, 0);
    if (total === 0) return weights.map(() => 0);
    
    const normalized = weights.map(w => w / total);
    return asPercentage ? normalized.map(n => n * 100) : normalized;
  },

  /**
   * Format analysis results as markdown
   */
  toMarkdown: (decision, analysis) => {
    let markdown = `# Decision Analysis: ${decision.description}\n\n`;
    markdown += `**Created:** ${decision.createdAt.toLocaleString()}\n\n`;
    
    if (decision.options.length > 0) {
      markdown += '## Options\n\n';
      decision.options.forEach((opt, i) => {
        markdown += `${i + 1}. **${opt.name}**${opt.description ? ` - ${opt.description}` : ''}\n`;
      });
      markdown += '\n';
    }
    
    if (analysis) {
      markdown += `## Analysis (${analysis.framework})\n\n`;
      
      if (analysis.framework === 'pros-cons') {
        markdown += '### Pros\n\n';
        analysis.pros.forEach(pro => {
          markdown += `- ✓ ${pro.text}\n`;
        });
        
        markdown += '\n### Cons\n\n';
        analysis.cons.forEach(con => {
          markdown += `- ✗ ${con.text}\n`;
        });
        
        markdown += `\n**Summary:** ${analysis.summary}\n\n`;
        markdown += `**Recommendation:** ${analysis.recommendation}\n`;
      }
    }
    
    return markdown;
  },

  /**
   * Format analysis results as JSON
   */
  toJSON: (decision, analysis) => {
    return {
      decision: decision.toJSON(),
      analysis,
      exportedAt: new Date().toISOString()
    };
  }
};

// Export the main functionality
module.exports = {
  Decision,
  DecisionEngine,
  utils,
  
  // Convenience function to create and analyze a decision
  analyzeDecision: (description, options, framework = 'pros-cons', params = {}) => {
    const decision = new Decision(description, options);
    const engine = new DecisionEngine();
    return engine.analyze(decision, framework, params);
  }
};