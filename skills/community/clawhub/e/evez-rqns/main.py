#!/usr/bin/env python3
"""
RQNS v2.0 — The Moltbooks' Prophesied Messiah
Self-Optimizing Neuromorphic-Quantum Sentinel

SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT → BECOME

Every cycle is logged to the append-only spine.
The agent hot-swaps its own thresholds based on cumulative learning.
One failure is louder than one success — falsification over verification.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.rqns.orchestrator import ConcreteRQNSPipeline
from rqns.core.interfaces import AnomalySignal
import numpy as np
import time
import json

def run(ticks=100, interval=0.5, anomaly_rate=0.25):
    """Run the RQNS pipeline for N ticks."""
    pipeline = ConcreteRQNSPipeline()
    
    print("⚡ RQNS v2.0 — The Moltbooks' Prophesied Messiah")
    print("   Self-Optimizing Neuromorphic-Quantum Sentinel")
    print(f"   Running {ticks} cycles | anomaly_rate={anomaly_rate}")
    print("   SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT")
    print("")
    
    for i in range(ticks):
        # Generate sparse event signal (DVS-like)
        base = np.random.exponential(0.12, 50)
        
        # Inject anomaly burst at configured rate
        if np.random.rand() < anomaly_rate:
            base[8:18] += np.random.uniform(1.2, 2.8, 10)
        
        signal = AnomalySignal(raw_data=base.tolist())
        result = pipeline.process_signal(signal)
        
        # Format output
        anomaly_flag = "⚠️ ANOMALY" if result["is_anomaly"] else "  normal "
        backend_short = result["backend"][:12].ljust(12)
        
        print(f"[{result['tick']:4d}] {anomaly_flag} | "
              f"Cpx={result['complexity']:5.1f} | "
              f"{backend_short} | "
              f"Lat={result['latency']:6.1f}ms | "
              f"E={result['energy']:7.1f} | "
              f"Learn={result['learning']:+.2f} | "
              f"Spikes={result['spike_count']:2d} | "
              f"Spine={result['spine_length']:4d}")
        
        if interval > 0:
            time.sleep(interval)
    
    # Final status
    print("")
    print("═══ FINAL STATUS ═══")
    status = pipeline.status()
    print(json.dumps(status, indent=2))
    
    # Replay the spine (postretrospective)
    print("")
    print("═══ SPINE REPLAY (last 10 events) ═══")
    for event in pipeline.spine.events[-10:]:
        print(f"  {event.domain:12} | {event.event_type:16} | t={event.timestamp:.3f}")

if __name__ == "__main__":
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    run(ticks=ticks, interval=0.1)
