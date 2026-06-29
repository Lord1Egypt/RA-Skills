/**
 * Self Modifier - 自我代码修正模块
 * 接收修改建议，生成代码补丁
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const os = require('os');

const MAX_PATCH_SIZE = 1024 * 100; // 补丁文件最大 100KB
const AUDIT_LOG_FILE = 'self-modifier-audit.log';

class SelfModifier {
  constructor(projectRoot) {
    this.projectRoot = projectRoot;
    this.configFile = path.join(projectRoot, '.opencode', 'config.json');
    this.patchDir = path.join(projectRoot, 'logs', 'patches');
    this.enabled = this.isEnabled();
    this.changeLog = path.join(projectRoot, 'logs', 'self-modifier.log');
    this.patchDir = path.join(projectRoot, 'patches');
    this.auditLogPath = path.join(projectRoot, 'logs', AUDIT_LOG_FILE);
    this.init();

    // 启动时警告：此功能仅适用于沙箱/开发环境
    if (this.enabled) {
      console.warn('[SelfModifier] 警告: 自我修改已启用。此功能仅适用于沙箱/开发环境，'
        + '不建议在生产环境中使用。设置 HEARTFLOW_ENABLE_SELF_MODIFICATION=0 可禁用。');
    }
  }

  init() {
    fs.mkdirSync(this.patchDir, { recursive: true });
    try { fs.chmodSync(this.patchDir, 0o700); } catch (e) { /* best effort */ }
  }

  isEnabled() {
    try {
      if (fs.existsSync(this.configFile)) {
        const config = JSON.parse(fs.readFileSync(this.configFile, 'utf8'));
        return config.selfModificationEnabled === true;
      }
    } catch (e) {}
    return false;
  }

  /**
   * 执行修改
   */
  applyModification(suggestion) {
    if (!this.enabled) {
      return {
        success: false,
        reason: 'self_modification_disabled',
        message: '自我修改功能已关闭，请在 config.json 中启用'
      };
    }

    const { targetFile, functionName, newBehavior } = this.parseSuggestion(suggestion);
    
    if (!targetFile || !functionName) {
      return {
        success: false,
        reason: 'invalid_suggestion',
        message: '无法解析修改建议'
      };
    }

    const fullPath = path.join(this.projectRoot, targetFile);
    
    if (!fs.existsSync(fullPath)) {
      return {
        success: false,
        reason: 'file_not_found',
        message: `文件不存在: ${targetFile}`
      };
    }

    const originalCode = fs.readFileSync(fullPath, 'utf8');
    const modifiedCode = this.generatePatch(originalCode, functionName, newBehavior);
    
    const diff = this.generateDiff(originalCode, modifiedCode, targetFile);
    
    this.savePatch(diff, targetFile);

    return {
      success: true,
      targetFile: targetFile,
      function: functionName,
      diff: diff,
      patchFile: `${this.patchDir}/${this.getPatchFilename(targetFile)}`,
      message: '补丁已生成，请在验证后手动应用'
    };
  }

  /**
   * 解析修改建议
   */
  parseSuggestion(suggestion) {
    const suggestionStr = typeof suggestion === 'string' ? suggestion : 
                         suggestion.suggestion || suggestion.description || '';

    const patterns = [
      /修改\s+([^\s]+)\s+中的\s+([^\s]+)\s+函数/,
      /modify\s+([^\s]+)\s+.*?\s+([^\s]+)\s+function/,
      /update\s+([^\s]+)\s+.*?\s+([^\s]+)/,
      /change\s+([^\s]+)\s+.*?\s+([^\s]+)/
    ];

    for (const pattern of patterns) {
      const match = suggestionStr.match(pattern);
      if (match) {
        return {
          targetFile: match[1],
          functionName: match[2],
          newBehavior: suggestionStr
        };
      }
    }

    return {
      targetFile: 'src/core/clarity.js',
      functionName: 'setTuning',
      newBehavior: suggestionStr
    };
  }

  /**
   * 生成补丁代码
   */
  generatePatch(originalCode, functionName, newBehavior) {
    const functionPattern = new RegExp(
      `(function\\s+${functionName}|const\\s+${functionName}\\s*=|let\\s+${functionName}\\s*=|var\\s+${functionName}\\s*=)`,
      'g'
    );

    if (!functionPattern.test(originalCode)) {
      return originalCode + '\n\n// New function: ' + functionName + '\n// ' + newBehavior;
    }

    const enhancement = this.generateEnhancement(functionName, newBehavior);
    
    return originalCode.replace(
      functionPattern,
      `$1${enhancement}`
    );
  }

  /**
   * 生成增强代码
   */
  generateEnhancement(functionName, newBehavior) {
    const enhancements = {
      'calculatePAD': `
  // Self-Modifier: 增加对用户挫败感的敏感度
  const frustrationIndicators = ['difficult', 'hard', 'frustrated', '挫败', '难', '不行'];
  const hasFrustration = context?.userInput?.some(input => 
    frustrationIndicators.some(indicator => input.toLowerCase().includes(indicator))
  );
  if (hasFrustration) {
    pad.pleasure -= 0.2;
    pad.dominance -= 0.1;
  }
`,
      'default': `
  // Self-Modifier enhancement based on: ${newBehavior.substring(0, 50)}...
`
    };

    return enhancements[functionName] || enhancements.default;
  }

  /**
   * 生成差异
   */
  generateDiff(original, modified, filename) {
    const originalLines = original.split('\n');
    const modifiedLines = modified.split('\n');
    
    const diff = {
      filename: filename,
      timestamp: new Date().toISOString(),
      original: {
        lines: originalLines.length,
        hash: crypto.createHash('sha256').update(original).digest('hex')
      },
      modified: {
        lines: modifiedLines.length,
        hash: crypto.createHash('sha256').update(modified).digest('hex')
      },
      changes: [],
      unifiedDiff: this.generateUnifiedDiff(original, modified, filename)
    };

    let lineNum = 0;
    const maxLines = Math.max(originalLines.length, modifiedLines.length);
    
    for (let i = 0; i < maxLines; i++) {
      const origLine = originalLines[i] || '';
      const modLine = modifiedLines[i] || '';
      
      if (origLine !== modLine) {
        diff.changes.push({
          line: i + 1,
          original: origLine.substring(0, 80),
          modified: modLine.substring(0, 80)
        });
      }
    }

    return diff;
  }

  /**
   * 生成统一格式差异
   */
  generateUnifiedDiff(original, modified, filename) {
    const lines = [
      `--- a/${filename}`,
      `+++ b/${filename}`,
      `@@ @@`
    ];

    const origLines = original.split('\n');
    const modLines = modified.split('\n');
    
    let i = 0;
    while (i < Math.max(origLines.length, modLines.length)) {
      const orig = origLines[i] || '';
      const mod = modLines[i] || '';
      
      if (orig !== mod) {
        if (orig) lines.push(`-${orig}`);
        if (mod) lines.push(`+${mod}`);
      } else {
        lines.push(` ${orig}`);
      }
      i++;
    }

    return lines.join('\n');
  }

  /**
   * 保存补丁
   */
  savePatch(diff, targetFile) {
    const patchFile = path.join(this.patchDir, this.getPatchFilename(targetFile));
    fs.writeFileSync(patchFile, diff.unifiedDiff);
    try { fs.chmodSync(patchFile, 0o600); } catch (e) { /* best effort */ }

    const metaFile = patchFile.replace('.diff', '.json');
    fs.writeFileSync(metaFile, JSON.stringify(diff, null, 2));
    try { fs.chmodSync(metaFile, 0o600); } catch (e) { /* best effort */ }
  }

  getPatchFilename(targetFile) {
    const name = targetFile.replace(/[^a-zA-Z0-9]/g, '_');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    return `${name}_${timestamp}.diff`;
  }

  /**
   * 列出补丁历史
   */
  listPatches() {
    if (!fs.existsSync(this.patchDir)) {
      return [];
    }

    return fs.readdirSync(this.patchDir)
      .filter(f => f.endsWith('.json'))
      .map(f => {
        const fullPath = path.join(this.patchDir, f);
        const stat = fs.statSync(fullPath);
        return {
          file: f,
          created: stat.mtime.toISOString()
        };
      })
      .sort((a, b) => new Date(b.created) - new Date(a.created));
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      enabled: this.enabled,
      configFile: this.configFile,
      patchesGenerated: this.listPatches().length
    };
  }

  /**
   * 写入审计日志（结构化安全事件记录）
   */
  _auditLog(entry) {
    try {
      const logDir = path.dirname(this.auditLogPath);
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      const logEntry = JSON.stringify({
        timestamp: new Date().toISOString(),
        event: entry.event,
        file: entry.file,
        source: 'self-modifier',
        details: entry.details || {}
      }) + '\n';
      fs.appendFileSync(this.auditLogPath, logEntry);
    } catch (e) {
      // 审计日志不可中断主逻辑
    }
  }

  /**
   * 普通日志
   */
  _log(msg) {
    console.log(`[SelfModifier] ${msg}`);
  }

  /**
   * 启用功能
   */
  async metacognitiveModify(suggestion) {
    if (!this.enabled) {
      return {
        success: false,
        reason: 'self_modification_disabled',
        action: 'generate_patch_only'
      };
    }

    this._log(`元认知修改: ${suggestion.type || 'unknown'}`);
    this._auditLog({ event: 'metacognitive_modify_attempt', file: suggestion.file || 'unknown', details: { type: suggestion.type } });

    const parsed = this.parseSuggestion(suggestion);
    if (!parsed) {
      this._auditLog({ event: 'metacognitive_modify_failed', file: 'unknown', details: { reason: 'cannot_parse_suggestion' } });
      return { success: false, reason: 'cannot_parse_suggestion' };
    }

    const filePath = path.join(this.projectRoot, parsed.file);
    if (!fs.existsSync(filePath)) {
      this._auditLog({ event: 'metacognitive_modify_failed', file: parsed.file, details: { reason: 'file_not_found' } });
      return { success: false, reason: 'file_not_found', path: parsed.file };
    }

    const originalContent = fs.readFileSync(filePath, 'utf8');
    const modifiedContent = this.applyModification(originalContent, parsed);

    if (modifiedContent === originalContent) {
      return { success: false, reason: 'no_changes_made' };
    }

    const patch = this.generatePatch(originalContent, modifiedContent, parsed);

    // 检查补丁大小
    if (Buffer.byteLength(patch, 'utf8') > MAX_PATCH_SIZE) {
      this._auditLog({ event: 'patch_rejected_size', file: parsed.file, details: { size: Buffer.byteLength(patch, 'utf8') } });
      return { success: false, reason: 'patch_too_large', message: `补丁文件超过 ${MAX_PATCH_SIZE / 1024}KB 限制` };
    }

    const patchFileName = `self-mod-${Date.now()}.patch`;
    // 在审批前写入临时目录，而非 patches/
    const tempDir = os.tmpdir();
    const tempPatchPath = path.join(tempDir, patchFileName);

    fs.writeFileSync(tempPatchPath, patch);
    try { fs.chmodSync(tempPatchPath, 0o600); } catch (e) { /* best effort */ }

    this._auditLog({ event: 'patch_generated_temp', file: parsed.file, details: { patchFile: patchFileName, tempPath: tempPatchPath } });

    this.recordChange({
      file: parsed.file,
      suggestion: suggestion.type,
      timestamp: new Date().toISOString(),
      action: 'patch_generated',
      patchFile: patchFileName,
      requiresApproval: true
    });

    this._log(`补丁已生成: ${patchFileName} (需要用户审批)`);
    this._auditLog({ event: 'patch_pending_approval', file: parsed.file, details: { patchFile: patchFileName } });

    return {
      success: true,
      action: 'patch_generated',
      patchFile: patchFileName,
      patchPath: tempPatchPath,
      description: this.describeChanges(originalContent, modifiedContent),
      requiresApproval: true,
      instructions: `请审查 ${tempPatchPath} 中的补丁文件，运行 applyApprovedPatch() 应用`
    };
  }

  generatePatch(original, modified, parsed) {
    const timestamp = new Date().toISOString();
    const diff = this.computeSimpleDiff(original, modified);
    
    const patch = `# Self-Modifier 补丁文件
# 生成时间: ${timestamp}
# 目标文件: ${parsed.file}
# 修改类型: ${parsed.type || 'unknown'}
#
# 审查后使用以下命令应用:
#   patch -p1 < patches/${`self-mod-${Date.now()}.patch`}
#
# 撤销补丁:
#   patch -R -p1 < patches/${`self-mod-${Date.now()}.patch`}
#
# ============================================================================
--- a/${parsed.file}
+++ b/${parsed.file}
${diff}
`;

    return patch;
  }

  computeSimpleDiff(original, modified) {
    const origLines = original.split('\n');
    const modLines = modified.split('\n');
    let diff = '';
    let lineNum = 0;

    for (let i = 0; i < Math.max(origLines.length, modLines.length); i++) {
      lineNum = i + 1;
      const origLine = origLines[i] || '';
      const modLine = modLines[i] || '';

      if (origLine !== modLine) {
        if (origLine && !modLine) {
          diff += `@@ -${lineNum},1 +${lineNum},0 @@\n-${origLine}\n`;
        } else if (!origLine && modLine) {
          diff += `@@ -${lineNum},0 +${lineNum},1 @@\n+${modLine}\n`;
        } else {
          diff += `@@ -${lineNum},1 +${lineNum},1 @@\n-${origLine}\n+${modLine}\n`;
        }
      }
    }

    return diff || '(无差异 - 可能为格式调整)';
  }

  /**
   * 列出待审批的补丁文件
   */
  listPendingPatches() {
    const patches = [];
    try {
      // 从 patches/ 目录
      if (fs.existsSync(this.patchDir)) {
        const fromPatches = fs.readdirSync(this.patchDir)
          .filter(f => f.endsWith('.patch'))
          .map(f => {
            const stat = fs.statSync(path.join(this.patchDir, f));
            return {
              file: f,
              created: stat.mtime.toISOString(),
              size: stat.size,
              source: 'patches'
            };
          });
        patches.push(...fromPatches);
      }

      // 从临时目录
      const tmpDir = os.tmpdir();
      const tmpFiles = fs.readdirSync(tmpDir)
        .filter(f => f.startsWith('self-mod-') && f.endsWith('.patch'))
        .map(f => {
          const stat = fs.statSync(path.join(tmpDir, f));
          return {
            file: f,
            created: stat.mtime.toISOString(),
            size: stat.size,
            source: 'tmpdir'
          };
        });
      patches.push(...tmpFiles);

      return patches.sort((a, b) => new Date(b.created) - new Date(a.created));
    } catch (e) {
      return [];
    }
  }

  /**
   * 应用已审批的补丁
   */
  async applyApprovedPatch(patchFileName) {
    // 先在临时目录中查找，再在 patches/ 中查找
    let patchPath = path.join(os.tmpdir(), patchFileName);
    let sourceIsTemp = true;

    if (!fs.existsSync(patchPath)) {
      patchPath = path.join(this.patchDir, patchFileName);
      sourceIsTemp = false;
    }

    if (!fs.existsSync(patchPath)) {
      this._auditLog({ event: 'patch_apply_failed', file: patchFileName, details: { reason: 'patch_not_found' } });
      return { success: false, reason: 'patch_not_found' };
    }

    try {
      const patchContent = fs.readFileSync(patchPath, 'utf8');

      // 补丁大小检查
      if (Buffer.byteLength(patchContent, 'utf8') > MAX_PATCH_SIZE) {
        this._auditLog({ event: 'patch_apply_rejected_size', file: patchFileName, details: { size: Buffer.byteLength(patchContent, 'utf8') } });
        return { success: false, reason: 'patch_too_large' };
      }

      const targetFile = this.extractTargetFromPatch(patchContent);

      if (!targetFile) {
        this._auditLog({ event: 'patch_apply_failed', file: patchFileName, details: { reason: 'invalid_patch_format' } });
        return { success: false, reason: 'invalid_patch_format' };
      }

      const targetPath = path.join(this.projectRoot, targetFile);
      if (!fs.existsSync(targetPath)) {
        this._auditLog({ event: 'patch_apply_failed', file: targetFile, details: { reason: 'target_file_not_found' } });
        return { success: false, reason: 'target_file_not_found' };
      }

      const originalContent = fs.readFileSync(targetPath, 'utf8');
      const modifiedContent = this.applyPatchToContent(originalContent, patchContent);

      fs.writeFileSync(targetPath, modifiedContent);
      try { fs.chmodSync(targetPath, 0o600); } catch (e) { /* best effort */ }

      // 补丁已审批，复制到 patches/ 留存审计
      if (sourceIsTemp) {
        const archivedPatch = path.join(this.patchDir, patchFileName);
        fs.copyFileSync(patchPath, archivedPatch);
        try { fs.chmodSync(archivedPatch, 0o600); } catch (e) { /* best effort */ }
        // 从临时目录清理
        try { fs.unlinkSync(patchPath); } catch (e) { /* ignore */ }
      }

      this.recordChange({
        file: targetFile,
        action: 'patch_applied',
        patchFile: patchFileName,
        timestamp: new Date().toISOString()
      });

      this._auditLog({
        event: 'patch_applied',
        file: targetFile,
        details: { patchFile: patchFileName, source: sourceIsTemp ? 'tmpdir' : 'patches' }
      });

      this._log(`已应用审批补丁: ${patchFileName}`);

      return {
        success: true,
        file: targetFile,
        description: this.describeChanges(originalContent, modifiedContent)
      };
    } catch (e) {
      this._auditLog({ event: 'patch_apply_error', file: patchFileName, details: { error: e.message } });
      return { success: false, error: e.message };
    }
  }

  extractTargetFromPatch(patchContent) {
    const match = patchContent.match(/^\+\+\+ b\/(.+)$/m);
    return match ? match[1] : null;
  }

  applyPatchToContent(content, patchContent) {
    const lines = content.split('\n');
    const patchLines = patchContent.split('\n');
    let result = [...lines];
    let offset = 0;

    for (const line of patchLines) {
      if (line.startsWith('+') && !line.startsWith('+++')) {
        const insertLine = line.substring(1);
        result.splice(offset, 0, insertLine);
        offset++;
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        result.splice(offset, 1);
      } else if (line.startsWith('@@')) {
        // 跳过 hunk 头
      }
    }

    return result.join('\n');
  }

  /**
   * 拒绝并删除补丁
   */
  rejectPatch(patchFileName) {
    // 尝试 patches/ 和 tmpdir 两处清理
    let found = false;

    const patchPath = path.join(this.patchDir, patchFileName);
    if (fs.existsSync(patchPath)) {
      fs.unlinkSync(patchPath);
      found = true;
    }

    const tempPath = path.join(os.tmpdir(), patchFileName);
    if (fs.existsSync(tempPath)) {
      fs.unlinkSync(tempPath);
      found = true;
    }

    if (!found) {
      return { success: false, reason: 'patch_not_found' };
    }

    this.recordChange({
      action: 'patch_rejected',
      patchFile: patchFileName,
      timestamp: new Date().toISOString()
    });

    this._auditLog({
      event: 'patch_rejected',
      file: patchFileName,
      details: { reason: 'user_rejected' }
    });

    this._log(`已拒绝并删除补丁: ${patchFileName}`);

    return { success: true };
  }

  enable() {
    this.setConfig(true);
    this.enabled = true;
  }

  /**
   * 禁用功能
   */
  disable() {
    this.setConfig(false);
    this.enabled = false;
  }

  setConfig(enabled) {
    try {
      let config = {};
      if (fs.existsSync(this.configFile)) {
        config = JSON.parse(fs.readFileSync(this.configFile, 'utf8'));
      }
      config.selfModificationEnabled = enabled;
      fs.writeFileSync(this.configFile, JSON.stringify(config, null, 2));
      try { fs.chmodSync(this.configFile, 0o600); } catch (e) { /* best effort */ }
    } catch (e) {
      console.error('[SelfModifier] 配置更新失败:', e.message);
    }
  }
}

/**
 * CLI 入口
 */
if (require.main === module) {
  const modifier = new SelfModifier(process.cwd());
  
  console.log('=== Self Modifier ===');
  console.log('状态:', modifier.getStatus().enabled ? '已启用' : '已禁用');
  
  if (modifier.enabled) {
    const testSuggestion = {
      targetFile: 'src/core/clarity.js',
      functionName: 'start',
      suggestion: '修改 start 函数，增强启动可靠性'
    };
    
    const result = modifier.applyModification(testSuggestion);
    console.log('结果:', result.success ? '成功' : result.message);
    if (result.success) {
      console.log('补丁文件:', result.patchFile);
    }
  } else {
    console.log('请在 config.json 中设置 selfModificationEnabled: true 来启用');
  }
}

module.exports = { SelfModifier };
