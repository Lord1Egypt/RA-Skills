#!/usr/bin/env python3
"""
📊 EÜR-Erstellung (Einnahmen-Überschuss-Rechnung)
Generiert EÜR für Steuererklärung
"""

import json
from datetime import datetime
from pathlib import Path

class EUErstellung:
    def __init__(self, jahr, unternehmen="Merlin Krischnah Media"):
        self.jahr = jahr
        self.unternehmen = unternehmen
        self.einnahmen = {}
        self.ausgaben = {}
        self.kategorien_einnahmen = [
            'YouTube AdSense',
            'Patreon',
            'Spreadshirt',
            'Sonstige Einnahmen'
        ]
        self.kategorien_ausgaben = [
            'Software',
            'Marketing',
            'Dienstleistungen',
            'Hosting',
            'Bürobedarf',
            'Fahrkosten',
            'Beratung',
            'Sonstige Ausgaben'
        ]
    
    def add_einnahme(self, kategorie, monat, betrag, beschreibung=''):
        if kategorie not in self.einnahmen:
            self.einnahmen[kategorie] = {}
        if monat not in self.einnahmen[kategorie]:
            self.einnahmen[kategorie][monat] = []
        self.einnahmen[kategorie][monat].append({
            'betrag': betrag,
            'beschreibung': beschreibung
        })
    
    def add_ausgabe(self, kategorie, monat, betrag, beschreibung=''):
        if kategorie not in self.ausgaben:
            self.ausgaben[kategorie] = {}
        if monat not in self.ausgaben[kategorie]:
            self.ausgaben[kategorie][monat] = []
        self.ausgaben[kategorie][monat].append({
            'betrag': betrag,
            'beschreibung': beschreibung
        })
    
    def from_json(self, buchungen_path):
        """Lädt Buchungen aus JSON-Datei"""
        with open(buchungen_path, 'r') as f:
            buchungen = json.load(f)
        
        for buchung in buchungen:
            kategorie = buchung.get('kategorie')
            monat = buchung.get('monat', buchung.get('datum', '')[:7])
            betrag = buchung.get('betrag')
            beschreibung = buchung.get('beschreibung', buchung.get('anbieter', ''))
            
            if kategorie in self.kategorien_einnahmen:
                self.add_einnahme(kategorie, monat, betrag, beschreibung)
            else:
                self.add_ausgabe(kategorie, monat, abs(betrag), beschreibung)
    
    def berechne_summen(self):
        """Berechnet Gesamtsummen"""
        einnahmen_gesamt = 0
        for kat, monate in self.einnahmen.items():
            for monat, eintraege in monate.items():
                einnahmen_gesamt += sum(e['betrag'] for e in eintraege)
        
        ausgaben_gesamt = 0
        for kat, monate in self.ausgaben.items():
            for monat, eintraege in monate.items():
                ausgaben_gesamt += sum(e['betrag'] for e in eintraege)
        
        return {
            'einnahmen': einnahmen_gesamt,
            'ausgaben': ausgaben_gesamt,
            'gewinn': einnahmen_gesamt - ausgaben_gesamt,
            'gewinn_marge': ((einnahmen_gesamt - ausgaben_gesamt) / einnahmen_gesamt * 100) if einnahmen_gesamt > 0 else 0
        }
    
    def generate_report(self, format='markdown'):
        """Generiert EÜR-Bericht"""
        summen = self.berechne_summen()
        
        if format == 'markdown':
            return self._generate_markdown(summen)
        elif format == 'csv':
            return self._generate_csv(summen)
        else:
            return self._generate_json(summen)
    
    def _generate_markdown(self, summen):
        report = f"""# Einnahmen-Überschuss-Rechnung {self.jahr}

**Unternehmen:** {self.unternehmen}  
**Steuerjahr:** {self.jahr}  
**Erstellt:** {datetime.now().strftime('%d.%m.%Y')}

---

## 📊 ZUSAMMENFASSUNG

| Position | Betrag |
|----------|--------|
| Einnahmen | €{summen['einnahmen']:,.2f} |
| Ausgaben | €{summen['ausgaben']:,.2f} |
| **GEWINN** | **€{summen['gewinn']:,.2f}** |
| Gewinn-Marge | {summen['gewinn_marge']:.1f}% |

---

## 💰 EINNAHMEN

| Kategorie | Summe | Monate |
|-----------|-------|--------|
"""
        
        for kat in self.kategorien_einnahmen:
            if kat in self.einnahmen:
                summe = sum(
                    sum(e['betrag'] for e in eintraege)
                    for eintraege in self.einnahmen[kat].values()
                )
                monate = sorted(self.einnahmen[kat].keys())
                report += f"| {kat} | €{summe:,.2f} | {', '.join(monate)} |\n"
        
        report += f"| **GESAMT** | **€{summen['einnahmen']:,.2f}** | |\n"
        
        report += """

---

## 💸 AUSGABEN

| Kategorie | Summe | Monate |
|-----------|-------|--------|
"""
        
        for kat in self.kategorien_ausgaben:
            if kat in self.ausgaben:
                summe = sum(
                    sum(e['betrag'] for e in eintraege)
                    for eintraege in self.ausgaben[kat].values()
                )
                monate = sorted(self.ausgaben[kat].keys())
                report += f"| {kat} | €{summe:,.2f} | {', '.join(monate)} |\n"
        
        report += f"| **GESAMT** | **€{summen['ausgaben']:,.2f}** | |\n"
        
        report += """

---

## 📋 FÜR STEUERBERATER

### Anlage EÜR:
- Zeile 4: Einnahmen aus freiberuflicher Tätigkeit: €{einnahmen:.2f}
- Zeile 11: Betriebsausgaben: €{ausgaben:.2f}
- Zeile 20: Gewinn: €{gewinn:.2f}

### Belege:
- Eingangsrechnungen: {anzahl_ausgaben}
- Ausgangsrechnungen: {anzahl_einnahmen}

---

*Erstellt mit OpenClaw Accounting Skill*
""".format(
            einnahmen=summen['einnahmen'],
            ausgaben=summen['ausgaben'],
            gewinn=summen['gewinn'],
            anzahl_einnahmen=sum(len(monate) for monate in self.einnahmen.values()),
            anzahl_ausgaben=sum(len(monate) for monate in self.ausgaben.values())
        )
        
        return report
    
    def _generate_csv(self, summen):
        import io
        output = io.StringIO()
        
        output.write("Kategorie;Typ;Monat;Betrag;Beschreibung\n")
        
        for kat, monate in self.einnahmen.items():
            for monat, eintraege in monate.items():
                for e in eintraege:
                    output.write(f"{kat};Einnahme;{monat};{e['betrag']};{e['beschreibung']}\n")
        
        for kat, monate in self.ausgaben.items():
            for monat, eintraege in monate.items():
                for e in eintraege:
                    output.write(f"{kat};Ausgabe;{monat};{e['betrag']};{e['beschreibung']}\n")
        
        return output.getvalue()
    
    def _generate_json(self, summen):
        return json.dumps({
            'jahr': self.jahr,
            'unternehmen': self.unternehmen,
            'summen': summen,
            'einnahmen': self.einnahmen,
            'ausgaben': self.ausgaben
        }, indent=2)
    
    def save(self, output_path, format='markdown'):
        """Speichert EÜR in Datei"""
        report = self.generate_report(format)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path


