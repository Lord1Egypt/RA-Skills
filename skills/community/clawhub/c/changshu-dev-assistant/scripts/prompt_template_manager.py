#!/usr/bin/env python3
"""
Prompt模板管理器
为昌叔量身定制的Prompt模板管理工具, 支持渲染/增删/持久化
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


class PromptTemplateManager:
    """Prompt模板管理器, 支持持久化到JSON文件"""

    DEFAULT_TEMPLATES_PATH = os.path.expanduser("~/.hermes/changshu_prompt_templates.json")

    DEFAULT_TEMPLATES = {
        "database": {
            "code_review": {
                "template": "请审查以下达梦数据库存储过程代码，识别潜在问题并提供修复建议：\n\n{code}\n\n请按照以下格式输出审查结果：\n1. 问题描述\n2. 问题位置\n3. 修复建议\n4. 修复后的代码",
                "description": "达梦数据库代码审查模板"
            }
        }
    }

    def __init__(self, config_path: str = None):
        """初始化Prompt模板管理器

        Args:
            config_path: 模板持久化文件路径, 默认 ~/.hermes/changshu_prompt_templates.json
        """
        self.config_path = config_path or self.DEFAULT_TEMPLATES_PATH
        self.templates: Dict = {}
        self._load()

    def _load(self):
        """从JSON文件加载模板, 文件不存在时使用默认模板"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.templates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.templates = self._deep_copy_templates(self.DEFAULT_TEMPLATES)
            self._save()

    def _save(self):
        """将模板持久化到JSON文件"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _deep_copy_templates(templates: Dict) -> Dict:
        """深拷贝模板字典"""
        return json.loads(json.dumps(templates))

    def load(self):
        """重新从文件加载模板"""
        self._load()

    def get_template(self, category: str, task: str) -> Optional[str]:
        """获取指定类别和任务的Prompt模板

        Args:
            category: 类别名
            task: 任务名

        Returns:
            模板字符串, 不存在时返回None
        """
        try:
            return self.templates[category][task]["template"]
        except KeyError:
            return None

    def list_categories(self) -> List[str]:
        """列出所有类别"""
        return list(self.templates.keys())

    def list_tasks(self, category: str) -> List[str]:
        """列出指定类别下的所有任务

        Args:
            category: 类别名

        Returns:
            任务名列表
        """
        if category in self.templates:
            return list(self.templates[category].keys())
        return []

    def render_template(self, category: str, task: str, variables: Dict = None) -> Optional[str]:
        """渲染模板, 将 {var_name} 替换为变量值

        Args:
            category: 类别名
            task: 任务名
            variables: 变量字典, 如 {"code": "SELECT * FROM t"}

        Returns:
            渲染后的字符串, 模板不存在时返回None
        """
        template = self.get_template(category, task)
        if template is None:
            return None
        if variables is None:
            return template
        result = template
        for key, value in variables.items():
            result = result.replace("{" + key + "}", str(value))
        return result

    def add_template(self, category: str, task: str, template: str, description: str = ""):
        """添加新模板并持久化

        Args:
            category: 类别名
            task: 任务名
            template: 模板内容, 支持 {var_name} 占位符
            description: 模板描述
        """
        if category not in self.templates:
            self.templates[category] = {}
        self.templates[category][task] = {
            "template": template,
            "description": description,
        }
        self._save()

    def delete_template(self, category: str, task: str) -> bool:
        """删除指定模板并持久化

        Args:
            category: 类别名
            task: 任务名

        Returns:
            是否成功删除
        """
        if category not in self.templates:
            return False
        if task not in self.templates[category]:
            return False
        del self.templates[category][task]
        # 如果类别下已无任务, 删除整个类别
        if not self.templates[category]:
            del self.templates[category]
        self._save()
        return True


def main():
    """CLI入口"""
    if len(sys.argv) < 2:
        print("用法: python3 prompt_template_manager.py [list|get|render|add|delete]")
        sys.exit(1)

    command = sys.argv[1]
    manager = PromptTemplateManager()

    if command == "list":
        categories = manager.list_categories()
        if not categories:
            print("暂无模板类别")
        else:
            for cat in categories:
                print(f"类别: {cat}")
                for task in manager.list_tasks(cat):
                    desc = manager.templates[cat][task].get("description", "")
                    print(f"  - {task}: {desc}")
    elif command == "get":
        if len(sys.argv) < 4:
            print("用法: python3 prompt_template_manager.py get <category> <task>")
            sys.exit(1)
        template = manager.get_template(sys.argv[2], sys.argv[3])
        if template:
            print(template)
        else:
            print("模板未找到")
    elif command == "render":
        if len(sys.argv) < 4:
            print("用法: python3 prompt_template_manager.py render <category> <task> [key=value ...]")
            sys.exit(1)
        variables = {}
        for arg in sys.argv[4:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                variables[k] = v
        result = manager.render_template(sys.argv[2], sys.argv[3], variables)
        if result:
            print(result)
        else:
            print("模板未找到")
    elif command == "add":
        if len(sys.argv) < 5:
            print("用法: python3 prompt_template_manager.py add <category> <task> <template>")
            sys.exit(1)
        manager.add_template(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"已添加模板: {sys.argv[2]}/{sys.argv[3]}")
    elif command == "delete":
        if len(sys.argv) < 4:
            print("用法: python3 prompt_template_manager.py delete <category> <task>")
            sys.exit(1)
        if manager.delete_template(sys.argv[2], sys.argv[3]):
            print(f"已删除模板: {sys.argv[2]}/{sys.argv[3]}")
        else:
            print("模板未找到, 无法删除")
    else:
        print(f"未知命令: {command}")
        print("用法: python3 prompt_template_manager.py [list|get|render|add|delete]")
        sys.exit(1)


if __name__ == "__main__":
    main()
