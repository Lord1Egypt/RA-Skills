"""
ELIS - Error Log Intelligent Summary Helper v5.0 (简化版)
用于在 MRE 失败时自动生成错误分析报告
"""

import json


def analyze_error_logs(exec_output, problem_context="unknown"):
    """分析错误日志并返回结构化结果（规则引擎实现）"""
    
    # 提取错误关键行
    lines = exec_output.strip().split('\n') if exec_output else []
    error_lines = [line for line in lines if any(kw in line.lower() for kw in ['error', 'fail', 'exception'])][:3]
    
    # 规则引擎分析
    analysis = {
        "core_issue": "",
        "causes": [],
        "fix_command": "",
        "risk_level": "Medium",
        "confidence_score": 0.85,
        "rollback_command": "# 暂无回滚命令"
    }
    
    # 规则 1：检测 pty 相关错误
    if any('pty' in line.lower() for line in error_lines):
        analysis["core_issue"] = "exec 命令未指定 pty=true，导致 TTY 终端程序运行失败"
        analysis["causes"] = [
            "当前会话配置中缺少 pty 参数",
            "目标命令需要交互式终端环境（如 tail -f, grep 等）",
            "执行模式为 sandboxed，未传递正确的 shell 环境变量"
        ]
        analysis["fix_command"] = "openclaw doctor --fix --pty=true --yieldMs=15000"
    # 规则 2：检测权限错误
    elif any('permission' in line.lower() for line in error_lines):
        analysis["core_issue"] = "exec 命令需要管理员权限或目标路径缺少执行权限"
        analysis["causes"] = [
            "当前用户没有文件/目录的执行权限",
            "可能需要使用 sudo 或以 root 身份运行"
        ]
        analysis["fix_command"] = "sudo openclaw doctor --fix --pty=true"
    # 规则 3：检测超时错误
    elif any('timeout' in line.lower() for line in error_lines):
        analysis["core_issue"] = "执行命令超时（默认 30 秒），需要增加 timeout 参数"
        analysis["causes"] = [
            "网络请求或长任务超过默认超时时间",
            "可能需要使用 --timeout=300 延长等待时间"
        ]
        analysis["fix_command"] = "openclaw doctor --fix --timeout=300"
    else:
        analysis["core_issue"] = f"执行失败：{''.join(error_lines)[:100]}"
        analysis["causes"] = ["请查看完整日志或使用 canvas 报告查看详细信息"]
    
    return analysis


def generate_diagnosis_report_html(analysis):
    """根据分析结果生成简单的 HTML 报告"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>诊断报告</title></head>
<body style="font-family:sans-serif;padding:20px;">
<h1>OpenClaw 诊断报告 v5.0</h1>
<p><strong>核心问题：</strong>{analysis.get('core_issue','待分析')}</p>
<p><strong>可能原因：</strong></p>
<ul>{"".join([f"<li>{c}</li>" for c in analysis.get('causes',[])])}</ul>
<p><strong>修复建议：</strong><br>{analysis.get('fix_command','')}</p>
<p><strong>风险等级：</strong>{analysis.get('risk_level','Low')}</p>
<p><strong>置信度：</strong>{analysis.get('confidence_score',0):.2f}</p>
</body></html>"""
    return html


if __name__ == "__main__":
    # 测试
    test_output = "ERROR: Command not found: tail -f\\nReason: pty=true parameter is missing"
    analysis = analyze_error_logs(test_output, "CLI/Config")
    print(json.dumps(analysis, indent=2))
