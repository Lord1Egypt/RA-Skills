#!/usr/bin/env python3
"""
Test-Framework für MCP-Server und DeepMasterAgent
Testet JSON-Simulation und Modul-Orchestrierung
"""

import pytest
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from deep_master_agent import DeepMasterAgent
except ImportError as e:
    print(f"Import-Fehler: {e}")
    DeepMasterAgent = None

class TestMCPSystem:
    """
    Test-Suite für das MCP-System
    """
    
    def setup_method(self):
        """Setup für jeden Test"""
        self.test_dir = tempfile.mkdtemp()
        self.maximus_dir = os.path.join(self.test_dir, "maximus_files")
        os.makedirs(self.maximus_dir, exist_ok=True)
        
        # Test-Modul erstellen
        self.create_test_module()
    
    def create_test_module(self):
        """Erstellt Test-Modul für Tests"""
        test_module = {
            "module": "test-module",
            "id": "m999",
            "function": "test_function",
            "input_types": ["test"],
            "output": {"content_type": "test", "confidence": 0.9},
            "technologies": ["Testing"],
            "synergies": []
        }
        
        with open(os.path.join(self.maximus_dir, "m999.json"), "w") as f:
            json.dump(test_module, f, indent=2)
    
    def test_json_module_structure(self):
        """Testet JSON-Modul-Struktur"""
        # Prüfe ob scattered_files existiert
        scattered_dir = "scattered_files"
        assert os.path.exists(scattered_dir), f"Verzeichnis {scattered_dir} nicht gefunden"
        
        # Prüfe JSON-Dateien
        json_files = [f for f in os.listdir(scattered_dir) if f.endswith('.json')]
        assert len(json_files) > 0, "Keine JSON-Dateien in scattered_files gefunden"
        
        # Validiere erste JSON-Datei
        with open(os.path.join(scattered_dir, json_files[0]), 'r') as f:
            module_data = json.load(f)
        
        required_fields = ["module", "id", "function", "input_types", "output"]
        for field in required_fields:
            assert field in module_data, f"Feld {field} fehlt in JSON-Modul"
        
        print(f"✅ JSON-Struktur validiert: {json_files[0]}")
    
    def test_maximus_files_collection(self):
        """Testet ob Dateien in maximus_files gesammelt wurden"""
        maximus_dir = "maximus_files"
        
        if os.path.exists(maximus_dir):
            files = os.listdir(maximus_dir)
            print(f"📁 Maximus-Dateien gefunden: {len(files)}")
            for file in files:
                print(f"   - {file}")
        else:
            print("⚠️ maximus_files Verzeichnis nicht gefunden")
    
    @pytest.mark.asyncio
    async def test_deep_master_agent_basic(self):
        """Testet DeepMasterAgent Grundfunktionen"""
        if DeepMasterAgent is None:
            pytest.skip("DeepMasterAgent konnte nicht importiert werden")
        
        # Temporäres maximus_files für Test
        original_dir = "maximus_files"
        
        agent = DeepMasterAgent()
        agent.maximus_dir = self.maximus_dir
        
        # Test Modul laden
        module = await agent.load_module("m999")
        assert module is not None, "Test-Modul konnte nicht geladen werden"
        assert module["module"] == "test-module"
        
        print("✅ DeepMasterAgent Modul-Loading funktioniert")
    
    @pytest.mark.asyncio
    async def test_content_recognition_fallback(self):
        """Testet Fallback Content Recognition"""
        if DeepMasterAgent is None:
            pytest.skip("DeepMasterAgent konnte nicht importiert werden")
        
        agent = DeepMasterAgent()
        
        # Test verschiedene Content-Typen
        test_cases = [
            ("def test(): return True", "python"),
            ("name,age\nAlice,30", "table"),
            ("From: test@example.com", "email"),
            ("<html><body>Test</body></html>", "html"),
            ("Unknown content", "unknown")
        ]
        
        for content, expected_type in test_cases:
            result = agent._fallback_content_recognition(content)
            assert result["content_type"] == expected_type, f"Falsche Erkennung für {content}"
        
        print("✅ Fallback Content Recognition funktioniert")
    
    def test_synergy_calculation(self):
        """Testet Synergie-Berechnung"""
        if DeepMasterAgent is None:
            pytest.skip("DeepMasterAgent konnte nicht importiert werden")
        
        agent = DeepMasterAgent()
        
        # Test-Module
        module_a = {
            "technologies": ["Python", "Machine Learning"],
            "input_types": ["CSV", "JSON"]
        }
        module_b = {
            "technologies": ["Python", "Data Analysis"],
            "input_types": ["CSV", "Excel"]
        }
        
        synergy_score = agent.calculate_synergy_score(module_a, module_b)
        assert 0 <= synergy_score <= 1, "Synergie-Score außerhalb des gültigen Bereichs"
        assert synergy_score > 0, "Synergie-Score sollte > 0 sein für ähnliche Module"
        
        print(f"✅ Synergie-Berechnung: {synergy_score}")

def run_manual_tests():
    """Führt Tests manuell aus (ohne pytest)"""
    print("🧪 Starte manuelle Tests für MCP-System...")
    
    test_suite = TestMCPSystem()
    test_suite.setup_method()
    
    try:
        # Test 1: JSON-Struktur
        test_suite.test_json_module_structure()
        
        # Test 2: Maximus-Dateien
        test_suite.test_maximus_files_collection()
        
        # Test 3: Synergie-Berechnung
        test_suite.test_synergy_calculation()
        
        print("\n✅ Alle manuellen Tests erfolgreich!")
        
    except Exception as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Führe manuelle Tests aus
    success = run_manual_tests()
    
    if success:
        print("\n🎯 MCP-System Tests erfolgreich!")
        print("📋 Nächste Schritte:")
        print("   1. Flowise-Workflow testen")
        print("   2. Erstes Python-Modul erstellen")
        print("   3. SaaS-Demo vorbereiten")
    else:
        print("\n⚠️ Einige Tests fehlgeschlagen - prüfe Konfiguration")
