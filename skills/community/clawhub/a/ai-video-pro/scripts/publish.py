"""
多平台发布脚本

支持发布到微博、小红书、抖音、云存储等平台。
支持草稿/正式版管理。
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from credential_manager import get_credential, get_cloud_credentials


def load_platform_config(platform_name: str) -> dict:
    """加载平台配置文件。"""
    config_dir = Path(__file__).parent.parent / "assets" / "platform_configs"
    config_file = config_dir / f"{platform_name}.json"

    if not config_file.exists():
        raise FileNotFoundError(f"平台配置文件不存在: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def transcode_video(input_path: str, platform_name: str,
                    output_dir: str = None) -> str:
    """
    将视频转码为目标平台的规格。

    Args:
        input_path: 输入视频路径
        platform_name: 平台名称
        output_dir: 输出目录（默认为输入文件同目录）

    Returns:
        转码后的视频文件路径
    """
    config = load_platform_config(platform_name)

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"输入视频不存在: {input_path}")

    if output_dir:
        output_path = Path(output_dir) / f"{input_path.stem}_{platform_name}.mp4"
    else:
        output_path = input_path.parent / f"{input_path.stem}_{platform_name}.mp4"

    # 构建 ffmpeg 命令
    video_config = config["video"]
    max_w = video_config["max_resolution"]["width"]
    max_h = video_config["max_resolution"]["height"]

    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-c:v", video_config["video_codec"],
        "-preset", video_config.get("preset", "medium"),
        "-crf", str(video_config.get("crf", 23)),
        "-c:a", video_config["audio_codec"],
        "-b:a", video_config.get("audio_bitrate", "128k"),
        "-movflags", "+faststart",
        "-vf", f"scale={max_w}:{max_h}:force_original_aspect_ratio=decrease,"
               f"pad={max_w}:{max_h}:-1:-1:black",
        "-r", str(video_config.get("fps", 30)),
        str(output_path),
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=300)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg 转码失败: {e.stderr.decode()[:500]}")
    except FileNotFoundError:
        raise RuntimeError("未找到 ffmpeg，请先安装: python scripts/install_deps.py --backend dalle_ffmpeg")

    # 检查文件大小限制
    output_size_mb = output_path.stat().st_size / (1024 * 1024)
    max_size_mb = video_config["max_file_size_mb"]
    if output_size_mb > max_size_mb:
        raise RuntimeError(
            f"转码后文件 ({output_size_mb:.1f}MB) 超过平台限制 ({max_size_mb}MB)，"
            f"请减少视频时长或降低画质"
        )

    return str(output_path)


def publish_to_weibo(video_path: str, title: str = "",
                     description: str = "") -> dict:
    """发布到微博。"""
    import urllib.request

    token = get_credential("weibo")
    config = load_platform_config("weibo")

    # 微博视频上传 API
    url = f"{config['api']['base_url']}{config['api']['upload_endpoint']}"

    # 构建 multipart 请求
    boundary = f"----WebKitFormBoundary{int(time.time())}"
    video_data = Path(video_path).read_bytes()
    video_name = Path(video_path).name

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="access_token"\r\n\r\n'
        f"{token}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="status"\r\n\r\n'
        f"{title} {description}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="video"; filename="{video_name}"\r\n'
        f"Content-Type: video/mp4\r\n\r\n"
    ).encode("utf-8") + video_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return {"success": True, "platform": "weibo", "response": data}
    except Exception as e:
        return {"success": False, "platform": "weibo", "error": str(e)}


def publish_to_douyin(video_path: str, title: str = "") -> dict:
    """发布到抖音。"""
    import urllib.request

    token = get_credential("douyin")
    config = load_platform_config("douyin")

    # Step 1: 上传视频
    upload_url = f"{config['api']['base_url']}{config['api']['upload_endpoint']}"

    video_data = Path(video_path).read_bytes()

    req = urllib.request.Request(
        upload_url,
        data=video_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "video/mp4",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            upload_result = json.loads(resp.read())

        video_id = upload_result.get("data", {}).get("video", {}).get("video_id")
        if not video_id:
            return {"success": False, "platform": "douyin", "error": "上传失败，未获取到 video_id"}

        # Step 2: 发布视频
        publish_url = f"{config['api']['base_url']}{config['api']['publish_endpoint']}"
        publish_payload = {
            "video_id": video_id,
            "text": title,
        }

        req = urllib.request.Request(
            publish_url,
            data=json.dumps(publish_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            publish_result = json.loads(resp.read())
            return {"success": True, "platform": "douyin", "response": publish_result}

    except Exception as e:
        return {"success": False, "platform": "douyin", "error": str(e)}


def publish_to_xiaohongshu(video_path: str, title: str = "") -> dict:
    """
    小红书发布（仅准备发布包）。

    注意: 小红书无官方 API，不进行自动上传。
    生成发布就绪的文件包，由用户手动上传。
    """
    output_dir = Path(video_path).parent / "xhs_publish_ready"
    output_dir.mkdir(exist_ok=True)

    # 转码为小红书规格
    try:
        transcoded = transcode_video(video_path, "xiaohongshu", str(output_dir))
    except Exception as e:
        return {"success": False, "platform": "xiaohongshu", "error": str(e)}

    # 生成发布说明
    readme = output_dir / "发布说明.txt"
    readme.write_text(
        f"小红书发布包\n"
        f"{'=' * 30}\n"
        f"标题: {title}\n"
        f"视频: {Path(transcoded).name}\n"
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"请手动上传到小红书:\n"
        f"1. 打开小红书 App\n"
        f"2. 点击底部 '+' 按钮\n"
        f"3. 选择此视频文件\n"
        f"4. 编辑标题和标签\n"
        f"5. 发布\n\n"
        f"注意: 小红书推荐 3:4 竖屏比例\n",
        encoding="utf-8",
    )

    return {
        "success": True,
        "platform": "xiaohongshu",
        "mode": "manual",
        "output_dir": str(output_dir),
        "message": f"发布包已准备好: {output_dir}\n请手动上传到小红书",
    }


def upload_to_cloud(video_path: str, cloud_provider: str) -> dict:
    """上传到云存储。"""
    credentials = get_cloud_credentials(cloud_provider)

    if cloud_provider == "aliyun_oss":
        return _upload_aliyun_oss(video_path, credentials)
    elif cloud_provider == "tencent_cos":
        return _upload_tencent_cos(video_path, credentials)
    elif cloud_provider == "aws_s3":
        return _upload_aws_s3(video_path, credentials)
    else:
        return {"success": False, "error": f"不支持的云存储: {cloud_provider}"}


def _upload_aliyun_oss(video_path: str, credentials: dict) -> dict:
    """上传到阿里云 OSS。"""
    try:
        import oss2

        auth = oss2.Auth(
            credentials["ALIYUN_ACCESS_KEY_ID"],
            credentials["ALIYUN_ACCESS_KEY_SECRET"],
        )
        bucket_name = credentials["ALIYUN_OSS_BUCKET"]
        endpoint = os.environ.get("ALIYUN_OSS_ENDPOINT", "oss-cn-hangzhou.aliyuncs.com")
        bucket = oss2.Bucket(auth, endpoint, bucket_name)

        key = f"ai-video-pro/{datetime.now().strftime('%Y%m%d')}/{Path(video_path).name}"
        bucket.put_object_from_file(key, video_path)

        url = f"https://{bucket_name}.{endpoint}/{key}"
        return {"success": True, "cloud": "aliyun_oss", "url": url}
    except ImportError:
        return {"success": False, "error": "需要安装 oss2: pip install oss2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _upload_tencent_cos(video_path: str, credentials: dict) -> dict:
    """上传到腾讯云 COS。"""
    try:
        from qcloud_cos import CosConfig, CosS3Client

        config = CosConfig(
            SecretId=credentials["TENCENT_SECRET_ID"],
            SecretKey=credentials["TENCENT_SECRET_KEY"],
            Region=os.environ.get("TENCENT_COS_REGION", "ap-guangzhou"),
        )
        client = CosS3Client(config)
        bucket = credentials["TENCENT_COS_BUCKET"]

        key = f"ai-video-pro/{datetime.now().strftime('%Y%m%d')}/{Path(video_path).name}"
        client.upload_file(Bucket=bucket, Key=key, LocalFilePath=video_path)

        region = os.environ.get("TENCENT_COS_REGION", "ap-guangzhou")
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{key}"
        return {"success": True, "cloud": "tencent_cos", "url": url}
    except ImportError:
        return {"success": False, "error": "需要安装 cos-python-sdk-v5: pip install cos-python-sdk-v5"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _upload_aws_s3(video_path: str, credentials: dict) -> dict:
    """上传到 AWS S3。"""
    try:
        import boto3

        s3 = boto3.client(
            "s3",
            aws_access_key_id=credentials["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=credentials["AWS_SECRET_ACCESS_KEY"],
        )
        bucket = credentials["AWS_S3_BUCKET"]

        key = f"ai-video-pro/{datetime.now().strftime('%Y%m%d')}/{Path(video_path).name}"
        s3.upload_file(video_path, bucket, key)

        region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        return {"success": True, "cloud": "aws_s3", "url": url}
    except ImportError:
        return {"success": False, "error": "需要安装 boto3: pip install boto3"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ===== 项目版本管理 =====

def get_projects_file() -> Path:
    """获取项目清单文件路径。"""
    projects_dir = Path.home() / ".ai-video-pro"
    projects_dir.mkdir(exist_ok=True)
    return projects_dir / "projects.json"


def load_projects() -> list:
    """加载项目清单。"""
    projects_file = get_projects_file()
    if projects_file.exists():
        with open(projects_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_project(video_path: str, status: str = "draft",
                 platform: str = None, metadata: dict = None) -> dict:
    """保存项目记录。"""
    projects = load_projects()

    project = {
        "id": len(projects) + 1,
        "video_path": str(Path(video_path).resolve()),
        "status": status,  # draft / published
        "platform": platform,
        "created_at": datetime.now().isoformat(),
        "metadata": metadata or {},
    }

    projects.append(project)

    with open(get_projects_file(), "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    return project


def list_projects() -> list:
    """列出所有项目。"""
    return load_projects()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Video Pro 多平台发布")
    parser.add_argument("--platform", required=True,
                        choices=["weibo", "xiaohongshu", "douyin", "cloud"],
                        help="目标平台")
    parser.add_argument("--mode", default="draft",
                        choices=["draft", "publish"],
                        help="发布模式 (draft=草稿, publish=发布)")
    parser.add_argument("--file", required=True, help="视频文件路径")
    parser.add_argument("--title", default="", help="视频标题")
    parser.add_argument("--cloud-provider", default="aliyun_oss",
                        choices=["aliyun_oss", "tencent_cos", "aws_s3"],
                        help="云存储 provider (仅 --platform cloud 时有效)")

    args = parser.parse_args()

    video_path = Path(args.file)
    if not video_path.exists():
        print(f"错误: 视频文件不存在: {video_path}")
        sys.exit(1)

    if args.mode == "draft":
        # 草稿模式：仅转码和保存项目记录
        print(f"准备草稿: {video_path.name} → {args.platform}")
        try:
            transcoded = transcode_video(str(video_path), args.platform)
            project = save_project(transcoded, status="draft", platform=args.platform)
            print(f"草稿已保存: {transcoded}")
            print(f"项目 ID: {project['id']}")
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)

    elif args.mode == "publish":
        # 发布模式
        print(f"发布到 {args.platform}: {video_path.name}")

        # 先转码
        try:
            transcoded = transcode_video(str(video_path), args.platform)
        except Exception as e:
            print(f"转码失败: {e}")
            sys.exit(1)

        # 发布
        if args.platform == "weibo":
            result = publish_to_weibo(transcoded, args.title)
        elif args.platform == "douyin":
            result = publish_to_douyin(transcoded, args.title)
        elif args.platform == "xiaohongshu":
            result = publish_to_xiaohongshu(transcoded, args.title)
        elif args.platform == "cloud":
            result = upload_to_cloud(transcoded, args.cloud_provider)
        else:
            result = {"success": False, "error": "不支持的平台"}

        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("success"):
            save_project(transcoded, status="published", platform=args.platform,
                         metadata=result)
