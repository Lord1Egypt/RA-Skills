"""bazi-engine 发布包构建（通用市场分发版，平台无关）

用法：
    python tools/build_release_zip.py            # 打包（版本号自动取自 skill/SKILL.md）
    python tools/build_release_zip.py v1.4.0     # 指定版本号
    python tools/build_release_zip.py --check    # 只做交付包契约校验，不写出 ZIP（CI 用）

要点（对齐 HANDOFF 踩坑 #17/#18/#22）：
- ZIP 内文件直接在根，无外层嵌套目录
- 排除平台禁止的 LICENSE / LICENSE-DATA / README.en.md（数据许可改以 DATA-LICENSE.txt 随包分发）
- ZIP 根放 SKILL.md（从 skill/SKILL.md 复制），与项目源 skill/SKILL.md 保持同步
- 只打包可对外内容（ui/engine/kb/skill/tools + README.md），内部文档（HANDOFF/AI_CONTEXT/发布物料等）与 docs/assets 不进 ZIP
"""
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _skill_version() -> str:
    """从 skill/SKILL.md frontmatter 读版本号。
    2026-10-12（v1.3.11）：默认值原写死为 'v1.3.0'，无参运行会产出"文件名与内容不符"的包（误传风险）。"""
    try:
        txt = (ROOT / 'skill' / 'SKILL.md').read_text(encoding='utf-8')
        # 注意：正则里不要出现"冒号紧跟反斜杠"的字面量（会被 check_repo_hygiene 误判为 Windows 盘符路径）
        m = re.search('^version:[ \t]*([0-9][0-9A-Za-z.-]*)', txt, re.M)
        return 'v' + m.group(1) if m else 'v0.0.0'
    except Exception:
        return 'v0.0.0'


ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
CHECK_ONLY = '--check' in sys.argv
VERSION = ARGS[0] if ARGS else _skill_version()
OUT = ROOT / f'bazi-engine-{VERSION}.zip'

# 顶层目录白名单（只打包这些目录）
INCLUDE_DIRS = {'ui', 'engine', 'kb', 'skill', 'tools'}
# 顶层文件白名单（根文件只放 README.md；SKILL.md 单独复制到根）
INCLUDE_ROOT_FILES = {'README.md'}
# SkillHub 禁止 / 内部不对外
EXCLUDE_ROOT_FILES = {'LICENSE', 'LICENSE-DATA', 'README.en.md',
                      'HANDOFF.md', 'SkillHub-Submission-Kit.md',
                      'SkillHub发布最终指引.md',
                      '验收与截图清单_3案例.md', '.gitignore'}
# 目录内排除的子路径/文件模式
EXCLUDE_SUB = {
    'kb/04-rules-db/drafts',        # 内部取材源
    'kb/02-rules/bazi-mbti.md',     # 2026-10：早期版本来源不明（无作者无 URL），现版已重写但按约定仍不纳入对外/商用交付
    'tools/__pycache__', 'tools/_dbg', 'tools/archive',  # 归档脚本不进发布包（2026-08-19 审计修复）
    'kb/05-reference',  # 内部参考
    # 2026-10-11：作者运维工具不进市场包（compliance_soften 涉及自有 C 端产品口径，publish_clawhub 为发布操作脚本），
    # 与交付标的无关且会暴露内部业务流程
    'tools/compliance_soften.py', 'tools/publish_clawhub.ps1',
    # 2026-10-12（v1.3.11）：C 端软化派生产物**不在仓库里**（.gitignore 忽略），却曾被打进发布包
    # → 包内容取决于"本机是否跑过软化脚本"，干净克隆下打出的包少一个文件、MD5 不同（不可复现）。
    'engine/engine.compliance.js',
}
EXCLUDE_NAMES = {'__pycache__', '.DS_Store', 'Thumbs.db'}

# 2026-10 风险面扫描修复：THIRD-PARTY.md 声明"kb/03-classics/ 中的 docx 提取件不进商业交付包"，
# 但当时 EXCLUDE_SUB 并未包含它们 → 声明与实际不符（发布包/Release 附件里实有 6 个 docx 提取件：
# bazi-wuxing-table / ditian-sui / qiongtong-baojian / sanming-tonghui / workflow-full / yuanhai-ziping）。
# 现改为**按文件头部的来源标记自动排除**，并在打包后做硬校验（见 main 的 docx_left 检查），
# 保证"声明即事实"：以后任何新增的 docx 提取件也会自动被挡在交付包之外。
DOCX_PROVENANCE_RE = re.compile(r'来源[：:].{0,60}\.docx', re.IGNORECASE)

# 本次构建中被"docx 来源"规则自动排除的文件（打印出来，避免静默）
DOCX_EXCLUDED = []


def has_docx_provenance(path: Path) -> bool:
    """文件头部 1500 字符内声明了 .docx 来源 → 第三方整理件，不进交付包"""
    if path.suffix.lower() not in ('.md', '.txt'):
        return False
    try:
        head = path.read_text(encoding='utf-8', errors='ignore')[:1500]
    except Exception:
        return False
    return bool(DOCX_PROVENANCE_RE.search(head))



