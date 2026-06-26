#!/usr/bin/env python3
"""
Population: Manages a collection of skill variants.

Responsibilities:
- Initialize population from a skill (cloning + mutations)
- Store and update fitness scores
- Select elites via ranking
- Persist variants to disk
"""

import hashlib
import json
import random
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import filelock


@dataclass
class Variant:
    """Represents one skill variant in the population."""
    variant_id: str
    path: Path  # Where variant code lives (temporary)
    generation: int
    fitness: float = 0.0
    code: Dict[str, str] = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

    def save(self, dest_path: Path):
        """Write variant code to destination directory."""
        dest_path.mkdir(parents=True, exist_ok=True)
        for rel_path, content in self.code.items():
            file_path = dest_path / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

        # Save metadata
        meta_file = dest_path / ".variant.json"
        meta_file.write_text(json.dumps({
            "id": self.variant_id,
            "generation": self.generation,
            "fitness": self.fitness,
            "metadata": self.metadata
        }, indent=2))

    def compute_hash(self) -> str:
        """Compute deterministic hash of code content."""
        content_str = json.dumps(self.code, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]


class Population:
    """Manages a set of variants."""

    def __init__(
        self,
        skill_path: Path,
        size: int,
        mutation_rate: float = 0.1,
        work_dir: str = ".gan_evolution"
    ):
        self.skill_path = skill_path
        self.size = size
        self.mutation_rate = mutation_rate
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(exist_ok=True)

        self.variants: List[Variant] = []
        self.generation = 0

    def initialize(self):
        """Bootstrap population: clone skill N times with random mutations."""
        base_id = self.skill_path.name
        for i in range(self.size):
            variant_id = f"{base_id}_gen0_var{i}"
            variant_dir = self.work_dir / f"gen0" / variant_id
            variant_dir.mkdir(parents=True, exist_ok=True)

            # Clone skill files
            code = self._clone_skill_code()

            # Apply random mutation (small chance per file)
            if random.random() < self.mutation_rate:
                code = self._random_mutation(code)

            variant = Variant(
                variant_id=variant_id,
                path=variant_dir,
                generation=0,
                code=code,
                metadata={"parent": "original", "mutations": []}
            )
            variant.save(variant_dir)
            self.variants.append(variant)

    def initialize_from_variants(self, variants: List[Dict]):
        """Replace population with provided variants."""
        self.variants = []
        for var_data in variants:
            variant = Variant(
                variant_id=var_data["variant_name"],
                path=self.work_dir / f"gen{var_data['generation']}" / var_data["variant_name"],
                generation=var_data["generation"],
                code=var_data["code"],
                metadata={"changes": var_data.get("changes", [])}
            )
            self.variants.append(variant)

    def _clone_skill_code(self) -> Dict[str, str]:
        """Copy all skill files into dict {rel_path: content}."""
        code = {}
        for file in self.skill_path.rglob("*"):
            if file.is_file():
                rel = file.relative_to(self.skill_path)
                code[str(rel)] = file.read_text()
        return code

    def _random_mutation(self, code: Dict[str, str]) -> Dict[str, str]:
        """Apply a simple random mutation."""
        # Choose random file
        if not code:
            return code

        file_key = random.choice(list(code.keys()))
        content = code[file_key]

        # Simple mutations
        mutations = [
            lambda s: s.replace("True", "False") if "True" in s else s,
            lambda s: s.replace("False", "True") if "False" in s else s,
            lambda s: s.replace("0.5", "0.6") if "0.5" in s else s,
            lambda s: s + "\n# mutated: " + str(random.randint(1000, 9999)) if s.endswith("\n") else s + "\n# mutated",
        ]

        mutation = random.choice(mutations)
        new_content = mutation(content)

        code[file_key] = new_content
        return code

    def update_scores(self, scores: List[float]):
        """Update fitness scores for all variants."""
        if len(scores) != len(self.variants):
            raise ValueError("Score count mismatch")
        for variant, score in zip(self.variants, scores):
            variant.fitness = score

    def get_best(self) -> Variant:
        """Return variant with highest fitness."""
        return max(self.variants, key=lambda v: v.fitness)

    def get_average(self) -> float:
        """Compute average fitness."""
        if not self.variants:
            return 0.0
        return sum(v.fitness for v in self.variants) / len(self.variants)

    def get_elites(self, count: int) -> List[Variant]:
        """Return top-N variants by fitness."""
        sorted_variants = sorted(self.variants, key=lambda v: v.fitness, reverse=True)
        return sorted_variants[:count]

    def __len__(self):
        return len(self.variants)

    @staticmethod
    def from_variants(variants: List[Dict], skill_path: Path = None, mutation_rate: float = 0.1) -> 'Population':
        """Create Population instance from raw variant data."""
        pop = Population(skill_path or Path("."), size=len(variants), mutation_rate=mutation_rate)
        pop.initialize_from_variants(variants)
        return pop

    def initialize_from_variants(self, variants: List[Dict]):
        """Replace current variants with provided variant data."""
        self.variants = []
        for var_data in variants:
            variant = Variant(
                variant_id=var_data["variant_name"],
                path=self.work_dir / f"gen{var_data['generation']}" / var_data["variant_name"],
                generation=var_data["generation"],
                code=var_data["code"],
                fitness=var_data.get("fitness", 0.0),
                metadata={
                    "changes": var_data.get("changes", []),
                    "reasoning": var_data.get("reasoning", "")
                }
            )
            self.variants.append(variant)


if __name__ == "__main__":
    # Quick test
    skill_path = Path("/home/gem/workspace/agent/workspace/skills/self-improving-agent")
    pop = Population(skill_path, size=5)
    pop.initialize()
    print(f"Population initialized with {len(pop)} variants")
    for v in pop.variants[:3]:
        print(f"  - {v.variant_id} (fitness={v.fitness})")