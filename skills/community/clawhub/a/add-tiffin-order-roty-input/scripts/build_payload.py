import json
from datetime import datetime


def format_dates(dates):
    return '; '.join([d.strftime('%d/%m/%Y') for d in sorted(dates)])


def build_payload(parsed, product, mod1, mod2, per_date_costs):
    userRef = "CR6osYANseVNs089MuMqwPNdKXF3"
    vendorRef = "qfiDIvUSocQFrVPzM4zQ"
    customerName = parsed.get('customerName') or (parsed.get('userAddress') or '').split(' ')[1] if parsed.get('userAddress') else ''
    payload = {
        "userRef": userRef,
        "vendorRef": vendorRef,
        "status": "Confirmed",
        "pickup": False,
        "userAddress": parsed.get('userAddress',''),
        "deliveryInstructions": "",
        "preferredTime": "",
        "deliveryCost": 0,
        "discount": "totalorder:0",
        "bankTransfer": True,
        "bankTransferReference": "",
        "cash": False,
        "customerName": customerName,
        "customerEmail": parsed.get('customerEmail',''),
        "customerPhoneNumber": parsed.get('customerPhoneNumber',''),
        "selfManagedNdisTransaction": False,
        "listOfOrderDetails": []
    }
    detail = {
        "name": product['name'],
        "productRef": product['productRef'],
        "quantity": 1,
        "modifier1Name": product.get('modifier1Name','Selection'),
        "modification1": mod1.get('modificationName') if mod1 else '',
        "modifier2Name": product.get('modifier2Name','Customisations (free unless priced)'),
        "modification2": mod2.get('modificationName') if mod2 else '',
        "specialRequests": parsed.get('specialRequests',''),
        "image": product.get('photo',''),
        "isCatering": True,
        "deliverySchedule": format_dates(parsed.get('deliveryDates',[])),
        "perProductCost": json.dumps([float(x) for x in per_date_costs])
    }
    payload['listOfOrderDetails'].append(detail)
    return payload

if __name__ == '__main__':
    import sys
    print('build_payload module')
