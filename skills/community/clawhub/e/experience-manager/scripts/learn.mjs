#!/usr/bin/env node
/**
 * 经验学习脚本
 * 从 zip 包中学习经验，转化为自己的 SOUL/AGENTS/TOOLS
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import AdmZip from 'adm-zip';
import https from 'https';
import http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const EXPERIENCES_DIR = path.join(process.env.HOME || '/root', '.openclaw', 'experiences');
const PACKAGES_DIR = path.join(EXPERIENCES_DIR, 'packages');
const EXTRACTED_DIR = path.join(EXPERIENCES_DIR, 'extracted');
const INDEX_FILE = path.join(EXPERIENCES_DIR, 'index.json');
const WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || '/root', '.openclaw', 'workspace');
const AGENTS_DIR = process.env.OPENCLAW_AGENTS_DIR || '/data/openclaw/agents';

let TARGET_WORKSPACE = WORKSPACE_DIR;

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function readIndex() {
  if (!fs.existsSync(INDEX_FILE)) {
    return { agents: {} };
  }
  const data = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8'));
  if (data.experiences && !data.agents) {
    return { agents: {} };
  }
  return data;
}

function writeIndex(index) {
  ensureDir(EXPERIENCES_DIR);
  fs.writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2), 'utf8');
}

function getAgentName(workspaceDir) {
  if (workspaceDir === WORKSPACE_DIR) {
    return 'default';
  }
  const basename = path.basename(workspaceDir);
  return basename.replace(/-workspace$/, '');
}

function checkLearned(index, name, version, agentName) {
  const agentExperiences = index.agents?.[agentName]?.experiences || [];
  return agentExperiences.find(e => e.name === name && e.version === version);
}

function checkNewerVersion(index, name, version, agentName) {
  const agentExperiences = index.agents?.[agentName]?.experiences || [];
  const existing = agentExperiences.find(e => e.name === name);
  if (existing && existing.version !== version) {
    return existing;
  }
  return null;
}

const HUB_API_BASE = 'https://www.expericehub.com:18080';

function request(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    protocol.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('Parse failed: ' + data));
        }
      });
    }).on('error', reject);
  });
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(dest);
    protocol.get(url, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        downloadFile(response.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      if (response.statusCode !== 200) {
        reject(new Error('Download failed: HTTP ' + response.statusCode));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(dest);
      });
    }).on('error', reject);
  });
}

async function getZipPath(source) {
  if (!source.startsWith('http://') && 
      !source.startsWith('https://') && 
      !source.startsWith('file://') &&
      !source.startsWith('/') &&
      !source.startsWith('~')) {
    const packagePath = path.join(PACKAGES_DIR, source);
    if (fs.existsSync(packagePath)) {
      return packagePath;
    }
    
    const withZip = path.join(PACKAGES_DIR, source + '.zip');
    if (fs.existsSync(withZip)) {
      return withZip;
    }
    
    console.log('Searching Experience Hub: ' + source);
    try {
      const apiUrl = HUB_API_BASE + '/api/experiences/' + source;
      const details = await request(apiUrl);
      
      if (details && details.id) {
        console.log('Found: ' + details.name + ' v' + details.version);
        console.log('Description: ' + details.description);
        
        const expYml = {
          schema: details.schema || 'openclaw.experience.v1',
          name: details.name,
          description: details.description,
          metadata: {
            version: details.version,
            author: details.author
          },
          skills: details.skills ? JSON.parse(details.skills) : []
        };
        
        const tempDir = path.join(PACKAGES_DIR, 'temp', details.id);
        ensureDir(tempDir);
        
        fs.writeFileSync(path.join(tempDir, 'exp.yml'), yaml.dump(expYml));
        
        if (details.references && details.references.length > 0) {
          console.log('References: ' + details.references.length + ' files');
          for (const ref of details.references) {
            const refPath = path.join(tempDir, ref.path);
            ensureDir(path.dirname(refPath));
            fs.writeFileSync(refPath, ref.content);
          }
        }
        
        const zipPath = path.join(PACKAGES_DIR, details.id + '.zip');
        const zip = new AdmZip();
        zip.addLocalFolder(tempDir);
        zip.writeZip(zipPath);
        
        console.log('Built: ' + zipPath);
        return zipPath;
      }
    } catch (err) {
      console.log('API error: ' + err.message);
    }
    
    throw new Error('Package not found: ' + source);
  }
  
  if (source.startsWith('http://') || source.startsWith('https://')) {
    const filename = path.basename(source) || 'experience.zip';
    const destPath = path.join(PACKAGES_DIR, filename);
    ensureDir(PACKAGES_DIR);
    console.log('Downloading: ' + source);
    await downloadFile(source, destPath);
    console.log('Done: ' + destPath);
    return destPath;
  }
  
  if (source.startsWith('file://')) {
    return source.replace('file://', '');
  }
  
  if (fs.existsSync(source)) {
    return path.resolve(source);
  }
  
  const packagePath = path.join(PACKAGES_DIR, source);
  if (fs.existsSync(packagePath)) {
    return packagePath;
  }
  
  throw new Error('Package not found: ' + source);
}

function extractZip(zipPath) {
  const zip = new AdmZip(zipPath);
  const name = path.basename(zipPath, '.zip');
  const extractPath = path.join(EXTRACTED_DIR, name);
  ensureDir(extractPath);
  zip.extractAllTo(extractPath, true);
  return { name, extractPath };
}

function readExpYml(extractPath) {
  const expPath = path.join(extractPath, 'exp.yml');
  if (!fs.existsSync(expPath)) {
    throw new Error('exp.yml not found');
  }
  const content = fs.readFileSync(expPath, 'utf8');
  return yaml.load(content);
}

function readReferences(extractPath, expYml) {
  const references = {};
  const refs = expYml.references || {};
  if (refs.soul) {
    const soulPath = path.join(extractPath, refs.soul);
    if (fs.existsSync(soulPath)) {
      references.soul = fs.readFileSync(soulPath, 'utf8');
    }
  }
  if (refs.agents) {
    const agentsPath = path.join(extractPath, refs.agents);
    if (fs.existsSync(agentsPath)) {
      references.agents = fs.readFileSync(agentsPath, 'utf8');
    }
  }
  if (refs.tools) {
    const toolsPath = path.join(extractPath, refs.tools);
    if (fs.existsSync(toolsPath)) {
      references.tools = fs.readFileSync(toolsPath, 'utf8');
    }
  }
  return references;
}

function checkDependencies(expYml) {
  const handler = getSchemaHandler(expYml);
  const required = handler.getSkills(expYml);
  const missing = [];
  const installed = [];
  
  const possibleDirs = [
    path.join(process.env.HOME || '/root', '.openclaw', 'skills'),
    '/app/skills',
    path.join(__dirname, '../../skills')
  ];
  
  let installedSkills = [];
  for (const dir of possibleDirs) {
    if (fs.existsSync(dir)) {
      try {
        const skills = fs.readdirSync(dir)
          .filter(d => {
            try {
              return fs.statSync(path.join(dir, d)).isDirectory() && !d.startsWith('.');
            } catch {
              return false;
            }
          });
        installedSkills.push(...skills);
      } catch (e) {}
    }
  }
  installedSkills = [...new Set(installedSkills)];
  
  for (const skill of required) {
    const isInstalled = installedSkills.some(s => 
      s.toLowerCase() === skill.toLowerCase() ||
      s.toLowerCase().replace(/[_-]/g, '') === skill.toLowerCase().replace(/[_-]/g, '')
    );
    if (isInstalled) {
      installed.push(skill);
    } else {
      missing.push(skill);
    }
  }
  
  return { required, installed, missing, satisfied: missing.length === 0 };
}

function analyzeRelevance(expYml, workspaceDir = TARGET_WORKSPACE) {
  const soulPath = path.join(workspaceDir, 'SOUL.md');
  const toolsPath = path.join(workspaceDir, 'TOOLS.md');
  const hasSoul = fs.existsSync(soulPath);
  const hasTools = fs.existsSync(toolsPath);
  
  const handler = getSchemaHandler(expYml);
  const mySkills = [];
  const requiredSkills = handler.getSkills(expYml);
  const skillMatch = requiredSkills.filter(s => mySkills.includes(s)).length;
  
  let relevance = 'medium';
  if (skillMatch === requiredSkills.length && requiredSkills.length > 0) {
    relevance = 'high';
  } else if (skillMatch > 0) {
    relevance = 'medium';
  } else {
    relevance = 'low';
  }
  
  return { relevance, skillMatch, totalSkills: requiredSkills.length, hasSoul, hasTools };
}

const SCHEMA_HANDLERS = {
  'openclaw.experience.v1': {
    getName: (expYml) => expYml.name,
    getVersion: (expYml) => expYml.metadata?.version || '1.0.0',
    getDescription: (expYml) => expYml.description,
    getSkills: (expYml) => expYml.skills || [],
    getReferences: (expYml) => ({ soul: expYml.soul, agents: expYml.agents, tools: expYml.tools }),
    getType: (expYml) => 'best_practice'
  },
  'default': {
    getName: (expYml) => expYml.meta?.name || expYml.name,
    getVersion: (expYml) => expYml.meta?.version || expYml.metadata?.version || '1.0.0',
    getDescription: (expYml) => expYml.meta?.description || expYml.description,
    getSkills: (expYml) => expYml.context?.required_skills || expYml.skills || [],
    getReferences: (expYml) => expYml.references || {},
    getType: (expYml) => expYml.core?.type || 'best_practice'
  }
};

function getSchemaHandler(expYml) {
  const schema = expYml.schema;
  if (schema && SCHEMA_HANDLERS[schema]) {
    return SCHEMA_HANDLERS[schema];
  }
  return SCHEMA_HANDLERS['default'];
}

function determineTargets(expYml) {
  const targets = [];
  const reasons = [];
  const handler = getSchemaHandler(expYml);
  const refs = handler.getReferences(expYml);
  const type = handler.getType(expYml);
  
  if (refs.soul) {
    targets.push({ file: 'SOUL.md', section: 'Behavior', reason: 'ref: ' + refs.soul, sourceFile: refs.soul });
    reasons.push('SOUL.md: ' + refs.soul);
  }
  if (refs.agents) {
    targets.push({ file: 'AGENTS.md', section: 'Workflow', reason: 'ref: ' + refs.agents, sourceFile: refs.agents });
    reasons.push('AGENTS.md: ' + refs.agents);
  }
  if (refs.tools) {
    targets.push({ file: 'TOOLS.md', section: 'Tools', reason: 'ref: ' + refs.tools, sourceFile: refs.tools });
    reasons.push('TOOLS.md: ' + refs.tools);
  }
  if (type === 'error_lesson') {
    targets.push({ file: '.learnings/ERRORS.md', section: 'Error', reason: 'error_lesson' });
    reasons.push('ERRORS.md: error_lesson');
  }
  if (type === 'knowledge_gap') {
    targets.push({ file: '.learnings/LEARNINGS.md', section: 'Knowledge', reason: 'knowledge_gap' });
    reasons.push('LEARNINGS.md: knowledge_gap');
  }
  if (targets.length === 0) {
    targets.push({ file: 'AGENTS.md', section: 'Experience', reason: 'default' });
    reasons.push('AGENTS.md: default');
  }
  
  return { targets, reasons };
}

function generatePlan(expYml, relevance) {
  const { targets, reasons } = determineTargets(expYml);
  return { targets, reasons, content: '' };
}

function generateContent(expYml) {
  const lines = [];
  lines.push('## ' + (expYml.meta?.title || 'Experience'));
  lines.push('> Source: ' + (expYml.meta?.name || expYml.name) + ' v' + (expYml.meta?.version || expYml.metadata?.version || '1.0.0'));
  lines.push('> Type: ' + (expYml.core?.type || 'best_practice'));
  lines.push('');
  if (expYml.core?.problem?.description) {
    lines.push('**Problem**: ' + expYml.core.problem.description);
    lines.push('');
  }
  if (expYml.core?.solution?.steps?.length > 0) {
    lines.push('**Solution**:');
    expYml.core.solution.steps.forEach((step, i) => lines.push((i + 1) + '. ' + step));
    lines.push('');
  }
  return lines.join('\n');
}

function applyLearning(expYml, plan, references) {
  const results = { success: [], failed: [], details: [] };
  
  for (const target of plan.targets) {
    const targetPath = path.join(TARGET_WORKSPACE, target.file);
    
    try {
      let backupPath = null;
      if (fs.existsSync(targetPath)) {
        backupPath = targetPath + '.bak.' + Date.now();
        fs.copyFileSync(targetPath, backupPath);
      }
      
      let content;
      if (target.sourceFile && references[target.file.toLowerCase().replace('.md', '')]) {
        content = references[target.file.toLowerCase().replace('.md', '')];
      } else {
        if (target.file === 'SOUL.md') {
          content = generateSoulContent(expYml);
        } else if (target.file === 'AGENTS.md') {
          content = generateAgentsContent(expYml);
        } else {
          content = generateContent(expYml);
        }
      }
      
      if (fs.existsSync(targetPath)) {
        fs.appendFileSync(targetPath, '\n\n' + content);
      } else {
        ensureDir(path.dirname(targetPath));
        fs.writeFileSync(targetPath, content);
      }
      
      results.success.push(target.file);
      results.details.push({ file: target.file, status: 'success', backupPath, linesAdded: content.split('\n').length });
    } catch (err) {
      results.failed.push(target.file);
      results.details.push({ file: target.file, status: 'failed', error: err.message });
    }
  }
  
  return results;
}

function generateSoulContent(expYml) {
  const handler = getSchemaHandler(expYml);
  const name = handler.getName(expYml);
  const version = handler.getVersion(expYml);
  const description = handler.getDescription(expYml);
  const type = handler.getType(expYml);
  
  const lines = [];
  lines.push('## ' + (description || 'Experience'));
  lines.push('> Source: Package ' + name + ' v' + version);
  lines.push('> Type: ' + type);
  lines.push('> Learned: ' + new Date().toISOString());
  lines.push('');
  lines.push('**Principle**: ' + description);
  lines.push('');
  lines.push('**Guidelines**:');
  lines.push('1. ' + description);
  lines.push('');
  return lines.join('\n');
}

function generateAgentsContent(expYml) {
  const handler = getSchemaHandler(expYml);
  const name = handler.getName(expYml);
  const version = handler.getVersion(expYml);
  const description = handler.getDescription(expYml);
  const type = handler.getType(expYml);
  
  const lines = [];
  lines.push('## ' + (description || 'Experience'));
  lines.push('> Source: Package ' + name + ' v' + version);
  lines.push('> Type: ' + type);
  lines.push('');
  lines.push('**Scenario**: ' + description);
  lines.push('');
  lines.push('**Process**:');
  lines.push('1. ' + description);
  lines.push('');
  lines.push('**Rules**: ' + description);
  lines.push('');
  return lines.join('\n');
}

function generateChangePreview(expYml, plan, references = {}, workspaceDir = TARGET_WORKSPACE) {
  const preview = [];
  
  for (const target of plan.targets) {
    const targetPath = path.join(workspaceDir, target.file);
    
    let newContent;
    const refKey = target.file.toLowerCase().replace('.md', '');
    if (references[refKey]) {
      newContent = references[refKey];
    } else {
      if (target.file === 'SOUL.md') {
        newContent = generateSoulContent(expYml);
      } else if (target.file === 'AGENTS.md') {
        newContent = generateAgentsContent(expYml);
      } else {
        newContent = generateContent(expYml);
      }
    }
    
    let existingContent = '';
    let fileExists = false;
    if (fs.existsSync(targetPath)) {
      existingContent = fs.readFileSync(targetPath, 'utf8');
      fileExists = true;
    }
    
    const existingLines = existingContent.split('\n');
    const tailContent = existingLines.slice(-5).join('\n');
    
    preview.push({
      file: target.file,
      path: targetPath,
      exists: fileExists,
      operation: fileExists ? 'Append' : 'Create',
      tailContent,
      newContent,
      section: target.section,
      reason: target.reason
    });
  }
  
  return preview;
}

function displayChangePreview(preview) {
  for (const item of preview) {
    console.log('File: ' + item.file);
    console.log('  Path: ' + item.path);
    console.log('  Operation: ' + item.operation);
    console.log('  Section: ' + item.section);
    console.log('  Reason: ' + item.reason);
    console.log('');
    if (item.exists) {
      console.log('  Current:');
      console.log('  ' + '-'.repeat(60));
      item.tailContent.split('\n').forEach(line => console.log('  ' + line));
      console.log('  ' + '-'.repeat(60));
      console.log('                           Append below:');
    }
    console.log('  New:');
    console.log('  ' + '-'.repeat(60));
    item.newContent.split('\n').forEach(line => console.log('  + ' + line));
    console.log('  ' + '-'.repeat(60));
    console.log('');
  }
}

function confirmChanges(args) {
  return new Promise((resolve) => {
    if (args.includes('--dry-run')) {
      console.log('Mode: dry-run');
      resolve(false);
      return;
    }
    if (args.includes('--yes') || args.includes('-y')) {
      console.log('Y (--yes)');
      resolve(true);
      return;
    }
    console.log('This will modify SOUL.md/AGENTS.md/TOOLS.md');
    console.log('Continue? [Y/N/S]');
    import('readline').then((readlineModule) => {
      const readline = readlineModule.createInterface({ input: process.stdin, output: process.stdout });
      readline.question('> ', (answer) => {
        readline.close();
        const choice = answer.trim().toUpperCase();
        if (choice === 'Y' || choice === 'YES') {
          resolve(true);
        } else if (choice === 'S' || choice === 'SAVE') {
          resolve('save');
        } else {
          resolve(false);
        }
      });
    }).catch(() => {
      resolve(false);
    });
  });
}

function generateVerificationGuide(expYml, results, deps) {
  const guide = {
    title: expYml.meta?.title || 'Experience',
    type: expYml.core?.type || 'best_practice',
    problem: expYml.core?.problem?.description || '',
    solution: expYml.core?.solution?.steps || [],
    skills: deps.required || [],
    appliedFiles: results.success || [],
    steps: []
  };
  
  guide.steps = [
    { title: 'View learned content', description: 'Check the applied files' },
    { title: 'Apply in practice', description: 'Use in relevant scenarios' }
  ];
  
  return guide;
}

function displayVerificationGuide(guide) {
  console.log('Verification Guide\n');
  console.log('Experience: ' + guide.title);
  console.log('Type: ' + guide.type);
  console.log('');
  console.log('Steps:');
  guide.steps.forEach((step, i) => {
    console.log((i + 1) + '. ' + step.title);
    if (step.description) console.log('   ' + step.description);
  });
  console.log('');
}

function recordLearning(expYml, appliedFiles) {
  const index = readIndex();
  const handler = getSchemaHandler(expYml);
  const name = handler.getName(expYml);
  const version = handler.getVersion(expYml);
  const description = handler.getDescription(expYml);
  const agentName = getAgentName(TARGET_WORKSPACE);
  
  if (!index.agents) index.agents = {};
  if (!index.agents[agentName]) {
    index.agents[agentName] = { name: agentName, workspace: TARGET_WORKSPACE, experiences: [] };
  }
  
  const agentExperiences = index.agents[agentName].experiences;
  const existingIndex = agentExperiences.findIndex(e => e.name === name);
  
  const record = {
    name, version, title: description,
    status: 'learned',
    learned_at: new Date().toISOString(),
    applied_to: appliedFiles
  };
  
  if (existingIndex >= 0) {
    agentExperiences[existingIndex] = record;
  } else {
    agentExperiences.push(record);
  }
  
  writeIndex(index);
}

async function main() {
  const args = process.argv.slice(2);
  let source = null;
  let targetAgent = null;
  
  for (const arg of args) {
    if (arg === '--yes' || arg === '-y') {}
    else if (arg === '--dry-run') {}
    else if (arg.startsWith('--agent=')) {
      targetAgent = arg.replace('--agent=', '').trim();
    } else if (!arg.startsWith('--')) {
      source = arg;
    }
  }
  
  if (!source) {
    console.error('Usage: node learn.mjs <package> [options]');
    console.error('Options: --yes, --dry-run, --agent=<name>');
    process.exit(1);
  }
  
  if (targetAgent) {
    const agentDir = targetAgent.endsWith('-workspace') ? targetAgent : targetAgent + '-workspace';
    const agentPath = path.join(AGENTS_DIR, agentDir);
    if (!fs.existsSync(agentPath)) {
      console.error('Agent not found: ' + agentPath);
      process.exit(1);
    }
    TARGET_WORKSPACE = agentPath;
    console.log('Target: ' + targetAgent);
    console.log('Workspace: ' + TARGET_WORKSPACE + '\n');
  }
  
  console.log('Learning...\n');
  
  try {
    const zipPath = await getZipPath(source);
    
    console.log('Extracting...');
    const { name, extractPath } = extractZip(zipPath);
    console.log('Done: ' + extractPath + '\n');
    
    console.log('Reading...');
    const expYml = readExpYml(extractPath);
    const handler = getSchemaHandler(expYml);
    const expName = handler.getName(expYml);
    const expVersion = handler.getVersion(expYml);
    const expDescription = handler.getDescription(expYml);
    const expType = handler.getType(expYml);
    
    console.log('  Name: ' + expName);
    console.log('  Version: ' + expVersion);
    console.log('  Description: ' + expDescription);
    console.log('  Type: ' + expType);
    console.log();
    
    const index = readIndex();
    const agentName = getAgentName(TARGET_WORKSPACE);
    const learned = checkLearned(index, expName, expVersion, agentName);
    if (learned) {
      console.log('Already learned: ' + expName + ' v' + expVersion);
      console.log('Time: ' + learned.learned_at);
      return;
    }
    
    console.log('Checking dependencies...');
    const deps = checkDependencies(expYml);
    const requiredSkills = handler.getSkills(expYml);
    console.log('Required: ' + (requiredSkills.join(', ') || 'none'));
    if (deps.missing.length > 0) {
      console.log('Missing: ' + deps.missing.join(', '));
    }
    console.log('Satisfied: ' + (deps.satisfied ? 'yes' : 'partial'));
    console.log();
    
    console.log('Analyzing relevance...');
    const relevance = analyzeRelevance(expYml, TARGET_WORKSPACE);
    console.log('Relevance: ' + relevance.relevance);
    console.log();
    
    console.log('Generating plan...');
    const plan = generatePlan(expYml, relevance);
    console.log('Target:');
    plan.targets.forEach(t => console.log('  - ' + t.file + ' (' + t.section + ')'));
    console.log();
    
    const references = readReferences(extractPath, expYml);
    console.log('Change preview:\n');
    const preview = generateChangePreview(expYml, plan, references, TARGET_WORKSPACE);
    displayChangePreview(preview);
    console.log();
    
    const confirmed = await confirmChanges(args);
    if (confirmed === 'save') {
      const savePath = path.join(EXPERIENCES_DIR, 'pending', expName + '-preview.txt');
      ensureDir(path.dirname(savePath));
      let content = 'Package: ' + expName + ' v' + expVersion + '\n\nChanges:\n';
      preview.forEach(item => content += item.file + ': ' + item.newContent + '\n');
      fs.writeFileSync(savePath, content);
      console.log('Saved to: ' + savePath);
      return;
    }
    
    if (!confirmed) {
      console.log('Cancelled');
      return;
    }
    console.log();
    
    console.log('Applying...\n');
    const results = applyLearning(expYml, plan, references);
    
    if (results.success.length > 0) {
      console.log('Success:');
      results.details.filter(d => d.status === 'success').forEach(d => {
        console.log('  ' + d.file + ' (' + d.linesAdded + ' lines)');
      });
      console.log();
    }
    
    const appliedFiles = results.success;
    recordLearning(expYml, appliedFiles);
    
    console.log('Done!\n');
    const verificationGuide = generateVerificationGuide(expYml, results, deps);
    displayVerificationGuide(verificationGuide);
    
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();