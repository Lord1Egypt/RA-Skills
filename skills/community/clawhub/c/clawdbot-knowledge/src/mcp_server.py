#!/usr/bin/env python3
"""
MCP-Server für DeepALL Maxima Maximus System
Prüft, indexiert und sammelt verstreute Dateien in maximus_files/
"""

import os
import json
import shutil
import asyncio
import aiohttp
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
import ast
from datetime import datetime

# Lade echte Umgebungsvariablen aus .env.real
load_dotenv('.env.real')

class MCPServer:
    """
    Master Content Processor Server
    Organisiert verstreute Dateien für das DeepALL Maxima Maximus System
    """
    
    def __init__(self):
        # MongoDB-Verbindung
        try:
            self.mongo_client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
            self.db = self.mongo_client[os.getenv("MONGODB_DATABASE", "deepall_hypercode")]
            logging.info("✅ MongoDB-Verbindung hergestellt")
        except Exception as e:
            logging.warning(f"⚠️ MongoDB nicht verfügbar: {e}")
            self.mongo_client = None
            self.db = None
        
        # Flowise-Konfiguration
        self.flowise_url = os.getenv("FLOWISE_URL", "https://flowise.luli-server.de")
        self.flowise_api_key = os.getenv("FLOWISE_API_KEY")
        
        # Verzeichnisse
        self.scattered_dir = "scattered_files"
        self.maximus_dir = "maximus_files"
        
        # Maximus-Verzeichnis erstellen
        os.makedirs(self.maximus_dir, exist_ok=True)
        
        # Logging konfigurieren
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Statistiken
        self.stats = {
            "processed": 0,
            "valid": 0,
            "invalid": 0,
            "collected": 0
        }

    async def check_json_file(self, file_path: str) -> dict:
        """
        Prüft JSON-Datei auf Syntax und DeepALL-Kompatibilität
        """
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
            
            # Prüfe DeepALL-Modul-Struktur
            required_fields = ["module", "id", "function", "input_types", "output"]
            if all(field in data for field in required_fields):
                # Zusätzliche Validierung für DeepALL-Module
                if isinstance(data.get("input_types"), list) and isinstance(data.get("output"), dict):
                    return {
                        "file": file_path,
                        "status": "valid",
                        "type": "json",
                        "module_type": "deepall_module",
                        "module_id": data.get("id"),
                        "module_name": data.get("module")
                    }
                else:
                    return {
                        "file": file_path,
                        "status": "invalid",
                        "error": "Invalid DeepALL module structure",
                        "type": "json"
                    }
            else:
                # Prüfe auf Flowise-Workflow
                if "nodes" in data and "connections" in data:
                    return {
                        "file": file_path,
                        "status": "valid",
                        "type": "json",
                        "module_type": "flowise_workflow",
                        "workflow_name": data.get("name", "unnamed")
                    }
                else:
                    return {
                        "file": file_path,
                        "status": "invalid",
                        "error": "Unknown JSON structure",
                        "type": "json"
                    }
                    
        except json.JSONDecodeError as e:
            return {
                "file": file_path,
                "status": "invalid",
                "error": f"JSON syntax error: {str(e)}",
                "type": "json"
            }
        except Exception as e:
            return {
                "file": file_path,
                "status": "invalid",
                "error": str(e),
                "type": "json"
            }

    async def check_python_file(self, file_path: str) -> dict:
        """
        Prüft Python-Datei auf Syntax und DeepALL-Kompatibilität
        """
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                content = f.read()
            
            # Syntax-Prüfung
            ast.parse(content)
            
            # Prüfe auf DeepALL-Klassen
            module_type = "python_script"
            if "class DeepAI" in content or "class Deep" in content:
                module_type = "deepall_module"
            elif "DeepMasterAgent" in content:
                module_type = "deepmaster_agent"
            elif "MCPServer" in content:
                module_type = "mcp_server"
            
            return {
                "file": file_path,
                "status": "valid",
                "type": "python",
                "module_type": module_type
            }
            
        except SyntaxError as e:
            return {
                "file": file_path,
                "status": "invalid",
                "error": f"Python syntax error: {str(e)}",
                "type": "python"
            }
        except Exception as e:
            return {
                "file": file_path,
                "status": "invalid",
                "error": str(e),
                "type": "python"
            }

    async def test_flowise_compatibility(self, file_path: str) -> bool:
        """
        Testet Flowise-Kompatibilität (simuliert)
        """
        try:
            if not self.flowise_api_key:
                self.logger.warning("Flowise API Key nicht verfügbar - überspringe Test")
                return True
            
            # Simulierter Flowise-Test
            # In echter Implementierung würde hier ein API-Aufruf stattfinden
            async with aiohttp.ClientSession() as session:
                # Placeholder für echten Flowise-Test
                await asyncio.sleep(0.1)  # Simuliere API-Aufruf
                return True
                
        except Exception as e:
            self.logger.warning(f"Flowise-Test fehlgeschlagen: {e}")
            return False

    async def index_file(self, file_info: dict):
        """
        Indexiert Datei in MongoDB
        """
        if self.db is None:
            self.logger.warning("MongoDB nicht verfügbar - überspringe Indexierung")
            return
        
        try:
            # Füge Zeitstempel hinzu
            file_info["indexed_at"] = datetime.now()
            file_info["mcp_version"] = "2.0.0"
            
            # Upsert in MongoDB
            self.db.file_index.update_one(
                {"file": file_info["file"]},
                {"$set": file_info},
                upsert=True
            )
            
            self.logger.info(f"📊 Indexiert: {os.path.basename(file_info['file'])} - {file_info['status']}")
            
        except Exception as e:
            self.logger.error(f"Indexierung fehlgeschlagen: {e}")

    def collect_file(self, file_info: dict):
        """
        Kopiert gültige Datei in maximus_files/
        """
        if file_info["status"] == "valid":
            try:
                source_path = file_info["file"]
                dest_path = os.path.join(self.maximus_dir, os.path.basename(source_path))
                
                # Vermeide Überschreibung
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(dest_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    dest_path = f"{base}_{counter}{ext}"
                
                shutil.copy2(source_path, dest_path)
                self.logger.info(f"📁 Gesammelt: {os.path.basename(source_path)} -> {os.path.basename(dest_path)}")
                self.stats["collected"] += 1
                
            except Exception as e:
                self.logger.error(f"Sammeln fehlgeschlagen: {e}")

    async def process_files(self):
        """
        Durchläuft alle Dateien in scattered_files/
        """
        if not os.path.exists(self.scattered_dir):
            self.logger.error(f"Verzeichnis {self.scattered_dir} nicht gefunden!")
            return
        
        self.logger.info(f"🔍 Durchsuche {self.scattered_dir}...")
        
        for root, _, files in os.walk(self.scattered_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self.stats["processed"] += 1
                
                if file.endswith(".json"):
                    file_info = await self.check_json_file(file_path)
                elif file.endswith(".py"):
                    file_info = await self.check_python_file(file_path)
                else:
                    file_info = {
                        "file": file_path,
                        "status": "skipped",
                        "error": "Unsupported file type",
                        "type": "unknown"
                    }
                
                # Statistiken aktualisieren
                if file_info["status"] == "valid":
                    self.stats["valid"] += 1
                elif file_info["status"] == "invalid":
                    self.stats["invalid"] += 1
                
                # Indexieren und sammeln
                await self.index_file(file_info)
                self.collect_file(file_info)

    def print_summary(self):
        """
        Gibt Zusammenfassung der Verarbeitung aus
        """
        self.logger.info("=" * 50)
        self.logger.info("📊 MCP-Server Zusammenfassung:")
        self.logger.info(f"   Verarbeitet: {self.stats['processed']}")
        self.logger.info(f"   Gültig: {self.stats['valid']}")
        self.logger.info(f"   Ungültig: {self.stats['invalid']}")
        self.logger.info(f"   Gesammelt: {self.stats['collected']}")
        self.logger.info(f"📁 Maximus-Dateien in: {self.maximus_dir}")
        self.logger.info("=" * 50)

    async def run(self):
        """
        Hauptausführung des MCP-Servers
        """
        self.logger.info("🚀 MCP-Server gestartet - DeepALL Maxima Maximus System")
        
        try:
            await self.process_files()
            self.print_summary()
            
            if self.stats["collected"] > 0:
                self.logger.info("✅ MCP-Server erfolgreich abgeschlossen!")
                self.logger.info("🔄 Nächster Schritt: DeepMasterAgent testen")
            else:
                self.logger.warning("⚠️ Keine Dateien gesammelt - prüfe scattered_files/")
                
        except Exception as e:
            self.logger.error(f"❌ MCP-Server Fehler: {e}")
        finally:
            if self.mongo_client:
                self.mongo_client.close()

if __name__ == "__main__":
    mcp = MCPServer()
    asyncio.run(mcp.run())
