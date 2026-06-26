---
name: agent-code-debugger
description: Provides debugging assistance for AI-generated code with pattern detection, common issue identification, and fix suggestions across multiple programming languages including C#/.NET Core and Visual Studio integration guidance.
---

# Agent Code Debugger

Debugging assistance for AI-generated code with multi-language support.

## When to Use

- Debugging AI-generated code
- Analyzing code for common AI generation issues
- Getting Visual Studio debugging guidance
- Detecting security vulnerabilities in generated code
- Quick fixes for common code issues

## Usage

```javascript
const debugger = require('./skills/agent-code-debugger');

// Analyze code for issues
const analysis = debugger.analyze(code, { language: 'csharp' });
console.log(analysis.summary);

// Get fix suggestions
const fixes = debugger.suggestFixes(analysis.issues);

// Get Visual Studio guidance
const guidance = debugger.getVisualStudioGuidance('csharp');

// Generate debug configuration
const config = debugger.generateDebugConfig('csharp');

// Quick fix common issues
const fixed = debugger.quickFix(code, 'console_writeline_leftover');
```

## API

### `analyze(code, options?)`

Analyze code for issues.

```javascript
const analysis = analyze(csharpCode, { language: 'csharp' });
// {
//   language: 'csharp',
//   totalIssues: 5,
//   criticalCount: 0,
//   highCount: 2,
//   mediumCount: 2,
//   lowCount: 1,
//   issues: [...],
//   summary: 'Found 5 issue(s): 2 high, 2 medium, 1 low'
// }
```

### `suggestFixes(issues, options?)`

Generate fix suggestions for issues.

```javascript
const fixes = suggestFixes(analysis.issues, { language: 'csharp' });
// [{ type: 'async_void', fixSuggestion: '...', ... }]
```

### `getVisualStudioGuidance(language?)`

Get Visual Studio debugging guidance.

```javascript
const guidance = getVisualStudioGuidance('csharp');
// {
//   breakpoints: '...',
//   watchWindow: '...',
//   tips: [...]
// }
```

### `generateDebugConfig(language, options?)`

Generate debug configuration for VS Code / Visual Studio.

```javascript
const config = generateDebugConfig('csharp');
// { visualStudio: {...}, vscode: {...} }
```

### `detectAIPatterns(code)`

Detect common AI-generated code characteristics.

```javascript
const patterns = detectAIPatterns(code);
// [{ type: 'todo_comments', description: '...', suggestion: '...' }]
```

### `quickFix(code, issueType)`

Apply quick fix for common issues.

```javascript
const fixed = quickFix(code, 'console_writeline_leftover');
// { original: '...', fixed: '...', applied: true }
```

### `generateReport(analysis)`

Generate a markdown debugging report.

```javascript
const report = generateReport(analysis);
// '# Code Analysis Report\n...'
```

## Supported Languages

- **C# / .NET Core** - Full support with Visual Studio guidance
- **TypeScript** - Type safety and async patterns
- **JavaScript** - Promise and async/await patterns
- **Python** - Exception handling and best practices
- **Java** - Exception handling and threading

## Common Issues Detected

### C# / .NET Core

| Issue | Severity | Description |
|-------|----------|-------------|
| `async_void` | High | async void should only be used for event handlers |
| `task_result_blocking` | High | .Result blocks thread, potential deadlock |
| `task_wait_blocking` | High | .Wait() blocks thread |
| `empty_catch` | High | Empty catch swallows exceptions |
| `console_writeline_leftover` | Low | Debug Console.WriteLine left in code |
| `thread_sleep_blocking` | Medium | Thread.Sleep blocks thread |

### JavaScript / TypeScript

| Issue | Severity | Description |
|-------|----------|-------------|
| `promise_without_catch` | High | Promise chain without .catch() |
| `async_without_try_catch` | Medium | Async function without error handling |
| `console_log_leftover` | Low | Debug console.log left in code |
| `explicit_any_type` | Medium | Explicit use of any type (TS) |
| `ts_ignore_comment` | High | @ts-ignore suppresses errors (TS) |

### Python

| Issue | Severity | Description |
|-------|----------|-------------|
| `bare_except` | High | Bare except catches all exceptions |
| `wildcard_import` | Medium | Wildcard import pollutes namespace |
| `print_statement_leftover` | Low | Debug print left in code |

## Visual Studio Debugging Tips

### Breakpoints
- **F9** - Toggle breakpoint
- **F5** - Start debugging
- **F10** - Step over
- **F11** - Step into
- **Shift+F11** - Step out

### Debug Windows
- **Watch** - Monitor variables
- **Immediate** - Evaluate expressions
- **Call Stack** - Trace execution
- **Locals** - View local variables
- **Autos** - View relevant variables

### Advanced Features
- **Conditional breakpoints** - Right-click breakpoint > Conditions
- **Hit count** - Break after N hits
- **Exception settings** - Break on specific exceptions
- **Edit and Continue** - Modify code while debugging

## Example: Debugging AI-Generated C# Code

```javascript
const debugger = require('./skills/agent-code-debugger');

const aiGeneratedCode = `
public async void ProcessData() {
    var result = GetDataAsync().Result;
    Console.WriteLine($"Debug: {result}");
    try {
        // Process result
    } catch {
        // Handle error
    }
}
`;

// Analyze
const analysis = debugger.analyze(aiGeneratedCode, { language: 'csharp' });
console.log(analysis.summary);
// Found 4 issue(s): 3 high, 1 low

// Get fixes
const fixes = debugger.suggestFixes(analysis.issues);
for (const fix of fixes) {
  console.log(`Line ${fix.line}: ${fix.type}`);
  console.log(`Fix: ${fix.fixSuggestion}`);
}

// Quick fix
const cleaned = debugger.quickFix(aiGeneratedCode, 'console_writeline_leftover');

// Get VS guidance
const guidance = debugger.getVisualStudioGuidance('csharp');
console.log('Tips:', guidance.tips);
```

## Example: Generating Debug Configuration

```javascript
const debugger = require('./skills/agent-code-debugger');

// For C# / .NET Core
const csharpConfig = debugger.generateDebugConfig('csharp');
console.log(JSON.stringify(csharpConfig.vscode, null, 2));

// For TypeScript
const tsConfig = debugger.generateDebugConfig('typescript');
console.log(JSON.stringify(tsConfig.vscode, null, 2));
```

## Notes

- Pattern detection based on common AI-generated code issues
- Security vulnerability scanning included
- Multi-language support with language-specific patterns
- Visual Studio and VS Code integration guidance
- Quick fixes available for common cleanup tasks
- Reports generated in markdown format
