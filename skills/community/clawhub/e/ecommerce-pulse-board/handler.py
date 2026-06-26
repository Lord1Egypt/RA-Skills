#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

REVIEW_WINDOW_RULES = {
    'Daily': ['daily', 'today', 'yesterday', 'morning', 'day'],
    'Weekly': ['weekly', 'this week', 'last week', 'week'],
    'Monthly': ['monthly', 'this month', 'last month', 'month'],
    'Post-Campaign': ['post-campaign', 'after campaign', 'campaign debrief'],
    'Quarterly': ['quarterly', 'quarter', 'q1', 'q2', 'q3', 'q4'],
}

CHANNEL_RULES = {
    'Shopify': ['shopify', 'dtc', 'storefront'],
    'Amazon': ['amazon'],
    'TikTok Shop': ['tiktok', 'douyin'],
    'JD': ['jd', 'jingdong'],
    'Taobao': ['taobao', '1688'],
    'WeChat / Weidian': ['wechat', 'weixin', 'weidian'],
    'Other': ['other', 'general'],
}

PILLAR_RULES = {
    'Traffic': ['traffic', 'visit', 'session', 'click', 'impression', 'reach', 'ctr'],
    'Conversion': ['conversion', 'cvr', 'checkout', 'cart', 'atc', 'order', 'purchase'],
    'Inventory': ['inventory', 'stock', 'stockout', 'oos', 'backorder', 'cover', 'aging'],
    'Marketing Efficiency': ['roas', 'mer', 'cpm', 'cpc', 'cpa', 'ad spend', 'spend'],
    'Fulfillment': ['fulfillment', 'shipping', 'delivery', 'od', 'late shipment', 'oms', 'warehouse'],
}

CONCERN_RULES = {
    'GMV / Revenue': ['gmv', 'revenue', 'sales', 'orders'],
    'Margin / Profitability': ['margin', 'profit', 'gross', 'refund'],
    'Traffic / Channel': ['traffic', 'channel', 'traffic drop'],
    'Inventory / Stockout': ['stockout', 'inventory', 'stock', 'cover'],
    'Ad Efficiency': ['roas', 'mer', 'ad spend', 'efficiency'],
    'Fulfillment': ['shipping', 'delivery', 'fulfillment', 'oms'],
}

PulseInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for kw in kws if kw in text) for name, kws in rules.items()}


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'Not specified'


