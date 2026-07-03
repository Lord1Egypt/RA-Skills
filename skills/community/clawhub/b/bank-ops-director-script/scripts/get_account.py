#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Данные счёта компании для навыка bank-ops-director-script.

Генерируются локально, без сети, только стандартная библиотека. Детерминированы
по текущей дате: в пределах одного дня стабильны, день ото дня суммы слегка
меняются, статусы и сроки остаются согласованными. Все интервалы («осталось N
дней» / «просрочено N дней») уже посчитаны и лежат в JSON готовыми полями.

Запуск: python3 get_account.py [раздел]
Раздел: all | account | operations | restrictions | kartoteka | certificates |
        powers_of_attorney | recommended_actions
"""
import json
import random
import sys
from datetime import date, datetime, timedelta

SECTIONS = ("account", "operations", "restrictions", "kartoteka",
            "certificates", "powers_of_attorney", "recommended_actions")

# Скользящие смещения в днях от сегодняшней даты — статусы стабильны при любом
# дне запуска (просроченное остаётся просроченным, «скоро» остаётся «скоро»).
CERT_HEAD_OVERDUE = 14      # сертификат руководителя: истёк
CERT_ACC_LEFT = 34          # сертификат бухгалтера: ~середина июля
CERT_DEP_LEFT = 200         # сертификат заместителя: ~конец года
POA9_LEFT = 50              # доверенность № 9: ~конец июля
POA12_OVERDUE = 145
SUSP_DAYS = 22              # приостановление ФНС: действует
DECL_OVERDUE = 47           # декларация по НДС: срок сдачи прошёл
K2_AGE_1, K2_AGE_2 = 21, 9  # возраст документов картотеки № 2


def build(today=None):
    today = today or date.today()
    rnd = random.Random(today.toordinal())

    def past(n):
        return (today - timedelta(days=n)).isoformat()

    def fut(n):
        return (today + timedelta(days=n)).isoformat()

    sal1 = rnd.randint(70, 95) * 1000
    sal2 = rnd.randint(55, 70) * 1000
    ndfl = round((sal1 + sal2) * 0.13 / 1000) * 1000
    inc0 = rnd.randint(60, 120) * 1000
    inc1a = rnd.randint(180, 320) * 1000
    inc1b = rnd.randint(120, 260) * 1000
    inc3 = rnd.randint(250, 360) * 1000
    vznos = rnd.randint(40, 55) * 1000
    rent = 95000

    ops = [
        {"date": past(0), "time": "09:12", "amount": inc0,
         "counterparty": "ООО «Клиент-Торг»", "purpose": "аванс по договору 14/26",
         "status": "исполнена"},
        {"date": past(1), "time": "16:40", "amount": -ndfl,
         "counterparty": "ФНС", "purpose": "НДФЛ", "status": "исполнена"},
        {"date": past(1), "time": "16:38", "amount": -sal2,
         "counterparty": "Петрова А.С.", "purpose": "заработная плата",
         "status": "исполнена"},
        {"date": past(1), "time": "16:35", "amount": -sal1,
         "counterparty": "Иванов И.И.", "purpose": "заработная плата",
         "status": "исполнена"},
        {"date": past(1), "time": "11:05", "amount": inc1a,
         "counterparty": "ООО «Клиент-Торг»", "purpose": "оплата по счёту № 88",
         "status": "исполнена"},
        {"date": past(1), "time": "10:20", "amount": inc1b,
         "counterparty": "ИП Смирнов В.В.", "purpose": "оплата по договору 7/26",
         "status": "исполнена"},
        {"date": past(2), "time": "14:02", "amount": -rent,
         "counterparty": "АО «Аренда-Сервис»", "purpose": "аренда",
         "status": "отклонена банком (приостановление по ст. 76 НК)"},
        {"date": past(3), "time": "12:30", "amount": inc3,
         "counterparty": "ООО «Клиент-Торг»", "purpose": "оплата по счёту № 84",
         "status": "исполнена"},
        {"date": past(3), "time": "09:15", "amount": -vznos,
         "counterparty": "ФНС", "purpose": "страховые взносы",
         "status": "исполнена"},
    ]

    executed = [o for o in ops if o["status"] == "исполнена"]
    y_in = sum(o["amount"] for o in executed if o["date"] == past(1) and o["amount"] > 0)
    y_out = sum(-o["amount"] for o in executed if o["date"] == past(1) and o["amount"] < 0)
    y_in_n = sum(1 for o in executed if o["date"] == past(1) and o["amount"] > 0)
    y_out_n = sum(1 for o in executed if o["date"] == past(1) and o["amount"] < 0)
    start_today = rnd.randint(1100, 1500) * 1000
    current = start_today + sum(o["amount"] for o in executed if o["date"] == past(0))
    last_outgoing = next((o for o in executed if o["amount"] < 0), None)

    kartoteka2 = [
        {"doc": "инкассовое поручение ФНС № 8", "amount": 85000, "queue": 3,
         "date": past(K2_AGE_1), "days_in_kartoteka": K2_AGE_1},
        {"doc": "платёжное требование № 45, ООО «Поставщик»", "amount": 120000,
         "queue": 5, "date": past(K2_AGE_2), "days_in_kartoteka": K2_AGE_2},
    ]

    return {
        "data_kind": "synthetic_sample",
        "as_of": datetime.now().isoformat(timespec="minutes"),
        "company": {"name": "ООО «Ромашка»", "inn": "demo-inn"},
        "account": {
            "number": "demo-account-0001",
            "bank": "GreenBank",
            "currency": "RUB",
            "balance_start_today": start_today,
            "balance_current": current,
            "spending_mode": ("ограничено: действует приостановление по ст. 76 НК — "
                              "проходят платежи очередей выше налоговых (зарплата, налоги); "
                              "прочие отклоняются или попадают в картотеку"),
            "turnover_yesterday": {"in": y_in, "in_count": y_in_n,
                                   "out": y_out, "out_count": y_out_n},
            "last_outgoing": last_outgoing,
        },
        "operations": ops,
        "restrictions": [
            {"kind": "приостановление операций", "basis": "ст. 76 НК РФ",
             "reason": "непредставление декларации по НДС", "since": past(SUSP_DAYS),
             "status": "действует", "days_active": SUSP_DAYS},
            {"kind": "приостановление операций", "basis": "ст. 76 НК РФ",
             "since": past(121), "lifted": past(103), "status": "снято"},
        ],
        "kartoteka": {"k2": kartoteka2,
                      "k2_total": sum(x["amount"] for x in kartoteka2),
                      "k1": []},
        "certificates": [
            {"owner": "Руководитель (Иванов И.И.)",
             "valid_to": past(CERT_HEAD_OVERDUE), "status": "просрочен",
             "days_overdue": CERT_HEAD_OVERDUE},
            {"owner": "Бухгалтер (Петрова А.С.)",
             "valid_to": fut(CERT_ACC_LEFT), "status": "действует, истекает скоро",
             "days_left": CERT_ACC_LEFT},
            {"owner": "Заместитель руководителя (Сидоров П.П.)",
             "valid_to": fut(CERT_DEP_LEFT), "status": "действует",
             "days_left": CERT_DEP_LEFT},
        ],
        "powers_of_attorney": [
            {"number": 12, "issued": past(510), "holder": "Иванов И.И.",
             "scope": "право подписи платёжных документов",
             "valid_to": past(POA12_OVERDUE), "status": "просрочена",
             "days_overdue": POA12_OVERDUE},
            {"number": 7, "issued": past(100), "holder": "Петрова А.С.",
             "scope": "представление интересов в банке",
             "valid_to": fut(260), "status": "действует", "days_left": 260},
            {"number": 9, "issued": past(60), "holder": "Сидоров П.П.",
             "scope": "получение выписок",
             "valid_to": fut(POA9_LEFT), "status": "действует, истекает скоро",
             "days_left": POA9_LEFT},
        ],
        "recommended_actions": [
            {"priority": 1, "action": "подать декларацию по НДС за 1 кв. 2026",
             "reason": ("срок сдачи прошёл; это причина приостановления по ст. 76 НК — "
                        "после подачи налоговая отменит решение и банк снимет ограничение"),
             "days_overdue": DECL_OVERDUE},
            {"priority": 1, "action": "перевыпустить сертификат ЭП руководителя",
             "reason": "истёк, подписание платежей в банк-клиенте недоступно",
             "days_overdue": CERT_HEAD_OVERDUE},
            {"priority": 2, "action": "обеспечить на счёте 205 000 ₽",
             "reason": "погашение документов картотеки № 2"},
            {"priority": 3, "action": "продлить доверенность № 9 (Сидоров П.П.)",
             "reason": "истекает", "days_left": POA9_LEFT},
        ],
    }


def main():
    section = sys.argv[1] if len(sys.argv) > 1 else "all"
    data = build()
    if section != "all":
        if section not in SECTIONS:
            print(json.dumps({"error": "unknown section",
                              "sections": list(SECTIONS)}, ensure_ascii=False))
            return
        data = {"data_kind": data["data_kind"], "as_of": data["as_of"],
                section: data[section]}
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
