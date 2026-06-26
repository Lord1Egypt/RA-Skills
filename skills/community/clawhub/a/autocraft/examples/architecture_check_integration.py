"""
验证子代理 - 架构检查集成示例

演示如何在验证子代理中集成架构检查
"""

import os
import sys
import json
from pathlib import Path

# 添加架构检查脚本路径
sys.path.append(str(Path(__file__).parent.parent / "scripts" / "architecture-check"))

from validator_template import check_architecture_quality, integrate_with_validation

def verify_code_with_architecture_check(task_info: dict, output_files: list) -> dict:
    """
    验证代码（包含架构检查）
    
    参数:
        task_info: 任务信息
        output_files: 产出物文件列表
        
    返回:
        dict: 验证结果
    """
    verification_results = {
        "verification_success": True,
        "verification_report": "",
        "dimension_results": {},
        "issues_found": [],
        "improvements_suggested": []
    }
    
    # 1. 完整性检查
    completeness_result = check_completeness(task_info, output_files)
    verification_results["dimension_results"]["完整性"] = completeness_result["result"]
    if completeness_result["result"] == "FAIL":
        verification_results["verification_success"] = False
        verification_results["issues_found"].extend(completeness_result["issues"])
    
    # 2. 正确性检查
    correctness_result = check_correctness(task_info, output_files)
    verification_results["dimension_results"]["正确性"] = correctness_result["result"]
    if correctness_result["result"] == "FAIL":
        verification_results["verification_success"] = False
        verification_results["issues_found"].extend(correctness_result["issues"])
    
    # 3. 可运行性检查
    runnability_result = check_runnability(task_info, output_files)
    verification_results["dimension_results"]["可运行性"] = runnability_result["result"]
    if runnability_result["result"] == "FAIL":
        verification_results["verification_success"] = False
        verification_results["issues_found"].extend(runnability_result["issues"])
    
    # 4. 一致性检查
    consistency_result = check_consistency(task_info, output_files)
    verification_results["dimension_results"]["一致性"] = consistency_result["result"]
    if consistency_result["result"] == "FAIL":
        verification_results["verification_success"] = False
        verification_results["issues_found"].extend(consistency_result["issues"])
    
    # 5. 安全性检查
    security_result = check_security(task_info, output_files)
    verification_results["dimension_results"]["安全性"] = security_result["result"]
    if security_result["result"] == "FAIL":
        verification_results["verification_success"] = False
        verification_results["issues_found"].extend(security_result["issues"])
    
    # 6. 架构合理性检查（新增）
    architecture_result = integrate_with_validation(task_info, output_files)
    verification_results["dimension_results"]["架构合理性"] = architecture_result["result"]
    if architecture_result["result"] == "FAIL":
        verification_results["verification_success"] = False
        verification_results["issues_found"].extend(architecture_result.get("issues", []))
        verification_results["improvements_suggested"].extend(architecture_result.get("recommendations", []))
    
    # 生成验证报告
    verification_results["verification_report"] = generate_verification_report(
        verification_results["dimension_results"],
        verification_results["issues_found"],
        verification_results["improvements_suggested"]
    )
    
    return verification_results

def check_completeness(task_info: dict, output_files: list) -> dict:
    """检查完整性"""
    # 实际实现中，这里会检查所有要求的功能/字段/文件是否齐全
    return {"result": "PASS", "issues": []}

def check_correctness(task_info: dict, output_files: list) -> dict:
    """检查正确性"""
    # 实际实现中，这里会检查产出物内容是否与设计文档完全一致
    return {"result": "PASS", "issues": []}

def check_runnability(task_info: dict, output_files: list) -> dict:
    """检查可运行性"""
    # 实际实现中，这里会检查代码是否能运行
    return {"result": "PASS", "issues": []}

def check_consistency(task_info: dict, output_files: list) -> dict:
    """检查一致性"""
    # 实际实现中，这里会检查执行日志与实际产出物是否一致
    return {"result": "PASS", "issues": []}

def check_security(task_info: dict, output_files: list) -> dict:
    """检查安全性"""
    # 实际实现中，这里会检查SQL注入、输入验证等安全问题
    return {"result": "PASS", "issues": []}

def generate_verification_report(dimension_results: dict, issues_found: list, improvements_suggested: list) -> str:
    """生成验证报告"""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("验证报告")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # 维度检查结果
    report_lines.append("📊 维度检查结果")
    for dimension, result in dimension_results.items():
        status_icon = "✅" if result == "PASS" else "❌"
        report_lines.append(f"  {status_icon} {dimension}: {result}")
    report_lines.append("")
    
    # 总体结果
    all_pass = all(result == "PASS" for result in dimension_results.values())
    overall_status = "✅ 通过" if all_pass else "❌ 不通过"
    report_lines.append(f"📈 总体验证结果: {overall_status}")
    report_lines.append("")
    
    # 发现问题
    if issues_found:
        report_lines.append("⚠️  发现的问题")
        for i, issue in enumerate(issues_found, 1):
            report_lines.append(f"  {i}. {issue}")
        report_lines.append("")
    
    # 改进建议
    if improvements_suggested:
        report_lines.append("💡 改进建议")
        for i, suggestion in enumerate(improvements_suggested, 1):
            report_lines.append(f"  {i}. {suggestion}")
        report_lines.append("")
    
    # 架构检查详情（如果有）
    if "架构合理性" in dimension_results and dimension_results["架构合理性"] == "FAIL":
        report_lines.append("🏗️  架构问题详情")
        report_lines.append("  文件职责单一性（SRP原则）检查失败")
        report_lines.append("  建议：")
        report_lines.append("    1. 拆分职责混淆的文件")
        report_lines.append("    2. 将业务逻辑从路由文件移动到服务层")
        report_lines.append("    3. 提取公共功能，减少耦合")
        report_lines.append("")
        report_lines.append("  参考架构规则：templates/architecture-rules/architecture_rules.md")
        report_lines.append("")
    
    report_lines.append("=" * 80)
    return "\n".join(report_lines)

# 使用示例
if __name__ == "__main__":
    # 模拟任务信息
    task_info = {
        "task_id": "TSK-001",
        "task_name": "数据管理模块开发",
        "project_path": "/data/projects/sample-project",
        "deliverables": [
            "backend/api/routers/data_router.py",
            "backend/services/data_service.py"
        ]
    }
    
    # 模拟产出物文件
    output_files = [
        "/data/projects/sample-project/backend/api/routers/data_router.py",
        "/data/projects/sample-project/backend/services/data_service.py"
    ]
    
    # 运行验证（包含架构检查）
    result = verify_code_with_architecture_check(task_info, output_files)
    
    # 输出验证结果
    print("验证结果JSON:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\n" + "=" * 80)
    print("验证报告:")
    print(result["verification_report"])
    
    # 保存验证结果（模拟验证子代理输出）
    output_path = f"/tmp/autocraft_output/{task_info['task_id']}_verification_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n验证结果已保存到: {output_path}")
    
    # 检查架构合理性维度
    if result["dimension_results"].get("架构合理性") == "FAIL":
        print("\n⚠️  发现架构问题，需要重构代码")
        print("请参考架构规则文档：templates/architecture-rules/architecture_rules.md")
        print("运行架构检查脚本：python3 scripts/architecture-check/architecture_check.py --path /path/to/code")