class EcommercePulseBoard:
    def __init__(self, user_input: PulseInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.window = self._detect_window()
        self.channels = self._detect_channels()
        self.pillars = self._detect_pillars()
        self.concern = self._detect_concern()

    def _normalize_input(self, user_input: PulseInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['window', 'channels', 'kpis', 'concern', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_window(self) -> str:
        scores = _score_rules(self.lower, REVIEW_WINDOW_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Weekly'

    def _detect_channels(self) -> List[str]:
        matched = [name for name, kws in CHANNEL_RULES.items() if any(kw in self.lower for kw in kws)]
        return matched or ['Shopify', 'Amazon']

    def _detect_pillars(self) -> List[str]:
        matched = [name for name, kws in PILLAR_RULES.items() if any(kw in self.lower for kw in kws)]
        return matched or ['Traffic', 'Conversion', 'Marketing Efficiency']

    def _detect_concern(self) -> str:
        scores = _score_rules(self.lower, CONCERN_RULES)
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'Overall Health'

    def _pillar_scores(self) -> List[Dict[str, str]]:
        pillar_notes = {
            'Traffic': {
                'signal': 'Sessions, clicks, reach; direction vs. prior period.',
                'check': 'Which channel drove the most traffic? Any sudden channel shifts?',
                'owner': 'Paid Media + Organic',
            },
            'Conversion': {
                'signal': 'CVR, checkout completion, cart abandonment rate.',
                'check': 'Did CVR hold despite traffic changes? Any funnel step spikes?',
                'owner': 'Storefront + Product',
            },
            'Inventory': {
                'signal': 'Days of cover, stockout count, inbound ETA confidence.',
                'check': 'Any hero SKU at risk of stockout before next inbound?',
                'owner': 'Ops + Purchasing',
            },
            'Marketing Efficiency': {
                'signal': 'ROAS, MER, CPM, CPC; blended vs. channel-level.',
                'check': 'Did ROAS hold? Any channel efficiency degradation?',
                'owner': 'Paid Media',
            },
            'Fulfillment': {
                'signal': 'OTIF %, late shipment rate, average delivery time.',
                'check': 'Any warehouse or carrier capacity constraints?',
                'owner': 'Ops + Logistics',
            },
        }
        scores = {
            'Traffic': '🟡 Moderate',
            'Conversion': '🟡 Moderate',
            'Inventory': '🟡 Moderate',
            'Marketing Efficiency': '🟡 Moderate',
            'Fulfillment': '🟢 Good',
        }
        if self.concern == 'Traffic / Channel':
            scores['Traffic'] = '🔴 Weak'
        if self.concern == 'GMV / Revenue':
            scores['Conversion'] = '🔴 Weak'
        if self.concern == 'Ad Efficiency':
            scores['Marketing Efficiency'] = '🔴 Weak'
        if self.concern == 'Inventory / Stockout':
            scores['Inventory'] = '🔴 Weak'
        if self.concern == 'Fulfillment':
            scores['Fulfillment'] = '🔴 Weak'
        rows = []
        for pillar in ['Traffic', 'Conversion', 'Inventory', 'Marketing Efficiency', 'Fulfillment']:
            if pillar in self.pillars:
                info = pillar_notes[pillar]
                rows.append({
                    'pillar': pillar,
                    'score': scores.get(pillar, '🟡 Moderate'),
                    'signal': info['signal'],
                    'check': info['check'],
                    'owner': info['owner'],
                })
        return rows

    def _signal_of_week(self) -> str:
        concern_signals = {
            'GMV / Revenue': 'Top-line demand direction this week; whether volume is up, flat, or down and which channel is driving the change.',
            'Margin / Profitability': 'Refund rate and promotional discount depth; whether margin is being protected as volume changes.',
            'Traffic / Channel': 'Channel mix and whether traffic sources are shifting in quality or cost.',
            'Inventory / Stockout': 'Hero SKU cover and whether any inbound risk is emerging before the next campaign.',
            'Ad Efficiency': 'ROAS trend vs. prior 7 days; whether any channel is becoming inefficient.',
            'Fulfillment': 'OTIF and late shipment rate; any carrier or warehouse pressure building up.',
            'Overall Health': 'The single most material observation from the week across channels and pillars.',
        }
        return concern_signals.get(self.concern, concern_signals['Overall Health'])

    def _risk_watchlist(self) -> List[Dict[str, str]]:
        risks = [
            {
                'area': 'Traffic Concentration',
                'cause': 'Over-reliance on a single paid channel creates vulnerability if ROAS declines.',
                'owner': 'Paid Media',
                'mitigation': 'Diversify to at least 2 channels; build organic or email as a hedge.',
            },
            {
                'area': 'Inventory Risk at Hero SKU',
                'cause': 'Top SKUs with low days of cover and uncertain inbound timing.',
                'owner': 'Ops + Purchasing',
                'mitigation': 'Lock reorder for hero SKUs with <14 days cover; do not wait for sell-through confirmation.',
            },
            {
                'area': 'Conversion Funnel Weakness',
                'cause': 'Cart abandonment or checkout drop-off that is not being actively diagnosed.',
                'owner': 'Storefront',
                'mitigation': 'Set up weekly funnel review; address the highest-drop-off step first.',
            },
        ]
        if self.concern == 'Ad Efficiency':
            risks.insert(0, {
                'area': 'ROAS Decline in Paid Channel',
                'cause': 'Creative fatigue, audience exhaustion, or landing page conversion drop.',
                'owner': 'Paid Media',
                'mitigation': 'Pause declining campaign, test new creative, and audit landing page before scaling back.',
            })
        return risks[:3]

    def _priority_actions(self) -> List[str]:
        actions = [
            'Review the signal of the week and confirm whether it is a trend or a one-time event.',
            'Check inventory cover for the top 3 SKUs — lock reorder if days of cover is below 14.',
            'Run a 7-day ROAS check across all paid channels; flag any channel down >15% vs. prior week.',
            'Review the top 3 conversion drop-off steps in the checkout funnel.',
            'Confirm fulfillment OTIF for the week; escalate any carrier delays before they compound.',
        ]
        if self.concern == 'Traffic / Channel':
            actions.insert(0, 'Audit traffic source mix: paid vs. organic vs. referral. Identify the channel with the most leverage.')
        if self.concern == 'Inventory / Stockout':
            actions.insert(0, 'Pull a stockout report for all SKUs with <10 days of cover. Assign an owner and ETA for each.')
        return actions[:5]

    def _channel_spotlight(self) -> List[str]:
        lines = []
        for ch in self.channels:
            lines.append(f'### {ch}')
            lines.append(f'- Track: orders, AOV, refund rate, and top SKU performance.')
            lines.append(f'- Watch: stock availability, campaign performance, and customer review velocity.')
            lines.append('')
        return lines

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Ecommerce Pulse Brief')
        lines.append('')
        lines.append(f'**Review window:** {self.window}')
        lines.append(f'**Channels in scope:** {_join(self.channels)}')
        lines.append(f'**Main concern:** {self.concern}')
        lines.append('**Method note:** This is a heuristic operational brief. No live analytics, ad platform, ERP, or OMS was accessed.')
        lines.append('')
        lines.append('## Pulse Summary')
        lines.append(f'- **{self.window} review** across {_join(self.channels)}.')
        lines.append(f'- Primary concern this cycle: **{self.concern}**.')
        lines.append('- Assess each pillar below; treat 🟡 as "monitor closely" and 🔴 as "action required today."')
        lines.append('')
        lines.append('## Pillar Health Grid')
        lines.append('| Pillar | Score | Signal | First Check | Owner |')
        lines.append('|---|---|---|---|---|')
        for row in self._pillar_scores():
            lines.append(f'| {row["pillar"]} | {row["score"]} | {row["signal"]} | {row["check"]} | {row["owner"]} |')
        lines.append('')
        lines.append('## Signal of the Week')
        lines.append(f'- **{self.concern}:** {self._signal_of_week()}')
        lines.append('')
        lines.append('## Risk Watchlist')
        lines.append('| At-Risk Area | Likely Cause | Recommended Owner | Mitigation |')
        lines.append('|---|---|---|---|---|')
        for risk in self._risk_watchlist():
            lines.append(f'| {risk["area"]} | {risk["cause"]} | {risk["owner"]} | {risk["mitigation"]} |')
        lines.append('')
        lines.append('## Priority Actions')
        for idx, action in enumerate(self._priority_actions(), 1):
            lines.append(f'{idx}. {action}')
        lines.append('')
        lines.append('## Channel Spotlight')
        for item in self._channel_spotlight():
            lines.append(item)
        lines.append('## Data Quality Note')
        lines.append('- KPI values in this brief are directional. Confirm actual numbers against your analytics, ad platform, or ERP before making irreversible decisions.')
        lines.append('- If any pillar is missing data, treat it as 🟡 by default until confirmed.')
        lines.append('- Cross-reference channel-level data against total business metrics to avoid double-counting or missing attribution gaps.')
        return '\n'.join(lines)


def handle(user_input: PulseInput) -> str:
    return EcommercePulseBoard(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
