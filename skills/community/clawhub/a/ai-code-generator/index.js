/**
 * AI Code Generator - Plan-and-Solve + ReAct
 */

class CodeGenerator {
  constructor(options = {}) {
    this.style = options.style || 'professional';
    this.includeTests = options.includeTests ?? true;
    this.includeDocs = options.includeDocs ?? true;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async generate(options) {
    const {
      requirements,
      language = 'javascript',
      framework = 'express',
      database = null,
      features = []
    } = options;

    if (this.verbose) {
      console.log('🏗️  Starting code generation...');
      console.log(`   Requirements: ${requirements.substring(0, 100)}...`);
      console.log(`   Language: ${language}`);
      console.log(`   Framework: ${framework}`);
      console.log();
    }

    // Phase 1: Analyze requirements
    if (this.verbose) console.log('📋 Phase 1: Analyzing requirements...\n');
    const analysis = await this.analyzeRequirements(requirements);

    // Phase 2: Design architecture
    if (this.verbose) console.log('🏗️  Phase 2: Designing architecture...\n');
    const architecture = await this.designArchitecture(analysis, language, framework);

    // Phase 3: Plan file structure
    if (this.verbose) console.log('📁 Phase 3: Planning file structure...\n');
    const fileStructure = await this.planFileStructure(architecture);

    // Phase 4: Generate code for each file
    if (this.verbose) console.log('📝 Phase 4: Generating code...\n');
    const files = await this.generateFiles(fileStructure, requirements, language);

    // Phase 5: Generate tests
    if (this.includeTests) {
      if (this.verbose) console.log('🧪 Phase 5: Generating tests...\n');
      const testFiles = await this.generateTests(files, language);
      files.push(...testFiles);
    }

    // Phase 6: Generate documentation
    if (this.includeDocs) {
      if (this.verbose) console.log('📚 Phase 6: Generating documentation...\n');
      const docFiles = await this.generateDocumentation(files, requirements);
      files.push(...docFiles);
    }

    if (this.verbose) console.log('✅ Code generation complete!\n');

    return {
      requirements,
      analysis,
      architecture,
      files,
      fileCount: files.length,
      instructions: this.generateInstructions(files)
    };
  }

  async analyzeRequirements(requirements) {
    const prompt = `Analyze these requirements:

${requirements}

Provide:
1. Core features
2. User stories
3. Technical requirements
4. Non-functional requirements (performance, security, etc.)
5. Potential challenges`;

    return await this.llm.generate(prompt);
  }

  async designArchitecture(analysis, language, framework) {
    const prompt = `Design architecture for:

${analysis}

Language: ${language}
Framework: ${framework}

Provide:
1. Architecture pattern (MVC, Microservices, etc.)
2. Component diagram
3. Data flow
4. API design
5. Database schema (if applicable)`;

    return await this.llm.generate(prompt);
  }

  async planFileStructure(architecture) {
    const prompt = `Plan file structure for this architecture:

${architecture}

Return as JSON:
{
  "files": [
    {
      "path": "src/controllers/user.controller.js",
      "description": "User CRUD operations",
      "dependencies": ["user.model.js", "auth.middleware.js"]
    }
  ]
}`;

    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch (e) {}

    return { files: [] };
  }

  async generateFiles(fileStructure, requirements, language) {
    const files = [];

    for (const fileSpec of fileStructure.files) {
      if (this.verbose) {
        console.log(`  Generating: ${fileSpec.path}`);
      }

      const content = await this.generateFileContent(
        fileSpec,
        requirements,
        language
      );

      files.push({
        path: fileSpec.path,
        content,
        description: fileSpec.description
      });
    }

    return files;
  }

  async generateFileContent(fileSpec, requirements, language) {
    const prompt = `Generate code for:

File: ${fileSpec.path}
Description: ${fileSpec.description}
Requirements: ${requirements}
Language: ${language}
Dependencies: ${fileSpec.dependencies ? fileSpec.dependencies.join(', ') : 'None'}

Write complete, production-ready code with:
- Proper imports/exports
- Error handling
- Comments for complex logic
- Follow best practices`;

    return await this.llm.generate(prompt);
  }

  async generateTests(files, language) {
    const testFiles = [];
    const sourceFiles = files.filter(f => !f.path.includes('test'));

    for (const file of sourceFiles.slice(0, 3)) { // Limit to 3 test files for speed
      const testPath = file.path.replace('.js', '.test.js').replace('src/', 'tests/');
      
      const prompt = `Write unit tests for:

${file.content}

File: ${testPath}
Framework: Jest (for JavaScript) or pytest (for Python)

Include:
- Test setup
- Happy path tests
- Edge case tests
- Error handling tests`;

      const content = await this.llm.generate(prompt);
      testFiles.push({
        path: testPath,
        content,
        description: `Tests for ${file.path}`
      });
    }

    return testFiles;
  }

  async generateDocumentation(files, requirements) {
    const readme = await this.generateREADME(requirements, files);
    
    return [
      {
        path: 'README.md',
        content: readme,
        description: 'Project documentation'
      }
    ];
  }

  async generateREADME(requirements, files) {
    const prompt = `Generate README.md for:

Requirements: ${requirements}
Files: ${files.map(f => `- ${f.path}`).join('\n')}

Include:
1. Project title and description
2. Features
3. Installation instructions
4. Usage examples
5. API documentation (if applicable)
6. Testing instructions
7. Contributing guidelines`;

    return await this.llm.generate(prompt);
  }

  generateInstructions(files) {
    return `## Next Steps

1. **Review Generated Code**
   - Check all files for correctness
   - Verify business logic
   - Update as needed

2. **Install Dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Configure Environment**
   - Copy .env.example to .env
   - Update environment variables

4. **Run Tests**
   \`\`\`bash
   npm test
   \`\`\`

5. **Start Application**
   \`\`\`bash
   npm start
   \`\`\`

6. **Customize**
   - Add your business logic
   - Update styling
   - Add additional features

Generated ${files.length} files. Review and customize as needed.`;
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return '// Generated code...';
    }
  };
}

module.exports = { CodeGenerator };
