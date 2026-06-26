#!/usr/bin/env python3
"""
Extract key information from EDID in structured format (Bilingual: Chinese/English).
Usage: ./extract_info.py <edid-file-or-path> [--lang zh|en]
"""

import sys
import subprocess
import re
import json
import os
import argparse

# Language strings
LANG = {
    'zh': {
        'title': '📺 显示器信息',
        'subtitle': '🖥️  显示能力',
        'audio_title': '🔊 音频',
        'color_title': '🎨 色彩特性',
        'issue_title': '⚠️  问题/备注',
        'json_title': '📄 JSON 输出',
        'manufacturer': '制造商',
        'model': '型号',
        'product_code': '产品代码',
        'serial': '序列号',
        'made_in': '生产日期',
        'edid_version': 'EDID版本',
        'preferred': '首选分辨率',
        'max': '最大分辨率',
        'audio': '音频',
        'supported': '支持',
        'not_supported': '不支持',
        'YCbCr_444': 'YCbCr 4:4:4',
        'YCbCr_422': 'YCbCr 4:2:2',
        'red': '红',
        'green': '绿',
        'blue': '蓝',
        'white': '白',
        'limited': '分辨率支持有限',
        'empty': '⚠️  EDID为空',
        'error': '❌ EDID解析错误',
        'parsing': '正在解析EDID',
        'week': '第{}周',
        'year': '年',
    },
    'en': {
        'title': '📺 Display Information',
        'subtitle': '🖥️  Display Capabilities',
        'audio_title': '🔊 Audio',
        'color_title': '🎨 Color Characteristics',
        'issue_title': '⚠️  Issues/Notes',
        'json_title': '📄 JSON Output',
        'manufacturer': 'Manufacturer',
        'model': 'Model',
        'product_code': 'Product Code',
        'serial': 'Serial Number',
        'made_in': 'Made in',
        'edid_version': 'EDID Version',
        'preferred': 'Preferred',
        'max': 'Max Resolution',
        'audio': 'Audio',
        'supported': 'Supported',
        'not_supported': 'Not Supported',
        'YCbCr_444': 'YCbCr 4:4:4',
        'YCbCr_422': 'YCbCr 4:2:2',
        'red': 'Red',
        'green': 'Green',
        'blue': 'Blue',
        'white': 'White',
        'limited': 'Limited resolution support',
        'empty': '⚠️  EDID is empty',
        'error': '❌ EDID parse error',
        'parsing': 'Parsing EDID',
        'week': 'Week {}',
        'year': '',
    }
}

def get_lang():
    """Detect language from args or environment"""
    # Check command line args first
    for arg in sys.argv[1:]:
        if arg == '--lang' or arg.startswith('--lang='):
            return 'zh' if 'zh' in arg else 'en'
    
    # Check environment
    lang = os.environ.get('LANG', '')
    if 'zh' in lang.lower():
        return 'zh'
    return 'en'

# Get current language (will be set in main after parsing args)
L = None

def get_L():
    """Get language dict based on current context"""
    global L
    if L is None:
        lang = 'zh'
        # Check command line args first
        for arg in sys.argv[1:]:
            if arg == '--lang' or arg.startswith('--lang='):
                if 'en' in arg:
                    lang = 'en'
                    break
        # Check environment
        if lang == 'zh':
            lang_env = os.environ.get('LANG', '')
            if 'zh' not in lang_env.lower():
                lang = 'en'
        L = LANG[lang]
    return L

