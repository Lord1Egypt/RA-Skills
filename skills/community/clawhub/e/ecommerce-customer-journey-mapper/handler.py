#!/usr/bin/env python3
import re
import sys
from typing import List, Dict, Tuple

STAGES = [
    'Awareness', 'Consideration', 'Product Evaluation', 'Add-to-cart',
    'Checkout', 'Post-purchase', 'Retention / Advocacy'
]

STAGE_RULES = {
    'Awareness': ['ad', 'ads', 'meta', 'tiktok', 'instagram', 'traffic', 'click', '曝光', '广告', '点击', '流量'],
    'Consideration': ['landing', 'homepage', 'message', 'messaging', 'faq', 'review', '疑虑', '页面', '文案', '评论'],
    'Product Evaluation': ['product page', 'ingredient', 'comparison', 'proof', '评价', '产品页', '成分', '对比', '证明'],
    'Add-to-cart': ['cart', '加购', 'shipping', '运费', 'bundle', '优惠'],
    'Checkout': ['checkout', 'payment', '结账', '支付', 'address', 'tax'],
    'Post-purchase': ['email', 'onboarding', 'delivery', 'support', '售后', '物流', '开箱', '使用指导'],
    'Retention / Advocacy': ['repeat', 'retention', 'loyalty', 'referral', '复购', '留存', '会员', '推荐']
}

FRICTION_LIBRARY = {
    'Awareness': ['Message promise is vague or too broad', 'Traffic source intent may not match landing-page promise'],
    'Consideration': ['Key objections are not answered early enough', 'Trust proof is weak or scattered'],
    'Product Evaluation': ['Product detail is insufficient for confident decision-making', 'Evidence does not fully support the promise'],
    'Add-to-cart': ['Price/value framing may be unclear', 'Shipping or bundle incentives are not obvious'],
    'Checkout': ['Late surprise costs create friction', 'Checkout flow may feel high-effort or low-trust'],
    'Post-purchase': ['Onboarding and expectation-setting are weak', 'Support guidance is reactive instead of proactive'],
    'Retention / Advocacy': ['No clear repeat-purchase trigger', 'Little post-purchase community or referral motivation']
}

RECOMMENDATIONS = {
    'Awareness': ['Clarify primary value proposition in ads and above-the-fold copy', 'Align channel promise with landing-page proof'],
    'Consideration': ['Move FAQ and objection handling higher on the page', 'Add social proof and category-specific reassurance blocks'],
    'Product Evaluation': ['Improve comparison, ingredient/spec, and results framing', 'Add product-use context and expected-outcome guidance'],
    'Add-to-cart': ['Test bundle framing and low-friction incentives', 'Surface shipping thresholds and return policy earlier'],
    'Checkout': ['Reduce surprise fees and simplify field requirements', 'Increase visible trust signals around payment and shipping'],
    'Post-purchase': ['Add onboarding emails and usage tips', 'Create a support macro for the top 3 confusion points'],
    'Retention / Advocacy': ['Create a reorder or replenishment trigger', 'Add referral, review, or UGC follow-up flow']
}

class JourneyAnalyzer:
    def __init__(self, text: str):
        self.text = text.strip()
        self.lower = self.text.lower()
        self.mode = 'deep' if any(k in self.lower for k in ['deep', 'audit', 'full', '完整', '深度']) else 'quick'
        self.goal = self._detect_goal()
        self.matched = self._map_stages()

    def _detect_goal(self) -> str:
        goal_map = {
            'retention': ['retention', 'repeat', '复购', '留存'],
            'checkout': ['checkout', 'payment', '结账', '支付'],
            'dropoff': ['drop', 'drop-off', 'conversion', '转化', '流失'],
            'messaging': ['message', 'messaging', '文案', '信息一致'],
        }
        for goal, keys in goal_map.items():
            if any(k in self.lower for k in keys):
                return goal
        return 'journey-audit'

    def _map_stages(self) -> Dict[str, List[str]]:
        matched = {}
        for stage, keys in STAGE_RULES.items():
            hits = [k for k in keys if k in self.lower]
            matched[stage] = hits
        return matched

    def _evidence_summary(self, stage: str) -> str:
        hits = self.matched.get(stage, [])
        if hits:
            return 'Signals found: ' + ', '.join(hits[:4])
        return 'No direct signals found, using heuristic baseline from common e-commerce patterns.'

    def _priority(self, stage: str) -> str:
        if stage in ('Checkout', 'Add-to-cart', 'Product Evaluation'):
            return 'High'
        if stage in ('Consideration', 'Post-purchase'):
            return 'Medium'
        return 'Medium-Low'

    def render(self) -> str:
        lines = []
        lines.append('# E-commerce Customer Journey Map')
        lines.append('')
        lines.append(f'**Mode:** {self.mode.title()}')
        lines.append(f'**Primary objective:** {self.goal}')
        lines.append('**Method note:** This is a heuristic, template-based analysis. No real API or analytics data was accessed.')
        lines.append('')
        lines.append('## Executive Summary')
        lines.append('- This analysis focuses on aligning promise, proof, checkout clarity, and post-purchase continuity.')
        lines.append('- The report prioritizes stages where friction most often suppresses conversion or repeat purchase.')
        lines.append('')
        lines.append('## Journey Stage Map')
        for stage in STAGES:
            lines.append(f'### {stage}')
            lines.append(f'- Evidence: {self._evidence_summary(stage)}')
            lines.append(f'- Likely friction: {FRICTION_LIBRARY[stage][0]}')
            lines.append(f'- User emotion hypothesis: {"uncertain / skeptical" if stage in ("Consideration", "Product Evaluation", "Checkout") else "curious / evaluating"}')
            lines.append(f'- Priority: {self._priority(stage)}')
            lines.append('')
        lines.append('## Friction Point Report')
        for stage in STAGES:
            lines.append(f'- **{stage}**: {FRICTION_LIBRARY[stage][0]}; {FRICTION_LIBRARY[stage][1]}')
        lines.append('')
        lines.append('## Opportunity Matrix')
        lines.append('| Stage | Impact | Effort | Suggested move |')
        lines.append('|---|---|---|---|')
        for stage in ['Consideration', 'Product Evaluation', 'Checkout', 'Post-purchase']:
            lines.append(f'| {stage} | High | Medium | {RECOMMENDATIONS[stage][0]} |')
        lines.append('')
        lines.append('## Prioritized Action Brief')
        top = ['Consideration', 'Product Evaluation', 'Checkout'] if self.goal != 'retention' else ['Post-purchase', 'Retention / Advocacy', 'Product Evaluation']
        for i, stage in enumerate(top, 1):
            lines.append(f'{i}. **{stage}**: {RECOMMENDATIONS[stage][0]}')
            lines.append(f'   - Why now: {FRICTION_LIBRARY[stage][0]}')
            lines.append(f'   - Expected effect: Reduce uncertainty and increase stage progression')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return JourneyAnalyzer(user_input).render()

if __name__ == '__main__':
    print(handle(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()))
