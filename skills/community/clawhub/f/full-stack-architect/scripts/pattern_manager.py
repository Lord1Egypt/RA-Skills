#!/usr/bin/env python3
"""
模式库管理脚本
用于收集、整理和共享可复用的模式
"""

import os
import json
import re
from datetime import datetime

class PatternManager:
    def __init__(self):
        self.conventions_dir = os.path.join(os.path.dirname(__file__), '../../prd-context/conventions')
        self.patterns_file = os.path.join(self.conventions_dir, 'agents.md')
        self.patterns_json_file = os.path.join(self.conventions_dir, 'patterns.json')
        
        # 创建必要的目录
        if not os.path.exists(self.conventions_dir):
            os.makedirs(self.conventions_dir)
        
        # 初始化模式文件
        self._init_patterns_file()
    
    def _init_patterns_file(self):
        """初始化模式文件"""
        if not os.path.exists(self.patterns_file):
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                f.write("# 可复用模式\n\n")
        
        if not os.path.exists(self.patterns_json_file):
            with open(self.patterns_json_file, 'w', encoding='utf-8') as f:
                json.dump({'patterns': []}, f, ensure_ascii=False, indent=2)
    
    def add_pattern(self, name, domain, description, example, tags=None):
        """添加新模式
        
        Args:
            name: 模式名称
            domain: 技术领域
            description: 模式描述
            example: 代码示例
            tags: 标签列表
            
        Returns:
            pattern_id: 模式ID
        """
        # 加载现有模式
        patterns = self.get_patterns()
        
        # 生成模式ID
        pattern_id = len(patterns) + 1
        
        # 创建新模式
        pattern = {
            'id': pattern_id,
            'name': name,
            'domain': domain,
            'description': description,
            'example': example,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # 添加到模式列表
        patterns.append(pattern)
        
        # 保存到JSON文件
        self._save_patterns(patterns)
        
        # 更新Markdown文件
        self._update_patterns_md(patterns)
        
        print(f"模式添加成功: {name} (ID: {pattern_id})")
        return pattern_id
    
    def get_patterns(self):
        """获取所有模式
        
        Returns:
            patterns: 模式列表
        """
        try:
            with open(self.patterns_json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('patterns', [])
        except Exception as e:
            print(f"加载模式失败: {str(e)}")
            return []
    
    def get_pattern_by_id(self, pattern_id):
        """根据ID获取模式
        
        Args:
            pattern_id: 模式ID
            
        Returns:
            pattern: 模式对象
        """
        patterns = self.get_patterns()
        for pattern in patterns:
            if pattern['id'] == pattern_id:
                return pattern
        return None
    
    def update_pattern(self, pattern_id, **kwargs):
        """更新模式
        
        Args:
            pattern_id: 模式ID
            **kwargs: 要更新的字段
            
        Returns:
            success: 是否更新成功
        """
        patterns = self.get_patterns()
        updated = False
        
        for pattern in patterns:
            if pattern['id'] == pattern_id:
                for key, value in kwargs.items():
                    if key in pattern:
                        pattern[key] = value
                pattern['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            self._save_patterns(patterns)
            self._update_patterns_md(patterns)
            print(f"模式更新成功: ID {pattern_id}")
        else:
            print(f"模式不存在: ID {pattern_id}")
        
        return updated
    
    def delete_pattern(self, pattern_id):
        """删除模式
        
        Args:
            pattern_id: 模式ID
            
        Returns:
            success: 是否删除成功
        """
        patterns = self.get_patterns()
        new_patterns = [p for p in patterns if p['id'] != pattern_id]
        
        if len(new_patterns) != len(patterns):
            self._save_patterns(new_patterns)
            self._update_patterns_md(new_patterns)
            print(f"模式删除成功: ID {pattern_id}")
            return True
        else:
            print(f"模式不存在: ID {pattern_id}")
            return False
    
    def search_patterns(self, query):
        """搜索模式
        
        Args:
            query: 搜索关键词
            
        Returns:
            results: 搜索结果
        """
        patterns = self.get_patterns()
        results = []
        
        query_lower = query.lower()
        for pattern in patterns:
            if (query_lower in pattern['name'].lower() or 
                query_lower in pattern['domain'].lower() or 
                query_lower in pattern['description'].lower() or
                any(query_lower in tag.lower() for tag in pattern['tags'])):
                results.append(pattern)
        
        return results
    
    def _save_patterns(self, patterns):
        """保存模式到JSON文件
        
        Args:
            patterns: 模式列表
        """
        try:
            with open(self.patterns_json_file, 'w', encoding='utf-8') as f:
                json.dump({'patterns': patterns}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存模式失败: {str(e)}")
    
    def _update_patterns_md(self, patterns):
        """更新Markdown格式的模式文件
        
        Args:
            patterns: 模式列表
        """
        try:
            # 按领域分组
            patterns_by_domain = {}
            for pattern in patterns:
                domain = pattern['domain']
                if domain not in patterns_by_domain:
                    patterns_by_domain[domain] = []
                patterns_by_domain[domain].append(pattern)
            
            # 生成Markdown内容
            md_content = "# 可复用模式\n\n"
            
            for domain, domain_patterns in patterns_by_domain.items():
                md_content += f"## {domain}\n\n"
                
                for pattern in domain_patterns:
                    md_content += f"### {pattern['name']}\n"
                    md_content += f"- **描述**：{pattern['description']}\n"
                    if pattern['tags']:
                        md_content += f"- **标签**：{', '.join(pattern['tags'])}\n"
                    md_content += f"- **创建时间**：{pattern['created_at']}\n"
                    md_content += f"- **代码示例**：\n"
                    md_content += f"  ```{self._guess_language(pattern['example'])}\n"
                    md_content += f"  {pattern['example']}\n"
                    md_content += f"  ```\n\n"
            
            # 保存到文件
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
        except Exception as e:
            print(f"更新模式Markdown文件失败: {str(e)}")
    
    def _guess_language(self, code):
        """猜测代码语言
        
        Args:
            code: 代码示例
            
        Returns:
            language: 语言名称
        """
        if 'const' in code and '=>' in code:
            return 'javascript'
        elif 'def' in code and 'import' in code:
            return 'python'
        elif 'function' in code and '{' in code:
            return 'javascript'
        elif 'class' in code and '{' in code:
            return 'java'
        elif 'SELECT' in code or 'INSERT' in code:
            return 'sql'
        else:
            return 'code'
    
    def import_patterns(self, import_file):
        """从文件导入模式
        
        Args:
            import_file: 导入文件路径
            
        Returns:
            imported_count: 导入的模式数量
        """
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
                imported_patterns = imported_data.get('patterns', [])
        except Exception as e:
            print(f"导入文件读取失败: {str(e)}")
            return 0
        
        existing_patterns = self.get_patterns()
        existing_names = {p['name'] for p in existing_patterns}
        
        new_patterns = []
        for pattern in imported_patterns:
            if pattern['name'] not in existing_names:
                # 生成新ID
                pattern['id'] = len(existing_patterns) + len(new_patterns) + 1
                pattern['created_at'] = datetime.now().isoformat()
                pattern['updated_at'] = datetime.now().isoformat()
                new_patterns.append(pattern)
        
        if new_patterns:
            all_patterns = existing_patterns + new_patterns
            self._save_patterns(all_patterns)
            self._update_patterns_md(all_patterns)
            print(f"成功导入 {len(new_patterns)} 个模式")
        else:
            print("没有新模式可导入")
        
        return len(new_patterns)
    
    def export_patterns(self, export_file):
        """导出模式到文件
        
        Args:
            export_file: 导出文件路径
            
        Returns:
            success: 是否导出成功
        """
        try:
            patterns = self.get_patterns()
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump({'patterns': patterns}, f, ensure_ascii=False, indent=2)
            print(f"模式导出成功: {export_file}")
            return True
        except Exception as e:
            print(f"模式导出失败: {str(e)}")
            return False

if __name__ == "__main__":
    import sys
    
    manager = PatternManager()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python pattern_manager.py add <名称> <领域> <描述> <示例> [标签1,标签2,...]")
        print("  python pattern_manager.py list")
        print("  python pattern_manager.py get <ID>")
        print("  python pattern_manager.py update <ID> --name <名称> --domain <领域> --description <描述> --example <示例> --tags <标签>")
        print("  python pattern_manager.py delete <ID>")
        print("  python pattern_manager.py search <关键词>")
        print("  python pattern_manager.py import <文件路径>")
        print("  python pattern_manager.py export <文件路径>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 6:
            print("参数不足: python pattern_manager.py add <名称> <领域> <描述> <示例> [标签1,标签2,...]")
            sys.exit(1)
        
        name = sys.argv[2]
        domain = sys.argv[3]
        description = sys.argv[4]
        example = sys.argv[5]
        tags = sys.argv[6].split(',') if len(sys.argv) > 6 else []
        
        manager.add_pattern(name, domain, description, example, tags)
    
    elif command == 'list':
        patterns = manager.get_patterns()
        print(f"共 {len(patterns)} 个模式:")
        for pattern in patterns:
            print(f"ID: {pattern['id']}, 名称: {pattern['name']}, 领域: {pattern['domain']}")
    
    elif command == 'get':
        if len(sys.argv) != 3:
            print("参数不足: python pattern_manager.py get <ID>")
            sys.exit(1)
        
        pattern_id = int(sys.argv[2])
        pattern = manager.get_pattern_by_id(pattern_id)
        if pattern:
            print(f"ID: {pattern['id']}")
            print(f"名称: {pattern['name']}")
            print(f"领域: {pattern['domain']}")
            print(f"描述: {pattern['description']}")
            print(f"标签: {', '.join(pattern['tags'])}")
            print(f"示例: {pattern['example']}")
        else:
            print(f"模式不存在: ID {pattern_id}")
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("参数不足: python pattern_manager.py update <ID> --name <名称> --domain <领域> --description <描述> --example <示例> --tags <标签>")
            sys.exit(1)
        
        pattern_id = int(sys.argv[2])
        kwargs = {}
        
        for i in range(3, len(sys.argv), 2):
            if i + 1 >= len(sys.argv):
                break
            key = sys.argv[i].lstrip('--')
            value = sys.argv[i + 1]
            if key == 'tags':
                value = value.split(',')
            kwargs[key] = value
        
        manager.update_pattern(pattern_id, **kwargs)
    
    elif command == 'delete':
        if len(sys.argv) != 3:
            print("参数不足: python pattern_manager.py delete <ID>")
            sys.exit(1)
        
        pattern_id = int(sys.argv[2])
        manager.delete_pattern(pattern_id)
    
    elif command == 'search':
        if len(sys.argv) != 3:
            print("参数不足: python pattern_manager.py search <关键词>")
            sys.exit(1)
        
        query = sys.argv[2]
        results = manager.search_patterns(query)
        print(f"搜索 '{query}' 结果: {len(results)} 个模式")
        for pattern in results:
            print(f"ID: {pattern['id']}, 名称: {pattern['name']}, 领域: {pattern['domain']}")
    
    elif command == 'import':
        if len(sys.argv) != 3:
            print("参数不足: python pattern_manager.py import <文件路径>")
            sys.exit(1)
        
        import_file = sys.argv[2]
        manager.import_patterns(import_file)
    
    elif command == 'export':
        if len(sys.argv) != 3:
            print("参数不足: python pattern_manager.py export <文件路径>")
            sys.exit(1)
        
        export_file = sys.argv[2]
        manager.export_patterns(export_file)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
