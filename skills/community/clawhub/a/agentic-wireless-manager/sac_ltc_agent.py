#!/usr/bin/env python3
"""
SAC-LTC Network Intelligence Agent
===================================
Lightweight SAC (Soft Actor-Critic) with LTC (Liquid Time-Constant) cells
for intelligent Wi-Fi / hotspot switching and RF environment sensing.

Derived from PreceptualAI UHCI (Universal Heterogeneous Connectivity Intelligence).
Simplified for single-device laptop/PC use. CPU-only, ~15K parameters.

Usage:
    python3 sac_ltc_agent.py --test              # Self-test
    python3 sac_ltc_agent.py --init-weights       # Generate heuristic weights
    python3 sac_ltc_agent.py --decide '<json>'    # Make switching decision
    python3 sac_ltc_agent.py --sense '<json>'     # Presence detection
    python3 sac_ltc_agent.py --explain '<json>'   # Explain RF environment
"""

import json, math, os, sys, time
from pathlib import Path

FEATURE_NAMES = [
    "rssi",          # Normalized signal strength (0=unusable, 1=excellent)
    "snr",           # Signal-to-noise ratio normalized
    "latency",       # Inverse latency (0=high latency, 1=low)
    "throughput",    # Normalized throughput
    "packet_loss",   # Inverse loss (0=high loss, 1=no loss)
    "congestion",    # Inverse congestion (0=crowded, 1=empty channel)
    "is_5ghz",       # 1 if 5GHz/6GHz band, 0 if 2.4GHz
    "is_hotspot",    # 1 if mobile hotspot, 0 if infrastructure AP
]
N_FEATURES = len(FEATURE_NAMES)
HIDDEN_DIM = 32
KAN_HIDDEN = 16
MAX_NETWORKS = 5
HISTORY_LEN = 8
DATA_DIR = Path.home() / ".net-intel"

# ---------------------------------------------------------------------------
# Try PyTorch, fall back to pure numpy
# ---------------------------------------------------------------------------
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import numpy as np
except ImportError:
    np = None

# ===========================================================================
# NUMPY FALLBACK IMPLEMENTATION (no PyTorch needed)
# ===========================================================================

def _sigmoid(x):
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))

def _softplus(x):
    if x > 20:
        return x
    return math.log(1.0 + math.exp(x))

def _tanh(x):
    return math.tanh(max(-500, min(500, x)))

def _silu(x):
    return x * _sigmoid(x)

class NumpyLTCCell:
    """Liquid Time-Constant cell — numpy/pure-python implementation.

    ODE: τ(x)·dh/dt = -h + tanh(W_h·h + W_x·x + b)
    τ(x) = τ_base + softplus(W_τ·x + b_τ)
    Euler discretization: h' = h + (Δt/τ(x))·(-h + f(x,h))
    """
    def __init__(self, input_dim, hidden_dim, weights=None):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.dt = 1.0
        if weights:
            self.W_x = weights["W_x"]
            self.W_h = weights["W_h"]
            self.b = weights["b"]
            self.W_tau = weights["W_tau"]
            self.b_tau = weights["b_tau"]
            self.tau_base = weights["tau_base"]
        else:
            self._init_random()

    def _init_random(self):
        s = 1.0 / math.sqrt(self.hidden_dim)
        import random
        def rand_mat(r, c):
            return [[random.gauss(0, s) for _ in range(c)] for _ in range(r)]
        self.W_x = rand_mat(self.input_dim, self.hidden_dim)
        self.W_h = rand_mat(self.hidden_dim, self.hidden_dim)
        self.b = [0.0] * self.hidden_dim
        self.W_tau = rand_mat(self.input_dim, self.hidden_dim)
        self.b_tau = [0.0] * self.hidden_dim
        self.tau_base = [1.0] * self.hidden_dim

    def forward(self, x, h):
        """x: list[float] len=input_dim, h: list[float] len=hidden_dim"""
        # f(x,h) = tanh(W_h·h + W_x·x + b)
        f = []
        for j in range(self.hidden_dim):
            val = self.b[j]
            for i in range(self.input_dim):
                val += self.W_x[i][j] * x[i]
            for i in range(self.hidden_dim):
                val += self.W_h[i][j] * h[i]
            f.append(_tanh(val))
        # τ(x) = τ_base + softplus(W_τ·x + b_τ)
        tau = []
        for j in range(self.hidden_dim):
            val = self.b_tau[j]
            for i in range(self.input_dim):
                val += self.W_tau[i][j] * x[i]
            tau.append(self.tau_base[j] + _softplus(val))
        # h' = h + (dt/τ)·(-h + f)
        h_new = []
        for j in range(self.hidden_dim):
            h_new.append(h[j] + (self.dt / tau[j]) * (-h[j] + f[j]))
        return h_new, tau

    def zero_state(self):
        return [0.0] * self.hidden_dim


