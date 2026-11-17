---
name: comment-wordcloud
version: 1.0.0
description: Generate word frequency statistics and word cloud from social media comments
whenToUse: When you need to analyze hot topics in social media comments
---

## Overview

This skill generates word frequency statistics and word cloud images from social media comment data.

## Usage

Provide comment data in JSON format. The script will automatically:

1. Read and parse comment data
2. Use jieba for Chinese word segmentation
3. Filter stop words
4. Calculate word frequency
5. Generate word cloud
6. Output word frequency JSON and word cloud PNG

## Input Format

Comment data should be in JSON format, each element contains a `content` field:

```json
[
  {"content": "This product is very useful"},
  {"content": "High cost performance, recommend purchase"}
]
```

## Output Format

- `{output_dir}/word_freq.json`: Word frequency statistics
- `{output_dir}/word_cloud.png`: Word cloud image

## Tech Stack

- Python 3.11+
- jieba 0.42.1
- wordcloud 1.9.3
- matplotlib 3.9.0

## Parameters

- `data_source`: Comment data file path (required)
- `output_dir`: Output directory (required)
- `stop_words`: Stop words file path (optional)
- `custom_words`: Custom vocabulary (optional, comma separated)
- `max_words`: Max words in word cloud (optional, default 200)

## Example

```bash
python scripts/generate_wordcloud.py references/sample_comments.json output/ --max-words 10
```

## Notes

1. Need to install Python dependencies: jieba, wordcloud, matplotlib
2. Need Chinese font file (use system font by default)
3. Stop words file is a text file with one word per line
4. Custom vocabulary will be added to tokenizer with priority
