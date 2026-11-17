#!/usr/bin/env python3
"""Offline correctness tests for the SanMar skill's new parsers.

Runs the documented sample responses from the SanMar guides through the
real client/parsers (no network — a fake requests session returns canned
XML). Exits non-zero on the first failed assertion.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feed_parsers import (  # noqa: E402
    parse_daily_invoice_fixedwidth,
    parse_edi810,
    parse_inventory_feed,
    parse_shipment_status,
)
from sanmar_client import SanMarClient, _parse_invoices  # noqa: E402
from schemas import SanMarCredentials  # noqa: E402


class _FakeResp:
    def __init__(self, text: str, status: int = 200) -> None:
        self.text = text
        self.status_code = status
        self.ok = 200 <= status < 300


class _FakeSession:
    def __init__(self, text: str) -> None:
        self._text = text

    def post(self, *_a, **_k) -> _FakeResp:
        return _FakeResp(self._text)


def _client(xml: str) -> SanMarClient:
    return SanMarClient(
        credentials=SanMarCredentials("123", "u@x.com", "pw"),
        session=_FakeSession(xml),
    )


# --- 1. Invoice SOAP: GetInvoicesByPurchaseOrderNo (WS Guide 24.1 p37-39) ---
INVOICE_XML = """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
  <S:Body>
    <Invoices xmlns="http://webservice.integration.sanmar.com/">
      <Invoice>
        <Header>
          <InvoiceNo>12345678</InvoiceNo>
          <SalesOrderNumber>123456789</SalesOrderNumber>
          <InvoiceDate>2014-08-01</InvoiceDate>
          <InvoiceStatus>Unpaid</InvoiceStatus>
          <CustomerNo>5</CustomerNo>
          <SoldTo><Name>SANMAR</Name><Address><Address1>22833 SE Black Nugget Rd</Address1>
            <City>ISSAQUAH</City><State>WA</State><PostalCode>98029</PostalCode><Country>US</Country></Address></SoldTo>
          <RemitTo><Name>SANMAR CORP</Name><Address><Address1>PO BOX 34060</Address1>
            <City>SEATTLE</City><State>WA</State><PostalCode>98124-1060</PostalCode><Country>USA</Country></Address></RemitTo>
          <PurchaseOrderNo>4520838A</PurchaseOrderNo>
          <OrderDate>2014-08-01</OrderDate>
          <DueDate>2014-08-31</DueDate>
          <ShipVia>UPS</ShipVia><FOB>SPARKS NV</FOB><Terms>NET 30</Terms>
          <TotalCases>1</TotalCases><TotalWeight>36</TotalWeight>
          <SubTotal>192.72</SubTotal><SalesTax>0.0</SalesTax>
          <ShippingHandlingCharges>0.0</ShippingHandlingCharges><TotalAmount>192.72</TotalAmount>
          <Miscellaneous><FreightSavings>0.0</FreightSavings><TrackingIDs>NotUsed</TrackingIDs></Miscellaneous>
        </Header>
        <LineItem><StyleNo>2000</StyleNo><StyleColor>Red</StyleColor>
          <StyleDescription>100% ULTRA CTN T RED</StyleDescription><StyleSize>M</StyleSize>
          <Quantity>16</Quantity><UnitPrice>1.84</UnitPrice><Amount>29.44</Amount><UniqueKey>263633</UniqueKey></LineItem>
        <LineItem><StyleNo>2000</StyleNo><StyleColor>Red</StyleColor>
          <StyleDescription>100% ULTRA CTN T RED</StyleDescription><StyleSize>L</StyleSize>
          <Quantity>14</Quantity><UnitPrice>1.84</UnitPrice><Amount>25.76</Amount><UniqueKey>263634</UniqueKey></LineItem>
      </Invoice>
    </Invoices>
  </S:Body>
