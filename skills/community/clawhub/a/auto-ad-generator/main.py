#!/usr/bin/env python3
"""
Auto Ad Generator - Main entry point
Supports both PIL-based and Dreamina (即梦) backend for image generation.
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

def load_config(config_path):
    """Load ad configuration from JSON file."""
    with open(config_path) as f:
        return json.load(f)

def generate_ad_pil(car_image, brand, model, headline, subtitle, slogan, 
                    style="premium", output="ad_output.jpg"):
    """Legacy PIL-based generation (no API required)."""
    from generate_background import generate_background
    from composite_ad import composite_layers, add_text_layers
    
    work_dir = Path("/tmp/auto_ad_work")
    work_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎨 Generating {style} style background (PIL)...")
    bg_path = work_dir / "background.png"
    generate_background(style, str(bg_path), "1080x1920")
    
    print(f"🖼️ Composing layers...")
    temp_composite = work_dir / "composite.png"
    composite_layers(
        str(bg_path),
        car_image,
        str(temp_composite),
        car_scale=0.65,
        car_position="center-bottom"
    )
    
    print(f"✍️ Adding typography...")
    text_config = {
        "headline": f"{brand}{model}" if model else brand,
        "subtitle": subtitle,
        "slogan": slogan
    }
    add_text_layers(str(temp_composite), output, text_config, "luxury")
    
    print(f"✅ Generated: {output}")
    return output

def generate_ad_dreamina(car_image, brand, model, headline, subtitle, slogan,
                         style="premium", platform="xiaohongshu", 
                         brand_type="automotive", output_dir="./output"):
    """
    Dreamina-based generation with AI backgrounds.
    
    Args:
        car_image: Path to car image (will be used with image2image or composited)
        brand: Brand name
        model: Model name
        headline: Main headline
        subtitle: Subtitle text
        slogan: Slogan text
        style: premium/warm/cool/dark/cultural/fragrance/tea
        platform: wechat/xiaohongshu/airport_h/airport_v/lightbox
        brand_type: automotive/cultural/fragrance/tea/recruitment/welfare
        output_dir: Output directory
    """
    from dreamina_backend import generate_ad_background, get_credit
    
    # Check credit
    credit = get_credit()
    if credit:
        print(f"💰 Dreamina Credit: {credit.get('total_credit', 0)}")
    
    # Platform to ratio mapping
    platform_ratios = {
        "wechat": "21:9",      # 900x383 approx
        "xiaohongshu": "3:4",   # 3:4 standard
        "airport_h": "16:9",    # 横屏
        "airport_v": "9:16",    # 竖屏
        "lightbox": "16:9"      # 灯箱通常是横版
    }
    
    ratio = platform_ratios.get(platform, "16:9")
    
    print(f"\n🎯 Generating {platform} ad ({ratio}) with Dreamina...")
    print(f"   Style: {style}, Brand Type: {brand_type}")
    
    # Generate AI background
    result = generate_ad_background(style, ratio, brand_type)
    
    if not result:
        print("❌ Background generation failed")
        return None
    
    submit_id = result.get('submit_id')
    status = result.get('gen_status')
    
    print(f"\n📋 Task submitted:")
    print(f"   Submit ID: {submit_id}")
    print(f"   Status: {status}")
    
    if result.get('result_url'):
        print(f"   Result URL: {result['result_url']}")
    
    # Save task info
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    task_info = {
        "submit_id": submit_id,
        "status": status,
        "platform": platform,
        "ratio": ratio,
        "style": style,
        "brand_type": brand_type,
        "brand": brand,
        "model": model,
        "headline": headline,
        "subtitle": subtitle,
        "slogan": slogan,
        "car_image": str(car_image),
        "result_url": result.get('result_url'),
        "next_step": "Use dreamina query_result to check status, then composite with car image"
    }
    
    info_path = output_path / f"{brand}_{model}_{platform}_task.json"
    with open(info_path, 'w') as f:
        json.dump(task_info, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Task info saved: {info_path}")
    print(f"\n⏭️  Next steps:")
    print(f"   1. Wait for generation: dreamina query_result --submit_id={submit_id}")
    print(f"   2. Download result and composite with car image")
    print(f"   3. Add typography using composite_ad.py")
    
    return task_info

def interactive_mode():
    """Interactive mode - ask user for inputs."""
    print("🚗 广告生成器 (Auto Ad Generator)")
    print("=" * 50)
    
    print("\n选择生成后端:")
    print("1. PIL (本地生成，免费，质量一般)")
    print("2. Dreamina/即梦 (AI生成，消耗积分，质量高)")
    backend_choice = input("选择 (1-2, 默认2): ").strip() or "2"
    
    # Common inputs
    car_image = input("\n产品/车辆图片路径: ").strip()
    brand = input("品牌名称: ").strip()
    model = input("产品/车型: ").strip()
    headline = input("主标题 (默认: 品牌+产品): ").strip() or f"{brand}{model}"
    subtitle = input("副标题: ").strip()
    slogan = input("口号/Slogan: ").strip()
    
    print("\n风格选择:")
    print("1. premium - 蓝紫渐变 (豪华/科技)")
    print("2. warm - 橙粉渐变 (运动/年轻)")
    print("3. cool - 青绿渐变 (环保/现代)")
    print("4. dark - 深色调 (神秘/高端)")
    print("5. cultural - 国风山水 (文旅)")
    print("6. fragrance - 粉金轻奢 (香化)")
    print("7. tea - 禅意自然 (茶叶)")
    style_choice = input("选择风格 (1-7, 默认1): ").strip() or "1"
    
    styles = {
        "1": "premium", "2": "warm", "3": "cool", "4": "dark",
        "5": "cultural", "6": "fragrance", "7": "tea"
    }
    style = styles.get(style_choice, "premium")
    
    if backend_choice == "2":
        print("\n目标平台:")
        print("1. wechat - 公众号头图 (21:9)")
        print("2. xiaohongshu - 小红书封面 (3:4)")
        print("3. airport_h - 机场横屏 (16:9)")
        print("4. airport_v - 机场竖屏 (9:16)")
        print("5. lightbox - 灯箱广告 (16:9)")
        platform_choice = input("选择平台 (1-5, 默认2): ").strip() or "2"
        
        platforms = {
            "1": "wechat", "2": "xiaohongshu", "3": "airport_h",
            "4": "airport_v", "5": "lightbox"
        }
        platform = platforms.get(platform_choice, "xiaohongshu")
        
        # Auto-detect brand type from style
        brand_types = {
            "premium": "automotive", "warm": "automotive", 
            "cool": "automotive", "dark": "automotive",
            "cultural": "cultural", "fragrance": "fragrance", "tea": "tea"
        }
        brand_type = brand_types.get(style, "automotive")
        
        output_dir = input("\n输出目录 (默认: ./output): ").strip() or "./output"
        
        return generate_ad_dreamina(
            car_image, brand, model, headline, subtitle, slogan,
            style, platform, brand_type, output_dir
        )
    else:
        output = input("\n输出路径 (默认: car_ad.jpg): ").strip() or "car_ad.jpg"
        return generate_ad_pil(
            car_image, brand, model, headline, subtitle, slogan, style, output
        )

def main():
    parser = argparse.ArgumentParser(
        description="Generate advertisement posters with PIL or Dreamina AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python main.py
  
  # PIL mode (local generation)
  python main.py --backend pil --car suv.jpg --brand 理想 --model i6 \\
    --subtitle "新形态纯电五座SUV" \\
    --slogan "理想，就是活成自己喜欢的样子"
  
  # Dreamina mode (AI generation)
  python main.py --backend dreamina --car suv.jpg --brand 理想 --model i6 \\
    --subtitle "新形态纯电五座SUV" \\
    --platform xiaohongshu --style premium
  
  # With config file
  python main.py --config ad_config.json
        """
    )
    
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive mode")
    parser.add_argument("--config", "-c", help="Config JSON file")
    parser.add_argument("--backend", choices=["pil", "dreamina"], 
                       default="dreamina", help="Generation backend")
    
    # Content params
    parser.add_argument("--car", "--product", dest="car", help="Product/car image path")
    parser.add_argument("--brand", help="Brand name")
    parser.add_argument("--model", help="Product model name")
    parser.add_argument("--headline", help="Main headline")
    parser.add_argument("--subtitle", help="Subtitle")
    parser.add_argument("--slogan", help="Slogan")
    
    # Style params
    parser.add_argument("--style", default="premium",
                       choices=["premium", "warm", "cool", "dark", "sunset",
                               "cultural", "fragrance", "tea"],
                       help="Visual style")
    parser.add_argument("--platform", default="xiaohongshu",
                       choices=["wechat", "xiaohongshu", "airport_h", 
                               "airport_v", "lightbox"],
                       help="Target platform")
    parser.add_argument("--brand-type", default="automotive",
                       choices=["automotive", "cultural", "fragrance", 
                               "tea", "recruitment", "welfare"],
                       help="Brand/business type")
    
    # Output params
    parser.add_argument("--output", "-o", default="./output",
                       help="Output path (PIL) or directory (Dreamina)")
    
    args = parser.parse_args()
    
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
    elif args.config:
        config = load_config(args.config)
        backend = config.get("backend", "pil")
        if backend == "dreamina":
            generate_ad_dreamina(
                config.get("car_image"),
                config.get("brand"),
                config.get("model", ""),
                config.get("headline", ""),
                config.get("subtitle", ""),
                config.get("slogan", ""),
                config.get("style", "premium"),
                config.get("platform", "xiaohongshu"),
                config.get("brand_type", "automotive"),
                config.get("output", "./output")
            )
        else:
            generate_ad_pil(
                config.get("car_image"),
                config.get("brand"),
                config.get("model", ""),
                config.get("headline", ""),
                config.get("subtitle", ""),
                config.get("slogan", ""),
                config.get("style", "premium"),
                config.get("output", "car_ad.jpg")
            )
    elif args.backend == "dreamina":
        if not args.car:
            print("❌ Error: --car is required")
            parser.print_help()
            sys.exit(1)
        generate_ad_dreamina(
            args.car, args.brand or "", args.model or "",
            args.headline or f"{args.brand}{args.model}",
            args.subtitle or "", args.slogan or "",
            args.style, args.platform, args.brand_type, args.output
        )
    else:
        if not args.car:
            print("❌ Error: --car is required")
            parser.print_help()
            sys.exit(1)
        generate_ad_pil(
            args.car, args.brand or "", args.model or "",
            args.headline or f"{args.brand}{args.model}",
            args.subtitle or "", args.slogan or "",
            args.style, args.output
        )

if __name__ == "__main__":
    main()
