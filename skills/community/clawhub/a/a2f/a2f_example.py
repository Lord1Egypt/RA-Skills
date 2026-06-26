"""
Archive2Figure (A2F) API - Complete Example

This script demonstrates the complete A2F workflow:
1. Upload PDF and extract character features
2. Generate images using extracted features
3. Poll for job completion and retrieve results

API Documentation: See ../ref/api1_doc.pdf
"""

import asyncio
import httpx
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent directory to path for importing api_key_manager
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.api_key_manager import get_headers


class A2FClient:
    """Client for Archive2Figure API"""

    def __init__(self, api_base: str = "https://wuji.cyphy.com/api"):
        self.api_base = api_base
        self.timeout = 60.0
        self.base_headers = get_headers()

    async def extract_features(
        self,
        pdf_path: str,
        role: str,
        loop_count: int = 2,
        gen_method: str = "qwen"
    ) -> Dict[str, Any]:
        """
        Step 1: Extract character features from PDF

        Args:
            pdf_path: Path to PDF file
            role: Character name (e.g., "李清照")
            loop_count: Number of extraction loops (1-5)
            gen_method: Generation method (default: "qwen")

        Returns:
            Dictionary with extracted features

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            httpx.HTTPError: If API request fails
        """

        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with open(pdf_path, "rb") as f:
                files = {
                    "files[0]": (pdf_file.name, f, "application/pdf")
                }
                data = {
                    "role": role,
                    "loop_count": loop_count,
                    "gen_method": gen_method,
                    "openclaw": 1
                }
                headers = get_headers(self.base_headers)

                response = await client.post(
                    f"{self.api_base}/archiveData",
                    data=data,
                    files=files,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()

        # Extract features from response
        if result and isinstance(result, dict):
            first_key = list(result.keys())[0]
            return {
                "role": role,
                "features": result[first_key],
                "raw_response": result
            }

        raise ValueError("Invalid response format from API")

    async def generate_images(
        self,
        text: str,
        negative_text: Optional[str] = None,
        gen_method: int = 5,
        gen_size: int = 1,
        img_num: int = 4,
        json_format: int = 1
    ) -> Dict[str, str]:
        """
        Step 2: Generate character images

        Args:
            text: Combined prompt text
            negative_text: Negative prompts (quality control)
            gen_method: Generation method (default: 5)
            gen_size: Generation size (default: 1)
            img_num: Number of images to generate (1-10)
            json_format: Response format (default: 1)

        Returns:
            Dictionary with job_id

        Raises:
            httpx.HTTPError: If API request fails
        """

        # Default negative prompt for quality control
        if negative_text is None:
            negative_text = (
                "文本, 特写, 裁剪, 出框, 最差质量, 低质量, "
                "jpeg 伪影, pgl y, 重复, 病态, 残缺, 额外的手指, "
                "变异的手, 画得不好的手, 画得不好的脸, 突变, 变形, "
                "模糊, 脱水, 不良的解剖结构, 不良的比例, 额外的肢体, "
                "克隆的脸, 毁容, 总体比例, 畸形的四肢, 缺失的手臂, "
                "缺失的腿, 额外的手臂, 多余的腿, 融合的手指, 太多的手指, "
                "长脖子, 水印, 印章"
            )

        payload = {
            "text": text,
            "negative_text": negative_text,
            "gen_method": gen_method,
            "gen_size": gen_size,
            "img_num": img_num,
            "json": json_format,
            "openclaw": 1
        }
        headers = get_headers(self.base_headers)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.api_base}/a2fgen",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()

        # Extract job_id
        job_id = result.get("job_id") or result.get("id")
        if not job_id:
            raise ValueError("No job_id returned from API")

        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Job created successfully"
        }

    async def check_job_status(
        self,
        job_id: str
    ) -> Dict[str, Any]:
        """
        Step 3: Check job status and get results

        Args:
            job_id: Job ID from generate_images

        Returns:
            Dictionary with job status and results (if complete)

        Raises:
            httpx.HTTPError: If API request fails
        """

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.api_base}/job_status/{job_id}"
            )
            response.raise_for_status()
            return response.json()

    async def wait_for_completion(
        self,
        job_id: str,
        max_wait: int = 300,
        poll_interval: int = 5
    ) -> List[str]:
        """
        Wait for job completion and return results

        Args:
            job_id: Job ID to wait for
            max_wait: Maximum wait time in seconds (default: 300)
            poll_interval: Polling interval in seconds (default: 5)

        Returns:
            List of result URLs

        Raises:
            TimeoutError: If job doesn't complete within max_wait
            Exception: If job fails
        """

        start_time = time.time()

        while time.time() - start_time < max_wait:
            result = await self.check_job_status(job_id)
            # API returns numeric status: 0 = completed, 1 = processing
            status = result.get("status")
            progress = result.get("progress", 0)

            print(f"Job {job_id}: status={status} ({progress}%)")

            # status: 0 means completed
            if status == 0:
                results = result.get("results", []) or result.get("output", [])
                if results:
                    if isinstance(results, str):
                        results = [results]
                    print(f"\nJob completed! Generated {len(results)} images")
                    return results
                else:
                    raise Exception("Job completed but no results returned")

            # status: 1 means processing, continue waiting
            elif status == 1:
                pass  # Continue waiting

            # Other status values might indicate failure
            elif status is not None and status != 1:
                error = result.get("error", result.get("msg", "Unknown error"))
                raise Exception(f"Job failed: {error}")

            await asyncio.sleep(poll_interval)

        raise TimeoutError(f"Job did not complete within {max_wait} seconds")

    async def complete_workflow(
        self,
        pdf_path: str,
        role: str,
        style_prompt: str = "写实风格,真人风格",
        img_num: int = 4
    ) -> Dict[str, Any]:
        """
        Complete A2F workflow: Extract → Generate → Retrieve

        Args:
            pdf_path: Path to PDF file
            role: Character name
            style_prompt: Additional style prompts
            img_num: Number of images to generate

        Returns:
            Dictionary with features, job_id, and result URLs
        """

        print(f"\n{'='*60}")
        print(f"A2F Workflow: {role}")
        print(f"{'='*60}\n")

        # Step 1: Extract features
        print("Step 1: Extracting features from PDF...")
        extraction = await self.extract_features(pdf_path, role)
        features = extraction["features"]

        print(f"✓ Features extracted:")
        print(f"  - Role: {features.get('role', ['N/A'])[0]}")
        print(f"  - Gender: {features.get('gender', ['N/A'])[0]}")
        print(f"  - Age: {features.get('age', ['N/A'])[0]}")

        # Step 2: Build prompt
        print("\nStep 2: Building prompt...")
        prompt = self._build_prompt(features, style_prompt)
        print(f"✓ Prompt: {prompt[:100]}...")

        # Step 3: Generate images
        print("\nStep 3: Generating images...")
        generation = await self.generate_images(
            text=prompt,
            img_num=img_num
        )
        job_id = generation["job_id"]
        print(f"✓ Job started: {job_id}")

        # Step 4: Wait for completion
        print("\nStep 4: Waiting for completion...")
        results = await self.wait_for_completion(job_id)

        return {
            "role": role,
            "features": features,
            "job_id": job_id,
            "results": results
        }

    def _build_prompt(
        self,
        features: Dict[str, List[str]],
        style_prompt: str
    ) -> str:
        """Build effective prompt from features

        According to PDF: Only include gender and text features.
        Do NOT include: Role, language, voice, cusstyle
        """

        gender = features.get("gender", [""])[0] or ""

        # Base prompt with only gender
        prompt_parts = [gender] if gender else []

        # Add text features (visual descriptors)
        prompt_parts.extend(["肖像画", "正脸", "全身照", "站立", "看着观众"])

        # Add detailed visual features only
        visual_keys = ["ffeatures", "clothing", "hairstyle", "accessories", "headdress", "build", "footwear"]
        for key in visual_keys:
            if key in features and features[key]:
                prompt_parts.extend(features[key])

        # Add style prompt
        prompt_parts.append(style_prompt)

        # Filter empty strings and join
        return ", ".join(filter(None, prompt_parts))


