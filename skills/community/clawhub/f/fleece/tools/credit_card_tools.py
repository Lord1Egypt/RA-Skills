from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool, BaseTool, StructuredTool

from tools.brave_client import build_brave_wrapper, search_and_format

# Cents-per-point defaults by issuer keyword for ROI calculation
_CPP_MAP = {
    "chase": 1.5,
    "sapphire": 1.5,
    "freedom": 1.0,
    "amex": 1.8,
    "american express": 1.8,
    "gold": 1.8,
    "platinum": 1.8,
    "capital one": 1.35,
    "venture": 1.35,
    "citi": 1.6,
    "strata": 1.6,
    "bilt": 1.7,
    "marriott": 0.8,
    "hilton": 0.5,
    "delta": 1.1,
    "united": 1.2,
    "southwest": 1.5,
}


def _guess_cpp(card_name: str) -> float:
    lower = card_name.lower()
    for keyword, cpp in _CPP_MAP.items():
        if keyword in lower:
            return cpp
    return 1.0  # default to cash back value


# ---------------------------------------------------------------------------
# Pydantic schemas for multi-argument tools
# ---------------------------------------------------------------------------

class CompareCardsInput(BaseModel):
    card_a: str = Field(description="Name of the first credit card")
    card_b: str = Field(description="Name of the second credit card")
    comparison_aspects: str = Field(
        default="fees,rewards,welcome_offer,credits,transfer_partners",
        description="Comma-separated aspects to compare",
    )


class FirstYearROIInput(BaseModel):
    card_name: str = Field(description="Name of the credit card")
    monthly_spend_travel: float = Field(default=0, description="Monthly travel spend in dollars")
    monthly_spend_dining: float = Field(default=0, description="Monthly dining spend in dollars")
    monthly_spend_other: float = Field(default=0, description="Monthly other spend in dollars")


class AnalyzeWalletInput(BaseModel):
    cards_owned: str = Field(description="Comma-separated list of credit cards the user currently holds")


class RecommendCardsInput(BaseModel):
    spending_profile: str = Field(description="Description of the user's spending habits and priorities")
    preferences: str = Field(default="", description="Additional preferences (e.g. no annual fee, travel perks)")


# ---------------------------------------------------------------------------
# Tool factory
# ---------------------------------------------------------------------------

