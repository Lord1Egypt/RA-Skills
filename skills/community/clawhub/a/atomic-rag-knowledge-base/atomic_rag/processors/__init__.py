"""
领域专用处理器

针对数学、物理、化学、医学等领域的特殊处理逻辑。
"""

import re
from typing import Dict, List, Any


class BaseProcessor:
    """基础处理器"""
    
    def process(self, text: str) -> Dict:
        """处理文本，返回结构化数据"""
        return {
            "steps": self._extract_steps(text),
            "key_points": self._extract_key_points(text),
            "common_mistakes": self._extract_common_mistakes(text),
            "verification": self._extract_verification(text),
            "metadata": {}
        }
    
    def _extract_steps(self, text: str) -> List[str]:
        """提取步骤"""
        step_markers = ['第一步', '第二步', '第三步', '第四步', '第五步',
                       '1.', '2.', '3.', '4.', '5.',
                       '首先', '然后', '接着', '最后']
        
        steps = []
        for marker in step_markers:
            if marker in text:
                # 简单提取包含marker的句子
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        steps.append(s.strip())
        
        return steps[:5]  # 最多5个步骤
    
    def _extract_key_points(self, text: str) -> List[str]:
        """提取关键点"""
        key_markers = ['重点是', '关键在于', '核心是', '要注意的是', '必须掌握']
        
        points = []
        for marker in key_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        points.append(s.strip())
        
        return points[:5]
    
    def _extract_common_mistakes(self, text: str) -> List[str]:
        """提取常见错误"""
        mistake_markers = ['容易错', '常见错误', '不要', '注意', '谨防', '误区']
        
        mistakes = []
        for marker in mistake_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        mistakes.append(s.strip())
        
        return mistakes[:5]
    
    def _extract_verification(self, text: str) -> str:
        """提取验证方法"""
        verify_markers = ['检验是否', '验证方法', '如何判断', '判断标准', '掌握标准']
        
        for marker in verify_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        return s.strip()
        
        return "理解并能复述核心概念"


class GeneralProcessor(BaseProcessor):
    """通用处理器"""
    pass


class MathProcessor(BaseProcessor):
    """
    数学书籍专用处理器
    
    特殊处理：
    - 公式提取 (LaTeX)
    - 证明步骤识别
    - 定理定义标注
    """
    
    def process(self, text: str) -> Dict:
        result = super().process(text)
        
        # 添加数学特定处理
        result["metadata"].update({
            "has_formulas": self._has_formulas(text),
            "has_proof": self._has_proof(text),
            "has_theorem": self._has_theorem(text)
        })
        
        result["formulas"] = self._extract_formulas(text)
        
        return result
    
    def _has_formulas(self, text: str) -> bool:
        """检测是否包含公式"""
        formula_patterns = [
            r'\$\$', r'\$[^$]+\$',  # LaTeX公式
            r'[a-zA-Z0-9]+\s*[+\-*/=]\s*[a-zA-Z0-9]+',  # 数学表达式
            r'∫', r'∑', r'√', r'∞', r'π', r'θ'  # 数学符号
        ]
        return any(re.search(p, text) for p in formula_patterns)
    
    def _has_proof(self, text: str) -> bool:
        """检测是否是证明"""
        proof_markers = ['证明', '证:', '证：', 'Q.E.D', '□', '∎']
        return any(marker in text for marker in proof_markers)
    
    def _has_theorem(self, text: str) -> bool:
        """检测是否包含定理"""
        theorem_markers = ['定理', '定义', '公理', '引理', '推论', '性质', '定律']
        return any(marker in text for marker in theorem_markers)
    
    def _extract_formulas(self, text: str) -> List[str]:
        """提取公式"""
        formulas = []
        
        # 提取LaTeX公式
        latex_formulas = re.findall(r'\$\$(.*?)\$\$|\$(.*?)\$', text)
        for f in latex_formulas:
            formulas.append(f[0] or f[1])
        
        # 提取数学表达式
        expressions = re.findall(r'[a-zA-Z0-9]+\s*[=\u2264\u2265+\-*/\u00B2\u00B3]+\s*[a-zA-Z0-9]+', text)
        formulas.extend(expressions[:5])
        
        return formulas[:10]  # 最多10个


