"""
ClawScan License Manager
Simple license validation for paid features
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict


class LicenseManager:
    """Manage licenses for ClawScan paid features"""
    
    FREE_MONTHLY_SCANS = 5
    
    def __init__(self):
        self.config_dir = Path.home() / ".clawscan"
        self.license_file = self.config_dir / "license.json"
        self.usage_file = self.config_dir / "usage.json"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Create config directory if needed"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_usage(self) -> Dict:
        """Load usage statistics"""
        if not self.usage_file.exists():
            return {"scans_this_month": 0, "month": datetime.now().month, "year": datetime.now().year}
        
        try:
            data = json.loads(self.usage_file.read_text())
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Reset if new month
            if data.get("month") != current_month or data.get("year") != current_year:
                return {"scans_this_month": 0, "month": current_month, "year": current_year}
            
            return data
        except:
            return {"scans_this_month": 0, "month": datetime.now().month, "year": datetime.now().year}
    
    def _save_usage(self, usage: Dict):
        """Save usage statistics"""
        self.usage_file.write_text(json.dumps(usage, indent=2))
    
    def get_remaining_free_scans(self) -> int:
        """Get number of free scans remaining this month"""
        usage = self._load_usage()
        remaining = self.FREE_MONTHLY_SCANS - usage.get("scans_this_month", 0)
        return max(0, remaining)
    
    def record_scan(self) -> bool:
        """
        Record a scan attempt.
        Returns True if allowed, False if quota exceeded.
        """
        # Check if has valid license first
        if self.has_valid_license():
            return True
        
        # Check free quota
        usage = self._load_usage()
        if usage.get("scans_this_month", 0) < self.FREE_MONTHLY_SCANS:
            usage["scans_this_month"] = usage.get("scans_this_month", 0) + 1
            self._save_usage(usage)
            return True
        
        return False
    
    def has_valid_license(self) -> bool:
        """Check if user has valid paid license"""
        if not self.license_file.exists():
            return False
        
        try:
            license_data = json.loads(self.license_file.read_text())
            
            # Check expiration
            expires = license_data.get("expires")
            if expires:
                expiry_date = datetime.fromisoformat(expires)
                if datetime.now() > expiry_date:
                    return False
            
            # Verify license key format (basic check)
            key = license_data.get("key", "")
            if not self._verify_key_format(key):
                return False
            
            return True
            
        except:
            return False
    
    def _verify_key_format(self, key: str) -> bool:
        """Basic license key format verification"""
        # Format: CLAW-XXXX-XXXX-XXXX
        parts = key.split("-")
        if len(parts) != 4 or parts[0] != "CLAW":
            return False
        
        # Check each part is 4 alphanumeric chars
        for part in parts[1:]:
            if len(part) != 4 or not part.isalnum():
                return False
        
        return True
    
    def activate_license(self, key: str) -> bool:
        """
        Activate a license key.
        Returns True if successful.
        """
        if not self._verify_key_format(key):
            return False
        
        # In real implementation, would verify with server
        # For now, accept any properly formatted key
        license_data = {
            "key": key,
            "activated": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=365)).isoformat(),
            "type": "personal",
            "verified": False  # Would be True after server verification
        }
        
        self.license_file.write_text(json.dumps(license_data, indent=2))
        return True
    
    def get_license_info(self) -> Optional[Dict]:
        """Get license information if exists"""
        if not self.has_valid_license():
            return None
        
        try:
            return json.loads(self.license_file.read_text())
        except:
            return None
    
    def deactivate(self):
        """Remove license (for testing/refunds)"""
        if self.license_file.exists():
            self.license_file.unlink()


# Global instance
_license_manager = None

def get_license_manager() -> LicenseManager:
    """Get singleton license manager instance"""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager
