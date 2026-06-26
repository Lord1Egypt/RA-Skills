"""
train_handwriting_model.py — 手写数字识别模型微调流水线

三步:
1. 合成训练数据 (Handright)
2. 基于 CnOCR number 模型微调
3. 导出 ONNX 并集成到 pipeline
"""
import os, sys, random, subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TRAIN_DIR = SKILL_DIR / 'training'
DATA_DIR = TRAIN_DIR / 'data' / 'synthetic'
MODEL_DIR = TRAIN_DIR / 'models'
FONTS_DIR = TRAIN_DIR / 'fonts'

def step1_generate_data(count=5000):
    """用 Handright 生成手写日期训练数据"""
    print(f'[Step 1] Generating {count} synthetic handwritten dates...')
    
    from datetime import datetime, timedelta
    from handright import Template, handwrite
    from PIL import Image, ImageFont
    
    # Find available handwriting fonts
    font_files = list(FONTS_DIR.glob('*.ttf')) + list(FONTS_DIR.glob('*.TTC')) + list(FONTS_DIR.glob('*.TTF'))
    if not font_files:
        print('No fonts found, using PIL default')
        return []
    
    print(f'  Fonts: {len(font_files)} available')
    
    # Generate random dates (2018-2026)
    start = datetime(2018, 1, 1)
    end = datetime(2026, 12, 31)
    dates = []
    for _ in range(count):
        delta = random.randint(0, (end - start).days)
        d = start + timedelta(days=delta)
        dates.append(d.strftime('%Y年%m月%d日'))
    
    # Create output dir
    os.makedirs(str(DATA_DIR), exist_ok=True)
    samples = []
    
    for i, date_str in enumerate(dates):
        font_path = str(random.choice(font_files))
        try:
            font = ImageFont.truetype(font_path, 48)
        except:
            continue
        
        template = Template(
            background=Image.new('RGB', (600, 80), (255, 255, 255)),
            font_size=48,
            font=font,
            line_spacing=1.0,
            fill_priority_color=(0, 0, 0),
            perturb_x_sigma=2,
            perturb_y_sigma=2,
            perturb_threshold=1,
        )
        
        images = handwrite(date_str, template)
        for j, img in enumerate(images):
            path = str(DATA_DIR / f'date_{i:05d}_{j}.png')
            if hasattr(img, 'save'):
                img.save(path)
            else:
                Image.fromarray(img).save(path)
            samples.append((path, date_str))
        
        if (i+1) % 1000 == 0:
            print(f'  Generated {i+1}/{count}', flush=True)
    
    print(f'  Total: {len(samples)} images')
    return samples

def step2_create_training_files(samples):
    """创建 CnOCR 训练格式 TSV"""
    print('[Step 2] Creating training TSV files...')
    
    random.shuffle(samples)
    split = int(len(samples) * 0.9)
    train = samples[:split]
    eval_s = samples[split:]
    
    train_path = TRAIN_DIR / 'train.tsv'
    eval_path = TRAIN_DIR / 'eval.tsv'
    
    with open(str(train_path), 'w', encoding='utf-8') as f:
        for img_path, label in train:
            f.write(f"{os.path.abspath(img_path)}\t{label}\n")
    
    with open(str(eval_path), 'w', encoding='utf-8') as f:
        for img_path, label in eval_s:
            f.write(f"{os.path.abspath(img_path)}\t{label}\n")
    
    print(f'  Train: {len(train)} samples -> {train_path}')
    print(f'  Eval:  {len(eval_s)} samples -> {eval_path}')
    return train_path, eval_path

def step3_finetune(train_tsv, eval_tsv, epochs=20):
    """微调 CnOCR number 模型"""
    print(f'[Step 3] Fine-tuning CnOCR number model ({epochs} epochs)...')
    
    # The training command is: cnocr train -m base_model_name --train-file train.tsv --eval-file eval.tsv
    cmd = [
        sys.executable, '-m', 'cnocr', 'train',
        '-m', 'number-densenet_lite_136-gru',
        '--train-file', str(train_tsv),
        '--eval-file', str(eval_tsv),
        '--epoch', str(epochs),
        '--output-dir', str(MODEL_DIR / 'finetuned'),
    ]
    
    print(f'  Running: {\" \".join(cmd)}')
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f'  Training completed!')
        print(f'  Output: {MODEL_DIR / "finetuned"}')
    else:
        print(f'  Training failed: {result.stderr[:500]}')
    
    return result.returncode == 0

def step4_export_onnx():
    """导出微调后的模型为 ONNX"""
    print('[Step 4] Exporting to ONNX...')
    
    model_path = MODEL_DIR / 'finetuned' / 'model.pth'
    if not model_path.exists():
        print(f'  Model not found at {model_path}')
        return False
    
    import torch
    from cnocr import CnOcr
    
    # Load fine-tuned model
    ocr = CnOcr(model_name=str(MODEL_DIR / 'finetuned'))
    
    # Create dummy input and export
    dummy = torch.randn(1, 1, 32, 320)
    
    onnx_path = MODEL_DIR / 'handwriting_date_model.onnx'
    torch.onnx.export(
        ocr.model,
        dummy,
        str(onnx_path),
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {3: 'width'}},
        opset_version=12
    )
    
    print(f'  ONNX model exported: {onnx_path}')
    print(f'  Size: {onnx_path.stat().st_size / 1024 / 1024:.1f} MB')
    return True


if __name__ == '__main__':
    print('=' * 50)
    print('Handwriting Date Recognition Model Training')
    print('=' * 50)
    
    # Step 1
    samples = step1_generate_data(5000)
    if not samples:
        print('ERROR: No training data generated')
        sys.exit(1)
    
    # Step 2
    train_path, eval_path = step2_create_training_files(samples)
    
    # Step 3
    success = step3_finetune(str(train_path), str(eval_path), epochs=20)
    if not success:
        print('ERROR: Training failed')
        sys.exit(1)
    
    # Step 4
    step4_export_onnx()
    
    print()
    print('=' * 50)
    print('Training pipeline complete!')
    print(f'Model: {MODEL_DIR / "handwriting_date_model.onnx"}')
    print('=' * 50)
