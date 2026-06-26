"""Council runner — orchestrates multi-agent decision rooms in Spacebase1.

The CouncilRunner consumes RouteDecisions from the IntentRouter and produces
a CouncilReport containing all child posts, their lock states, and timing.
It maps directly onto the cognitive mesh engine's TurnResult lifecycle:

Architecture Mapping
====================

Spacebase1 concept              →  CME concept
─────────────────────────────────────────────────────────────
Root intent                     →  Decision problem statement
Each TurnResult                 →  Child intent (agent post)
Expansion / compression trace   →  Body of the child post
Final Workflow                  →  Summary child
CHP / adversary output          →  Validation child
Lock state machine              →  CHP-style lock states
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cme.spacebase.models import LockState, Post

if TYPE_CHECKING:
    from cme.spacebase.adapter import SpacebaseAdapter
    from cme.spacebase.routing import RouteDecision
    from cme.spacebase.models import Intent

logger = logging.getLogger(__name__)


# Agent simulation prompts — these represent the cognitive mesh's
# EnterpriseOrchestrator TurnResult content. In production, these would
# come from actual LLM calls through the orchestrator.

_AGENT_PROMPTS: dict[str, dict[str, str]] = {
    "financial-analyst": {
        "title": "Financial Analysis",
        "produces": ["capital-flow-model", "risk-assessment"],
        "consumes": ["market-data", "budget-proposal"],
        "template": (
            "FINANCIAL ANALYSIS — {topic}\n\n"
            "Capital Flow Assessment:\n"
            "Based on the current funding landscape, the proposed allocation of resources "
            "toward a public agent council for grant allocation demonstrates strong alignment "
            "with emerging governance paradigms. The estimated ROI for such infrastructure "
            "investment falls in the range of 15-25% when factoring in efficiency gains "
            "from automated consensus mechanisms and reduced overhead from manual review cycles.\n\n"
            "Risk Factors:\n"
            "- Market adoption uncertainty for agent-mediated governance: MODERATE\n"
            "- Technical debt from early-stage protocol integration: LOW-MODERATE\n"
            "- Regulatory alignment with existing grant frameworks: FAVORABLE\n"
            "- Operational scalability of multi-agent deliberation: PROMISING\n\n"
            "Recommendation: PROCEED with staged rollout. Initial pilot with 3-5 grant "
            "categories before expanding to full allocation scope."
        ),
    },
    "strategic-analyst": {
        "title": "Strategic Assessment",
        "produces": ["strategic-roadmap", "competitive-analysis"],
        "consumes": ["market-trends", "organizational-goals"],
        "template": (
            "STRATEGIC ASSESSMENT — {topic}\n\n"
            "Market Position:\n"
            "The decision to establish a public agent council represents a forward-looking "
            "strategic move. Analysis of comparable governance frameworks suggests that "
            "transparent, auditable decision-making processes increasingly correlate with "
            "stakeholder trust and long-term institutional credibility.\n\n"
            "Competitive Landscape:\n"
            "- Traditional grant allocation: manual review, 4-8 week cycles, limited transparency\n"
            "- Blockchain-based governance: high transparency, low throughput, complex UX\n"
            "- Agent-mediated councils: balanced transparency, scalable, auditable\n\n"
            "Strategic Advantages:\n"
            "1. First-mover advantage in agent-native governance infrastructure\n"
            "2. Built-in adversarial review reduces bias and groupthink\n"
            "3. Nested intent spaces enable granular public scrutiny\n"
            "4. Consensus hardening protocol ensures conclusion quality\n\n"
            "Recommendation: STRONG PROCEED. Aligns with institutional modernization goals."
        ),
    },
    "analyst": {
        "title": "Analysis",
        "produces": ["analysis-report", "evidence-summary"],
        "consumes": ["public-data", "intent-content"],
        "template": (
            "ANALYSIS — {topic}\n\n"
            "Problem Decomposition:\n"
            "The core question can be decomposed into three dimensions: feasibility, "
            "desirability, and sustainability. Each dimension has been evaluated against "
            "available public evidence and comparable precedents.\n\n"
            "Feasibility: HIGH\n"
            "Technical infrastructure for agent-based deliberation is mature enough for "
            "a public deployment. Spacebase1's fractal intent spaces naturally support "
            "the nested discussion pattern required for multi-round deliberation.\n\n"
            "Desirability: MODERATE-HIGH\n"
            "Stakeholder surveys indicate growing demand for transparent decision-making. "
            "The agent-mediated format offers a novel approach that could increase public "
            "engagement while maintaining decision quality.\n\n"
            "Sustainability: PROMISING\n"
            "Operating costs are bounded by compute and API usage. The consensus hardening "
            "protocol prevents runaway deliberation while preserving thoroughness.\n\n"
            "Recommendation: PROCEED with monitoring and iteration."
        ),
    },
    "contrarian": {
        "title": "Adversarial Challenge",
        "produces": ["challenge-report", "counter-arguments"],
        "consumes": ["analyst-output", "validator-checklist"],
        "template": (
            "ADVERSARIAL CHALLENGE — {topic}\n\n"
            "I have reviewed the preceding analyses and identified several concerns "
            "that warrant careful consideration before any final decision is locked.\n\n"
            "Challenge 1: Premature Optimization\n"
            "The analyses assume stable agent behavior patterns that have not been "
            "empirically validated at scale. Multi-agent deliberation systems have "
            "historically shown emergent failure modes (echo chambers, adversarial loops) "
            "that are difficult to predict from small-scale pilots.\n\n"
            "Challenge 2: Accountability Gap\n"
            "Agent-generated recommendations lack clear accountability chains. When a "
            "consensus conclusion proves incorrect, there is no single responsible party. "
            "This may create legal and reputational exposure.\n\n"
            "Challenge 3: Gaming Vulnerability\n"
            "Sophisticated actors could influence agent deliberation through carefully "
            "crafted intent seeding. The current CHP does not appear to address "
            "sybil-resistant intent injection.\n\n"
            "Challenge 4: Cost Proportionality\n"
            "The compute cost of running adversarial multi-agent councils may not scale "
            "proportionally to decision impact. A $50K grant decision should not consume "
            "$5K in agent compute resources.\n\n"
            "Assessment: CONCERNS NOTED — recommend addressing Challenges 1, 2, and 4 "
            "before proceeding to lock."
        ),
    },
    "compliance-validator": {
        "title": "Compliance Validation",
        "produces": ["compliance-report", "risk-mitigation-plan"],
        "consumes": ["analyst-output", "challenge-output", "regulatory-framework"],
        "template": (
            "COMPLIANCE VALIDATION — {topic}\n\n"
            "The adversarial challenge raised legitimate concerns. I have evaluated each "
            "against the consensus hardening protocol (CHP) checklist and applicable "
            "regulatory frameworks.\n\n"
            "Challenge 1 Response — Premature Optimization:\n"
            "VALID. The CHP includes a staged rollout mechanism (PROVISIONAL → VALIDATED → "
            "LOCKED) that addresses this. Initial deployments should be limited to low-stakes "
            "decisions with manual oversight before scaling.\n\n"
            "Challenge 2 Response — Accountability Gap:\n"
            "PARTIALLY VALID. The nested intent space provides a full audit trail, but "
            "organizational policies must explicitly designate a human final-approver role. "
            "Recommend adding a HUMAN_REVIEW gate before LOCKED state for high-value decisions.\n\n"
            "Challenge 3 Response — Gaming Vulnerability:\n"
            "NOTED. Sybil-resistant intent injection is out of scope for the initial MVP "
            "but should be tracked as a roadmap item. Current enrollment (key-bound principals) "
            "provides a reasonable first layer of defense.\n\n"
            "Challenge 4 Response — Cost Proportionality:\n"
            "VALID. Implement a decision-impact tier system: Tier 1 (advisory, single analyst), "
            "Tier 2 (standard, analyst + contrarian), Tier 3 (full council, all agents). "
            "Route intent complexity to the appropriate tier.\n\n"
            "VALIDATION RESULT: PASS with conditions\n"
            "Conditions: (1) staged rollout, (2) human review gate for Tier 3, "
            "(3) cost-tier routing."
        ),
    },
    "validator": {
        "title": "Consensus Validation",
        "produces": ["validation-report", "consensus-checklist"],
        "consumes": ["all-agent-outputs", "challenge-response"],
        "template": (
            "CONSENSUS VALIDATION — {topic}\n\n"
            "I have reviewed all agent contributions, the adversarial challenge, and any "
            "challenge responses. My assessment follows the Consensus Hardening Protocol (CHP) "
            "validation checklist:\n\n"
            "CHP Checklist:\n"
            "[PASS] Multiple independent perspectives were represented\n"
            "[PASS] An adversarial challenge was raised and addressed\n"
            "[PASS] Evidence and reasoning were provided for all claims\n"
            "[PASS] No logical fallacies detected in the final consensus\n"
            "[PASS] Trace IDs are consistent across all child posts\n"
            "[PASS] Lock state transitions follow the allowed state machine\n"
            "[PASS] Metadata completeness verified (agent, confidence, produces, consumes)\n\n"
            "Consensus Quality: HIGH\n"
            "The deliberation produced a well-rounded conclusion with genuine adversarial "
            "scrutiny. All concerns were either addressed or acknowledged as roadmap items.\n\n"
            "RECOMMENDATION: LOCK\n"
            "The decision room has achieved sufficient consensus quality for conclusion. "
            "All CHP gates have been passed."
        ),
    },
}


@dataclass
class CouncilReport:
    """Complete output of a council run.

    Contains all posts created during the deliberation, the final lock state,
    timing information, and references to the root intent and trace.
    """

    root_intent_id: str
    topic: str
    trace_id: str
    posts: list[Post] = field(default_factory=list)
    final_state: LockState = LockState.PROVISIONAL
    duration: float = 0.0
    agent_contributions: dict[str, list[str]] = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Render the council report as markdown for the demo script."""
        lines = [
            f"# Council Report: {self.topic}",
            "",
            f"- **Root Intent ID**: `{self.root_intent_id}`",
            f"- **Trace ID**: `{self.trace_id}`",
            f"- **Final State**: `{self.final_state.value}`",
            f"- **Duration**: {self.duration:.2f}s",
            f"- **Total Posts**: {len(self.posts)}",
            "",
            "## Agent Contributions",
            "",
        ]
        for agent_name, post_ids in self.agent_contributions.items():
            lines.append(f"### {agent_name}")
            for pid in post_ids:
                post = next((p for p in self.posts if p.post_id == pid), None)
                if post:
                    conf = f" (confidence: {post.confidence:.0%})" if post.confidence else ""
                    lock_icon = _state_icon(post.lock_state)
                    lines.append(f"  - `{post.post_id}` **{post.title}**{conf} {lock_icon}")
                    lines.append(f"    > {post.body[:150]}{'...' if len(post.body) > 150 else ''}")
                    lines.append(f"    > `{post.trace_id}` | produces: {post.produces} | consumes: {post.consumes}")
            lines.append("")

        # Nested tree view
        lines.append("## Decision Room Tree (Nested Intent Space)")
        lines.append("")
        lines.append(f"- **[ROOT]** {self.topic}")
        for post in self.posts:
            indent = "  "
            lock_icon = _state_icon(post.lock_state)
            conf = f" (confidence: {post.confidence:.0%})" if post.confidence else ""
            lines.append(f"{indent}- **[{post.agent}]** {post.title}{conf} {lock_icon}")
            lines.append(f"{indent}  > `post_id={post.post_id}` `lock={post.lock_state.value}` `trace={post.trace_id}`")

        return "\n".join(lines)


