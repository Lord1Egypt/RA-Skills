#!/usr/bin/env python3
"""报告脚手架 — 一键创建报告目录结构

用法:
  python3 init.py "报告名称"                        # 默认 executive-summary 模板
  python3 init.py "报告名称" --template decision-memo  # 指定模板
  python3 init.py "报告名称" --dir /path/to/reports     # 指定输出目录
"""
import sys, json, argparse, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = {
    'executive-summary': 'templates/executive-summary.md',
    'decision-memo': 'templates/decision-memo.md',
    'one-pager': 'templates/one-pager.md',
    'board-briefing': 'templates/board-briefing.md',
}


def main():
    p = argparse.ArgumentParser(description='报告脚手架 — 一键创建报告目录')
    p.add_argument('name', help='报告名称')
    p.add_argument('--template', '-t', choices=list(TEMPLATES.keys()),
                   default='executive-summary', help='模板类型')
    p.add_argument('--dir', '-d', default='reports', help='输出根目录')
    args = p.parse_args()

    # 创建目录
    report_dir = Path(args.dir) / args.name
    if report_dir.exists():
        print(f'错误：目录已存在 {report_dir}', file=sys.stderr)
        sys.exit(1)
    report_dir.mkdir(parents=True)
    (report_dir / 'appendix').mkdir()

    # 复制模板
    template_src = SKILL_DIR / TEMPLATES[args.template]
    if not template_src.exists():
        print(f'错误：模板不存在 {template_src}', file=sys.stderr)
        sys.exit(1)

    template_content = template_src.read_text(encoding='utf-8')
    # 替换占位符
    template_content = template_content.replace('{报告标题}', args.name)
    template_content = template_content.replace('YYYY-MM-DD',
                                                datetime.now(CST).strftime('%Y-%m-%d'))

    report_file = report_dir / f'01-{args.name}-v1.0.0.md'
    report_file.write_text(template_content, encoding='utf-8')

    # 创建 version.json
    version_data = {
        'version': '1.0.0',
        'releaseDate': datetime.now(CST).strftime('%Y-%m-%d'),
        'author': 'report-builder V2.0',
        'template': args.template,
        'changes': ['V1.0.0: 初始版本']
    }
    (report_dir / 'version.json').write_text(
        json.dumps(version_data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')

    # 创建 VERSION.md
    version_md = f"""# {args.name} — 版本历史

| 版本 | 日期 | 变更 | 作者 |
|------|------|------|------|
| V1.0.0 | {datetime.now(CST).strftime('%Y-%m-%d')} | 初始版本 | report-builder V2.0 |
"""
    (report_dir / 'VERSION.md').write_text(version_md, encoding='utf-8')

    # 创建 README.md 索引
    readme = f"""# {args.name} — 报告索引

| 文件 | 版本 | 状态 |
|------|------|------|
| [{report_file.name}](./{report_file.name}) | V1.0.0 | 初稿 |
"""
    (report_dir / 'README.md').write_text(readme, encoding='utf-8')

    print(f'✅ 报告已创建：{report_dir}')
    print(f'   模板：{args.template}')
    print(f'   文件：{report_file.relative_to(Path.cwd())}')
    print(f'   版本：V1.0.0')


if __name__ == '__main__':
    main()
