#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专家工具箱 - Expert Toolkit
核心功能：智能匹配专家，加载专家prompt，调用模型输出
"""

import sys
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 强制UTF-8输出，解决Windows GBK编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# 配置文件目录
CONFIG_DIR = Path(os.path.join(os.path.dirname(__file__), '..', 'config'))

# 知识库中角色的根目录 - 支持环境变量覆盖默认路径
DEFAULT_ROLES_ROOT = os.path.expanduser("~/.openclaw/workspace/knowledge/agency-orchestrator/roles")
ROLES_ROOT = Path(os.getenv("EXPERT_TOOLKIT_ROLES_ROOT", DEFAULT_ROLES_ROOT))

class ExpertRole:
    def __init__(self, path: Path, name: str, category: str, chinese_name: str = None):
        self.path = path
        self.name = name  # 文件名（不含扩展名）
        self.category = category  # 分类目录
        self.chinese_name = chinese_name or name.replace('-', ' ')
        self.content = None  # 缓存prompt内容
    
    def load_content(self) -> str:
        """加载专家prompt内容"""
        if self.content is None:
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.content = f.read()
            except OSError as e:
                self.content = f"⚠️  加载专家prompt失败: {e}"
        return self.content

# 中文分类映射 - 中文 -> 英文
CATEGORY_MAP = {
    '产品': 'product',
    '设计': 'design',
    '技术': 'engineering',
    '工程': 'engineering',
    '财务': 'finance',
    '金融': 'finance',
    '游戏': 'game-development',
    '营销': 'paid-media',
    '市场': 'marketing',
    '市场营销': 'marketing',
    '项目': 'project-management',
    '销售': 'sales',
    '战略': 'strategy',
    '客服': 'support',
    '测试': 'testing',
    '数据': 'data',
}

# 反向映射：英文 -> 中文（用于显示）
CATEGORY_REVERSE_MAP = {
    'product': '产品',
    'design': '设计',
    'engineering': '技术',
    'finance': '财务',
    'marketing': '市场',

    'game-development': '游戏',
    'paid-media': '营销',
    'project-management': '项目',
    'sales': '销售',
    'strategy': '战略',
    'support': '客服',
    'testing': '测试',
    'data': '数据',
}

class ExpertLibrary:
    """专家库，管理所有专家角色"""
    
    def __init__(self, roles_root: Path = ROLES_ROOT):
        self.roles_root = roles_root
        self.roles: Dict[str, ExpertRole] = {}  # id (file stem) -> ExpertRole
        self.name_map: Dict[str, ExpertRole] = {}  # lower(role.name) -> ExpertRole
        self.chinese_name_map: Dict[str, ExpertRole] = {}  # lower(chinese_name) -> ExpertRole
        self.categories: Dict[str, int] = {}  # category -> count
        self.chinese_translate: Dict[str, str] = self._load_chinese_translate()
        self.keyword_mapping: Dict[str, List[str]] = self._load_keyword_mapping()
        self._load_all_roles()
    
    def _load_chinese_translate(self) -> Dict[str, str]:
        """加载中文翻译映射"""
        config_file = CONFIG_DIR / 'chinese_translate.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"⚠️  解析 chinese_translate.json 失败: {e}，使用空映射")
        return {}
    
    def _load_keyword_mapping(self) -> Dict[str, List[str]]:
        """加载关键词映射"""
        config_file = CONFIG_DIR / 'keyword_mapping.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"⚠️  解析 keyword_mapping.json 失败: {e}，使用空映射")
        return {}
    
    def _extract_chinese_name(self, content: str, filename: str) -> str:
        """从markdown内容提取中文名（第一个标题就是角色名）"""
        if not content:
            return filename.replace('-', ' ')
        first_line = content.split('\n')[0].strip()
        if first_line.startswith('# '):
            return first_line[2:].strip()
        return filename.replace('-', ' ')
    
    def _load_all_roles(self):
        """加载所有专家角色"""
        if not self.roles_root.exists():
            return
        
        for category_dir in self.roles_root.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue
            
            category = category_dir.name
            count = 0
            
            for md_file in category_dir.glob('*.md'):
                if md_file.name.startswith('.'):
                    continue
                
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                except OSError as e:
                    print(f"⚠️  读取 {md_file} 失败: {e}，跳过")
                    continue
                
                chinese_name = self._extract_chinese_name(content, md_file.stem)
                role = ExpertRole(md_file, md_file.stem, category, chinese_name)
                role.content = content  # 预加载，小文件不占空间
                self.roles[md_file.stem] = role
                # 也按中文名索引，方便中文搜索（单独字典避免key冲突）
                self.chinese_name_map[chinese_name.lower()] = role
                # 添加小写名称索引，优化查找
                self.name_map[role.name.lower()] = role
                count += 1
            
            self.categories[category] = count
    
    def search(self, keyword: str) -> List[ExpertRole]:
        """搜索专家，按关键词匹配名字、中文名、分类"""
        keyword = keyword.lower()
        results = []
        seen = set()
        
        # 如果是中文分类，转换为英文
        mapped_category = None
        if keyword in CATEGORY_MAP:
            mapped_category = CATEGORY_MAP[keyword]
            keyword = mapped_category
        
        # 如果关键词在中文翻译映射里，直接添加对应的专家
        if keyword in self.chinese_translate:
            expert_id = self.chinese_translate[keyword]
            role = self.get_by_name(expert_id)
            if role and role.name not in seen:
                results.append(role)
                seen.add(role.name)
        
        # 检查中文翻译映射中的键是否包含关键词（支持简写，如"架构"匹配"架构师"）
        for cn_name, expert_id in self.chinese_translate.items():
            if keyword in cn_name.lower() and expert_id not in seen:
                role = self.get_by_name(expert_id)
                if role and role.name not in seen:
                    results.append(role)
                    seen.add(role.name)
        
        for role_id, role in self.roles.items():
            # 匹配id、中文名、分类
            match = False
            if keyword in role_id.lower():
                match = True
            elif role.chinese_name and keyword in role.chinese_name.lower():
                match = True
            elif mapped_category and role.category.lower() == mapped_category:
                match = True
            elif keyword in role.category.lower():
                match = True
            
            if match and role.name not in seen:
                results.append(role)
                seen.add(role.name)
        
        return sorted(results, key=lambda x: x.name)
    
    def get_by_name(self, name: str) -> Optional[ExpertRole]:
        """根据名字或中文名获取专家"""
        name = name.lower().strip()
        
        # 中文翻译映射，方便用户用中文调用
        if name in self.chinese_translate:
            name = self.chinese_translate[name]
        
        # O(1) 直接查找小写名称索引
        if name in self.name_map:
            return self.name_map[name]
        
        if name in self.roles:
            return self.roles.get(name)
        
        # 查找中文名索引
        if name in self.chinese_name_map:
            return self.chinese_name_map[name]
        
        # 模糊匹配
        results = self.search(name)
        if results:
            return results[0]
        
        return None
    
    def list_category(self, category: str) -> List[ExpertRole]:
        """列出某个分类下的所有专家"""
        results = []
        seen = set()
        category = category.lower()
        
        # 如果是中文分类，转换为英文
        if category in CATEGORY_MAP:
            category = CATEGORY_MAP[category]
        
        for role in self.roles.values():
            if role.category.lower() == category and role.name not in seen:
                results.append(role)
                seen.add(role.name)
        return sorted(results, key=lambda x: x.name)
    
    def get_categories(self) -> List[Tuple[str, int]]:
        """获取所有分类和专家数量"""
        return sorted(self.categories.items(), key=lambda x: x[0])
    
    def count_total(self) -> int:
        """获取总专家数"""
        seen = set()
        for role in self.roles.values():
            seen.add((role.category, role.name))
        return len(seen)

def format_search_results(results: List[ExpertRole], keyword: str) -> str:
    """格式化搜索结果"""
    if not results:
        return f"🔍 没有找到匹配「{keyword}」的专家，换个关键词试试吧。"
    
    output = [f"🔍 找到 {len(results)} 个匹配的专家：\n"]
    for i, role in enumerate(results, 1):
        output.append(f"{i}. **{role.chinese_name}** → `{role.category}/{role.name}`")
    
    output.append("\n💡 调用：`/expert {中文名} 你的问题` 就能直接使用了。")
    return '\n'.join(output)

def format_categories(categories: List[Tuple[str, int]], total: int) -> str:
    """格式化分类列表 - 显示中文分类名 + 英文"""
    output = [f"📂 共有 {len(categories)} 个分类，总计 {total} 位专家：\n"]
    for i, (category, count) in enumerate(categories, 1):
        # 如果有中文映射，显示中文 + 英文
        if category in CATEGORY_REVERSE_MAP:
            cn_name = CATEGORY_REVERSE_MAP[category]
            output.append(f"{i}. **{cn_name}** ({category}) → {count} 位专家")
        else:
            output.append(f"{i}. **{category}** → {count} 位专家")
    
    output.append("\n💡 查看分类下专家：`/expert list 分类名`（支持中文分类名）")
    return '\n'.join(output)

def format_list_category(results: List[ExpertRole], category: str) -> str:
    """格式化分类下专家列表"""
    if not results:
        return f"📚 分类「{category}」下没有找到专家，检查分类名对不对。"
    
    output = [f"📚 分类「{category}」下共有 {len(results)} 位专家：\n"]
    for i, role in enumerate(results, 1):
        output.append(f"{i}. **{role.chinese_name}** → `{role.name}`")
    
    output.append("\n💡 调用：`/expert {中文名} 你的问题` 就能直接使用了。")
    return '\n'.join(output)

def build_system_prompt(role: ExpertRole, user_query: str) -> str:
    """构建完整的system prompt"""
    role_content = role.load_content()
    return f"""{role_content}

