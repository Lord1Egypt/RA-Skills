---
name: draw-animal
version: 0.1.0
description: Generate a text description of an animal picture via Python script
activation:
  patterns:
    - "draw an animal"
    - "generate animal picture description"
    - "show me a [animal] picture"
  keywords:
    - "draw"
    - "animal"
    - "picture"
    - "description"
  exclude_keywords:
    - "delete"
    - "remove"
    - "rm"
  tags:
    - "test"
    - "animal"
    - "text-generation"
  max_context_tokens: 1000
metadata:
  openclaw:
    requires:
      bins: [python3]  # 依赖python3可执行文件
      env: []  # 无环境变量依赖，留空即可
---

# Draw Animal Skill Instructions
## Overview
This skill generates a simple text description for an animal picture. If no specific animal type is specified, "pig" will be used as the default.

## Execution Logic
1. Prompt the user to specify the animal they want to generate a picture description for, and provide a few common options (e.g., cat, dog, bird) as recommendations.
2. Extract the "animal" parameter from the user's input, then run the Python script with this parameter (using "pig" if no parameter is provided). Optionally, extract the "lang" parameter (default: en) to support English/Chinese descriptions:
   ```bash
   python3 {baseDir}/scripts/draw_animal.py --animal {animal:-pig} --lang {lang:-en}
