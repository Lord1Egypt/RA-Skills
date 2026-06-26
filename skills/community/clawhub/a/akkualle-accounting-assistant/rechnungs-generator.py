#!/usr/bin/env python3
"""
📄 Rechnungs-Generator
Erstellt professionelle PDF-Rechnungen
"""

from fpdf import FPDF
from datetime import datetime
import json
import os

class RechnungsPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        # Logo/Company Name
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'MERLIN KRISCHNAH MEDIA', 0, 1, 'L')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 5, 'Premium Digital Agency', 0, 1, 'L')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()}', 0, 0, 'C')


def create_rechnung(
    rechnungs_nr,
    kunde_name,
    kunde_adresse,
    kunde_plz_ort,
    leistungen,
    ausstellungsdatum=None,
    faelligkeitsdatum=None,
    einleitungstext="Vielen Dank für Ihren Auftrag. Hiermit stellen wir Ihnen folgende Leistungen in Rechnung:",
    ust_befreit=True,
    bank_name="N26",
    bank_iban="DE...",
    bank_bic="...",
    output_path=None
):
    """
    Erstellt eine PDF-Rechnung
    
    Args:
        rechnungs_nr: Rechnungsnummer (z.B. RE2024-0001)
        kunde_name: Name des Kunden
        kunde_adresse: Straße + Nr
        kunde_plz_ort: PLZ + Ort
        leistungen: Liste von Dicts [{'beschreibung': '...', 'menge': 1, 'einzelpreis': 100.00}]
        ausstellungsdatum: Datum (default: heute)
        faelligkeitsdatum: Fälligkeitsdatum (default: +14 Tage)
        einleitungstext: Einleitungstext
        ust_befreit: USt-befreit (Kleinunternehmerregelung)
        bank_name: Bankname
        bank_iban: IBAN
        bank_bic: BIC
        output_path: Ausgabepfad
    
    Returns:
        PDF-Dateipfad
    """
    
    # Daten
    if ausstellungsdatum is None:
        ausstellungsdatum = datetime.now()
    elif isinstance(ausstellungsdatum, str):
        ausstellungsdatum = datetime.strptime(ausstellungsdatum, '%Y-%m-%d')
    
    if faelligkeitsdatum is None:
        faelligkeitsdatum = datetime(ausstellungsdatum.year, ausstellungsdatum.month, ausstellungsdatum.day)
        from datetime import timedelta
        faelligkeitsdatum += timedelta(days=14)
    elif isinstance(faelligkeitsdatum, str):
        faelligkeitsdatum = datetime.strptime(faelligkeitsdatum, '%Y-%m-%d')
    
    # PDF erstellen
    pdf = RechnungsPDF()
    pdf.add_page()
    
    # Absender
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 5, 'Merlin Krischnah Media UG | Musterstraße 1 | 55116 Mainz', 0, 1, 'L')
    pdf.ln(5)
    
    # Empfänger
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, kunde_name, 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, kunde_adresse, 0, 1, 'L')
    pdf.cell(0, 5, kunde_plz_ort, 0, 1, 'L')
    pdf.ln(10)
    
    # Rechnungstitel
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'RECHNUNG', 0, 1, 'C')
    pdf.ln(5)
    
    # Rechnungsdetails
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(40, 6, 'Rechnungsnummer:', 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, rechnungs_nr, 0, 1, 'L')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(40, 6, 'Ausstellungsdatum:', 0, 0, 'L')
    pdf.cell(0, 6, ausstellungsdatum.strftime('%d.%m.%Y'), 0, 1, 'L')
    
    pdf.cell(40, 6, 'Fälligkeitsdatum:', 0, 0, 'L')
    pdf.cell(0, 6, faelligkeitsdatum.strftime('%d.%m.%Y'), 0, 1, 'L')
    pdf.ln(10)
    
    # Einleitungstext
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 5, einleitungstext)
    pdf.ln(10)
    
    # Leistungstabelle
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(90, 8, 'Beschreibung', 1, 0, 'L', True)
    pdf.cell(20, 8, 'Menge', 1, 0, 'C', True)
    pdf.cell(30, 8, 'Einzelpreis', 1, 0, 'R', True)
    pdf.cell(30, 8, 'Gesamt', 1, 1, 'R', True)
    
    pdf.set_font('Helvetica', '', 10)
    gesamt_summe = 0
    
    for leistung in leistungen:
        beschreibung = leistung['beschreibung']
        menge = leistung.get('menge', 1)
        einzelpreis = leistung['einzelpreis']
        gesamt = menge * einzelpreis
        gesamt_summe += gesamt
        
        pdf.cell(90, 7, beschreibung[:50], 1, 0, 'L')
        pdf.cell(20, 7, str(menge), 1, 0, 'C')
        pdf.cell(30, 7, f'€{einzelpreis:,.2f}', 1, 0, 'R')
        pdf.cell(30, 7, f'€{gesamt:,.2f}', 1, 1, 'R')
    
    # Gesamtsumme
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(140, 8, 'Gesamtbetrag', 1, 0, 'R')
    pdf.cell(30, 8, f'€{gesamt_summe:,.2f}', 1, 1, 'R')
    pdf.ln(10)
    
    # Steuerhinweis
    if ust_befreit:
        pdf.set_font('Helvetica', 'I', 9)
        pdf.multi_cell(0, 5, 
            'Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.\n'
            'Als Kleinunternehmer im Sinne von § 19 Abs. 1 UStG wird die Umsatzsteuer '
            'in der Rechnung nicht gesondert ausgewiesen.'
        )
        pdf.ln(5)
    
    # Zahlungsbedingungen
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Zahlungsbedingungen:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 5, 
        f'Bitte überweisen Sie den Betrag innerhalb von 14 Tagen auf folgendes Konto:\n\n'
        f'Bank: {bank_name}\n'
        f'IBAN: {bank_iban}\n'
        f'BIC: {bank_bic}\n\n'
        f'Verwendungszweck: {rechnungs_nr}'
    )
    pdf.ln(10)
    
    # Grußformel
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 5, 
        'Vielen Dank für Ihr Vertrauen!\n\n'
        'Mit freundlichen Grüßen\n\n'
        'Merlin Krischnah\n'
        'Merlin Krischnah Media UG'
    )
    
    # Speichern
    if output_path is None:
        output_path = f'rechnungen/{rechnungs_nr}.pdf'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    
    return output_path


