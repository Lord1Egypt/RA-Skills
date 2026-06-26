#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Sequence, Union

WatchInput = Union[str, Dict[str, Any]]

WATCH_MODE_RULES = {
    'Pricing and Promo Scan': ['price', 'pricing', 'discount', 'promo', 'promotion', 'coupon', 'markdown'],
    'Assortment and Launch Scan': ['launch', 'new sku', 'new product', 'assortment', 'variant', 'bundle'],
    'Creative and Messaging Scan': ['creative', 'message', 'copy', 'ugc', 'ad', 'content'],
    'Service and CX Scan': ['service', 'support', 'shipping', 'delivery', 'refund'],
    'Weekly General Watch': ['weekly', 'monitor', 'watchlist', 'watch'],
}

SURFACE_RULES = {
    'DTC site': ['dtc', 'site', 'website', 'shopify'],
    'Amazon': ['amazon'],
    'Tmall / Taobao': ['tmall', 'taobao', '淘宝'],
    'TikTok Shop / Douyin': ['tiktok', 'douyin'],
    'Xiaohongshu': ['xiaohongshu', 'xhs', 'rednote'],
    'Retail / offline': ['retail', 'store shelf', 'offline'],
}

SIGNAL_RULES = {
    'Price and discounting': ['price', 'discount', 'coupon', 'promo', 'markdown'],
    'Assortment and launch': ['launch', 'sku', 'assortment', 'variant', 'bundle'],
    'Reviews and proof': ['review', 'rating', 'testimonial', 'proof'],
    'Creative and messaging': ['creative', 'message', 'copy', 'ugc', 'ad'],
    'Service and fulfillment': ['shipping', 'delivery', 'refund', 'service', 'support'],
}

PRESSURE_RULES = {
    'Aggressive price pressure': ['heavy discount', 'aggressive', 'deep discount', 'price war'],
    'Launch visibility risk': ['launch', 'new product', 'debut'],
    'Trust or proof drift': ['review', 'rating', 'testimonial', 'ugc'],
    'Service perception risk': ['late delivery', 'refund issues', 'support complaints'],
}


def _normalize_input(user_input: WatchInput) -> str:
    if isinstance(user_input, dict):
        chunks: List[str] = []
        for key in ['surfaces', 'competitors', 'watch_mode', 'signals', 'notes', 'priority']:
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


class CompetitorWatchtower:
    def __init__(self, user_input: WatchInput):
        self.raw = user_input
        self.text = _normalize_input(user_input)
        self.lower = self.text.lower()
        self.watch_mode = _match_one(self.lower, WATCH_MODE_RULES, 'Weekly General Watch')
        self.surfaces = _match_many(self.lower, SURFACE_RULES, ['DTC site', 'Amazon'], limit=4)
        self.signals = _match_many(self.lower, SIGNAL_RULES, ['Price and discounting', 'Assortment and launch'], limit=4)
        self.pressure_flags = _match_many(self.lower, PRESSURE_RULES, ['Aggressive price pressure'], limit=3)

    def _signal_rows(self) -> List[List[str]]:
        notes = {
            'Price and discounting': ['Price and discounting', 'Track list price, bundle logic, discount depth, and whether urgency is sustainable.'],
            'Assortment and launch': ['Assortment and launch', 'Watch for hero SKU changes, new bundles, premiumization, or defensive line extensions.'],
            'Reviews and proof': ['Reviews and proof', 'Check whether the competitor is strengthening trust with ratings, UGC, or comparison claims.'],
            'Creative and messaging': ['Creative and messaging', 'Look for sharper hooks, clearer proof, or positioning shifts that could change buyer perception.'],
            'Service and fulfillment': ['Service and fulfillment', 'Monitor delivery promises, refund friction, and support positioning that can alter conversion quality.'],
        }
        return [notes[item] for item in self.signals if item in notes]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Competitor Watchtower Brief')
        lines.append('')
        lines.append(f'**Watch mode:** {self.watch_mode}')
        lines.append(f'**Surfaces in scope:** {_join(self.surfaces)}')
        lines.append(f'**Priority signals:** {_join(self.signals)}')
        lines.append(f'**Pressure flags:** {_join(self.pressure_flags)}')
        lines.append('**Method note:** This is a heuristic competitor brief. No live scraping, ad library, marketplace API, or BI platform was accessed.')
        lines.append('')
        lines.append('## Competitive Situation Summary')
        lines.append('- Treat competitor movement as a signal to interpret, not a command to react instantly.')
        lines.append('- Ask whether the rival move threatens your margin, conversion path, trust position, or category narrative.')
        lines.append(f'- Because the main watch mode is **{self.watch_mode.lower()}**, the operator should separate real commercial risk from performative noise.')
        lines.append('')
        lines.append('## Signal Grid')
        lines.append('| Signal | What to inspect first |')
        lines.append('|---|---|')
        for row in self._signal_rows():
            lines.append(f'| {row[0]} | {row[1]} |')
        lines.append('')
        lines.append('## Threats and Opportunity Windows')
        lines.append('- If the competitor is discounting hard, decide whether the threat is real share loss or just visible noise with weak staying power.')
        lines.append('- If a rival launched something new, check whether it fills a real whitespace or simply reframes an existing offer.')
        lines.append('- Look for opportunities where the competitor is teaching the market but leaving trust, service, or value gaps open.')
        lines.append('')
        lines.append('## Response Options')
        lines.append('1. Hold position when the rival move does not materially change buyer choice or category economics.')
        lines.append('2. Strengthen proof, offer clarity, or merchandising before matching a competitor on price.')
        lines.append('3. Escalate only the moves that affect your hero SKUs, margin guardrails, or launch window.')
        lines.append('4. Create a tighter follow-up watchlist for any unresolved threat instead of reacting with broad panic.')
        lines.append('')
        lines.append('## Watch Cadence and Owners')
        lines.append('- **Weekly operator scan:** price, promo, and hero-SKU changes.')
        lines.append('- **Campaign window scan:** creative, launch, and landing-page changes during high-risk periods.')
        lines.append('- **Owner suggestion:** one commercial owner, one marketplace owner, and one brand or content owner for interpretation.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        lines.append('- This brief depends on the evidence quality supplied by the user and may overstate or understate competitor intent when notes are incomplete.')
        lines.append('- Legal, pricing, assortment, and public-response decisions remain human-approved.')
        lines.append('- Avoid overfitting to one screenshot, one campaign, or one temporary discount burst.')
        return "\n".join(lines)


def handle(user_input: WatchInput) -> str:
    return CompetitorWatchtower(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
