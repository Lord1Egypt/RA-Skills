#!/usr/bin/env python3
"""
📄 Rechnungs-Generator v2.0
Unterstützt alle 3 Firmen mit Logo
"""

from fpdf import FPDF
from datetime import datetime, timedelta
import json
import os

# Firmendaten
FIRMEN = {
    'einzelunternehmen': {
        'name': 'Merlin Krischnah',
        'legal_name': 'Merlin Krischnah (Einzelunternehmer)',
        'adresse': 'Musterstraße 1',
        'plz_ort': '55116 Mainz',
        'telefon': '+49 152 27393530',
        'email': 'hello@mk-media.eu',
        'website': 'www.mk-media.eu',
        'ust_id': 'DE123456789',  # Zu ergänzen
        'steuernummer': 'TBD',
        'bank': {
            'name': 'N26',
            'iban': 'DE89 3704 0044 0532 0130 00',  # Zu ergänzen
            'bic': 'NTSBDEB1XXX'
        },
        'ust_befreit': False,  # USt-pflichtig
        'ust_satz': 19,
        'logo': None  # Pfad zu Logo
    },
    'ug': {
        'name': 'Merlin Krischnah Media UG',
        'legal_name': 'Merlin Krischnah Media UG (haftungsbeschränkt)',
        'adresse': 'Musterstraße 1',
        'plz_ort': '55116 Mainz',
        'telefon': '+49 152 27393530',
        'email': 'hello@mk-media.eu',
        'website': 'www.mk-media.eu',
        'ust_id': 'DE123456789',  # Zu ergänzen
        'handelsregister': 'HRB 12345 Mainz',  # Zu ergänzen
        'geschaeftsfuehrer': 'Merlin Krischnah',
        'bank': {
            'name': 'N26',
            'iban': 'DE89 3704 0044 0532 0130 00',
            'bic': 'NTSBDEB1XXX'
        },
        'ust_befreit': False,
        'ust_satz': 19,
        'logo': None
    },
    'ltd': {
        'name': 'MK Media Ltd',
        'legal_name': 'MK Media Ltd (Irish Limited)',
        'adresse': 'Dublin, Ireland',
        'plz_ort': 'Ireland',
        'telefon': '+353 ...',
        'email': 'hello@mk-media.eu',
        'website': 'www.mk-media.eu',
        'company_number': 'TBD',  # Irish Company Number
        'ust_id': 'IE...',  # Irish VAT
        'bank': {
            'name': 'TBD',
            'iban': 'IE...',
            'bic': '...'
        },
        'ust_befreit': False,
        'ust_satz': 23,  # Irish VAT 23%
        'logo': None
    }
}


class RechnungsPDF(FPDF):
    def __init__(self, firma_key='ug'):
        super().__init__()
        self.firma = FIRMEN.get(firma_key, FIRMEN['ug'])
        self.set_auto_page_break(auto=True, margin=20)
    
    def header(self):
        # Logo falls vorhanden
        if self.firma.get('logo') and os.path.exists(self.firma['logo']):
            self.image(self.firma['logo'], 10, 10, 50)
            self.ln(20)
        
        # Firmenname
        self.set_font('Helvetica', 'B', 18)
        self.cell(0, 8, self.firma['name'], 0, 1, 'L')
        self.set_font('Helvetica', '', 9)
        self.cell(0, 5, self.firma['adresse'], 0, 0, 'L')
        self.cell(0, 5, self.firma['telefon'], 0, 1, 'R')
        self.cell(0, 5, self.firma['plz_ort'], 0, 0, 'L')
        self.cell(0, 5, self.firma['email'], 0, 1, 'R')
        self.ln(5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)
    
    def footer(self):
        self.set_y(-20)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_font('Helvetica', '', 8)
        
        footer_text = self.firma['legal_name']
        if self.firma.get('handelsregister'):
            footer_text += f' | {self.firma["handelsregister"]}'
        if self.firma.get('ust_id'):
            footer_text += f' | USt-Id: {self.firma["ust_id"]}'
        
        self.cell(0, 5, footer_text, 0, 1, 'C')
        self.cell(0, 5, f'Seite {self.page_no()}', 0, 0, 'C')


