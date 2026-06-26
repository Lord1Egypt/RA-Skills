#!/bin/bash
# fix_setup.sh

echo "🔧 修复 trade-code-analyzer 设置..."

# 1. 创建必要的 __init__.py 文件
echo "创建模块初始化文件..."
touch scripts/__init__.py
touch scripts/parser/__init__.py
touch scripts/analyzer/__init__.py
touch scripts/knowledge/__init__.py

# 2. 创建缺失的解析器占位文件
echo "创建 React 解析器占位..."
cat > scripts/parser/react_parser.py << 'EOF'
from .base import BaseCodeParser, ParsedComponent, ParsedAPI, ParsedRule
from typing import List, Dict, Any

class ReactParser(BaseCodeParser):
    """React 组件解析器（占位实现）"""
    
    def parse(self) -> Dict[str, Any]:
        return {
            "file_info": {
                "path": self.file_path,
                "type": "react",
                "note": "React 解析器尚未完全实现"
            },
            "components": [],
            "apis": [],
            "business_rules": [],
            "complexity": self.calculate_complexity()
        }
    
    def extract_components(self) -> List[ParsedComponent]:
        return []
    
    def extract_apis(self) -> List[ParsedAPI]:
        return []
    
    def extract_business_rules(self) -> List[ParsedRule]:
        return []
EOF

# 3. 创建 Angular 解析器占位
echo "创建 Angular 解析器占位..."
cat > scripts/parser/angular_parser.py << 'EOF'
from .base import BaseCodeParser, ParsedComponent, ParsedAPI, ParsedRule
from typing import List, Dict, Any

class AngularParser(BaseCodeParser):
    """Angular 组件解析器（占位实现）"""
    
    def parse(self) -> Dict[str, Any]:
        return {
            "file_info": {
                "path": self.file_path,
                "type": "angular",
                "note": "Angular 解析器尚未完全实现"
            },
            "components": [],
            "apis": [],
            "business_rules": [],
            "complexity": self.calculate_complexity()
        }
    
    def extract_components(self) -> List[ParsedComponent]:
        return []
    
    def extract_apis(self) -> List[ParsedAPI]:
        return []
    
    def extract_business_rules(self) -> List[ParsedRule]:
        return []
EOF

# 4. 确保 base.py 存在
if [ ! -f "scripts/parser/base.py" ]; then
    echo "❌ 错误: scripts/parser/base.py 不存在，请先创建基础解析器类"
    exit 1
fi

# 5. 测试导入
echo "测试导入..."
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from parser.vue_parser import VueParser
print('✓ VueParser 导入成功')
"

echo ""
echo "✅ 修复完成！现在可以运行:"
echo "  python3 scripts/cli.py --help"
echo "  python3 scripts/cli.py parse <your-file>.vue"