#!/usr/bin/env python3
"""
DeepMasterAgent für DeepALL Maxima Maximus System
Orchestriert JSON-Module und Flowise-Integration
"""

import json
import os
import aiohttp
import asyncio
from dotenv import load_dotenv
import logging
from datetime import datetime
from typing import Dict, List, Any

# Lade echte Umgebungsvariablen aus .env.real
load_dotenv('.env.real')

class DeepMasterAgent:
    """
    DeepMasterAgent orchestriert Module und Synergien
    basierend auf JSON-Definitionen und Flowise-Workflows
    """
    
    def __init__(self):
        # Flowise-Konfiguration
        self.flowise_url = os.getenv("FLOWISE_URL", "https://flowise.luli-server.de")
        self.flowise_api_key = os.getenv("FLOWISE_API_KEY")
        self.flowise_chatflow_id = os.getenv("FLOWISE_CHATFLOW_ID")
        
        # Verzeichnisse
        self.maximus_dir = "maximus_files"
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Cache für geladene Module
        self.module_cache = {}
        
        # Statistiken
        self.stats = {
            "tasks_processed": 0,
            "modules_loaded": 0,
            "synergies_calculated": 0,
            "flowise_calls": 0
        }

    async def load_module(self, module_id: str) -> Dict[str, Any]:
        """
        Lädt JSON-Modul aus maximus_files/
        """
        # Prüfe Cache
        if module_id in self.module_cache:
            return self.module_cache[module_id]
        
        try:
            module_file = f"{self.maximus_dir}/{module_id}.json"

            # Versuche zuerst maximus_files
            if os.path.exists(module_file):
                with open(module_file, "r", encoding='utf-8') as f:
                    module_data = json.load(f)
            else:
                # Fallback: Enhanced Data Pipeline (scattered_files)
                scattered_file = f"scattered_files/{module_id}.json"
                if os.path.exists(scattered_file):
                    with open(scattered_file, "r", encoding='utf-8') as f:
                        module_data = json.load(f)

                    # Erweitere mit Performance-Daten falls verfügbar
                    performance_file = f"scattered_files/performance/{module_id}_performance.json"
                    if os.path.exists(performance_file):
                        try:
                            with open(performance_file, "r", encoding="utf-8") as f:
                                perf_data = json.load(f)
                            module_data["performance_metrics"] = perf_data.get("performance", {})
                            self.logger.info(f"📈 Performance-Daten hinzugefügt für {module_id}")
                        except Exception as e:
                            self.logger.warning(f"Performance-Daten nicht verfügbar für {module_id}: {e}")

                    self.logger.info(f"📦 Modul geladen (Enhanced Pipeline): {module_data.get('module', module_id)}")
                else:
                    self.logger.warning(f"Modul {module_id} nicht gefunden in {self.maximus_dir} oder scattered_files")
                    return None

            # Cache das Modul
            self.module_cache[module_id] = module_data
            self.stats["modules_loaded"] += 1

            self.logger.info(f"📦 Modul geladen: {module_data.get('module', module_id)}")
            return module_data
            
        except Exception as e:
            self.logger.error(f"Fehler beim Laden von Modul {module_id}: {e}")
            return None

    async def query_flowise(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sendet Anfrage an Flowise Content Recognition Workflow
        """
        if not self.flowise_api_key:
            self.logger.warning("Flowise nicht konfiguriert - verwende erweiterten Fallback")
            return self._enhanced_fallback_recognition(payload.get("content", ""))

        try:
            # Verwende den Simple Flowise Server API
            url = f"{self.flowise_url}/api/v1/prediction/content-recognition"
            headers = {
                "Authorization": f"Bearer {self.flowise_api_key}",
                "Content-Type": "application/json"
            }

            # Payload für Simple Flowise Server
            flowise_payload = {
                "question": payload.get("content", "")
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=flowise_payload, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.stats["flowise_calls"] += 1

                        # Extrahiere Ergebnis aus Flowise Response
                        if isinstance(result, dict):
                            content_type = result.get('content_type', 'unknown')
                            confidence = result.get('confidence', 0.0)
                            self.logger.info(f"🌐 Flowise Workflow: {content_type} (Confidence: {confidence:.2f})")
                            return result
                        else:
                            self.logger.warning("Unerwartetes Flowise Response Format")
                            return self._enhanced_fallback_recognition(payload.get("content", ""))
                    else:
                        self.logger.warning(f"Flowise-Fehler: {response.status}")
                        return self._enhanced_fallback_recognition(payload.get("content", ""))

        except Exception as e:
            self.logger.error(f"Flowise-Workflow fehlgeschlagen: {e}")
            return self._enhanced_fallback_recognition(payload.get("content", ""))

    def _enhanced_fallback_recognition(self, content: str) -> Dict[str, Any]:
        """
        Erweiterte Fallback Content Recognition mit Pattern-Matching aus Flowise Workflow
        """
        import re

        # Pattern-Definitionen aus Flowise Workflow
        patterns = {
            'python': [
                r'def\s+\w+\s*\(',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*["\']__main__["\']',
                r'class\s+\w+\s*\(',
                r'print\s*\('
            ],
            'javascript': [
                r'function\s+\w+\s*\(',
                r'const\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'var\s+\w+\s*=',
                r'console\.log\s*\(',
                r'=>\s*{'
            ],
            'table': [
                r'\w+,\w+,\w+',
                r'\w+\t\w+\t\w+',
                r'\|\s*\w+\s*\|\s*\w+\s*\|',
                r'Name\s*[,\t]\s*Age',
                r'\w+\s*[,\t]\s*\d+'
            ],
            'email': [
                r'From:\s*\S+@\S+',
                r'To:\s*\S+@\S+',
                r'Subject:\s*.+',
                r'\S+@\S+\.\S+',
                r'Dear\s+\w+',
                r'Best\s+regards'
            ],
            'html': [
                r'<html\b',
                r'<div\b',
                r'<p\b',
                r'<a\s+href=',
                r'<img\s+src=',
                r'</\w+>'
            ]
        }

        # Pattern-Analyse
        results = {}
        total_matches = 0

        for content_type, type_patterns in patterns.items():
            matches = 0
            matched_patterns = []

            for pattern in type_patterns:
                try:
                    pattern_matches = len(re.findall(pattern, content, re.IGNORECASE))
                    if pattern_matches > 0:
                        matches += pattern_matches
                        matched_patterns.append(pattern)
                except re.error:
                    continue

            if matches > 0:
                confidence = min(0.9, matches * 0.15 + 0.3)
                results[content_type] = {
                    'matches': matches,
                    'patterns': matched_patterns,
                    'confidence': confidence
                }
                total_matches += matches

        # Beste Übereinstimmung finden
        if results:
            best_type = max(results.keys(), key=lambda k: results[k]['confidence'])
            best_result = results[best_type]

            return {
                "content_type": best_type,
                "confidence": round(best_result['confidence'], 3),
                "language": self._detect_language(content),
                "entities": self._extract_entities(content, best_type),
                "patterns_detected": best_result['patterns'][:3],  # Top 3 patterns
                "reasoning": f"Pattern-based classification: {best_result['matches']} matches",
                "source": "enhanced_fallback",
                "processing_timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "content_type": "unknown",
                "confidence": 0.0,
                "language": "unknown",
                "entities": [],
                "patterns_detected": [],
                "reasoning": "No patterns matched",
                "source": "enhanced_fallback",
                "processing_timestamp": datetime.now().isoformat()
            }

    def _detect_language(self, content: str) -> str:
        """Spracherkennung basierend auf Flowise Workflow"""
        import re

        patterns = {
            'en': r'\b(the|and|or|but|in|on|at|to|for|of|with|by)\b',
            'de': r'\b(der|die|das|und|oder|aber|in|an|zu|für|von|mit|bei)\b',
            'fr': r'\b(le|la|les|et|ou|mais|dans|sur|à|pour|de|avec|par)\b',
            'es': r'\b(el|la|los|las|y|o|pero|en|sobre|a|para|de|con|por)\b'
        }

        max_matches = 0
        detected_lang = 'unknown'

        for lang, pattern in patterns.items():
            try:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                if matches > max_matches:
                    max_matches = matches
                    detected_lang = lang
            except re.error:
                continue

        return detected_lang if max_matches > 0 else 'unknown'

    def _extract_entities(self, content: str, content_type: str) -> List[str]:
        """Entitäten-Extraktion basierend auf Content-Typ"""
        import re

        entities = []

        try:
            if content_type == 'python':
                # Funktionsnamen extrahieren
                functions = re.findall(r'def\s+(\w+)\s*\(', content)
                entities.extend(functions[:5])
            elif content_type == 'javascript':
                # Funktionsnamen extrahieren
                functions = re.findall(r'function\s+(\w+)\s*\(', content)
                entities.extend(functions[:5])
            elif content_type == 'email':
                # Email-Adressen extrahieren
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
                entities.extend(emails[:3])
            elif content_type == 'table':
                # Header extrahieren (erste Zeile)
                lines = content.strip().split('\n')
                if lines:
                    first_line = lines[0]
                    for sep in [',', '\t', '|']:
                        if sep in first_line:
                            headers = [h.strip().replace('"', '') for h in first_line.split(sep)]
                            entities.extend(headers[:5])
                            break
        except Exception:
            pass

        return entities

    def calculate_synergy_score(self, module_a: Dict, module_b: Dict) -> float:
        """
        Berechnet Synergie-Score zwischen zwei Modulen
        Formel aus PRD: 0.4 * tech_overlap + 0.3 * data_compatibility + 0.2 * historical_success + 0.1 * resonance_score + 0.1 * embedding_similarity
        """
        try:
            # Technologie-Überschneidung
            tech_a = set(module_a.get("technologies", []))
            tech_b = set(module_b.get("technologies", []))
            tech_overlap = len(tech_a.intersection(tech_b)) / max(len(tech_a.union(tech_b)), 1)
            
            # Datenformat-Kompatibilität
            input_a = set(module_a.get("input_types", []))
            input_b = set(module_b.get("input_types", []))
            data_compatibility = len(input_a.intersection(input_b)) / max(len(input_a.union(input_b)), 1)
            
            # Historischer Erfolg (simuliert)
            historical_success = 0.6  # Placeholder
            
            # Resonanz-Score (simuliert)
            resonance_score = 0.5  # Placeholder
            
            # Embedding-Ähnlichkeit (simuliert)
            embedding_similarity = 0.7  # Placeholder
            
            # PRD-Formel anwenden
            synergy_score = (
                0.4 * tech_overlap +
                0.3 * data_compatibility +
                0.2 * historical_success +
                0.1 * resonance_score +
                0.1 * embedding_similarity
            )
            
            self.stats["synergies_calculated"] += 1
            return round(synergy_score, 3)
            
        except Exception as e:
            self.logger.error(f"Synergie-Berechnung fehlgeschlagen: {e}")
            return 0.0

    async def find_synergistic_modules(self, primary_module: Dict, threshold: float = 0.5) -> List[Dict]:
        """
        Findet Module mit hoher Synergie zum Primärmodul
        """
        synergistic_modules = []

        # Erweiterte Modul-Zuordnung
        module_mapping = {
            "DeepAI-Analytics": "m042",
            "DeepAI-Research": "m203",
            "DeepAI-Communication": "m055",
            "DeepAI-KnowledgeGraph": "m067",
            "DeepAI-Encryption": "m038",
            "DeepAI-DataScience": "m049",
            "deepai-analytics": "m042",
            "deepai-research": "m203",
            "deepai-communication": "m055",
            "deepai-knowledgegraph": "m067",
            "deepai-encryption": "m038",
            "deepai-datascience": "m049"
        }

        # Prüfe vordefinierte Synergien
        predefined_synergies = primary_module.get("synergies", [])
        for synergy in predefined_synergies:
            if synergy.get("tech_overlap", 0) > threshold:
                synergy_module_name = synergy.get("module", "")
                synergy_module_id = module_mapping.get(synergy_module_name)

                if synergy_module_id:
                    synergy_module = await self.load_module(synergy_module_id)
                    if synergy_module:
                        synergy_score = self.calculate_synergy_score(primary_module, synergy_module)
                        synergistic_modules.append({
                            "module": synergy_module,
                            "synergy_score": synergy_score,
                            "reason": "predefined_synergy"
                        })
                        self.logger.info(f"🔗 Synergie gefunden: {primary_module['module']} → {synergy_module['module']} (Score: {synergy_score:.3f})")

        return synergistic_modules

    async def orchestrate_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Hauptorchestierung: Analysiert Content, lädt Module, berechnet Synergien
        """
        try:
            self.stats["tasks_processed"] += 1
            self.logger.info(f"🎯 Orchestriere Task: {task.get('module', 'auto-detect')}")
            
            # 1. Content Recognition via Flowise
            content = task.get("content", "")
            recognition = await self.query_flowise({"content": content})
            
            # 2. Primärmodul bestimmen
            primary_module_id = task.get("module")
            if not primary_module_id:
                # Auto-Detection basierend auf Content-Type
                content_type = recognition.get("content_type", "unknown")
                module_mapping = {
                    "python": "m127",      # deepai-datascience
                    "table": "m127",       # deepai-datascience
                    "email": "m089",       # deepai-communication
                    "html": "m156",        # deepai-knowledgegraph
                    "document": "m156",    # deepai-knowledgegraph
                    "unknown": "m203"      # deepai-research
                }
                primary_module_id = module_mapping.get(content_type, "m203")
            
            # 3. Primärmodul laden
            primary_module = await self.load_module(primary_module_id)
            if not primary_module:
                return [{"error": f"Primärmodul {primary_module_id} nicht gefunden"}]
            
            # 4. Ergebnisse sammeln
            results = [{
                "module": primary_module["module"],
                "module_id": primary_module["id"],
                "result": primary_module["output"],
                "content_type": recognition.get("content_type"),
                "confidence": recognition.get("confidence"),
                "role": "primary"
            }]
            
            # 5. Synergistische Module finden
            synergistic_modules = await self.find_synergistic_modules(primary_module)
            for synergy in synergistic_modules:
                if synergy["synergy_score"] > 0.5:  # Threshold aus PRD
                    results.append({
                        "module": synergy["module"]["module"],
                        "module_id": synergy["module"]["id"],
                        "result": synergy["module"]["output"],
                        "synergy_score": synergy["synergy_score"],
                        "role": "synergistic"
                    })
            
            # 6. Metadaten hinzufügen
            for result in results:
                result["timestamp"] = datetime.now().isoformat()
                result["orchestrated_by"] = "DeepMasterAgent"
            
            self.logger.info(f"✅ Task orchestriert: {len(results)} Module aktiviert")
            return results
            
        except Exception as e:
            self.logger.error(f"Orchestrierung fehlgeschlagen: {e}")
            return [{"error": str(e)}]

    def print_stats(self):
        """
        Gibt Statistiken aus
        """
        self.logger.info("=" * 50)
        self.logger.info("📊 DeepMasterAgent Statistiken:")
        self.logger.info(f"   Tasks verarbeitet: {self.stats['tasks_processed']}")
        self.logger.info(f"   Module geladen: {self.stats['modules_loaded']}")
        self.logger.info(f"   Synergien berechnet: {self.stats['synergies_calculated']}")
        self.logger.info(f"   Flowise-Aufrufe: {self.stats['flowise_calls']}")
        self.logger.info("=" * 50)

# Test-Funktion
async def test_deep_master_agent():
    """
    Testet den DeepMasterAgent mit Beispiel-Daten
    """
    agent = DeepMasterAgent()
    
    # Test-Task
    task = {
        "content": "name,age\nAlice,30\nBob,25",
        "module": "m127"  # deepai-datascience
    }
    
    print("🧪 Teste DeepMasterAgent...")
    results = await agent.orchestrate_task(task)
    
    print("\n📋 Ergebnisse:")
    for result in results:
        print(f"  - {result.get('module', 'unknown')}: {result.get('role', 'unknown')}")
    
    agent.print_stats()
    return results

if __name__ == "__main__":
    asyncio.run(test_deep_master_agent())
