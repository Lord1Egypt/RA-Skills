"""
验证子代理 - 完整验证模板（架构检查 + 设计文档对照）

使用方式：
1. 在验证子代理中导入此模板
2. 调用 verify_with_design_documents() 函数
3. 使用返回的结果作为验证结果

此模板集成了：
- 架构合理性检查（SRP原则）
- 设计文档对照验证
- API接口一致性验证
- 数据库映射验证
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verify_with_design_documents(task_info: Dict[str, Any], 
                                output_files: List[str]) -> Dict[str, Any]:
    """
    运行完整的验证（包含设计文档对照）
    
    参数:
        task_info: 任务信息字典
            - task_id: 任务ID
            - project_path: 项目根目录路径
            - input_files: 设计文档路径映射（可选）
            - deliverables: 产出物文件列表（可选）
        
        output_files: 产出物文件路径列表
        
    返回:
        Dict: 验证结果（验证子代理JSON格式）
    """
    
    try:
        # 提取必要信息
        task_id = task_info.get('task_id', 'UNKNOWN')
        project_path = task_info.get('project_path', '.')
        
        # 提取设计文档路径
        design_docs = task_info.get('input_files', {})
        if not design_docs:
            logger.warning("任务信息中没有设计文档路径（input_files字段）")
            # 尝试从其他字段提取
            for key in ['api_design', 'system_function_design', 'database_design', 'prd']:
                if key in task_info:
                    design_docs[key] = task_info[key]
        
        # 检查输出文件是否存在
        existing_files = []
        for file_path in output_files:
            full_path = Path(file_path)
            if not full_path.is_absolute():
                full_path = Path(project_path) / file_path
            
            if full_path.exists():
                existing_files.append(str(full_path))
            else:
                logger.warning(f"产出物文件不存在: {file_path}")
        
        if not existing_files:
            return _create_error_result("没有可用的产出物文件进行验证")
        
        # 导入集成验证器
        try:
            # 添加设计检查目录到路径
            design_check_dir = Path(__file__).parent.parent.parent / 'scripts' / 'design-check'
            sys.path.append(str(design_check_dir))
            
            from integrated_validator import IntegratedValidator
        except ImportError as e:
            logger.error(f"无法导入集成验证器: {str(e)}")
            return _create_error_result(f"验证工具配置错误: {str(e)}")
        
        # 分类文件类型
        api_code_files = []
        model_files = []
        other_files = []
        
        for file_path in existing_files:
            file_lower = file_path.lower()
            if 'router' in file_lower or 'api' in file_lower:
                api_code_files.append(file_path)
            elif 'model' in file_lower or 'schema' in file_lower:
                model_files.append(file_path)
            else:
                other_files.append(file_path)
        
        logger.info(f"文件分类: API代码={len(api_code_files)}, 模型={len(model_files)}, 其他={len(other_files)}")
        
        # 运行集成验证
        validator = IntegratedValidator(project_path)
        
        result = validator.run_comprehensive_validation(
            code_files=existing_files,
            design_docs=design_docs,
            api_code_files=api_code_files if 'api_design' in design_docs else None,
            model_files=model_files if 'database_design' in design_docs else None
        )
        
        # 构建验证结果
        verification_result = {
            'verification_success': result['verification_success'],
            'verification_report': result['verification_report'],
            'dimension_results': result['dimension_results'],
            'issues_found': result['issues_found'],
            'improvements_suggested': result['improvements_suggested']
        }
        
        # 添加设计文档检查详情
        if design_docs:
            verification_result['design_document_check'] = {
                'documents_checked': list(design_docs.keys()),
                'coverage_percentage': 100 if result['verification_success'] else 0,
                'missing_endpoints': [issue['description'] for issue in result.get('detailed_issues', []) 
                                     if 'API_' in issue.get('type', '')],
                'missing_functions': [issue['description'] for issue in result.get('detailed_issues', []) 
                                     if 'DESIGN_' in issue.get('type', '')],
                'field_mismatches': [issue['description'] for issue in result.get('detailed_issues', []) 
                                    if 'DATABASE_' in issue.get('type', '')]
            }
        
        # 记录验证结果
        logger.info(f"验证完成: success={result['verification_success']}, issues={len(result['issues_found'])}")
        
        return verification_result
        
    except Exception as e:
        logger.error(f"验证过程中发生异常: {str(e)}", exc_info=True)
        return _create_error_result(f"验证异常: {str(e)}")


def verify_architecture_only(code_path: str) -> Dict[str, Any]:
    """
    仅运行架构检查（向后兼容）
    
    参数:
        code_path: 代码目录路径
        
    返回:
        Dict: 架构检查结果
    """
    try:
        # 导入架构检查器
        architecture_dir = Path(__file__).parent.parent.parent / 'scripts' / 'architecture-check'
        sys.path.append(str(architecture_dir))
        
        from architecture_check import ArchitectureChecker
        
        checker = ArchitectureChecker(code_path)
        results = checker.run_checks()
        
        # 提取高危问题
        high_severity_issues = []
        for file_result in results.get('srp_checks', []):
            for issue in file_result.get('issues', []):
                if issue.get('severity') == 'HIGH':
                    high_severity_issues.append(issue)
        
        # 构建结果
        return {
            'status': 'SUCCESS',
            'issues_found': len(high_severity_issues),
            'dimension_result': 'FAIL' if high_severity_issues else 'PASS',
            'detailed_issues': high_severity_issues,
            'summary': results['summary']
        }
        
    except Exception as e:
        logger.error(f"架构检查失败: {str(e)}")
        return {
            'status': 'ERROR',
            'error': str(e),
            'dimension_result': 'FAIL'
        }


def _create_error_result(error_message: str) -> Dict[str, Any]:
    """创建错误结果"""
    return {
        'verification_success': False,
        'verification_report': f"验证失败: {error_message}",
        'dimension_results': {
            '完整性': 'FAIL',
            '正确性': 'FAIL',
            '可运行性': 'FAIL',
            '一致性': 'FAIL',
            '安全性': 'FAIL',
            '架构合理性': 'FAIL'
        },
        'issues_found': [error_message],
        'improvements_suggested': [
            "检查验证工具配置",
            "确保设计文档路径正确",
            "联系系统管理员"
        ]
    }


def save_verification_result(task_id: str, result: Dict[str, Any]) -> str:
    """
    保存验证结果到文件
    
    参数:
        task_id: 任务ID
        result: 验证结果
        
    返回:
        str: 保存的文件路径
    """
    output_dir = Path("/tmp/autocraft_output")
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / f"{task_id}_verification_result.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"验证结果已保存到: {output_path}")
    return str(output_path)


# 使用示例
if __name__ == '__main__':
    print("=" * 80)
    print("验证模板使用示例")
    print("=" * 80)
    
    # 示例配置
    example_task_info = {
        'task_id': 'TEST-001',
        'task_name': '测试验证',
        'project_path': '/data/projects/deeptutor-lite',
        'input_files': {
            'api_design': 'docs/design/07-API设计-DeepTutor-Lite.md',
            'system_function_design': 'docs/design/03-系统功能设计-DeepTutor-Lite.md'
        }
    }
    
    example_output_files = [
        'backend/api/routers/test_router.py',
        'backend/services/test_service.py'
    ]
    
    print(f"\n任务信息:")
    print(f"  ID: {example_task_info['task_id']}")
    print(f"  项目: {example_task_info['project_path']}")
    print(f"  设计文档: {list(example_task_info['input_files'].keys())}")
    
    print(f"\n产出物文件:")
    for file in example_output_files:
        print(f"  • {file}")
    
    print(f"\n使用方法:")
    print("""
# 在验证子代理中使用:
from verification_template import verify_with_design_documents, save_verification_result

# 运行验证
result = verify_with_design_documents(task_info, output_files)

# 保存结果
result_path = save_verification_result(task_info['task_id'], result)

# 输出结果（验证子代理的最后一步）
print(json.dumps(result, ensure_ascii=False, indent=2))
""")
    
    # 演示仅架构检查
    print(f"\n仅架构检查（向后兼容）:")
    print("""
from verification_template import verify_architecture_only

arch_result = verify_architecture_only('/path/to/code')
print(f"架构合理性: {arch_result['dimension_result']}")
""")