def collect() -> list:
    """返回 [(arc_name, abs_path)]，arc 为 ZIP 内路径（根无嵌套）"""
    items = []
    # 根文件
    for f in sorted(ROOT.iterdir()):
        if not f.is_file():
            continue
        if f.name in INCLUDE_ROOT_FILES:
            items.append((f.name, f))
    # 根 SKILL.md ← skill/SKILL.md（坑 #22：ZIP 根必须有且与源同步）
    skill_src = ROOT / 'skill' / 'SKILL.md'
    if skill_src.exists():
        items.append(('SKILL.md', skill_src))
    # 2026-10：数据许可随包分发。平台禁止 LICENSE/LICENSE-DATA 文件名，故改名为 DATA-LICENSE.txt，
    # 避免"包内含 1000 条 NC 数据却无任何数据许可声明"（第三方据此主张 MIT/MIT-0 授权）。
    lic_data = ROOT / 'LICENSE-DATA'
    if lic_data.exists():
        items.append(('DATA-LICENSE.txt', lic_data))
    # 2026-10：第三方权利与排除清单必须随包分发（否则包内数据无权利说明）
    tp = ROOT / 'THIRD-PARTY.md'
    if tp.exists():
        items.append(('THIRD-PARTY.md', tp))
    # 白名单目录
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name not in INCLUDE_DIRS:
            continue
        for p in sorted(d.rglob('*')):
            if not p.is_file():
                continue
            if p.name in EXCLUDE_NAMES:
                continue
            arc = p.relative_to(ROOT).as_posix()
            if any(arc.startswith(s) for s in EXCLUDE_SUB):
                continue
            if has_docx_provenance(p):
                DOCX_EXCLUDED.append(arc)
                continue
            if arc.endswith(('.tmp', '.bak')):
                continue
            items.append((arc, p))
    return items


def check_contract(items):
    """交付包契约断言（正式打包与 --check 都执行）：返回 (arcs, problems)"""
    arcs = sorted(a for a, _ in items)
    problems = []
    for req in ('README.md', 'SKILL.md', 'DATA-LICENSE.txt', 'THIRD-PARTY.md',
                'kb/04-rules-db/rules.json', 'kb/README.md'):
        if req not in arcs:
            problems.append(f'缺少必需文件: {req}')
    for forbidden in ('engine/engine.compliance.js', 'LICENSE', 'LICENSE-DATA'):
        if forbidden in arcs:
            problems.append(f'包含不应交付的文件: {forbidden}')
    rj = next((p for a, p in items if a == 'kb/04-rules-db/rules.json'), None)
    if rj:
        try:
            if 'license' not in json.loads(rj.read_text(encoding='utf-8')):
                problems.append('rules.json 顶层缺少 license 字段（数据文件需自带许可标识）')
        except Exception as e:
            problems.append(f'rules.json 解析失败: {e}')
    return arcs, problems


def main():
    items = collect()
    arcs, problems = check_contract(items)
    # 硬校验：交付包内不得含 docx 提取件（THIRD-PARTY.md 声明的"不进商业交付包"必须为真）
    docx_left = []
    for arc in arcs:
        if not arc.lower().endswith(('.md', '.txt')):
            continue
        src = ROOT / arc
        if src.exists():
            try:
                if DOCX_PROVENANCE_RE.search(src.read_text(encoding='utf-8', errors='ignore')[:1500]):
                    docx_left.append(arc)
            except Exception:
                pass
    if docx_left:
        problems.append('包内含 docx 提取件（第三方整理，权利链不完整）: ' + ', '.join(docx_left))

    print(f'版本: {VERSION}')
    print(f'包含文件: {len(arcs)} 个')
    print('根文件:', ', '.join(a for a in arcs if '/' not in a))
    print('自动排除(来源标注为 .docx 的第三方整理件):', ', '.join(sorted(DOCX_EXCLUDED)) or '无')
    print('校验-包内无 docx 提取件:', 'OK' if not docx_left else f'❌ 异常: {docx_left}')

    if CHECK_ONLY:
        if problems:
            print('\n❌ 交付包契约校验未过（--check，未写出 ZIP）：')
            for pr in problems:
                print('   - ' + pr)
            sys.exit(1)
        print('\n✅ 交付包契约校验通过（--check，未写出 ZIP）')
        return

    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(str(OUT), 'w', zipfile.ZIP_DEFLATED) as zf:
        for arc, path in items:
            zf.write(str(path), arc)
    print(f'ZIP 输出: {OUT}')
    print(f'ZIP 大小: {OUT.stat().st_size / 1024:.1f} KB')
    bad_root = [a for a in arcs if a.split('/')[0] in EXCLUDE_ROOT_FILES]
    nested = [a for a in arcs if a.count('/') == 0 and a not in ('README.md', 'SKILL.md', 'DATA-LICENSE.txt', 'THIRD-PARTY.md')]
    print('校验-排除名单残留:', bad_root if bad_root else '无')
    print('校验-根无嵌套:', 'OK' if not nested else f'异常: {nested}')
    import hashlib
    for kf in ['ui/index.html', 'engine/engine.dist.js', 'skill/SKILL.md', 'kb/04-rules-db/rules.json', 'SKILL.md']:
        src = ROOT / kf
        if src.exists():
            print(f'MD5 {kf}: {hashlib.md5(src.read_bytes()).hexdigest()}')
    print(f'MD5 {OUT.name}: {hashlib.md5(OUT.read_bytes()).hexdigest()}')
    if problems:
        print('\n❌ 交付包契约校验未过：')
        for pr in problems:
            print('   - ' + pr)
        sys.exit(1)
    print('✅ 交付包契约校验通过')


if __name__ == '__main__':
    main()
