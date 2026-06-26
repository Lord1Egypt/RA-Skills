#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List


def _load_skill_meta(slug):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = re.search(r'^---$(.*?)^---$', content, re.DOTALL | re.MULTILINE)
    return meta.group(1).strip() if meta else ''


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ''
    if isinstance(inputs, str):
        return inputs.strip()
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _clean_option(text: str) -> str:
    text = text.strip().strip(' ?.!')
    text = re.sub(r'^(whether to|to|either)\s+', '', text, flags=re.IGNORECASE)
    return text[:1].upper() + text[1:] if text else 'Unnamed option'


CRITERIA_RULES = {
    'Cost and runway': ['cost', 'money', 'salary', 'income', 'budget', 'cash', 'runway'],
    'Time and life load': ['time', 'busy', 'schedule', 'bandwidth', 'capacity'],
    'Energy and stress': ['energy', 'stress', 'burnout', 'tired'],
    'Meaning and growth': ['meaning', 'growth', 'purpose', 'learn', 'career'],
    'Family impact': ['family', 'kids', 'partner', 'home'],
    'Reversibility': ['reverse', 'reversible', 'test', 'trial', 'pilot'],
}


class DecisionForestPlanner:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.snippets = self._split_snippets()
        self.decision = self._extract_decision()
        self.deadline = self._extract_deadline()
        self.options = self._extract_options()
        self.non_negotiables = self._extract_non_negotiables()
        self.criteria = self._extract_criteria()
        self.facts = self._extract_facts()
        self.assumptions = self._extract_assumptions()
        self.fears = self._extract_fears()
        self.recommended_option = self._recommend_choice()
        self.review_date = self._review_date()

    def _split_snippets(self) -> List[str]:
        parts = re.split(r'[\n.;!?]+', self.raw)
        return [part.strip(' -•') for part in parts if part.strip(' -•')]

    def _extract_decision(self) -> str:
        match = re.search(r'(should i .+?|choose between .+?|decide whether to .+?)(?:[.?!]|$)', self.lower)
        if match:
            decision = match.group(1)
        elif self.snippets:
            decision = self.snippets[0]
        else:
            decision = 'Choose the strongest path from the available options'
        decision = decision.strip()
        return decision[:1].upper() + decision[1:]

    def _extract_deadline(self) -> str:
        match = re.search(r'(by\s+[a-z0-9\- ]+|before\s+[a-z0-9\- ]+|next\s+week|this\s+month|this\s+quarter|tomorrow)', self.lower)
        if match:
            return match.group(1).strip()
        return 'No hard deadline stated'

    def _extract_options(self) -> List[str]:
        patterns = [
            r'between\s+(.+?)\s+and\s+(.+?)(?:[.?!]|$)',
            r'should i\s+(.+?)\s+or\s+(.+?)(?:[.?!]|$)',
            r'decide whether to\s+(.+?)\s+or\s+(.+?)(?:[.?!]|$)',
            r'(.+?)\s+vs\.?\s+(.+?)(?:[.?!]|$)',
        ]
        options: List[str] = []
        for pattern in patterns:
            match = re.search(pattern, self.lower)
            if match:
                options = [_clean_option(match.group(1)), _clean_option(match.group(2))]
                break
        if not options:
            options = ['Stay with the current path', 'Make a smaller new move']
        if not any('test' in option.lower() or 'trial' in option.lower() or 'pilot' in option.lower() for option in options):
            options.append('Run a smaller reversible test')
        return options[:3]

    def _extract_non_negotiables(self) -> List[str]:
        items: List[str] = []
        if any(word in self.lower for word in ['family', 'kids', 'partner', 'home']):
            items.append('Protect family stability and attention.')
        if any(word in self.lower for word in ['money', 'salary', 'income', 'cash', 'runway', 'budget']):
            items.append('Protect financial runway.')
        if any(word in self.lower for word in ['health', 'sleep', 'burnout', 'stress']):
            items.append('Avoid a choice that clearly harms health or recovery.')
        if any(word in self.lower for word in ['values', 'ethic', 'integrity']):
            items.append('Do not trade away core values for short-term gain.')
        if not items:
            items = ['Protect financial and emotional stability.', 'Keep the first move as reversible as possible.']
        return items

    def _extract_criteria(self) -> List[str]:
        found = [label for label, keywords in CRITERIA_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        defaults = ['Cost and runway', 'Time and life load', 'Meaning and growth', 'Reversibility']
        ordered: List[str] = []
        for item in found + defaults:
            if item not in ordered:
                ordered.append(item)
        return ordered[:4]

    def _extract_facts(self) -> str:
        for snippet in self.snippets:
            if any(word in snippet.lower() for word in ['already', 'currently', 'have', 'is', 'are', 'deadline', 'offer']):
                return snippet
        return f'You are comparing {self.options[0]} and {self.options[1]}.'

    def _extract_assumptions(self) -> str:
        for snippet in self.snippets:
            if any(word in snippet.lower() for word in ['maybe', 'probably', 'might', 'if', 'could']):
                return snippet
        return 'Some upside and downside estimates are still assumptions, not verified evidence.'

    def _extract_fears(self) -> str:
        for snippet in self.snippets:
            if any(word in snippet.lower() for word in ['afraid', 'worry', 'fear', 'regret', 'fail']):
                return snippet
        return 'Fear of choosing the wrong branch permanently is louder than the available proof.'

    def _reversibility(self, option: str) -> str:
        lower = option.lower()
        if any(word in lower for word in ['test', 'trial', 'pilot', 'part-time', 'part time', 'prototype']):
            return 'Mostly reversible'
        if any(word in lower for word in ['quit', 'resign', 'buy', 'move', 'full-time', 'full time']):
            return 'Harder to reverse'
        return 'Partly reversible'

    def _key_unknown(self, option: str) -> str:
        if 'Cost and runway' in self.criteria:
            return 'The true cost and runway required.'
        if 'Family impact' in self.criteria:
            return 'The effect on family energy and logistics.'
        if 'Meaning and growth' in self.criteria:
            return 'Whether the option still feels meaningful after the novelty fades.'
        return 'Which hidden tradeoff matters most in real life.'

    def _branch_summary(self, option: str) -> Dict[str, str]:
        reversible = self._reversibility(option)
        best_case = f'{option} aligns with your top criteria and creates useful momentum.'
        base_case = f'{option} works, but it comes with tradeoffs in {self.criteria[0].lower()} and {self.criteria[1].lower()}.'
        worst_case = f'{option} looks attractive now, but the hidden costs are larger than expected.'
        return {
            'best': best_case,
            'base': base_case,
            'worst': worst_case,
            'reversible': reversible,
            'unknown': self._key_unknown(option),
        }

    def _recommend_choice(self) -> str:
        test_option = next((option for option in self.options if 'test' in option.lower() or 'trial' in option.lower()), None)
        if test_option and ('fear' in self.fears.lower() or self.deadline == 'No hard deadline stated'):
            return test_option
        stable_option = next((option for option in self.options if 'stay' in option.lower() or 'current' in option.lower()), None)
        if stable_option and any('runway' in item.lower() or 'stability' in item.lower() for item in self.non_negotiables):
            return stable_option
        growth_option = next((option for option in self.options if any(word in option.lower() for word in ['start', 'build', 'move', 'create'])), None)
        if growth_option and 'Meaning and growth' in self.criteria:
            return growth_option
        return self.options[0]

    def _review_date(self) -> str:
        if self.deadline != 'No hard deadline stated':
            return self.deadline
        return 'After one real-world test or within 7 days'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Decision Forest')
        lines.append('')
        lines.append('## Decision Trunk')
        lines.append(f'- Decision: {self.decision}')
        lines.append(f'- Deadline: {self.deadline}')
        lines.append(f"- Non-negotiables: {'; '.join(self.non_negotiables)}")
        lines.append(f'- Facts: {self.facts}')
        lines.append(f'- Assumptions: {self.assumptions}')
        lines.append(f'- Fears: {self.fears}')
        lines.append('')
        lines.append('## Criteria')
        for criterion in self.criteria:
            lines.append(f'- {criterion}')
        lines.append('')
        lines.append('## Branches')
        labels = ['A', 'B', 'C']
        for label, option in zip(labels, self.options):
            summary = self._branch_summary(option)
            lines.append(f'### Option {label}: {option}')
            lines.append(f"- Best case: {summary['best']}")
            lines.append(f"- Base case: {summary['base']}")
            lines.append(f"- Worst case: {summary['worst']}")
            lines.append(f"- Reversible or not: {summary['reversible']}")
            lines.append(f"- Key unknown: {summary['unknown']}")
            lines.append('')
        lines.append('## Choice Logic')
        lines.append(f'- Most aligned option: {self.recommended_option}')
        lines.append('- Why: It protects learning while keeping the biggest constraints visible.')
        lines.append('- What would change the choice: Clearer evidence on the main unknown or a non-negotiable becoming more urgent.')
        lines.append(f'- Review date: {self.review_date}')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('decision-forest')
    planner = DecisionForestPlanner(inputs)
    return planner.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
