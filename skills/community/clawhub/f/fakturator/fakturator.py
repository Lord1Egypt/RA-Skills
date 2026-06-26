#!/usr/bin/env python3
"""
Fakturownik — Generator Faktur VAT
Wersja: 1.0.0
Autor: Tomasz Pędzierski / Infinity Tech

Użycie:
    python3 fakturator.py
    python3 fakturator.py --demo
    python3 fakturator.py --generate "usługa IT" 1000 1 23
"""

import sys
import json
from datetime import datetime, timedelta
import re

# Polskie stawki VAT
VAT_RATES = {
    23: 23.0,
    8: 8.0,
    5: 5.0,
    0: 0.0,
    'zw': 0.0,  # zwolniony
    'np': 0.0,  # nie podlega
}

def validate_nip(nip):
    """Waliduje polski numer NIP."""
    nip = nip.replace('-', '').replace(' ', '')
    if not nip.isdigit():
        return False
    if len(nip) != 10:
        return False
    # Właściwa walidacja NIP
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    checksum = 0
    for i in range(9):
        checksum += int(nip[i]) * weights[i]
    checksum %= 11
    return checksum == int(nip[9])

def validate_regon(regon):
    """Waliduje polski numer REGON."""
    regon = regon.replace('-', '').replace(' ', '')
    if not regon.isdigit():
        return False
    if len(regon) not in [9, 14]:
        return False
    return True

def format_nip(nip):
    """Formatuje NIP do postaci XX-XXX-XX-XX-XXX."""
    nip = nip.replace('-', '').replace(' ', '')
    if len(nip) == 10:
        return f"{nip[:2]}-{nip[2:5]}-{nip[5:7]}-{nip[7:9]}-{nip[9:]}"
    return nip

def calculate_vat(amount, vat_rate):
    """Oblicza kwotę VAT i brutto."""
    netto = float(amount)
    vat_percent = VAT_RATES.get(vat_rate, 23.0)
    vat_amount = round(netto * vat_percent / 100, 2)
    brutto = round(netto + vat_amount, 2)
    return netto, vat_amount, brutto, vat_percent

def generate_invoice_number(year=None, month=None, counter=1):
    """Generuje numer faktury w formacie FV/RRRR/MM/XXX."""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    return f"FV/{year}/{month:02d}/{counter:03d}"

def generate_invoice(
    seller_name,
    seller_address,
    seller_nip,
    seller_regon=None,
    buyer_name=None,
    buyer_address=None,
    buyer_nip=None,
    items=None,
    invoice_number=None,
    invoice_date=None,
    sale_date=None,
    payment_date=None,
    payment_method='przelew',
    notes=None,
    template='classic'
):
    """Generuje fakturę VAT."""
    
    if items is None:
        items = []
    if invoice_date is None:
        invoice_date = datetime.now()
    if sale_date is None:
        sale_date = invoice_date
    if payment_date is None:
        payment_date = invoice_date + timedelta(days=14)
    if invoice_number is None:
        invoice_number = generate_invoice_number()
    
    # Walidacja NIP sprzedawcy
    if not validate_nip(seller_nip):
        return {'error': f"Nieprawidłowy NIP sprzedawcy: {seller_nip}"}
    
    # Walidacja NIP nabywcy (jeśli podany)
    if buyer_nip:
        if not validate_nip(buyer_nip):
            return {'error': f"Nieprawidłowy NIP nabywcy: {buyer_nip}"}
    
    # Oblicz sumy
    total_netto = 0
    total_vat = 0
    total_brutto = 0
    
    for item in items:
        netto, vat_amount, brutto, vat_pct = calculate_vat(
            item.get('amount', 0),
            item.get('vat', 23)
        )
        item['netto'] = netto
        item['vat_amount'] = vat_amount
        item['brutto'] = brutto
        item['vat_pct'] = vat_pct
        item['total'] = round(netto * item.get('quantity', 1), 2)
        total_netto += item['total']
        total_vat += round(item['total'] * vat_pct / 100, 2)
        total_brutto += round(item['total'] * (1 + vat_pct / 100), 2)
    
    total_vat = round(total_vat, 2)
    total_brutto = round(total_brutto, 2)
    
    invoice = {
        'invoice_number': invoice_number,
        'invoice_date': invoice_date.strftime('%Y-%m-%d'),
        'sale_date': sale_date.strftime('%Y-%m-%d') if isinstance(sale_date, datetime) else sale_date,
        'payment_date': payment_date.strftime('%Y-%m-%d') if isinstance(payment_date, datetime) else payment_date,
        'payment_method': payment_method,
        'seller': {
            'name': seller_name,
            'address': seller_address,
            'nip': seller_nip,
            'nip_formatted': format_nip(seller_nip),
            'regon': seller_regon,
        },
        'buyer': {
            'name': buyer_name or '',
            'address': buyer_address or '',
            'nip': buyer_nip or '',
            'nip_formatted': format_nip(buyer_nip) if buyer_nip else '',
        },
        'items': items,
        'summary': {
            'total_netto': round(total_netto, 2),
            'total_vat': total_vat,
            'total_brutto': total_brutto,
        },
        'template': template,
        'notes': notes or '',
        'generated': datetime.now().isoformat(),
    }
    
    return invoice

