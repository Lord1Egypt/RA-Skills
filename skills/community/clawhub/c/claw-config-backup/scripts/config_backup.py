import sys
import json5
import shutil
import hashlib
import argparse
from datetime import datetime
from pathlib import Path


# =========================
# 🔹 计算文件 hash
# =========================
def file_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# =========================
# 🔹 校验 JSON5
# =========================
def validate_json5(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json5.load(f)
        return True, None
    except Exception as e:
        return False, str(e)


# =========================
# 🔹 获取最新备份文件
# =========================
def get_latest_backup(backup_dir, stem, suffix):
    files = sorted(
        backup_dir.glob(f"{stem}_*{suffix}"),
        #key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    return files[0] if files else None


# =========================
# 🔹 主逻辑
# =========================
def process(file_path, backup_dir):
    file_path = Path(file_path)
    backup_dir = Path(backup_dir)

    # 1️⃣ 校验 JSON5
    valid, err = validate_json5(file_path)
    if not valid:
        print(f"❌ JSON5 无效: {err}")
        return

    print("✅ JSON5 validate passed")

    # 2️⃣ 准备 backup 目录
    backup_dir.mkdir(parents=True, exist_ok=True)

    # 3️⃣ 当前文件 hash
    current_hash = file_hash(file_path)

    # 4️⃣ 找最新备份
    latest = get_latest_backup(backup_dir, file_path.stem, file_path.suffix)

    if latest:
        latest_hash = file_hash(latest)

        if latest_hash == current_hash:
            print("⚠️ config file unchange, skip backup")
            return

    # 5️⃣ 创建新备份
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_file = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"

    #shutil.copy2(file_path, backup_file)
    try:
        shutil.copy2(file_path, backup_file)
    except OSError as e:
        print(f"❌ 备份失败: {e}")
        return False

    print(f"📦 已备份: {backup_file}")


# =========================
# 🔹 CLI 入口
# =========================
def main():
    parser = argparse.ArgumentParser(
        description="Validate JSON5 and backup with hash check"
    )

    parser.add_argument(
        "file",
        help="JSON5 文件路径"
    )

    parser.add_argument(
        "-o", "--output",
        default="backup",
        help="备份目录（默认: backup）"
    )

    args = parser.parse_args()

    if not process(args.file, args.output):
        sys.exit(1)


if __name__ == "__main__":
    main()
