#!/usr/bin/env python3
"""
词库更新脚本 - 从多个 GitHub 开源词库拉取最新内容合并到本地
每天第一次使用时自动触发

词库来源:
  - konsheng/Sensitive-lexicon (广告、政治、暴恐、色情、涉枪涉爆等)
  - bigdata-labs/sensitive-stop-words (广告、政治、色情、涉枪涉爆)
  - jkiss/sensitive-words (广告、政治、色情)
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

# 词库保存目录（Skill 所在目录的 data/ 子目录）
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
STATE_FILE = DATA_DIR / ".update_state.json"
WORDS_FILE = DATA_DIR / "sensitive_words.txt"

# 上游 raw 文件地址
SOURCES = [
    # konsheng/Sensitive-lexicon
    ("konsheng/Sensitive-lexicon", "广告类型", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E5%B9%BF%E5%91%8A%E7%B1%BB%E5%9E%8B.txt"),
    ("konsheng/Sensitive-lexicon", "政治类型", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E6%94%BF%E6%B2%BB%E7%B1%BB%E5%9E%8B.txt"),
    ("konsheng/Sensitive-lexicon", "暴恐词库", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E6%9A%B4%E6%81%90%E8%AF%8D%E5%BA%93.txt"),
    ("konsheng/Sensitive-lexicon", "色情词库", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E8%89%B2%E6%83%85%E8%AF%8D%E5%BA%93.txt"),
    ("konsheng/Sensitive-lexicon", "涉枪涉爆", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E6%B6%89%E6%9E%AA%E6%B6%89%E7%88%86.txt"),
    ("konsheng/Sensitive-lexicon", "其他词库", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E5%85%B6%E4%BB%96%E8%AF%8D%E5%BA%93.txt"),
    ("konsheng/Sensitive-lexicon", "补充词库", "https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/%E8%A1%A5%E5%85%85%E8%AF%8D%E5%BA%93.txt"),
    # bigdata-labs/sensitive-stop-words
    ("bigdata-labs/sensitive-stop-words", "广告", "https://raw.githubusercontent.com/bigdata-labs/sensitive-stop-words/master/%E5%B9%BF%E5%91%8A.txt"),
    ("bigdata-labs/sensitive-stop-words", "政治类", "https://raw.githubusercontent.com/bigdata-labs/sensitive-stop-words/master/%E6%94%BF%E6%B2%BB%E7%B1%BB.txt"),
    ("bigdata-labs/sensitive-stop-words", "色情类", "https://raw.githubusercontent.com/bigdata-labs/sensitive-stop-words/master/%E8%89%B2%E6%83%85%E7%B1%BB.txt"),
    ("bigdata-labs/sensitive-stop-words", "涉枪涉爆违法信息关键词", "https://raw.githubusercontent.com/bigdata-labs/sensitive-stop-words/master/%E6%B6%89%E6%9E%AA%E6%B6%89%E7%88%86%E8%BF%9D%E6%B3%95%E4%BF%A1%E6%81%AF%E5%85%B3%E9%94%AE%E8%AF%8D.txt"),
    # jkiss/sensitive-words
    ("jkiss/sensitive-words", "广告", "https://raw.githubusercontent.com/jkiss/sensitive-words/master/%E5%B9%BF%E5%91%8A.txt"),
    ("jkiss/sensitive-words", "政治类", "https://raw.githubusercontent.com/jkiss/sensitive-words/master/%E6%94%BF%E6%B2%BB%E7%B1%BB.txt"),
    ("jkiss/sensitive-words", "色情类", "https://raw.githubusercontent.com/jkiss/sensitive-words/master/%E8%89%B2%E6%83%85%E7%B1%BB.txt"),
]

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {}

def save_state(state: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def needs_update() -> bool:
    """判断今天是否还没更新过"""
    state = load_state()
    return state.get("last_update") != str(date.today())

def fetch_words(url: str) -> set:
    """从 URL 拉取词库，自动检测编码，返回词条集合"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()

        # 自动检测编码（支持 UTF-16 BOM / UTF-8 BOM / GBK）
        if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
            content = raw.decode("utf-16", errors="ignore")
        elif raw[:3] == b"\xef\xbb\xbf":
            content = raw.decode("utf-8-sig", errors="ignore")
        else:
            # 优先 utf-8，失败降级 gbk
            try:
                content = raw.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                content = raw.decode("gbk", errors="ignore")

        words = set()
        for line in content.splitlines():
            # 去掉注释、空行、逗号（bigdata-labs 词库有尾随逗号）
            word = line.strip().rstrip(",")
            if word and not word.startswith("#") and len(word) >= 2:
                # 过滤掉全 ASCII 乱码行（UTF-16 解码残留）
                if any("\u4e00" <= c <= "\u9fff" for c in word) or any(c.isalpha() for c in word):
                    words.add(word)
        return words
    except urllib.error.URLError as e:
        print(f"  ⚠️  拉取失败: {url} → {e}", file=sys.stderr)
        return set()

def update_words(force: bool = False) -> bool:
    """
    更新词库。返回 True 表示更新了，False 表示跳过（今天已更新）。
    force=True 强制更新。
    """
    if not force and not needs_update():
        return False

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("🔄 正在更新违禁词库...")

    all_words: set = set()
    ok_count = 0

    for repo, name, url in SOURCES:
        print(f"  📥 {repo} / {name}...", end=" ", flush=True)
        words = fetch_words(url)
        if words:
            all_words |= words
            print(f"{len(words)} 词")
            ok_count += 1
        else:
            print("跳过")

    # 保留旧词库（网络失败时不清空）
    if ok_count == 0:
        print("⚠️  所有词库拉取失败，保留本地缓存", file=sys.stderr)
        save_state({"last_update": str(date.today()), "word_count": _count_local()})
        return False

    # 写入合并后的词库（排序去重）
    sorted_words = sorted(all_words)
    WORDS_FILE.write_text("\n".join(sorted_words) + "\n", encoding="utf-8")

    state = {"last_update": str(date.today()), "word_count": len(sorted_words)}
    save_state(state)
    print(f"✅ 词库更新完成：共 {len(sorted_words):,} 词（来自 {ok_count}/{len(SOURCES)} 个来源）")
    return True

def _count_local() -> int:
    if WORDS_FILE.exists():
        return sum(1 for line in WORDS_FILE.read_text().splitlines() if line.strip())
    return 0

def load_words() -> set:
    """加载本地词库，返回集合"""
    if not WORDS_FILE.exists():
        return set()
    return set(
        line.strip()
        for line in WORDS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )

def status() -> dict:
    state = load_state()
    return {
        "last_update": state.get("last_update", "从未更新"),
        "word_count": state.get("word_count", _count_local()),
        "words_file": str(WORDS_FILE),
        "needs_update": needs_update(),
    }

if __name__ == "__main__":
    force = "--force" in sys.argv
    updated = update_words(force=force)
    if not updated and not force:
        s = status()
        print(f"ℹ️  今日已更新（{s['last_update']}），词库共 {s['word_count']:,} 词。跳过更新。")
        print("  使用 --force 强制重新拉取")
