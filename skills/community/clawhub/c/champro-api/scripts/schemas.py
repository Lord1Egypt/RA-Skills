"""Order shapes for the CHAMPRO REST API, and their JSON serialisation.

Plain dataclasses — no pydantic, no ORM — so the skill runs in any Python
3.11+ process. `to_payload()` emits CHAMPRO's exact field spellings, which are
inconsistent enough (`ShipToLastName` but `Address`, `ZIPCode` but `StateCode`)
that hand-building the dict at each call site is how typos reach production.

Two order types share one envelope and differ in which fields are legal:

* `STOCK`  — needs `ShippingMethod`, per-item `Warehouse` (or `Autowarehouse`),
             and rejects roster/decoration fields.
* `CUSTOM` — needs `LeadTime` and `ProofFileURL`, carries `TeamColor` and
             per-item `TeamName`/`PlayerName`/`PlayerNumber`, and takes no
             warehouse (CHAMPRO decides).

Mixing the two in one order is documented error 07, so `OrderType` drives
serialisation rather than merely labelling it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

STOCK = "STOCK"
CUSTOM = "CUSTOM"

PROOF_FILE_EXTENSIONS = (".pdf", ".jpg", ".jpeg", ".png")


def _clean(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


@dataclass
class OrderItem:
    """One line. Which fields apply depends on the parent order's type."""

    sku: str
    quantity: int
    # STOCK only
    warehouse: str | None = None
    # CUSTOM only
    team_name: str | None = None
    player_name: str | None = None
    player_number: str | None = None

    def to_payload(self, order_type: str) -> dict[str, Any]:
        body: dict[str, Any] = {"SKU": str(self.sku).strip().upper(), "Quantity": int(self.quantity)}
        if order_type == STOCK:
            warehouse = _clean(self.warehouse)
            if warehouse:
                body["Warehouse"] = str(warehouse).upper()
        else:
            # CHAMPRO echoes these back on every custom line; sending them as
            # explicit nulls keeps request and response shapes aligned.
            body["TeamName"] = _clean(self.team_name)
            body["PlayerName"] = _clean(self.player_name)
            body["PlayerNumber"] = _clean(self.player_number)
        return body

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrderItem":
        return cls(
            sku=str(data.get("sku") or data.get("SKU") or "").strip(),
            quantity=int(data.get("quantity") or data.get("Quantity") or 0),
            warehouse=data.get("warehouse") or data.get("Warehouse"),
            team_name=data.get("team_name") or data.get("TeamName"),
            player_name=data.get("player_name") or data.get("PlayerName"),
            player_number=data.get("player_number") or data.get("PlayerNumber"),
        )


