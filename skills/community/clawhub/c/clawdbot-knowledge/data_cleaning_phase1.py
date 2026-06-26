#!/usr/bin/env python3
"""
DATENBEREINIGUNGSSCRIPT - Phase 1
Saubere Aufbereitung der DeepAll-Modul-Daten
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import json

class DataCleaner:
    """Klasse für die Bereinigung der CSV-Daten"""
    
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
        self.cleaning_log = []
        
    def log_cleaning_action(self, action, details):
        """Protokolliert Bereinigungsaktionen"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        }
        self.cleaning_log.append(log_entry)
        print(f"🧹 {action}: {details}")
    
    def load_data(self):
        """Lädt die CSV-Daten"""
        try:
            self.df = pd.read_csv(self.input_file)
            self.log_cleaning_action("DATEN LADEN", f"Erfolgreich geladen: {len(self.df)} Zeilen, {len(self.df.columns)} Spalten")
            return True
        except Exception as e:
            self.log_cleaning_action("FEHLER BEIM LADEN", str(e))
            return False
    
    def clean_self_improvement_capabilities(self):
        """Bereinigt die self_improvement_capabilities Spalte"""
        if 'self_improvement_capabilities' not in self.df.columns:
            self.log_cleaning_action("SPALTE NICHT GEFUNDEN", "self_improvement_capabilities")
            return
        
        original_values = self.df['self_improvement_capabilities'].copy()
        
        # Mapping für die Bereinigung
        cleaning_mapping = {
            # Standardwerte beibehalten
            'batch processing': 'batch processing',
            'real-time streaming': 'real-time streaming', 
            'edge computing': 'edge computing',
            'high': 'high',
            'medium': 'medium',
            'low': 'low',
            
            # Beschreibende Werte standardisieren
            'modul: eigene zeile': 'unspecified',
            'modul: eigene zeile, alle spalten': 'unspecified',
            'superintelligenz: alle zugehörigen module': 'unspecified',
            'deepmaster: alles': 'unspecified',
            
            # Numerische Werte zu 'unspecified'
            '83': 'unspecified',
            '85': 'unspecified', 
            '40': 'unspecified',
            '93': 'unspecified',
            '14': 'unspecified',
            '18': 'unspecified',
            '53': 'unspecified',
            '150': 'unspecified',
            '152': 'unspecified',
            '155': 'unspecified',
            '158': 'unspecified',
            '160': 'unspecified',
            '161': 'unspecified',
            '142': 'unspecified'
        }
        
        # Bereinigung durchführen
        self.df['self_improvement_capabilities'] = self.df['self_improvement_capabilities'].map(cleaning_mapping).fillna('unspecified')
        
        # Statistik
        changed_count = (original_values != self.df['self_improvement_capabilities']).sum()
        self.log_cleaning_action("SELBSTVERBESSERUNG BEREINIGT", f"{changed_count} Einträge bereinigt")
        
        # Neue Verteilung
        new_dist = self.df['self_improvement_capabilities'].value_counts()
        self.log_cleaning_action("NEUE VERTEILUNG", f"Top 3: {dict(new_dist.head(3))}")
    
    def clean_technology(self):
        """Bereinigt die technology Spalte"""
        if 'technology' not in self.df.columns:
            self.log_cleaning_action("SPALTE NICHT GEFUNDEN", "technology")
            return
        
        original_values = self.df['technology'].copy()
        
        # Numerische Werte identifizieren und bereinigen
        def clean_tech_value(value):
            if pd.isna(value):
                return 'unspecified'
            
            value_str = str(value).strip()
            
            # Wenn es nur Zahlen sind
            if re.match(r'^\d+$', value_str):
                return 'unspecified'
            
            # Bereinige bekannte Probleme
            if value_str in ['150', '152', '155', '158', '160', '161', '142']:
                return 'unspecified'
            
            return value_str
        
        self.df['technology'] = self.df['technology'].apply(clean_tech_value)
        
        # Statistik
        changed_count = (original_values != self.df['technology']).sum()
        self.log_cleaning_action("TECHNOLOGIE BEREINIGT", f"{changed_count} Einträge bereinigt")
        
        # Neue Verteilung
        new_dist = self.df['technology'].value_counts()
        self.log_cleaning_action("NEUE VERTEILUNG", f"Top 3: {dict(new_dist.head(3))}")
    
    def clean_leserechte(self):
        """Bereinigt die leserechte Spalte"""
        if 'leserechte' not in self.df.columns:
            self.log_cleaning_action("SPALTE NICHT GEFUNDEN", "leserechte")
            return
        
        original_values = self.df['leserechte'].copy()
        
        def clean_leserechte_value(value):
            if pd.isna(value):
                return 'unspecified'
            
            value_str = str(value).strip()
            
            # synehsyXXX Muster
            if re.match(r'^synehsy\d+$', value_str):
                return 'synehsx_pattern'
            
            # Andere bekannte Muster
            if value_str in ['superintelligenz: alle zugehörigen module', 'deepmaster: alles', ' alle spalten']:
                return 'unspecified'
            
            return value_str
        
        self.df['leserechte'] = self.df['leserechte'].apply(clean_leserechte_value)
        
        # Statistik
        changed_count = (original_values != self.df['leserechte']).sum()
        self.log_cleaning_action("LESERECHTE BEREINIGT", f"{changed_count} Einträge bereinigt")
        
        # Neue Verteilung
        new_dist = self.df['leserechte'].value_counts()
        self.log_cleaning_action("NEUE VERTEILUNG", f"Top 3: {dict(new_dist.head(3))}")
    
    def standardize_categories(self):
        """Standardisiert die Kategorien"""
        if 'category' not in self.df.columns:
            self.log_cleaning_action("SPALTE NICHT GEFUNDEN", "category")
            return
        
        original_values = self.df['category'].copy()
        
        # Kategorien-Mapping für Konsistenz
        category_mapping = {
            'machine learning': 'machine_learning',
            'external integration': 'external_integration',
            'cloud management': 'cloud_management', 
            'optimization': 'optimization',
            'efficiency': 'efficiency',
            'data processing': 'data_processing',
            'anomaly detection': 'anomaly_detection',
            'security': 'security',
            'deepall-core': 'deepall_core',
            'experimental': 'experimental',
            'ai': 'ai',
            'healthcare': 'healthcare',
            'finance': 'finance',
            'infrastructure': 'infrastructure'
        }
        
        self.df['category'] = self.df['category'].map(category_mapping).fillna(self.df['category'])
        
        # Statistik
        changed_count = (original_values != self.df['category']).sum()
        self.log_cleaning_action("KATEGORIEN STANDARDISIERT", f"{changed_count} Einträge bereinigt")
    
    def remove_duplicates(self):
        """Entfernt doppelte Einträge"""
        original_count = len(self.df)
        
        # Auf Duplikate prüfen (alle Spalten)
        duplicates = self.df.duplicated()
        duplicate_count = duplicates.sum()
        
        if duplicate_count > 0:
            self.df = self.df.drop_duplicates()
            self.log_cleaning_action("DUPLIKATE ENTFERNT", f"{duplicate_count} Duplikate entfernt")
        else:
            self.log_cleaning_action("KEINE DUPLIKATE", "Keine doppelten Einträge gefunden")
    
    def validate_data(self):
        """Validiert die bereinigten Daten"""
        self.log_cleaning_action("DATENVALIDIERUNG", "Starte Validierung...")
        
        # Prüfe auf NaN Werte
        nan_counts = self.df.isnull().sum()
        nan_columns = nan_counts[nan_counts > 0]
        
        if len(nan_columns) > 0:
            self.log_cleaning_action("NAN WERTE GEFUNDEN", f"Spalten mit NaN: {dict(nan_columns)}")
        else:
            self.log_cleaning_action("KEINE NAN WERTE", "Alle Spalten sind vollständig")
        
        # Prüfe auf leere Strings
        empty_counts = {}
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                empty_count = (self.df[col] == '').sum()
                if empty_count > 0:
                    empty_counts[col] = empty_count
        
        if empty_counts:
            self.log_cleaning_action("LEERE STRINGS GEFUNDEN", f"Spalten mit leeren Strings: {empty_counts}")
        else:
            self.log_cleaning_action("KEINE LEEREN STRINGS", "Keine leeren Strings gefunden")
        
        # Datenstatistik
        self.log_cleaning_action("DATENSTATISTIK", f"Bereinigte Daten: {len(self.df)} Zeilen, {len(self.df.columns)} Spalten")
    
    def save_cleaned_data(self):
        """Speichert die bereinigten Daten"""
        try:
            self.df.to_csv(self.output_file, index=False)
            self.log_cleaning_action("DATEN GESPEICHERT", f"Bereinigte Daten gespeichert: {self.output_file}")
            return True
        except Exception as e:
            self.log_cleaning_action("FEHLER BEIM SPEICHERN", str(e))
            return False
    
    def save_cleaning_log(self):
        """Speichert das Bereinigungsprotokoll"""
        log_file = self.output_file.replace('.csv', '_cleaning_log.json')
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(self.cleaning_log, f, indent=2, ensure_ascii=False)
            self.log_cleaning_action("PROTOKOLL GESPEICHERT", f"Bereinigungsprotokoll: {log_file}")
            return True
        except Exception as e:
            self.log_cleaning_action("FEHLER BEIM SPEICHERN DES PROTOKOLLS", str(e))
            return False
    
    def run_full_cleaning(self):
        """Führt die vollständige Bereinigung durch"""
        print("🚀 STARTE DATENBEREINIGUNG - PHASE 1")
        print("=" * 50)
        
        # Schritt 1: Daten laden
        if not self.load_data():
            return False
        
        # Schritt 2: Selbstverbesserungsfähigkeiten bereinigen
        self.clean_self_improvement_capabilities()
        
        # Schritt 3: Technologien bereinigen
        self.clean_technology()
        
        # Schritt 4: Leserechte bereinigen
        self.clean_leserechte()
        
        # Schritt 5: Kategorien standardisieren
        self.standardize_categories()
        
        # Schritt 6: Duplikate entfernen
        self.remove_duplicates()
        
        # Schritt 7: Daten validieren
        self.validate_data()
        
        # Schritt 8: Daten speichern
        if not self.save_cleaned_data():
            return False
        
        # Schritt 9: Protokoll speichern
        if not self.save_cleaning_log():
            return False
        
        print("=" * 50)
        print("✅ DATENBEREINIGUNG ABGESCHLOSSEN!")
        
        return True

def main():
    """Hauptfunktion für die Datenbereinigung"""
    input_file = "/home/deepall/.clawdbot/media/inbound/f6abb43f-7d5a-44e1-bd5b-a7b7e354c8fa_fixed_formatted.csv"
    output_file = "/home/deepall/clawd/my-mcp-server/deepall_modules_cleaned.csv"
    
    cleaner = DataCleaner(input_file, output_file)
    
    if cleaner.run_full_cleaning():
        print("🎉 Phase 1 erfolgreich abgeschlossen!")
        print(f"📁 Bereinigte Datei: {output_file}")
        return True
    else:
        print("❌ Phase 1 fehlgeschlagen!")
        return False

if __name__ == "__main__":
    main()