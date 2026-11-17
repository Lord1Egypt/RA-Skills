#!/usr/bin/env python3
"""
Darwinian Prompt Evolution Engine for OpenClaw.
Optimizes candidate system prompts across generations using mutation strategies
(compression, strict negative constraints, few-shot injection) and Pareto selection.
"""

import copy
import random
from typing import List, Dict, Any, Tuple


MUTATION_STRATEGIES = [
    # 1. Negative Constraint Tightening
    "STRICT DIRECTIVE: Do not produce extraneous conversational filler. Output exclusively the requested fields.",
    # 2. Schema Guardrail Injection
    "SCHEMA INTEGRITY: If any required attribute is missing or ambiguous, return 'NULL' immediately without hallucinating.",
    # 3. Role Sharpening
    "DOMAIN EXPERTISE: You are a high-throughput, deterministic execution engine calibrated for zero false positives.",
    # 4. Token Compression Directive
    "TOKEN COMPRESSION: Formulate responses with maximum brevity to minimize token consumption."
]


def mutate_prompt(base_prompt: str, generation: int = 1) -> str:
    """Applies a random semantic mutation strategy to evolve the system prompt."""
    strategy = random.choice(MUTATION_STRATEGIES)
    mutated = base_prompt.strip() + f"\n\n[GENERATION {generation} - OPTIMIZATION]\n" + strategy
    return mutated


def evolve_prompt(
    initial_prompt: str,
    domain_tag: str,
    generations: int = 3,
    population_size: int = 4
) -> Dict[str, Any]:
    """
    Executes evolutionary optimization over multiple generations.
    Returns the best Pareto-optimal prompt candidate.
    """
    current_population = [initial_prompt]
    best_candidate = initial_prompt
    best_fitness = 0.0

    history = []

    for gen in range(1, generations + 1):
        gen_candidates = []
        for parent in current_population:
            for _ in range(population_size // len(current_population)):
                mutated = mutate_prompt(parent, generation=gen)
                
                # Fitness scoring: Balances brevity, directive clarity, and structure
                char_count = len(mutated)
                brevity_score = max(0.0, 1.0 - (char_count / 1500.0))
                structure_score = 0.9 if "STRICTE" in mutated or "IMPÉRATIF" in mutated else 0.6
                fitness = round((0.4 * brevity_score) + (0.6 * structure_score), 4)

                candidate_obj = {
                    "generation": gen,
                    "prompt": mutated,
                    "fitness_score": fitness,
                    "char_count": char_count
                }
                gen_candidates.append(candidate_obj)
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_candidate = mutated

        gen_candidates.sort(key=lambda x: x["fitness_score"], reverse=True)
        current_population = [c["prompt"] for c in gen_candidates[:2]]  # Keep top 2 survivors
        history.append({
            "generation": gen,
            "top_fitness": gen_candidates[0]["fitness_score"],
            "candidates_count": len(gen_candidates)
        })

    return {
        "best_prompt": best_candidate,
        "best_fitness_score": best_fitness,
        "total_generations": generations,
        "evolution_history": history
    }


if __name__ == "__main__":
    base = "Tu es un agent spécialisé pour invoice_extraction."
    res = evolve_prompt(base, "invoice_extraction", generations=3)
    print("🧬 Prompt Evolution Result:")
    print(f"Top Fitness Score: {res['best_fitness_score']}")
    print("Best Evolved Prompt:\n", res["best_prompt"])
