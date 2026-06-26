#!/usr/bin/env python3
"""
即梦AI视频生成封装 (Jimeng AI Video Generation 3.0)
支持文生视频 (text-to-video) 和图生视频 (image-to-video)

API: 火山引擎视觉智能 (visual.volcengineapi.com)
认证: IAM AK/SK (V4签名, 使用 volcenginesdkcore)
产品文档: https://www.volcengine.com/docs/85621

环境变量:
  VOLC_ACCESS_KEY_ID  - 火山引擎 Access Key ID (IAM)
  VOLC_SECRET_KEY     - 火山引擎 Secret Access Key (IAM)

价格 (2026.03):
  720P: 0.28 元/秒
  1080P: 0.63 元/秒

用法:
  # 文生视频
  python3 jimeng_video.py "一只猫在雪地里奔跑" -o cat.mp4

  # 图生视频
  python3 jimeng_video.py --image input.png "猫咪在雪地中" -o cat.mp4

  # Python API
  from jimeng_video import JimengVideo
  jv = JimengVideo()
  task_id = jv.submit("千军万马")
  video_url = jv.poll(task_id)
"""

import os, json, time, base64, argparse, sys
import requests

API_HOST = "visual.volcengineapi.com"
API_REGION = "cn-north-1"
SERVICE = "cv"
VERSION = "2022-08-31"

# req_key 映射
REQ_KEYS = {
    "t2v_720p": "jimeng_t2v_v30",         # 文生视频 720P
    "t2v_1080p": "jimeng_t2v_v30_1080p",   # 文生视频 1080P
    "i2v_720p": "jimeng_i2v_v30",         # 图生视频 720P
    "i2v_1080p": "jimeng_i2v_v30_1080p",  # 图生视频 1080P
}


def _sign(method, path, headers, body, query, ak, sk):
    """使用 volcenginesdkcore 的 V4 签名"""
    from volcenginesdkcore.signv4 import SignerV4
    SignerV4.sign(path, method, headers, body, None, query, ak, sk,
                  API_REGION, SERVICE)
    return headers


