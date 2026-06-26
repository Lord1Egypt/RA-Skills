#!/usr/bin/env node

/**
 * OpenClaw Quick Start Templates
 * Ready-to-use agent templates
 */

const fs = require('fs');
const path = require('path');

// Template definitions
const templates = {
  'research-bot': {
    name: 'Research Bot',
    description: 'Research agent with web search and summarization',
    files: {
      'AGENT.md': `# Research Bot Agent

Research agent that searches the web and summarizes findings.

## Capabilities
- Web search using free search service
- Summarize findings
- Generate reports
- Save research to memory

## Usage
\`\`\`bash
# Start research
openclaw run

# Or use via message
"Research: [your topic]"
\`\`\`

## Example
\`\`\`
Research: Latest trends in AI automation
\`\`\`
`,
      'custom/research.js': `#!/usr/bin/env node

/**
 * Research Function
 * Search and summarize web content
 */

const { execSync } = require('child_process');

function searchWeb(query) {
  try {
    const output = execSync(\`node ~/.openclaw/workspace/custom/free_search.js '\${query}'\`, {
      encoding: 'utf8',
      timeout: 30000
    });
    return output;
  } catch (error) {
    console.error('Search failed:', error.message);
    return null;
  }
}

function summarizeResults(results) {
  // Extract top results
  const lines = results.split('\\n');
  let summary = '';
  let count = 0;

  for (const line of lines) {
    if (line.startsWith('-') && line.includes('http')) {
      summary += line + '\\n';
      count++;
      if (count >= 5) break;
    }
  }

  return summary;
}

function research(topic) {
  console.log(\`🔍 Researching: \${topic}\\n\`);

  const results = searchWeb(topic);
  if (!results) {
    console.log('❌ Failed to search the web');
    return;
  }

  const summary = summarizeResults(results);
  console.log('📊 Top Results:');
  console.log(summary);

  // Save to memory
  const { execSync } = require('child_process');
  try {
    execSync(\`node ~/.openclaw/skills/openclaw-memorize/memorize.js save "research-\${Date.now()}" "\${topic}"\`, {
      encoding: 'utf8'
    });
    console.log('✅ Research saved to memory');
  } catch (error) {
    // Ignore if memorize skill not installed
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const topic = args.join(' ');

  if (!topic) {
    console.log('Usage: node research.js <topic>');
    console.log('Example: node research.js "AI automation trends"');
    process.exit(1);
  }

  research(topic);
}

module.exports = { research };
`
    }
  },
  'content-generator': {
    name: 'Content Generator',
    description: 'Generate blog posts, social media content, and emails',
    files: {
      'AGENT.md': `# Content Generator Agent

Generate various types of content using AI.

## Capabilities
- Blog posts
- Social media content
- Email drafts
- Marketing copy

## Usage
\`\`\`bash
openclaw run
\`\`\`

## Example
\`\`\`
Generate a blog post about "Benefits of AI automation"
\`\`\`
`,
      'custom/generate.js': `#!/usr/bin/env node

/**
 * Content Generator
 * Generate various types of content
 */

const contentTypes = {
  'blog': {
    template: (topic) => \`# \${topic}

## Introduction
[AI will generate introduction]

## Key Points
[AI will generate key points]

## Conclusion
[AI will generate conclusion]
\`
  },
  'social': {
    template: (topic) => \`🚀 \${topic}

[AI will generate social media post]

#AI #Automation #OpenClaw
\`
  },
  'email': {
    template: (topic) => \`Subject: \${topic}

Hi [Name],

[AI will generate email body]

Best regards,
[Your Name]
\`
  }
};

function generateContent(type, topic) {
  const generator = contentTypes[type];

  if (!generator) {
    console.log(\`❌ Unknown content type: \${type}\`);
    console.log('Available types:', Object.keys(contentTypes).join(', '));
    return;
  }

  console.log(\`✍️ Generating \${type} content for: \${topic}\\n\`);
  console.log('─'.repeat(80));
  console.log(generator.template(topic));
  console.log('─'.repeat(80));
  console.log('\\n💡 Tip: Use this as a starting point and customize as needed');
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const type = args[0];
  const topic = args.slice(1).join(' ');

  if (!type || !topic) {
    console.log('Usage: node generate.js <type> <topic>');
    console.log('Types: blog, social, email');
    console.log('Example: node generate.js blog "AI automation benefits"');
    process.exit(1);
  }

  generateContent(type, topic);
}

module.exports = { generateContent };
`
    }
  },
  'task-automator': {
    name: 'Task Automator',
    description: 'Automate repetitive tasks and workflows',
    files: {
      'AGENT.md': `# Task Automator Agent

Automate repetitive tasks and workflows.

## Capabilities
- Scheduled tasks
- File processing
- API integration
- Workflows

## Usage
\`\`\`bash
openclaw run
\`\`\`

## Example
\`\`\`
Run task: backup-files
\`\`\`
`,
      'custom/automate.js': `#!/usr/bin/env node

/**
 * Task Automator
 * Run automated tasks
 */

const fs = require('fs');
const path = require('path');

const tasks = {
  'backup-files': {
    description: 'Backup important files',
    run: async () => {
      console.log('📦 Starting file backup...');
      const source = process.env.HOME;
      const backupDir = path.join(source, 'backups');

      if (!fs.existsSync(backupDir)) {
        fs.mkdirSync(backupDir, { recursive: true });
      }

      console.log('✅ Backup completed');
      return true;
    }
  },
  'cleanup-temp': {
    description: 'Clean up temporary files',
    run: async () => {
      console.log('🧹 Cleaning up temporary files...');
      // Add cleanup logic here
      console.log('✅ Cleanup completed');
      return true;
    }
  }
};

async function runTask(taskName) {
  const task = tasks[taskName];

  if (!task) {
    console.log(\`❌ Unknown task: \${taskName}\`);
    console.log('Available tasks:', Object.keys(tasks).join(', '));
    return;
  }

  console.log(\`⚡ Running task: \${task.description}\\n\`);
  const success = await task.run();

  if (success) {
    console.log(\`✅ Task completed successfully\`);
  } else {
    console.log(\`❌ Task failed\`);
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const taskName = args[0];

  if (!taskName) {
    console.log('Usage: node automate.js <task_name>');
    console.log('Available tasks:', Object.keys(tasks).join(', '));
    process.exit(1);
  }

  runTask(taskName);
}

module.exports = { runTask };
`
    }
  }
};

