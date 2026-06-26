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


BLOCK_KEYWORDS = {
    'early morning': ['early morning', '6am', '7am', 'wake up', 'first thing'],
    'late morning': ['late morning', '9am', '10am', '11am', 'mid-morning'],
    'early afternoon': ['early afternoon', 'after lunch', '1pm', '2pm'],
    'late afternoon': ['late afternoon', '3pm', '4pm', '5pm'],
    'evening': ['evening', 'night', '7pm', '8pm', '9pm'],
}

POSITIVE_WORDS = ['sharp', 'clear', 'focused', 'best', 'good', 'great', 'creative', 'strong', 'steady', 'alert']
NEGATIVE_WORDS = ['crash', 'slump', 'low', 'foggy', 'tired', 'drained', 'flat', 'sleepy', 'hard']
DISRUPTOR_RULES = [
    ('poor sleep', ['poor sleep', 'slept badly', 'sleep debt', 'up late']),
    ('caffeine spikes and crashes', ['coffee', 'caffeine', 'espresso']),
    ('meal timing or after-lunch dip', ['after lunch', 'hungry', 'meal', 'ate late']),
    ('family or work interruptions', ['interrupt', 'kids', 'child', 'meeting', 'messages']),
    ('workout timing', ['workout', 'exercise', 'run', 'gym']),
]


class EnergyPeakFinder:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.snippets = self._snippets()
        self.block_scores = self._score_blocks()
        self.best_window = self._best_window()
        self.lowest_window = self._lowest_window()
        self.disruptors = self._disruptors()
        self.hypotheses = self._hypotheses()
        self.task_matching = self._task_matching()
        self.experiment = self._experiment()

    def _snippets(self) -> List[str]:
        parts = re.split(r'[\n.;!?]+|,\s*but\s+|\s+but\s+', self.raw, flags=re.IGNORECASE)
        return [part.strip(' -•') for part in parts if part.strip(' -•')]

    def _score_blocks(self) -> Dict[str, int]:
        scores = {block: 0 for block in BLOCK_KEYWORDS}
        mentioned = False
        for snippet in self.snippets:
            lower = snippet.lower()
            positive = sum(1 for word in POSITIVE_WORDS if word in lower)
            negative = sum(1 for word in NEGATIVE_WORDS if word in lower)
            delta = positive - negative
            for block, keywords in BLOCK_KEYWORDS.items():
                if any(keyword in lower for keyword in keywords):
                    scores[block] += delta if delta != 0 else 1
                    mentioned = True
        if not mentioned:
            scores['late morning'] = 2
            scores['early afternoon'] = -1
        return scores

    def _best_window(self) -> str:
        return max(self.block_scores, key=self.block_scores.get)

    def _lowest_window(self) -> str:
        return min(self.block_scores, key=self.block_scores.get)

    def _disruptors(self) -> List[str]:
        found = [label for label, words in DISRUPTOR_RULES if any(word in self.lower for word in words)]
        if 'urgent' in self.lower or 'deadline' in self.lower or 'adrenaline' in self.lower:
            found.append('urgency may be disguising itself as usable energy')
        if not found:
            found.append('not enough repeated disruptor data yet')
        unique: List[str] = []
        for item in found:
            if item not in unique:
                unique.append(item)
        return unique

    def _hypotheses(self) -> Dict[str, str]:
        boosts: List[str] = []
        drains: List[str] = []
        if any(word in self.lower for word in ['slept well', 'good sleep', 'early bed']):
            boosts.append('Sleep quality appears to lift your steadier focus windows.')
        if any(word in self.lower for word in ['walk', 'exercise', 'workout', 'sunlight']):
            boosts.append('Movement or light exposure may be supporting alertness.')
        if self.best_window == 'late morning':
            boosts.append('Late morning looks like your most reliable cognitive window right now.')
        if any(word in self.lower for word in ['coffee', 'caffeine', 'espresso']):
            drains.append('Caffeine may be creating a false peak or a sharper later drop.')
        if any(word in self.lower for word in ['after lunch', 'hungry', 'meal', 'ate late']):
            drains.append('Meal timing may be contributing to an afternoon dip.')
        if any(word in self.lower for word in ['interrupt', 'kids', 'meeting', 'messages']):
            drains.append('Interruptions are likely reducing usable energy even when alertness exists.')
        if not boosts:
            boosts.append('Your best energy window needs one more week of observation to confirm.')
        if not drains:
            drains.append('The main drain is not fully clear yet, so keep tracking sleep, meals, and interruptions.')
        return {
            'boosts': ' '.join(boosts[:2]),
            'drains': ' '.join(drains[:2]),
        }

    def _task_matching(self) -> Dict[str, str]:
        return {
            'peak': f'Use {self.best_window} for deep work, writing, strategy, or hard problem-solving.',
            'medium': 'Use the middle windows for planning, meetings, lighter study, and admin that still needs attention.',
            'low': f'Use {self.lowest_window} for chores, inbox, recovery, or lower-stakes tasks.',
        }

    def _experiment(self) -> str:
        confounders = ', '.join(self.disruptors[:2])
        return f'For the next 7 days, protect {self.best_window} for your hardest task, keep {self.lowest_window} lighter, and log sleep, meals, and {confounders} once per day.'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Energy Pattern Review')
        lines.append('')
        lines.append('## Observation Summary')
        lines.append(f'- Best energy window: {self.best_window}')
        lines.append(f'- Lowest energy window: {self.lowest_window}')
        lines.append(f"- Most common disruptors: {', '.join(self.disruptors)}")
        lines.append('')
        lines.append('## Task Matching')
        lines.append(f"- Peak energy tasks: {self.task_matching['peak']}")
        lines.append(f"- Medium energy tasks: {self.task_matching['medium']}")
        lines.append(f"- Low energy tasks: {self.task_matching['low']}")
        lines.append('')
        lines.append('## Hypotheses')
        lines.append(f"- What seems to boost energy: {self.hypotheses['boosts']}")
        lines.append(f"- What seems to drain energy: {self.hypotheses['drains']}")
        lines.append('')
        lines.append('## Next Experiment')
        lines.append(f'- For the next 7 days, I will: {self.experiment}')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('energy-peak-finder')
    finder = EnergyPeakFinder(inputs)
    return finder.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