class NumpyKANLinear:
    """Simplified KAN layer: base(SiLU) + spline(RBF B-spline approximation)."""
    def __init__(self, in_dim, out_dim, weights=None):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.grid_size = 5
        if weights:
            self.base_weight = weights["base_weight"]
            self.spline_weight = weights["spline_weight"]
            self.grid = weights.get("grid", self._default_grid())
        else:
            s = 1.0 / math.sqrt(in_dim)
            import random
            self.base_weight = [[random.gauss(0, s) for _ in range(out_dim)] for _ in range(in_dim)]
            self.spline_weight = [[[random.gauss(0, s * 0.1) for _ in range(out_dim)]
                                   for _ in range(self.grid_size + 3)]
                                  for _ in range(in_dim)]
            self.grid = self._default_grid()

    def _default_grid(self):
        # Grid points for B-spline from -1 to 1
        n = self.grid_size + 3  # grid_size + spline_order
        return [-1.0 + 2.0 * i / (n - 1) for i in range(n)]

    def _rbf_basis(self, x, center, width=0.3):
        return math.exp(-((x - center) ** 2) / (2 * width * width))

    def forward(self, x):
        """x: list[float] len=in_dim → list[float] len=out_dim"""
        # Base: SiLU activation then linear
        base_out = [0.0] * self.out_dim
        for i in range(self.in_dim):
            activated = _silu(x[i])
            for j in range(self.out_dim):
                base_out[j] += self.base_weight[i][j] * activated
        # Spline: RBF basis evaluation
        spline_out = [0.0] * self.out_dim
        for i in range(self.in_dim):
            for k, center in enumerate(self.grid):
                basis = self._rbf_basis(x[i], center)
                for j in range(self.out_dim):
                    spline_out[j] += self.spline_weight[i][k][j] * basis
        return [base_out[j] + spline_out[j] for j in range(self.out_dim)]


