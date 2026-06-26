import numpy as np

class CounterfactualRegretMinimizer:
    """
    Models a simplified personal decision problem using CFR principles
    to find the optimal mixed strategy over simulated time.

    Usage:
        actions = ["Stay in Job", "Start Business"]
        cfr = CounterfactualRegretMinimizer(actions)
        for _ in range(1000):
            utilities = [np.random.normal(5, 1), np.random.normal(6, 4)]
            cfr.update(utilities)
        print(cfr.get_average_strategy())
        print(cfr.regret_report())
    """

    def __init__(self, actions):
        self.actions = actions
        self.num_actions = len(actions)
        self.regret_sum = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.iteration = 0

    def get_strategy(self):
        """Calculates current strategy via regret matching."""
        strategy = np.maximum(self.regret_sum, 0)
        normalizing_sum = np.sum(strategy)
        if normalizing_sum > 0:
            strategy = strategy / normalizing_sum
        else:
            strategy = np.ones(self.num_actions) / self.num_actions
        return strategy

    def update(self, utilities):
        """
        Updates counterfactual regret based on realized utilities.
        utilities: array of payoffs if each action had been taken.
        """
        utilities = np.array(utilities, dtype=float)
        strategy = self.get_strategy()
        self.strategy_sum += strategy
        expected_utility = np.dot(strategy, utilities)
        for a in range(self.num_actions):
            self.regret_sum[a] += utilities[a] - expected_utility
        self.iteration += 1

    def get_average_strategy(self):
        """Returns the converged optimal strategy distribution."""
        normalizing_sum = np.sum(self.strategy_sum)
        if normalizing_sum > 0:
            return self.strategy_sum / normalizing_sum
        else:
            return np.ones(self.num_actions) / self.num_actions

    def regret_report(self):
        """Returns a human-readable regret summary per action."""
        avg = self.get_average_strategy()
        report = {}
        for i, action in enumerate(self.actions):
            report[action] = {
                "optimal_weight": round(float(avg[i]), 3),
                "cumulative_regret": round(float(self.regret_sum[i]), 2),
                "recommendation": "Primary path" if avg[i] == max(avg) else "Hedge / fallback"
            }
        return report


if __name__ == "__main__":
    # Example: Weighing "Stay in Job" vs "Start Business" over 1000 simulations
    actions = ["Stay in Job", "Start Business"]
    cfr = CounterfactualRegretMinimizer(actions)

    for _ in range(1000):
        u_stay   = np.random.normal(5, 1)   # Stable, low variance
        u_start  = np.random.normal(6, 4)   # Higher EV, high variance
        cfr.update([u_stay, u_start])

    print("=== CFR Life Strategy Analysis ===")
    print(f"Iterations: {cfr.iteration}")
    print()
    for action, data in cfr.regret_report().items():
        print(f"  {action}:")
        print(f"    Optimal weight   : {data['optimal_weight']:.1%}")
        print(f"    Cumulative regret: {data['cumulative_regret']}")
        print(f"    Verdict          : {data['recommendation']}")
