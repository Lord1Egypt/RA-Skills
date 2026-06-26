import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from .config import config

try:
    from sentence_transformers import util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


@dataclass
class CheckResult:
    dimension: str
    is_consistent: bool
    score: float
    details: str
    issues: List[str]


class ConsistencyChecker:
    def __init__(self, vector_store=None):
        self.vector_store = vector_store
        self.embedding = getattr(vector_store, 'embedding', None)
        self.dimension_weights = {
            'character': 0.35,
            'plot': 0.30,
            'style': 0.20,
            'world': 0.15
        }

    def check_consistency(
        self,
        generated_text: str,
        anchors: Dict[str, str]
    ) -> Tuple[bool, str]:
        results = self.check_all_dimensions(generated_text, anchors)

        overall_score = sum(
            r.score * self.dimension_weights.get(r.dimension, 0.25)
            for r in results
        )

        is_consistent = overall_score >= config.consistency.threshold

        issues = []
        for r in results:
            if not r.is_consistent:
                issues.append(f"[{r.dimension}] {r.details}")

        message = f"综合评分：{overall_score:.2f}"
        if issues:
            message += f"\n发现问题：\n" + "\n".join(issues)
        else:
            message += "，各维度一致性良好。"

        return is_consistent, message

    def check_all_dimensions(
        self,
        generated_text: str,
        anchors: Dict[str, str]
    ) -> List[CheckResult]:
        results = []

        if '人设' in anchors:
            results.append(self.check_character_consistency(generated_text, anchors['人设']))

        if '核心剧情' in anchors:
            results.append(self.check_plot_consistency(generated_text, anchors['核心剧情']))

        if '文风' in anchors:
            results.append(self.check_style_consistency(generated_text, anchors['文风']))

        if '世界观' in anchors:
            results.append(self.check_world_consistency(generated_text, anchors['世界观']))

        return results

    def check_character_consistency(
        self,
        generated_text: str,
        character_anchor: str
    ) -> CheckResult:
        issues = []
        score = 1.0

        characters = self._parse_characters(character_anchor)

        for char_name, char_info in characters.items():
            if char_name in generated_text:
                age_pattern = r'(\d+)\s*岁'
                anchor_age = re.search(age_pattern, char_info)
                text_age = re.search(age_pattern, generated_text)

                if anchor_age and text_age and anchor_age.group(1) != text_age.group(1):
                    issues.append(f"角色'{char_name}'年龄不一致：设定{anchor_age.group(1)}岁，文中为{text_age.group(1)}岁")
                    score -= 0.3

                trait_keywords = ['性格', '善良', '勇敢', '聪明', '洒脱', '嫉恶如仇', '温柔', '冷酷']
                for trait in trait_keywords:
                    if trait in char_info:
                        opposite_traits = {
                            '善良': ['残忍', '恶毒'],
                            '勇敢': ['胆小', '怯懦'],
                            '温柔': ['暴躁', '凶狠'],
                            '洒脱': ['拘谨', '优柔寡断']
                        }
                        if trait in opposite_traits:
                            for opp in opposite_traits[trait]:
                                if opp in generated_text and char_name in generated_text:
                                    issues.append(f"角色'{char_name}'性格矛盾：设定{trait}，但表现出{opp}")
                                    score -= 0.2

        if self.embedding and character_anchor and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                anchor_embedding = self.embedding.embed_query(character_anchor)
                text_embedding = self.embedding.embed_query(generated_text)
                semantic_score = util.cos_sim(anchor_embedding, text_embedding).item()
                score = (score + semantic_score) / 2
            except Exception:
                pass

        score = max(0.0, min(1.0, score))

        return CheckResult(
            dimension='character',
            is_consistent=score >= 0.6,
            score=score,
            details=f"人设一致性评分：{score:.2f}",
            issues=issues
        )

    def check_plot_consistency(
        self,
        generated_text: str,
        plot_anchor: str
    ) -> CheckResult:
        issues = []
        score = 1.0

        plot_keywords = plot_anchor.split('；')

        contradiction_patterns = [
            (r'已死|死亡|牺牲', r'复活|重生|出现'),
            (r'离开|告别|分别', r'一直在|始终在'),
            (r'得到|获得|拥有', r'失去|丢失|没有'),
        ]

        for pattern1, pattern2 in contradiction_patterns:
            if re.search(pattern1, plot_anchor) and re.search(pattern2, generated_text):
                issues.append(f"剧情可能存在矛盾：'{pattern1}'与'{pattern2}'")
                score -= 0.3

        if self.embedding and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                anchor_embedding = self.embedding.embed_query(plot_anchor)
                text_embedding = self.embedding.embed_query(generated_text)
                semantic_score = util.cos_sim(anchor_embedding, text_embedding).item()
                score = (score + semantic_score) / 2
            except Exception:
                pass

        score = max(0.0, min(1.0, score))

        return CheckResult(
            dimension='plot',
            is_consistent=score >= 0.6,
            score=score,
            details=f"剧情一致性评分：{score:.2f}",
            issues=issues
        )

    def check_style_consistency(
        self,
        generated_text: str,
        style_anchor: str
    ) -> CheckResult:
        issues = []
        score = 1.0

        ancient_markers = ['之', '乎', '者', '也', '矣', '焉', '吾', '汝', '尔']
        modern_markers = ['的', '了', '着', '过', '吗', '呢', '吧', '啊']

        ancient_count = sum(generated_text.count(m) for m in ancient_markers)
        modern_count = sum(generated_text.count(m) for m in modern_markers)

        text_length = max(len(generated_text), 1)
        ancient_ratio = ancient_count / text_length
        modern_ratio = modern_count / text_length

        if '古风' in style_anchor or '武侠' in style_anchor:
            if modern_ratio > ancient_ratio * 2:
                issues.append(f"文风偏现代，与设定'{style_anchor}'不符")
                score -= 0.3
        elif '现代' in style_anchor:
            if ancient_ratio > modern_ratio * 2:
                issues.append(f"文风偏古风，与设定'{style_anchor}'不符")
                score -= 0.3

        sentence_lengths = [
            len(s) for s in re.split(r'[。！？\n]', generated_text) if s.strip()
        ]
        avg_length = sum(sentence_lengths) / max(len(sentence_lengths), 1)

        if '简洁' in style_anchor and avg_length > 50:
            issues.append(f"句子平均长度{avg_length:.1f}字，与'简洁'风格不符")
            score -= 0.2
        elif '细腻' in style_anchor and avg_length < 20:
            issues.append(f"句子平均长度{avg_length:.1f}字，与'细腻'风格不符")
            score -= 0.2

        score = max(0.0, min(1.0, score))

        return CheckResult(
            dimension='style',
            is_consistent=score >= 0.6,
            score=score,
            details=f"文风一致性评分：{score:.2f}",
            issues=issues
        )

    def check_world_consistency(
        self,
        generated_text: str,
        world_anchor: str
    ) -> CheckResult:
        issues = []
        score = 1.0

        modern_items = ['手机', '电脑', '汽车', '飞机', '网络', '电视', '冰箱']
        fantasy_items = ['飞剑', '法宝', '灵石', '仙丹', '阵法', '修为']

        if '古风' in world_anchor or '武侠' in world_anchor or '仙侠' in world_anchor:
            for item in modern_items:
                if item in generated_text:
                    issues.append(f"出现现代元素'{item}'，与世界观'{world_anchor}'冲突")
                    score -= 0.2

        if '现代' in world_anchor:
            for item in fantasy_items:
                if item in generated_text:
                    issues.append(f"出现玄幻元素'{item}'，与世界观'{world_anchor}'冲突")
                    score -= 0.2

        if self.embedding and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                anchor_embedding = self.embedding.embed_query(world_anchor)
                text_embedding = self.embedding.embed_query(generated_text)
                semantic_score = util.cos_sim(anchor_embedding, text_embedding).item()
                score = (score + semantic_score) / 2
            except Exception:
                pass

        score = max(0.0, min(1.0, score))

        return CheckResult(
            dimension='world',
            is_consistent=score >= 0.6,
            score=score,
            details=f"世界观一致性评分：{score:.2f}",
            issues=issues
        )

    def _parse_characters(self, character_anchor: str) -> Dict[str, str]:
        characters = {}
        parts = character_anchor.split('；')

        for part in parts:
            if '：' in part:
                name, info = part.split('：', 1)
                characters[name.strip()] = info.strip()
            elif ':' in part:
                name, info = part.split(':', 1)
                characters[name.strip()] = info.strip()

        return characters

    def get_detailed_report(
        self,
        generated_text: str,
        anchors: Dict[str, str]
    ) -> Dict[str, Any]:
        results = self.check_all_dimensions(generated_text, anchors)

        report = {
            'summary': {
                'overall_consistent': all(r.is_consistent for r in results),
                'total_issues': sum(len(r.issues) for r in results),
                'dimension_scores': {r.dimension: r.score for r in results}
            },
            'details': [
                {
                    'dimension': r.dimension,
                    'is_consistent': r.is_consistent,
                    'score': r.score,
                    'details': r.details,
                    'issues': r.issues
                }
                for r in results
            ],
            'recommendations': self._generate_recommendations(results)
        }

        return report

    def _generate_recommendations(self, results: List[CheckResult]) -> List[str]:
        recommendations = []

        for result in results:
            if not result.is_consistent:
                if result.dimension == 'character':
                    recommendations.append("建议检查角色设定，确保人设前后一致")
                elif result.dimension == 'plot':
                    recommendations.append("建议回顾前文剧情，避免逻辑矛盾")
                elif result.dimension == 'style':
                    recommendations.append("建议调整用词和句式，保持文风统一")
                elif result.dimension == 'world':
                    recommendations.append("建议检查世界观设定，避免时代错乱")

        return recommendations
