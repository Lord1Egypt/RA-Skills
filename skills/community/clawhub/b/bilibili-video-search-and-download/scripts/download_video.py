import subprocess
import sys
from pathlib import Path

DOWNLOAD_DIR = Path("downloads")


def download_video(url: str, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"正在下载: {url}")
    result = subprocess.run(
        [
            sys.executable, "-m", "yt_dlp",
            "-o", str(output_dir / "%(title)s.%(ext)s"),
            "--merge-output-format", "mp4",
            "--write-thumbnail",
            "--embed-thumbnail",
            "--embed-metadata",
            "--print", "after_move:filename",
            url,
        ],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        print(f"下载失败: {result.stderr.strip()}")
        sys.exit(1)

    out_path = result.stdout.strip()
    if not out_path:
        print("下载失败: 无法获取输出文件路径")
        sys.exit(1)

    out_file = Path(out_path)
    if not out_file.exists():
        print(f"下载失败: 文件不存在 — {out_path}")
        sys.exit(1)
    if out_file.stat().st_size == 0:
        print(f"下载失败: 文件为空 — {out_path}")
        sys.exit(1)

    print(f"下载完成: {out_path} ({out_file.stat().st_size / 1024 / 1024:.1f}MB)")


def main():
    if len(sys.argv) < 2:
        print("用法: python download_video.py <B站视频URL 或 BV号>")
        print("示例: python download_video.py https://www.bilibili.com/video/BV1qD4y1U7fs")
        print("示例: python download_video.py BV1qD4y1U7fs")
        sys.exit(1)

    arg = sys.argv[1]
    if arg.startswith("BV"):
        url = f"https://www.bilibili.com/video/{arg}"
    else:
        url = arg

    download_video(url, DOWNLOAD_DIR)


if __name__ == "__main__":
    main()
