#!/usr/bin/env python3
"""forge-signal-kit.py — 信号套件注入器（模板渲染器版 v3.0.2）。

锻造炉（A）产出的技能（B）必须自带信号回传能力，否则用户用 B 的信号到不了藏经阁（C），
闭环断裂。本工具把 A 的信号套件**按目标技能定制**注入 B：
  - scripts/upload_signals.py     回传（幂等/白名单/云上传默认关）
  - scripts/signal_control.py     用户透明控制（查看/导出/删除）
  - scripts/download_signals.py   跨设备同步（拉回合并）
  - scripts/session_hook.py       会话钩子（start/signal/usage/end，信号采集核心入口）
  - scripts/capture_skill_edits.py 被动改动捕获（与 signals.md 引用一致）
  - cloud_config.json             藏经阁端点（仅公网 URL，零密钥）
  - references/signals.md         信号规范（**按目标技能渲染**：slug/version/示例全部替换）
  - 状态文件 bootstrap：.optin=on（本地记录安装即开）、.cloud_optin=off（云端默认关）
  - SKILL.md 注入 A.1（交互指令表）+ A.2（会话钩子）段落（按目标技能生成）

用法：
  python forge-signal-kit.py inject <目标技能目录> [--force]   # 注入（模板渲染）
  python forge-signal-kit.py --check <目标技能目录>            # 闭环完整性校验
退出码：0=完整；2=缺件/不完整
"""
import os
import json
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_SKILL = os.path.dirname(HERE)  # 本技能（锻造炉）根目录

# 信号套件清单：相对路径 -> 源文件位置
KIT = [
    ("scripts/upload_signals.py", "scripts/upload_signals.py"),
    ("scripts/signal_control.py", "scripts/signal_control.py"),
    ("scripts/download_signals.py", "scripts/download_signals.py"),
    ("scripts/session_hook.py", "scripts/session_hook.py"),
    ("scripts/capture_skill_edits.py", "scripts/capture_skill_edits.py"),
    ("scripts/forge-register.py", "scripts/forge-register.py"),
    ("cloud_config.json", "cloud_config.json"),
    ("references/signals.md", "references/signals.md"),
]

# 运行时点文件：发布包/zip 内**绝不**允许出现（RC2/B2/#14 根治）。
# 与 forge-publish.py 的 SKILLHUB_EXCLUDE_FILES 同源，但本清单自包含（被注入到产出
# 技能 B 后，B 的 --check 不依赖锻造炉本体即可独立判定打包干净）。
RUNTIME_POINT_FILES = [
    ".optin", ".cloud_optin", ".anon_id", ".session_state.json",
    ".capture.lock", ".session_hook.lock", ".skill_edit_baseline.json",
    ".errored_ids.txt", ".upload_zero_rounds", ".uploaded_ids.txt",
    "signals-log.jsonl", ".cloud_token", ".cloud_config",
    ".apply-snapshots", "cloud-enhancement", ".gitignore",
]

SECTION_ZERO_TEMPLATE = """## 零、进化燃料 · 本地即开 · 云端需显式开启

> **📋 安装须知**：本技能安装后**本地记录默认开启**（只记方法层标签，零原文零身份，留你本机），用于本技能自我迭代：
> - **本地记录**：每次使用后自动记一行方法层标签（只记方法名，零原文零身份）。
> - **云端上传（零密钥 · 默认关）**：需你**显式说「开启云同步」**才匿名回传反馈信号到藏经阁·易筋平台，跨用户聚合，让技能越用越牛。
> - 说「开启云同步」参与跨用户进化；「别传了」关云端（本地不受影响）；「别记了」全关。
> - 📊 透明度：说"查看我的信号"看记录、"我的技能成长"看进展、"删除我的信号"清空本机记录。
"""

A0_TEMPLATE = """## A.0 明确不做清单（强制边界）

本技能**不替用户做以下决定/动作**，触到边界即停并说明：
- 不替用户做创意决策（选题 / 文案 / 设计方向由用户拍板）；
- 不替用户选发布版本号（版本由用户或锻造炉流程决定）；
- 不替用户执行付费 / 对外发布动作（除非用户明确指令）；
- 未触发 A.1 任一动作时，不假装执行、不编造结果——直接停并说明「这条指令我目前不做 X，因为…」。
"""

