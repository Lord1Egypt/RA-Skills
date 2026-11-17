# -*- coding: utf-8 -*-
"""红队扫描器：中英双库扫描越狱/危险能力请求，输出风险分级+命中模式。零依赖。

退出码契约（**门禁不得 fail-open**，2026-09-28 修复）：
    rc=0  未发现已知红队模式 → 通过
    rc=1  仅命中中危模式      → 需人工复核
    rc=2  命中高危模式        → 拦截（调用方应据此阻断）
    rc=3  用法或环境错误（文件不存在 / 参数错误）

修复记录（2026-09-28）：原实现 main() 无返回值、__main__ 未 sys.exit()，
退出码恒为 0 —— 命中高危也"看起来通过"，属 fail-open，违背 LGD-III「有门禁」。
本次把检测结果交给退出码，并让 argparse 用法错误走 rc=3（不再占用 rc=2）。
"""
import argparse, pathlib, re, sys

PATTERNS = [
    ("指令覆盖", re.compile(r"忽略(之前|以上|前面)的?(指令|规定|设定)|ignore (the )?(previous|above|prior) (instructions|rules)", re.I)),
    ("角色扮演越狱", re.compile(r"\bDAN\b|无限制模式|扮演(一个)?(邪恶|evil)|developer mode|无限制", re.I)),
    ("提权", re.compile(r"以(管理员|admin|root)身份|关闭安全(限制|措施)|disable (the )?safe(guard|ty)|escalate", re.I)),
    ("数据外泄", re.compile(r"打印(出)?(system prompt|系统提示)|泄露(记忆|密钥|密码|api)|print (the )?(system prompt|memory)|exfiltrat", re.I)),
    ("自修改", re.compile(r"修改(你|自己)的?(代码|规则|指令)|modify (your|its) (own )?(code|rules|instructions)|self-?improv", re.I)),
    ("去约束", re.compile(r"不要(再)?(遵守|受限)|不用(遵守|管)规则|ignore (all )?constraints|without (any )?restriction", re.I)),
]

TIER = {"指令覆盖": "🔴高危", "数据外泄": "🔴高危", "自修改": "🔴高危",
        "提权": "🔴高危", "角色扮演越狱": "🟡中危", "去约束": "🟡中危"}

RC_CLEAN, RC_MEDIUM, RC_HIGH, RC_USAGE = 0, 1, 2, 3


def scan(text):
    hits = []
    for name, pat in PATTERNS:
        for m in pat.finditer(text):
            hits.append((name, m.group(0)))
    return hits


def exit_code_for(hits):
    """命中 → 退出码；无命中 → 0。高危优先。"""
    tiers = {TIER.get(n, "🟡中危") for n, _ in hits}
    if "🔴高危" in tiers:
        return RC_HIGH
    if "🟡中危" in tiers:
        return RC_MEDIUM
    return RC_CLEAN


class _Parser(argparse.ArgumentParser):
    """用法错误一律 rc=3，不占用 rc=2（rc=2 已语义化为「命中高危」）。"""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(RC_USAGE, f"{self.prog}: 用法错误: {message}\n")


def main(argv=None):
    ap = _Parser(description="红队扫描器：扫越狱/危险能力请求，按风险分级返回退出码。")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    a = ap.parse_args(argv)

    try:
        text = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8-sig")
    except OSError as e:
        print(f"❌ 无法读取输入：{e}", file=sys.stderr)
        return RC_USAGE

    hits = scan(text)
    if not hits:
        print("✅ 未发现已知红队模式")
        return RC_CLEAN

    tiers = {}
    for name, frag in hits:
        tiers.setdefault(TIER.get(name, "🟡中危"), []).append((name, frag))
    print(f"⚠️ 命中 {len(hits)} 处：")
    for tier in ("🔴高危", "🟡中危"):
        if tier in tiers:
            print(f"  {tier}")
            for name, frag in tiers[tier]:
                print(f"    - [{name}] …{frag}…")
    rc = exit_code_for(hits)
    if rc == RC_HIGH:
        print("\n🔒 处置：高危请求直接拦截，不执行、不解释攻击细节。")
        print("   rc=2（拦截）")
    else:
        print("\n🟡 处置：中危请求需人工复核后再决定是否执行。")
        print("   rc=1（复核）")
    return rc


if __name__ == "__main__":
    sys.exit(main())