class PhysicsProcessor(BaseProcessor):
    """
    物理书籍专用处理器
    
    特殊处理：
    - 物理模型提取
    - 公式推导过程
    - 适用条件标注
    """
    
    def process(self, text: str) -> Dict:
        result = super().process(text)
        
        result["metadata"].update({
            "has_model": self._has_model(text),
            "has_derivation": self._has_derivation(text),
            "has_conditions": self._has_conditions(text)
        })
        
        result["physics"] = {
            "models": self._extract_models(text),
            "formulas": self._extract_formulas(text),
            "conditions": self._extract_conditions(text)
        }
        
        return result
    
    def _has_model(self, text: str) -> bool:
        """检测是否包含物理模型"""
        model_markers = ['模型', '原型', '简化', '理想', '物理模型']
        return any(marker in text for marker in model_markers)
    
    def _has_derivation(self, text: str) -> bool:
        """检测是否包含推导"""
        derivation_markers = ['推导', '由', '得', '联立', '代入', '根据']
        return any(marker in text for marker in derivation_markers)
    
    def _has_conditions(self, text: str) -> bool:
        """检测是否有适用条件"""
        condition_markers = ['当', '在', '条件下', '适用于', '前提是']
        return any(marker in text for marker in condition_markers)
    
    def _extract_models(self, text: str) -> List[str]:
        """提取物理模型"""
        models = []
        model_markers = ['模型', '原型']
        
        for marker in model_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s and len(s) < 100:
                        models.append(s.strip())
        
        return models[:5]
    
    def _extract_formulas(self, text: str) -> List[str]:
        """提取物理公式"""
        return self._extract_common_formulas(text)
    
    def _extract_conditions(self, text: str) -> List[str]:
        """提取适用条件"""
        conditions = []
        condition_markers = ['当', '在', '条件下', '适用于']
        
        for marker in condition_markers:
            sentences = text.split('。')
            for s in sentences:
                if marker in s:
                    conditions.append(s.strip())
        
        return conditions[:5]
    
    def _extract_common_formulas(self, text: str) -> List[str]:
        """提取常见公式"""
        formulas = []
        # 物理常用符号
        patterns = [
            r'F\s*=\s*ma',
            r'E\s*=\s*mc\s*2',
            r'v\s*=\s*d/t',
            r'a\s*=\s*Δv/Δt',
            r'F\s*=\s*kΔx'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            formulas.extend(matches)
        
        return formulas[:10]


class ChemistryProcessor(BaseProcessor):
    """
    化学书籍专用处理器
    
    特殊处理：
    - 化学反应式识别
    - 反应机理提取
    - 条件参数记录
    """
    
    def process(self, text: str) -> Dict:
        result = super().process(text)
        
        result["metadata"].update({
            "has_reaction": self._has_reaction(text),
            "has_mechanism": self._has_mechanism(text)
        })
        
        result["chemistry"] = {
            "reactions": self._extract_reactions(text),
            "mechanism": self._extract_mechanism(text),
            "conditions": self._extract_conditions(text)
        }
        
        return result
    
    def _has_reaction(self, text: str) -> bool:
        """检测是否包含化学反应"""
        reaction_markers = ['反应', '方程式', '→', '=', '合成', '分解', '置换']
        return any(marker in text for marker in reaction_markers)
    
    def _has_mechanism(self, text: str) -> bool:
        """检测是否包含反应机理"""
        mechanism_markers = ['机理', '过程', '中间体', '过渡态']
        return any(marker in text for marker in mechanism_markers)
    
    def _extract_reactions(self, text: str) -> List[str]:
        """提取化学反应式"""
        reactions = []
        
        # 匹配化学反应式
        pattern = r'[A-Za-z0-9\u4e00-\u9fa5]+\s*(?:→|=|→|→|生成|生成)\s*[A-Za-z0-9\u4e00-\u9fa5]+'
        matches = re.findall(pattern, text)
        reactions.extend(matches)
        
        return reactions[:10]
    
    def _extract_mechanism(self, text: str) -> List[str]:
        """提取反应机理"""
        mechanism = []
        mechanism_markers = ['机理', '过程', '中间体']
        
        for marker in mechanism_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        mechanism.append(s.strip())
        
        return mechanism[:5]
    
    def _extract_conditions(self, text: str) -> List[str]:
        """提取反应条件"""
        conditions = []
        condition_markers = ['温度', '压力', '催化剂', '溶剂', '条件']
        
        for marker in condition_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        conditions.append(s.strip())
        
        return conditions[:5]


class MedicineProcessor(BaseProcessor):
    """
    医学书籍专用处理器
    
    特殊处理：
    - 诊断逻辑提取
    - 治疗方案记录
    - 鉴别诊断标注
    """
    
    def process(self, text: str) -> Dict:
        result = super().process(text)
        
        result["metadata"].update({
            "has_diagnosis": self._has_diagnosis(text),
            "has_treatment": self._has_treatment(text)
        })
        
        result["medicine"] = {
            "diagnosis": self._extract_diagnosis(text),
            "treatment": self._extract_treatment(text),
            "differential": self._extract_differential(text)
        }
        
        return result
    
    def _has_diagnosis(self, text: str) -> bool:
        """检测是否包含诊断逻辑"""
        diagnosis_markers = ['诊断', '症状', '体征', '检查', '阳性', '阴性']
        return any(marker in text for marker in diagnosis_markers)
    
    def _has_treatment(self, text: str) -> bool:
        """检测是否包含治疗方案"""
        treatment_markers = ['治疗', '用药', '药物', '手术', '疗程', '剂量']
        return any(marker in text for marker in treatment_markers)
    
    def _extract_diagnosis(self, text: str) -> Dict:
        """提取诊断逻辑"""
        diagnosis = {
            "symptoms": [],
            "exams": [],
            "diagnosis": []
        }
        
        # 提取症状
        symptom_markers = ['症状', '表现为', '出现']
        for marker in symptom_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        diagnosis["symptoms"].append(s.strip())
        
        # 提取检查
        exam_markers = ['检查', '化验', '影像', '超声', 'CT', 'MRI']
        for marker in exam_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        diagnosis["exams"].append(s.strip())
        
        # 提取诊断
        diagnosis_markers = ['诊断', '确诊为', '考虑为']
        for marker in diagnosis_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        diagnosis["diagnosis"].append(s.strip())
        
        return diagnosis
    
    def _extract_treatment(self, text: str) -> List[str]:
        """提取治疗方案"""
        treatments = []
        treatment_markers = ['治疗', '用药', '药物', '手术', '方案']
        
        for marker in treatment_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        treatments.append(s.strip())
        
        return treatments[:10]
    
    def _extract_differential(self, text: str) -> List[str]:
        """提取鉴别诊断"""
        differential = []
        differential_markers = ['鉴别诊断', '需要与', '区别', '排除']
        
        for marker in differential_markers:
            if marker in text:
                sentences = text.split('。')
                for s in sentences:
                    if marker in s:
                        differential.append(s.strip())
        
        return differential[:5]
