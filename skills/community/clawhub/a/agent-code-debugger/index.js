/**
 * Agent Code Debugger - Debugging assistance for AI-generated code
 * 
 * Features:
 * - Pattern detection for common AI-generated code issues
 * - Multi-language support (JavaScript, TypeScript, Python, C#, Java)
 * - Syntax error detection and fix suggestions
 * - Logic error analysis
 * - Security vulnerability scanning
 * - Performance issue detection
 * - IDE integration guidance (VS Code, Visual Studio)
 * - Fix generation with explanations
 * 
 * Usage:
 *   const debugger = require('./skills/agent-code-debugger');
 *   const analysis = debugger.analyze(code, { language: 'csharp' });
 *   const fixes = debugger.suggestFixes(analysis.issues);
 */

/**
 * Common AI-generated code patterns and their issues
 */
const COMMON_PATTERNS = {
  javascript: {
    issues: [
      {
        pattern: /var\s+\w+\s*=\s*require\s*\(\s*['"]\.\/\w+['"]\s*\)\s*;?\s*$/gm,
        name: 'missing_error_handling_require',
        description: 'require() without error handling',
        severity: 'medium',
        fix: 'Wrap require in try-catch or use conditional require'
      },
      {
        pattern: /async\s+function\s+\w+\s*\([^)]*\)\s*\{[^}]*\}(?!\s*catch)/g,
        name: 'async_without_try_catch',
        description: 'Async function without try-catch block',
        severity: 'medium',
        fix: 'Add try-catch block for error handling'
      },
      {
        pattern: /\.then\s*\([^)]*\)\s*;?\s*$/gm,
        name: 'promise_without_catch',
        description: 'Promise chain without .catch()',
        severity: 'high',
        fix: 'Add .catch() handler to promise chain'
      },
      {
        pattern: /console\.log\s*\([^)]*\)\s*;?/g,
        name: 'console_log_leftover',
        description: 'Debug console.log statement left in code',
        severity: 'low',
        fix: 'Remove or replace with proper logging'
      },
      {
        pattern: /==\s*['"]\w+['"]|['"]\w+['"]\s*==/g,
        name: 'loose_equality_string',
        description: 'Loose equality (==) with string, use ===',
        severity: 'medium',
        fix: 'Use strict equality (===) for type-safe comparison'
      }
    ]
  },
  typescript: {
    issues: [
      {
        pattern: /:\s*any\b/g,
        name: 'explicit_any_type',
        description: 'Explicit use of any type defeats type checking',
        severity: 'medium',
        fix: 'Replace with specific type or use unknown'
      },
      {
        pattern: /@ts-ignore/g,
        name: 'ts_ignore_comment',
        description: '@ts-ignore suppresses type errors',
        severity: 'high',
        fix: 'Fix the underlying type error instead of ignoring'
      },
      {
        pattern: /as\s+any\b/g,
        name: 'type_assertion_any',
        description: 'Type assertion to any is unsafe',
        severity: 'medium',
        fix: 'Use proper type guards or validation'
      }
    ]
  },
  python: {
    issues: [
      {
        pattern: /except\s*:/g,
        name: 'bare_except',
        description: 'Bare except catches all exceptions including KeyboardInterrupt',
        severity: 'high',
        fix: 'Use except Exception as e: for specific exception handling'
      },
      {
        pattern: /print\s*\([^)]*\)/g,
        name: 'print_statement_leftover',
        description: 'Debug print statement left in code',
        severity: 'low',
        fix: 'Remove or replace with logging module'
      },
      {
        pattern: /from\s+\w+\s+import\s+\*/g,
        name: 'wildcard_import',
        description: 'Wildcard import pollutes namespace',
        severity: 'medium',
        fix: 'Import specific names: from module import name1, name2'
      },
      {
        pattern: /==\s*None|!=\s*None/g,
        name: 'equality_none',
        description: 'Use "is None" instead of "== None"',
        severity: 'low',
        fix: 'Use "is None" or "is not None" for None comparisons'
      }
    ]
  },
  csharp: {
    issues: [
      {
        pattern: /catch\s*\(\s*\)\s*\{/g,
        name: 'empty_catch',
        description: 'Empty catch block swallows exceptions',
        severity: 'high',
        fix: 'Add exception handling or at least logging'
      },
      {
        pattern: /async\s+void\s+/g,
        name: 'async_void',
        description: 'async void should only be used for event handlers',
        severity: 'high',
        fix: 'Return Task or Task<T> instead of void'
      },
      {
        pattern: /\.Result\s*;?\s*$/gm,
        name: 'task_result_blocking',
        description: '.Result blocks the thread, potential deadlock',
        severity: 'high',
        fix: 'Use await instead of .Result'
      },
      {
        pattern: /\.Wait\s*\(\s*\)/g,
        name: 'task_wait_blocking',
        description: '.Wait() blocks the thread',
        severity: 'high',
        fix: 'Use await instead of .Wait()'
      },
      {
        pattern: /string\.Format\s*\(/g,
        name: 'string_format_verbose',
        description: 'Consider using string interpolation for readability',
        severity: 'low',
        fix: 'Use $"..." string interpolation syntax'
      },
      {
        pattern: /public\s+\w+\s+\w+\s*\{\s*get\s*;\s*set\s*;\s*\}/g,
        name: 'auto_property_no_validation',
        description: 'Auto-property without validation',
        severity: 'medium',
        fix: 'Consider adding validation in setter or constructor'
      },
      {
        pattern: /Console\.WriteLine\s*\([^)]*\)\s*;?/g,
        name: 'console_writeline_leftover',
        description: 'Debug Console.WriteLine left in code',
        severity: 'low',
        fix: 'Remove or replace with proper logging (ILogger, Serilog, etc.)'
      },
      {
        pattern: /Thread\.Sleep\s*\(/g,
        name: 'thread_sleep_blocking',
        description: 'Thread.Sleep blocks the thread',
        severity: 'medium',
        fix: 'Use Task.Delay for async operations'
      }
    ]
  },
  java: {
    issues: [
      {
        pattern: /catch\s*\(\s*Exception\s+\w+\s*\)\s*\{\s*\}/g,
        name: 'empty_catch_exception',
        description: 'Empty catch block swallows all exceptions',
        severity: 'high',
        fix: 'Add proper exception handling or logging'
      },
      {
        pattern: /System\.out\.print(?:ln)?\s*\([^)]*\)\s*;?/g,
        name: 'system_out_print',
        description: 'System.out.print left in code',
        severity: 'low',
        fix: 'Use a logging framework (SLF4J, Log4j, etc.)'
      },
      {
        pattern: /new\s+Thread\s*\(/g,
        name: 'raw_thread_creation',
        description: 'Direct Thread creation, consider ExecutorService',
        severity: 'medium',
        fix: 'Use ExecutorService or thread pool'
      },
      {
        pattern: /\.printStackTrace\s*\(\s*\)/g,
        name: 'print_stack_trace',
        description: 'printStackTrace() is not proper error handling',
        severity: 'medium',
        fix: 'Use proper logging framework'
      }
    ]
  }
};

/**
 * Security vulnerability patterns
 */
const SECURITY_PATTERNS = [
  {
    pattern: /eval\s*\(/g,
    languages: ['javascript', 'typescript'],
    name: 'eval_usage',
    description: 'eval() is dangerous and can execute arbitrary code',
    severity: 'critical',
    fix: 'Avoid eval(), use safer alternatives like JSON.parse() or Function constructor'
  },
  {
    pattern: /innerHTML\s*=/g,
    languages: ['javascript', 'typescript'],
    name: 'inner_html_assignment',
    description: 'innerHTML can lead to XSS vulnerabilities',
    severity: 'high',
    fix: 'Use textContent or sanitize HTML before assignment'
  },
  {
    pattern: /exec\s*\(/g,
    languages: ['python'],
    name: 'exec_usage',
    description: 'exec() can execute arbitrary code',
    severity: 'critical',
    fix: 'Avoid exec(), use safer alternatives'
  },
  {
    pattern: /subprocess\.(?:call|run|Popen)\s*\([^)]*shell\s*=\s*True/g,
    languages: ['python'],
    name: 'shell_true_subprocess',
    description: 'shell=True in subprocess can lead to command injection',
    severity: 'critical',
    fix: 'Avoid shell=True, pass arguments as list'
  },
  {
    pattern: /string\s+sql\s*=\s*["'].*?\+.*?["']/gi,
    languages: ['csharp', 'java'],
    name: 'sql_concatenation',
    description: 'SQL string concatenation can lead to SQL injection',
    severity: 'critical',
    fix: 'Use parameterized queries or prepared statements'
  }
];

/**
 * Analyze code for issues
 */
function analyze(code, options = {}) {
  const language = (options.language || 'javascript').toLowerCase();
  const issues = [];
  
  // Get language-specific patterns
  const langPatterns = COMMON_PATTERNS[language] || COMMON_PATTERNS.javascript;
  
  // Check language-specific issues
  for (const issueDef of langPatterns.issues) {
    const matches = code.matchAll(issueDef.pattern);
    for (const match of matches) {
      issues.push({
        type: issueDef.name,
        description: issueDef.description,
        severity: issueDef.severity,
        line: getLineNumber(code, match.index),
        column: getColumnNumber(code, match.index),
        match: match[0],
        fix: issueDef.fix,
        category: 'code_quality'
      });
    }
  }
  
  // Check security issues
  for (const secPattern of SECURITY_PATTERNS) {
    if (secPattern.languages.includes(language)) {
      const matches = code.matchAll(secPattern.pattern);
      for (const match of matches) {
        issues.push({
          type: secPattern.name,
          description: secPattern.description,
          severity: secPattern.severity,
          line: getLineNumber(code, match.index),
          column: getColumnNumber(code, match.index),
          match: match[0],
          fix: secPattern.fix,
          category: 'security'
        });
      }
    }
  }
  
  // Sort by severity
  const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  issues.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);
  
  return {
    language,
    totalIssues: issues.length,
    criticalCount: issues.filter(i => i.severity === 'critical').length,
    highCount: issues.filter(i => i.severity === 'high').length,
    mediumCount: issues.filter(i => i.severity === 'medium').length,
    lowCount: issues.filter(i => i.severity === 'low').length,
    issues,
    summary: generateSummary(issues)
  };
}

/**
 * Get line number from index
 */
function getLineNumber(code, index) {
  const lines = code.substring(0, index).split('\n');
  return lines.length;
}

/**
 * Get column number from index
 */
function getColumnNumber(code, index) {
  const lines = code.substring(0, index).split('\n');
  return lines[lines.length - 1].length + 1;
}

/**
 * Generate summary of issues
 */
function generateSummary(issues) {
  if (issues.length === 0) {
    return 'No issues found. Code looks clean!';
  }
  
  const critical = issues.filter(i => i.severity === 'critical').length;
  const high = issues.filter(i => i.severity === 'high').length;
  const medium = issues.filter(i => i.severity === 'medium').length;
  const low = issues.filter(i => i.severity === 'low').length;
  
  const parts = [];
  if (critical > 0) parts.push(`${critical} critical`);
  if (high > 0) parts.push(`${high} high`);
  if (medium > 0) parts.push(`${medium} medium`);
  if (low > 0) parts.push(`${low} low`);
  
  return `Found ${issues.length} issue(s): ${parts.join(', ')}`;
}

/**
 * Suggest fixes for issues
 */
function suggestFixes(issues, options = {}) {
  return issues.map(issue => ({
    ...issue,
    fixSuggestion: generateFixSuggestion(issue, options)
  }));
}

/**
 * Generate fix suggestion
 */
function generateFixSuggestion(issue, options = {}) {
  const suggestions = {
    empty_catch: {
      csharp: `// Before:
catch { }

// After:
catch (Exception ex) {
    _logger.LogError(ex, "Error occurred in {MethodName}", nameof(YourMethod));
    throw; // or handle appropriately
}`,
      java: `// Before:
catch (Exception e) { }

// After:
catch (Exception e) {
    log.error("Error occurred", e);
    throw e; // or handle appropriately
}`
    },
    async_void: {
      csharp: `// Before:
public async void DoWork() { }

// After:
public async Task DoWorkAsync() { }

// For event handlers only:
public async void OnButtonClick(object sender, EventArgs e) { }`
    },
    task_result_blocking: {
      csharp: `// Before:
var result = SomeAsyncMethod().Result;

// After:
var result = await SomeAsyncMethod();

// If not in async context, use:
var result = await SomeAsyncMethod().ConfigureAwait(false);`
    },
    console_writeline_leftover: {
      csharp: `// Before:
Console.WriteLine($"Debug: {value}");

// After (using ILogger):
_logger.LogInformation("Processing value: {Value}", value);

// Or remove if not needed`
    }
  };
  
  return suggestions[issue.type]?.[options.language || 'csharp'] || issue.fix;
}

/**
 * Get Visual Studio debugging guidance
 */
function getVisualStudioGuidance(language = 'csharp') {
  const guidance = {
    csharp: {
      breakpoints: 'Set breakpoints by clicking in the left margin or pressing F9',
      watchWindow: 'Use Debug > Windows > Watch to monitor variables',
      immediateWindow: 'Use Debug > Windows > Immediate for evaluating expressions',
      callStack: 'Use Debug > Windows > Call Stack to trace execution',
      exceptions: 'Debug > Windows > Exception Settings to break on specific exceptions',
      attach: 'Debug > Attach to Process to debug running applications',
      tips: [
        'Use [Conditional("DEBUG")] for debug-only code',
        'Add Debugger.Break() for programmatic breakpoints',
        'Use DebuggerDisplay attribute for custom object display',
        'Enable "Just My Code" in Debug options for cleaner debugging',
        'Use IntelliTrace for historical debugging (Enterprise edition)'
      ]
    },
    typescript: {
      breakpoints: 'Set breakpoints in .ts files, VS will map to compiled JS',
      launchConfig: 'Create launch.json for Node.js or browser debugging',
      watchWindow: 'Use Debug > Windows > Watch for variable monitoring',
      tips: [
        'Enable source maps in tsconfig.json',
        'Use debugger; statement for programmatic breakpoints',
        'Configure launch.json for different environments'
      ]
    }
  };
  
  return guidance[language] || guidance.csharp;
}

/**
 * Generate debug configuration for VS Code / Visual Studio
 */
function generateDebugConfig(language, options = {}) {
  const configs = {
    csharp: {
      visualStudio: {
        name: '.NET Core Launch',
        type: 'coreclr',
        request: 'launch',
        preLaunchTask: 'build',
        program: '${workspaceFolder}/bin/Debug/net8.0/YourApp.dll',
        args: [],
        cwd: '${workspaceFolder}',
        console: 'internalConsole',
        stopAtEntry: false,
        env: {
          ASPNETCORE_ENVIRONMENT: 'Development'
        }
      },
      vscode: {
        version: '0.2.0',
        configurations: [{
          name: '.NET Core Launch (console)',
          type: 'coreclr',
          request: 'launch',
          preLaunchTask: 'build',
          program: '${workspaceFolder}/bin/Debug/net8.0/YourApp.dll',
          args: [],
          cwd: '${workspaceFolder}',
          console: 'internalConsole',
          stopAtEntry: false
        }]
      }
    },
    typescript: {
      vscode: {
        version: '0.2.0',
        configurations: [{
          type: 'node',
          request: 'launch',
          name: 'Launch Program',
          skipFiles: ['<node_internals>/**'],
          program: '${workspaceFolder}/src/index.ts',
          outFiles: ['${workspaceFolder}/dist/**/*.js'],
          preLaunchTask: 'tsc: build - tsconfig.json'
        }]
      }
    },
    python: {
      vscode: {
        version: '0.2.0',
        configurations: [{
          name: 'Python: Current File',
          type: 'python',
          request: 'launch',
          program: '${file}',
          console: 'integratedTerminal'
        }]
      }
    }
  };
  
  return configs[language] || configs.csharp;
}

/**
 * Detect common AI-generated code characteristics
 */
function detectAIPatterns(code) {
  const patterns = [];
  
  // Check for common AI generation markers
  if (/\/\/\s*(TODO|FIXME|NOTE|HACK):/gi.test(code)) {
    patterns.push({
      type: 'todo_comments',
      description: 'Contains TODO/FIXME comments typical of AI-generated code',
      suggestion: 'Review and address or remove placeholder comments'
    });
  }
  
  if (/function\s*\(\s*\)\s*\{[\s\S]*\}/.test(code) && code.split('function').length > 5) {
    patterns.push({
      type: 'many_functions',
      description: 'Many function definitions, possible over-engineering',
      suggestion: 'Consider if all functions are necessary or can be consolidated'
    });
  }
  
  if (/\/\*\*[\s\S]*?\*\//g.test(code)) {
    const docComments = code.match(/\/\*\*[\s\S]*?\*\//g) || [];
    if (docComments.length > 3) {
      patterns.push({
        type: 'excessive_documentation',
        description: 'Many JSDoc/doc comments, typical of AI generation',
        suggestion: 'Keep useful documentation, remove redundant comments'
      });
    }
  }
  
  if (/^(\/\/|\/\*|\*|#)/gm.test(code) && code.split('\n').filter(l => l.trim().startsWith('//') || l.trim().startsWith('#') || l.trim().startsWith('*')).length > code.split('\n').length * 0.3) {
    patterns.push({
      type: 'comment_heavy',
      description: 'Heavy commenting, possibly over-explained',
      suggestion: 'Reduce comments, let code speak for itself'
    });
  }
  
  return patterns;
}

/**
 * Quick fix for common issues
 */
function quickFix(code, issueType, options = {}) {
  const fixes = {
    console_writeline_leftover: (code) => {
      return code.replace(/Console\.WriteLine\s*\([^)]*\)\s*;?/g, '');
    },
    console_log_leftover: (code) => {
      return code.replace(/console\.log\s*\([^)]*\)\s*;?/g, '');
    },
    print_statement_leftover: (code) => {
      return code.replace(/print\s*\([^)]*\)/g, '');
    },
    system_out_print: (code) => {
      return code.replace(/System\.out\.print(?:ln)?\s*\([^)]*\)\s*;?/g, '');
    }
  };
  
  const fixFn = fixes[issueType];
  if (fixFn) {
    return {
      original: code,
      fixed: fixFn(code),
      applied: true
    };
  }
  
  return {
    original: code,
    fixed: code,
    applied: false,
    message: `No automatic fix available for ${issueType}`
  };
}

/**
 * Generate debugging report
 */
function generateReport(analysis, options = {}) {
  const lines = [];
  
  lines.push('# Code Analysis Report');
  lines.push('');
  lines.push(`**Language:** ${analysis.language}`);
  lines.push(`**Total Issues:** ${analysis.totalIssues}`);
  lines.push('');
  
  if (analysis.criticalCount > 0) {
    lines.push(`🔴 **Critical:** ${analysis.criticalCount}`);
  }
  if (analysis.highCount > 0) {
    lines.push(`🟠 **High:** ${analysis.highCount}`);
  }
  if (analysis.mediumCount > 0) {
    lines.push(`🟡 **Medium:** ${analysis.mediumCount}`);
  }
  if (analysis.lowCount > 0) {
    lines.push(`🟢 **Low:** ${analysis.lowCount}`);
  }
  
  lines.push('');
  lines.push('---');
  lines.push('');
  
  if (analysis.issues.length > 0) {
    lines.push('## Issues');
    lines.push('');
    
    for (const issue of analysis.issues) {
      const emoji = {
        critical: '🔴',
        high: '🟠',
        medium: '🟡',
        low: '🟢'
      }[issue.severity];
      
      lines.push(`### ${emoji} ${issue.type}`);
      lines.push('');
      lines.push(`**Line ${issue.line}:** ${issue.description}`);
      lines.push(`**Fix:** ${issue.fix}`);
      lines.push('');
    }
  } else {
    lines.push('✅ No issues found!');
  }
  
  return lines.join('\n');
}

module.exports = {
  analyze,
  suggestFixes,
  getVisualStudioGuidance,
  generateDebugConfig,
  detectAIPatterns,
  quickFix,
  generateReport,
  COMMON_PATTERNS,
  SECURITY_PATTERNS
};
