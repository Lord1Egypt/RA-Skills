#!/usr/bin/env python3
"""
Fetch completed job results from AiriLab.
"""

import json
import sys
from pathlib import Path

import requests

AIRILAB_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AIRILAB_PATH))

from core.paths import get_config_dir  # noqa: E402

CONFIG_DIR = get_config_dir()
TOKEN_FILE = CONFIG_DIR / '.env'
PROJECT_FILE = CONFIG_DIR / 'project_config.json'
RESULT_URL = 'https://cn.airilab.com/api/CrudRouters/getOneRecord'


def get_token():
    if not TOKEN_FILE.exists():
        return None

    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('AIRILAB_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None


def get_project_config():
    if not PROJECT_FILE.exists():
        return None

    try:
        with open(PROJECT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def fetch_result(job_id: str) -> dict:
    token = get_token()
    if not token:
        return {
            'success': False,
            'output_urls': [],
            'thumbnail_url': None,
            'toolset': None,
            'message': 'Missing token, please login first',
        }

    project = get_project_config()
    if not project:
        return {
            'success': False,
            'output_urls': [],
            'thumbnail_url': None,
            'toolset': None,
            'message': 'Missing project config',
        }

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'projectId': project.get('projectId', 0),
        'teamId': project.get('teamId', 0),
        'language': 'chs',
        'desiredGenerationId': job_id,
    }

    try:
        response = requests.post(RESULT_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        if result.get('status') != 200:
            return {
                'success': False,
                'output_urls': [],
                'thumbnail_url': None,
                'toolset': None,
                'message': f"API error: {result.get('message', 'Unknown')}",
            }

        data = result.get('data', {})
        models = data.get('projectGenerationModel', [])
        if not models:
            return {
                'success': False,
                'output_urls': [],
                'thumbnail_url': None,
                'toolset': None,
                'message': 'No generation model found',
            }

        model = models[0]
        medias = model.get('projectMedias', [])
        if not medias:
            return {
                'success': False,
                'output_urls': [],
                'thumbnail_url': None,
                'toolset': None,
                'message': 'No output media yet',
            }

        output_urls = [m.get('url', '') for m in medias if m.get('url')]
        thumbnail_url = output_urls[0] if output_urls else None

        workflow_name = model.get('workflowName', 'unknown')
        workflow_head = workflow_name.split()[0] if workflow_name else ''
        toolset_map = {
            'MJ': 'mj',
            'Upscale': 'upscale',
            'Trans': 'atmosphere',
        }

        return {
            'success': True,
            'output_urls': output_urls,
            'thumbnail_url': thumbnail_url,
            'toolset': toolset_map.get(workflow_head, 'unknown'),
            'message': f'Fetched {len(output_urls)} image(s)',
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'output_urls': [],
            'thumbnail_url': None,
            'toolset': None,
            'message': f'Network error: {str(e)}',
        }
    except Exception as e:
        return {
            'success': False,
            'output_urls': [],
            'thumbnail_url': None,
            'toolset': None,
            'message': f'Unexpected error: {str(e)}',
        }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch task result')
    parser.add_argument('--job-id', required=True, help='Task ID')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')

    args = parser.parse_args()
    result = fetch_result(args.job_id)

    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False))
    else:
        if result['success']:
            print(result['message'])
            print(f"tool: {result['toolset']}")
            for i, url in enumerate(result['output_urls'], 1):
                print(f'image{i}: {url}')
            print(f"thumbnail: {result['thumbnail_url']}")
        else:
            print(result['message'])

    sys.exit(0 if result['success'] else 1)
