"""XAI (Grok) video provider."""

from common import api_post, poll_for_url


def generate(api_key, prompt, image_url):
    """Submit video to XAI, poll until ready, return video URL."""
    payload = {
        "model": "grok-imagine-video",
        "prompt": prompt,
        "duration": 15,
        "image": {"url": image_url},
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    code, body = api_post("https://api.x.ai/v1/videos/generations", headers, payload)
    video_id = body.get("request_id")
    if not video_id:
        print(f"XAI video submit failed: {body}")
        return None
    print(f"XAI video submitted ({code}): request_id={video_id}")
    return poll_for_url(
        f"https://api.x.ai/v1/videos/{video_id}",
        {"Authorization": f"Bearer {api_key}"},
    )
