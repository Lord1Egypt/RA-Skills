#!/usr/bin/env python3
"""Build data/books/book01..07.md from raw sources (Griffith Gutenberg #24869 + Dutt Uttara Kandam OCR)."""
import re, sys
from pathlib import Path
SKILL = Path(__file__).resolve().parent.parent
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else SKILL / "raw"
OUT = SKILL / "data" / "books"
OUT.mkdir(parents=True, exist_ok=True)

ROMAN = {'I':1,'V':5,'X':10,'L':50,'C':100}
def roman(s):
    s = s.upper(); tot = 0
    for i,ch in enumerate(s):
        v = ROMAN.get(ch)
        if v is None: return None
        nxt = ROMAN.get(s[i+1]) if i+1 < len(s) else 0
        tot += -v if nxt and nxt > v else v
    return tot

KANDA = [
 ("Bāla Kāṇḍa", "童年篇"), ("Ayodhyā Kāṇḍa", "阿逾陀篇"), ("Araṇya Kāṇḍa", "森林篇"),
 ("Kiṣkindhā Kāṇḍa", "猴国篇"), ("Sundara Kāṇḍa", "美妙篇"), ("Yuddha Kāṇḍa", "战斗篇"),
 ("Uttara Kāṇḍa", "后篇"),
]

# ---------- Griffith books I-VI ----------
g = (RAW / "pg24869.txt").read_text(encoding="utf-8").splitlines()
# body: from second "BOOK I." heading to APPENDIX
starts = [i for i,l in enumerate(g) if re.match(r"^BOOK [IVX]+\.\(?\d*\)?\s*$", l.strip()) or re.match(r"^Book I\.\s*$", l.strip())]
book_heads = [i for i,l in enumerate(g) if re.match(r"^BOOK (I|II|III|IV|V|VI)\.(\(\d+\))?$", l.strip()) and i > 600]
app = next(i for i,l in enumerate(g) if l.strip()=="APPENDIX." and i > book_heads[-1])
assert len(book_heads)==6, book_heads
bounds = book_heads + [app]
stats = []
for b in range(6):
    lines = g[bounds[b]+1:bounds[b+1]]
    out = [f"# Book {b+1} · {KANDA[b][0]}（{KANDA[b][1]}）", ""]
    ncanto = 0
    for l in lines:
        s = l.rstrip()
        s = re.sub(r"\(\d+\)(?=[A-Za-z])", " ", s)  # glued footnote refs
        s = re.sub(r"\(\d+\)", "", s)          # footnote refs
        m = re.match(r"^Canto ([IVXLC]+)\.?\s*(.*)$", s.strip())
        if m and not l.startswith(" "):
            ncanto += 1
            title = m.group(2).strip()
            out += ["", f"## Canto {m.group(1)}" + (f". {title}" if title else ""), ""]
            continue
        out.append(s.strip() if s.startswith("  ") else s)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    (OUT / f"book{b+1:02d}.md").write_text(text, encoding="utf-8")
    stats.append((b+1, ncanto, len(text)))

# ---------- Dutt Uttara Kandam (OCR) ----------
d = (RAW / "TheRamayanaUttaraKandam.txt").read_text(encoding="utf-8").splitlines()
first = next(i for i,l in enumerate(d) if l.strip().startswith("SECTION I."))
end = max(i for i,l in enumerate(d) if l.strip().startswith("THE END"))
d = d[first:end]
# split into pages on "Digitized by" lines
pages, cur = [], []
for l in d:
    if re.search(r"Digitized\s+by", l):
        pages.append(cur); cur = []
    else:
        cur.append(l)
pages.append(cur)
FN = re.compile(r"^\s*([\*†‡§¶%^]|[tf%J]\s+(i\.\s?e\.|Compare|The|This|Lit|Literally|A |An |Vide|See|That|He|She|It|Or|In|i\.e))")
body = []
for pg in pages:
    # drop page header: first non-empty line(s) like "1558 RAMAYANA." or "UTTARAKANDAM. 1557"
    lines = list(pg)
    k = 0
    while k < len(lines) and not lines[k].strip(): k += 1
    if k < len(lines) and re.search(r"(RAM\s*A\s*Y\s*A\s*N\s*A|KANDAM|K\s*A\s*N\s*D\s*A\s*M)\W*\s*\d*\s*$", lines[k].strip(), re.I) and len(lines[k].strip()) < 40:
        lines = lines[k+1:]
    # drop footnote block at page end
    nonempty = [i for i,l in enumerate(lines) if l.strip()]
    cut = None
    for i in nonempty[3:]:
        if FN.match(lines[i]):
            # footnote block if rest of page is short
            if len([j for j in nonempty if j >= i]) <= 12:
                cut = i; break
    if cut is not None: lines = lines[:cut]
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    body.extend(lines)