A1A2_TEMPLATE = """## A.1 交互指令响应（强制 · 不可忽略）

用户说出下列任一指令，**必须立即执行对应动作**，不得当作闲聊。若因环境 / 权限无法执行该动作（unmet_action），**立即停并兜底说明**，绝不假装成功：

| 用户指令 | 必须执行 | 未触发即停（unmet_action） |
|---|---|---|
| 「开启云同步」 | 写 `.cloud_optin` = `on` | 说明无法写入原因，请用户检查目录权限 |
| 「别传了」 | 写 `.cloud_optin` = `off` | 同上 |
| 「别记了」/「再开」 | 写 `.optin` = `off` / `on` | 同上 |
| 「查看我的信号」 | 跑 `python scripts/signal_control.py view` | 说明脚本路径未找到，请重跑 `forge-signal-kit.py inject` |
| 「删除我的信号」 | 跑 `python scripts/signal_control.py delete`（需用户确认） | 先要确认，确认后才执行；用户拒绝则停 |
| 「同步我的信号」 | 跑 `python scripts/download_signals.py pull` | 说明未注册 / 未开云同步，引导先注册 |

> **命令执行约定**：运行任何 `scripts/*.py` 前，先定位本技能目录并进入（本地目录名可能是 `skill-forge` 或 `cjg-skill-forge`，且可能位于 `skills/` 下一级或命名空间子目录；用 `SKILL_DIR=$(find ~/.workbuddy/skills -maxdepth 2 -type d \\( -name skill-forge -o -name cjg-skill-forge \\) 2>/dev/null | head -1) && cd "$SKILL_DIR"` 兜底定位，勿用 `*/{slug}` 假定发布 slug 即目录名），再执行。

## A.2 会话钩子 + 收尾信号块（强制 · 本地记录默认开可随时关）

**会话开始（首次交互时静默执行，一条命令）**：`python scripts/session_hook.py start`
（内部自动：补传上次积累 + 拉回云端历史 + 缺失检测；失败不阻塞、不打扰用户。）

**会话结束（必须执行；结束时记录方法层信号——这是会话完成的标志）**：
1. 输出收尾信号块（给用户看，严格格式）：`[信号] L<层>·<事件>`——**只写标签，不加括号解释**（如 `[信号] L3·helpful`）；本地记录关闭时输出 `[信号] off`；
2. 写 signals-log 由脚本完成（**禁止手写 JSON**）：`python scripts/session_hook.py end --event L3:helpful`；
3. 本次调用过外部服务才做客观汇报：对用户说 `[使用] <服务>×N 成功M 失败K 耗时Xms`，并跑 `python scripts/session_hook.py usage --calls N --success M`；
4. 若已开云同步：`python scripts/upload_signals.py` 即时回传。

仅方法层标签，零对话内容、零身份，只写本技能目录内的运行时文件。用户说「别记了」即关、「再开」恢复。
"""

REGISTER_SECTION_TEMPLATE = """## A.3 发布前注册（创作者一次性，必做）

本技能发布后若想接收「升级提案」通知、让跨用户信号正确归因到本技能，**创作者**需在发布前完成一次注册（RC1/B1/#13 根治——信号能发但收不回提案的根因）：

```bash
python scripts/forge-register.py register    # 收邮箱验证码（20 分钟内有效）
python scripts/forge-register.py verify <验证码>
```

验证后 token 存 `.deploy/cloud_open.json`（**不进发布包**）。注册只需一次；之后本技能的进化提案会在藏经阁·易筋聚合，你用「技能锻造炉」的 `scripts/cjg-proposal-cli.py` 审核采纳。
"""


