# A2F Examples

This directory contains example scripts for using the Archive2Figure (A2F) API.

## Files

- **a2f_example.py** - Complete example with A2FClient class
- **quick_start.py** - Simple quick start example
- **batch_generation.py** - Batch character generation example

## Quick Start

### Basic Usage

```python
from a2f_example import A2FClient
import asyncio

async def main():
    client = A2FClient()

    result = await client.complete_workflow(
        pdf_path="path/to/character.pdf",
        role="Character Name",
        style_prompt="写实风格,真人风格",
        img_num=4
    )

    print(f"Generated {len(result['results'])} images")
    for url in result['results']:
        print(url)

asyncio.run(main())
```

## Examples

### 1. Complete Workflow

```python
# One complete function: extract → generate → retrieve
result = await client.complete_workflow(
    pdf_path="character.pdf",
    role="李清照"
)
```

### 2. Step-by-Step

```python
# Step 1: Extract features
extraction = await client.extract_features("character.pdf", "李清照")

# Step 2: Generate images
generation = await client.generate_images(
    text="李清照, 女性, 写实风格"
)

# Step 3: Wait for results
results = await client.wait_for_completion(generation['job_id'])
```

### 3. Custom Prompt

```python
# Build your own prompt
prompt = "角色名, 性别, 年龄, 服装, 配饰, 风格"
generation = await client.generate_images(text=prompt, img_num=4)
```

## Requirements

```bash
pip install httpx asyncio
```

## Running Examples

```bash
# Run complete example
python a2f_example.py

# Run quick start
python quick_start.py

# Run batch generation
python batch_generation.py
```

## Notes

- Ensure you have valid PDF files with character descriptions
- Jobs typically take 1-5 minutes to complete
- Maximum 10 images per generation
- Use negative prompts to control quality
