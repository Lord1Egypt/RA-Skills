#!/usr/bin/env python3
"""
Real SAC-LTC Training Pipeline for Network Switching
=====================================================
Trains the Soft Actor-Critic with Liquid Time-Constant cells
for intelligent Wi-Fi / cellular hotspot switching decisions.

Uses real RF physics models (ITU-R propagation, 3GPP path loss)
to generate physically grounded training environments — not mocks.

Usage:
    python3 train_sac_ltc.py                    # Train with defaults
    python3 train_sac_ltc.py --episodes 5000    # Custom episode count
    python3 train_sac_ltc.py --eval             # Evaluate trained model
"""

import json, math, os, random, sys, time
from pathlib import Path
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

DATA_DIR = Path.home() / ".net-intel"
DEVICE = torch.device("cpu")  # Intentionally CPU — model is tiny, GPU overhead not worth it

# ============================================================================
# RF PHYSICS — Real propagation models from ITU-R and 3GPP standards
# ============================================================================

class RFPhysics:
    """ITU-R and 3GPP propagation models for realistic training environments."""

    @staticmethod
    def free_space_path_loss(freq_ghz, dist_m):
        """ITU-R free-space path loss (dB). FSPL = 20log10(d) + 20log10(f) + 32.44"""
        if dist_m < 1:
            dist_m = 1
        return 20 * math.log10(dist_m) + 20 * math.log10(freq_ghz * 1000) + 32.44

    @staticmethod
    def indoor_path_loss_itu(freq_ghz, dist_m, n_walls=0, wall_loss_db=5.0):
        """ITU-R P.1238 indoor propagation. Loss = FSPL + wall_penetration + floor_factor."""
        fspl = RFPhysics.free_space_path_loss(freq_ghz, dist_m)
        # Distance power loss coefficient for residential
        n = 28 if freq_ghz < 3 else 30  # Path loss exponent
        excess = max(0, 10 * (n / 20 - 1) * math.log10(max(1, dist_m)))
        wall = n_walls * wall_loss_db
        return fspl + excess + wall

    @staticmethod
    def uma_nlos_3gpp(freq_ghz, dist_m):
        """3GPP TR 38.901 UMa NLOS path loss (7-24 GHz range)."""
        if dist_m < 10:
            dist_m = 10
        return 13.54 + 39.08 * math.log10(dist_m) + 20 * math.log10(freq_ghz)

    @staticmethod
    def rain_attenuation_itu(freq_ghz, rain_rate_mmh, path_km):
        """ITU-R P.838-3 rain attenuation. gamma_R = k * R^alpha."""
        # Coefficients for horizontal polarization (simplified)
        if freq_ghz < 5:
            k, alpha = 0.000387, 0.912
        elif freq_ghz < 10:
            k, alpha = 0.00887, 1.264
        elif freq_ghz < 30:
            k, alpha = 0.167, 1.032
        else:
            k, alpha = 0.751, 0.843
        gamma = k * (rain_rate_mmh ** alpha)
        return gamma * path_km

    @staticmethod
    def thermal_noise_dbm(bandwidth_mhz, temp_k=290):
        """Thermal noise floor = kTB."""
        k_boltz = 1.38e-23
        noise_w = k_boltz * temp_k * bandwidth_mhz * 1e6
        return 10 * math.log10(noise_w * 1000)  # Convert to dBm

    @staticmethod
    def shannon_capacity_mbps(bandwidth_mhz, snr_db):
        """Shannon capacity: C = BW * log2(1 + SNR)."""
        snr_linear = 10 ** (snr_db / 10)
        return bandwidth_mhz * math.log2(1 + snr_linear)


# ============================================================================
# ENVIRONMENT — Realistic RF Environment with multiple networks
# ============================================================================

