"""agent-pay-client usage examples."""
from agent_pay_client import AgentPayClient, PayerConfig

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Inspect a paywall without paying")
    print("=" * 70)
    client = AgentPayClient()
    info = client.get_payment_options(
        "https://btc-vision.org/.netlify/functions/mcp",
        json={"tool": "get_full_summary"},
    )
    print(info)

    print()
    print("=" * 70)
    print("EXAMPLE 2: Pay via x402 with an explicit spending ceiling")
    print("=" * 70)
    config = PayerConfig(
        evm_private_key="0x" + "11" * 32,  # replace with your own key, never commit real keys
        max_x402_atomic="50000",            # refuse any charge above $0.05 USDC
    )
    result = AgentPayClient(config).fetch(
        "https://btc-vision.org/.netlify/functions/mcp",
        json={"tool": "get_full_summary"},
    )
    print(result)

    print()
    print("=" * 70)
    print("EXAMPLE 3: L402/Lightning stays manual-approval unless opted in")
    print("=" * 70)
    result2 = AgentPayClient(PayerConfig()).fetch(
        "https://btc-vision.org/.netlify/functions/mcp",
        json={"tool": "get_market_signals"},
    )
    print(result2)  # will report "manual payment required" with the invoice/QR
