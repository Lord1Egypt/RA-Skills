#!/usr/bin/env python3
"""
Code Spec Guardian — Lightweight Project Context Extractor

仅做两件事：
  1. 语言检测（读顶层标志文件）
  2. 提取关键配置文件片段

不遍历源码树，不 glob 文件列表。核心分析交给模型。

Usage:
    python3 analyze_project.py <project_path> [-o output.json]
"""
import json, os, sys, argparse
from pathlib import Path

MAX_BYTES = 4096

def read_head(path, n=4096):
    try:
        with open(path, encoding='utf-8-sig', errors='replace') as f:
            return f.read(n)
    except Exception:
        return None

def detect(root: Path):
    """只读顶层 files 检测语言和框架，不做子目录遍历。"""
    top = {f.name for f in root.iterdir() if f.is_file()}
    all_dirs = {f.name for f in root.iterdir() if f.is_dir()}

    lang, fw = [], []

    # Node
    pj = root / 'package.json'
    if pj.exists():
        lang.append('node')
        try:
            pkg = json.loads(read_head(pj, 32768))
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
            dep_names = list(deps.keys())
            for kw, name in [('vue', 'Vue'), ('react', 'React'), ('next', 'Next.js'),
                             ('nuxt', 'Nuxt'), ('svelte', 'Svelte'), ('angular', 'Angular'),
                             ('express', 'Express'), ('fastify', 'Fastify'), ('nestjs', 'NestJS'),
                             ('element-plus', 'Element Plus'), ('antd', 'Ant Design'),
                             ('unocss', 'UnoCSS'), ('tailwindcss', 'Tailwind'),
                             ('pinia', 'Pinia'), ('zustand', 'Zustand'),
                             ('echarts', 'ECharts'), ('vite', 'Vite'),
                             ('wujie', 'Wujie')]:
                if kw in dep_names:
                    fw.append(name)
        except Exception:
            pass

    # Python
    if any(f in top for f in ['pyproject.toml', 'setup.py', 'requirements.txt', 'Pipfile']):
        lang.append('python')

    # Java
    if any(f in top for f in ['pom.xml', 'build.gradle', 'build.gradle.kts']):
        lang.append('java')
        pom = root / 'pom.xml'
        if pom.exists():
            c = (read_head(pom) or '').lower()
            if 'spring-boot' in c: fw.append('Spring Boot')
            if 'mybatis' in c: fw.append('MyBatis')

    # Go
    if 'go.mod' in top:
        lang.append('go')
        c = read_head(root / 'go.mod') or ''
        for kw, name in [('gin-gonic', 'Gin'), ('echo', 'Echo'), ('fiber', 'Fiber'), ('beego', 'Beego')]:
            if kw in c: fw.append(name)

    # Rust
    if 'Cargo.toml' in top:
        lang.append('rust')

    # PHP
    if 'composer.json' in top:
        lang.append('php')

    return {'languages': lang, 'frameworks': fw}

def extract_configs(root: Path):
    """只读顶层关键配置文件，返回片段。"""
    cfgs = {}
    # 前端 / Node.js
    for name in ['package.json', '.prettierrc', '.prettierrc.json', '.editorconfig',
                 'eslint.config.ts', 'eslint.config.js', '.eslintrc.js', '.eslintrc.cjs',
                 'tsconfig.json', 'vite.config.ts', 'vite.config.js',
                 'uno.config.ts', 'uno.config.js',
                 'tailwind.config.js', 'tailwind.config.ts',
                 'postcss.config.js', 'postcss.config.ts',
                 '.gitignore']:
        fp = root / name
        if fp.exists():
            cfgs[name] = read_head(fp, MAX_BYTES)
    # Python
    for name in ['pyproject.toml', 'setup.cfg', 'requirements.txt']:
        fp = root / name
        if fp.exists():
            cfgs[name] = read_head(fp, MAX_BYTES)
    # Java
    for name in ['pom.xml', 'build.gradle', 'build.gradle.kts']:
        fp = root / name
        if fp.exists():
            cfgs[name] = read_head(fp, MAX_BYTES)
    # Go
    fp = root / 'go.mod'
    if fp.exists():
        cfgs['go.mod'] = read_head(fp, MAX_BYTES)
    # Rust
    fp = root / 'Cargo.toml'
    if fp.exists():
        cfgs['Cargo.toml'] = read_head(fp, MAX_BYTES)
    # PHP
    fp = root / 'composer.json'
    if fp.exists():
        cfgs['composer.json'] = read_head(fp, MAX_BYTES)
    return cfgs

def main():
    ap = argparse.ArgumentParser(description='Code Spec Guardian — Lightweight Context Extractor')
    ap.add_argument('project_path')
    ap.add_argument('-o', '--output', default=None)
    args = ap.parse_args()

    root = Path(args.project_path).resolve()
    if not root.exists():
        print(f'ERROR: {args.project_path} not found', file=sys.stderr)
        sys.exit(1)

    out = {
        'project_path': str(root),
        **detect(root),
        'configs': extract_configs(root),
    }

    output_path = Path(args.output) if args.output else root / '.code-spec' / 'project_context.json'
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f'  Done → {output_path}')
    print(f'  Languages: {", ".join(out["languages"]) or "unknown"} | Frameworks: {", ".join(out["frameworks"]) or "none"}')

if __name__ == '__main__':
    main()
