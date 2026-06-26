import json
from pathlib import Path
from typing import Dict, Any

class ContextStore:
    """
    Zentraler Kontext-Speicher für persistentes Variablen-Pinning.
    Speichert Key-Value-Paare projektbasiert ab, um Redundanzen zu minimieren.
    """
    
    def __init__(self, storage_file: str = "context_store.json"):
        self.storage_file = Path(storage_file)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.storage_file.exists():
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def get_project_vars(self, project_name: str) -> Dict[str, Any]:
        return self.data.get(project_name, {}).get("vars", {})

    def set_project_var(self, project_name: str, key: str, value: Any):
        if project_name not in self.data:
            self.data[project_name] = {"project": project_name, "vars": {}}
        self.data[project_name]["vars"][key] = value
        self.save()
