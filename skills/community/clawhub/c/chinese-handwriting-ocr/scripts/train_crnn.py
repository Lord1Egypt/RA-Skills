"""
train_crnn.py — 从零训练手写数字CRNN模型（仅13类字符：0-9 + 年月日）
无需下载预训练模型，直接合成数据 + PyTorch训练 + ONNX导出
"""
import os, sys, random, argparse
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F

SKILL_DIR = Path(__file__).parent.parent
TRAIN_DIR = SKILL_DIR / 'training'
DATA_DIR = TRAIN_DIR / 'data' / 'synthetic'
MODEL_DIR = TRAIN_DIR / 'models'
FONTS_DIR = TRAIN_DIR / 'fonts'

# 字符集: 数字0-9 + 年月日
# blank at index 0, then digits, then date chars
VOCAB = ['0','1','2','3','4','5','6','7','8','9','年','月','日']
# CTC blank should be last char or separate. We'll use VOCAB[0]='0' as blank
# Better: add explicit blank at index 0, shift others
# Actually PyTorch CTCLoss uses blank=0 by default
# So VOCAB[0] is the blank, and real chars start from 1
# But we trained with VOCAB[0]='0'... Let me fix this properly:
# blank is 0, chars: 0-9 at 1-10, 年月日 at 11-13
ALL_CHARS = ['','0','1','2','3','4','5','6','7','8','9','年','月','日']  # index 0 = blank
CHAR_MAP = {c:i for i,c in enumerate(ALL_CHARS)}
NUM_CLASSES = len(ALL_CHARS)  # 14 (blank + 13 real chars)

# ─── CRNN Model ────────────────────────────────────────
class CRNN(nn.Module):
    """CRNN + CTC for sequence recognition"""
    def __init__(self, img_h=32, n_channel=1, n_class=NUM_CLASSES, n_hidden=256):
        super().__init__()
        
        self.cnn = nn.Sequential(
            nn.Conv2d(n_channel, 64, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, 1, 1), nn.ReLU(),
            nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(2, (2,1)),
            nn.Conv2d(256, 512, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(2, (2,1)),
        )
        
        self.rnn = nn.LSTM(1024, n_hidden, bidirectional=True, batch_first=True, num_layers=2)
        self.fc = nn.Linear(n_hidden * 2, n_class)
    
    def forward(self, x):
        x = self.cnn(x)
        b, c, h, w = x.size()
        x = x.permute(0, 3, 1, 2).contiguous().view(b, w, c * h)  # (B, W', C*H)
        x, _ = self.rnn(x)
        x = x.permute(1, 0, 2)  # (T, B, H*2)
        x = self.fc(x)
        return x

# ─── Dataset ────────────────────────────────────────────
class SynthDateDataset(Dataset):
    def __init__(self, num_samples=3000, is_train=True):
        self.samples = self._generate(num_samples)
    
    def _generate(self, n):
        from PIL import Image, ImageDraw, ImageFont
        font_files = list(FONTS_DIR.glob('*.ttf')) + list(FONTS_DIR.glob('*.ttc')) + list(FONTS_DIR.glob('*.TTC'))
        if not font_files:
            font_files = list(Path(r'C:\Windows\Fonts').glob('*.ttf'))
        
        start = datetime(2018, 1, 1)
        end = datetime(2026, 12, 31)
        samples = []
        
        for _ in range(n):
            delta = random.randint(0, (end - start).days)
            d = start + timedelta(days=delta)
            label = d.strftime('%Y年%m月%d日')
            
            img = Image.new('L', (400, 48), 255)
            draw = ImageDraw.Draw(img)
            font_path = str(random.choice(font_files)) if font_files else None
            
            try:
                font = ImageFont.truetype(font_path, 36) if font_path else ImageFont.load_default()
                draw.text((10, 8), label, fill=0, font=font)
            except:
                continue
            
            # Augment: slight rotation, noise
            img = np.array(img)
            if random.random() > 0.5:
                angle = random.uniform(-2, 2)
                from scipy.ndimage import rotate
                img = rotate(img, angle, reshape=False, cval=255)
            if random.random() > 0.5:
                noise = np.random.normal(0, 15, img.shape)
                img = np.clip(img + noise, 0, 255).astype(np.uint8)
            
            samples.append((img, label))
        
        return samples
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img, label = self.samples[idx]
        # Resize to (32, 320)
        from PIL import Image as PILImage
        img = PILImage.fromarray(img).resize((320, 32))
        img = np.array(img).astype(np.float32) / 255.0
        img = 1.0 - img  # Invert: black text on white -> white text on black? No, keep as-is
        img = torch.FloatTensor(img).unsqueeze(0)  # (1, 32, 320)
        
        # Encode label
        target = [CHAR_MAP[c] for c in label]  # Now 0='', 1='0', 2='1', etc.
        target_len = len(target)
        
        return img, torch.LongTensor(target), target_len

# ─── CTC Beam Decoder ──────────────────────────────────
def decode_ctc(output, blank=0):
    """Greedy CTC decoder"""
    output = F.softmax(output, dim=2)
    preds = output.argmax(dim=2)  # (T, B)
    preds = preds[:, 0].tolist()
    
    # Collapse repeats and remove blanks
    prev = -1
    decoded = []
    for p in preds:
        if p != blank and p != prev:
            if p < len(ALL_CHARS) and p > 0:  # skip blank (0)
                decoded.append(p)
        prev = p
    
    return ''.join([ALL_CHARS[p] for p in decoded])

# ─── Training ──────────────────────────────────────────
def train(model, train_loader, val_loader, epochs=30, device='cpu'):
    model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    ctc_loss = nn.CTCLoss(blank=0, zero_infinity=True)  # blank at index 0
    
    best_acc = 0
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for imgs, targets, target_lens in train_loader:
            imgs = imgs.to(device)
            
            optimizer.zero_grad()
            output = model(imgs)  # (T, B, C)
            T, B, C = output.shape
            
            # CTC Loss requires log_softmax
            output_log = F.log_softmax(output, dim=2)
            input_lens = torch.full((B,), T, dtype=torch.long)
            loss = ctc_loss(output_log, targets, input_lens, target_lens)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for imgs, targets, target_lens in val_loader:
                imgs = imgs.to(device)
                output = model(imgs)
                
                pred = decode_ctc(output)
                gt = ''.join([ALL_CHARS[t] for t in targets[0].tolist()])
                correct += (pred == gt)
                total += 1
        
        acc = correct / max(total, 1) * 100
        print(f'Epoch {epoch+1}/{epochs}: loss={total_loss/len(train_loader):.4f}, val_acc={acc:.1f}%', flush=True)
        
        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), str(MODEL_DIR / 'best_crnn.pth'))
    
    print(f'Best validation accuracy: {best_acc:.1f}%', flush=True)
    return best_acc

