/**
 * Research Assistant - ReAct + Plan-and-Solve
 */

class ResearchAssistant {
  constructor(options = {}) {
    this.depth = options.depth || 'standard';
    this.maxSources = options.maxSources || 10;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async research(options) {
    const { topic, depth = this.depth, sources = this.maxSources } = options;

    if (this.verbose) {
      console.log(`🔬 Starting research: ${topic}`);
      console.log(`   Depth: ${depth}`);
      console.log(`   Target sources: ${sources}\n`);
    }

    // Phase 1: Plan research
    const plan = await this.createPlan(topic, depth);

    if (this.verbose) {
      console.log('📋 Research plan created\n');
    }

    // Phase 2: Execute research (ReAct loops)
    const searchResults = await this.executeSearch(topic, plan);

    if (this.verbose) {
      console.log(`📚 Collected ${searchResults.length} sources\n`);
    }

    // Phase 3: Analyze and synthesize
    const analysis = await this.analyze(topic, searchResults);

    if (this.verbose) {
      console.log('📊 Analysis complete\n');
    }

    // Phase 4: Generate report
    const report = await this.generateReport(topic, analysis, searchResults);

    if (this.verbose) {
      console.log('✅ Research complete\n');
    }

    return report;
  }

  async createPlan(topic, depth) {
    const prompt = `Create a research plan for: ${topic}

Depth: ${depth}

Include:
1. Key research questions
2. Search terms and queries
3. Types of sources to look for
4. Analysis framework

Return structured plan.`;

    return await this.llm.generate(prompt);
  }

  async executeSearch(topic, plan) {
    // Simulated search results (in production, use actual search API)
    const results = [];
    
    for (let i = 0; i < this.maxSources; i++) {
      results.push({
        title: `Source ${i + 1}: Research on ${topic}`,
        url: `https://example.com/source-${i + 1}`,
        summary: `Key findings from source ${i + 1}...`,
        credibility: Math.random() > 0.3 ? 'high' : 'medium'
      });
    }

    return results;
  }

  async analyze(topic, sources) {
    const prompt = `Analyze these sources about: ${topic}

Sources:
${sources.map(s => `- ${s.title}: ${s.summary}`).join('\n')}

Provide:
1. Key findings
2. Consensus points
3. Conflicting information
4. Trends and patterns
5. Gaps in research`;

    return await this.llm.generate(prompt);
  }

  async generateReport(topic, analysis, sources) {
    const prompt = `Generate a comprehensive research report:

Topic: ${topic}

Analysis:
${analysis}

Sources:
${sources.map(s => `${s.title} - ${s.url}`).join('\n')}

Structure:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Methodology
5. Citations
6. Recommendations`;

    const content = await this.llm.generate(prompt);

    return {
      title: topic,
      summary: this.extractSection(content, 'executive summary'),
      findings: this.extractSection(content, 'key findings'),
      analysis: content,
      citations: sources.map(s => ({
        title: s.title,
        url: s.url,
        credibility: s.credibility
      })),
      sources: sources.length,
      content
    };
  }

  extractSection(content, sectionName) {
    const regex = new RegExp(`${sectionName}[:\\s]+([\\s\\S]+?)(?:\\n\\n[0-9]|$)`, 'i');
    const match = content.match(regex);
    return match ? match[1].trim() : '';
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Research report...';
    }
  };
}

module.exports = { ResearchAssistant };