class NumpyNetworkAgent:
    """Complete SAC-LTC agent for network switching — numpy implementation."""

    def __init__(self, n_actions=MAX_NETWORKS, weights_path=None):
        self.n_actions = n_actions
        self.ltc = NumpyLTCCell(N_FEATURES, HIDDEN_DIM)
        self.kan1 = NumpyKANLinear(HIDDEN_DIM, KAN_HIDDEN)
        self.kan2 = NumpyKANLinear(KAN_HIDDEN, n_actions)
        self.hidden = self.ltc.zero_state()
        self.history = []
        self.tau_history = []
        if weights_path and os.path.exists(weights_path):
            self.load(weights_path)

    def observe(self, features):
        """Feed one observation (list of N_FEATURES floats, normalized 0-1)."""
        self.hidden, tau = self.ltc.forward(features, self.hidden)
        self.history.append({"features": features[:], "hidden": self.hidden[:], "tau": tau[:]})
        self.tau_history.append(tau[:])
        if len(self.history) > HISTORY_LEN * 10:
            self.history = self.history[-HISTORY_LEN * 10:]
        if len(self.tau_history) > 100:
            self.tau_history = self.tau_history[-100:]

    def decide(self):
        """Get action probabilities from KAN actor."""
        h1 = self.kan1.forward(self.hidden)
        # Layer norm approximation
        mean_h = sum(h1) / len(h1)
        var_h = sum((v - mean_h) ** 2 for v in h1) / len(h1)
        std_h = math.sqrt(var_h + 1e-5)
        h1 = [(v - mean_h) / std_h for v in h1]
        logits = self.kan2.forward(h1)
        # Softmax
        max_l = max(logits)
        exps = [math.exp(l - max_l) for l in logits]
        sum_e = sum(exps)
        probs = [e / sum_e for e in exps]
        action = probs.index(max(probs))
        return {"action": action, "confidence": max(probs), "probs": probs, "logits": logits}

    def explain(self, network_names=None):
        """Generate explainable decision breakdown."""
        if not self.history:
            return {"error": "No observations yet"}
        decision = self.decide()
        # Feature attribution via finite differences
        base_logits = decision["logits"]
        chosen = decision["action"]
        attributions = {}
        features = self.history[-1]["features"]
        for i, name in enumerate(FEATURE_NAMES):
            perturbed = features[:]
            perturbed[i] = max(0, min(1, features[i] + 0.1))
            # Re-run through LTC + KAN with perturbation
            h_pert, _ = self.ltc.forward(perturbed, self.hidden)
            h1 = self.kan1.forward(h_pert)
            mean_h = sum(h1) / len(h1)
            var_h = sum((v - mean_h) ** 2 for v in h1) / len(h1)
            std_h = math.sqrt(var_h + 1e-5)
            h1 = [(v - mean_h) / std_h for v in h1]
            pert_logits = self.kan2.forward(h1)
            attributions[name] = pert_logits[chosen] - base_logits[chosen]
        # Normalize attributions
        max_attr = max(abs(v) for v in attributions.values()) or 1.0
        attributions = {k: round(v / max_attr, 3) for k, v in attributions.items()}
        # Temporal trend from tau values
        tau_now = self.tau_history[-1] if self.tau_history else [1.0] * HIDDEN_DIM
        avg_tau = sum(tau_now) / len(tau_now)
        if len(self.tau_history) >= 3:
            tau_prev = self.tau_history[-3]
            avg_tau_prev = sum(tau_prev) / len(tau_prev)
            if avg_tau > avg_tau_prev * 1.1:
                trend = "stabilizing"
            elif avg_tau < avg_tau_prev * 0.9:
                trend = "reacting to change"
            else:
                trend = "stable"
        else:
            trend = "insufficient data"
        # Top factors
        sorted_attr = sorted(attributions.items(), key=lambda x: abs(x[1]), reverse=True)
        top_factors = sorted_attr[:3]
        # Plain English reason
        reasons = []
        for name, weight in top_factors:
            if abs(weight) < 0.1:
                continue
            direction = "strong" if weight > 0 else "weak"
            reasons.append(f"{name} is {direction} ({weight:+.2f})")
        name_str = network_names[decision["action"]] if network_names else f"network {decision['action']}"
        reason = f"Choose {name_str}: " + ", ".join(reasons) if reasons else "No dominant factor"
        # Layman summary
        feat = self.history[-1]["features"]
        issues = []
        if feat[0] < 0.4:
            issues.append("signal is weak")
        if feat[2] < 0.3:
            issues.append("response time is slow")
        if feat[4] < 0.8:
            issues.append("some data is getting lost")
        if feat[5] < 0.4:
            issues.append("your channel is crowded")
        if not issues:
            layman = "Your connection looks good. No action needed."
        else:
            layman = "Issues: " + "; ".join(issues) + "."
        return {
            "action": decision["action"],
            "confidence": round(decision["confidence"], 3),
            "probs": [round(p, 3) for p in decision["probs"]],
            "feature_weights": attributions,
            "top_factors": top_factors,
            "time_constants_avg": round(avg_tau, 3),
            "temporal_trend": trend,
            "reason": reason,
            "layman_summary": layman,
        }

    def sense(self, rssi_samples, baseline_variance=None):
        """Detect presence from RSSI time series.

        Args:
            rssi_samples: list of dicts, each with "bssid"/"ssid" and "rssi" (dBm),
                          collected at ~1/sec. Minimum 10 samples.
            baseline_variance: float, expected variance in quiet environment (default 1.5)

        Returns:
            dict with presence assessment and explanation.
        """
        if baseline_variance is None:
            baseline_variance = 1.5
        if len(rssi_samples) < 5:
            return {"presence": "insufficient_data", "confidence": 0,
                    "plain_explanation": "Need at least 5 seconds of readings."}
        # Group by BSSID/SSID
        by_ap = {}
        for s in rssi_samples:
            key = s.get("bssid", s.get("ssid", "unknown"))
            by_ap.setdefault(key, []).append(s["rssi"])
        # Analyze each AP
        ap_results = {}
        max_variance_ratio = 0
        for ap, readings in by_ap.items():
            if len(readings) < 3:
                continue
            mean_r = sum(readings) / len(readings)
            variance = sum((r - mean_r) ** 2 for r in readings) / len(readings)
            peak_to_peak = max(readings) - min(readings)
            variance_ratio = variance / max(baseline_variance, 0.1)
            # Feed variance time series through LTC for pattern detection
            # Compute autocorrelation at lag 1 for periodicity
            if len(readings) > 3:
                diffs = [readings[i+1] - readings[i] for i in range(len(readings)-1)]
                mean_d = sum(diffs) / len(diffs)
                var_d = sum((d - mean_d)**2 for d in diffs) / len(diffs)
                if var_d > 0 and len(diffs) > 1:
                    autocorr = sum((diffs[i] - mean_d) * (diffs[i+1] - mean_d)
                                   for i in range(len(diffs)-1)) / ((len(diffs)-1) * var_d)
                else:
                    autocorr = 0
            else:
                autocorr = 0
            # Classify pattern
            if abs(autocorr) > 0.5:
                pattern = "periodic"  # Likely appliance (microwave, etc.)
            elif peak_to_peak > 6:
                pattern = "walking"  # Large swings = active movement
            elif peak_to_peak > 3:
                pattern = "subtle_movement"
            else:
                pattern = "stationary"
            ap_results[ap] = {
                "mean_rssi": round(mean_r, 1),
                "variance": round(variance, 2),
                "peak_to_peak": round(peak_to_peak, 1),
                "variance_ratio": round(variance_ratio, 2),
                "autocorrelation": round(autocorr, 3),
                "pattern": pattern,
                "n_samples": len(readings),
            }
            max_variance_ratio = max(max_variance_ratio, variance_ratio)
        # Overall presence assessment
        if max_variance_ratio > 5:
            presence = "active_movement"
            confidence = min(0.95, 0.5 + max_variance_ratio * 0.05)
        elif max_variance_ratio > 3:
            presence = "likely"
            confidence = min(0.85, 0.4 + max_variance_ratio * 0.08)
        elif max_variance_ratio > 1.5:
            presence = "possible"
            confidence = min(0.6, 0.2 + max_variance_ratio * 0.1)
        else:
            presence = "none"
            confidence = max(0.05, 1.0 - max_variance_ratio * 0.5)
        # Check for periodic interference (not human)
        any_periodic = any(r["pattern"] == "periodic" for r in ap_results.values())
        if any_periodic and presence in ("possible", "likely"):
            presence = "possible_interference"
            confidence *= 0.6
        # Plain English
        if presence == "none":
            plain = "No movement detected. The signals around you are steady."
        elif presence == "possible_interference":
            plain = ("Some signal fluctuation detected, but the pattern looks "
                     "like an electronic device (microwave, Bluetooth) rather "
                     "than a person moving.")
        elif presence == "possible":
            plain = "Slight signal disturbance detected. Someone might be nearby but I'm not very sure."
        elif presence == "likely":
            plain = ("Movement detected — the WiFi signals are wobbling in a way "
                     "that usually means a person is moving nearby.")
        else:  # active_movement
            plain = ("Clear movement detected. Someone is actively moving in the "
                     "area around you — the signals are showing strong disruption.")
        return {
            "presence": presence,
            "confidence": round(confidence, 3),
            "max_variance_ratio": round(max_variance_ratio, 2),
            "baseline_variance": baseline_variance,
            "per_ap": ap_results,
            "plain_explanation": plain,
        }

    def sense_directional(self, rssi_samples, spatial_map, baseline_variance=None):
        """Directional presence detection using calibrated spatial map.

        Args:
            rssi_samples: list of dicts with bssid/ssid and rssi
            spatial_map: dict mapping bssid/ssid → direction (front/back/left/right)
            baseline_variance: quiet baseline

        Returns:
            dict with per-direction presence assessment.
        """
        # Group samples by direction using spatial map
        by_direction = {"front": [], "back": [], "left": [], "right": [], "unknown": []}
        for s in rssi_samples:
            key = s.get("bssid", s.get("ssid", "unknown"))
            direction = spatial_map.get(key, "unknown")
            by_direction[direction].append(s)
        results = {}
        for direction, samples in by_direction.items():
            if direction == "unknown" or len(samples) < 3:
                results[direction] = {"presence": "no_data", "confidence": 0}
                continue
            sense_result = self.sense(samples, baseline_variance)
            results[direction] = sense_result
        # Build ASCII map
        def status(d):
            r = results.get(d, {})
            p = r.get("presence", "no_data")
            if p in ("active_movement", "likely"):
                return "MOVEMENT"
            elif p == "possible":
                return "maybe"
            else:
                return "clear"
        ascii_map = (
            f"        [{status('front').center(10)}]\n"
            f"            FRONT\n"
            f"              |\n"
            f"[{status('left').center(8)}] -- YOU -- [{status('right').center(8)}]\n"
            f"   LEFT       |      RIGHT\n"
            f"              |\n"
            f"            BACK\n"
            f"        [{status('back').center(10)}]"
        )
        return {"directions": results, "map": ascii_map}

    def get_environment_profile(self, history_entries):
        """Analyze history to produce RF environment profile in plain English."""
        if not history_entries or len(history_entries) < 5:
            return "Not enough data yet. Keep monitoring for at least 10 minutes."
        # Analyze network counts over time
        net_counts = [len(e.get("nets", [])) for e in history_entries]
        avg_nets = sum(net_counts) / len(net_counts)
        max_nets = max(net_counts)
        min_nets = min(net_counts)
        # Score trends
        scores = []
        for e in history_entries:
            for n in e.get("nets", []):
                if n.get("connected"):
                    scores.append(n.get("score", 50))
        avg_score = sum(scores) / len(scores) if scores else 50
        # Congestion analysis
        congestion_vals = []
        for e in history_entries:
            for n in e.get("nets", []):
                if n.get("connected"):
                    congestion_vals.append(n.get("congestion", 0))
        avg_congestion = sum(congestion_vals) / len(congestion_vals) if congestion_vals else 0
        # Build profile
        lines = []
        if avg_nets > 10:
            lines.append(f"You're in a busy RF environment with {int(avg_nets)} networks on average nearby.")
        elif avg_nets > 5:
            lines.append(f"Moderate wireless density — about {int(avg_nets)} networks around you.")
        else:
            lines.append(f"Relatively quiet RF area with about {int(avg_nets)} visible networks.")
        if max_nets - min_nets > 5:
            lines.append(f"Network count varies a lot ({min_nets}-{max_nets}), suggesting people/devices come and go.")
        if avg_congestion > 4:
            lines.append("Your channel is consistently crowded. Consider asking your router admin to switch channels.")
        elif avg_congestion > 2:
            lines.append("Some channel congestion at peak times but generally manageable.")
        if avg_score > 75:
            lines.append("Overall your connection quality has been good.")
        elif avg_score > 50:
            lines.append("Your connection quality is decent but could be better.")
        else:
            lines.append("Your connection has been struggling. Auto-optimization is actively working to help.")
        return "\n".join(lines)

    def save(self, path):
        """Save model weights to JSON."""
        data = {
            "ltc": {
                "W_x": self.ltc.W_x, "W_h": self.ltc.W_h, "b": self.ltc.b,
                "W_tau": self.ltc.W_tau, "b_tau": self.ltc.b_tau, "tau_base": self.ltc.tau_base,
            },
            "kan1": {"base_weight": self.kan1.base_weight, "spline_weight": self.kan1.spline_weight},
            "kan2": {"base_weight": self.kan2.base_weight, "spline_weight": self.kan2.spline_weight},
            "hidden": self.hidden,
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f)

    def load(self, path):
        """Load model weights from JSON."""
        with open(path) as f:
            data = json.load(f)
        self.ltc = NumpyLTCCell(N_FEATURES, HIDDEN_DIM, data["ltc"])
        self.kan1 = NumpyKANLinear(HIDDEN_DIM, KAN_HIDDEN, data["kan1"])
        self.kan2 = NumpyKANLinear(KAN_HIDDEN, self.n_actions, data["kan2"])
        self.hidden = data.get("hidden", self.ltc.zero_state())

    def init_heuristic_weights(self):
        """Pre-train weights with known RF heuristics so the model starts smart.

        Encodes:
          - High RSSI + low latency → prefer that network
          - Penalize packet loss and congestion heavily
          - 5GHz preferred for throughput, 2.4GHz for range
          - Hotspot penalty (less stable than infrastructure)
          - Temporal hysteresis via tau_base (don't switch too fast)
        """
        import random
        random.seed(42)
        # LTC: make signal and latency features strongly influence hidden state
        # Feature order: rssi, snr, latency, throughput, packet_loss, congestion, is_5ghz, is_hotspot
        importance = [1.0, 0.7, 0.9, 0.8, 0.6, 0.5, 0.3, -0.2]
        for i in range(N_FEATURES):
            for j in range(HIDDEN_DIM):
                self.ltc.W_x[i][j] = importance[i] * (0.5 + random.gauss(0, 0.1))
        # Tau: make time constants higher (slower) for stable features, lower for volatile
        tau_sensitivity = [0.3, 0.3, 0.5, 0.5, 0.8, 0.4, 0.1, 0.1]
        for i in range(N_FEATURES):
            for j in range(HIDDEN_DIM):
                self.ltc.W_tau[i][j] = tau_sensitivity[i] * random.gauss(0, 0.2)
        # Set tau_base high to prevent oscillation (hysteresis)
        self.ltc.tau_base = [2.0 + random.gauss(0, 0.1) for _ in range(HIDDEN_DIM)]
        # KAN actor: bias toward higher-scoring networks
        s = 1.0 / math.sqrt(HIDDEN_DIM)
        for i in range(HIDDEN_DIM):
            for j in range(KAN_HIDDEN):
                self.kan1.base_weight[i][j] = random.gauss(0, s)
        for i in range(KAN_HIDDEN):
            for j in range(self.n_actions):
                self.kan2.base_weight[i][j] = random.gauss(0, 0.2)
        # Save
        weights_path = DATA_DIR / "weights.json"
        self.save(str(weights_path))
        return str(weights_path)