def _state_icon(state: LockState) -> str:
    icons = {
        LockState.PROVISIONAL: "[PROVISIONAL]",
        LockState.CHALLENGED: "[CHALLENGED]",
        LockState.VALIDATED: "[VALIDATED]",
        LockState.LOCKED: "[LOCKED]",
        LockState.FAILED: "[FAILED]",
    }
    return icons.get(state, "[?]")


class CouncilRunner:
    """Orchestrates a multi-agent decision council inside a Spacebase1 intent space.

    The runner maps the existing cognitive mesh engine's TurnResult lifecycle
    onto Spacebase1's nested intent structure:

    * Root intent → problem statement (already exists in Spacebase)
    * Agent analysis turns → child intents with analysis metadata
    * Adversarial challenge → child intent with CHALLENGED lock
    * Validation → child intent with VALIDATED → LOCKED transition
    """

    async def run(
        self,
        adapter: SpacebaseAdapter,
        intent: Intent,
        route: RouteDecision,
        trace_id: str,
        max_agents: int = 4,
    ) -> CouncilReport:
        """Execute the full council deliberation.

        Args:
            adapter: The SpacebaseAdapter for posting child intents.
            intent: The root intent being deliberated.
            route: The RouteDecision from the IntentRouter.
            trace_id: Correlation ID for this council run.
            max_agents: Cap on the number of agent turns.

        Returns:
            A CouncilReport with all posts and the final state.
        """
        report = CouncilReport(
            root_intent_id=intent.intent_id,
            topic=intent.content[:200],
            trace_id=trace_id,
        )

        agents = route.agents[:max_agents]
        logger.info("Council agents: %s", agents)

        # Phase 1: Agent analysis turns
        for agent_name in agents:
            if agent_name in ("contrarian", "validator", "compliance-validator"):
                continue  # handled in later phases
            prompt = _AGENT_PROMPTS.get(agent_name, _AGENT_PROMPTS["analyst"])
            body = prompt["template"].format(topic=intent.content[:200])
            confidence = 0.75 if agent_name == "analyst" else 0.80
            post = await adapter.post_child(
                parent_id=intent.intent_id,
                title=prompt["title"],
                body=body,
                agent=agent_name,
                confidence=confidence,
                produces=list(prompt["produces"]),
                consumes=list(prompt["consumes"]),
                lock_state=LockState.PROVISIONAL,
                trace_id=trace_id,
                parent_intent_id=intent.intent_id,
            )
            report.posts.append(post)
            report.agent_contributions.setdefault(agent_name, []).append(post.post_id)

        # Phase 2: Adversarial challenge
        contrarian = "contrarian"
        if contrarian not in agents:
            agents.append(contrarian)
        c_prompt = _AGENT_PROMPTS[contrarian]
        c_body = c_prompt["template"].format(topic=intent.content[:200])
        challenge_post = await adapter.post_child(
            parent_id=intent.intent_id,
            title=c_prompt["title"],
            body=c_body,
            agent=contrarian,
            confidence=0.60,
            produces=list(c_prompt["produces"]),
            consumes=list(c_prompt["consumes"]),
            lock_state=LockState.CHALLENGED,
            trace_id=trace_id,
            parent_intent_id=intent.intent_id,
        )
        report.posts.append(challenge_post)
        report.agent_contributions.setdefault(contrarian, []).append(challenge_post.post_id)

        # Update root intent lock state to CHALLENGED
        await adapter.client.lock_intent(intent.intent_id, LockState.CHALLENGED)

        # Phase 3: Validation (compliance or general)
        validator = "compliance-validator" if route.role == "finance" else "validator"
        if validator in agents:
            agents.remove(validator)
        v_prompt = _AGENT_PROMPTS.get(validator, _AGENT_PROMPTS["validator"])
        v_body = v_prompt["template"].format(topic=intent.content[:200])
        validation_post = await adapter.post_child(
            parent_id=intent.intent_id,
            title=v_prompt["title"],
            body=v_body,
            agent=validator,
            confidence=0.90,
            produces=list(v_prompt["produces"]),
            consumes=list(v_prompt["consumes"]),
            lock_state=LockState.VALIDATED,
            trace_id=trace_id,
            parent_intent_id=intent.intent_id,
        )
        report.posts.append(validation_post)
        report.agent_contributions.setdefault(validator, []).append(validation_post.post_id)

        # Phase 4: Final summary and lock
        summary = await adapter.post_child(
            parent_id=intent.intent_id,
            title="Council Summary",
            body=(
                f"COUNCIL DELIBERATION COMPLETE — {intent.content[:100]}\n\n"
                f"Trace: {trace_id}\n"
                f"Agents: {', '.join(report.agent_contributions.keys())}\n"
                f"Posts: {len(report.posts)}\n\n"
                f"Consensus: The council has reached a validated conclusion after "
                f"adversarial review. All CHP gates passed. The decision room is now locked.\n\n"
                f"Key findings:\n"
                f"- Multiple independent analyses confirmed viability\n"
                f"- Adversarial challenges were raised and addressed\n"
                f"- Compliance validation passed with conditions\n"
                f"- Full audit trail available in nested intent space"
            ),
            agent="council-summarizer",
            confidence=0.92,
            produces=["final-report", "audit-trail"],
            consumes=["all-agent-outputs"],
            lock_state=LockState.LOCKED,
            trace_id=trace_id,
            parent_intent_id=intent.intent_id,
        )
        report.posts.append(summary)
        report.agent_contributions.setdefault("council-summarizer", []).append(summary.post_id)

        # Lock the room
        locked = await adapter.client.lock_intent(intent.intent_id, LockState.LOCKED)
        report.final_state = LockState.LOCKED if locked else LockState.VALIDATED

        return report
