// File Classification Manager - Main Module
const path = require('path');
const fs = require('fs').promises;

class FileClassificationManager {
  constructor(workspaceRoot = process.env.OPENCLAW_WORKSPACE || '.') {
    this.workspaceRoot = workspaceRoot;
    this.projectsDir = path.join(workspaceRoot, 'projects');
    this.tempDir = path.join(workspaceRoot, 'temp');
  }

  // Ensure project directory structure exists
  async ensureProjectStructure(projectName) {
    const projectOutputDir = path.join(this.projectsDir, projectName, 'outputs');
    const projectAssetsDir = path.join(this.projectsDir, projectName, 'assets');
    const tempIntermediateDir = path.join(this.tempDir, projectName, 'intermediate');
    const tempCacheDir = path.join(this.tempDir, projectName, 'cache');

    await Promise.all([
      fs.mkdir(projectOutputDir, { recursive: true }),
      fs.mkdir(projectAssetsDir, { recursive: true }),
      fs.mkdir(tempIntermediateDir, { recursive: true }),
      fs.mkdir(tempCacheDir, { recursive: true })
    ]);

    return {
      outputs: projectOutputDir,
      assets: projectAssetsDir,
      intermediate: tempIntermediateDir,
      cache: tempCacheDir
    };
  }

  // Classify file type and determine destination
  classifyFileType(filename) {
    const basename = path.basename(filename).toLowerCase();
    
    // Final output files (reports, reviews, summaries)
    if (basename.includes('review') && filename.endsWith('.md')) {
      return 'output';
    }
    if (basename.includes('final') && filename.endsWith('.md')) {
      return 'output';
    }
    if (basename.includes('comprehensive') && filename.endsWith('.md')) {
      return 'output';
    }
    if (basename.includes('summary') && filename.endsWith('.md')) {
      return 'output';
    }

    // Script files
    if (filename.endsWith('.py') || filename.endsWith('.js') || filename.endsWith('.m')) {
      return 'intermediate';
    }

    // Extracted content files
    if (basename.includes('content') && filename.endsWith('.txt')) {
      return 'intermediate';
    }
    if (basename.includes('extract') && filename.endsWith('.txt')) {
      return 'intermediate';
    }

    // Document files
    if (filename.endsWith('.pdf') || filename.endsWith('.docx')) {
      return 'intermediate';
    }

    // Data files
    if (filename.endsWith('.mat') || filename.endsWith('.csv') || filename.endsWith('.json')) {
      return 'intermediate';
    }

    // Image files
    if (filename.endsWith('.png') || filename.endsWith('.jpg') || filename.endsWith('.jpeg') || filename.endsWith('.gif')) {
      return 'intermediate';
    }

    // Default to intermediate for unknown types
    return 'intermediate';
  }

  // Route file to appropriate directory
  async classifyAndRouteFile(filepath, projectContext) {
    const fileType = this.classifyFileType(filepath);
    const filename = path.basename(filepath);
    
    // Ensure project structure exists
    const dirs = await this.ensureProjectStructure(projectContext);
    
    let destinationPath;
    if (fileType === 'output') {
      destinationPath = path.join(dirs.outputs, filename);
    } else {
      destinationPath = path.join(dirs.intermediate, filename);
    }

    // Move the file
    await fs.rename(filepath, destinationPath);
    
    return destinationPath;
  }

  // Detect project from file content (basic implementation)
  detectProjectFromContent(content) {
    // This is a placeholder - in real implementation would use NLP
    // to extract project-relevant keywords
    const keywords = ['dipleg', 'pv', 'sofc', 'ice', 'format', 'course', 'proposal', 'share'];
    
    for (const keyword of keywords) {
      if (content.toLowerCase().includes(keyword)) {
        return keyword + '_project';
      }
    }
    
    return 'general';
  }

  // Cleanup workspace root
  async cleanupWorkspaceRoot() {
    const files = await fs.readdir(this.workspaceRoot);
    const movedFiles = [];
    const errors = [];

    for (const file of files) {
      const fullPath = path.join(this.workspaceRoot, file);
      const stat = await fs.stat(fullPath);
      
      // Skip directories and system files
      if (stat.isDirectory()) continue;
      if (['AGENTS.md', 'SOUL.md', 'USER.md', 'IDENTITY.md', 'HEARTBEAT.md', 'TOOLS.md', 'README.md'].includes(file)) {
        continue;
      }

      try {
        // Read file content to detect project
        const content = await fs.readFile(fullPath, 'utf8');
        const project = this.detectProjectFromContent(content);
        
        const newPath = await this.classifyAndRouteFile(fullPath, project);
        movedFiles.push({ original: fullPath, new: newPath });
      } catch (error) {
        errors.push({ file, error: error.message });
      }
    }

    return { movedFiles, errors };
  }
}

module.exports = FileClassificationManager;