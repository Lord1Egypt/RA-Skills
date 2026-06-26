#!/usr/bin/env python3
"""
Agent 选择器 - 根据任务自动选择合适的人格身份

功能：
1. 任务分析 → 识别需要的专业领域
2. Agent 匹配 → 从 agency-agents-zh 选择最佳 Agent
3. 人格切换 → 加载对应的 Prompt
4. 子 Agent 创建 → 创建专门 Agent 完成任务
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class AgentCategory(Enum):
    """Agent 类别"""
    ENGINEERING = "engineering"
    TESTING = "testing"
    DESIGN = "design"
    PRODUCT = "product"
    MARKETING = "marketing"
    SALES = "sales"
    SUPPORT = "support"
    SPECIALIZED = "specialized"
    GAME_DEVELOPMENT = "game-development"
    PAID_MEDIA = "paid-media"
    PROJECT_MANAGEMENT = "project-management"
    SCRIPTS = "scripts"
    SPATIAL_COMPUTING = "spatial-computing"
    STRATEGY = "strategy"
    INTEGRATIONS = "integrations"
    EXAMPLES = "examples"


@dataclass
class AgentProfile:
    """Agent 档案"""
    id: str
    name: str
    category: AgentCategory
    keywords: List[str]
    prompt_path: str
    expertise: List[str]


class AgentSelector:
    """Agent 选择器"""
    
    # 关键词到 Agent 的映射
    KEYWORD_MAPPING = {
        # 前端开发
        "react": "engineering/engineering-frontend-developer",
        "vue": "engineering/engineering-frontend-developer",
        "angular": "engineering/engineering-frontend-developer",
        "typescript": "engineering/engineering-frontend-developer",
        "javascript": "engineering/engineering-frontend-developer",
        "css": "engineering/engineering-frontend-developer",
        "html": "engineering/engineering-frontend-developer",
        
        # 后端开发
        "nodejs": "engineering/engineering-backend-developer",
        "python": "engineering/engineering-backend-developer",
        "java": "engineering/engineering-backend-developer",
        "go": "engineering/engineering-backend-developer",
        "api": "engineering/engineering-backend-developer",
        "database": "engineering/engineering-backend-developer",
        
        # 全栈
        "fullstack": "engineering/engineering-fullstack-developer",
        "架构": "engineering/engineering-software-architect",
        "技术方案": "engineering/engineering-software-architect",
        
        # DevOps
        "docker": "engineering/engineering-devops-automator",
        "kubernetes": "engineering/engineering-devops-automator",
        "ci/cd": "engineering/engineering-devops-automator",
        "部署": "engineering/engineering-devops-automator",
        
        # 测试
        "测试": "testing/testing-qa-engineer",
        "test": "testing/testing-qa-engineer",
        "qa": "testing/testing-qa-engineer",
        "可访问性": "testing/testing-accessibility-auditor",
        "安全": "engineering/engineering-security-engineer",
        
        # 设计
        "ux": "design/design-ux-designer",
        "ui": "design/design-ui-designer",
        "体验": "design/design-ux-designer",
        "交互": "design/design-interaction-designer",
        "界面": "design/design-ui-designer",
        
        # 产品
        "产品": "product/product-manager",
        "需求": "product/product-manager",
        "roadmap": "product/product-manager",
        
        # AI/ML
        "ai": "specialized/ai-ml-engineer",
        "ml": "specialized/ai-ml-engineer",
        "机器学习": "specialized/ai-ml-engineer",
        "大模型": "specialized/ai-ml-engineer",
    }
    
    def __init__(self, agent_source: str = ""):
        """
        初始化 Agent 选择器
        
        Args:
            agent_source: Agent 来源路径
                         - 空：使用打包的 agency-agents-zh（604 个 Agent）
                         - "/path/to/agency-agents-zh": 使用外部 Agent
        """
        self.agent_source = agent_source
        # 使用打包的 agency-agents-zh（优先）
        self.packed_agents_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agency-agents-zh")
        # 内置的 3 个基础 Agent（降级）
        self.builtin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agency")
        self.available_agents = self._scan_available_agents()
    
    def _scan_available_agents(self) -> List[AgentProfile]:
        """扫描可用的 Agent（优先打包的 agency-agents-zh，降级到内置）
        
        支持：
        - 递归扫描所有子目录（包括 game-development/unity 等）
        - 验证 YAML frontmatter（确保是真正的 Agent）
        - 排除非 Agent 文件（playbook/runbook 等）
        """
        agents = []
        seen_ids = set()
        
        # 扫描路径（优先级从高到低）
        paths_to_scan = []
        
        # 1. 打包的 agency-agents-zh（146 个 Agent）- 最高优先级
        if os.path.exists(self.packed_agents_path):
            paths_to_scan.append(("packed", self.packed_agents_path))
        
        # 2. 外部 Agent 源（如果配置）
        elif self.agent_source and os.path.exists(self.agent_source):
            paths_to_scan.append(("external", self.agent_source))
        
        # 3. 内置 Agent（3 个基础 Agent）- 降级方案
        if os.path.exists(self.builtin_path):
            paths_to_scan.append(("builtin", self.builtin_path))
        
        # 扫描所有路径
        for source_type, base_path in paths_to_scan:
            if source_type in ["packed", "external"]:
                # 递归扫描所有 .md 文件（包括子目录）
                base_path_obj = Path(base_path)
                for md_file in base_path_obj.rglob('*.md'):
                    # 跳过根目录文档
                    if md_file.name in ['README.md', 'CONTRIBUTING.md', 'UPSTREAM.md']:
                        continue
                    
                    # 计算相对路径作为 agent_id
                    try:
                        rel_path = md_file.relative_to(base_path)
                        # 跳过 strategy 下的非 Agent 文件（playbook/runbook/coordination）
                        if rel_path.parts[0] == 'strategy' and len(rel_path.parts) > 1:
                            continue
                        
                        # 构建 agent_id
                        if len(rel_path.parts) == 2:
                            # 一级分类：engineering/engineering-frontend-developer
                            agent_id = f"{rel_path.parts[0]}/{rel_path.stem}"
                        elif len(rel_path.parts) == 3:
                            # 二级分类：game-development/unity/unity-developer
                            agent_id = f"{rel_path.parts[0]}/{rel_path.parts[1]}/{rel_path.stem}"
                        else:
                            continue
                        
                        if agent_id in seen_ids:
                            continue
                        
                        # 验证是否有 YAML frontmatter（真正的 Agent）
                        if not self._has_frontmatter(md_file):
                            continue
                        
                        # 加载 Agent 档案
                        profile = self._load_agent_profile_with_path(agent_id, md_file)
                        if profile:
                            agents.append(profile)
                            seen_ids.add(agent_id)
                    except Exception as e:
                        print(f"⚠️ 处理文件 {md_file} 失败：{e}")
                        continue
            else:
                # 扁平结构：dev-agent.md, test-bot.md
                for file in os.listdir(base_path):
                    if file.endswith('.md'):
                        agent_id = file[:-3]  # 移除 .md
                        if agent_id not in seen_ids:
                            profile = self._load_agent_profile(agent_id, base_path, flat=True)
                            if profile:
                                agents.append(profile)
                                seen_ids.add(agent_id)
        
        return agents
    
    def _has_frontmatter(self, file_path: Path) -> bool:
        """检查文件是否有 YAML frontmatter（真正的 Agent 标识）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                return first_line == '---'
        except:
            return False
    
    def _load_agent_profile_with_path(self, agent_id: str, file_path: Path) -> Optional[AgentProfile]:
        """
        从指定路径加载 Agent 档案
        
        Args:
            agent_id: Agent ID
            file_path: 完整的文件路径
        
        Returns:
            AgentProfile 或 None
        """
        try:
            # 解析分类
            parts = agent_id.split('/')
            if len(parts) < 2:
                return None
            
            # 确定分类（使用第一部分）
            category_str = parts[0]
            try:
                category = AgentCategory(category_str)
            except ValueError:
                category = AgentCategory.SPECIALIZED
            
            # 提取名称
            name = parts[-1].replace('-', ' ').title()
            
            # 读取 Prompt 文件
            keywords = self._extract_keywords(str(file_path))
            expertise = self._extract_expertise(str(file_path))
            
            return AgentProfile(
                id=agent_id,
                name=name,
                category=category,
                keywords=keywords,
                prompt_path=str(file_path),
                expertise=expertise
            )
        except Exception as e:
            print(f"⚠️ 加载 Agent {agent_id} 失败：{e}")
            return None
    
    def _load_agent_profile(self, agent_id: str, base_path: str, flat: bool = False) -> Optional[AgentProfile]:
        """
        加载 Agent 档案
        
        Args:
            agent_id: Agent ID
            base_path: 基础路径
            flat: 是否为扁平结构（内置 Agent 使用扁平结构）
        """
        try:
            if flat:
                # 扁平结构：dev-agent.md
                name = agent_id.replace('-', ' ').title()
                prompt_path = os.path.join(base_path, f"{agent_id}.md")
                category = AgentCategory.SPECIALIZED  # 内置 Agent 默认类别
            else:
                # 分类结构：engineering/engineering-frontend-developer.md
                parts = agent_id.split('/')
                if len(parts) < 2:
                    return None
                
                category = AgentCategory(parts[0])
                name = parts[1].replace('-', ' ').title()
                prompt_path = os.path.join(base_path, f"{parts[1]}.md")
            
            # 读取 Prompt 文件
            keywords = self._extract_keywords(prompt_path)
            expertise = self._extract_expertise(prompt_path)
            
            return AgentProfile(
                id=agent_id,
                name=name,
                category=category,
                keywords=keywords,
                prompt_path=prompt_path,
                expertise=expertise
            )
        except Exception as e:
            print(f"⚠️ 加载 Agent {agent_id} 失败：{e}")
            return None
    
    def _extract_keywords(self, prompt_path: str) -> List[str]:
        """从 Prompt 文件提取关键词"""
        keywords = []
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取专长关键词
            if '**专长**:' in content:
                expertise_line = content.split('**专长**:')[1].split('\n')[0]
                keywords = [k.strip() for k in expertise_line.split(',')]
            
            return keywords
        except:
            return []
    
    def _extract_expertise(self, prompt_path: str) -> List[str]:
        """从 Prompt 文件提取专长领域"""
        # 简化实现，实际应该解析 Prompt 文件
        return []
    
    def select_agent(self, task: str) -> str:
        """
        根据任务选择最佳 Agent
        
        Args:
            task: 任务描述
            
        Returns:
            str: Agent ID
        """
        # 1. 提取任务关键词
        keywords = self._extract_task_keywords(task)
        
        # 2. 匹配 Agent
        matched_agents = []
        for keyword in keywords:
            if keyword in self.KEYWORD_MAPPING:
                agent_id = self.KEYWORD_MAPPING[keyword]
                matched_agents.append(agent_id)
        
        # 3. 返回最佳匹配
        if matched_agents:
            # 返回出现频率最高的 Agent
            from collections import Counter
            counter = Counter(matched_agents)
            return counter.most_common(1)[0][0]
        
        # 4. 默认返回全栈工程师
        return "engineering/engineering-fullstack-developer"
    
    def _extract_task_keywords(self, task: str) -> List[str]:
        """从任务描述提取关键词"""
        keywords = []
        task_lower = task.lower()
        
        # 匹配预定义关键词
        for keyword in self.KEYWORD_MAPPING.keys():
            if keyword.lower() in task_lower:
                keywords.append(keyword)
        
        return keywords
    
    def select_agents_for_roundtable(self, topic: str) -> List[str]:
        """
        为 RoundTable 智能选择多个 Agent（使用 146 个 Agent 池）
        
        智能选择逻辑：
        1. 分析主题关键词
        2. 匹配最相关的 Agent
        3. 确保多领域覆盖（技术 + 体验 + 质量 + 专业）
        
        Args:
            topic: 讨论主题
            
        Returns:
            List[str]: Agent ID 列表（3-5 个）
        """
        agents = []
        topic_lower = topic.lower()
        
        # ========== 步骤 1: 分析主题关键词 ==========
        topic_keywords = {
            # AI/ML 相关
            'ai_ml': ['ai', 'ml', '智能', '机器学习', '大模型', 'llm', 'rag', 'nlp', 'cv'],
            # 前端/移动端
            'frontend': ['前端', 'web', 'react', 'vue', 'angular', '移动端', 'ios', 'android', '小程序'],
            # 后端/架构
            'backend': ['后端', '架构', 'api', '微服务', '数据库', 'server', 'backend'],
            # 安全相关
            'security': ['安全', 'security', '审计', '漏洞', '加密', '认证', 'auth'],
            # 游戏开发
            'game': ['游戏', 'game', 'unity', 'unreal', 'godot', 'roblox'],
            # 电商/商业
            'ecommerce': ['电商', '购物', '商城', '支付', '订单', '商品'],
            # 数据相关
            'data': ['数据', 'data', 'etl', '仓库', '分析', 'bi', '报表'],
            # 设计/体验
            'design': ['设计', '体验', 'ui', 'ux', '交互', '界面', '视觉'],
            # DevOps/部署
            'devops': ['devops', '部署', 'ci/cd', 'docker', 'k8s', '运维', 'sre'],
        }
        
        # 匹配主题类别
        matched_categories = []
        for category, keywords in topic_keywords.items():
            if any(kw in topic_lower for kw in keywords):
                matched_categories.append(category)
        
        # ========== 步骤 2: 选择核心 Agent（3 个固定角色）==========
        
        # 1. 技术专家 - 根据主题选择最匹配的 engineering Agent
        tech_agent = self._select_best_engineering_agent(matched_categories)
        agents.append(tech_agent)
        
        # 2. 体验专家 - 根据主题选择 design Agent
        design_agent = self._select_best_design_agent(matched_categories)
        agents.append(design_agent)
        
        # 3. 质量专家 - 根据主题选择 testing Agent
        test_agent = self._select_best_testing_agent(matched_categories)
        agents.append(test_agent)
        
        # ========== 步骤 3: 添加专业领域 Agent（0-2 个）==========
        
        # AI/ML 专家
        if 'ai_ml' in matched_categories:
            ai_agent = self._find_agent(['ai-ml-engineer', 'ai-engineer'], 'specialized')
            if ai_agent:
                agents.append(ai_agent)
        
        # 安全专家
        if 'security' in matched_categories:
            security_agent = self._find_agent(['security-engineer', 'security-auditor'], 'engineering')
            if security_agent:
                agents.append(security_agent)
        
        # 游戏开发专家
        if 'game' in matched_categories:
            if 'unity' in topic_lower:
                game_agent = self._find_agent(['unity-architect', 'unity-developer'], 'game-development')
            elif 'unreal' in topic_lower:
                game_agent = self._find_agent(['unreal-systems-engineer', 'unreal-developer'], 'game-development')
            else:
                game_agent = self._find_agent(['game-developer', 'game-designer'], 'game-development')
            if game_agent:
                agents.append(game_agent)
        
        # 数据专家
        if 'data' in matched_categories:
            data_agent = self._find_agent(['data-engineer', 'database-optimizer'], 'engineering')
            if data_agent:
                agents.append(data_agent)
        
        # DevOps 专家
        if 'devops' in matched_categories:
            devops_agent = self._find_agent(['devops-automator', 'sre'], 'engineering')
            if devops_agent and devops_agent not in agents:
                agents.append(devops_agent)
        
        # ========== 步骤 4: 去重并限制数量 ==========
        # 去重
        unique_agents = []
        seen = set()
        for agent in agents:
            if agent not in seen:
                unique_agents.append(agent)
                seen.add(agent)
        
        # 限制最多 5 个
        return unique_agents[:5] if len(unique_agents) > 5 else unique_agents
    
    def _select_best_engineering_agent(self, categories: List[str]) -> str:
        """根据类别选择最佳 engineering Agent"""
        # 类别到 Agent 的映射（按优先级排序）
        category_mapping = {
            'mobile': ['engineering-mobile-app-builder'],  # 移动端优先
            'frontend': ['engineering-frontend-developer', 'engineering-senior-developer'],
            'backend': ['engineering-backend-architect', 'engineering-software-architect'],
            'ai_ml': ['engineering-ai-engineer'],
            'security': ['engineering-security-engineer'],
            'game': ['engineering-rapid-prototyper'],
            'data': ['engineering-data-engineer', 'engineering-database-optimizer'],
            'devops': ['engineering-devops-automator', 'engineering-sre'],
        }
        
        # 尝试按类别匹配（按优先级）
        for category in ['mobile', 'frontend', 'backend', 'ai_ml', 'security', 'game', 'data', 'devops']:
            if category in categories:
                for agent_id in category_mapping.get(category, []):
                    agent = self._find_agent([agent_id], 'engineering')
                    if agent:
                        return agent
        
        # 默认返回软件架构师
        return 'engineering/engineering-software-architect'
    
    def _select_best_design_agent(self, categories: List[str]) -> str:
        """根据类别选择最佳 design Agent"""
        # 体验/设计相关类别优先
        if 'design' in categories or 'frontend' in categories:
            # 优先选择 UI/UX 相关
            ui_agent = self._find_agent(['ui-designer', 'ux-architect'], 'design')
            if ui_agent:
                return ui_agent
        
        # 默认返回 UX 架构师
        return 'design/design-ux-architect'
    
    def _select_best_testing_agent(self, categories: List[str]) -> str:
        """根据类别选择最佳 testing Agent"""
        # 根据类别选择测试专家
        if 'api' in str(categories).lower():
            api_tester = self._find_agent(['api-tester'], 'testing')
            if api_tester:
                return api_tester
        
        if 'security' in categories:
            security_tester = self._find_agent(['security-auditor', 'accessibility-auditor'], 'testing')
            if security_tester:
                return security_tester
        
        # 默认返回 API 测试专家
        return 'testing/testing-api-tester'
    
    def _find_agent(self, name_patterns: List[str], category: str = None) -> Optional[str]:
        """
        根据名称模式查找 Agent
        
        Args:
            name_patterns: Agent 名称模式列表（如 ['security-engineer', 'security-auditor']）
            category: 可选的分类过滤（如 'engineering', 'testing'）
        
        Returns:
            Agent ID 或 None
        """
        for agent in self.available_agents:
            # 分类过滤
            if category and agent.category.value != category:
                continue
            
            # 名称匹配
            agent_id_lower = agent.id.lower()
            for pattern in name_patterns:
                if pattern.lower() in agent_id_lower:
                    return agent.id
        
        return None
    
    def get_software_development_agents(self) -> List[str]:
        """
        获取所有与软件开发相关的 Agent（用于 Auto-Coding）
        
        包括：
        - 所有 engineering 分类（22 个）
        - design 分类中的 UI/UX 设计师
        - testing 分类（质量保证）
        - specialized 中的 AI/ML 工程师
        - game-development 中的游戏开发者（如需要）
        
        Returns:
            List[str]: Agent ID 列表
        """
        agents = []
        
        # 1. 所有 engineering 分类（22 个）
        engineering_agents = [a.id for a in self.available_agents 
                             if a.category.value == "engineering"]
        agents.extend(engineering_agents)
        
        # 2. design 分类中的 UI/UX 设计师
        design_agents = [a.id for a in self.available_agents 
                        if a.category.value == "design" and 
                        any(kw in a.id.lower() for kw in ["ui", "ux", "design"])]
        agents.extend(design_agents)
        
        # 3. testing 分类（质量保证）
        testing_agents = [a.id for a in self.available_agents 
                         if a.category.value == "testing"]
        agents.extend(testing_agents)
        
        # 4. specialized 中的 AI/ML 工程师
        ai_agents = [a.id for a in self.available_agents 
                    if a.category.value == "specialized" and 
                    any(kw in a.id.lower() for kw in ["ai", "ml", "machine-learning"])]
        agents.extend(ai_agents)
        
        # 5. game-development 中的开发者（可选）
        game_agents = [a.id for a in self.available_agents 
                      if a.category.value == "game-development" and 
                      any(kw in a.id.lower() for kw in ["developer", "engineer", "scripter"])]
        agents.extend(game_agents)
        
        return agents
    
    def load_agent_prompt(self, agent_id: str) -> str:
        """
        加载 Agent Prompt
        
        Args:
            agent_id: Agent ID
            
        Returns:
            str: Agent Prompt 内容
        """
        # 查找 Agent
        for agent in self.available_agents:
            if agent.id == agent_id:
                try:
                    with open(agent.prompt_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"⚠️ 加载 Prompt 失败：{e}")
                    return self._get_default_prompt(agent_id)
        
        # 未找到 Agent，返回默认 Prompt
        return self._get_default_prompt(agent_id)
    
    def _get_default_prompt(self, agent_id: str) -> str:
        """获取默认 Prompt"""
        return f"""你是一位专业的 {agent_id}。

请从你的专业角度提供详细分析和建议。

输出要求：
- 使用 Markdown 格式
- 包含具体的技术细节
- 如有表格、列表请清晰呈现
"""


