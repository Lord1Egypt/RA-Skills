#!/usr/bin/env python3
"""
Generator: Uses LLM to create skill variants.

Strategy:
- Take parent skill code + performance feedback
- Prompt LLM to generate improved variants
- Diversify via temperature and mutation strategies
"""

import json
import os
import random
import sys
from pathlib import Path
from typing import Dict, List, Optional

import openai

# Base configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Try to load OpenRouter configuration from openclaw.json
try:
    with open('/home/gem/workspace/agent/openclaw.json') as f:
        CONFIG = json.load(f)
    OR_CONFIG = CONFIG.get('models', {}).get('providers', {}).get('openrouter', {})
    # Prefer free models if available
    free_models = [m['id'] for m in OR_CONFIG.get('models', []) if m['id'].endswith(':free')]
    DEFAULT_MODEL = free_models[0] if free_models else 'stepfun/step-3.5-flash:free'
    print(f"[Generator] Loaded model from config: {DEFAULT_MODEL}")
except Exception as e:
    print(f"[Generator] Could not load openclaw.json: {e}, using hardcoded free model")
    DEFAULT_MODEL = 'stepfun/step-3.5-flash:free'


class Generator:
    """LLM-powered variant generator with multi-key fallback and rotation."""

    def __init__(self, model: str = None):
        self.model = model or DEFAULT_MODEL
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.client = None

        # Try to initialize with a key
        if self.api_keys:
            self._set_client(self.api_keys[0])
        elif OPENROUTER_API_KEY:
            self._set_client(OPENROUTER_API_KEY)
            self.api_keys = [OPENROUTER_API_KEY]
        else:
            print("[Generator] ⚠️ No OpenRouter API keys found. Will use local mutation fallback.")

    def _load_api_keys(self) -> List[str]:
        """Load all available OpenRouter API keys from configured locations."""
        keys = []

        # 1. Read from key rotation file (single current key)
        key_file = Path("/home/gem/workspace/agent/.secrets/openrouter-key")
        if key_file.exists():
            key = key_file.read_text().strip()
            if key:
                keys.append(key)

        # 2. Read from multi-key directory (key1, key2, ...)
        keys_dir = Path("/home/gem/workspace/agent/.secrets/openrouter-keys")
        if keys_dir.exists():
            for key_file in sorted(keys_dir.glob("key*")):
                key = key_file.read_text().strip()
                if key and key not in keys:  # avoid duplicates
                    keys.append(key)

        # 3. Read from rotation script state (if available)
        state_file = Path("/home/gem/workspace/agent/.secrets/.openrouter-key-rotation-state")
        if state_file.exists():
            try:
                index = int(state_file.read_text().strip())
                # rotate-openrouter-key.sh has KEYS array; we can't read that from here
                # but we have already collected keys from keys_dir
                if 0 <= index < len(keys):
                    # Move the current key to front for priority
                    keys.insert(0, keys.pop(index))
            except Exception as e:
                print(f"[Generator] Failed to read rotation state: {e}")

        return keys

    def _set_client(self, api_key: str):
        """Initialize OpenAI client with given key."""
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    def _rotate_key(self) -> Optional[str]:
        """Cycle to next available API key."""
        if not self.api_keys:
            return None
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        key = self.api_keys[self.current_key_index]
        self._set_client(key)
        return key

    def _call_llm(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
        """Call LLM with key rotation and retry logic."""
        max_attempts = len(self.api_keys) if self.api_keys else 1
        for attempt in range(max_attempts):
            try:
                if attempt > 0:
                    print(f"[Generator] Retry {attempt+1}/{max_attempts} with key index {self.current_key_index}")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
            except openai.RateLimitError as e:
                print(f"[Generator] Rate limit on key {self.current_key_index}: {e}")
                self._rotate_key()
            except openai.AuthenticationError as e:
                print(f"[Generator] Auth error on key {self.current_key_index}: {e}")
                self._rotate_key()
            except Exception as e:
                print(f"[Generator] API error on key {self.current_key_index}: {e}")
                self._rotate_key()
        return None

    def _read_skill_code(self, skill_path: Path) -> Dict:
        """Read skill files into a structured representation."""
        code = {}
        for file in skill_path.rglob("*"):
            if file.is_file() and file.suffix in [".py", ".ts", ".js", ".md"]:
                relative = file.relative_to(skill_path)
                code[str(relative)] = file.read_text()
        return code

    def _create_prompt(self, parent: Dict, elites: List[Dict], fitness_stats: Dict) -> str:
        """Construct generation prompt."""
        parent_code = "\n".join([f"## {k}\n{v}" for k, v in parent["code"].items()])

        elite_examples = ""
        for i, elite in enumerate(elites[:3]):  # Show top 3
            elite_examples += f"\n--- Elite {i+1} (fitness={elite['fitness']:.2f}) ---\n"
            elite_examples += "\n".join([f"## {k}\n{v[:500]}..." for k, v in elite["code"].items()])

        prompt = f"""You are an AI skill evolution engineer. Generate an improved variant of the following skill.

## Parent Skill
{parent_code}

## Top Elite Variants (for reference)
{elite_examples}

## Performance Context
- Population avg fitness: {fitness_stats['avg']:.3f}
- Best fitness: {fitness_stats['best']:.3f}
- Generation: {fitness_stats['generation']}

## Mutation Strategies (choose one or combine):
- **Parameter Tuning**: Adjust thresholds, rates, weights
- **Logic Refinement**: Improve algorithms, error handling
- **Prompt Engineering**: Better LLM prompts (if applicable)
- **Structure Optimization**: Reorganize code, add caching, parallelization
- **New Feature Addition**: Introduce beneficial new capabilities

## Output Format (strict JSON):
{{
  "variant_name": "skill-variant-<unique>",
  "changes": ["Brief description of changes"],
  "code": {{"relative/path/to/file": "full file content", ...}},
  "reasoning": "Why this variant should perform better"
}}

Generate ONE high-quality variant now. Focus on **practical improvements** that increase:
- Accuracy / Correctness
- Speed / Efficiency  
- Robustness (error handling, edge cases)
- Maintainability (clean code, comments)

Respond ONLY with valid JSON, no additional text."""

        return prompt

    def generate_variant(self, parent_skill_path: Path, strategy: str = "auto") -> Dict:
        """Generate a single variant using LLM with fallback."""
        parent = {
            "id": "parent",
            "code": self._read_skill_code(parent_skill_path),
            "fitness": 0.0
        }

        if self.client is None:
            return self._simple_mutation(parent_skill_path, parent)

        prompt = self._create_prompt(parent, [], {"avg": 0.0, "best": 0.0, "generation": 0})
        content = self._call_llm(prompt, temperature=0.8, max_tokens=2000)

        if content:
            try:
                variant = json.loads(content)
                variant["generation"] = 1
                variant["fitness"] = 0.0
                return variant
            except json.JSONDecodeError as e:
                print(f"[Generator] JSON parse error: {e}, falling back to local mutation")
        
        return self._simple_mutation(parent_skill_path, parent)

    def _simple_mutation(self, parent_skill_path: Path, parent: Dict) -> Dict:
        """Simple local mutation when LLM is unavailable."""
        code = parent["code"].copy()
        # Apply simple random mutations to a random file
        if code:
            file_key = random.choice(list(code.keys()))
            content = code[file_key]
            mutations = [
                lambda s: s.replace("True", "False") if "True" in s else s,
                lambda s: s.replace("False", "True") if "False" in s else s,
                lambda s: s.replace("0.5", "0.6") if "0.5" in s else s,
                lambda s: s + "\n# mutated" if s.endswith("\n") else s + "\n# mutated",
            ]
            mutation = random.choice(mutations)
            code[file_key] = mutation(content)
        
        return {
            "variant_name": f"{parent_skill_path.name}-simple-mut-{random.randint(100,999)}",
            "changes": ["Simple local mutation (no LLM)"],
            "code": code,
            "generation": 1,
            "fitness": 0.0
        }

    def generate_next_generation(
        self,
        elites: List[Dict],
        population_size: int,
        mutation_rate: float = 0.1
    ) -> List[Dict]:
        """Generate full next generation from elite parents."""
        new_population = []

        # Keep elites unchanged (elitism)
        for elite in elites:
            elite_copy = elite.copy()
            elite_copy["generation"] = elite["generation"] + 1
            new_population.append(elite_copy)

        # Generate offspring until we fill population
        while len(new_population) < population_size:
            # Select random elite as parent
            parent = random.choice(elites)
            # Small chance to mutate even elite offspring
            if random.random() < mutation_rate:
                # Generate mutated variant
                variant = self.generate_variant_from_parent(parent)
            else:
                # Crossover: combine two parents
                parent2 = random.choice(elites)
                variant = self.crossover(parent, parent2)

            variant["generation"] = parent["generation"] + 1
            new_population.append(variant)

        return new_population[:population_size]

    def generate_variant_from_parent(self, parent: Dict) -> Dict:
        """Generate a mutated variant from a single parent dict using LLM with fallback."""
        prompt = f"""Given this skill code (file structure):

Parent files: {list(parent['code'].keys())}

Apply ONE focused improvement. Output JSON with:

{{
  "variant_name": "skill-variant-<unique>",
  "changes": ["<change description>"],
  "code": {{"relative/path/to/file": "full updated content", ...}},
  "reasoning": "<why>"
}}

Improve in one of:
- Parameter tuning
- Error handling
- Speed optimization
- Structure cleanup
- Documentation

Respond ONLY with valid JSON."""
        
        if self.client is not None:
            content = self._call_llm(prompt, temperature=0.8, max_tokens=1500)
            if content:
                try:
                    variant = json.loads(content)
                    variant["generation"] = parent.get("generation", 0) + 1
                    variant["fitness"] = 0.0
                    return variant
                except json.JSONDecodeError as e:
                    print(f"[Generator] JSON parse error in variant_from_parent: {e}")

        # Fallback: shallow copy with simple mutation
        code = parent["code"].copy()
        if code:
            file_key = random.choice(list(code.keys()))
            code[file_key] = code[file_key] + "\n# mutated by fallback"
        
        return {
            "variant_name": f"{parent.get('variant_name','skill')}-mutant-{random.randint(100,999)}",
            "changes": ["Fallback mutation (simple append)"],
            "code": code,
            "generation": parent.get("generation", 0) + 1,
            "fitness": 0.0,
            "reasoning": "Fallback due to LLM error"
        }

    def crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """Create child by combining code from two parents (no LLM needed)."""
        child_code = parent1["code"].copy()
        taken_from_parent2 = []
        
        # Randomly replace some files with parent2's version
        for key in parent2["code"]:
            if random.random() < 0.3:
                child_code[key] = parent2["code"][key]
                taken_from_parent2.append(key)

        return {
            "variant_name": f"cross-{parent1.get('variant_name','p1')[:10]}-{parent2.get('variant_name','p2')[:10]}",
            "changes": [
                f"Crossover: kept {len(child_code)} total files",
                f"Replaced {len(taken_from_parent2)} files from parent2"
            ],
            "code": child_code,
            "generation": max(parent1.get("generation",0), parent2.get("generation",0)) + 1,
            "fitness": 0.0,
            "reasoning": "Combined code from two elite parents via file-level mixing"
        }


if __name__ == "__main__":
    # Quick test
    gen = Generator()
    test_skill = Path("/home/gem/workspace/agent/workspace/skills/self-improving-agent")
    if test_skill.exists():
        variant = gen.generate_variant(test_skill)
        print(json.dumps(variant, indent=2))