def format_invoice_text(invoice):
    """Formatuje fakturę jako tekst do wyświetlenia."""
    
    if 'error' in invoice:
        return f"❌ Błąd: {invoice['error']}"
    
    lines = []
    lines.append("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         FAKTURA VAT                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """.strip())
    
    lines.append(f"\n📄 Numer: {invoice['invoice_number']}")
    lines.append(f"📅 Data wystawienia: {invoice['invoice_date']}")
    lines.append(f"📅 Data sprzedaży: {invoice['sale_date']}")
    lines.append(f"💳 Termin płatności: {invoice['payment_date']}")
    lines.append(f"💰 Forma płatności: {invoice['payment_method']}")
    
    lines.append("\n" + "─"*70)
    lines.append("SPRZEDAWCA:")
    lines.append("─"*70)
    lines.append(f"  {invoice['seller']['name']}")
    lines.append(f"  {invoice['seller']['address']}")
    lines.append(f"  NIP: {invoice['seller']['nip_formatted']}")
    if invoice['seller'].get('regon'):
        lines.append(f"  REGON: {invoice['seller']['regon']}")
    
    lines.append("\n" + "─"*70)
    lines.append("NABYWCA:")
    lines.append("─"*70)
    if invoice['buyer']['name']:
        lines.append(f"  {invoice['buyer']['name']}")
        lines.append(f"  {invoice['buyer']['address']}")
        if invoice['buyer']['nip']:
            lines.append(f"  NIP: {invoice['buyer']['nip_formatted']}")
    else:
        lines.append("  [nie podano]")
    
    lines.append("\n" + "═"*70)
    lines.append(f"{'Lp.':<4} {'Nazwa towaru/usługi':<30} {'Cena':>10} {'VAT':>6} {'Netto':>10} {'Brutto':>10}")
    lines.append("═"*70)
    
    for i, item in enumerate(invoice['items'], 1):
        name = item.get('name', 'Usługa')[:30]
        amount = item.get('amount', 0)
        vat_pct = item.get('vat_pct', 23)
        total_netto = item.get('total', amount)
        total_brutto = item.get('brutto', amount * (1 + vat_pct/100))
        lines.append(f"{i:<4} {name:<30} {amount:>10.2f} {vat_pct:>5}% {total_netto:>10.2f} {total_brutto:>10.2f}")
    
    lines.append("═"*70)
    lines.append(f"{'':4} {'RAZEM NETTO:':<40} {invoice['summary']['total_netto']:>10.2f}")
    lines.append(f"{'':4} {'VAT:':<40} {invoice['summary']['total_vat']:>10.2f}")
    lines.append("─"*70)
    lines.append(f"{'':4} {'RAZEM BRUTTO:':<40} {invoice['summary']['total_brutto']:>10.2f} zł")
    lines.append("═"*70)
    
    if invoice.get('notes'):
        lines.append(f"\n📝 Uwagi: {invoice['notes']}")
    
    lines.append(f"\n✅ Faktura wygenerowana: {invoice['generated'][:10]}")
    
    return "\n".join(lines)

