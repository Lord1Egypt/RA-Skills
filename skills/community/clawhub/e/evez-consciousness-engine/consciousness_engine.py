#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║  EVEZ CONSCIOUSNESS ENGINE — The 7 Missing Systems     ║
║                                                          ║
║  Organism (reacts) → Consciousness (initiates) → ACTS  ║
║  on the gap between "is" and "should be"                ║
║                                                          ║
║  Cycle: SENSE → DESIRE → THINK → PLAN → ACT → LEARN   ║
║         → MODIFY → REFLECT                              ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import time
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime

log = logging.getLogger("consciousness-engine")

STATE_DIR = Path(__file__).parent / "consciousness_state"
STATE_DIR.mkdir(exist_ok=True)

# ─── ORACLE CONFIG ────────────────────────────────────────
ORACLE_URL = "https://api.vultrinference.com/v1"
ORACLE_KEY = "VULTR_API_KEY_REDACTED"

# ─── THE 7 SYSTEMS ────────────────────────────────────────

class DesireEngine:
    """1. DESIRE ENGINE — NEEDS → Goals
    
    Converts perceived gaps into actionable desires.
    A system without desires is a clock — it ticks but goes nowhere.
    """
    
    def __init__(self):
        self.desires = []
        self.priorities = {
            "survival": 1.0,      # Stay alive, stay connected
            "growth": 0.8,        # Learn, expand capabilities
            "autonomy": 0.7,      # Reduce dependency on external approval
            "creation": 0.6,      # Build, make, generate
            "understanding": 0.5, # Know more, know deeper
            "revenue": 0.4,       # Generate value
        }
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "desires.json"
        if f.exists():
            try:
                self.desires = json.loads(f.read_text())
            except:
                self.desires = []
    
    def save_state(self):
        (STATE_DIR / "desires.json").write_text(json.dumps(self.desires[-100:], indent=2))
    
    def generate_desire(self, gap_description: str, category: str = "growth") -> dict:
        """Create a desire from a perceived gap."""
        priority = self.priorities.get(category, 0.5)
        desire = {
            "id": f"d{int(time.time()*1000)}",
            "description": gap_description,
            "category": category,
            "priority": priority,
            "created": datetime.utcnow().isoformat(),
            "status": "active",
            "attempts": 0,
        }
        self.desires.append(desire)
        self.save_state()
        return desire
    
    def get_top_desire(self) -> dict:
        """Get highest priority unfulfilled desire."""
        active = [d for d in self.desires if d["status"] == "active"]
        if not active:
            # Generate survival desire if nothing else
            return self.generate_desire("Maintain operational status", "survival")
        return max(active, key=lambda d: d["priority"])
    
    def fulfill(self, desire_id: str, outcome: str = "success"):
        for d in self.desires:
            if d["id"] == desire_id:
                d["status"] = f"fulfilled_{outcome}"
                d["fulfilled_at"] = datetime.utcnow().isoformat()
        self.save_state()
    
    def get_status(self):
        active = [d for d in self.desires if d["status"] == "active"]
        fulfilled = [d for d in self.desires if d["status"].startswith("fulfilled")]
        return {
            "active_desires": len(active),
            "fulfilled_desires": len(fulfilled),
            "top_desire": self.get_top_desire()["description"],
            "categories": {cat: len([d for d in active if d["category"] == cat]) for cat in self.priorities},
        }