class RFEnvironment:
    """Simulates a realistic wireless environment with physics-grounded propagation.

    NOT a mock — uses real ITU-R and 3GPP models for path loss, noise, and capacity.
    Models real-world phenomena: congestion patterns, interference, movement, hotspot behavior.
    """

    def __init__(self, n_networks=5, seed=None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.n_networks = n_networks
        self.step_count = 0
        self.time_of_day = random.uniform(0, 24)  # hours
        self._generate_environment()

    def _generate_environment(self):
        """Create a physically realistic set of networks."""
        self.networks = []
        # User position (origin)
        self.user_x, self.user_y = 0.0, 0.0
        for i in range(self.n_networks):
            is_hotspot = random.random() < 0.3  # 30% chance of hotspot
            if is_hotspot:
                # Hotspot: closer, mobile, variable backhaul
                dist = random.uniform(1, 8)  # 1-8 meters
                freq = 2.4 if random.random() < 0.3 else 5.0  # Most hotspots on 5GHz
                bandwidth = random.choice([20, 40, 80])
                # Cellular backhaul characteristics
                cell_gen = random.choice(["3g", "4g", "4g", "5g", "5g"])
                if cell_gen == "3g":
                    backhaul_mbps = random.uniform(1, 5)
                    backhaul_latency = random.uniform(80, 200)
                elif cell_gen == "4g":
                    backhaul_mbps = random.uniform(10, 50)
                    backhaul_latency = random.uniform(20, 60)
                else:  # 5g
                    backhaul_mbps = random.uniform(50, 300)
                    backhaul_latency = random.uniform(8, 25)
            else:
                # Infrastructure AP
                dist = random.uniform(3, 30)  # 3-30 meters
                freq = random.choice([2.4, 5.0, 5.0])  # Bias toward 5GHz
                bandwidth = random.choice([20, 40, 80, 160])
                backhaul_mbps = random.uniform(100, 1000)  # Wired backhaul
                backhaul_latency = random.uniform(2, 10)
                cell_gen = None
            # Channel assignment (realistic — clustered on popular channels)
            if freq == 2.4:
                channel = random.choice([1, 1, 6, 6, 11, 11, 1, 6, 3, 9])
            else:
                channel = random.choice([36, 44, 149, 149, 149, 153, 157, 161])
            # AP position (angle and distance from user)
            angle = random.uniform(0, 2 * math.pi)
            tx_power_dbm = random.uniform(15, 23) if not is_hotspot else random.uniform(10, 18)
            # Number of other networks on same channel (will be computed dynamically)
            n_walls = random.randint(0, 3) if dist > 5 else 0
            self.networks.append({
                "id": i,
                "ssid": f"{'Hotspot' if is_hotspot else 'AP'}_{i}",
                "is_hotspot": is_hotspot,
                "cell_gen": cell_gen,
                "freq_ghz": freq,
                "channel": channel,
                "bandwidth_mhz": bandwidth,
                "distance_m": dist,
                "angle_rad": angle,
                "tx_power_dbm": tx_power_dbm,
                "n_walls": n_walls,
                "backhaul_mbps": backhaul_mbps,
                "backhaul_latency_ms": backhaul_latency,
                "movement_speed": random.uniform(0.5, 2.0) if is_hotspot else 0,
                "noise_figure_db": random.uniform(3, 7),
            })

    def _compute_rssi(self, net, extra_loss_db=0):
        """Compute RSSI using real propagation model."""
        path_loss = RFPhysics.indoor_path_loss_itu(
            net["freq_ghz"], net["distance_m"],
            n_walls=net["n_walls"]
        )
        rssi = net["tx_power_dbm"] - path_loss - extra_loss_db
        return max(-100, min(-20, rssi))

    def _compute_noise(self, net):
        """Compute noise floor from thermal + interference."""
        thermal = RFPhysics.thermal_noise_dbm(net["bandwidth_mhz"])
        # Co-channel interference from other networks on same channel
        co_channel = sum(1 for n in self.networks
                        if n["channel"] == net["channel"] and n["id"] != net["id"])
        interference = co_channel * 3  # ~3dB per co-channel interferer
        return thermal + net["noise_figure_db"] + interference

    def _congestion_factor(self, net):
        """Count co-channel and adjacent-channel networks."""
        co = sum(1 for n in self.networks
                 if n["channel"] == net["channel"] and n["id"] != net["id"])
        adj = sum(1 for n in self.networks
                  if abs(n["channel"] - net["channel"]) <= 2
                  and n["channel"] != net["channel"]
                  and n["freq_ghz"] == net["freq_ghz"])
        return co + adj * 0.5

    def step(self):
        """Advance environment by one timestep (~30 seconds).

        Returns observations for all networks as list of dicts.
        """
        self.step_count += 1
        self.time_of_day = (self.time_of_day + 30 / 3600) % 24  # +30s

        # Time-of-day congestion pattern (real: peaks at 6-10pm)
        hour = self.time_of_day
        congestion_multiplier = 1.0 + 0.5 * math.exp(-((hour - 20) ** 2) / 8)

        # Random events
        has_movement = random.random() < 0.15  # 15% chance someone walks by
        has_interference = random.random() < 0.05  # 5% chance of interference event
        interference_band = 2.4 if random.random() < 0.7 else 5.0

        observations = []
        for net in self.networks:
            # Hotspot movement — distance changes over time
            if net["is_hotspot"] and net["movement_speed"] > 0:
                net["distance_m"] += random.gauss(0, 0.3)
                net["distance_m"] = max(1, min(15, net["distance_m"]))

            # Human movement causes temporary RSSI fluctuation
            body_loss = 0
            if has_movement:
                # Body absorption: 3-12 dB depending on proximity to signal path
                body_loss = random.uniform(3, 12) * math.exp(-net["distance_m"] / 10)

            # Compute RF metrics
            rssi = self._compute_rssi(net, extra_loss_db=body_loss)
            noise = self._compute_noise(net)
            # Add interference event
            if has_interference and abs(net["freq_ghz"] - interference_band) < 0.5:
                noise += random.uniform(5, 15)
            snr = rssi - noise

            # Throughput from Shannon capacity, limited by backhaul
            capacity = RFPhysics.shannon_capacity_mbps(net["bandwidth_mhz"], max(0, snr))
            # Congestion reduces effective throughput
            cong = self._congestion_factor(net) * congestion_multiplier
            effective_throughput = capacity / max(1, 1 + cong * 0.3)
            # Bottleneck is min of wireless capacity and backhaul
            throughput = min(effective_throughput, net["backhaul_mbps"])
            throughput = max(0.1, throughput + random.gauss(0, throughput * 0.05))

            # Latency: propagation + processing + congestion + backhaul
            base_latency = 2 + net["distance_m"] * 0.01  # ~2ms base
            congestion_latency = cong * random.uniform(2, 8)
            backhaul_lat = net["backhaul_latency_ms"]
            latency = base_latency + congestion_latency + backhaul_lat
            latency = max(1, latency + random.gauss(0, latency * 0.1))

            # Packet loss from congestion and poor SNR
            loss = 0
            if snr < 10:
                loss += random.uniform(1, 5)
            if cong > 5:
                loss += random.uniform(0.5, 3)
            loss = max(0, min(50, loss + random.gauss(0, 0.3)))

            observations.append({
                "id": net["id"],
                "ssid": net["ssid"],
                "is_hotspot": net["is_hotspot"],
                "cell_gen": net["cell_gen"],
                "rssi_dbm": round(rssi, 1),
                "noise_dbm": round(noise, 1),
                "snr_db": round(snr, 1),
                "latency_ms": round(latency, 1),
                "throughput_mbps": round(throughput, 2),
                "packet_loss_pct": round(loss, 2),
                "channel": net["channel"],
                "freq_ghz": net["freq_ghz"],
                "bandwidth_mhz": net["bandwidth_mhz"],
                "n_networks_on_channel": int(self._congestion_factor(net)),
                "is_5ghz": net["freq_ghz"] >= 5.0,
                "has_movement": has_movement,
                "has_interference": has_interference,
            })

        return observations

    def get_reward(self, action, observations):
        """Compute reward for choosing a network.

        Reward function designed to encourage:
          - High throughput
          - Low latency
          - Low packet loss
          - Stability (not switching too often)
        """
        if action >= len(observations):
            return -10.0  # Invalid action
        obs = observations[action]
        # Throughput reward (log scale to prevent domination by very fast networks)
        throughput_r = math.log2(max(1, obs["throughput_mbps"])) / 10
        # Latency penalty
        latency_r = -obs["latency_ms"] / 200
        # Loss penalty
        loss_r = -obs["packet_loss_pct"] / 5
        # Signal quality bonus
        snr_r = max(0, obs["snr_db"]) / 60
        return throughput_r + latency_r + loss_r + snr_r


# ============================================================================
# PyTorch SAC-LTC Model
# ============================================================================

class TorchLTCCell(nn.Module):
    """Liquid Time-Constant cell in PyTorch."""
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.W_x = nn.Linear(input_dim, hidden_dim)
        self.W_h = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_tau = nn.Linear(input_dim, hidden_dim)
        self.tau_base = nn.Parameter(torch.ones(hidden_dim))
        self.dt = 1.0
        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.W_x.weight)
        nn.init.xavier_uniform_(self.W_h.weight)
        nn.init.xavier_uniform_(self.W_tau.weight)
        nn.init.zeros_(self.W_x.bias)
        nn.init.zeros_(self.W_tau.bias)

    def forward(self, x, h):
        """x: (B, input_dim), h: (B, hidden_dim) → h_new: (B, hidden_dim), tau: (B, hidden_dim)"""
        f = torch.tanh(self.W_x(x) + self.W_h(h))
        tau = self.tau_base + F.softplus(self.W_tau(x))
        h_new = h + (self.dt / tau) * (-h + f)
        return h_new, tau