# ─── ONNX Export ───────────────────────────────────────
def export_onnx(model, device='cpu'):
    model.to('cpu')
    model.eval()
    
    dummy = torch.randn(1, 1, 32, 320)
    
    onnx_path = str(MODEL_DIR / 'handwriting_date_crnn.onnx')
    torch.onnx.export(
        model, dummy, onnx_path,
        input_names=['input'], output_names=['output'],
        dynamic_axes={'input': {3: 'width'}},
        opset_version=12
    )
    
    size = os.path.getsize(onnx_path) / 1024 / 1024
    print(f'ONNX exported: {onnx_path} ({size:.1f} MB)', flush=True)
    return onnx_path

# ─── Main ──────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', type=int, default=3000, help='Training samples')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--device', default='cpu')
    args = parser.parse_args()
    
    os.makedirs(str(MODEL_DIR), exist_ok=True)
    os.makedirs(str(DATA_DIR), exist_ok=True)
    
    print('Generating training data...', flush=True)
    train_ds = SynthDateDataset(args.samples, is_train=True)
    val_ds = SynthDateDataset(max(200, args.samples//10), is_train=False)
    
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=1)
    
    print(f'Train: {len(train_ds)}, Val: {len(val_ds)}', flush=True)
    
    model = CRNN()
    total_params = sum(p.numel() for p in model.parameters())
    print(f'Model params: {total_params/1024:.1f}K', flush=True)
    
    acc = train(model, train_loader, val_loader, args.epochs, args.device)
    
    export_onnx(model)
    
    print(f'\nTraining complete! Accuracy: {acc:.1f}%', flush=True)
    print(f'Model: {MODEL_DIR / "handwriting_date_crnn.onnx"}', flush=True)
