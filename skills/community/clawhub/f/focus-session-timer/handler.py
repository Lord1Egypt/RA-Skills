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


HEAVY_TASK_WORDS = ['write', 'draft', 'strategy', 'code', 'coding', 'research', 'study', 'chapter', 'memo', 'analysis', 'problem set', 'exam']
LIGHT_TASK_WORDS = ['email', 'inbox', 'admin', 'cleanup', 'review', 'reply', 'small task', 'quick']
LOW_ENERGY_WORDS = ['tired', 'low energy', 'foggy', 'drained', 'sleepy', 'exhausted']
INTERRUPTION_WORDS = ['interrupt', 'kids', 'child', 'caregiving', 'meeting', 'on-call', 'support', 'phone', 'messages']


class FocusSessionPlanner:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.task = self._extract_task()
        self.cognitive_load = self._detect_cognitive_load()
        self.mode = self._choose_mode()
        self.definition_of_done = self._definition_of_done()
        self.start_ritual = self._start_ritual()
        self.interruption_rule = self._interruption_rule()
        self.break_plan = self._break_plan()
        self.progress_prompt = self._progress_prompt()
        self.next_start = self._next_start()

    def _snippets(self) -> List[str]:
        pieces = re.split(r'[\n.;!?]+', self.raw)
        return [piece.strip(' -•') for piece in pieces if piece.strip(' -•')]

    def _extract_task(self) -> str:
        patterns = [
            r'(?:focus on|work on|study|writing|write|finish|complete)\s+(.+?)(?:\b(?:for|with|before|but|and)\b|$)',
            r'task\s*(?:is|:)?\s*(.+?)(?:\b(?:for|with|before|but|and)\b|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.lower)
            if match:
                task = match.group(1).strip(' ,')
                if task:
                    return task[:1].upper() + task[1:]
        snippets = self._snippets()
        if snippets:
            snippet = snippets[0].strip()
            return snippet[:1].upper() + snippet[1:]
        return 'Move one meaningful task forward'

    def _detect_cognitive_load(self) -> str:
        if any(word in self.lower for word in HEAVY_TASK_WORDS):
            return 'heavy'
        if any(word in self.lower for word in LIGHT_TASK_WORDS):
            return 'light'
        return 'medium'

    def _choose_mode(self) -> Dict[str, str]:
        interrupted = any(word in self.lower for word in INTERRUPTION_WORDS)
        low_energy = any(word in self.lower for word in LOW_ENERGY_WORDS)
        explicit_short = bool(re.search(r'\b(10|15)\s*(minutes|minute|min)\b', self.lower))
        explicit_long = bool(re.search(r'\b(45|50|60|90)\s*(minutes|minute|min)\b', self.lower)) or 'deep work' in self.lower
        if self.cognitive_load == 'light' or explicit_short:
            return {'label': 'Quick Sprint', 'length': '15 minutes', 'break': '3 minutes'}
        if self.cognitive_load == 'heavy' and not interrupted and not low_energy:
            return {'label': 'Deep Work Block', 'length': '50 minutes', 'break': '10 minutes'}
        if explicit_long and not interrupted:
            return {'label': 'Deep Work Block', 'length': '50 minutes', 'break': '10 minutes'}
        return {'label': 'Standard Focus', 'length': '25 minutes', 'break': '5 minutes'}

    def _definition_of_done(self) -> str:
        if 'write' in self.lower or 'draft' in self.lower:
            return 'Finish one rough draft or one clear section.'
        if 'study' in self.lower or 'problem' in self.lower or 'exam' in self.lower:
            return 'Finish one problem set, section, or review target.'
        if 'email' in self.lower or 'inbox' in self.lower:
            return 'Clear one defined batch of messages and leave the inbox with a visible stopping point.'
        if 'code' in self.lower or 'debug' in self.lower:
            return 'Finish one bug fix, one function, or one tested chunk of implementation.'
        return f'Finish one visible chunk of: {self.task.lower()}.'

    def _start_ritual(self) -> List[str]:
        ritual = [
            'Put the task name and finish line where you can see it.',
            'Close or silence the obvious distraction channels for one block.',
        ]
        if self.mode['label'] == 'Quick Sprint':
            ritual.append('Open only the single document, tab, or queue this sprint needs.')
        elif self.mode['label'] == 'Deep Work Block':
            ritual.append('Set a blank capture line for stray ideas so they do not steal the block.')
        else:
            ritual.append('Take one breath and name the first concrete action before starting.')
        return ritual

    def _interruption_rule(self) -> str:
        if any(word in self.lower for word in INTERRUPTION_WORDS):
            return 'Mark the exact stopping point, write the next tiny action, handle the interruption, then restart with a 5 minute re-entry sprint.'
        return 'If interrupted, write one sentence about where you stopped, park the distraction, and restart from the smallest next action.'

    def _break_plan(self) -> str:
        return f"{self.mode['break']} away from the task. A real break means standing up, moving, water, or a window, not messages or scrolling."

    def _progress_prompt(self) -> str:
        if self.mode['label'] == 'Deep Work Block':
            return 'Name the deepest part of the task that actually moved.'
        if self.mode['label'] == 'Quick Sprint':
            return 'Name the smallest visible thing you finished.'
        return 'Name what moved and what stayed sticky.'

    def _next_start(self) -> str:
        if 'write' in self.lower or 'draft' in self.lower:
            return 'Start the next session by reopening the draft and revising the first unfinished paragraph.'
        if 'study' in self.lower or 'problem' in self.lower:
            return 'Start with the first unsolved problem or the note you left beside it.'
        if 'email' in self.lower or 'inbox' in self.lower:
            return 'Start with the next message batch, not the whole inbox.'
        return 'Start with the first unfinished step you can do in under two minutes.'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Focus Session Card')
        lines.append('')
        lines.append('## Session Goal')
        lines.append(f'- Task: {self.task}')
        lines.append(f'- Definition of done: {self.definition_of_done}')
        lines.append(f"- Chosen mode: {self.mode['label']} ({self.mode['length']})")
        lines.append('')
        lines.append('## Start Ritual')
        for item in self.start_ritual:
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## During Session')
        lines.append('- Distraction capture: Keep one scratch line or note open for unrelated thoughts, errands, or tabs to revisit later.')
        lines.append(f'- If interrupted, I will: {self.interruption_rule}')
        lines.append('')
        lines.append('## Break Plan')
        lines.append(f"- Length: {self.mode['break']}")
        lines.append(f'- What counts as a real break: {self.break_plan}')
        lines.append('')
        lines.append('## End Review')
        lines.append(f'- Progress made: {self.progress_prompt}')
        lines.append(f'- Next starting point: {self.next_start}')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('focus-session-timer')
    planner = FocusSessionPlanner(inputs)
    return planner.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
