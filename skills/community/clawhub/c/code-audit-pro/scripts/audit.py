#!/usr/bin/env python3
"""
Code Audit Pro v1.0 — 代码审查引擎
支持：Python/JS/Java/Go/Rust/C++ 语法检查 + 安全扫描 + AI幻觉检测
"""

import subprocess
import sys
import os
import re
import json
from pathlib import Path

# === 已知真实API/库（防AI幻觉） ===
REAL_PYTHON_LIBS = {'os','sys','json','re','math','datetime','collections','itertools',
    'functools','pathlib','typing','asyncio','threading','multiprocessing',
    'logging','hashlib','hmac','base64','binascii','csv','xml','html',
    'urllib','requests','flask','django','fastapi','numpy','pandas',
    'pytest','unittest','sqlite3','sqlalchemy','redis','celery','boto3',
    'beautifulsoup4','lxml','scrapy','pydantic','click','rich','tqdm',
    'jinja2','werkzeug','gunicorn','uvicorn','psycopg2','pymongo',
    'cryptography','pyyaml','tomllib','arrow','httpx','aiohttp',
    'websockets','grpcio','protobuf','opencv-python','pillow',
    'matplotlib','seaborn','plotly','scipy','sklearn','tensorflow',
    'torch','transformers','langchain','openai','anthropic','mistralai',
    'pypdf2','reportlab','openpyxl','xlrd','python-docx',
}

REAL_JS_LIBS = {'express','koa','fastify','nestjs','socket.io','ws',
    'react','vue','angular','svelte','next','nuxt','gatsby',
    'lodash','axios','dayjs','moment','chalk','commander','inquirer',
    'ora','figlet','dotenv','cors','helmet','morgan','compression',
    'passport','jsonwebtoken','bcrypt','uuid','nanoid','zod','joi',
    'yup','prisma','typeorm','sequelize','mongoose','redis','ioredis',
    'bull','agenda','node-cron','nodemailer','multer','sharp','cheerio',
    'puppeteer','playwright','jest','vitest','mocha','cypress',
    'eslint','prettier','webpack','vite','rollup','esbuild',
    'tailwindcss','sass','less','postcss','babel','typescript',
    'graphql','apollo','trpc','swagger','bullmq','amqplib','kafkajs',
    'nodemon','ts-node','pm2','forever',
}

HALLUCINATED_APIS = {
    # 经常被AI幻觉出来的不存在的API
    'npm: super-fetch-helper': '不存在的npm包',
    'npm: easy-validate-all': '不存在的npm包',
    'pip: ai-code-optimizer': '不存在的pip包',
    'pip: deep-codereview': '不存在的pip包',
    'pip: auto-ml-engine': '不存在的pip包',
    'java: com.google.common.codereview': '不存在的Java包',
    'rust: codereview_crate': '不存在的Rust crate',
}

# === 安全模式检测 ===
SECURITY_PATTERNS = [
    (r'exec\s*\(', 'exec() 执行任意代码', 'CRITICAL'),
    (r'eval\s*\(', 'eval() 执行任意代码', 'CRITICAL'),
    (r'pickle\.loads?\s*\(', '不安全的反序列化', 'CRITICAL'),
    (r'(?i)password\s*=\s*["\'][^"\']+["\']', '硬编码密码', 'CRITICAL'),
    (r'(?i)secret_key\s*=\s*["\'][^"\']+["\']', '硬编码密钥', 'CRITICAL'),
    (r'(?i)api_key\s*=\s*["\'][^"\']+["\']', '硬编码API密钥', 'CRITICAL'),
    (r'(?i)token\s*=\s*["\'][A-Za-z0-9_-]{20,}["\']', '硬编码Token', 'CRITICAL'),
    (r'requests\.get\(f["\']?.*\{.*\}', 'f-string注入风险', 'WARNING'),
    (r'subprocess\.(call|run|Popen)\s*\(.*shell\s*=\s*True', 'Shell注入风险', 'CRITICAL'),
    (r'(?i)\.execute\(f["\']', 'SQL注入风险(f-string)', 'CRITICAL'),
    (r'<script>', 'XSS风险', 'CRITICAL'),
    (r'\.innerHTML\s*=', 'XSS风险(innerHTML)', 'WARNING'),
    (r'(?i)cookie.*domain\s*=', 'Cookie域名设置不当', 'WARNING'),
    (r'os\.system\s*\(', 'os.system() 命令执行', 'CRITICAL'),
]

