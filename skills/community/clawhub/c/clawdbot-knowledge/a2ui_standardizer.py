#!/usr/bin/env python3
"""
A2UI JSONL Format Standardization & Optimization
"""

import json
import re
from typing import Dict, List, Any

class A2UIStandardizer:
    """Standardisiert A2UI JSONL Formate für maximale Kompatibilität"""
    
    def __init__(self):
        self.templates = {
            'basic_dashboard': self._get_basic_dashboard_template(),
            'agent_status': self._get_agent_status_template(),
            'performance_grid': self._get_performance_grid_template()
        }
    
    def _get_basic_dashboard_template(self) -> str:
        """Standardisiertes Basic Dashboard Template"""
        return '{"beginRendering": {"surfaceId": "{surface_id}", "root": "main-container"}}\n{"surfaceUpdate": {"surfaceId": "{surface_id}", "components": [\n  {"id": "main-container", "component": {"Column": {"children": {"explicitList": ["header", "content"]}}}},\n  {"id": "header", "component": {"Card": {"child": "header-content"}}},\n  {"id": "header-content", "component": {"Column": {"children": {"explicitList": ["title", "subtitle"]}}}},\n  {"id": "title", "component": {"Text": {"usageHint": "h1", "text": {{"literalString": "{title}"}}}}},\n  {"id": "subtitle", "component": {"Text": {"text": {{"literalString": "{subtitle}"}}}},\n  {"id": "content", "component": {"Card": {"child": "content-grid"}}},\n  {"id": "content-grid", "component": {"Row": {"children": {"explicitList": {content_items}}}}}\n]}}'
    
    def _get_agent_status_template(self) -> str:
        """Agenten Status Template"""
        return '{"id": "{agent_id}-card", "component": {"Card": {"child": "{agent_id}-content"}}}\n{"id": "{agent_id}-content", "component": {{"Column": {{"children": {{"explicitList": ["{agent_id}-icon", "{agent_id}-text"]}}}}}}\n{"id": "{agent_id}-icon", "component": {{"Text": {{"text": {{"literalString": "{icon}"}}}}}}\n{"id": "{agent_id}-text", "component": {{"Text": {{"text": {{"literalString": "{status_text}"}}}}}}'
    
    def _get_performance_grid_template(self) -> str:
        """Performance Grid Template"""
        return '{"id": "performance-grid", "component": {"Card": {"child": "performance-content"}}}\n{"id": "performance-content", "component": {"Column": {"children": {"explicitList": ["performance-title", "metrics-row"]}}}}\n{"id": "performance-title", "component": {"Text": {"usageHint": "h2", "text": {"literalString": "📊 Performance Metrics"}}}}\n{"id": "metrics-row", "component": {"Row": {"children": {"explicitList": {metrics}}}}}'
    
    def create_standardized_dashboard(self, 
                                    surface_id: str, 
                                    title: str, 
                                    subtitle: str,
                                    agents: List[Dict[str, Any]]) -> str:
        """Erstellt standardisiertes Dashboard"""
        
        # Template mit Basis-Daten füllen
        template = self.templates['basic_dashboard'].format(
            surface_id=surface_id,
            title=title,
            subtitle=subtitle,
            content_items=json.dumps([f'"{agent["id"]}-card"' for agent in agents])
        )
        
        # Agenten-Komponenten hinzufügen
        agent_components = []
        for agent in agents:
            agent_component = self.templates['agent_status'].format(
                agent_id=agent['id'],
                icon=agent['icon'],
                status_text=agent['status_text']
            )
            agent_components.append(agent_component)
        
        # Performance-Metriken hinzufügen
        performance_template = self.templates['performance_grid'].format(
            metrics=json.dumps([f'"{metric["id"]}-metric"' for metric in agents])
        )
        
        return template + '\n' + '\n'.join(agent_components) + '\n' + performance_template
    
    def validate_jsonl(self, jsonl_content: str) -> Dict[str, Any]:
        """Validiert JSONL Inhalt"""
        lines = jsonl_content.strip().split('\n')
        validation_result = {
            'total_lines': len(lines),
            'valid_lines': 0,
            'invalid_lines': 0,
            'errors': []
        }
        
        for i, line in enumerate(lines):
            if line.strip():
                try:
                    json.loads(line)
                    validation_result['valid_lines'] += 1
                except json.JSONDecodeError as e:
                    validation_result['invalid_lines'] += 1
                    validation_result['errors'].append({
                        'line': i + 1,
                        'error': str(e),
                        'content': line[:100] + '...' if len(line) > 100 else line
                    })
        
        return validation_result

# Demo der Standardisierung
if __name__ == "__main__":
    print("🔧 A2UI JSONL Format Standardization Demo")
    print("=" * 50)
    
    standardizer = A2UIStandardizer()
    
    # Agenten-Daten
    agents = [
        {"id": "memory", "icon": "🧠", "status_text": "Memory Agent\\n✅ Active"},
        {"id": "analysis", "icon": "📊", "status_text": "Analysis Agent\\n✅ Active"},
        {"id": "reasoning", "icon": "🤖", "status_text": "Reasoning Agent\\n✅ Active"},
        {"id": "planning", "icon": "📋", "status_text": "Planning Agent\\n✅ Active"}
    ]
    
    # Standardisiertes Dashboard erstellen
    dashboard_jsonl = standardizer.create_standardized_dashboard(
        surface_id="axiomata-dashboard",
        title="🌟 AXIOMATA Global Intelligence Grid",
        subtitle="Standardized A2UI Dashboard",
        agents=agents
    )
    
    # Validierung
    validation = standardizer.validate_jsonl(dashboard_jsonl)
    
    print(f"📊 Validierungsergebnis:")
    print(f"   Gesamte Zeilen: {validation['total_lines']}")
    print(f"   Gültige Zeilen: {validation['valid_lines']}")
    print(f"   Ungültige Zeilen: {validation['invalid_lines']}")
    print(f"   Fehler: {len(validation['errors'])}")
    
    if validation['errors']:
        print(f"\n❌ Fehlerdetails:")
        for error in validation['errors'][:3]:  # Nur erste 3 Fehler zeigen
            print(f"   Zeile {error['line']}: {error['error']}")
    
    print(f"\n✅ Standardisierung abgeschlossen!")
    print(f"   Dashboard ist bereit für A2UI Rendering")