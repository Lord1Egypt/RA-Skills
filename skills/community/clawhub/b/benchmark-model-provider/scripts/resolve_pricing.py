#!/usr/bin/env python3
import argparse
import json

PRICING = {
    'cliproxy/gpt-5.4': {'input_per_million': 10.0, 'output_per_million': 30.0, 'confidence': 'near-match-estimate'},
    'cliproxy/gpt-5.4-mini': {'input_per_million': 2.0, 'output_per_million': 8.0, 'confidence': 'near-match-estimate'},
    'cliproxy/gpt-5.3-codex': {'input_per_million': 5.0, 'output_per_million': 15.0, 'confidence': 'near-match-estimate'},
    'cliproxy/claude-sonnet-4-6': {'input_per_million': 3.0, 'output_per_million': 15.0, 'confidence': 'near-match-estimate'},
    'cliproxy/claude-opus-4-6-thinking': {'input_per_million': 15.0, 'output_per_million': 75.0, 'confidence': 'near-match-estimate'},
    'cliproxy/gemini-3.1-pro-high': {'input_per_million': 7.0, 'output_per_million': 21.0, 'confidence': 'near-match-estimate'},
    'cliproxy/gemini-3.1-pro-low': {'input_per_million': 3.5, 'output_per_million': 10.5, 'confidence': 'near-match-estimate'},
}


def resolve(model: str):
    if model in PRICING:
        data = PRICING[model].copy()
        data['model'] = model
        data['source'] = 'built-in pricing map'
        return data
    return {
        'model': model,
        'input_per_million': 1.0,
        'output_per_million': 3.0,
        'confidence': 'local-estimate' if '/' not in model else 'unknown',
        'source': 'fallback estimate',
    }


def main():
    ap = argparse.ArgumentParser(description='Resolve pricing for model ids')
    ap.add_argument('models', nargs='+')
    args = ap.parse_args()
    print(json.dumps([resolve(m) for m in args.models], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
