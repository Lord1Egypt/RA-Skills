#!/usr/bin/env python3
"""
数据库映射验证工具
验证代码中的数据模型是否与数据库设计文档一致
"""

import re
import json
import logging
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseMappingVerifier:
    """数据库映射验证器"""
    
    def __init__(self):
        self.design_tables = {}
        self.code_models = {}
        self.issues = []
    
    def load_database_design(self, design_path: str) -> bool:
        """加载数据库设计文档"""
        try:
            with open(design_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析数据库设计文档
            self.design_tables = self._parse_database_design(content)
            logger.info(f"加载数据库设计文档成功: {design_path} ({len(self.design_tables)}个表)")
            return True
            
        except Exception as e:
            logger.error(f"加载数据库设计文档失败: {str(e)}")
            return False
    
    def _parse_database_design(self, content: str) -> Dict[str, Any]:
        """解析数据库设计文档内容"""
        tables = {}
        
        # 提取表定义
        # 格式：### 知识图谱表 (knowledge_graph)
        table_pattern = r'###\s*([^\n]+)\s*\(([^)]+)\)'
        table_matches = re.findall(table_pattern, content)
        
        for table_name, table_code in table_matches:
            # 提取表描述部分
            desc_pattern = rf'###\s*{re.escape(table_name)}[^\n]+\n(.*?)(?=###|\Z)'
            desc_match = re.search(desc_pattern, content, re.DOTALL)
            
            if not desc_match:
                continue
            
            table_content = desc_match.group(1)
            
            # 提取字段定义（表格格式）
            # | 字段名 | 类型 | 约束 | 说明 |
            field_pattern = r'\|\s*(\w+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
            field_matches = re.findall(field_pattern, table_content)
            
            fields = []
            for field_name, field_type, field_constraint, field_desc in field_matches:
                fields.append({
                    'name': field_name.strip(),
                    'type': field_type.strip(),
                    'constraint': field_constraint.strip(),
                    'description': field_desc.strip()
                })
            
            # 提取主键
            primary_key_match = re.search(r'主键\s*:\s*`([^`]+)`', table_content)
            primary_key = primary_key_match.group(1) if primary_key_match else ''
            
            # 提取索引
            indexes = []
            index_pattern = r'索引\s*:\s*`([^`]+)`\s*\(([^)]+)\)'
            index_matches = re.findall(index_pattern, table_content)
            for index_name, index_fields in index_matches:
                indexes.append({
                    'name': index_name.strip(),
                    'fields': [f.strip() for f in index_fields.split(',')]
                })
            
            tables[table_code] = {
                'name': table_name.strip(),
                'code': table_code.strip(),
                'fields': fields,
                'primary_key': primary_key,
                'indexes': indexes,
                'total_fields': len(fields)
            }
        
        return tables
    
    def extract_models_from_code(self, code_path: str) -> Dict[str, Any]:
        """从代码中提取数据模型定义"""
        try:
            with open(code_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            models = {}
            
            # 识别模型文件类型
            file_name = Path(code_path).name.lower()
            
            if 'model' in file_name or file_name.endswith('.py'):
                # SQLAlchemy模型
                models.update(self._extract_sqlalchemy_models(content, code_path))
            elif 'schema' in file_name:
                # Pydantic模型
                models.update(self._extract_pydantic_models(content, code_path))
            
            logger.info(f"从代码中提取数据模型: {code_path} ({len(models)}个模型)")
            return models
            
        except Exception as e:
            logger.error(f"提取数据模型失败 {code_path}: {str(e)}")
            return {}
    
    def _extract_sqlalchemy_models(self, content: str, file_path: str) -> Dict[str, Any]:
        """提取SQLAlchemy模型定义"""
        models = {}
        
        # 查找类定义（SQLAlchemy模型）
        class_pattern = r'class\s+(\w+)\s*\(.*?Base.*?\):'
        class_matches = re.findall(class_pattern, content, re.DOTALL)
        
        for class_name in class_matches:
            # 提取类内容
            class_content_pattern = rf'class\s+{re.escape(class_name)}\s*\([^)]+\):\s*(.*?)(?=class\s+\w+\s*\(|\Z)'
            class_content_match = re.search(class_content_pattern, content, re.DOTALL)
            
            if not class_content_match:
                continue
            
            class_content = class_content_match.group(1)
            
            # 提取字段定义
            fields = []
            
            # Column定义
            column_pattern = r'(\w+)\s*=\s*Column\(([^)]+)\)'
            column_matches = re.findall(column_pattern, class_content)
            
            for field_name, column_args in column_matches:
                # 解析Column参数
                field_type = self._parse_column_type(column_args)
                constraints = self._parse_column_constraints(column_args)
                
                fields.append({
                    'name': field_name,
                    'type': field_type,
                    'constraints': constraints,
                    'source': 'sqlalchemy'
                })
            
            # 关系定义
            relationship_pattern = r'(\w+)\s*=\s*relationship\(([^)]+)\)'
            relationship_matches = re.findall(relationship_pattern, class_content)
            
            for rel_name, rel_args in relationship_matches:
                # 解析关系
                rel_type = self._parse_relationship_type(rel_args)
                
                fields.append({
                    'name': rel_name,
                    'type': 'relationship',
                    'relationship_type': rel_type,
                    'source': 'sqlalchemy'
                })
            
            models[class_name.lower()] = {
                'name': class_name,
                'type': 'sqlalchemy',
                'file': file_path,
                'fields': fields,
                'total_fields': len(fields)
            }
        
        return models
    
    def _extract_pydantic_models(self, content: str, file_path: str) -> Dict[str, Any]:
        """提取Pydantic模型定义"""
        models = {}
        
        # 查找类定义（Pydantic模型）
        class_pattern = r'class\s+(\w+)\s*\(.*?(?:BaseModel|BaseSchema).*?\):'
        class_matches = re.findall(class_pattern, content, re.DOTALL)
        
        for class_name in class_matches:
            # 提取类内容
            class_content_pattern = rf'class\s+{re.escape(class_name)}\s*\([^)]+\):\s*(.*?)(?=class\s+\w+\s*\(|\Z)'
            class_content_match = re.search(class_content_pattern, content, re.DOTALL)
            
            if not class_content_match:
                continue
            
            class_content = class_content_match.group(1)
            
            # 提取字段定义
            fields = []
            
            # 字段定义模式
            field_patterns = [
                r'(\w+)\s*:\s*([^\n#]+)',  # field: type
                r'(\w+)\s*=\s*Field\(([^)]+)\)'  # field = Field(...)
            ]
            
            for pattern in field_patterns:
                field_matches = re.findall(pattern, class_content)
                for field_name, field_def in field_matches:
                    field_type = self._parse_pydantic_type(field_def)
                    
                    fields.append({
                        'name': field_name,
                        'type': field_type,
                        'source': 'pydantic'
                    })
            
            models[class_name.lower()] = {
                'name': class_name,
                'type': 'pydantic',
                'file': file_path,
                'fields': fields,
                'total_fields': len(fields)
            }
        
        return models
    
    def _parse_column_type(self, column_args: str) -> str:
        """解析Column类型"""
        # 提取类型参数
        type_pattern = r'(\w+)\s*\(|(\w+)\s*,'
        type_match = re.search(type_pattern, column_args)
        
        if type_match:
            return type_match.group(1) or type_match.group(2) or 'unknown'
        
        # 简单类型
        simple_types = ['Integer', 'String', 'Text', 'DateTime', 'Boolean', 'Float', 'Numeric']
        for simple_type in simple_types:
            if simple_type in column_args:
                return simple_type
        
        return 'unknown'
    
    def _parse_column_constraints(self, column_args: str) -> Dict[str, Any]:
        """解析Column约束"""
        constraints = {}
        
        # 检查主键
        if 'primary_key=True' in column_args:
            constraints['primary_key'] = True
        
        # 检查外键
        foreign_key_match = re.search(r'ForeignKey\(["\']([^"\']+)["\']\)', column_args)
        if foreign_key_match:
            constraints['foreign_key'] = foreign_key_match.group(1)
        
        # 检查唯一约束
        if 'unique=True' in column_args:
            constraints['unique'] = True
        
        # 检查可为空
        if 'nullable=False' in column_args:
            constraints['nullable'] = False
        elif 'nullable=True' in column_args:
            constraints['nullable'] = True
        
        # 检查默认值
        default_match = re.search(r'default=([^,]+)', column_args)
        if default_match:
            constraints['default'] = default_match.group(1)
        
        return constraints
    
    def _parse_relationship_type(self, rel_args: str) -> str:
        """解析关系类型"""
        if '"many-to-one"' in rel_args or "'many-to-one'" in rel_args:
            return 'many-to-one'
        elif '"one-to-many"' in rel_args or "'one-to-many'" in rel_args:
            return 'one-to-many'
        elif '"one-to-one"' in rel_args or "'one-to-one'" in rel_args:
            return 'one-to-one'
        elif '"many-to-many"' in rel_args or "'many-to-many'" in rel_args:
            return 'many-to-many'
        
        return 'unknown'
    
    def _parse_pydantic_type(self, field_def: str) -> str:
        """解析Pydantic字段类型"""
        # 提取类型注解
        type_pattern = r'(\w+)\s*\[|(\w+)\s*$'
        type_match = re.search(type_pattern, field_def.strip())
        
        if type_match:
            return type_match.group(1) or type_match.group(2) or 'unknown'
        
        # 常见类型
        common_types = ['str', 'int', 'float', 'bool', 'datetime', 'date', 'list', 'dict']
        for common_type in common_types:
            if common_type in field_def.lower():
                return common_type
        
        return 'unknown'
    
    def verify_database_mapping(self, design_path: str, code_paths: List[str]) -> Dict[str, Any]:
        """验证数据库映射一致性"""
        # 加载设计文档
        if not self.load_database_design(design_path):
            return {
                'success': False,
                'error': '无法加载数据库设计文档',
                'issues': []
            }
        
        # 从代码中提取模型
        self.code_models = {}
        for code_path in code_paths:
            models = self.extract_models_from_code(code_path)
            self.code_models.update(models)
        
        # 执行验证
        self._verify_table_coverage()
        self._verify_field_mapping()
        self._verify_constraints()
        
        # 生成报告
        return self.generate_report()
    
    def _verify_table_coverage(self):
        """验证表覆盖：设计文档中的表是否都在代码中有对应模型"""
        for table_code, table_info in self.design_tables.items():
            table_name = table_info['name']
            
            # 查找匹配的代码模型
            matched = False
            for model_name, model_info in self.code_models.items():
                # 检查模型名是否与表名或表代码匹配
                if (table_name.lower() in model_name or 
                    table_code.lower() in model_name or
                    model_name in table_name.lower() or
                    model_name in table_code.lower()):
                    matched = True
                    break
            
            if not matched:
                self.issues.append({
                    'type': 'MISSING_MODEL',
                    'severity': 'HIGH',
                    'description': f"设计文档中的表没有对应的代码模型: {table_name} ({table_code})",
                    'design_table': table_info,
                    'suggestion': f"需要创建对应的数据模型类: class {table_name.capitalize()}(Base)"
                })
    
    def _verify_field_mapping(self):
        """验证字段映射：设计文档中的字段是否都在代码模型中有对应"""
        for table_code, table_info in self.design_tables.items():
            table_name = table_info['name']
            
            # 查找对应的代码模型
            matched_model = None
            for model_name, model_info in self.code_models.items():
                if (table_name.lower() in model_name or 
                    table_code.lower() in model_name):
                    matched_model = model_info
                    break
            
            if not matched_model:
                continue
            
            # 检查字段映射
            for design_field in table_info['fields']:
                field_name = design_field['name']
                field_type = design_field['type']
                
                # 在代码模型中查找字段
                field_found = False
                for code_field in matched_model['fields']:
                    if code_field['name'].lower() == field_name.lower():
                        field_found = True
                        
                        # 检查类型是否匹配
                        if not self._types_match(field_type, code_field['type']):
                            self.issues.append({
                                'type': 'FIELD_TYPE_MISMATCH',
                                'severity': 'MEDIUM',
                                'description': f"字段类型不匹配: {table_name}.{field_name} (设计: {field_type}, 代码: {code_field['type']})",
                                'design_field': design_field,
                                'code_field': code_field,
                                'suggestion': f"将代码中的类型从 {code_field['type']} 改为 {field_type}"
                            })
                        break
                
                if not field_found:
                    self.issues.append({
                        'type': 'MISSING_FIELD',
                        'severity': 'HIGH',
                        'description': f"设计文档中的字段未在代码模型中定义: {table_name}.{field_name}",
                        'design_field': design_field,
                        'suggestion': f"在模型 {matched_model['name']} 中添加字段: {field_name}"
                    })
    
    def _verify_constraints(self):
        """验证约束：主键、外键、唯一约束等"""
        for table_code, table_info in self.design_tables.items():
            table_name = table_info['name']
            
            # 查找对应的代码模型
            matched_model = None
            for model_name, model_info in self.code_models.items():
                if (table_name.lower() in model_name or 
                    table_code.lower() in model_name):
                    matched_model = model_info
                    break
            
            if not matched_model:
                continue
            
            # 检查主键
            design_pk = table_info.get('primary_key', '')
            if design_pk:
                # 在代码模型中查找主键
                pk_found = False
                for code_field in matched_model['fields']:
                    if (code_field['name'].lower() == design_pk.lower() and 
                        code_field.get('constraints', {}).get('primary_key')):
                        pk_found = True
                        break
                
                if not pk_found:
                    self.issues.append({
                        'type': 'MISSING_PRIMARY_KEY',
                        'severity': 'HIGH',
                        'description': f"设计文档中的主键未在代码模型中定义: {table_name}.{design_pk}",
                        'design_table': table_info,
                        'suggestion': f"在模型 {matched_model['name']} 中将字段 {design_pk} 设置为 primary_key=True"
                    })
            
            # 检查索引
            for index in table_info.get('indexes', []):
                index_name = index['name']
                index_fields = index['fields']
                
                # 简单的索引检查（可以改进）
                # 检查索引字段是否都在模型中存在
                missing_index_fields = []
                for index_field in index_fields:
                    field_found = False
                    for code_field in matched_model['fields']:
                        if code_field['name'].lower() == index_field.lower():
                            field_found = True
                            break
                    
                    if not field_found:
                        missing_index_fields.append(index_field)
                
                if missing_index_fields:
                    self.issues.append({
                        'type': 'INVALID_INDEX',
                        'severity': 'MEDIUM',
                        'description': f"索引字段不存在: {table_name}.{index_name} (缺失字段: {', '.join(missing_index_fields)})",
                        'design_index': index,
                        'suggestion': f"添加缺失的字段或修正索引定义"
                    })
    
    def _types_match(self, design_type: str, code_type: str) -> bool:
        """判断类型是否匹配"""
        # 类型映射
        type_mapping = {
            # 数据库类型 -> 代码类型
            'VARCHAR': ['str', 'string'],
            'INT': ['int', 'integer'],
            'BIGINT': ['int', 'integer'],
            'TEXT': ['str', 'string', 'text'],
            'DATETIME': ['datetime', 'timestamp'],
            'BOOLEAN': ['bool', 'boolean'],
            'FLOAT': ['float'],
            'DECIMAL': ['float', 'decimal'],
            'JSON': ['dict', 'json']
        }
        
        design_type_lower = design_type.lower()
        code_type_lower = code_type.lower()
        
        # 完全匹配
        if design_type_lower == code_type_lower:
            return True
        
        # 检查类型映射
        for db_type, code_types in type_mapping.items():
            if db_type.lower() in design_type_lower:
                for allowed_code_type in code_types:
                    if allowed_code_type in code_type_lower:
                        return True
        
        return False
    
    def generate_report(self) -> Dict[str, Any]:
        """生成验证报告"""
        total_issues = len(self.issues)
        high_severity = sum(1 for issue in self.issues if issue['severity'] == 'HIGH')
        medium_severity = sum(1 for issue in self.issues if issue['severity'] == 'MEDIUM')
        
        # 统计表数量
        design_table_count = len(self.design_tables)
        code_model_count = len(self.code_models)
        
        # 计算覆盖率
        matched_tables = 0
        for table_code, table_info in self.design_tables.items():
            for model_name, model_info in self.code_models.items():
                if (table_info['name'].lower() in model_name or 
                    table_code.lower() in model_name):
                    matched_tables += 1
                    break
        
        table_coverage = matched_tables / design_table_count * 100 if design_table_count > 0 else 0
        
        # 字段统计
        total_design_fields = sum(table['total_fields'] for table in self.design_tables.values())
        total_code_fields = sum(model['total_fields'] for model in self.code_models.values())
        
        report = {
            'summary': {
                'design_tables': design_table_count,
                'code_models': code_model_count,
                'matched_tables': matched_tables,
                'table_coverage_percentage': round(table_coverage, 2),
                'total_design_fields': total_design_fields,
                'total_code_fields': total_code_fields,
                'total_issues': total_issues,
                'high_severity_issues': high_severity,
                'medium_severity_issues': medium_severity
            },
            'design_tables': self.design_tables,
            'code_models': self.code_models,
            'issues': self.issues,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if self.issues:
            # 根据问题类型生成建议
            missing_models = [i for i in self.issues if i['type'] == 'MISSING_MODEL']
            missing_fields = [i for i in self.issues if i['type'] == 'MISSING_FIELD']
            field_type_mismatches = [i for i in self.issues if i['type'] == 'FIELD_TYPE_MISMATCH']
            missing_pks = [i for i in self.issues if i['type'] == 'MISSING_PRIMARY_KEY']
            
            if missing_models:
                recommendations.append(f"需要创建 {len(missing_models)} 个缺失的数据模型")
            
            if missing_fields:
                recommendations.append(f"需要添加 {len(missing_fields)} 个缺失的字段")
            
            if field_type_mismatches:
                recommendations.append(f"需要修正 {len(field_type_mismatches)} 个字段类型不匹配")
            
            if missing_pks:
                recommendations.append(f"需要设置 {len(missing_pks)} 个缺失的主键")
        else:
            recommendations.append("数据模型与数据库设计完全一致")
        
        # 覆盖率建议
        coverage = self.generate_report()['summary']['table_coverage_percentage']
        if coverage < 100:
            recommendations.append(f"数据模型覆盖率为 {coverage}%，需要提高覆盖率")
        else:
            recommendations.append("数据模型覆盖率100%，优秀！")
        
        return recommendations


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库映射验证工具')
    parser.add_argument('--design', required=True, help='数据库设计文档路径')
    parser.add_argument('--code', required=True, nargs='+', help='要检查的代码文件路径')
    parser.add_argument('--report', help='JSON报告输出路径')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 设置日志
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行验证
    verifier = DatabaseMappingVerifier()
    report = verifier.verify_database_mapping(args.design, args.code)
    
    # 输出报告
    print("=" * 80)
    print("数据库映射验证报告")
    print("=" * 80)
    
    summary = report['summary']
    print(f"\n📊 数据模型统计")
    print(f"   设计文档表: {summary['design_tables']}个")
    print(f"   代码模型: {summary['code_models']}个")
    print(f"   匹配的表: {summary['matched_tables']}个")
    print(f"   表覆盖率: {summary['table_coverage_percentage']}%")
    print(f"   设计文档字段: {summary['total_design_fields']}个")
    print(f"   代码字段: {summary['total_code_fields']}个")
    
    print(f"\n🔍 问题统计")
    print(f"   总问题数: {summary['total_issues']}")
    print(f"   高危问题: {summary['high_severity_issues']}")
    print(f"   中危问题: {summary['medium_severity_issues']}")
    
    if report['issues']:
        print(f"\n❌ 发现的问题:")
        for i, issue in enumerate(report['issues'], 1):
            severity_icon = '❌' if issue['severity'] == 'HIGH' else '⚠️'
            print(f"   {severity_icon} [{issue['severity']}] {issue['type']}: {issue['description']}")
    else:
        print(f"\n✅ 未发现问题，数据模型与数据库设计一致")
    
    print(f"\n💡 改进建议:")
    for rec in report['recommendations']:
        print(f"   • {rec}")
    
    # 保存JSON报告
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON报告已保存到: {args.report}")
    
    return 0 if summary['high_severity_issues'] == 0 else 1


if __name__ == '__main__':
    exit(main())