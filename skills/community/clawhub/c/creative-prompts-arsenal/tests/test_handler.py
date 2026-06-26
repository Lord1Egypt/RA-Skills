#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_blank_page_writing_context_is_detected():
    output = handle('I have a blank page and need to write an article')
    assert '# Creative Prompt Kit' in output
    assert '- Domain: Writing' in output
    assert '- What feels stuck: Blank page' in output


def test_dict_input_supports_business_context():
    output = handle({
        'domain': 'Business',
        'stuckness': 'Too many ideas',
        'project': 'a new consulting offer'
    })
    assert 'a new consulting offer' in output
    assert 'Too many ideas' in output


def test_output_contains_best_first_prompt():
    output = handle('My design work feels stale and repetitive')
    assert '## Best First Prompt' in output
    assert '- Start with:' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
