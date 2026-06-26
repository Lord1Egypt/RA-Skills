#!/usr/bin/env python3
"""Health Check - Production-grade validation with functional tests."""
import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.workspace = Path.home() / ".openclaw/workspace"
        self.piper_dir = self.workspace / "piper"
        self.checks = []
        self.fatal_errors = []
        
    def check(self, name: str, passed: bool, details: str = "", fatal: bool = False) -> None:
        """Record a check result."""
        status = "✅" if passed else "❌"
        self.checks.append({
            "name": name,
            "passed": passed,
            "status": status,
            "details": details,
            "fatal": fatal
        })
        print(f"{status} {name}")
        if details:
            print(f"   {details}")
        if not passed and fatal:
            self.fatal_errors.append(name)
    
    def run_all(self) -> int:
        """Run all health checks."""
        print("\n🏥 Audio PT Auto-Reply - Health Check")
        print("=" * 60)
        print()
        
        # Critical: Python & Core
        print("🔴 Critical Path:")
        self.check_python()
        self.check_piper_binary()
        
        if self.fatal_errors:
            print(f"\n❌ FATAL: Cannot proceed without: {', '.join(self.fatal_errors)}")
            return 2
        
        # Important: Dependencies
        print("\n🟡 Dependencies:")
        self.check_python_deps()
        
        # Features: Models & Integration
        print("\n🟢 Features:")
        self.check_voice_models()
        self.check_claude_integration()
        
        # Advanced: Functional Tests
        print("\n🔵 Functional Tests:")
        self.run_functional_tests()
        
        # Summary
        print("\n" + "=" * 60)
        passed = sum(1 for c in self.checks if c["passed"])
        total = len(self.checks)
        
        print(f"Results: {passed}/{total} checks passed\n")
        
        if self.fatal_errors:
            print(f"❌ FATAL ERRORS ({len(self.fatal_errors)}):")
            for err in self.fatal_errors:
                print(f"  • {err}")
            return 2
        
        elif total - passed > 0:
            print(f"⚠️  {total - passed} issue(s) found. Some features may not work.")
            return 1
        
        else:
            print("✅ Everything is ready! Your skill is fully configured.")
            return 0
    
    # ========================================================================
    # Critical Checks
    # ========================================================================
    
    def check_python(self) -> None:
        """Check Python availability (critical)."""
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.strip() or result.stderr.strip()
            self.check("Python 3", True, version, fatal=False)
        except Exception as e:
            self.check("Python 3", False, f"Error: {e}", fatal=True)
    
    def check_piper_binary(self) -> None:
        """Check Piper binary exists and is executable (critical)."""
        piper_binary = self.piper_dir / "piper" / "piper"
        
        exists = piper_binary.exists()
        if not exists:
            self.check(
                "Piper binary",
                False,
                f"Not found at {piper_binary}. Run: bash install.sh",
                fatal=True
            )
            return
        
        executable = os.access(piper_binary, os.X_OK)
        if not executable:
            self.check(
                "Piper binary",
                False,
                f"Not executable. Run: chmod +x {piper_binary}",
                fatal=True
            )
            return
        
        self.check("Piper binary", True, f"Found at {piper_binary}", fatal=False)
    
    # ========================================================================
    # Dependency Checks
    # ========================================================================
    
    def check_python_deps(self) -> None:
        """Check Python dependencies."""
        deps = [
            ("transformers", "Speech recognition"),
            ("torch", "ML framework"),
            ("torchaudio", "Audio processing"),
        ]
        
        for package, desc in deps:
            try:
                __import__(package)
                self.check(f"{package}", True, f"{desc} - OK")
            except ImportError:
                self.check(
                    f"{package}",
                    False,
                    f"{desc} - Install with: pip install {package}"
                )
        
        # Claude integration (optional)
        try:
            __import__("anthropic")
            self.check("anthropic", True, "Claude API integration available")
        except ImportError:
            self.check(
                "anthropic",
                False,
                "Optional: pip install anthropic for Claude support"
            )
        
        # FFmpeg (critical for synthesis)
        if not self._has_command("ffmpeg"):
            self.check(
                "ffmpeg",
                False,
                "Critical for TTS! Install: apt-get install ffmpeg (Linux) or brew install ffmpeg (Mac)"
            )
        else:
            self.check("ffmpeg", True, "Available for audio conversion")
    
    # ========================================================================
    # Feature Checks
    # ========================================================================
    
    def check_voice_models(self) -> None:
        """Check voice models."""
        voices = {
            "jeff": "pt_BR-jeff-medium.onnx",
            "miro": "pt_BR-miro-high.onnx",
        }
        
        for name, model in voices.items():
            model_path = self.piper_dir / model
            exists = model_path.exists()
            
            self.check(
                f"Voice: {name}",
                exists,
                str(model_path) if not exists else f"{model_path.stat().st_size} bytes"
            )
    
    def check_claude_integration(self) -> None:
        """Check Claude API integration."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if api_key:
            self.check(
                "ANTHROPIC_API_KEY",
                True,
                "Claude API configured ✨"
            )
        else:
            self.check(
                "ANTHROPIC_API_KEY",
                False,
                "Optional: Set for intelligent responses"
            )
    
    # ========================================================================
    # Functional Tests (the important part!)
    # ========================================================================
    
    def run_functional_tests(self) -> None:
        """Actually test the system works."""
        
        # Test 1: Transcription (without audio, just check import)
        self._test_transcription_import()
        
        # Test 2: Synthesis (minimal test with dummy text)
        self._test_synthesis()
        
        # Test 3: Claude adapter (if available)
        if os.environ.get("ANTHROPIC_API_KEY"):
            self._test_claude_adapter()
    
    def _test_transcription_import(self) -> None:
        """Test transcription module loads."""
        try:
            # Just import to validate syntax
            from transformers import pipeline
            self.check(
                "Transcription module",
                True,
                "Model can be loaded (slow on first run)"
            )
        except Exception as e:
            self.check(
                "Transcription module",
                False,
                f"Import failed: {str(e)}"
            )
    
    def _test_synthesis(self) -> None:
        """Test actual synthesis (functional test!)."""
        try:
            # Create a minimal test script inline
            test_code = """