def create_rechnung(
    firma_key='ug',
    rechnungs_nr='RE2024-0001',
    kunde=None,
    leistungen=None,
    datum=None,
    einleitungstext=None,
    output_path=None
):
    """
    Erstellt eine PDF-Rechnung
    
    Args:
        firma_key: 'einzelunternehmen', 'ug' oder 'ltd'
        rechnungs_nr: Rechnungsnummer
        kunde: {'name': '', 'adresse': '', 'plz_ort': ''}
        leistungen: [{'beschreibung': '', 'menge': 1, 'einzelpreis': 100}]
        datum: 'YYYY-MM-DD' oder datetime
        einleitungstext: Optionaler Einleitungstext
        output_path: Ausgabepfad
    
    Returns:
        Dateipfad der PDF
    """
    
    # Defaults
    if kunde is None:
        kunde = {'name': 'Kunde', 'adresse': 'Adresse', 'plz_ort': 'PLZ Ort'}
    
    if leistungen is None:
        leistungen = [{'beschreibung': 'Leistung', 'menge': 1, 'einzelpreis': 100}]
    
    if datum is None:
        datum = datetime.now()
    elif isinstance(datum, str):
        datum = datetime.strptime(datum, '%Y-%m-%d')
    
    faelligkeit = datum + timedelta(days=14)
    
    firma = FIRMEN.get(firma_key, FIRMEN['ug'])
    
    # PDF
    pdf = RechnungsPDF(firma_key)
    pdf.add_page()
    
    # Empfänger
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, kunde['name'], 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, kunde.get('adresse', ''), 0, 1, 'L')
    pdf.cell(0, 5, kunde.get('plz_ort', ''), 0, 1, 'L')
    
    if kunde.get('land'):
        pdf.cell(0, 5, kunde['land'], 0, 1, 'L')
    
    pdf.ln(10)
    
    # Rechnungstitel
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'RECHNUNG', 0, 1, 'C')
    pdf.ln(5)
    
    # Rechnungsdetails
    pdf.set_font('Helvetica', '', 10)
    details = [
        ('Rechnungsnummer:', rechnungs_nr),
        ('Ausstellungsdatum:', datum.strftime('%d.%m.%Y')),
        ('Faelligkeitsdatum:', faelligkeit.strftime('%d.%m.%Y'))
    ]
    
    for label, value in details:
        pdf.cell(50, 6, label, 0, 0, 'L')
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 6, value, 0, 1, 'L')
        pdf.set_font('Helvetica', '', 10)
    
    pdf.ln(5)
    
    # Einleitungstext
    if einleitungstext:
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, einleitungstext)
        pdf.ln(5)
    
    # Leistungstabelle
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    
    # Header
    pdf.cell(85, 8, 'Beschreibung', 1, 0, 'L', True)
    pdf.cell(15, 8, 'Menge', 1, 0, 'C', True)
    pdf.cell(30, 8, 'Einzelpreis', 1, 0, 'R', True)
    pdf.cell(30, 8, 'Gesamt', 1, 1, 'R', True)
    
    pdf.set_font('Helvetica', '', 10)
    netto_summe = 0
    
    for leistung in leistungen:
        beschreibung = leistung['beschreibung'][:50]
        menge = leistung.get('menge', 1)
        einzelpreis = leistung['einzelpreis']
        gesamt = menge * einzelpreis
        netto_summe += gesamt
        
        # Euro als EUR schreiben (encoding fix)
        pdf.cell(85, 7, beschreibung, 1, 0, 'L')
        pdf.cell(15, 7, str(menge), 1, 0, 'C')
        pdf.cell(30, 7, f'{einzelpreis:,.2f} EUR', 1, 0, 'R')
        pdf.cell(30, 7, f'{gesamt:,.2f} EUR', 1, 1, 'R')
    
    pdf.ln(5)
    
    # Summen
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(130, 7, 'Nettobetrag:', 0, 0, 'R')
    pdf.cell(30, 7, f'{netto_summe:,.2f} EUR', 0, 1, 'R')
    
    ust_betrag = 0
    if not firma.get('ust_befreit') and firma.get('ust_satz'):
        ust_betrag = netto_summe * firma['ust_satz'] / 100
        pdf.cell(130, 7, f"Umsatzsteuer ({firma['ust_satz']}%):", 0, 0, 'R')
        pdf.cell(30, 7, f'{ust_betrag:,.2f} EUR', 0, 1, 'R')
    
    brutto_summe = netto_summe + ust_betrag
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(130, 8, 'Gesamtbetrag:', 0, 0, 'R')
    pdf.cell(30, 8, f'{brutto_summe:,.2f} EUR', 0, 1, 'R')
    pdf.ln(10)
    
    # Steuerhinweis
    if firma.get('ust_befreit'):
        pdf.set_font('Helvetica', 'I', 9)
        pdf.multi_cell(0, 5,
            'Gemaess § 19 UStG wird keine Umsatzsteuer berechnet.\n'
            'Als Kleinunternehmer im Sinne von § 19 Abs. 1 UStG wird die Umsatzsteuer '
            'in der Rechnung nicht gesondert ausgewiesen.'
        )
        pdf.ln(5)
    
    # Zahlungsbedingungen
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Zahlungsbedingungen:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    
    bank = firma['bank']
    zahlungstext = (
        f'Bitte ueberweisen Sie den Betrag innerhalb von 14 Tagen auf folgendes Konto:\n\n'
        f"Bank: {bank['name']}\n"
        f"IBAN: {bank['iban']}\n"
        f"BIC: {bank['bic']}\n\n"
        f'Verwendungszweck: {rechnungs_nr}'
    )
    pdf.multi_cell(0, 5, zahlungstext)
    pdf.ln(10)
    
    # Grußformel
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 5,
        'Vielen Dank fuer Ihren Auftrag!\n\n'
        'Mit freundlichen Gruessen\n\n'
        f"{firma.get('geschaeftsfuehrer', 'Merlin Krischnah')}\n"
        f"{firma['name']}"
    )
    
    # Speichern
    if output_path is None:
        output_dir = 'rechnungen'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{rechnungs_nr}.pdf')
    
    pdf.output(output_path)
    
    return output_path


if __name__ == '__main__':
    # Beispiel: Rechnung für UG
    leistungen = [
        {'beschreibung': 'YouTube Video Produktion', 'menge': 1, 'einzelpreis': 500.00},
        {'beschreibung': 'Video Editing', 'menge': 1, 'einzelpreis': 300.00},
    ]
    
    kunde = {
        'name': 'Beispiel GmbH',
        'adresse': 'Musterstr. 123',
        'plz_ort': '10115 Berlin',
        'land': 'Deutschland'
    }
    
    # UG mit 19% USt
    output = create_rechnung(
        firma_key='ug',
        rechnungs_nr='RE2024-0001',
        kunde=kunde,
        leistungen=leistungen,
        einleitungstext='Vielen Dank fuer Ihren Auftrag!'
    )
    
    print(f'✅ Rechnung erstellt: {output}')
    
    # Einzelunternehmer (Kleinunternehmerregelung)
    output2 = create_rechnung(
        firma_key='einzelunternehmen',
        rechnungs_nr='RE2024-0002',
        kunde=kunde,
        leistungen=leistungen
    )
    
    print(f'✅ Rechnung (Einzelunternehmer) erstellt: {output2}')