</S:Envelope>"""


def test_invoice_soap() -> None:
    res = _client(INVOICE_XML).get_invoices(query_type="purchase_order", value="4520838A")
    assert res.count == 1, res.count
    inv = res.invoices[0]
    assert inv.invoice_number == "12345678"
    assert inv.po_number == "4520838A"
    assert inv.sales_order_number == "123456789"
    assert inv.due_date == "2014-08-31"
    assert inv.terms == "NET 30"
    assert inv.total_amount == 192.72
    assert len(inv.lines) == 2
    assert inv.lines[0].style == "2000" and inv.lines[0].size == "M"
    assert inv.lines[0].quantity == 16 and inv.lines[0].unit_price == 1.84
    assert inv.lines[1].unique_key == "263634"
    common = inv.to_common()
    assert common["source"] == "sanmar"
    assert common["po_number"] == "4520838A"
    assert common["is_credit"] is False
    assert common["has_lines"] is True
    assert common["charges"]["merchandise"] == 192.72
    assert common["lines"][0]["qty_shipped"] == 16
    assert common["lines"][0]["net_price"] == 1.84
    print("PASS test_invoice_soap")


def test_invoice_single_root() -> None:
    # GetInvoiceByInvoiceNo returns a single <Invoice> root (no <Invoices>).
    single = INVOICE_XML.replace("<Invoices xmlns", "<Invoice xmlns").replace(
        "</Invoices>", ""
    )
    # remove the inner <Invoice>/<\/Invoice> wrapper duplication safely by parsing directly
    xml = """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body>
      <Invoice xmlns="http://webservice.integration.sanmar.com/">
        <Header><InvoiceNo>999</InvoiceNo><PurchaseOrderNo>PO9</PurchaseOrderNo>
        <TotalAmount>-5.00</TotalAmount></Header>
        <LineItem><StyleNo>PC61</StyleNo><StyleSize>S</StyleSize><Quantity>-1</Quantity>
        <UnitPrice>5.00</UnitPrice><Amount>-5.00</Amount></LineItem>
      </Invoice></S:Body></S:Envelope>"""
    invs = _parse_invoices(__import__("xml.etree.ElementTree", fromlist=["fromstring"]).fromstring(xml))
    assert len(invs) == 1 and invs[0].invoice_number == "999"
    assert invs[0].to_common()["is_credit"] is True  # negative total → credit memo
    assert single  # smoke: replacement produced text
    print("PASS test_invoice_single_root")


# --- 2. PromoStandards OSN tracking (WS Guide 24.1 p91) ---
OSN_XML = """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
  <S:Body>
    <ns2:GetOrderShipmentNotificationResponse
      xmlns:ns2="http://www.promostandards.org/WSDL/OrderShipmentNotificationService/1.0.0/"
      xmlns="http://www.promostandards.org/WSDL/OrderShipmentNotificationService/1.0.0/SharedObjects/">
      <ns2:OrderShipmentNotificationArray>
        <ns2:OrderShipmentNotification>
          <ns2:purchaseOrderNumber>PONUMBER</ns2:purchaseOrderNumber>
          <ns2:complete>true</ns2:complete>
          <ns2:SalesOrderArray>
            <ns2:SalesOrder>
              <ns2:salesOrderNumber>1112223334</ns2:salesOrderNumber>
              <ns2:complete>true</ns2:complete>
              <ns2:ShipmentLocationArray>
                <ns2:ShipmentLocation>
                  <ns2:id>1</ns2:id>
                  <ns2:ShipFromAddress><address1>x</address1><city>IRVING</city><region>TX</region>
                    <postalCode>75038</postalCode><country>US</country></ns2:ShipFromAddress>
                  <ns2:ShipToAddress><address1>y</address1><city>Jacksonville</city><region>FL</region>
                    <postalCode>32218</postalCode><country>US</country></ns2:ShipToAddress>
                  <ns2:PackageArray>
                    <ns2:Package>
                      <ns2:id>1</ns2:id>
                      <ns2:trackingNumber>1Z999</ns2:trackingNumber>
                      <ns2:shipmentDate>2023-01-12T22:44:42.467-08:00</ns2:shipmentDate>
                      <ns2:carrier>UPS</ns2:carrier>
                      <ns2:shipmentMethod>Ground</ns2:shipmentMethod>
                      <ns2:ItemArray>
                        <ns2:Item><ns2:supplierProductId>PC55P</ns2:supplierProductId>
                          <ns2:supplierPartId>834732</ns2:supplierPartId><ns2:quantity>1</ns2:quantity></ns2:Item>
                      </ns2:ItemArray>
                    </ns2:Package>
                  </ns2:PackageArray>
                </ns2:ShipmentLocation>
              </ns2:ShipmentLocationArray>
            </ns2:SalesOrder>
          </ns2:SalesOrderArray>
        </ns2:OrderShipmentNotification>
      </ns2:OrderShipmentNotificationArray>
    </ns2:GetOrderShipmentNotificationResponse>
  </S:Body>
