#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全盘扫描 AI Agent 安装目录与会话记录存储位置（环境无关版）。

覆盖范围：用户主目录、AppData、WSL 家目录、其他磁盘项目目录。
输出：$OUTPUT_DIR/agent_scan_report.json
"""
import os, sys, json, re, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HOME, all_homes, appdata_roots, extra_disk_roots, out_dir

OUT = os.path.join(out_dir(), "agent_scan_report.json")

AGENT_DEFS = {
    "Claude Code": ["claude"], "OpenAI Codex": ["codex"], "WorkBuddy": ["workbuddy"],
    "CodeBuddy": ["codebuddy"], "dsh": ["dsh"], "DeepSeek": ["deepseek"],
    "Kimi": ["kimi"], "Cursor": ["cursor"], "Trae": ["trae"], "Qoder": ["qoder"],
    "Lingma": ["lingma"], "GitHub Copilot": ["copilot"], "Gemini": ["gemini"],
    "Aider": ["aider"], "opencode": ["opencode"], "Windsurf": ["windsurf"],
    "Cline": ["cline"], "Continue": ["continue"], "Junie": ["junie"],
    "MarsCode": ["marscode"], "CodeGPT": ["codegpt"], "CodeGraph": ["codegraph"],
    "OpenAkita": ["openakita"], "Ollama": ["ollama"], "LM Studio": ["lmstudio"],
    "Cherry Studio": ["cherry"], "Dokobot": ["dokobot"], "SheetAgent": ["sheetagent"],
    "ZCode": ["zcode"], "Kimi Code": ["kimicode", "kimi-code"],
    "OpenClaw": ["openclaw", "clawdbot", "moltbot"], "Hermes": ["hermes"],
    "Qwen Code": ["qwen-code", "qwencode"], "Kiro": ["kiro"],
    "Roo Code": ["roo-code", "roocline"], "Gemini CLI": ["gemini-cli"],
    "Amp": ["amp"], "Augment Code": ["augment"],
}

SESSION_DIR_RE = re.compile(
    r"(session|project|conversation|chat|history|thread|rollout|transcript|dialog|workspace)", re.I)
SESSION_NAME_RE = re.compile(
    r"(session|conversation|chat|history|thread|rollout|transcript|dialog|message|turn|prompt)", re.I)
SESSION_EXT = {".jsonl", ".db", ".sqlite", ".sqlite3", ".vscdb", ".json"}
NOISE_DIRS = {
    "node_modules", ".git", "Cache_Data", "GPUCache", "Code Cache",
    "DawnGraphiteCache", "DawnWebGPUCache", "Crashpad", "Dictionaries",
    "_locales", "extensions", "test", "tests", "fixtures", "bin", "locales",
}
NOISE_FILE_RE = re.compile(r"^(messages|package|manifest|settings|config|keybindings|state)\.json$", re.I)


def walk_depth(root, maxdepth):
    root = root.rstrip("\\/")
    base_depth = root.count(os.sep)
    for dp, dns, fns in os.walk(root, topdown=True, onerror=lambda e: None):
        dns[:] = [d for d in dns if d not in NOISE_DIRS]
        yield dp, dns, fns
        if dp.count(os.sep) - base_depth >= maxdepth:
            dns[:] = []


def is_session_file(name, parent_dir, ext):
    if NOISE_FILE_RE.match(name) or ext.lower() not in SESSION_EXT:
        return False
    if SESSION_NAME_RE.search(os.path.splitext(name)[0]):
        return True
    if SESSION_DIR_RE.search(parent_dir) and ext.lower() == ".jsonl":
        return True
    return False


def scan_agent_root(root):
    session_dirs, session_files = [], []
    for dp, dns, fns in walk_depth(root, 7):
        dname = os.path.basename(dp)
        cnt = sz = 0
        cur = []
        for f in fns:
            if is_session_file(f, dname, os.path.splitext(f)[1]):
                p = os.path.join(dp, f)
                try:
                    fs = os.path.getsize(p)
                except OSError:
                    fs = 0
                cur.append({"path": p, "size_kb": round(fs / 1024, 1)})
                cnt += 1
                sz += fs
        if (SESSION_DIR_RE.search(dname) and dname.lower() not in NOISE_DIRS) or \
           sum(1 for f in fns if f.lower().endswith(".jsonl")) >= 3:
            if cnt:
                session_dirs.append({"path": dp, "files": cnt, "size_kb": round(sz / 1024, 1)})
        session_files.extend(cur)
    return session_dirs, session_files


def agent_name(low):
    for agent, kws in AGENT_DEFS.items():
        if any(kw in low for kw in kws):
            return agent
    return None


def main():
    t0 = time.time()
    agents = {}
    # 1) 各 home 顶层的 agent 特征目录
    hosts = all_homes() + appdata_roots()
    for host in dict.fromkeys(hosts):
        try:
            entries = list(os.scandir(host))
        except OSError:
            continue
        for e in entries:
            if not e.is_dir():
                continue
            name = agent_name(e.name.lower())
            if name:
                agents.setdefault(name, []).append(e.path)

    # 2) 其他磁盘的项目级 .claude / .codex（两级）
    for drv in extra_disk_roots():
        try:
            e1s = list(os.scandir(drv))
        except OSError:
            continue
        for e1 in e1s:
            if not e1.is_dir():
                continue
            candidates = [e1.path]
            try:
                candidates += [e2.path for e2 in os.scandir(e1.path) if e2.is_dir()]
            except OSError:
                pass
            for c in candidates:
                name = agent_name(os.path.basename(c).lower())
                if name:
                    agents.setdefault(name, []).append(c)

    for k in agents:
        agents[k] = sorted(set(agents[k]))

    report = {"scan_time": time.strftime("%Y-%m-%d %H:%M:%S"),
              "env": {"home": HOME, "wsl_homes": [h for h in all_homes() if "wsl" in h.lower()]},
              "agents": {}}
    for agent, roots in agents.items():
        entry = {"roots": roots, "session_dirs": [], "session_files": []}
        for r in roots:
            sd, sf = scan_agent_root(r)
            entry["session_dirs"].extend(sd)
            entry["session_files"].extend(sf)
        report["agents"][agent] = entry
        print(f"[{agent}] roots={len(roots)} dirs={len(entry['session_dirs'])} files={len(entry['session_files'])}")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nDONE in {time.time()-t0:.1f}s -> {OUT}")


if __name__ == "__main__":
    main()
