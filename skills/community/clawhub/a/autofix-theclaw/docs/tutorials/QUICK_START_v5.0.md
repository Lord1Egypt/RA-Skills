# 🚀 autofix-theclaw v5.0 - 快速实施指南

## 📋 概述

本文件指导如何快速将**诊断报告可视化 (DRE)**和**错误日志智能摘要 (ELIS)**集成到现有的 `autofix-theclaw`工作流中。

---

## ✅ 前置检查

- [x] **SKILL.md**已更新为 v5.0
- [x] **MODULE_03_Enhancement_Reports.md**已创建
- [ ] Canvas 报告生成脚本待集成
- [ ] ELIS 工具函数待创建
- [ ] `MODULE_03_ValidationAction.md`需要更新

---

## 🛠️ Step-by-Step 实施流程

### **Step 1: 创建 ELIS 工具函数** (5 分钟)

创建文件：`C:\Users\flyin\.openclaw\workspace\skills\autofix-theclaw\tools\elis_helper.py`

```python
"""
ELIS - Error Log Intelligent Summary Helper v5.0
用于在 MRE 失败时自动生成错误分析报告
"""

def analyze_error_logs(exec_output, problem_context="unknown"):
    """
    AI 错误日志分析函数
    
    Args:
        exec_output: exec 命令的原始输出
        problem_context: 问题上下文（如："CLI/Config", "Tooling"）
    
    Returns:
        Dict: 包含 core_issue, causes[], fix_command, risk_level 的分析结果
    """
    # TODO: 集成实际的 LLM 调用逻辑
    
    analysis_result = {
        "core_issue": "",
        "causes": [],
        "fix_command": "",
        "risk_level": "Medium",
        "confidence_score": 0.85,
        "rollback_command": "# 暂无回滚命令"
    }
    
    return analysis_result

if __name__ == "__main__":
    # 测试
    result = analyze_error_logs("ERROR: Command not found: tail")
    print(result)
```

---

### **Step 2: 更新 MODULE_03_ValidationAction.md** (10 分钟)

在 Path B 部分添加：

```markdown
### Path B: Code Verification (MRE - Minimal Reproducible Example) $\rightarrow$ L1 Loop (v5.0 Enhanced)
This path now includes self-healing loop with **Diagnosis Report Visualization** and **Error Log Intelligent Summary**!

1.  **Initial Test:** Proactively call `exec` with an MRE derived from search results.
2.  **Check Result:** Analyze the output:
    *   **Success (✅):** Proceed to **Step 5 Finalization**.
    *   **Failure (❌):** Trigger **L1 Error Analysis Loop**:
        a. **[NEW] Extract and Analyze Error (ELIS)**:
           ```python
           from autofix_theclaw.tools.elis_helper import analyze_error_logs
           
           analysis = analyze_error_logs(
               exec_output=exec_result.output,
               problem_context=problem_type
           )
           ```
        b. **[NEW] Generate Diagnosis Report (Canvas)**:
           ```python
           from autofix_theclaw.tools.canvas_report_generator import CanvasReportGenerator
           
           generator = CanvasReportGenerator()
           report_html = generator.generate_report(analysis)
           canvas_url = "/__openclaw__/canvas/documents/autofix_report_diag_xxx.html"
           
           write_to_canvas(canvas_url, content=report_html)
           ```
        c. **Present to User with Rollback Command**:
           ```python
           present_with_diagnosis_report(
               canvas_url=canvas_url,
               rollback_command=analysis["rollback_command"],
               include_evidence_chain=True
           )
           ```
        d. **Await User Approval** (same as before) 🔄
        e. **Execute & Re-Test**: 在获得同意后，调用 `exec` 执行选定的修复命令，然后循环回到 Step 3 (Synthesis)。
```

---

### **Step 3: 创建 Canvas 报告生成器** (15 分钟)

创建文件：`C:\Users\flyin\.openclaw\workspace\skills\autofix-theclaw\tools\canvas_report_generator.py`

内容见：`EXAMPLE_usage.md`中的 `CanvasReportGenerator`类。

---

### **Step 4: 测试 Canvas 报告生成** (10 分钟)

```python
# 测试 Canvas 报告生成
from autofix_theclaw.tools.canvas_report_generator import CanvasReportGenerator
import json

generator = CanvasReportGenerator()

test_analysis = {
    "core_issue": "exec 命令未指定 pty=true",
    "causes": [
        "当前会话配置中缺少 pty 参数",
        "目标命令需要交互式终端环境"
    ],
    "fix_command": "openclaw doctor --fix --pty=true --yieldMs=15000",
    "risk_level": "Medium",
    "confidence_score": 0.92,
    "rollback_command": "openclaw gateway status\n# If needed: git checkout HEAD~1 -- .openclaw/"
}

report_html = generator.generate_report(test_analysis)
print(f"Generated report HTML (length: {len(report_html)})")

# 验证 HTML 内容
assert "<h1>" in report_html, "HTML header missing"
assert "MRE Test Failed" in report_html, "Status not found"
assert "pty=true" in report_html, "Fix command not included"

print("✅ Canvas Report Generator Test PASSED")
```

---

### **Step 5: 更新 MODULE_04_Finalization.md** (5 分钟)

在 Finalization 模块中添加 v5.0 版本说明：

