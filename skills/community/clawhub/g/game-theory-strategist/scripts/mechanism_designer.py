class PersonalMechanismDesigner:
    """
    Evaluates whether a proposed agreement or life arrangement meets the
    criteria for Individual Rationality (IR) and Incentive Compatibility (IC).

    IR:  Participating >= Outside option (agent won't walk away)
    IC:  Acting truthfully >= Acting deceptively (agent has no reason to lie/defect)

    Usage:
        designer = PersonalMechanismDesigner(["Partner A", "Partner B"])
        designer.set_utility("Partner A", truthful_payoff=10, lying_payoff=12, outside_option=2)
        designer.set_utility("Partner B", truthful_payoff=10, lying_payoff=8,  outside_option=2)
        for line in designer.evaluate_mechanism():
            print(line)
    """

    def __init__(self, agents):
        self.agents = agents
        self.utilities = {}

    def set_utility(self, agent, truthful_payoff, lying_payoff, outside_option):
        """
        truthful_payoff  : utility when the agent cooperates/is honest
        lying_payoff     : utility when the agent defects/misrepresents
        outside_option   : utility of not participating at all (BATNA)
        """
        if agent not in self.agents:
            raise ValueError(f"Agent '{agent}' not in agent list: {self.agents}")
        self.utilities[agent] = {
            "truthful": truthful_payoff,
            "lying":    lying_payoff,
            "outside":  outside_option
        }

    def check_individual_rationality(self):
        """IR: participating is better than walking away."""
        return {
            agent: payoffs["truthful"] >= payoffs["outside"]
            for agent, payoffs in self.utilities.items()
        }

    def check_incentive_compatibility(self):
        """IC: truth-telling is better than defecting."""
        return {
            agent: payoffs["truthful"] >= payoffs["lying"]
            for agent, payoffs in self.utilities.items()
        }

    def evaluate_mechanism(self):
        """Returns a list of assessment strings for each agent."""
        ir = self.check_individual_rationality()
        ic = self.check_incentive_compatibility()
        report = []
        for agent in self.agents:
            if agent not in self.utilities:
                report.append(f"MISSING DATA: No utilities set for {agent}.")
                continue
            p = self.utilities[agent]
            failures = []
            if not ir[agent]:
                delta = p["outside"] - p["truthful"]
                failures.append(
                    f"FAILED IR: {agent} will likely walk away "
                    f"(outside option {p['outside']} > participation {p['truthful']}, gap: {delta:+.1f})"
                )
            if not ic[agent]:
                delta = p["lying"] - p["truthful"]
                failures.append(
                    f"FAILED IC: {agent} has incentive to defect/lie "
                    f"(defection payoff {p['lying']} > honest payoff {p['truthful']}, gap: {delta:+.1f})"
                )
            if not failures:
                report.append(
                    f"SUCCESS: {agent}'s incentives are aligned "
                    f"(participation: {p['truthful']}, outside: {p['outside']}, honesty surplus: {p['truthful'] - p['lying']:+.1f})"
                )
            else:
                report.extend(failures)
        return report

    def suggest_fix(self):
        """Suggests adjustments to restore IR and IC for failing agents."""
        ir = self.check_individual_rationality()
        ic = self.check_incentive_compatibility()
        suggestions = []
        for agent in self.agents:
            if agent not in self.utilities:
                continue
            p = self.utilities[agent]
            if not ir[agent]:
                gap = p["outside"] - p["truthful"]
                suggestions.append(
                    f"{agent}: Increase participation payoff by at least {gap:.1f} "
                    f"(e.g., add sweeteners, reduce obligations, or lower the outside option via timing/urgency)."
                )
            if not ic[agent]:
                gap = p["lying"] - p["truthful"]
                suggestions.append(
                    f"{agent}: Reduce defection payoff by at least {gap:.1f} "
                    f"(e.g., add monitoring, penalties for dishonesty, vesting cliffs, or performance milestones)."
                )
        return suggestions if suggestions else ["No fixes needed — mechanism is IR and IC for all agents."]


if __name__ == "__main__":
    # Example: Co-founder equity dispute
    print("=== Co-founder Mechanism Analysis ===")
    designer = PersonalMechanismDesigner(["Founder A", "Founder B"])
    designer.set_utility("Founder A", truthful_payoff=10, lying_payoff=13, outside_option=4)
    designer.set_utility("Founder B", truthful_payoff=10, lying_payoff=7,  outside_option=6)

    print("\nAssessment:")
    for line in designer.evaluate_mechanism():
        print(" ", line)

    print("\nRecommended fixes:")
    for line in designer.suggest_fix():
        print(" ", line)

    print()

    # Example: Marriage chore division
    print("=== Household Chore Mechanism ===")
    designer2 = PersonalMechanismDesigner(["Partner A", "Partner B"])
    designer2.set_utility("Partner A", truthful_payoff=10, lying_payoff=12, outside_option=2)
    designer2.set_utility("Partner B", truthful_payoff=10, lying_payoff=8,  outside_option=2)

    print("\nAssessment:")
    for line in designer2.evaluate_mechanism():
        print(" ", line)
