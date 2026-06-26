"""file-sorter 核心实现：解压、匹配、分类、移动"""
import json, os, re, shutil, sys, time, io
from pathlib import Path

# Windows 终端 GBK 编码兼容：强制 stdout/stderr 使用 UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
RULES_FILE = SCRIPT_DIR / "rules.json"

# ── 规则管理 ──────────────────────────────────────────────

DEFAULT_CONFIG = {
    "rules": [],
    "settings": {"unmatched_dir": "_未分类", "conflict_strategy": "rename"},
}

def load_config():
    if not RULES_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def add_rule(name, keywords, target_dir, match_mode="contains"):
    config = load_config()
    config["rules"].append({
        "name": name, "keywords": keywords,
        "target_dir": target_dir, "match_mode": match_mode,
    })
    save_config(config)
    return config

def delete_rule(name):
    config = load_config()
    config["rules"] = [r for r in config["rules"] if r["name"] != name]
    save_config(config)
    return config

def list_rules():
    config = load_config()
    return config["rules"], config["settings"]

# ── 安全校验 ─────────────────────────────────────────────

def _validate_member_path(member_name, dest):
    """校验归档成员路径，防止路径遍历攻击。
    拒绝绝对路径和包含 '..' 的路径，确保解压目标在 dest 内。"""
    # 拒绝绝对路径
    if os.path.isabs(member_name):
        raise ValueError(f"安全拒绝: 归档包含绝对路径成员 '{member_name}'")
    # 拒绝 .. 路径遍历
    normalized = os.path.normpath(member_name)
    if normalized.startswith("..") or "/.." in normalized or "\\.." in normalized:
        raise ValueError(f"安全拒绝: 归档包含路径遍历成员 '{member_name}'")
    # 最终确认解压目标在 dest 目录内
    target = (dest / normalized).resolve()
    dest_resolved = dest.resolve()
    if not str(target).startswith(str(dest_resolved)):
        raise ValueError(f"安全拒绝: 成员 '{member_name}' 解压后会逃逸到目标目录外")

def _validate_all_members(names, dest):
    """批量校验所有成员路径，有任何危险成员则中止解压。"""
    dangerous = []
    for name in names:
        try:
            _validate_member_path(name, dest)
        except ValueError as e:
            dangerous.append(str(e))
    if dangerous:
        raise ValueError(
            f"归档包含 {len(dangerous)} 个危险成员，已中止解压:\n" +
            "\n".join(dangerous[:10]) +
            ("\n..." if len(dangerous) > 10 else "")
        )

# ── 解压 ─────────────────────────────────────────────────

def extract(archive_path, dest_dir=None, password=None):
    """安全解压压缩文件，返回 (解压目录Path, 文件列表)。
    所有格式在解压前校验成员路径，拒绝绝对路径和 '..' 路径遍历。
    原生支持 zip/tar/tar.gz/tar.bz2；rar/7z 需要 py7zr/rarfile 或命令行工具。"""
    archive = Path(archive_path).resolve()
    if not archive.exists():
        raise FileNotFoundError(f"文件不存在: {archive}")

    if dest_dir is None:
        ts = int(time.time())
        dest_dir = archive.parent / f"_temp_sort_{ts}"
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    suffix = archive.name.lower()

    if suffix.endswith(".zip"):
        import zipfile
        with zipfile.ZipFile(archive, "r") as zf:
            _validate_all_members(zf.namelist(), dest)
            if password:
                zf.setpassword(password.encode())
            zf.extractall(dest)

    elif suffix.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar")):
        import tarfile
        with tarfile.open(archive, "r:*") as tf:
            names = [m.name for m in tf.getmembers()]
            _validate_all_members(names, dest)
            # 逐个安全提取：跳过符号链接和设备文件
            for member in tf.getmembers():
                if member.issym() or member.islnk():
                    print(f"⚠️ 跳过符号链接: {member.name}")
                    continue
                if not (member.isfile() or member.isdir()):
                    print(f"⚠️ 跳过特殊文件: {member.name}")
                    continue
                tf.extract(member, dest)

    elif suffix.endswith(".7z"):
        try:
            import py7zr
            with py7zr.SevenZipFile(archive, "r", password=password) as sz:
                _validate_all_members(sz.getnames(), dest)
                sz.extractall(dest)
        except ImportError:
            _run_cmd(["7z", "x", str(archive), f"-o{dest}",
                       f"-p{password}" if password else "", "-y"])
            # 命令行解压后校验结果
            _verify_extracted_files(dest)

    elif suffix.endswith(".rar"):
        try:
            import rarfile
            with rarfile.RarFile(archive, "r") as rf:
                _validate_all_members(rf.namelist(), dest)
                rf.extractall(dest, pwd=password)
        except ImportError:
            _run_cmd(["unrar", "x", "-y",
                       f"-p{password}" if password else "-p-", str(archive), str(dest) + "/"])
            _verify_extracted_files(dest)
    else:
        raise ValueError(f"不支持的格式: {archive.suffix}")

    files = [p for p in dest.rglob("*") if p.is_file()]
    return dest, files

def _verify_extracted_files(dest):
    """命令行工具解压后，校验所有文件确实在 dest 目录内。"""
    dest_resolved = dest.resolve()
    for p in dest.rglob("*"):
        if not str(p.resolve()).startswith(str(dest_resolved)):
            raise ValueError(f"安全拒绝: 解压后发现逃逸文件 '{p}'")

