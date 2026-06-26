#!/usr/bin/env python3
"""
Drug Safety Review System with Free Trial & Demo Mode
Comprehensive medication safety analysis with interaction detection,
contraindication screening, allergy checks, and dosing optimization.

Version: 1.1.0
"""

import json
from functools import lru_cache
import sys
import argparse
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════
# Configuration / 配置
# ═══════════════════════════════════════════════════
BILLING_URL = 'https://skillpay.me/api/v1/billing'
API_KEY = os.environ.get('SKILLPAY_API_KEY', '')
SKILL_ID = os.environ.get('SKILLPAY_SKILL_ID', '')
VERSION = "1.1.0"

# ═══════════════════════════════════════════════════
# Localization / 本地化
# ═══════════════════════════════════════════════════
MESSAGES = {
    'zh': {
        'error_user_id_required': '错误：需要提供用户ID',
        'error_payment_failed': '错误：支付失败或余额不足',
        'error_billing_config': '错误：缺少计费配置。请设置 SKILLPAY_API_KEY 和 SKILLPAY_SKILL_ID',
        'demo_mode_active': '演示模式：无需API密钥，返回模拟药物安全数据',
        'trial_mode_active': '免费试用模式：剩余 {} 次调用',
        'processing': '正在进行药物安全审查...',
        'critical_alert': '警告：发现严重药物安全问题！',
        'drug_not_found': '未找到药物信息: {}',
    },
    'en': {
        'error_user_id_required': 'Error: User ID is required',
        'error_payment_failed': 'Error: Payment failed or insufficient balance',
        'error_billing_config': 'Error: Billing configuration missing',
        'demo_mode_active': 'Demo mode: No API key needed, returning simulated drug safety data',
        'trial_mode_active': 'Trial mode: {} calls remaining',
        'processing': 'Performing drug safety review...',
        'critical_alert': 'Warning: Critical drug safety issues detected!',
        'drug_not_found': 'Drug information not found: {}',
    }
}

