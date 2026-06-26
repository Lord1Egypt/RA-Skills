"""
验证子代理 - 架构合理性检查模板

使用方式：
1. 将此模板集成到验证子代理的验证逻辑中
2. 调用 check_architecture_quality() 函数
3. 根据结果更新验证维度
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

def check_architecture_quality(code_path: str) -> Dict:
    """
    检查代码架构质量
    
    参数:
        code_path: 代码目录路径
        
    返回:
        Dict: 检查结果
    """
    try:
        # 确保架构检查脚本存在
        script_path = Path(__file__).parent / "architecture_check.py"
        if not script_path.exists():
            return {
                "status": "ERROR",
                "issues": ["架构检查脚本不存在"],
                "dimension_result": "FAIL"
            }
        
        # 运行架构检查
        report_path = "/tmp/architecture_report.json"
        result = subprocess.run(
            [
                sys.executable, str(script_path),
                "--path", code_path,
                "--report", report_path
            ],
            capture_output=True,
            text=True,
            timeout=120  # 2分钟超时
        )
        
        # 检查执行结果
        if result.returncode == 0:
            # 成功执行，读取报告
            if os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                
                # 检查是否有高危问题
                if report.get("summary", {}).get("high_severity", 0) > 0:
                    return {
                        "status": "FAIL",
                        "issues": ["发现架构高危问题，违反SRP原则"],
                        "report": report,
                        "dimension_result": "FAIL"
                    }
                else:
                    return {
                        "status": "PASS",
                        "report": report,
                        "dimension_result": "PASS"
                    }
            else:
                return {
                    "status": "ERROR",
                    "issues": ["架构检查报告未生成"],
                    "dimension_result": "FAIL"
                }
        elif result.returncode == 1:
            # 发现高危问题
            if os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                
                # 提取问题详情
                issues = []
                for check_type in ["srp_checks", "structure_checks", "boundary_checks"]:
                    for check in report.get(check_type, []):
                        for issue in check.get("issues", []):
                            if issue.get("severity") == "HIGH":
                                issues.append(f"{issue.get('file')}: {issue.get('description')}")
                
                return {
                    "status": "FAIL",
                    "issues": issues,
                    "report": report,
                    "dimension_result": "FAIL"
                }
            else:
                return {
                    "status": "FAIL",
                    "issues": ["架构检查发现高危问题"],
                    "error": result.stderr,
                    "dimension_result": "FAIL"
                }
        else:
            # 执行错误
            return {
                "status": "ERROR",
                "issues": [f"架构检查执行失败: {result.stderr}"],
                "dimension_result": "FAIL"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "ERROR",
            "issues": ["架构检查超时（超过2分钟）"],
            "dimension_result": "FAIL"
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "issues": [f"架构检查异常: {str(e)}"],
            "dimension_result": "FAIL"
        }

def integrate_with_validation(task_info: Dict, output_files: List[str]) -> Dict:
    """
    集成到验证子代理的验证流程
    
    参数:
        task_info: 任务信息
        output_files: 产出物文件列表
        
    返回:
        Dict: 架构合理性维度验证结果
    """
    # 确定代码路径（通常是项目根目录）
    project_path = task_info.get("project_path", ".")
    
    # 运行架构检查
    architecture_result = check_architecture_quality(project_path)
    
    # 构建验证结果
    if architecture_result["status"] == "PASS":
        return {
            "dimension": "架构合理性",
            "result": "PASS",
            "details": "代码架构符合设计原则，未发现SRP违规",
            "report_summary": architecture_result.get("report", {}).get("summary", {})
        }
    elif architecture_result["status"] == "FAIL":
        return {
            "dimension": "架构合理性",
            "result": "FAIL",
            "details": "发现架构问题，违反SRP原则",
            "issues": architecture_result.get("issues", []),
            "report_summary": architecture_result.get("report", {}).get("summary", {}),
            "recommendations": [
                "1. 拆分职责混淆的文件",
                "2. 将业务逻辑从路由文件移动到服务层",
                "3. 提取公共功能，减少耦合"
            ]
        }
    else:  # ERROR
        return {
            "dimension": "架构合理性",
            "result": "FAIL",  # 检查失败视为不通过
            "details": f"架构检查失败: {architecture_result.get('issues', ['未知错误'])[0]}",
            "issues": architecture_result.get("issues", []),
            "recommendations": ["请手动检查代码架构"]
        }

def get_architecture_checklist() -> List[str]:
    """
    获取架构检查清单
    
    返回:
        List[str]: 架构检查项目列表
    """
    return [
        "✅ 文件职责单一性（SRP原则）",
        "   - 一个文件只负责一个功能或一组相关功能",
        "   - 禁止在一个文件中混合多个不相关功能",
        "   - 文件大小适中（建议≤50KB，≤500行）",
        "",
        "✅ 代码结构合理性",
        "   - 路由层：只处理HTTP请求/响应",
        "   - 服务层：包含业务逻辑",
        "   - 数据访问层：数据库操作",
        "   - 工具层：公共函数和工具",
        "",
        "✅ 功能边界分明性",
        "   - 不同功能之间耦合度低",
        "   - 公共功能提取到公共模块",
        "   - 避免循环依赖",
        "",
        "✅ 分层架构符合性",
        "   - 遵循MVC/分层架构模式",
        "   - 业务逻辑不在路由文件中",
        "   - 数据库操作不在服务层之外",
        "",
        "✅ 模块依赖合理性",
        "   - 避免导入过多不相关模块（建议≤15个）",
        "   - 依赖关系清晰，无循环依赖",
        "   - 公共模块依赖合理"
    ]

# 使用示例
if __name__ == "__main__":
    # 示例：检查当前目录
    result = check_architecture_quality(".")
    
    print(f"状态: {result['status']}")
    print(f"维度结果: {result.get('dimension_result', 'N/A')}")
    
    if result["status"] == "FAIL":
        print("发现架构问题:")
        for issue in result.get("issues", []):
            print(f"  - {issue}")
    
    # 获取检查清单
    print("\n架构检查清单:")
    for item in get_architecture_checklist():
        print(item)