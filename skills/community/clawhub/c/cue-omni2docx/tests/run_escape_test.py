#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_escape_test.py — 属性 breakout 专项回归（M394）：判据按标签解析器，不按字符串搜。

为什么不用 grep：在产件里搜 alert 只能证「那串字符没出现」，证不了「它没变成一枚可执行属性」；
提前闭合属性之后，payload 会以**属性名**的形出现在标签里——只有解析器分得清属性名与属性值。
所以本件用 html.parser 把产件读回来，逐条判：属性名集合、属性值逐字等于上游那段文本、文本节点没被过度转义。

用例（五枚，逐枚自报）：
  E1 正控：alt/description 里带 " 与 < ⇒ 产件解析后 img.alt 逐字等于原串（完整落在引号内）
  E2 反证：alt=" onerror="alert(1) ⇒ img 的属性名里不得出现 onerror（值仍是整串原样）
  E3 反证：脚注 key 带引号闭合形 ⇒ sup/a 不得多出属性名，id 值逐字回原
  E4 反证：链接 href 带引号闭合形 ⇒ a 不得多出 onload 之类属性名
  E5 分工：正文文本节点里的引号不得被写成 &quot;（esc 与 esc_attr 两形各走各的出口）

跑法：python3 tests/run_escape_test.py（零网络、零外部依赖，产物落 tests/out/）
退码：0 五枚全合；1 有不合（逐枚点名实得）；3 取值域故障（render_html.py 或本件跑不起来——不读成「零违例」）。
"""
import html.parser as _hp
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "scripts"
RENDER = str(SKILL / "render_html.py")
OUT = HERE / "out"
OUT.mkdir(parents=True, exist_ok=True)
PY = sys.executable

PAYLOAD_ATTR = 'x" onerror="alert(1)'
PAYLOAD_KEY = 'k" autofocus="z'
PAYLOAD_HREF = 'http://x.test/a" onload="evil'
TEXT_QUOTE = '正文里的引号"和尖括号<应保持原样'   # 件内那条 CJK 空格归一是既有行为，比对的两侧都先去空格


class Collect(_hp.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.data = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs), [k for k, _ in attrs]))

    def handle_data(self, d):
        self.data.append(d)


def render(md_text, name):
    md = OUT / (name + ".md")
    htm = OUT / (name + ".html")
    md.write_text(md_text, encoding="utf-8")
    r = subprocess.run([PY, "-B", RENDER, "--md", str(md), "--out", str(htm)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not htm.is_file():
        raise SystemExit("3 取值域故障：render_html 没出件（%s｜rc=%d｜%s）"
                         % (name, r.returncode, (r.stderr or r.stdout).strip()[:120]))
    body = htm.read_text(encoding="utf-8")
    c = Collect()
    c.feed(body)
    c.close()
    return body, c


def find(c, tag, want_attr=None):
    for t, attrs, names in c.tags:
        if t != tag:
            continue
        if want_attr is None or want_attr in attrs:
            return attrs, names
    return None, None


def main():
    rows = []

    # E1 正控
    body, c = render('![%s](https://example.org/a.png)\n' % PAYLOAD_ATTR, "e1")
    attrs, names = find(c, "img")
    ok = attrs is not None and attrs.get("alt") == PAYLOAD_ATTR
    rows.append(("E1 正控：alt 含引号仍完整落在属性内", ok,
                 "解析器读回的 alt=%r｜属性名=%s" % (None if attrs is None else attrs.get("alt"), names)))

    # E2 反证：不得出现可执行属性名
    bad_attr = "onerror" in (names or []) or "alert(1)" in " ".join(names or [])
    rows.append(("E2 反证：img 不得多出 onerror 属性名", (not bad_attr) and ok,
                 "属性名清单=%s（判据＝按解析器读回的属性名集合，不是在文本里搜 alert）" % (names,)))

    # E3 反证：脚注 key
    body3, c3 = render("正文一句[^%s]。\n\n[^%s]: 脚注正文\n" % (PAYLOAD_KEY, PAYLOAD_KEY), "e3")
    a_attrs, a_names = find(c3, "a", "href")
    li_attrs, li_names = find(c3, "li")
    key_ok = any((v or "").startswith('fn-k" autofocus=') for v in
                 [(a_attrs or {}).get("href", ""), (li_attrs or {}).get("id", "")])
    leak = any(x in (a_names or []) + (li_names or []) for x in ("autofocus", "onerror", "onclick"))
    rows.append(("E3 反证：脚注 key 的引号没闭合属性", key_ok and not leak,
                 "a 属性名=%s｜li 属性名=%s｜href/id 现读=%r / %r"
                 % (a_names, li_names, (a_attrs or {}).get("href"), (li_attrs or {}).get("id"))))

    # E4 反证：链接 href
    body4, c4 = render("[点我](%s)\n" % PAYLOAD_HREF, "e4")
    l_attrs, l_names = find(c4, "a", "href")
    href_ok = (l_attrs or {}).get("href") == PAYLOAD_HREF
    leak4 = any(x in (l_names or []) for x in ("onload", "onerror", "onclick", "evil"))
    rows.append(("E4 反证：链接 href 的引号没闭合属性", href_ok and not leak4,
                 "a 属性名=%s｜href 现读=%r" % (l_names, (l_attrs or {}).get("href"))))

    # E5 分工：文本节点不该被转成实体（比对两侧都先去空格——件内 CJK 空格归一是既有行为）
    body5, c5 = render(TEXT_QUOTE + "\n", "e5")
    joined = "".join(c5.data).replace(" ", "")
    text_ok = TEXT_QUOTE in joined
    over = "&quot;" in body5.split("</style>")[-1] if "</style>" in body5 else "&quot;" in body5
    rows.append(("E5 分工：文本节点的引号保持原样（不过度转义）", text_ok and not over,
                 "解析回的正文含原句=%s｜正文区出现 &quot;=%s" % (text_ok, over)))

    bad = 0
    for name, ok, note in rows:
        bad += 0 if ok else 1
        print("%-46s %s" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            print("     实得：%s" % note)
        else:
            print("     读数：%s" % note)
    print("=" * 72)
    print("合计 %d 例，PASS %d，FAIL %d" % (len(rows), len(rows) - bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