@dataclass
class Order:
    """One CHAMPRO order: a ship-to, a type, and its lines."""

    po: str
    order_type: str
    ship_to_first_name: str
    ship_to_last_name: str
    address: str
    city: str
    state_code: str
    zip_code: str
    country_code: str = "USA"
    phone: str = ""
    address2: str | None = None
    is_residential: bool = False
    items: list[OrderItem] = field(default_factory=list)
    # STOCK
    shipping_method: str | None = None
    shipping_customer_account: str | None = None
    # CUSTOM
    lead_time: str | None = None
    proof_file_url: str | None = None
    team_color: str | None = None

    def to_payload(self) -> dict[str, Any]:
        order_type = (self.order_type or "").strip().upper()
        body: dict[str, Any] = {
            "PO": _clean(self.po),
            "OrderType": order_type,
            "ShipToLastName": _clean(self.ship_to_last_name),
            "ShipToFirstName": _clean(self.ship_to_first_name),
            "Address": _clean(self.address),
            "Address2": _clean(self.address2) or "",
            "City": _clean(self.city),
            "StateCode": _clean(self.state_code),
            "ZIPCode": _clean(self.zip_code),
            "CountryCode": _clean(self.country_code) or "USA",
            "Phone": _clean(self.phone),
            # The spec types this Boolean but its own examples send 1/0, and
            # the response echoes true/false. 1/0 is accepted by both.
            "IsResidential": 1 if self.is_residential else 0,
            "OrderItems": [item.to_payload(order_type) for item in self.items],
        }
        if order_type == STOCK:
            body["ShippingMethod"] = _clean(self.shipping_method)
            account = _clean(self.shipping_customer_account)
            if account:
                body["ShippingCustomerAccount"] = account
        else:
            body["LeadTime"] = _clean(self.lead_time)
            body["ProofFileURL"] = _clean(self.proof_file_url)
            team_color = _clean(self.team_color)
            if team_color:
                body["TeamColor"] = team_color
        return body

    @property
    def total_quantity(self) -> int:
        return sum(int(item.quantity or 0) for item in self.items)

    @property
    def product_masters(self) -> list[str]:
        """Distinct product masters implied by the lines.

        CHAMPRO SKUs prefix the product master (`JSBJ8` -> `JSBJ8GACL`), but the
        suffix length varies by configuration, so this cannot be derived by
        slicing. Resolution happens against ProductInfo in `validation.py`;
        this only reports what was supplied explicitly.
        """

        return []

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Order":
        raw_items = data.get("items") or data.get("OrderItems") or []
        residential = data.get("is_residential", data.get("IsResidential", False))
        if isinstance(residential, str):
            residential = residential.strip().lower() in ("1", "true", "yes", "y")
        return cls(
            po=str(data.get("po") or data.get("PO") or "").strip(),
            order_type=str(data.get("order_type") or data.get("OrderType") or STOCK).upper(),
            ship_to_first_name=str(
                data.get("ship_to_first_name") or data.get("ShipToFirstName") or ""
            ),
            ship_to_last_name=str(
                data.get("ship_to_last_name") or data.get("ShipToLastName") or ""
            ),
            address=str(data.get("address") or data.get("Address") or ""),
            address2=data.get("address2") or data.get("Address2"),
            city=str(data.get("city") or data.get("City") or ""),
            state_code=str(data.get("state_code") or data.get("StateCode") or ""),
            zip_code=str(data.get("zip_code") or data.get("ZIPCode") or ""),
            country_code=str(data.get("country_code") or data.get("CountryCode") or "USA"),
            phone=str(data.get("phone") or data.get("Phone") or ""),
            is_residential=bool(residential),
            items=[OrderItem.from_dict(i) for i in raw_items],
            shipping_method=data.get("shipping_method") or data.get("ShippingMethod"),
            shipping_customer_account=(
                data.get("shipping_customer_account") or data.get("ShippingCustomerAccount")
            ),
            lead_time=data.get("lead_time") or data.get("LeadTime"),
            proof_file_url=data.get("proof_file_url") or data.get("ProofFileURL"),
            team_color=data.get("team_color") or data.get("TeamColor"),
        )


@dataclass
class ShipTo:
    """Custom Builder ship-to. A *different* field spelling from `Order`.

    The CB PlaceOrder takes a nested `ShipTo` object with `Zip`, `Address1` and
    a *string* `IsResidential` ("true"/"false"), where the REST API takes flat
    `ZIPCode`, `Address` and an integer. Same concept, three incompatible
    spellings; keeping them in separate types is what stops one leaking into
    the other.
    """

    first_name: str
    last_name: str
    address1: str
    city: str
    state: str
    zip: str
    country: str = "USA"
    company: str | None = None
    phone: str | None = None
    address2: str | None = None
    suite: str | None = None
    is_residential: bool = False

    def to_payload(self) -> dict[str, Any]:
        return {
            "FirstName": _clean(self.first_name),
            "LastName": _clean(self.last_name),
            "Company": _clean(self.company) or "",
            "Phone": _clean(self.phone) or "",
            "Address1": _clean(self.address1),
            "Address2": _clean(self.address2) or "",
            "Suite": _clean(self.suite) or "",
            "City": _clean(self.city),
            "State": _clean(self.state),
            "Zip": _clean(self.zip),
            "Country": _clean(self.country) or "USA",
            "IsResidential": "true" if self.is_residential else "false",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ShipTo":
        residential = data.get("is_residential", data.get("IsResidential", False))
        if isinstance(residential, str):
            residential = residential.strip().lower() in ("1", "true", "yes", "y")
        return cls(
            first_name=str(data.get("first_name") or data.get("FirstName") or ""),
            last_name=str(data.get("last_name") or data.get("LastName") or ""),
            address1=str(data.get("address1") or data.get("Address1") or data.get("address") or ""),
            address2=data.get("address2") or data.get("Address2"),
            suite=data.get("suite") or data.get("Suite"),
            city=str(data.get("city") or data.get("City") or ""),
            state=str(data.get("state") or data.get("State") or data.get("state_code") or ""),
            zip=str(data.get("zip") or data.get("Zip") or data.get("zip_code") or ""),
            country=str(data.get("country") or data.get("Country") or "USA"),
            company=data.get("company") or data.get("Company"),
            phone=data.get("phone") or data.get("Phone"),
            is_residential=bool(residential),
        )
