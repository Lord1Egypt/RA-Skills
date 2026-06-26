#!/usr/bin/env python3
import re
import sys

DEMAND_POSITIVE = ['pain', 'portable', 'gift', 'problem', 'solution', 'pet', 'office', 'organize', 'beauty', 'skincare', 'fitness', 'travel', 'home']
SATURATED = ['galaxy projector', 'posture corrector', 'led strip', 'fidget spinner', 'waist trainer']
HIGH_RISK = ['medical', 'supplement', 'battery', 'fragile', 'glass', 'cosmetic claim', 'copyright', 'trademark', 'baby', 'liquid']
CREATIVE_FRIENDLY = ['before after', 'demo', 'portable', 'pet', 'cleaning', 'organizer', 'relief', 'projector', 'beauty']

class ProductResearchEngine:
    def __init__(self, text: str):
        self.text = text.strip()
        self.lower = self.text.lower()
        self.market = self._extract_market()
        self.price_low, self.price_high = self._extract_price_band()
        self.product = self._extract_product()

    def _extract_market(self):
        for m in ['us', 'uk', 'germany', 'de', 'canada', 'australia', '美国', '英国', '德国']:
            if m in self.lower:
                return m.upper() if len(m) <= 3 else m.title()
        return 'Generic'

    def _extract_price_band(self):
        nums = [int(n) for n in re.findall(r'\$?(\d{1,3})', self.lower)]
        if len(nums) >= 2:
            return min(nums[0], nums[1]), max(nums[0], nums[1])
        if len(nums) == 1:
            return nums[0], nums[0]
        return 25, 60

    def _extract_product(self):
        words = re.split(r'[,\n]', self.text)
        return words[0][:80] if words else self.text[:80]

    def score_demand(self):
        score = 70
        if any(k in self.lower for k in DEMAND_POSITIVE):
            score += 10
        if 'seasonal' in self.lower or 'holiday' in self.lower:
            score -= 10
        return max(20, min(score, 95))

    def score_competition(self):
        score = 55
        if any(k in self.lower for k in SATURATED):
            score = 80
        if 'niche' in self.lower or 'bundle' in self.lower:
            score -= 10
        return max(10, min(score, 95))

    def score_margin(self):
        low, high = self.price_low, self.price_high
        midpoint = (low + high) / 2
        if midpoint >= 35:
            return 78
        if midpoint >= 20:
            return 65
        return 45

    def score_creative_fit(self):
        score = 60
        if any(k in self.lower for k in CREATIVE_FRIENDLY):
            score += 15
        if 'demo' in self.lower or 'ugc' in self.lower:
            score += 10
        return max(20, min(score, 95))

    def score_risk(self):
        score = 30
        if any(k in self.lower for k in HIGH_RISK):
            score += 35
        if 'size' in self.lower or 'fragile' in self.lower:
            score += 10
        return max(5, min(score, 95))

    def recommendation(self):
        demand = self.score_demand()
        comp = self.score_competition()
        margin = self.score_margin()
        creative = self.score_creative_fit()
        risk = self.score_risk()
        viability = round((demand + (100-comp) + margin + creative + (100-risk)) / 5)
        if viability >= 72 and risk <= 45:
            decision = 'Go'
        elif viability >= 55:
            decision = 'Test'
        else:
            decision = 'Reject'
        return viability, decision

    def render(self):
        demand = self.score_demand()
        comp = self.score_competition()
        margin = self.score_margin()
        creative = self.score_creative_fit()
        risk = self.score_risk()
        viability, decision = self.recommendation()
        notes = [
            'Validate unit economics with real supplier quotes before launch.',
            'Use 3-5 ad angles before rejecting a product after one creative attempt.',
            'Check compliance and claim language before publishing ads.',
        ]
        why_win = 'Clear problem-solution framing and easy-to-demo content can improve test efficiency.'
        why_fail = 'If the category is saturated or claims are hard to support, CAC and refund risk can rise quickly.'
        lines = [
            '# Dropshipping Product Research Memo', '',
            f'**Candidate:** {self.product}',
            f'**Target market:** {self.market}',
            '**Method note:** Heuristic scoring only. No real-time marketplace or ad data was accessed.', '',
            '## Viability Score',
            f'- Overall viability: **{viability}/100**',
            f'- Recommendation: **{decision}**', '',
            '## Scored Analysis',
            f'- Demand potential: **{demand}/100**',
            f'- Competition saturation: **{comp}/100** (higher = more crowded)',
            f'- Margin potential: **{margin}/100**',
            f'- Creative angle potential: **{creative}/100**',
            f'- Logistics / compliance risk: **{risk}/100** (higher = riskier)', '',
            '## Research Memo',
            f'- Why it may win: {why_win}',
            f'- Why it may fail: {why_fail}',
            '- Ideal angle: Focus on an obvious use-case, visual proof, and one memorable pain point.', '',
            '## Go / Test / Reject Rationale',
            f'- Decision summary: {decision} because viability is {viability}/100 with risk at {risk}/100.',
            f'- Competition note: {"Highly saturated, differentiation needed." if comp >= 75 else "Competitive but still testable with angle discipline."}',
            f'- Margin note: {"Healthy enough for paid testing." if margin >= 65 else "Margin looks thin, watch CAC carefully."}', '',
            '## Risk & Execution Notes'
        ]
        for n in notes:
            lines.append(f'- {n}')
        lines += ['', '## Next Steps', '1. Validate supplier cost, shipping time, and return risk.', '2. Prepare 3 ad hooks and 1 landing-page angle.', '3. Run a low-budget test before scaling.']
        return '\n'.join(lines)

def handle(user_input: str) -> str:
    return ProductResearchEngine(user_input).render()

if __name__ == '__main__':
    print(handle(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()))
