#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

OBJECTIVE_RULES = {
    'SKU Cleanup': ['cleanup', 'rationalize', 'prune', 'retire', 'long-tail', 'long tail', 'sku clutter', 'bloat', 'duplicate'],
    'Gap Discovery': ['gap', 'whitespace', 'white space', 'coverage', 'missing', 'price ladder', 'assortment gap'],
    'Expansion Planning': ['expand', 'extension', 'premium', 'premiumize', 'bundle', 'add sku', 'line extension', 'expand range'],
    'Seasonal Review': ['seasonal', 'holiday', 'summer', 'winter', 'back to school', 'gifting', 'campaign'],
}

SIGNAL_RULES = {
    'Revenue / Units': ['revenue', 'sales', 'gmv', 'units', 'velocity', 'sell-through', 'sell through', 'conversion'],
    'Margin / Cost': ['margin', 'profit', 'cost', 'gross margin', 'contribution'],
    'Returns / Reviews': ['return', 'refund', 'review', 'rating', 'score', 'feedback'],
    'Inventory / Markdown': ['inventory', 'stock', 'markdown', 'clearance', 'aged', 'aging'],
    'Variants / Coverage': ['size', 'color', 'variant', 'attribute', 'pack', 'material', 'coverage', 'price band'],
}

CONSTRAINT_RULES = {
    'Warehouse / Cash Constraint': ['warehouse', 'cash', 'capacity', 'shelf', 'space'],
    'Strategic Hero Protection': ['hero', 'flagship', 'protected line', 'core line', 'brand'],
    'Seasonal Timing': ['seasonal', 'holiday', 'campaign', 'launch window', 'promo'],
}

SEGMENT_NOTES = {
    'hero': 'Protect proven traffic and conversion anchors before pruning the catalog around them.',
    'core': 'Maintain the dependable volume and margin base that stabilizes the category.',
    'seasonal': 'Treat seasonal items as opportunity bets, not permanent assortment defaults.',
    'long-tail': 'Challenge slow movers that add complexity without enough reach, margin, or strategic value.',
    'duplicate-risk': 'Group near-identical products and variants to test whether they deserve separate shelf space.',
}

ActionInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for keyword in keywords if keyword in text) for name, keywords in rules.items()}


