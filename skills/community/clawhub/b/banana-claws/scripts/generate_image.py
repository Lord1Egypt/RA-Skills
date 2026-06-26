#!/usr/bin/env python3
import argparse
import base64
import json
import os
import pathlib
import re
import sys
from typing import Any, List
from urllib.parse import urlparse

import requests


def _needs_clarification(prompt: str) -> list[str]:
    text = prompt.lower()
    hints: list[str] = []

    if not re.search(r"\b(\d{3,4}x\d{3,4}|thumbnail|banner|poster|icon|avatar|wallpaper|og|social)\b", text):
        hints.append("Output format/size is unclear. Add target like 'thumbnail 1280x720' or 'OG 1280x640'.")

    if not re.search(r"\b(cinematic|pixel|8-bit|vector|realistic|anime|watercolor|cyberpunk|minimal|gritty|retro|flat)\b", text):
        hints.append("Style is unclear. Add style keywords (e.g., cinematic, pixel-art, flat vector).")

    if re.search(r"\b(text|title|headline|logo|wordmark)\b", text) and not re.search(r"['\"“”][^'\"“”]{2,}['\"“”]", prompt):
        hints.append("Text rendering requested but exact copy is missing. Put required text in quotes.")

    if not re.search(r"\b(high contrast|readable|legible|safe area|centered|negative space)\b", text):
        hints.append("Composition constraints are vague. Consider adding readability/composition constraints.")

    return hints


def _read_baseline_as_data_url(path_or_url: str, *, max_mb: int, allow_local: bool, require_workspace_local: bool, workspace_root: str) -> str:
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        parsed = urlparse(path_or_url)
        if parsed.scheme not in ('http', 'https'):
            raise ValueError('Only http/https baseline URLs are allowed')
        return path_or_url

    if not allow_local:
        raise ValueError('Local baseline path upload blocked. Re-run with --confirm-external-upload for local files.')

    p = pathlib.Path(path_or_url).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f'Baseline image not found: {path_or_url}')
    if not p.is_file() or p.is_symlink():
        raise ValueError('Baseline must be a regular non-symlink file')

    allowed = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}
    suffix = p.suffix.lower()
    if suffix not in allowed:
        raise ValueError('Baseline extension not allowed. Use png/jpg/jpeg/webp')

    if require_workspace_local:
        root = pathlib.Path(workspace_root).expanduser().resolve()
        try:
            p.relative_to(root)
        except Exception:
            raise ValueError(f'Baseline path must be under workspace root: {root}')

    size = p.stat().st_size
    if size > max_mb * 1024 * 1024:
        raise ValueError(f'Baseline file too large ({size} bytes), max is {max_mb}MB')

    b = p.read_bytes()
    return f"data:{allowed[suffix]};base64," + base64.b64encode(b).decode('ascii')


def _detect_edit_intent(prompt: str) -> bool:
    text = prompt.lower()
    patterns = [
        r"\b(edit|modify|revise|iterate|variant|variation|based on|from this|use this|same but|keep same|preserve)\b",
        r"\b(attached|attachment|reference image|foundational image|baseline image)\b",
    ]
    return any(re.search(p, text) for p in patterns)


def _apply_baseline_rails(args: argparse.Namespace) -> tuple[argparse.Namespace, list[str]]:
    applied: list[str] = []
    if args.baseline_image:
        if not args.variation_strength:
            args.variation_strength = 'low'
            applied.append('variation_strength=low')
        if not args.lock_palette:
            args.lock_palette = True
            applied.append('lock_palette=true')
        if not args.lock_composition:
            args.lock_composition = True
            applied.append('lock_composition=true')
    return args, applied


def _build_variant_constraint_text(args: argparse.Namespace) -> str:
    lines: List[str] = []
    if args.baseline_image:
        lines.append('Use the provided baseline image as the primary composition anchor.')
    if args.variation_strength:
        lines.append(f'Variation strength: {args.variation_strength}.')
    if args.lock_palette:
        lines.append('Lock color palette close to baseline.')
    if args.lock_composition:
        lines.append('Lock composition/layout close to baseline.')
    if args.must_keep:
        lines.append('Must-keep elements: ' + '; '.join(args.must_keep))
    return '\n'.join(lines)


