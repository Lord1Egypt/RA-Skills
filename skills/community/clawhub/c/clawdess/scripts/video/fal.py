"""FAL video provider (Kling via FAL queue)."""

from common import api_post, poll_for_url


def generate(api_key, prompt, image_url):
    """Submit video to FAL, poll until ready, return video URL."""
    payload = {
        "prompt": prompt,
        "duration": 15,
        "image_url": image_url,
        "video_output_type": "mp4",
        "video_quality": "high",
    }
    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    code, body = api_post(
        "https://queue.fal.run/fal-ai/wan/v2.2-a14b/image-to-video/lora",
        headers, payload,
    )
    video_id = body.get("request_id")
    if not video_id:
        print(f"FAL video submit failed: {body}")
        return None
    print(f"FAL video submitted ({code}): request_id={video_id}")
    return poll_for_url(
        f"https://queue.fal.run/fal-ai/wan/requests/{video_id}",
        {"Authorization": f"Key {api_key}"},
    )
