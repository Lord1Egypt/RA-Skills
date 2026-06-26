#!/usr/bin/env python3
"""Auto-Claw Image Optimizer 演示"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.image_optimizer import ImageOptimizer

SITE_URL = "http://linghangyuan1234.dpdns.org"
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"

BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw Image Optimizer                   ║
║       图片扫描 · 分析 · 优化命令                 ║
╚══════════════════════════════════════════════════════════╝"""

def main():
    print(BANNER)
    
    optimizer = ImageOptimizer(web_root=WEB_ROOT, site_url=SITE_URL)
    
    print("\n" + "="*60)
    print("  第1步：扫描图片")
    print("="*60)
    
    report = optimizer.run_full_analysis()
    
    print("\n" + "="*60)
    print("  第2步：汇总")
    print("="*60)
    
    print(f"\n  总图片数: {report.total_images}")
    print(f"  总体积: {report.total_size_mb:.2f}MB")
    print(f"  可节省: {report.potential_savings_mb:.2f}MB")
    print(f"  优化后: {report.optimized_size_mb:.2f}MB")
    
    if report.recommendations:
        for rec in report.recommendations:
            print(f"  {rec}")
    
    if report.images:
        print("\n  图片列表:")
        for img in report.images[:10]:
            print(f"  - {img.url} ({img.size_kb:.1f}KB)")
            for issue in img.issues:
                print(f"    ⚠️  {issue[:60]}")
    else:
        print("\n  (暂无上传图片，工具已就绪)")
    
    print("\n" + "="*60)
    print("  第3步：优化命令示例")
    print("="*60)
    
    print("\n  # JPG压缩（需安装jpegoptim）")
    print("  jpegoptim --max=85 --size=200k /path/to/image.jpg")
    print("\n  # PNG压缩（需安装optipng）")
    print("  optipng -o5 /path/to/image.png")
    print("\n  # WebP生成（需安装cwebp）")
    print("  cwebp -q 80 /path/to/image.jpg -o /path/to/image.webp")
    
    print("\n" + "="*60)
    print("  ✅ 图片优化分析完成")
    print("="*60)
    print("""
  能力 #15 完成: Image Optimizer ✅
  
  技术实现：
    ✅ 图片扫描 (wp-content/uploads)
    ✅ 格式分析 (JPG/PNG/GIF/WebP)
    ✅ 压缩建议与命令生成
    ✅ WebP生成命令
    ✅ 批量命令导出
    
  可扩展：
    → 自动执行压缩
    → WordPress插件集成
    → CDN自动同步
""")

if __name__ == "__main__":
    main()
