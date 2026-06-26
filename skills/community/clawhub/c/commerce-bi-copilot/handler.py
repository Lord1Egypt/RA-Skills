#!/usr/bin/env python3
import sys
from typing import Dict, List

MODE_RULES = {
    'Anomaly Diagnosis': ['why', 'drop', 'down', 'decline', 'spike', 'anomaly', 'sudden', 'fell'],
    'Weekly Review': ['weekly', 'monday', 'week over week', 'wow', 'leadership update'],
    'Campaign Recap': ['campaign', 'promotion', 'promo', 'launch', 'sale', 'black friday'],
    'Executive Summary': ['monthly', 'board', 'executive', 'founder update', 'leadership'],
    'Daily Health Check': ['daily', 'today', 'yesterday', 'morning digest'],
}

METRIC_RULES: Dict[str, Dict[str, object]] = {
    'GMV': {
        'keywords': ['gmv', 'gross merchandise value', 'sales', 'revenue'],
        'why': 'Track top-line demand and commercial momentum.',
        'verify': 'Confirm whether the team means gross sales, order value before refunds, or another house definition.',
    },
    'Net Revenue': {
        'keywords': ['net revenue', 'net sales', 'after refund', 'refund adjusted'],
        'why': 'Separate real collected revenue from gross demand.',
        'verify': 'Check refund timing, cancellation handling, and tax or shipping treatment.',
    },
    'ROAS / MER': {
        'keywords': ['roas', 'mer', 'ad spend', 'marketing efficiency', 'cac'],
        'why': 'Connect spend to revenue efficiency and budget quality.',
        'verify': 'Confirm attribution window and whether blended or channel-level spend is in scope.',
    },
    'Conversion Rate': {
        'keywords': ['conversion', 'cvr', 'checkout', 'sessions', 'traffic'],
        'why': 'Explain whether the issue is demand volume or funnel quality.',
        'verify': 'Check session source mix, landing-page quality, and checkout completion assumptions.',
    },
    'Refund Rate': {
        'keywords': ['refund', 'returns', 'chargeback', 'cancel'],
        'why': 'Protect net revenue and reveal post-purchase quality issues.',
        'verify': 'Separate policy-driven refunds from defects, logistics, and friendly fraud patterns.',
    },
    'Inventory Health': {
        'keywords': ['inventory', 'stock', 'stockout', 'oos', 'backorder'],
        'why': 'Show whether demand was lost because the best sellers were unavailable.',
        'verify': 'Review stockout duration, top-SKU share, and substitute-product behavior.',
    },
}

CHANNEL_RULES = {
    'Shopify': ['shopify'],
    'Amazon': ['amazon'],
    'TikTok Shop': ['tiktok', 'tik tok', 'douyin'],
    'Meta Ads': ['meta', 'facebook ads', 'instagram ads'],
    'Google Ads': ['google ads', 'google', 'youtube'],
    'GA4 / Analytics': ['ga4', 'analytics', 'google analytics'],
    'ERP / Inventory': ['erp', 'inventory', 'warehouse'],
    'CRM / Retention': ['crm', 'klaviyo', 'email', 'retention'],
}