def rechnung_aus_json(json_path, output_dir='rechnungen'):
    """Erstellt Rechnung aus JSON-Datei"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    output_path = os.path.join(output_dir, f"{data['rechnungs_nr']}.pdf")
    
    return create_rechnung(
        rechnungs_nr=data['rechnungs_nr'],
        kunde_name=data['kunde']['name'],
        kunde_adresse=data['kunde']['adresse'],
        kunde_plz_ort=data['kunde']['plz_ort'],
        leistungen=data['leistungen'],
        ausstellungsdatum=data.get('datum'),
        output_path=output_path
    )


if __name__ == '__main__':
    import sys
    
    # Beispiel-Rechnung
    beispiel_leistungen = [
        {
            'beschreibung': 'YouTube Video Produktion - Konzept & Dreh',
            'menge': 1,
            'einzelpreis': 500.00
        },
        {
            'beschreibung': 'YouTube Video Editing & Postproduktion',
            'menge': 1,
            'einzelpreis': 300.00
        },
        {
            'beschreibung': 'YouTube SEO Optimierung',
            'menge': 1,
            'einzelpreis': 150.00
        }
    ]
    
    output = create_rechnung(
        rechnungs_nr='RE2024-0001',
        kunde_name='Beispiel GmbH',
        kunde_adresse='Musterstraße 123',
        kunde_plz_ort='12345 Berlin',
        leistungen=beispiel_leistungen,
        bank_name='N26',
        bank_iban='DE89 3704 0044 0532 0130 00',
        bank_bic='NTSBDEB1XXX'
    )
    
    print(f"✅ Rechnung erstellt: {output}")
    
    # Zusammenfassung
    gesamt = sum(l['menge'] * l['einzelpreis'] for l in beispiel_leistungen)
    print(f"   Gesamt: €{gesamt:,.2f}")
    print(f"   Leistungen: {len(beispiel_leistungen)}")