if __name__ == '__main__':
    import sys
    
    # Beispiel-Daten
    eur = EUErstellung(2024, "Merlin Krischnah Media")
    
    # Google AdSense
    eur.add_einnahme('YouTube AdSense', '2024-06', 1766.51, 'Monatseinnahmen Juni')
    eur.add_einnahme('YouTube AdSense', '2024-07', 2516.99, 'Monatseinnahmen Juli')
    eur.add_einnahme('YouTube AdSense', '2024-08', 3674.80, 'Monatseinnahmen August')
    eur.add_einnahme('YouTube AdSense', '2024-09', 3430.22, 'Monatseinnahmen September')
    
    # Ausgaben
    eur.add_ausgabe('Software', '2024-07', 19.00, 'OpusClip Abo')
    eur.add_ausgabe('Software', '2024-08', 74.44, 'Wondershare')
    eur.add_ausgabe('Marketing', '2024-07', 7.00, 'Followerfabrik')
    eur.add_ausgabe('Dienstleistungen', '2024-07', 374.50, 'easyIrland')
    eur.add_ausgabe('Hosting', '2024-07', 21.00, 'Strato')
    eur.add_ausgabe('Beratung', '2024-10', 65.00, 'Steuerberaterin')
    
    # Ausgabe
    print(eur.generate_report('markdown'))
    
    # Optional: Speichern
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
        eur.save(output_path)
        print(f"\n✅ EÜR gespeichert: {output_path}")