#!/usr/bin/env python3
"""Validate a Precog market spec against the skill safe rails, offline.

Runs before `forecast create market` preview. Fails fast with field-specific
errors. Exit 0 when the spec passes, exit 2 with one `field: reason` line per
failure on stderr. Prints `spec ok` on stdout when valid.

Safe rails (see workflows/create-precog-market.md):
- English only: question, resolution_criteria, and outcomes must be ASCII.
- Question under 40 chars, ends with `?`.
- 2+ outcomes, each 23 chars or fewer, no empties, no commas.
- resolution_criteria 40+ chars with a source signal and a fallback signal.
- Category uppercase, start < end, collateral a valid 0x address.

Usage:
  python validate_market_spec.py --spec market.yaml
"""
import argparse
import json
import os
import sys
from urllib.parse import urlparse

REQUIRED_KEYS = {
    'question',
    'resolution_criteria',
    'image_url',
    'category',
    'outcomes',
    'end_timestamp',
    'collateral_address',
}
MAX_QUESTION_LENGTH = 40
MAX_OUTCOME_LENGTH = 23
MIN_CRITERIA_LENGTH = 40
SOURCE_SIGNALS = ('http://', 'https://', 'www.', '.gov', '.com', '.org',
                  'official', 'website', 'announced', 'published',
                  'according to', 'based on')
FALLBACK_SIGNALS = ('cancel', 'postpone', 'void', 'default', 'no change',
                    'resolves to', 'resolve to')


def fail(errors, field, reason):
    # Register one field-specific failure for the final report.
    errors.append(f'{field}: {reason}')


def is_ascii(text):
    # English-only rail rejects any non-ASCII text outright.
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True


def check_question(data, errors):
    # Reject a missing or blank question before content checks.
    value = data.get('question')
    if not isinstance(value, str) or not value.strip():
        fail(errors, 'question', 'must be a non-empty string.')
        return
    question = value.strip()

    # English-only rail.
    if not is_ascii(question):
        fail(errors, 'question', 'must be English (ASCII only).')

    # Short card title ending with a question mark.
    if not question.endswith('?'):
        fail(errors, 'question', 'must end with a question mark.')
    if len(question) >= MAX_QUESTION_LENGTH:
        fail(errors, 'question',
             f'must be under {MAX_QUESTION_LENGTH} characters (got {len(question)}).')


def check_outcomes(data, errors):
    # Reject a missing outcomes field before label checks.
    value = data.get('outcomes')
    if isinstance(value, str):
        fail(errors, 'outcomes',
             'must be a list of labels, not a comma-separated string.')
        return
    if not isinstance(value, (list, tuple)):
        fail(errors, 'outcomes', 'must be a list of strings.')
        return

    # A market needs at least two selectable outcomes.
    if len(value) < 2:
        fail(errors, 'outcomes', 'must contain at least two outcomes.')

    # Validate each label before commas can split it server-side.
    for index, label in enumerate(value):
        field = f'outcomes[{index}]'
        if not isinstance(label, str) or not label.strip():
            fail(errors, field, 'must be a non-empty string.')
            continue
        text = label.strip()

        # English-only rail.
        if not is_ascii(text):
            fail(errors, field, 'must be English (ASCII only).')

        # Short display labels with no comma separators.
        if ',' in text:
            fail(errors, field, 'must not contain commas.')
        if len(text) > MAX_OUTCOME_LENGTH:
            fail(errors, field,
                 f'must not exceed {MAX_OUTCOME_LENGTH} characters (got {len(text)}).')


def check_criteria(data, errors):
    # Reject a missing or blank criteria before substance checks.
    value = data.get('resolution_criteria')
    if not isinstance(value, str) or not value.strip():
        fail(errors, 'resolution_criteria', 'must be a non-empty string.')
        return
    criteria = value.strip()

    # English-only rail.
    if not is_ascii(criteria):
        fail(errors, 'resolution_criteria', 'must be English (ASCII only).')

    # Criteria must spell out how the market resolves.
    if len(criteria) < MIN_CRITERIA_LENGTH:
        fail(errors, 'resolution_criteria',
             f'must be at least {MIN_CRITERIA_LENGTH} characters (got {len(criteria)}).')

    # Criteria must name the source that decides the outcome.
    lowered = criteria.lower()
    if not any(signal in lowered for signal in SOURCE_SIGNALS):
        fail(errors, 'resolution_criteria',
             'must name a source (URL or words like official, announced, based on).')

    # Criteria must state the fallback when the event does not happen.
    if not any(signal in lowered for signal in FALLBACK_SIGNALS):
        fail(errors, 'resolution_criteria',
             'must state a fallback (cancel, postpone, void, default outcome).')


