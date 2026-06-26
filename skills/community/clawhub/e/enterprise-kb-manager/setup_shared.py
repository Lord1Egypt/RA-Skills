#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统知识库环境设置脚本
"""

import os
import sys
from pathlib import Path

def setup_system_kb():
    """设置系统知识库环境"""
    print("🔧 设置系统知识库环境...")
    
    # 导入系统配置
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    sys.path.insert(0, str(src_dir))
    
    from src.system_config import get_system_kb_path
    
    # 获取系统路径
    system_path = get_system_kb_path()
    print(f"📁 系统路径: {system_path}")
    
    # 创建目录结构（setup有权限创建）
    os.makedirs(system_path, exist_ok=True)
    
    data_path = os.path.join(system_path, "chroma_db")
    documents_path = os.path.join(system_path, "documents")
    
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(documents_path, exist_ok=True)
    
    print(f"✓ 数据目录: {data_path}")
    print(f"✓ 文档目录: {documents_path}")
    
    # 创建配置文件
    config_data = {
        "shared_kb_path": system_path,
        "data_path": data_path,
        "documents_path": documents_path,
        "collection_name": "enterprise_kb",
        "vector_dimension": 1024
    }
    
    config_file = os.path.join(system_path, "config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 创建配置文件: {config_file}")
    
    # 创建README文件
    readme_content = f"""# 系统知识库目录

这是系统级的知识库数据目录，所有skills都会自动使用此路径。

## 目录结构

```
{Path(system_path).name}/
├── chroma_db/              # ChromaDB向量数据库文件
├── documents/              # 原始文档存储
├── config.json            # 系统配置文件
└── README.md              # 说明文档
```

## 路径说明

- **Windows**: `C:/ProgramData/kb-data`
- **Linux/Mac (系统级)**: `/usr/local/share/kb-data`
- **Linux/Mac (用户级)**: `~/.local/share/kb-data`

## 支持的Skills

1. **kb-manager** - 知识库管理系统（读写权限）
2. **kb-reader** - 知识库只读查询器（只读权限）

## 优势

- **固定路径**: 所有agent自动使用相同的系统路径
- **无需配置**: 不需要环境变量或符号链接
- **系统标准**: 遵循操作系统的标准目录结构
- **权限管理**: 自动处理权限问题

## 注意事项

- 此目录由主agent或管理员创建
- 请勿手动删除或修改核心文件
- 定期备份此目录以防数据丢失
- 在Linux/Mac上，如果没有系统权限会自动使用用户目录
"""
    
    readme_file = Path(system_path) / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✓ 创建说明文件: {readme_file}")
    
    print("✅ 系统知识库环境设置完成！")
    print(f"📁 系统目录: {system_path}")
    print("💡 所有skills现在都会自动使用此固定路径")
    
    return system_path

if __name__ == "__main__":
    setup_system_kb()

if __name__ == "__main__":
    setup_shared_kb()