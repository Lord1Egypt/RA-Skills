#!/usr/bin/env python3
"""Meeting Extractor — Pull action items and decisions from transcripts."""
import sys, re, json, argparse
from pathlib import Path

ACTION_PATTERNS = [
    r'(?:action|todo|task|assign|follow[- ]?up)[:\s]+(.+)',
    r'(\w+)\s+(?:will|should|needs? to|has to|going to)\s+(.+)',
    r'(?:by|before|deadline|due)\s+((?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|next week|eod|eow|\d{1,2}/\d{1,2}|\w+ \d{1,2})\b.*)',
]

DECISION_PATTERNS = [
    r'(?:decided|agreed|approved|confirmed|chose|selected|going with)[:\s]+(.+)',
    r'(?:the decision is|we\'ll go with|final answer is)[:\s]+(.+)',
    r'(?:yes|approved|let\'s do it|sounds good|ship it)[.!]?\s*(.*)',
]

QUESTION_PATTERNS = [
    r'(\?.+)',
    r'(?:what about|how about|what if|why don\'t we|can we|should we)\s+(.+)\??',
]

def extract_attendees(text):
    """Extract attendee names from common patterns."""
    names = set()
    for m in re.finditer(r'(?:hi|hello|hey),?\s+(\w+)', text, re.I):
        names.add(m.group(1).title())
    for m in re.finditer(r'^(\w+):', text, re.M):
        word = m.group(1)
        if len(word) > 1 and word[0].isupper() and not word.isupper():
            names.add(word)
    return sorted(names)

def extract_actions(text):
    """Extract action items."""
    items = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        for pat in ACTION_PATTERNS:
            m = re.search(pat, line, re.I)
            if m:
                items.append(line[:200])
                break
    return items

def extract_decisions(text):
    """Extract decisions."""
    items = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        for pat in DECISION_PATTERNS:
            m = re.search(pat, line, re.I)
            if m:
                items.append(line[:200])
                break
    return items

def extract_questions(text):
    """Extract unresolved questions."""
    items = []
    for line in text.split('\n'):
        line = line.strip()
        if '?' in line and len(line) > 10:
            items.append(line[:200])
    return items

def summarize(text):
    """Create a brief summary from first/last parts."""
    sentences = re.split(r'[.!]\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if len(sentences) <= 5:
        return ' '.join(sentences)
    return ' '.join(sentences[:3] + ['...'] + sentences[-2:])

def format_output(text, fmt='text'):
    attendees = extract_attendees(text)
    actions = extract_actions(text)
    decisions = extract_decisions(text)
    questions = extract_questions(text)
    summary = summarize(text)

    if fmt == 'json':
        return json.dumps({
            'summary': summary,
            'attendees': attendees,
            'action_items': actions,
            'decisions': decisions,
            'questions': questions,
        }, indent=2)

    lines = [f"\n{'='*50}", "  MEETING SUMMARY", f"{'='*50}", ""]

    if attendees:
        lines.append(f"  Attendees: {', '.join(attendees)}")
        lines.append("")

    lines.extend(["  Summary:", f"  {summary}", ""])

    if decisions:
        lines.append("  Decisions:")
        for i, d in enumerate(decisions, 1):
            lines.append(f"    {i}. {d}")
        lines.append("")

    if actions:
        lines.append("  Action Items:")
        for i, a in enumerate(actions, 1):
            lines.append(f"    {i}. {a}")
        lines.append("")

    if questions:
        lines.append("  Open Questions:")
        for i, q in enumerate(questions, 1):
            lines.append(f"    {i}. {q}")

    lines.append(f"\n{'='*50}")
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['extract'])
    parser.add_argument('file', help='Transcript file')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')
    parser.add_argument('--followup', action='store_true', help='Generate follow-up email')
    args = parser.parse_args()

    text = Path(args.file).read_text()
    print(format_output(text, args.format))

if __name__ == '__main__':
    main()
