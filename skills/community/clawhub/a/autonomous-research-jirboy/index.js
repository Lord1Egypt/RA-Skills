/**
 * Autonomous Research Skill - Entry Point
 * 
 * Orchestrates the 23-stage research pipeline from AutoResearchClaw.
 * Converts a research topic into a complete academic paper.
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

// Configuration paths
const SKILL_DIR = path.join(__dirname);
const CONFIG_FILE = path.join(SKILL_DIR, 'config.yaml');
const CONFIG_TEMPLATE = path.join(SKILL_DIR, 'config.example.yaml');
const ARTIFACTS_DIR = path.join(process.env.OPENCLAW_WORKSPACE || process.cwd(), 'artifacts');

/**
 * Main entry point for the autonomous research skill
 * @param {Object} options - Skill options
 * @param {string} options.topic - Research topic/idea
 * @param {string} options.mode - Experiment mode: 'simulated' | 'sandbox' | 'ssh_remote'
 * @param {string} options.template - Conference template: 'neurips' | 'icml' | 'iclr'
 * @param {boolean} options.autoApprove - Skip gate approvals
 * @param {string} options.model - LLM model to use
 * @returns {Promise<Object>} - Research results
 */
async function run(options) {
  const {
    topic,
    mode = 'simulated',
    template = 'neurips',
    autoApprove = true,
    model,
  } = options;

  if (!topic) {
    throw new Error('Research topic is required');
  }

  console.log(`🔬 Starting autonomous research on: "${topic}"`);
  console.log(`   Mode: ${mode}, Template: ${template}, Auto-approve: ${autoApprove}`);

  try {
    // Step 1: Ensure configuration exists
    await ensureConfig();

    // Step 2: Update config with user preferences
    await updateConfig({ mode, template, model });

    // Step 3: Run the pipeline
    const result = await runPipeline(topic, autoApprove);

    // Step 4: Return results
    return {
      success: true,
      topic,
      artifacts: result.artifacts,
      deliverables: result.deliverables,
      message: generateSummary(result),
    };
  } catch (error) {
    console.error('❌ Research pipeline failed:', error.message);
    return {
      success: false,
      topic,
      error: error.message,
      suggestions: getTroubleshootingSuggestions(error),
    };
  }
}

/**
 * Ensure configuration file exists
 */
async function ensureConfig() {
  try {
    await fs.access(CONFIG_FILE);
  } catch {
    console.log('📝 Creating configuration from template...');
    await fs.copyFile(CONFIG_TEMPLATE, CONFIG_FILE);
  }
}

/**
 * Update configuration with user preferences
 */
async function updateConfig prefs) {
  let config = await fs.readFile(CONFIG_FILE, 'utf-8');
  
  if (prefs.mode) {
    config = config.replace(/mode:\s*['"]?\w+['"]?/, `mode: '${prefs.mode}'`);
  }
  
  if (prefs.template) {
    config = config.replace(/template:\s*['"]?\w+['"]?/, `template: '${prefs.template}'`);
  }
  
  if (prefs.model) {
    config = config.replace(/primary_model:\s*['"]?[\w.-]+['"]?/, `primary_model: '${prefs.model}'`);
  }
  
  await fs.writeFile(CONFIG_FILE, config);
}

/**
 * Run the 23-stage research pipeline
 */
async function runPipeline(topic, autoApprove) {
  const args = [
    'researchclaw',
    'run',
    `--topic "${topic}"`,
    `--config "${CONFIG_FILE}"`,
    autoApprove ? '--auto-approve' : '',
  ].filter(Boolean).join(' ');

  console.log('🚀 Executing pipeline:', args);
  
  const { stdout, stderr } = await execAsync(args, {
    cwd: SKILL_DIR,
    timeout: 24 * 60 * 60 * 1000, // 24 hour timeout
    maxBuffer: 10 * 1024 * 1024, // 10MB buffer
  });

  if (stderr && !stderr.includes('WARNING')) {
    console.warn('Pipeline warnings:', stderr);
  }

  // Parse output to find artifact directory
  const artifactMatch = stdout.match(/artifacts\/(rc-[^/\s]+)/);
  const artifactDir = artifactMatch 
    ? path.join(process.cwd(), 'artifacts', artifactMatch[1])
    : null;

  return {
    raw_output: stdout,
    artifacts: artifactDir,
    deliverables: artifactDir ? path.join(artifactDir, 'deliverables') : null,
  };
}

/**
 * Generate human-readable summary of results
 */
function generateSummary(result) {
  const parts = ['✅ 研究完成！'];
  
  if (result.deliverables) {
    parts.push(`\n📁 输出目录：${result.deliverables}`);
    parts.push('\n📄 生成文件:');
    parts.push('   - paper_draft.md (论文草稿)');
    parts.push('   - paper.tex (LaTeX 源码)');
    parts.push('   - references.bib (参考文献)');
    parts.push('   - charts/ (图表)');
    parts.push('   - experiment_runs/ (实验代码和结果)');
  }
  
  return parts.join('\n');
}

/**
 * Get troubleshooting suggestions based on error
 */
function getTroubleshootingSuggestions(error) {
  const message = error.message.toLowerCase();
  
  if (message.includes('api') || message.includes('key')) {
    return '检查 LLM API Key 配置是否正确';
  }
  if (message.includes('network') || message.includes('connection')) {
    return '检查网络连接，确保可以访问 OpenAlex/Semantic Scholar/arXiv';
  }
  if (message.includes('timeout')) {
    return '实验执行超时，尝试使用 simulated 模式或增加 timeout 配置';
  }
  if (message.includes('latex') || message.includes('compile')) {
    return '检查 MiKTeX 是否正确安装';
  }
  
  return '查看详细错误日志，或尝试使用 simulated 模式重新运行';
}

// Export for OpenClaw skill system
module.exports = {
  run,
  runPipeline,
  ensureConfig,
};
