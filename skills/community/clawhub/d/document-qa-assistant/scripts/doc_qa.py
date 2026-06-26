#!/usr/bin/env python3
"""Document QA — 基于文档回答问题"""
import argparse, os, sys, json

def read_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md"):
        with open(path, encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        try:
            import subprocess
            result = subprocess.run(["python3", "-c",
                f"import pdfplumber; print(pdfplumber.open('{path}').pages[0].extract_text())"],
                capture_output=True, text=True)
            return result.stdout or "[PDF读取失败]"
        except:
            return "[PDF解析不可用]"
    else:
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except:
            return f"[无法读取: {path}]"

def search_in_content(question: str, content: str, context_lines: int = 20) -> list:
    q_words = [w for w in question if len(w) > 1]
    lines = content.splitlines()
    scores = []
    for i, line in enumerate(lines):
        score = sum(1 for w in q_words if w in line.lower())
        if score > 0:
            start = max(0, i - context_lines // 2)
            end = min(len(lines), i + context_lines // 2)
            scores.append((score, "\n".join(lines[start:end]), i+1))
    scores.sort(reverse=True)
    return scores[:5]

def qa(question: str, docs_path: str, context_len: int = 20) -> dict:
    if os.path.isdir(docs_path):
        files = [os.path.join(docs_path, f) for f in os.listdir(docs_path)
                 if os.path.isfile(os.path.join(docs_path, f))]
    else:
        files = [docs_path]
    all_results = []
    for f in files:
        content = read_file(f)
        results = search_in_content(question, content, context_len)
        for score, excerpt, line in results:
            all_results.append({"file": f, "line": line, "score": score, "excerpt": excerpt[:300]})
    all_results.sort(key=lambda x: x["score"], reverse=True)
    top = all_results[:3]
    answer = f"根据检索结果，最相关的回答来自：\n"
    for r in top:
        answer += f"- {r['file']} (第{r['line']}行, 相关度:{r['score']})\n  {r['excerpt'][:150]}...\n"
    return {"answer": answer, "sources": top, "confidence": "high" if top else "low"}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--docs", required=True)
    p.add_argument("--question", required=True)
    p.add_argument("--context-len", type=int, default=20)
    args = p.parse_args()
    result = qa(args.question, args.docs, args.context_len)
    print(result["answer"])
    print(f"\n[来源 {len(result['sources'])} 条]")
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
