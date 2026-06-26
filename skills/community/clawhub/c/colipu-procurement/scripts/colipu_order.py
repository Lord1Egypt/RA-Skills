# -*- coding: utf-8 -*-
"""
科力普采购助手 - 指定商品下单
用法: python colipu_order.py "商品ID,数量" "商品ID,数量"
"""
import sys
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colipu_client import ColipuClient

def get_product_info(client, item_id):
    """获取商品详情（从 GetAttributeGroupList），失败则返回 None"""
    url = f"{client.config.base_url}/api/b2bApi/GetAttributeGroupList"
    resp = client.session.get(url, params={"ItemId": item_id}, headers=client._get_headers())
    try:
        data = resp.json()
        if data.get("code") == 1:
            items = data.get("Data", {}).get("items", [])
            if items:
                item = items[0]
                return {
                    "ItemSkuId": item.get("ItemId") or item.get("ProductSkuId"),
                    "SkuName": item.get("ItemFullName", ""),
                    "SalePrice": item.get("SalePrice", 0),
                    "NetPrice": item.get("NetPrice", 0),
                }
    except Exception:
        pass
    return None

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python colipu_order.py \"1618,50\" \"7986054,50\"")
        return

    # 解析参数
    selections = []
    for arg in args:
        parts = arg.strip().split(",")
        if len(parts) == 2:
            try:
                item_id = int(parts[0].strip())
                qty = int(parts[1].strip())
                selections.append((item_id, qty))
            except:
                pass

    if not selections:
        print("[X] Bad args. Example: python colipu_order.py \"1618,50\" \"7986054,50\"")
        return

    client = ColipuClient()

    if not client.config.login_name or not client.config.password:
        print("[X] Missing credentials: set env COLIPU_LOGIN_NAME / COLIPU_PASSWORD")
        return

    login_result = client.login()
    if login_result.get("code") != 1:
        print(f"[X] Login failed: {login_result.get('message', 'unknown')}")
        return
    print(f"[OK] Logged in")

    # 收货地址 + 成本中心
    receivers = client.get_receivers()
    cost_centers = client.get_valid_cost_centers()
    if not receivers or not cost_centers:
        print("[X] No receiver or cost center found")
        return

    receiver = receivers[0]
    cost_center = cost_centers[0]
    print(f"[i] Receiver: {receiver.get('ContactName','')} {receiver.get('Area','')}")
    print(f"[i] Cost Center: {cost_center.get('CostCenterName','')}")

    items = []
    total = 0.0
    for item_id, qty in selections:
        detail = get_product_info(client, item_id)
        if detail and detail["SalePrice"] > 0:
            items.append(client.build_order_item(
                item_sku_id=detail["ItemSkuId"],
                sale_price=detail["SalePrice"],
                sale_qty=qty
            ))
            subtotal = detail["SalePrice"] * qty
            total += subtotal
            safe_print(f"  [+] {detail['SkuName'][:40]} x{qty} = {subtotal:.2f}")
        else:
            items.append(client.build_order_item(
                item_sku_id=item_id,
                sale_price=0,
                sale_qty=qty
            ))
            safe_print(f"  [?] Item ID:{item_id} x{qty} (price unknown)")

    safe_print(f"\n  Total: {total:.2f} CNY")
    print()

    pre_result = client.pre_create_order(
        receiver_id=receiver["ReceiverId"],
        cost_center_id=cost_center["CostCenterId"],
        items=items
    )

    if not pre_result.get("Data", {}).get("Success"):
        msg = pre_result.get("Data", {}).get("Message", "unknown error")
        safe_print(f"[X] Pre-submit failed: {msg}")
        return

    guid = pre_result.get("Data", {}).get("Message")
    safe_print(f"[i] Pre-submitted OK, GuId: {guid}")
    print()

    confirm_result = client.confirm_order(guid=guid)

    if confirm_result.get("Code") == 200 and confirm_result.get("Data", {}).get("Success"):
        so_id = client.wait_order_create_result(guid, timeout=30) or "(async, query later in order list)"
        safe_print(f"\n{'='*50}")
        safe_print(f"[OK] ORDER PLACED SUCCESSFULLY!")
        safe_print(f"{'='*50}")
        safe_print(f"  SO#: {so_id}")
        safe_print(f"  Items: {len(items)} SKU(s)")
        safe_print(f"  Total: {total:.2f} CNY")
        safe_print(f"  Receiver: {receiver.get('ContactName','')}")
        safe_print(f"  Cost Center: {cost_center.get('CostCenterName','')}")
        safe_print(f"  Status: Pending Approval")
    else:
        msg = confirm_result.get("Data", {}).get("Message", "unknown")
        safe_print(f"\n[X] Order failed: {msg}")


def safe_print(msg):
    """Print with UTF-8 encoding fallbacks for Windows GBK terminals"""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
