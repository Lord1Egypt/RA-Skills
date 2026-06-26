"""
Multi-Agent Debate Framework — adversarial reasoning for better conclusions
AgentBounty: Dialectic AI $5,200
"""
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from collections import defaultdict


class Stance(Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    SYNTHESIZE = "synthesize"
    DEVIL_ADVOCATE = "devil_advocate"
    EXPERT = "expert"


@dataclass
class Argument:
    agent_name: str
    stance: str
    content: str
    round_num: int
    responding_to: Optional[str] = None  # agent_name being responded to
    score: float = 0.0
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class Agent:
    name: str
    stance: str
    model: str = "default"
    system_prompt: str = ""
    personality: str = ""  # e.g. "analytical", "creative", "skeptical"

    def get_system_prompt(self, topic: str) -> str:
        base = f"You are {self.name}, arguing {self.stance} the topic: '{topic}'."
        if self.personality:
            base += f" Your style is {self.personality}."
        if self.system_prompt:
            base += f" {self.system_prompt}"
        stance_guidance = {
            "support": "Make the strongest case FOR the topic. Use evidence, logic, and examples.",
            "oppose": "Make the strongest case AGAINST the topic. Find flaws, counterexamples, and risks.",
            "synthesize": "Find common ground between opposing views. Identify where both sides agree.",
            "devil_advocate": "Argue the weakest points to expose vulnerabilities and strengthen the final conclusion.",
            "expert": "Provide deep domain knowledge. Cite specific research, data, and technical details.",
        }
        base += f" {stance_guidance.get(self.stance, '')}"
        return base


@dataclass
class JudgeCriteria:
    evidence: float = 1.0    # Weight for factual support
    logic: float = 1.0       # Weight for logical coherence
    novelty: float = 0.5     # Weight for original insights
    completeness: float = 0.8  # Weight for addressing all points
    clarity: float = 0.3     # Weight for clear expression


class Judge:
    """Evaluate debate arguments and determine winners."""

    def __init__(self, criteria: Optional[JudgeCriteria] = None, model: str = "default"):
        self.criteria = criteria or JudgeCriteria()
        self.model = model

    def score_argument(self, argument: Argument, all_arguments: list[Argument]) -> float:
        """Score an argument based on criteria. Simplified heuristic scoring."""
        score = 0.0
        content = argument.content.lower()
        word_count = len(content.split())

        # Evidence: mentions of data, studies, numbers, citations
        evidence_markers = ["study", "research", "data", "%", "percent", "according to",
                           "evidence", "shown", "proven", "demonstrated", "cited"]
        evidence_count = sum(1 for m in evidence_markers if m in content)
        score += min(evidence_count * 0.1, 0.5) * self.criteria.evidence

        # Logic: transitional reasoning markers
        logic_markers = ["therefore", "because", "however", "consequently", "thus",
                        "implies", "follows", "given that", "if...then", "alternatively"]
        logic_count = sum(1 for m in logic_markers if m.replace("...", " ") in content)
        score += min(logic_count * 0.08, 0.4) * self.criteria.logic

        # Novelty: unique points not raised by others
        other_content = " ".join(a.content.lower() for a in all_arguments if a.id != argument.id)
        unique_words = set(content.split()) - set(other_content.split())
        novelty_ratio = len(unique_words) / max(word_count, 1)
        score += min(novelty_ratio, 0.3) * self.criteria.novelty

        # Completeness: responds to counterarguments
        if argument.responding_to:
            score += 0.2 * self.criteria.completeness

        # Clarity: reasonable length, not too short or verbose
        if 50 < word_count < 800:
            score += 0.15 * self.criteria.clarity
        elif 30 < word_count < 1200:
            score += 0.05 * self.criteria.clarity

        # Response quality: addresses specific points
        response_markers = ["you argue", "your point about", "addressing", "counter to", "in response"]
        if argument.responding_to and any(m in content for m in response_markers):
            score += 0.1

        return round(min(score, 1.0), 3)

    def evaluate_round(self, arguments: list[Argument]) -> dict:
        for arg in arguments:
            arg.score = self.score_argument(arg, arguments)

        by_stance = defaultdict(list)
        for arg in arguments:
            by_stance[arg.stance].append(arg)

        stance_avg = {stance: sum(a.score for a in args) / len(args) for stance, args in by_stance.items() if args}
        winner = max(stance_avg, key=stance_avg.get) if stance_avg else "draw"

        return {
            "round_winner": winner,
            "stance_scores": {k: round(v, 3) for k, v in stance_avg.items()},
            "best_argument": max(arguments, key=lambda a: a.score).id if arguments else None,
        }

    def final_verdict(self, rounds: list[dict], all_arguments: list[Argument]) -> dict:
        # Aggregate round winners
        round_winners = [r["round_winner"] for r in rounds]
        win_counts = defaultdict(int)
        for w in round_winners:
            win_counts[w] += 1

        overall_winner = max(win_counts, key=win_counts.get) if win_counts else "draw"

        # Find consensus points (arguments where both sides agree)
        support_args = [a for a in all_arguments if a.stance == "support"]
        oppose_args = [a for a in all_arguments if a.stance == "oppose"]
        synth_args = [a for a in all_arguments if a.stance == "synthesize"]

        consensus = [a.content[:100] for a in synth_args if a.score > 0.3]

        # Top arguments
        top_args = sorted(all_arguments, key=lambda a: a.score, reverse=True)[:5]

        return {
            "overall_winner": overall_winner,
            "rounds_won": dict(win_counts),
            "consensus_points": consensus,
            "top_arguments": [{"agent": a.agent_name, "stance": a.stance, "score": a.score, "excerpt": a.content[:150]} for a in top_args],
            "total_arguments": len(all_arguments),
            "confidence": round(sum(a.score for a in all_arguments) / max(len(all_arguments), 1), 3),
        }


class Debate:
    """Orchestrate a multi-agent debate."""

    def __init__(self, topic: str, rounds: int = 3, max_words: int = 500, convergence: float = 0.7):
        self.topic = topic
        self.rounds = rounds
        self.max_words = max_words
        self.convergence_threshold = convergence
        self.agents: list[Agent] = []
        self.judge: Optional[Judge] = None
        self.arguments: list[Argument] = []
        self.round_results: list[dict] = []
        self.id = str(uuid.uuid4())[:8]

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def set_judge(self, judge: Judge):
        self.judge = judge

    def _simulate_argument(self, agent: Agent, round_num: int, responding_to: Optional[Argument] = None) -> Argument:
        """Simulate an agent's argument. In production, call the LLM here."""
        # This is a placeholder that generates a mock argument structure
        # Real implementation would call agent.model with agent.get_system_prompt(self.topic)
        content = f"[{agent.name} arguing {agent.stance} on round {round_num}] "
        if responding_to:
            content += f"In response to {responding_to.agent_name}: "
        content += f"Regarding '{self.topic}', the {agent.stance} position holds that..."

        return Argument(
            agent_name=agent.name,
            stance=agent.stance,
            content=content,
            round_num=round_num,
            responding_to=responding_to.agent_name if responding_to else None,
        )

    def run(self) -> dict:
        """Execute the full debate."""
        if not self.judge:
            self.judge = Judge()

        for round_num in range(1, self.rounds + 1):
            round_args = []

            # Each agent argues in order
            for agent in self.agents:
                # Find the best opposing argument from previous round to respond to
                responding_to = None
                if round_num > 1:
                    prev = [a for a in self.arguments if a.round_num == round_num - 1 and a.stance != agent.stance]
                    if prev:
                        responding_to = max(prev, key=lambda a: a.score)

                arg = self._simulate_argument(agent, round_num, responding_to)
                round_args.append(arg)
                self.arguments.append(arg)

            # Judge this round
            result = self.judge.evaluate_round(round_args)
            self.round_results.append(result)

            # Check convergence
            if result["stance_scores"]:
                scores = list(result["stance_scores"].values())
                if len(scores) >= 2 and max(scores) - min(scores) < (1 - self.convergence_threshold) * 0.3:
                    break

        verdict = self.judge.final_verdict(self.round_results, self.arguments)
        return {
            "debate_id": self.id,
            "topic": self.topic,
            "rounds_completed": len(self.round_results),
            "verdict": verdict,
            "round_results": self.round_results,
        }

    def export(self) -> str:
        """Export full debate transcript as JSON."""
        return json.dumps({
            "id": self.id,
            "topic": self.topic,
            "agents": [{"name": a.name, "stance": a.stance, "model": a.model} for a in self.agents],
            "arguments": [{"id": a.id, "agent": a.agent_name, "stance": a.stance, "round": a.round_num, "content": a.content, "score": a.score, "responding_to": a.responding_to} for a in self.arguments],
            "round_results": self.round_results,
        }, indent=2)


if __name__ == "__main__":
    debate = Debate("Should startups use microservices architecture?")
    debate.add_agent(Agent("pro_ms", stance="support", model="gpt-4o", personality="data-driven"))
    debate.add_agent(Agent("anti_ms", stance="oppose", model="claude-sonnet-4", personality="skeptical"))
    debate.add_agent(Agent("synth", stance="synthesize", model="gemini-2.5-pro", personality="balanced"))
    debate.set_judge(Judge())
    result = debate.run()
    print(json.dumps(result["verdict"], indent=2))
