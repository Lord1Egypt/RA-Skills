# RQNS Orchestrator — The ACT layer
# SENSE → DESIRE → THINK → PLAN → ACT, all wired through the event spine

from rqns.core.interfaces import RQNSPipeline, AnomalySignal, EventSpine
from rqns.modules.sensor_agent import ConcreteSensorAgent
from rqns.modules.rqns_agent import ContextualBanditAgent
from rqns.modules.patch_pipeline import ConcretePatchPipeline
import numpy as np

class ConcreteRQNSPipeline(RQNSPipeline):
    """
    The full RQNS pipeline: Sensor → Agent → (Solver) → Patch → Spine
    Every step is logged to the append-only event spine.
    """
    
    def __init__(self):
        self.sensor = ConcreteSensorAgent()
        self.agent = ContextualBanditAgent()
        self.patcher = ConcretePatchPipeline(self.agent)
        self.spine = EventSpine()
        self.tick = 0
        
        # Stats
        self.total_signals = 0
        self.total_anomalies = 0
        self.total_quantum_routes = 0
        self.total_local_routes = 0
    
    def process_signal(self, signal: AnomalySignal) -> dict:
        self.tick += 1
        self.total_signals += 1
        
        # SENSE: Neuromorphic spike encoding
        detection = self.sensor.process_signal(signal)
        self.spine.append("sensor", "detection", {
            "signal_id": detection.signal_id,
            "complexity": detection.complexity,
            "confidence": detection.confidence,
            "is_anomaly": detection.is_anomaly,
            "spike_count": detection.features.get("spike_count", 0)
        })
        
        if detection.is_anomaly:
            self.total_anomalies += 1
        
        # DESIRE → THINK → PLAN: Agent allocation decision
        job, decision = self.agent.analyze_anomaly(detection)
        self.spine.append("agent", "allocation", {
            "job_id": job.job_id,
            "backend": decision.backend.value,
            "route_to_t3": decision.route_to_t3,
            "estimated_latency": decision.estimated_latency
        })
        
        # ACT: Route to backend
        if decision.route_to_t3:
            self.total_quantum_routes += 1
            # Mock solver result (real D-Wave integration requires dwave-system)
            from rqns.core.interfaces import QuantumResult
            result = QuantumResult(
                job_id=job.job_id,
                success=True,
                backend=decision.backend.value,
                solution_energy=-detection.complexity * 1.8,
                latency_ms=decision.estimated_latency * 1000
            )
            patch_log = self.patcher.process_solver_result(result)
            self.spine.append("solver", "result", {
                "backend": result.backend,
                "energy": result.solution_energy,
                "latency_ms": result.latency_ms,
                "success": result.success,
                "cumulative_learning": patch_log.cumulative_learning
            })
            energy = result.solution_energy
            latency = result.latency_ms
        else:
            self.total_local_routes += 1
            energy = 0.0
            latency = decision.estimated_latency
        
        # LEARN: Log the cycle
        self.spine.append("orchestrator", "cycle_complete", {
            "tick": self.tick,
            "complexity": detection.complexity,
            "backend": decision.backend.value,
            "energy": energy,
            "latency": latency
        })
        
        return {
            "signal_id": signal.source_id if hasattr(signal, 'source_id') else str(self.tick),
            "tick": self.tick,
            "complexity": detection.complexity,
            "confidence": detection.confidence,
            "is_anomaly": detection.is_anomaly,
            "spike_count": detection.features.get("spike_count", 0),
            "backend": decision.backend.value,
            "latency": latency,
            "energy": energy,
            "learning": self.patcher.cumulative_learning,
            "total_anomalies": self.total_anomalies,
            "total_quantum_routes": self.total_quantum_routes,
            "spine_length": len(self.spine.events)
        }
    
    def status(self) -> dict:
        return {
            "tick": self.tick,
            "total_signals": self.total_signals,
            "total_anomalies": self.total_anomalies,
            "total_quantum_routes": self.total_quantum_routes,
            "total_local_routes": self.total_local_routes,
            "cumulative_learning": self.patcher.cumulative_learning,
            "spine_events": len(self.spine.events),
            "agent_thresholds": {k.value: v for k, v in self.agent.delegation_thresholds.items()},
            "sensor_total_spikes": self.sensor.total_spikes
        }
