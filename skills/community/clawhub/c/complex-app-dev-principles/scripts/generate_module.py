#!/usr/bin/env python3
"""
I漫剧APP开发技能 - 模块脚手架生成工具
快速生成符合规范的新模块代码结构
"""

import os
import sys
from datetime import datetime

MODULE_TEMPLATE = """# {module_name}模块

## 模块信息
- **模块名称**: {module_name}
- **创建时间**: {create_time}
- **开发状态**: 开发中
- **优先级**: P0/P1/P2

## 功能描述
[请描述模块的主要功能]

## 接口定义

### 对外接口
| 接口名称 | 输入参数 | 输出结果 | 说明 |
|---------|---------|---------|------|
| | | | |

### 依赖接口
| 依赖模块 | 接口名称 | 用途 |
|---------|---------|------|
| | | |

## 数据结构
```json
{{
    "module": "{module_name}",
    "version": "1.0.0"
}}
```

## 测试用例
| 用例编号 | 测试内容 | 预期结果 | 状态 |
|---------|---------|---------|------|
| | | | |

## 开发日志
| 日期 | 开发者 | 操作 | 说明 |
|-----|--------|-----|------|
| {create_time} | | 创建模块 | 初始版本 |
"""

def generate_module(module_name: str, output_dir: str = "."):
    """生成模块脚手架"""
    module_dir = os.path.join(output_dir, module_name)

    if os.path.exists(module_dir):
        print(f"错误: 模块 '{module_name}' 已存在")
        return False

    os.makedirs(module_dir)

    # 创建模块文档
    doc_content = MODULE_TEMPLATE.format(
        module_name=module_name,
        create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    doc_path = os.path.join(module_dir, "README.md")
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(doc_content)

    # 创建源代码目录
    src_dir = os.path.join(module_dir, "src")
    os.makedirs(src_dir)

    # 创建测试目录
    test_dir = os.path.join(module_dir, "tests")
    os.makedirs(test_dir)

    print(f"✓ 模块 '{module_name}' 创建成功")
    print(f"  - 文档: {doc_path}")
    print(f"  - 源码: {src_dir}/")
    print(f"  - 测试: {test_dir}/")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_module.py <模块名称> [输出目录]")
        sys.exit(1)

    module_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    generate_module(module_name, output_dir)
