"""
GapDetector — 技能缺口检测器 v2.0
===================================
整合 skill-evolver 的 generate_skill_draft() 能力

v2.0 改进：
  - 新增 CAPABILITY_KEYWORDS 能力关键词体系
  - 新增 get_active_capabilities() 从 scores.json 推断用户能力需求
  - 新增 scan_shared_skills() 扫描 SharedSkills 技能清单
  - 新增 detect_gaps_from_scores() 基于评分数据检测缺口
  - 新增 generate_skill_draft() 生成完整的 SKILL.md 草稿
  - 原有 detect_gaps() 保留，两个数据源互补

与 skill-evolver 共用 ~/.skill_scoreboard/scores.json
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import Counter

# ── 与 skill-evolver 共用路径 ────────────────────────────────────────────────
SKILL_DB_DIR = Path.home() / ".skill_scoreboard"
SHARED_SKILLS = Path.home() / "SharedSkills"
DB_FILE = SKILL_DB_DIR / "scores.json"


# ── 能力关键词体系（来自 skill-evolver） ─────────────────────────────────────
CAPABILITY_KEYWORDS = {
    # 信息处理类
    '搜索/研究': ['search', 'research', '查找', '调研', '论文', '新闻', 'tavily', 'arxiv'],
    '网页抓取': ['fetch', 'crawl', 'scrape', '抓取', '网页', 'web_fetch'],
    '文档总结': ['summarize', '总结', '摘要', '概括', '阅读理解'],
    '翻译': ['translate', '翻译', '中英', 'language'],
    '数据分析': ['analyze', 'analysis', '数据', '统计', 'analytics', 'pandas'],
    '代码审查': ['code review', 'review', '审查', 'lint', 'prettier'],

    # 媒体类
    '图片生成': ['image', 'generate image', '画图', 'AI画图', 'midjourney', 'dalle'],
    '视频生成': ['video', '视频', '生成视频'],
    '音频处理': ['audio', '音频', '语音', 'tts', 'stt'],
    '音乐生成': ['music', '音乐', 'suno', 'song'],

    # 办公类
    'PPT制作': ['ppt', 'powerpoint', '演示', '幻灯片', 'slides'],
    '文档写作': ['write', '写作', '文档', 'report', '文案'],
    '飞书集成': ['feishu', 'lark', '飞书', '文档', 'wiki', '云文档'],
    '邮件处理': ['email', '邮件', 'imap', 'smtp', 'himalaya'],

    # 开发类
    '代码生成': ['code', '代码', '写代码', 'generate code', 'copilot'],
    'Git操作': ['git', 'github', 'commit', 'branch', 'pull request'],
    'Shell命令': ['shell', 'bash', 'exec', 'terminal', '命令行'],
    'API调试': ['api', 'http', 'request', '调试', 'postman'],

    # 智能体类
    '任务规划': ['plan', '规划', '分解任务', 'task planning'],
    '自我改进': ['self-improve', '自我提升', '蒸馏', 'dream', 'm-flow'],
    '技能进化': ['skill', '技能', 'capability', 'evolution', '进化的'],
    '学习能力': ['learn', '学习', 'adapt', '适应', '新技能'],
}


class GapDetector:
    """技能缺口检测器 v2.0"""

    # 已有的技能类型（保留原有分类）
    SKILL_CATEGORIES = {
        'memory': '记忆管理',
        'code': '代码开发',
        'research': '研究搜索',
        'creative': '创意生成',
        'social': '社交媒体',
        'productivity': '效率工具',
        'data': '数据处理',
        'mlops': '机器学习运维',
        'devops': 'DevOps',
        'security': '安全相关',
        'communication': '通讯工具',
        'media': '媒体处理',
    }

    def __init__(self, work_analysis: Dict, skill_scores: Dict, skill_registry: Dict):
        """
        初始化缺口检测器
        work_analysis: WorkAnalyzer 的分析结果
        skill_scores: SkillScorer 的评分结果
        skill_registry: SkillRegistry 的技能注册表
        """
        self.work_analysis = work_analysis
        self.skill_scores = skill_scores
        self.skill_registry = skill_registry
        self._scores_cache = None

    # ── v2.0 新增：scores.json 数据加载 ───────────────────────────────────────

    def _load_scores(self) -> Dict:
        """加载 skill-scoreboard 评分数据（带缓存）"""
        if self._scores_cache is not None:
            return self._scores_cache
        if DB_FILE.exists():
            try:
                self._scores_cache = json.loads(DB_FILE.read_text(encoding='utf-8'))
                return self._scores_cache
            except Exception:
                pass
        self._scores_cache = {}
        return self._scores_cache

    def get_active_capabilities(self, days: int = 30) -> Counter:
        """
        从已有技能的调用分布，推断用户需要的能力类型。
        返回: Counter({能力类型: 调用次数})
        """
        scores = self._load_scores()
        today = datetime.now()
        week_ago = (today - __import__('datetime').timedelta(days=days)).isoformat()[:10]

        active_capabilities = Counter()

        for skill, data in scores.items():
            call_log = data.get('call_log', [])
            recent = [c for c in call_log if c.get('time', '')[:10] >= week_ago]
            if not recent:
                continue

            call_count = len(recent)
            skill_lower = skill.lower()

            for cap, keywords in CAPABILITY_KEYWORDS.items():
                if any(kw in skill_lower for kw in keywords):
                    active_capabilities[cap] += call_count
                    break

        return active_capabilities

    def scan_shared_skills(self) -> dict:
        """扫描 SharedSkills，返回技能清单（含元信息）"""
        skills = {}
        if not SHARED_SKILLS.exists():
            return skills

        for skill_dir in SHARED_SKILLS.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue

            name = skill_dir.name
            skill_md = skill_dir / "SKILL.md"
            desc = ""
            triggers = []

            if skill_md.exists():
                try:
                    content = skill_md.read_text(encoding='utf-8')
                    desc_match = re.search(r'description:\s*\"?([^\"\n]+)\"?', content)
                    if desc_match:
                        desc = desc_match.group(1).strip()
                    triggers_match = re.search(r'triggers:\s*\n((?:-\s*[^\n]+\n)+)', content)
                    if triggers_match:
                        for line in triggers_match.group(1).split('\n'):
                            m = re.match(r'-\s*\"?([^\"]+)\"?', line.strip())
                            if m:
                                triggers.append(m.group(1).strip())
                except Exception:
                    pass

            skills[name] = {
                'path': str(skill_dir),
                'description': desc,
                'triggers': triggers,
                'has_errors': (skill_dir / '.error').exists(),
            }

        return skills

    # ── v2.0 新增：基于评分数据的缺口检测 ──────────────────────────────────────

    def detect_gaps_from_scores(self) -> List[Dict]:
        """
        基于 scores.json 检测技能缺口（来自 skill-evolver）。
        返回需要开发的新技能列表。
        """
        scores = self._load_scores()
        shared_skills = self.scan_shared_skills()
        active_caps = self.get_active_capabilities(days=30)
        all_active_caps = set(active_caps.keys())

        # 已覆盖的能力
        covered_caps = set()
        for cap, keywords in CAPABILITY_KEYWORDS.items():
            for skill in shared_skills.keys():
                skill_lower = skill.lower()
                if any(kw in skill_lower for kw in keywords):
                    covered_caps.add(cap)
                    break

        # 缺口 = 常用但不覆盖的能力
        missing_caps = all_active_caps - covered_caps
        gaps = []

        for cap in missing_caps:
            recent_count = active_caps.get(cap, 0)
            if recent_count > 0:
                gaps.append({
                    'type': 'missing_capability',
                    'capability': cap,
                    'recent_calls': recent_count,
                    'urgency': 'high' if recent_count >= 3 else 'medium',
                    'reason': f"近30天有{recent_count}次调用但无对应技能",
                    'source': 'scores',
                })

        # 按紧急程度排序
        gaps.sort(key=lambda x: (
            {'high': 0, 'medium': 1, 'low': 2}.get(x.get('urgency', 'low'), 2),
            -x.get('recent_calls', 0)
        ))

        return gaps

    # ── v2.0 新增：生成 SKILL.md 草稿 ────────────────────────────────────────

    def generate_skill_draft(self, gap: Dict) -> Optional[Dict]:
        """
        根据缺口生成完整的 SKILL.md 草稿。
        返回 {'name': ..., 'draft': ..., 'triggers': [...]} 或 None。
        """
        cap = gap.get('capability', '')
        urgency = gap.get('urgency', 'medium')

        # 能力 → 技能名 + 触发词 + 草稿内容
        SKILL_TEMPLATES = {
            '搜索/研究': {
                'name': 'deep-researcher',
                'triggers': ['帮我调研', '深入研究', '搜索论文', 'AI新闻', '竞品分析'],
                'draft': """---
