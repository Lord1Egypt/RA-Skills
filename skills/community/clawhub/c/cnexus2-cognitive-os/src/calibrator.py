from collections import Counter


class PersonaCalibrator:
    """
    Persona Distiller - Module 2: Initial Belief & Strategy Calibrator
    Scans all distilled memory blocks to reverse-engineer the subject's
    cognitive profile parameters before the kernel starts conversing.
    """
    def __init__(self):
        self.profile = {
            "dominant_intent": "converse",
            "initial_belief_base": 0.0,
            "policy_bias": {"SPEAK": 0.5, "RECALL": 0.5},
            "cognitive_density": 0.0,
        }

    def analyze_profile(self, serialized_blocks: list) -> dict:
        """
        Core analysis method. Scans memory blocks to extract personality traits.
        """
        if not serialized_blocks:
            print("[Calibrator][Warning] Empty memory blocks, returning default balanced profile.")
            return self.profile

        total_blocks = len(serialized_blocks)
        intent_list = []
        strategy_list = []
        weight_sum = 0.0

        for block in serialized_blocks:
            content = block.get('content', {})
            metadata = block.get('metadata', {})
            intent_list.append(content.get('intent', 'converse'))
            strategy_list.append(metadata.get('strategy', 'SPEAK'))
            weight_sum += block.get('weight', 0.1)

        # Intent dominance
        intent_counts = Counter(intent_list)
        dominant_intent = intent_counts.most_common(1)[0][0]

        # Policy bias (SPEAK vs RECALL)
        strategy_counts = Counter(strategy_list)
        speak_count = strategy_counts.get("SPEAK", 0)
        recall_count = strategy_counts.get("RECALL", 0)
        total_strategies = speak_count + recall_count
        if total_strategies > 0:
            self.profile["policy_bias"]["SPEAK"] = round(speak_count / total_strategies, 2)
            self.profile["policy_bias"]["RECALL"] = round(recall_count / total_strategies, 2)

        # Initial belief baseline
        avg_weight = weight_sum / total_blocks
        self.profile["initial_belief_base"] = min(
            round(avg_weight * 0.3 + (total_blocks * 0.002), 3), 0.5
        )
        self.profile["dominant_intent"] = dominant_intent
        self.profile["cognitive_density"] = round(total_blocks / 90.0, 2)

        print(f"[Calibrator] Cognitive profile extracted:")
        print(f" -> Dominant intent: {self.profile['dominant_intent']}")
        print(f" -> Belief baseline: {self.profile['initial_belief_base']}")
        print(f" -> Policy bias: SPEAK={self.profile['policy_bias']['SPEAK']}, RECALL={self.profile['policy_bias']['RECALL']}")
        print(f" -> Daily density: {self.profile['cognitive_density']} posts/day")
        return self.profile

    def apply_to_kernel(self, kernel_instance, calibrated_profile: dict):
        """
        Hot-inject the calibrated personality profile into a running CNexusOSKernel instance.
        """
        kernel_instance.reset()
        if hasattr(kernel_instance, 'cog') and 'cog_state' in kernel_instance.cog:
            cog_state = kernel_instance.cog['cog_state']
            cog_state['accumulated_weight'] = calibrated_profile["initial_belief_base"]
            cog_state['persona_policy_bias'] = calibrated_profile["policy_bias"]
            print("[Calibrator] Personality profile injected into kernel runtime.")
        else:
            print("[Calibrator][Error] Kernel runtime not ready, injection failed.")
