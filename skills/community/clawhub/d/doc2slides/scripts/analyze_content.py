#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
Analyze PDF content with LLM and generate detailed slide structure.

Usage:
  python analyze_content.py --text <text_file> --output outline.json
  python analyze_content.py --content-json content.json --output outline.json
"""

import sys
import json
import argparse
import asyncio
from pathlib import Path

try:
    from llm_adapter import LLMAdapter
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("Error: llm_adapter not found")


ANALYZE_PROMPT = """你是一位专业的咨询公司（McKinsey/BCG）PPT设计师。请分析以下文档内容，生成详细的幻灯片结构。

## 输入文档
{content}

## 输出要求
生成 JSON 格式的幻灯片结构，包含 **12-18 个 slides**：

```json
{{
  "title": "文档标题",
  "subtitle": "副标题",
  "metadata": {{
    "author": "",
    "date": "",
    "keywords": ["关键词1", "关键词2"],
    "design_style": "简约科技风",
    "source_summary": "文档摘要（2-3句话）",
    "source_content": "完整文档内容（原文）"
  }},
  "slides": [
    {{
      "id": 1,
      "title": "页面标题",
      "type": "cover|content|dashboard|big_number|timeline|comparison",
      "key_points": ["要点1", "要点2", "要点3", "要点4"],
      "content_detail": "详细内容段落（100-200字）",
      "data_points": [
        {{"label": "指标名称", "value": "数字", "unit": "单位"}}
      ],
      "layout_suggestion": "cover|dashboard|big_number|content|comparison|timeline",
      "content_mode": "mixed|paragraph|bullet",
      "content_note": "内容来源说明"
    }}
  ]
}}
```

## 关键规则
1. **slide 数量**：生成 12-18 个 slides，覆盖文档所有重要内容
2. **每个 slide 必须有**：
   - 4-6 个 key_points（要点）
   - 100-200 字的 content_detail
   - **data_points 必须提取！**（这是最重要的规则）

3. **【硬性要求 - 不可违反】**
   - ⚠️ key_points 不得少于 4 个。少于 4 个的 slide 会被系统自动丢弃并重新生成
   - ⚠️ content_detail 不得少于 80 字。内容空洞的 slide 毫无价值
   - ⚠️ 如果文档某部分内容较少，也要从上下文中推断出合理的要点，不要留空
   - ⚠️ 目录页、过渡页、总结页也必须有实质性的 key_points，不能只写"目录"两个字

## 【最重要】数据提取规则
**每个 slide 必须提取 data_points！** 即使只有一个数字也要提取！

扫描文档中的所有数字，包括：
- 金额：3亿元、2500万、14亿 → {{"label": "融资金额", "value": "3", "unit": "亿元"}}
- 百分比：33%、60-70%、100% → {{"label": "增长率", "value": "33", "unit": "%"}}
- 数量：100家、40人、110个国家 → {{"label": "服务客户数", "value": "100", "unit": "家"}}
- 年份：2020年、2023年 → {{"label": "成立年份", "value": "2020", "unit": "年"}}
- 排名：排名第一 → {{"label": "行业排名", "value": "1", "unit": "名"}}

**示例转换**：
原文："已经服务近100家金融、消费、制造等行业的大型企业客户"
→ {{"label": "服务客户数", "value": "100", "unit": "家"}}

原文："年营收突破2500万"
→ {{"label": "年营收", "value": "2500", "unit": "万"}}

原文："前轮估值14亿人民币"
→ {{"label": "估值", "value": "14", "unit": "亿"}}

## 布局建议
- 有 3+ 个数字指标 → dashboard（仪表盘）
- 有 1-2 个核心大数字 → big_number
- 时间线内容 → timeline
- 对比内容 → comparison
- 一般内容 → content
- 封面 → cover

## JSON 输出规范（极其重要！）
1. **禁止**在 JSON 字符串值中使用双引号 `"`，请用单引号 `'` 或书名号 `《》` 代替
2. **禁止**在 source_content 字段中包含原始文档（太长），只写摘要
3. source_content 字段最多 500 字
4. 所有字符串值中不能出现未转义的双引号

## 直接输出 JSON，不要有其他文字
"""


async def analyze_with_llm(content: str, model: str = None, instruction: str = None) -> dict:
    """Use LLM to analyze content and generate slide structure."""
    if not HAS_LLM:
        print("Error: LLM adapter not available")
        return None

    adapter = LLMAdapter(model=model)

    # Build prompt with optional user instruction
    prompt = ANALYZE_PROMPT.format(content=content[:50000])  # Limit content length
    
    if instruction:
        prompt += f"""

---

## 【用户自定义指令 — 最高优先级】
以下用户指令**覆盖**上述所有默认规则，必须严格遵守：
{instruction}
"""

    print(f"Analyzing content ({len(content)} chars)...")

    try:
        response = await adapter.generate(
            prompt,
            temperature=0.3,
            max_tokens=16000,
            timeout=300.0  # 5 minutes timeout
        )
        
        # Extract JSON from response
        text = response.get('content', '') or response.get('reasoning_content', '')
        
        # Try to find JSON block
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            json_str = json_match.group()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"JSON preview: {json_str[:500]}...")
                
                # Try to fix common issues
                try:
                    fixed = json_str
                    # 1. Remove trailing commas
                    fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)
                    # 2. Replace Chinese quotes inside JSON strings
                    fixed = fixed.replace('\u201c', "'").replace('\u201d', "'")
                    # 3. Replace smart/curly double quotes
                    fixed = fixed.replace('\u2018', "'").replace('\u2019', "'")
                    # 4. Try to find the JSON object boundaries and truncate source_content if needed
                    #    LLM often puts full document text which contains unescaped quotes
                    result = json.loads(fixed)
                    return result
                except json.JSONDecodeError as e2:
                    print(f"JSON fix attempt failed: {e2}")
                    # Last resort: try to extract just the structure without source_content
                    try:
                        # Remove source_content field entirely (it's the biggest source of errors)
                        fixed2 = re.sub(r'"source_content"\s*:\s*".*?"', '"source_content": ""', json_str, flags=re.DOTALL)
                        fixed2 = re.sub(r',(\s*[}\]])', r'\1', fixed2)
                        return json.loads(fixed2)
                    except:
                        print("All JSON fix attempts failed")
                        return None
        
        print("No JSON found in response")
        return None
        
    except Exception as e:
        print(f"LLM error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Analyze content and generate slide structure')
    parser.add_argument('--text', help='Text file path')
    parser.add_argument('--content-json', help='Content JSON file (from read_content.py)')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file')
    parser.add_argument('--model', help='LLM model to use')
    parser.add_argument('--instruction', help='User instruction to guide analysis (e.g., "focus on financial data, use 10 slides max")')
    
    args = parser.parse_args()
    
    content = ""
    
    if args.content_json:
        with open(args.content_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            content = data.get('text', '') or data.get('summary', '')
    elif args.text:
        with open(args.text, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("Error: Must provide --text or --content-json")
        sys.exit(1)
    
    if not content:
        print("Error: No content to analyze")
        sys.exit(1)
    
    # Run LLM analysis
    result = asyncio.run(analyze_with_llm(content, args.model, getattr(args, 'instruction', None)))
    
    if not result:
        print("Failed to analyze content")
        sys.exit(1)
    
    # Save result
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(result.get('slides', []))} slides")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
