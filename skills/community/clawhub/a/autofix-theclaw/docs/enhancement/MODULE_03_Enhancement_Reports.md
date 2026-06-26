---
name: MODULE_03_Enhancement_Reports
description: New module for generating interactive diagnostic reports and intelligent error log summaries in v5.0 release.
---

# 🖼️ Diagnosis Report & Error Log Intelligence (v5.0 New Feature)

**Version:** 5.0 (Emergency Release)  
**Status:** Active  
**Author:** autofix-theclaw Skill Team

---

## 🎯 Module Goals

This module introduces two critical enhancements to the diagnostic workflow:

1. **Diagnosis Report Visualization (DRE)** - Generates interactive, canvas-based diagnostic reports for Path B MRE failures
2. **Error Log Intelligent Summary (ELIS)** - Uses LLM-powered analysis to extract root causes from exec output

---

## 🖼️ Feature 1: Diagnosis Report Visualization (DRE)

### 📋 Overview
When a Minimal Reproducible Example (MRE) test fails in Path B, instead of just showing raw exec output, the system now generates an **interactive diagnostic report** using the `canvas` tool.

### 🔄 Workflow

```
Path B MRE Test → Failure Detected 
↓  
[NEW] Extract Key Metrics: 
  - Problem Type (CLI/Config/Network)
  - Risk Level (Critical/Medium/Low)
  - Error Count & Types
  - Affected Tools
↓  
[NEW] Generate Canvas Report via canvas.snapshot(action="snapshot", javaScript="<diagnostic-report-logic>")
↓  
Display to User with: 
  ✅ Visual risk flags (🔴/🟠/🟢)
  📊 Evidence chain diagram (Doc vs GH)
  ⚡ Exec result status codes highlighted
  🔄 Rollback command code block
```

### 💻 Implementation Details