name: deep-researcher
description: 深度研究助手 — 自动搜索、筛选、总结多个信息源的research技能
triggers:
- 帮我调研
- 深入研究
- 搜索论文
- AI新闻
- 竞品分析
---

# deep-researcher

## 使用场景
- 需要从多个来源收集信息的研究任务
- 竞品分析、市场调研
- 学术论文搜索与总结

## 步骤
1. 使用 web_search 搜索多个关键词
2. 对每个结果用 web_fetch 抓取内容
3. 提取关键信息，生成结构化摘要
4. 如需最新信息，使用 tavily API

## 工具
- web_search / web_fetch
- 可选：tavily search API

## 质量标准
- 至少3个独立来源
- 标注信息来源和时效性
"""},
            '文档总结': {
                'name': 'doc-summarizer',
                'triggers': ['总结文档', '帮我概括', '阅读摘要', '长文章总结'],
                'draft': """---
name: doc-summarizer
description: 文档总结助手 — 长文本/多文档自动摘要的关键技能
triggers:
- 总结文档
- 帮我概括
- 阅读摘要
- 长文章总结
---

# doc-summarizer

## 使用场景
- 长文档快速概览
- 多份文档横向对比总结
- 论文摘要提取

## 步骤
1. 读取或抓取文档内容
2. 识别核心论点（首段/末段/小标题）
3. 生成3-5句话的核心摘要
4. 列出关键数据和结论
"""},
            'PPT制作': {
                'name': 'ppt-generator',
                'triggers': ['制作PPT', '生成幻灯片', '演示文稿', '做汇报'],
                'draft': """---
name: ppt-generator
description: PPT自动生成 — 根据主题和大纲生成PPT文稿和设计建议
triggers:
- 制作PPT
- 生成幻灯片
- 演示文稿
- 做汇报
---

# ppt-generator

## 使用场景
- 快速生成汇报PPT大纲
- 根据文档生成PPT
- 输出可导入Keynote/PPT的XML/大纲

## 工具
- powerpoint skill（实际生成.pptx）
- 或输出 Markdown 大纲供人工制作

## 步骤
1. 确定PPT主题和受众
2. 生成大纲（5-8页）
3. 每页：标题 + 要点 + 备注
4. 如需生成.pptx，使用 python-pptx 库
"""},
            '数据分析': {
                'name': 'data-analyst',
                'triggers': ['分析数据', '数据可视化', '统计', '生成图表'],
                'draft': """---
name: data-analyst
description: 数据分析助手 — 数据清洗、统计分析、可视化的端到端技能
triggers:
- 分析数据
- 数据可视化
- 统计
- 生成图表
---

# data-analyst

## 使用场景
- CSV/Excel 数据清洗和预处理
- 描述性统计和趋势分析
- 生成 matplotlib/seaborn 可视化图表

## 步骤
1. 加载数据（pandas read_csv/read_excel）
2. 数据清洗（去重、缺失值处理、类型转换）
3. 统计分析（describe、相关性、分组聚合）
4. 生成可视化图表
5. 撰写分析结论

## 工具
- pandas, numpy
- matplotlib, seaborn
- scipy.stats（统计检验）
"""},
            '翻译': {
                'name': 'translator',
                'triggers': ['翻译', '中英互译', '润色英文', '翻译文案'],
                'draft': """---
name: translator
description: 翻译与润色助手 — 中英互译、专业术语处理、语境适配
triggers:
- 翻译
- 中英互译
- 润色英文
- 翻译文案
---

# translator

## 使用场景
- 中英互译
- 专业文档翻译（技术/商业/学术）
- 英文润色和语法检查

## 步骤
1. 识别语言对和领域类型
2. 逐段翻译，保留专业术语
3. 检查术语一致性
4. 润色目标语言表达（流畅度、地道性）
"""},
            '网页抓取': {
                'name': 'web-scraper',
                'triggers': ['抓取网页', '爬取数据', '提取网页内容', '批量获取页面'],
                'draft': """---
name: web-scraper
description: 网页抓取助手 — 批量抓取、解析、提取结构化数据
triggers:
- 抓取网页
- 爬取数据
- 提取网页内容
- 批量获取页面
---

# web-scraper

## 使用场景
- 批量抓取列表页数据
- 提取正文内容（去除广告/导航）
- 结构化数据抽取（表格、商品信息）

## 步骤
1. requests 获取页面 HTML
2. BeautifulSoup 解析 DOM
3. CSS选择器/xpath 提取目标字段
4. 清洗后输出 JSON/CSV

## 注意事项
- 遵守 robots.txt 和网站服务条款
- 控制请求频率，避免封禁
"""},
            '图片生成': {
                'name': 'image-generator',
                'triggers': ['生成图片', 'AI画图', '帮我画', '生成插画', '图片生成'],
                'draft': """---
name: image-generator
description: AI图片生成助手 — 描述生成图片、风格转换、图片编辑
triggers:
- 生成图片
- AI画图
- 帮我画
- 生成插画
- 图片生成
---

# image-generator

## 使用场景
- 根据文本描述生成图片
- 现有图片的风格转换
- 产品图、宣传图、海报生成

## 工具
- image_generate skill（即梦/图片生成）
- 可选：DALL-E、Midjourney API

## 步骤
1. 理解用户需求，提取画面描述关键词
2. 构建英文 prompt（更利于图片生成AI）
3. 调用图片生成工具
4. 如需调整，提取反馈并重新生成
"""},
            '视频生成': {
                'name': 'video-generator',
                'triggers': ['生成视频', 'AI视频', '视频制作', '生成短视频'],
                'draft': """---
name: video-generator
description: AI视频生成助手 — 文本/图片转视频、配音、字幕
triggers:
- 生成视频
- AI视频
- 视频制作
- 生成短视频
---

# video-generator

## 使用场景
- 文本描述生成视频片段
- 图片生成视频动画
- 短视频脚本和成品制作

## 工具
- 可用：图片生成 + ffmpeg 组合
- 可选：Runway、Pika、PIKA API

## 步骤
1. 确定视频主题和时长
2. 生成关键帧图片
3. 组装成视频（ffmpeg）
4. 添加字幕和背景音乐
"""},
            'Git操作': {
                'name': 'git-assistant',
                'triggers': ['Git操作', 'commit', '分支管理', '解决冲突', 'PR'],
                'draft': """---
name: git-assistant
description: Git操作助手 — commit、branch、merge、冲突解决、PR管理
triggers:
- Git操作
- commit
- 分支管理
- 解决冲突
- PR
---

# git-assistant

## 使用场景
- 日常 Git commit、push、pull
- 分支创建、切换、合并
- Git 冲突快速解决
- Pull Request 创建和管理

## 步骤
1. 了解当前工作目录的 Git 状态
2. 根据需求选择合适的 Git 操作
3. 执行操作并处理可能的冲突
4. 确认最终状态
"""},
            'Shell命令': {
                'name': 'shell-automation',
                'triggers': ['Shell命令', '写脚本', '批处理', '自动化脚本'],
                'draft': """---
name: shell-automation
description: Shell自动化助手 — 编写、调试、优化Shell脚本和批处理任务
triggers:
- Shell命令
- 写脚本
- 批处理
- 自动化脚本
---

# shell-automation

## 使用场景
- 编写日常自动化脚本
- 数据批量处理任务
- 系统管理脚本
- CI/CD 流水线脚本

## 步骤
1. 理解任务需求，拆解步骤
2. 编写 shell 脚本（bash）
3. 添加错误处理和日志
4. 测试脚本，确认安全后执行
"""},
            '飞书集成': {
                'name': 'feishu-integration',
                'triggers': ['飞书集成', '飞书文档', '飞书消息', '飞书机器人'],
                'draft': """---
name: feishu-integration
description: 飞书集成助手 — 文档管理、消息发送、机器人交互
triggers:
- 飞书集成
- 飞书文档
- 飞书消息
- 飞书机器人
---

# feishu-integration

## 使用场景
- 读写飞书云文档
- 发送飞书消息给用户/群组
- 飞书机器人 webhook
- 拉取飞书消息记录

## 工具
- 飞书开放平台 API
- feishu/飞书 skill
"""},
        }

        template = SKILL_TEMPLATES.get(cap)
        if not template:
            # 通用草稿（无具体模板时）
            # 能力 → 英文标识符映射（避免中文正则替换问题）
            CAP_NAME_MAP = {
                '图片生成': 'image-generation', '视频生成': 'video-generation',
                '音频处理': 'audio-processing', '音乐生成': 'music-generation',
                '翻译': 'translation', '飞书集成': 'feishu-integration',
                '邮件处理': 'email-handling', '代码审查': 'code-review',
                '任务规划': 'task-planning', '自我改进': 'self-improvement',
                '技能进化': 'skill-evolution', '学习能力': 'learning',
                'API调试': 'api-debug', 'Git操作': 'git-ops',
                'Shell命令': 'shell-automation', '网页抓取': 'web-scraping',
            }
            safe_name = CAP_NAME_MAP.get(cap, f'new-skill-{cap}')
            return {
                'name': safe_name,
                'capability': cap,
                'triggers': [cap],
                'draft': f"""---
name: {safe_name}
description: {cap} — 由技能缺口检测自动生成
triggers:
- {cap}
---

# {safe_name}

## 使用场景
- {gap.get('reason', '满足' + cap + '能力需求')}

## 步骤
1. 理解用户需求
2. 规划执行步骤
3. 调用相关工具完成任务
4. 返回结果

## 工具
- 待定（根据实际使用场景补充）
"""}
        return {
            'name': template['name'],
            'capability': cap,
            'triggers': template['triggers'],
            'draft': template['draft'],
            'urgency': urgency,
        }

    # ── v2.0 新增：完整缺口报告（含草稿）───────────────────────────────────────

    def detect_and_generate(self) -> Dict:
        """
        执行完整缺口检测流程：
        1. 从 scores.json 检测能力缺口
        2. 生成 SKILL.md 草稿
        返回 {
            'gaps': [...],           # 缺口列表
            'drafts': [...],         # SKILL.md 草稿列表
            'missing_capabilities': [...],
            'outdated_skills': [...],
        }
        """
        scores = self._load_scores()
        shared_skills = self.scan_shared_skills()

        # 1. 基于评分数据的缺口
        score_gaps = self.detect_gaps_from_scores()

        # 2. 生成草稿
        drafts = []
        for gap in score_gaps:
            draft = self.generate_skill_draft(gap)
            if draft:
                drafts.append(draft)

        # 3. 过时技能（90天+未用）
        outdated = []
        for skill, data in scores.items():
            last = data.get('last_call', '')
            if last:
                try:
                    days_ago = (datetime.now() - datetime.fromisoformat(last[:10])).days
                    if days_ago >= 90:
                        outdated.append({
                            'skill': skill,
                            'days_ago': days_ago,
                            'last_score': round(data.get('score', 0), 2),
                        })
                except Exception:
                    pass

        return {
            'gaps': score_gaps,
            'drafts': drafts,
            'missing_capabilities': score_gaps,
            'outdated_skills': sorted(outdated, key=lambda x: -x['days_ago']),
            'scanned_at': datetime.now().isoformat(),
        }

    # ── 原有方法（保留兼容）───────────────────────────────────────────────────

    def detect_gaps(self) -> List[Dict]:
        """
        v2.0: 整合两个数据源的缺口检测。
        原 detect_gaps() 逻辑保留，同时加入 scores 数据源的缺口。
        """
        gaps = []

        # 1. 从未完成任务分析（原有逻辑）
        task_gaps = self._detect_from_tasks()
        gaps.extend(task_gaps)

        # 2. 从技能活跃度分析（原有逻辑）
        activity_gaps = self._detect_from_activity()
        gaps.extend(activity_gaps)

        # 3. 从工作类型分析（原有逻辑）
        type_gaps = self._detect_from_work_type()
        gaps.extend(type_gaps)

        # 4. v2.0: 从 scores.json 检测能力缺口（新逻辑）
        score_gaps = self.detect_gaps_from_scores()
        for sg in score_gaps:
            # 避免与原有逻辑重复（按 capability 去重）
            existing_types = {g.get('capability') for g in gaps if g.get('type') == 'missing_capability'}
            if sg.get('capability') not in existing_types:
                gaps.append(sg)

        # 5. 去重并评估优先级
        gaps = self._deduplicate_gaps(gaps)

        return gaps

    def _detect_from_tasks(self) -> List[Dict]:
        """从未完成任务分析技能需求"""
        gaps = []
        incomplete = self.work_analysis.get('incomplete_tasks', [])

        for task in incomplete:
            content = task.get('content', '').lower()

            if any(kw in content for kw in ['搜索', '查找', '查询', '搜索资料']):
                gaps.append({
                    'type': 'research',
                    'needed_for': task['content'][:50],
                    'priority': 'high',
                    'reason': '任务需要研究搜索能力',
                    'source': 'work_analysis',
                })

            if any(kw in content for kw in ['代码', '开发', '编程', '写代码']):
                gaps.append({
                    'type': 'code',
                    'needed_for': task['content'][:50],
                    'priority': 'high',
                    'reason': '任务需要编程开发能力',
                    'source': 'work_analysis',
                })

            if any(kw in content for kw in ['分析', '数据', '统计']):
                gaps.append({
                    'type': 'data',
                    'needed_for': task['content'][:50],
                    'priority': 'medium',
                    'reason': '任务需要数据分析能力',
                    'source': 'work_analysis',
                })

            if any(kw in content for kw in ['图片', '视频', '音频', '媒体']):
                gaps.append({
                    'type': 'media',
                    'needed_for': task['content'][:50],
                    'priority': 'medium',
                    'reason': '任务需要媒体处理能力',
                    'source': 'work_analysis',
                })

            if any(kw in content for kw in ['部署', '服务器', '运维']):
                gaps.append({
                    'type': 'devops',
                    'needed_for': task['content'][:50],
                    'priority': 'medium',
                    'reason': '任务需要DevOps能力',
                    'source': 'work_analysis',
                })

        return gaps

    def _detect_from_activity(self) -> List[Dict]:
        """从技能活跃度分析补充需求"""
        gaps = []

        dormant_skills = [
            (name, data) for name, data in self.skill_scores.items()
            if data.get('tier') in ['🗄️', '⚰️']
        ]

        if len(dormant_skills) > 3:
            gaps.append({
                'type': 'review',
                'skill_names': [s[0] for s in dormant_skills[:3]],
                'priority': 'low',
                'reason': '多个技能长期未用，建议复习或归档',
                'source': 'work_analysis',
            })

        active_categories = self._get_active_categories()
        for category, desc in self.SKILL_CATEGORIES.items():
            if category not in active_categories and category != 'review':
                gaps.append({
                    'type': 'missing_category',
                    'category': category,
                    'category_desc': desc,
                    'priority': 'low',
                    'reason': f'缺少{category}类技能覆盖',
                    'source': 'work_analysis',
                })

        return gaps

    def _detect_from_work_type(self) -> List[Dict]:
        """从工作类型分析潜在需求"""
        gaps = []

        entries = self.work_analysis.get('total_entries', 0)
        insights = len(self.work_analysis.get('insights', []))
        decisions = len(self.work_analysis.get('decisions', []))

        if insights > 5 and decisions < 2:
            gaps.append({
                'type': 'decision_support',
                'priority': 'medium',
                'reason': '工作产生大量洞察但决策少，可能需要更好的决策框架',
                'source': 'work_analysis',
            })

        corrections = len(self.work_analysis.get('corrections', []))
        if corrections > 3:
            gaps.append({
                'type': 'error_prevention',
                'priority': 'high',
                'reason': f'今日有{corrections}次纠正，需要错误预防机制',
                'source': 'work_analysis',
            })

        return gaps

    def _get_active_categories(self) -> Set[str]:
        """获取当前活跃的技能类别"""
        active = set()
        for name, data in self.skill_scores.items():
            if data.get('tier') in ['🔥', '📈']:
                name_lower = name.lower()
                if 'code' in name_lower or 'dev' in name_lower:
                    active.add('code')
                elif 'search' in name_lower or 'web' in name_lower:
                    active.add('research')
                elif 'media' in name_lower or 'audio' in name_lower:
                    active.add('media')
                elif 'data' in name_lower or 'analysis' in name_lower:
                    active.add('data')
                elif 'deploy' in name_lower or 'server' in name_lower:
                    active.add('devops')
        return active

    def _deduplicate_gaps(self, gaps: List[Dict]) -> List[Dict]:
        """去重并评估优先级"""
        seen = set()
        result = []

        for gap in gaps:
            key = gap.get('type', '') + gap.get('category', '') + gap.get('capability', '')
            if key not in seen:
                seen.add(key)
                result.append(gap)

        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        result.sort(key=lambda x: priority_order.get(x.get('priority', x.get('urgency', 'low')), 2))

        return result

    def suggest_skill_name(self, gap_type: str) -> str:
        """根据缺口类型建议技能名称"""
        suggestions = {
            'research': 'web-research',
            'code': 'code-assistant',
            'data': 'data-analysis',
            'media': 'media-processor',
            'devops': 'devops-automation',
            'decision_support': 'decision-helper',
            'error_prevention': 'error-checker',
            'missing_capability': f'new-skill-{gap_type}',
        }
        return suggestions.get(gap_type, f'new-skill-{gap_type}')
