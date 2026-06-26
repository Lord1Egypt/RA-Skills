Roty Tiffin - add-tiffin-order-roty-input

This skill automates placing Roty tiffin orders using the pricing_engine and build_payload scripts. It is intended for use with OpenClaw's skills system. 

Contents:
- scripts/handle_message.py — skill dispatcher
- scripts/pricing_engine.py — pricing logic
- scripts/build_payload.py — build order payload
- scripts/post_order.py — POSTs to order API + follow-ups
- data/products_roty.json — vendor/product list and prices

Please keep secrets and API keys out of this package; use environment variables instead.
