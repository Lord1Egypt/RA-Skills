/**
 * Decision Advisor - Tree of Thoughts for Decision Making
 */

class DecisionAdvisor {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async advise(options) {
    const {
      decision,
      options: optionList,
      criteria = [],
      context = ''
    } = options;

    if (this.verbose) {
      console.log(`🎯 Decision: ${decision}`);
      console.log(`   Options: ${optionList.join(', ')}`);
      console.log(`   Criteria: ${criteria.length}`);
      console.log();
    }

    // Phase 1: Generate/expand options
    const expandedOptions = await this.generateOptions(decision, optionList, context);

    if (this.verbose) {
      console.log(`💡 Generated ${expandedOptions.length} options\n`);
    }

    // Phase 2: Define/refine criteria
    const refinedCriteria = await this.defineCriteria(decision, criteria);

    if (this.verbose) {
      console.log(`📊 ${refinedCriteria.length} decision criteria\n`);
    }

    // Phase 3: Evaluate options
    const evaluations = await this.evaluateOptions(decision, expandedOptions, refinedCriteria, context);

    if (this.verbose) {
      console.log('⚖️  Evaluation complete\n');
    }

    // Phase 4: Generate recommendation
    const recommendation = this.generateRecommendation(expandedOptions, refinedCriteria, evaluations);

    if (this.verbose) {
      console.log('✅ Recommendation generated\n');
    }

    return recommendation;
  }

  async generateOptions(decision, initialOptions, context) {
    const prompt = `Decision: ${decision}

Initial options: ${initialOptions.join(', ')}

Context: ${context}

Generate additional options to consider. Include creative alternatives that might not be obvious.

Return as JSON array:
["option 1", "option 2", "option 3"]`;

    try {
      const response = await this.llm.generate(prompt);
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        const additional = JSON.parse(jsonMatch[0]);
        return [...initialOptions, ...additional];
      }
    } catch (e) {}

    return initialOptions;
  }

  async defineCriteria(decision, initialCriteria) {
    if (initialCriteria.length > 0) {
      return initialCriteria;
    }

    const prompt = `For the decision: ${decision}

What criteria should be considered?

Return as JSON array:
[
  {"name": "Criterion 1", "weight": 0.3},
  {"name": "Criterion 2", "weight": 0.2}
]

Weights should sum to 1.0`;

    try {
      const response = await this.llm.generate(prompt);
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch (e) {}

    // Default criteria
    return [
      { name: 'Cost', weight: 0.3 },
      { name: 'Benefits', weight: 0.3 },
      { name: 'Risk', weight: 0.2 },
      { name: 'Feasibility', weight: 0.2 }
    ];
  }

  async evaluateOptions(decision, options, criteria, context) {
    const evaluations = [];

    for (const option of options) {
      const scores = {};
      let totalScore = 0;

      for (const criterion of criteria) {
        const score = await this.scoreOption(decision, option, criterion, context);
        scores[criterion.name] = score;
        totalScore += score * criterion.weight;
      }

      evaluations.push({
        option,
        scores,
        totalScore: parseFloat(totalScore.toFixed(2))
      });
    }

    return evaluations.sort((a, b) => b.totalScore - a.totalScore);
  }

  async scoreOption(decision, option, criterion, context) {
    const prompt = `Rate option "${option}" for decision: ${decision}

Criterion: ${criterion.name}
Context: ${context}

Rate from 1-10 (10 is best):`;

    const response = await this.llm.generate(prompt);
    const score = parseFloat(response.match(/\d+(\.\d+)?/)?.[0] || '5');
    return Math.min(10, Math.max(1, score));
  }

  generateRecommendation(options, criteria, evaluations) {
    const best = evaluations[0];
    const second = evaluations[1];

    const analysis = this.buildAnalysisTable(options, criteria, evaluations);
    const reasons = this.generateReasons(best, criteria);
    const risks = this.identifyRisks(best);

    return {
      recommendation: best.option,
      score: best.totalScore,
      confidence: this.calculateConfidence(best, second),
      analysis,
      reasons,
      risks,
      alternatives: evaluations.slice(1, 3).map(e => e.option),
      fullRanking: evaluations
    };
  }

  buildAnalysisTable(options, criteria, evaluations) {
    let table = '| Criteria | Weight |';
    options.forEach(opt => {
      table += ` ${opt.substring(0, 10)} |`;
    });
    table += '\n|' + '-'.repeat(10) + '|';
    criteria.forEach(c => {
      table += ` ${c.weight.toFixed(2)} |`;
    });
    table += '\n';

    criteria.forEach(criterion => {
      table += `| ${criterion.name} | ${criterion.weight.toFixed(2)} |`;
      evaluations.forEach(eval_ => {
        table += ` ${eval_.scores[criterion.name].toFixed(1)} |`;
      });
      table += '\n';
    });

    table += '| **Total** | |';
    evaluations.forEach(eval_ => {
      table += ` **${eval_.totalScore.toFixed(2)}** |`;
    });

    return table;
  }

  generateReasons(best, criteria) {
    return [
      `Highest overall score (${best.totalScore}/10)`,
      `Strong performance across ${criteria.length} criteria`,
      'Best balance of trade-offs'
    ];
  }

  identifyRisks(best) {
    return [
      'Consider implementation complexity',
      'Evaluate long-term maintenance costs',
      'Assess team learning curve'
    ];
  }

  calculateConfidence(best, second) {
    const margin = best.totalScore - (second ? second.totalScore : 0);
    if (margin > 2) return 'High (90%)';
    if (margin > 1) return 'Medium-High (75%)';
    if (margin > 0.5) return 'Medium (60%)';
    return 'Low (50%)';
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return '5';
    }
  };
}

module.exports = { DecisionAdvisor };
