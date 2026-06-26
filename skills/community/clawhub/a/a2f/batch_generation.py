"""
A2F Batch Generation Example

Generate multiple characters from multiple PDFs.
"""

import asyncio
import httpx
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# Add parent directory to path for importing api_key_manager
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.api_key_manager import get_headers

BASE_HEADERS = get_headers()


class BatchA2F:
    """Batch A2F generation"""

    def __init__(self, api_base: str = "https://wuji.cyphy.com/api"):
        self.api_base = api_base

    async def extract_features(self, pdf_path: str, role: str) -> Dict:
        """Extract features from PDF"""

        headers = get_headers(BASE_HEADERS)
        async with httpx.AsyncClient() as client:
            with open(pdf_path, "rb") as f:
                files = {"files[0]": (pdf_path, f, "application/pdf")}
                data = {"role": role, "loop_count": 2, "gen_method": "qwen", "openclaw": 1}

                response = await client.post(f"{self.api_base}/archiveData", data=data, files=files, headers=headers)
                return response.json()

    async def generate_images(self, prompt: str, img_num: int = 4) -> str:
        """Generate images and return job_id"""

        payload = {
            "text": prompt,
            "negative_text": "低质量, 模糊, 变形",
            "gen_method": 5,
            "img_num": img_num,
            "json": 1,
            "openclaw": 1
        }
        headers = get_headers(BASE_HEADERS)

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api_base}/a2fgen", json=payload, headers=headers)
            result = response.json()
            return result.get("job_id")

    async def check_status(self, job_id: str) -> Dict:
        """Check job status"""

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base}/job_status/{job_id}")
            return response.json()

    async def generate_batch(
        self,
        characters: List[Tuple[str, str]],
        style: str = "写实风格,真人风格"
    ) -> Dict[str, Dict]:
        """Generate multiple characters"""

        jobs = {}

        # Step 1: Extract features for all characters
        print("Step 1: Extracting features...")
        for pdf_path, role_name in characters:
            try:
                features = await self.extract_features(pdf_path, role_name)
                jobs[role_name] = {"features": features}
                print(f"  ✓ {role_name}: Features extracted")
            except Exception as e:
                print(f"  ❌ {role_name}: {e}")
                jobs[role_name] = {"error": str(e)}

        # Step 2: Generate images for all characters
        print("\nStep 2: Generating images...")
        for role_name, data in jobs.items():
            if "error" in data:
                continue

            try:
                prompt = f"{role_name}, {style}"
                job_id = await self.generate_images(prompt)
                jobs[role_name]["job_id"] = job_id
                print(f"  ✓ {role_name}: Job {job_id}")
            except Exception as e:
                print(f"  ❌ {role_name}: {e}")
                jobs[role_name]["error"] = str(e)

        # Step 3: Wait for all jobs to complete
        print("\nStep 3: Waiting for completion...")

        completed = 0
        total = len([j for j in jobs.values() if "job_id" in j])

        while completed < total:
            for role_name, data in jobs.items():
                if "job_id" not in data or "results" in data:
                    continue

                try:
                    status = await self.check_status(data["job_id"])

                    if status["status"] == "completed":
                        jobs[role_name]["results"] = status.get("results", [])
                        completed += 1
                        print(f"  ✓ {role_name}: Complete ({completed}/{total})")

                    elif status["status"] == "failed":
                        jobs[role_name]["error"] = status.get("error", "Unknown error")
                        completed += 1
                        print(f"  ❌ {role_name}: Failed ({completed}/{total})")

                except Exception as e:
                    print(f"  ⚠ {role_name}: {e}")

            if completed < total:
                await asyncio.sleep(5)

        return jobs


async def main():
    """Batch generation example"""

    batch = BatchA2F()

    # Define characters to generate
    characters = [
        ("ref/李清照诗词中的自我形象研究_侯淑婉.pdf", "李清照"),
        # Add more characters as needed
        # ("path/to/another.pdf", "Another Character"),
    ]

    print(f"Generating {len(characters)} characters\n")
    print("="*60)

    results = await batch.generate_batch(characters)

    print("\n" + "="*60)
    print("Batch Generation Complete!")
    print("="*60)

    for role_name, data in results.items():
        print(f"\n{role_name}:")
        if "results" in data:
            print(f"  Generated {len(data['results'])} images:")
            for i, url in enumerate(data['results'], 1):
                print(f"    {i}. {url}")
        elif "error" in data:
            print(f"  ❌ Error: {data['error']}")


if __name__ == "__main__":
    asyncio.run(main())
