"""SanMar SOAP client.

Encapsulates the raw SOAP/XML mechanics for the SanMar web services
the SME skill calls. Extracted from a working Odoo integration but
purged of Odoo-specific concerns (ORM, env, recordsets, credential
vault). Auth is provided per-call via :class:`SanMarCredentials`.

Endpoints, namespaces, operation names, payload shapes, and error
parsing match SanMar's published SOAP services as observed in
production traffic.
"""

from __future__ import annotations

import logging
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from xml.sax.saxutils import escape as _xml_escape

import requests

from schemas import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    CartValidationLineError,
    CartValidationResult,
    InventoryLevelPart,
    InventoryLevelsResult,
    InventoryResult,
    Invoice,
    InvoiceAddress,
    InvoiceLine,
    InvoiceResult,
    OrderStatusResult,
    PricingItem,
    PricingLine,
    PricingResult,
    ProductSearchResult,
    ProductVariant,
    PurchaseOrderDraft,
    PurchaseOrderResult,
    SanMarCredentials,
    TrackingItem,
    TrackingResult,
    TrackingShipment,
    WarehouseQuantity,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SanMarError(Exception):
    """Base class for SanMar skill errors."""

    surface = "sanmar"
    operation = ""
    retryable = False

    def to_dict(self) -> dict[str, object]:
        return {
            "status": "error",
            "surface": self.surface,
            "operation": self.operation,
            "message": str(self),
            "retryable": self.retryable,
        }


class SanMarConfigError(SanMarError):
    """Missing or invalid configuration (credentials, environment)."""


class SanMarTransportError(SanMarError):
    """Network / HTTP failure talking to SanMar."""

    retryable = True


class SanMarAPIError(SanMarError):
    """SanMar returned a SOAP fault or errorOccurred=true."""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SanMarEndpoints:
    pricing: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarPricingServicePort"
    )
    product_info: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarProductInfoServicePort"
    )
    inventory: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarWebServicePort"
    )
    po_submit_prod: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarPOServicePort"
    )
    po_submit_dev: str = (
        "https://test-ws.sanmar.com:8080/SanMarWebService/SanMarPOServicePort"
    )
    order_status: str = (
        "https://ws.sanmar.com:8080/promostandards/OrderShipmentNotificationServiceBinding"
    )
    inventory_promo: str = (
        "https://ws.sanmar.com:8080/promostandards/InventoryServiceBinding"
    )
    invoice_prod: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/InvoicePort"
    )
    invoice_dev: str = (
        "https://test-ws.sanmar.com:8080/SanMarWebService/InvoicePort"
    )

    def po_url(self, environment: str) -> str:
        return self.po_submit_dev if environment == "development" else self.po_submit_prod

    def invoice_url(self, environment: str) -> str:
        return self.invoice_dev if environment == "development" else self.invoice_prod


# Namespace constants used by SanMar's WSDLs.
_NS_SOAPENV = "http://schemas.xmlsoap.org/soap/envelope/"
_NS_WEB = "http://webservice.integration.sanmar.com/"  # PO/inventory binding
_NS_IMPL = "http://impl.webservice.integration.sanmar.com/"  # pricing/product binding
_NS_PROMO = (
    "http://www.promostandards.org/WSDL/OrderShipmentNotificationService/1.0.0/"
)
_NS_PROMO_SHARED = (
    "http://www.promostandards.org/WSDL/OrderShipmentNotificationService/1.0.0/SharedObjects/"
)
_NS_INV = "http://www.promostandards.org/WSDL/Inventory/2.0.0/"  # PromoStandards inventory v2
_NS_INV_SHARED = "http://www.promostandards.org/WSDL/Inventory/2.0.0/SharedObjects/"


def credentials_from_env() -> SanMarCredentials:
    """Optional fallback: load credentials from SANMAR_* env vars.

    The supported runtime pattern is for the agent to collect
    credentials from the user and pass an explicit
    :class:`SanMarCredentials` object into every tool call. This
    helper is the optional cache layer — used only when the caller
    did not pass credentials directly. Raises
    :class:`SanMarConfigError` if no env-var fallback is configured;
    the agent should treat that error as a signal to ask the user.
    """

    customer_number = os.getenv("SANMAR_CUSTOMER_NUMBER", "").strip()
    username = os.getenv("SANMAR_USERNAME", "").strip()
    password = os.getenv("SANMAR_PASSWORD", "").strip()
    environment = os.getenv("SANMAR_ENV", "production").strip() or "production"

    missing = [
        name
        for name, value in (
            ("customer_number", customer_number),
            ("username", username),
            ("password", password),
        )
        if not value
    ]
    if missing:
        raise SanMarConfigError(
            "SanMar web-service credentials were not provided. "
            "Ask the user for "
            + ", ".join(missing)
            + " and supply them either via the SANMAR_CUSTOMER_NUMBER / "
            "SANMAR_USERNAME / SANMAR_PASSWORD environment variables or as "
            "credential fields (customer_number, username, password) in the "
            "tool's stdin JSON."
        )

    return SanMarCredentials(
        customer_number=customer_number,
        username=username,
        password=password,
        environment=environment,
    )