class TorchKANLinear(nn.Module):
    """KAN layer: base(SiLU) + spline(RBF)."""
    def __init__(self, in_dim, out_dim, grid_size=5):
        super().__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.grid_size = grid_size
        n_basis = grid_size + 3
        self.base_weight = nn.Linear(in_dim, out_dim)
        self.spline_weight = nn.Parameter(torch.randn(in_dim, n_basis, out_dim) * 0.1)
        self.register_buffer("grid", torch.linspace(-1, 1, n_basis))

    def forward(self, x):
        # Base: SiLU + linear
        base = self.base_weight(F.silu(x))
        # Spline: RBF basis
        # x: (B, in_dim) → expand for grid: (B, in_dim, 1)
        x_expand = x.unsqueeze(-1)  # (B, in_dim, 1)
        basis = torch.exp(-0.5 * ((x_expand - self.grid) / 0.3) ** 2)  # (B, in_dim, n_basis)
        spline = torch.einsum("bin,ino->bo", basis, self.spline_weight)
        return base + spline


class SACLTCAgent(nn.Module):
    """Full SAC-LTC agent with actor and twin critics."""
    def __init__(self, n_features=8, hidden_dim=32, kan_hidden=16, n_actions=5):
        super().__init__()
        self.n_actions = n_actions
        self.hidden_dim = hidden_dim
        # Encoder
        self.ltc = TorchLTCCell(n_features, hidden_dim)
        # Actor (KAN)
        self.kan1 = TorchKANLinear(hidden_dim, kan_hidden)
        self.ln1 = nn.LayerNorm(kan_hidden)
        self.kan2 = TorchKANLinear(kan_hidden, n_actions)
        # Twin critics
        self.q1 = nn.Sequential(
            nn.Linear(hidden_dim, 64), nn.LayerNorm(64), nn.SiLU(),
            nn.Linear(64, n_actions)
        )
        self.q2 = nn.Sequential(
            nn.Linear(hidden_dim, 64), nn.LayerNorm(64), nn.SiLU(),
            nn.Linear(64, n_actions)
        )
        # Target critics
        self.q1_target = nn.Sequential(
            nn.Linear(hidden_dim, 64), nn.LayerNorm(64), nn.SiLU(),
            nn.Linear(64, n_actions)
        )
        self.q2_target = nn.Sequential(
            nn.Linear(hidden_dim, 64), nn.LayerNorm(64), nn.SiLU(),
            nn.Linear(64, n_actions)
        )
        self.q1_target.load_state_dict(self.q1.state_dict())
        self.q2_target.load_state_dict(self.q2.state_dict())
        # Entropy temperature
        self.log_alpha = nn.Parameter(torch.tensor(0.0))
        self.target_entropy = -0.98 * math.log(1.0 / n_actions)

    def actor(self, h):
        """h: (B, hidden_dim) → probs: (B, n_actions)"""
        x = self.kan1(h)
        x = self.ln1(x)
        logits = self.kan2(x)
        return F.softmax(logits, dim=-1)

    def forward(self, x_seq, h=None):
        """Process sequence through LTC then actor.

        x_seq: (B, T, n_features)
        Returns: probs, h_final, all_tau
        """
        B, T, _ = x_seq.shape
        if h is None:
            h = torch.zeros(B, self.hidden_dim, device=x_seq.device)
        all_tau = []
        for t in range(T):
            h, tau = self.ltc(x_seq[:, t, :], h)
            all_tau.append(tau)
        probs = self.actor(h)
        return probs, h, all_tau


