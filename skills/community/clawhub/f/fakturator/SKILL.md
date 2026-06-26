# Fakturownik — Generator Faktur VAT

## Description
Profesjonalny generator faktur VAT dla freelancerów, małych firm i przedsiębiorców. Tworzy ładnie sformatowane faktury zgodne z polskimi przepisami, gotowe do wydruku lub wysłania mailem.

## Features
- **Generator faktur VAT** — tworzy profesjonalne faktury zgodne z polskim prawem
- **Wzory faktur** — 3 szablony do wyboru (klasyczna, nowoczesna, minimalistyczna)
- **Automatyczne obliczenia** — netto, VAT, brutto, suma całkowita
- **Dane firmowe** — zapamiętuje dane sprzedawcy i nabywcy
- **Eksport PDF** — gotowe do wydruku
- **Historia faktur** — zapisuj i zarządzaj wystawionymi fakturami
- **Numeryacja** — automatyczny numer faktury (FV/2026/05/001)

## Wymagania
- Python 3.8+ (opcjonalnie)
- OpenClaw z zainstalowanym skillem
- Dane firmy: NIP, nazwa, adres

## Usage
Użytkownik podaje:
1. Dane nabywcy (nazwa, adres, NIP)
2. Pozycje na fakturze (nazwa usługi, ilość, cena jednostkowa)
3. Opcjonalnie: termin płatności, forma płatności, uwagi

Skill automatycznie:
- Oblicza sumy netto i brutto
- Dodaje podatek VAT 23% (lub 8%, 5% dla niektórych towarów)
- Generuje numer faktury
- Tworzy profesjonalny wydruk

## Przykłady użycia
```
"Wystaw fakturę za usługę IT dla firmy X"
"Wygeneruj fakturę VAT dla Jana Kowalskiego"
"Utwórz fakturę na 500 zł netto + VAT"
"Dodaj pozycję: konsultacja IT, 300 zł, 23% VAT"
```

## Wersja PRO (12.29 zł brutto)
- Wysyłanie faktury mailem bezpośrednio do klienta (przez SMTP)
- 10+ profesjonalnych szablonów (różne style do wyboru)
- Historia wystawionych faktur (zapisane w plikach)
- Automatyczna numeracja z kontrolą duplikatów
- Priorytetowa obsługa mailowa
- Kontakt: tomaszpedzierski.infinity@wp.pl

**Jak wykupić?** Wyślij maila na tomaszpedzierski.infinity@wp.pl — odpowiem z linkiem do płatności.

## Autor
**Twórca:** Tomasz Pędzierski

## Licencja
MIT License

## Status
✅ Gotowy do użycia

---

*Fakturownik — wystawiaj profesjonalne faktury szybko i łatwo*