def parse_edid(edid_path):
    """Run edid-decode and parse output."""
    try:
        result = subprocess.run(
            ['edid-decode', edid_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        return output
    except FileNotFoundError:
        return "Error: edid-decode not found. Install with: sudo apt-get install edid-decode"
    except subprocess.TimeoutExpired:
        return "Error: edid-decode timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def extract_info(output):
    """Extract key information from edid-decode output."""
    info = {
        "status": "unknown",
        "manufacturer": None,
        "model": None,
        "product_code": None,
        "serial": None,
        "week": None,
        "year": None,
        "edid_version": None,
        "preferred_timing": None,
        "supported_resolutions": [],
        "max_resolution": None,
        "audio_support": False,
        "YCbCr_444": False,
        "YCbCr_422": False,
        "color_info": {},
        "issues": []
    }
    
    # Check for errors
    if "Error:" in output:
        info["issues"].append("EDID decode error")
        info["status"] = "error"
        return info
    
    if "was empty" in output:
        info["issues"].append("EDID is empty")
        info["status"] = "empty"
        return info
    
    info["status"] = "ok"
    
    # Extract manufacturer
    match = re.search(r'Manufacturer:\s*(.+)', output)
    if match:
        info["manufacturer"] = match.group(1).strip()
    
    # Extract model
    match = re.search(r'Model:\s*(\S+)', output)
    if match:
        info["model"] = match.group(1).strip()
    
    # Extract product code
    match = re.search(r'Product code:\s*(0x[0-9a-fA-F]+)', output)
    if match:
        info["product_code"] = match.group(1).strip()
    
    # Extract serial
    match = re.search(r'Serial number:\s*(\S+)', output)
    if match:
        info["serial"] = match.group(1).strip()
    
    # Extract week/year
    match = re.search(r'Made in:\s*week (\d+) of (\d+)', output)
    if match:
        info["week"] = match.group(1).strip()
        info["year"] = match.group(2).strip()
    
    # Extract EDID version
    match = re.search(r'EDID Structure Version & Revision:\s*(.+)', output)
    if match:
        info["edid_version"] = match.group(1).strip()
    
    # Extract max resolution - Priority: DTD native > VIC > DMT
    resolutions = []
    max_area = 0
    max_res = None
    
    # Step 1: Get Detailed Timing Descriptors (DTD)
    for m in re.finditer(r'DTD \d+:\s+(\d+)x(\d+)\s+(\d+\.?\d*)\s*Hz', output):
        w, h, hz = int(m.group(1)), int(m.group(2)), float(m.group(3))
        res = f"{w}x{h}@{hz}"
        if res not in resolutions:
            resolutions.append(res)
        area = w * h
        if area > max_area:
            max_area = area
            max_res = f"{w}x{h} @ {hz}Hz"
    
    # Step 2: If no DTD found, fall back to VIC
    if not max_res:
        for m in re.finditer(r'VIC\s+\d+:\s+(\d+)x(\d+)\s+(\d+\.?\d*)\s*Hz', output):
            w, h, hz = int(m.group(1)), int(m.group(2)), float(m.group(3))
            res = f"{w}x{h}@{hz}"
            if res not in resolutions:
                resolutions.append(res)
            area = w * h
            if area > max_area:
                max_area = area
                max_res = f"{w}x{h} @ {hz}Hz"
    
    # Step 3: Fall back to DMT
    if not max_res:
        for m in re.finditer(r'DMT 0x\d+:\s+(\d+)x(\d+)\s+(\d+\.?\d*)\s*Hz', output):
            w, h, hz = int(m.group(1)), int(m.group(2)), float(m.group(3))
            res = f"{w}x{h}@{hz}"
            if res not in resolutions:
                resolutions.append(res)
            area = w * h
            if area > max_area:
                max_area = area
                max_res = f"{w}x{h} @ {hz}Hz"
    
    info["supported_resolutions"] = resolutions[:50]
    info["max_resolution"] = max_res
    
    # Check audio support
    if "Basic audio support" in output or "Audio Data Block" in output:
        info["audio_support"] = True
    
    # Check YCbCr support
    if "Supports YCbCr 4:4:4" in output:
        info["YCbCr_444"] = True
    if "Supports YCbCr 4:2:2" in output:
        info["YCbCr_422"] = True
    
    # === Feature 5: HDMI Version Detection ===
    # HDMI version can be inferred from supported features
    hdmi_info = {}
    if "HDMI" in output:
        hdmi_info["present"] = True
        # Check for HDMI 2.1 features
        if "ALLM" in output or "VRR" in output:
            hdmi_info["version"] = "2.1"
            hdmi_info["features"] = ["ALLM", "VRR"]
        elif "420" in output:
            hdmi_info["version"] = "2.0"
        else:
            hdmi_info["version"] = "1.4"
    
    # Check for eARC
    if "eARC" in output or "Enhanced audio" in output:
        hdmi_info["earc"] = True
    
    info["hdmi"] = hdmi_info
    
    # === Feature 6: Color Space Analysis ===
    info["color_space"] = {
        "rgb": True,  # Almost all digital displays support RGB
        "ycbcr_444": info["YCbCr_444"],
        "ycbcr_422": info["YCbCr_422"]
    }
    
    # === Feature 7: Audio Capabilities ===
    info["audio"] = {"support": info["audio_support"], "formats": []}
    if "Linear PCM" in output:
        info["audio"]["formats"].append("PCM")
    if "AC-3" in output or "Dolby" in output:
        info["audio"]["formats"].append("Dolby Digital")
    if "DTS" in output:
        info["audio"]["formats"].append("DTS")
    if "Enhanced AC-3" in output or "DD+" in output:
        info["audio"]["formats"].append("Dolby Digital Plus")
    if "DTS-HD" in output:
        info["audio"]["formats"].append("DTS-HD")
    if "TrueHD" in output:
        info["audio"]["formats"].append("Dolby TrueHD")
    if "Atmos" in output:
        info["audio"]["formats"].append("Dolby Atmos")
    
    # === Feature 8: DDC/CI Support ===
    # DDC/CI is indicated by having a valid DDC structure
    info["ddc"] = {"support": False}
    if "DDC/CI" in output or "I2C" in output:
        info["ddc"]["support"] = True
    
    # === Feature: HDR Support ===
    info["hdr"] = {"support": False, "types": []}
    if "HDR" in output:
        info["hdr"]["support"] = True
    if "HDR10" in output:
        info["hdr"]["types"].append("HDR10")
    if "Dolby Vision" in output:
        info["hdr"]["types"].append("Dolby Vision")
    if "HLG" in output:
        info["hdr"]["types"].append("HLG")
    
    # === Feature: VRR (Variable Refresh Rate) ===
    info["vrr"] = {"support": False, "types": []}
    if "VRR" in output or "Variable" in output:
        info["vrr"]["support"] = True
        info["vrr"]["types"].append("HDMI VRR")
    if "FreeSync" in output:
        info["vrr"]["types"].append("AMD FreeSync")
    if "G-Sync" in output or "G-SYNC" in output:
        info["vrr"]["types"].append("NVIDIA G-Sync")
    
    # Extract color characteristics
    match = re.search(r'Red\s+:\s+([\d.]+),\s*([\d.]+)', output)
    if match:
        info["color_info"]["red"] = {"x": match.group(1), "y": match.group(2)}
    match = re.search(r'Green:\s+([\d.]+),\s*([\d.]+)', output)
    if match:
        info["color_info"]["green"] = {"x": match.group(1), "y": match.group(2)}
    match = re.search(r'Blue\s+:\s+([\d.]+),\s*([\d.]+)', output)
    if match:
        info["color_info"]["blue"] = {"x": match.group(1), "y": match.group(2)}
    match = re.search(r'White:\s+([\d.]+),\s*([\d.]+)', output)
    if match:
        info["color_info"]["white"] = {"x": match.group(1), "y": match.group(2)}
    
    # Check for issues
    if not info["manufacturer"]:
        info["issues"].append("Unknown manufacturer")
    if not info["model"]:
        info["issues"].append("Unknown model")
    if info["supported_resolutions"]:
        if len(info["supported_resolutions"]) < 5:
            # Use default English for issue since language not set yet
            info["issues"].append("Limited resolution support")
    
    return info

def main():
    global L
    # Determine language from args/env
    lang = 'zh'
    for arg in sys.argv[1:]:
        if arg == '--lang' or arg.startswith('--lang='):
            if 'en' in arg:
                lang = 'en'
                break
    if lang == 'zh':
        lang_env = os.environ.get('LANG', '')
        if 'zh' not in lang_env.lower():
            lang = 'en'
    L = LANG[lang]
    
    if len(sys.argv) < 2:
        print("Usage: extract_info.py <edid-file-or-path> [--lang zh|en]")
        print("Example: extract_info.py /sys/class/drm/card0-HDMI-A-1/edid")
        print("Example: extract_info.py /path/to/edid.bin --lang en")
        sys.exit(1)
    
    edid_path = sys.argv[1]
    
    print(f"{L['parsing']}: {edid_path}")
    print("=" * 50)
    
    output = parse_edid(edid_path)
    info = extract_info(output)
    
    # Print human-readable summary
    print(f"\n{L['title']}:")
    print("-" * 30)
    
    if info["status"] == "empty":
        print(L['empty'])
        sys.exit(1)
    elif info["status"] == "error":
        print(L['error'])
        for issue in info["issues"]:
            print(f"   - {issue}")
        sys.exit(1)
    
    if info["manufacturer"]:
        print(f"   {L['manufacturer']}: {info['manufacturer']}")
    if info["model"]:
        print(f"   {L['model']}: {info['model']}")
    if info["product_code"]:
        print(f"   {L['product_code']}: {info['product_code']}")
    if info["week"] and info["year"]:
        print(f"   {L['made_in']}: {L['week'].format(info['week'])}, {info['year']}")
    if info["edid_version"]:
        print(f"   {L['edid_version']}: {info['edid_version']}")
    
    print(f"\n{L['subtitle']}:")
    print("-" * 30)
    if info["preferred_timing"]:
        print(f"   {L['preferred']}: {info['preferred_timing']}")
    if info["max_resolution"]:
        print(f"   {L['max']}: {info['max_resolution']}")
    if info["audio_support"]:
        print(f"   🔊 {L['audio']}: {L['supported']}")
    if info["YCbCr_444"]:
        print(f"   🎨 {L['YCbCr_444']}: {L['supported']}")
    if info["YCbCr_422"]:
        print(f"   🎨 {L['YCbCr_422']}: {L['supported']}")
    
    if info["color_info"]:
        print(f"\n{L['color_title']}:")
        print("-" * 30)
        for color, coords in info["color_info"].items():
            print(f"   {color.capitalize()}: x={coords['x']}, y={coords['y']}")
    
    if info["issues"]:
        print(f"\n{L['issue_title']}:")
        print("-" * 30)
        for issue in info["issues"]:
            print(f"   - {issue}")
    
    # Print JSON for programmatic use
    print(f"\n{L['json_title']}:")
    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()