def _extract_image_data_url(first: Any) -> str | None:
    if not isinstance(first, dict):
        return None
    data_url = None
    if isinstance(first.get('image_url'), dict):
        data_url = first['image_url'].get('url')
    if not data_url and isinstance(first.get('imageUrl'), dict):
        data_url = first['imageUrl'].get('url')
    if not data_url:
        data_url = first.get('url')
    return data_url


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--prompt', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--model', default='openai/gpt-5-image')
    p.add_argument('--image-size', choices=['low', 'medium', 'high'], default='', help='Model-dependent quality/size tier for iterative vs final passes')
    p.add_argument('--clarify-hints', action='store_true', help='Print prompt-clarification hints before generation')
    p.add_argument('--strict-clarify', action='store_true', help='Fail fast if prompt appears ambiguous for production-style tasks')
    p.add_argument('--baseline-image', default='', help='Path/URL to baseline image for locked variants')
    p.add_argument('--baseline-source-kind', choices=['current_attachment', 'reply_attachment', 'explicit_path_or_url'], default='', help='How baseline was resolved by caller')
    p.add_argument('--variation-strength', choices=['low', 'medium', 'high'], default='')
    p.add_argument('--must-keep', action='append', default=[], help='Repeatable constraint for required elements')
    p.add_argument('--lock-palette', action='store_true')
    p.add_argument('--lock-composition', action='store_true')
    p.add_argument('--output-format', choices=['path', 'json'], default='path')
    p.add_argument('--save-response-json', default='', help='Optional path to write full provider response JSON')
    p.add_argument('--require-baseline-for-edit-intent', action='store_true', default=True)
    p.add_argument('--allow-no-baseline-on-edit-intent', action='store_true', help='Disable fail-fast baseline requirement for edit-like prompts')
    p.add_argument('--confirm-external-upload', action='store_true', help='Required to upload a local baseline file to provider')
    p.add_argument('--max-baseline-mb', type=int, default=10, help='Maximum local baseline file size in MB')
    p.add_argument('--require-workspace-local-baseline', action='store_true', default=True, help='Require local baseline path to be under workspace root')
    p.add_argument('--workspace-root', default='/home/brad/.openclaw/workspace', help='Workspace root used for local baseline path safety')
    args = p.parse_args()

    key = os.getenv('OPENROUTER_API_KEY')
    if not key:
        print('OPENROUTER_API_KEY is not set', file=sys.stderr)
        return 2

    if args.allow_no_baseline_on_edit_intent:
        args.require_baseline_for_edit_intent = False

    clarify = _needs_clarification(args.prompt)
    if args.clarify_hints and clarify:
        for h in clarify:
            print(f'CLARIFY_HINT: {h}', file=sys.stderr)

    if args.strict_clarify and clarify:
        print('Prompt requires clarification before generation:', file=sys.stderr)
        for h in clarify:
            print(f'- {h}', file=sys.stderr)
        return 3

    edit_intent_detected = _detect_edit_intent(args.prompt)
    if edit_intent_detected and args.require_baseline_for_edit_intent and not args.baseline_image:
        print('Edit/variant intent detected but no baseline image was provided. Resolve baseline using policy: current attachment > replied-message attachment > clarify request.', file=sys.stderr)
        return 4

    if args.baseline_image and not args.baseline_source_kind:
        args.baseline_source_kind = 'explicit_path_or_url'

    args, rails_applied = _apply_baseline_rails(args)

    extra_constraints = _build_variant_constraint_text(args)
    final_prompt = args.prompt if not extra_constraints else f"{args.prompt}\n\n{extra_constraints}"

    if args.baseline_image:
        try:
            img_url = _read_baseline_as_data_url(
                args.baseline_image,
                max_mb=args.max_baseline_mb,
                allow_local=args.confirm_external_upload,
                require_workspace_local=args.require_workspace_local_baseline,
                workspace_root=args.workspace_root,
            )
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 2
        content: Any = [
            {'type': 'text', 'text': final_prompt},
            {'type': 'image_url', 'image_url': {'url': img_url}},
        ]
    else:
        content = final_prompt

    payload: dict[str, Any] = {
        'model': args.model,
        'messages': [{'role': 'user', 'content': content}],
        'modalities': ['image', 'text'],
    }
    if args.image_size:
        payload['image_size'] = args.image_size

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }

    r = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, data=json.dumps(payload), timeout=180)
    if r.status_code >= 300:
        print(f'Generation failed: {r.status_code} {r.text[:500]}', file=sys.stderr)
        return 1

    data = r.json()

    if args.save_response_json:
        save_path = pathlib.Path(args.save_response_json)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

    choices = data.get('choices') or []
    if not choices:
        print('No choices returned', file=sys.stderr)
        return 1

    msg = (choices[0] or {}).get('message') or {}
    images = msg.get('images') or msg.get('image') or []
    if isinstance(images, dict):
        images = [images]
    if not images:
        print(f'No images found in response message: keys={list(msg.keys())}', file=sys.stderr)
        return 1

    first = images[0]
    data_url = _extract_image_data_url(first)
    if not data_url:
        print('Unsupported image payload shape', file=sys.stderr)
        return 1

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if data_url.startswith('data:image') and 'base64,' in data_url:
        b64 = data_url.split('base64,', 1)[1]
        out.write_bytes(base64.b64decode(b64))
    elif data_url.startswith('http://') or data_url.startswith('https://'):
        img = requests.get(data_url, timeout=180)
        img.raise_for_status()
        out.write_bytes(img.content)
    else:
        print('Unknown image URL format', file=sys.stderr)
        return 1

    result = {
        'out': str(out),
        'provider_generation_id': data.get('id'),
        'provider_model': data.get('model'),
        'provider_created': data.get('created'),
        'provider_usage': data.get('usage'),
        'provider_response': data,
        'edit_intent_detected': edit_intent_detected,
        'baseline_applied': bool(args.baseline_image),
        'baseline_source': args.baseline_image or '',
        'baseline_source_kind': args.baseline_source_kind or '',
        'baseline_resolution_policy': 'current_attachment>reply_attachment>clarify',
        'rails_applied': rails_applied,
        'clarify_hints': clarify,
    }

    if args.output_format == 'json':
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(str(out))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