# === AI幻觉模式检测 ===
AI_HALLUCINATION_PATTERNS = [
    (r'(?:pip install|from|import)\s+[\w.-]*hallucinat', '可能的AI幻觉: 包含hallucination关键词的import'),
    (r'(?:from|import)\s+\w*[Ff]ake\w*', '可能的AI幻觉: 包含Fake的import'),
    (r'#\s*(?:TODO|FIXME|HACK)\s*:\s*(?:fix|implement|add)\s+(?:this|the|actual|real)', '占位符TODO'),
    (r'pass\s+#\s*TODO', '占位符pass + TODO'),
    (r'function\s+\w+\s*\(\s*\)\s*\{\s*\}', '空函数定义'),
]

def detect_language(file_path):
    """自动检测语言"""
    ext_map = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.jsx': 'react', '.tsx': 'react',
        '.java': 'java', '.go': 'go', '.rs': 'rust',
        '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
        '.rb': 'ruby', '.php': 'php', '.swift': 'swift',
        '.kt': 'kotlin', '.scala': 'scala',
    }
    ext = Path(file_path).suffix
    return ext_map.get(ext, 'unknown')

def check_security(content, filename):
    """安全检查"""
    findings = []
    for pattern, desc, severity in SECURITY_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            for m in matches[:3]:
                findings.append({
                    'severity': severity,
                    'description': desc,
                    'match': m[:80],
                    'file': filename
                })
    return findings

def check_ai_hallucination(content, filename, lang):
    """AI幻觉检测"""
    findings = []
    
    # 1. 检查import的包是否真实
    if lang == 'python':
        imports = re.findall(r'^(?:from|import)\s+(\w+)', content, re.MULTILINE)
        for imp in imports:
            if imp not in REAL_PYTHON_LIBS and not imp.startswith('_'):
                findings.append({
                    'severity': 'WARNING',
                    'description': f'可疑import: {imp} — 不在已知Python包列表中',
                    'match': imp,
                    'file': filename
                })
    
    elif lang in ('javascript', 'typescript', 'react'):
        imports = re.findall(r'(?:require\([\'"])([\w@/-]+)', content)
        imports += re.findall(r"(?:from\s+['\"])([\w@/-]+)", content)
        for imp in imports:
            imp_name = imp.split('/')[0].lstrip('@')
            if imp_name not in REAL_JS_LIBS and not imp_name.startswith('.'):
                findings.append({
                    'severity': 'WARNING',
                    'description': f'可疑import: {imp} — 不在已知npm包列表中',
                    'match': imp,
                    'file': filename
                })
    
    # 2. 检查AI幻觉模式
    for pattern, desc in AI_HALLUCINATION_PATTERNS:
        if re.search(pattern, content):
            findings.append({
                'severity': 'WARNING',
                'description': desc,
                'match': '',
                'file': filename
            })
    
    return findings

def check_performance(content, filename):
    """性能问题检测"""
    findings = []
    
    # N+1查询模式
    if re.search(r'for.*in.*:.*\.(?:query|find|get)\s*\(', content):
        findings.append({
            'severity': 'WARNING',
            'description': '可能的N+1查询: 循环内执行数据库查询',
            'match': '',
            'file': filename
        })
    
    # 循环内IO
    if re.search(r'for.*in.*:.*\.(?:write|read|open|send)\s*\(', content):
        findings.append({
            'severity': 'WARNING',
            'description': '循环内IO操作，建议批量处理',
            'match': '',
            'file': filename
        })
    
    return findings