# 快捷函数
def switch_agent(agent_id: str, agent_source: str = "") -> str:
    """
    切换人格身份（快捷函数）
    
    Args:
        agent_id: Agent ID
        agent_source: Agent 来源路径
        
    Returns:
        str: Agent Prompt 内容
    """
    selector = AgentSelector(agent_source)
    prompt = selector.load_agent_prompt(agent_id)
    print(f"✅ 已切换到 {agent_id} 人格")
    return prompt


def auto_select_agent(task: str, agent_source: str = "") -> str:
    """
    自动选择 Agent（快捷函数）
    
    Args:
        task: 任务描述
        agent_source: Agent 来源路径
        
    Returns:
        str: Agent ID
    """
    selector = AgentSelector(agent_source)
    return selector.select_agent(task)


def select_roundtable_agents(topic: str, agent_source: str = "") -> List[str]:
    """
    为 RoundTable 选择 Agent（快捷函数）
    
    Args:
        topic: 讨论主题
        agent_source: Agent 来源路径
        
    Returns:
        List[str]: Agent ID 列表
    """
    selector = AgentSelector(agent_source)
    return selector.select_agents_for_roundtable(topic)


# 测试
if __name__ == "__main__":
    selector = AgentSelector()
    
    # 测试任务匹配
    test_tasks = [
        "设计一个 React 前端架构",
        "编写 Python 后端 API",
        "设计用户体验方案",
        "编写测试用例",
        "AI 技术方案设计"
    ]
    
    print("Agent 选择测试：")
    print("="*60)
    for task in test_tasks:
        agent = selector.select_agent(task)
        print(f"任务：{task}")
        print(f"匹配 Agent: {agent}")
        print("-"*60)
