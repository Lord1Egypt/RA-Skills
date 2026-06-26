"""
generate_training_data.py — 合成手写日期训练数据生成器
生成日期图片用于微调手写数字识别模型
"""
import os, re, random
from datetime import datetime, timedelta

class DateDataGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_date_list(self, num_samples=5000, start_year=2018, end_year=2026):
        """生成随机日期列表"""
        start = datetime(start_year, 1, 1)
        end = datetime(end_year, 12, 31)
        dates = []
        for _ in range(num_samples):
            delta = random.randint(0, (end - start).days)
            d = start + timedelta(days=delta)
            dates.append(d.strftime('%Y年%m月%d日'))
        return dates
    
    def generate_with_handright(self, date_list, font_paths=None):
        """用Handright生成手写体日期图片"""
        try:
            from handright import Template, handwrite
            from PIL import Image, ImageFont
            
            if not font_paths:
                # Use system handwriting fonts
                font_paths = [
                    r'C:\Windows\Fonts\BRUSHSCI.TTF',
                    r'C:\Windows\Fonts\LHANDW.TTF',
                    r'C:\Windows\Fonts\FRSCRIPT.TTF',
                ]
                # Filter to existing files
                font_paths = [f for f in font_paths if os.path.exists(f)]
            
            if not font_paths:
                print("No handwriting fonts found, using PIL default")
                return self._generate_pil_basic(date_list)
            
            template = Template(
                background=Image.new('RGB', (600, 80), (255, 255, 255)),
                font_size=48,
                font=ImageFont.truetype(random.choice(font_paths), 48),
                line_spacing=1.0,
                fill_priority_color=(0, 0, 0),
                perturb_x_sigma=2,
                perturb_y_sigma=2,
                perturb_threshold=1,
            )
            
            samples = []
            for i, date_str in enumerate(date_list):
                images = handwrite(date_str, template)
                for j, img in enumerate(images):
                    path = os.path.join(self.output_dir, f'date_{i:05d}_{j}.png')
                    if hasattr(img, 'save'):
                        img.save(path)
                    else:
                        Image.fromarray(img).save(path)
                    label = date_str
                    samples.append((path, label))
            
            return samples
        
        except ImportError:
            print("Handright not available, falling back to PIL")
            return self._generate_pil_basic(date_list)
    
    def _generate_pil_basic(self, date_list):
        """Fallback: use PIL to generate basic training images"""
        from PIL import Image, ImageDraw, ImageFont
        
        samples = []
        font = None
        
        for fp in [
            r'C:\Windows\Fonts\BRUSHSCI.TTF',
            r'C:\Windows\Fonts\LHANDW.TTF',
            r'C:\Windows\Fonts\FRSCRIPT.TTF',
        ]:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, 48)
                    break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
        
        for i, label in enumerate(date_list):
            img = Image.new('RGB', (600, 80), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.text((20, 15), label, fill=(0, 0, 0), font=font)
            path = os.path.join(self.output_dir, f'date_{i:05d}.png')
            img.save(path)
            samples.append((path, label))
        
        return samples
    
    def create_cnocr_training_files(self, samples, split_ratio=0.9):
        """创建CnOCR训练格式的TSV文件"""
        random.shuffle(samples)
        split = int(len(samples) * split_ratio)
        train = samples[:split]
        eval_s = samples[split:]
        
        train_path = os.path.join(self.output_dir, '..', 'train.tsv')
        eval_path = os.path.join(self.output_dir, '..', 'eval.tsv')
        
        with open(train_path, 'w', encoding='utf-8') as f:
            for img_path, label in train:
                f.write(f"{os.path.abspath(img_path)}\t{label}\n")
        
        with open(eval_path, 'w', encoding='utf-8') as f:
            for img_path, label in eval_s:
                f.write(f"{os.path.abspath(img_path)}\t{label}\n")
        
        print(f"Created {train_path} ({len(train)} samples)")
        print(f"Created {eval_path} ({len(eval_s)} samples)")
        return train_path, eval_path


if __name__ == '__main__':
    import sys
    
    output_dir = os.path.join(os.path.dirname(__file__) or '.', 'data', 'synthetic_dates')
    gen = DateDataGenerator(output_dir)
    
    print("Generating date list...")
    dates = gen.generate_date_list(5000)
    
    print("Generating handwritten date images...")
    samples = gen.generate_with_handright(dates)
    
    print(f"Created {len(samples)} training samples")
    
    print("Creating CnOCR training files...")
    gen.create_cnocr_training_files(samples)
    
    print("Done! Training data ready at:", output_dir)
