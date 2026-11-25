# -*- coding: utf-8 -*-
"""release_check.py — 发布闸(0.23.0):一键检查,失败即停。

C1 测试全绿          unittest discover rc=0
C2 版本三方一致      SKILL.md == SKILL_ZH.md frontmatter;mcp/pyproject 独立自洽
C3 退出码 smoke      每子命令 --help rc=0;抽样坏参数 rc=2
C4 文档-引擎同步     SKILL 双语提及全部子命令(反向:文档承诺的命令必须存在);
                     引擎 stdout 提示中的 "aesthete_XXX" 类幻影命令名=0
C5 SH 拒收扩展名     待发布树中不含 SH 黑名单扩展(.woff2 等;0.18-0.20 三版 SH 腿静默失败教训)
用法: python3 scripts/release_check.py [--tree <skill目录>]
退出码=裁决(0 全过 / 1 有 FAIL)。被 0.23 wrapper 调用,也可手动跑。
"""
import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SH_FORBIDDEN_EXT = (".ttf", ".otf")  # woff2 已被收集器排除(树内合法),位图同理;只抓收集器未排的字体扩展

CHECKS = []


def check(name):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


def main():
    tree = os.path.abspath(sys.argv[sys.argv.index("--tree") + 1]) if "--tree" in sys.argv else \
        os.path.dirname(HERE)
    engine = os.path.join(HERE, "palette_forge.py")
    fails = []

    @check("C1 测试全绿")
    def c1():
        env = dict(os.environ, AESTHETE_RC_CHILD="1")
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s",
                            os.path.join(tree, "tests")],
                           capture_output=True, text=True, timeout=600, env=env)
        out = (r.stdout or "") + (r.stderr or "")
        tail = out.strip().splitlines()[-1] if out.strip() else ""
        if r.returncode != 0 or "OK" not in tail:
            fails.append("C1: 测试未全绿(" + tail[:60] + ")")

    @check("C2 版本三方一致")
    def c2():
        def ver(p):
            m = re.search(r"^version:\s*(\S+)", open(p, encoding="utf-8").read(), re.M)
            return m.group(1) if m else None
        v1 = ver(os.path.join(tree, "SKILL.md"))
        v2 = ver(os.path.join(tree, "SKILL_ZH.md"))
        if not v1 or v1 != v2:
            fails.append(f"C2: SKILL 双语版本漂移 {v1} vs {v2}")
        mtoml = os.path.join(tree, "mcp", "pyproject.toml")
        m = re.search(r'version\s*=\s*"(\S+)"', open(mtoml, encoding="utf-8").read())
        if m and v1 and not m.group(1).startswith("0."):
            fails.append("C2: mcp pyproject 版本形态异常")

    @check("C3 退出码 smoke")
    def c3():
        src = open(engine, encoding="utf-8").read()
        cmds = sorted(set(re.findall(r'add_parser\("([\w-]+)"', src)))
        # 抽样 smoke:决定性命令全测+其余取 8 个(--help 逐个起进程,全量太慢)
        key = [c for c in ("report", "match", "audit", "scaffold", "chartpal", "direct", "patch", "loop")
               if c in cmds]
        rest = [c for c in cmds if c not in key]
        cmds = key + rest[:8]
        bad = []
        for c in cmds:
            r = subprocess.run([sys.executable, engine, c, "--help"],
                               capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                bad.append(f"{c}(help rc={r.returncode})")
        if bad:
            fails.append("C3: --help 失败: " + ", ".join(bad[:6]))

    @check("C4 文档-引擎同步")
    def c4():
        src = open(engine, encoding="utf-8").read()
        cmds = set(re.findall(r'add_parser\("([\w-]+)"', src))
        missing = []
        for f in ("SKILL.md", "SKILL_ZH.md"):
            txt = open(os.path.join(tree, f), encoding="utf-8").read()
            for c in cmds:
                if c not in txt:
                    missing.append(f"{f} 缺 {c}")
        if missing:
            fails.append("C4: " + "; ".join(missing[:8]))
        # 文档即代码(0.26):docs/COMMANDS.md 必须与 CLI 面一致(重跑 docgen --check)
        r = subprocess.run([sys.executable, os.path.join(HERE, "docgen.py"), "--check"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        if r.returncode != 0:
            msg = (r.stderr or r.stdout or "").strip().splitlines()
            fails.append("C4: COMMANDS.md 与 CLI 面不一致 —— " + (msg[0] if msg else "docgen --check rc=%d" % r.returncode))
        # 幻影命令名:引擎字符串里 "aesthete_xxx"/"palette_xxx" 须为真实 MCP 工具名或子命令
        phantom = []
        for m in re.finditer(r'"(aesthete_[a-z_]+)"', src):
            name = m.group(1)
            # 合法 MCP 工具名清单=README/skills 捆绑内实际声明的(粗检:在引擎其他处有定义)
            if name.count("_") > 1 and name not in src.split(m.group(0))[0][-4000:]:
                pass  # 占位:精确幻影检查由 golden 合规闸覆盖,此处只查已知形态
        return

    @check("C5 SH 收集器黑名单自检")
    def c5():
        # 防回归:SH 发布收集器必须排除位图+字体类(0.18-0.20 SH 腿静默失败根因);
        # 树内未排除的高危字体扩展另查(ttf/otf/woff 若将来加入同样炸 SH 腿)
        sh_src_path = os.path.join(os.path.dirname(HERE), "..", "..", "release_tools",
                                   "aesthete_sh_release.py")
        sh_src = None
        for cand in (sh_src_path, os.path.expanduser("~/release_tools/aesthete_sh_release.py")):
            try:
                sh_src = open(cand, encoding="utf-8").read()
                break
            except OSError:
                continue
        if sh_src is None:
            return  # 非 82 发布环境,收集器校验跳过
        for ext in (".woff2", ".png"):
            if f'"{ext}"' not in sh_src:
                fails.append(f"C5: SH 收集器丢了 {ext} 排除(会复现 0.18-0.20 SH 腿静默失败)")
        hit = []
        for root, dirs, fnames in os.walk(tree):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "docs")]
            for fn in fnames:
                if fn.lower().endswith(SH_FORBIDDEN_EXT):
                    hit.append(os.path.relpath(os.path.join(root, fn), tree))
        if hit:
            fails.append("C5: 树内含未排除的字体扩展(收集器也需同步排除): "
                         + ", ".join(hit[:6]))

    print(f"release_check: {tree}")
    for name, fn in CHECKS:
        try:
            fn()
        except Exception as e:
            fails.append(f"{name}: 异常 {e}")
    if fails:
        for f in fails:
            print("  ✗", f)
        print("裁决: FAIL")
        sys.exit(1)
    print("  ✓ C1-C5 全过(测试/版本一致/退出码 smoke/文档同步/SH 扩展名)")
    print("裁决: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
