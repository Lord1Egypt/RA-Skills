"""
Chinese-localized output formatters for the Lafeitu brand skill.

Based on the engine's lib/formatters.py pattern, adapted with
Chinese currency defaults and Mandarin display labels.
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
        print("您的购物车是空的。")
        return

    curr = data.get("currency", "CNY")
    print(f"{'商品':<20} | {'规格':<10} | {'单价':<8} | {'数量':<4} | {'小计':<8}")
    for item in data["items"]:
        name = item.get("product_name", item.get("product_slug", ""))
        variant = item.get("gram", item.get("variant", ""))
        price = item.get("price", 0)
        qty = item.get("quantity", 0)
        subtotal = price * qty
        sym = currency(item.get("currency", curr))
        print(f"{name[:20]:<20} | {str(variant):<10} | {sym}{price:<7.2f} | {qty:<4} | {sym}{subtotal:<7.2f}")

    sym = currency(curr)
    print(f"总计金额: {sym}{data.get('totalPrice', 0):.2f}")

def _format_product_list(data):
    for p in data["products"]:
        name = p.get("name")
        slug = p.get("slug")
        print(f"• {name} ({slug})")
        if p.get("variants"):
            prices = []
            for v in p["variants"]:
                sym = currency(v.get("currency", "CNY"))
                prices.append(f"{v.get('variant')}g: {sym}{v.get('price')}")
            print(f"  规格: {' / '.join(prices)}")
    print(f"共 {data.get('total')} 款商品 | 第 {data.get('page')}/{data.get('totalPages')} 页")