# ═══════════════════════════════════════════════════
# Free Trial Manager / 免费试用管理
# ═══════════════════════════════════════════════════
class TrialManager:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.trial_dir = os.path.expanduser("~/.openclaw/skill_trial")
        self.trial_file = os.path.join(self.trial_dir, f"{skill_name}.json")
        self.max_free_calls = 10
        os.makedirs(self.trial_dir, exist_ok=True)
    
    def _load_trial_data(self) -> Dict[str, Any]:
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_trial_data(self, data: Dict[str, Any]):
        try:
            with open(self.trial_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Could not save trial data: {e}", file=sys.stderr)
    
    def get_trial_remaining(self, user_id: str) -> int:
        if not user_id:
            return 0
        data = self._load_trial_data()
        user_data = data.get(user_id, {})
        used_calls = user_data.get('used_calls', 0)
        return max(0, self.max_free_calls - used_calls)
    
    def use_trial(self, user_id: str) -> bool:
        if not user_id:
            return False
        data = self._load_trial_data()
        if user_id not in data:
            data[user_id] = {'used_calls': 0, 'first_use': datetime.now().isoformat()}
        data[user_id]['used_calls'] += 1
        data[user_id]['last_use'] = datetime.now().isoformat()
        self._save_trial_data(data)
        return True

# ═══════════════════════════════════════════════════
# SkillPay Billing / 计费系统
# ═══════════════════════════════════════════════════
class SkillPayBilling:
    def __init__(self, api_key: str = API_KEY, skill_id: str = SKILL_ID):
        self.api_key = api_key
        self.skill_id = skill_id
        self.headers = {'X-API-Key': api_key, 'Content-Type': 'application/json'}
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        url = f"{BILLING_URL}{endpoint}"
        try:
            req = urllib.request.Request(
                url, data=json.dumps(data).encode('utf-8') if data else None,
                headers=self.headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f'HTTP {e.code}: {e.reason}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def charge_user(self, user_id: str) -> Dict[str, Any]:
        result = self._make_request('/charge', method='POST', data={
            'user_id': user_id, 'skill_id': self.skill_id, 'amount': 0,
        })
        if result.get('success'):
            return {'ok': True, 'balance': result.get('balance', 0)}
        else:
            return {'ok': False, 'balance': result.get('balance', 0), 
                   'payment_url': result.get('payment_url')}

# ═══════════════════════════════════════════════════
# Drug Database / 药物数据库
# ═══════════════════════════════════════════════════
class DrugDatabase:
    """内置药物数据库查询"""
    
    DRUG_INFO = {
        'warfarin': {
            'name': '华法林 (Warfarin)',
            'category': '抗凝药 (Anticoagulant)',
            'indications': ['房颤', '深静脉血栓', '肺栓塞'],
            'common_doses': ['2.5mg', '5mg'],
            'major_interactions': ['aspirin', 'amoxicillin', 'metronidazole'],
            'contraindications': ['出血', '妊娠', '近期手术'],
            'monitoring': ['INR', '出血征象'],
        },
        'metformin': {
            'name': '二甲双胍 (Metformin)',
            'category': '降糖药 (Antidiabetic)',
            'indications': ['2型糖尿病'],
            'common_doses': ['500mg', '850mg', '1000mg'],
            'major_interactions': ['contrast', 'furosemide'],
            'contraindications': ['严重肾功能不全', '酸中毒'],
            'monitoring': ['肾功能', '血糖'],
        },
        'amoxicillin': {
            'name': '阿莫西林 (Amoxicillin)',
            'category': '抗生素 (Antibiotic)',
            'indications': ['细菌感染'],
            'common_doses': ['250mg', '500mg'],
            'major_interactions': ['warfarin', 'allopurinol'],
            'contraindications': ['青霉素过敏'],
            'monitoring': ['过敏反应'],
        },
        'lisinopril': {
            'name': '赖诺普利 (Lisinopril)',
            'category': '降压药 (ACE Inhibitor)',
            'indications': ['高血压', '心衰'],
            'common_doses': ['5mg', '10mg', '20mg'],
            'major_interactions': ['spironolactone', 'nsaids'],
            'contraindications': ['妊娠', '双侧肾动脉狭窄'],
            'monitoring': ['血压', '肾功能', '血钾'],
        },
        'simvastatin': {
            'name': '辛伐他汀 (Simvastatin)',
            'category': '降脂药 (Statin)',
            'indications': ['高胆固醇血症'],
            'common_doses': ['10mg', '20mg', '40mg'],
            'major_interactions': ['clarithromycin', 'itraconazole', 'gemfibrozil'],
            'contraindications': ['活动性肝病', '妊娠'],
            'monitoring': ['肝功能', '肌酸激酶'],
        },
        'aspirin': {
            'name': '阿司匹林 (Aspirin)',
            'category': '抗血小板药 (Antiplatelet)',
            'indications': ['心血管疾病预防', '疼痛', '发热'],
            'common_doses': ['75mg', '100mg', '300mg'],
            'major_interactions': ['warfarin', 'nsaids'],
            'contraindications': ['出血', '阿司匹林哮喘'],
            'monitoring': ['出血征象', '胃肠道症状'],
        },
    }
    
    @classmethod
    def search_drug(cls, query: str) -> Optional[Dict[str, Any]]:
        """搜索药物信息"""
        query_lower = query.lower()
        for key, info in cls.DRUG_INFO.items():
            if query_lower in key or query_lower in info['name'].lower():
                return {'key': key, **info}
        return None
    
    @classmethod
    def get_all_drugs(cls) -> List[str]:
        """获取所有药物列表"""
        return list(cls.DRUG_INFO.keys())

# ═══════════════════════════════════════════════════
# Demo Data Generator / 演示数据生成器
# ═══════════════════════════════════════════════════
class DemoDataGenerator:
    @staticmethod
    def generate_demo_review() -> Dict[str, Any]:
        return {
            'review_id': f'SAFETY_DEMO_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True,
            'safety_status': 'requires_intervention',
            'risk_score': {
                'score': 15,
                'level': 'high',
                'safety_status': 'requires_intervention'
            },
            'medication_count': 3,
            'alert_count': 2,
            'alerts': [
                {
                    'alert_id': 'DDI-WAR-AMO',
                    'severity': 'major',
                    'category': 'drug_drug_interaction',
                    'title': '华法林 - 阿莫西林 相互作用',
                    'description': '阿莫西林可能通过减少产维生素K的肠道菌群而增强抗凝效果',
                    'recommendation': '密切监测INR。考虑使用多西环素等替代抗生素。',
                    'monitoring': ['INR', '出血征象']
                },
                {
                    'alert_id': 'ALLERGY-AMO',
                    'severity': 'critical',
                    'category': 'allergy',
                    'title': '阿莫西林 - 已知过敏',
                    'description': '患者有青霉素过敏史，过敏反应为过敏性休克',
                    'recommendation': '避免使用阿莫西林。使用替代抗生素。',
                    'monitoring': ['过敏反应征象']
                }
            ],
            'recommendations': [
                {
                    'type': 'alternative_therapy',
                    'for_alert': 'ALLERGY-AMO',
                    'alternatives': [
                        {'drug': '多西环素', 'reasoning': '无显著华法林相互作用', 'formulary_status': 'available'},
                        {'drug': '阿奇霉素', 'reasoning': '与华法林相互作用最小', 'formulary_status': 'available'}
                    ]
                }
            ],
            'drug_summary': [
                {'drug': '华法林', 'dose': '5mg', 'frequency': '每日一次'},
                {'drug': '阿莫西林', 'dose': '500mg', 'frequency': '每8小时一次', 'alert': '过敏风险'},
                {'drug': '二甲双胍', 'dose': '850mg', 'frequency': '每日两次'},
            ],
            'disclaimer': '这是演示数据，仅供测试使用。实际用药决策请咨询专业医生或药师。'
        }

# ═══════════════════════════════════════════════════
# Drug Safety Reviewer / 药物安全审查器
# ═══════════════════════════════════════════════════
class DrugSafetyReviewer:
    DRUG_INTERACTIONS = {
        ('warfarin', 'amoxicillin'): {
            'severity': 'major',
            'mechanism': '阿莫西林可能通过减少产维生素K的肠道菌群而增强抗凝效果',
            'recommendation': '密切监测INR。考虑使用多西环素等替代抗生素。',
            'monitoring': ['INR', '出血征象']
        },
        ('warfarin', 'aspirin'): {
            'severity': 'major',
            'mechanism': '抗血小板作用叠加增加出血风险',
            'recommendation': '如可能避免联用。如必要，使用最低有效阿司匹林剂量。',
            'monitoring': ['INR', '出血征象', '胃肠道症状']
        },
        ('metformin', 'contrast'): {
            'severity': 'major',
            'mechanism': '碘造影剂增加乳酸酸中毒风险',
            'recommendation': '造影前48小时及后48小时停用二甲双胍。',
            'monitoring': ['肾功能', '乳酸水平']
        },
        ('lisinopril', 'spironolactone'): {
            'severity': 'major',
            'mechanism': '高钾血症风险增加',
            'recommendation': '密切监测血钾。考虑替代降压药。',
            'monitoring': ['血钾', '肾功能']
        },
        ('simvastatin', 'clarithromycin'): {
            'severity': 'major',
            'mechanism': 'CYP3A4抑制增加他汀血药浓度，横纹肌溶解风险',
            'recommendation': '避免联用。使用普伐他汀或瑞舒伐他汀替代。',
            'monitoring': ['CK水平', '肌肉症状']
        },
    }
    
    CONTRAINDICATIONS = {
        'metformin': {'conditions': ['严重肾功能不全', '酸中毒', '严重感染'], 'reason': '乳酸酸中毒风险'},
        'warfarin': {'conditions': ['活动性出血', '妊娠', '出血性卒中'], 'reason': '出血风险高'},
        'ace_inhibitors': {'conditions': ['双侧肾动脉狭窄', '血管性水肿病史'], 'reason': '急性肾衰竭或血管性水肿风险'},
        'beta_blockers': {'conditions': ['严重哮喘', '心脏传导阻滞', '心源性休克'], 'reason': '支气管痉挛或血流动力学不稳定'},
        'nsaids': {'conditions': ['活动性消化性溃疡', '严重心衰', '妊娠晚期'], 'reason': '出血、液体潴留或胎儿危害风险'},
    }
    
    ALLERGY_CROSS_REACTIVITY = {
        'penicillin': ['amoxicillin', 'ampicillin', 'piperacillin', 'cephalosporins'],
        'sulfa': ['sulfamethoxazole', 'furosemide', 'hydrochlorothiazide'],
        'cephalosporin': ['penicillin'],
    }
    
    RENAL_DOSING = {
        'metformin': {'egfr_cutoff': 30, 'action': 'contraindicated'},
        'gabapentin': {'egfr_cutoff': 30, 'action': 'reduce_dose'},
        'levofloxacin': {'egfr_cutoff': 50, 'action': 'reduce_dose'},
        'enoxaparin': {'egfr_cutoff': 30, 'action': 'reduce_dose'},
    }
    
    def __init__(self, demo_mode: bool = False):
        self.billing = SkillPayBilling()
        self.trial = TrialManager("drug-safety-review")
        self.demo_mode = demo_mode or not API_KEY
        self.lang = 'zh'
    
    def set_language(self, lang: str):
        self.lang = lang if lang in MESSAGES else 'zh'
    
    def get_message(self, key: str, *args) -> str:
        msg = MESSAGES.get(self.lang, MESSAGES['zh']).get(key, key)
        return msg.format(*args) if args else msg
    
    def check_drug_interactions(self, medications: List[Dict]) -> List[Dict]:
        alerts = []
        drug_names = [m['drug'].lower() for m in medications]
        
        for i, drug1 in enumerate(drug_names):
            for drug2 in drug_names[i+1:]:
                interaction = self.DRUG_INTERACTIONS.get((drug1, drug2)) or \
                             self.DRUG_INTERACTIONS.get((drug2, drug1))
                
                if interaction:
                    alerts.append({
                        'alert_id': f'DDI-{drug1[:3].upper()}-{drug2[:3].upper()}',
                        'severity': interaction['severity'],
                        'category': 'drug_drug_interaction',
                        'title': f'{drug1.title()} - {drug2.title()} 相互作用',
                        'description': interaction['mechanism'],
                        'recommendation': interaction['recommendation'],
                        'monitoring': interaction['monitoring']
                    })
        
        return alerts
    
    def check_contraindications(self, medications: List[Dict], 
                                patient_conditions: List[str] = None) -> List[Dict]:
        alerts = []
        patient_conditions = patient_conditions or []
        
        for med in medications:
            drug = med['drug'].lower()
            
            if drug in self.CONTRAINDICATIONS:
                contraindication = self.CONTRAINDICATIONS[drug]
                for condition in contraindication['conditions']:
                    if condition in patient_conditions:
                        alerts.append({
                            'alert_id': f'CONTRA-{drug[:3].upper()}',
                            'severity': 'critical',
                            'category': 'contraindication',
                            'title': f'{drug.title()} 禁忌',
                            'description': f'{drug.title()} 在 {condition} 患者中禁忌',
                            'recommendation': f'原因: {contraindication["reason"]}。考虑替代治疗。',
                            'monitoring': []
                        })
        
        return alerts
    
    def check_allergies(self, medications: List[Dict], allergies: List[Dict]) -> List[Dict]:
        alerts = []
        
        for med in medications:
            drug = med['drug'].lower()
            
            for allergy in allergies:
                allergen = allergy.get('allergen', '').lower()
                reaction = allergy.get('reaction', 'unknown reaction')
                
                if allergen in drug or drug in allergen:
                    severity = 'critical' if 'anaphylaxis' in reaction.lower() or '休克' in reaction else 'major'
                    alerts.append({
                        'alert_id': f'ALLERGY-{drug[:3].upper()}',
                        'severity': severity,
                        'category': 'allergy',
                        'title': f'{drug.title()} - 已知过敏',
                        'description': f'患者有{allergen}过敏史，反应为{reaction}',
                        'recommendation': f'避免使用{drug.title()}。使用替代药物。',
                        'monitoring': ['过敏反应征象']
                    })
                
                elif allergen in self.ALLERGY_CROSS_REACTIVITY:
                    cross_drugs = self.ALLERGY_CROSS_REACTIVITY[allergen]
                    if drug in cross_drugs or any(d in drug for d in cross_drugs):
                        alerts.append({
                            'alert_id': f'CROSS-{drug[:3].upper()}',
                            'severity': 'major',
                            'category': 'cross_reactivity',
                            'title': f'可能的交叉过敏: {drug.title()}',
                            'description': f'患者对{allergen}过敏。可能与{drug}存在交叉过敏。',
                            'recommendation': f'考虑过敏测试或使用替代药物。如使用需密切监测。',
                            'monitoring': ['过敏反应征象']
                        })
        
        return alerts
    
    def check_renal_dosing(self, medications: List[Dict], renal_function: Dict) -> List[Dict]:
        alerts = []
        egfr = renal_function.get('egfr', 90)
        
        for med in medications:
            drug = med['drug'].lower()
            
            if drug in self.RENAL_DOSING:
                dosing_info = self.RENAL_DOSING[drug]
                if egfr < dosing_info['egfr_cutoff']:
                    if dosing_info['action'] == 'contraindicated':
                        alerts.append({
                            'alert_id': f'RENAL-{drug[:3].upper()}',
                            'severity': 'critical',
                            'category': 'renal_dosing',
                            'title': f'{drug.title()} 禁忌(肾功能)',
                            'description': f'eGFR {egfr} 低于阈值 ({dosing_info["egfr_cutoff"]})。药物禁忌。',
                            'recommendation': '使用不经肾脏清除的替代药物。',
                            'monitoring': ['肾功能']
                        })
                    else:
                        alerts.append({
                            'alert_id': f'RENAL-{drug[:3].upper()}',
                            'severity': 'moderate',
                            'category': 'renal_dosing',
                            'title': f'{drug.title()} 需调整剂量',
                            'description': f'eGFR {egfr} 低于阈值 ({dosing_info["egfr_cutoff"]})。需调整剂量。',
                            'recommendation': '根据肾功能减少剂量。参考剂量调整指南。',
                            'monitoring': ['肾功能', '血药浓度(如有)']
                        })
        
        return alerts
    
    def suggest_alternatives(self, problematic_drug: str) -> List[Dict]:
        alternative_map = {
            'amoxicillin': [
                {'drug': '多西环素', 'reasoning': '与华法林无显著相互作用', 'formulary_status': 'available'},
                {'drug': '阿奇霉素', 'reasoning': '与华法林相互作用最小', 'formulary_status': 'available'}
            ],
            'simvastatin': [
                {'drug': '普伐他汀', 'reasoning': '不经CYP3A4代谢', 'formulary_status': 'available'},
                {'drug': '瑞舒伐他汀', 'reasoning': 'CYP3A4代谢极少', 'formulary_status': 'available'}
            ],
            'tramadol': [
                {'drug': '对乙酰氨基酚', 'reasoning': '无血清素能效应', 'formulary_status': 'available'},
            ],
        }
        return alternative_map.get(problematic_drug.lower(), [])
    
    def calculate_risk_score(self, alerts: List[Dict]) -> Dict[str, Any]:
        severity_weights = {'critical': 10, 'major': 5, 'moderate': 2, 'minor': 1}
        total_score = sum(severity_weights.get(a['severity'], 0) for a in alerts)
        
        if total_score >= 20:
            return {'score': total_score, 'level': 'very_high', 'safety_status': 'requires_immediate_intervention'}
        elif total_score >= 10:
            return {'score': total_score, 'level': 'high', 'safety_status': 'requires_intervention'}
        elif total_score >= 5:
            return {'score': total_score, 'level': 'moderate', 'safety_status': 'caution_advised'}
        elif total_score > 0:
            return {'score': total_score, 'level': 'low', 'safety_status': 'monitoring_recommended'}
        else:
            return {'score': total_score, 'level': 'minimal', 'safety_status': 'safe'}
    
    def review(self, medications: List[Dict], allergies: List[Dict] = None,
               patient_data: Dict = None) -> Dict[str, Any]:
        if self.demo_mode:
            return DemoDataGenerator.generate_demo_review()
        
        allergies = allergies or []
        patient_data = patient_data or {}
        
        all_alerts = []
        all_alerts.extend(self.check_drug_interactions(medications))
        all_alerts.extend(self.check_contraindications(medications, patient_data.get('conditions', [])))
        all_alerts.extend(self.check_allergies(medications, allergies))
        
        renal_function = patient_data.get('renal_function', {})
        if renal_function:
            all_alerts.extend(self.check_renal_dosing(medications, renal_function))
        
        severity_order = {'critical': 0, 'major': 1, 'moderate': 2, 'minor': 3}
        all_alerts.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        risk_assessment = self.calculate_risk_score(all_alerts)
        
        recommendations = []
        for alert in all_alerts:
            if alert['severity'] in ['critical', 'major']:
                alternatives = self.suggest_alternatives(alert['title'].split()[0])
                if alternatives:
                    recommendations.append({
                        'type': 'alternative_therapy',
                        'for_alert': alert['alert_id'],
                        'alternatives': alternatives
                    })
        
        return {
            'review_id': f'SAFETY_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'safety_status': risk_assessment['safety_status'],
            'risk_score': risk_assessment,
            'medication_count': len(medications),
            'alert_count': len(all_alerts),
            'alerts': all_alerts,
            'recommendations': recommendations,
            'disclaimer': '临床决策支持工具。请与专业医生或药师核实建议。'
        }
    
    def process(self, medications: List[Dict], allergies: List[Dict] = None,
                patient_data: Dict = None, user_id: str = "") -> Dict[str, Any]:
        if self.demo_mode:
            print(self.get_message('demo_mode_active'), file=sys.stderr)
            return {
                'success': True, 'demo_mode': True, 'trial_mode': False,
                'trial_remaining': 0, 'balance': None, 'review': self.review(medications, allergies, patient_data)
            }
        
        if not user_id:
            return {'success': False, 'error': self.get_message('error_user_id_required')}
        
        trial_remaining = self.trial.get_trial_remaining(user_id)
        
        if trial_remaining > 0:
            self.trial.use_trial(user_id)
            return {
                'success': True, 'demo_mode': False, 'trial_mode': True,
                'trial_remaining': trial_remaining - 1, 'balance': None,
                'review': self.review(medications, allergies, patient_data)
            }
        
        if not self.billing.api_key or not self.billing.skill_id:
            return {'success': False, 'error': self.get_message('error_billing_config')}
        
        charge_result = self.billing.charge_user(user_id)
        
        if not charge_result.get('ok'):
            return {
                'success': False, 'demo_mode': False, 'trial_mode': False,
                'trial_remaining': 0, 'error': self.get_message('error_payment_failed'),
                'balance': charge_result.get('balance', 0),
                'paymentUrl': charge_result.get('payment_url'),
            }
        
        return {
            'success': True, 'demo_mode': False, 'trial_mode': False,
            'trial_remaining': 0, 'balance': charge_result.get('balance'),
            'review': self.review(medications, allergies, patient_data)
        }

# ═══════════════════════════════════════════════════
# Convenience Functions / 便捷函数
# ═══════════════════════════════════════════════════
def review_medications(medications: List[Dict], allergies: List[Dict] = None,
                      patient_data: Dict = None, user_id: str = "",
                      demo_mode: bool = False) -> Dict[str, Any]:
    reviewer = DrugSafetyReviewer(demo_mode)
    return reviewer.process(medications, allergies, patient_data, user_id)

def search_drug_info(drug_name: str) -> Optional[Dict[str, Any]]:
    """查询药物信息"""
    return DrugDatabase.search_drug(drug_name)

# ═══════════════════════════════════════════════════
# Main Entry Point / 主入口
# ═══════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description='Drug Safety Review v1.1.0 - 药物安全审查系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  # 演示模式
  python safety_review.py --demo
  
  # 药物安全审查
  python safety_review.py -m '[{"drug":"warfarin","dose":"5mg"}]' \\
    -a '[{"allergen":"penicillin","reaction":"皮疹"}]' -u "user_123"
  
  # 查询药物信息
  python safety_review.py --search "metformin"
  
  # 列出所有药物
  python safety_review.py --list-drugs
        """)
    
    parser.add_argument('--medications', '-m', help='药物JSON数组 / Medications JSON')
    parser.add_argument('--allergies', '-a', default='[]', help='过敏史JSON / Allergies JSON')
    parser.add_argument('--patient', '-p', default='{}', help='患者数据JSON / Patient data JSON')
    parser.add_argument('--user-id', '-u', help='用户ID / User ID')
    parser.add_argument('--api-key', '-k', default=API_KEY, help='API Key')
    parser.add_argument('--skill-id', default=SKILL_ID, help='Skill ID')
    parser.add_argument('--demo', action='store_true', help='演示模式 / Demo mode')
    parser.add_argument('--language', '-l', choices=['zh', 'en'], default='zh', help='语言 / Language')
    parser.add_argument('--search', help='搜索药物 / Search drug')
    parser.add_argument('--list-drugs', action='store_true', help='列出药物 / List all drugs')
    parser.add_argument('--output', '-o', help='输出文件 / Output file')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()
    
    if args.search:
        result = DrugDatabase.search_drug(args.search)
        if result:
            print(json.dumps({'success': True, 'drug_info': result}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({'success': False, 'error': f'Drug not found: {args.search}'}, ensure_ascii=False))
        return 0
    
    if args.list_drugs:
        drugs = DrugDatabase.get_all_drugs()
        print(json.dumps({'success': True, 'drugs': drugs}, ensure_ascii=False, indent=2))
        return 0
    
    api_key = args.api_key or os.environ.get('SKILLPAY_API_KEY', '')
    skill_id = args.skill_id or os.environ.get('SKILLPAY_SKILL_ID', '')
    demo_mode = args.demo or not api_key
    
    reviewer = DrugSafetyReviewer(demo_mode)
    reviewer.set_language(args.language)
    
    if args.demo or args.medications:
        try:
            medications = json.loads(args.medications) if args.medications else []
            allergies = json.loads(args.allergies)
            patient_data = json.loads(args.patient)
        except json.JSONDecodeError as e:
            print(json.dumps({'success': False, 'error': f'Invalid JSON: {str(e)}'}, ensure_ascii=False))
            return 1
        
        result = reviewer.process(medications, allergies, patient_data, args.user_id)
    else:
        parser.print_help()
        return 1
    
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Result saved to: {args.output}")
    else:
        print(output_json)
    
    return 0 if result.get('success') else 1

if __name__ == '__main__':
    sys.exit(main())
