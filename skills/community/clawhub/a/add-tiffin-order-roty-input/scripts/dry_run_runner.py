from parse_roty_input import parse_message
from match_product_and_modifiers import find_product_by_intent, match_modifiers
from pricing_engine import determine_cost_of_each_date_catering_product
from build_payload import build_payload


def dry_run(text):
    parsed = parse_message(text)
    print('Parsed:', parsed)
    pref, product = find_product_by_intent(parsed.get('intent'))
    if not product:
        print('Product not resolved. Available products:')
        import json, os
        pf = json.load(open('..//data/products_roty.json'))
        print([v['name'] for v in pf.values()])
        return
    m1, m2 = match_modifiers(product, parsed.get('mod1'), parsed.get('mod2'))
    print('Chosen productRef:', product['productRef'], 'name:', product['name'])
    print('Modifier1:', m1)
    print('Modifier2:', m2)
    dates = parsed.get('deliveryDates')
    if not dates:
        print('No delivery dates parsed; aborting')
        return
    per_date = determine_cost_of_each_date_catering_product(product.get('price'), m1.get('additionalCost') if m1 else 0, m2.get('additionalCost') if m2 else 0, product.get('cateringDiscountStack'), dates, product.get('cateringDiscountMode'), product.get('cateringDefaultWindowDays'))
    print('Per-date costs:', per_date)
    payload = build_payload(parsed, product, m1, m2, per_date)
    import json
    print('Payload (dry-run, not sent):')
    print(json.dumps(payload, indent=2))

if __name__ == '__main__':
    sample = "Roty input anne frank 46 kwinana st glen waverley veg 6 rotis extra rice wed to fri no onion"
    dry_run(sample)
