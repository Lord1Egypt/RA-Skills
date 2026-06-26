#!/usr/bin/env python3
"""
Test CPU mode feasibility for Fooocus
Checks if CPU mode can work without CUDA
"""

import sys
import subprocess

def test_pytorch_cpu():
    """Test if PyTorch CPU version works"""
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} installed")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
            return "cuda"
        else:
            print("⚠️  CUDA not available, CPU mode only")
            
            # Test CPU tensor operations
            try:
                x = torch.randn(100, 100)
                y = torch.matmul(x, x)
                print("✅ CPU tensor operations work")
                return "cpu"
            except Exception as e:
                print(f"❌ CPU operations failed: {e}")
                return "failed"
                
    except ImportError:
        print("❌ PyTorch not installed")
        return "not_installed"

def test_fooocus_cpu_compatibility():
    """Check Fooocus CPU compatibility"""
    print("\n" + "="*60)
    print("Fooocus CPU Mode Feasibility Test")
    print("="*60)
    
    # Test 1: PyTorch
    pytorch_status = test_pytorch_cpu()
    
    if pytorch_status == "not_installed":
        print("\n📦 Installation required:")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
        return False
    
    if pytorch_status == "failed":
        print("\n❌ PyTorch CPU mode not working properly")
        return False
    
    # Test 2: Other dependencies
    deps = ["PIL", "numpy", "requests"]
    missing = []
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep} available")
        except ImportError:
            print(f"❌ {dep} missing")
            missing.append(dep)
    
    if missing:
        print(f"\n📦 Install missing dependencies:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    # Test 3: Estimate performance
    print("\n" + "="*60)
    print("Performance Estimate (CPU Mode)")
    print("="*60)
    
    if pytorch_status == "cpu":
        print("⚠️  CPU mode will be VERY SLOW")
        print("   Expected time per image:")
        print("   - 512x512, 4 steps (lightning): 2-5 minutes")
        print("   - 512x512, 20 steps: 10-20 minutes")
        print("   - 1024x1024, 30 steps: 30-60 minutes")
        print("\n💡 Recommendations:")
        print("   1. Use --preset lightning with --steps 4")
        print("   2. Reduce resolution to 512x512")
        print("   3. Consider Google Colab for free GPU")
    
    return True

def test_fooocus_installation():
    """Test if Fooocus can be installed"""
    import os
    from pathlib import Path
    
    fooocus_path = Path.home() / "Fooocus"
    
    print("\n" + "="*60)
    print("Fooocus Installation Check")
    print("="*60)
    
    if fooocus_path.exists():
        print(f"✅ Fooocus found at {fooocus_path}")
        
        # Check key files
        required = ["webui.py", "entry_with_update.py"]
        missing = [f for f in required if not (fooocus_path / f).exists()]
        
        if missing:
            print(f"❌ Missing files: {missing}")
            return False
        
        print("✅ Installation looks complete")
        return True
    else:
        print(f"❌ Fooocus not found at {fooocus_path}")
        print("\n📦 To install:")
        print("   python scripts/install_fooocus.py")
        return False

def test_model_download():
    """Check if models can be downloaded"""
    import urllib.request
    
    print("\n" + "="*60)
    print("Model Download Check")
    print("="*60)
    
    test_urls = [
        ("https://huggingface.co", "HuggingFace"),
        ("https://github.com", "GitHub"),
        ("https://civitai.com", "Civitai")
    ]
    
    for url, name in test_urls:
        try:
            req = urllib.request.Request(url, method="HEAD")
            req.add_header("User-Agent", "Fooocus-Test/1.0")
            with urllib.request.urlopen(req, timeout=10) as _:
                print(f"✅ {name} accessible")
        except Exception as e:
            print(f"⚠️  {name} may be blocked: {e}")
    
    print("\n📦 Model download requirement:")
    print("   - First run downloads ~6GB of models")
    print("   - Requires stable internet connection")
    print("   - May take 10-30 minutes")

def main():
    print("="*60)
    print("Fooocus CPU Mode Test")
    print("="*60)
    print("\nThis test checks if Fooocus can run in CPU mode")
    print("(without NVIDIA GPU)\n")
    
    # Run tests
    pytorch_ok = test_fooocus_cpu_compatibility()
    install_ok = test_fooocus_installation()
    test_model_download()
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    if pytorch_ok and install_ok:
        print("✅ CPU mode is FEASIBLE")
        print("\n⚠️  WARNING: CPU mode is extremely slow!")
        print("   Only recommended for testing or when GPU is unavailable")
        print("\nTo start Fooocus in CPU mode:")
        print("   cd ~/Fooocus")
        print("   python entry_with_update.py --always-low-vram")
        print("\nTo generate with CPU optimizations:")
        print("   python scripts/generate.py --prompt 'test' --cpu-optimize")
    elif not pytorch_ok:
        print("❌ Cannot run: PyTorch not properly installed")
        print("\nTo install PyTorch (CPU version):")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    elif not install_ok:
        print("❌ Cannot run: Fooocus not installed")
        print("\nTo install Fooocus:")
        print("   python scripts/install_fooocus.py")
    
    print("\n" + "="*60)
    print("Alternative: Google Colab (Free GPU)")
    print("="*60)
    print("If CPU mode is too slow, use:")
    print("   https://colab.research.google.com/github/lllyasviel/Fooocus/blob/main/fooocus_colab.ipynb")

if __name__ == "__main__":
    main()
