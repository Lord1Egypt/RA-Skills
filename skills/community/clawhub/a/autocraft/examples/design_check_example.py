#!/usr/bin/env python3
"""
设计文档对照验证示例
展示如何在验证子代理中使用设计文档对照验证
"""

import os
import sys
import json
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent / 'scripts' / 'design-check'))

# 模拟验证器，因为实际文件可能不存在
class MockIntegratedValidator:
    def __init__(self, project_path):
        self.project_path = project_path
    
    def run_comprehensive_validation(self, code_files, design_docs, api_code_files=None, model_files=None):
        # 返回模拟结果
        return {
            'verification_success': False,
            'verification_report': "模拟验证报告",
            'dimension_results': {
                '完整性': 'PASS',
                '正确性': 'FAIL',
                '可运行性': 'PASS',
                '一致性': 'PASS',
                '安全性': 'PASS',
                '架构合理性': 'FAIL'
            },
            'issues_found': ["模拟问题1", "模拟问题2"],
            'improvements_suggested': ["模拟建议1", "模拟建议2"],
            'detailed_issues': []
        }

IntegratedValidator = MockIntegratedValidator

def verify_code_with_design_documents(task_info, output_files):
    """
    验证代码（包含设计文档对照）
    
    参数：
    - task_info: 任务信息，包含设计文档路径
    - output_files: 产出物文件列表
    
    返回：
    - 验证结果（验证子代理JSON格式）
    """
    
    # 提取项目路径
    project_path = task_info.get('project_path', '.')
    
    # 提取设计文档路径（从input_files字段）
    design_docs = {}
    if 'input_files' in task_info:
        # input_files格式：{"api_design": "docs/design/07-API设计-DeepTutor-Lite.md", ...}
        design_docs = task_info['input_files']
    else:
        # 向后兼容：从task_info直接提取
        for key in ['api_design', 'system_function_design', 'database_design', 'prd']:
            if key in task_info:
                design_docs[key] = task_info[key]
    
    # 确定API代码文件和模型文件
    api_code_files = []
    model_files = []
    
    for file_path in output_files:
        file_lower = file_path.lower()
        if 'router' in file_lower or 'api' in file_lower:
            api_code_files.append(file_path)
        elif 'model' in file_lower or 'schema' in file_lower:
            model_files.append(file_path)
    
    # 运行集成验证
    validator = IntegratedValidator(project_path)
    
    try:
        result = validator.run_comprehensive_validation(
            code_files=output_files,
            design_docs=design_docs,
            api_code_files=api_code_files if 'api_design' in design_docs else None,
            model_files=model_files if 'database_design' in design_docs else None
        )
        
        # 构建验证子代理格式的结果
        verification_result = {
            'verification_success': result['verification_success'],
            'verification_report': result['verification_report'],
            'dimension_results': result['dimension_results'],
            'issues_found': result['issues_found'],
            'improvements_suggested': result['improvements_suggested']
        }
        
        # 添加设计文档检查详情
        if 'design_docs' in design_docs:
            verification_result['design_document_check'] = {
                'documents_checked': list(design_docs.keys()),
                'coverage_percentage': 100 if result['verification_success'] else 0,
                'missing_endpoints': [issue['description'] for issue in result['detailed_issues'] 
                                     if 'API_' in issue.get('type', '')],
                'missing_functions': [issue['description'] for issue in result['detailed_issues'] 
                                     if 'DESIGN_' in issue.get('type', '')],
                'field_mismatches': [issue['description'] for issue in result['detailed_issues'] 
                                    if 'DATABASE_' in issue.get('type', '')]
            }
        
        return verification_result
        
    except Exception as e:
        # 验证过程中发生错误
        error_report = f"验证过程中发生错误: {str(e)}"
        
        return {
            'verification_success': False,
            'verification_report': error_report,
            'dimension_results': {
                '完整性': 'FAIL',
                '正确性': 'FAIL',
                '可运行性': 'FAIL',
                '一致性': 'FAIL',
                '安全性': 'FAIL',
                '架构合理性': 'FAIL'
            },
            'issues_found': [f"验证工具错误: {str(e)}"],
            'improvements_suggested': ["修复验证工具配置", "检查设计文档路径是否正确"]
        }


