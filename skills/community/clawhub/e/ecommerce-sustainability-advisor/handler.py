#!/usr/bin/env python3
import sys
from typing import List

HOTSPOT_RULES = {
    'packaging': ['packaging', 'box', 'plastic', 'bubble wrap', 'oversized', 'single-use', 'mailer'],
    'logistics': ['air', 'express', 'shipping', 'split shipment', 'long distance', 'delivery'],
    'returns': ['return', 'returns', 'refund', 'exchange', 'fit issue', 'damage'],
    'claims': ['eco-friendly', 'green', 'sustainable', 'carbon neutral', 'biodegradable', 'planet-friendly'],
    'sourcing': ['supplier', 'material', 'virgin', 'recycled', 'origin', 'procurement'],
}

CLAIM_WORDS = ['eco-friendly', 'green', 'sustainable', 'carbon neutral', 'biodegradable', 'plastic-free']
EVIDENCE_WORDS = ['certified', 'verified', 'fsc', 'recycled content', '%', 'tested', 'audited']

HOTSPOT_EXPLANATIONS = {
    'packaging': 'Packaging waste is often the fastest practical win because teams can reduce material, void fill, and carton size without rebuilding the whole business.',
    'logistics': 'Shipping mode and split-fulfillment choices can quietly drive impact and cost at the same time.',
    'returns': 'Returns create duplicated transport, extra packaging, and inventory handling, so prevention is a strong sustainability lever.',
    'claims': 'Claim language can create greenwashing risk if the brand says more than it can support.',
    'sourcing': 'Material and supplier choices determine how credible long-term sustainability improvements really are.',
}


class SustainabilityAdvisor:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.hotspots = self._detect_hotspots()
        self.claim_risk = self._detect_claim_risk()

    def _detect_hotspots(self) -> List[str]:
        found = [name for name, keywords in HOTSPOT_RULES.items() if any(word in self.lower for word in keywords)]
        if not found:
            return ['packaging', 'logistics', 'claims']
        ordered = []
        for candidate in ['packaging', 'returns', 'logistics', 'claims', 'sourcing']:
            if candidate in found:
                ordered.append(candidate)
        return ordered

    def _detect_claim_risk(self) -> bool:
        has_claim = any(word in self.lower for word in CLAIM_WORDS)
        has_evidence = any(word in self.lower for word in EVIDENCE_WORDS)
        return has_claim and not has_evidence

    def _roadmap_items(self) -> List[str]:
        actions = []
        if 'packaging' in self.hotspots:
            actions.append('Pilot right-sized packaging, reduce void fill, and document one packaging spec per core SKU family.')
        if 'returns' in self.hotspots:
            actions.append('Attack avoidable returns through fit guidance, clearer expectations, and damage-prevention packaging.')
        if 'logistics' in self.hotspots:
            actions.append('Review air-heavy or split-shipment patterns and consolidate where customer promise still remains acceptable.')
        if 'claims' in self.hotspots:
            actions.append('Rewrite broad sustainability claims into narrower statements tied to specific evidence or current initiatives.')
        if 'sourcing' in self.hotspots:
            actions.append('Ask suppliers for material composition, recycled-content data, and packaging alternatives before making bigger claims.')
        return actions[:4]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# E-commerce Sustainability Action Brief')
        lines.append('')
        lines.append('**Method note:** This is a directional operational review. It is not a certified lifecycle assessment, carbon audit, or legal opinion.')
        lines.append('')
        lines.append('## Executive Summary')
        lines.append('- Focus first on the hotspots that are both materially meaningful and operationally feasible for an e-commerce team to change.')
        if self.claim_risk:
            lines.append('- Current language suggests elevated greenwashing risk because claims appear broader than the evidence provided.')
        else:
            lines.append('- Messaging risk appears manageable from the provided text, but evidence should still be checked before public claims are expanded.')
        lines.append('')
        lines.append('## Impact Hotspots')
        for hotspot in self.hotspots:
            lines.append(f'### {hotspot.title()}')
            lines.append(f'- Why it matters: {HOTSPOT_EXPLANATIONS[hotspot]}')
            priority = 'High' if hotspot in ('packaging', 'returns', 'claims') else 'Medium'
            lines.append(f'- Priority: {priority}')
            lines.append('')
        lines.append('## 90-Day Action Roadmap')
        for idx, action in enumerate(self._roadmap_items(), 1):
            lines.append(f'{idx}. {action}')
        lines.append('')
        lines.append('## Claim Wording Cautions')
        if self.claim_risk:
            lines.append('- Avoid broad phrases like "eco-friendly" or "carbon neutral" unless you can show current evidence, scope, and boundaries.')
            lines.append('- Prefer narrower wording such as "reduced packaging weight" or "contains recycled content" when those facts are documented.')
        else:
            lines.append('- Keep environmental wording specific, scoped, and evidence-backed.')
            lines.append('- Review any new headline claim with supporting proof before launch.')
        lines.append('')
        lines.append('## KPI Starter Pack')
        lines.append('- Packaging weight per order')
        lines.append('- Average parcel cube utilization or right-size rate')
        lines.append('- Return rate driven by avoidable reasons such as damage or fit confusion')
        lines.append('- Share of claims supported by documented evidence')
        lines.append('')
        lines.append('## Assumptions and Limitations')
        lines.append('- The brief assumes the user shared the main operational pain points and not just a marketing concern.')
        lines.append('- Formal carbon accounting, legal review, and certification work still require specialist follow-up.')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return SustainabilityAdvisor(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