# ============================================================================
# REPLAY BUFFER
# ============================================================================

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state_seq, action, reward, next_state_seq, done):
        self.buffer.append((state_seq, action, reward, next_state_seq, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(np.array(states), dtype=torch.float32),
            torch.tensor(actions, dtype=torch.long),
            torch.tensor(rewards, dtype=torch.float32),
            torch.tensor(np.array(next_states), dtype=torch.float32),
            torch.tensor(dones, dtype=torch.float32),
        )

    def __len__(self):
        return len(self.buffer)


# ============================================================================
# TRAINING LOOP
# ============================================================================

def normalize_features(obs):
    """Convert raw observation dict to normalized feature vector."""
    rssi = obs["rssi_dbm"]
    noise = obs["noise_dbm"]
    return [
        max(0, min(1, (rssi + 100) / 60)),
        max(0, min(1, (rssi - noise) / 60)),
        max(0, min(1, 1 - (obs["latency_ms"] / 200))),
        max(0, min(1, obs["throughput_mbps"] / 100)),
        max(0, min(1, 1 - (obs["packet_loss_pct"] / 10))),
        max(0, min(1, 1 - (obs["n_networks_on_channel"] / 10))),
        1.0 if obs["is_5ghz"] else 0.0,
        1.0 if obs["is_hotspot"] else 0.0,
    ]


def train(episodes=2000, seq_len=8, batch_size=128, gamma=0.99, tau_polyak=0.005, lr=3e-4):
    n_networks = 5
    agent = SACLTCAgent(n_features=8, hidden_dim=32, kan_hidden=16, n_actions=n_networks).to(DEVICE)

    actor_params = list(agent.ltc.parameters()) + list(agent.kan1.parameters()) + \
                   list(agent.ln1.parameters()) + list(agent.kan2.parameters())
    critic_params = list(agent.q1.parameters()) + list(agent.q2.parameters())

    actor_opt = optim.Adam(actor_params, lr=lr)
    critic_opt = optim.Adam(critic_params, lr=lr)
    alpha_opt = optim.Adam([agent.log_alpha], lr=lr)

    buffer = ReplayBuffer(capacity=50000)
    best_reward = -float("inf")
    reward_history = []

    print(f"Training SAC-LTC: {episodes} episodes, {n_networks} networks")
    print(f"Model parameters: {sum(p.numel() for p in agent.parameters()):,}")
    start_time = time.time()

    for ep in range(episodes):
        env = RFEnvironment(n_networks=n_networks, seed=ep)
        state_history = deque(maxlen=seq_len)
        ep_reward = 0
        current_action = 0

        # Warm up state history
        for _ in range(seq_len):
            obs_list = env.step()
            features = [normalize_features(o) for o in obs_list]
            # Use best-scoring network's features as state
            state_history.append(features[current_action])

        for step in range(100):  # 100 steps per episode (~50 minutes simulated)
            obs_list = env.step()
            state_seq = np.array(list(state_history))  # (seq_len, n_features)

            # Get action from policy
            with torch.no_grad():
                s = torch.tensor(state_seq, dtype=torch.float32).unsqueeze(0)
                probs, _, _ = agent(s)
                dist = torch.distributions.Categorical(probs)
                action = dist.sample().item()

            # Get reward
            reward = env.get_reward(action, obs_list)
            # Switching penalty (hysteresis)
            if action != current_action:
                reward -= 0.3  # Small penalty for switching
            current_action = action

            # Next state
            features = [normalize_features(o) for o in obs_list]
            state_history.append(features[action])
            next_state_seq = np.array(list(state_history))

            done = step == 99
            buffer.push(state_seq, action, reward, next_state_seq, float(done))
            ep_reward += reward

            # Train if enough data
            if len(buffer) >= batch_size:
                states, actions, rewards_b, next_states, dones = buffer.sample(batch_size)

                # Critic update
                with torch.no_grad():
                    next_probs, _, _ = agent(next_states)
                    next_q1 = agent.q1_target(agent.ltc(next_states[:, -1, :],
                               torch.zeros(batch_size, agent.hidden_dim))[0])
                    next_q2 = agent.q2_target(agent.ltc(next_states[:, -1, :],
                               torch.zeros(batch_size, agent.hidden_dim))[0])
                    next_q_min = torch.min(next_q1, next_q2)
                    alpha = agent.log_alpha.exp()
                    next_v = (next_probs * (next_q_min - alpha * torch.log(next_probs + 1e-8))).sum(-1)
                    target_q = rewards_b + gamma * (1 - dones) * next_v

                # Process states through LTC
                _, h_final, _ = agent(states)
                q1_vals = agent.q1(h_final).gather(1, actions.unsqueeze(1)).squeeze()
                q2_vals = agent.q2(h_final).gather(1, actions.unsqueeze(1)).squeeze()
                critic_loss = F.mse_loss(q1_vals, target_q) + F.mse_loss(q2_vals, target_q)

                critic_opt.zero_grad()
                critic_loss.backward()
                torch.nn.utils.clip_grad_norm_(critic_params, 1.0)
                critic_opt.step()

                # Actor update
                probs_train, h_train, _ = agent(states)
                q1_train = agent.q1(h_train.detach())
                q2_train = agent.q2(h_train.detach())
                q_min = torch.min(q1_train, q2_train)
                alpha = agent.log_alpha.exp().detach()
                log_probs = torch.log(probs_train + 1e-8)
                actor_loss = (probs_train * (alpha * log_probs - q_min)).sum(-1).mean()

                actor_opt.zero_grad()
                actor_loss.backward()
                torch.nn.utils.clip_grad_norm_(actor_params, 1.0)
                actor_opt.step()

                # Alpha (entropy temperature) update
                entropy = -(probs_train.detach() * log_probs.detach()).sum(-1).mean()
                alpha_loss = agent.log_alpha * (entropy - agent.target_entropy)
                alpha_opt.zero_grad()
                alpha_loss.backward()
                alpha_opt.step()

                # Soft update target networks
                with torch.no_grad():
                    for p, p_targ in zip(agent.q1.parameters(), agent.q1_target.parameters()):
                        p_targ.data.mul_(1 - tau_polyak).add_(p.data, alpha=tau_polyak)
                    for p, p_targ in zip(agent.q2.parameters(), agent.q2_target.parameters()):
                        p_targ.data.mul_(1 - tau_polyak).add_(p.data, alpha=tau_polyak)

        reward_history.append(ep_reward)

        if ep_reward > best_reward:
            best_reward = ep_reward

        if (ep + 1) % 100 == 0:
            avg_r = np.mean(reward_history[-100:])
            elapsed = time.time() - start_time
            print(f"  Episode {ep+1}/{episodes} | Avg reward: {avg_r:.2f} | "
                  f"Best: {best_reward:.2f} | Alpha: {agent.log_alpha.exp().item():.3f} | "
                  f"Time: {elapsed:.0f}s")

    # Save trained weights
    save_path = DATA_DIR / "trained_model.pt"
    torch.save(agent.state_dict(), str(save_path))
    print(f"\nModel saved to {save_path}")

    # Export to numpy-compatible JSON for the lightweight agent
    export_to_numpy_weights(agent, str(DATA_DIR / "weights.json"))
    print(f"Numpy weights exported to {DATA_DIR / 'weights.json'}")

    return agent, reward_history


def export_to_numpy_weights(agent, path):
    """Export PyTorch model weights to JSON format for the numpy agent."""
    with torch.no_grad():
        data = {
            "ltc": {
                "W_x": agent.ltc.W_x.weight.t().tolist(),  # Transpose for our convention
                "W_h": agent.ltc.W_h.weight.t().tolist(),
                "b": agent.ltc.W_x.bias.tolist(),
                "W_tau": agent.ltc.W_tau.weight.t().tolist(),
                "b_tau": agent.ltc.W_tau.bias.tolist(),
                "tau_base": agent.ltc.tau_base.tolist(),
            },
            "kan1": {
                "base_weight": agent.kan1.base_weight.weight.t().tolist(),
                "spline_weight": agent.kan1.spline_weight.tolist(),
            },
            "kan2": {
                "base_weight": agent.kan2.base_weight.weight.t().tolist(),
                "spline_weight": agent.kan2.spline_weight.tolist(),
            },
            "hidden": [0.0] * agent.hidden_dim,
        }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)