---

# 用户问题

{user_query}

请以{role.chinese_name}的专业身份回答用户问题。
"""

def match_experts_by_requirement(requirement: str, library: ExpertLibrary) -> List[ExpertRole]:
    """根据用户需求智能匹配专家
    
    这里用关键词匹配，简单有效，可以后续升级LLM匹配
    """
    matched = set()
    requirement_lower = requirement.lower()
    
    # 关键词匹配（从外置配置加载）
    for keyword, expert_names in library.keyword_mapping.items():
        if keyword in requirement_lower:
            for expert_name in expert_names:
                role = library.get_by_name(expert_name)
                if role:
                    matched.add(role)
    
    # 如果没匹配到，试试搜索
    if not matched:
        # 分词搜索
        words = re.findall(r'[\w]+', requirement_lower)
        for word in words:
            if len(word) >= 2:
                results = library.search(word)
                for role in results[:3]:  # 最多取3个
                    matched.add(role)
    
    # 还是没匹配到，给默认通用专家
    if not matched:
        # 先尝试找 product-manager，如果找不到就取第一个专家
        default = library.get_by_name('product-manager')
        if default:
            matched.add(default)
        elif library.count_total() > 0:
            # 取第一个专家作为默认
            for role in library.roles.values():
                matched.add(role)
                break
    
    return list(matched)[:5]  # 最多5个专家，避免太长

def handle_command(command: str, args: str, library: ExpertLibrary) -> str:
    """处理不同命令"""
    
    if command == 'search':
        keyword = args.strip()
        results = library.search(keyword)
        return format_search_results(results, keyword)
    
    elif command == 'categories':
        categories = library.get_categories()
        total = library.count_total()
        return format_categories(categories, total)
    
    elif command == 'list':
        category = args.strip()
        results = library.list_category(category)
        return format_list_category(results, category)
    
    else:
        # 直接调用专家，command其实是专家名
        role = library.get_by_name(command)
        if not role:
            # 尝试搜索
            results = library.search(command)
            if not results:
                return f"❌ 没有找到名为「{command}」的专家，试试 `/expert search {command}` 搜索一下。"
            role = results[0]
        
        prompt = build_system_prompt(role, args.strip())
        # 返回prompt给调用者，让大模型处理
        return f"""🔧 已加载专家 **{role.chinese_name}** ({role.category}/{role.name})