**Step A: Canvas Report Generation**
```python
# After exec fails in Path B:
canvas.snapshot(
    action="snapshot",
    javaScript="""
      // Generate diagnostic report HTML
      const metrics = {
        riskLevel: errorSeverity,
        problemType: triage.category,
        affectedTools: [...],
        errorCount: log.lines.filter(l => l.includes('error')).length
      };
      
      return `
        <html>
          <head><style>
            .risk-critical { color: #dc3545; font-weight: bold; }
            .risk-medium { color: #ffc107; }
            .risk-low { color: #28a745; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
          </style></head>
          <body>
            <h2>🔍 Diagnosis Report</h2>
            <div class="risk-critical">Risk Level: ${metrics.riskLevel}</div>
            <p><strong>Problem Type:</strong> ${metrics.problemType}</p>
            <p><strong>Affected Tools:</strong> ${metrics.affectedTools.join(', ')}</p>
            <p><strong>Error Count:</strong> ${metrics.errorCount}</p>
            <hr>
            <h3>📊 Evidence Chain</h3>
            <ul>
              <li>OpenClaw Docs: 📖 [Link]</li>
              <li>GitHub Issues: 🐛 [Link]</li>
            </ul>
            <hr>
            <h3>💡 Root Cause Analysis</h3>
            <p>${elAnalysis.summary}</p>
            <h3>🔧 Recommended Fix</h3>
            <pre><code class="bash">${elAnalysis.fixCommand}</code></pre>
            <hr>
            <div class="risk-medium">⚠️ Rollback Command:</div>
            <pre><code class="bash">${rollbackCommand}</code></pre>
          </body>
        </html>
      `;
    """
  )
```

**Step B: Canvas Display Options**
```python
# Option 1: Inline display (preferred for webchat)
canvas.present(url="/__openclaw__/canvas/documents/reports/diag_20260517_xxx.html")

# Option 2: Screenshot capture for sharing
canvas.snapshot(
    action="snapshot",
    outputFormat="png",
    fullPage=true,
    maxChars=4096
)
```

### 📊 Report Layout Template

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; }
    .risk-critical { background: #f8d7da; padding: 15px; border-radius: 5px; color: #721c24; }
    .risk-medium { background: #fff3cd; padding: 10px; border-radius: 5px; color: #856404; }
    .risk-low { background: #d4edda; padding: 10px; border-radius: 5px; color: #155724; }
    code { font-size: 90%; background: #f8f9fa; padding: 3px 6px; border-radius: 3px; }
    h2 { border-bottom: 2px solid #007bff; padding-bottom: 10px; }
  </style>
</head>
<body>
  <h1 style="color:#007bff;">🔍 OpenClaw Diagnostic Report</h1>
  
  <div class="risk-critical">
    <strong>⚠️ Status:</strong> MRE Test Failed | <strong>Risk Level:</strong> Critical
  </div>
  
  <h2>📋 Problem Context</h2>
  <p><strong>Issue Type:</strong> ${triage.type}</p>
  <p><strong>Affected Tools:</strong> ${affectedTools.join(', ')}</p>
  
  <h2>🔬 Error Analysis</h2>
  <pre>${errorLogs}</pre>
  
  <h2>💡 Root Cause (AI Analysis)</h2>
  <p><strong>Core Issue:</strong> ${rootCause.summary}</p>
  <p><strong>Possible Causes:</strong></p>
  <ul>
    <li>${rootCause.cause1}</li>
    <li>${rootCause.cause2}</li>
  </ul>
  
  <h2>🔧 Recommended Fix</h2>
  <pre><code class="bash">${fixCommand}</code></pre>
  
  <div class="risk-medium">
    <strong>⚠️ Rollback Command (if needed):</strong><br>
    <pre><code class="bash">${rollbackCommand}</code></pre>
  </div>
  
  <h2>🔗 Evidence Chain</h2>
  <ul>
    <li><a href="${docsLink}">📖 OpenClaw Docs</a></li>
    <li><a href="${ghLink}">🐛 GitHub Issues</a></li>
  </ul>
</body>
</html>
```

---

## 🧠 Feature 2: Error Log Intelligent Summary (ELIS)

### 📋 Overview
When MRE fails, the system now uses LLM-powered analysis to extract the root cause from exec output, rather than just showing raw logs.

### 🔄 Workflow

```
exec Command → Fails with Output 
↓  
[NEW] Pass output to LLM for analysis:
mem.recall("autofix-theclaw", corpus="all") + tavily_search(query="<error-message>")
↓  
AI Analysis Generates:
  - Core Issue (根因)
  - Possible Causes (可能原因)
  - Recommended Fix (修复建议)
  - Risk Level (风险等级)
↓  
Present to User with Confidence Score
```

### 💻 Implementation Details

**Step A: Error Log Collection**
```python
# After exec fails:
errorOutput = exec_result.output.strip()
errorLines = [line for line in errorOutput.split('\n') if 'error' in line.lower() or 'fail' in line.lower()]
errorMessages = ' '.join(errorLines)
```

**Step B: LLM-Driven Analysis**
```python
# Use session model for analysis
analysis = session.execute(
    f"""
    Analyze this OpenClaw error: "{errorMessages}"
    
    Generate a structured analysis with:
    1. Core Issue (根因): One sentence summary
    2. Possible Causes (可能原因): 2-3 bullet points  
    3. Recommended Fix (修复建议): Specific command(s) to try
    4. Risk Level: Critical/Medium/Low
    
    Format as JSON with keys: core_issue, causes[], fix_command, risk_level
    """
)

# Extract and parse the analysis
rootCause = json.loads(analysis)
```

**Step C: Generate Rollback Command**
```python
# Always generate rollback command for safety
rollbackCommand = f"""# Rollback Command (execute if needed):
openclaw gateway status  # Check current state
# If issue persists, consider:
openclaw doctor --fix --dry-run  # Dry-run to preview changes
# OR revert to previous config:
git checkout HEAD~1 -- .openclaw/  # If using git"""
```

### 📊 Analysis Output Template

```json
{
  "core_issue": "exec 命令未指定 pty=true，导致 TTY 终端程序运行失败",
  "causes": [
    "当前会话配置中缺少 pty 参数",
    "目标命令需要交互式终端环境（如：tail -f, grep 等）",
    "执行模式为 sandboxed，未传递正确的 shell 环境变量"
  ],
  "fix_command": "openclaw doctor --fix --pty=true --yieldMs=15000",
  "risk_level": "Medium",
  "confidence_score": 0.92,
  "evidence_chain": {
    "docs_match": true,
    "gh_issue_match": true,
    "pattern_matches": ["exec_timeout", "pty_missing"]
  }
}
```

### 📝 User-Friendly Analysis Output

```markdown
## 🔍 AI 错误分析报告

**核心问题：** exec 命令未指定 pty=true，导致 TTY 终端程序运行失败

**可能原因：**
- ❌ 当前会话配置中缺少 pty 参数
- ❌ 目标命令需要交互式终端环境（如：tail -f, grep 等）  
- ❌ 执行模式为 sandboxed，未传递正确的 shell 环境变量

**风险等级：** ⚠️ Medium (中等风险)

**修复建议：**
```bash
openclaw doctor --fix --pty=true --yieldMs=15000
```

**回滚命令（如需要）：**
```bash
# 先检查当前状态
openclaw gateway status

# 如果问题仍然存在，可以：
openclaw doctor --fix --dry-run  # 预览更改但不执行
```

---
**证据链分析：**
- ✅ OpenClaw Docs 支持此解决方案 (匹配度: 0.85)
- ✅ GitHub Issues 确认相同问题 (Issue #XXX)
- 🎯 模式匹配：exec_timeout, pty_missing (置信度：92%)
```

---

## 🔗 Integration Points

### Where to Insert in Existing Flow

**Path B - MRE Loop Enhancement:**
```python
# ORIGINAL Step 4B:
if mre_result.failed:
    # [NEW] Extract and analyze error
    rootCause = elis_analyze(exec_result.output)
    
    # [NEW] Generate diagnostic report canvas
    diag_report_url = generate_diagnosis_report(rootCause, exec_result)
    
    # Present to user with rollback option
    present_with_canvas(
        title="MRE 验证失败 - 诊断报告",
        url=diag_report_url,
        include_rollback=True
    )
```

---

## ✅ Rollback Plan (for Feature Testing)

To test these enhancements safely:

1. **Backup Current State:**
   ```bash
   git status
   git add .
   git commit -m "Autofix v5.0 diagnostic reports feature"
   ```

2. **Test with Dry-Run:**
   ```python
   # Add dry-run flag before exec:
   exec(command=f"...", pty=True, yieldMs=10000)  # Test mode
   ```

3. **Revert Changes:**
   ```bash
   git checkout HEAD~1 -- skills/autofix-theclaw/MODULE_03_Enhancement_Reports.md
   ```

---

## 📊 Performance Impact

| Feature | Additional Latency | Resource Usage |
|---------|-------------------|----------------|
| **DRE (Canvas)** | +2-4 seconds | ~50MB canvas memory |
| **ELIS (LLM Analysis)** | +8-12 seconds | LLM token: ~2k tokens |

**Total Additional Time:** 10-16 seconds per MRE failure  
**Trade-off:** Better user experience, higher confidence resolution

---

## 📚 References

- Canvas Tool Docs: `C:\Users\flyin\AppData\Roaming\npm\node_modules\openclaw\docs`
- LLM Analysis Best Practices: See `memory-setup\SKILL.md` for context injection
- Evidence Chain Protocol: See `MODULE_02_SearchChain.md` Section 3

---

*This module is designed for immediate integration into autofix-theclaw v5.0 workflow.*