def main():
    """示例主函数"""
    print("=" * 80)
    print("设计文档对照验证示例")
    print("=" * 80)
    
    # 示例1：M-01知识图谱管理模块验证
    print("\n📋 示例1：验证M-01知识图谱管理模块")
    
    task_info = {
        'task_id': 'M01-BE-DEV-001',
        'task_name': '知识图谱管理模块开发',
        'project_path': '/data/projects/deeptutor-lite',
        'input_files': {
            'api_design': 'docs/design/07-API设计-DeepTutor-Lite.md',
            'system_function_design': 'docs/design/03-系统功能设计-DeepTutor-Lite.md',
            'database_design': 'docs/design/08-数据库设计-DeepTutor-Lite.md'
        }
    }
    
    output_files = [
        '/data/projects/deeptutor-lite/backend/api/routers/knowledge_graph.py',
        '/data/projects/deeptutor-lite/backend/services/knowledge_graph_service.py',
        '/data/projects/deeptutor-lite/backend/schemas/knowledge_graph.py',
        '/data/projects/deeptutor-lite/backend/models/knowledge_graph.py'
    ]
    
    print(f"任务ID: {task_info['task_id']}")
    print(f"设计文档: {', '.join(task_info['input_files'].keys())}")
    print(f"代码文件: {len(output_files)}个")
    
    # 运行验证（使用模拟数据，因为实际文件可能不存在）
    print("\n🔍 运行验证...")
    
    # 创建模拟验证结果
    mock_result = {
        'verification_success': False,
        'verification_report': """================================================================================
集成验证报告
================================================================================

📊 维度检查结果:
   ❌ 完整性: PASS
   ❌ 正确性: FAIL
   ✅ 可运行性: PASS
   ✅ 一致性: PASS
   ✅ 安全性: PASS
   ❌ 架构合理性: FAIL

🔍 发现问题汇总:

   ARCHITECTURE_SRP_VIOLATION:
     ❌ HIGH: 1个
   DESIGN_MISSING_ENDPOINT:
     ❌ HIGH: 3个

📈 详细统计:
   架构检查: 1个问题 (1高危)
   设计文档对照: 3个问题 (3高危)
   API接口验证: 0个问题 (0高危)
   API覆盖率: 75%
   数据库映射: 0个问题 (0高危)
   表覆盖率: 100%

🎯 总体结论:
   ❌ 验证失败：发现4个高危问题""",
        'dimension_results': {
            '完整性': 'PASS',
            '正确性': 'FAIL',
            '可运行性': 'PASS',
            '一致性': 'PASS',
            '安全性': 'PASS',
            '架构合理性': 'FAIL'
        },
        'issues_found': [
            "路由文件包含业务逻辑类: knowledge_graph.py 包含 KnowledgeGraphParser 和 KnowledgeGraphRepository",
            "缺失API端点: POST /api/knowledge-graph/upload (功能ID: F-001)",
            "缺失API端点: GET /api/knowledge-graph/list (功能ID: F-005)",
            "缺失API端点: GET /api/knowledge-graph/template (功能ID: F-006)"
        ],
        'improvements_suggested': [
            "1. 重构代码架构，遵循单一职责原则",
            "2. 拆分职责混淆的文件，分离路由、服务、数据访问层",
            "3. 对照设计文档，确保功能实现完整",
            "4. 检查设计文档中的功能是否全部实现"
        ],
        'design_document_check': {
            'documents_checked': ['api_design', 'system_function_design', 'database_design'],
            'coverage_percentage': 75,
            'missing_endpoints': [
                "POST /api/knowledge-graph/upload",
                "GET /api/knowledge-graph/list", 
                "GET /api/knowledge-graph/template"
            ],
            'missing_functions': [],
            'field_mismatches': []
        }
    }
    
    # 输出验证结果
    print("\n" + "=" * 80)
    print("验证结果")
    print("=" * 80)
    
    print(f"\n验证成功: {mock_result['verification_success']}")
    
    print(f"\n📊 维度检查结果:")
    for dim, res in mock_result['dimension_results'].items():
        status = '✅' if res == 'PASS' else '❌'
        print(f"  {status} {dim}: {res}")
    
    if mock_result['issues_found']:
        print(f"\n❌ 发现的问题:")
        for issue in mock_result['issues_found']:
            print(f"  • {issue}")
    
    print(f"\n💡 改进建议:")
    for suggestion in mock_result['improvements_suggested']:
        print(f"  • {suggestion}")
    
    # 输出设计文档对照详情
    if 'design_document_check' in mock_result:
        print(f"\n📄 设计文档对照详情:")
        design_check = mock_result['design_document_check']
        print(f"  检查的文档: {', '.join(design_check['documents_checked'])}")
        print(f"  覆盖率: {design_check['coverage_percentage']}%")
        
        if design_check['missing_endpoints']:
            print(f"  缺失的API端点:")
            for endpoint in design_check['missing_endpoints']:
                print(f"    • {endpoint}")
    
    # 示例2：成功验证的示例
    print("\n" + "=" * 80)
    print("📋 示例2：成功验证的模块")
    
    success_mock_result = {
        'verification_success': True,
        'verification_report': """================================================================================
集成验证报告
================================================================================

📊 维度检查结果:
   ✅ 完整性: PASS
   ✅ 正确性: PASS
   ✅ 可运行性: PASS
   ✅ 一致性: PASS
   ✅ 安全性: PASS
   ✅ 架构合理性: PASS

📈 详细统计:
   架构检查: 0个问题 (0高危)
   设计文档对照: 0个问题 (0高危)
   API接口验证: 0个问题 (0高危)
   API覆盖率: 100%
   数据库映射: 0个问题 (0高危)
   表覆盖率: 100%

🎯 总体结论:
   ✅ 验证通过：未发现高危问题""",
        'dimension_results': {
            '完整性': 'PASS',
            '正确性': 'PASS',
            '可运行性': 'PASS',
            '一致性': 'PASS',
            '安全性': 'PASS',
            '架构合理性': 'PASS'
        },
        'issues_found': [],
        'improvements_suggested': ["代码质量优秀，继续保持！"],
        'design_document_check': {
            'documents_checked': ['api_design', 'system_function_design'],
            'coverage_percentage': 100,
            'missing_endpoints': [],
            'missing_functions': [],
            'field_mismatches': []
        }
    }
    
    print(f"\n验证成功: {success_mock_result['verification_success']}")
    print(f"设计文档覆盖率: {success_mock_result['design_document_check']['coverage_percentage']}%")
    print("✅ 所有功能与设计文档完全一致")
    
    # 展示如何在实际验证子代理中使用
    print("\n" + "=" * 80)
    print("🔧 在实际验证子代理中的使用")
    print("=" * 80)
    
    print("""
验证子代理应按照以下步骤进行设计文档对照验证：

1. 从任务信息中提取设计文档路径
   ```python
   design_docs = task_info.get('input_files', {})
   ```

2. 加载并运行集成验证
   ```python
   validator = IntegratedValidator(project_path)
   result = validator.run_comprehensive_validation(
       code_files=output_files,
       design_docs=design_docs,
       api_code_files=api_files,
       model_files=model_files
   )
   ```

3. 构建验证结果JSON
   ```python
   verification_result = {
       'verification_success': result['verification_success'],
       'verification_report': result['verification_report'],
       'dimension_results': result['dimension_results'],
       'issues_found': result['issues_found'],
       'improvements_suggested': result['improvements_suggested']
   }
   ```

4. 保存结果文件
   ```python
   output_path = f"/tmp/autocraft_output/{task_id}_verification_result.json"
   with open(output_path, 'w', encoding='utf-8') as f:
       json.dump(verification_result, f, ensure_ascii=False, indent=2)
   ```
""")
    
    print("\n🎯 关键改进：")
    print("• 验证子代理现在可以自动检查代码是否严格遵循设计文档")
    print("• 防止类似 knowledge_graph.py 的职责混淆问题")
    print("• 确保功能完整性，避免遗漏设计文档中的功能")
    print("• 提高代码质量，减少技术债务")


if __name__ == '__main__':
    main()