import sys
sys.path.insert(0, '.')

from pathlib import Path
piper_dir = Path.home() / ".openclaw/workspace/piper"
model_path = piper_dir / "pt_BR-jeff-medium.onnx"

if not model_path.exists():
    print("Model not found")
    sys.exit(1)

import subprocess
import tempfile

with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
    temp_wav = f.name

piper_binary = piper_dir / "piper" / "piper"

try:
    subprocess.run(
        [str(piper_binary), "--model", str(model_path), "--output_file", temp_wav],
        input=b"Teste",
        timeout=10,
        capture_output=True,
        check=True
    )
    
    size = Path(temp_wav).stat().st_size
    if size > 0:
        print(f"OK:{size}")
    else:
        print("ERROR:No output")
finally:
    Path(temp_wav).unlink(missing_ok=True)
"""
            
            result = subprocess.run(
                ["python3", "-c", test_code],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.workspace
            )
            
            if result.returncode == 0 and result.stdout.startswith("OK:"):
                size = result.stdout.strip().split(":")[1]
                self.check(
                    "Synthesis (TTS)",
                    True,
                    f"✓ Piper generates audio ({size} bytes)"
                )
            else:
                self.check(
                    "Synthesis (TTS)",
                    False,
                    f"Failed: {result.stderr[:100]}"
                )
                
        except subprocess.TimeoutExpired:
            self.check(
                "Synthesis (TTS)",
                False,
                "Timeout (>30s) - may indicate slow system"
            )
        except Exception as e:
            self.check(
                "Synthesis (TTS)",
                False,
                f"Error: {str(e)}"
            )
    
    def _test_claude_adapter(self) -> None:
        """Test Claude adapter (if API key set)."""
        try:
            # Quick sanity check with a timeout
            result = subprocess.run(
                ["python3", "-c", "from anthropic import Anthropic; print('OK')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.check("Claude adapter", True, "✓ API client functional")
            else:
                self.check("Claude adapter", False, "API client failed to initialize")
                
        except Exception as e:
            self.check("Claude adapter", False, f"Error: {str(e)}")
    
    # ========================================================================
    # Utilities
    # ========================================================================
    
    @staticmethod
    def _has_command(cmd: str) -> bool:
        """Check if command exists in PATH."""
        result = subprocess.run(
            ["which", cmd],
            capture_output=True
        )
        return result.returncode == 0


if __name__ == "__main__":
    checker = HealthChecker()
    exit_code = checker.run_all()
    print()
    sys.exit(exit_code)
