"""
AI含量检测器 - 核心检测引擎
基于PRD 3.1.2章节的多维度检测特征体系实现
"""

import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class AIContentLevel(Enum):
    """AI含量等级定义 (0-10级)"""
    LEVEL_0 = 0   # 完全人工
    LEVEL_1 = 1   # 人工为主，AI轻度辅助
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4   # 人机协同
    LEVEL_5 = 5
    LEVEL_6 = 6
    LEVEL_7 = 7   # AI为主
    LEVEL_8 = 8
    LEVEL_9 = 9
    LEVEL_10 = 10 # 完全AI生成


@dataclass
class DetectionResult:
    """检测结果数据结构"""
    level: int                    # AI含量等级 0-10
    score: float                  # AI参与度综合得分 0-100
    confidence: float             # 置信度
    dimension_scores: Dict[str, float]  # 各维度得分
    description: str              # 等级说明
    warning: str                  # 中立提示语
    processing_time: float        # 处理耗时


class AIFingerprintDetector:
    """
    大模型生成指纹特征检测 (权重35%)
    检测文本是否匹配主流大模型的生成指纹
    """
    
    # 大模型特有句式偏好/套话模板
    AI_PATTERNS = {
        'gpt': [
            r'(?:综上所述|总而言之|总的来说|一言以蔽之)',
            r'(?:值得注意的是|需要指出的是|值得一提的是)',
            r'(?:首先.*其次.*(?:最后|总之))',
            r'(?:让我们.*(?:探讨|分析|了解))',
            r'(?:在.*(?:背景| context|情况)下)',
            r'(?:从.*(?:角度|层面|方面)来看)',
        ],
        'claude': [
            r'(?:I\'m happy to|I\'d be glad to)',
            r'(?:Here\'s|Here is)',
            r'(?:Based on|According to)',
        ],
        'wenxin': [
            r'(?:百度|文心一言|文心大模型)',
            r'(?:作为.*(?:AI|人工智能|助手))',
            r'(?:很高兴为你|很乐意|让我来)',
        ],
        'doubao': [
            r'(?:豆包|字节跳动)',
            r'(?:我来.*(?:帮你|为你))',
            r'(?:关于.*(?:问题|话题))',
        ]
    }
    
    # AI回避话术特征
    AVOIDANCE_PATTERNS = [
        r'(?:作为.*(?:AI|人工智能).*(?:无法|不能|不会))',
        r'(?:我的.*(?:能力|知识|数据).*有限)',
        r'(?:建议.*(?:参考|咨询|查阅).*(?:专业|权威))',
        r'(?:无法提供.*(?:具体|详细|准确).*(?:信息|数据))',
    ]
    
    # 过度完美的逻辑衔接词
    PERFECT_TRANSITIONS = [
        '此外', '另外', '同时', '并且', '更重要的是',
        '综上所述', '因此', '由此可知', '由此可见',
        'firstly', 'secondly', 'thirdly', 'finally',
        'moreover', 'furthermore', 'in addition', 'consequently'
    ]
    
    def __init__(self):
        self.fingerprint_db = self._load_fingerprint_db()
    
    def _load_fingerprint_db(self) -> Dict:
        """加载生成指纹库"""
        # 实际项目中从文件加载
        return {
            'models': ['gpt-4', 'gpt-3.5', 'claude', 'wenxin', 'doubao'],
            'version_features': {}
        }
    
    def detect(self, text: str) -> Dict:
        """
        执行指纹特征检测
        返回: {'score': float, 'model_trace': str, 'details': dict}
        """
        text_lower = text.lower()
        
        # 1. 生成指纹匹配
        fingerprint_score = self._match_fingerprint(text)
        
        # 2. 生成溯源
        model_trace = self._trace_generation_source(text)
        
        # 3. 生成模式检测
        pattern_score = self._detect_generation_pattern(text)
        
        # 4. 回避话术检测
        avoidance_score = self._detect_avoidance(text)
        
        # 综合计算
        combined_score = (
            fingerprint_score * 0.4 +
            pattern_score * 0.35 +
            avoidance_score * 0.25
        )
        
        return {
            'score': min(100, combined_score),
            'model_trace': model_trace,
            'details': {
                'fingerprint_match': fingerprint_score,
                'pattern_score': pattern_score,
                'avoidance_score': avoidance_score
            }
        }
    
    def _match_fingerprint(self, text: str) -> float:
        """匹配大模型生成指纹"""
        score = 0
        total_patterns = 0
        matched_patterns = 0
        
        for model, patterns in self.AI_PATTERNS.items():
            for pattern in patterns:
                total_patterns += 1
                if re.search(pattern, text, re.IGNORECASE):
                    matched_patterns += 1
                    score += 15  # 每个匹配增加15分
        
        # 归一化到0-100
        if total_patterns > 0:
            base_score = (matched_patterns / total_patterns) * 100
        else:
            base_score = 0
        
        return min(100, base_score + score)
    
    def _trace_generation_source(self, text: str) -> str:
        """生成溯源 - 判断可能的生成模型"""
        scores = {}
        
        for model, patterns in self.AI_PATTERNS.items():
            match_count = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
            scores[model] = match_count / len(patterns) if patterns else 0
        
        # 返回最可能的模型
        if scores:
            best_model = max(scores, key=scores.get)
            return best_model if scores[best_model] > 0.3 else 'unknown'
        return 'unknown'
    
    def _detect_generation_pattern(self, text: str) -> float:
        """检测AI生成模式"""
        score = 0
        
        # 检测过度完美的逻辑衔接
        transition_count = sum(1 for t in self.PERFECT_TRANSITIONS 
                              if t.lower() in text.lower())
        if transition_count > 3:
            score += 30
        
        # 检测固定开篇模板
        opening_patterns = [
            r'^(?:你好|您好|亲爱的).*[,.，。]',
            r'^(?:关于|针对|对于).*[,，。]',
            r'^(?:在.*(?:今天|当前|目前))',
        ]
        for pattern in opening_patterns:
            if re.search(pattern, text):
                score += 20
        
        # 检测结尾套话
        ending_patterns = [
            r'(?:希望|祝).*(?:愉快|顺利|成功|有帮助).*!*$',
            r'(?:如果|若).*(?:问题|疑问|需要).*(?:联系|帮助)',
            r'(?:谢谢|感谢).*(?:阅读|观看|关注)',
        ]
        for pattern in ending_patterns:
            if re.search(pattern, text):
                score += 20
        
        return min(100, score)
    
    def _detect_avoidance(self, text: str) -> float:
        """检测AI回避话术"""
        count = 0
        for pattern in self.AVOIDANCE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        
        # 每检测到一个回避话术增加25分
        return min(100, count * 25)


class PerplexityAnalyzer:
    """
    文本困惑度与生成概率特征检测 (权重25%)
    基于NLP指标Perplexity判断
    """
    
    def __init__(self):
        # 简化实现 - 实际应加载语言模型
        self.token_patterns = self._build_token_patterns()
    
    def _build_token_patterns(self) -> Dict:
        """构建Token分布模式"""
        return {
            'uniform_patterns': [
                r'[，。！？；：]',
                r'[,.!?;:]',
            ],
            'variance_patterns': [
                r'[…~～]',
                r'(?:嗯|啊|哦|呃|那个|这个)',
            ]
        }
    
    def analyze(self, text: str) -> Dict:
        """
        分析文本困惑度特征
        返回: {'score': float, 'perplexity_proxy': float, 'details': dict}
        """
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return {'score': 50, 'perplexity_proxy': 0.5, 'details': {}}
        
        # 1. 句子长度均匀度 (AI生成更均匀)
        sentence_lengths = [len(s) for s in sentences]
        length_variance = self._calculate_variance(sentence_lengths)
        uniformity_score = 100 - min(100, length_variance / 10)
        
        # 2. 标点分布均匀度
        punctuation_scores = []
        for s in sentences:
            punct_count = len(re.findall(r'[，。！？；：,.!?;:\s]', s))
            punctuation_scores.append(punct_count)
        
        punct_variance = self._calculate_variance(punctuation_scores) if len(punctuation_scores) > 1 else 0
        punct_uniformity = 100 - min(100, punct_variance * 5)
        
        # 3. 词汇多样性 (人类文本更多样)
        words = re.findall(r'\w+', text)
        unique_words = set(words)
        diversity = len(unique_words) / len(words) if words else 0
        
        # 4. 口语化波动检测
        oral_patterns = len(re.findall(r'(?:嗯|啊|哦|呃|哈哈|嘿嘿)', text))
        oral_variance = min(100, oral_patterns * 10)
        
        # 综合计算
        # AI文本特征: 均匀度高(low variance) + 口语化波动低
        ai_score = (
            uniformity_score * 0.35 +
            punct_uniformity * 0.25 +
            (1 - diversity) * 20 +  # 低多样性偏向AI
            (100 - oral_variance) * 0.2
        )
        
        return {
            'score': ai_score,
            'perplexity_proxy': ai_score / 100,
            'details': {
                'uniformity': uniformity_score,
                'punctuation_uniformity': punct_uniformity,
                'vocabulary_diversity': diversity,
                'oral_variance': oral_variance
            }
        }
    
    def _calculate_variance(self, values: List[float]) -> float:
        """计算方差"""
        if not values or len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance


class SemanticAnalyzer:
    """
    语义与逻辑结构特征检测 (权重15%)
    检测文本的逻辑规整度、模板化程度
    """
    
    def __init__(self):
        self.structure_patterns = {
            'total_subtotal': [
                r'(?:总的来说|综上所述|总而言之).*?[,，。]',
                r'(?:首先|第一).*?(?:其次|第二).*?(?:最后|第三|总之)',
            ],
            'bullet_pattern': [
                r'(?:[①②③④⑤]|[1-9]\.|[（(][1-9][)）])',
                r'(?:一、|二、|三、|四、|五、)',
            ],
            'paragraph_structure': [
                r'(?:引言|正文|结论|总结)',
                r'(?:背景|现状|问题|建议|展望)',
            ]
        }
    
    def analyze(self, text: str) -> Dict:
        """
        分析语义与逻辑结构
        返回: {'score': float, 'details': dict}
        """
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # 1. 总分总结构检测
        total_subtotal_score = self._detect_total_subtotal(text)
        
        # 2. 分点式结构检测
        bullet_score = self._detect_bullet_structure(text)
        
        # 3. 段落均匀度
        para_uniformity = self._analyze_paragraph_uniformity(paragraphs)
        
        # 4. 逻辑连贯性 (简单实现)
        coherence_score = self._analyze_coherence(text)
        
        # 5. 模板化程度
        template_score = self._detect_template(text)
        
        # 综合计算 (高规整度偏向AI)
        ai_score = (
            total_subtotal_score * 0.25 +
            bullet_score * 0.20 +
            para_uniformity * 0.20 +
            coherence_score * 0.15 +
            template_score * 0.20
        )
        
        return {
            'score': ai_score,
            'details': {
                'total_subtotal': total_subtotal_score,
                'bullet_structure': bullet_score,
                'paragraph_uniformity': para_uniformity,
                'coherence': coherence_score,
                'template': template_score
            }
        }
    
    def _detect_total_subtotal(self, text: str) -> float:
        """检测总分总结构"""
        score = 0
        for pattern in self.structure_patterns['total_subtotal']:
            if re.search(pattern, text):
                score += 30
        return min(100, score)
    
    def _detect_bullet_structure(self, text: str) -> float:
        """检测分点式结构"""
        score = 0
        for pattern in self.structure_patterns['bullet_pattern']:
            matches = re.findall(pattern, text)
            score += len(matches) * 15
        return min(100, score)
    
    def _analyze_paragraph_uniformity(self, paragraphs: List[str]) -> float:
        """分析段落均匀度"""
        if len(paragraphs) < 2:
            return 50
        
        lengths = [len(p) for p in paragraphs]
        variance = self._calculate_variance(lengths)
        
        # 低方差 = 高均匀度 = 偏向AI
        return 100 - min(100, variance / 50)
    
    def _analyze_coherence(self, text: str) -> float:
        """分析逻辑连贯性"""
        # 检测过度连贯的特征
        transition_words = [
            '因此', '所以', '于是', '从而', '进而',
            'because', 'therefore', 'thus', 'consequently'
        ]
        
        count = sum(1 for word in transition_words if word in text)
        # 过多过渡词可能表示过度连贯
        return min(100, count * 8)
    
    def _detect_template(self, text: str) -> float:
        """检测模板化程度"""
        score = 0
        
        # 检测固定模板
        for pattern in self.structure_patterns['paragraph_structure']:
            if re.search(pattern, text):
                score += 20
        
        # 检测对称结构
        if re.search(r'(?:不仅.*而且|不但.*而且|既.*又)', text):
            score += 15
        
        return min(100, score)
    
    def _calculate_variance(self, values: List[float]) -> float:
        if not values or len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)


class StyleAnalyzer:
    """
    语言风格与用词特征检测 (权重15%)
    检测用词标准化程度、句式均匀度、修订痕迹
    """
    
    # 标准化书面语词汇 (AI偏好)
    STANDARD_WORDS = [
        '进行', '开展', '实施', '推进', '落实',
        '优化', '提升', '增强', '完善', '强化',
        'important', 'significant', 'crucial', 'essential'
    ]
    
    # 口语化词汇 (人类偏好)
    ORAL_WORDS = [
        '呢', '啦', '吧', '啊', '哦',
        '其实', '说实话', '老实说', '讲真',
        '有点', '挺', '蛮', '挺', '超级'
    ]
    
    # 个人化表达标记
    PERSONAL_MARKERS = [
        r'(?:我觉得|我认为|在我看来|依我看)',
        r'(?:我的经验|我的经历|我曾经)',
        r'(?:根据我|以我.*为例)',
        r'(?:个人感觉|个人看法)',
    ]
    
    # 修订痕迹标记
    REVISION_MARKERS = [
        r'(?:\(.*\))',  # 括号注释
        r'(?:【.*?】)',  # 方括号补充
        r'(?:补充.*?:)',  # 补充说明
        r'(?:注：|备注：)',  # 注释放置
    ]
    
    def analyze(self, text: str) -> Dict:
        """
        分析语言风格与用词
        返回: {'score': float, 'details': dict}
        """
        # 1. 用词标准化程度
        standard_score = self._detect_standard_words(text)
        
        # 2. 口语化程度
        oral_score = self._detect_oral_words(text)
        
        # 3. 句式均匀度
        sentence_uniformity = self._analyze_sentence_uniformity(text)
        
        # 4. 个人表达特征
        personal_score = self._detect_personal_markers(text)
        
        # 5. 修订痕迹
        revision_score = self._detect_revision_marks(text)
        
        # 6. 错别字检测 (反向指标)
        typo_score = self._detect_typos(text)
        
        # 综合计算
        # 高标准化 + 低口语化 + 高句式均匀 + 低个人特征 - 修订痕迹 - 错别字 = 偏向AI
        ai_score = (
            standard_score * 0.25 +
            (100 - oral_score) * 0.20 +
            sentence_uniformity * 0.20 +
            (100 - personal_score) * 0.15 +
            (100 - revision_score) * 0.10 +
            (100 - typo_score) * 0.10
        )
        
        return {
            'score': ai_score,
            'details': {
                'standard_words': standard_score,
                'oral_words': oral_score,
                'sentence_uniformity': sentence_uniformity,
                'personal_markers': personal_score,
                'revision_marks': revision_score,
                'typos': typo_score
            }
        }
    
    def _detect_standard_words(self, text: str) -> float:
        """检测标准化词汇使用频率"""
        count = sum(1 for word in self.STANDARD_WORDS if word in text)
        return min(100, count * 8)
    
    def _detect_oral_words(self, text: str) -> float:
        """检测口语化词汇"""
        count = sum(1 for word in self.ORAL_WORDS if word in text)
        return min(100, count * 6)
    
    def _analyze_sentence_uniformity(self, text: str) -> float:
        """分析句式均匀度"""
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 50
        
        lengths = [len(s) for s in sentences]
        variance = self._calculate_variance(lengths)
        
        # 低方差 = 高均匀度 = 偏向AI
        return 100 - min(100, variance / 5)
    
    def _detect_personal_markers(self, text: str) -> float:
        """检测个人表达标记"""
        count = 0
        for pattern in self.PERSONAL_MARKERS:
            count += len(re.findall(pattern, text))
        return min(100, count * 12)
    
    def _detect_revision_marks(self, text: str) -> float:
        """检测修订痕迹"""
        count = 0
        for pattern in self.REVISION_MARKERS:
            count += len(re.findall(pattern, text))
        return min(100, count * 15)
    
    def _detect_typos(self, text: str) -> float:
        """检测可能的错别字 (简化版)"""
        # 常见错别字模式
        typo_patterns = [
            r'(?:的|地|得)\s+(?:的|地|得)',  # 的地得混用
            r'(?:他|她|它)\s+(?:他|她|它)',  # 他她它混用
        ]
        
        count = 0
        for pattern in typo_patterns:
            count += len(re.findall(pattern, text))
        
        # 人类更容易出现错别字
        return min(100, count * 20)
    
    def _calculate_variance(self, values: List[float]) -> float:
        if not values or len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)


class HumanModificationDetector:
    """
    人工修改与参与度特征检测 (权重10%)
    反向验证维度
    """
    
    def __init__(self):
        self.human_markers = {
            'style_inconsistency': [
                r'(?:但是|不过|然而).*?(?:不过|但是)',  # 转折词混用
                r'(?:非常|十分|特别|相当).*?(?:有点|稍微)',  # 程度词矛盾
            ],
            'personal_experience': [
                r'(?:我曾经|我当初|那年|那段时间)',
                r'(?:记得|回忆|想起|那时候)',
                r'(?:亲身经历|亲眼所见|亲耳所闻)',
            ],
            'exclusive_info': [
                r'(?:内部消息|独家|知情人士|小道消息)',
                r'(?:据我所知|据我了解|据我观察)',
            ],
            'emotional_expression': [
                r'[!！]{2,}',  # 多感叹号
                r'[?？]{2,}',  # 多问號
                r'(?:…|\.\.\.){2,}',  # 省略号重复
                r'(?:哈哈|嘿嘿|呵呵|呜呜)',
            ]
        }
    
    def detect(self, text: str) -> Dict:
        """
        检测人工参与痕迹
        返回: {'score': float, 'details': dict}
        """
        # 1. 风格不一致性
        style_score = self._detect_style_inconsistency(text)
        
        # 2. 个人经验表述
        experience_score = self._detect_personal_experience(text)
        
        # 3. 专属信息
        exclusive_score = self._detect_exclusive_info(text)
        
        # 4. 情绪化表达
        emotional_score = self._detect_emotional_expression(text)
        
        # 5. 段落间风格差异 (简化版)
        para_variance = self._analyze_paragraph_style_variance(text)
        
        # 综合计算 (高人工特征 = 低AI含量)
        # 所有指标都是反向的：越高表示越像人类
        human_score = (
            style_score * 0.15 +
            experience_score * 0.30 +
            exclusive_score * 0.25 +
            emotional_score * 0.15 +
            para_variance * 0.15
        )
        
        # 转换为AI参与度分数 (反向)
        ai_score = 100 - human_score
        
        return {
            'score': ai_score,
            'details': {
                'style_inconsistency': style_score,
                'personal_experience': experience_score,
                'exclusive_info': exclusive_score,
                'emotional_expression': emotional_score,
                'paragraph_variance': para_variance
            }
        }
    
    def _detect_style_inconsistency(self, text: str) -> float:
        """检测风格不一致"""
        count = 0
        for pattern in self.human_markers['style_inconsistency']:
            count += len(re.findall(pattern, text))
        return min(100, count * 20)
    
    def _detect_personal_experience(self, text: str) -> float:
        """检测个人经验表述"""
        count = 0
        for pattern in self.human_markers['personal_experience']:
            count += len(re.findall(pattern, text))
        return min(100, count * 15)
    
    def _detect_exclusive_info(self, text: str) -> float:
        """检测专属信息"""
        count = 0
        for pattern in self.human_markers['exclusive_info']:
            count += len(re.findall(pattern, text))
        return min(100, count * 20)
    
    def _detect_emotional_expression(self, text: str) -> float:
        """检测情绪化表达"""
        count = 0
        for pattern in self.human_markers['emotional_expression']:
            count += len(re.findall(pattern, text))
        return min(100, count * 10)
    
    def _analyze_paragraph_style_variance(self, text: str) -> float:
        """分析段落间风格差异"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        if len(paragraphs) < 2:
            return 30  # 默认中等
        
        # 简单计算：检测段落间用词差异
        variances = []
        for i in range(len(paragraphs) - 1):
            p1, p2 = paragraphs[i], paragraphs[i+1]
            
            # 计算用词重叠度
            words1 = set(re.findall(r'\w+', p1))
            words2 = set(re.findall(r'\w+', p2))
            
            if words1 and words2:
                overlap = len(words1 & words2) / len(words1 | words2)
                variances.append(1 - overlap)
        
        if variances:
            avg_variance = sum(variances) / len(variances) * 100
            return min(100, avg_variance * 2)
        
        return 30


class AIDensityDetector:
    """
    AI含量检测主类
    整合所有检测维度，输出最终分级结果
    """
    
    # 权重配置 (根据PRD 3.1.2.2)
    WEIGHTS = {
        'fingerprint': 0.35,      # 大模型生成指纹特征
        'perplexity': 0.25,       # 文本困惑度与生成概率
        'semantic': 0.15,         # 语义与逻辑结构
        'style': 0.15,            # 语言风格与用词
        'human_modification': 0.10 # 人工修改与参与度
    }
    
    def __init__(self):
        self.fingerprint_detector = AIFingerprintDetector()
        self.perplexity_analyzer = PerplexityAnalyzer()
        self.semantic_analyzer = SemanticAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        self.human_detector = HumanModificationDetector()
    
    def detect(self, text: str) -> DetectionResult:
        """
        执行AI含量检测
        
        Args:
            text: 待检测文本 (10-10000字)
            
        Returns:
            DetectionResult: 检测结果
        """
        import time
        start_time = time.time()
        
        # 1. 多维度特征提取
        fingerprint_result = self.fingerprint_detector.detect(text)
        perplexity_result = self.perplexity_analyzer.analyze(text)
        semantic_result = self.semantic_analyzer.analyze(text)
        style_result = self.style_analyzer.analyze(text)
        human_result = self.human_detector.detect(text)
        
        # 2. 加权融合计算综合得分
        dimension_scores = {
            'fingerprint': fingerprint_result['score'],
            'perplexity': perplexity_result['score'],
            'semantic': semantic_result['score'],
            'style': style_result['score'],
            'human_modification': human_result['score']
        }
        
        total_score = sum(
            dimension_scores[key] * self.WEIGHTS[key]
            for key in self.WEIGHTS.keys()
        )
        
        # 3. 分级映射 (根据PRD 3.1.2.3)
        level = self._map_score_to_level(total_score)
        
        # 4. 生成描述
        description = self._get_level_description(level)
        
        processing_time = time.time() - start_time
        
        return DetectionResult(
            level=level,
            score=round(total_score, 2),
            confidence=self._calculate_confidence(dimension_scores),
            dimension_scores=dimension_scores,
            description=description,
            warning="本检测仅针对AI生成占比，不对内容的真实性、专业性、实用性做任何评价",
            processing_time=round(processing_time, 3)
        )
    
    def _map_score_to_level(self, score: float) -> int:
        """
        将综合得分映射到0-10级
        映射规则参考PRD 3.1.2.3
        """
        if score < 1:
            return 0
        elif score <= 10:
            return 1
        elif score <= 20:
            return 2
        elif score <= 30:
            return 3
        elif score <= 40:
            return 4
        elif score <= 60:
            return 5
        elif score <= 70:
            return 6
        elif score <= 80:
            return 7
        elif score <= 90:
            return 8
        elif score < 100:
            return 9
        else:
            return 10
    
    def _get_level_description(self, level: int) -> str:
        """获取等级说明"""
        descriptions = {
            0: "完全人工书写，无任何AI辅助生成、润色、修改痕迹",
            1: "人工为主，AI仅做个别错别字修正、标点调整",
            2: "人工为主，AI做简单用词润色、语句通顺度优化",
            3: "人工为主，AI做段落排版、局部语句精简，无核心内容修改",
            4: "人机协同，AI生成内容框架，人工填充全部核心观点与细节",
            5: "人机协同，AI生成初稿，人工修改占比≥50%，替换核心观点",
            6: "人机协同，AI生成核心内容，人工局部修改占比30%-50%",
            7: "AI为主，人工修改占比10%-30%",
            8: "AI为主，人工仅修改个别语句、错别字，修改占比<10%",
            9: "AI为主，人工仅做标题、标点微调，无核心内容修改",
            10: "完全AI生成，无任何人工参与"
        }
        return descriptions.get(level, "未知等级")
    
    def _calculate_confidence(self, dimension_scores: Dict[str, float]) -> float:
        """计算置信度"""
        # 基于各维度得分的一致性计算
        values = list(dimension_scores.values())
        if not values:
            return 0.5
        
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        
        # 方差越小，置信度越高
        confidence = 1 - (variance / 10000)
        return round(max(0.5, min(1.0, confidence)), 2)


# 便捷函数
def detect_ai_content(text: str) -> DetectionResult:
    """
    便捷的AI含量检测函数
    
    使用示例:
        result = detect_ai_content("这是一段测试文本...")
        print(f"AI含量等级: {result.level}")
        print(f"AI参与度得分: {result.score}")
    """
    detector = AIDensityDetector()
    return detector.detect(text)


if __name__ == '__main__':
    # 测试代码
    test_texts = [
        # 人工文本示例
        "我觉得这个方案还行吧，不过说实话，我之前也没做过类似的项目。",
        
        # AI文本示例
        "综上所述，本文从多个角度全面分析了当前形势。首先，我们需要认识到问题的复杂性；其次，要采取有效措施加以应对。",
        
        # 混合文本示例
        "作为一个AI助手，我很乐意帮助你。不过根据我的经验，这个问题其实挺复杂的，我之前遇到过类似的情况..."
    ]
    
    detector = AIDensityDetector()
    for i, text in enumerate(test_texts, 1):
        result = detector.detect(text)
        print(f"\n=== 测试文本 {i} ===")
        print(f"文本: {text[:50]}...")
        print(f"AI含量等级: {result.level}/10")
        print(f"AI参与度得分: {result.score}")
        print(f"置信度: {result.confidence}")
        print(f"说明: {result.description}")
        print(f"各维度得分: {result.dimension_scores}")