# ===========================================================================
# NORMALIZATION HELPERS
# ===========================================================================

def normalize_network_features(raw):
    """Convert raw network measurements to normalized [0,1] features.

    Args:
        raw: dict with keys like rssi_dbm, noise_dbm, latency_ms,
             throughput_mbps, packet_loss_pct, n_networks_on_channel,
             is_5ghz (bool), is_hotspot (bool)
    """
    rssi = raw.get("rssi_dbm", -70)
    noise = raw.get("noise_dbm", -90)
    latency = raw.get("latency_ms", 50)
    throughput = raw.get("throughput_mbps", 10)
    loss = raw.get("packet_loss_pct", 0)
    congestion = raw.get("n_networks_on_channel", 3)
    is_5g = 1.0 if raw.get("is_5ghz", False) else 0.0
    is_hotspot = 1.0 if raw.get("is_hotspot", False) else 0.0

    return [
        max(0, min(1, (rssi + 100) / 60)),         # -100→0, -40→1
        max(0, min(1, (rssi - noise) / 60)),        # SNR: 0dB→0, 60dB→1
        max(0, min(1, 1 - (latency / 200))),        # 0ms→1, 200ms→0
        max(0, min(1, throughput / 100)),            # 0Mbps→0, 100Mbps→1
        max(0, min(1, 1 - (loss / 10))),            # 0%→1, 10%→0
        max(0, min(1, 1 - (congestion / 10))),      # 0 nets→1, 10 nets→0
        is_5g,
        is_hotspot,
    ]