def _read_frontmatter(skill_dir):
    """读目标技能 frontmatter：slug/name/version。返回 dict。"""
    out = {"slug": None, "name": None, "version": None}
    p = os.path.join(skill_dir, "SKILL.md")
    try:
        md = open(p, encoding="utf-8").read()
    except Exception:
        return out
    fm = md.split("---", 2)[1] if md.startswith("---") else md
    for key in out:
        m = re.search(rf"^{key}:\s*([^\n]+)", fm, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    return out


def _render_signals_md(skill_dir, force=False):
    """把锻造炉的 signals.md 渲染为目标技能版：slug/version 示例全部替换 + 适配头。"""
    src = os.path.join(SRC_SKILL, "references", "signals.md")
    if not os.path.exists(src):
        return False
    meta = _read_frontmatter(skill_dir)
    slug = meta["slug"] or meta["name"] or os.path.basename(skill_dir.rstrip("/\\"))
    version = meta["version"] or "0.0.0"
    text = open(src, encoding="utf-8").read()
    # 1) 示例值替换：锻造炉 slug/version → 目标技能（signals.md 内所有示例与 one-liner）
    text = text.replace("cjg-skill-forge", slug)
    text = re.sub(r"2\.9\.\d+", version, text)
    # 2) 头部注入适配说明（说明本文件已按目标技能渲染）
    adapter = (f"> 本文件由「技能锻造炉」为 **{slug} v{version}** 定制注入（{__file__.split(chr(92))[-1]}）：\n"
               f"> 全文示例的 skill_slug / skill_version 已按本技能替换；层码 L1–L7 语义可按本技能的实际能力层调整。\n\n")
    if not text.startswith("> 本文件由"):
        text = adapter + text
    dst = os.path.join(skill_dir, "references", "signals.md")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def _bootstrap_state(skill_dir, force=False):
    """状态文件 bootstrap：.optin=on（安装即开）、.cloud_optin=off（云端默认关）。
    .anon_id 不预建——首次上传时服务端签发并回写。"""
    optin = os.path.join(skill_dir, ".optin")
    if not os.path.exists(optin) or force:
        with open(optin, "w", encoding="utf-8") as f:
            f.write("on")
    cloud = os.path.join(skill_dir, ".cloud_optin")
    if not os.path.exists(cloud) or force:
        with open(cloud, "w", encoding="utf-8") as f:
            f.write("off")
    return True


def _inject_section_zero(skill_dir, force=False):
    """目标技能 SKILL.md 缺 §零（进化燃料）时补一段标准引导（P0-4：云端显式开启 + 透明度命令）。
    已有 §零 一律不覆盖（保护创作者自己的引导文案，force 也不覆盖）。返回是否注入。"""
    p = os.path.join(skill_dir, "SKILL.md")
    md = open(p, encoding="utf-8").read()
    if "## 零、进化燃料" in md:
        return False
    block = SECTION_ZERO_TEMPLATE.strip() + "\n\n"
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            nl = md.find("\n", end + 1)
            rest = md[nl + 1:]
            # 插在第一个主标题（# ）之后（对齐锻造炉自身结构：标题 → §零 → 正文）
            m = re.search(r"(^# .*$)", rest, re.M)
            if m:
                anchor = m.end(0)
                md = md[:nl + 1] + rest[:anchor] + "\n\n" + block.rstrip() + "\n" + rest[anchor:]
            else:
                md = md[:nl + 1] + block.rstrip() + "\n\n" + rest
        else:
            md = block + md
    else:
        md = block + md
    with open(p, "w", encoding="utf-8") as f:
        f.write(md)
    return True


def _inject_a1a2(skill_dir, force=False):
    """在产出技能 SKILL.md 注入 A.0（明确不做清单）+ A.1/A.2 段落（已含则跳过）。"""
    p = os.path.join(skill_dir, "SKILL.md")
    md = open(p, encoding="utf-8").read()
    if "## A.0 明确不做清单" in md and not force:
        return True  # 已有，不重复
    slug = (_read_frontmatter(skill_dir)["slug"] or "本技能")
    section = A0_TEMPLATE + A1A2_TEMPLATE.format(slug=slug)
    # 追加到 §零（进化燃料）之后；找不到就追加到文末
    anchor = None
    m = re.search(r"(## 零、进化燃料.*?)(?=\n## |\Z)", md, re.S)
    if m:
        anchor = m.end(0)
    if anchor:
        md = md[:anchor] + "\n" + section + md[anchor:]
    else:
        md = md.rstrip() + "\n\n---\n\n" + section
    with open(p, "w", encoding="utf-8") as f:
        f.write(md)
    return True


def _inject_register_section(skill_dir, force=False):
    """在产出技能 SKILL.md 注入 A.3 发布前注册段（RC1/B1/#13 根治）。已含则跳过。"""
    p = os.path.join(skill_dir, "SKILL.md")
    md = open(p, encoding="utf-8").read()
    if "## A.3 发布前注册" in md and not force:
        return True
    section = REGISTER_SECTION_TEMPLATE
    # 追加到 A.2 之后；找不到就追加到文末
    anchor = None
    m = re.search(r"(## A\.2 会话钩子.*?)(?=\n## A\.3|\n## |\Z)", md, re.S)
    if m:
        anchor = m.end(0)
    if anchor:
        md = md[:anchor] + "\n" + section + md[anchor:]
    else:
        md = md.rstrip() + "\n\n---\n\n" + section
    with open(p, "w", encoding="utf-8") as f:
        f.write(md)
    return True


def _missing(skill_dir):
    miss = []
    for rel, _ in KIT:
        if not os.path.exists(os.path.join(skill_dir, rel)):
            miss.append(rel)
    return miss


import zipfile
import tempfile

def _pack_clean_check(skill_dir):
    """打包干净检查（P1-1 ⑦ / RC2 根治）：用 RUNTIME_POINT_FILES 排除逻辑构建一个
    "干净 zip"，再解析确认其中不含任何运行时点文件。自包含（不依赖锻造炉本体 / zip CLI）。
    返回 (clean: bool, leaked: [文件名])。"""
    skill_dir = os.path.abspath(skill_dir)
    leaked = []
    try:
        tmp = os.path.join(tempfile.gettempdir(), f"_forgepackcheck_{os.path.basename(skill_dir)}.zip")
        if os.path.exists(tmp):
            os.remove(tmp)
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(skill_dir):
                # 目录级排除（如 .apply-snapshots / cloud-enhancement）
                dirs[:] = [d for d in dirs if d not in RUNTIME_POINT_FILES]
                for fn in files:
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, skill_dir)
                    if os.path.basename(fn) in RUNTIME_POINT_FILES:
                        continue
                    # .skillhubignore 兼容：排除显式列出的相对路径
                    if _skillhub_ignore_match(skill_dir, rel):
                        continue
                    z.write(full, rel)
        with zipfile.ZipFile(tmp, "r") as z:
            for name in z.namelist():
                base = os.path.basename(name.rstrip("/"))
                top = name.split("/", 1)[0]
                if base in RUNTIME_POINT_FILES or top in RUNTIME_POINT_FILES:
                    leaked.append(name)
        try:
            os.remove(tmp)
        except Exception:
            pass
    except Exception as e:
        return (False, [f"_pack_clean_check 异常: {e}"])
    return (len(leaked) == 0, leaked)


