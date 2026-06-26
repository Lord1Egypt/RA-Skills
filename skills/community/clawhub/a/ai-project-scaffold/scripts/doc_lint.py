#!/usr/bin/env python3
"""
文档规范检查器 —— 铁律的代码化 enforcement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
扫描项目中所有 .md/.yaml 文档，自动检测：
  - 重复内容（跨文件相似度 > 70%）
  - 超字数文件
  - 模糊命名（final/new/latest/draft/temp）
  - 空模板（生成后未填写）
  - 非约定文件名（随意命名的野文档）

用法:
  python3 doc_lint.py --name MyProject [--output .]
  python3 doc_lint.py --name MyProject --strict       # 严格模式，重复内容报错
  python3 doc_lint.py --name MyProject --fix           # 自动标记可疑文件
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 规则定义
# ═══════════════════════════════════════════════════════════════

# 允许的文件名（白名单）
ALLOWED_FILES = {
    # 根目录
    "README.md", ".gitignore", "_project_config.yaml",
    # 01_data
    "01_data/README.md", "01_data/04_quality_log.md",
    # 02_tokenization
    "02_tokenization/README.md", "02_tokenization/05_generated/README.md",
    # 03_models
    "03_models/README.md",
    # 04_experiments
    "04_experiments/experiment_log.md",
    # 06_shared
    "06_shared/README.md", "06_shared/configs/README.md",
    # configs
    "06_shared/configs/training/deepspeed_zero2.yaml",
    "06_shared/configs/training/deepspeed_zero3.yaml",
    "06_shared/configs/training/lora_config.yaml",
    "06_shared/configs/training/qlora_config.yaml",
    "06_shared/configs/training/wandb_config.yaml",
}

# 允许的命名模式（正则）
ALLOWED_PATTERNS = [
    r"01_data/01_raw/source_.+/metadata\.yaml$",
    r"01_data/02_qc/reports/qc_report_.+\.md$",
    r"01_data/02_qc/scripts/.+\.(py|sh)$",
    r"02_tokenization/01_existing/.+/notes\.md$",
    r"02_tokenization/01_existing/.+/config\.yaml$",
    r"02_tokenization/02_custom/.+/README\.md$",
    r"02_tokenization/02_custom/.+/eval\.md$",
    r"02_tokenization/02_custom/.+/scripts/.+\.(py|sh)$",
    r"02_tokenization/02_custom/.+/configs/.+\.(yaml|json)$",
    r"03_models/.*/configs/.+\.(yaml|json|py|sh)$",
    r"03_models/.*/scripts/.+\.(py|sh)$",
    r"05_docs/design/architecture_decision_\d{3}_.+\.md$",
    r"05_docs/meetings/meeting_\d{4}-\d{2}-\d{2}_.+\.md$",
    r"05_docs/references/.+\.(md|pdf|bib)$",
    r"06_shared/scripts/.+\.(py|sh)$",
    r"06_shared/configs/.*\.(yaml|json)$",
    r"scripts/.+\.py$",
]

# 模糊命名关键词（禁止出现）
VAGUE_NAMES = [
    "final", "new", "latest", "old", "draft", "temp", "tmp",
    "test", "backup", "copy", "revised", "updated", "version",
    "v2_final", "v3_revised", "use_this_one",
]

# 各文件的字数上限
WORD_LIMITS = {
    "README.md": 350,
    "01_data/README.md": 400,
    "02_tokenization/README.md": 400,
    "03_models/README.md": 400,
    "06_shared/README.md": 300,
    "01_data/04_quality_log.md": None,  # 不限
    "04_experiments/experiment_log.md": None,  # 不限
}

# 重复内容阈值（0-1，越高越严格）
SIMILARITY_THRESHOLD = 0.6


def find_all_docs(base: str) -> list:
    """找到所有 .md 和 .yaml 文件"""
    docs = []
    for root, dirs, filenames in os.walk(base):
        # 跳过不需要检查的目录
        dirs[:] = [d for d in dirs if d not in [
            '.git', '__pycache__', 'checkpoints', 'logs',
            'vocab_output', 'data', 'cleaned', 'checkpoints',
            'runs', 'benchmarks', '.vscode', '.idea',
        ]]
        for f in filenames:
            if f.endswith(('.md', '.yaml', '.yml')):
                fpath = os.path.join(root, f)
                rel = os.path.relpath(fpath, base)
                docs.append({
                    "path": fpath,
                    "rel": rel,
                    "name": f,
                    "size": os.path.getsize(fpath),
                })
    return docs


def is_allowed_file(rel_path: str) -> bool:
    """检查文件是否在白名单或匹配允许模式"""
    if rel_path in ALLOWED_FILES:
        return True
    for pattern in ALLOWED_PATTERNS:
        if re.search(pattern, rel_path):
            return True
    return False


def check_vague_naming(name: str) -> list:
    """检查文件名是否包含模糊关键词"""
    issues = []
    name_lower = name.lower()
    for vn in VAGUE_NAMES:
        if vn in name_lower:
            issues.append(f"包含模糊词 '{vn}'")
    return issues


def check_word_count(path: str, rel: str) -> tuple:
    """检查字数是否超限"""
    # yaml/json 配置文件不检查字数（它们是数据，不是文档）
    if rel.endswith(('.yaml', '.yml', '.json')):
        return (True, 0, None)
    for pattern, limit in WORD_LIMITS.items():
        if rel.endswith(pattern) or rel == pattern:
            if limit is None:
                return (True, None, None)
            try:
                with open(path, errors='ignore') as f:
                    # 统计中文字数 + 英文单词数
                    content = f.read()
                    # 去掉 markdown 格式符号
                    clean = re.sub(r'[#*`\-|>\[\]()]', '', content)
                    clean = re.sub(r'\s+', ' ', clean).strip()
                    words = len(clean)
            except Exception:
                return (True, 0, limit)
            if words > limit:
                return (False, words, limit)
            return (True, words, limit)
    # 没有匹配的字数限制规则，用默认 500
    try:
        with open(path, errors='ignore') as f:
            content = f.read()
            clean = re.sub(r'[#*`\-|>\[\]()]', '', content)
            clean = re.sub(r'\s+', ' ', clean).strip()
            words = len(clean)
    except Exception:
        return (True, 0, 500)
    if words > 500:
        return (False, words, 500)
    return (True, words, 500)


def check_empty_template(path: str, size: int) -> bool:
    """检查模板是否为空（生成后未填写）"""
    if size < 50:
        return False
    try:
        with open(path, errors='ignore') as f:
            content = f.read()

        # 检查是否完全是模板占位符
        template_indicators = [
            "<!-- 简要描述项目目标 -->",
            "简要描述项目目标",
            "<实验名称>",
            "<描述>",
            "YYYY-MM-DD: <实验名称>",
        ]
        has_real_content = False
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith('<!--') and not stripped.startswith('#'):
                is_template = False
                for ti in template_indicators:
                    if ti in stripped:
                        is_template = True
                        break
                if not is_template:
                    has_real_content = True
                    break

        if not has_real_content:
            return False
    except Exception:
        pass
    return True


def extract_text_blocks(content: str, min_len: int = 30) -> list:
    """提取文本段落（>30字符的连续文本）"""
    # 去掉代码块
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # 去掉表格
    content = re.sub(r'\|.*\|', '', content)
    # 去掉标题
    content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
    # 去掉链接和图片
    content = re.sub(r'\[([^\]]*)\]\([^)]*\)', '', content)
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # 分词（中英文混合）
    blocks = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if len(line) >= min_len:
            blocks.append(line)
    return blocks


def simple_similarity(text1: str, text2: str) -> float:
    """简单 Jaccard 相似度（基于字符 trigram）"""
    def trigrams(s):
        return set(s[i:i+3] for i in range(len(s) - 2))

    t1 = trigrams(text1)
    t2 = trigrams(text2)
    if not t1 or not t2:
        return 0.0
    intersection = t1 & t2
    union = t1 | t2
    return len(intersection) / len(union)


def check_duplicates(docs: list) -> list:
    """检查跨文件重复内容"""
    issues = []
    # 只检查 .md 文件，且只检查组间（不同目录的文件）
    md_docs = [(d["path"], d["rel"]) for d in docs
               if d["name"].endswith('.md') and d["size"] > 100]

    if len(md_docs) < 2:
        return issues

    checked = set()
    for i, (path1, rel1) in enumerate(md_docs):
        try:
            with open(path1, errors='ignore') as f:
                content1 = f.read()
            # 只提取长段落
            blocks1 = extract_text_blocks(content1)
            text1 = " ".join(blocks1)
            if len(text1) < 100:
                continue
        except Exception:
            continue

        for j, (path2, rel2) in enumerate(md_docs):
            if i >= j:
                continue
            pair = (rel1, rel2)
            if pair in checked:
                continue
            checked.add(pair)

            # 跳过同一目录下的文件（允许内部引用）
            if os.path.dirname(rel1) == os.path.dirname(rel2):
                continue

            try:
                with open(path2, errors='ignore') as f:
                    content2 = f.read()
                blocks2 = extract_text_blocks(content2)
                text2 = " ".join(blocks2)
                if len(text2) < 100:
                    continue
            except Exception:
                continue

            sim = simple_similarity(text1, text2)
            if sim > SIMILARITY_THRESHOLD:
                issues.append({
                    "file1": rel1,
                    "file2": rel2,
                    "similarity": sim,
                })
    return issues


def run_lint(base: str, project_name: str, strict: bool = False, fix: bool = False):
    """主检查逻辑"""
    print(f"\n{'='*60}")
    print(f"📋 文档规范检查: {project_name}")
    print(f"📁 {os.path.abspath(base)}")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if strict:
        print(f"🔒 严格模式（重复内容 = 错误）")
    if fix:
        print(f"🔧 修复模式（自动标记可疑文件）")
    print(f"{'='*60}\n")

    docs = find_all_docs(base)
    if not docs:
        print("  🕐 未找到任何文档文件")
        return

    wild_files = []       # 野文档（不在白名单）
    vague_names = []      # 模糊命名
    overlimit = []        # 超字数
    empty_templates = []  # 空模板
    duplicate_issues = [] # 重复内容
    passes = []

    print(f"📄 扫描 {len(docs)} 个文档文件...\n")

    for doc in docs:
        rel = doc["rel"]
        name = doc["name"]
        size = doc["size"]
        path = doc["path"]

        # 1. 检查是否允许的文件
        if not is_allowed_file(rel):
            wild_files.append(rel)
            if fix:
                _mark_suspicious(path, "非约定文件名，请确认是否需要")

        # 2. 检查模糊命名
        name_issues = check_vague_naming(name)
        if name_issues:
            for ni in name_issues:
                vague_names.append(f"  {rel}: {ni}")
            if fix:
                _mark_suspicious(path, f"模糊命名: {', '.join(name_issues)}")

        # 3. 检查字数
        ok, words, limit = check_word_count(path, rel)
        if not ok and limit:
            overlimit.append(f"  {rel}: {words} 字 (上限 {limit})")

        # 4. 检查空模板
        if name.endswith('.md') and not check_empty_template(path, size):
            empty_templates.append(f"  {rel}: 模板未填写 ({size} bytes)")

        # 5. 对过大的文件标记
        if size > 10000:  # 超过 10KB
            overlimit.append(f"  {rel}: 文件过大 ({size:,} bytes)，建议拆分")

    # 6. 检查跨文件重复
    print("🔍 检查跨文件重复内容...")
    duplicate_issues = check_duplicates(docs)

    # ── 输出结果 ──

    has_issues = False

    if wild_files:
        has_issues = True
        print(f"\n🔴 野文档（不在约定位置，共 {len(wild_files)} 个）:")
        for f in wild_files:
            print(f"  ❌ {f}")
        print(f"\n  💡 这些文件不符合目录规范。如果是必要的，")
        print(f"     请移到约定目录或用约定命名（如 architecture_decision_NNN_xxx.md）")

    if vague_names:
        has_issues = True
        print(f"\n⚠️  模糊命名（共 {len(vague_names)} 个）:")
        for vn in vague_names:
            print(f"  {vn}")

    if overlimit:
        has_issues = True
        print(f"\n⚠️  超字数/过大文件（共 {len(overlimit)} 个）:")
        for ol in overlimit:
            print(f"  {ol}")

    if empty_templates:
        print(f"\n🟡 空模板（共 {len(empty_templates)} 个）:")
        for et in empty_templates:
            print(f"  {et}")
        print(f"\n  💡 这些是脚手架生成的模板，正常。填完内容后会自动通过。")

    if duplicate_issues:
        is_error = strict
        prefix = "🔴" if is_error else "⚠️"
        label = "错误" if is_error else "警告"
        print(f"\n{prefix} 跨文件重复内容（{label}，共 {len(duplicate_issues)} 处）:")
        for di in duplicate_issues:
            print(f"  📎 {di['file1']} ↔ {di['file2']} (相似度: {di['similarity']:.0%})")
        if not strict:
            print(f"\n  💡 用 --strict 将重复内容视为错误")
        if is_error:
            has_issues = True

    # ── 统计 ──
    ok_count = len(docs) - len(wild_files) - len(vague_names)
    print(f"\n{'='*60}")
    print(f"📊 检查统计")
    print(f"{'='*60}")
    print(f"  总文件: {len(docs)}")
    print(f"  ✅ 命名合规: {ok_count}")
    print(f"  🔴 野文档: {len(wild_files)}")
    print(f"  ⚠️  模糊命名: {len(vague_names)}")
    print(f"  ⚠️  超字数: {len(overlimit)}")
    print(f"  ⚠️  重复内容: {len(duplicate_issues)}")
    print(f"  🟡 空模板: {len(empty_templates)}")

    if not has_issues and not wild_files and not vague_names:
        print(f"\n  🎉 文档规范检查全部通过！")
    else:
        exit_code = 1 if (strict and duplicate_issues) or wild_files else 0
        print(f"\n  💡 修复建议:")
        if wild_files:
            print(f"     1. 移除或移走野文档到约定目录")
        if vague_names:
            print(f"     2. 重命名模糊文件，去掉 final/new/latest/draft")
        if overlimit:
            print(f"     3. 拆分/精简超字数文件")
        if duplicate_issues:
            print(f"     4. 删除重复内容，在一个位置维护唯一真理")

    if fix:
        print(f"\n  🔧 已在可疑文件头部添加 HTML 注释标记")

    return 0 if not has_issues else (1 if strict and duplicate_issues else 0)


def _mark_suspicious(path: str, reason: str):
    """在文件头部添加审核标记"""
    try:
        with open(path) as f:
            content = f.read()
        marker = f"<!-- 🔴 DOC-LINT: {reason} -->\n"
        if not content.startswith("<!-- 🔴 DOC-LINT:"):
            with open(path, "w") as f:
                f.write(marker + content)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="AI 项目文档规范检查器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  doc_lint.py --name MyLLM                    # 常规检查
  doc_lint.py --name MyLLM --strict           # 严格模式
  doc_lint.py --name MyLLM --fix              # 自动标记可疑文件
        """)
    parser.add_argument("--name", type=str, required=True, help="项目名称")
    parser.add_argument("--output", type=str, default=".", help="项目父目录")
    parser.add_argument("--strict", action="store_true", help="严格模式：重复内容视为错误")
    parser.add_argument("--fix", action="store_true", help="自动在可疑文件头部添加标记")
    args = parser.parse_args()

    base = os.path.join(args.output, args.name)
    if not os.path.isdir(base):
        print(f"❌ 项目不存在: {base}")
        sys.exit(1)

    exit_code = run_lint(base, args.name, strict=args.strict, fix=args.fix)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