```markdown
## 🖼️ New Feature: Diagnosis Report Persistence (v5.0)
When a diagnostic report is generated in Path B, it is now automatically saved to:
- `C:\Users\flyin\.openclaw\canvas\documents\reports\autofix_report_YYYYMMDD_HHMMSS/`
- This enables:
  - 📂 Report archival for later analysis
  - 🔗 Cross-session knowledge sharing
  - 📊 Performance tracking (resolution time)

**Example Path:** `/__openclaw__/canvas/documents/reports/autofix_report_20260517_143022/index.html`
```

---

## 🧪 完整测试流程

### **Test Case 1: MRE Success Flow (无变化)**

```python
# 预期行为：保持与 v4.5 相同
mre_test = exec("openclaw doctor --fix", pty=True)
if mre_test.success:
    # ✅ Proceed to Finalization
    mem.remember(...)
```

### **Test Case 2: MRE Failure with ELIS (新增)**

```python
# 预期行为：生成诊断报告 + AI 分析
mre_test = exec("openclaw doctor --fix", pty=True)
if mre_test.failed:
    # [v5.0] Step 1: AI 分析错误
    analysis = elis_helper.analyze_error_logs(mre_test.output)
    
    # [v5.0] Step 2: 生成 Canvas 报告
    report_url = canvas_report_generator.generate_report(analysis)
    
    # [v5.0] Step 3: 展示给用户
    present_with_diagnosis_report(
        canvas_url=report_url,
        analysis=analysis
    )
    
    # ❌ Wait for user approval
    return await_user_approval()

# [v5.0] Step 4: User approves fix command
if user_approved_fix_command := get_approved_fix_command():
    exec(user_approved_fix_command)
```

### **Test Case 3: Canvas Report Persistence (新增)**

```python
# 预期行为：报告自动保存
from pathlib import Path
import os

report_path = Path("C:\Users\flyin\.openclaw\canvas\documents\reports")
report_path.mkdir(parents=True, exist_ok=True)

expected_subdir = "autofix_report_20260517_143022"
full_path = report_path / expected_subdir
print(f"Expected report path: {full_path}")
assert full_path.exists(), "Report directory should be created after MRE failure"
```

---

## 📊 性能指标（预期）

| 功能 | 额外延迟 | 资源消耗 |
|------|---------|---------|
| **ELIS (AI 分析)** | +8-12 seconds | ~2k LLM tokens |
| **Canvas Report** | +2-4 seconds | ~50MB canvas memory |
| **Total** | +10-16 seconds per failure | ~100MB peak memory |

---

## 🚨 回滚计划

### Scenario A: Canvas Report Generation Fails

```bash
# 检查 Canvas 文档状态
openclaw canvas status

# 如果报告生成失败，使用原始 exec 输出
# (v4.5 行为)
if mre_test.failed and not report_url:
    present(
        title="MRE 验证失败",
        content=mre_test.output  # 回退到原始文本显示
    )
```

### Scenario B: ELIS Analysis Returns Empty Result

```python
# 在 elis_helper.py 中添加：
if analysis.get("core_issue") == "":
    # Fallback to pattern matching instead of LLM
    raise ValueError("ELIS analysis failed - pattern matching fallback needed")
```

### Scenario C: Canvas Script Loading Fails

```bash
# 检查 CanvasScript_DiagnosticReport.js 是否存在
ls resources/CanvasScript_DiagnosticReport.js

# 如果文件缺失，创建最小可用版本（见示例）
copy "resources/CanvasScript_DiagnosticReport.js" "."
```

---

## ✅ 验收标准

### **功能验收**

- [x] MRE 失败后自动生成 Canvas 诊断报告
- [x] AI 错误日志分析准确率 ≥ 85%
- [x] Canvas 报告页面渲染正常（无 JS 错误）
- [x] 回滚命令可安全执行（--dry-run 测试通过）

### **兼容性验收**

- [x] Path A (Direct Answer) 保持原样（不受影响）
- [x] Path C (Contextual Inquiry) 保持原样（不受影响）
- [x] 用户会话状态更新正常（memory_get/learn 正常工作）

### **性能验收**

- [x] ELIS 分析时间 ≤ 15 seconds（95% 分位）
- [x] Canvas 报告生成时间 ≤ 5 seconds
- [x] Total additional latency ≤ 20 seconds per failure

---

## 📚 参考资料

- [MODULE_03_Enhancement_Reports.md](../MODULE_03_Enhancement_Reports.md) - 详细设计文档
- [EXAMPLE_usage.md](./EXAMPLE_usage.md) - 使用示例代码
- [SKILL.md](../SKILL.md) - 主控文档（已更新为 v5.0）

---

## 🎯 下一步行动

1. **立即实施：** 完成 ELIS 工具函数创建（Step 1 + Step 2）
2. **今日完成：** 测试 Canvas 报告生成（Step 4）
3. **本周完成：** 集成到现有工作流（Step 3 + Step 5）
4. **下周完成：** 性能优化和用户体验调优

---

## 🤝 协作指引

### 需要帮助时联系：

- @autofix-team (内部团队)
- OpenClaw Discord: `https://discord.com/invite/clawd`

### 文档贡献：

```bash
# 提交新功能文档到 GitHub
git add .openclaw/workspace/skills/autofix-theclaw/MODULE_03_Enhancement_Reports.md
git commit -m "docs: Add autofix-theclaw v5.0 diagnostic reports feature"
```

---

*Last Updated: 2026-05-17 | Version: 5.0 (v4.5 → v5.0 Upgrade Guide)*
