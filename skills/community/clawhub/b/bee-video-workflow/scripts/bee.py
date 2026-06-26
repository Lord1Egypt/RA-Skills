#!/usr/bin/env python3
"""
🐝 Bee — 视频全流程自动化
下载 → 截封面 → OSS上传 → 蚁小二发布 → 飞书记录

用法:
  python3 bee.py run "链接或路径" [--title T] [--desc D] [--tags '["t1"]']
                                  [--publish 目标] [--platform 平台] [--draft]
                                  [--no-feishu] [--no-oss] [--cover 封面路径]
  python3 bee.py accounts          查看蚁小二账号
  python3 bee.py status <id>       查看发布状态
"""

import os, sys, json, time, subprocess, hashlib, re, shutil, argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# ============================================================
# 配置
# ============================================================
WORK_DIR = Path(__file__).parent.parent / "workspace"
WORK_DIR.mkdir(exist_ok=True)

# OSS
OSS_KEY_ID     = os.environ.get("OSS_ACCESS_KEY_ID", "")
OSS_KEY_SECRET = os.environ.get("OSS_ACCESS_KEY_SECRET", "")
OSS_BUCKET     = os.environ.get("OSS_BUCKET_NAME", "")
OSS_ENDPOINT   = os.environ.get("OSS_ENDPOINT", "")
OSS_PREFIX     = os.environ.get("OSS_PREFIX", "bee/")

# 蚁小二
YXE_TOKEN = os.environ.get("YIXIAOER_TOKEN", "")
YXE_BASE  = os.environ.get("YIXIAOER_BASE_URL", "https://www.yixiaoer.cn/api")
YXE_SCRIPT = Path(__file__).parent.parent.parent / "yixiaoer-pro" / "scripts" / "upload_and_publish.py"

# 飞书多维表格
BITABLE_APP_TOKEN = "Lv3fbmpWGacqhosSRtXct9EnnVd"
BITABLE_TABLE_ID  = "tblWsUQPqlAYsnV3"


# ============================================================
# 工具函数
# ============================================================
def log(emoji, msg):
    print(f"{emoji} {msg}", flush=True)

def run_cmd(cmd, timeout=300):
    """运行命令并返回 (returncode, stdout, stderr)"""
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr

def ffprobe_info(video_path):
    """获取视频元信息"""
    code, out, _ = run_cmd([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=width,height,codec_name,codec_type",
        "-of", "json", str(video_path)
    ])
    if code != 0:
        return {}
    try:
        data = json.loads(out)
        fmt = data.get("format", {})
        video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
        return {
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "codec": video_stream.get("codec_name"),
            "duration": round(float(fmt.get("duration", 0))),
            "size": int(fmt.get("size", 0)),
            "bitrate": int(fmt.get("bit_rate", 0)),
        }
    except:
        return {}

def extract_cover(video_path, output_path, timestamp="00:00:02"):
    """从视频截取封面"""
    code, _, err = run_cmd([
        "ffmpeg", "-y", "-i", str(video_path),
        "-ss", timestamp, "-vframes", "1",
        "-q:v", "2", str(output_path)
    ])
    if code != 0:
        # 如果 2 秒处失败，试 0 秒
        code, _, _ = run_cmd([
            "ffmpeg", "-y", "-i", str(video_path),
            "-ss", "00:00:00", "-vframes", "1",
            "-q:v", "2", str(output_path)
        ])
    return Path(output_path).exists()


# ============================================================
# Step 1: 下载视频
# ============================================================
def download_video(source):
    """
    下载或识别视频来源
    返回: {"path": str, "title": str, "author": str, "source_url": str}
    """
    source = source.strip()

    # 本地文件
    if os.path.isfile(source):
        log("📁", f"本地文件: {source}")
        return {
            "path": source,
            "title": Path(source).stem,
            "author": "",
            "source_url": "",
        }

    # URL — 先试 yt-dlp（通用下载器）
    if source.startswith("http"):
        log("📥", f"下载: {source}")

        output_dir = WORK_DIR / "downloads"
        output_dir.mkdir(exist_ok=True)

        # 生成唯一文件名
        url_hash = hashlib.md5(source.encode()).hexdigest()[:10]
        output_tpl = str(output_dir / f"%(id)s_{url_hash}.%(ext)s")
        info_file = output_dir / f"{url_hash}.info.json"

        # cookies 文件（如果有）
        cookie_file = Path(__file__).parent.parent.parent.parent / "scripts" / "douyin_cookies.txt"

        cmd = [
            "yt-dlp", "--no-warnings", "-f", "best",
            "--write-info-json",
            "-o", output_tpl,
        ]
        if cookie_file.exists() and cookie_file.stat().st_size > 50:
            cmd.extend(["--cookies", str(cookie_file)])
        cmd.append(source)

        code, out, err = run_cmd(cmd, timeout=120)

        # 找到下载的文件
        if code == 0:
            for ext in ["mp4", "webm", "mkv", "flv"]:
                files = sorted(output_dir.glob(f"*{url_hash}.{ext}"), key=os.path.getmtime, reverse=True)
                if files:
                    video_path = files[0]

                    # 读取 info json
                    title = ""
                    author = ""
                    for jf in output_dir.glob(f"*{url_hash}*.info.json"):
                        try:
                            info = json.loads(jf.read_text())
                            title = info.get("title", info.get("description", ""))
                            author = info.get("uploader", info.get("creator", ""))
                        except:
                            pass

                    log("✅", f"下载完成: {video_path.name}")
                    return {
                        "path": str(video_path),
                        "title": title or video_path.stem,
                        "author": author,
                        "source_url": source,
                    }

        # yt-dlp 失败，输出错误
        log("⚠️", f"yt-dlp 下载失败: {err.strip()[-200:]}")
        raise RuntimeError(
            f"视频下载失败。如果是抖音链接，可能需要 cookies 或代理。\n"
            f"你也可以直接把视频文件发给我，我来处理后续步骤。"
        )

    raise ValueError(f"无法识别的输入: {source}")


