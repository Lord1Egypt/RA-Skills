#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Sequence, Union

PlanInput = Union[str, Dict[str, Any]]

PROGRAM_RULES = {
    'Product Seeding Program': ['seed', 'seeding', 'sample', 'gift'],
    'Paid Campaign Brief': ['paid', 'fee', 'sponsored', 'deliverable', 'whitelist'],
    'Affiliate / Commission Program': ['affiliate', 'commission', 'cps', 'rev share'],
    'Launch Squad / Ambassador Program': ['ambassador', 'always-on', 'community', 'long-term'],
    'Live Selling Collaboration': ['live', 'livestream', 'stream', 'co-host'],
}

CHANNEL_RULES = {
    'TikTok / Douyin': ['tiktok', 'douyin'],
    'Xiaohongshu': ['xiaohongshu', 'xhs', 'rednote'],
    'Instagram': ['instagram'],
    'YouTube': ['youtube'],
    'Bilibili': ['bilibili'],
    'WeChat': ['wechat'],
}

OBJECTIVE_RULES = {
    'Awareness': ['awareness', 'reach', 'visibility'],
    'Conversion': ['conversion', 'sales', 'purchase', 'affiliate'],
    'Review Seeding': ['review', 'seed', 'ugc', 'testimonial'],
    'Launch Momentum': ['launch', 'drop', 'debut'],
    'Content Library Build': ['content library', 'ugc', 'asset', 'creative'],
}

CREATOR_TYPE_RULES = {
    'UGC creators': ['ugc', 'content creator'],
    'Micro creators': ['micro', 'nano', 'small creator'],
    'Expert creators': ['expert', 'doctor', 'trainer', 'specialist', 'authority'],
    'Affiliate creators': ['affiliate', 'commission', 'deal'],
    'Live hosts': ['live', 'host', 'stream'],
}

RISK_RULES = {
    'Audience mismatch': ['wrong audience', 'misaligned', 'fit'],
    'Brief ambiguity': ['brief', 'unclear', 'vague', 'confusing'],
    'Tracking gap': ['tracking', 'attribution', 'link', 'coupon code'],
    'Disclosure / compliance risk': ['disclosure', 'compliance', 'ad label', 'policy'],
    'Slow approval cycle': ['approval', 'legal', 'review delay'],
    'Overpaying for weak proof': ['high fee', 'expensive', 'costly', 'overpay'],
}


def _normalize_input(user_input: PlanInput) -> str:
    if isinstance(user_input, dict):
        chunks: List[str] = []
        for key in ['channels', 'objective', 'creator_types', 'program', 'deliverables', 'risks', 'notes']:
            value = user_input.get(key)
            if not value:
                continue
            if isinstance(value, list):
                value = ', '.join(str(item) for item in value)
            chunks.append(f'{key}: {value}')
        return ' | '.join(chunks)
    return str(user_input or '').strip()


def _match_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    for label, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return label
    return default


