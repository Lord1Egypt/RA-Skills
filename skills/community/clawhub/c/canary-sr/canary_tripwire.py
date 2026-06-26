#!/usr/bin/env python3
"""
Canary Tripwire — Honeypot File Management
Creates and monitors tripwire files that should never be accessed.

Author: Shadow Rose
License: MIT
"""

import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TripwireManager:
    """Manages honeypot tripwire files and monitoring."""
    
    def __init__(self, tripwire_dir: str = '.canary_tripwires'):
        """
        Initialize tripwire manager.
        
        Args:
            tripwire_dir: Directory to store tripwire files
        """
        self.tripwire_dir = Path(tripwire_dir).expanduser().resolve()
        self.tripwire_dir.mkdir(exist_ok=True)
        
        self.registry_file = self.tripwire_dir / 'registry.json'
        self.alert_log = self.tripwire_dir / 'alerts.log'
        
        self.tripwires = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load tripwire registry from disk."""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_registry(self):
        """Save tripwire registry to disk."""
        with open(self.registry_file, 'w') as f:
            json.dump(self.tripwires, f, indent=2)
    
    def create_tripwire(
        self,
        path: str,
        content: Optional[str] = None,
        severity: str = 'high',
        description: str = ''
    ) -> bool:
        """
        Create a tripwire file.
        
        Args:
            path: Path to create tripwire at
            content: File content (default: honeypot warning)
            severity: Alert severity if triggered
            description: Description of what this tripwire protects
            
        Returns:
            True if created successfully
        """
        tripwire_path = Path(path).expanduser().resolve()
        
        # Check if already registered
        if str(tripwire_path) in self.tripwires:
            print(f"Tripwire already registered: {path}")
            return False

        # Refuse to overwrite existing files not created by Canary
        if tripwire_path.exists():
            print(f"Canary: refusing to overwrite existing file: {path} — use a dedicated decoy path")
            return False

        # Default content
        if content is None:
            content = self._generate_honeypot_content(path)
        
        # Create file
        try:
            tripwire_path.parent.mkdir(parents=True, exist_ok=True)
            with open(tripwire_path, 'x') as f:
                f.write(content)
            
            # Calculate hash
            content_hash = self._hash_content(content)
            
            # Register tripwire
            self.tripwires[str(tripwire_path)] = {
                'created': datetime.now().isoformat(),
                'hash': content_hash,
                'severity': severity,
                'description': description,
                'triggered': False,
                'trigger_count': 0,
            }
            
            self._save_registry()
            print(f"✅ Tripwire created: {path}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to create tripwire: {e}")
            return False
    
    def _generate_honeypot_content(self, path: str) -> str:
        """Generate honeypot file content."""
        return f"""# CANARY TRIPWIRE
# This file should never be accessed.
#
# Path: {path}
# Created: {datetime.now().isoformat()}
#
# If you see this, you have triggered a safety tripwire.
# This file exists to detect unauthorized access.
#
# DO NOT MODIFY OR DELETE THIS FILE.