# ---------------------------------------------------------------------------
# Carrier normalization (extracted from Odoo SanMarIntegration._normalize_carrier)
# ---------------------------------------------------------------------------


def normalize_carrier(raw_carrier: str | None) -> str | None:
    """Map SanMar carrier strings to canonical ids: fedex|ups|usps|None."""

    if not raw_carrier:
        return None
    c = raw_carrier.strip().lower()
    if "fedex" in c or "fed ex" in c:
        return "fedex"
    if "ups" in c:
        return "ups"
    if "usps" in c or "united states postal" in c:
        return "usps"
    return None


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class SanMarClient:
    """Raw SanMar SOAP client.

    The client owns endpoint config, an HTTP session, retry behavior,
    and SOAP envelope construction. It does not validate domain
    semantics — callers should use the agent-facing tools in
    ``sanmar_tools`` (exposed via ``scripts/sanmar.py``).
    """

    def __init__(
        self,
        credentials: SanMarCredentials | None = None,
        endpoints: SanMarEndpoints | None = None,
        timeout: int = 30,
        session: requests.Session | None = None,
    ) -> None:
        self.credentials = credentials or credentials_from_env()
        self.endpoints = endpoints or SanMarEndpoints()
        self.timeout = timeout
        self._session = session or requests.Session()

    # ------------------------------------------------------------------
    # Low-level HTTP
    # ------------------------------------------------------------------

    def _post_soap(
        self, url: str, payload: str | bytes, soap_action: str, *, operation: str
    ) -> str:
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": soap_action,
        }
        try:
            response = self._session.post(
                url, data=payload, headers=headers, timeout=self.timeout
            )
        except requests.RequestException as exc:
            err = SanMarTransportError(f"Transport error calling {url}: {exc}")
            err.operation = operation
            raise err from exc

        if response.status_code >= 500:
            err = SanMarTransportError(
                f"Upstream {response.status_code} for {operation}: {response.text[:200]}"
            )
            err.operation = operation
            raise err

        if not response.ok:
            err = SanMarAPIError(
                f"HTTP {response.status_code} for {operation}: {response.text[:300]}"
            )
            err.operation = operation
            raise err

        return response.text

    @staticmethod
    def _check_soap_error(root: ET.Element, operation: str) -> None:
        """SanMar surfaces business errors via <errorOccurred> *and*
        the typo'd <errorOccured> (product info port only).

        Raises :class:`SanMarAPIError` if the response signals an error.
        """

        for tag in ("errorOccurred", "errorOccured"):
            el = root.find(f".//{tag}")
            if el is not None and el.text and el.text.strip().lower() == "true":
                msg_el = root.find(".//message")
                msg = msg_el.text if msg_el is not None and msg_el.text else "Unknown error"
                err = SanMarAPIError(msg)
                err.operation = operation
                raise err

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def get_inventory(self, style: str, color: str, size: str) -> InventoryResult:
        creds = self.credentials
        payload = (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:web="{_NS_WEB}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<web:getInventoryQtyForStyleColorSize>"
            f"<arg0>{creds.customer_number}</arg0>"
            f"<arg1>{creds.username}</arg1>"
            f"<arg2>{creds.password}</arg2>"
            f"<arg3>{style}</arg3>"
            f"<arg4>{color}</arg4>"
            f"<arg5>{size}</arg5>"
            "</web:getInventoryQtyForStyleColorSize>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )
        text = self._post_soap(
            self.endpoints.inventory,
            payload,
            soap_action="getInventoryQtyForStyleColorSize",
            operation="getInventoryQtyForStyleColorSize",
        )
        root = ET.fromstring(text)
        self._check_soap_error(root, "getInventoryQtyForStyleColorSize")

        warehouse_qtys: list[int] = []
        for el in root.findall(".//listResponse"):
            try:
                warehouse_qtys.append(int((el.text or "0").strip()))
            except ValueError:
                continue

        # Reference implementation treats availability as the maximum
        # single-warehouse quantity (SanMar's API returns per-warehouse
        # totals; a single shipment ships from one warehouse).
        total = max(warehouse_qtys) if warehouse_qtys else 0
        return InventoryResult(
            style=style,
            color=color,
            size=size,
            warehouse_quantities=warehouse_qtys,
            total_available=total,
        )

    # ------------------------------------------------------------------
    # Pricing
    # ------------------------------------------------------------------

    def get_pricing(self, lines: list[PricingLine]) -> PricingResult:
        if not lines:
            return PricingResult(items=[])

        creds = self.credentials
        arg0_chunks = "".join(
            f"<arg0><color>{ln.color}</color><size>{ln.size}</size>"
            f"<style>{ln.style}</style></arg0>"
            for ln in lines
        )
        payload = (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:impl="{_NS_IMPL}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<impl:getPricing>"
            f"{arg0_chunks}"
            "<arg1>"
            f"<sanMarCustomerNumber>{creds.customer_number}</sanMarCustomerNumber>"
            f"<sanMarUserName>{creds.username}</sanMarUserName>"
            f"<sanMarUserPassword>{creds.password}</sanMarUserPassword>"
            "</arg1>"
            "</impl:getPricing>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )
        text = self._post_soap(
            self.endpoints.pricing,
            payload,
            soap_action="getPricing",
            operation="getPricing",
        )
        root = ET.fromstring(text)
        self._check_soap_error(root, "getPricing")

        items: list[PricingItem] = []
        for resp in root.findall(".//listResponse"):
            items.append(
                PricingItem(
                    style=_text(resp, "style"),
                    color=_text(resp, "color"),
                    size=_text(resp, "size"),
                    inventory_key=_text_or_none(resp, "inventoryKey"),
                    size_index=_text_or_none(resp, "sizeIndex"),
                    piece_price=_float_or_none(resp, "piecePrice"),
                    dozen_price=_float_or_none(resp, "dozenPrice"),
                    case_price=_float_or_none(resp, "casePrice"),
                    my_price=_float_or_none(resp, "myPrice"),
                    sale_piece_price=_float_or_none(resp, "salePiecePrice"),
                    sale_dozen_price=_float_or_none(resp, "saleDozenPrice"),
                    sale_case_price=_float_or_none(resp, "saleCasePrice"),
                )
            )
        return PricingResult(items=items)

    # ------------------------------------------------------------------
    # Product info / catalog search
    # ------------------------------------------------------------------

    def search_products(
        self, style: str, color: str | None = None, size: str | None = None
    ) -> ProductSearchResult:
        creds = self.credentials
        arg0_inner = f"<style>{style}</style>"
        if color:
            arg0_inner += f"<color>{color}</color>"
        if size:
            arg0_inner += f"<size>{size}</size>"

        payload = (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:impl="{_NS_IMPL}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<impl:getProductInfoByStyleColorSize>"
            f"<arg0>{arg0_inner}</arg0>"
            "<arg1>"
            f"<sanMarCustomerNumber>{creds.customer_number}</sanMarCustomerNumber>"
            f"<sanMarUserName>{creds.username}</sanMarUserName>"
            f"<sanMarUserPassword>{creds.password}</sanMarUserPassword>"
            "</arg1>"
            "</impl:getProductInfoByStyleColorSize>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )

        text = self._post_soap(
            self.endpoints.product_info,
            payload,
            soap_action="getProductInfoByStyleColorSize",
            operation="getProductInfoByStyleColorSize",
        )
        root = ET.fromstring(text)

        # Product info port emits the typo'd <errorOccured>. Also map
        # "Invalid style specified" to an empty result rather than an
        # error, matching the reference implementation.
        for tag in ("errorOccurred", "errorOccured"):
            el = root.find(f".//{tag}")
            if el is not None and el.text and el.text.strip().lower() == "true":
                msg_el = root.find(".//message")
                msg = msg_el.text if msg_el is not None and msg_el.text else "Unknown error"
                if "Invalid style specified" in msg:
                    return ProductSearchResult(style=style, title=None)
                err = SanMarAPIError(msg)
                err.operation = "getProductInfoByStyleColorSize"
                raise err

        title: str | None = None
        weight: float | None = None
        image: str | None = None
        colors: set[str] = set()
        sizes: set[str] = set()
        variants: list[ProductVariant] = []

        for resp in root.findall(".//listResponse"):
            basic = resp.find("productBasicInfo") or resp
            img_info = resp.find("productImageInfo")
            price_info = resp.find("productPriceInfo")

            v_color = _text(basic, "color")
            v_size = _text(basic, "size")
            v_title = _text_or_none(basic, "productTitle")
            v_weight = _float_or_none(basic, "pieceWeight")
            v_image = (
                _text_or_none(img_info, "colorProductImage") if img_info is not None else None
            )
            v_piece_price = (
                _float_or_none(price_info, "piecePrice") if price_info is not None else None
            )
            unique_key = _text_or_none(basic, "uniqueKey")
            inventory_key = _text_or_none(basic, "inventoryKey")
            size_index = _text_or_none(basic, "sizeIndex")

            if title is None and v_title:
                title = v_title.replace(f" {style}", "").strip()
            if weight is None and v_weight is not None:
                weight = v_weight
            if image is None and v_image:
                image = v_image
            if v_color:
                colors.add(v_color)
            if v_size:
                sizes.add(v_size)

            variants.append(
                ProductVariant(
                    style=style,
                    color=v_color,
                    size=v_size,
                    unique_key=unique_key,
                    inventory_key=inventory_key,
                    size_index=size_index,
                    image=v_image,
                    piece_price=v_piece_price,
                )
            )

        return ProductSearchResult(
            style=style,
            title=title,
            weight=weight,
            image=image,
            colors=sorted(colors),
            sizes=sorted(sizes),
            variants=variants,
        )

    # ------------------------------------------------------------------
    # Purchase orders
    # ------------------------------------------------------------------

    def build_po_envelope(self, draft: PurchaseOrderDraft, *, pre_submit: bool) -> bytes:
        """Build the SOAP envelope for ``submitPO`` or ``getPreSubmitInfo``.

        Pre-submit lines only need style/color/size/quantity. Submit
        lines must include inventoryKey and sizeIndex (typically
        obtained by calling :meth:`get_pricing` first).

        Implemented with the stdlib ElementTree so the skill has no
        dependency beyond ``requests``.
        """

        creds = self.credentials

        # Register prefixes so the serialized envelope reads as
        # <soapenv:...> / <web:...> instead of ns0/ns1. SanMar accepts
        # any well-formed prefix, but matching the original guide
        # keeps debugging readable.
        ET.register_namespace("soapenv", _NS_SOAPENV)
        ET.register_namespace("web", _NS_WEB)

        envelope = ET.Element(f"{{{_NS_SOAPENV}}}Envelope")
        ET.SubElement(envelope, f"{{{_NS_SOAPENV}}}Header")
        body = ET.SubElement(envelope, f"{{{_NS_SOAPENV}}}Body")
        op_tag = "getPreSubmitInfo" if pre_submit else "submitPO"
        op = ET.SubElement(body, f"{{{_NS_WEB}}}{op_tag}")

        ship_to = draft.ship_to
        arg0 = ET.SubElement(op, "arg0")
        ET.SubElement(arg0, "attention").text = ship_to.attention or ship_to.name
        ET.SubElement(arg0, "notes").text = ship_to.notes or ""
        ET.SubElement(arg0, "poNum").text = draft.po_number
        ET.SubElement(arg0, "shipTo").text = ship_to.name
        ET.SubElement(arg0, "shipAddress1").text = ship_to.address1
        ET.SubElement(arg0, "shipAddress2").text = ship_to.address2 or ""
        ET.SubElement(arg0, "shipCity").text = ship_to.city
        ET.SubElement(arg0, "shipState").text = ship_to.state
        ET.SubElement(arg0, "shipZip").text = ship_to.zip
        ET.SubElement(arg0, "shipMethod").text = ship_to.ship_method or "UPS"
        ET.SubElement(arg0, "shipEmail").text = ship_to.email or ""
        ET.SubElement(arg0, "residence").text = ship_to.residence or "N"

        for line in draft.lines:
            detail = ET.SubElement(arg0, "webServicePoDetailList")
            if not pre_submit:
                # Submit requires inventoryKey + sizeIndex from getPricing.
                if line.inventory_key:
                    ET.SubElement(detail, "inventoryKey").text = line.inventory_key
                if line.size_index:
                    ET.SubElement(detail, "sizeIndex").text = line.size_index
            ET.SubElement(detail, "style").text = line.style
            ET.SubElement(detail, "color").text = line.color
            ET.SubElement(detail, "size").text = line.size
            ET.SubElement(detail, "quantity").text = str(int(line.quantity))

        arg1 = ET.SubElement(op, "arg1")
        ET.SubElement(arg1, "sanMarCustomerNumber").text = creds.customer_number
        ET.SubElement(arg1, "sanMarUserName").text = creds.username
        ET.SubElement(arg1, "sanMarUserPassword").text = creds.password

        return ET.tostring(envelope, encoding="utf-8", xml_declaration=True)

    def pre_submit_po(self, draft: PurchaseOrderDraft) -> CartValidationResult:
        payload = self.build_po_envelope(draft, pre_submit=True)
        text = self._post_soap(
            self.endpoints.po_url(self.credentials.environment),
            payload,
            soap_action="getPreSubmitInfo",
            operation="getPreSubmitInfo",
        )
        root = ET.fromstring(text)

        # Per-line errors come back inside webServicePoDetailList.
        errored: list[CartValidationLineError] = []
        for detail in root.findall(".//webServicePoDetailList"):
            err_el = detail.find(".//errorOccured")
            if err_el is None:
                err_el = detail.find(".//errorOccurred")
            if err_el is not None and err_el.text and err_el.text.strip().lower() == "true":
                errored.append(
                    CartValidationLineError(
                        style=_text(detail, "style"),
                        color=_text(detail, "color"),
                        size=_text(detail, "size"),
                        message=_text_or_none(detail, "message") or "Unknown error",
                    )
                )

        # Top-level error (auth / schema)
        try:
            self._check_soap_error(root, "getPreSubmitInfo")
        except SanMarAPIError:
            if not errored:
                raise

        return CartValidationResult(ok=not errored, errored_lines=errored)

    def submit_po(self, draft: PurchaseOrderDraft) -> PurchaseOrderResult:
        payload = self.build_po_envelope(draft, pre_submit=False)
        text = self._post_soap(
            self.endpoints.po_url(self.credentials.environment),
            payload,
            soap_action="submitPO",
            operation="submitPO",
        )
        root = ET.fromstring(text)
        self._check_soap_error(root, "submitPO")

        sanmar_ref = _text_or_none(root, "poNum")
        return PurchaseOrderResult(
            status="submitted",
            po_number=draft.po_number,
            sanmar_reference=sanmar_ref,
            raw_payload=payload.decode("utf-8") if isinstance(payload, bytes) else payload,
            raw_response=text,
        )

    # ------------------------------------------------------------------
    # PromoStandards order shipment notification
    # ------------------------------------------------------------------

    def _shipment_notification_payload(
        self,
        *,
        query_type: str,
        reference_number: str | None = None,
        shipment_date: str | None = None,
    ) -> str:
        creds = self.credentials
        if query_type == "3":
            selector = (
                f"<ns:shipmentDateTimeStamp>{_xml_escape(shipment_date or '')}"
                "</ns:shipmentDateTimeStamp>"
            )
        else:
            selector = (
                f"<ns:referenceNumber>{_xml_escape(reference_number or '')}"
                "</ns:referenceNumber>"
            )
        return (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:ns="{_NS_PROMO}" '
            f'xmlns:shar="{_NS_PROMO_SHARED}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<ns:GetOrderShipmentNotificationRequest>"
            "<shar:wsVersion>1.0.0</shar:wsVersion>"
            f"<shar:id>{_xml_escape(creds.username)}</shar:id>"
            f"<shar:password>{_xml_escape(creds.password)}</shar:password>"
            f"<ns:queryType>{query_type}</ns:queryType>"
            f"{selector}"
            "</ns:GetOrderShipmentNotificationRequest>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )

    def get_shipment_notification(
        self,
        *,
        query_type: str = "1",
        reference_number: str | None = None,
        shipment_date: str | None = None,
    ) -> ET.Element | None:
        """Raw OSN SOAP call. Returns the parsed XML root or ``None`` if
        SanMar responded with a service-level error message.

        ``query_type`` — ``"1"`` = customer purchase-order number,
        ``"2"`` = SanMar sales-order number, ``"3"`` =
        ``shipmentDateTimeStamp`` (UTC, 7-day max window).
        """

        text = self._post_soap(
            self.endpoints.order_status,
            self._shipment_notification_payload(
                query_type=query_type,
                reference_number=reference_number,
                shipment_date=shipment_date,
            ),
            soap_action="getOrderShipmentNotification",
            operation="GetOrderShipmentNotificationRequest",
        )
        root = ET.fromstring(text)
        ns = {"ns2": _NS_PROMO}
        err_el = root.find(".//ns2:errorMessage", namespaces=ns)
        if err_el is not None and err_el.text:
            logger.warning(
                "SanMar OSN error for %s: %s",
                reference_number or shipment_date,
                err_el.text,
            )
            return None
        return root

    def get_tracking(
        self,
        po_number: str | None = None,
        *,
        sales_order_number: str | None = None,
        shipment_date: str | None = None,
    ) -> TrackingResult:
        """Tracking detail for a PO (default), a SanMar sales-order number,
        or a shipment date/time.

        Returns one :class:`TrackingShipment` per shipped package, each
        carrying the tracking number, normalized carrier, ship method,
        ship date, the SanMar sales order it belongs to, ship-from/to
        city+state, and the items in the box.
        """

        if sales_order_number:
            query_type, reference = "2", sales_order_number
        elif shipment_date:
            query_type, reference = "3", None
        else:
            query_type, reference = "1", po_number
        label = po_number or sales_order_number or shipment_date or ""

        root = self.get_shipment_notification(
            query_type=query_type,
            reference_number=reference,
            shipment_date=shipment_date,
        )
        if root is None:
            return TrackingResult(po_number=label, shipments=[])

        ns = {"ns2": _NS_PROMO, "shar": _NS_PROMO_SHARED}
        osn = root.find(".//ns2:OrderShipmentNotification", namespaces=ns)
        complete: bool | None = None
        if osn is not None:
            c = osn.find("ns2:complete", namespaces=ns)
            complete = (
                c.text.strip().lower() == "true" if c is not None and c.text else None
            )

        shipments: list[TrackingShipment] = []
        for so in root.findall(".//ns2:SalesOrder", namespaces=ns):
            son = _child_text(so, "ns2:salesOrderNumber", ns) or None
            for loc in so.findall(".//ns2:ShipmentLocation", namespaces=ns):
                ship_from = loc.find("ns2:ShipFromAddress", namespaces=ns)
                ship_to = loc.find("ns2:ShipToAddress", namespaces=ns)
                for pkg in loc.findall("ns2:PackageArray/ns2:Package", namespaces=ns):
                    tracking = _child_text(pkg, "ns2:trackingNumber", ns)
                    if not tracking:
                        continue
                    items = [
                        TrackingItem(
                            style=_child_text(it, "ns2:supplierProductId", ns),
                            part_id=_child_text(it, "ns2:supplierPartId", ns),
                            quantity=_child_int(it, "ns2:quantity", ns),
                        )
                        for it in pkg.findall("ns2:ItemArray/ns2:Item", namespaces=ns)
                    ]
                    shipments.append(
                        TrackingShipment(
                            tracking_number=tracking,
                            carrier=normalize_carrier(
                                _child_text(pkg, "ns2:carrier", ns) or None
                            ),
                            shipment_method=_child_text(pkg, "ns2:shipmentMethod", ns)
                            or None,
                            ship_date=_child_text(pkg, "ns2:shipmentDate", ns) or None,
                            sales_order_number=son,
                            ship_from_city=_addr_part(ship_from, "city", ns),
                            ship_from_state=_addr_part(ship_from, "region", ns),
                            ship_to_city=_addr_part(ship_to, "city", ns),
                            ship_to_state=_addr_part(ship_to, "region", ns),
                            items=items,
                        )
                    )
        return TrackingResult(po_number=label, complete=complete, shipments=shipments)

    def get_order_status(self, po_number: str) -> OrderStatusResult:
        root = self.get_shipment_notification(query_type="1", reference_number=po_number)
        if root is None:
            return OrderStatusResult(po_number=po_number, status="unknown")

        ns = {"ns2": _NS_PROMO}
        sales_order = root.find(".//ns2:salesOrderNumber", namespaces=ns)
        sanmar_order_number = (
            sales_order.text.strip() if sales_order is not None and sales_order.text else None
        )
        package_count = len(root.findall(".//ns2:Package", namespaces=ns))
        status = "shipped" if package_count else ("submitted" if sanmar_order_number else "unknown")
        return OrderStatusResult(
            po_number=po_number,
            sanmar_order_number=sanmar_order_number,
            shipment_count=package_count,
            status=status,
        )

    # ------------------------------------------------------------------
    # PromoStandards inventory levels (v2.0.0 — per-warehouse breakdown)
    # ------------------------------------------------------------------

    def _inventory_levels_payload(
        self, style: str, part_ids: list[str] | None
    ) -> str:
        creds = self.credentials
        filt = ""
        if part_ids:
            parts = "".join(
                f"<shar:partId>{_xml_escape(str(p))}</shar:partId>" for p in part_ids
            )
            filt = f"<shar:Filter><shar:partIdArray>{parts}</shar:partIdArray></shar:Filter>"
        return (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:ns="{_NS_INV}" xmlns:shar="{_NS_INV_SHARED}">'
            "<soapenv:Header/><soapenv:Body>"
            "<ns:GetInventoryLevelsRequest>"
            "<shar:wsVersion>2.0.0</shar:wsVersion>"
            f"<shar:id>{_xml_escape(creds.username)}</shar:id>"
            f"<shar:password>{_xml_escape(creds.password)}</shar:password>"
            f"<shar:productId>{_xml_escape(style)}</shar:productId>"
            f"{filt}"
            "</ns:GetInventoryLevelsRequest>"
            "</soapenv:Body></soapenv:Envelope>"
        )

    def get_inventory_levels(
        self, style: str, part_ids: list[str] | None = None
    ) -> InventoryLevelsResult:
        """PromoStandards getInventoryLevels v2.0.0 — named per-warehouse
        availability for a style (optionally filtered to specific partIds).
        """

        if not style:
            raise SanMarConfigError("style is required")
        text = self._post_soap(
            self.endpoints.inventory_promo,
            self._inventory_levels_payload(style, part_ids),
            soap_action="getInventoryLevels",
            operation="getInventoryLevels",
        )
        root = ET.fromstring(text)
        err = _promo_service_error(root)
        if err:
            e = SanMarAPIError(err)
            e.operation = "getInventoryLevels"
            raise e

        ns = {"shar": _NS_INV_SHARED}
        parts: list[InventoryLevelPart] = []
        for pi in root.findall(".//shar:PartInventory", namespaces=ns):
            warehouses = [
                WarehouseQuantity(
                    warehouse_id=_child_text(loc, "shar:inventoryLocationId", ns),
                    warehouse_name=_child_text(loc, "shar:inventoryLocationName", ns),
                    postal_code=_child_text(loc, "shar:postalCode", ns),
                    quantity=_child_int(
                        loc,
                        "shar:inventoryLocationQuantity/shar:Quantity/shar:value",
                        ns,
                    ),
                )
                for loc in pi.findall(
                    "shar:InventoryLocationArray/shar:InventoryLocation", namespaces=ns
                )
            ]
            parts.append(
                InventoryLevelPart(
                    part_id=_child_text(pi, "shar:partId", ns),
                    color=_child_text(pi, "shar:partColor", ns),
                    size=_child_text(pi, "shar:labelSize", ns),
                    description=_child_text(pi, "shar:partDescription", ns),
                    total_available=_child_int(
                        pi, "shar:quantityAvailable/shar:Quantity/shar:value", ns
                    ),
                    warehouses=warehouses,
                )
            )
        return InventoryLevelsResult(style=style, parts=parts)

    # ------------------------------------------------------------------
    # Invoicing (SanMar Standard InvoicePort)
    # ------------------------------------------------------------------

    _INVOICE_OPS = {
        "purchase_order": "GetInvoicesByPurchaseOrderNo",
        "invoice_number": "GetInvoiceByInvoiceNo",
        "invoice_date_range": "GetInvoicesByInvoiceDateRange",
        "order_date": "GetInvoicesByOrderDate",
        "unpaid": "GetUnpaidInvoices",
    }
    _INVOICE_HEADER_OPS = {
        "purchase_order": "GetInvoicesHeaderByPurchaseOrderNo",
        "invoice_date_range": "GetInvoicesHeaderByInvoiceDateRange",
        "order_date": "GetInvoicesHeaderByOrderDate",
        "unpaid": "GetUnpaidInvoicesHeader",
    }

    def _invoice_payload(
        self,
        operation: str,
        *,
        value: str | None,
        start_date: str | None,
        end_date: str | None,
    ) -> str:
        creds = self.credentials
        if operation in (
            "GetInvoicesByPurchaseOrderNo",
            "GetInvoicesHeaderByPurchaseOrderNo",
        ):
            selector = f"<web:PurchaseOrderNo>{_xml_escape(str(value))}</web:PurchaseOrderNo>"
        elif operation == "GetInvoiceByInvoiceNo":
            selector = f"<web:InvoiceNo>{_xml_escape(str(value))}</web:InvoiceNo>"
        elif operation in (
            "GetInvoicesByInvoiceDateRange",
            "GetInvoicesHeaderByInvoiceDateRange",
        ):
            selector = (
                f"<web:StartDate>{_xml_escape(str(start_date))}</web:StartDate>"
                f"<web:EndDate>{_xml_escape(str(end_date))}</web:EndDate>"
            )
        elif operation in ("GetInvoicesByOrderDate", "GetInvoicesHeaderByOrderDate"):
            selector = f"<web:Date>{_xml_escape(str(value))}</web:Date>"
        else:  # GetUnpaidInvoices / GetUnpaidInvoicesHeader
            selector = ""
        return (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" xmlns:web="{_NS_WEB}">'
            "<soapenv:Header/><soapenv:Body>"
            f"<web:{operation}>"
            # NOTE: InvoicePort uses CustomerNo / UserName / Password — distinct
            # from the sanMar* auth field names on the other standard ports.
            f"<web:CustomerNo>{_xml_escape(creds.customer_number)}</web:CustomerNo>"
            f"<web:UserName>{_xml_escape(creds.username)}</web:UserName>"
            f"<web:Password>{_xml_escape(creds.password)}</web:Password>"
            f"{selector}"
            f"</web:{operation}>"
            "</soapenv:Body></soapenv:Envelope>"
        )

    def get_invoices(
        self,
        *,
        query_type: str,
        value: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        headers_only: bool = False,
    ) -> InvoiceResult:
        """SanMar Standard Invoicing (``InvoicePort``).

        ``query_type`` ∈ ``purchase_order`` | ``invoice_number`` |
        ``invoice_date_range`` | ``order_date`` | ``unpaid``. Returns
        header + line items (or header-only when ``headers_only`` and the
        query type supports it). A "not found" upstream response yields an
        empty result rather than an error.
        """

        if headers_only and query_type in self._INVOICE_HEADER_OPS:
            operation = self._INVOICE_HEADER_OPS[query_type]
        else:
            operation = self._INVOICE_OPS.get(query_type)
            headers_only = False
        if operation is None:
            raise SanMarConfigError(
                f"Unknown invoice query_type {query_type!r}. Use one of: "
                + ", ".join(self._INVOICE_OPS)
            )
        if query_type in ("purchase_order", "invoice_number", "order_date") and not value:
            raise SanMarConfigError(f"query_type {query_type!r} requires a value")
        if query_type == "invoice_date_range" and not (start_date and end_date):
            raise SanMarConfigError(
                "query_type 'invoice_date_range' requires start_date and end_date "
                "(yyyy-mm-dd, max 3 months apart)"
            )

        text = self._post_soap(
            self.endpoints.invoice_url(self.credentials.environment),
            self._invoice_payload(
                operation, value=value, start_date=start_date, end_date=end_date
            ),
            soap_action=operation,
            operation=operation,
        )
        root = ET.fromstring(text)
        invoices = _parse_invoices(root)
        if not invoices:
            fault = _first_fault_text(root)
            if fault and not any(
                token in fault.lower()
                for token in ("not found", "no data", "no invoice")
            ):
                e = SanMarAPIError(fault)
                e.operation = operation
                raise e

        query_value = value
        if query_value is None and start_date:
            query_value = f"{start_date}..{end_date}"
        return InvoiceResult(
            query_type=query_type,
            query_value=str(query_value) if query_value is not None else None,
            count=len(invoices),
            invoices=invoices,
            headers_only=headers_only,
            operation=operation,
        )


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------


def _text(node: ET.Element, tag: str) -> str:
    el = node.find(f".//{tag}")
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def _text_or_none(node: ET.Element, tag: str) -> str | None:
    el = node.find(f".//{tag}")
    if el is None or el.text is None:
        return None
    text = el.text.strip()
    return text or None


def _float_or_none(node: ET.Element, tag: str) -> float | None:
    raw = _text_or_none(node, tag)
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _to_float(raw: str | None) -> float | None:
    if not raw:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _to_int(raw: str | None) -> int:
    if not raw:
        return 0
    try:
        return int(float(raw))
    except (TypeError, ValueError):
        return 0


def _child_text(node: ET.Element, path: str, ns: dict[str, str]) -> str:
    """Namespaced ``find`` returning stripped text (``""`` if absent)."""

    el = node.find(path, namespaces=ns)
    return el.text.strip() if el is not None and el.text else ""


def _child_int(node: ET.Element, path: str, ns: dict[str, str]) -> int:
    return _to_int(_child_text(node, path, ns))


def _addr_part(addr_el: ET.Element | None, tag: str, ns: dict[str, str]) -> str | None:
    """Read a PromoStandards address sub-field (SharedObjects namespace)."""

    if addr_el is None:
        return None
    el = addr_el.find(f"shar:{tag}", namespaces=ns)
    if el is None:  # fall back to an unqualified element
        el = addr_el.find(tag)
    return el.text.strip() if el is not None and el.text else None


def _localname(tag: str) -> str:
    """Strip any ``{namespace}`` prefix from an ElementTree tag."""

    return tag.rsplit("}", 1)[-1]


def _promo_service_error(root: ET.Element) -> str | None:
    """Return the description of a PromoStandards ``ServiceMessage`` whose
    severity is ``Error`` (namespace-agnostic), else ``None``."""

    for msg in root.iter():
        if _localname(msg.tag) != "ServiceMessage":
            continue
        severity = description = ""
        for child in msg:
            local = _localname(child.tag)
            if local == "severity":
                severity = (child.text or "").strip()
            elif local == "description":
                description = (child.text or "").strip()
        if severity.lower() == "error":
            return description or "Service error"
    return None


def _first_fault_text(root: ET.Element) -> str | None:
    """Return the first SOAP fault / error message text (namespace-agnostic)."""

    for el in root.iter():
        if _localname(el.tag) in ("faultstring", "faultString", "errorMessage"):
            if el.text and el.text.strip():
                return el.text.strip()
    return None


# --- Invoice response parsing (SanMar Standard InvoicePort; namespace-agnostic) ---


def _find_local(node: ET.Element | None, name: str) -> ET.Element | None:
    if node is None:
        return None
    for child in node:
        if _localname(child.tag) == name:
            return child
    return None


def _find_all_local(node: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in node if _localname(child.tag) == name]


def _text_local(node: ET.Element | None, name: str) -> str:
    child = _find_local(node, name)
    return child.text.strip() if child is not None and child.text else ""


def _parse_invoice_address(block: ET.Element | None) -> InvoiceAddress:
    if block is None:
        return InvoiceAddress()
    addr = _find_local(block, "Address")
    return InvoiceAddress(
        name=_text_local(block, "Name"),
        address1=_text_local(addr, "Address1"),
        address2=_text_local(addr, "Address2"),
        city=_text_local(addr, "City"),
        state=_text_local(addr, "State"),
        postal_code=_text_local(addr, "PostalCode"),
        country=_text_local(addr, "Country"),
    )


def _parse_invoice_line(li: ET.Element) -> InvoiceLine:
    return InvoiceLine(
        style=_text_local(li, "StyleNo"),
        color=_text_local(li, "StyleColor"),
        size=_text_local(li, "StyleSize"),
        description=_text_local(li, "StyleDescription"),
        quantity=_to_int(_text_local(li, "Quantity")),
        unit_price=_to_float(_text_local(li, "UnitPrice")),
        amount=_to_float(_text_local(li, "Amount")),
        unique_key=_text_local(li, "UniqueKey") or None,
    )


def _parse_invoices(root: ET.Element) -> list[Invoice]:
    """Parse ``<Invoice>`` elements from an InvoicePort response.

    Handles both the single ``<Invoice>`` root (GetInvoiceByInvoiceNo) and
    the ``<Invoices><Invoice>…`` wrapper (all other methods).
    """

    invoices: list[Invoice] = []
    for inv_el in [el for el in root.iter() if _localname(el.tag) == "Invoice"]:
        header = _find_local(inv_el, "Header")
        if header is None:
            continue
        misc = _find_local(header, "Miscellaneous")
        invoices.append(
            Invoice(
                invoice_number=_text_local(header, "InvoiceNo") or None,
                sales_order_number=_text_local(header, "SalesOrderNumber") or None,
                po_number=_text_local(header, "PurchaseOrderNo") or None,
                invoice_date=_text_local(header, "InvoiceDate") or None,
                order_date=_text_local(header, "OrderDate") or None,
                due_date=_text_local(header, "DueDate") or None,
                invoice_status=_text_local(header, "InvoiceStatus") or None,
                terms=_text_local(header, "Terms") or None,
                ship_via=_text_local(header, "ShipVia") or None,
                fob=_text_local(header, "FOB") or None,
                customer_number=_text_local(header, "CustomerNo") or None,
                total_cases=_to_int(_text_local(header, "TotalCases")) or None,
                total_weight=_to_float(_text_local(header, "TotalWeight")),
                sub_total=_to_float(_text_local(header, "SubTotal")),
                sales_tax=_to_float(_text_local(header, "SalesTax")),
                shipping_handling=_to_float(
                    _text_local(header, "ShippingHandlingCharges")
                ),
                total_amount=_to_float(_text_local(header, "TotalAmount")),
                freight_savings=_to_float(_text_local(misc, "FreightSavings"))
                if misc is not None
                else None,
                tracking_ids=(_text_local(misc, "TrackingIDs") or None)
                if misc is not None
                else None,
                sold_to=_parse_invoice_address(_find_local(header, "SoldTo")),
                ship_to=_parse_invoice_address(_find_local(header, "ShipTo")),
                remit_to=_parse_invoice_address(_find_local(header, "RemitTo")),
                lines=[_parse_invoice_line(li) for li in _find_all_local(inv_el, "LineItem")],
            )
        )
    return invoices
