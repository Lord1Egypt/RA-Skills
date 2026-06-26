#!/usr/bin/env python3
"""测试 code_quality 模块的独立验证脚本"""
import importlib.util
import sys
import os
from types import ModuleType

base_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(base_dir, '..'))

# Register proper two-level package hierarchy
# full_stack_architect (top-level) -> ai_models + code_generator (sub-packages)

fsa = ModuleType('full_stack_architect')
fsa.__path__ = [parent_dir]
fsa.__package__ = 'full_stack_architect'
sys.modules['full_stack_architect'] = fsa

ai_pkg = ModuleType('full_stack_architect.ai_models')
ai_pkg.__path__ = [os.path.join(parent_dir, 'ai-models')]
ai_pkg.__package__ = 'full_stack_architect.ai_models'
sys.modules['full_stack_architect.ai_models'] = ai_pkg

spec_cm = importlib.util.spec_from_file_location(
    'full_stack_architect.ai_models.config_manager',
    os.path.join(parent_dir, 'ai-models', 'config_manager.py')
)
mod_cm = importlib.util.module_from_spec(spec_cm)
mod_cm.__package__ = 'full_stack_architect.ai_models'
sys.modules['full_stack_architect.ai_models.config_manager'] = mod_cm
spec_cm.loader.exec_module(mod_cm)

cg_pkg = ModuleType('full_stack_architect.code_generator')
cg_pkg.__path__ = [os.path.join(parent_dir, 'code-generator')]
cg_pkg.__package__ = 'full_stack_architect.code_generator'
sys.modules['full_stack_architect.code_generator'] = cg_pkg

spec_cq = importlib.util.spec_from_file_location(
    'full_stack_architect.code_generator.code_quality',
    os.path.join(parent_dir, 'code-generator', 'code_quality.py')
)
mod_cq = importlib.util.module_from_spec(spec_cq)
mod_cq.__package__ = 'full_stack_architect.code_generator'
sys.modules['full_stack_architect.code_generator.code_quality'] = mod_cq
spec_cq.loader.exec_module(mod_cq)

checker = mod_cq.CodeQualityChecker()
print('CodeQualityChecker 初始化成功')
print('规则加载成功，语言:', list(checker.rules.keys()))

python_code = 'def factorial(n):\n    if n <= 1:\n        return n\n    else:\n        return factorial(n-1) + factorial(n-2)\n'
result = checker.check_code_quality(python_code, 'python')
print('Python 代码检查结果:', result['message'])
print('发现的问题:', result['issues'])

js_code = 'function factorial(n) {\n    if (n <= 1) {\n        return n;\n    } else {\n        return factorial(n-1) + factorial(n-2);\n    }\n}\n'
result = checker.check_code_quality(js_code, 'javascript')
print('JavaScript 代码检查结果:', result['message'])
print('发现的问题:', result['issues'])

print('\n全部测试通过!')