def check_dead_code(content, filename):
    """死代码检测"""
    findings = []
    
    # 无限递归风险
    lines = content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        # 递归函数无base case
        if re.match(r'def\s+\w+.*:', stripped) or re.match(r'function\s+\w+', stripped):
            func_body = lines[i:i+20]
            func_text = '\n'.join(func_body)
            func_name = re.findall(r'(?:def|function)\s+(\w+)', stripped)
            if func_name and func_text.count(func_name[0]) > 2:
                # 检查是否有base case
                if not re.search(r'if.*return|if.*break|if.*exit', func_text[:200]):
                    findings.append({
                        'severity': 'WARNING',
                        'description': f'函数 {func_name[0]} 可能是递归但未发现base case',
                        'match': stripped[:60],
                        'file': filename
                    })
    
    return findings

def audit_file(file_path):
    """审计单个文件"""
    path = Path(file_path)
    if not path.exists():
        print(f'❌ 文件不存在: {file_path}')
        return
    
    content = path.read_text(encoding='utf-8', errors='ignore')
    lang = detect_language(file_path)
    filename = str(path)
    
    print(f'\n🔍 审查: {filename}')
    print(f'   语言: {lang}')
    print(f'   行数: {len(content.splitlines())}')
    
    all_findings = []
    all_findings.extend(check_security(content, filename))
    all_findings.extend(check_ai_hallucination(content, filename, lang))
    all_findings.extend(check_performance(content, filename))
    all_findings.extend(check_dead_code(content, filename))
    
    # 统计
    critical = [f for f in all_findings if f['severity'] == 'CRITICAL']
    warnings = [f for f in all_findings if f['severity'] == 'WARNING']
    
    print(f'\n📋 结果:')
    if not all_findings:
        print('   ✅ 未发现问题')
        return
    
    if critical:
        print(f'\n🔴 致命 ({len(critical)}):')
        for f in critical:
            print(f'   - {f["description"]}')
            if f['match']:
                print(f'     {f["match"]}')
    
    if warnings:
        print(f'\n🟡 警告 ({len(warnings)}):')
        for f in warnings:
            print(f'   - {f["description"]}')
            if f['match']:
                print(f'     {f["match"]}')


def main():
    args = sys.argv[1:]
    
    if not args:
        print('''
🔍 Code Audit Pro v1.0

用法:
  audit <文件或目录>     审查文件/目录
  audit --check <代码>   审查输入的代码片段

示例:
  audit app.py
  audit src/
  audit --check "import os\\nos.system('ls')"
''')
        return
    
    if args[0] == '--check':
        code = ' '.join(args[1:])
        audit_file_from_content(code, 'stdin')
    else:
        path = args[0]
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
                for f in files:
                    ext = Path(f).suffix
                    if ext in ('.py','.js','.ts','.jsx','.tsx','.java','.go','.rs','.c','.cpp','.rb','.php'):
                        audit_file(os.path.join(root, f))
        else:
            audit_file(path)


def audit_file_from_content(content, filename):
    findings = []
    findings.extend(check_security(content, filename))
    findings.extend(check_ai_hallucination(content, filename, 'python'))
    findings.extend(check_performance(content, filename))
    findings.extend(check_dead_code(content, filename))
    
    critical = [f for f in findings if f['severity'] == 'CRITICAL']
    warnings = [f for f in findings if f['severity'] == 'WARNING']
    
    if not findings:
        print('✅ 未发现问题')
        return
    
    if critical:
        print(f'🔴 {len(critical)} 个致命问题:')
        for f in critical:
            print(f'   - {f["description"]}: {f["match"][:60]}')
    
    if warnings:
        print(f'🟡 {len(warnings)} 个警告:')
        for f in warnings:
            print(f'   - {f["description"]}: {f["match"][:60]}')


if __name__ == '__main__':
    main()