DRIVER_LIBRARY = {
    'Traffic / Spend': {
        'keywords': ['traffic', 'spend', 'sessions', 'click', 'impression', 'meta', 'google'],
        'why': 'Volume shifts often start with paid or organic traffic quality and budget pacing.',
        'slices': 'channel, campaign, audience, creative, landing page',
    },
    'Conversion / Funnel': {
        'keywords': ['conversion', 'checkout', 'atc', 'cart', 'site', 'cvr'],
        'why': 'Revenue can fall even when traffic is stable if the funnel weakens.',
        'slices': 'device, landing page, PDP, cart, checkout step',
    },
    'Pricing / Promotion': {
        'keywords': ['discount', 'promo', 'promotion', 'coupon', 'price', 'sale'],
        'why': 'Promotions can inflate demand but hurt quality, margin, or post-promo retention.',
        'slices': 'offer type, order size, new vs returning, campaign window',
    },
    'Refund / Post-purchase': {
        'keywords': ['refund', 'return', 'chargeback', 'cancel'],
        'why': 'Net revenue problems are often hidden in refunds, cancels, and service failure.',
        'slices': 'reason code, SKU, fulfillment node, market, acquisition source',
    },
    'Inventory / Availability': {
        'keywords': ['inventory', 'stock', 'stockout', 'oos', 'backorder'],
        'why': 'High-demand SKUs can bottleneck the whole business when unavailable.',
        'slices': 'SKU, variant, top sellers, stockout hours, region',
    },
    'Channel Mix': {
        'keywords': ['channel', 'marketplace', 'shopify', 'amazon', 'mix', 'region'],
        'why': 'A business may look worse overall when volume shifts toward lower-converting or lower-margin channels.',
        'slices': 'channel, region, customer type, assisted vs direct',
    },
}


