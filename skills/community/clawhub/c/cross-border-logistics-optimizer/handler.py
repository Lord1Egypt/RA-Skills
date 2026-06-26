#!/usr/bin/env python3
import re
import sys
from typing import Dict, List, Optional, Tuple

COUNTRY_ALIASES = {
    'china': 'China',
    'germany': 'Germany',
    'brazil': 'Brazil',
    'canada': 'Canada',
    'united states': 'United States',
    'usa': 'United States',
    'us': 'United States',
    'uk': 'United Kingdom',
    'united kingdom': 'United Kingdom',
    'france': 'France',
    'australia': 'Australia',
    'japan': 'Japan',
}

PRODUCT_RULES = {
    'cosmetics': ['cosmetic', 'beauty', 'skincare', 'cream', 'liquid', 'serum'],
    'battery electronics': ['battery', 'electronics', 'device', 'bluetooth', 'charger', 'power bank'],
    'apparel': ['apparel', 'fashion', 'clothing', 'shirt', 'dress'],
    'supplements': ['supplement', 'powder', 'capsule', 'vitamin'],
    'accessories': ['accessory', 'jewelry', 'case', 'cable'],
}

PRIORITY_RULES = {
    'fastest': ['fastest', 'urgent', 'express', 'quickest'],
    'cheapest': ['cheapest', 'low cost', 'lowest cost', 'budget'],
    'safest': ['safest', 'reliable', 'low risk', 'secure'],
}

LANES = [
    {
        'name': 'Economy Tracked Packet',
        'cost': 'Low',
        'speed': 'Slow',
        'customs': 'Medium-High',
        'tracking': 'Basic',
        'best_for': 'cost-sensitive, low-risk parcels',
    },
    {
        'name': 'Duty-aware Direct Line',
        'cost': 'Medium',
        'speed': 'Medium',
        'customs': 'Low-Medium',
        'tracking': 'Good',
        'best_for': 'balanced e-commerce lanes with customs control',
    },
    {
        'name': 'Express Courier',
        'cost': 'High',
        'speed': 'Fast',
        'customs': 'Medium',
        'tracking': 'Excellent',
        'best_for': 'urgent deliveries or premium customer promises',
    },
]


