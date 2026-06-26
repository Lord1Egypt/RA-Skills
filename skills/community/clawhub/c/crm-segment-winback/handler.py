#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

BUSINESS_RULES = {
    'DTC Brand': ['dtc', 'direct to consumer', 'brand', 'shopify', 'owned'],
    'Marketplace Seller': ['amazon', 'jd', 'taobao', 'marketplace', 'platform'],
    'Subscription': ['subscription', 'subscribe', 'recurring', 'membership'],
    'Hybrid': ['hybrid', 'multi-channel', ' DTC and marketplace'],
}

SEGMENT_RULES = {
    'New Customer': ['new', 'first order', 'first purchase', 'onboarding'],
    'Active Customer': ['active', 'regular', 'repeat', 'frequent'],
    'Lapsed Customer': ['lapsed', 'inactive', 'dormant', 'has not purchased', '90 days'],
    'VIP / Loyal': ['vip', 'loyal', 'top', 'best', 'high value', 'lifetime'],
    'At-Risk': ['at risk', 'at-risk', 'declining', 'decreasing', 'reduced'],
    'Churned': ['churned', 'churn', 'lost', 'unsubscribed', 'opted out'],
}

CHANNEL_RULES = {
    'Email': ['email', 'klaviyo', 'mailchimp', 'newsletter'],
    'SMS': ['sms', 'text', 'message', 'smsbump'],
    'WeChat': ['wechat', 'weixin', 'miniprogram'],
    'App Push': ['push', 'app notification', 'mobile push'],
}

WinbackInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for kw in kws if kw in text) for name, kws in rules.items()}


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'Not specified'