class JimengVideo:
    """即梦AI视频生成客户端"""

    def __init__(self, ak=None, sk=None):
        self.ak = ak or os.environ.get("VOLC_ACCESS_KEY_ID", "")
        self.sk = sk or os.environ.get("VOLC_SECRET_KEY", "")
        if not self.ak or not self.sk:
            raise ValueError(
                "环境变量 VOLC_ACCESS_KEY_ID 和 VOLC_SECRET_KEY 未设置\n"
                "请到 https://console.volcengine.com/iam/keymanage 创建密钥")

    def _request(self, action, body_dict):
        """发送签名请求"""
        body = json.dumps(body_dict)
        query = {"Action": action, "Version": VERSION}
        headers = {
            "Content-Type": "application/json",
            "Host": API_HOST,
        }
        _sign("POST", "/", headers, body, query, self.ak, self.sk)
        url = f"https://{API_HOST}/"
        resp = requests.post(url, params=query, headers=headers, data=body, timeout=30)
        return resp.json()

    def submit(self, prompt: str, mode: str = "t2v_720p",
               image_path: str = None, seed: int = -1,
               frames: int = 121, aspect_ratio: str = "16:9",
               callback_url: str = None) -> str:
        """
        提交视频生成任务

        Args:
            prompt: 提示词 (建议400字以内)
            mode: 模式 (t2v_720p/t2v_1080p/i2v_720p/i2v_1080p)
            image_path: 图生视频时的输入图片路径
            seed: 随机种子 (-1为随机)
            frames: 总帧数 (需满足 frames%24==1，有效值: 121/145/169/193/217/241)
            aspect_ratio: 宽高比 (16:9/4:3/1:1/3:4/9:16/21:9)
            callback_url: 回调URL (可选)

        Returns:
            task_id: 任务ID
        """
        req_key = REQ_KEYS.get(mode)
        if not req_key:
            raise ValueError(f"无效模式: {mode}, 可选: {list(REQ_KEYS.keys())}")

        body_dict = {
            "req_key": req_key,
            "prompt": prompt,
            "seed": seed,
            "frames": frames,
            "aspect_ratio": aspect_ratio,
        }

        if image_path and mode.startswith("i2v"):
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
            body_dict["image"] = img_data

        if callback_url:
            body_dict["callback_url"] = callback_url

        result = self._request("CVSync2AsyncSubmitTask", body_dict)

        if result.get("code") != 10000:
            raise RuntimeError(
                f"提交失败: {result.get('message', 'unknown')} "
                f"(code: {result.get('code')})")

        task_id = result["data"]["task_id"]
        return task_id

    def query(self, task_id: str, req_key: str = None) -> dict:
        """
        查询任务状态

        Returns:
            dict: 包含 status 和 video_url (完成时)
            status: in_queue / generating / done / not_found / expired
        """
        body_dict = {
            "req_key": req_key or REQ_KEYS["t2v_720p"],
            "task_id": task_id,
        }
        result = self._request("CVSync2AsyncGetResult", body_dict)

        if result.get("code") != 10000:
            raise RuntimeError(
                f"查询失败: {result.get('message', 'unknown')} "
                f"(code: {result.get('code')})")

        return result.get("data", {})

    def poll(self, task_id: str, req_key: str = None,
             interval: int = 10, timeout: int = 300, verbose: bool = True) -> str:
        """
        轮询等待任务完成

        Returns:
            video_url: 视频下载URL
        """
        start = time.time()
        while time.time() - start < timeout:
            data = self.query(task_id, req_key)
            status = data.get("status", "unknown")

            if verbose:
                elapsed = int(time.time() - start)
                print(f"    ⏳ 状态: {status} ({elapsed}s)", flush=True)

            if status == "done":
                video_url = data.get("video_url", "")
                if video_url:
                    if verbose:
                        print(f"    ✅ 生成完成!")
                    return video_url
                else:
                    raise RuntimeError("任务完成但未返回视频URL")
            elif status in ("not_found", "expired"):
                raise RuntimeError(f"任务异常: {status}")
            elif status in ("in_queue", "generating"):
                time.sleep(interval)
            else:
                time.sleep(interval)

        raise TimeoutError(f"视频生成超时 ({timeout}s)")

    def generate(self, prompt: str, output_path: str, mode: str = "t2v_720p",
                 image_path: str = None, seed: int = -1,
                 frames: int = 121, aspect_ratio: str = "16:9",
                 interval: int = 10, timeout: int = 300, verbose: bool = True) -> str:
        """
        一键生成: 提交 + 轮询 + 下载

        Returns:
            output_path: 本地视频文件路径
        """
        if verbose:
            mode_label = "图生视频" if image_path else "文生视频"
            print(f"  🎬 即梦AI {mode_label}...")

        task_id = self.submit(prompt, mode=mode, image_path=image_path,
                             seed=seed, frames=frames, aspect_ratio=aspect_ratio)
        if verbose:
            print(f"    任务ID: {task_id}")

        video_url = self.poll(task_id, REQ_KEYS.get(mode), interval, timeout, verbose)

        if verbose:
            print(f"    📥 下载视频...")
        resp = requests.get(video_url, timeout=120)
        resp.raise_for_status()

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)

        size_kb = os.path.getsize(output_path) // 1024
        if verbose:
            print(f"    ✅ 已保存: {output_path} ({size_kb}KB)")

        return output_path


def main():
    parser = argparse.ArgumentParser(description="即梦AI视频生成 (Jimeng AI 3.0)")
    parser.add_argument("prompt", help="视频提示词")
    parser.add_argument("-o", "--output", default="jimeng_output.mp4", help="输出路径")
    parser.add_argument("--mode", default="t2v_720p",
                       choices=["t2v_720p", "t2v_1080p", "i2v_720p", "i2v_1080p"])
    parser.add_argument("--image", help="图生视频的输入图片")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子")
    parser.add_argument("--frames", type=int, default=121,
                       help="帧数 (需满足 frames%%24==1: 121/145/169/193/217/241)")
    parser.add_argument("--aspect", default="16:9",
                       choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"])
    parser.add_argument("--interval", type=int, default=10, help="轮询间隔(秒)")
    parser.add_argument("--timeout", type=int, default=300, help="超时(秒)")
    args = parser.parse_args()

    jv = JimengVideo()
    jv.generate(args.prompt, args.output, mode=args.mode, image_path=args.image,
               seed=args.seed, frames=args.frames, aspect_ratio=args.aspect,
               interval=args.interval, timeout=args.timeout)


if __name__ == "__main__":
    main()