async def main():
    """Example usage"""

    client = A2FClient()

    # Example 1: Complete workflow
    try:
        result = await client.complete_workflow(
            pdf_path="ref/李清照诗词中的自我形象研究_侯淑婉.pdf",
            role="李清照",
            style_prompt="写实风格,真人风格",
            img_num=4
        )

        print("\n" + "="*60)
        print("Workflow Complete!")
        print("="*60)
        print(f"\nGenerated images for {result['role']}:")
        for i, url in enumerate(result['results'], 1):
            print(f"  {i}. {url}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    # Example 2: Step-by-step workflow
    print("\n" + "="*60)
    print("Example 2: Step-by-Step Workflow")
    print("="*60)

    try:
        # Step 1: Extract features
        extraction = await client.extract_features(
            pdf_path="ref/李清照诗词中的自我形象研究_侯淑婉.pdf",
            role="李清照"
        )
        print(f"\n✓ Features extracted: {extraction['role']}")

        # Step 2: Generate images
        prompt = "李清照, 女性, 成人, 写实风格, 真人风格"
        generation = await client.generate_images(
            text=prompt,
            img_num=2
        )
        print(f"✓ Generation started: {generation['job_id']}")

        # Step 3: Wait for results
        results = await client.wait_for_completion(generation['job_id'])
        print(f"\n✓ Results: {len(results)} images generated")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    # Example 3: Custom prompt generation
    print("\n" + "="*60)
    print("Example 3: Custom Prompt")
    print("="*60)

    custom_prompt = (
        "李清照, 女性, 成人, "
        "肖像画, 正脸, 全身照, "
        "皮肤白皙, 面容清秀, 表情细腻, "
        "古代服饰, 轻薄衣衫, 色彩淡雅, "
        "金钗, 玉饰, "
        "写诗, 宋代江南水乡, "
        "婉约, 细腻, "
        "写实风格, 真人风格"
    )

    print(f"\nCustom prompt:\n{custom_prompt}\n")

    try:
        generation = await client.generate_images(
            text=custom_prompt,
            img_num=1
        )
        print(f"✓ Job ID: {generation['job_id']}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    # Run examples
    asyncio.run(main())
