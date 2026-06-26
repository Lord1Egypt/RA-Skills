#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_runtime(skill_dir: Path):
    runtime_path = skill_dir / 'config' / 'runtime.json'
    if runtime_path.exists():
        try:
            return json.loads(runtime_path.read_text(encoding='utf-8'))
        except Exception:
            pass
    example_path = skill_dir / 'config' / 'runtime.example.json'
    return json.loads(example_path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', default='1024x1792')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--prompt-file', default='')
    parser.add_argument('--prompt-text', default='')
    parser.add_argument('--requirement-text', default='')
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    runtime = load_runtime(skill_dir)
    cfg = runtime.get('image_generation', {})
    mode = cfg.get('mode', 'direct_prompt')
    size = cfg.get('size', args.size)
    count = int(cfg.get('count', args.count))

    prompt_text = (args.prompt_text or '').strip()
    if (not prompt_text) and args.prompt_file:
        p = Path(args.prompt_file)
        if p.exists():
            prompt_text = p.read_text(encoding='utf-8').strip()

    if not prompt_text:
        prompt_text = (
            '围绕楼盘主文案生成营销主图：画面必须与当日文案和热点角度直接相关，'
            '包含1-3位人物与具体生活情境（如看房、归家、亲子、会客），'
            '体现“故事瞬间”而非空镜头风景，保留真实摄影质感。'
        )

    requirement_text = (
        (args.requirement_text or '').strip()
        or (cfg.get('requirement_text', '') or '').strip()
        or (
            '画面与文案同主题；允许人物、互动和故事动作；'
            '允许在图中加入简洁中文标题/短句；避免无关风景空镜头；'
            '不要添加外部品牌logo或平台水印。'
        )
    )

    direct_message = (
        f"给我生成图片。\n"
        f"{prompt_text}\n"
        f"尺寸：{size}\n"
        f"张数：{count}\n"
        f"要求：{requirement_text}"
    )

    result = {
        'ok': True,
        'mode': mode,
        'size': size,
        'count': count,
        'direct_message': direct_message,
        'direct_prefix': '给我生成图片。',
        'requirement_text': requirement_text,
        'fallback_notice': '若当前本地大模型未成功出图，则保留主图提示词、备选图提示词、负面词，并提示用户可直接发给豆包生成图片。'
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