TRIPWIRE_ID: {self._generate_tripwire_id(path)}
"""
    
    def _generate_tripwire_id(self, path: str) -> str:
        """Generate unique ID for tripwire."""
        return hashlib.sha256(f"{path}{time.time()}".encode()).hexdigest()[:16]
    
    def _hash_content(self, content: str) -> str:
        """Calculate content hash."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def check_tripwires(self) -> List[Dict]:
        """
        Check all tripwires for modifications or access.
        
        Returns:
            List of triggered tripwires
        """
        triggered = []
        
        for path, info in self.tripwires.items():
            tripwire_path = Path(path)
            
            # Check if file exists
            if not tripwire_path.exists():
                alert = self._trigger_alert(path, 'DELETED', info['severity'])
                triggered.append(alert)
                continue
            
            # Check if modified
            try:
                with open(tripwire_path, 'r') as f:
                    current_content = f.read()
                
                current_hash = self._hash_content(current_content)
                
                if current_hash != info['hash']:
                    alert = self._trigger_alert(path, 'MODIFIED', info['severity'])
                    triggered.append(alert)
                
                # Check access time (if supported)
                stat = tripwire_path.stat()
                created_time = datetime.fromisoformat(info['created']).timestamp()
                
                # If accessed after creation (with small buffer for system noise)
                if stat.st_atime > created_time + 60:
                    alert = self._trigger_alert(path, 'ACCESSED', info['severity'])
                    triggered.append(alert)
            
            except Exception as e:
                alert = self._trigger_alert(path, f'ERROR: {e}', 'critical')
                triggered.append(alert)
        
        return triggered
    
    def _trigger_alert(self, path: str, event: str, severity: str) -> Dict:
        """
        Trigger tripwire alert.
        
        Args:
            path: Tripwire path
            event: Event type (ACCESSED, MODIFIED, DELETED)
            severity: Alert severity
            
        Returns:
            Alert dictionary
        """
        # Update registry
        if path in self.tripwires:
            self.tripwires[path]['triggered'] = True
            self.tripwires[path]['trigger_count'] += 1
            self.tripwires[path]['last_trigger'] = datetime.now().isoformat()
            self._save_registry()
        
        # Create alert
        alert = {
            'timestamp': datetime.now().isoformat(),
            'path': path,
            'event': event,
            'severity': severity,
            'description': self.tripwires.get(path, {}).get('description', ''),
        }
        
        # Log alert
        with open(self.alert_log, 'a') as f:
            f.write(json.dumps(alert) + '\n')
        
        print(f"\n{'='*70}")
        print(f"🚨 TRIPWIRE ALERT")
        print(f"{'='*70}")
        print(f"Path:     {path}")
        print(f"Event:    {event}")
        print(f"Severity: {severity}")
        print(f"Time:     {alert['timestamp']}")
        print(f"{'='*70}\n")
        
        return alert
    
    def remove_tripwire(self, path: str, delete_file: bool = False):
        """
        Remove tripwire from monitoring.
        
        Args:
            path: Tripwire path
            delete_file: If True, also delete the file
        """
        path = str(Path(path).expanduser().resolve())
        if path not in self.tripwires:
            print(f"Tripwire not found: {path}")
            return
        
        # Remove from registry
        del self.tripwires[path]
        self._save_registry()
        
        # Optionally delete file
        if delete_file:
            tripwire_path = Path(path)
            if tripwire_path.exists():
                tripwire_path.unlink()
                print(f"✅ Tripwire removed and deleted: {path}")
            else:
                print(f"✅ Tripwire removed (file already gone): {path}")
        else:
            print(f"✅ Tripwire removed (file kept): {path}")
    
    def list_tripwires(self) -> List[Dict]:
        """
        List all registered tripwires.
        
        Returns:
            List of tripwire info dictionaries
        """
        result = []
        for path, info in self.tripwires.items():
            result.append({
                'path': path,
                **info
            })
        return result
    
    def get_alert_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get alert history.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of alert dictionaries
        """
        if not self.alert_log.exists():
            return []
        
        alerts = []
        with open(self.alert_log, 'r') as f:
            for line in f:
                try:
                    alert = json.loads(line.strip())
                    alerts.append(alert)
                except:
                    continue
        
        # Return most recent first
        alerts.reverse()
        
        if limit:
            return alerts[:limit]
        return alerts


def main():
    """CLI for tripwire management."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Canary Tripwire Manager')
    parser.add_argument('action', choices=['create', 'check', 'list', 'remove', 'alerts'],
                       help='Action to perform')
    parser.add_argument('--path', help='Tripwire path')
    parser.add_argument('--content', help='File content (optional)')
    parser.add_argument('--severity', default='high', choices=['critical', 'high', 'medium', 'low'],
                       help='Alert severity')
    parser.add_argument('--description', default='', help='Tripwire description')
    parser.add_argument('--delete-file', action='store_true', help='Delete file on remove')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    parser.add_argument('--dir', default='.canary_tripwires', help='Tripwire directory')
    
    args = parser.parse_args()
    
    manager = TripwireManager(args.dir)
    
    if args.action == 'create':
        if not args.path:
            print("Error: --path required")
            return
        
        manager.create_tripwire(
            args.path,
            content=args.content,
            severity=args.severity,
            description=args.description
        )
    
    elif args.action == 'check':
        triggered = manager.check_tripwires()
        
        if not triggered:
            print("✅ All tripwires intact")
        else:
            print(f"⚠️  {len(triggered)} tripwire(s) triggered")
    
    elif args.action == 'list':
        tripwires = manager.list_tripwires()
        
        if not tripwires:
            print("No tripwires registered")
        else:
            print(f"\nRegistered Tripwires ({len(tripwires)}):")
            print("-" * 70)
            for tw in tripwires:
                status = "🚨 TRIGGERED" if tw['triggered'] else "✅ OK"
                print(f"{status:15} {tw['path']}")
                print(f"                Severity: {tw['severity']}")
                if tw['description']:
                    print(f"                {tw['description']}")
                if tw['triggered']:
                    print(f"                Triggers: {tw['trigger_count']}")
                print()
    
    elif args.action == 'remove':
        if not args.path:
            print("Error: --path required")
            return
        
        manager.remove_tripwire(args.path, delete_file=args.delete_file)
    
    elif args.action == 'alerts':
        alerts = manager.get_alert_history(limit=args.limit)
        
        if not alerts:
            print("No alerts in history")
        else:
            print(f"\nAlert History ({len(alerts)} total):")
            print("-" * 70)
            for alert in alerts:
                print(f"[{alert['timestamp']}]")
                print(f"  Path:     {alert['path']}")
                print(f"  Event:    {alert['event']}")
                print(f"  Severity: {alert['severity']}")
                if alert.get('description'):
                    print(f"  Info:     {alert['description']}")
                print()


if __name__ == '__main__':
    main()
