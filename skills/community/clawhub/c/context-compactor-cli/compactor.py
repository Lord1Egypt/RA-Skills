#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
context-compactor — condenses a long agent conversation/session transcript
into a compact handoff memo: decisions, facts, open tasks, links, risks.
Works on Russian and English text without external dependencies.

Usage:
    python3 compactor.py --input session.md
    python3 compactor.py --input session.md --max-lines 400 --output handoff.md
    python3 compactor.py --self-test

Safety:
    Lines containing credentials (password, token, api key, secret,
    private keys, sk-/ghp_ tokens...) have their VALUES replaced with
    <REDACTED: ...> before scoring/output, so a handoff memo should not leak
    secrets to the receiving agent (best-effort pattern matching - review memos before sharing). --self-test asserts the covered cases.

Heuristics & limits:
    - Bucketing priority: strong decisions > (link + weak decision = facts)
      > tasks > risks > facts. Weak decision words without a link stay
      decisions; "agreed, link: <url>" lands in facts.
    - Long transcripts: the FIRST max_lines*2 and LAST max_lines lines are
      considered (final decisions usually sit at the end); the rest is
      counted and reported as truncated.
    - Dedup is by full normalized line (whitespace+case), not by first 80 chars.

MIT License. Author: Viacheslav Bochkarev.
"""
import argparse
import datetime
import os
import re
import sys

__version__ = "1.1.7"

# ---- heuristics -----------------------------------------------------------

STRONG_DECISION_RU = re.compile(
    r"\b(решили|решил|решила|выбрали|выбрал|выбрала|утвердили|утверждено|приняли|принято|план такой)\b", re.I)
STRONG_DECISION_EN = re.compile(
    r"\b(decided|agreed|approved|adopted|chose|chosen|settled on|let'?s go with|going with)\b", re.I)
# Weak decision markers: without a link — decision, with a link — fact/link
WEAK_DECISION_RU = re.compile(
    r"\b(договорились|остановились на|делаем|будем|начинаем|переходим|берём|запускаем|публикуем)\b", re.I)
WEAK_DECISION_EN = re.compile(
    r"\b(we will|we'?re (going to|starting|moving)|switching to|plan is|let'?s do)\b", re.I)

TASK_RU = re.compile(r"\b(нужно|надо|необходимо|следует|осталось|предстоит|задача|todo|сделать|следующий шаг|напомни|проверь|подготовь|настрой|обнови|доделать|доделай)\b", re.I)
TASK_EN = re.compile(r"\b(todo|to-do|next step|next:?|need to|must|have to|remaining|open (task|item)|follow[- ]?up|remember to|don'?t forget|remind|still (need|open))\b", re.I)
FACT_RU = re.compile(r"\b(называется|означает|версия|логин|email|адрес|url|ссылка|id|номер|стоит|цена|тариф|дата|срок|дедлайн|репозиторий|установлен|настроен|готово|закончено|вышла|вышел)\b", re.I)
FACT_EN = re.compile(r"\b(is called|means|version|login|email|url|link|id|number|price|tariff|date|deadline|located at|repository|installed|configured|done|released)\b", re.I)
RISK_RU = re.compile(r"\b(риск|опасно|нельзя|не работает|сломано|баг|проблема|ошибка|упало|потеря|блокер|ждёт|зависит от)\b", re.I)
RISK_EN = re.compile(r"\b(risk|danger|broken|fails?|bug|problem|error|crash|loss|blocker|waiting on|depends on|not working)\b", re.I)
LINK = re.compile(r"https?://[^\s)\]>\"']+|(?<![\w.])@[A-Za-z0-9_]{2,30}\b", re.I)

NOISE = re.compile(
    r"^\s*(```|{|}|\[tool|\]|\| *[-:]+ *\|$|<\?xml|import |const |let |function |def |class |return |print\(|curl |git |sudo |scp |ssh |npm |pip |docker |node |python)",
    re.I)
SKIP_WORDS = {"а", "и", "но", "в", "на", "с", "по", "к", "у", "не", "да", "нет", "ок", "окей", "давай",
              "the", "and", "but", "of", "to", "in", "on", "for", "with", "ok", "yes", "no", "well"}

MAX_LINE_LEN = 280

# ---- secret redaction -----------------------------------------------------

_CRED_KW = (r"password|passwd|парол[ья]|токен|token|api[-_ ]?key|api[-_ ]?ключ|"
            r"secret|client[-_]?secret|private[-_ ]?key")
# value after ':' or '=' — always redacted (even short values like 'pass: abc')
_CRED_EQ = re.compile(rf"\b({_CRED_KW})\s*[:=]\s*(?P<val>[^\s,;)\]}}]+)", re.I)
# value after a plain SPACE — only if it looks like a secret (not an ordinary word)
_CRED_SP = re.compile(rf"\b({_CRED_KW})\s+(?P<val>\S+)", re.I)
_CRED_LABEL = re.compile(r"\b(password|парол[ья]|token|токен|secret)\b", re.I)
_BEARER = re.compile(r"\b(bearer|authorization)\s*[:=]?\s*[A-Za-z0-9._\-]{8,}", re.I)
# well-known token prefixes — every alternative consumes the FULL token body, never
# only the prefix (GitHub: ghp_ classic PAT, gho_ OAuth, ghu_ user-to-server,
# ghs_ server-to-server, github_pat_ fine-grained — 36-char base62 bodies)
_HARD_TOKEN = re.compile(
    r"\b(sk-[A-Za-z0-9_\-]{8,}|ghp_[A-Za-z0-9]{20,}|gh[ous]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"glpat-[A-Za-z0-9_\-]{20,}|sk-ant-[A-Za-z0-9_\-]{20,}|xox[baprs]-[A-Za-z0-9\-]{10,}|"
    r"AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{30,}|ya29\.[A-Za-z0-9_\-]{20,})\b")
# generic JWT: eyJ<header>.<payload>.<signature>
_JWT = re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{6,}\b")
# credentials embedded in a URL: scheme://user:pass@host  ->  scheme://<REDACTED: userinfo>@host
_URL_CRED = re.compile(r"(https?://)[^/\s@]+:[^/\s@]*@", re.I)
# canonical multiline PEM (BEGIN/END on separate lines) — handled in condense on the whole text
_PRIVKEY_BLOCK = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]{0,4000}?-----END [A-Z ]*PRIVATE KEY-----")
# single-line PEM without leading '-----' ('BEGIN RSA PRIVATE KEY-----MIIE...-----END RSA PRIVATE KEY-----')
_PEM_INLINE = re.compile(r"\bBEGIN [A-Z0-9 ]*PRIVATE KEY-{3,}[A-Za-z0-9+/=]+-{3,}END [A-Z0-9 ]*PRIVATE KEY-{0,5}", re.I)


def _label_for(kw):
    k = kw.lower()
    if "парол" in k or "pass" in k:
        return "password"
    if "токен" in k or "token" in k:
        return "token"
    if "secret" in k:
        return "secret"
    return "api-key"


def _is_secretlike(val):
    """A value after a plain SPACE must look like a secret, not an ordinary word
    ("server password" is not a secret; "hunter2"/"1234"/"суперсекрет123" are)."""
    if len(val) >= 16:
        return True
    if val.isdigit():
        return len(val) >= 4
    return bool(re.search(r"[0-9A-ZЁ_\-+/=]", val))


def sanitize_line(line, strict=False):
    """Replaces secret values with <REDACTED: ...>; returns (line, found_any).

    Redaction is best-effort by pattern; with strict=True a line that still
    carries a credential marker after the passes is suppressed entirely.
    """
    out = line
    found = False

    # 1) whole tokens/blocks are cut first (found=True so the fallback never re-wraps a marker)
    out = _URL_CRED.sub(lambda m: m.group(1) + "<REDACTED: url-userinfo>@", out)
    out = _JWT.sub(lambda m: "<REDACTED: token>", out)
    out = _PEM_INLINE.sub(lambda m: "<REDACTED: private-key>", out)
    out = _PRIVKEY_BLOCK.sub(lambda m: "<REDACTED: private-key>", out)
    out = _BEARER.sub(lambda m: "<REDACTED: token>", out)
    out = _HARD_TOKEN.sub(lambda m: "<REDACTED: token>", out)
    if out != line:
        found = True

    # 2) "key: value" (EQ — always) and "key value" (SP — secret-like only)
    for rx, eq_sep in ((_CRED_EQ, True), (_CRED_SP, False)):
        def _repl_cred(m, eq_sep=eq_sep):
            nonlocal found
            kw = m.group(1)
            val = m.group("val")
            # placeholder <...> or an already-inserted <REDACTED...> marker — never re-redact
            if val.startswith("<"):
                return m.group(0)
            if not eq_sep and not _is_secretlike(val):
                return m.group(0)
            found = True
            head = m.group(0)[:m.group(0).rfind(val)]
            return f"{head}<REDACTED: {_label_for(kw)}>"
        out = rx.sub(_repl_cred, out)

    # 3) lone keyword on a short line ("pass:", "token: ...") — hide the tail
    if not found and _CRED_LABEL.search(out) and len(re.sub(r"\s+", "", out)) < 40:
        def _repl_short(m):
            nonlocal found
            found = True
            return f"<REDACTED: {_label_for(m.group(1))}>"
        out = re.sub(r"\b(password|парол[ья]|токен|token|secret)\b.*$", _repl_short, out, flags=re.I)
        if out != line:
            found = True

    # 4) strict mode: a credential marker with an unextractable value -> drop the whole line
    if strict and not found and _CRED_LABEL.search(out):
        return "<REDACTED: credential line>", True
    return out, found


# ---- scoring --------------------------------------------------------------

def clean_line(line):
    return re.sub(r"^[\s>#*\-•‣\[\]\d.)]+", "", line).strip()


def line_score(line, tail_bonus=False):
    """Heuristic importance score for a single line."""
    s = 0
    if STRONG_DECISION_RU.search(line) or STRONG_DECISION_EN.search(line):
        s += 6
    if WEAK_DECISION_RU.search(line) or WEAK_DECISION_EN.search(line):
        s += 4
    if TASK_RU.search(line) or TASK_EN.search(line):
        s += 4
    if RISK_RU.search(line) or RISK_EN.search(line):
        s += 3
    if FACT_RU.search(line) or FACT_EN.search(line):
        s += 1
    if LINK.search(line):
        s += 3
    if len(line) < 20 or len(line) > MAX_LINE_LEN:
        s -= 1
    if NOISE.search(line):
        s -= 2
    if tail_bonus:
        s += 1  # final decisions/tasks at the end of the session matter more
    return s


def bucket_of(line):
    strong = STRONG_DECISION_RU.search(line) or STRONG_DECISION_EN.search(line)
    weak = WEAK_DECISION_RU.search(line) or WEAK_DECISION_EN.search(line)
    is_link = bool(LINK.search(line))
    if strong:
        return "decisions"
    if weak and is_link:
        # "agreed, link: ..." is a fact/link, not a decision
        return "facts"
    if weak:
        return "decisions"
    if TASK_RU.search(line) or TASK_EN.search(line):
        return "tasks"
    if RISK_RU.search(line) or RISK_EN.search(line):
        return "risks"
    if is_link or FACT_RU.search(line) or FACT_EN.search(line):
        return "facts"
    return None


def _norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def condense(text, max_lines=500, strict=False):
    """Returns (scored, truncated_count). Considers the start AND the END of the session."""
    # block secrets (multiline PEM keys with BEGIN/END on separate lines) —
    # redacted on the whole text BEFORE the line split, otherwise per-line handling misses them
    text = _PRIVKEY_BLOCK.sub(lambda m: "<REDACTED: private-key>", text)
    raw = [(i, l.rstrip()) for i, l in enumerate(text.splitlines()) if l.strip()]
    total = len(raw)
    truncated = 0
    if total > max_lines * 3:
        head = raw[:max_lines * 2]
        tail = raw[-max_lines:]
        truncated = total - len(head) - len(tail)
        raw = head + tail
    tail_start = total - max_lines  # "end of session" = the last max_lines lines of the ORIGINAL
    scored = []
    for _pos, (orig_i, r) in enumerate(raw):
        line, _red = sanitize_line(clean_line(r), strict=strict)
        if not line or line.lower() in SKIP_WORDS:
            continue
        s = line_score(line, tail_bonus=(orig_i >= tail_start))
        if s >= 3:
            scored.append((s, orig_i, line, bucket_of(line)))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored, truncated


def build_memo(text, max_lines=500, max_items=60, source=None, strict=False):
    picked_all, truncated = condense(text, max_lines, strict)
    picked = picked_all[:max_items]
    buckets = {"decisions": [], "tasks": [], "risks": [], "facts": []}
    for _s, _idx, line, b in picked:
        buckets.setdefault(b or "facts", []).append(line)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    src = os.path.basename(source) if source else "stdin"
    out = ["# Handoff memo (auto-compacted)", ""]
    out.append(f"> context-compactor v{__version__} · {now} · source: {src}")
    out.append("> Auto-compacted from a session transcript. Review before use.")
    out.append("> ⚠️ Redaction is best-effort pattern matching — inspect the memo before sharing it.")
    if truncated:
        out.append(f"> ⚠️ Input truncated: {truncated} lines not considered (head and end of the session were kept).")
    out.append("")
    labels = {"decisions": "✅ Decisions", "tasks": "📌 Open tasks",
              "risks": "⚠️ Risks", "facts": "🔗 Facts & links"}
    for key in ("decisions", "tasks", "risks", "facts"):
        items = buckets[key]
        if not items:
            continue
        seen = set()
        uniq = []
        for it in items:
            n = _norm(it)
            if n in seen:
                continue
            seen.add(n)
            uniq.append(it)
        out.append(f"## {labels[key]}")
        out.append("")
        for it in uniq:
            out.append(f"- {it}")
        out.append("")
    return "\n".join(out)


def self_test():
    sample = (
        "Пользователь: давай сделаем новый скилл для сканера.\n"
        "Ассистент: решили сделать skill-injection-scanner на python, MIT-лицензия, автор Viacheslav Bochkarev.\n"
        "Пользователь: ок, но надо проверить его тестами перед публикацией.\n"
        "Ассистент: риск: без тестов будет много ложных срабатываний.\n"
        "Ассистент: репозиторий проекта: https://github.com/vnbochkarev-netizen/skill-injection-scanner, MIT.\n"
        "Ассистент: договорились, ссылка на CI: https://ci.example.com/build/42 (это ссылка, не решение).\n"
        "Пользователь: давай.\n"
        "```\nconst x = 1;\n```\n"
        "Ассистент: решили: используем продакшен-пароль hunter2 и API ключ AbCdEf123456 для deploy.\n"
        "Ассистент: решили: root-пароль суперсекрет123, применяем на проде.\n"
        "Ассистент: решили: использовать пароль 1234 для всех серверов команды и включить MFA.\n"
        "Ассистент: решили: доступ по https://admin:hunter2secret@db.example.com:5432/prod, креды в урле.\n"
        "Ассистент: решили: токен eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c для API.\n"
        "Ассистент: решили: пароль \"hunter2quoted\" для доступа к панели.\n"
        "Ассистент: решили: REDACTED-SECRET для деплоя в CI.\n"
        "Ассистент: решили: REDACTED-SECRET для вебхуков.\n"
        "Ассистент: решили: REDACTED-SECRET для раннера.\n"
        "Ассистент: договорились: токен ghp_0123456789ABCDEF0123 кладём в env.\n"
        "Ассистент: приватный ключ для сервера:\n"
        "REDACTED-SECRET\n"
        "Ассистент: решили: BEGIN RSA PRIVATE KEY-----MIIEpAIBAAKCAQEA1c3C8f0x-----END RSA PRIVATE KEY----- для доступа по ssh.\n"
        "Ассистент: договорились, завтра публикуем.\n"
    )
    memo = build_memo(sample, source="self-test sample")
    ok_dec = "Decisions" in memo and "skill-injection-scanner" in memo
    ok_task = "Open tasks" in memo and "проверить" in memo
    ok_risk = "Risks" in memo and "ложных срабатываний" in memo
    ok_fact = "Facts" in memo and "github.com" in memo
    ok_noise = "const x = 1" not in memo
    ok_meta = "context-compactor v" in memo and "self-test sample" in memo
    # secret line reached the memo, but with <REDACTED>, no raw value
    ok_red = "<REDACTED" in memo and "hunter2" not in memo and "AbCdEf123456" not in memo
    # Cyrillic secret values are cut too (not an ASCII-only charset!)
    ok_cyr = "суперсекрет123" not in memo
    # short password on a long line ("пароль 1234 ...")
    ok_short = "пароль 1234" not in memo and "1234 для всех серверов" not in memo
    ok_url = "hunter2secret" not in memo and "url-userinfo" in memo
    ok_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in memo
    ok_quoted = "hunter2quoted" not in memo
    # ghp_ token cut
    ok_ghp = "ghp_0123456789ABCDEF0123" not in memo
    # gho_/ghu_/ghs_ tokens cut as WHOLE values — regression: a bare `gho_|ghu_`
    # alternative matched only the prefix and left the full token body in the memo
    ok_gho = "gho_" not in memo and "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" not in memo
    ok_ghu = "ghu_" not in memo and "abcdefghijklmnopqrstuvwxyz0123456789" not in memo
    ok_ghs = "ghs_" not in memo and "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" not in memo
    # strict mode must not keep a line whose credential was only partially consumed
    # (the old prefix-only match set found=True, so --strict kept the leaking line)
    strict_gho = build_memo("decided: REDACTED-SECRET in vault\n",
                            strict=True, source="strict-gho")
    ok_strict_gho = "gho_" not in strict_gho and "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" not in strict_gho
    # every _HARD_TOKEN family must consume its full body — no prefix-only matches
    _fam = {
        "sk-": "REDACTED-SECRET",
        "ghp_": "REDACTED-SECRET",
        "gho_": "REDACTED-SECRET",
        "ghu_": "REDACTED-SECRET",
        "ghs_": "REDACTED-SECRET",
        "github_pat_": "github_pat_ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwx",
        "glpat-": "REDACTED-SECRET",
        "sk-ant-": "REDACTED-SECRET",
        "xoxb-": "REDACTED-SECRET",
        "AKIA": "REDACTED-SECRET",
        "AIza": "REDACTED-SECRETjkl",
        "ya29.": "ya29.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl",
    }
    ok_families = True
    for _prefix, _value in _fam.items():
        _out, _r = sanitize_line(f"decided: {_value} in vault", strict=True)
        ok_families = ok_families and "<REDACTED" in _out and _value[len(_prefix):] not in _out
    # multiline PEM block cut entirely (the <REDACTED: private-key> marker in the memo is legit)
    ok_pem = "BEGIN" not in memo and "MIIEowIB" not in memo
    # single-line PEM without leading '-----' also cut; no double-wrapped markers
    ok_pem_inline = "MIIEpAIB" not in memo and "<REDACTED: <REDACTED" not in memo
    big_pem = "REDACTED-SECRET\n"
    pem_memo = build_memo("Ассистент: решили: ключ:\n" + big_pem, source="pem-big")
    ok_pem_big = "A" * 900 not in pem_memo and "BEGIN PRIVATE KEY" not in pem_memo
    strict_in = "Ассистент: решили: пароль записан в env-файле, доступ только у админа, обсудили всё подробно\n"
    strict_memo = build_memo(strict_in, strict=True, source="strict")
    ok_strict = "env-файле" not in strict_memo and "пароль записан" not in strict_memo
    ok = (ok_dec and ok_task and ok_risk and ok_fact and ok_noise and ok_meta and ok_red
          and ok_cyr and ok_short and ok_url and ok_jwt and ok_quoted and ok_ghp
          and ok_gho and ok_ghu and ok_ghs and ok_strict_gho and ok_families
          and ok_pem and ok_pem_inline and ok_pem_big and ok_strict)
    print(f"SELFTEST: decisions={ok_dec} tasks={ok_task} risks={ok_risk} facts={ok_fact} "
          f"noise_filtered={ok_noise} meta={ok_meta} secrets_redacted={ok_red} cyrillic={ok_cyr} "
          f"short_val={ok_short} url_creds={ok_url} jwt={ok_jwt} quoted={ok_quoted} ghp={ok_ghp} "
          f"gho={ok_gho} ghu={ok_ghu} ghs={ok_ghs} strict_gho={ok_strict_gho} "
          f"token_families={ok_families} "
          f"pem_block={ok_pem} pem_inline={ok_pem_inline} pem_big={ok_pem_big} strict={ok_strict}")
    if not ok:
        print(memo)
    return ok


def main():
    ap = argparse.ArgumentParser(description="Condense a session transcript into a compact handoff memo")
    ap.add_argument("--input", help="path to transcript file (txt/md)")
    ap.add_argument("--output", help="output path (default: stdout)")
    ap.add_argument("--max-lines", type=int, default=500, help="max transcript lines to consider")
    ap.add_argument("--max-items", type=int, default=60, help="max memo items")
    ap.add_argument("--strict", action="store_true",
                    help="redact whole lines that still carry a credential marker (conservative)")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)

    if not args.input:
        ap.print_help()
        sys.exit(2)
    # consent/warning at the point of execution: what we read and where output goes
    print(f"⚠️ context-compactor v{__version__} will read: {args.input}", file=sys.stderr)
    print("   Transcript content is processed locally; no data leaves the machine.", file=sys.stderr)
    print("   Redaction is best-effort — review the memo before sharing it.", file=sys.stderr)
    if args.output:
        print(f"   Memo will be written to: {args.output}", file=sys.stderr)
    try:
        with open(args.input, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as e:
        print(f"Failed to read {args.input}: {e}", file=sys.stderr)
        sys.exit(2)

    memo = build_memo(text, args.max_lines, args.max_items, source=args.input, strict=args.strict)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(memo)
        print(f"Done: {args.output} ({len(memo)} chars)")
    else:
        print(memo)


if __name__ == "__main__":
    main()
