#!/usr/bin/env python3
"""
Diagnostic Report Generator
Generates human-readable diagnostic report from EDID data
Usage: python3 diagnostic_report.py <edid-file>
"""

import sys
import subprocess
import re
import os

def parse_edid(edid_path):
    """Run edid-decode and return output"""
    try:
        result = subprocess.run(
            ['edid-decode', edid_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except FileNotFoundError:
        return "Error: edid-decode not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_value(output, key):
    """Extract value from EDID output"""
    match = re.search(rf'{key}:\s*(.+)', output)
    return match.group(1).strip() if match else None

def generate_report(output):
    """Generate diagnostic report"""
    report = []
    report.append("=" * 60)
    report.append("        EDID 诊断报告 / Diagnostic Report")
    report.append("=" * 60)
    
    # Check for errors first
    if "Error:" in output:
        report.append("\n❌ EDID 解码错误")
        report.append(f"   {output}")
        return "\n".join(report)
    
    if "was empty" in output:
        report.append("\n⚠️  EDID 为空")
        report.append("   可能原因：显示器未连接、处于睡眠模式或线缆问题")
        return "\n".join(report)
    
    # Basic Information
    report.append("\n📺 基本信息")
    report.append("-" * 40)
    
    manufacturer = get_value(output, "Manufacturer")
    model = get_value(output, "Model")
    year = get_value(output, "Made in")
    edid_ver = get_value(output, "EDID Structure Version")
    
    report.append(f"   制造商: {manufacturer or '未知'}")
    report.append(f"   型号: {model or '未知'}")
    if year:
        report.append(f"   生产日期: {year}")
    report.append(f"   EDID 版本: {edid_ver or '未知'}")
    
    # Display Capabilities
    report.append("\n🖥️  显示能力")
    report.append("-" * 40)
    
    # Screen size
    size_match = re.search(r'Maximum image size:\s*(\d+)\s*cm\s*x\s*(\d+)\s*cm', output)
    if size_match:
        w, h = int(size_match.group(1)), int(size_match.group(2))
        diag = ((w**2 + h**2) ** 0.5) / 2.54
        report.append(f"   屏幕尺寸: 约 {diag:.1f} 英寸 ({w}cm x {h}cm)")
    
    # Gamma
    gamma = get_value(output, "Gamma")
    if gamma:
        report.append(f"   Gamma: {gamma}")
    
    # Color format
    if "RGB color display" in output:
        report.append("   色彩格式: RGB")
    if "Supports YCbCr 4:4:4" in output:
        report.append("   YCbCr 4:4:4: ✅ 支持")
    if "Supports YCbCr 4:2:2" in output:
        report.append("   YCbCr 4:2:2: ✅ 支持")
    
    # Resolution & Refresh
    report.append("\n📐 分辨率与刷新率")
    report.append("-" * 40)
    
    # Native resolution
    native_match = re.search(r'Native detailed modes:\s*(\d+)', output)
    if native_match:
        report.append(f"   原生详细模式数: {native_match.group(1)}")
    
    # Get DTD timings (preferred timing)
    dtd_matches = re.findall(r'DTD (\d+):\s+(\d+)x(\d+)\s+(\d+\.?\d*)\s*Hz', output)
    if dtd_matches:
        report.append("   详细时序:")
        for i, (num, w, h, hz) in enumerate(dtd_matches[:3]):
            marker = "⭐" if i == 0 else " "
            report.append(f"     {marker} DTD {num}: {w}x{h} @ {hz}Hz")
    
    # Audio
    report.append("\n🔊 音频能力")
    report.append("-" * 40)
    
    if "Basic audio support" in output or "Audio Data Block" in output:
        report.append("   音频: ✅ 支持")
        
        # Audio formats
        if "Linear PCM" in output:
            report.append("   - PCM: ✅")
        if "AC-3" in output or "Dolby" in output:
            report.append("   - AC-3/Dolby: ✅")
        if "DTS" in output:
            report.append("   - DTS: ✅")
        if "Enhanced AC-3" in output or "DD+" in output:
            report.append("   - Dolby Digital+: ✅")
    else:
        report.append("   音频: ❌ 不支持")
    
    # Warnings & Issues
    report.append("\n⚠️  诊断结果")
    report.append("-" * 40)
    
    issues = []
    
    # Check for common issues
    if not native_match:
        issues.append("无原生分辨率")
    
    if "underscanned" in output.lower():
        issues.append("默认underscan，可能需要调整")
    
    if "overscanned" in output.lower():
        issues.append("默认overscan，可能需要调整")
    
    # Check monitor ranges
    if "Monitor ranges" not in output and "Display Range Limits" not in output:
        issues.append("无显示器范围限制信息")
    
    # Check for valid timings
    if not dtd_matches:
        issues.append("无详细时序描述符")
    
    if issues:
        for issue in issues:
            report.append(f"   - {issue}")
    else:
        report.append("   ✅ 未发现明显问题")
    
    # Conformity
    if "EDID conformity: FAIL" in output:
        report.append("\n🔴 EDID 合规性: 失败")
        # Extract failure reason
        fail_match = re.search(r'Failures:(.*?)(?:^$|\Z)', output, re.MULTILINE | re.DOTALL)
        if fail_match:
            report.append(f"   {fail_match.group(1).strip()[:200]}")
    else:
        report.append("\n🟢 EDID 合规性: 通过")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 diagnostic_report.py <edid-file>")
        print("Example: python3 diagnostic_report.py /sys/class/drm/card0-HDMI-A-1/edid")
        sys.exit(1)
    
    edid_path = sys.argv[1]
    
    if not os.path.exists(edid_path):
        print(f"Error: File not found: {edid_path}")
        sys.exit(1)
    
    print(f"正在分析: {edid_path}")
    print("-" * 40)
    
    output = parse_edid(edid_path)
    report = generate_report(output)
    print(report)

if __name__ == "__main__":
    main()