# ============================================================
# Step 2: 上传到 OSS
# ============================================================
def upload_to_oss(file_path, sub_prefix=""):
    """上传文件到 OSS，返回 {"oss_url": str, "oss_key": str}"""
    if not all([OSS_KEY_ID, OSS_KEY_SECRET, OSS_BUCKET, OSS_ENDPOINT]):
        log("⚠️", "OSS 未配置，跳过上传")
        return {"oss_url": "", "oss_key": "", "skipped": True}

    import oss2

    auth = oss2.Auth(OSS_KEY_ID, OSS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

    ext = Path(file_path).suffix
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = Path(file_path).stem[:30]
    oss_key = f"{OSS_PREFIX}{sub_prefix}{ts}_{name}{ext}"

    file_size = os.path.getsize(file_path)
    log("☁️", f"上传 OSS: {oss_key} ({file_size / 1024 / 1024:.1f}MB)")

    if file_size > 100 * 1024 * 1024:
        oss2.resumable_upload(bucket, oss_key, file_path, part_size=10 * 1024 * 1024, num_threads=4)
    else:
        with open(file_path, "rb") as f:
            bucket.put_object(oss_key, f)

    ep = OSS_ENDPOINT if OSS_ENDPOINT.startswith("http") else f"https://{OSS_ENDPOINT}"
    host = urlparse(ep).netloc
    oss_url = f"https://{OSS_BUCKET}.{host}/{oss_key}"

    log("✅", f"OSS 上传完成: {oss_url}")
    return {"oss_url": oss_url, "oss_key": oss_key, "skipped": False}


# ============================================================
# Step 3: 蚁小二发布
# ============================================================
def publish_yixiaoer(video_path, cover_path, target, platform="", title="", desc="", tags=None, draft=False):
    """通过蚁小二发布视频"""
    if not YXE_TOKEN:
        log("⚠️", "YIXIAOER_TOKEN 未配置，跳过发布")
        return {"skipped": True, "reason": "no_token"}

    if not YXE_SCRIPT.exists():
        log("⚠️", f"蚁小二脚本不存在: {YXE_SCRIPT}")
        return {"skipped": True, "reason": "script_missing"}

    cmd_name = "draft" if draft else "publish_full"
    tags_json = json.dumps(tags or [], ensure_ascii=False)

    cmd = [
        "python3", str(YXE_SCRIPT), cmd_name,
        str(video_path), str(cover_path),
        target, platform or "all",
        title, desc, tags_json,
    ]

    log("🐜", f"蚁小二{('草稿' if draft else '发布')}: 目标={target}, 平台={platform or 'all'}")
    code, out, err = run_cmd(cmd, timeout=120)

    if code == 0:
        try:
            result = json.loads(out)
            log("✅", f"蚁小二完成: {result.get('taskSetId', 'ok')}")
            return result
        except:
            return {"output": out.strip(), "ok": True}
    else:
        log("❌", f"蚁小二失败: {err.strip()[-200:]}")
        return {"error": err.strip()[-200:], "ok": False}


# ============================================================
# Step 4: 飞书多维表格记录
# ============================================================
def record_to_feishu(data):
    """
    通过 OpenClaw feishu_bitable_create_record 工具记录
    由于工具调用需要 Agent 层执行，这里输出指令让 Agent 代为执行
    """
    log("📋", "飞书记录数据已准备好（需要 Agent 调用 feishu_bitable_create_record）")
    return {
        "bitable_app_token": BITABLE_APP_TOKEN,
        "bitable_table_id": BITABLE_TABLE_ID,
        "fields": data,
        "pending": True,
    }


# ============================================================
# 主流程
# ============================================================
def run_pipeline(source, title="", desc="", tags=None, publish_target="",
                 platform="", draft=False, no_feishu=False, no_oss=False, cover_path=""):
    """完整流程"""
    result = {
        "status": "running",
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "steps": {},
    }

    try:
        # ── Step 1: 下载 ──
        log("🐝", "=== Step 1/5: 获取视频 ===")
        video_info = download_video(source)
        result["steps"]["download"] = {"ok": True, **video_info}
        result["video_path"] = video_info["path"]
        result["title"] = title or video_info.get("title", "")
        result["author"] = video_info.get("author", "")

        # ── Step 2: 视频信息 + 封面 ──
        log("🐝", "=== Step 2/5: 视频处理 ===")
        probe = ffprobe_info(video_info["path"])
        result["steps"]["probe"] = probe
        log("📊", f"视频: {probe.get('width')}x{probe.get('height')}, "
                   f"{probe.get('duration')}s, {probe.get('codec')}")

        # 截封面
        if not cover_path:
            cover_path = str(Path(video_info["path"]).with_suffix(".jpg"))
            # 在视频 1/3 处截取（通常更有代表性）
            ss = max(1, probe.get("duration", 6) // 3)
            extract_cover(video_info["path"], cover_path, f"00:00:{ss:02d}")
        if Path(cover_path).exists():
            log("🖼️", f"封面: {cover_path}")
        result["cover_path"] = cover_path

        # ── Step 3: OSS 上传 ──
        if not no_oss:
            log("🐝", "=== Step 3/5: OSS 上传 ===")
            oss_video = upload_to_oss(video_info["path"], "video/")
            result["steps"]["oss_video"] = oss_video
            result["oss_url"] = oss_video.get("oss_url", "")

            if Path(cover_path).exists():
                oss_cover = upload_to_oss(cover_path, "cover/")
                result["steps"]["oss_cover"] = oss_cover
                result["oss_cover_url"] = oss_cover.get("oss_url", "")
        else:
            log("⏭️", "跳过 OSS 上传")

        # ── Step 4: 蚁小二发布 ──
        if publish_target:
            log("🐝", "=== Step 4/5: 蚁小二发布 ===")
            yxe_result = publish_yixiaoer(
                video_info["path"], cover_path,
                publish_target, platform,
                result["title"], desc or result["title"],
                tags, draft
            )
            result["steps"]["yixiaoer"] = yxe_result
        else:
            log("⏭️", "未指定发布目标，跳过蚁小二")

        # ── Step 5: 飞书记录 ──
        if not no_feishu:
            log("🐝", "=== Step 5/5: 飞书记录 ===")
            feishu_fields = {
                "标题": result.get("title", ""),
                "作者": result.get("author", ""),
                "来源链接": result.get("steps", {}).get("download", {}).get("source_url", ""),
                "OSS地址": result.get("oss_url", ""),
                "封面OSS": result.get("oss_cover_url", ""),
                "时长(秒)": probe.get("duration", 0),
                "分辨率": f"{probe.get('width', '')}x{probe.get('height', '')}",
                "处理时间": datetime.now().isoformat(),
            }
            if publish_target:
                feishu_fields["发布目标"] = publish_target
                feishu_fields["发布状态"] = "已提交" if not draft else "草稿"

            result["steps"]["feishu"] = record_to_feishu(feishu_fields)
        else:
            log("⏭️", "跳过飞书记录")

        result["status"] = "success"
        log("🎉", "全流程完成!")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        log("❌", f"流程失败: {e}")

    # 输出结果 JSON
    print("\n" + "=" * 50)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="🐝 Bee 视频全流程自动化")
    sub = parser.add_subparsers(dest="command")

    # run
    p_run = sub.add_parser("run", help="执行完整流程")
    p_run.add_argument("source", help="视频链接或本地路径")
    p_run.add_argument("--title", default="", help="视频标题")
    p_run.add_argument("--desc", default="", help="视频描述")
    p_run.add_argument("--tags", default="[]", help='标签JSON: \'["tag1","tag2"]\'')
    p_run.add_argument("--publish", default="", help="蚁小二发布目标")
    p_run.add_argument("--platform", default="", help="指定平台")
    p_run.add_argument("--draft", action="store_true", help="存草稿")
    p_run.add_argument("--no-feishu", action="store_true", help="跳过飞书")
    p_run.add_argument("--no-oss", action="store_true", help="跳过OSS")
    p_run.add_argument("--cover", default="", help="自定义封面路径")

    # accounts
    sub.add_parser("accounts", help="查看蚁小二账号")

    # status
    p_status = sub.add_parser("status", help="查看发布状态")
    p_status.add_argument("task_id", help="任务ID")

    args = parser.parse_args()

    if args.command == "run":
        tags = json.loads(args.tags) if args.tags else []
        run_pipeline(
            source=args.source,
            title=args.title,
            desc=args.desc,
            tags=tags,
            publish_target=args.publish,
            platform=args.platform,
            draft=args.draft,
            no_feishu=args.no_feishu,
            no_oss=args.no_oss,
            cover_path=args.cover,
        )

    elif args.command == "accounts":
        if not YXE_TOKEN:
            print("❌ YIXIAOER_TOKEN 未配置")
            sys.exit(1)
        code, out, err = run_cmd(["python3", str(YXE_SCRIPT), "accounts"])
        print(out or err)

    elif args.command == "status":
        if not YXE_TOKEN:
            print("❌ YIXIAOER_TOKEN 未配置")
            sys.exit(1)
        code, out, err = run_cmd(["python3", str(YXE_SCRIPT), "status", args.task_id])
        print(out or err)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
