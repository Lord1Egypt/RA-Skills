#!/usr/bin/env python3
"""auto_router.py - Intelligent task routing for Frugal Orchestrator v0.5.0

Routes tasks to optimal execution:
- system: direct terminal commands
- script: Python/Node automation
- ai: AI subordinates for complex reasoning

Output: JSON with route, confidence, command
"""
import json
import re
import sys
from typing import Dict, Any, Optional

# Pattern categories
SYSTEM_PATTERNS = [
    ('file_read', [r'cat', r'read file', r'show content']),
    ('text_search', [r'grep', r'search for', r'find pattern']),
    ('text_transform', [r'sed', r'awk', r'tr', r'cut', r'sort', r'uniq', r'replace', r'transform']),
    ('data_query', [r'jq', r'json query', r'parse json']),
    ('network', [r'curl', r'wget', r'http', r'download']),
    ('file_ops', [r'ls', r'find', r'locate', r'list files']),
    ('system_info', [r'ps', r'top', r'netstat', r'lsof']),
]

SCRIPT_PATTERNS = [
    ('data_processing', [r'process csv', r'process json', r'parse data']),
    ('file_conversions', [r'convert csv', r'convert json']),
    ('batch_ops', [r'batch', r'bulk', r'multiple files']),
    ('calculations', [r'calculate', r'compute', r'sum', r'average']),
    ('automation', [r'automate', r'schedule', r'script']),
]

AI_PATTERNS = [
    ('reasoning', [r'analyze', r'evaluate', r'assess', r'determine', r'recommend', r'why', r'how should']),
    ('planning', [r'plan', r'design', r'architect', r'strategy', r'roadmap']),
    ('creation', [r'write', r'create', r'generate', r'draft', r'compose']),
    ('synthesis', [r'summarize', r'synthesize', r'consolidate', r'insights']),
    ('debugging', [r'debug', r'fix', r'troubleshoot', r'investigate']),
    ('research', [r'research', r'investigate', r'explore', r'discover']),
    ('decision', [r'compare', r'contrast', r'choose', r'select', r'prioritize']),
]

class TaskRouter:
    """Intelligent task router."""

    THRESHOLD = 0.75

    def __init__(self):
        self.scores = {'system': 0.0, 'script': 0.0, 'ai': 0.0}
        self.patterns = []

    def _analyze(self, task: str) -> Dict[str, float]:
        task_lower = task.lower()

        for cat, patterns in SYSTEM_PATTERNS:
            for p in patterns:
                if p in task_lower:
                    self.scores['system'] += 0.4
                    self.patterns.append(f's:{cat}')
                    break

        for cat, patterns in SCRIPT_PATTERNS:
            for p in patterns:
                if p in task_lower:
                    self.scores['script'] += 0.35
                    self.patterns.append(f'sc:{cat}')
                    break

        for cat, patterns in AI_PATTERNS:
            for p in patterns:
                if re.search(r'\b' + p.replace(' ', r'\s+') + r'\b', task_lower):
                    self.scores['ai'] += 0.5
                    self.patterns.append(f'ai:{cat}')
                    break

        # Direct command boosts
        direct = ['curl ', 'grep ', 'sed ', 'awk ', 'jq ', 'cat ', 'ls ', 'ps ']
        for d in direct:
            if d in task_lower:
                self.scores['system'] += 0.3

        if re.search(r'https?://\S+', task):
            self.scores['system'] += 0.2

        # Normalize
        total = sum(self.scores.values())
        if total > 0:
            for k in self.scores:
                self.scores[k] = min(self.scores[k] / (total * 0.7), 0.99)

        return self.scores

    def _build_cmd(self, task: str, route: str) -> Optional[str]:
        if route == 'system':
            # URL in task
            match = re.search(r'(https?://\S+)', task)
            if match:
                return f"curl -s {match.group(1)}"

            if 'grep' in task.lower():
                return 'grep <pattern> <file>'
            if 'cat ' in task.lower():
                return 'cat <file>'
            if 'ls' in task.lower():
                return 'ls -la'
            if 'jq' in task.lower():
                return 'jq <filter>'

            return 'bash -c <command>'

        elif route == 'script':
            return 'python3 -c "# TODO"'

        return task

    def route(self, task: str) -> Dict[str, Any]:
        if not task.strip():
            return {'route': 'error', 'confidence': 1.0, 'error': 'Empty task', 'command': None}

        scores = self._analyze(task)
        best = max(scores, key=scores.get)
        conf = scores[best]

        if conf < 0.4:
            best = 'ai'
            conf = max(conf, 0.5)

        return {
            'route': best,
            'confidence': round(conf, 2),
            'command': self._build_cmd(task, best),
            'scores': {k: round(v, 2) for k, v in scores.items()},
            'patterns': self.patterns[:5]
        }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Usage: auto_router.py <task>'}, indent=2))
        sys.exit(1)

    task = ' '.join(sys.argv[1:])
    print(json.dumps(TaskRouter().route(task), indent=2))


if __name__ == '__main__':
    main()