</S:Envelope>"""


def test_tracking() -> None:
    res = _client(OSN_XML).get_tracking("PONUMBER")
    assert res.complete is True
    assert len(res.shipments) == 1
    s = res.shipments[0]
    assert s.tracking_number == "1Z999"
    assert s.carrier == "ups"
    assert s.shipment_method == "Ground"
    assert s.ship_date.startswith("2023-01-12")
    assert s.sales_order_number == "1112223334"
    assert s.ship_from_city == "IRVING" and s.ship_from_state == "TX"
    assert s.ship_to_city == "Jacksonville" and s.ship_to_state == "FL"
    assert len(s.items) == 1 and s.items[0].style == "PC55P"
    assert s.items[0].part_id == "834732" and s.items[0].quantity == 1
    print("PASS test_tracking")


# --- 3. PromoStandards Inventory v2.0.0 getInventoryLevels (WS Guide 24.1 p72) ---
INV_XML = """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
  <S:Body>
    <ns2:GetInventoryLevelsResponse
      xmlns:ns2="http://www.promostandards.org/WSDL/Inventory/2.0.0/"
      xmlns="http://www.promostandards.org/WSDL/Inventory/2.0.0/SharedObjects/">
      <Inventory>
        <productId>k420</productId>
        <PartInventoryArray>
          <PartInventory>
            <partId>92032</partId><mainPart>false</mainPart><partColor>Black</partColor><labelSize>S</labelSize>
            <partDescription>Port Authority Polo K420</partDescription>
            <quantityAvailable><Quantity><uom>EA</uom><value>1045</value></Quantity></quantityAvailable>
            <InventoryLocationArray>
              <InventoryLocation><inventoryLocationId>1</inventoryLocationId>
                <inventoryLocationName>Seattle</inventoryLocationName><postalCode>98027</postalCode>
                <inventoryLocationQuantity><Quantity><uom>EA</uom><value>0</value></Quantity></inventoryLocationQuantity>
              </InventoryLocation>
              <InventoryLocation><inventoryLocationId>2</inventoryLocationId>
                <inventoryLocationName>Cincinnati</inventoryLocationName><postalCode>45069</postalCode>
                <inventoryLocationQuantity><Quantity><uom>EA</uom><value>167</value></Quantity></inventoryLocationQuantity>
              </InventoryLocation>
            </InventoryLocationArray>
          </PartInventory>
        </PartInventoryArray>
      </Inventory>
    </ns2:GetInventoryLevelsResponse>
  </S:Body>
