#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import DecisionForestPlanner, handle


def test_option_extraction():
    planner = DecisionForestPlanner('Should I stay in my job or start a small consulting business by June?')
    assert 'Stay in my job' in planner.options[0]
    assert any('test' in option.lower() for option in planner.options)


def test_recommended_option_exists():
    planner = DecisionForestPlanner('I worry about money, so I need help deciding whether to stay or start something new.')
    assert planner.recommended_option


def test_output_sections():
    output = handle('Should I move cities or stay where I am? I am afraid of regretting it later.')
    assert output.startswith('# Decision Forest')
    assert '- Facts:' in output
    assert '- Assumptions:' in output
    assert '- Fears:' in output
    assert '- Review date:' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
