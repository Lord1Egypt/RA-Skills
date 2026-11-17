#!/usr/bin/env python3
"""ClawCode Lens — lokal kode-forklaring (unik feature: ingen ekstern API)."""
import sys
import os
import re

KEYWORDS = {
    "python": ["def ", "class ", "import ", "from ", "return ", "if ", "elif ", "else:", "for ", "while ", "try:", "except"],
    "javascript": ["function ", "const ", "let ", "var ", "=>", "class ", "import ", "export ", "if (", "for (", "while ("],
    "java": ["public ", "private ", "class ", "void ", "import ", "return ", "if (", "for (", "try {"],
    "c": ["#include", "int ", "void ", "char ", "struct ", "if (", "for (", "while ("],
    "go": ["func ", "package ", "import ", "if ", "for ", "return "],
    "rust": ["fn ", "let ", "impl ", "pub ", "match ", "use "],
    "sql": ["SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE", "JOIN", "CREATE"],
}

LANGS = {"py": "python", "js": "javascript", "ts": "typescript", "java": "java",
         "c": "c", "cpp": "c", "go": "go", "rs": "rust", "sql": "sql",
         "sh": "bash", "php": "php", "rb": "ruby"}


def detect_lang(path: str) -> str:
    ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    return LANGS.get(ext, "python")


def explain(path: str, lang: str, detail: bool = False) -> str:
    with open(path, encoding="utf-8", errors="replace") as f:
        code = f.read()
    lines = code.splitlines()
    out = [f"# Forklaring: {path}", f"**Sprog:** {lang} · **Linjer:** {len(lines)} · **Tegn:** {len(code)}", ""]

    # Nøglekonstruktioner
    kws = KEYWORDS.get(lang, [])
    found = {}
    for kw in kws:
        n = sum(1 for l in lines if kw in l)
        if n:
            found[kw.strip().rstrip("(")] = n
    if found:
        out.append("## Nøglekonstruktioner")
        for k, n in sorted(found.items(), key=lambda x: -x[1])[:10]:
            out.append(f"- `{k}` — {n} forekomster")

    # Funktioner/klasser
    out.append("")
    out.append("## Definitioner")
    defs = []
    for i, l in enumerate(lines, 1):
        if re.match(r"^\s*(def |function |class |func |fn |public .*\(|private .*\()", l):
            defs.append(f"- Linje {i}: `{l.strip()[:90]}`")
    out.extend(defs if defs else ["- (ingen fundet)"])

    if detail:
        out.append("")
        out.append("## Første 20 linjer")
        out.append("```" + lang)
        out.extend(lines[:20])
        out.append("```")

    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("BRUG: python3 explain.py fil.py [--lang sprog] [--detail]")
    path = sys.argv[1]
    lang = detect_lang(path)
    if "--lang" in sys.argv:
        lang = sys.argv[sys.argv.index("--lang") + 1]
    print(explain(path, lang, detail="--detail" in sys.argv))