class CommerceBICopilot:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.mode = self._detect_mode()
        self.metrics = self._detect_metrics()
        self.channels = self._detect_channels()
        self.drivers = self._detect_drivers()

    def _detect_mode(self) -> str:
        for mode in ['Anomaly Diagnosis', 'Weekly Review', 'Campaign Recap', 'Executive Summary', 'Daily Health Check']:
            if any(keyword in self.lower for keyword in MODE_RULES[mode]):
                return mode
        return 'Daily Health Check'

    def _detect_metrics(self) -> List[str]:
        metrics = [name for name, data in METRIC_RULES.items() if any(keyword in self.lower for keyword in data['keywords'])]
        return metrics or ['GMV', 'Conversion Rate', 'Refund Rate', 'Inventory Health']

    def _detect_channels(self) -> List[str]:
        channels = [name for name, keywords in CHANNEL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return channels or ['Orders / Storefront', 'Ads / Traffic']

    def _detect_drivers(self) -> List[str]:
        drivers = [name for name, data in DRIVER_LIBRARY.items() if any(keyword in self.lower for keyword in data['keywords'])]
        ordered = []
        for candidate in ['Traffic / Spend', 'Conversion / Funnel', 'Pricing / Promotion', 'Refund / Post-purchase', 'Inventory / Availability', 'Channel Mix']:
            if candidate in drivers and candidate not in ordered:
                ordered.append(candidate)
        for candidate in ['Traffic / Spend', 'Conversion / Funnel', 'Inventory / Availability']:
            if candidate not in ordered:
                ordered.append(candidate)
        return ordered[:4]

    def _drill_downs(self) -> List[str]:
        tasks = []
        if 'GMV' in self.metrics or 'Net Revenue' in self.metrics:
            tasks.append('Slice performance by channel, top campaign, top SKU family, and region against a recent baseline.')
        if 'ROAS / MER' in self.metrics:
            tasks.append('Compare spend pacing, attribution window assumptions, and new-vs-returning customer efficiency.')
        if 'Refund Rate' in self.metrics:
            tasks.append('Break refund or cancel reasons by SKU, market, and fulfillment node to isolate operational issues.')
        if 'Inventory Health' in self.metrics:
            tasks.append('Review top-SKU stockout windows and estimate lost demand during unavailable hours.')
        if not tasks:
            tasks.append('Reconcile the metric dictionary before diagnosing causes so the team is debating the same number.')
        tasks.append('Document one plain-English answer to the business question before opening additional dashboard tabs.')
        return tasks[:4]

    def _next_actions(self) -> List[str]:
        actions = ['Lock the metric definition for this review so GMV, net revenue, and refund-adjusted revenue are not mixed together.']
        if 'Traffic / Spend' in self.drivers:
            actions.append('Check campaign pacing and the last 7-day median before changing budget or blaming creative.')
        if 'Conversion / Funnel' in self.drivers:
            actions.append('Inspect the highest-leverage funnel step and look for device, checkout, or landing-page friction.')
        if 'Inventory / Availability' in self.drivers:
            actions.append('Protect the top-selling SKUs with alerts, substitute logic, or replenishment follow-up.')
        if 'Refund / Post-purchase' in self.drivers:
            actions.append('Create a short refund-reason review with ops and CX so net revenue leakage is owned by someone specific.')
        if 'Pricing / Promotion' in self.drivers:
            actions.append('Review whether the offer structure boosted low-quality orders or trained customers to wait for discounts.')
        return actions[:4]

    def _executive_brief(self) -> List[str]:
        if self.mode == 'Weekly Review':
            return [
                'Frame the week around the biggest KPI movement, the strongest contributor, and the clearest risk entering next week.',
                'Keep the leadership update to wins, losses, root-cause hypothesis, and the one action each owner should take next.',
                'Use one chart per important story instead of a dashboard dump.',
            ]
        if self.mode == 'Campaign Recap':
            return [
                'Summarize campaign lift, efficiency quality, refund or margin side effects, and inventory readiness for the next push.',
                'Separate temporary promo volume from demand that is likely to persist.',
                'Call out what should be repeated, reduced, or tested differently next time.',
            ]
        if self.mode == 'Executive Summary':
            return [
                'Lead with the business outcome, not the chart mechanics.',
                'Explain the main driver in one sentence and the decision it points to in the next sentence.',
                'Keep open questions visible so leadership knows where the evidence is still incomplete.',
            ]
        if self.mode == 'Anomaly Diagnosis':
            return [
                'Start with the likely driver cluster instead of listing every metric that moved.',
                'State which slices would confirm or invalidate the current hypothesis fastest.',
                'Do not recommend a major budget, pricing, or inventory change until the top suspect is checked against a baseline.',
            ]
        return [
            'Use a compact daily summary: what moved, what most likely caused it, and what the team should verify today.',
            'Focus on exceptions and owner-ready tasks, not exhaustive dashboard narration.',
            'Escalate only when the movement is material, persistent, or tied to a key launch or inventory risk.',
        ]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Commerce BI Brief')
        lines.append('')
        lines.append(f'**Analysis mode:** {self.mode}')
        lines.append(f'**Channels referenced:** {", ".join(self.channels)}')
        lines.append('**Method note:** This is a heuristic commerce-analysis brief. No live BI connector, warehouse, or spreadsheet was accessed.')
        lines.append('')
        lines.append('## Executive Summary')
        lines.append('- Treat the input as a business question that needs a short answer, a likely explanation, and the next verification step.')
        lines.append('- Align the metric dictionary first so the team is not debating conflicting versions of the same KPI.')
        lines.append('')
        lines.append('## KPI Snapshot')
        lines.append('| Metric | Why it matters | First verification step |')
        lines.append('|---|---|---|')
        for metric in self.metrics:
            data = METRIC_RULES[metric]
            lines.append(f'| {metric} | {data["why"]} | {data["verify"]} |')
        lines.append('')
        lines.append('## Likely Driver Tree')
        for driver in self.drivers:
            data = DRIVER_LIBRARY[driver]
            lines.append(f'### {driver}')
            lines.append(f'- Why this matters: {data["why"]}')
            lines.append(f'- First slices to check: {data["slices"]}')
            lines.append('')
        lines.append('## Recommended Drill-Downs')
        for idx, item in enumerate(self._drill_downs(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Next Best Actions')
        for idx, item in enumerate(self._next_actions(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Executive-Ready Brief')
        for bullet in self._executive_brief():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Assumptions and Limits')
        lines.append('- This output is only as strong as the KPI notes and definitions the user provided.')
        lines.append('- Attribution, refund timing, and stock availability can all distort the apparent story if definitions are inconsistent.')
        lines.append('- Budget moves, pricing changes, and operational decisions still require human review.')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return CommerceBICopilot(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
