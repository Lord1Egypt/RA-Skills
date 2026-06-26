#!/usr/bin/env python3
import datetime
"""
Agent Security Scanner v4.1.0 - 发布前完整验证脚本

用途：验证发布包是否完整、可运行、符合质量要求
使用：python3 release_validator.py
"""

import os
import sys
import json
from pathlib import Path

# 配置
RELEASE_DIR = Path(__file__).parent
REQUIRED_FILES = {
    # 核心代码
    'src/multi_language_scanner_v4.py': '主扫描器',
    'src/fast_batch_scan.py': '批量扫描入口',
    'src/intent_detector_v2.py': '意图分析器',
    'src/llm_analyzer.py': 'LLM 分析器',
    'src/engine/smart_pattern_detector.py': '智能评分系统',
    
    # 配置
    'config/quality_gate.yaml': '质量门禁配置',
    
    # npm/技能
    'package.json': 'npm 配置',
    'SKILL.md': '技能规范',
    
    # 文档
    'README.md': '项目说明',
    'LICENSE': '许可证',
    'requirements.txt': '依赖列表',
}

REQUIRED_FEATURES = {
    'whitelist_patterns': '白名单模式',
    'blacklist_patterns': '黑名单模式',
    'SmartScanner': '智能评分系统',
    'EnhancedIntentDetector': '意图分析器',
    'LLMAnalyzer': 'LLM 分析器',
}

QUALITY_THRESHOLDS = {
    'detection_rate': 85.0,
    'false_positive_rate': 15.0,
    'speed': 4000,
}


class ReleaseValidator:
    """发布包验证器"""
    
    def __init__(self, release_dir: Path):
        self.release_dir = release_dir
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def validate_files(self):
        """验证必要文件是否存在"""
        print("="*70)
        print("1️⃣  验证必要文件")
        print("="*70)
        
        for file_path, description in REQUIRED_FILES.items():
            full_path = self.release_dir / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                self.passed.append(f"✅ {file_path} ({size:,} bytes)")
                print(f"  ✅ {file_path:<50} {description}")
            else:
                self.errors.append(f"❌ {file_path} - {description}")
                print(f"  ❌ {file_path:<50} {description} (缺失)")
        
        print()
    
    def validate_code_quality(self):
        """验证代码质量"""
        print("="*70)
        print("2️⃣  验证代码功能")
        print("="*70)
        
        # 测试扫描器加载
        try:
            sys.path.insert(0, str(self.release_dir / 'src'))
            from multi_language_scanner_v4 import MultiLanguageScanner
            scanner = MultiLanguageScanner()
            self.passed.append("✅ 扫描器可正常加载")
            print("  ✅ 扫描器可正常加载")
        except Exception as e:
            self.errors.append(f"❌ 扫描器加载失败：{e}")
            print(f"  ❌ 扫描器加载失败：{e}")
        
        # 验证必要功能
        scanner_code = (self.release_dir / 'src' / 'multi_language_scanner_v4.py').read_text()
        for feature, description in REQUIRED_FEATURES.items():
            if feature in scanner_code:
                self.passed.append(f"✅ {description}")
                print(f"  ✅ {description}")
            else:
                self.errors.append(f"❌ {description} (代码中未找到 {feature})")
                print(f"  ❌ {description} (代码中未找到 {feature})")
        
        print()
    
    def validate_benchmark(self):
        """验证性能指标"""
        print("="*70)
        print("3️⃣  验证性能指标")
        print("="*70)
        
        validation_file = self.release_dir / 'pre_release_validation.json'
        if not validation_file.exists():
            self.warnings.append("⚠️  缺少验证报告 (pre_release_validation.json)")
            print("  ⚠️  缺少验证报告 (pre_release_validation.json)")
            print()
            return
        
        try:
            with open(validation_file) as f:
                data = json.load(f)
            
            metrics = data.get('metrics', {})
            dr = metrics.get('detection_rate', 0)
            fpr = metrics.get('false_positive_rate', 100)
            speed = metrics.get('speed', 0)
            
            # 检测率
            if dr >= QUALITY_THRESHOLDS['detection_rate']:
                self.passed.append(f"✅ 检测率 {dr}% ≥ {QUALITY_THRESHOLDS['detection_rate']}%")
                print(f"  ✅ 检测率 {dr}% ≥ {QUALITY_THRESHOLDS['detection_rate']}%")
            else:
                self.errors.append(f"❌ 检测率 {dr}% < {QUALITY_THRESHOLDS['detection_rate']}%")
                print(f"  ❌ 检测率 {dr}% < {QUALITY_THRESHOLDS['detection_rate']}%")
            
            # 误报率
            if fpr <= QUALITY_THRESHOLDS['false_positive_rate']:
                self.passed.append(f"✅ 误报率 {fpr}% ≤ {QUALITY_THRESHOLDS['false_positive_rate']}%")
                print(f"  ✅ 误报率 {fpr}% ≤ {QUALITY_THRESHOLDS['false_positive_rate']}%")
            else:
                self.errors.append(f"❌ 误报率 {fpr}% > {QUALITY_THRESHOLDS['false_positive_rate']}%")
                print(f"  ❌ 误报率 {fpr}% > {QUALITY_THRESHOLDS['false_positive_rate']}%")
            
            # 速度
            if speed >= QUALITY_THRESHOLDS['speed']:
                self.passed.append(f"✅ 速度 {speed}/s ≥ {QUALITY_THRESHOLDS['speed']}/s")
                print(f"  ✅ 速度 {speed}/s ≥ {QUALITY_THRESHOLDS['speed']}/s")
            else:
                self.errors.append(f"❌ 速度 {speed}/s < {QUALITY_THRESHOLDS['speed']}/s")
                print(f"  ❌ 速度 {speed}/s < {QUALITY_THRESHOLDS['speed']}/s")
        
        except Exception as e:
            self.warnings.append(f"⚠️  读取验证报告失败：{e}")
            print(f"  ⚠️  读取验证报告失败：{e}")
        
        print()
    
    def generate_report(self):
        """生成验证报告"""
        print("="*70)
        print("📊 验证报告")
        print("="*70)
        print()
        
        total_checks = len(self.passed) + len(self.errors) + len(self.warnings)
        passed = len(self.passed)
        errors = len(self.errors)
        warnings = len(self.warnings)
        
        print(f"总检查项：{total_checks}")
        print(f"通过：    {passed} ✅")
        print(f"错误：    {errors} ❌")
        print(f"警告：    {warnings} ⚠️")
        print()
        
        if self.errors:
            print("错误列表:")
            for error in self.errors:
                print(f"  {error}")
            print()
        
        if self.warnings:
            print("警告列表:")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        # 最终判定
        print("="*70)
        if errors == 0:
            print("✅ 验证通过 - 可以发布")
            return True
        else:
            print("❌ 验证失败 - 需要修复")
            return False


def main():
    """主函数"""
    print("="*70)
    print("Agent Security Scanner v4.1.0 - 发布前验证")
    print("="*70)
    print()
    
    validator = ReleaseValidator(RELEASE_DIR)
    
    # 执行验证
    validator.validate_files()
    validator.validate_code_quality()
    validator.validate_benchmark()
    
    # 生成报告
    passed = validator.generate_report()
    
    # 保存报告
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '4.1.0',
        'passed': passed,
        'total_checks': len(validator.passed) + len(validator.errors) + len(validator.warnings),
        'passed_count': len(validator.passed),
        'errors': validator.errors,
        'warnings': validator.warnings,
    }
    
    report_file = RELEASE_DIR / 'validation_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n验证报告已保存：{report_file}")
    
    # 返回状态码
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
