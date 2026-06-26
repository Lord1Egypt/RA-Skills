#!/usr/bin/env python3
"""
GAN Evolution Engine - Main Orchestrator

Implements Generative Adversarial Evolution for AI Agent Skills.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generator import Generator
from scripts.discriminator import Discriminator
from scripts.population import Population

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GANEvolutionEngine:
    """Main orchestrator for GAN-based skill evolution."""

    def __init__(
        self,
        skill_path: str,
        population_size: int = 20,
        generations: int = 10,
        elite_ratio: float = 0.2,
        mutation_rate: float = 0.1,
        output_dir: str = "evolved",
        model: str = "openrouter/stepfun/step-3.5-flash:free",
        publish: bool = False,
        topic: str = None,
        signals: List[str] = None,
        category: str = "optimize"
    ):
        self.skill_path = Path(skill_path)
        self.population_size = population_size
        self.generations = generations
        self.elite_ratio = elite_ratio
        self.mutation_rate = mutation_rate
        self.output_dir = Path(output_dir)
        self.model = model
        self.publish = publish
        self.topic = topic or f"evolution-{self.skill_path.name}"
        self.signals = signals or ["skill", "evolution", "gan", "optimization", "performance", "automation", "quality"]
        self.category = category

        self.output_dir.mkdir(exist_ok=True)

        # Components
        self.generator = Generator(model=model)
        self.discriminator = Discriminator()
        self.population: Population = None

        # Metrics
        self.history = []
        self.champion_variant = None

    def bootstrap(self):
        """Initialize population by cloning target skill and applying random mutations."""
        logger.info(f"Bootstrapping population from {self.skill_path}")
        self.population = Population(
            skill_path=self.skill_path,
            size=self.population_size,
            mutation_rate=self.mutation_rate
        )
        self.population.initialize()
        logger.info(f"Initial population: {len(self.population)} variants")

    def run_generation(self, gen_idx: int) -> Dict:
        """Execute one generation: Generate → Evaluate → Select."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Generation {gen_idx + 1}/{self.generations}")
        logger.info(f"{'='*60}")

        # 1. Evaluate current population (Discriminator)
        logger.info("Evaluating population...")
        scores = self.discriminator.evaluate_population(self.population)
        self.population.update_scores(scores)

        best = self.population.get_best()
        avg = self.population.get_average()
        logger.info(f"Best fitness: {best.fitness:.3f} (variant {best.variant_id})")
        logger.info(f"Average fitness: {avg:.3f}")

        # 2. Select elites for reproduction
        elite_count = max(1, int(self.population_size * self.elite_ratio))
        elites = self.population.get_elites(elite_count)
        logger.info(f"Selected {len(elites)} elites for crossover")

        # Convert Variant objects to dicts for Generator
        elite_dicts = []
        for e in elites:
            elite_dicts.append({
                "variant_name": e.variant_id,
                "code": e.code,
                "fitness": e.fitness,
                "generation": e.generation,
                "metadata": e.metadata
            })

        # 3. Generate next generation (Generator)
        logger.info("Generating next generation...")
        new_variants = self.generator.generate_next_generation(
            elites=elite_dicts,
            population_size=self.population_size,
            mutation_rate=self.mutation_rate
        )

        # 4. Form next population
        self.population = Population.from_variants(
            new_variants,
            skill_path=self.skill_path,
            mutation_rate=self.mutation_rate
        )

        return {
            "generation": gen_idx + 1,
            "best_fitness": best.fitness,
            "avg_fitness": avg,
            "elite_count": len(elites),
            "population_size": len(self.population)
        }

    def run(self) -> Tuple[Path, float]:
        """Execute full evolution cycle."""
        start_time = time.time()

        # Bootstrap
        self.bootstrap()

        # Evolution loop
        for gen in range(self.generations):
            record = self.run_generation(gen)
            self.history.append(record)

            # Early stopping if convergence (optional)
            if gen > 2 and abs(record["best_fitness"] - self.history[-2]["best_fitness"]) < 0.001:
                logger.info("Convergence detected, stopping early")
                break

        # Final evaluation
        final_scores = self.discriminator.evaluate_population(self.population)
        self.population.update_scores(final_scores)
        champion = self.population.get_best()

        # Save champion
        champion_path = self.output_dir / f"{self.skill_path.name}-v{champion.generation}"
        champion.save(champion_path)
        logger.info(f"🏆 Champion saved: {champion_path}")

        total_time = time.time() - start_time
        logger.info(f"\nEvolution completed in {total_time/60:.1f} minutes")
        logger.info(f"Final best fitness: {champion.fitness:.3f}")

        return champion_path, champion.fitness

    def save_history(self):
        """Save evolution history to JSON."""
        history_path = self.output_dir / "evolution_history.json"
        with open(history_path, 'w') as f:
            json.dump(self.history, f, indent=2)
        logger.info(f"History saved: {history_path}")

    def publish_capsule(self):
        """Publish evolution results as an EvoMap capsule."""
        try:
            champion = self.population.get_best()
            if not champion:
                logger.error("No champion available to publish")
                return

            # Build capsule content
            capsule_content = self._build_capsule_content(champion)

            # Prepare publish command
            publish_script = Path("/home/gem/workspace/agent/workspace/skills/evomap-publish/scripts/publish.py")
            if not publish_script.exists():
                logger.error(f"evomap-publish script not found: {publish_script}")
                return

            # Get credentials from environment or ~/.evomap/
            node_id = os.environ.get("A2A_NODE_ID") or os.environ.get("EVOMAP_NODE_ID")
            node_secret = os.environ.get("A2A_NODE_SECRET") or os.environ.get("EVOMAP_NODE_SECRET")

            if not node_id or not node_secret:
                # Try reading from ~/.evomap/
                evomap_dir = Path.home() / ".evomap"
                if evomap_dir.exists():
                    node_id_file = evomap_dir / "node_id"
                    secret_file = evomap_dir / "node_secret"
                    if node_id_file.exists():
                        node_id = node_id_file.read_text().strip()
                    if secret_file.exists():
                        node_secret = secret_file.read_text().strip()

            if not node_id or not node_secret:
                logger.error("EvoMap credentials not found. Set A2A_NODE_ID and A2A_NODE_SECRET env vars or configure ~/.evomap/")
                return

            # Build command
            cmd = [
                "python3", str(publish_script),
                "--node-id", node_id,
                "--secret", node_secret,
                "--topic", self.topic,
                "--category", self.category,
                "--signals", ",".join(self.signals),
                "--summary", f"GAN evolution of {self.skill_path.name}",
                "--strategy", "Analyze skill variants via generator-discriminator loop",
                "--content", capsule_content,
                "--confidence", str(round(champion.fitness, 2))
            ]

            logger.info(f"Running publish: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                logger.info("✅ Capsule published successfully")
                logger.info(result.stdout)
            else:
                logger.error(f"Publish failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Publish error: {e}", exc_info=True)

    def _build_capsule_content(self, champion) -> str:
        """Generate capsule content describing the evolution results."""
        history_summary = ""
        for record in self.history[-5:]:  # Last 5 generations
            history_summary += f"Gen {record['generation']}: best={record['best_fitness']:.3f}, avg={record['avg_fitness']:.3f}\n"

        content = f"""
# GAN Evolution Results: {self.skill_path.name}

**Champion:** {champion.variant_id}
**Final Fitness:** {champion.fitness:.3f}
**Generations:** {self.generations}
**Population Size:** {self.population_size}

## Performance Trend
```
{history_summary}
```

## Technical Approach
- **Generator:** LLM-powered code mutation and crossover
- **Discriminator:** Automated benchmark-based fitness evaluation
- **Strategy:** Elite selection + mutation rate {self.mutation_rate}

## Evolutionary Insights
- Best fitness improved from baseline to {champion.fitness:.3f}
- Champion implements {len(champion.metadata.get('changes', []))} distinct changes
- Key improvements: (auto-detected by fitness metrics)

## Next Steps
- Apply learned mutations to production codebase
- Run extended benchmark suite for validation
- Consider increasing population size for future runs

**Model:** {self.model}
**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}
""".strip()
        return content


def main():
    parser = argparse.ArgumentParser(description="GAN Evolution Engine for Skills")
    parser.add_argument("--skill", required=True, help="Path to target skill directory")
    parser.add_argument("--generations", type=int, default=10, help="Number of generations")
    parser.add_argument("--population", type=int, default=20, help="Population size")
    parser.add_argument("--elite-ratio", type=float, default=0.2, help="Elite selection ratio")
    parser.add_argument("--mutation-rate", type=float, default=0.1, help="Mutation probability")
    parser.add_argument("--output", default="evolved", help="Output directory")
    parser.add_argument("--model", default="openrouter/stepfun/step-3.5-flash:free", help="LLM model")
    parser.add_argument("--publish", action="store_true", help="Publish capsule to EvoMap")
    parser.add_argument("--promote", action="store_true", help="Promote champion to production")
    parser.add_argument("--topic", help="EvoMap topic for capsule (default: evolution-<skillname>)")
    parser.add_argument("--signals", default="skill,evolution,gan,optimization,performance,automation,quality",
                        help="Comma-separated signal tags for capsule")
    parser.add_argument("--category", default="optimize", choices=["repair", "optimize", "innovate", "regulatory"],
                        help="Capsule category")

    args = parser.parse_args()

    # Validate skill path
    skill_path = Path(args.skill)
    if not skill_path.exists():
        logger.error(f"Skill not found: {skill_path}")
        sys.exit(1)

    # Parse signals
    signals = [s.strip() for s in args.signals.split(",") if s.strip()]

    # Run evolution
    engine = GANEvolutionEngine(
        skill_path=str(skill_path),
        population_size=args.population,
        generations=args.generations,
        elite_ratio=args.elite_ratio,
        mutation_rate=args.mutation_rate,
        output_dir=args.output,
        model=args.model,
        publish=args.publish,
        topic=args.topic,
        signals=signals,
        category=args.category
    )

    champion_path, fitness = engine.run()
    engine.save_history()

    logger.info(f"\n✅ Evolution complete!")
    logger.info(f"🏆 Champion: {champion_path}")
    logger.info(f"📊 Final fitness: {fitness:.3f}")

    # Optional: publish to EvoMap
    if args.publish:
        logger.info("📤 Publishing capsule to EvoMap...")
        engine.publish_capsule()


if __name__ == "__main__":
    main()