def _match_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    found = [label for label, keywords in rules.items() if any(keyword in text for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class CreatorCollaborationPlanner:
    def __init__(self, user_input: PlanInput):
        self.raw = user_input
        self.text = _normalize_input(user_input)
        self.lower = self.text.lower()
        self.program_type = _match_one(self.lower, PROGRAM_RULES, 'Product Seeding Program')
        self.channels = _match_many(self.lower, CHANNEL_RULES, ['TikTok / Douyin', 'Xiaohongshu'], limit=4)
        self.objective = _match_one(self.lower, OBJECTIVE_RULES, 'Awareness')
        self.creator_mix = _match_many(self.lower, CREATOR_TYPE_RULES, ['Micro creators', 'UGC creators'], limit=4)
        self.risks = _match_many(self.lower, RISK_RULES, ['Brief ambiguity', 'Tracking gap'], limit=4)

    def _rubric_rows(self) -> List[List[str]]:
        base = {
            'UGC creators': ['UGC creators', 'Fast asset generation and social proof', 'Weak differentiation if the brief is generic'],
            'Micro creators': ['Micro creators', 'Affordable reach with stronger community trust', 'Results depend on fit and follow-through, not follower count alone'],
            'Expert creators': ['Expert creators', 'Credibility for high-consideration or trust-sensitive products', 'Require tighter fact control and usually slower approval'],
            'Affiliate creators': ['Affiliate creators', 'Performance-minded distribution with sales accountability', 'Needs cleaner tracking, incentive logic, and margin discipline'],
            'Live hosts': ['Live hosts', 'High-intent commerce moments and interactive selling', 'Operational load is higher and the brief must be much tighter'],
        }
        return [base[item] for item in self.creator_mix if item in base]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Creator Collaboration Plan')
        lines.append('')
        lines.append(f'**Program type:** {self.program_type}')
        lines.append(f'**Channels in scope:** {_join(self.channels)}')
        lines.append(f'**Primary objective:** {self.objective}')
        lines.append(f'**Creator mix:** {_join(self.creator_mix)}')
        lines.append(f'**Risk flags:** {_join(self.risks)}')
        lines.append('**Method note:** This is a heuristic collaboration plan. No live creator database, audience analytics, or attribution tool was accessed.')
        lines.append('')
        lines.append('## Collaboration Strategy Summary')
        lines.append('- Choose the collaboration model based on what the business actually needs: trust, content volume, reach, or conversion proof.')
        lines.append(f'- Because the main objective is **{self.objective.lower()}**, the creator plan should optimize for fit and message clarity before scale.')
        lines.append('- Use one operator-owned source of truth for creator status, samples, approvals, and content rights.')
        lines.append('')
        lines.append('## Creator Mix and Selection Rubric')
        lines.append('| Creator type | Best use | Main watch-out |')
        lines.append('|---|---|---|')
        for row in self._rubric_rows():
            lines.append(f'| {row[0]} | {row[1]} | {row[2]} |')
        lines.append('')
        lines.append('## Offer Structure and Brief Essentials')
        lines.append('- Define what the creator must communicate, what proof is mandatory, and what they must avoid improvising.')
        lines.append('- Keep the compensation logic simple enough that the creator can understand how value is created on both sides.')
        lines.append('- Clarify deliverables, approval rounds, usage rights, posting window, and disclosure expectations before sending samples or contracts.')
        lines.append('')
        lines.append('## Outreach and Negotiation Plan')
        lines.append('1. Build a short target list by creator fit, not by vanity reach alone.')
        lines.append('2. Send outreach with one clear hook, one product reason to care, and one simple ask.')
        lines.append('3. Qualify creators on audience fit, execution quality, speed, and willingness to follow the brief.')
        lines.append('4. Negotiate deliverables, usage rights, timing, and payment logic before the product ships or the brief goes live.')
        lines.append('')
        lines.append('## Timeline and Operating Rhythm')
        lines.append('- **Week 1:** finalize goal, shortlist creators, and lock brief essentials.')
        lines.append('- **Week 2:** outreach, negotiation, sample logistics, and disclosure prep.')
        lines.append('- **Week 3:** creator content production, review, and revision management.')
        lines.append('- **Week 4:** publishing, tracking, debrief, and next-wave decisions.')
        lines.append('')
        lines.append('## Measurement and Debrief')
        lines.append('- Track fit-to-output first: response rate, acceptance rate, content quality, and revision burden.')
        lines.append('- Then track campaign effect using the best available evidence such as code usage, click quality, saves, comments, or assisted conversions.')
        lines.append('- Capture which creator archetypes generated the strongest trust, content reusability, and commercial signal.')
        lines.append('')
        lines.append('## Risk Controls and Limits')
        lines.append('- This plan is heuristic and depends on the user-supplied audience, product, and channel context.')
        lines.append('- Legal, brand safety, disclosure, payment, and rights decisions remain human-approved.')
        lines.append('- Do not confuse creator popularity with creator fit or sales quality.')
        return "\n".join(lines)


def handle(user_input: PlanInput) -> str:
    return CreatorCollaborationPlanner(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
