"""构建 NewApi 乘客与联系人（测试/演示）。"""
from __future__ import annotations

from typing import Any


def demo_passengers(adult: int = 1, child: int = 0, infant: int = 0) -> list[dict[str, Any]]:
    """生成满足常见校验要求的演示乘客（仅维护者自动化测试，勿对用户展示）。"""
    passengers: list[dict[str, Any]] = []
    pax_id = 1

    for _ in range(adult):
        passengers.append(
            {
                "paxId": pax_id,
                "name": "ZHANG/SAN",
                "paxType": "ADT",
                "birthday": "1990-01-15",
                "gender": "M",
                "cardNum": "E12345678",
                "cardType": "PP",
                "cardIssuedPlace": "CN",
                "cardExpiryDate": "2030-12-31",
                "nationality": "CN",
            }
        )
        pax_id += 1

    for _ in range(child):
        passengers.append(
            {
                "paxId": pax_id,
                "name": "ZHANG/XIAO",
                "paxType": "CHD",
                "birthday": "2018-06-01",
                "gender": "M",
                "cardNum": "E87654321",
                "cardType": "PP",
                "cardIssuedPlace": "CN",
                "cardExpiryDate": "2030-12-31",
                "nationality": "CN",
                "accompaniedPaxId": "1",
            }
        )
        pax_id += 1

    for _ in range(infant):
        passengers.append(
            {
                "paxId": pax_id,
                "name": "ZHANG/WU",
                "paxType": "INF",
                "birthday": "2024-01-01",
                "gender": "F",
                "cardNum": "E11112222",
                "cardType": "PP",
                "cardIssuedPlace": "CN",
                "cardExpiryDate": "2030-12-31",
                "nationality": "CN",
                "accompaniedPaxId": "1",
            }
        )
        pax_id += 1

    return passengers


def demo_agent_contact() -> dict[str, str]:
    return {
        "agentName": "ZHANG/SAN",
        "agentEmail": "skill-demo@flightroutes24.com",
        "mobile": "13800138000",
        "areaCode": "86",
    }