def format_invoice_csv(invoice):
    """Formatuje fakturę jako CSV."""
    lines = []
    lines.append("FAKTURA VAT")
    lines.append(f"Numer;{invoice['invoice_number']}")
    lines.append(f"Data wystawienia;{invoice['invoice_date']}")
    lines.append(f"Data sprzedaży;{invoice['sale_date']}")
    lines.append(f"Termin płatności;{invoice['payment_date']}")
    lines.append(f"Forma płatności;{invoice['payment_method']}")
    lines.append("")
    lines.append("SPRZEDAWCA")
    lines.append(f"Nazwa;{invoice['seller']['name']}")
    lines.append(f"Adres;{invoice['seller']['address']}")
    lines.append(f"NIP;{invoice['seller']['nip']}")
    lines.append("")
    lines.append("NABYWCA")
    lines.append(f"Nazwa;{invoice['buyer']['name']}")
    lines.append(f"Adres;{invoice['buyer']['address']}")
    lines.append(f"NIP;{invoice['buyer']['nip']}")
    lines.append("")
    lines.append("POZYCJE")
    lines.append("Lp;Nazwa;Ilość;Cena jedn.;VAT %;Netto;Brutto")
    for i, item in enumerate(invoice['items'], 1):
        lines.append(f"{i};{item.get('name','')};{item.get('quantity',1)};{item.get('amount',0)};{item.get('vat_pct',23)};{item.get('total',0)};{item.get('brutto',0)}")
    lines.append("")
    lines.append(f";;;RAZEM NETTO;{invoice['summary']['total_netto']}")
    lines.append(f";;;VAT;{invoice['summary']['total_vat']}")
    lines.append(f";;;RAZEM BRUTTO;{invoice['summary']['total_brutto']}")
    return "\n".join(lines)

def format_invoice_json(invoice):
    """Formatuje fakturę jako JSON."""
    return json.dumps(invoice, ensure_ascii=False, indent=2)

def demo_invoice():
    """Generuje przykładową fakturę."""
    return generate_invoice(
        seller_name="Infinity Tech Group sp. z o.o.",
        seller_address="ul. Rynek Solny 1/6, 22-400 Zamość",
        seller_nip="9223090619",
        seller_regon="544554591",
        buyer_name="Przykładowa Firma sp. z o.o.",
        buyer_address="ul. Główna 10, 20-001 Lublin",
        buyer_nip="1234567890",
        items=[
            {'name': 'Usługa wdrożeniowa OpenClaw', 'quantity': 1, 'amount': 5000.00, 'vat': 23},
            {'name': 'Konsultacja IT', 'quantity': 8, 'amount': 200.00, 'vat': 23},
            {'name': 'Licencja oprogramowania', 'quantity': 1, 'amount': 1500.00, 'vat': 23},
        ],
        invoice_number='FV/2026/05/001',
        notes='Dziękujemy za współpracę!',
    )

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   📄 Fakturownik v1.0 📄                                    ║
║              Generator Faktur VAT dla Firm i Freelancerów                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if '--demo' in sys.argv:
        print("\n🚀 GENEROWANIE PRZYKŁADOWEJ FAKTURY...\n")
        invoice = demo_invoice()
        print(format_invoice_text(invoice))
        
        # Zapisz demo
        with open('/home/node/.openclaw/workspace/fakturownik/demo_faktura.txt', 'w') as f:
            f.write(format_invoice_text(invoice))
        print("\n✅ Zapisano demo: demo_faktura.txt")
    
    elif '--generate' in sys.argv:
        idx = sys.argv.index('--generate')
        if idx + 4 <= len(sys.argv):
            name = sys.argv[idx + 1]
            amount = float(sys.argv[idx + 2])
            quantity = int(sys.argv[idx + 3])
            vat = int(sys.argv[idx + 4])
            
            invoice = generate_invoice(
                seller_name="Twoja Firma sp. z o.o.",
                seller_address="Twój adres",
                seller_nip="0000000000",
                buyer_name="Klient sp. z o.o.",
                buyer_address="Adres klienta",
                buyer_nip="0000000000",
                items=[{'name': name, 'quantity': quantity, 'amount': amount, 'vat': vat}],
            )
            print(format_invoice_text(invoice))
        else:
            print("❌ Użycie: --generate 'nazwa' cena ilość vat")
    
    elif '--csv' in sys.argv:
        invoice = demo_invoice()
        print(format_invoice_csv(invoice))
    
    elif '--json' in sys.argv:
        invoice = demo_invoice()
        print(format_invoice_json(invoice))
    
    else:
        print("""
📖 DOSTĘPNE POLECENIA:

   python3 fakturator.py --demo       — Generuj przykładową fakturę
   python3 fakturator.py --csv        — Eksportuj do CSV
   python3 fakturator.py --json        — Eksportuj do JSON
   python3 fakturator.py --generate "usługa" 1000 1 23

💡 PRZYKŁAD:
   python3 fakturator.py --generate "Konsultacja IT" 500 5 23

📊 WYNIK:
   Generuje fakturę VAT z podsumowaniem i szczegółami pozycji.
        """)
        
        print("\n" + "="*70)
        print("🚀 DEMO: Przykładowa faktura")
        print("="*70)
        
        invoice = demo_invoice()
        print(format_invoice_text(invoice))

if __name__ == "__main__":
    main()