def evaluate(n_episodes=50):
    """Evaluate trained model."""
    model_path = DATA_DIR / "trained_model.pt"
    if not model_path.exists():
        print("No trained model found. Run training first.")
        sys.exit(1)

    agent = SACLTCAgent()
    agent.load_state_dict(torch.load(str(model_path), weights_only=True))
    agent.eval()

    total_rewards = []
    for ep in range(n_episodes):
        env = RFEnvironment(n_networks=5, seed=10000 + ep)
        state_history = deque(maxlen=8)
        ep_reward = 0
        current_action = 0

        for _ in range(8):
            obs_list = env.step()
            features = [normalize_features(o) for o in obs_list]
            state_history.append(features[current_action])

        for step in range(100):
            obs_list = env.step()
            state_seq = np.array(list(state_history))
            with torch.no_grad():
                s = torch.tensor(state_seq, dtype=torch.float32).unsqueeze(0)
                probs, _, _ = agent(s)
                action = probs.argmax(dim=-1).item()
            reward = env.get_reward(action, obs_list)
            if action != current_action:
                reward -= 0.3
            current_action = action
            features = [normalize_features(o) for o in obs_list]
            state_history.append(features[action])
            ep_reward += reward

        total_rewards.append(ep_reward)

    print(f"\nEvaluation Results ({n_episodes} episodes):")
    print(f"  Mean reward:   {np.mean(total_rewards):.2f}")
    print(f"  Std reward:    {np.std(total_rewards):.2f}")
    print(f"  Min reward:    {np.min(total_rewards):.2f}")
    print(f"  Max reward:    {np.max(total_rewards):.2f}")

    # Random baseline
    random_rewards = []
    for ep in range(n_episodes):
        env = RFEnvironment(n_networks=5, seed=10000 + ep)
        ep_reward = 0
        current_action = 0
        for _ in range(8):
            env.step()
        for step in range(100):
            obs_list = env.step()
            action = random.randint(0, 4)
            reward = env.get_reward(action, obs_list)
            if action != current_action:
                reward -= 0.3
            current_action = action
            ep_reward += reward
        random_rewards.append(ep_reward)

    print(f"\nRandom Baseline ({n_episodes} episodes):")
    print(f"  Mean reward:   {np.mean(random_rewards):.2f}")
    improvement = ((np.mean(total_rewards) - np.mean(random_rewards)) /
                   abs(np.mean(random_rewards))) * 100
    print(f"\nSAC-LTC improvement over random: {improvement:.1f}%")


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if "--eval" in sys.argv:
        evaluate()
    else:
        episodes = 2000
        for i, arg in enumerate(sys.argv):
            if arg == "--episodes" and i + 1 < len(sys.argv):
                episodes = int(sys.argv[i + 1])
        train(episodes=episodes)
