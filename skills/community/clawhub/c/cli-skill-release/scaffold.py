#!/usr/bin/env python3
"""scaffold.py — 生成零依赖 Python CLI 技能的可用骨架（cli-skill-release 自带）。

把 cli-skill-release 正文里的"踩坑点"直接编码进模板，作者无需再踩一遍：
  - tests/conftest.py 已写好 sys.path 注入（过 §2 pytest exit 2 陷阱）
  - <name>.py 的 doctor 子命令已定义 --path（过 §3 CI 必现失败陷阱）
  - .github/workflows/ci.yml 已含 tee $GITHUB_STEP_SUMMARY（过 §4 排障命门）
  - LICENSE 为 MIT-0 + ASCII 版权名（过 §5 licensee 陷阱）
  - 不含 skill-card.md（过 §6 ClawHub 保留名冲突）

零依赖：仅用标准库。用法：
    python scaffold.py <skill-name> [--author "He Wei"] [--email you@x.com] [--dest DIR]
"""
import argparse
import datetime
import os
import sys

# --------------------------------------------------------------------------
# 模板（占位符：__NAME__=展示名, __MODULE__=模块名(蛇形), __AUTHOR__, __EMAIL__, __YEAR__；真实 Python 守卫 __name__ 不动）
# --------------------------------------------------------------------------

SKILL_MD = '''---
name: __MODULE__
slug: __MODULE__
displayName: __NAME__（零依赖 CLI 技能）
version: 0.1.0
author: __AUTHOR__
license: MIT-0
description: >
  （用一句话说明这个技能做什么、何时触发。触发描述写法参考内置 skill-creator：
   用第三人称 "This skill should be used when..."，具体说明用户会说什么触发它。）
---

# __NAME__

（在这里写技能正文。SKILL.md 的"内容怎么写"交给 skill-creator；本技能负责把它发到市场。）

## 何时用
（描述触发场景）

## 怎么做
（核心流程，命令用代码块）
'''

MAIN_PY = '''#!/usr/bin/env python3
"""__NAME__ — 零依赖 CLI 技能示例入口。

由 cli-skill-release 的 scaffold.py 生成。含 doctor 自检门（支持 --path，过 CI 陷阱）。
"""
import argparse
import os
import sys


def discover_local(roots, include_self=True):
    """扫描给定根目录下的技能目录（示例实现，可按需替换）。"""
    found = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "SKILL.md")):
                found.append(path)
    return found


def cmd_doctor(args):
    roots = [args.path] if args.path else [os.path.dirname(os.path.abspath(__file__))]
    skills = discover_local(roots, include_self=args.path is not None)
    print("[doctor] 扫描 {n} 个根，发现 {m} 个技能目录".format(n=len(roots), m=len(skills)))
    for s in skills:
        print("  - " + s)
    print("[doctor] OK")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="__MODULE__", description="__NAME__ 零依赖 CLI 技能")
    sub = p.add_subparsers(dest="cmd")
    d = sub.add_parser("doctor", help="自检技能目录")
    d.add_argument("--path", default=None, help="指定扫描根目录（CI 用 .）")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "doctor":
        return cmd_doctor(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

SAMPLE_MODULE = '''"""示例子模块（纯标准库）。CLI 主文件或测试可 import 它。"""


def greet(name="world"):
    return "hello, " + name
'''

CONFTEST = '''import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
'''

TEST_SMOKE = '''import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "__MODULE__.py")


def test_doctor_path_exits_zero():
    """§3 陷阱：doctor 必须接受 --path，否则 CI 全平台必现失败。"""
    r = subprocess.run([sys.executable, MAIN, "doctor", "--path", "."],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_imports_sample_module():
    """§2 陷阱：tests 直接 import scripts 模块需 conftest 注入 sys.path。"""
    import sample_module
    assert sample_module.greet("ci") == "hello, ci"
'''

CI_YML = '''name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m pip install -q "pytest>=8.3,<9"
      - name: Run pytest
        run: python -m pytest -q 2>&1 | tee $GITHUB_STEP_SUMMARY
      - name: Doctor
        run: python __MODULE__.py doctor --path .
'''

LICENSE = '''Copyright (c) __YEAR__ __AUTHOR__

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

LISTING = '''# __NAME__ — 一句话定位

## 为什么需要
（写痛点：同类只能装不能管 / CI 总红 / LICENSE 总显示 Other / 上架总被卡……）

## 核心差异化
1. （具体可验证的卖点，如"零依赖""140 passed""AST 级扫描"，避免空泛形容词）
2.
3.

## 安装
- 方式一：ClawHub 搜索 `__MODULE__`
- 方式二：下载仓库后 `python __MODULE__.py doctor`

## 功能矩阵
| 功能 | 说明 |
|---|---|
| doctor | 自检技能目录 |

## 链接
- GitHub: https://github.com/<you>/__MODULE__
'''

README = '''# __NAME__

零依赖 Python CLI 技能。由 cli-skill-release 的 scaffold.py 生成。

## 快速开始
```
python __MODULE__.py doctor --path .
python -m pytest -q
```

## 结构
- `__MODULE__.py` CLI 入口（含 doctor 自检门）
- `scripts/` 子模块
- `tests/` 测试（含稳健的 sys.path 注入）
- `.github/workflows/ci.yml` GitHub Actions

## License
MIT-0（Copyright (c) __YEAR__ __AUTHOR__）
'''

GITIGNORE = '''_*
*.pyc
__pycache__/
.tmp-pub/
REVIEW-APPROVAL-*.html
'''


def _render(tpl, name, module_name, author, email, year):
    return (tpl
            .replace("__NAME__", name)
            .replace("__MODULE__", module_name)
            .replace("__AUTHOR__", author)
            .replace("__EMAIL__", email)
            .replace("__YEAR__", year))


def scaffold(name, author, email, dest):
    module_name = name.replace("-", "_").replace(" ", "_")
    year = str(datetime.date.today().year)
    files = {
        "SKILL.md": SKILL_MD,
        module_name + ".py": MAIN_PY,
        os.path.join("scripts", "sample_module.py"): SAMPLE_MODULE,
        os.path.join("tests", "conftest.py"): CONFTEST,
        os.path.join("tests", "test_smoke.py"): TEST_SMOKE,
        os.path.join(".github", "workflows", "ci.yml"): CI_YML,
        "LICENSE": LICENSE,
        "MARKETPLACE-LISTING.md": LISTING,
        "README.md": README,
        ".gitignore": GITIGNORE,
    }
    created = []
    for rel, tpl in files.items():
        content = _render(tpl, name, module_name, author, email, year)
        path = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        created.append(rel)
    return created


def main(argv=None):
    p = argparse.ArgumentParser(description="生成零依赖 CLI 技能骨架")
    p.add_argument("name", help="技能名（如 my-cli-skill）")
    p.add_argument("--author", default="He Wei", help="版权名（ASCII，如 He Wei）")
    p.add_argument("--email", default="you@example.com", help="作者邮箱")
    p.add_argument("--dest", default=None, help="输出目录（默认 ./<name>）")
    args = p.parse_args(argv)
    dest = args.dest or os.path.join(os.getcwd(), args.name)
    created = scaffold(args.name, args.author, args.email, dest)
    print("[scaffold] 已生成到: " + dest)
    for rel in created:
        print("  + " + rel)
    print("[scaffold] 下一步: cd " + dest + " && python -m venv env && env/Scripts/python -m pip install pytest && python -m pytest -q && python " + args.name.replace('-', '_') + ".py doctor --path .")
    return 0


if __name__ == "__main__":
    sys.exit(main())