</S:Envelope>"""


def test_inventory_levels() -> None:
    res = _client(INV_XML).get_inventory_levels("K420")
    assert len(res.parts) == 1
    p = res.parts[0]
    assert p.part_id == "92032" and p.color == "Black" and p.size == "S"
    assert p.total_available == 1045
    assert len(p.warehouses) == 2
    assert p.warehouses[0].warehouse_name == "Seattle" and p.warehouses[0].quantity == 0
    assert p.warehouses[1].warehouse_name == "Cincinnati" and p.warehouses[1].quantity == 167
    print("PASS test_inventory_levels")


# --- 4. Fixed-width Daily Invoice file (FTP Guide 23.1 p22) ---
def _fw_line(**vals: str) -> str:
    from feed_parsers import _INVOICE_FIELDS

    buf = [" "] * 332
    for name, start, end in _INVOICE_FIELDS:
        v = vals.get(name, "")[: end - start + 1]
        buf[start - 1 : start - 1 + len(v)] = list(v)
    return "".join(buf)


def test_fixedwidth_invoice() -> None:
    # Values sized to the guide's documented field widths (its own example
    # values are illustrative and exceed the stated widths).
    line1 = _fw_line(
        account_number="0000123456", account_name="Company Name",
        invoice_number="058316700", invoice_date="2019-06-18", po_number="PO NUMBER",
        order_date="2019-06-18", due_date="2019-07-18", terms="NET 30",
        unique_key="709802", style="K500", color="Light Blue",
        description="PA SILK TOUCH POLO", size="M", pieces="000002",
        price="0000007.49", amount="0000014.98", sales_tax="0000000.00",
        shipping_handling="0000003.50", total="0000018.48",
        invoice_total="0000018.48", sales_order_number="012345678",
    )
    line2 = _fw_line(
        account_number="0000123456", invoice_number="058316700",
        po_number="PO NUMBER", unique_key="709803", style="K500", color="Light Blue",
        description="PA SILK TOUCH POLO", size="L", pieces="000001",
        price="0000007.49", amount="0000007.49", invoice_total="0000018.48",
        sales_order_number="012345678",
    )
    invoices = parse_daily_invoice_fixedwidth(line1 + "\n" + line2)
    assert len(invoices) == 1, len(invoices)
    inv = invoices[0]
    assert inv.invoice_number == "058316700"
    assert inv.po_number == "PO NUMBER"
    assert inv.total_amount == 18.48
    assert inv.sales_tax == 0.0
    assert inv.shipping_handling == 3.5
    assert len(inv.lines) == 2
    assert inv.lines[0].style == "K500" and inv.lines[0].size == "M"
    assert inv.lines[0].quantity == 2 and inv.lines[0].unit_price == 7.49
    assert inv.sub_total == 22.47  # 14.98 + 7.49
    assert inv.to_common()["po_number"] == "PO NUMBER"
    print("PASS test_fixedwidth_invoice")


# --- 5. EDI-810 (FTP Guide 23.1 p24) ---
EDI = (
    "ST*810*1141379~BIG*20130628*44209995*20130628****CN*00~CUR*BY*USD~"
    "N1*BY*Company Name~"
    "IT1*1*3*EA*9.99*PE*VN*167592*ZZ*K420 - Athletic Gold - S~"
    "PID*F****PA Pique Knit Polos Athletic Gold S~"
    "IT1*2*10*EA*9.99*PE*VN*216181*ZZ*K420 - Blueberry - XS~"
    "TDS*13317~TXI*ZZ*13.31~CTT*2~SE*10*1141379~"
)


def test_edi810() -> None:
    invoices = parse_edi810(EDI)
    assert len(invoices) == 1, len(invoices)
    inv = invoices[0]
    assert inv.invoice_number == "44209995"
    assert inv.invoice_date == "2013-06-28"
    assert inv.total_amount == 133.17
    assert inv.sales_tax == 13.31
    assert len(inv.lines) == 2
    assert inv.lines[0].style == "K420" and inv.lines[0].color == "Athletic Gold"
    assert inv.lines[0].size == "S" and inv.lines[0].quantity == 3
    assert inv.lines[0].unique_key == "167592" and inv.lines[0].unit_price == 9.99
    print("PASS test_edi810")


# --- 6. Shipment status ASN (FTP Guide 23.1 p21) ---
def test_shipment_status() -> None:
    cols = [
        "123456", "18367163", "WEST CHESTER, OH", "11/20/2015", "ABC CO", "JOHN DOE",
        "123 MAIN ST", "Suite 102", "LONG ISLAND CITY", "NY", "11101", "USA",
        "8.7", "8.4", "3.95", "56.84", "1ZE435930310783934", "1", "Not Used", "1",
        "2400B", "GILDAN 100% YOUTH L/S WHITE", "White", "L", "3", "25852", "4", "LP0002488302",
    ]
    rows = parse_shipment_status("\t".join(cols))
    assert len(rows) == 1
    r = rows[0]
    assert r.customer_po == "123456" and r.sales_order_number == "18367163"
    assert r.tracking_number == "1ZE435930310783934"
    assert r.invoice_total == 56.84 and r.freight == 8.4
    assert r.style == "2400B" and r.color == "White" and r.size == "L" and r.quantity == 3
    assert r.inventory_key == "25852" and r.size_index == "4" and r.lpn == "LP0002488302"
    print("PASS test_shipment_status")


# --- 7. Inventory feed dip.txt (FTP Guide 23.1 p15) ---
def test_inventory_feed() -> None:
    # Inventory_Key|Size_Index|Catalog_No|Catalog_Color|Size|Whse_No|Quantity|Piece_Weight|
    # Piece_Price|Dozens_Price|Case_Price|Case_Size|... |Unique_key(18)|...
    row = "9203|2|K420|Black|S|3|179|0.5|9.99|9.99|8.5|72|||||| 9203-2 |M"
    row = "9203|2|K420|Black|S|3|179|0.5|9.99|9.99|8.5|72|0|0|0|||92032|M"
    rows = parse_inventory_feed(row, style_filter="K420")
    assert len(rows) == 1
    r = rows[0]
    assert r.inventory_key == "9203" and r.size_index == "2"
    assert r.style == "K420" and r.color == "Black" and r.size == "S"
    assert r.warehouse_no == "3" and r.quantity == 179
    assert r.piece_price == 9.99 and r.case_price == 8.5 and r.case_size == 72
    assert r.unique_key == "92032"
    # style filter excludes other styles
    assert parse_inventory_feed(row, style_filter="ZZZ") == []
    print("PASS test_inventory_feed")


if __name__ == "__main__":
    test_invoice_soap()
    test_invoice_single_root()
    test_tracking()
    test_inventory_levels()
    test_fixedwidth_invoice()
    test_edi810()
    test_shipment_status()
    test_inventory_feed()
    print("\nALL TESTS PASSED")
