#!/usr/bin/env python3
"""
Quick test script to verify all skill functions work correctly
Run this after installation to confirm everything works
"""
import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and show result"""
    print(f"\n🔍 Testing: {description}")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed! Error: {e.stderr.strip()}")
        return False

def main():
    print("="*60)
    print("📊 Data Analysis for Feishu - Quick Test Script")
    print("="*60)
    print("This script will test all core functions to ensure they work correctly.")
    print("Generated test charts will be saved to ./test_output/ directory.\n")
    
    # Create output directory
    os.makedirs("test_output", exist_ok=True)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Basic funnel chart
    tests_total += 1
    cmd = f"python scripts/main.py --type funnel --title 'User Conversion Funnel' --labels 'Visit' 'Register' 'Add to Cart' 'Purchase' 'Repurchase' --values 10000 4500 2200 1200 500 --output test_output/funnel.png"
    if run_command(cmd, "Basic funnel chart generation"):
        tests_passed +=1
    
    # Test 2: Line chart
    tests_total +=1
    cmd = f"python scripts/main.py --type line --title 'Weekly Traffic' --x-axis 'Mon' 'Tue' 'Wed' 'Thu' 'Fri' 'Sat' 'Sun' --y-axis 1200 1500 1350 1680 1820 2100 1950 --y-name 'Visits' --area --output test_output/line.png"
    if run_command(cmd, "Line chart with area fill"):
        tests_passed +=1
    
    # Test 3: Bar chart
    tests_total +=1
    cmd = f"python scripts/main.py --type bar --title 'Sales by Region' --x-axis 'East' 'North' 'South' 'West' 'Northwest' 'Northeast' --y-axis 120 98 85 62 45 38 --y-name 'Sales (10k)' --output test_output/bar.png"
    if run_command(cmd, "Bar chart generation"):
        tests_passed +=1
    
    # Test 4: Pie chart
    tests_total +=1
    cmd = f"python scripts/main.py --type pie --title 'Revenue Composition' --labels 'Product Sales' 'Service' 'Licensing' 'Others' --values 65 20 10 5 --output test_output/pie.png"
    if run_command(cmd, "Pie chart generation"):
        tests_passed +=1
    
    # Test 5: Gauge chart
    tests_total +=1
    cmd = f"python scripts/main.py --type gauge --title 'Annual Target Completion' --value 75 --max 100 --unit '%' --output test_output/gauge.png"
    if run_command(cmd, "Gauge chart generation"):
        tests_passed +=1
    
    # Test 6: Dual axis chart
    tests_total +=1
    cmd = f"python scripts/main.py --type dual_axis --title 'Monthly Sales & Growth' --x-axis 'Jan' 'Feb' 'Mar' 'Apr' 'May' 'Jun' --y1-axis 120 150 135 180 210 240 --y1-name 'Sales (k)' --y2-axis 0 25 -10 33.3 16.7 14.3 --y2-name 'Growth (%)' --output test_output/dual_axis.png"
    if run_command(cmd, "Dual axis chart generation"):
        tests_passed +=1
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 Test Summary: {tests_passed}/{tests_total} tests passed")
    print("="*60)
    
    if tests_passed == tests_total:
        print("✅ All tests passed! The skill is working correctly.")
        print(f"📁 Test charts saved to: {os.path.abspath('test_output')}")
        print("\n🚀 You can now start using the skill for your data analysis tasks!")
        return 0
    else:
        print(f"❌ {tests_total - tests_passed} tests failed. Please check the error messages above.")
        print("💡 Common issues: Missing dependencies, network problem (for Chromium download), permission issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
