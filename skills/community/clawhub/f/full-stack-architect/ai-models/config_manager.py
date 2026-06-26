#!/usr/bin/env python3
"""
统一配置管理器
负责管理系统中所有模板和规则配置
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConfigManager:
    """统一配置管理器"""

    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), 'config')

        self.config_dir = Path(config_dir)
        self.config_cache: Dict[str, Any] = {}

        self.config_dir.mkdir(parents=True, exist_ok=True)

        self._initialize_default_configs()

    def _initialize_default_configs(self):
        language_templates_file = self.config_dir / 'language_templates.json'
        if not language_templates_file.exists():
            default_language_templates = {
                'python': {
                    'hello_world': '# Python Hello World\nprint("Hello, World!")\n',
                    'web_server': '# Python Web Server using Flask\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\'/\')\ndef hello():\n    return "Hello, World!"\n\nif __name__ == "__main__":\n    app.run(debug=True)\n',
                    'data_analysis': '# Python Data Analysis using pandas\nimport pandas as pd\n\n# Read data\ndf = pd.read_csv(\'data.csv\')\n\n# Basic analysis\nprint(df.head())\nprint(df.describe())\n\n# Filter data\nfiltered = df[df[\'value\'] > 100]\nprint(filtered)\n'
                },
                'javascript': {
                    'hello_world': '// JavaScript Hello World\nconsole.log("Hello, World!");\n',
                    'web_server': '// JavaScript Web Server using Express\nconst express = require(\'express\');\nconst app = express();\nconst port = 3000;\n\napp.get(\'/\', (req, res) => {\n  res.send(\'Hello, World!\');\n});\n\napp.listen(port, () => {\n  console.log(`Server running at http://localhost:${port}`);\n});\n',
                    'react_component': '// React Component\nimport React from \'react\';\n\nfunction HelloWorld() {\n  return (\n    <div>\n      <h1>Hello, World!</h1>\n      <p>Welcome to React</p>\n    </div>\n  );\n}\n\nexport default HelloWorld;\n'
                },
                'go': {
                    'hello_world': '// Go Hello World\npackage main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}\n',
                    'web_server': '// Go Web Server\npackage main\n\nimport (\n    "fmt"\n    "net/http"\n)\n\nfunc hello(w http.ResponseWriter, r *http.Request) {\n    fmt.Fprintf(w, "Hello, World!")\n}\n\nfunc main() {\n    http.HandleFunc("/", hello)\n    http.ListenAndServe(":8080", nil)\n}\n'
                },
                'java': {
                    'hello_world': '// Java Hello World\npublic class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n',
                    'web_server': '// Java Web Server using Spring Boot\nimport org.springframework.boot.SpringApplication;\nimport org.springframework.boot.autoconfigure.SpringBootApplication;\nimport org.springframework.web.bind.annotation.GetMapping;\nimport org.springframework.web.bind.annotation.RestController;\n\n@SpringBootApplication\n@RestController\npublic class Application {\n\n    @GetMapping("/")\n    public String hello() {\n        return "Hello, World!";\n    }\n\n    public static void main(String[] args) {\n        SpringApplication.run(Application.class, args);\n    }\n}\n'
                }
            }
            self._save_config('language_templates.json', default_language_templates)

        code_templates_file = self.config_dir / 'code_templates.json'
        if not code_templates_file.exists():
            default_code_templates = {
                'function': '请生成一个{language}函数，实现以下功能：\n{function_description}\n\n要求：\n1. 函数名合理\n2. 参数类型明确\n3. 包含适当的注释\n4. 处理边界情况\n5. 代码风格符合{language}标准\n',
                'class': '请生成一个{language}类，实现以下功能：\n{class_description}\n\n要求：\n1. 类名合理\n2. 包含必要的属性和方法\n3. 构造函数完整\n4. 包含适当的注释\n5. 代码风格符合{language}标准\n',
                'module': '请生成一个{language}模块，实现以下功能：\n{module_description}\n\n要求：\n1. 模块结构清晰\n2. 包含必要的函数和类\n3. 提供适当的文档\n4. 处理错误情况\n5. 代码风格符合{language}标准\n',
                'algorithm': '请生成一个{language}实现，实现以下算法：\n{algorithm_description}\n\n要求：\n1. 算法实现正确\n2. 时间复杂度合理\n3. 包含适当的注释\n4. 提供测试用例\n5. 代码风格符合{language}标准\n'
            }
            self._save_config('code_templates.json', default_code_templates)

        text_templates_file = self.config_dir / 'text_templates.json'
        if not text_templates_file.exists():
            default_text_templates = {
                'prd_summary': '请对以下PRD文档进行总结，提取关键信息：\n\n{prd_content}\n\n总结应该包括：\n1. 项目概述\n2. 核心功能\n3. 技术栈\n4. 目标用户\n5. 成功指标\n',
                'tech_recommendation': '请根据以下项目需求，推荐合适的技术栈：\n\n项目需求：{project_requirements}\n\n推荐应该包括：\n1. 前端技术\n2. 后端技术\n3. 数据库\n4. 部署方案\n5. 推荐理由\n',
                'code_explanation': '请解释以下代码的功能和实现原理：\n\n{code}\n\n解释应该包括：\n1. 代码的整体功能\n2. 关键部分的详细说明\n3. 可能的优化建议\n',
                'bug_analysis': '请分析以下代码中可能存在的bug：\n\n{code}\n\n分析应该包括：\n1. 可能的bug\n2. 问题原因\n3. 修复建议\n',
                'documentation': '请为以下功能编写文档：\n\n功能描述：{feature_description}\n\n文档应该包括：\n1. 功能概述\n2. 使用方法\n3. 参数说明\n4. 示例代码\n5. 注意事项\n'
            }
            self._save_config('text_templates.json', default_text_templates)

        quality_rules_file = self.config_dir / 'quality_rules.json'
        if not quality_rules_file.exists():
            default_quality_rules = {
                'python': {
                    'naming_convention': {
                        'function': '^[a-z_][a-z0-9_]*$',
                        'class': '^[A-Z][a-zA-Z0-9]*$',
                        'variable': '^[a-z_][a-z0-9_]*$',
                        'constant': '^[A-Z_][A-Z0-9_]*$'
                    },
                    'code_structure': {
                        'max_line_length': 79,
                        'indentation': 4,
                        'blank_lines': {
                            'between_functions': 2,
                            'between_classes': 2,
                            'between_methods': 1
                        }
                    },
                    'best_practices': {
                        'docstrings': True,
                        'type_hints': True,
                        'error_handling': True,
                        'imports_order': True
                    }
                },
                'javascript': {
                    'naming_convention': {
                        'function': '^[a-z][a-zA-Z0-9]*$',
                        'class': '^[A-Z][a-zA-Z0-9]*$',
                        'variable': '^[a-z][a-zA-Z0-9]*$',
                        'constant': '^[A-Z_][A-Z0-9_]*$'
                    },
                    'code_structure': {
                        'max_line_length': 80,
                        'indentation': 2,
                        'blank_lines': {
                            'between_functions': 2,
                            'between_classes': 2,
                            'between_methods': 1
                        }
                    },
                    'best_practices': {
                        'comments': True,
                        'error_handling': True,
                        'const_let': True,
                        'arrow_functions': True
                    }
                },
                'go': {
                    'naming_convention': {
                        'function': '^[A-Z][a-zA-Z0-9]*$',
                        'struct': '^[A-Z][a-zA-Z0-9]*$',
                        'variable': '^[a-z][a-zA-Z0-9]*$',
                        'constant': '^[A-Z_][A-Z0-9_]*$'
                    },
                    'code_structure': {
                        'max_line_length': 80,
                        'indentation': 4,
                        'blank_lines': {
                            'between_functions': 1,
                            'between_structs': 1,
                            'between_methods': 1
                        }
                    },
                    'best_practices': {
                        'error_handling': True,
                        'doc_comments': True,
                        'imports_order': True,
                        'short_variable_names': True
                    }
                },
                'java': {
                    'naming_convention': {
                        'class': '^[A-Z][a-zA-Z0-9]*$',
                        'method': '^[a-z][a-zA-Z0-9]*$',
                        'variable': '^[a-z][a-zA-Z0-9]*$',
                        'constant': '^[A-Z_][A-Z0-9_]*$'
                    },
                    'code_structure': {
                        'max_line_length': 80,
                        'indentation': 4,
                        'blank_lines': {
                            'between_classes': 2,
                            'between_methods': 1,
                            'between_blocks': 1
                        }
                    },
                    'best_practices': {
                        'javadoc': True,
                        'error_handling': True,
                        'modifiers_order': True,
                        'imports_order': True
                    }
                }
            }
            self._save_config('quality_rules.json', default_quality_rules)

    def _load_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        config_path = self.config_dir / config_name

        if config_name in self.config_cache:
            return self.config_cache[config_name]

        if not config_path.exists():
            logger.error(f"配置文件不存在: {config_path}")
            return None

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.config_cache[config_name] = config
            logger.info(f"加载配置成功: {config_name}")
            return config
        except Exception as e:
            logger.error(f"加载配置失败 {config_name}: {str(e)}")
            return None

    def _save_config(self, config_name: str, config: Dict[str, Any]) -> bool:
        config_path = self.config_dir / config_name

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            self.config_cache[config_name] = config
            logger.info(f"保存配置成功: {config_name}")
            return True
        except Exception as e:
            logger.error(f"保存配置失败 {config_name}: {str(e)}")
            return False

    def get_language_templates(self) -> Dict[str, Any]:
        config = self._load_config('language_templates.json')
        return config if config else {}

    def get_code_templates(self) -> Dict[str, Any]:
        config = self._load_config('code_templates.json')
        return config if config else {}

    def get_text_templates(self) -> Dict[str, Any]:
        config = self._load_config('text_templates.json')
        return config if config else {}

    def get_quality_rules(self) -> Dict[str, Any]:
        config = self._load_config('quality_rules.json')
        return config if config else {}

    def update_language_templates(self, templates: Dict[str, Any]) -> bool:
        return self._save_config('language_templates.json', templates)

    def update_code_templates(self, templates: Dict[str, Any]) -> bool:
        return self._save_config('code_templates.json', templates)

    def update_text_templates(self, templates: Dict[str, Any]) -> bool:
        return self._save_config('text_templates.json', templates)

    def update_quality_rules(self, rules: Dict[str, Any]) -> bool:
        return self._save_config('quality_rules.json', rules)

    def reload_config(self, config_name: Optional[str] = None):
        if config_name:
            if config_name in self.config_cache:
                del self.config_cache[config_name]
            self._load_config(config_name)
        else:
            self.config_cache.clear()
            self._load_config('language_templates.json')
            self._load_config('code_templates.json')
            self._load_config('text_templates.json')
            self._load_config('quality_rules.json')

        logger.info("配置重新加载完成")


_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


if __name__ == "__main__":
    manager = ConfigManager()

    print("语言模板配置:")
    language_templates = manager.get_language_templates()
    print(json.dumps(language_templates, ensure_ascii=False, indent=2))

    print("\n代码模板配置:")
    code_templates = manager.get_code_templates()
    print(json.dumps(code_templates, ensure_ascii=False, indent=2))

    print("\n文本模板配置:")
    text_templates = manager.get_text_templates()
    print(json.dumps(text_templates, ensure_ascii=False, indent=2))

    print("\n代码质量规则配置:")
    quality_rules = manager.get_quality_rules()
    print(json.dumps(quality_rules, ensure_ascii=False, indent=2))
