"""
Output formatters for the Agentic Commerce Engine CLI.

Separates presentation from business logic, enabling future frontends
(MCP server, REST proxy, etc.) to reuse commerce_client.py without
pulling in CLI display concerns.
"""
import json

CURRENCY_SYMBOLS = {"CNY": "¥", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}

def currency(code):
    return CURRENCY_SYMBOLS.get(code, f"{code} ")

def format_output(data, command=None):
    """Route data to the appropriate human-readable formatter, or fall back to JSON."""
    if isinstance(data, dict) and "error" in data:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if command == "cart" and isinstance(data, dict) and data.get("success") and "items" in data:
        _format_cart(data)
    elif command == "list" and isinstance(data, dict) and data.get("success") and "products" in data:
        _format_product_list(data)
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def _format_cart(data):
    if not data["items"]:
        print("Your cart is empty.")
        return

    curr = data.get("currency", "USD")
    print(f"{'Item':<25} | {'Variant':<15} | {'Price':<10} | {'Qty':<4} | {'Subtotal':<10}")
    for item in data["items"]:
        name = item.get("product_name", item.get("product_slug", ""))
        variant = item.get("variant", item.get("gram", ""))
        price = item.get("price", 0)
        qty = item.get("quantity", 0)
        subtotal = price * qty
        sym = currency(item.get("currency", curr))
        print(f"{name[:25]:<25} | {str(variant):<15} | {sym}{price:<9.2f} | {qty:<4} | {sym}{subtotal:<9.2f}")

    sym = currency(data.get("currency", curr))
    print(f"Total: {sym}{data.get('totalPrice', 0):.2f}")

def _format_product_list(data):
    for p in data["products"]:
        name = p.get("name")
        slug = p.get("slug")
        print(f"• {name} ({slug})")
        if p.get("variants"):
            parts = []
            for v in p["variants"]:
                v_name = v.get("variant", v.get("gram"))
                v_price = v.get("price")
                sym = currency(v.get("currency", "USD"))
                parts.append(f"{v_name}: {sym}{v_price}")
            print(f"  Variants: {' | '.join(parts)}")
    print(f"Total: {data.get('total')} items found | Page {data.get('page')}/{data.get('totalPages')}")