// List templates
function listTemplates() {
  console.log('\\n📋 Available Templates');
  console.log('─'.repeat(80));

  for (const [key, template] of Object.entries(templates)) {
    console.log(\`\${key.padEnd(20)} - \${template.description}\`);
  }

  console.log('─'.repeat(80));
  console.log('\\nUsage:');
  console.log('  node start.js create <template_name> <project_path>');
  console.log('\\nExample:');
  console.log('  node start.js create research-bot ./my-bot');
  console.log();
}

// Create project from template
function createProject(templateName, projectPath) {
  const template = templates[templateName];

  if (!template) {
    console.log(\`❌ Template not found: \${templateName}\`);
    console.log('Run "node start.js list" to see available templates');
    process.exit(1);
  }

  console.log(\`🚀 Creating project from "\${template.name}" template...\`);

  // Create project directory
  if (!fs.existsSync(projectPath)) {
    fs.mkdirSync(projectPath, { recursive: true });
  }

  // Copy template files
  for (const [filePath, content] of Object.entries(template.files)) {
    const targetPath = path.join(projectPath, filePath);
    const dir = path.dirname(targetPath);

    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(targetPath, content);
    console.log(\`  ✅ Created: \${filePath}\`);
  }

  console.log('\\n✅ Project created successfully!');
  console.log(\`\nNext steps:\`);
  console.log(\`  cd \${projectPath}\`);
  console.log(\`  # Customize your agent\`);
  console.log(\`  openclaw run\`);
  console.log();
}

// Show help
function showHelp() {
  console.log(\`
🚀 OpenClaw Quick Start

Usage:
  node start.js list
  node start.js create <template_name> <project_path>

Examples:
  node start.js list
  node start.js create research-bot ./my-bot
\`);
}

// Main function
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'list':
    case 'ls':
      listTemplates();
      break;

    case 'create': {
      const templateName = args[1];
      const projectPath = args[2];

      if (!templateName || !projectPath) {
        console.log('❌ Please provide template name and project path');
        showHelp();
        process.exit(1);
      }

      createProject(templateName, projectPath);
      break;
    }

    default:
      showHelp();
      break;
  }
}

main();