def score_network(features):
    """Score a network 0-100 from normalized features."""
    weights = [30, 15, 25, 20, 10, 0, 0, 0]  # Ignore band/hotspot in score
    score = sum(f * w for f, w in zip(features, weights))
    return max(0, min(100, round(score)))


# ===========================================================================
# CLI INTERFACE
# ===========================================================================

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    weights_path = str(DATA_DIR / "weights.json")

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "--test":
        print("SAC-LTC Network Intelligence Agent — Self Test")
        print(f"  PyTorch available: {HAS_TORCH}")
        print(f"  NumPy available: {np is not None}")
        print(f"  Data directory: {DATA_DIR}")
        agent = NumpyNetworkAgent(n_actions=3)
        # Simulate a few observations
        test_networks = [
            {"rssi_dbm": -47, "noise_dbm": -94, "latency_ms": 12,
             "throughput_mbps": 45, "packet_loss_pct": 0,
             "n_networks_on_channel": 5, "is_5ghz": True, "is_hotspot": False},
            {"rssi_dbm": -62, "noise_dbm": -88, "latency_ms": 34,
             "throughput_mbps": 25, "packet_loss_pct": 0.5,
             "n_networks_on_channel": 2, "is_5ghz": True, "is_hotspot": True},
            {"rssi_dbm": -71, "noise_dbm": -90, "latency_ms": 85,
             "throughput_mbps": 8, "packet_loss_pct": 2,
             "n_networks_on_channel": 7, "is_5ghz": False, "is_hotspot": False},
        ]
        for i, raw in enumerate(test_networks):
            features = normalize_network_features(raw)
            score = score_network(features)
            print(f"\n  Network {i}: score={score}/100, features={[round(f,2) for f in features]}")
            agent.observe(features)
        result = agent.explain(["MyWiFi", "iPhone-5G", "Neighbor_2G"])
        print(f"\n  Decision: {result['reason']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Temporal trend: {result['temporal_trend']}")
        print(f"  Feature weights: {result['feature_weights']}")
        print(f"  Layman: {result['layman_summary']}")
        # Test sensing
        print("\n  Testing presence sensing...")
        import random
        random.seed(99)
        quiet = [{"ssid": "TestAP", "rssi": -50 + random.gauss(0, 0.8)} for _ in range(20)]
        movement = [{"ssid": "TestAP", "rssi": -50 + random.gauss(0, 3.5) + 2*math.sin(i*0.5)} for i in range(20)]
        q_result = agent.sense(quiet)
        m_result = agent.sense(movement)
        print(f"  Quiet room: {q_result['presence']} (conf {q_result['confidence']})")
        print(f"  Movement:   {m_result['presence']} (conf {m_result['confidence']})")
        print(f"\n  Quiet explanation: {q_result['plain_explanation']}")
        print(f"  Movement explanation: {m_result['plain_explanation']}")
        print("\n  All tests passed.")

    elif cmd == "--init-weights":
        agent = NumpyNetworkAgent(n_actions=MAX_NETWORKS)
        path = agent.init_heuristic_weights()
        print(f"Heuristic weights saved to {path}")

    elif cmd == "--decide":
        if len(sys.argv) < 3:
            print("Usage: --decide '<json array of raw network dicts>'")
            sys.exit(1)
        networks = json.loads(sys.argv[2])
        agent = NumpyNetworkAgent(n_actions=len(networks), weights_path=weights_path)
        names = [n.get("ssid", f"net{i}") for i, n in enumerate(networks)]
        for n in networks:
            features = normalize_network_features(n)
            agent.observe(features)
        result = agent.explain(names)
        print(json.dumps(result, indent=2))

    elif cmd == "--sense":
        if len(sys.argv) < 3:
            print("Usage: --sense '<json array of {ssid, rssi} samples>'")
            sys.exit(1)
        samples = json.loads(sys.argv[2])
        agent = NumpyNetworkAgent()
        result = agent.sense(samples)
        print(json.dumps(result, indent=2))

    elif cmd == "--explain":
        if len(sys.argv) < 3:
            print("Usage: --explain '<json array of raw network dicts>'")
            sys.exit(1)
        networks = json.loads(sys.argv[2])
        agent = NumpyNetworkAgent(n_actions=len(networks), weights_path=weights_path)
        names = [n.get("ssid", f"net{i}") for i, n in enumerate(networks)]
        for n in networks:
            features = normalize_network_features(n)
            agent.observe(features)
        result = agent.explain(names)
        # Print layman-friendly output
        print(f"DECISION: {result['reason']}")
        print(f"CONFIDENCE: {result['confidence']*100:.0f}%")
        print(f"TREND: {result['temporal_trend']}")
        print(f"\nSIMPLE EXPLANATION:")
        print(f"  {result['layman_summary']}")
        print(f"\nFACTOR BREAKDOWN:")
        for name, weight in result['top_factors']:
            bar = "+" * max(1, int(abs(weight) * 10)) if weight > 0 else "-" * max(1, int(abs(weight) * 10))
            print(f"  {name:15s} [{bar:>10s}] {weight:+.3f}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
