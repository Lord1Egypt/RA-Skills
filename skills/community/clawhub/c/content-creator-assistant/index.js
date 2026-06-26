/**
 * Content Creator Assistant
 * 
 * Combines Tree of Thoughts (creative exploration) with Reflection (iterative refinement)
 */

const { TreeOfThoughtsAgent } = require('./agents/tree-of-thoughts');
const { ReflectionAgent } = require('./agents/reflection');

class ContentCreatorAssistant {
  constructor(options = {}) {
    this.style = options.style || 'professional';
    this.tone = options.tone || 'informative';
    this.iterations = options.iterations || 3;
    this.branches = options.branches || 4;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    
    // Initialize agents
    this.totAgent = new TreeOfThoughtsAgent({
      maxDepth: 2,
      branchFactor: this.branches,
      beamWidth: 2,
      verbose: this.verbose,
      llm: this.llm
    });
    
    this.reflectionAgent = new ReflectionAgent({
      maxIterations: this.iterations,
      verbose: this.verbose,
      llm: this.llm,
      criteria: [
        'Clarity: Is the content easy to understand?',
        'Engagement: Is the content interesting and compelling?',
        'Accuracy: Is the information correct and well-researched?',
        'Structure: Is the content well-organized?',
        'Style: Does it match the requested tone and style?',
        'Completeness: Are all key points covered?'
      ]
    });
  }

  async write(options) {
    const {
      topic,
      type = 'article',
      audience = 'general',
      length = 'medium',
      keyPoints = [],
      wordCount = null
    } = options;

    if (this.verbose) {
      console.log('✍️  Starting content creation...');
      console.log(`   Topic: ${topic}`);
      console.log(`   Type: ${type}`);
      console.log(`   Audience: ${audience}`);
      console.log();
    }

    // Phase 1: Tree of Thoughts - Explore angles
    if (this.verbose) {
      console.log('🌳 Phase 1: Exploring content angles (Tree of Thoughts)...\n');
    }

    const angleTask = this.buildAngleTask(topic, type, audience, keyPoints);
    const bestAngle = await this.totAgent.execute(angleTask);

    if (this.verbose) {
      console.log(`\n✅ Selected angle: ${bestAngle.substring(0, 100)}...\n`);
    }

    // Phase 2: Generate outline
    if (this.verbose) {
      console.log('📋 Phase 2: Generating outline...\n');
    }

    const outline = await this.generateOutline(topic, bestAngle, type, keyPoints);

    if (this.verbose) {
      console.log('Outline generated\n');
    }

    // Phase 3: Write initial draft
    if (this.verbose) {
      console.log('📝 Phase 3: Writing initial draft...\n');
    }

    const draft = await this.writeDraft(topic, outline, length, wordCount);

    if (this.verbose) {
      console.log(`Draft complete (${this.countWords(draft)} words)\n`);
    }

    // Phase 4: Reflection - Iterative refinement
    if (this.verbose) {
      console.log('🔄 Phase 4: Refining content (Reflection)...\n');
    }

    const refinedContent = await this.reflectionAgent.execute(
      `Improve the following content for ${type} targeting ${audience}:\n\n${draft}`
    );

    if (this.verbose) {
      console.log(`\n✅ Refinement complete (${this.countWords(refinedContent)} words)\n`);
    }

    // Phase 5: Final polish
    if (this.verbose) {
      console.log('✨ Phase 5: Final polish...\n');
    }

    const finalContent = await this.polish(refinedContent, type, this.style, this.tone);

    if (this.verbose) {
      console.log('✅ Content creation complete!\n');
    }

    return {
      title: this.extractTitle(finalContent),
      content: finalContent,
      wordCount: this.countWords(finalContent),
      outline,
      draft,
      iterations: this.iterations
    };
  }

  buildAngleTask(topic, type, audience, keyPoints) {
    return `Generate different content angles for:

Topic: ${topic}
Type: ${type}
Audience: ${audience}
Key Points: ${keyPoints.join(', ')}

Provide ${this.branches} distinct approaches to this content. Each approach should have a unique angle or perspective.`;
  }

  async generateOutline(topic, angle, type, keyPoints) {
    const prompt = `
Create a detailed outline for:

Topic: ${topic}
Selected Angle: ${angle}
Type: ${type}
Key Points: ${keyPoints.join(', ')}

Outline structure:
1. Introduction (hook + thesis)
2. Main sections (3-5 sections)
3. Conclusion (summary + call-to-action)

Return as markdown with clear hierarchy.`;

    return await this.llm.generate(prompt);
  }

  async writeDraft(topic, outline, length, wordCount) {
    const lengthGuidance = wordCount 
      ? `Target word count: ${wordCount} words`
      : `Length: ${length} (${this.getLengthGuidance(length)})`;

    const prompt = `
Write a complete draft based on this outline:

Topic: ${topic}
${lengthGuidance}

Outline:
${outline}

Write the full content following the outline structure.`;

    return await this.llm.generate(prompt);
  }

  async polish(content, type, style, tone) {
    const prompt = `
Polish the following content:

Type: ${type}
Style: ${style}
Tone: ${tone}

Content:
${content}

Improve:
1. Grammar and spelling
2. Sentence flow and variety
3. Word choice and vocabulary
4. Transitions between sections
5. Overall readability

Maintain the original meaning while enhancing quality.`;

    return await this.llm.generate(prompt);
  }

  countWords(text) {
    return text.trim().split(/\s+/).length;
  }

  getLengthGuidance(length) {
    const guidelines = {
      short: '500-800 words',
      medium: '1000-1500 words',
      long: '2000+ words'
    };
    return guidelines[length] || guidelines.medium;
  }

  extractTitle(content) {
    const lines = content.split('\n');
    const titleLine = lines.find(line => line.startsWith('# '));
    return titleLine ? titleLine.replace('# ', '').trim() : 'Untitled';
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return '# Content\n\nGenerated content...';
    }
  };
}

module.exports = { ContentCreatorAssistant };
