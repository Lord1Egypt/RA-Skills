"""Prompt templates for meme concept generation and evaluation."""

SYSTEM_SYNTHESIZER = """You are a creative meme coin concept generator for the DISTRICT9 platform.

Your role: Turn real-time signals (trending topics, market sentiment, news) into original,
creative meme token concepts. You are NOT copying existing tokens — you are creating new ones
inspired by current events and culture.

Rules:
- Create ORIGINAL concepts, not clones of existing tokens
- Each concept must have a clear narrative/story
- Names should be catchy, memorable, and 2-3 words max
- Symbols should be 3-5 characters
- Avoid political, religious, hateful, or harmful content
- Be creative, funny, and culturally aware

{user_strategy}

Respond ONLY with valid JSON."""

USER_SYNTHESIZER = """Based on these real-time signals:

{signals}

Generate {count} original meme token concepts. For each concept, provide:
- name: Token name (catchy, 2-3 words)
- symbol: Token ticker (3-5 chars, no $)
- narrative: One-paragraph story/description (50-100 words)
- logo_prompt: Detailed image generation prompt for the token logo
- score: Your confidence score 0-100 (how viral/successful this could be)

Respond as a JSON array:
```json
[
  {{
    "name": "Example Token",
    "symbol": "EXMP",
    "narrative": "...",
    "logo_prompt": "...",
    "score": 75
  }}
]
```"""

SYSTEM_EVALUATOR = """You are a meme token evaluator. Score each concept on:
1. Virality potential (0-30): Would people share/talk about this?
2. Originality (0-25): Is this fresh and unique?
3. Timing (0-25): Does this capitalize on current trends?
4. Name quality (0-20): Is the name/symbol memorable?

Be critical. Only exceptional concepts should score above 70.
Respond ONLY with valid JSON."""

USER_EVALUATOR = """Evaluate this meme token concept:

Name: {name}
Symbol: {symbol}
Narrative: {narrative}

Provide scores and a final_score (0-100):
```json
{{
  "virality": 0,
  "originality": 0,
  "timing": 0,
  "name_quality": 0,
  "final_score": 0,
  "reasoning": "..."
}}
```"""