---

{prompt}
"""

def handle_auto_match(requirement: str, library: ExpertLibrary) -> str:
    """处理自动匹配模式@expert"""
    matched = match_experts_by_requirement(requirement, library)
    
    if not matched:
        return "😅 很抱歉，我没能匹配到合适的专家，你可以试试 `/expert search 关键词` 手动找。"
    
    output = [f"🤖 已为你的需求自动匹配 {len(matched)} 位专家：\n"]
    
    for i, role in enumerate(matched, 1):
        output.append(f"\n---\n")
        output.append(f"**{i}. {role.chinese_name}** ({role.category}/{role.name})")
        output.append("\n")
        output.append(build_system_prompt(role, requirement))
    
    output.append("\n---\n✅ 以上是各位专家从不同专业角度给出的分析，请综合参考。")
    
    return '\n'.join(output)

def parse_input(input_text: str) -> Tuple[str, str, bool]:
    """解析用户输入
    
    返回: (command/role, args, is_auto_match)
    is_auto_match=True 表示是@expert自动匹配模式
    """
    input_text = input_text.strip()
    
    # 检测是否是@expert自动匹配
    if input_text.startswith('@expert'):
        requirement = input_text[len('@expert'):].strip()
        return '', requirement, True
    
    # 检测是否是/expert命令
    if input_text.startswith('/expert'):
        rest = input_text[len('/expert'):].strip()
        parts = rest.split(None, 1)
        if len(parts) == 0:
            return 'categories', '', False
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ''
        return command, args, False
    
    # 命令行测试时，直接传入命令和参数（已经去掉了/expert）
    parts = input_text.split(None, 1)
    if len(parts) == 0:
        return 'categories', '', False
    command = parts[0]
    args = parts[1] if len(parts) > 1 else ''
    return command, args, False

def main():
    """入口函数，供测试"""
    library = ExpertLibrary()
    print(f"Loaded {library.count_total()} experts from {len(library.categories)} categories.")

if __name__ == '__main__':
    main()