class LogisticsOptimizer:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.origin, self.destination = self._extract_countries()
        self.priority = self._detect_priority()
        self.product_type = self._detect_product_type()
        self.weight_kg = self._extract_weight_kg()
        self.dimensions_cm = self._extract_dimensions_cm()
        self.declared_value = self._extract_declared_value()
        self.risk_flags = self._build_risk_flags()

    def _extract_countries(self) -> Tuple[str, str]:
        origin = 'Origin not specified'
        destination = 'Destination not specified'
        route_match = re.search(r'from\s+([a-z\s]+?)\s+to\s+([a-z\s]+?)(?:\s+for|\s+with|\s+at|\s+via|$)', self.lower)
        if route_match:
            raw_origin = route_match.group(1).strip()
            raw_destination = route_match.group(2).strip()
            origin = COUNTRY_ALIASES.get(raw_origin, raw_origin.title())
            destination = COUNTRY_ALIASES.get(raw_destination, raw_destination.title())
            return origin, destination
        found = []
        for key, display in COUNTRY_ALIASES.items():
            if key in self.lower and display not in found:
                found.append(display)
        if found:
            origin = found[0]
        if len(found) > 1:
            destination = found[1]
        return origin, destination

    def _detect_priority(self) -> str:
        for priority, keywords in PRIORITY_RULES.items():
            if any(word in self.lower for word in keywords):
                return priority
        return 'balanced'

    def _detect_product_type(self) -> str:
        for name, keywords in PRODUCT_RULES.items():
            if any(word in self.lower for word in keywords):
                return name
        return 'general merchandise'

    def _extract_weight_kg(self) -> Optional[float]:
        match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|g|lb|lbs)', self.lower)
        if not match:
            return None
        value = float(match.group(1))
        unit = match.group(2)
        if unit == 'g':
            return round(value / 1000, 2)
        if unit in ('lb', 'lbs'):
            return round(value * 0.4536, 2)
        return value

    def _extract_dimensions_cm(self) -> Optional[Tuple[int, int, int]]:
        match = re.search(r'(\d{1,3})\s*[x×]\s*(\d{1,3})\s*[x×]\s*(\d{1,3})\s*(cm|in)', self.lower)
        if not match:
            return None
        dims = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
        unit = match.group(4)
        if unit == 'in':
            dims = [round(d * 2.54) for d in dims]
        return tuple(dims)

    def _extract_declared_value(self) -> Optional[int]:
        match = re.search(r'\$\s?(\d{1,5})|(\d{1,5})\s?(?:usd|dollars)', self.lower)
        if not match:
            return None
        for part in match.groups():
            if part:
                return int(part)
        return None

    def _build_risk_flags(self) -> List[str]:
        flags: List[str] = []
        if self.destination == 'Brazil':
            flags.append('Brazil lanes often face documentation scrutiny and longer customs dwell time.')
        if self.destination == 'Germany':
            flags.append('Germany-bound parcels need precise product description and tax-ready paperwork.')
        if self.destination == 'Canada':
            flags.append('Canada lanes can punish dimensional weight on light but bulky parcels.')
        if self.product_type == 'cosmetics':
            flags.append('Cosmetics need cleaner ingredient/category descriptions and leak-resistant packaging.')
        if self.product_type == 'battery electronics':
            flags.append('Battery goods may trigger carrier restrictions and special handling checks.')
        if self.weight_kg and self.weight_kg > 2:
            flags.append('Heavier parcels may lose economy-lane savings quickly.')
        if self.dimensions_cm and sum(self.dimensions_cm) > 90:
            flags.append('Parcel size may attract dimensional-weight surcharges or oversize screening.')
        if any(word in self.lower for word in ['customs', 'delay', 'sensitive', 'duty']):
            flags.append('The user already signaled customs sensitivity, so reliability matters more than headline price.')
        return flags or ['Inputs are limited, so the analysis uses a generic parcel-shipping baseline.']

    def _recommended_lane(self) -> Dict[str, str]:
        if self.priority == 'fastest':
            return LANES[2]
        if self.priority == 'cheapest' and self.product_type in ('general merchandise', 'accessories', 'apparel') and len(self.risk_flags) <= 2:
            return LANES[0]
        if self.product_type in ('cosmetics', 'battery electronics', 'supplements') or any('customs' in flag.lower() for flag in self.risk_flags):
            return LANES[1]
        if self.priority == 'safest':
            return LANES[1]
        return LANES[1]

    def _packaging_notes(self) -> List[str]:
        notes = []
        if self.dimensions_cm and sum(self.dimensions_cm) > 90:
            notes.append('Reduce void fill and carton size to control dimensional-weight billing.')
        if self.product_type == 'cosmetics':
            notes.append('Use leak-control sealing and isolate liquid SKUs from outer-wall impact points.')
        if self.product_type == 'battery electronics':
            notes.append('Use inner cushioning plus clear battery labeling before handoff to the carrier.')
        if not notes:
            notes.append('Use a right-sized carton and document pack-out consistency to reduce exceptions.')
        notes.append('Place a clean commercial description and value summary where the fulfillment team cannot miss it.')
        return notes

    def render(self) -> str:
        recommended = self._recommended_lane()
        lines: List[str] = []
        lines.append('# Cross-border Logistics Decision Brief')
        lines.append('')
        lines.append(f'**Route:** {self.origin} to {self.destination}')
        lines.append(f'**Business priority:** {self.priority}')
        lines.append(f'**Product type:** {self.product_type}')
        lines.append(f'**Weight estimate:** {self.weight_kg if self.weight_kg is not None else "Not provided"}')
        lines.append(f'**Declared value:** ${self.declared_value}' if self.declared_value is not None else '**Declared value:** Not provided')
        lines.append('**Method note:** This is a heuristic lane comparison. No live carrier rate or customs API was used.')
        lines.append('')
        lines.append('## Route Comparison')
        lines.append('| Option | Cost | Speed | Customs risk | Tracking | Best fit |')
        lines.append('|---|---|---|---|---|---|')
        for lane in LANES:
            lines.append(f'| {lane["name"]} | {lane["cost"]} | {lane["speed"]} | {lane["customs"]} | {lane["tracking"]} | {lane["best_for"]} |')
        lines.append('')
        lines.append('## Recommended Plan')
        lines.append(f'- Recommended lane: **{recommended["name"]}**')
        if recommended['name'] == 'Express Courier':
            rationale = 'Choose this when speed is the clear priority and the customer promise justifies the higher spend.'
        elif recommended['name'] == 'Economy Tracked Packet':
            rationale = 'Choose this when cost matters most and the parcel profile is low-risk enough to tolerate slower movement.'
        else:
            rationale = 'Choose this when the business needs a balanced lane with better customs control than the cheapest option.'
        lines.append(f'- Why this fits: {rationale}')
        lines.append(f'- Operational reminder: Match the lane to the real parcel profile before handoff, especially if weight, value, or product sensitivity changes.')
        lines.append('')
        lines.append('## Packaging Checklist')
        for note in self._packaging_notes():
            lines.append(f'- {note}')
        lines.append('')
        lines.append('## Customs and Exception Risks')
        for flag in self.risk_flags:
            lines.append(f'- {flag}')
        lines.append('')
        lines.append('## Assumptions and Next Steps')
        lines.append('- Confirm the exact carrier service, not just the brand, because service families behave differently.')
        lines.append('- Recheck declaration wording, parcel dimensions, and value before the final label is purchased.')
        lines.append('- If the lane is mission critical, compare one live quote after this heuristic shortlisting step.')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return LogisticsOptimizer(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
