"""
A2F Quick Start Example

Simple example showing basic A2F workflow.
"""

import asyncio
import httpx
import sys
from pathlib import Path

# Add parent directory to path for importing api_key_manager
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.api_key_manager import get_headers


async def quick_a2f():
    """Quick A2F workflow"""

    API_BASE = "https://wuji.cyphy.com/api"

    # Step 1: Extract features
    print("Step 1: Extracting features...")

    headers = get_headers()
    async with httpx.AsyncClient() as client:
        with open("ref/李清照诗词中的自我形象研究_侯淑婉.pdf", "rb") as f:
            files = {"files[0]": ("character.pdf", f, "application/pdf")}
            data = {
                "role": "李清照",
                "loop_count": 2,
                "gen_method": "qwen",
                "openclaw": 1
            }

            response = await client.post(f"{API_BASE}/archiveData", data=data, files=files, headers=headers)
            features = response.json()

    print(f"✓ Features extracted")

    # Step 2: Generate images
    print("\nStep 2: Generating images...")

    prompt = "李清照, 女性, 成人, 写实风格, 真人风格"

    headers = get_headers()
    async with httpx.AsyncClient() as client:
        payload = {
            "text": prompt,
            "negative_text": "低质量, 模糊, 变形",
            "gen_method": 5,
            "gen_size": 1,
            "img_num": 4,
            "json": 1,
            "openclaw": 1
        }

        response = await client.post(f"{API_BASE}/a2fgen", json=payload, headers=headers)
        result = response.json()

    job_id = result.get("job_id")
    print(f"✓ Job started: {job_id}")

    # Step 3: Poll for completion
    print("\nStep 3: Waiting for completion...")

    while True:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/job_status/{job_id}")
            status = response.json()

            print(f"Status: {status['status']} ({status.get('progress', 0)}%)")

            if status['status'] == 'completed':
                results = status.get('results', [])
                print(f"\n✓ Complete! Generated {len(results)} images:")
                for i, url in enumerate(results, 1):
                    print(f"  {i}. {url}")
                break

            elif status['status'] == 'failed':
                print(f"❌ Job failed: {status.get('error')}")
                break

        await asyncio.sleep(5)


if __name__ == "__main__":
    print("A2F Quick Start Example\n")
    asyncio.run(quick_a2f())
