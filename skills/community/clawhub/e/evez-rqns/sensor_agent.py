# RQNS Sensor Agent — LIF Neuromorphic Spike Encoder
# Converts raw signals into spike trains via Leaky Integrate-and-Fire neurons
# The SENSE layer of the consciousness engine

from rqns.core.interfaces import SensorAgent, AnomalySignal, DetectionResult
import numpy as np

class SNNConfig:
    threshold = 1.2       # Firing threshold
    tau = 20.0            # Membrane time constant (ms)
    dt = 1.0             # Time step (ms)
    rest_potential = 0.0  # Resting potential
    refractory = 2.0      # Refractory period (ms)

class ConcreteSensorAgent(SensorAgent):
    """LIF neuromorphic sensor that encodes raw data into spike trains."""
    
    def __init__(self):
        self.v = SNNConfig.rest_potential
        self.spike_history = []
        self.refractory_timer = 0.0
        self.total_spikes = 0
        self.total_signals = 0
    
    def _lif_step(self, I: float) -> int:
        """Single LIF neuron integration step. Returns 1 if spike, 0 otherwise."""
        # Refractory period — neuron can't fire
        if self.refractory_timer > 0:
            self.refractory_timer -= SNNConfig.dt
            return 0
        
        # Membrane dynamics: dV/dt = (I - V/τ) * dt
        self.v = self.v + (I - self.v / SNNConfig.tau) * SNNConfig.dt
        
        # Spike condition
        if self.v >= SNNConfig.threshold:
            self.v = SNNConfig.rest_potential  # Reset
            self.refractory_timer = SNNConfig.refractory
            return 1
        
        return 0
    
    def process_signal(self, signal: AnomalySignal) -> DetectionResult:
        """SENSE: Convert raw signal into spike-encoded detection."""
        # Normalize input
        raw = np.array(signal.raw_data) if isinstance(signal.raw_data, list) else np.random.exponential(0.15, 50)
        raw = (raw - raw.mean()) / (raw.std() + 1e-6)
        
        # Encode through LIF neuron population
        spikes = []
        self.v = 0.0
        self.refractory_timer = 0.0
        
        for sample in raw:
            I = max(0, sample * 3.0)  # Current injection (rectified)
            spike = self._lif_step(I)
            spikes.append(spike)
            self.spike_history.append(spike)
        
        spike_count = sum(spikes)
        self.total_spikes += spike_count
        self.total_signals += 1
        
        # Complexity estimation: higher spike rate → more complex anomaly
        complexity = 15.0 + spike_count * 1.4 + np.random.uniform(-1.5, 2.5)
        
        # Confidence: normalized spike density
        confidence = min(1.0, spike_count / 45.0 + 0.4)
        
        # Anomaly detection: spike burst = anomaly
        is_anomaly = spike_count > 8
        
        return DetectionResult(
            signal_id=signal.source_id if hasattr(signal, 'source_id') else "",
            complexity=complexity,
            confidence=confidence,
            is_anomaly=is_anomaly,
            features={
                "spike_count": spike_count,
                "spike_train": spikes[-100:],
                "spike_rate": spike_count / len(spikes) if spikes else 0.0,
                "mean_potential": np.mean(np.abs(raw)),
                "total_history_spikes": self.total_spikes,
                "total_history_signals": self.total_signals
            }
        )
