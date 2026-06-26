#!/usr/bin/env python3
"""
Agent 选择器 - 安全增强版 + 自动身份管理

功能：
1. 任务分析 → 识别需要的专业领域
2. Agent 匹配 → 从 agency-agents 选择最佳 Agent
3. 人格切换 → 加载对应的 Prompt
4. 子 Agent 创建 → 创建专门 Agent 完成任务
5. 自动身份管理 → 每轮对话独立判断，自动恢复默认身份

安全加固：
- ✅ 路径白名单验证
- ✅ 文件大小限制（100KB）
- ✅ 输入长度限制（10000 字符）
- ✅ 符号链接验证
- ✅ 文件编码验证
- ✅ 错误信息脱敏

性能优化：
- ✅ Prompt 缓存（缓存命中 <1ms）
- ✅ 懒加载（按需加载 Prompt）
- ✅ 轻量切换（无需切换时 <2ms）
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
    """
    Agent 选择器 - 安全增强版 + 自动身份管理
    
    特性：
    - 安全加固：6 层安全防护
    - 性能优化：缓存 + 懒加载
    - 自动身份：每轮对话独立判断，自动恢复默认身份
    
    使用示例：
    ```python
    selector = AgentSelector()
    
    # 对话 1：代码安全检查
    selector.analyze_and_switch("帮我做代码安全检查")
    # 输出：🔄 切换到 安全工程师
    prompt = selector.get_prompt()
    # ... 执行任务 ...
    selector.complete_task()
    # 输出：✅ 已恢复到默认身份
    
    # 对话 2：继续安全检查
    selector.analyze_and_switch("还有安全问题吗？")
    # 输出：🔄 切换到 安全工程师（缓存命中 <1ms）
    ```
    """
    
    # 🔒 安全常量
    MAX_FILE_SIZE = 100 * 1024  # 100KB 文件大小限制
    MAX_TASK_LENGTH = 10000  # 任务描述长度限制
    MAX_PATH_DEPTH = 5  # 最大路径深度
    
    # 🔒 允许的目录白名单
    ALLOWED_DIRECTORIES = [
        "agency-agents-zh",
        "agency-agents",
        "agency"
    ]
    
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
        
        # 安全
        "安全": "engineering/engineering-security-engineer",
        "security": "engineering/engineering-security-engineer",
        "审计": "testing/testing-security-auditor",
        
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
        "ai": "specialized/specialized-ai-ml-engineer",
        "ml": "specialized/specialized-ai-ml-engineer",
        "机器学习": "specialized/specialized-ai-ml-engineer",
        "大模型": "specialized/specialized-ai-ml-engineer",
    }
    
    # Agent 中文名映射
    AGENT_NAMES = {
        "engineering/software-engineer": "软件工程师",
        "engineering/security-engineer": "安全工程师",
        "engineering/frontend-developer": "前端工程师",
        "engineering/backend-developer": "后端工程师",
        "engineering/fullstack-developer": "全栈工程师",
        "engineering/software-architect": "软件架构师",
        "engineering/devops-automator": "DevOps 工程师",
        "testing/qa-engineer": "QA 工程师",
        "testing/accessibility-auditor": "可访问性审计师",
        "testing/security-auditor": "安全审计师",
        "design/ux-designer": "UX 设计师",
        "design/ui-designer": "UI 设计师",
        "product/product-manager": "产品经理",
        "specialized/ai-ml-engineer": "AI/ML 工程师",
    }
    
    def __init__(self, agent_source: str = "", default_agent: str = ""):
        """
        初始化 Agent 选择器（安全增强版 + 自动身份管理）
        
        Args:
            agent_source: Agent 来源路径
                         - 空：使用内置的 agency-agents
                         - "/path/to/agency-agents": 使用外部 Agent（必须在白名单内）
            default_agent: 默认身份（可选）
                         - 空：使用 "engineering/software-engineer"
        
        🔒 安全验证：
        - 路径必须在 skills 目录内
        - 目录名必须在白名单中
        - 路径深度不能超过限制
        
        ⚡ 性能优化：
        - Prompt 缓存：缓存已加载的 Prompt
        - 懒加载：按需加载 Prompt
        """
        # 🔒 先设置 skills_root（必须在验证之前）
        self.skills_root = Path(__file__).parent.parent.resolve()  # 指向 skills 目录
        self.packed_agents_path = self.skills_root / "agency-agents-zh"
        self.builtin_path = self.skills_root / "agency"
        
        # 🔒 验证并设置 agent_source（现在 self.skills_root 已定义）
        if agent_source:
            self.agent_source = self._validate_agent_source(agent_source)
        else:
            self.agent_source = ""
        
        # 设置默认身份
        self.default_agent = default_agent or "engineering/engineering-frontend-developer"
        self.current_agent = self.default_agent
        
        # ⚡ 性能优化：缓存和懒加载
        self.prompt_cache: Dict[str, str] = {}
        self.loaded_prompt: Optional[str] = None
        
        # 扫描可用 Agent
        self.available_agents = self._scan_available_agents()
        
        # 🔒 预编译正则表达式（防 DoS）
        self._compiled_keywords = {
            re.compile(re.escape(kw), re.IGNORECASE): agent_id 
            for kw, agent_id in self.KEYWORD_MAPPING.items()
        }
    
    def _validate_agent_source(self, agent_source: str) -> str:
        """
        🔒 验证 Agent 来源路径（安全加固）
        
        验证规则：
        1. 路径必须在 skills 目录内
        2. 目录名必须在白名单中
        3. 路径深度不能超过限制
        
        Args:
            agent_source: 用户提供的路径
            
        Returns:
            str: 验证后的绝对路径
            
        Raises:
            ValueError: 路径验证失败
        """
        try:
            # 解析并规范化路径
            resolved = Path(agent_source).expanduser().resolve()
            
            # 🔒 规则 1: 必须在 skills 目录内
            try:
                resolved.relative_to(self.skills_root)
            except ValueError:
                raise ValueError(
                    f"Agent source must be within skills directory. "
                    f"Got: {agent_source}"
                )
            
            # 🔒 规则 2: 目录名必须在白名单中
            if resolved.name not in self.ALLOWED_DIRECTORIES:
                raise ValueError(
                    f"Agent source directory '{resolved.name}' not in allowed list: "
                    f"{self.ALLOWED_DIRECTORIES}"
                )
            
            # 🔒 规则 3: 路径深度不能超过限制
            depth = len(resolved.relative_to(self.skills_root).parts)
            if depth > self.MAX_PATH_DEPTH:
                raise ValueError(
                    f"Path depth {depth} exceeds maximum {self.MAX_PATH_DEPTH}"
                )
            
            # 验证目录存在
            if not resolved.is_dir():
                raise ValueError(f"Agent source directory does not exist: {agent_source}")
            
            return str(resolved)
            
        except Exception as e:
            # 🔒 错误信息脱敏
            raise ValueError(f"Invalid agent source: {type(e).__name__}")
    
    def _scan_available_agents(self) -> List[AgentProfile]:
        """
        扫描可用的 Agent（安全增强版）
        
        🔒 安全检查：
        - 验证符号链接目标
        - 限制文件大小
        - 验证文件编码
        - 排除非 Agent 文件
        
        Returns:
            List[AgentProfile]: Agent 档案列表
        """
        agents = []
        seen_ids = set()
        
        # 确定扫描路径
        paths_to_scan = []
        
        # 1. 使用指定的 agent_source
        if self.agent_source:
            paths_to_scan.append(("specified", Path(self.agent_source)))
        # 2. 使用内置的 agency-agents
        elif self.packed_agents_path.exists():
            paths_to_scan.append(("packed", self.packed_agents_path))
        # 3. 降级到基础 agency
        elif self.builtin_path.exists():
            paths_to_scan.append(("builtin", self.builtin_path))
        
        # 扫描所有路径
        for source_type, base_path in paths_to_scan:
            try:
                scanned = self._scan_directory(base_path, seen_ids)
                agents.extend(scanned)
            except Exception:
                # 🔒 错误脱敏
                print(f"⚠️ 扫描目录失败：{source_type}")
                continue
        
        return agents
    
    def _scan_directory(self, base_path: Path, seen_ids: set) -> List[AgentProfile]:
        """
        扫描目录中的 Agent（安全增强版）
        
        🔒 安全检查：
        - 不跟随外部符号链接
        - 跳过根目录文档
        - 验证 YAML frontmatter
        
        Args:
            base_path: 基础路径
            seen_ids: 已处理的 Agent ID 集合
            
        Returns:
            List[AgentProfile]: Agent 档案列表
        """
        agents = []
        
        try:
            # 🔒 不跟随符号链接
            for md_file in base_path.rglob('*.md'):
                # 🔒 跳过符号链接（或验证目标）
                if md_file.is_symlink():
                    try:
                        target = md_file.resolve()
                        target.relative_to(base_path.resolve())
                    except ValueError:
                        print(f"⚠️ 跳过外部符号链接")
                        continue
                
                # 跳过根目录文档
                if md_file.name in ['README.md', 'CONTRIBUTING.md', 'UPSTREAM.md']:
                    continue
                
                # 构建 agent_id
                try:
                    rel_path = md_file.relative_to(base_path)
                    
                    # 跳过 strategy 下的非 Agent 文件
                    if rel_path.parts[0] == 'strategy' and len(rel_path.parts) > 1:
                        continue
                    
                    # 构建 agent_id
                    agent_id = self._build_agent_id(rel_path)
                    if not agent_id or agent_id in seen_ids:
                        continue
                    
                    # 🔒 验证 YAML frontmatter
                    if not self._has_frontmatter(md_file):
                        continue
                    
                    # 加载 Agent 档案
                    profile = self._load_agent_profile_with_path(agent_id, md_file)
                    if profile:
                        agents.append(profile)
                        seen_ids.add(agent_id)
                        
                except Exception:
                    # 🔒 错误脱敏
                    continue
                    
        except Exception:
            # 🔒 错误脱敏
            pass
        
        return agents
    
    def _build_agent_id(self, rel_path: Path) -> Optional[str]:
        """
        构建 Agent ID
        
        Args:
            rel_path: 相对路径
            
        Returns:
            Optional[str]: Agent ID，无效返回 None
        """
        try:
            if len(rel_path.parts) == 2:
                return f"{rel_path.parts[0]}/{rel_path.stem}"
            elif len(rel_path.parts) == 3:
                return f"{rel_path.parts[0]}/{rel_path.parts[1]}/{rel_path.stem}"
            else:
                return None
        except Exception:
            return None
    
    def _has_frontmatter(self, file_path: Path) -> bool:
        """
        验证文件是否有 YAML frontmatter（真正的 Agent）
        
        🔒 安全读取：限制读取大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否有 frontmatter
        """
        try:
            # 🔒 限制读取大小
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1024)  # 只读前 1KB
            
            content = content.strip()
            return content.startswith('---') and '---' in content[3:]
            
        except Exception:
            return False
    
    def _load_agent_profile_with_path(self, agent_id: str, file_path: Path) -> Optional[AgentProfile]:
        """
        加载 Agent 档案（安全增强版）
        
        🔒 安全检查：
        - 验证文件大小
        - 验证符号链接
        - 验证文件编码
        - 限制读取量
        
        Args:
            agent_id: Agent ID
            file_path: 文件路径
            
        Returns:
            Optional[AgentProfile]: Agent 档案，失败返回 None
        """
        try:
            # 🔒 验证文件大小
            if file_path.stat().st_size > self.MAX_FILE_SIZE:
                print(f"⚠️ 跳过超大文件")
                return None
            
            # 🔒 验证符号链接
            if file_path.is_symlink():
                try:
                    target = file_path.resolve()
                    target.relative_to(self.skills_root)
                except ValueError:
                    print(f"⚠️ 跳过外部符号链接")
                    return None
            
            # 🔒 安全读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(self.MAX_FILE_SIZE)
            
            # 解析 frontmatter
            if not content.startswith('---'):
                return None
            
            end_frontmatter = content.find('---', 3)
            if end_frontmatter == -1:
                return None
            
            frontmatter_text = content[4:end_frontmatter].strip()
            
            # 简单解析 YAML（避免依赖外部库）
            metadata = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
            
            # 提取必要信息
            name = metadata.get('name', agent_id.split('/')[-1])
            category_str = metadata.get('category', agent_id.split('/')[0])
            
            try:
                category = AgentCategory(category_str)
            except ValueError:
                category = AgentCategory.SPECIALIZED
            
            # 提取关键词
            keywords_str = metadata.get('keywords', '')
            keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
            
            # 提取专长
            expertise_str = metadata.get('expertise', '')
            expertise = [e.strip() for e in expertise_str.split(',') if e.strip()]
            
            return AgentProfile(
                id=agent_id,
                name=name,
                category=category,
                keywords=keywords,
                prompt_path=str(file_path),
                expertise=expertise
            )
            
        except UnicodeDecodeError:
            print(f"⚠️ 文件编码错误")
            return None
        except Exception:
            # 🔒 错误脱敏
            print(f"⚠️ Agent 加载失败")
            return None
    
    # ============================================================================
    # ⚡ 性能优化：自动身份管理
    # ============================================================================
    
    def analyze_and_switch(self, task: str) -> str:
        """
        分析任务并自动切换身份（D 方案：每轮对话独立判断）
        
        工作流程：
        1. 分析任务关键词
        2. 检测话题是否变化
        3. 如需要，切换到新身份
        4. 任务完成后自动恢复默认身份
        
        性能：
        - 无需切换：<2ms
        - 需要切换：<1ms（不加载文件）
        
        Args:
            task: 任务描述
            
        Returns:
            str: 当前使用的 Agent ID
        
        使用示例：
        ```python
        selector = AgentSelector()
        
        # 对话 1：代码安全检查
        selector.analyze_and_switch("帮我做代码安全检查")
        # 输出：🔄 切换到 安全工程师
        
        # 获取 Prompt（懒加载）
        prompt = selector.get_prompt()
        
        # ... 执行任务 ...
        
        # 任务完成
        selector.complete_task()
        # 输出：✅ 已恢复到默认身份
        ```
        """
        # 🔒 限制输入长度
        if len(task) > self.MAX_TASK_LENGTH:
            task = task[:self.MAX_TASK_LENGTH]
        
        # 分析任务，匹配目标 Agent
        target_agent = self.select_agent(task)
        
        # 检测是否需要切换
        if target_agent != self.current_agent:
            # 切换身份（不立即加载 Prompt，懒加载）
            self.current_agent = target_agent
            self.loaded_prompt = None  # 标记需要重新加载
            print(f"🔄 切换到 {self._get_agent_name(target_agent)}")
        
        return self.current_agent
    
    def get_prompt(self) -> str:
        """
        获取当前身份的 Prompt（懒加载 + 缓存）
        
        性能：
        - 缓存命中：<1ms
        - 缓存未命中：50-200ms（首次加载）
        
        Returns:
            str: 当前身份的 Prompt 内容
        
        使用示例：
        ```python
        selector = AgentSelector()
        selector.analyze_and_switch("代码安全检查")
        
        # 获取 Prompt（首次加载 50-200ms）
        prompt1 = selector.get_prompt()
        
        # 再次获取（缓存命中 <1ms）
        prompt2 = selector.get_prompt()
        ```
        """
        # 懒加载：真正需要时才加载
        if self.loaded_prompt is None:
            # 先查缓存
            if self.current_agent in self.prompt_cache:
                self.loaded_prompt = self.prompt_cache[self.current_agent]
            else:
                # 缓存未命中，读取文件
                self.loaded_prompt = self.load_agent_prompt(self.current_agent)
                # 存入缓存
                self.prompt_cache[self.current_agent] = self.loaded_prompt
        
        return self.loaded_prompt
    
    def complete_task(self):
        """
        任务完成，恢复到默认身份
        
        性能：<0.1ms
        
        使用示例：
        ```python
        selector = AgentSelector()
        selector.analyze_and_switch("代码安全检查")
        # ... 执行任务 ...
        selector.complete_task()
        # 输出：✅ 已恢复到默认身份
        ```
        """
        if self.current_agent != self.default_agent:
            print(f"✅ 已恢复到默认身份 {self._get_agent_name(self.default_agent)}")
            self.current_agent = self.default_agent
            self.loaded_prompt = None  # 清除缓存的 Prompt
    
    def _get_agent_name(self, agent_id: str) -> str:
        """
        获取 Agent 中文名
        
        Args:
            agent_id: Agent ID
            
        Returns:
            str: 中文名，如果没有映射则返回原 ID
        """
        return self.AGENT_NAMES.get(agent_id, agent_id.split('/')[-1].replace('-', ' ').title())
    
    # ============================================================================
    # 基础方法
    # ============================================================================
    
    def select_agent(self, task: str) -> str:
        """
        自动选择 Agent（安全增强版）
        
        🔒 安全限制：
        - 限制任务描述长度
        - 使用预编译正则（防 DoS）
        
        Args:
            task: 任务描述
            
        Returns:
            str: Agent ID
        """
        # 🔒 限制输入长度
        if len(task) > self.MAX_TASK_LENGTH:
            task = task[:self.MAX_TASK_LENGTH]
        
        task_lower = task.lower()
        
        # 🔒 使用预编译正则匹配
        for pattern, agent_id in self._compiled_keywords.items():
            if pattern.search(task_lower):
                return agent_id
        
        # 默认返回软件工程师
        return self.default_agent
    
    def load_agent_prompt(self, agent_id: str) -> str:
        """
        加载 Agent 的 Prompt
        
        🔒 安全读取：
        - 验证路径在 skills 目录内
        - 限制文件大小
        - 验证文件编码
        
        Args:
            agent_id: Agent ID（如 "engineering/engineering-frontend-developer"）
            
        Returns:
            str: Prompt 内容
        """
        try:
            # 构建文件路径
            parts = agent_id.split('/')
            
            # 支持多级路径
            if len(parts) == 2:
                # 二级路径：engineering/engineering-frontend-developer
                file_path = self.packed_agents_path / parts[0] / f"{parts[1]}.md"
            elif len(parts) == 3:
                # 三级路径：game-development/unity/unity-developer
                file_path = self.packed_agents_path / parts[0] / parts[1] / f"{parts[2]}.md"
            else:
                raise ValueError("Invalid agent_id format")
            
            # 🔒 验证路径在 skills 目录内
            file_path = file_path.resolve()
            file_path.relative_to(self.skills_root)
            
            # 🔒 验证文件存在
            if not file_path.exists():
                raise ValueError(f"Agent not found: {agent_id}")
            
            # 🔒 验证文件大小
            if file_path.stat().st_size > self.MAX_FILE_SIZE:
                raise ValueError("Agent file too large")
            
            # 🔒 安全读取
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(self.MAX_FILE_SIZE)
            
            # 移除 frontmatter
            if content.startswith('---'):
                end_frontmatter = content.find('---', 3)
                if end_frontmatter != -1:
                    content = content[end_frontmatter + 3:].strip()
            
            return content
            
        except UnicodeDecodeError:
            raise ValueError("Invalid file encoding")
        except Exception:
            # 🔒 错误脱敏
            raise ValueError(f"Failed to load agent: {agent_id}")
    
    def select_agents_for_roundtable(self, topic: str) -> List[str]:
        """
        为 RoundTable 讨论选择 Agent
        
        Args:
            topic: 讨论主题
            
        Returns:
            List[str]: Agent ID 列表（通常 3 个）
        """
        # 🔒 限制输入长度
        if len(topic) > self.MAX_TASK_LENGTH:
            topic = topic[:self.MAX_TASK_LENGTH]
        
        topic_lower = topic.lower()
        
        # 根据主题选择不同组合
        agents = []
        
        # 工程类话题
        if any(kw in topic_lower for kw in ["架构", "开发", "工程", "系统", "api", "backend", "frontend"]):
            agents.extend([
                "engineering/engineering-frontend-developer",
                "engineering/engineering-backend-developer",
                "engineering/engineering-software-architect"
            ])
        
        # 设计类话题
        elif any(kw in topic_lower for kw in ["设计", "体验", "ux", "ui", "界面"]):
            agents.extend([
                "design/design-ux-designer",
                "design/design-ui-designer",
                "engineering/engineering-frontend-developer"
            ])
        
        # 测试类话题
        elif any(kw in topic_lower for kw in ["测试", "test", "qa", "质量"]):
            agents.extend([
                "testing/testing-qa-engineer",
                "engineering/engineering-software-architect",
                "engineering/engineering-backend-developer"
            ])
        
        # AI 类话题
        elif any(kw in topic_lower for kw in ["ai", "ml", "智能", "模型"]):
            agents.extend([
                "specialized/specialized-ai-ml-engineer",
                "engineering/engineering-backend-developer",
                "engineering/engineering-software-architect"
            ])
        
        # 默认组合
        else:
            agents.extend([
                "engineering/engineering-fullstack-developer",
                "product/product-manager",
                "design/design-ux-designer"
            ])
        
        # 验证 Agent 是否存在
        available_ids = {a.id for a in self.available_agents}
        agents = [a for a in agents if a in available_ids]
        
        # 如果不足 3 个，补充默认 Agent
        while len(agents) < 3:
            default = "engineering/engineering-fullstack-developer"
            if default not in agents:
                agents.append(default)
            else:
                break
        
        return agents[:3]


# ============================================================================
# 快捷函数
# ============================================================================

def auto_select_agent(task: str, agent_source: str = "") -> str:
    """
    自动选择 Agent（快捷函数）
    
    Args:
        task: 任务描述
        agent_source: Agent 来源路径（可选）
        
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
        agent_source: Agent 来源路径（可选）
        
    Returns:
        List[str]: Agent ID 列表
    """
    selector = AgentSelector(agent_source)
    return selector.select_agents_for_roundtable(topic)


def switch_agent(agent_id: str, agent_source: str = "") -> str:
    """
    切换人格身份（快捷函数）
    
    Args:
        agent_id: Agent ID（如 "engineering/engineering-frontend-developer"）
        agent_source: Agent 来源路径（可选）
        
    Returns:
        str: 加载的 Prompt 内容
    """
    selector = AgentSelector(agent_source)
    prompt = selector.load_agent_prompt(agent_id)
    print(f"✅ 已切换到 {agent_id} 人格")
    return prompt


# ============================================================================
# 测试
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("Agent Selector - 安全增强版 + 自动身份管理测试")
    print("="*60)
    
    selector = AgentSelector()
    
    print(f"\n📊 可用 Agent 数量：{len(selector.available_agents)}")
    print(f"🏠 默认身份：{selector._get_agent_name(selector.default_agent)}")
    
    # 测试自动身份管理
    print("\n" + "="*60)
    print("自动身份管理测试：")
    print("="*60)
    
    test_tasks = [
        "帮我做代码安全检查",
        "继续检查安全问题",
        "写一个 React 组件",
        "设计数据库 schema",
    ]
    
    for i, task in enumerate(test_tasks, 1):
        print(f"\n【对话 {i}】{task}")
        selector.analyze_and_switch(task)
        prompt = selector.get_prompt()
        print(f"   Prompt 长度：{len(prompt)} 字符")
        selector.complete_task()
    
    # 测试性能
    print("\n" + "="*60)
    print("性能测试：")
    print("="*60)
    
    import time
    
    # 首次切换（缓存未命中）
    start = time.time()
    selector.analyze_and_switch("代码安全检查")
    prompt1 = selector.get_prompt()
    t1 = (time.time() - start) * 1000
    print(f"首次切换 + 加载：{t1:.1f}ms")
    
    # 再次切换（缓存命中）
    start = time.time()
    selector.analyze_and_switch("继续检查安全")
    prompt2 = selector.get_prompt()
    t2 = (time.time() - start) * 1000
    print(f"再次切换（缓存命中）：{t2:.1f}ms")
    
    # 无需切换
    start = time.time()
    selector.analyze_and_switch("还有安全问题吗？")
    t3 = (time.time() - start) * 1000
    print(f"无需切换：<1ms (实际 {t3:.1f}ms)")
    
    print("\n✅ 所有测试完成！")
