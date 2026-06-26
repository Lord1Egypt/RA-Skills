#!/usr/bin/env python3

import subprocess
import json
import time

# --- Config (from Skill's references/config.md) ---
TARGET_SHEET_ID = "1Nnwv4DbbUgfiNDiJdgCvnyxH6oPBis_99fm-2voehl4"
TARGET_SHEET_NAME = "Sheet1"
SOURCE_SHEET_ID = "1ryQvtIcUD0nwfd4l6nIonipkgsQF4AqeBo7jRnfsyTQ"
SOURCE_SHEET_NAME = "Sheet1"

BATCH_SIZE = 20  # Process 20 words per Gemini call


def format_and_write_excel() -> dict:
    try:
        # 1. Read data from Source Google Sheet (fr and en columns)
        cmd_get = ["gog", "sheets", "get", SOURCE_SHEET_ID, "Sheet1!A2:B1000", "--json"]
        res = subprocess.run(cmd_get, capture_output=True, text=True, check=True)
        source_data = json.loads(res.stdout).get("values", [])

        if not source_data:
            return {"success": False, "error": "Source Google Sheet is empty or has no data."}

        new_data = []
        print(f"Processing {len(source_data)} words in batches of {BATCH_SIZE}...")

        processed_count = 0
        for i in range(0, len(source_data), BATCH_SIZE):
            batch = source_data[i:i + BATCH_SIZE]
            batch_prompts = []

            for j, row in enumerate(batch):
                if not row or len(row) < 1:
                    continue
                fr_word = str(row[0]).strip()
                en_trans = str(row[1]).strip() if len(row) > 1 else ""
                batch_prompts.append({
                    "id": i + j + 1,
                    "fr_word": fr_word,
                    "en_translation": en_trans,
                })

            if not batch_prompts:
                continue

            main_prompt = (
                "You are a helpful language translation assistant. "
                "I will provide a JSON array of French vocabulary words. "
                "For each word, return a JSON object with EXACTLY these keys:\n"
                '- "id": (number) the original id\n'
                '- "fr_word": (string) the French word\n'
                '- "en_translation": (string) the English translation\n'
                '- "chinese_translation": (string) professional Chinese translation of the term\n'
                '- "example_fr": (string) a natural French example sentence using the word\n'
                '- "example_cn": (string) Chinese translation of the example sentence\n\n'
                f"Input Data: {json.dumps(batch_prompts, ensure_ascii=False)}\n\n"
                "Return ONLY a valid JSON array. Do not include markdown formatting or explanations."
            )

            try:
                # Use gemini -p for non-interactive headless mode
                res_gemini = subprocess.run(
                    ["gemini", "-p", main_prompt],
                    capture_output=True, text=True, check=True
                )
                output = res_gemini.stdout.strip()

                # Strip markdown code fences if present
                if output.startswith("```json"):
                    output = output[7:]
                elif output.startswith("```"):
                    output = output[3:]
                if output.endswith("```"):
                    output = output[:-3]

                batch_results = json.loads(output.strip())

                if not isinstance(batch_results, list):
                    raise ValueError("Gemini did not return a JSON array.")

                for result in batch_results:
                    new_data.append([
                        result.get("id", ""),
                        result.get("fr_word", ""),
                        result.get("en_translation", ""),
                        result.get("chinese_translation", ""),
                        result.get("example_fr", ""),
                        result.get("example_cn", ""),
                    ])
                    processed_count += 1

                print(f"Batch {i // BATCH_SIZE + 1}: {len(batch_results)} words done.")

            except Exception as e:
                stderr = res_gemini.stderr if 'res_gemini' in dir() else 'N/A'
                print(f"Error in batch {i // BATCH_SIZE + 1}: {e}\nGemini stderr: {stderr}")

                # Fallback: preserve source data, mark translation as failed
                for j, row in enumerate(batch):
                    fr_word = str(row[0]).strip()
                    en_trans = str(row[1]).strip() if len(row) > 1 else ""
                    new_data.append([i + j + 1, fr_word, en_trans, "Generation Failed", "", ""])
                    processed_count += 1

            time.sleep(2)

        # 2. Clear target sheet
        print("Clearing target sheet...")
        subprocess.run(
            ["gog", "sheets", "clear", TARGET_SHEET_ID, f"{TARGET_SHEET_NAME}!A1:F1000"],
            capture_output=True, text=True, check=True
        )

        # 3. Write results with header — pass JSON directly, no shell=True
        output_data = [
            ["Index", "Fr Original", "En Translation", "Chinese Translation",
             "Example Sentence (FR)", "Example Sentence (CN)"]
        ] + new_data

        print(f"Writing {len(output_data)} rows to target sheet...")
        subprocess.run(
            [
                "gog", "sheets", "update",
                TARGET_SHEET_ID, f"{TARGET_SHEET_NAME}!A1",
                "--values-json", json.dumps(output_data, ensure_ascii=False),
                "--input=USER_ENTERED", "--json",
            ],
            capture_output=True, text=True, check=True
        )

        return {"success": True, "message": f"Processed {processed_count} words and updated target sheet."}

    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"Command failed: {e.cmd}\nStderr: {e.stderr}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = format_and_write_excel()
    print(json.dumps(result, indent=2, ensure_ascii=False))
