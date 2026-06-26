#!/usr/bin/env python3
"""
📊 Beleg-Analyse
Analysiert PDF-Rechnungen und extrahiert Beträge, Daten, Anbieter
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

def extract_invoice_data(pdf_path):
    """Extrahiert Daten aus einer Rechnungs-PDF"""
    
    # PDF zu Text
    result = subprocess.run(
        ['pdftotext', '-layout', pdf_path, '-'],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Betrag finden (verschiedene Formate)
    betrag_match = re.search(r'(?:gesamt|total|betrag|summe).*?(\d+[,.]\d{2})\s*(?:€|EUR)', text, re.IGNORECASE)
    if not betrag_match:
        betrag_match = re.search(r'(\d+[,.]\d{2})\s*(?:€|EUR)', text)
    
    betrag = None
    if betrag_match:
        betrag = float(betrag_match.group(1).replace(',', '.'))
    
    # Datum finden
    datum_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if not datum_match:
        datum_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', text)
        if datum_match:
            datum = datetime.strptime(datum_match.group(1), '%d.%m.%Y').strftime('%Y-%m-%d')
        else:
            datum = None
    else:
        datum = datum_match.group(1)
    
    # Anbieter aus Dateiname oder Text
    anbieter = Path(pdf_path).stem
    anbieter_match = re.search(r'Rechnung[_\s]+(.+?)(?:\d{4}|$)', anbieter, re.IGNORECASE)
    if anbieter_match:
        anbieter = anbieter_match.group(1).replace('_', ' ').strip()
    
    return {
        'datei': os.path.basename(pdf_path),
        'datum': datum,
        'anbieter': anbieter,
        'betrag': betrag,
        'text_preview': text[:200] if text else ''
    }

def kategorisieren(anbieter):
    """Kategorisiert basierend auf Anbieter"""
    kategorien = {
        'OpusClip': 'Software',
        'Wondershare': 'Software',
        'Followerfabrik': 'Marketing',
        'Copecart': 'Marketing',
        'Strato': 'Hosting',
        'easyIrland': 'Dienstleistungen',
        'cogra': 'Dienstleistungen',
        'Google AdSense': 'Einnahmen YouTube',
        'AdSence': 'Einnahmen YouTube',
        'Patreon': 'Einnahmen Patreon',
        'Spreadshirt': 'Einnahmen Spreadshirt',
        'Steuerberater': 'Beratung'
    }
    
    for key, kat in kategorien.items():
        if key.lower() in anbieter.lower():
            return kat
    
    return 'Sonstiges'

def ordner_analysieren(ordner_path):
    """Analysiert alle PDFs in einem Ordner"""
    ergebnisse = []
    
    for root, dirs, files in os.walk(ordner_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                data = extract_invoice_data(pdf_path)
                data['kategorie'] = kategorisieren(data['anbieter'])
                data['pfad'] = pdf_path
                ergebnisse.append(data)
    
    return ergebnisse

def generate_summary(ergebnisse):
    """Generiert Zusammenfassung"""
    summen = {}
    
    for eintrag in ergebnisse:
        kat = eintrag['kategorie']
        if kat not in summen:
            summen[kat] = {'betrag': 0, 'anzahl': 0}
        
        if eintrag['betrag']:
            summen[kat]['betrag'] += eintrag['betrag']
            summen[kat]['anzahl'] += 1
    
    return summen

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        pfad = sys.argv[1]
        
        if os.path.isfile(pfad):
            # Einzelne Datei
            data = extract_invoice_data(pfad)
            data['kategorie'] = kategorisieren(data['anbieter'])
            print(json.dumps(data, indent=2))
        elif os.path.isdir(pfad):
            # Ordner
            ergebnisse = ordner_analysieren(pfad)
            summen = generate_summary(ergebnisse)
            
            print("=== ANALYSE ABGESCHLOSSEN ===\n")
            print(f"Dateien analysiert: {len(ergebnisse)}\n")
            
            print("=== SUMMEN NACH KATEGORIE ===")
            for kat, data in sorted(summen.items()):
                print(f"{kat}: €{data['betrag']:,.2f} ({data['anzahl']} Belege)")
            
            print("\n=== DETAILS ===")
            print(json.dumps(ergebnisse, indent=2))
        else:
            print(f"Fehler: Pfad nicht gefunden: {pfad}")
    else:
        print("Verwendung: python3 beleg-analyse.py <pfad>")