def build_tools(brave_api_key: str) -> list[BaseTool]:
    wrapper = build_brave_wrapper(brave_api_key)
    recent_wrapper = build_brave_wrapper(brave_api_key, freshness="pm")

    # --- Tool 1: Full card report ---
    @tool
    def search_card_full_report(card_name: str) -> str:
        """Look up a comprehensive credit card report including annual fee, welcome offer,
        earning rates, statement credits, benefits, and redemption strategy.
        Use when the user asks about a specific card in detail."""
        query = f'"{card_name}" credit card annual fee welcome offer earning rates benefits credits 2025'
        return search_and_format(wrapper, query)

    # --- Tool 2: Earning rates ---
    @tool
    def search_card_earning_rates(card_name: str, category: str = "") -> str:
        """Find the earning rates for a credit card, optionally filtered to a spending category
        (dining, travel, groceries, gas, etc.).
        Use when the user asks how many points, miles, or cash back a card earns."""
        category_clause = f"{category} " if category else ""
        query = f'"{card_name}" {category_clause}earning rates points miles cashback per dollar categories 2025'
        return search_and_format(wrapper, query)

    # --- Tool 3: Transfer partners ---
    @tool
    def search_transfer_partners(card_name: str) -> str:
        """Find the airline and hotel transfer partners for a credit card's rewards program,
        including transfer ratios and timing.
        Use when the user asks about transfer partners or moving points to airlines/hotels."""
        query = f'"{card_name}" transfer partners airlines hotels ratio transfer time 2025'
        return search_and_format(wrapper, query)

    # --- Tool 4: Statement credits ---
    @tool
    def search_statement_credits(card_name: str) -> str:
        """Look up all statement credits and perks a credit card offers — dining, travel,
        streaming, hotel, airline credits — including enrollment requirements.
        Use when the user asks about credits, perks, or offsetting the annual fee."""
        query = f'"{card_name}" statement credits perks benefits complete list how to use 2025'
        return search_and_format(wrapper, query)

    # --- Tool 5: First-year ROI ---
    def _calculate_first_year_roi(
        card_name: str,
        monthly_spend_travel: float = 0,
        monthly_spend_dining: float = 0,
        monthly_spend_other: float = 0,
    ) -> str:
        """Calculate the estimated first-year return on investment for a credit card given
        the user's spending habits.
        Use when the user wants to know if a card is worth it based on how they spend."""
        annual_travel = monthly_spend_travel * 12
        annual_dining = monthly_spend_dining * 12
        annual_other = monthly_spend_other * 12

        query = f'"{card_name}" annual fee welcome bonus points value first year 2025'
        research = search_and_format(wrapper, query)

        cpp = _guess_cpp(card_name)
        spend_summary = (
            f"Annual spend — Travel: ${annual_travel:,.0f} | "
            f"Dining: ${annual_dining:,.0f} | "
            f"Other: ${annual_other:,.0f}\n"
            f"Assumed value per point: {cpp}¢\n\n"
            f"Live research results:\n{research}\n\n"
            "Based on the research above, calculate the net first-year value as: "
            "welcome bonus value + estimated annual earn value + annual credits - annual fee. "
            "Show the math step by step."
        )
        return spend_summary

    calculate_first_year_roi = StructuredTool.from_function(
        func=_calculate_first_year_roi,
        name="calculate_first_year_roi",
        description=(
            "Calculate the estimated first-year return on investment for a credit card "
            "given the user's monthly spending on travel, dining, and other categories. "
            "Use when the user wants to know if a card is worth it for them."
        ),
        args_schema=FirstYearROIInput,
    )

    # --- Tool 6: Compare two cards ---
    def _compare_cards(
        card_a: str,
        card_b: str,
        comparison_aspects: str = "fees,rewards,welcome_offer,credits,transfer_partners",
    ) -> str:
        """Compare two credit cards side by side across fees, rewards, welcome offers,
        credits, and transfer partners.
        Use when the user asks 'which is better' or wants to compare two specific cards."""
        aspects = comparison_aspects.replace(",", ", ")
        query_a = f'"{card_a}" credit card {aspects} 2025'
        query_b = f'"{card_b}" credit card {aspects} 2025'
        results_a = search_and_format(wrapper, query_a)
        results_b = search_and_format(wrapper, query_b)
        return (
            f"## {card_a}\n{results_a}\n\n"
            f"## {card_b}\n{results_b}\n\n"
            "Compare the two cards above across these aspects and present a side-by-side "
            f"markdown table: {aspects}."
        )

    compare_cards = StructuredTool.from_function(
        func=_compare_cards,
        name="compare_cards",
        description=(
            "Compare two credit cards side by side. Searches for current data on both cards "
            "and produces a structured comparison. Use when the user asks 'which is better' "
            "or wants to compare two specific cards."
        ),
        args_schema=CompareCardsInput,
    )

    # --- Tool 7: Wallet / portfolio analysis ---
    def _analyze_wallet(cards_owned: str) -> str:
        """Analyze the user's existing credit card portfolio for gaps, overlaps, and
        optimization opportunities.
        Use when the user says 'I have X and Y cards, how do I maximize?' or asks about their wallet."""
        card_list = [c.strip() for c in cards_owned.split(",") if c.strip()]
        results = []
        for card in card_list:
            query = f'"{card}" earning rates categories benefits 2025'
            result = search_and_format(wrapper, query, max_results=2)
            results.append(f"### {card}\n{result}")

        combined = "\n\n".join(results)
        return (
            f"{combined}\n\n"
            "Based on the card details above, identify:\n"
            "1. Category coverage map (which card to use for travel, dining, groceries, gas, etc.)\n"
            "2. Overlapping benefits or redundant earning categories\n"
            "3. Gaps — spending categories with no bonus multiplier\n"
            "4. Top 1-2 cards that would complement this portfolio"
        )

    analyze_wallet = StructuredTool.from_function(
        func=_analyze_wallet,
        name="analyze_wallet",
        description=(
            "Analyze the user's existing credit card portfolio for gaps, overlaps, and "
            "optimization opportunities. Use when the user says 'I have X and Y cards, "
            "how do I maximize?' or asks about their wallet/portfolio."
        ),
        args_schema=AnalyzeWalletInput,
    )

    # --- Tool 8: Recent news / changes ---
    @tool
    def search_recent_changes(card_name: str) -> str:
        """Search for recent news and changes to a credit card in the last month —
        benefit cuts, fee increases, new perks, or limited-time offers.
        Use when the user asks if anything has changed recently about a card."""
        query = f'"{card_name}" credit card changes update news 2025'
        return search_and_format(recent_wrapper, query)

    # --- Tool 9: Profile-based recommendations ---
    def _recommend_cards_for_profile(
        spending_profile: str,
        preferences: str = "",
    ) -> str:
        """Search for the best US credit cards matching a spending profile and preferences.
        Use when the user asks for card recommendations based on how they spend."""
        pref_clause = f"{preferences} " if preferences else ""
        query = (
            f"best credit cards {spending_profile} {pref_clause}US 2025 "
            f"site:nerdwallet.com OR site:thepointsguy.com OR site:doctorofcredit.com OR site:uscreditcardguide.com"
        )
        return search_and_format(wrapper, query)

    recommend_cards_for_profile = StructuredTool.from_function(
        func=_recommend_cards_for_profile,
        name="recommend_cards_for_profile",
        description=(
            "Search for the best US credit cards matching a spending profile and preferences "
            "(e.g. 'high dining and travel spend, no annual fee preferred'). "
            "Use when the user asks for card recommendations based on their habits."
        ),
        args_schema=RecommendCardsInput,
    )

    return [
        search_card_full_report,
        search_card_earning_rates,
        search_transfer_partners,
        search_statement_credits,
        calculate_first_year_roi,
        compare_cards,
        analyze_wallet,
        search_recent_changes,
        recommend_cards_for_profile,
    ]
