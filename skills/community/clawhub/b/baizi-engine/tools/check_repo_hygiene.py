# -*- coding: utf-8 -*-
"""公开仓库卫生门禁：阻止内部/商业文档与私密文件再次进入公开仓库。

为什么存在（2026-10 事故）：
  本仓库曾把内部文档（HANDOFF.md / 工作区说明.md / docs/history/ 下的竞对分析、发布物料、
  SkillHub-Submission-Kit 等）提交进公开仓库；即使后来 `git rm`，旧提交对象在 GitHub 上仍可按 SHA
  取回，最终只能**删库重建 + 全量重写历史**才清干净（并留下一个第三方 fork 无法回收）。
  教训：靠"记得别提交"不可靠，必须有机器门禁 —— 这就是本脚本。

两种模式：
  · 默认（CI/手动）：检查**已跟踪文件**（`git ls-files`）
  · `--staged`：检查**暂存区待提交文件**（`git diff --cached`），用于 git pre-commit 钩子 —— 在**泄漏发生前**拦截

安装钩子：`python tools/check_repo_hygiene.py --install-hook`
"""
import io
import os
import re
import subprocess
import sys

# 禁止进入公开仓库的路径模式（保持通用，不写出具体业务文档名以免自曝）
FORBIDDEN = [
    (r"(^|/)HANDOFF\.md$", "内部交接文档（含定价/渠道/卡点等商业信息）"),
    (r"(^|/)工作区说明\.md$", "内部工作区说明"),
    (r"(^|/)AI_CONTEXT\.md$", "内部上下文文档"),
    (r"^docs/history/", "历史归档（发布物料/竞对分析/验收清单）"),
    (r"^docs/course-", "课程物料（商业内容）"),
    (r"^docs/专栏/", "专栏物料（商业内容）"),
    (r"\.zip$", "发布包（构建产物，不入库）"),
    (r"qrcode", "个人二维码素材"),
    (r"^_local/", "本地临时工作目录"),
    (r"^marketing-assets/", "营销素材缓存"),
    (r"^\.dsh-uploads/", "DSH 上传临时目录"),
    (r"^\.workbuddy/", "WorkBuddy 本地缓存"),
    (r"(^|/)\.fingerprints\.json$", "溯源指纹（公开即失效）"),
]

# 内容级特征（在文件**内容**里匹配；两种模式都查）。2026-10 由风险面扫描补充：
# 公开仓库里不该出现本机盘符路径与本地工具链路径——它们会泄漏 Windows 用户名、目录结构与所用平台。
# 这些模式只在**行内**匹配，且不含 URL（`https://`、`file://` 不会命中）。
CONTENT_PATTERNS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "私钥内容"),
    (r"[A-Za-z]:\\[A-Za-z]", "本机 Windows 盘符路径（泄漏用户名/目录结构）"),
    (r"[A-Za-z]:/(?:Users|Program|Windows|home|tmp|opt|michael)/", "本机绝对路径"),
    (r"\.workbuddy\b", "本地工具链路径（泄漏平台与用户名）"),
    (r"/home/[A-Za-z][\w.-]*/", "本机 POSIX 绝对路径"),
]

# 本文件自身含上述模式字符串（作为检测规则），跳过自检
SELF = "tools/check_repo_hygiene.py"

# .gitignore / .gitattributes 的职责就是列出本地目录与文件名，对"本地目录名"类规则豁免（仍查私钥与盘符路径）
LOCAL_DIR_OK = {".gitignore", ".gitattributes"}
LOCAL_DIR_RULES = (r"\.workbuddy\b", r"/home/[A-Za-z][\w.-]*/")

# 二进制/压缩文件不做内容扫描
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip", ".gz", ".woff", ".woff2", ".ttf", ".pdf"}

HOOK = """#!/bin/sh
# 由 tools/check_repo_hygiene.py --install-hook 安装：提交前拦截内部文档/私密文件
exec python "$(git rev-parse --show-toplevel)/tools/check_repo_hygiene.py" --staged
"""


def sh(args):
    p = subprocess.run(args, capture_output=True)
    return p.returncode, (p.stdout or b"").decode("utf-8", "replace")


def repo_root():
    rc, out = sh(["git", "rev-parse", "--show-toplevel"])
    return out.strip() if rc == 0 else os.getcwd()


def targets(staged):
    if staged:
        rc, out = sh(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    else:
        rc, out = sh(["git", "ls-files"])
    if rc != 0:
        print("⚠️ 无法读取 git 文件列表（退出码 %d），跳过检查" % rc)
        return None
    return [l for l in out.splitlines() if l.strip()]


def main():
    argv = sys.argv[1:]
    if "--install-hook" in argv:
        root = repo_root()
        hooks = os.path.join(root, ".git", "hooks")
        os.makedirs(hooks, exist_ok=True)
        hp = os.path.join(hooks, "pre-commit")
        with io.open(hp, "w", encoding="utf-8", newline="\n") as f:
            f.write(HOOK)
        print("✅ 已安装 pre-commit 钩子：%s" % hp)
        print("   （本机生效，不入库；CI 侧另有同名检查步骤）")
        return 0

    staged = "--staged" in argv
    files = targets(staged)
    if files is None:
        return 0

    scope = "暂存区" if staged else "已跟踪文件"
    hits = []
    for f in files:
        for pat, why in FORBIDDEN:
            if re.search(pat, f):
                hits.append((f, why))
                break

    content_hits = []
    root = repo_root()
    for f in files:
        if f == SELF:
            continue
        full = os.path.join(root, f)
        if not os.path.isfile(full):
            continue
        if os.path.splitext(f)[1].lower() in SKIP_EXT:
            continue
        try:
            if os.path.getsize(full) > 3 * 1024 * 1024:
                continue
            with io.open(full, "r", encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    if len(line) > 20000:      # 内联大数据行（dist / index.html 的 RULES）
                        continue
                    for pat, why in CONTENT_PATTERNS:
                        if f in LOCAL_DIR_OK and pat in LOCAL_DIR_RULES:
                            continue
                        if re.search(pat, line):
                            content_hits.append((f, i, why, line.strip()[:80]))
                            break
        except Exception:
            continue

    if hits or content_hits:
        total = len(hits) + len(content_hits)
        print("❌ 公开仓库卫生门禁未通过（%s，共 %d 项）：" % (scope, total))
        for f, why in hits:
            print("   🔴 %s   ← %s" % (f, why))
        for f, i, why, sample in content_hits:
            print("   🔴 %s:%d   ← %s" % (f, i, why))
            print("        例: %s" % sample)
        print()
        print("   这些内容属于内部/商业资料，不得进入公开仓库（2026-10 曾因此删库重建）。")
        print("   正确做法：移出仓库，放进你在仓库外自建的本地归档目录，并写入 .gitignore。")
        print("   并用 .gitignore 忽略。确认确实需要提交时：git commit --no-verify（请三思）。")
        return 1

    print("✅ 公开仓库卫生门禁通过（%s %d 个文件：无内部/商业文档、无本机路径或私钥特征）" % (scope, len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