def _run_cmd(cmd):
    import subprocess
    cmd = [c for c in cmd if c]  # 去掉空字符串
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"命令失败: {' '.join(cmd)}\n{r.stderr}")

# ── 匹配分类 ─────────────────────────────────────────────

def match_file(filename, rules):
    """按规则顺序匹配文件名，返回首条命中的规则 name，未命中返回 None。"""
    name_lower = filename.lower()
    for rule in rules:
        mode = rule.get("match_mode", "contains")
        for kw in rule["keywords"]:
            kw_lower = kw.lower()
            if mode == "contains" and kw_lower in name_lower:
                return rule["name"]
            elif mode == "startswith" and name_lower.startswith(kw_lower):
                return rule["name"]
            elif mode == "endswith" and name_lower.endswith(kw_lower):
                return rule["name"]
            elif mode == "regex" and re.search(kw, filename, re.IGNORECASE):
                return rule["name"]
    return None

def classify(files, rules, settings):
    """对文件列表执行分类，返回 [(文件Path, 规则名/None, 目标子目录)] 列表。"""
    rule_map = {r["name"]: r["target_dir"] for r in rules}
    unmatched = settings.get("unmatched_dir", "_未分类")
    results = []
    for f in files:
        matched = match_file(f.name, rules)
        target = rule_map[matched] if matched else unmatched
        results.append((f, matched, target))
    return results

# ── 移动文件 ─────────────────────────────────────────────

def move_files(classified, output_dir, conflict_strategy="rename"):
    """将分类结果移动到 output_dir 下对应子目录。返回 (成功数, 跳过数)。"""
    out = Path(output_dir)
    ok, skipped = 0, 0
    for src, _rule, sub in classified:
        dst_dir = out / sub
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / src.name

        if dst.exists():
            if conflict_strategy == "skip":
                skipped += 1; continue
            elif conflict_strategy == "rename":
                dst = _unique_name(dst)
            # overwrite: 直接覆盖

        shutil.move(str(src), str(dst))
        ok += 1
    return ok, skipped

def _unique_name(path):
    stem, suffix = path.stem, path.suffix
    i = 1
    while path.exists():
        path = path.parent / f"{stem}_{i}{suffix}"
        i += 1
    return path

# ── 报告生成 ──────────────────────────────────────────────

def generate_report(archive_name, classified):
    """生成 Markdown 格式的分类报告字符串。"""
    total = len(classified)
    lines = [f"📂 分类报告 — {archive_name}（共 {total} 个文件）\n"]
    lines.append("| # | 文件名 | 匹配规则 | 目标目录 |")
    lines.append("|---|--------|----------|----------|")
    stats = {}
    for i, (f, rule, target) in enumerate(classified, 1):
        label = rule if rule else "⚠️ 未匹配"
        lines.append(f"| {i} | {f.name} | {label} | {target}/ |")
        stats[label] = stats.get(label, 0) + 1
    summary = " | ".join(f"{k} {v} 个" for k, v in stats.items())
    lines.append(f"\n📊 统计：{summary}")
    return "\n".join(lines)

# ── CLI 入口 ──────────────────────────────────────────────

def main():
    """命令行接口：python file_sorter.py <command> [args...]
    命令:
      init                          初始化 rules.json
      add <name> <keywords> <dir> [mode]  添加规则 (keywords 逗号分隔)
      delete <name>                 删除规则
      list                          列出所有规则
      classify <archive> <output>   分类文件（仅预览）
      execute <archive> <output>    分类并移动文件
    """
    if len(sys.argv) < 2:
        print(main.__doc__); return

    cmd = sys.argv[1]

    if cmd == "init":
        config = load_config()
        print(json.dumps(config, ensure_ascii=False, indent=2))

    elif cmd == "add":
        name, kws, tdir = sys.argv[2], sys.argv[3].split(","), sys.argv[4]
        mode = sys.argv[5] if len(sys.argv) > 5 else "contains"
        add_rule(name, kws, tdir, mode)
        print(f"已添加规则: {name}")

    elif cmd == "delete":
        delete_rule(sys.argv[2])
        print(f"已删除规则: {sys.argv[2]}")

    elif cmd == "list":
        rules, settings = list_rules()
        print(json.dumps({"rules": rules, "settings": settings}, ensure_ascii=False, indent=2))

    elif cmd in ("classify", "execute"):
        archive, output = sys.argv[2], sys.argv[3]
        password = sys.argv[4] if len(sys.argv) > 4 else None
        rules, settings = list_rules()
        if not rules:
            print("错误: 没有分类规则，请先添加规则"); sys.exit(1)
        dest, files = extract(archive, password=password)
        classified = classify(files, rules, settings)
        report = generate_report(Path(archive).name, classified)
        print(report)
        if cmd == "execute":
            ok, skip = move_files(classified, output, settings.get("conflict_strategy", "rename"))
            print(f"\n✅ 完成: 移动 {ok} 个文件, 跳过 {skip} 个")
            # 清理临时目录
            shutil.rmtree(dest, ignore_errors=True)
            print(f"🗑️ 已清理临时目录: {dest}")
        else:
            print(f"\n📌 预览模式，文件未移动。临时目录: {dest}")
    else:
        print(f"未知命令: {cmd}"); print(main.__doc__)

if __name__ == "__main__":
    main()