class CRMSegmentWinback:
    def __init__(self, user_input: WinbackInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.business = self._detect_business()
        self.segments = self._detect_segments()
        self.channels = self._detect_channels()
        self.goal = self._detect_goal()

    def _normalize_input(self, user_input: WinbackInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['business', 'segments', 'channels', 'campaign_goal', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_business(self) -> str:
        scores = _score_rules(self.lower, BUSINESS_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'DTC Brand'

    def _detect_segments(self) -> List[str]:
        matched = [name for name, kws in SEGMENT_RULES.items() if any(kw in self.lower for kw in kws)]
        return matched or ['New Customer', 'Active Customer', 'Lapsed Customer']

    def _detect_channels(self) -> List[str]:
        matched = [name for name, kws in CHANNEL_RULES.items() if any(kw in self.lower for kw in kws)]
        return matched or ['Email']

    def _detect_goal(self) -> str:
        if any(kw in self.lower for kw in ['winback', 'reengage', 're-activate', 'reactivate', 'lapsed', 'churn']):
            return 'Winback / Re-engagement'
        if any(kw in self.lower for kw in ['vip', 'loyal', 'lifetime', 'retention']):
            return 'VIP Loyalty'
        if any(kw in self.lower for kw in ['onboarding', 'new customer', 'first order']):
            return 'New Customer Onboarding'
        return 'Segment Health Review'

    def _segment_framework(self) -> List[Dict[str, str]]:
        return [
            {
                'segment': 'New Customer',
                'definition': 'First order completed within last 30 days',
                'recency': '0–30 days',
                'frequency': '1 order',
                'monetary': 'First-order AOV',
                'engagement': 'Email opens >20%, SMS click >5%',
                'priority': 'High',
            },
            {
                'segment': 'Active Customer',
                'definition': '2+ orders in last 90 days, AOV above median',
                'recency': '0–90 days',
                'frequency': '2+ orders',
                'monetary': 'Above median AOV',
                'engagement': 'Email opens >30%, SMS click >8%',
                'priority': 'Maintain',
            },
            {
                'segment': 'Lapsed Customer',
                'definition': 'No purchase in 60–180 days, previously active',
                'recency': '60–180 days',
                'frequency': 'Was 2+, now 0',
                'monetary': 'Below or at median AOV',
                'engagement': 'Email opens <15%, disengaged',
                'priority': 'High — winback window',
            },
            {
                'segment': 'At-Risk',
                'definition': 'Declining purchase frequency or AOV in last 60 days',
                'recency': '0–60 days but declining',
                'frequency': 'Frequency dropping MoM',
                'monetary': 'AOV declining',
                'engagement': 'Email opens <20%, SMS沉默',
                'priority': 'Urgent — early intervention',
            },
            {
                'segment': 'VIP / Loyal',
                'definition': 'Top 10% by LTV, 3+ orders in last 6 months, no refund issues',
                'recency': '0–60 days',
                'frequency': '3+ orders',
                'monetary': 'Top 10% LTV',
                'engagement': 'High across all channels',
                'priority': 'Protect — exclusive offers',
            },
            {
                'segment': 'Churned',
                'definition': 'No purchase in 180+ days, email/SMS also disengaged',
                'recency': '180+ days',
                'frequency': 'Previously active, now 0',
                'monetary': 'Variable, often below median',
                'engagement': 'Unsubscribed or fully disengaged',
                'priority': 'Low priority — expensive to win back',
            },
        ]

    def _winback_triggers(self) -> List[Dict[str, str]]:
        return [
            {'trigger': 'No purchase in 30 days', 'segment': 'Active → Lapsed', 'action': 'Send a re-engagement email with best-seller recommendation.'},
            {'trigger': 'No purchase in 60 days', 'segment': 'Lapsed', 'action': 'SMS winback with 10–15% off incentive; email follow-up with social proof.'},
            {'trigger': 'No purchase in 90 days', 'segment': 'Lapsed → At-Risk', 'action': 'Personalized "we miss you" email + exclusive offer + UGC reminder.'},
            {'trigger': 'Frequency declining (MoM)', 'segment': 'Active → At-Risk', 'action': 'Proactive outreach; offer a loyalty reward or bundle to stabilize.'},
            {'trigger': 'Cart abandoned (email)', 'segment': 'Any active segment', 'action': 'Automated 3-step cart abandonment sequence.'},
            {'trigger': '180+ days, unsubscribed', 'segment': 'Churned', 'action': 'Consider suppression; reactivation cost often exceeds LTV.'},
        ]

    def _channel_matrix(self) -> List[str]:
        lines = ['| Segment | Best Channel | Message Type | Frequency | Offer Tone |']
        lines.append('|---|---|---|---|---|')
        matrix = [
            ('New Customer', 'Email', 'Onboarding sequence + product education', 'Email d1/d3/d7', 'Value-add, no discount'),
            ('Active Customer', 'Email + SMS', 'New arrival + loyalty points', 'Weekly email, bi-weekly SMS', 'Appreciation + early access'),
            ('Lapsed Customer', 'SMS + Email', 'Winback offer + social proof', 'SMS d1/d7, Email d3', 'Discount or exclusive offer'),
            ('At-Risk', 'SMS + App Push', 'Urgency + personalized product', 'SMS d1/d3', 'Small incentive to reactivate'),
            ('VIP / Loyal', 'Email + WeChat', 'Exclusive preview + VIP-only offer', 'Monthly exclusive', 'Recognition, no heavy discount'),
            ('Churned', 'Email only', 'Last-chance re-engagement', 'One-time email', 'Deep discount or free gift with order'),
        ]
        for row in matrix:
            lines.append(f'| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |')
        return lines

    def _campaign_sequence(self) -> List[str]:
        if self.goal == 'Winback / Re-engagement':
            return [
                'Day 1: SMS — "We miss you — here\'s 15% off your next order [CODE]"',
                'Day 3: Email — "Top sellers this week" + personalized product recommendations',
                'Day 7: Email — "A customer like you loved [specific product]" + UGC social proof',
                'Day 14: Optional — Second discount email or free shipping offer for first order back',
            ]
        if self.goal == 'New Customer Onboarding':
            return [
                'Day 1: Welcome email — brand story + what\'s in the package',
                'Day 3: Product education email — how to use, tips, FAQs',
                'Day 7: Cross-sell email — complementary product based on first purchase',
                'Day 14: Review request email — request product review + social share',
                'Day 30: Reactivation check — has this customer purchased again? If not, move to lapsed flow.',
            ]
        if self.goal == 'VIP Loyalty':
            return [
                'Monthly: Exclusive early access to new product launches',
                'Quarterly: VIP-only discount or free shipping event',
                'Ongoing: Personalized birthday/anniversary offer',
                'Post-purchase: Thank-you note + loyalty points bonus',
            ]
        return [
            'Map each segment to the appropriate campaign flow above.',
            'Set up triggered sends for behavioral signals (abandoned cart, browse, review).',
            'Review segment size and engagement monthly; suppress disengaged contacts to protect deliverability.',
        ]

    def _kpi_framework(self) -> List[str]:
        return [
            '**Segment size:** Count of contacts per segment, updated monthly.',
            '**Email open rate:** Target >25% for winback, >35% for VIP; <15% signals disengagement.',
            '**SMS click rate:** Target >5%; below 2% suggests message or offer fatigue.',
            '**Reactivation rate:** % of lapsed customers who purchase within 30 days of winback campaign.',
            '**LTV of reactivated customers:** Compare against new customer LTV to assess winback ROI.',
            '**Opt-out rate:** Target <0.5% per campaign; spike indicates message frequency or relevance issue.',
        ]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# CRM Segment & Winback Brief')
        lines.append('')
        lines.append(f'**Business type:** {self.business}')
        lines.append(f'**Campaign goal:** {self.goal}')
        lines.append(f'**Segments in scope:** {_join(self.segments)}')
        lines.append(f'**Channels:** {_join(self.channels)}')
        lines.append('**Method note:** This is a heuristic CRM brief. No live CRM platform, customer data warehouse, or marketing automation tool was accessed.')
        lines.append('')
        lines.append('## Segment Framework')
        lines.append('| Segment | Definition | Recency | Frequency | Monetary | Engagement Signal | Priority |')
        lines.append('|---|---|---|---|---|---|---|')
        for row in self._segment_framework():
            lines.append(f'| {row["segment"]} | {row["definition"]} | {row["recency"]} | {row["frequency"]} | {row["monetary"]} | {row["engagement"]} | {row["priority"]} |')
        lines.append('')
        lines.append('## Winback Trigger Library')
        lines.append('| Trigger | Segment Transition | Recommended Action |')
        lines.append('|---|---|---|')
        for row in self._winback_triggers():
            lines.append(f'| {row["trigger"]} | {row["segment"]} | {row["action"]} |')
        lines.append('')
        lines.append('## Channel Suitability Matrix')
        for row in self._channel_matrix():
            lines.append(row)
        lines.append('')
        lines.append('## Campaign Sequence Ideas')
        for item in self._campaign_sequence():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## KPI Framework')
        for item in self._kpi_framework():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Data Quality Notes')
        lines.append('- Confirm RFM (Recency, Frequency, Monetary) definitions are consistent across all platforms before importing into a CRM tool.')
        lines.append('- Suppress unsubscribed and permanently bounced contacts from all non-permission-based campaigns.')
        lines.append('- Tag each contact with lifecycle stage so the system can auto-transition them over time.')
        return '\n'.join(lines)


def handle(user_input: WinbackInput) -> str:
    return CRMSegmentWinback(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