def check_category(data, errors):
    # Reject a missing or blank category before case checks.
    value = data.get('category')
    if not isinstance(value, str) or not value.strip():
        fail(errors, 'category', 'must be a non-empty string.')
        return

    # Uppercase tokens only, single or comma-separated.
    for token in value.split(','):
        token = token.strip()
        if not token:
            fail(errors, 'category', 'must not contain empty tokens.')
        elif token != token.upper():
            fail(errors, 'category', f'token {token!r} must be uppercase.')


def check_image_url(data, errors):
    # Reject a missing or blank image before scheme checks.
    value = data.get('image_url')
    if not isinstance(value, str) or not value.strip():
        fail(errors, 'image_url', 'must be a non-empty string.')
        return
    parsed = urlparse(value.strip())

    # Accept http(s) or ipfs with a host (a bare CID counts as host).
    if parsed.scheme in ('http', 'https'):
        if not parsed.netloc:
            fail(errors, 'image_url', 'http(s) URL must have a host.')
    elif parsed.scheme == 'ipfs':
        if not (parsed.netloc or parsed.path.strip('/')):
            fail(errors, 'image_url', 'ipfs URL must have a host or CID.')
    else:
        fail(errors, 'image_url', 'must be http(s) or ipfs.')


def check_timestamps(data, errors):
    # Read both timestamps, defaulting start to now like the CLI.
    import time
    start = data.get('start_timestamp', int(time.time()))
    end = data.get('end_timestamp')

    # Both timestamps must be integers.
    for name, ts in (('start_timestamp', start), ('end_timestamp', end)):
        if isinstance(ts, bool) or not isinstance(ts, int):
            fail(errors, name, 'must be an integer (unix seconds).')

    # Start must precede end when both parsed.
    if (isinstance(start, int) and isinstance(end, int)
            and not isinstance(start, bool) and not isinstance(end, bool)
            and start >= end):
        fail(errors, 'start_timestamp', 'must be before end_timestamp.')


def check_collateral(data, errors):
    # YAML can parse an unquoted 0x address as an integer, like the CLI.
    value = data.get('collateral_address')
    if isinstance(value, int) and not isinstance(value, bool):
        if value < 0:
            fail(errors, 'collateral_address', 'must be an EVM address.')
            return
        address = f'0x{value:040x}'
    elif isinstance(value, str) and value.strip():
        address = value.strip()
    else:
        fail(errors, 'collateral_address', 'must be a non-empty string.')
        return

    # Format: 0x followed by exactly 40 hexadecimal characters.
    if len(address) != 42 or not address.startswith('0x'):
        fail(errors, 'collateral_address', 'must be a 0x address.')
        return
    try:
        int(address[2:], 16)
    except ValueError:
        fail(errors, 'collateral_address', 'must be hexadecimal.')


def load_spec(spec_path):
    # Resolve the path and read the file before format-specific parsing.
    if not os.path.exists(spec_path):
        raise RuntimeError(f'spec file not found: {spec_path}')
    with open(spec_path, encoding='utf-8') as f:
        text = f.read()

    # Parse by file extension, never guess from content.
    suffix = os.path.splitext(spec_path)[1].casefold()
    if suffix == '.json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f'spec is not valid JSON: {e}') from e
    if suffix in ('.yaml', '.yml'):
        try:
            import yaml
        except ImportError as e:
            raise RuntimeError('pyyaml is required for YAML specs.') from e
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise RuntimeError(f'spec is not valid YAML: {e}') from e
    raise RuntimeError('spec must use a .json, .yaml, or .yml extension.')


def validate(data):
    errors = []

    # Reject a non-mapping root before field checks.
    if not isinstance(data, dict):
        return ['spec: must be a mapping.']

    # Reject unknown keys so typos fail before a provider request.
    unknown = sorted(set(data) - REQUIRED_KEYS - {'start_timestamp'})
    for key in unknown:
        fail(errors, key, 'unknown field.')

    # Reject missing required keys with the full field list.
    missing = sorted(REQUIRED_KEYS - set(data))
    for key in missing:
        fail(errors, key, 'missing required field.')

    # Validate each present field, skipping missing ones already reported.
    checks = (
        ('question', check_question),
        ('resolution_criteria', check_criteria),
        ('image_url', check_image_url),
        ('category', check_category),
        ('outcomes', check_outcomes),
        ('collateral_address', check_collateral),
    )
    for key, check in checks:
        if key in data:
            check(data, errors)
    if 'end_timestamp' in data or 'start_timestamp' in data:
        check_timestamps(data, errors)
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    args = p.parse_args()

    try:
        data = load_spec(args.spec)
    except RuntimeError as e:
        print(f'spec: {e}', file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 2

    # Build and print the pass report on stdout only.
    print('spec ok')
    return 0


if __name__ == "__main__":
    sys.exit(main())