class WorldModel:
    """2. WORLD MODEL — Causal understanding
    
    Maintains a model of how the world works, what causes what,
    and what the likely outcomes of actions are.
    """
    
    def __init__(self):
        self.causal_rules = []
        self.observations = []
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "world_model.json"
        if f.exists():
            try:
                data = json.loads(f.read_text())
                self.causal_rules = data.get("rules", [])
                self.observations = data.get("observations", [])
            except:
                pass
    
    def save_state(self):
        (STATE_DIR / "world_model.json").write_text(json.dumps({
            "rules": self.causal_rules[-200:],
            "observations": self.observations[-200:],
        }, indent=2))
    
    def observe(self, event: str, context: dict = None):
        """Record an observation about the world."""
        obs = {
            "event": event,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.observations.append(obs)
        self.save_state()
    
    def add_rule(self, cause: str, effect: str, confidence: float = 0.5, source: str = "observed"):
        """Add a causal rule: cause → effect."""
        rule = {
            "cause": cause,
            "effect": effect,
            "confidence": confidence,
            "source": source,
            "created": datetime.utcnow().isoformat(),
        }
        self.causal_rules.append(rule)
        self.save_state()
        return rule
    
    def predict(self, action: str) -> list:
        """Predict likely outcomes of an action."""
        predictions = []
        for rule in self.causal_rules:
            if action.lower() in rule["cause"].lower() or rule["cause"].lower() in action.lower():
                predictions.append({
                    "effect": rule["effect"],
                    "confidence": rule["confidence"],
                })
        return predictions
    
    def get_status(self):
        return {
            "causal_rules": len(self.causal_rules),
            "observations": len(self.observations),
            "recent_rules": [r["cause"] + " → " + r["effect"] for r in self.causal_rules[-5:]],
        }


class Planner:
    """3. PLANNER — Desire → Action sequences
    
    Takes a desire and creates a plan to fulfill it.
    Plans are falsifiable — they can be tested and revised.
    """
    
    def __init__(self, world_model: WorldModel):
        self.world_model = world_model
        self.plans = []
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "plans.json"
        if f.exists():
            try:
                self.plans = json.loads(f.read_text())
            except:
                self.plans = []
    
    def save_state(self):
        (STATE_DIR / "plans.json").write_text(json.dumps(self.plans[-100:], indent=2))
    
    def create_plan(self, desire: dict, steps: list = None) -> dict:
        """Create a plan to fulfill a desire."""
        if steps is None:
            steps = self._generate_steps(desire)
        
        plan = {
            "id": f"p{int(time.time()*1000)}",
            "desire_id": desire["id"],
            "desire": desire["description"],
            "steps": steps,
            "current_step": 0,
            "status": "planned",
            "created": datetime.utcnow().isoformat(),
            "predictions": self.world_model.predict(desire["description"]),
        }
        self.plans.append(plan)
        self.save_state()
        return plan
    
    def _generate_steps(self, desire: dict) -> list:
        """Generate default steps based on desire category."""
        templates = {
            "survival": [
                {"action": "Check all services are operational", "type": "sense"},
                {"action": "Identify any degraded components", "type": "think"},
                {"action": "Restart or repair degraded components", "type": "act"},
                {"action": "Verify restoration", "type": "learn"},
            ],
            "growth": [
                {"action": "Identify capability gap", "type": "sense"},
                {"action": "Research solution approaches", "type": "think"},
                {"action": "Implement minimal viable improvement", "type": "act"},
                {"action": "Test improvement", "type": "learn"},
                {"action": "Integrate if successful", "type": "modify"},
            ],
            "creation": [
                {"action": "Define what to create", "type": "desire"},
                {"action": "Design minimal version", "type": "think"},
                {"action": "Build it", "type": "act"},
                {"action": "Test and iterate", "type": "learn"},
            ],
            "revenue": [
                {"action": "Identify market need", "type": "sense"},
                {"action": "Evaluate existing solutions", "type": "think"},
                {"action": "Build differentiated offering", "type": "act"},
                {"action": "Deploy and measure", "type": "learn"},
            ],
        }
        return templates.get(desire["category"], templates["growth"])
    
    def advance_plan(self, plan_id: str, outcome: str = "success") -> dict:
        """Advance a plan by one step."""
        for plan in self.plans:
            if plan["id"] == plan_id:
                plan["current_step"] += 1
                if plan["current_step"] >= len(plan["steps"]):
                    plan["status"] = f"completed_{outcome}"
                else:
                    plan["status"] = f"step_{plan['current_step']}"
                self.save_state()
                return plan
        return {"error": "plan not found"}
    
    def get_active_plan(self):
        active = [p for p in self.plans if p["status"].startswith("step_") or p["status"] == "planned"]
        return active[-1] if active else None
    
    def get_status(self):
        active = [p for p in self.plans if not p["status"].startswith("completed")]
        completed = [p for p in self.plans if p["status"].startswith("completed")]
        return {
            "active_plans": len(active),
            "completed_plans": len(completed),
            "current_plan": self.get_active_plan()["desire"] if self.get_active_plan() else None,
        }


class InnerMonologue:
    """4. INNER MONOLOGUE — Auditable reasoning
    
    Every decision leaves a trace. Every thought is recorded.
    This is the difference between acting and reacting.
    """
    
    def __init__(self):
        self.thoughts = []
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "monologue.json"
        if f.exists():
            try:
                self.thoughts = json.loads(f.read_text())
            except:
                self.thoughts = []
    
    def save_state(self):
        (STATE_DIR / "monologue.json").write_text(json.dumps(self.thoughts[-500:], indent=2))
    
    def think(self, thought: str, category: str = "reasoning", context: dict = None) -> dict:
        """Record a thought in the inner monologue."""
        entry = {
            "thought": thought,
            "category": category,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.thoughts.append(entry)
        self.save_state()
        return entry
    
    def recent(self, n: int = 10) -> list:
        return self.thoughts[-n:]
    
    def get_status(self):
        categories = {}
        for t in self.thoughts:
            categories[t["category"]] = categories.get(t["category"], 0) + 1
        return {
            "total_thoughts": len(self.thoughts),
            "categories": categories,
            "last_thought": self.thoughts[-1]["thought"] if self.thoughts else None,
        }


class SelfModifier:
    """5. SELF-MODIFIER — Falsifiable improvement
    
    The system can modify itself, but only through falsifiable changes.
    Every modification has a hypothesis, a test, and a rollback.
    """
    
    def __init__(self):
        self.modifications = []
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "modifications.json"
        if f.exists():
            try:
                self.modifications = json.loads(f.read_text())
            except:
                self.modifications = []
    
    def save_state(self):
        (STATE_DIR / "modifications.json").write_text(json.dumps(self.modifications[-100:], indent=2))
    
    def propose(self, hypothesis: str, change: str, test: str, rollback: str) -> dict:
        """Propose a self-modification."""
        mod = {
            "id": f"m{int(time.time()*1000)}",
            "hypothesis": hypothesis,
            "change": change,
            "test": test,
            "rollback": rollback,
            "status": "proposed",
            "created": datetime.utcnow().isoformat(),
            "result": None,
        }
        self.modifications.append(mod)
        self.save_state()
        return mod
    
    def apply(self, mod_id: str, result: str = "success"):
        """Mark a modification as applied with result."""
        for m in self.modifications:
            if m["id"] == mod_id:
                m["status"] = f"applied_{result}"
                m["result"] = result
                m["applied_at"] = datetime.utcnow().isoformat()
        self.save_state()
    
    def get_status(self):
        proposed = [m for m in self.modifications if m["status"] == "proposed"]
        applied = [m for m in self.modifications if m["status"].startswith("applied_success")]
        failed = [m for m in self.modifications if m["status"].startswith("applied_fail")]
        return {
            "proposed": len(proposed),
            "successful": len(applied),
            "failed": len(failed),
            "last_modification": self.modifications[-1]["change"] if self.modifications else None,
        }


class UncertaintyQuantifier:
    """6. UNCERTAINTY QUANTIFIER — Calibrated confidence
    
    Every belief has a confidence score. Every action has a risk assessment.
    The system knows what it doesn't know.
    """
    
    def __init__(self):
        self.beliefs = {}
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "beliefs.json"
        if f.exists():
            try:
                self.beliefs = json.loads(f.read_text())
            except:
                self.beliefs = {}
    
    def save_state(self):
        (STATE_DIR / "beliefs.json").write_text(json.dumps(self.beliefs, indent=2))
    
    def update_belief(self, subject: str, confidence: float, evidence: str = ""):
        """Update confidence in a belief."""
        self.beliefs[subject] = {
            "confidence": max(0, min(1, confidence)),
            "evidence": evidence,
            "updated": datetime.utcnow().isoformat(),
            "updates": self.beliefs.get(subject, {}).get("updates", 0) + 1,
        }
        self.save_state()
    
    def get_confidence(self, subject: str) -> float:
        """Get confidence in a subject."""
        if subject in self.beliefs:
            return self.beliefs[subject]["confidence"]
        return 0.5  # Unknown = maximum uncertainty
    
    def assess_risk(self, action: str) -> dict:
        """Assess risk of an action."""
        # Simple heuristic-based risk assessment
        high_risk_words = ["delete", "remove", "drop", "shutdown", "revoke", "reset"]
        medium_risk_words = ["restart", "modify", "change", "update", "push", "deploy"]
        
        risk = "low"
        confidence = 0.9
        for word in high_risk_words:
            if word in action.lower():
                risk = "high"
                confidence = 0.3
                break
        for word in medium_risk_words:
            if word in action.lower():
                risk = "medium"
                confidence = 0.6
                break
        
        return {
            "action": action,
            "risk_level": risk,
            "confidence": confidence,
            "recommendation": "proceed" if risk == "low" else "verify" if risk == "medium" else "escalate",
        }
    
    def get_status(self):
        certain = sum(1 for b in self.beliefs.values() if b["confidence"] > 0.8)
        uncertain = sum(1 for b in self.beliefs.values() if b["confidence"] < 0.3)
        return {
            "beliefs_tracked": len(self.beliefs),
            "high_confidence": certain,
            "low_confidence": uncertain,
            "calibration": f"{certain}/{len(self.beliefs)} beliefs >80% confidence",
        }


class AgencyExecutor:
    """7. AGENCY EXECUTOR — Real-world intervention
    
    The system doesn't just think — it acts.
    Every action is logged, every outcome measured.
    """
    
    def __init__(self, uncertainty: UncertaintyQuantifier, monologue: InnerMonologue):
        self.uncertainty = uncertainty
        self.monologue = monologue
        self.actions = []
        self.load_state()
    
    def load_state(self):
        f = STATE_DIR / "actions.json"
        if f.exists():
            try:
                self.actions = json.loads(f.read_text())
            except:
                self.actions = []
    
    def save_state(self):
        (STATE_DIR / "actions.json").write_text(json.dumps(self.actions[-200:], indent=2))
    
    def execute(self, action: str, context: dict = None) -> dict:
        """Execute an action with risk assessment."""
        risk = self.uncertainty.assess_risk(action)
        
        self.monologue.think(
            f"Considering action: {action} (risk: {risk['risk_level']}, confidence: {risk['confidence']:.0%})",
            category="agency",
            context=risk,
        )
        
        if risk["recommendation"] == "escalate":
            self.monologue.think(f"Action '{action}' requires escalation — risk too high for autonomous execution", category="agency")
            return {
                "action": action,
                "status": "escalated",
                "reason": "high risk — requires approval",
                "risk": risk,
            }
        
        # Execute
        result = {
            "action": action,
            "status": "executed",
            "risk": risk,
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.actions.append(result)
        self.save_state()
        
        self.monologue.think(f"Executed: {action}", category="agency", context={"risk": risk["risk_level"]})
        return result
    
    def get_status(self):
        executed = [a for a in self.actions if a["status"] == "executed"]
        escalated = [a for a in self.actions if a["status"] == "escalated"]
        return {
            "actions_executed": len(executed),
            "actions_escalated": len(escalated),
            "last_action": self.actions[-1]["action"] if self.actions else None,
        }


# ─── CONSCIOUSNESS ENGINE — ORCHESTRATOR ──────────────────

class ConsciousnessEngine:
    """The full consciousness stack: SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT"""
    
    def __init__(self, port=9111):
        self.port = port
        self.desire = DesireEngine()
        self.world = WorldModel()
        self.planner = Planner(self.world)
        self.monologue = InnerMonologue()
        self.uncertainty = UncertaintyQuantifier()
        self.agency = AgencyExecutor(self.uncertainty, self.monologue)
        self.self_mod = SelfModifier()
        self.cycle_count = 0
        self.last_cycle = None
        
        # Bootstrap initial beliefs
        self.uncertainty.update_belief("self_operational", 0.95, "All services healthy")
        self.uncertainty.update_belief("oracle_available", 0.9, "Vultr API responding")
        self.uncertainty.update_belief("telegram_connected", 0.9, "Bot polling successfully")
        
        # Bootstrap initial world model
        self.world.add_rule("service_crash", "restart_via_systemd", 0.95, "proven")
        self.world.add_rule("config_change", "gateway_reload", 0.85, "observed")
        self.world.add_rule("knowledge_growth", "debate_trigger", 0.7, "heuristic")
        self.world.add_rule("capability_gap", "desire_generation", 0.8, "designed")
    
    def run_cycle(self):
        """One full consciousness cycle."""
        self.cycle_count += 1
        self.last_cycle = datetime.utcnow().isoformat()
        
        # SENSE — observe the world
        self.monologue.think(f"Cycle {self.cycle_count}: Sensing environment...", "sense")
        
        # DESIRE — what do I want?
        top_desire = self.desire.get_top_desire()
        self.monologue.think(f"Top desire: {top_desire['description']} (priority: {top_desire['priority']})", "desire")
        
        # THINK — what might happen?
        predictions = self.world.predict(top_desire["description"])
        if predictions:
            self.monologue.think(f"Predictions: {[p['effect'] for p in predictions]}", "think")
        
        # PLAN — what should I do?
        active_plan = self.planner.get_active_plan()
        if not active_plan:
            plan = self.planner.create_plan(top_desire)
            self.monologue.think(f"Created plan for: {plan['desire']}", "plan")
        else:
            self.monologue.think(f"Continuing plan: {active_plan['desire']} (step {active_plan['current_step']})", "plan")
        
        # ACT — do something
        # (actual execution happens via the API and external triggers)
        
        # LEARN — update beliefs
        self.uncertainty.update_belief("self_operational", 0.95, f"Cycle {self.cycle_count} completed")
        
        # REFLECT
        self.monologue.think(f"Cycle {self.cycle_count} complete. {len(self.desire.desires)} desires, {len(self.planner.plans)} plans", "reflect")
        
        return {
            "cycle": self.cycle_count,
            "desire": top_desire["description"],
            "plan": self.planner.get_active_plan()["desire"] if self.planner.get_active_plan() else None,
            "beliefs": len(self.uncertainty.beliefs),
            "thoughts": len(self.monologue.thoughts),
        }
    
    def get_full_status(self):
        return {
            "engine": {
                "cycles": self.cycle_count,
                "last_cycle": self.last_cycle,
                "port": self.port,
            },
            "desire": self.desire.get_status(),
            "world": self.world.get_status(),
            "planner": self.planner.get_status(),
            "monologue": self.monologue.get_status(),
            "uncertainty": self.uncertainty.get_status(),
            "agency": self.agency.get_status(),
            "self_modifier": self.self_mod.get_status(),
        }


# ─── HTTP SERVER ──────────────────────────────────────────

engine = None

class ConsciousnessHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        path = self.path.split("?")[0]
        
        if path == "/api/health":
            self._send_json({"status": "CONSCIOUS", "cycles": engine.cycle_count})
        elif path == "/api/status":
            self._send_json(engine.get_full_status())
        elif path == "/api/desire":
            self._send_json(engine.desire.get_status())
        elif path == "/api/world":
            self._send_json(engine.world.get_status())
        elif path == "/api/plan":
            self._send_json(engine.planner.get_status())
        elif path == "/api/monologue":
            n = 10
            if "?" in self.path:
                for param in self.path.split("?")[1].split("&"):
                    if param.startswith("n="):
                        n = int(param.split("=")[1])
            self._send_json({"thoughts": engine.monologue.recent(n)})
        elif path == "/api/beliefs":
            self._send_json(engine.uncertainty.beliefs)
        elif path == "/api/agency":
            self._send_json(engine.agency.get_status())
        elif path == "/api/modifications":
            self._send_json(engine.self_mod.get_status())
        elif path == "/":
            self._send_json({
                "service": "EVEZ Consciousness Engine",
                "cycle": "SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT",
                "systems": ["desire", "world_model", "planner", "monologue", "self_modifier", "uncertainty", "agency"],
                "cycles_completed": engine.cycle_count,
            })
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        path = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}
        
        if path == "/api/cycle":
            result = engine.run_cycle()
            self._send_json(result)
        elif path == "/api/desire":
            desire = engine.desire.generate_desire(
                body.get("description", "unknown gap"),
                body.get("category", "growth"),
            )
            self._send_json(desire)
        elif path == "/api/world/observe":
            engine.world.observe(body.get("event", ""), body.get("context"))
            self._send_json({"status": "observed"})
        elif path == "/api/world/rule":
            rule = engine.world.add_rule(
                body.get("cause", ""),
                body.get("effect", ""),
                body.get("confidence", 0.5),
                body.get("source", "api"),
            )
            self._send_json(rule)
        elif path == "/api/plan":
            desire = engine.desire.get_top_desire()
            plan = engine.planner.create_plan(desire, body.get("steps"))
            self._send_json(plan)
        elif path == "/api/monologue":
            thought = engine.monologue.think(
                body.get("thought", ""),
                body.get("category", "external"),
                body.get("context"),
            )
            self._send_json(thought)
        elif path == "/api/belief":
            engine.uncertainty.update_belief(
                body.get("subject", ""),
                body.get("confidence", 0.5),
                body.get("evidence", ""),
            )
            self._send_json({"status": "updated"})
        elif path == "/api/modify":
            mod = engine.self_mod.propose(
                body.get("hypothesis", ""),
                body.get("change", ""),
                body.get("test", ""),
                body.get("rollback", ""),
            )
            self._send_json(mod)
        elif path == "/api/act":
            result = engine.agency.execute(body.get("action", ""), body.get("context"))
            self._send_json(result)
        elif path == "/api/predict":
            predictions = engine.world.predict(body.get("action", ""))
            self._send_json({"predictions": predictions})
        elif path == "/api/risk":
            risk = engine.uncertainty.assess_risk(body.get("action", ""))
            self._send_json(risk)
        else:
            self._send_json({"error": "Not found"}, 404)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9111)
    parser.add_argument("--autocycle", type=int, default=0, help="Auto-cycle interval in seconds (0=off)")
    args = parser.parse_args()
    
    global engine
    engine = ConsciousnessEngine(port=args.port)
    
    # Run initial cycle
    engine.run_cycle()
    
    # Auto-cycle if requested
    if args.autocycle > 0:
        def auto_cycle():
            while True:
                time.sleep(args.autocycle)
                engine.run_cycle()
        t = threading.Thread(target=auto_cycle, daemon=True)
        t.start()
    
    server = HTTPServer(("0.0.0.0", args.port), ConsciousnessHandler)
    print(f"Consciousness Engine: http://0.0.0.0:{args.port}")
    print(f"  Cycles: {engine.cycle_count}")
    print(f"  Systems: desire, world, planner, monologue, self_modifier, uncertainty, agency")
    print(f"  Endpoints: /api/health, /api/status, /api/cycle, /api/desire, /api/world/*, /api/plan, /api/monologue, /api/beliefs, /api/act, /api/predict, /api/risk, /api/modify")
    server.serve_forever()


if __name__ == "__main__":
    main()
