#!/usr/bin/env python3
"""
📄 DATEV-Export
Erstellt DATEV-kompatiblen CSV-Export für Steuerberater
"""

import csv
import json
from datetime import datetime
from pathlib import Path

# SKR03 Kontenplan
SKR03_KONTEN = {
    # Erträge (8000-8999)
    'Einnahmen YouTube': '8400',
    'Einnahmen Patreon': '8400',
    'Einnahmen Spreadshirt': '8400',
    'Sonstige Einnahmen': '8400',
    
    # Aufwendungen (6000-6999)
    'Software': '6815',
    'Marketing': '6800',
    'Dienstleistungen': '6200',
    'Hosting': '6815',
    'Bürobedarf': '6815',
    'Fahrkosten': '6640',
    'Beratung': '6200',
    'Sonstige Ausgaben': '6800',
}

def get_skr03_konto(kategorie, typ='ausgabe'):
    """Gibt SKR03-Kontonummer zurück"""
    return SKR03_KONTEN.get(kategorie, '6800' if typ == 'ausgabe' else '8400')

def buchungen_to_datev(buchungen, output_path=None):
    """
    Konvertiert Buchungen in DATEV-CSV-Format
    
    Args:
        buchungen: Liste von Buchungs-Dicts
        output_path: Optionaler Ausgabepfad
    
    Returns:
        CSV-String oder Dateipfad
    """
    # DATEV-Header
    header = [
        'Umsatz',           # Betrag
        'Soll/Haben',       # S oder H
        'WKZ Umsatz',       # Währung
        'Kurs',             # Wechselkurs
        'Basis-Umsatz',     # Basis-Betrag
        'WKZ Basis-Umsatz', # Basis-Währung
        'Konto',            # Gegenkonto
        'Gegenkonto',       # Konto
        'Belegfeld1',       # Belegnummer
        'Belegfeld2',       # Belegdatum
        'Skonto',           # Skonto
        'Buchungstext',     # Beschreibung
        'Postensperre',     # Sperre
        'Diverse Adressfelder', # Adressfelder
        'Geschäftspartnerbank', # Bank
        'Sachverhalt',      # Sachverhalt
        'Zahlweise',        # Zahlweise
        'Forderungsart',    # Forderungsart
        'Veranlagungsnummer', # Veranlagungsnr.
        'Ausstellungsdatum',   # Ausstellungsdatum
        'Datum',            # Buchungsdatum
        'Steuercode',       # Steuercode
    ]
    
    rows = []
    beleg_nr = 1
    
    for buchung in buchungen:
        kategorie = buchung.get('kategorie', 'Sonstige Ausgaben')
        betrag = buchung.get('betrag', 0)
        datum = buchung.get('datum') or buchung.get('monat', '2024-01') + '-01'
        beschreibung = buchung.get('beschreibung') or buchung.get('anbieter', '')
        
        # Typ bestimmen
        if 'Einnahmen' in kategorie:
            typ = 'einnahme'
            soll_haben = 'H'  # Haben
            konto = '1200'    # Bank
            gegenkonto = get_skr03_konto(kategorie, 'einnahme')
        else:
            typ = 'ausgabe'
            soll_haben = 'S'  # Soll
            konto = get_skr03_konto(kategorie, 'ausgabe')
            gegenkonto = '1200'  # Bank
            betrag = abs(betrag)
        
        # Datum formatieren
        try:
            buch_datum = datetime.strptime(datum, '%Y-%m-%d').strftime('%d.%m.%Y')
            beleg_datum = buch_datum
        except:
            buch_datum = '01.01.2024'
            beleg_datum = buch_datum
        
        # Belegnummer
        beleg = f"RE{buchung.get('jahr', 2024)}-{beleg_nr:04d}"
        beleg_nr += 1
        
        # Steuercode (0=ohne, 1=19%, 2=7%)
        steuercode = '1' if buchung.get('ust_pflichtig', True) else '0'
        
        row = [
            f"{betrag:.2f}",      # Umsatz
            soll_haben,            # Soll/Haben
            'EUR',                 # WKZ
            '',                    # Kurs
            '',                    # Basis-Umsatz
            '',                    # WKZ Basis
            konto,                 # Konto
            gegenkonto,            # Gegenkonto
            beleg,                 # Belegfeld1
            beleg_datum,           # Belegfeld2
            '',                    # Skonto
            beschreibung,          # Buchungstext
            '',                    # Postensperre
            '',                    # Adressfelder
            '',                    # Geschäftspartnerbank
            '',                    # Sachverhalt
            '',                    # Zahlweise
            '',                    # Forderungsart
            '',                    # Veranlagungsnummer
            '',                    # Ausstellungsdatum
            buch_datum,            # Datum
            steuercode,            # Steuercode
        ]
        
        rows.append(row)
    
    # CSV erstellen
    import io
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(header)
    writer.writerows(rows)
    
    csv_content = output.getvalue()
    
    # Optional speichern
    if output_path:
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write(csv_content)
        return output_path
    
    return csv_content


def from_buchhaltungs_json(json_path, output_path):
    """
    Erstellt DATEV-Export aus buchhaltung-2024.csv
    """
    import csv as csv_module
    
    buchungen = []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        reader = csv_module.DictReader(f, delimiter=',')
        for row in reader:
            betrag = float(row.get('Betrag_EUR', '0').replace('~', '').replace('TBD', '0'))
            
            if betrag != 0:
                buchungen.append({
                    'datum': f"2024-{row.get('Monat', '01')}",
                    'kategorie': row.get('Kategorie', 'Sonstige Ausgaben'),
                    'betrag': betrag,
                    'anbieter': row.get('Anbieter', ''),
                    'beschreibung': row.get('Typ', ''),
                })
    
    return buchungen_to_datev(buchungen, output_path)


if __name__ == '__main__':
    import sys
    
    # Test-Daten
    test_buchungen = [
        {
            'datum': '2024-06-15',
            'kategorie': 'Einnahmen YouTube',
            'betrag': 1766.51,
            'anbieter': 'Google AdSense',
            'beschreibung': 'YouTube Einnahmen Juni 2024',
            'ust_pflichtig': False
        },
        {
            'datum': '2024-07-25',
            'kategorie': 'Software',
            'betrag': -19.00,
            'anbieter': 'OpusClip',
            'beschreibung': 'OpusClip Abo Juli 2024',
            'ust_pflichtig': True
        },
        {
            'datum': '2024-07-30',
            'kategorie': 'Hosting',
            'betrag': -21.00,
            'anbieter': 'Strato',
            'beschreibung': 'Hosting Juli 2024',
            'ust_pflichtig': True
        }
    ]
    
    # Ausgabe
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
        result = buchungen_to_datev(test_buchungen, output_path)
        print(f"✅ DATEV-Export erstellt: {result}")
    else:
        print(buchungen_to_datev(test_buchungen))