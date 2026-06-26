#!/usr/bin/env python3
"""
Baby Photo Book Generator
Generate professional baby photo books with intelligent layout optimization.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from PIL import Image, ExifTags
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import argparse


class PhotoLayoutEngine:
    """Intelligent layout engine that minimizes whitespace"""
    
    def __init__(self, page_width, page_height):
        self.page_w = page_width
        self.page_h = page_height
        self.margin = 0.3 * cm
        self.gap = 0.2 * cm
        self.avail_w = page_width - 2 * self.margin
        self.avail_h = page_height - 2 * self.margin
    
    def get_aspect(self, photo_path):
        try:
            img = Image.open(photo_path)
            return img.width / img.height
        except:
            return 1.0
    
    def calculate_layout(self, photos):
        """Calculate optimal layout to minimize whitespace"""
        n = len(photos)
        if n == 0:
            return []
        
        aspects = [self.get_aspect(p['path']) for p in photos]
        
        if n == 1:
            return self._layout_1(photos[0], aspects[0])
        elif n == 2:
            return self._layout_2(photos, aspects)
        elif n == 3:
            return self._layout_3(photos, aspects)
        else:
            return self._layout_4(photos, aspects)
    
    def _layout_1(self, photo, aspect):
        """Single photo - maximize to fill page"""
        if aspect > self.avail_w / self.avail_h:
            w = self.avail_w
            h = w / aspect
        else:
            h = self.avail_h
            w = h * aspect
        
        x = self.margin + (self.avail_w - w) / 2
        y = self.margin + (self.avail_h - h) / 2
        return [(photo, (x, y, x + w, y + h))]
    
    def _layout_2(self, photos, aspects):
        """Two photos - side by side or stacked"""
        a1, a2 = aspects[0], aspects[1]
        
        # Try horizontal arrangement
        h = self.avail_h
        w1 = h * a1
        w2 = h * a2
        
        if w1 + w2 + self.gap <= self.avail_w:
            total_w = w1 + w2 + self.gap
            start_x = self.margin + (self.avail_w - total_w) / 2
            y = self.margin + (self.avail_h - h) / 2
            blank1 = self.avail_w * self.avail_h - (w1 * h + w2 * h)
        else:
            scale = (self.avail_w - self.gap) / (w1 + w2)
            w1 *= scale
            w2 *= scale
            h *= scale
            start_x = self.margin
            y = self.margin + (self.avail_h - h) / 2
            blank1 = self.avail_w * self.avail_h - (w1 * h + w2 * h)
        
        # Try vertical arrangement
        w = self.avail_w
        h1 = w / a1
        h2 = w / a2
        
        if h1 + h2 + self.gap <= self.avail_h:
            total_h = h1 + h2 + self.gap
            start_y = self.margin + (self.avail_h - total_h) / 2
            blank2 = self.avail_w * self.avail_h - (w * h1 + w * h2)
        else:
            scale = (self.avail_h - self.gap) / (h1 + h2)
            h1 *= scale
            h2 *= scale
            w *= scale
            start_y = self.margin
            blank2 = self.avail_w * self.avail_h - (w * h1 + w * h2)
        
        if blank1 <= blank2:
            y = self.margin + (self.avail_h - h) / 2
            return [
                (photos[0], (start_x, y, start_x + w1, y + h)),
                (photos[1], (start_x + w1 + self.gap, y, start_x + w1 + self.gap + w2, y + h))
            ]
        else:
            x = self.margin + (self.avail_w - w) / 2
            return [
                (photos[0], (x, start_y + h2 + self.gap, x + w, start_y + h2 + self.gap + h1)),
                (photos[1], (x, start_y, x + w, start_y + h2))
            ]
    
    def _layout_3(self, photos, aspects):
        """Three photos - intelligent split"""
        a1, a2, a3 = aspects
        
        # Find best photo for left side (portrait preferred)
        vertical_scores = [(i, 1 / a) for i, a in enumerate(aspects)]
        left_idx = max(range(3), key=lambda i: vertical_scores[i][1])
        right_idxs = [i for i in range(3) if i != left_idx]
        
        left_w = self.avail_w * 0.5 - self.gap / 2
        right_w = self.avail_w * 0.5 - self.gap / 2
        
        h_left = min(self.avail_h, left_w / aspects[left_idx])
        w_left = h_left * aspects[left_idx]
        
        right_h = (self.avail_h - self.gap) / 2
        w_r1 = min(right_w, right_h * aspects[right_idxs[0]])
        h_r1 = w_r1 / aspects[right_idxs[0]]
        w_r2 = min(right_w, right_h * aspects[right_idxs[1]])
        h_r2 = w_r2 / aspects[right_idxs[1]]
        
        used_area1 = w_left * h_left + w_r1 * h_r1 + w_r2 * h_r2
        blank1 = self.avail_w * self.avail_h - used_area1
        
        # Try top-bottom arrangement
        horizontal_scores = [(i, a) for i, a in enumerate(aspects)]
        top_idx = max(range(3), key=lambda i: horizontal_scores[i][1])
        bottom_idxs = [i for i in range(3) if i != top_idx]
        
        top_h = self.avail_h * 0.5 - self.gap / 2
        bottom_h = self.avail_h * 0.5 - self.gap / 2
        
        w_top = min(self.avail_w, top_h * aspects[top_idx])
        h_top = w_top / aspects[top_idx]
        
        bottom_w = (self.avail_w - self.gap) / 2
        h_b1 = min(bottom_h, bottom_w / aspects[bottom_idxs[0]])
        w_b1 = h_b1 * aspects[bottom_idxs[0]]
        h_b2 = min(bottom_h, bottom_w / aspects[bottom_idxs[1]])
        w_b2 = h_b2 * aspects[bottom_idxs[1]]
        
        used_area2 = w_top * h_top + w_b1 * w_b1 + w_b2 * w_b2
        blank2 = self.avail_w * self.avail_h - used_area2
        
        if blank1 <= blank2:
            y_left = self.margin + (self.avail_h - h_left) / 2
            x_left = self.margin + (left_w - w_left) / 2
            
            x_right = self.margin + left_w + self.gap + (right_w - max(w_r1, w_r2)) / 2
            y_r1 = self.margin + right_h + self.gap + (right_h - h_r1) / 2
            y_r2 = self.margin + (right_h - h_r2) / 2
            
            result = [None] * 3
            result[left_idx] = (photos[left_idx], (x_left, y_left, x_left + w_left, y_left + h_left))
            result[right_idxs[0]] = (photos[right_idxs[0]], (x_right, y_r1, x_right + w_r1, y_r1 + h_r1))
            result[right_idxs[1]] = (photos[right_idxs[1]], (x_right, y_r2, x_right + w_r2, y_r2 + h_r2))
            return result
        else:
            x_top = self.margin + (self.avail_w - w_top) / 2
            y_top = self.margin + self.avail_h - h_top - (top_h - h_top) / 2
            
            y_bottom = self.margin + (bottom_h - max(h_b1, h_b2)) / 2
            x_b1 = self.margin + (bottom_w - w_b1) / 2
            x_b2 = self.margin + bottom_w + self.gap + (bottom_w - w_b2) / 2
            
            result = [None] * 3
            result[top_idx] = (photos[top_idx], (x_top, y_top, x_top + w_top, y_top + h_top))
            result[bottom_idxs[0]] = (photos[bottom_idxs[0]], (x_b1, y_bottom, x_b1 + w_b1, y_bottom + h_b1))
            result[bottom_idxs[1]] = (photos[bottom_idxs[1]], (x_b2, y_bottom, x_b2 + w_b2, y_bottom + h_b2))
            return result
    
    def _layout_4(self, photos, aspects):
        """Four photos - 2x2 adaptive grid"""
        base_w = (self.avail_w - self.gap) / 2
        base_h = (self.avail_h - self.gap) / 2
        
        positions = []
        for i, (photo, aspect) in enumerate(zip(photos, aspects)):
            col = i % 2
            row = i // 2
            
            if aspect > 1.5:
                cell_w = base_w * 1.1
                cell_h = base_h * 0.9
            elif aspect < 0.7:
                cell_w = base_w * 0.9
                cell_h = base_h * 1.1
            else:
                cell_w = base_w
                cell_h = base_h
            
            if aspect > cell_w / cell_h:
                w = cell_w
                h = w / aspect
            else:
                h = cell_h
                w = h * aspect
            
            base_x = self.margin + col * (base_w + self.gap)
            base_y = self.margin + (1 - row) * (base_h + self.gap)
            
            x = base_x + (base_w - w) / 2
            y = base_y + (base_h - h) / 2
            
            positions.append((photo, (x, y, x + w, y + h)))
        
        return positions


class BabyPhotoBookGenerator:
    """Baby photo book generator"""
    
    def __init__(self, output_path="baby_photo_book.pdf"):
        self.output_path = output_path
        self.page_width, self.page_height = A4
        self.register_fonts()
        
        self.baby_stages = [
            ("Newborn", 0, 1, "0-1 month"),
            ("Early Infant", 1, 3, "1-3 months"),
            ("Mid Infant", 3, 6, "3-6 months"),
            ("Late Infant", 6, 9, "6-9 months"),
            ("Crawling", 9, 12, "9-12 months"),
            ("Early Toddler", 12, 18, "1-1.5 years"),
            ("Mid Toddler", 18, 24, "1.5-2 years"),
            ("Late Toddler", 24, 36, "2-3 years"),
        ]
        
        self.layout_engine = PhotoLayoutEngine(self.page_width, self.page_height)
    
    def register_fonts(self):
        try:
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/msyh.ttc",
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('Chinese', font_path))
                        self.font_name = 'Chinese'
                        return
                    except:
                        continue
            self.font_name = 'Helvetica'
        except:
            self.font_name = 'Helvetica'
    
    def get_photo_date(self, image_path):
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            if exif:
                for tag in [0x9003, 0x9004, 0x0132]:
                    if tag in exif:
                        try:
                            return datetime.strptime(exif[tag], "%Y:%m:%d %H:%M:%S")
                        except:
                            continue
            timestamp = os.path.getmtime(image_path)
            return datetime.fromtimestamp(timestamp)
        except:
            return datetime.now()
    
    def organize_photos(self, photo_paths, birth_date=None):
        stage_photos = defaultdict(list)
        for photo_path in photo_paths:
            photo_date = self.get_photo_date(photo_path)
            if birth_date:
                age_months = (photo_date.year - birth_date.year) * 12 + \
                           (photo_date.month - birth_date.month)
                stage_name = None
                for name, start, end, range_str in self.baby_stages:
                    if start <= age_months < end:
                        stage_name = f"{name} ({range_str})"
                        break
                key = stage_name or "Other"
                stage_photos[key].append({
                    'path': photo_path, 'date': photo_date, 'age_months': age_months
                })
            else:
                key = photo_date.strftime("%Y-%m")
                stage_photos[key].append({
                    'path': photo_path, 'date': photo_date, 'age_months': None
                })
        return stage_photos
    
    def create_cover(self, c, baby_name):
        c.setFillColor(HexColor("#FFF0F5"))
        c.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)
        c.setFillColor(HexColor("#8B4513"))
        c.setFont(self.font_name, 40)
        c.drawCentredString(self.page_width/2, self.page_height*0.6, f"{baby_name}'s Photo Book")
        c.setFont(self.font_name, 12)
        c.setFillColor(HexColor("#A0522D"))
        c.drawCentredString(self.page_width/2, self.page_height*0.05, 
                           datetime.now().strftime("%Y-%m"))
    
    def create_chapter(self, c, title, count):
        c.setFillColor(HexColor("#FFF5EE"))
        c.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)
        c.setFillColor(HexColor("#8B4513"))
        c.setFont(self.font_name, 28)
        c.drawCentredString(self.page_width/2, self.page_height*0.52, title)
        c.setFont(self.font_name, 10)
        c.setFillColor(HexColor("#A0522D"))
        c.drawCentredString(self.page_width/2, self.page_height*0.45, f"{count} photos")
    
    def draw_photo_page(self, c, layout_result):
        for photo_info, coords in layout_result:
            x1, y1, x2, y2 = coords
            try:
                c.drawImage(photo_info['path'], x1, y1, width=x2-x1, height=y2-y1)
                date_str = photo_info['date'].strftime("%Y-%m-%d")
                if photo_info['age_months']:
                    date_str += f" ({photo_info['age_months']}m)"
                c.setFont(self.font_name, 6)
                c.setFillColor(HexColor("#666666"))
                c.drawCentredString((x1+x2)/2, y1 - 6, date_str)
            except Exception as e:
                print(f"[WARN] Cannot draw: {e}")
    
    def generate(self, photo_folder, baby_name="Baby", birth_date_str=None):
        photo_paths = []
        for file_path in Path(photo_folder).rglob('*'):
            if file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp'}:
                photo_paths.append(str(file_path))
        
        if not photo_paths:
            print("[ERROR] No photos found!")
            return False
        
        print(f"[OK] Found {len(photo_paths)} photos")
        
        birth_date = None
        if birth_date_str:
            try:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            except:
                pass
        
        stage_photos = self.organize_photos(photo_paths, birth_date)
        sorted_stages = sorted(stage_photos.items(), 
                              key=lambda x: self._get_stage_order(x[0]))
        
        c = canvas.Canvas(self.output_path, pagesize=A4)
        self.create_cover(c, baby_name)
        c.showPage()
        
        for stage_name, photos in sorted_stages:
            if not photos:
                continue
            print(f"Processing: {stage_name} ({len(photos)} photos)")
            
            self.create_chapter(c, stage_name, len(photos))
            c.showPage()
            
            photos.sort(key=lambda x: x['date'])
            
            for i in range(0, len(photos), 4):
                page_photos = photos[i:i+4]
                layout_result = self.layout_engine.calculate_layout(page_photos)
                self.draw_photo_page(c, layout_result)
                c.showPage()
        
        c.save()
        print(f"[SUCCESS] Generated: {self.output_path}")
        return True
    
    def _get_stage_order(self, stage_name):
        for i, (name, start, end, range_str) in enumerate(self.baby_stages):
            if name in stage_name:
                return i
        return 999


def main():
    parser = argparse.ArgumentParser(description='Baby Photo Book Generator')
    parser.add_argument('photo_folder', help='Path to photo folder')
    parser.add_argument('--output', '-o', default='baby_photo_book.pdf')
    parser.add_argument('--name', '-n', default='Baby')
    parser.add_argument('--birth', '-b', help='Birth date: YYYY-MM-DD')
    
    args = parser.parse_args()
    
    generator = BabyPhotoBookGenerator(args.output)
    generator.generate(args.photo_folder, args.name, args.birth)


if __name__ == "__main__":
    main()