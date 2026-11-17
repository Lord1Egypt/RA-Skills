#!/usr/bin/env python3
import json
import sys
import time
import requests
import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('prompt', help='Image prompt')
    parser.add_argument('--seed', type=int, default=None, help='Fixed seed (random otherwise)')
    parser.add_argument('--steps', type=int, default=5, help='Sampling steps')
    parser.add_argument('--output', default=None, help='Output PNG path')
    parser.add_argument('--host', default='localhost:8188', help='ComfyUI host:port')
    args = parser.parse_args()

    workflow_path = Path(__file__).parent.parent / 'workflows' / 'flux2.json'
    if not workflow_path.exists():
        raise FileNotFoundError(f'Workflow missing: {workflow_path}')

    # Load and modify workflow
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Set prompt
    workflow['76']['inputs']['value'] = args.prompt

    # Randomize or set seed
    import random
    seed = args.seed or int(random.randrange(sys.maxsize))
    workflow['77:73']['inputs']['noise_seed'] = seed

    # Optional steps
    workflow['77:62']['inputs']['steps'] = args.steps

    # Submit prompt
    url = f'http://{args.host}/prompt'
    resp = requests.post(url, json={'prompt': workflow})
    resp.raise_for_status()
    prompt_id = resp.json()['prompt_id']
    print(f'Submitted prompt_id: {prompt_id} (seed: {seed})')

    # Poll for completion
    history_url = f'http://{args.host}/history/{prompt_id}'
    while True:
        time.sleep(1)
        hist_resp = requests.get(history_url)
        hist_resp.raise_for_status()
        history = hist_resp.json()
        if prompt_id in history and history[prompt_id]['outputs']:
            break

    # Get image info from node 78 (SaveImage)
    outputs = history[prompt_id]['outputs']['85']
    if 'images' not in outputs or not outputs['images']:
        raise ValueError('No images in output')
    img_info = outputs['images'][0]
    filename = img_info['filename']
    subfolder = img_info['subfolder'] or 'output'
    print(f'Image ready: {filename} in {subfolder}')

    # Download image
    subfolder_path = img_info.get('subfolder', '')
    view_url = f'http://{args.host}/view?filename={filename}&type=output&subfolder={subfolder_path}'
    img_resp = requests.get(view_url)
    img_resp.raise_for_status()

    out_path = args.output or f'./gen-{seed}.jpg'
    with open(out_path, 'wb') as f:
        f.write(img_resp.content)
    print(f'Saved: {out_path}')
    return out_path

if __name__ == '__main__':
    main()