def _join_list(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class AssortmentScout:
    def __init__(self, user_input: ActionInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.objective = self._detect_objective()
        self.signals = self._detect_signals()
        self.constraints = self._detect_constraints()
        self.segments = ['hero', 'core', 'seasonal', 'long-tail', 'duplicate-risk']

    def _normalize_input(self, user_input: ActionInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['objective', 'catalog_scope', 'signals', 'constraints', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_objective(self) -> str:
        scores = _score_rules(self.lower, OBJECTIVE_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'SKU Cleanup'

    def _detect_signals(self) -> List[str]:
        matched = [name for name, keywords in SIGNAL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return matched or ['Revenue / Units', 'Margin / Cost', 'Variants / Coverage']

    def _detect_constraints(self) -> List[str]:
        matched = [name for name, keywords in CONSTRAINT_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        base = matched or ['Strategic Hero Protection']
        if 'Warehouse / Cash Constraint' not in base:
            base.append('Warehouse / Cash Constraint')
        return base[:3]

    def _scorecard_rows(self) -> List[Dict[str, str]]:
        rows = [
            {
                'lens': 'Hero Dependence',
                'inspect': 'Revenue concentration in top products, launch age, and margin resilience.',
                'why': 'A weak bench behind hero SKUs makes growth fragile and limits assortment flexibility.',
            },
            {
                'lens': 'Tail Bloat',
                'inspect': 'Long-tail units, markdown frequency, support load, and warehouse complexity.',
                'why': 'Low-value tail items often consume attention and cash without creating net incremental demand.',
            },
            {
                'lens': 'Coverage Gaps',
                'inspect': 'Price ladder, use case ladder, variant balance, and entry-to-premium spacing.',
                'why': 'A catalog can look large while still missing practical buying paths for important segments.',
            },
            {
                'lens': 'Duplicate Risk',
                'inspect': 'Near-identical variants, overlapping claims, and products with similar price and demand profiles.',
                'why': 'Overlap can create internal competition that raises costs without enough incremental revenue.',
            },
        ]
        return rows

    def _gap_map(self) -> List[str]:
        items = [
            'Review whether the price ladder jumps too sharply between entry, core, and premium offers.',
            'Check if important use cases are uncovered while low-value variants multiply inside the same use case.',
            'Confirm whether size, color, pack size, or material variants reflect real demand rather than internal preference.',
        ]
        if self.objective == 'Gap Discovery':
            items.insert(0, 'Prioritize white-space opportunities where demand intent is clear but current coverage is thin.')
        if self.objective == 'Expansion Planning':
            items.insert(0, 'Look for bundle, premium, or adjacent-line opportunities that extend the hero logic instead of fragmenting it.')
        return items[:4]

    def _watchlist(self) -> List[str]:
        items = [
            'Flag SKU clusters with similar price, promise, and audience but weak differentiation in margin or demand quality.',
            'Question variant families that expanded faster than evidence, especially color or pack-size proliferation.',
            'Escalate any product that underperforms yet remains protected by habit instead of strategic rationale.',
        ]
        if 'Returns / Reviews' in self.signals:
            items.append('Review whether high-return or low-rating items are masking a product-market or quality mismatch.')
        return items[:4]

    def _actions(self) -> List[str]:
        actions = [
            'Keep and defend the hero and core SKUs that anchor traffic, conversion, or margin quality.',
            'Merge or simplify near-duplicate variants before adding new assortment complexity.',
            'Retire, bundle, or repackage long-tail items that create operational drag without strategic upside.',
            'Create one focused test for the highest-confidence white-space or premiumization opportunity.',
        ]
        if self.objective == 'Gap Discovery':
            actions[3] = 'Add one deliberate gap-filling test where the price ladder or use-case ladder is visibly incomplete.'
        if self.objective == 'Expansion Planning':
            actions[3] = 'Expand around the strongest hero logic with one adjacent line, bundle, or premium tier instead of broad SKU proliferation.'
        if self.objective == 'Seasonal Review':
            actions[2] = 'Reduce seasonal clutter early so the promo window is concentrated on the highest-conviction assortment.'
        return actions

    def _execution_brief(self) -> List[str]:
        return [
            'Week 1: confirm taxonomy, price bands, and which SKUs are strategically protected before any retire or merge discussion.',
            'Week 2: review the duplicate-risk clusters and long-tail items with merch, ops, and inventory owners in the same room.',
            'Week 3: approve one gap-fill or bundle test, plus one cleanup action that removes measurable complexity.',
            'Week 4: compare pre-change and post-change signals, then lock the next assortment cycle based on evidence rather than anecdote.',
        ]

    def _assumptions(self) -> List[str]:
        notes = [
            'This brief is heuristic and only as strong as the catalog, pricing, and performance notes supplied by the user.',
            'Cannibalization is inferred from overlap patterns, not proven through controlled causal analysis.',
            'Retire, merge, pricing, and supplier decisions should remain human-approved.',
        ]
        missing = [signal for signal in ['Returns / Reviews', 'Inventory / Markdown'] if signal not in self.signals]
        if missing:
            notes.append(f'Missing or lightly referenced signals: {_join_list(missing)}.')
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Assortment Scout Brief')
        lines.append('')
        lines.append(f'**Primary objective:** {self.objective}')
        lines.append(f'**Signals referenced:** {_join_list(self.signals)}')
        lines.append(f'**Operating constraints:** {_join_list(self.constraints)}')
        lines.append('**Method note:** This is a heuristic assortment-planning brief. No live ERP, PIM, storefront, or marketplace data was accessed.')
        lines.append('')
        lines.append('## Assortment Health Summary')
        lines.append('- Start by clarifying the role of each SKU: hero, core, seasonal, long-tail, or duplicate-risk.')
        lines.append('- Treat assortment quality as a portfolio question, not a pure sales ranking exercise.')
        lines.append('- If taxonomy or pricing logic is weak, downgrade any aggressive keep-add-retire recommendation to a hypothesis.')
        lines.append('')
        lines.append('## Scorecard Lenses')
        lines.append('| Lens | What to inspect first | Why it matters |')
        lines.append('|---|---|---|')
        for row in self._scorecard_rows():
            lines.append(f'| {row["lens"]} | {row["inspect"]} | {row["why"]} |')
        lines.append('')
        lines.append('## Coverage and Gap Map')
        for idx, item in enumerate(self._gap_map(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Cannibalization Watchlist')
        for bullet in self._watchlist():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Action Recommendations')
        for idx, action in enumerate(self._actions(), 1):
            lines.append(f'{idx}. {action}')
        lines.append('')
        lines.append('## 30-Day Execution Brief')
        for idx, action in enumerate(self._execution_brief(), 1):
            lines.append(f'{idx}. {action}')
        lines.append('')
        lines.append('## Segment Notes')
        for segment in self.segments:
            lines.append(f'- **{segment}:** {SEGMENT_NOTES[segment]}')
        lines.append('')
        lines.append('## Assumptions and Limits')
        for note in self._assumptions():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: ActionInput) -> str:
    return AssortmentScout(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