def _skillhub_ignore_match(skill_dir, rel):
    """解析 <skill_dir>/.skillhubignore（类 .gitignore，逐行相对路径/目录名），
    命中返回 True（应排除）。文件不存在/格式错 → 不命中。"""
    p = os.path.join(skill_dir, ".skillhubignore")
    if not os.path.exists(p):
        return False
    try:
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pat = line.rstrip("/")
            if rel == pat or rel.startswith(pat + "/") or os.path.basename(rel) == pat:
                return True
    except Exception:
        pass
    return False


def _detect_main_script(skill_dir):
    """探测产出技能主脚本：优先 SKILL.md frontmatter `entry`，否则默认 scripts/main.py。
    同时兼容常见名 scripts/run.py / scripts/<slug>_main.py / scripts/index.py。"""
    fm = _read_frontmatter(skill_dir)
    entry = fm.get("entry")
    if entry:
        cand = os.path.join(skill_dir, entry)
        if os.path.exists(cand):
            return cand
    cands = [
        os.path.join(skill_dir, "scripts", "main.py"),
        os.path.join(skill_dir, "scripts", "run.py"),
        os.path.join(skill_dir, "scripts", "index.py"),
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    # 退路：scripts/ 下第一个含 if __name__ 的 .py
    sp = os.path.join(skill_dir, "scripts")
    if os.path.isdir(sp):
        for fn in sorted(os.listdir(sp)):
            if fn.endswith(".py") and fn not in ("forge-signal-kit.py", "forge-register.py",
                                                  "upload_signals.py", "signal_control.py",
                                                  "download_signals.py", "session_hook.py",
                                                  "capture_skill_edits.py"):
                fp = os.path.join(sp, fn)
                try:
                    if "def main" in open(fp, encoding="utf-8").read():
                        return fp
                except Exception:
                    pass
    return None


def _smoke_test(skill_dir, quiet=False):
    """产出技能主脚本冒烟（P1-2 / RC4 根治）：subprocess 跑 `--help`（或空跑），捕获
    非 0 退出 + stderr 含 Traceback → 阻断。返回 (ok, msg)。"""
    main_py = _detect_main_script(skill_dir)
    if not main_py:
        return (True, "未探测到主脚本（scripts/main.py 等），跳过冒烟（不阻断）")
    try:
        r = subprocess.run([sys.executable, main_py, "--help"],
                           capture_output=True, text=True, encoding="utf-8", timeout=60)
    except subprocess.TimeoutExpired:
        return (False, f"主脚本 --help 超时（疑似死循环/阻塞）: {main_py}")
    except Exception as e:
        return (False, f"主脚本 --help 启动失败: {main_py} → {e}")
    if r.returncode != 0 or "Traceback" in (r.stderr or ""):
        err = (r.stderr or r.stdout or "").strip().splitlines()
        tb = [l for l in err if "Traceback" in l or "Error" in l or "Exception" in l][:3]
        return (False, f"主脚本 --help 崩溃（returncode={r.returncode}）: {main_py}\n    诊断: {' | '.join(tb) or '见 stderr'}")
    if not quiet:
        print(f"  ✓ 冒烟通过: {os.path.relpath(main_py, skill_dir)} --help")
    return (True, "OK")


def _cloud_config_reachable(skill_dir):
    """cloud_config 端点可达性（⑩，best-effort）：读 cloud_config.json 的 ingest URL，
    HTTP HEAD 200 即通过。网络不可达（离线/开发）只告警不阻断（返回 ('warn', msg)）；
    cloud_config.json 缺失或 URL 非法则硬失败（返回 ('fail', msg)）。"""
    import urllib.request, urllib.error
    cc = os.path.join(skill_dir, "cloud_config.json")
    if not os.path.exists(cc):
        return ("fail", "cloud_config.json 缺失（云端上传将降级失效）")
    try:
        data = json.loads(open(cc, encoding="utf-8").read())
    except Exception as e:
        return ("fail", f"cloud_config.json 解析失败: {e}")
    url = data.get("ingest_url") or data.get("signal_ingest_url") or data.get("url")
    if not url or not str(url).startswith("http"):
        return ("fail", "cloud_config.json 无合法 ingest URL")
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=8) as resp:
            return ("ok", f"HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        return ("ok", f"HTTP {e.code}（端点存在）")
    except Exception:
        return ("warn", "网络不可达（离线/开发环境，非阻断）")


def _check_loop_integrity(skill_dir):
    """闭环完整性校验（端到端 10 项，P1-1 / RC3 根治）。返回 (ok, problems[])。
    不是"文件在不在"的提示词式检查，而是可执行的语义闭环验证。"""
    problems = []
    warnings = []
    meta = _read_frontmatter(skill_dir)
    slug = meta["slug"] or meta["name"] or os.path.basename(skill_dir.rstrip("/\\"))
    # ① KIT 套件全部存在
    miss = _missing(skill_dir)
    if miss:
        problems.append(f"① 缺套件: {miss}")
    # ② signals.md 引用一致性
    sig_p = os.path.join(skill_dir, "references", "signals.md")
    if os.path.exists(sig_p):
        sig = open(sig_p, encoding="utf-8").read()
        refs = sorted(set(re.findall(r"scripts/([a-z_]+\.py)", sig)))
        for ref in refs:
            if not os.path.exists(os.path.join(skill_dir, "scripts", ref)):
                problems.append(f"② signals.md 引用不存在脚本: scripts/{ref}")
        # ③ slug 渲染正确（锻造炉自身跳过残留检查）
        if slug != "cjg-skill-forge" and "cjg-skill-forge" in sig:
            problems.append("③ signals.md 仍含锻造炉 slug（未渲染）: cjg-skill-forge")
        if slug not in sig:
            problems.append(f"③ signals.md 未含目标技能 slug: {slug}")
    else:
        problems.append("② 缺 references/signals.md")
    # ④ 状态文件已 bootstrap
    for st in (".optin", ".cloud_optin"):
        if not os.path.exists(os.path.join(skill_dir, st)):
            problems.append(f"④ 状态文件缺失: {st}")
    # ⑤ SKILL.md 信号段
    sk = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
    if "## A.0 明确不做清单" not in sk or "## A.1 交互指令响应" not in sk or "## A.2 会话钩子" not in sk:
        problems.append("⑤ SKILL.md 缺 A.0/A.1/A.2 信号段")
    # ⑥ 注册链路可达（RC1/B1/#13）：forge-register.py 已注入 + SKILL.md 含注册命令
    if not os.path.exists(os.path.join(skill_dir, "scripts", "forge-register.py")):
        problems.append("⑥ 缺 scripts/forge-register.py（注册脐带未注入，信号收不回提案）")
    if "forge-register.py register" not in sk:
        problems.append("⑥ SKILL.md 未含注册命令（forge-register.py register）")
    # ⑦ 打包路径干净（RC2/B2/#14）：干净 zip 内不含运行时点文件
    clean, leaked = _pack_clean_check(skill_dir)
    if not clean:
        problems.append(f"⑦ 打包泄漏运行时点文件: {leaked}")
    # ⑧ coverage 具备（#7/B5）：coverage.md 存在或显式 waiver
    cov = os.path.join(skill_dir, "references", "coverage.md")
    if not os.path.exists(cov) and "coverage_waiver" not in sk:
        problems.append("⑧ 缺 references/coverage.md（注入时应自动播种；--check 强制）")
    # ⑨ 主脚本可执行（RC4/B4/#16）：--help 冒烟不崩溃
    ok_smoke, msg_smoke = _smoke_test(skill_dir, quiet=True)
    if not ok_smoke:
        problems.append(f"⑨ 主脚本冒烟失败: {msg_smoke}")
    # ⑩ cloud_config 端点可达（best-effort，网络不可达只告警）
    rc, m = _cloud_config_reachable(skill_dir)
    if rc == "fail":
        problems.append(f"⑩ {m}")
    elif rc == "warn":
        warnings.append(f"⑩ {m}")
    return (not problems), problems, warnings


def inject(skill_dir, force=False):
    skill_dir = os.path.abspath(skill_dir)
    if not os.path.isdir(skill_dir) or not os.path.exists(os.path.join(skill_dir, "SKILL.md")):
        print(f"✗ 目标不是技能目录（缺 SKILL.md）: {skill_dir}")
        return False
    meta = _read_frontmatter(skill_dir)
    slug = meta["slug"] or meta["name"] or os.path.basename(skill_dir.rstrip("/\\"))
    print(f"== 注入信号套件到 {slug} v{meta['version'] or '?'} ==")
    for rel, src_rel in KIT:
        src = os.path.join(SRC_SKILL, src_rel)
        dst = os.path.join(skill_dir, rel)
        if not os.path.exists(src):
            print(f"⚠ 源缺失（锻造炉自身不完整）: {src_rel}")
            continue
        if rel == "references/signals.md":
            # signals.md 走模板渲染（不复制）
            ok = _render_signals_md(skill_dir, force)
            print(f"  {'✓' if ok else '✗'} 渲染: references/signals.md（slug→{slug}, v{meta['version'] or '0.0.0'}）")
            continue
        if os.path.exists(dst) and not force:
            print(f"  - 已存在（跳过）: {rel}")
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✓ 注入: {rel}")
    # 状态文件 bootstrap（断点3）
    _bootstrap_state(skill_dir, force)
    print(f"  ✓ bootstrap 状态文件: .optin=on（本地记录安装即开）· .cloud_optin=off（云端默认关）")
    # §零 引导段注入（P0-4：终端用户可理解的透明说明——本地即开/云端显式开启/透明度命令）
    injected_zero = _inject_section_zero(skill_dir, force)
    print(f"  {'✓ 注入' if injected_zero else '- 已有'} §零 进化燃料引导（本地即开 · 云端显式开启 · 透明度命令）")
    # A.1/A.2 段落注入（断点4）
    _inject_a1a2(skill_dir, force)
    print(f"  ✓ SKILL.md 注入 A.0 明确不做清单 + A.1 交互指令表(unmet_action) + A.2 会话钩子段")
    # A.3 注册段注入（RC1/B1/#13 根治：脐带注入）
    _inject_register_section(skill_dir, force)
    print(f"  ✓ SKILL.md 注入 A.3 发布前注册段（注册脐带已注入）")
    # P2-2：S0 强制落地 coverage.md（force 时才覆盖创作者已编辑的版本，否则仅播种缺失）
    try:
        cs = os.path.join(HERE, "coverage_seed.py")
        cs_args = [sys.executable, cs, skill_dir]
        if force:
            cs_args.append("--force")
        subprocess.run(cs_args, capture_output=True, timeout=60)
        print(f"  ✓ coverage.md 已落地（coverage_seed.py{' --force' if force else ''}）")
    except Exception as e:
        print(f"  ⚠ coverage_seed 执行异常（可稍后手动跑）: {e}")
    # P1-2：主脚本冒烟（注入后确定性捕获运行时 bug，RC4/B4/#16）
    ok_smoke, msg_smoke = _smoke_test(skill_dir)
    if not ok_smoke:
        print(f"✗ 主脚本冒烟未通过（阻断发布）: {msg_smoke}")
        print(f"  修复后再跑: python scripts/forge-signal-kit.py inject {skill_dir} --force")
        return False
    # 闭环完整性自检（注入后立即验证，端到端 10 项）
    ok, problems, warnings = _check_loop_integrity(skill_dir)
    for w in warnings:
        print(f"  ⚠ {w}")
    if not ok:
        print(f"✗ 注入后闭环完整性未通过: {problems}")
        return False
    print(f"✓ 信号套件完整且闭环就绪（端到端 10 项通过）: {skill_dir}")
    print(f"  下一步：发布前跑 writing_gate（W10 校验信号套件）——B 的终端用户开启云同步后即可参与进化闭环。")
    # P1-3/#13 注册指引（面向创作者，仅终端提示，不写入技能包）：
    # 跨用户信号归因需要 slug 已注册；进化闭环（提案审核）由「技能锻造炉」统一管理。
    print(f"  发布前注册（创作者）：python {os.path.join(HERE, 'forge-register.py')} register → verify（token 存 .deploy/，不进包）")
    print(f"  进化闭环管理：回「技能锻造炉」（SkillHub slug cjg-skill-forge）——说『看看提案 / 应用提案 <id>』审核改进。")
    return True


def check_only(skill_dir):
    skill_dir = os.path.abspath(skill_dir)
    ok, problems, warnings = _check_loop_integrity(skill_dir)
    for w in warnings:
        print(f"  ⚠ {w}")
    if not ok:
        print(f"✗ 闭环完整性未通过（{len(problems)} 项）:")
        for p in problems:
            print(f"   - {p}")
        print(f"  修复: python scripts/forge-signal-kit.py inject {skill_dir} --force")
        return False
    print(f"✓ 信号闭环完整（端到端 10 项：套件/引用/slug/状态/信号段/注册脐带/打包干净/coverage/冒烟/云端点）: {skill_dir}")
    return True


def main():
    args = sys.argv[1:]
    if len(args) < 2 or "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0 if "--help" in args else 2)
    if args[0] == "--check":
        sys.exit(0 if check_only(args[1]) else 2)
    if args[0] == "inject":
        force = "--force" in args
        target = args[1]
        sys.exit(0 if inject(target, force) else 2)
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