text = "\n".join(l.rstrip() for l in body)
# OCR fixes
rep = {"\u2014": "—", "R&mayana":"Ramayana", "R&ma":"Rama", "Brahm&":"Brahma", "V&lmiki":"Valmiki"}
rep.update({"\\Jn ":"On ","JL HIS ":"THIS "})
for a,b in rep.items(): text = text.replace(a,b)
text = re.sub(r"(?<=[A-Za-z])&(?=[a-z])", "a", text)
text = re.sub(r"(?<=[a-z])S(?=[a-z])", "a", text)
for a,b in {"Havana":"Ravana","Rvana":"Ravana","Rlma":"Rama","RSma":"Rama","TUkshasa":"Rakshasa","R&kshasa":"Rakshasa","LankB":"Lanka","LankS":"Lanka","Lankl":"Lanka","LankI":"Lanka"}.items():
    text = re.sub(r"\b"+a+r"\b", b, text)
text = re.sub(r"(\w)- *\n\s*(\w)", r"\1\2", text)          # de-hyphenate
lines = text.split("\n")
out = [f"# Book 7 · {KANDA[6][0]}（{KANDA[6][1]}）", "", "> Prose translation by Manmatha Nath Dutt (1894), OCR text lightly cleaned. Section numbers normalised; occasional OCR errors may remain.", ""]
para, prev_sec = [], 0
def flush():
    if para:
        p = " ".join(x.strip() for x in para)
        p = re.sub(r"\s+", " ", p)
        p = re.sub(r"(?<=[\w\.,;'’!?\)])[\*†‡§\^]+", "", p)   # footnote markers
        p = re.sub(r" ([,;:\.!?])", r"\1", p)
        out.append(p.strip()); out.append("")
        para.clear()
nsec = 0
for l in lines:
    s = l.strip()
    m = re.match(r"^[S8s]\s*[Ee]\s*[Cc]\s*[Tt]\s*[Ii]\s*[Oo]\s*[Nn]\s+([A-Za-z\. ,]+?)\s*[\.,]?\s*$", s)
    if m and len(s) < 30:
        flush()
        raw = re.sub(r"[^IVXLC]", "", m.group(1).replace("l","I").replace("f","I").replace("t","I").replace("U","II").replace("M","II").upper())
        n = roman(raw) if raw else None
        if n is None or n <= prev_sec or n > prev_sec + 4:
            n = prev_sec + 1
        prev_sec = n; nsec += 1
        # write numeral
        def toroman(x):
            vals=[(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]; r=''
            for v,c in vals:
                while x>=v: r+=c; x-=v
            return r
        out += ["", f"## Section {toroman(n)}", ""]
        continue
    if not s:
        # only break paragraph if the previous line ended a sentence
        if para and re.search(r"[\.!?\"'’”\)]\s*$", para[-1]):
            flush()
        continue
    if re.fullmatch(r"[\W\dIil|]{1,6}", s) or len(re.findall(r"[A-Za-z]", s)) < 2:  # stray OCR junk / page numbers
        continue
    para.append(s)
flush()
t7 = "\n".join(out)
t7 = re.sub(r"\n{3,}", "\n\n", t7).strip() + "\n"
(OUT / "book07.md").write_text(t7, encoding="utf-8")
stats.append((7, nsec, len(t7)))

full = ["# The Rāmāyaṇa of Vālmīki — Full Text (Books 1–7)", "", "Books 1–6: Ralph T. H. Griffith (verse, 1870–1874). Book 7: Manmatha Nath Dutt (prose, 1894). See SOURCE.md.", ""]
for b in range(1,8):
    full.append((OUT / f"book{b:02d}.md").read_text(encoding="utf-8").replace("\n# ", "\n# ").rstrip()); full.append("")
(OUT.parent / "ramayana-full.md").write_text("\n".join(full), encoding="utf-8")
for s in stats: print("book%02d cantos=%d chars=%d" % s)
