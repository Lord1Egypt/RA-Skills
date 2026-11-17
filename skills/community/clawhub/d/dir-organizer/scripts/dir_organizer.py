import argparse, json, os, shutil, sys

MAP = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".heic"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".epub"],
    "表格": [".xls", ".xlsx", ".csv", ".ods"],
    "演示": [".ppt", ".pptx", ".key"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "视频": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "代码": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".sh", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".sql"],
}

def cat_of(ext):
    for cat, exts in MAP.items():
        if ext in exts:
            return cat
    return "其他"

def main():
    ap = argparse.ArgumentParser(description="dir-organizer · 按类型整理目录（默认预览，--apply 才移动）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--apply", action="store_true", help="执行移动（缺省只预览）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    plan = []
    for f in sorted(os.listdir(a.dir)):
        p = os.path.join(a.dir, f)
        if not os.path.isfile(p):
            continue
        cat = cat_of(os.path.splitext(f)[1].lower())
        plan.append((p, os.path.join(a.dir, cat, f)))
    moved = 0
    if a.apply:
        for src, dst in plan:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst); moved += 1
    if a.json:
        print(json.dumps({"mode": "apply" if a.apply else "dry-run", "moved": moved,
                          "plan": [{"file": os.path.basename(s), "to": os.path.basename(os.path.dirname(d))} for s, d in plan]},
                         ensure_ascii=False, indent=2))
    else:
        print("模式: %s ｜ 计划归类 %d 个文件" % ("APPLY" if a.apply else "DRY-RUN 预览", len(plan)))
        for s, d in plan:
            print("  %s -> %s/" % (os.path.basename(s), os.path.basename(os.path.dirname(d))))
        if not a.apply:
            print("预览完成，加 --apply 执行（文件只移动不删除）")
    sys.exit(0)

if __name__ == "__main__":
    main()
